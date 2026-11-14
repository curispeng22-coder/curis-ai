"""T-018: real local runtime and ledger, injected Provider only; no paid calls."""
import asyncio
import json
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient
from app.database import Database
from app.conversation_service import ConversationService
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.writing_chapter_service import WritingChapterService, WritingConflict
from backend.tests.test_writing_selected_execution import ready, explicit_work
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO, command


def fixture(tmp_path, monkeypatch, fail=False):
    values = ready(tmp_path, monkeypatch, fail=fail)
    db, app, entry, service, calls, w, b, c, binding = values
    work = explicit_work(db, app, entry, service, w, b, c, binding)
    return values, work


def send(values, work, request='t018', retry=0):
    db, app, entry, service, calls, w, b, c, binding = values
    root = f'/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}'
    with TestClient(app) as client:
        response = client.post(root + '/messages', headers={'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}, json={
            'binding_ref': binding['ref'], 'body': '明确交办', 'request_id': request,
            'model_key': 'model.writing-entry', 'work_ref': work, 'retry_no': retry})
        assert response.status_code == 202, response.text
        state = client.get(root + '/discussion/' + binding['ref'], headers={'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO})
        assert state.status_code == 200, state.text
        return state.json()


def snapshot(db, workspace, work):
    projection = SharedWorkspaceProjection(db)
    current = RuntimeFoundation(db).get(work)
    row = next(item for item in projection.workspace(COMPANY, workspace)['work_items'] if item['object_ref'] == work)
    employee = projection.employee(COMPANY, workspace, current['data']['responsibilityRouting']['responsibilityHolderRef'])
    return current, row, employee


def latest_execution(work):
    return list(work['data']['responsibilityRouting']['executions'].values())[-1]


def adopt(values, reply, request='t018-adopt'):
    db, _, _, service, _, w, b, c, binding = values
    text = reply['body']
    candidate = command(service, w, b, c, 'candidate.recorded', {'binding_ref': binding['ref'],
        'message_ref': reply['message_id'], 'reply_start': 0,
        'reply_end': len(text.encode('utf-16-le')) // 2, 'reply_excerpt': text}, request='t018-candidate')
    base = service.chapter(COMPANY, w, b, c)['draft']['ref']
    args = (COMPANY, w, b, c, 'candidate.adopted', request, base, {'candidate_ref': candidate['ref'], 'confirmed': True})
    first = service.command(*args)
    assert service.command(*args) == first
    return first


def test_w05_w07_success_is_scoped_and_w06_completion_survives_restart(tmp_path, monkeypatch):
    values, work = fixture(tmp_path, monkeypatch)
    db, _, entry, service, calls, w, b, c, binding = values
    state = send(values, work)
    assert len(calls) == 1
    with scope():
        current, row, employee = snapshot(db, w, work)
        execution = next(iter(current['data']['responsibilityRouting']['executions'].values()))
        assert row['work_status'].upper() == 'ACTIVE' and latest_execution(current)['status'] == execution['status'] == 'ACCEPTED'
        assert row['current_executor_ref'] is None and employee['ui_status']['code'] == 'idle'
        result_ref = execution['resultRef']
        result = SharedWorkspaceProjection(db).result(COMPANY, w, result_ref)
        assert result['source_work_ref'] == work and result['owner_ref'] == 'writing-entry-employee'
        assert result['execution_ref'] == state['attempts'][0]['attempt_id']
        assert result['status'] == 'COMPLETED' and result['verification_status'] == 'VERIFIED'
        reply = next(m for m in state['messages'] if m['sender']['kind'] == 'EMPLOYEE')
        assert reply['sender']['ref'] == execution['employeeRef']
        # Replaying the original execution cannot generate another Task, Result or adoption.
        with db.connect() as con:
            claim = json.loads(con.execute("select payload from evolution_events where event_type='conversation.attempt.started'").fetchone()[0])
            task = con.execute('select * from tasks where work_ref=?', (work,)).fetchone()
            usage = con.execute('select * from ai_usage_records where work_ref=?', (work,)).fetchone()
            assert task['execution_ref'] == usage['execution_ref'] == claim['attempt_id']
            assert task['employee_id'] == usage['employee_id'] == 'writing-entry-employee'
            assert usage['task_id'] == task['task_id'] and usage['execution_status'] == 'success'
        async def forbidden(_): raise AssertionError('duplicate dispatch')
        asyncio.run(entry.conversations.execute(claim, forbidden))
        adopted = adopt(values, reply)
        inspection = command(service, w, b, c, 'inspection.recorded', {'mode': 'AUTHOR_MANUAL',
            'checks': ['continuity', 'language', 'rights'], 'note': 't018 formal replay'})
        formal_args = (COMPANY, w, b, c, 'formal.confirmed', 't018-formal', adopted['draft']['ref'],
            {'inspection_ref': inspection['ref'], 'confirmed': True})
        formal = service.command(*formal_args)
        assert service.command(*formal_args) == formal
        formal_state = service.chapter(COMPANY, w, b, c)
        with pytest.raises((WritingConflict, RuntimeScopeError, ValueError)):
            service.prepare_message(COMPANY, w, b, c, binding_ref=binding['ref'], body='明确交办',
                request_id='t018', model_key='model.writing-entry', work_ref=work, retry_no=1)
        assert service.chapter(COMPANY, w, b, c) == formal_state
        current, row, employee = snapshot(db, w, work)
        assert current['lifecycle_status'] == row['work_status'].upper() == current['data']['responsibilityRouting']['status'] == 'COMPLETED'
        assert row['current_executor_ref'] is None and employee['ui_status']['code'] == 'idle'
        cold = Database(db.path)
        assert snapshot(cold, w, work) == (current, row, employee)
        # Fresh interpreter, same SQLite: persistence proof, no desktop/W-15 claim.
        program = """
import json, sys
from app.database import Database
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext
from app.writing_chapter_service import WritingChapterService
from app.shared_workspace_projection import SharedWorkspaceProjection
path, workspace, work, book, chapter, company, ceo, author = sys.argv[1:]
with TenantContext.scope(tenant_id='selfuse', company_id=company, ceo_id=ceo, role='ceo'):
    db = Database(path)
    print(json.dumps({'work': RuntimeFoundation(db).get(work),
        'draft': WritingChapterService(db).chapter(company, workspace, book, chapter)['draft'],
        'employee_status': SharedWorkspaceProjection(db).employee(company, workspace, author)['ui_status']}))
"""
        process = subprocess.run([sys.executable, '-c', program, str(db.path), w, work, b, c, COMPANY, CEO,
            current['data']['responsibilityRouting']['responsibilityHolderRef']],
            capture_output=True, text=True, timeout=30, check=True)
        readback = json.loads(process.stdout)
        assert readback == {'work': current, 'draft': adopted['draft'], 'employee_status': employee['ui_status']}
        assert WritingChapterService(cold).chapter(COMPANY, w, b, c)['draft'] == adopted['draft']
        asyncio.run(ConversationService(cold).execute(claim, forbidden))
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='writing.chapter.formal.confirmed'").fetchone()[0] == 1
        assert con.execute('select count(*) from tasks where work_ref=?', (work,)).fetchone()[0] == 1
        assert con.execute('select count(*) from ai_usage_records where work_ref=?', (work,)).fetchone()[0] == 1
        assert con.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE' and parent_id=?", (work,)).fetchone()[0] == 1
    assert len(calls) == 1


@pytest.mark.parametrize('company_policy', [False, True])
def test_w05_w06_w14_provider_failure_releases_executor_without_success(tmp_path, monkeypatch, company_policy):
    if company_policy:
        from backend.tests.test_writing_exec_t018_fees import writing_policy
        values = writing_policy(tmp_path, monkeypatch, return_values=True, fail=True)
        db, app, entry, service, _, w, b, c, binding = values
        work = explicit_work(db, app, entry, service, w, b, c, binding)
    else:
        values, work = fixture(tmp_path, monkeypatch, fail=True)
    db, _, entry, service, calls, w, b, c, binding = values
    state = send(values, work)
    assert len(calls) == 1 and state['attempts'][0]['effect_status'] == 'UNKNOWN'
    assert not [m for m in state['messages'] if m['sender']['kind'] == 'EMPLOYEE']
    with scope():
        current, row, employee = snapshot(db, w, work)
        assert row['work_status'].upper() == 'WAITING' and latest_execution(current)['status'] == 'FAILED'
        assert row['current_executor_ref'] is None and employee['ui_status']['code'] == 'blocked'
        assert not current['data'].get('acceptanceRefs') and not current['data']['responsibilityRouting']['resultRefs']
        assert snapshot(Database(db.path), w, work) == (current, row, employee)
        assert service.chapter(COMPANY, w, b, c)['draft']['text'] == '雨停以后，书桌上的信仍未打开。'
        assert entry.metadata(COMPANY, w)['pending'][0]['status'] == 'UNKNOWN'
        if company_policy:
            from app.company_execution_policy import CompanyExecutionPolicy, RESERVE_MICRO_CNY
            assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['reserved_micro_cny'] == RESERVE_MICRO_CNY
        with pytest.raises((WritingConflict, RuntimeScopeError)):
            service.prepare_message(COMPANY, w, b, c, binding_ref=binding['ref'], body='明确交办',
                request_id='t018', model_key='model.writing-entry', work_ref=work, retry_no=1)
    assert len(calls) == 1


@pytest.mark.parametrize('after_attach', [False, True])
def test_w06_cancel_closes_execution_and_list_without_provider(tmp_path, monkeypatch, after_attach):
    values, work = fixture(tmp_path, monkeypatch)
    db, _, entry, service, calls, w, b, c, binding = values
    with scope():
        claim, _ = service.prepare_message(COMPANY, w, b, c, binding_ref=binding['ref'], body='明确交办',
            request_id='cancel', model_key='model.writing-entry', work_ref=work)
        if after_attach:
            # Stop at the actual executor boundary: Task is persisted, Provider not called.
            async def stop(_):
                with TestClient(values[1]) as client:
                    response = client.post(f'/api/workspace/runtime/foundation/team-operating/works/{work}/cancel',
                        headers={'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}, json={'reason': 't018 stop at attachment'})
                    assert response.status_code == 200, response.text
                raise RuntimeError('stopped')
            asyncio.run(entry.conversations.execute(claim, stop))
        else:
            ResponsibilityRoutingRuntime(db).cancel_work(work, reason='t018 stop before attachment')
            async def forbidden(_): raise AssertionError('cancelled work dispatch')
            asyncio.run(entry.conversations.execute(claim, forbidden))
        current, row, employee = snapshot(db, w, work)
        assert row['work_status'].upper() == latest_execution(current)['status'] == 'CANCELLED'
        assert row['current_executor_ref'] is None and employee['ui_status']['code'] == 'idle'
        assert all(e['status'] == 'CANCELLED' for e in current['data']['responsibilityRouting']['executions'].values())
        assert snapshot(Database(db.path), w, work) == (current, row, employee)
        assert not current['data'].get('acceptanceRefs')
        if not after_attach:
            attempt = entry.conversations.read_request(COMPANY, binding['conversation_ref'], 'cancel')['attempts'][0]
            assert attempt['status'] == 'CANCELLED' and attempt['effect_status'] == 'SETTLED'
            assert entry.metadata(COMPANY, w)['pending'] == []
        else:
            with db.connect() as con:
                assert con.execute('select status from tasks where work_ref=?', (work,)).fetchone()[0] == 'CANCELLED'
    assert calls == []


@pytest.mark.parametrize('company_policy', [False, True])
def test_w06_proven_prelaunch_failure_can_retry_same_work_once(tmp_path, monkeypatch, company_policy):
    if company_policy:
        from backend.tests.test_writing_exec_t018_fees import writing_policy
        values = writing_policy(tmp_path, monkeypatch, return_values=True)
        db, app, entry, service, _, w, b, c, binding = values
        work = explicit_work(db, app, entry, service, w, b, c, binding)
    else:
        values, work = fixture(tmp_path, monkeypatch)
    db, _, entry, service, calls, w, b, c, binding = values
    with scope():
        args = dict(binding_ref=binding['ref'], body='明确交办', request_id='safe-retry', model_key='model.writing-entry', work_ref=work)
        claim, _ = service.prepare_message(COMPANY, w, b, c, **args)
        validator = entry.conversations.selection_validator
        def reject(*args, **kwargs): raise WritingConflict('t018 preflight interruption')
        monkeypatch.setattr(entry.conversations, 'selection_validator', reject)
        async def forbidden(_): raise AssertionError('preflight must stop dispatch')
        asyncio.run(entry.conversations.execute(claim, forbidden))
        assert latest_execution(RuntimeFoundation(db).get(work))['status'] == 'FAILED'
        assert calls == []
        monkeypatch.setattr(entry.conversations, 'selection_validator', validator)
        if company_policy:
            from app.company_execution_policy import CompanyExecutionPolicy
            assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['reserved_micro_cny'] == 0
    state = send(values, work, request='safe-retry', retry=1)
    assert len(calls) == 1 and len(state['attempts']) == 2
    with scope():
        current, row, employee = snapshot(db, w, work)
        assert latest_execution(current)['status'] == 'ACCEPTED' and row['current_executor_ref'] is None
        assert len(current['data']['responsibilityRouting']['executions']) == 2
        reply = next(m for m in state['messages'] if m['sender']['kind'] == 'EMPLOYEE')
        adopted = adopt(values, reply)
        before = service.chapter(COMPANY, w, b, c)
        with pytest.raises((ValueError, WritingConflict, RuntimeScopeError)):
            service.prepare_message(COMPANY, w, b, c, **args, retry_no=1)
        assert service.chapter(COMPANY, w, b, c) == before
        assert before['draft'] == adopted['draft']
        if company_policy:
            assert CompanyExecutionPolicy(db).read(COMPANY)['totals']['reserved_micro_cny'] == 0
            with db.connect() as con:
                assert len(CompanyExecutionPolicy(db).rows(con, COMPANY, 'reserved')) == 2
                assert len(CompanyExecutionPolicy(db).rows(con, COMPANY, 'settled')) == 2
    assert len(calls) == 1


@pytest.mark.parametrize('foreign', ['tenant', 'company', 'workspace', 'chapter'])
def test_w07_w14_foreign_result_cannot_be_read_or_adopted(tmp_path, monkeypatch, foreign):
    from app.workspace_package_runtime import WorkspacePackageRuntime
    values, work = fixture(tmp_path, monkeypatch)
    db, _, _, service, calls, w, b, c, binding = values
    state = send(values, work)
    with scope():
        result_ref = next(iter(RuntimeFoundation(db).get(work)['data']['responsibilityRouting']['executions'].values()))['resultRef']
        reply = next(m for m in state['messages'] if m['sender']['kind'] == 'EMPLOYEE')
        candidate = command(service, w, b, c, 'candidate.recorded', {'binding_ref': binding['ref'],
            'message_ref': reply['message_id'], 'reply_start': 0,
            'reply_end': len(reply['body'].encode('utf-16-le')) // 2, 'reply_excerpt': reply['body']})
        other = WorkspacePackageRuntime(db, tmp_path / 'package-store').create_object(w,
            'core.domain-object.create', 'WritingChapter', {'title': '另一文稿', 'bookRef': b, 'status': 'DRAFT'})['object_id']
        command(service, w, b, other, 'draft.saved', {'text': '另一文稿原文', 'knowledge': []}, request='other-draft')
        before = service.chapter(COMPANY, w, b, c)
    identity = {'tenant_id': 'foreign'} if foreign == 'tenant' else {}
    company = 'foreign' if foreign == 'company' else COMPANY
    workspace = 'foreign' if foreign == 'workspace' else w
    chapter = other if foreign == 'chapter' else c
    with scope(**identity):
        if foreign != 'chapter':
            with pytest.raises((RuntimeScopeError, KeyError)):
                SharedWorkspaceProjection(db).result(company, workspace, result_ref)
        with pytest.raises((RuntimeScopeError, WritingConflict, ValueError)):
            service.command(company, workspace, b, chapter, 'candidate.adopted', 'foreign-adoption',
                before['draft']['ref'], {'candidate_ref': candidate['ref'], 'confirmed': True})
    with scope():
        assert service.chapter(COMPANY, w, b, c) == before
        assert service.chapter(COMPANY, w, b, other)['draft']['text'] == '另一文稿原文'
    assert len(calls) == 1


@pytest.mark.parametrize('tamper', ['company', 'workspace', 'binding', 'bridge'])
def test_w06_w14_company_author_projection_requires_scoped_current_identity(tmp_path, monkeypatch, tamper):
    values, work = fixture(tmp_path, monkeypatch)
    db, _, _, _, calls, w, *_ = values
    with scope():
        projection = SharedWorkspaceProjection(db)
        author = RuntimeFoundation(db).get(work)['data']['responsibilityRouting']['responsibilityHolderRef']
        assert projection.employee(COMPANY, w, author)['company_employee_ref'] == 'writing-entry-employee'
        with db.connect() as con:
            if tamper == 'company':
                con.execute('update runtime_entities set company_id=? where entity_id=?', ('foreign', author))
            elif tamper == 'workspace':
                con.execute('update runtime_entities set workspace_id=? where entity_id=?', ('foreign', author))
            elif tamper == 'binding':
                con.execute("update employee_capability_bindings set enabled=0 where employee_id='writing-entry-employee'")
            else:
                row = con.execute('select data_json from runtime_entities where entity_id=?', (author,)).fetchone()
                data = json.loads(row[0]); data['identityBridge']['companyEmployeeRef'] = 'foreign'
                con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(data), author))
        assert not [e for e in projection.employees(COMPANY, w) if e['employee_ref'] == author]
    assert calls == []


def test_w06_unknown_executor_acknowledgement_releases_live_occupancy_but_never_replays(tmp_path, monkeypatch):
    values, work = fixture(tmp_path, monkeypatch)
    db, _, entry, service, calls, w, b, c, binding = values
    with scope():
        claim, _ = service.prepare_message(COMPANY, w, b, c, binding_ref=binding['ref'], body='明确交办',
            request_id='lost-ack', model_key='model.writing-entry', work_ref=work)
        async def interrupted(_): raise RuntimeError('t018 lost executor acknowledgement')
        asyncio.run(entry.conversations.execute(claim, interrupted))
        current, row, employee = snapshot(db, w, work)
        assert row['work_status'] == 'waiting' and row['current_executor_ref'] is None
        assert employee['ui_status']['code'] == 'blocked'
        execution = latest_execution(current)
        assert execution['status'] == 'UNKNOWN' and execution['provenance']['effect_status'] == 'UNKNOWN'
        cold = ConversationService(Database(db.path))
        assert cold.read_request(COMPANY, binding['conversation_ref'], 'lost-ack')['attempts'][0]['effect_status'] == 'UNKNOWN'
        async def forbidden(_): raise AssertionError('uncertain physical attempt cannot replay')
        asyncio.run(cold.execute(claim, forbidden))
        assert snapshot(Database(db.path), w, work) == (current, row, employee)
    assert calls == []


def test_direct_writing_two_works_inherit_formal_and_read_back_after_restart(tmp_path, monkeypatch):
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime

    from backend.tests.test_writing_exec_t018_fees import writing_policy

    db, app, entry, service, calls, workspace, *_ = writing_policy(
        tmp_path, monkeypatch, return_values=True, reservations=2,
    )
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    base = f'/api/workspace/v1/companies/{COMPANY}/writing/{workspace}'
    with scope():
        assignment = entry.metadata(COMPANY, workspace)['assignment_ref']
        ResponsibilityRoutingRuntime(db).publish_workflow(
            company_id=COMPANY, workspace_id=workspace, scope_type='WORKSPACE',
            scope_ref=workspace, workflow_key='direct-writing-test',
            assignment_refs=[assignment], default_flow=['WRITING_CHAPTER_AUTHOR'],
        )
    with TestClient(app) as client:
        def request(method, url, status=200, **kwargs):
            response = client.request(method, url, headers=headers, **kwargs)
            assert response.status_code == status, response.text
            return response.json()

        direct = request('POST', base + '/direct')
        assert request('POST', base + '/direct') == direct
        book, chapter = direct['book_ref'], direct['chapter_ref']
        root = f'{base}/books/{book}/chapters/{chapter}'
        work_url = f'/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work'

        def execute(body, key, continuation=None):
            current = request('GET', root)
            assert current['direct']
            draft = current['draft']
            length = len(draft['text'].encode('utf-16-le')) // 2
            selection = {'draft_ref': draft['ref'], 'sha256': draft['sha256'], 'start': 0, 'end': length,
                         'excerpt': draft['text'], 'anchor': f"{draft['ref']}:0:{length}",
                         'knowledge': draft['knowledge']}
            binding = request('POST', root + '/discussion', json={
                'request_id': key + '-bind', 'expected_draft_ref': draft['ref'],
                'data': {'selection': selection},
            })
            source = {'kind': 'writing', 'book_ref': book, 'chapter_ref': chapter,
                      'expected_draft_ref': draft['ref'], 'selection': selection}
            if continuation is not None:
                source['continuation'] = continuation
            work = request('POST', work_url, json={
                'request_id': key + '-work', 'problem': body, 'expected_result': '完整文稿候选',
                'model_key': 'model.writing-entry', 'source': source,
            })['work']['entity_id']
            payload = {'request_id': key, 'body': body, 'binding_ref': binding['ref'],
                       'model_key': 'model.writing-entry', 'work_ref': work}
            request('POST', root + '/messages', status=202, json=payload)
            discussion = request('GET', root + '/discussion/' + binding['ref'])
            reply = next(item for item in discussion['messages']
                         if item.get('provenance', {}).get('execution_selection', {}).get('work_ref') == work)
            text = reply['body']
            candidate = request('POST', root + '/commands/candidate.recorded', json={
                'request_id': key + '-candidate', 'expected_draft_ref': draft['ref'],
                'data': {'binding_ref': binding['ref'], 'message_ref': reply['message_id'], 'reply_start': 0,
                         'reply_end': len(text.encode('utf-16-le')) // 2, 'reply_excerpt': text},
            })
            return work, candidate, draft

        first, candidate, draft = execute('写一封短信', 'direct-first')
        adopted = request('POST', root + '/commands/candidate.adopted', json={
            'request_id': 'direct-adopt', 'expected_draft_ref': draft['ref'],
            'data': {'candidate_ref': candidate['ref'], 'confirmed': True},
        })
        second, revision, _ = execute('语气更温暖', 'direct-second', {
            'source_ref': adopted['formal_ref'], 'requirements': '语气更温暖',
            'confirmed': True, 'mode': 'REVISE',
        })
        before = request('GET', root)

    assert first != second and len(calls) == 2
    assert adopted['draft']['text'] in json.dumps(calls[-1], ensure_ascii=False)
    with scope():
        cold = Database(db.path)
        chapters = WritingChapterService(cold)
        assert chapters.open_direct(COMPANY, workspace) == direct
        restored = chapters.chapter(COMPANY, workspace, book, chapter)
        assert restored['events'] == before['events']
        assert restored['draft'] == adopted['draft']
        assert [event['ref'] for event in restored['events'] if event['action'] == 'formal.confirmed'] == [adopted['formal_ref']]
        assert any(event['ref'] == revision['ref'] and event['work_ref'] == second for event in restored['events'])
        first_work, _, first_employee = snapshot(cold, workspace, first)
        second_work, _, second_employee = snapshot(cold, workspace, second)
        assert first_work['lifecycle_status'] == 'COMPLETED' and second_work['lifecycle_status'] == 'ACTIVE'
        assert first_employee['ui_status']['code'] == second_employee['ui_status']['code'] == 'idle'
        lineage = latest_execution(second_work)['provenance']['execution_selection']['work_continuation']
        assert lineage['source_ref'] == adopted['formal_ref'] and lineage['parent_work_ref'] == first
