"""Four persisted scripts and strict original basis; all DBs are isolated fixtures."""
import copy
import json
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.database import Database
from app.content_growth_entry_service import ContentGrowthEntryService, ASSETS, FORMATS
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from app.api.content_growth_router import build_content_growth_router
from app.workspace_package_runtime import WorkspacePackageRuntime
from app.runtime import RuntimeScopeError, RuntimeFoundation
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.employee_execution_identity import EmployeeExecutionIdentity
from backend.tests.test_cg_content_entry import setup, data, selected
from backend.tests.test_cg_selected_execution import ready
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO


def install_v02(db, path):
    with scope():
        package=WorkspacePackageRuntime(db,path/'v02-store').install(ASSETS/'content_growth_v02',COMPANY,department_id='cg-dept',business_id='cg-v02-business',business_name='受控四格式候选')
    return package['instance']['workspace_id']


def work():
    return dict(goal='',shots=[],recording_requirements='',output_intent='UNCONFIRMED',output_spec='',source_refs=[],assignment_ref='',recipient_ref='',model_key='')


def draft(format='speech', body=''):
    return {**data(body), 'format':format, 'work':work()}


def create(s,w,values=None,request='create-four'):
    return s.command(COMPANY,w,'','create',request_id=request,data=values or draft())


def save(s,w,row,values,request='save-four'):
    return s.command(COMPANY,w,row['content']['entity_id'],'save',request_id=request,expected_version_ref=row['version']['entity_id'],data=values)


def shot():
    return dict(id='stable-shot-one',title='开场',description='真实脚本输入',camera='',caption='',sound='',duration=12)


def shot_selection(row):
    return dict(version_ref=row['version']['entity_id'],locator='shot',shot_id='stable-shot-one',shot_snapshot=copy.deepcopy(row['version']['data']['work']['shots'][0]))


def fixture(path):
    db,_,oldw=setup(path);w=install_v02(db,path)
    return db,ContentGrowthService(db),w,oldw


def candidate(s,w,row,values=None,selection=None):
    values=values or {**draft(row['version']['data']['format'],'完整脚本候选'), 'work':copy.deepcopy(row['version']['data']['work'])}
    return s.command(COMPANY,w,row['content']['entity_id'],'candidate',request_id='manual-four',expected_version_ref=row['version']['entity_id'],data={**values,'selection':selection or selected(row)})


