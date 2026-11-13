from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import AutonomousControlError, AutonomousOperatingControl, ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.workspace import WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.test_autonomous_operating_phase1 import approved_inputs
from backend.tests.test_autonomous_operating_primary_two_cycle_e2e import (
    BUSINESS,
    CEO,
    COMPANY,
    DEPARTMENT,
    HEADERS,
    PREFIX,
    TENANT,
    TwoCycleRDProvider,
    cycle2_plan,
    evaluate,
    prepare_cycle2,
)


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-learning.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


def two_cycle_truth(path, client: TestClient):
    provider = TwoCycleRDProvider()
    state = prepare_cycle2(path, client, provider)
    control, series, cycle2 = state["control"], state["series"], state["cycle2"]
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control.materialize_cycle_work(
            series_id=series["entity_id"],
            cycle_id=cycle2["entity_id"],
            workflow_key="rd-autonomous-primary",
            plan=cycle2_plan(state),
        )
    response = client.post(f"{PREFIX}/works/{cycle2['entity_id']}/execute", headers=HEADERS)
    assert response.status_code == 200, response.text
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        restarted = AutonomousOperatingControl(Database(str(path)))
        restarted.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle2["entity_id"])
        cycle2 = restarted.accept_and_close_cycle(
            series_id=series["entity_id"], cycle_id=cycle2["entity_id"], reason="second Cycle accepted",
        )
        evaluate(restarted, series, cycle2, observed="第二轮受控研发结果已验收")
        decision2 = restarted.review_next_cycle(
            series_id=series["entity_id"],
            cycle_id=cycle2["entity_id"],
            decision="WAIT",
            reason="两轮证据足够形成候选经验，但不创建第三轮",
            wait_reason="等待新的独立观察窗口",
            next_check_at="2026-08-23T09:00:00+00:00",
        )
        assert decision2["lifecycle_status"] == "APPLIED"
    state.update({"control": restarted, "cycle2": cycle2, "decision2": decision2, "provider": provider})
    return state


def candidate(control, state, *, claim="小批量受控修改并配套测试证据，可降低研发回归风险", **overrides):
    values = {
        "series_id": state["series"]["entity_id"],
        "supporting_cycle_refs": [state["cycle1"]["entity_id"], state["cycle2"]["entity_id"]],
        "claim": claim,
        "scope_type": "DOMAIN",
        "scope_ref": "RD",
        "confidence": "HIGH",
        "conditions": ["受控修改路径", "每轮都有独立测试证据"],
        "limitations": ["未验证高风险迁移", "未验证外部生产环境"],
        "proposed_use": "FUTURE_CONTEXT",
        "revalidate_when": ["连续两轮出现相反测试结果", "权限边界变化"],
    }
    values.update(overrides)
    return control.create_learning_candidate(**values)


