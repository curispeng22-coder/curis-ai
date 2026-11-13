"""Synthetic C01 source checks. No external provider or Native application."""
from __future__ import annotations

import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.shared_workspace_router import build_shared_workspace_router
from app.api.team_operating_router import build_team_operating_router
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.result_store import ResultStore
from app.result_attention import ResultAttention
from app.runtime.foundation import RuntimeScopeError
from app.runtime.foundation import RuntimeFoundation
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.runtime.responsibility_routing import ResponsibilityRoutingError, ResponsibilityRoutingRuntime
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.task_execution_control import TaskExecutionControlService, build_task_execution_control_router
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import seed, add_team, TENANT, COMPANY, WORKSPACE, EMPLOYEE
from backend.tests.test_general_single_attempt_limits import ready as limited_ready, task_for as limited_task_for


def scope():
    return TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="ceo")


def source_for(fields):
    return json.dumps({"status": "USER_REQUIRED", "resultType": "general-business-result",
                       "summary": "等待用户补充", "problem": "", "humanInput": fields}, ensure_ascii=False)


@pytest.fixture
def prepared(tmp_path):
    database = seed(tmp_path / "human-input.sqlite")
    add_team(database)
    with scope():
        work = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE, problem="整理反馈",
            expected_result="形成改进建议", constraints=[], references=[],
            idempotency_key="human-input-work",
        )["work"]
        ref = work["entity_id"]
        router = ResponsibilityRoutingRuntime(database)
        assignment = work["data"]["responsibilityRouting"]["currentAssignmentRef"]
        key = f"responsibility:{ref}:{assignment}:1"
        router.begin_employee_execution(ref, execution_key=key, assignment_ref=assignment)
        task = ResultStore(database).create_task(
            "整理反馈", company_id=COMPANY, workspace_id=WORKSPACE, work_ref=ref,
            execution_ref=key, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            capability_source="tenant_private", capability_type="agent",
            capability_id="agent.general.local", employee_id=EMPLOYEE,
        )
        task_id = task["task_id"]
        router.attach_provider_task(ref, execution_key=key, task_ref=task_id)
        fields = {
            "kind": "LOCAL_INFORMATION", "aiCompleted": "已梳理已有反馈",
            "whyUser": "缺少本周原始反馈", "userAction": "提供反馈摘要",
            "destination": "原工作详情", "doneCriterion": "摘要可读且属于本工作",
            "resumePlan": "收到后继续整理", "targetRef": ref, "evidenceRefs": [],
        }
        with database.connect() as connection:
            connection.execute("update tasks set status='COMPLETED', output=? where task_id=?",
                               (source_for(fields), task_id))
    return database, ref, key, task_id, fields


