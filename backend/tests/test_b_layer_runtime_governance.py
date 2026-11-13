# -*- coding: utf-8 -*-
"""B 层运行时治理边界 · T09 串联冒烟测试（纯离线）。

覆盖范围（对应 docs/architecture/b-layer-runtime-governance-impl-plan.md §4 T09
七条验收要点）：

1. 自治白名单六条件全满足 → ``needs_gate=False``，无 ``b.governance.gate`` 事件。
2. 逐类 G1–G8 触发 → 各自生成**禁词合规**的 ``GatePrompt``（断言全部文本不含
   ``FORBIDDEN_TERMS`` 任一命中，且通过 JSON Schema 校验）。
3. 注入含禁词模板 → 回退 "B 模拟 + C 取消" 二元闸，且回退闸本身也禁词合规。
4. 关闸（``enabled=False``）/ 加 ``whitelist.actions`` / G2 命中
   ``external_send.allow_list`` → 不弹。
5. G4：``estimated_tokens`` 跨 ``token_hard_limit`` → 弹；跨 ``warn_ratio`` → 仅提示不阻断。
6. **L2 不触发断言**：``governance.LOCKED_ACTIONS`` 长度与内容不变；B 层不引入
   ``budget_guard``、不解除 ``auto_modify_code`` / ``lift_human_approval_gate``。
7. 四个接线点均落 ``b.governance.gate`` 事件（mock event_log / DecisionSink 验证），
   且脱敏（payload 无路径 / Key / 参数）。

纯离线：仅 unittest + mock，不触真实 DB / 网络 / L2 写链路。
测试自身不触 L2、不依赖 ``budget_guard``（全仓无此模块）。
"""

from __future__ import annotations

import os

# 强制 mock 模式（与 conftest 一致），确保在导入 connector 等重依赖前设好，离线可跑。
os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")
os.environ.setdefault("CURIS_ENV", "test")
os.environ.setdefault("CURIS_IDENTITY_MODE", "test")

import unittest  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from app.gate_prompt import (  # noqa: E402
    FORBIDDEN_TERMS,
    GateOption,
    GatePrompt,
    render_gate_prompt,
    scan_forbidden_terms,
    validate_gate_prompt,
)
from app.gate_prompt_templates import (  # noqa: E402
    GATE_TEMPLATES,
    G_CATEGORIES,
    GATE_BUSINESS_CATEGORY,
    TemplateSpec,
)
from app.runtime_governance import (  # noqa: E402
    ActionContext,
    check_autonomy_boundary,
    evaluate,
    load_config,
    outcome_for_letter,
)
from app.runtime_governance_config import (  # noqa: E402
    DEFAULT_TOKEN_HARD_LIMIT,
    RuntimeGovernanceConfig,
    clear_config_cache,
)

# 四个接线点（最小改动文件）的治理 seam。
from app.content_workflow_runtime import ContentWorkflowRuntime  # noqa: E402
from app.governance import CompanyGovernance  # noqa: E402
from app.local_rd_toolset import LocalRDToolset  # noqa: E402
from app.real_rd_executor import RealRDExecutor  # noqa: E402


# --------------------------------------------------------------------------- #
# 测试夹具
# --------------------------------------------------------------------------- #
class FakeSink:
    """非交互 DecisionSink：固定返回某一决策字母（A/B/C/D）。"""

    def __init__(self, letter: str) -> None:
        self.letter = letter

    def ask(self, gate: object) -> str:  # 满足 runtime_checkable DecisionSink 协议
        return self.letter


# payload 脱敏断言用的泄露标记（路径 / Key / 参数），按 T09 第 7 条字面要求。
# 注意：不含 FORBIDDEN_TERMS 中的 "token"/"API" 等，因为 gate_label（如 "G4-token"）
# 属内部路由标签、非用户泄露，不在"无路径/Key/参数"的脱敏范围内。
_PAYLOAD_LEAK_MARKERS = (
    "/",          # 路径分隔符
    "secret",
    "password",
    "api_key",
    "Bearer",
    "Authorization",
)


