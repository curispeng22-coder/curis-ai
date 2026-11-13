"""Manual scope -> original observations -> direction -> content context, real storage."""
import copy
from uuid import uuid4
import pytest
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from app.content_growth_operating_service import ContentGrowthOperatingService
from app.runtime import RuntimeScopeError
from backend.tests.test_cg_content_entry import setup, data, selected
from app.content_growth_entry_service import ASSETS
from app.workspace_package_runtime import WorkspacePackageRuntime
from backend.tests.test_writing_chapter_vertical import scope, COMPANY


def draft(format="speech", body=""):
    work = dict(goal="", shots=[], recording_requirements="", output_intent="UNCONFIRMED", output_spec="", source_refs=[], assignment_ref="", recipient_ref="", model_key="")
    return {**data(body), "format":format, "work":work}


def install_v02(db, path):
    with scope():
        installed=WorkspacePackageRuntime(db,path/"v02-store").install(ASSETS/"content_growth_v02",COMPANY,department_id="cg-dept",business_id="cg-v02-business",business_name="受控四格式候选")
    return installed["instance"]["workspace_id"]


def create(service, workspace, values=None, request="create-four"):
    return service.command(COMPANY,workspace,"","create",request_id=request,data=values or draft())


def save(service, workspace, row, values, request="save-four"):
    return service.command(COMPANY,workspace,row["content"]["entity_id"],"save",request_id=request,expected_version_ref=row["version"]["entity_id"],data=values)


def chain(service,w):
    scope_record=service.command(COMPANY,w,'Scope','scope','',{'title':'工作阅读','platform':'xhs','keywords':'纸质阅读','period':'十月'})
    snapshot=service.command(COMPANY,w,'Snapshot','snapshot','',{'title':'原观察','scope_ref':scope_record['ref'],'source':{'label':'作者人工观察','locator':'人工记录第1页','note':'不代表平台统计'},'period':'十月','value':None,'unit':'','definition':'','body':'两个读者提到阅读时间'})
    reference=service.command(COMPANY,w,'Reference','reference','',{'title':'阅读场景','scope_ref':scope_record['ref'],'snapshot_ref':snapshot['ref'],'body':'人工判断：从具体场景开始','purpose':'CONTEXT','locator':'原观察前两条'})
    direction=service.command(COMPANY,w,'Direction','direction','',{'title':'下班阅读','reference_ref':reference['ref'],'body':'面向通勤读者，介绍阅读方法','confirmed':True})
    return scope_record,snapshot,reference,direction


def test_manual_chain_versions_and_explicit_context(tmp_path):
    db,_,_=setup(tmp_path);w=install_v02(db,tmp_path);s=ContentGrowthService(db);ops=ContentGrowthOperatingService(db,service=s)
    with scope():
        original=ops.read(COMPANY,w);assert original['records']==[]
        _,snap,ref,direction=chain(ops,w)
        row=create(s,w);content=row['content']['entity_id'];version=row['version']['entity_id']
        data={'title':'原方向','content_ref':content,'version_ref':version,'reference_refs':[ref['ref']],'direction_ref':direction['ref'],'report_refs':[]}
        value=ops.command(COMPANY,w,'Context','bind','',data)
        assert ops.command(COMPANY,w,'Context','bind','',data)==value
        assert s.content(COMPANY,w,content)['operating_context']['ref']==value['ref']
        changed=copy.deepcopy(data);changed['title']='别的'
        with pytest.raises(ContentGrowthConflict):ops.command(COMPANY,w,'Context','bind','',changed)
        assert snap['payload']['value'] is None
        assert value['source']=='CEO_MANUAL' and value['connection_status']=='NOT_CONNECTED'
        assert ContentGrowthOperatingService(db,service=ContentGrowthService(db)).read(COMPANY,w)['records'][-1]['ref']==value['ref']
        with pytest.raises((ValueError,RuntimeScopeError)):ops.command(COMPANY,w,'Context','foreign','',{**data,'content_ref':'foreign'})
        with db.connect() as con:assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0


