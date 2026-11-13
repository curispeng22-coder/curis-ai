"""Ephemeral, task-bound HTTP MCP tools served by the packaged Curis backend."""
from __future__ import annotations

import base64
import contextvars
import hashlib
import json
import os
import secrets
import stat
import threading
import time
from pathlib import Path

from .agent_work_resources import open_directory
from .skill_package import relative_path
from .agent_adapter import _AGENT_STOP_SPAWN_LOCK

MAX_REQUEST = 12 * 1024 * 1024


def read_manifest_file(root: Path, relative: str, expected: dict) -> bytes:
    name = Path(relative_path(relative))
    directory = open_directory(root, root.parent.parent.parent.parent)
    try:
        for part in name.parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        fd = os.open(name.name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW, dir_fd=directory)
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != expected["bytes"]:
                raise ValueError("技能文件身份或大小改变。")
            with os.fdopen(fd, "rb", closefd=False) as handle:
                data = handle.read(2 * 1024 * 1024 + 1)
            after = os.fstat(fd)
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns) or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                raise ValueError("技能文件摘要改变。")
            return data
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def write_output(resources, name: str, data: bytes, *, _capture_token=None) -> dict:
    relative = Path(relative_path(name))
    if len(relative.parts) != 1 or not data or len(data) > 8 * 1024 * 1024:
        raise ValueError("成果必须使用单个文件名，大小介于 1 字节和 8 MiB。")
    existing = resources.collect(_capture_token=_capture_token)
    if len(existing) >= 32 or sum(item["bytes"] for item in existing) + len(data) > 16 * 1024 * 1024:
        raise ValueError("成果文件数量或总大小已达到本次上限。")
    directory = open_directory(resources.path / "output", resources.path.parent)
    try:
        fd = os.open(relative.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(directory)
    return next(item for item in resources.collect(_capture_token=_capture_token) if item["relative_path"] == relative.name)


def schema(properties, required):
    return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}


