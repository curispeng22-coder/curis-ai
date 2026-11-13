from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import AutonomousControlError, AutonomousOperatingControl, RuntimeFoundation
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase1 import COMPANY, TENANT
from backend.tests.test_autonomous_operating_phase2 import (
    ControlledProvider,
    HEADERS,
    PREFIX,
    approved_plan,
    setup_runtime,
)


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-phase3a.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def evaluation_contract(version: str = "evaluation-v1") -> dict:
    return {
        "version": version,
        "status": "APPROVED",
        "body": {
            "observationWindow": {"kind": "CYCLE", "count": 1},
            "success": "accepted result and verified evidence",
            "failure": "result missed the approved objective",
            "insufficientEvidence": "required source is missing or inconclusive",
            "continueObservation": "one additional bounded window may be observed",
            "escalateWhen": "evidence conflicts or protected strategy must change",
        },
        "approvedBy": "CEO",
        "approvedAt": "2026-08-21T12:00:00+00:00",
    }


def close_real_cycle(path, client: TestClient):
    database, control, series, claimed, employee_ref = setup_runtime(path, client)
    cycle_id = claimed["cycle"]["entity_id"]
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        control.materialize_cycle_work(
            series_id=series["entity_id"], cycle_id=cycle_id,
            workflow_key="autonomous-phase2", plan=approved_plan(),
        )
    response = client.post(f"{PREFIX}/works/{cycle_id}/execute", headers=HEADERS)
    assert response.status_code == 200, response.text
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        control.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle_id)
        cycle = control.accept_and_close_cycle(
            series_id=series["entity_id"], cycle_id=cycle_id, reason="Phase 3A accepted input",
        )
    return database, control, series, cycle, employee_ref


def evaluate(control, series, cycle, *, outcome="SUCCESS", sufficiency="SUFFICIENT", facts=None):
    source = cycle["data"]["evidenceRefs"][0]
    return control.evaluate_closed_cycle(
        series_id=series["entity_id"], cycle_id=cycle["entity_id"],
        contract=evaluation_contract(), outcome=outcome,
        observed_facts=facts or [{"name": "accepted_result", "value": outcome == "SUCCESS", "sourceRef": source}],
        comparison={"expected": "accepted result", "observed": outcome},
        confidence="HIGH" if sufficiency == "SUFFICIENT" else "UNKNOWN",
        sufficiency=sufficiency,
    )


@pytest.mark.parametrize(
    ("outcome", "sufficiency"),
    [("SUCCESS", "SUFFICIENT"), ("FAILURE", "SUFFICIENT"), ("INSUFFICIENT", "INSUFFICIENT")],
)
def test_evaluation_is_evidence_bound_versioned_and_restart_safe(tmp_path, outcome, sufficiency):
    path = tmp_path / f"evaluation-{outcome.lower()}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            first = evaluate(control, series, cycle, outcome=outcome, sufficiency=sufficiency)
            restarted = AutonomousOperatingControl(Database(str(path)))
            current_cycle = RuntimeFoundation(restarted.db).get(cycle["entity_id"])
            replay = evaluate(restarted, restarted.get_series(series["entity_id"]), current_cycle,
                              outcome=outcome, sufficiency=sufficiency)
            assert replay == first
            assert first["contractPin"]["status"] == "APPROVED"
            assert first["resultRefs"] and first["evidenceRefs"] and first["acceptanceRef"]
            assert first["goalPin"] and first["strategyPin"] and first["envelopePin"]
            assert current_cycle["data"]["autonomousControl"]["successorCycleRef"] is None
            assert "acceptedLearning" not in current_cycle["data"]
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 0


@pytest.mark.parametrize(
    ("decision", "kwargs", "series_state"),
    [
        ("CONTINUE", {}, "ACTIVE"),
        ("ADJUST", {"adjustment": {"changes": {"tactic": "smaller-batch"}}}, "ACTIVE"),
        ("WAIT", {"wait_reason": "等待下一份真实回执", "next_check_at": "2026-08-22T12:00:00+00:00"}, "WAITING"),
    ],
)
def test_leader_decisions_apply_once_inside_authority(tmp_path, decision, kwargs, series_state):
    path = tmp_path / f"decision-{decision.lower()}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, employee_ref = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            evaluate(control, series, cycle)
            packet = control.review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision=decision, reason=f"Leader chose {decision}", **kwargs,
            )
            assert packet["lifecycle_status"] == "APPLIED"
            assert packet["data"]["decision"] == decision
            assert packet["data"]["actorRef"] == employee_ref
            assert packet["data"]["ceoGateRequired"] is False
            assert control.get_series(series["entity_id"])["lifecycle_status"] == series_state
            replay = AutonomousOperatingControl(Database(str(path))).review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision=decision, reason=f"Leader chose {decision}", **kwargs,
            )
            assert replay["entity_id"] == packet["entity_id"]
            with pytest.raises(AutonomousControlError, match="conflicting next-cycle Decision"):
                control.review_next_cycle(
                    series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                    decision="ESCALATE", reason="conflicting replay",
                )
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1


def test_out_of_envelope_adjust_becomes_ceo_escalation(tmp_path):
    path = tmp_path / "outside-envelope.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        _, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            evaluate(control, series, cycle)
            packet = control.review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision="ADJUST", reason="Goal must change",
                adjustment={"changes": {"goal": "new goal"}},
            )
            assert packet["lifecycle_status"] == "WAITING_CEO"
            assert packet["data"]["requestedDecision"] == "ADJUST"
            assert packet["data"]["decision"] == "ESCALATE"
            assert packet["data"]["ceoGateRequired"] is True
            assert control.get_series(series["entity_id"])["lifecycle_status"] == "WAITING"
            assert RuntimeFoundation(control.db).get(cycle["entity_id"])["data"]["autonomousControl"]["successorCycleRef"] is None


