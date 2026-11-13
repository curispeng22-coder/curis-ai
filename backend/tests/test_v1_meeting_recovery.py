"""Recovery checks; deterministic transport is regression evidence, never cloud acceptance."""
import json

from fastapi.testclient import TestClient

from app.main import create_app
from app.meeting_service import MeetingService
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import (
    COMPANY, HEADERS, PREFIX, TENANT, MeetingProvider, seed,
)
from backend.tests.test_v1_meeting_employee_self_judgment import (
    _create_meeting, _patch_orchestration,
)


def test_decision_work_respects_exhausted_global_budget(tmp_path):
    path = tmp_path / "decision-budget.sqlite"
    database, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    meeting_id = _create_meeting(database, employees)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = MeetingService(database)
        service.request_decision(COMPANY, meeting_id, provider._decision())
        service.choose_decision(COMPANY, meeting_id, choice="FOCUS", reason="隔离测试授权")
    _patch_orchestration(database, meeting_id, {"providerCallCount": 30})
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    assert provider.calls == []
    assert detail["orchestration"]["providerCallCount"] == 30
    assert detail["orchestration"]["status"] == "BLOCKED"
    assert detail["result_refs"] == []


def test_invalid_model_json_keeps_failed_call_accounting(tmp_path):
    path = tmp_path / "invalid-json.sqlite"
    database, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)

    def invalid_response(_url, payload, _headers, _timeout):
        provider.calls.append(payload)
        return {"choices": [{"message": {"content": "not valid JSON"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}}

    adapter = provider.adapter()
    adapter.http_post = invalid_response
    meeting_id = _create_meeting(database, employees)
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    assert len(provider.calls) == 1
    assert detail["orchestration"]["providerCallCount"] == 1
    assert detail["orchestration"]["status"] == "BLOCKED"
    with database.connect() as connection:
        works = connection.execute("select data_json from runtime_entities where entity_type='WORK'").fetchall()
    for row in works:
        route = json.loads(row["data_json"]).get("responsibilityRouting", {})
        assert not route.get("currentExecutorRef")