def test_manual_candidate_feedback_is_separate_version_bound_receipt(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        row=create(s,w,draft('graphic',data()['body']))
        prepared=candidate(s,w,row)
        ref=row['content']['entity_id']; item=prepared['candidates'][0]
        before=(prepared['content'],item['version'])
        request=dict(candidate_ref=item['version']['entity_id'],candidate_version=item['feedback_version'],
            basis_version_ref=row['version']['entity_id'],action='REVISE',reason='请由我手动修改',request_id=str(uuid4()))
        first=s.candidate_feedback(COMPANY,w,ref,**request)
        assert first['action']=='REVISE' and not first['replayed']
        assert s.candidate_feedback(COMPANY,w,ref,**request)['receipt_ref']==first['receipt_ref']
        cold=ContentGrowthService(Database(db.path)).content(COMPANY,w,ref)
        assert cold['candidates'][0]['feedback']['receipt_ref']==first['receipt_ref']
        assert (cold['content'],cold['candidates'][0]['version'])==before
        with pytest.raises(ContentGrowthConflict):s.candidate_feedback(COMPANY,w,ref,**{**request,'action':'REJECT'})
        with pytest.raises(ContentGrowthConflict):s.candidate_feedback(COMPANY,w,ref,**{**request,'request_id':str(uuid4()),'action':'ACCEPT'})
        adopted=adopt(s,w,cold)
        assert adopted['version']['data']['source_candidate_ref']==item['version']['entity_id']
        assert adopted['candidates'][0]['feedback']['action']=='REVISE'
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='cg.candidate.feedback'").fetchone()[0]==1
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0
        assert con.execute('pragma integrity_check').fetchone()[0]=='ok'


def test_manual_feedback_stale_head_foreign_actor_and_race(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        row=create(s,w,draft('graphic',data()['body']))
        prepared=candidate(s,w,row); item=prepared['candidates'][0]
        arguments=dict(candidate_ref=item['version']['entity_id'],candidate_version=item['feedback_version'],
            basis_version_ref=row['version']['entity_id'],reason='已核对候选')
        ref=row['content']['entity_id']
    with scope(ceo_id='other'),pytest.raises(RuntimeScopeError):
        s.candidate_feedback(COMPANY,w,ref,**arguments,action='ACCEPT',request_id=str(uuid4()))
    def decide(action):
        with scope():
            try:
                s.candidate_feedback(COMPANY,w,ref,**arguments,action=action,request_id=str(uuid4()))
                return 'saved'
            except ContentGrowthConflict:return 'conflict'
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(decide,('ACCEPT','REJECT')))==['conflict','saved']
    with scope():
        other=create(s,w,draft('graphic',data()['body']),request='different-content')
        with pytest.raises(RuntimeScopeError):
            s.candidate_feedback(COMPANY,w,other['content']['entity_id'],**arguments,action='ACCEPT',request_id=str(uuid4()))
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='cg.candidate.feedback'").fetchone()[0]==1


def test_manual_feedback_http_strict_validation_and_source_gate(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        row=create(s,w,draft('graphic',data()['body']))
        prepared=candidate(s,w,row)
        item=prepared['candidates'][0]
    app=FastAPI()
    @app.middleware('http')
    async def identity(request:Request,call_next):
        with scope(ceo_id=request.headers.get('X-CEO',CEO)):
            return await call_next(request)
    app.include_router(build_content_growth_router(db,lambda *_:None,service=s))
    url=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}/candidate-feedback'
    payload=dict(candidate_ref=item['version']['entity_id'],candidate_version=item['feedback_version'],
        basis_version_ref=row['version']['entity_id'],action='ACCEPT',reason='评价此候选',request_id=str(uuid4()))
    with TestClient(app) as client:
        assert client.post(url,json={**payload,'reason':' '}).status_code==422
        assert client.post(url,json={**payload,'action':'APPROVE'}).status_code==422
        assert client.post(url,json={**payload,'candidate_version':'wrong'}).status_code==422
        assert client.post(url,json={**payload,'request_id':'wrong'}).status_code==422
        assert client.post(url,json=payload,headers={'X-CEO':'foreign'}).status_code==404
        first=client.post(url,json=payload)
        assert first.status_code==200,first.text
        assert client.post(url,json=payload).json()['receipt_ref']==first.json()['receipt_ref']
        assert client.post(url,json={**payload,'request_id':str(uuid4()),'action':'REJECT'}).status_code==409


def test_manual_feedback_stale_head_rolls_back_without_receipt(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        row=create(s,w,draft('graphic',data()['body']))
        prepared=candidate(s,w,row)
        item=prepared['candidates'][0]
        save(s,w,row,draft('graphic','新的正文版本'))
        with pytest.raises(ContentGrowthConflict):
            s.candidate_feedback(COMPANY,w,row['content']['entity_id'],
                candidate_ref=item['version']['entity_id'],candidate_version=item['feedback_version'],
                basis_version_ref=row['version']['entity_id'],action='REVISE',reason='旧版本',request_id=str(uuid4()))
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='cg.candidate.feedback'").fetchone()[0]==0


def adopt(s,w,row):
    return s.command(COMPANY,w,row['content']['entity_id'],'adopt',request_id='adopt-four',expected_version_ref=row['version']['entity_id'],data={'candidate_ref':row['candidates'][0]['version']['entity_id'],'checks':{'content':True,'references':True,'account':True}})


@pytest.mark.parametrize('format',FORMATS)
def test_empty_create_and_save_cold_versions_no_implicit_activation(tmp_path,format):
    db,s,w,oldw=fixture(tmp_path)
    with scope():
        entry=s.entry
        assert entry.publication(candidate=True,version='0.2.0')['published'] is False
        with pytest.raises(ValueError):entry.publication(version='0.2.0')
        row=create(s,w,draft(format));ref=row['content']['entity_id'];assert row['version']['data']['body']==''
        assert row['version']['data']['work']['output_intent']=='UNCONFIRMED'
        assert create(s,w,draft(format))['content']['entity_id']==ref
        changed=draft(format);changed['work']['goal']='本次真实输入目标'
        saved=save(s,w,row,changed)
        assert len(saved['versions'])==2 and saved['version']['data']['body']==''
        assert s.entry.authoring_scope(COMPANY,oldw)['definition']['version']=='0.1.0'
        cold=ContentGrowthService(Database(db.path)).content(COMPANY,w,ref)
        assert cold['version']==saved['version'] and next(v for v in cold['versions'] if v['entity_id']==row['version']['entity_id'])['data']['work']['goal']==''
    with db.connect() as con:
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0
        assert con.execute('select count(*) from tasks').fetchone()[0]==0
        assert con.execute('pragma integrity_check').fetchone()[0]=='ok'


@pytest.mark.parametrize('field',['title','topic','audience'])
def test_required_real_input_not_relaxed(tmp_path,field):
    _,s,w,_=fixture(tmp_path)
    with scope(),pytest.raises(ValueError):create(s,w,{**draft(),field:''})


def test_shot_snapshot_manual_candidate_adoption_immutable_and_no_media(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        values=draft();values['work']['shots']=[shot()]
        row=create(s,w,values);original=copy.deepcopy(row['version'])
        c=candidate(s,w,row,selection=shot_selection(row))
        adopted=adopt(s,w,c);assert adopted['version']['data']['source_candidate_ref']==c['candidates'][0]['version']['entity_id']
        assert adopted['version']['data']['work']['shots']==[shot()]
        assert adopted['content']['lifecycle_status']=='DRAFT'
        assert not adopted['version']['data'].get('mediaReady')
        again=adopt(s,w,c);assert again['version']['entity_id']==adopted['version']['entity_id']
        assert next(v for v in s.content(COMPANY,w,row['content']['entity_id'])['versions'] if v['entity_id']==original['entity_id'])==original
        assert s.selection(original,shot_selection(row))['shot_snapshot']==shot()
        with pytest.raises(ValueError):s.selection(original,{**shot_selection(row),'shot_snapshot':{**shot(),'duration':13}})
        with pytest.raises(ValueError):s.command(COMPANY,w,'','create',request_id='bad-media',data={**draft(),'mediaReady':True})


@pytest.mark.parametrize('change',['body','title','topic','audience','goal','shots','recording_requirements','output_intent','output_spec'])
def test_every_saved_basis_change_blocks_old_candidate_even_with_checks(tmp_path,change):
    _,s,w,_=fixture(tmp_path)
    with scope():
        values=draft('short_video',data()['body']);values['work']['shots']=[shot()]
        row=create(s,w,values);c=candidate(s,w,row,values={**values,'body':'候选正文'})
        changed=copy.deepcopy(values)
        if change in {'body','title','topic','audience'}:changed[change]+='改变'
        elif change=='shots':changed['work']['shots'][0]['caption']='新的字幕'
        elif change=='output_intent':changed['work'][change]='VIDEO'
        else:changed['work'][change]='新的要求'
        after=save(s,w,row,changed)
        assert after['candidates'][0]['eligible'] is False
        with pytest.raises(ContentGrowthConflict):adopt(s,w,after)
        assert c['candidates'][0]['version']['data']['basis_version_ref']==row['version']['entity_id']


def test_lossless_purposes_same_source_and_source_version_recheck(tmp_path):
    _,s,w,_=fixture(tmp_path)
    with scope():
        source=create(s,w,draft('graphic',data()['body']),request='source')
        scope_info=s.entry.authoring_scope(COMPANY,w)['scope']
        base={'reference_id':source['content']['entity_id'],'workspace_id':w,'kind':'CONTENT_ITEM','locator':''}
        refs=s.resolve_references(scope_info,[{**base,'purpose':p} for p in s.REFERENCE_ADAPTER])
        assert [r['purpose'] for r in refs]==list(s.REFERENCE_ADAPTER) and len(refs)==5
        assert all(r['version_ref']==source['version']['entity_id'] for r in refs)
        values=draft('long_video',data()['body']);values['references']=refs;values['work']['source_refs']=[refs[-1]]
        row=create(s,w,values);c=candidate(s,w,row,{**values,'body':'候选'})
        save(s,w,source,draft('graphic','新来源版本'),request='source-change')
        after=s.content(COMPANY,w,row['content']['entity_id']);assert after['candidates'][0]['eligible'] is False
        with pytest.raises(ContentGrowthConflict):adopt(s,w,after)
        assert c['candidates'][0]['version']['data']['references']==refs
        for bad in [{**base,'purpose':'BACKGROUND'},{**base,'purpose':'CONTEXT','workspace_id':'foreign'},{**base,'purpose':'CONTEXT','kind':'REPORT'}]:
            with pytest.raises((ValueError,RuntimeScopeError)):s.resolve_references(scope_info,[bad])


@pytest.mark.parametrize('identity',[{'tenant_id':'other'},{'company_id':'other'},{'ceo_id':'other'},{'role':'employee'}])
def test_actual_foreign_actor_scope_rejected(tmp_path,identity):
    _,s,w,_=fixture(tmp_path)
    with scope(**identity),pytest.raises(RuntimeScopeError):create(s,w)


def test_cas_and_empty_candidate_utf16_and_format_retarget_denied(tmp_path):
    db,s,w,_=fixture(tmp_path)
    with scope():
        row=create(s,w,draft('speech',data()['body']))
        with pytest.raises(ValueError):candidate(s,w,row,{**draft('speech'),'body':''})
        with pytest.raises(ValueError):s.selection(row['version'],{**selected(row),'end':3})
        with pytest.raises(ValueError):save(s,w,row,draft('long_video','换形态'))
    def change(i):
        with scope():
            try:return save(ContentGrowthService(Database(db.path)),w,row,draft('speech',f'修改{i}'),request=f'concurrent-{i}')
            except ValueError:return None
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(change,[1,2]))
    assert sum(x is not None for x in results)==1
    with scope():assert len(s.content(COMPANY,w,row['content']['entity_id'])['versions'])==2


def execution_fixture(path,monkeypatch,fail=False):
    db,app,entry,legacy,calls,oldw,oldrow,oldbinding,oldpayload=ready(path,monkeypatch,fail)
    w=install_v02(db,path)
    entry.execution_grant={**entry.execution_grant,'workspace_id':w,'grant_ref':'controlled-four-only'}
    with scope():
        f=RuntimeFoundation(db);role=f.create('ROLE_SLOT',company_id=COMPANY,workspace_id=w,data={'name':'脚本责任'})
        employee=f.create('AI_EMPLOYEE',company_id=COMPANY,workspace_id=w,lifecycle_status='AVAILABLE',data={'name':'脚本作者'})
        assignment=ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY,workspace_id=w,scope_type='WORKSPACE',scope_ref=w,role_ref=role['entity_id'],employee_ref=employee['entity_id'],responsibility_key='CONTENT_AUTHOR',responsibility='仅文本脚本建议',output_contract={'requiresResult':False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY,workspace_id=w,runtime_employee_ref=employee['entity_id'],company_employee_ref='cg-employee',employee_capability_binding_ref='cg-model-binding')
        s=ContentGrowthService(db,entry=entry,conversations=app.state.conversation_service) if hasattr(app.state,'conversation_service') else ContentGrowthService(db,entry=entry)
        s.conversations.selection_validator=entry.validate_execution_selection
    return db,app,entry,s,calls,w,assignment


def test_manual_feedback_rechecks_current_assignment_and_model_without_execution(tmp_path,monkeypatch):
    db,_,_,s,calls,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        values=draft('graphic',data()['body'])
        values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values)
        prepared=candidate(s,w,row,values={**values,'body':'人工修改候选'})
        item=prepared['candidates'][0]
        receipt=s.candidate_feedback(COMPANY,w,row['content']['entity_id'],
            candidate_ref=item['version']['entity_id'],candidate_version=item['feedback_version'],
            basis_version_ref=row['version']['entity_id'],action='ACCEPT',reason='人工评价',request_id=str(uuid4()))
        assert receipt['action']=='ACCEPT' and calls==[]
    with db.connect() as con:
        assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0


@pytest.mark.parametrize('fail',[False,True])
def test_actual_http_controlled_executor_single_usage_unknown_no_replay(tmp_path,monkeypatch,fail):
    from fastapi.testclient import TestClient
    db,app,entry,s,calls,w,assignment=execution_fixture(tmp_path,monkeypatch,fail)
    with scope():
        values=draft('short_video',data()['body']);values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values);binding=s.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='bind-four',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
    root=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}'
    payload=dict(binding_ref=binding['binding_ref'],body='仅讨论原脚本',request_id='four-original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row),references=[])
    with TestClient(app) as client:
        headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
        result=client.post(root+'/messages',json=payload,headers=headers);assert result.status_code==202,result.text
        claim=result.json()['attempt'];assert claim['execution_selection']['purpose']=='CG_CONTENT_REPLY'
        assert len(calls)==1
        for _ in range(3):
            query=client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':claim['attempt_id']},headers=headers)
            assert query.status_code==200,query.text
            assert query.json()['attempt']['status']==('UNKNOWN' if fail else 'COMPLETED')
        client.post(root+'/messages',json=payload,headers=headers);assert len(calls)==1
        if fail:
            assert client.post(root+'/messages',json={**payload,'request_id':'new-request'},headers=headers).status_code==409
        else:
            c=client.post(root+'/reply-candidate',json={'binding_ref':binding['binding_ref'],'attempt_id':claim['attempt_id'],'request_id':'four-materialize'},headers=headers)
            assert c.status_code==200,c.text
            assert c.json()['candidates'][0]['version']['data']['provenance']['source_class']=='CONTROLLED_EXECUTOR'
    with db.connect() as con:
        assert con.execute('select count(*) from ai_usage_records where workspace_id=?',(w,)).fetchone()[0]==1
        assert con.execute("select count(*) from evolution_events where event_type='cg.outbound.claimed'").fetchone()[0] == 1
        assert con.execute("select count(*) from tasks where workspace_id=?",(w,)).fetchone()[0] == 1
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK' and workspace_id=?",(w,)).fetchone()[0]==0


def test_changed_assignment_or_model_cannot_be_waived(tmp_path,monkeypatch):
    db,_,_,s,_,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        values=draft('long_video',data()['body']);values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values);c=candidate(s,w,row,{**values,'body':'候选'})
        with db.connect() as con:con.execute("update employee_capability_bindings set enabled=0 where id='cg-model-binding'")
        current=s.content(COMPANY,w,row['content']['entity_id']);assert not current['candidates'][0]['eligible']
        with pytest.raises((ContentGrowthConflict,RuntimeScopeError)):adopt(s,w,current)
        assert c['candidates'][0]['version']['data']['qualification']==row['version']['data']['qualification']


