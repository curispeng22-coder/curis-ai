"""T-007 isolated identity/contract tests; synthetic assets imply no package/model acceptance."""
import json
import re
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.database import Database
from app.employee_templates import EmployeeTemplateContract, PROFESSIONAL_TEAM_PACKAGES, professional_team_contract
from app.runtime import RuntimeFoundation
from app.runtime.first_run_delivery import FirstRunDelivery, FirstGeneralWorkspaceDraft
from app.tenant_context import TenantContext
from app.workspace_package_runtime import WorkspacePackageRuntime

COMPANY, CEO = 't007-company', 't007-owner'


def scope():
    return TenantContext.scope(tenant_id='selfuse', company_id=COMPANY, ceo_id=CEO, role='ceo')


def fixture(tmp_path, monkeypatch, kind='writing'):
    db = Database(str(tmp_path / 'preset.sqlite'))
    db.initialize()
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse',?,'示例数据','active')", (COMPANY, CEO))
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) values ('t007-dept','selfuse',?,'test','示例数据','TEST','active')", (COMPANY,))
    runtime = WorkspacePackageRuntime(db, tmp_path / 'store')
    (package_id, version), (_, _, digest) = next((key, val) for key, val in PROFESSIONAL_TEAM_PACKAGES.items() if val[0] == kind)
    contract = professional_team_contract(package_id, version, digest)
    definition = dict(package_id=package_id, version=version, digest=digest, initial_team_contract=contract)
    package = dict(manifest={'packageId': package_id, 'version': version, 'schemaVersion': '1', 'workspace': {'name': '示例数据'}},
                   digest=digest, surfaces={}, schemas={}, root=tmp_path)
    # Only immutable asset preparation is substituted. All scope, SQL, routing,
    # receipt validation, transitions, rollback and repeat handling are production code.
    monkeypatch.setattr(runtime, 'prepare_confirmed_assets', lambda source: (package, tmp_path))
    draft = FirstGeneralWorkspaceDraft(COMPANY, CEO, '示例数据', '示例数据', '示例业务', '完成一篇示例文稿', '示例定位', '示例空间', intent_summary='示例需求')
    snapshot = dict(intent=draft.intent_summary, business_name=draft.business_name, goal=draft.goal,
                    positioning=draft.positioning, workspace_name=draft.workspace_name,
                    company_id=COMPANY, department_id='t007-dept', package_id=package_id, definition=definition)
    foundation = RuntimeFoundation(db)
    foundation.create('CEO_ASSISTANT', company_id=COMPANY, owner_ref=CEO, data={'name': '示例数据'})
    run = foundation.create('FOUNDING_RUN', owner_ref=CEO, lifecycle_status='PROPOSED',
                            data={'v1Proposal': {'snapshot': snapshot, 'proposal_sha256': 't007-proposal'}})
    foundation.transition(run['entity_id'], 'CEO_CONFIRMED', actor='CEO', trigger='confirm_company')
    def materialize():
        return FirstRunDelivery(db).materialize_package_for_existing_company(run['entity_id'], draft,
            package_runtime=runtime, source=tmp_path, definition=definition, department_id='t007-dept', proposal_sha256='t007-proposal')
    return db, contract, materialize


def team(result):
    assert result['activation']['status'] == 'COMPLETED', result['activation']
    return result['creation_result']['initial_team']


def test_three_presets_concurrent_start_repeat_and_cold_read(tmp_path, monkeypatch):
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch)
    def invoke(_):
        with scope():
            return team(create())
    with ThreadPoolExecutor(max_workers=2) as pool:
        first, repeated = list(pool.map(invoke, range(2)))
    assert first == repeated
    assert len({first['leaderRef'], first['employeeRef'], first['reviewerRef']}) == 3
    with scope():
        assert team(create()) == first
        with db.connect() as con:
            rows = con.execute("select name from employee_instances where company_id=? order by name", (COMPANY,)).fetchall()
            assert {r[0] for r in rows} == {'主编', '作者', '编辑'}
            assert len(rows) == 3
            state = EmployeeTemplateContract(db).professional_team_state_in_connection(con, company_id=COMPANY,
                business_id=first['businessRef'], workspace_id=first['workspaceRef'], contract=contract)
            assert state['team']['employeeRef'] == first['employeeRef']
            assert len(state['team']['companyEmployeeRefs']) == 3
            keys = [json.loads(con.execute('select data_json from runtime_entities where entity_id=?', (a['assignmentRef'],)).fetchone()[0])['responsibilityKey'] for a in first['assignments']]
            assert keys == ['WRITING_CHIEF_EDITOR', 'WRITING_CHAPTER_AUTHOR', 'WRITING_REVIEWER']
            assert con.execute('select count(*) from employee_capability_bindings').fetchone()[0] == 0
            assert con.execute('pragma foreign_key_check').fetchall() == []
        cold = FirstRunDelivery(Database(db.path)).package_creation_status(first_run_id(db), COMPANY, CEO)
        assert cold['creation_result']['initial_team'] == first


