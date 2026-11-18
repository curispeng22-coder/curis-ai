"""Synthetic original-Work receipts through real storage/routes; no public or Provider acceptance."""
import json
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.agent_tool_server import AgentToolSessions
from app.agent_work_resources import AgentWorkResources
from app.api.team_operating_router import build_team_operating_router
from app.conversation_service import digest
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.music_market_evidence import MusicMarketEvidence, AcceptMarketEvidenceIn, MarketBrowserPermissionIn
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation, ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import seed, TENANT, COMPANY, WORKSPACE, BUSINESS


def scope(**changes):
    return TenantContext.scope(**dict(tenant_id=TENANT, company_id=COMPANY, ceo_id="ceo", role="owner") | changes)


def replace_data(db, ref, update):
    data = RuntimeFoundation(db).get(ref)["data"]
    update(data)
    with db.connect() as con:
        con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
            (json.dumps(data), TENANT, ref))


def synthetic_work(db, ref, owner, data):
    with db.connect() as con:
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,parent_id,owner_ref,"
            "lifecycle_status,data_json,created_at,updated_at) values (?,?,'WORK',?,'cycle',?,'ACTIVE',?,'now','now')",
            (ref, TENANT, COMPANY, owner, json.dumps(data)))
    return RuntimeFoundation(db).get(ref)


