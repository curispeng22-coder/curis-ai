from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime.autonomous_operating import AutonomousControlError, AutonomousOperatingControl
from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
from app.runtime.foundation import RuntimeFoundation
from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_cross_domain_xhs import (
    BUSINESS,
    COMPANY,
    CEO,
    HEADERS,
    PREFIX,
    TENANT,
    WORKFLOW,
    XHSProvider,
    evaluation_contract,
    plan,
    setup,
)


RESEARCH_WORKFLOW = "xhs-canonical-research-work"
CONTENT_WORKFLOW = "xhs-canonical-content-work"


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    db_file = tmp_path / "cross-surface-multi-work.sqlite"
    for name in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"):
        monkeypatch.setenv(name, str(db_file))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def _scope(tenant_id: str = TENANT):
    return TenantContext.scope(tenant_id, company_id=COMPANY, ceo_id=CEO, role="test")


def _assignments(database: Database) -> dict[str, dict]:
    with database.connect() as connection:
        rows = connection.execute(
            "select * from runtime_entities where tenant_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT'",
            (TENANT,),
        ).fetchall()
    values = []
    for row in rows:
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        values.append(item)
    return {item["data"]["responsibilityKey"]: item for item in values}


def _publish_single_responsibility(client: TestClient, state: dict, assignment: dict, workflow_key: str, result_type: str):
    data = assignment["data"]
    response = client.post(
        f"{PREFIX}/definitions/publish",
        headers=HEADERS,
        json={
            "company_id": COMPANY,
            "scope_type": "WORKSPACE",
            "scope_ref": state["workspace_id"],
            "workspace_id": state["workspace_id"],
            "workflow_key": workflow_key,
            "roles": [{
                "responsibility_key": data["responsibilityKey"],
                "role_name": data["responsibility"],
                "employee_ref": data["employeeRef"],
                "role_ref": data["roleRef"],
                "assignment_ref": assignment["entity_id"],
                "responsibility": data["responsibility"],
                "input_contract": data["inputContract"],
                "output_contract": {"requiresResult": True, "resultType": result_type},
            }],
            "default_flow": [data["responsibilityKey"]],
        },
    )
    assert response.status_code == 200, response.text


def _prepare(path, client: TestClient, provider: XHSProvider):
    state = setup(path, client, provider)
    assignments = _assignments(state["database"])
    _publish_single_responsibility(
        client, state, assignments["xhs-research"], RESEARCH_WORKFLOW, "xhs-research-brief",
    )
    _publish_single_responsibility(
        client, state, assignments["xhs-copy"], CONTENT_WORKFLOW, "xhs-publish-package",
    )
    assignments = _assignments(state["database"])
    with _scope():
        state["control"].materialize_cycle_work(
            series_id=state["series"]["entity_id"], cycle_id=state["cycle"]["entity_id"],
            workflow_key=WORKFLOW, plan=plan(state),
        )
    return state, assignments


def _execute_work(client: TestClient, state: dict, work: dict, assignment: dict, workflow_key: str):
    database = state["database"]
    with _scope():
        routing = ResponsibilityRoutingRuntime(database)
        routed = routing.start_work(
            work["entity_id"], scope_type="WORKSPACE", scope_ref=state["workspace_id"],
            workflow_key=workflow_key,
        )
        assert routed["data"]["responsibilityRouting"]["currentAssignmentRef"] == assignment["entity_id"]
        child = CanonicalChildWorkRuntime(database)
        child.transition_work(work["entity_id"], "READY", actor="SYSTEM")
        child.transition_work(work["entity_id"], "ACTIVE", actor=assignment["data"]["employeeRef"])
    response = client.post(f"{PREFIX}/works/{work['entity_id']}/execute", headers=HEADERS)
    assert response.status_code == 200, response.text
    route = response.json()["work"]["data"]["responsibilityRouting"]
    assert route["status"] == "COMPLETED"
    assert route["currentExecutorRef"] is None
    before_replay = len(state["provider"].calls)
    replay = client.post(f"{PREFIX}/works/{work['entity_id']}/execute", headers=HEADERS)
    assert replay.status_code == 200
    assert len(state["provider"].calls) == before_replay
    return route


