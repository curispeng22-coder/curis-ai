from __future__ import annotations

import asyncio

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.runtime_foundation_router import build_runtime_foundation_router
from app.database import Database
from app.runtime import RuntimeFoundation
from app.runtime.workspace import RD_STAGES, WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-rd-real-slice"
COMPANY = "company-rd-real-slice"
CEO = "ceo-rd-real-slice"
PROJECT = "project-rd-real-slice"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


def blueprint():
    return {
        "stages": list(RD_STAGES),
        "agentRefs": ["engineering-ai"],
        "capabilityRefs": ["requirement:codex-runtime"],
        "connectorRefs": [],
        "platformConstraints": {},
        "replyPolicy": "CEO_REVIEW",
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
        "lifecycleMode": "STUDIO_DRAFT",
        "roleSlots": [{
            "role": "Engineering AI",
            "responsibility": "执行受控软件变更",
            "capabilityRefs": ["requirement:codex-runtime"],
            "staffingStatus": "PLANNED_NOT_MATERIALIZED",
        }],
        "capabilityBindings": [{
            "capabilityRef": "requirement:codex-runtime",
            "capability": "Codex Runtime",
            "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
        }],
        "failurePolicy": {"manualFallback": "保留失败事实", "owner": "CEO Assistant"},
    }


def make_app(path, state):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'RD Company')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into projects(project_id, tenant_id, company_id, name, goal, status) "
            "values (?, ?, ?, 'RD Project', '验证真实研发执行', 'active')",
            (PROJECT, TENANT, COMPANY),
        )
    seed_canonical_business(database, TENANT, COMPANY, "business-rd-real-slice")
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="agent",
        capability_id="agent.codex.rd",
        display_name="Codex Runtime",
        metadata={
            "kind": "codex-cli",
            "cwd": "/tmp",
            "computer_access_intent": "AUTO_WITHIN_BOUNDARY",
            "live_status": "available",
            "permissions": ["workspace.write"],
            "cost_per_unit": 0,
        },
    )
    with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
        RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)

    async def execute(request):
        state["calls"] = state.get("calls", 0) + 1
        state["request"] = request
        if state.get("delay"):
            await asyncio.sleep(state["delay"])
        return state["result"]

    app = FastAPI()

    @app.middleware("http")
    async def tenant_scope(request: Request, call_next):
        with TenantContext.scope(
            request.headers.get("X-Tenant-Id", TENANT),
            ceo_id=request.headers.get("X-Ceo-Id", CEO),
            role="test",
        ):
            return await call_next(request)

    app.include_router(build_runtime_foundation_router(database, execute))
    return app, database


def operating_workspace(client, database):
    created = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "business_ref": "business-rd-real-slice",
            "business_type": "RD",
            "name": "RD Real Slice",
            "blueprint_version": "v1",
            "blueprint": blueprint(),
        },
    )
    assert created.status_code == 201, created.text
    workspace_id = created.json()["workspace"]["workspace_id"]
    simulation = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
        headers=HEADERS,
        json={"ceo_id": CEO, "scenario_id": "ORG-001", "blueprint_version": "v1"},
    ).json()
    simulation_id = simulation["simulation_run_id"]
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/transition",
        headers=HEADERS,
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start"},
    ).status_code == 200
    executed = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate"},
    ).json()
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
        headers=HEADERS,
        json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": executed["evidence_refs"]},
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/capability-supply-review",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "selections": [{
                "requirement_ref": "requirement:codex-runtime",
                "source": "tenant_private",
                "capability_type": "agent",
                "capability_id": "agent.codex.rd",
            }],
        },
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
        headers=HEADERS,
        json={"ceo_id": CEO, "choice": "APPROVE", "reason": "批准单员工首轮执行"},
    ).status_code == 200
    return workspace_id


def cycle(client, workspace_id):
    response = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "owner_ref": "CEO Assistant",
            "outcome_ref": "函数与测试同时通过",
            "intent_ref": "修复受控函数",
            "blueprint_version": "v1",
            "project_ref": PROJECT,
            "work_item_title": "修复金额函数",
            "instruction": "修改 src/calc.py 并补充测试",
            "resource_refs": ["src/calc.py", "tests/test_calc.py"],
            "test_command": ["python3", "-m", "pytest", "-q"],
            "requested_access_intent": "AUTO_WITHIN_BOUNDARY",
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["execution_ref"] == "rd_task:auto"
    return response.json()["entity_id"]


def start_and_execute(client, workspace_id, cycle_id):
    started = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/start",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "开始真实研发 Task"},
    )
    assert started.status_code == 200, started.text
    assert started.json()["data"]["workContext"]["currentExecutorRef"] is None
    return client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "调用 Codex"},
    )


