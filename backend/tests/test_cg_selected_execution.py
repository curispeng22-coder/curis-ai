"""Actual shared Task/Usage under injected HTTP, with durable workspace claim lock."""
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from dataclasses import replace
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter
from app.identity_membership import IdentityMembership
from app.content_growth_service import ContentGrowthService
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.conversation_service import ConversationService
from backend.tests.test_cg_content_entry import setup, data, selected
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO


def ready(path,monkeypatch,fail=False):
    db,_,w=setup(path)
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) values ('cg-employee','selfuse',?,'cg-dept','et_product_manager','图文作者','内容制作','idle')",(COMPANY,))
        con.execute("insert into official_models(model_key,provider_id,display_name,supported_models,gateway_ref,status,default_model,type,name) values ('model.cg-test','controlled-provider','受控模型','[\"contract-model\"]','cg-test-gateway','active','contract-model','model','Controlled')")
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('cg-model-binding','selfuse','cg-employee','official','model','model.cg-test')")
    calls=[]
    def post(url,payload,headers,timeout):
        calls.append(payload)
        if fail:raise RuntimeError('controlled outbound uncertain')
        return {'choices':[{'message':{'content':'雨后，书桌上的信仍未打开。灯光映出陌生的邮戳。'}}], 'usage':{'prompt_tokens':8,'completion_tokens':7,'total_tokens':15}}
    adapter=ModelGatewayAdapter(base_url='https://provider.invalid',api_key='test-only',gateway_id='cg-test-gateway',model_name='contract-model',http_post=post)
    original=IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership,'_authorize_test',lambda self,tenant,request:replace(original(self,tenant,request),role='ceo'))
    app=create_app(str(db.path),model_gateway_adapter=adapter);entry=app.state.content_growth_entry_service
    entry.execution_grant=dict(tenant_id='selfuse',company_id=COMPANY,workspace_id=w,model_key='model.cg-test',grant_ref='controlled-cg-single',max_output_tokens=128,max_input_bytes=50000,max_cost_usd=1,price_version='controlled-zero',price_upper_bound_usd_per_input_byte=0,price_upper_bound_usd_per_output_token=0,effective_system_authorization=True,source_class='CONTROLLED_EXECUTOR')
    with scope():
        f=RuntimeFoundation(db);role=f.create('ROLE_SLOT',company_id=COMPANY,workspace_id=w,data={'name':'图文作者'})
        employee=f.create('AI_EMPLOYEE',company_id=COMPANY,workspace_id=w,lifecycle_status='AVAILABLE',data={'name':'图文作者'})
        assignment=ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY,workspace_id=w,scope_type='WORKSPACE',scope_ref=w,role_ref=role['entity_id'],employee_ref=employee['entity_id'],responsibility_key='CONTENT_GRAPHIC_AUTHOR',responsibility='只讨论图文正文',output_contract={'requiresResult':False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY,workspace_id=w,runtime_employee_ref=employee['entity_id'],company_employee_ref='cg-employee',employee_capability_binding_ref='cg-model-binding')
        service=ContentGrowthService(db,entry=entry)
        service.conversations.selection_validator=entry.validate_execution_selection
        row=service.command(COMPANY,w,'','create',request_id='content-1',data=data())
        binding=service.bind_discussion(COMPANY,w,row['content']['entity_id'],request_id='discussion-1',expected_version_ref=row['version']['entity_id'],assignment_ref=assignment['entity_id'])
    payload=dict(binding_ref=binding['binding_ref'],body='讨论选段，给出完整候选正文',request_id='original',model_key='model.cg-test',expected_version_ref=row['version']['entity_id'],selection=selected(row),references=[])
    return db,app,entry,service,calls,w,row,binding,payload


