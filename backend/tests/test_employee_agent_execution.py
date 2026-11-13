"""Self-made offline resources only; no Agent, browser, provider or product database."""
from pathlib import Path

import pytest

from app.agent_work_resources import AgentWorkResources, require_browser_boundary
from app.skill_package import inspect_package, install_package, digest
from test_skill_package import archive, REPO, COMMIT


def test_local_agent_registration_binding_preserves_scope_and_never_executes(tmp_path, monkeypatch):
    """Run the actual registration closure and canonical binding service, not App startup."""
    import ast
    import json
    from types import SimpleNamespace
    from fastapi import HTTPException
    from app.tenant_context import TenantContext
    from app.employee_templates import EmployeeTemplateContract
    import app.ai_capability_registry as registry
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    db, _, _ = _seed(tmp_path / "local-add.sqlite")
    executable = tmp_path / "codex"
    executable.write_bytes(b"synthetic; no execution")
    executable.chmod(0o700)
    monkeypatch.setattr(registry.shutil, "which", lambda name: str(executable) if name == "codex" else None)
    monkeypatch.setattr(registry, "AGENT_ADAPTER_REGISTRY", {"codex": registry.AGENT_ADAPTER_REGISTRY["codex"]})
    monkeypatch.setattr(registry.subprocess, "run", lambda *_a, **_k: pytest.fail("Agent started"))
    source = ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())
    handler = next(node for node in ast.walk(source) if isinstance(node, ast.FunctionDef)
                   and node.name == "create_workspace_private_capability")
    handler.decorator_list = []
    namespace = {"__name__": "app.main", "__package__": "app", "PrivateCapabilityIn": object, "HTTPException": HTTPException, "database": db,
                 "TenantContext": TenantContext, "json": json,
                 "_reject_secret_like_metadata": lambda **_kwargs: None}
    exec(compile(ast.Module(body=[handler], type_ignores=[]), "<actual-private-registration-closure>", "exec"), namespace)
    register = namespace[handler.name]
    item = registry.discover_local_agents()[0]
    payload = SimpleNamespace(capability_type="agent", capability_id=item["capability_id"],
                              display_name="Synthetic Codex", metadata={"local_agent_ref": item["discovery_ref"], "execution_ready": True})
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        first = register(payload)
        assert register(payload) == first
        assert first["metadata"]["execution_ready"] is False
        payload.display_name = "conflicting name"
        with pytest.raises(HTTPException) as conflict: register(payload)
        assert conflict.value.status_code == 409
        assert db.get_tenant_private_capability(TENANT, "agent", item["capability_id"])["display_name"] == "Synthetic Codex"
        db.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id="agent.codex")
        with db.connect() as con:
            con.execute("update employee_instances set allowed_effect_classes_json=? where tenant_id=? and id=?",
                        (json.dumps(["exec"]), TENANT, COMPANY_EMPLOYEE))
        employees = EmployeeTemplateContract(db)
        before = employees.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"]
        employees.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, item["capability_id"])
        after = employees.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"]
        assert any(row["id"] == BINDING for row in after)
        assert len([row for row in after if row["capability_id"] == item["capability_id"]]) == 1
        application = tmp_path / "WorkBuddy.app"
        from test_ai_capability_registry import _synthetic_app
        _synthetic_app(application)
        registry.AGENT_ADAPTER_REGISTRY["workbuddy"] = {
            "name": "Synthetic WorkBuddy", "commands": [], "applications": [str(application)],
            "adapter_readiness": "UNVERIFIED"}
        unverified = next(row for row in registry.discover_local_agents() if row["agent_id"] == "workbuddy")
        saved = register(SimpleNamespace(capability_type="agent", capability_id=unverified["capability_id"],
                         display_name="Synthetic WorkBuddy", metadata={"local_agent_ref": unverified["discovery_ref"]}))
        assert saved["status"] == "inactive" and saved["metadata"]["execution_ready"] is False
        with pytest.raises(ValueError, match="not available"):
            employees.set_employee_capability_bindings(COMPANY_EMPLOYEE, [*after, {
                "capability_source": "tenant_private", "capability_type": "agent", "capability_id": unverified["capability_id"]}])
        assert employees.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"] == after
    with TenantContext.scope("foreign-tenant", role="test"):
        with pytest.raises(ValueError): employees.list_employee_capability_bindings(COMPANY_EMPLOYEE)
        assert db.get_tenant_private_capability("foreign-tenant", "agent", item["capability_id"]) is None


def test_atomic_agent_add_preserves_interleaved_edits_and_disabled_binding(tmp_path):
    import json
    from app.tenant_context import TenantContext
    from app.employee_templates import EmployeeTemplateContract
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    db, _, _ = _seed(tmp_path / "atomic-add.sqlite")
    service = EmployeeTemplateContract(db)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        for key in ("agent.codex", "agent.new", "agent.concurrent"):
            db.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id=key)
        with db.connect() as connection:
            connection.execute("update employee_instances set allowed_effect_classes_json=? where tenant_id=? and id=?",
                (json.dumps(["exec"]), TENANT, COMPANY_EMPLOYEE))
        # Window A read before window B adds and removes unrelated bindings.
        stale = service.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"]
        assert stale[0]["id"] == BINDING
        service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.concurrent")
        with db.connect() as connection:
            connection.execute("delete from employee_capability_bindings where tenant_id=? and id=?", (TENANT, BINDING))
        result = service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.new")
        assert {item["capability_id"] for item in result["bindings"]} == {"agent.concurrent", "agent.new"}
        assert service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.new")["bindings"] == result["bindings"]
        with pytest.raises(ValueError, match="company"):
            service.add_employee_agent_binding(COMPANY_EMPLOYEE, "foreign-company", "agent.codex")
        with db.connect() as connection:
            connection.execute("update employee_capability_bindings set enabled=0 where tenant_id=? and employee_id=? "
                "and capability_id='agent.new'", (TENANT, COMPANY_EMPLOYEE))
        with pytest.raises(ValueError, match="禁用"):
            service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.new")
        current = service.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"]
        assert next(item for item in current if item["capability_id"] == "agent.new")["enabled"] is False
        with db.connect() as connection:
            connection.execute("update employee_instances set allowed_effect_classes_json='[]' where tenant_id=? and id=?",
                (TENANT, COMPANY_EMPLOYEE))
        with pytest.raises(ValueError, match="authorized"):
            service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.codex")
        assert service.list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"] == current
    with TenantContext.scope("foreign-tenant", role="test"):
        with pytest.raises(ValueError): service.add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, "agent.new")


def test_atomic_agent_add_serializes_two_simultaneous_writers(tmp_path):
    import json
    import threading
    from app.tenant_context import TenantContext
    from app.employee_templates import EmployeeTemplateContract
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    db, _, _ = _seed(tmp_path / "simultaneous-add.sqlite")
    for key in ("agent.codex", "agent.one", "agent.two"):
        db.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id=key)
    with db.connect() as connection:
        connection.execute("update employee_instances set allowed_effect_classes_json=? where tenant_id=? and id=?",
            (json.dumps(["exec"]), TENANT, COMPANY_EMPLOYEE))
    barrier = threading.Barrier(2)
    errors = []
    def writer(key):
        try:
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
                barrier.wait(timeout=5)
                EmployeeTemplateContract(db).add_employee_agent_binding(COMPANY_EMPLOYEE, COMPANY, key)
        except Exception as error: errors.append(error)
    threads = [threading.Thread(target=writer, args=(key,)) for key in ("agent.one", "agent.two")]
    for thread in threads: thread.start()
    for thread in threads: thread.join(timeout=10)
    assert not any(thread.is_alive() for thread in threads)
    assert not errors
    with TenantContext.scope(TENANT, role="test"):
        bindings = EmployeeTemplateContract(db).list_employee_capability_bindings(COMPANY_EMPLOYEE)["bindings"]
        assert {item["capability_id"] for item in bindings} == {"agent.codex", "agent.one", "agent.two"}


def test_atomic_agent_binding_handler_passes_explicit_company_and_maps_rejection():
    import ast
    from types import SimpleNamespace
    from fastapi import HTTPException
    tree = ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())
    handler = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
                   and node.name == "add_workspace_employee_agent_binding")
    handler.decorator_list = []
    calls = []
    def add(*args):
        calls.append(args)
        if args[1] == "foreign": raise ValueError("company mismatch")
        return {"employee_id": args[0]}
    namespace = {"EmployeeAgentBindingAddIn": object, "HTTPException": HTTPException,
                 "employee_template_contract": SimpleNamespace(add_employee_agent_binding=add)}
    exec(compile(ast.Module(body=[handler], type_ignores=[]), "<actual-atomic-add-handler>", "exec"), namespace)
    assert namespace[handler.name]("employee", SimpleNamespace(company_id="company", capability_id="agent")) == {"employee_id": "employee"}
    assert calls == [("employee", "company", "agent")]
    with pytest.raises(HTTPException) as error:
        namespace[handler.name]("employee", SimpleNamespace(company_id="foreign", capability_id="agent"))
    assert error.value.status_code == 422


@pytest.mark.parametrize('kind,ids', [
    ('content-growth', {'content_ref': 'synthetic-content'}),
    ('music', {'song_ref': 'synthetic-song'}),
    ('writing', {'book_ref': 'synthetic-book', 'chapter_ref': 'synthetic-chapter'}),
])
def test_pending_origin_projection_checks_snapshot_scope_and_only_returns_ids(kind, ids):
    from copy import deepcopy
    from app.api.team_operating_router import _verified_origin_projection
    work = {'company_id': 'company', 'workspace_id': 'workspace',
            'data': {'responsibilityAssignmentRef': 'assignment'}}
    scope = {'tenant_id': 'tenant', 'company_id': 'company', 'workspace_id': 'workspace'}
    snapshot = {'kind': kind, 'context': {**scope, 'assignment_ref': 'assignment'},
                'scope': {**scope, **(ids if kind == 'writing' else {})},
                **(ids if kind != 'writing' else {}), 'private': 'SYNTHETIC_SECRET'}
    contract = {'agentSource': {'input': {'kind': kind, **ids, 'text': 'SYNTHETIC_SECRET'}, 'snapshot': snapshot}}
    expected = {'status': 'VERIFIED', 'assignment_ref': 'assignment', 'source': {'kind': kind, **ids}}
    assert _verified_origin_projection(work, contract, 'tenant') == expected
    for mutate in ('tenant', 'company', 'workspace', 'assignment', 'kind', 'source_id', 'snapshot_id'):
        changed_work, changed = deepcopy(work), deepcopy(contract)
        snap = changed['agentSource']['snapshot']
        if mutate in ('tenant', 'company', 'workspace'):
            snap['context'][mutate + '_id'] = 'foreign'
        elif mutate == 'assignment': changed_work['data']['responsibilityAssignmentRef'] = 'foreign'
        elif mutate == 'kind': snap['kind'] = 'foreign'
        elif mutate == 'source_id': changed['agentSource']['input'][next(iter(ids))] = 'foreign'
        else: (snap['scope'] if kind == 'writing' else snap)[next(iter(ids))] = 'foreign'
        assert _verified_origin_projection(changed_work, changed, 'tenant') == {'status': 'UNKNOWN'}
    assert _verified_origin_projection(work, {}, 'tenant') == {'status': 'UNKNOWN'}
    assert 'SYNTHETIC_SECRET' not in str(expected)


def test_pending_origin_projection_references_bind_conversation_without_references():
    from app.api.team_operating_router import _verified_origin_projection
    work = {'company_id': 'company', 'workspace_id': 'workspace', 'data': {'responsibilityAssignmentRef': 'assignment'}}
    snapshot = {'kind': 'references', 'conversation_id': 'conversation', 'references': ['SYNTHETIC_PRIVATE'],
                'context': {'tenant_id': 'tenant', 'company_id': 'company', 'workspace_id': 'workspace', 'assignment_ref': 'assignment'}}
    contract = {'agentSource': {'input': {'kind': 'references', 'references': []}, 'snapshot': snapshot}}
    assert _verified_origin_projection(work, contract, 'tenant') == {
        'status': 'VERIFIED', 'assignment_ref': 'assignment', 'source': {'kind': 'references', 'conversation_id': 'conversation'}}
    snapshot.pop('conversation_id')
    assert _verified_origin_projection(work, contract, 'tenant') == {'status': 'UNKNOWN'}


@pytest.mark.parametrize('kind,ids', [
    ('content-growth', {'content_ref': 'synthetic-content'}),
    ('music', {'song_ref': 'synthetic-song'}),
    ('writing', {'book_ref': 'synthetic-book', 'chapter_ref': 'synthetic-chapter'}),
])
def test_pending_origin_projection_original_work_get_reads_cycle_contract(tmp_path, monkeypatch, kind, ids):
    from fastapi.testclient import TestClient
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY
    from app.runtime import RuntimeFoundation
    from app.runtime.child_work import CanonicalChildWorkRuntime
    db, app, _, query, assignment_ref, _, headers = _publication_case(tmp_path, monkeypatch, 'content-growth')
    workspace = query['workspace_id']
    with scope():
        assignment = RuntimeFoundation(db).get(assignment_ref)['data']
        base = {'tenant_id': 'selfuse', 'company_id': COMPANY, 'workspace_id': workspace}
        snapshot = {'kind': kind, 'context': {**base, 'assignment_ref': assignment_ref},
                    'scope': {**base, **(ids if kind == 'writing' else {})},
                    **(ids if kind != 'writing' else {}), 'text': 'SYNTHETIC_PRIVATE_TEXT'}
        contract = {'problem': 'fixture', 'expectedResult': 'fixture',
                    'agentSource': {'input': {'kind': kind, **ids}, 'snapshot': snapshot}}
        work = CanonicalChildWorkRuntime(db).create_cycle_work(company_id=COMPANY, workspace_id=workspace,
            scope_type=assignment['scopeType'], scope_ref=assignment['scopeRef'], assignment_ref=assignment_ref,
            release_key='origin-fixture-' + kind, contract=contract)['work']['entity_id']
        with TestClient(app, client=('127.0.0.1', 49180)) as client:
            response = client.get('/api/workspace/runtime/foundation/team-operating/works/' + work, headers=headers)
        assert response.status_code == 200, response.text
        assert response.json()['origin'] == {'status': 'VERIFIED', 'assignment_ref': assignment_ref,
                                             'source': {'kind': kind, **ids}}
        assert 'SYNTHETIC_PRIVATE_TEXT' not in str(response.json()['origin'])


