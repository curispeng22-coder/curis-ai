import socket
from email.message import Message
from types import SimpleNamespace
import pytest
from app.agent_browser import BrowserLease, PublicTargets


def resolved(address):
    ip6 = ":" in address
    return [(socket.AF_INET6 if ip6 else socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "",
             (address, 443, 0, 0) if ip6 else (address, 443))]


@pytest.mark.parametrize("address", ["127.0.0.1", "10.2.3.4", "169.254.169.254", "192.168.1.1",
                                    "::1", "fc00::1", "64:ff9b::c0a8:101", "::ffff:8.8.8.8"])
def test_public_dns_cannot_rebind_to_private_or_transition_targets(address):
    policy = PublicTargets(["example.com"], resolver=lambda *args, **kwargs: resolved(address))
    with pytest.raises(ValueError):
        policy.resolve("example.com")


def test_explicit_host_and_public_ip_must_both_match_before_connection():
    addresses = resolved("93.184.216.34")
    policy = PublicTargets(["example.com"], resolver=lambda *args, **kwargs: addresses)
    assert policy.resolve("example.com") == addresses
    for url in ["http://example.com/", "https://example.com:444/", "https://example.com.evil.org/",
                "https://user:password@example.com/", "https://127.0.0.1/",
                "https://example.com/?access_token=private", "https://example.com/#access_token=private"]:
        with pytest.raises(ValueError):
            policy.url(url)
    assert policy.url("https://example.com/public#section") == "example.com"
    mixed = PublicTargets(["example.com"], resolver=lambda *a, **kw: addresses + resolved("127.0.0.1"))
    with pytest.raises(ValueError):
        mixed.resolve("example.com")


def dns_body(*, host="example.com", data="93.184.216.34", status=0, answer_type=1):
    import json
    return json.dumps({"Status": status, "Question": [{"name": host, "type": 1}],
        "Answer": [{"name": host, "type": answer_type, "data": data}]}).encode()


def test_only_all_benchmark_system_answers_use_fixed_bootstrap():
    calls = []
    def bootstrap(host):
        calls.append(host)
        return resolved("93.184.216.34")
    policy = PublicTargets(["example.com"], resolver=lambda *a, **kw: resolved("198.18.16.11") + resolved("198.19.1.2"),
        bootstrap=bootstrap)
    assert policy.resolve("example.com") == resolved("93.184.216.34") and calls == ["example.com"]
    assert policy.dns_snapshot()[0]["method"] == "PINNED_DOH_BENCHMARK_BOOTSTRAP"
    assert policy.dns_snapshot()[0]["bootstrap_ip"] == "1.1.1.1"
    with pytest.raises(ValueError):
        policy.resolve("cloudflare-dns.com")
    assert calls == ["example.com"]
    normal = PublicTargets(["example.com"], resolver=lambda *a, **kw: resolved("93.184.216.34"), bootstrap=bootstrap)
    normal.resolve("example.com")
    assert calls == ["example.com"] and normal.dns_snapshot()[0]["method"] == "SYSTEM_PUBLIC"


@pytest.mark.parametrize("addresses", [
    [], resolved("198.18.16.11") + resolved("93.184.216.34"),
    resolved("198.18.16.11") + resolved("10.0.0.1"),
    resolved("127.0.0.1"), resolved("169.254.169.254"), resolved("192.168.1.1"),
    resolved("240.0.0.1"), resolved("224.0.0.1"), resolved("ff02::1"),
])
def test_mixed_private_reserved_or_empty_dns_never_uses_bootstrap(addresses):
    calls = []
    policy = PublicTargets(["example.com"], resolver=lambda *a, **kw: addresses,
        bootstrap=lambda host: calls.append(host))
    with pytest.raises(ValueError):
        policy.resolve("example.com")
    assert calls == [] and policy.dns_snapshot() == []


@pytest.mark.parametrize("addresses", [resolved("10.0.0.1"), resolved("127.0.0.1"),
    resolved("198.18.16.11"), resolved("64:ff9b::c0a8:101"), resolved("::ffff:8.8.8.8"), []])
def test_bootstrap_results_still_pass_the_original_public_ip_boundary(addresses):
    policy = PublicTargets(["example.com"], resolver=lambda *a, **kw: resolved("198.18.16.11"),
        bootstrap=lambda host: addresses)
    with pytest.raises(ValueError):
        policy.resolve("example.com")
    assert policy.dns_snapshot() == []


@pytest.mark.parametrize("response", [(302, dns_body()), (500, dns_body()), (200, b"x" * 65537),
    (200, b"not json"), (200, b"[]"), (200, dns_body(status=3)), (200, dns_body(status=False)),
    (200, dns_body(host="unapproved.example")), (200, dns_body(data="10.0.0.1")),
    (200, dns_body(data="198.18.1.1")), (200, dns_body(data="224.0.0.1")),
    (200, dns_body(data="::ffff:8.8.8.8")), (200, dns_body(data="2001:4860:4860::8888", answer_type=28)),
    (200, dns_body(data="canonical.example.com", answer_type=5)),
    (200, b'{"Status":0,"Question":[{"name":"example.com","type":1}],"Answer":[]}'),
])
def test_pinned_dns_rejects_bad_transport_or_answer_without_redirect_or_private_fallback(response):
    from app.agent_browser import pinned_public_dns
    calls = []
    def exchange(host):
        calls.append(host)
        return response
    with pytest.raises(ValueError):
        pinned_public_dns("example.com", exchange=exchange)
    assert calls == ["example.com"]


def test_pinned_dns_timeout_is_closed_and_valid_answer_is_literal():
    from app.agent_browser import pinned_public_dns
    def timeout(host):
        raise TimeoutError("self-authored timeout")
    with pytest.raises(ValueError):
        pinned_public_dns("example.com", exchange=timeout)
    assert pinned_public_dns("example.com", exchange=lambda host: (200, dns_body())) == resolved("93.184.216.34")