def test_legacy_assignment_and_execution_purpose_do_not_upgrade_implicitly(tmp_path,monkeypatch):
    db,_,entry,s,_,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        values=draft('speech',data()['body']);values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values)
        binding=s.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='finite-bind',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
        claim,_=s.prepare_message(COMPANY,w,row['content']['entity_id'],binding_ref=binding['binding_ref'],body='讨论原脚本',request_id='finite-original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row),references=[])
        with pytest.raises(RuntimeScopeError):entry.validate_execution_selection({**claim['execution_selection'],'purpose':'CG_GRAPHIC_REPLY'},attempt_id=claim['attempt_id'])
        actual=RuntimeFoundation(db).get(assignment['entity_id']);changed={**actual['data'],'responsibilityKey':'CONTENT_GRAPHIC_AUTHOR'}
        with db.connect() as con:con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(changed),assignment['entity_id']))
        with pytest.raises(RuntimeScopeError):create(s,w,values,request='cannot-upgrade-assignment')


def test_http_foreign_scope_no_task_or_usage_and_all_purposes_lossless(tmp_path,monkeypatch):
    from fastapi.testclient import TestClient
    db,app,entry,s,calls,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        source=create(s,w,draft('graphic',data()['body']),request='http-source')
        refs=s.resolve_references(entry.authoring_scope(COMPANY,w)['scope'],[dict(reference_id=source['content']['entity_id'],workspace_id=w,kind='CONTENT_ITEM',purpose=p,locator='') for p in s.REFERENCE_ADAPTER])
        values=draft('long_video',data()['body']);values['references']=refs;values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values);binding=s.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='http-bind',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
    root=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}'
    payload=dict(binding_ref=binding['binding_ref'],body='仅讨论真实原脚本',request_id='http-original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row),references=refs)
    with TestClient(app) as client:
        for headers in [{'X-Tenant-Id':'other','X-Ceo-Id':CEO},{'X-Tenant-Id':'selfuse','X-Ceo-Id':'other-owner'}]:
            denied=client.post(root+'/messages',json=payload,headers=headers);assert denied.status_code in {401,403,404},denied.text
            assert calls==[]
        response=client.post(root+'/messages',json=payload,headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO});assert response.status_code==202,response.text
        claim=response.json()['attempt'];assert [r['purpose'] for r in claim['execution_selection']['references']]==list(s.REFERENCE_ADAPTER)
        assert len(calls)==1
        c=client.post(root+'/reply-candidate',json={'binding_ref':binding['binding_ref'],'attempt_id':claim['attempt_id'],'request_id':'http-candidate'},headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO})
        assert c.status_code==200,c.text
        assert c.json()['candidates'][0]['version']['data']['references']==refs
    with db.connect() as con:
        assert con.execute('select count(*) from tasks where workspace_id=?',(w,)).fetchone()[0]==1
        assert con.execute('select count(*) from ai_usage_records where workspace_id=?',(w,)).fetchone()[0]==1


