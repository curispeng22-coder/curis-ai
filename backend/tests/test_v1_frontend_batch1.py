from __future__ import annotations

from fastapi.testclient import TestClient
from fastapi import FastAPI, Request

from app.api.frontend_v1_router import build_frontend_v1_router
from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext


TENANT = "tenant-v1-frontend-batch1"
CEO = "ceo-v1-frontend-batch1"
COMPANY = "company-v1-frontend-batch1"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO, "X-Role": "ceo"}


def confirmed_run(client: TestClient, intent_ref: str) -> dict:
    current = client.post(
        "/api/workspace/runtime/foundation/founding-runs",
        headers=HEADERS,
        json={"owner_ref": CEO, "intent_ref": intent_ref, "org_version": "org-v1"},
    ).json()
    for target, trigger in (
        ("INTENT_CAPTURED", "capture_intent"),
        ("CLARIFYING", "request_clarification"),
        ("PROPOSED", "propose_company"),
        ("CEO_CONFIRMED", "confirm_company"),
    ):
        response = client.post(
            f"/api/workspace/runtime/foundation/entities/{current['entity_id']}/transition",
            headers=HEADERS,
            json={"target": target, "actor": "CEO", "trigger": trigger, "reason": "v1 test"},
        )
        assert response.status_code == 200, response.text
        current = response.json()
    return current


def test_presentation_company_business_attention_and_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "v1-frontend.sqlite"
    with TestClient(create_app(str(path))) as client:
        presentation = client.put(
            "/api/workspace/v1/presentation", headers=HEADERS,
            json={"welcome_dismissed": True, "display_name": "一鸣", "avatar_ref": "preset:iris"},
        )
        assert presentation.status_code == 200
        assert client.get("/api/workspace/v1/presentation", headers=HEADERS).json()["display_name"] == "一鸣"
        assert client.get(
            "/api/workspace/runtime/foundation/companies", headers=HEADERS,
        ).json()["companies"] == []

        company_run = confirmed_run(client, "company-setup")
        created_company = client.post(
            f"/api/workspace/runtime/foundation/founding-runs/{company_run['entity_id']}/materialize-company",
            headers=HEADERS,
            json={"company_id": COMPANY, "ceo_id": CEO, "name": "山海科技"},
        )
        assert created_company.status_code == 200, created_company.text
        assert created_company.json()["assistant"]["entity_type"] == "CEO_ASSISTANT"
        assert created_company.json()["workspaces"] == []

        business_run = confirmed_run(client, "first-business")
        draft = {
            "intent": "为独立创作者提供内容增长服务",
            "business_name": "内容增长服务",
            "goal": "获得第一个可验证客户结果",
            "positioning": "服务独立创作者",
            "workspace_name": "内容增长工作空间",
        }
        saved = client.put(
            f"/api/workspace/v1/founding-runs/{business_run['entity_id']}/business-draft",
            headers=HEADERS, json=draft,
        )
        assert saved.status_code == 200
        assert saved.json()["data"]["v1Proposal"]["goal"] == draft["goal"]
        created = client.post(
            f"/api/workspace/v1/companies/{COMPANY}/founding-runs/{business_run['entity_id']}/business",
            headers=HEADERS,
            json={"ceo_id": CEO, **{key: draft[key] for key in ("business_name", "goal", "positioning", "workspace_name")}, "intent_summary": draft["intent"]},
        )
        assert created.status_code == 200, created.text
        body = created.json()
        assert body["business"]["definition"]["goal"] == draft["goal"]
        assert body["parent"]["parentPath"]["company"]["company_id"] == COMPANY
        assert len(body["business"]["workspaces"]) == 1

        same = client.post(
            f"/api/workspace/v1/companies/{COMPANY}/founding-runs/{business_run['entity_id']}/business",
            headers=HEADERS,
            json={"ceo_id": CEO, **{key: draft[key] for key in ("business_name", "goal", "positioning", "workspace_name")}, "intent_summary": draft["intent"]},
        )
        assert same.status_code == 200
        assert same.json()["creation_result"]["business_id"] == body["creation_result"]["business_id"]

        attention = client.get(f"/api/workspace/v1/companies/{COMPANY}/attention", headers=HEADERS)
        assert attention.status_code == 200
        assert attention.json()["workspace_count"] == 1
        assert attention.json()["state"] == "QUIET"

    with TestClient(create_app(str(path))) as restarted:
        assert restarted.get("/api/workspace/v1/presentation", headers=HEADERS).json()["welcome_dismissed"] is True
        businesses = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/businesses", headers=HEADERS,
        ).json()["businesses"]
        assert len(businesses) == 1
        assert businesses[0]["workspaces"][0]["name"] == "内容增长工作空间"


