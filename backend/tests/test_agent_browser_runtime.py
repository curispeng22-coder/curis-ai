import base64
import pytest
from app.agent_browser_runtime import ReaderLease, load_trusted_reader_lock as _bundled_lock_loader
from app.agent_work_resources import AgentWorkResources

IDENTITY = {"tenant_id":"tenant", "company_id":"company", "work_ref":"work", "task_id":"task",
            "employee_id":"employee", "binding_ref":"binding"}
RUNTIME = {"complete":True, "executionAuthorized":True, "boot_id":"boot", "container_id":"container", "image_digest":"sha256:fixture"}
def real_png():
    import struct
    import zlib
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return (bytes.fromhex("89504e470d0a1a0a")
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes([0, 255, 0, 0, 255])))
            + chunk(b"IEND", b""))

PNG = real_png()

class Policy:
    def url(self, url):
        if url != "https://example.com/":
            raise ValueError("foreign URL")

class Transport:
    def __init__(self):
        self.requests=[]; self.closed=0; self.tamper=None
    def request(self, envelope):
        self.requests.append(envelope)
        action=envelope["action"]
        data={"ready":True} if action=="start" else {"tab_id":"tab", "url":"https://example.com/"}
        if action=="screenshot": data["image_base64"]=base64.b64encode(PNG).decode()
        response={key:envelope[key] for key in ("identity","nonce","sequence","boot_id","container_id","image_digest")}
        response["result"]=data
        if self.tamper: response[self.tamper]="wrong"
        return response
    def close(self): self.closed+=1

@pytest.fixture(autouse=True)
def fake_released_lock(monkeypatch, request):
    if request.node.name == "test_bundled_unreleased_lock_fails_closed":
        return
    monkeypatch.setattr("app.agent_browser_runtime.load_trusted_reader_lock",
                        lambda: {"browserImageDigest": RUNTIME["image_digest"]})

def resources(tmp_path):
    item=AgentWorkResources(tmp_path,tenant_id="tenant",company_id="company",work_ref="work",task_id="task")
    item.prepare([])
    return item

def test_reader_rejects_unreleased_runtime():
    with pytest.raises(ValueError):
        ReaderLease(IDENTITY,Policy(),Transport(),{**RUNTIME,"complete":False})

def test_reader_screenshot_is_unavailable_before_file_creation(tmp_path):
    transport=Transport(); lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()
    original=resources(tmp_path)
    lease.call({"action":"navigate","url":"https://example.com/"},original)
    with pytest.raises(ValueError, match="截图成果暂不可用"):
        lease.call({"action":"screenshot"},original)
    assert original.collect()==[]
    lease.close();lease.close()
    assert transport.closed==1

@pytest.mark.parametrize("field",["identity","nonce","sequence","boot_id","container_id","image_digest"])
def test_reader_rejects_mismatched_response(field):
    transport=Transport();transport.tamper=field
    with pytest.raises(ValueError):
        ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()

def test_reader_rejects_foreign_action_target_and_stopped_work(tmp_path):
    running=[True]; transport=Transport(); lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME,alive=lambda:running[0]).start()
    original=resources(tmp_path)
    with pytest.raises(ValueError): lease.call({"action":"navigate","url":"https://private.example/"},original)
    with pytest.raises(ValueError): lease.call({"action":"click"},original)
    running[0]=False
    with pytest.raises(PermissionError): lease.call({"action":"navigate","url":"https://example.com/"},original)

def test_guest_real_dispatcher_enforces_identity_sequence_and_owned_tab(tmp_path):
    from app.agent_browser_guest import ReaderGuest
    class Driver:
        def start(self): return {"ready":True}
        def navigate(self, url): return {"tab_id":"tab","url":url}
        def observe(self, tab_id): return {"tab_id":tab_id,"url":"https://example.com/","text":"public"}
        def screenshot(self, tab_id):
            return {"tab_id":tab_id,"url":"https://example.com/","image_base64":base64.b64encode(PNG).decode()}
        def close(self): pass
    class GuestTransport:
        def __init__(self): self.guest=None
        def request(self, frame):
            if self.guest is None:
                self.guest=ReaderGuest(frame["identity"],frame["nonce"],RUNTIME,Policy(),Driver())
            return self.guest.handle(frame)
        def close(self): self.guest.close()
    transport=GuestTransport()
    lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()
    original=resources(tmp_path)
    lease.call({"action":"navigate","url":"https://example.com/"},original)
    assert lease.call({"action":"observe"},original)["result"]["text"]=="public"
    with pytest.raises(ValueError, match="截图成果暂不可用"):
        lease.call({"action":"screenshot"},original)
    assert original.collect()==[]
    last=transport.guest.sequence
    with pytest.raises(ValueError):
        transport.guest.handle({**transport.guest.runtime,"identity":IDENTITY,"nonce":lease.nonce,
                                "sequence":last,"action":"observe","arguments":{"tab_id":"tab"}})
    lease.close()

def test_literal_escaped_png_text_is_not_a_png(tmp_path):
    transport=Transport()
    lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()
    original=resources(tmp_path)
    lease.call({"action":"navigate","url":"https://example.com/"},original)
    old=transport.request
    def bad(frame):
        response=old(frame)
        if frame["action"]=="screenshot":
            response["result"]["image_base64"]=base64.b64encode(bytes.fromhex("5c783839504e475c725c6e5c7831615c6e")).decode()
        return response
    transport.request=bad
    with pytest.raises(ValueError): lease.call({"action":"screenshot"},original)
    assert original.collect()==[]

@pytest.mark.parametrize("bad", [
    bytes.fromhex("89504e470d0a1a0a"),
    PNG[:-1],
    PNG[:29] + bytes([PNG[29] ^ 1]) + PNG[30:],
])
def test_incomplete_or_bad_crc_png_is_rejected(tmp_path, bad):
    transport=Transport()
    lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()
    original=resources(tmp_path)
    lease.call({"action":"navigate","url":"https://example.com/"},original)
    old=transport.request
    def malformed(frame):
        result=old(frame)
        if frame["action"]=="screenshot":
            result["result"]["image_base64"]=base64.b64encode(bad).decode()
        return result
    transport.request=malformed
    with pytest.raises(ValueError): lease.call({"action":"screenshot"},original)
    assert original.collect()==[]

def test_bundled_unreleased_lock_fails_closed(monkeypatch):
    # Exercise the actual bundled gate even when other isolated suites install fake runtime inputs.
    monkeypatch.setattr("app.agent_browser_runtime.load_trusted_reader_lock",_bundled_lock_loader)
    from app.agent_browser_runtime import load_trusted_reader_lock
    with pytest.raises(ValueError, match="not released"):
        load_trusted_reader_lock()
    with pytest.raises(ValueError, match="not released"):
        ReaderLease(IDENTITY, Policy(), Transport(), RUNTIME, nonce="a" * 48)
    from app.agent_browser_runtime import open_native_browser_for_work
    with pytest.raises(ValueError,match="暂不能执行"):
        open_native_browser_for_work(IDENTITY,["example.com"],lambda:False,
            root="/synthetic-owned/agent-browser",metadata={})

def test_reader_rejects_runtime_image_outside_pinned_lock():
    with pytest.raises(ValueError, match="pinned image"):
        ReaderLease(IDENTITY, Policy(), Transport(), {**RUNTIME, "image_digest":"sha256:foreign"})

def test_screenshot_rejected_before_output_even_if_stop_changes(tmp_path, monkeypatch):
    import app.agent_tool_server as tool_server
    running=[True]; transport=Transport(); lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME,alive=lambda:running[0]).start()
    original=resources(tmp_path)
    lease.call({"action":"navigate","url":"https://example.com/"},original)
    writes=[]
    monkeypatch.setattr(tool_server,"write_output",lambda *args, **kwargs: writes.append(True))
    with pytest.raises(ValueError, match="截图成果暂不可用"):
        lease.call({"action":"screenshot"},original)
    assert writes==[] and original.collect()==[]
    running[0]=False
    with pytest.raises(PermissionError):
        lease.call({"action":"screenshot"},original)
    assert original.collect()==[]

def test_unverified_legacy_browser_screenshot_is_refused_before_rpc_or_output(tmp_path):
    from app.agent_browser import BrowserLease
    original=resources(tmp_path)
    lease=object.__new__(BrowserLease)
    lease.browser_id="browser"; lease.identity=dict(original.identity); lease.tab="tab"
    lease.session="session"; lease.sequence=0; lease.stop_check=lambda:True
    lease._session_started=False
    lease.connected=lambda:"browser"; lease._tab_url=lambda:"https://example.com/"
    lease.policy=Policy()
    lease.rpc=lambda *args:(_ for _ in ()).throw(AssertionError("unverified legacy session reached RPC"))
    with pytest.raises(ValueError,match="会话尚未核验"):
        lease.call({"action":"screenshot"},original)
    assert original.collect()==[]

def test_owned_pipe_transport_serves_persistent_guest_without_process_or_network(tmp_path):
    import os
    import threading
    from app.agent_browser_runtime import BoundedPipeTransport
    from app.agent_browser_guest import ReaderGuest, serve_reader
    class Driver:
        def __init__(self): self.closed=False
        def start(self): return {"ready":True}
        def navigate(self, url): return {"tab_id":"tab","url":url}
        def observe(self, tab_id): return {"tab_id":tab_id,"url":"https://example.com/","text":"public"}
        def screenshot(self, tab_id):
            return {"tab_id":tab_id,"url":"https://example.com/","image_base64":base64.b64encode(PNG).decode()}
        def close(self): self.closed=True
    guest_read, host_write = os.pipe()
    host_read, guest_write = os.pipe()
    transport=BoundedPipeTransport(host_read,host_write,timeout=2)
    os.close(host_read); os.close(host_write)
    lease=ReaderLease(IDENTITY,Policy(),transport,RUNTIME)
    driver=Driver(); guest=ReaderGuest(IDENTITY,lease.nonce,RUNTIME,Policy(),driver)
    errors=[]
    def run():
        try: serve_reader(guest,guest_read,guest_write,seconds=5)
        except Exception as e: errors.append(e)
    thread=threading.Thread(target=run);thread.start()
    original=resources(tmp_path)
    try:
        lease.start()
        lease.call({"action":"navigate","url":"https://example.com/"},original)
        assert lease.call({"action":"observe"},original)["result"]["text"]=="public"
        with pytest.raises(ValueError, match="截图成果暂不可用"):
            lease.call({"action":"screenshot"},original)
        assert original.collect()==[]
    finally:
        lease.close(); thread.join(timeout=3)
    assert not thread.is_alive() and driver.closed and errors==[]

