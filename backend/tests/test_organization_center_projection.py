from __future__ import annotations

from fastapi.testclient import TestClient

from app.database import Database
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.runtime.business_spine import CanonicalBusinessSpine
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext


TENANT = "tenant-organization-center"
COMPANY = "company-organization-center"
CEO = "ceo-organization-center"
DEPARTMENT = "department-content"
BUSINESS = "business-growth"
EMPLOYEE = "employee-content"
RUNTIME_EMPLOYEE = "runtime-employee-content"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO, "X-Role": "ceo"}


def _seed(path) -> str:
    database = Database(str(path))
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) "
            "values (?, ?, ?, 'Curis Test', 'active')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, mission) "
            "values (?, ?, ?, 'template-content', '内容与市场部', 'CONTENT', '负责内容增长')",
            (DEPARTMENT, TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_templates(id, name, role, source, tenant_id) "
            "values ('template-editor', '内容策划', '内容策划', 'tenant_private', ?)",
            (TENANT,),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values (?, ?, ?, ?, 'template-editor', '小策', '内容策划', 'idle')",
            (EMPLOYEE, TENANT, COMPANY, DEPARTMENT),
        )
        connection.execute(
            "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
            "values ('binding-editor', ?, ?, 'tenant_private', 'agent', 'agent.codex')",
            (TENANT, EMPLOYEE),
        )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        business = CanonicalBusinessSpine(database).create_draft_with_first_workspace(
            company_id=COMPANY,
            department_id=DEPARTMENT,
            business_id=BUSINESS,
            name="内容增长",
            goal="建立稳定内容增长",
            positioning="面向目标受众持续经营内容",
            workspace_name="小红书运营",
            business_type="XHS",
            blueprint_version="v1",
            blueprint={
                "businessType": "XHS",
                "platform": "XHS",
                "stages": ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"],
                "agentRefs": [], "capabilityRefs": [], "connectorRefs": [],
                "platformConstraints": {}, "replyPolicy": "CEO_REVIEW", "evidenceRules": [],
            },
        )
        workspace_id = business["workspaces"][0]["workspace_id"]
        foundation = RuntimeFoundation(database)
        foundation.create(
            "AI_EMPLOYEE", entity_id=RUNTIME_EMPLOYEE, company_id=COMPANY,
            workspace_id=workspace_id, lifecycle_status="AVAILABLE",
            data={"name": "小策", "responsibility": "规划内容增长"},
        )
        foundation.create(
            "ROLE_SLOT", entity_id="role-content-planner", company_id=COMPANY,
            workspace_id=workspace_id, data={"name": "内容策划"},
        )
        EmployeeExecutionIdentity(database).bind(
            company_id=COMPANY,
            workspace_id=workspace_id,
            runtime_employee_ref=RUNTIME_EMPLOYEE,
            company_employee_ref=EMPLOYEE,
            employee_capability_binding_ref="binding-editor",
        )
        ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY,
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            role_ref="role-content-planner",
            employee_ref=RUNTIME_EMPLOYEE,
            responsibility_key="content-planning",
            responsibility="负责内容增长计划",
            workspace_id=workspace_id,
            is_leader=True,
            assignment_id="assignment-content-planner",
        )
    return workspace_id


def test_projection_uses_canonical_identity_and_survives_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "organization.sqlite"
    with TestClient(create_app(str(path))) as client:
        workspace_id = _seed(path)
        response = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/organization",
            headers=HEADERS,
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["company"]["company_id"] == COMPANY
        assert [item["id"] for item in payload["departments"]] == [DEPARTMENT]
        assert [item["id"] for item in payload["employees"]] == [EMPLOYEE]
        business = payload["businesses"][0]
        assert business["business_id"] == BUSINESS
        assert business["workspaces"][0]["workspace_id"] == workspace_id
        assignment = business["team"][0]["data"]
        assert assignment["employeeRef"] == RUNTIME_EMPLOYEE
        assert assignment["companyEmployeeRef"] == EMPLOYEE
        assert assignment["employeeIdentityStatus"] == "VERIFIED_EXPLICIT_BRIDGE"
        assert "project" not in payload
        assert "capability" not in payload

    with TestClient(create_app(str(path))) as reopened:
        saved = reopened.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/organization",
            headers=HEADERS,
        )
        assert saved.status_code == 200
        assignment = saved.json()["businesses"][0]["team"][0]["data"]
        assert assignment["companyEmployeeRef"] == EMPLOYEE


