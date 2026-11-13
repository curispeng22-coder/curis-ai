"""统一开发后端接口（DevAgent 协议）。

DevAgent 协议定义了一个开发后端的最小接口：接收 prompt，返回
{output, total_tokens, estimated_cost, ...}。所有后端实现此协议即可
作为 RealRDExecutor 的 model 参数。

当前实现：
- ModelGatewayAdapter（已有，直接匹配协议）
- ClaudeCodeAdapter（Anthropic API）
"""

from __future__ import annotations

import os
import select
import subprocess
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DevAgent(Protocol):
    """统一开发后端接口。

    实现者只需提供 execute(prompt) 方法，返回含 output（unified diff 文本）
    的字典。RealRDExecutor 通过此协议调用任意后端，不感知具体实现。
    """

    def execute(self, prompt: str) -> dict[str, Any]:
        """执行 prompt，返回开发后端输出。

        Args:
            prompt: 完整 prompt（含任务指令 + 文件内容 + 错误上下文）

        Returns:
            字典必须含 ``output``（str，unified diff 文本）。
            可选字段：total_tokens, estimated_cost, model_gateway_id, model_name, status。
            当后端无法输出 unified diff 时，``output`` 可返回空字符串，由调用方处理。
        """
        ...


class ClaudeCodeAdapter:
    """通过 Anthropic API 调用 Claude Code 的适配器。

    用法：
        adapter = ClaudeCodeAdapter(api_key="sk-...", model="claude-sonnet-4-20250514")
        executor = RealRDExecutor(model=adapter, ...)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 8192,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.model = model
        self.max_tokens = max_tokens
        self.base_url = base_url or "https://api.anthropic.com/v1"

    def execute(self, prompt: str) -> dict[str, Any]:
        """通过 Anthropic Messages API 调用 Claude，返回统一格式。"""
        if not self.api_key:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "anthropic",
                "status": "no_api_key",
            }
        import httpx

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            resp = httpx.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=body,
                timeout=300,
            )
            resp.raise_for_status()
            data = resp.json()
            text = "".join(
                block["text"]
                for block in data.get("content", [])
                if block.get("type") == "text"
            )
            usage = data.get("usage", {})
            return {
                "output": text,
                "total_tokens": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "anthropic",
                "status": "success",
            }
        except Exception as error:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "anthropic",
                "status": f"error: {type(error).__name__}",
            }


class OpenAICodexAdapter:
    """通过 OpenAI Chat Completions API 调用 Codex / GPT 的适配器。

    兼容任意 OpenAI 格式的 API（Azure / 本地网关 / 第三方代理）。

    用法：
        adapter = OpenAICodexAdapter(api_key="sk-...", model="gpt-4o")
        executor = RealRDExecutor(model=adapter, ...)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o",
        max_tokens: int = 8192,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.max_tokens = max_tokens
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL", "")).rstrip("/") or "https://api.openai.com/v1"

    def execute(self, prompt: str) -> dict[str, Any]:
        """通过 OpenAI Chat Completions API 调用模型，返回统一格式。"""
        if not self.api_key:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "openai",
                "status": "no_api_key",
            }
        import httpx

        headers = {
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }
        body = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            resp = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=body,
                timeout=300,
            )
            resp.raise_for_status()
            data = resp.json()
            choice = data.get("choices", [{}])[0]
            text = (choice.get("message") or {}).get("content", "")
            usage = data.get("usage", {})
            return {
                "output": text or "",
                "total_tokens": usage.get("total_tokens", 0),
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "openai",
                "status": "success",
            }
        except Exception as error:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_name": self.model,
                "model_gateway_id": "openai",
                "status": f"error: {type(error).__name__}",
            }