def test_fixed_dns_transport_uses_one_ip_verified_sni_and_no_account_headers(monkeypatch):
    import ssl
    import app.agent_browser as module
    events = []
    class Connection:
        def settimeout(self, value): events.append(("timeout", value))
        def connect(self, address): events.append(("connect", address))
        def do_handshake(self): events.append(("handshake", True))
        def sendall(self, data): events.append(("request", data.decode()))
        def shutdown(self, how): pass
        def close(self): pass
    connection = Connection()
    class Context:
        check_hostname, verify_mode = True, ssl.CERT_REQUIRED
        def wrap_socket(self, raw, **kwargs):
            assert raw is connection
            events.append(("tls", kwargs))
            return raw
    class Response:
        status = 200
        def __init__(self, secure): assert secure is connection
        def begin(self): pass
        def read(self, maximum):
            assert maximum == 65537
            return dns_body()
    def context(**kwargs):
        events.append(("ca", kwargs))
        return Context()
    monkeypatch.setattr(module.socket, "socket", lambda *a: connection)
    monkeypatch.setattr(module.ssl, "create_default_context", context)
    monkeypatch.setattr(module.http.client, "HTTPResponse", Response)
    assert module.pinned_public_dns("example.com") == resolved("93.184.216.34")
    assert ("connect", ("1.1.1.1", 443)) in events
    assert ("tls", {"server_hostname": "cloudflare-dns.com", "do_handshake_on_connect": False}) in events
    assert ("ca", {"cafile": module.certifi.where()}) in events
    request = next(value for key, value in events if key == "request")
    assert request.startswith("GET /dns-query?name=example.com&type=A HTTP/1.1\r\n")
    assert "Host: cloudflare-dns.com\r\n" in request
    assert "authorization" not in request.lower() and "cookie" not in request.lower()


def headers(**extra):
    result = Message()
    result["Host"] = "example.com"
    result["Cookie"] = "fixture-cookie"
    result["Authorization"] = "Bearer fixture"
    result["X-Session-Token"] = "fixture"
    result["Accept"] = "text/html"
    for key, value in extra.items():
        result[key] = value
    return result


def test_proxy_enforces_read_methods_and_strips_all_account_headers():
    policy = PublicTargets(["example.com"])
    sent, length = policy.request("example.com", "GET", "/public", headers())
    assert sent == {"Accept": "text/html"} and length == 0
    for method in ["POST", "PUT", "PATCH", "DELETE", "CONNECT"]:
        with pytest.raises(ValueError):
            policy.request("example.com", method, "/public", headers())
    for extra in [{"Content-Length": "1"}, {"Upgrade": "websocket"}, {"Transfer-Encoding": "chunked"}]:
        with pytest.raises(ValueError):
            policy.request("example.com", "GET", "/public", headers(**extra))


def test_browser_tools_bind_original_work_and_never_offer_actions_or_scripts():
    lease = object.__new__(BrowserLease)
    lease.identity = {"tenant_id": "tenant", "company_id": "company", "work_ref": "work", "task_id": "task"}
    lease.browser_id = "owned-browser"
    lease._session_started = True
    lease.connected = lambda: "owned-browser"
    lease.tab, lease.session = None, "owned-session"
    lease.policy = PublicTargets(["example.com"])
    calls = []
    visible = {"url": "https://example.com/public", "scope": "agent"}
    def rpc(method, params):
        calls.append((method, params))
        if method == "tool.navigate":
            return {"tab_id": 7, "url": params["url"], "final_url": params["url"], "reached": "domcontentloaded"}
        if method == "tool.tab_list":
            return {"tabs": [{"tab_id": 7, **visible}]}
        return {"tab_id": 7, "text": "Public fixture content"}
    lease.rpc = rpc
    resources = SimpleNamespace(identity=lease.identity)
    assert lease.call({"action": "navigate", "url": "https://example.com/public"}, resources)["tab_id"] == 7
    assert lease.call({"action": "observe"}, resources)["result"]["text"] == "Public fixture content"
    assert next(params for method, params in calls if method == "tool.observe")["probe_hover"] is False
    before_rejected = len(calls)
    for action in ["click", "type", "evaluate", "upload", "download", "login"]:
        with pytest.raises(ValueError):
            lease.call({"action": action}, resources)
    with pytest.raises(ValueError):
        lease.call({"action": "observe"}, SimpleNamespace(identity={**lease.identity, "work_ref": "foreign-work"}))
    assert len(calls) == before_rejected
    for changes in [{"url": "https://foreign.example/private"}, {"url": "chrome://history"},
                    {"url": "https://example.com/public", "scope": "user"}]:
        visible.update(changes)
        with pytest.raises(ValueError):
            lease.call({"action": "observe"}, resources)
        assert calls[-1][0] == "tool.tab_list"


def test_bundled_browser_tool_needs_no_workspace_path_and_rejects_tampering(tmp_path, monkeypatch):
    import hashlib
    import app.agent_browser as module
    monkeypatch.setattr(module.sys, "_MEIPASS", str(tmp_path), raising=False)
    binary = tmp_path / "vendor/browser-skill/bsk"
    binary.parent.mkdir(parents=True)
    binary.write_bytes(b"self-authored vendor fixture, never executed")
    binary.chmod(0o700)
    monkeypatch.setattr(module, "BSK_SHA256", hashlib.sha256(binary.read_bytes()).hexdigest())
    assert module.managed_browser_tool({}) == binary
    with pytest.raises(ValueError):
        module.managed_browser_tool({"browser_skill_path": "relative/bsk"})
    linked = tmp_path / "linked-bsk"
    linked.symlink_to(binary)
    with pytest.raises(ValueError):
        module.managed_browser_tool({"browser_skill_path": str(linked)})
    binary.write_bytes(b"tampered fixture")
    with pytest.raises(ValueError):
        module.managed_browser_tool({})

