"""Step 4：连接器模式界面切换（持久化设置优先，环境变量兜底）。

覆盖：
- ``Database.get_setting / set_setting / delete_setting / list_settings`` 键值仓储。
- ``GET/PUT /api/connectors/mode`` 读写与来源标记（setting / env / default）。
- ``GET /api/connectors`` 的 ``mode`` 跟随持久化设置变化。
- 红线复核：工作流代码依旧不感知 ``CURIS_CONNECTOR_MODE``。
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.connectors import (
    ConnectorMode,
    current_connector_mode,
    set_connector_mode_provider,
)
from app.database import Database
from app.main import create_app

TENANT = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
WORKFLOW_SRC = (
    Path(__file__).resolve().parents[1] / "app" / "content_workflow_runtime.py"
)


class Step4SystemSettingsTestCase(unittest.TestCase):
    """system_settings 键值仓储基础行为。"""

    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(
            lambda: os.path.exists(self.db_path) and os.unlink(self.db_path)
        )
        self.database = Database(self.db_path)
        self.database.initialize()

    def test_get_returns_default_when_absent(self):
        self.assertIsNone(self.database.get_setting("connector.mode"))
        self.assertEqual(
            self.database.get_setting("connector.mode", "mock"), "mock"
        )

    def test_set_then_get_and_overwrite(self):
        self.database.set_setting("connector.mode", "real")
        self.assertEqual(self.database.get_setting("connector.mode"), "real")
        self.database.set_setting("connector.mode", "mock")
        self.assertEqual(self.database.get_setting("connector.mode"), "mock")

    def test_delete_and_list_by_prefix(self):
        self.database.set_setting("connector.mode", "real")
        self.database.set_setting("capability.probe", "true")
        self.assertEqual(
            self.database.list_settings("connector."), {"connector.mode": "real"}
        )
        self.assertTrue(self.database.delete_setting("connector.mode"))
        self.assertFalse(self.database.delete_setting("connector.mode"))
        self.assertIsNone(self.database.get_setting("connector.mode"))
        self.assertEqual(len(self.database.list_settings()), 1)


class Step4ConnectorModeApiTestCase(unittest.TestCase):
    """连接器模式读写端点 + 解析优先级。"""

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
        self.addCleanup(
            lambda: os.path.exists(self.db_path) and os.unlink(self.db_path)
        )
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)
        # create_app 注入了模式提供者，测试结束后撤销，避免污染其它用例。
        self.addCleanup(lambda: set_connector_mode_provider(None))

    def test_default_mode_is_mock_from_env_or_default(self):
        response = self.client.get("/api/connectors/mode", headers=TENANT)
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(body["mode"], "mock")
        self.assertIn(body["source"], ("env", "default"))
        self.assertIsNone(body["persisted"])

    def test_put_real_persists_and_wins_over_env(self):
        with patch.dict(os.environ, {"CURIS_CONNECTOR_MODE": "mock"}):
            written = self.client.put(
                "/api/connectors/mode", headers=TENANT, json={"mode": "real"}
            )
            self.assertEqual(written.status_code, 200, written.text)
            self.assertEqual(written.json()["mode"], "real")
            self.assertEqual(written.json()["source"], "setting")

            # 连接器层实际解析结果同步变为 real（工作流代码零改动）。
            self.assertEqual(current_connector_mode(), ConnectorMode.REAL)

            catalog = self.client.get("/api/connectors", headers=TENANT)
            self.assertEqual(catalog.status_code, 200, catalog.text)
            self.assertEqual(catalog.json()["mode"], "real")
            self.assertEqual(catalog.json()["mode_source"], "setting")

    def test_put_empty_clears_setting_and_falls_back_to_env(self):
        self.client.put(
            "/api/connectors/mode", headers=TENANT, json={"mode": "real"}
        )
        with patch.dict(os.environ, {"CURIS_CONNECTOR_MODE": "mock"}):
            cleared = self.client.put(
                "/api/connectors/mode", headers=TENANT, json={"mode": ""}
            )
            self.assertEqual(cleared.status_code, 200, cleared.text)
            self.assertEqual(cleared.json()["mode"], "mock")
            self.assertEqual(cleared.json()["source"], "env")
            self.assertIsNone(cleared.json()["persisted"])

    def test_put_rejects_unknown_mode(self):
        rejected = self.client.put(
            "/api/connectors/mode", headers=TENANT, json={"mode": "staging"}
        )
        self.assertEqual(rejected.status_code, 422, rejected.text)

    def test_workflow_code_still_does_not_branch_on_connector_mode(self):
        """红线复核：模式来源变了，但工作流代码依旧不感知。"""
        text = WORKFLOW_SRC.read_text(encoding="utf-8")
        self.assertNotIn("CURIS_CONNECTOR_MODE", text)
        self.assertNotIn("os.getenv", text)


if __name__ == "__main__":
    unittest.main()