class BLayerRuntimeGovernanceTest(unittest.TestCase):
    """T09 串联冒烟测试主套件。"""

    # ----------------------------------------------------------------- #
    # 工具方法
    # ----------------------------------------------------------------- #
    def _ctx_for_category(self, category: str, config: RuntimeGovernanceConfig) -> ActionContext:
        """构造能命中指定 G 类别且会被闸拦截的 ActionContext。"""
        if category == "G1":
            return ActionContext(action_type="deploy", external=True, irreversible=True)
        if category == "G2":
            return ActionContext(action_type="external_send", external=True, destination="partner-x")
        if category == "G3":
            return ActionContext(action_type="data_delete", protected_collections=("customers",))
        if category == "G4":
            return ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        if category == "G5":
            return ActionContext(action_type="billing_config")
        if category == "G6":
            return ActionContext(action_type="marketplace")
        if category == "G7":
            return ActionContext(action_type="permission")
        if category == "G8":
            return ActionContext(action_type="core_asset")
        raise AssertionError(f"unknown category {category}")

    def _assert_gate_compliant(self, gate: GatePrompt) -> None:
        """断言 GatePrompt 全文本不含禁词，且通过 JSON Schema 校验。"""
        self.assertIsInstance(gate, GatePrompt)
        texts = [gate.title, gate.business_risk, gate.one_line_consequence]
        for opt in gate.options:
            texts.append(opt.label)
            texts.append(opt.effect)
        for text in texts:
            hits = scan_forbidden_terms(text or "")
            self.assertEqual(
                hits, [],
                f"GatePrompt 文本命中禁词 {hits!r} -> {text!r}",
            )
        # JSON Schema 校验（maxLength / 2–4 选项 / required）不应抛错。
        validate_gate_prompt(gate)

    def _assert_payload_desensitized(self, payload: dict) -> None:
        """断言事件 payload 脱敏：仅含约定键，且无路径 / Key / 参数泄露。"""
        allowed_keys = {"gate_label", "category", "outcome", "needs_gate"}
        self.assertLessEqual(
            set(payload.keys()), allowed_keys,
            f"payload 含非约定键：{set(payload.keys()) - allowed_keys}",
        )
        for key, value in payload.items():
            if isinstance(value, str):
                lowered = value.lower()
                for marker in _PAYLOAD_LEAK_MARKERS:
                    self.assertNotIn(
                        marker.lower(), lowered,
                        f"payload[{key!r}] 可能泄露敏感数据：{value!r}",
                    )


# --------------------------------------------------------------------------- #
# 验收要点 1 · 自治白名单六条件
# --------------------------------------------------------------------------- #
class TestAutonomyBoundary(BLayerRuntimeGovernanceTest):
    def test_autonomy_boundary_all_satisfied_no_gate(self):
        cfg = RuntimeGovernanceConfig()
        ctx = ActionContext(
            action_type="tool_call",
            external=False,
            in_sandbox=True,
            in_path_whitelist=True,
            estimated_tokens=100,
            irreversible=False,
        )
        self.assertTrue(check_autonomy_boundary(ctx, cfg))
        dec = evaluate(ctx, cfg)
        self.assertFalse(dec.needs_gate)
        self.assertIsNone(dec.category)
        self.assertIsNone(dec.gate)
        self.assertEqual(dec.reason, "autonomy_boundary")

    def test_autonomy_boundary_each_violation_fails(self):
        cfg = RuntimeGovernanceConfig()
        base = dict(
            action_type="tool_call",
            external=False,
            in_sandbox=True,
            in_path_whitelist=True,
            estimated_tokens=100,
            irreversible=False,
        )
        violations = {
            "external": {**base, "external": True},
            "data_delete": {**base, "action_type": "data_delete"},
            "over_token": {**base, "estimated_tokens": DEFAULT_TOKEN_HARD_LIMIT + 1},
            "l2_action": {**base, "action_type": "billing_config"},
            "irreversible": {**base, "irreversible": True},
            "out_of_sandbox": {**base, "in_sandbox": False},
        }
        for name, kw in violations.items():
            with self.subTest(violation=name):
                ctx = ActionContext(**kw)
                self.assertFalse(
                    check_autonomy_boundary(ctx, cfg),
                    f"六条件违反项 {name} 应判定不在自治边界内",
                )

    def test_autonomy_boundary_no_event_recorded(self):
        """自治边界满足 → 接线点也不落 b.governance.gate 事件。"""
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(
            action_type="tool_call",
            external=False,
            in_sandbox=True,
            in_path_whitelist=True,
            estimated_tokens=100,
            irreversible=False,
        )
        letter = inst._governance_evaluate(ctx, FakeSink("A"), "issue-x", "T-autonomy")
        self.assertEqual(letter, "A")  # 自治放行，不经用户决策
        inst.event_log.record.assert_not_called()