def test_pipe_transport_times_out_and_closes_only_its_owned_fds():
    import os
    from app.agent_browser_runtime import BoundedPipeTransport
    guest_read, host_write=os.pipe(); host_read, guest_write=os.pipe()
    transport=BoundedPipeTransport(host_read,host_write,timeout=0.05)
    try:
        with pytest.raises(TimeoutError): transport.request({"a":1})
        with pytest.raises(OSError): os.fstat(transport._read_fd)
        with pytest.raises(OSError): os.fstat(transport._write_fd)
        os.fstat(host_read); os.fstat(host_write)
        os.fstat(guest_read); os.fstat(guest_write)
    finally:
        os.close(host_read); os.close(host_write)
        os.close(guest_read);os.close(guest_write)

def test_pipe_transport_rejects_oversized_request_without_writing():
    import os
    from app.agent_browser_runtime import BoundedPipeTransport, MAX_FRAME
    guest_read, host_write=os.pipe(); host_read, guest_write=os.pipe()
    transport=BoundedPipeTransport(host_read,host_write,timeout=1)
    try:
        with pytest.raises(ValueError): transport.request({"data":"x"*MAX_FRAME})
    finally:
        transport.close();os.close(host_read);os.close(host_write);os.close(guest_read);os.close(guest_write)


def test_pipe_transport_rejects_half_and_multiple_response_frames():
    import os
    import threading
    from app.agent_browser_runtime import BoundedPipeTransport
    for response, error in ((b'{"ok":', TimeoutError), (b'{"ok":1}\n{"ok":2}\n', ValueError)):
        guest_read, host_write = os.pipe(); host_read, guest_write = os.pipe()
        transport = BoundedPipeTransport(host_read, host_write, timeout=0.2)
        failures = []
        def respond():
            try:
                os.read(guest_read, 4096)
                os.write(guest_write, response)
            except Exception as exc:
                failures.append(exc)
        thread = threading.Thread(target=respond); thread.start()
        try:
            with pytest.raises(error):
                transport.request({"request": 1})
        finally:
            thread.join(timeout=1); transport.close()
            for fd in (guest_read, host_write, host_read, guest_write): os.close(fd)
        assert not thread.is_alive() and not failures

def test_pipe_transport_concurrent_close_and_original_fd_reuse_are_scoped():
    import os
    import threading
    from app.agent_browser_runtime import BoundedPipeTransport
    guest_read, host_write = os.pipe(); host_read, guest_write = os.pipe()
    transport = BoundedPipeTransport(host_read, host_write, timeout=2)
    original_fds = (host_read, host_write)
    os.close(host_read); os.close(host_write)
    unrelated_read, unrelated_write = os.pipe()
    assert {unrelated_read, unrelated_write} == set(original_fds)
    failures = []
    def request():
        try: transport.request({"request": 1})
        except Exception as exc: failures.append(exc)
    thread = threading.Thread(target=request); thread.start()
    try:
        assert os.read(guest_read, 4096)
        transport.close()
        thread.join(timeout=1)
        assert not thread.is_alive()
        assert len(failures) == 1 and isinstance(failures[0], PermissionError)
        transport.close()
        os.write(unrelated_write, b"x")
        assert os.read(unrelated_read, 1) == b"x"
    finally:
        transport.close(); thread.join(timeout=1)
        for fd in (guest_read, guest_write, unrelated_read, unrelated_write): os.close(fd)

def test_pipe_transport_rejects_wrong_direction_and_self_pipe():
    import os
    from app.agent_browser_runtime import BoundedPipeTransport
    read_fd, write_fd = os.pipe()
    other_read, other_write = os.pipe()
    try:
        try:
            transport = BoundedPipeTransport(read_fd, write_fd, timeout=0.2)
        except ValueError:
            transport = None  # Some systems identify both ends as the same inode.
        if transport is not None:
            try:
                with pytest.raises(ValueError, match="response must contain a result"):
                    transport.request({"request": 1})
            finally:
                transport.close()
        with pytest.raises(ValueError): BoundedPipeTransport(write_fd, other_read)
        for fd in (read_fd, write_fd, other_read, other_write): os.fstat(fd)
    finally:
        for fd in (read_fd, write_fd, other_read, other_write): os.close(fd)

def test_pipe_transport_refuses_result_in_request():
    import os
    from app.agent_browser_runtime import BoundedPipeTransport
    guest_read, host_write = os.pipe(); host_read, guest_write = os.pipe()
    transport = BoundedPipeTransport(host_read, host_write, timeout=0.2)
    try:
        with pytest.raises(ValueError, match="request must not contain a result"):
            transport.request({"result": {"ready": True}})
    finally:
        transport.close()
        for fd in (guest_read, host_write, host_read, guest_write): os.close(fd)


def test_private_pipe_factory_connects_distinct_guest_ends_and_closes_only_owned():
    import os
    import threading
    from app.agent_browser_runtime import BoundedPipeTransport
    transport, guest_read, guest_write = BoundedPipeTransport.create_pipe_pair(timeout=1)
    failures = []
    def respond():
        try:
            assert os.read(guest_read, 4096)
            os.write(guest_write, b'{"result":')
            threading.Event().wait(0.02)
            os.write(guest_write, b'{"ready":true}}' + bytes([10]))
        except Exception as exc:
            failures.append(exc)
    thread = threading.Thread(target=respond); thread.start()
    try:
        assert transport.request({"action": "start"}) == {"result": {"ready": True}}
        transport.close()
        os.fstat(guest_read); os.fstat(guest_write)
    finally:
        transport.close(); thread.join(timeout=1)
        os.close(guest_read); os.close(guest_write)
    assert not thread.is_alive() and not failures


@pytest.mark.parametrize("boundary", ["stopped", "expired"])
def test_guest_rechecks_stop_and_deadline_after_read_before_action(boundary):
    import os
    from app.agent_browser_guest import serve_reader
    class Guest:
        def __init__(self):
            self.calls = 0
            self.closed = False
        def handle(self, frame):
            self.calls += 1
            raise AssertionError("driver must not run after stop or expiry")
        def close(self):
            self.closed = True
    guest_read, host_write = os.pipe(); host_read, guest_write = os.pipe()
    guest = Guest()
    alive_values = iter([True, False]) if boundary == "stopped" else None
    clock_values = iter([0, 0, 0, 2]) if boundary == "expired" else None
    alive = (lambda: next(alive_values)) if alive_values is not None else (lambda: True)
    clock = (lambda: next(clock_values)) if clock_values is not None else (lambda: 0)
    try:
        os.write(host_write, b'{}' + bytes([10]))
        with pytest.raises(PermissionError, match="stopped before action"):
            serve_reader(guest, guest_read, guest_write, alive=alive, clock=clock, seconds=1)
        assert guest.calls == 0 and guest.closed
        with pytest.raises(OSError): os.fstat(guest_read)
        with pytest.raises(OSError): os.fstat(guest_write)
        os.fstat(host_read); os.fstat(host_write)
    finally:
        os.close(host_read); os.close(host_write)


class _HostFakeProcess:
    def __init__(self, events, exited=True):
        self.events, self.exited = events, exited
    def terminate(self):
        self.events.append("terminate")
    def has_exited(self):
        self.events.append("inspect")
        return self.exited

class _HostFakeTransport:
    def __init__(self, events):
        self.events = events
    def close(self):
        self.events.append("close")

def test_host_registry_rejects_forgery_cross_work_and_reuse():
    from app.agent_browser_runtime import ReaderHostRegistry
    events = []
    process = _HostFakeProcess(events)
    transport = _HostFakeTransport(events)
    registry = ReaderHostRegistry(lambda identity: (process, transport, RUNTIME))
    token = registry.start(IDENTITY)
    with pytest.raises(PermissionError): registry.claim(object(), IDENTITY)
    with pytest.raises(PermissionError): registry.claim(token, {**IDENTITY, "work_ref": "other"})
    assert events == []
    claimed_transport, claimed_runtime = registry.claim(token, IDENTITY)
    assert claimed_transport is transport and claimed_runtime == RUNTIME
    with pytest.raises(PermissionError): registry.claim(token, IDENTITY)
    with pytest.raises(ValueError, match="handle reuse"): registry.start(IDENTITY)
    assert registry.stop(token, IDENTITY) == "GONE"
    assert registry.stop(token, IDENTITY) == "GONE"
    assert events == ["close", "terminate", "inspect"]

def test_host_registry_expiry_closes_then_requests_exact_handle_termination():
    from app.agent_browser_runtime import ReaderHostRegistry
    events, now = [], [10]
    process = _HostFakeProcess(events)
    transport = _HostFakeTransport(events)
    registry = ReaderHostRegistry(lambda identity: (process, transport, RUNTIME),
                                  clock=lambda: now[0], seconds=1)
    token = registry.start(IDENTITY)
    now[0] = 11
    with pytest.raises(PermissionError, match="expired"): registry.claim(token, IDENTITY)
    assert events == ["close", "terminate", "inspect"]
    assert registry.stop(token, IDENTITY) == "GONE"

def test_host_registry_stop_without_exit_confirmation_stays_unknown():
    from app.agent_browser_runtime import ReaderHostRegistry
    events = []
    process = _HostFakeProcess(events, exited=False)
    registry = ReaderHostRegistry(lambda identity: (process, _HostFakeTransport(events), RUNTIME))
    token = registry.start(IDENTITY)
    assert registry.stop(token, IDENTITY) == "UNKNOWN"
    process.exited = True
    assert registry.stop(token, IDENTITY) == "UNKNOWN"
    with pytest.raises(PermissionError): registry.claim(token, IDENTITY)
    assert events == ["close", "terminate", "inspect"]


