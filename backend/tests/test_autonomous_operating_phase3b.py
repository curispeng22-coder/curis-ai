from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import AutonomousControlError, AutonomousOperatingControl, RuntimeFoundation
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase1 import COMPANY, TENANT
from backend.tests.test_autonomous_operating_phase2 import ControlledProvider
from backend.tests.test_autonomous_operating_phase3a import close_real_cycle, evaluate


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-phase3b.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def prepare_decision(path, client, decision="CONTINUE", **kwargs):
    database, control, series, cycle, _ = close_real_cycle(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
        evaluate(control, series, cycle, outcome="FAILURE" if decision in {"ESCALATE", "PAUSE", "STOP"} else "SUCCESS")
        packet = control.review_next_cycle(
            series_id=series["entity_id"], cycle_id=cycle["entity_id"],
            decision=decision, reason=f"Phase 3B {decision}", **kwargs,
        )
        if decision in {"PAUSE", "STOP"}:
            packet = control.apply_ceo_terminal_decision(packet["entity_id"], reason=f"CEO authorized {decision}")
    return database, control, series, cycle, packet


def assert_no_learning(cycle):
    assert "acceptedLearning" not in cycle["data"]
    assert "learning" not in cycle["data"]


def test_continue_creates_exactly_one_existing_successor_with_lineage(tmp_path):
    path = tmp_path / "continue.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, predecessor, packet = prepare_decision(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            before = RuntimeFoundation(database).get(predecessor["entity_id"])
            result = control.authorize_successor(packet["entity_id"])
            successor = result["cycle"]
            assert result["created"] is True
            assert successor["entity_type"] == "CYCLE"
            assert successor["lifecycle_status"] == "PLANNED"
            assert successor["data"]["executionStatus"] == "NOT_STARTED"
            successor_control = successor["data"]["autonomousControl"]
            assert successor_control["predecessorCycleRef"] == predecessor["entity_id"]
            assert successor_control["predecessorDecisionRef"] == packet["entity_id"]
            assert successor_control["successorCycleRef"] is None
            after = RuntimeFoundation(database).get(predecessor["entity_id"])
            assert after["data"]["autonomousControl"]["successorCycleRef"] == successor["entity_id"]
            for key in ("workspaceGoalPin", "businessGoalPin", "strategyPin", "envelopePin", "planPin", "evaluationPin"):
                assert after["data"]["autonomousControl"][key] == before["data"]["autonomousControl"][key]
            assert after["data"]["autonomousEvaluation"] == before["data"]["autonomousEvaluation"]
            assert after["data"]["autonomousLeaderReview"] == before["data"]["autonomousLeaderReview"]
            current_series = control.get_series(series["entity_id"])
            assert current_series["lifecycle_status"] == "ACTIVE"
            assert current_series["data"]["lastCycleRef"] == predecessor["entity_id"]
            assert current_series["data"]["currentCycleRef"] == successor["entity_id"]
            updated_packet = RuntimeFoundation(database).get(packet["entity_id"])
            assert updated_packet["data"]["successorCycleRef"] == successor["entity_id"]
            assert updated_packet["data"]["successorTriggerClaimRef"] == result["claim"]["entity_id"]
            assert result["claim"]["data"]["decisionRef"] == packet["entity_id"]
            merged = control.claim_trigger(
                series_id=series["entity_id"], source_type="SCHEDULED", source_key="during-successor",
            )
            assert merged["merged"] is True
            assert merged["cycle"]["entity_id"] == successor["entity_id"]
            assert_no_learning(after)
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 2
                assert connection.execute("select count(*) from tasks").fetchone()[0] == 1
                assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_bounded_adjust_creates_successor_with_adjusted_immutable_pins(tmp_path):
    path = tmp_path / "adjust.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, predecessor, packet = prepare_decision(
            path, client, "ADJUST", adjustment={"changes": {"tactic": "smaller-batch"}},
        )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            old_pin = predecessor["data"]["autonomousControl"]["strategyPin"]
            result = control.authorize_successor(packet["entity_id"])
            new_control = result["cycle"]["data"]["autonomousControl"]
            assert new_control["strategyPin"]["strategyRef"] != old_pin["strategyRef"]
            assert new_control["strategyPin"]["version"].startswith(f"{old_pin['version']}.adjust.")
            assert new_control["envelopePin"] == predecessor["data"]["autonomousControl"]["envelopePin"]
            assert new_control["planPin"]["status"] == "UNRESOLVED"
            assert new_control["planPin"]["requiredChanges"] == {"tactic": "smaller-batch"}
            reread_predecessor = RuntimeFoundation(database).get(predecessor["entity_id"])
            assert reread_predecessor["data"]["autonomousControl"]["strategyPin"] == old_pin
            strategies = control.get_series(series["entity_id"])["data"]["strategyVersions"]
            assert len(strategies) == 2
            assert strategies[-1]["body"]["tactic"] == "smaller-batch"
            assert strategies[-1]["authorityDecisionRef"] == packet["entity_id"]


