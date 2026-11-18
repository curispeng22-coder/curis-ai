"""Real canonical initial teams over existing transactional event receipts."""
import json
from concurrent.futures import ThreadPoolExecutor
import pytest
from app.employee_templates import EmployeeTemplateContract, professional_team_contract
from app.workspace_package_runtime import WorkspacePackageRuntime, PackageConflictError, PackageScopeError
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.organization_projection import read_organization_projection
from app.runtime.business_spine import CanonicalBusinessSpine
from backend.tests.test_writing_entry_readiness import company_only, confirmed, materialize
from backend.tests.test_writing_chapter_vertical import scope, COMPANY, CEO

ASSETS=__import__('pathlib').Path(__file__).resolve().parents[1]/'app/bundled_workspace_packages'

def install(runtime,folder='music',business='team-business'):
 return runtime.install(ASSETS/folder,COMPANY,department_id='writing-test-department',business_id=business,business_name='真实测试业务')

def payload(detail):
 p=detail['package'];return dict(company_id=COMPANY,ceo_id=CEO,request_id='original-request',expected={'business_id':'team-business','package_id':p['package_id'],'version':p['version'],'digest':p['digest'],'assignments':[]})

def legacy(tmp_path,monkeypatch):
 db,runtime=company_only(tmp_path)
 original=EmployeeTemplateContract.materialize_professional_team_in_connection
 with monkeypatch.context() as patch:
  patch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',lambda *a,**k: {})
  detail=install(runtime)
 return db,runtime,detail,original

@pytest.mark.parametrize(('folder','assignment_count','employee_count'),[
 ('writing_authoring',2,1),
 ('content_growth_v02',3,3),
 ('music',2,1),
])
def test_new_install_true_identity_two_assignments_and_same_business_retry(tmp_path,folder,assignment_count,employee_count):
 db,runtime=company_only(tmp_path)
 with scope():
  detail=install(runtime,folder);ws=detail['instance']['workspace_id']
  with db.connect() as con:
   assignments=con.execute("select data_json from runtime_entities where entity_type='RESPONSIBILITY_ASSIGNMENT'").fetchall();assert len(assignments)==assignment_count
   employee=json.loads(assignments[0][0])['employeeRef']
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==employee_count
   assert con.execute('select count(*) from employee_capability_bindings').fetchone()[0]==0
  identity=EmployeeExecutionIdentity(db).resolve(company_id=COMPANY,workspace_id=ws,runtime_employee_ref=employee)
  assert identity['identity_status']=='VERIFIED_EXPLICIT_BRIDGE'
  assert install(runtime,folder)['instance']['workspace_id']==ws
  with pytest.raises(PackageConflictError):install(runtime,folder,'another-business')
  projection=read_organization_projection(db,CanonicalBusinessSpine(db),COMPANY);assert len(projection['employees'])==employee_count


def test_confirmed_caller_not_doubled_and_new_install_rollback(tmp_path,monkeypatch):
 db,runtime=company_only(tmp_path)
 with scope():
  run,draft,proposal=confirmed(db);result=materialize(__import__('app.runtime.first_run_delivery',fromlist=['FirstRunDelivery']).FirstRunDelivery(db),runtime,run,draft,proposal)
  assert result['activation']['status']=='COMPLETED'
  with db.connect() as con:assert con.execute('select count(*) from employee_instances').fetchone()[0]==1
  def fail(*args,**kwargs):raise ValueError('materializer stopped')
  monkeypatch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',fail)
  with pytest.raises(PackageConflictError):install(runtime)
  with db.connect() as con:
   assert con.execute("select count(*) from canonical_businesses where business_id='team-business'").fetchone()[0]==0
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==1


def test_legacy_completion_request_replay_response_loss_concurrency_and_rename(tmp_path,monkeypatch):
 with scope():db,runtime,detail,_=legacy(tmp_path,monkeypatch)
 ws=detail['instance']['workspace_id'];values=payload(detail)
 def call(_):
  with scope():return runtime.complete_professional_team(ws,**values)
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(call,[0,1]))
 assert results[0]['receipt']==results[1]['receipt']
 with scope():
  assert call(None)['receipt']==results[0]['receipt']
  with db.connect() as con:
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==1
   assert con.execute("select count(*) from evolution_events where event_type='professional.initial_team.completed'").fetchone()[0]==1
   employee=results[0]['current_team']['companyEmployeeRef'];con.execute("update employee_instances set name='用户自定义名称' where id=?",(employee,))
  repeated=call(None);assert repeated['current_team']['name']=='用户自定义名称'
  state=repeated['current_team'];other=values|{'request_id':'different-request','expected':values['expected']|{'assignments':state['assignments']}}
  assert runtime.complete_professional_team(ws,**other)['current_team']['companyEmployeeRef']==employee
  with pytest.raises(PackageConflictError):runtime.complete_professional_team(ws,**(values|{'expected':values['expected']|{'assignments':state['assignments']}}))

