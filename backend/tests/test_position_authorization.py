"""岗位级能力授权（Phase-10）回归测试。

验证：
- 内置 et_* 官方模板迁移回填全开（兼容基线）：绑定不被拒。
- 未声明授权的新岗位（deny-by-default）：绑定能力被拒（422）。
- 员工实例级覆盖（引导生成收敛授权）：绑定 exec 能力被拒、只读放行。
- 员工无岗位模板 → 放行。
- resolver 授权过滤：收敛岗位员工解析越权能力 → 无可用；无员工 → 正常。
"""

from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app

ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-authz", "X-Ceo-Id": "ceo-authz"}
ADMIN = {"Authorization": "Bearer platform-admin-dev"}
DEPT_TEMPLATE_ID = "official.department.software_rnd"
EMP_TEMPLATE_ID = "official.employee.tech_lead"


class PositionAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-authz-")
        self.addCleanup(self.workspace.cleanup)
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        original_env = dict(os.environ)
        os.environ.update({
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev",
                # 不设 CURIS_D1_WORKSPACE_ROOT（坑见 08-04 日志：污染 local_rd_toolset）
                "CURIS_D1_EXECUTE_ENABLED": "false",
                "CURIS_D1_FROZEN": "true",
                "CURIS_RD_SANDBOX": "off",
        })
        def restore_environment():
            # Restore values without clearing unchanged native temp-path settings.
            for key in set(os.environ) - original_env.keys():
                del os.environ[key]
            for key, value in original_env.items():
                if os.environ.get(key) != value:
                    os.environ[key] = value
        self.addCleanup(restore_environment)
        root_override = patch("app.local_rd_toolset._WORKSPACE_ROOT_OVERRIDE", None)
        root_override.start()
        self.addCleanup(root_override.stop)

    def _client(self) -> TestClient:
        client = TestClient(create_app(self.db_path))
        self.addCleanup(client.close)
        return client

    def _seed_employee(
        self, client: TestClient, *, template_id: str = EMP_TEMPLATE_ID
    ) -> str:
        company = client.get("/api/workspace/companies", headers=HEADERS).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=HEADERS,
            json={"company_id": company["company_id"], "template_id": DEPT_TEMPLATE_ID, "name": "研发部"},
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=HEADERS,
            json={
                "department_id": department["id"],
                "template_id": template_id,
                "name": "岗位员工",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        return employee["id"]

    def _set_instance_authorization(self, employee_id: str, allowed: list[str]) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "update employee_instances set allowed_effect_classes_json = ? where id = ?",
                (json.dumps(allowed), employee_id),
            )

    def _set_template_authorization(self, allowed: list[str]) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "update employee_templates set allowed_effect_classes_json = ? where id = ?",
                (json.dumps(allowed), EMP_TEMPLATE_ID),
            )

    def _register_agent_capability(self, client: TestClient) -> str:
        key = "ext.exec_agent"
        response = client.post(
            "/api/platform/capabilities",
            headers=ADMIN,
            json={"capability_key": key, "type": "agent", "display_name": "Exec Agent", "gateway_ref": "newapi"},
        )
        self.assertEqual(response.status_code, 201, response.text)
        return key

    def _register_private_agent(self, client: TestClient) -> str:
        response = client.post(
            "/api/workspace/capabilities/private",
            headers=HEADERS,
            json={
                "capability_type": "agent",
                "capability_id": "my-exec-agent",
                "display_name": "My Exec Agent",
                "metadata": {
                    "kind": "openai-compatible",
                    "endpoint": "https://private.example.com",
                    "credential_ref": "env:TEST_AUTHZ_AGENT_KEY",
                },
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return "my-exec-agent"

    # ── 内置 et_* 全开（兼容基线）──
    def test_official_template_backfilled_all_open(self):
        self._client()
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "select allowed_effect_classes_json from employee_templates where id = ?",
                (EMP_TEMPLATE_ID,),
            ).fetchone()
        self.assertIn("exec", json.loads(row[0]))

    # ── 绑定校验 ──────────────────────────────────────────────────
    def test_bind_authorized_capability_ok(self):
        client = self._client()
        employee_id = self._seed_employee(client)
        response = client.put(
            f"/api/workspace/employees/{employee_id}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [
                    {
                        "capability_source": "official",
                        "capability_type": "model",
                        "capability_id": "official.newapi.default",
                    }
                ]
            },
        )
        self.assertEqual(response.status_code, 200, response.text)

    def test_bind_unauthorized_capability_rejected_422(self):
        client = self._client()
        employee_id = self._seed_employee(client)
        self._register_private_agent(client)
        self._set_instance_authorization(employee_id, ["read", "retrieve"])
        response = client.put(
            f"/api/workspace/employees/{employee_id}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "agent",
                        "capability_id": "my-exec-agent",
                    }
                ]
            },
        )
        self.assertEqual(response.status_code, 422, response.text)
        self.assertIn("not authorized", response.json()["detail"])

    def test_bind_deny_by_default_position_rejected(self):
        client = self._client()
        employee_id = self._seed_employee(client)
        self._set_template_authorization([])
        response = client.put(
            f"/api/workspace/employees/{employee_id}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [
                    {
                        "capability_source": "official",
                        "capability_type": "model",
                        "capability_id": "official.newapi.default",
                    }
                ]
            },
        )
        self.assertEqual(response.status_code, 422, response.text)

    # ── resolver 授权过滤 ─────────────────────────────────────────
    def test_resolver_filters_unauthorized_capability(self):
        from app.capability_authorizer import CapabilityAuthorizer
        from app.capability_catalog import CapabilityCatalog
        from app.capability_resolver import CapabilityExhausted, CapabilityRequirement, CapabilityResolver
        from app.database import Database
        from app.evolution_event_log import EvolutionEventLog
        from app.tenant_context import TenantContext

        client = self._client()
        employee_id = self._seed_employee(client)
        self._set_instance_authorization(employee_id, ["read"])
        self._register_agent_capability(client)

        database = Database(self.db_path)
        catalog = CapabilityCatalog(database, EvolutionEventLog(database))
        with TenantContext.scope("tenant-authz"):
            authorizer = CapabilityAuthorizer(database)
            resolver = CapabilityResolver(catalog=catalog, database=database)
            # 无员工 → 候选存在，可解析（授权不拦截）
            handle = resolver.resolve(CapabilityRequirement(cap_type="agent"))
            self.assertEqual(handle.key, "ext.exec_agent")
            # 员工授权 read → agent(exec) 被过滤 → 无可用
            with self.assertRaises(CapabilityExhausted):
                resolver.resolve(
                    CapabilityRequirement(cap_type="agent"),
                    employee_id=employee_id,
                )

    # ── 实例级授权列写入（引导落地路径）──────────────────────────
    def test_instance_authorization_column_write(self):
        client = self._client()
        employee_id = self._seed_employee(client)
        self._set_instance_authorization(employee_id, ["read", "retrieve"])
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "select allowed_effect_classes_json from employee_instances where id = ?",
                (employee_id,),
            ).fetchone()
        self.assertEqual(json.loads(row[0]), ["read", "retrieve"])


