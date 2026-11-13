"""Isolated contract tests, not external model/desktop evidence."""
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.frontend_v1_router import build_frontend_v1_router
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.result_attention import ResultAttention
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import seed, COMPANY, TENANT, WORKSPACE


def scope(**overrides):
    return TenantContext.scope(**{"tenant_id": TENANT, "company_id": COMPANY, "ceo_id": "ceo", "role": "ceo", **overrides})


def fixture(path):
    db = seed(path)
    with scope():
        task = ResultStore(db).create_task("客户反馈整理结果", company_id=COMPANY, workspace_id=WORKSPACE)
        ResultStore(db).transition(task["task_id"], "COMPLETED", {"output": "有一条反馈需要跟进"})
    return db, "task:" + task["task_id"]


def app(db):
    value = FastAPI()
    @value.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo"), role=request.headers.get("X-Role", "ceo")):
            return await call_next(request)
    value.include_router(build_frontend_v1_router(db))
    return value


def test_receipt_is_separate_durable_idempotent_and_versioned(tmp_path):
    path = tmp_path / "receipts.sqlite"
    db, ref = fixture(path)
    service = ResultAttention(db)
    with scope():
        original = ResultStore(db).get_task(ref[5:])
        detail = service.detail(COMPANY, WORKSPACE, ref)
        assert not detail["viewed"]
        assert len(service.unseen_results(COMPANY)) == 1
        assert EvolutionEventLog(db).get_all() == []  # GET/list never marks viewed.
        first = service.mark_viewed(COMPANY, WORKSPACE, ref, detail["result_version"])
        assert service.mark_viewed(COMPANY, WORKSPACE, ref, detail["result_version"]) == first
        assert service.unseen_results(COMPANY) == []
        assert ResultStore(db).get_task(ref[5:]) == original
    reopened = ResultAttention(Database(str(path)))
    with scope():
        assert reopened.detail(COMPANY, WORKSPACE, ref)["viewed"]
        assert reopened.unseen_results(COMPANY) == []
        # Existing ResultStore revision creates a different content identity.
        ResultStore(db).transition(ref[5:], "COMPLETED", {"output": "新增反馈及来源"})
        latest = reopened.detail(COMPANY, WORKSPACE, ref)
        assert latest["result_version"] != detail["result_version"]
        assert not latest["viewed"]
        assert len(reopened.unseen_results(COMPANY)) == 1
        with pytest.raises(ValueError, match="更新"):
            reopened.mark_viewed(COMPANY, WORKSPACE, ref, detail["result_version"])
    with db.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("select count(*) from evolution_events where event_type='result.viewed'").fetchone()[0] == 1
        assert connection.execute("select count(*) from runtime_entities where entity_type='ACCEPTANCE'").fetchone()[0] == 0


def test_concurrent_receipts_exactly_once(tmp_path):
    db, ref = fixture(tmp_path / "concurrent.sqlite")
    with scope():
        version = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)["result_version"]
    def mark(_):
        with scope():
            return ResultAttention(db).mark_viewed(COMPANY, WORKSPACE, ref, version)["receipt_ref"]
    with ThreadPoolExecutor(max_workers=6) as pool:
        assert len(set(pool.map(mark, range(12)))) == 1


@pytest.mark.parametrize("overrides", [{"tenant_id": "other"}, {"company_id": "other"}, {"ceo_id": "other"}, {"role": "employee"}])
def test_receipt_denies_identity_scope_conflicts(tmp_path, overrides):
    db, ref = fixture(tmp_path / "scope.sqlite")
    with scope():
        version = ResultAttention(db).detail(COMPANY, WORKSPACE, ref)["result_version"]
    with scope(**overrides), pytest.raises(RuntimeScopeError):
        ResultAttention(db).mark_viewed(COMPANY, WORKSPACE, ref, version)
    assert EvolutionEventLog(db).get_all() == []


def test_wrong_workspace_and_failed_detail_never_write(tmp_path):
    db, ref = fixture(tmp_path / "missing.sqlite")
    with TestClient(app(db)) as client:
        prefix = f"/api/workspace/v1/companies/{COMPANY}"
        assert client.get(prefix + "/result-detail", params={"workspace_id": "wrong", "result_ref": ref}).status_code == 404
        assert client.post(prefix + "/result-viewed", json={"workspace_id": WORKSPACE, "result_ref": ref, "result_version": "0" * 64}).status_code == 409
        assert client.post(prefix + "/result-viewed", json={"workspace_id": WORKSPACE, "result_ref": ref, "result_version": "invalid"}).status_code == 422
    assert EvolutionEventLog(db).get_all() == []