class AgentToolSessions:
    def __init__(self, *, clock=time.monotonic):
        self.clock = clock
        self.sessions = {}
        self.lock = threading.RLock()

    def register(self, resources, packages, should_stop, *, browser=None, seconds=90):
        if type(seconds) not in {int, float} or not 0 < seconds <= 90:
            raise ValueError("工具许可最长 90 秒。")
        token = secrets.token_urlsafe(32)
        manifests = {p["manifest"]["package_sha256"]: p["manifest"] for p in packages}
        with self.lock:
            self.sessions[token] = {"resources": resources, "manifests": manifests, "browser": browser,
                "stop": should_stop, "expires": self.clock() + seconds, "context": contextvars.copy_context(),
                "lock": threading.Lock(), "calls": 0, "reads": set(), "browser_calls": [], "closed": False}
        return token

    def bind_owner_channel(self, token, identity):
        """Bind the existing tool token once; the token never crosses the owner pipe."""
        keys = {"tenant_id","company_id","work_ref","task_id","employee_id","binding_ref"}
        if (type(identity) is not dict or set(identity) != keys
                or any(type(v) is not str or not v or "\0" in v or len(v)>256 for v in identity.values())):
            raise PermissionError("原工作工具身份无法核验。")
        with _AGENT_STOP_SPAWN_LOCK, self.lock:
            session = self.sessions.get(token)
            if not session:raise PermissionError("工具许可不可用。")
            self._require_live(session)
            if (any(identity[k] != v for k,v in session["resources"].identity.items())
                    or session.get("owner_channel_bound")):
                raise PermissionError("工具许可不能跨工作或重复绑定。")
            session["owner_channel_bound"] = True
        try:
            descriptor = session["resources"].owner_channel_descriptor(session["manifests"])
            with _AGENT_STOP_SPAWN_LOCK:self._require_live(session)
            return _OwnerWorkTools(self,token,identity,descriptor)
        except BaseException:
            with _AGENT_STOP_SPAWN_LOCK:session["closed"] = True
            raise

    def close(self, token):
        with _AGENT_STOP_SPAWN_LOCK, self.lock:
            session = self.sessions.pop(token, None)
            if session:
                session["closed"] = True
        if session and session["browser"]:
            session["browser"].close()

    def close_all(self):
        with self.lock:
            tokens = list(self.sessions)
        for token in tokens:
            self.close(token)

    def evidence(self, token):
        with self.lock:
            item = self.sessions.get(token)
            if not item:
                return []
            return [{"package_sha256": key, "path": path, "sha256": sha, "read_by_agent_tool": True}
                    for key, path, sha in sorted(item["reads"])]

    def browser_evidence(self, token):
        with self.lock:
            item = self.sessions.get(token)
            return [dict(call) for call in item["browser_calls"]] if item else []

    def handle(self, token, request):
        if not isinstance(token, str) or len(token) > 128:
            raise PermissionError("工具许可不可用。")
        with self.lock:
            session = self.sessions.get(token)
        if not session:
            raise PermissionError("工具许可不可用。")
        with session["lock"]:
            return session["context"].copy().run(self._handle, session, request)

    def _handle(self, session, request):
        with _AGENT_STOP_SPAWN_LOCK:
            self._require_live(session)
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
            raise ValueError("无效的 MCP 请求。")
        method, params, request_id = request.get("method"), request.get("params", {}), request.get("id")
        if not isinstance(params, dict) or (request_id is not None and type(request_id) not in {str, int}):
            raise ValueError("无效的 MCP 参数。")
        if method in {"notifications/initialized", "notifications/cancelled"} and request_id is None:
            return None
        if method == "initialize":
            result = {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}},
                "serverInfo": {"name": "curis-original-work", "version": "1"},
                "instructions": "Only this task's pinned skills, output files and explicitly allowed public browser targets are available."}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": self._tools(session)}
        elif method == "tools/call":
            session["calls"] += 1
            if session["calls"] > 100:
                raise PermissionError("本次工具请求已达到上限。")
            try:
                value = self._call(session, params.get("name"), params.get("arguments", {}))
                with _AGENT_STOP_SPAWN_LOCK:
                    self._require_live(session)
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": False}
            except (ValueError, OSError, UnicodeError, KeyError, TypeError):
                result = {"content": [{"type": "text", "text": "工具请求未通过原工作范围、文件摘要或浏览器边界检查。"}], "isError": True}
        else:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method unavailable"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    def _require_live(self, session):
        if session["closed"] or self.clock() >= session["expires"] or session["stop"]():
            raise PermissionError("原工作已停止，或工具许可已到期。")

    def _tools(self, session):
        tools = [
            {"name": "read_skill", "description": "Read one file from an explicitly bound, verified skill package. Never execute its scripts.",
             "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
             "inputSchema": schema({"package_sha256": {"type": "string"}, "path": {"type": "string"}}, ["package_sha256", "path"])},
            {"name": "write_output", "description": "Create a new file in this original task's output folder. Existing files cannot be overwritten.",
             "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False},
             "inputSchema": schema({"name": {"type": "string"}, "encoding": {"type": "string", "enum": ["utf8", "base64"]},
                "content": {"type": "string", "maxLength": MAX_REQUEST}}, ["name", "encoding", "content"])},
        ]
        if session["browser"]:
            tools.append({"name": "browser", "description": "Read approved public HTTPS pages in this work's isolated BrowserSkill session; no accounts, forms or arbitrary scripts.",
                "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
                "inputSchema": schema({"action": {"type": "string", "enum": ["navigate", "observe", "extract", "screenshot"]},
                    "url": {"type": "string"}, "target_id": {"type": "string"}}, ["action"])})
        return tools

    def _call(self, session, name, arguments):
        if not isinstance(arguments, dict):
            raise ValueError("工具参数必须是对象。")
        resources = session["resources"]
        if name == "read_skill" and set(arguments) == {"package_sha256", "path"}:
            key, path = arguments["package_sha256"], arguments["path"]
            manifest = session["manifests"][key]
            expected = next((f for f in manifest["files"] if f["path"] == path), None)
            if expected is None:
                raise ValueError("文件不属于已绑定的技能包。")
            data = read_manifest_file(resources.path / ".agents" / "skills" / key, path, expected)
            text = data.decode("utf-8")
            session["reads"].add((key, path, expected["sha256"]))
            return {"package_sha256": key, "path": path, "sha256": expected["sha256"], "text": text}
        if name == "write_output" and set(arguments) == {"name", "encoding", "content"}:
            content = arguments["content"]
            if not isinstance(content, str) or len(content) > MAX_REQUEST:
                raise ValueError("成果超出大小上限。")
            if arguments["encoding"] == "utf8":
                data = content.encode()
            elif arguments["encoding"] == "base64":
                data = base64.b64decode(content, validate=True)
            else:
                raise ValueError("成果编码不支持。")
            # Linearize this backend's final write against persisted task cancellation.
            with _AGENT_STOP_SPAWN_LOCK:
                self._require_live(session)
                value = write_output(resources, arguments["name"], data)
                self._require_live(session)
                return value
        if name == "browser" and session["browser"] and set(arguments) <= {"action", "url", "target_id"}:
            browser = session["browser"]
            value = browser.call(arguments, resources)
            with self.lock:
                if session["closed"] or self.clock() >= session["expires"] or session["stop"]():
                    raise PermissionError("原工作已停止或许可到期，拒绝迟到结果。")
                session["browser_calls"].append({"action": arguments["action"], "session_id": browser.session,
                    "browser_instance_id": browser.browser_id, "tab_id": browser.tab,
                    "result_sha256": hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                    **({"url": value["url"]} if arguments["action"] == "navigate" else {}),
                    "dns": value.get("dns") or [],
                    "content_verification": "UNVERIFIED"})
            return value
        raise ValueError("工具或参数不属于本次授权。")

    async def http(self, request):
        from fastapi.responses import JSONResponse, Response
        import asyncio
        if not request.client or request.client.host not in {"127.0.0.1", "::1"} or request.method != "POST":
            return Response(status_code=403)
        auth = request.headers.get("authorization", "")
        if not auth.startswith("Bearer ") or request.headers.get("origin"):
            return Response(status_code=403)
        with self.lock:
            bound = self.sessions.get(auth[7:])
        if not bound or any(request.headers.get(header) not in {None, bound["resources"].identity[field]}
                            for header, field in (("x-tenant-id", "tenant_id"), ("x-company-id", "company_id"))):
            return Response(status_code=403)
        body = bytearray()
        async for chunk in request.stream():
            if len(body) + len(chunk) > MAX_REQUEST:
                return Response(status_code=413)
            body.extend(chunk)
        try:
            result = await asyncio.to_thread(self.handle, auth[7:], json.loads(body))
        except PermissionError:
            return Response(status_code=403)
        except (ValueError, TypeError):
            return Response(status_code=400)
        return JSONResponse(result) if result is not None else Response(status_code=202)


