from __future__ import annotations

import json
import os
import re
import sys

from fastapi.testclient import TestClient

from app.agent_adapter import CodexCliAdapter
from app.ai_usage import AIUsageService
from app.database import Database
from app.main import create_app
from app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from app.runtime.child_work import CanonicalChildWorkRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business
from backend.tests.test_rd_workspace_real_execution import (
    COMPANY,
    CEO,
    HEADERS,
    PROJECT,
    TENANT,
    blueprint as rd_blueprint,
)
from backend.tests.test_v1_general_operating_contract import (
    BUSINESS as GENERAL_BUSINESS,
    COMPANY as GENERAL_COMPANY,
    TENANT as GENERAL_TENANT,
    WORKSPACE as GENERAL_WORKSPACE,
    seed as seed_general_workspace,
)


def _rd_workspace(client: TestClient, database: Database) -> str:
    created = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "business_ref": "business-rd-real-slice",
            "business_type": "RD",
            "name": "Canonical RD",
            "blueprint_version": "v1",
            "blueprint": rd_blueprint(),
        },
    )
    assert created.status_code == 201, created.text
    workspace_id = created.json()["workspace"]["workspace_id"]
    simulation_response = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
        headers=HEADERS,
        json={"ceo_id": CEO, "scenario_id": "ORG-001", "blueprint_version": "v1"},
    )
    assert simulation_response.status_code == 201, simulation_response.text
    simulation = simulation_response.json()
    simulation_id = simulation["simulation_run_id"]
    for path, payload in (
        ("transition", {"ceo_id": CEO, "target": "RUNNING", "trigger": "start"}),
        ("execute", {"ceo_id": CEO, "target": "RUNNING", "trigger": "validate"}),
    ):
        response = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/{path}",
            headers=HEADERS,
            json=payload,
        )
        assert response.status_code == 200, response.text
        if path == "execute":
            evidence_refs = response.json()["evidence_refs"]
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
        headers=HEADERS,
        json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": evidence_refs},
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/capability-supply-review",
        headers=HEADERS,
        json={"ceo_id": CEO, "selections": [{
            "requirement_ref": "requirement:codex-runtime",
            "source": "tenant_private",
            "capability_type": "agent",
            "capability_id": "agent.codex.rd",
        }]},
    ).status_code == 200
    assert client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
        headers=HEADERS,
        json={"ceo_id": CEO, "choice": "APPROVE", "reason": "M4 canonical RD"},
    ).status_code == 200
    with database.connect() as connection:
        employee = connection.execute(
            "select entity_id from runtime_entities where tenant_id=? and workspace_id=? "
            "and entity_type='AI_EMPLOYEE'",
            (TENANT, workspace_id),
        ).fetchone()
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values (?, ?, ?, ?, 'template-rd-m4', '研发员工', 'developer', 'idle')",
            (employee["entity_id"], TENANT, COMPANY, f"department-{COMPANY}"),
        )
        connection.execute(
            "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
            "values ('binding-rd-m4', ?, ?, 'tenant_private', 'agent', 'agent.codex.rd')",
            (TENANT, employee["entity_id"]),
        )
    return workspace_id


