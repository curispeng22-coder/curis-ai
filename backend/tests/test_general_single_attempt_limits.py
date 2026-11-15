"""Technical canonical fixtures and fake transport; never Native or paid evidence."""
import json
import multiprocessing
import os
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.database import Database
from app.tenant_context import TenantContext
from app.runtime.foundation import RuntimeFoundation
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.evolution_event_log import EvolutionEventLog
from app.result_store import ResultStore
from app.model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError
from app.runtime import general_execution_limits as limits
from app.api.team_operating_router import build_team_operating_router
from backend.tests.test_v1_general_operating_contract import seed, add_team, TENANT, COMPANY, WORKSPACE, EMPLOYEE

BOUNDS = {"max_prompt_bytes": 4096, "max_output_tokens": 2048}
META = {"provider_type": "ollama", "model_name": "fixture-model", "base_url": "http://127.0.0.1:9", "provider_protocol": "openai_chat"}


def context():
    return TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="ceo")


@pytest.fixture
def ready(tmp_path, monkeypatch):
    path = tmp_path / "general.sqlite"
    for name in ["CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"]:
        monkeypatch.setenv(name, str(path))
    db = seed(path)
    add_team(db)
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type="model", capability_id="model.fixture", display_name="Technical fixture model", metadata=META)
    with db.connect() as con:
        con.execute("update employee_capability_bindings set capability_type='model', capability_id='model.fixture' where tenant_id=? and id='binding-general'", (TENANT,))
    with context():
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=WORKSPACE, runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE, employee_capability_binding_ref="binding-general")
        work = GeneralWorkspaceDelivery(db).create_work(company_id=COMPANY, workspace_id=WORKSPACE, problem="内部交付核对", expected_result="仅依据提供资料形成清单", constraints=[], references=[], idempotency_key="one-work")["work"]
    return db, work["entity_id"], path


def task_for(db, ref):
    mark = limits.arm(db, ref, BOUNDS)
    routing = ResponsibilityRoutingRuntime(db)
    key = "responsibility:limited:1"
    routing.begin_employee_execution(ref, execution_key=key, assignment_ref=mark["assignment_ref"])
    reserved = limits.reserve_task(db, ref, key)
    task = ResultStore(db).create_task("内部核对", company_id=COMPANY, workspace_id=WORKSPACE, work_ref=ref, execution_ref=key, scope_type="WORKSPACE", scope_ref=WORKSPACE,
                                     capability_source="tenant_private", capability_type="model", capability_id="model.fixture", employee_id=EMPLOYEE)
    limits.bind_task(db, reserved, task["task_id"], key)
    routing.attach_provider_task(ref, execution_key=key, task_ref=task["task_id"])
    EmployeeExecutionIdentity(db).record_task_assignment(company_id=COMPANY, workspace_id=WORKSPACE, assignment_ref=mark["assignment_ref"], assignment_revision=mark["assignment_revision"], runtime_employee_ref=EMPLOYEE, task_ref=task["task_id"], employee_capability_binding_ref="binding-general")
    return task["task_id"]


def adapter(calls, protocol="openai_chat", failure=False):
    def post(url, body, headers, timeout):
        calls.append({"url": url, "body": body, "timeout": timeout})
        if failure:
            raise TimeoutError("Technical response loss")
        output = json.dumps({"status": "ACCEPTED", "resultType": "general-business-result", "summary": "技术fixture输出", "problem": ""})
        if protocol == "anthropic_messages":
            return {"content": [{"type": "text", "text": output}], "usage": {"input_tokens": 20, "output_tokens": 10}}
        if protocol == "gemini_generate_content":
            return {"candidates": [{"content": {"parts": [{"text": output}]}}], "usageMetadata": {"promptTokenCount": 20, "candidatesTokenCount": 10, "totalTokenCount": 30}}
        return {"choices": [{"message": {"content": output}}], "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30}}
    return ModelGatewayAdapter(base_url=META["base_url"], api_key="technical-no-secret", gateway_id="ollama", model_name=META["model_name"], http_post=post, protocol=protocol)


def test_real_snapshot_task_claim_and_bytes_wire(ready):
    db, ref, _ = ready
    with context():
        task = task_for(db, ref)
        calls = []
        model = adapter(calls)
        with pytest.raises(limits.GeneralLimitsError):
            limits.claim_outbound(db, task, "界" * 1366, model)
        assert limits.event(db, limits.OUTBOUND, ref) is None
        bounded = limits.claim_outbound(db, task, "a" * 4096, model)
        model.execute("a" * 4096, max_output_tokens=bounded["max_output_tokens"])
        assert len(calls) == 1 and calls[0]["body"]["max_tokens"] == 2048
        with pytest.raises(limits.GeneralLimitsError):
            limits.claim_outbound(db, task, "a", model)
        assert limits.event(db, limits.OUTBOUND, ref)["task_ref"] == task
        with pytest.raises(limits.GeneralLimitsError):
            limits.arm(db, ref)  # Omitted flag cannot continue or create a second Task.


@pytest.mark.parametrize("value", [True, 1.2, 0, -1, 2049])
def test_strict_output_ceiling(ready, value):
    db, ref, _ = ready
    with context(), pytest.raises(limits.GeneralLimitsError):
        limits.arm(db, ref, {**BOUNDS, "max_output_tokens": value})


@pytest.mark.parametrize("change", ["reparent", "revision", "model", "scope", "corrupt", "consult"])
def test_original_mark_rejects_scope_model_revision_and_corruption(ready, change):
    db, ref, _ = ready
    with context():
        mark = limits.arm(db, ref, BOUNDS)
        with db.connect() as con:
            if change == "reparent":
                con.execute("update runtime_entities set parent_id='another-cycle' where entity_id=?", (ref,))
            elif change == "scope":
                con.execute("update runtime_entities set company_id='another-company' where entity_id=?", (ref,))
            elif change == "corrupt":
                con.execute("update evolution_events set payload='{}' where event_type=? and correlation_id=?", (limits.MARK, ref))
            elif change == "model":
                meta = {**META, "model_name": "different-model"}
                con.execute("update tenant_private_capabilities set metadata_json=? where capability_id='model.fixture'", (json.dumps(meta),))
            else:
                row = con.execute("select data_json from runtime_entities where entity_id=?", (mark["assignment_ref"],)).fetchone()
                data = json.loads(row[0]);data["revision"] += 1
                if change == "consult":
                    data["inputContract"] = {"consultResponsibility": "other"}
                con.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), mark["assignment_ref"]))
        with pytest.raises((limits.GeneralLimitsError, ValueError, KeyError)):
            limits.arm(db, ref)
        assert limits.event(db, limits.OUTBOUND, ref) is None


