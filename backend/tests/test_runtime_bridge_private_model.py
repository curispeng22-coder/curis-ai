"""Runtime bridge: tenant_private 模型（env:VAR 密钥）端到端调用回归测试。

验证 main.py 的 execute_model_gateway 在 runtime_capability.source == "tenant_private"
且 type == "model" 时，会按私有能力元数据里的 base_url / api_key / model_name 构造
ModelGatewayAdapter 并真正打到用户自定义端点，而不是回落到 default_executor。

密钥以 env:VAR 形式引用（Step 5 兼容），绝不落库；缺失 env 变量时 fail-closed，
不得误打到私有端点。
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter

ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-bridge", "X-Ceo-Id": "ceo-bridge"}

PRIVATE_BASE_URL = "https://private-gateway.example.com"
PRIVATE_MODEL_NAME = "private-model-a"
PRIVATE_CREDENTIAL_REF = "env:TEST_PRIVATE_MODEL_KEY"
PRIVATE_SECRET = "private-secret-xyz"


class RecordingHttpPost:
    """记录所有出站 HTTP 调用，并返回 OpenAI 兼容响应。"""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def __call__(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        self.calls.append(
            {
                "url": url,
                "payload": payload,
                "headers": headers,
                "timeout": timeout,
            }
        )
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            "--- a/backend/app/sample.py\n"
                            "+++ b/backend/app/sample.py\n"
                            "@@ -1 +1 @@\n"
                            "-VALUE = 1\n"
                            "+VALUE = 2\n"
                        )
                    }
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }


class RuntimeBridgePrivateModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-bridge-")
        self.addCleanup(self.workspace.cleanup)
        self.workspace_path = Path(self.workspace.name)
        target = self.workspace_path / "backend/app/sample.py"
        test_file = self.workspace_path / "backend/tests/test_sample.py"
        python_bin = self.workspace_path / "backend/.venv/bin/python"
        target.parent.mkdir(parents=True)
        test_file.parent.mkdir(parents=True)
        python_bin.parent.mkdir(parents=True)
        target.write_text("VALUE = 1\n", encoding="utf-8")
        test_file.write_text(
            "from pathlib import Path\n\n"
            "def test_value():\n"
            "    assert 'VALUE = 2' in Path('backend/app/sample.py').read_text()\n",
            encoding="utf-8",
        )
        python_bin.write_text(
            f"#!/bin/sh\nexec '{ROOT / 'backend/.venv/bin/python'}' \"$@\"\n",
            encoding="utf-8",
        )
        python_bin.chmod(0o755)
        subprocess.run(["git", "init", "-q"], cwd=self.workspace_path, check=True)
        subprocess.run(
            ["git", "config", "user.email", "bridge@example.invalid"],
            cwd=self.workspace_path,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Bridge Test"],
            cwd=self.workspace_path,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=self.workspace_path, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.workspace_path, check=True)

        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))

        # 默认不注入 TEST_PRIVATE_MODEL_KEY；有需要的测试自行设置，保证 fail-closed 用例独立。
        self.http_post = RecordingHttpPost()
        self.env = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_D1_EXECUTE_ENABLED": "true",
                "CURIS_D1_FROZEN": "false",
                "CURIS_D1_WORKSPACE_ROOT": str(self.workspace_path),
                "CURIS_RD_SANDBOX": "off",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        root_override = patch("app.local_rd_toolset._WORKSPACE_ROOT_OVERRIDE", None)
        root_override.start()
        self.addCleanup(root_override.stop)

    def _client(self) -> TestClient:
        client = TestClient(
            create_app(
                self.db_path,
                model_gateway_adapter=ModelGatewayAdapter(http_post=self.http_post),
            )
        )
        self.addCleanup(client.close)
        return client

    def _register_private_model(self, client: TestClient) -> None:
        model = client.post(
            "/api/workspace/private-models",
            headers=HEADERS,
            json={
                "name": "my-private-coder",
                "provider_type": "openai_compatible",
                "base_url": PRIVATE_BASE_URL,
                "model_name": PRIVATE_MODEL_NAME,
                "credential_ref": PRIVATE_CREDENTIAL_REF,
                "enabled": True,
            },
        )
        self.assertEqual(model.status_code, 201, model.text)
        self.assertEqual(model.json()["credential_ref"], PRIVATE_CREDENTIAL_REF)
        self.assertEqual(model.json()["source"], "tenant_private")

    def _fixture(self, client: TestClient, capability_id: str, capability_type: str = "model"):
        company = client.get("/api/workspace/companies", headers=HEADERS).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=HEADERS,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "研发负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        bound = client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": capability_type,
                        "capability_id": capability_id,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(bound.status_code, 200, bound.text)
        project = client.post(
            "/api/workspace/projects",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "name": "Bridge 研发项目",
                "goal": "跑通私有能力调用闭环",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "status": "active",
            },
        ).json()
        created = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=HEADERS,
            json={
                "content": "把 sample.py 的 VALUE 从 1 改为 2",
                "employee_id": employee["id"],
                "capability_source": "tenant_private",
                "capability_type": capability_type,
                "capability_id": capability_id,
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        return project["project_id"], created.json()["task_id"]

    def _run(self, client: TestClient, project_id: str, task_id: str):
        return client.post(
            "/api/workspace/rd-workflow/run",
            headers=HEADERS,
            json={
                "project_id": project_id,
                "task_id": task_id,
                "target_files": ["backend/app/sample.py"],
                "test_file": "backend/tests/test_sample.py",
                "max_rounds": 1,
            },
        )

    def test_tenant_private_model_with_env_credential_routes_to_its_own_endpoint(self):
        os.environ["TEST_PRIVATE_MODEL_KEY"] = PRIVATE_SECRET
        self.addCleanup(lambda: os.environ.pop("TEST_PRIVATE_MODEL_KEY", None))

        client = self._client()
        self._register_private_model(client)
        project_id, task_id = self._fixture(client, "my-private-coder")
        self._run(client, project_id, task_id)

        # 运行时桥必须真正把调用打到私有端点（而非 default_executor）。
        self.assertGreaterEqual(len(self.http_post.calls), 1)
        private_calls = [
            c for c in self.http_post.calls
            if c["url"] == f"{PRIVATE_BASE_URL}/v1/chat/completions"
        ]
        self.assertEqual(
            len(private_calls),
            len(self.http_post.calls),
            "tenant_private 模型的所有调用都应路由到私有端点",
        )
        call = private_calls[0]
        self.assertEqual(call["headers"]["Authorization"], f"Bearer {PRIVATE_SECRET}")
        self.assertEqual(call["payload"]["model"], PRIVATE_MODEL_NAME)

    def test_model_call_emits_runtime_trace_event(self):
        """执行模型调用后，runtime_trace 必须落一条 model_call 事件（EvoFlow A2 闭环）。"""
        os.environ["TEST_PRIVATE_MODEL_KEY"] = PRIVATE_SECRET
        self.addCleanup(lambda: os.environ.pop("TEST_PRIVATE_MODEL_KEY", None))

        client = self._client()
        self._register_private_model(client)
        project_id, task_id = self._fixture(client, "my-private-coder")
        self._run(client, project_id, task_id)

        trace = client.get("/api/workspace/runtime-trace", headers=HEADERS).json()["events"]
        self.assertGreaterEqual(len(trace), 1, "执行后必须产生运行时 trace 事件")
        model_events = [e for e in trace if e["event_type"] == "model_call"]
        self.assertGreaterEqual(len(model_events), 1, "必须包含至少一条 model_call trace")
        self.assertTrue(
            any(e.get("task_ref") == task_id for e in model_events),
            "trace 事件必须关联到本次执行任务",
        )
        self.assertTrue(
            all(e.get("capability") for e in model_events),
            "trace 事件必须携带能力标识",
        )
        self.assertIn("usage_record_id", model_events[0]["payload"])

    def test_tenant_private_model_missing_env_credential_rejects_all_outbound(self):
        # Missing selected credentials must reject both private and default routes.
        self.assertNotIn("TEST_PRIVATE_MODEL_KEY", os.environ)

        client = self._client()
        self._register_private_model(client)
        project_id, task_id = self._fixture(client, "my-private-coder")
        self._run(client, project_id, task_id)
        self.assertEqual(self.http_post.calls, [], "Missing selected credentials must not call the default gateway")

        private_calls = [
            c for c in self.http_post.calls
            if c["url"] == f"{PRIVATE_BASE_URL}/v1/chat/completions"
        ]
        self.assertEqual(
            private_calls,
            [],
            "缺失 env 密钥时不得路由到私有端点（回落/失败都必须 fail-closed）",
        )


class RuntimeBridgePrivateAgentTests(RuntimeBridgePrivateModelTests):
    """租户私有 Agent（env:VAR 密钥）运行时桥接回归。

    Agent 与 Model 走同一 execute_model_gateway 接收槽：openai-compatible 类型的
    私有 agent 按其 endpoint + 密钥构造 ModelGatewayAdapter 真实打到自定义端点；
    mcp / http 等非 openai-compatible 类型暂无专用运行时适配器，必须 fail-closed。
    """

    AGENT_BASE_URL = "https://private-agent.example.com"
    AGENT_CREDENTIAL_REF = "env:TEST_PRIVATE_AGENT_KEY"
    AGENT_SECRET = "private-agent-secret-xyz"

    def _register_private_agent(self, client: TestClient, capability_id: str, kind: str):
        agent = client.post(
            "/api/workspace/capabilities/private",
            headers=HEADERS,
            json={
                "capability_type": "agent",
                "capability_id": capability_id,
                "display_name": f"My {kind} Agent",
                "metadata": {
                    "kind": kind,
                    "endpoint": self.AGENT_BASE_URL,
                    "credential_ref": self.AGENT_CREDENTIAL_REF,
                },
            },
        )
        self.assertEqual(agent.status_code, 201, agent.text)
        self.assertEqual(agent.json()["source"], "tenant_private")
        self.assertEqual(agent.json()["capability_type"], "agent")

    def test_tenant_private_agent_openai_compatible_routes_to_its_own_endpoint(self):
        os.environ["TEST_PRIVATE_AGENT_KEY"] = self.AGENT_SECRET
        self.addCleanup(lambda: os.environ.pop("TEST_PRIVATE_AGENT_KEY", None))

        client = self._client()
        self._register_private_agent(client, "my-private-agent", "openai-compatible")
        project_id, task_id = self._fixture(
            client, "my-private-agent", capability_type="agent"
        )
        self._run(client, project_id, task_id)

        self.assertGreaterEqual(len(self.http_post.calls), 1)
        agent_calls = [
            c for c in self.http_post.calls
            if c["url"] == f"{self.AGENT_BASE_URL}/v1/chat/completions"
        ]
        self.assertEqual(
            len(agent_calls),
            len(self.http_post.calls),
            "tenant_private agent 的所有调用都应路由到私有端点",
        )
        call = agent_calls[0]
        self.assertEqual(call["headers"]["Authorization"], f"Bearer {self.AGENT_SECRET}")
        self.assertEqual(call["payload"]["model"], "my-private-agent")

    def test_tenant_private_agent_unsupported_kind_fails_closed(self):
        # mcp 等非 openai-compatible 类型：必须 fail-closed，绝不误打到私有端点。
        os.environ["TEST_PRIVATE_AGENT_KEY"] = self.AGENT_SECRET
        self.addCleanup(lambda: os.environ.pop("TEST_PRIVATE_AGENT_KEY", None))

        client = self._client()
        self._register_private_agent(client, "my-mcp-agent", "mcp")
        project_id, task_id = self._fixture(
            client, "my-mcp-agent", capability_type="agent"
        )
        self._run(client, project_id, task_id)

        agent_calls = [
            c for c in self.http_post.calls
            if c["url"] == f"{self.AGENT_BASE_URL}/v1/chat/completions"
        ]
        self.assertEqual(
            agent_calls,
            [],
            "mcp 等非 openai-compatible agent 不得打到私有端点（fail-closed）",
        )


if __name__ == "__main__":
    unittest.main()


@pytest.mark.parametrize("missing,reason", [
    ("base_url", "Selected private model route is incomplete"),
    ("provider_type", "Selected private model route is incomplete"),
    ("model_name", "Selected private model route is incomplete"),
    ("credential_ref", "Selected private model credentials are unavailable"),
    ("missing_env", "Selected private model credentials are unavailable"),
])
def test_private_model_formal_caller_rejects_before_any_send(tmp_path, monkeypatch, missing, reason):
    """Actual ASGI tool caller; no legacy Git/RD fixture or subprocess."""
    from app.database import Database
    from app.result_store import ResultStore
    from app.runtime_capability_context import RuntimeCapabilityContext
    from app.tenant_context import TenantContext

    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setenv("CURIS_CREDENTIAL_BACKEND", "local-dev")
    monkeypatch.setenv("CURIS_MODEL_GATEWAY_PROFILE", "")
    monkeypatch.setenv("CURIS_CALLER_FIXTURE_KEY", "synthetic-private-key")
    if missing == "missing_env":
        monkeypatch.delenv("CURIS_CALLER_FIXTURE_KEY")
    path = tmp_path / "private-caller.sqlite"
    post = RecordingHttpPost()
    default = ModelGatewayAdapter(base_url="https://default.invalid", api_key="synthetic-default-key",
                                  gateway_id="default", model_name="default-model", http_post=post)
    app = create_app(str(path), model_gateway_adapter=default)
    db = Database(str(path))
    metadata = {"provider_type": "openai_compatible", "base_url": "https://private.invalid",
                "model_name": "private-fixture", "provider_protocol": "openai_chat",
                "chat_path": "/v1/chat/completions", "credential_ref": "env:CURIS_CALLER_FIXTURE_KEY"}
    metadata.pop(missing, None)
    company = "private-caller-company"
    with TenantContext.scope("tenant-bridge", company_id=company, ceo_id="ceo-bridge", role="ceo"):
        with db.connect() as con:
            con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,?,?,?,'active')",
                        (company, "tenant-bridge", "ceo-bridge", "Synthetic caller company"))
        db.save_tenant_private_capability(tenant_id="tenant-bridge", capability_type="model",
            capability_id="private-caller-model", display_name="Synthetic private model", metadata=metadata)
        task = ResultStore(db).create_task("Reject an incomplete selected route", company_id=company,
            capability_source="tenant_private", capability_type="model", capability_id="private-caller-model")
    context = {"source": "tenant_private", "type": "model", "id": "private-caller-model",
               "task_id": task["task_id"], "company_id": company}
    with TestClient(app) as client, RuntimeCapabilityContext.scope(context):
        response = client.post("/api/tool/execute", headers=HEADERS,
                               json={"tool_name": "model_gateway_tool", "input": "Synthetic rejection only"})
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == reason
    assert post.calls == []  # Neither selected nor default transport may be called.
    with db.connect() as con:
        assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
        assert con.execute("select count(*) from executions where task_id=?", (task["task_id"],)).fetchone()[0] == 0
        assert con.execute("select status from tasks where task_id=?", (task["task_id"],)).fetchone()[0] == "INIT"