@pytest.mark.parametrize('mutation',['partial','disabled','foreign','package','department','basis','blueprint','leader-flag'])
def test_empty_or_conflicting_state_fails_without_new_employee(tmp_path,monkeypatch,mutation):
 with scope():
  db,runtime,detail,writer=legacy(tmp_path,monkeypatch);ws=detail['instance']['workspace_id'];values=payload(detail)
  with db.connect() as con:
   if mutation in ['partial','disabled','leader-flag']:
    con.execute('begin immediate');team=writer(EmployeeTemplateContract(db),con,company_id=COMPANY,business_id='team-business',workspace_id=ws,contract=professional_team_contract(detail['package']['package_id'],detail['package']['version'],detail['package']['digest']))
    if mutation=='partial':con.execute("update runtime_entities set lifecycle_status='DISABLED' where entity_id=?",(team['assignments'][0]['assignmentRef'],))
    elif mutation=='disabled':con.execute('update employee_instances set enabled=0 where id=?',(team['employeeRef'],))
    else:con.execute("update runtime_entities set data_json=json_set(data_json,'$.isLeader',json('false')) where entity_id=?",(team['assignments'][0]['assignmentRef'],))
   if mutation=='package':con.execute("update installed_workspace_packages set digest=?",('f'*64,))
   if mutation=='blueprint':con.execute("update workspaces set blueprint_version='foreign-version'")
   if mutation=='department':con.execute("update department_instances set enabled=0")
   before=con.execute('select count(*) from employee_instances').fetchone()[0]
  if mutation=='foreign':values['company_id']='foreign'
  if mutation=='basis':values['expected']['assignments']=[{'ref':'foreign','revision':1,'employee_ref':'foreign'}]
  with pytest.raises((PackageConflictError,PackageScopeError)):runtime.complete_professional_team(ws,**values)
  with db.connect() as con:
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==before
   assert con.execute("select count(*) from evolution_events where event_type='professional.initial_team.completed'").fetchone()[0]==0


def test_completion_failure_rolls_back_employees_roles_links_and_receipt(tmp_path,monkeypatch):
 with scope():
  db,runtime,detail,writer=legacy(tmp_path,monkeypatch);ws=detail['instance']['workspace_id']
  def fail_after_write(*args,**kwargs):writer(*args,**kwargs);raise ValueError('failure after team writes')
  monkeypatch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',fail_after_write)
  with pytest.raises(PackageConflictError):runtime.complete_professional_team(ws,**payload(detail))
  with db.connect() as con:
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==0
   assert con.execute("select count(*) from runtime_entities where entity_type in ('ROLE_SLOT','AI_EMPLOYEE','RESPONSIBILITY_ASSIGNMENT')").fetchone()[0]==0
   assert con.execute('select count(*) from runtime_links').fetchone()[0]==0
   assert con.execute("select count(*) from evolution_events where event_type='professional.initial_team.completed'").fetchone()[0]==0


def test_strict_http_boundary_and_no_automatic_get_backfill(tmp_path,monkeypatch):
 from fastapi import FastAPI
 from fastapi.testclient import TestClient
 from app.workspace_package_api import build_workspace_package_router
 with scope():
  db,runtime,detail,_=legacy(tmp_path,monkeypatch);ws=detail['instance']['workspace_id'];values=payload(detail)
  monkeypatch.setenv('CURIS_WORKSPACE_PACKAGE_STORE',str(tmp_path/'api-store'))
  app=FastAPI();app.include_router(build_workspace_package_router(db));client=TestClient(app)
  assert client.get('/api/workspace/packages/workspaces/'+ws).status_code==200
  with db.connect() as con:assert con.execute('select count(*) from employee_instances').fetchone()[0]==0
  url='/api/workspace/packages/workspaces/'+ws+'/initial-team'
  assert client.post(url,json=values|{'ceo_id':'other'}).status_code==403
  assert client.post(url,json=values|{'unexpected':True}).status_code==422
  response=client.post(url,json=values);assert response.status_code==200,response.text
  assert client.post(url,json=values).json()['receipt']==response.json()['receipt']


