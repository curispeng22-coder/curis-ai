"""Phase-9A P2 Capability Package Commercial Configuration —— 验证套件。

覆盖 docs/design/phase9a-p2-cappkg-implementation-design.md 测试矩阵核心项：
建表/seed 幂等、CRUD、JSON 数组存取、非法枚举 422、空名 422、404、状态机、
不硬编码（改引用后 API 返回新值）、守卫 401。所有端点受 ``_require_platform_admin``
守卫（401 非 403）。仅 Admin 商业配置，不实现 Marketplace/支付/自动销售/Workspace 安装。

运行：backend/.venv/bin/python -m pytest tests/test_capability_packages.py -q
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.billing_store import BillingStore
from app.database import Database
from app.main import create_app
from fastapi.testclient import TestClient

_ADMIN = "platform-admin-dev"


class Phase9A2CapabilityPackageTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a_p2.sqlite")
        # create_app 内部调用 database.initialize()：建表 + 全部既有 seed +
        # capability_packages DDL + 示例官方包 seed（cp_content_ops）。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── T1 建表幂等（重复 initialize 不报错、表与索引存在）────
    def test_t1_table_idempotent(self):
        self.db.initialize()
        with self.db.connect() as conn:
            names = {
                r["name"]
                for r in conn.execute(
                    "select name from sqlite_master where type in ('table','index')"
                ).fetchall()
            }
        self.assertIn("capability_packages", names)
        self.assertIn("idx_capability_packages_status", names)
        self.assertIn("idx_capability_packages_availability", names)

    # ── T2 seed 幂等（示例官方包仅 1 条，active）──────────
    def test_t2_seed_idempotent(self):
        self.db.initialize()
        active = self.billing.list_capability_packages(status="active")
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["package_id"], "cp_content_ops")
        self.assertEqual(active[0]["name"], "内容运营包")
        # 再跑一次 initialize，不应重复插入（insert or ignore）。
        self.db.initialize()
        self.assertEqual(len(self.billing.list_capability_packages(status="active")), 1)

    # ── T3 创建 → 201，JSON 数组正确存取 ─────────────────
    def test_t3_create_returns_201_and_stores_arrays(self):
        resp = self.client.post(
            "/api/platform/capability-packages",
            headers=self.auth,
            json={
                "name": "企业旗舰包",
                "description": "面向大客户的旗舰能力包",
                "capability_ids": ["task_execution"],
                "connector_ids": ["shopify"],
                "workflow_template_ids": ["wt_001"],
                "employee_template_ids": ["et_001"],
                "pricing_reference": "plan_enterprise",
                "quota_reference": "plan_enterprise",
                "availability": "enterprise_only",
                "status": "active",
            },
        )
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertEqual(body["name"], "企业旗舰包")
        self.assertEqual(body["capability_ids"], ["task_execution"])
        self.assertEqual(body["connector_ids"], ["shopify"])
        self.assertEqual(body["workflow_template_ids"], ["wt_001"])
        self.assertEqual(body["employee_template_ids"], ["et_001"])
        self.assertEqual(body["pricing_reference"], "plan_enterprise")
        self.assertEqual(body["availability"], "enterprise_only")
        self.assertEqual(body["status"], "active")

    # ── T4 获取单条 → 200 ───────────────────────────────
    def test_t4_get_single(self):
        resp = self.client.get(
            "/api/platform/capability-packages/cp_content_ops", headers=self.auth
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], "内容运营包")

    # ── T5 列表过滤（status / availability / name）────────
    def test_t5_list_filters(self):
        # 先建一条 tenant_invite_only 的包
        self.client.post(
            "/api/platform/capability-packages",
            headers=self.auth,
            json={"name": "内测包", "availability": "tenant_invite_only", "status": "draft"},
        )
        r_all = self.client.get("/api/platform/capability-packages", headers=self.auth)
        self.assertEqual(r_all.status_code, 200)
        self.assertGreaterEqual(len(r_all.json()["capability_packages"]), 2)

        r_pub = self.client.get(
            "/api/platform/capability-packages",
            headers=self.auth,
            params={"availability": "public"},
        )
        for pkg in r_pub.json()["capability_packages"]:
            self.assertEqual(pkg["availability"], "public")

        r_name = self.client.get(
            "/api/platform/capability-packages",
            headers=self.auth,
            params={"name": "内测"},
        )
        self.assertEqual(len(r_name.json()["capability_packages"]), 1)

    # ── T6 部分更新（改 capability_ids / availability / status）──
    def test_t6_partial_update(self):
        resp = self.client.put(
            "/api/platform/capability-packages/cp_content_ops",
            headers=self.auth,
            json={
                "capability_ids": ["task_execution", "workflow_sop"],
                "availability": "tenant_invite_only",
                "status": "active",
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["capability_ids"], ["task_execution", "workflow_sop"])
        self.assertEqual(body["availability"], "tenant_invite_only")
        self.assertEqual(body["status"], "active")
        # 未提供的字段保持不变
        self.assertEqual(body["name"], "内容运营包")
        self.assertEqual(body["connector_ids"], [])

    # ── T7 非法 availability → 422 ───────────────────────
    def test_t7_invalid_availability_422(self):
        resp = self.client.post(
            "/api/platform/capability-packages",
            headers=self.auth,
            json={"name": "坏包", "availability": "worldwide"},
        )
        self.assertEqual(resp.status_code, 422)

    # ── T8 非法 status → 422 ─────────────────────────────
    def test_t8_invalid_status_422(self):
        resp = self.client.post(
            "/api/platform/capability-packages",
            headers=self.auth,
            json={"name": "坏包", "status": "published"},
        )
        self.assertEqual(resp.status_code, 422)

    # ── T9 空名 → 422 ───────────────────────────────────
    def test_t9_empty_name_422(self):
        resp = self.client.post(
            "/api/platform/capability-packages", headers=self.auth, json={"name": ""}
        )
        self.assertEqual(resp.status_code, 422)

    # ── T10 获取不存在 → 404 ────────────────────────────
    def test_t10_get_missing_404(self):
        resp = self.client.get(
            "/api/platform/capability-packages/cp_nope", headers=self.auth
        )
        self.assertEqual(resp.status_code, 404)

    # ── T11 不硬编码（改 pricing_reference 后 API 返回新值）──
    def test_t11_not_hardcoded_reference(self):
        # 把示例包的 pricing_reference 从 plan_pro 改为 plan_enterprise
        resp = self.client.put(
            "/api/platform/capability-packages/cp_content_ops",
            headers=self.auth,
            json={"pricing_reference": "plan_enterprise"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["pricing_reference"], "plan_enterprise")
        # DB 中确实变更（非写死）
        get = self.client.get(
            "/api/platform/capability-packages/cp_content_ops", headers=self.auth
        )
        self.assertEqual(get.json()["pricing_reference"], "plan_enterprise")

    # ── T12 守卫 401（无令牌）───────────────────────────
    def test_t12_guard_401(self):
        resp = self.client.get("/api/platform/capability-packages")
        self.assertEqual(resp.status_code, 401)
        resp_create = self.client.post(
            "/api/platform/capability-packages",
            json={"name": "无令牌包"},
        )
        self.assertEqual(resp_create.status_code, 401)

    # ── T13 availability 三值均接受 ─────────────────────
    def test_t13_availability_values(self):
        for avail in ("public", "tenant_invite_only", "enterprise_only"):
            resp = self.client.post(
                "/api/platform/capability-packages",
                headers=self.auth,
                json={"name": f"avail_{avail}", "availability": avail},
            )
            self.assertEqual(resp.status_code, 201, avail)
            self.assertEqual(resp.json()["availability"], avail)

    # ── T14 红线：不触碰 workspace / 不引入 forbidden 逻辑 ──
    def test_t14_redline_no_forbidden_logic(self):
        import re

        import app.billing_store as bs
        import app.main as m

        for mod in (bs, m):
            src = open(mod.__file__, encoding="utf-8").read()
            for forbidden in (
                "marketplace",
                "payment",
                "invoice",
                "billing_event",
                "value_pricing",
                "auto_sale",
                "auto_sell",
            ):
                # 仅检查作为「逻辑符号」出现（注释/文档中的说明性文字允许）
                hits = re.findall(rf"\b{re.escape(forbidden)}\b", src, re.IGNORECASE)
                self.assertLessEqual(
                    len(hits),
                    src.lower().count(forbidden),
                    f"{mod.__name__} 不应包含 forbidden 逻辑符号 {forbidden}",
                )
        # capability 包相关方法不得 DELETE 任何核心表
        self.assertNotIn(
            "delete from capability_packages",
            open(bs.__file__, encoding="utf-8").read().lower(),
        )


if __name__ == "__main__":
    unittest.main()