def fixture(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    db = seed(path)
    from app.workspace_package_runtime import PACKAGE_DDL
    with db.connect() as con:
        con.executescript(PACKAGE_DDL)
    foundation = RuntimeFoundation(db)
    events = EvolutionEventLog(db)
    with db.connect() as con:
        con.execute("insert into installed_workspace_packages "
            "(tenant_id,package_id,version,digest,status,manifest_json,surfaces_json,schemas_json,source_path,stored_path,installed_at) "
            "values (?,'com.curis.local.music','test','test','ACTIVE','{}','{}','{}','','','now')", (TENANT,))
        con.execute("insert into workspace_package_instances values ('test-music',?,?,?,'com.curis.local.music','test',"
            "'test','ACTIVE','now','now')", (TENANT, COMPANY, WORKSPACE))
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) "
            "values ('company-worker',?,?,'department','et_product_manager','fixture','research','idle')", (TENANT, COMPANY))
    foundation.create("AI_EMPLOYEE", entity_id="worker", company_id=COMPANY, lifecycle_status="AVAILABLE",
        data={"companyEmployeeRef": "company-worker"})
    origin = {"conversation_ref": "conversation-fixture", "business_ref": BUSINESS}
    cycle = foundation.create("CYCLE", entity_id="cycle", company_id=COMPANY, lifecycle_status="RUNNING",
        data={"kind": "GENERAL_WORK_CYCLE", "scopeType": "BUSINESS", "scopeRef": BUSINESS,
              "contract": {"conversationResearchSource": origin, "problem": "Research market",
                  "expectedResult": "A reviewed source", "constraints": [], "references": []}})
    for ref, owner, extra in (("root", "leader", {"leaderDelegation": {"childWorkRefs": ["child"]}}),
            ("child", "worker", {"leaderRootWorkRef": "root"})):
        synthetic_work(db, ref, owner, {"kind": "CANONICAL_CHILD_WORK", "cycleRef": "cycle",
                "scopeType": "BUSINESS", "scopeRef": BUSINESS, "responsibilityRouting": {"status": "ACTIVE", "executions": {}}, **extra})
    events.record(correlation_id=origin["conversation_ref"], event_type="conversation.research_work.confirmed",
        payload={**origin, "work_ref": "root", "cycle_ref": "cycle"}, idempotency_key="fixture-confirmed")
    store = ResultStore(db)
    task = store.create_task("Synthetic research", company_id=COMPANY, scope_type="BUSINESS", scope_ref=BUSINESS,
        work_ref="child", execution_ref="leader:worker:fixture", employee_id="company-worker", capability_source="tenant_private", capability_type="agent", capability_id="agent.fixture")
    task_ref = task["task_id"]
    store.transition(task_ref, "COMPLETED", {"output": json.dumps({"status": "ACCEPTED", "summary": "Synthetic result, not market evidence"})})
    resources = AgentWorkResources(path.parent / "agent-work", tenant_id=TENANT, company_id=COMPANY,
        work_ref="child", task_id=task_ref)
    resources.prepare([])
    browser = SimpleNamespace(identity=resources.identity, session="fixture-session", browser_id="fixture-browser", tab=1,
        call=lambda args, original: {"url": "https://example.org/fixture", "result": {"text": "Synthetic study: video 31 percent, 2023."}},
        close=lambda: None)
    tools = AgentToolSessions()
    token = tools.register(resources, [], lambda: False, browser=browser)
    response = tools.handle(token, {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "browser", "arguments": {"action": "observe"}}})
    assert not response["result"]["isError"]
    receipts, calls = resources.collect(), tools.browser_evidence(token)
    tools.close(token)
    artifact = store.save_artifact(task_ref, title="Fixture source", content=json.dumps(receipts[0]),
        source_ref="fixture-source", artifact_type="agent_file_receipt")
    with db.connect() as con:
        con.execute("insert into ai_usage_records(usage_record_id,tenant_id,company_id,model_gateway_id,provider_id,"
            "model_name,currency,cost_source,employee_id,capability_id,capability_type,task_id,department_id,business_id,"
            "work_ref,execution_ref,request_id,execution_status,metering_status,occurred_at,idempotency_key,scope_type,scope_ref,input_tokens,output_tokens,reasoning_tokens,total_tokens,capability_binding_id) "
            "values ('usage',?,?,'fixture','fixture','agent.fixture','CNY','unknown','company-worker','agent.fixture','agent',?,"
            "'department',?,'child','leader:worker:fixture','fixture','success',?,'now','fixture-usage','BUSINESS',?,0,0,0,0,'fixture-binding')",
            (TENANT, COMPANY, task_ref, BUSINESS, 'unknown', BUSINESS))
    events.record(correlation_id=task_ref, event_type="usage.task_execution", idempotency_key="fixture-execution",
        payload={"usage_record_id": "usage", "execution_ref": "leader:worker:fixture", "task_id": task_ref, "work_ref": "child", "company_id": COMPANY,
            "employee_id": "company-worker", "status": "success", "artifact_receipts": receipts, "browser_tool_calls": calls})
    record = {"executionKey": "leader:worker:fixture", "status": "ACCEPTED", "taskRef": task_ref,
        "artifactRefs": [artifact["artifact_id"]], "provenance": {"verification_status": "VERIFIED", "callback_actor_ref": "worker"}}
    replace_data(db, "child", lambda d: d["responsibilityRouting"].setdefault("executions", {}).update({record["executionKey"]: record}))
    app = FastAPI()
    @app.middleware("http")
    async def identity(request, call_next):
        with scope():
            return await call_next(request)
    app.include_router(build_team_operating_router(db))
    service = MusicMarketEvidence(db)
    preview = service.preview("child", task_ref, artifact["artifact_id"])
    payload = {"task_ref": task_ref, "artifact_ref": artifact["artifact_id"], "result_version": preview["result_version"],
        "snapshot_sha256": preview["snapshot_sha256"], "request_id": "fixture-accept", "reviewed": True,
        "metrics": [{"label": "video", "value": "31", "unit": "percent", "period": "2023",
            "population": "synthetic sample", "source_quote": "video 31 percent, 2023"}],
        "limitations": "Synthetic fixture; not public evidence or product acceptance."}
    return db, app, payload, resources


def test_original_business_result_acceptance_http_restart_and_idempotency(tmp_path):
    with scope():
        db, app, payload, _ = fixture(tmp_path / "market.sqlite")
        with db.connect() as con:
            assert MusicMarketEvidence(db).accepted(con, RuntimeFoundation(db).get("root")) is None
        with TestClient(app) as client:
            result = client.post("/team-operating/works/child/market-evidence/accept", json=payload)
            assert result.status_code == 200, result.text
            assert client.post("/team-operating/works/child/market-evidence/accept", json=payload).json() == result.json()
        cold = Database(db.path)
        service = MusicMarketEvidence(cold)
        with cold.connect() as con:
            accepted = service.accepted(con, RuntimeFoundation(cold).get("root"))
            assert accepted["inputs"] == [{"evidence_ref": result.json()["evidence_ref"],
                "evidence_version": result.json()["evidence_version"]}]
            assert con.execute("select count(*) from tasks").fetchone()[0] == 1
            assert con.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE'").fetchone()[0] == 1
        child = RuntimeFoundation(cold).get("child")
        assert child["lifecycle_status"] == "COMPLETED" and child["workspace_id"] is None
        assert child["data"]["resultRefs"] == ["task:" + payload["task_ref"]]