# --------------------------------------------------------------------------- #
# 验收要点 2 · 逐类 G1–G8 均生成禁词合规 GatePrompt
# --------------------------------------------------------------------------- #
class TestG1G8ForbiddenCompliance(BLayerRuntimeGovernanceTest):
    def test_each_category_generates_compliant_gate(self):
        cfg = RuntimeGovernanceConfig()
        for category in G_CATEGORIES:
            with self.subTest(category=category):
                ctx = self._ctx_for_category(category, cfg)
                dec = evaluate(ctx, cfg)
                self.assertTrue(dec.needs_gate, f"{category} 应触发闸")
                self.assertEqual(dec.category, category)
                self.assertIsNotNone(dec.gate)
                self._assert_gate_compliant(dec.gate)
                # 业务风险类别（GatePrompt.category）须为设计约定的枚举值。
                self.assertEqual(dec.gate.category, GATE_BUSINESS_CATEGORY[category])


# --------------------------------------------------------------------------- #
# 验收要点 3 · 含禁词模板 → 回退 B+C 二元安全闸（且合规）
# --------------------------------------------------------------------------- #
class TestForbiddenTemplateFallback(BLayerRuntimeGovernanceTest):
    def test_forbidden_template_falls_back_to_binary_gate(self):
        bad_spec = TemplateSpec(
            title="请部署到沙箱 API 端点",
            business_risk="回滚部署会造成伤害",
            options_effects={"A": "直接继续", "B": "先模拟看效果", "C": "取消"},
            recommended="A",
            consequence="部署失败很难挽回",
        )
        # 注入含禁词模板：唯一禁词 enforcement 点应丢弃并回退二元安全闸。
        with patch.dict(GATE_TEMPLATES, {"G1": bad_spec}):
            gate = render_gate_prompt(
                "G1", ActionContext(action_type="deploy", external=True, irreversible=True)
            )
        # 回退闸：仅 B（模拟）+ C（取消），推荐 B。
        self.assertEqual([o.id for o in gate.options], ["B", "C"])
        self.assertEqual(gate.recommended, "B")
        # 回退闸本身亦禁词合规且通过 Schema 校验。
        self._assert_gate_compliant(gate)

    def test_fallback_gate_id_and_category_sane(self):
        bad_spec = TemplateSpec(
            title="需要调用 schema 接口",
            business_risk="包含 token 的敏感内容",
            options_effects={"A": "继续", "B": "模拟", "C": "取消"},
            recommended="A",
            consequence="diff 回滚失败",
        )
        with patch.dict(GATE_TEMPLATES, {"G2": bad_spec}):
            gate = render_gate_prompt(
                "G2", ActionContext(action_type="external_send", external=True)
            )
        self.assertTrue(gate.gate_id.startswith("fallback-"))
        self.assertEqual(gate.category, GATE_BUSINESS_CATEGORY["G2"])