@pytest.mark.parametrize('fail',[False,True])
def test_selected_shared_actual_usage_and_query_no_replay(tmp_path,monkeypatch,fail):
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch,fail)
    root=f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{row["content"]["entity_id"]}'
    headers={'X-Tenant-Id':'selfuse','X-Ceo-Id':CEO}
    with TestClient(app) as client:
        response=client.post(root+'/messages',json=payload,headers=headers);assert response.status_code==202,response.text
        assert len(calls)==1,response.text
        assert calls[0]['max_tokens']==128
        with db.connect() as con:before=con.execute('select count(*) from evolution_events').fetchone()[0]
        attempt=response.json()['attempt']['attempt_id']
        query=client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':attempt},headers=headers)
        assert query.status_code==200,query.text
        state=query.json();assert state['attempt']['status']==('UNKNOWN' if fail else 'COMPLETED'),state
        for _ in range(3):client.get(root+'/discussion/'+binding['binding_ref'],params={'attempt_id':attempt},headers=headers)
        with db.connect() as con:assert con.execute('select count(*) from evolution_events').fetchone()[0]==before
        client.post(root+'/messages',json=payload,headers=headers);assert len(calls)==1
        assert client.post(root+'/messages',json={**payload,'model_key':'other'},headers=headers).status_code==409
        assert client.post(root+'/messages',json={**payload,'allow_execution':True},headers=headers).status_code==422
        if not fail:
            candidate=client.post(root+'/reply-candidate',json={'binding_ref':binding['binding_ref'],'attempt_id':attempt,'request_id':'candidate'},headers=headers)
            assert candidate.status_code==200,candidate.text
            item=candidate.json();assert item['content']['current_version_id']==row['version']['entity_id']
            assert item['candidates'][0]['version']['data']['provenance']['source_class']=='CONTROLLED_EXECUTOR'
    with db.connect() as con:
        usage=con.execute('select * from ai_usage_records where workspace_id=?',(w,)).fetchall();assert len(usage)==1
        assert usage[0]['capability_id']=='model.cg-test' and usage[0]['fallback_from_model'] is None
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0]==0
        assert con.execute("select count(*) from evolution_events where event_type='cg.outbound.claimed'").fetchone()[0]==1


def test_two_conversations_concurrent_atomic_workspace_lock(tmp_path,monkeypatch):
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch)
    with scope():
        other=service.command(COMPANY,w,'','create',request_id='content-2',data=data('雨后😀，另一篇内容。'))
        with db.connect() as con:
            con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) values ('cg-second-employee','selfuse',?,'cg-dept','et_product_manager','第二图文作者','内容制作','idle')",(COMPANY,))
            con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('cg-second-model-binding','selfuse','cg-second-employee','official','model','model.cg-test')")
        f=RuntimeFoundation(db);role2=f.create('ROLE_SLOT',company_id=COMPANY,workspace_id=w,data={'name':'第二图文责任'})
        employee2=f.create('AI_EMPLOYEE',company_id=COMPANY,workspace_id=w,lifecycle_status='AVAILABLE',data={'name':'第二图文作者'})
        assignment2=ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY,workspace_id=w,scope_type='WORKSPACE',scope_ref=w,role_ref=role2['entity_id'],employee_ref=employee2['entity_id'],responsibility_key='CONTENT_GRAPHIC_AUTHOR',responsibility='第二内容建议',output_contract={'requiresResult':False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY,workspace_id=w,runtime_employee_ref=employee2['entity_id'],company_employee_ref='cg-second-employee',employee_capability_binding_ref='cg-second-model-binding')
        bound=service.bind_discussion(COMPANY,w,other['content']['entity_id'],request_id='discussion-2',expected_version_ref=other['version']['entity_id'],assignment_ref=assignment2['entity_id'])
    second={**payload,'binding_ref':bound['binding_ref'],'request_id':'other-original','expected_version_ref':other['version']['entity_id'],'selection':selected(other)}
    barrier=Barrier(2)
    original_collection=service.collection
    def synchronized(c,w):
        result=original_collection(c,w)
        barrier.wait(timeout=5)
        result['pending_requests']=[] # Deliberately let both callers pass the preflight window.
        return result
    monkeypatch.setattr(service,'collection',synchronized)
    def prepare(pair):
        item,values=pair
        with scope():
            try:return service.prepare_message(COMPANY,w,item['content']['entity_id'],**values)[0]
            except RuntimeScopeError as error:return str(error)
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(prepare,[(row,payload),(other,second)]))
    assert sum(isinstance(r,dict) for r in results)==1,results
    assert calls==[]
    with db.connect() as con:assert con.execute("select count(*) from evolution_events where event_type='conversation.attempt.started'").fetchone()[0]==1
    winner=next(r for r in results if isinstance(r,dict));monkeypatch.setattr(service,'collection',original_collection)
    # Cold projection marks a persisted unfinished claim UNKNOWN without writes.
    cold=ContentGrowthService(db,entry=entry,conversations=ConversationService(db));cold.conversations.selection_validator=entry.validate_execution_selection
    with scope():
        query=cold.query_request(COMPANY,w,winner['execution_selection']['content_ref'],binding['binding_ref'] if winner['conversation_id']==binding['conversation_id'] else bound['binding_ref'],attempt_id=winner['attempt_id'])
        assert query['attempt']['status']=='UNKNOWN'
        loser=(other,second) if winner['conversation_id']==binding['conversation_id'] else (row,payload)
        with pytest.raises(ValueError):cold.prepare_message(COMPANY,w,loser[0]['content']['entity_id'],**loser[1])
        assert cold.conversations.read_request(COMPANY,winner['conversation_id'])['messages']
    assert calls==[]