@pytest.mark.parametrize("change", ["unreviewed", "quote", "snapshot", "result", "handwritten", "task", "root", "source-bytes"])
def test_rejects_invalid_acceptance_without_completing_child(tmp_path, change):
    with scope():
        db, app, payload, resources = fixture(tmp_path / "reject.sqlite")
        if change == "unreviewed": payload["reviewed"] = False
        if change == "quote": payload["metrics"][0]["source_quote"] = "invented external fact"
        if change == "snapshot": payload["snapshot_sha256"] = "0" * 64
        if change == "result": payload["result_version"] = "0" * 64
        if change == "task": payload["task_ref"] = "foreign"
        if change == "root": replace_data(db, "root", lambda d: d["leaderDelegation"].update(childWorkRefs=[]))
        if change == "handwritten":
            with db.connect() as con:
                con.execute("update evolution_events set payload=json_set(payload,'$.browser_tool_calls',json('[]')) "
                    "where event_type='usage.task_execution'")
        if change == "source-bytes":
            (resources.path / "output" / resources.collect()[0]["relative_path"]).write_text("tampered")
        with TestClient(app) as client:
            response = client.post("/team-operating/works/child/market-evidence/accept", json=payload)
            assert response.status_code == 422, response.text
        assert RuntimeFoundation(db).get("child")["lifecycle_status"] == "ACTIVE"
        with db.connect() as con:
            assert con.execute("select count(*) from runtime_entities where entity_type='EVIDENCE'").fetchone()[0] == 0


def test_summary_exact_versions_and_changed_result_are_rejected(tmp_path):
    with scope():
        db, _, payload, _ = fixture(tmp_path / "versions.sqlite")
        service = MusicMarketEvidence(db)
        result = service.accept("child", AcceptMarketEvidenceIn(**payload))
        f = RuntimeFoundation(db)
        with db.connect() as con:
            expected = service.accepted(con, f.get("root"))
        summary = synthetic_work(db, "summary", "leader",
            {"leaderRootWorkRef": "root", "scopeType": "BUSINESS", "scopeRef": BUSINESS,
                "responsibilityRouting": {"executions": {"leader:summary:fixture": {"status": "SUBMITTING"}}}})
        replace_data(db, "root", lambda d: d["leaderDelegation"].update(summaryWorkRef=summary["entity_id"]))
        with db.connect() as con:
            con.execute("begin immediate")
            service.pin_summary(con, service._entity(con, "root"), summary["entity_id"], expected, "leader:summary:fixture")
        assert f.get(summary["entity_id"])["data"]["responsibilityRouting"]["executions"]["leader:summary:fixture"]["evidenceInputs"] == expected["inputs"]
        replace_data(db, result["evidence_ref"], lambda d: d.update(limitations="tampered"))
        with db.connect() as con, pytest.raises(PermissionError):
            service.pin_summary(con, service._entity(con, "root"), summary["entity_id"], expected)
        def valid_new_version(data):
            data.pop("payloadSha256")
            data["payloadSha256"] = digest(data)
        replace_data(db, result["evidence_ref"], valid_new_version)
        with db.connect() as con, pytest.raises(PermissionError, match="版本已改变"):
            service.pin_summary(con, service._entity(con, "root"), summary["entity_id"], expected)
        assert f.get(summary["entity_id"])["data"]["marketEvidenceInputs"] == expected["inputs"]


def test_concurrent_acceptance_creates_one_evidence_and_acceptance(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    with scope():
        db, _, payload, _ = fixture(tmp_path / "concurrent.sqlite")
    def accept(_):
        with scope():
            return MusicMarketEvidence(db).accept("child", AcceptMarketEvidenceIn(**payload))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(accept, range(2)))
    assert results[0] == results[1]
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='EVIDENCE'").fetchone()[0] == 1
        assert con.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE'").fetchone()[0] == 1


