from __future__ import annotations

import json
import re
import threading

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-team-real-e2e"
COMPANY = "company-team-real-e2e"
WORKSPACE = "workspace-team-real-e2e"
BUSINESS = "business-team-real-e2e"
CAPABILITY = "agent.team.local"
PREFIX = "/api/workspace/runtime/foundation/team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo-team-real-e2e"}


class DeterministicProvider:
    """Approved local provider double using the real Task/Session/callback path."""

    def __init__(self):
        self.calls: list[dict] = []

    def execute(self, prompt: str) -> dict:
        match = re.search(r"输出结果类型：([^\n]+)", prompt)
        result_type = match.group(1).strip() if match else "generic-result"
        session = f"local-session-{len(self.calls) + 1}"
        payload = {
            "status": "ACCEPTED",
            "resultType": result_type,
            "summary": f"{result_type} 已完成",
            "problem": "",
        }
        self.calls.append({"session": session, "result_type": result_type, "prompt": prompt})
        return {
            "output": json.dumps(payload, ensure_ascii=False),
            "status": "success",
            "session_id": session,
            "outbound_attempted": False,
            "total_tokens": 8,
            "estimated_cost": 0,
        }


class RevisionProvider(DeterministicProvider):
    def execute(self, prompt: str) -> dict:
        result = super().execute(prompt)
        if self.calls[-1]["result_type"] == "quality-result":
            quality_calls = sum(item["result_type"] == "quality-result" for item in self.calls)
            payload = json.loads(result["output"])
            if quality_calls == 1:
                payload.update({"status": "REJECTED", "summary": "需要修订", "problem": "验收条件未满足"})
                result["output"] = json.dumps(payload, ensure_ascii=False)
        return result


class AlwaysRejectProvider(RevisionProvider):
    def execute(self, prompt: str) -> dict:
        result = super().execute(prompt)
        if self.calls[-1]["result_type"] == "quality-result":
            payload = json.loads(result["output"])
            payload.update({"status": "REJECTED", "summary": "仍需修订", "problem": "验收条件仍未满足"})
            result["output"] = json.dumps(payload, ensure_ascii=False)
        return result


class MalformedProvider(DeterministicProvider):
    def execute(self, prompt: str) -> dict:
        result = super().execute(prompt)
        result["output"] = "provider returned text without the required Result contract"
        return result


class BlockingProvider(DeterministicProvider):
    def __init__(self):
        super().__init__()
        self.started = threading.Event()
        self.release = threading.Event()

    def execute(self, prompt: str) -> dict:
        self.started.set()
        assert self.release.wait(5)
        return super().execute(prompt)


def seed(path):
    database = Database(str(path))
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo-team-real-e2e', 'Team E2E')",
            (COMPANY, TENANT),
        )
        connection.execute(
            "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
            "values (?, ?, '内容增长', 'CUSTOM', '可发布内容方案', 'ACTIVE')",
            (BUSINESS, TENANT),
        )
    seed_canonical_business(database, TENANT, COMPANY, BUSINESS)
    with database.connect() as connection:
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values (?, ?, ?, ?, '内容增长办公室', 'OPERATING', 'v1', 'RESOLVED', '', 'CANONICAL_TEST')",
            (WORKSPACE, TENANT, COMPANY, BUSINESS),
        )
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="agent", capability_id=CAPABILITY,
        display_name="Deterministic Local Agent", metadata={"kind": "approved-local-test-provider"},
    )
    employees = {}
    templates = {
        "leader": "et_tech_lead", "topic": "et_product_manager",
        "research": "et_architect", "copy": "et_frontend_engineer",
    }
    with TenantContext.scope(TENANT):
        foundation = RuntimeFoundation(database)
        for key in ("leader", "topic", "research", "copy"):
            employee_id = f"employee-{key}"
            with database.connect() as connection:
                connection.execute(
                    "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                    "values (?, ?, ?, '', ?, ?, ?, 'idle')",
                    (employee_id, TENANT, COMPANY, templates[key], key, key),
                )
                connection.execute(
                    "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
                    "values (?, ?, ?, 'tenant_private', 'agent', ?)",
                    (f"binding-{key}", TENANT, employee_id, CAPABILITY),
                )
            employees[key] = foundation.create(
                "AI_EMPLOYEE", entity_id=employee_id, company_id=COMPANY,
                workspace_id=WORKSPACE, lifecycle_status="AVAILABLE", data={"name": key},
            )["entity_id"]
    return database, employees


