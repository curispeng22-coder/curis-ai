from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
from threading import Event

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import (
    AutonomousControlError,
    AutonomousOperatingControl,
    ResponsibilityRoutingRuntime,
    RuntimeFoundation,
)
from app.runtime.workspace import RD_STAGES, WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase1 import approved_inputs
from backend.tests.test_autonomous_operating_phase3a import evaluation_contract


TENANT = "tenant-autonomous-primary-rd"
COMPANY = "company-autonomous-primary-rd"
DEPARTMENT = "department-autonomous-primary-rd"
BUSINESS = "business-autonomous-primary-rd"
PROJECT = "project-autonomous-primary-rd"
CEO = "ceo-autonomous-primary-rd"
CAPABILITY = "agent.autonomous.rd.controlled"
WORKFLOW_KEY = "rd-autonomous-primary"
PREFIX = "/api/workspace/runtime/foundation/team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-primary.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


class TwoCycleRDProvider:
    def __init__(self, *, second_mode: str = "success", block_second: bool = False):
        self.second_mode = second_mode
        self.block_second = block_second
        self.calls: list[dict] = []
        self.second_started = Event()
        self.release_second = Event()

    def execute(self, prompt: str) -> dict:
        call_number = len(self.calls) + 1
        session = f"rd-primary-session-{call_number}"
        self.calls.append({"prompt": prompt, "session": session})
        if call_number == 2 and self.block_second:
            self.second_started.set()
            if not self.release_second.wait(timeout=5):
                raise TimeoutError("test did not release second provider call")
        if call_number == 2 and self.second_mode == "failure":
            raise TimeoutError("controlled second-cycle provider failure")
        if call_number == 2 and self.second_mode == "invalid":
            output = "partial output without the required result contract"
        else:
            output = json.dumps(
                {
                    "status": "ACCEPTED",
                    "resultType": "rd-operating-result",
                    "summary": (
                        "首轮已形成受控修复与测试证据"
                        if call_number == 1
                        else "第二轮已基于首轮证据完成独立回归验证"
                    ),
                    "problem": "",
                },
                ensure_ascii=False,
            )
        return {
            "output": output,
            "status": "success",
            "session_id": session,
            "outbound_attempted": False,
            "total_tokens": call_number * 5,
            "estimated_cost": 0,
        }