def test_independent_workspace_not_mislocked(tmp_path,monkeypatch):
    from app.workspace_package_runtime import WorkspacePackageRuntime
    from app.content_growth_entry_service import ContentGrowthEntryService,ASSETS
    db,app,entry,service,calls,w,row,binding,payload=ready(tmp_path,monkeypatch)
    with scope():
        first,_=service.prepare_message(COMPANY,w,row['content']['entity_id'],**payload)
        runtime=WorkspacePackageRuntime(db,tmp_path/'second-store')
        from app.workspace_package_runtime import validate_package
        from pathlib import Path
        package=validate_package(ASSETS/'content_growth');otherw='cg-independent-workspace'
        target=Path(runtime.get_workspace(w)['package']['stored_path'])
        with db.connect() as con:
            con.execute('begin immediate')
            runtime.install_confirmed_in_connection(con,package,target,COMPANY,department_id='cg-dept',business_id='cg-business-2',
                business_name='独立业务',business_goal='独立图文',business_positioning='内部测试',workspace_id=otherw,workspace_name='独立内容空间')
        assert otherw != w
        f=RuntimeFoundation(db);role=f.create('ROLE_SLOT',company_id=COMPANY,workspace_id=otherw,data={'name':'独立作者'})
        employee=f.create('AI_EMPLOYEE',company_id=COMPANY,workspace_id=otherw,lifecycle_status='AVAILABLE',data={'name':'独立作者'})
        assignment=ResponsibilityRoutingRuntime(db).create_assignment(company_id=COMPANY,workspace_id=otherw,scope_type='WORKSPACE',scope_ref=otherw,role_ref=role['entity_id'],employee_ref=employee['entity_id'],responsibility_key='CONTENT_GRAPHIC_AUTHOR',responsibility='独立工作空间内容',output_contract={'requiresResult':False})
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY,workspace_id=otherw,runtime_employee_ref=employee['entity_id'],company_employee_ref='cg-employee',employee_capability_binding_ref='cg-model-binding')
        otherentry=ContentGrowthEntryService(db,execution_grant={**entry.execution_grant,'workspace_id':otherw,'grant_ref':'independent-single'})
        other=ContentGrowthService(db,entry=otherentry);other.conversations.selection_validator=otherentry.validate_execution_selection
        content=other.command(COMPANY,otherw,'','create',request_id='independent-content',data=data())
        bound=other.bind_discussion(COMPANY,otherw,content['content']['entity_id'],request_id='independent-bind',expected_version_ref=content['version']['entity_id'],assignment_ref=assignment['entity_id'])
        second,created=other.prepare_message(COMPANY,otherw,content['content']['entity_id'],**{**payload,'binding_ref':bound['binding_ref'],'request_id':'independent-request','expected_version_ref':content['version']['entity_id'],'selection':selected(content)})
        assert created and second['attempt_id'] != first['attempt_id']
    assert calls==[]
    with db.connect() as con:assert con.execute("select count(*) from evolution_events where event_type='conversation.attempt.started'").fetchone()[0]==2