def test_tls_uses_only_owned_config_and_cleans_key_after_success(tmp_path, monkeypatch):
    import base64
    import hashlib
    import app.agent_browser as module
    directory = tmp_path / "tls"
    calls = []
    loaded = []
    monkeypatch.setenv("OPENSSL_CONF", "/self-authored-forbidden-parent.cnf")
    monkeypatch.setenv("DYLD_LIBRARY_PATH", "/self-authored-parent-libraries")
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-never-forwarded")
    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        assert kwargs["env"] == {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8",
                                 "OPENSSL_CONF": str(directory / "request.cnf")}
        assert argv[:4] == ["/usr/bin/sandbox-exec", "-f", str(directory / "crypto.sb"), "/usr/bin/openssl"]
        assert kwargs["cwd"] == directory and kwargs["check"] is True
        if argv[4] == "req":
            (directory / "key.pem").write_text("self-authored fake key; no crypto invoked")
            (directory / "cert.pem").write_text("self-authored fake certificate")
            assert kwargs["stderr"] == module.subprocess.PIPE
            return SimpleNamespace(stdout=b"")
        if argv[4] == "x509":
            return SimpleNamespace(stdout=b"self-authored public fixture")
        assert argv[4] == "pkey" and kwargs["input"] == b"self-authored public fixture"
        return SimpleNamespace(stdout=b"self-authored DER fixture")
    class Context:
        def load_cert_chain(self, cert, key):
            assert key.stat().st_mode & 0o777 == 0o600
            loaded.append((cert, key))
        def set_alpn_protocols(self, protocols):
            assert protocols == ["http/1.1"]
    context = Context()
    monkeypatch.setattr(module.subprocess, "run", run)
    monkeypatch.setattr(module.ssl, "SSLContext", lambda protocol: context)
    actual, pin = module.tls_certificate(directory, ["example.com"])
    assert actual is context and loaded == [(directory / "cert.pem", directory / "key.pem")]
    assert pin == base64.b64encode(hashlib.sha256(b"self-authored DER fixture").digest()).decode()
    assert [argv[4] for argv, _ in calls] == ["req", "x509", "pkey"]
    assert not (directory / "key.pem").exists()
    profile = (directory / "crypto.sb").read_text()
    assert "(deny network*)" in profile and "(deny file-read-data)" in profile
    assert "/private/etc" not in profile and "/self-authored-parent" not in profile
    assert "subjectAltName=DNS:example.com" in (directory / "request.cnf").read_text()


@pytest.mark.parametrize("stage", ["req", "x509", "pkey"])
@pytest.mark.parametrize("failure", ["exit", "timeout"])
def test_tls_failure_is_safe_stops_commands_and_removes_partial_key(tmp_path, monkeypatch, stage, failure):
    import app.agent_browser as module
    directory = tmp_path / "tls"
    calls = []
    private_diagnostic = b"self-authored diagnostic that must not enter the API response"
    def run(argv, **kwargs):
        calls.append(argv[4])
        if argv[4] == "req":
            (directory / "key.pem").write_text("self-authored partial key")
        if argv[4] == stage:
            if failure == "exit":
                raise module.subprocess.CalledProcessError(1, argv, stderr=private_diagnostic)
            raise module.subprocess.TimeoutExpired(argv, kwargs["timeout"], stderr=private_diagnostic)
        return SimpleNamespace(stdout=b"self-authored public fixture")
    monkeypatch.setattr(module.subprocess, "run", run)
    with pytest.raises(ValueError, match="本地安全连接") as captured:
        module.tls_certificate(directory, ["example.com"])
    assert private_diagnostic.decode() not in str(captured.value)
    assert isinstance(captured.value.__cause__, module.subprocess.SubprocessError)
    assert calls == ["req", "x509", "pkey"][:["req", "x509", "pkey"].index(stage) + 1]
    assert not (directory / "key.pem").exists()

@pytest.mark.parametrize("failure", [None, "chrome", "service", "cancel"])
def test_browser_startup_is_scoped_checked_and_cleans_up_early_exit(tmp_path, monkeypatch, failure):
    import hashlib
    import itertools
    import json
    from pathlib import Path
    import threading
    import app.agent_browser as module

    real_directory = module.safe_directory
    def directory(path):
        path = Path(path)
        if path.parent == Path("/private/tmp") and path.name.startswith("curis-browser-"):
            path = tmp_path / "state"
        return real_directory(path)
    monkeypatch.setattr(module, "safe_directory", directory)
    monkeypatch.setattr(module, "_LEASE_LOCK", threading.Lock())
    ticks = itertools.count()
    monkeypatch.setattr(module.time, "monotonic", lambda: next(ticks) / 10)
    monkeypatch.setattr(module.time, "sleep", lambda seconds: None)
    monkeypatch.setenv("MAC_CHROMIUM_TMPDIR", "/self-authored-unapproved-parent")
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-not-forwarded")
    bsk = tmp_path / "bsk"
    bsk.write_bytes(b"self-authored BSK fixture, never executed")
    monkeypatch.setattr(module, "BSK_SHA256", hashlib.sha256(bsk.read_bytes()).hexdigest())
    monkeypatch.setattr(module, "managed_browser_tool", lambda metadata: bsk)
    chrome = tmp_path / "Chrome.app/Contents/MacOS/Chrome"
    chrome.parent.mkdir(parents=True)
    chrome.write_text("self-authored Chrome fixture, never executed")
    class Probe:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def bind(self, address): assert address == ("127.0.0.1", module.WS_PORT)
    monkeypatch.setattr(module.socket, "socket", lambda *args: Probe())
    proxy_closed = []
    class Proxy:
        port, spki = 18001, "self-authored-spki"
        def __init__(self, *args, **kwargs): pass
        def close(self): proxy_closed.append(True)
    monkeypatch.setattr(module, "PublicReadProxy", Proxy)
    processes, closed = [], []
    class Process:
        def __init__(self, command, cwd, environment, *, deadline):
            assert deadline > 0
            self.kind = "service" if "daemon" in command else "chrome"
            self.pid = 101 if self.kind == "service" else 102
            self.checks = 0
            processes.append((self.kind, command, environment, self))
            if self.kind == "service":
                (cwd / "daemon.json").write_text(json.dumps({"pid": self.pid, "ws_port": module.WS_PORT,
                    "version": "0.3.3", "host_managed": True, "sock_path": str(cwd / "run/daemon.sock")}))
        def alive(self):
            self.checks += 1
            return not (failure == self.kind and self.checks >= 2)
        def close(self):
            closed.append(self.kind)
            return {"supervisor": "EXITED", "direct_child": "EXITED", "descendants": "UNKNOWN", "effects": "UNKNOWN"}
    monkeypatch.setattr(module, "OwnedProcess", Process)
    def start():
        return module.BrowserLease(tmp_path / "browser", {"tenant_id": "tenant", "company_id": "company"},
            {"browser_chrome_path": str(chrome)}, [], setup=True, alive=lambda: failure != "cancel")
    if failure:
        with pytest.raises(ValueError, match="连接尚未核验"):
            start()
        assert sorted(closed) == ["chrome", "service"] and proxy_closed == [True]
        assert not module._LEASE_LOCK.locked()
    else:
        lease = start()
        assert all(process.checks >= 2 for _, _, _, process in processes)
        # Alive startup is still not BrowserSkill connection or a verified visible window.
        assert lease.setup and not hasattr(lease, "browser_id")
        lease.close()
        assert sorted(closed) == ["chrome", "service"] and not module._LEASE_LOCK.locked()
    service_env = next(env for kind, _, env, _ in processes if kind == "service")
    command, chrome_env = next((cmd, env) for kind, cmd, env, _ in processes if kind == "chrome")
    expected_tmp = str(tmp_path / "state/tmp")
    assert chrome_env == {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8",
                          "TMPDIR": expected_tmp, "MAC_CHROMIUM_TMPDIR": expected_tmp}
    assert "MAC_CHROMIUM_TMPDIR" not in service_env and "OPENAI_API_KEY" not in service_env
    assert "--no-sandbox" not in command and "--disable-web-security" not in command
    profile = Path(command[2]).read_text()
    assert "(deny network*)" in profile and "(deny file-read-data)" in profile
    assert "localhost:18001" in profile and "localhost:52829" in profile
    assert 'local unix-socket (subpath ' + json.dumps(expected_tmp) in profile
    assert "/self-authored-unapproved-parent" not in profile
    assert "Application Support/Google/Chrome" not in profile


