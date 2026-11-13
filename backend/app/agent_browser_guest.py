"""Guest protocol dispatcher. The caller provides a separately verified Reader driver."""
from __future__ import annotations

import json

MAX_FRAME = 262144
MAX_RESULT = 16 * 1024 * 1024


class ReaderGuest:
    def __init__(self, identity, nonce, runtime, policy, driver):
        required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
        if not isinstance(identity, dict) or any(not isinstance(identity.get(k), str) or not identity[k] for k in required):
            raise ValueError("Guest requires complete original Work identity")
        if not isinstance(nonce, str) or len(nonce) != 48 or any(c not in "0123456789abcdef" for c in nonce):
            raise ValueError("Guest nonce invalid")
        if any(not isinstance(runtime.get(k), str) or not runtime[k] for k in ("boot_id", "container_id", "image_digest")):
            raise ValueError("Guest runtime binding invalid")
        self.identity, self.nonce, self.runtime = dict(identity), nonce, dict(runtime)
        self.policy, self.driver = policy, driver
        self.sequence, self.tab, self.url, self.started = 0, None, None, False

    def handle(self, frame):
        if not isinstance(frame, dict) or len(json.dumps(frame, ensure_ascii=False).encode()) > MAX_FRAME:
            raise ValueError("Guest request invalid or oversized")
        binding = {"identity":self.identity, "nonce":self.nonce, **{k:self.runtime[k] for k in ("boot_id","container_id","image_digest")}}
        if any(frame.get(k) != v for k,v in binding.items()):
            raise ValueError("Guest request identity mismatch")
        sequence = frame.get("sequence")
        if type(sequence) is not int or sequence != self.sequence + 1:
            raise ValueError("Guest request sequence mismatch")
        action, args = frame.get("action"), frame.get("arguments")
        if not isinstance(args, dict):
            raise ValueError("Guest arguments invalid")
        if action == "start" and args == {} and not self.started:
            result = self.driver.start()
            if result != {"ready":True}:
                raise ValueError("Guest browser connection not verified")
            self.started = True
        elif self.started and action == "navigate" and set(args) == {"url"}:
            self.policy.url(args["url"])
            result = self.driver.navigate(args["url"])
            if not isinstance(result, dict) or not result.get("tab_id"):
                raise ValueError("Guest tab unavailable")
            self.policy.url(result.get("url", ""))
            self.tab, self.url = result["tab_id"], result["url"]
        elif self.started and action in {"observe","extract","screenshot"}:
            expected = {"tab_id", "target_id"} if action == "extract" and "target_id" in args else {"tab_id"}
            if set(args) != expected or self.tab is None or args["tab_id"] != self.tab:
                raise ValueError("Guest action is outside the owned tab")
            result = getattr(self.driver, action)(**args)
            if not isinstance(result, dict) or result.get("tab_id") != self.tab or result.get("url") != self.url:
                raise ValueError("Guest result changed page or tab")
            self.policy.url(result["url"])
        else:
            raise ValueError("Guest action not permitted")
        if len(json.dumps(result, ensure_ascii=False).encode()) > MAX_RESULT:
            raise ValueError("Guest response too large")
        self.sequence = sequence
        return {**binding, "sequence":sequence, "result":result}

    def close(self):
        if self.started:
            self.started = False
            self.driver.close()

