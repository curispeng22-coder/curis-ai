"""Tests for the GAP1 security-gated agent executor dispatcher."""
import json
import os
import stat
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from app.agent_adapter import CodexCliAdapter
from app.agent_executor_dispatch import build_agent_executor, _command_allowlist
from app.capability_adapters import CliAdapter, HttpApiAdapter, McpAdapter
from app.model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError


def _default_executor():
    def fake_post(url, payload, headers, timeout):
        raise AssertionError("default provider must not be called")

    return ModelGatewayAdapter(
        base_url="https://provider.invalid", api_key="test-only",
        gateway_id="qa-default", model_name="default-model", http_post=fake_post)


def _rejected(metadata, **kwargs):
    with pytest.raises(ModelGatewayExecutionError) as exc:
        build_agent_executor(metadata, default_executor=_default_executor(), **kwargs)
    assert exc.value.status == "configuration_rejected"
    assert exc.value.http_status == 403
    return exc.value


# ── codex-cli / openai-compatible preserved ──────────────────────────────────

def test_codex_cli_preserved():
    executor = build_agent_executor(
        {"kind": "codex-cli", "cwd": "/tmp/qa", "sandbox": "workspace-write",
         "computer_access_intent": "AUTO_WITHIN_BOUNDARY", "timeout": 120},
        resolved_api_key=None, default_executor=_default_executor())
    assert isinstance(executor, CodexCliAdapter)
    assert executor.cwd == os.path.realpath("/tmp/qa")
    assert executor.sandbox == "workspace-write"
    assert executor.requested_intent == "AUTO_WITHIN_BOUNDARY"
    assert executor.timeout == 120


def test_openai_compatible_preserved():
    executor = build_agent_executor(
        {"kind": "openai-compatible", "endpoint": "http://127.0.0.1:9/v1",
         "model_name": "agent-x"},
        resolved_api_key="secret", default_executor=_default_executor())
    assert isinstance(executor, ModelGatewayAdapter)
    assert executor.base_url == "http://127.0.0.1:9/v1"
    assert executor.model_name == "agent-x"


def test_openai_compatible_capability_id_fallback():
    executor = build_agent_executor(
        {"kind": "openai-compatible", "endpoint": "http://127.0.0.1:9"},
        resolved_api_key="secret", default_executor=_default_executor(),
        capability_id="cap-42")
    assert executor.model_name == "cap-42"


def test_openai_compatible_missing_configuration_rejected():
    _rejected({"kind": "openai-compatible"}, resolved_api_key=None)
    _rejected({"kind": "openai-compatible", "endpoint": "http://x"}, resolved_api_key=None)
    _rejected({"kind": "openai-compatible", "endpoint": ""}, resolved_api_key="k")


def test_unknown_kind_rejected():
    _rejected({"kind": "ransomware-shell"}, resolved_api_key=None)
    # default kind when metadata.kind missing behaves like the legacy branch
    _rejected({}, resolved_api_key=None)


# ── allowlist facts ──────────────────────────────────────────────────────────

def test_allowlist_comes_from_registry():
    allow = _command_allowlist()
    assert "codex" in allow and "claude" in allow and "gemini" in allow
    for forbidden in ("bash", "sh", "zsh", "python3", "cmd", "powershell"):
        assert forbidden not in allow


# ── local-cli ────────────────────────────────────────────────────────────────

def test_local_cli_builds_allowlisted():
    executor = build_agent_executor(
        {"kind": "local-cli", "command": "claude", "args": ["-p", "--model", "sonnet"],
         "timeout": 60, "credential_ref": "env:QA_CLAUDE_KEY"},
        resolved_api_key=None, default_executor=_default_executor())
    assert isinstance(executor, CliAdapter)
    assert executor.command == "claude"
    assert executor.args == ["-p", "--model", "sonnet"]
    assert executor.timeout == 60
    assert executor.cwd is None  # tenant cwd never accepted


@pytest.mark.parametrize("command", [
    "bash", "sh", "zsh", "python3", "/usr/bin/claude", "../claude",
    "claude; rm", "tmp/claude", "", 123,
])
def test_local_cli_command_rejected(command):
    _rejected({"kind": "local-cli", "command": command}, resolved_api_key=None)