# These fixtures never create a process, socket, browser, database or external file.
def owned_process_fixture(monkeypatch, *, record="valid", waits=None, close_error=None):
    import io
    import json
    import signal
    import threading
    import app.agent_browser as module
    events = []
    class Input(io.BytesIO):
        def close(self):
            events.append("stdin-close")
            should_fail = close_error is not None and not self.closed
            super().close()
            if should_fail:
                raise close_error
    class Process:
        pid, returncode = 100, None
        stdin, stderr = Input(), io.BytesIO()
        outcomes = list(waits if waits is not None else [-signal.SIGKILL])
        def poll(self): return self.returncode
        def wait(self, *, timeout):
            assert 0 <= timeout <= 1
            events.append("wait")
            outcome = self.outcomes.pop(0)
            if isinstance(outcome, BaseException):
                raise outcome
            self.returncode = outcome
            return outcome
        def terminate(self): events.append("terminate")
        def kill(self): events.append("kill")
    owned = object.__new__(module.OwnedProcess)
    owned.process, owned.pid, owned.group_id = Process(), 101, 100
    owned.deadline, owned.nonce = module.time.monotonic() + 10, "a" * 32
    owned.shutdown_evidence, owned._close_lock = None, threading.Lock()
    value = {"type": "curis.supervisor.child_reaped", "nonce": owned.nonce, "child_pid": 101, "returncode": -15}
    if record == "normal": value = {"type": "curis.supervisor.result", "nonce": owned.nonce, "returncode": 0}
    if record == "nonce": value["nonce"] = "b" * 32
    if record == "child": value["child_pid"] = 999
    owned.diagnostic = bytearray((json.dumps(value) + "\n").encode()) if record != "missing" else bytearray()
    owned._read_diagnostic = lambda: None
    monkeypatch.setattr(module, "_UNRESOLVED_BROWSER_PROCESSES", [])
    return owned, events, module


@pytest.mark.parametrize("record", ["valid", "normal", "nonce", "child", "missing"])
def test_owned_browser_close_requires_attempt_and_child_bound_receipt(monkeypatch, record):
    owned, events, module = owned_process_fixture(monkeypatch, record=record)
    evidence = owned.close()
    assert evidence["supervisor"] == "EXITED"
    assert evidence["direct_child"] == ("EXITED" if record in {"valid", "normal"} else "UNKNOWN")
    assert evidence["descendants"] == evidence["effects"] == "UNKNOWN"
    assert bool(module._UNRESOLVED_BROWSER_PROCESSES) == (record not in {"valid", "normal"})
    before = list(events)
    assert owned.close() == evidence and events == before  # No repeated signals or cleanup retry.


def test_owned_browser_close_escalates_only_held_supervisor_with_bounded_wait(monkeypatch):
    import subprocess
    import signal
    owned, events, _ = owned_process_fixture(monkeypatch, waits=[
        subprocess.TimeoutExpired("self-authored fixture", 1), subprocess.TimeoutExpired("self-authored fixture", 1), -signal.SIGKILL])
    assert owned.close()["direct_child"] == "EXITED"
    assert events == ["stdin-close", "wait", "terminate", "wait", "kill", "wait"]


@pytest.mark.parametrize("failure", [OSError("synthetic channel failure"), KeyboardInterrupt()])
def test_owned_browser_channel_failure_cannot_skip_wait_or_pipe_closure(monkeypatch, failure):
    owned, events, _ = owned_process_fixture(monkeypatch, close_error=failure)
    if isinstance(failure, Exception):
        owned.close()
    else:
        with pytest.raises(KeyboardInterrupt) as captured:
            owned.close()
        assert captured.value is failure
    assert "wait" in events and owned.process.stderr.closed
    assert owned.shutdown_evidence["descendants"] == "UNKNOWN"


def test_owned_browser_unconfirmed_reap_is_retained_and_not_retried(monkeypatch):
    import subprocess
    owned, events, module = owned_process_fixture(monkeypatch, record="missing", waits=[
        subprocess.TimeoutExpired("fixture", 1) for _ in range(3)])
    evidence = owned.close()
    assert evidence["supervisor"] == evidence["direct_child"] == "UNKNOWN"
    assert module._UNRESOLVED_BROWSER_PROCESSES == [owned]
    count = len(events)
    assert owned.close() == evidence and len(events) == count


