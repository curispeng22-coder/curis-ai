"""C02 source-only Result response tests; fixture callbacks are not Provider evidence."""
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.frontend_v1_router import build_frontend_v1_router
from app.database import Database
from app.result_attention import ResultAttention
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import seed, add_team, TENANT, COMPANY, WORKSPACE, EMPLOYEE


def scope(**overrides):
    return TenantContext.scope(**{"tenant_id": TENANT, "company_id": COMPANY, "ceo_id": "ceo", "role": "ceo", **overrides})


def source(path):
    db = seed(path)
    add_team(db)
    with scope():
        work = GeneralWorkspaceDelivery(db).create_work(company_id=COMPANY, workspace_id=WORKSPACE,
            problem="整理反馈", expected_result="形成建议", constraints=[], references=[],
            idempotency_key="c02-result-work")["work"]
        work_ref = work["entity_id"]
        routing = work["data"]["responsibilityRouting"]
        assignment = routing["currentAssignmentRef"]
        key = f"responsibility:{work_ref}:{assignment}:1"
        engine = ResponsibilityRoutingRuntime(db)
        engine.begin_employee_execution(work_ref, execution_key=key, assignment_ref=assignment)
        task = ResultStore(db).create_task("整理反馈", company_id=COMPANY, workspace_id=WORKSPACE,
            work_ref=work_ref, execution_ref=key, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            capability_source="tenant_private", capability_type="agent",
            capability_id="agent.general.local", employee_id=EMPLOYEE)
        engine.attach_provider_task(work_ref, execution_key=key, task_ref=task["task_id"])
        ResultStore(db).transition(task["task_id"], "COMPLETED", {"output": "一份可读的结果"})
        provenance = {"verification_status": "VERIFIED", "task_ref": task["task_id"],
            "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE}
        engine.finish_employee_execution(work_ref, execution_key=key, status="ACCEPTED",
            task_ref=task["task_id"], session_ref="fixture-session", result_ref="task:" + task["task_id"],
            result_summary="已整理", provenance=provenance)
    return db, work_ref, "task:" + task["task_id"]


def payload(work, result, action="ACCEPT", request=None):
    return {"workspace_id": WORKSPACE, "result_ref": result["reference_id"],
        "result_version": result["result_version"], "source_work_ref": work,
        "action": action, "reason": "已核对原结果", "request_id": request or str(uuid4())}


def app(db):
    value = FastAPI()
    @value.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo"), role=request.headers.get("X-Role", "ceo")):
            return await call_next(request)
    value.include_router(build_frontend_v1_router(db))
    return value


def test_response_is_append_only_scoped_replay_and_cold_read(tmp_path):
    db, work, ref = source(tmp_path / "response.sqlite")
    with scope():
        attention = ResultAttention(db)
        detail = attention.detail(COMPANY, WORKSPACE, ref)
        assert detail["response_eligibility"]["status"] == "ELIGIBLE"
        original_work = RuntimeFoundation(db).get(work)
        original_task = ResultStore(db).get_task(ref[5:])
        request = payload(work, detail)
        first = attention.decide_response(COMPANY, workspace_id=WORKSPACE,
            result_ref=ref, result_version_value=request["result_version"],
            source_work_ref=work, action=request["action"], reason=request["reason"], request_id=request["request_id"])
        assert first["action"] == "ACCEPT" and not first["replayed"]
        assert attention.decide_response(COMPANY, workspace_id=WORKSPACE,
            result_ref=ref, result_version_value=request["result_version"],
            source_work_ref=work, action=request["action"], reason=request["reason"], request_id=request["request_id"])["replayed"]
        assert RuntimeFoundation(db).get(work) == original_work
        assert ResultStore(db).get_task(ref[5:]) == original_task
    with scope():
        cold = ResultAttention(Database(str(tmp_path / "response.sqlite"))).detail(COMPANY, WORKSPACE, ref)
        assert cold["user_response"]["receipt_ref"] == first["receipt_ref"]
        assert cold["result_version"] == detail["result_version"]
        with pytest.raises(ValueError):
            ResultAttention(db).decide_response(COMPANY, workspace_id=WORKSPACE,
                result_ref=ref, result_version_value=request["result_version"], source_work_ref=work,
                action="REJECT", reason="不同决定", request_id=str(uuid4()))
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='result.response'").fetchone()[0] == 1
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_response_rejects_legacy_task_wrong_actor_and_bad_shape(tmp_path):
    db, work, ref = source(tmp_path / "denied.sqlite")
    with scope():
        detail = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)
    with TestClient(app(db)) as client:
        url = f"/api/workspace/v1/companies/{COMPANY}/result-response"
        good = payload(work, detail)
        assert client.post(url, json={**good, "reason": " "}).status_code == 422
        assert client.post(url, json={**good, "result_version": "x"}).status_code == 422
        assert client.post(url, json={**good, "action": "APPROVE"}).status_code == 422
        assert client.post(url, json={**good, "request_id": "not-a-uuid"}).status_code == 422
        assert client.post(url, json={**good, "source_work_ref": "wrong"}).status_code == 404
        assert client.post(url, json=good, headers={"X-CEO": "other"}).status_code == 404
        assert client.post(url, json=good, headers={"X-Role": "employee"}).status_code == 404
        assert client.post(url, json={**good, "result_version": "0" * 64}).status_code == 409
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='result.response'").fetchone()[0] == 0


