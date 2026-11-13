from __future__ import annotations

import hashlib
import json

from fastapi.testclient import TestClient

from app.database import Database
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.result_store import ResultStore
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import (
    COMPANY,
    EMPLOYEE,
    TENANT,
    WORKSPACE,
    add_team,
    app,
    seed,
)


def test_general_workspace_truthfully_stops_before_inventing_a_team(tmp_path):
    database = seed(tmp_path / "general-p1-gap.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        view = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
    assert view["operating_readiness"] == {
        "status": "NEEDS_DECISION",
        "reason": "尚未形成唯一的团队责任安排",
        "workflow_key": None,
        "owner": "CEO",
        "next_action": "确认团队责任与员工",
    }
    with TestClient(app(database)) as client:
        response = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works",
            json={
                "problem": "整理客户反馈",
                "expected_result": "形成可验证建议",
                "constraints": [],
                "references": [],
                "idempotency_key": "p1-gap",
            },
        )
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "RESPONSIBILITY_UNRESOLVED"
    with database.connect() as connection:
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type in ('CYCLE','WORK')"
        ).fetchone()[0] == 0


def test_general_workspace_projects_real_routing_result_and_restart(tmp_path):
    path = tmp_path / "general-p1-operating.sqlite"
    database = seed(path)
    add_team(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        evidence = RuntimeFoundation(database).create(
            "EVIDENCE", company_id=COMPANY, workspace_id=WORKSPACE,
            data={"summary": "本地执行回调已验证"},
        )
        created = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            problem="整理客户反馈",
            expected_result="形成可验证建议",
            constraints=["只使用已提供资料"],
            references=[],
            idempotency_key="p1-operating",
        )

    async def employee_execution(payload):
        if payload["mode"] == "submit":
            return {"task_ref": "task-general-p1"}
        return {
            "output": json.dumps({
                "status": "ACCEPTED",
                "resultType": "general-business-result",
                "summary": "已形成一项可验证建议",
                "problem": "",
            }, ensure_ascii=False),
            "task_status": "COMPLETED",
            "session_ref": "session-general-p1",
            "artifact_refs": [],
            "execution_binding": {"callbackProvenance": {
                "verification_status": "VERIFIED",
                "evidence_event_ref": evidence["entity_id"],
            }},
        }

    with TestClient(app(database, employee_execution)) as client:
        response = client.post(
            f"/team-operating/works/{created['work']['entity_id']}/execute?max_executions=1"
        )
    assert response.status_code == 200

    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        view = SharedWorkspaceProjection(reopened).general_workspace(COMPANY, WORKSPACE)
    item = view["current_work"][0]
    assert item["work_ref"] == created["work"]["entity_id"]
    assert item["problem"] == "整理客户反馈"
    assert item["expected_result"] == "形成可验证建议"
    assert item["status"] == "COMPLETED"
    assert item["responsibility_holder_ref"] == EMPLOYEE
    assert item["responsibility_holder_name"] == "小策"
    assert item["current_executor_ref"] is None
    assert item["result_refs"] == ["task:task-general-p1"]
    assert item["evidence_refs"] == [evidence["entity_id"]]
    assert item["recovery_action"] == "当前工作已收口"


def test_general_workspace_retries_the_same_waiting_work_without_duplicate_active_execution(tmp_path):
    database = seed(tmp_path / "general-p1-retry.sqlite")
    add_team(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        work_ref = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE,
            problem="整理客户反馈", expected_result="形成可验证建议",
            constraints=[], references=[], idempotency_key="p1-retry",
        )["work"]["entity_id"]

    attempts = 0

    async def employee_execution(payload):
        nonlocal attempts
        if payload["mode"] == "submit":
            attempts += 1
            return {"task_ref": f"task-retry-{attempts}"}
        verified = attempts == 2
        return {
            "output": json.dumps({
                "status": "ACCEPTED", "resultType": "general-business-result",
                "summary": "重试后完成", "problem": "",
            }, ensure_ascii=False),
            "task_status": "COMPLETED", "session_ref": f"session-retry-{attempts}",
            "artifact_refs": [],
            "execution_binding": {"callbackProvenance": {
                "verification_status": "VERIFIED" if verified else "UNVERIFIED",
            }},
        }

    with TestClient(app(database, employee_execution)) as client:
        first = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
        assert first.status_code == 200
        assert first.json()["work"]["data"]["responsibilityRouting"]["status"] == "WAITING"
        second = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
        assert second.status_code == 200
        assert second.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED"
    assert attempts == 2


