"""Isolated real local entry mechanics; no Provider/native acceptance."""
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.first_run_delivery import FirstRunDelivery, FirstGeneralWorkspaceDraft
from app.runtime.business_spine import BusinessSpineError
from app.writing_entry_service import WritingEntryService, ASSETS
from app.writing_chapter_service import WritingConflict
from app.database import Database
from app.workspace_package_runtime import WorkspacePackageRuntime
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO


def company_only(path):
    db = Database(str(path / "entry.sqlite")); db.initialize()
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse',?,'受控入口测试公司','active')", (COMPANY, CEO))
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values ('writing-test-department','selfuse',?,'writing-test-template','受控测试部门','TEST','active')", (COMPANY,))
    return db, WorkspacePackageRuntime(db, path / "package-store")


def confirmed(db, name="第一项写作", goal="完成本地原创"):
    foundation = RuntimeFoundation(db)
    if not foundation.list("CEO_ASSISTANT", company_id=COMPANY):
        foundation.create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO, data={"name": "测试助理"})
    entry = WritingEntryService(db)
    values = dict(intent="写原创章节", business_name=name, goal=goal, positioning="原创", workspace_name="写作空间",
                  package_id=entry.publication()["package_id"], department_id="writing-test-department")
    proposal = entry.proposal(COMPANY, values)
    run = foundation.create("FOUNDING_RUN", owner_ref=CEO, lifecycle_status="PROPOSED", data={"v1Proposal": proposal})
    foundation.transition(run["entity_id"], "CEO_CONFIRMED", actor="CEO", trigger="confirm_company")
    draft = FirstGeneralWorkspaceDraft(COMPANY, CEO, "测试公司", "测试部门", name, values["goal"], values["positioning"], values["workspace_name"], intent_summary=values["intent"])
    return run["entity_id"], draft, proposal


def materialize(delivery, runtime, run, draft, proposal, **kw):
    return delivery.materialize_package_for_existing_company(run, draft, package_runtime=runtime,
        source=ASSETS / "writing_authoring", definition=proposal["snapshot"]["definition"],
        department_id=proposal["department_id"], proposal_sha256=proposal["proposal_sha256"], **kw)


def test_confirmed_atomic_repeat_multiple_business_cold_read(tmp_path):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
    delivery = FirstRunDelivery(db)
    def create(_):
        with scope(): return materialize(delivery, runtime, run, draft, proposal)
    with ThreadPoolExecutor(max_workers=2) as pool: list(pool.map(create, [0, 1]))
    with scope():
        result = materialize(delivery, runtime, run, draft, proposal)
        assert result["activation"]["status"] == "COMPLETED", result
        assert FirstRunDelivery(db).package_creation_status(run, COMPANY, CEO)["creation_result"] == result["creation_result"]
        run2, draft2, proposal2 = confirmed(db, "独立第二业务")
        second = materialize(delivery, runtime, run2, draft2, proposal2)
        assert second["activation"]["status"] == "COMPLETED", second
        assert result["creation_result"]["workspace_id"] != second["creation_result"]["workspace_id"]
        assert WritingEntryService(db).local.collection(COMPANY, second["creation_result"]["workspace_id"])["books"] == []
        with pytest.raises(BusinessSpineError): materialize(delivery, runtime, run, replace(draft, goal="换目标"), proposal)
    with db.connect() as con:
        assert con.execute("select count(*) from canonical_businesses where business_id like 'business-first-%'").fetchone()[0] == 2
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_install_rollback_explicit_retry_and_unknown_no_replay(tmp_path, monkeypatch):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        delivery = FirstRunDelivery(db)
        original = runtime.install_confirmed_in_connection
        monkeypatch.setattr(runtime, "install_confirmed_in_connection", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("injected transaction failure")))
        assert materialize(delivery, runtime, run, draft, proposal)["activation"]["status"] == "FAILED"
        with db.connect() as con:
            assert con.execute("select count(*) from canonical_businesses where business_id=?", (delivery._ids(run)["business_id"],)).fetchone()[0] == 0
        assert materialize(delivery, runtime, run, draft, proposal)["activation"]["status"] == "FAILED"
        monkeypatch.setattr(runtime, "install_confirmed_in_connection", original)
        assert materialize(delivery, runtime, run, draft, proposal, retry_no=1)["activation"]["status"] == "COMPLETED"
        run2, draft2, proposal2 = confirmed(db, "未知创建")
        with db.connect() as con:
            row = con.execute("select data_json from runtime_entities where entity_id=?", (run2,)).fetchone()
            data = json.loads(row[0]); data["v1Activation"] = {"company_id": COMPANY, "status": "RUNNING", "process_id": "old-process"}
            con.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), run2))
        assert materialize(delivery, runtime, run2, draft2, proposal2)["activation"]["status"] == "UNKNOWN"


@pytest.mark.parametrize("identity", [{"tenant_id": "other"}, {"company_id": "other"}, {"ceo_id": "other"}, {"role": "employee"}])
def test_entry_rejects_foreign_actor(tmp_path, identity):
    db, _, w, _, _ = setup(tmp_path)
    with scope(**identity), pytest.raises(RuntimeScopeError): WritingEntryService(db).assign(COMPANY, w, "any", 0)


def test_no_model_local_authoring_and_invalid_department(tmp_path):
    db, _, w, _, _ = setup(tmp_path)
    with scope():
        entry = WritingEntryService(db)
        assert entry.definitions(COMPANY)["available"] is True
        assert entry.metadata(COMPANY, w)["execution"]["status"] == "UNAVAILABLE"
        with pytest.raises(RuntimeScopeError): entry.proposal(COMPANY, {"package_id": entry.publication()["package_id"], "department_id": "foreign"})
        with pytest.raises(WritingConflict): entry.proposal(COMPANY, {"package_id": "unknown", "department_id": "writing-test-department"})


def test_missing_runtime_holder_preserves_local_entry(tmp_path):
    db, _, w, _, _ = setup(tmp_path)
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) values ('missing-holder','selfuse',?,'writing-test-department','et_product_manager','测试作者','写作','idle')", (COMPANY,))
    with scope():
        entry = WritingEntryService(db)
        entry.assign(COMPANY, w, "missing-holder", entry.metadata(COMPANY, w)["assignment_revision"])
        with db.connect() as con:
            con.execute("delete from runtime_entities where entity_id='missing-holder'")
        assert entry.metadata(COMPANY, w)["execution"]["status"] == "UNAVAILABLE"
        assert entry.local.collection(COMPANY, w)["books"]