@pytest.mark.parametrize('kind', ['content-growth', 'writing', 'music'])
def test_pending_origin_projection_real_sources_and_scope_adversaries(tmp_path, monkeypatch, kind):
    import json
    from fastapi import HTTPException
    from fastapi.testclient import TestClient
    from backend.tests.test_company_execution_policy import policy_ready, HEADERS
    from backend.tests.test_professional_conversation_journeys import _agent_professional_source
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY
    from app.conversation_service import ConversationService
    from app.runtime import RuntimeFoundation
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from app.api.team_operating_router import build_team_operating_router
    db, app, _, _, _, workspace, row, binding, payload = policy_ready(tmp_path, monkeypatch)
    source = {'kind': 'content-growth', 'content_ref': row['content']['entity_id'],
              'expected_version_ref': row['version']['entity_id'], 'selection': payload['selection'],
              'references': payload['references']}
    if kind != 'content-growth':
        workspace, binding, source = _agent_professional_source(kind, db, app, tmp_path)
    assignment_ref = binding['context']['assignment_ref']
    with scope():
        foundation = RuntimeFoundation(db)
        assignment = foundation.get(assignment_ref)['data']
        snapshot = ConversationService(db).agent_work_source(COMPANY, workspace, assignment_ref, source)
        contract = {'problem': 'SYNTHETIC_PRIVATE_PROBLEM', 'expectedResult': 'fixture',
                    'agentSource': {'input': source, 'snapshot': snapshot}}
        work = CanonicalChildWorkRuntime(db).create_cycle_work(company_id=COMPANY, workspace_id=workspace,
            scope_type=assignment['scopeType'], scope_ref=assignment['scopeRef'], assignment_ref=assignment_ref,
            release_key='real-origin-' + kind, contract=contract)['work']
        work_ref = work['entity_id']
        endpoint = next(item.endpoint for item in build_team_operating_router(db).routes
                        if item.path.endswith('/works/{work_ref}') and 'GET' in item.methods)
        def http_read(headers=HEADERS):
            with TestClient(app, client=('127.0.0.1', 49180)) as client:
                return client.get('/api/workspace/runtime/foundation/team-operating/works/' + work_ref, headers=headers)
        response = http_read()
        assert response.status_code == 200, response.text
        origin = response.json()['origin']
        assert origin['status'] == 'VERIFIED' and origin['assignment_ref'] == assignment_ref
        assert origin['source']['kind'] == kind
        assert 'SYNTHETIC_PRIVATE_PROBLEM' not in json.dumps(origin)
        assert set(origin) == {'status', 'assignment_ref', 'source'}
        fields = {'content-growth': {'kind', 'content_ref'}, 'writing': {'kind', 'book_ref', 'chapter_ref'},
                  'music': {'kind', 'song_ref'}}[kind]
        assert set(origin['source']) == fields
        with db.connect() as con:
            con.execute('insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,?,?,?,?)',
                        ('synthetic-other-company', 'selfuse', 'synthetic-other-ceo', 'Synthetic', 'active'))
        for headers in ({**HEADERS, 'X-Tenant-Id': 'foreign-tenant'},
                        {**HEADERS, 'X-Ceo-Id': 'synthetic-other-ceo'}):
            denied_http = http_read(headers)
            assert denied_http.status_code != 200
            assert 'SYNTHETIC_PRIVATE_PROBLEM' not in denied_http.text
            assert all(source[field] not in denied_http.text for field in fields - {'kind'})
        with scope(tenant_id='foreign-tenant'):
            with pytest.raises(HTTPException) as denied: endpoint(work_ref)
            assert 'SYNTHETIC_PRIVATE_PROBLEM' not in str(denied.value.detail)
            assert all(source[field] not in str(denied.value.detail) for field in fields - {'kind'})
        with scope(company_id='foreign-company'):
            with pytest.raises(HTTPException) as denied: endpoint(work_ref)
            assert 'SYNTHETIC_PRIVATE_PROBLEM' not in str(denied.value.detail)
            assert all(source[field] not in str(denied.value.detail) for field in fields - {'kind'})
        cycle_ref = work['data']['cycleRef']
        with db.connect() as con:
            cycle_data = json.loads(con.execute('select data_json from runtime_entities where tenant_id=? and entity_id=?',
                                                ('selfuse', cycle_ref)).fetchone()[0])
            original_cycle = json.dumps(cycle_data)
            cycle_data['contract']['agentSource']['snapshot']['context']['workspace_id'] = 'foreign-workspace'
            con.execute('update runtime_entities set data_json=? where tenant_id=? and entity_id=?',
                        (json.dumps(cycle_data), 'selfuse', cycle_ref))
        assert http_read().json()['origin'] == {'status': 'UNKNOWN'}
        with db.connect() as con:
            con.execute('update runtime_entities set data_json=? where tenant_id=? and entity_id=?',
                        (original_cycle, 'selfuse', cycle_ref))
            con.execute('update runtime_entities set workspace_id=? where tenant_id=? and entity_id=?',
                        ('foreign-workspace', 'selfuse', cycle_ref))
        assert http_read().json()['origin'] == {'status': 'UNKNOWN'}
        with db.connect() as con:
            con.execute('update runtime_entities set workspace_id=? where tenant_id=? and entity_id=?',
                        (workspace, 'selfuse', cycle_ref))
            data = json.loads(con.execute('select data_json from runtime_entities where tenant_id=? and entity_id=?',
                                          ('selfuse', work_ref)).fetchone()[0])
            original = json.dumps(data)
            data['cycleRef'] = assignment_ref  # Same-tenant non-Cycle entity.
            con.execute('update runtime_entities set data_json=? where tenant_id=? and entity_id=?',
                        (json.dumps(data), 'selfuse', work_ref))
        assert http_read().json()['origin'] == {'status': 'UNKNOWN'}
        with db.connect() as con:
            con.execute('update runtime_entities set data_json=? where tenant_id=? and entity_id=?',
                        (original, 'selfuse', work_ref))
            for n in ('one', 'two'):
                con.execute('insert into runtime_links(link_id,tenant_id,company_id,workspace_id,source_id,relation,target_id,created_at) '
                            'values (?,?,?,?,?,?,?,?)', ('synthetic-' + n, 'selfuse', COMPANY, workspace, work_ref,
                                                          'HAS_SUCCESSOR_WORK', 'synthetic-target-' + n, '2026-01-01'))
        with pytest.raises(HTTPException): endpoint(work_ref)
        assert http_read().status_code != 200


@pytest.mark.parametrize('status', ['outcome_unknown', 'cancelled', 'authorization_revoked', 'timeout', 'response_invalid', 'network_error'])
def test_attempted_agent_error_never_falls_back_and_preserves_attempt(status):
    import asyncio
    from app.agent_adapter import AgentExecutionError
    from app.tool_executor import ToolExecutionError, ToolExecutor

    calls = []
    executor = ToolExecutor(None, {})

    async def execute(candidate, _prompt):
        calls.append(candidate)
        if candidate == 'agent':
            raise AgentExecutionError('synthetic uncertain result', status=status, outbound_attempted=True)
        return {'output': 'unexpected fallback', 'cost': 0}

    executor.execute = execute
    with pytest.raises(ToolExecutionError) as caught:
        asyncio.run(executor.execute_chain(['agent'], 'synthetic', lambda _: ['agent', 'fallback']))
    assert calls == ['agent']
    assert caught.value.status == status
    assert caught.value.outbound_attempted is True
    assert isinstance(caught.value.cause, AgentExecutionError)


def test_unattempted_agent_failure_keeps_existing_fallback():
    import asyncio
    from app.agent_adapter import AgentExecutionError
    from app.tool_executor import ToolExecutor

    calls = []
    executor = ToolExecutor(None, {})

    async def execute(candidate, _prompt):
        calls.append(candidate)
        if candidate == 'agent':
            raise AgentExecutionError('synthetic safe failure', status='configuration_rejected', outbound_attempted=False)
        return {'output': 'safe fallback', 'cost': 0}

    executor.execute = execute
    result = asyncio.run(executor.execute_chain(['agent'], 'synthetic', lambda _: ['agent', 'fallback']))
    assert calls == ['agent', 'fallback']
    assert result['output'] == 'safe fallback'


@pytest.mark.parametrize('status', ['cancelled', 'authorization_revoked', 'reservation_unknown', 'outcome_unknown', 'supervisor_unavailable'])
def test_unattempted_agent_stop_or_unknown_reservation_never_falls_back(status):
    import asyncio
    from app.agent_adapter import AgentExecutionError
    from app.tool_executor import ToolExecutionError, ToolExecutor

    calls = []
    executor = ToolExecutor(None, {})

    async def execute(candidate, _prompt):
        calls.append(candidate)
        raise AgentExecutionError('synthetic stopped or unknown', status=status, outbound_attempted=False)

    executor.execute = execute
    with pytest.raises(ToolExecutionError) as caught:
        asyncio.run(executor.execute_chain(['agent'], 'synthetic', lambda _: ['agent', 'fallback']))
    assert calls == ['agent']
    assert caught.value.status == status
    assert caught.value.outbound_attempted is False


@pytest.mark.parametrize("terminal", ["FAILED", "CANCELLED"])
def test_unknown_agent_event_blocks_only_original_work_without_reservation(tmp_path, terminal):
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeScopeError

    db, _, _ = _seed(tmp_path / "unknown.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        store = ResultStore(db, EvolutionEventLog(db))
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="work-a")
        store.transition(task["task_id"], terminal)
        store.record_agent_outcome_unknown(task["task_id"])
        store.record_agent_outcome_unknown(task["task_id"])
        policy = CompanyExecutionPolicy(db)
        with pytest.raises(RuntimeScopeError, match="不能重复启动"):
            policy.require_unreserved_agent_work(COMPANY, "work-a")
        policy.require_unreserved_agent_work(COMPANY, "work-b")


@pytest.mark.parametrize("outcome", ["cancelled", "completed", "artifact_error"])
def test_agent_finalization_commits_only_the_winning_task_state(tmp_path, outcome):
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext

    db, _, _ = _seed(tmp_path / "agent-finalize.sqlite")
    with TenantContext.scope(TENANT, subject_id="fixture-subject", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        events = EvolutionEventLog(db)
        store = ResultStore(db, events)
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE,
                                 work_ref="work-a", capability_source="tenant_private",
                                 capability_type="agent", capability_id="agent.fixture")
        task_id = task["task_id"]
        store.save_workflow(task_id, [])
        store.save_auto_workflow(task_id, [])
        store.transition(task_id, "RUNNING")
        control = TaskExecutionControlService(db, events)
        if outcome == "cancelled":
            control.cancel(task_id)
        result = {"tool_name": "agent", "output": "synthetic result", "cost": 3,
                  "outbound_attempted": True, "status": "success", "capability_type": "agent",
                  "artifact_receipts": [{}] if outcome == "artifact_error" else [{"relative_path": "result.txt"}],
                  "agent_artifacts": ["result.txt"], "trace": [],
                  "_agent_step_traces": [{"step": {"step": 1, "action": "execute"}, "input": "fixture prompt",
                      "tool_name": "agent", "output": "synthetic result", "timestamp": "fixture-time",
                      "tool_traces": [{"step": 1, "tool": "agent", "input": "fixture prompt",
                                       "output": "synthetic result", "timestamp": "fixture-time"}]}]}
        if outcome == "artifact_error":
            with pytest.raises(KeyError):
                store.finalize_agent_execution(task_id, "fixture prompt", result)
            assert store.get_task(task_id)["status"] == "RUNNING"
            assert store.list_executions(task_id) == [] and store.list_artifacts(task_id=task_id) == []
            assert store.list_trace(task_id) == [] and store.list_workflow_trace(task_id) == []
            assert not [e for e in events.get_by_correlation_id(task_id) if e["event_type"] == "usage.task_execution"]
            return
        finalized = store.finalize_agent_execution(task_id, "fixture prompt", result)
        execution = store.list_executions(task_id)
        assert len(execution) == 1 and execution[0]["cost"] == 3
        audit = [e for e in events.get_by_correlation_id(task_id) if e["event_type"] == "usage.task_execution"]
        assert len(audit) == 1
        if outcome == "cancelled":
            assert finalized["status"] == "CANCELLED" and execution[0]["output"] == ""
            assert store.list_artifacts(task_id=task_id) == []
            assert store.list_trace(task_id) == [] and store.list_workflow_trace(task_id) == []
            assert store.get_workflow(task_id)["status"] == "CANCELLED"
            assert not audit[0]["payload"].get("artifact_receipts") and not audit[0]["payload"].get("agent_artifacts")
            assert any(e["event_type"] == "agent.execution.outcome_unknown" for e in events.get_by_correlation_id(task_id))
        else:
            assert finalized["status"] == "COMPLETED" and execution[0]["output"] == "synthetic result"
            assert {a["source_ref"] for a in store.list_artifacts(task_id=task_id)} == {"task.output", "agent.output:result.txt"}
            assert store.get_workflow(task_id)["status"] == "COMPLETED"
            assert store.list_trace(task_id)[0]["output"] == "synthetic result"
            assert store.list_workflow_trace(task_id)[0]["output"] == "synthetic result"
            assert audit[0]["payload"]["artifact_receipts"][0]["relative_path"] == "result.txt"
            with pytest.raises(ValueError):
                control.cancel(task_id)
        with pytest.raises(ValueError):
            store.finalize_agent_execution(task_id, "fixture prompt", result)
        assert len(store.list_executions(task_id)) == 1


@pytest.mark.parametrize("outcome", ["cancelled", "completed", "record_error", "paused", "cancelled_error", "empty_trace"])
def test_agent_orchestrator_finalization_follows_actual_task_state(tmp_path, monkeypatch, outcome):
    import asyncio
    from types import SimpleNamespace
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    from app.evolution_event_log import EvolutionEventLog
    from app.orchestrator import Orchestrator
    from app.result_store import ResultStore
    from app.task_execution_control import ExecutionPaused, TaskExecutionControlService
    from app.tenant_context import TenantContext
    from app.agent_adapter import AgentExecutionError
    from app.tool_executor import ToolExecutionError

    db, _, _ = _seed(tmp_path / "agent-orchestrator.sqlite")
    with TenantContext.scope(TENANT, subject_id="fixture-subject", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        events = EvolutionEventLog(db)
        store = ResultStore(db, events)
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE,
                                 work_ref="work-a", capability_source="tenant_private",
                                 capability_type="agent", capability_id="agent.fixture")
        task_id = task["task_id"]
        control = TaskExecutionControlService(db, events)
        async def execute_step(_step, _prompt):
            if outcome in {"cancelled", "paused", "cancelled_error"}:
                control.cancel(task_id)
            if outcome == "paused":
                raise ExecutionPaused("CANCELLED")
            if outcome == "cancelled_error":
                raise ToolExecutionError("synthetic unknown", [], AgentExecutionError(
                    "synthetic unknown", status="outcome_unknown", outbound_attempted=True))
            return {"tool_name": "agent", "output": "synthetic result", "cost": 3,
                    "status": "success", "outbound_attempted": True,
                    "trace": [] if outcome == "empty_trace" else [{"tool": "agent", "input": "fixture", "output": "synthetic result",
                                                                  "timestamp": "fixture-time"}],
                    "artifact_receipts": [{"relative_path": "result.txt"}]}
        employee = SimpleNamespace(execute_step=execute_step,
                                   router=SimpleNamespace(tool_for_generated_step=lambda _: "model_gateway_tool"))
        builder = SimpleNamespace(build=lambda *args, **kwargs: "fixture prompt")
        runner = Orchestrator(store, builder, employee, execution_control=control)
        monkeypatch.setattr(runner, "_writing_reply_selection", lambda _: None)
        monkeypatch.setattr(runner, "generate_auto_workflow", lambda _: [])
        learned = []
        monkeypatch.setattr(runner, "_learn_from_execution", lambda *args: learned.append(True))
        if outcome == "record_error":
            original = events.record_in_connection
            def reject_pending(connection, **kwargs):
                if kwargs["event_type"] == "agent.completion.followup_pending":
                    raise RuntimeError("synthetic transaction failure")
                return original(connection, **kwargs)
            monkeypatch.setattr(events, "record_in_connection", reject_pending)
        if outcome in {"record_error", "empty_trace"}:
            with pytest.raises(RuntimeError):
                asyncio.run(runner.run(task_id))
        else:
            asyncio.run(runner.run(task_id))
        stored = store.get_task(task_id)
        if outcome == "completed":
            assert stored["status"] == "COMPLETED" and stored["output"] == "synthetic result"
            assert store.list_trace(task_id)[0]["output"] == "synthetic result" and learned == [True]
            with pytest.raises(ValueError):
                control.cancel(task_id)
        else:
            assert stored["status"] in {"CANCELLED", "FAILED"} and not stored["output"]
            assert store.list_artifacts(task_id=task_id) == [] and store.list_trace(task_id) == []
            assert store.list_workflow_trace(task_id) == [] and learned == []
            if outcome == "cancelled":
                assert store.list_executions(task_id)[0]["output"] == ""
                assert any(e["event_type"] == "agent.execution.outcome_unknown" for e in events.get_by_correlation_id(task_id))
            else:
                assert store.list_executions(task_id) == []
            if outcome in {"cancelled_error", "empty_trace"}:
                assert any(e["event_type"] == "agent.execution.outcome_unknown" for e in events.get_by_correlation_id(task_id))


