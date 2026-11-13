"""Phase-9A P1 QuotaRule Configuration —— 工程师实现验证套件（T1–T15 核心）。

本文件由工程师编写，覆盖 docs/design/phase9a-p1-quota-implementation-design.md §9
测试矩阵。所有端点均受 ``_require_platform_admin`` 守卫；quota_rules 为计划级配额
权威来源，per-tenant ``quotas`` 实例层不变。不触 Workspace / Credential Vault /
Shared Contract / Employee Runtime / Usage Event 写入。数值均为可改写占位（非写死）。

运行：backend/.venv/bin/python -m pytest tests/test_quota_rules.py -q
"""

from __future__ import annotations

import inspect
import os
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.billing_store import BillingStore
from app.database import Database
from app.main import create_app
from fastapi.testclient import TestClient

_ADMIN = "platform-admin-dev"


class Phase9AP1QuotaRuleTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a_p1.sqlite")
        # create_app 内部调用 database.initialize()：建表 + pricing_rules DDL +
        # plans 镜像列 ALTER + Free/Pro 默认订阅价 seed + quota_rules DDL + 15 条 seed。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── T1 建表幂等（重复 initialize 不报错、表存在、部分唯一索引生效）────
    def test_t1_table_idempotent(self):
        # 再跑一次 initialize（已建表 + 已 seed），应安全幂等。
        self.db.initialize()
        with self.db.connect() as conn:
            names = {
                r["name"]
                for r in conn.execute(
                    "select name from sqlite_master where type in ('table','index')"
                ).fetchall()
            }
        self.assertIn("quota_rules", names)
        self.assertIn("idx_quota_rules_plan_type_active", names)
        self.assertIn("idx_quota_rules_plan", names)
        self.assertIn("idx_quota_rules_status", names)

    # ── T2 seed 幂等（15 条 active，每 plan+type 仅一条 active）──────────
    def test_t2_seed_idempotent(self):
        # 再跑一次 initialize，seed 不应重复插入（insert or ignore）。
        self.db.initialize()
        active = self.billing.list_quota_rules(status="active")
        self.assertEqual(len(active), 15)
        # 每 (plan_id, quota_type) 仅一条 active（部分唯一索引强制）。
        seen = {(r["plan_id"], r["quota_type"]) for r in active}
        self.assertEqual(len(seen), 15)

    # ── T3 创建数值型规则 → 201 ─────────────────────────────────────────
    def test_t3_create_numeric_rule(self):
        resp = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": "plan_pro",
                "quota_type": "token_limit",
                "limit_value": 123456,
                "is_unlimited": False,
                "period": "monthly",
                "enforcement_mode": "notify",
                "status": "active",
            },
        )
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertIn("quota_rule_id", body)
        self.assertTrue(body["quota_rule_id"].startswith("qr_"))
        self.assertEqual(body["is_unlimited"], False)
        self.assertEqual(body["limit_value"], 123456)
        # 旧 active 同 plan+type 应被置 disabled（覆盖语义）。
        old = self.billing.list_quota_rules(
            plan_id="plan_pro", quota_type="token_limit", status="disabled"
        )
        self.assertTrue(
            any(r["quota_rule_id"] == "qr_pro_token" for r in old)
        )

    # ── T4 创建准入型规则（capability_limit + source_scope）──────────────
    def test_t4_create_admission_rule(self):
        resp = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": "plan_pro",
                "quota_type": "capability_limit",
                "source_scope": ["official", "tenant_private"],
                "enforcement_mode": "block",
                "status": "active",
            },
        )
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertIsNone(body["limit_value"])
        self.assertEqual(body["source_scope"], ["official", "tenant_private"])

    # ── T5 非法枚举 → 422 ───────────────────────────────────────────────
    def test_t5_invalid_enum_422(self):
        for bad in (
            {"plan_id": "plan_pro", "quota_type": "bogus"},
            {"plan_id": "plan_pro", "quota_type": "token_limit", "enforcement_mode": "bogus"},
            {"plan_id": "plan_pro", "quota_type": "token_limit", "period": "bogus"},
            {"plan_id": "plan_pro", "quota_type": "token_limit", "status": "bogus"},
        ):
            resp = self.client.post(
                "/api/platform/quota-rules", headers=self.auth, json=bad
            )
            self.assertEqual(
                resp.status_code,
                422,
                f"非法枚举 {bad} 应返回 422，实际 {resp.status_code}: {resp.text}",
            )

    # ── T6 覆盖语义（store 层：激活新规则，旧 active → disabled）─────────
    def test_t6_cover_semantics(self):
        old = self.billing.create_quota_rule(
            plan_id="plan_free",
            quota_type="workflow_limit",
            is_unlimited=True,
            status="active",
        )
        new = self.billing.create_quota_rule(
            plan_id="plan_free",
            quota_type="workflow_limit",
            limit_value=999,
            status="active",
        )
        active = self.billing.get_active_quota_rule("plan_free", "workflow_limit")
        self.assertEqual(active["quota_rule_id"], new["quota_rule_id"])
        disabled = self.billing.list_quota_rules(
            plan_id="plan_free", quota_type="workflow_limit", status="disabled"
        )
        self.assertTrue(
            any(r["quota_rule_id"] == old["quota_rule_id"] for r in disabled)
        )

    # ── T7 列表过滤（plan + status）─────────────────────────────────────
    def test_t7_list_filter(self):
        listed = self.billing.list_quota_rules(plan_id="plan_pro", status="active")
        self.assertTrue(listed)
        self.assertTrue(all(r["plan_id"] == "plan_pro" for r in listed))
        self.assertTrue(all(r["status"] == "active" for r in listed))
        # enforcement_mode 过滤
        blocked = self.billing.list_quota_rules(enforcement_mode="block")
        self.assertTrue(blocked)
        self.assertTrue(all(r["enforcement_mode"] == "block" for r in blocked))

    # ── T8 更新部分字段（updated_at 刷新、未传字段不变）──────────────────
    def test_t8_update_partial(self):
        rule = self.billing.create_quota_rule(
            plan_id="plan_pro",
            quota_type="employee_seat_limit",
            limit_value=10,
            status="draft",
        )
        rid = rule["quota_rule_id"]
        before = rule["updated_at"]
        # SQLite current_timestamp 仅秒级精度：间隔 >1s 保证 updated_at 刷新可见。
        time.sleep(1.05)
        updated = self.billing.update_quota_rule(
            rid, limit_value=20, status="active"
        )
        self.assertEqual(updated["limit_value"], 20)
        self.assertEqual(updated["status"], "active")
        self.assertEqual(updated["is_unlimited"], False)  # 未传字段保持默认
        self.assertNotEqual(updated["updated_at"], before)

    # ── T9 已 active 禁止改 limit_value → 422 ───────────────────────────
    def test_t9_active_limit_locked(self):
        rid = "qr_pro_token"  # seed 中已是 active
        resp = self.client.put(
            f"/api/platform/quota-rules/{rid}",
            headers=self.auth,
            json={"limit_value": 1},
        )
        self.assertEqual(resp.status_code, 422)
        # store 层同样抛 ValueError
        with self.assertRaises(ValueError):
            self.billing.update_quota_rule(rid, limit_value=1)

    # ── T10 不存在资源 → 404 ────────────────────────────────────────────
    def test_t10_not_found_404(self):
        resp = self.client.put(
            "/api/platform/quota-rules/does_not_exist",
            headers=self.auth,
            json={"status": "disabled"},
        )
        self.assertEqual(resp.status_code, 404)
        with self.assertRaises(KeyError):
            self.billing.update_quota_rule("does_not_exist", status="disabled")

    # ── T11 套餐配额预览 GET /plans/{id}/quotas ─────────────────────────
    def test_t11_plan_quota_preview(self):
        resp = self.client.get(
            "/api/platform/plans/plan_free/quotas", headers=self.auth
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["plan_id"], "plan_free")
        # Free 套餐应有 5 条配额规则（5 类各一条 active）。
        self.assertEqual(len(body["quota_rules"]), 5)
        types = {r["quota_type"] for r in body["quota_rules"]}
        self.assertEqual(
            types,
            {
                "token_limit",
                "employee_seat_limit",
                "workflow_limit",
                "capability_limit",
                "connector_limit",
            },
        )

    # ── T12 不硬编码（改 DB 中 seed 值，API 返回新值）────────────────────
    def test_t12_not_hardcoded(self):
        # seed 值来自 DB（非写死常量）：直接改 DB 中某规则 limit，API 应返回新值。
        with self.db.connect() as conn:
            conn.execute(
                "update quota_rules set limit_value=424242 where quota_rule_id='qr_free_token'"
            )
        # 通过 store 读取
        rules = self.billing.list_quota_rules(
            plan_id="plan_free", quota_type="token_limit"
        )
        self.assertEqual(rules[0]["limit_value"], 424242)
        # 通过 API 读取
        resp = self.client.get(
            "/api/platform/plans/plan_free/quotas", headers=self.auth
        )
        tokens = [
            r
            for r in resp.json()["quota_rules"]
            if r["quota_rule_id"] == "qr_free_token"
        ]
        self.assertEqual(tokens[0]["limit_value"], 424242)

    # ── T13 admin-only 守卫（缺/错令牌一律 401；POST/PUT 带合法 Body 无令牌 401）──
    def test_t13_admin_only_guard(self):
        get_endpoints = [
            "GET /api/platform/quota-rules",
            "GET /api/platform/plans/plan_pro/quotas",
        ]
        for spec in get_endpoints:
            method, url = spec.split(" ", 1)
            resp = self.client.request(method, url)
            self.assertEqual(
                resp.status_code, 401, f"{spec} 无令牌应返回 401，实际 {resp.status_code}"
            )
            resp_bad = self.client.request(
                method, url, headers={"Authorization": "Bearer wrong-token"}
            )
            self.assertEqual(
                resp_bad.status_code, 401, f"{spec} 错误令牌应返回 401，实际 {resp_bad.status_code}"
            )

        write_endpoints = [
            ("POST", "/api/platform/quota-rules"),
            ("PUT", "/api/platform/quota-rules/qr_pro_token"),
        ]
        for method, url in write_endpoints:
            # 带合法 Body 但无令牌 → 守卫拦截 → 401
            body = {
                "plan_id": "plan_pro",
                "quota_type": "token_limit",
                "limit_value": 10,
            }
            resp_body = self.client.request(method, url, json=body)
            self.assertEqual(
                resp_body.status_code,
                401,
                f"{method} {url} 合法 Body+无令牌应返回 401，实际 {resp_body.status_code}",
            )

    # ── T14 状态机（draft→active→disabled，get_active 仅返回 active）────
    def test_t14_state_machine(self):
        # 用全新 plan 避免与三档 seed 的 active 规则相互干扰。
        plan = self.billing.create_plan(
            plan_code="t14plan", name="T14", tier="pro", status="active"
        )
        plan_id = plan["plan_id"]
        rule = self.billing.create_quota_rule(
            plan_id=plan_id,
            quota_type="connector_limit",
            limit_value=5,
            status="draft",
        )
        rid = rule["quota_rule_id"]
        self.assertIsNone(
            self.billing.get_active_quota_rule(plan_id, "connector_limit")
        )
        activated = self.billing.update_quota_rule(rid, status="active")
        self.assertEqual(activated["status"], "active")
        active = self.billing.get_active_quota_rule(plan_id, "connector_limit")
        self.assertEqual(active["quota_rule_id"], rid)
        disabled = self.billing.update_quota_rule(rid, status="disabled")
        self.assertEqual(disabled["status"], "disabled")
        self.assertIsNone(
            self.billing.get_active_quota_rule(plan_id, "connector_limit")
        )

    # ── T15 禁止清单代码审查（新 QuotaRule 方法无 BillingEvent/Payment/
    #     Invoice/Marketplace/ValuePricing 逻辑；marketplace 仅作数据源值）────
    def test_t15_no_forbidden_logic(self):
        import app.billing_store as bs

        targets = [
            bs.BillingStore.create_quota_rule,
            bs.BillingStore.update_quota_rule,
            bs.BillingStore.list_quota_rules,
            bs.BillingStore.get_active_quota_rule,
            bs.BillingStore._quota_rule_dto,
            bs.BillingStore._get_quota_rule_row,
            bs.BillingStore._expire_old_active_quota_rules,
        ]
        forbidden = [
            "payment",
            "invoice",
            "billing_event",
            "ValuePricing",
            "value_event",
        ]
        for fn in targets:
            src = inspect.getsource(fn)
            for word in forbidden:
                self.assertNotIn(
                    word, src, f"{fn.__name__} 不应包含禁止逻辑关键字 {word!r}"
                )


if __name__ == "__main__":
    unittest.main()