class WorkBuddyAdapter:
    """通过 WorkBuddy / CodeBuddy Agent 执行开发任务的适配器。

    两种模式：
    1. API 模式（默认）：通过 CODEBUDDY_API_KEY 调用 Agent SDK
    2. CLI 模式：通过 codebuddy CLI 执行

    用法：
        adapter = WorkBuddyAdapter(api_key="wb-...")
        executor = RealRDExecutor(model=adapter, ...)
    """

    def __init__(
        self,
        api_key: str | None = None,
        agent_type: str = "general-purpose",
        timeout_seconds: int = 600,
    ) -> None:
        self.api_key = api_key or os.getenv("CODEBUDDY_API_KEY", "")
        self.agent_type = agent_type
        self.timeout_seconds = timeout_seconds

    def execute(self, prompt: str) -> dict[str, Any]:
        """通过 CodeBuddy Agent SDK 或 CLI 执行 prompt。

        优先使用 SDK（codebuddy-agent-sdk），不可用时尝试 CLI。
        """
        if not self.api_key:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": self.agent_type,
                "status": "no_api_key",
            }
        # 尝试 SDK 模式
        try:
            return self._execute_via_sdk(prompt)
        except ImportError:
            pass
        # 降级 CLI 模式
        try:
            return self._execute_via_cli(prompt)
        except Exception as error:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": self.agent_type,
                "status": f"error: {type(error).__name__}",
            }

    def _execute_via_sdk(self, prompt: str) -> dict[str, Any]:
        """通过 codebuddy-agent-sdk Python 包调用 WorkBuddy。"""
        from codebuddy_agent_sdk import AgentClient

        client = AgentClient(api_key=self.api_key)
        result = client.run(
            agent_type=self.agent_type,
            prompt=prompt,
            timeout=self.timeout_seconds,
        )
        return {
            "output": result.get("output", ""),
            "total_tokens": result.get("total_tokens", 0),
            "estimated_cost": result.get("estimated_cost", 0.0),
            "model_gateway_id": "workbuddy",
            "model_name": self.agent_type,
            "status": result.get("status", "success"),
        }

    def _execute_via_cli(self, prompt: str) -> dict[str, Any]:
        """降级路径：通过 codebuddy CLI 执行。"""
        import subprocess
        import tempfile
        import json

        # 写入临时 prompt 文件
        prompt_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        )
        prompt_file.write(prompt)
        prompt_path = prompt_file.name
        prompt_file.close()
        try:
            result = subprocess.run(
                ["codebuddy", "run", "--agent", self.agent_type, "--prompt-file", prompt_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            output = result.stdout
            return {
                "output": output,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": self.agent_type,
                "status": "success" if result.returncode == 0 else f"cli_exit_{result.returncode}",
            }
        except FileNotFoundError:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": self.agent_type,
                "status": "cli_not_found",
            }
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": self.agent_type,
                "status": "timeout",
            }
        finally:
            import os as _os

            try:
                _os.unlink(prompt_path)
            except Exception:
                pass


class CodexAgentAdapter:
    """通过 ChatGPT 桌面端自带的 Codex agent CLI 执行开发任务的适配器。

    与协议内其余「输出 unified diff、由执行器 apply」的后端不同，本适配器
    指示 Codex agent 在 workspace 内**直接修改磁盘文件**（filesystem-mutating）。
    因此设置 ``mutates_filesystem = True``，供 ``RealRDExecutor`` 识别并跳过
    diff parse/apply，失败时改用 ``git checkout`` 回滚。

    环境要求：``codex`` CLI 已安装并登录（ChatGPT 桌面端自带，订阅额度可直接
    使用，无需 ``sk-`` key）。

    用法：
        adapter = CodexAgentAdapter(cwd="/path/to/repo")
        executor = RealRDExecutor(model=adapter, ...)
    """

    def __init__(
        self,
        codex_bin: str = "/Users/yy/.local/bin/codex",
        cwd: str | None = None,
        model: str | None = None,
        sandbox: str = "danger-full-access",
        approval: str = "never",
        timeout_seconds: int = 900,
        extra_args: list[str] | None = None,
    ) -> None:
        self.codex_bin = codex_bin
        self.cwd = cwd or os.getcwd()
        self.model = model
        self.sandbox = sandbox
        self.approval = approval
        self.timeout_seconds = timeout_seconds
        self.extra_args = list(extra_args) if extra_args else []
        # 关键标志：RealRDExecutor 据此识别 filesystem-mutating 后端，
        # 跳过 diff parse/apply，并在失败时改用 git checkout 回滚。
        self.mutates_filesystem = True

    def execute(self, prompt: str) -> dict[str, Any]:
        """运行 Codex agent，让其直接在 workspace 内修改文件，返回真实 git diff。

        使用 pty 伪终端以绕过 codex 交互模式对 TTY 的要求。
        Args:
            prompt: 完整 prompt（含任务指令 + 目标文件 + 错误上下文），
                由 ``RealRDExecutor._build_agent_prompt`` 生成，**不**要求返回 diff。

        Returns:
            字典含 ``output``（``cwd`` 内的真实 ``git diff`` 文本）以及
            ``total_tokens`` / ``estimated_cost`` / ``model_gateway_id`` /
            ``model_name`` / ``status``。
            status 可为 ``success`` / ``cli_not_found`` / ``timeout`` / ``error: ...``。
        """
        if not self.codex_bin or not os.path.exists(self.codex_bin):
            return {
                "output": "",
                "total_tokens": 0, "estimated_cost": 0.0,
                "model_gateway_id": "codex-cli",
                "model_name": self.model or "gpt-5.6-luna",
                "status": "cli_not_found",
            }
        cmdv = [self.codex_bin]
        if self.model:
            cmdv += ["-m", self.model]
        cmdv += ["-s", self.sandbox, "-a", self.approval]
        cmdv += self.extra_args
        cmdv.append(prompt)

        import pty
        try:
            pid, fd = pty.fork()
            if pid == 0:
                os.chdir(self.cwd)
                os.execv(self.codex_bin, cmdv)
                os._exit(1)
            output = b""
            timed_out = False
            try:
                while True:
                    r, _, _ = select.select([fd], [], [], self.timeout_seconds)
                    if not r:
                        timed_out = True
                        break
                    data = os.read(fd, 65536)
                    if not data:
                        break
                    output += data
            finally:
                os.close(fd)
                os.waitpid(pid, 0)
            if timed_out:
                return {
                    "output": "", "total_tokens": 0, "estimated_cost": 0.0,
                    "model_gateway_id": "codex-cli",
                    "model_name": self.model or "gpt-5.6-luna",
                    "status": "timeout",
                }
        except FileNotFoundError:
            return {
                "output": "", "total_tokens": 0, "estimated_cost": 0.0,
                "model_gateway_id": "codex-cli",
                "model_name": self.model or "gpt-5.6-luna",
                "status": "cli_not_found",
            }
        except Exception as error:
            return {
                "output": "", "total_tokens": 0, "estimated_cost": 0.0,
                "model_gateway_id": "codex-cli",
                "model_name": self.model or "gpt-5.6-luna",
                "status": f"error: {type(error).__name__}",
            }

        # agent 已在磁盘直接改文件，取真实 git diff 作为 output（供审计/记录）。
        output = ""
        try:
            import subprocess as _sp
            git_result = _sp.run(
                ["git", "-C", self.cwd, "diff"],
                capture_output=True, text=True, timeout=60,
            )
            if git_result.returncode == 0:
                output = git_result.stdout
        except Exception:
            pass
        # agent 已在磁盘直接改文件，取真实 git diff 作为 output。
        output = ""
        try:
            import subprocess as _sp
            git_result = _sp.run(
                ["git", "-C", self.cwd, "diff"],
                capture_output=True, text=True, timeout=60,
            )
            if git_result.returncode == 0:
                output = git_result.stdout
        except Exception:
            output = ""

        return {
            "output": output,
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "model_gateway_id": "codex-cli",
            "model_name": self.model or "gpt-5.6-luna",
            "status": "success",
        }