def _add_materializable_team(database):
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="agent", capability_id="agent.general.team",
        display_name="General team local execution", metadata={"kind": "accepted-local-provider"},
    )
    members = (
        ("employee-general-leader", "林总", "业务负责人", "leader", True),
        ("employee-general-research", "小研", "研究员工", "research", False),
        ("employee-general-delivery", "小成", "交付员工", "delivery", False),
    )
    with database.connect() as connection:
        for employee_ref, name, role, _, _ in members:
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                "values (?, ?, ?, 'department', 'et_product_manager', ?, ?, 'idle')",
                (employee_ref, TENANT, COMPANY, name, role),
            )
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
                "values (?, ?, ?, 'tenant_private', 'agent', 'agent.general.team')",
                (f"binding-{employee_ref}", TENANT, employee_ref),
            )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        foundation = RuntimeFoundation(database)
        routing = ResponsibilityRoutingRuntime(database)
        for employee_ref, name, role_name, responsibility_key, is_leader in members:
            role = foundation.create(
                "ROLE_SLOT", company_id=COMPANY, workspace_id=WORKSPACE,
                data={"name": role_name, "responsibility": f"承担{role_name}责任"},
            )
            foundation.create(
                "AI_EMPLOYEE", entity_id=employee_ref, company_id=COMPANY, workspace_id=WORKSPACE,
                lifecycle_status="AVAILABLE", data={"name": name, "companyEmployeeRef": employee_ref},
            )
            routing.create_assignment(
                company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
                role_ref=role["entity_id"], employee_ref=employee_ref,
                responsibility_key=responsibility_key, responsibility=f"承担{role_name}责任",
                output_contract={"requiresResult": True, "resultType": "general-business-result"},
                is_leader=is_leader,
            )
    return members


def test_general_workspace_materializes_existing_team_once_and_preserves_empty_truth(tmp_path):
    path = tmp_path / "general-p1-team.sqlite"
    database = seed(path)
    with TestClient(app(database)) as client:
        blocked = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/materialize"
        )
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["code"] == "TEAM_TRUTH_INCOMPLETE"
    _add_materializable_team(database)
    with TestClient(app(database)) as client:
        first = client.post(f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/materialize")
        replay = client.post(f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/materialize")
    assert first.status_code == replay.status_code == 200
    assert first.json()["created"] is True
    assert replay.json()["created"] is False
    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        recovered = GeneralWorkspaceDelivery(reopened).materialize_team(
            company_id=COMPANY, workspace_id=WORKSPACE,
        )
    assert recovered["created"] is False
    with reopened.connect() as connection:
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='RESPONSIBILITY_WORKFLOW'"
        ).fetchone()[0] == 1
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'"
        ).fetchone()[0] == 3


