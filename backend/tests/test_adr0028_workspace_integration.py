import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.ceo_context import CeoContext
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app
from app.result_store import ResultStore
from app.tenant_context import TenantContext


class RecordingExecutor:
    def execute(self, prompt: str) -> dict:
        return {
            "output": "Execution result",
            "cost": 0.25,
            "model_gateway_id": "newapi",
            "model_name": "deepseek-v4-flash",
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
            "estimated_cost": 0.25,
            "status": "success",
        }


class ADR0028WorkspaceIntegrationTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def test_workspace_reads_official_department_catalog(self):
        app = create_app(self.db_path)
        client = TestClient(app)

        response = client.get(
            "/api/catalog/department-types",
            headers={"X-Tenant-Id": "tenant-acme"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("department_types", payload)
        self.assertTrue(payload["department_types"])
        self.assertTrue(
            all(item["source"] == "official" for item in payload["department_types"])
        )

    def test_workspace_reads_official_tool_catalog_without_credentials(self):
        app = create_app(self.db_path)
        client = TestClient(app)

        response = client.get(
            "/api/catalog/tools",
            headers={"X-Tenant-Id": "tenant-acme"},
        )

        self.assertEqual(response.status_code, 200)
        tools = response.json()["tools"]
        self.assertTrue(tools)
        self.assertTrue(all(item["source"] == "official" for item in tools))
        self.assertTrue(all(item["status"] == "active" for item in tools))
        self.assertFalse(any("api_key" in item or "secret" in item or "password" in item for item in tools))

    def test_task_execution_emits_tenant_and_ceo_scoped_usage_event(self):
        app = create_app(
            self.db_path,
            tool_functions={"codex_tool": RecordingExecutor().execute},
        )
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-acme", "X-Ceo-Id": "ceo-001"}
        task_id = client.post(
            "/api/task",
            json={"content": "Create code release notes"},
            headers=headers,
        ).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        usage_response = client.get(
            "/api/platform/usage",
            params={"tenant_id": "tenant-acme"},
            headers={"X-Platform-Admin-Token": "platform-admin-dev"},
        )

        self.assertEqual(run_response.status_code, 200)
        self.assertEqual(usage_response.status_code, 200)
        events = usage_response.json()["usage_events"]
        self.assertEqual(
            [event["event_type"] for event in events],
            ["usage.tool_call", "usage.task_execution"],
        )
        for event in events:
            self.assertTrue(event["id"])
            self.assertEqual(event["tenant_id"], "tenant-acme")
            self.assertEqual(event["task_id"], task_id)
            self.assertEqual(event["capability_source"], "official")
            self.assertEqual(event["model_gateway_id"], "")
            self.assertEqual(event["model_name"], "")
            self.assertIsNone(event["prompt_tokens"])
            self.assertIsNone(event["completion_tokens"])
            self.assertIsNone(event["total_tokens"])
            self.assertIsNone(event["estimated_cost"])
            self.assertEqual(event["status"], "success")
            self.assertTrue(event["created_at"])
            self.assertEqual(event["payload"]["ceo_id"], "ceo-001")
            self.assertTrue(event["payload"]["idempotency_key"])
        self.assertEqual(events[0]["capability_type"], "tool")
        self.assertEqual(events[0]["capability_id"], "codex_tool")
        self.assertEqual(events[1]["capability_type"], "task")
        self.assertEqual(events[1]["capability_id"], "task_execution")

    def test_execution_fails_closed_without_ceo_id_when_usage_event_required(self):
        app = create_app(
            self.db_path,
            tool_functions={"codex_tool": RecordingExecutor().execute},
        )
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-acme"}
        task_id = client.post(
            "/api/task",
            json={"content": "Create code release notes"},
            headers=headers,
        ).json()["task_id"]

        response = client.post(f"/api/task/{task_id}/run", headers=headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn("UsageContext", response.json()["detail"])

    def test_usage_events_are_idempotent_for_same_execution(self):
        database = Database(self.db_path)
        database.initialize()
        store = ResultStore(database, EvolutionEventLog(database))
        with TenantContext.scope("tenant-acme", ceo_id="ceo-001"):
            with CeoContext.scope("ceo-001"):
                task = store.create_task("Run once")
                store.save_execution(task["task_id"], "codex_tool", "prompt", "output", 0.5)
                store.save_execution(task["task_id"], "codex_tool", "prompt", "output", 0.5)

        with database.connect() as connection:
            rows = connection.execute(
                "select event_type from evolution_events where event_type in "
                "('usage.tool_call', 'usage.task_execution')"
            ).fetchall()

        self.assertEqual(
            sorted(row["event_type"] for row in rows),
            ["usage.task_execution", "usage.tool_call"],
        )

    def test_workspace_private_capabilities_are_tenant_scoped_and_do_not_pollute_official_catalog(self):
        app = create_app(self.db_path)
        client = TestClient(app)
        tenant_a = {"X-Tenant-Id": "tenant-a"}
        tenant_b = {"X-Tenant-Id": "tenant-b"}

        create_response = client.post(
            "/api/workspace/capabilities/private",
            headers=tenant_a,
            json={
                "capability_type": "tool",
                "capability_id": "draft_writer",
                "display_name": "Tenant A Draft Writer",
            },
        )
        tenant_a_list = client.get("/api/workspace/capabilities/private", headers=tenant_a)
        tenant_b_list = client.get("/api/workspace/capabilities/private", headers=tenant_b)
        official_catalog = client.get("/api/catalog/capabilities", headers=tenant_a)

        self.assertEqual(create_response.status_code, 201)
        private_capability = create_response.json()
        self.assertEqual(private_capability["tenant_id"], "tenant-a")
        self.assertEqual(private_capability["source"], "tenant_private")
        self.assertEqual(tenant_a_list.json()["capabilities"][0]["capability_id"], "draft_writer")
        self.assertEqual(tenant_b_list.json()["capabilities"], [])
        self.assertFalse(
            any(item["capability_key"] == "draft_writer" for item in official_catalog.json()["capabilities"])
        )

    def test_workspace_cannot_write_official_capability_catalog(self):
        app = create_app(self.db_path)
        client = TestClient(app)

        unauthorized_platform_write = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "official.blocked",
                "type": "tool",
                "display_name": "Blocked",
            },
            headers={"X-Tenant-Id": "tenant-a"},
        )
        catalog_response = client.get("/api/catalog/capabilities", headers={"X-Tenant-Id": "tenant-a"})

        self.assertEqual(unauthorized_platform_write.status_code, 401)
        self.assertEqual(catalog_response.status_code, 200)

    def test_workspace_private_model_tool_connector_configs_are_tenant_private(self):
        app = create_app(self.db_path)
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-a"}

        model = client.post(
            "/api/workspace/private-models",
            headers=headers,
            json={
                "name": "tenant-deepseek",
                "provider_type": "newapi-compatible",
                "base_url": "https://tenant-gateway.example.com",
                "model_name": "tenant-model-a",
                "credential_ref": "env:TENANT_A_MODEL_KEY",
                "enabled": True,
            },
        )
        tool = client.post(
            "/api/workspace/private-tools",
            headers=headers,
            json={
                "name": "tenant-writer",
                "type": "llm_tool",
                "description": "Tenant private writing tool",
                "config_ref": "env:TENANT_A_TOOL_CONFIG",
                "enabled": True,
            },
        )
        connector = client.post(
            "/api/workspace/private-connectors",
            headers=headers,
            json={
                "name": "tenant-crm",
                "connector_type": "crm",
                "config_ref": "env:TENANT_A_CRM_CONFIG",
                "enabled": True,
            },
        )

        self.assertEqual(model.status_code, 201)
        self.assertEqual(tool.status_code, 201)
        self.assertEqual(connector.status_code, 201)
        self.assertEqual(model.json()["tenant_id"], "tenant-a")
        self.assertEqual(model.json()["source"], "tenant_private")
        self.assertEqual(model.json()["provider_type"], "newapi-compatible")
        self.assertEqual(model.json()["credential_ref"], "env:TENANT_A_MODEL_KEY")
        self.assertEqual(tool.json()["source"], "tenant_private")
        self.assertEqual(tool.json()["type"], "llm_tool")
        self.assertEqual(connector.json()["source"], "tenant_private")
        self.assertEqual(connector.json()["connector_type"], "crm")
        self.assertFalse(
            any(
                item["capability_key"] in {"tenant-deepseek", "tenant-writer", "tenant-crm"}
                for item in client.get("/api/catalog/capabilities", headers=headers).json()["capabilities"]
            )
        )

    def test_workspace_capability_selector_unifies_official_and_tenant_private_sources(self):
        app = create_app(self.db_path)
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-a"}
        client.post(
            "/api/workspace/private-tools",
            headers=headers,
            json={
                "name": "tenant-writer",
                "type": "llm_tool",
                "description": "Tenant private writing tool",
                "config_ref": "env:TENANT_A_TOOL_CONFIG",
                "enabled": True,
            },
        )

        response = client.get("/api/workspace/capabilities/selector", headers=headers)

        self.assertEqual(response.status_code, 200)
        capabilities = response.json()["capabilities"]
        self.assertTrue(
            any(
                item["source"] == "official"
                and item["capability_type"] == "tool"
                and item["capability_id"] == "model_gateway_tool"
                for item in capabilities
            )
        )
        private = [
            item for item in capabilities
            if item["source"] == "tenant_private" and item["capability_id"] == "tenant-writer"
        ]
        self.assertEqual(len(private), 1)
        self.assertEqual(private[0]["capability_type"], "tool")
        self.assertEqual(private[0]["label"], "tenant-writer")

    def test_task_execution_can_select_tenant_private_tool_and_usage_records_private_source(self):
        app = create_app(
            self.db_path,
            tool_functions={"model_gateway_tool": RecordingExecutor().execute},
        )
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-001"}
        client.post(
            "/api/workspace/private-tools",
            headers=headers,
            json={
                "name": "tenant-writer",
                "type": "llm_tool",
                "description": "Tenant private writing tool",
                "config_ref": "env:TENANT_A_TOOL_CONFIG",
                "enabled": True,
            },
        )
        task_id = client.post(
            "/api/task",
            headers=headers,
            json={
                "content": "Create private draft",
                "capability_source": "tenant_private",
                "capability_type": "tool",
                "capability_id": "tenant-writer",
            },
        ).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        usage_response = client.get(
            "/api/platform/usage",
            params={"tenant_id": "tenant-a", "capability_source": "tenant_private"},
            headers={"X-Platform-Admin-Token": "platform-admin-dev"},
        )

        self.assertEqual(run_response.status_code, 200)
        self.assertEqual(run_response.json()["selected_tool"], "tenant-writer")
        events = usage_response.json()["usage_events"]
        self.assertEqual(
            [event["event_type"] for event in events],
            ["usage.tool_call", "usage.task_execution"],
        )
        self.assertTrue(all(event["capability_source"] == "tenant_private" for event in events))
        tool_events = [event for event in events if event["capability_type"] == "tool"]
        self.assertEqual(tool_events[0]["capability_id"], "tenant-writer")
        self.assertEqual(tool_events[0]["tenant_id"], "tenant-a")
        self.assertEqual(tool_events[0]["task_id"], task_id)


if __name__ == "__main__":
    unittest.main()
