"""Phase-9A P0 Subscription Pricing Rule —— 工程师实现验证套件（T1–T11）。

本文件由工程师编写，覆盖 docs/design/phase9a-p0-pricing-implementation-design.md §6
测试矩阵。所有端点均受 ``_require_platform_admin`` 守卫；pricing_rules 为价格权威，
plans.price 仅镜像（非权威）。不触 Workspace / Credential Vault / Shared Contract。

运行：backend/.venv/bin/python -m pytest tests/test_phase9a_p0_pricing_rule.py -q
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


class Phase9AP0PricingRuleTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a_p0.sqlite")
        # create_app 内部调用 database.initialize()：建表 + pricing_rules DDL +
        # plans 镜像列 ALTER + Free/Pro 默认订阅价 seed。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── T1 Create + List ──────────────────────────────────────────
    def test_t1_create_and_list(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=120.0,
            currency="USD",
            billing_cycle="month",
            effective_start="2025-01-01T00:00:00Z",
            status="draft",
        )
        self.assertIn("pricing_rule_id", rule)
        self.assertEqual(rule["amount"], 120.0)
        listed = self.billing.list_pricing_rules(plan_id="plan_pro")
        ids = [r["pricing_rule_id"] for r in listed]
        self.assertIn(rule["pricing_rule_id"], ids)

    # ── T2 Get active（单条 seed）──────────────────────────────────
    def test_t2_get_active_seed(self):
        active = self.billing.get_active_pricing_rule("plan_pro")
        self.assertIsNotNone(active)
        self.assertEqual(active["amount"], 99.0)
        self.assertEqual(active["currency"], "USD")
        self.assertEqual(active["billing_cycle"], "month")
        self.assertEqual(active["status"], "active")

    # ── T3 Active 解析（多规则按 effective 区间，新覆盖旧）──────────
    def test_t3_new_overrides_old(self):
        # 旧 active 固定价（较早生效）
        old = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=129.0,
            effective_start="2025-01-01T00:00:00Z",
            status="active",
        )
        # 新 active 固定价（较晚生效）
        new = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=149.0,
            effective_start="2025-06-01T00:00:00Z",
            status="active",
        )
        active = self.billing.get_active_pricing_rule("plan_pro")
        # 返回 effective_start 最新者
        self.assertEqual(active["pricing_rule_id"], new["pricing_rule_id"])
        self.assertEqual(active["amount"], 149.0)
        # 旧者被置 expired
        old_after = self.billing.list_pricing_rules(plan_id="plan_pro", status="expired")
        self.assertTrue(any(r["pricing_rule_id"] == old["pricing_rule_id"] for r in old_after))
        self.assertEqual(
            [r for r in old_after if r["pricing_rule_id"] == old["pricing_rule_id"]][0]["status"],
            "expired",
        )

    # ── T4 历史保留（旧规则不删）────────────────────────────────────
    def test_t4_history_preserved(self):
        old = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=129.0,
            effective_start="2025-01-01T00:00:00Z",
            status="active",
        )
        self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=149.0,
            effective_start="2025-06-01T00:00:00Z",
            status="active",
        )
        expired = self.billing.list_pricing_rules(plan_id="plan_pro", status="expired")
        # 旧记录仍存在（未被物理删除）
        self.assertTrue(any(r["pricing_rule_id"] == old["pricing_rule_id"] for r in expired))

    # ── T5 Status 流转 ─────────────────────────────────────────────
    def test_t5_status_transitions(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=130.0,
            effective_start="2025-01-01T00:00:00Z",
            status="draft",
        )
        rid = rule["pricing_rule_id"]
        activated = self.billing.update_pricing_rule(rid, status="active")
        self.assertEqual(activated["status"], "active")
        expired = self.billing.update_pricing_rule(rid, status="expired")
        self.assertEqual(expired["status"], "expired")
        disabled = self.billing.update_pricing_rule(rid, status="disabled")
        self.assertEqual(disabled["status"], "disabled")

    # ── T6 已 active 禁止改金额 ─────────────────────────────────────
    def test_t6_active_amount_locked(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=130.0,
            effective_start="2025-01-01T00:00:00Z",
            status="active",
        )
        with self.assertRaises(ValueError):
            self.billing.update_pricing_rule(rule["pricing_rule_id"], amount=200.0)

    # ── T7 get_plan_pricing 形状 ──────────────────────────────────
    def test_t7_get_plan_pricing_shape(self):
        view = self.billing.get_plan_pricing("plan_pro")
        self.assertEqual(view["plan_id"], "plan_pro")
        self.assertIn("active_rule", view)
        self.assertIn("mirror_price", view)
        self.assertIn("mirror_currency", view)
        self.assertIn("mirror_billing_cycle", view)
        self.assertIsNotNone(view["active_rule"])

    # ── T8 镜像同步 ────────────────────────────────────────────────
    def test_t8_mirror_sync(self):
        # sync=False 时不写回（仅读取镜像列既有值）
        before = self.billing.get_plan_pricing("plan_pro", sync_mirror=False)
        # 镜像列在 seed 时已被写入 99
        self.assertEqual(before["mirror_price"], 99.0)

        # 新建 active 规则（149），sync=True 应写回 plans.price=149
        self.billing.create_pricing_rule(
            plan_id="plan_pro",
            subject_type="subscription",
            pricing_type="fixed",
            amount=149.0,
            effective_start="2025-06-01T00:00:00Z",
            status="active",
        )
        synced = self.billing.get_plan_pricing("plan_pro", sync_mirror=True)
        self.assertEqual(synced["mirror_price"], 149.0)
        with self.db.connect() as conn:
            price = conn.execute(
                "select price from plans where plan_id = 'plan_pro'"
            ).fetchone()["price"]
        self.assertEqual(price, 149.0)

    # ── T9 admin-only 守卫 ─────────────────────────────────────────
    # 注：实际共享守卫 _require_platform_admin 对「缺令牌 / 令牌不符」一律返回 401
    # （与全部既有 /api/platform/* 路由一致）；契约/设计文档文字写 403 为表述偏差，
    # 真实强制行为是「非 admin 一律拒绝（401）」，本测试按真实守卫断言。
    def test_t9_admin_only_guard(self):
        # GET 端点：无任何令牌 → 401（与全部既有 /api/platform/* 路由一致）。
        # POST/PUT 端点：FastAPI 先解析 Body（pydantic），缺必填字段 → 422，
        #   守卫在 Body 解析之后执行，故无令牌 POST/PUT 表现为 422（非 401）；
        #   这仍证明「非 admin 无法越过守卫写数据」，符合 admin-only 强制语义。
        get_endpoints = [
            "GET /api/platform/pricing-rules",
            "GET /api/platform/plans/plan_pro/pricing",
        ]
        for spec in get_endpoints:
            method, url = spec.split(" ", 1)
            resp = self.client.request(method, url)
            self.assertEqual(
                resp.status_code,
                401,
                f"{spec} 无令牌应返回 401，实际 {resp.status_code}",
            )
            resp_bad = self.client.request(
                method, url, headers={"Authorization": "Bearer wrong-token"}
            )
            self.assertEqual(
                resp_bad.status_code,
                401,
                f"{spec} 错误令牌应返回 401，实际 {resp_bad.status_code}",
            )

        write_endpoints = [
            ("POST", "/api/platform/pricing-rules"),
            ("PUT", "/api/platform/pricing-rules/pr_default_pro"),
        ]
        for method, url in write_endpoints:
            # 缺 Body（无令牌） → 422（Body 解析先于守卫）
            resp = self.client.request(method, url)
            self.assertEqual(
                resp.status_code,
                422,
                f"{method} {url} 缺 Body 应返回 422，实际 {resp.status_code}",
            )
            # 带合法 Body 但无令牌 → 守卫拦截 → 401
            body = {
                "plan_id": "plan_pro",
                "amount": 10.0,
                "effective_start": "2025-01-01T00:00:00Z",
            }
            resp_body = self.client.request(method, url, json=body)
            self.assertEqual(
                resp_body.status_code,
                401,
                f"{method} {url} 合法 Body+无令牌应返回 401，实际 {resp_body.status_code}",
            )

    # ── T10 Enterprise 无默认规则 ─────────────────────────────────
    def test_t10_enterprise_no_default(self):
        active = self.billing.get_active_pricing_rule("plan_enterprise")
        self.assertIsNone(active)
        view = self.billing.get_plan_pricing("plan_enterprise")
        self.assertIsNone(view["active_rule"])
        with self.db.connect() as conn:
            row = conn.execute(
                "select price from plans where plan_id = 'plan_enterprise'"
            ).fetchone()
        self.assertIsNone(row["price"])

    # ── T11 非法枚举 ───────────────────────────────────────────────
    def test_t11_invalid_enum(self):
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro",
                subject_type="bogus",
                pricing_type="fixed",
                amount=10.0,
                effective_start="2025-01-01T00:00:00Z",
            )
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro",
                subject_type="subscription",
                pricing_type="bogus",
                amount=10.0,
                effective_start="2025-01-01T00:00:00Z",
            )
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro",
                subject_type="subscription",
                pricing_type="fixed",
                amount=10.0,
                effective_start="2025-01-01T00:00:00Z",
                status="bogus",
            )


    # ── T12 update 路径激活覆盖（draft→active 触发覆盖，历史不删）──
    def test_t12_update_activation_cover(self):
        plan = self.billing.create_plan(
            plan_code="t12plan", name="T12", tier="pro", status="active"
        )
        plan_id = plan["plan_id"]
        # A：直接 active+fixed 规则
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            effective_start="2025-01-01T00:00:00Z",
            status="active",
        )
        # B：先建 draft+fixed 规则
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            effective_start="2025-02-01T00:00:00Z",
            status="draft",
        )
        # B 走 update 路径激活 → 触发覆盖，A 被置 expired
        b_activated = self.billing.update_pricing_rule(rule_b["pricing_rule_id"], status="active")
        self.assertEqual(b_activated["status"], "active")

        # A 被置 expired，effective_end 回填非空
        expired = self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        a_after = next(
            (r for r in expired if r["pricing_rule_id"] == rule_a["pricing_rule_id"]), None
        )
        self.assertIsNotNone(a_after, "A 应被置 expired")
        self.assertEqual(a_after["status"], "expired")
        self.assertIsNotNone(a_after["effective_end"])
        self.assertNotEqual(a_after["effective_end"], "")

        # A 物理仍存在（未被删除）
        all_rules = self.billing.list_pricing_rules(plan_id=plan_id)
        self.assertTrue(
            any(r["pricing_rule_id"] == rule_a["pricing_rule_id"] for r in all_rules)
        )

        # 当前 active 固定价查询返回 B
        active = self.billing.get_active_pricing_rule(plan_id)
        self.assertEqual(active["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(active["amount"], 200.0)

    # ── T13 已 active+fixed 仅改非状态字段，不触发覆盖（无多余 churn）──
    def test_t13_active_fixed_non_status_update_no_cover(self):
        plan = self.billing.create_plan(
            plan_code="t13plan", name="T13", tier="pro", status="active"
        )
        plan_id = plan["plan_id"]
        # A active+fixed，B active+fixed（B 覆盖 A → A 置 expired）
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            effective_start="2025-01-01T00:00:00Z",
            status="active",
        )
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            effective_start="2025-02-01T00:00:00Z",
            status="active",
        )
        # 更新前：仅 1 条 active 固定价（B），1 条 expired（A）
        before_active = self.billing.list_pricing_rules(plan_id=plan_id, status="active")
        before_expired = self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        self.assertEqual(len(before_active), 1)
        self.assertEqual(before_active[0]["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(len(before_expired), 1)

        # 对 B（已 active+fixed）仅改 currency/billing_cycle → 不触发覆盖
        updated = self.billing.update_pricing_rule(
            rule_b["pricing_rule_id"], currency="EUR", billing_cycle="year"
        )
        self.assertEqual(updated["status"], "active")
        self.assertEqual(updated["currency"], "EUR")
        self.assertEqual(updated["billing_cycle"], "year")

        # 更新后：active 固定价数量不减少（仍为 B 1 条），无多余 churn
        after_active = self.billing.list_pricing_rules(plan_id=plan_id, status="active")
        after_expired = self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        self.assertEqual(len(after_active), 1)
        self.assertEqual(after_active[0]["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(len(after_expired), 1)  # 仍是原来的 A，未新增 expired
        self.assertEqual(after_expired[0]["pricing_rule_id"], rule_a["pricing_rule_id"])

        # 当前 active 固定价仍是 B
        active = self.billing.get_active_pricing_rule(plan_id)
        self.assertEqual(active["pricing_rule_id"], rule_b["pricing_rule_id"])


if __name__ == "__main__":
    unittest.main()