def _claim_process(path, task, queue):
    db = Database(path)
    with context():
        try:
            model = adapter([])
            bounded = limits.claim_outbound(db, task, "one", model)
            model.execute("one", max_output_tokens=bounded["max_output_tokens"])
            queue.put("winner")
        except Exception:
            queue.put("blocked")


def test_independent_processes_one_winner_and_no_reclaim(ready):
    db, ref, path = ready
    with context():
        task = task_for(db, ref)
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue(); processes = [ctx.Process(target=_claim_process, args=(str(path), task, queue)) for _ in range(2)]
    for p in processes:p.start()
    for p in processes:p.join(20);assert p.exitcode == 0
    assert sorted([queue.get(timeout=5), queue.get(timeout=5)]) == ["blocked", "winner"]
    with context(), pytest.raises(limits.GeneralLimitsError):
        limits.claim_outbound(db, task, "one", adapter([]))  # Winner may have crashed before sending.


@pytest.mark.parametrize("protocol", ["openai_chat", "anthropic_messages", "gemini_generate_content"])
def test_existing_adapter_low_output_protocol_wire(ready, protocol):
    db, ref, _ = ready
    with db.connect() as con:con.execute("update tenant_private_capabilities set metadata_json=? where capability_id='model.fixture'", (json.dumps({**META, "provider_protocol": protocol}),))
    with context():
        mark = limits.arm(db, ref, {**BOUNDS, "max_output_tokens": 32})
        key="responsibility:low:1";ResponsibilityRoutingRuntime(db).begin_employee_execution(ref, execution_key=key, assignment_ref=mark["assignment_ref"])
        reserved=limits.reserve_task(db,ref,key);task=ResultStore(db).create_task("one",company_id=COMPANY,workspace_id=WORKSPACE,scope_type="WORKSPACE",scope_ref=WORKSPACE,work_ref=ref,execution_ref=key,employee_id=EMPLOYEE,capability_source="tenant_private",capability_type="model",capability_id="model.fixture")
        limits.bind_task(db,reserved,task["task_id"],key);ResponsibilityRoutingRuntime(db).attach_provider_task(ref,execution_key=key,task_ref=task["task_id"])
        calls=[];model=adapter(calls,protocol);limits.claim_outbound(db,task["task_id"],"one",model);model.execute("one",max_output_tokens=32)
        payload=calls[0]["body"];assert (payload.get("max_tokens") if protocol!='gemini_generate_content' else payload["generationConfig"]["maxOutputTokens"])==32


def test_claim_survives_transport_timeout_and_different_task(ready):
    db, ref, _ = ready
    with context():
        task=task_for(db,ref);calls=[];model=adapter(calls,failure=True);limits.claim_outbound(db,task,"one",model)
        with pytest.raises(Exception):model.execute("one",max_output_tokens=2048)
        with pytest.raises(limits.GeneralLimitsError):limits.claim_outbound(db,task,"one",model)
        with pytest.raises(limits.GeneralLimitsError):limits.reserve_task(db,ref,"different-key")
        assert len(calls)==1


def test_actual_strict_api_marks_before_submit_and_normal_mode_unchanged(ready):
    db, ref, _ = ready
    calls=[]
    async def execution(request):calls.append(request);raise RuntimeError("Technical stop before Task/HTTP")
    app=FastAPI()
    @app.middleware("http")
    async def actor(request:Request, call_next):
        with context():return await call_next(request)
    app.include_router(build_team_operating_router(db,execution))
    with TestClient(app) as client:
        assert client.post(f"/team-operating/works/{ref}/execute?max_executions=1",json={**BOUNDS,"max_output_tokens":True}).status_code==422
        assert calls==[]
        response=client.post(f"/team-operating/works/{ref}/execute?max_executions=1",json=BOUNDS)
        assert response.status_code==200,response.text
    with context():assert limits.work_limits(db,ref)
    assert len(calls)==1