# --------------------------------------------------------------------------- #
# 验收要点 4 · 关闸 / whitelist.actions / G2 allow_list → 不弹
# --------------------------------------------------------------------------- #
class TestGateDisabledWhitelistAllowList(BLayerRuntimeGovernanceTest):
    def test_disabled_gate_no_pop(self):
        cfg = RuntimeGovernanceConfig()
        cfg.gates.production_deploy.enabled = False
        dec = evaluate(ActionContext(action_type="deploy", external=True, irreversible=True), cfg)
        self.assertFalse(dec.needs_gate)
        self.assertEqual(dec.reason, "gate_disabled")

    def test_whitelist_actions_no_pop(self):
        cfg = RuntimeGovernanceConfig()
        cfg.whitelist.actions = ("deploy",)
        dec = evaluate(ActionContext(action_type="deploy", external=True, irreversible=True), cfg)
        self.assertFalse(dec.needs_gate)
        self.assertEqual(dec.reason, "whitelisted")

    def test_g2_allow_list_no_pop(self):
        cfg = RuntimeGovernanceConfig()
        cfg.gates.external_send.allow_list = ("trusted-partner",)
        dec = evaluate(
            ActionContext(action_type="external_send", external=True, destination="trusted-partner"),
            cfg,
        )
        self.assertFalse(dec.needs_gate)
        self.assertEqual(dec.reason, "whitelisted")

    def test_g2_non_allow_list_still_pops(self):
        cfg = RuntimeGovernanceConfig()
        cfg.gates.external_send.allow_list = ("trusted-partner",)
        dec = evaluate(
            ActionContext(action_type="external_send", external=True, destination="unknown"),
            cfg,
        )
        self.assertTrue(dec.needs_gate)


# --------------------------------------------------------------------------- #
# 验收要点 5 · G4 token 预算（硬限拦截 / warn_ratio 仅提示不阻断）
# --------------------------------------------------------------------------- #
class TestG4TokenBudget(BLayerRuntimeGovernanceTest):
    def test_over_hard_limit_pops(self):
        cfg = RuntimeGovernanceConfig()
        dec = evaluate(
            ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 5000),
            cfg,
        )
        self.assertTrue(dec.needs_gate)
        self.assertEqual(dec.category, "G4")
        self.assertIsNotNone(dec.gate)

    def test_at_hard_limit_not_blocked(self):
        cfg = RuntimeGovernanceConfig()
        dec = evaluate(
            ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT),
            cfg,
        )
        self.assertFalse(dec.needs_gate)

    def test_warn_ratio_zone_not_blocked(self):
        """跨 warn_ratio（但低于硬限）→ 仅提示不阻断（needs_gate=False）。"""
        cfg = RuntimeGovernanceConfig()
        warn_tokens = int(DEFAULT_TOKEN_HARD_LIMIT * cfg.budget.warn_ratio) + 1000
        self.assertLess(warn_tokens, DEFAULT_TOKEN_HARD_LIMIT)
        dec = evaluate(ActionContext(action_type="token_spend", estimated_tokens=warn_tokens), cfg)
        self.assertFalse(dec.needs_gate)


# --------------------------------------------------------------------------- #
# 验收要点 6 · L2 不触发断言（LOCKED_ACTIONS 不变 / 无 budget_guard / 不解锁锁）
# --------------------------------------------------------------------------- #
class TestL2NotTriggered(BLayerRuntimeGovernanceTest):
    def test_locked_actions_unchanged(self):
        before = list(CompanyGovernance.LOCKED_ACTIONS)
        # 触发 B 层各模块（含接线点）以验证运行中不会改动锁定清单。
        cfg = RuntimeGovernanceConfig()
        for category in G_CATEGORIES:
            evaluate(self._ctx_for_category(category, cfg), cfg)
        after = list(CompanyGovernance.LOCKED_ACTIONS)
        self.assertEqual(before, after)
        self.assertEqual(after, ["lift_human_approval_gate", "auto_modify_code"])

    def test_no_budget_guard_dependency(self):
        """全仓无 budget_guard 模块（临时桥以配置硬限 + 调用方累加实现 G4）。"""
        with self.assertRaises(ModuleNotFoundError):
            import budget_guard  # noqa: F401

    def test_runtime_governance_does_not_lift_locks(self):
        """B 层闸引擎不得 import / 调用解除 LOCKED_ACTIONS 的路径。"""
        app_dir = Path(__file__).resolve().parents[1] / "app"
        source = (app_dir / "runtime_governance.py").read_text(encoding="utf-8")
        self.assertNotIn(
            "budget_guard", source,
            "runtime_governance 不应依赖 budget_guard",
        )
        # 仅禁止「调用」解除锁（lift_human_approval_gate(）；模块 docstring 中以字符串
        # 声明「不解除」是合规的，不应误判。
        self.assertNotIn(
            "lift_human_approval_gate(", source,
            "runtime_governance 不得调用解除 A 层锁定",
        )

    def test_no_new_billing_multitenant_business_logic(self):
        """B 层模块不引入计费 / 多租户 / 商业逻辑（仅边界呈现与配置）。"""
        app_dir = Path(__file__).resolve().parents[1] / "app"
        for fname in (
            "runtime_governance.py",
            "gate_prompt.py",
            "gate_prompt_templates.py",
            "runtime_governance_config.py",
        ):
            source = (app_dir / fname).read_text(encoding="utf-8")
            for bad in ("budget_guard", "lift_human_approval_gate("):
                self.assertNotIn(bad, source, f"{fname} 不应含 {bad}")