def create_model_work(client, db, workspace, assignment, payload, source):
    with scope():
        ResponsibilityRoutingRuntime(db).publish_workflow(company_id=COMPANY, workspace_id=workspace,
            scope_type='WORKSPACE', scope_ref=workspace, workflow_key='selected-model-work',
            assignment_refs=[assignment], default_flow=[RuntimeFoundation(db).get(assignment)['data']['responsibilityKey']])
    body = {'request_id': 'explicit-work', 'problem': payload['body'], 'expected_result': 'explicitly accepted text result',
            'model_key': payload['model_key'], 'source': source}
    url = f'/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work'
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    response = client.post(url, headers=headers, json=body)
    assert response.status_code == 200, response.text
    assert client.post(url, headers=headers, json=body).json()['work']['entity_id'] == response.json()['work']['entity_id']
    return response.json()['work']['entity_id']


@pytest.mark.parametrize('fail', [False, True])
def test_cg_formal_model_work_result_and_explicit_adoption(tmp_path, monkeypatch, fail):
    db, app, entry, service, calls, w, row, binding, payload = ready(tmp_path, monkeypatch, fail)
    ref = row['content']['entity_id']
    root = f'/api/workspace/v1/companies/{COMPANY}/content-growth/{w}/contents/{ref}'
    headers = {'X-Tenant-Id': 'selfuse', 'X-Ceo-Id': CEO}
    with TestClient(app) as client:
        work = create_model_work(client, db, w, binding['context']['assignment_ref'], payload,
            {'kind': 'content-growth', 'content_ref': ref, 'expected_version_ref': payload['expected_version_ref'],
             'selection': payload['selection'], 'references': payload['references']})
        assert not calls
        request = {**payload, 'work_ref': work}
        response = client.post(root + '/messages', headers=headers, json=request)
        assert response.status_code == 202, response.text
        client.post(root + '/messages', headers=headers, json=request)
        assert len(calls) == 1
        attempt = response.json()['attempt']['attempt_id']
        candidate = client.post(root + '/reply-candidate', headers=headers,
            json={'binding_ref': binding['binding_ref'], 'attempt_id': attempt, 'request_id': 'candidate-work'})
        with scope():
            assert RuntimeFoundation(db).get(work)['lifecycle_status'] == 'ACTIVE'
        if fail:
            assert candidate.status_code != 200
            return
        assert candidate.status_code == 200, candidate.text
        selected = candidate.json()['candidates'][0]['version']
        body = {'request_id': 'adopt-work', 'expected_version_ref': payload['expected_version_ref'],
                'data': {'candidate_ref': selected['entity_id'], 'checks': {'content': True, 'references': True, 'account': True}}}
        adopted = client.post(root + '/commands/adopt', headers=headers, json=body)
        assert adopted.status_code == 200, adopted.text
        assert client.post(root + '/commands/adopt', headers=headers, json=body).status_code == 200
    with scope(), db.connect() as con:
        done = RuntimeFoundation(db).get(work)
        assert done['lifecycle_status'] == done['data']['responsibilityRouting']['status'] == 'COMPLETED'
        assert done['data']['responsibilityRouting']['currentExecutorRef'] is None
        task = con.execute('select * from tasks where work_ref=?', (work,)).fetchall()
        usage = con.execute('select * from ai_usage_records where work_ref=?', (work,)).fetchall()
        assert len(task) == len(usage) == len(done['data']['acceptanceRefs']) == 1
        assert usage[0]['task_id'] == task[0]['task_id']
        assert done['data']['resultRefs'] == ['task:' + task[0]['task_id']]
        assert RuntimeFoundation(db).get(done['data']['acceptanceRefs'][0])['lifecycle_status'] == 'CLOSED'
