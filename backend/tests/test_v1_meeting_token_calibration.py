"""Bounded local regressions, never a substitute for cloud acceptance."""
import json

import pytest

from app.meeting_service import MeetingService
from app.model_gateway import ModelGatewayAdapter
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import COMPANY, TENANT, seed, MeetingProvider, HEADERS, PREFIX
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


def context():
    return {
        "meeting": {"topic": "研究", "background": "背景" * 2000},
        "speaker": {"employeeRef": "employee-a", "responsibility": "核对证据", "responsibilityKey": "research"},
        "trigger": {"kind": "CEO_MESSAGE", "text": "问题" * 2000},
        "recentConversation": [{"text": "讨论" * 2000, "actorRef": "employee-b"} for _ in range(10)],
        "selectedKnowledge": [{"ref": "knowledge-a", "title": "合法资料", "bodyExcerpt": "证据" * 600}],
        "selectedRefs": ["knowledge-a"], "proposal": {"summary": "方向" * 2000},
        "decision": {"ref": "decision-a", "status": "WAITING_CEO"},
    }


def test_judgment_context_and_output_are_small():
    source = context()
    result = MeetingService._compact_context(source, judgment=True)
    assert len(result["recentConversation"]) == 3
    assert len(result["meeting"]["background"]) <= 180
    assert "bodyExcerpt" not in result["selectedKnowledge"][0]
    assert result["selectedRefs"] == ["knowledge-a"]
    assert result["decision"]["status"] == "WAITING_CEO"
    prompt = MeetingService._self_judgment_prompt(source, source["speaker"])
    assert '"should_speak"' in prompt and "STAY_SILENT" in prompt
    assert "最多60字" in prompt and '"contribution"' not in prompt
    assert len(prompt) < 3000


def test_contribution_keeps_evidence_leader_has_bounded_context():
    source = context()
    assert source["selectedKnowledge"][0]["bodyExcerpt"] in MeetingService._speaker_prompt(source)
    compact = MeetingService._compact_context(source)
    assert len(compact["recentConversation"]) == 4
    assert len(compact["selectedKnowledge"][0]["summary"]) == 500
    prompt = MeetingService._leader_prompt(source, {"response": "专业观点", "unused": "x" * 50000})
    assert "专业观点" in prompt and "unused" not in prompt
    assert len(prompt) < 7000


def test_gateway_output_ceiling_is_in_actual_request():
    payloads = []
    def post(_url, payload, _headers, _timeout):
        payloads.append(payload)
        return {"choices": [{"message": {"content": "{}"}}],
                "usage": {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30}}
    adapter = ModelGatewayAdapter(base_url="https://isolated.example.invalid", api_key="local-test-only",
                                  model_name="test", http_post=post)
    result = adapter.execute("bounded", max_output_tokens=2048)
    assert payloads[-1]["max_tokens"] == 2048
    assert result["total_tokens"] == 30
    adapter.execute("unchanged")
    assert "max_tokens" not in payloads[-1]
    for bad in (0, -1, True, 100000, "1024"):
        with pytest.raises(ValueError):
            adapter.execute("invalid", max_output_tokens=bad)
    assert len(payloads) == 2


def test_saved_budget_and_accounting_survive_service_restart(tmp_path):
    assert MeetingService.LIMITS == {
        "maxTurns": 6, "maxConsecutiveTurns": 1, "maxNoProgress": 2,
        "maxProviderCalls": 30, "maxConfirmedTokens": 80000,
        "maxConfirmedCost": "1.00", "maxElapsedSeconds": 300,
    }
    database, employees, _ = seed(tmp_path / "budget.sqlite")
    meeting_id = _create_meeting(database, employees)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        def update(state):
            state["limits"]["maxConfirmedTokens"] = 8000
            service._merge_usage(state, {"confirmedTokens": 7990, "confirmedCost": "0", "unknownMetering": True})
            service._merge_usage(state, {"confirmedTokens": 20, "confirmedCost": "0", "unknownMetering": True})
            return state
        service._update_orchestration(meeting_id, update)
        with database.connect() as conn:
            before = conn.execute("select orchestration_json from strategy_meetings where meeting_id=?", (meeting_id,)).fetchone()[0]
        # A new service/connection may read history but cannot recalibrate its saved limits.
        restarted = MeetingService(database)
        state = json.loads(before)
        assert state["usage"]["confirmedTokens"] == 8010
        assert state["limits"]["maxConfirmedTokens"] == 8000
        assert "Token" in restarted._budget_reason(state)
        with database.connect() as conn:
            assert conn.execute("select orchestration_json from strategy_meetings where meeting_id=?", (meeting_id,)).fetchone()[0] == before


def test_persisted_judgment_task_applies_output_ceiling_only_to_gate(tmp_path):
    from fastapi.testclient import TestClient
    from app.main import create_app
    path = tmp_path / "request-ceiling.sqlite"
    database, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    provider.leaders = 3
    adapter = provider.adapter()
    post = adapter.http_post
    requests = []
    def observe(url, payload, headers, timeout):
        text = payload["messages"][0]["content"]
        requests.append(("meeting-self-judgment" in text, payload.get("max_tokens")))
        return post(url, payload, headers, timeout)
    adapter.http_post = observe
    meeting_id = _create_meeting(database, employees)
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        response = client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        assert response.status_code in (200, 202)
    assert any(gate for gate, _ in requests)
    assert any(not gate for gate, _ in requests)
    assert all(limit == (2048 if gate else None) for gate, limit in requests)
