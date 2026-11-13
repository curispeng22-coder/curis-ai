"""T-011 isolated local launch; no model or account connections."""
from app.database import Database
from app.first_launch_service import FirstLaunchService
from app.tenant_context import TenantContext


def test_launch_repeat_and_restart(tmp_path, monkeypatch):
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'launch.sqlite')); db.initialize()
    with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
        first = FirstLaunchService(db).ensure()
        assert len(first['teams']) == 3
        assert all(t['status_label'] == '待连接能力' for t in first['teams'])
        assert FirstLaunchService(db).ensure() == first
        assert FirstLaunchService(Database(db.path)).ensure() == first


def test_draft_without_model_survives_restart_and_configuration(tmp_path, monkeypatch):
    from app.writing_entry_service import WritingEntryService
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'draft.sqlite')); db.initialize()
    with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
        service = FirstLaunchService(db)
        launch = service.ensure()
        c = launch['company_id']; w = next(t['workspace_id'] for t in launch['teams'] if t['kind'] == 'writing')
        saved = service.save_draft(c, w, 'original', '保留原始任务输入\n写一篇文稿', 0)
        assert saved['next_action'] == 'CONFIGURE_MODEL'
        assert saved['work']['lifecycle_status'] == 'PLANNED'
        work = saved['work']['entity_id']
        assert service.save_draft(c, w, 'original', saved['draft']['text'], 0)['work']['entity_id'] == work
        cold = FirstLaunchService(Database(db.path))
        assert cold.read_draft(c, w, work)['draft'] == saved['draft']
        # Offline capability response, no Provider/model call or credential.
        monkeypatch.setattr(WritingEntryService, 'execution_policy', lambda *a, **k: {'status': 'AVAILABLE'})
        resumed = cold.read_draft(c, w, work)
        assert resumed['next_action'] == 'CONTINUE_TASK'
        assert resumed['draft'] == saved['draft']
        assert resumed['return_to']['work_id'] == work


def test_launch_rejects_employee_and_foreign_company(tmp_path):
    import pytest
    from app.runtime import RuntimeScopeError
    db = Database(str(tmp_path/'scope.sqlite')); db.initialize()
    with TenantContext.scope('selfuse', ceo_id='owner', role='employee'), pytest.raises(RuntimeScopeError):
        FirstLaunchService(db).ensure()
    with TenantContext.scope('selfuse', ceo_id='owner', role='ceo', company_id='foreign'), pytest.raises(RuntimeScopeError):
        FirstLaunchService(db).ensure()


def test_api_launch_draft_and_cold_read(tmp_path, monkeypatch):
    from app.api.frontend_v1_router import build_frontend_v1_router, WritingTaskDraftIn
    from fastapi import HTTPException
    import pytest
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'api.sqlite')); db.initialize()
    def endpoints(database):
        return {route.name: route.endpoint for route in build_frontend_v1_router(database).routes}
    api = endpoints(db)
    with TenantContext.scope('selfuse', ceo_id='t011-api-owner', role='ceo'):
        first = api['first_launch']()
        c = first['company_id']; w = next(t['workspace_id'] for t in first['teams'] if t['kind'] == 'writing')
        saved = api['save_writing_task_draft'](c, w, WritingTaskDraftIn(draft_id='original', text='原任务输入', expected_revision=0))
        work = saved['work']['entity_id']
        restarted = endpoints(Database(db.path))
        assert restarted['first_launch']() == first
        assert restarted['read_writing_task_draft'](c, w, work)['draft']['text'] == '原任务输入'
    with TenantContext.scope('foreign', ceo_id='foreign', role='ceo'), pytest.raises(HTTPException) as denied:
        restarted['read_writing_task_draft'](c, w, work)
    assert denied.value.status_code == 404


