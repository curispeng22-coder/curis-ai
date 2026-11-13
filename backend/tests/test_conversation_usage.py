"""Real ledger/orchestrator contract tests; controlled HTTP is not cloud acceptance."""
import json
import sqlite3
import urllib.error

import pytest
from fastapi.testclient import TestClient

from app.ai_usage import AIUsageService
from app.database import Database
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter
from app.operating_intelligence import OperatingIntelligence
from backend.tests.test_employee_conversation import setup, scope
from backend.tests.test_v1_general_operating_contract import COMPANY, TENANT, EMPLOYEE, WORKSPACE


def prepared(path, fail=False):
    db, assignment = setup(path)
    calls = []
    def post(url, payload, headers, timeout):
        calls.append(payload)
        if fail:
            raise urllib.error.HTTPError(url, 503, "unavailable", {}, None)
        return {"choices": [{"message": {"content": "我会按当前责任讨论所选资料，不把引用当作已完成。"}}],
                "usage": {"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7}}
    adapter = ModelGatewayAdapter(base_url="https://provider.invalid", api_key="test-only",
        gateway_id="conversation-test", model_name="contract-model", http_post=post)
    with db.connect() as con:
        con.execute("insert into official_models(model_key,provider_id,display_name,supported_models,gateway_ref,status,default_model,type,name) "
            "values ('model.conversation','contract-provider','Contract','[\"contract-model\"]','conversation-test','active','contract-model','model','Contract')")
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
            "values ('binding-conversation',?,?,'official','model','model.conversation')", (TENANT, EMPLOYEE))
    with scope():
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE, employee_capability_binding_ref="binding-conversation")
    return db, assignment, adapter, calls


def test_credential_wait_projection_preserves_original_attempt(tmp_path, monkeypatch):
    from app.conversation_service import ConversationService

    db, assignment, _, calls = prepared(tmp_path / "wait.sqlite")
    clock = [10]
    monkeypatch.setattr("app.conversation_service.monotonic", lambda: clock[0])
    with scope():
        service = ConversationService(db)
        claim, created = service.prepare(COMPANY, EMPLOYEE, body="原请求", request_id="wait",
                                         assignment_ref=assignment)
        assert created
        conversation = claim["conversation_id"]
        with pytest.raises(RuntimeError, match="controlled resolver failure"):
            with service.model_credential_wait(claim["attempt_id"]):
                live = service.read(COMPANY, conversation_id=conversation)["attempts"][-1]
                assert live["status"] == "RUNNING" and live["credential_wait"] == "WAITING"
                clock[0] = 41
                long = service.read_request(COMPANY, conversation)["attempts"][-1]
                assert long["status"] == "RUNNING" and long["credential_wait"] == "LONG_WAIT"
                cold = ConversationService(db).read_request(COMPANY, conversation)["attempts"][-1]
                assert cold["status"] == "UNKNOWN" and "credential_wait" not in cold
                raise RuntimeError("controlled resolver failure")
        reread = service.read(COMPANY, conversation_id=conversation)["attempts"][-1]
        assert reread["attempt_id"] == claim["attempt_id"]
        assert reread["status"] == "RUNNING" and "credential_wait" not in reread
    assert calls == []


@pytest.mark.parametrize("evidence", ["settled", "live", "outbound", "usage", "binding_mismatch", "no_settlement",
                                      "no_finish", "duplicate_finish", "active_task"])
