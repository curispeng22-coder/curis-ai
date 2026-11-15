"""Owned BrowserSkill session with public-only, method-limited TLS egress."""
from __future__ import annotations

import base64
import ctypes
import hashlib
import http.client
import ipaddress
import json
import os
import re
import secrets
import signal
import select
import socket
import socketserver
import ssl
import stat
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import parse_qsl, quote, urljoin, urlsplit

import certifi

from .agent_adapter import packaged_supervisor_command, _verified_child_exit_receipt
from .agent_work_resources import safe_directory

BSK_SHA256 = "900c85d168a4a23f19767aa918b4de4c2ae0097cd298fca3691b89843935bb58"
BSK_COMMIT = "d9a78aed47874459ae1e44523a597e42dd9acf99"


def managed_browser_tool(metadata):
    configured = str(metadata.get("browser_skill_path") or "")
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    path = Path(configured) if configured else root / "vendor/browser-skill/bsk"
    if (not path.is_absolute() or not path.is_file() or path.is_symlink()
            or not os.access(path, os.X_OK) or hashlib.sha256(path.read_bytes()).hexdigest() != BSK_SHA256):
        raise ValueError("内置 BrowserSkill 尚未就绪或版本无法核验，请检查应用安装。")
    return path
WS_PORT = 52829
_LEASE_LOCK = threading.Lock()
_UNRESOLVED_BROWSER_PROCESSES = []
SENSITIVE_HEADERS = {"authorization", "proxy-authorization", "cookie", "set-cookie",
                     "set-cookie2", "connection", "proxy-connection", "transfer-encoding", "content-length", "referer"}
PUBLIC_REQUEST_HEADERS = {"accept", "accept-language", "accept-encoding", "user-agent", "range",
                          "if-none-match", "if-modified-since", "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site"}
SETUP_HOSTS = ("chromewebstore.google.com", "clients2.google.com", "clients2.googleusercontent.com",
               "clients4.google.com", "lh3.googleusercontent.com", "www.gstatic.com", "ssl.gstatic.com")
BENCHMARK_NETWORK = ipaddress.ip_network("198.18.0.0/15")


from .agent_browser_policy import (host_name, _doh_exchange, pinned_public_dns, PublicTargets,
    tls_certificate, PublicReadProxy)


class _BrowserBsdInfo(ctypes.Structure):
    # Apple's proc_bsdinfo ABI, also used by the existing PID-bound Native controls.
    _fields_ = [(name, ctypes.c_uint32) for name in (
        "flags", "status", "xstatus", "pid", "ppid", "uid", "gid", "ruid", "rgid", "svuid", "svgid", "rfu")]
    _fields_ += [("comm", ctypes.c_char * 16), ("name", ctypes.c_char * 32)]
    _fields_ += [(name, ctypes.c_uint32) for name in ("nfiles", "pgid", "pjobc", "tdev", "tpgid")]
    _fields_ += [("nice", ctypes.c_int32), ("start_seconds", ctypes.c_uint64), ("start_microseconds", ctypes.c_uint64)]


def _browser_libproc():
    if sys.platform != "darwin" or ctypes.sizeof(_BrowserBsdInfo) != 136:
        raise ValueError("当前平台无法核验浏览器内核身份。")
    library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
    library.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    library.proc_pidinfo.restype = ctypes.c_int
    library.proc_pidpath.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
    library.proc_pidpath.restype = ctypes.c_int
    library.proc_listchildpids.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    library.proc_listchildpids.restype = ctypes.c_int
    return library


def _browser_process_identity(pid):
    if type(pid) is not int or pid <= 1:
        raise ValueError("浏览器进程标识无法核验。")
    library = _browser_libproc()
    info = _BrowserBsdInfo()
    if (library.proc_pidinfo(pid, 3, 0, ctypes.byref(info), ctypes.sizeof(info)) != ctypes.sizeof(info)
            or info.pid != pid or info.status not in {2, 3, 4}
            or info.start_seconds <= 0 or info.start_microseconds >= 1000000):
        raise ValueError("浏览器内核进程身份不可用。")
    path = ctypes.create_string_buffer(4096)
    if library.proc_pidpath(pid, path, len(path)) <= 0:
        raise ValueError("浏览器可执行路径不可核验。")
    return {"pid": pid, "ppid": int(info.ppid), "uid": int(info.uid), "pgid": int(info.pgid),
            "start": (int(info.start_seconds), int(info.start_microseconds)),
            "executable": os.fsdecode(path.value)}


def _browser_direct_children(supervisor_pid):
    # Query only this held supervisor's children, never an all-process inventory.
    library = _browser_libproc()
    buffer = (ctypes.c_int * 4)()
    ctypes.set_errno(0)
    count = library.proc_listchildpids(supervisor_pid, buffer, ctypes.sizeof(buffer))
    if count < 0 or count >= len(buffer) or (count == 0 and ctypes.get_errno()):
        raise ValueError("浏览器直接子进程集合无法核验。")
    children = tuple(buffer[:count])  # This API returns a PID count, not a byte length.
    if len(children) > 1 or any(pid <= 1 for pid in children):
        raise ValueError("浏览器监督进程出现非预期的直接子进程。")
    return children