if __name__ == "__main__":
    unittest.main()

# Source10: real canonical package/team mechanics in isolated, self-made databases.
import ast
from types import SimpleNamespace
import pytest
from app.employee_templates import EmployeeTemplateContract
from app.tenant_context import TenantContext
from test_writing_entry_readiness import company_only
from test_writing_chapter_vertical import scope, COMPANY, CEO

AGENT = {"capability_source": "tenant_private", "capability_type": "agent",
         "capability_id": "agent.position-fixture", "priority": 80, "enabled": True}


def canonical_employee(tmp_path, folder="music"):
    db, runtime = company_only(tmp_path)
    with scope():
        runtime.install(Path(__file__).resolve().parents[1] / "app/bundled_workspace_packages" / folder,
            COMPANY, department_id="writing-test-department", business_id="position-business", business_name="授权测试")
        with db.connect() as con:
            employee = con.execute("select id from employee_instances where company_id=?", (COMPANY,)).fetchone()[0]
        db.save_tenant_private_capability(tenant_id="selfuse", capability_type="agent",
            capability_id=AGENT["capability_id"], display_name="Synthetic Agent", metadata={"kind": "codex-cli"})
    return db, EmployeeTemplateContract(db), employee


def permission_request(profile, enabled=True):
    return {"company_id": COMPANY, "expected_revision": profile["execution_permission"]["revision"], "enabled": enabled}


