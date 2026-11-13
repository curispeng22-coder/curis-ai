"""RealRDExecutor 独立、可重复单元测试（QA 验收闸门）。

设计目标：脱离实时模型网关、脱离 macOS sandbox-exec，用 Fake 对象验证
``RealRDExecutor`` 的编排逻辑与脱敏契约。

实现方式（严格遵循 team-lead 契约）：
- ``FakeModel``：通过构造函数注入 ``RealRDExecutor(model, ...)``，脚本化返回
  合法 diff / 抛异常模拟网关瞬时错误 / 返回非 diff 文本模拟非法输出。
- ``FakeToolset``：通过 ``toolset_cls=`` 注入，构造函数签名为
  ``__init__(self, scope, event_log, command_registry=None)``，与 executor 的
  ``_build_toolsets`` 调用约定完全一致；**不继承真实 LocalRDToolset**，因此绝不
  触发真实 ``sandbox-exec`` / ``patch`` / 真实文件 I/O。
- 事件日志：使用真实临时 sqlite + ``EvolutionEventLog``（含 ``evolution_events``
  表），使单主占锁（``_claim_once``）与汇总（``_record_run_summary``）路径被真实执行。

覆盖用例：
1. ``test_normalize_diff_counts``     —— ``_normalize_diff_counts`` 纯函数单测。
2. ``test_parse_diff_strips_noise``   —— ``_parse_diff`` 剥离引导说明 + 尾部围栏。
3. ``test_run_happy_path``            —— 正常闭环：succeeded + diff + files。
4. ``test_run_model_gateway_error_retryable`` —— 网关瞬时错误可重试。
5. ``test_run_invalid_diff_retry_then_fail``  —— 非法 diff 重试耗尽后返回 failed。
6. ``test_desensitized_fatal``        —— 不可重试致命错误脱敏为 ``RealRDExecutorError``。
7. ``test_run_test_failure_retry_then_succeed``—— 测试失败可重试（command_failed）。
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from typing import Any

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import LocalRDToolError, SandboxMode
from app.real_rd_executor import RealRDExecutor, RealRDExecutorError


# ---------------------------------------------------------------------------
# 被测目标文件（相对 workspace 根）与已知内容；diff 据此手工构造。
# ---------------------------------------------------------------------------
TARGET = "tools/real_rd_fixture/target_a.py"

# 将 ``BETA = 2`` 改为 ``BETA = 3`` 的合法 unified diff（供 FakeModel 返回）。
VALID_DIFF_OK = (
    f"--- a/{TARGET}\n"
    f"+++ b/{TARGET}\n"
    "@@ -1,2 +1,2 @@\n"
    " ALPHA = 1\n"
    "-BETA = 2\n"
    "+BETA = 3\n"
)

# 脱敏 grep 的禁用词（路径 / 密钥 / 敏感串）。
BANNED_TOKENS = ("/Users", "/home", "api_key", "sk-", "Bearer", ".env", TARGET)


# ---------------------------------------------------------------------------
# FakeModel：脚本化模型网关适配器（构造函数注入，非工具集）。
# 每个元素可以是 dict（直接作为 execute 返回值）或 Exception 实例
# （execute 时抛出，模拟网关瞬时错误）。
# ---------------------------------------------------------------------------
class FakeModel:
    def __init__(self, scripted: list[Any]) -> None:
        self._scripted = list(scripted)
        self.calls = 0

    def execute(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        if not self._scripted:
            raise RuntimeError("no scripted model response available")
        item = self._scripted.pop(0)
        if isinstance(item, Exception):
            raise item
        if isinstance(item, dict):
            return dict(item)
        raise RuntimeError(f"unexpected scripted item: {type(item)!r}")


# ---------------------------------------------------------------------------
# FakeScenario：单次 ``run`` 内三个 FakeToolset 实例共享的脚本化行为。
# 因为 executor 在 ``run`` 内部构造 read/write/git 三个独立工具集实例，而构造函数
# 只接受 (scope, event_log, command_registry)，故用模块级共享场景对象承载脚本。
# ---------------------------------------------------------------------------
class FakeScenario:
    def reset(self) -> None:
        self.read_files: dict[str, dict[str, Any]] = {}
        self.apply_files: list[dict[str, str]] = []
        self.git_diff_text: str = ""
        self.test_exit_codes: list[int] = []
        self.read_error: LocalRDToolError | None = None
        self.apply_error: LocalRDToolError | None = None
        self.git_error: LocalRDToolError | None = None
        self.test_error: LocalRDToolError | None = None


SCENARIO = FakeScenario()


def _noop_rollback() -> None:
    return None


# ---------------------------------------------------------------------------
# FakeToolset：独立 Fake（不继承真实 LocalRDToolset，绝不触发 sandbox-exec）。
# 构造函数签名严格匹配 executor 的 ``_build_toolsets``：
# ``__init__(self, scope, event_log, command_registry=None)``。
# ---------------------------------------------------------------------------
class FakeToolset:
    def __init__(
        self,
        scope: Any,
        event_log: Any,
        command_registry: dict[str, Any] | None = None,
        *,
        sandbox_mode: Any = None,
    ) -> None:
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}
        self.sandbox_mode = sandbox_mode

    def read_file(self, raw: str) -> dict[str, Any]:
        if SCENARIO.read_error is not None:
            raise SCENARIO.read_error
        payload = json.loads(raw)
        path = payload["path"]
        out = SCENARIO.read_files.get(path)
        if out is None:
            out = {
                "sha256": "fake-sha256-" + path,
                "lines": [{"text": f"# content of {path}"}],
                "ends_with_newline": True,
            }
        return {"output": out}

    def _apply_diff_transactional(self, raw: str) -> tuple[dict[str, Any], Any]:
        if SCENARIO.apply_error is not None:
            raise SCENARIO.apply_error
        return ({"output": {"files": SCENARIO.apply_files}}, _noop_rollback)

    def run_test(self, raw: str) -> dict[str, Any]:
        if SCENARIO.test_error is not None:
            raise SCENARIO.test_error
        payload = json.loads(raw)
        command_id = payload["command_id"]
        if command_id not in self.command_registry:
            raise LocalRDToolError(
                "command_not_registered", "command_id is not registered"
            )
        codes = SCENARIO.test_exit_codes
        exit_code = codes.pop(0) if codes else 0
        if exit_code != 0:
            raise LocalRDToolError(
                "command_failed", "registered command failed", exit_code=exit_code
            )
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict[str, Any]:
        if SCENARIO.git_error is not None:
            raise SCENARIO.git_error
        payload = json.loads(raw)
        if payload.get("operation") != "diff":
            raise LocalRDToolError(
                "git_operation_forbidden", "git operation is not allowed"
            )
        return {"output": {"output": SCENARIO.git_diff_text}}


# ---------------------------------------------------------------------------
# 辅助构造器
# ---------------------------------------------------------------------------
def model_response(output: str, *, tokens: int = 12) -> dict[str, Any]:
    """构造符合 ModelGatewayAdapter.execute 返回形状的脚本响应。"""
    prompt_tokens = max(tokens - 1, 1)
    completion_tokens = tokens - prompt_tokens
    unit_price_input = 0.000001
    unit_price_output = 0.000002
    return {
        "status": "success",
        "output": output,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": tokens,
        "estimated_cost": round(
            prompt_tokens * unit_price_input
            + completion_tokens * unit_price_output,
            8,
        ),
        "model_gateway_id": "fake-gateway",
        "model_name": "fake-model",
        "provider_id": "fake-provider",
        "unit_price_input": unit_price_input,
        "unit_price_output": unit_price_output,
        "price_version": "test-v1",
        "currency": "USD",
        "cost_source": "focused_test",
        "http_status": 200,
        "latency_ms": 1,
        "outbound_attempted": True,
    }


def make_event_log() -> EvolutionEventLog:
    """创建临时 sqlite + EvolutionEventLog（含 evolution_events 表）。"""
    tmp_dir = tempfile.mkdtemp(prefix="real-rd-qa-")
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


class RealRDExecutorQATestCase(unittest.TestCase):
    def setUp(self) -> None:
        SCENARIO.reset()
        self.event_log = make_event_log()

    # ------------------------------------------------------------------ #
    def _make_spec(
        self,
        *,
        issue_id: str = "real-rd-qa-1",
        max_rounds: int = 3,
        target_files: list[str] | None = None,
        allow_paths: list[str] | None = None,
        test_command_id: str = "rd_verify",
        test_command_argv: tuple[str, ...] = ("pytest", "tests/test_real_rd_verify.py"),
        instructions: str = "Change BETA to 3.",
    ) -> dict[str, Any]:
        return {
            "issue_id": issue_id,
            "target_files": target_files or [TARGET],
            "test_command_id": test_command_id,
            "test_command_argv": list(test_command_argv),
            "instructions": instructions,
            "max_rounds": max_rounds,
            "allow_paths": allow_paths or [TARGET, "backend/tests/test_real_rd_verify.py"],
        }

    # ------------------------------------------------------------------ #
    # 用例 1：_normalize_diff_counts 纯函数单测
    # ------------------------------------------------------------------ #
    def test_normalize_diff_counts(self) -> None:
        # (a) 头部计数错误但 body 正确（实际 9/9 行）→ 重写后计数 == body
        #     真实行数，且 old_start 保持不变。
        diff_a = (
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -37,8 +37,8 @@\n"
            " line_a\n"
            " line_b\n"
            " line_c\n"
            " line_d\n"
            " line_e\n"
            " line_f\n"
            " line_g\n"
            " line_h\n"
            " line_i\n"
        )
        normalized_a = RealRDExecutor._normalize_diff_counts(diff_a)
        self.assertIn("@@ -37,9 +37,9 @@", normalized_a)
        self.assertNotIn("@@ -37,8", normalized_a)

        # (b) 多 hunk：每个头计数错误、body 正确 → 分别重算。
        diff_b = (
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -10,1 +10,1 @@\n"
            " a\n"
            "-b\n"
            "+c\n"
            "+d\n"
            "@@ -50,5 +50,5 @@\n"
            " x\n"
            "-y\n"
            " z\n"
        )
        normalized_b = RealRDExecutor._normalize_diff_counts(diff_b)
        # 第一 hunk：consumed=2, produced=3 → 重写；old_start 10 不变。
        self.assertIn("@@ -10,2 +10,3 @@", normalized_b)
        self.assertNotIn("@@ -10,1", normalized_b)
        # 第二 hunk：consumed=3, produced=2 → 重写；old_start 50 不变。
        self.assertIn("@@ -50,3 +50,2 @@", normalized_b)
        self.assertNotIn("@@ -50,5", normalized_b)

        # (c) 含空 context 行（仅前导空格）：应被计入计数，old_start 不变。
        diff_c = (
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -1,2 +1,3 @@\n"
            " a\n"
            " \n"
            " b\n"
        )
        normalized_c = RealRDExecutor._normalize_diff_counts(diff_c)
        # body: " a"(ctx) / " "(空ctx) / " b"(ctx) → consumed=3, produced=3
        self.assertIn("@@ -1,3 +1,3 @@", normalized_c)
        # 空 context 行（" \n"）必须被保留并计入，而非被跳过。
        self.assertIn("\n \n", normalized_c)

    # ------------------------------------------------------------------ #
    # 用例 2：_parse_diff 剥离引导说明 + 尾部 ``` 围栏，并归一计数
    # ------------------------------------------------------------------ #
    def test_parse_diff_strips_noise(self) -> None:
        raw = (
            "Sure! Here is the unified diff you requested for the issue:\n\n"
            f"--- a/{TARGET}\n"
            f"+++ b/{TARGET}\n"
            "@@ -1,2 +1,2 @@\n"
            " ALPHA = 1\n"
            "-BETA = 2\n"
            "+BETA = 3\n"
            "\n"
            "```\n"
            "Hope this helps!\n"
        )
        cleaned = RealRDExecutor._parse_diff(raw)
        self.assertTrue(cleaned.startswith(f"--- a/{TARGET}"))
        self.assertIn("ALPHA = 1", cleaned)
        self.assertIn("+BETA = 3", cleaned)
        # 引导说明与尾部围栏/客套话均被剥离
        self.assertNotIn("Sure!", cleaned)
        self.assertNotIn("Hope this helps", cleaned)
        self.assertNotIn("```", cleaned)
        # body 为 2/2，计数归一后头保持不变
        self.assertIn("@@ -1,2 +1,2 @@", cleaned)

    # ------------------------------------------------------------------ #
    # 用例 3：正常闭环（happy path）
    # ------------------------------------------------------------------ #
    def test_run_happy_path(self) -> None:
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        SCENARIO.apply_files = [
            {
                "path": TARGET,
                "preimage_hash": "pre-hash-abc",
                "postimage_hash": "post-hash-xyz",
            }
        ]
        SCENARIO.test_exit_codes = [0]
        SCENARIO.git_diff_text = VALID_DIFF_OK

        spec = self._make_spec()
        model = FakeModel([model_response(VALID_DIFF_OK)])
        executor = RealRDExecutor(model, self.event_log, toolset_cls=FakeToolset)
        result = executor.run(spec)

        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["test_exit_code"], 0)
        self.assertIn("+BETA = 3", result["diff_text"])
        self.assertTrue(result["files"])
        self.assertEqual(result["files"][0]["path"], TARGET)
        self.assertEqual(result["rounds"], 1)
        self.assertEqual(model.calls, 1)
        self.assertEqual(result["total_tokens"], 12)
        self.assertEqual(result["model_name"], "fake-model")

        # 单主占锁（started）与汇总（succeeded）事件已真实落库。
        event_types = [event["event_type"] for event in self.event_log.get_all()]
        self.assertIn("real_rd.run.started", event_types)
        self.assertIn("real_rd.run.succeeded", event_types)

    # ------------------------------------------------------------------ #
    # 用例 4：网关瞬时错误可重试（首轮抛异常，次轮成功）
    # ------------------------------------------------------------------ #
    def test_run_model_gateway_error_retryable(self) -> None:
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        SCENARIO.apply_files = [
            {
                "path": TARGET,
                "preimage_hash": "pre-hash-abc",
                "postimage_hash": "post-hash-xyz",
            }
        ]
        SCENARIO.test_exit_codes = [0]
        SCENARIO.git_diff_text = VALID_DIFF_OK

        # 第一次 execute 抛异常模拟网关瞬时错误；第二次返回合法 diff。
        model = FakeModel(
            [
                RuntimeError("simulated gateway timeout / network blip"),
                model_response(VALID_DIFF_OK, tokens=7),
            ]
        )
        spec = self._make_spec(issue_id="real-rd-qa-gw-retry", max_rounds=3)
        executor = RealRDExecutor(model, self.event_log, toolset_cls=FakeToolset)
        result = executor.run(spec)

        # 网关瞬时错误未被当作致命 RealRDExecutorError 抛出，而是重试并成功。
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(model.calls, 2)
        self.assertEqual(result["rounds"], 2)

    # ------------------------------------------------------------------ #
    # 用例 5：非法 diff 重试耗尽后返回 failed（不泄漏非脱敏异常）
    # ------------------------------------------------------------------ #
    def test_run_invalid_diff_retry_then_fail(self) -> None:
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        # 始终返回非 diff 文本 → 每轮 _parse_diff 抛 _RoundFailed → 重试耗尽。
        model = FakeModel(
            [
                model_response("I am not a diff, just some prose explaining things."),
                model_response("Still not a diff. Maybe try `# TODO` later?"),
                model_response("Definitely not a unified diff."),
            ]
        )
        spec = self._make_spec(issue_id="real-rd-qa-invalid", max_rounds=3)
        executor = RealRDExecutor(model, self.event_log, toolset_cls=FakeToolset)

        # 轮次耗尽后应返回 failed 结果，而非抛出未脱敏异常。
        result = executor.run(spec)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["diff_text"], "")
        self.assertEqual(result["rounds"], 3)
        self.assertEqual(model.calls, 3)

    # ------------------------------------------------------------------ #
    # 用例 6：不可重试致命错误 → 脱敏为 RealRDExecutorError
    # ------------------------------------------------------------------ #
    def test_desensitized_fatal(self) -> None:
        # 让 read 工具抛不可重试的 LocalRDToolError（如 sensitive_value_detected）。
        SCENARIO.read_error = LocalRDToolError(
            "sensitive_value_detected",
            "the real tool would refuse here with internal detail",
        )
        model = FakeModel([model_response(VALID_DIFF_OK)])
        spec = self._make_spec(issue_id="real-rd-qa-fatal")
        executor = RealRDExecutor(model, self.event_log, toolset_cls=FakeToolset)

        with self.assertRaises(RealRDExecutorError) as ctx:
            executor.run(spec)
        error = ctx.exception
        # 脱敏码：固定 failure_code，而非原始内部错误类型。
        self.assertEqual(error.failure_code, "tool_rejected")
        # message 不得泄露路径 / 密钥 / 内部错误类型。
        message = str(error)
        for banned in BANNED_TOKENS:
            self.assertNotIn(banned, message)
        self.assertNotIn("sensitive_value_detected", message)

    # ------------------------------------------------------------------ #
    # 用例 7（补充）：测试失败（command_failed）可重试，次轮成功
    # ------------------------------------------------------------------ #
    def test_run_test_failure_retry_then_succeed(self) -> None:
        SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        SCENARIO.apply_files = [
            {
                "path": TARGET,
                "preimage_hash": "pre-hash-abc",
                "postimage_hash": "post-hash-xyz",
            }
        ]
        # 首轮 run_test 退出码 1（可重试），次轮 0（成功）。
        SCENARIO.test_exit_codes = [1, 0]
        SCENARIO.git_diff_text = VALID_DIFF_OK

        model = FakeModel(
            [model_response(VALID_DIFF_OK), model_response(VALID_DIFF_OK)]
        )
        spec = self._make_spec(issue_id="real-rd-qa-testfail", max_rounds=3)
        executor = RealRDExecutor(model, self.event_log, toolset_cls=FakeToolset)
        result = executor.run(spec)

        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["rounds"], 2)
        self.assertEqual(model.calls, 2)

    # ------------------------------------------------------------------ #
    # 用例 8（新增）：sandbox_mode 透传至三个 LocalRDToolset 实例
    # ------------------------------------------------------------------ #
    def test_sandbox_mode_passthrough(self) -> None:
        model = FakeModel([model_response(VALID_DIFF_OK)])
        executor = RealRDExecutor(
            model, self.event_log, toolset_cls=FakeToolset, sandbox_mode=SandboxMode.OFF
        )
        read_tools, write_tools, git_tools = executor._build_toolsets(
            "t",
            "p",
            "task",
            "real-rd:probe",
            [TARGET],
            "rd_verify",
            ["pytest", "tests/test_real_rd_verify.py"],
            [TARGET, "backend/tests/test_real_rd_verify.py"],
        )
        for tools in (read_tools, write_tools, git_tools):
            self.assertEqual(tools.sandbox_mode, SandboxMode.OFF)


if __name__ == "__main__":
    unittest.main()