def test_work_bridge_requires_released_lock_and_verified_adapter(monkeypatch):
    import app.agent_browser_runtime as runtime
    calls = []
    def blocked():
        raise ValueError("lock not released")
    monkeypatch.setattr(runtime, "load_trusted_reader_lock", blocked)
    monkeypatch.setattr(runtime, "_open_verified_host_adapter", lambda lock: calls.append(lock))
    with pytest.raises(ValueError, match="尚未完成独立验证"):
        runtime.open_reader_for_work(IDENTITY, ["example.com"], lambda: False)
    assert calls == []

def test_work_bridge_default_adapter_is_unavailable(monkeypatch):
    import app.agent_browser_runtime as runtime
    with pytest.raises(ValueError, match="not released"):
        runtime.open_reader_for_work(IDENTITY, ["example.com"], lambda: False)

@pytest.mark.parametrize("kind", [None, "NATIVE_BROWSERSKILL", "UNKNOWN"])
def test_work_bridge_vm_rejects_other_backend_before_owner(monkeypatch, kind):
    import app.agent_browser_runtime as runtime
    import app.reader_vm_host as host
    monkeypatch.setattr(runtime, "load_trusted_reader_lock", lambda: {"runtimeKind": kind})
    monkeypatch.setattr(host, "open_owned_reader", lambda *args: pytest.fail("owner must not open"))
    with pytest.raises(ValueError, match="not released"):
        runtime.open_reader_for_work(IDENTITY, ["example.com"], lambda: False)


@pytest.mark.parametrize("failure", [False, True])
def test_work_bridge_vm_forwards_original_work_once_to_existing_owner(monkeypatch, failure):
    import app.agent_browser_runtime as runtime
    import app.reader_vm_host as host
    calls = []
    should_stop = lambda: False
    sentinel = object()
    monkeypatch.setattr(runtime, "load_trusted_reader_lock", lambda: {"runtimeKind": "VM"})
    monkeypatch.setattr(runtime, "_open_verified_host_adapter", lambda *args: pytest.fail("legacy adapter must not open"))
    def owned(identity, policy, stop):
        calls.append((identity.copy(), sorted(policy.hosts), stop))
        assert identity is not IDENTITY and stop is should_stop
        if failure:
            raise PermissionError("synthetic owner startup UNKNOWN")
        return sentinel  # Only open_owned_reader starts its lease; no second start here.
    monkeypatch.setattr(host, "open_owned_reader", owned)
    if failure:
        with pytest.raises(PermissionError, match="UNKNOWN"):
            runtime.open_reader_for_work(IDENTITY, ["example.com"], should_stop)
    else:
        assert runtime.open_reader_for_work(IDENTITY, ["example.com"], should_stop) is sentinel
    assert calls == [(IDENTITY, ["example.com"], should_stop)]


def _fixed_bridge_fixture(monkeypatch, *, exited=True):
    import app.agent_browser_runtime as runtime
    events = []
    image = "sha256:" + "a" * 64
    container = "b" * 64
    lock = {"browserImageDigest": image, "hostHelperClosure": {
        "dockerCliPath": "/opt/curis/bin/docker", "dockerCliSha256": "c" * 64,
        "dockerSocketPath": "/Users/Shared/curis-exec-20261029-vm01/d/docker.sock",
        "dockerConfigDir": "/Users/Shared/curis-exec-20261029-vm01/d",
        "guestWorkerPath": "/opt/curis/bin/reader-worker"}}
    class Handle:
        def close(self): events.append(("close",))
    class Adapter:
        def verified_runtime(self):
            return {"boot_id": "0" * 8 + "-" + "0" * 4 + "-" + "0" * 4 + "-" + "0" * 4 + "-" + "0" * 12,
                    "container_id": container, "image_digest": image}
        def start_fixed_exec(self, argv, identity):
            events.append(("start", argv, identity))
            return Handle()
        def stop_owned_container(self, which): events.append(("stop", which))
        def owned_container_exited(self, which):
            events.append(("inspect", which))
            return exited
    adapter = Adapter()
    monkeypatch.setattr(runtime, "load_trusted_reader_lock", lambda: lock)
    monkeypatch.setattr(runtime, "_open_verified_host_adapter", lambda value: adapter)
    return runtime, lock, adapter, events, container

def test_fixed_host_bridge_emits_only_locked_argv_and_owned_stop(monkeypatch):
    runtime, lock, adapter, events, container = _fixed_bridge_fixture(monkeypatch)
    bridge = runtime.FixedHostBridge(IDENTITY, lambda: False)
    bridge.start()
    command = events[0][1]
    assert command == (lock["hostHelperClosure"]["dockerCliPath"], "--host",
        "unix://" + lock["hostHelperClosure"]["dockerSocketPath"], "--config",
        lock["hostHelperClosure"]["dockerConfigDir"], "exec", "-i", container,
        lock["hostHelperClosure"]["guestWorkerPath"])
    with pytest.raises(PermissionError): bridge.stop({**IDENTITY, "work_ref": "foreign"})
    assert bridge.stop(IDENTITY) == "GONE"
    assert bridge.stop(IDENTITY) == "GONE"
    assert events[1:] == [("close",), ("stop", container), ("inspect", container)]

def test_fixed_host_bridge_unreleased_lock_never_opens_adapter(monkeypatch):
    import app.agent_browser_runtime as runtime
    calls = []
    def blocked(): raise ValueError("not released")
    monkeypatch.setattr(runtime, "load_trusted_reader_lock", blocked)
    monkeypatch.setattr(runtime, "_open_verified_host_adapter", lambda lock: calls.append(True))
    bridge = runtime.FixedHostBridge(IDENTITY, lambda: False)
    with pytest.raises(ValueError, match="not released"): bridge.start()
    assert calls == []

@pytest.mark.parametrize("tamper", ["socket", "command", "container", "image"])
def test_fixed_host_bridge_rejects_untrusted_target_before_exec(monkeypatch, tamper):
    runtime, lock, adapter, events, container = _fixed_bridge_fixture(monkeypatch)
    original = adapter.verified_runtime
    if tamper == "socket": lock["hostHelperClosure"]["dockerSocketPath"] = "/tmp/other.sock"
    if tamper == "command": lock["hostHelperClosure"]["guestWorkerPath"] = "/bin/sh -c bad"
    if tamper in ("container", "image"):
        def invalid():
            snapshot = original()
            snapshot["container_id" if tamper == "container" else "image_digest"] = "foreign"
            return snapshot
        adapter.verified_runtime = invalid
    with pytest.raises(ValueError):
        runtime.FixedHostBridge(IDENTITY, lambda: False).start()
    assert events == []

def test_fixed_host_bridge_unconfirmed_stop_stays_unknown(monkeypatch):
    runtime, _, _, events, container = _fixed_bridge_fixture(monkeypatch, exited=False)
    bridge = runtime.FixedHostBridge(IDENTITY, lambda: False)
    bridge.start()
    assert bridge.stop(IDENTITY) == "UNKNOWN"
    assert bridge.stop(IDENTITY) == "UNKNOWN"
    assert events[1:] == [("close",), ("stop", container), ("inspect", container)]


@pytest.mark.parametrize("response", [
    b'{"result":1,"result":2}\n',
    b'{"result":{"x":1,"x":2}}\n',
    b'{"result":NaN}\n',
    b'{"result":1e999}\n',
    b'{"result":{"nested":[-1e999]}}\n',
    b'{"result":"\xff"}\n',
    '{"result":1}'.encode("utf-16") + b"\n",
])
def test_pipe_transport_rejects_ambiguous_json_and_closes(response):
    import os
    import threading
    from app.agent_browser_runtime import BoundedPipeTransport
    transport, guest_read, guest_write = BoundedPipeTransport.create_pipe_pair(timeout=1)
    errors = []
    def reply():
        try:
            os.read(guest_read, 4096)
            os.write(guest_write, response)
        except Exception as error:
            errors.append(error)
    worker = threading.Thread(target=reply)
    worker.start()
    try:
        with pytest.raises(ValueError):
            transport.request({"action": "start"})
        with pytest.raises(PermissionError):
            transport.request({"action": "start"})
    finally:
        worker.join(timeout=2)
        transport.close()
        os.close(guest_read)
        os.close(guest_write)
    assert not worker.is_alive() and not errors


def test_reader_rejects_boolean_sequence_and_closes_lease():
    class BooleanSequenceTransport(Transport):
        def request(self, envelope):
            response = super().request(envelope)
            response["sequence"] = True
            return response
    transport = BooleanSequenceTransport()
    lease = ReaderLease(IDENTITY, Policy(), transport, RUNTIME)
    with pytest.raises(ValueError, match="identity mismatch"):
        lease.start()
    assert lease.closed and transport.closed == 1
    with pytest.raises(PermissionError):
        lease.start()
    assert len(transport.requests) == 1


@pytest.mark.parametrize("failure", ["identity", "revoked", "timeout"])
def test_reader_failed_inflight_request_closes_without_retry(failure):
    running = [True]
    class FailingTransport(Transport):
        def request(self, envelope):
            if failure == "timeout":
                self.requests.append(envelope)
                raise TimeoutError("fixture timeout")
            response = super().request(envelope)
            if failure == "identity":
                response["identity"] = {**response["identity"], "work_ref": "other"}
            if failure == "revoked":
                running[0] = False
            return response
    transport = FailingTransport()
    lease = ReaderLease(IDENTITY, Policy(), transport, RUNTIME, alive=lambda: running[0])
    with pytest.raises((ValueError, PermissionError, TimeoutError)):
        lease.start()
    assert lease.closed and transport.closed == 1
    with pytest.raises(PermissionError):
        lease.start()
    assert len(transport.requests) == 1


def test_reader_invalid_ready_closes_before_any_retry():
    class BadReady(Transport):
        def request(self, envelope):
            response = super().request(envelope)
            response["result"] = {"ready": False}
            return response
    transport = BadReady()
    lease = ReaderLease(IDENTITY, Policy(), transport, RUNTIME)
    with pytest.raises(ValueError, match="connection"):
        lease.start()
    assert lease.closed and transport.closed == 1
    with pytest.raises(PermissionError):
        lease.start()
    assert len(transport.requests) == 1


