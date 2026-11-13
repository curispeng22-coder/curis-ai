"""Phase-8 Billing MVP Admin (issue P8) — QA 验证套件。

沿用 backend/tests 既有 TestClient + unittest 风格（参考 test_d4_platform）。
覆盖：
  A. 鉴权守卫（全部 12 个新端点：无令牌 → 401；有效令牌 → 放行）
  B. Plan 管理（创建 Free/Pro/Enterprise、重复 plan_code → 422、404、PUT 非法 enum → 422、
     toggle enable↔active / disable↔deprecated、plan_code 与 tenants.plan_tier 1:1 不破坏）
  C. Quota 管理（派生/更新实例、PUT 更新 limit、GET 返回 current_usage 已派生、
     GET 缺 tenant_id → 空列表隔离优先）
  D. Usage 聚合（缺 tenant_id → 422 fail-closed；有 tenant_id 返回分组聚合；
     断言响应不含 credential 明文 / tenant_private 内容）
  E. Billing Event（calculate 生成 draft/calculated、amount 计算正确、status 过滤、
     issued 仅状态占位无资金副作用）
  F. 6 项禁止的代码级核验（grep / 静态扫描断言）

运行：backend/.venv/bin/python -m pytest tests/test_phase8_billing_mvp.py -q
"""

from __future__ import annotations

import json
import os
import re
import unittest
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.main import create_app
from fastapi.testclient import TestClient

_APP_DIR = Path(__file__).resolve().parents[1] / "app"
_MAIN_PY = _APP_DIR / "main.py"
_BILLING_STORE_PY = _APP_DIR / "billing_store.py"
_ADMIN = "platform-admin-dev"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _code_only(text: str) -> str:
    """Strip comments and string literals so forbidden-scope scans hit only code.

    Docstrings legitimately *mention* forbidden words (e.g. "we never import
    credential_vault"); those must not be treated as violations.
    """
    text = re.sub(r'"""[\s\S]*?"""', '""', text)
    text = re.sub(r"'''[\s\S]*?'''", "''", text)
    text = re.sub(r'"[^"\n]*"', '""', text)
    text = re.sub(r"'[^'\n]*'", "''", text)
    text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)
    return text


def _code_hits(text: str, pattern: str) -> list[str]:
    """Return all regex hits within code-only text."""
    return re.findall(pattern, _code_only(text))