@pytest.mark.parametrize("folder", ["writing_authoring", "content_growth_v02", "music"])
def test_canonical_three_explicit_permission_existing_empty_and_cold_revoke(tmp_path, folder):
    db, service, employee = canonical_employee(tmp_path, folder)
    with scope():
        before = service.list_employee_capability_bindings(employee)
        assert before["bindings"] == [] and before["execution_permission"]["manageable"]
        assert before["execution_permission"]["effective_classes"] == []
        with pytest.raises(ValueError, match="执行许可"):
            service.require_agent_execution_permission(employee, COMPANY)
        granted = service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        assert granted["execution_permission"]["effective_classes"] == ["exec"]
        assert len(granted["bindings"]) == 1
        service.require_agent_execution_permission(employee, COMPANY)
        cold = EmployeeTemplateContract(db)
        assert cold.list_employee_capability_bindings(employee) == granted
        revoked = cold.set_employee_capability_bindings(employee, granted["bindings"],
            execution_permission=permission_request(granted, False))
        assert revoked["execution_permission"]["effective_classes"] == [] and revoked["bindings"] == []
        with pytest.raises(ValueError, match="执行许可"):
            service.require_agent_execution_permission(employee, COMPANY)
        with db.connect() as con:
            assert con.execute("select t.allowed_effect_classes_json from employee_templates t "
                "join employee_instances e on t.id=e.template_id where e.id=?", (employee,)).fetchone()[0] == "[]"


@pytest.mark.parametrize("identity", [{"tenant_id": "foreign"}, {"company_id": "foreign"},
                                      {"ceo_id": "foreign"}, {"role": "employee"}])
def test_explicit_permission_rejects_foreign_actor_without_partial_write(tmp_path, identity):
    _, service, employee = canonical_employee(tmp_path)
    with scope():
        before = service.list_employee_capability_bindings(employee)
    with scope(**identity), pytest.raises(ValueError):
        service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
    with scope():
        assert service.list_employee_capability_bindings(employee) == before


def test_permission_and_binding_rollback_stale_company_and_invalid_capability(tmp_path, monkeypatch):
    _, service, employee = canonical_employee(tmp_path)
    with scope():
        before = service.list_employee_capability_bindings(employee)
        for request, bindings in [
            ({**permission_request(before), "company_id": "foreign"}, [AGENT]),
            ({**permission_request(before), "expected_revision": "0" * 64}, [AGENT]),
            (permission_request(before), [{**AGENT, "capability_id": "not-registered"}]),
            (permission_request(before), [AGENT, AGENT]),
        ]:
            with pytest.raises(ValueError):
                service.set_employee_capability_bindings(employee, bindings, execution_permission=request)
            assert service.list_employee_capability_bindings(employee) == before
        original = service._write_capability_bindings
        def fail_after_write(*args):
            original(*args)
            raise ValueError("synthetic transaction failure")
        with monkeypatch.context() as patcher:
            patcher.setattr(service, "_write_capability_bindings", fail_after_write)
            with pytest.raises(ValueError, match="synthetic"):
                service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        assert service.list_employee_capability_bindings(employee) == before
        granted = service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        with pytest.raises(ValueError, match="资料已变化"):
            service.set_employee_capability_bindings(employee, [], execution_permission=permission_request(before, False))
        assert service.list_employee_capability_bindings(employee) == granted


def test_exec_never_adds_read_and_preserves_existing_disabled_model_identity(tmp_path):
    db, service, employee = canonical_employee(tmp_path)
    with scope():
        with db.connect() as con:
            con.execute("update employee_instances set allowed_effect_classes_json=? where id=?",
                        (json.dumps(["read"]), employee))
        model = {"capability_source": "official", "capability_type": "model",
                 "capability_id": "official.newapi.default", "priority": 17, "enabled": False}
        baseline = service.set_employee_capability_bindings(employee, [model])
        granted = service.set_employee_capability_bindings(employee, [*baseline["bindings"], AGENT],
            execution_permission=permission_request(baseline))
        assert granted["execution_permission"]["effective_classes"] == ["exec", "read"]
        assert granted["bindings"][0] == baseline["bindings"][0]
        again = service.set_employee_capability_bindings(employee, granted["bindings"],
            execution_permission=permission_request(granted))
        assert again["bindings"] == granted["bindings"]
        revoked = service.set_employee_capability_bindings(employee, again["bindings"],
            execution_permission=permission_request(again, False))
        assert revoked["bindings"] == baseline["bindings"]
        assert revoked["execution_permission"]["effective_classes"] == ["read"]


