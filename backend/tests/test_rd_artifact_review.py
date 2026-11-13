from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.runtime_foundation_router import build_runtime_foundation_router
from app.database import Database
from app.runtime import RuntimeFoundation
from app.runtime.workspace import RD_STAGES, WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-rd-artifact-review"
COMPANY = "company-rd-artifact-review"
CEO = "ceo-rd-artifact-review"
PROJECT = "project-rd-artifact-review"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}
ACTIVE_DB = (Path(__file__).resolve().parents[2] / "data" / "curis.sqlite").resolve()


def isolated_database(path: Path, monkeypatch) -> Database:
    resolved = path.resolve()
    if resolved == ACTIVE_DB:
        raise RuntimeError("artifact review tests refuse the active Curis database")
    for name in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"):
        monkeypatch.setenv(name, str(resolved))
    assert len({os.environ[name] for name in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB")}) == 1
    database = Database(str(resolved))
    database.initialize()
    return database


def blueprint():
    return {
        "stages": list(RD_STAGES),
        "agentRefs": ["engineering-ai", "review-ai"],
        "capabilityRefs": ["requirement:codex-runtime", "requirement:review-checklist"],
        "connectorRefs": [],
        "platformConstraints": {},
        "replyPolicy": "CEO_REVIEW",
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
        "lifecycleMode": "STUDIO_DRAFT",
        "roleSlots": [
            {
                "role": "Engineering AI",
                "responsibility": "执行受控软件变更",
                "capabilityRefs": ["requirement:codex-runtime"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
            {
                "role": "Review AI",
                "responsibility": "检查代码 Artifact 与验证证据",
                "capabilityRefs": ["requirement:review-checklist"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
        ],
        "capabilityBindings": [
            {
                "capabilityRef": "requirement:codex-runtime",
                "capability": "Codex Runtime",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
            {
                "capabilityRef": "requirement:review-checklist",
                "capability": "Review Checklist",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
        ],
        "failurePolicy": {"manualFallback": "保留失败事实", "owner": "CEO Assistant"},
    }


def make_app(path: Path, state: dict, monkeypatch):
    database = isolated_database(path, monkeypatch)
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'RD Company')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into projects(project_id, tenant_id, company_id, name, goal, status) "
            "values (?, ?, ?, 'RD Project', '验证双员工代码审核', 'active')",
            (PROJECT, TENANT, COMPANY),
        )
    seed_canonical_business(database, TENANT, COMPANY, "business-rd-artifact-review")
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="agent",
        capability_id="agent.codex.rd",
        display_name="Codex Runtime",
        metadata={
            "kind": "codex-cli",
            "cwd": str(path.parent),
            "computer_access_intent": "AUTO_WITHIN_BOUNDARY",
            "live_status": "available",
            "permissions": ["workspace.write"],
            "cost_per_unit": 0,
        },
    )
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="tool",
        capability_id="tool.review.checklist",
        display_name="Review Checklist",
        metadata={"live_status": "available", "permissions": ["artifact.read"], "cost_per_unit": 0},
    )
    with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
        RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)

    async def execute(request):
        if (request.get("subject") or {}).get("data", {}).get("artifactReviewExecution"):
            state["review_calls"] = state.get("review_calls", 0) + 1
            state["review_request"] = request
            if state.get("review_results"):
                return state["review_results"][state["review_calls"] - 1]
            return state["review_result"]
        state["primary_calls"] = state.get("primary_calls", 0) + 1
        if state.get("primary_results"):
            return state["primary_results"][state["primary_calls"] - 1]
        return {
            "status": "succeeded",
            "output": "真实主执行摘要",
            "task_ref": "task-primary",
            "session_ref": "session-primary",
            "artifact_refs": ["artifact-primary"],
            "changed_files": ["src/calc.py"],
            "test_result": {"command": ["python3", "-m", "pytest", "-q"], "exitCode": 0},
            "computer_access": {
                "requested_intent": "AUTO_WITHIN_BOUNDARY",
                "configured_state": "CONFIGURED",
                "effective_state": "UNKNOWN",
                "verification_state": "UNVERIFIED",
            },
            "execution_binding": {"executionEmployeeRef": "execution-primary"},
        }

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


def operating_workspace(client):
    created = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "business_ref": "business-rd-artifact-review",
            "business_type": "RD",
            "name": "RD Artifact Review",
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
            "selections": [
                {
                    "requirement_ref": "requirement:codex-runtime",
                    "source": "tenant_private",
                    "capability_type": "agent",
                    "capability_id": "agent.codex.rd",
                },
                {
                    "requirement_ref": "requirement:review-checklist",
                    "source": "tenant_private",
                    "capability_type": "tool",
                    "capability_id": "tool.review.checklist",
                },
            ],
        },
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
        headers=HEADERS,
        json={"ceo_id": CEO, "choice": "APPROVE", "reason": "批准研发与审核员工"},
    ).status_code == 200
    return workspace_id


def completed_cycle(client, workspace_id):
    created = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "owner_ref": "CEO Assistant",
            "outcome_ref": "代码与测试可审核",
            "intent_ref": "完成受控函数修改",
            "blueprint_version": "v1",
            "project_ref": PROJECT,
            "work_item_title": "修复金额函数",
            "instruction": "修改 src/calc.py",
            "resource_refs": ["src/calc.py"],
            "test_command": ["python3", "-m", "pytest", "-q"],
            "requested_access_intent": "AUTO_WITHIN_BOUNDARY",
        },
    )
    assert created.status_code == 201, created.text
    cycle_id = created.json()["entity_id"]
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/start",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "分配研发责任"},
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "执行受控修改"},
    ).status_code == 202
    detail = client.get(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
        headers=HEADERS,
    ).json()
    cycle = next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)
    assert cycle["data"]["executionStatus"] == "COMPLETED"
    reviewer = next(item for item in detail["employees"] if item["data"]["name"] == "Review AI")
    return cycle, reviewer