class Phase8BillingMVPTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _ADMIN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "phase8.sqlite")
        # create_app 内部调用 database.initialize()：建表 + 幂等 seed 三档默认 Plan。
        self.app = create_app(self.db_path)
        self.client = TestClient(self.app)
        # 独立连接同一 sqlite 文件，用于注入测试数据（initialize 已建表/seed）。
        self.db = Database(self.db_path)
        self.auth = {"Authorization": f"Bearer {_ADMIN}"}

    def tearDown(self):
        self.tmp.cleanup()

    # ── helpers ──────────────────────────────────────────────────────────
    def _seed_tenant(self, tenant_id: str, plan_tier: str = "free") -> dict:
        return self.db.create_tenant(tenant_id, name=tenant_id, plan_tier=plan_tier)

    def _insert_usage(self, tenant_id: str, payload: dict, etype: str = "usage.completion"):
        usage_record_id = f"usage-{uuid.uuid4()}"
        total_tokens = payload.get("total_tokens")
        cost = payload.get("estimated_cost")
        company_id = f"company-{tenant_id}"
        project_id = f"project-{tenant_id}"
        department_id = f"department-{tenant_id}"
        with self.db.connect() as c:
            c.execute(
                "insert or ignore into companies(company_id, tenant_id, name) values (?, ?, ?)",
                (company_id, tenant_id, company_id),
            )
            c.execute(
                "insert or ignore into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
                "values (?, ?, ?, 'billing-test', 'Billing Test', 'TEST')",
                (department_id, tenant_id, company_id),
            )
            c.execute(
                "insert or ignore into projects(project_id, tenant_id, company_id, department_id, name, goal) "
                "values (?, ?, ?, ?, 'Billing Test', 'Usage fixture')",
                (project_id, tenant_id, company_id, department_id),
            )
            c.execute(
                "insert into ai_usage_records "
                "(usage_record_id, tenant_id, company_id, model_gateway_id, provider_id, model_name, "
                "total_tokens, cost_amount, currency, cost_source, price_version, employee_id, "
                "capability_id, capability_type, task_id, project_id, department_id, request_id, "
                "execution_status, metering_status, occurred_at, idempotency_key, workflow_run_id) "
                "values (?, ?, ?, 'test', 'test', ?, ?, ?, ?, ?, ?, ?, 'test.model', 'model', "
                "'test-task', ?, ?, ?, 'success', ?, "
                "current_timestamp, ?, ?)",
                (
                    usage_record_id,
                    tenant_id,
                    company_id,
                    payload.get("model_name", "test-model"),
                    total_tokens,
                    cost,
                    payload.get("currency", "USD"),
                    "estimated" if cost is not None else "unknown",
                    "test-v1" if cost is not None else None,
                    payload.get("employee_id", "test-employee"),
                    project_id,
                    department_id,
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

    # ── A. 鉴权守卫（12 个新端点）────────────────────────────────────────
    def _all_endpoints(self):
        """返回 (method, path, json_body|None) 列表，覆盖全部 12 个新端点。"""
        return [
            ("GET", "/api/platform/plans", None),
            ("POST", "/api/platform/plans", {"plan_code": "auth_free", "name": "AuthFree", "tier": "free"}),
            ("GET", "/api/platform/plans/plan_free", None),
            ("PUT", "/api/platform/plans/plan_free", {"name": "Renamed"}),
            ("POST", "/api/platform/plans/plan_free/toggle", {"action": "enable"}),
            ("GET", "/api/platform/quotas", None),
            ("POST", "/api/platform/quotas", {"tenant_id": "t-auth", "plan_id": "plan_free", "quota_type": "token"}),
            ("GET", "/api/platform/quotas/t-auth", None),
            ("PUT", "/api/platform/quotas/quota_nonexistent", {"limit_value": 10}),
            ("GET", "/api/platform/usage/summary", None),
            ("GET", "/api/platform/billing-events", None),
            ("POST", "/api/platform/billing-events/calculate", {"tenant_id": "t-auth"}),
        ]

    def test_all_12_endpoints_require_auth(self):
        for method, path, body in self._all_endpoints():
            resp = self.client.request(method, path, json=body)
            self.assertEqual(
                resp.status_code, 401,
                f"无令牌应 401：{method} {path} 返回 {resp.status_code}",
            )

    def test_valid_token_allows_access_on_all_12_endpoints(self):
        for method, path, body in self._all_endpoints():
            resp = self.client.request(method, path, json=body, headers=self.auth)
            self.assertNotEqual(
                resp.status_code, 401,
                f"有效令牌应放行（非 401）：{method} {path} 返回 {resp.status_code}",
            )

    def test_wrong_token_rejected(self):
        bad = {"Authorization": "Bearer wrong-token"}
        resp = self.client.get("/api/platform/plans", headers=bad)
        self.assertEqual(resp.status_code, 401)

    # ── B. Plan 管理 ────────────────────────────────────────────────────
    def test_create_plan_free_pro_enterprise(self):
        for code, tier in [("qa_free", "free"), ("qa_pro", "pro"), ("qa_ent", "enterprise")]:
            resp = self.client.post(
                "/api/platform/plans",
                headers=self.auth,
                json={"plan_code": code, "name": code, "tier": tier},
            )
            self.assertEqual(resp.status_code, 201, resp.text)
            body = resp.json()
            self.assertEqual(body["plan_code"], code)
            self.assertEqual(body["tier"], tier)
            self.assertEqual(body["status"], "draft")  # 默认 draft

    def test_create_plan_duplicate_code_returns_422(self):
        # plan_free 已由 seed 存在 → 重复 plan_code 触发 IntegrityError → 422。
        resp = self.client.post(
            "/api/platform/plans",
            headers=self.auth,
            json={"plan_code": "free", "name": "Dup", "tier": "free"},
        )
        self.assertEqual(resp.status_code, 422, resp.text)

    def test_get_plan_not_found_returns_404(self):
        resp = self.client.get("/api/platform/plans/plan_does_not_exist", headers=self.auth)
        self.assertEqual(resp.status_code, 404, resp.text)

    def test_put_plan_invalid_status_returns_422(self):
        resp = self.client.put(
            "/api/platform/plans/plan_free",
            headers=self.auth,
            json={"status": "not_a_real_status"},
        )
        self.assertEqual(resp.status_code, 422, resp.text)

    def test_put_plan_valid_status_and_fields(self):
        resp = self.client.put(
            "/api/platform/plans/plan_free",
            headers=self.auth,
            json={"status": "deprecated", "name": "FreeRenamed"},
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        body = resp.json()
        self.assertEqual(body["status"], "deprecated")
        self.assertEqual(body["name"], "FreeRenamed")

    def test_toggle_enable_sets_active_disable_sets_deprecated(self):
        # 先建一个 draft plan。
        created = self.client.post(
            "/api/platform/plans",
            headers=self.auth,
            json={"plan_code": "qa_toggle", "name": "Toggle", "tier": "free", "status": "draft"},
        ).json()
        pid = created["plan_id"]

        enable = self.client.post(
            f"/api/platform/plans/{pid}/toggle", headers=self.auth, json={"action": "enable"}
        )
        self.assertEqual(enable.status_code, 200, enable.text)
        self.assertEqual(enable.json()["status"], "active")

        disable = self.client.post(
            f"/api/platform/plans/{pid}/toggle", headers=self.auth, json={"action": "disable"}
        )
        self.assertEqual(disable.status_code, 200, disable.text)
        self.assertEqual(disable.json()["status"], "deprecated")

    def test_toggle_invalid_action_returns_422(self):
        resp = self.client.post(
            "/api/platform/plans/plan_free/toggle", headers=self.auth, json={"action": "frobnicate"}
        )
        self.assertEqual(resp.status_code, 422, resp.text)

    def test_plan_code_one_to_one_with_tenant_plan_tier(self):
        # 造一个 enterprise 租户，反查 plan_code=enterprise 的计划不被破坏。
        from app.billing_store import BillingStore

        self._seed_tenant("t-ent", plan_tier="enterprise")
        tenant = self.db.get_tenant("t-ent")
        self.assertEqual(tenant["plan_tier"], "enterprise")
        ent_plan = BillingStore(self.db).get_plan_by_code("enterprise")
        self.assertIsNotNone(ent_plan, "enterprise 计划应被 seed 存在")
        self.assertEqual(ent_plan["plan_code"], "enterprise")
        # 重复创建 enterprise plan_code 应 422（1:1 对齐约束不破坏）。
        dup = self.client.post(
            "/api/platform/plans",
            headers=self.auth,
            json={"plan_code": "enterprise", "name": "DupEnt", "tier": "enterprise"},
        )
        self.assertEqual(dup.status_code, 422, dup.text)

    # ── C. Quota 管理 ───────────────────────────────────────────────────
    def test_post_quota_derives_instance_from_plan(self):
        self._seed_tenant("t-quota")
        resp = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={"tenant_id": "t-quota", "plan_id": "plan_free", "quota_type": "token"},
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        body = resp.json()
        self.assertEqual(body["tenant_id"], "t-quota")
        self.assertEqual(body["quota_type"], "token")
        self.assertEqual(body["plan_code"], "free")  # 由 plan_id=plan_free 派生
        self.assertEqual(body["limit_value"], 0)

    def test_put_quota_updates_limit_value(self):
        self._seed_tenant("t-quota2")
        created = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={"tenant_id": "t-quota2", "plan_id": "plan_free", "quota_type": "token"},
        ).json()
        qid = created["quota_id"]
        resp = self.client.put(
            f"/api/platform/quotas/{qid}", headers=self.auth, json={"limit_value": 12345}
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertEqual(resp.json()["limit_value"], 12345)

    def test_get_quotas_missing_tenant_id_returns_empty_list(self):
        resp = self.client.get("/api/platform/quotas", headers=self.auth)
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertEqual(resp.json(), {"quotas": []})

    def test_get_quotas_for_tenant_returns_derived_current_usage(self):
        self._seed_tenant("t-usage")
        # 注入 1500 token 用量（event_type like 'usage.%'）。
        self._insert_usage("t-usage", {"total_tokens": 1500, "model_name": "gpt-4"})
        created = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={"tenant_id": "t-usage", "plan_id": "plan_free", "quota_type": "token"},
        ).json()
        resp = self.client.get("/api/platform/quotas/t-usage", headers=self.auth)
        self.assertEqual(resp.status_code, 200, resp.text)
        quotas = resp.json()["quotas"]
        token_quota = next(q for q in quotas if q["quota_type"] == "token")
        # current_usage 由读时聚合派生（实时 token 用量 = 1500）。
        self.assertEqual(token_quota["current_usage"], 1500)

    # ── D. Usage 只读聚合 ───────────────────────────────────────────────
    def test_usage_summary_missing_tenant_id_returns_422(self):
        resp = self.client.get("/api/platform/usage/summary", headers=self.auth)
        self.assertEqual(resp.status_code, 422, resp.text)
        self.assertIn("tenant_id", resp.json()["detail"])

    def test_usage_summary_aggregates_by_model_capability_employee_workflow(self):
        self._seed_tenant("t-sum")
        payload = {
            "total_tokens": 1000,
            "estimated_cost": 0.02,
            "model_name": "gpt-4",
            "capability_source": "official",
            "employee_id": "emp-1",
            "workflow_run_id": "wr-1",
        }
        # 两条同维度事件，用于聚合计数。
        self._insert_usage("t-sum", payload)
        self._insert_usage("t-sum", payload)
        resp = self.client.get(
            "/api/platform/usage/summary", headers=self.auth, params={"tenant_id": "t-sum"}
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        data = resp.json()
        self.assertEqual(data["tenant_id"], "t-sum")
        self.assertEqual(data["totals"]["total_tokens"], 2000)
        self.assertEqual(data["totals"]["event_count"], 2)
        # by_model
        self.assertEqual(len(data["by_model"]), 1)
        self.assertEqual(data["by_model"][0]["model_name"], "gpt-4")
        self.assertEqual(data["by_model"][0]["total_tokens"], 2000)
        self.assertEqual(data["by_model"][0]["count"], 2)
        # by_capability_source
        self.assertEqual(data["by_capability_source"][0]["capability_source"], "official")
        self.assertEqual(data["by_capability_source"][0]["count"], 2)
        # by_employee
        self.assertEqual(data["by_employee"][0]["employee_id"], "emp-1")
        self.assertEqual(data["by_employee"][0]["count"], 2)
        # by_workflow
        self.assertEqual(data["by_workflow"][0]["workflow_run_id"], "wr-1")
        self.assertEqual(data["by_workflow"][0]["count"], 2)

    def test_usage_summary_unknown_partial_zero_and_currency_are_distinct(self):
        self._seed_tenant("money-scope")
        self._seed_tenant("money-other")
        def summary():
            response = self.client.get("/api/platform/usage/summary", headers=self.auth,
                                       params={"tenant_id": "money-scope"})
            self.assertEqual(response.status_code, 200, response.text)
            return response.json()
        empty = summary()["totals"]
        self.assertIsNone(empty["total_cost"])
        self.assertEqual(empty["cost_by_currency"], [])
        self._insert_usage("money-scope", {"model_name": "usd", "total_tokens": 10})
        self._insert_usage("money-other", {"model_name": "foreign", "estimated_cost": 99})
        unknown = summary()["totals"]
        self.assertIsNone(unknown["total_cost"])
        self.assertEqual(unknown["unknown_cost_count"], 1)
        self._insert_usage("money-scope", {"model_name": "usd", "estimated_cost": 0})
        partial = summary()
        self.assertIsNone(partial["totals"]["total_cost"])
        self.assertEqual(partial["totals"]["cost_by_currency"], [
            {"currency": "USD", "known_cost": 0.0, "unknown_cost_count": 1}])
        self.assertIsNone(partial["by_model"][0]["total_cost"])
        self._insert_usage("money-scope", {"model_name": "eur", "estimated_cost": 2, "currency": "EUR"})
        mixed = summary()
        self.assertIsNone(mixed["totals"]["total_cost"])
        self.assertIsNone(mixed["totals"]["currency"])
        self.assertEqual([row["currency"] for row in mixed["totals"]["cost_by_currency"]], ["EUR", "USD"])
        self.assertNotIn("foreign", str(mixed))
        eur = next(row for row in mixed["by_model"] if row["model_name"] == "eur")
        self.assertEqual(eur["total_cost"], 2.0)
        self.assertEqual(eur["currency"], "EUR")

    def test_usage_summary_no_credential_plaintext_or_tenant_private_leak(self):
        self._seed_tenant("t-sec")
        # 注入含明文凭证 / tenant_private 内容的事件，验证聚合响应绝不回显。
        payload = {
            "total_tokens": 500,
            "model_name": "gpt-4",
            "capability_source": "official",
            "employee_id": "emp-1",
            "workflow_run_id": "wr-1",
            "estimated_cost": 0.01,
            "credential_id": "cred-abc",
            "credential_ref_digest": "sha256:deadbeef",
            "provider_api_key": "sk-SUPERSECRET123",
            "api_key": "ak-LEAKED999",
            "tenant_private": {"ssn": "123-45-6789", "bank_account": "acct-999"},
        }
        self._insert_usage("t-sec", payload)
        resp = self.client.get(
            "/api/platform/usage/summary", headers=self.auth, params={"tenant_id": "t-sec"}
        )
        self.assertEqual(resp.status_code, 200, resp.text)
        body_str = resp.text
        # 明文敏感字段一律不得出现。
        for leak in (
            "sk-SUPERSECRET123",
            "ak-LEAKED999",
            "123-45-6789",
            "acct-999",
            "provider_api_key",
            "api_key",
            "tenant_private",
            "ssn",
        ):
            self.assertNotIn(leak, body_str, f"响应泄露了敏感字段/键：{leak}")
        # 合法脱敏字段也并非必须出现（usage_summary 不返回 credential 字段），
        # 但分组维度字段必须存在。
        self.assertIn("gpt-4", body_str)
        self.assertIn("official", body_str)

    # ── E. Billing Event ───────────────────────────────────────────────
    def _seed_calc_tenant(self):
        """造一个自定义 plan（可控 limit/overage 单价）+ 租户，便于精确断言 amount。"""
        self.client.post(
            "/api/platform/plans",
            headers=self.auth,
            json={
                "plan_code": "calc",
                "name": "Calc",
                "tier": "pro",
                "quota_rules": {
                    "token_monthly_limit": 100,
                    "seat_limit": 2,
                    "capability_sources": ["official"],
                    "workflow_monthly_limit": 5,
                    "overage": {
                        "token_unit_price_per_1k": 0.5,
                        "seat_unit_price": 3,
                        "workflow_unit_price": 0.1,
                        "capability_unit_price": 0,
                    },
                    "currency": "USD",
                },
            },
        )
        self._seed_tenant("t-calc", plan_tier="calc")
        # token 用量 1100 → overage 1000 → amount = (1000/1000)*0.5 = 0.5
        self._insert_usage("t-calc", {"total_tokens": 1100, "model_name": "gpt-4"})
        # seat 5 个启用 → overage 3 → amount = 3*3 = 9.0
        for i in range(5):
            self._insert_employee("t-calc", f"e{i}")
        # workflow 10 次 → overage 5 → amount = 5*0.1 = 0.5
        for i in range(10):
            self._insert_workflow_run("t-calc", f"w{i}")

    def test_calculate_generates_draft_when_as_calculated_false(self):
        self._seed_calc_tenant()
        resp = self.client.post(
            "/api/platform/billing-events/calculate",
            headers=self.auth,
            json={"tenant_id": "t-calc", "as_calculated": False},
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        events = resp.json()["billing_events"]
        self.assertTrue(events)
        self.assertTrue(all(e["status"] == "draft" for e in events))

    def test_calculate_amount_formula_correct(self):
        self._seed_calc_tenant()
        resp = self.client.post(
            "/api/platform/billing-events/calculate",
            headers=self.auth,
            json={"tenant_id": "t-calc", "as_calculated": True},
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        events = resp.json()["billing_events"]
        by_subject = {e["subject_id"]: e for e in events if e["subject_type"] == "quota_overage"}
        plan_event = next(e for e in events if e["subject_type"] == "plan")

        # token: overage 1000 * 0.5/1k = 0.5
        self.assertIn("token", by_subject)
        self.assertAlmostEqual(by_subject["token"]["amount"], 0.5, places=6)
        # seat: overage 3 * 3 = 9.0
        self.assertIn("employee_seat", by_subject)
        self.assertAlmostEqual(by_subject["employee_seat"]["amount"], 9.0, places=6)
        # workflow: overage 5 * 0.1 = 0.5
        self.assertIn("workflow", by_subject)
        self.assertAlmostEqual(by_subject["workflow"]["amount"], 0.5, places=6)
        # plan 级汇总 = 0.5 + 9.0 + 0.5 = 10.0，状态 calculated，币种 USD。
        self.assertAlmostEqual(plan_event["amount"], 10.0, places=6)
        self.assertEqual(plan_event["status"], "calculated")
        self.assertEqual(plan_event["currency"], "USD")

    def test_calculate_tenant_not_found_returns_422(self):
        resp = self.client.post(
            "/api/platform/billing-events/calculate",
            headers=self.auth,
            json={"tenant_id": "t-no-such"},
        )
        self.assertEqual(resp.status_code, 422, resp.text)

    def test_billing_events_filter_by_status(self):
        self._seed_calc_tenant()
        # 生成 calculated 事件。
        self.client.post(
            "/api/platform/billing-events/calculate",
            headers=self.auth,
            json={"tenant_id": "t-calc", "as_calculated": True},
        )
        calculated = self.client.get(
            "/api/platform/billing-events", headers=self.auth, params={"status": "calculated"}
        ).json()["billing_events"]
        self.assertTrue(calculated)
        self.assertTrue(all(e["status"] == "calculated" for e in calculated))

        draft = self.client.get(
            "/api/platform/billing-events", headers=self.auth, params={"status": "draft"}
        ).json()["billing_events"]
        self.assertEqual(draft, [])

    def test_issued_status_is_placeholder_no_side_effects(self):
        """issued 仅状态占位：set_billing_event_status 不产生额外写 / 外部调用。"""
        from app.billing_store import BillingStore

        self._seed_calc_tenant()
        events = self.client.post(
            "/api/platform/billing-events/calculate",
            headers=self.auth,
            json={"tenant_id": "t-calc", "as_calculated": True},
        ).json()["billing_events"]
        target = events[0]
        before_count = len(
            self.client.get(
                "/api/platform/billing-events", headers=self.auth, params={"tenant_id": "t-calc"}
            ).json()["billing_events"]
        )

        store = BillingStore(self.db)
        updated = store.set_billing_event_status(target["billing_event_id"], "issued")
        self.assertEqual(updated["status"], "issued")
        self.assertAlmostEqual(updated["amount"], target["amount"], places=6)

        # 事件总数不变（仅状态变更，无新增行），且金额未被改写。
        after_count = len(
            self.client.get(
                "/api/platform/billing-events", headers=self.auth, params={"tenant_id": "t-calc"}
            ).json()["billing_events"]
        )
        self.assertEqual(after_count, before_count)

    # ── F. 6 项禁止核验 ────────────────────────────────────────────────
    def test_forbidden_1_billing_store_does_not_import_credential_vault(self):
        text = _read(_BILLING_STORE_PY)
        # 仅在 docstring 中提及；不得出现真实 import / 代码引用。
        code_hits = _code_hits(text, r"credential_vault")
        self.assertEqual(code_hits, [], f"billing_store 引用了 credential_vault: {code_hits}")

    def test_forbidden_2_no_workspace_write_touches_billing(self):
        text = _read(_MAIN_PY)
        # 解析每个路由：收集 (path, 函数体)；workspace 路由的函数体不得引用 billing。
        route_re = re.compile(
            r'@app\.(get|post|put|delete|patch)\(\s*["\'](/api/workspace[^"\']*)["\']'
        )
        # 函数体：从 def 行到下一个顶层 def（缩进 4 空格）之前。
        func_spans = list(re.finditer(r'\n    def (\w+)\(', text))
        src = "\n" + text
        violations = []
        for m in route_re.finditer(text):
            path = m.group(2)
            # 找到该装饰器之后的 def（即处理函数）。
            after = m.end()
            next_def = text.find("\n    def ", after)
            body = text[after:next_def] if next_def != -1 else text[after:]
            if "billing" in body:
                violations.append(path)
        self.assertEqual(
            violations, [],
            f"存在 /api/workspace 写路径触及 billing：{violations}",
        )
        # 正向：计费路由全部位于 /api/platform/*。
        billing_routes = re.findall(
            r'@app\.(get|post|put|delete)\(\s*["\'](/api/platform/[^"\']*(?:plans|quotas|usage|summary|billing-events)[^"\']*)["\']',
            text,
        )
        self.assertTrue(billing_routes, "应能发现 billing 相关 /api/platform 路由")

    def test_forbidden_3_no_payment_invoice_deduct_endpoints(self):
        main_text = _read(_MAIN_PY)
        store_text = _read(_BILLING_STORE_PY)
        for text, label in ((main_text, "main.py"), (store_text, "billing_store.py")):
            code_hits = _code_hits(text, r"\b(payment|invoice|deduct)\b")
            self.assertEqual(
                code_hits, [],
                f"{label} 出现 payment/invoice/deduct 可执行代码（应仅评论/文档）：{code_hits}",
            )
        # 路由路径不得包含 payment/invoice/deduct。
        path_hits = re.findall(r'["\'](/api/[^"\']*(?:payment|invoice|deduct)[^"\']*)["\']', main_text)
        self.assertEqual(path_hits, [], f"发现 payment/invoice/deduct 端点路径：{path_hits}")

    def test_forbidden_4_calculate_no_value_event_or_roi(self):
        text = _read(_BILLING_STORE_PY)
        code_hits = _code_hits(text, r"\b(value_event|roi|estimated_value)\b")
        self.assertEqual(
            code_hits, [],
            f"billing_store 出现 value_event/roi/estimated_value 可执行代码：{code_hits}",
        )

    def test_forbidden_5_marketplace_not_implemented_for_billing(self):
        text = _read(_BILLING_STORE_PY)
        # billing_store 不得出现 marketplace 计费/分润逻辑。
        self.assertNotIn("marketplace", text)
        # main.py 的 billing 路由体内不得出现 marketplace 计费/分润逻辑。
        main_text = _read(_MAIN_PY)
        # 找出 billing-events/calculate 处理函数体并检查。
        m = re.search(r'(/api/platform/billing-events/calculate[\s\S]*?)(\n    @app\.|\ndef |\Z)', main_text)
        self.assertIsNotNone(m, "应找到 billing-events/calculate 路由")
        body = m.group(1)
        # marketplace 在 calculate 体内不得作为计费/分润逻辑出现。
        self.assertNotRegex(body, r"marketplace", "calculate 路由体不得含 marketplace 计费/分润逻辑")

    # ── G. Phase-9A 修正覆盖（is_unlimited / custom quota / seed 占位）────────
    def _calculate_dimensions(self, tenant_id: str) -> dict:
        """直连 BillingStore 估算，返回 plan 级汇总事件的 dimensions 明细。"""
        from app.billing_store import BillingStore

        events = BillingStore(self.db).calculate_billing_events(tenant_id)
        plan_event = next(e for e in events if e["subject_type"] == "plan")
        return plan_event["breakdown"]["dimensions"]

    def test_plan_is_unlimited_flag_zeroes_overage(self):
        # 需求 D1：plan 级 is_unlimited=true → 该维度 overage_qty=0 且 is_unlimited=true。
        self.client.post(
            "/api/platform/plans",
            headers=self.auth,
            json={
                "plan_code": "unlim",
                "name": "Unlim",
                "tier": "pro",
                "quota_rules": {
                    "quota_mode": "plan_default",
                    "is_unlimited": True,
                    "token_monthly_limit": 100,
                    "seat_limit": 2,
                    "capability_sources": ["official"],
                    "workflow_monthly_limit": 5,
                    "overage": {
                        "token_unit_price_per_1k": 0.5,
                        "seat_unit_price": 3,
                        "workflow_unit_price": 0.1,
                        "capability_unit_price": 0,
                    },
                    "currency": "USD",
                },
            },
        )
        self._seed_tenant("t-unlim", plan_tier="unlim")
        # 注入远超上限的用量（若非显式无限，应产生超量）。
        self._insert_usage("t-unlim", {"total_tokens": 1000, "model_name": "gpt-4"})
        dims = self._calculate_dimensions("t-unlim")
        self.assertEqual(dims["token"]["is_unlimited"], True)
        self.assertEqual(dims["token"]["overage"], 0)
        self.assertEqual(dims["token"]["amount"], 0.0)

    def test_enterprise_custom_unconfigured_is_zero_not_unlimited(self):
        # 需求 D2：Enterprise(quota_mode=custom) 未配置 quota 实例时，overage=0 且
        # breakdown 含 "configured": false（不再静默无限）。
        self._seed_tenant("t-entx", plan_tier="enterprise")
        # 注入海量 usage，确认不会因 limit=null 被当作无限而产生/跳过估算。
        self._insert_usage("t-entx", {"total_tokens": 10**12, "model_name": "gpt-4"})
        dims = self._calculate_dimensions("t-entx")
        self.assertEqual(dims["token"]["configured"], False)
        self.assertEqual(dims["token"]["is_unlimited"], False)
        self.assertEqual(dims["token"]["overage"], 0)
        self.assertEqual(dims["token"]["amount"], 0.0)

    def test_enterprise_custom_configured_instance_computes_overage(self):
        # 需求 D3：Enterprise 配置了具体 quota 实例（limit_value>0）时，按实例 limit 正常计算超量。
        self._seed_tenant("t-entc", plan_tier="enterprise")
        created = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={
                "tenant_id": "t-entc",
                "plan_id": "plan_enterprise",
                "quota_type": "token",
                "limit_value": 100,
            },
        ).json()
        self.assertEqual(created["is_unlimited"], False)
        self._insert_usage("t-entc", {"total_tokens": 1000, "model_name": "gpt-4"})
        dims = self._calculate_dimensions("t-entc")
        self.assertEqual(dims["token"]["configured"], True)
        self.assertEqual(dims["token"]["is_unlimited"], False)
        self.assertEqual(dims["token"]["limit"], 100)
        self.assertEqual(dims["token"]["overage"], 900)  # 1000 - 100

    def test_quota_is_unlimited_persisted_and_read_back(self):
        # 需求 D4：upsert_quota_limit / update_quota 透传 is_unlimited 并能在 _quota_dto 中读回。
        from app.billing_store import BillingStore

        self._seed_tenant("t-qi")
        store = BillingStore(self.db)
        created = store.upsert_quota_limit(
            tenant_id="t-qi",
            plan_id="plan_free",
            quota_type="token",
            limit_value=500,
            is_unlimited=True,
        )
        self.assertEqual(created["is_unlimited"], True)
        self.assertEqual(created["limit_value"], 500)

        # update_quota 显式置为 False。
        updated = store.update_quota(created["quota_id"], limit_value=500, is_unlimited=False)
        self.assertEqual(updated["is_unlimited"], False)

        # update_quota 不传 is_unlimited（None）→ 保持原值 False。
        updated2 = store.update_quota(updated["quota_id"], limit_value=999)
        self.assertEqual(updated2["is_unlimited"], False)
        self.assertEqual(updated2["limit_value"], 999)

        # 经 API 透传 is_unlimited=true。
        resp = self.client.post(
            "/api/platform/quotas",
            headers=self.auth,
            json={
                "tenant_id": "t-qi",
                "plan_id": "plan_free",
                "quota_type": "employee_seat",
                "limit_value": 10,
                "is_unlimited": True,
            },
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        self.assertEqual(resp.json()["is_unlimited"], True)

        # PUT 透传 is_unlimited=false。
        qid = resp.json()["quota_id"]
        put = self.client.put(
            f"/api/platform/quotas/{qid}",
            headers=self.auth,
            json={"limit_value": 10, "is_unlimited": False},
        )
        self.assertEqual(put.status_code, 200, put.text)
        self.assertEqual(put.json()["is_unlimited"], False)

    def test_seed_plans_have_quota_mode_and_correct_placeholders(self):
        # 需求 D5：三档 seed 的 quota_rules_json 含 quota_mode；Enterprise 的
        # token_monthly_limit 为 null、Pro 超量价为 null（占位，非写死真实价格）。
        from app.billing_store import BillingStore

        store = BillingStore(self.db)
        free = store.get_plan("plan_free")
        pro = store.get_plan("plan_pro")
        ent = store.get_plan("plan_enterprise")

        self.assertEqual(free["quota_rules"].get("quota_mode"), "plan_default")
        self.assertEqual(pro["quota_rules"].get("quota_mode"), "plan_default")
        self.assertEqual(ent["quota_rules"].get("quota_mode"), "custom")

        # Enterprise token_monthly_limit 为 null（待 Admin 按企业单独设置，不固定无限）。
        self.assertIsNone(ent["quota_rules"].get("token_monthly_limit"))
        self.assertIsNone(ent["quota_rules"].get("seat_limit"))

        # Pro 超量单价占位为 null（由总控决策席后续配置 $XX，非写死真实价格）。
        self.assertIsNone(pro["quota_rules"]["overage"]["token_unit_price_per_1k"])
        self.assertIsNone(pro["quota_rules"]["overage"]["seat_unit_price"])
        self.assertIsNone(pro["quota_rules"]["overage"]["workflow_unit_price"])

        # Free 超量价为真实 0（免费档，非占位 null）。
        self.assertEqual(free["quota_rules"]["overage"]["token_unit_price_per_1k"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