@pytest.mark.parametrize("tamper", ["missing_tab", "foreign_url", "policy_revoked"])
def test_reader_bad_navigation_response_closes_before_retry(tmp_path, tamper):
    class ConditionalPolicy:
        def __init__(self):
            self.allowed = True
        def url(self, url):
            if not self.allowed or url != "https://example.com/":
                raise ValueError("destination denied")
    policy = ConditionalPolicy()
    class BadNavigation(Transport):
        def request(self, envelope):
            response = super().request(envelope)
            if envelope["action"] == "navigate":
                if tamper == "missing_tab":
                    response["result"]["tab_id"] = ""
                elif tamper == "foreign_url":
                    response["result"]["url"] = "https://foreign.example/"
                else:
                    policy.allowed = False
            return response
    transport = BadNavigation()
    lease = ReaderLease(IDENTITY, policy, transport, RUNTIME).start()
    with pytest.raises(ValueError):
        lease.call({"action": "navigate", "url": "https://example.com/"}, resources(tmp_path))
    assert lease.closed and transport.closed == 1
    with pytest.raises(PermissionError):
        lease.start()
    assert len(transport.requests) == 2



@pytest.mark.parametrize("blocked_action", ["start", "observe"])
def test_reader_rejects_concurrent_operation_and_close_does_not_wait_for_lease_lock(tmp_path, blocked_action):
    import threading
    entered, release = threading.Event(), threading.Event()
    class BlockingTransport(Transport):
        def request(self, envelope):
            if envelope["action"] == blocked_action:
                entered.set()
                if not release.wait(2):
                    raise TimeoutError("fixture release timed out")
            return super().request(envelope)
    transport = BlockingTransport()
    lease = ReaderLease(IDENTITY, Policy(), transport, RUNTIME)
    resource = resources(tmp_path)
    if blocked_action == "observe":
        lease.start()
        lease.call({"action": "navigate", "url": "https://example.com/"}, resource)
    failures = []
    def run():
        try:
            if blocked_action == "start":
                lease.start()
            else:
                lease.call({"action": "observe"}, resource)
        except BaseException as error:
            failures.append(error)
    worker = threading.Thread(target=run)
    worker.start()
    try:
        assert entered.wait(2)
        with pytest.raises(PermissionError, match="already in progress"):
            lease.start()
        lease.close()
        assert lease.closed and transport.closed == 1
    finally:
        release.set()
        worker.join(timeout=2)
    assert not worker.is_alive()
    assert len(failures) == 1 and isinstance(failures[0], PermissionError)
    before_retry = len(transport.requests)
    with pytest.raises(PermissionError):
        lease.start()
    assert len(transport.requests) == before_retry



def test_registry_blocked_factory_does_not_block_another_work_stop():
    import threading
    from app.agent_browser_runtime import ReaderHostRegistry
    entered, release = threading.Event(), threading.Event()
    first = {**IDENTITY, "work_ref": "first"}
    second = {**IDENTITY, "work_ref": "second"}
    def factory(identity):
        if identity == second:
            entered.set()
            if not release.wait(2):
                raise TimeoutError("fixture")
        return _HostFakeProcess([]), _HostFakeTransport([]), RUNTIME
    registry = ReaderHostRegistry(factory)
    token = registry.start(first)
    worker = threading.Thread(target=lambda: registry.start(second))
    worker.start()
    stopper = None
    try:
        assert entered.wait(2)
        stopped = []
        stopper = threading.Thread(target=lambda: stopped.append(registry.stop(token, first)))
        stopper.start()
        stopper.join(timeout=0.5)
        assert not stopper.is_alive() and stopped == ["GONE"]
    finally:
        release.set()
        worker.join(timeout=2)
        if stopper is not None:
            stopper.join(timeout=2)


def test_registry_blocked_work_stop_does_not_block_other_work():
    import threading
    from app.agent_browser_runtime import ReaderHostRegistry
    entered, release = threading.Event(), threading.Event()
    first = {**IDENTITY, "work_ref": "first"}
    second = {**IDENTITY, "work_ref": "second"}
    class BlockingProcess(_HostFakeProcess):
        def terminate(self):
            entered.set()
            if not release.wait(2):
                raise TimeoutError("fixture")
            super().terminate()
    def factory(identity):
        process = BlockingProcess([]) if identity == first else _HostFakeProcess([])
        return process, _HostFakeTransport([]), RUNTIME
    registry = ReaderHostRegistry(factory)
    a, b = registry.start(first), registry.start(second)
    results = []
    worker = threading.Thread(target=lambda: results.append(registry.stop(a, first)))
    worker.start()
    stopper = None
    try:
        assert entered.wait(2)
        other = []
        stopper = threading.Thread(target=lambda: other.append(registry.stop(b, second)))
        stopper.start()
        stopper.join(timeout=0.5)
        assert not stopper.is_alive() and other == ["GONE"]
    finally:
        release.set()
        worker.join(timeout=2)
        if stopper is not None:
            stopper.join(timeout=2)
    assert results == ["GONE"]


def test_registry_concurrent_shared_handles_are_never_closed_on_rejection():
    import threading
    from app.agent_browser_runtime import ReaderHostRegistry
    barrier = threading.Barrier(2)
    events = []
    process, transport = _HostFakeProcess(events), _HostFakeTransport(events)
    def factory(identity):
        barrier.wait(timeout=2)
        return process, transport, RUNTIME
    registry = ReaderHostRegistry(factory)
    tokens, failures = [], []
    def run():
        try:
            tokens.append(registry.start(IDENTITY))
        except ValueError as error:
            failures.append(str(error))
    workers = [threading.Thread(target=run) for _ in range(2)]
    for worker in workers: worker.start()
    for worker in workers: worker.join(timeout=2)
    assert all(not worker.is_alive() for worker in workers)
    assert len(tokens) == len(failures) == 1 and events == []
    assert registry.stop(tokens[0], IDENTITY) == "GONE"
    assert events == ["close", "terminate", "inspect"]



def test_registry_rejects_untrusted_token_and_identity_without_callbacks():
    from app.agent_browser_runtime import ReaderHostRegistry
    events = []
    registry = ReaderHostRegistry(lambda identity: (_HostFakeProcess(events), _HostFakeTransport(events), RUNTIME))
    token = registry.start(IDENTITY)
    class BadToken:
        def __hash__(self):
            raise AssertionError("untrusted token hash must not run")
    class BadString(str):
        def __eq__(self, other):
            raise AssertionError("untrusted equality must not run")
    with pytest.raises(PermissionError):
        registry.stop(BadToken(), IDENTITY)
    with pytest.raises(PermissionError):
        registry.stop(token, {**IDENTITY, "work_ref": BadString("work")})
    assert registry.stop(token, IDENTITY) == "GONE"



def test_registry_binds_snapshot_before_blocking_factory():
    import threading
    from app.agent_browser_runtime import ReaderHostRegistry
    entered, release = threading.Event(), threading.Event()
    identity = dict(IDENTITY)
    seen = []
    def factory(value):
        seen.append(value.copy())
        entered.set()
        if not release.wait(2):
            raise TimeoutError("fixture")
        return _HostFakeProcess([]), _HostFakeTransport([]), RUNTIME
    registry = ReaderHostRegistry(factory)
    tokens = []
    worker = threading.Thread(target=lambda: tokens.append(registry.start(identity)))
    worker.start()
    try:
        assert entered.wait(2)
        identity["work_ref"] = "different"
    finally:
        release.set()
        worker.join(timeout=2)
    assert not worker.is_alive() and seen == [IDENTITY] and len(tokens) == 1
    with pytest.raises(PermissionError):
        registry.claim(tokens[0], identity)
    registry.claim(tokens[0], IDENTITY)
    assert registry.stop(tokens[0], IDENTITY) == "GONE"


def test_registry_rejects_identity_with_string_subclass_key():
    from app.agent_browser_runtime import ReaderHostRegistry
    class ForeignKey(str):
        pass
    identity = {ForeignKey(k) if k == "work_ref" else k: v for k, v in IDENTITY.items()}
    registry = ReaderHostRegistry(lambda identity: (_HostFakeProcess([]), _HostFakeTransport([]), RUNTIME))
    with pytest.raises(ValueError):
        registry.start(identity)


