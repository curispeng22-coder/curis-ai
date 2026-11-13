"""Shared executor/actual canonical Usage with injected HTTP; no network."""
import asyncio
import json
from dataclasses import replace
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter
from app.identity_membership import IdentityMembership
from app.writing_entry_service import WritingEntryService
from app.writing_chapter_service import WritingChapterService, WritingConflict
from app.runtime import RuntimeScopeError
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO, command


def ready(tmp_path, monkeypatch, *, fail=False):
    db, _, w, b, c = setup(tmp_path)
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) values ('writing-entry-employee','selfuse',?,'writing-test-department','et_product_manager','章节作者','写作','idle')", (COMPANY,))
        con.execute("insert into official_models(model_key,provider_id,display_name,supported_models,gateway_ref,status,default_model,type,name) values ('model.writing-entry','controlled-provider','Controlled','[\"contract-model\"]','writing-entry-test','active','contract-model','model','Controlled')")
    calls = []
    def post(url, payload, headers, timeout):
        calls.append(payload)
        if fail: raise RuntimeError("controlled outbound unavailable")
        return {"choices": [{"message": {"content": "第二段可以改成：灯光照亮了陌生邮戳。"}}], "usage": {"prompt_tokens": 8, "completion_tokens": 7, "total_tokens": 15}}
    adapter = ModelGatewayAdapter(base_url="https://provider.invalid", api_key="test-only", gateway_id="writing-entry-test", model_name="contract-model", http_post=post)
    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request: replace(original(self, tenant, request), role="ceo"))
    app = create_app(str(db.path), model_gateway_adapter=adapter)
    entry = app.state.writing_entry_service
    entry.execution_grant = dict(tenant_id="selfuse", company_id=COMPANY, workspace_id=w, model_key="model.writing-entry", grant_ref="controlled-single-use", max_output_tokens=128, max_input_bytes=50000, max_cost_usd=1, price_version="controlled-zero-price", price_upper_bound_usd_per_input_byte=0, price_upper_bound_usd_per_output_token=0, effective_system_authorization=True, source_class="CONTROLLED_EXECUTOR")
    service = WritingChapterService(db, conversation_service=entry.conversations, entry_service=entry)
    with scope():
        before = entry.metadata(COMPANY, w)
        revision = before["assignment_revision"]
        already_assigned = bool(before["assignment_ref"]) and before["company_employee_ref"] == "writing-entry-employee"
        assigned = entry.assign(COMPANY, w, "writing-entry-employee", revision)
        assert assigned["company_employee_ref"] == "writing-entry-employee"
        assert assigned["assignment_revision"] == revision + (0 if already_assigned else 1)
        chosen = entry.select_model(COMPANY, w, "model.writing-entry")
        assert chosen["execution"]["status"] == "AVAILABLE", chosen
        draft = command(service, w, b, c, "draft.saved", {"text": "雨停以后，书桌上的信仍未打开。", "knowledge": []})["draft"]
        selection = {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 0, "end": 4, "excerpt": "雨停以后", "anchor": draft["ref"] + ":0:4", "knowledge": []}
        binding = service.bind_discussion(COMPANY, w, b, c, request_id="binding", expected_draft_ref=draft["ref"], data={"selection": selection})
    return db, app, entry, service, calls, w, b, c, binding


