"""Isolated mapping/validator proof, not a substitute for cloud E2E."""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.meeting_service import MeetingService
from app.tenant_context import TenantContext
from backend.tests.test_v1_meeting_autonomous_discussion import (
    seed, MeetingProvider, COMPANY, TENANT, HEADERS, PREFIX,
)
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


@pytest.mark.parametrize("missing", [None, "event", "cannotDecideReason", "continuationPlan", "recommendationReason", "foreign_ref"])
def test_mapping_and_fail_closed(tmp_path, missing):
    path = tmp_path / "mapping.sqlite"
    database, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    request = provider._decision()
    request.pop("decisionKey")
    request["recommendationIndex"] = 0
    request["evidenceRefs"] = [knowledge]
    request["options"][0].pop("cost")  # Unknown, not a fabricated price.
    if missing == "foreign_ref":
        request["evidenceRefs"] = ["knowledge-not-selected"]
    elif missing:
        request.pop(missing)
    provider._decision = lambda: request
    meeting_id = _create_meeting(database, employees, context_refs=[{"type": "KNOWLEDGE", "ref": knowledge}])
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        detail = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    with database.connect() as conn:
        count = conn.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0]
    if missing:
        assert count == 0 and not detail["decision_ref"]
        assert detail["orchestration"]["status"] == "BLOCKED"
        assert detail["orchestration"]["blockedReason"]
        assert not detail["orchestration"]["activeRunId"]
        assert not detail["work_refs"] and not detail["result_refs"]
        return
    assert count == 1
    decision = detail["decision"]
    data = decision["data"]
    assert decision["lifecycle_status"] == "WAITING_CEO"
    assert data["meetingRef"] == meeting_id and data["conversationRef"] == detail["conversation_id"]
    assert data["proposalRef"] == detail["orchestration"]["proposal"]["artifactRef"]
    assert data["proposalRef"] in data["resultRefs"] and data["evidenceRefs"] == [knowledge]
    assert data["requesterRef"] == employees["leader"][0] and data["assignmentRef"]
    assert data["businessRef"] == detail["business_id"]
    assert decision["company_id"] == COMPANY and decision["workspace_id"] == detail["workspace_id"]
    assert data["options"][0]["cost"] == {"value": "尚未验证", "provenance": "UNK"}
    assert data["layer0Actions"] == ["VIEW_OPTIONS", "DEFER"]
    calls = len(provider.calls)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            service = MeetingService(database)
            meeting = database.get_strategy_meeting(TENANT, meeting_id)
            packet = service._map_leader_decision(meeting, request)
            again = service.request_decision(COMPANY, meeting_id, packet)
            assert again["decision_ref"] == detail["decision_ref"]
            assert again["timeline"] == detail["timeline"]
            bad = dict(packet, complexity="INVALID")
            with pytest.raises(ValueError):
                service.request_decision(COMPANY, meeting_id, bad)
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
    assert len(provider.calls) == calls
    with database.connect() as conn:
        assert conn.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 1
        assert conn.execute("pragma integrity_check").fetchone()[0] == "ok"
