"""Resolver checks are not an execution/Provider acceptance claim."""
import sqlite3

import pytest

from app.resource_scope_policy import ResourceScopePolicy as Scope


@pytest.fixture
def connection(tmp_path):
    with sqlite3.connect(tmp_path / "scope.sqlite") as conn:
        conn.row_factory = sqlite3.Row
        conn.executescript("""
            create table companies(tenant_id text, company_id text);
            create table department_instances(tenant_id text, company_id text, id text, deleted_at text);
            create table canonical_businesses(tenant_id text, company_id text, business_id text,
                department_id text, lifecycle_status text);
            create table workspaces(tenant_id text, company_id text, workspace_id text,
                business_id text, business_relation_status text);
            insert into companies values ('t', 'c'), ('t', 'other-company');
            insert into department_instances values ('t', 'c', 'd', null), ('t', 'c', 'sibling', null);
            insert into canonical_businesses values ('t', 'c', 'b', 'd', 'ACTIVE');
            insert into workspaces values ('t', 'c', 'w', 'b', 'RESOLVED');
        """)
        yield conn


@pytest.mark.parametrize("kind,ref,parents", [
    ("COMPANY", "c", (None, None, None)),
    ("DEPARTMENT", "d", ("d", None, None)),
    ("BUSINESS", "b", ("d", "b", None)),
    ("WORKSPACE", "w", ("d", "b", "w")),
])
def test_canonical_lineage(connection, kind, ref, parents):
    scope = Scope.resolve_execution_scope(connection, tenant_id="t", company_id="c",
                                          scope_type=kind, scope_ref=ref)
    assert scope["scope_type"] == kind and scope["scope_ref"] == ref
    assert tuple(scope[key] for key in ("department_id", "business_id", "workspace_id")) == parents


@pytest.mark.parametrize("tenant,company,kind,ref", [
    ("other-tenant", "c", "WORKSPACE", "w"),
    ("t", "other-company", "WORKSPACE", "w"),
    ("t", "c", "BUSINESS", "missing"),
    ("t", "c", "PROJECT", "b"),
    ("t", "c", "COMPANY", "other-company"),
])
def test_invalid_scope_rejected(connection, tenant, company, kind, ref):
    with pytest.raises(ValueError):
        Scope.resolve_execution_scope(connection, tenant_id=tenant, company_id=company,
                                      scope_type=kind, scope_ref=ref)


def test_broken_parent_and_unresolved_workspace_fail_closed(connection):
    connection.execute("update canonical_businesses set department_id='missing'")
    with pytest.raises(ValueError):
        Scope.resolve_execution_scope(connection, tenant_id="t", company_id="c",
                                      scope_type="WORKSPACE", scope_ref="w")
    connection.execute("update canonical_businesses set department_id='d'")
    connection.execute("update workspaces set business_relation_status='QUARANTINED'")
    with pytest.raises(ValueError):
        Scope.resolve_execution_scope(connection, tenant_id="t", company_id="c",
                                      scope_type="WORKSPACE", scope_ref="w")


def test_legacy_workspace_only_and_scope_collision(connection):
    legacy = Scope.execution_scope_from_record(connection, tenant_id="t",
                                               record={"company_id": "c", "workspace_id": "w"})
    assert legacy["scope_type"] == "WORKSPACE"
    for record in ({"company_id": "c"},
                   {"company_id": "c", "workspace_id": "w", "data": {"scopeType": "BUSINESS", "scopeRef": "b"}}):
        with pytest.raises(ValueError):
            Scope.execution_scope_from_record(connection, tenant_id="t", record=record)
    department = Scope.resolve_execution_scope(connection, tenant_id="t", company_id="c",
                                                scope_type="DEPARTMENT", scope_ref="d")
    sibling = Scope.resolve_execution_scope(connection, tenant_id="t", company_id="c",
                                             scope_type="DEPARTMENT", scope_ref="sibling")
    Scope.require_same_execution_scope(department, department)
    for other in (sibling, legacy):
        with pytest.raises(ValueError):
            Scope.require_same_execution_scope(department, other)