def test_projection_is_tenant_scoped_and_does_not_infer_vacancy_or_risk(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "scope.sqlite"
    with TestClient(create_app(str(path))) as client:
        _seed(path)
        denied = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/organization",
            headers={"X-Tenant-Id": "other-tenant", "X-Ceo-Id": CEO, "X-Role": "ceo"},
        )
        assert denied.status_code == 404
        payload = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/organization",
            headers=HEADERS,
        ).json()
        assert "vacancy" not in payload["businesses"][0]
        assert "risk" not in payload["businesses"][0]


def test_new_team_projection_current_business_leader_author_and_edits(tmp_path):
    import json
    from app.organization_projection import read_organization_projection
    from backend.tests.test_writing_entry_readiness import company_only, confirmed, materialize
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY as writing_company
    from app.runtime.first_run_delivery import FirstRunDelivery
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        receipt = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)['creation_result']['initial_team']
        def current(): return read_organization_projection(db, CanonicalBusinessSpine(db), writing_company)
        payload = current(); business = payload['businesses'][0]
        assert len(business['team']) == 2
        assert {item['data']['scopeType'] for item in business['team']} == {'BUSINESS', 'WORKSPACE'}
        assert {item['data']['companyEmployeeRef'] for item in business['team']} == {receipt['employeeRef']}
        assert all(item['data']['roleName'] for item in business['team'])
        assert all(item['data']['employeeEnabled'] for item in business['team'])
        with db.connect() as con:
            con.execute("update employee_instances set name='当前名字',enabled=0 where id=?", (receipt['employeeRef'],))
        payload = current()
        assert payload['employees'][0]['name'] == '当前名字'
        assert all(item['data']['employeeEnabled'] is False for item in payload['businesses'][0]['team'])
        run2, draft2, proposal2 = confirmed(db, '另一项业务')
        second = materialize(FirstRunDelivery(db), runtime, run2, draft2, proposal2)['creation_result']['initial_team']
        with db.connect() as con:
            row = con.execute('select data_json from runtime_entities where entity_id=?', (receipt['assignments'][1]['assignmentRef'],)).fetchone()
            data = json.loads(row[0]); data['employeeRef'] = second['employeeRef']
            con.execute('update runtime_entities set owner_ref=?,data_json=? where entity_id=?', (second['employeeRef'],json.dumps(data),receipt['assignments'][1]['assignmentRef']))
        businesses = {item['business_id']: item for item in current()['businesses']}
        assert {item['data']['companyEmployeeRef'] for item in businesses[second['businessRef']]['team']} == {second['employeeRef']}
        assert next(item for item in businesses[receipt['businessRef']]['team'] if item['data']['scopeType'] == 'WORKSPACE')['data']['companyEmployeeRef'] == second['employeeRef']
        with db.connect() as con: con.execute('update employee_instances set deleted_at=current_timestamp where id=?', (second['employeeRef'],))
        assert all('companyEmployeeRef' not in item['data'] for item in {b['business_id']: b for b in current()['businesses']}[second['businessRef']]['team'])
        with TenantContext.scope('foreign', company_id=writing_company, role='test'):
            import pytest
            with pytest.raises(Exception, match='CEO identity|CEO does not own|Company is outside'): current()