def test_candidate_acceptance_restart_replay_future_context_and_no_cycle3(tmp_path):
    path = tmp_path / "learning-accepted.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": TwoCycleRDProvider().execute})) as client:
        state = two_cycle_truth(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control = AutonomousOperatingControl(Database(str(path)))
        before = control.get_series(state["series"]["entity_id"])
        learning_candidate = candidate(control, state)
        assert learning_candidate["artifact_type"] == "learning_candidate"
        assert learning_candidate["status"] == "generated"
        assert candidate(control, state)["artifact_id"] == learning_candidate["artifact_id"]
        def accept():
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
                return AutonomousOperatingControl(Database(str(path))).accept_learning_candidate(
                    learning_candidate["artifact_id"], actor="LEADER",
                )

        with ThreadPoolExecutor(max_workers=2) as pool:
            accepted, concurrent_replay = [future.result() for future in [pool.submit(accept), pool.submit(accept)]]
        assert concurrent_replay["artifact_id"] == accepted["artifact_id"]
        assert accepted["artifact_type"] == "accepted_learning" and accepted["status"] == "accepted"
        assert control.accept_learning_candidate(learning_candidate["artifact_id"], actor="LEADER")["artifact_id"] == accepted["artifact_id"]
        context = AutonomousOperatingControl(Database(str(path))).resolve_learning_context(state["series"]["entity_id"])
        assert [item["acceptedLearningRef"] for item in context] == [accepted["artifact_id"]]
        assert context[0]["provenance"]["cycleRefs"] == [state["cycle1"]["entity_id"], state["cycle2"]["entity_id"]]
        assert len(context[0]["provenance"]["resultRefs"]) == 2
        assert len(context[0]["provenance"]["evidenceRefs"]) == 2
        assert len(context[0]["provenance"]["evaluationRefs"]) == 2
        assert len(context[0]["provenance"]["decisionRefs"]) == 2
        after = control.get_series(state["series"]["entity_id"])
        assert after["data"]["strategyVersions"] == before["data"]["strategyVersions"]
        assert after["data"]["currentStrategyRef"] == before["data"]["currentStrategyRef"]
        with control.db.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where tenant_id=? and entity_type='CYCLE'",
                (TENANT,),
            ).fetchone()[0] == 2


