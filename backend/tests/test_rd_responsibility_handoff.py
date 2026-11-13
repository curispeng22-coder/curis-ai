from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from .test_rd_artifact_review import (
    CEO,
    COMPANY,
    HEADERS,
    completed_cycle,
    create_and_execute_review,
    make_app,
    operating_workspace,
)


def approved_cycle(client, workspace_id):
    cycle, target = completed_cycle(client, workspace_id)
    assert create_and_execute_review(client, workspace_id, cycle, target).status_code == 202
    detail = client.get(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
        headers=HEADERS,
    ).json()
    cycle = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
    assert cycle["data"]["artifactReview"]["status"] == "APPROVED"
    return cycle, target


def create_handoff(client, workspace_id, cycle, target):
    return client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/responsibility-handoff",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "target_employee_ref": target["entity_id"],
            "responsibility_summary": "接管已审核代码的验证责任",
            "reason": "实现完成且审核通过，进入独立验证",
            "next_check_at": "2026-08-18T02:00:00+00:00",
        },
    )


def handoff_action(client, workspace_id, cycle_id, action, payload):
    return client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/responsibility-handoff/{action}",
        headers=HEADERS,
        json=payload,
    )


def test_rd_handoff_transfers_holder_once_and_survives_restart(tmp_path, monkeypatch):
    state = {"review_result": {
        "status": "succeeded",
        "review_outcome": "APPROVED",
        "output": "REVIEW_OUTCOME: APPROVED\n代码与证据一致。",
        "task_ref": "task-review-approved",
        "session_ref": "session-review-approved",
        "artifact_refs": ["artifact-review-approved"],
    }}
    app, database = make_app(tmp_path / "rd-handoff.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, target = approved_cycle(client, workspace_id)
        original_holder = cycle["data"]["workContext"]["responsibilityEmployeeRef"]

        first = create_handoff(client, workspace_id, cycle, target)
        duplicate_create = create_handoff(client, workspace_id, cycle, target)
        assert first.status_code == duplicate_create.status_code == 201
        handoff_ref = first.json()["data"]["responsibilityHandoff"]["handoffRef"]
        assert duplicate_create.json()["data"]["responsibilityHandoff"]["handoffRef"] == handoff_ref
        assert first.json()["data"]["workContext"]["responsibilityEmployeeRef"] == original_holder

        sent = handoff_action(
            client, workspace_id, cycle["entity_id"], "send",
            {"ceo_id": CEO, "reason": "发送责任上下文"},
        )
        duplicate_send = handoff_action(
            client, workspace_id, cycle["entity_id"], "send",
            {"ceo_id": CEO, "reason": "重复发送"},
        )
        assert sent.status_code == duplicate_send.status_code == 200
        assert sent.json()["data"]["responsibilityHandoff"]["status"] == "SENT"
        assert sent.json()["data"]["workContext"]["responsibilityEmployeeRef"] == original_holder

        accepted = handoff_action(
            client, workspace_id, cycle["entity_id"], "respond",
            {"ceo_id": CEO, "decision": "ACKNOWLEDGE", "reason": "上下文完整，接管责任"},
        )
        duplicate_accept = handoff_action(
            client, workspace_id, cycle["entity_id"], "respond",
            {"ceo_id": CEO, "decision": "ACKNOWLEDGE", "reason": "重复确认"},
        )
        assert accepted.status_code == duplicate_accept.status_code == 200
        assert accepted.json()["data"]["responsibilityHandoff"]["status"] == "COMPLETED"
        assert accepted.json()["data"]["workContext"]["responsibilityEmployeeRef"] == target["entity_id"]
        assert accepted.json()["data"]["workContext"]["currentExecutorRef"] is None

        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert len(detail["handoffs"]) == 1
        assert detail["handoffs"][0]["entity_id"] == handoff_ref
        assert detail["handoffs"][0]["lifecycle_status"] == "COMPLETED"
        assert not detail["decisions"]
        assert next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])["data"]["artifactReview"]["originalHolderRef"] == original_holder

        with database.connect() as connection:
            transitions = connection.execute(
                "select source, target from runtime_transition_log "
                "where tenant_id = ? and entity_type = 'handoff' and entity_id = ? order by log_id",
                (HEADERS["X-Tenant-Id"], handoff_ref),
            ).fetchall()
        assert [(row["source"], row["target"]) for row in transitions] == [
            ("CREATED", "SENT"),
            ("SENT", "ACKNOWLEDGED"),
            ("ACKNOWLEDGED", "COMPLETED"),
        ]

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        recovered = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
        assert recovered["data"]["responsibilityHandoff"]["handoffRef"] == handoff_ref
        assert recovered["data"]["responsibilityHandoff"]["status"] == "COMPLETED"
        assert recovered["data"]["workContext"]["responsibilityEmployeeRef"] == target["entity_id"]
        assert recovered["data"]["workContext"]["currentExecutorRef"] is None


@pytest.mark.parametrize("decision, terminal", [("RETURN", "RETURNED"), ("REJECT", "REJECTED")])
def test_rd_handoff_return_or_reject_keeps_original_holder(tmp_path, monkeypatch, decision, terminal):
    state = {"review_result": {
        "status": "succeeded",
        "review_outcome": "APPROVED",
        "output": "REVIEW_OUTCOME: APPROVED",
        "task_ref": f"task-review-{decision.lower()}",
        "artifact_refs": [f"artifact-review-{decision.lower()}"],
    }}
    app, _ = make_app(tmp_path / f"rd-handoff-{decision.lower()}.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, target = approved_cycle(client, workspace_id)
        original_holder = cycle["data"]["workContext"]["responsibilityEmployeeRef"]
        assert create_handoff(client, workspace_id, cycle, target).status_code == 201
        assert handoff_action(
            client, workspace_id, cycle["entity_id"], "send",
            {"ceo_id": CEO, "reason": "发送责任上下文"},
        ).status_code == 200
        response = handoff_action(
            client, workspace_id, cycle["entity_id"], "respond",
            {"ceo_id": CEO, "decision": decision, "reason": "上下文不足，暂不接管"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["responsibilityHandoff"]["status"] == terminal
        assert response.json()["data"]["workContext"]["responsibilityEmployeeRef"] == original_holder
        assert response.json()["data"]["workContext"]["currentExecutorRef"] is None
