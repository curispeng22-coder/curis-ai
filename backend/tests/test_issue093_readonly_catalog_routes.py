"""Issue 093（Admin 资产复盘）：只读 Catalog GET 路由接口测试。

验证新增的四个只读 GET 路由：
  GET /api/platform/personas         -> {"persona_templates": [...]}
  GET /api/platform/dashboards       -> {"dashboard_templates": [...]}
  GET /api/platform/company-packages -> {"company_packages": [...]}
  GET /api/platform/company-templates-> {"company_templates": [...]}

断言：
  1) 鉴权失败（无/错令牌）-> 401（与 _require_platform_admin 一致）。
  2) 鉴权通过 -> HTTP 200，且返回种子数据行数 > 0。

复用现有 /api/platform/* 既有风格（见 test_d4_platform.py）：临时 SQLite +
TestClient + CURIS_PLATFORM_ADMIN_TOKEN。仅消费 seed_wave1 等价初始化数据，
不修改任何源码或未授权文件。
"""

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.main import create_app
from fastapi.testclient import TestClient

# 与现有 /api/platform/* 测试保持一致的 dev 令牌（生产须由环境变量注入）。
_PLATFORM_ADMIN_TOKEN = "platform-admin-dev"


class Issue093ReadonlyCatalogRoutesTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _PLATFORM_ADMIN_TOKEN)
        self.tmp = TemporaryDirectory()
        db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.client = TestClient(create_app(db_path))
        self.auth = {"Authorization": f"Bearer {_PLATFORM_ADMIN_TOKEN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── 鉴权门禁：与既有 /api/platform/* 行为一致 ──
    def test_routes_require_platform_admin(self):
        routes = [
            "/api/platform/personas",
            "/api/platform/dashboards",
            "/api/platform/company-packages",
            "/api/platform/company-templates",
        ]
        for route in routes:
            # 无令牌 -> 401
            self.assertEqual(
                self.client.get(route).status_code, 401, f"{route} 无令牌应 401"
            )
            # 错误令牌 -> 401
            self.assertEqual(
                self.client.get(route, headers={"Authorization": "Bearer wrong"}).status_code,
                401,
                f"{route} 错误令牌应 401",
            )

    # ── 四个只读 GET 路由：200 + 种子行数 > 0 ──
    def test_list_personas_returns_seeded_rows(self):
        resp = self.client.get("/api/platform/personas", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("persona_templates", body)
        self.assertGreater(len(body["persona_templates"]), 0)

    def test_list_dashboards_returns_seeded_rows(self):
        resp = self.client.get("/api/platform/dashboards", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("dashboard_templates", body)
        self.assertGreater(len(body["dashboard_templates"]), 0)

    def test_list_company_packages_returns_seeded_rows(self):
        resp = self.client.get("/api/platform/company-packages", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("company_packages", body)
        self.assertGreater(len(body["company_packages"]), 0)

    def test_list_company_templates_returns_seeded_rows(self):
        resp = self.client.get("/api/platform/company-templates", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("company_templates", body)
        self.assertGreater(len(body["company_templates"]), 0)


if __name__ == "__main__":
    unittest.main()