def _accept_work(state: dict, work: dict, route: dict):
    database = state["database"]
    result_refs = list(route["resultRefs"])
    artifact_refs = list(route["artifactRefs"])
    with _scope():
        foundation = RuntimeFoundation(database)
        evidence = foundation.create(
            "EVIDENCE", company_id=COMPANY, workspace_id=state["workspace_id"],
            parent_id=work["entity_id"], owner_ref=route["responsibilityHolderRef"],
            lifecycle_status="CURRENT", verification_status="VERIFIED", evidence_condition="CURRENT",
            data={"providerEvidenceRefs": list(route["evidenceRefs"]), "resultRefs": result_refs},
        )
        acceptance = foundation.create(
            "ACCEPTANCE", company_id=COMPANY, workspace_id=state["workspace_id"],
            parent_id=work["entity_id"], owner_ref=route["responsibilityHolderRef"],
            data={"resultRefs": result_refs, "evidenceRefs": [evidence["entity_id"]]},
        )
        foundation.transition(acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept")
        foundation.transition(acceptance["entity_id"], "CLOSED", actor="SYSTEM", trigger="close")
        runtime = CanonicalChildWorkRuntime(database)
        completed = runtime.complete_work(
            work["entity_id"], result_refs=result_refs, artifact_refs=artifact_refs,
            evidence_refs=[evidence["entity_id"]], acceptance_refs=[acceptance["entity_id"]],
        )
        assert runtime.complete_work(
            work["entity_id"], result_refs=result_refs, artifact_refs=artifact_refs,
            evidence_refs=[evidence["entity_id"]], acceptance_refs=[acceptance["entity_id"]],
        )["entity_id"] == completed["entity_id"]
    return completed


def _counts(database: Database) -> dict[str, int]:
    with database.connect() as connection:
        entity_counts = {
            kind: connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type=?",
                (TENANT, kind),
            ).fetchone()[0]
            for kind in (
                "OPERATING_SERIES", "CYCLE", "WORK", "RESPONSIBILITY_ASSIGNMENT", "AI_EMPLOYEE",
                "HANDOFF", "EVIDENCE", "ACCEPTANCE", "DECISION_PACKET", "LEARNING",
            )
        }
        entity_counts.update({
            "PROVIDER_TASK": connection.execute(
                "select count(*) from tasks where tenant_id=?", (TENANT,),
            ).fetchone()[0],
            "ARTIFACT": connection.execute(
                "select count(*) from artifacts where tenant_id=?", (TENANT,),
            ).fetchone()[0],
            "PROVIDER_SESSION": connection.execute(
                "select count(distinct json_extract(payload, '$.session_id')) from evolution_events "
                "where tenant_id=? and event_type='usage.task_execution'",
                (TENANT,),
            ).fetchone()[0],
        })
        cycles = [json.loads(row["data_json"]) for row in connection.execute(
            "select data_json from runtime_entities where tenant_id=? and entity_type='CYCLE'",
            (TENANT,),
        ).fetchall()]
        entity_counts["EVALUATION"] = sum("autonomousEvaluation" in item for item in cycles)
        entity_counts["LEADER_REVIEW"] = sum("autonomousLeaderReview" in item for item in cycles)
        return entity_counts


