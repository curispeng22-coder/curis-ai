from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.runtime_foundation_router import build_runtime_foundation_router
from app.database import Database
from app.runtime import RuntimeFoundation
from app.runtime.workspace import RD_STAGES
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-operating-cycle"
COMPANY = "company-operating-cycle"
CEO = "ceo-operating-cycle"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


def studio_blueprint():
    return {
        "stages": list(RD_STAGES),
        "agentRefs": ["engineering-ai", "qa-ai"],
        "capabilityRefs": ["requirement:code-repository", "requirement:test-runner"],
        "connectorRefs": [],
        "platformConstraints": {},
        "replyPolicy": "CEO_REVIEW",
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
        "lifecycleMode": "STUDIO_DRAFT",
        "roleSlots": [
            {
                "role": "Engineering AI",
                "responsibility": "实现已批准的软件变更",
                "capabilityRefs": ["requirement:code-repository", "requirement:test-runner"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
            {
                "role": "QA AI",
                "responsibility": "验证结果与失败恢复路径",
                "capabilityRefs": ["requirement:test-runner"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
        ],
        "capabilityBindings": [
            {
                "capabilityRef": "requirement:code-repository",
                "capability": "代码仓库",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
            {
                "capabilityRef": "requirement:test-runner",
                "capability": "测试运行器",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
        ],
        "failurePolicy": {
            "manualFallback": "CEO Assistant 升级给 CEO 并转人工处理",
            "owner": "CEO Assistant",
        },
    }


def app_for(path, state):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Operating Company')",
            (COMPANY, TENANT, CEO),
        )
    with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
        RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)

    async def execute(request):
        state["calls"] = state.get("calls", 0) + 1
        state["request"] = request
        result = state.get("result", {"status": "succeeded", "output": "真实运行结果"})
        if isinstance(result, Exception):
            raise result
        return result

    app = FastAPI()

    @app.middleware("http")
    async def tenant_scope(request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-Id", TENANT)
        ceo_id = request.headers.get("X-Ceo-Id", CEO)
        with TenantContext.scope(tenant_id, ceo_id=ceo_id, role="test"):
            return await call_next(request)

    app.include_router(build_runtime_foundation_router(database, execute))
    return app, database


def prepare_operating_workspace(client: TestClient, database: Database, *, name="Operating RD"):
    seed_canonical_business(database, TENANT, COMPANY, f"business-{name.lower().replace(' ', '-')}")
    created = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "business_ref": f"business-{name.lower().replace(' ', '-')}",
            "business_type": "RD",
            "name": name,
            "blueprint_version": "v1",
            "blueprint": studio_blueprint(),
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
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start_staffing_simulation"},
    ).status_code == 200
    executed = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate_staffing_proposal"},
    ).json()
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
        headers=HEADERS,
        json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": executed["evidence_refs"]},
    ).status_code == 200
    for capability_id, display_name, permissions in (
        ("tenant.repo-reader", "repo-reader", ["repository.read"]),
        ("tenant.test-runner", "test-runner", ["sandbox.execute"]),
    ):
        database.save_tenant_private_capability(
            tenant_id=TENANT,
            capability_type="tool",
            capability_id=capability_id,
            display_name=display_name,
            metadata={"live_status": "available", "cost_per_unit": 0, "permissions": permissions},
        )
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/capability-supply-review",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "selections": [
                {
                    "requirement_ref": "requirement:code-repository",
                    "source": "tenant_private",
                    "capability_type": "tool",
                    "capability_id": "tenant.repo-reader",
                },
                {
                    "requirement_ref": "requirement:test-runner",
                    "source": "tenant_private",
                    "capability_type": "tool",
                    "capability_id": "tenant.test-runner",
                },
            ],
        },
    ).status_code == 200
    approved = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
        headers=HEADERS,
        json={"ceo_id": CEO, "choice": "APPROVE", "reason": "CEO 批准当前团队进入运行"},
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["workspaceStatus"] == "OPERATING"
    return workspace_id


def create_cycle(client: TestClient, workspace_id: str):
    response = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "owner_ref": "CEO Assistant",
            "outcome_ref": "完成可验收的 Curis 增量",
            "intent_ref": "完善 Curis",
            "blueprint_version": "v1",
            "execution_ref": "workflow_run:wfr-operating-real",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["entity_id"]


def start_and_execute(client: TestClient, workspace_id: str, cycle_id: str):
    started = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/start",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "CEO 启动当前 Operating Cycle"},
    )
    assert started.status_code == 200, started.text
    assert started.json()["lifecycle_status"] == "RUNNING"
    executed = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "CEO 请求已激活 AI 团队执行"},
    )
    assert executed.status_code == 200, executed.text
    return executed.json()


