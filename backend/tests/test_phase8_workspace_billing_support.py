from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}
ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class Phase8WorkspaceBillingSupportTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev",
                "CURIS_MODEL_GATEWAY_PRICE_VERSION": "phase8-test-v1",
            },
        )
        environment.start()
        self.addCleanup(environment.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))

        def fake_http_post(url, payload, headers, timeout):
            return {
                "choices": [{"message": {"content": "billing support output"}}],
                "usage": {
                    "prompt_tokens": 11,
                    "completion_tokens": 13,
                    "total_tokens": 24,
                    "estimated_cost": 0.006,
                },
            }

        self.client = TestClient(
            create_app(
                self.db_path,
                model_gateway_adapter=ModelGatewayAdapter(
                    base_url="https://gateway.example",
                    api_key="phase8-test-key",
                    gateway_id="newapi",
                    model_name="deepseek-v4-flash",
                    http_post=fake_http_post,
                ),
            )
        )

    def test_ai_usage_ledger_contains_cost_fields_and_audit_only_references_it(self):
        employee = self._create_tech_lead_with_binding(TENANT_A)
        task_id = self.client.post(
            f"/api/workspace/projects/{employee['_project_id']}/tasks",
            headers=TENANT_A,
            json={
                "content": "整理 Phase-8 billing usage evidence",
                "employee_id": employee["id"],
                "capability_source": "official",
                "capability_type": "tool",
                "capability_id": "model_gateway_tool",
            },
        ).json()["task_id"]

        run = self.client.post(f"/api/task/{task_id}/run", headers=TENANT_A)
        self.assertEqual(run.status_code, 200, run.text)
        record = self.client.get(
            "/api/ai-usage/records", headers=TENANT_A
        ).json()["records"][0]
        audit = self.client.get(
            "/api/platform/usage?tenant_id=tenant-a", headers=ADMIN
        ).json()["usage_events"]
        model_event = next(item for item in audit if item["event_type"] == "usage.model_call")

        self.assertEqual(record["tenant_id"], "tenant-a")
        self.assertEqual(record["task_id"], task_id)
        self.assertEqual(record["employee_id"], employee["id"])
        self.assertEqual(record["capability_id"], "model_gateway_tool")
        self.assertEqual(record["model_name"], "deepseek-v4-flash")
        self.assertEqual(record["input_tokens"], 11)
        self.assertEqual(record["output_tokens"], 13)
        self.assertEqual(record["total_tokens"], 24)
        self.assertEqual(record["cost_amount"], "0.006")
        self.assertEqual(record["cost_source"], "estimated")
        self.assertEqual(model_event["payload"]["usage_record_id"], record["usage_record_id"])
        self.assertNotIn("total_tokens", model_event["payload"])
        self.assertNotIn("estimated_cost", model_event["payload"])

    def test_usage_meter_is_admin_read_only_tenant_scoped_and_not_billing_event(self):
        employee_a = self._create_tech_lead_with_binding(TENANT_A)
        employee_b = self._create_tech_lead_with_binding(TENANT_B)
        task_a = self.client.post(
            f"/api/workspace/projects/{employee_a['_project_id']}/tasks",
            headers=TENANT_A,
            json={
                "content": "Tenant A usage meter task",
                "employee_id": employee_a["id"],
                "capability_source": "official",
                "capability_type": "tool",
                "capability_id": "model_gateway_tool",
            },
        ).json()["task_id"]
        task_b = self.client.post(
            f"/api/workspace/projects/{employee_b['_project_id']}/tasks",
            headers=TENANT_B,
            json={
                "content": "Tenant B usage meter task",
                "employee_id": employee_b["id"],
                "capability_source": "official",
                "capability_type": "tool",
                "capability_id": "model_gateway_tool",
            },
        ).json()["task_id"]
        self.assertEqual(
            self.client.post(f"/api/task/{task_a}/run", headers=TENANT_A).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(f"/api/task/{task_b}/run", headers=TENANT_B).status_code,
            200,
        )

        no_admin = self.client.get("/api/platform/usage-meter?tenant_id=tenant-a")
        missing_tenant = self.client.get("/api/platform/usage-meter", headers=ADMIN)
        response = self.client.get(
            "/api/platform/usage-meter?tenant_id=tenant-a",
            headers=ADMIN,
        )

        self.assertEqual(no_admin.status_code, 401)
        self.assertEqual(missing_tenant.status_code, 422)
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload["tenant_id"], "tenant-a")
        self.assertEqual(payload["totals"]["usage_event_count"], 1)
        self.assertEqual(payload["totals"]["total_tokens"], 24)
        self.assertEqual(payload["totals"]["estimated_cost"], 0.006)
        self.assertTrue(any(item["model_name"] == "deepseek-v4-flash" for item in payload["by_model"]))
        self.assertNotIn(task_b, str(payload))
        self.assertNotIn("billing_event", payload)
        self.assertNotIn("invoice", payload)

    def _create_tech_lead_with_binding(self, headers: dict[str, str]) -> dict:
        department = self.client.post(
            "/api/workspace/departments",
            headers=headers,
            json={"template_id": "official.department.software_rnd", "name": "研发部"},
        )
        self.assertEqual(department.status_code, 201, department.text)
        templates = self.client.get(
            "/api/workspace/employee-templates",
            headers=headers,
        ).json()["employee_templates"]
        template_id = next(item["id"] for item in templates if item["role"] == "tech_lead")
        employee = self.client.post(
            "/api/workspace/employees",
            headers=headers,
            json={
                "department_id": department.json()["id"],
                "template_id": template_id,
                "name": "Tech Lead",
                "status": "idle",
                "enabled": True,
            },
        )
        self.assertEqual(employee.status_code, 201, employee.text)
        binding = self.client.put(
            f"/api/workspace/employees/{employee.json()['id']}/capabilities",
            headers=headers,
            json={
                "bindings": [
                    {
                        "capability_source": "official",
                        "capability_type": "tool",
                        "capability_id": "model_gateway_tool",
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(binding.status_code, 200, binding.text)
        company = self.client.get(
            "/api/workspace/companies", headers=headers
        ).json()["companies"][0]
        project = self.client.post(
            "/api/workspace/projects",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "department_id": department.json()["id"],
                "name": "Usage Project",
                "goal": "Measure model usage",
                "owner_employee_id": employee.json()["id"],
            },
        )
        self.assertEqual(project.status_code, 201, project.text)
        return {**employee.json(), "_project_id": project.json()["project_id"]}


if __name__ == "__main__":
    unittest.main()


class UsageMeterMoneyFactsTests(unittest.TestCase):
    def test_amount_unknown_does_not_follow_token_metering(self):
        from app.usage_meter import UsageMeterService
        def event(amount, currency="USD"):
            return {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2,
                    "metering_status": "confirmed", "cost_amount": amount, "currency": currency,
                    "cost_source": "unknown" if amount is None else "provider_reported"}
        empty = UsageMeterService._totals([])
        self.assertIsNone(empty["estimated_cost"])
        self.assertEqual(empty["cost_by_currency"], [])
        unknown = UsageMeterService._totals([event(None)])
        self.assertEqual(unknown["unmetered_count"], 0)
        self.assertEqual(unknown["unknown_cost_count"], 1)
        self.assertIsNone(unknown["estimated_cost"])
        zero = UsageMeterService._totals([event("0")])
        self.assertEqual(zero["estimated_cost"], 0.0)
        self.assertEqual(zero["unknown_cost_count"], 0)
        partial = UsageMeterService._totals([event("0.25"), event(None)])
        self.assertIsNone(partial["estimated_cost"])
        self.assertEqual(partial["cost_by_currency"], [{"currency": "USD", "known_cost": 0.25, "unknown_cost_count": 1}])
        mixed = UsageMeterService._totals([event("1", "USD"), event("2", "EUR")])
        self.assertIsNone(mixed["estimated_cost"])
        self.assertIsNone(mixed["currency"])
        self.assertEqual([row["known_cost"] for row in mixed["cost_by_currency"]], [2.0, 1.0])