def test_template_exec_cannot_be_falsely_revoked_by_empty_inheritance(tmp_path):
    db, service, employee = canonical_employee(tmp_path)
    with scope():
        with db.connect() as con:
            con.execute("update employee_templates set allowed_effect_classes_json=? where id="
                        "(select template_id from employee_instances where id=?)", ('["exec"]', employee))
        before = service.list_employee_capability_bindings(employee)
        assert before["execution_permission"]["enabled"] and not before["execution_permission"]["can_revoke"]
        with pytest.raises(ValueError, match="岗位模板"):
            service.set_employee_capability_bindings(employee, [], execution_permission=permission_request(before, False))
        assert service.list_employee_capability_bindings(employee) == before


@pytest.mark.parametrize("tamper", ["package", "definition", "assignment"])
def test_same_role_label_or_id_does_not_replace_canonical_package_contract(tmp_path, tamper):
    db, service, employee = canonical_employee(tmp_path)
    with scope():
        before = service.list_employee_capability_bindings(employee)
        with db.connect() as con:
            if tamper == "package":
                con.execute("update workspace_package_instances set package_digest=?", ("0" * 64,))
            elif tamper == "definition":
                con.execute("update employee_templates set responsibility='unapproved' where id="
                            "(select template_id from employee_instances where id=?)", (employee,))
            else:
                con.execute("update runtime_entities set lifecycle_status='REVOKED' where entity_type='RESPONSIBILITY_ASSIGNMENT'")
        current = service.list_employee_capability_bindings(employee)
        assert not current["execution_permission"]["manageable"]
        with pytest.raises(ValueError):
            service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        assert not service.list_employee_capability_bindings(employee)["execution_permission"]["enabled"]


def test_permission_request_is_strict_and_cannot_smuggle_effect_classes():
    from app.main import EmployeeExecutionPermissionIn
    from pydantic import ValidationError
    values = {"company_id": COMPANY, "expected_revision": "a" * 64, "enabled": True}
    assert EmployeeExecutionPermissionIn(**values).enabled is True
    for bad in ({"enabled": "true"}, {"enabled": 1}, {"enabled": None}, {"allowed_effect_classes": ["read"]}):
        with pytest.raises(ValidationError):
            EmployeeExecutionPermissionIn(**(values | bad))


def production_gateway_functions(db, service):
    # Compile unchanged production function bodies, with only external dependencies replaced.
    # This exercises actual gate/callback logic, not a duplicate test implementation.
    import app.main as main
    tree = ast.parse(Path(main.__file__).read_text())
    names = {"require_agent_position", "execute_model_gateway", "agent_stopped",
             "reserve_original_agent_call", "run_scoped_agent"}
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name in names]
    assert len(functions) == len(names)
    env = dict(vars(main))
    env.update(database=db, employee_template_contract=service, default_executor=object(),
               uuid=__import__("uuid"))
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(main.__file__), "exec"), env)
    return env