def test_supervisor_final_result_cannot_replace_kernel_child_identity(monkeypatch):
    import io
    import json
    import signal
    import app.agent_browser as module
    payloads, reads = [], []
    class Input(io.BytesIO):
        def write(self, data):
            payloads.append(json.loads(data))
            reads.append((json.dumps({"type": "curis.supervisor.result", "nonce": payloads[-1]["nonce"], "returncode": 0}) + "\n").encode())
            return super().write(data)
    class Error(io.BytesIO):
        def fileno(self): return 77  # Fake descriptor; every operation is intercepted.
    class Process:
        pid, returncode = 100, None
        stdin, stderr = Input(), Error()
        def poll(self): return self.returncode
        def wait(self, *, timeout): self.returncode = -signal.SIGKILL; return self.returncode
    process = Process()
    monkeypatch.setattr(module, "_UNRESOLVED_BROWSER_PROCESSES", [])
    monkeypatch.setattr(module, "packaged_supervisor_command", lambda: ["/self-authored-never-executed"])
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: process)
    monkeypatch.setattr(module.os, "set_blocking", lambda fd, value: None)
    def read(*args):
        if reads: return reads.pop(0)
        raise BlockingIOError()
    monkeypatch.setattr(module.os, "read", read)
    monkeypatch.setattr(module.select, "select", lambda *a: ([process.stderr], [], []))
    monkeypatch.setattr(module, "_browser_process_identity", lambda pid: {"pid": pid, "ppid": 1, "uid": module.os.getuid(),
        "pgid": pid, "start": (1, 0), "executable": "/self-authored-never-executed"})
    monkeypatch.setattr(module, "_browser_direct_children", lambda pid: ())
    with pytest.raises(ValueError, match="启动身份"):
        module.OwnedProcess(["/usr/bin/sandbox-exec", "-f", "/self-authored-policy", "/self-authored-command"], "/self-authored-cwd", {})
    assert set(payloads[0]) == {"command", "cwd", "environment", "prompt", "timeout", "nonce", "deadline"}
    assert len(payloads[0]["nonce"]) == 32 and payloads[0]["environment"] == {}
    assert process.stdin.closed and process.stderr.closed
    assert module._UNRESOLVED_BROWSER_PROCESSES[0].shutdown_evidence["direct_child"] == "UNKNOWN"


def lease_cleanup_fixture(monkeypatch, *, chrome_error=None, child_state="EXITED", proxy_error=None):
    import threading
    import app.agent_browser as module
    events = []
    class Process:
        def __init__(self, name): self.name = name
        def close(self):
            events.append(self.name)
            if self.name == "chrome" and chrome_error: raise chrome_error
            return {"supervisor": "EXITED", "direct_child": child_state, "descendants": "UNKNOWN", "effects": "UNKNOWN"}
    class Proxy:
        def close(self):
            events.append("proxy")
            if proxy_error: raise proxy_error
    lease = object.__new__(module.BrowserLease)
    lease.chrome, lease.service, lease.proxy = Process("chrome"), Process("service"), Proxy()
    lease._close_lock, lease._closed, lease.shutdown_evidence = threading.Lock(), False, None
    lease.deadline = module.time.monotonic() + 5
    lease.lock_held = True
    lock = threading.Lock(); lock.acquire()
    monkeypatch.setattr(module, "_LEASE_LOCK", lock)
    monkeypatch.setattr(module, "_UNRESOLVED_BROWSER_PROCESSES", [])
    return lease, events, lock


@pytest.mark.parametrize("failure", [OSError("synthetic close"), KeyboardInterrupt()])
def test_lease_teardown_always_attempts_other_process_and_proxy(monkeypatch, failure):
    lease, events, lock = lease_cleanup_fixture(monkeypatch, chrome_error=failure)
    if isinstance(failure, Exception):
        evidence = lease.close()
    else:
        with pytest.raises(KeyboardInterrupt) as captured:
            lease.close()
        assert captured.value is failure
        evidence = lease.shutdown_evidence
    assert events == ["chrome", "service", "proxy"] and lease._closed
    assert evidence["state"] == "OUTCOME_UNKNOWN" and lock.locked()
    before = list(events)
    lease.close()
    assert events == before


@pytest.mark.parametrize("child_state,proxy_error", [("EXITED", None), ("UNKNOWN", None), ("EXITED", OSError("synthetic proxy close"))])
def test_lease_releases_admission_only_after_confirmed_local_cleanup(monkeypatch, child_state, proxy_error):
    lease, events, lock = lease_cleanup_fixture(monkeypatch, child_state=child_state, proxy_error=proxy_error)
    evidence = lease.close()
    safe = child_state == "EXITED" and proxy_error is None
    assert lock.locked() != safe
    assert evidence["state"] == ("CLOSED_WITH_UNKNOWN_EFFECTS" if safe else "OUTCOME_UNKNOWN")
    assert evidence["descendants"] == evidence["effects"] == "UNKNOWN"


def test_closed_lease_rejects_new_tool_calls_before_identity_or_network_reads():
    lease = object.__new__(BrowserLease)
    lease._closed = True
    lease.connected = lambda: pytest.fail("closed lease must not inspect processes")
    with pytest.raises(ValueError, match="已停止"):
        lease.call({"action": "observe"}, SimpleNamespace(identity={}))


def test_inflight_browser_text_is_not_adopted_after_close():
    lease = object.__new__(BrowserLease)
    lease.identity = {"tenant_id": "tenant", "company_id": "company", "work_ref": "work", "task_id": "task"}
    lease.browser_id, lease.tab, lease.session = "owned", 7, "owned-session"
    lease._session_started = True
    lease.connected = lambda: "owned"
    lease._tab_url = lambda: "https://example.com/public"
    lease.policy = SimpleNamespace(dns_snapshot=lambda: [])
    def late(method, params):
        lease._closed = True
        return {"tab_id": 7, "text": "self-authored late result"}
    lease.rpc = late
    with pytest.raises(ValueError, match="已停止"):
        lease.call({"action": "observe"}, SimpleNamespace(identity=lease.identity))