def test_professional_new_install_rejects_nonowner_without_new_team(tmp_path):
 db,runtime=company_only(tmp_path)
 with scope(ceo_id='another-ceo'):
  with pytest.raises(PackageScopeError):install(runtime)
 with db.connect() as con:
  assert con.execute('select count(*) from employee_instances').fetchone()[0]==0
  assert con.execute('select count(*) from canonical_businesses').fetchone()[0]==0


def normal_founding_draft_company(tmp_path):
 from app.database import Database
 from app.runtime import RuntimeFoundation
 db=Database(str(tmp_path/'normal-founding.sqlite'));db.initialize();foundation=RuntimeFoundation(db)
 run=foundation.create('FOUNDING_RUN',owner_ref=CEO)
 for target,actor in [('INTENT_CAPTURED','CEO'),('CLARIFYING','SYSTEM'),('PROPOSED','SYSTEM'),('CEO_CONFIRMED','CEO')]:
  run=foundation.transition(run['entity_id'],target,actor=actor,trigger='normal founding fixture')
 run,assistant=foundation.materialize_company(run['entity_id'],company_id=COMPANY,ceo_id=CEO,name='正常创立测试公司')
 from app.employee_templates import EmployeeTemplateContract
 department=EmployeeTemplateContract(db).create_department_instance(template_id='dt_music',name='音乐部',company_id=COMPANY,enabled_employee_template_ids=[],enabled=True,status='active')
 with db.connect() as con:
  assert con.execute('select status from companies where company_id=?',(COMPANY,)).fetchone()[0]=='draft'
  baseline=con.execute('select count(*) from employee_instances').fetchone()[0]
 return db,WorkspacePackageRuntime(db,tmp_path/'normal-package-store'),department['id'],run,assistant,baseline


def test_draft_company_normal_founding_new_install_and_explicit_empty_completion(tmp_path,monkeypatch):
 with scope():
  db,runtime,department,run,assistant,baseline=normal_founding_draft_company(tmp_path)
  with monkeypatch.context() as patch:
   patch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',lambda *a,**k: {})
   detail=runtime.install(ASSETS/'music',COMPANY,department_id=department,business_id='team-business',business_name='原空团队业务')
  ws=detail['instance']['workspace_id'];result=runtime.complete_professional_team(ws,**payload(detail))
  assert result['current_team']['companyEmployeeRef']
  assert runtime.complete_professional_team(ws,**payload(detail))['receipt']==result['receipt']
  from app.runtime import RuntimeFoundation
  assert RuntimeFoundation(db).get(run['entity_id'])==run
  assert RuntimeFoundation(db).get(assistant['entity_id'])==assistant
  with db.connect() as con:
   assert con.execute('select status from companies where company_id=?',(COMPANY,)).fetchone()[0]=='draft'
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==baseline+1
  second=WorkspacePackageRuntime(db,tmp_path/'normal-package-store')
  other=second.install(ASSETS/'writing_authoring',COMPANY,department_id=department,business_id='draft-new-business',business_name='正常草拟公司新业务')
  with db.connect() as con:
   assert con.execute('select status from companies where company_id=?',(COMPANY,)).fetchone()[0]=='draft'
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==baseline+2
  assert other['instance']['workspace_id']!=ws

@pytest.mark.parametrize('state',['disabled','archived'])
def test_draft_company_terminal_unknown_rejected_for_both_commands(tmp_path,monkeypatch,state):
 with scope():
  db,runtime,department,_,_,baseline=normal_founding_draft_company(tmp_path)
  with monkeypatch.context() as patch:
   patch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',lambda *a,**k: {})
   detail=runtime.install(ASSETS/'music',COMPANY,department_id=department,business_id='team-business',business_name='旧空业务')
  with db.connect() as con:con.execute('update companies set status=? where company_id=?',(state,COMPANY))
  with pytest.raises(PackageScopeError):runtime.complete_professional_team(detail['instance']['workspace_id'],**payload(detail))
  with pytest.raises(PackageScopeError):runtime.install(ASSETS/'writing_authoring',COMPANY,department_id=department,business_id='new-rejected',business_name='不可配置业务')
  with db.connect() as con:
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==baseline
   assert con.execute('select status from companies where company_id=?',(COMPANY,)).fetchone()[0]==state