def serve_reader(guest, read_fd, write_fd, *, alive=lambda: True, clock=None, seconds=90, handoff=None):
    """Serve one lease; a one-byte handoff receipt becomes 1 when FDs transfer.

    Before transfer the caller retains both FDs. After transfer this function
    closes them even when setup fails; a local close does not prove remote stop.
    """
    import os
    import select
    import stat
    import time
    clock = clock or time.monotonic
    if (type(read_fd) is not int or type(write_fd) is not int or read_fd == write_fd
            or not 0 < seconds <= 90
            or (handoff is not None and (type(handoff) is not bytearray or handoff != b"\x00"))
            or not all(stat.S_ISFIFO(os.fstat(fd).st_mode) for fd in (read_fd, write_fd))):
        raise ValueError("Guest pipe configuration invalid")
    try:
        if handoff is not None:
            handoff[0] = 1
        os.set_blocking(read_fd, False)
        os.set_blocking(write_fd, False)
        deadline, pending = clock() + seconds, bytearray()
        while alive() and clock() < deadline:
            readable, _, _ = select.select([read_fd], [], [], min(0.05, max(0, deadline-clock())))
            if not readable:
                continue
            try:
                chunk = os.read(read_fd, 65536)
            except BlockingIOError:
                continue
            if not chunk:
                return
            pending.extend(chunk)
            if len(pending) > MAX_FRAME:
                raise ValueError("Guest request frame too large")
            while bytes([10]) in pending:
                line, rest = bytes(pending).split(bytes([10]), 1)
                pending = bytearray(rest)
                frame = json.loads(line)
                if not alive() or clock() >= deadline:
                    raise PermissionError("Guest lease stopped before action")
                response = (json.dumps(guest.handle(frame), ensure_ascii=False, separators=(",", ":")) + chr(10)).encode()
                if len(response) > MAX_RESULT:
                    raise ValueError("Guest response frame too large")
                sent = 0
                while sent < len(response):
                    if not alive() or clock() >= deadline:
                        raise PermissionError("Guest lease stopped while responding")
                    _, writable, _ = select.select([], [write_fd], [], min(0.05, max(0, deadline-clock())))
                    if not writable:
                        continue
                    try:
                        count = os.write(write_fd, response[sent:])
                    except BlockingIOError:
                        continue
                    if count <= 0:
                        raise ValueError("Guest response pipe closed")
                    sent += count
    finally:
        if handoff is None or handoff[0] == 1:
            for fd in (read_fd, write_fd):
                try:
                    os.close(fd)
                except OSError:
                    pass
            guest.close()


BSK_LINUX_SHA256 = "00167ad8a2efd44e9eae46c62dcb3a9938a8957b38425401af9043be8818bf58"
EXTENSION_MANIFEST_SHA256 = "60718d7bce02bf94722910ba5bbfdbb4ab5efc4b4c1070a57e69a4298d56c52e"
BSK_PATH = "/opt/curis/bin/bsk"
CHROMIUM_PATH = "/ms-playwright/chromium-1248/chrome-linux-arm64/chrome"
EXTENSION_PATH = "/opt/curis/extension"
RUNTIME_MANIFEST_PATH = "/opt/curis/runtime.playwright.json"
BSK_NAVIGATE_TIMEOUT_MS = 10000
BSK_NAVIGATE_IPC_SECONDS = 13  # Official navigation deadline + 2s response grace + 1s IPC margin.
BSK_IPC_SECONDS = 5



def _linux_worker_preflight():
    import os
    import signal
    import sys
    from pathlib import Path
    if (sys.platform != "linux" or os.geteuid() == 0
            or not callable(getattr(os, "pidfd_open", None))
            or not callable(getattr(signal, "pidfd_send_signal", None))):
        raise PermissionError("Reader needs a non-root Linux worker with pidfd support")
    status = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines() if ":" in line)
    if (status.get("NoNewPrivs", "").strip() != "1"
            or status.get("Seccomp", "").strip() != "2"
            or int(status.get("CapEff", "1").strip(), 16) != 0):
        raise PermissionError("Reader worker process restrictions are missing")
    # Probe permission as well as Python support before creating any owned child.
    pidfd = os.pidfd_open(os.getpid(), 0)
    try:
        signal.pidfd_send_signal(pidfd, 0, None, 0)
    finally:
        os.close(pidfd)
    return Path("/proc/sys/kernel/random/boot_id").read_text().strip()


