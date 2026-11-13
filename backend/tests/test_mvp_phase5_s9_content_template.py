from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.company_instantiation import CompanyInstantiationService
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app
from app.wave1_seed import seed_wave1


ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": "ceo-s9"}

# Legacy XHS/content business_type template frozen out of V1 scope (CEO decision 2026-10-07).
_SKIP_LEGACY_CONTENT = unittest.skip(
    "Legacy RD/XHS/TTK business_type chain frozen out of V1 "
    "(CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007, CEO decision 2026-10-07)"
)


class ContentModel:
    gateway_id = "test-gateway"
    model_name = "test-content-model"

    def __init__(self, output: str):
        self.output = output

    def runtime_config_is_declared(self):
        return True

    def validate_runtime_config(self):
        return None

    def execute(self, _prompt):
        return {
            "output": self.output,
            "estimated_cost": 0.008,
            "model_gateway_id": "test-gateway",
            "provider_id": "test-gateway",
            "model_name": "test-content-model",
            "prompt_tokens": 40,
            "completion_tokens": 80,
            "total_tokens": 120,
            "currency": "USD",
            "cost_source": "model_gateway_adapter",
            "ledger_cost_source": "estimated",
            "price_version": "test-v1",
            "metering_status": "confirmed",
            "status": "success",
            "outbound_attempted": True,
        }


def model_output() -> str:
    return json.dumps({
        "trend_analysis": "用户提供的行业报告显示，AI 团队开始关注可审计的真实执行证据。",
        "topic": {
            "title": "AI 团队真正交付的五个证据",
            "angle": "从真实任务、成本与结果追踪切入。",
        },
        "platforms": {
            "xhs": {
                "title": "AI 团队交付别只看聊天记录",
                "body": "收藏这份五项证据清单：任务、执行者、模型、成本、成果。",
                "image_headline": "AI 团队交付证据",
                "image_subtitle": "五项清单，一眼看懂",
            },
            "douyin": {
                "title": "30 秒看懂 AI 团队是否真交付",
                "body": "开场：你的 AI 团队真的完成任务了吗？正文：检查五项事实。",
                "image_headline": "AI 团队真交付",
                "image_subtitle": "30 秒检查五项事实",
            },
            "toutiao": {
                "title": "从聊天到交付：AI 团队的五项审计证据",
                "body": "企业部署 AI 团队后，应按任务、人员、模型、成本和成果核验。",
                "image_headline": "从聊天到交付",
                "image_subtitle": "AI 团队的五项审计证据",
            },
        },
        "retrospective": {
            "hypothesis": "证据清单型内容更容易带来收藏和有效咨询。",
            "metrics": ["收藏率", "完播率", "有效咨询数"],
            "next_review": "发布 72 小时后按平台分别复盘，未发布前不填写表现数据。",
        },
    }, ensure_ascii=False)


