"""Owner/persistence checks only; never claimed as real provider acceptance."""
from concurrent.futures import ThreadPoolExecutor
import asyncio

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.api.conversation_router import build_conversation_router

from app.conversation_service import ConversationService
from app.database import Database
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.ai_usage import AIUsageService
from app.result_store import ResultStore
from app.evolution_event_log import EvolutionEventLog
from backend.tests.test_v1_general_operating_contract import seed, add_team, COMPANY, TENANT, EMPLOYEE, WORKSPACE


def scope(**overrides):
    return TenantContext.scope(**{"tenant_id": TENANT, "company_id": COMPANY, "ceo_id": "ceo", "role": "ceo", **overrides})


def setup(path):
    db = seed(path)
    add_team(db)
    with scope():
        assignment = RuntimeFoundation(db).list("RESPONSIBILITY_ASSIGNMENT", company_id=COMPANY)[0]
    return db, assignment["entity_id"]


def test_stable_owner_assignment_context_and_restart(tmp_path):
    path = tmp_path / "conversation.sqlite"
    db, assignment = setup(path)
    with scope():
        service = ConversationService(db)
        original = service.open(COMPANY, EMPLOYEE)
        first = service.append_ceo(COMPANY, EMPLOYEE, body="讨论目标，不建立工作", request_id="first", assignment_ref=assignment)
        ResponsibilityRoutingRuntime(db).update_assignment(assignment, responsibility="新的当前责任")
        second = service.append_ceo(COMPANY, EMPLOYEE, body="按当前责任继续", request_id="second", assignment_ref=assignment)
        assert first["context"]["responsibility"] != second["context"]["responsibility"]
        restored = ConversationService(Database(str(path))).read(COMPANY, EMPLOYEE)
        assert restored["conversation_id"] == original["conversation_id"]
        assert restored["messages"] == [first, second]
        assert first["sender"] == {"kind": "CEO", "ref": "ceo"}
        assert first["timestamp"] and first["message_id"] != second["message_id"]
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
        assert con.execute("select count(*) from tasks").fetchone()[0] == 0
        assert con.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_concurrent_append_idempotency_and_conflict(tmp_path):
    db, assignment = setup(tmp_path / "concurrent.sqlite")
    def append(_):
        with scope():
            return ConversationService(db).append_ceo(COMPANY, EMPLOYEE, body="同一消息", request_id="same", assignment_ref=assignment)
    with ThreadPoolExecutor(max_workers=6) as pool:
        messages = list(pool.map(append, range(12)))
    assert all(message == messages[0] for message in messages)
    with scope():
        service = ConversationService(db)
        assert len(service.read(COMPANY, EMPLOYEE)["messages"]) == 1
        with pytest.raises(ValueError, match="conflicts"):
            service.append_ceo(COMPANY, EMPLOYEE, body="不同消息", request_id="same", assignment_ref=assignment)


@pytest.mark.parametrize("other", [{"tenant_id": "other"}, {"company_id": "other"}, {"ceo_id": "other"}])
def test_owner_isolation(tmp_path, other):
    db, _ = setup(tmp_path / "scope.sqlite")
    with scope(**other), pytest.raises(RuntimeScopeError):
        ConversationService(db).open(COMPANY, EMPLOYEE)


def test_different_employee_and_reassigned_context(tmp_path):
    db, assignment = setup(tmp_path / "employees.sqlite")
    with scope():
        foundation = RuntimeFoundation(db)
        other = foundation.create("AI_EMPLOYEE", company_id=COMPANY, workspace_id=WORKSPACE, lifecycle_status="AVAILABLE")
        service = ConversationService(db)
        assert service.owner(COMPANY, EMPLOYEE)["conversation_id"] != service.owner(COMPANY, other["entity_id"])["conversation_id"]
        ResponsibilityRoutingRuntime(db).update_assignment(assignment, employee_ref=other["entity_id"])
        with pytest.raises(RuntimeScopeError):
            service.append_ceo(COMPANY, EMPLOYEE, body="不能再用旧责任", request_id="wrong", assignment_ref=assignment)