@pytest.mark.parametrize("prior_present", [False, True])
def test_agent_resume_with_no_remaining_steps_requires_reconciliation(tmp_path, monkeypatch, prior_present):
    import asyncio
    from types import SimpleNamespace
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    from app.agent_adapter import AgentExecutionError
    from app.evolution_event_log import EvolutionEventLog
    from app.orchestrator import Orchestrator
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext

    db, _, _ = _seed(tmp_path / "agent-resume.sqlite")
    with TenantContext.scope(TENANT, subject_id="fixture-subject", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        events = EvolutionEventLog(db)
        store = ResultStore(db, events)
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE,
                                 work_ref="work-a", capability_source="tenant_private",
                                 capability_type="agent", capability_id="agent.fixture")
        task_id = task["task_id"]
        step = {"step": 1, "step_name": "original", "action": "execute"}
        store.save_workflow(task_id, [step])
        store.save_auto_workflow(task_id, [])
        if prior_present:
            store.save_workflow_trace(task_id, step, {"tool_name": "agent", "output": "prior result",
                "trace": [{"timestamp": "fixture-time"}]}, "fixture")
        store.update_workflow(task_id, completed_step=1)
        store.transition(task_id, "RESUMED")
        employee = SimpleNamespace(execute_step=lambda *args: pytest.fail("agent was replayed"))
        runner = Orchestrator(store, SimpleNamespace(build=lambda *a, **k: "fixture"), employee,
                              execution_control=TaskExecutionControlService(db, events))
        monkeypatch.setattr(runner, "_writing_reply_selection", lambda _: None)
        with pytest.raises(AgentExecutionError) as error:
            asyncio.run(runner.run(task_id))
        assert error.value.status == "outcome_unknown" and error.value.outbound_attempted is False
        assert store.list_executions(task_id) == [] and store.list_artifacts(task_id=task_id) == []


@pytest.mark.parametrize("flags, expect_unknown", [([True, False], True), ([False, None], True), ([False, False], False)])
def test_multistep_agent_cancellation_preserves_all_outbound_states(tmp_path, monkeypatch, flags, expect_unknown):
    import asyncio
    from types import SimpleNamespace
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE
    from app.evolution_event_log import EvolutionEventLog
    from app.orchestrator import Orchestrator
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext

    db, _, _ = _seed(tmp_path / "agent-multistep.sqlite")
    with TenantContext.scope(TENANT, subject_id="fixture-subject", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        events = EvolutionEventLog(db)
        store = ResultStore(db, events)
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE,
                                 work_ref="work-a", capability_source="tenant_private",
                                 capability_type="agent", capability_id="agent.fixture")
        task_id = task["task_id"]
        plan = [{"step": i, "step_name": f"step {i}", "action": "execute", "purpose": "fixture",
                 "expected_output": "fixture", "tool_required": "model_gateway_tool"} for i in (1, 2)]
        store.save_workflow(task_id, plan)
        store.save_auto_workflow(task_id, plan)
        store.transition(task_id, "RESUMED")
        control = TaskExecutionControlService(db, events)
        async def execute_step(step, _prompt):
            if step["step"] == 2:
                control.cancel(task_id)
            return {"tool_name": "agent", "output": "synthetic result", "cost": 1,
                    "status": "success", "outbound_attempted": flags[step["step"] - 1],
                    "trace": [{"tool": "agent", "input": "fixture", "output": "synthetic result",
                               "timestamp": "fixture-time"}]}
        runner = Orchestrator(store, SimpleNamespace(build=lambda *a, **k: "fixture"),
                              SimpleNamespace(execute_step=execute_step), execution_control=control)
        monkeypatch.setattr(runner, "_writing_reply_selection", lambda _: None)
        result = asyncio.run(runner.run(task_id))
        assert result["status"] == "CANCELLED"
        assert store.list_executions(task_id)[0]["output"] == "" and store.list_trace(task_id) == []
        unknown = [e for e in events.get_by_correlation_id(task_id) if e["event_type"] == "agent.execution.outcome_unknown"]
        assert bool(unknown) is expect_unknown


def resources(root, company="company-a"):
    return AgentWorkResources(root, tenant_id="tenant-a", company_id=company, work_ref="work-a", task_id="task-a")


def test_complete_skill_materialization_has_scoped_environment_and_unverified_use(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-key-never-forwarded")
    manifest, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: archive())
    installed = install_package(tmp_path / "packages", manifest, files)
    execution = resources(tmp_path / "work")
    prepared = execution.prepare([{"manifest": manifest, "path": str(installed), "skill_template_id": "skill-a"}])
    assert set(prepared["environment"]) == {"PATH", "TMPDIR", "LANG", "NO_PROXY", "no_proxy"}
    assert prepared["environment"]["NO_PROXY"] == prepared["environment"]["no_proxy"] == "localhost,127.0.0.1,::1"
    assert prepared["environment"]["TMPDIR"].startswith(str(execution.path))
    receipt = prepared["receipt"]["skills"][0]
    assert receipt["used"] == "UNVERIFIED"
    for item in manifest["files"]:
        assert digest((Path(receipt["path"]) / item["path"]).read_bytes()) == item["sha256"]
    assert execution.path != resources(tmp_path / "work", "company-b").path
    with pytest.raises(ValueError, match="不能自动重复"):
        execution.prepare([])


def test_files_are_collected_only_from_original_output_directory(tmp_path):
    execution = resources(tmp_path)
    execution.prepare([])
    (execution.path / "output" / "result.txt").write_text("self-made fixture")
    (execution.path / "unrelated.txt").write_text("not a declared result")
    receipts = execution.collect()
    assert [item["relative_path"] for item in receipts] == ["result.txt"]
    assert receipts[0]["work_ref"] == "work-a"
    assert receipts[0]["content_verification"] == "UNVERIFIED"
    assert receipts[0]["sha256"] == digest(b"self-made fixture")


def test_scope_and_browser_claims_never_grant_execution(tmp_path):
    with pytest.raises(ValueError, match="original Company"):
        AgentWorkResources(tmp_path, tenant_id="tenant-a", company_id="", work_ref="work-a", task_id="task-a")
    claimed = {"company_id": "company-a", "work_ref": "work-a", "profile_id": "profile-a",
               "allowed_actions": ["observe"], "allowed_hosts": ["example.com"], "verified": True}
    with pytest.raises(ValueError, match="实际工具边界"):
        require_browser_boundary(claimed, company_id="company-a", work_ref="work-a",
                                 profile_id="profile-a", url="https://example.com", action="observe")


def test_download_revalidates_scope_bytes_and_links(tmp_path):
    execution = resources(tmp_path)
    execution.prepare([])
    output = execution.path / "output"
    (output / "report.txt").write_bytes(b"original report")
    receipt = execution.collect()[0]
    assert execution.read_output(receipt) == b"original report"
    with pytest.raises(ValueError, match="原公司"):
        resources(tmp_path, "company-b").read_output(receipt)
    (output / "report.txt").write_bytes(b"modified report")
    with pytest.raises(ValueError):
        execution.read_output(receipt)
    (output / "report.txt").unlink()
    (output / "outside.txt").write_bytes(b"original report")
    (output / "report.txt").symlink_to(output / "outside.txt")
    with pytest.raises(OSError):
        execution.read_output(receipt)


@pytest.mark.parametrize('status', ['CANCELLED', 'AWAITING_INPUT', 'HUMAN_HANDOFF', 'COMPLETED', 'FAILED'])
def test_stopped_or_terminal_task_cannot_reserve_agent_call(tmp_path, status):
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeScopeError

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type='agent', capability_id='agent.codex',
                                     display_name='Synthetic Codex', metadata={'kind': 'codex-cli'})
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
        policy = CompanyExecutionPolicy(db)
        current = policy.save_agent_allowance(COMPANY, request_id='grant', expected_revision='',
            enabled=True, consent=True, binding_refs=[BINDING])
        store = ResultStore(db)
        task = store.create_task('fixture', company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref='work-stop')
        assert store.transition(task['task_id'], status)['status'] == status
        with pytest.raises(RuntimeScopeError, match='原工作不存在或已经占用过调用次数'):
            policy.reserve_agent_call(COMPANY, BINDING, task['task_id'], 'work-stop', current['revision'])
        assert policy.agent_readiness(COMPANY)['used_calls'] == 0
        active = store.create_task('active fixture', company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref='work-active')
        assert store.transition(active['task_id'], 'RUNNING')['status'] == 'RUNNING'
        policy.reserve_agent_call(COMPANY, BINDING, active['task_id'], 'work-active', current['revision'])
        assert policy.agent_readiness(COMPANY)['used_calls'] == 1


def test_concurrent_cancellation_and_reservation_preserve_actual_order(tmp_path):
    import threading
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeScopeError

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type='agent', capability_id='agent.codex',
                                     display_name='Synthetic Codex', metadata={'kind': 'codex-cli'})
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
        policy = CompanyExecutionPolicy(db)
        current = policy.save_agent_allowance(COMPANY, request_id='grant', expected_revision='',
            enabled=True, consent=True, binding_refs=[BINDING])
        store = ResultStore(db)
        task = store.create_task('fixture', company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref='concurrent-work')
        store.transition(task['task_id'], 'RUNNING')

    barrier = threading.Barrier(2, timeout=5)
    observed = {}
    def reserve():
        try:
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
                barrier.wait()
                CompanyExecutionPolicy(db).reserve_agent_call(COMPANY, BINDING, task['task_id'],
                                                              'concurrent-work', current['revision'])
            observed['reserve'] = 'reserved'
        except RuntimeScopeError as error:
            observed['reserve'] = str(error)
        except Exception as error:
            observed['reserve_error'] = repr(error)

    def cancel():
        try:
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
                barrier.wait()
                observed['cancel'] = ResultStore(db).transition(task['task_id'], 'CANCELLED')['status']
        except Exception as error:
            observed['cancel_error'] = repr(error)

    threads = [threading.Thread(target=reserve), threading.Thread(target=cancel)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)
    assert not any(thread.is_alive() for thread in threads), 'fixture workers still running'
    assert 'reserve_error' not in observed and 'cancel_error' not in observed, observed
    assert observed['cancel'] == 'CANCELLED'
    assert observed['reserve'] == 'reserved' or '原工作不存在或已经占用过调用次数' in observed['reserve']
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
        assert ResultStore(db).get_task(task['task_id'])['status'] == 'CANCELLED'
        assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)['used_calls'] == (observed['reserve'] == 'reserved')


