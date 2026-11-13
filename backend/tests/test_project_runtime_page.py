from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.issue_pipeline import IssueQueue, NLParser, ResultReviewer
import app.issue_pipeline_api as pipeline_api
from app.main import create_app
from app.pipeline_runtime import NodeResult, PipelineRuntime
from app.scheduler import scheduler_manager
from app.task_graph import TaskGraph, TaskNode


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class _SuccessfulRuntime:
    def run_node(self, node, graph):
        node.status = "done"
        node.result = {
            "status": "success",
            "output": "--- a/example.py\n+++ b/example.py\n@@ -1 +1 @@\n-old\n+new",
            "files": ["example.py"],
        }
        node.trace.append({"step": node.id, "tool": "local-test", "status": "success"})
        return NodeResult(node_id=node.id, status="done", output=node.result)


class _ArtifactRuntime:
    def run_node(self, node, graph):
        node.status = "done"
        node.attempts = 1
        node.result = {"status": "success", "output": "4 passed"}
        node.trace.append({"step": node.id, "tool": "local.project_runtime.focused", "status": "success"})
        return NodeResult(node_id=node.id, status="done", output=node.result)


class _SuccessfulToolResolver:
    def resolve(self, requirement, exclude_keys=None, employee_id=None):
        class _Adapter:
            def execute(self, prompt):
                return {"status": "success", "output": "focused check passed"}

        return pipeline_api.CapabilityHandle(
            key="local.project_runtime.focused", type="tool", adapter=_Adapter()
        )


