from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.runtime_foundation_router import build_runtime_foundation_router
from app.database import Database
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation
from app.runtime.models import ensure_ceo_day_schema
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext


TENANT = "tenant-shared-workspace"
COMPANY = "company-shared-workspace"
OTHER_COMPANY = "company-other"
WORKSPACE = "workspace-shared-workspace"
OTHER_WORKSPACE = "workspace-other"
CEO = "ceo-shared-workspace"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


def _seed(path):
    database = Database(str(path))
    database.initialize()
    ensure_ceo_day_schema(database)
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Shared Company')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Other Company')",
            (OTHER_COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
            "values ('business-shared', ?, '客户反馈业务', 'CUSTOM', '形成可回访结果', 'OPERATING')",
            (TENANT,),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department-business', ?, ?, 'template-business', '客户成功部', 'customer_success')",
            (TENANT, COMPANY),
        )
        for business_id, name in (("business-shared", "客户反馈业务"), ("business-other", "其他业务")):
            connection.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
                "lifecycle_status, created_at, updated_at) values (?, ?, ?, 'department-business', ?, "
                "'ACTIVE', current_timestamp, current_timestamp)",
                (business_id, TENANT, COMPANY, name),
            )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values (?, ?, ?, 'business-shared', '客户反馈办公室', 'OPERATING', 'v1', 'RESOLVED', '', 'CANONICAL_TEST')",
            (WORKSPACE, TENANT, COMPANY),
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values (?, ?, ?, 'business-other', '其他办公室', 'DRAFT', 'v1', 'RESOLVED', '', 'CANONICAL_TEST')",
            (OTHER_WORKSPACE, TENANT, COMPANY),
        )
        connection.execute(
            "insert into projects(project_id, tenant_id, company_id, name, goal, status) "
            "values ('project-shared', ?, ?, '反馈改进', '完成可验证修复', 'active')",
            (TENANT, COMPANY),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values ('department-rd', ?, ?, 'template-rd', '研发部', 'software_rnd')",
            (TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('employee-developer', ?, ?, 'department-rd', 'template-developer', '陈真', '研发工程师', 'idle')",
            (TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_affiliations(id, tenant_id, employee_id, department_id, project_id) "
            "values ('aff-developer', ?, 'employee-developer', 'department-rd', 'project-shared')",
            (TENANT,),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values ('employee-reviewer', ?, ?, '', 'template-reviewer', '错误公司审核员', '审核员', 'idle')",
            (TENANT, OTHER_COMPANY),
        )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        foundation = RuntimeFoundation(database)
        foundation.create(
            "ROLE_SLOT", entity_id="role-developer", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="ASSIGNED",
            data={
                "name": "研发工程师", "responsibility": "处理当前修复",
                "assignedEmployeeRef": "employee-developer", "capabilityRefs": ["requirement:codex"],
            },
        )
        foundation.create(
            "AI_EMPLOYEE", entity_id="employee-developer", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="AVAILABLE", presence_state="AVAILABLE",
            data={"name": "陈真", "roleSlotRef": "role-developer", "responsibility": "处理当前修复"},
        )
        foundation.create(
            "ROLE_SLOT", entity_id="role-reviewer", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="ASSIGNED",
            data={
                "name": "代码审核员", "responsibility": "审核执行结果",
                "assignedEmployeeRef": "employee-reviewer", "capabilityRefs": [],
            },
        )
        foundation.create(
            "AI_EMPLOYEE", entity_id="employee-reviewer", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="OPERATING", presence_state="RUNNING",
            data={"name": "林审", "roleSlotRef": "role-reviewer", "responsibility": "审核执行结果"},
        )
        foundation.create(
            "CAPABILITY_BINDING", entity_id="binding-codex", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="ACTIVE", verification_status="VERIFIED", capability_ref="requirement:codex",
            data={
                "name": "研发执行能力", "requirementRef": "requirement:codex",
                "authorizationStatus": "AUTHORIZED_ACTIVE",
                "supplyReview": {
                    "source": "tenant_private", "capabilityType": "agent",
                    "capabilityId": "agent.local", "blockers": [],
                },
            },
        )
        store = ResultStore(database)
        task = store.create_task(
            "修复受控函数", company_id=COMPANY, project_id="project-shared",
            employee_id="employee-developer", employee_role="研发工程师", employee_name="陈真",
        )
        completed = store.transition(task["task_id"], "COMPLETED", {"output": "函数已修复，测试通过"})
        artifact = store.list_artifacts(task_id=completed["task_id"])[0]
        evidence = foundation.create(
            "EVIDENCE", entity_id="evidence-shared", company_id=COMPANY, workspace_id=WORKSPACE,
            parent_id="cycle-shared", verification_status="VERIFIED", evidence_condition="CURRENT",
            data={"summary": "测试通过", "artifactRefs": [artifact["artifact_id"]]},
        )
        foundation.create(
            "CYCLE", entity_id="cycle-shared", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", owner_ref=CEO, execution_ref="rd_task:auto",
            data={
                "projectRef": "project-shared",
                "workContext": {
                    "objectOwnerRef": CEO, "responsibilityEmployeeRef": "employee-developer",
                    "responsibilityRoleSlotRef": "role-developer", "currentExecutorRef": None,
                    "status": "waiting", "activity": "等待验证环境恢复",
                    "systemActivity": {"kind": "TEST_ENVIRONMENT", "status": "waiting", "label": "等待测试环境"},
                },
                "artifactRefs": [artifact["artifact_id"]], "evidenceRefs": [evidence["entity_id"]],
                "resultRefs": [artifact["artifact_id"], evidence["entity_id"]],
                "computerAccess": {
                    "requested_intent": "AUTO_WITHIN_BOUNDARY", "configured_state": "CONFIGURED",
                    "effective_state": "UNKNOWN", "verification_state": "UNVERIFIED",
                },
            },
        )
        foundation.create(
            "CONTENT_ITEM", entity_id="work-review", company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="DRAFT", owner_ref=CEO,
            data={
                "workContext": {
                    "responsibilityEmployeeRef": "employee-reviewer", "responsibilityRoleSlotRef": "role-reviewer",
                    "currentExecutorRef": "employee-reviewer", "status": "working", "activity": "审核变更说明",
                },
            },
        )
        other_task = store.create_task("其他公司的结果", company_id=OTHER_COMPANY)
        other_task = store.transition(other_task["task_id"], "COMPLETED", {"output": "不可跨公司读取"})
        other_artifact = store.list_artifacts(task_id=other_task["task_id"])[0]
        unrelated_task = store.create_task("同公司其他空间结果", company_id=COMPANY)
        unrelated_task = store.transition(unrelated_task["task_id"], "COMPLETED", {"output": "不可跨空间读取"})
        unrelated_artifact = store.list_artifacts(task_id=unrelated_task["task_id"])[0]
    return database, artifact["artifact_id"], other_artifact["artifact_id"], unrelated_artifact["artifact_id"]


def _app(database):
    app = FastAPI()

    @app.middleware("http")
    async def tenant_scope(request: Request, call_next):
        with TenantContext.scope(
            request.headers.get("X-Tenant-Id", TENANT), company_id=COMPANY,
            ceo_id=request.headers.get("X-Ceo-Id", CEO), role="test",
        ):
            return await call_next(request)

    app.include_router(build_runtime_foundation_router(database))
    return app


def test_shared_projection_is_truthful_scoped_and_restartable(tmp_path):
    path = tmp_path / "shared.sqlite"
    database, artifact_ref, other_artifact_ref, unrelated_artifact_ref = _seed(path)

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        direct = SharedWorkspaceProjection(database).workspace(COMPANY, WORKSPACE)
    developer = next(item for item in direct["team"]["employees"] if item["employee_ref"] == "employee-developer")
    reviewer = next(item for item in direct["team"]["employees"] if item["employee_ref"] == "employee-reviewer")
    assert direct["business"]["resolved"] is True
    assert developer["ui_status"]["code"] == "blocked"
    assert developer["current_execution"] is None
    assert developer["current_responsibilities"][0]["responsibility_holder_ref"] == "employee-developer"
    assert developer["composer"]["agent_backed"] is True
    assert developer["composer"]["computer_access"]["configured_state"] == "CONFIGURED"
    assert developer["composer"]["computer_access"]["effective_state"] == "UNKNOWN"
    assert reviewer["ui_status"]["code"] == "working"
    assert developer["organization_record"]["identity_status"] == "EXACT_ID_MATCH"
    assert developer["organization_record"]["primary_department"]["name"] == "研发部"
    assert developer["organization_record"]["affiliations"][0]["project"]["project_id"] == "project-shared"
    assert reviewer["organization_record"] is None
    assert direct["system_activity"] == [{
        "object_ref": "cycle-shared", "kind": "TEST_ENVIRONMENT",
        "status": "waiting", "label": "等待测试环境",
    }]
    assert {item["kind"] for item in direct["results"]} == {"ARTIFACT", "EVIDENCE"}

    with TestClient(_app(database)) as client:
        response = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared",
            headers=HEADERS,
        )
        assert response.status_code == 200, response.text
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/results/{artifact_ref}",
            headers=HEADERS,
        )
        assert detail.status_code == 200, detail.text
        assert detail.json()["content"] == "函数已修复，测试通过"
        assert client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/results/{other_artifact_ref}",
            headers=HEADERS,
        ).status_code == 404
        assert client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/results/{unrelated_artifact_ref}",
            headers=HEADERS,
        ).status_code == 404
        assert client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/employees/missing",
            headers=HEADERS,
        ).status_code == 404
        employee_detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/employees/employee-developer",
            headers=HEADERS,
        )
        assert employee_detail.status_code == 200, employee_detail.text
        assert employee_detail.json()["organization"]["workspace"]["workspace_id"] == WORKSPACE
        assert employee_detail.json()["organization"]["exact_company_employee"]["primary_department"]["name"] == "研发部"
        assert employee_detail.json()["recent_result_refs"] == [artifact_ref, "evidence-shared"]

    restarted = Database(str(path))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        recovered = SharedWorkspaceProjection(restarted).workspace(COMPANY, WORKSPACE)
    assert recovered == direct
    with restarted.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []


