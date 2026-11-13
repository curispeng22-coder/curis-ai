from __future__ import annotations

from fastapi.testclient import TestClient

from .test_rd_artifact_review import CEO, COMPANY, HEADERS, make_app, operating_workspace
from .test_rd_responsibility_handoff import approved_cycle


def packet_payload():
    return {
        "ceo_id": CEO,
        "decision_key": "user-schema-migration",
        "event": "用户数据结构变更已通过代码审核，但会影响线上存储。",
        "cannot_decide_reason": "该变更具有业务影响且不应由研发员工自行决定。",
        "options": [
            {
                "option_id": "SAFE_DRY_RUN",
                "label": "先执行隔离演练",
                "impact": {"value": "只验证迁移脚本与回滚路径，不改线上数据。", "provenance": "POLICY"},
                "risk": {"value": "演练仍可能暴露脚本缺陷，但不会写入线上库。", "provenance": "EST"},
                "cost": {"value": "尚未验证额外时间成本。", "provenance": "UNK"},
                "continuation_instruction": "在声明文件范围内补充迁移 dry-run 校验，不连接或写入线上数据库。",
                "resource_refs": ["src/calc.py"],
                "test_command": ["python3", "-m", "pytest", "-q"],
            },
            {
                "option_id": "PAUSE_CHANGE",
                "label": "暂停本次结构变更",
                "impact": {"value": "保留当前已审核结果，不继续迁移准备。", "provenance": "FACT"},
                "risk": {"value": "业务目标会延后，具体影响尚未验证。", "provenance": "UNK"},
                "cost": {"value": "不产生新的执行成本。", "provenance": "FACT"},
                "continuation_instruction": "记录暂停原因并验证现有代码测试保持通过，不执行迁移。",
                "resource_refs": ["src/calc.py"],
                "test_command": ["python3", "-m", "pytest", "-q"],
            },
        ],
        "recommendation_option_id": "SAFE_DRY_RUN",
        "recommendation_provenance": "EST",
        "recommendation_reason": {
            "value": "研发员工建议先隔离演练，因为当前没有线上回滚证据。",
            "provenance": "EST",
        },
        "ceo_choice_prompt": "请选择先演练或暂停；查看方案前不会执行。",
        "continuation_plan": "选择后由原研发负责人沿现有受控 Task 路径自动继续。",
    }