def test_failed_binding_bounded_retry_and_restart_no_replay(tmp_path):
    db, assignment = setup(tmp_path / "retry.sqlite")
    launched = []
    async def forbidden_executor(task_id):
        launched.append(task_id)
        raise AssertionError("An unbound Employee must never execute")
    with scope():
        service = ConversationService(db)
        args = dict(body="保留原输入", request_id="retry", assignment_ref=assignment)
        first, created = service.prepare(COMPANY, EMPLOYEE, **args)
        assert created
        assert not service.prepare(COMPANY, EMPLOYEE, **args)[1]
        restored = ConversationService(db)
        assert restored.read(COMPANY, EMPLOYEE)["attempts"][0]["status"] == "UNVERIFIED"
        with pytest.raises(ValueError):
            restored.prepare(COMPANY, EMPLOYEE, **args, retry_no=1)
        asyncio.run(service.execute(first, forbidden_executor))
        assert service.read(COMPANY, EMPLOYEE)["attempts"][0]["status"] == "FAILED"
        ResponsibilityRoutingRuntime(db).update_assignment(assignment, responsibility="更新后的合法责任")
        second, created = service.prepare(COMPANY, EMPLOYEE, **args, retry_no=1)
        assert created and second["context"] != first["context"]
        assert second["message_id"] == first["message_id"]
        assert not service.prepare(COMPANY, EMPLOYEE, **args, retry_no=1)[1]
        asyncio.run(service.execute(second, forbidden_executor))
        with pytest.raises(ValueError):
            service.prepare(COMPANY, EMPLOYEE, **args, retry_no=2)
        state = ConversationService(db).read(COMPANY, EMPLOYEE)
        assert len(state["messages"]) == 1 and len(state["attempts"]) == 2
        assert all(item["status"] == "FAILED" for item in state["attempts"])
        assert launched == []


def test_invalid_binding_blocks_before_provider_launch(tmp_path):
    """The real ledger, not only the Python resolver, must support this origin."""
    db, assignment = setup(tmp_path / "execution.sqlite")
    db.save_tenant_private_capability(tenant_id=TENANT, capability_type="model", capability_id="model.unit",
        display_name="Unit contract model", metadata={"testOnly": True})
    with db.connect() as con:
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
            "values ('binding-model',?,?,'tenant_private','model','model.unit')", (TENANT, EMPLOYEE))
    called = []
    with scope():
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE, employee_capability_binding_ref="binding-model")
        service = ConversationService(db)
        claim, created = service.prepare(COMPANY, EMPLOYEE, body="仅讨论目标", request_id="execute", assignment_ref=assignment)
        assert created
        with db.connect() as con:
            con.execute("update employee_capability_bindings set enabled=0 where id='binding-model'")
        async def executor(task_id):
            called.append(task_id)
            raise AssertionError("Unsupported accounting must prevent external execution")
        asyncio.run(service.execute(claim, executor))
        state = ConversationService(db).read(COMPANY, EMPLOYEE)
        assert called == []
        assert state["attempts"][0]["status"] == "FAILED"
        assert len(state["messages"]) == 1
        assert state["attempts"][0]["task_ref"] is None
        assert not service.prepare(COMPANY, EMPLOYEE, body="仅讨论目标", request_id="execute", assignment_ref=assignment)[1]
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='WORK'").fetchone()[0] == 0
        assert con.execute("select count(*) from projects").fetchone()[0] == 0
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0


def test_selected_result_reference_is_not_viewed_and_is_scoped(tmp_path):
    db, assignment = setup(tmp_path / "refs.sqlite")
    with scope():
        store = ResultStore(db)
        task = store.create_task("已选结果", company_id=COMPANY, workspace_id=WORKSPACE)
        store.transition(task["task_id"], "COMPLETED", {"output": "Evidence remains in ResultStore, not conversation"})
        ref = {"kind": "RESULT", "reference_id": "task:" + task["task_id"], "workspace_id": WORKSPACE}
        service = ConversationService(db)
        message = service.append_ceo(COMPANY, EMPLOYEE, body="讨论这个来源", request_id="refs", assignment_ref=assignment, references=[ref])
        assert message["references"][0]["reference_id"] == ref["reference_id"]
        assert "content" not in message["references"][0]
        with pytest.raises(RuntimeScopeError):
            service.append_ceo(COMPANY, EMPLOYEE, body="错误范围", request_id="bad", assignment_ref=assignment,
                references=[{**ref, "workspace_id": "other"}])
        with pytest.raises(RuntimeScopeError):
            service.append_ceo(COMPANY, EMPLOYEE, body="错误类型", request_id="bad-type", assignment_ref=assignment,
                references=[{**ref, "kind": "EVIDENCE"}])
        restored = ConversationService(db).read(COMPANY, EMPLOYEE)
        assert restored["messages"] == [message]
    with db.connect() as con:
        assert con.execute("select count(*) from evolution_events where event_type='result.viewed'").fetchone()[0] == 0