def rd_blueprint() -> dict:
    return {
        "goal": "连续验证受控代码变更与测试证据",
        "stages": list(RD_STAGES),
        "agentRefs": ["rd-operating-leader"],
        "capabilityRefs": ["requirement:controlled-rd-provider"],
        "connectorRefs": [],
        "platformConstraints": {"productionWrite": False},
        "replyPolicy": "CEO_ACCEPTANCE",
        "evidenceRules": ["REAL_RESULTSTORE_ARTIFACT", "REAL_TEST_EVIDENCE"],
        "lifecycleMode": "STUDIO_DRAFT",
        "roleSlots": [
            {
                "role": "研发负责人",
                "responsibility": "在批准边界内完成受控研发验证",
                "capabilityRefs": ["requirement:controlled-rd-provider"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            }
        ],
        "capabilityBindings": [
            {
                "capabilityRef": "requirement:controlled-rd-provider",
                "capability": "Controlled RD Provider",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            }
        ],
        "failurePolicy": {"manualFallback": "保留失败事实", "owner": "研发负责人"},
    }


def approved_plan(version: str, body: dict) -> dict:
    return {
        "version": version,
        "status": "APPROVED",
        "body": body,
        "approvedBy": CEO,
        "approvedAt": f"2026-08-21T{13 if version == 'rd-plan-v1' else 14}:00:00+00:00",
    }


def setup_rd_runtime(path, client: TestClient):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) "
            "values (?, ?, ?, 'Primary RD Company', 'active')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values (?, ?, ?, 'rd-primary-template', '研发部', 'RD')",
            (DEPARTMENT, TENANT, COMPANY),
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
            "lifecycle_status, goal, positioning, created_at, updated_at) "
            "values (?, ?, ?, ?, '产品研发', 'ACTIVE', '持续交付可验证的软件结果', "
            "'受控修改与真实证据', current_timestamp, current_timestamp)",
            (BUSINESS, TENANT, COMPANY, DEPARTMENT),
        )
        connection.execute(
            "insert into projects(project_id, tenant_id, company_id, name, goal, status) "
            "values (?, ?, ?, '受控回归项目', '两轮独立验证', 'active')",
            (PROJECT, TENANT, COMPANY),
        )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        foundation = RuntimeFoundation(database)
        foundation.create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
        workspace = WorkspaceRuntime(database).create_workspace(
            company_id=COMPANY,
            business_ref=BUSINESS,
            business_type="RD",
            name="自主研发办公室",
            blueprint_version="rd-workspace-v1",
            blueprint=rd_blueprint(),
        )["workspace"]
        workspace_id = workspace["workspace_id"]
        role = foundation.list("ROLE_SLOT", company_id=COMPANY, workspace_id=workspace_id)[0]
        employee = foundation.list("AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace_id)[0]
        foundation.transition(role["entity_id"], "READY", actor="SYSTEM", trigger="validate_role")
        foundation.transition(employee["entity_id"], "CREATED", actor="CEO", trigger="accept_proposal")
        foundation.transition(employee["entity_id"], "CONFIGURED", actor="CEO", trigger="configure")
        foundation.transition(employee["entity_id"], "AVAILABLE", actor="CEO", trigger="approve_simulation")
        assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY,
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workspace_id=workspace_id,
            employee_ref=employee["entity_id"],
            role_ref=role["entity_id"],
            responsibility_key="rd-operating-leader",
            responsibility="持续负责受控研发结果与证据",
            input_contract={"requiredRefs": ["project", "cycle-plan"]},
            output_contract={"requiresResult": True, "resultType": "rd-operating-result"},
            is_leader=True,
        )
        with database.connect() as connection:
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                "values (?, ?, ?, ?, 'rd-operating-leader', '研发负责人', '研发负责人', 'idle')",
                (employee["entity_id"], TENANT, COMPANY, DEPARTMENT),
            )
        database.save_tenant_private_capability(
            tenant_id=TENANT,
            capability_type="agent",
            capability_id=CAPABILITY,
            display_name="Controlled RD Provider",
            metadata={"kind": "controlled-provider", "productionSideEffect": False},
            status="active",
        )
        with database.connect() as connection:
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, "
                "capability_type, capability_id, enabled) values (?, ?, ?, 'tenant_private', 'agent', ?, 1)",
                ("binding-autonomous-primary-rd", TENANT, employee["entity_id"], CAPABILITY),
            )

    published = client.post(
        f"{PREFIX}/definitions/publish",
        headers=HEADERS,
        json={
            "company_id": COMPANY,
            "scope_type": "WORKSPACE",
            "scope_ref": workspace_id,
            "workspace_id": workspace_id,
            "workflow_key": WORKFLOW_KEY,
            "roles": [
                {
                    "responsibility_key": "rd-operating-leader",
                    "role_name": "研发负责人",
                    "employee_ref": employee["entity_id"],
                    "role_ref": role["entity_id"],
                    "assignment_ref": assignment["entity_id"],
                    "responsibility": "完成一轮有真实 ResultStore 与测试证据的研发验证",
                    "input_contract": {"requiredRefs": ["project", "cycle-plan"]},
                    "output_contract": {"requiresResult": True, "resultType": "rd-operating-result"},
                    "is_leader": True,
                }
            ],
            "default_flow": ["rd-operating-leader"],
        },
    )
    assert published.status_code == 200, published.text

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        strategy, envelope = approved_inputs("rd-strategy-v1")
        control = AutonomousOperatingControl(database)
        series = control.create_series(
            company_id=COMPANY,
            workspace_id=workspace_id,
            leader_assignment_ref=assignment["entity_id"],
            strategy=strategy,
            envelope=envelope,
        )
        cycle1 = control.claim_trigger(
            series_id=series["entity_id"],
            source_type="SCHEDULED",
            source_key="rd-observation-window-1",
        )["cycle"]
    return database, control, series, cycle1, workspace_id, employee["entity_id"]


