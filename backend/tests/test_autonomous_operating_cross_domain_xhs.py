from __future__ import annotations

import json
import re

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
from app.runtime.workspace import WorkspaceRuntime
from app.tenant_context import TenantContext


TENANT = "tenant-autonomous-cross-domain-xhs"
COMPANY = "company-autonomous-cross-domain-xhs"
DEPARTMENT = "department-autonomous-cross-domain-xhs"
BUSINESS = "business-autonomous-cross-domain-xhs"
CEO = "ceo-autonomous-cross-domain-xhs"
CAPABILITY = "agent.autonomous.xhs.controlled"
WORKFLOW = "xhs-autonomous-content-proof"
PREFIX = "/api/workspace/runtime/foundation/team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


@pytest.fixture(autouse=True)
def isolated_database_environment(tmp_path, monkeypatch):
    path = tmp_path / "autonomous-cross-domain-xhs.sqlite"
    monkeypatch.setenv("CURIS_DB", str(path))
    monkeypatch.setenv("CURIS_DB_PATH", str(path))
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(path))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")


class XHSProvider:
    """Controlled provider on the real Task/Session/callback path; not live analytics."""

    def __init__(self, *, malformed: bool = False):
        self.malformed = malformed
        self.calls: list[dict] = []

    def execute(self, prompt: str) -> dict:
        result_type = re.search(r"输出结果类型：([^\n]+)", prompt).group(1).strip()
        session = f"xhs-cross-domain-session-{len(self.calls) + 1}"
        self.calls.append({"result_type": result_type, "session": session, "prompt": prompt})
        if self.malformed:
            output = "provider output without the required XHS Result contract"
        else:
            payload = {
                "status": "ACCEPTED",
                "resultType": result_type,
                "summary": {
                    "xhs-topic-plan": "已形成面向目标受众的内容角度",
                    "xhs-research-brief": "已形成带来源边界的内容依据",
                    "xhs-publish-package": "已形成待审核内容资产；发布能力尚未连接",
                }[result_type],
                "problem": "",
                "domain": "XHS",
                "publicationStatus": "NOT_CONNECTED",
                "analyticsStatus": "UNAVAILABLE",
            }
            output = json.dumps(payload, ensure_ascii=False)
        return {
            "output": output,
            "status": "success",
            "session_id": session,
            "outbound_attempted": False,
            "total_tokens": 6,
            "estimated_cost": 0,
        }


def strategy() -> tuple[dict, dict]:
    common = {"status": "APPROVED", "approvedBy": CEO, "approvedAt": "2026-08-21T15:00:00+00:00"}
    return (
        {
            **common,
            "version": "xhs-strategy-v1",
            "body": {
                "audienceHypothesis": "独立开发者需要可验证的本地 AI 经营方法",
                "contentAngle": "用真实边界解释产品能力",
                "cadence": "one-reviewable-note",
            },
        },
        {
            **common,
            "version": "xhs-envelope-v1",
            "body": {
                "allowed": ["audienceHypothesis", "contentAngle", "cadence"],
                "protected": ["goal", "brandBoundary", "externalPublish"],
            },
        },
    )


def evaluation_contract() -> dict:
    return {
        "version": "xhs-evaluation-v1",
        "status": "APPROVED",
        "body": {
            "observationWindow": {"kind": "CONTENT_REVIEW", "count": 1},
            "success": "reviewable content package with explicit source and publication boundaries",
            "failure": "content package violates the approved audience or brand boundary",
            "insufficientEvidence": "source or review evidence is missing",
            "continueObservation": "wait for one bounded content review window",
            "escalateWhen": "protected brand or external publication authority must change",
        },
        "approvedBy": CEO,
        "approvedAt": "2026-08-21T15:05:00+00:00",
    }


def blueprint() -> dict:
    return {
        "goal": "形成一条来源边界清楚、可供审核的小红书内容资产",
        "stages": ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"],
        "agentRefs": ["xhs-content-team"],
        "capabilityRefs": ["xhs-content-research", "xhs-writing"],
        "connectorRefs": ["xhs-publishing"],
        "platformConstraints": {"platform": "XHS", "publishing": "NOT_CONNECTED"},
        "replyPolicy": "CONTENT_REVIEW",
        "evidenceRules": ["PROVIDER_PROVENANCE", "NO_FAKE_ANALYTICS"],
        "platform": "XHS",
    }


