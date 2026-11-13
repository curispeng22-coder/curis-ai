from __future__ import annotations

import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.shared_workspace_router import build_shared_workspace_router
from app.api.team_operating_router import build_team_operating_router
from app.api.frontend_v1_router import build_frontend_v1_router
from app.database import Database
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.child_work import ChildWorkError
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.tenant_context import TenantContext


TENANT = "tenant-v1-general"
COMPANY = "company-v1-general"
WORKSPACE = "workspace-v1-general"
BUSINESS = "business-v1-general"
EMPLOYEE = "employee-v1-general"


def seed(path):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo', '通用业务公司')",
            (COMPANY, TENANT),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department', ?, ?, 'official.department.software_rnd', '业务部', 'business.general')",
            (TENANT, COMPANY),
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, goal, "
            "lifecycle_status, created_at, updated_at) values (?, ?, ?, 'department', '客户反馈业务', "
            "'形成一个可验证改进', 'DRAFT', current_timestamp, current_timestamp)",
            (BUSINESS, TENANT, COMPANY),
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
            "blueprint_version, status, business_relation_status, business_relation_reason, business_relation_source) "
            "values (?, ?, ?, ?, '客户反馈办公室', ?, 'generic-v1', 'DRAFT', 'RESOLVED', '', 'CANONICAL_TEST')",
            (WORKSPACE, TENANT, COMPANY, BUSINESS, json.dumps({"productForm": "GENERIC"})),
        )
    return database