def execute_and_close(client, control, series, cycle, plan):
    cycle_id = cycle["entity_id"]
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        running = control.materialize_cycle_work(
            series_id=series["entity_id"],
            cycle_id=cycle_id,
            workflow_key=WORKFLOW_KEY,
            plan=plan,
        )
        assert running["lifecycle_status"] == "RUNNING"
    response = client.post(f"{PREFIX}/works/{cycle_id}/execute", headers=HEADERS)
    assert response.status_code == 200, response.text
    assert response.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED"
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        waiting = control.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle_id)
        assert waiting["lifecycle_status"] == "WAITING_CEO"
        return control.accept_and_close_cycle(
            series_id=series["entity_id"],
            cycle_id=cycle_id,
            reason="CEO accepts the bounded result and evidence",
        )


def evaluate(control, series, cycle, *, observed: str):
    evidence_ref = cycle["data"]["evidenceRefs"][0]
    return control.evaluate_closed_cycle(
        series_id=series["entity_id"],
        cycle_id=cycle["entity_id"],
        contract=evaluation_contract("rd-evaluation-v1"),
        outcome="SUCCESS",
        observed_facts=[
            {
                "name": "rd_verified_result",
                "value": observed,
                "sourceRef": evidence_ref,
            }
        ],
        comparison={"expected": "独立受控研发结果", "observed": observed},
        confidence="HIGH",
        sufficiency="SUFFICIENT",
    )


def prepare_cycle2(path, client, provider):
    database, control, series, cycle1, workspace_id, employee_ref = setup_rd_runtime(path, client)
    cycle1_plan = approved_plan(
        "rd-plan-v1",
        {
            "domain": "RD",
            "projectRef": PROJECT,
            "observationWindow": "cycle-1",
            "work": "建立受控修复与测试证据基线",
            "acceptance": "Result contract accepted and Evidence verified",
        },
    )
    cycle1 = execute_and_close(client, control, series, cycle1, cycle1_plan)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        evaluation1 = evaluate(control, series, cycle1, observed="首轮受控变更与测试证据已验收")
        decision1 = control.review_next_cycle(
            series_id=series["entity_id"],
            cycle_id=cycle1["entity_id"],
            decision="CONTINUE",
            reason="首轮证据充分，按同一策略进入独立第二观察周期",
        )
        restarted = AutonomousOperatingControl(Database(str(path)))
        successor = restarted.authorize_successor(decision1["entity_id"])
        replay = restarted.authorize_successor(decision1["entity_id"])
        assert replay["cycle"]["entity_id"] == successor["cycle"]["entity_id"]
        assert replay["claim"]["entity_id"] == successor["claim"]["entity_id"]
    return {
        "database": database,
        "control": restarted,
        "series": series,
        "cycle1": cycle1,
        "evaluation1": evaluation1,
        "decision1": decision1,
        "cycle2": successor["cycle"],
        "claim2": successor["claim"],
        "workspace_id": workspace_id,
        "employee_ref": employee_ref,
        "provider": provider,
    }


def cycle2_plan(state):
    cycle1 = state["cycle1"]
    return approved_plan(
        "rd-plan-v2",
        {
            "domain": "RD",
            "projectRef": PROJECT,
            "observationWindow": "cycle-2",
            "work": "基于首轮结果复核边界并完成独立第二轮回归验证",
            "acceptance": "second Result contract accepted with distinct Evidence",
            "predecessorCycleRef": cycle1["entity_id"],
            "predecessorDecisionRef": state["decision1"]["entity_id"],
            "predecessorResultRefs": cycle1["data"]["resultRefs"],
            "predecessorEvidenceRefs": cycle1["data"]["evidenceRefs"],
            "predecessorEvaluationRef": state["evaluation1"]["evaluationRef"],
        },
    )


def entity_counts(database):
    with database.connect() as connection:
        counts = {
            kind: connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type=?",
                (TENANT, kind),
            ).fetchone()[0]
            for kind in (
                "OPERATING_SERIES",
                "CYCLE",
                "TRIGGER_CLAIM",
                "EVIDENCE",
                "ACCEPTANCE",
                "DECISION_PACKET",
            )
        }
        counts["PROVIDER_TASK"] = connection.execute("select count(*) from tasks").fetchone()[0]
        counts["ARTIFACT"] = connection.execute("select count(*) from artifacts").fetchone()[0]
        cycles = connection.execute(
            "select data_json from runtime_entities where tenant_id=? and entity_type='CYCLE'",
            (TENANT,),
        ).fetchall()
        payloads = [json.loads(row["data_json"]) for row in cycles]
        counts["EVALUATION"] = sum("autonomousEvaluation" in item for item in payloads)
        counts["LEADER_REVIEW"] = sum("autonomousLeaderReview" in item for item in payloads)
        return counts