def test_company_assignment_without_business_and_restart(tmp_path):
    from app.database import Database
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
    from app.tenant_context import TenantContext

    database = Database(str(tmp_path / "assignment.sqlite"))
    database.initialize()
    with TenantContext.scope("scope-tenant"):
        with database.connect() as conn:
            conn.execute("insert into companies(company_id,tenant_id,ceo_id,name) values ('c','scope-tenant','ceo','Scope')")
        foundation = RuntimeFoundation(database)
        employee = foundation.create("AI_EMPLOYEE", company_id="c", lifecycle_status="AVAILABLE")
        role = foundation.create("ROLE_SLOT", company_id="c")
        assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id="c", scope_type="COMPANY", scope_ref="c", role_ref=role["entity_id"],
            employee_ref=employee["entity_id"], responsibility_key="company-analysis",
            responsibility="Only the assigned bounded company analysis", is_leader=True,
        )
        restarted = RuntimeFoundation(Database(database.path)).get(assignment["entity_id"])
        assert restarted["workspace_id"] is None
        assert restarted["data"]["scopeType"] == "COMPANY"
        assert restarted["data"]["scopeRef"] == "c"
        assert restarted["data"]["employeeRef"] == employee["entity_id"]
        with database.connect() as conn:
            assert conn.execute("select count(*) from canonical_businesses").fetchone()[0] == 0
            assert conn.execute("select count(*) from workspaces").fetchone()[0] == 0


@pytest.mark.parametrize("kind", ["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"])
def test_four_scope_work_identity_and_restart(tmp_path, kind):
    from backend.tests.test_responsibility_routing_runtime import _seed, TENANT, COMPANY, BUSINESS, WORKSPACE
    from app.database import Database
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from app.result_store import ResultStore
    from app.tenant_context import TenantContext

    with TenantContext.scope(TENANT):
        database, foundation, routing = _seed(tmp_path / "work.sqlite")
        ref = {"COMPANY": COMPANY, "DEPARTMENT": "department-routing", "BUSINESS": BUSINESS, "WORKSPACE": WORKSPACE}[kind]
        workspace = WORKSPACE if kind == "WORKSPACE" else None
        employee = foundation.create("AI_EMPLOYEE", company_id=COMPANY, lifecycle_status="AVAILABLE")
        role = foundation.create("ROLE_SLOT", company_id=COMPANY)
        assignment = routing.create_assignment(
            company_id=COMPANY, workspace_id=workspace, scope_type=kind, scope_ref=ref,
            role_ref=role["entity_id"], employee_ref=employee["entity_id"],
            responsibility_key="bounded-scope-work", responsibility="Review selected evidence only",
        )
        arguments = dict(company_id=COMPANY, workspace_id=workspace, scope_type=kind, scope_ref=ref,
                         assignment_ref=assignment["entity_id"], release_key="same-request", contract={"problem": "bounded"})
        created = CanonicalChildWorkRuntime(database).create_cycle_work(**arguments)
        restarted = CanonicalChildWorkRuntime(Database(database.path))
        replay = restarted.create_cycle_work(**arguments)
        assert replay["cycle"]["entity_id"] == created["cycle"]["entity_id"]
        assert replay["work"]["entity_id"] == created["work"]["entity_id"]
        assert replay["work"]["workspace_id"] == workspace
        assert replay["work"]["data"]["scopeType"] == kind
        assert replay["work"]["data"]["scopeRef"] == ref
        assert len(restarted.list_cycle_work(created["cycle"]["entity_id"])) == 1
        task = ResultStore(database).create_task(
            "Scoped execution request", company_id=COMPANY, workspace_id=workspace,
            scope_type=kind, scope_ref=ref, work_ref=created["work"]["entity_id"], execution_ref="attempt-1",
        )
        persisted_task = ResultStore(Database(database.path)).get_task(task["task_id"])
        assert persisted_task["scope_type"] == kind and persisted_task["scope_ref"] == ref
        assert persisted_task["project_id"] is None
        assert persisted_task["workspace_id"] == workspace
        if kind != "WORKSPACE":
            from app.ai_usage import AIUsageService
            # A scope alone never grants execution: this fixture has no Company Employee binding.
            with database.connect() as conn, pytest.raises(KeyError, match="usage lineage resource not found"):
                AIUsageService._validate_lineage(
                    conn, tenant_id=TENANT, employee_id=employee["entity_id"], capability_id="not-launched",
                    capability_type="model", task_id=task["task_id"], project_id=None,
                    department_id=None, capability_binding_id=None,
                )
        with pytest.raises(ValueError):
            restarted.create_cycle_work(**{**arguments, "scope_ref": "missing"})


