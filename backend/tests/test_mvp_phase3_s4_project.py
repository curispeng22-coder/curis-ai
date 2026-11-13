from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}
ROOT = Path(__file__).resolve().parents[2]


class MVPPhase3S4ProjectTests(unittest.TestCase):
    def setUp(self):
        identity_env = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        identity_env.start()
        self.addCleanup(identity_env.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)

    def test_create_project_with_owner_and_isolate_tenant(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department_response = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        )
        self.assertEqual(department_response.status_code, 201, department_response.text)
        department = department_response.json()

        employee_response = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "技术负责人",
                "instructions_override": "负责项目目标和交付质量。",
                "status": "idle",
                "enabled": True,
            },
        )
        self.assertEqual(employee_response.status_code, 201, employee_response.text)
        employee = employee_response.json()

        project_response = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "name": "Curis MVP 交付",
                "goal": "完成可由用户在浏览器操作的 MVP 闭环。",
                "description": "保持 Curis v1.0 架构。",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "status": "planned",
            },
        )
        self.assertEqual(project_response.status_code, 201, project_response.text)
        project = project_response.json()
        self.assertEqual(project["goal"], "完成可由用户在浏览器操作的 MVP 闭环。")
        self.assertEqual(project["department_id"], department["id"])
        self.assertEqual(project["owner_employee_id"], employee["id"])
        self.assertEqual(project["status"], "planned")

        detail = self.client.get(
            f"/api/workspace/projects/{project['project_id']}", headers=TENANT_A
        )
        self.assertEqual(detail.status_code, 200, detail.text)
        tenant_a_projects = self.client.get(
            "/api/workspace/projects", headers=TENANT_A
        ).json()["projects"]
        tenant_b_projects = self.client.get(
            "/api/workspace/projects", headers=TENANT_B
        ).json()["projects"]
        self.assertEqual([item["project_id"] for item in tenant_a_projects], [project["project_id"]])
        self.assertEqual(tenant_b_projects, [])

    def test_project_pages_use_real_api_and_truthful_containers(self):
        paths = [
            ROOT / "frontend/app/ceo-office/projects/page.js",
            ROOT / "frontend/app/ceo-office/projects/ProjectFormDrawer.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("SAMPLE_PROJECT", source)
        self.assertNotIn("草稿已生成（本地）", source)
        self.assertNotIn("proj.progress ||", source)
        self.assertIn("createProject", source)
        self.assertIn("getProject", source)
        self.assertIn("getTasks", source)
        for label in ("概览", "任务", "资料", "成果", "数据"):
            self.assertIn(label, source)


if __name__ == "__main__":
    unittest.main()
