from __future__ import annotations

import json
import re

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import AutonomousControlError, AutonomousOperatingControl, RuntimeFoundation
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase1 import (
    BUSINESS,
    COMPANY,
    TENANT,
    approved_inputs,
    seed_scope,
)


WORKSPACE = "workspace-a"
CAPABILITY = "agent.autonomous.local"
PREFIX = "/api/workspace/runtime/foundation/team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo-phase1"}


class ControlledProvider:
    def __init__(self, *, malformed: bool = False, failure: Exception | None = None):
        self.calls: list[dict] = []
        self.malformed = malformed
        self.failure = failure

    def execute(self, prompt: str) -> dict:
        if self.failure:
            raise self.failure
        result_type = re.search(r"输出结果类型：([^\n]+)", prompt).group(1).strip()
        session = f"phase2-session-{len(self.calls) + 1}"
        self.calls.append({"prompt": prompt, "session": session})
        output = "invalid partial provider output" if self.malformed else json.dumps(
            {"status": "ACCEPTED", "resultType": result_type, "summary": "本轮工作已完成", "problem": ""},
            ensure_ascii=False,
        )
        return {
            "output": output,
            "status": "success",
            "session_id": session,
            "outbound_attempted": False,
            "total_tokens": 4,
            "estimated_cost": 0,
        }


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-phase2.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def approved_plan() -> dict:
    return {
        "version": "plan-v1",
        "status": "APPROVED",
        "body": {"work": "生成一个有真实来源的经营结果", "acceptance": "Result contract accepted"},
        "approvedBy": "CEO",
        "approvedAt": "2026-08-21T10:00:00+00:00",
    }


def setup_runtime(path, client: TestClient, *, capability_status: str = "active", binding_enabled: int = 1):
    database, assignment_ref = seed_scope(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        assignment = RuntimeFoundation(database).get(assignment_ref)
        employee_ref = assignment["data"]["employeeRef"]
        role_ref = assignment["data"]["roleRef"]
        with database.connect() as connection:
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                "values (?, ?, ?, '', 'et_tech_lead', '经营负责人', '负责人', 'idle')",
                (employee_ref, TENANT, COMPANY),
            )
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, "
                "capability_type, capability_id, enabled) values ('binding-phase2', ?, ?, 'tenant_private', 'agent', ?, ?)",
                (TENANT, employee_ref, CAPABILITY, binding_enabled),
            )
        database.save_tenant_private_capability(
            tenant_id=TENANT, capability_type="agent", capability_id=CAPABILITY,
            display_name="Controlled Phase 2 Provider", metadata={"kind": "controlled-provider"},
            status=capability_status,
        )
    published = client.post(
        f"{PREFIX}/definitions/publish",
        headers=HEADERS,
        json={
            "company_id": COMPANY,
            "scope_type": "WORKSPACE",
            "scope_ref": WORKSPACE,
            "workspace_id": WORKSPACE,
            "workflow_key": "autonomous-phase2",
            "roles": [{
                "responsibility_key": "workspace-leader",
                "role_name": "负责人",
                "employee_ref": employee_ref,
                "role_ref": role_ref,
                "assignment_ref": assignment_ref,
                "responsibility": "完成一个边界明确的经营工作",
                "input_contract": {"requiredRefs": ["work"]},
                "output_contract": {"requiresResult": True, "resultType": "phase2-result"},
                "is_leader": True,
            }],
            "default_flow": ["workspace-leader"],
        },
    )
    assert published.status_code == 200, published.text
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        strategy, envelope = approved_inputs()
        control = AutonomousOperatingControl(database)
        series = control.create_series(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            leader_assignment_ref=assignment_ref,
            strategy=strategy,
            envelope=envelope,
        )
        claimed = control.claim_trigger(
            series_id=series["entity_id"], source_type="MANUAL", source_key="phase2:manual:1",
        )
    return database, control, series, claimed, employee_ref