def test_xhs_one_cycle_two_canonical_work_provider_handoff_evaluation_and_decision(tmp_path):
    db_file = tmp_path / "xhs-multi-work-success.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(db_file), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state, assignments = _prepare(db_file, client, provider)
        cycle_id = state["cycle"]["entity_id"]
        with _scope():
            runtime = CanonicalChildWorkRuntime(state["database"])
            work_a = runtime.create_work(
                cycle_id=cycle_id, assignment_ref=assignments["xhs-research"]["entity_id"],
                release_key="research", input_refs=[state["content"]["entity_id"]],
            )
        route_a = _execute_work(client, state, work_a, assignments["xhs-research"], RESEARCH_WORKFLOW)
        work_a = _accept_work(state, work_a, route_a)

        with _scope():
            restarted = CanonicalChildWorkRuntime(Database(str(db_file)))
            assert restarted.get_work(work_a["entity_id"])["data"]["resultRefs"] == work_a["data"]["resultRefs"]
            release = restarted.release_next_work(
                work_a["entity_id"], release_key="content",
                target_assignment_ref=assignments["xhs-copy"]["entity_id"],
                accepted_result_ref=work_a["data"]["resultRefs"][0],
                input_refs=[state["content"]["entity_id"]], reason="研究结果已验收，转交内容创作",
            )
            replay = restarted.release_next_work(
                work_a["entity_id"], release_key="content",
                target_assignment_ref=assignments["xhs-copy"]["entity_id"],
                accepted_result_ref=work_a["data"]["resultRefs"][0],
                input_refs=[state["content"]["entity_id"]], reason="研究结果已验收，转交内容创作",
            )
            assert replay["work"]["entity_id"] == release["work"]["entity_id"]
            assert replay["handoff"]["entity_id"] == release["handoff"]["entity_id"]
            assert replay["duplicate"] is True
            assert release["handoff"]["lifecycle_status"] == "COMPLETED"
            work_b = CanonicalChildWorkRuntime(Database(str(db_file))).get_work(release["work"]["entity_id"])

        route_b = _execute_work(client, state, work_b, assignments["xhs-copy"], CONTENT_WORKFLOW)
        work_b = _accept_work(state, work_b, route_b)
        with _scope():
            control = AutonomousOperatingControl(Database(str(db_file)))
            aggregate = CanonicalChildWorkRuntime(control.db).aggregate_cycle(cycle_id)
            assert set(aggregate["workRefs"]) == {work_a["entity_id"], work_b["entity_id"]}
            assert len(aggregate["resultRefs"]) == 2
            assert len(aggregate["evidenceRefs"]) == 2
            assert len(aggregate["acceptanceRefs"]) == 2
            control.request_cycle_close(series_id=state["series"]["entity_id"], cycle_id=cycle_id)
            closed = control.accept_and_close_cycle(
                series_id=state["series"]["entity_id"], cycle_id=cycle_id,
                reason="研究与内容两项工作均有独立结果、证据和验收",
            )
            cycle_evidence = closed["data"]["evidenceRefs"][0]
            evaluation = control.evaluate_closed_cycle(
                series_id=state["series"]["entity_id"], cycle_id=cycle_id,
                contract=evaluation_contract(), outcome="SUCCESS",
                observed_facts=[{
                    "name": "xhs_cross_professional_work",
                    "value": {"research": "ACCEPTED", "content": "ACCEPTED", "publishing": "NOT_CONNECTED"},
                    "sourceRef": cycle_evidence,
                }],
                comparison={"expected": "two accepted professional Works", "observed": "research and content accepted"},
                confidence="HIGH", sufficiency="SUFFICIENT",
            )
            assert set(evaluation["workRefs"]) == {work_a["entity_id"], work_b["entity_id"]}
            assert control.evaluate_closed_cycle(
                series_id=state["series"]["entity_id"], cycle_id=cycle_id,
                contract=evaluation_contract(), outcome="SUCCESS",
                observed_facts=[{
                    "name": "xhs_cross_professional_work",
                    "value": {"research": "ACCEPTED", "content": "ACCEPTED", "publishing": "NOT_CONNECTED"},
                    "sourceRef": cycle_evidence,
                }],
                comparison={"expected": "two accepted professional Works", "observed": "research and content accepted"},
                confidence="HIGH", sufficiency="SUFFICIENT",
            )["evaluationRef"] == evaluation["evaluationRef"]
            decision = control.review_next_cycle(
                series_id=state["series"]["entity_id"], cycle_id=cycle_id, decision="WAIT",
                reason="跨专业内容资产已形成，等待真实发布能力",
                wait_reason="小红书发布与分析 Connector 尚未连接",
                next_check_at="2026-08-23T09:00:00+00:00",
            )
            assert control.review_next_cycle(
                series_id=state["series"]["entity_id"], cycle_id=cycle_id, decision="WAIT",
                reason="跨专业内容资产已形成，等待真实发布能力",
                wait_reason="小红书发布与分析 Connector 尚未连接",
                next_check_at="2026-08-23T09:00:00+00:00",
            )["entity_id"] == decision["entity_id"]
            cycle = RuntimeFoundation(control.db).get(cycle_id)
            assert cycle["data"]["autonomousLeaderReview"]["leaderEmployeeRef"] == state["employees"]["leader"]
            assert decision["data"]["successorCycleRef"] is None

        reopened = Database(str(db_file))
        reopened.initialize()
        with _scope():
            persisted = RuntimeFoundation(reopened).get(cycle_id)
            assert persisted["data"]["autonomousEvaluation"]["evaluationRef"] == evaluation["evaluationRef"]
            assert persisted["data"]["nextCycleDecisionRef"] == decision["entity_id"]
            counts = _counts(reopened)
            assert counts == {
                "OPERATING_SERIES": 1,
                "CYCLE": 1,
                "WORK": 2,
                "RESPONSIBILITY_ASSIGNMENT": 4,
                "AI_EMPLOYEE": 4,
                "HANDOFF": 1,
                "EVIDENCE": 3,
                "ACCEPTANCE": 3,
                "DECISION_PACKET": 1,
                "LEARNING": 0,
                "PROVIDER_TASK": 2,
                "ARTIFACT": 2,
                "PROVIDER_SESSION": 2,
                "EVALUATION": 1,
                "LEADER_REVIEW": 1,
            }
        assert [item["result_type"] for item in provider.calls] == ["xhs-research-brief", "xhs-publish-package"]