# Populated legacy schema fixtures exercise the real table replacement on isolated DBs.
import sqlite3
from contextlib import contextmanager
from app.workspace_package_runtime import PACKAGE_DDL, PackageConflictError, PackageScopeError
from backend.tests.test_writing_chapter_vertical import local_chain
from app.writing_chapter_service import WritingChapterService

INSTANCE_TABLES = ('workspace_package_instances', 'workspace_package_objects',
    'workspace_package_activities', 'workspace_package_lifecycle_events', 'workspace_package_migration_journal')


def database_values(db):
    with db.connect() as con:
        names = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
        return {name: tuple(tuple(r) for r in con.execute('select * from "' + name + '" order by rowid')) for name in names}


def legacy_populated(path, monkeypatch):
    path.mkdir(parents=True, exist_ok=True)
    db = Database(str(path / 'writing.sqlite')); db.initialize()
    old_ddl = PACKAGE_DDL.replace('  foreign key(tenant_id, package_id, package_version)',
        '  unique(tenant_id, company_id, package_id, package_version),\n  foreign key(tenant_id, package_id, package_version)', 1)
    with db.connect() as con: con.executescript(old_ddl)
    with monkeypatch.context() as patch:
        patch.setattr(WorkspacePackageRuntime, '_migrate_instance_uniqueness', lambda self: None)
        db, runtime, w, b, c = setup(path)
    with scope():
        local_chain(WritingChapterService(db), w, b, c)
    with db.connect() as con:
        instance = dict(con.execute('select * from workspace_package_instances').fetchone())
        for table in INSTANCE_TABLES[-2:]:
            # Synthetic old lifecycle checkpoints are fixture evidence, not live upgrade claims.
            row = {r['name']: 1 if r['type'].lower() == 'integer' else 'legacy-fixture-' + r['name']
                   for r in con.execute('pragma table_info(' + table + ')')}
            row.update({k: instance[k] for k in ('instance_id', 'tenant_id', 'company_id', 'workspace_id', 'package_id')})
            row.update(from_version=instance['package_version'], to_version=instance['package_version'],
                from_digest=instance['package_digest'], to_digest=instance['package_digest'])
            if table.endswith('events'): row['action'] = 'UPGRADE'
            else: row.update(direction='UP', status='APPLIED', reversible=1, affected_count=2)
            con.execute('insert into ' + table + '(' + ','.join(row) + ') values (' + ','.join('?' for _ in row) + ')', tuple(row.values()))
    return db, runtime


class CheckedMigrationDatabase:
    def __init__(self, db, deny=None):
        self.path, self.deny, self.settings = db.path, deny, []

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.path); con.row_factory = sqlite3.Row
        con.execute('pragma foreign_keys=on')
        if self.deny:
            con.set_authorizer(lambda action, *args: sqlite3.SQLITE_DENY if action == self.deny else sqlite3.SQLITE_OK)
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback(); raise
        finally:
            self.settings.append(con.execute('pragma foreign_keys').fetchone()[0]); con.close()


def migrate_only(db):
    runtime = object.__new__(WorkspacePackageRuntime); runtime.db = db
    runtime._migrate_instance_uniqueness()


def test_populated_instance_migration_preserves_all_tables_and_fk_setting(tmp_path, monkeypatch):
    db, runtime = legacy_populated(tmp_path, monkeypatch)
    before = database_values(db); checked = CheckedMigrationDatabase(db)
    migrate_only(checked)
    assert database_values(db) == before
    assert checked.settings == [1]
    with db.connect() as con:
        assert con.execute('pragma foreign_key_check').fetchall() == []
        assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'
        assert len(con.execute('pragma index_list(workspace_package_instances)').fetchall()) == 2
    migrate_only(checked)
    assert database_values(db) == before and checked.settings == [1, 1]
    with scope(): WorkspacePackageRuntime(db, runtime.store_root)
    assert database_values(db) == before


@pytest.mark.parametrize('denied', [sqlite3.SQLITE_DROP_TABLE, sqlite3.SQLITE_ALTER_TABLE])
def test_populated_migration_failure_rolls_back_schema_rows_and_fk(tmp_path, monkeypatch, denied):
    db, _ = legacy_populated(tmp_path, monkeypatch)
    before = database_values(db)
    with db.connect() as con: schema = tuple(tuple(r) for r in con.execute('select * from sqlite_master order by name'))
    checked = CheckedMigrationDatabase(db, denied)
    with pytest.raises(sqlite3.DatabaseError): migrate_only(checked)
    assert checked.settings == [1] and database_values(db) == before
    with db.connect() as con:
        assert tuple(tuple(r) for r in con.execute('select * from sqlite_master order by name')) == schema
        assert con.execute('pragma foreign_key_check').fetchall() == []
    migrate_only(CheckedMigrationDatabase(db))
    assert database_values(db) == before


@pytest.mark.parametrize('ddl', [
    'alter table workspace_package_instances add column unexpected text',
    'create index custom_instance_index on workspace_package_instances(company_id)',
    'create trigger custom_instance_trigger after insert on workspace_package_instances begin select 1; end',
    'create view custom_instance_view as select * from workspace_package_instances',
    'create table unexpected_child(id text references workspace_package_instances(instance_id))',
    "update workspace_package_objects set instance_id='orphan-fixture'",
])
def test_unknown_schema_dependency_or_orphan_stops_without_mutation(tmp_path, monkeypatch, ddl):
    db, runtime = legacy_populated(tmp_path, monkeypatch)
    with db.connect() as con: con.execute(ddl)
    before = database_values(db)
    with db.connect() as con: schema = tuple(tuple(r) for r in con.execute('select * from sqlite_master order by name'))
    with pytest.raises(PackageConflictError):
        with scope(): WorkspacePackageRuntime(db, runtime.store_root)
    assert database_values(db) == before
    with db.connect() as con: assert tuple(tuple(r) for r in con.execute('select * from sqlite_master order by name')) == schema


def test_concurrent_populated_migration_and_repeated_startup(tmp_path, monkeypatch):
    db, runtime = legacy_populated(tmp_path, monkeypatch); before = database_values(db)
    def start(_):
        with scope(): return WorkspacePackageRuntime(Database(db.path), runtime.store_root)
    with ThreadPoolExecutor(max_workers=3) as pool: list(pool.map(start, range(3)))
    assert database_values(db) == before
    with scope(): WorkspacePackageRuntime(Database(db.path), runtime.store_root)
    assert database_values(db) == before