def test_actual_main_single_task_step_and_sink_limits_no_replay(ready, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    import app.orchestrator as orchestrator_module
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    db, ref, path = ready
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    def forbidden_pattern(*args):
        raise AssertionError("Limited Task must not enter learned or keyword expansion")
    monkeypatch.setattr(orchestrator_module.Orchestrator, "generate_auto_workflow", forbidden_pattern)
    calls=[]
    with TestClient(create_app(str(path), model_gateway_adapter=adapter(calls))) as client:
        response=client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1",json=BOUNDS,headers={"X-Tenant-Id":TENANT,"X-Ceo-Id":"ceo"})
        assert response.status_code==200,response.text
        assert len(calls)==1,response.text
        assert calls[0]["body"]["max_tokens"]==2048
        replay=client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1",headers={"X-Tenant-Id":TENANT,"X-Ceo-Id":"ceo"})
        assert len(calls)==1
        assert replay.status_code in {200,422}
    with context():
        mark=limits.work_limits(db,ref);assert mark
        with db.connect() as con:
            assert con.execute("select count(*) from tasks where work_ref=?",(ref,)).fetchone()[0]==1
            usage=con.execute("select * from ai_usage_records where task_id=?",(limits.event(db,limits.OUTBOUND,ref)["task_ref"],)).fetchall()
            assert len(usage)==1
        task_ref=limits.event(db,limits.OUTBOUND,ref)["task_ref"]
        workflow=ResultStore(db).get_workflow(task_ref)["workflow_plan"]
        assert len(workflow)==1 and workflow[0]["tool_required"]=="model_gateway_tool"


def test_actual_unbounded_normal_path_and_strict_invalid_body(ready, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    db,ref,path=ready
    monkeypatch.setenv("CURIS_ENV","test");monkeypatch.setenv("CURIS_IDENTITY_MODE","test")
    calls=[]
    with TestClient(create_app(str(path),model_gateway_adapter=adapter(calls))) as client:
        headers={"X-Tenant-Id":TENANT,"X-Ceo-Id":"ceo"}
        rejected=client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute",json={**BOUNDS,"unexpected":1},headers=headers)
        assert rejected.status_code==422 and calls==[]
        response=client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1",headers=headers)
        assert response.status_code==200,response.text
        assert calls and "max_tokens" not in calls[0]["body"]
    with context():assert limits.work_limits(db,ref) is None

@pytest.mark.parametrize("case",["actor","task-work","task-model","marker-missing","binding-corrupt","adapter-endpoint","adapter-profile","agent"])
def test_scoped_limits_reject_all_untrusted_or_changed_paths(ready,case):
    db,ref,_=ready
    if case=="actor":
        with TenantContext.scope(TENANT,company_id=COMPANY,role="employee"),pytest.raises(limits.GeneralLimitsError):limits.arm(db,ref,BOUNDS)
        return
    with context():
        task=task_for(db,ref)
        calls=[];model=adapter(calls)
        with db.connect() as con:
            if case=="task-work":con.execute("update tasks set work_ref='other' where task_id=?",(task,))
            elif case=="task-model":con.execute("update tasks set requested_capability_id='other' where task_id=?",(task,))
            elif case=="marker-missing":con.execute("delete from evolution_events where event_type=? and correlation_id=?",(limits.MARK,ref))
            elif case=="binding-corrupt":con.execute("update evolution_events set payload='{}' where event_type=? and correlation_id=?",(limits.BIND,task))
            elif case=="agent":con.execute("update employee_capability_bindings set capability_type='agent' where id='binding-general'")
        if case=="adapter-endpoint":model.base_url="http://127.0.0.1:10"
        elif case=="adapter-profile":model.profile="different-profile"
        with pytest.raises((limits.GeneralLimitsError,ValueError,KeyError)):limits.claim_outbound(db,task,"one",model)
        assert calls==[] and limits.event(db,limits.OUTBOUND,ref) is None


def test_claim_db_failure_and_invalid_limits_never_send(ready,monkeypatch):
    db,ref,_=ready
    with context():
        task=task_for(db,ref);calls=[];model=adapter(calls)
        original=EvolutionEventLog.record
        def fail(self,**kwargs):
            if kwargs['event_type']==limits.OUTBOUND:raise RuntimeError('Technical DB failure before claim commit')
            return original(self,**kwargs)
        monkeypatch.setattr(EvolutionEventLog,'record',fail)
        with pytest.raises(RuntimeError):limits.claim_outbound(db,task,'one',model)
        assert calls==[] and limits.event(db,limits.OUTBOUND,ref) is None


def test_actual_provider_output_violation_keeps_confirmed_usage_and_no_retry(ready,monkeypatch):
    monkeypatch.setenv('CURIS_PRODUCT','workspace');monkeypatch.setenv('CURIS_LOCAL_OWNER_ENABLED','0')
    from app.main import create_app
    from app.identity_membership import IdentityMembership,AuthorizedMembership
    monkeypatch.setattr(IdentityMembership,'_authorize_test',lambda self,tenant,request_id:AuthorizedMembership('technical-owner',tenant,COMPANY,'ceo','ceo','active',request_id))
    db,ref,path=ready;calls=[];model=adapter(calls);post=model.http_post
    def overshoot(*args):
        value=post(*args);value['usage']={'prompt_tokens':20,'completion_tokens':2049,'total_tokens':2069};return value
    model.http_post=overshoot
    with TestClient(create_app(str(path),model_gateway_adapter=model)) as client:
        headers={'X-Tenant-Id':TENANT,'X-Ceo-Id':'ceo'}
        response=client.post(f'/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1',json=BOUNDS,headers=headers)
        assert response.status_code==200,response.text
        assert len(calls)==1
        client.post(f'/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1',headers=headers)
        assert len(calls)==1
    with context(),db.connect() as con:
        usage=con.execute('select * from ai_usage_records where execution_status=?',('limit_violation',)).fetchall()
        assert len(usage)==1 and usage[0]['output_tokens']==2049 and usage[0]['metering_status']=='confirmed'
        task=con.execute('select status from tasks where work_ref=?',(ref,)).fetchone()
        assert task['status']=='FAILED'

def test_missing_mark_cannot_become_unbounded_or_mint_another_task(ready):
    db,ref,_=ready
    with context():
        task_for(db,ref)
        with db.connect() as con:con.execute('delete from evolution_events where event_type=? and correlation_id=?',(limits.MARK,ref))
        with pytest.raises(limits.GeneralLimitsError):limits.arm(db,ref,None)
        with pytest.raises(limits.GeneralLimitsError):limits.reserve_task(db,ref,'another-key')
        with db.connect() as con:assert con.execute('select count(*) from tasks where work_ref=?',(ref,)).fetchone()[0]==1

@pytest.mark.parametrize('field',['event_type','correlation_id'])
def test_original_key_lookup_rejects_receipt_identity_migration(ready,field):
    db,ref,_=ready
    with context():
        limits.arm(db,ref,BOUNDS)
        with db.connect() as con:con.execute(f'update evolution_events set {field}=? where event_type=? and correlation_id=?',('changed-purpose-or-identity',limits.MARK,ref))
        with pytest.raises(limits.GeneralLimitsError):limits.arm(db,ref,None)
        with pytest.raises(limits.GeneralLimitsError):limits.reserve_task(db,ref,'new-key')

@pytest.mark.parametrize('scope,ref',[('COMPANY',COMPANY),('DEPARTMENT','department'),('BUSINESS','business-v1-general'),('WORKSPACE',WORKSPACE)])
def test_unmarked_existing_four_scope_tasks_have_no_new_limit(ready,scope,ref):
    db,_,_=ready
    with context():
        task=ResultStore(db).create_task('原正常请求',company_id=COMPANY,workspace_id=WORKSPACE if scope=='WORKSPACE' else None,scope_type=scope,scope_ref=ref)
        assert limits.task_limits(db,task['task_id']) is None

def test_actual_unknown_metering_is_not_zero_and_attempt_is_not_refunded(ready,monkeypatch):
    monkeypatch.setenv('CURIS_PRODUCT','workspace');monkeypatch.setenv('CURIS_LOCAL_OWNER_ENABLED','0')
    from app.main import create_app
    from app.identity_membership import IdentityMembership,AuthorizedMembership
    monkeypatch.setattr(IdentityMembership,'_authorize_test',lambda self,tenant,request_id:AuthorizedMembership('technical-owner',tenant,COMPANY,'ceo','ceo','active',request_id))
    db,ref,path=ready;calls=[];model=adapter(calls);post=model.http_post
    def unmetered(*args):
        value=post(*args);value.pop('usage');return value
    model.http_post=unmetered
    with TestClient(create_app(str(path),model_gateway_adapter=model)) as client:
        headers={'X-Tenant-Id':TENANT,'X-Ceo-Id':'ceo'}
        client.post(f'/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1',json=BOUNDS,headers=headers)
        client.post(f'/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1',headers=headers)
        assert len(calls)==1
    with context(),db.connect() as con:
        usage=con.execute('select total_tokens,cost_amount,metering_status from ai_usage_records where task_id=?',(limits.event(db,limits.OUTBOUND,ref)['task_ref'],)).fetchall()
        assert len(usage)==1 and usage[0]['total_tokens'] is None and usage[0]['cost_amount'] is None and usage[0]['metering_status']=='unknown'


def _command_ownership_worker(path, ref, role, schedule, fixed, barrier, phases, queue, folder):
    """Force the saved stale-write shape through real commands; wrappers are test-only."""
    from pathlib import Path
    import traceback
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.api import team_operating_router as router_module
    assert all(os.environ.get(k) == path for k in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"))
    counts = dict(begin=0, attach=0, finish=0, CONTINUE=0)
    calls = []
    report = {"role": role, "pid": os.getpid(), "schedule": schedule, "fixed": fixed}
    def wait(name):
        assert phases[name].wait(15), "barrier timed out: " + name
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("CURIS_PRODUCT", "workspace")
        patch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
        patch.setenv("CURIS_ENV", "test")
        patch.setenv("CURIS_IDENTITY_MODE", "test")
        patch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
        original_arm = router_module.arm_general_limits
        def arm(*args, **kwargs):
            value = original_arm(*args, **kwargs)
            barrier.wait(15)
            return value
        patch.setattr(router_module, "arm_general_limits", arm)
        original_reserve = limits.reserve_task
        def reserve(*args, **kwargs):
            if role == "loser":
                wait("winner_pause")
            return original_reserve(*args, **kwargs)
        patch.setattr(limits, "reserve_task", reserve)
        original_begin = ResponsibilityRoutingRuntime.begin_employee_execution
        def begin(self, *args, **kwargs):
            counts["begin"] += 1
            if fixed and schedule == "stale_begin" and role == "winner":
                phases["winner_pause"].set()
                wait("loser_done")
            return original_begin(self, *args, **kwargs)
        patch.setattr(ResponsibilityRoutingRuntime, "begin_employee_execution", begin)
        original_attach = ResponsibilityRoutingRuntime.attach_provider_task
        def attach(self, *args, **kwargs):
            counts["attach"] += 1
            if role == "winner" and schedule == "stale_finish":
                phases["winner_pause"].set()
                wait("loser_done" if fixed else "stale_read")
                value = original_attach(self, *args, **kwargs)
                phases["attached"].set()
                if not fixed:
                    wait("stale_written")
                return value
            return original_attach(self, *args, **kwargs)
        patch.setattr(ResponsibilityRoutingRuntime, "attach_provider_task", attach)
        original_finish = ResponsibilityRoutingRuntime.finish_employee_execution
        def finish(self, *args, **kwargs):
            counts["finish"] += 1
            return original_finish(self, *args, **kwargs)
        patch.setattr(ResponsibilityRoutingRuntime, "finish_employee_execution", finish)
        original_route = ResponsibilityRoutingRuntime.route
        def route(self, *args, **kwargs):
            if kwargs.get("signal") == "CONTINUE":
                counts["CONTINUE"] += 1
            return original_route(self, *args, **kwargs)
        patch.setattr(ResponsibilityRoutingRuntime, "route", route)
        original_write = ResponsibilityRoutingRuntime._write_work
        def write(self, work, routing, assignment, **kwargs):
            if not fixed and role == "loser" and routing.get("lastAction") == "EMPLOYEE_RESULT_FAILED":
                report["captured_stale_lease"] = routing["executions"]
                phases["stale_read"].set()
                wait("attached")
                value = original_write(self, work, routing, assignment, **kwargs)
                phases["stale_written"].set()
                return value
            return original_write(self, work, routing, assignment, **kwargs)
        patch.setattr(ResponsibilityRoutingRuntime, "_write_work", write)
        model = adapter(calls)
        original_post = model.http_post
        def physical(*args):
            fd = os.open(str(Path(folder) / "global-http.jsonl"), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            try:
                os.write(fd, (json.dumps({"role": role, "pid": os.getpid(), "max_tokens": args[1].get("max_tokens")}) + "\n").encode())
            finally:
                os.close(fd)
            return original_post(*args)
        model.http_post = physical
        try:
            with TestClient(create_app(path, model_gateway_adapter=model)) as client:
                result = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1", json=BOUNDS, headers={"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"})
                report.update(status=result.status_code, body=result.json())
        except BaseException:
            report["exception"] = traceback.format_exc()
        finally:
            report.update(core_calls=counts, fake_http_count=len(calls))
            Path(folder, role + "-response.json").write_text(json.dumps(report, indent=2))
            phases["loser_done"].set() if role == "loser" else None
            queue.put(report)


@pytest.mark.parametrize("schedule", ["stale_finish", "stale_begin"])
def test_deterministic_full_command_ownership(ready, schedule):
    from pathlib import Path
    db, ref, path = ready
    fixed = os.environ.get("CURIS_CONCURRENCY_PREFIX") != "1"
    if not fixed and schedule != "stale_finish":
        pytest.skip("Only one controlled pre-fix reproduction is authorized")
    folder = path.parent / schedule
    folder.mkdir()
    ctx = multiprocessing.get_context("spawn")
    barrier = ctx.Barrier(2)
    phases = {k: ctx.Event() for k in ("winner_pause", "loser_done", "stale_read", "attached", "stale_written")}
    queue = ctx.Queue()
    processes = [ctx.Process(target=_command_ownership_worker, args=(str(path), ref, role, schedule, fixed, barrier, phases, queue, str(folder))) for role in ("winner", "loser")]
    for p in processes:
        p.start()
    for p in processes:
        p.join(25)
    reports = [json.loads((folder / (role + "-response.json")).read_text()) if (folder / (role + "-response.json")).exists() else {"role": role, "response": "NOT_CAPTURED", "exit": p.exitcode} for role, p in zip(("winner", "loser"), processes)]
    trace = folder / "global-http.jsonl"
    physical = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
    with context(), db.connect() as con:
        tasks = [dict(row) for row in con.execute("select task_id,status,error from tasks where work_ref=?", (ref,))]
        work = RuntimeFoundation(db).get(ref)
        events = {kind: con.execute("select count(*) from evolution_events where event_type=? and (correlation_id=? or json_extract(payload,'$.work_ref')=?)", (kind, ref, ref)).fetchone()[0] for kind in (limits.MARK, limits.RESERVE, limits.BIND, limits.OUTBOUND)}
    evidence = {"technicalFixture": True, "fixed": fixed, "schedule": schedule, "work_ref": ref, "reports": reports, "physical": physical, "tasks": tasks, "routing": work["data"]["responsibilityRouting"], "events": events}
    # Always persist both command responses and missing-counter truth before assertions.
    (folder / "combined.json").write_text(json.dumps(evidence, indent=2))
    assert all(p.exitcode == 0 for p in processes), evidence
    assert all("exception" not in report for report in reports), evidence
    assert len(tasks) == 1, evidence
    lease = next(iter(evidence["routing"]["executions"].values()))
    if not fixed:
        assert tasks[0]["status"] == "INIT" and lease["status"] == "FAILED" and lease["taskRef"] is None, evidence
        assert physical == [] and events[limits.OUTBOUND] == 0, evidence
    else:
        assert reports[0]["status"] == 200 and reports[1]["status"] == 422, evidence
        assert reports[1]["core_calls"] == dict(begin=0, attach=0, finish=0, CONTINUE=0), evidence
        assert len(physical) == 1 and sum(r["fake_http_count"] for r in reports) == 1, evidence
        assert tasks[0]["status"] == "COMPLETED" and lease["status"] == "ACCEPTED" and lease["taskRef"] == tasks[0]["task_id"], evidence
        assert evidence["routing"]["status"] == "COMPLETED" and all(count == 1 for count in events.values()), evidence


@pytest.mark.parametrize("case", ["missing", "persisted_nonce", "live_once"])
def test_internal_owner_cannot_be_supplied_or_replayed(ready, monkeypatch, case):
    import asyncio
    from app.main import create_app
    from app.api import runtime_foundation_router as factory
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    captured = {}
    original = factory.build_team_operating_router
    def capture(db, executor):
        captured.update(database=db, executor=executor)
        return original(db, executor)
    monkeypatch.setattr(factory, "build_team_operating_router", capture)
    _, ref, path = ready
    create_app(str(path), model_gateway_adapter=adapter([]))
    db, executor = captured["database"], captured["executor"]
    with context():
        mark = limits.arm(db, ref, BOUNDS)
        key = f"responsibility:{ref}:{mark['assignment_ref']}:1"
        assignment = next(a for a in RuntimeFoundation(db).get(mark["workflow_ref"])["data"]["assignments"] if a["assignmentRef"] == mark["assignment_ref"])
        request = dict(execution_ref="team_employee:auto", mode="submit", company_id=COMPANY, workspace_id=WORKSPACE, work_ref=ref, execution_key=key, runtime_employee_ref=EMPLOYEE, assignment=assignment, prompt="Technical internal ownership fixture")
        async def exercise():
            if case != "live_once":
                limits.reserve_task(db, ref, key)
                ResponsibilityRoutingRuntime(db).begin_employee_execution(ref, execution_key=key, assignment_ref=mark["assignment_ref"])
                if case == "persisted_nonce":
                    request.update(command_owner=limits.event(db, limits.RESERVE, ref), owner_nonce=limits.event(db, limits.RESERVE, ref)["nonce"], limits=mark)
                with pytest.raises(limits.GeneralLimitsError):
                    await executor(request)
                return
            with limits.command_owner(db, ref, key, executor):
                with pytest.raises(limits.GeneralLimitsError):
                    with limits.command_owner(db, ref, key, executor):
                        pass
                ResponsibilityRoutingRuntime(db).begin_employee_execution(ref, execution_key=key, assignment_ref=mark["assignment_ref"])
                with pytest.raises(limits.GeneralLimitsError):
                    await asyncio.create_task(executor(request))
                with pytest.raises(limits.GeneralLimitsError):
                    limits.consume_task_owner(db, ref, key, lambda _: None)
                first = await executor(request)
                assert first["task_ref"]
                with pytest.raises(limits.GeneralLimitsError):
                    await executor(request)
            with pytest.raises(limits.GeneralLimitsError):
                await executor(request)
        asyncio.run(exercise())
        with db.connect() as con:
            assert con.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0] == (1 if case == "live_once" else 0)
        assert limits.event(db, limits.OUTBOUND, ref) is None


@pytest.mark.parametrize("case", ["same", "input_drift", "output_drift", "active_unpublished"])
def test_published_contract_identity_is_the_validation_input(ready, case):
    db, ref, _ = ready
    with context():
        mark = limits.arm(db, ref, BOUNDS)
        with db.connect() as con:
            target = mark["assignment_ref"] if case == "active_unpublished" else mark["workflow_ref"]
            row = con.execute("select data_json from runtime_entities where entity_id=?", (target,)).fetchone()
            data = json.loads(row[0])
            assignment = data if case == "active_unpublished" else data["assignments"][0]
            if case in {"input_drift", "active_unpublished"}:
                assignment["inputContract"] = {"consultResponsibility": "not-published"} if case == "active_unpublished" else {"requiredRefs": ["changed-unpublished-ref"]}
            if case == "output_drift":
                assignment["outputContract"] = {"resultType": "changed-result"}
            con.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(data), target))
            stored = json.loads(con.execute("select data_json from runtime_entities where entity_id=?", (target,)).fetchone()[0])
            assert stored == data  # This fixture really edits the intended row.
        if case in {"input_drift", "output_drift"}:
            with pytest.raises(limits.GeneralLimitsError):
                limits.work_limits(db, ref)
        else:
            assert limits.work_limits(db, ref) == mark
        assert limits.event(db, limits.OUTBOUND, ref) is None


@pytest.mark.parametrize("failure", ["task_commit", "reservation_commit", "timeout"])
def test_owner_failure_holds_without_replacement(ready, monkeypatch, failure):
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    db, ref, path = ready
    calls = []
    original_task = ResultStore.create_task
    if failure == "task_commit":
        def fail_task(self, *args, **kwargs):
            if kwargs.get("work_ref") == ref:
                raise RuntimeError("Technical Task commit failure")
            return original_task(self, *args, **kwargs)
        monkeypatch.setattr(ResultStore, "create_task", fail_task)
    if failure == "reservation_commit":
        with context(), db.connect() as con:
            con.execute("create trigger deny_reserved before insert on evolution_events when NEW.event_type='general.execution_task.reserved' begin select raise(ABORT,'Technical reservation commit failure'); end")
    with TestClient(create_app(str(path), model_gateway_adapter=adapter(calls, failure=failure == "timeout")), raise_server_exceptions=False) as client:
        headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
        url = f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1"
        first = client.post(url, json=BOUNDS, headers=headers)
        second = client.post(url, headers=headers)
    with context(), db.connect() as con:
        count = con.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0]
        route = RuntimeFoundation(db).get(ref)["data"]["responsibilityRouting"]
        assert count == (1 if failure == "timeout" else 0)
        assert len(calls) == (1 if failure == "timeout" else 0)
        if failure == "reservation_commit":
            assert limits.event(db, limits.RESERVE, ref) is None and not route.get("executions")
        else:
            assert limits.event(db, limits.RESERVE, ref) is not None and route["status"] == "WAITING"
            assert second.status_code == 422
        assert first.status_code in {200, 500}, first.text