def test_api_scope_and_duplicate_send(tmp_path):
    db, assignment = setup(tmp_path / "api.sqlite")
    app = FastAPI()
    @app.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo")):
            return await call_next(request)
    async def forbidden(task_id):
        raise AssertionError("unbound Employee")
    app.include_router(build_conversation_router(db, forbidden))
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    payload = {"body": "保留消息", "request_id": "api", "assignment_ref": assignment}
    with TestClient(app) as client:
        assert client.get(prefix, headers={"X-CEO": "other"}).status_code == 404
        before = client.get(prefix).json()
        assert client.post(prefix + "/open").json()["conversation_id"] == before["conversation_id"]
        assert client.post(prefix + "/messages", json=payload).status_code == 202
        assert client.post(prefix + "/messages", json=payload).status_code == 202
        state = client.get(prefix).json()
        assert len(state["messages"]) == 1 and len(state["attempts"]) == 1
        assert state["attempts"][0]["status"] == "FAILED"
        assert client.post(prefix + "/messages", json={**payload, "retry_no": 2}).status_code == 422
        assert client.get(prefix + "/references", params={"assignment_ref": "wrong"}).status_code == 404


def _selection(binding_id, source, model_key, company=COMPANY, workspace=WORKSPACE):
    return {"purpose": "CONVERSATION_REPLY", "binding_id": binding_id,
            "scope": {"company_id": company, "workspace_id": workspace},
            "model": {"source": source, "model_key": model_key}}


def _bind_two_official_models(db):
    with db.connect() as con:
        con.execute("insert into official_models(model_key,provider_id,display_name,supported_models,gateway_ref,"
                    "status,default_model,type,name) values ('model.conv-a','controlled-provider','对话模型A',"
                    "'[\"contract-a\"]','conv-a-gateway','active','contract-a','model','A'),"
                    "('model.conv-b','controlled-provider','对话模型B','[\"contract-b\"]','conv-b-gateway',"
                    "'active','contract-b','model','B')")
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,"
                    "capability_type,capability_id,priority) values "
                    "('binding-a',?,'employee-v1-general','official','model','model.conv-a',10), "
                    "('binding-b',?,'employee-v1-general','official','model','model.conv-b',20)", (TENANT, TENANT))
    with scope():
        EmployeeExecutionIdentity(db).bind(company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE,
            employee_capability_binding_ref="binding-a")


def test_unbridged_employee_with_company_ref_reads_via_detail_entry(tmp_path):
    # Production-shape regression (QA Q-1 disposition): a runtime AI_EMPLOYEE always
    # carries companyEmployeeRef from instantiation, even before an identity bridge
    # exists. The employee-detail entry uses the company employee id and must resolve.
    import json as _json
    from datetime import datetime, timezone
    db, _ = setup(tmp_path / "unbridged-detail.sqlite")
    at = datetime.now(timezone.utc).isoformat()
    with db.connect() as con:
        con.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,"
                    "name,role,status) values (?,?,?,?,'et_product_manager','无桥员工','product_manager','idle')",
                    ("company-emp-unbridged", TENANT, COMPANY, "department"))
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,"
                    "owner_ref,lifecycle_status,verification_status,evidence_condition,data_json,created_at,updated_at) "
                    "values (?,?,?,?,?,'','AVAILABLE','UNVERIFIED','MISSING',?,?,?)",
                    ("rt-unbridged", TENANT, "AI_EMPLOYEE", COMPANY, WORKSPACE,
                     _json.dumps({"name": "无桥员工", "companyEmployeeRef": "company-emp-unbridged"}, ensure_ascii=False), at, at))
    app = FastAPI()
    @app.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo")):
            return await call_next(request)
    async def forbidden(task_id):
        raise AssertionError("must not execute")
    app.include_router(build_conversation_router(db, forbidden))
    with TestClient(app) as client:
        response = client.get(f"/api/workspace/v1/companies/{COMPANY}/employees/company-emp-unbridged/conversation",
                              headers={"X-CEO": "ceo"})
        assert response.status_code == 200
        value = response.json()
        assert value["owner_ref"] == "rt-unbridged"
        assert value["execution_models"] and all(model["binding_id"] is None for model in value["execution_models"])


