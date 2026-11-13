from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.result_store import ResultStore
from app.runtime.autonomous_operating import AutonomousOperatingControl
from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
from app.runtime.foundation import RuntimeFoundation
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase3a import evaluation_contract
from backend.tests.test_autonomous_operating_primary_two_cycle_e2e import (
    COMPANY,
    CEO,
    PROJECT,
    TENANT,
    WORKFLOW_KEY,
    approved_plan,
    setup_rd_runtime,
)

def _agent_followup_fixture(tmp_path):
    client, database, _, series, cycle, _, employee_ref, reviewer = _setup(tmp_path / "agent-followup.sqlite")
    runtime = CanonicalChildWorkRuntime(database)
    foundation = RuntimeFoundation(database)
    contract = {"problem": "original", "expectedResult": "result",
        "agentBinding": {"bindingRef": "fixture-binding", "employeeRef": employee_ref},
        "agentSource": {"input": {"kind": "content-growth", "content_ref": "fixture-content"},
                        "snapshot": {"conversation_id": "fixture-permanent-conversation"}}}
    with database.connect() as con:
        data = dict(foundation.get(cycle["entity_id"])["data"], contract=contract)
        con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
            (json.dumps(data), TENANT, cycle["entity_id"]))
    work = runtime.create_work(cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"],
        release_key="original-agent")
    parent = _complete(runtime, database, work["entity_id"], employee_ref, "agent-result")
    request = dict(release_key="explicit-followup", target_assignment_ref=series["owner_ref"],
        accepted_result_ref=parent["data"]["resultRefs"][0], reason="user requested follow-up",
        followup_contract={**contract, "problem": "new explicit request"})
    return client, database, runtime, foundation, cycle, parent, reviewer, request


@pytest.mark.parametrize("failure", ["WAITING_CEO", "PAUSED", "REVIEWING", "revision", "employee", "object", "conversation", "successor"])
def test_explicit_followup_rejects_changed_authority_atomically(tmp_path, failure):
    with _scope():
        client, database, runtime, foundation, cycle, parent, reviewer, request = _agent_followup_fixture(tmp_path)
        try:
            with database.connect() as con:
                if failure in {"WAITING_CEO", "PAUSED", "REVIEWING", "successor"}:
                    con.execute("update runtime_entities set lifecycle_status=? where tenant_id=? and entity_id=?",
                        ("CLOSED" if failure == "successor" else failure, TENANT, cycle["entity_id"]))
                if failure in {"revision", "employee"}:
                    assignment = foundation.get(request["target_assignment_ref"])
                    data = deepcopy(assignment["data"])
                    if failure == "revision":
                        data["revision"] += 1
                    else:
                        data["employeeRef"] = reviewer["data"]["employeeRef"]
                    con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                        (json.dumps(data), TENANT, assignment["entity_id"]))
                if failure == "successor":
                    runtime._insert_link(con, foundation.get(cycle["entity_id"]), "HAS_SUCCESSOR_CYCLE",
                        "other-previously-linked-cycle", "2026-10-29T00:00:00Z")
                before = con.execute("select count(*) from runtime_entities where tenant_id=?", (TENANT,)).fetchone()[0]
            if failure == "object":
                request["followup_contract"] = deepcopy(request["followup_contract"])
                request["followup_contract"]["agentSource"]["input"]["content_ref"] = "other-content"
            if failure == "conversation":
                request["followup_contract"] = deepcopy(request["followup_contract"])
                request["followup_contract"]["agentSource"]["snapshot"]["conversation_id"] = "other-conversation"
            with pytest.raises(ChildWorkError):
                runtime.release_next_work(parent["entity_id"], **request)
            with database.connect() as con:
                assert con.execute("select count(*) from runtime_entities where tenant_id=?", (TENANT,)).fetchone()[0] == before
                assert not con.execute("select 1 from runtime_links where tenant_id=? and source_id=? and relation='HAS_SUCCESSOR_WORK'",
                    (TENANT, parent["entity_id"])).fetchone()
            assert foundation.get(parent["entity_id"]) == parent
        finally:
            client.close()


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "canonical-child-work.sqlite"
    for name in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"):
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def _scope():
    return TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test")


