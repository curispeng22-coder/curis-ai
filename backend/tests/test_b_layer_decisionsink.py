# -*- coding: utf-8 -*-
"""B 层运行时治理 · 真实 DecisionSink 后端机制测试桩（headless，纯离线）。

覆盖 ``docs/architecture/b-layer-runtime-governance-decisionsink.md`` 的 T-DS3 验收
要点（与 T-DS1 / T-DS2 对应）：

1. **闭环**：``evaluate(needs_gate=True)`` → 接线 helper 传 ``pending_sink`` → 返
   ``PendingDecisionRaised`` → ``resolve_decision(pid, "A")`` →
   ``store.get_letter(pid) == "A"``；引擎据此经 ``outcome_for_letter`` 映射
   outcome=allowed。
2. **fail-closed**：``get_letter`` 在 pending（未回填）/ 过期 / 缺失 / cancelled → ``"C"``；
   resolver 异常（非法 letter / 已终态 / 缺失）→ 抛 ``PendingDecisionError``，不泄露
   路径 / Key / 参数。
3. **共存**：``AutoApproveSink``→``"A"``、``CancellingSink``→``"C"``、默认 None→``"C"``，
   与 ``PendingDecisionSink`` 三态互不干扰。
4. **脱敏**：落库 ``gate_snapshot`` 为 GatePrompt JSON，断言不含 ``FORBIDDEN_TERMS``；
   ``b.governance.gate`` 事件 payload 无路径 / Key / 参数。
5. **L2 不触发断言**：无新计费 / 多租户 / 商业逻辑；``governance.LOCKED_ACTIONS`` 不变；
   ``decision_sink`` 模块不 import 任何解除锁的路径。

纯离线：仅 unittest + mock + 临时 sqlite 文件；不触真实 DB 服务 / 网络 / L2 写链路。
测试本身不依赖 ``test_local_rd_toolset.py`` 的 4 个失败用例，可独立通过。
"""

from __future__ import annotations

import os
import tempfile
import unittest  # noqa: E402

# 强制 mock 模式（与 conftest 一致），确保在导入 connector 等重依赖前设好，离线可跑。
os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")
os.environ.setdefault("CURIS_ENV", "test")
os.environ.setdefault("CURIS_IDENTITY_MODE", "test")

from unittest.mock import MagicMock  # noqa: E402

from app.decision_sink import (  # noqa: E402
    PendingDecisionError,
    PendingDecisionRaised,
    PendingDecisionSink,
    PendingDecisionStore,
    resolve_decision,
)
from app.gate_prompt import FORBIDDEN_TERMS  # noqa: E402
from app.runtime_governance import (  # noqa: E402
    ActionContext,
    AutoApproveSink,
    CancellingSink,
    evaluate,
    load_config,
    outcome_for_letter,
)
from app.runtime_governance_config import (  # noqa: E402
    DEFAULT_TOKEN_HARD_LIMIT,
    RuntimeGovernanceConfig,
)

# 三个活跃接线点（与 T-DS2 对应）的治理 seam。
from app.content_workflow_runtime import ContentWorkflowRuntime  # noqa: E402
from app.governance import CompanyGovernance  # noqa: E402
from app.real_rd_executor import RealRDExecutor  # noqa: E402


# payload 脱敏断言用的泄露标记（路径 / Key / 参数）。
_PAYLOAD_LEAK_MARKERS = (
    "/",
    "secret",
    "password",
    "api_key",
    "Bearer",
    "Authorization",
)


class DecisionSinkTestBase(unittest.TestCase):
    """共享夹具：临时 sqlite 目录 + 合规 GatePrompt 构造。"""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._db_path = os.path.join(self._tmp.name, "b_layer_pending_decisions.sqlite")
        self.cfg = RuntimeGovernanceConfig()
        self.store = PendingDecisionStore(self._db_path)
        self.sink = PendingDecisionSink(self.store)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _compliant_gate(self, action_type: str = "token_spend", **kw: object):
        """构造能命中闸且生成禁词合规 GatePrompt 的 ActionContext 对应的 GatePrompt。"""
        ctx_kwargs: dict[str, object] = {"action_type": action_type}
        if action_type == "token_spend":
            ctx_kwargs["estimated_tokens"] = DEFAULT_TOKEN_HARD_LIMIT + 1
        else:
            ctx_kwargs.update(kw)
        ctx = ActionContext(**ctx_kwargs)  # type: ignore[arg-type]
        decision = evaluate(ctx, self.cfg)
        self.assertTrue(decision.needs_gate, "应触发闸以产出 GatePrompt")
        assert decision.gate is not None
        return decision.gate