def test_manual_exact_types_and_revisions(tmp_path):
    db,_,w=setup(tmp_path);s=ContentGrowthService(db);ops=ContentGrowthOperatingService(db,service=s)
    with scope():
        first,*_=chain(ops,w)
        for value in [{'title':'bad','platform':[],'keywords':'x','period':'x'},{'title':'bad','platform':'weibo','keywords':'x','period':'x'},{'title':'bad','platform':'xhs','keywords':'x','period':'x','verified':True}]:
            with pytest.raises((ValueError,TypeError)):ops.command(COMPANY,w,'Scope','bad','',value)
        new=ops.command(COMPANY,w,'Scope','revision',first['ref'],{**first['payload'],'period':'十一月'})
        assert new['revision']==2 and new['identity_ref']==first['ref']
        with pytest.raises(ContentGrowthConflict):ops.command(COMPANY,w,'Scope','late',first['ref'],first['payload'])
        assert next(r for r in ops.read(COMPANY,w)['records'] if r['ref']==first['ref'])['payload']['period']=='十月'


def test_report_pins_existing_account_period_and_observation_without_schema_widening(tmp_path):
    from backend.tests.test_cg_channel_accounts import account_data
    db,_,_=setup(tmp_path);w=install_v02(db,tmp_path);s=ContentGrowthService(db);ops=ContentGrowthOperatingService(db,service=s)
    with scope():
        account=s.account_create(COMPANY,w,data=account_data())
        observation=s.observation_create(COMPANY,w,request_id='report-observation',data={'title':'原人工观察','body':'人工记录两条留言','scope_ref':account['entity_id'],'period':'十月'})
        ref=observation['record']['entity_id']
        before=s.observation(COMPANY,w,ref)
        row=create(s,w)
        data={'title':'十月人工报告','account_ref':account['entity_id'],'period':'十月','observation_refs':[ref],'content_ref':row['content']['entity_id'],'version_ref':row['version']['entity_id'],'artifact_ref':'','fact':'两条人工留言','interpretation':'不能推定增长','unknown':'外部统计未连接','next_decision':'继续人工观察','confirmed':True}
        report=ops.command(COMPANY,w,'Report','report','',data)
        assert report['basis'][0]['ref']==ref and report['source']=='CEO_MANUAL'
        assert s.observation(COMPANY,w,ref)==before
        with pytest.raises(ValueError,match='账号和期间'):ops.command(COMPANY,w,'Report','wrong-period','',{**data,'period':'十一月'})
        other=s.account_create(COMPANY,w,data=account_data(name='另一个账号'))
        with pytest.raises(ValueError,match='账号和期间'):ops.command(COMPANY,w,'Report','wrong-account','',{**data,'account_ref':other['entity_id']})


def test_context_inherits_through_atomic_save_receipt_and_replay(tmp_path):
    db,_,_=setup(tmp_path);w=install_v02(db,tmp_path);s=ContentGrowthService(db);ops=ContentGrowthOperatingService(db,service=s)
    with scope():
        row=create(s,w);c=row['content']['entity_id'];v=row['version']['entity_id'];_,_,reference,direction=chain(ops,w)
        original=ops.command(COMPANY,w,'Context','original','',{'title':'原方向','content_ref':c,'version_ref':v,'reference_refs':[reference['ref']],'direction_ref':direction['ref'],'report_refs':[]})
        saved=save(s,w,row,draft('speech','保存新正文'),request='saved-with-context')
        replay=save(s,w,row,draft('speech','保存新正文'),request='saved-with-context')
        assert saved['version']['entity_id']==replay['version']['entity_id']
        assert saved['operating_context']['ref']==original['ref']
        assert 'operating_context_ref' not in saved['version']['data']
        with db.connect() as con:
            receipts=con.execute("select payload from evolution_events where event_type='cg.content.saved' and correlation_id=?",(c,)).fetchall()
        import json
        assert len(receipts)==1 and json.loads(receipts[0][0])['context_ref']==original['ref']
        # A later explicit binding changes only this version, never the inherited original record.
        revised=ops.command(COMPANY,w,'Context','explicit-new',original['ref'],{**original['payload'],'version_ref':saved['version']['entity_id'],'title':'明确重绑'})
        assert s.content(COMPANY,w,c)['operating_context']['ref']==revised['ref']
        with db.connect() as con:assert ops.context(con,s.entry.authoring_scope(COMPANY,w),c,v)['ref']==original['ref']