@pytest.mark.parametrize('route_status,claim_status,matching,allowed', [
    ('CANCELLED', 'RUNNING', True, False),
    ('EXECUTING', 'SUBMITTING', True, False),
    ('EXECUTING', 'RUNNING', False, False),
    ('EXECUTING', 'RUNNING', True, True),
])
def test_agent_reservation_requires_current_scoped_work_claim(tmp_path, monkeypatch, route_status, claim_status, matching, allowed):
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY
    from app.company_execution_policy import CompanyExecutionPolicy, agent_work_claim_active
    from app.employee_execution_identity import EmployeeExecutionIdentity
    from app.result_store import ResultStore
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime, RuntimeScopeError
    from app.runtime.child_work import CanonicalChildWorkRuntime

    db, app, _, query, assignment_ref, _, headers = _publication_case(tmp_path, monkeypatch)
    workspace = query['workspace_id']
    db.save_tenant_private_capability(tenant_id='selfuse', capability_type='agent', capability_id='agent.codex',
                                     display_name='Synthetic Codex', metadata={'kind': 'codex-cli'})
    with scope():
        foundation = RuntimeFoundation(db)
        assignment = foundation.get(assignment_ref)['data']
        employee = EmployeeExecutionIdentity(db).resolve(company_id=COMPANY, workspace_id=workspace,
                                                          runtime_employee_ref=assignment['employeeRef'])
        with db.connect() as connection:
            connection.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                               "values ('fixture-agent-binding','selfuse',?,'tenant_private','agent','agent.codex')",
                               (employee['company_employee_ref'],))
        policy = CompanyExecutionPolicy(db)
        grant = policy.save_agent_allowance(COMPANY, request_id='grant', expected_revision='',
                                           enabled=True, consent=True, binding_refs=['fixture-agent-binding'])
        routing = ResponsibilityRoutingRuntime(db)
        routing.publish_workflow(company_id=COMPANY, workspace_id=workspace, scope_type=assignment['scopeType'],
            scope_ref=assignment['scopeRef'], workflow_key='fixture', assignment_refs=[assignment_ref],
            default_flow=[assignment['responsibilityKey']])
        work = CanonicalChildWorkRuntime(db).create_cycle_work(company_id=COMPANY, workspace_id=workspace,
            scope_type=assignment['scopeType'], scope_ref=assignment['scopeRef'],
            assignment_ref=assignment_ref, release_key='fixture-work',
            contract={'problem': 'fixture', 'expectedResult': 'fixture'})['work']['entity_id']
        routing.start_work(work, scope_type=assignment['scopeType'], scope_ref=assignment['scopeRef'],
                           workflow_key='fixture', initial_responsibility=assignment['responsibilityKey'])
        routing.begin_employee_execution(work, execution_key='claim', assignment_ref=assignment_ref)
        task = ResultStore(db).create_task('fixture', company_id=COMPANY, workspace_id=workspace,
                                           employee_id=employee['company_employee_ref'], work_ref=work, execution_ref='claim',
                                           capability_source='tenant_private', capability_type='agent', capability_id='agent.codex')
        ResultStore(db).transition(task['task_id'], 'RUNNING')
        if claim_status == 'RUNNING':
            routing.attach_provider_task(work, execution_key='claim', task_ref=task['task_id'] if matching else 'different-task')
        if route_status == 'CANCELLED':
            routing.cancel_work(work, reason='fixture cancellation')
        with db.connect() as connection:
            assert agent_work_claim_active(connection, tenant_id='selfuse', company_id=COMPANY, work_ref=work,
                                           task_id=task['task_id'], execution_ref='claim') is allowed
            assert not agent_work_claim_active(connection, tenant_id='foreign', company_id=COMPANY, work_ref=work,
                                                task_id=task['task_id'], execution_ref='claim')
            assert not agent_work_claim_active(connection, tenant_id='selfuse', company_id=COMPANY, work_ref='missing',
                                                task_id=task['task_id'], execution_ref='claim')
        if allowed:
            policy.reserve_agent_call(COMPANY, 'fixture-agent-binding', task['task_id'], work, grant['revision'])
            from app.evolution_event_log import EvolutionEventLog
            from fastapi.testclient import TestClient
            result_store = ResultStore(db, EvolutionEventLog(db))
            result_store.record_agent_outcome_unknown(task['task_id'])
            evidence = {'child_pid': 123, 'returncode': -15, 'attempt_sha256': 'a' * 64}
            with pytest.raises(ValueError, match='invalid local child evidence'):
                result_store.record_agent_local_child_exit(task['task_id'], {**evidence, 'attempt_sha256': 'bad'})
            result_store.record_agent_local_child_exit(task['task_id'], evidence)
            result_store.record_agent_local_child_exit(task['task_id'], evidence)
            with TestClient(app, client=('127.0.0.1', 49180)) as client:
                read = client.get('/api/workspace/runtime/foundation/team-operating/works/' + work, headers=headers)
                assert read.status_code == 200, read.text
                projection = next(item for item in read.json()['tasks'] if item['task_id'] == task['task_id'])
                assert projection['local_process_state'] == 'DIRECT_CHILD_REAPED'
                assert projection['reason_code'] == 'outcome_unknown' and projection['result_ref'] is None
            from app.api.team_operating_router import build_team_operating_router
            from app.database import Database
            from app.tenant_context import TenantContext
            reopened = Database(db.path)
            route = next(item.endpoint for item in build_team_operating_router(reopened).routes
                         if item.path.endswith('/works/{work_ref}') and 'GET' in item.methods)
            after_reopen = route(work)
            projection = next(item for item in after_reopen['tasks'] if item['task_id'] == task['task_id'])
            assert projection['local_process_state'] == 'DIRECT_CHILD_REAPED'
            assert projection['reason_code'] == 'outcome_unknown' and projection['call_reserved']
            with TenantContext.scope('foreign', company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
                with pytest.raises(ValueError, match='scope is unavailable'):
                    ResultStore(reopened, EvolutionEventLog(reopened)).record_agent_local_child_exit(task['task_id'], evidence)
            with reopened.connect() as connection:
                events = connection.execute("select payload from evolution_events where tenant_id='selfuse' "
                    "and correlation_id=? and event_type='agent.execution.local_child_exit'", (task['task_id'],)).fetchall()
                assert len(events) == 1 and 'child_pid' not in events[0]['payload']
            EvolutionEventLog(reopened).record(correlation_id=task['task_id'], event_type='agent.execution.local_child_exit',
                payload={'state': 'forged'}, idempotency_key='fixture-forged-local-evidence')
            tampered = route(work)
            projection = next(item for item in tampered['tasks'] if item['task_id'] == task['task_id'])
            assert projection['local_process_state'] == 'UNKNOWN' and projection['reason_code'] == 'outcome_unknown'
        else:
            with pytest.raises(RuntimeScopeError, match='原工作已停止或执行关联发生变化'):
                policy.reserve_agent_call(COMPANY, 'fixture-agent-binding', task['task_id'], work, grant['revision'])
        assert policy.agent_readiness(COMPANY)['used_calls'] == int(allowed)


@pytest.mark.parametrize('reread,expected_status', [
    ('cancelled', 200), ('active', 422), ('missing', 422), ('unauthorized', 422),
])
def test_cancelled_work_execute_error_requires_scoped_reread(tmp_path, monkeypatch, reread, expected_status):
    import asyncio
    from fastapi import HTTPException
    from app.api import team_operating_router as module
    from app.runtime import ResponsibilityRoutingError
    from app.tenant_context import TenantContext
    from test_employee_execution_identity import _seed, TENANT, COMPANY

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    calls = []
    def get_work(_self, _ref):
        calls.append(True)
        if len(calls) == 1:
            raise ResponsibilityRoutingError('Work has no active responsibility route')
        if reread == 'missing':
            raise KeyError('missing')
        return {'company_id': 'foreign-company' if reread == 'unauthorized' else COMPANY, 'data': {'responsibilityRouting': {
            'status': 'CANCELLED' if reread != 'active' else 'EXECUTING'}}}
    monkeypatch.setattr(module.RuntimeFoundation, 'get', get_work)
    router = module.build_team_operating_router(db)
    endpoint = next(route.endpoint for route in router.routes if route.path.endswith('/works/{work_ref}/execute'))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
        if expected_status == 200:
            result = asyncio.run(endpoint('fixture-work', limits=None, max_executions=1))
            assert result['work']['data']['responsibilityRouting']['status'] == 'CANCELLED'
            assert '外部效果仍需核验' in result['execution_blocked']
        else:
            with pytest.raises(HTTPException) as caught:
                asyncio.run(endpoint('fixture-work', limits=None, max_executions=1))
            assert caught.value.status_code == expected_status


@pytest.mark.parametrize('entrypoint', ['team-cancel', 'general-control'])
def test_work_stop_entrypoints_acquire_spawn_lock_before_read(tmp_path, monkeypatch, entrypoint):
    import threading
    from types import SimpleNamespace
    from app.agent_adapter import _AGENT_STOP_SPAWN_LOCK
    from app.api import team_operating_router as module
    from app.runtime import RuntimeScopeError
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from app.tenant_context import TenantContext
    from test_employee_execution_identity import _seed, TENANT, COMPANY

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    entered = threading.Event()
    read_started = threading.Event()
    finished = threading.Event()
    errors = []
    def fail_read(*_args, **_kwargs):
        read_started.set()
        raise RuntimeScopeError('fixture stop before mutation')
    if entrypoint == 'team-cancel':
        monkeypatch.setattr(module.RuntimeFoundation, 'get', fail_read)
        router = module.build_team_operating_router(db)
        endpoint = next(route.endpoint for route in router.routes if route.path.endswith('/works/{work_ref}/cancel'))
        invoke = lambda: endpoint('fixture-work', module.CancelOperatingWorkIn(reason='fixture stop'))
    else:
        dummy = SimpleNamespace(_require_general_work=fail_read)
        invoke = lambda: GeneralWorkspaceDelivery.control_work(dummy, company_id=COMPANY,
            workspace_id='fixture-workspace', work_ref='fixture-work', action='CANCEL')
    def run():
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo'):
            entered.set()
            try:
                invoke()
            except Exception as error:
                errors.append(error)
            finally:
                finished.set()
    with _AGENT_STOP_SPAWN_LOCK:
        thread = threading.Thread(target=run)
        thread.start()
        assert entered.wait(5)
        assert not read_started.wait(0.05)
    thread.join(5)
    assert not thread.is_alive() and finished.is_set() and read_started.is_set() and len(errors) == 1


@pytest.mark.parametrize('late_response', [False, True])
def test_original_work_cancel_reaches_agent_stop_check_without_real_spawn(tmp_path, monkeypatch, late_response):
    import os
    from types import SimpleNamespace
    from fastapi.testclient import TestClient
    import app.agent_adapter as agent_adapter
    import app.agent_executor_dispatch as dispatch
    from app.agent_adapter import AgentExecutionError
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.employee_execution_identity import EmployeeExecutionIdentity
    from app.runtime import RuntimeFoundation
    from backend.tests.test_company_execution_policy import policy_ready, HEADERS
    from backend.tests.test_professional_conversation_journeys import _agent_professional_source
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY

    monkeypatch.setenv('CURIS_AGENT_TMP_ROOT', os.environ['CURIS_TEST_ROOT'])
    db, app, _, _, model_calls, _, _, _, _ = policy_ready(tmp_path, monkeypatch)
    workspace, binding, source = _agent_professional_source('writing', db, app, tmp_path)
    assignment = binding['context']['assignment_ref']
    with scope():
        employee_ref = RuntimeFoundation(db).get(assignment)['data']['employeeRef']
        identity = EmployeeExecutionIdentity(db).resolve(company_id=COMPANY, workspace_id=workspace,
                                                          runtime_employee_ref=employee_ref)
        db.save_tenant_private_capability(tenant_id='selfuse', capability_type='agent', capability_id='agent.fixture',
                                         display_name='Synthetic Agent', metadata={'kind': 'codex-cli'})
        with db.connect() as connection:
            connection.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                               "values ('fixture-stop-binding','selfuse',?,'tenant_private','agent','agent.fixture')",
                               (identity['company_employee_ref'],))
        CompanyExecutionPolicy(db).save_agent_allowance(COMPANY, request_id='fixture-stop-grant', expected_revision='',
            enabled=True, consent=True, binding_refs=['fixture-stop-binding'])
    monkeypatch.setattr(agent_adapter, 'require_codex_execution_available', lambda: None)
    observed = []
    root = '/api/workspace/runtime/foundation/team-operating'
    def factory(_metadata, **kwargs):
        context = kwargs['execution_context']
        def execute(_prompt):
            observed.append(('before', context['should_stop']()))
            context['before_launch']()
            cancelled = client.post(root + f'/works/{work}/cancel', headers=HEADERS, json={'reason': 'fixture stop'})
            observed.append(('cancel_status', cancelled.status_code))
            if cancelled.status_code != 200:
                observed.append(('cancel_detail', cancelled.json().get('detail')))
                print('Synthetic cancellation error:', cancelled.json().get('detail'))
            observed.append(('after', context['should_stop']()))
            if late_response:
                return {'output': 'SYNTHETIC_LATE_OUTPUT_MUST_NOT_BE_ADOPTED'}
            raise AgentExecutionError('fixture stopped after reservation', status='cancelled', outbound_attempted=False)
        return SimpleNamespace(execute=execute)
    monkeypatch.setattr(dispatch, 'build_agent_executor', factory)
    with TestClient(app, client=('127.0.0.1', 49180)) as client:
        workflow_path = root + f'/assignments/{assignment}/agent-workflow'
        reviewed = client.get(workflow_path, headers=HEADERS, params={'company_id': COMPANY, 'workspace_id': workspace})
        assert reviewed.status_code == 200
        basis = reviewed.json()
        if basis['state'] == 'NEEDS_PUBLICATION':
            published = client.post(workflow_path, headers=HEADERS, json={'company_id': COMPANY, 'workspace_id': workspace,
                'expected_revision': basis['assignment_revision'], 'review_token': basis['review_token'], 'confirm': True})
            assert published.status_code == 200 and published.json()['state'] == 'READY'
        else:
            assert basis['state'] == 'READY'
        created = client.post(root + f'/assignments/{assignment}/work', headers=HEADERS,
            json={'request_id': 'fixture-stop-work', 'problem': 'Summarize the selected text',
                  'expected_result': 'A short summary', 'agent_binding_ref': 'fixture-stop-binding', 'source': source})
        assert created.status_code == 200, created.text
        work = created.json()['work']['entity_id']
        response = client.post(root + f'/works/{work}/execute?max_executions=1', headers=HEADERS)
        assert response.status_code == 200, response.text
        assert 'SYNTHETIC_LATE_OUTPUT_MUST_NOT_BE_ADOPTED' not in response.text
    assert observed == [('before', False), ('cancel_status', 200), ('after', True)]
    assert model_calls == []
    with scope():
        assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)['used_calls'] == 1


def test_allowance_is_one_pool_across_regrant_restart_and_unknown_calls(tmp_path, monkeypatch):
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeScopeError
    db, _, _ = _seed(tmp_path / "agent.sqlite")
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id="agent.codex",
                                     display_name="Synthetic Codex", metadata={"kind": "codex-cli"})
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        policy = CompanyExecutionPolicy(db)
        current = policy.save_agent_allowance(COMPANY, request_id="grant-1", expected_revision="",
            enabled=True, consent=True, binding_refs=[BINDING])
        with pytest.raises(RuntimeScopeError, match="仍有效"):
            policy.new_agent_authorization(COMPANY, request_id="premature", previous_authorization_ref=current["authorization_ref"],
                expected_revision=current["revision"], binding_refs=[BINDING], consent=True)
        for index in range(4):
            work_ref = f"work-{index}"
            task = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref=work_ref)
            ResultStore(db).transition(task["task_id"], "RUNNING")
            policy.reserve_agent_call(COMPANY, BINDING, task["task_id"], work_ref, current["revision"])
            with pytest.raises(RuntimeScopeError, match="重复启动"):
                policy.reserve_agent_call(COMPANY, BINDING, task["task_id"], work_ref, current["revision"])
            replacement = ResultStore(db).create_task("same original work", company_id=COMPANY,
                employee_id=COMPANY_EMPLOYEE, work_ref=work_ref)
            ResultStore(db).transition(replacement["task_id"], "RUNNING")
            with pytest.raises(RuntimeScopeError, match="重复启动"):
                policy.reserve_agent_call(COMPANY, BINDING, replacement["task_id"], work_ref, current["revision"])
            assert policy.agent_readiness(COMPANY)["used_calls"] == index + 1
        assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["remaining_calls"] == 0
        current = policy.save_agent_allowance(COMPANY, request_id="revoke", expected_revision=current["revision"],
            enabled=False, binding_refs=[])
        current = policy.save_agent_allowance(COMPANY, request_id="grant-2", expected_revision=current["revision"],
            enabled=True, consent=True, binding_refs=[BINDING])
        assert current["used_calls"] == 4 and current["state"] == "BLOCKED"
        fifth = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="work-a")
        ResultStore(db).transition(fifth["task_id"], "RUNNING")
        with pytest.raises(RuntimeScopeError, match="4 次"):
            policy.reserve_agent_call(COMPANY, BINDING, fifth["task_id"], "work-a", current["revision"])
        old_reference = current["authorization_ref"]
        request = dict(request_id="explicit-new-permit", previous_authorization_ref=old_reference,
            expected_revision=current["revision"], binding_refs=[BINDING], consent=True)
        monkeypatch.setenv("CURIS_AGENT_AUTHORIZATION_REF", old_reference)
        assert not policy.agent_readiness(COMPANY)["new_authorization_allowed"]
        with pytest.raises(RuntimeScopeError, match="不能增加新额度"):
            policy.new_agent_authorization(COMPANY, **request)
        monkeypatch.delenv("CURIS_AGENT_AUTHORIZATION_REF")
        with pytest.raises(ValueError):
            policy.new_agent_authorization(COMPANY, **{**request, "consent": False})
        with db.connect() as con:
            old_calls = policy.agent_rows(con, "reserved", old_reference)
        fresh = policy.new_agent_authorization(COMPANY, **request)
        assert fresh["authorization_ref"] != old_reference and fresh["remaining_calls"] == 4
        assert fresh["total_reserved_calls"] == 4 and fresh["authorization_history"] == [
            {"authorization_ref": old_reference, "used_calls": 4}]
        assert policy.new_agent_authorization(COMPANY, **request)["authorization_ref"] == fresh["authorization_ref"]
        with pytest.raises(ValueError):
            policy.new_agent_authorization(COMPANY, **{**request, "expected_revision": "changed"})
        with pytest.raises(RuntimeScopeError, match="原明确授权"):
            policy.reserve_agent_call(COMPANY, BINDING, fifth["task_id"], "work-a", fresh["revision"], old_reference)
        policy.reserve_agent_call(COMPANY, BINDING, fifth["task_id"], "work-a", fresh["revision"], fresh["authorization_ref"])
        assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["used_calls"] == 1
        with pytest.raises(RuntimeScopeError, match="重复启动"):
            replay = ResultStore(db).create_task("old Work cannot be replayed under a new permit",
                company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="work-0")
            ResultStore(db).transition(replay["task_id"], "RUNNING")
            policy.reserve_agent_call(COMPANY, BINDING, replay["task_id"], "work-0", fresh["revision"], fresh["authorization_ref"])
        with db.connect() as con:
            assert policy.agent_rows(con, "reserved", old_reference) == old_calls
        refreshed = policy.save_agent_allowance(COMPANY, request_id="new-ref-regrant", expected_revision=fresh["revision"],
            enabled=True, consent=True, binding_refs=[BINDING], authorization_ref=fresh["authorization_ref"])
        assert refreshed["used_calls"] == 1 and refreshed["total_reserved_calls"] == 5
        with pytest.raises(RuntimeScopeError, match="旧授权请求"):
            policy.save_agent_allowance(COMPANY, request_id="grant-1", expected_revision=refreshed["revision"],
                enabled=True, consent=True, binding_refs=[BINDING], authorization_ref=fresh["authorization_ref"])
        revoked = policy.save_agent_allowance(COMPANY, request_id="revoke-new-ref", expected_revision=refreshed["revision"],
            enabled=False, binding_refs=[], authorization_ref=fresh["authorization_ref"])
        assert revoked["used_calls"] == 1 and revoked["new_authorization_allowed"]
        next_grant = policy.new_agent_authorization(COMPANY, request_id="explicit-after-revoke",
            previous_authorization_ref=fresh["authorization_ref"], expected_revision=revoked["revision"],
            binding_refs=[BINDING], consent=True)
        assert next_grant["used_calls"] == 0 and next_grant["total_reserved_calls"] == 5
        with pytest.raises(RuntimeScopeError, match="历史授权"):
            policy.new_agent_authorization(COMPANY, **request)
        monkeypatch.setenv("CURIS_AGENT_AUTHORIZATION_REF", old_reference)
        with pytest.raises(RuntimeScopeError, match="明确授权不一致"):
            policy.agent_readiness(COMPANY)
        monkeypatch.delenv("CURIS_AGENT_AUTHORIZATION_REF")