# --------------------------------------------------------------------------- #
# 验收要点 7 · 四个接线点均落 b.governance.gate 事件（脱敏）
# --------------------------------------------------------------------------- #
class TestWiringPointsRecordEvents(BLayerRuntimeGovernanceTest):
    def test_real_rd_executor_records_gate_event(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)

        # sink 选 C → cancelled，落 b.governance.gate=cancelled。
        letter = inst._governance_evaluate(ctx, FakeSink("C"), "issue-1", "G4-token")
        self.assertEqual(letter, "C")
        inst.event_log.record.assert_called_once()
        call = inst.event_log.record.call_args
        self.assertEqual(call.kwargs["event_type"], "b.governance.gate")
        payload = call.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self._assert_payload_desensitized(payload)

        # sink 选 A → allowed，落 b.governance.gate=allowed。
        inst.event_log.reset_mock()
        letter = inst._governance_evaluate(ctx, FakeSink("A"), "issue-1", "G4-token")
        self.assertEqual(letter, "A")
        inst.event_log.record.assert_called_once()
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "allowed")
        self._assert_payload_desensitized(payload)

    def test_real_rd_executor_no_sink_fail_closed_cancels(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        # 无 sink → fail-closed 默认取消并落事件。
        letter = inst._governance_evaluate(ctx, None, "issue-1", "G4-token")
        self.assertEqual(letter, "C")
        inst.event_log.record.assert_called_once()
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self._assert_payload_desensitized(payload)

    def test_content_workflow_records_gate_event(self):
        inst = ContentWorkflowRuntime.__new__(ContentWorkflowRuntime)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()

        # G1 真实发布 → sink 选 C → 取消，返回 False 并落事件。
        cont = inst._governance_gate_before_publish(FakeSink("C"), "run-1", "selfuse")
        self.assertFalse(cont)
        inst.event_log.record.assert_called_once()
        call = inst.event_log.record.call_args
        self.assertEqual(call.kwargs["event_type"], "b.governance.gate")
        payload = call.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self._assert_payload_desensitized(payload)

        # sink 选 A → 允许，返回 True 并落事件。
        inst.event_log.reset_mock()
        cont = inst._governance_gate_before_publish(FakeSink("A"), "run-1", "selfuse")
        self.assertTrue(cont)
        inst.event_log.record.assert_called_once()
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "allowed")
        self._assert_payload_desensitized(payload)

    def test_governance_records_gate_event(self):
        inst = CompanyGovernance.__new__(CompanyGovernance)
        inst._event_log = MagicMock()
        proposal = {
            "proposal_id": "p1",
            "ceo_id": "ceo1",
            "tenant_id": "selfuse",
            "type_key": "billing_change",  # 映射到 G5
            "approved_by": "ceo1",
            "approved_at": "2026-07-20",
        }

        # 业务风险呈现 → sink 选 C → 中止写链路，落 b.governance.gate=cancelled。
        cont = inst._governance_present(proposal, FakeSink("C"))
        self.assertFalse(cont)
        inst._event_log.record.assert_called_once()
        call = inst._event_log.record.call_args
        self.assertEqual(call.kwargs["event_type"], "b.governance.gate")
        payload = call.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self._assert_payload_desensitized(payload)

        # sink 选 A → 继续，落 b.governance.gate=allowed。
        inst._event_log.reset_mock()
        cont = inst._governance_present(proposal, FakeSink("A"))
        self.assertTrue(cont)
        inst._event_log.record.assert_called_once()
        payload = inst._event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "allowed")
        self._assert_payload_desensitized(payload)

    def test_local_rd_toolset_precheck_passthrough(self):
        """本地工具为防御性 no-op 直通：不弹闸、不落事件（设计如此）。"""
        inst = LocalRDToolset.__new__(LocalRDToolset)
        try:
            inst._governance_precheck()
        except Exception as exc:  # noqa: BLE001
            self.fail(f"_governance_precheck 不应抛错：{exc}")
        # 本地工具上下文恒满足自治边界 → needs_gate=False（故无事件）。
        dec = evaluate(
            ActionContext(action_type="tool_call", external=False, in_sandbox=True, in_path_whitelist=True),
        )
        self.assertFalse(dec.needs_gate)

    def test_canonical_outcome_mapping_b_is_simulated(self):
        """中心映射 outcome_for_letter 规定 B→simulated（设计约定）。"""
        self.assertEqual(outcome_for_letter("A"), "allowed")
        self.assertEqual(outcome_for_letter("B"), "simulated")
        self.assertEqual(outcome_for_letter("C"), "cancelled")
        self.assertEqual(outcome_for_letter("D"), "alternative")

    def test_wiring_maps_b_to_simulated_via_outcome_for_letter(self):
        """统一 outcome 映射（③）：三个活跃接线点经中心 outcome_for_letter 把 B 映射为 simulated。

        设计中心映射 outcome_for_letter 规定 B→'simulated'；RealRDExecutor /
        ContentWorkflowRuntime / CompanyGovernance 的接线点已统一改调该中心函数，
        故 B 不再被内联映射为 allowed。本断言锁定统一后的真实映射。
        """
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        letter = inst._governance_evaluate(ctx, FakeSink("B"), "issue-1", "G4-token")
        self.assertEqual(letter, "B")
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "simulated")