@pytest.mark.parametrize('locator',['body','shot'])
def test_long_body_forty_shots_small_selection_raw_message_no_whole_history(tmp_path,monkeypatch,locator):
    from fastapi.testclient import TestClient
    from app.conversation_service import digest
    db,app,entry,s,calls,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        empty=draft('long_video');row=create(s,w,empty)
        values=draft('long_video','雨后😀'+('保留完整脚本。'*1400)+'UNSELECTED_BODY_SECRET')
        assert 8000<len(values['body'])<=20000
        values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        values['work']['shots']=[shot()]+[{**shot(),'id':f'unselected-shot-{i}','title':f'UNSELECTED_SHOT_SECRET_{i}','description':'原镜头完整保留。'*200} for i in range(1,40)]
        row=save(s,w,row,values);assert len(row['version']['data']['work']['shots'])==40
        binding=s.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='long-bind',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
        s.conversations.append_ceo(COMPANY,binding['context']['employee_ref'],body='OLD_HISTORY_SECRET',request_id='old-topic',assignment_ref=assignment['entity_id'],references=[],conversation_id=binding['conversation_id'])
        full=dict(version_ref=row['version']['entity_id'],locator='body',start=0,end=len(values['body'].encode('utf-16-le'))//2,excerpt=values['body'])
        with pytest.raises(ValueError,match='更小范围'):s.prepare_message(COMPANY,w,row['content']['entity_id'],binding_ref=binding['binding_ref'],body='整篇范围过大',request_id='too-large',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=full,references=[])
        with db.connect() as con:assert con.execute("select count(*) from evolution_events where event_type='conversation.attempt.started'").fetchone()[0]==0
    payload=dict(binding_ref=binding['binding_ref'],body='只讨论这个已保存选段',request_id='long-original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row) if locator=='body' else shot_selection(row),references=[])
    root=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}'
    with TestClient(app) as client:
        headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
        result=client.post(root+'/messages',json=payload,headers=headers);assert result.status_code==202,result.text
        claim=result.json()['attempt'];assert claim['execution_selection']['basis_sha256']==digest(row['version']['data'])
        state=client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':claim['attempt_id']},headers=headers).json()
        ceo=next(m for m in state['messages'] if m['idempotency_key']=='long-original');assert ceo['body']==payload['body']
        assert state['attempt']['status']=='COMPLETED'
    assert len(calls)==1
    actual=json.dumps(calls[0],ensure_ascii=False)
    assert len(actual.encode('utf-8'))<32000
    for marker in ['OLD_HISTORY_SECRET','UNSELECTED_BODY_SECRET','UNSELECTED_SHOT_SECRET_39','unselected-shot-39']:assert marker not in actual
    assert ('真实脚本输入' in actual) if locator=='shot' else ('😀' in actual)
    with scope():assert s.content(COMPANY,w,row['content']['entity_id'])['version']==row['version']


def test_source_revalidated_before_outbound_after_task_context_assembly(tmp_path,monkeypatch):
    from fastapi.testclient import TestClient
    db,app,entry,s,calls,w,assignment=execution_fixture(tmp_path,monkeypatch)
    with scope():
        source=create(s,w,draft('graphic','真实原来源正文'),request='second-check-source')
        refs=s.resolve_references(entry.authoring_scope(COMPANY,w)['scope'],[dict(reference_id=source['content']['entity_id'],workspace_id=w,kind='CONTENT_ITEM',purpose='EVIDENCE',locator='')])
        values=draft('speech',data()['body']);values['references']=refs;values['work'].update(assignment_ref=assignment['entity_id'],recipient_ref='cg-employee',model_key='model.cg-test')
        row=create(s,w,values);binding=s.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='second-bind',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
    original=entry.validate_execution_selection;checks=[]
    def validate(selection,**kwargs):
        checks.append(selection['basis_version_ref'])
        if len(checks)==3:
            save(s,w,source,draft('graphic','实际来源已在调用前更新'),request='between-checks')
        return original(selection,**kwargs)
    monkeypatch.setattr(entry,'validate_execution_selection',validate)
    root=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}'
    payload=dict(binding_ref=binding['binding_ref'],body='依据原来源讨论',request_id='double-original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row),references=refs)
    with TestClient(app) as client:
        headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
        result=client.post(root+'/messages',json=payload,headers=headers);assert result.status_code==202,result.text
        assert len(checks)>=3 and calls==[]
        claim=result.json()['attempt'];query=client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':claim['attempt_id']},headers=headers)
        assert query.status_code==200
        assert query.json()['attempt']['status']!='COMPLETED'
        client.post(root+'/messages',json=payload,headers=headers);assert calls==[]
    with db.connect() as con:
        assert con.execute('select count(*) from ai_usage_records where workspace_id=?',(w,)).fetchone()[0]==0
        assert con.execute("select count(*) from evolution_events where event_type='cg.outbound.claimed'").fetchone()[0]==0


@pytest.mark.parametrize("payload", ["null", "[]", "{bad", "foreign_body", "foreign_work"])
def test_manual_creator_event_must_match_complete_saved_candidate(tmp_path, payload):
    db, service, workspace, _ = fixture(tmp_path)
    with scope():
        row = create(service, workspace, draft('graphic', data()['body']))
        prepared = candidate(service, workspace, row)
        item = prepared['candidates'][0]
        arguments = dict(candidate_ref=item['version']['entity_id'], candidate_version=item['feedback_version'],
            basis_version_ref=row['version']['entity_id'], action='ACCEPT', reason='已核对', request_id=str(uuid4()))
    with db.connect() as con:
        created = con.execute("select event_id,payload from evolution_events where event_type='cg.candidate.created' and correlation_id=?", (row['content']['entity_id'],)).fetchone()
        raw = created['payload']
        if payload.startswith('foreign'):
            value = json.loads(raw)
            if payload == 'foreign_body': value['request']['data']['body'] = '伪造正文'
            else: value['request']['data']['work']['goal'] = '伪造目标'
            raw = json.dumps(value)
        else: raw = payload
        con.execute('update evolution_events set payload=? where event_id=?', (raw, created['event_id']))
    with scope():
        if payload.startswith('foreign'):
            current = service.content(COMPANY, workspace, row['content']['entity_id'])
            assert current['candidates'][0]['eligible'] is False
        else:
            with pytest.raises(ContentGrowthConflict):
                service.content(COMPANY, workspace, row['content']['entity_id'])
        with pytest.raises((ContentGrowthConflict, RuntimeScopeError, ValueError)):
            service.candidate_feedback(COMPANY, workspace, row['content']['entity_id'], **arguments)
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='cg.candidate.feedback'").fetchone()[0] == 0
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