def test_unlimited_allowance_requires_scoped_confirmation_and_preserves_reservations(tmp_path, monkeypatch):
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE, BINDING
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeScopeError
    db, _, _ = _seed(tmp_path / "unlimited.sqlite")
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type="agent", capability_id="agent.codex",
                                      display_name="Synthetic Codex", metadata={"kind": "codex-cli"})
    with db.connect() as con:
        con.execute("insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo-trust', 'Other')",
                    ("other-company", TENANT))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        policy = CompanyExecutionPolicy(db)
        initial = policy.save_agent_allowance(COMPANY, request_id="bounded", expected_revision="",
                                             enabled=True, consent=True, binding_refs=[BINDING])
        for index in range(4):
            work = f"existing-{index}"
            task = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref=work)
            ResultStore(db).transition(task["task_id"], "RUNNING")
            policy.reserve_agent_call(COMPANY, BINDING, task["task_id"], work, initial["revision"])
        with db.connect() as con:
            old = policy.agent_rows(con, "reserved")
        assert policy.agent_readiness(COMPANY)["remaining_calls"] == 0
        with pytest.raises(ValueError):
            policy.save_agent_allowance(COMPANY, request_id="no-consent", expected_revision=initial["revision"],
                enabled=True, consent=False, unlimited_consent=True, binding_refs=[BINDING])
        grant = dict(request_id="unlimited", expected_revision=initial["revision"], enabled=True,
                     consent=True, unlimited_consent=True, binding_refs=[BINDING], authorization_ref=initial["authorization_ref"])
        monkeypatch.setenv("CURIS_AGENT_AUTHORIZATION_REF", initial["authorization_ref"])
        with pytest.raises((ValueError, RuntimeScopeError)):
            policy.save_agent_allowance(COMPANY, **{**grant, "request_id": "bad-binding", "binding_refs": ["other-binding"]})
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="member"):
            with pytest.raises(RuntimeScopeError):
                policy.save_agent_allowance(COMPANY, **{**grant, "request_id": "not-owner"})
        with TenantContext.scope("foreign-tenant", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
            with pytest.raises((ValueError, RuntimeScopeError)):
                policy.save_agent_allowance(COMPANY, **{**grant, "request_id": "wrong-tenant"})
        with pytest.raises((ValueError, RuntimeScopeError)):
            policy.save_agent_allowance("wrong-company", **{**grant, "request_id": "wrong-company"})
        with TenantContext.scope(TENANT, company_id="other-company", ceo_id="ceo-trust", role="ceo"):
            with pytest.raises(RuntimeScopeError, match="其他公司"):
                policy.save_agent_allowance("other-company", **{**grant, "request_id": "other-company"})
        assert policy.agent_readiness(COMPANY)["revision"] == initial["revision"]
        current = policy.save_agent_allowance(COMPANY, **grant)
        assert current["authorization_ref"] == initial["authorization_ref"]
        assert current["limit_mode"] == "UNLIMITED" and current["remaining_calls"] is None
        assert current["used_calls"] == 4 and current["authorization"]["original_max_calls"] == 4
        assert current["authorization"]["max_calls"] is None and current["effective_max_calls"] is None
        assert policy.save_agent_allowance(COMPANY, **grant)["revision"] == current["revision"]
        with pytest.raises(ValueError):
            policy.save_agent_allowance(COMPANY, **{**grant, "unlimited_consent": False})
        with pytest.raises(ValueError):
            policy.save_agent_allowance(COMPANY, **{**grant, "request_id": "stale"})
        assert CompanyExecutionPolicy(db).agent_readiness(COMPANY)["limit_mode"] == "UNLIMITED"
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        fifth = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="fresh-5")
        other = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="fresh-5")
        for item in (fifth, other):
            ResultStore(db).transition(item["task_id"], "RUNNING")
        barrier = Barrier(2)
        def attempt(item):
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
                barrier.wait()
                try:
                    CompanyExecutionPolicy(db).reserve_agent_call(COMPANY, BINDING, item["task_id"], "fresh-5", current["revision"])
                    return True
                except RuntimeScopeError:
                    return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(attempt, (fifth, other))) == [False, True]
        with pytest.raises(RuntimeScopeError, match="重复启动"):
            policy.reserve_agent_call(COMPANY, BINDING, fifth["task_id"], "fresh-5", current["revision"])
        replay = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="existing-0")
        ResultStore(db).transition(replay["task_id"], "RUNNING")
        with pytest.raises(RuntimeScopeError, match="重复启动"):
            policy.reserve_agent_call(COMPANY, BINDING, replay["task_id"], "existing-0", current["revision"])
        with db.connect() as con:
            assert policy.agent_rows(con, "reserved")[:4] == old
        assert policy.agent_readiness(COMPANY)["used_calls"] == 5
        blocked_task = ResultStore(db).create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE, work_ref="invalid-mode")
        ResultStore(db).transition(blocked_task["task_id"], "RUNNING")
        real_rows = policy.agent_rows
        with monkeypatch.context() as patcher:
            def unknown_mode(con, kind, authorization_ref=None):
                rows = real_rows(con, kind, authorization_ref)
                if kind == "changed" and rows:
                    rows[-1] = {**rows[-1], "limit_mode": "UNRECOGNIZED"}
                return rows
            patcher.setattr(policy, "agent_rows", unknown_mode)
            assert policy.agent_readiness(COMPANY)["state"] == "BLOCKED"
            with pytest.raises(RuntimeScopeError, match="次数范围"):
                policy.reserve_agent_call(COMPANY, BINDING, blocked_task["task_id"], "invalid-mode", current["revision"])
        barrier = Barrier(2)
        def revoke_or_reserve(revoke):
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
                local = CompanyExecutionPolicy(db)
                barrier.wait()
                if revoke:
                    return local.save_agent_allowance(COMPANY, request_id="stop-unlimited", expected_revision=current["revision"],
                        enabled=False, binding_refs=[], authorization_ref=initial["authorization_ref"])
                try:
                    local.reserve_agent_call(COMPANY, BINDING, blocked_task["task_id"], "invalid-mode", current["revision"])
                    return True
                except RuntimeScopeError:
                    return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            revoked, reserved_before_revoke = list(pool.map(revoke_or_reserve, (True, False)))
        assert revoked["limit_mode"] == "FOUR_CALLS" and revoked["state"] == "BLOCKED"
        assert policy.agent_readiness(COMPANY)["used_calls"] == 5 + int(reserved_before_revoke)
        with pytest.raises(RuntimeScopeError):
            policy.reserve_agent_call(COMPANY, BINDING, replay["task_id"], "existing-0", current["revision"])


def test_new_agent_authorization_input_requires_explicit_boolean_confirmation():
    from app.main import AgentAuthorizationIn
    from pydantic import ValidationError
    payload = dict(request_id="new", previous_authorization_ref="old", expected_revision="revision",
        binding_refs=["binding"], consent=True)
    assert AgentAuthorizationIn(**payload).consent is True
    for value in ("true", 1, None):
        with pytest.raises(ValidationError):
            AgentAuthorizationIn(**{**payload, "consent": value})


def test_short_native_temporary_storage_keeps_durable_results_and_rejects_reuse(tmp_path):
    import json
    import os
    from uuid import uuid4
    execution = AgentWorkResources(tmp_path / "durable", tenant_id="tenant", company_id="company",
        work_ref="work", task_id=uuid4().hex)
    prepared = execution.prepare([], temporary_root=Path(os.environ["CURIS_TEST_ROOT"]))
    temporary = Path(prepared["environment"]["TMPDIR"])
    assert len(str(temporary).encode()) <= 64
    assert temporary.stat().st_mode & 0o777 == 0o700
    assert json.loads((temporary / "owner.json").read_text()) == execution.identity
    assert not execution.path.is_relative_to(temporary) and (execution.path / "output").is_dir()
    with pytest.raises(ValueError, match="不自动复用"):
        execution.prepare_temporary(temporary.parent)
    (temporary / "owner.json").write_text(json.dumps({**execution.identity, "work_ref": "foreign"}))
    with pytest.raises(ValueError, match="身份不一致"):
        execution.prepare_temporary(temporary.parent)


def test_native_installation_metadata_inspection_never_creates_or_returns_identifier(tmp_path):
    from app.agent_adapter import installation_id_snapshot
    identifier = "14b4740e-dc05-4f43-920d-fd1a1f5d0d2e"
    path = tmp_path / "synthetic-installation-metadata"
    with pytest.raises(FileNotFoundError):
        installation_id_snapshot(path)
    assert not path.exists()
    path.write_text(identifier)
    path.chmod(0o644)
    before = installation_id_snapshot(path)
    assert before["size"] == 36 and before["mode"] == 0o644 and identifier not in str(before)
    assert installation_id_snapshot(path) == before
    path.chmod(0o600)
    with pytest.raises(ValueError):
        installation_id_snapshot(path)
    path.chmod(0o644)
    path.write_text("x" * 36)
    with pytest.raises(ValueError):
        installation_id_snapshot(path)
    link = tmp_path / "synthetic-link"
    link.symlink_to(path)
    with pytest.raises(OSError):
        installation_id_snapshot(link)


def native_catalog_fixture():
    return {"models": [{"slug": "gpt-5.6-sol", "tool_mode": "code_mode_only", "multi_agent_version": "v2",
        "use_responses_lite": True, "base_instructions": "SYNTHETIC_VENDOR_PROMPT_DO_NOT_PERSIST",
        "model_messages": {"prompt": "SYNTHETIC_VENDOR_MESSAGE_DO_NOT_PERSIST"}, "comp_hash": "old",
        "experimental_supported_tools": ["unapproved"], "supports_parallel_tool_calls": True}]}


def test_model_catalog_reduces_proved_capabilities_and_discards_vendor_prompts():
    import json
    from app.agent_work_resources import scoped_codex_model_catalog, SCOPED_CODEX_INSTRUCTIONS
    original = native_catalog_fixture()
    catalog, receipt = scoped_codex_model_catalog(original, "gpt-5.6-sol")
    model = catalog["models"][0]
    assert model["base_instructions"] == SCOPED_CODEX_INSTRUCTIONS and model["model_messages"] is None
    assert "SYNTHETIC_VENDOR" not in json.dumps(catalog) and "old" not in json.dumps(catalog)
    assert model["tool_mode"] == "direct" and model["multi_agent_version"] == "disabled"
    assert model["experimental_supported_tools"] == [] and model["input_modalities"] == ["text"]
    assert not model["supports_parallel_tool_calls"] and not model["supports_search_tool"]
    assert original["models"][0]["tool_mode"] == "code_mode_only"
    assert receipt["requested_native_metadata"]["multi_agent_version"] == "v2"
    with pytest.raises(ValueError):
        scoped_codex_model_catalog(original, "unknown-model")
    with pytest.raises(ValueError):
        scoped_codex_model_catalog({"models": original["models"] * 2}, "gpt-5.6-sol")
    original["models"][0]["multi_agent_version"] = "new-unproved-version"
    with pytest.raises(ValueError):
        scoped_codex_model_catalog(original, "gpt-5.6-sol")


def test_reduced_linux_catalog_is_reusable_without_restoring_native_capabilities():
    from app.agent_work_resources import scoped_codex_model_catalog
    catalog, _ = scoped_codex_model_catalog(native_catalog_fixture(), "gpt-5.6-sol")
    repeated, receipt = scoped_codex_model_catalog(catalog, "gpt-5.6-sol")
    assert repeated == catalog
    assert receipt["requested_native_metadata"]["tool_mode"] == "direct"
    assert receipt["effective_configuration"]["multi_agent_version"] == "disabled"


@pytest.mark.parametrize("key,value", [
    ("base_instructions", "untrusted replacement"), ("model_messages", {}),
    ("multi_agent_version", "v2"), ("tool_mode", "code_mode_only"),
    ("supports_parallel_tool_calls", True), ("supports_search_tool", 0),
    ("experimental_supported_tools", ["unapproved"]), ("use_responses_lite", 1),
])
def test_reduced_linux_catalog_rejects_changed_or_loosely_typed_capabilities(key, value):
    from app.agent_work_resources import scoped_codex_model_catalog
    catalog, _ = scoped_codex_model_catalog(native_catalog_fixture(), "gpt-5.6-sol")
    catalog["models"][0][key] = value
    with pytest.raises(ValueError):
        scoped_codex_model_catalog(catalog, "gpt-5.6-sol")


def test_native_metadata_probe_is_unmetered_bounded_and_catalog_is_read_only(tmp_path, monkeypatch):
    import hashlib
    import json
    import subprocess
    import app.agent_adapter as module
    temporary = tmp_path / "temporary"
    temporary.mkdir()
    executable = tmp_path / "synthetic-codex-not-executable"
    executable.write_bytes(b"self-authored non-executable fixture")
    monkeypatch.setattr(module, "PROVED_CODEX_SHA256", hashlib.sha256(executable.read_bytes()).hexdigest())
    charged, requests, verified = [], [], []
    adapter = module.CodexCliAdapter(cwd=str(tmp_path), executable=str(executable),
        environment={"PATH": "/usr/bin:/bin", "TMPDIR": str(temporary), "CURIS_AGENT_TOOL_TOKEN": "never-forward-to-metadata"},
        before_launch=lambda: charged.append(True), supervisor_command=["synthetic-supervisor-never-launched"])
    profile = temporary / "metadata.sb"
    profile.write_text("(version 1)\n(allow default)\n(deny network*)")
    monkeypatch.setattr(adapter, "_native_file_profile", lambda **kw: profile if kw == {"metadata_only": True} else None)
    monkeypatch.setattr(adapter, "_verify_installation", lambda **kw: verified.append(kw))
    def metadata_only(instance, command, *, input, timeout, **kwargs):
        assert command[-3:] == ["debug", "models", "--bundled"] and timeout == 8 and input == ""
        assert "CURIS_AGENT_TOOL_TOKEN" not in instance.environment
        instance.before_launch()
        requests.append(command)
        return subprocess.CompletedProcess(command, 0, json.dumps(native_catalog_fixture()), "")
    monkeypatch.setattr(module.CodexCliAdapter, "_run_process", metadata_only)
    catalog = adapter._prepare_model_profile()
    assert len(requests) == 1 and charged == [] and verified == [{"outbound_attempted": False}]
    assert catalog.stat().st_mode & 0o777 == 0o400
    assert "SYNTHETIC_VENDOR" not in catalog.read_text()
    assert adapter.native_model_profile["catalog_sha256"] == hashlib.sha256(catalog.read_bytes()).hexdigest()
    assert adapter.native_model_profile["generation_allowance_reserved_by_metadata"] is False
    boundary = adapter.native_model_profile["network_boundary"]
    assert boundary["os_destination_allowlist"] is False
    assert boundary["model_web_access"] == "SCOPED_CURIS_BROWSER_TOOL"
    assert adapter._access_snapshot(session_id="", is_resume=False, command_accepted=True)["network_boundary"] == boundary


def test_final_native_argv_keeps_per_tool_approval_after_server_table(tmp_path, monkeypatch):
    import json
    import subprocess
    from app.agent_adapter import CodexCliAdapter
    commands = []
    def runner(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, json.dumps({
            "type": "item.completed", "item": {"type": "agent_message", "text": "synthetic final result"}}) + "\n", "")
    adapter = CodexCliAdapter(cwd=str(tmp_path), executable="/synthetic/original-codex",
        runner=runner, environment={"TMPDIR": str(tmp_path)},
        tool_url="http://127.0.0.1:49180/api/workspace/agent-tools")
    catalog = tmp_path / "synthetic-catalog.json"
    def prepared():
        adapter.executable = "/synthetic/verified-codex"
        return catalog
    monkeypatch.setattr(adapter, "_prepare_model_profile", prepared)
    monkeypatch.setattr(adapter, "_native_file_profile", lambda: tmp_path / "synthetic-profile.sb")
    adapter.execute("self-authored prompt")
    command = commands[0]
    assert command[:4] == ["/usr/bin/sandbox-exec", "-f", str(tmp_path / "synthetic-profile.sb"), "/synthetic/verified-codex"]
    assert command[command.index("--model") + 1] == "gpt-5.6-sol"
    options = [command[i + 1] for i, item in enumerate(command) if item == "-c"]
    table = next(i for i, item in enumerate(options) if item.startswith("mcp_servers="))
    approvals = [item for item in options if "approval_mode" in item]
    assert approvals == [f'mcp_servers.curis.tools.{name}.approval_mode="approve"'
                         for name in ("read_skill", "write_output", "browser")]
    assert all(options.index(item) > table for item in approvals)
    assert not any("approval_policy" in item or ".default" in item for item in options)
    assert 'tools.experimental_request_user_input.enabled=false' in options
    assert 'features.image_generation=false' in options and 'features.multi_agent_v2=false' in options
    assert "model_catalog_json=" + json.dumps(str(catalog)) in options


def test_native_os_profiles_bind_runtime_root_and_deny_metadata_network(tmp_path, monkeypatch):
    import app.agent_adapter as module
    runtime = tmp_path / "0.144.6-aarch64-apple-darwin"
    (runtime / "bin").mkdir(parents=True)
    executable = runtime / "bin/codex"
    executable.write_bytes(b"self-authored fixture, never launched")
    temporary = tmp_path / "temporary"
    temporary.mkdir()
    adapter = module.CodexCliAdapter(cwd=str(tmp_path), executable=str(executable),
        environment={"TMPDIR": str(temporary)})
    monkeypatch.setattr(module, "installation_id_snapshot", lambda path: {"synthetic": True})
    metadata = adapter._native_file_profile(metadata_only=True).read_text()
    generation = adapter._native_file_profile().read_text()
    assert "(deny network*)" in metadata
    assert 'auth.json' not in metadata and 'models_cache.json' not in metadata
    assert str(runtime) in metadata and str(runtime) in generation
    assert "(deny file-write*)" in metadata and "(deny file-write*)" in generation
    assert "file-write-data (literal" in metadata
    assert "auth.json" in generation and "models_cache.json" in generation