def test_ordinary_pre_outbound_failure_readback(tmp_path, evidence):
    from app.conversation_service import ConversationService
    from app.result_store import ResultStore

    db, assignment, _, calls = prepared(tmp_path / "pre-outbound.sqlite")
    with scope():
        service = ConversationService(db)
        conversation = service.open(COMPANY, EMPLOYEE)["conversation_id"]
        message = service.append_ceo(COMPANY, EMPLOYEE, body="原请求", request_id="pre-outbound",
                                     assignment_ref=assignment)
        attempt_id = "conversation-execution-pre-outbound"
        context = message["context"]
        grant = {"tenant_id": TENANT, "company_id": COMPANY, "workspace_id": WORKSPACE,
                 "model_key": "model.conversation", "policy_revision": "original", "price_version": "price-test",
                 "grant_ref": "company-text-attempt:" + attempt_id}
        selection = {"purpose": "CONVERSATION_REPLY", "scope": {"company_id": COMPANY, "workspace_id": WORKSPACE},
                     "model": {"source": "official", "model_key": "model.conversation"}, "grant": grant,
                     "binding_id": "binding-conversation", "source_class": "EMPLOYEE_BINDING"}
        claim = {"attempt_id": attempt_id, "message_id": message["message_id"], "conversation_id": conversation,
                 "company_id": COMPANY, "employee_ref": EMPLOYEE, "context": context, "status": "RUNNING",
                 "process_id": service.process_id, "retry_no": 0, "execution_selection": selection}
        store = ResultStore(db)
        task = store.create_task("原请求", company_id=COMPANY, workspace_id=WORKSPACE,
                                 scope_type=context["scope_type"], scope_ref=context["scope_ref"],
                                 execution_ref=attempt_id, employee_id=EMPLOYEE, capability_type="model",
                                 capability_source="official", capability_id="model.conversation")
        task_id = task["task_id"]
        if evidence != "active_task":
            store.transition(task_id, "FAILED")
        events = service.events
        events.record(correlation_id=COMPANY, event_type="company.text_policy.reserved",
                      payload={"attempt_id": attempt_id, "grant": grant, "context": context,
                               "message_id": message["message_id"], "amount_micro_cny": 100})
        events.record(correlation_id=conversation, event_type="conversation.attempt.started", payload=claim)
        events.record(correlation_id=task_id, event_type="conversation.execution_bound",
                      payload={**claim, "task_id": task_id, "company_employee_ref": EMPLOYEE,
                               "capability_id": "model.conversation",
                               "binding_id": "different" if evidence == "binding_mismatch" else selection["binding_id"]})
        original = {**claim, "task_ref": task_id, "status": "UNVERIFIED", "effect_status": "UNKNOWN"}
        if evidence != "no_finish":
            events.record(correlation_id=conversation, event_type="conversation.attempt.finished", payload=original)
        if evidence == "duplicate_finish":
            events.record(correlation_id=conversation, event_type="conversation.attempt.finished", payload=original)
        if evidence != "no_settlement":
            events.record(correlation_id=COMPANY, event_type="company.text_policy.settled",
                          payload={"attempt_id": attempt_id, "estimated_micro_cny": 0, "currency": "CNY",
                                   "actual_paid": None, "basis": "NO_EXECUTOR_LAUNCH", "price_version": "price-test"})
        if evidence == "outbound":
            events.record(correlation_id=task_id, event_type="conversation.outbound.claimed",
                          payload={"attempt_id": attempt_id})
        if evidence == "live":
            service.running.add(attempt_id)

        with db.connect() as con:
            if evidence == "usage":
                con.execute(
                    "insert into ai_usage_records(usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,"
                    "model_name,currency,cost_source,employee_id,capability_id,capability_type,task_id,department_id,"
                    "business_id,workspace_id,conversation_ref,canonical_employee_ref,execution_ref,request_id,"
                    "execution_status,metering_status,occurred_at,idempotency_key) "
                    "values('usage-fixture',?,?,'gateway','provider','contract-model','CNY','unknown',?,"
                    "'model.conversation','model',?,'department','business',?,?,?,?,'pre-outbound','failed','unknown',"
                    "'2026-11-08T00:00:00Z','usage-fixture')",
                    (TENANT, COMPANY, EMPLOYEE, task_id, WORKSPACE, conversation, EMPLOYEE, attempt_id))
            before = con.execute("select * from evolution_events order by event_id").fetchall()
            usage_before = con.execute("select * from ai_usage_records").fetchall()
        for view in (service.read(COMPANY, conversation_id=conversation),
                     service.read_request(COMPANY, conversation, request_id="pre-outbound")):
            assert view["messages"] == [message]
            attempt, = view["attempts"]
            assert attempt["attempt_id"] == attempt_id and attempt["message_id"] == message["message_id"]
            if evidence == "settled":
                assert attempt == {**original, "status": "FAILED", "effect_status": "SETTLED",
                                   "recovery_basis": "NO_EXECUTOR_LAUNCH"}
            else:
                assert attempt["status"] == "UNKNOWN"
                assert attempt.get("recovery_basis") != "NO_EXECUTOR_LAUNCH"
        existing, created = service.prepare(COMPANY, EMPLOYEE, body="原请求", request_id="pre-outbound",
                                            assignment_ref=assignment, conversation_id=conversation)
        assert existing == claim and created is False
        with db.connect() as con:
            assert con.execute("select * from evolution_events order by event_id").fetchall() == before
            assert con.execute("select * from ai_usage_records").fetchall() == usage_before
        assert calls == []