def two_confirmed_businesses(path):
    db, runtime = company_only(path)
    with scope():
        first = confirmed(db, '迁移测试第一业务'); second = confirmed(db, '迁移测试第二业务')
    def create(item):
        with scope(): return materialize(FirstRunDelivery(db), runtime, *item)
    with ThreadPoolExecutor(max_workers=2) as pool: results = list(pool.map(create, [first, second]))
    assert all(r['activation']['status'] == 'COMPLETED' for r in results), results
    return db, runtime, [r['creation_result'] for r in results]


def test_multi_business_legacy_exact_lookup_ambiguity_and_tenant(tmp_path):
    db, runtime = company_only(tmp_path)
    with scope():
        first = confirmed(db); result = materialize(FirstRunDelivery(db), runtime, *first)['creation_result']
        args = dict(department_id='writing-test-department', business_name='legacy replay')
        with pytest.raises(PackageConflictError):
            runtime.install(ASSETS / 'writing_authoring', COMPANY, business_id='old-compatible-different-id', **args)
        second = confirmed(db, '第二业务'); other = materialize(FirstRunDelivery(db), runtime, *second)['creation_result']
        for item in (result, other):
            assert runtime.install(ASSETS / 'writing_authoring', COMPANY, business_id=item['business_id'], **args)['instance']['workspace_id'] == item['workspace_id']
        with pytest.raises(PackageConflictError, match='unambiguous'):
            runtime.install(ASSETS / 'writing_authoring', COMPANY, business_id='unknown-business', **args)
    with scope(tenant_id='foreign'), pytest.raises(PackageScopeError):
        runtime.install(ASSETS / 'writing_authoring', COMPANY, business_id=result['business_id'], **args)
    with db.connect() as con:
        assert con.execute('select count(*) from workspace_package_instances').fetchone()[0] == 2
        row = dict(con.execute('select * from workspace_package_instances limit 1').fetchone())
        row['instance_id'] = 'duplicate-workspace-test'
        with pytest.raises(sqlite3.IntegrityError):
            con.execute('insert into workspace_package_instances(' + ','.join(row) + ') values (' + ','.join('?' for _ in row) + ')', tuple(row.values()))


@pytest.mark.parametrize('operation', ['disable', 'uninstall'])
def test_multi_business_lifecycle_keeps_sibling_operational(tmp_path, operation):
    db, runtime, results = two_confirmed_businesses(tmp_path)
    with scope():
        sibling = results[1]['workspace_id']
        before = runtime.get_workspace(sibling)
        getattr(runtime, operation)(results[0]['workspace_id'])
        after = runtime.get_workspace(sibling)
        assert after['instance']['status'] == 'ACTIVE'
        assert after['instance']['package_digest'] == before['instance']['package_digest']
        runtime.create_object(sibling, 'core.domain-object.create', 'WritingBook', {'title': '另一个独立业务仍可用'})


def test_two_businesses_and_two_books_scope_and_cold_read(tmp_path):
    db, runtime, results = two_confirmed_businesses(tmp_path)
    identities = []
    with scope():
        for result in results:
            w = result['workspace_id']
            for index in range(2):
                b = runtime.create_object(w, 'core.domain-object.create', 'WritingBook', {'title': f'作品{index}'})['object_id']
                c = runtime.create_object(w, 'core.domain-object.create', 'WritingChapter', {'title': '第一章', 'bookRef': b})['object_id']
                text = w + b
                WritingChapterService(db).command(COMPANY, w, b, c, 'draft.saved', 'save-' + c, 'ABSENT', {'text': text, 'knowledge': []})
                identities.append((w, b, c, text))
        cold = WritingChapterService(Database(db.path))
        for w, b, c, text in identities:
            assert cold.chapter(COMPANY, w, b, c)['draft']['text'] == text
            other = results[1]['workspace_id'] if w == results[0]['workspace_id'] else results[0]['workspace_id']
            with pytest.raises(RuntimeScopeError): cold.chapter(COMPANY, other, b, c)
        cold_runtime = WorkspacePackageRuntime(Database(db.path), runtime.store_root)
        assert {r['workspace_id'] for r in cold_runtime.registry()} == {r['workspace_id'] for r in results}
        with db.connect() as con: assert con.execute('pragma foreign_key_check').fetchall() == []


@pytest.mark.parametrize('rename_fields', [False, True])
def test_multi_instance_update_rollback_reconcile_preserves_sibling(tmp_path, rename_fields):
    # Generic Package fixtures test existing lifecycle mechanics; Writing publication stays pinned.
    from backend.tests.test_workspace_package_runtime_p0 import _write_package
    from backend.tests.test_workspace_package_transactional_migration_p15 import _migration_package
    db, runtime = company_only(tmp_path)
    source = tmp_path / 'generic-v1'; _write_package(source)
    target = tmp_path / 'generic-v2'
    (_migration_package if rename_fields else _write_package)(target, version='0.2.0')
    with scope():
        package, stored = runtime.prepare_confirmed_assets(source)
        for index in range(2):
            with db.connect() as con:
                con.execute('begin immediate')
                runtime.install_confirmed_in_connection(con, package, stored, COMPANY,
                    department_id='writing-test-department', business_id=f'generic-business-{index}',
                    business_name=f'Generic fixture {index}', business_goal='', business_positioning='',
                    workspace_id=f'generic-workspace-{index}', workspace_name='Generic lifecycle fixture')
            runtime.create_object(f'generic-workspace-{index}', 'core.domain-object.create', 'FeedbackRecord',
                {'title': '受控机制测试', 'channel': 'MANUAL', 'summary': '受控机制测试保留独立业务数据', 'customerRef': f'customer-{index}', 'status': 'NEW'})
        def sibling_values():
            with db.connect() as con:
                return tuple(tuple(r) for r in con.execute("select * from workspace_package_instances where workspace_id='generic-workspace-1'")), tuple(tuple(r) for r in con.execute("select * from workspace_package_objects where workspace_id='generic-workspace-1'"))
        before = sibling_values()
        runtime.update('generic-workspace-0', target)
        assert sibling_values() == before
        runtime.rollback('generic-workspace-0')
        assert sibling_values() == before
        runtime.update('generic-workspace-0', target)
        runtime.update('generic-workspace-1', target)
        cold = WorkspacePackageRuntime(Database(db.path), runtime.store_root)
        assert len(cold.registry()) == 2
        cold.rollback('generic-workspace-0')
        assert cold.get_workspace('generic-workspace-1')['instance']['package_version'] == '0.2.0'
        cold.rollback('generic-workspace-1')
        assert {r['version'] for r in cold.registry()} == {'0.1.0'}
        with db.connect() as con:
            assert con.execute('pragma foreign_key_check').fetchall() == []
            assert con.execute('select count(*) from workspace_package_lifecycle_events').fetchone()[0] == 6