class OwnedProcess:
    """Only held supervisor handles are signalled; missing child evidence stays UNKNOWN."""
    def __init__(self, command, cwd, environment, *, deadline=None, browser_only=False):
        if _UNRESOLVED_BROWSER_PROCESSES:
            raise ValueError("先前浏览器停止状态未确认，请保留现场核验。")
        now = time.monotonic()
        self.deadline = min(now + 90, deadline if deadline is not None else now + 90)
        if self.deadline <= now:
            raise ValueError("浏览器启动期限已过。")
        self.nonce = secrets.token_hex(16)
        self.diagnostic = bytearray()
        self.shutdown_evidence = None
        self._close_lock = threading.Lock()
        supervisor_command = packaged_supervisor_command()
        if browser_only:
            from .agent_browser_runtime import validate_browser_supervisor_request
            validate_browser_supervisor_request({"command": command, "cwd": str(cwd),
                "environment": environment, "prompt": ""})
            expected_executable = os.path.realpath(command[0])
            supervisor_command[-1] = "--curis-browser-supervisor"
        else:
            if (len(command) < 4 or command[:2] != ["/usr/bin/sandbox-exec", "-f"]
                    or not Path(command[2]).is_absolute() or not Path(command[3]).is_absolute()):
                raise ValueError("浏览器必须保留已限定的外层沙箱。")
            expected_executable = os.path.realpath(command[3])
        self.process = subprocess.Popen(supervisor_command, cwd=cwd, env=environment,
            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            close_fds=True, start_new_session=True)
        self.group_id = self.process.pid
        try:
            self.supervisor_identity = _browser_process_identity(self.process.pid)
            if (self.supervisor_identity["pgid"] != self.process.pid or self.supervisor_identity["uid"] != os.getuid()
                    or self.supervisor_identity["executable"] != os.path.realpath(supervisor_command[0])):
                raise ValueError("持有的浏览器监督进程身份不匹配。")
            os.set_blocking(self.process.stderr.fileno(), False)
            request = {"command": command, "cwd": str(cwd), "environment": environment, "prompt": "",
                       "timeout": min(90, self.deadline - now), "nonce": self.nonce, "deadline": self.deadline}
            self.process.stdin.write((json.dumps(request) + "\n").encode())
            self.process.stdin.flush()
            startup_deadline = min(self.deadline, time.monotonic() + 4)
            while True:
                if self.process.poll() is not None or time.monotonic() >= startup_deadline:
                    raise ValueError("浏览器启动身份未确认，未报告就绪。")
                if _browser_process_identity(self.process.pid) != self.supervisor_identity:
                    raise ValueError("浏览器监督进程身份发生变化。")
                if select.select([self.process.stderr], [], [], 0)[0]:
                    self._read_diagnostic()
                    if self.diagnostic:
                        raise ValueError("浏览器已返回最终状态，不能替代运行中的启动身份。")
                children = _browser_direct_children(self.process.pid)
                if children:
                    if len(children) != 1:
                        raise ValueError("浏览器启动出现非预期的直接子进程集合。")
                    child = _browser_process_identity(children[0])
                    if (child["ppid"] != self.process.pid or child["pgid"] != self.group_id
                            or child["uid"] != self.supervisor_identity["uid"]
                            or child["start"] < self.supervisor_identity["start"]):
                        raise ValueError("浏览器直接子进程不属于原监督身份。")
                    # sandbox-exec may still be in its exec transition; no second launch or PID adoption.
                    if child["executable"] == expected_executable:
                        if (self.process.poll() is not None
                                or _browser_process_identity(self.process.pid) != self.supervisor_identity
                                or _browser_direct_children(self.process.pid) != children
                                or _browser_process_identity(children[0]) != child):
                            raise ValueError("浏览器启动身份在核验期间发生变化。")
                        self.pid, self.child_identity = child["pid"], child
                        break
                    if child["executable"] != "/usr/bin/sandbox-exec":
                        raise ValueError("浏览器直接子进程可执行路径不匹配。")
                remaining = startup_deadline - time.monotonic()
                if remaining > 0:
                    select.select([self.process.stderr], [], [], min(0.05, remaining))
        except BaseException:
            try:
                self.close()
            except BaseException:
                pass  # Keep the original startup/interruption error after attempting all cleanup.
            raise

    def _read_diagnostic(self):
        while len(self.diagnostic) <= 4096:
            try:
                chunk = os.read(self.process.stderr.fileno(), 4097 - len(self.diagnostic))
            except BlockingIOError:
                return
            if not chunk:
                return
            self.diagnostic.extend(chunk)
        raise ValueError("浏览器监督回执超过上限。")

    def alive(self):
        if self.shutdown_evidence is not None or self.process.poll() is not None or time.monotonic() >= self.deadline:
            return False
        try:
            return (_browser_process_identity(self.process.pid) == self.supervisor_identity
                    and _browser_process_identity(self.pid) == self.child_identity)
        except (OSError, ValueError, AttributeError):
            return False

    def close(self):
        with self._close_lock:
            if self.shutdown_evidence is not None:
                return dict(self.shutdown_evidence)
            evidence = {"supervisor": "UNKNOWN", "direct_child": "UNKNOWN",
                        "descendants": "UNKNOWN", "effects": "UNKNOWN", "errors": []}
            interruption = None
            def failed(error):
                nonlocal interruption
                evidence["errors"].append(type(error).__name__)
                if not isinstance(error, Exception) and interruption is None:
                    interruption = error
            try:
                if self.process.stdin and not self.process.stdin.closed:
                    try:
                        self.process.stdin.close()
                    except BaseException as error:
                        failed(error)
                for action in (None, "terminate", "kill"):
                    try:
                        if self.process.poll() is not None:
                            break
                        if action:
                            getattr(self.process, action)()  # Only this retained direct supervisor.
                        self.process.wait(timeout=min(1.0, max(0.0, self.deadline - time.monotonic())))
                    except BaseException as error:
                        failed(error)
                try:
                    code = self.process.poll()
                    if code is not None:
                        evidence["supervisor"] = "EXITED"
                    self._read_diagnostic()
                    data = bytes(self.diagnostic)
                    receipt = _verified_child_exit_receipt(data, self.nonce, code)
                    if (receipt is None and hasattr(self, "pid") and code == -signal.SIGKILL
                            and data.endswith(b"\n") and len(data.splitlines()) == 1):
                        pairs = json.loads(data, object_pairs_hook=list)
                        if isinstance(pairs, list) and len(pairs) == 3 and all(isinstance(pair, tuple) and len(pair) == 2 for pair in pairs):
                            result = dict(pairs)
                            if (set(result) == {"type", "nonce", "returncode"}
                                    and result["type"] == "curis.supervisor.result" and result["nonce"] == self.nonce
                                    and type(result["returncode"]) is int and -255 <= result["returncode"] <= 255):
                                receipt = {"child_pid": self.pid, "returncode": result["returncode"],
                                           "attempt_sha256": hashlib.sha256(self.nonce.encode("ascii")).hexdigest()}
                    if receipt and (not hasattr(self, "pid") or receipt["child_pid"] == self.pid):
                        evidence.update(direct_child="EXITED", receipt=receipt)
                except BaseException as error:
                    failed(error)
            finally:
                for pipe in (self.process.stdin, self.process.stderr):
                    if pipe and not pipe.closed:
                        try:
                            pipe.close()
                        except BaseException as error:
                            failed(error)
                self.shutdown_evidence = evidence
                if evidence["supervisor"] != "EXITED" or evidence["direct_child"] != "EXITED":
                    _UNRESOLVED_BROWSER_PROCESSES.append(self)
            if interruption is not None:
                raise interruption
            return dict(evidence)