@pytest.mark.parametrize("fail", [False, True])
def test_selected_actual_single_usage_and_unknown_failure(tmp_path, monkeypatch, fail):
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch, fail=fail)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}"
    payload = dict(binding_ref=binding["ref"], body="只讨论所选句子", request_id="original", model_key="model.writing-entry")
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        response = client.post(root + "/messages", json=payload, headers=headers)
        assert response.status_code == 202, response.text
        state = client.get(root + "/discussion/" + binding["ref"], headers=headers).json()
        assert len(calls) == 1, state
        assert calls[0]["max_tokens"] == 128
        assert state["attempts"][0]["effect_status"] == ("UNKNOWN" if fail else "SETTLED"), state
        assert len([m for m in state["messages"] if m["sender"]["kind"] == "EMPLOYEE"]) == (0 if fail else 1), state
        # Client cannot grant execution and never causes another outbound attempt.
        assert client.post(root + "/messages", json={**payload, "allow_execution": True}, headers=headers).status_code == 422
        client.post(root + "/messages", json=payload, headers=headers)
        assert len(calls) == 1
    with db.connect() as con:
        rows = con.execute("select * from ai_usage_records where company_id=? and workspace_id=?", (COMPANY, w)).fetchall()
        assert len(rows) == 1
        assert rows[0]["capability_id"] == "model.writing-entry" and rows[0]["fallback_from_model"] is None
        assert rows[0]["cost_amount"] is None and rows[0]["cost_source"] == "unknown"
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
    with scope():
        if fail:
            with pytest.raises(WritingConflict): entry.assign(COMPANY, w, "writing-entry-employee", entry.metadata(COMPANY, w)["assignment_revision"])
            assert entry.metadata(COMPANY, w)["pending"][0]["status"] == "UNKNOWN"
        else:
            reply = state["messages"][-1]
            assert reply["provenance"]["source_class"] == "CONTROLLED_EXECUTOR"
            assert reply["provenance"]["usage"]["usage_record_id"] == rows[0]["usage_record_id"]
            replacement = reply["body"]
            candidate = command(service, w, b, c, "candidate.recorded", {
                "binding_ref": binding["ref"], "message_ref": reply["message_id"],
                "reply_start": 0, "reply_end": len(replacement.encode("utf-16-le")) // 2,
                "reply_excerpt": replacement})
            adopted = command(service, w, b, c, "candidate.adopted", {"candidate_ref": candidate["ref"], "confirmed": True})
            assert adopted["draft"]["text"] == replacement + "，书桌上的信仍未打开。"
            assert len(calls) == 1
            cold = WritingChapterService(db)
            assert cold.chapter(COMPANY, w, b, c)["draft"]["sha256"] == adopted["draft"]["sha256"]


@pytest.mark.parametrize("tamper", ["draft", "assignment", "model", "grant", "binding"])
def test_preflight_tamper_no_outbound(tmp_path, monkeypatch, tamper):
    db, _, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    with scope():
        claim, _ = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"], body="受控测试", request_id="pending", model_key="model.writing-entry")
        with pytest.raises(WritingConflict): entry.assign(COMPANY, w, "writing-entry-employee", entry.metadata(COMPANY, w)["assignment_revision"])
        with pytest.raises(WritingConflict): entry.select_model(COMPANY, w, "model.writing-entry")
        if tamper == "draft": command(service, w, b, c, "draft.saved", {"text": "变更正文", "knowledge": []}, request="changed")
        elif tamper == "grant": entry.execution_grant = None
        else:
            with db.connect() as con:
                if tamper == "model": con.execute("update official_models set status='inactive' where model_key='model.writing-entry'")
                elif tamper == "binding": con.execute("update employee_capability_bindings set enabled=0 where id=?", (claim["execution_selection"]["binding_id"],))
                else:
                    row = con.execute("select data_json from runtime_entities where entity_id=?", (binding["assignment_ref"],)).fetchone()
                    data = json.loads(row[0]); data["revision"] += 1
                    con.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), binding["assignment_ref"]))
        async def forbidden(task): raise AssertionError("Preflight should reject before executor")
        asyncio.run(entry.conversations.execute(claim, forbidden))
        state = service.discussion(COMPANY, w, b, c, binding["ref"])
        assert state["attempts"][0]["status"] == "FAILED"
        assert state["attempts"][0]["effect_status"] == "SETTLED"
        assert len(state["messages"]) == 1 and calls == []
        with db.connect() as con: assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0


def explicit_work(db, app, entry, service, w, b, c, binding, *, concurrent=False):
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    with scope():
        assignment = entry.metadata(COMPANY, w)["assignment_ref"]
        ResponsibilityRoutingRuntime(db).publish_workflow(company_id=COMPANY, workspace_id=w,
            scope_type="WORKSPACE", scope_ref=w, workflow_key="writing-fixture-work",
            assignment_refs=[assignment], default_flow=["WRITING_CHAPTER_AUTHOR"])
        draft = service.chapter(COMPANY, w, b, c)["draft"]
    payload = {"request_id": "explicit-work", "problem": "明确交办", "expected_result": "待作者采用的正文候选",
               "model_key": "model.writing-entry", "source": {"kind": "writing", "book_ref": b,
               "chapter_ref": c, "expected_draft_ref": draft["ref"], "selection": binding["selection"]}}
    url = f"/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        if concurrent:
            from concurrent.futures import ThreadPoolExecutor
            from threading import Barrier
            gate = Barrier(2)
            def submit():
                gate.wait(timeout=5)
                return client.post(url, json=payload, headers=headers)
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(submit) for _ in range(2)]
                response, replay = [future.result(timeout=10) for future in futures]
        else:
            response = client.post(url, json=payload, headers=headers)
            replay = client.post(url, json=payload, headers=headers)
        assert response.status_code == 200, response.text
        assert replay.status_code == 200, replay.text
        assert replay.json()["work"]["entity_id"] == response.json()["work"]["entity_id"]
    work_ref = response.json()["work"]["entity_id"]
    with TestClient(app) as client:
        blocked = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{work_ref}/execute?max_executions=1", headers=headers)
        assert blocked.status_code == 422, blocked.text
        assert blocked.json()["detail"] == "Writing Model Work executes only through its original chapter request"
    return work_ref


