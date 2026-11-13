"""Recovery contract checks with isolated local HTTP responses, not cloud acceptance."""
import asyncio
import copy
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.meeting_service import MeetingService
from app.runtime.foundation import RuntimeScopeError
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import seed, MeetingProvider, COMPANY, TENANT, HEADERS, PREFIX
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


def counts(db):
    with db.connect() as conn:
        return {table: conn.execute(f"select count(*) from {table}").fetchone()[0]
                for table in ("tasks", "artifacts", "ai_usage_records", "runtime_entities", "evolution_events")}


def interrupted(tmp_path, monkeypatch, *, accounted=False, stop_type="meeting-self-judgment"):
    path = tmp_path / "reuse.sqlite"
    db, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    mid = _create_meeting(db, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    original = MeetingService._execute_on_work
    captured = {}

    async def stop_after_completion(self, meeting, assignment, **kwargs):
        result = await original(self, meeting, assignment, **kwargs)
        if kwargs["expected_type"] != stop_type:
            return result
        captured.update(meeting=meeting, assignment=assignment, kwargs=kwargs, result=result)
        if accounted:
            state = copy.deepcopy(meeting["orchestration"])
            self._merge_usage(state, result["usage"])
            self._save(meeting, orchestration=state)
        raise RuntimeError("test interruption after completion before event consumption")

    with monkeypatch.context() as patch:
        patch.setattr(MeetingService, "_execute_on_work", stop_after_completion)
        with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
            client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
    assert captured
    return path, db, provider, mid, captured


def test_resume_after_leader_completion_does_not_duplicate_visible_contribution(tmp_path, monkeypatch):
    path, db, provider, mid, c = interrupted(tmp_path, monkeypatch, stop_type="meeting-leader-evaluation")
    assert len(provider.calls) == 4
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        before = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        after = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    assert after["orchestration"]["status"] == "WAITING_CEO", after["orchestration"]
    assert len(provider.calls) == 12
    refs = [m["resultRef"] for m in after["timeline"] if m.get("resultRef")]
    assert len(refs) == len(set(refs))
    assert all(m in after["timeline"] for m in before["timeline"])


def test_new_evidence_does_not_rewrite_pending_events_completed_execution(tmp_path, monkeypatch):
    path, db, provider, mid, c = interrupted(tmp_path, monkeypatch)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(db)
        work = service.foundation.get(c["result"]["workRef"])
        cycle_before = service.foundation.get(work["parent_id"])
        evidence = service.knowledge.create_entry(title="New fictional source", body="Test input, not customer fact",
            company_id=COMPANY, target_type="WORKSPACE", target_ref=work["workspace_id"])
        service.add_message(COMPANY, mid, actor_type="CEO", actor_ref="", text="Supplement selected test input",
                            context_refs=[{"type": "KNOWLEDGE", "ref": evidence["id"]}])
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        after = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    assert after["orchestration"]["status"] == "WAITING_CEO", after["orchestration"]
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        assert MeetingService(db).foundation.get(work["parent_id"]) == cycle_before
        with db.connect() as conn:
            assert conn.execute("select count(*) from ai_usage_records where task_id=?",
                                (c["result"]["taskRef"],)).fetchone()[0] == 1


@pytest.mark.parametrize("accounted", [False, True])
def test_completed_reuse_is_read_only_and_accounting_is_idempotent(tmp_path, monkeypatch, accounted):
    path, db, provider, mid, c = interrupted(tmp_path, monkeypatch, accounted=accounted)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(db)
        work = service.foundation.get(c["result"]["workRef"])
        assert work["data"]["responsibilityRouting"]["status"] == "COMPLETED"
        before = counts(db)
        for _ in range(2):
            result = asyncio.run(service._execute_on_work(c["meeting"], c["assignment"],
                                **(c["kwargs"] | {"work": work})))
            assert result["parsed"] == c["result"]["parsed"]
            assert result["taskRef"] == c["result"]["taskRef"]
        assert counts(db) == before and len(provider.calls) == 1
        state = service.get(COMPANY, mid)["orchestration"]
        service._merge_usage(state, result["usage"])
        once = copy.deepcopy(state)
        service._merge_usage(state, result["usage"])
        assert state == once
        assert state["providerCallCount"] == 1 and state["usage"]["confirmedTokens"] == 20
        with pytest.raises(ValueError, match="active responsibility"):
            service.routing.begin_employee_execution(work["entity_id"], execution_key="new-attempt")

    # A new application instance; two simultaneous requests must consume only once.
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(lambda _: client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS), range(2)))
        final = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    assert final["orchestration"]["status"] == "WAITING_CEO", final["orchestration"]
    assert provider.gate_counts[c["assignment"]["runtimeEmployeeRef"]] == 3  # three distinct events, no replay
    assert final["orchestration"]["providerCallCount"] == len(provider.calls)
    assert final["orchestration"]["usage"]["confirmedTokens"] == len(provider.calls) * 20
    turns = final["orchestration"]["turns"]
    assert len({t["event"]["eventId"] for t in turns}) == len(turns)
    before = counts(db)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
    assert counts(db) == before