def test_task_scope_addition_does_not_reinterpret_history(tmp_path):
    from app.database import Database
    from app.result_store import ResultStore

    database = Database(str(tmp_path / "migration.sqlite"))
    database.initialize()
    task = ResultStore(database).create_task("Historical Task")
    with database.connect() as conn:
        conn.execute("alter table tasks drop column scope_type")
        conn.execute("alter table tasks drop column scope_ref")
        columns = [row["name"] for row in conn.execute("pragma table_info(tasks)")]
        names = ','.join('"'+name+'"' for name in columns)
        before = [tuple(row) for row in conn.execute(f"select {names} from tasks order by task_id")]
        objects = [tuple(row) for row in conn.execute(
            "select name, sql from sqlite_master where type in ('index','trigger') and tbl_name='tasks' order by name")]
    with database.connect() as conn:
        database._migrate_task_execution_scope(conn)
        database._migrate_task_execution_scope(conn)
        assert [tuple(row) for row in conn.execute(f"select {names} from tasks order by task_id")] == before
        assert [tuple(row) for row in conn.execute(
            "select name, sql from sqlite_master where type in ('index','trigger') and tbl_name='tasks' order by name")] == objects
        assert tuple(conn.execute("select scope_type,scope_ref from tasks where task_id=?", (task["task_id"],)).fetchone()) == (None, None)


def test_task_scope_migration_failure_is_atomic(tmp_path, monkeypatch):
    from app.database import Database

    database = Database(str(tmp_path / "migration-failure.sqlite"))
    database.initialize()
    with database.connect() as conn:
        conn.execute("alter table tasks drop column scope_type")
        conn.execute("alter table tasks drop column scope_ref")
        ensure = database._ensure_column
        def fail_second(connection, table, column, definition):
            if column == "scope_ref":
                raise RuntimeError("injected second-column failure")
            ensure(connection, table, column, definition)
        monkeypatch.setattr(database, "_ensure_column", fail_second)
        with pytest.raises(RuntimeError, match="injected"):
            database._migrate_task_execution_scope(conn)
        assert not {"scope_type", "scope_ref"}.intersection(row["name"] for row in conn.execute("pragma table_info(tasks)"))


