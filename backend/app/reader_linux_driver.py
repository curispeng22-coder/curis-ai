"""Candidate Linux BrowserSkill 0.3.3 driver; not a platform verifier.

The caller must supply an independently verified, Work-owned environment.
The production service has no such provider yet and deliberately fails closed.
"""
import base64
import json
import math
import secrets
import socket
import struct
import time

MAX_REPLY = 12 * 1024 * 1024


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite JSON number")
    return number


class LinuxReaderDriver:
    """One daemon session and one agent tab, with no browser process launch."""

    def __init__(self, environment, policy):
        self.env, self.policy = environment, policy
        self.session = self.browser = self.tab = self.url = None
        self.state = "NEW"

    def _check(self):
        if self.state in {"UNKNOWN", "CLOSED"} or self.env.verify() is not True:
            raise PermissionError("Linux reader ownership or egress is unverified")

    def _rpc(self, method, params):
        self._check()
        request_id = secrets.token_hex(16)
        data = (json.dumps({"id": request_id, "method": method, "params": params},
                           separators=(",", ":"), allow_nan=False) + "\n").encode()
        deadline = time.monotonic() + 15
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
                conn.settimeout(max(0.001, deadline - time.monotonic()))
                conn.connect(self.env.daemon_socket)
                # Linux SO_PEERCRED authenticates this UDS peer only, not the WS peer.
                pid, uid, gid = struct.unpack("3i", conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
                if self.env.verify_daemon_peer(pid, uid, gid) is not True:
                    raise PermissionError("daemon peer is not owned")
                self._check()
                conn.sendall(data)
                response = bytearray()
                while b"\n" not in response:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError("daemon response timeout")
                    conn.settimeout(remaining)
                    chunk = conn.recv(min(65536, MAX_REPLY + 1 - len(response)))
                    if not chunk:
                        raise ValueError("daemon response truncated")
                    response.extend(chunk)
                    if len(response) > MAX_REPLY:
                        raise ValueError("daemon response too large")
                line, trailing = bytes(response).split(b"\n", 1)
                if trailing:
                    raise ValueError("unexpected trailing daemon frame")
                result = json.loads(line.decode("utf-8"), object_pairs_hook=_object, parse_float=_finite_float,
                                    parse_constant=lambda _: (_ for _ in ()).throw(ValueError("invalid JSON")))
                if (not isinstance(result, dict) or result.get("id") != request_id
                        or "result" not in result or "error" in result):
                    raise ValueError("invalid daemon response")
                self._check()
                if not isinstance(result["result"], dict):
                    raise ValueError("invalid daemon result")
                return result["result"]
        except BaseException:
            self.state = "UNKNOWN"
            raise

    def _status(self):
        status = self._rpc("system.status", {})
        browsers = status.get("browsers")
        if (status.get("pid") != self.env.daemon_pid or status.get("daemon_version") != "0.3.3"
                or not isinstance(browsers, list) or len(browsers) != 1
                or not isinstance(browsers[0], dict) or browsers[0].get("extension_version") != "0.3.3"
                or browsers[0].get("unresponsive") or browsers[0].get("version_skew")
                or not isinstance(browsers[0].get("instance_id"), str)
                or not browsers[0]["instance_id"]):
            raise ValueError("browser connection is not verified")
        browser = browsers[0]["instance_id"]
        if self.env.verify_browser(browser) is not True:
            raise PermissionError("browser and extension ownership is unverified")
        return browser

    def start(self):
        if self.state != "NEW":
            raise ValueError("reader already started")
        try:
            self.browser = self._status()
            reply = self._rpc("session.start", {"browser_instance_id": self.browser, "focused": False})
            self.session = reply.get("session_id")
            if (not isinstance(self.session, str) or not self.session
                    or reply.get("browser_instance_id") != self.browser):
                raise ValueError("session ownership mismatch")
            self.state = "OPEN"
            return {"ready": True}
        except BaseException:
            self.state = "UNKNOWN"
            raise

    def _current_url(self):
        result = self._rpc("tool.tab_list", {"session_id": self.session, "scope": "agent"})
        tabs = result.get("tabs")
        if not isinstance(tabs, list):
            raise ValueError("invalid tab list")
        matches = [t for t in tabs if isinstance(t, dict) and t.get("tab_id") == self.tab
                   and t.get("scope") == "agent"]
        if len(matches) != 1 or not isinstance(matches[0].get("url"), str):
            raise ValueError("tab is not owned by the session")
        self.policy.url(matches[0]["url"])
        return matches[0]["url"]

    def _ready(self):
        if self.state != "OPEN" or self._status() != self.browser:
            raise PermissionError("reader session is not active")

    def navigate(self, url):
        try:
            self._ready()
            self.policy.url(url)
            params = {"session_id": self.session, "url": url, "wait_until": "domcontentloaded", "timeout_ms": 10000}
            if self.tab is not None:
                params["tab_id"] = self.tab
            result = self._rpc("tool.navigate", params)
            tab, final = result.get("tab_id"), result.get("final_url") or result.get("url")
            if (type(tab) is not int or tab < 0 or not isinstance(final, str)
                    or result.get("reached") != "domcontentloaded" or result.get("error_text")):
                raise ValueError("invalid navigation result")
            self.policy.url(final)
            if self.tab is not None and self.tab != tab:
                raise ValueError("navigation changed owned tab")
            self.tab, self.url = tab, final
            if self._current_url() != final:
                raise ValueError("navigation URL changed")
            return {"tab_id": tab, "url": final}
        except BaseException:
            self.state = "UNKNOWN"
            raise

    def _read(self, method, tab_id, extra):
        try:
            self._ready()
            if type(tab_id) is not int or tab_id != self.tab or self._current_url() != self.url:
                raise ValueError("reader tab changed")
            result = self._rpc(method, {"session_id": self.session, "tab_id": tab_id, **extra})
            if result.get("tab_id", tab_id) != tab_id or self._current_url() != self.url:
                raise ValueError("reader result changed tab or URL")
            return {**result, "tab_id": tab_id, "url": self.url}
        except BaseException:
            self.state = "UNKNOWN"
            raise

    def observe(self, tab_id):
        return self._read("tool.observe", tab_id, {"max_tokens": 6000, "max_depth": 8, "probe_hover": False})

    def extract(self, tab_id, target_id=None):
        if target_id is not None and (not isinstance(target_id, str) or not target_id or len(target_id) > 512):
            raise ValueError("invalid extraction target")
        extra = {"action": "table" if target_id else "discover", "max_rows": 200,
                 "max_columns": 30, "max_bytes": 131072, "timeout_ms": 5000}
        if target_id:
            extra["target_id"] = target_id
        return self._read("tool.extract", tab_id, extra)

    def screenshot(self, tab_id):
        result = self._read("tool.screenshot", tab_id, {})
        try:
            image = base64.b64decode(result.get("image_base64", ""), validate=True)
            if result.get("format") != "png" or not image.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("invalid screenshot")
            return result
        except BaseException:
            self.state = "UNKNOWN"
            raise

    def close(self):
        if self.state == "CLOSED":
            return
        if self.state != "OPEN" or not self.session:
            self.state = "UNKNOWN"
            return
        try:
            result = self._rpc("session.stop", {"session_id": self.session, "all": False})
            if (result.get("stopped") != [self.session]
                    or type(result.get("failed", [])) is not list or result.get("failed", [])
                    or type(result.get("return_failures", [])) is not list or result.get("return_failures", [])):
                raise ValueError("session stop not confirmed")
            self.state = "CLOSED"
        except BaseException:
            self.state = "UNKNOWN"
            raise