def test_execution_models_lists_global_eligible_models_and_marks_existing_bindings(tmp_path):
    db, _ = setup(tmp_path / "models.sqlite")
    with scope():
        assert all(model["binding_id"] is None for model in ConversationService(db).execution_models(COMPANY, EMPLOYEE))
    _bind_two_official_models(db)
    with db.connect() as con:
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,"
                    "capability_type,capability_id) values "
                    "('binding-other',?,'someone-else','official','model','model.conv-a')", (TENANT,))
        con.execute("update employee_capability_bindings set enabled=0 where id='binding-b'")
    with scope():
        models = ConversationService(db).execution_models(COMPANY, EMPLOYEE)
    by_key = {model["model_key"]: model for model in models}
    assert by_key["model.conv-a"]["binding_id"] == "binding-a"
    assert by_key["model.conv-b"]["binding_id"] is None
    assert "binding-other" not in {model["binding_id"] for model in models}


def test_conversation_selection_idempotent_replay_rejects_model_swap(tmp_path):
    db, assignment = setup(tmp_path / "selection-swap.sqlite")
    _bind_two_official_models(db)
    with scope():
        service = ConversationService(db)
        claim, created = service.prepare(COMPANY, EMPLOYEE, body="指定模型A回复", request_id="pick-a",
            assignment_ref=assignment, execution_selection=_selection("binding-a", "official", "model.conv-a"))
        assert created and claim["execution_selection"]["source_class"] == "EMPLOYEE_BINDING"
        # Idempotent replay keeps the exact selection; swapping model on the same request is rejected.
        assert not service.prepare(COMPANY, EMPLOYEE, body="指定模型A回复", request_id="pick-a",
            assignment_ref=assignment, execution_selection=_selection("binding-a", "official", "model.conv-a"))[1]
        with pytest.raises(ValueError):
            service.prepare(COMPANY, EMPLOYEE, body="指定模型A回复", request_id="pick-a",
                assignment_ref=assignment, execution_selection=_selection("binding-b", "official", "model.conv-b"))


def test_conversation_selection_rejects_foreign_scope_and_disabled_binding(tmp_path):
    db, assignment = setup(tmp_path / "selection-deny.sqlite")
    _bind_two_official_models(db)
    with db.connect() as con:
        con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,"
                    "capability_type,capability_id) values "
                    "('binding-other',?,'someone-else','official','model','model.conv-a')", (TENANT,))
    with scope():
        service = ConversationService(db)
        with pytest.raises(ValueError):
            service.prepare(COMPANY, EMPLOYEE, body="别人的绑定", request_id="foreign",
                assignment_ref=assignment, execution_selection=_selection("binding-other", "official", "model.conv-a"))
        with pytest.raises(RuntimeScopeError):
            service.prepare(COMPANY, EMPLOYEE, body="跨公司范围", request_id="foreign-scope",
                assignment_ref=assignment, execution_selection=_selection("binding-a", "official", "model.conv-a", company="other"))
    with db.connect() as con:
        con.execute("update employee_capability_bindings set enabled=0 where id='binding-a'")
    with scope():
        with pytest.raises(ValueError):
            ConversationService(db).prepare(COMPANY, EMPLOYEE, body="绑定已停用", request_id="disabled",
                assignment_ref=assignment, execution_selection=_selection("binding-a", "official", "model.conv-a"))