def _setup(path):
    client = TestClient(create_app(str(path)))
    database, control, series, cycle, workspace_id, employee_ref = setup_rd_runtime(path, client)
    with _scope():
        foundation = RuntimeFoundation(database)
        role = foundation.create(
            "ROLE_SLOT", entity_id="role-child-reviewer", company_id=COMPANY,
            workspace_id=workspace_id, lifecycle_status="ASSIGNED",
            data={"name": "结果复核", "responsibility": "复核前序结果"},
        )
        reviewer = foundation.create(
            "AI_EMPLOYEE", entity_id="employee-child-reviewer", company_id=COMPANY,
            workspace_id=workspace_id, lifecycle_status="AVAILABLE",
            data={"name": "复核员工", "responsibility": "复核前序结果"},
        )
        reviewer_assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY, scope_type="WORKSPACE", scope_ref=workspace_id,
            workspace_id=workspace_id, employee_ref=reviewer["entity_id"], role_ref=role["entity_id"],
            responsibility_key="review-result", responsibility="复核前序结果与证据",
            input_contract={"requiredRefs": ["predecessor-result"]},
            output_contract={"requiresResult": True},
        )
        control.materialize_cycle_work(
            series_id=series["entity_id"], cycle_id=cycle["entity_id"], workflow_key=WORKFLOW_KEY,
            plan=approved_plan(
                "rd-plan-v1",
                {"work": "验证多项独立工作", "acceptance": "每项工作有独立结果与证据"},
            ),
        )
    return client, database, control, series, cycle, workspace_id, employee_ref, reviewer_assignment