def test_draft_company_wrong_ceo_cannot_complete_or_install(tmp_path,monkeypatch):
 with scope():
  db,runtime,department,_,_,baseline=normal_founding_draft_company(tmp_path)
  with monkeypatch.context() as patch:
   patch.setattr(EmployeeTemplateContract,'materialize_professional_team_in_connection',lambda *a,**k: {})
   detail=runtime.install(ASSETS/'music',COMPANY,department_id=department,business_id='team-business',business_name='旧空业务')
 with scope(ceo_id='other-ceo'):
  with pytest.raises(PackageScopeError):runtime.complete_professional_team(detail['instance']['workspace_id'],**(payload(detail)|{'ceo_id':'other-ceo'}))
  with pytest.raises(PackageScopeError):runtime.install(ASSETS/'writing_authoring',COMPANY,department_id=department,business_id='rejected-other',business_name='其他身份')
 with db.connect() as con:assert con.execute('select count(*) from employee_instances').fetchone()[0]==baseline


@pytest.mark.parametrize('state',['closed','unknown'])
def test_draft_company_schema_rejects_unknown_terminal_labels(tmp_path,state):
 import sqlite3
 with scope():
  db,_,_,_,_,baseline=normal_founding_draft_company(tmp_path)
  with pytest.raises(sqlite3.IntegrityError,match='CHECK constraint'):
   with db.connect() as con:con.execute('update companies set status=? where company_id=?',(state,COMPANY))
  with db.connect() as con:
   assert con.execute('select status from companies where company_id=?',(COMPANY,)).fetchone()[0]=='draft'
   assert con.execute('select count(*) from employee_instances').fetchone()[0]==baseline