class WorkBuddyAgentAdapter:
    """通过 WorkBuddy 桌面端 codebuddy CLI（CodeBuddy Code，agentic 编码 CLI）执行的真·agentic 适配器。

    与协议内其余「输出 unified diff、由执行器 apply」的后端不同，本适配器指示
    codebuddy agent 在 cwd 内**直接读/改/跑文件**（filesystem-mutating，真 agentic，
    不是“返回文本”的编译器）。因此设置 ``mutates_filesystem = True``，供
    ``RealRDExecutor`` 识别并跳过 diff parse/apply，失败时改用 ``git checkout`` 回滚。

    认证差异（与 Codex 不同）：codebuddy CLI 没有 login 子命令，无法持久化 auth.json
    免 key；必须依赖 ``CODEBUDDY_API_KEY`` 环境变量。适配器默认读取该变量，无则优雅降级
    ``no_api_key``。

    用法：
        adapter = WorkBuddyAgentAdapter(cwd="/path/to/repo")
        executor = RealRDExecutor(model=adapter, ...)
    """

    def __init__(
        self,
        codebuddy_bin: str = "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/bin/codebuddy",
        cwd: str | None = None,
        permission_mode: str = "bypassPermissions",
        api_key: str | None = None,
        timeout_seconds: int = 900,
        extra_args: list[str] | None = None,
    ) -> None:
        self.codebuddy_bin = codebuddy_bin
        self.cwd = cwd or os.getcwd()
        self.permission_mode = permission_mode
        self.api_key = api_key or os.getenv("CODEBUDDY_API_KEY", "")
        self.timeout_seconds = timeout_seconds
        self.extra_args = list(extra_args) if extra_args else []
        # 关键标志：RealRDExecutor 据此识别 filesystem-mutating 后端，
        # 跳过 diff parse/apply，并在失败时改用 git checkout 回滚。
        self.mutates_filesystem = True

    def execute(self, prompt: str) -> dict[str, Any]:
        """运行 codebuddy agent，让其在 cwd 内直接修改文件，返回真实 git diff。

        Args:
            prompt: 完整 prompt（含任务指令 + 目标文件 + 错误上下文），
                由 ``RealRDExecutor._build_agent_prompt`` 生成，**不**要求返回 diff。

        Returns:
            字典含 ``output``（``cwd`` 内的真实 ``git diff`` 文本）以及
            ``total_tokens`` / ``estimated_cost`` / ``model_gateway_id`` /
            ``model_name`` / ``status``。
            status 可为 ``success`` / ``no_api_key`` / ``cli_not_found`` /
            ``timeout`` / ``error: ...``。
        """
        # 1) 无 key 优雅降级：codebuddy CLI 需 CODEBUDDY_API_KEY，无则不可用。
        if not self.api_key:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": "codebuddy-cli",
                "status": "no_api_key",
            }

        # 2) 拼命令：以 prompt 结尾，让 codebuddy 在 cwd 内直接读/改/跑。
        cmd = [
            self.codebuddy_bin,
            "-p",
            "--permission-mode", self.permission_mode,
            *self.extra_args,
            prompt,
        ]
        # 3) 执行；注入 CODEBUDDY_API_KEY 到环境（codebuddy 无 login 持久化）。
        try:
            subprocess.run(
                cmd,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                env={**os.environ, "CODEBUDDY_API_KEY": self.api_key},
            )
        except FileNotFoundError:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": "codebuddy-cli",
                "status": "cli_not_found",
            }
        except subprocess.TimeoutExpired:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": "codebuddy-cli",
                "status": "timeout",
            }
        except Exception as error:
            return {
                "output": "",
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "model_gateway_id": "workbuddy",
                "model_name": "codebuddy-cli",
                "status": f"error: {type(error).__name__}",
            }

        # 4) agent 已在磁盘直接改文件，取真实 git diff 作为 output（供审计/记录）。
        output = ""
        try:
            git_result = subprocess.run(
                ["git", "-C", self.cwd, "diff"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if git_result.returncode == 0:
                output = git_result.stdout
        except Exception:
            output = ""

        return {
            "output": output,
            "total_tokens": 0,
            "estimated_cost": 0.0,
            "model_gateway_id": "workbuddy",
            "model_name": "codebuddy-cli",
            "status": "success",
        }


def _build_private_capability_adapter(cap: dict[str, Any]) -> Any:
    """把 tenant_private 能力条目映射为可执行适配器。

    仅支持 OpenAI 兼容的 model / agent（与 ``main.py`` execute_model_gateway 的
    私有能力执行路径同构）：用 ``metadata`` 中的 base_url + credential_ref(env) +
    model_name 构造 ``ModelGatewayAdapter``。无可用 api_key 时返回明确失败适配器，
    交由 resolver 沿降级链换下一个能力。

    这样 pipeline 的 CapabilityResolver 才能把用户自配的私有模型（如 DeepSeek）
    作为可降级执行节点真实调用，而非因「不在候选池」而耗尽降级链升级。
    """
    meta = cap.get("private_metadata") or {}
    from .model_gateway import ModelGatewayAdapter, resolve_gateway_api_key
    from .capability_adapters import UnconfiguredAdapter

    api_key = resolve_gateway_api_key(meta.get("credential_ref"))
    if api_key:
        return ModelGatewayAdapter(
            base_url=meta.get("base_url"),
            api_key=api_key,
            gateway_id=meta.get("provider_type") or "tenant_private",
            model_name=meta.get("model_name") or cap.get("capability_key", ""),
        )
    return UnconfiguredAdapter(cap_key=str(cap.get("capability_key") or "private"))


class DevAgentFactory:
    """把能力目录条目映射为具体 ``DevAgent`` 适配器（默认工厂）。

    复用本模块既有 5 适配器；按 key / provider / type 启发式选路。非 model 类型
    由 P1 的 ``CapabilityAdapterFactory`` 接管（真实 CLI/HTTP/MCP/Webhook 适配器），
    本工厂仅负责 model / agent 类型。
    """

    @staticmethod
    def build(cap: dict[str, Any]) -> Any:
        cap_type = (cap.get("type") or "model").lower()
        key = (cap.get("capability_key") or cap.get("model_key") or "").lower()
        provider = (cap.get("provider_id") or "").lower()
        # 租户私有能力（tenant_private，OpenAI 兼容）：复用 main.py 私有模型执行路径。
        if cap.get("source") == "tenant_private" and cap.get("private_metadata"):
            return _build_private_capability_adapter(cap)
        if cap_type in ("model", "agent"):
            if "claude" in key or "anthropic" in provider or "claude" in provider:
                return ClaudeCodeAdapter()
            if "workbuddy" in key:
                return WorkBuddyAdapter()
            if "codex-cli" in key or key.endswith("-cli"):
                return CodexAgentAdapter()
            if "codebuddy" in key:
                return WorkBuddyAgentAdapter()
            # 默认 OpenAI 兼容（gpt / codex / 通用模型网关）。
            return OpenAICodexAdapter()
        # 非 model/agent：交给 P1 CapabilityAdapterFactory（不应到达此处）。
        return OpenAICodexAdapter()


__all__ = [
    "DevAgent",
    "DevAgentFactory",
    "ClaudeCodeAdapter",
    "OpenAICodexAdapter",
    "WorkBuddyAdapter",
    "CodexAgentAdapter",
    "WorkBuddyAgentAdapter",
]