def test_request_report_review_claim_and_result_exclusion(prepared):
    database, ref, key, task_id, fields = prepared
    with scope():
        router = ResponsibilityRoutingRuntime(database)
        callback = {"verification_status": "VERIFIED", "task_ref": task_id,
                    "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE}
        with pytest.raises(ResponsibilityRoutingError):
            router.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
                session_ref="session", request_fields=fields,
                callback={**callback, "verification_status": "UNVERIFIED"},
                source_output=source_for(fields))
        with pytest.raises(ResponsibilityRoutingError):
            router.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
                session_ref="session", request_fields=fields, callback=callback,
                source_output='{"status":"ACCEPTED"}')
        for invalid in ({**fields, "kind": ["LOCAL_INFORMATION"]},
                        {**fields, "userAction": ""},
                        {**fields, "targetRef": "foreign-work"}):
            with pytest.raises(ResponsibilityRoutingError):
                router.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
                    session_ref="session", request_fields=invalid, callback=callback,
                    source_output=source_for(fields))
        issued = router.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
            session_ref="session", request_fields=fields,
            callback=callback, source_output=source_for(fields))
        request = issued["request"]
        assert request["state"] == "WAITING_INPUT"
        work = RuntimeFoundation(database).get(ref)
        record = work["data"]["responsibilityRouting"]["executions"][key]
        assert record["status"] == "PARTIAL" and record["humanInputSource"] is True
        assert record["resultRef"] is None
        with pytest.raises(ResponsibilityRoutingError):
            router.route(ref, signal="CONTINUE")
        assert SharedWorkspaceProjection(database)._result(COMPANY, WORKSPACE, f"task:{task_id}", include_content=True) is None
        attention = ResultAttention(database)
        assert not any(item["source_ref"] == f"task:{task_id}" for item in attention.unseen_results(COMPANY))
        with pytest.raises(RuntimeScopeError):
            attention.detail(COMPANY, WORKSPACE, f"task:{task_id}")
        with pytest.raises(RuntimeScopeError):
            attention.mark_viewed(COMPANY, WORKSPACE, f"task:{task_id}", "arbitrary-version")
        projected = SharedWorkspaceProjection(database).general_workspace(COMPANY, WORKSPACE)
        assert projected["current_work"][0]["human_input"]["requestId"] == request["requestId"]
        assert f"task:{task_id}" not in projected["current_work"][0]["result_refs"]
        reported = router.report_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=1, submission_id="submission-1",
            kind="LOCAL_INFORMATION", local_text="本周有三项反馈", actor="ceo")
        assert reported["request"]["state"] == "LOCAL_REPORTED"
        duplicate_callback = router.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
            session_ref="session", request_fields=fields, callback=callback,
            source_output=source_for(fields))
        assert duplicate_callback["duplicate"] and duplicate_callback["request"]["state"] == "LOCAL_REPORTED"
        with pytest.raises(ResponsibilityRoutingError):
            router.finish_employee_execution(ref, execution_key=key, status="ACCEPTED",
                task_ref=task_id, session_ref="session")
        assert router.report_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=1, submission_id="submission-1",
            kind="LOCAL_INFORMATION", local_text="本周有三项反馈", actor="ceo")["duplicate"]
        with pytest.raises(ResponsibilityRoutingError):
            router.report_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=1, submission_id="submission-2",
                kind="LOCAL_INFORMATION", local_text="不同内容", actor="ceo")
        reviewed = router.review_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=2)
        assert reviewed["request"]["state"] == "READY"
        claimed = router.claim_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=3, submission_id="submission-1")
        assert claimed["executionKey"].endswith(":2")
        assert router.claim_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=3, submission_id="submission-1")["duplicate"]
        assert SharedWorkspaceProjection(database)._result(COMPANY, WORKSPACE, f"task:{task_id}", include_content=False) is None
        with database.connect() as connection:
            assert connection.execute("select count(*) from evolution_events where event_type='result.viewed'").fetchone()[0] == 0
            assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_external_report_unknown_and_direct_http_bypass(prepared):
    database, ref, key, task_id, fields = prepared
    fields["kind"] = "EXTERNAL_ACTION_REPORT"
    with scope():
        with database.connect() as connection:
            connection.execute("update tasks set output=? where task_id=?", (source_for(fields), task_id))
        request = ResponsibilityRoutingRuntime(database).finish_user_required_execution(
            ref, execution_key=key, task_ref=task_id, session_ref="session",
            request_fields=fields, callback={"verification_status": "VERIFIED", "task_ref": task_id,
                                             "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE},
            source_output=source_for(fields))["request"]
    app = FastAPI()

    @app.middleware("http")
    async def tenant(request: Request, call_next):
        with scope():
            return await call_next(request)

    async def forbidden_bridge(_):
        raise AssertionError("No Provider Task may be created")

    app.include_router(build_shared_workspace_router(database))
    app.include_router(build_team_operating_router(database, forbidden_bridge), prefix="/api/workspace/runtime/foundation")
    app.include_router(build_task_execution_control_router(
        TaskExecutionControlService(database, EvolutionEventLog(database)), object()))
    base = f"/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{ref}/human-input/{request['requestId']}"
    with TestClient(app) as client:
        bad = client.post(f"{base}/report", json={"revision": 1, "submission_id": "external-1",
            "kind": "EXTERNAL_ACTION_REPORT", "manual_source": "用户自述", "unexpected": True})
        assert bad.status_code == 422
        report = client.post(f"{base}/report", json={"revision": 1, "submission_id": "external-1",
            "kind": "EXTERNAL_ACTION_REPORT", "manual_source": "用户自述"})
        assert report.status_code == 200, report.text
        assert report.json()["request"]["state"] == "EXTERNAL_REPORTED_UNKNOWN"
        review = client.post(f"{base}/review", json={"revision": 2})
        assert review.status_code == 200 and review.json()["ready"] is False
        continuation = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/human-input/{request['requestId']}/continue",
            json={"revision": 2, "submission_id": "external-1"})
        assert continuation.status_code == 409
        direct = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute")
        assert direct.status_code == 422
        direct_route = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/route",
            json={"signal": "CONTINUE"})
        assert direct_route.status_code == 422
        task_state = client.get(f"/api/workspace/task-runs/{task_id}")
        assert task_state.status_code == 200
        assert task_state.json()["original_general_work"]["work_ref"] == ref
        blocked = client.post(f"/api/workspace/task-runs/{task_id}/resume", json={"resume_parameters": {}})
        assert blocked.status_code == 409
    with scope():
        stopped = ResponsibilityRoutingRuntime(database).cancel_work(ref, reason="CEO 停止")
        assert stopped["data"]["responsibilityRouting"]["humanInput"]["state"] == "INVALIDATED"
        with pytest.raises(ResponsibilityRoutingError):
            ResponsibilityRoutingRuntime(database).review_human_input(
                COMPANY, WORKSPACE, ref, request_id=request["requestId"], revision=2)