@pytest.mark.parametrize("kind", ["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"])
@pytest.mark.parametrize("fail", [False, True])
def test_four_scope_conversation_execution_usage_restart(tmp_path, monkeypatch, kind, fail):
    """Controlled HTTP through the real adapter/orchestrator; not live cloud acceptance."""
    import json
    from dataclasses import replace
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.identity_membership import IdentityMembership
    from app.ai_usage import AIUsageService
    from backend.tests.test_conversation_usage import prepared
    from backend.tests.test_employee_conversation import scope
    from backend.tests.test_v1_general_operating_contract import COMPANY, TENANT, EMPLOYEE, WORKSPACE, BUSINESS

    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test",
        lambda self, tenant, request: replace(original(self, tenant, request), role="ceo"))
    path = tmp_path / "execution.sqlite"
    db, assignment, adapter, calls = prepared(path, fail)
    ref = {"COMPANY": COMPANY, "DEPARTMENT": "department", "BUSINESS": BUSINESS, "WORKSPACE": WORKSPACE}[kind]
    workspace = WORKSPACE if kind == "WORKSPACE" else None
    with db.connect() as con:
        # Isolated canonical fixture: Company Employee/Role can hold any authorized scoped Assignment.
        con.execute("update runtime_entities set workspace_id=null where entity_type in ('AI_EMPLOYEE','ROLE_SLOT')")
        data = json.loads(con.execute("select data_json from runtime_entities where entity_id=?", (assignment,)).fetchone()[0])
        data.update(scopeType=kind, scopeRef=ref)
        con.execute("update runtime_entities set workspace_id=?,data_json=? where entity_id=?", (workspace, json.dumps(data), assignment))
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
    payload = {"body": "只讨论当前责任，不创建业务或工作", "request_id": "one", "assignment_ref": assignment}
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
        state = client.get(prefix, headers=headers).json()
    assert len(calls) == 1, state
    assert len(state["messages"]) == (1 if fail else 2), state
    assert state["attempts"][0]["status"] == ("FAILED" if fail else "COMPLETED"), state
    with scope():
        rows = AIUsageService(db).list_records(conversation_ref=state["conversation_id"])
    assert len(rows) == 1
    row = rows[0]
    assert (row["scope_type"], row["scope_ref"], row["workspace_id"]) == (kind, ref, workspace)
    assert row["company_id"] == COMPANY and row["canonical_employee_ref"] == EMPLOYEE
    assert row["project_id"] is None and row["work_ref"] is None
    assert row["cost_amount"] is None
    assert row["total_tokens"] == (None if fail else 7)
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        assert client.get(prefix, headers=headers).json()["messages"] == state["messages"]
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
    assert len(calls) == 1
    with scope():
        assert AIUsageService(db).list_records(conversation_ref=state["conversation_id"]) == rows
    with db.connect() as con:
        task = dict(con.execute("select * from tasks where task_id=?", (row["task_id"],)).fetchone())
        assert (task["scope_type"], task["scope_ref"], task["workspace_id"]) == (kind, ref, workspace)
        assert con.execute("select count(*) from projects").fetchone()[0] == 0
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


