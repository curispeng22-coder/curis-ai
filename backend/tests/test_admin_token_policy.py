"""R1 item8：平台管理员令牌门禁测试（Admin 资产复盘）。

验证 main.py 的令牌修复（设计 docs/plan/curis-roadmap-design.md §一）：
  A1) 未配置令牌 -> /api/platform/* 一律 401，detail == "Admin token not configured"。
  A2) 配置正确令牌 -> 200。
  A3) 错误令牌 -> 401（detail 为「需要有效的管理员令牌」）。
  A4) ADMIN_STRICT=true 且未配置令牌 -> create_app 启动期抛 RuntimeError（拒启动）。

复用 093 测试骨架：TemporaryDirectory + create_app + TestClient + CURIS_PLATFORM_ADMIN_TOKEN。
不修改任何源码或未授权文件。
"""

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.main import create_app
from fastapi.testclient import TestClient


class AdminTokenPolicyTest(unittest.TestCase):
    def _make_client(self, token: str | None, strict: bool = False) -> TestClient:
        # 每个用例用独立环境，确保令牌配置态干净。
        saved = {}
        for key in ("CURIS_PLATFORM_ADMIN_TOKEN", "PLATFORM_ADMIN_TOKEN", "ADMIN_STRICT"):
            saved[key] = os.environ.pop(key, None)
        try:
            if token is not None:
                os.environ["CURIS_PLATFORM_ADMIN_TOKEN"] = token
            if strict:
                os.environ["ADMIN_STRICT"] = "true"
            db_path = str(Path(self.tmp.name) / "curis.sqlite")
            return TestClient(create_app(db_path))
        finally:
            # 还原环境，避免跨用例污染
            for key, val in saved.items():
                if val is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = val

    def setUp(self):
        self.tmp = TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    # ── A1：未配置令牌 -> 401 ──
    def test_unconfigured_token_returns_401(self):
        client = self._make_client(token=None)
        resp = client.get("/api/platform/department-types")
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json().get("detail"), "Admin token not configured")

    # ── A2：配置正确令牌 -> 200 ──
    def test_configured_token_returns_200(self):
        client = self._make_client(token="test-secret")
        resp = client.get(
            "/api/platform/department-types",
            headers={"Authorization": "Bearer test-secret"},
        )
        self.assertEqual(resp.status_code, 200)

    # ── A3：错误令牌 -> 401 ──
    def test_wrong_token_returns_401(self):
        client = self._make_client(token="test-secret")
        resp = client.get(
            "/api/platform/department-types",
            headers={"Authorization": "Bearer wrong"},
        )
        self.assertEqual(resp.status_code, 401)
        self.assertIn("管理员令牌", resp.json().get("detail", ""))

    # ── A4：ADMIN_STRICT=true 且未配置 -> 启动期拒启动 ──
    def test_strict_mode_refuses_to_start_without_token(self):
        with self.assertRaises(RuntimeError):
            self._make_client(token=None, strict=True)


if __name__ == "__main__":
    unittest.main()