@pytest.mark.parametrize("decision", ["WAIT", "ESCALATE", "PAUSE", "STOP"])
def test_non_successor_decisions_never_create_cycle(tmp_path, decision):
    path = tmp_path / f"blocked-{decision.lower()}.sqlite"
    kwargs = {"wait_reason": "等待真实数据", "next_check_at": "2026-08-22T12:00:00+00:00"} if decision == "WAIT" else {}
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, predecessor, packet = prepare_decision(path, client, decision, **kwargs)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            result = control.authorize_successor(packet["entity_id"])
            assert result["cycle"] is None and result["claim"] is None and result["created"] is False
            trigger = control.claim_trigger(
                series_id=series["entity_id"], source_type="SCHEDULED", source_key=f"blocked:{decision}",
            )
            assert trigger["cycle"] is None
            expected = "CANCELLED" if decision == "STOP" else "CLAIMED"
            assert trigger["claim"]["lifecycle_status"] == expected
            assert RuntimeFoundation(database).get(predecessor["entity_id"])["data"]["autonomousControl"]["successorCycleRef"] is None
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1


def test_closed_cycle_cannot_be_bypassed_without_decision(tmp_path):
    path = tmp_path / "no-decision.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, cycle, _ = close_real_cycle(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with pytest.raises(AutonomousControlError, match="requires an applied Next-cycle Decision"):
                control.claim_trigger(series_id=series["entity_id"], source_type="RESULT", source_key="callback:bypass")
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1


def test_duplicate_and_restart_replay_return_same_claim_and_cycle(tmp_path):
    path = tmp_path / "replay.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, _, _, packet = prepare_decision(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            first = control.authorize_successor(packet["entity_id"])
            restarted = AutonomousOperatingControl(Database(str(path)))
            replay = restarted.authorize_successor(packet["entity_id"])
            assert replay["created"] is False
            assert replay["claim"]["entity_id"] == first["claim"]["entity_id"]
            assert replay["cycle"]["entity_id"] == first["cycle"]["entity_id"]
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 2
                assert connection.execute("select count(*) from runtime_entities where entity_type='TRIGGER_CLAIM'").fetchone()[0] == 2


def test_concurrent_successor_apply_is_exactly_once(tmp_path):
    path = tmp_path / "concurrent.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, _, _, _, packet = prepare_decision(path, client)

        def apply(_):
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
                return AutonomousOperatingControl(Database(str(path))).authorize_successor(packet["entity_id"])

        with ThreadPoolExecutor(max_workers=2) as pool:
            values = list(pool.map(apply, range(2)))
        assert len({item["cycle"]["entity_id"] for item in values}) == 1
        assert sorted(item["created"] for item in values) == [False, True]
        with database.connect() as connection:
            assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 2


def test_transaction_interruption_rolls_back_claim_cycle_and_lineage(tmp_path, monkeypatch):
    path = tmp_path / "transaction.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, _, predecessor, packet = prepare_decision(path, client)
        original_link = control._link
        monkeypatch.setattr(control, "_link", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("interrupt")))
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with pytest.raises(RuntimeError, match="interrupt"):
                control.authorize_successor(packet["entity_id"])
            with database.connect() as connection:
                assert connection.execute("select count(*) from runtime_entities where entity_type='CYCLE'").fetchone()[0] == 1
                assert connection.execute("select count(*) from runtime_entities where entity_type='TRIGGER_CLAIM'").fetchone()[0] == 1
            assert RuntimeFoundation(database).get(predecessor["entity_id"])["data"]["autonomousControl"]["successorCycleRef"] is None
            monkeypatch.setattr(control, "_link", original_link)
            assert control.authorize_successor(packet["entity_id"])["created"] is True


