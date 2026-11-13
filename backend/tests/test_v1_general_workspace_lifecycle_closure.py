from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.database import Database
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import (
    COMPANY,
    TENANT,
    WORKSPACE,
    add_team,
    app,
    seed,
)


def _create(database, key="lifecycle"):
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        return GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            problem="收敛一个通用业务问题",
            expected_result="形成可验证结果",
            constraints=[],
            references=[],
            idempotency_key=key,
        )["work"]["entity_id"]


def test_general_work_pause_resume_is_persistent_and_blocks_new_execution(tmp_path):
    database = seed(tmp_path / "general-lifecycle-pause.sqlite")
    add_team(database)
    work_ref = _create(database, "pause-resume")
    calls = []

    async def execution(payload):
        calls.append(payload["mode"])
        return {"task_ref": "task-should-not-run"}

    with TestClient(app(database, execution)) as client:
        paused = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{work_ref}/lifecycle/pause",
            json={"reason": "CEO 暂停，等待补充资料"},
        )
        assert paused.status_code == 200, paused.text
        assert paused.json()["work"]["lifecycle_status"] == "PAUSED"
        blocked = client.post(f"/team-operating/works/{work_ref}/execute")
        assert blocked.status_code == 200, blocked.text
        assert blocked.json()["execution_blocked"]
        resumed = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{work_ref}/lifecycle/resume",
            json={},
        )
        assert resumed.status_code == 200, resumed.text
        assert resumed.json()["work"]["lifecycle_status"] == "ACTIVE"
        replay = client.post(
            f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{work_ref}/lifecycle/resume",
            json={},
        )
        assert replay.status_code == 200 and replay.json()["duplicate"] is True
    assert calls == []

    reopened = Database(str(tmp_path / "general-lifecycle-pause.sqlite"))
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        view = SharedWorkspaceProjection(reopened).general_workspace(COMPANY, WORKSPACE)
    item = next(item for item in view["current_work"] if item["work_ref"] == work_ref)
    assert item["status"] == "ACTIVE"
    assert item["lifecycle_status"] == "ACTIVE"
    assert item["responsibility_status"] == "ACTIVE"


def test_general_work_cancel_archive_restore_is_idempotent_and_non_destructive(tmp_path):
    database = seed(tmp_path / "general-lifecycle-archive.sqlite")
    add_team(database)
    work_ref = _create(database, "cancel-archive")
    path = f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{work_ref}/lifecycle"
    with TestClient(app(database)) as client:
        cancelled = client.post(f"{path}/cancel", json={"reason": "不再继续这项工作"})
        assert cancelled.status_code == 200, cancelled.text
        assert cancelled.json()["work"]["lifecycle_status"] == "CANCELLED"
        replay = client.post(f"{path}/cancel", json={"reason": "重复点击"})
        assert replay.status_code == 200 and replay.json()["duplicate"] is True
        archived = client.post(f"{path}/archive", json={"reason": "保留历史记录"})
        assert archived.status_code == 200, archived.text
        assert archived.json()["work"]["lifecycle_status"] == "ARCHIVED"
        restored = client.post(f"{path}/restore", json={})
        assert restored.status_code == 200, restored.text
        assert restored.json()["work"]["lifecycle_status"] == "CANCELLED"

    with database.connect() as connection:
        row = connection.execute(
            "select lifecycle_status, data_json from runtime_entities where entity_id=?", (work_ref,)
        ).fetchone()
    assert row["lifecycle_status"] == "CANCELLED"
    assert json.loads(row["data_json"])["responsibilityRouting"]["status"] == "CANCELLED"
    with TestClient(app(database)) as client:
        assert client.post(f"{path}/archive", json={}).status_code == 200
        assert client.post(f"{path}/restore", json={}).status_code == 200