def first_run_id(db):
    with db.connect() as con:
        return con.execute("select entity_id from runtime_entities where entity_type='FOUNDING_RUN'").fetchone()[0]


@pytest.mark.parametrize('kind', ['content_growth', 'music'])
def test_nonwriting_keeps_one_employee_two_responsibilities_and_repeat(tmp_path, monkeypatch, kind):
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch, kind)
        first = team(create())
        assert team(create()) == first
        assert first['leaderRef'] == first['employeeRef']
        assert 'reviewerRef' not in first
        assert len(first['assignments']) == 2
        with db.connect() as con:
            assert con.execute('select count(*) from employee_instances where company_id=?', (COMPANY,)).fetchone()[0] == 1
            state = EmployeeTemplateContract(db).professional_team_state_in_connection(con, company_id=COMPANY,
                business_id=first['businessRef'], workspace_id=first['workspaceRef'], contract=contract)
            assert state['team']['employeeRef'] == first['employeeRef']
            for i, ref in enumerate(first['assignments']):
                data = json.loads(con.execute('select data_json from runtime_entities where entity_id=?', (ref['assignmentRef'],)).fetchone()[0])
                assert data['responsibilityKey'] == contract['leaderKey' if i == 0 else 'authorKey']
                assert data['inputContract'] == {}
                assert data['outputContract'] == ({} if i == 0 else {'coverage': contract['coverage'], 'independentReview': False})


def test_verbatim_presets_persist_and_read_without_source_files(tmp_path, monkeypatch):
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch)
        created = team(create())
        with db.connect() as con:
            for index, employee in enumerate(contract["members"]):
                doc = employee["description"]
                instructions = re.search(r'```text\n(.*?)\n```', doc, re.S)[1]
                schema = json.loads(re.search(r'## 输出格式\n\n```json\n(.*?)\n```', doc, re.S)[1])
                template = con.execute('select * from employee_templates where id=?', (employee['templateId'],)).fetchone()
                assert template['default_instructions'] == instructions
                assert template['description'] == doc
                ref = [created['leaderRef'], created['employeeRef'], created['reviewerRef']][index]
                instance = EmployeeTemplateContract(Database(db.path)).get_employee_instance(ref)
                assert instructions in instance['instructions_override']
                assert doc in instance['instructions_override']
                assert contract['collaboration'] in instance['instructions_override']
                data = json.loads(con.execute('select data_json from runtime_entities where entity_id=?', (created['assignments'][index]['assignmentRef'],)).fetchone()[0])
                assert data['outputContract'] == {**employee['outputContract'], 'schema': schema}
                assert data['inputContract']['required'] == employee['inputContract']['required']
                assert data['inputContract']['optional'] == employee['inputContract']['optional']
                assert data['inputContract']['documentation'] in doc
                # All three presets participate in existing scoped permission context,
                # without acquiring execution capability.
                row = con.execute('select * from employee_instances where id=?', (ref,)).fetchone()
                assert EmployeeTemplateContract(db)._professional_execution_context(con, row)
        # Returned contracts must not permit mutation of the approved definition.
        contract['members'][0]['defaultInstructions'] = 'tampered'
        fresh = professional_team_contract(contract['packageId'], contract['packageVersion'], contract['packageDigest'])
        assert fresh['members'][0]['defaultInstructions'] != 'tampered'


@pytest.mark.parametrize('field', ['default_instructions', 'description', 'default_tool'])
def test_conflicting_template_rolls_back_whole_team(tmp_path, monkeypatch, field):
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch)
        member = contract['members'][0]
        with db.connect() as con:
            con.execute('insert into employee_templates(id,slug,name,role,responsibility,department_type,source,tenant_id,default_instructions,description) values (?,?,?,?,?,?,?, ?,?,?)',
                (member['templateId'], member['templateId'].removeprefix('official.employee.'), member['name'], member['name'], member['responsibility'], 'writing', 'official', 'platform', member['defaultInstructions'], member['description']))
            con.execute(f'update employee_templates set {field}=? where id=?', ('tampered', member['templateId']))
        result = create()
        assert result['activation']['status'] == 'FAILED'
        assert 'conflicts with the approved catalog' in result['activation']['reason']
        with db.connect() as con:
            for table in ('canonical_businesses', 'workspaces', 'workspace_package_instances', 'employee_instances'):
                assert con.execute('select count(*) from ' + table).fetchone()[0] == 0
            assert con.execute('select ' + field + ' from employee_templates where id=?', (member['templateId'],)).fetchone()[0] == 'tampered'


