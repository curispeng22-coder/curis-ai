from __future__ import annotations

from contextlib import contextmanager

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation, SimulationRuntime
from app.tenant_context import TenantContext


TENANT_A = "tenant-runtime-api-a"
TENANT_B = "tenant-runtime-api-b"
COMPANY_A = "company-runtime-api-a"
COMPANY_A2 = "company-runtime-api-a2"
COMPANY_B = "company-runtime-api-b"
WORKSPACE_A = "workspace-runtime-api-a"
WORKSPACE_A2 = "workspace-runtime-api-a2"
WORKSPACE_B = "workspace-runtime-api-b"
HEADERS_A = {"X-Tenant-Id": TENANT_A}
HEADERS_B = {"X-Tenant-Id": TENANT_B}
CEO_HEADERS_A = {**HEADERS_A, "X-Ceo-Id": "ceo"}
CEO_HEADERS_B = {**HEADERS_B, "X-Ceo-Id": "ceo"}


@contextmanager
def client_for(path):
    with TestClient(create_app(str(path))) as client:
        yield client


def seed_runtime(path) -> tuple[str, str]:
    database = Database(str(path))
    with database.connect() as connection:
        for company_id, tenant_id in (
            (COMPANY_A, TENANT_A), (COMPANY_A2, TENANT_A), (COMPANY_B, TENANT_B),
        ):
            connection.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo', ?)",
                (company_id, tenant_id, company_id),
            )
        for workspace_id, tenant_id, company_id in (
            (WORKSPACE_A, TENANT_A, COMPANY_A),
            (WORKSPACE_A2, TENANT_A, COMPANY_A2),
            (WORKSPACE_B, TENANT_B, COMPANY_B),
        ):
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version) "
                "values (?, ?, ?, ?, ?, 'DRAFT', 'v1')",
                (workspace_id, tenant_id, company_id, f"business-{workspace_id}", workspace_id),
            )
    with TenantContext.scope(TENANT_A):
        foundation = RuntimeFoundation(database)
        assistant = foundation.create(
            "CEO_ASSISTANT", company_id=COMPANY_A, owner_ref="ceo",
            data={"prompt": "private prompt", "apiKey": "secret-value"},
        )
        employee = foundation.create("AI_EMPLOYEE", company_id=COMPANY_A, owner_ref=assistant["entity_id"])
        role = foundation.create("ROLE_SLOT", company_id=COMPANY_A)
        foundation.create(
            "CAPABILITY_BINDING", company_id=COMPANY_A, capability_ref="capability.runtime-api",
        )
        simulation = SimulationRuntime(database).create(
            company_id=COMPANY_A, ceo_id="ceo", scenario_id="RD-001", blueprint_version="v1",
            workspace_id=WORKSPACE_A, participants=[assistant["entity_id"], employee["entity_id"], role["entity_id"]],
        )
    return assistant["entity_id"], simulation["simulation_run_id"]


def test_snapshot_and_simulation_projection_are_scoped_and_redacted(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api.sqlite"
    with client_for(path) as client:
        _assistant_id, simulation_id = seed_runtime(path)
        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY_A}", headers=HEADERS_A,
        )
        assert snapshot.status_code == 200, snapshot.text
        assert snapshot.json()["assistant"]["entity_type"] == "CEO_ASSISTANT"
        assert snapshot.json()["workspaces"][0]["workspace_id"] == WORKSPACE_A
        assert "private prompt" not in snapshot.text
        assert "secret-value" not in snapshot.text

        listed = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY_A}/workspaces/{WORKSPACE_A}/simulations",
            headers=CEO_HEADERS_A,
        )
        assert listed.status_code == 200, listed.text
        assert listed.json()["simulations"][0]["simulation_run_id"] == simulation_id
        assert "participants" not in listed.json()["simulations"][0]


def test_workspace_simulation_can_start_once_and_audit_is_scoped(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api-simulation.sqlite"
    with client_for(path) as client:
        _assistant_id, simulation_id = seed_runtime(path)
        started = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{WORKSPACE_A}/simulations/{simulation_id}/transition",
            headers=CEO_HEADERS_A,
            json={"ceo_id": "ceo", "target": "RUNNING", "trigger": "ceo_start", "reason": "CEO 开始验证"},
        )
        assert started.status_code == 200, started.text
        assert started.json()["lifecycle_status"] == "RUNNING"
        assert started.json()["pass_status"] == "IN_PROGRESS"

        repeated = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{WORKSPACE_A}/simulations/{simulation_id}/transition",
            headers=CEO_HEADERS_A,
            json={"ceo_id": "ceo", "target": "RUNNING", "trigger": "repeat"},
        )
        cross_tenant = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{WORKSPACE_A}/simulations/{simulation_id}/transition",
            headers=CEO_HEADERS_B,
            json={"ceo_id": "ceo", "target": "RUNNING", "trigger": "cross_tenant"},
        )
        assert repeated.status_code == 409
        assert cross_tenant.status_code == 404

    with Database(str(path)).connect() as connection:
        audit = dict(connection.execute(
            "select actor, source, target, trigger, reason from runtime_transition_log "
            "where tenant_id = ? and entity_id = ? order by log_id desc limit 1",
            (TENANT_A, simulation_id),
        ).fetchone())
    assert audit == {
        "actor": "CEO", "source": "DRAFT", "target": "RUNNING",
        "trigger": "ceo_start", "reason": "CEO 开始验证",
    }


