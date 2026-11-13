from __future__ import annotations

from fastapi.testclient import TestClient

from app.employee_execution_identity import EmployeeExecutionIdentity
from app.evolution_event_log import EvolutionEventLog
from app.result_store import ResultStore
from app.tenant_context import TenantContext

from .test_rd_artifact_review import CEO, COMPANY, HEADERS, PROJECT, TENANT, make_app, operating_workspace
from .test_rd_p7_decision import packet_payload
from .test_rd_responsibility_handoff import approved_cycle, create_handoff, handoff_action


def execution_result(number: int, *, status: str = "succeeded") -> dict:
    failed = status == "failed"
    return {
        "status": status,
        "output": f"真实研发执行 {number}" if not failed else f"Provider 执行 {number} 失败",
        "error": "provider_execution_failed" if failed else "",
        "task_ref": f"task-primary-{number}",
        "session_ref": f"session-primary-{number}",
        "artifact_refs": [f"artifact-primary-{number}"],
        "changed_files": ["src/calc.py"],
        "test_result": {
            "command": ["python3", "-m", "pytest", "-q"],
            "exitCode": 1 if failed else 0,
        },
        "computer_access": {
            "requested_intent": "AUTO_WITHIN_BOUNDARY",
            "configured_state": "CONFIGURED",
            "effective_state": "UNKNOWN",
            "verification_state": "UNVERIFIED",
        },
        "execution_binding": {"executionEmployeeRef": "developer-execution"},
    }


def review_result(number: int, outcome: str) -> dict:
    return {
        "status": "succeeded",
        "review_outcome": outcome,
        "output": f"REVIEW_OUTCOME: {outcome}\n第 {number} 轮审核证据。",
        "task_ref": f"task-review-{number}",
        "session_ref": f"session-review-{number}",
        "artifact_refs": [f"artifact-review-{number}"],
    }


def cycle_from(client: TestClient, workspace_id: str, cycle_id: str) -> tuple[dict, dict]:
    detail = client.get(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
        headers=HEADERS,
    ).json()
    return next(item for item in detail["cycles"] if item["entity_id"] == cycle_id), detail


def execute_review(client: TestClient, workspace_id: str, cycle: dict, reviewer_ref: str) -> dict:
    path = (
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}"
        f"/cycles/{cycle['entity_id']}/artifact-review"
    )
    created = client.post(
        path,
        headers=HEADERS,
        json={"ceo_id": CEO, "reviewer_employee_ref": reviewer_ref},
    )
    assert created.status_code == 201, created.text
    response = client.post(
        f"{path}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "reason": "执行本轮代码审核"},
    )
    assert response.status_code == 202, response.text
    return cycle_from(client, workspace_id, cycle["entity_id"])[0]