@pytest.mark.parametrize("kind", ["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"])
@pytest.mark.parametrize("fail", [False, True])
def test_four_scope_work_provider_result_usage(tmp_path, kind, fail):
    import json
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.model_gateway import ModelGatewayAdapter
    from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from app.ai_usage import AIUsageService
    from app.result_attention import ResultAttention
    from backend.tests.test_conversation_usage import prepared
    from backend.tests.test_employee_conversation import scope
    from backend.tests.test_canonical_usage_attribution import _CanonicalProvider, _FailingProvider, PREFIX, HEADERS
    from backend.tests.test_v1_general_operating_contract import COMPANY, EMPLOYEE, WORKSPACE, BUSINESS

    path = tmp_path / "work-execution.sqlite"
    db, assignment_ref, _, _ = prepared(path)
    ref = {"COMPANY": COMPANY, "DEPARTMENT": "department", "BUSINESS": BUSINESS, "WORKSPACE": WORKSPACE}[kind]
    workspace = WORKSPACE if kind == "WORKSPACE" else None
    with db.connect() as con:
        con.execute("delete from employee_capability_bindings where id='binding-general'")
        con.execute("update runtime_entities set workspace_id=null where entity_type in ('AI_EMPLOYEE','ROLE_SLOT')")
        data = json.loads(con.execute("select data_json from runtime_entities where entity_id=?", (assignment_ref,)).fetchone()[0])
        data.update(scopeType=kind, scopeRef=ref)
        con.execute("update runtime_entities set workspace_id=?,data_json=? where entity_id=?", (workspace, json.dumps(data), assignment_ref))
        if kind != "WORKSPACE":
            con.execute("delete from runtime_entities where entity_type='WORKFLOW' and workspace_id=?", (WORKSPACE,))
            con.execute("delete from workspaces")
        if kind in {"COMPANY", "DEPARTMENT"}:
            con.execute("delete from canonical_businesses")
    provider = _FailingProvider() if fail else _CanonicalProvider()
    adapter = ModelGatewayAdapter(base_url="https://provider.invalid", api_key="test-only",
        gateway_id="conversation-test", model_name="contract-model", http_post=provider)
    with scope():
        routing = ResponsibilityRoutingRuntime(db)
        routing.publish_workflow(company_id=COMPANY, workspace_id=workspace, scope_type=kind, scope_ref=ref,
            workflow_key="scope-proof", assignment_refs=[assignment_ref], default_flow=[data["responsibilityKey"]])
        child = CanonicalChildWorkRuntime(db)
        created = child.create_cycle_work(company_id=COMPANY, workspace_id=workspace, scope_type=kind, scope_ref=ref,
            assignment_ref=assignment_ref, release_key="one", contract={"problem": "整理已提供的范围说明",
                "expectedResult": "给出简短核对结果", "constraints": ["不读取无关历史"], "references": []})
        work_ref = created["work"]["entity_id"]
        routing.start_work(work_ref, scope_type=kind, scope_ref=ref, workflow_key="scope-proof")
        child.transition_work(work_ref, "READY", actor="SYSTEM", reason="test")
        child.transition_work(work_ref, "ACTIVE", actor="SYSTEM", reason="test")
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        response = client.post(f"{PREFIX}/works/{work_ref}/execute?max_executions=1", headers=HEADERS)
        assert response.status_code == 200, response.text
        state = response.json()["work"]["data"]["responsibilityRouting"]
        assert state["status"] == ("WAITING" if fail else "COMPLETED"), state
        assert state["currentExecutorRef"] is None
        assert state["responsibilityHolderRef"] == EMPLOYEE
    assert len(provider.calls) == 1
    with scope():
        rows = AIUsageService(db).list_records(work_ref=work_ref)
        assert len(rows) == 1
        row = rows[0]
        assert (row["scope_type"], row["scope_ref"], row["workspace_id"]) == (kind, ref, workspace)
        assert row["project_id"] is None and row["cost_amount"] is None
        with db.connect() as con:
            actual = Scope.execution_scope_from_record(con, tenant_id=row["tenant_id"],
                record=RuntimeFoundation(db).get(work_ref))
        result = ResultAttention(db).detail(COMPANY, workspace, "task:" + row["task_id"], scope=actual)
        assert result["reference_id"] == "task:" + row["task_id"]
        assert result["status"] == ("FAILED" if fail else "COMPLETED")
        if fail:
            assert row["total_tokens"] is None
            db.initialize()
            assert AIUsageService(db).list_records(work_ref=work_ref) == rows
            assert RuntimeFoundation(db).get(work_ref)["data"]["responsibilityRouting"]["status"] == "WAITING"
            return
        assert result["artifacts"]
        assert all(item["content_sha256"] for item in result["artifacts"])
        evidence = RuntimeFoundation(db).create("EVIDENCE", company_id=COMPANY, workspace_id=workspace,
            parent_id=work_ref, owner_ref=EMPLOYEE, verification_status="VERIFIED", evidence_condition="CURRENT",
            data={"summary": "Controlled adapter execution evidence, not cloud quality",
                  "resultRef": result["reference_id"], "artifactRefs": result["artifact_refs"],
                  "usageRef": row["usage_record_id"]})
        viewed = ResultAttention(db).detail(COMPANY, workspace, evidence["entity_id"], scope=actual)
        assert viewed["data"]["resultRef"] == result["reference_id"]
        wrong = {**actual, "scope_ref": "missing-scope"}
        with pytest.raises(ValueError):
            ResultAttention(db).detail(COMPANY, wrong["workspace_id"], evidence["entity_id"], scope=wrong)
        # Verify the ACK trust seam against actual controlled-provider evidence;
        # this does not perform a product-level accountability transfer.
        from app.employee_execution_identity import EmployeeExecutionIdentity
        foundation = RuntimeFoundation(db)
        handoff = foundation.create("HANDOFF", company_id=COMPANY, workspace_id=workspace,
            parent_id=created["cycle"]["entity_id"], lifecycle_status="SENT",
            data={"scopeType": kind, "scopeRef": ref, "toEmployeeRef": EMPLOYEE})
        with db.connect() as con:
            cycle_data = json.loads(con.execute("select data_json from runtime_entities where entity_id=?",
                (created["cycle"]["entity_id"],)).fetchone()[0])
            cycle_data["responsibilityHandoff"] = {"handoffRef": handoff["entity_id"], "toEmployeeRef": EMPLOYEE}
            con.execute("update runtime_entities set data_json=? where entity_id=?",
                (json.dumps(cycle_data), created["cycle"]["entity_id"]))
        arguments = dict(company_id=COMPANY, workspace_id=workspace, cycle_ref=created["cycle"]["entity_id"],
                         target_employee_ref=EMPLOYEE, task_ref=row["task_id"], session_ref="")
        assert EmployeeExecutionIdentity(db).verify_handoff_ack(**arguments)["verification_status"] == "VERIFIED"
        db.initialize()
        assert EmployeeExecutionIdentity(db).verify_handoff_ack(**arguments)["ack_actor_ref"] == EMPLOYEE
        for changes in ({"toEmployeeRef": "wrong-employee"}, {"scopeRef": "missing"}):
            with db.connect() as con:
                con.execute("update runtime_entities set data_json=? where entity_id=?",
                    (json.dumps({**handoff["data"], **changes}), handoff["entity_id"]))
            with pytest.raises(ValueError):
                EmployeeExecutionIdentity(db).verify_handoff_ack(**arguments)
        with db.connect() as con:
            con.execute("update runtime_entities set data_json=? where entity_id=?",
                (json.dumps(handoff["data"]), handoff["entity_id"]))
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        assert client.post(f"{PREFIX}/works/{work_ref}/execute?max_executions=1", headers=HEADERS).status_code == 200
    assert len(provider.calls) == 1


