from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class BusinessDepartmentOrgModelTests(unittest.TestCase):
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
        self.client = TestClient(
            create_app(
                self.db_path,
                tool_functions={"default_tool": lambda _prompt: {"output": "已交付成果", "cost": 0}},
            )
        )
        self.addCleanup(self.client.close)

    def _organization(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "小红书业务部",
                "mission": "创造内容增长价值",
            },
        ).json()
        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "内容负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        return company, department, employee

    def test_project_requires_business_department_and_artifact_belongs_to_task(self):
        company, department, employee = self._organization()
        missing_department = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "name": "缺少归属的项目",
                "goal": "必须被拒绝",
            },
        )
        self.assertEqual(missing_department.status_code, 422)

        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "小红书增长",
                "goal": "产出真实内容成果",
            },
        ).json()
        task_id = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "生成首篇内容", "employee_id": employee["id"]},
        ).json()["task_id"]
        started = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks/{task_id}/jobs",
            headers=TENANT_A,
        )
        self.assertEqual(started.status_code, 202, started.text)

        task_artifacts = self.client.get(
            f"/api/workspace/tasks/{task_id}/artifacts", headers=TENANT_A
        )
        self.assertEqual(task_artifacts.status_code, 200, task_artifacts.text)
        artifact = task_artifacts.json()["artifacts"][0]
        self.assertEqual(artifact["task_id"], task_id)
        self.assertEqual(artifact["content"], "已交付成果")

        project_artifacts = self.client.get(
            f"/api/workspace/projects/{project['project_id']}/artifacts",
            headers=TENANT_A,
        )
        self.assertEqual(
            [item["artifact_id"] for item in project_artifacts.json()["artifacts"]],
            [artifact["artifact_id"]],
        )
        self.assertEqual(
            self.client.get(
                f"/api/workspace/tasks/{task_id}/artifacts", headers=TENANT_B
            ).status_code,
            404,
        )

    def test_legacy_project_without_department_is_migrated_idempotently(self):
        company, department, employee = self._organization()
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "历史项目",
                "goal": "保留历史数据",
            },
        ).json()
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "update projects set department_id = null where project_id = ?",
                (project["project_id"],),
            )

        Database(self.db_path).initialize()
        Database(self.db_path).initialize()

        with sqlite3.connect(self.db_path) as connection:
            migrated = connection.execute(
                "select department_id from projects where project_id = ?",
                (project["project_id"],),
            ).fetchone()[0]
            department_rows = connection.execute(
                """
                select id from department_instances
                where tenant_id = 'tenant-a' and company_id = ?
                  and name = '待归属业务部'
                """,
                (company["company_id"],),
            ).fetchall()
        self.assertTrue(migrated)
        self.assertEqual(len(department_rows), 1)
        self.assertEqual(migrated, department_rows[0][0])

    def test_completed_legacy_task_output_becomes_one_traceable_artifact(self):
        company, department, employee = self._organization()
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "迁移成果项目",
                "goal": "保留已完成任务成果",
            },
        ).json()
        task_id = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "历史成功任务", "employee_id": employee["id"]},
        ).json()["task_id"]
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "update tasks set status = 'COMPLETED', output = '历史真实结果' where task_id = ?",
                (task_id,),
            )

        Database(self.db_path).initialize()
        Database(self.db_path).initialize()

        response = self.client.get(
            f"/api/workspace/tasks/{task_id}/artifacts", headers=TENANT_A
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(len(response.json()["artifacts"]), 1)
        self.assertEqual(response.json()["artifacts"][0]["content"], "历史真实结果")


if __name__ == "__main__":
    unittest.main()