def test_non_owner_cannot_accept_and_non_music_root_is_not_gated(tmp_path):
    with scope():
        db, _, payload, _ = fixture(tmp_path / "owner.sqlite")
    with scope(ceo_id="foreign"), pytest.raises(PermissionError):
        MusicMarketEvidence(db).accept("child", AcceptMarketEvidenceIn(**payload))
    with scope():
        with db.connect() as con:
            con.execute("delete from workspace_package_instances")
            assert not MusicMarketEvidence(db).applies(con, RuntimeFoundation(db).get("root"))


def leader_fixture(tmp_path, monkeypatch, result_type="market-summary"):
    db, _, payload, _ = fixture(tmp_path / "data/curis.sqlite")
    f, routing = RuntimeFoundation(db), ResponsibilityRoutingRuntime(db)
    f.create("AI_EMPLOYEE", entity_id="leader", company_id=COMPANY, lifecycle_status="AVAILABLE")
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type="model", capability_id="model.fixture",
        display_name="Fixture only", metadata={"testOnly": True})
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) "
            "values ('leader',?,?,'department','et_product_manager','fixture leader','leader','idle')", (TENANT, COMPANY))
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
            "values ('leader-model',?,'leader','tenant_private','model','model.fixture')", (TENANT,))
    assignments = []
    for employee in ("leader", "worker"):
        role = f.create("ROLE_SLOT", company_id=COMPANY, data={"name": employee})
        assignments.append(routing.create_assignment(company_id=COMPANY, workspace_id=None, scope_type="BUSINESS",
            scope_ref=BUSINESS, role_ref=role["entity_id"], employee_ref=employee, responsibility_key=employee,
            responsibility=employee + " responsibility", is_leader=employee == "leader",
            output_contract={"resultType": result_type}))
    routing.publish_workflow(company_id=COMPANY, workspace_id=None, scope_type="BUSINESS", scope_ref=BUSINESS,
        workflow_key="market", assignment_refs=[a["entity_id"] for a in assignments], default_flow=["leader"])
    record = f.get("child")["data"]["responsibilityRouting"]["executions"]["leader:worker:fixture"]
    for ref, assignment in zip(("root", "child"), assignments):
        replace_data(db, ref, lambda d: d.pop("responsibilityRouting"))
        routing.start_work(ref, scope_type="BUSINESS", scope_ref=BUSINESS, workflow_key="market",
            initial_responsibility=assignment["data"]["responsibilityKey"])
        replace_data(db, ref, lambda d: d.update(responsibilityAssignmentRef=assignment["entity_id"]))
    record["assignmentRef"] = assignments[1]["entity_id"]
    replace_data(db, "child", lambda d: d["responsibilityRouting"].setdefault("executions", {}).update({"leader:worker:fixture": record}))
    replace_data(db, "root", lambda d: d["leaderDelegation"].update(planTaskRef="plan-fixture"))
    replace_data(db, "root", lambda d: d["responsibilityRouting"].setdefault("executions", {}).update({"leader:plan:fixture": {
        "executionKey": "leader:plan:fixture", "status": "ACCEPTED", "taskRef": "plan-fixture",
        "provenance": {"provider_capability": {"binding_ref": "leader-model"}}}}))
    return db, payload, f, routing, assignments