@pytest.mark.parametrize('stage', ['template', 'employee', 'AI_EMPLOYEE', 'ROLE_SLOT', 'assignment', 'link', 'receipt'])
def test_every_team_stage_rolls_back_in_callers_transaction(tmp_path, monkeypatch, stage):
    from contextlib import contextmanager
    with scope():
        db, _, create = fixture(tmp_path, monkeypatch)
        original = db.connect
        @contextmanager
        def injected():
            with original() as con:
                class Connection:
                    def __getattr__(self, name):
                        return getattr(con, name)
                    def execute(self, sql, params=()):
                        hit = ((stage == 'template' and sql.startswith('insert or ignore into employee_templates'))
                               or (stage == 'employee' and sql.startswith('insert into employee_instances'))
                               or (stage in {'AI_EMPLOYEE', 'ROLE_SLOT'} and sql.startswith('insert into runtime_entities') and len(params) > 2 and params[2] == stage)
                               or (stage == 'assignment' and "'RESPONSIBILITY_ASSIGNMENT'" in sql and sql.startswith('insert'))
                               or (stage == 'link' and sql.startswith('insert into runtime_links'))
                               or (stage == 'receipt' and sql.startswith('update runtime_entities set company_id=')))
                        if hit:
                            raise RuntimeError('t007 injected ' + stage)
                        return con.execute(sql, params)
                yield Connection()
        monkeypatch.setattr(db, 'connect', injected)
        result = create()
        assert result['activation']['status'] == 'FAILED'
        assert result['activation']['reason'] == 't007 injected ' + stage
        with original() as con:
            for table in ('canonical_businesses', 'workspaces', 'workspace_package_instances', 'employee_instances'):
                assert con.execute('select count(*) from ' + table).fetchone()[0] == 0
            assert con.execute("select count(*) from employee_templates where id like 'official.employee.writing.%'").fetchone()[0] == 0
            assert con.execute("select count(*) from runtime_entities where entity_type in ('AI_EMPLOYEE','ROLE_SLOT','RESPONSIBILITY_ASSIGNMENT')").fetchone()[0] == 0
            assert con.execute('pragma integrity_check').fetchone()[0] == 'ok'


@pytest.mark.parametrize('index', [0, 1, 2])
def test_any_disabled_member_blocks_readiness_without_backfill(tmp_path, monkeypatch, index):
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch)
        first = team(create())
        ref = [first['leaderRef'], first['employeeRef'], first['reviewerRef']][index]
        with db.connect() as con:
            con.execute('update employee_instances set enabled=0 where id=?', (ref,))
        assert team(create()) == first
        with db.connect() as con:
            with pytest.raises(ValueError, match='no available canonical'):
                EmployeeTemplateContract(db).professional_team_state_in_connection(con, company_id=COMPANY,
                    business_id=first['businessRef'], workspace_id=first['workspaceRef'], contract=contract)
            assert con.execute('select count(*) from employee_instances where company_id=?', (COMPANY,)).fetchone()[0] == 3


def test_manual_author_assignment_stores_same_input_and_schema(tmp_path, monkeypatch):
    from app.writing_entry_service import WritingEntryService
    with scope():
        db, contract, create = fixture(tmp_path, monkeypatch)
        first = team(create())
        author_assignment = first['assignments'][1]['assignmentRef']
        with db.connect() as con:
            con.execute('delete from runtime_links where source_id=?', (author_assignment,))
            con.execute('delete from runtime_entities where entity_id=?', (author_assignment,))
        entry = WritingEntryService(db)
        monkeypatch.setattr(entry, 'publication', lambda: {'initial_team_contract': contract})
        # Focus the existing empty-slot assignment branch, without package assets
        # or model metadata. The assignment service and identity reads stay real.
        monkeypatch.setattr(entry, '_configure', lambda company, workspace, operation: operation())
        entry.assign(COMPANY, first['workspaceRef'], first['employeeRef'], 0)
        with db.connect() as con:
            assigned = entry.assignments(con, COMPANY, first['workspaceRef'])
        assert len(assigned) == 1
        assert assigned[0]['data']['inputContract'] == contract['members'][1]['inputContract']
        assert assigned[0]['data']['outputContract'] == contract['members'][1]['outputContract']


@pytest.mark.parametrize('key', ['leaderRef', 'reviewerRef'])
def test_receipt_cannot_alias_distinct_writing_members(tmp_path, monkeypatch, key):
    with scope():
        db, _, create = fixture(tmp_path, monkeypatch)
        original = EmployeeTemplateContract.materialize_professional_team_in_connection
        def alias(self, *args, **kwargs):
            result = original(self, *args, **kwargs)
            result[key] = result['employeeRef']
            return result
        monkeypatch.setattr(EmployeeTemplateContract, 'materialize_professional_team_in_connection', alias)
        result = create()
        assert result['activation']['status'] == 'FAILED'
        assert result['activation']['reason'] == 'Initial team receipt is not fully materialized'
        with db.connect() as con:
            assert con.execute('select count(*) from employee_instances where company_id=?', (COMPANY,)).fetchone()[0] == 0
            assert con.execute('select count(*) from canonical_businesses').fetchone()[0] == 0