class _OwnerWorkTools:
    """Finite MCP dispatch over an already authenticated original container channel."""
    def __init__(self, server, token, identity, descriptor):
        self.server,self._token = server,token
        self.identity = dict(identity)
        self.descriptor = descriptor
        self.binding = None
        self.sequence = 0
        self.revoked = False
        self.lock = threading.Lock()

    def bind(self, runtime):
        import re
        keys = {"nonce","boot_id","container_id","image_digest"}
        if (type(runtime) is not dict or set(runtime) != keys
                or any(type(v) is not str for v in runtime.values())
                or not re.fullmatch(r"[0-9a-f]{48}",str(runtime.get("nonce")))
                or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",str(runtime.get("boot_id")))
                or not re.fullmatch(r"[0-9a-f]{64}",str(runtime.get("container_id")))
                or not re.fullmatch(r"sha256:[0-9a-f]{64}",str(runtime.get("image_digest")))):
            raise PermissionError("工具通道容器身份无效。")
        with self.lock:
            if self.revoked or self.binding is not None:raise PermissionError("工具通道不能重绑。")
            self.binding = {"identity":self.identity.copy(),**runtime}

    def revoke(self):
        # Do not hold the request lock: cancellation must revoke an in-flight call.
        with _AGENT_STOP_SPAWN_LOCK, self.server.lock:
            self.revoked = True
            session = self.server.sessions.get(self._token)
            if session:session["closed"] = True

    def dispatch(self, frame):
        with self.lock:
            if self.revoked or self.binding is None:raise PermissionError("工具通道已撤回。")
            if (type(frame) is not dict or set(frame) != {*self.binding,"sequence","request"}
                    or any(frame[k] != v for k,v in self.binding.items())
                    or type(frame["sequence"]) is not int or frame["sequence"] != self.sequence+1
                    or frame["sequence"] > 200):
                raise PermissionError("工具通道原工作、容器或序号不匹配。")
            request = frame["request"]
            if (type(request) is not dict or set(request)-{"jsonrpc","id","method","params"}
                    or request.get("jsonrpc") != "2.0"
                    or request.get("method") not in {"initialize","ping","notifications/initialized","tools/list","tools/call"}
                    or request.get("method") == "tools/call" and
                       (type(request.get("params")) is not dict or request["params"].get("name") not in {"read_skill","write_output","browser"})):
                raise PermissionError("工具通道仅允许原工作有限工具。")
            raw = json.dumps(frame,separators=(",",":"),allow_nan=False).encode()
            if len(raw) > 32768:raise ValueError("工具通道请求过大。")
            self.sequence = frame["sequence"]  # An admitted operation is never replayed.
            try:
                value = self.server.handle(self._token,request)
                response = {**self.binding,"sequence":self.sequence,"response":value}
                if len(json.dumps(response,separators=(",",":"),allow_nan=False).encode()) > 60000:
                    raise ValueError("工具通道结果过大，状态需核验。")
                if self.revoked:raise PermissionError("工具通道停止后拒绝结果。")
                return response
            except BaseException:
                self.revoke()
                raise