def test_music_business_research_publish_preserves_team_and_is_atomic(tmp_path, monkeypatch):
    from fastapi import FastAPI, Request
    from fastapi.testclient import TestClient
    from app.api.team_operating_router import build_team_operating_router
    from app.employee_templates import MUSIC_RESEARCH_RESPONSIBILITY, MUSIC_RESEARCH_WORKFLOW_KEY
    from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation

    db, runtime = company_only(tmp_path)
    with scope():
        with db.connect() as connection:
            connection.execute("begin immediate")
            EmployeeTemplateContract(db).materialize_builtin_organization(connection, company_id=COMPANY)
        detail = install(runtime)
        writing = install(runtime, "writing_authoring", "writing-business")
        workspace = detail["instance"]["workspace_id"]
        package = detail["package"]
        contract = professional_team_contract(package["package_id"], package["version"], package["digest"])
        service = EmployeeTemplateContract(db)
        with db.connect() as connection:
            original = service.professional_team_state_in_connection(
                connection, company_id=COMPANY, business_id="team-business", workspace_id=workspace, contract=contract,
            )
            employee = connection.execute("select * from employee_instances where id=?",
                (original["team"]["companyEmployeeRef"],)).fetchone()
            prior_proofs = service._professional_execution_context(connection, employee)
        assert prior_proofs and writing["instance"]["workspace_id"] != workspace

    app = FastAPI()
    app.include_router(build_team_operating_router(db))

    @app.middleware("http")
    async def identity(request: Request, call_next):
        with scope(role=request.headers.get("x-test-role", "owner"),
                   company_id=request.headers.get("x-test-company", COMPANY),
                   ceo_id=request.headers.get("x-test-ceo", CEO)):
            return await call_next(request)

    params = {"company_id": COMPANY, "scope_type": "BUSINESS", "scope_ref": "team-business",
              "workflow_key": MUSIC_RESEARCH_WORKFLOW_KEY}
    read = "/team-operating/definition"
    publish_path = "/team-operating/definitions/publish"

    def recorded():
        with db.connect() as connection:
            return tuple(tuple(row) for row in connection.execute(
                "select * from runtime_entities order by entity_id"
            )), tuple(tuple(row) for row in connection.execute("select * from runtime_links order by link_id"))

    with TestClient(app) as client:
        before = recorded()
        preview = client.get(read, params=params)
        assert preview.status_code == 200, preview.text
        draft = preview.json()
        assert draft["can_publish"] and draft["published"] is None and draft["scope"]["workspace_id"] is None
        researcher = next(person for person in draft["available_employees"] if person["role"] == "行业研究专家")
        leader = draft["leader"]
        roles = [
            {"responsibility_key": leader["responsibilityKey"], "role_name": leader["roleName"],
             "employee_ref": leader["employeeRef"], "responsibility": leader["responsibility"], "is_leader": True,
             "assignment_ref": leader["assignmentRef"], "role_ref": leader["roleRef"]},
            {"responsibility_key": MUSIC_RESEARCH_RESPONSIBILITY, "role_name": "市场研究",
             "employee_ref": researcher["employee_ref"], "responsibility": "核对公开市场来源"},
        ]
        proof = {"confirm": True, "leader_revision": leader["assignmentRevision"]}
        body = {**params, "roles": roles, "default_flow": [MUSIC_RESEARCH_RESPONSIBILITY], "music_research": proof}
        assert client.get(read, params=params, headers={"x-test-role":"employee"}).json()["available_employees"] == []
        for headers in [{"x-test-role":"employee"}, {"x-test-company":"foreign"}, {"x-test-ceo":"foreign"}]:
            assert client.post(publish_path, json=body, headers=headers).status_code in {403, 409}
        for changes in [
            {"music_research": None}, {"music_research": {**proof, "confirm": False}},
            {"music_research": {**proof, "leader_revision": proof["leader_revision"] + 1}},
            {"scope_ref": "writing-business"}, {"workspace_id": workspace}, {"workflow_key": " " + MUSIC_RESEARCH_WORKFLOW_KEY},
            *[{"roles": [roles[0], {**roles[1], "employee_ref": ref}]} for ref in (leader["employeeRef"], "foreign-worker")],
        ]:
            assert client.post(publish_path, json={**body, **changes}).status_code in {404, 409, 422}
        with db.connect() as connection:
            connection.execute("update employee_instances set enabled=0 where id=?", (researcher["employee_ref"],))
        try:
            assert client.post(publish_path, json=body).status_code == 409
        finally:
            with db.connect() as connection:
                connection.execute("update employee_instances set enabled=1 where id=?", (researcher["employee_ref"],))
        assert recorded() == before
        with monkeypatch.context() as injected:
            def fail_after_assignment(self, **kwargs):
                raise ValueError("fixture: publication failed after role and assignment writes")
            injected.setattr(ResponsibilityRoutingRuntime, "publish_workflow", fail_after_assignment)
            assert client.post(publish_path, json=body).status_code == 409
            assert recorded() == before

        def submit(_):
            response = client.post(publish_path, json=body)
            assert response.status_code == 200, response.text
            return response.json()

        with ThreadPoolExecutor(max_workers=3) as pool:
            original_release, *repeats = pool.map(submit, range(3))
        assert all(other == original_release for other in repeats)
        published = client.get(read, params=params).json()
        assert published == original_release and not published["can_publish"]
        assert published["published"]["version"] == 1 and published["published"]["roles"][0] == leader
        worker = published["published"]["roles"][1]
        assert worker["employeeRef"] == researcher["employee_ref"]
        assert worker["employeeName"] == researcher["name"] and worker["roleName"] == "市场研究"
        assert worker["outputContract"]["resultType"] == "market-summary"
        other = {**body, "roles": [roles[0], {**roles[1], "employee_ref": "other-worker"}]}
        assert client.post(publish_path, json=other).status_code == 409
    with scope():
        f = RuntimeFoundation(db)
        assert f.get(worker["roleRef"])["lifecycle_status"] == "ASSIGNED"
        after = recorded()
        assert len(after[0]) - len(before[0]) == 3
        assert len(after[1]) - len(before[1]) == 2
        with db.connect() as connection:
            current = service.professional_team_state_in_connection(
                connection, company_id=COMPANY, business_id="team-business", workspace_id=workspace, contract=contract,
            )
            assert current["basis"] == original["basis"] and current["team"] == original["team"]
            assert service._professional_execution_context(connection, employee) == prior_proofs
            for table in ("tasks", "ai_usage_records", "employee_capability_bindings", "tenant_private_capabilities"):
                assert connection.execute(f"select count(*) from {table}").fetchone()[0] == 0