# --------------------------------------------------------------------------- #
# 验收要点 1 · 闭环（写入 → resolver 回填 → 引擎读回；与三接线点集成）
# --------------------------------------------------------------------------- #
class TestClosedLoop(DecisionSinkTestBase):
    def test_real_rd_executor_pending_loop(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)

        raised = inst._governance_evaluate(ctx, None, "issue-1", "G4-token", pending_sink=self.sink)
        self.assertIsInstance(raised, PendingDecisionRaised)
        record = self.store.get(raised.pending_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.status, "pending")
        # 落 b.governance.gate=pending 事件。
        inst.event_log.record.assert_called_once()
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "pending")

        # resolver 回填 A → 引擎读回 A（allowed）。
        resolve_decision(raised.pending_id, "A", store=self.store)
        self.assertEqual(self.store.get_letter(raised.pending_id), "A")
        self.assertEqual(outcome_for_letter("A"), "allowed")

    def test_content_workflow_pending_loop(self):
        inst = ContentWorkflowRuntime.__new__(ContentWorkflowRuntime)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        decision = evaluate(
            ActionContext(action_type="deploy", external=True, irreversible=True), inst._gov_config
        )
        self.assertTrue(decision.needs_gate)

        raised = inst._resolve_gate(
            decision, None, "run-1", "selfuse", "G1-deploy", pending_sink=self.sink
        )
        self.assertIsInstance(raised, PendingDecisionRaised)
        record = self.store.get(raised.pending_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.status, "pending")
        inst.event_log.record.assert_called_once()
        self.assertEqual(
            inst.event_log.record.call_args.kwargs["payload"]["outcome"], "pending"
        )

        resolve_decision(raised.pending_id, "B", store=self.store)
        # get_letter 返回填字母 B（引擎再经 outcome_for_letter 映射为 simulated）。
        self.assertEqual(self.store.get_letter(raised.pending_id), "B")
        self.assertEqual(outcome_for_letter("B"), "simulated")

    def test_governance_pending_loop(self):
        inst = CompanyGovernance.__new__(CompanyGovernance)
        inst._event_log = MagicMock()
        proposal = {
            "proposal_id": "p1",
            "ceo_id": "ceo1",
            "tenant_id": "selfuse",
            "type_key": "billing_change",  # G5
            "approved_by": "ceo1",
            "approved_at": "2026-07-20",
        }
        raised = inst._governance_present(proposal, None, pending_sink=self.sink)
        self.assertIsInstance(raised, PendingDecisionRaised)
        record = self.store.get(raised.pending_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.status, "pending")
        inst._event_log.record.assert_called_once()
        self.assertEqual(
            inst._event_log.record.call_args.kwargs["payload"]["outcome"], "pending"
        )

        resolve_decision(raised.pending_id, "D", store=self.store)
        self.assertEqual(self.store.get_letter(raised.pending_id), "D")
        self.assertEqual(outcome_for_letter("D"), "alternative")