def test_selected_conversation_reply_runs_real_binding_with_usage(tmp_path, monkeypatch):
    from dataclasses import replace
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.model_gateway import ModelGatewayAdapter
    from app.identity_membership import IdentityMembership
    db, assignment = setup(tmp_path / "selected-exec.sqlite")
    _bind_two_official_models(db)
    calls = []
    def post(url, payload, headers, timeout):
        calls.append(payload)
        return {"choices": [{"message": {"content": "这是员工基于模型A的回复。"}}],
                "usage": {"prompt_tokens": 9, "completion_tokens": 8, "total_tokens": 17}}
    adapter = ModelGatewayAdapter(base_url="https://provider.invalid", api_key="test-only",
        gateway_id="conv-a-gateway", model_name="contract-a", http_post=post)
    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test",
        lambda self, tenant, request: replace(original(self, tenant, request), role="ceo"))
    app = create_app(str(db.path), model_gateway_adapter=adapter)
    prefix = f"/api/workspace/v1/companies/{COMPANY}/employees/{EMPLOYEE}/conversation"
    headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
    payload = {"body": "请用绑定的模型回复", "request_id": "selected-1", "assignment_ref": assignment,
               "execution_selection": _selection("binding-a", "official", "model.conv-a")}
    with TestClient(app) as client:
        models = client.get(prefix, headers=headers).json()["execution_models"]
        assert {item["binding_id"] for item in models if item["binding_id"]} == {"binding-a", "binding-b"}
        assert client.post(prefix + "/messages", json=payload, headers=headers).status_code == 202
        assert len(calls) == 1
        state = client.get(prefix, headers=headers).json()
        assert state["attempts"][0]["status"] == "COMPLETED", state["attempts"]
        reply = state["messages"][-1]
        assert reply["body"] == "这是员工基于模型A的回复。"
        assert reply["provenance"]["execution_selection"]["binding_id"] == "binding-a"
        assert reply["provenance"]["source_class"] == "EMPLOYEE_BINDING"
        # Replaying with a different binding is a conflict; a malformed selection is a 422.
        assert client.post(prefix + "/messages", json={**payload,
            "execution_selection": _selection("binding-b", "official", "model.conv-b")},
            headers=headers).status_code == 409
        bad = {**payload, "request_id": "bad-shape",
               "execution_selection": {"purpose": "CONVERSATION_REPLY", "binding_id": "binding-a",
                   "scope": {"company_id": COMPANY, "workspace_id": WORKSPACE},
                   "model": {"source": "personal", "model_key": "model.conv-a"}}}
        assert client.post(prefix + "/messages", json=bad, headers=headers).status_code == 422
        mismatched = {**payload, "request_id": "source-mismatch",
                      "execution_selection": {"purpose": "CONVERSATION_REPLY", "binding_id": "binding-a",
                          "scope": {"company_id": COMPANY, "workspace_id": WORKSPACE},
                          "model": {"source": "tenant_private", "model_key": "model.conv-a"}}}
        assert client.post(prefix + "/messages", json=mismatched, headers=headers).status_code == 409
    with db.connect() as con:
        usage = con.execute("select * from ai_usage_records where capability_binding_id='binding-a'").fetchall()
        assert len(usage) == 1 and usage[0]["fallback_from_model"] is None


def test_topic_without_employee_rejects_execution_selection(tmp_path):
    db, assignment = setup(tmp_path / "topic-no-employee.sqlite")
    app = FastAPI()
    @app.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-CEO", "ceo")):
            return await call_next(request)
    async def forbidden(task_id):
        raise AssertionError("must not execute")
    app.include_router(build_conversation_router(db, forbidden))
    with TestClient(app) as client:
        created = client.post(f"/api/workspace/v1/companies/{COMPANY}/conversations",
            json={"request_id": "topic-only", "title": "无员工话题"}, headers={"X-CEO": "ceo"}).json()
        response = client.post(f"/api/workspace/v1/companies/{COMPANY}/conversations/{created['conversation_id']}/messages",
            json={"body": "只记录", "request_id": "topic-msg", "assignment_ref": "",
                  "execution_selection": _selection("binding-a", "official", "model.conv-a")},
            headers={"X-CEO": "ceo"})
        assert response.status_code == 409


def test_typed_work_decision_knowledge_refs_keep_scope_without_hydration(tmp_path):
    from app.knowledge_service import KnowledgeService
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    db, assignment = setup(tmp_path / "typed-references.sqlite")
    with scope():
        work = GeneralWorkspaceDelivery(db).create_work(company_id=COMPANY, workspace_id=WORKSPACE,
            problem="只验证引用", expected_result="引用保持", constraints=[], references=[], idempotency_key="ref-work")["work"]
        decision = RuntimeFoundation(db).create("DECISION_PACKET", company_id=COMPANY, workspace_id=WORKSPACE)
        knowledge = KnowledgeService(db).create_entry(title="已选择资料", body="DO_NOT_HYDRATE_THIS_BODY",
            company_id=COMPANY, target_type="WORKSPACE", target_ref=WORKSPACE)
        refs = [{"reference_id": obj, "workspace_id": WORKSPACE, "kind": kind} for kind, obj in [
            ("WORK", work["entity_id"]), ("DECISION_PACKET", decision["entity_id"]), ("KNOWLEDGE", knowledge["id"])]]
        service = ConversationService(db)
        original = service.open(COMPANY, EMPLOYEE)
        message = service.append_ceo(COMPANY, EMPLOYEE, body="讨论选定引用", request_id="typed", assignment_ref=assignment, references=refs)
        restored = ConversationService(Database(db.path)).read(COMPANY, EMPLOYEE)
        assert restored["conversation_id"] == original["conversation_id"]
        assert restored["messages"][0]["references"] == message["references"]
        assert "DO_NOT_HYDRATE_THIS_BODY" not in str(restored)
        with pytest.raises(RuntimeScopeError):
            service.append_ceo(COMPANY, EMPLOYEE, body="不能越界", request_id="wrong-knowledge", assignment_ref=assignment,
                references=[{**refs[-1], "workspace_id": "other"}])