def test_formal_version_and_task_both_survive_cold_restart(tmp_path, monkeypatch):
    from app.workspace_package_runtime import WorkspacePackageRuntime
    from app.writing_chapter_service import WritingChapterService
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'formal.sqlite')); db.initialize()
    with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
        launch = FirstLaunchService(db).ensure(); company = launch['company_id']
        workspace = next(t['workspace_id'] for t in launch['teams'] if t['kind'] == 'writing')
        runtime = WorkspacePackageRuntime(db)
        # Existing carrier only; T-011 adds no book/chapter schema.
        book = runtime.create_object(workspace, 'core.domain-object.create', 'WritingBook', {'title': '已有文稿载体', 'status': 'DRAFT'})['object_id']
        chapter = runtime.create_object(workspace, 'core.domain-object.create', 'WritingChapter', {'title': '文稿', 'bookRef': book, 'status': 'DRAFT'})['object_id']
        writing = WritingChapterService(db)
        def command(action, payload):
            base = writing.chapter(company, workspace, book, chapter)['draft']['ref']
            return writing.command(company, workspace, book, chapter, action, action, base, payload)
        command('draft.saved', {'text': '重启后保留的正式文稿正文', 'knowledge': []})
        inspection = command('inspection.recorded', {'mode': 'AUTHOR_MANUAL', 'checks': ['continuity', 'language', 'rights'], 'note': '本地人工确认'})
        command('formal.confirmed', {'inspection_ref': inspection['ref'], 'confirmed': True})
        before = writing.chapter(company, workspace, book, chapter)
        draft = FirstLaunchService(db).save_draft(company, workspace, 'pending', '尚未执行的下一项任务', 0)
        cold_db = Database(db.path)
        assert WritingChapterService(cold_db).chapter(company, workspace, book, chapter) == before
        recovered = FirstLaunchService(cold_db).read_draft(company, workspace, draft['work']['entity_id'])
        assert recovered['draft'] == draft['draft']
        assert recovered['work']['lifecycle_status'] == 'PLANNED'


def test_interrupted_launch_resumes_same_company(tmp_path, monkeypatch):
    import pytest
    from app.runtime.first_run_delivery import FirstRunDelivery
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'interrupted.sqlite')); db.initialize()
    original = FirstRunDelivery.materialize_package_for_existing_company
    with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
        monkeypatch.setattr(FirstRunDelivery, 'materialize_package_for_existing_company', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('模拟中断')))
        with pytest.raises(RuntimeError): FirstLaunchService(db).ensure()
        monkeypatch.setattr(FirstRunDelivery, 'materialize_package_for_existing_company', original)
        result = FirstLaunchService(Database(db.path)).ensure()
        assert len(result['teams']) == 3
        with db.connect() as con:
            assert con.execute('select count(*) from companies').fetchone()[0] == 1
            assert con.execute('select count(*) from canonical_businesses').fetchone()[0] == 3
            assert con.execute('select count(*) from workspaces').fetchone()[0] == 3
            assert con.execute("select count(*) from employee_instances where name in ('主编','作者','编辑')").fetchone()[0] == 3
            assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'


def test_concurrent_launch_and_draft_conflict_do_not_duplicate(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    import pytest
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'concurrent.sqlite')); db.initialize()
    def launch(_):
        with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
            try:
                return FirstLaunchService(db).ensure()
            except ValueError:
                # A concurrent in-progress activation is queryable and retryable.
                return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(launch, range(2)))
    with TenantContext.scope('selfuse', ceo_id='t011-owner', role='ceo'):
        service = FirstLaunchService(db); result = service.ensure()
        assert any(value == result for value in results)
        c = result['company_id']; w = next(t['workspace_id'] for t in result['teams'] if t['kind'] == 'writing')
        saved = service.save_draft(c, w, 'same', '第一个输入', 0)
        with pytest.raises(ValueError): service.save_draft(c, w, 'same', '陈旧页面输入', 0)
        assert service.read_draft(c, w, saved['work']['entity_id'])['draft']['text'] == '第一个输入'
        with db.connect() as con:
            assert con.execute('select count(*) from companies').fetchone()[0] == 1
            assert con.execute('select count(*) from workspaces').fetchone()[0] == 3
            assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 1


def test_existing_package_workspace_from_another_run_is_reused(tmp_path, monkeypatch):
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path/'packages'))
    db = Database(str(tmp_path/'existing.sqlite'))
    db.initialize()
    with TenantContext.scope('selfuse', ceo_id='t011-existing-owner', role='ceo'):
        first = FirstLaunchService(db).ensure()
        writing = next(team for team in first['teams'] if team['kind'] == 'writing')
        with db.connect() as con:
            # A normal package activation has a different founding run identity.
            con.execute(
                "update runtime_entities set entity_id='other-writing-founding-run' "
                "where entity_type='FOUNDING_RUN' and entity_id like 'founding-launch-%-writing'"
            )
        for _ in range(2):
            result = FirstLaunchService(Database(db.path)).ensure()
            reused = next(team for team in result['teams'] if team['kind'] == 'writing')
            assert reused['workspace_id'] == writing['workspace_id']
            assert reused['business_id'] == writing['business_id']
        with db.connect() as con:
            assert con.execute('select count(*) from canonical_businesses').fetchone()[0] == 3
            assert con.execute('select count(*) from workspaces').fetchone()[0] == 3