def test_proxy_close_deadline_cannot_late_promote_unknown_or_release_admission(monkeypatch):
    import app.agent_browser as module
    lease, events, lock = lease_cleanup_fixture(monkeypatch)
    callbacks = []
    class Thread:
        def __init__(self, *, target, daemon):
            assert daemon is True
            callbacks.append(target)
        def start(self): pass  # Self-authored blocked close; no thread is started.
    monkeypatch.setattr(module.threading, "Thread", Thread)
    lease.deadline = module.time.monotonic() + 0.001
    evidence = lease.close()
    assert evidence["state"] == "OUTCOME_UNKNOWN" and evidence["proxy"] == "UNKNOWN" and lock.locked()
    callbacks[0]()  # A late completion cannot mutate the saved receipt or authorize reuse.
    assert events == ["chrome", "service", "proxy"]
    assert lease.close() == evidence and lease.shutdown_evidence["proxy"] == "UNKNOWN" and lock.locked()


def test_expired_owned_process_cleanup_has_no_unbounded_wait(monkeypatch):
    import subprocess
    owned, events, module = owned_process_fixture(monkeypatch, record="missing", waits=[
        subprocess.TimeoutExpired("fixture", 0) for _ in range(3)])
    owned.deadline = module.time.monotonic() - 1
    assert owned.close()["supervisor"] == "UNKNOWN"
    assert events == ["stdin-close", "wait", "terminate", "wait", "kill", "wait"]


def test_already_exited_owned_supervisor_is_not_signalled(monkeypatch):
    import signal
    owned, events, _ = owned_process_fixture(monkeypatch)
    owned.process.returncode = -signal.SIGKILL
    assert owned.close()["direct_child"] == "EXITED"
    assert events == ["stdin-close"]


@pytest.mark.parametrize("failure", [None, "ppid", "pgid", "uid", "old_start", "executable", "supervisor_changed", "two_children"])
def test_browser_start_binds_kernel_owned_child_without_new_supervisor_protocol(monkeypatch, failure):
    import io
    import json
    import signal
    import app.agent_browser as module
    requests, reads, events = [], [], []
    class Input(io.BytesIO):
        def write(self, data): requests.append(json.loads(data)); return super().write(data)
    class Error(io.BytesIO):
        def fileno(self): return 77
    class Process:
        pid, returncode = 100, None
        stdin, stderr = Input(), Error()
        def poll(self): return self.returncode
        def wait(self, *, timeout):
            assert 0 <= timeout <= 1
            self.returncode = -signal.SIGKILL
            reads.append((json.dumps({"type": "curis.supervisor.child_reaped", "nonce": requests[0]["nonce"],
                "child_pid": 101, "returncode": 0}) + "\n").encode())
            return self.returncode
        def terminate(self): events.append("held-supervisor-terminate")
        def kill(self): events.append("held-supervisor-kill")
    process = Process()
    supervisor = {"pid": 100, "ppid": 99, "uid": module.os.getuid(), "pgid": 100, "start": (10, 1), "executable": "/self-authored-supervisor"}
    child = {"pid": 101, "ppid": 100, "uid": module.os.getuid(), "pgid": 100, "start": (11, 2), "executable": "/self-authored-browser"}
    if failure == "ppid": child["ppid"] = 999
    if failure == "pgid": child["pgid"] = 999
    if failure == "uid": child["uid"] += 1
    if failure == "old_start": child["start"] = (9, 0)
    if failure == "executable": child["executable"] = "/foreign-ordinary-executable"
    probes = []
    def identity(pid):
        probes.append(pid)
        value = dict(supervisor if pid == 100 else child)
        if failure == "supervisor_changed" and len(probes) > 1: value["start"] = (12, 0)
        return value
    monkeypatch.setattr(module, "_UNRESOLVED_BROWSER_PROCESSES", [])
    monkeypatch.setattr(module, "packaged_supervisor_command", lambda: ["/self-authored-supervisor"])
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: process)
    monkeypatch.setattr(module, "_browser_process_identity", identity)
    monkeypatch.setattr(module, "_browser_direct_children", lambda pid: (101, 102) if failure == "two_children" else (101,))
    monkeypatch.setattr(module.os, "set_blocking", lambda *a: None)
    monkeypatch.setattr(module.select, "select", lambda *a: ([], [], []))
    def read(*args):
        if reads: return reads.pop(0)
        raise BlockingIOError()
    monkeypatch.setattr(module.os, "read", read)
    args = (["/usr/bin/sandbox-exec", "-f", "/self-authored-policy", "/self-authored-browser"], "/self-authored-cwd", {})
    if failure:
        with pytest.raises(ValueError): module.OwnedProcess(*args)
    else:
        owned = module.OwnedProcess(*args)
        assert owned.pid == 101 and owned.group_id == 100 and owned.alive()
        child["start"] = (12, 0)
        assert not owned.alive()  # PID reuse cannot pass on group membership alone.
        assert owned.close()["direct_child"] == "EXITED"
    assert set(requests[0]) == {"command", "cwd", "environment", "prompt", "timeout", "nonce", "deadline"}
    assert all(pid in {100, 101} for pid in probes)
    assert events == []  # No discovered PID, group or unneeded supervisor signal.


def test_mac_kernel_wrappers_use_bsdinfo_and_child_count_not_process_inventory(monkeypatch):
    import ctypes
    import app.agent_browser as module
    queries = []
    def pidinfo(pid, flavor, arg, pointer, size):
        queries.append(("identity", pid))
        assert flavor == 3 and size == 136
        value = ctypes.cast(pointer, ctypes.POINTER(module._BrowserBsdInfo)).contents
        value.pid, value.ppid, value.uid, value.pgid = pid, 100, 501, 100
        value.status, value.start_seconds, value.start_microseconds = 3, 11, 2
        return size
    def pidpath(pid, pointer, size):
        value = b"/self-authored-browser\0"
        ctypes.memmove(pointer, value, len(value))
        return len(value) - 1
    def children(pid, pointer, size):
        queries.append(("children", pid))
        pointer[0] = 101
        return 1  # PID count, not sizeof(pid_t).
    monkeypatch.setattr(module, "_browser_libproc", lambda: SimpleNamespace(proc_pidinfo=pidinfo, proc_pidpath=pidpath, proc_listchildpids=children))
    assert module._browser_direct_children(100) == (101,)
    identity = module._browser_process_identity(101)
    assert identity == {"pid": 101, "ppid": 100, "uid": 501, "pgid": 100, "start": (11, 2), "executable": "/self-authored-browser"}
    assert queries == [("children", 100), ("identity", 101)]


