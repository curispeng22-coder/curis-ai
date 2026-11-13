from __future__ import annotations

import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter


ROOT = Path(__file__).resolve().parents[2]
TENANT = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}


class FailoverHttpPost:
    def __init__(self):
        self.models = []

    def __call__(self, url, payload, headers, timeout):
        self.models.append(payload["model"])
        if payload["model"] == "preferred-model":
            raise urllib.error.HTTPError(url, 503, "unavailable", {}, None)
        return {
            "choices": [{"message": {"content": "fallback execution result"}}],
            "usage": {
                "prompt_tokens": 6,
                "completion_tokens": 4,
                "total_tokens": 10,
                "estimated_cost": 0.0042,
            },
        }


class MVPPhase4S7ModelGatewayTests(unittest.TestCase):
    def setUp(self):
        identity_env = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_MODEL_GATEWAY_PRICE_VERSION": "test-v1",
            },
        )
        identity_env.start()
        self.addCleanup(identity_env.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.http_post = FailoverHttpPost()
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="test-secret",
            gateway_id="newapi",
            model_name="fallback-model",
            http_post=self.http_post,
        )
        self.client = TestClient(create_app(self.db_path, model_gateway_adapter=adapter))
        self.addCleanup(self.client.close)

    def _project_and_employee(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT
        ).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        ).json()
        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT,
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
            headers=TENANT,
            json={
                "company_id": company["company_id"],
                "name": "S7 模型验收",
                "goal": "验证人工模型选择与回退",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
            },
        ).json()
        return project, employee

    def test_bound_model_runs_and_falls_back_once_with_usage(self):
        model = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT,
            json={
                "capability_key": "model.preferred",
                "type": "model",
                "name": "首选模型",
                "provider_id": "newapi",
                "model_name": "preferred-model",
                "description": "人工选择的首选模型",
            },
        )
        self.assertEqual(model.status_code, 201, model.text)
        self.assertEqual(model.json()["model_name"], "preferred-model")

        project, employee = self._project_and_employee()
        bound = self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT,
            json={
                "bindings": [
                    {
                        "capability_source": "official",
                        "capability_type": "model",
                        "capability_id": "model.preferred",
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(bound.status_code, 200, bound.text)

        created = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT,
            json={
                "content": "总结模型网关验收结果",
                "employee_id": employee["id"],
                "capability_source": "official",
                "capability_type": "model",
                "capability_id": "model.preferred",
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        task_id = created.json()["task_id"]
        stored = self.client.get(f"/api/task/{task_id}", headers=TENANT).json()
        self.assertEqual(stored["requested_capability_id"], "model.preferred")

        started = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks/{task_id}/jobs",
            headers=TENANT,
        )
        self.assertEqual(started.status_code, 202, started.text)
        job = self.client.get(f"/api/workspace/jobs/{task_id}", headers=TENANT)
        self.assertEqual(job.status_code, 200, job.text)
        self.assertEqual(job.json()["status"], "completed")
        self.assertEqual(job.json()["output"], "fallback execution result")
        self.assertEqual(self.http_post.models, ["preferred-model", "fallback-model"])
        usage = job.json()["model_usage"]
        self.assertEqual(usage["model_gateway_id"], "newapi")
        self.assertEqual(usage["model_name"], "fallback-model")
        self.assertEqual(usage["total_tokens"], 10)
        self.assertEqual(usage["estimated_cost"], 0.0042)
        self.assertTrue(usage["fallback_used"])
        self.assertEqual(usage["fallback_from_model"], "preferred-model")
        self.assertEqual(usage["fallback_reason"], "gateway_error")

        summary = self.client.get("/api/workspace/model-gateway", headers=TENANT)
        self.assertEqual(summary.status_code, 200, summary.text)
        payload = summary.json()
        self.assertTrue(any(item["gateway_id"] == "newapi" for item in payload["providers"]))
        self.assertTrue(any(item["model_key"] == "model.preferred" for item in payload["models"]))
        self.assertEqual(payload["usage"]["totals"]["usage_event_count"], 2)
        self.assertEqual(payload["usage"]["totals"]["total_tokens"], 10)
        self.assertEqual(payload["usage"]["totals"]["estimated_cost"], 0.0042)
        self.assertEqual(payload["usage"]["totals"]["unmetered_count"], 1)
        text = str(payload)
        for forbidden in ("test-secret", "Authorization", "总结模型网关验收结果", "output", "raw_response"):
            self.assertNotIn(forbidden, text)

    def test_frontend_selects_only_bound_models_and_shows_usage(self):
        paths = [
            ROOT / "frontend/lib/capabilities.js",
            ROOT / "frontend/app/ceo-office/capabilities/CapabilityFormDrawer.js",
            ROOT / "frontend/app/ceo-office/capabilities/[type]/[id]/page.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js",
            ROOT / "frontend/app/ceo-office/execution/tasks/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for value in (
            "getModelGatewaySummary",
            "getEmployeeCapabilities",
            "model_name",
            "capability_source",
            "fallback_used",
            "total_tokens",
        ):
            self.assertIn(value, source)


if __name__ == "__main__":
    unittest.main()