def _owner_crash_worker(path, ref):
    import asyncio
    assert all(os.environ.get(k) == path for k in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"))
    db = Database(path)
    with context():
        value = limits.work_limits(db, ref)
        key = f"responsibility:{ref}:{value['assignment_ref']}:1"
        async def crash():
            with limits.command_owner(db, ref, key, lambda _: None):
                os._exit(0)  # Test worker dies after commit, before Core or Task creation.
        asyncio.run(crash())


def test_committed_owner_crash_is_not_reclaimed(ready, monkeypatch):
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    db, ref, path = ready
    with context():
        limits.arm(db, ref, BOUNDS)
    p = multiprocessing.get_context("spawn").Process(target=_owner_crash_worker, args=(str(path), ref))
    p.start()
    p.join(15)
    assert p.exitcode == 0
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    calls = []
    with TestClient(create_app(str(path), model_gateway_adapter=adapter(calls))) as client:
        response = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1", headers={"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"})
        assert response.status_code == 422
    with context(), db.connect() as con:
        assert limits.event(db, limits.RESERVE, ref) and limits.event(db, limits.OUTBOUND, ref) is None
        assert not RuntimeFoundation(db).get(ref)["data"]["responsibilityRouting"].get("executions")
        assert con.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0] == 0
    assert calls == []