def test_shared_disabled_and_archived_references_last_uninstall(tmp_path):
    from pathlib import Path
    db, runtime, results = two_confirmed_businesses(tmp_path)
    with scope():
        ids = [r['workspace_id'] for r in results]
        stored = Path(runtime.get_workspace(ids[0])['package']['stored_path'])
        runtime.disable(ids[0]); assert stored.is_dir()
        runtime.disable(ids[1])
        with db.connect() as con: assert con.execute('select status from installed_workspace_packages').fetchone()[0] == 'DISABLED'
        before = database_values(db)
        runtime.uninstall(ids[0]); assert stored.is_dir()
        with pytest.raises(PackageConflictError, match='already uninstalled'): runtime.uninstall(ids[0])
        runtime.uninstall(ids[1]); assert not stored.exists()
        with db.connect() as con:
            assert con.execute('select status from installed_workspace_packages').fetchone()[0] == 'UNINSTALLED'
            assert {r[0] for r in con.execute('select status from workspace_package_instances')} == {'ARCHIVED'}
            assert con.execute('pragma foreign_key_check').fetchall() == []
        assert database_values(db)['workspace_package_objects'] == before['workspace_package_objects']


def test_cross_company_shared_assets_are_retained(tmp_path):
    db, runtime, results = two_confirmed_businesses(tmp_path)
    other = 'other-legitimate-company'
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse','other-ceo','Other company','active')", (other,))
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values ('other-department','selfuse',?,'writing-test-template','Other dept','TEST','active')", (other,))
    with scope(company_id=other, ceo_id='other-ceo'):
        package, target = runtime.prepare_confirmed_assets(ASSETS / 'writing_authoring')
        with db.connect() as con:
            con.execute('begin immediate')
            runtime.install_confirmed_in_connection(con, package, target, other,
                department_id='other-department', business_id='other-business', business_name='Other fixture',
                business_goal='', business_positioning='', workspace_id='other-workspace', workspace_name='Other writing')
    with scope():
        runtime.disable(results[0]['workspace_id']); runtime.uninstall(results[0]['workspace_id'])
        runtime.uninstall(results[1]['workspace_id'])
    with scope(company_id=other, ceo_id='other-ceo'):
        assert runtime.get_workspace('other-workspace')['instance']['status'] == 'ACTIVE'
        assert target.is_dir()
        runtime.create_object('other-workspace', 'core.domain-object.create', 'WritingBook', {'title': 'Other company still usable'})
        runtime.uninstall('other-workspace'); assert not target.exists()


@pytest.mark.parametrize('failure', ['move', 'commit'])
def test_uninstall_move_or_commit_failure_restores_rows_and_assets(tmp_path, monkeypatch, failure):
    from pathlib import Path
    import app.workspace_package_runtime as module
    db, runtime = company_only(tmp_path)
    with scope():
        result = materialize(FirstRunDelivery(db), runtime, *confirmed(db))['creation_result']
        w = result['workspace_id']; before = database_values(db)
        stored = Path(runtime.get_workspace(w)['package']['stored_path'])
        content = {str(p.relative_to(stored)): p.read_bytes() for p in stored.rglob('*') if p.is_file()}
        if failure == 'move':
            monkeypatch.setattr(module.os, 'replace', lambda *a: (_ for _ in ()).throw(OSError('injected move failure')))
        else:
            class CommitFailure:
                @contextmanager
                def connect(self):
                    with db.connect() as con:
                        yield con
                        raise RuntimeError('injected commit failure')
            runtime.db = CommitFailure()
        with pytest.raises((OSError, RuntimeError)): runtime.uninstall(w)
        assert database_values(db) == before
        assert {str(p.relative_to(stored)): p.read_bytes() for p in stored.rglob('*') if p.is_file()} == content
        with db.connect() as con: assert con.execute('pragma foreign_key_check').fetchall() == []


def test_uninstall_and_confirmed_creation_serialize_shared_resources(tmp_path, monkeypatch):
    import app.workspace_package_runtime as module
    from threading import Event
    db, runtime = company_only(tmp_path)
    with scope():
        result = materialize(FirstRunDelivery(db), runtime, *confirmed(db))['creation_result']
        second = confirmed(db, 'Racing second Business')
    moved, release = Event(), Event(); original = module.os.replace
    def controlled_move(source, target):
        original(source, target); moved.set()
        assert release.wait(5), 'test release timed out'
    monkeypatch.setattr(module.os, 'replace', controlled_move)
    def uninstall():
        with scope(): return runtime.uninstall(result['workspace_id'])
    def create():
        with scope(): return materialize(FirstRunDelivery(db), runtime, *second)
    with ThreadPoolExecutor(max_workers=2) as pool:
        uninstalling = pool.submit(uninstall)
        assert moved.wait(5)
        creating = pool.submit(create)
        release.set(); uninstalling.result(); creation = creating.result()
    # Last-reference uninstall won its write lock; activation cannot create an ACTIVE broken sibling.
    assert creation['activation']['status'] == 'FAILED', creation
    with db.connect() as con:
        assert con.execute("select count(*) from workspace_package_instances where status='ACTIVE'").fetchone()[0] == 0
        assert con.execute('pragma foreign_key_check').fetchall() == []


@pytest.mark.parametrize('operation', ['disable', 'uninstall'])
@pytest.mark.parametrize('identity', [{'tenant_id': 'foreign'}, {'company_id': 'foreign'}, {'ceo_id': 'foreign'}, {'role': 'employee'}])
def test_lifecycle_rejects_foreign_bound_identity_without_mutation(tmp_path, operation, identity):
    db, runtime, results = two_confirmed_businesses(tmp_path)
    before = database_values(db)
    with scope(**identity), pytest.raises(PackageScopeError): getattr(runtime, operation)(results[0]['workspace_id'])
    assert database_values(db) == before


