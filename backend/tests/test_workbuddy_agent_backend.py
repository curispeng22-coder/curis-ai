"""WorkBuddyAgentAdapter 与 RealRDExecutor agent 分支 单元测试（QA 验收闸门）。

真·WorkBuddy agentic 后端：封装 codebuddy CLI，在 cwd 内直接读/改/跑文件
（filesystem-mutating），复用与 Codex 后端相同的 RealRDExecutor agent 分支
（跳过 diff parse/apply，失败时改用 git checkout 回滚）。

纯离线、全程 ``unittest.mock`` 隔离真实 ``subprocess`` / 真实 ``codebuddy`` CLI /
真实 ``git``。覆盖：

A. WorkBuddyAgentAdapter 协议满足性 + 构造默认值
B. execute() 行为（mock ``app.dev_agent.subprocess.run``）
   - 成功路径（含两次 subprocess.run：codebuddy + git diff）
   - 指定 permission_mode（--permission-mode 注入 acceptEdits，证明参数透传）
   - 无 key 降级 / cli 缺失 / 超时 / 其它异常 → 降级 status
   - git diff 失败 → output 降级留空、不崩
C. RealRDExecutor agent 分支（最关键）
   - _build_agent_prompt 直接单测（不要求返回 diff）
   - _make_agent_rollback 直接单测（git checkout + 异常静默吞）
   - 端到端（FakeAgentModel 替身）：agent 分支跳过 _apply_diff_transactional，
     测试失败时触发 git checkout 回滚，耗尽 max_rounds → status == "failed"
   - 端到端（真·WorkBuddyAgentAdapter 驱动）：证明后端直接接入同一 agent 分支

风格沿用 test_codex_agent_backend.py（unittest.TestCase + unittest.mock，纯离线）。
backend 目录由 tests/conftest.py 注入 sys.path，可直接 ``from app.dev_agent import ...``。
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from typing import Any

from unittest import mock

from app.database import Database
from app.dev_agent import DevAgent, WorkBuddyAgentAdapter
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import LocalRDToolError
from app.real_rd_executor import RealRDExecutor


# ---------------------------------------------------------------------------
# 被测目标文件（相对 workspace 根）与已知内容（供 agent 分支 e2e 复用）。
# ---------------------------------------------------------------------------
TARGET = "tools/real_rd_fixture/target_a.py"

# 用于那些必须真正触发 subprocess.run 的用例——显式注入 key，避免依赖运行环境里
# 是否设置了 ``CODEBUDDY_API_KEY``。无 key 降级用例则显式传入 api_key=""。
FAKE_KEY = "wb-qa-fake-key"

# 默认 codebuddy 二进制路径（仅用于命令断言的可读性，不参与真实调用）。
DEFAULT_BIN = (
    "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/bin/codebuddy"
)


# ---------------------------------------------------------------------------
# 构造最小化的 subprocess.CompletedProcess（供 mock 的 subprocess.run 返回）。
# ---------------------------------------------------------------------------
def _cp(stdout: str, returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=[DEFAULT_BIN], returncode=returncode, stdout=stdout, stderr=""
    )


# ---------------------------------------------------------------------------
# 事件日志：临时 sqlite + EvolutionEventLog（含 evolution_events 表），
# 使 _claim_once 单主占锁与 _record_run_summary 汇总被真实执行。
# ---------------------------------------------------------------------------
def _make_event_log() -> EvolutionEventLog:
    tmp_dir = tempfile.mkdtemp(prefix="wb-agent-qa-")
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


# ===========================================================================
# A. WorkBuddyAgentAdapter 协议与构造
# ===========================================================================
class WorkBuddyAgentAdapterProtocolTestCase(unittest.TestCase):
    def test_isinstance_devagent(self) -> None:
        # 结构子类型：WorkBuddyAgentAdapter 提供 execute()，满足 DevAgent 协议。
        self.assertIsInstance(WorkBuddyAgentAdapter(), DevAgent)

    def test_mutates_filesystem_true(self) -> None:
        self.assertTrue(WorkBuddyAgentAdapter().mutates_filesystem)

    def test_construction_defaults(self) -> None:
        adapter = WorkBuddyAgentAdapter()
        # cwd 默认 None → 实例 cwd 等于 os.getcwd()
        self.assertEqual(adapter.cwd, os.getcwd())
        self.assertEqual(adapter.permission_mode, "bypassPermissions")
        self.assertEqual(adapter.extra_args, [])
        # 其余默认值
        self.assertEqual(adapter.codebuddy_bin, DEFAULT_BIN)
        self.assertEqual(adapter.timeout_seconds, 900)

    def test_construction_explicit_permission_mode(self) -> None:
        # 指定 permission_mode，后续 execute 用例断言命令含该值（证明参数透传）。
        adapter = WorkBuddyAgentAdapter(permission_mode="acceptEdits")
        self.assertEqual(adapter.permission_mode, "acceptEdits")


# ===========================================================================
# B. execute() 行为（mock app.dev_agent.subprocess.run）
# ===========================================================================
class WorkBuddyAgentAdapterExecuteTestCase(unittest.TestCase):
    # ---- 1. 成功路径：codebuddy 调用成功 + git diff 成功 ------------------
    def test_execute_success_returns_git_diff(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        codebuddy_result = _cp("", returncode=0)
        git_result = _cp(
            "diff --git a/x b/x\n@@ -1 +1 @@\n-old\n+new\n", returncode=0
        )
        with mock.patch(
            "app.dev_agent.subprocess.run", side_effect=[codebuddy_result, git_result]
        ) as mock_run:
            result = adapter.execute("do the thing")
        # 返回结构
        self.assertEqual(result["status"], "success")
        self.assertEqual(
            result["output"], "diff --git a/x b/x\n@@ -1 +1 @@\n-old\n+new\n"
        )
        self.assertEqual(result["model_gateway_id"], "workbuddy")
        self.assertEqual(result["model_name"], "codebuddy-cli")
        self.assertEqual(result["total_tokens"], 0)
        self.assertEqual(result["estimated_cost"], 0.0)
        # 两次 subprocess.run 都被调用（codebuddy + git diff）
        self.assertEqual(mock_run.call_count, 2)
        first_cmd = mock_run.call_args_list[0].args[0]
        self.assertIn("-p", first_cmd)
        self.assertIn("--permission-mode", first_cmd)
        self.assertIn("bypassPermissions", first_cmd)
        self.assertEqual(first_cmd[-1], "do the thing")  # 以 prompt 结尾

    # ---- 2. 指定 permission_mode：argv 含 acceptEdits 而非 bypassPermissions -
    def test_execute_with_permission_mode_injects_flag(self) -> None:
        adapter = WorkBuddyAgentAdapter(permission_mode="acceptEdits", api_key=FAKE_KEY)
        codebuddy_result = _cp("", returncode=0)
        git_result = _cp("D", returncode=0)
        with mock.patch(
            "app.dev_agent.subprocess.run", side_effect=[codebuddy_result, git_result]
        ) as mock_run:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "success")
        first_cmd = mock_run.call_args_list[0].args[0]
        self.assertIn("acceptEdits", first_cmd)
        self.assertNotIn("bypassPermissions", first_cmd)
        self.assertEqual(first_cmd[-1], "prompt")

    # ---- 3. 无 key 降级：直接返回 no_api_key，且绝不调用 subprocess.run ----
    def test_execute_no_api_key_skips_subprocess(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key="")  # 强制空 key，绕过 env
        with mock.patch("app.dev_agent.subprocess.run") as mock_run:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "no_api_key")
        self.assertEqual(result["output"], "")
        self.assertEqual(result["model_gateway_id"], "workbuddy")
        self.assertEqual(result["model_name"], "codebuddy-cli")
        # 无 key 直接降级，subprocess.run 永不被调用
        mock_run.assert_not_called()

    # ---- 4. cli 缺失：FileNotFoundError → cli_not_found -------------------
    def test_execute_cli_not_found(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        with mock.patch(
            "app.dev_agent.subprocess.run",
            side_effect=FileNotFoundError("codebuddy binary missing"),
        ) as mock_run:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "cli_not_found")
        self.assertEqual(result["output"], "")
        self.assertEqual(result["model_gateway_id"], "workbuddy")
        # 第一次 codebuddy 调用即抛错，git diff 永不被调用
        self.assertEqual(mock_run.call_count, 1)

    # ---- 5. 超时：TimeoutExpired → timeout --------------------------------
    def test_execute_timeout(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        with mock.patch(
            "app.dev_agent.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=[DEFAULT_BIN], timeout=900),
        ):
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["output"], "")

    # ---- 6. 其它异常 → error: <ClassName> --------------------------------
    def test_execute_other_exception(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        with mock.patch(
            "app.dev_agent.subprocess.run",
            side_effect=RuntimeError("boom"),
        ):
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "error: RuntimeError")
        self.assertEqual(result["output"], "")

    # ---- 7. git diff 失败（returncode=1）→ output 留空、不崩 -------------
    def test_execute_git_diff_failure_degrades_to_empty(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        codebuddy_result = _cp("", returncode=0)
        git_result = _cp("", returncode=1)  # git diff 非零退出
        with mock.patch(
            "app.dev_agent.subprocess.run", side_effect=[codebuddy_result, git_result]
        ) as mock_run:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "")
        self.assertEqual(mock_run.call_count, 2)

    # ---- 7b. git diff 抛异常 → 同样降级留空、不崩 -------------------------
    def test_execute_git_diff_raises_degrades_to_empty(self) -> None:
        adapter = WorkBuddyAgentAdapter(api_key=FAKE_KEY)
        codebuddy_result = _cp("", returncode=0)
        with mock.patch(
            "app.dev_agent.subprocess.run",
            side_effect=[codebuddy_result, RuntimeError("git boom")],
        ) as mock_run:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "")
        self.assertEqual(mock_run.call_count, 2)


# ===========================================================================
# C. RealRDExecutor agent 分支
# ===========================================================================
class _AgentScenario:
    """agent 分支 e2e 单次 run 共享脚本状态。"""

    def reset(self) -> None:
        self.read_files: dict[str, dict[str, Any]] = {}
        self.test_exit_codes: list[int] = []
        self.apply_calls: list[str] = []


_AGENT_SCENARIO = _AgentScenario()


def _noop_rollback() -> None:
    return None


class _FakeWorkBuddyModel:
    """filesystem-mutating 后端替身（WorkBuddy 形状响应，mutates_filesystem=True）。

    不依赖真实 codebuddy：execute 直接返回 agent 形状的统一响应，用于证明
    RealRDExecutor 的 agent 分支（跳过 diff apply + git checkout 回滚）对
    filesystem-mutating 后端通用。
    """

    mutates_filesystem = True
    cwd = "/tmp/agent-repo-test"

    def __init__(self, response: dict[str, Any] | None = None) -> None:
        self.calls = 0
        self._response = response or {
            "output": "",
            "status": "success",
            "model_name": "codebuddy-cli",
            "model_gateway_id": "workbuddy",
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }

    def execute(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        return dict(self._response)


class _AgentFakeToolset:
    """RealRDExecutor agent 分支专用 FakeToolset（不继承真实 LocalRDToolset，
    绝不触发 sandbox-exec / 真实文件 I/O）。"""

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
        payload = json.loads(raw)
        path = payload["path"]
        out = _AGENT_SCENARIO.read_files.get(
            path,
            {
                "sha256": "fake-sha256-" + path,
                "lines": [{"text": f"# content of {path}"}],
                "ends_with_newline": True,
            },
        )
        return {"output": out}

    def _apply_diff_transactional(self, raw: str) -> tuple[dict[str, Any], Any]:
        # agent 分支绝不应调用此方法；记录以便断言未触发。
        _AGENT_SCENARIO.apply_calls.append(raw)
        return ({"output": {"files": []}}, _noop_rollback)

    def run_test(self, raw: str) -> dict[str, Any]:
        payload = json.loads(raw)
        command_id = payload["command_id"]
        if command_id not in self.command_registry:
            raise LocalRDToolError("command_not_registered", "command not registered")
        codes = _AGENT_SCENARIO.test_exit_codes
        exit_code = codes.pop(0) if codes else 0
        if exit_code != 0:
            raise LocalRDToolError(
                "command_failed", "registered command failed", exit_code=exit_code
            )
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict[str, Any]:
        return {"output": {"output": ""}}


class RealRDExecutorWorkBuddyAgentBranchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _AGENT_SCENARIO.reset()
        self.event_log = _make_event_log()

    def _make_spec(self, *, issue_id: str = "wb-agent-qa-1") -> dict[str, Any]:
        return {
            "issue_id": issue_id,
            "target_files": [TARGET],
            "test_command_id": "rd_verify",
            "test_command_argv": ["pytest", "tests/test_real_rd_verify.py"],
            "instructions": "fix the bug",
            "max_rounds": 3,
            "allow_paths": [TARGET, "backend/tests/test_real_rd_verify.py"],
        }

    # ---- 8. _build_agent_prompt 直接单测 -------------------------------
    def test_build_agent_prompt_content(self) -> None:
        prompt = RealRDExecutor._build_agent_prompt("fix bug", ["a.py", "b.py"], "")
        self.assertIn("Directly modify", prompt)
        self.assertIn("Do NOT return a unified diff", prompt)
        self.assertIn("Task:", prompt)
        self.assertIn("fix bug", prompt)
        self.assertIn("a.py", prompt)
        self.assertIn("b.py", prompt)
        # 与 _build_prompt（要求返回 raw unified diff）措辞严格区分
        self.assertNotIn("return a raw unified diff", prompt)

    def test_build_agent_prompt_with_last_failure(self) -> None:
        prompt = RealRDExecutor._build_agent_prompt("fix bug", ["a.py"], "tests failed")
        self.assertIn("The previous attempt failed: tests failed", prompt)
        self.assertIn("Correct it by editing the files directly", prompt)

    # ---- 9. _make_agent_rollback 直接单测 ------------------------------
    def test_make_agent_rollback_calls_git_checkout(self) -> None:
        with mock.patch("app.real_rd_executor.subprocess.run") as mock_run:
            rb = RealRDExecutor._make_agent_rollback(["a.py"], "/tmp")
            rb()
            mock_run.assert_called_once_with(
                ["git", "checkout", "--", "a.py"],
                cwd="/tmp",
                capture_output=True,
                text=True,
                timeout=120,
            )

    def test_make_agent_rollback_swallows_exceptions(self) -> None:
        with mock.patch(
            "app.real_rd_executor.subprocess.run",
            side_effect=RuntimeError("boom"),
        ):
            rb = RealRDExecutor._make_agent_rollback(["a.py"], "/tmp")
            rb()  # 异常必须被静默吞掉，不向外溢出

    # ---- 10. 端到端（FakeAgentModel）：agent 分支跳过 apply + 测试失败
    #          触发 git checkout 回滚 ------------------------------------
    def test_agent_branch_skips_apply_and_triggers_git_checkout_rollback(self) -> None:
        _AGENT_SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        # 每轮测试都失败 → 触发回滚，耗尽 max_rounds → status == "failed"
        _AGENT_SCENARIO.test_exit_codes = [1, 1, 1]

        model = _FakeWorkBuddyModel()
        spec = self._make_spec(issue_id="wb-agent-qa-e2e")
        executor = RealRDExecutor(model, self.event_log, toolset_cls=_AgentFakeToolset)

        with mock.patch("app.real_rd_executor.subprocess.run") as mock_run:
            result = executor.run(spec)

        # 最强证明（1）：agent 模式跳过 diff parse/apply
        self.assertEqual(_AGENT_SCENARIO.apply_calls, [])
        # 最强证明（2）：测试失败时回滚被触发，底层 git checkout 被调用
        mock_run.assert_any_call(
            ["git", "checkout", "--", TARGET],
            cwd=model.cwd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        # 最强证明（3）：测试一直失败、达到 max_rounds → failed
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["rounds"], 3)
        self.assertEqual(model.calls, 3)

    # ---- 11. 端到端（真·WorkBuddyAgentAdapter 驱动）：最强证明后端接入
    #          同一 agent 分支，且 _apply_diff_transactional 被跳过 ----------
    def test_e2e_with_real_workbuddy_adapter(self) -> None:
        _AGENT_SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        # 每轮测试都失败 → 触发 git checkout 回滚，耗尽 max_rounds → failed
        _AGENT_SCENARIO.test_exit_codes = [1, 1, 1]

        model = WorkBuddyAgentAdapter(api_key=FAKE_KEY, cwd="/tmp/agent-repo-test")
        spec = self._make_spec(issue_id="wb-real-e2e")
        executor = RealRDExecutor(model, self.event_log, toolset_cls=_AgentFakeToolset)

        # 注意：app.dev_agent.subprocess 与 app.real_rd_executor.subprocess 解析到
        # 同一个真实的 subprocess 模块对象，因此两次 mock.patch 会冲突（后者覆盖前者）。
        # 故仅做一次 patch，用 router 按命令类型分流，并严格计数以自我校验拦截是否生效：
        #   - codebuddy 调用（每轮 1 次，共 3）
        #   - adapter 内部 git diff（每轮 1 次，共 3）
        #   - 测试失败触发的 git checkout 回滚（每轮 1 次，共 3）
        calls = {"codebuddy": 0, "git_diff": 0, "checkout": 0}

        def _router(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess:
            cmd = list(args[0]) if args else []
            if cmd and cmd[0] == DEFAULT_BIN:
                calls["codebuddy"] += 1
                return _cp("", returncode=0)  # codebuddy CLI 调用成功
            if len(cmd) >= 2 and cmd[0] == "git" and cmd[1] == "-C" and cmd[-1] == "diff":
                calls["git_diff"] += 1
                return _cp("diff text", returncode=0)  # adapter 内部 git diff
            if len(cmd) >= 2 and cmd[0] == "git" and cmd[1] == "checkout":
                calls["checkout"] += 1
                return _cp("", returncode=0)  # 回滚
            return _cp("", returncode=0)

        with mock.patch("app.dev_agent.subprocess.run", side_effect=_router) as mock_run:
            result = executor.run(spec)

        # agent 模式跳过 diff parse/apply（由 FakeToolset 记录）
        self.assertEqual(_AGENT_SCENARIO.apply_calls, [])
        # 计数严格自校验：若两次 patch 冲突或拦截未生效，这些断言会暴露。
        self.assertEqual(calls["codebuddy"], 3)  # 每轮 executor 真正驱动 adapter.execute
        self.assertEqual(calls["git_diff"], 3)  # 每轮 adapter 内部取真实 git diff
        self.assertEqual(calls["checkout"], 3)  # 每轮测试失败触发一次 git checkout 回滚
        self.assertEqual(mock_run.call_count, 9)
        # 回滚命令确实以正确参数下发
        self.assertTrue(
            any(
                ca.args[0][:2] == ["git", "checkout"]
                and TARGET in ca.args[0]
                and ca.kwargs.get("cwd") == "/tmp/agent-repo-test"
                for ca in mock_run.call_args_list
            )
        )
        # 真·后端响应形状透传到最终汇总
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["rounds"], 3)
        self.assertEqual(result["model_gateway_id"], "workbuddy")
        self.assertEqual(result["model_name"], "codebuddy-cli")


if __name__ == "__main__":
    unittest.main()