def test_context_goal_opt_out_keeps_default_excerpt_and_all_other_context():
    from copy import deepcopy
    from app.context_service import ContextService
    from app.prompt_builder import PromptBuilder
    content = "公开样例。" * 138 + "x" * 7  # 2077 UTF-8 bytes, no private Task text.
    assert len(content.encode()) == 2077
    package = {"id": "context-public-fixture", "task_goal": content,
               "relevant_memory": [{"memory_type": "task", "memory_level": "local", "title": "记忆", "content": "公开事实"}],
               "relevant_knowledge": [{"scope_name": "workspace", "title": "资料", "summary": "公开参考"}],
               "required_tools": ["model.fixture"], "constraints": [*ContextService.CONSTRAINTS, "Canonical scope: fixture-only"],
               "output_requirement": "保留完整要求"}
    before = deepcopy(package)
    service = ContextService(None, None, None)
    ordinary = service.prompt_excerpt(package)
    limited = service.prompt_excerpt(package, include_task_goal=False)
    assert ordinary == service.prompt_excerpt(package, include_task_goal=True)
    assert ordinary.replace("Task Goal: " + content + "\n", "", 1) == limited
    assert package == before
    builder = PromptBuilder()
    old = builder.build(content, skill_excerpt="公开员工指导", context_excerpt=ordinary)
    new = builder.build(content, skill_excerpt="公开员工指导", context_excerpt=limited)
    assert old.count(content) == 2 and new.count(content) == 1
    assert len(old.encode()) > 4096 >= len(new.encode())
    assert len(old.encode()) - len(new.encode()) == 2089
    for value in [*package["constraints"], "公开员工指导", "公开事实", "公开参考", "model.fixture", "保留完整要求"]:
        assert value in new


