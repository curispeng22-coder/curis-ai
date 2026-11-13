"""DevAgent 协议一致性 + 无 key 优雅降级 单元测试（QA 验收闸门）。

设计目标：纯离线、不触真实网络 / 真实 API key，用 ``unittest.mock`` 隔离
所有外部依赖（Anthropic / OpenAI HTTP、codebuddy SDK、codebuddy CLI）。

覆盖用例：
1. 协议满足性（结构子类型，不要求继承 ``DevAgent``）
   - ClaudeCodeAdapter / OpenAICodexAdapter / WorkBuddyAdapter 均 ``isinstance(..., DevAgent)``
   - （可选）ModelGatewayAdapter 既有后端协议满足性
2. 无 key 优雅降级：三适配器构造 ``api_key=None`` + 清除环境变量，
   ``execute`` 返回 ``status == "no_api_key"`` 且 ``output == ""``
3. 返回结构完整性：无 key 返回 dict 含全部约定键
4. WorkBuddyAdapter 降级链：SDK 导入失败（ImportError）→ 降级 CLI；
   CLI 二进制缺失（FileNotFoundError）→ ``cli_not_found``；
   CLI 超时（TimeoutExpired）→ ``timeout``；CLI 成功 → ``success``

测试风格沿用 ``test_real_rd_executor.py``（unittest.TestCase）。backend 目录由
``tests/conftest.py`` 注入 sys.path，故可直接 ``from app.dev_agent import ...``。
"""

from __future__ import annotations

import os
import sys
import subprocess
import unittest
from unittest import mock

from app.dev_agent import (
    DevAgent,
    ClaudeCodeAdapter,
    OpenAICodexAdapter,
    WorkBuddyAdapter,
)


# ── 可选：既有后端 ModelGatewayAdapter（仅做协议满足性校验，不执行网络）─────
try:
    from app.model_gateway import ModelGatewayAdapter as _RealModelGatewayAdapter

    _HAVE_MODEL_GATEWAY = True
except Exception:  # pragma: no cover - 依赖复杂或缺失时跳过
    _RealModelGatewayAdapter = None
    _HAVE_MODEL_GATEWAY = False


# 无 key 场景必须清除/置空的环境变量（适配器默认从这些变量读取密钥）。
_NO_KEY_ENV = {
    "ANTHROPIC_API_KEY": "",
    "OPENAI_API_KEY": "",
    "OPENAI_BASE_URL": "",
    "CODEBUDDY_API_KEY": "",
}


def _fake_cli_result(stdout: str, returncode: int = 0) -> "subprocess.CompletedProcess":
    """构造一个最小化的 subprocess 返回对象，供 mock 的 subprocess.run 返回。"""
    fake = mock.Mock(spec=subprocess.CompletedProcess)
    fake.stdout = stdout
    fake.returncode = returncode
    return fake


class DevAgentProtocolTestCase(unittest.TestCase):
    """用例 1：协议满足性（结构子类型，无需继承 DevAgent）。"""

    def test_claude_code_adapter_satisfies_devagent(self) -> None:
        self.assertIsInstance(ClaudeCodeAdapter(), DevAgent)

    def test_openai_codex_adapter_satisfies_devagent(self) -> None:
        self.assertIsInstance(OpenAICodexAdapter(), DevAgent)

    def test_workbuddy_adapter_satisfies_devagent(self) -> None:
        self.assertIsInstance(WorkBuddyAdapter(), DevAgent)

    @unittest.skipUnless(_HAVE_MODEL_GATEWAY, "ModelGatewayAdapter 不可干净 import，跳过")
    def test_model_gateway_adapter_satisfies_devagent(self) -> None:
        self.assertIsInstance(_RealModelGatewayAdapter(), DevAgent)


class DevAgentNoKeyDegradeTestCase(unittest.TestCase):
    """用例 2 & 3：无 key 优雅降级 + 返回结构完整性。"""

    def _assert_no_key_response(self, result: dict) -> None:
        self.assertEqual(result["status"], "no_api_key")
        self.assertEqual(result["output"], "")
        for key in (
            "output",
            "total_tokens",
            "estimated_cost",
            "model_gateway_id",
            "model_name",
            "status",
        ):
            self.assertIn(key, result)

    def test_claude_code_no_key(self) -> None:
        with mock.patch.dict(os.environ, _NO_KEY_ENV, clear=False):
            adapter = ClaudeCodeAdapter(api_key=None)
            result = adapter.execute("any prompt")
        self._assert_no_key_response(result)
        self.assertEqual(result["model_gateway_id"], "anthropic")

    def test_openai_codex_no_key(self) -> None:
        with mock.patch.dict(os.environ, _NO_KEY_ENV, clear=False):
            adapter = OpenAICodexAdapter(api_key=None)
            result = adapter.execute("any prompt")
        self._assert_no_key_response(result)
        self.assertEqual(result["model_gateway_id"], "openai")

    def test_workbuddy_no_key(self) -> None:
        with mock.patch.dict(os.environ, _NO_KEY_ENV, clear=False):
            adapter = WorkBuddyAdapter(api_key=None)
            result = adapter.execute("any prompt")
        self._assert_no_key_response(result)
        self.assertEqual(result["model_gateway_id"], "workbuddy")


class WorkBuddyAdapterDegradationChainTestCase(unittest.TestCase):
    """用例 4：WorkBuddyAdapter 降级链 SDK → CLI 及各失败分支。

    无论运行环境是否实际安装 ``codebuddy_agent_sdk``，均通过
    ``sys.modules['codebuddy_agent_sdk'] = None`` 强制 ``_execute_via_sdk``
    抛出 ImportError，从而稳定触发「降级到 CLI」分支。
    """

    def _run_with_sdk_import_error(self, subprocess_side_effect):
        """构造带 key 的适配器，强制 SDK 导入失败，并以给定方式 mock subprocess.run。"""
        with mock.patch.dict(os.environ, _NO_KEY_ENV, clear=False):
            adapter = WorkBuddyAdapter(api_key="wb-test-key")
            with mock.patch.dict(sys.modules, {"codebuddy_agent_sdk": None}):
                with mock.patch("subprocess.run", side_effect=subprocess_side_effect):
                    return adapter.execute("any prompt")

    def test_sdk_import_error_then_cli_not_found(self) -> None:
        result = self._run_with_sdk_import_error(
            FileNotFoundError("codebuddy binary not found")
        )
        self.assertEqual(result["status"], "cli_not_found")
        self.assertEqual(result["output"], "")

    def test_sdk_import_error_then_cli_timeout(self) -> None:
        result = self._run_with_sdk_import_error(
            subprocess.TimeoutExpired(cmd=["codebuddy", "run"], timeout=600)
        )
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["output"], "")

    def test_sdk_import_error_then_cli_success(self) -> None:
        fake = _fake_cli_result(
            stdout="--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-old\n+new\n",
            returncode=0,
        )
        with mock.patch.dict(os.environ, _NO_KEY_ENV, clear=False):
            adapter = WorkBuddyAdapter(api_key="wb-test-key")
            with mock.patch.dict(sys.modules, {"codebuddy_agent_sdk": None}):
                with mock.patch("subprocess.run", return_value=fake):
                    result = adapter.execute("any prompt")
        self.assertEqual(result["status"], "success")
        self.assertIn("+new", result["output"])


if __name__ == "__main__":
    unittest.main()
