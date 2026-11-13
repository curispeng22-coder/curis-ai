from __future__ import annotations

import json
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
SECRET = "phase6-secret-value-1234567890"


class Phase6WorkflowMvpTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            os.environ,
            {"CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev"},
        )
        environment.start()
        self.addCleanup(environment.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.gateway_prompts: list[str] = []
        self.gateway_headers: list[dict[str, str]] = []

        def fake_http_post(url, payload, headers, timeout):
            self.gateway_prompts.append(payload["messages"][-1]["content"])
            self.gateway_headers.append(headers)
            return {
                "choices": [{"message": {"content": f"workflow-output-{len(self.gateway_prompts)}"}}],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 7,
                    "total_tokens": 12,
                    "estimated_cost": 0.004,
                },
            }

        self.client = TestClient(
            create_app(
                self.db_path,
                model_gateway_adapter=ModelGatewayAdapter(
                    base_url="http://gateway.invalid",
                    api_key="fallback-key",
                    model_name="fallback-model",
                    http_post=fake_http_post,
                ),
            )
        )

    def test_workflow_template_is_official_sequential_and_marketplace_is_not_enabled(self):
        response = self.client.get("/api/workspace/workflow-templates", headers=TENANT_A)

        self.assertEqual(response.status_code, 200, response.text)
        templates = response.json()["workflow_templates"]
        template = next(item for item in templates if item["id"] == "official.workflow.software_rnd_sop")
        self.assertEqual(template["source"], "official")
        self.assertEqual(template["process_type"], "sequential")
        self.assertEqual(template["status"], "active")
        self.assertEqual(template["steps"][0]["employee_role"], "tech_lead")
        self.assertEqual(template["steps"][-1]["step_type"], "final_report")
        self.assertFalse(any(item["source"] == "marketplace" and item["status"] == "active" for item in templates))

    def test_workflow_run_executes_sequential_employee_steps_and_records_redacted_events(self):
        os.environ["CURIS_ENV"] = "local"
        self.addCleanup(lambda: os.environ.pop("CURIS_ENV", None))
        os.environ["CURIS_MODEL_GATEWAY_PRICE_VERSION"] = "phase6-test-v1"
        self.addCleanup(lambda: os.environ.pop("CURIS_MODEL_GATEWAY_PRICE_VERSION", None))
        department = self._create_department(TENANT_A)
        employees = self._create_rnd_employees(TENANT_A, department["id"])
        credential = self._create_credential(TENANT_A)
        self._create_private_model(TENANT_A, credential["credential_ref"])
        for employee in employees.values():
            self._bind_private_model(TENANT_A, employee["id"])
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "客户线索项目",
                "goal": "完成客户线索研发",
                "owner_employee_id": employees["tech_lead"]["id"],
            },
        ).json()

        created = self.client.post(
            "/api/workspace/workflows",
            headers=TENANT_A,
            json={
                "workflow_template_id": "official.workflow.software_rnd_sop",
                "department_id": department["id"],
                "company_id": company["company_id"],
                "project_id": project["project_id"],
                "content": "开发一个客户线索管理页面和后端接口",
                "name": "客户线索研发 SOP",
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        workflow_run_id = created.json()["workflow_run_id"]
        self.assertEqual(created.json()["tenant_id"], "tenant-a")
        self.assertEqual(created.json()["status"], "pending")
        self.assertEqual([step["status"] for step in created.json()["steps"]], ["pending"] * 7)

        statuses = []
        for _ in range(7):
            run = self.client.post(
                f"/api/workspace/workflows/{workflow_run_id}/run-next-step",
                headers=TENANT_A,
            )
            self.assertEqual(run.status_code, 200, run.text)
            statuses.append(run.json()["status"])

        detail = self.client.get(f"/api/workspace/workflows/{workflow_run_id}", headers=TENANT_A).json()
        self.assertEqual(statuses[-1], "succeeded")
        self.assertEqual(detail["status"], "succeeded")
        self.assertEqual(len(detail["steps"]), 7)
        self.assertEqual(len(detail["step_results"]), 7)
        self.assertIn("workflow-output-7", detail["final_report"])
        self.assertEqual(detail["steps"][0]["employee_role"], "tech_lead")
        self.assertEqual(detail["steps"][1]["employee_role"], "product_manager")
        self.assertEqual(detail["steps"][2]["employee_role"], "architect")
        self.assertEqual(detail["steps"][3]["employee_role"], "frontend_engineer")
        self.assertEqual(detail["steps"][4]["employee_role"], "backend_engineer")
        self.assertEqual(detail["steps"][5]["employee_role"], "qa_engineer")
        self.assertEqual(detail["steps"][6]["employee_role"], "tech_lead")
        self.assertEqual(self.gateway_headers[-1]["Authorization"], f"Bearer {SECRET}")

        usage = self.client.get(
            "/api/platform/usage?tenant_id=tenant-a&capability_source=tenant_private",
            headers=ADMIN,
        ).json()["usage_events"]
        model_calls = [item for item in usage if item["event_type"] == "usage.model_call"]
        self.assertEqual(len(model_calls), 7)
        self.assertTrue(all(item["workflow_run_id"] == workflow_run_id for item in model_calls))
        self.assertTrue(all(item["workflow_step_id"] for item in model_calls))
        self.assertTrue(all(item["employee_id"] for item in model_calls))
        self.assertTrue(all(item["payload"]["usage_record_id"] for item in model_calls))
        self.assertTrue(all("credential_id" not in item["payload"] for item in model_calls))
        self.assertNotIn(SECRET, json.dumps(model_calls))

        audit = self.client.get(
            f"/api/platform/audit?tenant_id=tenant-a&event_type=workflow.run.completed",
            headers=ADMIN,
        ).json()["audit_events"]
        self.assertEqual(len(audit), 1)
        self.assertEqual(json.loads(audit[0]["payload"])["workflow_run_id"], workflow_run_id)
        self.assertNotIn(SECRET, json.dumps(audit))

        isolated = self.client.get(f"/api/workspace/workflows/{workflow_run_id}", headers=TENANT_B)
        self.assertEqual(isolated.status_code, 404)

    def test_failed_step_marks_workflow_failed(self):
        def broken_tool(prompt):
            raise RuntimeError("safe failure")

        client = TestClient(create_app(self.db_path, tool_functions={"model_gateway_tool": broken_tool}))
        department = self._create_department(TENANT_A, client=client)
        employees = self._create_rnd_employees(TENANT_A, department["id"], client=client)
        for employee in employees.values():
            self._bind_official_model(TENANT_A, employee["id"], client=client)
        created = client.post(
            "/api/workspace/workflows",
            headers=TENANT_A,
            json={
                "workflow_template_id": "official.workflow.software_rnd_sop",
                "department_id": department["id"],
                "content": "实现失败场景",
            },
        ).json()

        response = client.post(
            f"/api/workspace/workflows/{created['workflow_run_id']}/run-next-step",
            headers=TENANT_A,
        )

        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["status"], "failed")
        self.assertEqual(response.json()["steps"][0]["status"], "failed")

    def _create_department(self, headers, client=None):
        client = client or self.client
        response = client.post(
            "/api/workspace/departments",
            headers=headers,
            json={"template_id": "official.department.software_rnd", "name": "研发部"},
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _create_rnd_employees(self, headers, department_id: str, client=None):
        client = client or self.client
        templates = {
            item["role"]: item["id"]
            for item in client.get("/api/workspace/employee-templates", headers=headers).json()["employee_templates"]
        }
        employees = {}
        for role, template_id in templates.items():
            response = client.post(
                "/api/workspace/employees",
                headers=headers,
                json={
                    "department_id": department_id,
                    "template_id": template_id,
                    "name": f"{role} 员工",
                    "instructions_override": f"按 {role} 职责执行。",
                    "status": "idle",
                    "enabled": True,
                },
            )
            self.assertEqual(response.status_code, 201, response.text)
            employees[role] = response.json()
        return employees

    def _create_credential(self, headers):
        response = self.client.post(
            "/api/workspace/credentials",
            headers=headers,
            json={"name": "Workflow Key", "provider": "newapi", "credential_type": "api_key", "secret": SECRET},
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _create_private_model(self, headers, credential_ref: str):
        response = self.client.post(
            "/api/workspace/private-models",
            headers=headers,
            json={
                "name": "workflow-private-model",
                "provider_type": "newapi-compatible",
                "base_url": "https://tenant-gateway.example",
                "model_name": "workflow-private-model-v1",
                "credential_ref": credential_ref,
                "enabled": True,
            },
        )
        self.assertEqual(response.status_code, 201, response.text)

    def _bind_private_model(self, headers, employee_id: str):
        response = self.client.put(
            f"/api/workspace/employees/{employee_id}/capabilities",
            headers=headers,
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "model",
                        "capability_id": "workflow-private-model",
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(response.status_code, 200, response.text)

    def _bind_official_model(self, headers, employee_id: str, client=None):
        client = client or self.client
        response = client.put(
            f"/api/workspace/employees/{employee_id}/capabilities",
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
        self.assertEqual(response.status_code, 200, response.text)


if __name__ == "__main__":
    unittest.main()