@pytest.mark.parametrize("limited,cached,writing,resuming,expected", [
    (True, False, False, False, [False]),
    (True, True, False, False, [True]),
    (False, False, False, False, [True]),
    (False, True, False, False, [True]),
    (False, False, False, True, [True]),
    (False, False, True, False, []),
    (True, False, False, True, []),
])
def test_goal_omission_is_only_for_fresh_limited_general_builder(monkeypatch, limited, cached, writing, resuming, expected):
    import asyncio
    from types import SimpleNamespace
    from app.orchestrator import Orchestrator
    from app.prompt_builder import PromptBuilder
    class StopBeforePrompt(Exception):
        pass
    seen = []
    task = {"task_id": "public-task", "status": "RESUMED" if resuming else "PENDING", "content": "公开正文", "prompt": "已有完整提示" if cached else None}
    store = SimpleNamespace(database=None, event_log=None, get_task=lambda _: task)
    context_service = SimpleNamespace(build=lambda _: {"id": "public-context"},
        prompt_excerpt=lambda package, include_task_goal=True: seen.append(include_task_goal) or "公开上下文")
    def stop(_):
        raise StopBeforePrompt()
    control = SimpleNamespace(mark_started=lambda _: None, mark_capability_selected=lambda _: None,
        mark_knowledge_retrieved=lambda *_: None, raise_if_stopped=stop)
    runner = Orchestrator(store, PromptBuilder(), None, context_service=context_service, execution_control=control)
    monkeypatch.setattr(limits, "task_limits", lambda *_: {"max_prompt_bytes": 4096} if limited else None)
    monkeypatch.setattr(runner, "_writing_reply_selection", lambda _: {"purpose": "WRITING_CHAPTER_REPLY"} if writing else None)
    with pytest.raises(ValueError if limited and resuming else StopBeforePrompt):
        asyncio.run(runner.run("public-task"))
    assert seen == expected
    assert task["prompt"] == ("已有完整提示" if cached else None)