def test_local_cli_args_validation():
    base = {"kind": "local-cli", "command": "claude"}
    _rejected({**base, "args": "-p"}, resolved_api_key=None)
    _rejected({**base, "args": ["x"] * 17}, resolved_api_key=None)
    _rejected({**base, "args": [""]}, resolved_api_key=None)
    _rejected({**base, "args": [1]}, resolved_api_key=None)
    _rejected({**base, "args": ["x" * 257]}, resolved_api_key=None)
    _rejected({**base, "cwd": "/"}, resolved_api_key=None)
    _rejected({**base, "timeout": 0}, resolved_api_key=None)
    _rejected({**base, "timeout": 901}, resolved_api_key=None)
    _rejected({**base, "credential_ref": "plaintext-secret"}, resolved_api_key=None)
    _rejected({**base, "credential_ref": "vault:x"}, resolved_api_key=None)


def test_local_cli_executes_allowlisted_stub_as_argv(tmp_path, monkeypatch):
    stub = tmp_path / "claude"
    stub.write_text("#!/usr/bin/env python3\nimport sys\nprint('OK:' + repr(sys.argv[1:]))\n")
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    executor = build_agent_executor(
        {"kind": "local-cli", "command": "claude", "args": ["--flag"]},
        resolved_api_key=None, default_executor=_default_executor())
    result = executor.execute("do thing; rm -rf /")
    assert result["status"] == "success"
    # prompt is a single argv element — no shell interpretation can occur
    assert "do thing; rm -rf /" in result["output"]
    assert "'--flag'" in result["output"]
    # ledger identity fields required by ai_usage.record_call
    assert executor.gateway_id == "cli:claude"
    assert executor.model_name == "claude"
    assert result["provider_id"] == "local-cli"


# ── mcp ──────────────────────────────────────────────────────────────────────

def test_mcp_builds_and_validates_server_argv():
    executor = build_agent_executor(
        {"kind": "mcp", "server_command": "gemini mcp serve", "tool_name": "chat"},
        resolved_api_key=None, default_executor=_default_executor())
    assert isinstance(executor, McpAdapter)
    assert executor.server_command.startswith("gemini")
    assert executor.tool_name == "chat"


@pytest.mark.parametrize("command", [
    "sh -c evil", "bash -i", "python3 -c 'x'", "/bin/gemini",
])
def test_mcp_server_command_rejected(command):
    _rejected({"kind": "mcp", "server_command": command}, resolved_api_key=None)


def test_mcp_misc_validation():
    _rejected({"kind": "mcp"}, resolved_api_key=None)
    _rejected({"kind": "mcp", "server_command": ""}, resolved_api_key=None)
    _rejected({"kind": "mcp", "server_command": "gemini", "tool_name": ""}, resolved_api_key=None)
    _rejected({"kind": "mcp", "server_command": "gemini", "tool_name": "x" * 65},
              resolved_api_key=None)


def test_mcp_executes_stdio_stub(tmp_path, monkeypatch):
    stub = tmp_path / "gemini"
    stub.write_text(
        "#!/usr/bin/env python3\n" +
        "import sys, json\n"
        "sys.stdin.readline()\n"  # initialize request
        "print(json.dumps({'jsonrpc':'2.0','id':1,'result':{}}), flush=True)\n"
        "line = sys.stdin.readline()\n"  # initialized notification
        "line = sys.stdin.readline()\n"  # tools/call
        "prompt = json.loads(line)['params']['arguments']['prompt']\n"
        "print(json.dumps({'jsonrpc':'2.0','id':2,'result':{"
        "'content':[{'type':'text','text':'MCP:'+prompt}]}}), flush=True)\n")
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    executor = build_agent_executor(
        {"kind": "mcp", "server_command": "gemini"},
        resolved_api_key=None, default_executor=_default_executor())
    result = executor.execute("hello mcp")
    assert result["status"] == "success"
    assert result["output"] == "MCP:hello mcp"
    # ledger identity fields required by ai_usage.record_call
    assert executor.gateway_id == "mcp:gemini"
    assert executor.model_name == "gemini"
    assert result["provider_id"] == "mcp"


# ── http ─────────────────────────────────────────────────────────────────────

def test_http_build_validation():
    executor = build_agent_executor(
        {"kind": "http", "url": "https://agent.example/run", "headers": {"X-Tenant": "a"}},
        resolved_api_key=None, default_executor=_default_executor())
    assert isinstance(executor, HttpApiAdapter)
    assert executor.url == "https://agent.example/run"