def _complete(runtime, database, work_id: str, employee_ref: str, label: str):
    runtime.transition_work(work_id, "READY", actor="SYSTEM")
    runtime.transition_work(work_id, "ACTIVE", actor=employee_ref)
    store = ResultStore(database)
    task = store.create_task(label, company_id=COMPANY, project_id=PROJECT, employee_id=employee_ref)
    task = store.transition(task["task_id"], "COMPLETED", {"output": f"{label} completed"})
    artifact = store.list_artifacts(task_id=task["task_id"])[0]
    foundation = RuntimeFoundation(database)
    evidence = foundation.create(
        "EVIDENCE", company_id=COMPANY, workspace_id=runtime.get_work(work_id)["workspace_id"],
        parent_id=work_id, owner_ref=employee_ref, lifecycle_status="CURRENT",
        verification_status="VERIFIED", evidence_condition="CURRENT",
        data={"summary": f"{label} verified", "taskRef": task["task_id"]},
    )
    result_refs = [f"task:{task['task_id']}"]
    evidence_refs = [evidence["entity_id"]]
    acceptance = foundation.create(
        "ACCEPTANCE", company_id=COMPANY, workspace_id=evidence["workspace_id"],
        parent_id=work_id, owner_ref=CEO,
        data={"resultRefs": result_refs, "evidenceRefs": evidence_refs},
    )
    foundation.transition(acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept")
    foundation.transition(acceptance["entity_id"], "CLOSED", actor="SYSTEM", trigger="close")
    return runtime.complete_work(
        work_id, result_refs=result_refs, artifact_refs=[artifact["artifact_id"]],
        evidence_refs=evidence_refs, acceptance_refs=[acceptance["entity_id"]],
    )


def test_multiple_child_work_closes_and_evaluates_one_cycle_after_restart(tmp_path):
    path = tmp_path / "multi-work.sqlite"
    client, database, control, series, cycle, _, employee_ref, reviewer_assignment = _setup(path)
    try:
        with _scope():
            runtime = CanonicalChildWorkRuntime(database)
            first = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"],
                release_key="research", input_refs=["goal:multi-work"],
            )
            first = _complete(runtime, database, first["entity_id"], employee_ref, "research")
            first_snapshot = json.dumps(first["data"], sort_keys=True)
            assert runtime.complete_work(
                first["entity_id"], result_refs=first["data"]["resultRefs"],
                artifact_refs=first["data"]["artifactRefs"], evidence_refs=first["data"]["evidenceRefs"],
                acceptance_refs=first["data"]["acceptanceRefs"],
            )["entity_id"] == first["entity_id"]
            released = runtime.release_next_work(
                first["entity_id"], release_key="review", target_assignment_ref=reviewer_assignment["entity_id"],
                accepted_result_ref=first["data"]["resultRefs"][0], reason="前序结果已验收，转交复核",
            )
            second = _complete(
                runtime, database, released["work"]["entity_id"],
                reviewer_assignment["data"]["employeeRef"], "review",
            )
            assert json.dumps(runtime.get_work(first["entity_id"])["data"], sort_keys=True) == first_snapshot
            aggregate = runtime.aggregate_cycle(cycle["entity_id"])
            assert aggregate["mode"] == "CHILD_WORK"
            assert set(aggregate["workRefs"]) == {first["entity_id"], second["entity_id"]}
            assert len(set(aggregate["resultRefs"])) == 2
            with database.connect() as connection:
                assert connection.execute(
                    "select target_id from runtime_links where tenant_id=? and source_id=? "
                    "and relation='HAS_SUCCESSOR_WORK'",
                    (TENANT, first["entity_id"]),
                ).fetchone()["target_id"] == second["entity_id"]
                assert connection.execute(
                    "select target_id from runtime_links where tenant_id=? and source_id=? "
                    "and relation='HAS_PREDECESSOR_WORK'",
                    (TENANT, second["entity_id"]),
                ).fetchone()["target_id"] == first["entity_id"]
            waiting = control.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle["entity_id"])
            assert waiting["lifecycle_status"] == "WAITING_CEO"
            closed = control.accept_and_close_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"], reason="两项工作均已验收",
            )
            evidence_ref = closed["data"]["evidenceRefs"][0]
            evaluation = control.evaluate_closed_cycle(
                series_id=series["entity_id"], cycle_id=cycle["entity_id"],
                contract=evaluation_contract("child-work-evaluation-v1"), outcome="SUCCESS",
                observed_facts=[{"name": "multi_work_complete", "value": 2, "sourceRef": evidence_ref}],
                comparison={"expected": 2, "observed": 2}, confidence="HIGH", sufficiency="SUFFICIENT",
            )
            assert evaluation["workRefs"] == aggregate["workRefs"]
            assert evaluation["aggregationHash"] == aggregate["aggregationHash"]

        reopened = Database(str(path))
        reopened.initialize()
        with _scope():
            persisted = CanonicalChildWorkRuntime(reopened).aggregate_cycle(cycle["entity_id"])
            assert persisted["aggregationHash"] == aggregate["aggregationHash"]
            assert RuntimeFoundation(reopened).get(cycle["entity_id"])["lifecycle_status"] == "CLOSED"
            with reopened.connect() as connection:
                assert connection.execute(
                    "select count(*) from runtime_entities where tenant_id=? and entity_type='CYCLE'",
                    (TENANT,),
                ).fetchone()[0] == 1
                assert connection.execute(
                    "select count(*) from runtime_entities where tenant_id=? and entity_type='LEARNING'",
                    (TENANT,),
                ).fetchone()[0] == 0
    finally:
        client.close()


def test_release_is_atomic_idempotent_and_rejects_conflict(tmp_path):
    path = tmp_path / "release.sqlite"
    client, database, _, series, cycle, _, employee_ref, reviewer_assignment = _setup(path)
    try:
        with _scope():
            runtime = CanonicalChildWorkRuntime(database)
            first = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="first",
            )
            first = _complete(runtime, database, first["entity_id"], employee_ref, "first")

        def release():
            with _scope():
                return CanonicalChildWorkRuntime(Database(str(path))).release_next_work(
                    first["entity_id"], release_key="next",
                    target_assignment_ref=reviewer_assignment["entity_id"],
                    accepted_result_ref=first["data"]["resultRefs"][0], reason="atomic release",
                )

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = [future.result() for future in (pool.submit(release), pool.submit(release))]
        assert len({item["work"]["entity_id"] for item in results}) == 1
        assert len({item["handoff"]["entity_id"] for item in results}) == 1
        with _scope():
            with pytest.raises(ChildWorkError, match="different target|conflicts"):
                CanonicalChildWorkRuntime(database).release_next_work(
                    first["entity_id"], release_key="next", target_assignment_ref=series["owner_ref"],
                    accepted_result_ref=first["data"]["resultRefs"][0], reason="conflicting replay",
                )
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='HANDOFF'",
                (TENANT,),
            ).fetchone()[0] == 1
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='WORK'",
                (TENANT,),
            ).fetchone()[0] == 2
    finally:
        client.close()