def test_explicit_escalation_waits_for_ceo(tmp_path):
    path = tmp_path / "escalate.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        _, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            evaluate(control, series, cycle, outcome="FAILURE")
            packet = control.review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision="ESCALATE", reason="经营证据冲突需要 CEO 判断",
            )
            assert packet["lifecycle_status"] == "WAITING_CEO"
            assert packet["data"]["decision"] == "ESCALATE"
            assert control.get_series(series["entity_id"])["lifecycle_status"] == "WAITING"


@pytest.mark.parametrize(("decision", "final_state"), [("PAUSE", "PAUSED"), ("STOP", "STOPPED")])
def test_pause_and_stop_require_real_ceo_authority(tmp_path, decision, final_state):
    path = tmp_path / f"terminal-{decision.lower()}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        _, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            evaluate(control, series, cycle, outcome="FAILURE")
            packet = control.review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision=decision, reason=f"Leader proposes {decision}",
            )
            assert packet["lifecycle_status"] == "WAITING_CEO"
            assert packet["data"]["ceoGateRequired"] is True
            assert control.get_series(series["entity_id"])["lifecycle_status"] == "WAITING"
            applied = AutonomousOperatingControl(Database(str(path))).apply_ceo_terminal_decision(
                packet["entity_id"], reason=f"CEO authorized {decision}",
            )
            assert applied["lifecycle_status"] == "APPLIED"
            assert control.get_series(series["entity_id"])["lifecycle_status"] == final_state
            assert RuntimeFoundation(control.db).get(cycle["entity_id"])["data"]["autonomousControl"]["successorCycleRef"] is None


def test_restart_between_review_and_decision_recovers_same_packet(tmp_path, monkeypatch):
    path = tmp_path / "review-restart.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            evaluate(control, series, cycle)
            monkeypatch.setattr(control, "_advance_next_cycle_decision", lambda _ref: (_ for _ in ()).throw(RuntimeError("restart")))
            with pytest.raises(RuntimeError, match="restart"):
                control.review_next_cycle(
                    series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                    decision="CONTINUE", reason="continue after restart",
                )
            with database.connect() as connection:
                assert connection.execute("select lifecycle_status from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == "DRAFT"
            restarted = AutonomousOperatingControl(Database(str(path)))
            packet = restarted.review_next_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                decision="CONTINUE", reason="continue after restart",
            )
            assert packet["lifecycle_status"] == "APPLIED"


def test_evaluation_and_decision_fail_closed_on_invalid_truth(tmp_path):
    path = tmp_path / "fail-closed.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, employee_ref = close_real_cycle(path, client)
        source = cycle["data"]["evidenceRefs"][0]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            invalid = evaluation_contract()
            del invalid["body"]["success"]
            with pytest.raises(AutonomousControlError, match="missing required"):
                control.evaluate_closed_cycle(
                    series_id=series["entity_id"], cycle_id=cycle["entity_id"], contract=invalid,
                    outcome="SUCCESS", observed_facts=[{"name": "x", "value": 1, "sourceRef": source}],
                    comparison={"x": 1}, confidence="HIGH", sufficiency="SUFFICIENT",
                )
            with pytest.raises(AutonomousControlError, match="conflicts"):
                evaluate(control, series, cycle, facts=[
                    {"name": "metric", "value": 1, "sourceRef": source},
                    {"name": "metric", "value": 2, "sourceRef": source},
                ])
            with database.connect() as connection:
                connection.execute(
                    "update runtime_entities set verification_status='UNVERIFIED' where tenant_id=? and entity_id=?",
                    (TENANT, source),
                )
            with pytest.raises(AutonomousControlError, match="missing, stale or unverified"):
                evaluate(control, series, cycle)
            with database.connect() as connection:
                connection.execute(
                    "update runtime_entities set verification_status='VERIFIED' where tenant_id=? and entity_id=?",
                    (TENANT, source),
                )
            evaluation = evaluate(control, series, cycle, outcome="INSUFFICIENT", sufficiency="INSUFFICIENT")
            assert evaluation["outcome"] == "INSUFFICIENT"
            with pytest.raises(AutonomousControlError, match="cannot continue or adjust"):
                control.review_next_cycle(
                    series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                    decision="CONTINUE", reason="not enough evidence",
                )
            with database.connect() as connection:
                connection.execute(
                    "update runtime_entities set lifecycle_status='PAUSED' where tenant_id=? and entity_id=?",
                    (TENANT, employee_ref),
                )
            with pytest.raises(AutonomousControlError, match="Leader is unavailable"):
                control.review_next_cycle(
                    series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                    decision="WAIT", reason="leader unavailable", wait_reason="wait",
                    next_check_at="2026-08-22T12:00:00+00:00",
                )
        with TenantContext.scope("tenant-other", company_id=COMPANY, role="test"):
            with pytest.raises(KeyError):
                AutonomousOperatingControl(database).get_series(series["entity_id"])


@pytest.mark.parametrize("pin", ["strategyPin", "envelopePin"])
def test_stale_strategy_or_envelope_pin_rejected(tmp_path, pin):
    path = tmp_path / f"stale-{pin}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with database.connect() as connection:
                row = connection.execute("select data_json from runtime_entities where entity_id=?", (cycle["entity_id"],)).fetchone()
                data = json.loads(row["data_json"])
                data["autonomousControl"][pin]["version"] = "stale"
                connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), cycle["entity_id"]))
            with pytest.raises(AutonomousControlError, match="pin is stale"):
                evaluate(control, series, RuntimeFoundation(database).get(cycle["entity_id"]))
