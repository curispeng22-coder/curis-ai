from __future__ import annotations

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-team-operating"
COMPANY = "company-team-operating"
WORKSPACE = "workspace-xhs-team-operating"
BUSINESS = "business-xhs-team-operating"
RD_BUSINESS = "business-rd-team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo-team-operating"}
PREFIX = "/api/workspace/runtime/foundation/team-operating"


def seed(path):
    database = Database(str(path))
    with database.connect() as conn:
        conn.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo-team-operating', 'Team Operating Company')",
            (COMPANY, TENANT),
        )
        for business_id, name in ((BUSINESS, "小红书运营"), (RD_BUSINESS, "研发")):
            conn.execute(
                "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
                "values (?, ?, ?, 'CUSTOM', '可验证结果', 'ACTIVE')",
                (business_id, TENANT, name),
            )
    seed_canonical_business(database, TENANT, COMPANY, BUSINESS)
    seed_canonical_business(database, TENANT, COMPANY, RD_BUSINESS)
    with database.connect() as conn:
        conn.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values (?, ?, ?, ?, 'AI科技', 'OPERATING', 'v1', 'RESOLVED', '', 'CANONICAL_TEST')",
            (WORKSPACE, TENANT, COMPANY, BUSINESS),
        )
    with TenantContext.scope(TENANT):
        foundation = RuntimeFoundation(database)
        employees = {}
        for key in ("leader", "topic", "research", "copy", "visual", "visual-v2", "publish"):
            employees[key] = foundation.create(
                "AI_EMPLOYEE", entity_id=f"employee-{key}", company_id=COMPANY,
                workspace_id=WORKSPACE, lifecycle_status="AVAILABLE", data={"name": key},
            )["entity_id"]
        for key in ("rd-leader", "product", "architect", "developer", "qa"):
            employees[key] = foundation.create(
                "AI_EMPLOYEE", entity_id=f"employee-{key}", company_id=COMPANY,
                lifecycle_status="AVAILABLE", data={"name": key},
            )["entity_id"]
    return database, employees


def role(key, employee, *, leader=False, assignment_ref=None, role_ref=None):
    return {
        "responsibility_key": key,
        "role_name": key,
        "employee_ref": employee,
        "responsibility": f"负责{key}",
        "input_contract": {"requiredRefs": [f"input:{key}"]},
        "output_contract": {"requiresResult": True},
        "is_leader": leader,
        "assignment_ref": assignment_ref,
        "role_ref": role_ref,
    }