def test_original_creation_locator_is_canonical_unique_and_read_only(tmp_path):
    import json
    from app.organization_projection import read_organization_projection
    from backend.tests.test_writing_entry_readiness import company_only, confirmed, materialize, database_values
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY as writing_company
    from app.runtime.first_run_delivery import FirstRunDelivery
    db, runtime = company_only(tmp_path)
    with scope():
        run, draft, proposal = confirmed(db)
        result = materialize(FirstRunDelivery(db), runtime, run, draft, proposal)
        before = database_values(db)
        def record(): return read_organization_projection(db, CanonicalBusinessSpine(db), writing_company)['businesses'][0]
        business = record(); locator = business['creation_record']
        assert locator == {'company_id': writing_company, 'business_id': result['creation_result']['business_id'], 'workspace_id': result['creation_result']['workspace_id'], 'founding_run_id': run}
        assert 'status' not in locator
        assert database_values(db) == before
        with db.connect() as con:
            row = con.execute('select * from runtime_entities where entity_id=?', (run,)).fetchone(); original = json.loads(row['data_json'])
            copy = dict(original)
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,owner_ref,lifecycle_status,data_json,created_at,updated_at) values ('duplicate','selfuse','FOUNDING_RUN',?,?,'COMPANY_CREATED',?,current_timestamp,current_timestamp)", (writing_company,row['owner_ref'],json.dumps(copy)))
        assert record()['creation_record'] is None and record()['creation_record_availability'] == 'AMBIGUOUS'
        with db.connect() as con:
            con.execute("delete from runtime_entities where entity_id='duplicate'")
            bad = json.loads(json.dumps(original)); bad['initialTeam']['workspaceRef'] = 'wrong'
            con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(bad),run))
        assert record()['creation_record'] is None
        with db.connect() as con:
            missing = dict(original); missing.pop('firstBusiness')
            con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(missing),run))
        assert record()['creation_record_availability'] == 'NO_RECORD'
        with db.connect() as con: con.execute('update runtime_entities set data_json=? where entity_id=?', (json.dumps(original),run))
        with scope(ceo_id='foreign'):
            import pytest
            with pytest.raises(Exception, match='CEO does not own'): record()


def test_pending_business_proposals_are_scoped_bounded_read_only_and_cold(tmp_path):
    import json
    import pytest
    from app.organization_projection import read_organization_projection
    from backend.tests.test_writing_entry_readiness import company_only, database_values
    from backend.tests.test_writing_chapter_vertical import scope, COMPANY as company, CEO as owner
    db, _ = company_only(tmp_path)
    def seed(ref, **changes):
        proposal = {'business_name': '保存提案 ' + ref, 'company_id': company, 'department_id': 'writing-test-department', 'package_id': 'fixture-professional', 'proposal_sha256': 'actual-saved-digest', 'snapshot': {'company_id': company, 'department_id': 'writing-test-department', 'definition': {'package_id': 'fixture-professional'}}}
        data = {'v1Proposal': proposal}
        for key in ('firstBusiness', 'v1Activation'):
            if key in changes: data[key] = changes[key]
        if 'proposalCompany' in changes: proposal['company_id'] = changes['proposalCompany']
        if 'snapshotCompany' in changes: proposal['snapshot']['company_id'] = changes['snapshotCompany']
        with db.connect() as con:
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,owner_ref,lifecycle_status,data_json,created_at,updated_at) values (?,?, 'FOUNDING_RUN',?,?,?,?,current_timestamp,?)", (ref, changes.get('tenant','selfuse'), changes.get('company_id',''), changes.get('owner',owner), changes.get('state','PROPOSED'), json.dumps(data), changes.get('updated','2026-10-09T01:00:00')))
    with scope():
        seed('pending'); seed('another-original')
        seed('confirmed-original', state='CEO_CONFIRMED', v1Activation={'company_id': company, 'status':'RUNNING','process_id':'old-process'})
        seed('foreign-owner', owner='foreign'); seed('foreign-tenant', tenant='foreign')
        seed('foreign-run-company', company_id='foreign'); seed('foreign-proposal',proposalCompany='foreign')
        seed('foreign-snapshot',snapshotCompany='foreign'); seed('unknown-state',state='UNKNOWN')
        seed('completed',state='COMPANY_CREATED',firstBusiness={'business_id':'actual-existing'})
        seed('contradictory-proposed',v1Activation={'status':'RUNNING'})
        before=database_values(db)
        def read(database=db):return read_organization_projection(database,CanonicalBusinessSpine(database),company)['pending_business_proposals']
        items=read();assert {i['founding_run_id'] for i in items}=={'pending','another-original'}
        assert all(set(i)=={'company_id','founding_run_id','business_name','lifecycle_status'} for i in items)
        assert database_values(db)==before
        assert read(Database(db.path))==items
        with scope(ceo_id='foreign'),pytest.raises(Exception,match='CEO does not own'):read()
        for n in range(25):seed('bounded-'+str(n).zfill(2),updated='2026-10-09T02:00:00')
        items=read();assert len(items)==20
        assert [i['founding_run_id'] for i in items]==['bounded-'+str(n).zfill(2) for n in range(20)]
        before=database_values(db);assert read()==items;assert database_values(db)==before