def test_m4_rd_task_records_canonical_and_optional_project_attribution(tmp_path, monkeypatch):
    db_path = tmp_path / "m4-rd.sqlite"
    root = tmp_path / "project"
    (root / "src").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "src" / "calc.py").write_text("def add(a, b):\n    return a - b\n")
    (root / "tests" / "test_calc.py").write_text(
        "from src.calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
    )

    def execute(self, prompt: str, *, session_id: str = ""):
        (root / "src" / "calc.py").write_text("def add(a, b):\n    return a + b\n")
        return {
            "output": "已修复加法函数并运行测试。",
            "cost": 0,
            "estimated_cost": 0,
            "ledger_cost_source": "unknown",
            "metering_status": "confirmed",
            "model_gateway_id": "codex-local-agent",
            "model_name": "codex-cli",
            "provider_id": "openai_codex",
            "prompt_tokens": 8,
            "completion_tokens": 5,
            "total_tokens": 13,
            "status": "success",
            "http_status": 200,
            "latency_ms": 1,
            "outbound_attempted": True,
            "session_id": "m4-codex-session",
            "progress": ["thread.started", "item.completed"],
            "artifacts": [],
            "permissions": {},
            "computer_access": self._access_snapshot(
                session_id="m4-codex-session", is_resume=False, command_accepted=True,
            ),
            "resume_supported": True,
            "cancel_supported": False,
        }

    if os.getenv("CURIS_RUN_LIVE_CODEX") != "1":
        monkeypatch.setattr(CodexCliAdapter, "execute", execute)
    app = create_app(str(db_path))
    database = Database(str(db_path))
    database.initialize()
    department = f"department-{COMPANY}"
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'M4 RD Company')",
            (COMPANY, TENANT, CEO),
        )
    seed_canonical_business(database, TENANT, COMPANY, "business-rd-real-slice", department_id=department)
    with database.connect() as connection:
        connection.execute(
            "insert into projects(project_id, tenant_id, company_id, department_id, name, goal, status) "
            "values (?, ?, ?, ?, 'RD Project', 'canonical execution', 'active')",
            (PROJECT, TENANT, COMPANY, department),
        )
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="agent",
        capability_id="agent.codex.rd",
        display_name="Codex Runtime",
        metadata={
            "kind": "codex-cli",
            "cwd": str(root),
                "computer_access_intent": "AUTO_WITHIN_BOUNDARY",
                "live_status": "available",
                "permissions": ["workspace.write"],
                "cost_per_unit": 0,
        },
    )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="test"):
        RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)

    with TestClient(app) as client:
        workspace_id = _rd_workspace(client, database)
        created = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "owner_ref": "CEO Assistant",
                "outcome_ref": "函数与测试通过",
                "intent_ref": "修复加法函数",
                "blueprint_version": "v1",
                "project_ref": PROJECT,
                "work_item_title": "修复加法函数",
                "instruction": "修复 src/calc.py 的 add 函数",
                "resource_refs": ["src/calc.py", "tests/test_calc.py"],
                "test_command": [sys.executable, "-m", "pytest", "-q"],
                "requested_access_intent": "AUTO_WITHIN_BOUNDARY",
            },
        )
        cycle_id = created.json()["entity_id"]
        assert client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/start",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "M4 real execution"},
        ).status_code == 200
        response = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles/{cycle_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "run Codex"},
        )
        assert response.status_code == 202, response.text

    with TenantContext.scope(TENANT):
        usage = AIUsageService(database).list_records(project_id=PROJECT)
    assert usage
    assert {record["workspace_id"] for record in usage} == {workspace_id}
    assert {record["business_id"] for record in usage} == {"business-rd-real-slice"}
    assert {record["project_id"] for record in usage} == {PROJECT}
    assert all(record["work_ref"] and record["execution_ref"] for record in usage)
    record = usage[0]
    with database.connect() as connection:
        work = connection.execute(
            "select entity_type, parent_id from runtime_entities where tenant_id=? and entity_id=?",
            (TENANT, record["work_ref"]),
        ).fetchone()
        task = connection.execute(
            "select status, workspace_id, work_ref, execution_ref, project_id from tasks where task_id=?",
            (record["task_id"],),
        ).fetchone()
    assert tuple(work) == ("WORK", cycle_id)
    assert tuple(task)[1:] == (workspace_id, record["work_ref"], record["execution_ref"], PROJECT)
    assert task["status"] == "COMPLETED"
    assert (root / "src" / "calc.py").read_text().endswith("return a + b\n")

    restarted = Database(str(db_path))
    restarted.initialize()
    with TenantContext.scope(TENANT):
        assert AIUsageService(restarted).get_record(record["usage_record_id"]) == record