@pytest.mark.parametrize("fail", [False, True])
def test_explicit_work_one_task_result_then_manual_adoption(tmp_path, monkeypatch, fail):
    from app.runtime import RuntimeFoundation
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch, fail=fail)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}"
    payload = {"binding_ref": binding["ref"], "body": "明确交办", "request_id": "work-message", "model_key": "model.writing-entry", "work_ref": work}
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        sent = client.post(root + "/messages", json=payload, headers=headers)
        assert sent.status_code == 202, sent.text
        current = client.get(root + "/discussion/" + binding["ref"], headers=headers).json()
        client.post(root + "/messages", json=payload, headers=headers)
    assert len(calls) == 1
    with db.connect() as con:
        tasks = con.execute("select * from tasks where work_ref=?", (work,)).fetchall()
        usage = con.execute("select * from ai_usage_records where work_ref=?", (work,)).fetchall()
        assert len(tasks) == len(usage) == 1
        assert usage[0]["task_id"] == tasks[0]["task_id"]
    with scope():
        before = RuntimeFoundation(db).get(work)
        assert before["lifecycle_status"] == "ACTIVE"  # Execution is never implicit adoption.
        if fail:
            assert current["attempts"][0]["effect_status"] == "UNKNOWN"
            assert not before["data"].get("acceptanceRefs")
            return
        reply = current["messages"][-1]
        text = reply["body"]
        candidate = command(service, w, b, c, "candidate.recorded", {"binding_ref": binding["ref"],
            "message_ref": reply["message_id"], "reply_start": 0, "reply_end": len(text.encode("utf-16-le")) // 2, "reply_excerpt": text})
        assert candidate["work_ref"] == work
        adopted = command(service, w, b, c, "candidate.adopted", {"candidate_ref": candidate["ref"], "confirmed": True})
        done = RuntimeFoundation(db).get(work)
        assert done["lifecycle_status"] == "COMPLETED"
        assert done["data"]["responsibilityRouting"]["status"] == "COMPLETED"
        assert done["data"]["responsibilityRouting"]["currentExecutorRef"] is None
        assert done["data"]["responsibilityRouting"]["resultRefs"] == done["data"]["resultRefs"]
        assert done["data"]["resultRefs"] == ["task:" + tasks[0]["task_id"]]
        assert done["data"]["acceptanceRefs"] == [adopted["acceptance_ref"]]
        assert RuntimeFoundation(db).get(adopted["acceptance_ref"])["lifecycle_status"] == "CLOSED"
        assert WritingChapterService(db).chapter(COMPANY, w, b, c)["draft"]["sha256"] == adopted["draft"]["sha256"]
    assert len(calls) == 1


def test_explicit_work_task_attach_failure_rolls_back_before_send(tmp_path, monkeypatch):
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    def fail_attach(*args, **kwargs):
        raise RuntimeError("synthetic attach failure")
    monkeypatch.setattr(ResponsibilityRoutingRuntime, "attach_provider_task", fail_attach)
    with scope():
        claim, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"], body="明确交办",
            request_id="attach-failure", model_key="model.writing-entry", work_ref=work)
        assert created
        async def forbidden(_):
            raise AssertionError("Provider cannot run after attachment rollback")
        asyncio.run(entry.conversations.execute(claim, forbidden))
    with db.connect() as con:
        assert con.execute("select count(*) from tasks where work_ref=?", (work,)).fetchone()[0] == 0
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
        assert con.execute("select count(*) from evolution_events where event_type='conversation.execution_bound'").fetchone()[0] == 0
    assert calls == []


def test_explicit_work_claim_failure_rolls_back_attempt_and_work(tmp_path, monkeypatch):
    from app.runtime import RuntimeFoundation
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    original = ResponsibilityRoutingRuntime.begin_employee_execution
    def interrupted(self, *args, **kwargs):
        original(self, *args, **kwargs)
        raise RuntimeError("synthetic claim commit failure")
    monkeypatch.setattr(ResponsibilityRoutingRuntime, "begin_employee_execution", interrupted)
    with scope():
        with pytest.raises(RuntimeError, match="synthetic claim"):
            service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"], body="明确交办",
                request_id="claim-rollback", model_key="model.writing-entry", work_ref=work)
        assert not RuntimeFoundation(db).get(work)["data"]["responsibilityRouting"].get("executions")
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='conversation.attempt.started'").fetchone()[0] == 0
        assert con.execute("select count(*) from tasks where work_ref=?", (work,)).fetchone()[0] == 0
    assert calls == []


