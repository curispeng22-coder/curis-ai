"""External SQLite only: shared holder/topic/quick-access contract, not cloud proof."""
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.conversation_service import ConversationService
from app.database import Database
from app.runtime import RuntimeScopeError
from backend.tests.test_employee_conversation import setup, scope
from backend.tests.test_v1_general_operating_contract import COMPANY, EMPLOYEE


def test_two_topics_same_employee_order_dismiss_reappear_and_restart(tmp_path):
    path = tmp_path / "topics.sqlite"
    db, assignment = setup(path)
    with scope():
        service = ConversationService(db)
        a = service.create(COMPANY, request_id="a", title="客户反馈", employee_ref=EMPLOYEE)["conversation_id"]
        b = service.create(COMPANY, request_id="b", title="每周复盘", employee_ref=EMPLOYEE)["conversation_id"]
        assert a != b and service.recent(COMPANY) == []  # Opening/visiting is not activity.
        for cid in [a, b]:
            service.append_ceo(COMPANY, EMPLOYEE, conversation_id=cid, body="讨论当前事实", request_id="first", assignment_ref=assignment)
        assert [x["conversation_id"] for x in service.recent(COMPANY)] == [b, a]
        assert [x["conversation_id"] for x in service.recent(COMPANY, search="客户")] == [a]
        service.dismiss(COMPANY, b)
        service.dismiss(COMPANY, b)
        assert len(service.read(COMPANY, conversation_id=b)["messages"]) == 1
        reopened = ConversationService(Database(str(path)))
        assert [x["conversation_id"] for x in reopened.recent(COMPANY)] == [a]
        reopened.append_ceo(COMPANY, EMPLOYEE, conversation_id=b, body="继续复盘", request_id="second", assignment_ref=assignment)
        assert [x["conversation_id"] for x in reopened.recent(COMPANY)] == [b, a]
        assert len(reopened.read(COMPANY, conversation_id=a)["messages"]) == 1
        assert len(reopened.read(COMPANY, conversation_id=b)["messages"]) == 2
        assert all("messages" not in x and "payload" not in x for x in reopened.recent(COMPANY))


def test_pre_employee_conversation_then_work_reference_same_owner(tmp_path):
    db, assignment = setup(tmp_path / "before-work.sqlite")
    from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
    from backend.tests.test_v1_general_operating_contract import WORKSPACE
    with scope():
        service = ConversationService(db)
        cid = service.create(COMPANY, request_id="before", title="先讨论一件事")["conversation_id"]
        first = service.append_ceo(COMPANY, conversation_id=cid, body="先整理客户问题", request_id="first")
        assert first["sender"]["kind"] == "CEO"
        service.join(COMPANY, cid, EMPLOYEE)
        service.join(COMPANY, cid, EMPLOYEE)
        work = GeneralWorkspaceDelivery(db).create_work(company_id=COMPANY, workspace_id=WORKSPACE,
            problem="整理客户问题", expected_result="可引用的工作", constraints=[], references=[], idempotency_key="topic-work")["work"]
        ref = {"kind": "WORK", "reference_id": work["entity_id"], "workspace_id": WORKSPACE}
        service.append_ceo(COMPANY, EMPLOYEE, conversation_id=cid, body="围绕这项工作继续", request_id="second",
                           assignment_ref=assignment, references=[ref])
        state = service.read(COMPANY, conversation_id=cid)
        assert state["conversation_id"] == cid and state["owner_ref"] == EMPLOYEE
        assert state["messages"][0] == first and len(state["messages"]) == 2
        assert state["messages"][1]["references"][0]["reference_id"] == work["entity_id"]
        assert state["messages"][0]["context"] == {"company_id": COMPANY}
        assert state["messages"][1]["context"]["assignment_ref"] == assignment
        with db.connect() as con:
            assert con.execute("select count(*) from tasks").fetchone()[0] == 0
            assert con.execute("select count(*) from projects").fetchone()[0] == 0