def setup(path, client: TestClient, provider: XHSProvider):
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, ?, 'XHS Cross-domain Company', 'active')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values (?, ?, ?, 'xhs-domain-template', '内容增长部', 'XHS')",
            (DEPARTMENT, TENANT, COMPANY),
        )
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, lifecycle_status, "
            "goal, positioning, created_at, updated_at) values (?, ?, ?, ?, '小红书内容增长', 'ACTIVE', "
            "'持续形成可验证的内容资产', '真实来源与平台边界优先', current_timestamp, current_timestamp)",
            (BUSINESS, TENANT, COMPANY, DEPARTMENT),
        )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        foundation = RuntimeFoundation(database)
        foundation.create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
        workspace = WorkspaceRuntime(database).create_workspace(
            company_id=COMPANY,
            business_ref=BUSINESS,
            business_type="XHS",
            name="小红书内容增长办公室",
            blueprint_version="xhs-cross-domain-v1",
            blueprint=blueprint(),
        )["workspace"]
        workspace_id = workspace["workspace_id"]
        employees: dict[str, str] = {}
        assignments: dict[str, str] = {}
        roles = {
            "leader": ("内容负责人", "持续负责内容目标与证据", True),
            "topic": ("选题策划", "形成受众与内容角度", False),
            "research": ("研究分析", "形成来源与风险边界", False),
            "copy": ("内容创作", "形成待审核内容资产", False),
        }
        for key, (name, responsibility, is_leader) in roles.items():
            role = foundation.create(
                "ROLE_SLOT",
                company_id=COMPANY,
                workspace_id=workspace_id,
                lifecycle_status="READY",
                data={"role": name},
            )
            employee = foundation.create(
                "AI_EMPLOYEE",
                company_id=COMPANY,
                workspace_id=workspace_id,
                lifecycle_status="AVAILABLE",
                data={"name": name, "roleSlotRef": role["entity_id"]},
            )
            employees[key] = employee["entity_id"]
            assignment = ResponsibilityRoutingRuntime(database).create_assignment(
                company_id=COMPANY,
                scope_type="WORKSPACE",
                scope_ref=workspace_id,
                workspace_id=workspace_id,
                employee_ref=employee["entity_id"],
                role_ref=role["entity_id"],
                responsibility_key=f"xhs-{key}",
                responsibility=responsibility,
                input_contract={"requiredRefs": ["content-item"]},
                output_contract={"requiresResult": True},
                is_leader=is_leader,
            )
            assignments[key] = assignment["entity_id"]
            with database.connect() as connection:
                connection.execute(
                    "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                    "values (?, ?, ?, ?, ?, ?, ?, 'idle')",
                    (employee["entity_id"], TENANT, COMPANY, DEPARTMENT, f"xhs-{key}", name, name),
                )
                connection.execute(
                    "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, "
                    "capability_type, capability_id, enabled) values (?, ?, ?, 'tenant_private', 'agent', ?, 1)",
                    (f"binding-xhs-{key}", TENANT, employee["entity_id"], CAPABILITY),
                )
        database.save_tenant_private_capability(
            tenant_id=TENANT,
            capability_type="agent",
            capability_id=CAPABILITY,
            display_name="Controlled XHS Provider",
            metadata={"kind": "controlled-provider", "externalPublish": False},
            status="active",
        )
        content, version = WorkspaceRuntime(database).create_content_item(
            company_id=COMPANY,
            workspace_id=workspace_id,
            blueprint_version="xhs-cross-domain-v1",
            platform="XHS",
            owner_ref=workspace_id,
            outcome_ref="形成一条待审核内容资产",
            intent_ref="解释本地 AI 经营能力的真实边界",
            platform_variant="图文",
            payload_ref="CEO accepted content intent",
            author=CEO,
            constraints_check="尚未发布；不得生成平台指标",
            title="Curis 如何诚实表达 AI 经营能力",
            body="待员工围绕真实能力边界形成内容资产。",
            tags=["AI经营", "本地优先"],
        )
        WorkspaceRuntime(database).accept_content_idea(
            company_id=COMPANY,
            workspace_id=workspace_id,
            content_id=content["entity_id"],
        )

    roles_payload = [
        {
            "responsibility_key": "xhs-leader",
            "role_name": "内容负责人",
            "employee_ref": employees["leader"],
            "assignment_ref": assignments["leader"],
            "responsibility": "持续负责内容目标与证据",
            "input_contract": {"requiredRefs": ["content-item"]},
            "output_contract": {"requiresResult": True, "resultType": "xhs-leader-review"},
            "is_leader": True,
        },
        {
            "responsibility_key": "xhs-topic",
            "role_name": "选题策划",
            "employee_ref": employees["topic"],
            "assignment_ref": assignments["topic"],
            "responsibility": "形成受众与内容角度",
            "input_contract": {"requiredRefs": ["content-item"]},
            "output_contract": {"requiresResult": True, "resultType": "xhs-topic-plan"},
        },
        {
            "responsibility_key": "xhs-research",
            "role_name": "研究分析",
            "employee_ref": employees["research"],
            "assignment_ref": assignments["research"],
            "responsibility": "形成来源与风险边界",
            "input_contract": {"requiredRefs": ["xhs-topic-plan"]},
            "output_contract": {"requiresResult": True, "resultType": "xhs-research-brief"},
        },
        {
            "responsibility_key": "xhs-copy",
            "role_name": "内容创作",
            "employee_ref": employees["copy"],
            "assignment_ref": assignments["copy"],
            "responsibility": "形成待审核内容资产",
            "input_contract": {"requiredRefs": ["xhs-research-brief"]},
            "output_contract": {"requiresResult": True, "resultType": "xhs-publish-package"},
        },
    ]
    published = client.post(
        f"{PREFIX}/definitions/publish",
        headers=HEADERS,
        json={
            "company_id": COMPANY,
            "scope_type": "WORKSPACE",
            "scope_ref": workspace_id,
            "workspace_id": workspace_id,
            "workflow_key": WORKFLOW,
            "roles": roles_payload,
            "default_flow": ["xhs-topic", "xhs-research", "xhs-copy"],
        },
    )
    assert published.status_code == 200, published.text
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        approved_strategy, envelope = strategy()
        control = AutonomousOperatingControl(database)
        series = control.create_series(
            company_id=COMPANY,
            workspace_id=workspace_id,
            leader_assignment_ref=assignments["leader"],
            strategy=approved_strategy,
            envelope=envelope,
        )
        cycle = control.claim_trigger(
            series_id=series["entity_id"],
            source_type="RESULT",
            source_key=f"xhs-content:{content['entity_id']}:review-1",
        )["cycle"]
    return {
        "database": database,
        "control": control,
        "series": series,
        "cycle": cycle,
        "workspace_id": workspace_id,
        "employees": employees,
        "content": content,
        "version": version,
        "provider": provider,
    }