@pytest.mark.parametrize("fail", [False, True, "append"])
def test_real_writer_without_work_duplicate_restart_and_reporting(tmp_path, fail, monkeypatch):
    from dataclasses import replace
    from app.identity_membership import IdentityMembership
    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test",
        lambda self, tenant, request: replace(original(self, tenant, request), role="ceo"))
    path = tmp_path / "usage.sqlite"
    db, assignment, adapter, calls = prepared(path, fail is True)
    if fail == "append":
        from app.evolution_event_log import EvolutionEventLog
        record = EvolutionEventLog.record
        def reject_reply(self, **kwargs):
            if kwargs.get("event_type") == "conversation.message" and kwargs.get("payload", {}).get("sender", {}).get("kind") == "EMPLOYEE":
                raise RuntimeError("Injected reply persistence failure")
            return record(self, **kwargs)
        monkeypatch.setattr(EvolutionEventLog, "record", reject_reply)
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    payload = {"body": "只讨论资料，不建立工作", "request_id": "same", "assignment_ref": assignment}
    headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
        state = client.get(prefix, headers=headers).json()
    assert len(calls) == 1
    with scope():
        usage = AIUsageService(db)
        rows = usage.list_records(conversation_ref=state["conversation_id"])
        assert len(rows) == 1
        row = rows[0]
        assert row["source_type"] == "CONVERSATION" and row["source_ref"] == state["conversation_id"]
        assert row["company_id"] == COMPANY and row["canonical_employee_ref"] == EMPLOYEE
        assert row["employee_id"] == EMPLOYEE and row["project_id"] is None and row["work_ref"] is None
        assert row["workspace_id"] == WORKSPACE and row["execution_ref"]
        from app.result_attention import ResultAttention
        from app.conversation_service import ConversationService
        from app.runtime import RuntimeScopeError
        assert ResultAttention(db).unseen_results(COMPANY) == []
        assert ConversationService(db).reference_options(COMPANY, EMPLOYEE, assignment) == []
        with pytest.raises(RuntimeScopeError, match="not a business Result"):
            ResultAttention(db).detail(COMPANY, WORKSPACE, "task:" + row["task_id"])
        assert row["total_tokens"] == (None if fail is True else 7)
        assert row["metering_status"] == ("unknown" if fail is True else "confirmed")
        assert row["cost_amount"] is None and row["cost_source"] == "unknown"
        assert usage.aggregate(group_by="conversation")["groups"][0]["key"] == state["conversation_id"]
        assert usage.aggregate(group_by="work")["totals"]["call_count"] == 1
        assert OperatingIntelligence(db).read(COMPANY)
        from app.business_metrics import BusinessMetricService
        from app.evolution_event_log import EvolutionEventLog
        metrics = BusinessMetricService(db, EvolutionEventLog(db))
        assert metrics.compute(COMPANY, 'usage-test')["estimated_cost"]["value"] is None
        assert metrics.read_period(COMPANY, 'usage-test')["estimated_cost"]["value"] is None
    assert len(state["messages"]) == (1 if fail else 2), state
    assert state["attempts"][0]["status"] == ("UNVERIFIED" if fail == "append" else "FAILED" if fail else "COMPLETED"), state
    db.initialize()
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        assert client.get(prefix, headers=headers).json()["messages"] == state["messages"]
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
    assert len(calls) == 1
    with scope():
        assert AIUsageService(db).get_record(row["usage_record_id"]) == row
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
        assert con.execute("select count(*) from projects").fetchone()[0] == 0
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