def test_finder_discovers_verified_standard_codex_without_path_or_test_pin(tmp_path, monkeypatch):
    import hashlib
    import app.agent_adapter as module
    monkeypatch.delenv("CURIS_CODEX_EXECUTABLE", raising=False)
    monkeypatch.setattr(module.shutil, "which", lambda command: None)
    executable = tmp_path / "public-runtime/bin/codex"
    real_path = module.Path
    class SyntheticHome:
        def __truediv__(self, relative):
            assert relative == ".codex/packages/standalone/releases/0.144.6-aarch64-apple-darwin/bin/codex"
            return executable
    class SyntheticPaths:
        def __new__(cls, value): return real_path(value)
        @staticmethod
        def home(): return SyntheticHome()
    monkeypatch.setattr(module, "Path", SyntheticPaths)
    executable.parent.mkdir(parents=True)
    executable.write_bytes(b"self-authored discovery fixture, never executed")
    executable.chmod(0o700)
    monkeypatch.setattr(module, "PROVED_CODEX_SHA256", hashlib.sha256(executable.read_bytes()).hexdigest())
    assert module.local_codex_executable() == str(executable)
    monkeypatch.setenv("CURIS_CODEX_EXECUTABLE", str(tmp_path / "missing-managed-pin"))
    assert module.local_codex_executable() == ""  # Explicit pin never silently falls back.
    monkeypatch.delenv("CURIS_CODEX_EXECUTABLE")
    executable.write_bytes(b"modified fixture")
    assert module.local_codex_executable() == ""


def test_discovery_and_authorization_probe_use_the_same_resolved_executable(monkeypatch):
    import subprocess
    import app.agent_adapter as adapter
    import app.ai_capability_registry as registry
    calls = []
    monkeypatch.setattr(adapter, "local_codex_executable", lambda: "/synthetic/verified/codex")
    def fake_run(argv, **kwargs):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, "synthetic version", "")
    monkeypatch.setattr(registry.subprocess, "run", fake_run)
    assert registry._command_status("codex") == (True, "synthetic version")
    assert registry._run_probe("codex", ["login", "status"])
    assert calls == [["/synthetic/verified/codex", "--version"], ["/synthetic/verified/codex", "login", "status"]]


def _publication_case(tmp_path, monkeypatch, direction="writing"):
    from backend.tests.test_company_execution_policy import policy_ready, HEADERS
    from backend.tests.test_professional_conversation_journeys import _agent_professional_source
    from backend.tests.test_writing_chapter_vertical import COMPANY
    fixture = policy_ready(tmp_path, monkeypatch)
    db, app, _, _, calls, workspace, _, binding, _ = fixture
    if direction != "content-growth":
        workspace, binding, _ = _agent_professional_source(direction, db, app, tmp_path)
    assignment = binding["context"]["assignment_ref"]
    path = "/api/workspace/runtime/foundation/team-operating/assignments/" + assignment + "/agent-workflow"
    return db, app, path, {"company_id": COMPANY, "workspace_id": workspace}, assignment, calls, HEADERS


def _publication_body(basis):
    return {key: basis[key] for key in ("company_id", "workspace_id", "review_token")} | {
        "expected_revision": basis["assignment_revision"], "confirm": True}


def _publication_preserved_state(db):
    # Only this test's synthetic database is inspected. A publication may add a
    # workflow row; every other table and runtime entity must remain unchanged.
    with db.connect() as connection:
        names = [row[0] for row in connection.execute(
            "select name from sqlite_master where type='table' order by name")]
        state = {}
        for name in names:
            quoted = '"' + name.replace('"', '""') + '"'
            where = " where entity_type != 'RESPONSIBILITY_WORKFLOW'" if name == "runtime_entities" else ""
            state[name] = sorted([tuple(row) for row in connection.execute("select * from " + quoted + where)], key=repr)
        return state


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
def test_professional_workflow_publication_is_explicit_idempotent_and_has_no_execution_effects(tmp_path, monkeypatch, direction):
    from fastapi.testclient import TestClient
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch, direction)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        before = _publication_preserved_state(db)
        review = client.get(path, params=query, headers=headers)
        assert review.status_code == 200, review.text
        basis = review.json()
        assert basis["state"] == "NEEDS_PUBLICATION" and basis["matching_count"] == 0, basis
        assert basis["publication_allowed"] and basis["assignment_ref"] == assignment
        assert _publication_preserved_state(db) == before
        body = _publication_body(basis)
        cancelled = client.post(path, headers=headers, json=body | {"confirm": False})
        assert cancelled.status_code == 422
        assert _publication_preserved_state(db) == before
        published = client.post(path, headers=headers, json=body)
        assert published.status_code == 200, published.text
        result = published.json()
        assert result["state"] == "READY" and result["matching_count"] == 1 and result["published"]
        assert result["workflow"]["version"] == 1
        assert result["workflow"]["default_flow"] == [basis["responsibility_key"]]
        repeated = client.post(path, headers=headers, json=body)
        assert repeated.status_code == 200 and repeated.json()["published"] is False, repeated.text
        assert repeated.json()["workflow"] == result["workflow"]
        assert _publication_preserved_state(db) == before
        assert calls == []


@pytest.mark.parametrize("direction", ["content-growth", "writing", "music"])
def test_professional_workflow_counts_latest_versions_and_rejects_multiple_keys(tmp_path, monkeypatch, direction):
    from fastapi.testclient import TestClient
    from app.runtime import ResponsibilityRoutingRuntime
    from backend.tests.test_writing_chapter_vertical import scope
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch, direction)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(path, params=query, headers=headers).json()
        first = client.post(path, headers=headers, json=_publication_body(basis))
        assert first.status_code == 200, first.text
        with scope():
            routing = ResponsibilityRoutingRuntime(db)
            # A second version of the same key is one latest workflow, not two.
            routing.publish_workflow(**query, scope_type=basis["scope_type"], scope_ref=basis["scope_ref"],
                workflow_key=basis["workflow_key"], assignment_refs=[assignment], default_flow=[basis["responsibility_key"]])
        latest = client.get(path, params=query, headers=headers).json()
        assert latest["matching_count"] == 1 and latest["workflow"]["version"] == 2
        repeated = client.post(path, headers=headers, json=_publication_body(latest))
        assert repeated.status_code == 200 and repeated.json()["workflow"]["version"] == 2
        with scope():
            routing.publish_workflow(**query, scope_type=basis["scope_type"], scope_ref=basis["scope_ref"],
                workflow_key="independent-conflicting-flow", assignment_refs=[assignment], default_flow=[basis["responsibility_key"]])
        ambiguous = client.get(path, params=query, headers=headers).json()
        assert ambiguous["matching_count"] == 2 and ambiguous["state"] == "AMBIGUOUS"
        assert ambiguous["publication_allowed"] is False
        before = _publication_preserved_state(db)
        refused = client.post(path, headers=headers, json=_publication_body(ambiguous))
        assert refused.status_code == 409 and calls == []
        assert _publication_preserved_state(db) == before


@pytest.mark.parametrize("failure", ["foreign-tenant", "foreign-company", "foreign-workspace", "missing-ceo", "other-ceo", "member", "stale", "changed-employee", "inactive", "generic"])
def test_workflow_publication_rejects_identity_scope_or_review_changes(tmp_path, monkeypatch, failure):
    import json
    from fastapi.testclient import TestClient
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
    from app.tenant_context import TenantContext
    from backend.tests.test_writing_chapter_vertical import scope
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(path, params=query, headers=headers).json()
        body = _publication_body(basis)
        sent_headers = dict(headers)
        if failure == "foreign-tenant":
            sent_headers["X-Tenant-Id"] = "foreign-tenant"
        elif failure in {"foreign-company", "foreign-workspace"}:
            body["company_id" if failure == "foreign-company" else "workspace_id"] = "foreign-scope"
        elif failure == "missing-ceo":
            sent_headers.pop("X-Ceo-Id")
        elif failure == "other-ceo":
            sent_headers["X-Ceo-Id"] = "different-ceo"
        elif failure == "member":
            current = TenantContext.current_identity
            monkeypatch.setattr(TenantContext, "current_identity", classmethod(lambda cls: {**current(), "role": "member"}))
        elif failure in {"stale", "changed-employee", "inactive"}:
            with scope():
                foundation = RuntimeFoundation(db); routing = ResponsibilityRoutingRuntime(db)
                if failure == "inactive":
                    with db.connect() as connection:
                        connection.execute("update runtime_entities set lifecycle_status='INACTIVE' where tenant_id='selfuse' and entity_id=?", (assignment,))
                elif failure == "changed-employee":
                    employee = foundation.create("AI_EMPLOYEE", **query, lifecycle_status="AVAILABLE", data={"name": "另一员工"})
                    routing.update_assignment(assignment, employee_ref=employee["entity_id"])
                else:
                    routing.update_assignment(assignment, responsibility="已修改的责任")
        elif failure == "generic":
            with db.connect() as connection:
                raw = connection.execute("select blueprint_json from workspaces where workspace_id=?", (query["workspace_id"],)).fetchone()[0]
                blueprint = json.loads(raw); blueprint["productForm"] = "GENERIC"
                connection.execute("update workspaces set blueprint_json=? where workspace_id=?",
                    (json.dumps(blueprint), query["workspace_id"]))
            generic = client.get(path, params=query, headers=headers).json()
            assert generic["state"] == "UNSUPPORTED" and not generic["publication_allowed"]
        before = _publication_preserved_state(db)
        rejected = client.post(path, headers=sent_headers, json=body)
        assert rejected.status_code in {403, 404, 409}, (failure, rejected.text)
        assert _publication_preserved_state(db) == before
        assert calls == []
        with scope():
            workflows = RuntimeFoundation(db).list("RESPONSIBILITY_WORKFLOW", **query)
        assert workflows == []


def test_existing_unique_workflow_with_stale_assignment_is_not_reused(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.runtime import ResponsibilityRoutingRuntime
    from backend.tests.test_writing_chapter_vertical import scope
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(path, params=query, headers=headers).json()
        assert client.post(path, headers=headers, json=_publication_body(basis)).status_code == 200
        with scope():
            ResponsibilityRoutingRuntime(db).update_assignment(assignment, responsibility="新的责任")
        stale = client.get(path, params=query, headers=headers).json()
        assert stale["matching_count"] == 1 and stale["state"] == "STALE"
        assert client.post(path, headers=headers, json=_publication_body(stale)).status_code == 409
        assert calls == []


def test_concurrent_duplicate_publication_creates_one_version_and_rolls_back_failed_publication(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    from fastapi.testclient import TestClient
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime, RuntimeScopeError
    from backend.tests.test_writing_chapter_vertical import scope
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(path, params=query, headers=headers).json()
        body = _publication_body(basis); before = _publication_preserved_state(db)
        original = ResponsibilityRoutingRuntime.publish_workflow
        def fail_after_insert(self, **kwargs):
            original(self, **kwargs)
            raise RuntimeScopeError("synthetic failure after canonical publication")
        with monkeypatch.context() as patch:
            patch.setattr(ResponsibilityRoutingRuntime, "publish_workflow", fail_after_insert)
            failed = client.post(path, headers=headers, json=body)
            assert failed.status_code == 403
        with scope():
            assert RuntimeFoundation(db).list("RESPONSIBILITY_WORKFLOW", **query) == []
        assert _publication_preserved_state(db) == before
        barrier = Barrier(2)
        def publish():
            barrier.wait(timeout=5)
            return client.post(path, headers=headers, json=body)
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(publish), pool.submit(publish)]
            results = [future.result(timeout=10) for future in futures]
        assert [result.status_code for result in results] == [200, 200], [result.text for result in results]
        assert sorted(result.json()["published"] for result in results) == [False, True]
        assert results[0].json()["workflow"] == results[1].json()["workflow"]
        with scope():
            workflows = RuntimeFoundation(db).list("RESPONSIBILITY_WORKFLOW", **query)
        assert len(workflows) == 1 and workflows[0]["data"]["version"] == 1
        assert _publication_preserved_state(db) == before and calls == []


def test_workflow_publication_serializes_assignment_edit_and_next_read_detects_staleness(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    from fastapi.testclient import TestClient
    from app.runtime import ResponsibilityRoutingRuntime
    from backend.tests.test_writing_chapter_vertical import scope
    db, app, path, query, assignment, calls, headers = _publication_case(tmp_path, monkeypatch)
    inserted, edit_started, edit_finished = Event(), Event(), Event()
    original = ResponsibilityRoutingRuntime.publish_workflow
    def publication(self, **kwargs):
        value = original(self, **kwargs)
        inserted.set()
        assert edit_started.wait(3)
        assert not edit_finished.wait(0.1), "assignment edit escaped the publication transaction"
        return value
    monkeypatch.setattr(ResponsibilityRoutingRuntime, "publish_workflow", publication)
    with TestClient(app, client=("127.0.0.1", 49180)) as client:
        basis = client.get(path, params=query, headers=headers).json()
        def edit():
            assert inserted.wait(3)
            edit_started.set()
            with scope():
                ResponsibilityRoutingRuntime(db).update_assignment(assignment, responsibility="稍后修改的责任")
            edit_finished.set()
        with ThreadPoolExecutor(max_workers=2) as pool:
            update = pool.submit(edit)
            published = pool.submit(lambda: client.post(path, headers=headers, json=_publication_body(basis)))
            response = published.result(timeout=10); update.result(timeout=10)
        assert response.status_code == 200, response.text
        current = client.get(path, params=query, headers=headers).json()
        assert current["state"] == "STALE" and current["assignment_revision"] == basis["assignment_revision"] + 1
        assert calls == []



@pytest.mark.parametrize("backend",["NATIVE_BROWSERSKILL","VM",None])
@pytest.mark.parametrize("failure",[None,"register","build","execute","cancel","no-browser","factory","lock","unknown-kind"])
def test_main_native_browser_work_tool_result_and_finally_close_without_app_or_database(monkeypatch,failure,backend):
    import ast,json,os,sys,types
    import app
    import app.agent_browser_runtime as browser_runtime
    from app.agent_tool_server import AgentToolSessions
    events,stopped,frames=[],[False],[]
    identity={"tenant_id":"tenant","company_id":"company","work_ref":"work","task_id":"task"}
    resources=types.SimpleNamespace(path=Path("/synthetic-owned/agent-work/work"),identity=identity)
    resources.prepare=lambda packages,**options:{"cwd":str(resources.path),"environment":{},"receipt":{"skills":[]}}
    work={"data":{"cycleRef":"cycle"}}
    hosts=[] if failure=="no-browser" else ["example.com"]
    cycle={"data":{"contract":{"agentBrowser":{"hosts":hosts}}}}
    class Foundation:
        def __init__(self,database):assert database.path=="/synthetic-owned/curis.sqlite"
        def get(self,ref):return work if ref=="work" else cycle
    # Substitute only dependencies of the actual production nested function.
    # Never import main or initialize its app, dotenv loader, database or provider.
    fake_runtime=types.ModuleType("app.runtime");fake_runtime.RuntimeFoundation=Foundation
    fake_api=types.ModuleType("app.api");fake_api.__path__=[]
    fake_router=types.ModuleType("app.api.team_operating_router")
    fake_router.verified_prior_for_work=lambda *args:None
    fake_router.prior_binding_digest=lambda value:"none"
    for name,module in [("app.runtime",fake_runtime),("app.api",fake_api),("app.api.team_operating_router",fake_router)]:
        monkeypatch.setitem(sys.modules,name,module)
    monkeypatch.setattr(app,"runtime",fake_runtime,raising=False)
    monkeypatch.setattr(app,"api",fake_api,raising=False)
    class Browser:
        session,browser_id,tab="daemon-session","owned-browser",None
        close_count=0
        def call(self,arguments,scoped):
            assert scoped is resources and scoped.identity==identity
            self.tab=7
            events.append(("browser",arguments["action"]))
            return {"url":"https://example.com/public","text":"self-authored public content","content_verification":"UNVERIFIED"}
        def close(self):self.close_count+=1;events.append(("browser-close",))
    browser=Browser()
    def open_browser(bound,allowed,should_stop,*,root=None,metadata=None):
        assert bound=={**identity,"employee_id":"employee","binding_ref":"binding"}
        assert allowed==hosts
        if backend=="NATIVE_BROWSERSKILL":
            assert str(root)=="/synthetic-owned/agent-browser" and metadata=={"source":"synthetic-binding"}
        else:assert root is metadata is None
        assert not should_stop()
        events.append(("browser-entry",backend))
        if failure=="factory":raise ValueError("synthetic denied native factory")
        return browser
    monkeypatch.setattr(browser_runtime,"open_native_browser_for_work",open_browser)
    monkeypatch.setattr(browser_runtime,"open_reader_for_work",open_browser)
    def reader_lock():
        if failure=="lock":raise ValueError("synthetic unreleased lock")
        return {"runtimeKind":"UNKNOWN" if failure=="unknown-kind" else backend}
    monkeypatch.setattr(browser_runtime,"load_trusted_reader_lock",reader_lock)
    class Tools(AgentToolSessions):
        def register(self,*args,**options):
            if failure=="register":raise RuntimeError("synthetic register failure")
            return super().register(*args,**options)
    tools=Tools()
    def build(metadata,**options):
        events.append(("build",))
        if failure=="build":raise RuntimeError("synthetic executor assembly failure")
        context=options["execution_context"]
        token=context["environment"]["CURIS_AGENT_TOOL_TOKEN"]
        def execute(prompt):
            events.append(("execute",))
            if failure=="execute":raise ValueError("synthetic executor failure")
            offered=tools.handle(token,{"jsonrpc":"2.0","id":1,"method":"tools/list"})["result"]["tools"]
            assert ("browser" in [tool["name"] for tool in offered])==(failure!="no-browser")
            if failure=="cancel":stopped[0]=True
            if hosts:
                for action in ["navigate","observe"]:
                    arguments={"action":action,**({"url":"https://example.com/public"} if action=="navigate" else {})}
                    reply=tools.handle(token,{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser","arguments":arguments}})
                    assert not reply["result"]["isError"]
                    frames.append(json.loads(reply["result"]["content"][0]["text"]))
            return {"output":"self-authored original Work result"}
        return types.SimpleNamespace(execute=execute)
    def accept(response,scoped,token,executor):
        assert callable(executor.execute)
        assert scoped is resources
        return {**response,"original_work":identity["work_ref"],"browser_tool_calls":tools.browser_evidence(token)}
    source=Path(__file__).resolve().parents[1]/"app/main.py"
    node=next(n for n in ast.walk(ast.parse(source.read_text())) if isinstance(n,ast.FunctionDef) and n.name=="run_scoped_agent")
    namespace={"__package__":"app","__name__":"app._synthetic_native_entry_test","Path":Path,"os":os,"json":json,
        "release_owned_codex_session":lambda identity,capability:None,
        "require_agent_position":lambda capability:None,"runtime_capability":{"id":"agent","company_id":"company","work_ref":"work"},
        "resources":resources,"packages":[],"database":types.SimpleNamespace(path="/synthetic-owned/curis.sqlite"),
        "metadata":{"source":"synthetic-binding",**({"runtimeKind":"NATIVE_BROWSERSKILL","browserImageDigest":"sha256:forged"}
            if backend!="NATIVE_BROWSERSKILL" else {})},"agent_task":"task","agent_employee":"employee","agent_binding":"binding",
        "TenantContext":types.SimpleNamespace(current_tenant_id=lambda:"tenant"),"agent_stopped":lambda:stopped[0],
        "agent_tools":tools,"build_agent_executor":build,"resolved_api_key":None,"default_executor":None,
        "agent_progress":lambda *args:None,"agent_local_state":lambda *args:None,"allowance":{"max_seconds":90},
        "accept_agent_response":accept,"reserve_original_agent_call":lambda:(_ for _ in ()).throw(AssertionError("reserved paid provider call"))}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),"exec"),namespace)
    if failure in {"register","build","execute","cancel","factory","lock","unknown-kind"}:
        with pytest.raises((RuntimeError,ValueError,PermissionError)):namespace["run_scoped_agent"]("self-authored prompt")
    else:
        result=namespace["run_scoped_agent"]("self-authored prompt")
        assert result["original_work"]=="work" and result["output"]=="self-authored original Work result"
        assert [row["action"] for row in result["browser_tool_calls"]]==([] if failure=="no-browser" else ["navigate","observe"])
        if hosts:assert all(row["content_verification"]=="UNVERIFIED" for row in result["browser_tool_calls"])
    assert tools.sessions=={} and browser.close_count==(0 if failure in {"no-browser","factory","lock","unknown-kind"} else 1)
    if failure in {"lock","unknown-kind"}:assert events==[]
    if failure=="cancel":assert not frames and not any(event[0]=="browser" for event in events)


@pytest.mark.parametrize('state',['missing','closed','revoked-during-collection'])
def test_main_accept_agent_result_requires_container_close_before_artifacts(tmp_path,state):
    import ast,types
    from app.agent_adapter import CodexCliAdapter,AgentExecutionError
    source=Path(__file__).resolve().parents[1]/'app/main.py'
    node=next(n for n in ast.walk(ast.parse(source.read_text())) if isinstance(n,ast.FunctionDef) and n.name=='accept_agent_response')
    events=[];revoked=[False]
    adapter=CodexCliAdapter(cwd=str(tmp_path))
    if state!='missing':adapter.container_stop_receipt={'ledger_state':'CLOSED_VERIFIED','container_id':'c'*64,'exit_codes':{'c'*64:137}}
    def collect():
        events.append('collect')
        if state=='revoked-during-collection':revoked[0]=True
        return []
    tools=types.SimpleNamespace(evidence=lambda token:events.append('skills') or [],browser_evidence=lambda token:[])
    namespace={'__package__':'app','agent_stopped':lambda:revoked[0],'agent_tools':tools,'allowance':{'authorization_ref':'synthetic'}}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),namespace)
    if state=='closed':
        result=namespace['accept_agent_response']({},types.SimpleNamespace(collect=collect),'synthetic',adapter)
        assert result['artifact_receipts']==[] and events==['skills','collect']
    else:
        with pytest.raises(AgentExecutionError):namespace['accept_agent_response']({},types.SimpleNamespace(collect=collect),'synthetic',adapter)
        assert events==([] if state=='missing' else ['skills','collect'])


