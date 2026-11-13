from __future__ import annotations

import json
import asyncio
import contextlib
from importlib.metadata import version, PackageNotFoundError
import hashlib
import math
import os
import pwd
import selectors
import signal
import shutil
import subprocess
import sys
import stat
import select
import threading
import time
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from uuid import UUID, uuid4

CODEX_EXECUTION_HOLD_CODE = "codex_execution_held"
# Release requires independent proof of process ownership, cleanup and unknown effects.
CODEX_STOP_VERIFIED = False
# CPU-only container candidates do not release Linux Codex/auth/tools or egress.
AGENT_CONTAINER_EXECUTION_VERIFIED = False

# Keep actual Popen objects when a bounded reap cannot establish child exit.
# This is process-local retention, not proof of descendant cleanup or a
# persistent recovery ledger. The real execution gate remains closed.
_UNRESOLVED_SUPERVISORS: list[subprocess.Popen] = []
_UNRESOLVED_SUPERVISORS_LOCK = threading.Lock()
_SUPERVISOR_ADMISSION = threading.Lock()
# Coordinates stop and child creation in this workspace process only.
_AGENT_STOP_SPAWN_LOCK = threading.RLock()


def _verified_child_exit_receipt(data: bytes, nonce: str, supervisor_returncode: int | None):
    """Accept only the owned supervisor's complete, attempt-bound stop receipt."""
    if len(data) > 4096 or not data.endswith(b"\n") or len(data.splitlines()) != 1:
        return None
    def unique_keys(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate receipt field")
            value[key] = item
        return value
    try:
        value = json.loads(data, object_pairs_hook=unique_keys)
    except (UnicodeError, ValueError):
        return None
    if (not isinstance(value, dict) or set(value) != {"type", "nonce", "child_pid", "returncode"}
            or value["type"] != "curis.supervisor.child_reaped" or value["nonce"] != nonce
            or type(value["child_pid"]) is not int or value["child_pid"] <= 1
            or type(value["returncode"]) is not int or not -255 <= value["returncode"] <= 255
            or supervisor_returncode != -signal.SIGKILL):
        return None
    return {"child_pid": value["child_pid"], "returncode": value["returncode"],
            "attempt_sha256": hashlib.sha256(nonce.encode("ascii")).hexdigest()}


def agent_stop_serialized(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        with _AGENT_STOP_SPAWN_LOCK:
            return function(*args, **kwargs)
    return wrapped

PROVED_CODEX_SHA256 = "80a3933d11a9d13ef806aa24f7bb8afc9169cfe4e9b09d6da6a92922cbde9cff"


def local_codex_executable() -> str:
    """Find the verified installed SDK without relying on a Finder shell PATH."""
    managed = os.environ.get("CURIS_CODEX_EXECUTABLE", "")
    standard = Path.home() / ".codex/packages/standalone/releases/0.144.6-aarch64-apple-darwin/bin/codex"
    candidates = [managed] if managed else [str(standard), shutil.which("codex")]
    for value in candidates:
        if not value:
            continue
        try:
            path = Path(value).resolve(strict=True)
            if path.is_file() and os.access(path, os.X_OK) and hashlib.sha256(path.read_bytes()).hexdigest() == PROVED_CODEX_SHA256:
                return str(path)
        except OSError:
            continue
    return ""


def installation_id_snapshot(path: Path) -> dict[str, Any]:
    """Inspect only the SDK's non-secret installation identifier; never return its bytes."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(descriptor)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1
                or stat.S_IMODE(info.st_mode) != 0o644 or info.st_size != 36):
            raise ValueError("Native installation metadata does not match the approved existing file")
        raw = os.read(descriptor, 37)
        if len(raw) != 36 or str(UUID(raw.decode("ascii"))) != raw.decode("ascii"):
            raise ValueError("Native installation metadata must already contain a valid identifier")
        return {"sha256": hashlib.sha256(raw).hexdigest(), "mode": stat.S_IMODE(info.st_mode),
                "uid": info.st_uid, "size": info.st_size, "inode": info.st_ino, "device": info.st_dev}
    finally:
        os.close(descriptor)


def packaged_supervisor_command() -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "--curis-agent-supervisor"]
    entry = Path(__file__).resolve().parents[2] / "desktop/runtime/backend_entry.py"
    return [sys.executable, "-I", "-S", "-B", str(entry), "--curis-agent-supervisor"]


def run_agent_supervisor() -> int:
    """Dispatch only after the fixed stop-safety release gate."""
    if not CODEX_STOP_VERIFIED:
        return 2
    return _run_agent_supervisor_candidate()


def _run_agent_supervisor_candidate() -> int:
    """Unreleased candidate: a live session leader anchors its own group."""
    channel = sys.stdin.fileno()
    if (os.getpid() != os.getsid(0) or os.getpid() != os.getpgrp()
            or not stat.S_ISFIFO(os.fstat(channel).st_mode)):
        return 2
    os.set_inheritable(channel, False)
    os.set_inheritable(sys.stderr.fileno(), False)
    os.set_blocking(channel, False)
    header = bytearray()
    started = time.monotonic()
    setup_deadline = started + 3
    while b"\n" not in header:
        remaining = setup_deadline - time.monotonic()
        if remaining <= 0 or not select.select([channel], [], [], remaining)[0]:
            return 2
        chunk = os.read(channel, 65536)
        if not chunk or len(header) + len(chunk) > 1024 * 1024:
            return 2
        header.extend(chunk)
    first, extra = bytes(header).split(b"\n", 1)
    if extra:
        return 2
    try:
        request = json.loads(first)
        fields = {"command", "cwd", "environment", "prompt", "timeout", "nonce"}
        if set(request) not in (fields, fields | {"deadline"}):
            return 2
        command, environment = request["command"], request["environment"]
        if (not isinstance(command, list) or not command or len(command) > 128
                or not all(isinstance(arg, str) and "\0" not in arg for arg in command)
                or not Path(command[0]).is_absolute() or not Path(request["cwd"]).is_dir()
                or not isinstance(environment, dict)
                or not all(isinstance(k, str) and isinstance(v, str) for k, v in environment.items())
                or type(request["timeout"]) not in {int, float} or not 0 < request["timeout"] <= 90
                or not isinstance(request["prompt"], str)
                or not isinstance(request["nonce"], str) or len(request["nonce"]) != 32
                or any(c not in "0123456789abcdef" for c in request["nonce"])):
            return 2
        if "deadline" in request and (type(request["deadline"]) not in {int, float}
                or not math.isfinite(request["deadline"])):
            return 2
    except (ValueError, TypeError, KeyError):
        return 2
    stopped = False

    def stop(_number, _frame):
        nonlocal stopped
        stopped = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    child = None
    deadline = min(started + request["timeout"], request.get("deadline", started + request["timeout"]))
    execution_deadline = deadline - min(2.0, max(0, deadline - started) / 2)
    completed = False
    try:
        if time.monotonic() >= execution_deadline:
            return 124
        if stopped or select.select([channel], [], [], 0)[0]:
            return 130
        child = subprocess.Popen(
            command, cwd=request["cwd"], env=environment, start_new_session=False,
            close_fds=True, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=subprocess.DEVNULL,
        )
        os.set_blocking(child.stdin.fileno(), False)
        pending = memoryview(request["prompt"].encode())
        while True:
            if stopped or time.monotonic() >= execution_deadline:
                return 130 if stopped else 124
            if select.select([channel], [], [], 0)[0]:
                return 130
            code = child.poll()
            if code is not None:
                if stopped or time.monotonic() >= execution_deadline or select.select([channel], [], [], 0)[0]:
                    return 130
                completed = True
                print(json.dumps({"type": "curis.supervisor.result", "nonce": request["nonce"], "returncode": code}),
                      file=sys.stderr, flush=True)
                return int(code)
            readable, writable, _ = select.select(
                [channel], [child.stdin] if pending else [],
                [], min(0.05, max(0, execution_deadline - time.monotonic())),
            )
            if readable:
                return 130
            if writable:
                try:
                    pending = pending[os.write(child.stdin.fileno(), pending[:65536]):]
                except BrokenPipeError:
                    pending = memoryview(b"")
            if not pending and not child.stdin.closed:
                child.stdin.close()
    finally:
        if child is not None:
            if not completed:
                try:
                    if child.poll() is None:
                        child.terminate()
                    try:
                        child_code = child.wait(timeout=min(0.75, max(0, deadline - time.monotonic())))
                    except subprocess.TimeoutExpired:
                        child.kill()  # Only the retained direct child, never a discovered PID.
                        child_code = child.wait(timeout=max(0, deadline - time.monotonic()))
                    print(json.dumps({"type": "curis.supervisor.child_reaped", "nonce": request["nonce"],
                                      "child_pid": child.pid, "returncode": child_code}),
                          file=sys.stderr, flush=True)
                except (OSError, subprocess.SubprocessError):
                    pass
            # The supervisor itself is the live group leader; never signal a stored child PID.
            if os.getpid() == os.getsid(0) == os.getpgrp():
                os.killpg(0, signal.SIGKILL)


class AgentExecutionError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status: str = "failed",
        outbound_attempted: bool = False,
        computer_access: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.http_status = 0
        self.outbound_attempted = outbound_attempted
        self.computer_access = computer_access or {}


class CodexExecutionHeld(AgentExecutionError):
    def __init__(self) -> None:
        super().__init__("真实 Agent 执行暂不可用：停止安全机制尚未验证。",
                         status=CODEX_EXECUTION_HOLD_CODE, outbound_attempted=False)


def require_codex_execution_available() -> None:
    if not CODEX_STOP_VERIFIED:
        raise CodexExecutionHeld()
    with _UNRESOLVED_SUPERVISORS_LOCK:
        if _UNRESOLVED_SUPERVISORS:
            raise AgentExecutionError("先前监督进程状态未确认，不能继续执行。",
                                      status="supervisor_unavailable", outbound_attempted=False)


def require_owned_container_execution_available() -> None:
    if not AGENT_CONTAINER_EXECUTION_VERIFIED:
        raise AgentExecutionError("受控 Agent 容器执行尚未通过验收。",
                                  status="container_execution_held",outbound_attempted=False)


# Independent native isolation, auth and stop evidence is required before release.
ACP_LOCAL_EXECUTION_VERIFIED = False
ACP_SDK_VERSION = "0.12.1"
_UNRESOLVED_ACP_PROCESSES = []


def require_acp_execution_available():
    if not ACP_LOCAL_EXECUTION_VERIFIED or _UNRESOLVED_ACP_PROCESSES:
        raise AgentExecutionError("本机 ACP 执行的隔离、授权及停止尚未验收。",
                                  status="acp_execution_held", outbound_attempted=False)


def _load_acp_sdk():
    try:
        if version("agent-client-protocol") != ACP_SDK_VERSION:
            raise ValueError("unsupported SDK version")
        import acp
        import acp.schema
        return acp
    except (ImportError, PackageNotFoundError, ValueError) as error:
        raise AgentExecutionError("固定版 ACP SDK 尚未准备好。", status="configuration_rejected") from error


class AcpStdioAdapter:
    """One SDK protocol bridge for trusted install-backed stdio Agents, not a scheduler.

    The launcher is host-selected; existing DSH configuration requires explicit consent.
    Native execution stays held until the exact isolation/stop path has real evidence.
    """
    gateway_id = "acp-stdio"
    model_name = "acp-agent"
    MAX_OUTPUT = 1024 * 1024
    MAX_WIRE = 8 * 1024 * 1024

    def __init__(self, *, installation: dict, cwd: str, profile_home: str,
                 shared_account: bool = False, timeout: float = 90, should_stop=lambda: False,
                 before_launch=lambda: None, on_progress=lambda _stage: None,
                 on_local_state=lambda _receipt: None, tool_url: str = "", tool_token: str = ""):
        self.installation = dict(installation)
        self.cwd = str(Path(cwd).resolve())
        self.profile_home = str(Path(profile_home).resolve())
        if type(shared_account) is not bool or (shared_account and installation.get("agent_id") != "deepseek_harness"):
            raise AgentExecutionError("共享账号选择无效。", status="configuration_rejected")
        self.shared_account = shared_account
        self.timeout = float(timeout)
        self.should_stop, self.before_launch = should_stop, before_launch
        self.on_progress, self.on_local_state = on_progress, on_local_state
        self.tool_url, self.tool_token = tool_url, tool_token
        self.cleanup = None
        self._spawn = asyncio.create_subprocess_exec
        self._connect = None  # Test seam; production always uses official SDK stdio.

    def require_closed(self):
        if not self.cleanup or self.cleanup.get("state") != "CLOSED":
            raise AgentExecutionError("ACP 会话或进程退出未确认，外部效果仍未知。",
                                      status="outcome_unknown", outbound_attempted=True)

    def _preflight(self):
        require_acp_execution_available()
        if not 3 <= self.timeout <= 90 or not math.isfinite(self.timeout):
            raise AgentExecutionError("ACP 时限无效。", status="configuration_rejected")
        root, home = Path(self.cwd), Path(self.profile_home)
        if self.shared_account:
            # OS account home only: no tenant-supplied path, inherited DSH_HOME or credential reads.
            try:
                home = Path(pwd.getpwuid(os.getuid()).pw_dir)
                dsh_home = home / ".dsh"
                for directory in (home, dsh_home):
                    info = directory.lstat()
                    if (not directory.is_absolute() or directory.resolve() != directory or not stat.S_ISDIR(info.st_mode)
                            or info.st_uid != os.getuid() or info.st_mode & 0o022):
                        raise ValueError("Unsafe default DSH directory")
            except (OSError, ValueError, KeyError) as error:
                raise AgentExecutionError("默认 DSH 配置目录无法安全核验，请先在 DSH 完成配置。", status="configuration_rejected") from error
            from .ai_capability_registry import acp_installation
            if acp_installation(self.installation.get("agent_id", "")) != self.installation:
                raise AgentExecutionError("ACP 安装已变化，请重新核验。", status="configuration_rejected")
            if not root.is_dir() or self.should_stop():
                raise AgentExecutionError("原工作不可用或已停止。", status="cancelled")
            # DSH owns credential resolution and official profile initialization; Curis never opens them.
            return {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8", "HOME": str(home),
                    "DSH_HOME": str(dsh_home), "TMPDIR": str(root), "NO_PROXY": "127.0.0.1,localhost,::1"}
        if not root.is_dir() or home.parent != root or home.is_symlink() or not home.is_dir():
            raise AgentExecutionError("原工作隔离 ACP 配置目录尚未准备。", status="configuration_rejected")
        profile_relative = self.installation.get("profile_directory", "")
        if not profile_relative or Path(profile_relative).is_absolute() or ".." in Path(profile_relative).parts:
            raise AgentExecutionError("ACP 隔离配置契约无效。", status="configuration_rejected")
        profile = home / profile_relative
        if not profile.is_dir() or profile.resolve() != profile:
            raise AgentExecutionError("ACP 离线配置尚未准备；不会自动安装或使用个人配置。", status="configuration_rejected")
        from .ai_capability_registry import acp_installation
        current = acp_installation(self.installation.get("agent_id", ""))
        if current != self.installation:
            raise AgentExecutionError("ACP 安装已变化，请重新核验。", status="configuration_rejected")
        if self.should_stop():
            raise AgentExecutionError("原工作已停止。", status="cancelled")
        # Do not inherit shell credentials, personal HOME, proxies or runtime injection.
        environment = {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8", "HOME": str(home),
                       "TMPDIR": str(home), "NO_PROXY": "127.0.0.1,localhost,::1"}
        for key, relative in current["profile_environment"].items():
            environment[key] = str(home / relative)
        return environment

    @staticmethod
    def _account_model(config_options):
        rows = [row for row in (config_options or []) if getattr(row, "id", None) == "model"]
        if len(rows) != 1 or getattr(rows[0], "type", None) != "select":
            raise AgentExecutionError("DSH 未提供可确认的账号模型。", status="account_model_unavailable", outbound_attempted=True)
        row = rows[0]
        options = []
        for item in row.options:
            options.extend(item.options if hasattr(item, "options") else [item])
        candidates = []
        for item in options:
            try:
                route = json.loads(item.value)
            except (ValueError, TypeError):
                continue
            if (isinstance(route, list) and len(route) == 2 and route[0] == "deepseek-account"
                    and isinstance(route[1], str) and 0 < len(route[1]) <= 256):
                candidates.append((item.value, route[1]))
        if not candidates or len({value for value, _ in candidates}) != len(candidates):
            raise AgentExecutionError("DSH 账号模型不可用，请先在 DSH 核对登录与额度。", status="account_model_unavailable", outbound_attempted=True)
        chosen = next((item for item in candidates if item[0] == row.current_value), candidates[0])
        return row, chosen

    def execute(self, prompt: str, *, session_id: str = "") -> dict[str, Any]:
        self.cleanup = None
        if session_id or not isinstance(prompt, str) or not prompt or len(prompt.encode()) > self.MAX_OUTPUT:
            raise AgentExecutionError("ACP 仅接受原工作的一次有界新会话。", status="configuration_rejected")
        started = time.monotonic()
        environment = self._preflight()
        sdk = _load_acp_sdk()
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._execute(prompt, environment, sdk, started=started))
        raise AgentExecutionError("ACP 同步入口不能在事件循环内直接调用。", status="configuration_rejected")

    async def _execute(self, prompt, environment, sdk, *, started=None):
        started = time.monotonic() if started is None else started
        deadline = started + self.timeout
        run_deadline = deadline - 2
        process = connection = stderr_task = stdout_task = active_prompt = spawn_task = None
        attempt_nonce = uuid4().hex
        attempted = False
        state = {"session": None, "error": None, "chunks": [], "bytes": 0, "wire": 0, "frames": 0, "account_model": None}
        adapter = self
        schema = sdk.schema

        class Client:
            async def session_update(self, session_id, update, **_kwargs):
                if session_id != state["session"]:
                    state["error"] = "foreign_session"
                    return
                if adapter.shared_account and state["account_model"] and getattr(update, "session_update", "") == "config_option_update":
                    try:
                        row, _chosen = adapter._account_model(update.config_options)
                        if row.current_value != state["account_model"] or _chosen[0] != state["account_model"]:
                            state["error"] = "account_model_changed"
                    except AgentExecutionError:
                        state["error"] = "account_model_changed"
                if getattr(update, "session_update", "") == "agent_message_chunk":
                    content = getattr(update, "content", None)
                    if getattr(content, "type", "") != "text":
                        state["error"] = "unsupported_content"
                        return
                    text = content.text
                    state["bytes"] += len(text.encode())
                    if state["bytes"] > adapter.MAX_OUTPUT:
                        state["error"] = "output_limit"
                        return
                    state["chunks"].append(text)
            async def request_permission(self, session_id, tool_call, options, **_kwargs):
                return schema.RequestPermissionResponse(outcome=schema.DeniedOutcome(outcome="cancelled"))
            async def denied(self, **_kwargs):
                raise sdk.RequestError.method_not_found("Unadvertised client operation")
            read_text_file = write_text_file = create_terminal = terminal_output = denied
            release_terminal = wait_for_terminal_exit = kill_terminal = create_elicitation = denied
            async def complete_elicitation(self, **_kwargs):
                return None
            async def ext_method(self, **_kwargs):
                raise sdk.RequestError.method_not_found("Unsupported extension")
            async def ext_notification(self, **_kwargs):
                state["error"] = "unsupported_extension"

        def observer(event):
            # Bound all frames, including ignored thoughts/tool/config notifications.
            state["frames"] += 1
            state["wire"] += len(json.dumps(event.message, ensure_ascii=False).encode())
            if state["frames"] > 4096 or state["wire"] > adapter.MAX_WIRE:
                state["error"] = "protocol_limit"

        async def watched(awaitable, *, retain=False):
            nonlocal active_prompt
            task = asyncio.ensure_future(awaitable)
            if retain: active_prompt = task
            try:
                while not task.done():
                    if self.should_stop():
                        raise AgentExecutionError("原工作已停止，外部效果仍需核验。", status="outcome_unknown", outbound_attempted=attempted)
                    if state["error"] or time.monotonic() >= run_deadline:
                        raise AgentExecutionError("ACP 协议或时限未通过核验。", status="outcome_unknown", outbound_attempted=attempted)
                    await asyncio.wait({task}, timeout=min(.05, max(0, run_deadline-time.monotonic())))
                if state["error"] or self.should_stop():
                    raise AgentExecutionError("ACP 会话边界失效。", status="outcome_unknown", outbound_attempted=attempted)
                return task.result()
            finally:
                if not task.done() and not retain:
                    task.cancel()
                    with contextlib.suppress(BaseException): await task

        async def drain_stderr():
            size = 0
            while True:
                chunk = await process.stderr.read(4096)
                if not chunk: return
                size += len(chunk)
                if size > 16384: state["error"] = "diagnostic_limit"
                # Never persist raw diagnostics: they can contain provider credentials.

        async def drain_stdout():
            while True:
                chunk = await process.stdout.read(4096)
                if not chunk: return
                state["wire"] += len(chunk)
                if state["wire"] > self.MAX_WIRE:
                    state["error"] = "protocol_limit"

        async def bounded(awaitable, seconds=.35):
            return await asyncio.wait_for(awaitable, timeout=max(.001, min(seconds, deadline-time.monotonic())))

        try:
            with _AGENT_STOP_SPAWN_LOCK:
                require_acp_execution_available()
                if time.monotonic() >= run_deadline:
                    raise AgentExecutionError("ACP 预检超过时限。", status="configuration_rejected")
                self.before_launch()
                if self.should_stop():
                    raise AgentExecutionError("原工作已停止。", status="cancelled")
                attempted = True  # Conservatively uncertain even if OS spawn response is lost.
                spawn_task = asyncio.create_task(self._spawn(*self.installation["command"], cwd=self.cwd,
                    env=environment, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE, start_new_session=True, limit=262144))
                done, _ = await asyncio.wait({spawn_task}, timeout=max(.001, run_deadline-time.monotonic()))
                if not done:
                    raise TimeoutError("ACP spawn response not yet available")
                process = spawn_task.result()
            stderr_task = asyncio.create_task(drain_stderr())
            connection = (self._connect or sdk.connect_to_agent)(Client(), process.stdin, process.stdout,
                                                                  observers=[observer], use_unstable_protocol=True)
            initialized = await watched(connection.initialize(protocol_version=1,
                client_capabilities=schema.ClientCapabilities(),
                client_info=schema.Implementation(name="curis", version="1")))
            if initialized.protocol_version != 1 or initialized.auth_methods:
                raise AgentExecutionError("ACP 版本或认证尚未核验。", status="outcome_unknown", outbound_attempted=True)
            session_capabilities = initialized.agent_capabilities.session_capabilities
            if not session_capabilities or session_capabilities.close is None:
                raise AgentExecutionError("Agent 未声明会话关闭能力。", status="outcome_unknown", outbound_attempted=True)
            servers = []
            if self.tool_url:
                if not initialized.agent_capabilities.mcp_capabilities or not initialized.agent_capabilities.mcp_capabilities.http:
                    raise AgentExecutionError("Agent 不支持原工作的受控 HTTP MCP。", status="outcome_unknown", outbound_attempted=True)
                from urllib.parse import urlparse
                target = urlparse(self.tool_url)
                if (target.scheme != "http" or target.hostname != "127.0.0.1" or not target.port
                        or target.path != "/api/workspace/agent-tools" or target.query or target.fragment
                        or target.username or target.password or not self.tool_token):
                    raise AgentExecutionError("原工作工具通道无效。", status="configuration_rejected", outbound_attempted=True)
                servers = [schema.HttpMcpServer(type="http", name="curis", url=self.tool_url,
                    headers=[schema.HttpHeader(name="Authorization", value="Bearer " + self.tool_token)])]
            session = await watched(connection.new_session(cwd=self.cwd, mcp_servers=servers))
            if not isinstance(session.session_id, str) or not session.session_id or len(session.session_id) > 256:
                raise AgentExecutionError("ACP 会话标识无效。", status="outcome_unknown", outbound_attempted=True)
            state["session"] = session.session_id
            if self.shared_account:
                row, (chosen, account_model) = self._account_model(session.config_options)
                selected = await watched(connection.set_config_option(config_id=row.id,
                    session_id=state["session"], value=chosen))
                confirmed, (confirmed_value, _) = self._account_model(selected.config_options)
                if confirmed.current_value != chosen or confirmed_value != chosen:
                    raise AgentExecutionError("DSH 未确认所选账号模型；未发送任务。", status="account_model_unconfirmed", outbound_attempted=True)
                state["account_model"] = chosen
                self.on_progress("acp.account_model.confirmed")
            self.on_progress("acp.session.started")
            response = await watched(connection.prompt(session_id=state["session"], prompt=[sdk.text_block(prompt)]), retain=True)
            if response.stop_reason != "end_turn" or not state["chunks"]:
                raise AgentExecutionError("ACP 回合未正常完成。", status="outcome_unknown", outbound_attempted=True)
            usage = getattr(response, "usage", None)
            result = {"output": "".join(state["chunks"]), "session_id": state["session"],
                "model_gateway_id": self.gateway_id, "model_name": self.model_name,
                "provider_id": "acp-stdio", "prompt_tokens": getattr(usage, "input_tokens", None),
                "completion_tokens": getattr(usage, "output_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
                "usage_basis": "PROVIDER_REPORTED" if usage is not None else "UNKNOWN",
                "status": "success", "http_status": 0, "outbound_attempted": True,
                "latency_ms": round((time.monotonic()-started)*1000), "artifacts": []}
            if self.shared_account:
                result.update(model_name=account_model, agent_account_provider="deepseek-account",
                    account_model_confirmed=True, shared_configuration=True)
        except AgentExecutionError:
            raise
        except Exception as error:
            raise AgentExecutionError("ACP 连接或结果未确认。", status="outcome_unknown" if attempted else "configuration_rejected",
                                      outbound_attempted=attempted) from error
        finally:
            # A timed-out spawn may still return a real child. Never cancel it or guess a PID.
            if process is None and spawn_task is not None:
                if not spawn_task.done():
                    await asyncio.wait({spawn_task}, timeout=max(0, deadline-time.monotonic()-1))
                if spawn_task.done() and not spawn_task.cancelled():
                    with contextlib.suppress(Exception):
                        process = spawn_task.result()
            closed_session = False
            terminal_observed = bool(active_prompt and active_prompt.done() and not active_prompt.cancelled() and active_prompt.exception() is None)
            if connection and state["session"]:
                if 'result' not in locals():
                    with contextlib.suppress(Exception): await bounded(connection.cancel(session_id=state["session"]))
                    if active_prompt:
                        try:
                            await bounded(asyncio.shield(active_prompt))
                            terminal_observed = True
                        except Exception: pass
                try:
                    await bounded(connection.close_session(session_id=state["session"]))
                    closed_session = True
                except Exception: pass
            if connection:
                with contextlib.suppress(Exception): await bounded(connection.close())
            if active_prompt and not active_prompt.done():
                active_prompt.cancel()
                with contextlib.suppress(BaseException): await active_prompt
            if process:
                if stderr_task is None:
                    stderr_task = asyncio.create_task(drain_stderr())
                if process.stdin: process.stdin.close()
                stdout_task = asyncio.create_task(drain_stdout())
                try:
                    await bounded(process.wait(), .4)
                except Exception:
                    # Signal only a group whose original direct child is still live.
                    # Escaped descendants/OS effects cannot be inferred from parent exit.
                    for sig in (signal.SIGTERM, signal.SIGKILL):
                        if process.returncode is not None: break
                        try:
                            if os.getpgid(process.pid) != process.pid: break
                            os.killpg(process.pid, sig)
                        except ProcessLookupError: break
                        except OSError: break
                        with contextlib.suppress(Exception): await bounded(process.wait(), .4)
                if stderr_task:
                    with contextlib.suppress(Exception): await bounded(asyncio.shield(stderr_task), .2)
                with contextlib.suppress(Exception): await bounded(asyncio.shield(stdout_task), .2)
                # Neither closing SDK streams nor parent exit alone proves EOF.
                stdout_eof = bool(stdout_task.done() and not stdout_task.cancelled() and stdout_task.exception() is None and process.stdout.at_eof())
                stderr_eof = bool(stderr_task and stderr_task.done() and not stderr_task.cancelled()
                                  and stderr_task.exception() is None)
                group_absent = False
                if process.returncode is not None:
                    try: os.killpg(process.pid, 0)
                    except ProcessLookupError: group_absent = True
                    except OSError: pass
                self.cleanup = {"state": "CLOSED" if closed_session and terminal_observed and process.returncode == 0 and stdout_eof and stderr_eof and group_absent and not state["error"] else "UNKNOWN",
                    "session_closed": closed_session, "terminal_observed": terminal_observed, "scope": "OWNED_PROCESS_GROUP", "escaped_descendants": "UNKNOWN", "parent_returncode": process.returncode,
                    "stdout_eof": stdout_eof, "stderr_eof": stderr_eof, "group_absent": group_absent,
                    "external_effects": "UNKNOWN"}
                if process.returncode is None or not group_absent or not stdout_eof or not stderr_eof:
                    _UNRESOLVED_ACP_PROCESSES.append(process)
                else:
                    self.on_local_state({"child_pid": process.pid, "returncode": process.returncode,
                        "attempt_sha256": hashlib.sha256(attempt_nonce.encode()).hexdigest()})
                for task in (stderr_task, stdout_task):
                    if task and not task.done():
                        task.cancel()
                        with contextlib.suppress(BaseException): await task
            else:
                if attempted: _UNRESOLVED_ACP_PROCESSES.append({"state": "SPAWN_UNKNOWN", "attempt_sha256": hashlib.sha256(attempt_nonce.encode()).hexdigest()})
                self.cleanup = {"state": "UNKNOWN" if attempted else "NOT_STARTED", "external_effects": "UNKNOWN"}
        self.require_closed()
        if self.should_stop():
            raise AgentExecutionError("原工作授权已失效，外部效果仍未知。", status="outcome_unknown", outbound_attempted=True)
        result["acp_cleanup"] = dict(self.cleanup)
        self.on_progress("acp.session.closed")
        return result


class CodexCliAdapter:
    """Official local Codex CLI adapter using the stable JSONL exec surface."""

    gateway_id = "codex-local-agent"
    model_name = "codex-cli"
    _INTENTS = {
        "ASK_WHEN_NEEDED": "read-only",
        "AUTO_WITHIN_BOUNDARY": "workspace-write",
        "REQUEST_WIDEST_NATIVE_ACCESS": None,
    }

    def __init__(
        self,
        *,
        cwd: str,
        sandbox: str | None = None,
        requested_intent: str = "",
        timeout: int = 300,
        executable: str | None = None,
        runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
        environment: dict[str, str] | None = None,
        should_stop: Callable[[], bool] | None = None,
        on_progress: Callable[[str], None] | None = None,
        before_launch: Callable[[], None] | None = None,
        on_local_state: Callable[[dict[str, Any]], None] | None = None,
        supervisor_command: list[str] | None = None,
        tool_url: str | None = None,
        container_session_factory=None,
    ) -> None:
        self.cwd = str(Path(cwd).resolve())
        self.requested_intent, self.sandbox = self._resolve_access_request(
            requested_intent=requested_intent,
            sandbox=sandbox,
        )
        self.timeout = timeout
        pinned_executable = os.environ.get("CURIS_CODEX_EXECUTABLE", "")
        if executable and pinned_executable and Path(executable).resolve() != Path(pinned_executable).resolve():
            raise AgentExecutionError("Native executable differs from the managed installation", status="configuration_rejected")
        self.executable = executable or pinned_executable or ""
        self.managed_executable = str(Path(pinned_executable).resolve()) if pinned_executable else ""
        self.native_model = os.environ.get("CURIS_CODEX_MODEL") or "gpt-5.6-sol"
        self.runner = runner
        self.environment = environment
        self.should_stop = should_stop or (lambda: False)
        self.on_progress = on_progress or (lambda event: None)
        self.before_launch = before_launch or (lambda: None)
        self.on_local_state = on_local_state or (lambda _evidence: None)
        self.supervisor_command = supervisor_command
        self.tool_url = tool_url
        self.container_session_factory = container_session_factory
        self.container_stop_receipt = None
        self.on_container_state = lambda _receipt: None
        self.installation_baseline = None
        self.native_model_profile = None

    def execute(self, prompt: str, *, session_id: str = "") -> dict[str, Any]:
        is_resume = bool(session_id)
        if self.requested_intent == "REQUEST_WIDEST_NATIVE_ACCESS":
            snapshot = self._access_snapshot(session_id=session_id, is_resume=is_resume, command_accepted=False)
            raise AgentExecutionError(
                "Codex CLI adapter does not support Full Computer Access",
                status="unsupported",
                computer_access=snapshot,
            )
        if self.runner is None:
            require_codex_execution_available()
        owned_linux=self.runner is None
        if owned_linux:
            require_owned_container_execution_available()
            if is_resume or not callable(self.container_session_factory):
                raise AgentExecutionError("原工作容器或续作边界尚未核验。",status="container_execution_held")
            from .reader_vm_host import load_owned_linux_profile
            linux_profile=load_owned_linux_profile()
            if self.native_model!="gpt-5.6-sol":
                raise AgentExecutionError("该 Linux 模型配置尚未核验。",status="configuration_rejected")
            from .agent_work_resources import scoped_codex_model_catalog
            _,self.native_model_profile=scoped_codex_model_catalog(linux_profile["modelCatalog"],self.native_model)
            self.native_model_profile.update(runtime="LINUX_OWNED_CONTAINER",
                tool_surface_basis="PINNED_LINUX_PROFILE_NOT_PER_TURN_TOOL_OBSERVATION",
                network_boundary={"purpose":linux_profile["egressPurpose"],"verification_state":"UNVERIFIED"})
            command=["/opt/curis/bin/codex","exec"]
        else:
            if not self.executable:
                self.executable = local_codex_executable()
            if not self.executable:
                raise AgentExecutionError("Codex CLI is not detected", status="unavailable")
            if not Path(self.cwd).is_dir():
                raise AgentExecutionError("Codex working directory is unavailable", status="configuration_rejected")
            if is_resume and self.runner is None:
                raise AgentExecutionError("Resume access cannot be verified; continue through the original Work with fresh authorization",
                    status="configuration_rejected", computer_access=self._access_snapshot(
                        session_id=session_id, is_resume=True, command_accepted=False))
            command = [self.executable, "exec"]
            if is_resume:
                command += ["resume", "--json", "--skip-git-repo-check", session_id, "-"]
            else:
                command += [
                    "--json",
                    "--sandbox",
                    self.sandbox,
                    "--cd",
                    self.cwd,
                    "--skip-git-repo-check",
                    "-",
                ]
                if self.environment is not None:
                    # Explicit per-invocation settings; never alter the user's native profile.
                    temporary = Path(self.environment.get("TMPDIR") or (Path(self.cwd) / "tmp"))
                    command[2:2] = ["--ignore-user-config", "--ephemeral",
                        "-c", "sqlite_home=" + json.dumps(str(temporary)),
                        "-c", 'history.persistence="none"',
                        "-c", "project_doc_max_bytes=0", "-c", "skills.include_instructions=false",
                        "-c", "skills.bundled.enabled=false", "-c", "features.plugins=false",
                        "-c", "features.apps=false", "-c", "features.memories=false"]
            if self.tool_url:
                from urllib.parse import urlsplit
                target = urlsplit(self.tool_url)
                if (target.scheme != "http" or target.hostname != "127.0.0.1" or not target.port
                        or target.path != "/api/workspace/agent-tools" or target.query or target.fragment or target.username):
                    raise AgentExecutionError("原工作工具端点不合法", status="configuration_rejected")
                settings = {"url": self.tool_url, "bearer_token_env_var": "CURIS_AGENT_TOOL_TOKEN",
                    "required": True, "startup_timeout_sec": 10, "tool_timeout_sec": 15}
                inline = ", ".join(f"{key} = {json.dumps(value)}" for key, value in settings.items())
                command[2:2] = ["-c", "mcp_servers={curis={" + inline + "}}", "-c", 'web_search="disabled"',
                    "-c", "features.shell_tool=false", "-c", "features.shell_snapshot=false",
                    "-c", "features.image_generation=false", "-c", "features.apply_patch_freeform=false",
                    "-c", "features.multi_agent=false", "-c", "features.multi_agent_v2=false", "-c", "features.hooks=false",
                    "-c", "tools.experimental_request_user_input.enabled=false",
                    "-c", "features.skill_mcp_dependency_install=false", "--strict-config", "--ignore-rules"]
                # Only the host's three reviewed, scoped tool names receive approval.
                # Unknown future tools retain the SDK's default approval behavior.
                approvals = []
                for name in ("read_skill", "write_output", "browser"):
                    approvals += ["-c", f'mcp_servers.curis.tools.{name}.approval_mode="approve"']
                table_end = command.index("mcp_servers={curis={" + inline + "}}") + 1
                command[table_end:table_end] = approvals
                catalog = self._prepare_model_profile()
                command[0] = self.executable
                command[2:2] = ["--model", self.native_model, "-c", "model_catalog_json=" + json.dumps(str(catalog))]
                generation_profile = self._native_file_profile()
                if self.native_model_profile is not None:
                    self.native_model_profile["generation_profile_sha256"] = hashlib.sha256(generation_profile.read_bytes()).hexdigest()
                command = ["/usr/bin/sandbox-exec", "-f", str(generation_profile), *command]
        started = time.monotonic()
        try:
            if owned_linux:
                completed=self._run_linux_container_candidate(prompt,linux_profile["modelCatalog"],timeout=self.timeout)
            else:
                completed = (self.runner or self._run_process)(
                    command,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
        except subprocess.TimeoutExpired as error:
            raise AgentExecutionError("Codex execution timed out", status="timed_out", outbound_attempted=True) from error
        finally:
            if self.installation_baseline is not None:
                self._verify_installation(outbound_attempted=True)
        if completed.returncode != 0:
            raise AgentExecutionError("Codex execution failed", outbound_attempted=True)
        parsed = self._parse_jsonl(completed.stdout)
        if not parsed["output"]:
            raise AgentExecutionError("Codex returned no final output", status="response_invalid", outbound_attempted=True)
        usage = parsed["usage"]
        resolved_session_id = parsed["session_id"] or session_id
        computer_access = self._access_snapshot(
            session_id=resolved_session_id,
            is_resume=is_resume,
            command_accepted=True,
        )
        if owned_linux:
            computer_access["native_mapping"].update(sandbox="read-only",approval="EXPLICIT_CURIS_STDIO_TOOLS_ONLY")
        return {
            "output": parsed["output"],
            "cost": 0,
            "estimated_cost": 0,
            "ledger_cost_source": "unknown",
            "metering_status": "confirmed" if usage.get("input_tokens") is not None else "unknown",
            "model_gateway_id": self.gateway_id,
            "model_name": self.model_name,
            "provider_id": "openai_codex",
            "prompt_tokens": usage.get("input_tokens"),
            "completion_tokens": usage.get("output_tokens"),
            "total_tokens": (usage.get("input_tokens") or 0) + (usage.get("output_tokens") or 0),
            "status": "success",
            "http_status": 200,
            "latency_ms": round((time.monotonic() - started) * 1000),
            "outbound_attempted": True,
            "session_id": resolved_session_id,
            "progress": parsed["progress"],
            "artifacts": parsed["artifacts"],
            "permissions": self._permissions_projection(computer_access),
            "computer_access": computer_access,
            "resume_supported": False,
            "cancel_supported": self.runner is None,
            "native_model_profile": self.native_model_profile,
        }

    def _verify_installation(self, *, outbound_attempted):
        try:
            unchanged = installation_id_snapshot(Path.home() / ".codex" / "installation_id") == self.installation_baseline
        except (OSError, ValueError):
            unchanged = False
        if not unchanged:
            raise AgentExecutionError("Native installation metadata changed; execution effects require verification",
                status="response_invalid", outbound_attempted=outbound_attempted)

    def _prepare_model_profile(self) -> Path:
        from .agent_work_resources import scoped_codex_model_catalog
        try:
            executable = Path(self.executable).resolve(strict=True)
            native_hash = hashlib.sha256(executable.read_bytes()).hexdigest()
        except OSError as error:
            raise AgentExecutionError("Native installation could not be verified before execution",
                status="configuration_rejected", outbound_attempted=False) from error
        if native_hash != PROVED_CODEX_SHA256:
            raise AgentExecutionError("This Native installation has not passed the bounded tool-surface check",
                status="configuration_rejected")
        self.executable = str(executable)
        temporary = Path((self.environment or {}).get("TMPDIR", ""))
        if not temporary.is_absolute() or not temporary.is_dir() or self.supervisor_command is None:
            raise AgentExecutionError("Scoped temporary storage and supervisor are required", status="configuration_rejected")
        profile = self._native_file_profile(metadata_only=True)
        # This independent supervisor never invokes the generation reservation callback.
        probe = CodexCliAdapter(cwd=str(temporary), executable=self.executable, timeout=8,
            environment={key: value for key, value in self.environment.items() if key != "CURIS_AGENT_TOOL_TOKEN"},
            should_stop=self.should_stop, supervisor_command=self.supervisor_command)
        try:
            completed = probe._run_process(["/usr/bin/sandbox-exec", "-f", str(profile),
                self.executable, "debug", "models", "--bundled"], input="", timeout=8)
            if completed.returncode != 0:
                raise ValueError("Native bundled metadata unavailable")
            catalog, receipt = scoped_codex_model_catalog(json.loads(completed.stdout), self.native_model)
            encoded = (json.dumps(catalog, ensure_ascii=False) + "\n").encode()
            path = temporary / "scoped-public-model-catalog.json"
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
            with os.fdopen(descriptor, "wb") as handle:
                os.fchmod(handle.fileno(), 0o400)
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            self.native_model_profile = {**receipt, "native_executable": self.executable,
                "native_executable_sha256": native_hash, "catalog_sha256": hashlib.sha256(encoded).hexdigest(),
                "installation_selection": "MANAGED_EXACT_PATH" if self.managed_executable else "DISCOVERED_HASH_VERIFIED",
                "managed_executable": self.managed_executable or None,
                "metadata_profile_sha256": hashlib.sha256(profile.read_bytes()).hexdigest(),
                "catalog_mode": "0400", "model": self.native_model, "metadata_network": "OS_DENIED",
                "metadata_seconds_limit": 8, "generation_allowance_reserved_by_metadata": False}
            self.native_model_profile["network_boundary"] = {
                "native_provider_services": "INFERENCE_AND_AUTHENTICATION",
                "os_destination_allowlist": False,
                "model_web_access": "SCOPED_CURIS_BROWSER_TOOL",
                "browser_destinations": "EXPLICIT_HOSTS_PUBLIC_IPS_VERIFIED_TLS"}
            return path
        except (ValueError, OSError, AgentExecutionError, subprocess.SubprocessError) as error:
            raise AgentExecutionError("Native model boundary could not be verified before execution",
                status="configuration_rejected", outbound_attempted=False) from error
        finally:
            self._verify_installation(outbound_attempted=False)

    def _native_file_profile(self, *, metadata_only=False) -> Path:
        root = Path(self.cwd).absolute()
        try:
            executable = Path(self.executable).resolve(strict=True)
        except OSError as error:
            raise AgentExecutionError("Native installation disappeared before execution", status="configuration_rejected") from error
        runtime = executable.parents[1]
        if runtime.name != "0.144.6-aarch64-apple-darwin" or executable.parent.name != "bin":
            raise AgentExecutionError("Native installation directory has not been verified", status="configuration_rejected")
        temporary = Path((self.environment or {}).get("TMPDIR") or root / "tmp").absolute()
        auth = Path.home() / ".codex" / "auth.json"
        cache = Path.home() / ".codex" / "models_cache.json"
        installation = Path.home() / ".codex" / "installation_id"
        try:
            snapshot = installation_id_snapshot(installation)
            if self.installation_baseline is not None and self.installation_baseline != snapshot:
                raise ValueError("Native metadata changed between setup stages")
            self.installation_baseline = snapshot
        except (OSError, ValueError) as error:
            raise AgentExecutionError("Existing Native installation metadata could not be verified",
                status="configuration_rejected") from error
        def quoted(value):
            return json.dumps(str(value))
        policy = "\n".join([
            "(version 1)", "(allow default)", "(deny file-read-data)",
            "(allow file-read-data (literal \"/\") (subpath \"/System\") (subpath \"/usr\") (subpath \"/bin\") (subpath \"/sbin\")",
            "  (literal " + quoted(executable) + ")",
            "  (subpath " + quoted(runtime) + ")",
            "" if metadata_only else "  (subpath " + quoted(root) + ")",
            "  (subpath " + quoted(temporary) + ")",
            "" if metadata_only else "  (literal " + quoted(auth) + ") (literal " + quoted(cache) + ")",
            "  (literal " + quoted(installation) + ")",
            "  (literal \"/dev/null\") (literal \"/dev/urandom\") (literal \"/dev/random\"))",
            "(deny file-write*)",
            "(allow file-write* (subpath " + quoted(temporary) + ") (literal \"/dev/null\"))",
            "(allow file-write-data (literal " + quoted(installation) + "))",
            "(deny network*)" if metadata_only else "",
        ]) + "\n"
        path = temporary / "native-metadata.sb" if metadata_only else root / "native-agent.sb"
        try:
            with path.open("x", encoding="utf-8") as handle:
                handle.write(policy)
            path.chmod(0o400)
        except OSError as error:
            raise AgentExecutionError("Native isolation profile could not be prepared", status="configuration_rejected") from error
        return path

    def _run_process(self, command, *, input, timeout, **kwargs):
        require_codex_execution_available()
        if not _SUPERVISOR_ADMISSION.acquire(blocking=False):
            raise AgentExecutionError("已有监督进程正在处理，不能重复启动。",
                                      status="supervisor_unavailable", outbound_attempted=False)
        try:
            # Check again under process-local admission before allocating a child.
            require_codex_execution_available()
            require_owned_container_execution_available()
            if not callable(self.container_session_factory):
                raise AgentExecutionError("没有绑定原工作的受控容器。",status="container_execution_held")
            return self._run_container_process_candidate(command, input=input, timeout=timeout)
        finally:
            _SUPERVISOR_ADMISSION.release()

    def require_owned_container_closed(self):
        receipt=self.container_stop_receipt
        if (type(receipt) is not dict or receipt.get("ledger_state")!="CLOSED_VERIFIED"
                or type(receipt.get("exit_codes")) is not dict
                or set(receipt["exit_codes"])!=set(filter(None,(receipt.get("container_id"),receipt.get("proxy_id"))))
                or any(type(v) is not int for v in receipt["exit_codes"].values())):
            raise AgentExecutionError("原工作容器退出尚未核验；结果未接受。",status="outcome_unknown")

    def _run_container_process_candidate(self, command, *, input, timeout):
        """Private CPU-fixture path; public calls still require both release gates."""
        from .reader_vm_host import OwnedAgentContainerError, _validate_agent_candidate_request
        if not callable(self.container_session_factory):
            raise AgentExecutionError("缺少原工作容器。",status="configuration_rejected")
        if self.should_stop():raise AgentExecutionError("启动前已停止。",status="cancelled")
        try:_validate_agent_candidate_request(command,input,min(timeout,80),self.should_stop)
        except (ValueError,TypeError,PermissionError) as error:
            raise AgentExecutionError("容器候选只允许已限定的无 Provider 输入。",status="configuration_rejected") from error
        self.container_stop_receipt=None
        self.before_launch()
        if self.should_stop():raise AgentExecutionError("授权已撤回，未分配容器。",status="cancelled")
        session=self.container_session_factory()
        try:
            value=session.run(command,input=input,timeout=min(timeout,80),should_stop=self.should_stop)
        except OwnedAgentContainerError as error:
            rejected=AgentExecutionError("执行已停止或未能核验；远端效果保持 UNKNOWN。",
                status={"cancelled":"cancelled","timeout":"timeout","eof":"channel_closed"}.get(error.reason,"outcome_unknown"),
                outbound_attempted=False)
            rejected.container_stop_receipt=error.receipt
            raise rejected from error
        finally:
            self.container_stop_receipt=session.stop_receipt
            if self.container_stop_receipt is not None:self.on_container_state(self.container_stop_receipt)
        self.require_owned_container_closed()
        if self.should_stop():raise AgentExecutionError("停止后结果未接受。",status="cancelled")
        return subprocess.CompletedProcess(command,value["returncode"],value["stdout"],value["stderr"])

    def _run_linux_container_candidate(self, prompt, public_catalog, *, timeout, on_device_login=None):
        """Private Linux path; it never imports or copies the native auth cache."""
        from .reader_vm_host import OwnedAgentContainerError, _validate_agent_candidate_request
        from .agent_work_resources import scoped_codex_model_catalog
        _validate_agent_candidate_request(["/usr/bin/python3","-I","-B","-c","pass"],prompt,min(timeout,80),self.should_stop)
        scoped_codex_model_catalog(public_catalog,"gpt-5.6-sol")
        if self.should_stop() or not callable(self.container_session_factory):
            raise AgentExecutionError("原工作已停止或缺少容器。",status="configuration_rejected")
        self.container_stop_receipt=None
        session=self.container_session_factory()
        reservation=[False]
        def reserve_after_authentication():
            reservation[0]=True
            self.before_launch()
        try:
            value=session.run_linux_candidate(prompt,public_catalog,timeout=min(timeout,80),
                should_stop=self.should_stop,before_launch=reserve_after_authentication,on_device_login=on_device_login)
        except OwnedAgentContainerError as error:
            rejected=AgentExecutionError("Linux Agent 尚未就绪或结果无法核验。",status={
                "authentication_required":"authentication_required","cancelled":"cancelled",
                "timeout":"timeout","eof":"channel_closed"}.get(error.reason,"outcome_unknown"),
                outbound_attempted=reservation[0])
            rejected.container_stop_receipt=error.receipt
            raise rejected from error
        finally:
            self.container_stop_receipt=session.stop_receipt
            if self.container_stop_receipt is not None:self.on_container_state(self.container_stop_receipt)
        self.require_owned_container_closed()
        if self.should_stop():raise AgentExecutionError("停止后结果未接受。",status="cancelled")
        return subprocess.CompletedProcess(["/opt/curis/bin/codex"],value["returncode"],value["stdout"],value["stderr"])

    def _run_process_candidate(self, command, *, input, timeout, **_kwargs):
        """Unreleased parent protocol; real execution remains held."""
        if self.environment is None or self.supervisor_command is None:
            raise AgentExecutionError("缺少已验证的执行监督器", status="configuration_rejected")
        if self.should_stop():
            raise AgentExecutionError("启动前已请求停止", status="cancelled")
        started = time.monotonic()
        budget = min(timeout, 90)
        deadline = started + budget
        execution_deadline = deadline - min(2.0, budget / 2)
        nonce = os.urandom(16).hex()
        payload = (json.dumps({"command": command, "cwd": self.cwd, "environment": self.environment,
            "prompt": input, "timeout": budget, "nonce": nonce, "deadline": deadline}) + "\n").encode("utf-8")
        self.before_launch()
        with _AGENT_STOP_SPAWN_LOCK:
            if self.should_stop():
                raise AgentExecutionError("已请求停止；调用占用需核验，未启动执行进程。",
                    status="cancelled", outbound_attempted=False)
            if time.monotonic() >= execution_deadline:
                raise AgentExecutionError("启动期限已过；调用占用需核验，未启动执行进程。",
                    status="cancelled", outbound_attempted=False)
            try:
                process = subprocess.Popen(self.supervisor_command, cwd=self.cwd, env=self.environment,
                    start_new_session=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            except (OSError, subprocess.SubprocessError) as error:
                raise AgentExecutionError("执行状态未确认，请核对后再继续",
                    status="outcome_unknown", outbound_attempted=True) from error
            # Retain the child before stop can observe a successful spawn.
            with _UNRESOLVED_SUPERVISORS_LOCK:
                _UNRESOLVED_SUPERVISORS.append(process)
        selector = None
        output, diagnostic, line = bytearray(), bytearray(), bytearray()
        stderr_eof = False
        pending = memoryview(payload)
        completed = None
        def request_owned_stop():
            # Signal only the retained Popen child, never a saved PID or group
            # number. Delivery cannot prove that descendants or effects stopped.
            if process.poll() is None:
                process.terminate()
        try:
            selector = selectors.DefaultSelector()
            for pipe in (process.stdin, process.stdout, process.stderr):
                os.set_blocking(pipe.fileno(), False)
            selector.register(process.stdin, selectors.EVENT_WRITE)
            selector.register(process.stdout, selectors.EVENT_READ)
            selector.register(process.stderr, selectors.EVENT_READ)
            while selector.get_map():
                if self.should_stop():
                    raise AgentExecutionError("已请求停止，进程与执行效果仍需核验",
                        status="outcome_unknown", outbound_attempted=True)
                if time.monotonic() >= execution_deadline:
                    raise AgentExecutionError("执行超时，执行效果仍需核验",
                        status="outcome_unknown", outbound_attempted=True)
                for key, _mask in selector.select(0.1):
                    pipe = key.fileobj
                    if pipe is process.stdin:
                        try:
                            pending = pending[os.write(pipe.fileno(), pending[:65536]):]
                        except BrokenPipeError:
                            pending = memoryview(b"")
                        if not pending:
                            selector.unregister(pipe)
                        continue
                    chunk = os.read(pipe.fileno(), 65536)
                    if not chunk:
                        if pipe is process.stderr:
                            stderr_eof = True
                        selector.unregister(pipe)
                        continue
                    if pipe is process.stderr:
                        diagnostic.extend(chunk)
                        if len(diagnostic) > 16384:
                            raise AgentExecutionError("监督状态无效，执行效果仍需核验",
                                status="outcome_unknown", outbound_attempted=True)
                        continue
                    output.extend(chunk)
                    if len(output) > 8 * 1024 * 1024:
                        raise AgentExecutionError("执行输出超出限制，效果仍需核验",
                            status="outcome_unknown", outbound_attempted=True)
                    line.extend(chunk)
                    while b"\n" in line:
                        raw, _, rest = line.partition(b"\n")
                        line = bytearray(rest)
                        try:
                            event = json.loads(raw)
                        except (ValueError, UnicodeError):
                            continue
                        kind = event.get("type") if isinstance(event, dict) else None
                        if kind in {"thread.started", "turn.started", "item.started", "item.completed", "turn.completed", "turn.failed"}:
                            self.on_progress(kind)
            remaining = max(0.0, execution_deadline - time.monotonic())
            process.wait(timeout=remaining)
            if self.should_stop():
                raise AgentExecutionError("已请求停止，进程与执行效果仍需核验",
                    status="outcome_unknown", outbound_attempted=True)
            try:
                records = diagnostic.splitlines()
                marker = json.loads(records[0]) if len(records) == 1 else None
                if (not isinstance(marker, dict) or set(marker) != {"type", "nonce", "returncode"}
                        or marker["type"] != "curis.supervisor.result" or marker["nonce"] != nonce
                        or type(marker["returncode"]) is not int or process.returncode != -signal.SIGKILL):
                    raise ValueError("unverified supervisor result")
                output_text = output.decode("utf-8")
            except (ValueError, UnicodeError, KeyError, TypeError) as error:
                raise AgentExecutionError("监督状态未确认，执行效果仍需核验",
                    status="outcome_unknown", outbound_attempted=True) from error
            if self.should_stop():
                raise AgentExecutionError("已请求停止，进程与执行效果仍需核验",
                    status="outcome_unknown", outbound_attempted=True)
            # A marker and SIGKILL alone cannot release this path. The gate
            # remains closed until owned-process cleanup has real evidence.
            if not CODEX_STOP_VERIFIED:
                raise AgentExecutionError("执行结果已返回，但停止状态未确认；外部效果仍需核验。",
                    status="outcome_unknown", outbound_attempted=True)
            completed = subprocess.CompletedProcess(command, marker["returncode"], output_text, "")
        except AgentExecutionError:
            raise
        except Exception as error:
            raise AgentExecutionError("监督状态未确认，执行效果仍需核验",
                status="outcome_unknown", outbound_attempted=True) from error
        finally:
            cleanup_failed = False
            cleanup_interruption = None
            def cleanup_error(error):
                nonlocal cleanup_failed, cleanup_interruption
                cleanup_failed = True
                if not isinstance(error, Exception) and cleanup_interruption is None:
                    cleanup_interruption = error
            # All failure paths use the same owned wait and attempt-bound receipt.
            try:
                try:
                    if process.returncode is None:
                        request_owned_stop()
                except BaseException as error:
                    cleanup_error(error)
                if process.stdin and not process.stdin.closed:
                    try:
                        process.stdin.close()
                    except BaseException as error:
                        cleanup_error(error)
                try:
                    if process.returncode is None:
                        process.wait(timeout=min(2.0, max(0.0, deadline - time.monotonic())))
                except BaseException as error:
                    cleanup_error(error)
                try:
                    if completed is None and process.stderr is not None and not process.stderr.closed:
                        while not stderr_eof and len(diagnostic) <= 4096:
                            try:
                                chunk = os.read(process.stderr.fileno(), 4097 - len(diagnostic))
                            except BlockingIOError:
                                break
                            if not chunk:
                                break
                            diagnostic.extend(chunk)
                        evidence = _verified_child_exit_receipt(bytes(diagnostic), nonce, process.returncode)
                        if evidence is not None:
                            self.on_local_state(evidence)
                except BaseException as error:
                    cleanup_error(error)
            finally:
                if selector is not None:
                    try:
                        selector.close()
                    except BaseException as error:
                        cleanup_error(error)
                for pipe in (process.stdin, process.stdout, process.stderr):
                    if pipe and not pipe.closed:
                        try:
                            pipe.close()
                        except BaseException as error:
                            cleanup_error(error)
            if cleanup_interruption is not None:
                raise cleanup_interruption
            if process.returncode is None or cleanup_failed:
                raise AgentExecutionError("监督通道关闭未确认，执行效果仍需核验",
                    status="outcome_unknown", outbound_attempted=True)
            with _UNRESOLVED_SUPERVISORS_LOCK:
                _UNRESOLVED_SUPERVISORS.remove(process)
        try:
            if self.should_stop() or not CODEX_STOP_VERIFIED:
                raise AgentExecutionError("执行后许可或停止状态未确认，效果仍需核验。",
                    status="outcome_unknown", outbound_attempted=True)
        except AgentExecutionError:
            raise
        except Exception as error:
            raise AgentExecutionError("执行后许可状态未确认，效果仍需核验。",
                status="outcome_unknown", outbound_attempted=True) from error
        return completed

    @classmethod
    def _resolve_access_request(cls, *, requested_intent: str, sandbox: str | None) -> tuple[str, str]:
        if sandbox is not None and sandbox not in {"read-only", "workspace-write"}:
            raise ValueError("Codex sandbox must be read-only or workspace-write")
        if not requested_intent:
            selected_sandbox = sandbox or "read-only"
            return (
                "ASK_WHEN_NEEDED" if selected_sandbox == "read-only" else "AUTO_WITHIN_BOUNDARY",
                selected_sandbox,
            )
        if requested_intent not in cls._INTENTS:
            raise ValueError("unsupported Codex computer access intent")
        mapped_sandbox = cls._INTENTS[requested_intent]
        if mapped_sandbox and sandbox and sandbox != mapped_sandbox:
            raise ValueError("Codex sandbox conflicts with requested computer access intent")
        return requested_intent, mapped_sandbox or ""

    def _access_snapshot(
        self,
        *,
        session_id: str,
        is_resume: bool,
        command_accepted: bool,
    ) -> dict[str, Any]:
        observed_at = datetime.now(timezone.utc).isoformat()
        if self.requested_intent == "REQUEST_WIDEST_NATIVE_ACCESS":
            return {
                "requested_intent": self.requested_intent,
                "native_mapping": {
                    "provider": "codex_cli",
                    "operation": "resume" if is_resume else "new_session",
                    "state": "UNSUPPORTED",
                    "reason": "Codex adapter never enables Full Computer Access",
                },
                "configured_state": "UNSUPPORTED",
                "effective_state": "UNKNOWN",
                "verification_state": "NOT_APPLICABLE",
                "evidence": {
                    "kind": "ADAPTER_GUARD",
                    "observed_at": observed_at,
                    "provider_limitation": "Full Computer Access is not configurable by this adapter",
                },
                "verified_at": None,
                "session_id": session_id or None,
            }
        if is_resume:
            return {
                "requested_intent": self.requested_intent,
                "native_mapping": {
                    "provider": "codex_cli",
                    "operation": "resume",
                    "state": "NOT_CONFIGURABLE",
                    "requested_sandbox": self.sandbox,
                    "reason": "Current Codex exec resume does not accept a sandbox declaration",
                },
                "configured_state": "NOT_CONFIGURABLE",
                "effective_state": "UNKNOWN",
                "verification_state": "UNVERIFIED",
                "evidence": {
                    "kind": "PROVIDER_LIMITATION",
                    "observed_at": observed_at,
                    "provider_limitation": "Resume access must be re-verified; no native effective access receipt is available",
                },
                "verified_at": None,
                "drift": "RESUME_ACCESS_UNVERIFIED",
                "session_id": session_id or None,
            }
        return {
            "requested_intent": self.requested_intent,
            "native_mapping": {
                "provider": "codex_cli",
                "operation": "new_session",
                "state": "APPLIED" if command_accepted else "PENDING",
                "sandbox": self.sandbox,
                "approval": "EXPLICIT_CURIS_TOOLS_ONLY_OTHER_TOOLS_DEFAULT" if self.tool_url else "PROVIDER_DEFAULT_NOT_DECLARED",
            },
            "configured_state": "CONFIGURED" if command_accepted else "PENDING",
            "effective_state": "UNKNOWN",
            "verification_state": "UNVERIFIED",
            "evidence": {
                "kind": "COMMAND_ARGUMENT_ACCEPTED" if command_accepted else "COMMAND_NOT_STARTED",
                "observed_at": observed_at,
                "provider_limitation": "Codex JSONL does not return effective access evidence",
            },
            "verified_at": None,
            "session_id": session_id or None,
            "network_boundary": (self.native_model_profile or {}).get("network_boundary"),
        }

    @staticmethod
    def _permissions_projection(computer_access: dict[str, Any]) -> dict[str, Any]:
        """Compatibility audit projection; it is never an effective-permission claim."""
        return {
            "requested_intent": computer_access["requested_intent"],
            "native_mapping": computer_access["native_mapping"],
            "configured_state": computer_access["configured_state"],
            "effective_state": computer_access["effective_state"],
            "verification_state": computer_access["verification_state"],
            "verified_at": computer_access["verified_at"],
        }

    @staticmethod
    def _parse_jsonl(text: str) -> dict[str, Any]:
        session_id = ""
        output = ""
        usage: dict[str, Any] = {}
        progress = []
        artifacts = []
        for line in text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            event_type = str(event.get("type") or "")
            progress.append(event_type)
            if event_type == "thread.started":
                session_id = str(event.get("thread_id") or "")
            elif event_type == "item.completed":
                item = event.get("item") or {}
                if item.get("type") == "agent_message":
                    output = str(item.get("text") or "")
                elif item.get("type") == "file_change":
                    artifacts.append({"type": "file_change", "id": item.get("id", "")})
            elif event_type == "turn.completed":
                usage = event.get("usage") or {}
        return {
            "session_id": session_id,
            "output": output,
            "usage": usage,
            "progress": progress,
            "artifacts": artifacts,
        }


def validate_agent_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    required = {"id", "name", "adapter", "capabilities"}
    missing = sorted(required - manifest.keys())
    if missing:
        raise ValueError("agent manifest missing: " + ", ".join(missing))
    if manifest["adapter"] not in {"codex_cli", "claude_code_cli", "http", "mcp", "coze"}:
        raise ValueError("agent manifest adapter is not supported")
    return {
        "id": str(manifest["id"]),
        "name": str(manifest["name"]),
        "adapter": str(manifest["adapter"]),
        "capabilities": list(manifest["capabilities"]),
        "credential_ref": str(manifest.get("credential_ref") or ""),
        "external_ref": str(manifest.get("external_ref") or ""),
    }