def test_xhs_second_work_missing_evidence_or_unavailable_employee_fails_closed(tmp_path):
    db_file = tmp_path / "xhs-multi-work-failure.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(db_file), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state, assignments = _prepare(db_file, client, provider)
        with _scope():
            runtime = CanonicalChildWorkRuntime(state["database"])
            work_a = runtime.create_work(
                cycle_id=state["cycle"]["entity_id"], assignment_ref=assignments["xhs-research"]["entity_id"],
                release_key="research",
            )
        work_a = _accept_work(
            state, work_a, _execute_work(client, state, work_a, assignments["xhs-research"], RESEARCH_WORKFLOW),
        )
        with _scope():
            RuntimeFoundation(state["database"]).transition(
                state["employees"]["copy"], "DEGRADED", actor="SYSTEM", trigger="capacity_or_capability_gap",
            )
            with pytest.raises(ChildWorkError, match="unavailable"):
                runtime.release_next_work(
                    work_a["entity_id"], release_key="content",
                    target_assignment_ref=assignments["xhs-copy"]["entity_id"],
                    accepted_result_ref=work_a["data"]["resultRefs"][0], reason="must fail",
                )
            RuntimeFoundation(state["database"]).transition(
                state["employees"]["copy"], "AVAILABLE", actor="SYSTEM", trigger="gap_resolved",
            )
            release = runtime.release_next_work(
                work_a["entity_id"], release_key="content",
                target_assignment_ref=assignments["xhs-copy"]["entity_id"],
                accepted_result_ref=work_a["data"]["resultRefs"][0], reason="employee recovered",
            )
        route_b = _execute_work(client, state, release["work"], assignments["xhs-copy"], CONTENT_WORKFLOW)
        with _scope():
            with pytest.raises(ChildWorkError, match="requires Result, Evidence and Acceptance"):
                runtime.complete_work(
                    release["work"]["entity_id"], result_refs=route_b["resultRefs"],
                    artifact_refs=route_b["artifactRefs"], evidence_refs=[], acceptance_refs=[],
                )
            with pytest.raises(AutonomousControlError, match="required child Work is not complete"):
                state["control"].request_cycle_close(
                    series_id=state["series"]["entity_id"], cycle_id=state["cycle"]["entity_id"],
                )
            assert state["control"].get_series(state["series"]["entity_id"])["lifecycle_status"] == "ACTIVE"
        with _scope("other-tenant"), pytest.raises(KeyError):
            CanonicalChildWorkRuntime(state["database"]).get_work(work_a["entity_id"])