def test_acp_main_gate_runs_before_credentials_or_preparation(monkeypatch):
    import ast
    import app.agent_adapter as module
    tree = ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())
    block = next(node for node in ast.walk(tree) if isinstance(node, ast.If)
                 and any(isinstance(child, ast.Constant) and child.value == "acp-stdio" for child in ast.walk(node.test))
                 and any(isinstance(child, ast.ImportFrom) and any(alias.name == "require_acp_execution_available" for alias in child.names) for child in node.body))
    namespace = {"__name__": "app.main", "__package__": "app", "metadata": {"kind": "acp-stdio", "credential_ref": "forbidden"}}
    with pytest.raises(module.AgentExecutionError) as error:
        exec(compile(ast.Module(body=[block], type_ignores=[]), "<actual-acp-precredential-gate>", "exec"), namespace)
    assert error.value.status == "acp_execution_held" and not error.value.outbound_attempted


def test_acp_installation_identity_is_bounded_and_rechecked(tmp_path, monkeypatch):
    import plistlib
    import hashlib
    import app.ai_capability_registry as registry
    from test_ai_capability_registry import _synthetic_app
    application = tmp_path / "Synthetic.app"
    _synthetic_app(application)
    metadata_path = application / "Contents/Info.plist"
    metadata = plistlib.loads(metadata_path.read_bytes())
    metadata["CFBundleShortVersionString"] = "synthetic"
    metadata_path.write_bytes(plistlib.dumps(metadata))
    launcher = application / "Contents/MacOS/synthetic-agent"
    digest = hashlib.sha256(launcher.read_bytes()).hexdigest()
    monkeypatch.setattr(registry, "ACP_INSTALLATIONS", {"synthetic": {
        "application": str(application), "bundle_id": "test.synthetic.agent", "version": "synthetic",
        "launcher": "Contents/MacOS/synthetic-agent", "files": {"Contents/MacOS/synthetic-agent": digest}, "args": ["--profile", "acp"],
        "profile_directory": ".dsh/profiles/acp", "profile_environment": {"DSH_HOME": ".dsh"}}})
    first = registry.acp_installation("synthetic")
    assert first["command"] == [str(launcher), "--profile", "acp"]
    assert registry.acp_installation("synthetic") == first
    launcher.chmod(0o600)
    with pytest.raises(ValueError): registry.acp_installation("synthetic")
    launcher.chmod(0o700)
    launcher.write_bytes(b"changed")
    with pytest.raises(ValueError): registry.acp_installation("synthetic")
    with pytest.raises(ValueError): registry.acp_installation("unknown")


def test_acp_result_and_unknown_usage_stay_on_original_canonical_work(tmp_path):
    from app.ai_usage import AIUsageService
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext
    from app.employee_execution_identity import EmployeeExecutionIdentity
    from app.evolution_event_log import EvolutionEventLog
    from app.runtime import ResponsibilityRoutingRuntime
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from test_v1_general_operating_contract import seed, add_team, TENANT, COMPANY, WORKSPACE, EMPLOYEE
    database = seed(tmp_path / "acp-canonical.sqlite")
    add_team(database)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        work = GeneralWorkspaceDelivery(database).create_work(company_id=COMPANY, workspace_id=WORKSPACE,
            problem="synthetic task", expected_result="synthetic result", constraints=["synthetic only"],
            references=["brief:synthetic"], idempotency_key="acp-work")["work"]
        work_ref = work["entity_id"]
        routing = ResponsibilityRoutingRuntime(database)
        key = "acp:synthetic:1"
        routing.begin_employee_execution(work_ref, execution_key=key)
        store = ResultStore(database)
        task = store.create_task("synthetic prompt", company_id=COMPANY, workspace_id=WORKSPACE,
            scope_type="WORKSPACE", scope_ref=WORKSPACE, work_ref=work_ref, execution_ref=key,
            capability_source="tenant_private", capability_type="agent", capability_id="agent.general.local", employee_id=EMPLOYEE)
        identity = EmployeeExecutionIdentity(database)
        identity.bind(company_id=COMPANY, workspace_id=WORKSPACE, runtime_employee_ref=EMPLOYEE,
            company_employee_ref=EMPLOYEE, employee_capability_binding_ref="binding-general")
        assignment = work["data"]["responsibilityAssignmentRef"]
        routing.attach_provider_task(work_ref, execution_key=key, task_ref=task["task_id"])
        current = routing._pinned(work_ref)[3]
        identity.record_task_assignment(company_id=COMPANY, workspace_id=WORKSPACE, runtime_employee_ref=EMPLOYEE,
            assignment_ref=assignment, assignment_revision=current["assignmentRevision"],
            task_ref=task["task_id"], employee_capability_binding_ref="binding-general")
        EvolutionEventLog(database).record(correlation_id=work_ref, event_type="team.execution_task_bound",
            idempotency_key="acp-task-bound", payload={"work_ref": work_ref, "execution_key": key, "task_ref": task["task_id"]})
        usage = AIUsageService(database)
        arguments = dict(tenant_id=TENANT, model_gateway_id="acp-stdio", provider_id="acp-stdio", model_name="acp-agent",
            input_tokens=None, output_tokens=None, total_tokens=None, cost_amount=None, currency="USD", cost_source="unknown",
            price_version=None, employee_id=EMPLOYEE, capability_id="agent.general.local", capability_type="agent",
            task_id=task["task_id"], project_id=None, department_id=None, request_id="acp-request", execution_status="success",
            metering_status="unknown", idempotency_key="acp-call", capability_binding_id="binding-general")
        record_id = usage.record_call(**arguments)
        assert usage.record_call(**arguments) == record_id
        record = usage.get_record(record_id)
        assert (record["work_ref"], record["execution_ref"], record["workspace_id"], record["company_id"]) == (work_ref, key, WORKSPACE, COMPANY)
        assert record["total_tokens"] is None and record["cost_amount"] is None
        store.transition(task["task_id"], "COMPLETED", {"output": "synthetic result"})
        routing.finish_employee_execution(work_ref, execution_key=key, status="ACCEPTED", task_ref=task["task_id"],
            session_ref="acp-synthetic-session", result_ref="task:"+task["task_id"], result_summary="synthetic result")
        assert store.get_task(task["task_id"])["work_ref"] == work_ref
        with pytest.raises((ValueError, KeyError)): usage.record_call(**{**arguments, "employee_id": "foreign", "idempotency_key": "foreign"})
    with TenantContext.scope("foreign", role="test"):
        with pytest.raises((PermissionError, KeyError)): usage.record_call(**arguments)


@pytest.mark.parametrize("audit_fails", [False, True])
def test_acp_stop_audit_preserves_scope_and_always_closes_tools(tmp_path, audit_fails):
    import ast
    from types import SimpleNamespace
    from app.agent_adapter import AcpStdioAdapter
    tree = ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())
    block = next(node for node in ast.walk(tree) if isinstance(node, ast.Try) and node.body
                 and isinstance(node.body[0], ast.ImportFrom)
                 and any(alias.name == "AcpStdioAdapter" for alias in node.body[0].names)
                 and any(isinstance(child, ast.Constant) and child.value == "agent.execution.acp_stop" for child in ast.walk(node)))
    executor = AcpStdioAdapter(installation={}, cwd=str(tmp_path), profile_home=str(tmp_path / ".acp-home"))
    executor.cleanup = {"state": "UNKNOWN", "external_effects": "UNKNOWN"}
    records, closed = [], []
    def record(**value):
        records.append(value)
        if audit_fails: raise RuntimeError("synthetic audit unavailable")
    namespace = {"__name__": "app.main", "__package__": "app", "executor": executor,
                 "event_log": SimpleNamespace(record=record), "agent_task": "task",
                 "runtime_capability": {"work_ref": "work"}, "tool_token": "synthetic-token",
                 "agent_tools": SimpleNamespace(close=lambda value: closed.append(value))}
    code = compile(ast.Module(body=[block], type_ignores=[]), "<actual-acp-stop-audit>", "exec")
    if audit_fails:
        with pytest.raises(RuntimeError): exec(code, namespace)
    else: exec(code, namespace)
    assert closed == ["synthetic-token"]
    assert records == [{"correlation_id": "task", "event_type": "agent.execution.acp_stop",
                        "payload": {"task_id": "task", "work_ref": "work", "cleanup": executor.cleanup}}]
    assert "synthetic-token" not in str(records)