def add_team(database):
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="agent",
        capability_id="agent.general.local",
        display_name="General local execution",
        metadata={"kind": "accepted-local-provider"},
    )
    with database.connect() as connection:
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values (?, ?, ?, 'department', 'et_product_manager', '小策', '业务负责人', 'idle')",
            (EMPLOYEE, TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
            "values ('binding-general', ?, ?, 'tenant_private', 'agent', 'agent.general.local')",
            (TENANT, EMPLOYEE),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        foundation = RuntimeFoundation(database)
        role = foundation.create(
            "ROLE_SLOT", company_id=COMPANY, workspace_id=WORKSPACE,
            data={"name": "业务负责人", "responsibility": "推进当前业务问题"},
        )
        foundation.create(
            "AI_EMPLOYEE", entity_id=EMPLOYEE, company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="AVAILABLE", data={"name": "小策"},
        )
        routing = ResponsibilityRoutingRuntime(database)
        assignment = routing.create_assignment(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            scope_type="WORKSPACE",
            scope_ref=WORKSPACE,
            role_ref=role["entity_id"],
            employee_ref=EMPLOYEE,
            responsibility_key="business-owner",
            responsibility="推进当前业务问题并返回可验证结果",
            output_contract={"requiresResult": True, "resultType": "general-business-result"},
        )
        routing.publish_workflow(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            scope_type="WORKSPACE",
            scope_ref=WORKSPACE,
            workflow_key="general-operating",
            assignment_refs=[assignment["entity_id"]],
            default_flow=["business-owner"],
        )


def app(database, employee_execution=None):
    value = FastAPI()

    @value.middleware("http")
    async def scope(request: Request, call_next):
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            return await call_next(request)

    value.include_router(build_shared_workspace_router(database))
    value.include_router(build_frontend_v1_router(database))
    if employee_execution is not None:
        value.include_router(build_team_operating_router(database, employee_execution))
    return value


def test_general_command_requires_truth_then_creates_one_canonical_work(tmp_path):
    path = tmp_path / "general-operating.sqlite"
    database = seed(path)
    payload = {
        "problem": "整理本周客户反馈",
        "expected_result": "形成一项有证据的改进建议",
        "constraints": ["只使用已提供资料"],
        "references": ["brief:customer-feedback"],
        "idempotency_key": "first-feedback-work",
    }
    with TestClient(app(database)) as client:
        blocked = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works", json=payload,
        )
        assert blocked.status_code == 409
        assert blocked.json()["detail"]["code"] == "RESPONSIBILITY_UNRESOLVED"
    with database.connect() as connection:
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type in ('CYCLE','WORK')"
        ).fetchone()[0] == 0

    add_team(database)
    with TestClient(app(database)) as client:
        first = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works", json=payload,
        )
        assert first.status_code == 200, first.text
        replay = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works", json=payload,
        )
        assert replay.status_code == 200, replay.text
    first_value, replay_value = first.json(), replay.json()
    assert first_value["cycle"]["entity_id"] == replay_value["cycle"]["entity_id"]
    assert first_value["work"]["entity_id"] == replay_value["work"]["entity_id"]
    assert first_value["work"]["entity_type"] == "WORK"
    assert first_value["work"]["lifecycle_status"] == "ACTIVE"
    route = first_value["work"]["data"]["responsibilityRouting"]
    assert route["responsibilityHolderRef"] == EMPLOYEE
    assert route["currentExecutorRef"] is None
    assert route["status"] == "ACTIVE"

    reopened = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        recovered = GeneralWorkspaceDelivery(reopened).create_work(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            problem=payload["problem"],
            expected_result=payload["expected_result"],
            constraints=payload["constraints"],
            references=payload["references"],
            idempotency_key=payload["idempotency_key"],
        )
        with pytest.raises(ChildWorkError):
            GeneralWorkspaceDelivery(reopened).create_work(
                company_id=COMPANY,
                workspace_id=WORKSPACE,
                problem="另一个问题",
                expected_result=payload["expected_result"],
                constraints=[],
                references=[],
                idempotency_key=payload["idempotency_key"],
            )
    assert recovered["work"]["entity_id"] == first_value["work"]["entity_id"]
    with reopened.connect() as connection:
        assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1
        assert connection.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_general_provider_context_is_bounded_and_waiting_retry_is_durable(tmp_path):
    path = tmp_path / "general-context.sqlite"
    database = seed(path)
    add_team(database)
    with database.connect() as connection:
        connection.execute(
            "update canonical_businesses set positioning='帮助客户把反馈变成低风险改进' where business_id=?",
            (BUSINESS,),
        )
        connection.execute(
            "update workspaces set blueprint_json=? where workspace_id=?",
            (json.dumps({"productForm": "GENERIC", "goal": "持续处理客户反馈"}), WORKSPACE),
        )
    calls = []

    async def employee_execution(payload):
        calls.append(payload)
        attempt = 1 + sum(item["mode"] == "run" for item in calls)
        if payload["mode"] == "submit":
            return {"task_ref": f"task-general-{attempt}"}
        rejected = sum(item["mode"] == "run" for item in calls) == 1
        result = {
            "status": "REJECTED" if rejected else "ACCEPTED",
            "resultType": "general-business-result",
            "summary": "缺少输入" if rejected else "已形成改进建议",
            "problem": "缺少客户反馈数据" if rejected else "",
        }
        return {
            "output": json.dumps(result, ensure_ascii=False),
            "task_status": "COMPLETED",
            "session_ref": f"session-{attempt}",
            "artifact_refs": [],
            "execution_binding": {"callbackProvenance": {"verification_status": "VERIFIED"}},
        }

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        created = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE,
            problem="整理本周客户反馈", expected_result="形成一项有证据的改进建议",
            constraints=["只使用已提供资料"], references=["brief:customer-feedback"],
            idempotency_key="context-retry-work",
        )
    work_ref = created["work"]["entity_id"]
    with TestClient(app(database, employee_execution)) as client:
        first = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
        assert first.status_code == 200, first.text
    prompt = next(item["prompt"] for item in calls if item["mode"] == "submit")
    for expected in (
        "客户反馈业务", "形成一个可验证改进", "帮助客户把反馈变成低风险改进",
        "客户反馈办公室", "持续处理客户反馈", "整理本周客户反馈",
        "形成一项有证据的改进建议", "只使用已提供资料",
        "brief:customer-feedback", "小策", "业务负责人",
    ):
        assert expected in prompt
    assert "UNRELATED_CONVERSATION" not in prompt
    assert len(prompt.encode("utf-8")) < 12_000

    waiting = first.json()["work"]
    route = waiting["data"]["responsibilityRouting"]
    assert route["status"] == "WAITING"
    assert route["responsibilityHolderRef"] == EMPLOYEE
    assert route["currentExecutorRef"] is None
    first_execution = next(iter(route["executions"].values()))
    assert first_execution["status"] == "REJECTED"
    assert first_execution["resultSummary"] == "缺少客户反馈数据 恢复方式：补充所需输入后继续同一工作。"

    restarted = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        recovered = RuntimeFoundation(restarted).get(work_ref)
        assert recovered["data"]["responsibilityRouting"]["executions"] == route["executions"]
        ResponsibilityRoutingRuntime(restarted).route(
            work_ref, signal="CONTINUE", result_refs=["source:customer-feedback"],
        )
    with TestClient(app(restarted, employee_execution)) as client:
        second = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
        assert second.status_code == 200, second.text
        replay = client.post(f"/team-operating/works/{work_ref}/execute?max_executions=1")
        assert replay.status_code == 200, replay.text
    assert second.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED"
    assert sum(item["mode"] == "run" for item in calls) == 2
    second_prompt = [item["prompt"] for item in calls if item["mode"] == "submit"][-1]
    assert "source:customer-feedback" in second_prompt
    executions = second.json()["work"]["data"]["responsibilityRouting"]["executions"]
    assert len(executions) == 2
    assert len({item["taskRef"] for item in executions.values()}) == 2