@pytest.mark.parametrize('changed', ["'active'", "'AC TIVE'"])
def test_schema_literal_changes_are_unknown_not_formatting(tmp_path, changed):
    db = Database(str(tmp_path / 'literal.sqlite')); db.initialize()
    with db.connect() as con: con.executescript(PACKAGE_DDL.replace("'ACTIVE','DISABLED','ARCHIVED'", changed + ",'DISABLED','ARCHIVED'", 1))
    before = database_values(db)
    with pytest.raises(PackageConflictError, match='unknown parent schema'): migrate_only(db)
    assert database_values(db) == before


@pytest.mark.parametrize('phase, exit_code', [('immutable_before_db', 91), ('transaction_before_commit', 92), ('committed_before_response', 93)])
def test_physical_creation_crash_and_lost_response_preserve_original_confirmation(tmp_path, phase, exit_code):
    import subprocess, sys
    from dataclasses import asdict
    from pathlib import Path
    from app.workspace_package_runtime import validate_package
    db, runtime = company_only(tmp_path)
    with scope(): run, draft, proposal = confirmed(db, 'Physical process boundary fixture')
    payload = {'db': db.path, 'store': str(runtime.store_root), 'run': run, 'draft': asdict(draft),
               'proposal': proposal, 'phase': phase, 'code': exit_code}
    program = '''
import os,json,sys
from app.database import Database
from app.workspace_package_runtime import WorkspacePackageRuntime
from app.runtime.first_run_delivery import FirstRunDelivery,FirstGeneralWorkspaceDraft
from backend.tests.test_writing_entry_readiness import materialize,scope
p=json.loads(sys.argv[1]);db=Database(p['db'])
with scope():
 runtime=WorkspacePackageRuntime(db,p['store']);delivery=FirstRunDelivery(db)
 if p['phase']=='immutable_before_db':
  original=runtime.prepare_confirmed_assets
  def stop(*a,**k):
   original(*a,**k);os._exit(p['code'])
  runtime.prepare_confirmed_assets=stop
 elif p['phase']=='transaction_before_commit':
  original=runtime.install_confirmed_in_connection
  def stop(*a,**k):
   original(*a,**k);os._exit(p['code'])
  runtime.install_confirmed_in_connection=stop
 else:
  original=delivery.package_creation_status
  def stop(*a,**k):
   result=original(*a,**k)
   if result['activation']['status']=='COMPLETED':os._exit(p['code'])
   return result
  delivery.package_creation_status=stop
 materialize(delivery,runtime,p['run'],FirstGeneralWorkspaceDraft(**p['draft']),p['proposal'])
raise SystemExit('boundary was not reached')
'''
    child = subprocess.run([sys.executable, '-c', program, json.dumps(payload)], capture_output=True, text=True, timeout=15)
    assert child.returncode == exit_code, child.stderr + child.stdout
    with scope():
        cold_runtime = WorkspacePackageRuntime(Database(db.path), runtime.store_root)
        cold = FirstRunDelivery(Database(db.path))
        result = cold.package_creation_status(run, COMPANY, CEO)
        expected = 'COMPLETED' if phase == 'committed_before_response' else 'UNKNOWN'
        assert result['activation']['status'] == expected
        assert result['activation']['proposal_sha256'] == proposal['proposal_sha256']
        replay = materialize(cold, cold_runtime, run, draft, proposal, retry_no=1)
        assert replay['activation']['status'] == expected
        if expected == 'COMPLETED': assert replay['creation_result'] == result['creation_result']
        with pytest.raises(BusinessSpineError): materialize(cold, cold_runtime, run, replace(draft, goal='replacement'), proposal)
    with db.connect() as con:
        count = 1 if expected == 'COMPLETED' else 0
        for table in ('canonical_businesses', 'workspaces', 'workspace_package_instances'):
            assert con.execute('select count(*) from ' + table).fetchone()[0] == count
        assert con.execute("select count(*) from employee_instances where template_id='official.employee.writing.author'").fetchone()[0] == count
        assert con.execute("select count(*) from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchone()[0] == count * 2
        assert con.execute('pragma foreign_key_check').fetchall() == []
        assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'
    retained = list(Path(runtime.store_root).glob('*/*/*'))
    assert len(retained) == 1 and validate_package(retained[0])['digest'] == proposal['snapshot']['definition']['digest']

# B initial teams use real catalog/identity rows and the original confirmation transaction.
from app.employee_templates import EmployeeTemplateContract, professional_team_contract


def test_b_team_identity_no_key_edit_and_multiple_instances(tmp_path):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        first = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
        team = first['creation_result']['initial_team']
        assert team['leaderRef'] == team['employeeRef']
        assert len(team['assignments']) == 2
        assert team['templateRef'] == 'official.employee.writing.author'
        assert team['executionVerification'] == 'UNVERIFIED'
        assert WritingEntryService(db).metadata(COMPANY, team['workspaceRef'])['execution']['status'] == 'UNAVAILABLE'
        with db.connect() as con:
            employee = con.execute('select * from employee_instances where id=?', (team['employeeRef'],)).fetchone()
            assert employee['company_id'] == COMPANY and employee['name'] == '章节作者'
            runtime_employee = con.execute('select * from runtime_entities where entity_id=?', (team['employeeRef'],)).fetchone()
            assert json.loads(runtime_employee['data_json'])['companyEmployeeRef'] == employee['id']
            assert 'identityBridge' not in json.loads(runtime_employee['data_json'])
            assert runtime_employee['verification_status'] == 'UNVERIFIED'
            assert con.execute('select count(*) from employee_capability_bindings where employee_id=?', (employee['id'],)).fetchone()[0] == 0
            for index, ref in enumerate(team['assignments']):
                assignment = con.execute('select * from runtime_entities where entity_id=?', (ref['assignmentRef'],)).fetchone()
                data = json.loads(assignment['data_json'])
                assert data['employeeRef'] == employee['id'] and data['scopeType'] == ('BUSINESS' if index == 0 else 'WORKSPACE')
                assert data['scopeRef'] == (team['businessRef'] if index == 0 else team['workspaceRef'])
                assert data['isLeader'] is (index == 0)
                assert len(con.execute('select * from runtime_links where source_id=?', (ref['assignmentRef'],)).fetchall()) == 2
            assert WritingEntryService(db).assignments(con, COMPANY, team['workspaceRef'])[0]['data']['employeeRef'] == employee['id']
            con.execute("update employee_instances set name='用户改名',enabled=0 where id=?", (employee['id'],))
        repeated = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
        assert repeated['creation_result']['initial_team'] == team
        assert EmployeeTemplateContract(db).get_employee_instance(team['employeeRef'])['name'] == '用户改名'
        run2, draft2, proposal2 = confirmed(db, '第二项专业业务')
        second = materialize(FirstRunDelivery(db), runtime, run2, draft2, proposal2)['creation_result']['initial_team']
        assert second['employeeRef'] != team['employeeRef'] and second['businessRef'] != team['businessRef']
        from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
        ResponsibilityRoutingRuntime(db).update_assignment(team['assignments'][1]['assignmentRef'], employee_ref=second['employeeRef'])
        materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
        with db.connect() as con:
            assert WritingEntryService(db).assignments(con, COMPANY, team['workspaceRef'])[0]['data']['employeeRef'] == second['employeeRef']
        assert FirstRunDelivery(Database(db.path)).package_creation_status(run, COMPANY, CEO)['creation_result']['initial_team'] == team
    with db.connect() as con: assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'


@pytest.mark.parametrize('stage', ['template', 'employee', 'AI_EMPLOYEE', 'ROLE_SLOT', 'assignment', 'link', 'receipt'])
def test_b_team_every_stage_rolls_back_in_same_connection(tmp_path, monkeypatch, stage):
    db, runtime = company_only(tmp_path)
    with scope(): run, draft, proposal = confirmed(db)
    original = db.connect
    @contextmanager
    def injected():
        with original() as con:
            class Connection:
                def __getattr__(self, name): return getattr(con, name)
                def execute(self, sql, params=()):
                    hit = ((stage == 'template' and sql.startswith('insert or ignore into employee_templates'))
                           or (stage == 'employee' and sql.startswith('insert into employee_instances'))
                           or (stage in {'AI_EMPLOYEE', 'ROLE_SLOT'} and sql.startswith('insert into runtime_entities') and len(params) > 2 and params[2] == stage)
                           or (stage == 'assignment' and "'RESPONSIBILITY_ASSIGNMENT'" in sql and sql.startswith('insert'))
                           or (stage == 'link' and sql.startswith('insert into runtime_links'))
                           or (stage == 'receipt' and sql.startswith('update runtime_entities set company_id=')))
                    if hit: raise RuntimeError('team stage failure: ' + stage)
                    return con.execute(sql, params)
            yield Connection()
    monkeypatch.setattr(db, 'connect', injected)
    with scope(): result = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
    assert result['activation']['status'] == 'FAILED', result
    with original() as con:
        assert con.execute('select count(*) from canonical_businesses where business_id=?', (FirstRunDelivery(db)._ids(run)['business_id'],)).fetchone()[0] == 0
        assert con.execute("select count(*) from employee_instances where template_id='official.employee.writing.author'").fetchone()[0] == 0
        assert con.execute("select count(*) from employee_templates where id='official.employee.writing.author'").fetchone()[0] == 0
        assert con.execute("select count(*) from runtime_entities where entity_type in ('AI_EMPLOYEE','ROLE_SLOT','RESPONSIBILITY_ASSIGNMENT')").fetchone()[0] == 0
        assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'
    monkeypatch.setattr(db, 'connect', original)
    with scope():
        retried = materialize(FirstRunDelivery(db), runtime, run, draft, proposal, retry_no=1)
        assert retried['activation']['status'] == 'COMPLETED'
        assert retried['creation_result']['initial_team']['employeeRef']


def test_b_team_contract_tamper_catalog_conflict_and_legacy_no_backfill(tmp_path):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        bad = json.loads(json.dumps(proposal)); bad['snapshot']['definition']['initial_team_contract']['displayName'] = '历史人物'
        with pytest.raises(BusinessSpineError): materialize(FirstRunDelivery(db), runtime, run, draft, bad)
        with db.connect() as con:
            con.execute("insert into employee_templates(id,name,role,source,tenant_id) values ('official.employee.writing.author','冲突模板','研发','official','platform')")
        failed = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
        assert failed['activation']['status'] == 'FAILED'
        with db.connect() as con:
            assert con.execute("select name from employee_templates where id='official.employee.writing.author'").fetchone()[0] == '冲突模板'
            con.execute("delete from employee_templates where id='official.employee.writing.author'")
        done = materialize(FirstRunDelivery(db), runtime, run, draft, proposal, retry_no=1)
        with db.connect() as con:
            row = con.execute('select data_json from runtime_entities where entity_id=?', (run,)).fetchone()
            data = json.loads(row[0]); data.pop('initialTeam'); con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(data), run))
            count = con.execute('select count(*) from employee_instances').fetchone()[0]
        assert 'initial_team' not in FirstRunDelivery(db).package_creation_status(run, COMPANY, CEO)['creation_result']
        assert 'initial_team' not in materialize(FirstRunDelivery(db), runtime, run, draft, proposal)['creation_result']
        with db.connect() as con: assert con.execute('select count(*) from employee_instances').fetchone()[0] == count
        with scope(company_id='foreign', ceo_id='foreign'):
            with pytest.raises(BusinessSpineError): FirstRunDelivery(db).package_creation_status(run, 'foreign', 'foreign')


