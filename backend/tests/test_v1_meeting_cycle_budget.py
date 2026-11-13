"""Per-event budget boundaries; disposable SQLite, not live-cloud acceptance."""
import copy
import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.meeting_service import MeetingService
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import seed, COMPANY, TENANT, MeetingProvider, PREFIX, HEADERS
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


def setup(tmp_path):
    db, employees, knowledge = seed(tmp_path / "cycle.sqlite")
    mid = _create_meeting(db, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    return db, MeetingService(db), mid, knowledge


def exhaust(service, mid):
    assert service._claim_advance(mid)
    meeting = service.db.get_strategy_meeting(TENANT, mid)
    state = meeting["orchestration"]
    state["usage"]["confirmedTokens"] = 80000
    state["providerCallCount"] = 10
    state["currentCycle"]["usage"]["confirmedTokens"] = 80000
    state["currentCycle"]["providerCallCount"] = 10
    return service._finish_advance(meeting, state, status="BLOCKED", outcome="BLOCKED",
                                   reason=service._budget_reason(state))["orchestration"]


def test_same_event_and_restart_cannot_refill(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        before = exhaust(service, mid)
        for instance in (service, MeetingService(db), MeetingService(db)):
            assert instance._claim_advance(mid) is None
            after = db.get_strategy_meeting(TENANT, mid)["orchestration"]
            assert after["currentCycle"] == before["currentCycle"]
            assert after["usage"] == before["usage"]


@pytest.mark.parametrize("kind", ["CEO_MESSAGE", "RESULT_RETURNED"])
def test_new_persisted_event_has_new_budget_not_new_lifetime(tmp_path, kind):
    db, service, mid, knowledge = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        before = exhaust(service, mid)
        if kind == "CEO_MESSAGE":
            service.add_message(COMPANY, mid, actor_type="CEO", actor_ref="", text="补充已选来源，重新评估",
                                context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
        else:
            # This service-level event path is used by canonical Result synchronization.
            service._queue_event(mid, service._event(kind, mid, refs=["test-result-reference"]))
        assert service._claim_advance(mid)
        state = db.get_strategy_meeting(TENANT, mid)["orchestration"]
        assert state["currentCycle"]["cycleId"] != before["currentCycle"]["cycleId"]
        assert state["currentCycle"]["usage"]["confirmedTokens"] == 0
        assert state["usage"] == before["usage"]
        assert state["providerCallCount"] == 10
        assert service._claim_advance(mid) is None
        assert not service._budget_reason(state)


def test_internal_descendant_does_not_refill(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        before = exhaust(service, mid)
        derived = service._cycle_event(before, "LEADER_REQUEST", "already-completed-task")
        service._queue_event(mid, derived)
        assert service._claim_advance(mid) is None
        after = db.get_strategy_meeting(TENANT, mid)["orchestration"]
        assert after["currentCycle"] == before["currentCycle"]


def test_requeued_consumed_event_keeps_its_original_budget(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        assert service._claim_advance(mid)
        meeting = db.get_strategy_meeting(TENANT, mid)
        state = meeting["orchestration"]
        event = copy.deepcopy(state["pendingEvents"][0])
        event.pop("budgetCycleId")
        state["lastProcessedEventId"] = event["eventId"]
        closed = service._finish_advance(meeting, state, status="SUFFICIENT", outcome="DISCUSSION_SUFFICIENT", pending=[])
        service._queue_event(mid, event)
        assert service._claim_advance(mid) is None
        restored = db.get_strategy_meeting(TENANT, mid)["orchestration"]
        assert restored["currentCycle"]["cycleId"] == closed["orchestration"]["currentCycle"]["cycleId"]
        assert restored["pendingEvents"][0]["budgetCycleId"] == restored["currentCycle"]["cycleId"]


def test_budget_task_inventory_rejects_wrong_ownership(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        meeting = db.get_strategy_meeting(TENANT, mid)
        with db.connect() as conn:
            # Deliberately conflicting isolated rows must not influence the budget.
            for task, company, workspace in [("wrong-company", "other", meeting["workspace_id"]),
                                              ("wrong-workspace", COMPANY, "other")]:
                conn.execute("insert into tasks(task_id,tenant_id,company_id,workspace_id,execution_ref,content,status) "
                             "values (?,?,?,?,?,?,'COMPLETED')",
                             (task, TENANT, company, workspace, f"meeting:{mid}:test", "isolated corruption test"))
        assert service._meeting_task_refs(mid) == []


def test_cycle_accounting_reuses_one_ledger_without_old_task_charge():
    state = MeetingService._orchestration()
    state["currentCycle"] = {"excludedTaskRefs": ["old"], "usage": {}, "providerCallCount": 0}
    usage = {"ledgerSnapshot": {"providerCallCount": 2,
        "usage": {"confirmedTokens": 80020, "confirmedCost": "0", "unknownMetering": True}},
        "ledgerRows": [
            {"task_id": "old", "total_tokens": 80000, "cost_amount": None, "metering_status": "confirmed"},
            {"task_id": "new", "total_tokens": 20, "cost_amount": None, "metering_status": "confirmed"},
        ]}
    MeetingService._merge_usage(state, usage)
    once = copy.deepcopy(state)
    MeetingService._merge_usage(state, usage)
    assert state == once
    assert state["usage"]["confirmedTokens"] == 80020
    assert state["currentCycle"]["usage"]["confirmedTokens"] == 20
    assert state["currentCycle"]["providerCallCount"] == 1


def test_legacy_history_is_not_reset_or_reclassified_as_new(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        meeting = db.get_strategy_meeting(TENANT, mid)
        state = meeting["orchestration"]
        state.pop("budgetVersion", None)
        state["usage"]["confirmedTokens"] = 84844
        state["providerCallCount"] = 19
        service._save(meeting, orchestration=state)
        assert service._claim_advance(mid) is None
        restored = db.get_strategy_meeting(TENANT, mid)["orchestration"]
        assert restored["usage"]["confirmedTokens"] == 84844
        assert restored["currentCycle"]["usage"]["confirmedTokens"] == 84844
        assert restored["currentCycle"]["legacy"] is True


def test_elapsed_cycle_cannot_be_refilled_by_reclaim(tmp_path):
    db, service, mid, _ = setup(tmp_path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        assert service._claim_advance(mid)
        meeting = db.get_strategy_meeting(TENANT, mid)
        state = meeting["orchestration"]
        state["currentCycle"]["startedAt"] = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
        state["activeRunId"] = ""
        state["runStartedAt"] = None
        service._save(meeting, orchestration=state)
        assert service._claim_advance(mid) is None
        restored = db.get_strategy_meeting(TENANT, mid)["orchestration"]
        assert restored["currentCycle"]["startedAt"] == state["currentCycle"]["startedAt"]
        assert restored["currentCycle"]["exhausted"]


def test_real_ledger_cycles_preserve_usage_and_do_not_replay(tmp_path):
    path = tmp_path / "ledger.sqlite"
    db, employees, knowledge = seed(path)
    mid = _create_meeting(db, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    provider = MeetingProvider(knowledge)
    original = provider.http_post

    def expensive_once(*args):
        result = original(*args)
        if len(provider.calls) <= 2:
            result["usage"] = {"prompt_tokens": 39990, "completion_tokens": 10, "total_tokens": 40000}
        return result

    provider.http_post = expensive_once
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        stopped = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()["orchestration"]
        assert stopped["status"] == "BLOCKED"
        assert stopped["currentCycle"]["usage"]["confirmedTokens"] == 80000
        assert len(provider.calls) == 2
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        assert len(provider.calls) == 2
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        assert len(provider.calls) == 2
        response = client.post(f"{PREFIX}/{mid}/messages", headers=HEADERS, json={
            "actor_type": "CEO", "text": "请评估已选资料的验证方法与假设边界", "context_refs": [{"type": "KNOWLEDGE", "ref": knowledge}],
        })
        assert response.status_code == 200
        current = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()["orchestration"]
        assert current["status"] == "WAITING_CEO", current
        assert current["usage"]["confirmedTokens"] == 80000 + (len(provider.calls) - 2) * 20
        assert current["currentCycle"]["usage"]["confirmedTokens"] == (len(provider.calls) - 2) * 20
        assert current["providerCallCount"] == len(provider.calls)
        assert current["cycleHistory"][0]["usage"]["confirmedTokens"] == 80000
        assert current["currentCycle"]["cycleId"] != stopped["currentCycle"]["cycleId"]
    before = len(provider.calls)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        assert client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()["orchestration"] == current
    assert len(provider.calls) == before


def test_evidence_wait_ends_cycle_and_new_source_starts_another(tmp_path):
    path = tmp_path / "evidence.sqlite"
    db, employees, knowledge = seed(path)
    mid = _create_meeting(db, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    provider = MeetingProvider(knowledge)
    original = provider.execute

    def request_missing_source(prompt):
        result = original(prompt)
        payload = json.loads(result["output"])
        if payload["resultType"] == "meeting-leader-evaluation":
            payload.update(outcome="REQUEST_EVIDENCE", evidenceRefs=[], summary="缺少可核验来源")
            result["output"] = json.dumps(payload)
        return result

    provider.execute = request_missing_source
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        first = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()["orchestration"]
        assert first["currentCycle"]["endedAt"] and first["status"] == "BLOCKED"
        calls = len(provider.calls)
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        assert len(provider.calls) == calls
        client.post(f"{PREFIX}/{mid}/messages", headers=HEADERS, json={
            "actor_type": "CEO", "text": "请重新核对资料中的问题边界",
            "context_refs": [{"type": "KNOWLEDGE", "ref": knowledge}],
        })
        second = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()["orchestration"]
        assert second["currentCycle"]["cycleId"] != first["currentCycle"]["cycleId"]
        assert second["currentCycle"]["providerCallCount"] == len(provider.calls) - calls
        assert second["providerCallCount"] == len(provider.calls)