def test_operating_cycle_accepts_and_closes_with_durable_chain(tmp_path):
    path = tmp_path / "operating-close.sqlite"
    state = {}
    app, database = app_for(path, state)
    with TestClient(app) as client:
        workspace_id = prepare_operating_workspace(client, database)
        cycle_id = create_cycle(client, workspace_id)
        executed = start_and_execute(client, workspace_id, cycle_id)
        assert executed["lifecycle_status"] == "WAITING_CEO"
        assert executed["data"]["executionStatus"] == "COMPLETED_UNVERIFIED"
        evidence_refs = executed["data"]["evidenceRefs"]
        accepted = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/review",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "decision": "ACCEPT",
                "evidence_refs": evidence_refs,
                "reason": "CEO 已核对真实构建与测试证据",
            },
        )
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["lifecycle_status"] == "ACCEPTED"
        closed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/close",
            headers=HEADERS,
            json={"ceo_id": CEO, "choice": "CONTINUE", "reason": "复盘通过，进入下一轮完善"},
        )
        assert closed.status_code == 200, closed.text
        assert closed.json()["lifecycle_status"] == "CLOSED"
        decision_id = closed.json()["data"]["decisionPacketId"]
        repeated = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/close",
            headers=HEADERS,
            json={"ceo_id": CEO, "choice": "CONTINUE", "reason": "重复请求"},
        )
        assert repeated.status_code == 200
        assert repeated.json()["data"]["decisionPacketId"] == decision_id

        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert next(item for item in detail["cycles"] if item["entity_id"] == cycle_id)["lifecycle_status"] == "CLOSED"
        assert {item["lifecycle_status"] for item in detail["acceptances"]} == {"CLOSED"}
        assert {item["lifecycle_status"] for item in detail["decisions"]} == {"APPLIED"}
        assert all(item["verification_status"] == "VERIFIED" for item in detail["evidence"] if item["parent_id"] == cycle_id)
        assert all(item["lifecycle_status"] == "AVAILABLE" for item in detail["employees"])
        assert all(item["lifecycle_status"] == "OPERATING" for item in detail["role_slots"])
        assert all(item["lifecycle_status"] == "ACTIVE" for item in detail["capability_bindings"])
        assert state["request"]["cycle_id"] == cycle_id

    with TestClient(app) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        )
        assert recovered.status_code == 200
        assert recovered.json()["cycles"][0]["lifecycle_status"] == "CLOSED"


def test_operating_cycle_rejects_without_verifying_evidence(tmp_path):
    path = tmp_path / "operating-reject.sqlite"
    state = {}
    app, database = app_for(path, state)
    with TestClient(app) as client:
        workspace_id = prepare_operating_workspace(client, database)
        cycle_id = create_cycle(client, workspace_id)
        executed = start_and_execute(client, workspace_id, cycle_id)
        rejected = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/review",
            headers=HEADERS,
            json={"ceo_id": CEO, "decision": "REJECT", "evidence_refs": [], "reason": "结果未满足验收标准"},
        )
        assert rejected.status_code == 200, rejected.text
        assert rejected.json()["lifecycle_status"] == "REJECTED"
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert {item["lifecycle_status"] for item in detail["acceptances"]} == {"REJECTED"}
        assert any(item["lifecycle_status"] == "REJECTED" for item in detail["handoffs"])
        evidence = next(item for item in detail["evidence"] if item["entity_id"] in executed["data"]["evidenceRefs"])
        assert evidence["verification_status"] == "UNVERIFIED"
        assert all(item["lifecycle_status"] == "AVAILABLE" for item in detail["employees"])


def test_operating_cycle_failure_pauses_and_resumes_without_success_evidence(tmp_path):
    path = tmp_path / "operating-recovery.sqlite"
    state = {"result": {"status": "failed", "error": "worker unavailable"}}
    app, database = app_for(path, state)
    with TestClient(app) as client:
        workspace_id = prepare_operating_workspace(client, database)
        cycle_id = create_cycle(client, workspace_id)
        failed = start_and_execute(client, workspace_id, cycle_id)
        assert failed["lifecycle_status"] == "PAUSED"
        assert failed["exception_status"] == "FAILED"
        assert failed["data"]["executionStatus"] == "FAILED"
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert not [item for item in detail["evidence"] if item["parent_id"] == cycle_id]
        assert all(item["lifecycle_status"] == "DEGRADED" and item["presence_state"] == "BLOCKED" for item in detail["employees"])

        resumed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/resume",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "执行器恢复，CEO 允许重试"},
        )
        assert resumed.status_code == 200, resumed.text
        assert resumed.json()["lifecycle_status"] == "RUNNING"
        state["result"] = {"status": "succeeded", "output": "恢复后的真实结果"}
        retried = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重试执行"},
        )
        assert retried.status_code == 200, retried.text
        assert retried.json()["lifecycle_status"] == "WAITING_CEO"
        assert retried.json()["data"]["failureEvents"][0]["resolvedAt"]


def test_operating_cycle_review_is_atomic_and_scope_fail_closed(tmp_path):
    path = tmp_path / "operating-atomic.sqlite"
    state = {}
    app, database = app_for(path, state)
    with TestClient(app) as client:
        workspace_id = prepare_operating_workspace(client, database)
        cycle_id = create_cycle(client, workspace_id)
        executed = start_and_execute(client, workspace_id, cycle_id)
        with database.connect() as connection:
            connection.execute(
                "create trigger fail_operating_accept before update of lifecycle_status on runtime_entities "
                "when old.entity_type = 'ACCEPTANCE' and new.lifecycle_status = 'ACCEPTED' "
                "begin select raise(abort, 'forced acceptance failure'); end"
            )
        failed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/review",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "decision": "ACCEPT",
                "evidence_refs": executed["data"]["evidenceRefs"],
                "reason": "强制失败验证",
            },
        )
        assert failed.status_code == 500
        with database.connect() as connection:
            connection.execute("drop trigger fail_operating_accept")
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert detail["cycles"][0]["lifecycle_status"] == "WAITING_CEO"
        assert {item["lifecycle_status"] for item in detail["acceptances"]} == {"PENDING"}
        assert all(item["verification_status"] == "UNVERIFIED" for item in detail["evidence"] if item["parent_id"] == cycle_id)
        assert all(item["lifecycle_status"] == "OPERATING" for item in detail["employees"])

        cross_tenant = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/review",
            headers={"X-Tenant-Id": "another-tenant", "X-Ceo-Id": CEO},
            json={"ceo_id": CEO, "decision": "REJECT", "evidence_refs": [], "reason": "forged"},
        )
        assert cross_tenant.status_code == 404