def test_general_workspace_handoff_p7_and_result_utility_share_canonical_truth(tmp_path):
    path = tmp_path / "general-p1-complete.sqlite"
    database = seed(path)
    _add_materializable_team(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        delivery = GeneralWorkspaceDelivery(database)
        delivery.materialize_team(company_id=COMPANY, workspace_id=WORKSPACE)
        created = delivery.create_work(
            company_id=COMPANY, workspace_id=WORKSPACE, problem="研究并形成改进方案",
            expected_result="形成可回访结果", constraints=[], references=[], idempotency_key="p1-team-work",
        )
    task_ids = {}

    async def employee_execution(payload):
        employee_ref = payload["runtime_employee_ref"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            store = ResultStore(database)
            if payload["mode"] == "submit":
                task = store.create_task(
                    f"{employee_ref}处理当前工作", company_id=COMPANY, workspace_id=WORKSPACE,
                    work_ref=payload["work_ref"], execution_ref=payload["execution_key"],
                    capability_source="tenant_private", capability_type="agent",
                    capability_id="agent.general.team", employee_id=employee_ref,
                )
                task_ids[employee_ref] = task["task_id"]
                return {"task_ref": task["task_id"]}
            task = store.transition(
                task_ids[employee_ref], "COMPLETED",
                {"output": json.dumps({
                    "status": "ACCEPTED", "resultType": "general-business-result",
                    "summary": f"{employee_ref}已完成", "problem": "",
                }, ensure_ascii=False)},
            )
            artifacts = store.list_artifacts(task_id=task["task_id"])
            return {
                "output": task["output"], "task_status": "COMPLETED",
                "session_ref": f"session-{employee_ref}",
                "artifact_refs": [item["artifact_id"] for item in artifacts],
                "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}},
            }

    work_ref = created["work"]["entity_id"]
    with TestClient(app(database, employee_execution)) as client:
        completed = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=16")
        assert completed.status_code == 200, completed.text
        view = client.get(f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general").json()
    work = view["current_work"][0]
    assert work["status"] == "COMPLETED"
    assert len(work["handoffs"]) == 1
    assert work["handoffs"][0]["status"] == "COMPLETED"
    assert work["handoffs"][0]["from_employee_name"] in {"小研", "小成"}
    assert work["handoffs"][0]["to_employee_name"] in {"小研", "小成"}
    assert work["handoffs"][0]["from_employee_name"] != work["handoffs"][0]["to_employee_name"]
    assert len(work["result_refs"]) == 2
    assert len(work["result_summaries"]) >= 2
    first_result = work["result_refs"][0]
    with TestClient(app(database)) as client:
        detail = client.get(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/results/{first_result}"
        )
    assert detail.status_code == 200, detail.text
    assert detail.json()["kind"] == "RESULT"
    assert detail.json()["verification_status"] == "VERIFIED"
    assert detail.json()["artifact_refs"]

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        decision_work = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE, problem="决定是否采用高风险方案",
            expected_result="CEO给出明确选择", constraints=[], references=[], idempotency_key="p1-decision-work",
        )
    decision_ref = decision_work["work"]["entity_id"]
    packet = {
        "decisionKey": "general-risk-choice", "complexity": "HIGH_RISK",
        "event": "当前方案会改变对外承诺", "cannotDecideReason": "这是不可逆的业务取舍",
        "ceoChoicePrompt": "选择稳妥方案还是推进高风险方案？", "continuationPlan": "恢复原责任并自动继续",
        "options": [
            {"optionId": "SAFE", "label": "采用稳妥方案", "impact": {"value": "影响较小", "provenance": "EST"}, "risk": {"value": "风险较低", "provenance": "EST"}, "cost": {"value": "成本未知", "provenance": "UNK"}},
            {"optionId": "BOLD", "label": "推进高风险方案", "impact": {"value": "影响未知", "provenance": "UNK"}, "risk": {"value": "风险较高", "provenance": "EST"}, "cost": {"value": "成本未知", "provenance": "UNK"}},
        ],
        "recommendation": {"optionId": "SAFE", "provenance": "EST"},
        "recommendationReason": {"value": "现有证据不足", "provenance": "EVIDENCE"},
    }
    with TestClient(app(database)) as client:
        requested = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{decision_ref}/decision",
            json=packet,
        )
        assert requested.status_code == 200, requested.text
        packet_ref = requested.json()["decision"]["entity_id"]
        duplicate = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{decision_ref}/decision",
            json=packet,
        )
        attention = client.get(f"/api/workspace/v1/companies/{COMPANY}/attention").json()
        assert duplicate.json()["decision"]["entity_id"] == packet_ref
        assert any(item["source_ref"] == packet_ref for item in attention["items"])
        blocked = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{decision_ref}/decision/choose",
            json={"choice": "SAFE", "reason": "CEO选择稳妥方案"},
        )
        assert blocked.status_code == 422
        reviewed = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{decision_ref}/decision/review"
        )
        assert reviewed.status_code == 200
        chosen = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{decision_ref}/decision/choose",
            json={"choice": "SAFE", "reason": "CEO选择稳妥方案"},
        )
        assert chosen.status_code == 200, chosen.text
    assert chosen.json()["decision"]["entity_id"] == packet_ref
    assert chosen.json()["decision"]["lifecycle_status"] == "APPLIED"
    assert chosen.json()["work"]["data"]["responsibilityRouting"]["status"] == "ACTIVE"
    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        persisted = RuntimeFoundation(reopened).get(packet_ref)
    assert persisted["data"]["choice"] == "SAFE"


