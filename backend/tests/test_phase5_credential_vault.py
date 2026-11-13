from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}
ADMIN = {"Authorization": "Bearer platform-admin-dev"}
SECRET = "phase5-secret-value-1234567890"


class Phase5CredentialVaultTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))

    def _client(self, **env):
        old_env = {key: os.environ.get(key) for key in env}
        os.environ.update({key: str(value) for key, value in env.items()})
        self.addCleanup(lambda: self._restore_env(old_env))
        return TestClient(create_app(self.db_path))

    @staticmethod
    def _restore_env(old_env):
        for key, value in old_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_credential_create_stores_metadata_without_plaintext_and_returns_safe_ref(self):
        client = self._client(CURIS_ENV="local")

        response = client.post(
            "/api/workspace/credentials",
            headers=TENANT_A,
            json={
                "name": "Tenant DeepSeek",
                "provider": "newapi",
                "credential_type": "api_key",
                "secret": SECRET,
            },
        )

        self.assertEqual(response.status_code, 201, response.text)
        credential = response.json()
        self.assertEqual(credential["tenant_id"], "tenant-a")
        self.assertEqual(credential["status"], "active")
        self.assertRegex(
            credential["credential_ref"],
            r"^local-dev://tenant/tenant-a/credential/cred-[0-9a-f-]+$",
        )
        self.assertNotIn(SECRET, json.dumps(credential))
        with open(self.db_path, "rb") as file:
            self.assertNotIn(SECRET.encode(), file.read())

    def test_resolver_enforces_tenant_status_and_environment_boundaries(self):
        client = self._client(CURIS_ENV="local")
        credential = client.post(
            "/api/workspace/credentials",
            headers=TENANT_A,
            json={
                "name": "Tenant Key",
                "provider": "newapi",
                "credential_type": "api_key",
                "secret": SECRET,
            },
        ).json()

        same_tenant = client.post(
            f"/api/workspace/credentials/{credential['credential_id']}/test",
            headers=TENANT_A,
        )
        self.assertEqual(same_tenant.status_code, 200)
        self.assertEqual(same_tenant.json()["status"], "ok")
        self.assertNotIn(SECRET, same_tenant.text)

        cross_tenant = client.post(
            f"/api/workspace/credentials/{credential['credential_id']}/test",
            headers=TENANT_B,
        )
        self.assertEqual(cross_tenant.status_code, 404)
        self.assertNotIn(SECRET, cross_tenant.text)

        disabled = client.post(
            f"/api/workspace/credentials/{credential['credential_id']}/disable",
            headers=TENANT_A,
        )
        self.assertEqual(disabled.status_code, 200)
        disabled_test = client.post(
            f"/api/workspace/credentials/{credential['credential_id']}/test",
            headers=TENANT_A,
        )
        self.assertEqual(disabled_test.status_code, 422)
        self.assertNotIn(SECRET, disabled_test.text)

        prod_client = self._client(CURIS_ENV="production")
        prod_test = prod_client.post(
            f"/api/workspace/credentials/{credential['credential_id']}/test",
            headers=TENANT_A,
        )
        self.assertEqual(prod_test.status_code, 422)
        self.assertIn("local-dev", prod_test.text)
        self.assertNotIn(SECRET, prod_test.text)

    def test_private_capabilities_bind_credential_ref_and_usage_event_is_redacted(self):
        captured_headers = []

        def fake_http_post(url, payload, headers, timeout):
            captured_headers.append(headers)
            return {
                "choices": [{"message": {"content": "credential-backed result"}}],
                "usage": {
                    "prompt_tokens": 3,
                    "completion_tokens": 4,
                    "total_tokens": 7,
                    "estimated_cost": 0.001,
                },
            }

        self._client(
            CURIS_ENV="local",
            CURIS_MODEL_GATEWAY_BASE_URL="http://fallback.invalid",
            CURIS_MODEL_GATEWAY_API_KEY="fallback-key",
            CURIS_MODEL_GATEWAY_MODEL="fallback-model",
        )
        app = create_app(
            self.db_path,
            model_gateway_adapter=ModelGatewayAdapter(
                base_url="http://fallback.invalid",
                api_key="fallback-key",
                model_name="fallback-model",
                http_post=fake_http_post,
            ),
        )
        client = TestClient(app)

        credential = client.post(
            "/api/workspace/credentials",
            headers=TENANT_A,
            json={
                "name": "Tenant Model Key",
                "provider": "newapi",
                "credential_type": "api_key",
                "secret": SECRET,
            },
        ).json()
        model = client.post(
            "/api/workspace/private-models",
            headers=TENANT_A,
            json={
                "name": "phase5-private-model",
                "provider_type": "newapi-compatible",
                "base_url": "https://tenant-gateway.example",
                "model_name": "tenant-secret-model",
                "credential_ref": credential["credential_ref"],
                "enabled": True,
            },
        )
        self.assertEqual(model.status_code, 201, model.text)
        self.assertEqual(model.json()["credential_ref"], credential["credential_ref"])
        self.assertNotIn(SECRET, model.text)

        for path, payload in (
            (
                "/api/workspace/private-tools",
                {
                    "name": "phase5-private-tool",
                    "type": "llm_tool",
                    "description": "credential-backed tool",
                    "config_ref": credential["credential_ref"],
                    "enabled": True,
                },
            ),
            (
                "/api/workspace/private-connectors",
                {
                    "name": "phase5-private-connector",
                    "connector_type": "crm",
                    "config_ref": credential["credential_ref"],
                    "enabled": True,
                },
            ),
        ):
            response = client.post(path, headers=TENANT_A, json=payload)
            self.assertEqual(response.status_code, 201, response.text)
            self.assertNotIn(SECRET, response.text)

        company = client.get("/api/workspace/companies", headers=TENANT_A).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "Credential 业务部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "Credential Employee",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT_A,
            json={
                "bindings": [{
                    "capability_source": "tenant_private",
                    "capability_type": "model",
                    "capability_id": "phase5-private-model",
                    "enabled": True,
                }]
            },
        )
        project = client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "Credential Project",
                "goal": "验证私有模型记账",
                "owner_employee_id": employee["id"],
                "status": "active",
            },
        ).json()
        task = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={
                "content": "Run credential backed private model",
                "employee_id": employee["id"],
                "capability_source": "tenant_private",
                "capability_type": "model",
                "capability_id": "phase5-private-model",
            },
        ).json()
        run = client.post(f"/api/task/{task['task_id']}/run", headers=TENANT_A)
        self.assertEqual(run.status_code, 200, run.text)
        self.assertEqual(captured_headers[-1]["Authorization"], f"Bearer {SECRET}")

        usage = client.get(
            "/api/platform/usage?tenant_id=tenant-a&capability_source=tenant_private",
            headers=ADMIN,
        ).json()["usage_events"]
        model_event = next(item for item in usage if item["event_type"] == "usage.model_call")
        self.assertTrue(model_event["payload"]["usage_record_id"])
        self.assertEqual(model_event["credential_id"], "")
        self.assertEqual(model_event["credential_ref_digest"], "")
        self.assertNotIn(SECRET, json.dumps(model_event))

        audit = client.get(
            "/api/platform/audit?tenant_id=tenant-a&event_type=credential.resolved",
            headers=ADMIN,
        ).json()["audit_events"]
        self.assertTrue(audit)
        self.assertNotIn(SECRET, json.dumps(audit))
        audit_payload = json.loads(audit[0]["payload"])
        self.assertEqual(
            set(audit_payload.keys()),
            {
                "tenant_id",
                "credential_id",
                "credential_ref_digest",
                "actor_id",
                "action",
                "status",
                "reason",
                "timestamp",
            },
        )

    def test_workspace_runtime_has_no_platform_calls_and_admin_reads_no_plaintext(self):
        client = self._client(CURIS_ENV="local")
        credential = client.post(
            "/api/workspace/credentials",
            headers=TENANT_A,
            json={
                "name": "Boundary Key",
                "provider": "newapi",
                "credential_type": "api_key",
                "secret": SECRET,
            },
        ).json()

        listing = client.get("/api/workspace/credentials", headers=TENANT_A)
        self.assertEqual(listing.status_code, 200)
        self.assertNotIn(SECRET, listing.text)
        self.assertNotIn("secret", listing.text.lower())

        audit = client.get("/api/platform/audit?tenant_id=tenant-a", headers=ADMIN)
        self.assertEqual(audit.status_code, 200)
        self.assertNotIn(SECRET, audit.text)
        self.assertIn(credential["credential_id"], audit.text)

        page_path = Path(__file__).resolve().parents[2] / "frontend" / "app" / "page.js"
        with open(page_path, "r", encoding="utf-8") as file:
            self.assertNotIn("/api/platform/", file.read())


if __name__ == "__main__":
    unittest.main()