class _ContentGrowthProvider:
    def __init__(self):
        self.calls = []

    def execute(self, prompt: str):
        match = re.search(r"输出结果类型：([^\n]+)", prompt)
        result_type = match.group(1).strip() if match else "content-growth-result"
        session_id = f"content-growth-session-{len(self.calls) + 1}"
        self.calls.append({"prompt": prompt, "result_type": result_type, "session_id": session_id})
        if result_type == "content-growth-evaluation":
            body = {
                "status": "REJECTED", "resultType": result_type,
                "summary": "没有真实渠道结果，不能形成经营结论。",
                "problem": "缺少真实发布回执与 Analytics 数据",
            }
        else:
            body = {
                "status": "ACCEPTED", "resultType": result_type,
                "summary": "已基于当前输入形成可追溯结果。", "problem": "",
            }
        return {
            "output": json.dumps(body, ensure_ascii=False), "status": "success",
            "session_id": session_id, "outbound_attempted": False,
            "total_tokens": 9, "estimated_cost": 0,
        }


def _accept_content_work(database: Database, work_ref: str, route: dict) -> dict:
    with TenantContext.scope(
        GENERAL_TENANT, company_id=GENERAL_COMPANY, ceo_id="ceo", role="test",
    ):
        foundation = RuntimeFoundation(database)
        evidence = foundation.create(
            "EVIDENCE", company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
            parent_id=work_ref, owner_ref=route["responsibilityHolderRef"],
            lifecycle_status="CURRENT", verification_status="VERIFIED",
            evidence_condition="CURRENT",
            data={"providerEvidenceRefs": route["evidenceRefs"], "resultRefs": route["resultRefs"]},
        )
        acceptance = foundation.create(
            "ACCEPTANCE", company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
            parent_id=work_ref, owner_ref=route["responsibilityHolderRef"],
            data={"resultRefs": route["resultRefs"], "evidenceRefs": [evidence["entity_id"]]},
        )
        foundation.transition(acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept")
        foundation.transition(acceptance["entity_id"], "CLOSED", actor="SYSTEM", trigger="close")
        return CanonicalChildWorkRuntime(database).complete_work(
            work_ref, result_refs=route["resultRefs"], artifact_refs=route["artifactRefs"],
            evidence_refs=[evidence["entity_id"]], acceptance_refs=[acceptance["entity_id"]],
        )


def test_m5_content_growth_headless_uses_shared_multi_work_and_waits_for_real_channel_data(tmp_path):
    path = tmp_path / "m5-content-growth.sqlite"
    provider = _ContentGrowthProvider()
    live_codex = os.getenv("CURIS_RUN_LIVE_CODEX") == "1"
    employee_tool = (
        CodexCliAdapter(
            cwd=str(tmp_path), requested_intent="ASK_WHEN_NEEDED", timeout=300,
        ).execute
        if live_codex else provider.execute
    )
    with TestClient(create_app(
        str(path), tool_functions={"model_gateway_tool": employee_tool},
    )) as client:
        database = seed_general_workspace(path)
        database.save_tenant_private_capability(
            tenant_id=GENERAL_TENANT, capability_type="agent",
            capability_id="agent.content-growth.controlled",
            display_name="Content Growth controlled provider",
            metadata={"kind": "accepted-local-test-provider"},
        )
        with database.connect() as connection:
            connection.execute(
                "update canonical_businesses set name='内容增长业务', goal='形成可验证的内容增长方法' "
                "where business_id=?", (GENERAL_BUSINESS,),
            )
            connection.execute(
                "update workspaces set name='内容增长办公室', blueprint_json=? where workspace_id=?",
                (json.dumps({"productForm": "GENERIC", "domain": "CONTENT_GROWTH"}), GENERAL_WORKSPACE),
            )
        employees = {}
        assignments = {}
        specs = (
            ("research", "研究员工", "研究事实与受众", "content-growth-research"),
            ("content", "内容员工", "形成内容方案", "content-growth-content"),
            (
                "evaluation", "评估员工",
                "基于真实回执评估结果；没有真实发布回执或 Analytics 时必须 REJECTED",
                "content-growth-evaluation",
            ),
        )
        with TenantContext.scope(
            GENERAL_TENANT, company_id=GENERAL_COMPANY, ceo_id="ceo", role="test",
        ):
            foundation = RuntimeFoundation(database)
            routing = ResponsibilityRoutingRuntime(database)
            for key, name, responsibility, result_type in specs:
                employee_id = f"content-growth-{key}-employee"
                with database.connect() as connection:
                    connection.execute(
                        "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, "
                        "name, role, status) values (?, ?, ?, 'department', ?, ?, ?, 'idle')",
                        (employee_id, GENERAL_TENANT, GENERAL_COMPANY, f"template-{key}", name, key),
                    )
                    connection.execute(
                        "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, "
                        "capability_type, capability_id) values (?, ?, ?, 'tenant_private', 'agent', "
                        "'agent.content-growth.controlled')",
                        (f"binding-content-growth-{key}", GENERAL_TENANT, employee_id),
                    )
                role = foundation.create(
                    "ROLE_SLOT", company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
                    data={"name": name, "responsibility": responsibility},
                )
                foundation.create(
                    "AI_EMPLOYEE", entity_id=employee_id, company_id=GENERAL_COMPANY,
                    workspace_id=GENERAL_WORKSPACE, lifecycle_status="AVAILABLE", data={"name": name},
                )
                assignment = routing.create_assignment(
                    company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
                    scope_type="WORKSPACE", scope_ref=GENERAL_WORKSPACE,
                    role_ref=role["entity_id"], employee_ref=employee_id,
                    responsibility_key=f"content-growth-{key}", responsibility=responsibility,
                    input_contract={"requiredRefs": {
                        "research": ["brief:content-growth-goal"],
                        "content": ["accepted-predecessor-result"],
                        "evaluation": [
                            "publication-receipt:NOT_CONNECTED", "analytics:UNAVAILABLE",
                        ],
                    }[key]},
                    output_contract={"requiresResult": True, "resultType": result_type},
                )
                routing.publish_workflow(
                    company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
                    scope_type="WORKSPACE", scope_ref=GENERAL_WORKSPACE,
                    workflow_key=f"content-growth-{key}", assignment_refs=[assignment["entity_id"]],
                    default_flow=[f"content-growth-{key}"],
                )
                employees[key], assignments[key] = employee_id, assignment
            cycle = foundation.create(
                "CYCLE", company_id=GENERAL_COMPANY, workspace_id=GENERAL_WORKSPACE,
                lifecycle_status="RUNNING", data={"goal": "研究、内容与真实结果评估"},
            )
            child = CanonicalChildWorkRuntime(database)
            work = child.create_work(
                cycle_id=cycle["entity_id"], assignment_ref=assignments["research"]["entity_id"],
                release_key="research", input_refs=["brief:content-growth-goal"],
            )

        accepted_work_refs = []
        for key, next_key in (("research", "content"), ("content", "evaluation")):
            with TenantContext.scope(
                GENERAL_TENANT, company_id=GENERAL_COMPANY, ceo_id="ceo", role="test",
            ):
                routing = ResponsibilityRoutingRuntime(database)
                routing.start_work(
                    work["entity_id"], scope_type="WORKSPACE", scope_ref=GENERAL_WORKSPACE,
                    workflow_key=f"content-growth-{key}",
                )
                child = CanonicalChildWorkRuntime(database)
                child.transition_work(work["entity_id"], "READY", actor="SYSTEM")
                child.transition_work(work["entity_id"], "ACTIVE", actor=employees[key])
            response = client.post(
                f"/api/workspace/runtime/foundation/team-operating/works/{work['entity_id']}/execute?max_executions=1",
                headers={"X-Tenant-Id": GENERAL_TENANT, "X-Ceo-Id": "ceo"},
            )
            assert response.status_code == 200, response.text
            route = response.json()["work"]["data"]["responsibilityRouting"]
            if live_codex and route["status"] == "WAITING":
                assert route["currentExecutorRef"] is None
                assert "brief:content-growth-goal" in json.dumps(route, ensure_ascii=False)
                with database.connect() as connection:
                    assert connection.execute(
                        "select count(*) from runtime_entities where entity_type='WORK'"
                    ).fetchone()[0] == 1
                    assert connection.execute(
                        "select count(*) from runtime_entities where entity_type='HANDOFF'"
                    ).fetchone()[0] == 0
                    assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
                restarted = Database(str(path))
                restarted.initialize()
                with TenantContext.scope(GENERAL_TENANT):
                    recovered = RuntimeFoundation(restarted).get(work["entity_id"])
                assert recovered["data"]["responsibilityRouting"]["status"] == "WAITING"
                return
            assert route["status"] == "COMPLETED" and route["currentExecutorRef"] is None
            completed = _accept_content_work(database, work["entity_id"], route)
            accepted_work_refs.append(work["entity_id"])
            with TenantContext.scope(
                GENERAL_TENANT, company_id=GENERAL_COMPANY, ceo_id="ceo", role="test",
            ):
                released = CanonicalChildWorkRuntime(database).release_next_work(
                    work["entity_id"], release_key=next_key,
                    target_assignment_ref=assignments[next_key]["entity_id"],
                    accepted_result_ref=completed["data"]["resultRefs"][0],
                    input_refs=(
                        completed["data"]["resultRefs"]
                        + (["capability:publishing=NOT_CONNECTED", "capability:analytics=UNAVAILABLE"]
                           if next_key == "evaluation" else [])
                    ),
                    reason=f"{key}结果已验收",
                )
                work = released["work"]

        with TenantContext.scope(
            GENERAL_TENANT, company_id=GENERAL_COMPANY, ceo_id="ceo", role="test",
        ):
            routing = ResponsibilityRoutingRuntime(database)
            routing.start_work(
                work["entity_id"], scope_type="WORKSPACE", scope_ref=GENERAL_WORKSPACE,
                workflow_key="content-growth-evaluation",
            )
            child = CanonicalChildWorkRuntime(database)
            child.transition_work(work["entity_id"], "READY", actor="SYSTEM")
            child.transition_work(work["entity_id"], "ACTIVE", actor=employees["evaluation"])
        waiting = client.post(
            f"/api/workspace/runtime/foundation/team-operating/works/{work['entity_id']}/execute?max_executions=1",
            headers={"X-Tenant-Id": GENERAL_TENANT, "X-Ceo-Id": "ceo"},
        )
        assert waiting.status_code == 200, waiting.text
        waiting_route = waiting.json()["work"]["data"]["responsibilityRouting"]
        assert waiting_route["status"] == "WAITING"
        assert waiting_route["currentExecutorRef"] is None
        assert "真实发布回执" in json.dumps(waiting_route, ensure_ascii=False)

    if not live_codex:
        assert len(provider.calls) == 3
    with database.connect() as connection:
        usage_events = [json.loads(row["payload"]) for row in connection.execute(
            "select payload from evolution_events where event_type='usage.task_execution' order by event_id"
        ).fetchall()]
        execution_events = [json.loads(row["payload"]) for row in connection.execute(
            "select payload from evolution_events where event_type='execution_started' order by event_id"
        ).fetchall()]
        assert len(usage_events) == 3
        assert all(item["workspace_id"] == GENERAL_WORKSPACE for item in usage_events)
        assert all(not item.get("project_id") for item in usage_events)
        assert len(execution_events) == 3
        assert all(item["business_id"] == GENERAL_BUSINESS for item in execution_events)
        assert all(item["workspace_id"] == GENERAL_WORKSPACE for item in execution_events)
        assert all(not item.get("project_id") for item in execution_events)
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='WORK'"
        ).fetchone()[0] == 3
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='HANDOFF'"
        ).fetchone()[0] == 2
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type='DECISION_PACKET'"
        ).fetchone()[0] == 0
        assert connection.execute("select count(*) from projects").fetchone()[0] == 0
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
    restarted = Database(str(path))
    restarted.initialize()
    with TenantContext.scope(GENERAL_TENANT):
        aggregate = CanonicalChildWorkRuntime(restarted).aggregate_cycle(
            cycle["entity_id"], require_complete=False,
        )
    assert len(aggregate["workRefs"]) == 3
    assert set(accepted_work_refs).issubset(aggregate["workRefs"])