def test_consumed_general_limit_blocks_human_continuation_before_new_task(tmp_path, monkeypatch):
    database, ref, _ = limited_ready.__wrapped__(tmp_path, monkeypatch)
    with scope():
        task_id = limited_task_for(database, ref)
        work = RuntimeFoundation(database).get(ref)
        route = work["data"]["responsibilityRouting"]
        key = next(iter(route["executions"]))
        limited_fields = {"kind": "LOCAL_INFORMATION", "aiCompleted": "已梳理资料",
            "whyUser": "缺少摘要", "userAction": "提供摘要", "destination": "原工作",
            "doneCriterion": "摘要可读", "resumePlan": "继续分析", "targetRef": ref}
        with database.connect() as connection:
            connection.execute("update tasks set status='COMPLETED', output=? where task_id=?",
                               (source_for(limited_fields), task_id))
        issued = ResponsibilityRoutingRuntime(database).finish_user_required_execution(
            ref, execution_key=key, task_ref=task_id, session_ref="session",
            request_fields=limited_fields,
            callback={"verification_status": "VERIFIED", "task_ref": task_id,
                      "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE},
            source_output=source_for(limited_fields),
        )["request"]
        routing = ResponsibilityRoutingRuntime(database)
        reported = routing.report_human_input(COMPANY, WORKSPACE, ref,
            request_id=issued["requestId"], revision=1, submission_id="limited-submission",
            kind="LOCAL_INFORMATION", local_text="摘要", actor="ceo")["request"]
        ready = routing.review_human_input(COMPANY, WORKSPACE, ref,
            request_id=issued["requestId"], revision=reported["revision"])["request"]
        with database.connect() as connection:
            before = connection.execute("select count(*) from tasks").fetchone()[0]
        with pytest.raises(RuntimeScopeError, match="single execution"):
            GeneralWorkspaceDelivery(database).precheck_human_continuation(
                company_id=COMPANY, workspace_id=WORKSPACE, work_ref=ref,
                request_id=issued["requestId"], revision=ready["revision"],
                submission_id="limited-submission")
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == before == 1


def test_changed_assignment_invalidates_pending_request(prepared):
    database, ref, key, task_id, fields = prepared
    with scope():
        request = ResponsibilityRoutingRuntime(database).finish_user_required_execution(
            ref, execution_key=key, task_ref=task_id, session_ref="session",
            request_fields=fields, source_output=source_for(fields),
            callback={"verification_status": "VERIFIED", "task_ref": task_id,
                      "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE})["request"]
        with database.connect() as connection:
            row = connection.execute("select data_json from runtime_entities where entity_id=?",
                                     (request["assignmentRef"],)).fetchone()
            assignment = json.loads(row["data_json"])
            assignment["revision"] += 1
            connection.execute("update runtime_entities set data_json=? where entity_id=?",
                               (json.dumps(assignment), request["assignmentRef"]))
        with pytest.raises(ResponsibilityRoutingError, match="scope changed"):
            ResponsibilityRoutingRuntime(database).report_human_input(
                COMPANY, WORKSPACE, ref, request_id=request["requestId"], revision=1,
                submission_id="stale-assignment", kind="LOCAL_INFORMATION",
                local_text="摘要", actor="ceo")


def test_stored_source_contract_and_utf8_bounds(prepared):
    database, ref, key, task_id, fields = prepared
    callback = {"verification_status": "VERIFIED", "task_ref": task_id,
                "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE}
    routing = ResponsibilityRoutingRuntime(database)
    with scope():
        for invalid in (
            {"status": "ACCEPTED", "resultType": "general-business-result", "humanInput": fields},
            {"status": "USER_REQUIRED", "resultType": "other-result", "humanInput": fields},
            {"status": "USER_REQUIRED", "resultType": "general-business-result",
             "humanInput": {**fields, "verifiedExternalEffect": True}},
            {"status": "USER_REQUIRED", "resultType": "general-business-result",
             "humanInput": fields, "verifiedExternalEffect": True},
        ):
            stored = json.dumps(invalid, ensure_ascii=False)
            with database.connect() as connection:
                connection.execute("update tasks set output=? where task_id=?", (stored, task_id))
            with pytest.raises(ResponsibilityRoutingError):
                routing.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
                    session_ref="session", request_fields=invalid.get("humanInput", fields),
                    callback=callback, source_output=stored)
        multibyte = {**fields, "whyUser": "界" * 334}
        stored = source_for(multibyte)
        with database.connect() as connection:
            connection.execute("update tasks set output=? where task_id=?", (stored, task_id))
        with pytest.raises(ResponsibilityRoutingError, match="incomplete or unsafe"):
            routing.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
                session_ref="session", request_fields=multibyte, callback=callback,
                source_output=stored)
        boundary = {**fields, "whyUser": "界" * 333 + "a"}
        assert len(boundary["whyUser"].encode("utf-8")) == 1000
        stored = source_for(boundary)
        with database.connect() as connection:
            connection.execute("update tasks set output=? where task_id=?", (stored, task_id))
        request = routing.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
            session_ref="session", request_fields=boundary, callback=callback,
            source_output=stored)["request"]
        with pytest.raises(ResponsibilityRoutingError):
            routing.report_human_input(COMPANY, WORKSPACE, ref, request_id=request["requestId"],
                revision=1, submission_id="界", kind="LOCAL_INFORMATION",
                local_text="摘要", actor="ceo")
        with pytest.raises(ResponsibilityRoutingError):
            routing.report_human_input(COMPANY, WORKSPACE, ref, request_id=request["requestId"],
                revision=1, submission_id="utf8-bound", kind="LOCAL_INFORMATION",
                local_text="界" * 667, actor="ceo")


@pytest.mark.parametrize("phase", ["report", "review", "claim"])
def test_duplicate_actions_recheck_current_assignment(tmp_path, phase):
    database, ref, key, task_id, fields = prepared.__wrapped__(tmp_path)
    with scope():
        routing = ResponsibilityRoutingRuntime(database)
        request = routing.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
            session_ref="session", request_fields=fields, source_output=source_for(fields),
            callback={"verification_status": "VERIFIED", "task_ref": task_id,
                      "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE})["request"]
        reported = routing.report_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=1, submission_id="same-report",
            kind="LOCAL_INFORMATION", local_text="摘要", actor="ceo")["request"]
        if phase in {"review", "claim"}:
            ready = routing.review_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=reported["revision"])["request"]
        if phase == "claim":
            routing.claim_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=ready["revision"],
                submission_id="same-report")
        with database.connect() as connection:
            row = connection.execute("select data_json from runtime_entities where entity_id=?",
                                     (request["assignmentRef"],)).fetchone()
            assignment = json.loads(row["data_json"])
            assignment["revision"] += 1
            connection.execute("update runtime_entities set data_json=? where entity_id=?",
                               (json.dumps(assignment), request["assignmentRef"]))
        actions = {
            "report": lambda: routing.report_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=1, submission_id="same-report",
                kind="LOCAL_INFORMATION", local_text="摘要", actor="ceo"),
            "review": lambda: routing.review_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=2),
            "claim": lambda: routing.claim_human_input(COMPANY, WORKSPACE, ref,
                request_id=request["requestId"], revision=3, submission_id="same-report"),
        }
        with pytest.raises(ResponsibilityRoutingError):
            actions[phase]()