def test_general_assignment_reuses_company_employee_without_moving_identity(tmp_path, monkeypatch):
    from backend.tests.test_conversation_usage import prepared
    from backend.tests.test_employee_conversation import scope
    from backend.tests.test_v1_general_operating_contract import COMPANY, EMPLOYEE, WORKSPACE
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from app.runtime import RuntimeFoundation

    db, _, _, calls = prepared(tmp_path / "company-employee.sqlite")
    with db.connect() as con:
        con.execute("update runtime_entities set workspace_id=null where entity_type='AI_EMPLOYEE' and entity_id=?", (EMPLOYEE,))
        con.execute("delete from runtime_entities where entity_type='RESPONSIBILITY_WORKFLOW'")
    with scope():
        delivery = GeneralWorkspaceDelivery(db)
        monkeypatch.setattr(delivery.models, "read_current", lambda: {"preference": {
            "source": "official", "model_key": "model.conversation", "model_name": "contract-model"}})
        result = delivery.assign_employee(company_id=COMPANY, workspace_id=WORKSPACE,
            employee_id=EMPLOYEE, responsibility="核对所选资料")
        assert result["created"]
        assert RuntimeFoundation(db).get(EMPLOYEE)["workspace_id"] is None
        assert not delivery.assign_employee(company_id=COMPANY, workspace_id=WORKSPACE,
            employee_id=EMPLOYEE, responsibility="核对所选资料")["created"]
        assert calls == []
        db.initialize()
        assert RuntimeFoundation(db).get(EMPLOYEE)["workspace_id"] is None


