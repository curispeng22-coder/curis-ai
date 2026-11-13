import sqlite3
import hashlib
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter


ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class RecordingHttpPost:
    def __init__(self):
        self.calls = []

    def __call__(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        self.calls.append({"url": url, "payload": payload, "headers": headers})
        return {
            "choices": [{"message": {"content": f"model:{payload['model']}"}}],
            "usage": {"total_tokens": 3, "estimated_cost": 0.0003},
        }


class TenantModelPreferenceTest(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            "os.environ",
            {
                "CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev",
                "CURIS_MODEL_GATEWAY_ID": "newapi",
                "CURIS_MODEL_GATEWAY_BASE_URL": "http://127.0.0.1:9/fixture-only",
                "CURIS_MODEL_GATEWAY_API_KEY": "fixture-no-network",
                "CURIS_MODEL_GATEWAY_MODEL": "newapi-default",
            },
        )
        environment.start()
        self.addCleanup(environment.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()

    def tearDown(self):
        self.tmp.cleanup()

    def _client(self, adapter=None):
        return TestClient(create_app(self.db_path, model_gateway_adapter=adapter))

    def _save_discovered_model(
        self,
        tenant_id: str,
        *,
        provider_id: str = "deepseek",
        model_name: str = "deepseek-chat",
        status: str = "active",
        verification_status: str = "verified",
        credential_status: str = "active",
        verification_provider: str | None = None,
        requires_credential: bool = True,
    ) -> str:
        credential_id = f"cred-{tenant_id}-{provider_id}"
        credential_ref = f"vault://tenant/{tenant_id}/credential/{credential_id}"
        self.database.save_credential_metadata(
            credential_id=credential_id,
            tenant_id=tenant_id,
            name="test credential",
            provider=provider_id,
            credential_type="api_key",
            credential_ref=credential_ref,
            status=credential_status,
        )
        capability_id = (
            f"user.{provider_id}."
            f"{hashlib.sha256(model_name.encode()).hexdigest()[:16]}"
        )
        self.database.save_tenant_private_capability(
            tenant_id=tenant_id,
            capability_type="model",
            capability_id=capability_id,
            display_name=model_name,
            status=status,
            metadata={
                "name": model_name,
                "provider_type": provider_id,
                "base_url": "https://provider.example.com",
                "model_name": model_name,
                "credential_ref": credential_ref,
                "provider_protocol": "openai_chat",
                "chat_path": "/v1/chat/completions",
                "discovery_verification": {
                    "status": verification_status,
                    "provider_id": verification_provider or provider_id,
                    "discovery_id": model_name,
                    "model_id": model_name,
                    "mode": "dynamic",
                    "requires_credential": requires_credential,
                },
            },
        )
        return capability_id

    def test_preference_write_read_delete_are_tenant_scoped(self):
        client = self._client()
        tenant_a = {"X-Tenant-Id": "tenant-A"}
        tenant_b = {"X-Tenant-Id": "tenant-B"}

        put_response = client.put(
            "/api/workspace/model-preference",
            json={"model_key": "official.newapi.default"},
            headers=tenant_a,
        )
        read_a = client.get("/api/workspace/model-preference", headers=tenant_a)
        read_b = client.get("/api/workspace/model-preference", headers=tenant_b)
        delete_a = client.delete("/api/workspace/model-preference", headers=tenant_a)
        read_after_delete = client.get("/api/workspace/model-preference", headers=tenant_a)

        self.assertEqual(put_response.status_code, 200)
        preference = put_response.json()["preference"]
        self.assertEqual(preference["tenant_id"], "tenant-A")
        self.assertEqual(preference["model_key"], "official.newapi.default")
        self.assertEqual(preference["gateway_ref"], "newapi")
        self.assertEqual(preference["model_name"], "newapi-default")
        self.assertEqual(preference["source"], "official")
        self.assertEqual(read_a.json()["preference"]["model_key"], "official.newapi.default")
        self.assertIsNone(read_b.json()["preference"])
        self.assertEqual(delete_a.status_code, 200)
        self.assertIsNone(read_after_delete.json()["preference"])

    def test_preference_accepts_verified_tenant_model_and_rejects_ineligible_entries(self):
        client = self._client()
        tenant = {"X-Tenant-Id": "tenant-A"}
        inactive = client.post(
            "/api/platform/models",
            json={
                "model_key": "official.inactive",
                "provider_id": "newapi",
                "display_name": "Inactive",
                "gateway_ref": "newapi",
                "supported_models": ["inactive-model"],
                "status": "inactive",
            },
            headers=ADMIN,
        )
        self.assertEqual(inactive.status_code, 201)

        private_key = self._save_discovered_model("tenant-A")
        wrong_tenant_key = self._save_discovered_model(
            "tenant-B", model_name="tenant-b-only-model"
        )
        stale_key = self._save_discovered_model(
            "tenant-A", model_name="stale-model", verification_status="unavailable"
        )
        wrong_provider_key = self._save_discovered_model(
            "tenant-A",
            model_name="wrong-provider-model",
            verification_provider="openai",
        )
        local_key = self._save_discovered_model(
            "tenant-A",
            provider_id="ollama",
            model_name="qwen-local",
            requires_credential=False,
        )

        inactive_response = client.put(
            "/api/workspace/model-preference",
            json={"model_key": "official.inactive"},
            headers=tenant,
        )
        private_response = client.put(
            "/api/workspace/model-preference",
            json={"model_key": private_key},
            headers=tenant,
        )
        wrong_tenant = client.put(
            "/api/workspace/model-preference",
            json={"model_key": wrong_tenant_key},
            headers=tenant,
        )
        stale = client.put(
            "/api/workspace/model-preference",
            json={"model_key": stale_key},
            headers=tenant,
        )
        wrong_provider = client.put(
            "/api/workspace/model-preference",
            json={"model_key": wrong_provider_key},
            headers=tenant,
        )
        local = client.put(
            "/api/workspace/model-preference",
            json={"model_key": local_key},
            headers=tenant,
        )
        unknown = client.put(
            "/api/workspace/model-preference",
            json={"model_key": "user.deepseek.unknown"},
            headers=tenant,
        )

        self.assertEqual(inactive_response.status_code, 422)
        self.assertEqual(private_response.status_code, 200)
        self.assertEqual(private_response.json()["preference"]["source"], "tenant_private")
        self.assertEqual(wrong_tenant.status_code, 422)
        self.assertEqual(stale.status_code, 422)
        self.assertEqual(wrong_provider.status_code, 422)
        self.assertEqual(local.status_code, 200)
        self.assertEqual(unknown.status_code, 422)

    def test_private_preference_survives_reconstruction_but_missing_credential_is_not_ready(self):
        model_key = self._save_discovered_model("tenant-A")
        headers = {"X-Tenant-Id": "tenant-A"}
        client = self._client()
        self.assertEqual(
            client.put(
                "/api/workspace/model-preference",
                json={"model_key": model_key},
                headers=headers,
            ).status_code,
            200,
        )
        client.close()

        reconstructed = self._client()
        restored = reconstructed.get("/api/workspace/model-preference", headers=headers).json()
        self.assertEqual(restored["preference"]["model_key"], model_key)
        credential_id = "cred-tenant-A-deepseek"
        self.database.disable_credential_metadata("tenant-A", credential_id)
        unavailable = reconstructed.get("/api/workspace/model-preference", headers=headers).json()
        self.assertIsNone(unavailable["preference"])
        self.assertFalse(any(item["model_key"] == model_key for item in unavailable["available_models"]))

    def test_preference_persistence_and_api_are_metadata_only(self):
        client = self._client()
        response = client.put(
            "/api/workspace/model-preference",
            json={"model_key": "official.newapi.default"},
            headers={"X-Tenant-Id": "tenant-A"},
        )

        self.assertEqual(response.status_code, 200)
        with closing(sqlite3.connect(self.db_path)) as connection:
            columns = {
                row[1]
                for row in connection.execute("pragma table_info(tenant_model_preferences)")
            }
        self.assertEqual(
            columns,
            {"tenant_id", "model_key", "gateway_ref", "model_name", "source", "updated_at"},
        )
        payload_text = str(client.get("/api/workspace/model-preference", headers={"X-Tenant-Id": "tenant-A"}).json())
        for forbidden in (
            "api_key",
            "token",
            "password",
            "secret",
            "credential_ref",
            "Authorization",
            "prompt",
            "output",
            "raw_http",
            "billing",
            "ROI",
            "tenant_package",
            "marketplace",
            "department_policy",
            "employee_policy",
            "optimization",
        ):
            self.assertNotIn(forbidden, payload_text)

    def test_runtime_uses_valid_preference_through_model_gateway_adapter_and_falls_back_when_invalid(self):
        http_post = RecordingHttpPost()
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="test-key",
            gateway_id="fallback-gw",
            model_name="fallback-model",
            http_post=http_post,
            gateway_resolver=self.database.get_model_gateway,
        )
        with self.database.connect() as con:
            con.execute("update model_gateways set base_url='https://selected.example.invalid', credential_ref='env:CURIS_MODEL_GATEWAY_API_KEY' where gateway_id='newapi'")
        client = self._client(adapter)
        headers = {"X-Tenant-Id": "tenant-A", "X-Ceo-Id": "ceo-1"}

        set_response = client.put(
            "/api/workspace/model-preference",
            json={"model_key": "official.newapi.default"},
            headers=headers,
        )
        company = client.get("/api/workspace/companies", headers=headers).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "Model 业务部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=headers,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "Model Employee",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        client.post(
            "/api/platform/gateways",
            headers=ADMIN,
            json={
                "gateway_id": "fallback-gw",
                "name": "Fallback Gateway",
                "base_url": "https://newapi.example.com",
                "default_model": "fallback-model",
            },
        )
        client.post(
            "/api/platform/models",
            headers=ADMIN,
            json={
                "model_key": "model.fallback",
                "provider_id": "fallback-gw",
                "display_name": "Fallback Model",
                "gateway_ref": "fallback-gw",
                "supported_models": ["fallback-model"],
                "default_model": "fallback-model",
            },
        )
        project = client.post(
            "/api/workspace/projects",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "Model Project",
                "goal": "验证模型偏好",
                "owner_employee_id": employee["id"],
                "status": "active",
            },
        ).json()

        def create_task(content: str) -> str:
            return client.post(
                f"/api/workspace/projects/{project['project_id']}/tasks",
                headers=headers,
                json={
                    "content": content,
                    "employee_id": employee["id"],
                },
            ).json()["task_id"]

        task_id = create_task("Run model task")
        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        self.assertEqual(run_response.status_code, 200, run_response.text)
        usage_events = client.get(
            "/api/platform/usage",
            params={"tenant_id": "tenant-A"},
            headers={"X-Platform-Admin-Token": "platform-admin-dev"},
        ).json()["usage_events"]
        usage = next(event["payload"] for event in usage_events if event["payload"].get("task_id") == task_id and "model_gateway_id" in event["payload"])

        self.assertEqual(set_response.status_code, 200)
        self.assertEqual(run_response.status_code, 200)
        self.assertEqual(http_post.calls[-1]["payload"]["model"], "newapi-default")
        self.assertEqual(usage["model_gateway_id"], "newapi")
        self.assertEqual(usage["model_name"], "newapi-default")
        self.assertEqual(http_post.calls[-1]["url"], "https://selected.example.invalid/v1/chat/completions")
        self.assertEqual(http_post.calls[-1]["headers"]["Authorization"], "Bearer fixture-no-network")

        disable_response = client.put(
            "/api/platform/models/official.newapi.default",
            json={"action": "disable"},
            headers=ADMIN,
        )
        stale_task_id = create_task("Run fallback task")
        stale_run = client.post(f"/api/task/{stale_task_id}/run", headers=headers)

        self.assertEqual(disable_response.status_code, 200)
        self.assertEqual(stale_run.status_code, 200, stale_run.text)
        self.assertEqual(http_post.calls[-1]["payload"]["model"], "fallback-model")


if __name__ == "__main__":
    unittest.main()