class LinuxBrowserSkillDriver:
    """Fixed in-container BSK driver. The host must authenticate the container and egress.

    A local BSK connection is not proof of Chromium sandboxing, network isolation,
    or descendant exit. Production and candidate release gates remain separate.
    """
    def __init__(self, identity, nonce, runtime, policy, proxy_spki):
        import hashlib
        import os
        import re
        import time
        from pathlib import Path
        boot = _linux_worker_preflight()
        config = json.loads(Path(RUNTIME_MANIFEST_PATH).read_text())
        if config.get("executionAuthorized") is not True:
            raise PermissionError("Reader product runtime candidate is not released")
        if (type(identity) is not dict or set(identity) != {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
                or any(type(v) is not str or not v for v in identity.values())
                or type(nonce) is not str or not re.fullmatch(r"[0-9a-f]{48}", nonce)
                or type(runtime) is not dict or runtime.get("boot_id") != boot
                or not re.fullmatch(r"[0-9a-f]{64}", str(runtime.get("container_id", "")))
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(runtime.get("image_digest", "")))
                or not re.fullmatch(r"[A-Za-z0-9+/]{43}=", proxy_spki)):
            raise PermissionError("Reader worker binding or proxy pin is invalid")
        for name, expected in [(BSK_PATH, BSK_LINUX_SHA256),
                               (EXTENSION_PATH + "/manifest.json", EXTENSION_MANIFEST_SHA256)]:
            path = Path(name)
            if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise PermissionError("Reader fixed BrowserSkill asset mismatch")
        if not Path(CHROMIUM_PATH).is_file() or Path(CHROMIUM_PATH).is_symlink():
            raise PermissionError("Reader fixed full Chromium is unavailable")
        if config.get("chromiumPath") != CHROMIUM_PATH or config.get("proxyEndpoint") != "http://172.30.253.2:8443":
            raise PermissionError("Reader fixed launch configuration mismatch")
        self.policy, self.nonce = policy, nonce
        self.deadline = time.monotonic() + 88
        self.stop_deadline = self.deadline + 2
        self.root = Path("/tmp/curis-reader")
        self.root.mkdir(mode=0o700)  # Fresh per-Work container tmpfs; never adopt a prior directory.
        for name in ("profile", "state", "tmp"):
            (self.root / name).mkdir(mode=0o700)
        self.environment = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "DISPLAY": ":99",
                            "TMPDIR": str(self.root / "tmp"), "BSK_HOME": str(self.root / "state"),
                            "BSK_AUTO_START": "0", "BSK_AUTO_UPDATE": "off"}
        self.socket_path = self.root / "state/run/daemon.sock"
        self.proxy_spki = proxy_spki
        self.processes, self.session, self.tab, self.browser = [], None, None, None
        self.closed, self.shutdown_evidence = False, None
        self.uid = os.geteuid()

    def _active(self):
        import time
        if self.closed or time.monotonic() >= self.deadline:
            raise PermissionError("Reader worker lease is closed or expired")
        if any(process.poll() is not None for process, _ in self.processes):
            raise PermissionError("Reader owned service exited")

    def _spawn(self, argv):
        import os
        import subprocess
        self._active()
        process = subprocess.Popen(argv, cwd=self.root, env=self.environment, close_fds=True,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        record = [process, None]
        self.processes.append(record)  # Preserve ownership even if acquiring the pidfd fails.
        record[1] = os.pidfd_open(process.pid)
        if process.poll() is not None:
            raise PermissionError("Reader owned service failed during startup")
        return process

    def _rpc(self, method, params, *, stopping=False):
        # A possibly admitted call is never retried. Stop owned resources and reject
        # every subsequent command, including responses arriving after this failure.
        self._rpc_inflight = False
        try:
            return self._exchange(method, params, stopping=stopping)
        except BaseException:
            if not stopping and self._rpc_inflight:
                try:
                    self.close()
                except BaseException:
                    pass
            raise

    def _exchange(self, method, params, *, stopping=False):
        import os
        import secrets
        import socket
        import stat
        import struct
        import time
        if not stopping:
            self._active()
        budget = 0.25 if stopping else (BSK_NAVIGATE_IPC_SECONDS if method == "tool.navigate" else BSK_IPC_SECONDS)
        deadline = min(self.stop_deadline if stopping else self.deadline, time.monotonic() + budget)
        info = self.socket_path.lstat()
        if not stat.S_ISSOCK(info.st_mode) or info.st_uid != self.uid or stat.S_IMODE(info.st_mode) & 0o077:
            raise PermissionError("Reader BSK socket ownership mismatch")
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Reader IPC deadline expired")
            connection.settimeout(min(remaining, 0.25))
            connection.connect(str(self.socket_path))
            pid, uid, _ = struct.unpack("3i", connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            if pid != self.daemon.pid or uid != self.uid or self.daemon.poll() is not None:
                raise PermissionError("Reader BSK peer identity mismatch")
            request_id = secrets.token_hex(16)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Reader IPC deadline expired")
            connection.settimeout(min(remaining, 0.25))
            self._rpc_inflight = not stopping
            connection.sendall((json.dumps({"id": request_id, "method": method, "params": params}) + "\n").encode())
            response = bytearray()
            while b"\n" not in response:
                if not stopping:
                    self._active()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Reader IPC deadline expired")
                connection.settimeout(min(remaining, 0.05))
                try:
                    chunk = connection.recv(65536)
                except socket.timeout:
                    continue  # Recheck original lease/cancellation; never resend the admitted RPC.
                if not chunk or len(response) + len(chunk) > MAX_RESULT:
                    raise ValueError("Reader BSK response invalid or oversized")
                response.extend(chunk)
            line, tail = bytes(response).split(b"\n", 1)
            if tail:
                raise ValueError("Reader BSK returned extra frames")
            from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
            try:
                value = json.loads(line, object_pairs_hook=_unique_json_object,
                                   parse_constant=_invalid_json_constant, parse_float=_finite_json_float)
            except (ValueError, UnicodeError):
                raise ValueError("Reader BSK response JSON_INVALID") from None
            if type(value) is not dict:
                raise ValueError("Reader BSK response TYPE_INVALID")
            if value.get("id") != request_id:
                raise ValueError("Reader BSK response ID_MISMATCH")
            if "error" in value and "result" in value:
                raise ValueError("Reader BSK response BODY_AMBIGUOUS")
            if "error" in value:
                error = value["error"]
                if (type(error) is not dict or type(error.get("code")) is not str
                        or type(error.get("message")) is not str):
                    raise ValueError("Reader BSK response ERROR_INVALID")
                # Fixed BrowserSkill 0.3.3 codes only; never expose message, data or an unknown code.
                codes = {"unknown_method", "unsupported", "invalid_params", "not_found", "permission_denied",
                         "timeout", "cdp_failed", "protocol_error", "cancelled", "user_aborted", "version_too_old",
                         "multiple_browsers_online", "no_browser_connected"}
                code = error["code"] if error["code"] in codes else "other"
                if code == "cdp_failed":
                    data = error.get("data")
                    reasons = {"cdp_extension_access_denied": "CDP_EXTENSION_ACCESS_DENIED",
                               "renderer_read_timeout": "RENDERER_READ_TIMEOUT"}
                    reason = data.get("reason") if type(data) is dict else None
                    reason = reasons.get(reason, "OTHER") if type(reason) is str else "OTHER"
                    page_rejected = error["message"].startswith("Page.navigate rejected: ")
                    net_errors = {"ERR_ABORTED", "ERR_TIMED_OUT", "ERR_BLOCKED_BY_CLIENT", "ERR_CONNECTION_CLOSED",
                                  "ERR_CONNECTION_RESET", "ERR_CONNECTION_REFUSED", "ERR_NAME_NOT_RESOLVED",
                                  "ERR_TUNNEL_CONNECTION_FAILED", "ERR_PROXY_CONNECTION_FAILED",
                                  "ERR_PROXY_CERTIFICATE_INVALID", "ERR_CERT_AUTHORITY_INVALID", "ERR_EMPTY_RESPONSE"}
                    detail = error["message"].removeprefix("Page.navigate rejected: ") if page_rejected else ""
                    net = detail.removeprefix("net::") if detail.startswith("net::") else "OTHER"
                    net = net if net in net_errors else "OTHER"
                    raise ValueError("Reader BSK RPC_ERROR_cdp_failed REASON=" + reason
                                     + " PAGE_NAVIGATE_REJECTED=" + ("YES" if page_rejected else "NO") + " NET=" + net)
                raise ValueError("Reader BSK RPC_ERROR_" + code)
            if "result" not in value:
                raise ValueError("Reader BSK response RESULT_MISSING")
            if not stopping:
                self._active()
            self._rpc_inflight = False
            return value["result"]

    def start(self):
        import time
        try:
            self.daemon = self._spawn([BSK_PATH, "daemon", "start", "--mode", "local", "--port", "52800",
                                      "--foreground", "--daemon-idle", "2m", "--session-idle", "2m"])
            self._spawn(["/usr/bin/Xvfb", ":99", "-screen", "0", "1280x800x24", "-nolisten", "tcp"])
            self._spawn([CHROMIUM_PATH, "--user-data-dir=" + str(self.root / "profile"),
                         "--no-first-run", "--no-default-browser-check", "--disable-sync",
                         "--disable-background-networking", "--disable-quic",
                         "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE 172.30.253.2",
                         "--proxy-server=http://172.30.253.2:8443", "--proxy-bypass-list=<-loopback>;127.0.0.1:52800",
                         "--ignore-certificate-errors-spki-list=" + self.proxy_spki,
                         "--disable-extensions-except=" + EXTENSION_PATH, "--load-extension=" + EXTENSION_PATH, "about:blank"])
            ready_deadline = min(self.deadline, time.monotonic() + 10)
            while True:
                self._active()
                try:
                    status = self._rpc("system.status", {})
                    browsers = status.get("browsers", [])
                    if (status.get("pid") != self.daemon.pid or status.get("daemon_version") != "0.3.3"
                            or len(browsers) != 1 or browsers[0].get("extension_version") != "0.3.3"
                            or browsers[0].get("unresponsive") or browsers[0].get("version_skew")):
                        raise ValueError("Reader fixed extension is not connected")
                    self.browser = browsers[0]["instance_id"]
                    break
                except FileNotFoundError:
                    pass
                except (TimeoutError, ConnectionRefusedError):
                    pass
                except ValueError:
                    # No fresh daemon or session is spawned on a readiness mismatch.
                    if time.monotonic() >= ready_deadline:
                        raise
                if time.monotonic() >= ready_deadline:
                    raise TimeoutError("Reader extension readiness deadline exceeded")
                time.sleep(0.05)
            started = self._rpc("session.start", {"browser_instance_id": self.browser, "focused": False})
            if (type(started) is not dict or type(started.get("session_id")) is not str
                    or not started["session_id"] or len(started["session_id"]) > 256
                    or started.get("browser_instance_id") != self.browser):
                raise ValueError("Reader session binding was not verified")
            self.session = started["session_id"]  # Daemon allocates the actual session ID.
            if type(started.get("agent_window_id")) is not int:
                raise ValueError("Reader Agent Window was not verified")
            self._active()
            return {"ready": True}
        except BaseException:
            try:
                self.close()
            except BaseException:
                pass
            raise

    def _url(self, tab_id):
        tabs = self._rpc("tool.tab_list", {"session_id": self.session, "scope": "agent"}).get("tabs", [])
        owned = [tab for tab in tabs if tab.get("tab_id") == tab_id and tab.get("scope") == "agent"]
        if len(owned) != 1:
            raise PermissionError("Reader tab ownership changed")
        url = owned[0].get("url", "")
        self.policy.url(url)
        return url

    def navigate(self, url):
        self.policy.url(url)
        value = self._rpc("tool.navigate", {"session_id": self.session, "url": url, "wait_until": "domcontentloaded",
                                            "timeout_ms": BSK_NAVIGATE_TIMEOUT_MS, **({"tab_id": self.tab} if self.tab else {})})
        if (type(value) is not dict or type(value.get("reached")) is not str
                or value["reached"] not in {"commit", "domcontentloaded", "load", "networkidle"}
                or value.get("error_text")):
            raise ValueError("Reader navigation did not reach its target")
        self.policy.url(value.get("final_url") or value.get("url", ""))
        tab = value["tab_id"]
        final_url = self._url(tab)
        self.tab = tab
        return {"tab_id": tab, "url": final_url}

    def _read(self, operation, tab_id, **options):
        if not self.session or tab_id != self.tab:
            raise PermissionError("Reader action is outside its owned session/tab")
        before = self._url(tab_id)
        params = {"session_id": self.session, "tab_id": tab_id, **options}
        value = self._rpc("tool." + operation, params)
        if value.get("tab_id", tab_id) != tab_id or self._url(tab_id) != before:
            raise PermissionError("Reader page changed during capture")
        return {**value, "tab_id": tab_id, "url": before}

    def observe(self, tab_id):
        return self._read("observe", tab_id, max_tokens=6000, max_depth=8, probe_hover=False)

    def extract(self, tab_id, target_id=None):
        return self._read("extract", tab_id, action="table" if target_id else "discover",
                          **({"target_id": target_id} if target_id else {}), max_rows=200, max_columns=30,
                          max_bytes=131072, timeout_ms=5000)

    def screenshot(self, tab_id):
        import base64
        value = self._read("screenshot", tab_id)
        if value.get("format") != "png":
            raise ValueError("Reader screenshot format mismatch")
        raw = base64.b64decode(value["image_base64"], validate=True)
        if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Reader screenshot is not PNG")
        return value

    def close(self):
        import os
        import signal
        import subprocess
        import time
        if self.shutdown_evidence is not None:
            return self.shutdown_evidence.copy()
        self.closed = True
        evidence = {"bsk_session": "UNKNOWN", "direct_children": "UNKNOWN", "descendants": "UNKNOWN", "effects": "UNKNOWN"}
        interruption = None
        stop_deadline = min(self.stop_deadline, time.monotonic() + 2)
        try:
            if self.session and time.monotonic() < stop_deadline:
                try:
                    result = self._rpc("session.stop", {"session_id": self.session}, stopping=True)
                    # Local daemon IPC uses the CLI-facing result, unlike extension WS.
                    if (type(result) is dict and result.get("stopped") == [self.session]
                            and result.get("return_failures", []) == [] and result.get("failed", []) == []):
                        evidence["bsk_session"] = "STOP_RETURNED"
                except BaseException as error:
                    if not isinstance(error, Exception):
                        interruption = error
            exited = True
            for process, pidfd in reversed(self.processes):
                try:
                    if process.poll() is None:
                        if pidfd is None:
                            exited = False
                            continue
                        signal.pidfd_send_signal(pidfd, signal.SIGTERM)
                        try:
                            process.wait(timeout=min(0.2, max(0, stop_deadline - time.monotonic())))
                        except subprocess.TimeoutExpired:
                            signal.pidfd_send_signal(pidfd, signal.SIGKILL)
                            process.wait(timeout=max(0, stop_deadline - time.monotonic()))
                    exited = exited and process.poll() is not None
                except BaseException as error:
                    exited = False
                    if not isinstance(error, Exception) and interruption is None:
                        interruption = error
                finally:
                    if pidfd is not None:
                        try:
                            os.close(pidfd)
                        except BaseException as error:
                            exited = False
                            if not isinstance(error, Exception) and interruption is None:
                                interruption = error
            if exited:
                evidence["direct_children"] = "EXITED"
        finally:
            self.shutdown_evidence = evidence
        if interruption is not None:
            raise interruption
        return evidence.copy()


def main():
    """One bounded bootstrap over the host-owned private stdin/stdout channel."""
    import os
    import select
    import sys
    import time
    from pathlib import Path
    if sys.argv[1:] != ["--stdio"]:
        raise ValueError("Reader worker requires its fixed stdio entrypoint")
    _linux_worker_preflight()
    from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
    deadline, pending = time.monotonic() + 5, bytearray()
    while b"\n" not in pending:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([sys.stdin.fileno()], [], [], remaining)[0]:
            raise TimeoutError("Reader bootstrap deadline expired")
        chunk = os.read(sys.stdin.fileno(), MAX_FRAME + 1 - len(pending))
        if not chunk or len(pending) + len(chunk) > MAX_FRAME:
            raise ValueError("Reader bootstrap invalid or oversized")
        pending.extend(chunk)
    line, tail = bytes(pending).split(b"\n", 1)
    if tail:
        raise ValueError("Reader bootstrap must be a separate frame")
    bootstrap = json.loads(line, object_pairs_hook=_unique_json_object,
                           parse_constant=_invalid_json_constant, parse_float=_finite_json_float)
    if type(bootstrap) is not dict or set(bootstrap) != {"identity", "nonce", "runtime", "hosts", "proxy_spki"}:
        raise ValueError("Reader bootstrap binding is incomplete")
    from .agent_browser_policy import PublicTargets
    policy = PublicTargets(bootstrap["hosts"])
    driver = LinuxBrowserSkillDriver(bootstrap["identity"], bootstrap["nonce"], bootstrap["runtime"], policy, bootstrap["proxy_spki"])
    guest = ReaderGuest(bootstrap["identity"], bootstrap["nonce"], bootstrap["runtime"], policy, driver)
    try:
        ack = {"identity": dict(bootstrap["identity"]), "nonce": bootstrap["nonce"], "sequence": 0,
               **{k: bootstrap["runtime"][k] for k in ("boot_id", "container_id", "image_digest")},
               "result": {"bootstrapped": True, "browser_started": False}}
        output = memoryview((json.dumps(ack, separators=(",", ":")) + "\n").encode())
        os.set_blocking(sys.stdout.fileno(), False)
        ack_deadline = time.monotonic() + 1
        while output:
            remaining = ack_deadline - time.monotonic()
            if remaining <= 0 or not select.select([], [sys.stdout.fileno()], [], remaining)[1]:
                raise TimeoutError("Reader bootstrap acknowledgement deadline expired")
            try:
                written = os.write(sys.stdout.fileno(), output)
            except BlockingIOError:
                continue
            if written <= 0:
                raise ValueError("Reader bootstrap response pipe closed")
            output = output[written:]
        serve_reader(guest, sys.stdin.fileno(), sys.stdout.fileno(), seconds=88,
                     alive=lambda: not driver.closed and time.monotonic() < driver.deadline)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