def test_recruited_employee_assignment_uses_verified_default_model_and_survives_restart(tmp_path):
    path = tmp_path / "general-assignment.sqlite"
    database = seed(path)
    model_name = "deepseek-chat"
    model_key = f"user.deepseek.{hashlib.sha256(model_name.encode()).hexdigest()[:16]}"
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="model", capability_id=model_key,
        display_name=model_name, status="active",
        metadata={
            "provider_type": "deepseek", "model_name": model_name,
            "discovery_verification": {
                "status": "verified", "provider_id": "deepseek", "discovery_id": model_name,
                "model_id": model_name, "requires_credential": False,
            },
        },
    )
    database.save_tenant_model_preference(
        tenant_id=TENANT, model_key=model_key, gateway_ref="deepseek",
        model_name=model_name, source="tenant_private",
    )
    with database.connect() as connection:
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('employee-recruited', ?, ?, '', 'et_product_manager', '小策', '业务经理', 'idle')",
            (TENANT, COMPANY),
        )
    with TestClient(app(database)) as client:
        candidates = client.get(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/candidates",
        )
        payload = {"employee_id": "employee-recruited", "responsibility": "推进客户反馈并返回可验证结果"}
        first = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/assign", json=payload,
        )
        replay = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/team/assign", json=payload,
        )
        created = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works",
            json={
                "problem": "整理客户反馈", "expected_result": "形成可验证建议",
                "constraints": [], "references": [], "idempotency_key": "assigned-work",
            },
        )
    assert candidates.status_code == 200
    assert candidates.json()["employees"][0]["capability_status"] == "AVAILABLE"
    assert first.status_code == replay.status_code == 200
    assert first.json()["created"] is True
    assert replay.json()["created"] is False
    assert created.status_code == 200
    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        delivery = GeneralWorkspaceDelivery(reopened)
        recovered = delivery.assign_employee(
            company_id=COMPANY, workspace_id=WORKSPACE, employee_id="employee-recruited",
            responsibility="推进客户反馈并返回可验证结果",
        )
        identity = delivery.identities.resolve(
            company_id=COMPANY, workspace_id=WORKSPACE, runtime_employee_ref="employee-recruited",
        )
    assert recovered["created"] is False
    assert identity["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE"
    with reopened.connect() as connection:
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'"
        ).fetchone()[0] == 1
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='RESPONSIBILITY_WORKFLOW'"
        ).fetchone()[0] == 1


# The real assign path intentionally keeps AI_EMPLOYEE at Company scope.
def _assigned_company_projection_fixture(path):
    database = seed(path)
    model_name = "deepseek-chat"
    model_key = f"user.deepseek.{hashlib.sha256(model_name.encode()).hexdigest()[:16]}"
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="model", capability_id=model_key,
        display_name=model_name, status="active",
        metadata={
            "provider_type": "deepseek", "model_name": model_name,
            "discovery_verification": {
                "status": "verified", "provider_id": "deepseek", "discovery_id": model_name,
                "model_id": model_name, "requires_credential": False,
            },
        },
    )
    database.save_tenant_model_preference(
        tenant_id=TENANT, model_key=model_key, gateway_ref="deepseek",
        model_name=model_name, source="tenant_private",
    )
    with database.connect() as connection:
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('employee-recruited', ?, ?, '', 'et_product_manager', '小策', '业务经理', 'idle')",
            (TENANT, COMPANY),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        assigned = GeneralWorkspaceDelivery(database).assign_employee(
            company_id=COMPANY, workspace_id=WORKSPACE, employee_id="employee-recruited",
            responsibility="推进客户反馈并返回可验证结果",
        )
    return database, assigned