def test_real_gateway_checks_before_credentials_and_running_continue_stop_on_revoke(tmp_path, monkeypatch):
    from app.runtime_capability_context import RuntimeCapabilityContext
    from app.model_gateway import ModelGatewayExecutionError
    from app.company_execution_policy import CompanyExecutionPolicy
    db, service, employee = canonical_employee(tmp_path)
    env = production_gateway_functions(db, service)
    calls = []
    class AllowanceReached(RuntimeError):
        pass
    def allowance(*args, **kwargs):
        calls.append("allowance")
        raise AllowanceReached()
    monkeypatch.setattr(CompanyExecutionPolicy, "require_agent_execution", allowance)
    context = {"source": "tenant_private", "type": "agent", "id": AGENT["capability_id"],
               "employee_id": employee, "company_id": COMPANY, "task_id": "synthetic-task"}
    env["credential_vault"] = SimpleNamespace(resolve=lambda *args: pytest.fail("credential read"))
    with scope(), RuntimeCapabilityContext.scope(context):
        with pytest.raises(ModelGatewayExecutionError, match="执行许可"):
            env["execute_model_gateway"]("self-made prompt")
        assert calls == []
        before = service.list_employee_capability_bindings(employee)
        granted = service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        with pytest.raises(AllowanceReached):
            env["execute_model_gateway"]("self-made prompt")
        assert calls == ["allowance"]
        env.update(runtime_capability=context, agent_employee=employee, agent_task="synthetic-task",
            agent_binding=granted["bindings"][0]["id"], metadata={"kind": "codex-cli"},
            allowance={"revision": "allow"}, event_log=None,
            agent_policy=SimpleNamespace(agent_rows=lambda *args: [{"enabled": True, "revision": "allow"}]),
            TaskExecutionControlService=lambda *args: SimpleNamespace(get_state=lambda _: {"task_status": "RUNNING"}))
        assert env["agent_stopped"]() is False
        revoked = service.set_employee_capability_bindings(employee, granted["bindings"],
            execution_permission=permission_request(granted, False))
        assert revoked["bindings"] == []
        assert env["agent_stopped"]() is True
        # A previously queued/continuing task and the final launch hook both re-read permission.
        for invoke in (lambda: env["execute_model_gateway"]("continue"),
                       lambda: env["run_scoped_agent"]("continue"),
                       env["reserve_original_agent_call"]):
            with pytest.raises(ModelGatewayExecutionError, match="执行许可"):
                invoke()
        assert calls == ["allowance"]  # No credential, reservation, resources or Provider execution.

def test_actual_capabilities_route_never_infers_permission_from_registered_agent(tmp_path):
    import app.main as main
    from app.capability_authorizer import CapabilityAuthorizer
    from fastapi import HTTPException
    db, service, employee = canonical_employee(tmp_path)
    tree = ast.parse(Path(main.__file__).read_text())
    route = next(node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef) and node.name == "set_workspace_employee_capabilities")
    route.decorator_list = []  # Execute the real endpoint body with an isolated service/identity.
    env = dict(vars(main), employee_template_contract=service, capability_authorizer=CapabilityAuthorizer(db))
    exec(compile(ast.Module(body=[route], type_ignores=[]), str(main.__file__), "exec"), env)
    put = env["set_workspace_employee_capabilities"]
    with scope():
        before = service.list_employee_capability_bindings(employee)
        with pytest.raises(HTTPException) as rejected:
            put(employee, main.EmployeeCapabilityBindingsIn(bindings=[AGENT]))
        assert rejected.value.status_code == 422
        assert service.list_employee_capability_bindings(employee) == before
        granted = put(employee, main.EmployeeCapabilityBindingsIn(
            bindings=[AGENT], execution_permission=permission_request(before)))
        assert granted["execution_permission"]["enabled"] is True
        revoked = put(employee, main.EmployeeCapabilityBindingsIn(
            bindings=granted["bindings"], execution_permission=permission_request(granted, False)))
        assert not revoked["execution_permission"]["enabled"] and revoked["bindings"] == []

def test_legacy_binding_writer_rechecks_permission_after_a_concurrent_revoke(tmp_path):
    from app.capability_authorizer import CapabilityAuthorizer
    db, service, employee = canonical_employee(tmp_path)
    with scope():
        before = service.list_employee_capability_bindings(employee)
        granted = service.set_employee_capability_bindings(employee, [AGENT], execution_permission=permission_request(before))
        assert CapabilityAuthorizer(db).authorize(employee, "agent")[0]  # An earlier API check passed.
        revoked = service.set_employee_capability_bindings(employee, granted["bindings"],
            execution_permission=permission_request(granted, False))
        with pytest.raises(ValueError, match="not authorized"):
            service.set_employee_capability_bindings(employee, [AGENT])  # Legacy/no-consent write arrives later.
        assert service.list_employee_capability_bindings(employee) == revoked



