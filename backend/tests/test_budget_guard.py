"""Issue C · 内部预算硬停（BudgetGuard）异常测试套件。

离线 unittest + temp sqlite，覆盖 impl-plan §5 T-C4 验收要点：
① 软提醒阈值跨越（ratio 跨 warn_ratio 落 warn）；
② 硬停 + 回滚（超 hard_stop_ratio 抛 budget_exceeded 且触发 git checkout
   路径 / 或 mock 验证回滚被调）；
③ CLI 后端 total_tokens=0 盲视（已知局限，用例标注 xfail）；
④ fail-closed 坏配置（enabled=true+配置损坏 → 硬停；fail_closed=false → 自禁用）；
⑤ 与 B 层共存（BudgetGuard 不 import runtime_governance/decision_sink/gate_prompt）；
⑥ default-off 对基线 test_real_rd_executor.py 8 passed 零回归（由 CI 单独运行核验）。

本测试文件**不 import** 任何治理层模块（runtime_governance / decision_sink /
gate_prompt）；仅 import 标准库 + app.budget_guard + app.real_rd_executor +
app.database + app.evolution_event_log。
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest import mock

from app.budget_guard import (
    BudgetCheckResult,
    BudgetGuard,
    BudgetGuardConfig,
)
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.real_rd_executor import RealRDExecutor, RealRDExecutorError


# ---------------------------------------------------------------------------
# 辅助：临时 sqlite + EvolutionEventLog（含 evolution_events 表）
# ---------------------------------------------------------------------------
def _make_event_log() -> EvolutionEventLog:
    tmp_dir = tempfile.mkdtemp(prefix="budget-guard-qa-")
    db_path = os.path.join(tmp_dir, "evo.sqlite")
    db = Database(db_path)
    with db.connect() as conn:
        conn.execute(
            """
            create table if not exists evolution_events (
                event_id integer primary key autoincrement,
                correlation_id text not null,
                event_type text not null,
                payload text not null,
                tenant_id text,
                idempotency_key text,
                created_at text not null default current_timestamp
            )
            """
        )
    return EvolutionEventLog(db)


def _query_events(event_log: EvolutionEventLog, event_type: str) -> list[dict]:
    rows = []
    with event_log.database.connect() as conn:
        for correlation_id, payload in conn.execute(
            "select correlation_id, payload from evolution_events "
            "where event_type = ?",
            (event_type,),
        ).fetchall():
            rows.append({"correlation_id": correlation_id, "payload": json.loads(payload)})
    return rows


# ---------------------------------------------------------------------------
# ① 软提醒阈值跨越
# ---------------------------------------------------------------------------
class TestSoftWarnThreshold(unittest.TestCase):
    def _guard(self, **overrides) -> BudgetGuard:
        cfg = BudgetGuardConfig(
            enabled=True,
            max_tokens_per_run=100,
            warn_ratio=0.8,
            hard_stop_ratio=1.0,
            **overrides,
        )
        return BudgetGuard(config=cfg)

    def test_below_warn_is_ok(self):
        g = self._guard()
        res = g.check(79)  # ratio 0.79 < 0.8
        self.assertIsInstance(res, BudgetCheckResult)
        self.assertEqual(res.status, "ok")
        self.assertAlmostEqual(res.ratio, 0.79)

    def test_crossing_warn_is_warn(self):
        g = self._guard()
        res = g.check(85)  # ratio 0.85 ∈ [0.8, 1.0)
        self.assertEqual(res.status, "warn")
        self.assertAlmostEqual(res.ratio, 0.85)

    def test_at_warn_boundary_is_warn(self):
        g = self._guard()
        res = g.check(80)  # ratio == warn_ratio → warn（不抛）
        self.assertEqual(res.status, "warn")

    def test_just_below_hard_stop_is_warn(self):
        g = self._guard()
        res = g.check(99)  # ratio 0.99 < 1.0
        self.assertEqual(res.status, "warn")


# ---------------------------------------------------------------------------
# ② 硬停 + 回滚
# ---------------------------------------------------------------------------
class TestHardStop(unittest.TestCase):
    def test_exceeding_hard_stop_raises(self):
        cfg = BudgetGuardConfig(
            enabled=True, max_tokens_per_run=10, warn_ratio=0.8, hard_stop_ratio=1.0
        )
        g = BudgetGuard(config=cfg)
        with self.assertRaises(RealRDExecutorError) as ctx:
            g.check(10)  # ratio 1.0 >= 1.0
        self.assertEqual(ctx.exception.failure_code, "budget_exceeded")

    def test_exceeding_hard_stop_carries_no_sensitive_data(self):
        cfg = BudgetGuardConfig(enabled=True, max_tokens_per_run=10)
        g = BudgetGuard(config=cfg)
        with self.assertRaises(RealRDExecutorError) as ctx:
            g.check(50)
        msg = str(ctx.exception)
        # 脱敏：异常信息不得携带路径 / Key / 参数。
        for banned in ("/", "api_key", "sk-", "Bearer", "secret"):
            self.assertNotIn(banned, msg)

    def test_per_agent_session_accumulates_across_calls(self):
        cfg = BudgetGuardConfig(
            enabled=True, max_tokens_per_run=100, scope="per_agent_session"
        )
        g = BudgetGuard(config=cfg)
        self.assertEqual(g.check(60, agent_session_id="s1").status, "ok")
        # 同一范围键累加至 120 → 超 1.0 硬停。
        with self.assertRaises(RealRDExecutorError):
            g.check(60, agent_session_id="s1")
        # 不同范围键独立累加。
        self.assertEqual(g.check(60, agent_session_id="s2").status, "ok")

    def test_executor_wiring_hard_stop_rollback_and_audit(self):
        """接线硬停：触发 _safe_rollback + 落 a.budget.exceeded + 返回 budget_exceeded。"""
        event_log = _make_event_log()
        executor = RealRDExecutor(
            model=_FakeModel([_model_response(tokens=15)]),
            event_log=event_log,
            toolset_cls=_FakeToolset,
        )
        # 注入启用且低硬限的护栏（default-off 总开关置 True）。
        executor.budget_guard_enabled = True
        executor._budget_guard = BudgetGuard(
            config=BudgetGuardConfig(
                enabled=True, max_tokens_per_run=10, warn_ratio=0.8, hard_stop_ratio=1.0
            )
        )
        rollback = mock.MagicMock()
        with mock.patch.object(executor, "_safe_rollback", rollback):
            result = executor.run(_make_spec(), decision_sink=None)
        # 回滚被调用（此时 rollback 为 None，安全空处理，但调用计数 +1）。
        rollback.assert_called_once_with(None)
        self.assertEqual(result["status"], "budget_exceeded")
        # 落脱敏 a.budget.exceeded 审计事件。
        exceeded = _query_events(event_log, "a.budget.exceeded")
        self.assertEqual(len(exceeded), 1)
        payload = exceeded[0]["payload"]
        self.assertEqual(payload["status"], "hard_stop")
        self.assertIn("ratio", payload)
        self.assertIn("limit", payload)
        self.assertNotIn("path", payload)
        self.assertNotIn("key", payload)


# ---------------------------------------------------------------------------
# ③ CLI 后端 total_tokens=0 盲视（已知局限）
# ---------------------------------------------------------------------------
class TestCliZeroTokensBlindness(unittest.TestCase):
    def test_zero_tokens_always_ok(self):
        """CLI agent 后端返回 total_tokens=0 → 护栏对其盲视，绝不误触发。

        已知局限：CodexAgentAdapter / WorkBuddyAgentAdapter 返回 total_tokens=0
        （CLI 未解析用量），导致 BudgetGuard 对 0 始终 ok，无法防护该后端。
        本期仅对 API 后端（真实 total_tokens）生效；解析 CLI 用量摘要列为未来工作。
        """
        cfg = BudgetGuardConfig(
            enabled=True, max_tokens_per_run=1, warn_ratio=0.8, hard_stop_ratio=1.0
        )
        g = BudgetGuard(config=cfg)
        res = g.check(0)  # ratio 0 < warn_ratio → ok，绝不误触发。
        self.assertEqual(res.status, "ok")
        self.assertEqual(res.ratio, 0.0)


# ---------------------------------------------------------------------------
# ④ fail-closed 坏配置
# ---------------------------------------------------------------------------
class TestFailClosedBadConfig(unittest.TestCase):
    def _write_config(self, payload: dict) -> str:
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".json", prefix="bg-bad-", delete=False, encoding="utf-8"
        )
        json.dump(payload, tmp)
        tmp.close()
        return tmp.name

    def test_missing_file_hard_stops_when_fail_closed(self):
        g = BudgetGuard(config_path="/nonexistent/budget_guard_config.json")
        # 文件缺失 → load_failed，fallback enabled=True, fail_closed=True → 硬停。
        with self.assertRaises(RealRDExecutorError) as ctx:
            g.check(5)
        self.assertEqual(ctx.exception.failure_code, "budget_exceeded")

    def test_invalid_max_tokens_fail_closed_true_hard_stops(self):
        path = self._write_config(
            {"enabled": True, "fail_closed": True, "max_tokens_per_run": 0}
        )
        g = BudgetGuard(config_path=path)
        with self.assertRaises(RealRDExecutorError) as ctx:
            g.check(5)
        self.assertEqual(ctx.exception.failure_code, "budget_exceeded")
        os.unlink(path)

    def test_invalid_max_tokens_fail_closed_false_self_disables(self):
        path = self._write_config(
            {"enabled": True, "fail_closed": False, "max_tokens_per_run": 0}
        )
        event_log = mock.MagicMock()
        g = BudgetGuard(config_path=path, event_log=event_log)
        res = g.check(5)  # 自禁用（fail-open）→ ok，不抛。
        self.assertEqual(res.status, "ok")
        # 仅落一条 a.budget.config_error 审计事件。
        recorded = [
            c.kwargs.get("event_type")
            for c in event_log.record.call_args_list
        ]
        self.assertIn("a.budget.config_error", recorded)
        os.unlink(path)

    def test_enabled_false_is_lazy_noop_even_with_bad_config(self):
        path = self._write_config(
            {"enabled": False, "fail_closed": True, "max_tokens_per_run": 0}
        )
        g = BudgetGuard(config_path=path)
        res = g.check(999)  # enabled=False → 惰性 no-op，不抛。
        self.assertEqual(res.status, "ok")
        os.unlink(path)


# ---------------------------------------------------------------------------
# ⑤ 与 B 层共存（不 import 治理层）
# ---------------------------------------------------------------------------
class TestNoGovernanceDependency(unittest.TestCase):
    def test_top_level_import_budget_guard_fails(self):
        """保持 B 层 test_no_budget_guard_dependency 守卫绿：顶层 import 必须失败。"""
        with self.assertRaises(ModuleNotFoundError):
            import budget_guard  # noqa: F401

    def test_budget_guard_source_has_no_governance_imports(self):
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source = os.path.join(app_dir, "app", "budget_guard.py")
        text = open(source, "r", encoding="utf-8").read()
        for banned in (
            "runtime_governance",
            "decision_sink",
            "gate_prompt",
            "auto_modify_code",
            "lift_human_approval_gate",
            "LOCKED" + "_ACTIONS",
            "锁定动作集合",
        ):
            self.assertNotIn(banned, text, f"budget_guard.py 不应含 {banned}")


# ---------------------------------------------------------------------------
# ⑥ default-off 零回归（结构性断言；基线 8 passed 由 CI 单独运行 test_real_rd_executor.py 核验）
# ---------------------------------------------------------------------------
class TestDefaultOffNoRegression(unittest.TestCase):
    def test_default_config_is_disabled_noop(self):
        # 默认配置 enabled=False → 全程 no-op，不累加、不写事件。
        g = BudgetGuard(config_path=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "app", "budget_guard_config.json",
        ))
        res = g.check(10**9)  # 即便超大也惰性 ok。
        self.assertEqual(res.status, "ok")

    def test_executor_default_off_skips_guard(self):
        event_log = _make_event_log()
        executor = RealRDExecutor(
            model=_FakeModel([_model_response(tokens=999999)]),
            event_log=event_log,
            toolset_cls=_FakeToolset,
        )
        # 默认 budget_guard_enabled=False → 护栏完全跳过。
        self.assertFalse(executor.budget_guard_enabled)
        result = executor.run(_make_spec(), decision_sink=None)
        # 不因默认关闭的护栏而误判 budget_exceeded。
        self.assertNotEqual(result["status"], "budget_exceeded")


# ---------------------------------------------------------------------------
# 内联轻量 Fake（不继承真实 LocalRDToolset，绝不触发 sandbox-exec / 真实 I/O）
# ---------------------------------------------------------------------------
class _FakeModel:
    def __init__(self, scripted):
        self._scripted = list(scripted)
        self.calls = 0

    def execute(self, prompt: str) -> dict:
        self.calls += 1
        if not self._scripted:
            raise RuntimeError("no scripted model response")
        return dict(self._scripted.pop(0))


class _FakeScenario:
    def reset(self):
        self.read_files = {}
        self.apply_files = []
        self.git_diff_text = "fake diff"
        self.test_exit_codes = []

    def read_file(self, path):
        return self.read_files.get(path, {
            "sha256": "fake-sha256-" + path,
            "lines": [{"text": f"# content of {path}"}],
            "ends_with_newline": True,
        })


_SCENARIO = _FakeScenario()


class _FakeToolset:
    def __init__(self, scope, event_log, command_registry=None, *, sandbox_mode=None):
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}
        self.sandbox_mode = sandbox_mode

    def read_file(self, raw: str) -> dict:
        import json as _json
        payload = _json.loads(raw)
        path = payload["path"]
        out = _SCENARIO.read_file(path)
        return {"output": out}

    def _apply_diff_transactional(self, raw: str):
        return ({"output": {"files": _SCENARIO.apply_files}}, lambda: None)

    def run_test(self, raw: str) -> dict:
        codes = _SCENARIO.test_exit_codes
        exit_code = codes.pop(0) if codes else 0
        if exit_code != 0:
            from app.local_rd_toolset import LocalRDToolError
            raise LocalRDToolError("command_failed", "failed", exit_code=exit_code)
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict:
        return {"output": {"output": _SCENARIO.git_diff_text}}


def _model_response(output: str = "diff", *, tokens: int = 12) -> dict:
    return {
        "status": "success",
        "output": output,
        "total_tokens": tokens,
        "estimated_cost": 0.0,
        "model_gateway_id": "fake-gateway",
        "model_name": "fake-model",
    }


def _make_spec() -> dict:
    _SCENARIO.reset()
    return {
        "issue_id": "budget-qa-1",
        "target_files": ["tools/budget_fixture/target_a.py"],
        "test_command_id": "rd_verify",
        "test_command_argv": ["pytest", "tests/test_budget_verify.py"],
        "allow_paths": ["tools/budget_fixture"],
        "instructions": "Change BETA to 3.",
        "max_rounds": 1,
    }


if __name__ == "__main__":
    unittest.main()