def test_phase2b_decision_revision_retry_and_restart_close_one_cycle(tmp_path, monkeypatch):
    state = {
        "primary_results": [
            execution_result(1),
            execution_result(2),
            execution_result(3, status="failed"),
            execution_result(4),
        ],
        "review_results": [
            review_result(1, "APPROVED"),
            review_result(2, "CHANGES_REQUESTED"),
            review_result(3, "APPROVED"),
        ],
    }
    app, database = make_app(tmp_path / "rd-phase2b-e2e.sqlite", state, monkeypatch)

    with TestClient(app) as client:
        workspace_id = operating_workspace(client)
        cycle, reviewer = approved_cycle(client, workspace_id)
        cycle_id = cycle["entity_id"]
        holder_ref = cycle["data"]["workContext"]["responsibilityEmployeeRef"]
        reviewer_ref = reviewer["entity_id"]
        decision_path = (
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}"
            f"/cycles/{cycle_id}/rd-decision"
        )
        assert client.post(decision_path, headers=HEADERS, json=packet_payload()).status_code == 201
        assert client.post(
            f"{decision_path}/review",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "CEO 已查看完整方案"},
        ).status_code == 200
        continued = client.post(
            f"{decision_path}/choose",
            headers=HEADERS,
            json={"ceo_id": CEO, "choice": "SAFE_DRY_RUN", "reason": "先执行隔离演练"},
        )
        assert continued.status_code == 202, continued.text
        cycle, detail = cycle_from(client, workspace_id, cycle_id)
        assert cycle["data"]["taskRef"] == "task-primary-2"
        assert cycle["data"]["artifactRefs"] == ["artifact-primary-2"]
        assert cycle["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert cycle["data"]["workContext"]["currentExecutorRef"] is None
        assert len(detail["decisions"]) == 1
        assert not detail["handoffs"]

        cycle = execute_review(client, workspace_id, cycle, reviewer_ref)
        change_review = cycle["data"]["artifactReview"]
        assert change_review["status"] == "CHANGES_REQUESTED"
        assert change_review["reviewerEmployeeRef"] == reviewer_ref
        assert change_review["originalHolderRef"] == holder_ref

        revision_path = (
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}"
            f"/cycles/{cycle_id}/artifact-review/revise"
        )
        revision_payload = {
            "ceo_id": CEO,
            "request_ref": change_review["requestRef"],
            "reason": "按第二轮审核意见修订",
        }
        failed = client.post(revision_path, headers=HEADERS, json=revision_payload)
        assert failed.status_code == 202, failed.text
        cycle, _ = cycle_from(client, workspace_id, cycle_id)
        assert cycle["lifecycle_status"] == "PAUSED"
        assert cycle["data"]["executionStatus"] == "FAILED"
        assert cycle["data"]["taskRef"] == "task-primary-3"
        assert cycle["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert cycle["data"]["workContext"]["currentExecutorRef"] is None
        duplicate_revision = client.post(revision_path, headers=HEADERS, json=revision_payload)
        assert duplicate_revision.status_code == 200
        assert state["primary_calls"] == 3

    with TestClient(app) as restarted:
        cycle, _ = cycle_from(restarted, workspace_id, cycle_id)
        assert cycle["lifecycle_status"] == "PAUSED"
        assert cycle["data"]["taskRef"] == "task-primary-3"
        resume_path = (
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}"
            f"/cycles/{cycle_id}/resume"
        )
        resume_payload = {"ceo_id": CEO, "reason": "Provider 已恢复，重试同一责任流"}
        resumed = restarted.post(resume_path, headers=HEADERS, json=resume_payload)
        duplicate_resume = restarted.post(resume_path, headers=HEADERS, json=resume_payload)
        assert resumed.status_code == 200, resumed.text
        assert duplicate_resume.status_code == 200, duplicate_resume.text
        assert resumed.json()["data"]["executionStatus"] == "READY"
        assert resumed.json()["data"]["workContext"]["currentExecutorRef"] is None
        retried = restarted.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重试 Developer 修订"},
        )
        assert retried.status_code == 202, retried.text
        cycle, detail = cycle_from(restarted, workspace_id, cycle_id)
        assert cycle["data"]["executionStatus"] == "COMPLETED"
        assert cycle["data"]["taskRef"] == "task-primary-4"
        assert cycle["data"]["taskHistoryRefs"] == [
            "task-primary-1",
            "task-primary-2",
            "task-primary-3",
        ]
        assert cycle["data"]["artifactHistoryRefs"] == [
            "artifact-primary-1",
            "artifact-primary-2",
            "artifact-primary-3",
        ]
        assert len(cycle["data"]["artifactReviewHistory"]) == 2
        assert [item["status"] for item in cycle["data"]["artifactReviewHistory"]] == [
            "APPROVED",
            "CHANGES_REQUESTED",
        ]
        assert cycle["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert cycle["data"]["workContext"]["currentExecutorRef"] is None
        assert state["primary_calls"] == 4
        assert not detail["handoffs"]

        cycle = execute_review(restarted, workspace_id, cycle, reviewer_ref)
        final_review = cycle["data"]["artifactReview"]
        assert final_review["status"] == "APPROVED"
        assert final_review["reviewerEmployeeRef"] == reviewer_ref
        assert final_review["originalHolderRef"] == holder_ref
        assert final_review["artifactRefs"] == ["artifact-primary-4"]
        assert state["review_calls"] == 3

        with database.connect() as connection:
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                "values (?, ?, ?, '', 'template-reviewer-e2e', 'Review AI', 'reviewer', 'idle')",
                (reviewer_ref, TENANT, COMPANY),
            )
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
                "values ('binding-reviewer-e2e', ?, ?, 'tenant_private', 'agent', 'agent.codex.rd')",
                (TENANT, reviewer_ref),
            )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            identity = EmployeeExecutionIdentity(database)
            identity.bind(
                company_id=COMPANY,
                workspace_id=workspace_id,
                runtime_employee_ref=reviewer_ref,
                company_employee_ref=reviewer_ref,
                employee_capability_binding_ref="binding-reviewer-e2e",
            )
            provider_task = ResultStore(database).create_task(
                "接收已审核责任上下文",
                company_id=COMPANY,
                project_id=PROJECT,
                capability_source="tenant_private",
                capability_type="agent",
                capability_id="agent.codex.rd",
                employee_id=reviewer_ref,
                employee_role="reviewer",
                employee_name="Review AI",
            )
            provider_task = ResultStore(database).transition(
                provider_task["task_id"], "COMPLETED", {"output": "责任上下文已验证"},
            )
            identity.record_task_assignment(
                company_id=COMPANY,
                workspace_id=workspace_id,
                runtime_employee_ref=reviewer_ref,
                task_ref=provider_task["task_id"],
                employee_capability_binding_ref="binding-reviewer-e2e",
            )
            EvolutionEventLog(database).record(
                correlation_id=provider_task["task_id"],
                event_type="usage.task_execution",
                tenant_id=TENANT,
                idempotency_key=f"provider-ack:{provider_task['task_id']}",
                payload={
                    "task_id": provider_task["task_id"],
                    "company_id": COMPANY,
                    "employee_id": reviewer_ref,
                    "capability_source": "tenant_private",
                    "session_id": "session-provider-ack-e2e",
                    "status": "success",
                },
            )

        assert create_handoff(restarted, workspace_id, cycle, reviewer).status_code == 201
        assert handoff_action(
            restarted,
            workspace_id,
            cycle_id,
            "send",
            {"ceo_id": CEO, "reason": "发送已审核责任上下文"},
        ).status_code == 200
        provider_ack_payload = {
            "ceo_id": CEO,
            "task_ref": provider_task["task_id"],
            "session_ref": "session-provider-ack-e2e",
            "reason": "Provider 证据证明接收 Employee 已确认",
        }
        provider_ack_path = (
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}"
            f"/cycles/{cycle_id}/responsibility-handoff/provider-ack"
        )
        forged_ack = restarted.post(
            provider_ack_path,
            headers=HEADERS,
            json={**provider_ack_payload, "session_ref": "forged-provider-session"},
        )
        assert forged_ack.status_code == 422
        before_ack, before_ack_detail = cycle_from(restarted, workspace_id, cycle_id)
        assert before_ack["data"]["responsibilityHandoff"]["status"] == "SENT"
        assert before_ack["data"]["workContext"]["responsibilityEmployeeRef"] == holder_ref
        assert before_ack_detail["handoffs"][0]["lifecycle_status"] == "SENT"
        acknowledged = restarted.post(provider_ack_path, headers=HEADERS, json=provider_ack_payload)
        duplicate_ack = restarted.post(provider_ack_path, headers=HEADERS, json=provider_ack_payload)
        assert acknowledged.status_code == duplicate_ack.status_code == 200
        assert acknowledged.json()["data"]["responsibilityHandoff"]["providerAck"]["verification_status"] == "VERIFIED"
        assert acknowledged.json()["data"]["workContext"]["responsibilityEmployeeRef"] == reviewer_ref
        assert acknowledged.json()["data"]["workContext"]["currentExecutorRef"] is None

    with TestClient(app) as final_restart:
        cycle, detail = cycle_from(final_restart, workspace_id, cycle_id)
        assert cycle["data"]["artifactReview"]["status"] == "APPROVED"
        assert cycle["data"]["taskRef"] == "task-primary-4"
        assert cycle["data"]["artifactReview"]["originalHolderRef"] == holder_ref
        assert cycle["data"]["workContext"]["responsibilityEmployeeRef"] == reviewer_ref
        assert cycle["data"]["workContext"]["currentExecutorRef"] is None
        assert len(detail["decisions"]) == 1
        assert len(detail["handoffs"]) == 1
        assert detail["handoffs"][0]["lifecycle_status"] == "COMPLETED"
        assert detail["handoffs"][0]["data"]["providerAck"]["verification_status"] == "VERIFIED"
        assert len({*cycle["data"]["taskHistoryRefs"], cycle["data"]["taskRef"]}) == 4
