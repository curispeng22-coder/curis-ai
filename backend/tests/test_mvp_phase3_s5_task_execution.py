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


class RecordingExecutor:
    def execute(self, prompt: str) -> dict:
        return {"output": "真实执行结果", "cost": 0.25}


class MVPPhase3S5TaskExecutionTests(unittest.TestCase):
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
                tool_functions={"default_tool": RecordingExecutor().execute},
            )
        )
        self.addCleanup(self.client.close)

    def _project_and_employee(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        ).json()
        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "技术负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "name": "MVP 交付",
                "goal": "完成任务执行闭环",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
            },
        ).json()
        return project, employee

    def test_project_task_runs_as_job_and_is_tenant_isolated(self):
        project, employee = self._project_and_employee()
        created = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "汇总项目发布清单", "employee_id": employee["id"]},
        )
        self.assertEqual(created.status_code, 201, created.text)
        task_id = created.json()["task_id"]

        started = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks/{task_id}/jobs",
            headers=TENANT_A,
        )
        self.assertEqual(started.status_code, 202, started.text)
        self.assertEqual(started.json()["job_id"], task_id)
        self.assertEqual(started.json()["status"], "queued")

        job = self.client.get(f"/api/workspace/jobs/{task_id}", headers=TENANT_A)
        self.assertEqual(job.status_code, 200, job.text)
        self.assertEqual(job.json()["status"], "completed")
        self.assertEqual(job.json()["output"], "真实执行结果")
        self.assertEqual(
            job.json()["state_flow"],
            ["INIT", "PENDING", "PARSED", "RUNNING", "COMPLETED"],
        )
        self.assertEqual(len(job.json()["executions"]), 1)
        self.assertEqual(
            self.client.get(f"/api/workspace/jobs/{task_id}", headers=TENANT_B).status_code,
            404,
        )

    def test_frontend_uses_real_task_and_job_apis(self):
        paths = [
            ROOT / "frontend/lib/api.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/page.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js",
            ROOT / "frontend/app/ceo-office/execution/page.js",
            ROOT / "frontend/app/ceo-office/execution/tasks/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("SAMPLE_TASK", source)
        self.assertNotIn("TerraSampleBadge", source)
        for api_name in (
            "createProjectTask",
            "startTaskJob",
            "getTaskJob",
            "getTask",
        ):
            self.assertIn(api_name, source)


if __name__ == "__main__":
    unittest.main()