def legal_adoption(tmp_path, *, with_context=True):
    """All candidate/feedback/adoption rows are produced by the real service commands."""
    db,_,_=setup(tmp_path);w=install_v02(db,tmp_path);service=ContentGrowthService(db);ops=ContentGrowthOperatingService(db,service=service)
    with scope():
        first=create(service,w,draft('graphic',data()['body']));c=first['content']['entity_id'];v=first['version']['entity_id'];context_record=None
        if with_context:
            _,_,reference,direction=chain(ops,w)
            from backend.tests.test_cg_channel_accounts import account_data
            account=service.account_create(COMPANY,w,data=account_data())
            observed=service.observation_create(COMPANY,w,request_id='adoption-observation',data={'title':'原观察','body':'两条人工记录','scope_ref':account['entity_id'],'period':'十月'})
            report=ops.command(COMPANY,w,'Report','adoption-report','',{'title':'原报告','account_ref':account['entity_id'],'period':'十月','observation_refs':[observed['record']['entity_id']],'content_ref':c,'version_ref':v,'artifact_ref':'','fact':'两条记录','interpretation':'不推定增长','unknown':'平台未连接','next_decision':'继续观察','confirmed':True})
            context_record=ops.command(COMPANY,w,'Context','adoption-context','',{'title':'人工依据A','content_ref':c,'version_ref':v,'reference_refs':[reference['ref']],'direction_ref':direction['ref'],'report_refs':[report['ref']]})
        row=service.command(COMPANY,w,c,'candidate',request_id='manual-candidate',expected_version_ref=v,data={**draft('graphic','候选的完整正文'),'selection':selected(first)})
        candidate=row['candidates'][0];assert candidate['eligible'] and not candidate['reasons']
        feedback=service.candidate_feedback(COMPANY,w,c,candidate_ref=candidate['version']['entity_id'],candidate_version=candidate['feedback_version'],basis_version_ref=v,action='ACCEPT',reason='人工核对三个边界',request_id=str(uuid4()))
        assert feedback['action']=='ACCEPT' and not feedback['replayed']
        adopted=service.command(COMPANY,w,c,'adopt',request_id='legal-adopt',expected_version_ref=v,data={'candidate_ref':candidate['version']['entity_id'],'checks':{'content':True,'references':True,'account':True}})
    return db,service,ops,w,c,first,candidate['version'],context_record,adopted


def test_legal_adoption_cold_read_further_save_and_explicit_rebind_keep_original_context(tmp_path):
    db,service,ops,w,c,first,candidate,original,adopted=legal_adoption(tmp_path)
    with scope():
        assert adopted['version']['data']['context_basis_ref']==original['ref']
        assert adopted['operating_context']['ref']==original['ref']
        assert ContentGrowthService(db).content(COMPANY,w,c)['operating_context']['ref']==original['ref']
        with db.connect() as con:
            info=service.entry.authoring_scope(COMPANY,w,connection=con)
            assert ops.context(con,info,c,candidate['entity_id'])['ref']==original['ref']
        saved=save(service,w,adopted,draft('graphic','采用后的再保存'),request='after-adoption')
        assert saved['operating_context']['ref']==original['ref']
        assert ContentGrowthService(db).content(COMPANY,w,c)['operating_context']['ref']==original['ref']
        replay=save(service,w,adopted,draft('graphic','采用后的再保存'),request='after-adoption')
        assert replay['version']['entity_id']==saved['version']['entity_id']
        rebound=ops.command(COMPANY,w,'Context','explicit-rebind',original['ref'],{**original['payload'],'title':'明确的新绑定B','version_ref':saved['version']['entity_id']})
        assert ContentGrowthService(db).content(COMPANY,w,c)['operating_context']['ref']==rebound['ref']
        with db.connect() as con:
            info=service.entry.authoring_scope(COMPANY,w,connection=con)
            assert ops.context(con,info,c,first['version']['entity_id'])['ref']==original['ref']
            assert ops.context(con,info,c,adopted['version']['entity_id'])['ref']==original['ref']
            assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0
            assert con.execute('pragma integrity_check').fetchone()[0]=='ok'
        cold=ContentGrowthService(db).content(COMPANY,w,c)
        for old in (first['version'],candidate,adopted['version'],saved['version']):assert next(v for v in cold['versions']if v['entity_id']==old['entity_id'])==old


def test_legacy_no_context_adoption_and_save_do_not_infer_a_later_binding(tmp_path):
    db,service,ops,w,c,first,candidate,original,adopted=legal_adoption(tmp_path,with_context=False)
    with scope():
        assert original is None and adopted['operating_context'] is None
        saved=save(service,w,adopted,draft('graphic','不带依据的继续保存'))
        assert saved['operating_context'] is None
        record=ops.command(COMPANY,w,'Context','later-only','',{'title':'后来的明确绑定','content_ref':c,'version_ref':saved['version']['entity_id'],'reference_refs':[],'direction_ref':'','report_refs':[]})
        assert service.content(COMPANY,w,c)['operating_context']['ref']==record['ref']
        with db.connect() as con:
            info=service.entry.authoring_scope(COMPANY,w,connection=con)
            assert ops.context(con,info,c,adopted['version']['entity_id']) is None
            assert ops.context(con,info,c,first['version']['entity_id']) is None