@pytest.mark.parametrize("url", [
    "file:///etc/passwd", "ftp://x/y", "", "not a url", "http://",
])
def test_http_url_rejected(url):
    _rejected({"kind": "http", "url": url}, resolved_api_key=None)


def test_http_method_and_headers_validation():
    base = {"kind": "http", "url": "https://x/y"}
    _rejected({**base, "method": "GET"}, resolved_api_key=None)
    _rejected({**base, "headers": "no"}, resolved_api_key=None)
    _rejected({**base, "headers": {1: "v"}}, resolved_api_key=None)
    _rejected({**base, "auth_env": "QA_HTTP_KEY"}, resolved_api_key=None)


def test_http_executes_against_local_stub(tmp_path, monkeypatch):
    seen = {}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("content-length", 0))
            seen["body"] = json.loads(self.rfile.read(length))
            seen["auth"] = self.headers.get("authorization")
            body = json.dumps({"output": "HTTP-OK"}).encode()
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        monkeypatch.setenv("QA_HTTP_AGENT_KEY", "bearer-token")
        executor = build_agent_executor(
            {"kind": "http", "url": f"http://127.0.0.1:{port}/run",
             "auth_env": "env:QA_HTTP_AGENT_KEY", "timeout": 10},
            resolved_api_key=None, default_executor=_default_executor())
        result = executor.execute("ping")
    finally:
        server.shutdown()
    assert result["status"] == "success"
    assert result["output"] == "HTTP-OK"
    assert seen["body"] == {"prompt": "ping"}
    assert seen["auth"] == "Bearer bearer-token"
    # ledger identity fields required by ai_usage.record_call
    assert executor.gateway_id == f"http:http://127.0.0.1:{port}/run"
    assert executor.model_name == f"http://127.0.0.1:{port}/run"
    assert result["provider_id"] == "http-agent"


def test_acp_dispatch_is_held_without_resolving_install_or_context(monkeypatch):
    import app.ai_capability_registry as registry
    def forbidden(*args, **kwargs): pytest.fail("installation lookup while held")
    monkeypatch.setattr(registry, "acp_installation", forbidden)
    from app.agent_adapter import AgentExecutionError
    with pytest.raises(AgentExecutionError) as error:
        build_agent_executor({"kind": "acp-stdio", "agent_id": "deepseek_harness"},
            resolved_api_key=None, default_executor=_default_executor())
    assert error.value.status == "acp_execution_held" and not error.value.outbound_attempted


def test_acp_dispatch_uses_only_original_work_context_and_install_reference(tmp_path, monkeypatch):
    import app.agent_adapter as module
    import app.ai_capability_registry as registry
    from app.agent_adapter import AcpStdioAdapter
    monkeypatch.setattr(module, "ACP_LOCAL_EXECUTION_VERIFIED", True)
    install = {"agent_id": "deepseek_harness", "installation_ref": "a" * 64, "command": ["/synthetic/dsh", "--profile", "acp"]}
    monkeypatch.setattr(registry, "acp_installation", lambda _: install)
    metadata = {"kind": "acp-stdio", "agent_id": "deepseek_harness", "installation_ref": "a" * 64}
    context = {"cwd": str(tmp_path), "max_seconds": 20, "before_launch": lambda: None, "should_stop": lambda: False}
    adapter = build_agent_executor(metadata, resolved_api_key=None, default_executor=_default_executor(), execution_context=context)
    assert isinstance(adapter, AcpStdioAdapter) and adapter.timeout == 20
    assert adapter.profile_home == str(tmp_path / ".acp-home")
    assert adapter.shared_account is False
    shared = build_agent_executor({**metadata, "dsh_shared_account": True}, resolved_api_key=None,
        default_executor=_default_executor(), execution_context=context)
    assert shared.shared_account is True and shared.cwd == str(tmp_path)
    for consent in ("true", 1, None, {}):
        _rejected({**metadata, "dsh_shared_account": consent}, resolved_api_key=None, execution_context=context)
    for key in ("command", "args", "cwd", "environment", "profile_home", "credential_ref", "config_ref"):
        _rejected({**metadata, key: "/personal"}, resolved_api_key=None, execution_context=context)
    _rejected({**metadata, "installation_ref": "b" * 64}, resolved_api_key=None, execution_context=context)
    _rejected(metadata, resolved_api_key="secret", execution_context=context)
    _rejected(metadata, resolved_api_key=None)