@pytest.mark.parametrize("run_outcome", ["exception", "unverified_raw", "verified_failure"])
def test_unknown_continuation_run_keeps_bound_task_without_replay(prepared, run_outcome):
    database, ref, key, task_id, fields = prepared
    with scope():
        EmployeeExecutionIdentity(database).bind(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE,
            employee_capability_binding_ref="binding-general",
        )
        runtime = ResponsibilityRoutingRuntime(database)
        request = runtime.finish_user_required_execution(ref, execution_key=key, task_ref=task_id,
            session_ref="session", request_fields=fields, source_output=source_for(fields),
            callback={"verification_status": "VERIFIED", "task_ref": task_id,
                      "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE})["request"]
        runtime.report_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=1, submission_id="unknown-run",
            kind="LOCAL_INFORMATION", local_text="补充事实", actor="ceo")
        runtime.review_human_input(COMPANY, WORKSPACE, ref,
            request_id=request["requestId"], revision=2)
    calls = []

    async def bridge(command):
        calls.append(command["mode"])
        if command["mode"] == "submit":
            with scope():
                task = ResultStore(database).create_task(
                    "原工作续接", company_id=COMPANY, workspace_id=WORKSPACE,
                    work_ref=ref, execution_ref=command["execution_key"],
                    scope_type="WORKSPACE", scope_ref=WORKSPACE,
                    capability_source="tenant_private", capability_type="agent",
                    capability_id="agent.general.local", employee_id=EMPLOYEE,
                )
            return {"task_ref": task["task_id"]}
        if run_outcome == "exception":
            raise RuntimeError("synthetic unknown run outcome")
        if run_outcome == "unverified_raw":
            return {"task_ref": command["task_ref"], "task_status": "INIT", "output": "",
                    "execution_binding": {"callbackProvenance": {
                        "verification_status": "UNVERIFIED", "task_ref": command["task_ref"],
                        "task_status": "INIT", "callback_actor_ref": EMPLOYEE}}}
        with scope():
            with database.connect() as connection:
                connection.execute("update tasks set status='FAILED', error='synthetic provider failure' where task_id=?",
                                   (command["task_ref"],))
        return {"task_ref": command["task_ref"], "task_status": "FAILED", "output": "",
                "execution_binding": {"callbackProvenance": {
                    "verification_status": "VERIFIED", "task_ref": command["task_ref"],
                    "task_status": "FAILED", "callback_actor_ref": EMPLOYEE}}}

    app = FastAPI()

    @app.middleware("http")
    async def tenant(request: Request, call_next):
        with scope():
            return await call_next(request)

    app.include_router(build_team_operating_router(database, bridge), prefix="/api/workspace/runtime/foundation")
    url = f"/api/workspace/runtime/foundation/team-operating/works/{ref}/human-input/{request['requestId']}/continue"
    with TestClient(app) as client:
        first = client.post(url, json={"revision": 3, "submission_id": "unknown-run"})
        assert first.status_code == 200, first.text
        second = client.post(url, json={"revision": 3, "submission_id": "unknown-run"})
        assert second.status_code == 200 and second.json()["duplicate"] is True
        assert second.json()["actionable"] is False
    with scope():
        work = RuntimeFoundation(database).get(ref)
        continuation = work["data"]["responsibilityRouting"]["humanInput"]
        execution = work["data"]["responsibilityRouting"]["executions"][continuation["continuationKey"]]
        expected_status = "FAILED" if run_outcome == "verified_failure" else "RUNNING"
        assert continuation["state"] == "CLAIMED" and execution["status"] == expected_status
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks where work_ref=?", (ref,)).fetchone()[0] == 2
    assert calls == ["submit", "run"]


def test_verified_user_required_callback_enters_original_work_without_result(tmp_path):
    database = seed(tmp_path / "callback.sqlite")
    add_team(database)
    with scope():
        ref = GeneralWorkspaceDelivery(database).create_work(
            company_id=COMPANY, workspace_id=WORKSPACE, problem="整理反馈",
            expected_result="形成建议", constraints=[], references=[], idempotency_key="callback-work",
        )["work"]["entity_id"]
        EmployeeExecutionIdentity(database).bind(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=EMPLOYEE, company_employee_ref=EMPLOYEE,
            employee_capability_binding_ref="binding-general",
        )
    calls = []

    async def bridge(command):
        calls.append(command["mode"])
        if command["mode"] == "submit":
            with scope():
                task = ResultStore(database).create_task(
                    "整理反馈", company_id=COMPANY, workspace_id=WORKSPACE,
                    work_ref=ref, execution_ref=command["execution_key"],
                    scope_type="WORKSPACE", scope_ref=WORKSPACE,
                    capability_source="tenant_private", capability_type="agent",
                    capability_id="agent.general.local", employee_id=EMPLOYEE,
                )
            return {"task_ref": task["task_id"]}
        output = ({"status": "USER_REQUIRED", "resultType": "general-business-result",
                   "humanInput": {"kind": "LOCAL_INFORMATION", "aiCompleted": "已看现有资料",
                       "whyUser": "缺少摘要", "userAction": "提供摘要", "destination": "原工作",
                       "doneCriterion": "摘要可读", "resumePlan": "继续分析", "targetRef": ref}}
                  if calls.count("run") == 1 else
                  {"status": "ACCEPTED", "resultType": "general-business-result", "summary": "反馈建议已形成", "problem": ""})
        with scope():
            with database.connect() as connection:
                connection.execute("update tasks set status='COMPLETED', output=? where task_id=?",
                                   (json.dumps(output, ensure_ascii=False), command["task_ref"]))
        return {"task_status": "COMPLETED", "output": json.dumps(output, ensure_ascii=False),
                "session_ref": "synthetic-session", "artifact_refs": [],
                "execution_binding": {"callbackProvenance": {
                    "verification_status": "VERIFIED", "task_ref": command["task_ref"],
                    "task_status": "COMPLETED", "callback_actor_ref": EMPLOYEE}}}

    app = FastAPI()

    @app.middleware("http")
    async def tenant(request: Request, call_next):
        with scope():
            return await call_next(request)

    app.include_router(build_team_operating_router(database, bridge), prefix="/api/workspace/runtime/foundation")
    app.include_router(build_shared_workspace_router(database), prefix="/api/workspace/runtime/foundation")
    with TestClient(app) as client:
        response = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute")
        assert response.status_code == 200, response.text
        route = response.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "WAITING" and route["humanInput"]["state"] == "WAITING_INPUT"
        assert route["resultRefs"] == []
        task_id = route["humanInput"]["sourceTaskRef"]
        assert SharedWorkspaceProjection(database)._result(COMPANY, WORKSPACE, f"task:{task_id}", include_content=True) is None
        blocked = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/execute")
        assert blocked.status_code == 422
        base = f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{WORKSPACE}/shared/general/works/{ref}/human-input/{route['humanInput']['requestId']}"
        reported = client.post(base + "/report", json={"revision": 1, "submission_id": "callback-submission",
            "kind": "LOCAL_INFORMATION", "local_text": "客户反馈摘要"})
        assert reported.status_code == 200, reported.text
        reviewed = client.post(base + "/review", json={"revision": 2})
        assert reviewed.status_code == 200, reviewed.text
        continued = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/human-input/{route['humanInput']['requestId']}/continue",
            json={"revision": 3, "submission_id": "callback-submission"})
        assert continued.status_code == 200, continued.text
        final_route = continued.json()["work"]["data"]["responsibilityRouting"]
        assert final_route["status"] == "COMPLETED"
        assert final_route["humanInput"]["state"] == "CLOSED"
        assert f"task:{task_id}" not in final_route["resultRefs"]
        assert len(final_route["resultRefs"]) == 1
        historical = client.post(f"/api/workspace/runtime/foundation/team-operating/works/{ref}/human-input/{route['humanInput']['requestId']}/continue",
            json={"revision": 3, "submission_id": "callback-submission"})
        assert historical.status_code == 200
        assert historical.json()["historical"] is True and historical.json()["actionable"] is False
        assert calls == ["submit", "run", "submit", "run"]