def test_rd_primary_two_complete_cycles_are_distinct_restart_safe_and_stop_before_cycle3(tmp_path):
    path = tmp_path / "rd-primary-two-cycle.sqlite"
    provider = TwoCycleRDProvider(block_second=True)
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = prepare_cycle2(path, client, provider)
        control, series, cycle2 = state["control"], state["series"], state["cycle2"]
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            predecessor_before = deepcopy(
                RuntimeFoundation(state["database"]).get(state["cycle1"]["entity_id"])
            )
        plan2 = cycle2_plan(state)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            running = control.materialize_cycle_work(
                series_id=series["entity_id"],
                cycle_id=cycle2["entity_id"],
                workflow_key=WORKFLOW_KEY,
                plan=plan2,
            )
            assert running["lifecycle_status"] == "RUNNING"
            restarted_running = AutonomousOperatingControl(Database(str(path)))
            replayed_work = restarted_running.materialize_cycle_work(
                series_id=series["entity_id"],
                cycle_id=cycle2["entity_id"],
                workflow_key=WORKFLOW_KEY,
                plan=plan2,
            )
            assert replayed_work["entity_id"] == cycle2["entity_id"]

        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(client.post, f"{PREFIX}/works/{cycle2['entity_id']}/execute", headers=HEADERS)
            assert provider.second_started.wait(timeout=5)
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
                during = RuntimeFoundation(Database(str(path))).get(cycle2["entity_id"])
                assert during["data"]["responsibilityRouting"]["currentExecutorRef"] == state["employee_ref"]
            provider.release_second.set()
            response = pending.result(timeout=5)
        assert response.status_code == 200, response.text
        assert response.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED"
        duplicate = client.post(f"{PREFIX}/works/{cycle2['entity_id']}/execute", headers=HEADERS)
        assert duplicate.status_code == 200

        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            restarted_after_result = AutonomousOperatingControl(Database(str(path)))
            restarted_after_result.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle2["entity_id"])
            cycle2_closed = restarted_after_result.accept_and_close_cycle(
                series_id=series["entity_id"],
                cycle_id=cycle2["entity_id"],
                reason="第二轮独立结果与证据已验收",
            )
            evaluation2 = evaluate(
                restarted_after_result,
                series,
                cycle2_closed,
                observed="第二轮独立回归结果与测试证据已验收",
            )
            assert evaluate(
                restarted_after_result,
                series,
                cycle2_closed,
                observed="第二轮独立回归结果与测试证据已验收",
            )["evaluationRef"] == evaluation2["evaluationRef"]
            decision2 = restarted_after_result.review_next_cycle(
                series_id=series["entity_id"],
                cycle_id=cycle2["entity_id"],
                decision="WAIT",
                reason="两轮证明完成，等待下一次真实观察窗口",
                wait_reason="本 Proof 明确停止在两轮",
                next_check_at="2026-08-22T09:00:00+00:00",
            )
            assert restarted_after_result.review_next_cycle(
                series_id=series["entity_id"],
                cycle_id=cycle2["entity_id"],
                decision="WAIT",
                reason="两轮证明完成，等待下一次真实观察窗口",
                wait_reason="本 Proof 明确停止在两轮",
                next_check_at="2026-08-22T09:00:00+00:00",
            )["entity_id"] == decision2["entity_id"]
            stopped = restarted_after_result.authorize_successor(decision2["entity_id"])
            assert stopped["created"] is False
            assert stopped["claim"] is None
            assert stopped["cycle"] is None

            cycle1_after = RuntimeFoundation(state["database"]).get(state["cycle1"]["entity_id"])
            assert cycle1_after["data"]["autonomousControl"] == predecessor_before["data"]["autonomousControl"]
            assert cycle1_after["data"]["autonomousEvaluation"] == predecessor_before["data"]["autonomousEvaluation"]
            assert cycle2_closed["data"]["autonomousControl"]["predecessorCycleRef"] == state["cycle1"]["entity_id"]
            assert cycle2_closed["data"]["autonomousControl"]["predecessorDecisionRef"] == state["decision1"]["entity_id"]
            assert cycle2_closed["data"]["autonomousControl"]["planPin"]["body"] == plan2["body"]
            assert cycle2_closed["data"]["resultRefs"] != state["cycle1"]["data"]["resultRefs"]
            assert cycle2_closed["data"]["evidenceRefs"] != state["cycle1"]["data"]["evidenceRefs"]
            assert decision2["entity_id"] != state["decision1"]["entity_id"]
            for item in (cycle1_after, RuntimeFoundation(state["database"]).get(cycle2["entity_id"])):
                assert "acceptedLearning" not in item["data"]
                assert "learning" not in item["data"]

        counts = entity_counts(state["database"])
        assert counts == {
            "OPERATING_SERIES": 1,
            "CYCLE": 2,
            "TRIGGER_CLAIM": 2,
            "EVIDENCE": 2,
            "ACCEPTANCE": 2,
            "DECISION_PACKET": 2,
            "PROVIDER_TASK": 2,
            "ARTIFACT": 2,
            "EVALUATION": 2,
            "LEADER_REVIEW": 2,
        }
        assert len(provider.calls) == 2
        assert provider.calls[0]["session"] != provider.calls[1]["session"]

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        restarted = AutonomousOperatingControl(Database(str(path)))
        assert restarted.get_series(state["series"]["entity_id"])["lifecycle_status"] == "WAITING"
        assert entity_counts(Database(str(path)))["CYCLE"] == 2


