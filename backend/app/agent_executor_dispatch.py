"""Security-gated dispatcher for tenant_private ``agent`` capabilities.

GAP1 provider generalization (Issue CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION):
the live execution path used to hard-code two agent kinds (``codex-cli`` and
``openai-compatible``). This module keeps both byte-identical and additionally
routes already-built adapters to live execution:

- ``local-cli``  -> CliAdapter, command restricted to an allowlist derived from
  AGENT_ADAPTER_REGISTRY (argv list only, no shell, no tenant cwd);
- ``mcp``        -> McpAdapter, same allowlist on the stdio server argv[0];
- ``http``       -> HttpApiAdapter, http(s) URL only, env-based credentials.

Everything unrecognized or outside the security boundary fails closed with the
same configuration_rejected / 403 error shape the legacy branch used; no
subprocess is spawned and no HTTP request is issued for rejected configurations.
"""
from __future__ import annotations

import os
import shlex
from typing import Any
from pathlib import Path
from urllib.parse import urlparse

from .agent_adapter import CodexCliAdapter, AcpStdioAdapter, packaged_supervisor_command
from .ai_capability_registry import AGENT_ADAPTER_REGISTRY
from .capability_adapters import CliAdapter, HttpApiAdapter, McpAdapter
from .model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError

MAX_ARGS = 16
MAX_ARG_LEN = 256
MAX_TOOL_LEN = 64
MAX_TIMEOUT = 900
DEFAULT_CLI_TIMEOUT = 900
DEFAULT_CODEX_TIMEOUT = 300


class _LedgerIdentityMixin:
    """Fill the identity fields the live usage ledger (ai_usage.record_call)
    requires. T08 adapters return ``model_gateway_id`` but no ``provider_id``
    and expose no ``gateway_id``/``model_name`` attributes; execution semantics
    stay entirely inside the wrapped adapter, this mixin only annotates
    identity. ``provider_id`` is the honest capability category (a tenant
    configured local CLI / MCP server / HTTP API), not a vendor claim.
    """

    _provider_id = ""

    def execute(self, prompt: str) -> dict[str, Any]:
        result = dict(super().execute(prompt))
        if not result.get("provider_id"):
            result["provider_id"] = self._provider_id
        return result


class _LedgerCliAdapter(_LedgerIdentityMixin, CliAdapter):
    _provider_id = "local-cli"

    def __init__(self, config: dict[str, Any], credentials_ref: str | None = None) -> None:
        super().__init__(config, credentials_ref)
        self.gateway_id = self.model_gateway_id
        self.model_name = self.command


class _LedgerMcpAdapter(_LedgerIdentityMixin, McpAdapter):
    _provider_id = "mcp"

    def __init__(self, config: dict[str, Any], credentials_ref: str | None = None) -> None:
        super().__init__(config, credentials_ref)
        self.gateway_id = self.model_gateway_id
        self.model_name = self.server_command


class _LedgerHttpAdapter(_LedgerIdentityMixin, HttpApiAdapter):
    _provider_id = "http-agent"

    def __init__(self, config: dict[str, Any], credentials_ref: str | None = None) -> None:
        super().__init__(config, credentials_ref)
        self.gateway_id = self.model_gateway_id
        self.model_name = self.url


def _rejected(message: str) -> ModelGatewayExecutionError:
    return ModelGatewayExecutionError(
        message, status="configuration_rejected", http_status=403)


def _command_allowlist() -> frozenset[str]:
    """Allowed local command names; AGENT_ADAPTER_REGISTRY is the single source."""
    allowed: set[str] = set()
    for entry in AGENT_ADAPTER_REGISTRY.values():
        for name in entry.get("commands") or []:
            if isinstance(name, str) and name:
                allowed.add(name)
    return frozenset(allowed)


