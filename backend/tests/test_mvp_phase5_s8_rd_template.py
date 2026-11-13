from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-s8", "X-Ceo-Id": "ceo-s8"}

# Legacy RD business chain frozen out of V1 scope (CEO decision 2026-10-07).
_SKIP_LEGACY_RD = unittest.skip(
    "Legacy RD/XHS/TTK business_type chain frozen out of V1 "
    "(CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007, CEO decision 2026-10-07)"
)


class DevelopmentModel:
    gateway_id = "test-gateway"
    model_name = "test-coder"

    def __init__(self, output: str):
        self.output = output

    def runtime_config_is_declared(self):
        return True

    def validate_runtime_config(self):
        return None

    def execute(self, _prompt):
        return {
            "output": self.output,
            "cost": 0.0042,
            "estimated_cost": 0.0042,
            "model_gateway_id": "test-gateway",
            "provider_id": "test-gateway",
            "model_name": "test-coder",
            "prompt_tokens": 6,
            "completion_tokens": 4,
            "total_tokens": 10,
            "currency": "USD",
            "cost_source": "model_gateway_adapter",
            "ledger_cost_source": "estimated",
            "price_version": "test-v1",
            "unit_price_input": 0.0003,
            "unit_price_output": 0.0006,
            "metering_status": "confirmed",
            "status": "success",
            "outbound_attempted": True,
        }