def create_and_execute_review(client, workspace_id, cycle, reviewer):
    created = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/artifact-review",
        headers=HEADERS,
        json={"ceo_id": CEO, "reviewer_employee_ref": reviewer["entity_id"]},
    )
    assert created.status_code == 201, created.text
    return client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/artifact-review/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "审核代码 Artifact"},
    )


@pytest.mark.parametrize("outcome", ["APPROVED", "CHANGES_REQUESTED"])
def test_artifact_review_keeps_holder_and_persists_real_result(tmp_path, monkeypatch, outcome):
    state = {"review_result": {
        "status": "succeeded",
        "review_outcome": outcome,
        "output": f"REVIEW_OUTCOME: {outcome}\n审核依据已记录。",
        "task_ref": f"task-review-{outcome.lower()}",
        "session_ref": f"session-review-{outcome.lower()}",
        "artifact_refs": [f"artifact-review-{outcome.lower()}"],
        "computer_access": {
            "requested_intent": "AUTO_WITHIN_BOUNDARY",
            "configured_state": "CONFIGURED",
            "effective_state": "UNKNOWN",
            "verification_state": "UNVERIFIED",
        },
    }}
    app, _ = make_app(tmp_path / f"rd-review-{outcome.lower()}.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, reviewer = completed_cycle(client, workspace_id)
        holder_ref = cycle["data"]["workContext"]["responsibilityEmployeeRef"]
        response = create_and_execute_review(client, workspace_id, cycle, reviewer)
        assert response.status_code == 202, response.text
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        reviewed = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
        review = reviewed["data"]["artifactReview"]
        assert review["status"] == outcome
        assert review["originalHolderRef"] == holder_ref
        assert reviewed["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert reviewed["data"]["workContext"]["currentExecutorRef"] is None
        assert review["currentExecutorRef"] is None
        assert review["reviewTaskRef"].startswith("task-review-")
        assert review["resultRefs"][-1].startswith("evidence-")
        assert state["review_request"]["subject"]["data"]["artifactReviewExecution"]["currentExecutorRef"] == reviewer["entity_id"]
        assert not detail["handoffs"] and not detail["decisions"]
        review_evidence = next(item for item in detail["evidence"] if item["data"].get("requestRef") == review["requestRef"])
        assert review_evidence["verification_status"] == "VERIFIED"

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        review = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])["data"]["artifactReview"]
        assert review["status"] == outcome
        assert review["currentExecutorRef"] is None
        assert not detail["handoffs"] and not detail["decisions"]


def test_artifact_review_failure_is_durable_without_transfer(tmp_path, monkeypatch):
    state = {"review_result": {
        "status": "failed",
        "error": "review_execution_failed",
        "output": "审核执行失败",
        "task_ref": "task-review-failed",
        "session_ref": "session-review-failed",
        "artifact_refs": ["artifact-review-failed"],
    }}
    app, _ = make_app(tmp_path / "rd-review-failed.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, reviewer = completed_cycle(client, workspace_id)
        holder_ref = cycle["data"]["workContext"]["responsibilityEmployeeRef"]
        assert create_and_execute_review(client, workspace_id, cycle, reviewer).status_code == 202
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        reviewed = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
        assert reviewed["data"]["executionStatus"] == "COMPLETED"
        assert reviewed["data"]["artifactReview"]["status"] == "FAILED"
        assert reviewed["data"]["artifactReview"]["currentExecutorRef"] is None
        assert reviewed["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert not detail["handoffs"] and not detail["decisions"]


def test_artifact_review_idempotency_and_restart_fail_closed(tmp_path, monkeypatch):
    state = {"review_result": {"status": "succeeded"}}
    app, database = make_app(tmp_path / "rd-review-interrupted.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, reviewer = completed_cycle(client, workspace_id)
        path = f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/artifact-review"
        payload = {"ceo_id": CEO, "reviewer_employee_ref": reviewer["entity_id"]}
        first = client.post(path, headers=HEADERS, json=payload)
        second = client.post(path, headers=HEADERS, json=payload)
        assert first.status_code == second.status_code == 201
        assert first.json()["data"]["artifactReview"]["requestRef"] == second.json()["data"]["artifactReview"]["requestRef"]
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            WorkspaceRuntime(database).begin_artifact_review_execution(
                company_id=COMPANY, workspace_id=workspace_id, cycle_id=cycle["entity_id"],
            )
        duplicate = client.post(
            f"{path}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重复提交"},
        )
        assert duplicate.status_code == 202
        assert duplicate.json()["data"]["artifactReview"]["status"] == "REVIEWING"
        assert state.get("review_calls", 0) == 0

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        review = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])["data"]["artifactReview"]
        assert review["status"] == "FAILED"
        assert review["currentExecutorRef"] is None
        assert review["failure"]["code"] == "review_interrupted_unverified"
        assert not detail["handoffs"] and not detail["decisions"]


def test_active_database_guard_fails_fast(monkeypatch):
    with pytest.raises(RuntimeError, match="active Curis database"):
        isolated_database(ACTIVE_DB, monkeypatch)
