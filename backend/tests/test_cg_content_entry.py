"""Isolated candidate carrier and canonical authoring; no ordinary publication."""
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.content_growth_entry_service import ContentGrowthEntryService, ASSETS
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from app.workspace_package_runtime import WorkspacePackageRuntime, validate_package, PackageValidationError
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO


def setup(path):
    db=Database(str(path/'cg.sqlite'));db.initialize()
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse',?,'测试内容公司','active')",(COMPANY,CEO))
        con.execute("insert into department_templates(id,slug,name,department_type,source,tenant_id) values ('cg-test','cg-test','受控内容部门模板','TEST','tenant_private','selfuse')")
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values ('cg-dept','selfuse',?,'cg-test','内容部门','TEST','active')",(COMPANY,))
    with scope():
        runtime=WorkspacePackageRuntime(db,path/'store')
        installed=runtime.install(ASSETS/'content_growth',COMPANY,department_id='cg-dept',business_id='cg-business',business_name='内部候选验证')
    return db,runtime,installed['instance']['workspace_id']


def data(body='雨后😀，书桌上的信仍未打开。'):
    return dict(title='第一篇图文',topic='原创故事',audience='文学读者',body=body,target_account_refs=[],references=[])


def create(service,w):return service.command(COMPANY,w,'','create',request_id='create-1',data=data())


def selected(row):return dict(version_ref=row['version']['entity_id'],start=2,end=4,excerpt='😀',locator='body')


def test_candidate_package_and_no_publication(tmp_path):
    db,runtime,w=setup(tmp_path)
    with scope():
        entry=ContentGrowthEntryService(db)
        assert entry.definitions(COMPANY)['available'] is True
        assert entry.publication()['version']=='0.2.0'
        assert entry.authoring_scope(COMPANY,w)['publication_status']=='INTERNAL_CANDIDATE_NO_PUBLICATION'
        with pytest.raises(ValueError):entry.publication(version="0.1.0")
        with pytest.raises(PackageValidationError):runtime.create_object(w,'core.domain-object.create','ContentGraphic',data())
    with db.connect() as con:assert con.execute('select count(*) from workspace_package_objects').fetchone()[0]==0


@pytest.mark.parametrize('bindings',[{'ContentGraphic':[]},{'ContentGraphic':{}},{'ContentGraphic':None},{'ContentGraphic':'UNKNOWN'},{'Unknown':'CONTENT_ITEM'},None])
def test_binding_malformed_fail_closed(tmp_path,bindings):
    package=tmp_path/'package';shutil.copytree(ASSETS/'content_growth',package)
    manifest=json.loads((package/'manifest.json').read_text());manifest['canonicalEntityBindings']=bindings
    (package/'manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(PackageValidationError):validate_package(package)


def test_binding_legacy_absent_semantics(tmp_path):
    package=tmp_path/'package';shutil.copytree(ASSETS/'content_growth',package)
    manifest=json.loads((package/'manifest.json').read_text());manifest.pop('canonicalEntityBindings');(package/'manifest.json').write_text(json.dumps(manifest))
    assert 'canonicalEntityBindings' not in validate_package(package)['manifest']


def test_canonical_create_save_candidate_adopt_cold_read(tmp_path):
    db,_,w=setup(tmp_path)
    with scope():
        s=ContentGrowthService(db);row=create(s,w);content=row['content']['entity_id'];head=row['version']['entity_id']
        assert create(s,w)['content']['entity_id']==content
        assert row['content']['lifecycle_status']=='DRAFT'
        assert s.selection(row['version'],selected(row))['excerpt']=='😀'
        candidate=s.command(COMPANY,w,content,'candidate',request_id='manual',expected_version_ref=head,data={**data('候选完整正文。'),'selection':selected(row)})
        assert candidate['content']['current_version_id']==head
        candidate_ref=candidate['candidates'][0]['version']['entity_id']
        adopted=s.command(COMPANY,w,content,'adopt',request_id='adopt-1',expected_version_ref=head,data={'candidate_ref':candidate_ref,'checks':{'content':True,'references':True,'account':True}})
        new=adopted['version']['entity_id'];assert new!=head and adopted['version']['data']['source_candidate_ref']==candidate_ref
        again=s.command(COMPANY,w,content,'adopt',request_id='adopt-1',expected_version_ref=head,data={'candidate_ref':candidate_ref,'checks':{'content':True,'references':True,'account':True}})
        assert again['version']['entity_id']==new
        cold=ContentGrowthService(Database(db.path)).content(COMPANY,w,content);assert cold['version']==adopted['version']
        assert cold['candidates'][0]['eligible'] is False
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='CONTENT_VERSION'").fetchone()[0]==3
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0]==0
        assert con.execute("select count(*) from runtime_entities where lifecycle_status='SCHEDULED'").fetchone()[0]==0
        assert con.execute('pragma integrity_check').fetchone()[0]=='ok'