@pytest.mark.parametrize('kind,version,key,folder', [('cg','0.1.0','CONTENT_GRAPHIC_AUTHOR','content_growth'), ('cg','0.2.0','CONTENT_AUTHOR','content_growth_v02'), ('music','0.2.0','MUSIC_SONG_AUTHOR','music')])
def test_b_team_unpublished_candidate_fixture_preserves_ordinary_gate(tmp_path, monkeypatch, kind, version, key, folder):
    from app.content_growth_entry_service import ContentGrowthEntryService
    from app.music_entry_service import MusicEntryService
    db, runtime = company_only(tmp_path)
    with scope():
        service = ContentGrowthEntryService(db) if kind == 'cg' else MusicEntryService(db)
        # The installed definitions are now published. Exercise the unpublished gate
        # with an isolated read fixture instead of treating current publication as false.
        from pathlib import Path
        original_read = Path.read_text
        release_names = {"content_growth_release.json", "content_growth_v02_release.json", "music_release.json"}
        def unpublished(path, *args, **kwargs):
            value = original_read(path, *args, **kwargs)
            if path.parent == ASSETS and path.name in release_names:
                data = json.loads(value); data["published"] = False
                return json.dumps(data)
            return value
        monkeypatch.setattr(Path, "read_text", unpublished)
        with pytest.raises(ValueError): service.publication()
        definition = service.publication(candidate=True, **({'version': version} if kind == 'cg' else {}))
        assert definition['published'] is False and definition['initial_team_contract']['authorKey'] == key
        run, draft, proposal = confirmed(db)
        snapshot = proposal['snapshot']; snapshot.update(package_id=definition['package_id'], definition=definition)
        proposal['package_id'] = definition['package_id']
        proposal['proposal_sha256'] = __import__('hashlib').sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        with db.connect() as con:
            con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps({'v1Proposal': proposal}), run))
        # Internal isolated confirmation fixture, never an ordinary entry or publication decision.
        result = FirstRunDelivery(db).materialize_package_for_existing_company(run, draft, package_runtime=runtime,
            source=ASSETS / folder, definition=definition, department_id=proposal['department_id'], proposal_sha256=proposal['proposal_sha256'])
        assert result['activation']['status'] == 'COMPLETED', result
        team = result['creation_result']['initial_team']
        assert team['templateRef'] == ('official.employee.content_growth.author' if kind == 'cg' else 'official.employee.music.author')
        assert 'PUBLISHING' in team['coverage'] if kind == 'cg' else len(team['coverage']) == 4
        with db.connect() as con:
            author = json.loads(con.execute('select data_json from runtime_entities where entity_id=?', (team['assignments'][1]['assignmentRef'],)).fetchone()[0])
            assert author['responsibilityKey'] == key and not author['capabilityBindingRefs']
        with pytest.raises(ValueError): service.publication()