def test_same_execute_waits_then_summarizes_once_without_research_retry(tmp_path, monkeypatch):
    with scope():
        db, payload, f, routing, assignments = leader_fixture(tmp_path, monkeypatch)
        calls = []
        async def execute(request):
            assert request["runtime_employee_ref"] == "leader", "research must not be rerun"
            calls.append(request)
            store = ResultStore(db)
            if request["mode"] == "submit":
                task = store.create_task(request["prompt"], company_id=COMPANY, scope_type="BUSINESS", scope_ref=BUSINESS,
                    work_ref=request["work_ref"], execution_ref=request["execution_key"], employee_id="leader")
                return {"task_ref": task["task_id"]}
            with db.connect() as con:
                evidence = MusicMarketEvidence(db).accepted(con, f.get("root"))
            value = {"status": "ACCEPTED", "resultType": "market-summary", "summary": "Synthetic summary"}
            value["recommendation"] = recommendation_fixture(evidence["inputs"])
            output = json.dumps(value)
            store.transition(request["task_ref"], "COMPLETED", {"output": output})
            return {"task_ref": request["task_ref"], "task_status": "COMPLETED", "output": output,
                "session_ref": "fixture-summary", "execution_binding": {"callbackProvenance": {
                    "verification_status": "VERIFIED", "callback_actor_ref": "leader"}}}
        def app():
            instance = FastAPI()
            @instance.middleware("http")
            async def identity(request, call_next):
                with scope(): return await call_next(request)
            instance.include_router(build_team_operating_router(db, employee_execution=execute))
            return instance
        with TestClient(app()) as client:
            waiting = client.post("/team-operating/works/root/execute")
            assert waiting.status_code == 200, waiting.text
            assert waiting.json()["delegation_status"] == "AWAITING_MARKET_EVIDENCE_ACCEPTANCE"
            assert calls == [] and "summaryWorkRef" not in f.get("root")["data"]["leaderDelegation"]
            # Route changes do not change the underlying Result content version.
            accepted = client.post("/team-operating/works/child/market-evidence/accept", json=payload)
            assert accepted.status_code == 200, accepted.text
            response = client.post("/team-operating/works/root/execute")
            assert response.status_code == 200, response.text
            assert response.json()["delegation_status"] == "ACCEPTED", response.text
        assert len(calls) == 2
        assert accepted.json()["evidence_ref"] in calls[0]["prompt"]
        assert accepted.json()["evidence_version"] in calls[0]["prompt"]
        assert "https://example.org/fixture" in calls[0]["prompt"]
        summary = f.get(response.json()["summary_work_ref"])
        records = summary["data"]["responsibilityRouting"]["executions"]
        assert len(records) == 1 and next(iter(records.values()))["evidenceInputs"] == [{
            "evidence_ref": accepted.json()["evidence_ref"], "evidence_version": accepted.json()["evidence_version"]}]
        with TestClient(app()) as restarted:
            replay = restarted.post("/team-operating/works/root/execute")
            assert replay.status_code == 200, replay.text
            assert replay.json()["summary_work_ref"] == summary["entity_id"] and len(calls) == 2


def recommendation_fixture(inputs):
    return {"evidence": inputs, "preferred_channel": "short_video", "rationale": "先检验短片能否引起试听兴趣，尚无转化事实。",
        "short_video": {"suitability": "用于短片触达兴趣人群", "hypothesis": "短片可能带来试听意愿"},
        "streaming_preview": {"suitability": "用于检验完整试听意愿", "hypothesis": "较长试听可能提升收藏意愿"},
        "seven_day_test": {"days": 7, "steps": ["第1至3天准备两组素材与统一记录口径", "第4至7天经批准后测试并比较"],
            "metrics": ["试听完成率：完成数/开始数", "收藏率：收藏数/试听人数"], "decision_rule": "只在样本和口径可比时选择表现较好方向，否则继续观察"},
        "limitations": "2023总体音乐习惯不能证明本歌曲获客或转化。"}


@pytest.mark.parametrize('change', ['failed', 'empty', 'event_execution'])
def test_source_discovery_rejects_non_success_or_cross_execution(tmp_path, change):
    with scope():
        db, app, payload, _ = fixture(tmp_path / 'proof.sqlite')
        with db.connect() as con:
            if change == 'failed':
                replace_data(db, 'child', lambda d: d['responsibilityRouting']['executions']['leader:worker:fixture'].update(status='FAILED'))
            elif change == 'empty':
                con.execute("update tasks set output='' where task_id=?", (payload['task_ref'],))
            elif change == 'model':
                con.execute("update tasks set requested_capability_type='model' where task_id=?", (payload['task_ref'],))
            else:
                con.execute("update evolution_events set payload=json_set(payload,'$.execution_ref','foreign') where event_type='usage.task_execution'")
        with TestClient(app) as client:
            assert client.get('/team-operating/works/child/market-evidence/source').json()['sources'] == []
            assert client.post('/team-operating/works/child/market-evidence/accept', json=payload).status_code == 422


def test_discover_then_read_exact_preview(tmp_path):
    with scope():
        db, app, payload, _ = fixture(tmp_path / 'discover.sqlite')
        with TestClient(app) as client:
            sources = client.get('/team-operating/works/child/market-evidence/source').json()['sources']
            assert sources == [{'work_ref': 'child', 'task_ref': payload['task_ref'], 'artifact_ref': payload['artifact_ref']}]
            preview = client.get('/team-operating/works/child/market-evidence/source', params={k: payload[k] for k in ('task_ref', 'artifact_ref')})
            assert preview.status_code == 200
            assert preview.json()['snapshot_sha256'] == payload['snapshot_sha256']
            assert preview.json()['content_verification'] == 'UNVERIFIED'
            assert client.get('/team-operating/works/child/market-evidence/source', params={'task_ref': payload['task_ref']}).status_code == 422