def plan(state) -> dict:
    return {
        "version": "xhs-plan-v1",
        "status": "APPROVED",
        "body": {
            "domain": "XHS",
            "contentItemRef": state["content"]["entity_id"],
            "contentVersionRef": state["version"]["entity_id"],
            "work": "形成一条来源边界清楚、可供审核但尚未发布的小红书内容资产",
            "acceptance": "typed content results and verified provider evidence; no external metric claim",
            "publicationBoundary": "NOT_CONNECTED",
            "analyticsBoundary": "UNAVAILABLE",
        },
        "approvedBy": CEO,
        "approvedAt": "2026-08-21T15:10:00+00:00",
    }


def execute_close_evaluate(path, client: TestClient, state, *, sufficiency="SUFFICIENT"):
    control, series, cycle = state["control"], state["series"], state["cycle"]
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        control.materialize_cycle_work(
            series_id=series["entity_id"],
            cycle_id=cycle["entity_id"],
            workflow_key=WORKFLOW,
            plan=plan(state),
        )
    response = client.post(f"{PREFIX}/works/{cycle['entity_id']}/execute", headers=HEADERS)
    assert response.status_code == 200, response.text
    route = response.json()["work"]["data"]["responsibilityRouting"]
    if route["status"] != "COMPLETED":
        return response, route, None
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        restarted = AutonomousOperatingControl(Database(str(path)))
        restarted.request_cycle_close(series_id=series["entity_id"], cycle_id=cycle["entity_id"])
        closed = restarted.accept_and_close_cycle(
            series_id=series["entity_id"],
            cycle_id=cycle["entity_id"],
            reason="内容资产与真实 Provider 证据已完成有界验收",
        )
        evidence_ref = closed["data"]["evidenceRefs"][0]
        evaluation = restarted.evaluate_closed_cycle(
            series_id=series["entity_id"],
            cycle_id=cycle["entity_id"],
            contract=evaluation_contract(),
            outcome="SUCCESS" if sufficiency == "SUFFICIENT" else "INSUFFICIENT",
            observed_facts=[{
                "name": "xhs_content_asset_readiness",
                "value": {
                    "contentItemRef": state["content"]["entity_id"],
                    "valueMeaning": "REVIEWABLE_CONTENT_ASSET",
                    "publication": "NOT_CONNECTED",
                    "analytics": "UNAVAILABLE",
                },
                "sourceRef": evidence_ref,
            }],
            comparison={
                "expected": "reviewable content asset with truthful external boundaries",
                "observed": "provider-backed content package; no publication or analytics claim",
            },
            confidence="HIGH" if sufficiency == "SUFFICIENT" else "UNKNOWN",
            sufficiency=sufficiency,
        )
    return response, route, evaluation