def publish_and_start(client, database, employees, work_ref="content-work"):
    roles = [
        {
            "responsibility_key": "leader", "role_name": "负责人", "employee_ref": employees["leader"],
            "responsibility": "处理经营咨询", "input_contract": {},
            "output_contract": {"requiresResult": True, "resultType": "leader-advice"}, "is_leader": True,
        },
        {
            "responsibility_key": "topic", "role_name": "选题", "employee_ref": employees["topic"],
            "responsibility": "形成选题", "input_contract": {"requiredRefs": ["work"]},
            "output_contract": {"requiresResult": True, "resultType": "topic-plan"},
        },
        {
            "responsibility_key": "research", "role_name": "调研", "employee_ref": employees["research"],
            "responsibility": "完成调研", "input_contract": {
                "requiredRefs": ["work", "topic-plan"], "consultResponsibility": "leader",
                "consultQuestion": "确认本次内容方向",
            },
            "output_contract": {"requiresResult": True, "resultType": "research-brief"},
        },
        {
            "responsibility_key": "copy", "role_name": "文案", "employee_ref": employees["copy"],
            "responsibility": "形成可发布内容方案", "input_contract": {"requiredRefs": ["research-brief"]},
            "output_contract": {"requiresResult": True, "resultType": "publish-package"},
        },
    ]
    response = client.post(
        f"{PREFIX}/definitions/publish", headers=HEADERS,
        json={
            "company_id": COMPANY, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE,
            "workspace_id": WORKSPACE, "workflow_key": "content-growth", "roles": roles,
            "default_flow": ["topic", "research", "copy"],
        },
    )
    assert response.status_code == 200, response.text
    with TenantContext.scope(TENANT):
        RuntimeFoundation(database).create(
            "CYCLE", entity_id=work_ref, company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "围绕指定主题生成一篇小红书内容方案"},
        )
    response = client.post(
        f"{PREFIX}/works/{work_ref}/start", headers=HEADERS,
        json={"scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": "content-growth"},
    )
    assert response.status_code == 200, response.text


def publish_revision_work(client, database, employees, work_ref, max_returns=2):
    roles = [
        {
            "responsibility_key": "copy", "role_name": "文案", "employee_ref": employees["copy"],
            "responsibility": "形成内容稿", "input_contract": {"requiredRefs": ["work"]},
            "output_contract": {"requiresResult": True, "resultType": "copy-result"},
        },
        {
            "responsibility_key": "research", "role_name": "审核", "employee_ref": employees["research"],
            "responsibility": "审核内容稿", "input_contract": {"requiredRefs": ["copy-result"]},
            "output_contract": {
                "requiresResult": True, "resultType": "quality-result",
                "returnResponsibility": "copy", "maxReturns": max_returns,
            },
        },
    ]
    response = client.post(
        f"{PREFIX}/definitions/publish", headers=HEADERS,
        json={
            "company_id": COMPANY, "scope_type": "WORKSPACE", "scope_ref": WORKSPACE,
            "workspace_id": WORKSPACE, "workflow_key": work_ref, "roles": roles,
            "default_flow": ["copy", "research"],
        },
    )
    assert response.status_code == 200, response.text
    with TenantContext.scope(TENANT):
        RuntimeFoundation(database).create(
            "CYCLE", entity_id=work_ref, company_id=COMPANY, workspace_id=WORKSPACE,
            lifecycle_status="RUNNING", data={"goal": "形成并审核内容稿"},
        )
    response = client.post(
        f"{PREFIX}/works/{work_ref}/start", headers=HEADERS,
        json={"scope_type": "WORKSPACE", "scope_ref": WORKSPACE, "workflow_key": work_ref},
    )
    assert response.status_code == 200, response.text