def test_codex_hold_never_falls_back_to_another_executor(monkeypatch):
    import asyncio
    from app.agent_adapter import CodexExecutionHeld
    from app.tool_executor import ToolExecutor, ToolExecutionError

    calls = []
    executor = ToolExecutor(None, {})
    async def execute(name, prompt):
        calls.append(name)
        if name == "first":
            raise CodexExecutionHeld()
        return {"output": "unexpected"}
    monkeypatch.setattr(executor, "execute", execute)
    with pytest.raises(ToolExecutionError) as caught:
        asyncio.run(executor.execute_chain(["first"], "fixture", fallback_planner=lambda _: ["first", "second"]))
    assert calls == ["first"]
    assert type(caught.value.cause) is CodexExecutionHeld


def test_same_text_or_status_does_not_spoof_codex_hold(monkeypatch):
    import asyncio
    from app.tool_executor import ToolExecutor

    calls = []
    executor = ToolExecutor(None, {})
    async def execute(name, prompt):
        calls.append(name)
        if name == "first":
            error = RuntimeError("codex_execution_held")
            error.status = "codex_execution_held"
            raise error
        return {"output": "fallback", "cost": 0}
    monkeypatch.setattr(executor, "execute", execute)
    result = asyncio.run(executor.execute_chain(["first"], "fixture", fallback_planner=lambda _: ["first", "second"]))
    assert calls == ["first", "second"]
    assert result["output"] == "fallback"


def writing_model_position(tmp_path, package="writing_authoring"):
    """An already materialized default-deny author, with metadata-only model consent."""
    import hashlib
    from app.company_execution_policy import CompanyExecutionPolicy
    db, service, employee = canonical_employee(tmp_path, package)
    model = "deepseek-flash"
    key = "user.deepseek." + hashlib.sha256(model.encode()).hexdigest()[:16]
    with scope():
        ref = "local-dev://tenant/selfuse/credential/cred-position-fixture"
        db.save_credential_metadata(credential_id="cred-position-fixture", tenant_id="selfuse",
            name="Synthetic metadata only", provider="deepseek", credential_type="api_key", credential_ref=ref)
        db.save_tenant_private_capability(tenant_id="selfuse", capability_type="model", capability_id=key,
            display_name="Synthetic Flash", metadata={"provider_type": "deepseek", "model_name": model,
                "base_url": "https://api.deepseek.com", "provider_protocol": "openai_chat",
                "chat_path": "/v1/chat/completions", "credential_ref": ref,
                "discovery_verification": {"status": "verified", "provider_id": "deepseek",
                    "model_id": model, "requires_credential": True}})
        with db.connect() as con:
            workspace = con.execute("select workspace_id from workspace_package_instances where company_id=?",
                                    (COMPANY,)).fetchone()[0]
        policy = CompanyExecutionPolicy(db)
        preview = policy.read(COMPANY)
        policy.save(COMPANY, request_id="position-model-consent", expected_revision="", enabled=True,
            consent=True, workspace_ids=[workspace], model_keys=[key], budget_cny="0.1", valid_hours=1,
            preview_token=preview["preview_token"], trial_authorization_ref="ceo-deepseek-synthetic-20261105-two-calls-cny-0.10")
    return db, service, employee, key, workspace


def test_writing_model_consent_never_grants_read_or_exec(tmp_path):
    from app.capability_authorizer import CapabilityAuthorizer
    db, service, employee, key, _ = writing_model_position(tmp_path)
    with scope():
        authorizer = CapabilityAuthorizer(db)
        assert authorizer.authorize(employee, "model", key)[0]
        assert not authorizer.authorize(employee, "model", "unapproved-model")[0]
        for kind in ["tool", "skill", "connector", "agent"]:
            assert not authorizer.authorize(employee, kind, "synthetic-read-tool")[0]
        assert authorizer.allowed_classes_for_employee(employee) == set()
        assert service.list_employee_capability_bindings(employee)["bindings"] == []
        with db.connect() as con:
            assert con.execute("select allowed_effect_classes_json from employee_instances where id=?", (employee,)).fetchone()[0] == "[]"
            assert con.execute("select allowed_effect_classes_json from employee_templates where id='official.employee.writing.author'").fetchone()[0] == "[]"
            assert con.execute("select count(*) from tasks").fetchone()[0] == 0
            assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0


