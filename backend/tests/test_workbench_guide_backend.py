"""业务工作台引导（Workbench Guide）后端回归测试。

验证：
- 引导模板注册表（内置 guide.business_workbench，未知 guide 404）。
- 会话状态机：start → answer（AI 追问/蓝图/manual_fallback）→ confirm 落地 → DONE。
- 引导模型解析：自定义 tenant_private agent 优先（env:VAR 密钥直调私有端点），
  官方偏好兜底；模型调用失败不静默降级（manual_fallback）。
- 落地复用现有原语：蓝图 → 部门/员工/项目真实落库。
- 安全：secret-like answer 拒绝；无默认公司 422；状态冲突 409。
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter

ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-guide", "X-Ceo-Id": "ceo-guide"}

DEPT_TEMPLATE_ID = "official.department.software_rnd"
EMP_TEMPLATE_ID = "official.employee.tech_lead"

BLUEPRINT_CONTENT = json.dumps(
    {
        "mode": "blueprint",
        "blueprint": {
            "project_name": "AI 短视频工作室",
            "goal": "每周产出 3 条爆款短视频",
            "description": "短视频内容制作工作台",
            "departments": [
                {
                    "template_id": DEPT_TEMPLATE_ID,
                    "name": "内容部",
                    "employees": [{"template_id": EMP_TEMPLATE_ID, "name": "主编"}],
                }
            ],
            "owner_employee_ref": "主编",
        },
    },
    ensure_ascii=False,
)

FOLLOW_UP_CONTENT = json.dumps(
    {"mode": "follow_up", "question": "你预期的业务产出周期是多久？"}, ensure_ascii=False
)

PRIVATE_AGENT_BASE_URL = "https://private-guide-agent.example.com"
PRIVATE_AGENT_KEY_REF = "env:TEST_GUIDE_AGENT_KEY"
PRIVATE_AGENT_SECRET = "guide-agent-secret-xyz"


class RecordingHttpPost:
    """记录所有出站调用；content 可配置（模拟引导 AI 的 JSON 输出）。"""

    def __init__(self, content: str = "") -> None:
        self.calls: list[dict] = []
        self.content = content

    def __call__(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        self.calls.append({"url": url, "payload": payload, "headers": headers, "timeout": timeout})
        return {
            "choices": [{"message": {"content": self.content}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }


class WorkbenchGuideBackendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-guide-")
        self.addCleanup(self.workspace.cleanup)
        self.workspace_path = Path(self.workspace.name)

        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))

        self.http_post = RecordingHttpPost()
        self.env = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_D1_EXECUTE_ENABLED": "true",
                "CURIS_D1_FROZEN": "false",
                "CURIS_D1_WORKSPACE_ROOT": str(self.workspace_path),
                "CURIS_RD_SANDBOX": "off",
                # 官方兜底路径需要可用网关；manual_fallback 用例单独清空。
                "CURIS_MODEL_GATEWAY_BASE_URL": "https://official-gateway.example.com",
                "CURIS_MODEL_GATEWAY_API_KEY": "test-gateway-key",
                "CURIS_MODEL_GATEWAY_MODEL": "test-model",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)

    def _client(self, http_post: RecordingHttpPost | None = None) -> TestClient:
        client = TestClient(
            create_app(
                self.db_path,
                model_gateway_adapter=ModelGatewayAdapter(
                    http_post=http_post or self.http_post
                ),
            )
        )
        self.addCleanup(client.close)
        return client

    # ── 模板与会话基础 ─────────────────────────────────────────────
    def test_list_guides_returns_builtin_template(self):
        client = self._client()
        guides = client.get("/api/workspace/guides", headers=HEADERS).json()["guides"]
        self.assertEqual(len(guides), 1)
        self.assertEqual(guides[0]["guide_id"], "guide.business_workbench")
        self.assertEqual(guides[0]["steps"][0]["type"], "free_form")

    def test_start_session_unknown_guide_404(self):
        client = self._client()
        response = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.not_exist"},
        )
        self.assertEqual(response.status_code, 404, response.text)

    def test_start_session_returns_first_step(self):
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        self.assertEqual(session["status"], "COLLECTING")
        self.assertEqual(session["current_step"], 1)
        self.assertEqual(session["step"]["step"], 1)

    # ── 蓝图全链路：start → answer → confirm 落地 ──────────────────
    def test_blueprint_full_chain_lands_workbench(self):
        self.http_post.content = BLUEPRINT_CONTENT
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        answer = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我想做一个短视频内容工作室，目标每周产出 3 条爆款。"},
        )
        self.assertEqual(answer.status_code, 200, answer.text)
        body = answer.json()
        self.assertEqual(body["mode"], "blueprint")
        self.assertEqual(body["status"], "READY")
        blueprint = body["blueprint"]
        self.assertEqual(blueprint["project_name"], "AI 短视频工作室")

        confirm = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/confirm",
            headers=HEADERS,
            json={"blueprint": blueprint},
        )
        self.assertEqual(confirm.status_code, 200, confirm.text)
        workbench = confirm.json()["workbench"]
        self.assertEqual(workbench["project_name"], "AI 短视频工作室")
        self.assertEqual(len(workbench["department_ids"]), 1)
        self.assertEqual(len(workbench["employee_ids"]), 1)
        self.assertIsNotNone(workbench["owner_employee_id"])

        project = client.get(
            f"/api/workspace/projects/{workbench['project_id']}", headers=HEADERS
        ).json()
        self.assertEqual(project["name"], "AI 短视频工作室")
        self.assertEqual(project["status"], "active")
        company = client.get("/api/workspace/companies", headers=HEADERS).json()["companies"][0]
        departments = client.get(
            f"/api/workspace/companies/{company['company_id']}/departments", headers=HEADERS
        ).json()["departments"]
        self.assertTrue(any(d["id"] == workbench["department_ids"][0] for d in departments))

    # ── AI 追问：信息不足不推进步骤 ────────────────────────────────
    def test_answer_follow_up_keeps_collecting(self):
        self.http_post.content = FOLLOW_UP_CONTENT
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        answer = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我想做一个内容工作室。"},
        ).json()
        self.assertEqual(answer["mode"], "follow_up")
        self.assertEqual(answer["status"], "COLLECTING")
        self.assertEqual(answer["current_step"], 1)

    # ── 模型不可用：manual_fallback，不静默降级 ────────────────────
    def test_answer_manual_fallback_when_model_unavailable(self):
        # 无自定义能力 + 官方网关配置缺失 → 配置校验失败重试耗尽 → manual_fallback。
        with patch.dict(
            os.environ,
            {
                "CURIS_MODEL_GATEWAY_BASE_URL": "",
                "CURIS_MODEL_GATEWAY_API_KEY": "",
                "CURIS_MODEL_GATEWAY_MODEL": "",
            },
        ):
            client = self._client()
            session = client.post(
                "/api/workspace/guides/sessions",
                headers=HEADERS,
                json={"guide_id": "guide.business_workbench"},
            ).json()
            answer = client.post(
                f"/api/workspace/guides/sessions/{session['session_id']}/answer",
                headers=HEADERS,
                json={"step": 1, "answer": "我想做一个内容工作室，目标每周产出爆款。"},
            )
        self.assertEqual(answer.status_code, 200, answer.text)
        body = answer.json()
        self.assertEqual(body["mode"], "manual_fallback")
        self.assertIn("goal", body["fields"])
        # 不静默降级：字段提示而非伪造蓝图；配置缺失不触发任何出站调用。
        self.assertEqual(self.http_post.calls, [])

    # ── 引导模型解析：自定义 tenant_private agent 优先 ─────────────
    def test_guide_model_resolver_prefers_tenant_private_agent(self):
        os.environ["TEST_GUIDE_AGENT_KEY"] = PRIVATE_AGENT_SECRET
        self.addCleanup(lambda: os.environ.pop("TEST_GUIDE_AGENT_KEY", None))
        self.http_post.content = BLUEPRINT_CONTENT

        client = self._client()
        registered = client.post(
            "/api/workspace/capabilities/private",
            headers=HEADERS,
            json={
                "capability_type": "agent",
                "capability_id": "my-guide-agent",
                "display_name": "My Guide Agent",
                "metadata": {
                    "kind": "openai-compatible",
                    "endpoint": PRIVATE_AGENT_BASE_URL,
                    "credential_ref": PRIVATE_AGENT_KEY_REF,
                },
            },
        )
        self.assertEqual(registered.status_code, 201, registered.text)

        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我想做一个短视频内容工作室，每周 3 条爆款。"},
        )
        self.assertGreaterEqual(len(self.http_post.calls), 1)
        for call in self.http_post.calls:
            self.assertEqual(call["url"], f"{PRIVATE_AGENT_BASE_URL}/v1/chat/completions")
            self.assertEqual(call["headers"]["Authorization"], f"Bearer {PRIVATE_AGENT_SECRET}")

    # ── 状态冲突与安全 ─────────────────────────────────────────────
    def test_confirm_before_ready_409(self):
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        confirm = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/confirm",
            headers=HEADERS,
            json={"blueprint": {"project_name": "x", "goal": "y", "departments": []}},
        )
        self.assertEqual(confirm.status_code, 409, confirm.text)

    def test_reconfirm_after_done_409(self):
        self.http_post.content = BLUEPRINT_CONTENT
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        answer = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我想做一个短视频内容工作室。"},
        ).json()
        blueprint = answer["blueprint"]
        first = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/confirm",
            headers=HEADERS,
            json={"blueprint": blueprint},
        )
        self.assertEqual(first.status_code, 200, first.text)
        second = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/confirm",
            headers=HEADERS,
            json={"blueprint": blueprint},
        )
        self.assertEqual(second.status_code, 409, second.text)

    def test_answer_secret_like_rejected_422(self):
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        answer = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我的 api_key=sk-abcdef1234567890 是这样的"},
        )
        self.assertEqual(answer.status_code, 422, answer.text)

    def test_confirm_no_company_422(self):
        # 无默认公司分支（正常 API 路径会惰性重建，此处 mock 防御分支）→ 422 提示先建公司。
        from app.workbench_guide import GuideSessionError, WorkbenchInstantiator

        self.http_post.content = BLUEPRINT_CONTENT
        client = self._client()
        session = client.post(
            "/api/workspace/guides/sessions",
            headers=HEADERS,
            json={"guide_id": "guide.business_workbench"},
        ).json()
        answer = client.post(
            f"/api/workspace/guides/sessions/{session['session_id']}/answer",
            headers=HEADERS,
            json={"step": 1, "answer": "我想做一个短视频内容工作室。"},
        ).json()
        blueprint = answer["blueprint"]
        with patch.object(
            WorkbenchInstantiator,
            "_default_company_id",
            side_effect=GuideSessionError(
                "尚未创建公司，请先创建公司后再发起业务引导",
                status="no_company",
                http_status=422,
            ),
        ):
            confirm = client.post(
                f"/api/workspace/guides/sessions/{session['session_id']}/confirm",
                headers=HEADERS,
                json={"blueprint": blueprint},
            )
        self.assertEqual(confirm.status_code, 422, confirm.text)
        self.assertIn("创建公司", confirm.json()["detail"])


if __name__ == "__main__":
    unittest.main()