def test_b_team_missing_receipt_cannot_complete(tmp_path, monkeypatch):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        monkeypatch.setattr(EmployeeTemplateContract, 'materialize_professional_team_in_connection', lambda *a, **k: {'employeeRef': 'not-materialized'})
        assert materialize(FirstRunDelivery(db), runtime, run, draft, proposal)['activation']['status'] == 'FAILED'
        with db.connect() as con:
            assert con.execute('select count(*) from canonical_businesses').fetchone()[0] == 0


def test_b_team_true_legacy_completed_snapshot_without_contract_no_backfill(tmp_path):
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        proposal['snapshot']['definition'].pop('initial_team_contract')
        proposal['proposal_sha256'] = __import__('hashlib').sha256(json.dumps(proposal['snapshot'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        delivery = FirstRunDelivery(db); ids = delivery._ids(run)
        package, target = runtime.prepare_confirmed_assets(ASSETS / 'writing_authoring')
        with db.connect() as con:
            con.execute('begin immediate')
            runtime.install_confirmed_in_connection(con, package, target, COMPANY, department_id=proposal['department_id'],
                business_id=ids['business_id'], business_name=draft.business_name, business_goal=draft.goal, business_positioning=draft.positioning,
                workspace_id=ids['workspace_id'], workspace_name=draft.workspace_name)
            data = {'v1Proposal': proposal, 'firstBusiness': {**ids, 'department_id': proposal['department_id']},
                    'v1Activation': {'company_id': COMPANY, 'status': 'COMPLETED', 'proposal_sha256': proposal['proposal_sha256']}}
            con.execute("update runtime_entities set company_id=?,lifecycle_status='COMPANY_CREATED',data_json=? where entity_id=?", (COMPANY,json.dumps(data),run))
        assert 'initial_team' not in materialize(delivery, runtime, run, draft, proposal)['creation_result']
        assert 'initial_team' not in FirstRunDelivery(Database(db.path)).package_creation_status(run, COMPANY, CEO)['creation_result']
        with db.connect() as con:
            assert con.execute('select count(*) from employee_instances').fetchone()[0] == 0
            assert con.execute("select count(*) from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchone()[0] == 0


def test_b_team_legacy_music_metadata_does_not_inherit_current_contract(tmp_path):
    from pathlib import Path
    import shutil
    from app.music_entry_service import MusicEntryService, LEGACY_DIGEST
    db, runtime = company_only(tmp_path)
    source = Path(__file__).resolve().parent / 'fixtures/music_legacy'
    copy = tmp_path / 'legacy-music-assets'; shutil.copytree(source, copy)
    with scope():
        installed = runtime.install(copy, COMPANY, department_id='writing-test-department', business_id='legacy-music', business_name='隔离旧版音乐')
        entry = MusicEntryService(db)
        definition = entry.authoring_scope(COMPANY, installed['instance']['workspace_id'])['definition']
        assert definition['version'] == '0.1.0' and definition['digest'] == LEGACY_DIGEST
        assert definition['published'] is False and 'initial_team_contract' not in definition
        assert entry.publication(candidate=True)['initial_team_contract']['packageVersion'] == '0.2.0'
        assert entry.publication()['published'] is True  # Current publication never promotes the legacy instance.
        with db.connect() as con:
            assert con.execute('select count(*) from employee_instances').fetchone()[0] == 0


def test_multiline_goal_materializes_same_confirmed_bytes_and_strict_names(tmp_path):
    db,runtime=company_only(tmp_path)
    goal="写原创章节\n保留第二行目标"
    with scope():
        run,draft,proposal=confirmed(db,goal=goal)
        delivery=FirstRunDelivery(db)
        result=materialize(delivery,runtime,run,draft,proposal)
        assert materialize(delivery,runtime,run,draft,proposal)==result
        with db.connect() as con:
            row=con.execute("select goal from canonical_businesses where company_id=?",(COMPANY,)).fetchone()
            assert row[0]==goal
        assert proposal['goal']==goal
    for bad in [' ', '目标\x00坏', '目标\t坏', '目标\r坏', '目标\x7f坏']:
        with pytest.raises(BusinessSpineError):FirstRunDelivery._goal(bad)
    with pytest.raises(BusinessSpineError):FirstRunDelivery._clean('公司\n名称','Company name')


def test_actual_http_route_dtos_for_compiled_consumers(tmp_path, monkeypatch):
    """Persist unmodified current in-process HTTP DTOs only when explicitly requested."""
    import os
    from pathlib import Path
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.api.runtime_foundation_router import build_runtime_foundation_router
    from app.api.frontend_v1_router import build_frontend_v1_router
    from app.api.writing_router import build_writing_router
    db, _ = company_only(tmp_path)
    monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE', str(tmp_path / 'http-packages'))
    app = FastAPI()
    app.include_router(build_runtime_foundation_router(db))
    app.include_router(build_frontend_v1_router(db))
    app.include_router(build_writing_router(db, None, entry_service=WritingEntryService(db)))
    runtime = '/api/workspace/runtime/foundation'
    v1 = '/api/workspace/v1'
    dto = {}
    with scope(), TestClient(app) as client:
        def call(method, path, data=None):
            response = client.request(method, path, json=data) if data is not None else client.request(method, path)
            assert response.status_code in (200, 201), (path, response.status_code, response.text)
            return response.json()
        def create(run, proposal):
            fields = {k: proposal[k] for k in ('business_name','goal','positioning','workspace_name','package_id','department_id','proposal_sha256')}
            return call('POST', f'{v1}/companies/{COMPANY}/founding-runs/{run}/business', {**fields,'ceo_id':CEO,'intent_summary':proposal['intent'],'retry_no':0})
        run, _, proposal = confirmed(db)
        created = create(run, proposal)
        assert created['activation']['status'] == 'COMPLETED'
        dto['founding_get'] = call('GET', f'{runtime}/founding-runs/{run}')
        dto['draft_get'] = call('GET', f'{v1}/founding-runs/{run}/business-draft')
        dto['business_result'] = call('GET', f'{v1}/companies/{COMPANY}/founding-runs/{run}/business-result')
        dto['organization'] = call('GET', f'{runtime}/companies/{COMPANY}/organization')
        w = created['creation_result']['workspace_id']
        dto['writing_entry'] = call('GET', f'{v1}/companies/{COMPANY}/writing/{w}/entry')
        dto['definitions'] = call('GET', f'{v1}/companies/{COMPANY}/business-definitions')
        dto['new_run'] = call('POST', f'{runtime}/founding-runs', {'owner_ref':CEO,'intent_ref':'businessCreation','org_version':'org-v1','blueprint_version':''})
        pending = dto['new_run']['entity_id']
        for target, trigger in [('INTENT_CAPTURED','capture_intent'),('CLARIFYING','request_clarification'),('PROPOSED','propose_company')]:
            dto['transition_'+target] = call('POST', f'{runtime}/entities/{pending}/transition', {'target':target,'actor':'CEO','trigger':trigger,'reason':'受控人工入口','evidenceRefs':[],'context':{}})
        values = {'company_id':COMPANY,'intent':'受控写作入口','business_name':'第二项完整写作','goal':'第一行目标\n第二行保持原字节','positioning':'原创','workspace_name':'第二写作空间','package_id':proposal['package_id'],'department_id':proposal['department_id']}
        dto['saved_pending'] = call('PUT', f'{v1}/founding-runs/{pending}/business-draft', values)
        dto['pending_get'] = call('GET', f'{runtime}/founding-runs/{pending}')
        dto['pending_draft'] = call('GET', f'{v1}/founding-runs/{pending}/business-draft')
        dto['pending_organization'] = call('GET', f'{runtime}/companies/{COMPANY}/organization')
        dto['confirmed_transition'] = call('POST', f'{runtime}/entities/{pending}/transition', {'target':'CEO_CONFIRMED','actor':'CEO','trigger':'confirm_company','reason':'明确确认原提案','evidenceRefs':[],'context':{}})
        dto['new_created'] = create(pending, dto['pending_draft']['proposal'])
        assert dto['new_created']['activation']['status'] == 'COMPLETED'
        assert 'data' not in dto['confirmed_transition']
    destination = os.getenv('CURIS_TEST_ROUTE_DTO_PATH')
    if destination:
        with Path(destination).open('x', encoding='utf-8') as output:
            json.dump({'responses':dto}, output, ensure_ascii=False, indent=2)


def test_confirmed_assets_concurrent_publish_never_reads_partial_target(tmp_path, monkeypatch):
    """Second producer finishes while the first has only created its private directory."""
    from threading import Event
    from pathlib import Path
    import app.workspace_package_runtime as module
    db, runtime = company_only(tmp_path)
    source = ASSETS / 'writing_authoring'
    partial, second_done = Event(), Event()
    copytree = module.shutil.copytree
    def controlled_copy(origin, destination, *args, **kwargs):
        if Path(origin) == source and not partial.is_set():
            Path(destination).mkdir(exist_ok=True)
            partial.set()
            assert second_done.wait(10), 'second producer failed to reach the publication boundary'
            return copytree(origin, destination, *args, **{**kwargs, 'dirs_exist_ok': True})
        return copytree(origin, destination, *args, **kwargs)
    monkeypatch.setattr(module.shutil, 'copytree', controlled_copy)
    def first():
        with scope(): return runtime.prepare_confirmed_assets(source)
    def second():
        try:
            with scope(): return runtime.prepare_confirmed_assets(source)
        finally: second_done.set()
    with ThreadPoolExecutor(max_workers=2) as pool:
        one = pool.submit(first)
        assert partial.wait(10)
        two = pool.submit(second)
        results = [one.result(), two.result()]
    assert results[0][1] == results[1][1]
    assert module.validate_package(results[0][1])['digest'] == results[0][0]['digest']
    assert not list(results[0][1].parent.glob('.*.staging'))


def test_confirmed_assets_never_overwrites_unknown_existing_target(tmp_path):
    import app.workspace_package_runtime as module
    db, runtime = company_only(tmp_path)
    source = ASSETS / 'writing_authoring'
    package = module.validate_package(source)
    target = runtime.store_root / package['manifest']['packageId'] / package['manifest']['version'] / package['digest']
    target.mkdir(parents=True)
    marker = target / 'manifest.json'
    marker.write_text('{not-complete', encoding='utf-8')
    foreign = target.parent / '.foreign.staging'; foreign.mkdir(); (foreign / 'keep').write_text('other producer', encoding='utf-8')
    with scope(), pytest.raises((module.PackageValidationError, module.PackageConflictError)):
        runtime.prepare_confirmed_assets(source)
    assert marker.read_text() == '{not-complete'
    assert (foreign / 'keep').read_text() == 'other producer'