def test_learning_rejects_one_cycle_or_stale_evidence(tmp_path):
    path = tmp_path / "learning-insufficient.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": TwoCycleRDProvider().execute})) as client:
        state = two_cycle_truth(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control = state["control"]
        with pytest.raises(AutonomousControlError, match="at least two"):
            candidate(control, state, supporting_cycle_refs=[state["cycle1"]["entity_id"]])
        evidence_ref = state["cycle1"]["data"]["evidenceRefs"][0]
        with control.db.connect() as connection:
            connection.execute(
                "update runtime_entities set evidence_condition='STALE' where tenant_id=? and entity_id=?",
                (TENANT, evidence_ref),
            )
        with pytest.raises(AutonomousControlError, match="stale or unverified"):
            candidate(control, state)


def test_company_or_protected_learning_requires_ceo(tmp_path):
    path = tmp_path / "learning-ceo-gate.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": TwoCycleRDProvider().execute})) as client:
        state = two_cycle_truth(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control = state["control"]
        proposed = candidate(
            control,
            state,
            scope_type="COMPANY_CANDIDATE",
            scope_ref=COMPANY,
            proposed_use="COMPANY_POLICY",
        )
        with pytest.raises(AutonomousControlError, match="CEO authority"):
            control.accept_learning_candidate(proposed["artifact_id"], actor="LEADER")
        accepted = control.accept_learning_candidate(proposed["artifact_id"], actor="CEO")
        assert accepted["data"]["acceptedBy"] == "CEO"


def add_xhs_series(database: Database) -> dict:
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        with database.connect() as connection:
            connection.execute(
                "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, "
                "goal, positioning, created_at, updated_at) values ('learning-xhs-business', ?, ?, ?, 'XHS Learning', "
                "'ACTIVE', '形成可审核内容资产', '真实内容边界', current_timestamp, current_timestamp)",
                (TENANT, COMPANY, DEPARTMENT),
            )
        workspace = WorkspaceRuntime(database).create_workspace(
            company_id=COMPANY,
            business_ref="learning-xhs-business",
            business_type="XHS",
            name="XHS Learning Isolation",
            blueprint_version="xhs-learning-v1",
            blueprint={
                "goal": "形成可审核内容资产",
                "stages": ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"],
                "agentRefs": ["xhs-leader"],
                "capabilityRefs": ["xhs-writing"],
                "connectorRefs": ["xhs-publishing"],
                "platformConstraints": {"publishing": "NOT_CONNECTED"},
                "replyPolicy": "CONTENT_REVIEW",
                "evidenceRules": ["NO_FAKE_ANALYTICS"],
                "platform": "XHS",
            },
        )["workspace"]
        foundation = RuntimeFoundation(database)
        role = foundation.create(
            "ROLE_SLOT", company_id=COMPANY, workspace_id=workspace["workspace_id"],
            lifecycle_status="READY", data={"role": "XHS Leader"},
        )
        employee = foundation.create(
            "AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace["workspace_id"],
            lifecycle_status="AVAILABLE", data={"name": "XHS Leader", "roleSlotRef": role["entity_id"]},
        )
        assignment = ResponsibilityRoutingRuntime(database).create_assignment(
            company_id=COMPANY,
            scope_type="WORKSPACE",
            scope_ref=workspace["workspace_id"],
            workspace_id=workspace["workspace_id"],
            employee_ref=employee["entity_id"],
            role_ref=role["entity_id"],
            responsibility_key="xhs-learning-leader",
            responsibility="负责 XHS 内容证据",
            is_leader=True,
        )
        approved_strategy, envelope = approved_inputs("xhs-learning-v1")
        return AutonomousOperatingControl(database).create_series(
            company_id=COMPANY,
            workspace_id=workspace["workspace_id"],
            leader_assignment_ref=assignment["entity_id"],
            strategy=approved_strategy,
            envelope=envelope,
        )


def test_rd_domain_learning_does_not_leak_into_xhs(tmp_path):
    path = tmp_path / "learning-domain-isolation.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": TwoCycleRDProvider().execute})) as client:
        state = two_cycle_truth(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        accepted = state["control"].accept_learning_candidate(candidate(state["control"], state)["artifact_id"], actor="LEADER")
        assert state["control"].resolve_learning_context(state["series"]["entity_id"])[0]["acceptedLearningRef"] == accepted["artifact_id"]
        xhs_series = add_xhs_series(state["database"])
        assert AutonomousOperatingControl(state["database"]).resolve_learning_context(xhs_series["entity_id"]) == []


def test_conflict_requires_explicit_supersede_then_invalidation_preserves_history(tmp_path):
    path = tmp_path / "learning-conflict.sqlite"
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": TwoCycleRDProvider().execute})) as client:
        state = two_cycle_truth(path, client)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control = state["control"]
        first = control.accept_learning_candidate(candidate(control, state)["artifact_id"], actor="LEADER")
        unresolved = candidate(
            control,
            state,
            claim="同样条件下小批量证据不足以降低回归风险",
            conflicts_with_refs=[first["artifact_id"]],
        )
        with pytest.raises(AutonomousControlError, match="explicit supersede"):
            control.accept_learning_candidate(unresolved["artifact_id"], actor="LEADER")
        replacement = candidate(
            control,
            state,
            claim="同样条件下需要额外边界检查才能降低回归风险",
            conflicts_with_refs=[first["artifact_id"]],
            supersedes_refs=[first["artifact_id"]],
        )
        second = control.accept_learning_candidate(replacement["artifact_id"], actor="LEADER")
        assert [item["acceptedLearningRef"] for item in control.resolve_learning_context(state["series"]["entity_id"])] == [second["artifact_id"]]
        evidence_ref = state["cycle2"]["data"]["evidenceRefs"][0]
        invalidated = control.invalidate_learning(
            second["artifact_id"],
            actor="LEADER",
            reason="后续复核要求重新验证该结论",
            evidence_refs=[evidence_ref],
        )
        assert invalidated["learning"]["status"] == "archived"
        assert control.resolve_learning_context(state["series"]["entity_id"]) == []
        with control.db.connect() as connection:
            statuses = dict(connection.execute(
                "select artifact_id, status from artifacts where artifact_id in (?, ?)",
                (first["artifact_id"], second["artifact_id"]),
            ).fetchall())
        assert statuses == {first["artifact_id"]: "archived", second["artifact_id"]: "archived"}
        assert connection_safe(control.db)


def connection_safe(database: Database) -> bool:
    with database.connect() as connection:
        return connection.execute("pragma integrity_check").fetchone()[0] == "ok"
