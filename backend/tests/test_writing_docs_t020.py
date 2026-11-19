"""T-020 local fake Provider only; formal manuscript and full cold readback."""
import asyncio
import json
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient
from app.database import Database
from app.conversation_service import ConversationService
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.writing_chapter_service import WritingChapterService, WritingConflict
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO, command, local_chain
from backend.tests.test_writing_chapter_api import app
from backend.tests.test_writing_selected_execution import ready, explicit_work
from backend.tests.test_writing_exec_t018 import send, snapshot


def confirm(service, w, b, c, key):
    check = command(service, w, b, c, 'inspection.recorded', {
        'mode': 'AUTHOR_MANUAL', 'checks': ['continuity', 'language', 'rights'], 'note': key}, request=key+'-check')
    return command(service, w, b, c, 'formal.confirmed', {
        'inspection_ref': check['ref'], 'confirmed': True}, request=key+'-formal')


def test_w09_copy_export_formal_candidates_and_history(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    service = WritingChapterService(db)
    application, _ = app(db)
    root = f'/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}'
    with TestClient(application) as client:
        assert client.get(root+'/manuscript/copy').status_code == 404
        with scope():
            draft, _, formal, _ = local_chain(service, w, b, c)
            text = draft['draft']['text']
            selection = {'draft_ref': draft['draft']['ref'], 'sha256': draft['draft']['sha256'],
                'start': 0, 'end': 4, 'excerpt': '雨停以后', 'anchor': draft['draft']['ref']+':0:4', 'knowledge': []}
            candidate = command(service, w, b, c, 'candidate.manual-recorded',
                {'selection': selection, 'replacement': '候选尚未采用'})
            before = service.chapter(COMPANY, w, b, c)
        state = client.get(root+'/manuscript').json()
        assert state['version']['ref'] == state['current_formal_ref'] == formal['ref']
        assert state['candidates'][0]['ref'] == candidate['ref']
        for endpoint in ('copy', 'export'):
            response = client.get(root+'/manuscript/'+endpoint)
            assert response.status_code == 200 and response.content == text.encode('utf-8')
            assert response.headers['content-type'] == 'text/plain; charset=utf-8'
            assert response.headers['cache-control'] == 'no-store'
            if endpoint == 'export': assert 'manuscript.txt' in response.headers['content-disposition']
            assert client.get(root+'/manuscript/'+endpoint, headers={'X-Test-CEO':'foreign'}).status_code == 404
            assert client.get(root+'/manuscript/'+endpoint, params={'version_ref':candidate['ref']}).status_code == 404
        with scope():
            assert service.chapter(COMPANY, w, b, c) == before
            command(service, w, b, c, 'draft.saved', {'text': '新版正文\n含 emoji 📝', 'knowledge': []}, request='new')
            second = confirm(service, w, b, c, 'second')
        history = client.get(root+'/manuscript', params={'version_ref':formal['ref']}).json()
        assert history['read_only'] is True and history['version']['snapshot']['text'] == text
        assert history['current_formal_ref'] == second['ref']
        assert history['versions'][1]['previous_version_ref'] == formal['ref']
        assert client.get(root+'/manuscript/export', params={'version_ref':formal['ref']}).content == text.encode()
        with scope():
            base = service.chapter(COMPANY, w, b, c)['draft']['ref']
        payload = {'request_id':'reopen', 'expected_draft_ref':base,
            'data':{'version_ref':formal['ref'], 'confirmed':True}}
        response = client.post(root+'/commands/version.reopened', json=payload)
        assert response.status_code == 200, response.text
        assert response.json()['draft']['text'] == text
        assert response.json()['draft']['source_version_ref'] == formal['ref']
        assert client.post(root+'/commands/version.reopened', json=payload).json() == response.json()
        assert client.get(root+'/manuscript/copy').text == '新版正文\n含 emoji 📝'
        assert client.post(root+'/commands/version.reopened', json={**payload,'request_id':'stale'}).status_code == 409
        with scope():
            latest = service.chapter(COMPANY, w, b, c)['draft']['ref']
        assert client.post(root+'/commands/version.reopened', json={**payload,'request_id':'foreign',
            'expected_draft_ref':latest, 'data':{'version_ref':candidate['ref'],'confirmed':True}}).status_code == 404
        assert client.get(root+'/manuscript/copy', params={'version_ref':second['ref']}).content == '新版正文\n含 emoji 📝'.encode()


def capture(db, w, b, c, works):
    service = WritingChapterService(db)
    projection = SharedWorkspaceProjection(db)
    current = [snapshot(db, w, work) for work in works]
    results = [projection.result(COMPANY, w, e['resultRef']) for work, _, _ in current
               for e in work['data']['responsibilityRouting']['executions'].values()]
    with db.connect() as con:
        acceptances = [dict(r) for r in con.execute("select * from runtime_entities where entity_type='ACCEPTANCE' order by entity_id")]
        counts = {table:con.execute('select count(*) from '+table).fetchone()[0]
                  for table in ('tasks','ai_usage_records','evolution_events')}
    return {'works':current, 'results':results, 'acceptances':acceptances,
            'chapter':service.chapter(COMPANY, w, b, c),
            'manuscript':service.manuscript(COMPANY, w, b, c), 'counts':counts}


def test_w12_two_works_full_readback_new_instance_and_process_without_replay(tmp_path, monkeypatch):
    values = ready(tmp_path, monkeypatch)
    db, application, entry, service, calls, w, b, c, binding = values
    works = [explicit_work(db, application, entry, service, w, b, c, binding)]
    formals = []
    for index in range(2):
        if index:
            # Bind and capture the Work with the same bounded fake authorization.
            entry.execution_grant = {**entry.execution_grant, 'grant_ref':'controlled-second-work'}
            with scope():
                draft = service.chapter(COMPANY, w, b, c)['draft']
                selection = {'draft_ref':draft['ref'], 'sha256':draft['sha256'], 'start':0,
                    'end':len(draft['text'].encode('utf-16-le'))//2, 'excerpt':draft['text'],
                    'anchor':draft['ref']+':0:'+str(len(draft['text'].encode('utf-16-le'))//2), 'knowledge':[]}
                binding = service.bind_discussion(COMPANY,w,b,c,request_id='second-binding',
                    expected_draft_ref=draft['ref'],data={'selection':selection})
                assignment = entry.metadata(COMPANY,w)['assignment_ref']
            with TestClient(application) as client:
                response = client.post(f'/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work',
                    headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}, json={
                    'request_id':'second-work','problem':'基于已采用正文续做','expected_result':'新的正文',
                    'model_key':'model.writing-entry','source':{'kind':'writing','book_ref':b,'chapter_ref':c,
                    'expected_draft_ref':draft['ref'],'selection':selection}})
                assert response.status_code == 200, response.text
                works.append(response.json()['work']['entity_id'])
            values = (db,application,entry,service,calls,w,b,c,binding)
        if not index:
            state = send(values, works[index], request='t020-send-0')
        else:
            root = f'/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}'
            headers = {'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
            with TestClient(application) as client:
                response = client.post(root+'/messages',headers=headers,json={
                    'binding_ref':binding['ref'],'body':'基于已采用正文续做','request_id':'t020-send-1',
                    'model_key':'model.writing-entry','work_ref':works[index]})
                assert response.status_code==202, response.text
                state = client.get(root+'/discussion/'+binding['ref'],headers=headers).json()
        reply = next(m for m in reversed(state['messages']) if m['sender']['kind']=='EMPLOYEE')
        with scope():
            candidate = command(service,w,b,c,'candidate.recorded',{'binding_ref':binding['ref'],
                'message_ref':reply['message_id'],'reply_start':0,
                'reply_end':len(reply['body'].encode('utf-16-le'))//2,'reply_excerpt':reply['body']},request=f'candidate-{index}')
            command(service,w,b,c,'candidate.adopted',{'candidate_ref':candidate['ref'],'confirmed':True},request=f'adopt-{index}')
            formals.append(confirm(service,w,b,c,f'formal-{index}'))
    assert len(calls)==2 and len(set(works))==2
    with scope():
        expected = json.loads(json.dumps(capture(db,w,b,c,works)))
        assert len(expected['results'])==len(expected['acceptances'])==2
        assert expected['works'][1][0]['data']['writingBasis']['draft_ref']==formals[0]['snapshot']['ref']
        adoptions = [e for e in expected['chapter']['events'] if e['action']=='candidate.adopted']
        assert len(adoptions)==2
        assert {a['work_ref'] for a in adoptions}==set(works)
        assert {a['acceptance_ref'] for a in adoptions}=={a['entity_id'] for a in expected['acceptances']}
        assert len(expected['manuscript']['versions'])==2
        assert expected['manuscript']['versions'][1]['previous_version_ref']==formals[0]['ref']
        assert all(work['lifecycle_status']=='COMPLETED' and employee['ui_status']['code']=='idle'
                   for work, row, employee in expected['works'])
        cold = Database(db.path)
        assert json.loads(json.dumps(capture(cold,w,b,c,works)))==expected
        with db.connect() as con:
            claims = [json.loads(r[0]) for r in con.execute("select payload from evolution_events where event_type='conversation.attempt.started' order by event_id")]
        assert len(claims)==2
        async def forbidden(_): raise AssertionError('completed execution replayed')
        for claim in claims: asyncio.run(ConversationService(cold).execute(claim,forbidden))
        assert json.loads(json.dumps(capture(cold,w,b,c,works)))==expected
    program = '''
import asyncio, json, sys
from backend.tests.test_writing_docs_t020 import capture, scope
from app.database import Database
from app.conversation_service import ConversationService
path,w,b,c,works,claims=sys.argv[1:]
db=Database(path)
async def forbidden(_): raise AssertionError('cold process dispatched Provider')
with scope():
    for claim in json.loads(claims): asyncio.run(ConversationService(db).execute(claim,forbidden))
    print(json.dumps(capture(db,w,b,c,json.loads(works))))
'''
    process = subprocess.run([sys.executable,'-c',program,str(db.path),w,b,c,json.dumps(works),json.dumps(claims)],
        capture_output=True,text=True,timeout=30,check=True)
    assert json.loads(process.stdout)==expected
    assert len(calls)==2


@pytest.mark.parametrize("foreign", ["tenant", "company", "workspace", "chapter"])
def test_w09_manuscript_scope_does_not_leak(tmp_path, foreign):
    db, runtime, w, b, c = setup(tmp_path)
    service = WritingChapterService(db)
    with scope():
        _, _, formal, _ = local_chain(service, w, b, c)
        other = runtime.create_object(w, "core.domain-object.create", "WritingChapter",
            {"title":"独立文稿", "bookRef":b, "status":"DRAFT"})["object_id"]
    with scope(**({"tenant_id":"foreign"} if foreign=="tenant" else {})):
        args = ("foreign" if foreign=="company" else COMPANY,
                "foreign" if foreign=="workspace" else w, b,
                other if foreign=="chapter" else c)
        with pytest.raises(RuntimeScopeError):
            service.manuscript_text(*args, formal["ref"])