def test_general_work_failed_execution_remains_waiting_without_completed_result(tmp_path):
    database = seed(tmp_path / "general-lifecycle-failure.sqlite")
    add_team(database)
    work_ref = _create(database, "failure")

    async def execution(payload):
        if payload["mode"] == "submit":
            return {"task_ref": "task-general-failure"}
        return {
            "output": json.dumps({"status": "FAILED", "summary": "测试命令失败", "problem": "请检查输入"}),
            "task_status": "FAILED",
            "session_ref": "session-general-failure",
            "artifact_refs": [],
            "execution_binding": {"callbackProvenance": {"verification_status": "UNVERIFIED"}},
        }

    with TestClient(app(database, execution)) as client:
        response = client.post(f"/team-operating/works/{work_ref}/execute")
        assert response.status_code == 200, response.text
        work = response.json()["work"]
        assert work["data"]["responsibilityRouting"]["status"] == "WAITING"
        assert work["lifecycle_status"] != "COMPLETED"
        current = client.get(f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general")
        item = next(item for item in current.json()["current_work"] if item["work_ref"] == work_ref)
        assert item["status"] == "WAITING"
        assert item["result_refs"] == ["task:task-general-failure"]
        with database.connect() as connection:
            execution_data = json.loads(connection.execute(
                "select data_json from runtime_entities where entity_id=?", (work_ref,)
            ).fetchone()["data_json"])
        assert next(iter(execution_data["responsibilityRouting"]["executions"].values()))["status"] == "FAILED"
        assert "核对原执行与证据" in item["recovery_action"]


def test_failed_work_cancel_rejects_before_any_routing_or_task_mutation(tmp_path):
    from app.runtime.child_work import CanonicalChildWorkRuntime
    database = seed(tmp_path / "invalid-cancel.sqlite")
    add_team(database)
    work_ref = _create(database, "invalid-cancel")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        child = CanonicalChildWorkRuntime(database)
        child.transition_work(work_ref, "FAILED", actor="SYSTEM", reason="TEST_ONLY injected local failure")
        before = child.get_work(work_ref)
        for action in ("cancel", "pause", "archive"):
            try:
                GeneralWorkspaceDelivery(database).control_work(company_id=COMPANY, workspace_id=WORKSPACE,
                    work_ref=work_ref, action=action, reason="must reject")
            except ValueError:
                pass
            else:
                raise AssertionError("illegal failed Work action was accepted")
            assert child.get_work(work_ref) == before
        projected = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
        item = next(x for x in projected["current_work"] if x["work_ref"] == work_ref)
        assert item["status"] == "FAILED"
        assert item["reason"] == "TEST_ONLY injected local failure"
        assert "重试" not in item["recovery_action"]


def test_pause_reason_and_employee_summary_follow_canonical_lifecycle(tmp_path):
    database = seed(tmp_path / "pause-reason.sqlite")
    add_team(database)
    work_ref = _create(database, "pause-reason")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        service = GeneralWorkspaceDelivery(database)
        service.control_work(company_id=COMPANY, workspace_id=WORKSPACE, work_ref=work_ref,
                             action="pause", reason="TEST_ONLY wait for operator")
        view = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
        item = next(x for x in view["current_work"] if x["work_ref"] == work_ref)
        assert item["reason"] == "TEST_ONLY wait for operator"
        employee = view["team"]["employees"][0]
        context = next(x for x in employee["current_responsibilities"] if x["object_ref"] == work_ref)
        assert context["work_status"] == "paused"
        assert not employee["ui_status"]["label"].startswith("工作中")
        service.control_work(company_id=COMPANY, workspace_id=WORKSPACE, work_ref=work_ref,
                             action="resume", reason="TEST_ONLY operator resumes original Work")
        resumed = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
        current = next(x for x in resumed["current_work"] if x["work_ref"] == work_ref)
        assert current["status"] == "ACTIVE"
        assert current["reason"] == "TEST_ONLY operator resumes original Work"


def test_company_scoped_holder_name_does_not_invent_workspace_team(tmp_path):
    database = seed(tmp_path / "company-holder.sqlite")
    add_team(database)
    ref = _create(database, "company-holder")
    with database.connect() as connection:
        connection.execute("update runtime_entities set workspace_id=null where entity_type='AI_EMPLOYEE'")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        view = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
    assert view["team"]["employees"] == []
    assert next(x for x in view["current_work"] if x["work_ref"] == ref)["responsibility_holder_name"] == "小策"
    assert view["operating_readiness"]["status"] == "NEEDS_DECISION"