class MVPPhase5S9ContentTemplateTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        identity = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        identity.start()
        self.addCleanup(identity.stop)

    def _client(self, output: str) -> TestClient:
        database = Database(self.db_path)
        database.initialize()
        seed_wave1(database)
        CompanyInstantiationService(database, EvolutionEventLog(database)).instantiate(
            "ccp_ai_content_company", "selfuse"
        )
        client = TestClient(create_app(self.db_path, model_gateway_adapter=ContentModel(output)))
        self.addCleanup(client.close)
        return client

    def _task(self, client: TestClient):
        companies = client.get("/api/workspace/companies", headers=HEADERS).json()["companies"]
        company = next(
            item
            for item in companies
            if item["source_company_package_id"] == "ccp_ai_content_company"
        )
        departments = client.get("/api/workspace/departments", headers=HEADERS).json()["departments"]
        department = next(
            item
            for item in departments
            if item["company_id"] == company["company_id"]
            and item["department_type"] == "content.growth"
        )
        employees = client.get("/api/workspace/employees", headers=HEADERS).json()["employees"]
        employee = next(
            item
            for item in employees
            if item["department_id"] == department["id"]
            and item["role"] == "content_operator"
        )
        registered = client.post(
            "/api/workspace/capabilities/registry",
            headers=HEADERS,
            json={
                "capability_key": "model.s9-content",
                "type": "model",
                "name": "S9 Content",
                "provider_id": "test-gateway",
                "model_name": "test-content-model",
            },
        )
        self.assertEqual(registered.status_code, 201, registered.text)
        bound = client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=HEADERS,
            json={
                "bindings": [{
                    "capability_source": "official",
                    "capability_type": "model",
                    "capability_id": "model.s9-content",
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
                "name": "S9 内容项目",
                "goal": "完成多平台内容成果闭环",
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "status": "active",
            },
        ).json()
        task = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=HEADERS,
            json={
                "content": "基于给定行业报告制作三平台内容",
                "employee_id": employee["id"],
                "capability_source": "official",
                "capability_type": "model",
                "capability_id": "model.s9-content",
            },
        )
        self.assertEqual(task.status_code, 201, task.text)
        return project, task.json()["task_id"]

    @_SKIP_LEGACY_CONTENT
    def test_real_content_task_persists_copy_svg_and_retrospective(self):
        client = self._client(model_output())
        project, task_id = self._task(client)
        response = client.post(
            "/api/workspace/content-workflow/run",
            headers=HEADERS,
            json={
                "project_id": project["project_id"],
                "task_id": task_id,
                "trend_source": "https://example.com/industry-report",
                "trend_summary": "行业报告讨论 AI 团队从对话走向可审计交付。",
                "platforms": ["xhs", "douyin", "toutiao"],
                "brand_voice_ref": "brand-curis",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        result = response.json()
        self.assertEqual(result["status"], "completed")
        self.assertFalse(result["published"])
        self.assertEqual(len(result["steps"]), 5)
        artifacts = result["package"]["artifacts"]
        self.assertEqual(len(artifacts), 8)
        self.assertEqual(
            {item["platform"] for item in artifacts if item["type"] == "media_asset"},
            {"xhs", "douyin", "toutiao"},
        )
        self.assertTrue(all(
            item["body"].startswith("<svg")
            for item in artifacts
            if item["type"] == "media_asset"
        ))
        self.assertEqual(
            [item for item in artifacts if item["type"] == "multichannel_draft"][0]
            ["metadata"]["published"],
            False,
        )

        task = client.get(f"/api/task/{task_id}", headers=HEADERS).json()
        self.assertEqual(task["status"], "COMPLETED")
        self.assertEqual(task["selected_tool"], "content_workflow_runtime")
        stored_output = json.loads(task["output"])
        self.assertEqual(stored_output["project_id"], project["project_id"])
        self.assertEqual(stored_output["package"]["package_id"], result["package"]["package_id"])
        job = client.get(f"/api/workspace/jobs/{task_id}", headers=HEADERS).json()
        self.assertEqual(job["model_usage"]["total_tokens"], 120)
        self.assertEqual(job["model_usage"]["estimated_cost"], 0.008)

        runs = client.get(
            "/api/results/content-workflow-runs",
            headers=HEADERS,
        ).json()["runs"]
        self.assertEqual(runs[0]["run_id"], result["run_id"])
        self.assertEqual(runs[0]["status"], "completed")
        packages = client.get(
            "/api/results/publish-packages",
            headers=HEADERS,
        ).json()["publish_packages"]
        self.assertEqual(packages[0]["status"], "generated")
        self.assertEqual(packages[0]["published_platforms"], [])

    @_SKIP_LEGACY_CONTENT
    def test_invalid_model_output_marks_run_and_task_failed(self):
        client = self._client("not-json")
        project, task_id = self._task(client)
        response = client.post(
            "/api/workspace/content-workflow/run",
            headers=HEADERS,
            json={
                "project_id": project["project_id"],
                "task_id": task_id,
                "trend_source": "行业报告",
                "trend_summary": "可追溯摘要",
                "platforms": ["xhs"],
            },
        )
        self.assertEqual(response.status_code, 422, response.text)
        task = client.get(f"/api/task/{task_id}", headers=HEADERS).json()
        self.assertEqual(task["status"], "FAILED")
        self.assertEqual(task["error"], "content_generation_failed")
        runs = client.get(
            "/api/results/content-workflow-runs",
            headers=HEADERS,
        ).json()["runs"]
        self.assertEqual(runs[0]["status"], "failed")

    def test_frontend_exposes_content_project_flow_and_structured_result(self):
        paths = [
            ROOT / "frontend/lib/content.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/ContentRunDrawer.js",
            ROOT / "frontend/app/ceo-office/projects/[id]/page.js",
            ROOT / "frontend/app/ceo-office/projects/ProjectFormDrawer.js",
            ROOT / "frontend/app/ceo-office/projects/page.js",
            ROOT / "frontend/app/ceo-office/execution/tasks/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for value in (
            "runContentWorkflow",
            "启动内容工作流",
            "热点来源",
            "trend_summary",
            "media_asset",
            "复盘计划",
            "外部发布未执行",
            "company_id: companyId",
            "getProjects()",
        ):
            self.assertIn(value, source)


if __name__ == "__main__":
    unittest.main()