def test_interrupted_release_rolls_back_handoff_and_child(tmp_path):
    path = tmp_path / "rollback.sqlite"
    client, database, _, series, cycle, _, employee_ref, reviewer_assignment = _setup(path)
    try:
        with _scope():
            runtime = CanonicalChildWorkRuntime(database)
            first = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="first",
            )
            first = _complete(runtime, database, first["entity_id"], employee_ref, "first")
        with database.connect() as connection:
            connection.execute(
                "create trigger abort_successor_work before insert on runtime_entities "
                f"when new.entity_type='WORK' and new.parent_id='{cycle['entity_id']}' "
                "begin select raise(abort, 'injected'); end",
            )
        runtime = CanonicalChildWorkRuntime(Database(str(path)))
        with _scope(), pytest.raises(Exception, match="injected"):
            runtime.release_next_work(
                first["entity_id"], release_key="next", target_assignment_ref=reviewer_assignment["entity_id"],
                accepted_result_ref=first["data"]["resultRefs"][0], reason="rollback proof",
            )
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='HANDOFF'",
                (TENANT,),
            ).fetchone()[0] == 0
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='WORK'",
                (TENANT,),
            ).fetchone()[0] == 1
            connection.execute("drop trigger abort_successor_work")
        with _scope():
            assert runtime.release_next_work(
                first["entity_id"], release_key="next", target_assignment_ref=reviewer_assignment["entity_id"],
                accepted_result_ref=first["data"]["resultRefs"][0], reason="rollback proof",
            )["duplicate"] is False
    finally:
        client.close()


def test_work_completion_and_scope_fail_closed(tmp_path):
    path = tmp_path / "failure.sqlite"
    client, database, _, series, cycle, _, _, _ = _setup(path)
    try:
        with _scope():
            runtime = CanonicalChildWorkRuntime(database)
            work = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="incomplete",
            )
            runtime.transition_work(work["entity_id"], "READY", actor="SYSTEM")
            runtime.transition_work(work["entity_id"], "ACTIVE", actor="SYSTEM")
            with pytest.raises(ChildWorkError, match="requires Result"):
                runtime.complete_work(
                    work["entity_id"], result_refs=[], artifact_refs=[], evidence_refs=[], acceptance_refs=[],
                )
            task = ResultStore(database).create_task("invalid acceptance", company_id=COMPANY)
            task = ResultStore(database).transition(task["task_id"], "COMPLETED", {"output": "result"})
            evidence = RuntimeFoundation(database).create(
                "EVIDENCE", company_id=COMPANY, workspace_id=work["workspace_id"], parent_id=work["entity_id"],
                verification_status="VERIFIED", evidence_condition="CURRENT",
            )
            pending = RuntimeFoundation(database).create(
                "ACCEPTANCE", company_id=COMPANY, workspace_id=work["workspace_id"], parent_id=work["entity_id"],
                data={"resultRefs": [f"task:{task['task_id']}"], "evidenceRefs": [evidence["entity_id"]]},
            )
            with pytest.raises(ChildWorkError, match="Acceptance"):
                runtime.complete_work(
                    work["entity_id"], result_refs=[f"task:{task['task_id']}"], artifact_refs=[],
                    evidence_refs=[evidence["entity_id"]], acceptance_refs=[pending["entity_id"]],
                )
            with pytest.raises(ChildWorkError, match="accepted parent"):
                runtime.release_next_work(
                    work["entity_id"], release_key="invalid-predecessor", target_assignment_ref=series["owner_ref"],
                    accepted_result_ref=f"task:{task['task_id']}", reason="must not release",
                )
            with pytest.raises(ChildWorkError, match="not complete"):
                runtime.aggregate_cycle(cycle["entity_id"])
        with TenantContext.scope("other-tenant", company_id=COMPANY, ceo_id=CEO, role="test"):
            with pytest.raises(KeyError):
                CanonicalChildWorkRuntime(database).get_work(work["entity_id"])
    finally:
        client.close()