def unstarted_leader(tmp_path, monkeypatch):
    db, payload, f, routing, assignments = leader_fixture(tmp_path, monkeypatch)
    replace_data(db, 'root', lambda d: (d.pop('leaderDelegation'), d['responsibilityRouting'].update(executions={})))
    return db, f, assignments


def test_real_published_workflow_preflight_blocks_before_any_submit(tmp_path, monkeypatch):
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        ready = service.readiness('root')
        codes = {b['code'] for b in ready['blockers']}
        assert not ready['ready'] and ready['can_set_browser_scope']
        assert {'PUBLIC_HOSTS_REQUIRED', 'PUBLIC_SOURCE_URL_REQUIRED', 'BROWSER_RELEASE_REQUIRED', 'EMPLOYEE_BINDING_REQUIRED'} <= codes
        saved = service.browser_scope('root', ['example.org'])
        assert saved['hosts'] == ['example.org'] and not saved['ready']
        calls = []
        async def execute(request):
            calls.append(request)
            raise AssertionError('preflight must precede Provider submission')
        app = FastAPI()
        app.include_router(build_team_operating_router(db, employee_execution=execute))
        with TestClient(app) as client:
            result = client.post('/team-operating/works/root/execute')
            assert result.status_code == 200, result.text
            assert result.json()['delegation_status'] == 'BLOCKED'
            assert not result.json()['market_evidence_readiness']['ready']
        assert calls == [] and not f.get('root')['data']['responsibilityRouting']['executions']
        assert f.get('root')['data']['marketEvidenceBrowser']['hosts'] == ['example.org']


@pytest.mark.parametrize('case', ['member', 'started', 'invalid_host', 'foreign_owner'])
def test_browser_scope_cannot_grant_permission_or_rewrite_started_work(tmp_path, monkeypatch, case):
    with scope():
        db, f, _ = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        if case == 'started':
            replace_data(db, 'root', lambda d: d['responsibilityRouting'].update(executions={'old': {'status': 'FAILED'}}))
        identity = {'role': 'member'} if case == 'member' else {'ceo_id': 'foreign'} if case == 'foreign_owner' else {}
        with scope(**identity), pytest.raises((ValueError, PermissionError)):
            service.browser_scope('root', ['localhost'] if case == 'invalid_host' else ['example.org'])
        assert 'marketEvidenceBrowser' not in f.get('root')['data']


@pytest.mark.parametrize('change', ['missing', 'stale', 'days', 'duplicate', 'identical', 'user_required'])
def test_recommendation_requires_actual_complete_body(change):
    from app.music_market_evidence import validate_research_recommendation
    inputs = [{'evidence_ref': 'fixture', 'evidence_version': 'a' * 64}]
    output = {'status': 'ACCEPTED', 'recommendation': recommendation_fixture(inputs)}
    if change == 'missing': output.pop('recommendation')
    elif change == 'stale': output['recommendation']['evidence'] = [{'evidence_ref': 'old', 'evidence_version': 'b' * 64}]
    elif change == 'days': output['recommendation']['seven_day_test']['days'] = 8
    elif change == 'duplicate': output['recommendation']['seven_day_test']['steps'] = ['same', 'same']
    elif change == 'identical': output['recommendation']['streaming_preview'] = output['recommendation']['short_video']
    else: output['status'] = 'USER_REQUIRED'
    with pytest.raises(ValueError): validate_research_recommendation(output, inputs)

def researcher_permission(service, assignment_ref, *, enabled=True):
    state = service.readiness("root")
    return MarketBrowserPermissionIn(assignment_ref=assignment_ref, employee_ref="company-worker",
        expected_revision=state["browser_permission_revision"], enabled=enabled)


@pytest.mark.parametrize("case", ["member", "foreign_owner", "foreign_company", "foreign_tenant",
    "leader", "not_research", "wrong_employee", "unknown_assignment", "stale_assignment", "child", "forged_origin"])
