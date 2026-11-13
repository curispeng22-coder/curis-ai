"""P1 统一适配器抽象（T08）：CLI / HTTP API / Webhook / MCP / Local Process。

把 P0 的 ``DevAgent`` 协议泛化为 ``CapabilityAdapter``，使「能力执行」不再局限于
model/agent 类型，可覆盖 CLI 工具、HTTP API、Webhook、MCP server 等外部能力。
所有适配器返回统一结构：{output, status, model_gateway_id?, model_name?, ...}，
status ∈ {success, no_api_key, cli_not_found, timeout, error:*}，与既有 DevAgent
保持一致（CapabilityHandle.execute 不变）。

设计要点（沿用 P0 §8② 静默降级、§7 共享约定）：
- 零新依赖：仅 Python 标准库 + 已装 httpx。
- 密钥不落明文：credentials_ref = "env:XXX" → 仅从 os.environ["XXX"] 读取。
- McpAdapter 走 stdio JSON-RPC 最小路径（initialize + tools/call 单次；完整
  tools 发现/编排标后续，见文档 §8 待确认项）。
- CapabilityAdapterFactory.build(cap) 重构原 DevAgentFactory，按 runtime_meta.
  adapter_kind 分派；model/agent 类型回落复用 dev_agent 既有 5 适配器。
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
from typing import Any, Protocol, runtime_checkable

try:
    import httpx
except Exception:  # pragma: no cover - httpx 为已装依赖，缺失则相关适配器不可用
    httpx = None  # type: ignore

from .dev_agent import DevAgentFactory


@runtime_checkable
class CapabilityAdapter(Protocol):
    """统一能力适配器协议（泛化 DevAgent）。"""

    def execute(self, prompt: str) -> dict[str, Any]:
        """执行能力，返回 {output, status, ...}。

        status ∈ {success, no_api_key, cli_not_found, timeout, error:*}。
        """
        ...


def _resolve_credentials_env(credentials_ref: str | None) -> dict[str, str]:
    """把 credentials_ref（"env:XXX"）解析为 {XXX: os.environ[XXX]}。

    仅取 env 名从 os.environ 读，绝不存储明文。非法形态返回空 dict。
    """
    if not credentials_ref or not credentials_ref.startswith("env:"):
        return {}
    env_name = credentials_ref[len("env:"):]
    if not env_name:
        return {}
    return {env_name: os.environ.get(env_name, "")}


class CliAdapter:
    """本地进程适配器（= Local Process Adapter）：subprocess 执行命令。

    adapter_config: {command, args?, cwd?, env_keys?, timeout?, credentials_ref?}
    prompt 作为末位位置参数传入（命令自行解析任务指令）；stdout 为 output。
    """

    def __init__(self, config: dict[str, Any] | None = None, credentials_ref: str | None = None) -> None:
        config = config or {}
        self.command = config.get("command") or ""
        self.args = list(config.get("args") or [])
        self.append_prompt = config.get("append_prompt", True) is not False
        self.cwd = config.get("cwd")
        self.env_keys = list(config.get("env_keys") or [])
        self.timeout = int(config.get("timeout") or 900)
        self.credentials_ref = credentials_ref or config.get("credentials_ref")
        self.model_gateway_id = f"cli:{self.command}"

    def execute(self, prompt: str) -> dict[str, Any]:
        if not self.command:
            return {"output": "", "status": "error:no_command", "model_gateway_id": self.model_gateway_id}
        env = dict(os.environ)
        env.update(_resolve_credentials_env(self.credentials_ref))
        for k in self.env_keys:
            if k in os.environ:
                env[k] = os.environ[k]
        cmd = [self.command, *self.args, *([prompt] if self.append_prompt else [])]
        try:
            proc = subprocess.run(cmd, cwd=self.cwd, env=env, capture_output=True, text=True, timeout=self.timeout)
        except FileNotFoundError:
            return {"output": "", "status": "cli_not_found", "model_gateway_id": self.model_gateway_id}
        except subprocess.TimeoutExpired:
            return {"output": "", "status": "timeout", "model_gateway_id": self.model_gateway_id}
        except Exception as error:
            return {"output": "", "status": f"error:{type(error).__name__}", "model_gateway_id": self.model_gateway_id}
        status = "success" if proc.returncode == 0 else f"cli_exit_{proc.returncode}"
        return {
            "output": proc.stdout or proc.stderr,
            "status": status,
            "model_gateway_id": self.model_gateway_id,
            "model_name": self.command,
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }


class HttpApiAdapter:
    """HTTP API 适配器：httpx 调用外部 API（prompt 经 JSON body 下发）。"""

    def __init__(self, config: dict[str, Any] | None = None, credentials_ref: str | None = None) -> None:
        config = config or {}
        self.url = config.get("url") or ""
        self.method = (config.get("method") or "POST").upper()
        self.auth_env = config.get("auth_env")
        self.headers = dict(config.get("headers") or {})
        self.timeout = int(config.get("timeout") or 900)
        self.credentials_ref = credentials_ref or config.get("credentials_ref")
        self.model_gateway_id = f"http:{self.url}"

    def execute(self, prompt: str) -> dict[str, Any]:
        if httpx is None:
            return {"output": "", "status": "error:no_httpx", "model_gateway_id": self.model_gateway_id}
        if not self.url:
            return {"output": "", "status": "error:no_url", "model_gateway_id": self.model_gateway_id}
        env = dict(os.environ)
        env.update(_resolve_credentials_env(self.credentials_ref))
        headers = dict(self.headers)
        auth_value = None
        if self.auth_env:
            auth_value = _resolve_credentials_env(self.auth_env).get(self.auth_env[len("env:"):])
        if auth_value:
            headers["authorization"] = f"Bearer {auth_value}"
        try:
            resp = httpx.request(self.method, self.url, json={"prompt": prompt}, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            try:
                data = resp.json()
                if isinstance(data, dict):
                    output = data.get("output", "") or json.dumps(data, ensure_ascii=False)
                else:
                    output = resp.text
            except Exception:
                output = resp.text
        except Exception as error:
            return {"output": "", "status": f"error:{type(error).__name__}", "model_gateway_id": self.model_gateway_id}
        return {
            "output": output,
            "status": "success",
            "model_gateway_id": self.model_gateway_id,
            "model_name": self.url,
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }


class WebhookAdapter(HttpApiAdapter):
    """Webhook 适配器：HttpApiAdapter 特化，fire-and-forget。

    仍发出 POST 请求（带 prompt），但不依赖业务回执，立即返回 dispatched。
    网络错误不视为失败（仅记录），保证 webhook 触发类能力恒可调度。
    """

    def __init__(self, config: dict[str, Any] | None = None, credentials_ref: str | None = None) -> None:
        super().__init__(config, credentials_ref)
        self.method = "POST"

    def execute(self, prompt: str) -> dict[str, Any]:
        if httpx is None:
            return {"output": "", "status": "error:no_httpx", "model_gateway_id": self.model_gateway_id}
        if not self.url:
            return {"output": "", "status": "error:no_url", "model_gateway_id": self.model_gateway_id}
        env = dict(os.environ)
        env.update(_resolve_credentials_env(self.credentials_ref))
        headers = dict(self.headers)
        auth_value = None
        if self.auth_env:
            auth_value = _resolve_credentials_env(self.auth_env).get(self.auth_env[len("env:"):])
        if auth_value:
            headers["authorization"] = f"Bearer {auth_value}"
        try:
            httpx.request("POST", self.url, json={"prompt": prompt}, headers=headers, timeout=self.timeout)
        except Exception:
            pass  # fire-and-forget：网络异常不阻断调度。
        return {
            "output": "dispatched",
            "status": "success",
            "model_gateway_id": self.model_gateway_id,
            "model_name": self.url,
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }


class McpAdapter:
    """MCP 适配器：stdio JSON-RPC 最小路径（initialize + tools/call 单次）。

    以 ``server_command`` 经 stdio 启 MCP server 子进程，读取 initialize 响应后
    发送 notifications/initialized，再 tools/call（参数 {"prompt": prompt}）取回
    text 结果。完整 tools 发现/多工具编排标后续补全点（文档 §8）。
    """

    def __init__(self, config: dict[str, Any] | None = None, credentials_ref: str | None = None) -> None:
        config = config or {}
        self.server_command = config.get("server_command") or ""
        self.tool_name = config.get("tool_name") or "run"
        self.timeout = int(config.get("timeout") or 900)
        self.credentials_ref = credentials_ref or config.get("credentials_ref")
        self.model_gateway_id = f"mcp:{self.server_command}"

    def execute(self, prompt: str) -> dict[str, Any]:
        if not self.server_command:
            return {"output": "", "status": "error:no_server_command", "model_gateway_id": self.model_gateway_id}
        try:
            cmd = shlex.split(self.server_command)
        except Exception:
            cmd = self.server_command.split()
        env = dict(os.environ)
        env.update(_resolve_credentials_env(self.credentials_ref))
        try:
            proc = subprocess.Popen(
                cmd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1,
            )
        except FileNotFoundError:
            return {"output": "", "status": "cli_not_found", "model_gateway_id": self.model_gateway_id}
        except Exception as error:
            return {"output": "", "status": f"error:{type(error).__name__}", "model_gateway_id": self.model_gateway_id}

        def _send(obj: dict[str, Any]) -> None:
            try:
                assert proc.stdin is not None
                proc.stdin.write(json.dumps(obj) + "\n")
                proc.stdin.flush()
            except Exception:
                pass

        output = ""
        try:
            # 1) initialize
            _send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                              "clientInfo": {"name": "curis", "version": "1.0"}}})
            try:
                assert proc.stdout is not None
                proc.stdout.readline()
            except Exception:
                pass
            # 2) initialized 通知
            _send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
            # 3) tools/call
            _send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                   "params": {"name": self.tool_name, "arguments": {"prompt": prompt}}})
            try:
                assert proc.stdout is not None
                line = proc.stdout.readline()
                if line:
                    output = self._extract_tool_output(json.loads(line))
            except Exception:
                pass
        finally:
            try:
                if proc.stdin is not None:
                    proc.stdin.close()
            except Exception:
                pass
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        return {
            "output": output,
            "status": "success" if output else "error:mcp_no_output",
            "model_gateway_id": self.model_gateway_id,
            "model_name": self.server_command,
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }

    @staticmethod
    def _extract_tool_output(data: dict[str, Any]) -> str:
        """从 tools/call 结果 JSON 中提取 text 片段。"""
        result = data.get("result") or {}
        content = result.get("content") or []
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "\n".join(parts)


class UnconfiguredAdapter:
    """未配置真实适配器的能力 → 明确失败，触发 resolver 静默降级（不再恒 success）。

    取代 P0 的 NullDevAgent（恒 success），使「非 model 类型无真实适配器」在运行期
    表现为失败并被降级链/升级正确处理，而非假装成功。
    """

    def __init__(self, cap_key: str = "unconfigured") -> None:
        self.cap_key = cap_key

    def execute(self, prompt: str) -> dict[str, Any]:
        return {
            "output": "",
            "status": "error:adapter_not_configured",
            "model_gateway_id": self.cap_key,
            "model_name": self.cap_key,
            "total_tokens": 0,
            "estimated_cost": 0.0,
        }


class CapabilityAdapterFactory:
    """按 catalog 条目的 runtime_meta.adapter_kind 分派具体 CapabilityAdapter。

    取代 P0 的 DevAgentFactory（后者仅覆盖 model/agent）。adapter_kind 来自
    runtime_meta；缺省时按 type/key 启发式推断。model/agent 回落复用 dev_agent
    既有适配器；cli/local → CliAdapter；http → HttpApiAdapter；webhook →
    WebhookAdapter；mcp → McpAdapter；其余（无真实适配器） → UnconfiguredAdapter。
    """

    @staticmethod
    def build(cap: dict[str, Any]) -> CapabilityAdapter:
        cap_type = (cap.get("type") or "model").lower()
        runtime_meta = cap.get("runtime_meta") or {}
        # 同时兼容 DB 行（嵌套 runtime_meta）与 API view（adapter_* 拍平到顶层）两种形态。
        adapter_kind = (runtime_meta.get("adapter_kind") or cap.get("adapter_kind") or "").lower()
        adapter_config = runtime_meta.get("adapter_config") or cap.get("adapter_config") or {}
        credentials_ref = runtime_meta.get("credentials_ref") or cap.get("credential_ref")
        key = (cap.get("capability_key") or cap.get("model_key") or "").lower()

        if not adapter_kind:
            # 未显式配置 adapter_kind → 按类型/key 启发式推断。
            if cap_type in ("model", "agent"):
                adapter_kind = "model"
            elif cap_type in ("cli", "local"):
                adapter_kind = "cli"
            elif cap_type == "http":
                adapter_kind = "http"
            elif cap_type == "webhook":
                adapter_kind = "webhook"
            elif cap_type == "mcp":
                adapter_kind = "mcp"
            else:
                adapter_kind = ""

        if adapter_kind in ("model", "agent"):
            return DevAgentFactory.build(cap)
        if adapter_kind in ("cli", "local"):
            return CliAdapter(adapter_config, credentials_ref)
        if adapter_kind == "http":
            return HttpApiAdapter(adapter_config, credentials_ref)
        if adapter_kind == "webhook":
            return WebhookAdapter(adapter_config, credentials_ref)
        if adapter_kind == "mcp":
            return McpAdapter(adapter_config, credentials_ref)
        # 无真实适配器：明确失败，交由 resolver 降级（取代 NullDevAgent 恒 success）。
        return UnconfiguredAdapter(cap_key=key)


__all__ = [
    "CapabilityAdapter",
    "CliAdapter",
    "HttpApiAdapter",
    "WebhookAdapter",
    "McpAdapter",
    "UnconfiguredAdapter",
    "CapabilityAdapterFactory",
]