# --------------------------------------------------------------------------- #
# ⑤ 阈值 / 禁词变更留痕守卫：把产品原则级铁律落为代码守卫
# --------------------------------------------------------------------------- #
class TestFrozenGovernanceThresholds(BLayerRuntimeGovernanceTest):
    """⑤ 阈值/禁词变更留痕守卫。

    把「产品原则级铁律」（docs/product-governance-principle.md，总控 2026-07-20 拍板）
    落为代码守卫：未来任何人改 ``runtime_governance_config.py`` / ``.json`` 偏离总控
    拍板值即测试失败。覆盖：token_hard_limit / protected_collections /
    default_decision_policy / FORBIDDEN_TERMS / load_config 默认值。确保 ⑤「变更须
    留痕 / 不漂移」可执行。
    """

    _FROZEN_FORBIDDEN_TERMS = frozenset(
        {
            "sandbox",
            "schema",
            "API",
            "token",
            "diff",
            "回滚",
            "部署",
            "端点",
            "进程",
            "权限位",
        }
    )

    def test_token_hard_limit_frozen(self):
        cfg = RuntimeGovernanceConfig()
        self.assertEqual(cfg.budget.token_hard_limit, 200000)

    def test_protected_collections_frozen(self):
        cfg = RuntimeGovernanceConfig()
        self.assertEqual(
            cfg.gates.data_deletion.protected_collections,
            ("customers", "orders", "employees"),
        )

    def test_default_decision_policy_frozen(self):
        cfg = RuntimeGovernanceConfig()
        self.assertEqual(cfg.default_decision_policy, "ask")

    def test_forbidden_terms_frozen(self):
        self.assertEqual(set(FORBIDDEN_TERMS), self._FROZEN_FORBIDDEN_TERMS)

    def test_load_config_defaults_frozen(self):
        clear_config_cache()
        cfg = load_config()
        self.assertEqual(cfg.budget.token_hard_limit, 200000)
        self.assertEqual(
            cfg.gates.data_deletion.protected_collections,
            ("customers", "orders", "employees"),
        )
        self.assertEqual(cfg.default_decision_policy, "ask")


if __name__ == "__main__":
    unittest.main(verbosity=2)