def test_rd_real_execution_result_chain_and_restart(tmp_path):
    state = {"result": {
        "status": "succeeded",
        "output": "真实执行摘要",
        "task_ref": "task-real-1",
        "session_ref": "session-real-1",
        "artifact_refs": ["artifact-real-1"],
        "changed_files": ["src/calc.py", "tests/test_calc.py"],
        "test_result": {"command": ["python3", "-m", "pytest", "-q"], "exitCode": 0},
        "computer_access": {
            "requested_intent": "AUTO_WITHIN_BOUNDARY",
            "configured_state": "CONFIGURED",
            "effective_state": "UNKNOWN",
            "verification_state": "UNVERIFIED",
        },
        "execution_binding": {"executionEmployeeRef": "employee-execution-1"},
        "conversation_summary": "代码修改已经完成，声明测试通过。",
    }}
    app, database = make_app(tmp_path / "rd-real.sqlite", state)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client, database)
        cycle_id = cycle(client, workspace_id)
        response = start_and_execute(client, workspace_id, cycle_id)
        assert response.status_code == 202, response.text
        accepted = response.json()
        assert accepted["lifecycle_status"] == "RUNNING"
        assert accepted["data"]["executionStatus"] == "RUNNING"
        assert accepted["data"]["workContext"]["currentExecutorRef"]
        assert accepted["data"]["conversation"]["summary"].startswith("研发员工已接手")
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        result = next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)
        assert result["data"]["executionStatus"] == "COMPLETED"
        assert result["data"]["workContext"]["currentExecutorRef"] is None
        assert result["data"]["taskRef"] == "task-real-1"
        assert result["data"]["resultRefs"] == ["artifact-real-1", result["data"]["evidenceRefs"][-1]]
        assert result["data"]["computerAccess"]["effective_state"] == "UNKNOWN"
        assert detail["employees"][0]["lifecycle_status"] == "AVAILABLE"
        assert detail["employees"][0]["presence_state"] == "IDLE"
        assert not detail["handoffs"] and not detail["acceptances"] and not detail["decisions"]
        assert detail["evidence"][-1]["verification_status"] == "VERIFIED"
        assert state["request"]["subject"]["data"]["workContext"]["currentExecutorRef"]

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        recovered = next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)
        assert recovered["data"]["taskRef"] == "task-real-1"
        assert recovered["data"]["workContext"]["currentExecutorRef"] is None
        assert recovered["data"]["computerAccess"]["effective_state"] == "UNKNOWN"


def test_rd_real_execution_failure_keeps_artifact_and_never_completes(tmp_path):
    state = {"result": {
        "status": "failed",
        "error": "rd_test_failed",
        "task_ref": "task-failed-1",
        "session_ref": "session-failed-1",
        "artifact_refs": ["artifact-failed-1"],
        "changed_files": ["src/calc.py"],
        "test_result": {"command": ["python3", "-m", "pytest", "-q"], "exitCode": 1},
        "computer_access": {
            "requested_intent": "AUTO_WITHIN_BOUNDARY",
            "configured_state": "CONFIGURED",
            "effective_state": "UNKNOWN",
            "verification_state": "UNVERIFIED",
        },
    }}
    app, database = make_app(tmp_path / "rd-failed.sqlite", state)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client, database)
        cycle_id = cycle(client, workspace_id)
        response = start_and_execute(client, workspace_id, cycle_id)
        assert response.status_code == 202, response.text
        assert response.json()["data"]["executionStatus"] == "RUNNING"
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        failed = next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)
        assert failed["lifecycle_status"] == "PAUSED"
        assert failed["data"]["executionStatus"] == "FAILED"
        assert failed["data"]["artifactRefs"] == ["artifact-failed-1"]
        assert failed["data"]["testResult"]["exitCode"] == 1
        assert failed["data"]["workContext"]["currentExecutorRef"] is None
        assert failed["data"]["workContext"]["responsibilityEmployeeRef"]
        assert detail["employees"][0]["lifecycle_status"] == "DEGRADED"
        assert detail["evidence"][-1]["verification_status"] == "VERIFIED"
        assert not detail["handoffs"] and not detail["acceptances"] and not detail["decisions"]


def test_rd_active_execution_is_idempotent_and_restart_fails_closed(tmp_path):
    state = {"result": {"status": "succeeded"}}
    app, database = make_app(tmp_path / "rd-interrupted.sqlite", state)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client, database)
        cycle_id = cycle(client, workspace_id)
        started = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/start",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "开始真实研发 Task"},
        )
        assert started.status_code == 200
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            WorkspaceRuntime(database).begin_operating_cycle_execution(
                company_id=COMPANY, workspace_id=workspace_id, cycle_id=cycle_id,
            )
        duplicate = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重复提交"},
        )
        assert duplicate.status_code == 202
        assert duplicate.json()["data"]["executionStatus"] == "RUNNING"
        assert state.get("calls", 0) == 0

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        interrupted = next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)
        assert interrupted["lifecycle_status"] == "PAUSED"
        assert interrupted["data"]["executionStatus"] == "FAILED"
        assert interrupted["data"]["workContext"]["currentExecutorRef"] is None
        assert interrupted["data"]["failureEvents"][-1]["code"] == "execution_interrupted_unverified"
        interruption_evidence = next(
            item for item in detail["evidence"] if item["parent_id"] == cycle_id
        )
        assert interruption_evidence["verification_status"] == "UNVERIFIED"