def test_opposing_concurrent_choice_one_winner(tmp_path):
    db, work, ref = source(tmp_path / "race.sqlite")
    with scope():
        result = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)
    def decide(action):
        with scope():
            try:
                ResultAttention(db).decide_response(COMPANY, workspace_id=WORKSPACE,
                    result_ref=ref, result_version_value=result["result_version"], source_work_ref=work,
                    action=action, reason="并发决定", request_id=str(uuid4()))
                return "saved"
            except ValueError:
                return "conflict"
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(decide, ("ACCEPT", "REJECT"))) == ["conflict", "saved"]
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='result.response'").fetchone()[0] == 1


@pytest.mark.parametrize("mutation", ["professional", "foreign_task_scope", "missing_execution", "malformed_work", "foreign_work_scope",
    "result_refs_string", "human_input_false", "copied_task_claim"])
def test_generic_response_rejects_foreign_or_malformed_canonical_source(tmp_path, mutation):
    db, work, ref = source(tmp_path / f"{mutation}.sqlite")
    with scope():
        original = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)
    with db.connect() as con:
        if mutation == "professional":
            con.execute("update workspaces set blueprint_json=? where workspace_id=?", ('{"productForm":"CONTENT_GROWTH"}', WORKSPACE))
        elif mutation == "foreign_task_scope":
            con.execute("update tasks set scope_ref=? where task_id=?", ("foreign", ref[5:]))
        elif mutation == "missing_execution":
            con.execute("update tasks set execution_ref=? where task_id=?", ("forged", ref[5:]))
        else:
            row = con.execute("select data_json from runtime_entities where entity_id=?", (work,)).fetchone()
            if mutation == "malformed_work":
                con.execute("update runtime_entities set data_json=? where entity_id=?", ("null", work))
            else:
                value = __import__("json").loads(row["data_json"])
                routing = value["responsibilityRouting"]
                if mutation == "result_refs_string":
                    routing["resultRefs"] = ref
                elif mutation == "human_input_false":
                    routing["humanInput"] = False
                elif mutation == "copied_task_claim":
                    old_key = con.execute("select execution_ref from tasks where task_id=?", (ref[5:],)).fetchone()["execution_ref"]
                    copied_key = "copied-claim"
                    routing["executions"][copied_key] = {**routing["executions"][old_key], "executionKey": copied_key}
                    con.execute("update tasks set execution_ref=? where task_id=?", (copied_key, ref[5:]))
                else:
                    routing["scopeRef"] = "foreign"
                con.execute("update runtime_entities set data_json=? where entity_id=?", (__import__("json").dumps(value), work))
    with scope():
        detail = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)
        assert detail["response_eligibility"]["status"] == "INELIGIBLE"
        with pytest.raises((ValueError, RuntimeScopeError)):
            ResultAttention(db).decide_response(COMPANY, workspace_id=WORKSPACE,
                result_ref=ref, result_version_value=original["result_version"], source_work_ref=work,
                action="ACCEPT", reason="已核对", request_id=str(uuid4()))
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='result.response'").fetchone()[0] == 0


def test_stored_result_response_requires_original_correlation_and_payload(tmp_path):
    db, work, ref = source(tmp_path / "receipt.sqlite")
    with scope():
        result = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)
        request = payload(work, result)
        ResultAttention(db).decide_response(COMPANY, workspace_id=WORKSPACE,
            result_ref=ref, result_version_value=request["result_version"], source_work_ref=work,
            action=request["action"], reason=request["reason"], request_id=request["request_id"])
    with db.connect() as con:
        row = con.execute("select event_id,payload from evolution_events where event_type='result.response'").fetchone()
        value = __import__("json").loads(row["payload"])
        value["result_ref"] = "task:foreign"
        con.execute("update evolution_events set payload=? where event_id=?", (__import__("json").dumps(value), row["event_id"]))
    with scope():
        assert ResultAttention(db).detail(COMPANY, WORKSPACE, ref)["response_eligibility"]["status"] == "INELIGIBLE"
        with pytest.raises(ValueError):
            ResultAttention(db).decide_response(COMPANY, workspace_id=WORKSPACE,
                result_ref=ref, result_version_value=request["result_version"], source_work_ref=work,
                action=request["action"], reason=request["reason"], request_id=request["request_id"])