@pytest.mark.parametrize("tamper", ["company", "employee", "binding"])
def test_conversation_attribution_scope_rejection(tmp_path, tamper):
    db, assignment, adapter, calls = prepared(tmp_path / "scope.sqlite")
    from app.conversation_service import ConversationService
    import asyncio
    with scope():
        service = ConversationService(db)
        claim, _ = service.prepare(COMPANY, EMPLOYEE, body="test", request_id="test", assignment_ref=assignment)
        async def inspect(task_id):
            with db.connect() as con:
                row = con.execute("select event_id,payload from evolution_events where correlation_id=? and event_type='conversation.execution_bound'", (task_id,)).fetchone()
                event = json.loads(row["payload"])
                event[{"company": "company_id", "employee": "employee_ref", "binding": "binding_id"}[tamper]] = "invalid"
                con.execute("update evolution_events set payload=? where event_id=?", (json.dumps(event), row["event_id"]))
            with pytest.raises(ValueError):
                AIUsageService(db).validate_business_context(tenant_id=TENANT, employee_id=EMPLOYEE,
                    capability_id="model.conversation", capability_type="model", task_id=task_id,
                    capability_binding_id="binding-conversation")
            return {"status": "FAILED"}
        asyncio.run(service.execute(claim, inspect))
    assert not calls
    with db.connect() as con:
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0


def test_migration_preserves_all_rows_indexes_triggers_and_rolls_back(tmp_path, monkeypatch):
    # Current accepted canonical schema is reconstructed from initialized schema by removing ONLY this delta.
    with monkeypatch.context() as historical:
        historical.setattr(Database, "_migrate_execution_scope_usage", staticmethod(lambda connection: None))
        db, _, _, _ = prepared(tmp_path / "template.sqlite")
    with db.connect() as con:
        schema = con.execute("select sql from sqlite_master where name='ai_usage_records'").fetchone()[0]
    assert "conversation_ref" in schema
    import re
    old = schema.replace('conversation_ref text, canonical_employee_ref text,', '')
    old = old.replace(' and conversation_ref is null and canonical_employee_ref is null', '')
    old = re.sub(r"and \(\s*\(work_ref is not null.*?\n        \)",
                 "and work_ref is not null and trim(work_ref) != ''", old, flags=re.S)
    path = tmp_path / "historical.sqlite"
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute(old)
    con.execute("create index custom_usage on ai_usage_records(request_id)")
    con.execute("create trigger immutable_usage before update on ai_usage_records begin select raise(abort,'immutable'); end")
    con.execute("insert into ai_usage_records(usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,model_name,currency,cost_source,employee_id,capability_id,capability_type,task_id,project_id,department_id,request_id,execution_status,metering_status,occurred_at,idempotency_key) "
        "values ('u','t','c','g','p','m','USD','unknown','e','cap','model','task','project','d','r','failed','unknown','2026-09-07','key')")
    before = dict(con.execute("select * from ai_usage_records").fetchone())
    objects = [tuple(r) for r in con.execute("select name,sql from sqlite_master where type in ('index','trigger') order by name")]
    con.commit()
    # Deny the destructive swap to prove the savepoint also restores its temp table.
    def deny_drop(action, arg1, arg2, db_name, trigger):
        return sqlite3.SQLITE_DENY if action == sqlite3.SQLITE_DROP_TABLE and arg1 == 'ai_usage_records' else sqlite3.SQLITE_OK
    con.set_authorizer(deny_drop)
    with pytest.raises(sqlite3.DatabaseError):
        Database._migrate_conversation_usage(con)
    con.set_authorizer(None)
    assert dict(con.execute("select * from ai_usage_records").fetchone()) == before
    assert not con.execute("select 1 from sqlite_master where name='ai_usage_records__conversation'").fetchone()
    Database._migrate_conversation_usage(con)
    assert {k: con.execute("select * from ai_usage_records").fetchone()[k] for k in before} == before
    assert [tuple(r) for r in con.execute("select name,sql from sqlite_master where type in ('index','trigger') order by name")] == objects
    Database._migrate_conversation_usage(con)
    with pytest.raises(sqlite3.IntegrityError):
        con.execute("update ai_usage_records set request_id='other'")
    assert con.execute("pragma integrity_check").fetchone()[0] == "ok"
    con.close()