# --------------------------------------------------------------------------- #
# 验收要点 2 · fail-closed（get_letter 单一真源 + resolver 异常）
# --------------------------------------------------------------------------- #
class TestFailClosed(DecisionSinkTestBase):
    def test_pending_unresolved_returns_c(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        self.assertEqual(self.store.get_letter(pid), "C")

    def test_resolved_returns_decision_letter(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        for letter in ("A", "B", "C", "D"):
            self.store.resolve(pid, letter)
            self.assertEqual(self.store.get_letter(pid), letter)
            # 重新 create 以测下一个字母（已终态不可重复 resolve）。
            pid = self.store.create(gate, correlation_id="x", gate_label="y")

    def test_missing_returns_c(self):
        self.assertEqual(self.store.get_letter("does-not-exist"), "C")

    def test_expired_returns_c(self):
        gate = self._compliant_gate()
        # ttl_seconds 为负 → expires_at 落在过去 → 过期。
        pid = self.store.create(gate, correlation_id="x", gate_label="y", ttl_seconds=-10)
        self.assertTrue(self.store.is_expired(pid))
        self.assertEqual(self.store.get_letter(pid), "C")

    def test_cancelled_returns_c(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        self.store.cancel(pid)
        record = self.store.get(pid)
        self.assertIsNotNone(record)
        self.assertEqual(record.status, "cancelled")
        self.assertEqual(self.store.get_letter(pid), "C")

    def test_resolve_illegal_letter_raises(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        with self.assertRaises(PendingDecisionError):
            self.store.resolve(pid, "Z")
        with self.assertRaises(PendingDecisionError):
            self.store.resolve(pid, "")

    def test_resolve_already_resolved_raises(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        self.store.resolve(pid, "A")
        with self.assertRaises(PendingDecisionError):
            self.store.resolve(pid, "B")  # 已终态

    def test_resolve_expired_raises(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y", ttl_seconds=-10)
        with self.assertRaises(PendingDecisionError):
            self.store.resolve(pid, "A")

    def test_cancel_missing_raises(self):
        with self.assertRaises(PendingDecisionError):
            self.store.cancel("nope")

    def test_cancel_already_resolved_idempotent_noop(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        self.store.resolve(pid, "A")
        # 已 resolved → cancel 幂等 no-op，返回既有记录（status 仍为 resolved）。
        record = self.store.cancel(pid)
        self.assertEqual(record.status, "resolved")
        self.assertEqual(self.store.get_letter(pid), "A")

    def test_resolve_decision_function_delegates(self):
        gate = self._compliant_gate()
        pid = self.store.create(gate, correlation_id="x", gate_label="y")
        record = resolve_decision(pid, "C", store=self.store)
        self.assertEqual(record.status, "resolved")
        self.assertEqual(record.decision, "C")


# --------------------------------------------------------------------------- #
# 验收要点 3 · 与既有 sink 共存（三态互不干扰）
# --------------------------------------------------------------------------- #
class TestSinkCoexistence(DecisionSinkTestBase):
    def test_pending_sink_returns_pending_id_nonblocking(self):
        gate = self._compliant_gate()
        pid = self.sink.ask(gate, correlation_id="c1", gate_label="G4-token")
        self.assertIsInstance(pid, str)
        self.assertEqual(len(pid), 32)  # uuid4 hex
        # 非阻塞：ask 后立即可 resolve（无需等待）。
        self.store.resolve(pid, "A")
        self.assertEqual(self.store.get_letter(pid), "A")

    def test_auto_approve_sink_returns_a(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        letter = inst._governance_evaluate(ctx, AutoApproveSink(), "issue-1", "G4-token")
        self.assertEqual(letter, "A")
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "allowed")

    def test_cancelling_sink_returns_c(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        letter = inst._governance_evaluate(ctx, CancellingSink(), "issue-1", "G4-token")
        self.assertEqual(letter, "C")
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")

    def test_no_sink_fail_closed_c(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        letter = inst._governance_evaluate(ctx, None, "issue-1", "G4-token")
        self.assertEqual(letter, "C")
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")

    def test_pending_sink_takes_precedence_over_decision_sink(self):
        """pending_sink 注入时优先于既有 decision_sink（按设计 §3.5 派发优先级）。"""
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        raised = inst._governance_evaluate(
            ctx, AutoApproveSink(), "issue-1", "G4-token", pending_sink=self.sink
        )
        self.assertIsInstance(raised, PendingDecisionRaised)
        self.assertEqual(self.store.get(raised.pending_id).status, "pending")


# --------------------------------------------------------------------------- #
# 验收要点 4 · 脱敏（gate_snapshot 无禁词；事件 payload 无路径/Key/参数）
# --------------------------------------------------------------------------- #
class TestDesensitization(DecisionSinkTestBase):
    def test_gate_snapshot_has_no_forbidden_terms(self):
        gate = self._compliant_gate("deploy", external=True, irreversible=True)
        pid = self.store.create(gate, correlation_id="c1", gate_label="G1-deploy")
        record = self.store.get(pid)
        self.assertIsNotNone(record)
        snapshot = record.gate_snapshot
        # 快照是合法 JSON。
        import json as _json
        parsed = _json.loads(snapshot)
        self.assertIn("gate_id", parsed)
        # 全文本不含任何禁词（含 options 的 label/effect）。
        text = snapshot.lower()
        for term in FORBIDDEN_TERMS:
            self.assertNotIn(term.lower(), text, f"gate_snapshot 命中禁词 {term!r}")

    def test_event_payload_desensitized(self):
        inst = ContentWorkflowRuntime.__new__(ContentWorkflowRuntime)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        decision = evaluate(
            ActionContext(action_type="deploy", external=True, irreversible=True), inst._gov_config
        )
        inst._resolve_gate(decision, None, "run-1", "selfuse", "G1-deploy", pending_sink=self.sink)
        payload = inst.event_log.record.call_args.kwargs["payload"]
        allowed_keys = {"gate_label", "category", "outcome", "needs_gate"}
        self.assertLessEqual(set(payload.keys()), allowed_keys)
        for value in payload.values():
            if isinstance(value, str):
                lowered = value.lower()
                for marker in _PAYLOAD_LEAK_MARKERS:
                    self.assertNotIn(marker.lower(), lowered)


# --------------------------------------------------------------------------- #
# 验收要点 5 · L2 不触发断言
# --------------------------------------------------------------------------- #
class TestL2NotTriggered(DecisionSinkTestBase):
    def test_locked_actions_unchanged(self):
        before = list(CompanyGovernance.LOCKED_ACTIONS)
        # 触发 B 层各模块（含接线点）以验证运行中不会改动锁定清单。
        for _ in range(3):
            self._compliant_gate()
        after = list(CompanyGovernance.LOCKED_ACTIONS)
        self.assertEqual(before, after)
        self.assertEqual(after, ["lift_human_approval_gate", "auto_modify_code"])

    def test_decision_sink_source_does_not_lift_locks(self):
        """decision_sink 模块不得 import / 调用解除 LOCKED_ACTIONS 的路径。"""
        import pathlib
        source = (
            pathlib.Path(__file__).resolve().parents[1] / "app" / "decision_sink.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("budget_guard", source, "decision_sink 不应依赖 budget_guard")
        self.assertNotIn(
            "lift_human_approval_gate(", source, "decision_sink 不得调用解除 A 层锁定"
        )
        self.assertNotIn("auto_modify_code", source, "decision_sink 不得触碰 auto_modify_code")

    def test_decision_sink_source_no_billing_multitenant_business(self):
        import pathlib
        source = (
            pathlib.Path(__file__).resolve().parents[1] / "app" / "decision_sink.py"
        ).read_text(encoding="utf-8")
        # 仅持久化脱敏快照 + 字母；不应引入计费/多租户/商业逻辑关键字。
        for bad in ("billing", "tenant", "BillingConfig", "multitenant"):
            self.assertNotIn(bad, source, f"decision_sink 不应含 {bad}")


# --------------------------------------------------------------------------- #
# 统一 outcome 映射（③）：B → simulated 一致性断言（与既有测试互补）
# --------------------------------------------------------------------------- #
class TestUnifiedOutcomeMapping(DecisionSinkTestBase):
    def test_outcome_for_letter_canonical(self):
        self.assertEqual(outcome_for_letter("A"), "allowed")
        self.assertEqual(outcome_for_letter("B"), "simulated")
        self.assertEqual(outcome_for_letter("C"), "cancelled")
        self.assertEqual(outcome_for_letter("D"), "alternative")
        # 未知字母 → fail-closed cancelled。
        self.assertEqual(outcome_for_letter("Z"), "cancelled")

    def test_wiring_b_maps_to_simulated(self):
        """三个活跃接线点经中心 outcome_for_letter 把 B 映射为 simulated（非 allowed）。"""
        for builder in (
            self._real_rd_b_letter,
            self._content_workflow_b_letter,
            self._governance_b_letter,
        ):
            with self.subTest(builder=builder.__name__):
                letter, outcome = builder()
                self.assertEqual(letter, "B")
                self.assertEqual(outcome, "simulated")

    def _real_rd_b_letter(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1)
        # 注入固定返 B 的 sink。
        letter = inst._governance_evaluate(ctx, _FixedLetterSink("B"), "issue-1", "G4-token")
        outcome = inst.event_log.record.call_args.kwargs["payload"]["outcome"]
        return letter, outcome

    def _content_workflow_b_letter(self):
        inst = ContentWorkflowRuntime.__new__(ContentWorkflowRuntime)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        decision = evaluate(
            ActionContext(action_type="deploy", external=True, irreversible=True), inst._gov_config
        )
        letter = inst._resolve_gate(decision, _FixedLetterSink("B"), "run-1", "selfuse", "G1-deploy")
        outcome = inst.event_log.record.call_args.kwargs["payload"]["outcome"]
        return ("B" if letter else "C"), outcome

    def _governance_b_letter(self):
        inst = CompanyGovernance.__new__(CompanyGovernance)
        inst._event_log = MagicMock()
        proposal = {
            "proposal_id": "p1",
            "ceo_id": "ceo1",
            "tenant_id": "selfuse",
            "type_key": "billing_change",
            "approved_by": "ceo1",
            "approved_at": "2026-07-20",
        }
        letter = inst._governance_present(proposal, _FixedLetterSink("B"))
        outcome = inst._event_log.record.call_args.kwargs["payload"]["outcome"]
        return ("B" if letter else "C"), outcome


# --------------------------------------------------------------------------- #
# 独立复核（A 收尾）· 默认 pending_sink=None 时三个接线点 helper 行为完全不变
# --------------------------------------------------------------------------- #
class TestDefaultBehaviorUnchanged(DecisionSinkTestBase):
    """独立复核：工程师是否真的让 pending_sink 默认 None 时行为不变。

    直调三处 helper（**不传** pending_sink），确认仍走既有 fail-closed C /
    cancelled，且**绝不**误触 ``b.governance.gate=pending``、不写入任何
    ``PendingDecisionRecord``。这是 ① 增量「默认行为零改动」的独立第三方断言。
    """

    def test_real_rd_evaluate_default_fail_closed_not_pending(self):
        inst = RealRDExecutor.__new__(RealRDExecutor)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        ctx = ActionContext(
            action_type="token_spend", estimated_tokens=DEFAULT_TOKEN_HARD_LIMIT + 1
        )
        # 不传 pending_sink → 应仍是既有 fail-closed 字母 C（非信号）。
        result = inst._governance_evaluate(ctx, None, "issue-1", "G4-token")
        self.assertEqual(result, "C")
        # 落的事件 outcome 是 cancelled，而非 pending。
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        # 未误触 pending：未向任何存储写入待决策记录。
        self.assertEqual(self.store.list_pending(), [])

    def test_content_workflow_default_fail_closed_not_pending(self):
        inst = ContentWorkflowRuntime.__new__(ContentWorkflowRuntime)
        inst.event_log = MagicMock()
        inst._gov_config = load_config()
        decision = evaluate(
            ActionContext(action_type="deploy", external=True, irreversible=True),
            inst._gov_config,
        )
        # 不传 pending_sink → 取消（False），不继续。
        result = inst._resolve_gate(decision, None, "run-1", "selfuse", "G1-deploy")
        self.assertFalse(result)
        payload = inst.event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self.assertEqual(self.store.list_pending(), [])

    def test_governance_present_default_fail_closed_not_pending(self):
        inst = CompanyGovernance.__new__(CompanyGovernance)
        inst._event_log = MagicMock()
        proposal = {
            "proposal_id": "p1",
            "ceo_id": "ceo1",
            "tenant_id": "selfuse",
            "type_key": "billing_change",
            "approved_by": "ceo1",
            "approved_at": "2026-07-20",
        }
        # 不传 pending_sink → 中止写链路（False）。
        result = inst._governance_present(proposal, None)
        self.assertFalse(result)
        payload = inst._event_log.record.call_args.kwargs["payload"]
        self.assertEqual(payload["outcome"], "cancelled")
        self.assertEqual(self.store.list_pending(), [])


class _FixedLetterSink:
    """固定返回某一决策字母的 DecisionSink（满足 runtime_checkable 协议）。"""

    def __init__(self, letter: str) -> None:
        self.letter = letter

    def ask(self, gate: object) -> str:
        return self.letter


if __name__ == "__main__":
    unittest.main(verbosity=2)