def test_real_employee_loop_restart_consult_completion_and_duplicate_safety(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-e2e.sqlite"
    provider = DeterministicProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_and_start(client, database, employees)
        first = client.post(f"{PREFIX}/works/content-work/execute?max_executions=1", headers=HEADERS)
        assert first.status_code == 200, first.text
        route = first.json()["work"]["data"]["responsibilityRouting"]
        assert first.json()["continuation_pending"] is True
        assert route["responsibilityHolderRef"] == employees["research"]
        assert route["currentExecutorRef"] is None
        assert len(route["executions"]) == 1
        assert len(route["handoffRefs"]) == 1

    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        resumed = client.post(f"{PREFIX}/works/content-work/execute", headers=HEADERS)
        assert resumed.status_code == 200, resumed.text
        route = resumed.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "COMPLETED"
        assert route["currentExecutorRef"] is None
        assert len(route["executions"]) == 4
        assert len(route["handoffRefs"]) == 2
        assert len(route["resultRefs"]) == 4
        consult = route["collaborations"][next(iter(route["collaborations"]))]
        assert consult["kind"] == "CONSULT" and consult["status"] == "COMPLETED"
        assert consult["holderEmployeeRef"] == employees["research"]
        assert consult["targetEmployeeRef"] == employees["leader"]
        assert all(item["provenance"]["verification_status"] == "VERIFIED" for item in route["executions"].values())
        assert all(item["contextMetrics"]["hydratedBodiesCount"] == 0 for item in route["executions"].values())
        assert all(item["contextMetrics"]["copiedConversationHistory"] is False for item in route["executions"].values())
        with database.connect() as connection:
            tasks_before = connection.execute("select count(*) from tasks").fetchone()[0]
        duplicate = client.post(f"{PREFIX}/works/content-work/execute", headers=HEADERS)
        assert duplicate.status_code == 200
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == tasks_before == 4
            assert connection.execute("select count(distinct json_extract(payload, '$.session_id')) from evolution_events where event_type='usage.task_execution'").fetchone()[0] == 4
            assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert len(provider.calls) == 4


def test_cancel_prevents_next_employee_and_preserves_completed_truth(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-cancel.sqlite"
    provider = DeterministicProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_and_start(client, database, employees, "cancel-work")
        assert client.post(f"{PREFIX}/works/cancel-work/execute?max_executions=1", headers=HEADERS).status_code == 200
        cancelled = client.post(
            f"{PREFIX}/works/cancel-work/cancel", headers=HEADERS, json={"reason": "CEO停止当前工作"},
        )
        assert cancelled.status_code == 200, cancelled.text
        route = cancelled.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "CANCELLED"
        assert route["currentExecutorRef"] is None
        assert len(route["executions"]) == 1
        assert len(route["resultRefs"]) == 1
        rerun = client.post(f"{PREFIX}/works/cancel-work/execute", headers=HEADERS)
        assert rerun.status_code == 200
        assert rerun.json()["work"]["data"]["responsibilityRouting"]["status"] == "CANCELLED"
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == 1


def test_rejected_result_returns_to_real_employee_then_qa_rechecks(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-return.sqlite"
    provider = RevisionProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_revision_work(client, database, employees, "revision-work")
        completed = client.post(f"{PREFIX}/works/revision-work/execute", headers=HEADERS)
        assert completed.status_code == 200, completed.text
        route = completed.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "COMPLETED"
        assert len(route["executions"]) == 4
        assert len(route["handoffRefs"]) == 3
        assert [item["resultStatus"] for item in route["executions"].values()] == [
            "ACCEPTED", "REJECTED", "ACCEPTED", "ACCEPTED",
        ]
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == 4
            assert connection.execute("select count(*) from runtime_entities where entity_type='DECISION_PACKET'").fetchone()[0] == 0
            assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_return_limit_stops_in_waiting_instead_of_looping(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-return-limit.sqlite"
    provider = AlwaysRejectProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_revision_work(client, database, employees, "return-limit-work", max_returns=1)
        response = client.post(f"{PREFIX}/works/return-limit-work/execute", headers=HEADERS)
        assert response.status_code == 200, response.text
        route = response.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "WAITING"
        assert route["currentExecutorRef"] is None
        assert len(route["executions"]) == 4
        assert len(route["handoffRefs"]) == 3
        assert sum(item["resultStatus"] == "REJECTED" for item in route["executions"].values()) == 2


def test_provider_success_without_valid_result_contract_does_not_advance(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-invalid-result.sqlite"
    provider = MalformedProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_and_start(client, database, employees, "invalid-result-work")
        response = client.post(f"{PREFIX}/works/invalid-result-work/execute", headers=HEADERS)
        assert response.status_code == 200, response.text
        route = response.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "WAITING"
        assert route["responsibilityHolderRef"] == employees["topic"]
        assert route["currentExecutorRef"] is None
        assert len(route["handoffRefs"]) == 0
        record = next(iter(route["executions"].values()))
        assert record["status"] == "FAILED"
        assert record["provenance"]["verification_status"] == "VERIFIED"
        with database.connect() as connection:
            assert connection.execute("select status from tasks").fetchone()[0] == "COMPLETED"


def test_missing_employee_capability_fails_closed_and_clears_executor(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-missing-capability.sqlite"
    provider = DeterministicProvider()
    with TestClient(create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})) as client:
        database, employees = seed(path)
        publish_and_start(client, database, employees, "missing-capability-work")
        with database.connect() as connection:
            connection.execute("update employee_capability_bindings set enabled=0 where employee_id=?", (employees["topic"],))
        response = client.post(f"{PREFIX}/works/missing-capability-work/execute", headers=HEADERS)
        assert response.status_code == 200, response.text
        route = response.json()["work"]["data"]["responsibilityRouting"]
        assert route["status"] == "WAITING"
        assert route["currentExecutorRef"] is None
        assert next(iter(route["executions"].values()))["status"] == "FAILED"
        with database.connect() as connection:
            assert connection.execute("select count(*) from tasks").fetchone()[0] == 0
        assert provider.calls == []


def test_cancel_active_provider_task_stops_continuation_without_orphan(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "team-real-active-cancel.sqlite"
    provider = BlockingProvider()
    app = create_app(str(path), tool_functions={"model_gateway_tool": provider.execute})
    with TestClient(app) as client:
        database, employees = seed(path)
        publish_and_start(client, database, employees, "active-cancel-work")
        outcome = {}

        def execute():
            outcome["response"] = client.post(f"{PREFIX}/works/active-cancel-work/execute", headers=HEADERS)

        thread = threading.Thread(target=execute)
        thread.start()
        assert provider.started.wait(5)
        cancelled = client.post(
            f"{PREFIX}/works/active-cancel-work/cancel", headers=HEADERS,
            json={"reason": "CEO停止正在执行的工作"},
        )
        assert cancelled.status_code == 200, cancelled.text
        provider.release.set()
        thread.join(5)
        assert not thread.is_alive()
        with TenantContext.scope(TENANT):
            route = RuntimeFoundation(database).get("active-cancel-work")["data"]["responsibilityRouting"]
        assert route["status"] == "CANCELLED"
        assert route["currentExecutorRef"] is None
        assert len(route["handoffRefs"]) == 0
        with database.connect() as connection:
            task = connection.execute("select status from tasks").fetchone()
            assert task["status"] == "CANCELLED"
            assert connection.execute("select count(*) from tasks").fetchone()[0] == 1


def _leader_synthetic_setup(path, provider, worker_keys=("topic", "copy")):
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    from app.model_gateway import ModelGatewayAdapter
    app = create_app(str(path), model_gateway_adapter=ModelGatewayAdapter(base_url="https://synthetic.invalid", api_key="synthetic",
        http_post=provider.http_post))
    database, employees = seed(path)
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=HEADERS["X-Ceo-Id"], role="owner"):
        foundation = RuntimeFoundation(database)
        routing = ResponsibilityRoutingRuntime(database)
        assignments = []
        for key in ("leader", *worker_keys):
            role = foundation.create("ROLE_SLOT", company_id=COMPANY, workspace_id=WORKSPACE, data={"name": key})
            # Two available bindings: the existing explicit preference must select the API model.
            database.save_tenant_private_capability(tenant_id=TENANT, capability_type="model",
                capability_id="model.leader.synthetic", display_name="Synthetic API", metadata={
                    "provider_type": "ollama", "base_url": "http://127.0.0.1:11434", "model_name": "synthetic"})
            with database.connect() as con:
                con.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                    "values (?, ?, ?, 'tenant_private', 'model', 'model.leader.synthetic')",
                    (f"api-{key}", TENANT, employees[key]))
            with database.connect() as con:
                con.execute("update employee_capability_bindings set priority=1 where tenant_id=? and id=?", (TENANT, f"api-{key}"))
            capability_ref = foundation.create("CAPABILITY_BINDING", company_id=COMPANY, workspace_id=WORKSPACE,
                lifecycle_status="ACTIVE", capability_ref="model.leader.synthetic")["entity_id"]
            assignments.append(routing.create_assignment(company_id=COMPANY, workspace_id=WORKSPACE,
                scope_type="WORKSPACE", scope_ref=WORKSPACE, role_ref=role["entity_id"], employee_ref=employees[key],
                responsibility_key=key, responsibility=f"{key} responsibility", is_leader=key == "leader",
                capability_binding_refs=[capability_ref], output_contract={"resultType": f"{key}-result"}))
        routing.publish_workflow(company_id=COMPANY, workspace_id=WORKSPACE, scope_type="WORKSPACE", scope_ref=WORKSPACE,
            workflow_key="leader-delegation", assignment_refs=[a["entity_id"] for a in assignments], default_flow=["leader"])
    provider.database = database
    provider.targets = [a["entity_id"] for a in assignments[1:]]
    return app, database, assignments


class LeaderSyntheticProvider(DeterministicProvider):
    def __init__(self, invalid=False, cancel=False):
        super().__init__()
        self.invalid = invalid
        self.cancel = cancel
        self.targets = []

    def http_post(self, url, payload, headers, timeout):
        result = self.execute(payload["messages"][-1]["content"])
        return {"choices": [{"message": {"content": result["output"]}}],
                "usage": {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8}}

    def execute(self, prompt):
        from app.runtime_capability_context import RuntimeCapabilityContext
        from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
        context = RuntimeCapabilityContext.current()
        result = super().execute(prompt)
        if "额外返回 delegations" in prompt:
            payload = json.loads(result["output"])
            payload["delegations"] = [{"assignmentRef": "unknown" if self.invalid else ref,
                "problem": f"bounded task {i}", "expectedResult": "verifiable result"} for i, ref in enumerate(self.targets)]
            result["output"] = json.dumps(payload)
        elif self.cancel and "汇总以下" not in prompt:
            root = RuntimeFoundation(self.database).get(context["work_ref"])["data"]["leaderRootWorkRef"]
            ResponsibilityRoutingRuntime(self.database).cancel_work(root, reason="synthetic owner cancellation")
        return result


def test_leader_autonomous_plan_children_original_summary_restart_and_binding_preference(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    provider = LeaderSyntheticProvider()
    path = tmp_path / "leader.sqlite"
    app, database, assignments = _leader_synthetic_setup(path, provider)

    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            created = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "coordinate existing employees", "expected_result": "original Work summary", "request_id": "leader-once"})
            assert created.status_code == 200, created.text
            ref = created.json()["work"]["entity_id"]
            first = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert first.status_code == 200, first.text
            assert first.json()["delegation_status"] == "ACCEPTED", first.text
            assert first.json()["acceptance_pending"] is True
            children = first.json()["child_work_refs"]
            assert len(children) == 2
            assert len(provider.calls) == 4
            assert "PENDING" in provider.calls[-1]["prompt"]
            # A new app/router instance must recover the same plan, tasks and summary.
            from app.model_gateway import ModelGatewayAdapter
            restarted = create_app(str(path), model_gateway_adapter=ModelGatewayAdapter(base_url="https://synthetic.invalid", api_key="synthetic",
                http_post=provider.http_post))
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=restarted), base_url="http://test", headers=HEADERS) as resumed:
                replay = await resumed.post(f"{PREFIX}/works/{ref}/execute")
                assert replay.status_code == 200, replay.text
                assert replay.json()["child_work_refs"] == children
            assert len(provider.calls) == 4
            with TenantContext.scope(TENANT):
                root = RuntimeFoundation(database).get(ref)
                assert root["lifecycle_status"] == "ACTIVE"
                assert root["data"]["responsibilityRouting"]["status"] == "ACTIVE"
                for child in children:
                    work = RuntimeFoundation(database).get(child)
                    assert work["parent_id"] == root["parent_id"]
                    assert work["data"]["leaderRootWorkRef"] == ref
                    assert not work["data"]["acceptanceRefs"]
            with database.connect() as con:
                tasks = con.execute("select requested_capability_type,work_ref from tasks where tenant_id=?", (TENANT,)).fetchall()
                assert len(tasks) == 4
                assert {t["requested_capability_type"] for t in tasks} == {"model"}
                assert {t["work_ref"] for t in tasks} == {ref, *children, first.json()["summary_work_ref"]}
                assert not con.execute("select 1 from runtime_entities where tenant_id=? and entity_type='ACCEPTANCE'", (TENANT,)).fetchone()
            from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
            import pytest
            with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=HEADERS["X-Ceo-Id"], role="owner"):
                runtime = CanonicalChildWorkRuntime(database)
                summary = RuntimeFoundation(database).get(first.json()["summary_work_ref"])
                result_ref = next(iter(summary["data"]["responsibilityRouting"]["executions"].values()))["resultRef"]
                proof = _leader_acceptance_receipts(database, ref, result_ref)
                with pytest.raises(ChildWorkError, match="explicit outcome acceptance"):
                    runtime.complete_work(ref, **proof)
                for work_ref in [*children, summary["entity_id"]]:
                    work = RuntimeFoundation(database).get(work_ref)
                    child_result = next(iter(work["data"]["responsibilityRouting"]["executions"].values()))["resultRef"]
                    runtime.complete_work(work_ref, **_leader_acceptance_receipts(database, work_ref, child_result))
                assert runtime.complete_work(ref, **proof)["lifecycle_status"] == "COMPLETED"
                assert runtime.aggregate_cycle(root["parent_id"], require_complete=True)
    asyncio.run(run())