@pytest.mark.parametrize("tamper", [None, "purpose", "work", "chapter", "binding", "canonical_task", "duplicate_canonical"])
def test_explicit_writing_work_requires_both_origins(tmp_path, monkeypatch, tamper):
    import asyncio
    from backend.tests.test_writing_selected_execution import ready, explicit_work
    from backend.tests.test_writing_chapter_vertical import scope as writing_scope, COMPANY as writing_company
    from app.evolution_event_log import EvolutionEventLog

    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    checked = []
    with writing_scope():
        claim, created = service.prepare_message(writing_company, w, b, c, binding_ref=binding["ref"], body="明确交办",
            request_id="dual-origin-check", model_key="model.writing-entry", work_ref=work)
        assert created
        async def inspect(task_id):
            with db.connect() as con:
                row = con.execute("select event_id,payload from evolution_events where correlation_id=? "
                    "and event_type='conversation.execution_bound'", (task_id,)).fetchone()
                event = json.loads(row["payload"])
                canonical = con.execute("select event_id,payload from evolution_events where correlation_id=? "
                    "and event_type='team.execution_task_bound'", (work,)).fetchone()
                assert canonical is not None
                proof = json.loads(canonical["payload"])
                if tamper == "purpose": event["execution_selection"]["purpose"] = "CONVERSATION_REPLY"
                if tamper == "work": event["execution_selection"]["work_ref"] = "another-work"
                if tamper == "chapter": event["execution_selection"]["scope"]["chapter_ref"] = "another-chapter"
                if tamper == "binding": event["binding_id"] = "another-binding"
                if tamper in {"purpose", "work", "chapter", "binding"}:
                    con.execute("update evolution_events set payload=? where event_id=?", (json.dumps(event), row["event_id"]))
                if tamper == "canonical_task":
                    proof["task_ref"] = "another-task"
                    con.execute("update evolution_events set payload=? where event_id=?", (json.dumps(proof), canonical["event_id"]))
            if tamper == "duplicate_canonical":
                EvolutionEventLog(db).record(correlation_id=work, event_type="team.execution_task_bound",
                    payload=proof, idempotency_key="synthetic-extra-binding-proof")
            def validate():
                return AIUsageService(db).validate_business_context(tenant_id="selfuse", employee_id="writing-entry-employee",
                    capability_id="model.writing-entry", capability_type="model", task_id=task_id,
                    capability_binding_id=claim["execution_selection"]["binding_id"])
            if tamper is None:
                attribution = validate()
                assert attribution["work_ref"] == work
                # Work is the ledger's primary origin; the independently checked conversation proof remains present.
                assert attribution["conversation_ref"] is None
                assert attribution["canonical_employee_ref"] is None
                assert event["conversation_id"] == claim["conversation_id"]
                assert event["employee_ref"] == claim["employee_ref"]
            else:
                with pytest.raises((ValueError, KeyError, PermissionError)):
                    validate()
            checked.append(tamper)
            return {"status": "FAILED"}  # Inspect provenance only; never invoke a transport.
        asyncio.run(entry.conversations.execute(claim, inspect))
    assert checked == [tamper]
    assert calls == []
    with db.connect() as con:
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0