def test_attention_is_reference_first_and_cross_company_fails_closed(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "attention.sqlite"
    with TestClient(create_app(str(path))) as client:
        company_run = confirmed_run(client, "company")
        assert client.post(
            f"/api/workspace/runtime/foundation/founding-runs/{company_run['entity_id']}/materialize-company",
            headers=HEADERS, json={"company_id": COMPANY, "ceo_id": CEO, "name": "山海科技"},
        ).status_code == 200
        # Runtime projection returns canonical references and explicit unknown fields,
        # not copied Decision/Result payloads.
        payload = client.get(f"/api/workspace/v1/companies/{COMPANY}/attention", headers=HEADERS).json()
        assert payload["unavailable"] == ["company_importance_scoring", "predicted_return_time"]
        denied = client.get("/api/workspace/v1/companies/company-other/attention", headers=HEADERS)
        assert denied.status_code == 404


def test_ceo_assistant_real_submit_persists_on_canonical_assistant(tmp_path) -> None:
    path = tmp_path / "assistant-conversation.sqlite"
    database = Database(str(path)); database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, '山海科技')",
            (COMPANY, TENANT, CEO),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        assistant = RuntimeFoundation(database).create(
            "CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO, data={"name": "小澄"},
        )
    calls = []

    def model_call(prompt, model_key):
        calls.append((prompt, model_key))
        return {"output": "当前公司事实已读取；未知指标仍标记为未知。", "provider": "deepseek", "model": "deepseek-chat"}

    def app_for(current):
        value = FastAPI()

        @value.middleware("http")
        async def scope(request: Request, call_next):
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
                return await call_next(request)

        value.include_router(build_frontend_v1_router(current, model_call))
        return value

    with TestClient(app_for(database)) as client:
        sent = client.post(
            f"/api/workspace/v1/companies/{COMPANY}/assistant/conversation",
            json={"message": "今天最重要的事情是什么？", "model_key": "model.deepseek"},
        )
    assert sent.status_code == 200, sent.text
    assert sent.json()["assistant_id"] == assistant["entity_id"]
    assert [item["role"] for item in sent.json()["messages"]] == ["user", "assistant"]
    assert calls and "今天最重要的事情是什么" in calls[0][0]
    with TestClient(app_for(Database(str(path)))) as client:
        recovered = client.get(f"/api/workspace/v1/companies/{COMPANY}/assistant/conversation")
    assert recovered.status_code == 200
    assert len(recovered.json()["messages"]) == 2
    assert recovered.json()["assistant"]["name"] == "小澄"


def test_work_attention_risk_quiet_terminal_and_p7_original_scope(tmp_path):
    from backend.tests.test_v1_general_operating_contract import seed, add_team, app, COMPANY as C, WORKSPACE as W, TENANT as T
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    database = seed(tmp_path / "work-attention.sqlite")
    add_team(database)
    with TenantContext.scope(T, company_id=C, ceo_id="ceo", role="test"):
        service = GeneralWorkspaceDelivery(database)
        work = service.create_work(company_id=C, workspace_id=W, problem="TEST_ONLY original problem", expected_result="manual control",
                                   constraints=[], references=[], idempotency_key="attention")["work"]
    ref = work["entity_id"]
    with TestClient(app(database)) as client:
        path = f"/api/workspace/v1/companies/{C}/attention"
        assert not any(x["source_ref"] == ref for x in client.get(path).json()["items"])
        with TenantContext.scope(T, company_id=C, ceo_id="ceo", role="test"):
            child = CanonicalChildWorkRuntime(database)
            child.transition_work(ref, "BLOCKED", actor="SYSTEM", reason="TEST_ONLY local evidence missing")
        item = next(x for x in client.get(path).json()["items"] if x["source_ref"] == ref)
        assert item["status"] == "BLOCKED" and item["rank"] == 2
        assert item["summary"] == "TEST_ONLY original problem"
        assert item["reason"] == "TEST_ONLY local evidence missing"
        assert item["work_ref"] == ref and item["workspace_id"] == W
        assert item["owner_name"] == "小策"
        with TenantContext.scope(T, company_id=C, ceo_id="ceo", role="test"):
            child.transition_work(ref, "ACTIVE", actor="SYSTEM")
            packet = ResponsibilityRoutingRuntime(database).route(ref, signal="DECISION_GATE", problem="TEST_ONLY operator decision")["decision"]
        items = client.get(path).json()["items"]
        assert not any(x["source_ref"] == ref for x in items)
        decision = next(x for x in items if x["source_ref"] == packet["entity_id"])
        assert decision["work_ref"] == ref
        with TenantContext.scope(T, company_id=C, ceo_id="ceo", role="test"):
            service.control_work(company_id=C, workspace_id=W, work_ref=ref, action="cancel", reason="operator stops")
        assert not any(x["source_ref"] == ref for x in client.get(path).json()["items"])
        assert client.get("/api/workspace/v1/companies/foreign/attention").status_code == 404


def test_attention_never_reads_a_cycle_or_transition_from_another_scope(tmp_path):
    from backend.tests.test_v1_general_operating_contract import seed, add_team, app, COMPANY as C, WORKSPACE as W, TENANT as T
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from app.runtime.child_work import CanonicalChildWorkRuntime
    database = seed(tmp_path / "attention-corrupt-parent.sqlite")
    add_team(database)
    with TenantContext.scope(T, company_id=C, ceo_id="ceo", role="test"):
        work = GeneralWorkspaceDelivery(database).create_work(company_id=C, workspace_id=W, problem="FOREIGN CONTRACT MUST NOT LEAK", expected_result="test",
                    constraints=[], references=[], idempotency_key="parent-scope")["work"]
        CanonicalChildWorkRuntime(database).transition_work(work["entity_id"], "FAILED", actor="SYSTEM", reason="local reason")
    with database.connect() as connection:
        connection.execute("update runtime_entities set workspace_id='other-ws' where entity_id=?", (work["parent_id"],))
        connection.execute("insert into runtime_transition_log(tenant_id,entity_type,entity_id,source,target,trigger,actor,at,reason,company_id,workspace_id) "
                           "values (?,'work',?,'ACTIVE','FAILED','test','SYSTEM','2099','FOREIGN REASON',?,'other-ws')", (T,work["entity_id"],C))
    with TestClient(app(database)) as client:
        item = next(x for x in client.get(f"/api/workspace/v1/companies/{C}/attention").json()["items"] if x["source_ref"] == work["entity_id"])
        assert "FOREIGN" not in item["summary"] and item["reason"] == "local reason"