def test_trigger_runs_existing_team_operating_and_closes_one_cycle(tmp_path):
    path = tmp_path / "success.sqlite"
    provider = ControlledProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, control, series, claimed, employee_ref = setup_runtime(path, client)
        cycle_id = claimed["cycle"]["entity_id"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            running = control.materialize_cycle_work(
                series_id=series["entity_id"], cycle_id=cycle_id,
                workflow_key="autonomous-phase2", plan=approved_plan(),
            )
            assert running["lifecycle_status"] == "RUNNING"
            route = running["data"]["responsibilityRouting"]
            assert route["responsibilityHolderRef"] == employee_ref
            assert route["currentExecutorRef"] is None
            restarted_before_execution = AutonomousOperatingControl(Database(str(path)))
            assert RuntimeFoundation(restarted_before_execution.db).get(cycle_id)["lifecycle_status"] == "RUNNING"
        executed = client.post(f"{PREFIX}/works/{cycle_id}/execute", headers=HEADERS)
        assert executed.status_code == 200, executed.text
        route = executed.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "COMPLETED"
        assert route["currentExecutorRef"] is None
        record = next(iter(route["executions"].values()))
        assert record["provenance"]["verification_status"] == "VERIFIED"
        assert record["taskRef"] and record["sessionRef"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            waiting = control.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle_id)
            assert waiting["lifecycle_status"] == "WAITING_CEO"
            closed = control.accept_and_close_cycle(
                series_id=series["entity_id"], cycle_id=cycle_id, reason="本轮真实结果与证据已验收",
            )
            assert closed["lifecycle_status"] == "CLOSED"
            assert closed["data"]["autonomousControl"]["successorCycleRef"] is None
            assert control.get_series(series["entity_id"])["lifecycle_status"] == "ACTIVE"
            assert control.get_series(series["entity_id"])["data"]["currentCycleRef"] is None
            replay = control.claim_trigger(
                series_id=series["entity_id"], source_type="MANUAL", source_key="phase2:manual:1",
            )
            assert replay["replayed"] is True and replay["cycle"]["entity_id"] == cycle_id
            restarted = AutonomousOperatingControl(Database(str(path)))
            assert restarted.accept_and_close_cycle(
                series_id=series["entity_id"], cycle_id=cycle_id, reason="replay",
            )["lifecycle_status"] == "CLOSED"
            with database.connect() as connection:
                assert connection.execute("select count(*) from tasks").fetchone()[0] == 1
                assert connection.execute("select count(*) from artifacts").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='EVIDENCE'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 0
                assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        duplicate = client.post(f"{PREFIX}/works/{cycle_id}/execute", headers=HEADERS)
        assert duplicate.status_code == 200
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == 1
        assert len(provider.calls) == 1


@pytest.mark.parametrize(
    ("capability_status", "binding_enabled", "message"),
    [("disabled", 1, "capability is unavailable"), ("active", 0, "permission binding")],
)
def test_pre_execution_capability_and_permission_fail_closed(
    tmp_path, capability_status, binding_enabled, message,
):
    path = tmp_path / f"gate-{capability_status}-{binding_enabled}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, claimed, _ = setup_runtime(
            path, client, capability_status=capability_status, binding_enabled=binding_enabled,
        )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with pytest.raises(AutonomousControlError, match=message):
                control.materialize_cycle_work(
                    series_id=series["entity_id"], cycle_id=claimed["cycle"]["entity_id"],
                    workflow_key="autonomous-phase2", plan=approved_plan(),
                )
            cycle = RuntimeFoundation(database).get(claimed["cycle"]["entity_id"])
            assert cycle["lifecycle_status"] == "PLANNED"
            assert not cycle["data"].get("responsibilityRouting")
            with database.connect() as connection:
                assert connection.execute("select count(*) from tasks").fetchone()[0] == 0


def test_router_and_cross_tenant_fail_closed_before_execution(tmp_path):
    path = tmp_path / "router-scope.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, claimed, _ = setup_runtime(path, client)
        cycle_id = claimed["cycle"]["entity_id"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with pytest.raises(AutonomousControlError, match="No existing Team Operating workflow"):
                control.materialize_cycle_work(
                    series_id=series["entity_id"], cycle_id=cycle_id,
                    workflow_key="missing-workflow", plan=approved_plan(),
                )
        with TenantContext.scope("tenant-other", company_id=COMPANY, role="test"):
            with pytest.raises(KeyError):
                AutonomousOperatingControl(database).materialize_cycle_work(
                    series_id=series["entity_id"], cycle_id=cycle_id,
                    workflow_key="autonomous-phase2", plan=approved_plan(),
                )


def test_unavailable_employee_fails_closed_before_provider_task(tmp_path):
    path = tmp_path / "employee-unavailable.sqlite"
    provider = ControlledProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, control, series, claimed, employee_ref = setup_runtime(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with database.connect() as connection:
                connection.execute(
                    "update runtime_entities set lifecycle_status='PAUSED' where tenant_id=? and entity_id=?",
                    (TENANT, employee_ref),
                )
            with pytest.raises(AutonomousControlError, match="Employee is not available"):
                control.materialize_cycle_work(
                    series_id=series["entity_id"], cycle_id=claimed["cycle"]["entity_id"],
                    workflow_key="autonomous-phase2", plan=approved_plan(),
                )
            with database.connect() as connection:
                assert connection.execute("select count(*) from tasks").fetchone()[0] == 0
        assert provider.calls == []


@pytest.mark.parametrize(
    "provider",
    [ControlledProvider(malformed=True), ControlledProvider(failure=TimeoutError("provider timeout"))],
)
def test_provider_failure_or_partial_truth_fails_cycle_without_stopping_series(tmp_path, provider):
    path = tmp_path / f"failure-{id(provider)}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, control, series, claimed, _ = setup_runtime(path, client)
        cycle_id = claimed["cycle"]["entity_id"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            control.materialize_cycle_work(
                series_id=series["entity_id"], cycle_id=cycle_id,
                workflow_key="autonomous-phase2", plan=approved_plan(),
            )
        response = client.post(f"{PREFIX}/works/{cycle_id}/execute", headers=HEADERS)
        assert response.status_code == 200, response.text
        route = response.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "WAITING"
        assert route["currentExecutorRef"] is None
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            failed = control.fail_cycle(
                series_id=series["entity_id"], cycle_id=cycle_id, reason="Provider execution did not satisfy the Result contract",
            )
            assert failed["lifecycle_status"] == "FAILED"
            assert failed["data"]["autonomousControl"]["successorCycleRef"] is None
            assert control.get_series(series["entity_id"])["lifecycle_status"] == "ACTIVE"
            restarted = AutonomousOperatingControl(Database(str(path)))
            assert restarted.fail_cycle(
                series_id=series["entity_id"], cycle_id=cycle_id, reason="replay",
            )["lifecycle_status"] == "FAILED"
            with database.connect() as connection:
                counts = connection.execute(
                    "select count(*), count(distinct task_id) from tasks",
                ).fetchone()
                assert counts[0] == counts[1] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 0
