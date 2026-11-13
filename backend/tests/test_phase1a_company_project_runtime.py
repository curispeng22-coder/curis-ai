from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class Phase1ACompanyProjectRuntimeTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(create_app(self.db_path, tool_functions={"model_gateway_tool": lambda prompt: {"output": prompt}}))

    def test_company_list_initializes_a_tenant_scoped_default_company(self):
        tenant_a = self.client.get("/api/workspace/companies", headers=TENANT_A)
        tenant_b = self.client.get("/api/workspace/companies", headers=TENANT_B)

        self.assertEqual(tenant_a.status_code, 200, tenant_a.text)
        self.assertEqual(tenant_b.status_code, 200, tenant_b.text)
        company_a = tenant_a.json()["companies"][0]
        company_b = tenant_b.json()["companies"][0]
        self.assertEqual(company_a["name"], "Curis AI Company")
        self.assertTrue(company_a["is_default"])
        self.assertEqual(company_a["tenant_id"], "tenant-a")
        self.assertEqual(company_a["ceo_id"], "ceo-a")
        self.assertNotEqual(company_a["company_id"], company_b["company_id"])

    def test_company_can_be_created_read_and_updated_inside_its_tenant(self):
        created = self.client.post(
            "/api/workspace/companies",
            headers=TENANT_A,
            json={"name": "研发实验室", "description": "负责 AI 产品研发"},
        )
        self.assertEqual(created.status_code, 201, created.text)
        company = created.json()

        fetched = self.client.get(f"/api/workspace/companies/{company['company_id']}", headers=TENANT_A)
        updated = self.client.patch(
            f"/api/workspace/companies/{company['company_id']}",
            headers=TENANT_A,
            json={"description": "研发与交付", "status": "disabled"},
        )

        self.assertEqual(fetched.status_code, 200, fetched.text)
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["description"], "研发与交付")
        self.assertEqual(updated.json()["status"], "disabled")

    def test_company_is_not_visible_outside_its_tenant(self):
        company = self._create_company(TENANT_A)

        response = self.client.get(f"/api/workspace/companies/{company['company_id']}", headers=TENANT_B)

        self.assertEqual(response.status_code, 404)

    def test_project_is_created_under_company_and_updates_its_runtime_metadata(self):
        company = self._create_company(TENANT_A)
        department = self._create_department(company["company_id"], TENANT_A)
        created = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "客户门户重构",
                "goal": "交付新的客户门户",
                "description": "先完成研发方案和最小实现。",
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        project = created.json()

        fetched = self.client.get(f"/api/workspace/projects/{project['project_id']}", headers=TENANT_A)
        updated = self.client.patch(
            f"/api/workspace/projects/{project['project_id']}",
            headers=TENANT_A,
            json={"status": "active", "description": "研发已开始。"},
        )

        self.assertEqual(project["company_id"], company["company_id"])
        self.assertEqual(project["status"], "planned")
        self.assertEqual(project["department_id"], department["id"])
        self.assertEqual(fetched.status_code, 200, fetched.text)
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["status"], "active")
        self.assertEqual(updated.json()["description"], "研发已开始。")

    def test_project_requires_a_company_and_keeps_department_and_tenant_boundaries(self):
        company_a = self._create_company(TENANT_A)
        company_b = self._create_company(TENANT_B)
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "template_id": "official.department.software_rnd",
                "company_id": company_a["company_id"],
                "name": "研发部",
            },
        )
        self.assertEqual(department.status_code, 201, department.text)

        invalid_company = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company_b["company_id"],
                "department_id": department.json()["id"],
                "name": "越权项目",
                "goal": "不应创建",
            },
        )
        invalid_department = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company_a["company_id"],
                "department_id": department.json()["id"],
                "name": "研发项目",
                "goal": "研发目标",
            },
        )
        self.assertEqual(invalid_company.status_code, 404)
        self.assertEqual(invalid_department.status_code, 201, invalid_department.text)

        isolated = self.client.get(
            f"/api/workspace/projects/{invalid_department.json()['project_id']}", headers=TENANT_B
        )
        self.assertEqual(isolated.status_code, 404)

    def test_company_project_runtime_has_no_platform_write_route_dependency(self):
        runtime_source = (Path(__file__).resolve().parents[1] / "app" / "company_project_runtime.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("/api/platform/", runtime_source)

    def _create_company(self, headers):
        response = self.client.post(
            "/api/workspace/companies",
            headers=headers,
            json={"name": "Tenant Company", "description": "测试公司"},
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _create_department(self, company_id, headers):
        response = self.client.post(
            "/api/workspace/departments",
            headers=headers,
            json={
                "template_id": "official.department.software_rnd",
                "company_id": company_id,
                "name": "业务部",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()


if __name__ == "__main__":
    unittest.main()