def test_leader_unknown_target_never_retries_or_creates_children(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    provider = LeaderSyntheticProvider(invalid=True)
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-invalid.sqlite", provider)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            response = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "delegate", "expected_result": "result", "request_id": "invalid-plan"})
            assert response.status_code == 200, response.text
            ref = response.json()["work"]["entity_id"]
            for _ in range(2):
                bad = await client.post(f"{PREFIX}/works/{ref}/execute")
                assert bad.status_code == 422, bad.text
            assert len(provider.calls) == 1
            with TenantContext.scope(TENANT):
                root = RuntimeFoundation(database).get(ref)
                assert "leaderDelegation" not in root["data"]
            with database.connect() as con:
                assert con.execute("select count(*) from runtime_entities where tenant_id=? and entity_type='WORK'", (TENANT,)).fetchone()[0] == 1
    asyncio.run(run())


def test_leader_original_cancellation_stops_remaining_delegation(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    provider = LeaderSyntheticProvider(cancel=True)
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-cancel.sqlite", provider)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            response = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "delegate", "expected_result": "result", "request_id": "cancel-plan"})
            assert response.status_code == 200, response.text
            ref = response.json()["work"]["entity_id"]
            result = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert result.status_code == 200, result.text
            assert result.json()["delegation_status"] == "BLOCKED"
            assert len(provider.calls) == 2
            replay = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert replay.status_code == 200, replay.text
            assert len(provider.calls) == 2
            assert "summaryWorkRef" not in result.json()["work"]["data"]["leaderDelegation"]
    asyncio.run(run())


def _leader_acceptance_receipts(database, ref, result_ref):
    foundation = RuntimeFoundation(database)
    evidence = foundation.create("EVIDENCE", company_id=COMPANY, workspace_id=WORKSPACE, parent_id=ref,
        lifecycle_status="CURRENT", verification_status="VERIFIED", evidence_condition="CURRENT",
        data={"summary": "Synthetic owner reviewed this exact result"})
    acceptance = foundation.create("ACCEPTANCE", company_id=COMPANY, workspace_id=WORKSPACE, parent_id=ref,
        owner_ref=HEADERS["X-Ceo-Id"], data={"resultRefs": [result_ref], "evidenceRefs": [evidence["entity_id"]]})
    foundation.transition(acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept")
    foundation.transition(acceptance["entity_id"], "CLOSED", actor="SYSTEM", trigger="close")
    return {"result_refs": [result_ref], "artifact_refs": [], "evidence_refs": [evidence["entity_id"]],
            "acceptance_refs": [acceptance["entity_id"]]}


def test_leader_concurrent_execute_reuses_original_plan_claim(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    class BlockedLeader(LeaderSyntheticProvider):
        def __init__(self):
            super().__init__()
            self.started = threading.Event()
            self.release = threading.Event()
        def execute(self, prompt):
            if "额外返回 delegations" in prompt:
                self.started.set()
                assert self.release.wait(5)
            return super().execute(prompt)
    provider = BlockedLeader()
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-concurrent.sqlite", provider)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            response = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "delegate", "expected_result": "result", "request_id": "concurrent-plan"})
            assert response.status_code == 200, response.text
            ref = response.json()["work"]["entity_id"]
            first = asyncio.create_task(client.post(f"{PREFIX}/works/{ref}/execute"))
            try:
                assert await asyncio.to_thread(provider.started.wait, 3)
                second = await client.post(f"{PREFIX}/works/{ref}/execute")
                assert second.status_code == 200, second.text
                assert second.json()["delegation_status"] == "IN_PROGRESS"
            finally:
                provider.release.set()
            completed = await first
            assert completed.status_code == 200, completed.text
            assert completed.json()["delegation_status"] == "ACCEPTED"
            assert len(provider.calls) == 4
    asyncio.run(run())


def test_leader_partial_release_rolls_back_and_reuses_verified_plan(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from app.runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    provider = LeaderSyntheticProvider()
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-rollback.sqlite", provider)
    original = CanonicalChildWorkRuntime._activate_leader_child_locked
    released = []
    def fail_second(self, con, child, root, assignment, contract):
        released.append(child["entity_id"])
        if len(released) == 2:
            raise ChildWorkError("synthetic interrupted release")
        return original(self, con, child, root, assignment, contract)
    monkeypatch.setattr(CanonicalChildWorkRuntime, "_activate_leader_child_locked", fail_second)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            response = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "delegate", "expected_result": "result", "request_id": "rollback-plan"})
            assert response.status_code == 200, response.text
            ref = response.json()["work"]["entity_id"]
            interrupted = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert interrupted.status_code == 422, interrupted.text
            assert len(provider.calls) == 1
            with database.connect() as con:
                assert con.execute("select count(*) from runtime_entities where tenant_id=? and entity_type='WORK'", (TENANT,)).fetchone()[0] == 1
                assert not con.execute("select 1 from runtime_transition_log where tenant_id=? and entity_id=?", (TENANT, released[0])).fetchone()
            monkeypatch.setattr(CanonicalChildWorkRuntime, "_activate_leader_child_locked", original)
            recovered = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert recovered.status_code == 200, recovered.text
            assert recovered.json()["delegation_status"] == "ACCEPTED", recovered.text
            assert len(provider.calls) == 4
    asyncio.run(run())


def test_leader_without_other_responsibilities_executes_own_work(tmp_path, monkeypatch):
    import asyncio
    import httpx
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant_id, request_id:
        AuthorizedMembership("synthetic-owner", tenant_id, COMPANY, HEADERS["X-Ceo-Id"], "owner", "active", request_id))
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    provider = LeaderSyntheticProvider()
    app, database, assignments = _leader_synthetic_setup(tmp_path / "leader-single.sqlite", provider, worker_keys=())
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test", headers=HEADERS) as client:
            created = await client.post(f"{PREFIX}/assignments/{assignments[0]['entity_id']}/work", json={
                "problem": "ordinary own responsibility", "expected_result": "result", "request_id": "leader-single"})
            assert created.status_code == 200, created.text
            ref = created.json()["work"]["entity_id"]
            result = await client.post(f"{PREFIX}/works/{ref}/execute")
            assert result.status_code == 200, result.text
            assert result.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED", result.text
            assert "leaderDelegation" not in result.json()["work"]["data"]
            assert len(provider.calls) == 1
    asyncio.run(run())


def test_writing_model_work_creation_failure_is_atomic(tmp_path, monkeypatch):
    from backend.tests.test_writing_selected_execution import ready
    from backend.tests.test_writing_chapter_vertical import scope as writing_scope, COMPANY as writing_company, CEO as writing_ceo
    from app.runtime.child_work import CanonicalChildWorkRuntime
    from app.runtime.responsibility_routing import ResponsibilityRoutingRuntime
    db, app, entry, service, calls, w, b, c, binding = ready(tmp_path, monkeypatch)
    with writing_scope():
        assignment = entry.metadata(writing_company, w)["assignment_ref"]
        ResponsibilityRoutingRuntime(db).publish_workflow(company_id=writing_company, workspace_id=w,
            scope_type="WORKSPACE", scope_ref=w, workflow_key="writing-failed-create",
            assignment_refs=[assignment], default_flow=["WRITING_CHAPTER_AUTHOR"])
        draft = service.chapter(writing_company, w, b, c)["draft"]
    original = CanonicalChildWorkRuntime.create_cycle_work
    def fail_after_create(self, **kwargs):
        original(self, **kwargs)
        raise ValueError("synthetic failure after canonical creation")
    monkeypatch.setattr(CanonicalChildWorkRuntime, "create_cycle_work", fail_after_create)
    with TestClient(app) as client:
        response = client.post(f"/api/workspace/runtime/foundation/team-operating/assignments/{assignment}/work",
            headers={"X-Tenant-Id": "selfuse", "X-Ceo-Id": writing_ceo}, json={"request_id": "rollback-work",
            "problem": "明确交办", "expected_result": "章节候选", "model_key": "model.writing-entry",
            "source": {"kind": "writing", "book_ref": b, "chapter_ref": c, "expected_draft_ref": draft["ref"], "selection": binding["selection"]}})
        assert response.status_code == 422, response.text
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type in ('WORK','CYCLE')").fetchone()[0] == 0
    assert calls == []