def test_acp_normal_http_registration_grant_and_original_work_pipeline(tmp_path, monkeypatch):
    """Actual App endpoints/services; only provider execution and trusted test identity injected."""
    import asyncio
    import json
    import os
    import httpx
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeFoundation
    from app.model_gateway import ModelGatewayAdapter
    from app.ai_usage import AIUsageService
    import app.agent_adapter as adapter_module
    from test_ai_capability_registry import _synthetic_acp_installation
    from test_v1_general_operating_contract import seed, add_team, TENANT, COMPANY, WORKSPACE, EMPLOYEE
    _synthetic_acp_installation(tmp_path, monkeypatch)
    path = tmp_path / "normal-acp.sqlite"
    database = seed(path); add_team(database)
    with database.connect() as con:
        con.execute("update employee_instances set allowed_effect_classes_json='[\"exec\"]' where tenant_id=? and id=?", (TENANT,EMPLOYEE))
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setenv("CURIS_AGENT_TMP_ROOT", str(Path(os.environ["TMPDIR"]).parent))
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, "ceo", "owner", "active", request_id))
    model = ModelGatewayAdapter(base_url="https://synthetic.invalid", api_key="synthetic",
        http_post=lambda *_args: pytest.fail("fallback provider called"))
    application = create_app(str(path), model_gateway_adapter=model)
    calls = []
    def execute(self, prompt, **kwargs):
        self.before_launch()
        calls.append(prompt)
        (Path(self.cwd)/"output/result.txt").write_text("synthetic evidence")
        self.cleanup = {"state": "CLOSED", "external_effects": "UNKNOWN"}
        return {"output": json.dumps({"status":"ACCEPTED","resultType":"general-business-result","summary":"synthetic result","problem":""}),
                "session_id":"synthetic-acp-session", "model_gateway_id":"acp-stdio", "model_name":"acp-agent", "provider_id":"acp-stdio",
                "prompt_tokens":None,"completion_tokens":None,"total_tokens":None,"status":"success","outbound_attempted":True,"artifacts":[]}
    monkeypatch.setattr(adapter_module.AcpStdioAdapter, "execute", execute)
    with TenantContext.scope(TENANT,company_id=COMPANY,ceo_id="ceo",role="owner"):
        assignment = RuntimeFoundation(database).list("RESPONSIBILITY_ASSIGNMENT",company_id=COMPANY,workspace_id=WORKSPACE)[0]["entity_id"]
    headers = {"X-Tenant-Id":TENANT,"X-Ceo-Id":"ceo"}
    root = "/api/workspace/runtime/foundation/team-operating"
    allowance = f"/api/workspace/v1/companies/{COMPANY}/agent-allowance"
    async def exercise():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application),base_url="http://test",headers=headers) as client:
            response = await client.get("/api/workspace/ai-capabilities/local?metadata_only=true")
            assert response.status_code == 200, response.text
            row, = response.json()["agents"]
            assert row["bindable"] and not row["execution_ready"]
            payload = {"capability_type":"agent","capability_id":row["capability_id"],"display_name":"Synthetic DSH","metadata":{"local_agent_ref":row["discovery_ref"]}}
            response = await client.post("/api/workspace/capabilities/private",json=payload)
            assert response.status_code == 201, response.text
            assert response.json()["metadata"]["kind"] == "acp-stdio" and response.json()["status"] == "active"
            response = await client.post(f"/api/workspace/employees/{EMPLOYEE}/agent-bindings",json={"company_id":COMPANY,"capability_id":row["capability_id"]})
            assert response.status_code == 200, response.text
            binding = next(item["id"] for item in response.json()["bindings"] if item["capability_id"] == row["capability_id"])
            foreign = await client.post(f"/api/workspace/employees/{EMPLOYEE}/agent-bindings",json={"company_id":"foreign","capability_id":row["capability_id"]})
            assert foreign.status_code == 422
            denied = await client.get(allowance, headers={"X-Tenant-Id":"foreign", "X-Ceo-Id":"ceo"})
            assert denied.status_code in {403,404,422}
            response = await client.get(allowance); assert response.status_code == 200,response.text
            initial = response.json()
            assert any(item["binding_ref"] == binding and item["agent_kind"] == "acp-stdio" for item in initial["binding_options"])
            wrong = await client.put(allowance,json={"request_id":"reuse-codex","expected_revision":initial["revision"],"authorization_ref":initial["authorization_ref"],"enabled":True,"consent":True,"binding_refs":[binding]})
            assert wrong.status_code == 422
            async def new_work(key):
                result = await client.post(root+f"/assignments/{assignment}/work",json={"request_id":key,"problem":"synthetic task","expected_result":"synthetic result","agent_binding_ref":binding,"source":{"kind":"references","references":[]}})
                assert result.status_code == 200,result.text
                return result.json()["work"]["entity_id"]
            blocked = await new_work("no-grant")
            await client.post(root+f"/works/{blocked}/execute?max_executions=1")
            assert not calls
            codex = await client.post("/api/workspace/capabilities/private", json={"capability_type":"agent","capability_id":"agent.synthetic.codex","display_name":"Synthetic Codex","metadata":{"kind":"codex-cli"}})
            assert codex.status_code == 201,codex.text
            codex = await client.post(f"/api/workspace/employees/{EMPLOYEE}/agent-bindings", json={"company_id":COMPANY,"capability_id":"agent.synthetic.codex"})
            assert codex.status_code == 200,codex.text
            codex_binding = next(item["id"] for item in codex.json()["bindings"] if item["capability_id"] == "agent.synthetic.codex")
            codex = await client.put(allowance,json={"request_id":"explicit-codex","expected_revision":initial["revision"],"authorization_ref":initial["authorization_ref"],"enabled":True,"consent":True,"binding_refs":[codex_binding]})
            assert codex.status_code == 200,codex.text
            initial = codex.json()
            codex_only = await new_work("codex-only-grant")
            await client.post(root+f"/works/{codex_only}/execute?max_executions=1")
            assert not calls and (await client.get(allowance)).json()["used_calls"] == 0
            response = await client.post(f"/api/workspace/v1/companies/{COMPANY}/agent-authorizations",json={"request_id":"explicit-acp","expected_revision":initial["revision"],"previous_authorization_ref":initial["authorization_ref"],"consent":True,"binding_refs":[binding]})
            assert response.status_code == 200,response.text
            grant = response.json()
            assert grant["authorization_ref"] != initial["authorization_ref"]
            held = await new_work("gate-held")
            await client.post(root+f"/works/{held}/execute?max_executions=1")
            assert not calls
            assert (await client.get(allowance)).json()["used_calls"] == 0
            monkeypatch.setattr(adapter_module,"ACP_LOCAL_EXECUTION_VERIFIED",True) # Synthetic provider only.
            work = await new_work("allowed")
            response = await client.post(root+f"/works/{work}/execute?max_executions=1")
            assert response.status_code == 200,response.text
            assert len(calls) == 1,response.text
            assert response.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED",response.text
            current = (await client.get(allowance)).json()
            assert current["used_calls"] == 1 and current["authorization_ref"] == grant["authorization_ref"]
            await client.post(root+f"/works/{work}/execute?max_executions=1")
            assert len(calls) == 1
            with TenantContext.scope(TENANT,company_id=COMPANY,ceo_id="ceo",role="owner"):
                records = AIUsageService(database).list_records(work_ref=work)
                assert len(records) == 1
                record = records[0]
                assert record["capability_id"] == row["capability_id"] and record["capability_binding_id"] == binding
                assert record["work_ref"] == work and record["execution_status"] == "success"
                assert record["total_tokens"] is None and record["cost_amount"] is None
            # Same canonical registration: compare-and-set edit retains bindings, results and usage.
            items = (await client.get("/api/workspace/capabilities/private?capability_type=agent")).json()["capabilities"]
            original = next(item for item in items if item["capability_id"] == row["capability_id"])
            edit_url = "/api/workspace/capabilities/private/agent/" + row["capability_id"] + "/dsh-account"
            edit = {"company_id": COMPANY, "expected_revision": original["revision"], "dsh_shared_account": True, "consent": True}
            with database.connect() as con:
                bindings_before = [dict(item) for item in con.execute("select * from employee_capability_bindings order by id")]
                task = con.execute("select task_id,status from tasks where work_ref=?", (work,)).fetchone()
                con.execute("update tasks set status='RUNNING' where task_id=?", (task["task_id"],))
            busy = await client.patch(edit_url, json=edit)
            assert busy.status_code == 409, busy.text
            with database.connect() as con:
                con.execute("update tasks set status=? where task_id=?", (task["status"], task["task_id"]))
            assert (await client.patch(edit_url, json={**edit, "consent": False})).status_code == 422
            assert (await client.patch(edit_url, json={**edit, "dsh_shared_account": "true"})).status_code == 422
            assert (await client.patch(edit_url, json={**edit, "metadata": {}})).status_code == 422
            assert (await client.patch(edit_url, json={**edit, "company_id": "foreign"})).status_code == 403
            assert (await client.patch(edit_url, json=edit, headers={"X-Tenant-Id":"foreign", "X-Ceo-Id":"ceo"})).status_code == 403
            authorize = IdentityMembership._authorize_test
            monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
                AuthorizedMembership("synthetic-member", tenant_id, COMPANY, "ceo", "member", "active", request_id))
            assert (await client.patch(edit_url, json=edit)).status_code == 403
            monkeypatch.setattr(IdentityMembership, "_authorize_test", authorize)
            with database.connect() as con:
                con.execute("update employee_instances set company_id='foreign' where tenant_id=? and id=?", (TENANT, EMPLOYEE))
            assert (await client.patch(edit_url, json=edit)).status_code == 409
            with database.connect() as con:
                con.execute("update employee_instances set company_id=? where tenant_id=? and id=?", (COMPANY, TENANT, EMPLOYEE))
            competing = await asyncio.gather(client.patch(edit_url, json=edit), client.patch(edit_url, json=edit))
            assert sorted(item.status_code for item in competing) == [200, 409]
            saved = next(item for item in competing if item.status_code == 200)
            assert saved.status_code == 200, saved.text
            edited = saved.json()
            assert edited["capability_id"] == original["capability_id"] and edited["revision"] != original["revision"]
            assert edited["metadata"] == {**original["metadata"], "dsh_shared_account": True,
                "dsh_account_selection_revision": edited["metadata"]["dsh_account_selection_revision"]}
            assert len(edited["metadata"]["dsh_account_selection_revision"]) == 32
            assert (await client.patch(edit_url, json=edit)).status_code == 409
            with TenantContext.scope(TENANT,company_id=COMPANY,ceo_id="ceo",role="owner"):
                from app.company_execution_policy import CompanyExecutionPolicy
                from app.runtime import RuntimeScopeError
                with pytest.raises(RuntimeScopeError): CompanyExecutionPolicy(database).require_agent_execution(COMPANY, binding)
                assert AIUsageService(database).list_records(work_ref=work) == records
                assert RuntimeFoundation(database).get(work)["data"]["responsibilityRouting"]["status"] == "COMPLETED"
            back = await client.patch(edit_url, json={**edit, "expected_revision":edited["revision"], "dsh_shared_account":False})
            assert back.status_code == 200, back.text
            assert back.json()["revision"] != original["revision"]
            with TenantContext.scope(TENANT,company_id=COMPANY,ceo_id="ceo",role="owner"):
                with pytest.raises(RuntimeScopeError): CompanyExecutionPolicy(database).require_agent_execution(COMPANY, binding)
            again = await client.patch(edit_url, json={**edit, "expected_revision":back.json()["revision"]})
            assert again.status_code == 200, again.text
            with database.connect() as con:
                assert [dict(item) for item in con.execute("select * from employee_capability_bindings order by id")] == bindings_before
            unchanged = (await client.get(allowance)).json()
            assert unchanged["used_calls"] == 1 and unchanged["authorization_ref"] == grant["authorization_ref"]
            refreshed = await client.put(allowance, json={"request_id":"confirm-edited-dsh", "expected_revision":unchanged["revision"],
                "authorization_ref":unchanged["authorization_ref"], "enabled":True,"consent":True,"binding_refs":[binding]})
            assert refreshed.status_code == 200, refreshed.text
            current = refreshed.json()
            assert current["used_calls"] == 1 and current["remaining_calls"] == 3
            response = await client.post(allowance+"/revoke",json={"request_id":"revoke-acp","expected_revision":current["revision"],"authorization_ref":current["authorization_ref"],"enabled":False,"consent":False,"binding_refs":[]})
            assert response.status_code == 200,response.text
            revoked = await new_work("revoked")
            await client.post(root+f"/works/{revoked}/execute?max_executions=1")
            assert len(calls) == 1
    asyncio.run(exercise())


@pytest.mark.parametrize("agent_key", ["leader", "topic"])
def test_leader_mixed_existing_agent_and_api_preferences_with_normal_http(tmp_path, monkeypatch, agent_key):
    import asyncio
    import httpx
    import os
    from pathlib import Path
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.tenant_context import TenantContext
    from app.runtime import RuntimeFoundation
    from app.ai_usage import AIUsageService
    import app.agent_adapter as adapters
    from test_ai_capability_registry import _synthetic_acp_installation
    from backend.tests.test_team_operating_real_employee_e2e import (
        _leader_synthetic_setup, LeaderSyntheticProvider, TENANT, COMPANY, WORKSPACE, HEADERS, PREFIX,
    )
    _synthetic_acp_installation(tmp_path, monkeypatch)
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setenv("CURIS_AGENT_TMP_ROOT", str(Path(os.environ["TMPDIR"]).parent))
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    provider = LeaderSyntheticProvider()
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-mixed.sqlite", provider)
    employee = f"employee-{agent_key}"
    with database.connect() as con:
        con.execute("update employee_capability_bindings set enabled=0 where tenant_id=? and employee_id=? and capability_type='agent'", (TENANT, employee))
        con.execute("update employee_instances set allowed_effect_classes_json='[\"exec\"]' where tenant_id=? and id=?", (TENANT, employee))
    agent_calls = []
    def execute(self, prompt, **kwargs):
        self.before_launch()
        agent_calls.append(prompt)
        result = provider.execute(prompt)
        (Path(self.cwd) / "output/result.txt").write_text("synthetic delegated result")
        self.cleanup = {"state": "CLOSED", "external_effects": "UNKNOWN"}
        return {**result, "model_gateway_id": "acp-stdio", "model_name": "acp-agent", "provider_id": "acp-stdio",
            "prompt_tokens": None, "completion_tokens": None, "total_tokens": None, "outbound_attempted": True,
            "artifacts": []}
    monkeypatch.setattr(adapters.AcpStdioAdapter, "execute", execute)
    monkeypatch.setattr(adapters, "ACP_LOCAL_EXECUTION_VERIFIED", True)  # Synthetic adapter only; source gate stays false.
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            response = await client.get("/api/workspace/ai-capabilities/local?metadata_only=true")
            assert response.status_code == 200, response.text
            row, = response.json()["agents"]
            response = await client.post("/api/workspace/capabilities/private", json={"capability_type": "agent",
                "capability_id": row["capability_id"], "display_name": "Synthetic DSH",
                "metadata": {"local_agent_ref": row["discovery_ref"]}})
            assert response.status_code == 201, response.text
            response = await client.post(f"/api/workspace/employees/{employee}/agent-bindings", json={
                "company_id": COMPANY, "capability_id": row["capability_id"]})
            assert response.status_code == 200, response.text
            binding = next(b["id"] for b in response.json()["bindings"] if b["capability_id"] == row["capability_id"])
            with TenantContext.scope(TENANT):
                target = next(a for a in assignments if a["data"]["employeeRef"] == employee)
                with database.connect() as con:
                    con.execute("update employee_capability_bindings set priority=0 where tenant_id=? and id=?", (TENANT, binding))
                    con.execute("update runtime_entities set capability_ref=? where tenant_id=? and entity_id=?",
                        (row["capability_id"], TENANT, target["data"]["capabilityBindingRefs"][0]))
            allowance = f"/api/workspace/v1/companies/{COMPANY}/agent-allowance"
            initial = (await client.get(allowance)).json()
            response = await client.post(f"/api/workspace/v1/companies/{COMPANY}/agent-authorizations", json={
                "request_id": "leader-agent-grant", "expected_revision": initial["revision"],
                "previous_authorization_ref": initial["authorization_ref"], "consent": True, "binding_refs": [binding]})
            assert response.status_code == 200, response.text
            payload = {"problem": "coordinate existing employees", "expected_result": "summary", "request_id": "leader-mixed"}
            if agent_key == "leader":
                payload.update(agent_binding_ref=binding, source={"kind": "references", "references": []})
            response = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json=payload)
            assert response.status_code == 200, response.text
            ref = response.json()["work"]["entity_id"]
            response = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert response.status_code == 200, response.text
            assert response.json()["delegation_status"] == "ACCEPTED", response.text
            assert response.json()["acceptance_pending"]
            expected = 2 if agent_key == "leader" else 1
            assert len(agent_calls) == expected
            assert len(provider.calls) == 4
            replay = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert replay.status_code == 200, replay.text
            assert replay.json()["delegation_status"] == "ACCEPTED", replay.text
            assert len(provider.calls) == 4
            current = (await client.get(allowance)).json()
            assert current["used_calls"] == expected
            with TenantContext.scope(TENANT):
                root = RuntimeFoundation(database).get(ref)
                refs = [ref, *root["data"]["leaderDelegation"]["childWorkRefs"], root["data"]["leaderDelegation"]["summaryWorkRef"]]
                usage = [record for work_ref in refs for record in AIUsageService(database).list_records(work_ref=work_ref)]
                assert len(usage) == 4
                assert sum(r["capability_type"] == "agent" for r in usage) == expected
                assert all(r["total_tokens"] is None and r["cost_amount"] is None for r in usage if r["capability_type"] == "agent")
                assert sum(bool(r.get("providerCallReserved")) for work_ref in refs
                    for r in RuntimeFoundation(database).get(work_ref)["data"]["responsibilityRouting"]["executions"].values()) == 4
                assert root["lifecycle_status"] == "ACTIVE"
    asyncio.run(run())