def test_scope_ledger_migration_preserves_history_and_is_atomic(tmp_path, monkeypatch):
    from app.database import Database

    db = Database(str(tmp_path / "history.sqlite"))
    with monkeypatch.context() as historical:
        historical.setattr(Database, "_migrate_execution_scope_usage", staticmethod(lambda con: None))
        db.initialize()
    with db.connect() as con:
        con.execute("create index scope_history_custom on ai_usage_records(request_id)")
        con.execute("create trigger scope_history_immutable before update on ai_usage_records begin select raise(abort,'immutable'); end")
        common = "usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,model_name,currency,cost_source,employee_id,capability_id,capability_type,task_id,department_id,request_id,execution_status,metering_status,occurred_at,idempotency_key"
        for source, extra, values in (
            ("legacy", "project_id", ["project"]),
            ("work", "business_id,workspace_id,work_ref,execution_ref", ["business", "workspace", "work", "execution"]),
            ("conversation", "business_id,workspace_id,conversation_ref,canonical_employee_ref,execution_ref", ["business", "workspace", "conversation", "employee", "execution"]),
        ):
            args = [source,"tenant","company","gateway","provider","model","USD","unknown","employee","capability","model","task","department","request","failed","unknown","2026-09-09",source] + values
            con.execute(f"insert into ai_usage_records({common},{extra}) values ({','.join('?' for _ in args)})", args)
        before = [dict(r) for r in con.execute("select * from ai_usage_records order by usage_record_id")]
        schema = [tuple(r) for r in con.execute("select type,name,sql from sqlite_master where tbl_name='ai_usage_records' order by type,name")]
        con.commit()
        con.set_authorizer(lambda action, first, *_: sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_DROP_TABLE and first == "ai_usage_records" else sqlite3.SQLITE_OK)
        with pytest.raises(sqlite3.DatabaseError):
            Database._migrate_execution_scope_usage(con)
        con.set_authorizer(None)
        assert [tuple(r) for r in con.execute("select type,name,sql from sqlite_master where tbl_name='ai_usage_records' order by type,name")] == schema
        assert [dict(r) for r in con.execute("select * from ai_usage_records order by usage_record_id")] == before
        assert not con.execute("select 1 from sqlite_master where name='ai_usage_records__scope'").fetchone()
        Database._migrate_execution_scope_usage(con)
        Database._migrate_execution_scope_usage(con)
        after = [dict(r) for r in con.execute("select * from ai_usage_records order by usage_record_id")]
        assert [{k: row[k] for k in old} for row, old in zip(after, before)] == before
        assert all(row["scope_type"] is None and row["scope_ref"] is None for row in after)
        assert [tuple(r) for r in con.execute("select type,name,sql from sqlite_master where tbl_name='ai_usage_records' and type != 'table' order by type,name")] == [r for r in schema if r[0] != "table"]
        with pytest.raises(sqlite3.IntegrityError, match="immutable"):
            con.execute("update ai_usage_records set cost_amount=0")
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


@pytest.mark.parametrize("kind", ["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"])
def test_assignment_authority_cannot_escape_scope_or_revision(tmp_path, kind):
    import json
    from backend.tests.test_conversation_usage import prepared
    from backend.tests.test_v1_general_operating_contract import COMPANY, TENANT, EMPLOYEE, WORKSPACE, BUSINESS

    db, assignment_ref, _, calls = prepared(tmp_path / "authorization.sqlite")
    ref = {"COMPANY": COMPANY, "DEPARTMENT": "department", "BUSINESS": BUSINESS, "WORKSPACE": WORKSPACE}[kind]
    with db.connect() as con:
        con.execute("update runtime_entities set workspace_id=null where entity_type in ('AI_EMPLOYEE','ROLE_SLOT')")
        data = json.loads(con.execute("select data_json from runtime_entities where entity_id=?", (assignment_ref,)).fetchone()[0])
        data.update(scopeType=kind, scopeRef=ref)
        con.execute("update runtime_entities set workspace_id=?,data_json=? where entity_id=?",
                    (WORKSPACE if kind == "WORKSPACE" else None, json.dumps(data), assignment_ref))
        actual = Scope.resolve_execution_scope(con, tenant_id=TENANT, company_id=COMPANY, scope_type=kind, scope_ref=ref)
        args = dict(tenant_id=TENANT, company_id=COMPANY, assignment_ref=assignment_ref,
                    employee_ref=EMPLOYEE, revision=data["revision"], scope=actual)
        assert Scope.authorize_assignment(con, **args)["scope_ref"] == ref
        for change in ({"tenant_id": "other"}, {"company_id": "other"}, {"employee_ref": "other"},
                       {"assignment_ref": "missing"}, {"revision": data["revision"] + 1},
                       {"scope": {**actual, "scope_ref": "sibling"}}):
            with pytest.raises(ValueError):
                Scope.authorize_assignment(con, **{**args, **change})
    assert not calls