def process_profile(path, read_paths, write_paths, ports, *, service=False, unix_paths=()):
    def rule(kind, value):
        return "(" + kind + " " + json.dumps(str(value)) + ")"
    lines = ["(version 1)", "(allow default)", "(deny file-read-data)",
        "(allow file-read-data (literal \"/\") (subpath \"/System\") (subpath \"/usr\") (subpath \"/Library/Apple\")",
        " (literal \"/dev/null\") (literal \"/dev/urandom\") (literal \"/dev/random\")",
        *[" " + rule(kind, value) for kind, value in read_paths], ")",
        "(deny file-write*)", "(allow file-write* (literal \"/dev/null\")",
        *[" " + rule("subpath", value) for value in write_paths], ")",
        "(deny network*)"]
    for port in ports:
        lines.append('(allow network-outbound (remote ip "localhost:' + str(port) + '"))')
    if service:
        lines += ['(allow network-bind (local ip "localhost:' + str(WS_PORT) + '"))',
                  '(allow network-inbound (local ip "localhost:' + str(WS_PORT) + '"))',
                  '(allow network-bind network-inbound network-outbound (local unix-socket (subpath ' + json.dumps(str(path.parent)) + ')))']
    for directory in unix_paths:
        lines.append('(allow network-bind network-inbound network-outbound (local unix-socket (subpath ' + json.dumps(str(directory)) + ')))')
    path.write_text("\n".join(lines) + "\n")
    return path