@pytest.mark.parametrize("second_mode", ["failure", "invalid"])
def test_cycle2_provider_failure_or_invalid_result_fails_closed_without_cycle3_or_learning(tmp_path, second_mode):
    path = tmp_path / f"rd-primary-{second_mode}.sqlite"
    provider = TwoCycleRDProvider(second_mode=second_mode)
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = prepare_cycle2(path, client, provider)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            state["control"].materialize_cycle_work(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle2"]["entity_id"],
                workflow_key=WORKFLOW_KEY,
                plan=cycle2_plan(state),
            )
        response = client.post(f"{PREFIX}/works/{state['cycle2']['entity_id']}/execute", headers=HEADERS)
        assert response.status_code == 200, response.text
        assert response.json()["work"]["data"]["responsibilityRouting"]["status"] == "WAITING"
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            failed = state["control"].fail_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle2"]["entity_id"],
                reason=f"controlled Cycle 2 {second_mode}",
            )
            assert failed["lifecycle_status"] == "FAILED"
            assert "acceptedLearning" not in failed["data"]
            assert "learning" not in failed["data"]
        counts = entity_counts(state["database"])
        assert counts["CYCLE"] == 2
        assert counts["PROVIDER_TASK"] == 2
        assert counts["ARTIFACT"] == (1 if second_mode == "failure" else 2)
        assert counts["EVIDENCE"] == 1
        assert counts["ACCEPTANCE"] == 1
        assert counts["DECISION_PACKET"] == 1


@pytest.mark.parametrize("gate", ["capability", "employee"])
def test_cycle2_missing_capability_or_unavailable_employee_blocks_before_provider(tmp_path, gate):
    path = tmp_path / f"rd-primary-{gate}.sqlite"
    provider = TwoCycleRDProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = prepare_cycle2(path, client, provider)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            with state["database"].connect() as connection:
                if gate == "capability":
                    connection.execute(
                        "update tenant_private_capabilities set status='disabled' "
                        "where tenant_id=? and capability_type='agent' and capability_id=?",
                        (TENANT, CAPABILITY),
                    )
                else:
                    connection.execute(
                        "update runtime_entities set lifecycle_status='PAUSED' "
                        "where tenant_id=? and entity_id=?",
                        (TENANT, state["employee_ref"]),
                    )
            with pytest.raises(AutonomousControlError, match="capability is unavailable|Employee is not available"):
                state["control"].materialize_cycle_work(
                    series_id=state["series"]["entity_id"],
                    cycle_id=state["cycle2"]["entity_id"],
                    workflow_key=WORKFLOW_KEY,
                    plan=cycle2_plan(state),
                )
        counts = entity_counts(state["database"])
        assert counts["CYCLE"] == 2
        assert counts["PROVIDER_TASK"] == 1
        assert counts["ARTIFACT"] == 1
        assert counts["DECISION_PACKET"] == 1
        assert len(provider.calls) == 1
