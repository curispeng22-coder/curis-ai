"""Phase-9A P0b 增量增强 —— QA 独立验证套件（不依赖工程师 T12/T13）。

本文件由 QA 工程师严过关编写，用于对「update_pricing_rule 在激活为 active+fixed
时自动把同 plan 旧 active 固定价规则置 expired」这一增强做**独立**语义验证。

覆盖场景：
  A. 主路径：同 plan 先有 active+fixed 规则 A；新建 draft+fixed 规则 B 后
     update(B, status='active') → A 变 expired、effective_end 非空、A 物理仍
     存在、get_active_pricing_rule 返回 B 且 status=='active'。
  B. 排除自身：update B 激活时，_expire_old_active_fixed_rules 排除 B 自身；
     同 plan 下别的 active 固定价（C）被正确置 expired，B 自身保持 active。
  C. 不触发边界：规则当前非 active 且更新后 status≠active（如改 amount 但保持
     draft）→ 同 plan 旧 active 固定价不受影响。
  D. 已 active+fixed 改非状态字段：仅改 currency/billing_cycle → trigger_cover
     为 False，同 plan active 固定价数量不增不减、无新 churn。
  E. 不删历史：覆盖仅改状态，pricing_rules 表行数在覆盖前后只增不减（本场景恒等）。

红线（代码级，另由 grep 核验，不在本套件内）：
  * 不 import / 调用 workspace runtime / credential_vault / workflow_runtime /
    employee / payment / invoice / marketplace / promotion / value pricing。
  * 不 DELETE 作用于 pricing_rules。
  * 所有 SQL 用 ? 占位。

运行：
  backend/.venv/bin/python -m pytest tests/test_phase9a_p0b_cover_qa.py -q
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.billing_store import BillingStore
from app.database import Database
from app.main import create_app

_ADMIN = "platform-admin-dev"


def _count_rows(db: "Database") -> int:
    with db.connect() as conn:
        return int(conn.execute("select count(*) from pricing_rules").fetchone()[0])


class Phase9AP0BCoverQATest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a_p0b.sqlite")
        # create_app 内部建表 + pricing_rules DDL + plans 镜像列 + 默认订阅价 seed。
        create_app(self.db_path)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def _new_plan(self, code: str) -> str:
        plan = self.billing.create_plan(
            plan_code=code, name=code, tier="pro", status="active"
        )
        return plan["plan_id"]

    # ── 场景 A：主路径激活覆盖（draft(fixed) → active 触发）─────────────
    def test_A_main_activation_cover(self):
        plan_id = self._new_plan("qa_a_plan")
        # A：直接 active+fixed（已生效订阅价）
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            billing_cycle="month",
            status="active",
        )
        # B：先建 draft+fixed
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            billing_cycle="month",
            status="draft",
        )

        # B 走 update 路径激活 → 触发覆盖
        b_activated = self.billing.update_pricing_rule(
            rule_b["pricing_rule_id"], status="active"
        )
        self.assertEqual(b_activated["status"], "active")

        # A 被置 expired，effective_end 回填非空
        a_after = self.billing.list_pricing_rules(
            plan_id=plan_id, status="expired"
        )
        a_row = next(
            (r for r in a_after if r["pricing_rule_id"] == rule_a["pricing_rule_id"]),
            None,
        )
        self.assertIsNotNone(a_row, "A 应被置 expired")
        self.assertEqual(a_row["status"], "expired")
        self.assertIsNotNone(a_row["effective_end"])
        self.assertNotEqual(a_row["effective_end"], "")

        # A 物理仍存在（未被删除）
        all_rows = self.billing.list_pricing_rules(plan_id=plan_id)
        self.assertTrue(
            any(r["pricing_rule_id"] == rule_a["pricing_rule_id"] for r in all_rows),
            "A 应物理存在（未被 DELETE）",
        )

        # 当前 active 固定价返回 B
        active = self.billing.get_active_pricing_rule(plan_id)
        self.assertIsNotNone(active)
        self.assertEqual(active["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(active["status"], "active")
        self.assertEqual(active["amount"], 200.0)

    # ── 场景 B：排除自身（同 plan 另有 C，激活 B 时 C 被过期、B 仍 active）──
    def test_B_exclude_self(self):
        plan_id = self._new_plan("qa_b_plan")
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            billing_cycle="month",
            status="active",
        )
        rule_c = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=150.0,
            billing_cycle="month",
            status="active",
        )
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            billing_cycle="month",
            status="draft",
        )

        self.billing.update_pricing_rule(rule_b["pricing_rule_id"], status="active")

        # 排除自身：B 自身未被误置 expired，仍为 active
        b_after = self.billing._get_pricing_rule_row(rule_b["pricing_rule_id"])
        self.assertEqual(b_after["status"], "active")

        # 同 plan 下其它 active 固定价（A、C）均被置 expired
        expired_ids = {
            r["pricing_rule_id"]
            for r in self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        }
        self.assertIn(rule_a["pricing_rule_id"], expired_ids)
        self.assertIn(rule_c["pricing_rule_id"], expired_ids)
        # 关键：B 不被包含在 expired 集合中 → 排除自身生效
        self.assertNotIn(rule_b["pricing_rule_id"], expired_ids)

        # 当前 active 固定价唯一且为 B
        active = self.billing.get_active_pricing_rule(plan_id)
        self.assertEqual(active["pricing_rule_id"], rule_b["pricing_rule_id"])

    # ── 场景 C：不触发边界（非 active→非 active，仅改金额保持 draft）─────
    def test_C_no_trigger_when_not_activating(self):
        plan_id = self._new_plan("qa_c_plan")
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            billing_cycle="month",
            status="active",
        )
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            billing_cycle="month",
            status="draft",
        )

        # 仅改 amount，status 不提供 → 保持 draft（非激活）
        updated = self.billing.update_pricing_rule(rule_b["pricing_rule_id"], amount=999.0)
        self.assertEqual(updated["status"], "draft")
        self.assertEqual(updated["amount"], 999.0)

        # 同 plan 旧 active 固定价 A 不受影响：仍 active、未产生新 expired
        a_after = self.billing._get_pricing_rule_row(rule_a["pricing_rule_id"])
        self.assertEqual(a_after["status"], "active")
        expired_ids = {
            r["pricing_rule_id"]
            for r in self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        }
        self.assertNotIn(rule_a["pricing_rule_id"], expired_ids)
        self.assertEqual(len(expired_ids), 0, "改 draft 金额不应产生任何 expired churn")

    # ── 场景 D：已 active+fixed 改非状态字段，不触发覆盖 ───────────────
    def test_D_active_fixed_non_status_no_cover(self):
        plan_id = self._new_plan("qa_d_plan")
        rule_a = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            billing_cycle="month",
            status="active",
        )
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            billing_cycle="month",
            status="active",
        )
        before_active = self.billing.list_pricing_rules(plan_id=plan_id, status="active")
        before_expired = self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        self.assertEqual(len(before_active), 1)
        self.assertEqual(before_active[0]["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(len(before_expired), 1)

        # 对 B（已 active+fixed）仅改 currency/billing_cycle
        updated = self.billing.update_pricing_rule(
            rule_b["pricing_rule_id"], currency="EUR", billing_cycle="year"
        )
        self.assertEqual(updated["status"], "active")
        self.assertEqual(updated["currency"], "EUR")
        self.assertEqual(updated["billing_cycle"], "year")

        # 更新后：active 固定价数量不增不减（仍为 B 1 条），无新 churn
        after_active = self.billing.list_pricing_rules(plan_id=plan_id, status="active")
        after_expired = self.billing.list_pricing_rules(plan_id=plan_id, status="expired")
        self.assertEqual(len(after_active), 1)
        self.assertEqual(after_active[0]["pricing_rule_id"], rule_b["pricing_rule_id"])
        self.assertEqual(len(after_expired), 1)
        self.assertEqual(after_expired[0]["pricing_rule_id"], rule_a["pricing_rule_id"])

        active = self.billing.get_active_pricing_rule(plan_id)
        self.assertEqual(active["pricing_rule_id"], rule_b["pricing_rule_id"])

    # ── 场景 E：不删历史（覆盖仅改状态，行数恒等）──────────────────────
    def test_E_no_delete_history_row_count(self):
        plan_id = self._new_plan("qa_e_plan")
        self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=100.0,
            billing_cycle="month",
            status="active",
        )
        rule_b = self.billing.create_pricing_rule(
            plan_id=plan_id,
            subject_type="subscription",
            pricing_type="fixed",
            amount=200.0,
            billing_cycle="month",
            status="draft",
        )

        before = _count_rows(self.db)
        # 基线含 seed 默认订阅价（如 plan_pro=99 active），故不固定断言为 2；
        # 只要满足「覆盖前后行数不变」即可证明未 DELETE / 未额外 INSERT。
        self.assertGreaterEqual(before, 2)

        self.billing.update_pricing_rule(rule_b["pricing_rule_id"], status="active")

        after = _count_rows(self.db)
        # 覆盖操作只 UPDATE 状态，绝不 DELETE / INSERT → 行数应相等
        self.assertEqual(after, before, "覆盖不应改变 pricing_rules 表行数（无删/无增）")


if __name__ == "__main__":
    unittest.main()
