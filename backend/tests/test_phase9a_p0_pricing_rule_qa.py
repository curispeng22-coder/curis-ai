"""Phase-9A P0 Subscription Pricing Rule —— QA 独立验证套件（Edward / software-qa-engineer）。

本文件由 QA 独立编写，**不依赖**工程师的 ``test_phase9a_p0_pricing_rule.py``（T1–T11），
对契约（docs/contracts/pricing-rule-contract.md）与实现设计蓝图做**二次验证**
（defense-in-depth），侧重工程师未覆盖的边界与集成路径：

  - DDL 契约：pricing_rules 列结构 + DB 层 CHECK 约束（直接 SQL 越界插入应被拒）
  - seed 完整性：pr_default_free / pr_default_pro / 无 Enterprise 规则 / 镜像列落地
  - BillingStore 单元：create / list(过滤) / get_active(as_of 时间旅行 + 边界) /
    新覆盖旧且历史保留 / 状态机 / 金额锁定 / 空更新幂等 / 不存在→KeyError
  - 镜像同步：sync=True 写回、sync=False 不写、Enterprise 不覆盖
  - 非法枚举（create 三枚举 + DB CHECK 兜底）
  - HTTP 集成：GET/POST/PUT 正常往返、PUT 不存在→404、非法枚举→422、admin 守卫→401

运行：backend/.venv/bin/python -m pytest tests/test_phase9a_p0_pricing_rule_qa.py -q

注（契约偏差，非源码 bug）：契约 §4 写「非 admin → 403」，但 ``_require_platform_admin``
（main.py:1068）是平台全路由共享守卫，统一返回 **401**（与全部既有 /api/platform/* 一致）。
本套件按真实强制行为断言 401，并将此契约文档措辞缺陷单独回报给架构师修正。
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


class Phase9AP0PricingRuleQATest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a_p0_qa.sqlite")
        # create_app 内部调用 database.initialize()：建表 + pricing_rules DDL +
        # plans 镜像列 ALTER + Free/Pro 默认订阅价 seed。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── DDL 契约 ───────────────────────────────────────────────────
    def test_qa_ddl_columns_present(self):
        """pricing_rules 表含契约 §1 全部 12 列。"""
        expected = {
            "pricing_rule_id", "subject_type", "pricing_type", "plan_id",
            "amount", "currency", "billing_cycle", "effective_start",
            "effective_end", "status", "created_at", "updated_at",
        }
        with self.db.connect() as conn:
            cols = {r["name"] for r in conn.execute("pragma table_info(pricing_rules)")}
        self.assertTrue(expected.issubset(cols), f"缺失列: {expected - cols}")

    def test_qa_ddl_check_rejects_illegal_subject_type(self):
        """DB 层 CHECK 约束：直接插入非法 subject_type 应被拒（IntegrityError）。"""
        with self.db.connect() as conn:
            with self.assertRaises(Exception):
                conn.execute(
                    "insert into pricing_rules "
                    "(pricing_rule_id, subject_type, pricing_type, plan_id, amount, "
                    " currency, billing_cycle, effective_start, status) "
                    "values ('pr_x', 'bogus', 'fixed', 'plan_pro', 1, 'USD', "
                    " 'month', '2025-01-01T00:00:00Z', 'draft')"
                )

    # ── seed 完整性 ────────────────────────────────────────────────
    def test_qa_seed_free_and_pro_active(self):
        free = self.billing.get_active_pricing_rule("plan_free")
        pro = self.billing.get_active_pricing_rule("plan_pro")
        self.assertIsNotNone(free)
        self.assertEqual(free["amount"], 0.0)
        self.assertEqual(free["currency"], "USD")
        self.assertEqual(free["billing_cycle"], "month")
        self.assertIsNotNone(pro)
        self.assertEqual(pro["amount"], 99.0)

    def test_qa_seed_no_enterprise_rule(self):
        ent = self.billing.get_active_pricing_rule("plan_enterprise")
        self.assertIsNone(ent)
        all_ent = self.billing.list_pricing_rules(plan_id="plan_enterprise")
        self.assertEqual(all_ent, [])

    def test_qa_seed_mirror_columns(self):
        with self.db.connect() as conn:
            free = conn.execute(
                "select price, price_currency, billing_cycle from plans where plan_id='plan_free'"
            ).fetchone()
            pro = conn.execute(
                "select price, price_currency, billing_cycle from plans where plan_id='plan_pro'"
            ).fetchone()
            ent = conn.execute(
                "select price from plans where plan_id='plan_enterprise'"
            ).fetchone()
        self.assertEqual((free["price"], free["price_currency"], free["billing_cycle"]), (0, "USD", "month"))
        self.assertEqual((pro["price"], pro["price_currency"], pro["billing_cycle"]), (99, "USD", "month"))
        self.assertIsNone(ent["price"])

    # ── create + list 过滤 ─────────────────────────────────────────
    def test_qa_create_returns_full_dto(self):
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
        self.assertTrue(rule["pricing_rule_id"].startswith("pr_"))
        self.assertEqual(rule["amount"], 120.0)
        self.assertIsInstance(rule["amount"], float)
        # 全部 12 字段齐备
        for key in ("pricing_rule_id", "subject_type", "pricing_type", "plan_id",
                    "amount", "currency", "billing_cycle", "effective_start",
                    "effective_end", "status", "created_at", "updated_at"):
            self.assertIn(key, rule)

    def test_qa_list_filters(self):
        self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=120.0, effective_start="2025-01-01T00:00:00Z", status="draft",
        )
        # 仅按 plan_id
        by_plan = self.billing.list_pricing_rules(plan_id="plan_pro")
        self.assertTrue(all(r["plan_id"] == "plan_pro" for r in by_plan))
        # 仅按 status
        drafts = self.billing.list_pricing_rules(status="draft")
        self.assertTrue(all(r["status"] == "draft" for r in drafts))
        # 组合过滤
        combo = self.billing.list_pricing_rules(plan_id="plan_pro", status="draft")
        self.assertTrue(all(r["plan_id"] == "plan_pro" and r["status"] == "draft" for r in combo))
        # 无匹配
        none = self.billing.list_pricing_rules(plan_id="plan_enterprise", status="active")
        self.assertEqual(none, [])

    # ── active 解析：时间旅行 + 边界 ───────────────────────────────
    def test_qa_active_resolution_time_travel(self):
        # seed pro 生效于 2024-01-01，永久（effective_end=NULL）
        before = self.billing.get_active_pricing_rule("plan_pro", as_of="2023-06-01T00:00:00Z")
        self.assertIsNone(before, "生效前不应解析出 active 规则")
        during = self.billing.get_active_pricing_rule("plan_pro", as_of="2024-06-01T00:00:00Z")
        self.assertIsNotNone(during)
        self.assertEqual(during["amount"], 99.0)
        future = self.billing.get_active_pricing_rule("plan_pro", as_of="2099-01-01T00:00:00Z")
        self.assertIsNotNone(future, "永久生效（effective_end=NULL）应持续解析")

    def test_qa_active_resolution_expiry_boundary(self):
        # 新建一条限时 active 固定价（2024-06 ~ 2024-12），会令 seed 过期
        self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=149.0, effective_start="2024-06-01T00:00:00Z",
            effective_end="2024-12-31T00:00:00Z", status="active",
        )
        inside = self.billing.get_active_pricing_rule("plan_pro", as_of="2024-08-01T00:00:00Z")
        self.assertIsNotNone(inside)
        self.assertEqual(inside["amount"], 149.0)
        # 窗口结束后：新规则已过期、seed 也已过期 → None
        after = self.billing.get_active_pricing_rule("plan_pro", as_of="2025-02-01T00:00:00Z")
        self.assertIsNone(after)
        # 窗口开始前：新规则未生效、seed 已过期 → None
        before = self.billing.get_active_pricing_rule("plan_pro", as_of="2024-02-01T00:00:00Z")
        self.assertIsNone(before)

    # ── 新覆盖旧（effective_start 排序）+ 历史保留 ─────────────────
    def test_qa_new_overrides_old_by_effective_start(self):
        self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=129.0, effective_start="2025-01-01T00:00:00Z", status="active",
        )
        new_rule = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=149.0, effective_start="2025-06-01T00:00:00Z", status="active",
        )
        active = self.billing.get_active_pricing_rule("plan_pro")
        self.assertEqual(active["pricing_rule_id"], new_rule["pricing_rule_id"])
        self.assertEqual(active["amount"], 149.0)

    def test_qa_history_preserved_not_deleted(self):
        old = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=129.0, effective_start="2025-01-01T00:00:00Z", status="active",
        )
        self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=149.0, effective_start="2025-06-01T00:00:00Z", status="active",
        )
        # 旧记录仍存在且被置 expired（未被物理删除）
        expired = self.billing.list_pricing_rules(plan_id="plan_pro", status="expired")
        self.assertTrue(any(r["pricing_rule_id"] == old["pricing_rule_id"] for r in expired))
        old_row = [r for r in expired if r["pricing_rule_id"] == old["pricing_rule_id"]][0]
        self.assertEqual(old_row["status"], "expired")
        self.assertIsNotNone(old_row["effective_end"], "旧规则应回填 effective_end")
        # 该 plan 的规则总数 = 1(seed) + 2(新建) = 3，未删任何一条
        total = self.billing.list_pricing_rules(plan_id="plan_pro")
        self.assertEqual(len(total), 3)

    # ── 状态机 ─────────────────────────────────────────────────────
    def test_qa_status_transitions(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=130.0, effective_start="2025-01-01T00:00:00Z", status="draft",
        )
        rid = rule["pricing_rule_id"]
        self.assertEqual(self.billing.update_pricing_rule(rid, status="active")["status"], "active")
        self.assertEqual(self.billing.update_pricing_rule(rid, status="expired")["status"], "expired")
        self.assertEqual(self.billing.update_pricing_rule(rid, status="disabled")["status"], "disabled")

    # ── 金额锁定 / 空更新 / 不存在 ─────────────────────────────────
    def test_qa_active_amount_locked(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=130.0, effective_start="2025-01-01T00:00:00Z", status="active",
        )
        with self.assertRaises(ValueError):
            self.billing.update_pricing_rule(rule["pricing_rule_id"], amount=200.0)

    def test_qa_draft_amount_mutable(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=130.0, effective_start="2025-01-01T00:00:00Z", status="draft",
        )
        updated = self.billing.update_pricing_rule(rule["pricing_rule_id"], amount=155.0)
        self.assertEqual(updated["amount"], 155.0)

    def test_qa_update_no_fields_idempotent(self):
        rule = self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=130.0, effective_start="2025-01-01T00:00:00Z", status="draft",
        )
        same = self.billing.update_pricing_rule(rule["pricing_rule_id"])
        self.assertEqual(same["amount"], 130.0)
        self.assertEqual(same["pricing_rule_id"], rule["pricing_rule_id"])

    def test_qa_update_missing_rule_keyerror(self):
        with self.assertRaises(KeyError):
            self.billing.update_pricing_rule("pr_does_not_exist", status="active")

    # ── 镜像同步 ───────────────────────────────────────────────────
    def test_qa_mirror_sync_true_writes_false_does_not(self):
        before = self.billing.get_plan_pricing("plan_pro", sync_mirror=False)
        self.assertEqual(before["mirror_price"], 99.0)  # seed 落地值
        # 新 active 规则 149，sync=True 应写回 plans.price
        self.billing.create_pricing_rule(
            plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
            amount=149.0, effective_start="2025-06-01T00:00:00Z", status="active",
        )
        synced = self.billing.get_plan_pricing("plan_pro", sync_mirror=True)
        self.assertEqual(synced["mirror_price"], 149.0)
        with self.db.connect() as conn:
            price = conn.execute("select price from plans where plan_id='plan_pro'").fetchone()["price"]
        self.assertEqual(price, 149.0)

    def test_qa_mirror_sync_enterprise_keeps_null(self):
        view = self.billing.get_plan_pricing("plan_enterprise", sync_mirror=True)
        self.assertIsNone(view["active_rule"])
        self.assertIsNone(view["mirror_price"])  # 无 active 规则时不覆盖镜像列
        with self.db.connect() as conn:
            price = conn.execute("select price from plans where plan_id='plan_enterprise'").fetchone()["price"]
        self.assertIsNone(price)

    # ── 非法枚举 ───────────────────────────────────────────────────
    def test_qa_invalid_enum_on_create(self):
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro", subject_type="bogus", pricing_type="fixed",
                amount=10.0, effective_start="2025-01-01T00:00:00Z",
            )
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro", subject_type="subscription", pricing_type="bogus",
                amount=10.0, effective_start="2025-01-01T00:00:00Z",
            )
        with self.assertRaises(ValueError):
            self.billing.create_pricing_rule(
                plan_id="plan_pro", subject_type="subscription", pricing_type="fixed",
                amount=10.0, effective_start="2025-01-01T00:00:00Z", status="bogus",
            )

    # ── HTTP 集成 ──────────────────────────────────────────────────
    def test_qa_http_get_list(self):
        resp = self.client.get("/api/platform/pricing-rules", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("pricing_rules", body)
        self.assertIsInstance(body["pricing_rules"], list)
        self.assertTrue(any(r["plan_id"] == "plan_pro" for r in body["pricing_rules"]))

    def test_qa_http_post_create(self):
        payload = {
            "plan_id": "plan_pro",
            "subject_type": "subscription",
            "pricing_type": "fixed",
            "amount": 110.0,
            "currency": "USD",
            "billing_cycle": "month",
            "effective_start": "2025-03-01T00:00:00Z",
            "status": "draft",
        }
        resp = self.client.post("/api/platform/pricing-rules", json=payload, headers=self.auth)
        self.assertEqual(resp.status_code, 201)
        created = resp.json()
        self.assertIn("pricing_rule_id", created)
        self.assertEqual(created["amount"], 110.0)
        # 后续 GET 可见
        listed = self.client.get("/api/platform/pricing-rules?plan_id=plan_pro", headers=self.auth)
        ids = [r["pricing_rule_id"] for r in listed.json()["pricing_rules"]]
        self.assertIn(created["pricing_rule_id"], ids)

    def test_qa_http_put_update_and_404(self):
        payload = {
            "plan_id": "plan_pro", "amount": 120.0,
            "effective_start": "2025-03-01T00:00:00Z", "status": "draft",
        }
        created = self.client.post("/api/platform/pricing-rules", json=payload, headers=self.auth).json()
        rid = created["pricing_rule_id"]
        upd = self.client.put(
            f"/api/platform/pricing-rules/{rid}", json={"status": "active"}, headers=self.auth
        )
        self.assertEqual(upd.status_code, 200)
        self.assertEqual(upd.json()["status"], "active")
        # 不存在 → 404
        missing = self.client.put(
            "/api/platform/pricing-rules/pr_missing", json={"status": "active"}, headers=self.auth
        )
        self.assertEqual(missing.status_code, 404)

    def test_qa_http_post_invalid_enum_422(self):
        payload = {
            "plan_id": "plan_pro", "amount": 10.0,
            "effective_start": "2025-01-01T00:00:00Z", "status": "bogus",
        }
        resp = self.client.post("/api/platform/pricing-rules", json=payload, headers=self.auth)
        self.assertEqual(resp.status_code, 422)

    def test_qa_http_plan_pricing(self):
        resp = self.client.get("/api/platform/plans/plan_pro/pricing", headers=self.auth)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["plan_id"], "plan_pro")
        self.assertIn("active_rule", body)
        self.assertIn("mirror_price", body)
        self.assertIsNotNone(body["active_rule"])

    # ── admin 守卫（契约偏差：真实返回 401，非 403）────────────────
    def test_qa_admin_guard_returns_401(self):
        # GET：无令牌 / 错误令牌 → 401
        self.assertEqual(
            self.client.get("/api/platform/pricing-rules").status_code, 401
        )
        self.assertEqual(
            self.client.get(
                "/api/platform/pricing-rules",
                headers={"Authorization": "Bearer wrong"},
            ).status_code,
            401,
        )
        # POST：合法 Body 但无令牌 → 守卫拦截 → 401（Body 先解析，守卫在其后）
        body = {"plan_id": "plan_pro", "amount": 10.0, "effective_start": "2025-01-01T00:00:00Z"}
        self.assertEqual(
            self.client.post("/api/platform/pricing-rules", json=body).status_code, 401
        )
        # 带令牌正常放行
        self.assertEqual(
            self.client.get("/api/platform/pricing-rules", headers=self.auth).status_code, 200
        )


if __name__ == "__main__":
    unittest.main()
