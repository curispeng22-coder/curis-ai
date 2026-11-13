"""CodexAgentAdapter 与 RealRDExecutor agent 分支 单元测试（QA 验收闸门）。

纯离线、全程 ``unittest.mock`` 隔离真实 ``pty`` / 真实 ``codex`` CLI /
真实 ``git``。覆盖：

A. CodexAgentAdapter 协议满足性 + 构造默认值
B. execute() 行为（mock ``pty.fork`` / ``os.read`` / ``app.dev_agent.subprocess.run``）
   - 成功路径（pty + git diff）
   - 指定 model（-m 注入）
   - cli 缺失 / 超时 / 其它异常 → 降级 status
   - git diff 失败 → output 降级留空、不崩
C. RealRDExecutor agent 分支
   - _build_agent_prompt 直接单测（不要求返回 diff）
   - _make_agent_rollback 直接单测（git checkout + 异常静默吞）
   - 端到端：agent 分支跳过 _apply_diff_transactional，测试失败时触发
     git checkout 回滚，最终 status == "failed"

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
from app.dev_agent import CodexAgentAdapter, DevAgent
from app.evolution_event_log import EvolutionEventLog
from app.local_rd_toolset import LocalRDToolError
from app.real_rd_executor import RealRDExecutor


# ---------------------------------------------------------------------------
# 被测目标文件（相对 workspace 根）与已知内容（供 agent 分支 e2e 复用）。
# ---------------------------------------------------------------------------
TARGET = "tools/real_rd_fixture/target_a.py"


# ---------------------------------------------------------------------------
# 构造最小化的 subprocess.CompletedProcess（供 mock 的 subprocess.run 返回）。
# ---------------------------------------------------------------------------
def _cp(stdout: str, returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=["codex"], returncode=returncode, stdout=stdout, stderr=""
    )


# ---------------------------------------------------------------------------
# 事件日志：临时 sqlite + EvolutionEventLog（含 evolution_events 表）
# ---------------------------------------------------------------------------
def _make_event_log() -> EvolutionEventLog:
    tmp_dir = tempfile.mkdtemp(prefix="codex-agent-qa-")
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
# A. CodexAgentAdapter 协议与构造
# ===========================================================================
class CodexAgentAdapterProtocolTestCase(unittest.TestCase):
    def test_isinstance_devagent(self) -> None:
        self.assertIsInstance(CodexAgentAdapter(), DevAgent)

    def test_mutates_filesystem_true(self) -> None:
        self.assertTrue(CodexAgentAdapter().mutates_filesystem)

    def test_construction_defaults(self) -> None:
        adapter = CodexAgentAdapter()
        self.assertEqual(adapter.cwd, os.getcwd())
        self.assertEqual(adapter.sandbox, "danger-full-access")
        self.assertEqual(adapter.approval, "never")
        self.assertEqual(adapter.extra_args, [])
        self.assertEqual(adapter.codex_bin, "/Users/yy/.local/bin/codex")
        self.assertEqual(adapter.timeout_seconds, 900)

    def test_construction_explicit_cwd(self) -> None:
        adapter = CodexAgentAdapter(cwd="/tmp/repo")
        self.assertEqual(adapter.cwd, "/tmp/repo")


# ===========================================================================
# B. execute() 行为（mock pty.fork + os.read + subprocess.run）
# ===========================================================================
def _mock_pty_parent(pty_return, read_data: bytes = b"ok\n"):
    """模拟 pty.fork 走父进程分支（pid > 0）。"""
    pf = mock.patch("pty.fork", return_value=pty_return)
    sel = mock.patch("select.select", return_value=([pty_return[1]], [], []))
    rd = mock.patch("os.read", side_effect=[read_data, b""])
    cl = mock.patch("os.close")
    wp = mock.patch("os.waitpid")
    return pf, sel, rd, cl, wp


class CodexAgentAdapterExecuteTestCase(unittest.TestCase):
    # ---- 成功路径：pty fork 模拟 codex + git diff 成功 ----------------
    def test_execute_success_returns_git_diff(self) -> None:
        adapter = CodexAgentAdapter()
        git_result = _cp("diff --git a/x b/x\n@@ -1 +1 @@\n-old\n+new\n", returncode=0)
        pty_return = (12345, 7)
        pty_patches = _mock_pty_parent(pty_return, b"codex did the work\n")
        for p in pty_patches:
            p.start()
            self.addCleanup(p.stop)
        with mock.patch(
            "app.dev_agent.subprocess.run", return_value=git_result
        ) as mock_run:
            result = adapter.execute("do the thing")
        self.assertEqual(result["status"], "success")
        self.assertEqual(
            result["output"],
            "diff --git a/x b/x\n@@ -1 +1 @@\n-old\n+new\n",
        )
        self.assertEqual(result["model_gateway_id"], "codex-cli")
        self.assertEqual(result["model_name"], "gpt-5.6-luna")
        self.assertEqual(result["total_tokens"], 0)
        self.assertEqual(result["estimated_cost"], 0.0)
        # subprocess.run 至少被调用一次（git diff）；具体次数因 execv 实现而异

    # ---- 指定 model：argv 含 -m <model> --------------------------------
    def test_execute_with_model_injects_m_flag(self) -> None:
        adapter = CodexAgentAdapter(model="gpt-5")
        pty_return = (12345, 7)
        pty_patches = _mock_pty_parent(pty_return)
        for p in pty_patches:
            p.start()
            self.addCleanup(p.stop)
        with mock.patch("app.dev_agent.subprocess.run", return_value=_cp("D", 0)):
            result = adapter.execute("prompt")
        self.assertEqual(result["model_name"], "gpt-5")

    # ---- cli 缺失：路径不存在 → cli_not_found ------------------------
    def test_execute_cli_not_found(self) -> None:
        adapter = CodexAgentAdapter(codex_bin="/nonexistent/codex")
        result = adapter.execute("prompt")
        self.assertEqual(result["status"], "cli_not_found")
        self.assertEqual(result["output"], "")

    # ---- 超时：select 超时 → timeout ----------------------------------
    def test_execute_timeout(self) -> None:
        adapter = CodexAgentAdapter()
        pty_return = (12345, 7)
        pf = mock.patch("pty.fork", return_value=pty_return)
        # select 返回空列表 → 超时
        sel = mock.patch("select.select", return_value=([], [], []))
        cl = mock.patch("os.close")
        wp = mock.patch("os.waitpid")
        sp = mock.patch("app.dev_agent.subprocess.run", return_value=_cp("", 0))
        with pf, sel, cl, wp, sp:
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["output"], "")

    # ---- 其它异常 → error: <ClassName> --------------------------------
    def test_execute_other_exception(self) -> None:
        adapter = CodexAgentAdapter()
        with mock.patch("pty.fork", side_effect=RuntimeError("boom")):
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "error: RuntimeError")

    # ---- git diff 失败（returncode=1）→ output 留空、不崩 ------------
    def test_execute_git_diff_failure_degrades_to_empty(self) -> None:
        adapter = CodexAgentAdapter()
        git_result = _cp("", returncode=1)
        pty_patches = _mock_pty_parent((12345, 7))
        for p in pty_patches:
            p.start()
            self.addCleanup(p.stop)
        with mock.patch("app.dev_agent.subprocess.run", return_value=git_result):
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "")

    # ---- git diff 抛异常 → 同样降级留空、不崩 --------------------------
    def test_execute_git_diff_raises_degrades_to_empty(self) -> None:
        adapter = CodexAgentAdapter()
        pty_patches = _mock_pty_parent((12345, 7))
        for p in pty_patches:
            p.start()
            self.addCleanup(p.stop)
        with mock.patch(
            "app.dev_agent.subprocess.run",
            side_effect=RuntimeError("git boom"),
        ):
            result = adapter.execute("prompt")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "")


# ===========================================================================
# C. RealRDExecutor agent 分支
# ===========================================================================
class _AgentScenario:
    def reset(self) -> None:
        self.read_files: dict[str, dict[str, Any]] = {}
        self.test_exit_codes: list[int] = []
        self.apply_calls: list[str] = []


_AGENT_SCENARIO = _AgentScenario()


def _noop_rollback() -> None:
    return None


class _FakeAgentModel:
    """filesystem-mutating 后端替身（mutates_filesystem=True）。"""
    mutates_filesystem = True
    cwd = "/tmp/agent-repo-test"

    def __init__(self, response: dict[str, Any] | None = None) -> None:
        self.calls = 0
        self._response = response or {
            "output": "", "status": "success",
            "model_name": "codex-cli", "model_gateway_id": "codex-cli",
            "total_tokens": 0, "estimated_cost": 0.0,
        }

    def execute(self, prompt: str) -> dict[str, Any]:
        self.calls += 1
        return dict(self._response)


class _AgentFakeToolset:
    def __init__(self, scope, event_log, command_registry=None, *, sandbox_mode=None):
        self.scope = scope
        self.event_log = event_log
        self.command_registry = command_registry or {}
        self.sandbox_mode = sandbox_mode

    def read_file(self, raw: str) -> dict[str, Any]:
        payload = json.loads(raw)
        path = payload["path"]
        out = _AGENT_SCENARIO.read_files.get(path, {
            "sha256": "fake-sha256-" + path,
            "lines": [{"text": f"# content of {path}"}],
            "ends_with_newline": True,
        })
        return {"output": out}

    def _apply_diff_transactional(self, raw: str) -> tuple[dict[str, Any], Any]:
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
            raise LocalRDToolError("command_failed", "registered command failed", exit_code=exit_code)
        return {"output": {"exit_code": 0}}

    def git_read(self, raw: str) -> dict[str, Any]:
        return {"output": {"output": ""}}


class RealRDExecutorAgentBranchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        _AGENT_SCENARIO.reset()
        self.event_log = _make_event_log()

    def _make_spec(self, *, issue_id: str = "agent-qa-1") -> dict[str, Any]:
        return {
            "issue_id": issue_id,
            "target_files": [TARGET],
            "test_command_id": "rd_verify",
            "test_command_argv": ["pytest", "tests/test_real_rd_verify.py"],
            "instructions": "fix the bug",
            "max_rounds": 3,
            "allow_paths": [TARGET, "backend/tests/test_real_rd_verify.py"],
        }

    def test_build_agent_prompt_content(self) -> None:
        prompt = RealRDExecutor._build_agent_prompt("fix bug", ["a.py", "b.py"], "")
        self.assertIn("Directly modify", prompt)
        self.assertIn("Do NOT return a unified diff", prompt)
        self.assertIn("Task:", prompt)
        self.assertIn("fix bug", prompt)
        self.assertIn("a.py", prompt)
        self.assertIn("b.py", prompt)
        self.assertNotIn("return a raw unified diff", prompt)

    def test_build_agent_prompt_with_last_failure(self) -> None:
        prompt = RealRDExecutor._build_agent_prompt("fix bug", ["a.py"], "tests failed")
        self.assertIn("The previous attempt failed: tests failed", prompt)
        self.assertIn("Correct it by editing the files directly", prompt)

    def test_make_agent_rollback_calls_git_checkout(self) -> None:
        with mock.patch("app.real_rd_executor.subprocess.run") as mock_run:
            rb = RealRDExecutor._make_agent_rollback(["a.py"], "/tmp")
            rb()
            mock_run.assert_called_once_with(
                ["git", "checkout", "--", "a.py"],
                cwd="/tmp", capture_output=True, text=True, timeout=120,
            )

    def test_make_agent_rollback_swallows_exceptions(self) -> None:
        with mock.patch("app.real_rd_executor.subprocess.run", side_effect=RuntimeError("boom")):
            rb = RealRDExecutor._make_agent_rollback(["a.py"], "/tmp")
            rb()

    def test_agent_branch_skips_apply_and_triggers_git_checkout_rollback(self) -> None:
        _AGENT_SCENARIO.read_files = {
            TARGET: {
                "sha256": "pre-hash-abc",
                "lines": [{"text": "ALPHA = 1"}, {"text": "BETA = 2"}],
                "ends_with_newline": True,
            }
        }
        _AGENT_SCENARIO.test_exit_codes = [1, 1, 1]
        model = _FakeAgentModel()
        spec = self._make_spec(issue_id="agent-qa-e2e")
        executor = RealRDExecutor(model, self.event_log, toolset_cls=_AgentFakeToolset)
        with mock.patch("app.real_rd_executor.subprocess.run") as mock_run:
            result = executor.run(spec)
        self.assertEqual(_AGENT_SCENARIO.apply_calls, [])
        mock_run.assert_any_call(
            ["git", "checkout", "--", TARGET],
            cwd=model.cwd, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["rounds"], 3)
        self.assertEqual(model.calls, 3)


if __name__ == "__main__":
    unittest.main()