class MVPPhase5S8RDTemplateTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-s8-workspace-")
        self.addCleanup(self.workspace.cleanup)
        self.workspace_path = Path(self.workspace.name)
        target = self.workspace_path / "backend/app/sample.py"
        test_file = self.workspace_path / "backend/tests/test_sample.py"
        python_bin = self.workspace_path / "backend/.venv/bin/python"
        target.parent.mkdir(parents=True)
        test_file.parent.mkdir(parents=True)
        python_bin.parent.mkdir(parents=True)
        target.write_text("VALUE = 1\n", encoding="utf-8")
        test_file.write_text(
            "from pathlib import Path\n\n"
            "def test_value():\n"
            "    assert 'VALUE = 2' in Path('backend/app/sample.py').read_text()\n",
            encoding="utf-8",
        )
        python_bin.write_text(
            f"#!/bin/sh\nexec '{ROOT / 'backend/.venv/bin/python'}' \"$@\"\n",
            encoding="utf-8",
        )
        python_bin.chmod(0o755)
        subprocess.run(["git", "init", "-q"], cwd=self.workspace_path, check=True)
        subprocess.run(
            ["git", "config", "user.email", "s8@example.invalid"],
            cwd=self.workspace_path,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "S8 Test"],
            cwd=self.workspace_path,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=self.workspace_path, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.workspace_path, check=True)

        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.env = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_D1_EXECUTE_ENABLED": "true",
                "CURIS_D1_FROZEN": "false",
                "CURIS_D1_WORKSPACE_ROOT": str(self.workspace_path),
                "CURIS_RD_SANDBOX": "off",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        self.root_override = patch("app.local_rd_toolset._WORKSPACE_ROOT_OVERRIDE", None)
        self.root_override.start()
        self.addCleanup(self.root_override.stop)

    def _client(self, output: str) -> TestClient:
        client = TestClient(create_app(self.db_path, model_gateway_adapter=DevelopmentModel(output)))
        self.addCleanup(client.close)
        return client

    def _task(self, client: TestClient):
        company = client.get("/api/workspace/companies", headers=HEADERS).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=HEADERS,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "研发负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        model = client.post(
            "/api/workspace/capabilities/registry",
            headers=HEADERS,
            json={
                "capability_key": "model.s8-coder",
                "type": "model",
                "name": "S8 Coder",
                "provider_id": "test-gateway",
                "model_name": "test-coder",
            },
        )
        self.assertEqual(model.status_code, 201, model.text)
        bound = client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [{
                    "capability_source": "official",
                    "capability_type": "model",
                    "capability_id": "model.s8-coder",
                    "enabled": True,
                }]
            },
        )
        self.assertEqual(bound.status_code, 200, bound.text)
        project = client.post(
            "/api/workspace/projects",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "name": "S8 研发项目",
                "goal": "跑通代码成果闭环",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "status": "active",
            },
        ).json()
        created = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=HEADERS,
            json={
                "content": "把 sample.py 的 VALUE 从 1 改为 2",
                "employee_id": employee["id"],
                "capability_source": "official",
                "capability_type": "model",
                "capability_id": "model.s8-coder",
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        return project, created.json()["task_id"]

    @_SKIP_LEGACY_RD
    def test_real_development_task_writes_tests_and_records_git_diff(self):
        diff = (
            "--- a/backend/app/sample.py\n"
            "+++ b/backend/app/sample.py\n"
            "@@ -1 +1 @@\n"
            "-VALUE = 1\n"
            "+VALUE = 2\n"
        )
        client = self._client(diff)
        project, task_id = self._task(client)
        response = client.post(
            "/api/workspace/rd-workflow/run",
            headers=HEADERS,
            json={
                "project_id": project["project_id"],
                "task_id": task_id,
                "target_files": ["backend/app/sample.py"],
                "test_file": "backend/tests/test_sample.py",
                "max_rounds": 1,
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        run = response.json()
        result = run["development_result"]
        self.assertEqual(run["status"], "completed")
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["test_exit_code"], 0)
        self.assertIn("+VALUE = 2", result["diff_text"])
        self.assertEqual(result["total_tokens"], 10)
        self.assertEqual(result["estimated_cost"], 0.0042)
        self.assertEqual(
            (self.workspace_path / "backend/app/sample.py").read_text(encoding="utf-8"),
            "VALUE = 2\n",
        )
        stored_run = client.get(
            f"/api/workspace/workflows/{run['workflow_run_id']}",
            headers=HEADERS,
        ).json()
        self.assertEqual(stored_run["project_id"], project["project_id"])
        self.assertEqual(stored_run["task_id"], task_id)
        self.assertEqual(len(stored_run["steps"]), 6)
        task = client.get(f"/api/task/{task_id}", headers=HEADERS).json()
        self.assertEqual(task["status"], "COMPLETED")
        self.assertEqual(task["selected_tool"], "real_rd_executor")

    @_SKIP_LEGACY_RD
    def test_failed_model_output_marks_workflow_and_task_failed(self):
        client = self._client("not a unified diff")
        project, task_id = self._task(client)
        response = client.post(
            "/api/workspace/rd-workflow/run",
            headers=HEADERS,
            json={
                "project_id": project["project_id"],
                "task_id": task_id,
                "target_files": ["backend/app/sample.py"],
                "test_file": "backend/tests/test_sample.py",
                "max_rounds": 1,
            },
        )
        self.assertEqual(response.status_code, 422, response.text)
        self.assertEqual(response.json()["detail"], "real_rd_failed")
        task = client.get(f"/api/task/{task_id}", headers=HEADERS).json()
        self.assertEqual(task["status"], "FAILED")
        runs = client.get("/api/workspace/workflows", headers=HEADERS).json()["workflow_runs"]
        self.assertEqual(runs[0]["status"], "failed")

    def test_execution_gate_is_fail_closed(self):
        with patch.dict(os.environ, {"CURIS_D1_EXECUTE_ENABLED": "false"}):
            db_file = tempfile.NamedTemporaryFile(delete=False)
            db_path = db_file.name
            db_file.close()
            self.addCleanup(lambda: os.path.exists(db_path) and os.unlink(db_path))
            client = TestClient(
                create_app(db_path, model_gateway_adapter=DevelopmentModel("unused"))
            )
            self.addCleanup(client.close)
            response = client.post(
                "/api/workspace/rd-workflow/run",
                headers=HEADERS,
                json={
                    "project_id": "project-none",
                    "task_id": "task-none",
                    "target_files": ["backend/app/sample.py"],
                    "test_file": "backend/tests/test_sample.py",
                },
            )
        self.assertEqual(response.status_code, 503, response.text)

    def test_frontend_uses_real_development_run_api(self):
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                ROOT / "frontend/lib/development.js",
                ROOT / "frontend/app/ceo-office/projects/[id]/DevelopmentRunDrawer.js",
                ROOT / "frontend/app/ceo-office/execution/runs/[id]/page.js",
            )
        )
        for value in (
            "/api/workspace/rd-workflow/run",
            "getWorkflowRun",
            "developmentResult.diff_text",
            "test_exit_code",
            "远程提交、分支与 PR 未执行",
        ):
            self.assertIn(value, source)


if __name__ == "__main__":
    unittest.main()