@pytest.mark.parametrize('corruption',['missing','wrong-kind','foreign-content','wrong-root','malformed-pin','candidate-pin-mismatch','missing-adoption-receipt','receipt-candidate-mismatch'])
def test_legal_adoption_then_corrupt_pin_or_receipt_fails_closed(tmp_path,corruption):
    import json
    db,service,ops,w,c,first,candidate,original,adopted=legal_adoption(tmp_path)
    with scope():
        # Only negative corruption uses SQL; the full legal adoption above is never fabricated.
        changed=dict(adopted['version']['data'])
        if corruption=='missing':changed['context_basis_ref']='missing-context'
        if corruption=='malformed-pin':changed['context_basis_ref']={'ref':original['ref']}
        if corruption=='candidate-pin-mismatch':changed['context_basis_ref']=''
        if corruption=='wrong-kind':
            changed['context_basis_ref']=ops.command(COMPANY,w,'Scope','wrong-kind','',{'title':'范围','platform':'xhs','keywords':'书','period':'十月'})['ref']
            with db.connect() as con:
                original_candidate=dict(candidate['data']);original_candidate['context_basis_ref']=changed['context_basis_ref']
                con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(original_candidate),candidate['entity_id']))
        if corruption=='foreign-content':
            other=create(service,w,draft('graphic','另一内容'),request='other-content')
            foreign=ops.command(COMPANY,w,'Context','foreign-context','',{'title':'另一内容依据','content_ref':other['content']['entity_id'],'version_ref':other['version']['entity_id'],'reference_refs':[],'direction_ref':'','report_refs':[]})
            changed['context_basis_ref']=foreign['ref']
            with db.connect() as con:
                value=dict(candidate['data']);value['context_basis_ref']=foreign['ref'];con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(value),candidate['entity_id']))
        if corruption=='wrong-root':
            saved=save(service,w,adopted,draft('graphic','后续正文'),request='wrong-root-next')
            later=ops.command(COMPANY,w,'Context','later-root',original['ref'],{**original['payload'],'version_ref':saved['version']['entity_id']})
            changed['context_basis_ref']=later['ref']
            with db.connect() as con:
                value=dict(candidate['data']);value['context_basis_ref']=later['ref'];con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(value),candidate['entity_id']))
        with db.connect() as con:
            con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(changed),adopted['version']['entity_id']))
            if corruption=='missing-adoption-receipt':con.execute("delete from evolution_events where event_type='cg.content.adopted' and correlation_id=?",(c,))
            if corruption=='receipt-candidate-mismatch':
                row=con.execute("select event_id,payload from evolution_events where event_type='cg.content.adopted' and correlation_id=?",(c,)).fetchone();value=json.loads(row['payload']);value['request']['candidate_ref']='foreign-candidate';con.execute('update evolution_events set payload=? where event_id=?',(json.dumps(value),row['event_id']))
        with db.connect() as con:
            info=service.entry.authoring_scope(COMPANY,w,connection=con)
            with pytest.raises((RuntimeScopeError,ContentGrowthConflict,KeyError)):
                ops.context(con,info,c,adopted['version']['entity_id'])


@pytest.mark.parametrize('field,value',[('context_ref','missing-context'),('context_ref',{}),('expected_version_ref',None),('expected_version_ref','foreign-version')])
def test_saved_after_adoption_receipt_cannot_lose_or_replace_its_original_pin(tmp_path,field,value):
    import json
    db,service,ops,w,c,first,candidate,original,adopted=legal_adoption(tmp_path)
    with scope():
        saved=save(service,w,adopted,draft('graphic','后续正文'))
        with db.connect() as con:
            row=con.execute("select event_id,payload from evolution_events where correlation_id=? and event_type='cg.content.saved'",(c,)).fetchone();payload=json.loads(row['payload'])
            if field=='expected_version_ref':payload['request'][field]=value
            else:payload[field]=value
            con.execute('update evolution_events set payload=? where event_id=?',(json.dumps(payload),row['event_id']))
        with db.connect() as con:
            info=service.entry.authoring_scope(COMPANY,w,connection=con)
            with pytest.raises((RuntimeScopeError,ContentGrowthConflict)):ops.context(con,info,c,saved['version']['entity_id'])