@pytest.mark.parametrize("content_bytes", [2077, 4097])
def test_actual_general_assembled_prompt_deduplicates_without_relaxing_limits(ready, monkeypatch, content_bytes):
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.context_service import ContextService
    from app.skill_runtime import SkillRuntime
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    db, ref, path = ready
    content = "公开样例。" * (content_bytes // 15) + "x" * (content_bytes % 15)
    assert len(content.encode()) == content_bytes
    original_create = ResultStore.create_task
    def create_public_task(self, _content, *args, **kwargs):
        return original_create(self, content, *args, **kwargs)
    monkeypatch.setattr(ResultStore, "create_task", create_public_task)
    monkeypatch.setattr(SkillRuntime, "prompt_excerpt", lambda *_: "公开员工指导必须保留")
    calls = []
    with TestClient(create_app(str(path), model_gateway_adapter=adapter(calls))) as client:
        headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
        url = f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1"
        response = client.post(url, json=BOUNDS, headers=headers)
        assert response.status_code == 200, response.text
        with context(), db.connect() as con:
            tasks = con.execute("select * from tasks where work_ref=?", (ref,)).fetchall()
            assert len(tasks) == 1
            task = dict(tasks[0])
            package = ContextService(db, None, None).get(task["context_package_id"])
            assert package["task_goal"] == task["content"] == content
            assert task["prompt"].count(content) == 1
            assert "公开员工指导必须保留" in task["prompt"]
            for value in [*package["constraints"], *package["required_tools"], package["output_requirement"]]:
                assert value in task["prompt"]
            if content_bytes == 2077:
                assert len(calls) == 1
                wire = calls[0]["body"]
                assert wire["max_tokens"] == 2048
                assert wire["messages"][-1]["content"] == task["prompt"]
                assert len(task["prompt"].encode()) <= 4096
                assert limits.event(db, limits.OUTBOUND, ref)["prompt_bytes"] == len(task["prompt"].encode())
            else:
                assert calls == [] and task["status"] == "FAILED"
                assert task["error"] == "Complete prompt exceeds the approved byte limit"
                assert limits.event(db, limits.OUTBOUND, ref) is None
        client.post(url, json=BOUNDS, headers=headers)
        assert len(calls) == (1 if content_bytes == 2077 else 0)
    with context(), db.connect() as con:
        assert con.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0] == 1
        assert limits.event(db, limits.RESERVE, ref) is not None