def test_identity_assignment_and_parent_failure_matrix(tmp_path):
    path = tmp_path / "identity-scope.sqlite"
    client, database, _, series, cycle, workspace_id, employee_ref, reviewer_assignment = _setup(path)
    try:
        with _scope():
            foundation = RuntimeFoundation(database)
            second_role = foundation.create(
                "ROLE_SLOT", entity_id="role-same-employee-second", company_id=COMPANY,
                workspace_id=workspace_id, lifecycle_status="ASSIGNED",
            )
            same_employee_assignment = ResponsibilityRoutingRuntime(database).create_assignment(
                company_id=COMPANY, scope_type="WORKSPACE", scope_ref=workspace_id,
                workspace_id=workspace_id, role_ref=second_role["entity_id"], employee_ref=employee_ref,
                responsibility_key="same-employee-second", responsibility="同一员工的另一项明确责任",
            )
            runtime = CanonicalChildWorkRuntime(database)
            first = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="identity-a",
            )
            assert runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="identity-a",
            )["entity_id"] == first["entity_id"]
            second = runtime.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=same_employee_assignment["entity_id"],
                release_key="identity-b",
            )
            assert first["entity_id"] != second["entity_id"]
            assert first["data"]["holderEmployeeRef"] == second["data"]["holderEmployeeRef"] == employee_ref
            assert first["data"]["responsibilityAssignmentRef"] != second["data"]["responsibilityAssignmentRef"]
            with pytest.raises(ChildWorkError, match="conflicts"):
                runtime.create_work(
                    cycle_id=cycle["entity_id"], assignment_ref=reviewer_assignment["entity_id"],
                    release_key="identity-a",
                )
            with pytest.raises(ChildWorkError, match="not CYCLE"):
                runtime.create_work(
                    cycle_id=series["entity_id"], assignment_ref=series["owner_ref"], release_key="bad-parent",
                )
            with pytest.raises(KeyError):
                runtime.create_work(
                    cycle_id=cycle["entity_id"], assignment_ref="missing-assignment", release_key="missing",
                )

        with database.connect() as connection:
            row = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and entity_id=?",
                (TENANT, reviewer_assignment["entity_id"]),
            ).fetchone()
            bad_scope = json.loads(row["data_json"])
            missing_employee = {**bad_scope, "employeeRef": "missing-employee"}
            connection.execute(
                "update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (json.dumps(missing_employee), TENANT, reviewer_assignment["entity_id"]),
            )
        with _scope(), pytest.raises(KeyError):
            CanonicalChildWorkRuntime(database).create_work(
                cycle_id=cycle["entity_id"], assignment_ref=reviewer_assignment["entity_id"],
                release_key="missing-employee",
            )
        with database.connect() as connection:
            bad_scope["scopeRef"] = "other-workspace"
            connection.execute(
                "update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (json.dumps(bad_scope), TENANT, reviewer_assignment["entity_id"]),
            )
        with _scope(), pytest.raises(ChildWorkError, match="outside the parent Cycle scope"):
            CanonicalChildWorkRuntime(database).create_work(
                cycle_id=cycle["entity_id"], assignment_ref=reviewer_assignment["entity_id"],
                release_key="cross-workspace",
            )
    finally:
        client.close()