@pytest.mark.parametrize('kind', ['content-growth', 'music'])
@pytest.mark.parametrize('tamper', [None, 'purpose', 'object', 'version', 'selection', 'binding', 'workspace', 'canonical_task'])
def test_business_model_work_requires_exact_dual_origin(tmp_path, monkeypatch, kind, tamper):
    from backend.tests.test_cg_selected_execution import ready as cg_ready, create_model_work
    from backend.tests.test_music_selected_execution import ready as music_ready
    from backend.tests.test_writing_chapter_vertical import scope as business_scope, COMPANY as company, CEO
    ready = cg_ready if kind == 'content-growth' else music_ready
    db, app, entry, service, calls, workspace, row, binding, payload = ready(tmp_path, monkeypatch)
    ref = row['content' if kind == 'content-growth' else 'song']['entity_id']
    source = ({'kind': kind, 'content_ref': ref, 'expected_version_ref': payload['expected_version_ref'],
               'selection': payload['selection'], 'references': payload['references']} if kind == 'content-growth' else
              {'kind': kind, 'song_ref': ref, 'expected': payload['expected'], 'selection': payload['selection'], 'references': []})
    root = f'/api/workspace/v1/companies/{company}/{kind}/{workspace}/' + ('contents/' if kind == 'content-growth' else 'songs/') + ref
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    with TestClient(app) as client:
        work = create_model_work(client, db, workspace, binding['context']['assignment_ref'], payload, source)
        response = client.post(root + '/messages', json={**payload, 'work_ref': work}, headers=headers)
        assert response.status_code == 202, response.text
        assert len(calls) == 1
    with business_scope():
        with db.connect() as con:
            task = dict(con.execute('select * from tasks where work_ref=?', (work,)).fetchone())
            origin = con.execute("select event_id,payload from evolution_events where correlation_id=? and event_type='conversation.execution_bound'", (task['task_id'],)).fetchone()
            event = json.loads(origin['payload'])
            selected = event['execution_selection']
            if tamper == 'purpose': selected['purpose'] = 'CONVERSATION_REPLY'
            if tamper == 'object': selected['content_ref' if kind == 'content-growth' else 'song_ref'] = 'foreign-object'
            if tamper == 'version':
                if kind == 'content-growth': selected['basis_version_ref'] = 'foreign-version'
                else: selected['expected']['lyrics_ref'] = 'foreign-version'
            if tamper == 'selection': selected['selection']['excerpt'] = 'forged-selection'
            if tamper == 'binding': event['binding_id'] = 'foreign-binding'
            if tamper == 'workspace': selected['scope']['workspace_id'] = 'foreign-workspace'
            if tamper:
                con.execute('update evolution_events set payload=? where event_id=?', (json.dumps(event), origin['event_id']))
            if tamper == 'canonical_task':
                proof = con.execute("select event_id,payload from evolution_events where correlation_id=? and event_type='team.execution_task_bound'", (work,)).fetchone()
                value = json.loads(proof['payload']); value['task_ref'] = 'foreign-task'
                con.execute('update evolution_events set payload=? where event_id=?', (json.dumps(value), proof['event_id']))
        def validate():
            return AIUsageService(db).validate_business_context(tenant_id='selfuse', employee_id='cg-employee',
                capability_id='model.cg-test', capability_type='model', task_id=task['task_id'], capability_binding_id='cg-model-binding')
        if tamper:
            with pytest.raises(ValueError): validate()
        else:
            assert validate()['work_ref'] == work
        assert len(calls) == 1


@pytest.mark.parametrize('kind', ['content-growth', 'music'])
@pytest.mark.parametrize('tamper', ['foreign-work', 'origin-version', 'binding', 'terminal'])
def test_business_work_mismatch_stops_before_task_and_provider(tmp_path, monkeypatch, kind, tamper):
    from backend.tests.test_cg_selected_execution import ready as cg_ready, create_model_work
    from backend.tests.test_music_selected_execution import ready as music_ready
    from backend.tests.test_writing_chapter_vertical import scope as business_scope, COMPANY as company, CEO
    from app.runtime import RuntimeFoundation
    db, app, entry, service, calls, workspace, row, binding, payload = (cg_ready if kind == 'content-growth' else music_ready)(tmp_path, monkeypatch)
    ref = row['content' if kind == 'content-growth' else 'song']['entity_id']
    source = ({'kind': kind, 'content_ref': ref, 'expected_version_ref': payload['expected_version_ref'], 'selection': payload['selection'], 'references': payload['references']} if kind == 'content-growth' else
              {'kind': kind, 'song_ref': ref, 'expected': payload['expected'], 'selection': payload['selection'], 'references': []})
    root = f'/api/workspace/v1/companies/{company}/{kind}/{workspace}/' + ('contents/' if kind == 'content-growth' else 'songs/') + ref
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    with TestClient(app) as client:
        work = create_model_work(client, db, workspace, binding['context']['assignment_ref'], payload, source)
        with business_scope(), db.connect() as con:
            original = RuntimeFoundation(db).get(work)
            if tamper == 'terminal':
                con.execute("update runtime_entities set lifecycle_status='COMPLETED' where entity_id=?", (work,))
            elif tamper in {'origin-version', 'binding'}:
                cycle_ref = original['data']['cycleRef']
                cycle = RuntimeFoundation(db).get(cycle_ref)
                contract = cycle['data']['contract']
                if tamper == 'binding': contract['modelBinding']['bindingRef'] = 'foreign-binding'
                elif kind == 'content-growth': contract['modelSource']['version_ref'] = 'foreign-version'
                else: contract['modelSource']['expected']['lyrics_ref'] = 'foreign-version'
                con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(cycle['data']), cycle_ref))
        response = client.post(root + '/messages', json={**payload, 'work_ref': 'foreign-work' if tamper == 'foreign-work' else work}, headers=headers)
        assert response.status_code in {404, 409, 422}, response.text
    assert calls == []
    with db.connect() as con:
        assert con.execute('select count(*) from tasks').fetchone()[0] == 0
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0] == 0


