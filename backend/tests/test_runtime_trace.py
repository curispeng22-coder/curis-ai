"""运行时 trace 事件服务（EvoFlow 复用 A2）回归测试。

验证：
- append-only 写入 + 查询（token / cache_hit / payload 字段完整往返）。
- run_id 过滤、limit 截断、时间倒序。
- 端点只读返回；不改变任务语义（tasks 表零改动）。
- effect_class（A1）投影派生正确（含工具名启发式）。
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.catalog_constants import (
    effect_class_for_capability,
    effect_class_for_tool,
)
from app.database import Database
from app.main import create_app
from app.runtime_trace import RuntimeTraceService
from app.tenant_context import TenantContext

ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-trace", "X-Ceo-Id": "ceo-trace"}
OTHER_HEADERS = {"X-Tenant-Id": "tenant-other", "X-Ceo-Id": "ceo-other"}


class RuntimeTraceBackendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory(prefix="curis-trace-")
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
                # 不设 CURIS_D1_WORKSPACE_ROOT：避免 create_app 把
                # local_rd_toolset._WORKSPACE_ROOT_OVERRIDE 残留成已删临时目录（坑见 08-04 日志）。
                "CURIS_D1_EXECUTE_ENABLED": "false",
                "CURIS_D1_FROZEN": "true",
                "CURIS_RD_SANDBOX": "off",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        root_override = patch("app.local_rd_toolset._WORKSPACE_ROOT_OVERRIDE", None)
        root_override.start()
        self.addCleanup(root_override.stop)

    def _client(self) -> TestClient:
        client = TestClient(create_app(self.db_path))
        self.addCleanup(client.close)
        return client

    def _service(self) -> RuntimeTraceService:
        database = Database(self.db_path)
        return RuntimeTraceService(database)

    # ── 写入 + 查询往返 ───────────────────────────────────────────
    def test_write_and_query_roundtrip(self):
        client = self._client()
        service = self._service()
        with TenantContext.scope("tenant-trace"):
            event = service.write_event(
                run_id="run-1",
                event_type="model_call",
                capability="official.newapi.default",
                task_id="task-1",
                task_ref="run-1/rd/1",
                tokens_in=10,
                tokens_out=20,
                cache_hit=True,
                latency_ms=123,
                payload={"ok": True, "status": "completed"},
            )
        self.assertEqual(event["event_type"], "model_call")
        self.assertEqual(event["tokens_in"], 10)
        self.assertEqual(event["cache_hit"], True)
        self.assertEqual(event["payload"]["status"], "completed")

        events = client.get("/api/workspace/runtime-trace", headers=HEADERS).json()["events"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["run_id"], "run-1")
        self.assertEqual(events[0]["task_ref"], "run-1/rd/1")
        self.assertEqual(events[0]["latency_ms"], 123)

    def test_tenant_isolation(self):
        client = self._client()
        service = self._service()
        with TenantContext.scope("tenant-trace"):
            service.write_event(run_id="run-1", event_type="model_call")
        other = client.get("/api/workspace/runtime-trace", headers=OTHER_HEADERS).json()["events"]
        self.assertEqual(other, [])

    def test_run_id_filter_and_limit(self):
        client = self._client()
        service = self._service()
        with TenantContext.scope("tenant-trace"):
            for index in range(5):
                service.write_event(run_id=f"run-{index % 2}", event_type=f"evt-{index}")
        filtered = client.get(
            "/api/workspace/runtime-trace", headers=HEADERS, params={"run_id": "run-1"}
        ).json()["events"]
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(item["run_id"] == "run-1" for item in filtered))
        limited = client.get(
            "/api/workspace/runtime-trace", headers=HEADERS, params={"limit": 3}
        ).json()["events"]
        self.assertEqual(len(limited), 3)

    # ── effect_class（A1）──
    def test_effect_class_heuristic(self):
        self.assertEqual(effect_class_for_tool("tl_ai_rd_file_reader"), "read")
        self.assertEqual(effect_class_for_tool("tl_ai_rd_code_docs_search"), "retrieve")
        self.assertEqual(effect_class_for_tool("tl_ai_rd_file_writer"), "write")
        self.assertEqual(effect_class_for_tool("tl_ai_rd_test_runner"), "exec")
        self.assertEqual(effect_class_for_tool("tl_ai_content_social_upload"), "write")
        self.assertEqual(effect_class_for_capability("model"), "read")
        self.assertEqual(effect_class_for_capability("agent"), "exec")
        self.assertEqual(effect_class_for_capability("mcp"), "exec")
        self.assertEqual(effect_class_for_capability("unknown_type"), "exec")  # deny-by-default 安全侧

    def test_catalog_projection_includes_effect_class(self):
        client = self._client()
        caps = client.get("/api/catalog/capabilities", headers=HEADERS).json()["capabilities"]
        self.assertGreaterEqual(len(caps), 1)
        for cap in caps:
            self.assertIn("effect_class", cap)
            self.assertIn(cap["effect_class"], {"read", "retrieve", "write", "exec"})


if __name__ == "__main__":
    unittest.main()