def _allowed_command(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise _rejected("agent command must be a non-empty string")
    if "/" in value or "\\" in value or ".." in value or "\x00" in value:
        raise _rejected("agent command must be a bare allowlisted command name")
    allowed = _command_allowlist()
    if not allowed or value not in allowed:
        raise _rejected(f"agent command {value!r} is not in the local agent allowlist")
    return value


def _clean_args(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > MAX_ARGS:
        raise _rejected(f"agent args must be a list of at most {MAX_ARGS} strings")
    args: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item or len(item) > MAX_ARG_LEN or "\x00" in item:
            raise _rejected("agent args must be non-empty strings")
        args.append(item)
    return args


def _timeout(value: Any, default: int) -> int:
    if value in (None, ""):
        return default
    try:
        timeout = int(value)
    except (TypeError, ValueError):
        raise _rejected("agent timeout must be an integer")
    if not 1 <= timeout <= MAX_TIMEOUT:
        raise _rejected(f"agent timeout must be between 1 and {MAX_TIMEOUT} seconds")
    return timeout


def _env_ref(value: Any) -> str | None:
    """Tenant credentials reach adapters via env references only (never inline)."""
    if value in (None, ""):
        return None
    if not isinstance(value, str) or not value.startswith("env:") or not value[4:]:
        raise _rejected("agent credential_ref must be an env: reference")
    return value


def _http_url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _rejected("http agent requires a url")
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise _rejected("http agent url must be http(s) with a host")
    return value.strip()


def _headers(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or len(value) > MAX_ARGS:
        raise _rejected("http agent headers must be an object")
    headers: dict[str, str] = {}
    for key, val in value.items():
        if not isinstance(key, str) or not key or len(key) > MAX_ARG_LEN:
            raise _rejected("http agent header names are invalid")
        if not isinstance(val, str) or len(val) > 4096 or "\x00" in val:
            raise _rejected("http agent header values are invalid")
        headers[key] = val
    return headers


def _build_local_cli(metadata: dict[str, Any]) -> CliAdapter:
    command = _allowed_command(metadata.get("command"))
    args = _clean_args(metadata.get("args"))
    if metadata.get("cwd"):
        # Tenant-controlled working directories would escape the server boundary.
        raise _rejected("local-cli agent does not accept a custom cwd")
    return _LedgerCliAdapter(
        {
            "command": command,
            "args": args,
            "append_prompt": True,
            "timeout": _timeout(metadata.get("timeout"), DEFAULT_CLI_TIMEOUT),
        },
        _env_ref(metadata.get("credential_ref") or metadata.get("config_ref")),
    )


def _build_mcp(metadata: dict[str, Any]) -> McpAdapter:
    raw = metadata.get("server_command")
    if not isinstance(raw, str) or not raw.strip():
        raise _rejected("mcp agent requires a server_command")
    try:
        argv = shlex.split(raw)
    except ValueError:
        raise _rejected("mcp server_command is not valid argv")
    if not argv:
        raise _rejected("mcp server_command must not be empty")
    _allowed_command(argv[0])
    _clean_args(argv[1:])
    tool_name = metadata.get("tool_name", "run")
    if not isinstance(tool_name, str) or not tool_name or len(tool_name) > MAX_TOOL_LEN:
        raise _rejected("mcp tool_name must be a short string")
    return _LedgerMcpAdapter(
        {
            "server_command": shlex.join(argv),
            "tool_name": tool_name,
            "timeout": _timeout(metadata.get("timeout"), DEFAULT_CLI_TIMEOUT),
        },
        _env_ref(metadata.get("credential_ref") or metadata.get("config_ref")),
    )


def _build_http(metadata: dict[str, Any]) -> HttpApiAdapter:
    url = _http_url(metadata.get("url") or metadata.get("endpoint"))
    method = str(metadata.get("method") or "POST").upper()
    if method not in {"POST", "PUT"}:
        raise _rejected("http agent method must be POST or PUT")
    auth_env = None
    if metadata.get("auth_env"):
        auth_env = _env_ref(metadata["auth_env"])
    return _LedgerHttpAdapter(
        {
            "url": url,
            "method": method,
            "headers": _headers(metadata.get("headers")),
            "timeout": _timeout(metadata.get("timeout"), DEFAULT_CLI_TIMEOUT),
            "auth_env": auth_env,
        },
        _env_ref(metadata.get("credential_ref") or metadata.get("config_ref")),
    )


def build_agent_executor(
    metadata: dict[str, Any],
    *,
    resolved_api_key: str | None,
    default_executor: ModelGatewayAdapter,
    capability_id: str = "",
    execution_context: dict[str, Any] | None = None,
) -> Any:
    """Build a live executor for a tenant_private agent capability.

    Raises ModelGatewayExecutionError(status=configuration_rejected, 403) on
    anything outside the allowed configuration surface.
    """
    metadata = metadata or {}
    kind = str(metadata.get("kind") or "openai-compatible").strip().lower()

    if kind == "acp-stdio":
        from .agent_adapter import require_acp_execution_available
        from .ai_capability_registry import acp_installation
        # Before install reads, credential resolution, reservation or resource allocation.
        require_acp_execution_available()
        context = execution_context or {}
        if (resolved_api_key or metadata.get("credential_ref") or metadata.get("config_ref")
                or any(key in metadata for key in ("command", "args", "cwd", "environment", "profile_home"))
                or not context.get("cwd") or not callable(context.get("before_launch"))
                or not callable(context.get("should_stop"))):
            raise _rejected("ACP requires the original Work's host-owned context; personal credentials are unsupported")
        try:
            installation = acp_installation(metadata.get("agent_id", ""))
        except (ValueError, OSError) as error:
            raise _rejected("ACP installation is unavailable or changed") from error
        if metadata.get("installation_ref") != installation["installation_ref"]:
            raise _rejected("ACP installation reference does not match")
        shared_account = metadata.get("dsh_shared_account", False)
        if type(shared_account) is not bool or (shared_account and metadata.get("agent_id") != "deepseek_harness"):
            raise _rejected("DSH shared account requires explicit installation-specific consent")
        return AcpStdioAdapter(installation=installation, cwd=context["cwd"],
            profile_home=str(Path(context["cwd"]) / ".acp-home"),
            shared_account=shared_account,
            timeout=min(_timeout(metadata.get("timeout"), 90), int(context.get("max_seconds") or 90), 90),
            should_stop=context["should_stop"], before_launch=context["before_launch"],
            on_progress=context.get("on_progress", lambda _stage: None),
            on_local_state=context.get("on_local_state", lambda _receipt: None),
            tool_url=context.get("tool_url", ""), tool_token=(context.get("environment") or {}).get("CURIS_AGENT_TOOL_TOKEN", ""))

    if kind == "codex-cli":
        context = execution_context or {}
        return CodexCliAdapter(
            cwd=context.get("cwd") or metadata.get("cwd") or os.getcwd(),
            sandbox=metadata.get("sandbox") or None,
            requested_intent=metadata.get("computer_access_intent") or "",
            timeout=min(int(metadata.get("timeout") or DEFAULT_CODEX_TIMEOUT), int(context.get("max_seconds") or MAX_TIMEOUT), MAX_TIMEOUT),
            **({"environment": context["environment"], "should_stop": context["should_stop"],
                "on_progress": context["on_progress"], "before_launch": context["before_launch"],
                "on_local_state": context.get("on_local_state"),
                "supervisor_command": packaged_supervisor_command(), "tool_url": context.get("tool_url")} if context else {}),
        )

    if kind == "openai-compatible":
        endpoint = str(metadata.get("endpoint") or "").rstrip("/")
        if not endpoint or not resolved_api_key:
            raise _rejected(
                f"tenant_private agent kind={kind!r} is not configured for execution")
        return ModelGatewayAdapter(
            base_url=endpoint,
            api_key=resolved_api_key,
            gateway_id=kind,
            model_name=metadata.get("model_name") or capability_id or "agent",
            timeout=default_executor.timeout,
            http_post=default_executor.http_post,
        )

    if kind == "local-cli":
        return _build_local_cli(metadata)
    if kind == "mcp":
        return _build_mcp(metadata)
    if kind == "http":
        return _build_http(metadata)

    raise _rejected(f"tenant_private agent kind={kind!r} is not configured for execution")