class BrowserLease:
    def __init__(self, root, identity, metadata, hosts, *, alive=lambda: True, setup=False):
        # This launcher owns Mac processes; a Linux runtime needs its verified adapter.
        if sys.platform != "darwin":
            raise ValueError("当前本地浏览器启动器仅支持 macOS；隔离运行环境适配器尚未验证。")
        self.identity, self.stop_check = dict(identity), alive
        self.deadline = time.monotonic() + 90
        self._closed = False
        self._close_lock = threading.Lock()
        self.shutdown_evidence = None
        profile_identity = {key: identity[key] for key in ("tenant_id", "company_id")}
        self.key = hashlib.sha256(json.dumps(profile_identity, sort_keys=True).encode()).hexdigest()
        self.base = safe_directory(Path(root) / self.key)
        override = os.environ.get("CURIS_AGENT_BROWSER_PROFILE", "")
        self.profile = Path(override) if override else self.base / "profile"
        if not self.profile.is_absolute():
            raise ValueError("受管浏览器资料夹必须是绝对路径。")
        if override:
            daily = Path.home() / "Library" / "Application Support"
            if self.profile == daily or daily in self.profile.parents:
                raise ValueError("不能接管用户日常浏览器资料夹。")
        profile_identity["profile_path"] = str(self.profile)
        marker = self.base / "owner.json"
        if marker.exists():
            if marker.is_symlink() or json.loads(marker.read_text()) != profile_identity:
                raise ValueError("浏览器资料夹不属于当前员工范围。")
        else:
            if self.profile.exists() and not override:
                raise ValueError("不能接管已有浏览器资料夹。")
            with marker.open("x") as handle:
                json.dump(profile_identity, handle, sort_keys=True)
        safe_directory(self.profile)
        singleton = self.profile / "SingletonLock"
        if os.path.lexists(singleton):
            target = os.readlink(singleton)
            found = re.fullmatch(r".+-([0-9]+)", target)
            if not found:
                raise ValueError("浏览器资料夹锁无法核验。")
            try:
                os.kill(int(found[1]), 0)
            except ProcessLookupError:
                pass  # Chrome itself handles its stale lock; Curis never deletes it.
            else:
                raise ValueError("此独立浏览器资料夹仍在使用中。")
        self.session = "curis-" + secrets.token_hex(12)
        self.state = safe_directory(Path("/private/tmp") / ("curis-browser-" + str(os.getuid()) + "-" + self.key[:16]))
        self.run = safe_directory(self.base / self.session)
        self.proxy = self.service = self.chrome = None
        self.tab = None
        self.sequence = 0
        self.setup = setup
        self._session_start_attempted = self._session_started = False
        self.policy = PublicTargets(list(SETUP_HOSTS) if setup else hosts)
        self.temporary = safe_directory(self.state / "tmp")
        self.environment = {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8", "TMPDIR": str(self.temporary)}
        bsk = managed_browser_tool(metadata)
        chrome = Path(str(metadata.get("browser_chrome_path") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")).absolute()
        if (not bsk.is_file() or bsk.is_symlink() or hashlib.sha256(bsk.read_bytes()).hexdigest() != BSK_SHA256
                or not chrome.is_file() or chrome.is_symlink()):
            raise ValueError("请先连接核验过的 BrowserSkill 0.3.3 和 Chrome。")
        if not _LEASE_LOCK.acquire(blocking=False):
            raise ValueError("另一项原工作仍持有独立浏览器，请先停止或等待完成。")
        self.lock_held = True
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                probe.bind(("127.0.0.1", WS_PORT))
            self.proxy = PublicReadProxy(self.run / "tls", self.policy, alive=alive)
            service_profile = process_profile(self.state / (self.session + ".sb"),
                [("literal", bsk), ("subpath", self.state), ("subpath", self.run)],
                [self.state, self.run], [], service=True)
            self.service = OwnedProcess(["/usr/bin/sandbox-exec", "-f", str(service_profile), str(bsk),
                "daemon", "start", "--mode", "local", "--port", str(WS_PORT), "--foreground",
                "--daemon-idle", "2m", "--session-idle", "2m"], self.state,
                {**self.environment, "BSK_HOME": str(self.state), "BSK_AUTO_START": "0", "BSK_AUTO_UPDATE": "off"},
                deadline=self.deadline)
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                try:
                    info = json.loads((self.state / "daemon.json").read_text())
                    if (info["pid"] == self.service.pid and info["ws_port"] == WS_PORT
                            and info.get("version") == "0.3.3" and info.get("host_managed") is True):
                        self.socket_path = Path(info["sock_path"])
                        if self.socket_path != self.state / "run" / "daemon.sock":
                            raise ValueError("浏览器 IPC 不属于本次受管目录。")
                        break
                except (OSError, ValueError, KeyError):
                    pass
                time.sleep(0.05)
            else:
                raise ValueError("独立浏览器服务未就绪。")
            chrome_profile = process_profile(self.run / "chrome.sb",
                [("subpath", chrome.parents[2]), ("subpath", self.profile), ("subpath", self.run), ("subpath", self.temporary)],
                [self.profile, self.run, self.temporary], [self.proxy.port, WS_PORT], unix_paths=[self.temporary])
            self.chrome = OwnedProcess(["/usr/bin/sandbox-exec", "-f", str(chrome_profile), str(chrome),
                "--user-data-dir=" + str(self.profile), "--no-first-run", "--no-default-browser-check",
                "--disable-sync", "--disable-background-networking", "--disable-quic",
                "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
                "--proxy-server=http://127.0.0.1:" + str(self.proxy.port),
                "--proxy-bypass-list=<-loopback>;127.0.0.1:" + str(WS_PORT),
                "--ignore-certificate-errors-spki-list=" + self.proxy.spki,
                "https://chromewebstore.google.com/detail/hhcmgoofomhgciiibhipgmgkgnoenaoi" if setup else "about:blank"],
                self.run, {**self.environment, "MAC_CHROMIUM_TMPDIR": str(self.temporary)}, deadline=self.deadline)
            self._check_startup()
        except BaseException:
            try:
                self.close()
            except BaseException:
                pass
            raise

    def _require_open(self):
        if (getattr(self, "_closed", False) or time.monotonic() >= getattr(self, "deadline", float("inf"))
                or not getattr(self, "stop_check", lambda: True)()):
            raise ValueError("原工作浏览器已停止，拒绝新的调用或迟到结果。")

    def _check_startup(self):
        # A supervisor spawn report alone does not prove the child stayed alive.
        # This bounded check still does not claim a visible window or BSK connection.
        deadline = time.monotonic() + 1
        while True:
            if not self.chrome.alive() or not self.service.alive() or not self.stop_check():
                raise ValueError("独立浏览器准备已中止，连接尚未核验。请重新准备；若仍退出，请检查应用安装。")
            if time.monotonic() >= deadline:
                return
            time.sleep(0.05)

    def rpc(self, method, params):
        admitted = False
        try:
            self._require_open()
            if not self.service or not self.service.alive() or not self.stop_check():
                raise ValueError("原浏览器执行已停止。")
            info = self.socket_path.lstat()
            if (not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.geteuid()
                    or stat.S_IMODE(info.st_mode) & 0o077):
                raise ValueError("浏览器 IPC 不是原受管套接字。")
            deadline = min(self.deadline, time.monotonic() + 5)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ValueError("浏览器执行期限已过。")
                connection.settimeout(remaining)
                connection.connect(str(self.socket_path))
                peer = struct.unpack("i", connection.getsockopt(0, 2, 4))[0]  # Darwin LOCAL_PEERPID.
                if peer != self.service.pid or not self.service.alive():
                    raise ValueError("浏览器 IPC 服务进程改变。")
                request_id = secrets.token_hex(12)
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("浏览器 IPC 已过期。")
                connection.settimeout(remaining)
                admitted = True  # Partial sends have UNKNOWN effects; never replay.
                connection.sendall((json.dumps({"id": request_id, "method": method, "params": params}) + "\n").encode())
                response = bytearray()
                while b"\n" not in response:
                    self._require_open()
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise ValueError("浏览器执行期限已过。")
                    connection.settimeout(remaining)
                    chunk = connection.recv(65536)
                    if not chunk or len(response) + len(chunk) > 12 * 1024 * 1024:
                        raise ValueError("浏览器响应无效或超出上限。")
                    response.extend(chunk)
                line, tail = bytes(response).split(b"\n", 1)
                if tail or time.monotonic() >= deadline:
                    raise ValueError("浏览器 IPC 包含额外帧或迟到结果。")
                from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
                value = json.loads(line, object_pairs_hook=_unique_json_object,
                                   parse_constant=_invalid_json_constant, parse_float=_finite_json_float)
                if (type(value) is not dict or value.get("id") != request_id or "error" in value
                        or type(value.get("result")) is not dict):
                    raise ValueError("浏览器请求没有有效结果。")
                self._require_open()
                if not self.service.alive():
                    raise ValueError("原浏览器服务已退出，拒绝迟到结果。")
                return value["result"]
        except BaseException as error:
            if admitted:
                try: self.close()
                except BaseException: error.add_note("Owned browser cleanup UNKNOWN; no automatic replay")
            raise
    def connected(self):
        self._require_open()
        if not self.chrome or not self.chrome.alive():
            raise ValueError("本次独立 Chrome 已退出。")
        status = self.rpc("system.status", {})
        browsers = status.get("browsers") or []
        if (status.get("pid") != self.service.pid or status.get("daemon_version") != "0.3.3"
                or len(browsers) != 1 or browsers[0].get("extension_version") != "0.3.3"
                or browsers[0].get("unresponsive") or browsers[0].get("version_skew")):
            raise ValueError("请在独立浏览器安装 BrowserSkill 0.3.3，并将扩展端口设为 52829。")
        # Only this newly owned Chrome process group may hold the extension connection.
        observed = subprocess.run(["/usr/sbin/lsof", "-nP", "-a", "-iTCP:" + str(WS_PORT),
            "-sTCP:ESTABLISHED", "-Fp"], capture_output=True, text=True, timeout=3, check=True,
            env=self.environment, cwd=self.run)
        pids = {int(line[1:]) for line in observed.stdout.splitlines() if re.fullmatch(r"p[0-9]+", line)}
        peers = pids - {self.service.pid}
        if not peers or any(os.getpgid(pid) != self.chrome.group_id for pid in peers):
            raise ValueError("连接包含未授权的浏览器进程。")
        return browsers[0]["instance_id"]

    def start(self):
        self._require_open()
        if self.setup:
            raise ValueError("准备窗口不能执行 Agent 浏览工具。")
        if getattr(self, "_session_start_attempted", False):
            raise ValueError("原浏览会话已请求，不能重复创建。")
        self._session_start_attempted = True
        try:
            deadline = min(self.deadline, time.monotonic() + 10)
            while True:
                self._require_open()
                try:
                    self.browser_id = self.connected()
                    break
                except (ValueError, OSError, subprocess.SubprocessError):
                    if time.monotonic() >= deadline:
                        raise ValueError("独立浏览器尚未就绪，请先在 Agent 许可设置连接扩展。")
                    time.sleep(0.1)
            result = self.rpc("session.start", {"browser_instance_id": self.browser_id, "focused": False})
            if (type(result) is not dict or type(result.get("session_id")) is not str
                    or not result["session_id"] or len(result["session_id"]) > 256
                    or result.get("browser_instance_id") != self.browser_id):
                raise ValueError("BrowserSkill 原会话身份未通过核验。")
            self.session = result["session_id"]
            if type(result.get("agent_window_id")) is not int:
                raise ValueError("BrowserSkill 专用 Agent Window 未通过核验。")
            self._require_open()
            self._session_started = True
            return self
        except BaseException as error:
            try: self.close()
            except BaseException: error.add_note("Owned browser cleanup UNKNOWN")
            raise

    def _tab_url(self, tab_id=None):
        target = self.tab if tab_id is None else tab_id
        tabs = self.rpc("tool.tab_list", {"session_id": self.session, "scope": "agent"}).get("tabs", [])
        selected = [tab for tab in tabs if tab.get("tab_id") == target and tab.get("scope") == "agent"]
        if len(selected) != 1:
            raise ValueError("原网页已不属于本次浏览会话。")
        url = selected[0].get("url") or ""
        self.policy.url(url)
        return url

    def call(self, arguments, resources):
        self._require_open()
        if not getattr(self, "_session_started", False):
            raise ValueError("原工作浏览会话尚未核验。")
        if self.connected() != self.browser_id or any(value != self.identity.get(key) for key, value in resources.identity.items()):
            raise ValueError("原工作浏览器身份改变。")
        action = arguments.get("action")
        if action == "navigate" and set(arguments) == {"action", "url"}:
            self.policy.url(arguments["url"])
            result = self.rpc("tool.navigate", {"session_id": self.session, "url": arguments["url"],
                "wait_until": "domcontentloaded", "timeout_ms": 10000, **({"tab_id": self.tab} if self.tab else {})})
            if (type(result) is not dict or type(result.get("reached")) is not str
                    or result["reached"] not in {"commit", "domcontentloaded", "load", "networkidle"}
                    or result.get("error_text") or type(result.get("tab_id")) is not int):
                raise ValueError("网页导航未返回有效完成阶段；原 tab 未被替换。")
            self.policy.url(result.get("final_url") or result.get("url") or "")
            tab = result["tab_id"]
            final_url = self._tab_url(tab)
            self._require_open()
            self.tab = tab
            return {"tab_id": self.tab, "url": final_url,
                "dns": self.policy.dns_snapshot(), "content_verification": "UNVERIFIED"}
        if self.tab is None:
            raise ValueError("请先打开本次明确授权的公开网页。")
        if action not in {"observe", "extract", "screenshot"}:
            raise ValueError("本次不允许该浏览器动作。")
        before_url = self._tab_url()
        params = {"session_id": self.session, "tab_id": self.tab}
        if action == "observe" and set(arguments) == {"action"}:
            result = self.rpc("tool.observe", {**params, "max_tokens": 6000, "max_depth": 8, "probe_hover": False})
        elif action == "extract" and set(arguments) <= {"action", "target_id"}:
            result = self.rpc("tool.extract", {**params, "action": "table" if arguments.get("target_id") else "discover",
                **({"target_id": arguments["target_id"]} if arguments.get("target_id") else {}),
                "max_rows": 200, "max_columns": 30, "max_bytes": 131072, "timeout_ms": 5000})
        elif action == "screenshot" and set(arguments) == {"action"}:
            from .agent_tool_server import write_output
            result = self.rpc("tool.screenshot", params)
            if self._tab_url() != before_url:
                raise ValueError("截图期间原网页已改变。")
            if result.get("format") != "png" or result.get("tab_id") != self.tab:
                raise ValueError("截图不属于原网页。")
            data = base64.b64decode(result["image_base64"], validate=True)
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("截图格式不合法。")
            if not self.stop_check():
                raise ValueError("原工作已停止，拒绝截图。")
            self.sequence += 1
            token = resources.begin_browser_capture()
            receipt = write_output(resources, f"browser-{self.sequence}.png", data, _capture_token=token)
            if not self.stop_check() or self._tab_url() != before_url:
                raise ValueError("原工作或网页已改变，拒绝截图来源。")
            resources.register_browser_capture(receipt, url=before_url, session_id=self.session, tab_id=self.tab, _capture_token=token)
            return receipt
        else:
            raise ValueError("本次不允许该浏览器动作。")
        if result.get("tab_id", self.tab) != self.tab or self._tab_url() != before_url:
            raise ValueError("浏览器结果越过原网页范围。")
        if len(json.dumps(result).encode()) > 262144:
            raise ValueError("浏览器文字结果超出上限。")
        self._require_open()
        return {"result": result, "url": before_url, "dns": self.policy.dns_snapshot(), "content_verification": "UNVERIFIED"}

    def close(self):
        with self._close_lock:
            if self.shutdown_evidence is not None:
                return dict(self.shutdown_evidence)
            self._closed = True  # Admission closes even if teardown is interrupted.
            evidence = {"processes": {}, "proxy": "NOT_STARTED", "descendants": "UNKNOWN", "effects": "UNKNOWN"}
            interruption = None
            safe = not _UNRESOLVED_BROWSER_PROCESSES
            for name in ("chrome", "service"):
                process = getattr(self, name, None)
                if process:
                    try:
                        value = process.close()
                        evidence["processes"][name] = value
                        safe = safe and isinstance(value, dict) and value.get("supervisor") == value.get("direct_child") == "EXITED"
                    except BaseException as error:
                        safe = False
                        evidence["processes"][name] = {"state": "UNKNOWN", "error": type(error).__name__}
                        if not isinstance(error, Exception) and interruption is None:
                            interruption = error
            if self.proxy:
                # Standard server.shutdown may block; never hold the caller indefinitely.
                completed = threading.Event()
                proxy_result = {}
                def close_proxy():
                    try:
                        self.proxy.close()
                        proxy_result["proxy"] = "CLOSED"
                    except BaseException as error:
                        proxy_result.update(proxy="UNKNOWN", proxy_error=type(error).__name__)
                    finally:
                        completed.set()
                try:
                    threading.Thread(target=close_proxy, daemon=True).start()
                    done = completed.wait(timeout=min(1.0, max(0.0, self.deadline - time.monotonic())))
                    if done:
                        evidence.update(proxy_result)
                    else:
                        evidence["proxy"] = "UNKNOWN"
                    safe = safe and done and evidence["proxy"] == "CLOSED"
                except BaseException as error:
                    safe = False
                    evidence.update(proxy="UNKNOWN", proxy_error=type(error).__name__)
                    if not isinstance(error, Exception) and interruption is None:
                        interruption = error
            evidence["state"] = "CLOSED_WITH_UNKNOWN_EFFECTS" if safe else "OUTCOME_UNKNOWN"
            self.shutdown_evidence = evidence
            if safe and getattr(self, "lock_held", False):
                self.lock_held = False
                _LEASE_LOCK.release()
            # Unconfirmed cleanup retains the lease; no second session adopts unknown resources.
            if interruption is not None:
                raise interruption
            return dict(evidence)


class AgentBrowserLease:
    """One Work-selected public source; fresh context and proxy, not OS confinement."""
    def __init__(self, release, identity, should_stop):
        from .agent_browser_runtime import browser_environment, read_browser_marker
        from .agent_work_resources import scope_key
        self.identity = dict(identity)
        self.release, self.should_stop = release, should_stop
        self.session = secrets.token_hex(6)
        self.browser_id = "agent-browser:" + self.session
        self.tab = "owned-default-tab"
        self.deadline = time.monotonic() + 80
        self.closed = False
        self.shutdown_evidence = None
        self.proxy = self.daemon = None
        self.url = None
        temporary = Path(release["temporaryRoot"])
        marker_content = {"runtimeKind": "NATIVE_AGENT_BROWSER", "releaseSha256": release["releaseSha256"]}
        try:
            temporary.mkdir(mode=0o700)
            with (temporary / "release.json").open("x") as marker:
                json.dump(marker_content, marker, sort_keys=True)
        except FileExistsError:
            info = temporary.lstat()
            marker = temporary / "release.json"
            if (not stat.S_ISDIR(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o700 or info.st_uid != os.getuid()
                    or str(temporary.resolve()) != str(temporary)
                    or json.loads(read_browser_marker(marker)) != marker_content):
                raise ValueError("浏览器短临时根已有未知资源，不自动接管。")
        self.directory = temporary / scope_key(
            **{k: self.identity[k] for k in ("tenant_id", "company_id", "work_ref", "task_id")})[:16]
        if self.directory.exists():
            raise ValueError("原浏览器执行目录已存在，不自动重新启动。")
        safe_directory(self.directory)
        for name in ("s", "home", "tmp", "config", "cache"):
            safe_directory(self.directory / name)
        with (self.directory / "owner.json").open("x") as marker:
            json.dump(self.identity, marker, sort_keys=True)
        self.environment = browser_environment(self.directory, self.session)
        self.socket = self.directory / "s" / (self.session + ".sock")
        self.pidfile = self.directory / "s" / (self.session + ".pid")
        (self.directory / "s" / (self.session + ".config")).write_text('{"debug":false}')
        self.policy = PublicTargets(release["hosts"])
        try:
            self.proxy = PublicReadProxy(self.directory / "tls", self.policy,
                alive=lambda: not self.closed and not should_stop(), seconds=80, source_url=release["sourceUrl"])
            self.daemon = OwnedProcess([release["cliPath"]], self.directory,
                {**self.environment, "AGENT_BROWSER_DAEMON": "1"}, deadline=self.deadline, browser_only=True)
            until = min(self.deadline, time.monotonic() + 6)
            while not self.socket.exists() and time.monotonic() < until and self.daemon.alive():
                time.sleep(0.05)
            self._check()
        except BaseException:
            self.close()
            raise

    def _check(self):
        from .agent_browser_runtime import read_browser_marker
        if (self.closed or self.should_stop() or time.monotonic() >= self.deadline
                or not self.daemon or not self.daemon.alive() or not self.socket.is_socket()
                or self.socket.is_symlink() or read_browser_marker(self.pidfile).strip() != str(self.daemon.pid)):
            raise PermissionError("原 Work 的独占浏览器身份或执行时限已失效。")

    def _command(self, arguments, *, closing=False):
        self._check()
        result = subprocess.run([self.release["cliPath"], "--session", self.session, *arguments],
            cwd=self.directory, env=self.environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True,
            timeout=min(24, max(0.1, self.deadline - time.monotonic())))
        if result.returncode != 0 or len(result.stdout) > 240000:
            raise ValueError("固定浏览器动作失败，保留原执行，不自动重试。")
        if not closing:
            self._check()
        return result.stdout.decode("utf-8", errors="strict").strip()

    def call(self, arguments, resources):
        self._check()
        if any(self.identity[k] != v for k, v in resources.identity.items()):
            raise PermissionError("浏览器不能跨 Work 使用。")
        if arguments == {"action": "navigate", "url": self.release["sourceUrl"]} and self.url is None:
            self.policy.url(arguments["url"])
            text = self._command(["--executable-path", self.release["chromePath"],
                "--allowed-domains", ",".join(sorted(self.policy.hosts)), "--proxy", f"http://127.0.0.1:{self.proxy.port}",
                "--proxy-bypass", "<-loopback>", "--args", "--ignore-certificate-errors-spki-list=" + self.proxy.spki,
                "open", arguments["url"]])
            current = self._command(["get", "url"])
            if current != arguments["url"]:
                raise ValueError("原 Work 浏览器的最终 URL 与已批准原文不一致。")
            self.url = current
            self.source_response = self._source_response()
            return {"url": current, "result": {"text": text}, "dns": self.policy.dns_snapshot(),
                "proxy_source_response": self.source_response}
        if arguments == {"action": "observe"} and self.url:
            text = self._command(["snapshot"])
            current = self._command(["get", "url"])
            if current != self.url or not text or self._source_response() != self.source_response:
                raise ValueError("浏览器原文或 URL 在采集中改变。")
            return {"url": current, "result": {"text": text}, "dns": self.policy.dns_snapshot(),
                "proxy_source_response": self.source_response}
        raise ValueError("本次仅允许打开一次已选公开原文并读取快照。")

    def _source_response(self):
        responses = self.proxy.source_snapshot()
        if (len(responses) != 1 or responses[0]["url"] != self.release["sourceUrl"]
                or responses[0]["method"] != "GET" or responses[0]["status"] != 200 or responses[0]["bytes"] <= 0
                or responses[0]["peer_ip"] not in responses[0]["validated_addresses"]):
            raise ValueError("原网页快照缺少唯一已通过代理交给浏览器的实际成功响应。")
        return responses[0]

    def close(self):
        if self.shutdown_evidence is not None:
            return self.shutdown_evidence
        normal = False
        errors = []
        try:
            if self.daemon and self.daemon.alive():
                try:
                    message = self._command(["close"], closing=True)
                    self.daemon.process.wait(timeout=min(4, max(0.1, self.deadline - time.monotonic())))
                    normal = "closed" in message.lower() and not self.socket.exists()
                except Exception as error:
                    errors.append(type(error).__name__)
        finally:
            self.closed = True
            held = self.daemon.close() if self.daemon else {"direct_child": "NOT_STARTED"}
            if self.proxy:
                self.proxy.close()
            self.shutdown_evidence = {"normal_browser_close": normal, "socket_removed": not self.socket.exists(),
                "held_process": held, "proxy_closed": self.proxy is None or self.proxy.server.fileno() == -1,
                "descendants": "UNKNOWN", "os_confinement": "NOT_CLAIMED", "errors": errors}
        return self.shutdown_evidence
