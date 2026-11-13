"""Phase-9A P1 QuotaRule Configuration —— QA 独立验证套件（A–I + 红线静态检查）。

由 QA 工程师严过关编写，独立于工程师的 test_quota_rules.py（T1–T15）。
以契约 docs/contracts/quota-rule-contract.md 与 docs/design/phase9a-p1-quota-implementation-design.md
为断言依据，自有断言，不依赖 T1–T15。

运行：backend/.venv/bin/python -m pytest tests/test_phase9a_p1_quota_qa.py -q
"""

from __future__ import annotations

import inspect
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.billing_store import BillingStore
from app.database import Database
from app.main import create_app
from fastapi.testclient import TestClient

_ADMIN = "platform-admin-dev"

_FIVE_TYPES = {
    "token_limit",
    "employee_seat_limit",
    "workflow_limit",
    "capability_limit",
    "connector_limit",
}


class Phase9AP1QuotaRuleQATest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "qa_phase9a_p1.sqlite")
        # create_app → database.initialize()：建表 + 15 条 seed（Free/Pro/Enterprise 各 5 active）。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.billing = BillingStore(self.db)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}
        # 隔离用全新套餐（避免污染三档 seed 的部分唯一索引不变量）。
        plan = self.billing.create_plan(
            plan_code="qa_plan", name="QA Plan", tier="pro", status="active"
        )
        self.plan = plan["plan_id"]

    def tearDown(self):
        self.tmp.cleanup()

    # ── A：CRUD 主路径（创建 active → 可见 → 改 enforcement_mode → 改 limit 经 draft → 激活）──
    def test_a_crud_main_path(self):
        # 创建一条 active 规则（plan+type 唯一），确认列表可见。
        resp = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": self.plan,
                "quota_type": "token_limit",
                "limit_value": 100,
                "period": "monthly",
                "enforcement_mode": "notify",
                "status": "active",
            },
        )
        self.assertEqual(resp.status_code, 201)
        rid = resp.json()["quota_rule_id"]
        self.assertTrue(rid.startswith("qr_"))

        listed = self.client.get(
            f"/api/platform/quota-rules?plan_id={self.plan}&quota_type=token_limit",
            headers=self.auth,
        )
        ids = [r["quota_rule_id"] for r in listed.json()["quota_rules"]]
        self.assertIn(rid, ids)

        # PUT 改 enforcement_mode（active 规则允许改 enforcement_mode，limit 不动）。
        resp2 = self.client.put(
            f"/api/platform/quota-rules/{rid}",
            headers=self.auth,
            json={"enforcement_mode": "throttle"},
        )
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json()["enforcement_mode"], "throttle")
        self.assertEqual(resp2.json()["limit_value"], 100)

        # limit_value 变更需非 active：用一条 draft 规则演示完整 CRUD 更新（active 禁改 limit 见 E）。
        resp3 = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": self.plan,
                "quota_type": "workflow_limit",
                "limit_value": 50,
                "status": "draft",
            },
        )
        self.assertEqual(resp3.status_code, 201)
        rid2 = resp3.json()["quota_rule_id"]

        resp4 = self.client.put(
            f"/api/platform/quota-rules/{rid2}",
            headers=self.auth,
            json={"limit_value": 999, "enforcement_mode": "block"},
        )
        self.assertEqual(resp4.status_code, 200)
        self.assertEqual(resp4.json()["limit_value"], 999)
        self.assertEqual(resp4.json()["enforcement_mode"], "block")

        # 激活 draft → 进入 active 查询。
        resp5 = self.client.put(
            f"/api/platform/quota-rules/{rid2}",
            headers=self.auth,
            json={"status": "active"},
        )
        self.assertEqual(resp5.status_code, 200)
        active = self.billing.get_active_quota_rule(self.plan, "workflow_limit")
        self.assertEqual(active["quota_rule_id"], rid2)

    # ── B：覆盖语义（同 plan+type 激活新规则 → 旧 active 置 disabled，物理仍存在；部分唯一索引不变量）──
    def test_b_cover_semantics(self):
        old = self.billing.create_quota_rule(
            plan_id=self.plan, quota_type="token_limit", limit_value=10, status="active"
        )
        new = self.billing.create_quota_rule(
            plan_id=self.plan, quota_type="token_limit", limit_value=20, status="active"
        )

        with self.db.connect() as conn:
            old_row = conn.execute(
                "select status from quota_rules where quota_rule_id = ?",
                (old["quota_rule_id"],),
            ).fetchone()
            new_row = conn.execute(
                "select status from quota_rules where quota_rule_id = ?",
                (new["quota_rule_id"],),
            ).fetchone()

        # 旧规则被置 disabled，但物理记录仍在（非 DELETE）。
        self.assertEqual(old_row["status"], "disabled")
        self.assertEqual(new_row["status"], "active")
        self.assertIsNotNone(old_row)

        # get_active 返回新规则（B）。
        active = self.billing.get_active_quota_rule(self.plan, "token_limit")
        self.assertEqual(active["quota_rule_id"], new["quota_rule_id"])

        # 部分唯一索引不变量：每 plan+type 仅一条 active。
        with self.db.connect() as conn:
            cnt = conn.execute(
                "select count(*) as c from quota_rules "
                "where plan_id = ? and quota_type = ? and status = 'active'",
                (self.plan, "token_limit"),
            ).fetchone()["c"]
        self.assertEqual(cnt, 1)

    # ── C：enforcement_mode 四值（notify/throttle/block/billing_only 均接受；ban → 422）──
    def test_c_enforcement_mode_four_values(self):
        for mode in ("notify", "throttle", "block", "billing_only"):
            resp = self.client.post(
                "/api/platform/quota-rules",
                headers=self.auth,
                json={
                    "plan_id": self.plan,
                    "quota_type": "token_limit",
                    "enforcement_mode": mode,
                    "status": "draft",
                },
            )
            self.assertEqual(resp.status_code, 201, f"enforcement_mode={mode!r} 应被接受")
            self.assertEqual(resp.json()["enforcement_mode"], mode)

        # 更新路径：取一条 draft 规则，依次改 enforcement_mode 为四值，均 200。
        created = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": self.plan,
                "quota_type": "employee_seat_limit",
                "enforcement_mode": "notify",
                "status": "draft",
            },
        )
        rid = created.json()["quota_rule_id"]
        for mode in ("notify", "throttle", "block", "billing_only"):
            resp = self.client.put(
                f"/api/platform/quota-rules/{rid}",
                headers=self.auth,
                json={"enforcement_mode": mode},
            )
            self.assertEqual(resp.status_code, 200, f"更新 enforcement_mode={mode!r} 应被接受")
            self.assertEqual(resp.json()["enforcement_mode"], mode)

        # 非法值 ban → 422。
        bad = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": self.plan,
                "quota_type": "token_limit",
                "enforcement_mode": "ban",
            },
        )
        self.assertEqual(bad.status_code, 422)

    # ── D：quota_type 五类 + period 四值（非法 cpu_limit/weekly → 422）──
    def test_d_quota_type_and_period(self):
        for qt in _FIVE_TYPES:
            resp = self.client.post(
                "/api/platform/quota-rules",
                headers=self.auth,
                json={"plan_id": self.plan, "quota_type": qt, "status": "draft"},
            )
            self.assertEqual(resp.status_code, 201, f"quota_type={qt!r} 应被接受")

        for p in ("daily", "monthly", "annual", "none"):
            resp = self.client.post(
                "/api/platform/quota-rules",
                headers=self.auth,
                json={
                    "plan_id": self.plan,
                    "quota_type": "token_limit",
                    "period": p,
                    "status": "draft",
                },
            )
            self.assertEqual(resp.status_code, 201, f"period={p!r} 应被接受")

        # 非法 quota_type → 422。
        bad_type = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={"plan_id": self.plan, "quota_type": "cpu_limit"},
        )
        self.assertEqual(bad_type.status_code, 422)

        # 非法 period → 422。
        bad_period = self.client.post(
            "/api/platform/quota-rules",
            headers=self.auth,
            json={
                "plan_id": self.plan,
                "quota_type": "token_limit",
                "period": "weekly",
            },
        )
        self.assertEqual(bad_period.status_code, 422)

    # ── E：已 active 禁改 limit_value → 422（ValueError 映射）──
    def test_e_active_limit_locked(self):
        # seed qr_pro_token 已是 active。
        resp = self.client.put(
            "/api/platform/quota-rules/qr_pro_token",
            headers=self.auth,
            json={"limit_value": 1},
        )
        self.assertEqual(resp.status_code, 422)
        with self.assertRaises(ValueError):
            self.billing.update_quota_rule("qr_pro_token", limit_value=1)

    # ── F：不硬编码（直接改 DB 中 seed 值，API 返回新值）──
    def test_f_not_hardcoded(self):
        with self.db.connect() as conn:
            conn.execute(
                "update quota_rules set limit_value = 424242 where quota_rule_id = 'qr_free_token'"
            )
        resp = self.client.get(
            "/api/platform/plans/plan_free/quotas", headers=self.auth
        )
        self.assertEqual(resp.status_code, 200)
        tokens = [
            r
            for r in resp.json()["quota_rules"]
            if r["quota_rule_id"] == "qr_free_token"
        ]
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["limit_value"], 424242)

    # ── G：套餐配额预览（Free/Pro/Enterprise 各 5 条 active seed 可见，覆盖 5 类）──
    def test_g_plan_quota_preview(self):
        for plan_id in ("plan_free", "plan_pro", "plan_enterprise"):
            resp = self.client.get(
                f"/api/platform/plans/{plan_id}/quotas", headers=self.auth
            )
            self.assertEqual(resp.status_code, 200)
            rules = resp.json()["quota_rules"]
            active = [r for r in rules if r["status"] == "active"]
            types = {r["quota_type"] for r in active}
            self.assertEqual(
                len(active), 5, f"{plan_id} 应有 5 条 active 配额规则（实际 {len(active)}）"
            )
            self.assertEqual(types, _FIVE_TYPES)

    # ── H：守卫 401（无/错令牌访问 4 路由 → 401，非 403；Workspace/前台无对应端点）──
    # 注意：POST/PUT 为带 body 的路由，FastAPI 先校验 body 再进入函数体守卫；
    # 故「无令牌」用例须携带合法 body，以触发 _require_platform_admin 守卫（401）。
    def test_h_admin_guard_401(self):
        endpoints = [
            ("GET", "/api/platform/quota-rules", None),
            (
                "POST",
                "/api/platform/quota-rules",
                {"plan_id": self.plan, "quota_type": "token_limit", "limit_value": 10},
            ),
            ("PUT", "/api/platform/quota-rules/qr_pro_token", {}),
            ("GET", "/api/platform/plans/plan_pro/quotas", None),
        ]
        for method, url, body in endpoints:
            no_token = self.client.request(method, url, json=body)
            self.assertEqual(
                no_token.status_code, 401, f"{method} {url} 无令牌应返回 401"
            )
            self.assertNotEqual(
                no_token.status_code, 403, f"{method} {url} 应为 401 而非 403"
            )
            bad_token = self.client.request(
                method, url, json=body, headers={"Authorization": "Bearer wrong-token"}
            )
            self.assertEqual(
                bad_token.status_code, 401, f"{method} {url} 错误令牌应返回 401"
            )

    # ── I：状态机（draft→active→disabled；disabled 不参与 active 查询）──
    def test_i_state_machine(self):
        rule = self.billing.create_quota_rule(
            plan_id=self.plan,
            quota_type="connector_limit",
            limit_value=5,
            status="draft",
        )
        rid = rule["quota_rule_id"]
        self.assertIsNone(
            self.billing.get_active_quota_rule(self.plan, "connector_limit")
        )
        activated = self.billing.update_quota_rule(rid, status="active")
        self.assertEqual(activated["status"], "active")
        active = self.billing.get_active_quota_rule(self.plan, "connector_limit")
        self.assertEqual(active["quota_rule_id"], rid)
        disabled = self.billing.update_quota_rule(rid, status="disabled")
        self.assertEqual(disabled["status"], "disabled")
        self.assertIsNone(
            self.billing.get_active_quota_rule(self.plan, "connector_limit")
        )

    # ── 红线静态检查 1：7 个 QuotaRule 方法不含 forbidden 逻辑（payment/invoice/
    #    billing_event/value_event/valuepricing/marketplace/promotion/workflow_runtime/
    #    credential_vault/sharedcontract/usageevent/employeeruntime）──
    def test_qa_redline_no_forbidden_logic(self):
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
            "value_event",
            "valuepricing",
            "marketplace",
            "promotion",
            "workflow_runtime",
            "credential_vault",
            "sharedcontract",
            "usageevent",
            "employeeruntime",
        ]
        for fn in targets:
            src = inspect.getsource(fn).lower()
            for word in forbidden:
                self.assertNotIn(
                    word, src, f"{fn.__name__} 不应包含禁止逻辑关键字 {word!r}"
                )

    # ── 红线静态检查 2：4 个 quota-rule 路由（嵌套于 create_app）无 DELETE/DROP ──
    def test_qa_redline_no_delete_on_core_tables(self):
        # 路由函数为 create_app 内闭包，非模块级属性；改为静态扫描源码的 P1 区段。
        main_path = Path(__file__).resolve().parent.parent / "app" / "main.py"
        text = main_path.read_text(encoding="utf-8")
        start = text.index("# ── Phase-9A P1 计划级配额规则")
        # 区段终点锚在下一个业务区段标记。此前锚在 "return app"，会把 create_app
        # 尾部**全部**无关路由吞进来，任何后续路由只要出现 delete/drop 字样即误报。
        # 本用例语义是「4 个 quota-rule 路由无 DELETE/DROP」，不是「main.py 后半段
        # 禁用 delete 一词」，故收敛到真实区段（同时更严格：不再被无关代码稀释）。
        end = text.index("# ── Phase-9A P2 官方能力包商业配置", start)
        section = text[start:end].lower()
        # 边界自检：确保收敛后的区段确实覆盖 4 个 quota-rule 路由。
        self.assertIn("/api/platform/quota-rules", section)
        self.assertIn("/api/platform/plans/{plan_id}/quotas", section)
        self.assertNotIn("delete", section, "quota-rules 区段不应包含 DELETE")
        self.assertNotIn("drop", section, "quota-rules 区段不应包含 DROP")


if __name__ == "__main__":
    unittest.main()