@pytest.mark.parametrize("damage,limited", [(None, True), ("body", True), ("missing-body", True),
    ("missing-receipt", True), ("missing-event", True), ("oversize", True),
    pytest.param(None, False, id="ordinary-atomic")])
def test_installed_skill_normal_work_persists_result_or_failure_without_replay(ready, monkeypatch, damage, limited):
    from app.main import create_app
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.skill_runtime import SkillRuntime
    from backend.tests.test_skill_package import archive, REPO, COMMIT

    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id:
        AuthorizedMembership("technical-owner", tenant, COMPANY, "ceo", "ceo", "active", request_id))
    db, ref, path = ready
    body = b"# Brief\nInclude a separate heading: Open Questions.\n"
    if damage == "oversize":
        body += b"x" * 4096
    with context():
        runtime = SkillRuntime(db)
        raw = archive({"repo/LICENSE": b"MIT", "repo/SKILL.md": body})
        manifest = runtime.preview_package(REPO, COMMIT, fetch=lambda _: raw)
        skill = runtime.install_repository(repo_url=REPO, commit=COMMIT,
            expected_package_sha256=manifest["package_sha256"], license_accepted=True, fetch=lambda _: raw)
        runtime.set_employee_bindings(EMPLOYEE, [{"skill_template_id": skill["skill_template_id"],
            "capability_binding_ids": ["binding-general"]}])
        package = runtime.package_root() / manifest["package_sha256"]
        if damage == "body":
            (package / "SKILL.md").chmod(0o600)
            (package / "SKILL.md").write_text("damaged")
        elif damage in {"missing-body", "missing-receipt"}:
            (package / ("SKILL.md" if damage == "missing-body" else ".curis-package.json")).unlink()
        elif damage == "missing-event":
            with db.connect() as con:
                con.execute("delete from evolution_events where event_type='skill.package.installed'")
    calls = []
    headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
    url = f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute?max_executions=1"
    with TestClient(create_app(str(path), model_gateway_adapter=adapter(calls))) as client:
        response = client.post(url, json=BOUNDS if limited else None, headers=headers)
        assert response.status_code == 200, response.text
        with context(), db.connect() as con:
            task = dict(con.execute("select * from tasks where work_ref=?", (ref,)).fetchone())
            work = RuntimeFoundation(db).get(ref)
            route = work["data"]["responsibilityRouting"]
            execution = next(iter(route["executions"].values()))
            assert execution["taskRef"] == task["task_id"] and route["currentExecutorRef"] is None
            if damage:
                assert calls == [] and limits.event(db, limits.OUTBOUND, ref) is None
                assert task["status"] == "FAILED" and task["error"] == "skill_guidance_unavailable"
                assert execution["status"] == "FAILED" and route["lastAction"] == "EMPLOYEE_RESULT_FAILED"
                assert route["status"] == "WAITING"
                assert work["lifecycle_status"] == "FAILED"
                assert not task["output"] and not execution["artifactRefs"]
            else:
                assert task["status"] == "COMPLETED"
                assert body.decode() in task["prompt"] and manifest["package_sha256"] in task["prompt"]
                assert len(calls) == 1
                assert calls[0]["body"]["messages"][-1]["content"] == task["prompt"]
                assert execution["status"] == "ACCEPTED" and route["status"] == "COMPLETED"
                assert f"task:{task['task_id']}" in route["resultRefs"]
        client.post(url, json=BOUNDS if limited else None, headers=headers)
        assert len(calls) == (0 if damage else 1)
    with context(), Database(str(path)).connect() as con:
        saved = con.execute("select status,prompt,output,error from tasks where task_id=?", (task["task_id"],)).fetchone()
        assert dict(saved) == {key: task[key] for key in ("status", "prompt", "output", "error")}
        assert con.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0] == 1
        saved_work = RuntimeFoundation(Database(str(path))).get(ref)
        assert saved_work["lifecycle_status"] == work["lifecycle_status"]