@pytest.mark.parametrize("count", [-1, 2, 4])
def test_ambiguous_kernel_child_list_fails_closed(monkeypatch, count):
    import ctypes
    import app.agent_browser as module
    def children(pid, pointer, size):
        pointer[0], pointer[1] = 101, 102
        return count
    monkeypatch.setattr(module, "_browser_libproc", lambda: SimpleNamespace(proc_listchildpids=children))
    with pytest.raises(ValueError): module._browser_direct_children(100)


@pytest.mark.parametrize("platform", ["linux", "win32", "freebsd14"])
def test_mac_browser_launcher_rejects_other_platforms_before_side_effects(monkeypatch, platform):
    import app.agent_browser as module
    def forbidden(*args, **kwargs):
        raise AssertionError("Unsupported launcher performed an operation")
    monkeypatch.setattr(module.sys, "platform", platform)
    monkeypatch.setattr(module, "safe_directory", forbidden)
    monkeypatch.setattr(module, "managed_browser_tool", forbidden)
    monkeypatch.setattr(module, "PublicReadProxy", forbidden)
    monkeypatch.setattr(module, "OwnedProcess", forbidden)
    monkeypatch.setattr(module.time, "monotonic", forbidden)
    with pytest.raises(ValueError, match="适配器尚未验证"):
        module.BrowserLease(object(), {}, {}, [], setup=True)


@pytest.mark.parametrize("failure", [None, "wildcard", "peer", "inactive", "nonce", "tls", "revoke"])
def test_managed_proxy_requires_fixed_owner_interface_and_lifetime(monkeypatch, failure):
    import ssl
    import app.agent_browser_policy as module
    import app.reader_vm_host as host
    identity = {k: k for k in ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")}
    nonce = "a" * 48
    binding = {"identity": identity.copy(), "nonce": nonce, "boot_id": "boot", "container_id": "container",
               "image_digest": "sha256:fixture", "network_id": "network", "proxy_ip": "172.30.253.2",
               "browser_ip": "172.30.253.3", "port": 8443, "verified": True, "active": True}
    if failure == "wildcard": binding["proxy_ip"] = "0.0.0.0"
    if failure == "peer": binding["browser_ip"] = "127.0.0.1"
    if failure == "inactive": binding["active"] = False
    if failure == "nonce": binding["nonce"] = "b" * 48
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    events = []
    def verified(work, token):
        assert work == identity and token == nonce
        return {**binding, "identity": binding["identity"].copy()}
    owner = SimpleNamespace(verified_proxy_binding=verified,
        proxy_tls=lambda *args: (None if failure == "tls" else context, "A" * 43 + "="))
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda work: owner)
    def initialize(self, policy, alive, seconds, supplied_context, spki, address, peer):
        assert supplied_context is context and address == ("172.30.253.2", 8443) and peer == "172.30.253.3"
        self.alive, self.deadline = alive, float("inf")
        events.append("initialize")
        if failure == "revoke": binding["active"] = False
    monkeypatch.setattr(module.PublicReadProxy, "_initialize", initialize)
    monkeypatch.setattr(module.PublicReadProxy, "close", lambda self: events.append("close"))
    if failure:
        with pytest.raises((PermissionError, ValueError)):
            module.PublicReadProxy.for_managed_runtime(identity, nonce, object())
        assert events == (["initialize", "close"] if failure == "revoke" else [])
    else:
        proxy = module.PublicReadProxy.for_managed_runtime(identity, nonce, object())
        proxy.check()
        binding["network_id"] = "replacement"
        with pytest.raises(ValueError): proxy.check()
        assert events == ["initialize"]