def test_browser_permission_rejects_ineligible_change(tmp_path, monkeypatch, case):
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        service.browser_scope("root", ["example.org"], "https://example.org/report")
        worker_ref = assignments[1]["entity_id"]
        request = researcher_permission(service, worker_ref).model_dump()
        target = "root"
        if case == "leader":
            request.update(assignment_ref=assignments[0]["entity_id"], employee_ref="leader")
        elif case == "wrong_employee":
            request["employee_ref"] = "leader"
        elif case == "unknown_assignment":
            request["assignment_ref"] = "not-in-workflow"
        elif case == "stale_assignment":
            replace_data(db, worker_ref, lambda d: d.update(revision=d["revision"] + 1))
        elif case == "not_research":
            workflow = f.get("root")["data"]["responsibilityRouting"]["workflowRef"]
            output = {"resultType": "song-plan"}
            replace_data(db, worker_ref, lambda d: d.update(outputContract=output))
            replace_data(db, workflow, lambda d: d["assignments"][1].update(outputContract=output))
            assert service.readiness("root")["browser_permissions"] == []
        elif case == "child":
            target = "child"
        elif case == "forged_origin":
            with db.connect() as con:
                con.execute("delete from evolution_events where event_type='conversation.research_work.confirmed'")
        identity = {"member": {"role": "member"}, "foreign_owner": {"ceo_id": "foreign"},
            "foreign_company": {"company_id": "foreign"}, "foreign_tenant": {"tenant_id": "foreign"}}.get(case, {})
        before = f.get("root")["data"]["marketEvidenceBrowserPermissions"]
        with scope(**identity), pytest.raises((KeyError, ValueError, PermissionError)):
            MusicMarketEvidence(db).browser_permission(target, MarketBrowserPermissionIn(**request))
        assert f.get("root")["data"]["marketEvidenceBrowserPermissions"] == before


def test_owner_public_permission_api_grants_revokes_and_changes_source_without_replay(tmp_path, monkeypatch):
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        service.browser_scope("root", ["example.org"], "https://example.org/report")
        worker_ref = assignments[1]["entity_id"]
        request = researcher_permission(service, worker_ref).model_dump()
        app = FastAPI()
        app.include_router(build_team_operating_router(db))
        with TestClient(app) as client:
            endpoint = "/team-operating/works/root/market-evidence/browser-permission"
            for invalid in [{"enabled": "true"}, {"expected_revision": True}, {"hosts": ["example.org"]}]:
                assert client.post(endpoint, json={**request, **invalid}).status_code == 422
            granted = client.post(endpoint, json=request)
            assert granted.status_code == 200, granted.text
            assert granted.json() == {"work_ref": "root", "assignment_ref": worker_ref,
                "employee_ref": "company-worker", "revision": request["expected_revision"] + 1, "enabled": True}
            assert service.readiness("root")["browser_permissions"][0]["can_revoke"]
            assert client.post(endpoint, json=request).status_code == 422
            service.browser_scope("root", ["example.org"], "https://example.org/another-report")
            service.browser_scope("root", ["example.org"], "https://example.org/report")
            assert not service.readiness("root")["browser_permissions"][0]["enabled"]
            grant = researcher_permission(service, worker_ref)
            assert client.post(endpoint, json=grant.model_dump()).status_code == 200
            replace_data(db, "root", lambda d: d["responsibilityRouting"].update(executions={"started": {"status": "RUNNING"}}))
            revoke = researcher_permission(service, worker_ref, enabled=False)
            assert client.post(endpoint, json=revoke.model_dump()).status_code == 200
            assert not service.readiness("root")["browser_permissions"][0]["enabled"]
            assert client.post(endpoint, json=grant.model_dump()).status_code == 422
            assert client.post(endpoint, json=researcher_permission(service, worker_ref).model_dump()).status_code == 422