@pytest.mark.parametrize("wrong", ["meeting", "event", "employee", "purpose", "company", "tenant", "task", "artifact", "result", "failed", "cancelled", "missing-artifact", "missing-usage", "task-key", "callback"])
def test_completed_reuse_rejects_mismatched_or_missing_truth(tmp_path, monkeypatch, wrong):
    _, db, provider, mid, c = interrupted(tmp_path, monkeypatch)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(db)
        meeting = copy.deepcopy(c["meeting"])
        assignment = copy.deepcopy(c["assignment"])
        kwargs = c["kwargs"] | {"work": service.foundation.get(c["result"]["workRef"])}
        if wrong == "meeting":
            meeting["meeting_id"] = "other-meeting"
        elif wrong == "event":
            kwargs["execution_key"] = kwargs["execution_key"].replace("meeting-event-", "wrong-event-")
        elif wrong == "employee":
            assignment["runtimeEmployeeRef"] = "other-employee"
        elif wrong == "purpose":
            kwargs["expected_type"] = "meeting-contribution"
        elif wrong == "company":
            meeting["company_id"] = "other-company"
        elif wrong == "tenant":
            kwargs["work"]["tenant_id"] = "other-tenant"
        else:
            # Deliberate corruption is confined to this test's external SQLite.
            with db.connect() as conn:
                if wrong == "task":
                    conn.execute("update tasks set status='RUNNING' where task_id=?", (c["result"]["taskRef"],))
                elif wrong == "artifact":
                    conn.execute("update artifacts set content='corrupted' where task_id=?", (c["result"]["taskRef"],))
                elif wrong in {"failed", "cancelled", "callback"}:
                    work = kwargs["work"]
                    record = work["data"]["responsibilityRouting"]["executions"][kwargs["execution_key"]]
                    if wrong == "callback":
                        record["provenance"]["callback_actor_ref"] = "other-actor"
                    else:
                        record["status"] = wrong.upper()
                    conn.execute("update runtime_entities set data_json=? where entity_id=?",
                                 (json.dumps(work["data"]), work["entity_id"]))
                elif wrong == "missing-artifact":
                    conn.execute("delete from artifacts where task_id=?", (c["result"]["taskRef"],))
                elif wrong == "missing-usage":
                    # Simulate a damaged external fixture, never migrate production.
                    conn.execute("drop trigger ai_usage_records_no_delete")
                    conn.execute("delete from ai_usage_records where task_id=?", (c["result"]["taskRef"],))
                elif wrong == "task-key":
                    conn.execute("update tasks set execution_ref='other-key' where task_id=?", (c["result"]["taskRef"],))
                else:
                    conn.execute("update tasks set output='' where task_id=?", (c["result"]["taskRef"],))
        before = counts(db)
        with pytest.raises((ValueError, KeyError, RuntimeScopeError)):
            asyncio.run(service._execute_on_work(meeting, assignment, **kwargs))
        assert counts(db) == before and len(provider.calls) == 1