def test_concurrent_save_conflict_no_partial_version(tmp_path):
    db,_,w=setup(tmp_path)
    with scope():row=create(ContentGrowthService(db),w)
    ref=row['content']['entity_id'];head=row['version']['entity_id']
    def save(i):
        with scope():
            try:return ContentGrowthService(Database(db.path)).command(COMPANY,w,ref,'save',request_id=f'save-{i}',expected_version_ref=head,data=data(f'版本{i}'))
            except ValueError:return None
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(save,[0,1]))
    assert sum(r is not None for r in results)==1
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='CONTENT_VERSION'").fetchone()[0]==2
        assert con.execute("select count(*) from runtime_links where relation='HAS_VERSION'").fetchone()[0]==2
        assert con.execute("select count(*) from evolution_events where event_type='cg.content.saved'").fetchone()[0]==1


def test_atomic_rollback_receipt_failure(tmp_path):
    db,_,w=setup(tmp_path)
    with scope():row=create(ContentGrowthService(db),w)
    with db.connect() as con:con.execute("create trigger fail_cg_save before insert on evolution_events when new.event_type='cg.content.saved' begin select raise(ABORT,'injected receipt failure'); end")
    with scope(),pytest.raises(Exception,match='injected receipt failure'):
        ContentGrowthService(db).command(COMPANY,w,row['content']['entity_id'],'save',request_id='fail',expected_version_ref=row['version']['entity_id'],data=data('不得留下半次保存'))
    with scope():assert ContentGrowthService(db).content(COMPANY,w,row['content']['entity_id'])['version']['entity_id']==row['version']['entity_id']
    with db.connect() as con:assert con.execute("select count(*) from runtime_entities where entity_type='CONTENT_VERSION'").fetchone()[0]==1


@pytest.mark.parametrize('identity',[{'tenant_id':'other'},{'company_id':'other'},{'ceo_id':'other'},{'role':'employee'}])
def test_foreign_write_scope(tmp_path,identity):
    db,_,w=setup(tmp_path)
    with scope(**identity),pytest.raises(RuntimeScopeError):create(ContentGrowthService(db),w)


def test_utf16_old_selection_and_stale_candidate(tmp_path):
    db,_,w=setup(tmp_path)
    with scope():
        s=ContentGrowthService(db);row=create(s,w);head=row['version']['entity_id'];ref=row['content']['entity_id']
        with pytest.raises(ValueError):s.selection(row['version'],{**selected(row),'end':3})
        s.command(COMPANY,w,ref,'candidate',request_id='candidate',expected_version_ref=head,data={**data('候选'),'selection':selected(row)})
        saved=s.command(COMPANY,w,ref,'save',request_id='save',expected_version_ref=head,data=data('后续正文'))
        assert '正文已改变' in saved['candidates'][0]['reasons'][0]
        with pytest.raises(ValueError):s.selection(saved['version'],selected(row))
        with pytest.raises(ContentGrowthConflict):s.command(COMPANY,w,ref,'adopt',request_id='stale',expected_version_ref=saved['version']['entity_id'],data={'candidate_ref':saved['candidates'][0]['version']['entity_id'],'checks':{'content':True,'references':True,'account':True}})


def test_reference_actual_version_stale_and_foreign_scope(tmp_path):
    from app.runtime import RuntimeFoundation
    db,_,w=setup(tmp_path)
    with scope():
        s=ContentGrowthService(db);other=s.command(COMPANY,w,'','create',request_id='source',data=data('来源正文'))
        ref={'reference_id':other['content']['entity_id'],'workspace_id':w,'kind':'CONTENT_ITEM','purpose':'FACT','locator':''}
        qualified=s.resolve_references(s.entry.authoring_scope(COMPANY,w)['scope'],[ref])
        assert qualified[0]['version_ref']==other['version']['entity_id']
        row=s.command(COMPANY,w,'','create',request_id='with-ref',data={**data(),'references':qualified})
        s.command(COMPANY,w,row['content']['entity_id'],'candidate',request_id='candidate-ref',expected_version_ref=row['version']['entity_id'],data={**data('候选正文'),'references':qualified,'selection':selected(row)})
        s.command(COMPANY,w,other['content']['entity_id'],'save',request_id='source-next',expected_version_ref=other['version']['entity_id'],data=data('新版来源正文'))
        updated=s.content(COMPANY,w,row['content']['entity_id']);assert not updated['candidates'][0]['eligible']
        assert any('引用版本已改变' in reason for reason in updated['candidates'][0]['reasons'])
        with pytest.raises(ValueError):s.resolve_references(s.entry.authoring_scope(COMPANY,w)['scope'],qualified)
        with pytest.raises(RuntimeScopeError):s.resolve_references(s.entry.authoring_scope(COMPANY,w)['scope'],[{**ref,'workspace_id':'foreign'}])


def test_local_admission_rejects_changed_or_missing_decision(tmp_path,monkeypatch):
    from pathlib import Path
    db, *_ = setup(tmp_path)
    original=Path.read_text
    def changed(path,*a,**kw):
        raw=original(path,*a,**kw)
        if path == ASSETS/'content_growth_v02_release.json':
            value=json.loads(raw);value['decision']['sha256']='0'*64;return json.dumps(value)
        return raw
    monkeypatch.setattr(Path,'read_text',changed)
    with scope(),pytest.raises(ValueError):ContentGrowthEntryService(db).publication()