def test_workspace_simulation_execution_requires_explicit_binding(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api-execution.sqlite"
    with client_for(path) as client:
        _assistant_id, simulation_id = seed_runtime(path)
        started = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{WORKSPACE_A}/simulations/{simulation_id}/transition",
            headers=CEO_HEADERS_A,
            json={"ceo_id": "ceo", "target": "RUNNING", "trigger": "ceo_start"},
        )
        assert started.status_code == 200, started.text
        blocked = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{WORKSPACE_A}/simulations/{simulation_id}/execute",
            headers=CEO_HEADERS_A,
            json={"ceo_id": "ceo", "target": "RUNNING", "trigger": "ceo_execute"},
        )
        assert blocked.status_code == 409
        assert blocked.json() == {"detail": "execution_subject_required"}


def test_founding_run_survives_restart_and_transition_audit_is_complete(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api-restart.sqlite"
    with client_for(path) as client:
        created = client.post(
            "/api/workspace/runtime/foundation/founding-runs",
            headers=HEADERS_A,
            json={"owner_ref": "ceo", "intent_ref": "intent-safe-ref"},
        )
        assert created.status_code == 201, created.text
        run_id = created.json()["entity_id"]
        moved = client.post(
            f"/api/workspace/runtime/foundation/entities/{run_id}/transition",
            headers=HEADERS_A,
            json={
                "target": "INTENT_CAPTURED", "actor": "CEO", "trigger": "capture_intent",
                "reason": "CEO 明确提交", "evidenceRefs": [], "nextCheckAt": "2026-08-10T00:00:00+00:00",
            },
        )
        assert moved.status_code == 200, moved.text
        assert moved.json()["lifecycle_status"] == "INTENT_CAPTURED"

    with client_for(path) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/founding-runs/{run_id}", headers=HEADERS_A,
        )
        assert recovered.status_code == 200, recovered.text
        assert recovered.json()["lifecycle_status"] == "INTENT_CAPTURED"
    with Database(str(path)).connect() as connection:
        audit = dict(connection.execute(
            "select actor, trigger, reason, evidence_refs_json, next_check_at from runtime_transition_log "
            "where tenant_id = ? and entity_id = ?",
            (TENANT_A, run_id),
        ).fetchone())
    assert audit == {
        "actor": "CEO", "trigger": "capture_intent", "reason": "CEO 明确提交",
        "evidence_refs_json": "[]", "next_check_at": "2026-08-10T00:00:00+00:00",
    }


def test_tenant_company_and_workspace_scope_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api-isolation.sqlite"
    with client_for(path) as client:
        seed_runtime(path)
        cross_tenant = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY_A}", headers=HEADERS_B,
        )
        wrong_company = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY_A}/workspaces/{WORKSPACE_A2}/simulations",
            headers=HEADERS_A,
        )
        assert cross_tenant.status_code == 404
        assert wrong_company.status_code == 404
        assert cross_tenant.json() == {"detail": "运行对象不存在或无权访问"}
        assert "tenant-runtime-api-a" not in cross_tenant.text


def test_illegal_actor_state_and_waiting_ceo_auto_approval_are_rejected_safely(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "runtime-api-errors.sqlite"
    with client_for(path) as client:
        created = client.post(
            "/api/workspace/runtime/foundation/founding-runs", headers=HEADERS_A,
            json={"owner_ref": "ceo"},
        ).json()
        run_id = created["entity_id"]
        database = Database(str(path))
        with TenantContext.scope(TENANT_A):
            foundation = RuntimeFoundation(database)
            foundation.transition(run_id, "INTENT_CAPTURED", actor="CEO", trigger="capture")
            foundation.transition(run_id, "CLARIFYING", actor="CEO", trigger="clarify")
            foundation.transition(run_id, "PROPOSED", actor="CEO", trigger="propose")
            foundation.transition(run_id, "WAITING_CEO", actor="SYSTEM", trigger="wait")

        automatic = client.post(
            f"/api/workspace/runtime/foundation/entities/{run_id}/transition", headers=HEADERS_A,
            json={"target": "PROPOSED", "actor": "SYSTEM", "trigger": "auto_approve"},
        )
        illegal = client.post(
            f"/api/workspace/runtime/foundation/entities/{run_id}/transition", headers=HEADERS_A,
            json={"target": "CEO_CONFIRMED", "actor": "CEO", "trigger": "skip_resume"},
        )
        missing = client.post(
            "/api/workspace/runtime/foundation/entities/not-found/transition", headers=HEADERS_A,
            json={"target": "PROPOSED", "actor": "CEO", "trigger": "resume"},
        )
        assert automatic.status_code == 403
        assert automatic.json() == {"detail": "当前操作者无权执行该状态转换"}
        assert illegal.status_code == 409
        assert missing.status_code == 404
        combined = automatic.text + illegal.text + missing.text
        assert "Traceback" not in combined
        assert "sqlite" not in combined.lower()
        assert str(path) not in combined