def test_xhs_uses_same_lifecycle_with_distinct_domain_truth_and_restart_replay(tmp_path):
    path = tmp_path / "xhs-cross-domain-success.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = setup(path, client, provider)
        _, route, evaluation = execute_close_evaluate(path, client, state)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            restarted = AutonomousOperatingControl(Database(str(path)))
            decision = restarted.review_next_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle"]["entity_id"],
                decision="WAIT",
                reason="内容资产已形成；等待真实发布能力与外部观察窗口",
                wait_reason="发布与分析连接尚未接入",
                next_check_at="2026-08-22T15:00:00+00:00",
            )
            replay = restarted.review_next_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle"]["entity_id"],
                decision="WAIT",
                reason="内容资产已形成；等待真实发布能力与外部观察窗口",
                wait_reason="发布与分析连接尚未接入",
                next_check_at="2026-08-22T15:00:00+00:00",
            )
            assert replay["entity_id"] == decision["entity_id"]
            stopped = restarted.authorize_successor(decision["entity_id"])
            assert stopped["created"] is False
            assert stopped["claim"] is None and stopped["cycle"] is None
            content = RuntimeFoundation(restarted.db).get(state["content"]["entity_id"])
            cycle = RuntimeFoundation(restarted.db).get(state["cycle"]["entity_id"])
            assert content["lifecycle_status"] == "DRAFT"
            assert "acceptedLearning" not in cycle["data"] and "learning" not in cycle["data"]
        assert evaluation["observedFacts"][0]["value"]["valueMeaning"] == "REVIEWABLE_CONTENT_ASSET"
        assert route["status"] == "COMPLETED" and route["currentExecutorRef"] is None
        assert [item["result_type"] for item in provider.calls] == [
            "xhs-topic-plan",
            "xhs-research-brief",
            "xhs-publish-package",
        ]
        assert len({item["session"] for item in provider.calls}) == 3
        assert all("publicationStatus" in json.loads(item["output"]) for item in _task_outputs(state["database"]))
        with TenantContext.scope("different-tenant", company_id=COMPANY, ceo_id=CEO, role="test"):
            with pytest.raises(KeyError):
                AutonomousOperatingControl(Database(str(path))).get_series(state["series"]["entity_id"])


def _task_outputs(database: Database) -> list[dict]:
    with database.connect() as connection:
        rows = connection.execute(
            "select output from tasks where tenant_id=? order by created_at, task_id",
            (TENANT,),
        ).fetchall()
    return [{"output": row["output"]} for row in rows]


@pytest.mark.parametrize("failure", ["capability", "malformed"])
def test_xhs_capability_or_domain_result_failure_is_fail_closed(tmp_path, failure):
    path = tmp_path / f"xhs-cross-domain-{failure}.sqlite"
    provider = XHSProvider(malformed=failure == "malformed")
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = setup(path, client, provider)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            if failure == "capability":
                with state["database"].connect() as connection:
                    connection.execute(
                        "update tenant_private_capabilities set status='disabled' where tenant_id=? and capability_id=?",
                        (TENANT, CAPABILITY),
                    )
                with pytest.raises(AutonomousControlError, match="capability is unavailable"):
                    state["control"].materialize_cycle_work(
                        series_id=state["series"]["entity_id"],
                        cycle_id=state["cycle"]["entity_id"],
                        workflow_key=WORKFLOW,
                        plan=plan(state),
                    )
                assert provider.calls == []
                return
        _, route, evaluation = execute_close_evaluate(path, client, state)
        assert evaluation is None
        assert route["status"] == "WAITING"
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            failed = state["control"].fail_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle"]["entity_id"],
                reason="invalid XHS Result contract",
            )
            assert failed["lifecycle_status"] == "FAILED"
            assert "acceptedLearning" not in failed["data"]


