from __future__ import annotations

import os
import tempfile
import unittest

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class Phase1ACompanyRuntimeFoundationTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        os.environ["CURIS_ENV"] = "local"
        self.addCleanup(lambda: os.environ.pop("CURIS_ENV", None))
        self.prompts: list[str] = []

        def gateway(prompt: str):
            self.prompts.append(prompt)
            return {"output": "safe execution", "cost": 0.01, "status": "success"}

        self.client = TestClient(create_app(self.db_path, tool_functions={"model_gateway_tool": gateway}))

    def test_company_department_employee_and_project_keep_runtime_lineage(self):
        company = self._create_company()
        departments = self.client.get(
            f"/api/workspace/companies/{company['company_id']}/departments", headers=TENANT_A
        )
        self.assertEqual(departments.status_code, 200, departments.text)
        department = departments.json()["departments"][0]
        self.assertEqual(department["department_type"], "software_rnd")
        self.assertEqual(department["name"], "Engineering Department")
        self.assertEqual(department["created_from_template_id"], "official.department.software_rnd")

        employee = self._create_employee(department["id"])
        updated_department = self.client.patch(
            f"/api/workspace/departments/{department['id']}",
            headers=TENANT_A,
            json={"manager_employee_id": employee["id"], "mission": "交付研发项目"},
        )
        self.assertEqual(updated_department.status_code, 200, updated_department.text)
        self.assertEqual(updated_department.json()["manager_employee_id"], employee["id"])
        self.assertEqual(employee["company_id"], company["company_id"])
        self.assertEqual(employee["created_from_template_id"], "official.employee.tech_lead")

        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "研发目标",
                "goal": "构建公司运行时基础",
            },
        )
        self.assertEqual(project.status_code, 201, project.text)
        self.assertEqual(project.json()["company_id"], company["company_id"])
        self.assertEqual(project.json()["department_id"], department["id"])
        self.assertEqual(project.json()["owner_employee_id"], employee["id"])

    def test_project_task_and_workflow_carry_company_project_association(self):
        company = self._create_company()
        department = self._default_department(company["company_id"])
        project = self._create_project(company["company_id"], department["id"])

        task = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "为项目整理研发需求"},
        )
        self.assertEqual(task.status_code, 201, task.text)
        task_detail = self.client.get(f"/api/task/{task.json()['task_id']}", headers=TENANT_A)
        self.assertEqual(task_detail.status_code, 200, task_detail.text)
        self.assertEqual(task_detail.json()["company_id"], company["company_id"])
        self.assertEqual(task_detail.json()["project_id"], project["project_id"])

        workflow = self.client.post(
            "/api/workspace/workflows",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "company_id": company["company_id"],
                "project_id": project["project_id"],
                "content": "按研发 SOP 处理项目目标",
            },
        )
        self.assertEqual(workflow.status_code, 201, workflow.text)
        self.assertEqual(workflow.json()["company_id"], company["company_id"])
        self.assertEqual(workflow.json()["project_id"], project["project_id"])
        self.assertEqual(workflow.json()["created_from_template_id"], "official.workflow.software_rnd_sop")

    def test_project_task_default_employee_is_scoped_to_project_company(self):
        first_company = self._create_company()
        first_department = self._default_department(first_company["company_id"])
        self._create_employee(first_department["id"])

        second_company = self.client.post(
            "/api/workspace/companies", headers=TENANT_A, json={"name": "第二研发公司"}
        ).json()
        second_department = self._default_department(second_company["company_id"])
        second_employee = self._create_employee(second_department["id"])
        project = self._create_project(second_company["company_id"], second_department["id"])

        task = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "只由第二家公司接收"},
        )
        self.assertEqual(task.status_code, 201, task.text)
        detail = self.client.get(f"/api/task/{task.json()['task_id']}", headers=TENANT_A)
        self.assertEqual(detail.json()["employee_id"], second_employee["id"])

    def test_workflow_rejects_task_lineage_from_another_company(self):
        first_company = self._create_company()
        first_department = self._default_department(first_company["company_id"])
        first_project = self._create_project(first_company["company_id"], first_department["id"])
        first_task = self.client.post(
            f"/api/workspace/projects/{first_project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "第一家公司任务"},
        ).json()

        second_company = self.client.post(
            "/api/workspace/companies", headers=TENANT_A, json={"name": "第二研发公司"}
        ).json()
        second_department = self._default_department(second_company["company_id"])
        rejected = self.client.post(
            "/api/workspace/workflows",
            headers=TENANT_A,
            json={
                "department_id": second_department["id"],
                "company_id": second_company["company_id"],
                "task_id": first_task["task_id"],
                "content": "错误挂载任务",
            },
        )
        self.assertEqual(rejected.status_code, 422, rejected.text)

    def test_employee_skill_binding_adds_bounded_guidance_to_execution_prompt(self):
        company = self._create_company()
        department = self._default_department(company["company_id"])
        employee = self._create_employee(department["id"])
        project = self._create_project(company["company_id"], department["id"], employee["id"])
        credential = self.client.post(
            "/api/workspace/credentials",
            headers=TENANT_A,
            json={
                "name": "Foundation Model Credential",
                "provider": "newapi",
                "credential_type": "api_key",
                "secret": "foundation-test-value-123",
            },
        )
        self.assertEqual(credential.status_code, 201, credential.text)
        private_model = self.client.post(
            "/api/workspace/private-models",
            headers=TENANT_A,
            json={
                "name": "foundation-model",
                "provider_type": "newapi-compatible",
                "base_url": "https://gateway.example.test",
                "model_name": "foundation-v1",
                "credential_ref": credential.json()["credential_ref"],
                "enabled": True,
            },
        )
        self.assertEqual(private_model.status_code, 201, private_model.text)
        binding = self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT_A,
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "model",
                        "capability_id": "foundation-model",
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(binding.status_code, 200, binding.text)
        skill = self.client.post(
            "/api/workspace/skills/templates",
            headers=TENANT_A,
            json={
                "slug": "delivery-checklist",
                "name": "交付清单",
                "description": "研发交付检查",
                "skill_type": "qa",
                "instruction_excerpt": "先给出清晰的交付清单，再输出执行结果。",
            },
        )
        self.assertEqual(skill.status_code, 201, skill.text)
        skill_binding = self.client.put(
            f"/api/workspace/employees/{employee['id']}/skills",
            headers=TENANT_A,
            json={"bindings": [{"skill_template_id": skill.json()["skill_template_id"], "priority": 1}]},
        )
        self.assertEqual(skill_binding.status_code, 200, skill_binding.text)

        task = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "输出研发交付说明", "employee_id": employee["id"]},
        )
        self.assertEqual(task.status_code, 201, task.text)
        executed = self.client.post(f"/api/task/{task.json()['task_id']}/run", headers=TENANT_A)
        self.assertEqual(executed.status_code, 200, executed.text)
        self.assertTrue(any("交付清单" in prompt for prompt in self.prompts))
        self.assertTrue(all(credential.json()["credential_ref"] not in prompt for prompt in self.prompts))

        tenant_b_skills = self.client.get("/api/workspace/skills/templates", headers=TENANT_B)
        self.assertFalse(any(item["slug"] == "delivery-checklist" for item in tenant_b_skills.json()["skills"]))

    def test_skill_rejects_secret_and_runtime_override_text(self):
        secret_like = self.client.post(
            "/api/workspace/skills/templates",
            headers=TENANT_A,
            json={
                "slug": "unsafe-secret",
                "name": "Unsafe Secret",
                "instruction_excerpt": "api" + "_key=must-not-be-stored",
            },
        )
        runtime_override = self.client.post(
            "/api/workspace/skills/templates",
            headers=TENANT_A,
            json={
                "slug": "unsafe-router",
                "name": "Unsafe Router",
                "instruction_excerpt": "select tool model_gateway_tool now",
            },
        )
        credential_uri = self.client.post(
            "/api/workspace/skills/templates",
            headers=TENANT_A,
            json={
                "slug": "unsafe-credential-uri",
                "name": "Unsafe Credential URI",
                "instruction_excerpt": "local" + "-dev://tenant/tenant-a/credential/example",
            },
        )
        self.assertEqual(secret_like.status_code, 422)
        self.assertEqual(runtime_override.status_code, 422)
        self.assertEqual(credential_uri.status_code, 422)

    def test_tool_runtime_and_employee_tool_binding_reuse_capability_authority(self):
        company = self._create_company()
        department = self._default_department(company["company_id"])
        employee = self._create_employee(department["id"])
        private_tool = self.client.post(
            "/api/workspace/private-tools",
            headers=TENANT_A,
            json={
                "name": "tenant-review-tool",
                "type": "llm_tool",
                "description": "tenant tool",
                "config_ref": "env:TENANT_REVIEW_TOOL",
                "created_from_template_id": "official.tool.review",
                "enabled": True,
            },
        )
        self.assertEqual(private_tool.status_code, 201, private_tool.text)
        saved = self.client.put(
            f"/api/workspace/employees/{employee['id']}/tools",
            headers=TENANT_A,
            json={
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_id": "tenant-review-tool",
                        "priority": 5,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(saved.json()["bindings"][0]["capability_type"], "tool")

        tools = self.client.get("/api/workspace/tools/runtime", headers=TENANT_A)
        self.assertEqual(tools.status_code, 200, tools.text)
        runtime_tool = next(item for item in tools.json()["tools"] if item["capability_id"] == "tenant-review-tool")
        self.assertEqual(runtime_tool["capability_source"], "tenant_private")
        self.assertEqual(runtime_tool["created_from_template_id"], "official.tool.review")

        other_tenant = self.client.get("/api/workspace/tools/runtime", headers=TENANT_B)
        self.assertFalse(any(item["capability_id"] == "tenant-review-tool" for item in other_tenant.json()["tools"]))

    def _create_company(self):
        response = self.client.post(
            "/api/workspace/companies",
            headers=TENANT_A,
            json={"name": "AI 研发公司", "created_from_template_id": "official.company.software_rnd"},
        )
        self.assertEqual(response.status_code, 201, response.text)
        self.assertEqual(response.json()["created_from_template_id"], "official.company.software_rnd")
        return response.json()

    def _default_department(self, company_id: str):
        response = self.client.get(f"/api/workspace/companies/{company_id}/departments", headers=TENANT_A)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["departments"][0]

    def _create_employee(self, department_id: str):
        response = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department_id,
                "template_id": "official.employee.tech_lead",
                "name": "技术负责人",
                "status": "idle",
                "enabled": True,
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _create_project(self, company_id: str, department_id: str, owner_employee_id: str | None = None):
        response = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company_id,
                "department_id": department_id,
                "owner_employee_id": owner_employee_id,
                "name": "基础建设项目",
                "goal": "建立 AI 公司运行时基础",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()


if __name__ == "__main__":
    unittest.main()