def test_explicit_work_stop_before_launch_never_sends(tmp_path, monkeypatch):
    from app.runtime import RuntimeFoundation
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    with scope():
        claim, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"], body="明确交办",
            request_id="stop-before-send", model_key="model.writing-entry", work_ref=work)
        assert created
        ResponsibilityRoutingRuntime(db).cancel_work(work, reason="合成停止反例")
        async def forbidden(_):
            raise AssertionError("Stopped Work must not invoke the provider")
        asyncio.run(entry.conversations.execute(claim, forbidden))
        assert RuntimeFoundation(db).get(work)["data"]["responsibilityRouting"]["status"] == "CANCELLED"
    assert calls == []
    with db.connect() as con:
        assert con.execute("select count(*) from tasks where work_ref=?", (work,)).fetchone()[0] == 0


def assert_consumed_work_request(db, entry, binding, request_id, work):
    with scope():
        original = entry.conversations.read_request(COMPANY, binding["conversation_ref"], request_id)
        assert len(original["attempts"]) == 1
        attempt = original["attempts"][0]
        with db.connect() as con:
            events_before = con.execute("select count(*) from evolution_events").fetchone()[0]
        # Resolution returns server configuration; consumption is checked by the validator.
        grant = entry.models.professional_grant(entry.execution_grant, COMPANY,
            entry.execution_grant["workspace_id"], "model.writing-entry")
        assert grant == entry.execution_grant
        assert entry.models.require_professional_grant(grant, COMPANY,
            grant["workspace_id"], "model.writing-entry", attempt_id=attempt["attempt_id"]) == grant
        for other_attempt in (None, "different-writing-attempt"):
            with pytest.raises(RuntimeScopeError, match="原专业回复授权已使用，请先查询原请求。"):
                entry.models.require_professional_grant(grant, COMPANY,
                    grant["workspace_id"], "model.writing-entry", attempt_id=other_attempt)
        with db.connect() as con:
            assert con.execute("select count(*) from evolution_events").fetchone()[0] == events_before
    assert attempt["execution_selection"]["work_ref"] == work
    assert len([m for m in original["messages"] if m["sender"]["kind"] == "CEO"
                and m["idempotency_key"] == request_id]) == 1
    with db.connect() as con:
        consumed = con.execute("select payload from evolution_events where event_type='conversation.execution_bound' "
            "and json_extract(payload,'$.execution_selection.grant.grant_ref')=?",
            (entry.execution_grant["grant_ref"],)).fetchall()
        assert len(consumed) == 1
        assert json.loads(consumed[0][0])["attempt_id"] == attempt["attempt_id"]
    return original


