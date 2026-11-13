from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class MVPPhase1S2WorkspaceTests(unittest.TestCase):
    def setUp(self):
        identity_env = patch.dict(os.environ, {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"})
        identity_env.start()
        self.addCleanup(identity_env.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)

    def test_company_department_and_home_summary_use_tenant_scoped_facts(self):
        company = self.client.get("/api/workspace/companies", headers=TENANT_A).json()["companies"][0]
        updated = self.client.patch(
            f"/api/workspace/companies/{company['company_id']}",
            headers=TENANT_A,
            json={"name": "云帆智能", "description": "AI 产品交付"},
        )
        self.assertEqual(updated.status_code, 200, updated.text)

        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
                "mission": "交付 AI 产品",
            },
        )
        self.assertEqual(department.status_code, 201, department.text)
        department_id = department.json()["id"]

        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department_id,
                "name": "Curis MVP",
                "goal": "完成核心闭环",
                "status": "active",
            },
        )
        self.assertEqual(project.status_code, 201, project.text)

        task_id = self.client.post(
            f"/api/workspace/projects/{project.json()['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "生成发布稿"},
        ).json()["task_id"]
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                insert into artifacts (
                  artifact_id, tenant_id, task_id, title, artifact_type,
                  status, content, source_ref, content_sha256
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "artifact_1",
                    "tenant-a",
                    task_id,
                    "发布稿",
                    "copywriting",
                    "generated",
                    "真实发布稿",
                    "test",
                    "test-sha256",
                ),
            )

        summary = self.client.get("/api/workspace/home/summary", headers=TENANT_A)
        self.assertEqual(summary.status_code, 200, summary.text)
        payload = summary.json()
        self.assertEqual(payload["company"]["name"], "云帆智能")
        self.assertEqual(payload["counts"], {"departments": 1, "projects": 1, "employees": 0})
        self.assertEqual(payload["departments"][0]["project_count"], 1)
        self.assertEqual(payload["projects"][0]["name"], "Curis MVP")
        self.assertEqual(payload["recent_artifacts"][0]["title"], "发布稿")

        isolated = self.client.get("/api/workspace/home/summary", headers=TENANT_B).json()
        self.assertNotEqual(isolated["company"]["company_id"], company["company_id"])
        self.assertEqual(isolated["counts"], {"departments": 0, "projects": 0, "employees": 0})

    def test_department_can_be_updated_and_active_employee_blocks_delete(self):
        company = self.client.get("/api/workspace/companies", headers=TENANT_A).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "交付部",
            },
        ).json()
        updated = self.client.patch(
            f"/api/workspace/departments/{department['id']}",
            headers=TENANT_A,
            json={"mission": "负责客户交付", "status": "active"},
        )
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["mission"], "负责客户交付")

        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "交付负责人",
            },
        )
        self.assertEqual(employee.status_code, 201, employee.text)

        response = self.client.delete(f"/api/workspace/departments/{department['id']}", headers=TENANT_A)

        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