@pytest.mark.parametrize("field", ["strategyVersion", "envelopeVersion"])
def test_stale_decision_pins_fail_closed(tmp_path, field):
    path = tmp_path / f"stale-{field}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, _, _, packet = prepare_decision(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with database.connect() as connection:
                row = connection.execute("select data_json from runtime_entities where entity_id=?", (packet["entity_id"],)).fetchone()
                data = json.loads(row["data_json"])
                data[field] = "stale"
                connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), packet["entity_id"]))
            with pytest.raises(AutonomousControlError, match="authority is stale"):
                control.authorize_successor(packet["entity_id"])


@pytest.mark.parametrize("target", ["strategy", "envelope"])
def test_stale_series_strategy_or_envelope_body_fail_closed(tmp_path, target):
    path = tmp_path / f"stale-series-{target}.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, _, packet = prepare_decision(path, client)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with database.connect() as connection:
                row = connection.execute("select data_json from runtime_entities where entity_id=?", (series["entity_id"],)).fetchone()
                data = json.loads(row["data_json"])
                current = data["strategyVersions"][-1]
                if target == "strategy":
                    current["bodyHash"] = "stale"
                else:
                    current["envelope"]["bodyHash"] = "stale"
                connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), series["entity_id"]))
            with pytest.raises(AutonomousControlError, match="authority is stale"):
                control.authorize_successor(packet["entity_id"])


def test_unapplied_invalid_adjustment_inactive_series_active_cycle_and_cross_tenant_fail_closed(tmp_path):
    path = tmp_path / "gates.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": ControlledProvider().execute})) as client:
        database, control, series, _, packet = prepare_decision(
            path, client, "ADJUST", adjustment={"changes": {"tactic": "smaller-batch"}},
        )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-phase1", role="test"):
            with database.connect() as connection:
                connection.execute("update runtime_entities set lifecycle_status='READY' where entity_id=?", (packet["entity_id"],))
            with pytest.raises(AutonomousControlError, match="not applied successor authority"):
                control.authorize_successor(packet["entity_id"])
            with database.connect() as connection:
                connection.execute("update runtime_entities set lifecycle_status='APPLIED' where entity_id=?", (packet["entity_id"],))
                row = connection.execute("select data_json from runtime_entities where entity_id=?", (packet["entity_id"],)).fetchone()
                data = json.loads(row["data_json"])
                data["adjustment"] = {"changes": {"goal": "forbidden"}}
                connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), packet["entity_id"]))
            with pytest.raises(AutonomousControlError, match="outside the Approved Strategy Envelope"):
                control.authorize_successor(packet["entity_id"])
            with database.connect() as connection:
                data["adjustment"] = {"changes": {"tactic": "smaller-batch"}}
                connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), packet["entity_id"]))
            control.set_series_state(series["entity_id"], "WAITING", next_check_at="2026-08-22T12:00:00+00:00")
            with pytest.raises(AutonomousControlError, match="ACTIVE Operating Series"):
                control.authorize_successor(packet["entity_id"])
            control.set_series_state(series["entity_id"], "ACTIVE")
            RuntimeFoundation(database).create(
                "CYCLE", company_id=COMPANY, workspace_id=series["workspace_id"], parent_id=series["entity_id"],
                data={"autonomousControl": {"seriesRef": series["entity_id"]}},
            )
            with pytest.raises(AutonomousControlError, match="while another Cycle is active"):
                control.authorize_successor(packet["entity_id"])
        with TenantContext.scope("tenant-other", company_id=COMPANY, role="test"):
            with pytest.raises(KeyError):
                AutonomousOperatingControl(database).authorize_successor(packet["entity_id"])
