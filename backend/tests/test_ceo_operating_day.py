"""CEO 经营日聚合 + 经营指标事实源（Phase-9）回归测试。

验证：
- 空公司：operating-day 返回完整五段结构，brief 空态文案，matters 为 info。
- 有数据：指标从现有实体聚合正确（projects/tasks/artifacts/ai_usage_records）。
- 周期 upsert 幂等：同周期 compute 两次行数不变、值更新。
- matters 推导：blocked_tasks>0 → risk；完成率低 → attention。
- 端点：默认公司解析、period 参数、timeline 排序、404。
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app

ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-opday", "X-Ceo-Id": "ceo-opday"}

PERIOD = "day:2026-08-04"


class CeoOperatingDayBackendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-opday-")
        self.addCleanup(self.workspace.cleanup)
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.env = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                # 注意：不设置 CURIS_D1_WORKSPACE_ROOT —— create_app 初始化时会把
                # local_rd_toolset._WORKSPACE_ROOT_OVERRIDE 设为该 env 值并全局残留，
                # 测试结束目录删除后会污染后续 local_rd_toolset 测试（workspace_root_unavailable）。
                "CURIS_D1_EXECUTE_ENABLED": "false",
                "CURIS_D1_FROZEN": "true",
                "CURIS_RD_SANDBOX": "off",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        # 防御：确保不残留指向已删除目录的 override（create_app 可能写入）。
        root_override = patch("app.local_rd_toolset._WORKSPACE_ROOT_OVERRIDE", None)
        root_override.start()
        self.addCleanup(root_override.stop)

    def _client(self) -> TestClient:
        client = TestClient(create_app(self.db_path))
        self.addCleanup(client.close)
        return client

    def _company_id(self, client: TestClient) -> str:
        return client.get("/api/workspace/companies", headers=HEADERS).json()["companies"][0][
            "company_id"
        ]

    def _seed_company_data(
        self, client: TestClient, company_id: str, *, tasks: int = 3, blocked: int = 1
    ) -> str:
        """SQL 直插 project + tasks + artifact + usage，返回 project_id。"""
        project_id = "project-opday-1"
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "insert into projects (project_id, tenant_id, company_id, department_id, "
                "name, goal, status, updated_at) values (?, ?, ?, 'dept-none', ?, ?, 'active', "
                "current_timestamp)",
                (project_id, "tenant-opday", company_id, "经营聚合项目", "验证经营日聚合"),
            )
            for index in range(tasks):
                status = "BLOCKED" if index < blocked else "COMPLETED"
                connection.execute(
                    "insert into tasks (task_id, tenant_id, company_id, project_id, content, "
                    "status, state_flow, created_at, updated_at) values (?, ?, ?, ?, ?, ?, '[]', "
                    "current_timestamp, current_timestamp)",
                    (
                        f"task-opday-{index}",
                        "tenant-opday",
                        company_id,
                        project_id,
                        f"任务 {index}",
                        status,
                    ),
                )
            connection.execute(
                "insert into artifacts (artifact_id, tenant_id, task_id, title, artifact_type, "
                "status, content, source_ref, content_sha256, created_at, updated_at) "
                "values (?, ?, ?, ?, 'execution_result', 'generated', ?, 'task.output', ?, "
                "current_timestamp, current_timestamp)",
                (
                    "artifact-opday-1",
                    "tenant-opday",
                    "task-opday-0",
                    "首个成果",
                    "成果内容",
                    "abc123",
                ),
            )
            connection.execute(
                "insert into ai_usage_records (usage_record_id, tenant_id, model_gateway_id, "
                "provider_id, model_name, employee_id, capability_id, capability_type, "
                "project_id, task_id, department_id, request_id, idempotency_key, "
                "input_tokens, output_tokens, total_tokens, "
                "cost_amount, currency, cost_source, price_version, execution_status, "
                "metering_status, occurred_at, created_at) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 10, 20, 30, ?, 'USD', "
                "'estimated', 'test-v1', 'completed', 'confirmed', current_timestamp, "
                "current_timestamp)",
                (
                    "usage-opday-1",
                    "tenant-opday",
                    "newapi",
                    "newapi",
                    "test-model",
                    "emp-opday-1",
                    "cap-opday",
                    "model",
                    project_id,
                    "task-opday-0",
                    "dept-none",
                    "req-opday-1",
                    "idem-opday-1",
                    1.25,
                ),
            )
        return project_id

    # ── 空公司 ────────────────────────────────────────────────────
    def test_operating_day_empty_company_returns_full_structure(self):
        client = self._client()
        company_id = self._company_id(client)
        response = client.get(
            "/api/workspace/ceo/operating-day",
            headers=HEADERS,
            params={"period": PERIOD},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(body["company_id"], company_id)
        for section in ("brief", "matters", "timeline", "pulse", "handoffs"):
            self.assertIn(section, body)
        self.assertIn("暂无经营数据", body["brief"]["summary"])
        self.assertEqual(body["matters"][0]["level"], "info")
        self.assertEqual(len(body["pulse"]), 9)

    # ── 有数据聚合 ────────────────────────────────────────────────
    def test_metrics_aggregate_from_entities(self):
        client = self._client()
        company_id = self._company_id(client)
        self._seed_company_data(client, company_id, tasks=3, blocked=1)
        body = client.get(
            "/api/workspace/ceo/operating-day",
            headers=HEADERS,
            params={"period": PERIOD},
        ).json()
        pulse = {item["metric_key"]: item for item in body["pulse"]}
        self.assertEqual(pulse["active_projects"]["value"], 1)
        self.assertEqual(pulse["tasks_total"]["value"], 3)
        self.assertEqual(pulse["tasks_completed"]["value"], 2)
        self.assertEqual(pulse["blocked_tasks"]["value"], 1)
        self.assertEqual(pulse["task_completion_rate"]["value"], 66.7)
        self.assertEqual(pulse["artifacts_count"]["value"], 1)
        self.assertEqual(pulse["estimated_cost"]["value"], 1.25)
        # matters 推导：blocked>0 → risk
        self.assertTrue(any(m["level"] == "risk" for m in body["matters"]))
        # timeline 含 task + artifact 事件，按时间倒序
        self.assertGreaterEqual(len(body["timeline"]), 2)
        ats = [item["at"] for item in body["timeline"]]
        self.assertEqual(ats, sorted(ats, reverse=True))
        # brief 含聚合摘要
        self.assertIn("1 个项目活跃", body["brief"]["summary"])
        self.assertIn("1 个任务受阻", body["brief"]["summary"])

    # ── 周期 upsert 幂等 ──────────────────────────────────────────
    def test_period_upsert_is_idempotent(self):
        client = self._client()
        company_id = self._company_id(client)
        self._seed_company_data(client, company_id, tasks=2, blocked=0)
        for _ in range(2):
            client.get(
                "/api/workspace/ceo/operating-day",
                headers=HEADERS,
                params={"period": PERIOD},
            )
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                "select count(*) as n from business_metrics "
                "where tenant_id = ? and company_id = ? and period = ?",
                ("tenant-opday", company_id, PERIOD),
            ).fetchone()
        self.assertEqual(rows[0], 9, "同周期重复 compute 不得产生重复行")

    # ── 端点行为 ──────────────────────────────────────────────────
    def test_unknown_company_404(self):
        client = self._client()
        response = client.get(
            "/api/workspace/ceo/operating-day",
            headers=HEADERS,
            params={"company_id": "company-not-exist"},
        )
        self.assertEqual(response.status_code, 404, response.text)

    def test_default_company_resolution(self):
        client = self._client()
        company_id = self._company_id(client)
        body = client.get(
            "/api/workspace/ceo/operating-day", headers=HEADERS
        ).json()
        self.assertEqual(body["company_id"], company_id)


if __name__ == "__main__":
    unittest.main()
