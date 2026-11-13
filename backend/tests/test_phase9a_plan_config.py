"""Phase-9A 套餐设计调整 —— 独立 QA 验证套件（合规红线，证明行为而非存在）。

本文件由 QA 独立编写，与工程师的 test_phase8_billing_mvp.py（G 节）形成互补与交叉验证：
- 不简单复跑既有用例，而是用**新的数据/新角度**证明每条合规红线确实生效；
- 覆盖全部三个超量维度（token / employee_seat / workflow），而非仅 token；
- 额外验证「遗留库迁移」（既有部署升级路径）与「旧语义三元残留」静态核查。

合规红线（来自 phase9a-plan-config-adjust-design.md）：
  R1 禁止 Enterprise 固定无限：custom 未配置实例时 overage=0 且 breakdown 标 configured:false
      （旧逻辑 limit==0 被静默当成无限，本测试用「configured:false + is_unlimited:false」捕捉回归）
  R2 显式无限须经 Admin 主动授予：POST /api/platform/quotas(is_unlimited=true) 后 overage=0 且 is_unlimited:true
  R3 价格未写死：Pro 超量单价（token/seat/workflow）均为 null 占位，Free 为真实 0
  R4 全 Admin 可配置：update_plan 可覆盖 Free 上限并生效于估算；upsert/update_quota 可双向改写 is_unlimited
  R5 回归保护：Free 1M token/3 seat、Pro 50M/15 seat 不变；Pro 因价格占位 overage 金额恒为 0
  R6 遗留库迁移：既有库 ALTER 新增 is_unlimited、seed 修正 Enterprise 不再 0=无限、Pro 价格占位

运行：backend/.venv/bin/python -m pytest tests/test_phase9a_plan_config.py -q
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import unittest
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

from app.billing_store import BillingStore
from app.database import Database
from app.main import create_app
from fastapi.testclient import TestClient

_APP_DIR = Path(__file__).resolve().parents[1] / "app"
_BILLING_STORE_PY = _APP_DIR / "billing_store.py"
_ADMIN = "platform-admin-dev"


def _code_only(text: str) -> str:
    """去除注释与字符串字面量，仅保留可执行代码结构，便于静态红线扫描。"""
    text = re.sub(r'"""[\s\S]*?"""', '""', text)
    text = re.sub(r"'''[\s\S]*?'''", "''", text)
    text = re.sub(r'"[^"\n]*"', '""', text)
    text = re.sub(r"'[^'\n]*'", "''", text)
    text = re.sub(r"#.*$", "", text, flags=re.MULTILINE)
    return text


class Phase9APlanConfigQATest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase9a.sqlite")
        # create_app 内部调用 database.initialize()：建表 + 幂等 seed 三档默认 Plan（含 Phase-9A）。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        self.db = Database(self.db_path)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── helpers（仿 test_phase8 模式，独立复刻以确保自包含）────────────
    def _seed_tenant(self, tenant_id: str, plan_tier: str = "free") -> dict:
        return self.db.create_tenant(tenant_id, name=tenant_id, plan_tier=plan_tier)

    def _insert_usage(self, tenant_id: str, payload: dict, etype: str = "usage.completion"):
        usage_record_id = f"usage-{uuid.uuid4()}"
        total_tokens = payload.get("total_tokens")
        cost = payload.get("estimated_cost")
        with self.db.connect() as c:
            c.execute(
                "insert into ai_usage_records "
                "(usage_record_id, tenant_id, model_gateway_id, provider_id, model_name, "
                "total_tokens, cost_amount, currency, cost_source, price_version, employee_id, "
                "capability_id, capability_type, task_id, project_id, department_id, request_id, "
                "execution_status, metering_status, occurred_at, idempotency_key, workflow_run_id) "
                "values (?, ?, 'test', 'test', ?, ?, ?, 'USD', ?, ?, ?, 'test.model', 'model', "
                "'test-task', 'test-project', 'test-department', ?, 'success', ?, "
                "current_timestamp, ?, ?)",
                (
                    usage_record_id,
                    tenant_id,
                    payload.get("model_name", "test-model"),
                    total_tokens,
                    cost,
                    "estimated" if cost is not None else "unknown",
                    "test-v1" if cost is not None else None,
                    payload.get("employee_id", "test-employee"),
                    usage_record_id,
                    "confirmed" if total_tokens is not None else "unknown",
                    usage_record_id,
                    payload.get("workflow_run_id"),
                ),
            )
            c.execute(
                "insert into evolution_events (correlation_id, event_type, payload, tenant_id) "
                "values (?, 'usage.model_call', ?, ?)",
                (
                    "corr",
                    json.dumps(
                        {
                            "usage_record_id": usage_record_id,
                            "capability_source": payload.get("capability_source", "official"),
                        }
                    ),
                    tenant_id,
                ),
            )

    def _insert_employee(self, tenant_id: str, eid: str, enabled: int = 1):
        with self.db.connect() as c:
            c.execute(
                "insert into employee_instances "
                "(id, tenant_id, company_id, department_id, template_id, name, role, enabled) "
                "values (?, ?, 'co', 'dep', 'tpl', ?, 'role', ?)",
                (eid, tenant_id, "name-" + eid, enabled),
            )

    def _insert_workflow_run(self, tenant_id: str, wid: str):
        with self.db.connect() as c:
            c.execute(
                "insert into workflow_runs "
                "(workflow_run_id, tenant_id, workflow_instance_id, workflow_template_id, task_id) "
                "values (?, ?, 'wi', 'wt', 'tk')",
                (wid, tenant_id),
            )

    def _calculate_dimensions(self, tenant_id: str) -> dict:
        """直连 BillingStore 估算，返回 plan 级汇总事件的 dimensions 明细（含 configured/is_unlimited）。"""
        events = BillingStore(self.db).calculate_billing_events(tenant_id)
        plan_event = next(e for e in events if e["subject_type"] == "plan")
        return plan_event["breakdown"]["dimensions"]

    # ── R1 禁止 Enterprise 固定无限（全三维度 + 不产生计费事件）────────
    def test_r1_enterprise_custom_unconfigured_zero_overage_all_dims_configured_false(self):
        """Enterprise(quota_mode=custom) 无任何 quota 实例时：
        三个维度 overage 均为 0，breakdown 均含 configured:false、is_unlimited:false；
        且**不生成任何 quota_overage 计费事件**（证明不是静默无限而不计费）。
        """
        self._seed_tenant("t-eua", plan_tier="enterprise")
        # 注入远超任何合理上限的用量，若旧逻辑 limit==0 当无限则会被"放过"——本测试断言其被显式标记未配置。
        self._insert_usage("t-eua", {"total_tokens": 10**12, "model_name": "gpt-4"})
        for i in range(50):
            self._insert_employee("t-eua", f"e{i}")
        for i in range(50):
            self._insert_workflow_run("t-eua", f"w{i}")

        events = BillingStore(self.db).calculate_billing_events("t-eua")
        dims = next(e for e in events if e["subject_type"] == "plan")["breakdown"]["dimensions"]

        for dim in ("token", "employee_seat", "workflow"):
            with self.subTest(dimension=dim):
                self.assertEqual(dims[dim]["overage"], 0, f"{dim} 应无超量（未配置≠无限）")
                self.assertEqual(dims[dim]["configured"], False, f"{dim} 应标记待 Admin 配置")
                self.assertEqual(dims[dim]["is_unlimited"], False, f"{dim} 不得静默无限")
                self.assertEqual(dims[dim]["amount"], 0.0)

        # 关键：不得生成 quota_overage 计费事件（旧逻辑会静默按无限跳过计费，新逻辑明确未配置）。
        overage_events = [e for e in events if e["subject_type"] == "quota_overage"]
        self.assertEqual(overage_events, [], "未配置企业租户不应生成任何超量计费事件")

    # ── R2 显式无限须经 Admin 主动授予（对照 R1 证明无限是显式而非默认）──
    def test_r2_enterprise_explicit_unlimited_requires_admin_grant(self):
        """不经 Admin 授予时（R1）is_unlimited=False；本测试经 POST /api/platform/quotas
        显式传 is_unlimited=true 后，三维度 overage=0 且 is_unlimited:true、configured:true。
        证明无限是 Admin 主动、可审计授予，而非静默默认。
        """
        self._seed_tenant("t-eub", plan_tier="enterprise")
        for qtype in ("token", "employee_seat", "workflow"):
            resp = self.client.post(
                "/api/platform/quotas",
                headers=self.auth,
                json={
                    "tenant_id": "t-eub",
                    "plan_id": "plan_enterprise",
                    "quota_type": qtype,
                    "limit_value": 0,
                    "is_unlimited": True,  # Admin 主动授予
                },
            )
            self.assertEqual(resp.status_code, 201, resp.text)

        self._insert_usage("t-eub", {"total_tokens": 10**12, "model_name": "gpt-4"})
        for i in range(50):
            self._insert_employee("t-eub", f"e{i}")
        for i in range(50):
            self._insert_workflow_run("t-eub", f"w{i}")

        dims = self._calculate_dimensions("t-eub")
        for dim in ("token", "employee_seat", "workflow"):
            with self.subTest(dimension=dim):
                self.assertEqual(dims[dim]["is_unlimited"], True, f"{dim} 应显式无限（经 Admin 授予）")
                self.assertEqual(dims[dim]["configured"], True, f"{dim} 实例已配置")
                self.assertEqual(dims[dim]["overage"], 0)
                self.assertEqual(dims[dim]["amount"], 0.0)

    # ── R3 价格未写死（Pro 占位 null，Free 真实 0）──────────────────────
    def test_r3_pro_overage_prices_are_null_placeholder_not_hardcoded(self):
        """读取 Pro 计划的 quota_rules.overage：token/seat/workflow 单价必须均为 null（占位），
        证明无真实价格被写死；对照 Free 超量价为真实 0（非 null），区分"占位"与"真实零"。
        """
        pro = BillingStore(self.db).get_plan("plan_pro")["quota_rules"]["overage"]
        self.assertIsNone(pro["token_unit_price_per_1k"], "Pro token 超量单价不得写死真实价格")
        self.assertIsNone(pro["seat_unit_price"], "Pro seat 超量单价不得写死真实价格")
        self.assertIsNone(pro["workflow_unit_price"], "Pro workflow 超量单价不得写死真实价格")

        free = BillingStore(self.db).get_plan("plan_free")["quota_rules"]["overage"]
        self.assertEqual(free["token_unit_price_per_1k"], 0, "Free 超量价应为真实 0")
        self.assertIsNotNone(free["token_unit_price_per_1k"])

    # ── R4 全 Admin 可配置（覆盖 Free 上限生效于估算 + is_unlimited 双向改写）──
    def test_r4_admin_overrides_free_limit_and_toggles_unlimited_flag(self):
        # 1) Admin 经 PUT /api/platform/plans 覆盖 Free 的 token_monthly_limit=999
        put = self.client.put(
            "/api/platform/plans/plan_free",
            headers=self.auth,
            json={
                "quota_rules": {
                    "quota_mode": "plan_default",
                    "is_unlimited": False,
                    "token_monthly_limit": 999,
                    "seat_limit": 3,
                    "capability_sources": ["official"],
                    "workflow_monthly_limit": 0,
                    "overage": {
                        "token_unit_price_per_1k": 0,
                        "seat_unit_price": 0,
                        "workflow_unit_price": 0,
                        "capability_unit_price": 0,
                    },
                    "currency": "USD",
                }
            },
        )
        self.assertEqual(put.status_code, 200, put.text)
        free = BillingStore(self.db).get_plan("plan_free")
        self.assertEqual(free["quota_rules"]["token_monthly_limit"], 999, "Admin 覆盖未持久化")

        # 覆盖须生效于估算（而非仅存储）：Free 租户 2000 token → overage=2000-999=1001
        self._seed_tenant("t-cfg", plan_tier="free")
        self._insert_usage("t-cfg", {"total_tokens": 2000, "model_name": "gpt-4"})
        dims = self._calculate_dimensions("t-cfg")
        self.assertEqual(dims["token"]["limit"], 999)
        self.assertEqual(dims["token"]["overage"], 1001)
        self.assertEqual(dims["token"]["configured"], True)

        # 2) is_unlimited 标记可经 upsert/update 双向改写（有限 ↔ 无限）
        store = BillingStore(self.db)
        created = store.upsert_quota_limit(
            tenant_id="t-cfg", plan_id="plan_free", quota_type="token",
            limit_value=500, is_unlimited=True,
        )
        self.assertEqual(created["is_unlimited"], True)
        updated = store.update_quota(created["quota_id"], limit_value=500, is_unlimited=False)
        self.assertEqual(updated["is_unlimited"], False, "update_quota 未将 is_unlimited 改回有限")
        # 再经 API 显式改回 True，证明双向均可经 Admin 配置
        resp = self.client.put(
            f"/api/platform/quotas/{created['quota_id']}",
            headers=self.auth,
            json={"limit_value": 500, "is_unlimited": True},
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertEqual(resp.json()["is_unlimited"], True)

    # ── R4 补充：Enterprise 配置了有限实例时按实例 limit 算超量（custom 派生自租户实例）──
    def test_r4_enterprise_custom_configured_finite_instance_computes_overage(self):
        self._seed_tenant("t-euc", plan_tier="enterprise")
        created = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={
                "tenant_id": "t-euc",
                "plan_id": "plan_enterprise",
                "quota_type": "token",
                "limit_value": 100,
            },
        ).json()
        self.assertEqual(created["is_unlimited"], False)
        self._insert_usage("t-euc", {"total_tokens": 1000, "model_name": "gpt-4"})
        dims = self._calculate_dimensions("t-euc")
        self.assertEqual(dims["token"]["configured"], True)
        self.assertEqual(dims["token"]["is_unlimited"], False)
        self.assertEqual(dims["token"]["limit"], 100)
        self.assertEqual(dims["token"]["overage"], 900)  # 1000 - 100，证明从实例派生而非模板

    # ── R5 回归保护（Free/Pro 默认档不变 + Pro overage 金额恒 0）────────
    def test_r5_regression_free_pro_defaults_and_pro_overage_amount_zero(self):
        free = BillingStore(self.db).get_plan("plan_free")["quota_rules"]
        pro = BillingStore(self.db).get_plan("plan_pro")["quota_rules"]
        # 默认档上限不变
        self.assertEqual(free["token_monthly_limit"], 1_000_000, "Free 默认 token 上限应仍为 1M")
        self.assertEqual(free["seat_limit"], 3, "Free 默认 seat 上限应仍为 3")
        self.assertEqual(pro["token_monthly_limit"], 50_000_000, "Pro 默认 token 上限应仍为 50M")
        self.assertEqual(pro["seat_limit"], 15, "Pro 默认 seat 上限应仍为 15")

        # Pro 租户超量：60M token(>50M) → overage_qty>0 但金额=0（价格占位 null，证明未写死真实价）
        self._seed_tenant("t-reg", plan_tier="pro")
        self._insert_usage("t-reg", {"total_tokens": 60_000_000, "model_name": "gpt-4"})
        for i in range(20):
            self._insert_employee("t-reg", f"e{i}")  # 20 > 15 → seat overage 5
        dims = self._calculate_dimensions("t-reg")
        self.assertGreater(dims["token"]["overage"], 0, "Pro token 应产生超量数量")
        self.assertEqual(dims["token"]["amount"], 0.0, "Pro 因价格占位 overage 金额须为 0")
        self.assertGreater(dims["employee_seat"]["overage"], 0, "Pro seat 应产生超量数量")
        self.assertEqual(dims["employee_seat"]["amount"], 0.0, "Pro seat 金额须为 0")

    # ── R6 遗留库迁移（既有部署升级路径）────────────────────────────────
    def test_r6_legacy_db_migration_adds_is_unlimited_and_fixes_seed(self):
        """构造 Phase-9A 之前的旧库：quotas 无 is_unlimited 列、plans seed 无 quota_mode
        （Enterprise 用 0=无限、Pro 用真实价格写死——旧缺陷）。触发 initialize() 后断言：
        - quotas 表现在含 is_unlimited 列；
        - Enterprise 迁移为 quota_mode=custom 且 token_monthly_limit=null（不再 0=无限）；
        - Pro 旧真实价格被迁移为占位 null（不再写死）。
        """
        legacy = str(Path(self.tmp.name) / "legacy.sqlite")
        conn = sqlite3.connect(legacy)
        conn.execute(
            "create table if not exists plans ("
            "plan_id text primary key, plan_code text, name text, tier text, status text, "
            "version text, billing_interval text, features_json text, quota_rules_json text, "
            "created_at text, updated_at text)"
        )
        conn.execute(
            "create table if not exists quotas ("
            "quota_id text primary key, tenant_id text, plan_id text, plan_code text, "
            "quota_type text, limit_value integer, current_usage integer, period text, "
            "period_start text, period_end text, source_scope_json text, status text, "
            "created_at text, updated_at text)"
        )
        # 旧 seed：Enterprise 0=无限；Pro 写死真实价格 0.002/9/0.01
        conn.execute(
            "insert into plans values ('plan_free','free','Free','free','active','1.0.0','monthly','[]',?,current_timestamp,current_timestamp)",
            ('{"token_monthly_limit":1000000,"seat_limit":3,"capability_sources":["official"],"workflow_monthly_limit":0,"overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},"currency":"USD"}',),
        )
        conn.execute(
            "insert into plans values ('plan_pro','pro','Pro','pro','active','1.0.0','monthly','[]',?,current_timestamp,current_timestamp)",
            ('{"token_monthly_limit":50000000,"seat_limit":15,"capability_sources":["official","tenant_private"],"workflow_monthly_limit":50000,"overage":{"token_unit_price_per_1k":0.002,"seat_unit_price":9,"workflow_unit_price":0.01,"capability_unit_price":0},"currency":"USD"}',),
        )
        conn.execute(
            "insert into plans values ('plan_enterprise','enterprise','Enterprise','enterprise','active','1.0.0','annual','[]',?,current_timestamp,current_timestamp)",
            ('{"token_monthly_limit":0,"seat_limit":0,"capability_sources":["official","tenant_private","marketplace"],"workflow_monthly_limit":0,"overage":{"token_unit_price_per_1k":0,"seat_unit_price":0,"workflow_unit_price":0,"capability_unit_price":0},"currency":"USD"}',),
        )
        conn.commit()
        conn.close()

        # 触发迁移（create_app 内部调用 database.initialize）
        create_app(legacy)
        store = BillingStore(Database(legacy))

        # quotas 表现在应有 is_unlimited 列
        with Database(legacy).connect() as c:
            cols = {r["name"] for r in c.execute("pragma table_info(quotas)")}
        self.assertIn("is_unlimited", cols, "遗留库迁移后 quotas 应新增 is_unlimited 列")

        # Enterprise 不再 0=无限：quota_mode=custom、token_monthly_limit=null
        ent = store.get_plan("plan_enterprise")["quota_rules"]
        self.assertEqual(ent["quota_mode"], "custom")
        self.assertIsNone(ent["token_monthly_limit"])
        self.assertIsNone(ent["seat_limit"])

        # Pro 旧真实价格被迁移为占位 null（证明不再写死）
        pro = store.get_plan("plan_pro")["quota_rules"]["overage"]
        self.assertIsNone(pro["token_unit_price_per_1k"])
        self.assertIsNone(pro["seat_unit_price"])
        self.assertIsNone(pro["workflow_unit_price"])

    # ── 静态红线：calculate_billing_events 须为三分支新语义，不得残留旧三元 ──
    def test_static_no_legacy_silent_unlimited_pattern(self):
        """核查 billing_store.calculate_billing_events 实际落地的逻辑结构：
        - 必须存在 if is_unlimited / elif limit and limit > 0 / else 三分支（新语义）；
        - 不得残留旧三元 `max(0, usage - limit) if limit and limit > 0 else 0`
          （该写法会令 limit==0 静默当作无限，是本次要修的缺陷）。
        """
        text = _BILLING_STORE_PY.read_text(encoding="utf-8")
        m = re.search(r"def calculate_billing_events\([\s\S]*?\n    def ", text)
        self.assertIsNotNone(m, "应找到 calculate_billing_events 函数体")
        body = m.group(0)
        code = _code_only(body)

        self.assertIn("if is_unlimited:", code, "缺少显式 is_unlimited 分支")
        self.assertIn("elif limit and limit > 0:", code, "缺少基于 limit>0 的分支")
        self.assertIn("else:", code, "缺少兜底分支")
        self.assertNotRegex(
            code,
            r"max\(\s*0\s*,\s*usage\s*-\s*limit\s*\)\s*if\s+limit",
            "存在旧语义三元：limit==0 会被静默当作无限",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