class ProjectRuntimePageTests(unittest.TestCase):
    def setUp(self):
        self.db_path = self._temp_path()
        self.queue_path = self._temp_path()
        pipeline_api._queue = IssueQueue(self.queue_path)
        pipeline_api._parser = NLParser()
        pipeline_api._dispatcher = None
        pipeline_api._graph_registry.clear()
        pipeline_api._graph_project_registry.clear()
        pipeline_api._graph_task_registry.clear()
        pipeline_api._build_runtime_fn = None
        self.client = TestClient(
            create_app(
                self.db_path,
                tool_functions={"model_gateway_tool": lambda prompt: {"output": prompt}},
            )
        )
        self.project = self._create_project(TENANT_A)

    def tearDown(self):
        scheduler_manager.stop_all(reason="test_teardown")
        pipeline_api._build_runtime_fn = None
        pipeline_api._queue = None
        pipeline_api._parser = None
        pipeline_api._dispatcher = None
        for base in (self.db_path, self.queue_path):
            for path in (base, f"{base}-wal", f"{base}-shm"):
                if os.path.exists(path):
                    os.unlink(path)

    @staticmethod
    def _temp_path():
        handle = tempfile.NamedTemporaryFile(delete=False)
        path = handle.name
        handle.close()
        return path

    def _create_project(self, headers):
        company = self.client.post(
            "/api/workspace/companies",
            headers=headers,
            json={"name": "Runtime Company"},
        ).json()
        department = self.client.post(
            "/api/workspace/departments",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "Runtime 业务部",
            },
        ).json()
        response = self.client.post(
            "/api/workspace/projects",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "Project Runtime",
                "goal": "交付项目运行页",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def _submit(self):
        response = self.client.post(
            "/api/pipeline/submit",
            headers=TENANT_A,
            json={
                "project_id": self.project["project_id"],
                "natural_language": "实现项目页面，然后运行测试",
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_project_submit_persists_scoped_runtime_snapshot(self):
        submitted = self._submit()

        response = self.client.get(
            f"/api/pipeline/project/{self.project['project_id']}",
            headers=TENANT_A,
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload["project"]["project_id"], self.project["project_id"])
        self.assertEqual(payload["runtime"]["task"]["id"], submitted["id"])
        self.assertEqual(payload["runtime"]["task"]["issue_spec"]["tenant_id"], "tenant-a")
        self.assertTrue(payload["runtime"]["graph"]["available"])
        self.assertEqual(payload["runtime"]["available_actions"], ["auto_run"])

        project = self.client.get(
            f"/api/workspace/projects/{self.project['project_id']}", headers=TENANT_A
        ).json()
        snapshot = json.loads(project["progress_json"])["runtime"]
        self.assertEqual(snapshot["task_id"], submitted["id"])
        self.assertEqual(snapshot["graph_id"], submitted["graph_id"])

        isolated = self.client.get(
            f"/api/pipeline/project/{self.project['project_id']}", headers=TENANT_B
        )
        self.assertEqual(isolated.status_code, 404)
        isolated_graph = self.client.get(
            f"/api/pipeline/{submitted['graph_id']}/graph", headers=TENANT_B
        )
        isolated_task = self.client.get(
            f"/api/pipeline/{submitted['id']}", headers=TENANT_B
        )
        self.assertEqual(isolated_graph.status_code, 404)
        self.assertEqual(isolated_task.status_code, 404)

        duplicate = self.client.post(
            "/api/pipeline/submit",
            headers=TENANT_A,
            json={
                "project_id": self.project["project_id"],
                "natural_language": "创建第二条冲突运行",
            },
        )
        self.assertEqual(duplicate.status_code, 409)

    def test_terminal_task_allows_a_new_goal_and_returns_the_new_runtime(self):
        first = self._submit()
        pipeline_api._get_queue().update_status(
            first["id"],
            status="failed",
            executor_result={"status": "failed", "rounds": 1, "test_exit_code": 1, "files": []},
        )

        response = self.client.post(
            "/api/pipeline/submit",
            headers=TENANT_A,
            json={
                "project_id": self.project["project_id"],
                "natural_language": "运行下一次检查",
            },
        )

        self.assertEqual(response.status_code, 200, response.text)
        second = response.json()
        self.assertNotEqual(second["id"], first["id"])
        payload = self.client.get(
            f"/api/pipeline/project/{self.project['project_id']}",
            headers=TENANT_A,
        ).json()
        self.assertEqual(payload["runtime"]["task"]["id"], second["id"])
        self.assertEqual(payload["runtime"]["task"]["natural_language"], "运行下一次检查")

    def test_refresh_reports_process_state_loss_without_faking_progress(self):
        self._submit()
        pipeline_api._graph_registry.clear()

        payload = self.client.get(
            f"/api/pipeline/project/{self.project['project_id']}", headers=TENANT_A
        ).json()

        self.assertFalse(payload["runtime"]["graph"]["available"])
        self.assertIsNone(payload["runtime"]["graph"]["progress"])
        self.assertTrue(all(node["status"] == "unknown" for node in payload["runtime"]["graph"]["nodes"]))
        self.assertEqual(payload["runtime"]["available_actions"], [])
        self.assertEqual(payload["runtime"]["blocked_reason"], "pipeline_process_state_unavailable")

    def test_auto_run_updates_task_for_review_and_decision(self):
        pipeline_api._build_runtime_fn = lambda graph: _SuccessfulRuntime()
        submitted = self._submit()

        started = self.client.post(
            f"/api/pipeline/{submitted['graph_id']}/auto-run", headers=TENANT_A
        )
        self.assertEqual(started.status_code, 200, started.text)
        payload = None
        for _ in range(100):
            payload = self.client.get(
                f"/api/pipeline/project/{self.project['project_id']}", headers=TENANT_A
            ).json()
            if payload["runtime"]["task"]["status"] == "review":
                break
            time.sleep(0.02)

        self.assertEqual(payload["runtime"]["task"]["status"], "review")
        self.assertTrue(payload["runtime"]["graph"]["is_complete"])
        self.assertTrue(all(node["status"] == "done" for node in payload["runtime"]["graph"]["nodes"]))
        self.assertEqual(
            payload["runtime"]["available_actions"],
            ["approve", "reject", "rework"],
        )
        self.assertEqual(payload["runtime"]["task"]["executor_result"]["test_exit_code"], 0)

        approved = self.client.post(
            f"/api/pipeline/{submitted['id']}/approve", headers=TENANT_A
        )
        self.assertEqual(approved.status_code, 200, approved.text)
        final = self.client.get(
            f"/api/pipeline/project/{self.project['project_id']}", headers=TENANT_A
        ).json()
        self.assertEqual(final["runtime"]["available_actions"], ["view_result"])

    def test_failed_task_retries_with_same_ids_and_surfaces_artifact(self):
        submitted = self._submit()
        pipeline_api._get_queue().update_status(
            submitted["id"],
            status="failed",
            executor_result={"status": "failed", "rounds": 0, "test_exit_code": 1, "files": []},
        )
        pipeline_api._graph_registry.clear()
        pipeline_api._graph_project_registry.clear()
        pipeline_api._graph_task_registry.clear()
        pipeline_api._build_runtime_fn = lambda graph: _ArtifactRuntime()

        started = self.client.post(
            f"/api/pipeline/{submitted['graph_id']}/auto-run", headers=TENANT_A
        )
        self.assertEqual(started.status_code, 200, started.text)
        payload = None
        for _ in range(100):
            payload = self.client.get(
                f"/api/pipeline/project/{self.project['project_id']}", headers=TENANT_A
            ).json()
            if payload["runtime"]["task"]["status"] == "review":
                break
            time.sleep(0.02)

        self.assertEqual(payload["runtime"]["task"]["id"], submitted["id"])
        self.assertEqual(payload["runtime"]["graph"]["graph_id"], submitted["graph_id"])
        self.assertEqual(payload["runtime"]["task"]["executor_result"]["rounds"], 2)
        self.assertEqual(payload["runtime"]["task"]["executor_result"]["artifact_text"], "4 passed\n\n4 passed")
        self.assertEqual(payload["runtime"]["trace"][0]["tool"], "local.project_runtime.focused")

    def test_fixed_local_project_uses_existing_focused_test_tool(self):
        from app.local_google_oidc import PROJECT_ID

        graph = TaskGraph.from_plan({
            "graph_id": "graph-local-focused",
            "nodes": [{"id": "n1", "goal": "run", "cap_type": "tool", "deps": []}],
        })
        pipeline_api._graph_project_registry[graph.graph_id] = PROJECT_ID
        with patch.dict(os.environ, {"CURIS_ENV": "local"}):
            runtime = pipeline_api._build_runtime(graph)
            handle = runtime.resolver.resolve(graph.nodes["n1"].cap_requirement_obj())

        self.assertEqual(handle.key, "local.project_runtime.focused")
        self.assertFalse(handle.adapter.append_prompt)
        self.assertEqual(handle.adapter.command, "/usr/bin/env")
        self.assertEqual(
            handle.adapter.args,
            [
                "CURIS_IDENTITY_MODE=test", sys.executable,
                "-m", "pytest", "-q", "--disable-warnings",
                "backend/tests/test_project_runtime_page.py",
            ],
        )

    def test_successful_tool_records_one_attempt_trace_and_result(self):
        graph = TaskGraph(graph_id="graph-tool-success")
        node = TaskNode(id="n1", goal="run", cap_requirement={"cap_type": "tool"})
        graph.add_node(node)
        runtime = PipelineRuntime(reviewer=ResultReviewer(), resolver=_SuccessfulToolResolver())

        result = runtime.run_node(node, graph)

        self.assertEqual(result.status, "done")
        self.assertEqual(node.attempts, 1)
        self.assertEqual(node.trace[0]["tool"], "local.project_runtime.focused")
        self.assertEqual(node.result["output"], "focused check passed")

    def test_cross_tenant_project_is_rejected_before_queue_write(self):
        other_project = self._create_project(TENANT_B)

        response = self.client.post(
            "/api/pipeline/submit",
            headers=TENANT_A,
            json={"project_id": other_project["project_id"], "natural_language": "实现页面"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(pipeline_api._get_queue().list_all(), [])


if __name__ == "__main__":
    unittest.main()