@pytest.mark.parametrize("kind", ["writing", "content-growth", "music"])
def test_ordinary_object_reply_receipt_and_explicit_adoption(tmp_path, monkeypatch, kind):
    from backend.tests.test_cg_selected_execution import ready as cg_ready
    from backend.tests.test_music_selected_execution import ready as music_ready
    from backend.tests.test_writing_chapter_vertical import scope as domain_scope, COMPANY as company, CEO
    from app.conversation_service import ConversationService
    if kind == "writing":
        from backend.tests.test_writing_selected_execution import ready as writing_ready
        db, app, entry, service, calls, workspace, book, object_ref, binding = writing_ready(tmp_path, monkeypatch)
        with domain_scope():
            row = service.chapter(company, workspace, book, object_ref)
        source = {"kind": kind, "book_ref": book, "chapter_ref": object_ref, "expected_draft_ref": row["draft"]["ref"]}
    elif kind == "content-growth":
        db, app, _, service, calls, workspace, row, binding, _ = cg_ready(tmp_path, monkeypatch)
        object_ref = row["content"]["entity_id"]
        source = {"kind": kind, "content_ref": object_ref, "expected_version_ref": row["version"]["entity_id"]}
    else:
        db, app, _, service, calls, workspace, row, binding, _ = music_ready(tmp_path, monkeypatch)
        object_ref = row["song"]["entity_id"]
        from backend.tests.test_music_canonical_entry import basis
        source = {"kind": kind, "song_ref": object_ref, "expected": basis(row)}
    conversation = binding["conversation_ref"] if kind == "writing" else binding["conversation_id"]
    with domain_scope():
        owner = ConversationService(db).owner(company, conversation_id=conversation)
        assignment = owner["discussion_scope"]["assignment_ref"]
    root = f"/api/workspace/v1/companies/{company}/conversations/{conversation}"
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    with TestClient(app) as client:
        sent = client.post(root + "/messages", headers=headers, json={"body": "直接讨论当前工作", "request_id": "ordinary",
            "assignment_ref": assignment, "execution_selection": {"purpose": "CONVERSATION_REPLY", "binding_id": None if kind == "writing" else "cg-model-binding",
                "scope": {"company_id": company, "workspace_id": workspace}, "model": {"source": "official", "model_key": "model.writing-entry" if kind == "writing" else "model.cg-test"}}})
        assert sent.status_code == 202, sent.text
        view = client.get(root, headers=headers).json()
        reply = next(m for m in view["messages"] if m["sender"]["kind"] == "EMPLOYEE")
        payload = {"workspace_id": workspace, "message_ref": reply["message_id"], "source": source}
        wrong = {**payload, "source": {**source, "content_ref" if kind == "content-growth" else "chapter_ref" if kind == "writing" else "song_ref": "other-object"}}
        assert client.post(root + "/receive-result", headers=headers, json=wrong).status_code == 404
        stale_source = {**source}
        if kind == "writing": stale_source["expected_draft_ref"] = "stale"
        elif kind == "content-growth": stale_source["expected_version_ref"] = "stale"
        else: stale_source["expected"] = {**source["expected"], "lyrics_ref": "stale"}
        assert client.post(root + "/receive-result", headers=headers, json={**payload, "source": stale_source}).status_code == 409
        with db.connect() as con:
            con.execute("update tasks set status='FAILED' where task_id=?", (reply["task_ref"],))
        assert client.post(root + "/receive-result", headers=headers, json=payload).status_code == 404
        with db.connect() as con:
            con.execute("update tasks set status='COMPLETED' where task_id=?", (reply["task_ref"],))
        first = client.post(root + "/receive-result", headers=headers, json=payload)
        assert first.status_code == 200, first.text
        assert client.post(root + "/receive-result", headers=headers, json=payload).json() == first.json()
        if kind == "writing":
            chapter_command = f"/api/workspace/v1/companies/{company}/writing/{workspace}/books/{book}/chapters/{object_ref}/commands/candidate.dialogue-recorded"
            duplicate = client.post(chapter_command, headers=headers, json={
                "request_id": "different-client-request",
                "expected_draft_ref": source["expected_draft_ref"],
                "data": {"conversation_ref": conversation, "message_ref": reply["message_id"]},
            })
            assert duplicate.status_code == 200, duplicate.text
            assert duplicate.json()["ref"] == first.json()["candidate_ref"]
        with db.connect() as con:
            binding_id = con.execute("select capability_binding_id from ai_usage_records where task_id=?", (reply["task_ref"],)).fetchone()[0]
            con.execute("update employee_capability_bindings set enabled=0 where id=?", (binding_id,))
        assert client.post(root + "/receive-result", headers=headers, json=payload).status_code in {404, 409}
        with db.connect() as con:
            con.execute("update employee_capability_bindings set enabled=1 where id=?", (binding_id,))
        candidate_ref = first.json()["candidate_ref"]
        with domain_scope():
            if kind == "writing":
                current = service.chapter(company, workspace, book, object_ref)
                assert current["draft"]["ref"] == source["expected_draft_ref"]
                adopted = service.command(company, workspace, book, object_ref, "candidate.adopted", "accept-ordinary",
                    source["expected_draft_ref"], {"candidate_ref": candidate_ref, "confirmed": True})
                assert adopted["draft"]["text"] == reply["body"]
            elif kind == "content-growth":
                current = service.content(company, workspace, object_ref)
                assert current["version"]["entity_id"] == source["expected_version_ref"]
                adopted = service.command(company, workspace, object_ref, "adopt", request_id="accept-ordinary",
                    expected_version_ref=source["expected_version_ref"], data={"candidate_ref": candidate_ref,
                        "checks": {"content": True, "references": True, "account": True}})
                assert adopted["version"]["data"]["body"] == reply["body"]
                adopted_candidate = next(c for c in adopted["candidates"] if c["version"]["entity_id"] == candidate_ref)
                assert not adopted_candidate["eligible"]
                assert adopted_candidate["reasons"] == ["已采用，请查看采用版本。"]
            else:
                current = service.content(company, workspace, object_ref)
                assert current["lyrics"]["entity_id"] == source["expected"]["lyrics_ref"]
                adopted = service.command(company, workspace, object_ref, "adopt-dialogue-lyrics", request_id="accept-ordinary",
                    expected=source["expected"], data={"candidate_ref": candidate_ref, "confirmed": True})
                assert adopted["lyrics"]["data"]["text"] == reply["body"]
                for key in ("production_ref", "master_ref", "choice_ref"):
                    assert adopted["song"]["data"][key] == row["song"]["data"][key]
            with db.connect() as con:
                task = con.execute("select work_ref from tasks where task_id=?", (reply["task_ref"],)).fetchone()
                assert not task[0]
                assert con.execute("select count(*) from ai_usage_records where task_id=?", (reply["task_ref"],)).fetchone()[0] == 1
                assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
        assert len(calls) == 1