def test_xhs_insufficient_evidence_requires_escalation_and_no_successor(tmp_path):
    path = tmp_path / "xhs-cross-domain-insufficient.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = setup(path, client, provider)
        _, _, evaluation = execute_close_evaluate(path, client, state, sufficiency="INSUFFICIENT")
        assert evaluation["sufficiency"] == "INSUFFICIENT"
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            with pytest.raises(AutonomousControlError, match="cannot continue"):
                state["control"].review_next_cycle(
                    series_id=state["series"]["entity_id"],
                    cycle_id=state["cycle"]["entity_id"],
                    decision="CONTINUE",
                    reason="must not continue with insufficient evidence",
                )
            packet = state["control"].review_next_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle"]["entity_id"],
                decision="ESCALATE",
                reason="内容来源不足，需要 CEO 判断是否补充资料",
            )
            assert packet["lifecycle_status"] == "WAITING_CEO"
            assert packet["data"]["ceoGateRequired"] is True
            assert packet["data"]["successorCycleRef"] is None


def test_xhs_protected_strategy_adjustment_requires_ceo_gate(tmp_path):
    path = tmp_path / "xhs-cross-domain-envelope.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = setup(path, client, provider)
        execute_close_evaluate(path, client, state)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            packet = state["control"].review_next_cycle(
                series_id=state["series"]["entity_id"],
                cycle_id=state["cycle"]["entity_id"],
                decision="ADJUST",
                reason="external publication would change protected authority",
                adjustment={"changes": {"externalPublish": "AUTO"}},
            )
            assert packet["lifecycle_status"] == "WAITING_CEO"
            assert packet["data"]["requestedDecision"] == "ADJUST"
            assert packet["data"]["decision"] == "ESCALATE"
            assert packet["data"]["authorityBasis"] == "CEO_GATE_OUTSIDE_APPROVED_STRATEGY_ENVELOPE"
            assert packet["data"]["successorCycleRef"] is None


def test_xhs_stale_goal_or_unavailable_leader_fails_closed(tmp_path):
    path = tmp_path / "xhs-cross-domain-authority.sqlite"
    provider = XHSProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        state = setup(path, client, provider)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            with state["database"].connect() as connection:
                row = connection.execute(
                    "select blueprint_json from workspaces where tenant_id=? and workspace_id=?",
                    (TENANT, state["workspace_id"]),
                ).fetchone()
                changed = json.loads(row["blueprint_json"])
                changed["goal"] = "unauthorized changed goal"
                connection.execute(
                    "update workspaces set blueprint_json=? where tenant_id=? and workspace_id=?",
                    (json.dumps(changed), TENANT, state["workspace_id"]),
                )
            with pytest.raises(AutonomousControlError, match="Goal pins"):
                state["control"].materialize_cycle_work(
                    series_id=state["series"]["entity_id"],
                    cycle_id=state["cycle"]["entity_id"],
                    workflow_key=WORKFLOW,
                    plan=plan(state),
                )

    second_path = tmp_path / "xhs-cross-domain-leader.sqlite"
    second_provider = XHSProvider()
    with TestClient(create_app(str(second_path), tool_functions={"model_gateway_tool": second_provider.execute})) as client:
        state = setup(second_path, client, second_provider)
        _, _, _ = execute_close_evaluate(second_path, client, state)
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
            with state["database"].connect() as connection:
                connection.execute(
                    "update runtime_entities set lifecycle_status='PAUSED' where tenant_id=? and entity_id=?",
                    (TENANT, state["employees"]["leader"]),
                )
            with pytest.raises(AutonomousControlError, match="Leader is unavailable"):
                state["control"].review_next_cycle(
                    series_id=state["series"]["entity_id"],
                    cycle_id=state["cycle"]["entity_id"],
                    decision="WAIT",
                    reason="leader unavailable",
                    wait_reason="leader unavailable",
                    next_check_at="2026-08-22T16:00:00+00:00",
                )