def test_readiness_uses_existing_model_and_position_permissions(tmp_path, monkeypatch):
    from app import agent_browser_runtime
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        service.browser_scope('root', ['example.org'], 'https://example.org/report')
        with db.connect() as con:
            con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('worker-model',?,'company-worker','tenant_private','model','model.fixture')", (TENANT,))
            con.execute("update employee_instances set allowed_effect_classes_json='[\"read\"]' where id in ('leader','company-worker')")
        monkeypatch.setattr(agent_browser_runtime, 'agent_browser_release', lambda **kw: {'releaseSha256': 'a' * 64})
        assert "PUBLIC_WEB_PERMISSION_REQUIRED" in {x["code"] for x in service.readiness("root")["blockers"]}
        service.browser_permission("root", researcher_permission(service, assignments[1]["entity_id"]))
        result = service.readiness('root')
        assert result['ready'], result
        assert result['source_url'] == 'https://example.org/report'
        with db.connect() as con:
            con.execute("update employee_instances set allowed_effect_classes_json='[\"exec\"]' where id='company-worker'")
        codes = {x['code'] for x in service.readiness('root')['blockers']}
        assert 'POSITION_PERMISSION_REQUIRED' in codes
        assert 'PUBLIC_WEB_PERMISSION_REQUIRED' not in codes


def test_original_entry_delegates_configured_hosts_to_worker(tmp_path, monkeypatch):
    with scope():
        db, f, assignments = unstarted_leader(tmp_path, monkeypatch)
        MusicMarketEvidence(db).browser_scope('root', ['example.org'])
        db.save_tenant_private_capability(tenant_id=TENANT, capability_type='agent', capability_id='agent.fixture',
            display_name='Offline fixture', metadata={'kind': 'codex-cli'})
        with db.connect() as con:
            con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) values ('worker-agent',?,'company-worker','tenant_private','agent','agent.fixture')", (TENANT,))
        # The release-positive branch is simulated only here; no browser or Provider is started.
        monkeypatch.setattr(MusicMarketEvidence, 'readiness', lambda self, ref: {'work_ref': ref, 'ready': True, 'blockers': []})
        calls = []
        async def execute(request):
            calls.append(request)
            worker = request['runtime_employee_ref'] == 'worker'
            store = ResultStore(db)
            if request['mode'] == 'submit':
                if worker:
                    contract = f.get(request['work_ref'])['data']['followupContract']
                    assert contract['agentBrowser']['hosts'] == ['example.org']
                    assert contract['agentBinding']['bindingRef'] == 'worker-agent'
                    assert contract['agentSource']['snapshot']['context']['assignment_ref'] == assignments[1]['entity_id']
                task = store.create_task(request['prompt'], company_id=COMPANY, scope_type='BUSINESS', scope_ref=BUSINESS,
                    work_ref=request['work_ref'], execution_ref=request['execution_key'], employee_id='company-worker' if worker else 'leader')
                return {'task_ref': task['task_id']}
            value = {'status': 'ACCEPTED', 'resultType': 'market-summary', 'summary': 'Synthetic bounded output'}
            if not worker:
                value['delegations'] = [{'assignmentRef': assignments[1]['entity_id'], 'problem': 'Read public source', 'expectedResult': 'Preserve source'}]
            output = json.dumps(value)
            store.transition(request['task_ref'], 'COMPLETED', {'output': output})
            return {'task_ref': request['task_ref'], 'task_status': 'COMPLETED', 'output': output, 'session_ref': 'fixture',
                'execution_binding': {'callbackProvenance': {'verification_status': 'VERIFIED', 'callback_actor_ref': 'worker' if worker else 'leader'}}}
        app = FastAPI()
        app.include_router(build_team_operating_router(db, employee_execution=execute))
        with TestClient(app) as client:
            response = client.post('/team-operating/works/root/execute')
            assert response.status_code == 200, response.text
            assert response.json()['delegation_status'] == 'AWAITING_MARKET_EVIDENCE_ACCEPTANCE', response.text
        assert len(calls) == 4
        assert 'summaryWorkRef' not in f.get('root')['data']['leaderDelegation']


@pytest.mark.parametrize('suffix', ['#', '#section', '%23'])
def test_original_source_url_rejects_raw_fragment_but_preserves_encoding(tmp_path, monkeypatch, suffix):
    with scope():
        db, f, _ = unstarted_leader(tmp_path, monkeypatch)
        service = MusicMarketEvidence(db)
        url = 'https://example.org/report' + suffix
        if '#' in suffix:
            with pytest.raises(ValueError, match='片段'):
                service.browser_scope('root', ['example.org'], url)
            assert 'marketEvidenceBrowser' not in f.get('root')['data']
        else:
            assert service.browser_scope('root', ['example.org'], url)['source_url'] == url