def test_canonical_work_lifecycle_precedes_stale_responsibility():
    from app.shared_workspace_projection import canonical_work_status
    for lifecycle in ("PLANNED", "READY", "WAITING", "BLOCKED", "FAILED", "PAUSED", "CANCELLED", "ARCHIVED", "COMPLETED"):
        assert canonical_work_status({"lifecycle_status": lifecycle, "data": {"responsibilityRouting": {"status": "EXECUTING"}}}) == lifecycle
    assert canonical_work_status({"lifecycle_status": "ACTIVE", "data": {"responsibilityRouting": {"status": "WAITING_DECISION"}}}) == "WAITING_DECISION"
    assert canonical_work_status({"lifecycle_status": "NEW_UNKNOWN", "data": {"responsibilityRouting": {"status": "ACTIVE"}}}) == "UNKNOWN"


def test_terminal_work_projection_does_not_keep_old_executor_or_rewrite_history():
    from copy import deepcopy
    original = {'entity_id': 'completed-work', 'entity_type': 'WORK', 'lifecycle_status': 'COMPLETED',
        'owner_ref': CEO, 'data': {'workContext': {'responsibilityEmployeeRef': 'employee-owner',
            'currentExecutorRef': 'employee-old', 'status': 'working'},
            'responsibilityRouting': {'status': 'ACTIVE', 'currentExecutorRef': 'employee-old'}, 'resultRefs': ['task:original']}}
    before = deepcopy(original)
    projected = SharedWorkspaceProjection._work_items([original], [], [])[0]
    assert projected['current_executor_ref'] is None
    assert projected['responsibility_holder_ref'] == 'employee-owner'
    assert projected['work_status'] == 'completed'
    assert projected['result_refs'] == ['task:original']
    assert original == before