def test_managed_proxy_production_owner_stays_closed_before_certificate_or_socket(monkeypatch):
    import app.agent_browser_policy as module
    def forbidden(*args, **kwargs): raise AssertionError("listener or certificate reached")
    monkeypatch.setattr(module, "tls_certificate", forbidden)
    monkeypatch.setattr(module.PublicReadProxy, "_initialize", forbidden)
    identity = {k: k for k in ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")}
    with pytest.raises(ValueError):
        module.PublicReadProxy.for_managed_runtime(identity, "a" * 48, object())


def test_proxy_default_loopback_and_managed_peer_filter_without_listener(monkeypatch):
    import app.agent_browser_policy as module
    events, handlers = [], []
    class Server:
        def __init__(self, address, handler):
            events.append(address)
            self.server_address = (address[0], address[1] or 45000)
            handlers.append(handler)
        def serve_forever(self): raise AssertionError("no server loop")
    class Background:
        def __init__(self, *args, **kwargs): pass
        def start(self): pass
    monkeypatch.setattr(module.socketserver, "ThreadingTCPServer", Server)
    monkeypatch.setattr(module.threading, "Thread", Background)
    monkeypatch.setattr(module.threading, "Timer", Background)
    monkeypatch.setattr(module, "tls_certificate", lambda *args: (object(), "fixture-pin"))
    proxy = module.PublicReadProxy(object(), SimpleNamespace(hosts=["example.com"]))
    assert events == [("127.0.0.1", 0)] and proxy.port == 45000
    managed = module.PublicReadProxy.__new__(module.PublicReadProxy)
    managed._initialize(object(), lambda: True, 90, object(), "fixture-pin", ("172.30.253.2", 8443), "172.30.253.3")
    served = []
    managed.serve = lambda request: served.append(request)
    handler = handlers[-1]
    for peer in ["127.0.0.1", "172.30.253.4", "172.30.253.3"]:
        instance = handler.__new__(handler)
        instance.client_address, instance.request = (peer, 40000), peer
        instance.handle()
    assert served == ["172.30.253.3"]
    assert events == [("127.0.0.1", 0), ("172.30.253.2", 8443)]



def native_browser_fixture():
    import time
    lease=object.__new__(BrowserLease)
    lease.identity={"tenant_id":"tenant","company_id":"company","work_ref":"work","task_id":"task"}
    lease._closed=False
    lease._session_start_attempted=lease._session_started=False
    lease.setup=False
    lease.deadline=time.monotonic()+30
    lease.stop_check=lambda:True
    lease.session,lease.browser_id,lease.tab="local-allocation-only","owned-browser",5
    lease.policy=PublicTargets(["example.com"])
    lease.connected=lambda:"owned-browser"
    lease.close_calls=[]
    def close():lease._closed=True;lease.close_calls.append(True)
    lease.close=close
    return lease


@pytest.mark.parametrize("failure",[None,"session","browser","window"])
def test_native_browser_session_start_uses_official_daemon_id_and_no_caller_session(failure):
    lease=native_browser_fixture()
    calls=[]
    def rpc(method,params):
        calls.append((method,params))
        assert method=="session.start" and params=={"browser_instance_id":"owned-browser","focused":False}
        value={"session_id":"daemon-created-id","browser_instance_id":"owned-browser","agent_window_id":12}
        if failure=="session":value["session_id"]=""
        if failure=="browser":value["browser_instance_id"]="foreign"
        if failure=="window":value["agent_window_id"]=True
        return value
    lease.rpc=rpc
    if failure:
        with pytest.raises(ValueError):lease.start()
        assert lease.close_calls==[True] and not lease._session_started
    else:
        assert lease.start() is lease and lease.session=="daemon-created-id" and lease._session_started
    with pytest.raises(ValueError):lease.start()
    assert len(calls)==1


@pytest.mark.parametrize("reached",["commit","domcontentloaded","load","networkidle","timeout",None,True,"unknown"])
def test_native_navigation_uses_real_lifecycle_and_adopts_only_revalidated_owned_tab(reached):
    lease=native_browser_fixture();lease._session_started=True
    calls=[]
    def rpc(method,params):
        calls.append(method)
        if method=="tool.navigate":
            return {"tab_id":7,"url":"https://example.com/public",**({"reached":reached} if reached is not None else {})}
        assert method=="tool.tab_list"
        return {"tabs":[{"tab_id":7,"scope":"agent","url":"https://example.com/public"}]}
    lease.rpc=rpc
    resources=SimpleNamespace(identity=lease.identity)
    if reached in ("commit","domcontentloaded","load","networkidle"):
        value=lease.call({"action":"navigate","url":"https://example.com/public"},resources)
        assert value["tab_id"]==lease.tab==7 and value["url"]=="https://example.com/public"
        assert calls==["tool.navigate","tool.tab_list"]
    else:
        with pytest.raises(ValueError):lease.call({"action":"navigate","url":"https://example.com/public"},resources)
        assert lease.tab==5 and calls==["tool.navigate"]


def test_native_navigation_rejected_foreign_tab_does_not_replace_original():
    lease=native_browser_fixture();lease._session_started=True
    lease.rpc=lambda method,params:({"tab_id":7,"url":"https://example.com/public","reached":"load"} if method=="tool.navigate"
        else {"tabs":[{"tab_id":7,"scope":"user","url":"https://example.com/public"}]})
    with pytest.raises(ValueError):lease.call({"action":"navigate","url":"https://example.com/public"},SimpleNamespace(identity=lease.identity))
    assert lease.tab==5


def test_native_browser_cannot_offer_tools_before_verified_agent_window():
    lease=native_browser_fixture()
    lease.connected=lambda:(_ for _ in ()).throw(AssertionError("unstarted browser inspected process"))
    with pytest.raises(ValueError,match="尚未核验"):lease.call({"action":"observe"},SimpleNamespace(identity=lease.identity))


@pytest.mark.parametrize("failure",[None,"peer","request-id","tail","duplicate","partial-send","slow-drip"])
def test_native_ipc_authentication_one_absolute_deadline_and_no_uncertain_replay(monkeypatch,failure):
    import json,stat,struct
    import app.agent_browser as module
    lease=native_browser_fixture()
    clock=[0.0]
    lease.deadline=30
    lease.service=SimpleNamespace(pid=101,alive=lambda:True)
    lease.socket_path=SimpleNamespace(lstat=lambda:SimpleNamespace(st_mode=stat.S_IFSOCK|0o600,st_uid=module.os.geteuid()))
    monkeypatch.setattr(module.time,"monotonic",lambda:clock[0])
    sent,packets,timeouts=[],[],[]
    class Connection:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def settimeout(self,value):assert 0<value<=5;timeouts.append(value)
        def connect(self,path):clock[0]+=1
        def getsockopt(self,*args):return struct.pack("i",999 if failure=="peer" else 101)
        def sendall(self,data):
            sent.append(json.loads(data))
            if failure=="partial-send":raise TimeoutError("synthetic partial write")
            request_id=sent[-1]["id"]
            if failure=="duplicate":
                response=('{"id":'+json.dumps(request_id)+',"result":{},"result":{}}\n').encode()
            else:
                response=(json.dumps({"id":"foreign" if failure=="request-id" else request_id,"result":{"ok":True}})+'\n').encode()
            if failure=="tail":response+=b'{}\n'
            packets.extend([response[:3],response[3:6],response[6:]])
        def recv(self,count):
            clock[0]+=2 if failure=="slow-drip" else .1
            return packets.pop(0)
    monkeypatch.setattr(module.socket,"socket",lambda *args:Connection())
    if failure:
        with pytest.raises((ValueError,TimeoutError)):lease.rpc("system.status",{})
        assert len(lease.close_calls)==(0 if failure=="peer" else 1)
    else:
        assert lease.rpc("system.status",{})=={"ok":True}
        assert timeouts[0]==5 and max(timeouts[1:])<=4 and not lease.close_calls
    assert len(sent)==(0 if failure=="peer" else 1)
    if lease._closed:
        with pytest.raises(ValueError):lease.rpc("system.status",{})
        assert len(sent)==1