def test_leader_failed_and_unknown_calls_keep_shared_ceiling_and_revision_fence(tmp_path):
    from backend.tests.test_team_operating_real_employee_e2e import (
        _leader_synthetic_setup, LeaderSyntheticProvider, TENANT as tenant, COMPANY as company,
        WORKSPACE as workspace, HEADERS,
    )
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-budget.sqlite", LeaderSyntheticProvider())
    runtime = CanonicalChildWorkRuntime(database)
    routing = ResponsibilityRoutingRuntime(database)
    store = ResultStore(database)
    with TenantContext.scope(tenant, company_id=company, ceo_id=HEADERS["X-Ceo-Id"], role="owner"):
        root = runtime.create_cycle_work(company_id=company, workspace_id=workspace, scope_type="WORKSPACE",
            scope_ref=workspace, assignment_ref=assignments[0]["entity_id"], release_key="budget",
            contract={"problem": "budget test", "expectedResult": "bounded calls"})["work"]
        ref = root["entity_id"]
        routing.start_work(ref, scope_type="WORKSPACE", scope_ref=workspace, workflow_key="leader-delegation")
        runtime.transition_work(ref, "READY", actor="SYSTEM")
        runtime.transition_work(ref, "ACTIVE", actor="SYSTEM")
        for index in range(9):
            key = f"leader:plan:synthetic-{index}"
            routing.begin_employee_execution(ref, execution_key=key, assignment_ref=assignments[0]["entity_id"])
            task = store.create_task("synthetic budget attempt", company_id=company, workspace_id=workspace,
                scope_type="WORKSPACE", scope_ref=workspace, work_ref=ref, execution_ref=key,
                employee_id=assignments[0]["data"]["employeeRef"], capability_source="tenant_private",
                capability_type="model", capability_id="model.leader.synthetic")
            store.transition(task["task_id"], "RUNNING")
            routing.attach_provider_task(ref, execution_key=key, task_ref=task["task_id"])
            if index == 8:
                with pytest.raises(ChildWorkError, match="budget exhausted"):
                    runtime.reserve_leader_call(task["task_id"])
                break
            assert runtime.reserve_leader_call(task["task_id"])
            with pytest.raises(ChildWorkError, match="already reserved"):
                runtime.reserve_leader_call(task["task_id"])
            routing.finish_employee_execution(ref, execution_key=key, status="FAILED", task_ref=task["task_id"],
                session_ref="", result_summary="synthetic outcome UNKNOWN; no refund")
            routing.route(ref, signal="CONTINUE")
        with database.connect() as con:
            current = RuntimeFoundation(database).get(assignments[0]["entity_id"])
            data = dict(current["data"], revision=current["data"]["revision"] + 1)
            con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (json.dumps(data), tenant, current["entity_id"]))
        with pytest.raises(ChildWorkError, match="snapshot changed"):
            runtime.reserve_leader_call(task["task_id"])
        root = RuntimeFoundation(database).get(ref)
        assert sum(bool(r.get("providerCallReserved")) for r in root["data"]["responsibilityRouting"]["executions"].values()) == 8


@pytest.mark.parametrize("open_human", [False, True])
def test_completion_closes_route_and_replays_without_new_history(tmp_path, open_human):
    client, database, _, series, cycle, _, employee, _ = _setup(tmp_path / "route-completion.sqlite")
    try:
        with _scope():
            runtime = CanonicalChildWorkRuntime(database)
            work = runtime.create_work(cycle_id=cycle["entity_id"], assignment_ref=series["owner_ref"], release_key="route-completion")
            with database.connect() as con:
                data = dict(work["data"], responsibilityRouting={"status": "ACTIVE", "currentExecutorRef": employee,
                    "executions": {"original": {"taskRef": "original-task"}}, "resultRefs": ["result:earlier"],
                    **({"humanInput": {"state": "OPEN"}} if open_human else {})})
                con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                    (json.dumps(data), TENANT, work["entity_id"]))
            if open_human:
                with pytest.raises(ChildWorkError, match="open Human Input"):
                    _complete(runtime, database, work["entity_id"], employee, "route-result")
                retained = runtime.get_work(work["entity_id"])
                assert retained["lifecycle_status"] == "ACTIVE"
                assert retained["data"]["responsibilityRouting"] == data["responsibilityRouting"]
                assert not retained["data"].get("acceptanceRefs")
                return
            done = _complete(runtime, database, work["entity_id"], employee, "route-result")
            route = done["data"]["responsibilityRouting"]
            assert route["status"] == "COMPLETED" and route["currentExecutorRef"] is None
            assert route["executions"] == {"original": {"taskRef": "original-task"}}
            assert route["resultRefs"] == ["result:earlier", *done["data"]["resultRefs"]]
            replay = runtime.complete_work(work["entity_id"], result_refs=done["data"]["resultRefs"],
                artifact_refs=done["data"]["artifactRefs"], evidence_refs=done["data"]["evidenceRefs"], acceptance_refs=done["data"]["acceptanceRefs"])
            assert replay == done
    finally:
        client.close()
