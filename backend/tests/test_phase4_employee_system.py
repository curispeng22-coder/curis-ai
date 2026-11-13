from __future__ import annotations

import os
import tempfile
import unittest

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}
ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class Phase4EmployeeSystemTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(
            create_app(
                self.db_path,
                tool_functions={
                    "model_gateway_tool": lambda prompt: {
                        "output": f"employee-result: {prompt[:24]}",
                        "cost": 0.02,
                        "model_gateway_id": "newapi",
                        "model_name": "phase4-demo-model",
                        "prompt_tokens": 12,
                        "completion_tokens": 8,
                        "total_tokens": 20,
                        "estimated_cost": 0.02,
                        "status": "success",
                    }
                },
            )
        )

    def test_official_research_department_and_employee_templates_are_available(self):
        employees = self.client.get("/api/workspace/employee-templates", headers=TENANT_A).json()[
            "employee_templates"
        ]
        departments = self.client.get("/api/workspace/department-templates", headers=TENANT_A).json()[
            "department_templates"
        ]

        roles = {item["role"] for item in employees}
        self.assertEqual(
            {
                "tech_lead",
                "product_manager",
                "architect",
                "frontend_engineer",
                "backend_engineer",
                "qa_engineer",
                "devops_engineer",
            },
            roles,
        )
        self.assertTrue(all(item["source"] == "official" for item in employees))
        rnd = next(item for item in departments if item["department_type"] == "software_rnd")
        self.assertEqual(rnd["source"], "official")
        self.assertEqual(len(rnd["default_employee_templates"]), 6)

    def test_tenant_can_create_department_employee_and_bind_private_capability(self):
        department = self._create_department(TENANT_A)
        employee = self._create_employee(TENANT_A, department["id"])
        private_tool = self.client.post(
            "/api/workspace/private-tools",
            json={
                "name": "tenant-writer",
                "type": "llm_tool",
                "description": "tenant scoped writer",
                "config_ref": "env:TENANT_WRITER_CONFIG",
                "enabled": True,
            },
            headers=TENANT_A,
        )
        self.assertEqual(private_tool.status_code, 201)

        response = self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "tool",
                        "capability_id": "tenant-writer",
                        "priority": 10,
                        "enabled": True,
                    }
                ]
            },
            headers=TENANT_A,
        )
        self.assertEqual(response.status_code, 200)
        bindings = response.json()["bindings"]
        self.assertEqual(bindings[0]["employee_id"], employee["id"])
        self.assertEqual(bindings[0]["capability_source"], "tenant_private")

        isolated = self.client.get("/api/workspace/employees", headers=TENANT_B).json()
        self.assertEqual(isolated["employees"], [])

    def test_fake_bound_capability_does_not_create_authoritative_ai_usage(self):
        department = self._create_department(TENANT_A)
        employee = self._create_employee(TENANT_A, department["id"])
        private_model = self.client.post(
            "/api/workspace/private-models",
            json={
                "name": "tenant-model",
                "provider_type": "newapi-compatible",
                "base_url": "https://gateway.example.test",
                "model_name": "tenant-model-v1",
                "credential_ref": "env:TENANT_MODEL_REF",
                "enabled": True,
            },
            headers=TENANT_A,
        )
        self.assertEqual(private_model.status_code, 201)
        binding = self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "model",
                        "capability_id": "tenant-model",
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
            headers=TENANT_A,
        )
        self.assertEqual(binding.status_code, 200)

        created = self.client.post(
            "/api/task",
            json={"content": "实现一个后端接口", "employee_id": employee["id"]},
            headers=TENANT_A,
        ).json()
        task_id = created["task_id"]
        task = self.client.get(f"/api/task/{task_id}", headers=TENANT_A).json()
        self.assertEqual(task["employee_id"], employee["id"])
        self.assertEqual(task["employee_role"], "tech_lead")
        self.assertEqual(task["requested_capability_source"], "tenant_private")

        run = self.client.post(f"/api/task/{task_id}/run", headers=TENANT_A)
        self.assertEqual(run.status_code, 200, run.text)
        ledger = self.client.get("/api/ai-usage/records", headers=TENANT_A).json()["records"]
        self.assertEqual(ledger, [])

    def _create_department(self, headers):
        response = self.client.post(
            "/api/workspace/departments",
            json={
                "template_id": "official.department.software_rnd",
                "name": "研发部",
                "enabled_employee_template_ids": ["official.employee.tech_lead"],
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _create_employee(self, headers, department_id: str):
        response = self.client.post(
            "/api/workspace/employees",
            json={
                "department_id": department_id,
                "template_id": "official.employee.tech_lead",
                "name": "技术负责人",
                "instructions_override": "按研发负责人职责拆解任务。",
                "enabled": True,
                "status": "idle",
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()


if __name__ == "__main__":
    unittest.main()
