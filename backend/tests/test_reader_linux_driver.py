import json

import pytest

from app.reader_linux_driver import LinuxReaderDriver


class Policy:
    def url(self, url):
        if not url.startswith("https://public.example/"):
            raise ValueError("unauthorized URL")


class Environment:
    daemon_pid = 21

    def verify(self):
        return True

    def verify_browser(self, browser):
        return browser == "browser-1"


def status():
    return {"pid": 21, "daemon_version": "0.3.3", "browsers": [
        {"instance_id": "browser-1", "extension_version": "0.3.3"}]}


def test_session_uses_daemon_assigned_id_and_one_tab(monkeypatch):
    driver = LinuxReaderDriver(Environment(), Policy())
    calls = []

    def rpc(method, params):
        calls.append((method, params))
        if method == "system.status":
            return status()
        if method == "session.start":
            return {"session_id": "assigned", "browser_instance_id": "browser-1"}
        if method == "tool.navigate":
            return {"tab_id": 4, "final_url": "https://public.example/a", "reached": "domcontentloaded"}
        if method == "tool.tab_list":
            return {"tabs": [{"tab_id": 4, "scope": "agent", "url": "https://public.example/a"}]}
        if method == "tool.observe":
            return {"tab_id": 4, "text": "page"}
        if method == "session.stop":
            return {"stopped": ["assigned"], "failed": []}
        raise AssertionError(method)

    monkeypatch.setattr(driver, "_rpc", rpc)
    assert driver.start() == {"ready": True}
    assert calls[1] == ("session.start", {"browser_instance_id": "browser-1", "focused": False})
    assert driver.navigate("https://public.example/a")["tab_id"] == 4
    assert driver.observe(4)["url"] == "https://public.example/a"
    driver.close()
    assert calls[-1] == ("session.stop", {"session_id": "assigned", "all": False})
    assert driver.state == "CLOSED"


def test_status_cannot_substitute_for_owned_extension(monkeypatch):
    env = Environment()
    env.verify_browser = lambda _: False
    driver = LinuxReaderDriver(env, Policy())
    monkeypatch.setattr(driver, "_rpc", lambda *_: status())
    with pytest.raises(PermissionError):
        driver.start()
    assert driver.state == "UNKNOWN"


def test_start_failure_is_unknown_and_not_claimed_stopped(monkeypatch):
    driver = LinuxReaderDriver(Environment(), Policy())
    def rpc(method, _params):
        if method == "system.status":
            return status()
        raise TimeoutError("session may have started")
    monkeypatch.setattr(driver, "_rpc", rpc)
    with pytest.raises(TimeoutError):
        driver.start()
    driver.close()
    assert driver.state == "UNKNOWN"


@pytest.mark.parametrize("result", [
    {"stopped": "prefix-assigned-suffix"},
    {"stopped": ["assigned"], "failed": ""},
    {"stopped": ["assigned"], "return_failures": {}},
    {"stopped": ["assigned", "other"]},
])
def test_stop_rejects_malformed_or_extra_receipts(monkeypatch, result):
    driver = LinuxReaderDriver(Environment(), Policy())
    driver.state, driver.session = "OPEN", "assigned"
    monkeypatch.setattr(driver, "_rpc", lambda *_: result)
    with pytest.raises(ValueError):
        driver.close()
    assert driver.state == "UNKNOWN"


def test_reject_changed_tab_and_url(monkeypatch):
    driver = LinuxReaderDriver(Environment(), Policy())
    driver.state, driver.session, driver.browser, driver.tab, driver.url = (
        "OPEN", "assigned", "browser-1", 4, "https://public.example/a")
    monkeypatch.setattr(driver, "_status", lambda: "browser-1")
    monkeypatch.setattr(driver, "_rpc", lambda *_: {"tabs": [
        {"tab_id": 4, "scope": "agent", "url": "https://public.example/other"}]})
    with pytest.raises(ValueError):
        driver.observe(4)
    assert driver.state == "UNKNOWN"


def test_rpc_rejects_wrong_peer_before_sending(monkeypatch):
    import app.reader_linux_driver as module
    class Socket:
        def __enter__(self): return self
        def __exit__(self, *_): pass
        def settimeout(self, _): pass
        def connect(self, _): pass
        def getsockopt(self, *_): return module.struct.pack("3i", 99, 1, 1)
        def sendall(self, _): raise AssertionError("must not send")
    env = Environment()
    env.daemon_socket = "/not-opened"
    env.verify_daemon_peer = lambda *_: False
    driver = LinuxReaderDriver(env, Policy())
    monkeypatch.setattr(module.socket, "socket", lambda *_: Socket())
    monkeypatch.setattr(module.socket, "SO_PEERCRED", 17, raising=False)
    with pytest.raises(PermissionError):
        driver._rpc("system.status", {})
    assert driver.state == "UNKNOWN"


def test_rpc_rejects_duplicate_and_mismatched_reply(monkeypatch):
    import app.reader_linux_driver as module
    class Socket:
        def __enter__(self): return self
        def __exit__(self, *_): pass
        def settimeout(self, _): pass
        def connect(self, _): pass
        def getsockopt(self, *_): return module.struct.pack("3i", 21, 1, 1)
        def sendall(self, data): self.request = json.loads(data)
        def recv(self, _): return b'{"id":"wrong","id":"other","result":{}}\n'
    env = Environment()
    env.daemon_socket = "/not-opened"
    env.verify_daemon_peer = lambda *_: True
    driver = LinuxReaderDriver(env, Policy())
    monkeypatch.setattr(module.socket, "socket", lambda *_: Socket())
    monkeypatch.setattr(module.socket, "SO_PEERCRED", 17, raising=False)
    with pytest.raises(ValueError):
        driver._rpc("system.status", {})
    assert driver.state == "UNKNOWN"


def test_json_rejects_nested_float_overflow():
    from app.reader_linux_driver import _finite_float
    with pytest.raises(ValueError):
        json.loads('{"nested":[1e999]}', parse_float=_finite_float)


def test_rpc_rejects_nested_float_overflow(monkeypatch):
    import app.reader_linux_driver as module
    class Socket:
        def __enter__(self): return self
        def __exit__(self, *_): pass
        def settimeout(self, _): pass
        def connect(self, _): pass
        def getsockopt(self, *_): return module.struct.pack("3i", 21, 1, 1)
        def sendall(self, data): self.request = json.loads(data)
        def recv(self, _):
            return ('{"id":"' + self.request["id"] + '","result":{"nested":[1e999]}}\n').encode()
    env = Environment()
    env.daemon_socket = "/not-opened"
    env.verify_daemon_peer = lambda *_: True
    driver = LinuxReaderDriver(env, Policy())
    monkeypatch.setattr(module.socket, "socket", lambda *_: Socket())
    monkeypatch.setattr(module.socket, "SO_PEERCRED", 17, raising=False)
    with pytest.raises(ValueError):
        driver._rpc("system.status", {})
    assert driver.state == "UNKNOWN"