def test_guest_fd_handoff_closes_before_guest_close_on_setup_failure(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace
    from app.agent_browser_guest import serve_reader
    events, receipt = [], bytearray(1)
    monkeypatch.setattr(os, "fstat", lambda fd: SimpleNamespace(st_mode=stat.S_IFIFO))
    def set_blocking(fd, _):
        if fd == 9002:
            raise OSError("second setup failed")
    monkeypatch.setattr(os, "set_blocking", set_blocking)
    monkeypatch.setattr(os, "close", lambda fd: events.append(("close", fd)))
    guest = SimpleNamespace(close=lambda: events.append(("guest_close",)))
    with pytest.raises(OSError):
        serve_reader(guest, 9001, 9002, handoff=receipt)
    assert receipt == b"\x01"
    assert events == [("close", 9001), ("close", 9002), ("guest_close",)]


def test_guest_invalid_fd_does_not_transfer_or_close(monkeypatch):
    import os
    from app.agent_browser_guest import serve_reader
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(os, "close", lambda fd: closed.append(fd))
    with pytest.raises(ValueError):
        serve_reader(object(), 9001, 9001, handoff=receipt)
    assert receipt == b"\x00" and closed == []


def test_guest_interrupt_after_take_closes_transferred_fds(monkeypatch):
    import os
    import stat
    from types import SimpleNamespace
    from app.agent_browser_guest import serve_reader
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(os, "fstat", lambda fd: SimpleNamespace(st_mode=stat.S_IFIFO))
    monkeypatch.setattr(os, "set_blocking", lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    monkeypatch.setattr(os, "close", lambda fd: closed.append(fd))
    with pytest.raises(KeyboardInterrupt):
        serve_reader(SimpleNamespace(close=lambda: None), 9001, 9002, handoff=receipt)
    assert receipt == b"\x01" and closed == [9001, 9002]


def test_guest_interrupt_before_take_keeps_caller_ownership(monkeypatch):
    import os
    from app.agent_browser_guest import serve_reader
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(os, "fstat", lambda fd: (_ for _ in ()).throw(KeyboardInterrupt()))
    monkeypatch.setattr(os, "close", lambda fd: closed.append(fd))
    with pytest.raises(KeyboardInterrupt):
        serve_reader(object(), 9001, 9002, handoff=receipt)
    assert receipt == b"\x00" and closed == []


def test_reader_frame_cannot_mutate_original_work_identity():
    class MutatingTransport(Transport):
        def request(self, frame):
            frame["identity"]["company_id"] = "foreign"
            return super().request(frame)
    lease = ReaderLease(IDENTITY, Policy(), MutatingTransport(), RUNTIME)
    with pytest.raises(ValueError, match="identity mismatch"):
        lease.start()
    assert lease.identity == IDENTITY


def test_reader_failed_stop_is_retained_without_retry():
    calls = []
    class FailingTransport(Transport):
        def close(self):
            calls.append(True)
            raise OSError("synthetic stop failure")
    lease = ReaderLease(IDENTITY, Policy(), FailingTransport(), RUNTIME)
    with pytest.raises(OSError):
        lease.close()
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        lease.close()
    assert calls == [True]


@pytest.mark.parametrize("failure", [None, OSError, KeyboardInterrupt])
def test_reader_concurrent_close_reports_pending_without_duplicate_stop(failure):
    import threading
    entered, release = threading.Event(), threading.Event()
    calls, errors = [], []
    original_error = failure("synthetic stop failure") if failure else None
    class BlockingTransport(Transport):
        def close(self):
            calls.append(True)
            entered.set()
            if not release.wait(2):
                raise TimeoutError("test did not release stop")
            if original_error:
                raise original_error
    lease = ReaderLease(IDENTITY, Policy(), BlockingTransport(), RUNTIME)
    def close():
        try:
            lease.close()
        except BaseException as error:
            errors.append(error)
    worker = threading.Thread(target=close)
    worker.start()
    try:
        assert entered.wait(2)
        with pytest.raises(RuntimeError, match="pending.*UNKNOWN"):
            lease.close()
        assert lease.closed and lease.stop_state == "UNKNOWN" and calls == [True]
        with pytest.raises(PermissionError):
            lease.start()
    finally:
        release.set()
        worker.join(2)
    assert not worker.is_alive() and calls == [True]
    if original_error:
        assert len(errors) == 1 and errors[0] is original_error
        with pytest.raises(RuntimeError, match="failed.*UNKNOWN"):
            lease.close()
    else:
        assert errors == []
        lease.close()
    assert calls == [True] and lease.stop_state == "UNKNOWN"


def linux_driver_fixture():
    import time
    from pathlib import Path
    from app.agent_browser_guest import LinuxBrowserSkillDriver
    driver = object.__new__(LinuxBrowserSkillDriver)
    driver.policy = Policy()
    driver.nonce = "a" * 48
    driver.root = Path("/synthetic-reader-only")
    driver.environment = {"BSK_HOME": "/synthetic-reader-only/state", "BSK_AUTO_START": "0", "BSK_AUTO_UPDATE": "off"}
    driver.deadline = time.monotonic() + 88
    driver.stop_deadline = driver.deadline + 2
    driver.proxy_spki = "A" * 43 + "="
    driver.processes, driver.session, driver.tab, driver.browser = [], None, None, None
    driver.closed, driver.shutdown_evidence = False, None
    return driver


def test_linux_driver_uses_fixed_full_chromium_and_host_managed_bsk():
    from types import SimpleNamespace
    from app.agent_browser_guest import BSK_PATH, CHROMIUM_PATH, EXTENSION_PATH
    driver = linux_driver_fixture()
    launched, calls = [], []
    def spawn(argv):
        launched.append(argv)
        return SimpleNamespace(pid=101, poll=lambda: None)
    def rpc(method, params, **options):
        calls.append((method, params))
        if method == "system.status":
            return {"pid": 101, "daemon_version": "0.3.3", "browsers": [
                {"instance_id": "owned", "extension_version": "0.3.3"}]}
        assert method == "session.start" and params == {"browser_instance_id": "owned", "focused": False}
        return {"session_id": "daemon-created-session", "browser_instance_id": "owned", "agent_window_id": 12}
    driver._spawn, driver._rpc = spawn, rpc
    assert driver.start() == {"ready": True}
    assert launched[0][0] == BSK_PATH and "--foreground" in launched[0]
    assert launched[1][0] == "/usr/bin/Xvfb" and launched[1][-2:] == ["-nolisten", "tcp"]
    assert launched[2][0] == CHROMIUM_PATH and "headless_shell" not in CHROMIUM_PATH
    assert "--no-sandbox" not in launched[2] and "--disable-web-security" not in launched[2]
    assert "--load-extension=" + EXTENSION_PATH in launched[2]
    assert "--user-data-dir=/synthetic-reader-only/profile" in launched[2]
    assert "--proxy-server=http://172.30.253.2:8443" in launched[2]
    # Exempt only the already-approved proxy/loopback, never target DNS or proxy bypass.
    resolver = [arg.split("=", 1)[1] for arg in launched[2] if arg.startswith("--host-resolver-rules=")]
    assert len(resolver) == 1
    rules = [rule.strip() for rule in resolver[0].split(",")]
    assert rules[0] == "MAP * ~NOTFOUND" and len(rules) == 3
    assert set(rules[1:]) == {"EXCLUDE 127.0.0.1", "EXCLUDE 172.30.253.2"}
    assert "--proxy-bypass-list=<-loopback>;127.0.0.1:52800" in launched[2]
    assert "--no-proxy-server" not in launched[2]
    assert calls[-1] == ("session.start", {"browser_instance_id": "owned", "focused": False})
    assert driver.session == "daemon-created-session"


def test_linux_driver_rejects_missing_agent_window_and_closes_once():
    from types import SimpleNamespace
    driver = linux_driver_fixture()
    driver._spawn = lambda argv: SimpleNamespace(pid=101, poll=lambda: None)
    def rpc(method, params, **options):
        if method == "system.status":
            return {"pid": 101, "daemon_version": "0.3.3", "browsers": [
                {"instance_id": "owned", "extension_version": "0.3.3"}]}
        assert method == "session.start"
        return {"session_id": "daemon-created-session", "browser_instance_id": "owned"}
    driver._rpc = rpc
    closes = []
    driver.close = lambda: closes.append(True)
    with pytest.raises(ValueError, match="Agent Window"):
        driver.start()
    assert closes == [True]


def test_linux_driver_observe_adds_only_revalidated_owned_url():
    driver = linux_driver_fixture()
    driver.session, driver.tab = "owned-session", 7
    calls = []
    def rpc(method, params, **options):
        calls.append(method)
        if method == "tool.tab_list":
            return {"tabs": [{"tab_id": 7, "scope": "agent", "url": "https://example.com/"}]}
        return {"text": "self-authored public fixture"}  # Official observe need not return URL.
    driver._rpc = rpc
    result = driver.observe(7)
    assert result == {"text": "self-authored public fixture", "tab_id": 7, "url": "https://example.com/"}
    assert calls == ["tool.tab_list", "tool.observe", "tool.tab_list"]
    with pytest.raises(PermissionError):
        driver.observe(8)
    assert len(calls) == 3


@pytest.mark.parametrize("reached", ["timeout", None, "unknown", True, False, [], {}])
def test_linux_navigation_partial_timeout_result_is_not_adopted(reached):
    driver = linux_driver_fixture()
    driver.session = "owned"
    driver._rpc = lambda *args: {"tab_id": 7, "url": "https://example.com/", **({"reached": reached} if reached is not None else {})}
    with pytest.raises(ValueError, match="did not reach"):
        driver.navigate("https://example.com/")
    assert driver.tab is None


@pytest.mark.parametrize("failure", [None, "peer", "request_id", "tail"])
def test_linux_rpc_binds_kernel_daemon_peer_and_json_line(failure, monkeypatch):
    import json, socket, stat, struct
    from types import SimpleNamespace
    driver = linux_driver_fixture()
    driver.uid = 501
    driver.daemon = SimpleNamespace(pid=101, poll=lambda: None)
    driver.socket_path = SimpleNamespace(lstat=lambda: SimpleNamespace(st_mode=stat.S_IFSOCK | 0o600, st_uid=501))
    packets = []
    class Connection:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def settimeout(self, timeout): assert 0 < timeout <= 5
        def connect(self, path): pass
        def getsockopt(self, level, option, size):
            assert (level, option, size) == (socket.SOL_SOCKET, socket.SO_PEERCRED, 12)
            return struct.pack("3i", 999 if failure == "peer" else 101, 501, 501)
        def sendall(self, data):
            request = json.loads(data)
            response = (json.dumps({"id": "foreign" if failure == "request_id" else request["id"], "result": {"ok": True}}) + "\n").encode()
            if failure == "tail": response += b'{}\n'
            packets.extend([response[:5], response[5:]])
        def recv(self, count): return packets.pop(0)
    monkeypatch.setattr(socket, "SO_PEERCRED", 17, raising=False)
    monkeypatch.setattr(socket, "socket", lambda *args: Connection())
    if failure:
        with pytest.raises((PermissionError, ValueError)):
            driver._rpc("system.status", {})
    else:
        assert driver._rpc("system.status", {}) == {"ok": True}


@pytest.mark.parametrize("return_failure", [False, True])
def test_linux_stop_targets_only_owned_session_and_pidfds(return_failure, monkeypatch):
    import os, signal, subprocess
    driver = linux_driver_fixture()
    driver.session = "owned-only"
    requests, signals, closed = [], [], []
    class Process:
        returncode = None
        def poll(self): return self.returncode
        def wait(self, timeout):
            if self.returncode is None:
                self.returncode = 0
            return self.returncode
    driver.processes = [[Process(), 9001], [Process(), 9002]]
    def rpc(method, params, **options):
        requests.append((method, params, options))
        return {"stopped": [], "failed": [{"session_id": "owned-only"}], "return_failures": [{"tab_id": 7}]} if return_failure else {"stopped": ["owned-only"]}
    driver._rpc = rpc
    monkeypatch.setattr(signal, "pidfd_send_signal", lambda fd, sig: signals.append((fd, sig)), raising=False)
    monkeypatch.setattr(os, "close", lambda fd: closed.append(fd))
    result = driver.close()
    assert requests == [("session.stop", {"session_id": "owned-only"}, {"stopping": True})]
    assert signals == [(9002, signal.SIGTERM), (9001, signal.SIGTERM)] and closed == [9002, 9001]
    assert result["direct_children"] == "EXITED" and result["effects"] == result["descendants"] == "UNKNOWN"
    assert result["bsk_session"] == ("UNKNOWN" if return_failure else "STOP_RETURNED")
    assert driver.close() == result and len(requests) == 1 and len(signals) == 2


def test_linux_worker_gate_refuses_before_asset_or_directory_access(monkeypatch):
    import json
    from pathlib import Path
    from app import agent_browser_guest as guest
    monkeypatch.setattr(guest, "_linux_worker_preflight", lambda: "boot")
    reads = []
    def read(path, *args, **kwargs):
        reads.append(str(path))
        assert str(path) == guest.RUNTIME_MANIFEST_PATH
        return json.dumps({"executionAuthorized": False})
    monkeypatch.setattr(Path, "read_text", read)
    with pytest.raises(PermissionError, match="not released"):
        guest.LinuxBrowserSkillDriver({}, "a" * 48, {}, Policy(), "A" * 43 + "=")
    assert reads == [guest.RUNTIME_MANIFEST_PATH]


@pytest.mark.parametrize("error", [TimeoutError, ConnectionResetError, ValueError])
def test_linux_possibly_admitted_rpc_failure_stops_without_replay(error):
    driver = linux_driver_fixture()
    calls = []
    def exchange(*args, **kwargs):
        calls.append("exchange")
        driver._rpc_inflight = True
        raise error("synthetic failure after send")
    def close():
        calls.append("stop")
        driver.closed = True
    driver._exchange, driver.close = exchange, close
    with pytest.raises(error):
        driver._rpc("tool.navigate", {})
    assert calls == ["exchange", "stop"]
    with pytest.raises(PermissionError):
        driver._active()


@pytest.mark.parametrize("reached", ["commit", "domcontentloaded", "load", "networkidle"])
def test_linux_navigation_accepts_official_lifecycle_strings_and_owned_tab(reached):
    driver = linux_driver_fixture()
    driver.session = "daemon-session"
    calls = []
    def rpc(method, params):
        calls.append((method, params))
        if method == "tool.navigate":
            assert params == {"session_id": "daemon-session", "url": "https://example.com/",
                              "wait_until": "domcontentloaded", "timeout_ms": 10000}
            return {"tab_id": 7, "url": "https://example.com/", "final_url": "https://example.com/", "reached": reached}
        assert method == "tool.tab_list" and params == {"session_id": "daemon-session", "scope": "agent"}
        return {"tabs": [{"tab_id": 7, "scope": "agent", "url": "https://example.com/"}]}
    driver._rpc = rpc
    assert driver.navigate("https://example.com/") == {"tab_id": 7, "url": "https://example.com/"}
    assert driver.tab == 7 and len(calls) == 2


@pytest.mark.parametrize("field,value", [("session_id", None), ("session_id", ""),
    ("browser_instance_id", "foreign"), ("agent_window_id", True)])
def test_linux_session_start_rejects_wrong_official_binding(field, value):
    from types import SimpleNamespace
    driver = linux_driver_fixture()
    driver._spawn = lambda argv: SimpleNamespace(pid=101, poll=lambda: None)
    def rpc(method, params, **options):
        if method == "system.status":
            return {"pid": 101, "daemon_version": "0.3.3", "browsers": [{"instance_id": "owned", "extension_version": "0.3.3"}]}
        assert method == "session.start" and "session_id" not in params
        result = {"session_id": "actual-session", "browser_instance_id": "owned", "agent_window_id": 12}
        result[field] = value
        return result
    driver._rpc = rpc
    stopped = []
    driver.close = lambda: stopped.append(driver.session)
    with pytest.raises(ValueError): driver.start()
    assert stopped == (["actual-session"] if field == "agent_window_id" else [None])


@pytest.mark.parametrize("reply", [{}, {"stopped": []}, {"stopped": ["foreign"]},
    {"stopped": ["owned-only"], "failed": [{"session_id": "owned-only"}]},
    {"stopped": ["owned-only"], "return_failures": [{"tab_id": 7}]}])
def test_linux_session_stop_requires_exact_actual_id_and_no_failures(reply):
    driver = linux_driver_fixture()
    driver.session = "owned-only"
    def rpc(method, params, **options):
        assert method == "session.stop" and params == {"session_id": "owned-only"} and options == {"stopping": True}
        return reply
    driver._rpc = rpc
    assert driver.close()["bsk_session"] == "UNKNOWN"



def test_reserved_owner_nonce_is_used_in_first_frame_without_second_generation(monkeypatch):
    import app.agent_browser_runtime as runtime
    reserved="0123456789abcdef"*3
    def forbidden(*args): raise AssertionError("reserved Work generated a second nonce")
    monkeypatch.setattr(runtime.secrets,"token_hex",forbidden)
    class ReservedTransport(Transport):
        def request(self,frame):
            assert frame["identity"]==IDENTITY and frame["nonce"]==reserved
            return super().request(frame)
    transport=ReservedTransport()
    lease=runtime.ReaderLease(IDENTITY,Policy(),transport,RUNTIME,nonce=reserved)
    assert lease.nonce==lease.session==reserved and transport.requests==[]
    lease.start()
    assert len(transport.requests)==1 and transport.requests[0]["nonce"]==reserved
    assert transport.requests[0]["sequence"]==1


@pytest.mark.parametrize("nonce", ["", "a"*47, "a"*49, "A"*48, "g"*48, "a"*47+"\n", b"a"*48, 1, True, [], {}])
def test_invalid_reserved_nonce_rejected_before_lock_clock_random_or_transport(monkeypatch,nonce):
    import app.agent_browser_runtime as runtime
    def forbidden(*args): raise AssertionError("invalid nonce caused an operation")
    monkeypatch.setattr(runtime,"load_trusted_reader_lock",forbidden)
    monkeypatch.setattr(runtime.secrets,"token_hex",forbidden)
    with pytest.raises(ValueError,match="reserved nonce"):
        runtime.ReaderLease(IDENTITY,Policy(),object(),RUNTIME,nonce=nonce,clock=forbidden)


def test_default_reader_nonce_still_generates_once_and_reuses_it(monkeypatch):
    import app.agent_browser_runtime as runtime
    calls=[]
    def generate(length): calls.append(length);return "b"*48
    monkeypatch.setattr(runtime.secrets,"token_hex",generate)
    transport=Transport()
    lease=runtime.ReaderLease(IDENTITY,Policy(),transport,RUNTIME).start()
    assert calls==[24] and lease.nonce==lease.session=="b"*48
    assert transport.requests[0]["nonce"]=="b"*48


@pytest.mark.parametrize("change", [{"complete":False},{"executionAuthorized":False},{"image_digest":"sha256:foreign"}])
def test_reserved_nonce_cannot_bypass_runtime_or_image_gate(change):
    transport=Transport()
    with pytest.raises(ValueError):
        ReaderLease(IDENTITY,Policy(),transport,{**RUNTIME,**change},nonce="a"*48)
    assert transport.requests==[]



def native_entry_fixture(monkeypatch, *, failure=None):
    import app.agent_browser_runtime as module
    import app.agent_browser as native
    from app.agent_browser_policy import PublicTargets
    events,stopped=[],[False]
    monkeypatch.setattr(module,"load_trusted_reader_lock",lambda:{"runtimeKind":"NATIVE_BROWSERSKILL"})
    class Lease:
        def __init__(self,root,identity,metadata,hosts,*,alive):
            self.identity=identity.copy();self.policy=PublicTargets(hosts);self.alive=alive
            self.session,self.browser_id,self.tab="actual-session","owned-browser",None
            events.append(("create",str(root),identity.copy(),metadata.copy(),tuple(hosts)))
            if failure=="create-revoke":stopped[0]=True
        def start(self):
            events.append(("start",))
            if failure=="start":raise ValueError("synthetic start failure")
            if failure=="start-revoke":stopped[0]=True
            if failure=="identity":self.identity["work_ref"]="foreign"
            if failure=="hosts":self.policy=PublicTargets(["foreign.example.com"])
            return object() if failure=="handle" else self
        def close(self):events.append(("close",))
    monkeypatch.setattr(native,"BrowserLease",Lease)
    return module,events,stopped


def test_native_work_entry_uses_existing_lease_and_filters_model_metadata(monkeypatch):
    module,events,stopped=native_entry_fixture(monkeypatch)
    metadata={"browser_skill_path":"/synthetic/bsk","api_key":"SYNTHETIC_PRIVATE","model_name":"model"}
    lease=module.open_native_browser_for_work(IDENTITY,["example.com"],lambda:stopped[0],
        root="/synthetic-owned/agent-browser",metadata=metadata)
    assert events==[("create","/synthetic-owned/agent-browser",IDENTITY,{"browser_skill_path":"/synthetic/bsk"},("example.com",)),("start",)]
    assert lease.identity==IDENTITY and lease.alive() and metadata["api_key"]=="SYNTHETIC_PRIVATE"
    stopped[0]=True
    assert not lease.alive()


@pytest.mark.parametrize("failure",["create-revoke","start","start-revoke","identity","hosts","handle"])
def test_native_work_entry_closes_original_handle_on_failure_or_binding_drift(monkeypatch,failure):
    module,events,stopped=native_entry_fixture(monkeypatch,failure=failure)
    with pytest.raises((ValueError,PermissionError)):
        module.open_native_browser_for_work(IDENTITY,["example.com"],lambda:stopped[0],
            root="/synthetic-owned/agent-browser",metadata={})
    assert events[-1]==("close",) and sum(e[0]=="create" for e in events)==1
    assert sum(e[0]=="start" for e in events)==(0 if failure=="create-revoke" else 1)


@pytest.mark.parametrize("failure",["vm-release","relative-root","wrong-root","personal-profile","executable","metadata","stopped","identity","hosts"])
def test_native_entry_rejects_unreleased_or_unscoped_requests_before_creation(monkeypatch,failure):
    module,events,stopped=native_entry_fixture(monkeypatch)
    root,metadata,identity,hosts="/synthetic-owned/agent-browser",{},IDENTITY,["example.com"]
    if failure=="vm-release":monkeypatch.setattr(module,"load_trusted_reader_lock",lambda:{"runtimeKind":"VM"})
    if failure=="relative-root":root="relative/agent-browser"
    if failure=="wrong-root":root="/synthetic-personal/Chrome"
    if failure=="personal-profile":monkeypatch.setenv("CURIS_AGENT_BROWSER_PROFILE","/synthetic-personal-profile")
    if failure=="executable":metadata={"browser_chrome_path":"/synthetic-unapproved/program"}
    if failure=="metadata":metadata=[]
    if failure=="stopped":stopped[0]=True
    if failure=="identity":identity={**IDENTITY,"tenant_id":""}
    if failure=="hosts":hosts=["localhost"]
    with pytest.raises((ValueError,PermissionError)):
        module.open_native_browser_for_work(identity,hosts,lambda:stopped[0],root=root,metadata=metadata)
    assert events==[]



def test_native_entry_cleanup_failure_preserves_start_error_and_unknown(monkeypatch):
    import app.agent_browser as native
    module,events,stopped=native_entry_fixture(monkeypatch,failure="start")
    def fail_close(self):events.append(("close-failed",));raise KeyboardInterrupt("synthetic cleanup interruption")
    monkeypatch.setattr(native.BrowserLease,"close",fail_close)
    with pytest.raises(ValueError,match="synthetic start failure") as error:
        module.open_native_browser_for_work(IDENTITY,["example.com"],lambda:False,
            root="/synthetic-owned/agent-browser",metadata={})
    assert events[-1]==("close-failed",) and any("UNKNOWN" in note for note in error.value.__notes__)


@pytest.mark.parametrize("failure", [None, "open", "signal", "close"])
def test_linux_preflight_probes_actual_pidfd_permissions_and_closes(monkeypatch, failure):
    import os, signal, sys
    from pathlib import Path
    from app import agent_browser_guest as guest
    calls = []
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(os, "geteuid", lambda: 1000)
    monkeypatch.setattr(os, "getpid", lambda: 1234)
    def read(path):
        if str(path) == "/proc/self/status":
            return "NoNewPrivs:\t1\nSeccomp:\t2\nCapEff:\t00000000\n"
        assert str(path) == "/proc/sys/kernel/random/boot_id"
        calls.append("boot")
        return "boot-id\n"
    def open_pidfd(pid, flags):
        calls.append(("open", pid, flags))
        if failure == "open":
            raise PermissionError("synthetic denied syscall")
        return 91
    def send(fd, sig, info, flags):
        calls.append(("signal", fd, sig, info, flags))
        if failure == "signal":
            raise PermissionError("synthetic denied syscall")
    def close(fd):
        calls.append(("close", fd))
        if failure == "close":
            raise OSError("synthetic close failure")
    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(os, "pidfd_open", open_pidfd, raising=False)
    monkeypatch.setattr(signal, "pidfd_send_signal", send, raising=False)
    monkeypatch.setattr(os, "close", close)
    if failure:
        with pytest.raises(OSError):
            guest._linux_worker_preflight()
    else:
        assert guest._linux_worker_preflight() == "boot-id"
    assert calls == ([("open", 1234, 0)] if failure == "open" else
                     [("open", 1234, 0), ("signal", 91, 0, None, 0), ("close", 91)]
                     + ([] if failure else ["boot"]))


def test_pidfd_seccomp_only_allows_zero_flags_and_probe_or_stop_signals():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    policy = json.loads((root / "backend/app/reader_seccomp.json").read_text())
    assert policy["defaultAction"] == "SCMP_ACT_ERRNO"
    rules = [rule for rule in policy["syscalls"] if any("pidfd" in name for name in rule["names"])]
    def arg(index, value):
        return {"index": index, "value": value, "valueTwo": 0, "op": "SCMP_CMP_EQ"}
    assert len(rules) == 4
    for rule, name, args in zip(rules,
            ["pidfd_open"] + ["pidfd_send_signal"] * 3,
            [[arg(1, 0)]] + [[arg(1, sig), arg(2, 0), arg(3, 0)] for sig in (0, 15, 9)]):
        assert rule["names"] == [name] and rule["action"] == "SCMP_ACT_ALLOW"
        assert rule["args"] == args and rule["includes"] == rule["excludes"] == {}


@pytest.mark.parametrize("mode", ["missing", "denied", "escalate"])
def test_linux_pidfd_stop_never_falls_back_to_numeric_pid(monkeypatch, mode):
    import os, signal, subprocess
    driver = linux_driver_fixture()
    calls = []
    class Process:
        returncode = None
        def poll(self): return self.returncode
        def wait(self, timeout):
            calls.append("wait")
            if calls.count("wait") == 1:
                raise subprocess.TimeoutExpired("synthetic", timeout)
            self.returncode = -9
            return self.returncode
    driver.processes = [[Process(), None if mode == "missing" else 91]]
    def send(fd, sig):
        calls.append((fd, sig))
        if mode == "denied":
            raise PermissionError("synthetic denied syscall")
    def forbidden(*args, **kwargs):
        pytest.fail("numeric PID signalling is forbidden")
    monkeypatch.setattr(signal, "pidfd_send_signal", send, raising=False)
    monkeypatch.setattr(os, "kill", forbidden)
    monkeypatch.setattr(os, "killpg", forbidden)
    monkeypatch.setattr(os, "close", lambda fd: calls.append(("close", fd)))
    result = driver.close()
    assert result["direct_children"] == ("EXITED" if mode == "escalate" else "UNKNOWN")
    assert result["descendants"] == result["effects"] == "UNKNOWN"
    assert calls == ({"missing": [], "denied": [(91, signal.SIGTERM), ("close", 91)],
                      "escalate": [(91, signal.SIGTERM), "wait", (91, signal.SIGKILL), "wait", ("close", 91)]}[mode])
    assert driver.close() == result


# BrowserSkill d9a78aed frame.rs serializes exactly one result/error body;
# error.rs uses these fixed snake_case codes, never numeric JSON-RPC codes.
@pytest.mark.parametrize("payload,expected", [
    ({"id": "request-id", "result": {"tab_id": 7, "url": "https://example.com/", "reached": "domcontentloaded"}}, None),
    ({"id": "request-id", "result": None}, None),
    ([], "TYPE_INVALID"),
    ({"id": "DO_NOT_EMIT", "result": {}}, "ID_MISMATCH"),
    ({"id": "request-id"}, "RESULT_MISSING"),
    ({"id": "request-id", "result": {}, "error": None}, "BODY_AMBIGUOUS"),
    ({"id": "request-id", "error": None}, "ERROR_INVALID"),
    ({"id": "request-id", "error": {"code": 123, "message": "DO_NOT_EMIT"}}, "ERROR_INVALID"),
    ({"id": "request-id", "error": {"code": "cdp_failed", "message": None}}, "ERROR_INVALID"),
    ({"id": "request-id", "error": {"code": "DO_NOT_EMIT", "message": "DO_NOT_EMIT", "data": {"private": "DO_NOT_EMIT"}}}, "RPC_ERROR_other"),
    (b'{"id":"request-id","result":{},"result":{"private":"DO_NOT_EMIT"}}\n', "JSON_INVALID"),
    (b'\xff\n', "JSON_INVALID"),
] + [({"id": "request-id", "error": {"code": code, "message": "DO_NOT_EMIT", "data": {"private": "DO_NOT_EMIT"}}}, "RPC_ERROR_" + code + (" REASON=OTHER PAGE_NAVIGATE_REJECTED=NO NET=OTHER" if code == "cdp_failed" else ""))
     for code in ["unknown_method", "unsupported", "invalid_params", "not_found", "permission_denied", "timeout",
                  "cdp_failed", "protocol_error", "cancelled", "user_aborted", "version_too_old",
                  "multiple_browsers_online", "no_browser_connected"]
] + [({"id": "request-id", "error": {"code": "cdp_failed", "message": message, "data": data}},
      "RPC_ERROR_cdp_failed REASON=" + reason + " PAGE_NAVIGATE_REJECTED=" + page + " NET=" + net)
     for data, message, reason, page, net in [
         ({"reason": "cdp_extension_access_denied", "private": "DO_NOT_EMIT"}, "DO_NOT_EMIT", "CDP_EXTENSION_ACCESS_DENIED", "NO", "OTHER"),
         ({"reason": "renderer_read_timeout"}, "DO_NOT_EMIT", "RENDERER_READ_TIMEOUT", "NO", "OTHER"),
         ({"reason": "DO_NOT_EMIT"}, "DO_NOT_EMIT", "OTHER", "NO", "OTHER"),
         ({"reason": ["DO_NOT_EMIT"]}, "DO_NOT_EMIT", "OTHER", "NO", "OTHER"),
         (None, "DO_NOT_EMIT", "OTHER", "NO", "OTHER"),
         (["DO_NOT_EMIT"], "DO_NOT_EMIT", "OTHER", "NO", "OTHER"),
         ({}, "Page.navigate rejected: net::ERR_DO_NOT_EMIT", "OTHER", "YES", "OTHER"),
         ({}, "Page.navigate rejected: net::ERR_PROXY_CONNECTION_FAILED https://private.example/DO_NOT_EMIT", "OTHER", "YES", "OTHER"),
         ({}, "net::ERR_PROXY_CONNECTION_FAILED", "OTHER", "NO", "OTHER"),
     ] + [({}, "Page.navigate rejected: net::" + net, "OTHER", "YES", net)
          for net in ["ERR_ABORTED", "ERR_TIMED_OUT", "ERR_BLOCKED_BY_CLIENT", "ERR_CONNECTION_CLOSED",
                      "ERR_CONNECTION_RESET", "ERR_CONNECTION_REFUSED", "ERR_NAME_NOT_RESOLVED",
                      "ERR_TUNNEL_CONNECTION_FAILED", "ERR_PROXY_CONNECTION_FAILED", "ERR_PROXY_CERTIFICATE_INVALID",
                      "ERR_CERT_AUTHORITY_INVALID", "ERR_EMPTY_RESPONSE"]]])
def test_linux_rpc_official_result_error_shapes_have_fixed_private_safe_classification(monkeypatch, payload, expected):
    import json, socket, stat, struct, secrets
    from types import SimpleNamespace
    driver = linux_driver_fixture()
    driver.uid = 501
    driver.daemon = SimpleNamespace(pid=101, poll=lambda: None)
    driver.socket_path = SimpleNamespace(lstat=lambda: SimpleNamespace(st_mode=stat.S_IFSOCK | 0o600, st_uid=501))
    packets, sent = [], []
    class Connection:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def settimeout(self, timeout): assert 0 < timeout <= 0.25
        def connect(self, path): pass
        def getsockopt(self, *args): return struct.pack("3i", 101, 501, 501)
        def sendall(self, data):
            frame = json.loads(data)
            assert frame == {"id": "request-id", "method": "tool.navigate", "params": {"session_id": "owned", "url": "https://example.com/", "wait_until": "domcontentloaded", "timeout_ms": 10000}}
            sent.append(frame)
            raw = payload if isinstance(payload, bytes) else (json.dumps(payload) + "\n").encode()
            packets.extend([raw[:3], raw[3:]])
        def recv(self, size): return packets.pop(0)
    monkeypatch.setattr(socket, "SO_PEERCRED", 17, raising=False)
    monkeypatch.setattr(socket, "socket", lambda *args: Connection())
    monkeypatch.setattr(secrets, "token_hex", lambda *args: "request-id")
    params = {"session_id": "owned", "url": "https://example.com/", "wait_until": "domcontentloaded", "timeout_ms": 10000}
    if expected:
        with pytest.raises(ValueError) as error: driver._rpc("tool.navigate", params)
        assert str(error.value) == ("Reader BSK " if expected.startswith("RPC_ERROR_") else "Reader BSK response ") + expected
        assert "DO_NOT_EMIT" not in str(error.value) and "private.example" not in str(error.value) and driver.closed
        with pytest.raises(PermissionError): driver._active()
    else:
        assert driver._rpc("tool.navigate", params) == payload["result"]
        assert not driver.closed and driver._rpc_inflight is False
    assert len(sent) == 1


@pytest.mark.parametrize("outcome", ["after-five-seconds", "cancel", "lease-expired", "ipc-expired"])
def test_linux_navigation_receive_budget_is_longer_than_tool_and_remains_cancellable(monkeypatch, outcome):
    import json, socket, stat, struct, secrets, time
    from types import SimpleNamespace
    from app import agent_browser_guest as guest, reader_vm_host as host
    assert guest.BSK_NAVIGATE_TIMEOUT_MS / 1000 + 2 < guest.BSK_NAVIGATE_IPC_SECONDS
    assert guest.BSK_NAVIGATE_IPC_SECONDS + guest.BSK_IPC_SECONDS < host._READER_ATTACH_TIMEOUT_SECONDS < 88
    driver = linux_driver_fixture()
    now, calls = [100.0], []
    driver.deadline, driver.stop_deadline = 120, 122
    driver.uid = 501
    driver.daemon = SimpleNamespace(pid=101, poll=lambda: None)
    driver.socket_path = SimpleNamespace(lstat=lambda: SimpleNamespace(st_mode=stat.S_IFSOCK | 0o600, st_uid=501))
    class Connection:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def settimeout(self, timeout):
            assert 0 < timeout <= (0.05 if "recv" in calls else 0.25)
        def connect(self, path): pass
        def getsockopt(self, *args): return struct.pack("3i", 101, 501, 501)
        def sendall(self, data): calls.append("send")
        def recv(self, size):
            calls.append("recv")
            if calls.count("recv") == 1:
                now[0] = 114 if outcome == "ipc-expired" else 106
                if outcome == "cancel": driver.closed = True
                if outcome == "lease-expired": driver.deadline = 105
                raise socket.timeout()
            return b'{"id":"request-id","result":{"ok":true}}\n'
    monkeypatch.setattr(socket, "SO_PEERCRED", 17, raising=False)
    monkeypatch.setattr(socket, "socket", lambda *args: Connection())
    monkeypatch.setattr(secrets, "token_hex", lambda *args: "request-id")
    monkeypatch.setattr(time, "monotonic", lambda: now[0])
    if outcome == "after-five-seconds":
        assert driver._rpc("tool.navigate", {}) == {"ok": True}
        assert calls == ["send", "recv", "recv"]
    else:
        with pytest.raises(TimeoutError if outcome == "ipc-expired" else PermissionError):
            driver._rpc("tool.navigate", {})
        assert calls == ["send", "recv"] and driver.closed


def test_public_browser_release_requires_bundled_assets_and_stop_evidence(tmp_path, monkeypatch):
    from app import agent_browser_runtime as runtime
    from backend.tests.test_agent_browser_packaging import assets_fixture, install_fixture, activate_fixture
    values = assets_fixture(tmp_path)
    lock, _, _, _, _ = values
    root = tmp_path / 'installed'
    expected = install_fixture(root, values)
    activate_fixture(monkeypatch, root, expected)
    monkeypatch.setattr(runtime, 'load_trusted_reader_lock', _bundled_lock_loader)
    assert runtime.agent_browser_release()['cliPath'] == str(root / runtime.BROWSER_BUNDLE_PATHS['cliPath'])
    monkeypatch.setattr(runtime, 'load_trusted_reader_lock', lambda: lock)
    profile = lock['agentBrowser']
    profile['identity'] = {'company_id': 'private-grant'}
    with pytest.raises(ValueError): runtime.agent_browser_release()
    profile.pop('identity')
    profile['stopEvidenceSha256'] = ''
    with pytest.raises(ValueError): runtime.agent_browser_release()
    profile['stopEvidenceSha256'] = 'a' * 64
    with pytest.raises(ValueError): runtime.agent_browser_release()


def test_public_browser_supervisor_allows_only_pinned_daemon_and_owned_directory(tmp_path, monkeypatch):
    import json
    from app import agent_browser_runtime as runtime
    from app.agent_work_resources import scope_key
    identity = dict(IDENTITY)
    temporary = tmp_path / 'short'; temporary.mkdir(mode=0o700)
    release = {'temporaryRoot': str(temporary), 'releaseSha256': 'a' * 64,
        'cliPath': '/fixture/verified-cli', 'cliSha256': 'b' * 64}
    monkeypatch.setattr(runtime, 'agent_browser_release', lambda **kw: release)
    monkeypatch.setattr(runtime, '_pinned_browser_asset', lambda path, sha: path)
    directory = temporary / scope_key(**{k: identity[k] for k in ('tenant_id', 'company_id', 'work_ref', 'task_id')})[:16]
    directory.mkdir(mode=0o700)
    for name in ('s', 'home', 'tmp', 'config', 'cache'): (directory / name).mkdir(mode=0o700)
    (temporary / 'release.json').write_text(json.dumps({'runtimeKind': 'NATIVE_AGENT_BROWSER', 'releaseSha256': 'a' * 64}))
    (directory / 'owner.json').write_text(json.dumps(identity))
    (directory / 's/012345abcdef.config').write_text('{"debug":false}')
    env = {**runtime.browser_environment(directory, '012345abcdef'), 'AGENT_BROWSER_DAEMON': '1'}
    valid = {'command': [release['cliPath']], 'cwd': str(directory), 'environment': env, 'prompt': ''}
    runtime.validate_browser_supervisor_request(valid)
    for change in ({'command': ['/bin/sh']}, {'command': [release['cliPath'], 'open', 'https://example.org']},
            {'prompt': 'arbitrary'}, {'environment': {**env, 'TOKEN': 'fixture'}}, {'cwd': str(tmp_path)}):
        with pytest.raises(ValueError): runtime.validate_browser_supervisor_request({**valid, **change})
    (directory / 'owner.json').write_text(json.dumps({**identity, 'task_id': 'foreign'}))
    with pytest.raises(ValueError): runtime.validate_browser_supervisor_request(valid)


def test_unreleased_public_browser_never_bypasses_agent_or_starts_helper(monkeypatch):
    from app import agent_adapter, agent_browser_runtime as runtime
    monkeypatch.setattr(agent_adapter, '_run_agent_supervisor_candidate', lambda **kw: pytest.fail('unreleased helper started'))
    assert runtime.run_browser_supervisor() == 2
    assert agent_adapter.CODEX_STOP_VERIFIED is False
    assert agent_adapter.run_agent_supervisor() == 2


def test_browser_request_validator_rejects_before_any_supervisor_child(monkeypatch, tmp_path):
    import io
    import json
    import stat
    from types import SimpleNamespace
    from app import agent_adapter as module
    request = {'command': ['/fixture/browser'], 'cwd': str(tmp_path), 'environment': {},
        'prompt': '', 'timeout': 2, 'nonce': 'a' * 32}
    class Input:
        def fileno(self): return 123
    class Status(io.StringIO):
        def fileno(self): return 124
    checked = []
    def reject(value):
        checked.append(value)
        raise ValueError('not a released browser request')
    monkeypatch.setattr(module.sys, 'stdin', Input())
    monkeypatch.setattr(module.sys, 'stderr', Status())
    monkeypatch.setattr(module.os, 'getpid', lambda: 100)
    monkeypatch.setattr(module.os, 'getsid', lambda _: 100)
    monkeypatch.setattr(module.os, 'getpgrp', lambda: 100)
    monkeypatch.setattr(module.os, 'fstat', lambda _: SimpleNamespace(st_mode=stat.S_IFIFO))
    monkeypatch.setattr(module.os, 'set_inheritable', lambda *a: None)
    monkeypatch.setattr(module.os, 'set_blocking', lambda *a: None)
    monkeypatch.setattr(module.os, 'read', lambda *a: (json.dumps(request) + '\n').encode())
    monkeypatch.setattr(module.select, 'select', lambda r, *a: (r, [], []))
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *a, **kw: pytest.fail('invalid browser request spawned'))
    assert module._run_agent_supervisor_candidate(request_validator=reject) == 2
    assert checked == [request]
