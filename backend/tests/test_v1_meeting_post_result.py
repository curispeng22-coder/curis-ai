"""Post-result routing contract with local provider, not cloud acceptance."""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.meeting_service import MeetingService
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import seed, MeetingProvider, COMPANY, TENANT, HEADERS, PREFIX
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


@pytest.mark.parametrize("outcome", ["DISCUSSION_SUFFICIENT", "CONTINUE_DISCUSSION", "NEEDS_CEO_DECISION", "BUDGET"])
def test_silent_result_still_reaches_bounded_leader(tmp_path, outcome):
    path = tmp_path / "result.sqlite"
    db, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    original = provider.execute
    observed = []

    def execute(prompt):
        raw = original(prompt)
        if '"kind":"RESULT_RETURNED"' in prompt:
            payload = json.loads(raw["output"])
            if payload["resultType"] == "meeting-self-judgment":
                payload["should_speak"] = False
            elif payload["resultType"] == "meeting-leader-evaluation":
                observed.append(prompt)
                assert '"returnedResults":[' in prompt and '"employeeJudgments":[' in prompt
                assert '"choice":"OPTION_' in prompt and '"executionStatus":"COMPLETED"' in prompt
                payload["outcome"] = outcome
                if outcome == "NEEDS_CEO_DECISION":
                    payload["proposal"] = {"summary": "返回结果产生新的取舍", "rationale": "隔离测试", "unknowns": []}
                    payload["decisionPacket"] = provider._decision()
            raw["output"] = json.dumps(payload, ensure_ascii=False)
        return raw

    provider.execute = execute
    mid = _create_meeting(db, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
        first = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
        assert first["decision"]["lifecycle_status"] == "WAITING_CEO"
        if outcome == "BUDGET":
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
                service = MeetingService(db)
                # Permit both real local Work executions and two self judgments; then stop before Leader.
                service._update_orchestration(mid, lambda state: state | {"limits": state["limits"] | {
                    "maxProviderCalls": 4}})
        client.post(f"{PREFIX}/{mid}/decision/review", headers=HEADERS)
        client.post(f"{PREFIX}/{mid}/decision/choose", headers=HEADERS,
                    json={"choice": "OPTION_1", "reason": "隔离验收"})
        final = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    if outcome == "BUDGET":
        assert not observed and final["orchestration"]["status"] == "BLOCKED"
        assert final["orchestration"]["currentCycle"]["providerCallCount"] == final["orchestration"]["limits"]["maxProviderCalls"]
        return
    assert observed and final["result_refs"], final["orchestration"]
    turns = [t for t in final["orchestration"]["turns"] if t["event"]["kind"] == "RESULT_RETURNED"]
    assert turns and all(t["speakerRef"] == "" and not any(j["should_speak"] for j in t["selfJudgments"].values()) for t in turns)
    assert len({t["event"]["eventId"] for t in turns}) == len(turns)
    assert all(t["leaderOutcome"] == outcome for t in turns)
    if outcome == "NEEDS_CEO_DECISION":
        assert final["decision_ref"] != first["decision_ref"]
        assert final["decision"]["lifecycle_status"] == "WAITING_CEO"
    elif outcome == "DISCUSSION_SUFFICIENT":
        assert final["orchestration"]["status"] == "SUFFICIENT"
    count = len(observed)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        restored = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
        assert restored["decision_ref"] == final["decision_ref"]
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
    assert len(observed) == count


def test_ordinary_ack_does_not_force_leader(tmp_path):
    db, employees, knowledge = seed(tmp_path / "ack.sqlite")
    provider = MeetingProvider(knowledge)
    mid = _create_meeting(db, employees)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(db)
        service._update_orchestration(mid, lambda s: s | {"pendingEvents": []})
        service.add_message(COMPANY, mid, actor_type="CEO", actor_ref="", text="收到")
    with TestClient(create_app(str(tmp_path / "ack.sqlite"), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
    assert provider.leaders == 0


def test_canonical_evidence_message_is_scoped_and_persistent(tmp_path):
    path = tmp_path / "evidence-message.sqlite"
    db, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    mid = _create_meeting(db, employees)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        rejected = client.post(f"{PREFIX}/{mid}/messages", headers=HEADERS, json={
            "text": "补充资料", "context_refs": [{"type": "KNOWLEDGE", "ref": "outside-scope"}]})
        assert rejected.status_code == 403
        response = client.post(f"{PREFIX}/{mid}/messages", headers=HEADERS, json={
            "text": "补充已选择的示例原文，请依据资料判断，不强求完成。",
            "context_refs": [{"type": "KNOWLEDGE", "ref": knowledge}]})
        assert response.status_code == 200, response.text
        before = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    assert {"type": "KNOWLEDGE", "ref": knowledge} in before["context_refs"]
    assert any(knowledge in str(call) for call in provider.calls)
    count = len(provider.calls)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        after = client.get(f"{PREFIX}/{mid}", headers=HEADERS).json()
    assert before["context_refs"] == after["context_refs"] and len(provider.calls) == count