def test_writing_work_cancelled_before_late_model_result_never_adopts(tmp_path, monkeypatch):
    from app.runtime import RuntimeFoundation
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    original = ModelGatewayAdapter.execute
    stopped = []
    def late_result(self, prompt, **kwargs):
        result = original(self, prompt, **kwargs)  # Controlled HTTP seam, never a real provider.
        ResponsibilityRoutingRuntime(db).cancel_work(work, reason="合成调用已开始，回执到达前停止")
        stopped.append(True)
        return result
    monkeypatch.setattr(ModelGatewayAdapter, "execute", late_result)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    payload = {"binding_ref": binding["ref"], "body": "明确交办", "request_id": "late-result",
               "model_key": "model.writing-entry", "work_ref": work}
    with TestClient(app) as client:
        response = client.post(root + "/messages", headers=headers, json=payload)
        assert response.status_code == 202, response.text
        current = client.get(root + "/discussion/" + binding["ref"], headers=headers).json()
        replay = client.post(root + "/messages", headers=headers, json=payload)
        assert replay.status_code == 404, replay.text
        assert replay.json()["detail"] == "原专业回复授权已使用，请先查询原请求。"
        reread = client.get(root + "/discussion/" + binding["ref"], headers=headers)
        assert reread.status_code == 200, reread.text
        assert reread.json() == current
    original_request = assert_consumed_work_request(db, entry, binding, "late-result", work)
    assert original_request["attempts"][0]["effect_status"] == "UNKNOWN"
    assert stopped == [True] and len(calls) == 1
    assert current["attempts"][0]["effect_status"] == "UNKNOWN"
    assert not [m for m in current["messages"] if m["sender"]["kind"] == "EMPLOYEE"]
    with scope():
        retained = RuntimeFoundation(db).get(work)
        assert retained["data"]["responsibilityRouting"]["status"] == "CANCELLED"
        assert retained["lifecycle_status"] != "COMPLETED"
        assert not retained["data"].get("acceptanceRefs")
        assert service.chapter(COMPANY, w, b, c)["draft"]["text"] == "雨停以后，书桌上的信仍未打开。"
    with db.connect() as con:
        tasks = con.execute("select task_id,status from tasks where work_ref=?", (work,)).fetchall()
        assert len(tasks) == 1 and tasks[0]["status"] == "COMPLETED"
        assert con.execute("select count(*) from ai_usage_records where work_ref=?", (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from evolution_events where event_type in "
                           "('writing.chapter.candidate.recorded','writing.chapter.candidate.adopted')").fetchone()[0] == 0
    with scope():
        with pytest.raises(RuntimeScopeError, match="候选修改缺少已验证员工回复来源"):
            command(service, w, b, c, "candidate.recorded", {
                "binding_ref": binding["ref"], "message_ref": "task:" + tasks[0]["task_id"],
                "reply_start": 0, "reply_end": 2, "reply_excerpt": "第二"}, request="reject-late-candidate")
        with pytest.raises(RuntimeScopeError, match="候选不属于当前章节。"):
            command(service, w, b, c, "candidate.adopted", {
                "candidate_ref": "task:" + tasks[0]["task_id"], "confirmed": True}, request="reject-late-adoption")
        assert service.chapter(COMPANY, w, b, c)["draft"]["text"] == "雨停以后，书桌上的信仍未打开。"
    assert len(calls) == 1
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type in "
            "('writing.chapter.candidate.recorded','writing.chapter.candidate.adopted')").fetchone()[0] == 0
        assert con.execute("select count(*) from tasks where work_ref=?", (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from ai_usage_records where work_ref=?", (work,)).fetchone()[0] == 1


def test_writing_work_concurrent_creation_and_duplicate_dispatch_send_once(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding, concurrent=True)
    entered, release = Event(), Event()
    original = ModelGatewayAdapter.execute
    def paused(self, prompt, **kwargs):
        entered.set()
        assert release.wait(timeout=10), "Bounded synthetic dispatch was not released"
        return original(self, prompt, **kwargs)
    monkeypatch.setattr(ModelGatewayAdapter, "execute", paused)
    url = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}/messages"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    payload = {"binding_ref": binding["ref"], "body": "明确交办", "request_id": "concurrent-dispatch",
               "model_key": "model.writing-entry", "work_ref": work}
    with TestClient(app) as client, ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(client.post, url, headers=headers, json=payload)
        try:
            assert entered.wait(timeout=5), "First request never reached the controlled model seam"
            second = pool.submit(client.post, url, headers=headers, json=payload).result(timeout=5)
            assert second.status_code == 404, second.text
            assert second.json()["detail"] == "原专业回复授权已使用，请先查询原请求。"
            original_request = assert_consumed_work_request(db, entry, binding, "concurrent-dispatch", work)
            assert original_request["attempts"][0]["status"] == "RUNNING"
            assert calls == []  # Second request cannot enter while the first dispatch is held.
        finally:
            release.set()
        response = first.result(timeout=10)
        assert response.status_code == 202, response.text
        reread = client.get(url.rsplit("/", 1)[0] + "/discussion/" + binding["ref"], headers=headers)
        assert reread.status_code == 200, reread.text
    settled = assert_consumed_work_request(db, entry, binding, "concurrent-dispatch", work)
    assert settled["attempts"][0]["attempt_id"] == original_request["attempts"][0]["attempt_id"]
    assert settled["attempts"][0]["effect_status"] == "SETTLED"
    assert reread.json()["attempts"][0]["attempt_id"] == settled["attempts"][0]["attempt_id"]
    assert len([m for m in settled["messages"] if m["sender"]["kind"] == "EMPLOYEE"]) == 1
    assert len(calls) == 1
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1
        assert con.execute("select count(*) from tasks where work_ref=?", (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from ai_usage_records where work_ref=?", (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from evolution_events where event_type='conversation.attempt.started'").fetchone()[0] == 1
        assert con.execute("select count(*) from evolution_events where correlation_id=? and event_type='team.execution_task_bound'", (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE' and parent_id=?", (work,)).fetchone()[0] == 0


@pytest.mark.parametrize("checkpoint", ["after_attach", "after_unknown"])
def test_writing_work_service_rebuild_keeps_unknown_without_redispatch(tmp_path, monkeypatch, checkpoint):
    from app.database import Database
    from app.conversation_service import ConversationService
    from app.runtime import RuntimeFoundation
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch, fail=True)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    request_id = "rebuild-original"
    if checkpoint == "after_attach":
        with scope():
            claim, created = service.prepare_message(COMPANY, w, b, c, binding_ref=binding["ref"], body="明确交办",
                request_id=request_id, model_key="model.writing-entry", work_ref=work)
            assert created
            async def interrupted(task_id):
                with db.connect() as con:
                    assert con.execute("select work_ref from tasks where task_id=?", (task_id,)).fetchone()[0] == work
                    marker = con.execute("select payload from evolution_events where correlation_id=? and event_type='team.execution_task_bound'", (work,)).fetchone()
                    assert json.loads(marker[0])["task_ref"] == task_id
                raise RuntimeError("Synthetic executor acknowledgement lost after attachment")
            asyncio.run(entry.conversations.execute(claim, interrupted))
        assert calls == []
    else:
        url = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}/messages"
        with TestClient(app) as client:
            response = client.post(url, headers={"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}, json={
                "binding_ref": binding["ref"], "body": "明确交办", "request_id": request_id,
                "model_key": "model.writing-entry", "work_ref": work})
            assert response.status_code == 202, response.text
        assert len(calls) == 1
        with db.connect() as con:
            claim = json.loads(con.execute("select payload from evolution_events where event_type='conversation.attempt.started'").fetchone()[0])
    with db.connect() as con:
        tasks_before = [tuple(row) for row in con.execute("select task_id,status,work_ref,execution_ref from tasks where work_ref=?", (work,))]
        assert len(tasks_before) == 1
        events_before = con.execute("select count(*) from evolution_events").fetchone()[0]
        usage_before = con.execute("select count(*) from ai_usage_records where work_ref=?", (work,)).fetchone()[0]
    cold_db = Database(db.path)
    cold = ConversationService(cold_db)
    assert cold.process_id != entry.conversations.process_id
    forbidden_calls = []
    async def forbidden(_):
        forbidden_calls.append(True)
        raise AssertionError("Retained UNKNOWN Task must never be dispatched again")
    with scope():
        readback = cold.read_request(COMPANY, claim["conversation_id"], request_id)
        assert readback["attempts"][0]["status"] == "UNKNOWN"
        assert readback["attempts"][0]["effect_status"] == "UNKNOWN"
        asyncio.run(cold.execute(claim, forbidden))
        asyncio.run(cold.execute(claim, forbidden))
        assert not RuntimeFoundation(cold_db).get(work)["data"].get("acceptanceRefs")
    assert forbidden_calls == []
    assert len(calls) == (0 if checkpoint == "after_attach" else 1)
    with cold_db.connect() as con:
        assert [tuple(row) for row in con.execute("select task_id,status,work_ref,execution_ref from tasks where work_ref=?", (work,))] == tasks_before
        assert con.execute("select count(*) from evolution_events").fetchone()[0] == events_before
        assert con.execute("select count(*) from ai_usage_records where work_ref=?", (work,)).fetchone()[0] == usage_before


def reviewed_work(tmp_path, monkeypatch, *, renew=True):
    from app.writing_chapter_service import CHECKS
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    first = explicit_work(db, app, entry, service, w, b, c, binding)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        response = client.post(root + '/messages', headers=headers, json={
            'binding_ref': binding['ref'], 'body': '明确交办', 'request_id': 'review-first-message',
            'model_key': 'model.writing-entry', 'work_ref': first})
        assert response.status_code == 202, response.text
        reply = client.get(root + '/discussion/' + binding['ref'], headers=headers).json()['messages'][-1]
    with scope():
        candidate = command(service, w, b, c, 'candidate.recorded', {'binding_ref': binding['ref'],
            'message_ref': reply['message_id'], 'reply_start': 0,
            'reply_end': len(reply['body'].encode('utf-16-le')) // 2, 'reply_excerpt': reply['body']})
        adopted = command(service, w, b, c, 'candidate.adopted', {'candidate_ref': candidate['ref'], 'confirmed': True})
        review = command(service, w, b, c, 'inspection.recorded', {'mode': 'AUTHOR_MANUAL',
            'checks': list(CHECKS), 'note': '复盘：保留邮戳线索，缩短开头。'}, request='first-work-review')
        draft = adopted['draft']
        selection = {'draft_ref': draft['ref'], 'sha256': draft['sha256'], 'start': 0, 'end': 2,
            'excerpt': draft['text'][:2], 'anchor': draft['ref'] + ':0:2', 'knowledge': []}
        second_binding = service.bind_discussion(COMPANY, w, b, c, request_id='second-work-binding',
            expected_draft_ref=draft['ref'], data={'selection': selection})
    if renew:
        entry.execution_grant = {**entry.execution_grant, 'grant_ref': 'controlled-explicit-second-grant'}
    source = {'kind': 'writing', 'book_ref': b, 'chapter_ref': c,
              'expected_draft_ref': draft['ref'], 'selection': selection, 'review_ref': review['ref']}
    return db, app, entry, service, calls, w, b, c, first, review, second_binding, source


def test_review_creates_distinct_work_without_call_then_explicit_dispatch(tmp_path, monkeypatch):
    from app.runtime import RuntimeFoundation
    db, app, entry, service, calls, w, b, c, first, review, binding, source = reviewed_work(tmp_path, monkeypatch)
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    assignment = binding['assignment_ref']
    url = f'/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work'
    payload = {'request_id': 'review-second-work', 'problem': '根据复盘调整当前选文',
        'expected_result': '待作者采用的第二次候选', 'model_key': 'model.writing-entry', 'source': source}
    with TestClient(app) as client:
        made = client.post(url, headers=headers, json=payload)
        assert made.status_code == 200, made.text
        second = made.json()['work']['entity_id']
        assert second != first
        replay = client.post(url, headers=headers, json=payload)
        assert replay.status_code == 200 and replay.json()['work']['entity_id'] == second
        assert len(calls) == 1
        with db.connect() as con:
            assert con.execute('select count(*) from tasks where work_ref=?', (second,)).fetchone()[0] == 0
            assert con.execute('select count(*) from ai_usage_records where work_ref=?', (second,)).fetchone()[0] == 0
        sent = client.post(f'/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}/messages',
            headers=headers, json={'binding_ref': binding['ref'], 'body': payload['problem'],
                'request_id': 'review-second-message', 'model_key': 'model.writing-entry', 'work_ref': second})
        assert sent.status_code == 202, sent.text
        assert sent.json()['attempt']['execution_selection']['work_review']['work_ref'] == first
    assert len(calls) == 2
    assert review['note'] in json.dumps(calls[-1], ensure_ascii=False)
    with scope():
        retained = RuntimeFoundation(db).get(second)
        assert retained['lifecycle_status'] == 'ACTIVE'
        assert not retained['data'].get('acceptanceRefs')
    with db.connect() as con:
        tasks = con.execute('select task_id,work_ref from tasks where work_ref in (?,?)', (first, second)).fetchall()
        assert len(tasks) == 2 and len({row['task_id'] for row in tasks}) == 2
        assert con.execute('select count(*) from ai_usage_records where work_ref=?', (second,)).fetchone()[0] == 1


@pytest.mark.parametrize('invalid', ['used_grant', 'no_grant', 'disabled_binding', 'stale_draft', 'foreign_review', 'foreign_chapter', 'unaccepted_work'])
def test_review_work_rejects_changed_basis_or_authorization_without_new_task(tmp_path, monkeypatch, invalid):
    db, app, entry, service, calls, w, b, c, first, review, binding, source = reviewed_work(
        tmp_path, monkeypatch, renew=invalid != 'used_grant')
    if invalid == 'no_grant': entry.execution_grant = None
    elif invalid == 'disabled_binding':
        with db.connect() as con:
            con.execute("update employee_capability_bindings set enabled=0 where capability_type='model'")
    elif invalid == 'stale_draft':
        with scope(): command(service, w, b, c, 'draft.saved', {'text': '复盘后正文已改', 'knowledge': []}, request='after-review-edit')
    elif invalid == 'foreign_review': source = {**source, 'review_ref': 'not-this-chapter-review'}
    elif invalid == 'foreign_chapter': source = {**source, 'chapter_ref': 'not-this-chapter'}
    elif invalid == 'unaccepted_work':
        with db.connect() as con:
            con.execute("update runtime_entities set lifecycle_status='ACTIVE' where entity_id=?", (first,))
    payload = {'request_id': 'rejected-review-work', 'problem': '根据复盘调整当前选文',
        'expected_result': '不应创建', 'model_key': 'model.writing-entry', 'source': source}
    with TestClient(app) as client:
        response = client.post(f"/api/workspace/runtime/foundation/team-operating/assignments/{binding['assignment_ref']}/work",
            headers={'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}, json=payload)
        assert response.status_code in (403, 409, 422), response.text
    assert len(calls) == 1
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1
        assert con.execute('select count(*) from tasks').fetchone()[0] == 1
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 1


def test_review_work_creation_failure_rolls_back_new_work_without_dispatch(tmp_path, monkeypatch):
    from app.runtime.child_work import CanonicalChildWorkRuntime
    db, app, entry, service, calls, w, b, c, first, review, binding, source = reviewed_work(tmp_path, monkeypatch)
    original = CanonicalChildWorkRuntime.create_cycle_work
    def fail_after_create(self, **kwargs):
        original(self, **kwargs)
        raise RuntimeError('Synthetic review Work creation failure')
    monkeypatch.setattr(CanonicalChildWorkRuntime, 'create_cycle_work', fail_after_create)
    with TestClient(app) as client, pytest.raises(RuntimeError, match='Synthetic review Work creation failure'):
        client.post(f"/api/workspace/runtime/foundation/team-operating/assignments/{binding['assignment_ref']}/work",
            headers={'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}, json={
                'request_id': 'review-creation-rollback', 'problem': '根据复盘修改', 'expected_result': '候选',
                'model_key': 'model.writing-entry', 'source': source})
    assert len(calls) == 1
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1
        assert con.execute('select count(*) from tasks').fetchone()[0] == 1
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 1


def test_existing_default_deny_author_can_bind_then_create_work_without_sending(tmp_path, monkeypatch):
    from test_position_authorization import writing_model_position
    from app.model_preferences import TenantModelPreferenceResolver
    from app.workspace_package_runtime import WorkspacePackageRuntime
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, employee_service, employee, key, w = writing_model_position(tmp_path)
    with scope():
        TenantModelPreferenceResolver(db).set_current(key)
        # This normal explicit configuration step does not create or replay a Work.
        employee_service.set_employee_capability_bindings(employee, [{"capability_source": "tenant_private",
            "capability_type": "model", "capability_id": key, "enabled": True}])
        runtime = WorkspacePackageRuntime(db, tmp_path / "package-store")
        b = runtime.create_object(w, "core.domain-object.create", "WritingBook", {"title": "合成作品", "status": "DRAFT"})["object_id"]
        c = runtime.create_object(w, "core.domain-object.create", "WritingChapter", {"title": "合成章节", "bookRef": b, "status": "DRAFT"})["object_id"]
        entry = WritingEntryService(db)
        service = WritingChapterService(db, conversation_service=entry.conversations, entry_service=entry)
        draft = command(service, w, b, c, "draft.saved", {"text": "海边有封信。", "knowledge": []})["draft"]
        selection = {"draft_ref": draft["ref"], "sha256": draft["sha256"], "start": 0, "end": 4,
                     "excerpt": "海边有封", "anchor": draft["ref"] + ":0:4", "knowledge": []}
        binding = service.bind_discussion(COMPANY, w, b, c, request_id="retained-binding",
            expected_draft_ref=draft["ref"], data={"selection": selection})
        assignment = entry.metadata(COMPANY, w)["assignment_ref"]
        ResponsibilityRoutingRuntime(db).publish_workflow(company_id=COMPANY, workspace_id=w,
            scope_type="WORKSPACE", scope_ref=w, workflow_key="normal-author-model",
            assignment_refs=[assignment], default_flow=["WRITING_CHAPTER_AUTHOR"])
        with db.connect() as con:
            assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request:
        replace(original(self, tenant, request), role="ceo"))
    app = create_app(str(db.path))
    payload = {"request_id": "retained-original-request", "problem": "只创建原交办，不启动",
        "expected_result": "待作者采用", "model_key": key, "source": {"kind": "writing", "book_ref": b,
        "chapter_ref": c, "expected_draft_ref": draft["ref"], "selection": binding["selection"]}}
    with TestClient(app) as client:
        response = client.post(f"/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work",
            headers={"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}, json=payload)
        assert response.status_code == 200, response.text
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1
        assert con.execute("select count(*) from tasks").fetchone()[0] == 0
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
        assert con.execute("select count(*) from evolution_events where event_type='company.text_policy.reserved'").fetchone()[0] == 0
