"""Existing Shared Task/Gateway/Usage under controlled HTTP, not audio generation."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from fastapi.testclient import TestClient
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.workspace_package_runtime import WorkspacePackageRuntime
from app.music_entry_service import ASSETS
from app.music_media_service import MusicMediaService, OPERATING_ROOT as APPROVED_ROOT
from backend.tests.test_cg_selected_execution import ready as cg_ready
from backend.tests.test_music_canonical_entry import data, basis, lyrics_selection
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO


def ready(path,monkeypatch,fail=False):
    db,app,_,_,calls,_,_,_,_=cg_ready(path,monkeypatch,fail)
    with scope():
        installed=WorkspacePackageRuntime(db,path/'store').install(ASSETS/'music',COMPANY,department_id='cg-dept',business_id='music-business',business_name='内部音乐执行验证')
        w=installed['instance']['workspace_id']
        f=RuntimeFoundation(db);role=f.create('ROLE_SLOT',company_id=COMPANY,workspace_id=w,data={'name':'歌曲作者'})
        employee=f.create('AI_EMPLOYEE',company_id=COMPANY,workspace_id=w,lifecycle_status='AVAILABLE',data={'name':'歌曲作者'})
        assignment=ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY,workspace_id=w,scope_type='WORKSPACE',scope_ref=w,role_ref=role['entity_id'],employee_ref=employee['entity_id'],responsibility_key='MUSIC_SONG_AUTHOR',responsibility='讨论保存歌词与制作依据，只提供文字建议',output_contract={'requiresResult':False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY,workspace_id=w,runtime_employee_ref=employee['entity_id'],company_employee_ref='cg-employee',employee_capability_binding_ref='cg-model-binding')
        service=app.state.music_service;entry=app.state.music_entry_service
        service.media=MusicMediaService(db,root=APPROVED_ROOT);entry.media=service.media
        entry.execution_grant=dict(tenant_id='selfuse',company_id=COMPANY,workspace_id=w,model_key='model.cg-test',grant_ref='controlled-music-single',max_output_tokens=128,max_input_bytes=50000,max_cost_usd=1,price_version='controlled-zero',price_upper_bound_usd_per_input_byte=0,price_upper_bound_usd_per_output_token=0,effective_system_authorization=True,source_class='CONTROLLED_EXECUTOR')
        row=service.command(COMPANY,w,'','create',request_id='song-1',data=data())
        binding=service.bind_discussion(COMPANY,w,row['song']['entity_id'],request_id='discussion-1',expected=basis(row),assignment_ref=assignment['entity_id'])
    payload=dict(binding_ref=binding['binding_ref'],body='讨论此歌词选段，给出文字建议',request_id='original',model_key='model.cg-test',expected=basis(row),selection=lyrics_selection(row),references=[])
    return db,app,entry,service,calls,w,row,binding,payload


@pytest.mark.parametrize('fail',[False,True])
def test_selected_actual_task_usage_unknown_and_query_zero_write(tmp_path,monkeypatch,fail):
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch,fail)
    root=f'/api/workspace/v1/companies/{COMPANY}/music/{w}/songs/{row["song"]["entity_id"]}'
    headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
    with TestClient(app) as client:
        response=client.post(root+'/messages',json=payload,headers=headers);assert response.status_code==202,response.text
        assert len(calls)==1 and calls[0]['max_tokens']==128
        attempt=response.json()['attempt']['attempt_id']
        with db.connect() as con:before=con.execute('select count(*) from evolution_events').fetchone()[0]
        for _ in range(3):
            query=client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':attempt},headers=headers)
            assert query.status_code==200,query.text
            assert query.json()['attempt']['status']==('UNKNOWN' if fail else 'COMPLETED')
        with db.connect() as con:assert con.execute('select count(*) from evolution_events').fetchone()[0]==before
        assert client.post(root+'/messages',json=payload,headers=headers).json()['created'] is False
        assert len(calls)==1
        assert client.post(root+'/messages',json={**payload,'model_key':'other'},headers=headers).status_code==409
        assert client.post(root+'/messages',json={**payload,'allow_execution':True},headers=headers).status_code==422
        if not fail:
            c=client.post(root+'/reply-candidate',json={'binding_ref':binding['binding_ref'],'attempt_id':attempt,'request_id':'candidate'},headers=headers)
            assert c.status_code==200,c.text
            assert c.json()['lyrics']['entity_id']==row['lyrics']['entity_id']
            assert c.json()['candidates'][0]['data']['asset_ref']=='' # text reply is not audio
            assert client.post(root+'/reply-candidate',json={'binding_ref':binding['binding_ref'],'attempt_id':attempt,'request_id':'changed-client-key'},headers=headers).json()['result_ref']==c.json()['result_ref']
    with db.connect() as con:
        usage=con.execute('select * from ai_usage_records where workspace_id=?',(w,)).fetchall();assert len(usage)==1
        assert usage[0]['capability_id']=='model.cg-test' and usage[0]['fallback_from_model'] is None
        assert con.execute("select count(*) from evolution_events where event_type='music.outbound.claimed'").fetchone()[0]==1


def test_workspace_atomic_claim_across_songs_and_independent_scope(tmp_path,monkeypatch):
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch)
    with scope():
        other=service.command(COMPANY,w,'','create',request_id='other-song',data=data())
        second_binding=service.bind_discussion(COMPANY,w,other['song']['entity_id'],request_id='other-discussion',expected=basis(other),assignment_ref=binding['context']['assignment_ref'])
    second={**payload,'binding_ref':second_binding['binding_ref'],'request_id':'other-original','expected':basis(other),'selection':lyrics_selection(other)}
    barrier=Barrier(2);original=service.pending
    def preflight(scope,**kwargs):
        result=original(scope,**kwargs);barrier.wait(timeout=5);return result
    monkeypatch.setattr(service,'pending',preflight)
    def claim(item):
        song,params=item
        with scope():
            try:return service.prepare_message(COMPANY,w,song,**params)
            except (RuntimeScopeError,ValueError):return None
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(claim,[(row['song']['entity_id'],payload),(other['song']['entity_id'],second)]))
    assert sum(r is not None for r in results)==1
    assert not calls
    monkeypatch.setattr(service,'pending',original)
    with scope():
        assert len(service.collection(COMPANY,w)['pending_requests'])==1
        foreign_scope={**entry.authoring_scope(COMPANY,w)['scope'],'workspace_id':'another-scoped-workspace'}
        assert not service.pending(foreign_scope)


def test_no_client_grant_no_task_and_typed_audio_validation(tmp_path,monkeypatch):
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch)
    entry.execution_grant=None
    root=f'/api/workspace/v1/companies/{COMPANY}/music/{w}/songs/{row["song"]["entity_id"]}'
    headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
    with TestClient(app) as client:
        response=client.post(root+'/messages',json=payload,headers=headers);assert response.status_code==404,response.text
        response=client.post(root+'/messages',json={**payload,'selection':{**payload['selection'],'start':True}},headers=headers);assert response.status_code==422
        assert client.post(root+'/commands/candidate',json={'request_id':'bad','expected':basis(row),'data':{'title':'x','suggestion':'x','url':'https://fakeaudio'}},headers=headers).status_code==422
    assert not calls
    with db.connect() as con:assert con.execute('select count(*) from tasks').fetchone()[0]==0


@pytest.mark.parametrize('fail', [False, True])
def test_music_formal_text_work_acceptance_is_not_audio(tmp_path, monkeypatch, fail):
    from backend.tests.test_cg_selected_execution import create_model_work
    db, app, entry, service, calls, w, row, binding, payload = ready(tmp_path, monkeypatch, fail)
    ref = row['song']['entity_id']
    root = f'/api/workspace/v1/companies/{COMPANY}/music/{w}/songs/{ref}'
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    with TestClient(app) as client:
        work = create_model_work(client, db, w, binding['context']['assignment_ref'], payload,
            {'kind': 'music', 'song_ref': ref, 'expected': payload['expected'], 'selection': payload['selection'], 'references': []})
        assert not calls
        request = {**payload, 'work_ref': work}
        response = client.post(root + '/messages', headers=headers, json=request)
        assert response.status_code == 202, response.text
        client.post(root + '/messages', headers=headers, json=request)
        assert len(calls) == 1
        candidate = client.post(root + '/reply-candidate', headers=headers,
            json={'binding_ref': binding['binding_ref'], 'attempt_id': response.json()['attempt']['attempt_id'], 'request_id': 'text-candidate'})
        with scope():
            assert RuntimeFoundation(db).get(work)['lifecycle_status'] == 'ACTIVE'
        if fail:
            assert candidate.status_code != 200
            return
        assert candidate.status_code == 200, candidate.text
        candidate_ref = candidate.json()['result_ref']
        payload = {'request_id': 'accept-text', 'expected': payload['expected'], 'data': {'candidate_ref': candidate_ref, 'confirmed': True}}
        refused = client.post(root + '/commands/accept-text-result', headers=headers, json={**payload, 'data': {**payload['data'], 'confirmed': False}})
        assert refused.status_code != 200
        accepted = client.post(root + '/commands/accept-text-result', headers=headers, json=payload)
        assert accepted.status_code == 200, accepted.text
        assert client.post(root + '/commands/accept-text-result', headers=headers, json=payload).json()['result_ref'] == accepted.json()['result_ref']
        assert accepted.json()['song']['data']['choice_ref'] == ''
        assert accepted.json()['song']['data']['master_ref'] == ''
        assert accepted.json()['lyrics']['entity_id'] == row['lyrics']['entity_id']
        assert accepted.json()['text_work_results'][candidate_ref]['status'] == 'COMPLETED'
        assert client.get(root, headers=headers).json()['text_work_results'][candidate_ref]['status'] == 'COMPLETED'
        assert accepted.json()['candidates'][0]['data']['asset_ref'] == ''
    with scope(), db.connect() as con:
        done = RuntimeFoundation(db).get(work)
        assert done['lifecycle_status'] == done['data']['responsibilityRouting']['status'] == 'COMPLETED'
        assert done['data']['responsibilityRouting']['currentExecutorRef'] is None
        task = con.execute('select * from tasks where work_ref=?', (work,)).fetchall()
        usage = con.execute('select * from ai_usage_records where work_ref=?', (work,)).fetchall()
        assert len(task) == len(usage) == len(done['data']['acceptanceRefs']) == 1
        assert done['data']['resultRefs'] == ['task:' + task[0]['task_id']]
        assert RuntimeFoundation(db).get(done['data']['acceptanceRefs'][0])['lifecycle_status'] == 'CLOSED'