def test_company_assignment_projection_is_complete_pure_and_survives_reopen(tmp_path, monkeypatch):
    path = tmp_path / "company-projection.sqlite"
    database, assigned = _assigned_company_projection_fixture(path)
    before = path.read_bytes()
    original_connect = database.connect
    from contextlib import contextmanager
    @contextmanager
    def readonly_connect():
        with original_connect() as connection:
            connection.execute("pragma query_only=on")
            yield connection
    monkeypatch.setattr(database, "connect", readonly_connect)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        projection = SharedWorkspaceProjection(database)
        first = projection.general_workspace(COMPANY, WORKSPACE)
        assert projection.general_workspace(COMPANY, WORKSPACE) == first
        assert GeneralWorkspaceDelivery(database).assign_employee(
            company_id=COMPANY, workspace_id=WORKSPACE, employee_id="employee-recruited",
            responsibility="推进客户反馈并返回可验证结果",
        )["created"] is False
        assert RuntimeFoundation(database).get("employee-recruited")["workspace_id"] is None
        reopened = SharedWorkspaceProjection(Database(str(path))).general_workspace(COMPANY, WORKSPACE)
    assert path.read_bytes() == before
    assert reopened == first
    assert first["operating_readiness"]["status"] == "READY_FOR_WORK"
    assert [e["employee_ref"] for e in first["team"]["employees"]] == ["employee-recruited"]
    employee = first["team"]["employees"][0]
    assert employee["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE"
    assert employee["identity_bridge"]["status"] == "VERIFIED"
    role = first["team"]["role_slots"][0]
    assert role["assigned_employee_ref"] == "employee-recruited"
    assert role["assigned_employee_exists"] is True
    assert employee["role_slot_ref"] == role["role_slot_ref"]
    assert first["team"]["capability_bindings"] == []  # Runtime bindings are a different layer.
    assert first["current_work"] == []
    with database.connect() as connection:
        assert connection.execute("select count(*) from employee_capability_bindings where employee_id='employee-recruited'").fetchone()[0] == 1
        assert connection.execute("select count(*) from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchone()[0] == 1


def test_company_employee_team_metadata_does_not_expand_workspace_results_or_projects(tmp_path, monkeypatch):
    database, _ = _assigned_company_projection_fixture(tmp_path / "team-only.sqlite")
    with database.connect() as connection:
        row = connection.execute("select data_json from runtime_entities where entity_id='employee-recruited'").fetchone()
        data = json.loads(row[0]) | {"projectRef": "foreign-project", "resultRefs": ["foreign-result"]}
        connection.execute("update runtime_entities set data_json=? where entity_id='employee-recruited'", (json.dumps(data),))
    projection = SharedWorkspaceProjection(database)
    original_projects, original_result = projection._projects, projection._result
    def projects(company, refs):
        assert "foreign-project" not in refs
        return original_projects(company, refs)
    def result(company, workspace, ref, **options):
        assert ref != "foreign-result"
        return original_result(company, workspace, ref, **options)
    monkeypatch.setattr(projection, "_projects", projects)
    monkeypatch.setattr(projection, "_result", result)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        assert projection.general_workspace(COMPANY, WORKSPACE)["operating_readiness"]["status"] == "READY_FOR_WORK"


import pytest


@pytest.mark.parametrize("corruption", [
    "missing_bridge", "wrong_bridge", "disabled_binding", "disabled_employee", "other_tenant",
    "other_company", "other_workspace", "wrong_assignment_scope", "missing_assignment",
    "inactive_assignment", "stale_revision", "wrong_snapshot_employee", "unpublished_workflow",
    "duplicate_workflow_version", "conflicting_role",
])
def test_company_assignment_projection_refuses_invalid_scope_and_identity(tmp_path, corruption):
    from app.runtime import RuntimeScopeError
    database, assigned = _assigned_company_projection_fixture(tmp_path / f"{corruption}.sqlite")
    assignment_ref = assigned["assignment"]["entity_id"]
    workflow_ref = assigned["workflow"]["entity_id"]
    role_ref = assigned["assignment"]["data"]["roleRef"]
    with database.connect() as connection:
        def data_change(ref, change):
            row = connection.execute("select data_json from runtime_entities where entity_id=?", (ref,)).fetchone()
            data = json.loads(row[0]); change(data)
            connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), ref))
        if corruption == "missing_bridge": data_change("employee-recruited", lambda d: d.pop("identityBridge"))
        elif corruption == "wrong_bridge": data_change("employee-recruited", lambda d: d["identityBridge"].update(companyEmployeeRef="other"))
        elif corruption == "disabled_binding": connection.execute("update employee_capability_bindings set enabled=0 where employee_id='employee-recruited'")
        elif corruption == "disabled_employee": connection.execute("update employee_instances set enabled=0 where id='employee-recruited'")
        elif corruption in {"other_tenant", "other_company", "other_workspace"}:
            column = {"other_tenant":"tenant_id", "other_company":"company_id", "other_workspace":"workspace_id"}[corruption]
            connection.execute(f"update runtime_entities set {column}='other' where entity_id='employee-recruited'")
        elif corruption == "wrong_assignment_scope": data_change(assignment_ref, lambda d: d.update(scopeRef="other"))
        elif corruption == "missing_assignment": connection.execute("delete from runtime_entities where entity_id=?", (assignment_ref,))
        elif corruption == "inactive_assignment": connection.execute("update runtime_entities set lifecycle_status='INACTIVE' where entity_id=?", (assignment_ref,))
        elif corruption == "stale_revision": data_change(assignment_ref, lambda d: d.update(revision=2))
        elif corruption == "wrong_snapshot_employee": data_change(workflow_ref, lambda d: d["assignments"][0].update(employeeRef="other"))
        elif corruption == "unpublished_workflow": connection.execute("update runtime_entities set lifecycle_status='DRAFT' where entity_id=?", (workflow_ref,))
        elif corruption == "duplicate_workflow_version":
            columns = [row[1] for row in connection.execute("pragma table_info(runtime_entities)")]
            values = dict(connection.execute("select * from runtime_entities where entity_id=?", (workflow_ref,)).fetchone())
            values["entity_id"] = "duplicate-workflow"
            connection.execute(f"insert into runtime_entities({','.join(columns)}) values ({','.join('?' for _ in columns)})", [values[col] for col in columns])
        elif corruption == "conflicting_role": data_change(role_ref, lambda d: d.update(assignedEmployeeRef="other"))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        with pytest.raises(RuntimeScopeError, match="General team assignment"):
            SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
