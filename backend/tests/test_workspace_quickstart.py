"""Tests for workspace quickstart API — 一步创建 Company → Department → Employee → Project。"""

from __future__ import annotations

import os
import tempfile
import unittest

from fastapi.testclient import TestClient

from app.main import create_app

TENANT_SELFUSE = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": "ceo-selfuse"}


class WorkspaceQuickstartTests(unittest.TestCase):
    """覆盖正常创建路径和参数校验边界。"""

    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(
            create_app(
                self.db_path,
                tool_functions={"model_gateway_tool": lambda prompt: {"output": prompt}},
            )
        )

    def test_quickstart_creates_full_chain_with_defaults(self):
        """使用默认参数调用 quickstart，验证全链路创建成功。"""
        resp = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={},
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        data = resp.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("company_id", data)
        self.assertIn("department_id", data)
        self.assertIn("employee_id", data)
        self.assertIn("project_id", data)
        self.assertTrue(data["company_id"].startswith("company-"))
        self.assertTrue(data["department_id"].startswith("dept-"))
        self.assertTrue(data["employee_id"].startswith("emp-"))
        self.assertTrue(data["project_id"].startswith("project-"))

        # 验证各资源可独立查询
        company = self.client.get(
            f"/api/workspace/companies/{data['company_id']}",
            headers=TENANT_SELFUSE,
        )
        self.assertEqual(company.status_code, 200)
        self.assertEqual(company.json()["company_id"], data["company_id"])

        project = self.client.get(
            f"/api/workspace/projects/{data['project_id']}",
            headers=TENANT_SELFUSE,
        )
        self.assertEqual(project.status_code, 200)
        self.assertEqual(project.json()["project_id"], data["project_id"])

    def test_quickstart_with_custom_params(self):
        """传自定义参数验证取值正确。"""
        resp = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={
                "company_name": "测试公司",
                "department_name": "研发部",
                "employee_name": "AI工程师",
                "project_name": "测试项目",
                "project_description": "这是一个测试项目",
            },
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        data = resp.json()
        self.assertEqual(data["status"], "ok")

        # 验证项目描述
        project = self.client.get(
            f"/api/workspace/projects/{data['project_id']}",
            headers=TENANT_SELFUSE,
        )
        self.assertEqual(project.status_code, 200)
        self.assertEqual(project.json()["name"], "测试项目")
        self.assertEqual(project.json()["description"], "这是一个测试项目")

    def test_quickstart_employee_has_skills_and_tools(self):
        """验证员工被正确分配 skills 和 tools。"""
        resp = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={},
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        employee_id = resp.json()["employee_id"]

        # 检查 skills
        skills_resp = self.client.get(
            f"/api/workspace/employees/{employee_id}/skills",
            headers=TENANT_SELFUSE,
        )
        self.assertEqual(skills_resp.status_code, 200)
        skills = skills_resp.json()["bindings"]
        self.assertGreater(len(skills), 0, "employee should have at least one skill")

        # 检查 tools
        tools_resp = self.client.get(
            f"/api/workspace/employees/{employee_id}/tools",
            headers=TENANT_SELFUSE,
        )
        self.assertEqual(tools_resp.status_code, 200)
        tools = tools_resp.json()["bindings"]
        self.assertGreater(len(tools), 0, "employee should have at least one tool")

    def test_quickstart_validates_employee_template(self):
        """传一个不存在的 employee_template_id 应返回 422。"""
        resp = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={"employee_template_id": "et_does_not_exist"},
        )
        self.assertEqual(resp.status_code, 422, resp.text)

    def test_quickstart_is_idempotent_for_company(self):
        """多次调用应返回同一 company_id（复用首个存在的公司）。"""
        resp1 = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={},
        )
        self.assertEqual(resp1.status_code, 200, resp1.text)

        resp2 = self.client.post(
            "/api/workspace/quickstart",
            headers=TENANT_SELFUSE,
            json={},
        )
        self.assertEqual(resp2.status_code, 200, resp2.text)

        data1 = resp1.json()
        data2 = resp2.json()
        self.assertEqual(data1["company_id"], data2["company_id"],
                         "company_id should be reused")
        # departments, employees, projects should be different (new ones each call)
        self.assertNotEqual(data1["department_id"], data2["department_id"])
        self.assertNotEqual(data1["project_id"], data2["project_id"])