def test_attention_terminal_decision_is_not_a_viewed_receipt(tmp_path):
    db, ref = fixture(tmp_path / "decision.sqlite")
    with scope():
        decision = RuntimeFoundation(db).create("DECISION_PACKET", company_id=COMPANY, workspace_id=WORKSPACE)
    # Projection fixtures isolate source lifecycle from P7 command regression.
    with db.connect() as connection:
        connection.execute("update runtime_entities set lifecycle_status='WAITING_CEO' where entity_id=?", (decision["entity_id"],))
    with TestClient(app(db)) as client:
        prefix = f"/api/workspace/v1/companies/{COMPANY}"
        items = client.get(prefix + "/attention").json()["items"]
        assert {x["source_ref"] for x in items} == {ref, decision["entity_id"]}
        detail = client.get(prefix + "/result-detail", params={"workspace_id": WORKSPACE, "result_ref": ref}).json()
        assert client.post(prefix + "/result-viewed", json={"workspace_id": WORKSPACE, "result_ref": ref, "result_version": detail["result_version"]}).status_code == 200
        assert [x["source_ref"] for x in client.get(prefix + "/attention").json()["items"]] == [decision["entity_id"]]
        with db.connect() as connection:
            connection.execute("update runtime_entities set lifecycle_status='APPLIED' where entity_id=?", (decision["entity_id"],))
        assert client.get(prefix + "/attention").json()["items"] == []
        assert client.get(prefix + "/attention").json()["items"] == []
    events = EvolutionEventLog(db).get_all()
    assert len(events) == 1 and events[0]["event_type"] == "result.viewed"


def test_event_idempotency_cannot_cross_tenants(tmp_path):
    db, _ = fixture(tmp_path / "event-scope.sqlite")
    log = EvolutionEventLog(db)
    log.record(correlation_id="result", event_type="result.viewed", payload={}, tenant_id="a", idempotency_key="same")
    with pytest.raises(ValueError):
        log.record(correlation_id="result", event_type="result.viewed", payload={}, tenant_id="b", idempotency_key="same")


def test_selfuse_owner_is_ceo_and_failed_result_is_not_acceptance(tmp_path):
    db, ref = fixture(tmp_path / "owner.sqlite")
    with scope(role="owner"):
        ResultStore(db).transition(ref[5:], "FAILED", {"output": "人工测试失败记录，未产生成功结果"})
        service = ResultAttention(db)
        detail = service.detail(COMPANY, WORKSPACE, ref)
        service.mark_viewed(COMPANY, WORKSPACE, ref, detail["result_version"])
        assert ResultStore(db).get_task(ref[5:])["status"] == "FAILED"
        assert service.unseen_results(COMPANY) == []


def test_assistant_references_stay_scoped_reference_first_and_durable(tmp_path):
    path = tmp_path / "references.sqlite"
    db, ref = fixture(path)
    with scope():
        assistant = RuntimeFoundation(db).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref="ceo", data={"name": "小澄"})
    calls = []
    def model_call(prompt, model):
        calls.append(prompt)
        return {"output": "请从来源查看这份资料。", "provider": "unit-test-only", "model": "not-live"}
    value = app(db)
    # app() has no callback; use the same authenticated router with a bounded test double.
    value.router.routes = [route for route in value.router.routes if "/api/workspace/v1" not in getattr(route, "path", "")]
    value.include_router(build_frontend_v1_router(db, model_call))
    with TestClient(value) as client:
        url = f"/api/workspace/v1/companies/{COMPANY}/assistant/conversation"
        response = client.post(url, json={"message": "这是什么资料？", "references": [{"reference_id": ref, "workspace_id": WORKSPACE}]})
        assert response.status_code == 200, response.text
        messages = response.json()["messages"]
        assert messages[0]["references"][0]["reference_id"] == ref
        assert messages[0]["message_id"] != messages[1]["message_id"]
        assert "有一条反馈需要跟进" not in calls[0]  # No result body hydration.
        assert client.post(url, json={"message": "越界", "references": [{"reference_id": ref, "workspace_id": "other"}]}).status_code == 404
        assert len(calls) == 1
    with TestClient(app(Database(str(path)))) as client:
        persisted = client.get(url).json()
        assert persisted["assistant"]["assistant_id"] == assistant["entity_id"]
        assert persisted["messages"] == messages
    assert EvolutionEventLog(db).get_all() == []  # Quoting/listing a result is not viewing it.