def publish(client, *, scope_type, scope_ref, workflow_key, roles, workspace_id=None, default_flow=None):
    response = client.post(
        f"{PREFIX}/definitions/publish", headers=HEADERS,
        json={
            "company_id": COMPANY, "scope_type": scope_type, "scope_ref": scope_ref,
            "workspace_id": workspace_id, "workflow_key": workflow_key, "roles": roles,
            "default_flow": default_flow,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def start(client, work_ref, *, scope_type, scope_ref, workflow_key):
    response = client.post(
        f"{PREFIX}/works/{work_ref}/start", headers=HEADERS,
        json={"scope_type": scope_type, "scope_ref": scope_ref, "workflow_key": workflow_key},
    )
    assert response.status_code == 200, response.text
    return response.json()["work"]


def route(client, work_ref, signal, **values):
    response = client.post(
        f"{PREFIX}/works/{work_ref}/route", headers=HEADERS,
        json={"signal": signal, **values},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_ui_definition_publish_reorder_version_pin_and_content_growth_e2e(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-operating-content.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, employees = seed(path)
        roles_v1 = [
            role("leader", employees["leader"], leader=True), role("topic", employees["topic"]),
            role("research", employees["research"]), role("copy", employees["copy"]),
            role("visual", employees["visual"]), role("publish", employees["publish"]),
        ]
        v1 = publish(
            client, scope_type="WORKSPACE", scope_ref=WORKSPACE, workspace_id=WORKSPACE,
            workflow_key="content-growth", roles=roles_v1,
        )
        assert v1["published"]["version"] == 1
        assert v1["published"]["default_flow"] == ["topic", "research", "copy", "visual", "publish"]

        empty = client.post(
            f"{PREFIX}/definitions/publish", headers=HEADERS,
            json={"company_id": COMPANY, "workspace_id": WORKSPACE, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth", "roles": []},
        )
        assert empty.status_code == 422
        duplicate_assignment = [dict(v1["published"]["roles"][1]), dict(v1["published"]["roles"][1])]
        duplicate_assignment[0] = role(
            "topic", employees["topic"],
            assignment_ref=v1["published"]["roles"][1]["assignmentRef"],
            role_ref=v1["published"]["roles"][1]["roleRef"],
        )
        duplicate_assignment[1] = role(
            "topic-copy", employees["copy"],
            assignment_ref=v1["published"]["roles"][1]["assignmentRef"],
            role_ref=v1["published"]["roles"][1]["roleRef"],
        )
        duplicate = client.post(
            f"{PREFIX}/definitions/publish", headers=HEADERS,
            json={"company_id": COMPANY, "workspace_id": WORKSPACE, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth", "roles": duplicate_assignment},
        )
        assert duplicate.status_code == 422
        assert client.get(
            f"{PREFIX}/definition", headers=HEADERS,
            params={"company_id": COMPANY, "workspace_id": WORKSPACE, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth"},
        ).json()["published"]["version"] == 1

        with TenantContext.scope(TENANT):
            foundation = RuntimeFoundation(database)
            old = foundation.create(
                "CYCLE", entity_id="content-old-v1", company_id=COMPANY, workspace_id=WORKSPACE,
                lifecycle_status="RUNNING", data={"goal": "旧工作继续 v1"},
            )
        old = start(client, old["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="content-growth")
        assert old["data"]["responsibilityRouting"]["workflowVersion"] == 1

        existing = {item["responsibilityKey"]: item for item in v1["published"]["roles"]}
        order_v2 = ["topic", "research", "visual", "copy", "publish", "leader"]
        roles_v2 = []
        for key in order_v2:
            item = existing[key]
            employee = employees["visual-v2"] if key == "visual" else item["employeeRef"]
            edited = role(
                key, employee, leader=item["isLeader"],
                assignment_ref=item["assignmentRef"], role_ref=item["roleRef"],
            )
            if key == "visual":
                edited["responsibility"] = "负责视觉表达与素材验收"
                edited["input_contract"] = {"requiredRefs": ["input:visual-brief", "result:research"]}
                edited["output_contract"] = {"requiresResult": True, "resultType": "visual-package"}
            roles_v2.append(edited)
        v2 = publish(
            client, scope_type="WORKSPACE", scope_ref=WORKSPACE, workspace_id=WORKSPACE,
            workflow_key="content-growth", roles=roles_v2, default_flow=["topic", "research", "visual", "copy", "publish"],
        )
        assert v2["published"]["version"] == 2
        assert v2["published"]["default_flow"] == ["topic", "research", "visual", "copy", "publish"]
        visual = next(item for item in v2["published"]["roles"] if item["responsibilityKey"] == "visual")
        assert visual["employeeRef"] == employees["visual-v2"]
        assert visual["responsibility"] == "负责视觉表达与素材验收"
        assert visual["inputContract"]["requiredRefs"][-1] == "result:research"
        assert visual["outputContract"]["resultType"] == "visual-package"

        with TenantContext.scope(TENANT):
            new = RuntimeFoundation(database).create(
                "CYCLE", entity_id="content-new-v2", company_id=COMPANY, workspace_id=WORKSPACE,
                lifecycle_status="RUNNING", data={"goal": "新工作使用 v2"},
            )
        new = start(client, new["entity_id"], scope_type="WORKSPACE", scope_ref=WORKSPACE, workflow_key="content-growth")
        assert new["data"]["responsibilityRouting"]["workflowVersion"] == 2
        assert old["data"]["responsibilityRouting"]["workflowVersion"] == 1

        first = route(client, new["entity_id"], "COMPLETED", result_refs=["result:topic"])
        assert first["work"]["data"]["responsibilityRouting"]["currentAssignmentRef"] == existing["research"]["assignmentRef"]
        consultation = route(
            client, new["entity_id"], "CONSULT", responsibility_key="leader",
            problem="需要确认内容方向", interaction_key="content-leader-consult",
            bounded_summary="只提供当前选题与目标", evidence_refs=[f"evidence:{index}" for index in range(20)],
        )
        holder = consultation["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"]
        assert holder == employees["research"]
        assert consultation["handoff"] is None
        cost = consultation["consult"]["context"]["cost"]
        assert cost["refsCount"] == 16
        assert cost["hydratedBodiesCount"] == 0
        assert cost["providerTaskCreatedByRouter"] is False
        assert cost["providerSessionCreatedByRouter"] is False
        completed = client.post(
            f"{PREFIX}/works/{new['entity_id']}/consult/content-leader-consult/complete",
            headers=HEADERS, json={"response": "继续当前方向", "result_refs": ["result:leader-guidance"]},
        )
        assert completed.status_code == 200, completed.text
        assert completed.json()["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"] == employees["research"]

        route(client, new["entity_id"], "COMPLETED", result_refs=["result:research"])
        returned = route(
            client, new["entity_id"], "RETURN_OR_REVISION", responsibility_key="copy",
            problem="视觉发现文案需要修订", evidence_refs=["evidence:visual-review"],
        )
        assert returned["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"] == employees["copy"]
        route(client, new["entity_id"], "COMPLETED", result_refs=["result:copy-revision"])
        route(client, new["entity_id"], "COMPLETED", result_refs=["result:publish"])

        persisted = client.get(
            f"{PREFIX}/definition", headers=HEADERS,
            params={"company_id": COMPANY, "workspace_id": WORKSPACE, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth"},
        )
        assert persisted.status_code == 200, persisted.text
        body = persisted.json()
        assert body["published"]["version"] == 2
        assert {item["workflow_version"] for item in body["running_work"]} == {1, 2}
        # A legacy completed Work with stale nested routing is projected without mutating history.
        with database.connect() as conn:
            conn.execute("update runtime_entities set lifecycle_status='COMPLETED', data_json=json_set(data_json, '$.responsibilityRouting.status', 'ACTIVE', '$.responsibilityRouting.currentExecutorRef', 'legacy-executor') where tenant_id=? and entity_id=?",
                         (TENANT, new["entity_id"]))
        reread = client.get(f"{PREFIX}/definition", headers=HEADERS,
            params={"company_id": COMPANY, "workspace_id": WORKSPACE, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth"})
        projected = next(item for item in reread.json()["running_work"] if item["work_ref"] == new["entity_id"])
        assert projected["work_status"] == "COMPLETED" and projected["current_executor_ref"] is None
        with database.connect() as conn:
            assert conn.execute("select json_extract(data_json, '$.responsibilityRouting.status') from runtime_entities where entity_id=?", (new["entity_id"],)).fetchone()[0] == "ACTIVE"
        with database.connect() as conn:
            assert conn.execute("select count(*) from tasks").fetchone()[0] == 0
            assert conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0] == 4
            assert conn.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_business_scope_rd_dynamic_collaboration_and_validation_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-operating-rd.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, employees = seed(path)
        roles = [
            role("leader", employees["rd-leader"], leader=True), role("product", employees["product"]),
            role("architect", employees["architect"]), role("developer", employees["developer"]),
            role("qa", employees["qa"]),
        ]
        published = publish(
            client, scope_type="BUSINESS", scope_ref=RD_BUSINESS,
            workflow_key="rd-default", roles=roles,
        )
        assert published["scope"]["workspace_id"] is None

        invalid = [dict(roles[0]), dict(roles[1])]
        invalid[1]["responsibility_key"] = invalid[0]["responsibility_key"]
        response = client.post(
            f"{PREFIX}/definitions/publish", headers=HEADERS,
            json={"company_id": COMPANY, "scope_type": "BUSINESS", "scope_ref": RD_BUSINESS, "workflow_key": "invalid", "roles": invalid},
        )
        assert response.status_code == 422
        invalid[1]["responsibility_key"] = "product"
        invalid[1]["employee_ref"] = "employee-not-real"
        response = client.post(
            f"{PREFIX}/definitions/publish", headers=HEADERS,
            json={"company_id": COMPANY, "scope_type": "BUSINESS", "scope_ref": RD_BUSINESS, "workflow_key": "invalid", "roles": invalid},
        )
        assert response.status_code == 422

        with TenantContext.scope(TENANT):
            work = RuntimeFoundation(database).create(
                "CYCLE", entity_id="rd-business-cycle", company_id=COMPANY,
                lifecycle_status="RUNNING", data={"goal": "研发动态协作"},
            )
        work = start(client, work["entity_id"], scope_type="BUSINESS", scope_ref=RD_BUSINESS, workflow_key="rd-default")
        for key in ("product", "architect"):
            route(client, work["entity_id"], "COMPLETED", result_refs=[f"result:{key}"])
        assert route(
            client, work["entity_id"], "CONSULT", responsibility_key="product",
            problem="需求边界需要确认", interaction_key="rd-product-consult",
        )["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"] == employees["developer"]
        client.post(
            f"{PREFIX}/works/{work['entity_id']}/consult/rd-product-consult/complete",
            headers=HEADERS, json={"response": "按当前验收边界继续"},
        ).raise_for_status()
        assert route(
            client, work["entity_id"], "CONSULT", responsibility_key="architect",
            problem="实现边界需要确认", interaction_key="rd-architect-consult",
        )["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"] == employees["developer"]
        client.post(
            f"{PREFIX}/works/{work['entity_id']}/consult/rd-architect-consult/complete",
            headers=HEADERS, json={"response": "保持当前实现边界"},
        ).raise_for_status()
        route(client, work["entity_id"], "COMPLETED", result_refs=["result:development"])
        returned = route(
            client, work["entity_id"], "RETURN_OR_REVISION", responsibility_key="developer",
            problem="QA发现缺陷", evidence_refs=["evidence:qa-failure"],
        )
        assert returned["work"]["data"]["responsibilityRouting"]["responsibilityHolderRef"] == employees["developer"]
        route(client, work["entity_id"], "COMPLETED", result_refs=["result:developer-fix"])
        final = route(client, work["entity_id"], "COMPLETED", result_refs=["result:qa-pass"])
        assert final["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED"
        assert final["work"]["data"]["responsibilityRouting"]["currentExecutorRef"] is None

        reopened = Database(str(path))
        with TenantContext.scope(TENANT):
            persisted = RuntimeFoundation(reopened).get(work["entity_id"])
        routing = persisted["data"]["responsibilityRouting"]
        assert routing["status"] == "COMPLETED"
        assert len(routing["collaborations"]) == 2
        with reopened.connect() as conn:
            assert conn.execute("select count(*) from workspaces where business_id=?", (RD_BUSINESS,)).fetchone()[0] == 0
            assert conn.execute("select count(*) from tasks").fetchone()[0] == 0
            assert conn.execute("select count(*) from runtime_entities where entity_type='HANDOFF'").fetchone()[0] == 5
            assert conn.execute("pragma integrity_check").fetchone()[0] == "ok"
