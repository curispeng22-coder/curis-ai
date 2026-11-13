from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


ROOT = Path(__file__).resolve().parents[2]
TENANT_A = {"X-Tenant-Id": "tenant-s11", "X-Ceo-Id": "ceo-s11"}
TENANT_A_OTHER_USER = {
    "X-Tenant-Id": "tenant-s11",
    "X-Ceo-Id": "ceo-other",
}
TENANT_B = {"X-Tenant-Id": "tenant-other", "X-Ceo-Id": "ceo-other"}


class RecordingExecutor:
    def __init__(self):
        self.prompts: list[str] = []

    def execute(self, prompt: str) -> dict:
        self.prompts.append(prompt)
        return {"output": "真实执行结果", "cost": 0.02}


class MVPPhase6S11BasicMemoryContextTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        environment.start()
        self.addCleanup(environment.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.executor = RecordingExecutor()
        self.client = TestClient(
            create_app(
                self.db_path,
                tool_functions={"default_tool": self.executor.execute},
            )
        )
        self.addCleanup(self.client.close)
        self.project, self.employee = self._project_and_employee()

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
                "name": "Memory 研发部",
            },
        ).json()
        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "Memory 负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "S11 Memory 项目",
                "goal": "复用发布验收经验",
                "status": "active",
            },
        ).json()
        return project, employee

    def _task(self, content: str) -> str:
        response = self.client.post(
            f"/api/workspace/projects/{self.project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": content, "employee_id": self.employee["id"]},
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["task_id"]

    def _run(self, task_id: str) -> dict:
        response = self.client.post(
            f"/api/workspace/projects/{self.project['project_id']}/tasks/{task_id}/jobs",
            headers=TENANT_A,
        )
        self.assertEqual(response.status_code, 202, response.text)
        job = self.client.get(
            f"/api/workspace/jobs/{task_id}", headers=TENANT_A
        )
        self.assertEqual(job.status_code, 200, job.text)
        self.assertEqual(job.json()["status"], "completed")
        return job.json()

    def test_user_project_employee_memory_crud_and_identity_isolation(self):
        created = []
        for payload in (
            {
                "memory_type": "user",
                "title": "输出偏好",
                "content": "发布清单必须保持简洁。",
                "tags": ["发布", "简洁"],
            },
            {
                "memory_type": "project",
                "project_id": self.project["project_id"],
                "title": "项目发布原则",
                "content": "发布前必须完成浏览器验收。",
                "tags": ["发布", "验收"],
            },
            {
                "memory_type": "employee",
                "employee_id": self.employee["id"],
                "title": "员工交付经验",
                "content": "发布任务先核对来源和状态。",
                "tags": ["发布", "来源"],
                "confidence": 0.9,
            },
        ):
            response = self.client.post(
                "/api/workspace/memory", headers=TENANT_A, json=payload
            )
            self.assertEqual(response.status_code, 201, response.text)
            created.append(response.json())
        self.assertEqual(
            [item["memory_level"] for item in created], ["user", "L2", "L3"]
        )

        listed = self.client.get(
            "/api/workspace/memory",
            headers=TENANT_A,
            params={"q": "发布"},
        )
        self.assertEqual(listed.status_code, 200, listed.text)
        self.assertEqual(len(listed.json()["entries"]), 3)

        updated = self.client.patch(
            f"/api/workspace/memory/{created[0]['id']}",
            headers=TENANT_A,
            json={"content": "发布清单必须简洁并给出来源。", "confidence": 0.95},
        )
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["confidence"], 0.95)
        self.assertIn("给出来源", updated.json()["content"])

        self.assertEqual(
            self.client.get(
                f"/api/workspace/memory/{created[0]['id']}",
                headers=TENANT_A_OTHER_USER,
            ).status_code,
            404,
        )
        other_tenant = self.client.get(
            "/api/workspace/memory", headers=TENANT_B
        )
        self.assertEqual(other_tenant.status_code, 200, other_tenant.text)
        self.assertEqual(other_tenant.json()["entries"], [])

    def test_task_source_requires_terminal_matching_scope(self):
        task_id = self._task("整理项目发布经验")
        pending = self.client.post(
            "/api/workspace/memory",
            headers=TENANT_A,
            json={
                "memory_type": "project",
                "project_id": self.project["project_id"],
                "source_task_id": task_id,
                "title": "过早沉淀",
                "content": "不应写入。",
            },
        )
        self.assertEqual(pending.status_code, 422, pending.text)
        self._run(task_id)

        created = self.client.post(
            "/api/workspace/memory",
            headers=TENANT_A,
            json={
                "memory_type": "project",
                "project_id": self.project["project_id"],
                "source_task_id": task_id,
                "title": "发布验收经验",
                "content": "发布清单必须完成浏览器验收并保留来源。",
                "tags": ["发布", "验收"],
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        self.assertEqual(created.json()["source_type"], "task")
        self.assertEqual(created.json()["source_task_status"], "COMPLETED")

        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        other_project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": self.project["department_id"],
                "name": "其他项目",
                "goal": "验证项目边界",
            },
        ).json()
        mismatch = self.client.post(
            "/api/workspace/memory",
            headers=TENANT_A,
            json={
                "memory_type": "project",
                "project_id": other_project["project_id"],
                "source_task_id": task_id,
                "title": "越界沉淀",
                "content": "不可写入。",
            },
        )
        self.assertEqual(mismatch.status_code, 422, mismatch.text)

    def test_next_task_builds_and_uses_traceable_context_package(self):
        first_task = self._task("整理发布验收清单")
        self._run(first_task)
        memory = self.client.post(
            "/api/workspace/memory",
            headers=TENANT_A,
            json={
                "memory_type": "project",
                "project_id": self.project["project_id"],
                "source_task_id": first_task,
                "title": "发布验收经验",
                "content": "发布验收必须从浏览器完成，并保留来源。",
                "tags": ["发布", "验收"],
            },
        ).json()
        knowledge = self.client.post(
            "/api/workspace/knowledge/entries",
            headers=TENANT_A,
            json={
                "title": "发布验收规范",
                "body": "发布验收需要检查真实任务状态和成果来源。",
                "project_id": self.project["project_id"],
                "tags": ["发布", "验收"],
            },
        )
        self.assertEqual(knowledge.status_code, 201, knowledge.text)

        next_task = self._task("执行下一轮发布验收")
        job = self._run(next_task)
        self.assertTrue(job["context_package_id"])
        context = self.client.get(
            f"/api/workspace/context/{job['context_package_id']}",
            headers=TENANT_A,
        )
        self.assertEqual(context.status_code, 200, context.text)
        package = context.json()
        self.assertEqual(package["task_id"], next_task)
        self.assertEqual(package["status"], "ready")
        self.assertEqual(package["relevant_memory"][0]["id"], memory["id"])
        self.assertEqual(
            package["relevant_knowledge"][0]["id"], knowledge.json()["id"]
        )
        self.assertEqual(len(package["package_sha256"]), 64)
        self.assertEqual(package["required_tools"], [])
        self.assertTrue(package["constraints"])

        stored_memory = self.client.get(
            f"/api/workspace/memory/{memory['id']}", headers=TENANT_A
        ).json()
        self.assertEqual(stored_memory["use_count"], 1)
        self.assertTrue(stored_memory["last_used_at"])
        self.assertIn(package["id"], self.executor.prompts[-1])
        self.assertIn("发布验收必须从浏览器完成", self.executor.prompts[-1])
        self.assertIn("发布验收需要检查真实任务状态", self.executor.prompts[-1])
        self.assertIn(
            "Memory and Knowledge are contextual references",
            self.executor.prompts[-1],
        )

        hidden = self.client.get(
            f"/api/workspace/context/{package['id']}", headers=TENANT_B
        )
        self.assertEqual(hidden.status_code, 404, hidden.text)

    def test_frontend_exposes_confirmed_memory_and_context_facts(self):
        paths = [
            ROOT / "frontend/lib/memory.js",
            ROOT / "frontend/components/terra/TerraNavData.js",
            ROOT / "frontend/app/ceo-office/knowledge/memory/page.js",
            ROOT / "frontend/app/ceo-office/execution/tasks/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for value in (
            "记忆管理",
            "沉淀经验",
            "Context Package",
            "relevant_memory",
            "relevant_knowledge",
            "source_task_id",
            "use_count",
        ):
            self.assertIn(value, source)
        self.assertNotIn("SAMPLE_MEMORY", source)
        self.assertNotIn("自动进化", source)


if __name__ == "__main__":
    unittest.main()