def test_topic_concurrent_creation_and_messages_are_idempotent(tmp_path):
    db, assignment = setup(tmp_path / "concurrent.sqlite")
    def create(_):
        with scope():
            service = ConversationService(db)
            cid = service.create(COMPANY, request_id="same", employee_ref=EMPLOYEE)["conversation_id"]
            message = service.append_ceo(COMPANY, EMPLOYEE, conversation_id=cid, body="一次消息", request_id="same", assignment_ref=assignment)
            return cid, message["message_id"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert len(set(pool.map(create, range(8)))) == 1
    with scope(), pytest.raises(ValueError):
        ConversationService(db).create(COMPANY, request_id="same", title="不同请求", employee_ref=EMPLOYEE)


@pytest.mark.parametrize("identity", [{"company_id": "other"}, {"tenant_id": "other"}, {"ceo_id": "other"}])
def test_topic_read_and_recent_scope_isolation(tmp_path, identity):
    db, _ = setup(tmp_path / "isolation.sqlite")
    with scope():
        cid = ConversationService(db).create(COMPANY, request_id="scope")["conversation_id"]
    with scope(**identity), pytest.raises(RuntimeScopeError):
        ConversationService(db).read(COMPANY, conversation_id=cid)
    with scope(**identity), pytest.raises(RuntimeScopeError):
        ConversationService(db).recent(COMPANY)


def test_joined_topics_use_one_ledger_and_do_not_mix_provider_context(tmp_path, monkeypatch):
    from dataclasses import replace
    from fastapi.testclient import TestClient
    from app.identity_membership import IdentityMembership
    from app.main import create_app
    from app.ai_usage import AIUsageService
    from backend.tests.test_conversation_usage import prepared
    from backend.tests.test_v1_general_operating_contract import TENANT
    authorize = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request:
        replace(authorize(self, tenant, request), role="ceo"))
    path = tmp_path / "joined-provider.sqlite"
    db, assignment, adapter, calls = prepared(path)
    headers = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}
    prefix = f"/api/workspace/v1/companies/{COMPANY}/conversations"
    states = []
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        for topic in ["TOPIC_ALPHA", "TOPIC_BETA"]:
            created = client.post(prefix, headers=headers, json={"request_id": topic, "title": topic})
            assert created.status_code == 201, created.text
            cid = created.json()["conversation_id"]
            url = prefix + "/" + cid
            assert client.post(url + "/messages", headers=headers, json={"body": topic, "request_id": "before"}).status_code == 202
            assert client.post(url + "/employee", headers=headers, json={"employee_ref": EMPLOYEE}).status_code == 200
            payload = {"body": "按当前责任回复", "assignment_ref": assignment, "request_id": "reply"}
            for _ in range(2):
                assert client.post(url + "/messages", headers=headers, json=payload).status_code == 202
            state = client.get(url, headers=headers).json()
            assert len(state["messages"]) == 3 and state["attempts"][0]["status"] == "COMPLETED", state
            states.append(state)
        assert len(client.get(prefix, headers=headers).json()["conversations"]) == 2
    assert len(calls) == 2
    import json
    assert "TOPIC_ALPHA" in json.dumps(calls[0]) and "TOPIC_BETA" not in json.dumps(calls[0])
    assert "TOPIC_BETA" in json.dumps(calls[1]) and "TOPIC_ALPHA" not in json.dumps(calls[1])
    with scope():
        reopened = ConversationService(Database(str(path)))
        for state in states:
            assert reopened.read(COMPANY, conversation_id=state["conversation_id"])["messages"] == state["messages"]
            usage = AIUsageService(db).list_records(conversation_ref=state["conversation_id"])
            assert len(usage) == 1 and usage[0]["canonical_employee_ref"] == EMPLOYEE
            assert usage[0]["project_id"] is None and usage[0]["work_ref"] is None
            assert usage[0]["cost_amount"] is None
