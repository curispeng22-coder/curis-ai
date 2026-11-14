"""T-006: persisted cross-layer closing, using controlled HTTP only."""
import asyncio
import inspect
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.conversation_service import ConversationService
from app.database import Database
from app.model_gateway import ModelGatewayAdapter
from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime, ResponsibilityRoutingError
from app.writing_chapter_service import WritingChapterService
from backend.tests import test_writing_chapter_vertical as vertical
from backend.tests.test_writing_selected_execution import ready, explicit_work, COMPANY, CEO, scope
from backend.tests.test_writing_chapter_vertical import command


@pytest.fixture
def writing(tmp_path, monkeypatch):
    # The historical artifact isn't shipped in this worktree. Use the shipped
    # package, still checked by setup's exact PACKAGE_DIGEST assertion.
    monkeypatch.setattr(vertical, "SOURCE", Path(__file__).resolve().parents[1] /
                        "app/bundled_workspace_packages/writing_authoring")
    return ready(tmp_path, monkeypatch)


def projection(app, workspace, work):
    with TestClient(app) as client:
        response = client.get("/api/workspace/runtime/foundation/team-operating/definition",
            params=dict(company_id=COMPANY, workspace_id=workspace, scope_type="WORKSPACE",
                        scope_ref=workspace, workflow_key="writing-fixture-work"),
            headers={"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO})
        assert response.status_code == 200, response.text
        return next(row for row in response.json()["running_work"] if row["work_ref"] == work)


@pytest.mark.parametrize("outcome", ["success", "failure", "cancelled", "retryable", "unknown"])
def test_five_outcomes_cross_layer_and_cold_no_replay(writing, monkeypatch, outcome):
    db, app, entry, service, calls, w, b, c, binding = writing
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    with scope():
        claim, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"],
            body="明确交办", request_id="state-case", model_key="model.writing-entry", work_ref=work)
        assert created
        original_grant = entry.execution_grant
        if outcome == "failure":
            entry.execution_grant = None  # Confirmed preflight failure, no Task.
        if outcome == "retryable":
            original = ResponsibilityRoutingRuntime.attach_provider_task
            def failed_attach(*args, **kwargs):
                raise RuntimeError("controlled transaction rollback before outbound")
            monkeypatch.setattr(ResponsibilityRoutingRuntime, "attach_provider_task", failed_attach)
        original_execute = ModelGatewayAdapter.execute
        def controlled(self, prompt, **kwargs):
            if outcome == "unknown":
                raise RuntimeError("controlled lost acknowledgement")
            result = original_execute(self, prompt, **kwargs)
            if outcome == "cancelled":
                ResponsibilityRoutingRuntime(db).cancel_work(work, reason="回执前取消")
            return result
        monkeypatch.setattr(ModelGatewayAdapter, "execute", controlled)
        endpoint = next(route.endpoint for route in app.routes
                        if getattr(route, "path", "").endswith("/chapters/{chapter_ref}/messages"))
        executor = inspect.getclosurevars(endpoint).nonlocals["executor"]
        asyncio.run(entry.conversations.execute(claim, executor))
        retained = RuntimeFoundation(db).get(work)
        routing = retained["data"]["responsibilityRouting"]
        expected = {"success": ("ACTIVE", "ACCEPTED"), "failure": ("WAITING", "FAILED"),
                    "retryable": ("WAITING", "FAILED"), "cancelled": ("CANCELLED", "CANCELLED"),
                    "unknown": ("WAITING", "FAILED")}[outcome]
        assert (routing["status"], routing["executions"][claim["attempt_id"]]["status"]) == expected
        if outcome == "unknown":
            assert routing["executions"][claim["attempt_id"]]["provenance"]["effect_status"] == "UNKNOWN"
        assert routing["currentExecutorRef"] is None
        assert retained["data"]["workContext"]["currentExecutorRef"] is None
        assert retained["data"]["workContext"]["status"] != "executing"
        assert retained["lifecycle_status"] == "ACTIVE"  # No implicit adoption.
        assert not retained["data"].get("acceptanceRefs")
        assert service.chapter(COMPANY, w, b, c)["draft"]["text"] == "雨停以后，书桌上的信仍未打开。"
    listed = projection(app, w, work)
    assert listed["work_status"] == expected[0]
    assert listed["current_executor_ref"] is None
    with db.connect() as con:
        tasks = [tuple(row) for row in con.execute("select task_id,status from tasks where work_ref=?", (work,))]
        events = con.execute("select count(*) from evolution_events").fetchone()[0]
    if outcome in {"failure", "retryable"}:
        assert tasks == [] and calls == []
    else:
        assert len(tasks) == 1
        assert tasks[0][1] == ("FAILED" if outcome == "unknown" else "COMPLETED")
    if outcome == "failure":
        entry.execution_grant = original_grant
    if outcome == "retryable":
        monkeypatch.setattr(ResponsibilityRoutingRuntime, "attach_provider_task", original)
    cold_db = Database(db.path)
    cold = ConversationService(cold_db)
    cold.selection_validator = entry.conversations.selection_validator
    dispatched = []
    async def forbidden(task):
        dispatched.append(task)
        raise AssertionError("A finished request must not replay")
    with scope():
        before = cold.read_request(COMPANY, claim["conversation_id"], "state-case")
        assert before["attempts"][0]["effect_status"] == ("UNKNOWN" if outcome in {"cancelled", "unknown"} else "SETTLED")
        asyncio.run(cold.execute(claim, forbidden))
        assert RuntimeFoundation(cold_db).get(work) == retained
        assert cold.read_request(COMPANY, claim["conversation_id"], "state-case") == before
    assert dispatched == []
    with cold_db.connect() as con:
        assert [tuple(row) for row in con.execute("select task_id,status from tasks where work_ref=?", (work,))] == tasks
        assert con.execute("select count(*) from evolution_events").fetchone()[0] == events
    if outcome == "retryable":
        monkeypatch.setattr(ResponsibilityRoutingRuntime, "attach_provider_task", original)
        with scope():
            retry, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"],
                body="明确交办", request_id="state-case", retry_no=1,
                model_key="model.writing-entry", work_ref=work)
            assert created and retry["attempt_id"] != claim["attempt_id"]
            asyncio.run(entry.conversations.execute(retry, executor))
            updated = RuntimeFoundation(db).get(work)["data"]["responsibilityRouting"]
            assert updated["executions"][claim["attempt_id"]]["status"] == "FAILED"
            assert updated["executions"][retry["attempt_id"]]["status"] == "ACCEPTED"
            assert updated["currentExecutorRef"] is None
            assert len(calls) == 1
    if outcome == "success":
        entry.execution_grant = {**entry.execution_grant, "grant_ref": "controlled-second-work"}
        assignment = claim["context"]["assignment_ref"]
        with scope():
            draft = service.chapter(COMPANY, w, b, c)["draft"]
        with TestClient(app) as client:
            second = client.post(
                f"/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work",
                headers={"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO},
                json={"request_id": "second-work", "problem": "第二个明确交办", "expected_result": "候选正文",
                      "model_key": "model.writing-entry", "source": {"kind": "writing", "book_ref": b,
                      "chapter_ref": c, "expected_draft_ref": draft["ref"], "selection": binding["selection"]}})
            assert second.status_code == 200, second.text
        second_ref = second.json()["work"]["entity_id"]
        assert second_ref != work
        with scope():
            next_claim, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"],
                body="第二个明确交办", request_id="second-request", model_key="model.writing-entry", work_ref=second_ref)
            assert created
            asyncio.run(entry.conversations.execute(next_claim, executor))
            assert RuntimeFoundation(db).get(work) == retained
            second_route = RuntimeFoundation(db).get(second_ref)["data"]["responsibilityRouting"]
            assert second_route["executions"][next_claim["attempt_id"]]["status"] == "ACCEPTED"
            assert second_route["currentExecutorRef"] is None
            assert second_route["responsibilityHolderRef"] == routing["responsibilityHolderRef"]
            assert len(calls) == 2
            reply = before["messages"][-1]
            candidate = command(service, w, b, c, "candidate.recorded", {
                "binding_ref": binding["ref"], "message_ref": reply["message_id"],
                "reply_start": 0, "reply_end": len(reply["body"].encode("utf-16-le")) // 2,
                "reply_excerpt": reply["body"]})
            command(service, w, b, c, "candidate.adopted", {"candidate_ref": candidate["ref"], "confirmed": True})
            adopted_work = RuntimeFoundation(db).get(work)
            assert adopted_work["lifecycle_status"] == "COMPLETED"
            assert adopted_work["data"]["responsibilityRouting"]["status"] == "COMPLETED"
            final_cold = ConversationService(Database(db.path))
            asyncio.run(final_cold.execute(claim, forbidden))
            assert RuntimeFoundation(final_cold.db).get(work) == adopted_work
            assert dispatched == [] and len(calls) == 2
        assert projection(app, w, work)["work_status"] == "COMPLETED"
    if outcome in {"unknown", "cancelled"}:
        with scope(), pytest.raises(ResponsibilityRoutingError):
            ResponsibilityRoutingRuntime(db).begin_employee_execution(work, execution_key="unsafe-retry")
        with scope(), pytest.raises(ResponsibilityRoutingError):
            ResponsibilityRoutingRuntime(db).attach_provider_task(work,
                execution_key=claim["attempt_id"], task_ref=tasks[0][0])
        with scope():
            assert RuntimeFoundation(db).get(work) == retained