def test_high_risk_rd_decision_requires_review_and_auto_continues_same_holder(tmp_path, monkeypatch):
    state = {"review_result": {
        "status": "succeeded",
        "review_outcome": "APPROVED",
        "output": "REVIEW_OUTCOME: APPROVED",
        "task_ref": "task-review-p7",
        "artifact_refs": ["artifact-review-p7"],
    }}
    app, database = make_app(tmp_path / "rd-p7.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, _ = approved_cycle(client, workspace_id)
        holder_ref = cycle["data"]["workContext"]["responsibilityEmployeeRef"]
        path = f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/rd-decision"

        first = client.post(path, headers=HEADERS, json=packet_payload())
        duplicate = client.post(path, headers=HEADERS, json=packet_payload())
        assert first.status_code == duplicate.status_code == 201
        decision_ref = first.json()["data"]["rdDecisionPacketRef"]
        assert duplicate.json()["data"]["rdDecisionPacketRef"] == decision_ref
        assert first.json()["data"]["workContext"]["status"] == "needs_ceo"
        assert first.json()["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert first.json()["data"]["workContext"]["currentExecutorRef"] is None
        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        pending = next(item for item in detail["decisions"] if item["entity_id"] == decision_ref)
        assert pending["data"]["layer0Actions"] == ["VIEW_OPTIONS", "DEFER"]
        assert pending["data"]["options"][0]["risk"]["provenance"] == "EST"

        blocked = client.post(
            f"{path}/choose", headers=HEADERS,
            json={"ceo_id": CEO, "choice": "SAFE_DRY_RUN", "reason": "尚未查看完整方案"},
        )
        assert blocked.status_code == 409
        deferred = client.post(
            f"{path}/choose", headers=HEADERS,
            json={
                "ceo_id": CEO,
                "choice": "DEFER",
                "reason": "先等待业务窗口",
                "next_check_at": "2026-08-18T02:00:00+00:00",
            },
        )
        assert deferred.status_code == 200
        assert deferred.json()["data"]["workContext"]["status"] == "needs_ceo"
        assert state["primary_calls"] == 1

        assert client.post(
            f"{path}/review", headers=HEADERS,
            json={"ceo_id": CEO, "reason": "CEO 已查看完整方案"},
        ).status_code == 200
        assert client.post(
            f"{path}/review", headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重复打开"},
        ).status_code == 200

        applied = client.post(
            f"{path}/choose", headers=HEADERS,
            json={"ceo_id": CEO, "choice": "SAFE_DRY_RUN", "reason": "先做隔离演练"},
        )
        assert applied.status_code == 202
        assert applied.json()["data"]["executionStatus"] == "RUNNING"
        assert applied.json()["data"]["workContext"]["currentExecutorRef"] == holder_ref

        detail = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        continued = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
        decision = next(item for item in detail["decisions"] if item["entity_id"] == decision_ref)
        assert decision["lifecycle_status"] == "APPLIED"
        assert decision["data"]["choice"] == "SAFE_DRY_RUN"
        assert continued["data"]["executionStatus"] == "COMPLETED"
        assert continued["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert continued["data"]["workContext"]["currentExecutorRef"] is None
        assert continued["data"]["taskHistoryRefs"] == ["task-primary"]
        assert continued["data"]["artifactReview"] is None
        assert len(continued["data"]["artifactReviewHistory"]) == 1
        assert state["primary_calls"] == 2
        assert not detail["handoffs"]

        with database.connect() as connection:
            transitions = connection.execute(
                "select source, target from runtime_transition_log "
                "where tenant_id = ? and entity_type = 'decision_packet' and entity_id = ? order by log_id",
                (HEADERS["X-Tenant-Id"], decision_ref),
            ).fetchall()
        assert [(row["source"], row["target"]) for row in transitions] == [
            ("DRAFT", "READY"),
            ("READY", "WAITING_CEO"),
            ("WAITING_CEO", "DECIDED"),
            ("DECIDED", "APPLIED"),
        ]

        repeated = client.post(
            f"{path}/choose", headers=HEADERS,
            json={"ceo_id": CEO, "choice": "SAFE_DRY_RUN", "reason": "重复提交"},
        )
        assert repeated.status_code == 200
        assert state["primary_calls"] == 2

    with TestClient(app) as restarted:
        detail = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        cycle = next(item for item in detail["cycles"] if item["entity_id"] == cycle["entity_id"])
        decision = next(item for item in detail["decisions"] if item["entity_id"] == decision_ref)
        assert decision["lifecycle_status"] == "APPLIED"
        assert cycle["data"]["executionStatus"] == "COMPLETED"
        assert cycle["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert cycle["data"]["workContext"]["currentExecutorRef"] is None


def test_rd_decision_provenance_fails_closed(tmp_path, monkeypatch):
    state = {"review_result": {
        "status": "succeeded",
        "review_outcome": "APPROVED",
        "output": "REVIEW_OUTCOME: APPROVED",
        "task_ref": "task-review-invalid-provenance",
        "artifact_refs": ["artifact-review-invalid-provenance"],
    }}
    app, _ = make_app(tmp_path / "rd-p7-invalid.sqlite", state, monkeypatch)
    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, _ = approved_cycle(client, workspace_id)
        payload = packet_payload()
        payload["options"][0]["risk"]["provenance"] = "GUESSED"
        response = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle['entity_id']}/rd-decision",
            headers=HEADERS,
            json=payload,
        )
        assert response.status_code == 422