@pytest.mark.parametrize("identity", [{"tenant_id": "foreign"}, {"company_id": "foreign"},
                                      {"ceo_id": "foreign"}, {"role": "employee"}])
def test_writing_model_consent_rejects_foreign_identity(tmp_path, identity):
    from app.capability_authorizer import CapabilityAuthorizer
    db, _, employee, key, _ = writing_model_position(tmp_path)
    with scope(**identity):
        # Existing no-employee legacy behavior is separate; no foreign binding may be written.
        if identity.get("tenant_id") == "foreign":
            with pytest.raises(ValueError): EmployeeTemplateContract(db).set_employee_capability_bindings(employee, [])
        else:
            assert not CapabilityAuthorizer(db).authorize(employee, "model", key)[0]


@pytest.mark.parametrize("invalid", ["revoked", "expired", "model-disabled", "destination", "credential-disabled",
                                     "team-tampered", "explicit-deny", "malformed", "trial-unknown"])
def test_writing_model_consent_rechecks_current_gate(tmp_path, invalid):
    from app.capability_authorizer import CapabilityAuthorizer
    db, service, employee, key, workspace = writing_model_position(tmp_path)
    with scope():
        with db.connect() as con:
            if invalid in {"revoked", "expired"}:
                row = con.execute("select event_id,payload from evolution_events where event_type='company.text_policy.changed'").fetchone()
                value = json.loads(row["payload"])
                if invalid == "revoked": value["enabled"] = False
                else: value["expires_at"] = "2000-01-01T00:00:00+00:00"
                con.execute("update evolution_events set payload=? where event_id=?", (json.dumps(value), row["event_id"]))
            elif invalid == "model-disabled":
                con.execute("update tenant_private_capabilities set status='disabled' where capability_id=?", (key,))
            elif invalid == "destination":
                con.execute("update tenant_private_capabilities set metadata_json=json_set(metadata_json,'$.base_url','https://foreign.invalid') where capability_id=?", (key,))
            elif invalid == "credential-disabled":
                con.execute("update credential_metadata set status='disabled'")
            elif invalid == "team-tampered":
                con.execute("update employee_instances set created_from_template_id='foreign' where id=?", (employee,))
            elif invalid in {"explicit-deny", "malformed"}:
                con.execute("update employee_instances set allowed_effect_classes_json=? where id=?",
                            ('["retrieve"]' if invalid == "explicit-deny" else 'invalid', employee))
        if invalid == "trial-unknown":
            from app.company_execution_policy import CompanyExecutionPolicy
            policy = CompanyExecutionPolicy(db)
            grant = policy.current_grant(COMPANY, workspace, key)
            with db.connect() as con:
                con.execute('begin immediate')
                policy.reserve(con, {"company_id": COMPANY, "attempt_id": "unknown-original", "message_id": "synthetic",
                    "context": {"workspace_id": workspace}}, {"grant": grant, "model": {"model_key": key}})
        assert not CapabilityAuthorizer(db).authorize(employee, "model", key)[0]
        with pytest.raises(ValueError):
            service.set_employee_capability_bindings(employee, [{"capability_source": "tenant_private",
                "capability_type": "model", "capability_id": key}])


@pytest.mark.parametrize("package", ["content_growth_v02", "music"])
def test_other_official_author_model_binding_preserves_default_deny(tmp_path, package):
    from app.capability_authorizer import CapabilityAuthorizer
    db, service, employee, key, _ = writing_model_position(tmp_path, package)
    with scope():
        authorizer = CapabilityAuthorizer(db)
        assert authorizer.authorize(employee, "model", key)[0]
        service.set_employee_capability_bindings(employee, [{"capability_source": "tenant_private", "capability_type": "model", "capability_id": key, "enabled": True}])
        assert service.list_employee_capability_bindings(employee)["bindings"][0]["enabled"]
        for kind in ("tool", "skill", "connector", "agent"):
            assert not authorizer.authorize(employee, kind, "synthetic-read-tool")[0]
        assert authorizer.allowed_classes_for_employee(employee) == set()