def test_cross_scope_context_reference_is_rejected_before_employee_execution(tmp_path):
    path = tmp_path / "general-context-isolation.sqlite"
    database = seed(path)
    add_team(database)
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values ('company-foreign', 'tenant-foreign', 'ceo-foreign', 'Foreign')"
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department-foreign', 'tenant-foreign', 'company-foreign', 'official.department.software_rnd', 'Foreign', 'business.general')"
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, created_at, updated_at) "
            "values ('business-foreign', 'tenant-foreign', 'company-foreign', 'department-foreign', 'Foreign', 'DRAFT', current_timestamp, current_timestamp)"
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, blueprint_version, status, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values ('workspace-foreign', 'tenant-foreign', 'company-foreign', 'business-foreign', 'Foreign', '{}', 'generic-v1', 'DRAFT', "
            "'RESOLVED', '', 'TEST')"
        )
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values ('company-other', ?, 'ceo-other', 'Other')",
            (TENANT,),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department-other', ?, 'company-other', 'official.department.software_rnd', 'Other', 'business.general')",
            (TENANT,),
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, created_at, updated_at) "
            "values ('business-other', ?, 'company-other', 'department-other', 'Other', 'DRAFT', current_timestamp, current_timestamp)",
            (TENANT,),
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, blueprint_version, status, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values ('workspace-other', ?, 'company-other', 'business-other', 'Other', '{}', 'generic-v1', 'DRAFT', "
            "'RESOLVED', '', 'TEST')",
            (TENANT,),
        )
    with TenantContext.scope("tenant-foreign", company_id="company-foreign", ceo_id="ceo-foreign", role="test"):
        RuntimeFoundation(database).create(
            "EVIDENCE", entity_id="foreign-evidence", company_id="company-foreign",
            workspace_id="workspace-foreign", data={"summary": "foreign"},
        )
    with TenantContext.scope(TENANT, company_id="company-other", ceo_id="ceo-other", role="test"):
        RuntimeFoundation(database).create(
            "EVIDENCE", entity_id="other-company-evidence", company_id="company-other",
            workspace_id="workspace-other", data={"summary": "other"},
        )
    calls = []

    async def employee_execution(payload):
        calls.append(payload)
        return {"task_ref": "should-not-exist"}

    works = []
    for index, reference in enumerate(("foreign-evidence", "other-company-evidence"), start=1):
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            works.append(GeneralWorkspaceDelivery(database).create_work(
                company_id=COMPANY, workspace_id=WORKSPACE,
                problem="整理反馈", expected_result="形成建议", constraints=[],
                references=[reference], idempotency_key=f"foreign-context-work-{index}",
            )["work"])
    with TestClient(app(database, employee_execution)) as client:
        for work in works:
            response = client.post(f"/team-operating/works/{work['entity_id']}/execute?max_executions=1")
            assert response.status_code == 422
            assert "outside the current Workspace" in response.json()["detail"]
    assert calls == []
    with TenantContext.scope(TENANT):
        for work in works:
            unchanged = RuntimeFoundation(database).get(work["entity_id"])
            assert unchanged["data"]["responsibilityRouting"]["currentExecutorRef"] is None
            assert unchanged["data"]["responsibilityRouting"].get("executions") in (None, {})
