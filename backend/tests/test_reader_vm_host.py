import pytest

from app import reader_vm_host as host
from app.agent_browser_runtime import ReaderLease

IDENTITY = {"tenant_id":"tenant", "company_id":"company", "work_ref":"work", "task_id":"task",
            "employee_id":"employee", "binding_ref":"binding"}
RUNTIME = {"complete":True, "executionAuthorized":True, "boot_id":"boot", "container_id":"container",
           "image_digest":"sha256:fixture"}


class Policy:
    def url(self, url):
        if url != "https://example.com/":
            raise ValueError("foreign URL")


class Transport:
    def __init__(self, events):
        self.events = events
    def request(self, frame):
        self.events.append(("request", frame["action"], frame["nonce"]))
        return {**{k:frame[k] for k in ("identity","nonce","sequence","boot_id","container_id","image_digest")},
                "result":{"ready":True}}
    def close(self):
        self.events.append(("close",))


class Owner:
    def __init__(self, events):
        self.events = events
        self.runtime = dict(RUNTIME)
    def verified_snapshot(self, identity):
        self.events.append(("snapshot", identity))
        return dict(self.runtime)
    def bind_session(self, identity, nonce, snapshot):
        self.events.append(("bind", identity, nonce, snapshot))
        return Transport(self.events)
    def dispatch_if_active(self, identity, transport, frame):
        return transport.request(frame)
    def revoke_bound_and_stop(self, identity, nonce, snapshot):
        assert identity == IDENTITY and snapshot == RUNTIME
        self.revoke_and_stop(identity)
    def revoke_and_stop(self, identity):
        self.events.append(("stop_requested", identity))
        return "UNKNOWN"


@pytest.fixture(autouse=True)
def allow_fixture_lock(monkeypatch):
    # Synthetic process-local holds, never clear real module ownership state.
    monkeypatch.setattr(host, "_WORK_HOLDS", {})
    monkeypatch.setattr(host, "_CONTAINER_HOLDS", {})
    import base64, hashlib, struct
    synthetic = struct.pack(">I",11)+b"ssh-ed25519"+struct.pack(">I",32)+bytes(32)
    monkeypatch.setattr(host, "_OWNER_HOST_KEY_SHA256", base64.b64encode(hashlib.sha256(synthetic).digest()).decode().rstrip("="))
    public_line="curis-browser ssh-ed25519 "+base64.b64encode(synthetic).decode()
    monkeypatch.setattr(host,"_OWNER_KNOWN_HOSTS_FILE_SHA256",hashlib.sha256(public_line.encode()).hexdigest())
    monkeypatch.setattr("app.agent_browser_runtime.load_trusted_reader_lock",
                        lambda: {"browserImageDigest": RUNTIME["image_digest"]})


def test_platform_verification_is_closed_by_default():
    with pytest.raises(ValueError, match="not released"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)


def test_owned_work_is_snapshotted_before_lease_nonce_binding(monkeypatch):
    events = []
    owner = Owner(events)
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    lease = host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert isinstance(lease, ReaderLease)
    assert [item[0] for item in events] == ["snapshot", "bind", "snapshot", "snapshot", "request", "snapshot"]
    assert events[1][2] == lease.nonce == events[4][2]
    assert events[1][1] == IDENTITY and events[1][3] == RUNTIME
    lease.close()
    lease.close()
    assert events[-1][0] == "stop_requested"
    assert not any(item[0] == "close" for item in events)


def test_revocation_after_binding_closes_and_requests_owned_stop(monkeypatch):
    events, stopped = [], [False]
    owner = Owner(events)
    original = owner.bind_session
    def bind(*args):
        result = original(*args)
        stopped[0] = True
        return result
    owner.bind_session = bind
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(PermissionError):
        host.open_owned_reader(IDENTITY, Policy(), lambda: stopped[0])
    assert [item[0] for item in events] == ["snapshot", "bind", "stop_requested"]


def test_changed_runtime_closes_and_requests_owned_stop(monkeypatch):
    events = []
    owner = Owner(events)
    original = owner.bind_session
    def bind(*args):
        result = original(*args)
        owner.runtime["boot_id"] = "changed"
        return result
    owner.bind_session = bind
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(PermissionError):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert [item[0] for item in events] == ["snapshot", "bind", "snapshot", "stop_requested"]



def test_transport_close_is_not_called_before_stop(monkeypatch):
    events = []
    class BadTransport(Transport):
        def close(self):
            self.events.append(("close",))
            raise OSError("fixture close")
    owner = Owner(events)
    owner.bind_session = lambda identity, nonce, snapshot: BadTransport(events)
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    lease = host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    lease.close()
    lease.close()
    assert events[-1][0] == "stop_requested"
    assert not any(item[0] == "close" for item in events)


def test_platform_without_revocation_contract_fails_closed(monkeypatch):
    events = []
    owner = Owner(events)
    owner.dispatch_if_active = None
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="atomic revocation"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert events == [("snapshot", IDENTITY)]  # No exclusively held resource to stop.


def test_stop_failure_remains_unknown_and_is_not_silently_retried():
    class FailingOwner(Owner):
        def revoke_and_stop(self, identity):
            raise OSError("stop failed")
    deferred = host._DeferredTransport(FailingOwner([]), IDENTITY, RUNTIME)
    with pytest.raises(OSError):
        deferred.close()
    assert deferred.stop_state == "UNKNOWN"
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        deferred.close()


def test_concurrent_close_reports_pending():
    import threading
    entered, release = threading.Event(), threading.Event()
    class BlockingOwner(Owner):
        def revoke_and_stop(self, identity):
            entered.set()
            if not release.wait(2):
                raise TimeoutError("test did not release stop")
    deferred = host._DeferredTransport(BlockingOwner([]), IDENTITY, RUNTIME)
    thread = threading.Thread(target=deferred.close)
    thread.start()
    try:
        assert entered.wait(2)
        with pytest.raises(RuntimeError, match="pending"):
            deferred.close()
    finally:
        release.set()
        thread.join(2)
    assert not thread.is_alive() and deferred.stop_state == "UNKNOWN"


def test_open_failure_reports_cleanup_failure(monkeypatch):
    owner = Owner([])
    owner.runtime["boot_id"] = []
    def fail_stop(identity):
        raise OSError("stop failed")
    owner.revoke_and_stop = fail_stop
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="runtime") as error:
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert any("UNKNOWN" in note for note in error.value.__notes__)


def test_start_cleanup_failure_is_reported_even_if_lease_swallows_it(monkeypatch):
    owner = Owner([])
    def fail_request(*_):
        raise ValueError("start failed")
    def fail_stop(*_):
        raise OSError("stop failed")
    owner.dispatch_if_active = fail_request
    owner.revoke_and_stop = fail_stop
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="start failed") as error:
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert any("UNKNOWN" in note for note in error.value.__notes__)


def test_close_can_revoke_while_request_admission_is_blocked():
    import threading
    entered, release = threading.Event(), threading.Event()
    events = []

    class AtomicOwner(Owner):
        revoked = False
        def dispatch_if_active(self, identity, transport, frame):
            entered.set()
            if not release.wait(2):
                raise TimeoutError("test did not release dispatch")
            if self.revoked:
                raise PermissionError("revoked")
            return transport.request(frame)
        def revoke_and_stop(self, identity):
            self.revoked = True
            super().revoke_and_stop(identity)

    owner = AtomicOwner(events)
    deferred = host._DeferredTransport(owner, IDENTITY, RUNTIME)
    deferred.bind(Transport(events), "a" * 48)
    errors = []
    def request():
        try:
            deferred.request({"action": "start", "sequence": 1, "nonce": "a" * 48, "identity": dict(IDENTITY),
                              **{k: RUNTIME[k] for k in ("boot_id", "container_id", "image_digest")}})
        except Exception as error:
            errors.append(error)
    thread = threading.Thread(target=request)
    thread.start()
    try:
        assert entered.wait(2)
        deferred.close()
    finally:
        release.set()
        thread.join(2)
    assert not thread.is_alive()
    assert len(errors) == 1 and isinstance(errors[0], PermissionError)
    assert [item[0] for item in events] == ["snapshot", "stop_requested"]


def test_unproven_rejected_channel_is_not_closed(monkeypatch):
    events = []
    class Unproven:
        def close(self):
            events.append(("unproven_close",))
    owner = Owner(events)
    owner.bind_session = lambda identity, nonce, snapshot: Unproven()
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="transport"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert ("unproven_close",) not in events
    assert events[-1][0] == "stop_requested"


def test_runtime_snapshot_rejects_mutable_or_extra_values(monkeypatch):
    events = []
    owner = Owner(events)
    owner.runtime["boot_id"] = ["not", "a", "string"]
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="runtime"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert [item[0] for item in events] == ["snapshot"]


@pytest.mark.parametrize("field", ["tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref", "nonce", "boot_id", "container_id", "image_digest"])
def test_owned_transport_rejects_foreign_binding_before_dispatch(field):
    events = []
    deferred = host._DeferredTransport(Owner(events), IDENTITY, RUNTIME)
    deferred.bind(Transport(events), "a" * 48)
    frame = {"identity": dict(IDENTITY), "nonce": "a" * 48, "sequence": 1, "action": "start",
             **{k: RUNTIME[k] for k in ("boot_id", "container_id", "image_digest")}}
    if field in IDENTITY:
        frame["identity"][field] = "foreign"
    else:
        frame[field] = "foreign"
    with pytest.raises(PermissionError, match="binding"):
        deferred.request(frame)
    assert events == []


@pytest.mark.parametrize("when", ["before", "after"])
def test_runtime_drift_is_rejected_around_dispatch(monkeypatch, when):
    owner = Owner([])
    deferred = host._DeferredTransport(owner, IDENTITY, RUNTIME)
    deferred.bind(Transport(owner.events), "a" * 48)
    frame = {"identity": dict(IDENTITY), "nonce": "a" * 48, "sequence": 1, "action": "start",
             **{k: RUNTIME[k] for k in ("boot_id", "container_id", "image_digest")}}
    if when == "before":
        owner.runtime["boot_id"] = "changed"
    else:
        original = owner.dispatch_if_active
        def dispatch(*args):
            result = original(*args)
            owner.runtime["boot_id"] = "changed"
            return result
        owner.dispatch_if_active = dispatch
    with pytest.raises(PermissionError, match="runtime changed"):
        deferred.request(frame)
    assert sum(e[0] == "request" for e in owner.events) == (when == "after")


def test_late_response_after_stop_is_rejected():
    owner = Owner([])
    deferred = host._DeferredTransport(owner, IDENTITY, RUNTIME)
    deferred.bind(Transport(owner.events), "a" * 48)
    def dispatch(identity, transport, frame):
        result = transport.request(frame)
        deferred.close()
        return result
    owner.dispatch_if_active = dispatch
    frame = {"identity": dict(IDENTITY), "nonce": "a" * 48, "sequence": 1, "action": "start",
             **{k: RUNTIME[k] for k in ("boot_id", "container_id", "image_digest")}}
    with pytest.raises(PermissionError, match="after revocation"):
        deferred.request(frame)
    assert deferred.stop_state == "UNKNOWN"


def test_stop_timeout_is_bounded_unknown_and_never_retried(monkeypatch):
    import threading
    workers, waits = [], []
    class Event:
        def set(self): pass
        def wait(self, timeout):
            waits.append(timeout)
            return False
    class Thread:
        def __init__(self, *, target, daemon):
            assert daemon
            workers.append(target)
        def start(self): pass
    monkeypatch.setattr(threading, "Event", Event)
    monkeypatch.setattr(threading, "Thread", Thread)
    events = []
    deferred = host._DeferredTransport(Owner(events), IDENTITY, RUNTIME)
    with pytest.raises(TimeoutError, match="UNKNOWN"):
        deferred.close()
    assert waits == [1] and deferred.stop_state == "UNKNOWN"
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        deferred.close()
    assert len(workers) == 1 and events == []
    workers[0]()  # Late completion cannot clear the retained failure or UNKNOWN.
    assert deferred.stop_state == "UNKNOWN"
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        deferred.close()


def test_admitted_request_cannot_be_replayed_after_owner_failure():
    owner = Owner([])
    def fail(*args):
        owner.events.append(("dispatch",))
        raise TimeoutError("synthetic uncertain request")
    owner.dispatch_if_active = fail
    deferred = host._DeferredTransport(owner, IDENTITY, RUNTIME)
    deferred.bind(Transport(owner.events), "a" * 48)
    frame = {"identity": dict(IDENTITY), "nonce": "a" * 48, "sequence": 1, "action": "start",
             **{k: RUNTIME[k] for k in ("boot_id", "container_id", "image_digest")}}
    with pytest.raises(TimeoutError):
        deferred.request(frame)
    with pytest.raises(PermissionError, match="sequence"):
        deferred.request(frame)
    assert sum(event[0] == "dispatch" for event in owner.events) == 1


def test_prebinding_stop_failure_preserves_original_runtime_error(monkeypatch):
    owner = Owner([])
    owner.runtime["boot_id"] = []
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    calls = []
    def stop(*args):
        calls.append(True)
        raise KeyboardInterrupt("synthetic cleanup interruption")
    monkeypatch.setattr(host, "_request_owned_stop", stop)
    with pytest.raises(ValueError, match="runtime") as error:
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert calls == []  # Invalid runtime never authorizes even an attempted stop.
    assert any("UNKNOWN" in note for note in error.value.__notes__)


@pytest.mark.parametrize("change", ["none", "task_id", "employee_id", "binding_ref"])
def test_original_work_cannot_acquire_another_owner_even_after_stop(change):
    original = host._DeferredTransport(Owner([]), IDENTITY, RUNTIME)
    original.bind(Transport([]), "a" * 48)
    original.close()
    replacement = dict(IDENTITY)
    if change != "none": replacement[change] = "replacement"
    with pytest.raises(PermissionError, match="reuse is forbidden"):
        host._DeferredTransport(Owner([]), replacement, {**RUNTIME, "container_id": "different"})
    assert len(host._WORK_HOLDS) == 1 and len(host._CONTAINER_HOLDS) == 1
    assert original.stop_state == "UNKNOWN"


def test_container_cannot_be_reused_by_other_work_or_image_and_is_not_stopped(monkeypatch):
    first = host._DeferredTransport(Owner([]), IDENTITY, RUNTIME)
    events = []
    owner = Owner(events)
    owner.runtime["image_digest"] = "sha256:replacement"
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    other = {**IDENTITY, "work_ref": "other"}
    with pytest.raises(PermissionError, match="reuse is forbidden"):
        host.open_owned_reader(other, Policy(), lambda: False)
    assert [event[0] for event in events] == ["snapshot"]
    assert len(host._WORK_HOLDS) == 2 and len(host._CONTAINER_HOLDS) == 1
    assert next(iter(host._CONTAINER_HOLDS.values())) is first._hold


def test_failed_snapshot_keeps_work_hold_and_does_not_stop_unknown_container(monkeypatch):
    events = []
    owner = Owner(events)
    owner.runtime["boot_id"] = []
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    with pytest.raises(ValueError, match="runtime"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    owner.runtime = dict(RUNTIME)
    with pytest.raises(PermissionError, match="reuse is forbidden"):
        host.open_owned_reader(IDENTITY, Policy(), lambda: False)
    assert [event[0] for event in events] == ["snapshot"]
    assert len(host._WORK_HOLDS) == 1 and not host._CONTAINER_HOLDS


def test_late_stop_captures_original_nonce_runtime_and_callable(monkeypatch):
    import threading
    workers, calls = [], []
    class Event:
        def set(self): pass
        def wait(self, timeout): return False
    class Thread:
        def __init__(self, *, target, daemon): workers.append(target)
        def start(self): pass
    monkeypatch.setattr(threading, "Event", Event)
    monkeypatch.setattr(threading, "Thread", Thread)
    owner = Owner([])
    owner.revoke_bound_and_stop = lambda *args: calls.append(args)
    identity, runtime = dict(IDENTITY), dict(RUNTIME)
    with pytest.raises(TimeoutError):
        host._request_owned_stop(owner, identity, nonce="a" * 48, snapshot=runtime)
    identity["work_ref"], runtime["container_id"] = "replacement", "replacement"
    owner.revoke_bound_and_stop = lambda *args: (_ for _ in ()).throw(AssertionError("replacement method"))
    workers[0]()
    assert calls == [(IDENTITY, "a" * 48, RUNTIME)]


def test_identity_only_stop_contract_is_rejected_without_thread(monkeypatch):
    owner = Owner([])
    owner.revoke_bound_and_stop = None
    with pytest.raises(ValueError, match="exact-generation"):
        host._DeferredTransport(owner, IDENTITY, RUNTIME)
    assert owner.events == [] and not host._WORK_HOLDS



def owner_public_inputs():
    import base64, struct
    config = "Host curis-browser\nHostName 127.0.0.1\nPort 62173\nUser yy\nIdentityFile /Users/yy/.curis-browser-runtime-01/lima/_config/user\n"
    key = struct.pack(">I",11)+b"ssh-ed25519"+struct.pack(">I",32)+bytes(32)
    return config, "curis-browser ssh-ed25519 "+base64.b64encode(key).decode()


def mock_public_ssh_fds(monkeypatch, fds=(9001,9002)):
    import os,stat
    from types import SimpleNamespace
    raw=dict(zip(fds,(value.encode() for value in owner_public_inputs())))
    original_stat,original_read=os.fstat,os.pread
    def fstat(fd):
        if fd not in raw:return original_stat(fd)
        return SimpleNamespace(st_dev=1,st_ino=fd,st_uid=os.geteuid(),st_mode=stat.S_IFREG|0o600,
            st_nlink=1,st_size=len(raw[fd]),st_mtime_ns=1,st_ctime_ns=1)
    monkeypatch.setattr(os,'fstat',fstat)
    monkeypatch.setattr(os,'pread',lambda fd,n,offset:raw[fd][offset:offset+n] if fd in raw else original_read(fd,n,offset))
    return raw


@pytest.mark.parametrize("change", [None,"include","proxy","wildcard","root","foreign-key","malformed-key"])
def test_owner_ssh_enrollment_rejects_configuration_expansion(change):
    config, key = owner_public_inputs()
    if change == "include": config += "Include /self-authored-user-config\n"
    if change == "proxy": config += "ProxyCommand /self-authored-command\n"
    if change == "wildcard": config = config.replace("Host curis-browser", "Host *")
    if change == "root": config = config.replace("User yy", "User root")
    if change == "foreign-key": key = key.replace("curis-browser", "foreign")
    if change == "malformed-key": key = "curis-browser ssh-ed25519 AAAA"
    if change:
        with pytest.raises(PermissionError): host._ssh_owner_inputs(config, key)
    else:
        assert host._ssh_owner_inputs(config, key)["hostname"] == "127.0.0.1"


def test_owner_ssh_uses_verified_values_without_inherited_fd_paths(monkeypatch):
    mock_public_ssh_fds(monkeypatch,(901,902))
    argv = host._ssh_owner_argv(901, 902)
    assert argv[:4] == ["/usr/bin/ssh", "-T", "-F", "/dev/null"]
    for option in ["StrictHostKeyChecking=yes", "UserKnownHostsFile=/dev/null", "GlobalKnownHostsFile=/dev/null",
                   "NoHostAuthenticationForLocalhost=no", "ControlPath=none", "ControlMaster=no",
                   "IdentityAgent=none", "IdentitiesOnly=yes", "ClearAllForwardings=yes", "BatchMode=yes"]:
        assert option in argv
    assert argv[-2] == "curis-browser" and "/usr/bin/python3 -I -B -c " in argv[-1]
    import ast
    tree = ast.parse(host._DOCKER_RPC_SOURCE)
    assert "request['boot_id'] == boot" in host._DOCKER_RPC_SOURCE
    assert host._DOCKER_RPC_SOURCE.index("request['boot_id'] == boot") < host._DOCKER_RPC_SOURCE.index("connection.request(")
    assert isinstance(tree, ast.Module)


def test_missing_owner_enrollment_never_starts_ssh_or_creates_ledger(monkeypatch):
    def missing(): raise FileNotFoundError("Owner has not enrolled its authenticated key")
    def forbidden(*args, **kwargs): raise AssertionError("runtime operation")
    monkeypatch.setattr(host, "_owner_directory", missing)
    monkeypatch.setattr(host, "_bounded_ssh_exchange", forbidden)
    monkeypatch.setattr(host, "_OwnerJournal", forbidden)
    owner = host._DedicatedDockerOwner(IDENTITY, "sha256:"+"b"*64)
    with pytest.raises(FileNotFoundError): owner.prepare("a"*48)
    with pytest.raises(PermissionError, match="reused"): owner.prepare("a"*48)
    with pytest.raises(PermissionError, match="remains closed"): owner.verified_snapshot(IDENTITY)


@pytest.mark.parametrize("method,path,boot", [("POST","/containers/create",None),
    ("POST","/containers/foreign/stop?t=1","boot"),("DELETE","/containers/"+"c"*64,"boot"),
    ("GET","/containers/json","boot"),("POST","/containers/"+"c"*64+"/restart","boot")])
def test_docker_bridge_rejects_unscoped_operations_before_files(monkeypatch, method, path, boot):
    monkeypatch.setattr(host, "_owner_directory", lambda: (_ for _ in ()).throw(AssertionError("opened owner state")))
    with pytest.raises(PermissionError): host._DedicatedDockerSSH().request(method,path,boot_id=boot)


@pytest.mark.parametrize("raw", [b'{"state":"INTENT"}', b'{"state":"RESET"}\n', b'{"state":"INTENT","state":"CREATED"}\n'])
def test_durable_owner_ledger_rejects_partial_unknown_or_duplicate_records(raw):
    with pytest.raises((PermissionError,ValueError)): host._owner_records(raw)


@pytest.mark.parametrize("failure", ["partial","fsync",None])
def test_owner_journal_durable_write_failure_is_poisoned_without_retry(monkeypatch, failure):
    import os
    from types import SimpleNamespace
    journal = object.__new__(host._OwnerJournal)
    journal.poisoned, journal.ledger_fd, journal.records = False, 9001, []
    import threading
    journal._write_lock = threading.Lock()
    calls = []
    monkeypatch.setattr(os,"fstat",lambda fd:SimpleNamespace(st_size=0))
    def write(fd,data):
        calls.append("write")
        return len(data)-1 if failure=="partial" else len(data)
    def sync(fd):
        calls.append("fsync")
        if failure=="fsync": raise OSError("synthetic fsync failure")
    monkeypatch.setattr(os,"write",write)
    monkeypatch.setattr(os,"fsync",sync)
    if failure:
        with pytest.raises(OSError): journal.append({"state":"INTENT"})
        assert journal.poisoned and journal.records == []
        with pytest.raises(PermissionError): journal.append({"state":"INTENT"})
        assert calls.count("write")==1
    else:
        journal.append({"state":"INTENT"})
        assert calls==["write","fsync"] and not journal.poisoned and journal.records==[{"state":"INTENT"}]


@pytest.mark.parametrize("failure", [None,"held","create-timeout","foreign-id","running"])
def test_real_owner_prepare_records_intent_before_create_and_never_starts(monkeypatch, failure):
    events, records = [], []
    digest, cid, boot = "sha256:"+"b"*64, "c"*64, "01234567-0123-0123-0123-0123456789ab"
    class Journal:
        def __init__(self): self.records = [{"state":"INTENT"}] if failure=="held" else []
        def append(self,row):
            events.append(("ledger",row["state"])); records.append(dict(row)); self.records.append(dict(row))
        def close(self): pass
    class Connection:
        def request(self,method,path,**kwargs):
            events.append((method,path))
            if path=="/version": body={"Os":"linux","Arch":"arm64","Version":"29.5.2"}
            elif path.startswith("/images/"): body={"Id":digest,"Os":"linux","Architecture":"arm64"}
            elif path=="/containers/create":
                assert events[-2]==("ledger","INTENT")
                config=kwargs["body"]
                assert config["HostConfig"]["NetworkMode"]=="none" and config["HostConfig"]["ReadonlyRootfs"]
                assert config["User"]=="pwuser" and not config["HostConfig"]["Binds"]
                if failure=="create-timeout": raise TimeoutError("synthetic ambiguous create")
                self.labels = config["Labels"]
                body={"Id":"foreign" if failure=="foreign-id" else cid}
            elif path.endswith("/json"):
                body={"Id":cid,"Image":digest,"Config":{"Labels":self.labels},"HostConfig":{"NetworkMode":"none","RestartPolicy":{"Name":"no"}},
                      "State":{"Running":failure=="running","Restarting":False,"Pid":0,"ExitCode":0}}
            elif path.endswith("/stop?t=1"): body=None
            else: raise AssertionError("unexpected Docker operation")
            return {"boot_id":boot,"status":200,"body":body}
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    monkeypatch.setattr(host,"_OwnerJournal",Journal)
    owner=host._DedicatedDockerOwner(IDENTITY,digest)
    if failure:
        with pytest.raises((PermissionError,TimeoutError)): owner.prepare("a"*48)
        with pytest.raises(PermissionError): owner.prepare("a"*48)
    else:
        result=owner.prepare("a"*48)
        assert result["executionAuthorized"] is False and result["container_id"]==cid
        snapshot={"complete":False,"executionAuthorized":False,"boot_id":boot,"container_id":cid,"image_digest":digest}
        with pytest.raises(PermissionError): owner.revoke_bound_and_stop(IDENTITY,"f"*48,snapshot)
        assert owner.revoke_bound_and_stop(IDENTITY,"a"*48,snapshot)["effects"]=="UNKNOWN"
        with pytest.raises(PermissionError): owner.revoke_bound_and_stop(IDENTITY,"a"*48,snapshot)
        assert events.index(("ledger","REVOKING")) < events.index(("POST","/containers/"+cid+"/stop?t=1"))
    assert all(not (event[0]=="POST" and event[1].endswith("/start")) for event in events)



@pytest.mark.parametrize("cleanup", ["ok", "append", "stop", "interrupt"])
@pytest.mark.parametrize("allocated", [False, True])
def test_prepare_failure_cleans_original_handle_before_closing_journal(monkeypatch, cleanup, allocated):
    events, records = [], []
    digest, cid, boot = "sha256:"+"b"*64, "c"*64, "01234567-0123-0123-0123-0123456789ab"
    original = PermissionError("synthetic original prepare failure")
    class Journal:
        def __init__(self): self.records=records; self.closed=False
        def append(self, row):
            assert not self.closed
            events.append(("ledger", row["state"]))
            if cleanup=="append" and row["state"]=="REVOKING":
                raise OSError("synthetic journal failure")
            records.append(dict(row))
        def close(self): self.closed=True; events.append(("close",))
    class Connection:
        def request(self, method, path, **options):
            events.append((method,path))
            if path=="/version": body={"Os":"linux","Arch":"arm64","Version":"29.5.2"}
            elif path.startswith("/images/"): body={"Id":digest,"Os":"linux","Architecture":"arm64"}
            elif path=="/containers/create":
                if not allocated: raise original
                self.labels=options["body"]["Labels"]
                body={"Id":cid}
            elif path.endswith("/stop?t=1"):
                assert not owner.journal.closed
                if cleanup=="stop": raise TimeoutError("synthetic stop failure")
                if cleanup=="interrupt": raise KeyboardInterrupt("synthetic cleanup interruption")
                body=None
            elif path=="/containers/"+cid+"/json":
                body={"Id":cid,"Image":digest,"Config":{"Labels":self.labels},
                      "HostConfig":{"RestartPolicy":{"Name":"no"}},
                      "State":{"Running":False,"Restarting":False,"Pid":0,"ExitCode":0}}
            else: raise AssertionError(path)
            return {"boot_id":boot,"status":200,"body":body}
    monkeypatch.setattr(host,"_OwnerJournal",Journal)
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    def fail_inspect(self): raise original
    monkeypatch.setattr(host._DedicatedDockerOwner,"_inspect",fail_inspect)
    owner=host._DedicatedDockerOwner(IDENTITY,digest)
    with pytest.raises(PermissionError) as caught: owner.prepare("a"*48)
    assert caught.value is original and owner.revoked and owner.journal.closed
    assert owner.stop_requested is allocated
    stops=[event for event in events if event==("POST","/containers/"+cid+"/stop?t=1")]
    assert len(stops)==int(allocated) and events[-1]==("close",)
    if allocated:
        assert events.index(("ledger","REVOKING")) < events.index(stops[0])
        assert records[-1]["state"]==("CLOSED_VERIFIED" if cleanup=="ok" else "CREATED" if cleanup=="append" else "REVOKING")
        assert bool(getattr(original,"__notes__",[])) is (cleanup!="ok")
        with pytest.raises(PermissionError,match="already requested"):
            owner.revoke_bound_and_stop(IDENTITY,"a"*48,dict(complete=False,executionAuthorized=False,
                boot_id=boot,container_id=cid,image_digest=digest))
    else:
        assert records[-1]["state"]=="INTENT"
    with pytest.raises(PermissionError,match="reused"): owner.prepare("a"*48)
    assert not any(event[0]=="POST" and event[1].endswith("/start") for event in events)


@pytest.mark.parametrize("failure", [None,"boot","status","duplicate","stopped-already"])
def test_docker_response_is_from_pinned_session_and_original_boot(monkeypatch, failure):
    import json, os
    boot="01234567-0123-0123-0123-0123456789ab"
    config,key=owner_public_inputs()
    mock_public_ssh_fds(monkeypatch)
    closed=[]
    monkeypatch.setattr(host,"_owner_directory",lambda:9000)
    monkeypatch.setattr(host,"_owner_file",lambda directory,name,flags:9001 if name.endswith("ssh.config") else 9002)
    monkeypatch.setattr(os,"read",lambda fd,count:config.encode() if fd==9001 else key.encode())
    monkeypatch.setattr(os,"lseek",lambda *args:0)
    monkeypatch.setattr(os,"close",lambda fd:closed.append(fd))
    def exchange(argv,fds,payload,seconds):
        assert fds==(9001,9002) and "StrictHostKeyChecking=yes" in argv
        assert json.loads(payload)["boot_id"]==boot
        if failure=="duplicate": return b'{"boot_id":"first","boot_id":"second","status":200,"body":null}'
        return json.dumps({"boot_id":"ffffffff-ffff-ffff-ffff-ffffffffffff" if failure=="boot" else boot,
             "status":500 if failure=="status" else (304 if failure=="stopped-already" else 200),"body":None}).encode()
    monkeypatch.setattr(host,"_bounded_ssh_exchange",exchange)
    if failure in {"boot","status","duplicate"}:
        with pytest.raises((PermissionError,ValueError)):
            host._DedicatedDockerSSH().request("GET","/version",boot_id=boot)
    else:
        method,path=("POST","/containers/"+"c"*64+"/stop?t=1") if failure=="stopped-already" else ("GET","/version")
        assert host._DedicatedDockerSSH().request(method,path,boot_id=boot)["boot_id"]==boot
    assert closed==[9001,9002,9000]


@pytest.mark.parametrize("failure", [None,"timeout","oversized"])
def test_actual_ssh_exchange_bounds_pipes_and_only_cleans_held_child(monkeypatch, failure):
    import os, select, subprocess
    events=[]
    mock_public_ssh_fds(monkeypatch,(901,902))
    class Pipe:
        closed=False
        def __init__(self,fd): self.fd=fd
        def fileno(self): return self.fd
        def close(self): self.closed=True
    class Process:
        stdin,stdout=Pipe(9001),Pipe(9002)
        ended=False
        def poll(self): return 0 if self.ended else None
        def terminate(self): events.append("terminate")
        def kill(self): events.append("kill"); self.ended=True
        def wait(self,timeout):
            if failure and not self.ended: raise subprocess.TimeoutExpired("synthetic",timeout)
            self.ended=True
            return 0
    process=Process()
    def popen(argv,**options):
        assert options["pass_fds"]==() and options["close_fds"] is True
        assert options["env"]=={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","HOME":host._OWNER_ROOT+"/home"}
        assert options["stderr"] is subprocess.DEVNULL and options["cwd"]==host._OWNER_ROOT
        return process
    chunks=[b"x"*2097153 if failure=="oversized" else b'{"self_authored":true}',b""]
    monkeypatch.setattr(subprocess,"Popen",popen)
    monkeypatch.setattr(os,"set_blocking",lambda *args:None)
    monkeypatch.setattr(os,"write",lambda fd,data:len(data))
    monkeypatch.setattr(os,"read",lambda fd,count:chunks.pop(0))
    monkeypatch.setattr(select,"select",lambda r,w,x,timeout:([] if failure=="timeout" else r,w,[]))
    if failure:
        with pytest.raises((TimeoutError,ValueError)):
            host._bounded_ssh_exchange(host._ssh_owner_argv(901,902),(901,902),b"{}",5)
        assert events==["terminate","kill"]
    else:
        assert host._bounded_ssh_exchange(host._ssh_owner_argv(901,902),(901,902),b"{}",5)==b'{"self_authored":true}'
        assert events==[]
    assert process.stdin.closed and process.stdout.closed



@pytest.mark.parametrize("labels,valid", [
    (None,True), ({},True), ({"org.opencontainers.image.version":"24.04"},True),
    ({"curis.reader.work":"forged"},False), ({"curis.reader.role":"proxy"},False),
    ({"curis.other":"forged"},False), ({"version":24},False), ([],False)])
def test_inherited_labels_require_exact_image_and_cannot_supply_curis_identity(labels, valid):
    digest="sha256:"+"b"*64
    image={"Id":digest,"Config":{"Labels":labels}}
    if valid:
        result=host._verified_image_labels(image,digest)
        assert result==(labels or {})
        result["new"]="synthetic"
        assert image["Config"]["Labels"]==labels
    else:
        with pytest.raises(PermissionError):host._verified_image_labels(image,digest)
    with pytest.raises(PermissionError):host._verified_image_labels(image,"sha256:"+"c"*64)


@pytest.mark.parametrize("check", ["prepare-inspect","topology","history","stop"])
@pytest.mark.parametrize("mutation", ["extra","inherited-value","nonce","role"])
def test_inherited_labels_do_not_relax_original_container_checks(monkeypatch, check, mutation):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    request=owner.connection.request
    def changed(method,path,**options):
        result=request(method,path,**options)
        if path=="/containers/"+owner.container_id+"/json":
            labels=result["body"]["Config"]["Labels"]
            key,value={"extra":("foreign","unexpected"),
                "inherited-value":("org.opencontainers.image.version","changed"),
                "nonce":("curis.reader.nonce","f"*48),"role":("curis.reader.role","proxy")}[mutation]
            labels[key]=value
        return result
    monkeypatch.setattr(owner.connection,"request",changed)
    if check=="stop":
        with pytest.raises(RuntimeError,match="stop incomplete"):
            owner.revoke_bound_and_stop(IDENTITY,owner.nonce,dict(complete=False,executionAuthorized=False,
                boot_id=owner.boot_id,container_id=owner.container_id,image_digest=owner.image_digest))
        assert owner.journal.closed and owner.journal.records[-1]["state"]!="CLOSED_VERIFIED"
    else:
        with pytest.raises(PermissionError):
            if check=="prepare-inspect": owner._inspect()
            elif check=="topology": owner._topology()
            else: owner._group_exits(owner._history_groups()[-1])


@pytest.mark.parametrize("failure", [None,"started","endpoint-id","network-id","address"])
def test_retirement_distinguishes_empty_created_endpoint_from_active_attachment(monkeypatch, failure):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    request=owner.connection.request
    def created(method,path,**options):
        result=request(method,path,**options)
        if path.startswith('/containers/'):
            info=result["body"]
            info["State"].update(Status="created",Dead=False,StartedAt="0001-01-01T00:00:00Z",FinishedAt="0001-01-01T00:00:00Z")
            if failure=="started":info["State"]["StartedAt"]="2026-11-04T00:00:00Z"
            for endpoint in info["NetworkSettings"]["Networks"].values():
                endpoint.update(NetworkID="",EndpointID="",IPAddress="",Gateway="",IPv6Gateway="",GlobalIPv6Address="")
                if failure=="endpoint-id":endpoint["EndpointID"]="f"*64
                if failure=="network-id":endpoint["NetworkID"]="f"*64
                if failure=="address":endpoint["IPAMConfig"]["IPv4Address"]="172.30.253.4"
        return result
    monkeypatch.setattr(owner.connection,"request",created)
    group=owner._history_groups()[0]
    if failure:
        with pytest.raises(PermissionError):owner._retirement_attachments(group)
    else:
        assert owner._retirement_attachments(group)=={owner.proxy_id:set(),owner.container_id:set()}


@pytest.mark.parametrize("failure", [None,"ledger","pins","boot","started","pid","labels","image",
    "endpoint","endpoint-id","address","missing-network","foreign-network","network-labels","network-identity",
    "journal","delete","delete-late","container-race","network-race","terminal","close"])
@pytest.mark.parametrize("actual_journal", [False, True])
def test_explicit_recovery_only_retires_pinned_empty_never_started_pair(monkeypatch, failure, actual_journal):
    import copy,hashlib,json,os,uuid
    from pathlib import Path
    real_journal,real_file=host._OwnerJournal,host._owner_file
    original,events,networks,containers=network_owner_fixture(monkeypatch)
    rows=copy.deepcopy(original.journal.records)
    history=copy.deepcopy(rows)
    group=original._history_groups()[0]
    pins={**{k:group["base"][k] for k in ("work","nonce","boot_id","image_digest")},
          **{k:group[k] for k in ("container_id","proxy_id","networks")}}
    raw=b''.join((json.dumps(row,sort_keys=True)+"\n").encode() for row in rows)
    ledger_hash=hashlib.sha256(raw).hexdigest()
    new_boot="11234567-0123-0123-0123-0123456789ab"
    if actual_journal:
        root=Path('/private/tmp/curis-exec-20261029-dev02')
        prefix='owner-recovery-journal-'+uuid.uuid4().hex+'-'
        for name,data in [('reader-owner.lock',b''),('reader-owner-ledger.jsonl',raw),('reader-owner-agent-ledger.jsonl',b'')]:
            fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                assert os.write(fd,data)==len(data)
                os.fsync(fd)
            finally:os.close(fd)
        monkeypatch.setattr(host,"_owner_directory",lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW))
        monkeypatch.setattr(host,"_owner_file",lambda directory,name,flags:real_file(directory,prefix+name,flags))
    class Journal(real_journal if actual_journal else object):
        def __init__(self):
            self.closed=False
            if actual_journal:
                super().__init__()
                assert self.records==rows
            else:self.ledger_fd=9007
            self.records=rows
        def append(self,row):
            assert not self.closed
            events.append(("recovery-ledger",row["state"]))
            if failure=="journal" or failure=="terminal" and row["state"]=="CLOSED_VERIFIED":
                raise OSError("synthetic recovery journal failure")
            if actual_journal:super().append(row)
            else:rows.append(copy.deepcopy(row))
        def close(self):
            if actual_journal:super().close()
            self.closed=True
            if failure=="close":raise OSError("synthetic close failure")
    request=original.connection.request
    deletes=[]
    reads=[0]
    class Connection:
        def request(self,method,path,**options):
            if path!="/version":assert options["boot_id"]==new_boot
            if method=="DELETE":
                assert rows[-1]["state"]=="UNSTARTED_RECOVERY_INTENT"
                assert path.split('/')[2] in pins["networks"].values()
                if failure=="delete" or failure=="delete-late" and deletes:raise TimeoutError("synthetic delete UNKNOWN")
                nid=path.split('/')[2]
                deletes.append(nid)
                assert networks[nid].get("Containers",{})=={} and not any(c["running"] for c in containers.values())
                del networks[nid]
                for container in containers.values():
                    container["spec"]["NetworkingConfig"]["EndpointsConfig"].pop(nid,None)
                events.append((method,path))
                return {"boot_id":new_boot,"status":204,"body":None}
            assert method in {"GET","DELETE"}
            result=request(method,path,**options)
            result["boot_id"]=pins["boot_id"] if failure=="boot" else new_boot
            if path.startswith('/containers/'):
                reads[0]+=1
                v=result["body"];state=v["State"]
                state.update(Status="created",Dead=False,StartedAt="0001-01-01T00:00:00Z",FinishedAt="0001-01-01T00:00:00Z")
                for endpoint in v["NetworkSettings"]["Networks"].values():
                    endpoint.update(NetworkID="",EndpointID="",IPAddress="",Gateway="",IPv6Gateway="",GlobalIPv6Address="")
                    if failure=="endpoint":endpoint["NetworkID"]=pins["networks"]["private"]
                    if failure=="endpoint-id":endpoint["EndpointID"]="f"*64
                    if failure=="address":endpoint["IPAMConfig"]["IPv4Address"]="172.30.253.4"
                if failure=="missing-network":v["NetworkSettings"]["Networks"]={}
                if failure=="started" or failure=="container-race" and reads[0]>2:state["StartedAt"]="2026-11-04T00:00:00Z"
                if failure=="pid":state["Pid"]=7
                if failure=="labels":v["Config"]["Labels"]["curis.reader.nonce"]="f"*48
                if failure=="image":v["Image"]="sha256:"+"f"*64
            if path.startswith('/networks/') and method=="GET" and result["status"]==200:
                v=result["body"]
                if failure=="foreign-network" or failure=="network-race" and reads[0]>2:v["Containers"]={"f"*64:{}}
                if failure=="network-labels":v["Labels"]["foreign"]="unexpected"
                if failure=="network-identity":v["Id"]="f"*64
            return result
    monkeypatch.setattr(host,"_OwnerJournal",Journal)
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    real_pread=os.pread
    monkeypatch.setattr(os,"pread",lambda fd,count,offset:raw if fd==9007 else real_pread(fd,count,offset))
    owner=host._DedicatedDockerOwner(IDENTITY,original.image_digest)
    if failure=="pins":pins["proxy_id"]="f"*64
    if failure=="ledger":ledger_hash="f"*64
    if failure:
        with pytest.raises((PermissionError,TimeoutError,OSError)):
            owner.recover_unstarted(pins,ledger_sha256=ledger_hash)
        assert owner.journal.closed
        assert rows[-1]["state"]!="CLOSED_VERIFIED" or failure=="close"
        if failure not in {"delete-late","terminal","close"}:assert deletes==[]
    else:
        receipt=owner.recover_unstarted(pins,ledger_sha256=ledger_hash)
        assert receipt["state"]=="CLOSED_VERIFIED" and receipt["containers_retained"] is True
        assert set(deletes)==set(pins["networks"].values()) and not networks
        assert rows[:5]==history and len(rows)==7 and len(containers)==2
        if actual_journal:
            persisted=(root/(prefix+'reader-owner-ledger.jsonl')).read_bytes()
            assert host._owner_records(persisted)==rows
            assert persisted.startswith(raw)
        assert owner._history_groups()[0]["recovery_boot_id"]==new_boot
        owner._verify_prior_holds("b"*48)
    with pytest.raises(PermissionError,match="reused"):
        owner.recover_unstarted(pins,ledger_sha256=ledger_hash)
    with pytest.raises(PermissionError,match="reused"):
        owner.prepare("b"*48,hosts=["example.com"])
    assert not any(event[0]=="POST" and ('/stop?' in event[1] or event[1].endswith('/start')) for event in events)


@pytest.mark.parametrize("stopped",[False,True])
@pytest.mark.parametrize("sequence", ["valid","intent-only","closed-first","duplicate-intent","started",
    "changed-boot","changed-hash","changed-container","changed-exits","extra-field","unknown-state"])
def test_real_recovery_append_parse_reopen_and_lifecycle_order(monkeypatch, sequence, stopped):
    import copy,hashlib,os,uuid
    from pathlib import Path
    real_journal,real_file=host._OwnerJournal,host._owner_file
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    initial=copy.deepcopy(owner.journal.records)
    group=owner._history_groups()[0]
    root=Path('/private/tmp/curis-exec-20261029-dev02')
    prefix='owner-recovery-order-'+uuid.uuid4().hex+'-'
    for name in ['reader-owner.lock','reader-owner-ledger.jsonl','reader-owner-agent-ledger.jsonl']:
        fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        os.close(fd)
    monkeypatch.setattr(host,"_owner_directory",lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW))
    monkeypatch.setattr(host,"_owner_file",lambda directory,name,flags:real_file(directory,prefix+name,flags))
    journal=real_journal()
    try:
        for row in initial:journal.append(row)
        if stopped:
            for state in ['START_INTENT','NETNS_FILTER_INTENT','REVOKING','STOP_RETURNED']:
                journal.append({**group['base'],'state':state,'container_id':group['container_id'],'proxy_id':group['proxy_id']})
        original=os.pread(journal.ledger_fd,1048577,0)
        owner.boot_id='11234567-0123-0123-0123-0123456789ab'
        receipt={**group['base'],'container_id':group['container_id'],'proxy_id':group['proxy_id'],
            'networks':group['networks'].copy(),'recovery_boot_id':owner.boot_id,
            'recovery_ledger_sha256':hashlib.sha256(original).hexdigest()}
        if stopped:
            receipt.update(filter_outcome='UNKNOWN',recovery_inspection_sha256='a'*64,
                recovery_prior_sha256=hashlib.sha256(b'[]').hexdigest(),exit_codes={group['container_id']:0,group['proxy_id']:0})
        intent={**receipt,'state':'STOPPED_RECOVERY_INTENT' if stopped else 'UNSTARTED_RECOVERY_INTENT'}
        terminal={**receipt,'state':'CLOSED_VERIFIED','exit_codes':{group['container_id']:0,group['proxy_id']:0}}
        if sequence=='unknown-state':
            with pytest.raises(PermissionError):journal.append({**intent,'state':'UNRECOGNIZED_RECOVERY'})
            assert os.pread(journal.ledger_fd,1048577,0)==original
        elif sequence=='closed-first':journal.append(terminal)
        else:
            if sequence=='started':journal.append({**group['base'],'state':'START_INTENT',
                'container_id':group['container_id'],'proxy_id':group['proxy_id']})
            journal.append(intent)
            if sequence=='duplicate-intent':journal.append(intent)
            if sequence=='changed-boot':terminal['recovery_boot_id']='21234567-0123-0123-0123-0123456789ab'
            if sequence=='changed-hash':terminal['recovery_ledger_sha256']='f'*64
            if sequence=='changed-container':terminal['container_id']='f'*64
            if sequence=='changed-exits':terminal['exit_codes'][group['container_id']]=137
            if sequence=='extra-field':terminal['untrusted']=True
            if sequence!='intent-only':journal.append(terminal)
        persisted=os.pread(journal.ledger_fd,1048577,0)
        assert persisted.startswith(original) and host._owner_records(persisted)==journal.records
    finally:journal.close()
    reopened=real_journal()
    try:
        owner.journal=reopened
        assert reopened.records==host._owner_records(persisted)
        if sequence=='valid':assert owner._history_groups()[0]['state']=='CLOSED_VERIFIED'
        elif sequence in {'intent-only','unknown-state'}:
            assert owner._history_groups(recovery=True)[0]['state']==(
                ('STOPPED_RECOVERY_INTENT' if stopped else 'UNSTARTED_RECOVERY_INTENT') if sequence=='intent-only' else 'STOP_RETURNED' if stopped else 'CREATED')
            with pytest.raises(PermissionError):owner._history_groups()
        else:
            with pytest.raises(PermissionError):owner._history_groups(recovery=True)
    finally:reopened.close()


@pytest.mark.parametrize("retirement", [False,"intent","verified"])
@pytest.mark.parametrize("references", [False,True])
@pytest.mark.parametrize("failure", [None,"ledger","inspection","prior","labels","pid","exit-changed",
    "endpoint","network-labels","snapshot-race","disconnect","delete","delete-late","intent-fsync","terminal-fsync","intent-partial","terminal-partial"])
def test_stopped_unknown_recovery_real_journal_and_next_work(monkeypatch, references, failure, retirement):
    import copy,hashlib,json,os,uuid
    from pathlib import Path
    real_journal,real_file=host._OwnerJournal,host._owner_file
    original,events,networks,containers=network_owner_fixture(monkeypatch)
    filter_proof=original.connection.browser_filter
    def failed_filter(*args):raise PermissionError('synthetic original filter UNKNOWN')
    monkeypatch.setattr(original.connection,'browser_filter',failed_filter)
    with pytest.raises(PermissionError):original.start_runtime()
    target=copy.deepcopy(original.journal.records)
    assert target[-1]['state']=='STOP_RETURNED' and any(r['state']=='NETNS_FILTER_INTENT' for r in target)
    group=original._history_groups()[0]
    if retirement:
        if retirement=='verified':
            index=next(i for i,r in enumerate(target) if r['state']=='NETNS_FILTER_INTENT')
            bound={key:group['base'][key] for key in ('boot_id','image_digest','work','nonce')}
            bound.update(container_id=group['container_id'],network_id=group['networks']['private'])
            proof=filter_proof('apply',bound)
            target.insert(index+1,{**target[index],'state':'NETNS_FILTER_VERIFIED','filter':proof})
        target.append({**group['base'],'state':'NETWORK_RETIRE_INTENT','container_id':group['container_id'],
            'proxy_id':group['proxy_id'],'networks':group['networks'].copy(),
            'exit_codes':{group['container_id']:137,group['proxy_id']:137}})
    pins={**{k:group['base'][k] for k in ('work','nonce','boot_id','image_digest')},
        **{k:group[k] for k in ('container_id','proxy_id','networks')}}
    base={'work':'e'*64,'nonce':'e'*48,'boot_id':'21234567-0123-0123-0123-0123456789ab','image_digest':original.image_digest}
    prior_id='d'*64
    initial=[{**base,'state':'INTENT'},{**base,'state':'CREATED','container_id':prior_id}]
    for state in ['REVOKING','STOP_RETURNED','CLOSED_VERIFIED']:
        initial.append({**base,'state':state,'container_id':prior_id,'proxy_id':None,
            **({'exit_codes':{prior_id:0}} if state=='CLOSED_VERIFIED' else {})})
    initial+=target
    root=Path('/private/tmp/curis-exec-20261029-dev02')
    prefix='owner-stopped-recovery-'+uuid.uuid4().hex+'-'
    for name in ['reader-owner.lock','reader-owner-ledger.jsonl','reader-owner-agent-ledger.jsonl']:
        fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);os.close(fd)
    monkeypatch.setattr(host,'_owner_directory',lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW))
    monkeypatch.setattr(host,'_owner_file',lambda directory,name,flags:real_file(directory,prefix+name,flags))
    seed=real_journal()
    for row in initial:seed.append(row)
    raw=os.pread(seed.ledger_fd,1048577,0);seed.close()
    ledger_hash=hashlib.sha256(raw).hexdigest()
    removed_before=set()
    if retirement in {'partial','removed'}:
        removed_before={pins['networks']['private']} if retirement=='partial' else set(pins['networks'].values())
        for nid in removed_before:
            del networks[nid]
            for value in containers.values():value['spec']['NetworkingConfig']['EndpointsConfig'].pop(nid,None)
    request=original.connection.request
    current='11234567-0123-0123-0123-0123456789ab'
    active=[False];reads=[0];deletes=[];disconnects=[]
    class Connection:
        def request(self,method,path,**options):
            if method=='DELETE':
                if failure=='delete' or failure=='delete-late' and deletes:raise TimeoutError('synthetic retirement UNKNOWN')
                nid=path.split('/')[2];assert nid in pins['networks'].values()
                assert networks[nid].get('Containers',{})=={}
                deletes.append(nid);del networks[nid]
                for c in containers.values():c['spec']['NetworkingConfig']['EndpointsConfig'].pop(nid,None)
                return {'status':204,'body':None,'boot_id':current}
            if path.endswith('/disconnect'):
                assert references
                if failure=='disconnect':raise TimeoutError('synthetic disconnect UNKNOWN')
                pair=(options['body']['Container'],path.split('/')[2]);disconnects.append(pair)
            if path=='/containers/'+prior_id+'/json':
                body={'Id':prior_id,'Image':original.image_digest,'Config':{'Labels':{
                    'org.opencontainers.image.version':'24.04','curis.reader.work':base['work'],'curis.reader.nonce':base['nonce']}},
                    'HostConfig':{'RestartPolicy':{'Name':'no'}},'State':{'Running':failure=='prior' and active[0],
                    'Restarting':False,'Pid':0,'ExitCode':0}}
                return {'status':200,'body':body,'boot_id':current}
            result=request(method,path,**options);result['boot_id']=current
            if path.startswith('/containers/') and method=='GET':
                info=result['body'];reads[0]+=int(active[0])
                info['State'].update(Status='exited',Dead=False,StartedAt='2026-11-04T00:00:00Z',
                    FinishedAt='2026-11-04T00:00:01Z',ExitCode=137)
                for name,e in info['NetworkSettings']['Networks'].items():
                    e.update(NetworkID=e['NetworkID'] if references else '',EndpointID='',IPAddress='',
                        Gateway='',IPv6Gateway='',GlobalIPv6Address='')
                    if active[0] and failure=='endpoint':e['EndpointID']='f'*64
                if active[0] and failure=='labels':info['Config']['Labels']['curis.reader.nonce']='f'*48
                if active[0] and failure=='pid':info['State']['Pid']=7
                if active[0] and failure=='exit-changed':info['State']['ExitCode']=0
                if active[0] and failure=='snapshot-race' and reads[0]>2:info['State']['FinishedAt']='changed'
            if active[0] and path.startswith('/networks/') and method=='GET' and result['status']==200 and failure=='network-labels':
                result['body']['Labels']['foreign']='unexpected'
            return result
    monkeypatch.setattr(host,'_DedicatedDockerSSH',Connection)
    monkeypatch.setattr(host,'_OwnerJournal',real_journal)
    connection=Connection()
    snapshot={'containers':{cid:connection.request('GET','/containers/'+cid+'/json')['body'] for cid in (pins['proxy_id'],pins['container_id'])},
        'networks':{nid:None if nid in removed_before else connection.request('GET','/networks/'+nid)['body'] for nid in pins['networks'].values()}}
    inspection=hashlib.sha256(json.dumps(snapshot,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    active[0]=True
    real_write,real_sync=os.write,os.fsync
    marker=[b'']
    def write(fd,data):
        marker[0]=data
        if (failure=='intent-partial' and (b'STOPPED_RECOVERY_INTENT' in data or b'RETIREMENT_RECOVERY_INTENT' in data)
                or failure=='terminal-partial' and b'CLOSED_VERIFIED' in data):return real_write(fd,data[:-1])
        return real_write(fd,data)
    def sync(fd):
        if (failure=='intent-fsync' and (b'STOPPED_RECOVERY_INTENT' in marker[0] or b'RETIREMENT_RECOVERY_INTENT' in marker[0])
                or failure=='terminal-fsync' and b'CLOSED_VERIFIED' in marker[0]):raise OSError('synthetic durable recovery failure')
        return real_sync(fd)
    monkeypatch.setattr(os,'write',write);monkeypatch.setattr(os,'fsync',sync)
    owner=host._DedicatedDockerOwner(IDENTITY,original.image_digest)
    recover=owner.recover_retirement if retirement else owner.recover_stopped
    if failure=='ledger':ledger_hash='f'*64
    if failure=='inspection':inspection='f'*64
    fails=failure is not None and (failure!='disconnect' or references)
    if fails:
        with pytest.raises((PermissionError,TimeoutError,OSError)):
            recover(pins,ledger_sha256=ledger_hash,inspection_sha256=inspection)
    else:
        receipt=recover(pins,ledger_sha256=ledger_hash,inspection_sha256=inspection)
        assert receipt['filter_outcome']=='UNKNOWN' and set(receipt['exit_codes'].values())=={137}
        assert set(deletes)==set(pins['networks'].values())-removed_before and len(containers)==2
        assert len(disconnects)==(sum(2 if role=='private' else 1 for role,nid in pins['networks'].items() if nid not in removed_before) if references else 0)
    monkeypatch.setattr(os,'fsync',real_sync)
    persisted=(root/(prefix+'reader-owner-ledger.jsonl')).read_bytes()
    assert persisted.startswith(raw)
    if failure in {'intent-partial','terminal-partial'}:
        with pytest.raises(PermissionError):real_journal()
        with pytest.raises(PermissionError):recover(pins,ledger_sha256=ledger_hash,inspection_sha256=inspection)
        return
    reopened=real_journal()
    try:
        owner.journal=reopened
        assert host._owner_records(persisted)==reopened.records
        if fails and failure!='terminal-fsync':
            with pytest.raises(PermissionError):owner._verify_prior_holds('b'*48)
        else:
            parsed=owner._history_groups()
            assert parsed[-1]['filter_state']==('VERIFIED' if retirement=='verified' else 'INTENT') and parsed[-1]['filter_outcome']=='UNKNOWN'
            # A fresh next Work uses the real history/hold gate in this same boot.
            fresh=host._DedicatedDockerOwner({**IDENTITY,'task_id':'fresh-next-work'},original.image_digest)
            fresh.boot_id=current;fresh.journal=reopened
            fresh._verify_prior_holds('b'*48)
            with pytest.raises(PermissionError):fresh._verify_prior_holds(pins['nonce'])
    finally:reopened.close()
    if not fails or failure=='terminal-fsync':
        result=fresh.prepare('b'*48,hosts=['example.com'])
        try:
            assert result['running'] is False and result['boot_id']==current
            assert fresh.journal.records[-1]['state']=='CREATED'
            assert fresh.journal.records[-1]['nonce']=='b'*48
        finally:fresh.journal.close()
    with pytest.raises(PermissionError):recover(pins,ledger_sha256=ledger_hash,inspection_sha256=inspection)


@pytest.mark.parametrize('failure',[None,'labels','image','running','pid','exit','network-returned','unresolved','audit-fsync','audit-partial'])
def test_closed_history_reconciles_across_boot_with_real_audit_before_next_work(monkeypatch,failure):
    import copy,hashlib,json,os,uuid
    from pathlib import Path
    real_journal,real_file=host._OwnerJournal,host._owner_file
    original,events,networks,containers=network_owner_fixture(monkeypatch)
    original.start_runtime()
    original.revoke_bound_and_stop(IDENTITY,original.nonce,owner_stop_snapshot(original))
    initial=copy.deepcopy(original.journal.records)
    assert initial[-1]['state']=='CLOSED_VERIFIED' and networks=={}
    if failure=='unresolved':initial=initial[:-1]
    root=Path('/private/tmp/curis-exec-20261029-dev02');prefix='owner-boot-audit-'+uuid.uuid4().hex+'-'
    for name in ['reader-owner.lock','reader-owner-ledger.jsonl','reader-owner-agent-ledger.jsonl']:
        fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);os.close(fd)
    monkeypatch.setattr(host,'_owner_directory',lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW))
    monkeypatch.setattr(host,'_owner_file',lambda directory,name,flags:real_file(directory,prefix+name,flags))
    journal=real_journal()
    for row in initial:journal.append(row)
    raw=os.pread(journal.ledger_fd,1048577,0);journal.close()
    current=['11234567-0123-0123-0123-0123456789ab']
    request=original.connection.request
    class Connection:
        browser_filter=original.connection.browser_filter
        def request(self,method,path,**options):
            if path!='/version':assert options['boot_id']==current[0]
            result=request(method,path,**options);result['boot_id']=current[0]
            if path=='/containers/'+original.container_id+'/json':
                v=result['body']
                if failure=='labels':v['Config']['Labels']['curis.reader.nonce']='f'*48
                if failure=='image':v['Image']='sha256:'+'f'*64
                if failure=='running':v['State']['Running']=True
                if failure=='pid':v['State']['Pid']=7
                if failure=='exit':v['State']['ExitCode']=137
            if failure=='network-returned' and path=='/networks/'+original.private_network:
                result['status']=200;result['body']={'Id':original.private_network}
            return result
    monkeypatch.setattr(host,'_DedicatedDockerSSH',Connection);monkeypatch.setattr(host,'_OwnerJournal',real_journal)
    real_write,real_sync=os.write,os.fsync;last=[b'']
    def write(fd,data):
        last[0]=data
        return real_write(fd,data[:-1] if failure=='audit-partial' and b'BOOT_CLOSURES_VERIFIED' in data else data)
    def sync(fd):
        if failure=='audit-fsync' and b'BOOT_CLOSURES_VERIFIED' in last[0]:raise OSError('synthetic boot audit fsync failure')
        return real_sync(fd)
    monkeypatch.setattr(os,'write',write);monkeypatch.setattr(os,'fsync',sync)
    event_start=len(events)
    owner=host._DedicatedDockerOwner({**IDENTITY,'task_id':'new-boot-work'},original.image_digest)
    if failure:
        with pytest.raises((PermissionError,OSError)):owner.prepare('b'*48,hosts=['example.com'])
        assert len(containers)==2 and networks=={}
        assert not any(e[0] in {'POST','DELETE'} for e in events[event_start:])
        assert owner.journal.ledger_fd is None
    else:
        owner.prepare('b'*48,hosts=['example.com'])
        records=owner.journal.records
        assert records[:len(initial)]==initial and records[len(initial)]['state']=='BOOT_CLOSURES_VERIFIED'
        audit=records[len(initial)]
        assert audit['prior_ledger_sha256']==hashlib.sha256(raw).hexdigest() and audit['boot_id']==current[0]
        assert records[len(initial)+1]['state']=='INTENT'
        owner.revoke_bound_and_stop(owner.identity,owner.nonce,owner_stop_snapshot(owner))
        second=host._DedicatedDockerOwner({**IDENTITY,'task_id':'same-boot-next'},original.image_digest)
        second.prepare('c'*48,hosts=['example.com'])
        assert sum(r['state']=='BOOT_CLOSURES_VERIFIED' for r in second.journal.records)==1
        second.revoke_bound_and_stop(second.identity,second.nonce,owner_stop_snapshot(second))
        current[0]='31234567-0123-0123-0123-0123456789ab'
        third=host._DedicatedDockerOwner({**IDENTITY,'task_id':'third-boot-next'},original.image_digest)
        third.prepare('d'*48,hosts=['example.com'])
        assert sum(r['state']=='BOOT_CLOSURES_VERIFIED' for r in third.journal.records)==2
        third.revoke_bound_and_stop(third.identity,third.nonce,owner_stop_snapshot(third))
        assert len(containers)==8 and networks=={}
    monkeypatch.setattr(os,'fsync',real_sync)
    persisted=(root/(prefix+'reader-owner-ledger.jsonl')).read_bytes();assert persisted.startswith(raw)
    if failure=='audit-partial':
        with pytest.raises(PermissionError):real_journal()
    else:
        reopened=real_journal()
        try:assert reopened.records==host._owner_records(persisted)
        finally:reopened.close()


def network_owner_fixture(monkeypatch, failure=None, *, prepared=True):
    import copy
    events,networks,containers=[],{},{}
    records,counter=[],[0]
    digest="sha256:"+"b"*64
    boot="01234567-0123-0123-0123-0123456789ab"
    class Journal:
        def __init__(self): self.records=records; self.closed=False
        def append(self,row): events.append(("ledger",row["state"])); self.records.append(copy.deepcopy(row))
        def close(self): self.closed=True
    class Connection:
        def browser_filter(self,action,binding,expected=None,*,paired=False):
            events.append(("filter",action))
            receipt={**binding,"pid":7,"started_at":"synthetic-start","kernel_start":123,
                     "namespace":[4,100],"rules_sha256":host._NETNS_PAIRED_FILTER_SHA256 if paired else host._NETNS_FILTER_SHA256}
            if expected is not None:assert receipt==expected
            return receipt
        def request(self,method,path,**options):
            events.append((method,path))
            body=options.get("body")
            if path=="/version": value={"Os":"linux","Arch":"arm64","Version":"29.5.2"}
            elif path.startswith("/images/"): value={"Id":digest,"Os":"linux","Architecture":"arm64","Config":{"Labels":{"org.opencontainers.image.version":"24.04"}}}
            elif path=="/networks/create":
                assert not any(n["IPAM"]==body["IPAM"] for n in networks.values()), "synthetic Docker subnet overlap"
                counter[0]+=1
                nid=str(counter[0])*64 if counter[0]<5 else format(counter[0],"064x")
                networks[nid]={**copy.deepcopy(body),"Id":nid}
                value={"Id":nid}
            elif path=="/containers/create":
                counter[0]+=1
                cid=str(counter[0])*64 if counter[0]<5 else format(counter[0],"064x")
                containers[cid]={"spec":copy.deepcopy(body),"running":False}
                value={"Id":cid}
            elif path.startswith("/networks/"):
                nid=path.split('/')[2]
                if path.endswith("/disconnect"):
                    assert method=="POST" and body["Force"] is True
                    assert not containers[body["Container"]]["running"]
                    containers[body["Container"]]["spec"]["NetworkingConfig"]["EndpointsConfig"].pop(nid)
                    return {"boot_id":boot,"status":200,"body":None}
                if method=="DELETE":
                    assert not any(nid in c["spec"]["NetworkingConfig"]["EndpointsConfig"] for c in containers.values())
                    del networks[nid]
                    return {"boot_id":boot,"status":204,"body":None}
                if nid not in networks:
                    return {"boot_id":boot,"status":404,"body":{"message":"synthetic network absent"}}
                value={**copy.deepcopy(networks[nid]),"Containers":{cid:{} for cid,c in containers.items()
                    if c["running"] and nid in c["spec"]["NetworkingConfig"]["EndpointsConfig"]}}
                if failure=="foreign-endpoint": value["Containers"]["f"*64]={}
            else:
                cid=path.split('/')[2]
                c=containers[cid]
                if path.endswith("/start"): c["running"]=True; value=None
                elif path.endswith("/stop?t=1"): c["running"]=False; value=None
                elif path.endswith("/json"):
                    spec=c["spec"]
                    value={"Id":cid,"Image":digest,"Config":{"Labels":{"org.opencontainers.image.version":"24.04",**spec["Labels"]},"User":spec["User"], **{key:copy.deepcopy(spec.get(key)) for key in ("Env","Entrypoint","Cmd","WorkingDir","StdinOnce","OpenStdin","Tty")},"Hostname":cid[:12]},
                        "HostConfig":copy.deepcopy(spec["HostConfig"]),"State":{"Running":c["running"],"Restarting":False,"Pid":7 if c["running"] else 0,"ExitCode":0},
                        "Mounts":[],"NetworkSettings":{"Networks":{networks[nid]["Name"]:{**copy.deepcopy(endpoint),
                            "NetworkID":nid,"IPAddress":endpoint["IPAMConfig"]["IPv4Address"] if c["running"] else ""}
                            for nid,endpoint in spec.get("NetworkingConfig",{}).get("EndpointsConfig",{}).items()}}}
                    if failure=="host-mount": value["Mounts"]=[{"Type":"bind","Destination":"/host"}]
                    if failure=="dns": value["HostConfig"]["Dns"]=["8.8.8.8"]
                    if failure=="extra-network": value["NetworkSettings"]["Networks"]["foreign"]={}
                else: raise AssertionError(path)
            return {"boot_id":boot,"status":200,"body":value}
    class Attach:
        def __init__(self,cid,boot_id): self.cid=cid; self.closed=False; events.append(("attach",cid))
        def request(self,frame):
            assert not self.closed
            runtime=frame["runtime"]
            ack={"identity":frame["identity"].copy(),"nonce":frame["nonce"],"sequence":0,**runtime}
            if self.cid=="3"*64:
                ack["result"]={"proxy_ready":True,"proxy_spki":"bad" if failure=="spki" else "A"*43+"="}
            else:
                ack["result"]={"bootstrapped":True,"browser_started":False}
                if failure=="browser-ack": ack["nonce"]="foreign"
            return ack
        def close(self): self.closed=True; events.append(("close",self.cid))
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    monkeypatch.setattr(host,"_OwnerJournal",Journal)
    monkeypatch.setattr(host,"_DockerAttachChannel",Attach)
    monkeypatch.setattr(host,"_private_seccomp",lambda:'{}')
    owner=host._DedicatedDockerOwner(IDENTITY,digest)
    if prepared: owner.prepare("a"*48,hosts=["example.com"])
    return owner,events,networks,containers


def test_networked_owner_attaches_before_start_and_bootstraps_tls_before_browser(monkeypatch):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    assert all(not c["running"] for c in containers.values())
    assert networks["1"*64]["Internal"] is True
    assert networks["1"*64]["Options"]["com.docker.network.bridge.gateway_mode_ipv4"]=="isolated"
    channel=owner.start_runtime()
    proxy,browser="3"*64,"4"*64
    assert events.index(("attach",proxy))<events.index(("POST","/containers/"+proxy+"/start"))
    assert events.index(("attach",browser))<events.index(("POST","/containers/"+browser+"/start"))
    assert events.index(("POST","/containers/"+proxy+"/start"))<events.index(("attach",browser))
    snapshot={"complete":False,"executionAuthorized":False,"boot_id":owner.boot_id,"container_id":browser,"image_digest":owner.image_digest}
    assert owner.bind_session(IDENTITY,"a"*48,snapshot) is channel
    with pytest.raises(PermissionError): owner.verified_snapshot(IDENTITY)
    with pytest.raises(PermissionError): owner.start_runtime()
    assert owner.revoke_bound_and_stop(IDENTITY,"a"*48,snapshot)["effects"]=="UNKNOWN"
    assert all(not c["running"] for c in containers.values())
    stops=[event for event in events if event[0]=="POST" and event[1].endswith("/stop?t=1")]
    assert stops==[("POST","/containers/"+proxy+"/stop?t=1"),("POST","/containers/"+browser+"/stop?t=1")]


@pytest.mark.parametrize("failure", ["foreign-endpoint","host-mount","dns","extra-network","spki","browser-ack"])
def test_networked_owner_rejects_topology_or_bootstrap_drift_without_retry(monkeypatch,failure):
    owner,events,networks,containers=network_owner_fixture(monkeypatch,failure)
    with pytest.raises(PermissionError): owner.start_runtime()
    with pytest.raises(PermissionError): owner.start_runtime()
    starts=[event for event in events if event[0]=="POST" and event[1].endswith("/start")]
    assert len(starts)==(2 if failure=="browser-ack" else (1 if failure=="spki" else 0))
    if failure in {"spki","browser-ack"}:
        assert owner.revoked and all(not c["running"] for c in containers.values())


def test_original_owner_dispatch_consumes_sequence_and_rejects_late_reply(monkeypatch):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    channel=owner.start_runtime()
    frame={"identity":IDENTITY.copy(),"nonce":owner.nonce,"boot_id":owner.boot_id,"container_id":owner.container_id,
           "image_digest":owner.image_digest,"sequence":1,"action":"start"}
    def request(frame): owner.revoked=True; return {"result":{"ready":True}}
    channel.request=request
    with pytest.raises(PermissionError,match="after revocation"): owner.dispatch_if_active(IDENTITY,channel,frame)
    assert owner._owner_sequence==1
    with pytest.raises(PermissionError): owner.dispatch_if_active(IDENTITY,channel,frame)


def test_linux_proxy_certificate_is_fresh_private_and_key_never_exported(monkeypatch):
    import subprocess,ssl
    from types import SimpleNamespace
    events=[]
    class Path:
        def __init__(self,name): self.name=name
        def __truediv__(self,name): return Path(self.name+"/"+name)
        def __str__(self): return self.name
        def mkdir(self,mode): events.append(("mkdir",mode))
        def write_text(self,text): assert "DNS:example.com" in text
        def chmod(self,mode): events.append(("chmod",mode))
        def unlink(self,missing_ok): events.append(("unlink",self.name))
    def run(argv,**options):
        assert argv[0]=="/usr/bin/openssl" and "sandbox-exec" not in argv
        assert options["env"]=={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","OPENSSL_CONF":"/synthetic-proxy/request.cnf"}
        assert 0<options["timeout"]<=4 and options["check"] is True
        return SimpleNamespace(stdout=b"synthetic-public-der")
    class Context:
        def __init__(self,protocol): assert protocol==ssl.PROTOCOL_TLS_SERVER
        def load_cert_chain(self,cert,key): assert str(key)=="/synthetic-proxy/key.pem"
        def set_alpn_protocols(self,values): assert values==["http/1.1"]
    monkeypatch.setattr(subprocess,"run",run)
    monkeypatch.setattr(ssl,"SSLContext",Context)
    context,spki=host._linux_proxy_tls(Path("/synthetic-proxy"),["example.com"])
    assert len(spki)==44 and context.minimum_version==ssl.TLSVersion.TLSv1_2
    assert events==[("mkdir",0o700),("chmod",0o600),("unlink","/synthetic-proxy/key.pem")]



def test_owner_pinned_fingerprint_cannot_be_replaced_by_another_valid_public_key(monkeypatch):
    config,key=owner_public_inputs()
    mock_public_ssh_fds(monkeypatch)
    monkeypatch.setattr(host,"_OWNER_HOST_KEY_SHA256","different-independently-enrolled-key")
    with pytest.raises(PermissionError,match="fingerprint"): host._ssh_owner_inputs(config,key)


@pytest.mark.parametrize("failure",["proxy-stop","journal"])
def test_stop_attempts_both_owned_containers_even_if_proxy_or_journal_fails(monkeypatch,failure):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    owner.start_runtime()
    original=owner.connection.request
    def request(method,path,**options):
        if failure=="proxy-stop" and path=="/containers/"+owner.proxy_id+"/stop?t=1":
            events.append((method,path)); raise TimeoutError("synthetic ambiguous proxy stop")
        return original(method,path,**options)
    owner.connection.request=request
    if failure=="journal":
        owner.journal.append=lambda row: (_ for _ in ()).throw(OSError("synthetic durable write failure"))
    snapshot={"complete":False,"executionAuthorized":False,"boot_id":owner.boot_id,"container_id":owner.container_id,"image_digest":owner.image_digest}
    with pytest.raises(RuntimeError,match="UNKNOWN"): owner.revoke_bound_and_stop(IDENTITY,owner.nonce,snapshot)
    assert all(channel.closed for channel in owner.channels) and owner.revoked
    assert not containers[owner.container_id]["running"]
    stops=[event for event in events if event[0]=="POST" and event[1].endswith("/stop?t=1")]
    assert stops==[("POST","/containers/"+owner.proxy_id+"/stop?t=1"),("POST","/containers/"+owner.container_id+"/stop?t=1")]
    with pytest.raises(PermissionError): owner.revoke_bound_and_stop(IDENTITY,owner.nonce,snapshot)
    assert len([event for event in events if event[0]=="POST" and event[1].endswith("/stop?t=1")])==2


def test_docker_start_submit_cannot_complete_after_original_stop(monkeypatch):
    import threading
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    entered,release=threading.Event(),threading.Event()
    original=owner.connection.request
    def request(method,path,**options):
        if path=="/containers/"+owner.proxy_id+"/start":
            entered.set()
            if not release.wait(2): raise TimeoutError("synthetic start not released")
        return original(method,path,**options)
    owner.connection.request=request
    errors=[]
    def start():
        try: owner._start_owned(owner.proxy_id)
        except BaseException as error: errors.append(error)
    snapshot={"complete":False,"executionAuthorized":False,"boot_id":owner.boot_id,"container_id":owner.container_id,"image_digest":owner.image_digest}
    def stop():
        try: owner.revoke_bound_and_stop(IDENTITY,owner.nonce,snapshot)
        except BaseException as error: errors.append(error)
    starter,stopper=threading.Thread(target=start),threading.Thread(target=stop)
    starter.start()
    try:
        assert entered.wait(2)
        stopper.start()
        assert owner._revoked_event.wait(2)
    finally:
        release.set();starter.join(2)
        if stopper.ident is not None: stopper.join(2)
    assert not starter.is_alive() and not stopper.is_alive() and not errors
    assert events.index(("POST","/containers/"+owner.proxy_id+"/start"))<events.index(("POST","/containers/"+owner.proxy_id+"/stop?t=1"))
    assert all(not c["running"] for c in containers.values())
    with pytest.raises(PermissionError): owner._start_owned(owner.container_id)


def test_late_attach_closes_its_held_child_after_stop_without_registration(monkeypatch):
    import threading
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    entered,release=threading.Event(),threading.Event()
    attached=[]
    class Channel:
        closed=False
        def __init__(self,*args):
            entered.set()
            if not release.wait(2): raise TimeoutError("synthetic attach not released")
            attached.append(self)
        def close(self): self.closed=True
    monkeypatch.setattr(host,"_DockerAttachChannel",Channel)
    errors=[]
    def attach():
        try: owner._attach_owned(owner.proxy_id)
        except BaseException as error: errors.append(error)
    thread=threading.Thread(target=attach);thread.start()
    try:
        assert entered.wait(2)
        owner.revoke_bound_and_stop(IDENTITY,owner.nonce,{"complete":False,"executionAuthorized":False,
            "boot_id":owner.boot_id,"container_id":owner.container_id,"image_digest":owner.image_digest})
    finally:
        release.set();thread.join(2)
    assert not thread.is_alive() and len(errors)==1 and isinstance(errors[0],PermissionError)
    assert attached[0].closed and owner.channels==[]


@pytest.mark.parametrize("bad_ack",[False,True,"changed-enrollment"])
def test_docker_attach_reuses_bound_reader_pipe_and_closes_held_ssh(monkeypatch,bad_ack):
    import os,subprocess
    import app.agent_browser_runtime as runtime
    config,key=owner_public_inputs()
    public_bytes=mock_public_ssh_fds(monkeypatch)
    closed,events=[],[]
    cid,boot="c"*64,"01234567-0123-0123-0123-0123456789ab"
    monkeypatch.setattr(host,"_owner_directory",lambda:9000)
    monkeypatch.setattr(host,"_owner_file",lambda d,name,flags:9001 if name.endswith("ssh.config") else 9002)
    monkeypatch.setattr(os,"read",lambda fd,count:config.encode() if fd==9001 else key.encode())
    monkeypatch.setattr(os,"lseek",lambda *args:0)
    monkeypatch.setattr(os,"close",lambda fd:closed.append(fd))
    class Stream:
        def __init__(self,fd): self.fd=fd
        def fileno(self): return self.fd
        def close(self): events.append(("stream-close",self.fd))
    class Process:
        stdin,stdout=Stream(8001),Stream(8002)
        ended=False
        def poll(self): return 0 if self.ended else None
        def terminate(self): events.append(("terminate",))
        def wait(self,timeout): self.ended=True;return 0
    process=Process()
    def popen(argv,**options):
        assert "StrictHostKeyChecking=yes" in argv and options["pass_fds"]==()
        assert options["env"]["HOME"]==host._OWNER_ROOT+"/home" and options["stderr"] is subprocess.DEVNULL
        return process
    class Pipe:
        def __init__(self,read,write,**options): assert (read,write)==(8002,8001) and options["timeout"]==host._READER_ATTACH_TIMEOUT_SECONDS
        def request(self,frame):
            assert frame=={"container_id":cid,"boot_id":boot}
            if bad_ack=="changed-enrollment":public_bytes[9001]=public_bytes[9001].replace(b'62173',b'62174')
            return {"container_id":"foreign" if bad_ack is True else cid,"boot_id":boot,"result":{"attached":True}}
        def close(self): events.append(("pipe-close",))
    monkeypatch.setattr(subprocess,"Popen",popen)
    monkeypatch.setattr(runtime,"BoundedPipeTransport",Pipe)
    if bad_ack:
        with pytest.raises(PermissionError): host._DockerAttachChannel(cid,boot)
    else:
        channel=host._DockerAttachChannel(cid,boot)
        channel.close();channel.close()
    assert closed==[9001,9002,9000] and events.count(("terminate",))==1 and events.count(("pipe-close",))==1


def test_proxy_certificate_generation_failure_deletes_only_fresh_key(monkeypatch):
    import subprocess
    unlinked=[]
    class Path:
        def __init__(self,name):self.name=name
        def __str__(self):return self.name
        def __truediv__(self,name):return Path(self.name+"/"+name)
        def mkdir(self,mode):assert mode==0o700
        def write_text(self,text):pass
        def unlink(self,missing_ok):unlinked.append(self.name)
    def fail(*args,**kwargs):raise subprocess.TimeoutExpired("synthetic openssl",4)
    monkeypatch.setattr(subprocess,"run",fail)
    with pytest.raises(subprocess.TimeoutExpired):host._linux_proxy_tls(Path("/synthetic-proxy"),["example.com"])
    assert unlinked==["/synthetic-proxy/key.pem"]



def test_v2_pin_is_required_without_old_pin_fallback_or_runtime_action(monkeypatch):
    import os
    names,closed=[],[]
    monkeypatch.setattr(host,"_owner_directory",lambda:9000)
    def open_file(directory,name,flags):
        names.append(name)
        if name=="reader-owner-ssh.config":return 9001
        raise FileNotFoundError("v2 enrollment absent")
    monkeypatch.setattr(host,"_owner_file",open_file)
    monkeypatch.setattr(os,"close",lambda fd:closed.append(fd))
    monkeypatch.setattr(host,"_bounded_ssh_exchange",lambda *args:(_ for _ in ()).throw(AssertionError("started SSH")))
    with pytest.raises(FileNotFoundError):host._DedicatedDockerSSH().request("GET","/version")
    assert names==["reader-owner-ssh.config","reader-owner-known_hosts-v2"]
    assert closed==[9001,9000]


def test_proxy_timeout_does_not_consume_browser_inspect_stop_or_verify_budget(monkeypatch):
    import time
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    owner.start_runtime()
    clock=[100.0]
    monkeypatch.setattr(time,"monotonic",lambda:clock[0])
    original=owner.connection.request
    calls=[]
    def request(method,path,**options):
        calls.append((method,path,options.get("seconds")))
        assert 0<options["seconds"]<=2
        if path=="/containers/"+owner.proxy_id+"/stop?t=1":
            clock[0]+=3
            raise TimeoutError("synthetic proxy exceeded old shared budget")
        return original(method,path,**options)
    owner.connection.request=request
    snapshot={"complete":False,"executionAuthorized":False,"boot_id":owner.boot_id,"container_id":owner.container_id,"image_digest":owner.image_digest}
    with pytest.raises(RuntimeError,match="UNKNOWN"):owner.revoke_bound_and_stop(IDENTITY,owner.nonce,snapshot)
    browser_calls=[(method,path.rsplit('/',1)[1],seconds) for method,path,seconds in calls if owner.container_id in path]
    assert browser_calls==[("GET","json",1),("POST","stop?t=1",2),("GET","json",1)]
    assert not containers[owner.container_id]["running"] and owner.stop_requested


@pytest.mark.parametrize("failure",[None,OSError,KeyboardInterrupt])
def test_attach_concurrent_close_reports_pending_then_retains_failure_without_retry(failure):
    import threading
    entered,release=threading.Event(),threading.Event()
    calls,errors=[],[]
    class Pipe:
        def close(self):
            calls.append(True);entered.set()
            if not release.wait(2):raise TimeoutError("synthetic close not released")
            if failure is not None:raise failure("synthetic cleanup failure")
    channel=object.__new__(host._DockerAttachChannel)
    channel.closed=False
    channel._close_lock=threading.Lock()
    channel._close_pending=channel._close_failure=False
    channel._close_done=threading.Event()
    channel.pipe,channel.process=Pipe(),None
    def close():
        try:channel.close()
        except BaseException as error:errors.append(error)
    thread=threading.Thread(target=close);thread.start()
    try:
        assert entered.wait(2)
        with pytest.raises(RuntimeError,match="pending"):channel.close()
        with pytest.raises(PermissionError):channel.request({"action":"start"})
        assert calls==[True]
    finally:
        release.set();thread.join(2)
    assert not thread.is_alive() and not channel._close_pending
    if failure is not None:
        assert len(errors)==1 and isinstance(errors[0],failure)
        with pytest.raises(RuntimeError,match="failed"):channel.close()
    else:
        assert not errors
        channel.close()
    assert calls==[True]


def test_real_owner_reader_uses_nonce_reserved_before_container_create(monkeypatch):
    import app.agent_browser_runtime as runtime
    from app.agent_browser_policy import PublicTargets
    owner,events,networks,containers=network_owner_fixture(monkeypatch, prepared=False)
    frames, nonces = [], []
    # Synthetic accepted snapshot only; production release stays closed.
    owner.verified_snapshot=lambda identity: {"complete":True,"executionAuthorized":True,
        "boot_id":owner.boot_id,"container_id":owner.container_id,"image_digest":owner.image_digest}
    monkeypatch.setattr(host,"_open_verified_vm_owner",lambda identity:owner)
    monkeypatch.setattr(runtime,"load_trusted_reader_lock",lambda:{"runtimeKind":"VM","browserImageDigest":owner.image_digest})
    def reserve(size):
        assert size == 24 and not nonces
        nonces.append("a"*48)
        return nonces[0]
    monkeypatch.setattr(runtime.secrets,"token_hex",reserve)
    bootstrap = owner.start_runtime
    def start():
        channel = bootstrap()
        def request(frame):
            frames.append(frame)
            return {**{k:frame[k] for k in ("identity","nonce","sequence","boot_id","container_id","image_digest")},"result":{"ready":True}}
        channel.request=request
        return channel
    owner.start_runtime = start
    lease=runtime.open_reader_for_work(IDENTITY,["example.com"],lambda:False)
    assert lease.nonce==lease.session==owner.nonce=="a"*48 and frames[0]["nonce"]==owner.nonce
    assert len(nonces) == len(frames) == 1
    assert events.index(("ledger","INTENT"))<events.index(("POST","/containers/create"))
    lease.close()
    assert owner.stop_requested and all(not c["running"] for c in containers.values())



@pytest.mark.parametrize("failure",[None,"missing","old-profile","tampered","symlink","hardlink","owner","writable","oversize"])
def test_private_seccomp_accepts_only_reviewed_bytes_and_safe_file_handle(monkeypatch,failure):
    import errno,hashlib,json,os,stat
    from pathlib import Path
    from types import SimpleNamespace
    path=Path(host.__file__).with_name("reader_seccomp.json")
    # Synthetic bytes and fake descriptors only. Actual approved file/pin equality
    # is checked separately by the static review, outside product-import tests.
    approved=b'{"defaultAction":"SCMP_ACT_ERRNO","syscalls":[{"names":["chroot"],"action":"SCMP_ACT_ALLOW"}]}'
    monkeypatch.setattr(host,"_PRIVATE_SECCOMP_SHA256",hashlib.sha256(approved).hexdigest())
    raw=approved
    if failure=="old-profile":
        original=json.loads(approved);original["syscalls"].pop();raw=json.dumps(original).encode()
    if failure=="tampered":raw=approved+b" "
    opened,reads,closed=[],[],[]
    def open_file(name,flags):
        assert name==str(path) and flags & os.O_NOFOLLOW and flags & os.O_NONBLOCK
        opened.append(name)
        if failure=="missing":raise FileNotFoundError(errno.ENOENT,"synthetic missing resource")
        if failure=="symlink":raise OSError(errno.ELOOP,"synthetic symlink")
        return 9001
    monkeypatch.setattr(os,"open",open_file)
    monkeypatch.setattr(os,"fstat",lambda fd:SimpleNamespace(st_mode=stat.S_IFREG|(0o666 if failure=="writable" else 0o644),
        st_uid=os.geteuid()+1 if failure=="owner" else os.geteuid(),st_nlink=2 if failure=="hardlink" else 1,
        st_size=65537 if failure=="oversize" else len(raw)))
    def read(fd,count):reads.append(count);return raw
    monkeypatch.setattr(os,"read",read)
    monkeypatch.setattr(os,"close",lambda fd:closed.append(fd))
    if failure:
        with pytest.raises((PermissionError,OSError)):host._private_seccomp()
    else:
        assert json.loads(host._private_seccomp())==json.loads(approved)
    assert len(opened)==1 and closed==([] if failure in {"missing","symlink"} else [9001])
    if failure in {"missing","symlink","hardlink","owner","writable","oversize"}:assert reads==[]
    else:assert reads==[65537]


@pytest.mark.parametrize("failure",["hosts","profile"])
def test_reader_preflight_rejects_bad_inputs_before_any_remote_or_ledger_operation(monkeypatch,failure):
    def forbidden(*args,**options):raise AssertionError("preflight performed runtime/state operation")
    class Connection:
        request=staticmethod(forbidden)
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    monkeypatch.setattr(host,"_OwnerJournal",forbidden)
    def invalid_profile():raise PermissionError("synthetic profile mismatch")
    monkeypatch.setattr(host,"_private_seccomp",invalid_profile)
    owner=host._DedicatedDockerOwner(IDENTITY,"sha256:"+"b"*64)
    with pytest.raises((PermissionError,ValueError)):
        owner.prepare("a"*48,hosts=["localhost"] if failure=="hosts" else ["example.com"])
    with pytest.raises(PermissionError,match="reused"):owner.prepare("a"*48,hosts=["example.com"])
    assert owner.journal is None and owner.private_network is None and owner.container_id is None


def test_owner_retains_reviewed_profile_for_create_and_topology_without_rereading(monkeypatch):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    monkeypatch.setattr(host,"_private_seccomp",lambda:(_ for _ in ()).throw(AssertionError("profile reread after allocation")))
    owner.start_runtime()
    assert owner._seccomp_profile=='{}'
    assert all("seccomp={}" in row["spec"]["HostConfig"]["SecurityOpt"] for row in containers.values())



def continuity_fixture(monkeypatch, networked=False):
    import copy
    boot="01234567-0123-0123-0123-0123456789ab"
    digest="sha256:"+"b"*64
    base={"work":"1"*64,"nonce":"a"*48,"boot_id":boot,"image_digest":digest}
    rows=[{**base,"state":"INTENT"}]
    labels={"curis.reader.work":base["work"],"curis.reader.nonce":base["nonce"]}
    objects={}
    if networked:
        for role,nid in [("private","2"*64),("external","3"*64)]:
            rows.append({**base,"state":"NETWORK","role":role,"network_id":nid})
            objects["/networks/"+nid]={"Id":nid,"Name":"curis-reader-"+base["nonce"]+"-"+role,
                "Labels":labels.copy(),"Driver":"bridge","Internal":role=="private","EnableIPv6":False,"Containers":{}}
        rows.append({**base,"state":"PROXY_CREATED","container_id":"4"*64})
    rows.append({**base,"state":"CREATED","container_id":"5"*64})
    original={"container_id":"5"*64,"proxy_id":"4"*64 if networked else None}
    for state in ["START_INTENT","ATTACHED","REVOKING","STOP_RETURNED"]:
        rows.append({**base,"state":state,**original})
    for cid in filter(None,original.values()):
        objects["/containers/"+cid+"/json"]={"Id":cid,"Image":digest,
            "Config":{"Labels":{**labels,**({"curis.reader.role":"proxy"} if cid==original["proxy_id"] else {})}},
            "HostConfig":{"RestartPolicy":{"Name":"no"}},"State":{"Running":False,"Restarting":False,"Pid":0,"ExitCode":137 if cid==original["proxy_id"] else 0}}
    events=[]
    class Journal:
        def __init__(self): self.records=rows
        def append(self,row):
            events.append(("ledger",row["state"]))
            rows.append(copy.deepcopy(row))
        def close(self): pass
    class Connection:
        def request(self,method,path,**options):
            events.append((method,path))
            if path=="/version": value={"Os":"linux","Arch":"arm64","Version":"29.5.2"}
            elif path.startswith("/images/"): value={"Id":digest,"Os":"linux","Architecture":"arm64"}
            elif path=="/containers/create":
                cid=str(len(objects)+6)*64
                assert len(cid)==64
                objects["/containers/"+cid+"/json"]={"Id":cid,"Image":digest,
                    "Config":{"Labels":copy.deepcopy(options["body"]["Labels"])},"HostConfig":{"NetworkMode":"none","RestartPolicy":{"Name":"no"}},
                    "State":{"Running":False,"Restarting":False,"Pid":0,"ExitCode":0}}
                value={"Id":cid}
            elif path.endswith("/stop?t=1"): value=None
            else: value=copy.deepcopy(objects[path])
            return {"boot_id":boot,"status":200,"body":value}
    monkeypatch.setattr(host,"_OwnerJournal",Journal)
    monkeypatch.setattr(host,"_DedicatedDockerSSH",Connection)
    return rows,objects,events,boot,digest


def test_same_boot_continuity_preserves_history_and_rechecks_each_generation(monkeypatch):
    import copy
    rows,objects,events,boot,digest=continuity_fixture(monkeypatch)
    history=copy.deepcopy(rows)
    second=host._DedicatedDockerOwner(IDENTITY,digest)
    second.prepare("b"*48)
    assert rows[:len(history)]==history
    assert rows[len(history)]["state"]=="CLOSED_VERIFIED"
    assert rows[len(history)]["exit_codes"]=={"5"*64:0}
    assert events.index(("GET","/containers/"+"5"*64+"/json"))<events.index(("ledger","CLOSED_VERIFIED"))<events.index(("ledger","INTENT"))<events.index(("POST","/containers/create"))
    snapshot={"complete":False,"executionAuthorized":False,"boot_id":boot,
              "container_id":second.container_id,"image_digest":digest}
    assert second.revoke_bound_and_stop(IDENTITY,"b"*48,snapshot)["effects"]=="UNKNOWN"
    third=host._DedicatedDockerOwner(IDENTITY,digest)
    third.prepare("c"*48)
    assert sum(r["state"]=="CLOSED_VERIFIED" for r in rows)==2
    assert events.count(("GET","/containers/"+"5"*64+"/json"))==2


@pytest.mark.parametrize("failure",[None,"running","restarting","pid","exit-missing","image","labels","missing","timeout","foreign-endpoint","network-name","network-id","boot","nonce","partial","missing-proxy","order","binding","extra","duplicate-id","duplicate-terminal","fsync"])
def test_prior_network_generation_is_retired_only_after_complete_independent_exit(monkeypatch,failure):
    import copy
    rows,objects,events,boot,digest=continuity_fixture(monkeypatch,True)
    old=copy.deepcopy(rows)
    container=objects["/containers/"+"5"*64+"/json"]
    network=objects["/networks/"+"2"*64]
    if failure=="running":container["State"]["Running"]=True
    if failure=="restarting":container["State"]["Restarting"]=True
    if failure=="pid":container["State"]["Pid"]=123
    if failure=="exit-missing":container["State"].pop("ExitCode")
    if failure=="image":container["Image"]="sha256:"+"f"*64
    if failure=="labels":container["Config"]["Labels"]["curis.reader.nonce"]="f"*48
    if failure=="missing":objects.pop("/containers/"+"5"*64+"/json")
    if failure=="foreign-endpoint":network["Containers"]={"f"*64:{}}
    if failure=="network-name":network["Name"]="foreign"
    if failure=="network-id":network["Id"]="f"*64
    if failure=="boot":boot="foreign"
    if failure=="partial":rows.pop()
    if failure=="missing-proxy":rows[:]=[r for r in rows if r["state"]!="PROXY_CREATED"]
    if failure=="order":rows[4],rows[5]=rows[5],rows[4]
    if failure=="binding":rows[-1]["work"]="f"*64
    if failure=="extra":rows[-1]["unknown"]=True
    if failure=="duplicate-id":rows[2]["network_id"]=rows[1]["network_id"]
    if failure=="duplicate-terminal":rows.append(copy.deepcopy(rows[-1]))
    owner=host._DedicatedDockerOwner(IDENTITY,digest)
    owner.boot_id=boot
    owner.journal=host._OwnerJournal()
    if failure=="timeout":
        owner.connection.request=lambda *a,**k:(_ for _ in ()).throw(TimeoutError("synthetic timeout"))
    if failure=="fsync":
        owner.journal.append=lambda row:(_ for _ in ()).throw(OSError("synthetic fsync failure"))
    if failure:
        with pytest.raises((PermissionError,OSError,KeyError)):
            owner._verify_prior_holds("a"*48 if failure=="nonce" else "b"*48)
        assert not any(e[0]=="POST" for e in events)
        assert not any(e==("ledger","CLOSED_VERIFIED") for e in events)
    else:
        with pytest.raises(PermissionError,match="unresolved"):
            owner._verify_prior_holds("b"*48)
        assert rows==old and not any(e[0] in {"POST","DELETE"} for e in events)


def owner_stop_snapshot(owner):
    return {"complete":False,"executionAuthorized":False,"boot_id":owner.boot_id,
            "container_id":owner.container_id,"image_digest":owner.image_digest}


def test_two_network_tasks_retire_only_their_networks_and_preserve_containers_history(monkeypatch):
    import copy
    first,events,networks,containers=network_owner_fixture(monkeypatch)
    first.start_runtime()
    first_ids=(first.proxy_id,first.container_id)
    first_networks={first.private_network,first.external_network}
    history=copy.deepcopy(first.journal.records)
    answer=first.revoke_bound_and_stop(IDENTITY,first.nonce,owner_stop_snapshot(first))
    assert answer["effects"]==answer["descendants"]=="UNKNOWN"
    assert first.journal.closed and networks=={}
    assert first.journal.records[:len(history)]==history
    assert [r["state"] for r in first.journal.records[-4:]]==["STOP_RETURNED","NETWORK_RETIRE_INTENT","NETWORKS_RETIRED","CLOSED_VERIFIED"]
    assert first.journal.records[-1]["networks"]=={"private":first.private_network,"external":first.external_network}
    assert set(answer["exit_codes"])==set(first_ids)
    assert set(containers)==set(first_ids) and not any(c["running"] for c in containers.values())
    removed={p.split('/')[2] for m,p in events if m=="DELETE"}
    assert removed==first_networks
    assert events.index(("ledger","NETWORK_RETIRE_INTENT"))<next(i for i,e in enumerate(events) if e[0]=="DELETE")
    second=host._DedicatedDockerOwner({**IDENTITY,"task_id":"second-task"},first.image_digest)
    second.prepare("b"*48,hosts=["example.com"])
    assert {second.private_network,second.external_network}.isdisjoint(first_networks)
    second.revoke_bound_and_stop(second.identity,second.nonce,owner_stop_snapshot(second))
    assert len(containers)==4 and networks=={} and second.journal.closed
    assert sum(r["state"]=="CLOSED_VERIFIED" for r in second.journal.records)==2
    with pytest.raises(PermissionError):
        host._DedicatedDockerOwner(IDENTITY,first.image_digest).prepare(first.nonce,hosts=["example.com"])


@pytest.mark.parametrize("failure",["foreign-endpoint","foreign-container-network","wrong-image","live","restart-policy","boolean-pid","legacy",
    "intent-fsync","disconnect-timeout","detach-unconfirmed","delete-timeout","delete-unconfirmed","final-fsync"])
def test_retirement_failures_keep_durable_hold_no_replay_and_release_journal(monkeypatch,failure):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    original=owner.connection.request
    original_append=owner.journal.append
    if failure=="legacy":
        owner._record.pop("network_retirement")
        for row in owner.journal.records:row.pop("network_retirement",None)
    def append(row):
        if (failure=="intent-fsync" and row["state"]=="NETWORK_RETIRE_INTENT"
                or failure=="final-fsync" and row["state"]=="CLOSED_VERIFIED"):
            raise OSError("synthetic durable intent failure")
        original_append(row)
    owner.journal.append=append
    def request(method,path,**options):
        if method=="POST" and path.endswith("/disconnect"):
            assert any(r["state"]=="NETWORK_RETIRE_INTENT" for r in owner.journal.records)
            if failure=="disconnect-timeout":
                original(method,path,**options)
                raise TimeoutError("synthetic admitted detach timeout")
            if failure=="detach-unconfirmed":return {"boot_id":owner.boot_id,"status":200,"body":None}
        if method=="DELETE":
            if failure=="delete-timeout":
                original(method,path,**options)
                raise TimeoutError("synthetic admitted delete timeout")
            if failure=="delete-unconfirmed":return {"boot_id":owner.boot_id,"status":204,"body":None}
        result=original(method,path,**options)
        # Inject after STOP_RETURNED, so stop itself is still attempted for both original IDs.
        if owner.journal.records[-1]["state"]=="STOP_RETURNED":
            if failure=="foreign-endpoint" and path.startswith("/networks/"):
                result["body"]["Containers"]["f"*64]={}
            if path.endswith("/json") and path.startswith("/containers/"):
                if failure=="wrong-image":result["body"]["Image"]="sha256:"+"f"*64
                if failure=="live":result["body"]["State"]["Running"]=True
                if failure=="restart-policy":result["body"]["HostConfig"]["RestartPolicy"]["Name"]="always"
                if failure=="boolean-pid":result["body"]["State"]["Pid"]=False
                if failure=="foreign-container-network":result["body"]["NetworkSettings"]["Networks"]["foreign"]={"NetworkID":"f"*64}
        return result
    owner.connection.request=request
    with pytest.raises((PermissionError,OSError)):
        owner.revoke_bound_and_stop(IDENTITY,owner.nonce,owner_stop_snapshot(owner))
    assert owner.journal.closed and owner.journal.records[-1]["state"]!="CLOSED_VERIFIED"
    if failure in {"foreign-endpoint","foreign-container-network","wrong-image","live","restart-policy","boolean-pid","legacy","intent-fsync"}:
        assert not any(m=="DELETE" or p.endswith("/disconnect") for m,p in events)
    prior_events=len(events)
    with pytest.raises(PermissionError):
        host._DedicatedDockerOwner(IDENTITY,owner.image_digest).prepare("b"*48,hosts=["example.com"])
    assert not any(m in {"POST","DELETE"} for m,p in events[prior_events:])
    assert len(containers)==2  # Never remove retained container metadata.


@pytest.mark.parametrize("method,path,body",[
    ("DELETE","/networks/prune",None),
    ("DELETE","/networks/curis-reader-name",None),
    ("DELETE","/networks/"+"a"*64,{"force":True}),
    ("POST","/networks/"+"a"*64+"/disconnect",{"Container":"name","Force":True}),
    ("POST","/networks/"+"a"*64+"/disconnect",{"Container":"b"*64,"Force":1}),
    ("POST","/networks/"+"a"*64+"/disconnect",{"Container":"b"*64,"Force":True,"extra":True}),
])
def test_network_mutation_rpc_rejects_names_prune_and_ambiguous_body_before_ssh(monkeypatch,method,path,body):
    monkeypatch.setattr(host,"_owner_directory",lambda:(_ for _ in ()).throw(AssertionError("SSH inputs opened")))
    with pytest.raises(PermissionError):
        host._DedicatedDockerSSH().request(method,path,body=body,boot_id="boot")


@pytest.mark.parametrize("status,method,path,accepted",[
    (404,"GET","/networks/"+"a"*64,True),
    (404,"GET","/containers/"+"a"*64+"/json",False),
    (404,"DELETE","/networks/"+"a"*64,False),
    (204,"DELETE","/networks/"+"a"*64,True),
])
def test_authenticated_network_absence_is_narrow_not_container_exit_proof(monkeypatch,status,method,path,accepted):
    import json,os
    config,key=owner_public_inputs()
    mock_public_ssh_fds(monkeypatch)
    boot="01234567-0123-0123-0123-0123456789ab"
    monkeypatch.setattr(host,"_owner_directory",lambda:9000)
    monkeypatch.setattr(host,"_owner_file",lambda d,n,f:9001 if n.endswith("ssh.config") else 9002)
    monkeypatch.setattr(os,"read",lambda fd,n:config.encode() if fd==9001 else key.encode())
    monkeypatch.setattr(os,"lseek",lambda *args:0)
    monkeypatch.setattr(os,"close",lambda *args:None)
    monkeypatch.setattr(host,"_bounded_ssh_exchange",lambda *args:json.dumps({"boot_id":boot,"status":status,"body":None}).encode())
    if accepted:assert host._DedicatedDockerSSH().request(method,path,boot_id=boot)["status"]==status
    else:
        with pytest.raises(PermissionError):host._DedicatedDockerSSH().request(method,path,boot_id=boot)


@pytest.mark.parametrize("failure",[None,"stop-timeout","intent-fsync"])
def test_real_journal_flock_blocks_second_owner_then_releases_after_verified_close(monkeypatch,failure):
    import os,uuid
    from pathlib import Path
    real_journal,real_file=host._OwnerJournal,host._owner_file
    first,events,networks,containers=network_owner_fixture(monkeypatch)
    initial=list(first.journal.records)
    root=Path('/private/tmp/curis-exec-20261029-dev02')
    prefix='owner-continuity-'+uuid.uuid4().hex+'-'
    for name in ['reader-owner-ledger.jsonl','reader-owner-agent-ledger.jsonl']:
        fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);os.close(fd)
    monkeypatch.setattr(host,"_owner_directory",lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW))
    monkeypatch.setattr(host,"_owner_file",lambda directory,name,flags:real_file(directory,prefix+name,flags))
    monkeypatch.setattr(host,"_OwnerJournal",real_journal)
    first.journal=real_journal()
    try:
        for row in initial:first.journal.append(row)
        held=os.fstat(first.journal.lock_fd)
        with pytest.raises(BlockingIOError):
            host._DedicatedDockerOwner(IDENTITY,first.image_digest).prepare("b"*48,hosts=["example.com"])
        assert len(containers)==2
        if failure:
            if failure=="stop-timeout":
                request=first.connection.request
                def fail_stop(method,path,**options):
                    if path.endswith("/stop?t=1"):raise TimeoutError("synthetic stop timeout")
                    return request(method,path,**options)
                first.connection.request=fail_stop
            else:
                append=first.journal.append
                def fail_intent(row):
                    if row["state"]=="NETWORK_RETIRE_INTENT":raise OSError("synthetic intent fsync failure")
                    append(row)
                first.journal.append=fail_intent
            with pytest.raises((RuntimeError,OSError)):
                first.revoke_bound_and_stop(IDENTITY,first.nonce,owner_stop_snapshot(first))
            assert first.journal.lock_fd is first.journal.ledger_fd is first.journal.directory is None
            next_owner=host._DedicatedDockerOwner(IDENTITY,first.image_digest)
            with pytest.raises(PermissionError):next_owner.prepare("c"*48,hosts=["example.com"])
            assert next_owner.journal.lock_fd is None  # Obtained the real lock, read the hold, then released.
            assert first.journal.records[-1]["state"]!="CLOSED_VERIFIED" and len(containers)==2
            print('retained synthetic flock fixture:',root/prefix)
            return
        first.revoke_bound_and_stop(IDENTITY,first.nonce,owner_stop_snapshot(first))
        assert first.journal.lock_fd is first.journal.ledger_fd is first.journal.directory is None
        second=host._DedicatedDockerOwner(IDENTITY,first.image_digest)
        try:
            second.prepare("c"*48,hosts=["example.com"])
            acquired=os.fstat(second.journal.lock_fd)
            assert (held.st_dev,held.st_ino)==(acquired.st_dev,acquired.st_ino)
            assert sum(r["state"]=="CLOSED_VERIFIED" for r in second.journal.records)==1
            second.revoke_bound_and_stop(IDENTITY,second.nonce,owner_stop_snapshot(second))
            assert second.journal.lock_fd is None and len(containers)==4 and networks=={}
        finally:
            if second.journal is not None:second.journal.close()
    finally:
        first.journal.close()
    # Retain these two self-authored empty-lock/synthetic-ledger fixtures; no unlink or user data.
    print('retained synthetic flock fixture:',root/prefix)


@pytest.mark.parametrize("failures",[
    {9001:OSError("synthetic close failure")},
    {9001:KeyboardInterrupt("ledger interrupted")},
    {9002:KeyboardInterrupt("lock interrupted")},
    {9003:KeyboardInterrupt("directory interrupted")},
    {9001:OSError("ledger close failure"),9002:KeyboardInterrupt("lock interrupted")},
    {9001:KeyboardInterrupt("first interruption"),9002:SystemExit("later interruption")},
])
def test_journal_close_attempts_all_fds_and_reraises_original_interruption(monkeypatch,failures):
    import os
    journal=object.__new__(host._OwnerJournal)
    journal.ledger_fd,journal.lock_fd,journal.directory=9001,9002,9003
    closed=[]
    def close(fd):
        closed.append(fd)
        if fd in failures:raise failures[fd]
    monkeypatch.setattr(os,"close",close)
    expected=next((e for e in failures.values() if not isinstance(e,Exception)),next(iter(failures.values())))
    with pytest.raises(type(expected)) as caught:journal.close()
    assert caught.value is expected
    assert closed==[9001,9002,9003]
    assert journal.ledger_fd is journal.lock_fd is journal.directory is None
    journal.close()
    assert closed==[9001,9002,9003]


def netns_binding_fixture():
    return {"boot_id":"01234567-0123-0123-0123-0123456789ab","container_id":"4"*64,
        "network_id":"1"*64,"image_digest":"sha256:"+"b"*64,"work":"a"*64,"nonce":"b"*48}


def netns_receipt_fixture(binding=None):
    return {**(binding or netns_binding_fixture()),"pid":71,"started_at":"synthetic-start",
        "kernel_start":123,"namespace":[4,100],"rules_sha256":host._NETNS_FILTER_SHA256}


def test_netns_fixed_rules_allow_only_exact_proxy_and_bsk_tuples():
    scope={}
    exec(host._NETNS_COMMON_SOURCE,scope)
    assert scope["RULE_HASH"]==host._NETNS_FILTER_SHA256
    for raw in (host._NETNS_RULES_V4,host._NETNS_RULES_V6):
        assert "*nat" not in raw and "RELATED" not in raw
        assert all(policy+" DROP" in raw for policy in [":INPUT",":OUTPUT",":FORWARD"])
    rules=[row for row in scope["normal"](host._NETNS_RULES_V4.encode()) if row[0]=="-A"]
    assert len(rules)==6
    for row in rules:
        assert row[-2:]==("-j","ACCEPT") and "tcp" in row
        assert row[row.index("--ctstate")+1] in {"NEW,ESTABLISHED","ESTABLISHED"}
        if "52800" in row:
            assert "lo" in row and row[row.index("-s")+1]==row[row.index("-d")+1]=="127.0.0.1/32"
        else:
            assert "8443" in row and "eth0" in row
            assert {row[row.index("-s")+1],row[row.index("-d")+1]}=={"172.30.253.2/32","172.30.253.3/32"}
    # Docker embedded DNS after DNAT still has neither an allowed address/port tuple nor UDP permission.
    assert not any(row[row.index("-d")+1] in {"127.0.0.11/32","0.0.0.0/0"} for row in rules)
    assert not any(row[0]=="-A" for row in scope["normal"](host._NETNS_RULES_V6.encode()))


NATIVE_FILTER4_SAVE = b'''# Generated by iptables-save v1.8.10 (nf_tables)
*filter
:INPUT DROP [2:64]
:FORWARD DROP [0:0]
:OUTPUT DROP [3:96]
-A INPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -i lo -p tcp -m tcp --dport 52800 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
-A INPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -i lo -p tcp -m tcp --sport 52800 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A INPUT -s 172.30.253.2/32 -d 172.30.253.3/32 -i eth0 -p tcp -m tcp --sport 8443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A OUTPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -o lo -p tcp -m tcp --dport 52800 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
-A OUTPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -o lo -p tcp -m tcp --sport 52800 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A OUTPUT -s 172.30.253.3/32 -d 172.30.253.2/32 -o eth0 -p tcp -m tcp --dport 8443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
COMMIT
# Completed
'''


@pytest.mark.parametrize('mutation',[None,'source','destination','interface','protocol','port','state','target',
    'rule-order','extra-rule','duplicate-option','unknown-option','negation','policy','base-order'])
def test_fixed_policy_matches_native_save_order_without_relaxing_comparison(mutation):
    scope={};exec(host._NETNS_COMMON_SOURCE,scope)
    raw=NATIVE_FILTER4_SAVE
    if mutation=='base-order':raw=raw.replace(b'-s 127.0.0.1/32 -d 127.0.0.1/32 -i lo',b'-i lo -s 127.0.0.1/32 -d 127.0.0.1/32',1)
    if mutation=='source':raw=raw.replace(b'-s 127.0.0.1/32',b'-s 0.0.0.0/0',1)
    if mutation=='destination':raw=raw.replace(b'-d 127.0.0.1/32',b'-d 127.0.0.2/32',1)
    if mutation=='interface':raw=raw.replace(b'-i lo',b'-i eth0',1)
    if mutation=='protocol':raw=raw.replace(b'-p tcp',b'-p udp',1)
    if mutation=='port':raw=raw.replace(b'--dport 52800',b'--dport 52801',1)
    if mutation=='state':raw=raw.replace(b'NEW,ESTABLISHED',b'RELATED,ESTABLISHED',1)
    if mutation=='target':raw=raw.replace(b'-j ACCEPT',b'-j DROP',1)
    if mutation=='rule-order':
        lines=raw.splitlines();lines[5],lines[6]=lines[6],lines[5];raw=b'\n'.join(lines)+b'\n'
    if mutation=='extra-rule':raw=raw.replace(b'COMMIT',b'-A OUTPUT -j ACCEPT\nCOMMIT')
    if mutation=='duplicate-option':raw=raw.replace(b'-i lo',b'-i lo -i lo',1)
    if mutation=='unknown-option':raw=raw.replace(b'-i lo',b'--in-interface lo',1)
    if mutation=='negation':raw=raw.replace(b'-i lo',b'! -i lo',1)
    if mutation=='policy':raw=raw.replace(b':OUTPUT DROP',b':OUTPUT ACCEPT',1)
    expected=scope['normal'](host._NETNS_RULES_V4.encode())
    try:actual=scope['normal'](raw)
    except ValueError:
        assert mutation in {'duplicate-option','unknown-option','negation'}
    else:
        assert (actual==expected) is (mutation is None)
    assert host._NETNS_FILTER_SHA256=='d4dbcbe54dd763448466cf5619d69cdc8d9406dd2aa1fc27a86df7767bf41776'


@pytest.mark.parametrize("failure",[None,"verify","wrong-namespace","root","foreign-v4","foreign-v6",
    "partial-v6","reordered","broad-rule","v6-not-applied","namespace-after-v4","deadline",
    "precheck4-exit","precheck6-exit","restore4-exit","restore6-exit","verify4-exit","verify6-exit"])
def test_entered_helper_verifies_namespace_before_rules_and_both_families_before_receipt(failure):
    import io,json,copy
    from contextlib import redirect_stdout
    from types import SimpleNamespace
    scope={};exec(host._NETNS_ENTER_SOURCE,scope)
    written,commands=[],[]
    empty=b'*filter\n:INPUT ACCEPT [0:0]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [0:0]\nCOMMIT\n'
    states={"4":empty,"6":empty}
    if failure=="verify":states={"4":host._NETNS_RULES_V4.encode(),"6":host._NETNS_RULES_V6.encode()}
    if failure in {"foreign-v4","foreign-v6"}:
        states["4" if failure=="foreign-v4" else "6"]=empty.replace(b'COMMIT',b'-A OUTPUT -j ACCEPT\nCOMMIT')
    request={"action":"verify" if failure=="verify" else "install","namespace":[4,100],"deadline":103}
    if failure=="deadline":request["deadline"]=100
    scope["sys"]=SimpleNamespace(stdin=SimpleNamespace(buffer=io.BytesIO(json.dumps(request).encode())))
    scope["time"]=SimpleNamespace(monotonic=lambda:100)
    def ns(path):
        assert path=='/proc/self/ns/net'
        return SimpleNamespace(st_dev=4,st_ino=101 if failure=="wrong-namespace" or failure=="namespace-after-v4" and written else 100)
    scope["os"]=SimpleNamespace(geteuid=lambda:1 if failure=="root" else 0,stat=ns)
    def run(argv,deadline,data=None):
        commands.append(argv)
        if failure and failure.endswith('-exit') and scope['_filter_stage']==failure[:-5]:
            raise scope['FilterChildFailure'](scope['_filter_stage'],'PermissionError',4)
        family="6" if "ip6tables" in argv[0] else "4"
        assert argv[0] in {"/usr/sbin/iptables-save","/usr/sbin/ip6tables-save","/usr/sbin/iptables-restore","/usr/sbin/ip6tables-restore"}
        if data is not None:
            assert argv[1:]==["--noflush","--wait","1"] and data.startswith(b'*filter\n')
            if failure=="partial-v6" and family=="6":raise TimeoutError("synthetic IPv6 restore timeout")
            written.append(family)
            states[family]=data
            return b''
        assert argv[1:]==["-t","filter"]
        value=states[family]
        if value==host._NETNS_RULES_V4.encode():value=NATIVE_FILTER4_SAVE
        if written and failure=="reordered" and family=="4":
            lines=value.splitlines();lines[4],lines[5]=lines[5],lines[4];value=b'\n'.join(lines)+b'\n'
        if written and failure=="broad-rule" and family=="4":value=value.replace(b'COMMIT',b'-A OUTPUT -j ACCEPT\nCOMMIT')
        if written and failure=="v6-not-applied" and family=="6":value=empty
        return b'# Generated synthetic\n'+value.replace(b'[0:0]',b'[2:64]')+b'# Completed synthetic\n'
    scope["run"]=run
    output=io.StringIO()
    if failure in {None,"verify"}:
        with redirect_stdout(output):scope["main"]()
        assert json.loads(output.getvalue())=={"namespace":[4,100],"rules_sha256":host._NETNS_FILTER_SHA256}
        assert written==([] if failure=="verify" else ["4","6"])
    else:
        with redirect_stdout(output),pytest.raises((PermissionError,TimeoutError)):scope["main"]()
        assert host._filter_failure_diagnostic(output.getvalue().encode()) is not None
        if failure.endswith('-exit'):
            diagnostic=host._filter_failure_diagnostic(output.getvalue().encode())
            assert diagnostic['stage']==failure[:-5] and diagnostic['exit_code']==4
            assert len(written)==(0 if failure.startswith(('precheck','restore4')) else 1 if failure.startswith('restore6') else 2)
        if failure in {"wrong-namespace","root","foreign-v4","foreign-v6","deadline"}:assert written==[]
        if failure in {"partial-v6","namespace-after-v4"}:assert written==["4"]


@pytest.mark.parametrize("failure",[None,"verify","boot","image","labels","pid","uid","host-netns",
    "acquire-race","start-race","final-race","wrong-network","entered-mismatch","entered-timeout","expected-mismatch","alarm","inherited-curis","inherited-image","extra-label","inherited-value","role-label"])
def test_privileged_helper_opens_fd_after_identity_rechecks_and_never_enters_host_netns(failure):
    import io,json,copy,os
    from contextlib import redirect_stdout
    from types import SimpleNamespace
    scope={};exec(host._NETNS_ROOT_SOURCE,scope)
    binding=netns_binding_fixture()
    request={**binding,"action":"verify" if failure in {"verify","expected-mismatch"} else "install","expected":None}
    if request["action"]=="verify":request["expected"]=netns_receipt_fixture(binding)
    if failure=="expected-mismatch":request["expected"]["namespace"]=[4,101]
    scope["sys"]=SimpleNamespace(stdin=SimpleNamespace(buffer=io.BytesIO(json.dumps(request).encode())))
    scope["time"]=SimpleNamespace(monotonic=lambda:100)
    trace,closed=[],[]
    timers,handler=[],[]
    def set_signal(signum,value):
        if callable(value):handler[:]=[value]
        return 'previous-handler'
    scope['signal']=SimpleNamespace(SIGALRM=14,ITIMER_REAL=0,
        signal=set_signal,setitimer=lambda kind,seconds:timers.append(seconds))
    inspection=[0]
    class Path:
        def __init__(self,path):self.path=path
        def read_text(self):
            if self.path.endswith('boot_id'):return 'foreign' if failure=="boot" else binding["boot_id"]
            if self.path.endswith('/stat'):
                start=124 if failure=="start-race" and inspection[0]>1 else 123
                return '71 (synthetic worker) '+' '.join(['S']+['0']*18+[str(start)])
            if self.path.endswith('/status'):return 'Uid:\t'+('0 0 0 0' if failure=="uid" else '1000 1000 1000 1000')+'\n'
            raise AssertionError(self.path)
    scope["Path"]=Path
    class Response:
        def __init__(self,path): self.path=path
        status=200
        def read(self,count):
            if self.path.startswith("/v1.53/images/"):
                return json.dumps({"Id":"sha256:"+"f"*64 if failure=="inherited-image" else binding["image_digest"],"Config":{"Labels":{"curis.reader.work":"forged"} if failure=="inherited-curis" else {"org.opencontainers.image.version":"24.04"}}}).encode()
            inspection[0]+=1;trace.append('inspect')
            if failure=='alarm' and inspection[0]==3:handler[0](14,None)
            pid=72 if failure=="acquire-race" and inspection[0]>1 or failure=="final-race" and inspection[0]>2 else 71
            body={"Id":binding["container_id"],"Image":"foreign" if failure=="image" else binding["image_digest"],
                "Config":{"User":"pwuser","Labels":{"org.opencontainers.image.version":"24.04","curis.reader.work":binding["work"],"curis.reader.nonce":"foreign" if failure=="labels" else binding["nonce"]}},
                "State":{"Running":True,"Restarting":False,"Pid":True if failure=="pid" else pid,"StartedAt":"synthetic-start"},
                "HostConfig":{"NetworkMode":binding["network_id"]},
                "NetworkSettings":{"Networks":{"private":{"NetworkID":binding["network_id"],"IPAddress":"foreign" if failure=="wrong-network" else "172.30.253.3"}}}}
            if failure=="extra-label":body["Config"]["Labels"]["foreign"]="unexpected"
            if failure=="inherited-value":body["Config"]["Labels"]["org.opencontainers.image.version"]="changed"
            if failure=="role-label":body["Config"]["Labels"]["curis.reader.role"]="proxy"
            return json.dumps(body).encode()
    class HTTP:
        def __init__(self,*args):pass
        def request(self,method,path):
            assert method=='GET' and path in ['/v1.53/containers/'+binding['container_id']+'/json','/v1.53/images/'+binding['image_digest']+'/json']
            self.path=path
        def getresponse(self):return Response(self.path)
        def close(self):trace.append('http-close')
    scope['http']=SimpleNamespace(client=SimpleNamespace(HTTPConnection=HTTP))
    def opened(path,flags):
        assert trace.count('inspect')==1 and path=='/proc/71/ns/net' and flags & os.O_CLOEXEC
        trace.append('open-netns');return 9005
    scope['os']=SimpleNamespace(geteuid=lambda:0,O_RDONLY=os.O_RDONLY,O_CLOEXEC=os.O_CLOEXEC,open=opened,
        fstat=lambda fd:SimpleNamespace(st_dev=4,st_ino=100),
        stat=lambda path:SimpleNamespace(st_dev=4,st_ino=100 if path=='/proc/self/ns/net' and failure=='host-netns' else 1 if path=='/proc/self/ns/net' else 100),
        close=lambda fd:closed.append(fd))
    def entered(argv,deadline,data,pass_fds,seconds):
        trace.append('enter')
        assert argv[:3]==['/usr/bin/nsenter','--net=/proc/self/fd/9005','--'] and argv[3:8]==['/usr/bin/python3','-I','-S','-B','-c']
        assert pass_fds==(9005,) and seconds==3 and deadline==103 and trace.count('inspect')==2
        assert json.loads(data)=={"action":request['action'],"namespace":[4,100],"deadline":103}
        if failure=='entered-timeout':raise TimeoutError('synthetic entered helper timeout')
        return json.dumps({"namespace":[4,101] if failure=='entered-mismatch' else [4,100],"rules_sha256":host._NETNS_FILTER_SHA256}).encode()
    scope['run']=entered
    output=io.StringIO()
    if failure in {None,'verify'}:
        with redirect_stdout(output):scope['main']()
        assert json.loads(output.getvalue())==netns_receipt_fixture(binding)
        assert trace.count('inspect')==3 and closed==[9005]
        assert timers==[3,0]
    else:
        with redirect_stdout(output),pytest.raises((PermissionError,TimeoutError)):scope['main']()
        diagnostic=json.loads(output.getvalue())
        assert diagnostic['curis_filter_failure']==1 and diagnostic['stage'] in host._FILTER_STAGES
        assert diagnostic['kind'] in host._FILTER_ERROR_KINDS
        assert host._filter_failure_diagnostic(output.getvalue().encode())==diagnostic
        assert closed==([9005] if 'open-netns' in trace else [])
        assert timers==[3,0]
        if failure in {'boot','image','labels','pid','uid','wrong-network','host-netns','acquire-race','start-race','expected-mismatch'}:assert 'enter' not in trace


@pytest.mark.parametrize("failure",[None,"timeout","nonce","hash","pid","revoked"])
def test_owner_filter_install_is_durable_once_and_before_ready_or_dispatch(monkeypatch,failure):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    original=owner.connection.browser_filter
    def filtered(action,binding,expected=None):
        assert owner.journal.records[-1]["state"]=="NETNS_FILTER_INTENT" and not getattr(owner,"_ready",False)
        if failure=='timeout':raise TimeoutError('synthetic admitted filter timeout')
        receipt=original(action,binding,expected)
        if failure=='nonce':receipt['nonce']='f'*48
        if failure=='hash':receipt['rules_sha256']='foreign'
        if failure=='pid':receipt['pid']=True
        if failure=='revoked':owner._revoked_event.set()
        return receipt
    owner.connection.browser_filter=filtered
    if failure:
        with pytest.raises((PermissionError,TimeoutError)):owner.start_runtime()
        assert not getattr(owner,'_ready',False) and owner.stop_requested and owner.journal.closed
        assert not any(r['state']=='NETNS_FILTER_VERIFIED' for r in owner.journal.records)
        assert owner.journal.records[-1]['state']=='STOP_RETURNED'
        assert len(networks)==2 and not any(c['running'] for c in containers.values())
        with pytest.raises(PermissionError):host._DedicatedDockerOwner(IDENTITY,owner.image_digest).prepare('b'*48,hosts=['example.com'])
    else:
        owner.start_runtime()
        states=[r['state'] for r in owner.journal.records]
        assert states.index('NETNS_FILTER_INTENT')<states.index('NETNS_FILTER_VERIFIED')<states.index('ATTACHED')
        assert owner._ready and owner._filter_snapshot['rules_sha256']==host._NETNS_FILTER_SHA256
        before=list(events)
        with pytest.raises(PermissionError):owner._install_netns_filter()
        assert events==before


@pytest.mark.parametrize("stage",['before','after','missing'])
def test_dispatch_requires_original_filter_before_and_after_result(monkeypatch,stage):
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    owner.start_runtime()
    verified,forwarded=[],[]
    original=owner.connection.browser_filter
    def filtered(action,binding,expected=None):
        verified.append(action)
        receipt=original(action,binding,expected)
        if stage=='before' or stage=='after' and len(verified)==2:receipt['namespace']=[4,101]
        return receipt
    owner.connection.browser_filter=filtered
    owner._channel.request=lambda frame:forwarded.append(frame) or {'synthetic':'late result'}
    if stage=='missing':owner._filter_snapshot=None
    frame={'identity':IDENTITY.copy(),'nonce':owner.nonce,'boot_id':owner.boot_id,
        'container_id':owner.container_id,'image_digest':owner.image_digest,'sequence':1,'action':'start','arguments':{}}
    with pytest.raises(PermissionError):owner.dispatch_if_active(IDENTITY,owner._channel,frame)
    assert len(forwarded)==(1 if stage=='after' else 0)
    assert owner.revoked and owner._revoked_event.is_set()
    with pytest.raises(PermissionError):owner.dispatch_if_active(IDENTITY,owner._channel,frame)


@pytest.mark.parametrize('failure',[None,'receipt','close-interrupt'])
def test_filter_client_uses_fixed_sudo_source_and_only_passes_ssh_inputs(failure,monkeypatch):
    import os,json,shlex
    config,pin=owner_public_inputs();closed=[]
    mock_public_ssh_fds(monkeypatch)
    binding=netns_binding_fixture();expected=netns_receipt_fixture(binding)
    monkeypatch.setattr(host,'_owner_directory',lambda:9000)
    monkeypatch.setattr(host,'_owner_file',lambda d,n,f:9001 if n.endswith('ssh.config') else 9002)
    monkeypatch.setattr(os,'read',lambda fd,n:config.encode() if fd==9001 else pin.encode())
    monkeypatch.setattr(os,'lseek',lambda *args:0)
    interruption=KeyboardInterrupt('synthetic SSH input close interrupted')
    def close(fd):
        closed.append(fd)
        if failure=='close-interrupt' and fd==9001:raise interruption
    monkeypatch.setattr(os,'close',close)
    def exchange(argv,fds,payload,seconds):
        assert fds==(9001,9002) and seconds==5
        command=shlex.split(argv[-1])
        assert command[:7]==['/usr/bin/sudo','-n','/usr/bin/python3','-I','-S','-B','-c']
        assert command[7]==host._NETNS_ROOT_SOURCE+'\nmain()\n'
        assert json.loads(payload)=={**binding,'action':'verify','expected':expected}
        receipt={**expected,'rules_sha256':'foreign'} if failure=='receipt' else expected
        return json.dumps(receipt).encode()
    monkeypatch.setattr(host,'_bounded_ssh_exchange',exchange)
    if failure:
        with pytest.raises(KeyboardInterrupt if failure=='close-interrupt' else PermissionError) as caught:
            host._DedicatedDockerSSH().browser_filter('verify',binding,expected)
        if failure=='close-interrupt':assert caught.value is interruption
    else:assert host._DedicatedDockerSSH().browser_filter('verify',binding,expected)==expected
    assert closed==[9001,9002,9000]


@pytest.mark.parametrize('failure',['command','pid','rules','action','reinstall','unbound-verify'])
def test_filter_client_rejects_arbitrary_privileged_inputs_before_owner_files(monkeypatch,failure):
    binding=netns_binding_fixture();expected=None;action='install'
    if failure in {'command','pid','rules'}:binding[failure]='caller supplied'
    if failure=='action':action='flush-global'
    if failure=='reinstall':expected=netns_receipt_fixture()
    if failure=='unbound-verify':action='verify'
    monkeypatch.setattr(host,'_owner_directory',lambda:(_ for _ in ()).throw(AssertionError('opened owner files')))
    with pytest.raises(PermissionError):host._DedicatedDockerSSH().browser_filter(action,binding,expected)


@pytest.mark.parametrize('failure',[None,'timeout','oversized','read-interrupt','cleanup-interrupt','tool-owner','exit','inner-diag','inner-invalid'])
def test_fixed_filter_child_bounds_io_deadline_and_closes_only_held_process(failure):
    import os,stat,subprocess,json,io
    from contextlib import redirect_stdout
    from types import SimpleNamespace
    scope={};exec(host._NETNS_COMMON_SOURCE,scope)
    scope['_filter_stage']='enter' if failure in {'inner-diag','inner-invalid'} else 'precheck4'
    scope['ENTER_SOURCE']='fixed-inner-source'
    argv=(['/usr/bin/nsenter','--net=/proc/self/fd/9005','--','/usr/bin/python3','-c','fixed-inner-source\nmain()\n']
        if failure in {'inner-diag','inner-invalid'} else ['/usr/sbin/iptables-save','-t','filter'])
    events=[]
    class Pipe:
        def __init__(self,fd):self.fd=fd;self.closed=False
        def fileno(self):return self.fd
        def close(self):self.closed=True;events.append(('close',self.fd))
    interruption=KeyboardInterrupt('synthetic filter interrupted')
    class Process:
        def __init__(self):self.stdin=Pipe(9001);self.stdout=Pipe(9002);self.ended=False
        def poll(self):return 0 if self.ended else None
        def terminate(self):
            events.append('terminate')
            if failure=='cleanup-interrupt':raise interruption
        def kill(self):events.append('kill');self.ended=True
        def wait(self,timeout):
            events.append('wait');assert 0<timeout<=1;self.ended=True
            return 4 if failure=='exit' else 1 if failure in {'inner-diag','inner-invalid'} else 0
    process=Process()
    def popen(arguments,**options):
        assert arguments==argv
        assert options['cwd']=='/' and options['pass_fds']==(9005,) and options['close_fds'] is True
        assert options['stderr']==subprocess.DEVNULL
        assert options['env']=={'PATH':'/usr/bin:/usr/sbin:/bin','LANG':'C'}
        events.append('spawn');return process
    scope['subprocess']=SimpleNamespace(Popen=popen,PIPE=subprocess.PIPE,DEVNULL=subprocess.DEVNULL,TimeoutExpired=subprocess.TimeoutExpired)
    chunks=([b'x'*4096]*17 if failure in {'oversized','cleanup-interrupt'} else [b'synthetic',b''])
    if failure in {'inner-diag','inner-invalid'}:
        value=dict(curis_filter_failure=1,stage='restore6',kind='PermissionError',exit_code=4)
        if failure=='inner-invalid':value['kind']='SYNTHETIC_PRIVATE_DATA'
        chunks=[(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode(),b'']
    def read(fd,count):
        assert fd==9002 and count==4096
        if failure=='read-interrupt':raise interruption
        return chunks.pop(0)
    scope['os']=SimpleNamespace(path=SimpleNamespace(realpath=lambda path:path),
        stat=lambda path:SimpleNamespace(st_mode=stat.S_IFREG|0o755,st_uid=1000 if failure=='tool-owner' else 0),
        set_blocking=lambda *args:None,write=lambda fd,data:len(data),read=read)
    now=[100.0]
    def clock():now[0]+=.6 if failure=='timeout' else .001;return now[0]
    scope['time']=SimpleNamespace(monotonic=clock)
    scope['select']=SimpleNamespace(select=lambda readable,writable,error,timeout:([],[],[]) if failure=='timeout' else (readable,writable,[]))
    if failure:
        if failure in {'exit','inner-diag','inner-invalid'}:
            with pytest.raises(scope['FilterChildFailure']) as caught:scope['run'](argv,103,b'fixed',(9005,))
            output=io.StringIO()
            with redirect_stdout(output):scope['emit_failure'](caught.value)
            diagnostic=host._filter_failure_diagnostic(output.getvalue().encode())
            assert diagnostic['stage']==('restore6' if failure=='inner-diag' else scope['_filter_stage'])
            assert diagnostic['exit_code']==(1 if failure=='inner-invalid' else 4)
            assert 'SYNTHETIC_PRIVATE_DATA' not in output.getvalue()
            assert 'terminate' not in events and process.stdout.closed and process.stdin.closed
            return
        expected=TimeoutError if failure=='timeout' else ValueError if failure=='oversized' else PermissionError if failure=='tool-owner' else KeyboardInterrupt
        with pytest.raises(expected) as caught:scope['run'](argv,103,b'fixed',(9005,))
        if failure in {'read-interrupt','cleanup-interrupt'}:assert caught.value is interruption
        if failure=='tool-owner':assert events==[]
        else:
            assert 'terminate' in events and process.ended
            assert process.stdout.closed and process.stdin.closed
    else:
        assert scope['run'](['/usr/sbin/iptables-save','-t','filter'],103,b'fixed',(9005,))==b'synthetic'
        assert 'terminate' not in events and process.stdout.closed and process.stdin.closed


def test_known_hosts_command_serializes_only_validated_public_pin_without_fd_or_path(monkeypatch):
    import shlex
    raw=mock_public_ssh_fds(monkeypatch,(901,902))
    argv=host._ssh_owner_argv(901,902)
    options=dict(item.split('=',1) for index,item in enumerate(argv) if index and argv[index-1]=='-o')
    assert argv[:4]==['/usr/bin/ssh','-T','-F','/dev/null']
    assert options['HostName']=='127.0.0.1' and options['Port']=='62173' and options['User']=='yy'
    assert options['IdentityFile']==host._OWNER_ROOT+'/lima/_config/user'
    assert options['StrictHostKeyChecking']=='yes'
    assert options['UserKnownHostsFile']==options['GlobalKnownHostsFile']=='/dev/null'
    command=shlex.split(options['KnownHostsCommand'])
    assert command==['/usr/bin/printf',r'%%s\n',raw[902].decode()]
    assert command[1].replace('%%','%')==r'%s\n'
    assert not any('/dev/fd/' in value for value in argv[:-1])
    assert not any('accept-new' in value or 'StrictHostKeyChecking=no' in value for value in argv)
    # A replaced pathname cannot change this argument: SSH consumes the validated bytes.
    raw[902]=b'foreign public bytes'
    assert command[2]==owner_public_inputs()[1]
    with pytest.raises(PermissionError):host._ssh_owner_argv(901,902)


@pytest.mark.parametrize('failure',[None,'mode','owner','hardlink','size','truncated','during-read','config-injection','pin-injection'])
def test_public_enrollment_snapshot_validates_fd_metadata_and_exact_contents(monkeypatch,failure):
    import os,stat
    raw=mock_public_ssh_fds(monkeypatch)
    original_stat,original_read=os.fstat,os.pread
    read=[False]
    def fstat(fd):
        value=original_stat(fd)
        if fd==9001:
            if failure=='mode':value.st_mode=stat.S_IFREG|0o644
            if failure=='owner':value.st_uid+=1
            if failure=='hardlink':value.st_nlink=2
            if failure=='size':value.st_size=65537
            if failure=='during-read' and read[0]:value.st_ctime_ns+=1
        return value
    def pread(fd,n,offset):
        value=original_read(fd,n,offset);read[0]=True
        return value[:-1] if failure=='truncated' else value
    monkeypatch.setattr(os,'fstat',fstat)
    monkeypatch.setattr(os,'pread',pread)
    if failure=='config-injection':raw[9001]+=b'ProxyCommand arbitrary\n'
    if failure=='pin-injection':raw[9002]+=b'\nforeign ssh-ed25519 AAAA'
    if failure:
        with pytest.raises(PermissionError):host._ssh_public_snapshot((9001,9002))
    else:
        before=host._ssh_public_snapshot((9001,9002))
        assert before[1]==owner_public_inputs()
        raw[9001]=raw[9001].replace(b'62173',b'62174')
        assert host._ssh_public_snapshot((9001,9002))!=before


@pytest.mark.parametrize('failure',['changed-after','nonzero','argv-mismatch','filter-valid','filter-secret','filter-wrong-command'])
def test_ssh_rejects_changed_enrollment_and_reports_only_bounded_exit_metadata(monkeypatch,failure):
    import os,select,subprocess,shlex,json
    raw=mock_public_ssh_fds(monkeypatch,(901,902))
    argv=host._ssh_owner_argv(901,902)
    if failure.startswith('filter-') and failure!='filter-wrong-command':
        argv[-1]='/usr/bin/sudo -n /usr/bin/python3 -I -S -B -c '+shlex.quote(host._NETNS_ROOT_SOURCE+'\nmain()\n')
    if failure=='argv-mismatch':argv[argv.index('Port=62173')]='Port=62174'
    class Stream:
        def __init__(self,fd):self.fd=fd;self.closed=False
        def fileno(self):return self.fd
        def close(self):self.closed=True
    class Process:
        stdin=Stream(8001);stdout=Stream(8002);ended=False
        def poll(self):return 0 if self.ended else None
        def terminate(self):raise AssertionError('already reaped child')
        def wait(self,timeout):
            self.ended=True
            if failure=='changed-after':raw[901]=raw[901].replace(b'62173',b'62174')
            return 255 if failure=='nonzero' else 1 if failure.startswith('filter-') else 0
    process=Process();spawned=[]
    def popen(arguments,**options):
        spawned.append(arguments)
        assert options['pass_fds']==() and options['stderr'] is subprocess.DEVNULL
        return process
    monkeypatch.setattr(subprocess,'Popen',popen)
    monkeypatch.setattr(os,'set_blocking',lambda *args:None)
    monkeypatch.setattr(os,'write',lambda fd,data:len(data))
    chunks=[b'SYNTHETIC_PRIVATE_OUTPUT',b'']
    if failure.startswith('filter-'):
        diagnostic=dict(curis_filter_failure=1,stage='restore4',kind='SYNTHETIC_PRIVATE_OUTPUT' if failure=='filter-secret' else 'PermissionError',exit_code=4)
        chunks[0]=(json.dumps(diagnostic,sort_keys=True,separators=(',',':'))+'\n').encode()
    monkeypatch.setattr(os,'read',lambda fd,n:chunks.pop(0))
    monkeypatch.setattr(select,'select',lambda r,w,x,timeout:(r,w,[]))
    with pytest.raises(PermissionError) as caught:host._bounded_ssh_exchange(argv,(901,902),b'{}',5)
    assert 'SYNTHETIC_PRIVATE_OUTPUT' not in str(caught.value)
    assert ('filter_stage=restore4' in str(caught.value)) is (failure=='filter-valid')
    if failure=='argv-mismatch':assert spawned==[]
    else:
        assert process.stdin.closed and process.stdout.closed
        if failure=='nonzero':
            assert 'exit=255' in str(caught.value) and 'stdout_bytes=24' in str(caught.value)
        elif failure=='changed-after':assert 'enrollment changed' in str(caught.value)


@pytest.mark.parametrize('mutation',[None,'stage','kind','extra','duplicate','whitespace','large','boolean','array','invalid',
    'exit-zero','exit-large','exit-boolean','exit-negative','exit-missing'])
def test_filter_diagnostic_accepts_only_bounded_canonical_allowlisted_metadata(mutation):
    import json
    value=dict(curis_filter_failure=1,stage='namespace',kind='OSError',exit_code=None)
    if mutation=='stage':value['stage']='SYNTHETIC_PRIVATE_DATA'
    if mutation=='kind':value['kind']='SYNTHETIC_PRIVATE_DATA'
    if mutation=='extra':value['details']='SYNTHETIC_PRIVATE_DATA'
    if mutation=='boolean':value['curis_filter_failure']=True
    if mutation=='array':value['stage']=[]
    if mutation=='exit-zero':value['exit_code']=0
    if mutation=='exit-large':value['exit_code']=256
    if mutation=='exit-boolean':value['exit_code']=True
    if mutation=='exit-negative':value['exit_code']=-65
    if mutation=='exit-missing':value.pop('exit_code')
    raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
    if mutation=='duplicate':raw=raw.replace(b'{',b'{"stage":"SYNTHETIC_PRIVATE_DATA",',1)
    if mutation=='whitespace':raw=b' '+raw
    if mutation=='large':raw=b'x'*513
    if mutation=='invalid':raw=b'not-json'
    assert (host._filter_failure_diagnostic(raw)==value) is (mutation is None)


def vm_released_lock():
    return {"complete": True, "executionAuthorized": True, "runtimeKind": "VM",
            "browserImageDigest": "sha256:" + "a" * 64, "proxyImageDigest": "sha256:" + "a" * 64,
            "hostHelperClosure": {"kind": "DEDICATED_DOCKER_SSH_V1", "root": host._OWNER_ROOT,
                "alias": host._OWNER_ALIAS, "hostKeySha256": host._OWNER_HOST_KEY_SHA256,
                "seccompSha256": host._PRIVATE_SECCOMP_SHA256}}


@pytest.mark.parametrize("tamper", [None, "complete", "executionAuthorized", "runtimeKind", "image", "proxy", "closure"])
def test_vm_factory_requires_fixed_release_before_construction(monkeypatch, tamper):
    lock = vm_released_lock()
    calls = []
    if tamper in ("complete", "executionAuthorized"): lock[tamper] = False
    if tamper == "runtimeKind": lock[tamper] = "NATIVE_BROWSERSKILL"
    if tamper == "image": lock["browserImageDigest"] = "sha256:bad"
    if tamper == "proxy": lock["proxyImageDigest"] = "sha256:" + "b" * 64
    if tamper == "closure": lock["hostHelperClosure"]["root"] = "/other"
    monkeypatch.setattr("app.agent_browser_runtime.load_trusted_reader_lock", lambda: lock)
    def construct(identity, image):
        calls.append((identity, image))
        return "synthetic-owner"
    monkeypatch.setattr(host, "_DedicatedDockerOwner", construct)
    if tamper:
        with pytest.raises(ValueError, match="not released"): host._open_verified_vm_owner(IDENTITY)
        assert calls == []
    else:
        assert host._open_verified_vm_owner(IDENTITY) == "synthetic-owner"
        assert calls == [(IDENTITY, lock["browserImageDigest"])]


@pytest.mark.parametrize("failure", [None, "prepare", "after-prepare", "start", "snapshot", "lease-start", "stop"])
def test_vm_work_hold_precedes_allocation_and_startup_failure_stops_exact_generation(monkeypatch, failure):
    from app.agent_browser_policy import PublicTargets
    events, stopped = [], [False]
    class Dedicated(host._DedicatedDockerOwner):
        def __init__(self):
            self.identity = IDENTITY.copy()
            self.boot_id, self.container_id, self.image_digest = RUNTIME["boot_id"], None, RUNTIME["image_digest"]
            self.proxy_id, self.nonce, self.stop_requested = None, None, False
        def prepare(self, nonce, *, hosts):
            assert host._WORK_HOLDS[("tenant", "company", "work")]["owner"] is self
            assert hosts == ["example.com"]
            events.append("prepare")
            self.nonce = nonce
            if failure == "prepare": raise ValueError("synthetic prepare")
            self.container_id, self.proxy_id = RUNTIME["container_id"], "proxy"
            if failure == "after-prepare": stopped[0] = True
        def start_runtime(self):
            events.append("bootstrap")
            if failure == "start":
                self.stop_requested = True  # Existing start_runtime already owns its one cleanup attempt.
                events.append("startup-stop")
                raise ValueError("synthetic bootstrap")
        def verified_snapshot(self, identity):
            assert identity == IDENTITY
            events.append("snapshot")
            if failure == "snapshot": raise ValueError("synthetic snapshot")
            return RUNTIME.copy()
        def bind_session(self, identity, nonce, snapshot):
            assert nonce == self.nonce and snapshot == RUNTIME
            events.append("bind")
            return Transport([])
        def dispatch_if_active(self, identity, transport, frame):
            events.append(frame["action"])
            if failure == "lease-start": raise ValueError("synthetic start frame")
            return transport.request(frame)
        def revoke_bound_and_stop(self, identity, nonce, snapshot):
            assert identity == self.identity and nonce == self.nonce
            assert snapshot["container_id"] == self.container_id and snapshot["boot_id"] == self.boot_id
            assert snapshot["image_digest"] == self.image_digest
            self.stop_requested = True
            events.append("stop")
            if failure == "stop": raise OSError("synthetic stop")
    owner = Dedicated()
    monkeypatch.setattr(host, "_open_verified_vm_owner", lambda identity: owner)
    if failure and failure != "stop":
        with pytest.raises((ValueError, PermissionError)) as error:
            host.open_owned_reader(IDENTITY, PublicTargets(["example.com"]), lambda: stopped[0])
        assert any("UNKNOWN" in note for note in error.value.__notes__)
        assert events.count("stop") == (1 if failure in ("after-prepare", "snapshot", "lease-start") else 0)
    else:
        lease = host.open_owned_reader(IDENTITY, PublicTargets(["example.com"]), lambda: stopped[0])
        assert events.count("start") == 1 and events.index("prepare") < events.index("bootstrap") < events.index("start")
        if failure == "stop":
            with pytest.raises(OSError): lease.close()
            with pytest.raises(RuntimeError, match="UNKNOWN"): lease.close()
        else: lease.close()
        assert events.count("stop") == 1
    with pytest.raises(PermissionError, match="unresolved owner"):
        host.open_owned_reader(IDENTITY, PublicTargets(["example.com"]), lambda: False)
    assert events.count("prepare") == 1


@pytest.mark.parametrize("tamper", [None, "release", "revoked", "not-ready", "proxy-exit", "browser-restart", "pid", "label", "image", "filter", "topology", "late-revoke"])
def test_released_snapshot_rechecks_both_running_containers_and_filter(monkeypatch, tamper):
    import threading
    owner = object.__new__(host._DedicatedDockerOwner)
    owner.identity, owner.image_digest = IDENTITY.copy(), "sha256:" + "a" * 64
    owner.boot_id, owner.container_id, owner.proxy_id = "boot", "browser", "proxy"
    owner.nonce = "c" * 48
    owner._record = {"work": "owned-work"}
    owner._image_labels = {"base-label": "value"}
    owner._state_lock, owner._revoked_event = threading.Lock(), threading.Event()
    owner.revoked, owner.stop_requested, owner._ready = tamper == "revoked", False, tamper != "not-ready"
    lock = vm_released_lock()
    if tamper == "release": lock["complete"] = False
    monkeypatch.setattr("app.agent_browser_runtime.load_trusted_reader_lock", lambda: lock)
    calls = []
    def verify(stage):
        calls.append(stage)
        if tamper == stage: raise PermissionError("synthetic changed " + stage)
    owner._topology = lambda: verify("topology")
    owner._verify_netns_filter = lambda: verify("filter")
    class Connection:
        def request(self, method, path, *, boot_id):
            assert method == "GET" and boot_id == "boot"
            cid = path.split('/')[2]
            calls.append(cid)
            labels = {**owner._image_labels, "curis.reader.work": "owned-work", "curis.reader.nonce": owner.nonce}
            if cid == "proxy": labels["curis.reader.role"] = "proxy"
            value = {"Id": cid, "Image": owner.image_digest, "Config": {"Labels": labels},
                     "State": {"Running": True, "Restarting": False, "Status": "running", "Pid": 123},
                     "HostConfig": {"RestartPolicy": {"Name": "no"}}}
            if tamper == "proxy-exit" and cid == "proxy": value["State"]["Running"] = False
            if tamper == "browser-restart" and cid == "browser": value["HostConfig"]["RestartPolicy"]["Name"] = "always"
            if tamper == "pid": value["State"]["Pid"] = True
            if tamper == "label": value["Config"]["Labels"] = {}
            if tamper == "image": value["Image"] = "sha256:" + "b" * 64
            if tamper == "late-revoke" and cid == "browser": owner._revoked_event.set()
            return {"body": value}
    owner.connection = Connection()
    if tamper:
        with pytest.raises(PermissionError): owner.verified_snapshot(IDENTITY)
    else:
        assert owner.verified_snapshot(IDENTITY) == {**RUNTIME, "container_id": "browser", "image_digest": owner.image_digest}
        assert calls == ["topology", "filter", "proxy", "browser"]


@pytest.mark.parametrize("retirement",["partial","removed"])
@pytest.mark.parametrize("references",[False,True])
def test_retirement_recovery_accepts_only_observed_prior_removal(monkeypatch,retirement,references):
    test_stopped_unknown_recovery_real_journal_and_next_work(monkeypatch,references,None,retirement)


def agent_container_fixture(monkeypatch, mode='completed'):
    import threading
    owner,events,networks,containers=network_owner_fixture(monkeypatch,prepared=False)
    closed,stopping=threading.Event(),threading.Event()
    class Channel:
        def __init__(self,cid,boot,**kwargs):
            self.cid,self.closed=cid,False
            assert kwargs=={'timeout_seconds':80}
            events.append(('agent_attach',cid))
        def request(self,frame):
            expected={k:v for k,v in frame.items() if k not in {'action','arguments'}}
            if frame['action']=='bootstrap':
                return {**expected,'result':{'ready':True,'network':'none','credentials':False}}
            events.append(('agent_execute',self.cid))
            if mode in {'cancelled','late'}:stopping.set()
            if mode in {'cancelled','late','timeout'}:
                assert closed.wait(2)
                if mode!='late':raise EOFError('synthetic disconnected channel')
            if mode=='eof':raise EOFError('synthetic input EOF')
            if mode=='foreign':expected['nonce']='f'*48
            return {**expected,'result':{'reason':'completed','returncode':0,'stdout':'fixture result','stderr':''}}
        def close(self):
            self.closed=True;closed.set();events.append(('agent_channel_closed',self.cid))
            if mode=='close-failure':raise OSError('synthetic close failure')
    monkeypatch.setattr(host,'_DockerAttachChannel',Channel)
    monkeypatch.setattr(host,'_AGENT_CONTAINER_IMAGE',owner.image_digest)
    monkeypatch.setattr(host,'_DedicatedDockerOwner',lambda identity,image:owner)
    session=host._OwnedAgentContainerSession(IDENTITY,owner.image_digest)
    return session,owner,events,containers,stopping


@pytest.mark.parametrize('mode',['completed','cancelled','timeout','eof','late','foreign','close-failure'])
def test_owned_agent_container_revokes_stops_before_result_and_never_replays(monkeypatch,mode):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch,mode)
    command=['/usr/bin/python3','-I','-B','-c','print("fixture")']
    if mode=='completed':
        result=session.run(command,input='',timeout=1,should_stop=stopping.is_set)
        assert result['stdout']=='fixture result' and result['stop_receipt']['ledger_state']=='CLOSED_VERIFIED'
    else:
        with pytest.raises(host.OwnedAgentContainerError) as failure:
            session.run(command,input='',timeout=.08 if mode=='timeout' else 1,should_stop=stopping.is_set)
        assert failure.value.reason=={'late':'cancelled','foreign':'response_invalid','close-failure':'cleanup_unknown'}.get(mode,mode)
    cid=owner.container_id
    assert len(containers)==1 and not containers[cid]['running']
    assert containers[cid]['spec']['HostConfig']['NetworkMode']=='none'
    assert containers[cid]['spec']['HostConfig']['Binds']==[]
    assert containers[cid]['spec']['StdinOnce'] is True
    assert not owner.private_network and not owner.proxy_id
    assert events.index(('agent_channel_closed',cid))<events.index(('POST','/containers/'+cid+'/stop?t=1'))
    assert events.count(('POST','/containers/'+cid+'/stop?t=1'))==1
    assert owner._revoked_event.is_set()
    with pytest.raises(PermissionError,match='replayed'):
        session.run(command,input='',timeout=1,should_stop=lambda:False)


@pytest.mark.parametrize('stage',['image','create'])
def test_owned_agent_container_cancel_during_prepare_retains_id_before_stop(monkeypatch,stage):
    import threading,time
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    request=owner.connection.request
    def blocked(method,path,**options):
        if (stage=='image' and path.startswith('/images/') or stage=='create' and path=='/containers/create'):
            stopping.set();time.sleep(.05)
        return request(method,path,**options)
    owner.connection.request=blocked
    with pytest.raises(host.OwnedAgentContainerError) as failure:
        session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=stopping.is_set)
    assert failure.value.reason=='cancelled'
    assert not any(event[0]=='agent_execute' for event in events)
    if stage=='image':
        assert containers=={} and not any(row['state']=='INTENT' for row in owner.journal.records)
    else:
        states=[r['state'] for r in owner.journal.records]
        assert states==['INTENT','CREATED','REVOKING','STOP_RETURNED','CLOSED_VERIFIED']
        assert len(containers)==1 and all(not c['running'] for c in containers.values())


@pytest.mark.parametrize('field',['Entrypoint','StdinOnce','Env','Binds','NetworkMode'])
def test_owned_agent_rejects_security_drift_before_command(monkeypatch,field):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    request=owner.connection.request
    def changed(method,path,**options):
        result=request(method,path,**options)
        if path.startswith('/containers/') and path.endswith('/json'):
            value=result['body']
            target=value['HostConfig'] if field in {'Binds','NetworkMode'} else value['Config']
            target[field]={'Binds':['/host:/host'],'NetworkMode':'host','Env':['HOST_SECRET=forbidden'],
                'Entrypoint':['/bin/sh'],'StdinOnce':False}[field]
        return result
    owner.connection.request=changed
    with pytest.raises(host.OwnedAgentContainerError):
        session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
    assert not any(event[0]=='agent_execute' for event in events)


def test_owned_agent_unknown_create_never_guesses_or_stops_discovered_container(monkeypatch):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    request=owner.connection.request
    def unknown(method,path,**options):
        value=request(method,path,**options)
        if path=='/containers/create':raise TimeoutError('synthetic create outcome unknown')
        return value
    owner.connection.request=unknown
    with pytest.raises(host.OwnedAgentContainerError,match='cleanup_unknown'):
        session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
    assert owner.container_id is None and len(containers)==1
    assert not any(method=='POST' and '/stop?' in path for method,path in events)


def test_owned_agent_public_factory_is_held_before_any_owner_allocation(monkeypatch):
    import app.agent_adapter as adapter
    monkeypatch.setattr(adapter,'AGENT_CONTAINER_EXECUTION_VERIFIED',False)
    monkeypatch.setattr(host,'_DedicatedDockerOwner',lambda *a:(_ for _ in ()).throw(AssertionError('allocated owner')))
    with pytest.raises(adapter.AgentExecutionError,match='尚未通过验收'):
        host.open_owned_agent_container(IDENTITY)
    compile(host._AGENT_CONTAINER_SOURCE,'fixed-linux-agent-source','exec')


def test_owned_agent_revocation_before_start_intent_never_appends_late_audit(monkeypatch):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    verify=owner._verify_agent_container
    def revoke_before_start(*,running):
        result=verify(running=running)
        if not running:session.revoke('cancelled')
        return result
    owner._verify_agent_container=revoke_before_start
    with pytest.raises(host.OwnedAgentContainerError) as error:
        session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
    assert error.value.reason=='cancelled'
    assert [r['state'] for r in owner.journal.records]==['INTENT','CREATED','REVOKING','STOP_RETURNED','CLOSED_VERIFIED']
    assert not any(e[0] in {'agent_attach','agent_execute'} for e in events)


def test_owned_agent_close_before_run_allocates_nothing(monkeypatch):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    assert session.close() is None and events==[] and containers=={}
    with pytest.raises(host.OwnedAgentContainerError):
        session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
    assert events==[]


@pytest.mark.parametrize('case',['late-tail','overflow','deadline-with-open-descendant-pipe'])
def test_agent_guest_drains_actual_loop_until_eof_with_original_bounds(case):
    import ast,types
    tree=ast.parse(host._AGENT_CONTAINER_SOURCE)
    node=next(n for n in tree.body if isinstance(n,ast.Try)
              and any(isinstance(x,ast.Assign) and isinstance(x.value,ast.Call)
                      and isinstance(x.value.func,ast.Attribute) and x.value.func.attr=='Popen' for x in n.body))
    clock=[0.0];calls=[];emitted=[]
    class Pipe:
        def __init__(self,fd):self.fd,self.closed=fd,False
        def fileno(self):return self.fd
        def close(self):self.closed=True
    stdin,output,error,control=Pipe(10),Pipe(11),Pipe(12),Pipe(0)
    child=types.SimpleNamespace(stdin=stdin,stdout=output,stderr=error,returncode=0,poll=lambda:0)
    def select(readers,writers,exceptional,timeout):
        calls.append(timeout);clock[0]+=timeout
        if len(calls)==1:return [error],[],[]
        if case=='deadline-with-open-descendant-pipe':return [],[],[]
        return [output],[],[]
    chunks={12:[b''],11:[b'x'*8193 if case=='overflow' else b'last result bytes',b'']}
    def read(fd,count):return chunks[fd].pop(0)
    namespace={'subprocess':types.SimpleNamespace(Popen=lambda *a,**k:child,TimeoutExpired=TimeoutError,PIPE=-1),
        'command':['fixed'],'args':{'input':'','timeout':.025 if case=='deadline-with-open-descendant-pipe' else 1},
        'os':types.SimpleNamespace(set_blocking=lambda *a:None,read=read),
        'time':types.SimpleNamespace(monotonic=lambda:clock[0]),'select':types.SimpleNamespace(select=select),
        'sys':types.SimpleNamespace(stdin=control),'out':bytearray(),'err':bytearray(),'child':None,
        'reason':'completed','binding':{},'emit':lambda binding,value:emitted.append(value),
        'read_frame':lambda timeout:(_ for _ in ()).throw(EOFError())}
    code=compile(ast.Module(body=[node],type_ignores=[]),'actual-fixed-guest-output-loop','exec')
    if case=='overflow':
        with pytest.raises(ValueError,match='output bound'):exec(code,namespace)
        assert not emitted
    else:
        exec(code,namespace)
        if case=='late-tail':
            assert emitted==[{'reason':'completed','returncode':0,'stdout':'last result bytes','stderr':''}]
            assert output.closed and error.closed and len(calls)==3
        else:
            assert emitted==[{'reason':'timeout'}] and clock[0]<=.025
    assert all(0<=value<=.02 for value in calls)


@pytest.mark.parametrize('retry',[0,1,True])
def test_agent_container_accepts_only_docker_explicit_zero_retry_default(monkeypatch,retry):
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    request=owner.connection.request
    def normalized(method,path,**options):
        result=request(method,path,**options)
        if path.startswith('/containers/') and path.endswith('/json'):
            result['body']['HostConfig']['RestartPolicy']['MaximumRetryCount']=retry
        return result
    owner.connection.request=normalized
    if type(retry) is int and retry==0:
        result=session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
        assert result['stop_receipt']['ledger_state']=='CLOSED_VERIFIED'
    else:
        with pytest.raises(host.OwnedAgentContainerError) as error:
            session.run(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1,should_stop=lambda:False)
        assert error.value.diagnostic=={'phase':'bootstrap','exception':'PermissionError','code':'RESTART_POLICY'}
        assert not any(row[0]=='agent_execute' for row in events)


@pytest.mark.parametrize('failure',[False,True])
def test_owner_waits_for_original_attach_close_before_deciding_cleanup(monkeypatch,failure):
    import threading,time
    attach_class=host._DockerAttachChannel
    owner,events,networks,containers=network_owner_fixture(monkeypatch)
    channel=object.__new__(attach_class)
    channel.closed=False
    channel._close_lock=threading.Lock()
    channel._close_done=threading.Event()
    channel._close_pending=channel._close_failure=False
    entered,release=threading.Event(),threading.Event()
    errors=[]
    class Pipe:
        def close(self):
            entered.set();assert release.wait(2)
            if failure:raise OSError('synthetic true close failure')
    channel.pipe,channel.process=Pipe(),None
    owner.channels=[channel]
    def close():
        try:channel.close()
        except BaseException as error:errors.append(error)
    thread=threading.Thread(target=close);thread.start();assert entered.wait(2)
    timer=threading.Timer(.05,release.set);timer.start()
    try:
        if failure:
            with pytest.raises(RuntimeError,match='incomplete'):owner.revoke_bound_and_stop(IDENTITY,owner.nonce,owner_stop_snapshot(owner))
            assert owner.journal.records[-1]['state']=='REVOKING'
        else:
            owner.revoke_bound_and_stop(IDENTITY,owner.nonce,owner_stop_snapshot(owner))
            assert owner.journal.records[-1]['state']=='CLOSED_VERIFIED'
    finally:
        release.set();thread.join(2);timer.join(2)
    assert channel.wait_closed(.01) is (not failure)
    assert bool(errors) is failure
    assert all(not v['running'] for v in containers.values())


@pytest.mark.parametrize('tamper',[None,'ledger','inspection','running','boot','nonce','state','post-intent','intent-write','none','none-active','none-foreign','none-invalid'])
def test_revoked_agent_exact_stopped_recovery_keeps_audit_without_runtime_mutation(monkeypatch,tamper):
    import copy,hashlib,json,os,uuid
    from pathlib import Path
    real_file,real_journal=host._owner_file,host._OwnerJournal
    root=Path('/private/tmp/curis-exec-20261029-dev02');prefix='agent-recovery-'+uuid.uuid4().hex+'-'
    for name in ['reader-owner.lock','reader-owner-ledger.jsonl','reader-owner-agent-ledger.jsonl']:
        fd=os.open(root/(prefix+name),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
    monkeypatch.setattr(host,'_owner_directory',lambda:os.open(root,os.O_RDONLY|os.O_DIRECTORY))
    monkeypatch.setattr(host,'_owner_file',lambda directory,name,flags:real_file(directory,prefix+name,flags))
    owner=host._DedicatedDockerOwner(IDENTITY,host._AGENT_CONTAINER_IMAGE)
    old='01234567-0123-0123-0123-0123456789ab';new='11234567-0123-0123-0123-0123456789ab';cid='c'*64
    base={'work':hashlib.sha256(json.dumps(IDENTITY,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
          'nonce':'a'*48,'boot_id':old,'image_digest':host._AGENT_CONTAINER_IMAGE}
    seed=real_journal()
    for state in ['INTENT','CREATED','START_INTENT','ATTACHED','REVOKING']:
        seed.append({**base,'state':state,**({'container_id':cid} if state=='CREATED' else
            {'container_id':cid,'proxy_id':None} if state!='INTENT' else {})})
    raw=os.pread(seed.ledger_fd,1048577,0);seed.close()
    pins={**base,'container_id':cid,'proxy_id':None,'networks':{}}
    info={'Id':cid,'Image':host._AGENT_CONTAINER_IMAGE,'Config':{'Labels':{'curis.reader.work':base['work'],'curis.reader.nonce':base['nonce']}},
          'HostConfig':{'RestartPolicy':{'Name':'no'},'NetworkMode':'none','PidMode':'','Binds':None,'Privileged':False},
          'NetworkSettings':{'Networks':{}},'State':{'Status':'exited','Running':False,'Restarting':False,'Dead':False,'Pid':0,
              'ExitCode':137,'StartedAt':'synthetic-start','FinishedAt':'synthetic-finish'}}
    if tamper in {'none','none-active','none-foreign','none-invalid'}:
        endpoint={k:None for k in ('IPAMConfig','Links','Aliases','DriverOpts','DNSNames')}
        endpoint.update({k:'' for k in ('EndpointID','Gateway','IPAddress','MacAddress','IPv6Gateway','GlobalIPv6Address')})
        endpoint.update(GwPriority=0,IPPrefixLen=0,GlobalIPv6PrefixLen=0,NetworkID='a'*64)
        if tamper=='none-active':endpoint['IPAddress']='172.17.0.2'
        if tamper=='none-invalid':endpoint['GwPriority']=False
        info['NetworkSettings']['Networks']={'foreign' if tamper=='none-foreign' else 'none':endpoint}
    def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    inspection=digest({'containers':{cid:info},'networks':{}});calls=[]
    class Connection:
        def request(self,method,path,**options):
            calls.append((method,path));assert method=='GET'
            if path=='/version':return {'boot_id':old if tamper=='boot' else new,'body':{'Os':'linux','Arch':'arm64','Version':'29.5.2'}}
            if path.startswith('/images/'):return {'body':{'Id':host._AGENT_CONTAINER_IMAGE,'Config':{'Labels':{}}}}
            if tamper=='post-intent' and owner.journal.records[-1]['state']=='AGENT_REVOKED_RECOVERY_INTENT':raise TimeoutError('synthetic interrupted verification')
            value=copy.deepcopy(info)
            if tamper=='running':value['State']['Running']=True
            return {'body':value}
    owner.connection=Connection()
    if tamper=='nonce':pins['nonce']='b'*48
    if tamper=='state':
        original=owner._history_groups
        def history(*args,**kwargs):
            groups=original(*args,**kwargs);groups[-1]['state']='ATTACHED';return groups
        owner._history_groups=history
    if tamper=='intent-write':
        original_append=real_journal.append
        def append(self,row):
            if row['state']=='AGENT_REVOKED_RECOVERY_INTENT':raise OSError('synthetic fsync failure')
            return original_append(self,row)
        monkeypatch.setattr(real_journal,'append',append)
    kwargs={'ledger_sha256':'0'*64 if tamper=='ledger' else hashlib.sha256(raw).hexdigest(),
            'inspection_sha256':'0'*64 if tamper=='inspection' else inspection}
    if tamper not in {None,'none'}:
        with pytest.raises((PermissionError,TimeoutError,OSError)):owner.recover_revoked_agent(pins,**kwargs)
        assert owner.journal.records[-1]['state']!='CLOSED_VERIFIED'
    else:
        receipt=owner.recover_revoked_agent(pins,**kwargs)
        assert receipt['descendants']==receipt['effects']=='UNKNOWN'
        assert receipt['exit_codes']=={cid:137}
        groups=owner._history_groups();assert groups[-1]['state']=='CLOSED_VERIFIED'
        persisted=(root/(prefix+'reader-owner-ledger.jsonl')).read_bytes();assert persisted.startswith(raw)
    with pytest.raises(PermissionError):owner.recover_revoked_agent(pins,**kwargs)
    assert all(method=='GET' for method,path in calls)


@pytest.mark.parametrize('change',['valid','empty','address','gateway','ipv6','endpoint','alias','link','ipam','driver','dns','prefix','bool','id','unknown','foreign','shape'])
def test_stopped_agent_none_endpoint_requires_exact_inert_shape(change):
    endpoint={k:None for k in ('IPAMConfig','Links','Aliases','DriverOpts','DNSNames')}
    endpoint.update({k:'' for k in ('EndpointID','Gateway','IPAddress','MacAddress','IPv6Gateway','GlobalIPv6Address')})
    endpoint.update(GwPriority=0,IPPrefixLen=0,GlobalIPv6PrefixLen=0,NetworkID='a'*64)
    networks={'none':endpoint}
    mapping={'address':('IPAddress','1.2.3.4'),'gateway':('Gateway','1.2.3.1'),'ipv6':('GlobalIPv6Address','::1'),
        'endpoint':('EndpointID','b'*64),'alias':('Aliases',['foreign']),'link':('Links',[]),'ipam':('IPAMConfig',{}),
        'driver':('DriverOpts',{}),'dns':('DNSNames',[]),'prefix':('IPPrefixLen',1),'bool':('IPPrefixLen',False),
        'id':('NetworkID','foreign'),'unknown':('Foreign',None)}
    if change in mapping:
        k,v=mapping[change];endpoint[k]=v
    if change=='empty':networks={}
    if change=='foreign':networks['bridge']={}
    if change=='shape':networks={'none':None}
    assert host._stopped_agent_networks(networks) is (change in {'valid','empty'})


def linux_catalog_fixture():
    return {'models':[{'slug':'gpt-5.6-sol','tool_mode':'code_mode_only','multi_agent_version':'v2','use_responses_lite':True}]}


def paired_original_work_fixture(monkeypatch):
    import os, uuid
    from pathlib import Path
    real_journal, real_file = host._OwnerJournal, host._owner_file
    reader, events, networks, containers = network_owner_fixture(monkeypatch, prepared=False)
    root = Path('/private/tmp/curis-exec-20261029-dev02')
    prefix = 'paired-work-' + uuid.uuid4().hex + '-'
    for name in ('reader-owner-ledger.jsonl', 'reader-owner-agent-ledger.jsonl'):
        fd = os.open(root / (prefix + name), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
    monkeypatch.setattr(host, '_owner_directory', lambda: os.open(root, os.O_RDONLY | os.O_DIRECTORY))
    monkeypatch.setattr(host, '_owner_file', lambda directory, name, flags: real_file(directory, prefix + name, flags))
    monkeypatch.setattr(host, '_OwnerJournal', real_journal)
    base_attach = host._DockerAttachChannel
    class Attach(base_attach):
        def __init__(self, cid, boot_id, **options):
            super().__init__(cid, boot_id)
        def request(self, frame):
            if 'runtime' in frame and frame['hosts'] == ['auth.openai.com', 'chatgpt.com']:
                return {'identity': frame['identity'], 'nonce': frame['nonce'], 'sequence': 0, **frame['runtime'],
                        'result': {'proxy_ready': True, 'purpose': 'CODEX_PROVIDER_CONNECT_V1'}}
            if frame.get('action') == 'bootstrap':
                return {**{k: v for k, v in frame.items() if k not in {'action', 'arguments'}},
                        'result': {'ready': True, 'authenticated': False,
                            'resource_sha256': frame['arguments']['resources']['sha256'],
                            'binary_sha256': '57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1'}}
            return super().request(frame)
    monkeypatch.setattr(host, '_DockerAttachChannel', Attach)
    agent = host._DedicatedDockerOwner(IDENTITY, reader.image_digest)
    agent._linux_bootstrap = {'resources': {'resources': {}, 'sha256': 'd' * 64}, 'catalog': {}}
    return reader, agent, events, networks, containers, root, prefix


def test_original_work_parent_holds_one_real_lock_for_both_distinct_purpose_pairs(monkeypatch):
    reader, agent, events, networks, containers, root, prefix = paired_original_work_fixture(monkeypatch)
    with host.original_work_owners(IDENTITY) as parent:
        parent.bind(reader, 'reader'); reader.prepare('a' * 48, hosts=['example.com']); reader.start_runtime()
        parent.bind(agent, 'agent'); agent.prepare_agent('b' * 48); agent.start_agent_runtime()
        assert len(containers) == 4 and len(networks) == 4
        assert {n['IPAM']['Config'][0]['Subnet'] for n in networks.values()} == {
            '172.30.251.0/29', '172.30.252.0/29', '172.30.253.0/29', '172.30.254.0/29'}
        assert reader._record['parent_attempt'] == agent._record['parent_attempt'] == parent.attempt
        assert reader.journal.records is not agent.journal.records
        assert agent._filter_snapshot['rules_sha256'] == host._NETNS_PAIRED_FILTER_SHA256
        assert reader._filter_snapshot['rules_sha256'] == host._NETNS_FILTER_SHA256
        assert 'CURIS_AGENT_PAIRED_NETWORK=1' in agent._provider_proxy_config['Env']
        with pytest.raises(BlockingIOError): host._OwnerJournal()
        other = host._DedicatedDockerOwner({**IDENTITY, 'work_ref': 'other'}, reader.image_digest)
        with pytest.raises(BlockingIOError): other.prepare('c' * 48)
        assert len(containers) == 4
    assert networks == {} and all(not c['running'] for c in containers.values())
    assert reader.stop_receipt['ledger_state'] == agent.stop_receipt['ledger_state'] == 'CLOSED_VERIFIED'
    journal = host._OwnerJournal()
    try:
        assert journal.records[-1]['state'] == journal.peer.records[-1]['state'] == 'CLOSED_VERIFIED'
    finally: journal.close()


@pytest.mark.parametrize('field', list(IDENTITY))
def test_parent_never_joins_a_child_with_changed_identity_field(monkeypatch, field):
    reader, agent, events, networks, containers, root, prefix = paired_original_work_fixture(monkeypatch)
    with host.original_work_owners(IDENTITY) as parent:
        foreign = host._DedicatedDockerOwner({**IDENTITY, field: 'foreign'}, reader.image_digest)
        with pytest.raises(PermissionError): parent.bind(foreign, 'agent')
        parent.bind(reader, 'reader')
        with pytest.raises(PermissionError): parent.bind(agent, 'reader')
        with pytest.raises(PermissionError):
            with host.original_work_owners({**IDENTITY, 'task_id': 'foreign'}): pass
    assert not containers and not networks


@pytest.mark.parametrize('failure', ['missing-reader', 'missing-agent', 'corrupt-agent', 'unclosed-agent'])
def test_independent_owner_rejects_missing_corrupt_or_unclosed_child_history(monkeypatch, failure):
    import json
    reader, agent, events, networks, containers, root, prefix = paired_original_work_fixture(monkeypatch)
    if failure.startswith('missing-'):
        (root / (prefix + ('reader-owner-ledger.jsonl' if failure == 'missing-reader' else 'reader-owner-agent-ledger.jsonl'))).unlink()
    else:
        value = 'not-json\n' if failure == 'corrupt-agent' else json.dumps({
            'work': '1' * 64, 'nonce': 'a' * 48, 'boot_id': '01234567-0123-0123-0123-0123456789ab',
            'image_digest': reader.image_digest, 'state': 'INTENT'}) + '\n'
        (root / (prefix + 'reader-owner-agent-ledger.jsonl')).write_text(value)
    with pytest.raises((FileNotFoundError, ValueError, PermissionError)): reader.prepare('c' * 48, hosts=['example.com'])
    assert not containers and not networks


def test_parent_unknown_child_still_stops_the_other_and_retains_real_lease(monkeypatch):
    reader, agent, events, networks, containers, root, prefix = paired_original_work_fixture(monkeypatch)
    monkeypatch.setattr(host, '_UNRESOLVED_WORK_OWNERS', [])
    parent = host.original_work_owners(IDENTITY)
    try:
        with pytest.raises(RuntimeError, match='lease retained'):
            with parent:
                parent.bind(reader, 'reader'); reader.prepare('a' * 48, hosts=['example.com']); reader.start_runtime()
                parent.bind(agent, 'agent'); agent.prepare_agent('b' * 48); agent.start_agent_runtime()
                original = agent.connection.request
                def failing_stop(method, path, **options):
                    if path.endswith('/stop?t=1'): raise TimeoutError('synthetic stop UNKNOWN')
                    return original(method, path, **options)
                agent.connection.request = failing_stop
        assert reader.stop_receipt['ledger_state'] == 'CLOSED_VERIFIED'
        assert agent.stop_receipt is None and host._UNRESOLVED_WORK_OWNERS == [parent]
        assert not containers[reader.container_id]['running'] and not containers[reader.proxy_id]['running']
        with pytest.raises(BlockingIOError): host._OwnerJournal()
    finally:
        if parent.journal is not None: parent.journal.close()  # Synthetic fixture teardown only.


def test_parent_keeps_global_lease_after_first_child_closes_and_rejects_changed_boot(monkeypatch):
    reader, agent, events, networks, containers, root, prefix = paired_original_work_fixture(monkeypatch)
    with host.original_work_owners(IDENTITY) as parent:
        parent.bind(reader, 'reader'); reader.prepare('a' * 48, hosts=['example.com']); reader.start_runtime()
        parent.bind(agent, 'agent'); agent.boot_id = '11234567-0123-0123-0123-0123456789ab'
        with pytest.raises(PermissionError, match='boot changed'): parent.borrow(agent)
        agent.prepare_agent('b' * 48); agent.start_agent_runtime()
        agent.revoke_bound_and_stop(IDENTITY, agent.nonce, {'complete': False, 'executionAuthorized': False,
            'boot_id': agent.boot_id, 'container_id': agent.container_id, 'image_digest': agent.image_digest})
        assert containers[reader.container_id]['running'] and len(networks) == 2
        with pytest.raises(BlockingIOError): host._OwnerJournal()
    assert networks == {} and reader.stop_receipt['ledger_state'] == 'CLOSED_VERIFIED'
    with pytest.raises(PermissionError): parent.__enter__()


def test_paired_filter_client_sends_only_fixed_alternate_rules_and_rejects_reader_receipt(monkeypatch):
    import os, json, shlex
    config, pin = owner_public_inputs()
    mock_public_ssh_fds(monkeypatch)
    binding = netns_binding_fixture(); receipt = netns_receipt_fixture(binding)
    receipt['rules_sha256'] = host._NETNS_PAIRED_FILTER_SHA256
    with pytest.raises(PermissionError): host._netns_receipt(binding, receipt)
    assert host._netns_receipt(binding, receipt, paired=True) == receipt
    monkeypatch.setattr(host, '_owner_directory', lambda: 9000)
    monkeypatch.setattr(host, '_owner_file', lambda d,n,f: 9001 if n.endswith('ssh.config') else 9002)
    monkeypatch.setattr(os, 'read', lambda fd,n: config.encode() if fd == 9001 else pin.encode())
    monkeypatch.setattr(os, 'lseek', lambda *args: 0)
    monkeypatch.setattr(os, 'close', lambda fd: None)
    def exchange(argv, fds, payload, seconds):
        script = shlex.split(argv[-1])[-1]
        assert script == host._NETNS_ROOT_SOURCE.replace('172.30.253.', '172.30.251.') + '\nmain()\n'
        assert '172.30.253.' not in script and '172.30.251.3' in script
        assert json.loads(payload) == {**binding, 'action': 'verify', 'expected': receipt}
        return json.dumps(receipt).encode()
    monkeypatch.setattr(host, '_bounded_ssh_exchange', exchange)
    assert host._DedicatedDockerSSH().browser_filter('verify', binding, receipt, paired=True) == receipt


@pytest.mark.parametrize('authenticated',[True,False])
def test_linux_guest_bound_bootstrap_precedes_reservation_and_original_close(monkeypatch,authenticated):
    from types import SimpleNamespace
    session,owner,events,containers,stopping=agent_container_fixture(monkeypatch)
    base_channel=host._DockerAttachChannel
    descriptor={'resources':{'identity':{k:IDENTITY[k] for k in ('tenant_id','company_id','work_ref','task_id')},'skills':[]},'sha256':'d'*64}
    tools=SimpleNamespace(identity=IDENTITY,descriptor=descriptor,bind=lambda runtime:None,revoke=lambda:events.append(('tool_revoke',)))
    session.bind_work_tools(tools)
    class LinuxChannel(base_channel):
        def request(self,frame):
            if 'action' not in frame:
                events.append(('provider_bootstrap',))
                return {'identity':frame['identity'],'nonce':frame['nonce'],'sequence':0,**frame['runtime'],
                    'result':{'proxy_ready':True,'purpose':'CODEX_PROVIDER_CONNECT_V1'}}
            if frame['action']=='bootstrap':
                assert frame['arguments']['resources']==descriptor
                assert frame['arguments']['catalog']['models'][0]['tool_mode']=='direct'
                events.append(('linux_bootstrap',))
                bound={k:v for k,v in frame.items() if k not in {'action','arguments'}}
                return {**bound,'result':{'ready':True,'authenticated':authenticated,'resource_sha256':'d'*64,
                    'binary_sha256':'57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1'}}
            assert set(frame['arguments'])=={'input','timeout'}
            assert ('reservation',) in events
            return super().request(frame)
    monkeypatch.setattr(host,'_DockerAttachChannel',LinuxChannel)
    kwargs={'timeout':2,'should_stop':stopping.is_set,'before_launch':lambda:events.append(('reservation',))}
    if authenticated:
        result=session.run_linux_candidate('original prompt',linux_catalog_fixture(),**kwargs)
        assert result['stdout']=='fixture result'
        assert events.index(('linux_bootstrap',))<events.index(('reservation',))<events.index(('agent_execute',owner.container_id))
    else:
        with pytest.raises(host.OwnedAgentContainerError) as error:session.run_linux_candidate('original prompt',linux_catalog_fixture(),**kwargs)
        assert error.value.reason=='authentication_required' and ('reservation',) not in events
        assert not any(e[0]=='agent_execute' for e in events)
    assert owner._agent_config['Entrypoint'][-1]==host._AGENT_CODEX_SOURCE
    assert owner._agent_config['HostConfig']['LogConfig']=={'Type':'none','Config':{}}
    assert owner.proxy_id and owner.private_network and owner.external_network
    assert owner._filter_snapshot is not None
    assert owner._provider_proxy_config['Cmd']==['--provider-proxy-stdio']
    assert owner.journal.records[-1]['state']=='CLOSED_VERIFIED'
    assert all(not c['running'] for c in containers.values())
    with pytest.raises(PermissionError):session.run_linux_candidate('repeat',linux_catalog_fixture(),**kwargs)


def test_linux_guest_argv_and_embedded_stdio_are_fixed_and_compile_without_execution():
    import ast,json
    for source in (host._AGENT_MCP_STDIO_SOURCE,host._AGENT_CODEX_SOURCE):compile(source,'fixed-linux-guest','exec')
    tree=ast.parse(host._AGENT_CODEX_SOURCE)
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='codex_argv')
    namespace={'json':json,'BINARY':'/opt/curis/bin/codex','WORK':'/tmp/curis-agent-work','BRIDGE':host._AGENT_MCP_STDIO_SOURCE}
    exec(compile(ast.Module(body=[function],type_ignores=[]),'actual-guest-argv','exec'),namespace)
    argv=namespace['codex_argv']()
    assert argv[:2]==['/opt/curis/bin/codex','exec'] and argv[-1]=='-'
    assert argv[argv.index('--sandbox')+1]=='read-only' and '--ignore-user-config' in argv and '--ephemeral' in argv
    assert any('mcp_servers={curis={command="/usr/bin/python3"' in x for x in argv)
    assert 'features.shell_tool=false' in argv and 'features.multi_agent=false' in argv
    assert not any('sandbox-exec' in x or 'CURIS_AGENT_TOOL_TOKEN' in x or '127.0.0.1' in x for x in argv)
    assert "env=environment" in host._AGENT_CODEX_SOURCE and "status.returncode==0" in host._AGENT_CODEX_SOURCE


@pytest.mark.parametrize('mode',['normal','oversize','closed','extra-reply'])
def test_actual_guest_stdio_bridge_bounds_frames_and_preserves_notifications(mode):
    import ast,json,socket,time
    from types import SimpleNamespace
    chunks=[b'{"jsonrpc":"2.0","id":1,"method":"initialize"}\n{"jsonrpc":"2.0","method":"notifications/initialized"}\n',b'']
    if mode=='oversize':chunks=[b'x'*32769]
    output=[]
    class Peer:
        sent=[];pending=b'';closed=False
        def settimeout(self,v):assert v>0
        def connect(self,path):assert path=='/tmp/curis-agent-work/owner-mcp.sock'
        def sendall(self,data):
            request=json.loads(data);self.sent.append(request)
            value=None if request['method']=='notifications/initialized' else {'jsonrpc':'2.0','id':1,'result':{}}
            self.pending=(json.dumps(value)+'\n').encode()+(b'{}\n' if mode=='extra-reply' else b'')
        def recv(self,n):
            if mode=='closed':return b''
            if mode=='extra-reply':data=self.pending;self.pending=b'';return data
            data=self.pending[:5];self.pending=self.pending[5:];return data
        def close(self):self.closed=True
    peer=Peer()
    namespace={'json':json,'time':time,'socket':SimpleNamespace(AF_UNIX=socket.AF_UNIX,SOCK_STREAM=socket.SOCK_STREAM,socket=lambda *a:peer),
        'sys':SimpleNamespace(stdin=SimpleNamespace(fileno=lambda:91)),
        'os':SimpleNamespace(read=lambda fd,n:chunks.pop(0)),
        'select':SimpleNamespace(select=lambda r,w,x,t:(r,[],[])),
        'print':lambda value,flush:output.append(json.loads(value))}
    tree=ast.parse(host._AGENT_MCP_STDIO_SOURCE);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef))
    exec(compile(ast.Module(body=[function],type_ignores=[]),'actual-guest-stdio','exec'),namespace)
    if mode=='normal':
        namespace['bridge_main']();assert len(peer.sent)==2 and len(output)==1
    else:
        with pytest.raises((ValueError,EOFError)):namespace['bridge_main']()
    assert peer.closed


@pytest.mark.parametrize('target',['chatgpt.com:443','auth.openai.com:443','evil.example:443','chatgpt.com:80','127.0.0.1:443','chatgpt.com.evil.example:443'])
def test_provider_connect_uses_only_exact_authorities_and_pinned_public_literal(monkeypatch,target):
    import io,socket,select,threading
    from types import SimpleNamespace
    from app.agent_browser_policy import PublicTargets
    class Stream:
        def __init__(self,header,received):self.header=header;self.received=list(received);self.sent=[];self.connected=None;self.closed=False
        def makefile(self,*args,**kwargs):return io.BytesIO(self.header)
        def recv(self,n):return self.received.pop(0)
        def sendall(self,data):self.sent.append(data)
        def shutdown(self,mode):assert mode==socket.SHUT_WR
        def connect(self,address):self.connected=address
        def close(self):self.closed=True
    raw=Stream(('CONNECT '+target+' HTTP/1.1\r\nHost: '+target+'\r\n\r\n').encode(),[b'client encrypted bytes',b''])
    upstream=Stream(b'',[b'server encrypted bytes',b''])
    policy=PublicTargets(['chatgpt.com','auth.openai.com'],resolver=lambda *a,**k:[(socket.AF_INET,socket.SOCK_STREAM,6,'',('93.184.216.34',443))])
    proxy=SimpleNamespace(policy=policy,check=lambda:None,sockets=set(),lock=threading.Lock(),total_bytes=0)
    def track(s):proxy.sockets.add(s);return s
    proxy.track=track
    monkeypatch.setattr(socket,'socket',lambda *args:upstream)
    monkeypatch.setattr(select,'select',lambda r,w,x,t:(list(r),[],[]))
    if target in {'chatgpt.com:443','auth.openai.com:443'}:
        host._serve_codex_provider_tunnel(proxy,raw)
        assert upstream.connected==('93.184.216.34',443)
        assert upstream.sent==[b'client encrypted bytes']
        assert raw.sent[-1]==b'server encrypted bytes'
    else:
        with pytest.raises(PermissionError):host._serve_codex_provider_tunnel(proxy,raw)
        assert upstream.connected is None
    assert raw.closed and not proxy.sockets


@pytest.mark.parametrize('mode',['late-tail','tool','foreign-reply','owner-eof','overflow','deadline'])
def test_actual_linux_guest_loop_drains_eof_relays_tools_and_keeps_original_deadline(mode):
    import ast,json,struct,subprocess,time
    from types import SimpleNamespace
    class Pipe:
        def __init__(self,fd,data=()):self.fd=fd;self.data=list(data);self.closed=False
        def fileno(self):return self.fd
        def close(self):self.closed=True
    stdin=Pipe(91);out=Pipe(92,[b'x'*8193] if mode=='overflow' else [b'first ',b'late tail',b'']);err=Pipe(93,[b'',])
    input_pipe=Pipe(90)
    child=SimpleNamespace(stdin=input_pipe,stdout=out,stderr=err,returncode=0,terminated=False)
    child.poll=lambda:None if mode in {'deadline','owner-eof'} else 0
    def terminate():child.terminated=True
    child.terminate=terminate;child.wait=lambda timeout:0;child.kill=lambda:None
    binding={'identity':IDENTITY,'nonce':'a'*48,'boot_id':'01234567-0123-0123-0123-0123456789ab','container_id':'c'*64,
             'image_digest':'sha256:'+'b'*64,'sequence':1}
    owner_request={'jsonrpc':'2.0','id':1,'method':'tools/list'}
    class Peer:
        closed=False;reads=[(json.dumps(owner_request)+'\n').encode(),b''];sent=[]
        def getsockopt(self,*args):return struct.pack('3i',7,1001,1001)
        def setblocking(self,*args):pass
        def settimeout(self,*args):pass
        def recv(self,n):return self.reads.pop(0)
        def sendall(self,data):self.sent.append(json.loads(data))
        def close(self):self.closed=True
    peer=Peer()
    class Listener:
        accepted=False;closed=False
        def bind(self,path):assert path=='/tmp/curis-agent-work/owner-mcp.sock'
        def listen(self,n):assert n==1
        def setblocking(self,*args):pass
        def accept(self):self.accepted=True;return peer,None
        def close(self):self.closed=True
    listener=Listener();emitted=[]
    def select_ready(readers,writers,exceptional,seconds):
        if mode=='owner-eof':return [stdin],[],[]
        if mode in {'tool','foreign-reply'}:
            if not listener.accepted:return [listener],[],[]
        return [x for x in readers if x in (out,err,peer)],[],[]
    def read_frame(seconds):
        assert seconds>0
        reply={k:v for k,v in binding.items() if k!='sequence'}
        value={**reply,'sequence':1,'response':{'jsonrpc':'2.0','id':1,'result':{'tools':[]}}}
        if mode=='foreign-reply':value['nonce']='f'*48
        return {**reply,'sequence':2,'action':'tool_response','arguments':value}
    ticks=[0]
    def monotonic():ticks[0]+=.6;return ticks[0]
    namespace={'json':json,'struct':struct,'WORK':'/tmp/curis-agent-work','sys':SimpleNamespace(stdin=stdin),
        'time':SimpleNamespace(monotonic=monotonic) if mode=='deadline' else time,
        'socket':SimpleNamespace(AF_UNIX=1,SOCK_STREAM=1,SOL_SOCKET=1,SO_PEERCRED=17,socket=lambda *a:listener),
        'select':SimpleNamespace(select=select_ready),'os':SimpleNamespace(chmod=lambda *a:None,geteuid=lambda:1001,set_blocking=lambda *a:None,
            read=lambda fd,n:({92:out,93:err}[fd]).data.pop(0)),
        'subprocess':SimpleNamespace(Popen=lambda *a,**k:child,PIPE=subprocess.PIPE,TimeoutExpired=subprocess.TimeoutExpired),
        'codex_argv':lambda:['/opt/curis/bin/codex','exec'],'emit':lambda b,r:emitted.append((b,r)),
        'read_frame':read_frame,'bound':lambda frame,seq,action:{k:v for k,v in frame.items() if k not in {'action','arguments'}}}
    tree=ast.parse(host._AGENT_CODEX_SOURCE);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_codex')
    exec(compile(ast.Module(body=[function],type_ignores=[]),'actual-linux-guest-loop','exec'),namespace)
    if mode in {'late-tail','tool'}:
        last,result=namespace['run_codex']({'sequence':1},binding,{'input':'','timeout':2},{})
        assert result['stdout']=='first late tail' and result['stderr']=='' and result['reason']=='completed'
        if mode=='tool':assert last['sequence']==2 and len(emitted)==1 and peer.sent[0]['id']==1
    else:
        with pytest.raises((PermissionError,ValueError,EOFError,TimeoutError)):
            namespace['run_codex']({'sequence':1},binding,{'input':'','timeout':1},{})
    assert listener.closed and input_pipe.closed and out.closed and err.closed
    if mode in {'deadline','owner-eof'}:assert child.terminated


@pytest.mark.parametrize('mode',['approved','denied','foreign-binding','late-stop','bad-url','failed-login'])
def test_host_device_login_exchange_is_bound_transient_and_never_reserves_a_model(mode):
    import time
    session=host._OwnedAgentContainerSession(IDENTITY)
    session.owner.nonce='a'*48;session.owner.boot_id='01234567-0123-0123-0123-0123456789ab';session.owner.container_id='c'*64
    calls=[];challenge={'verification_url':'https://auth.openai.com/codex/device','user_code':'ABCD-1234'}
    def callback(value):
        assert value==challenge;calls.append('display')
        if mode=='late-stop':session.revoke('eof')
        return mode!='denied'
    session._linux_on_login=callback
    class Channel:
        def request(self,frame):
            calls.append(frame['action']);binding={k:v for k,v in frame.items() if k not in {'action','arguments'}}
            if mode=='foreign-binding':binding['nonce']='f'*48
            if frame['action']=='authenticate':
                if mode=='failed-login':return {**binding,'result':{'authenticated':False}}
                value=dict(challenge)
                if mode=='bad-url':value['verification_url']='https://evil.example/device'
                return {**binding,'result':{'device_login':value}}
            assert frame['action']=='login_ack' and set(frame['arguments'])=={'continue'}
            return {**binding,'result':{'authenticated':frame['arguments']['continue']}}
    if mode=='approved':assert session._authenticate_linux(Channel(),time.monotonic()+2)==3
    else:
        with pytest.raises(host.OwnedAgentContainerError):session._authenticate_linux(Channel(),time.monotonic()+2)
    if mode in {'foreign-binding','bad-url','failed-login'}:assert 'display' not in calls
    if mode=='late-stop':assert 'login_ack' not in calls


@pytest.mark.parametrize('mode',['approved','denied','wrong-url','owner-eof','deadline','overflow'])
def test_actual_guest_device_flow_only_emits_fixed_challenge_and_obeys_original_deadline(mode):
    import ast,json,re,time,subprocess
    from types import SimpleNamespace
    class Pipe:
        closed=False
        data=[(b'Welcome\nhttps://auth.openai.com/codex/device\n\x1b[94mABCD-1234\x1b[0m\nFAKE-TOKEN-DO-NOT-EMIT\n'
            if mode!='wrong-url' else b'https://evil.example/device\nABCD-1234\n'),b'']
        def fileno(self):return 90
        def close(self):self.closed=True
    pipe=Pipe();stdin=object();child=SimpleNamespace(stdout=pipe,returncode=0,terminated=False)
    if mode=='overflow':pipe.data=[b'x'*8193]
    child.poll=lambda:None if mode in {'owner-eof','deadline'} else 0
    def terminate():child.terminated=True
    child.terminate=terminate;child.wait=lambda timeout:0;child.kill=lambda:None
    emitted=[];calls=[]
    def popen(argv,**options):
        assert argv==['/opt/curis/bin/codex','-c','cli_auth_credentials_store="file"','login','--device-auth']
        assert options['close_fds'] and options['env']=={'HOME':'/tmp/curis-agent-home'}
        return child
    def run(argv,**options):
        assert argv==['/opt/curis/bin/codex','-c','cli_auth_credentials_store="file"','login','status'];calls.append('local-status')
        return SimpleNamespace(returncode=0)
    def reply(seconds):return {'sequence':2,'action':'login_ack','arguments':{'continue':mode!='denied'}}
    ticks=[0]
    def clock():ticks[0]+=1;return ticks[0]
    namespace={'json':json,'re':re,'WORK':'/tmp/curis-agent-work','BINARY':'/opt/curis/bin/codex',
        'time':SimpleNamespace(monotonic=clock) if mode=='deadline' else time,
        'sys':SimpleNamespace(stdin=stdin),'os':SimpleNamespace(set_blocking=lambda *a:None,read=lambda *a:pipe.data.pop(0)),
        'select':SimpleNamespace(select=lambda r,w,x,t:([stdin] if mode=='owner-eof' else [pipe],[],[])),
        'subprocess':SimpleNamespace(Popen=popen,run=run,PIPE=subprocess.PIPE,STDOUT=subprocess.STDOUT,DEVNULL=subprocess.DEVNULL,TimeoutExpired=subprocess.TimeoutExpired),
        'emit':lambda binding,result:emitted.append(result),'read_frame':reply,
        'bound':lambda frame,seq,action:{'sequence':seq}}
    tree=ast.parse(host._AGENT_CODEX_SOURCE);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='authenticate_device')
    exec(compile(ast.Module(body=[function],type_ignores=[]),'actual-device-auth-flow','exec'),namespace)
    if mode in {'owner-eof','deadline','overflow'}:
        with pytest.raises((EOFError,TimeoutError,ValueError)):
            namespace['authenticate_device']({'sequence':1},{'sequence':1},{'timeout':1},{'HOME':'/tmp/curis-agent-home'})
    else:
        binding,authenticated=namespace['authenticate_device']({'sequence':1},{'sequence':1},{'timeout':2},{'HOME':'/tmp/curis-agent-home'})
        assert authenticated is (mode=='approved')
        if mode!='wrong-url':assert emitted==[{'device_login':{'verification_url':'https://auth.openai.com/codex/device','user_code':'ABCD-1234'}}]
        else:assert emitted==[]
    assert 'FAKE-TOKEN-DO-NOT-EMIT' not in json.dumps(emitted)
    assert pipe.closed
    if mode in {'owner-eof','deadline'}:assert child.terminated


@pytest.mark.parametrize('change',[None,'missing','image','binary','guest','purpose','auth-owner','authorization'])
def test_linux_runtime_profile_requires_existing_pinned_lock_and_independent_auth_owner(monkeypatch,change):
    import hashlib
    import app.agent_adapter as adapter
    import app.agent_browser_runtime as runtime
    monkeypatch.setattr(adapter,'CODEX_STOP_VERIFIED',True)
    monkeypatch.setattr(adapter,'AGENT_CONTAINER_EXECUTION_VERIFIED',True)
    profile={'imageDigest':'sha256:'+'a'*64,'binarySha256':'57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1',
        'guestSha256':hashlib.sha256(host._AGENT_CODEX_SOURCE.encode()).hexdigest(),'modelCatalog':linux_catalog_fixture(),
        'egressPurpose':'CODEX_PROVIDER_CONNECT_V1','authenticationOwner':'CURIS_KEYCHAIN_TMPFS_AUTH_V1','complete':True,'executionAuthorized':True}
    if change:
        if change=='missing':profile=None
        else:profile[{'image':'imageDigest','binary':'binarySha256','guest':'guestSha256','purpose':'egressPurpose',
             'auth-owner':'authenticationOwner','authorization':'executionAuthorized'}[change]]='invalid'
    monkeypatch.setattr(runtime,'load_trusted_reader_lock',lambda:{'linuxCodex':profile})
    if change:
        with pytest.raises(adapter.AgentExecutionError):host.load_owned_linux_profile()
    else:assert host.load_owned_linux_profile()['imageDigest']=='sha256:'+'a'*64


@pytest.mark.parametrize('failure',[None,'owner-eof','wrong-sequence','rejected','deadline'])
def test_guest_cache_roundtrip_requires_original_ack_and_scrubs_only_terminal_result(failure):
    import ast, json, time
    from types import SimpleNamespace
    previous=json.dumps({'tokens':{'access_token':'SYNTHETIC-OLD'}})
    current=json.dumps({'tokens':{'refresh_token':'SYNTHETIC-NEW'}})
    emitted=[]
    def read(seconds):
        assert seconds>0
        if failure=='owner-eof':raise EOFError('synthetic closed pipe')
        return {'sequence':5 if failure=='wrong-sequence' else 4,'action':'auth_saved','arguments':{'accepted':failure!='rejected'}}
    def bound(frame,sequence,action):
        assert frame['sequence']==sequence and frame['action']==action
        return {'sequence':sequence}
    namespace={'MANAGED_AUTH':True,'PREVIOUS_AUTH_CACHE':previous,'read_owned_auth_cache':lambda:current,
        'json':json,'time':time,'emit':lambda binding,result:emitted.append(result),'read_frame':read,'bound':bound}
    function=next(n for n in ast.parse(host._AGENT_CODEX_SOURCE).body if isinstance(n,ast.FunctionDef) and n.name=='return_owned_auth')
    exec(compile(ast.Module(body=[function],type_ignores=[]),'guest-auth-writeback','exec'),namespace)
    args=({'sequence':3},{'reason':'completed','returncode':0,'stdout':'SYNTHETIC-OLD / SYNTHETIC-NEW','stderr':'SYNTHETIC-NEW'},time.monotonic()+(-1 if failure=='deadline' else 2))
    if failure:
        with pytest.raises((EOFError,AssertionError,TimeoutError)):namespace['return_owned_auth'](*args)
    else:
        binding,result=namespace['return_owned_auth'](*args)
        assert binding=={'sequence':4} and 'SYNTHETIC' not in result['stdout']+result['stderr']
        assert emitted==[{'auth_writeback':{'cache':current,'authenticated':True}}]
    assert len(emitted)==(0 if failure=='deadline' else 1)


@pytest.mark.parametrize('change',[None,'symlink','uid','hardlink','mode','oversize','empty'])
def test_guest_reads_cache_only_from_private_owned_regular_0600_file(change):
    import ast,os,stat
    from types import SimpleNamespace
    calls=[]
    def opened(path,flags):
        assert path=='/tmp/curis-agent-home/.codex/auth.json'
        assert flags==os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK
        calls.append('open');return 90
    info=SimpleNamespace(st_mode=(stat.S_IFLNK if change=='symlink' else stat.S_IFREG)|(0o644 if change=='mode' else 0o600),
        st_uid=0 if change=='uid' else 1001,st_nlink=2 if change=='hardlink' else 1,st_size=32769 if change=='oversize' else 0 if change=='empty' else 2)
    namespace={'HOME':'/tmp/curis-agent-home','stat':stat,'os':SimpleNamespace(open=opened,fstat=lambda fd:info,
        read=lambda fd,size:b'{}',close=lambda fd:calls.append('close'),O_RDONLY=os.O_RDONLY,O_NOFOLLOW=os.O_NOFOLLOW,O_NONBLOCK=os.O_NONBLOCK)}
    function=next(n for n in ast.parse(host._AGENT_CODEX_SOURCE).body if isinstance(n,ast.FunctionDef) and n.name=='read_owned_auth_cache')
    exec(compile(ast.Module(body=[function],type_ignores=[]),'guest-owned-cache-read','exec'),namespace)
    if change:
        with pytest.raises(AssertionError):namespace['read_owned_auth_cache']()
    else:assert namespace['read_owned_auth_cache']()=='{}'
    assert calls==['open','close']


def test_guest_restore_creates_only_private_tmpfs_cache_with_exclusive_nofollow_0600():
    import ast,os,json
    from types import SimpleNamespace
    calls=[];cache=json.dumps({'auth_mode':'chatgpt','tokens':{'access_token':'SYNTHETIC'}})
    def opened(path,flags,mode):
        assert path=='/tmp/curis-agent-home/.codex/auth.json'
        assert flags==os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW and mode==0o600
        calls.append('open');return 90
    namespace={'MANAGED_AUTH':True,'HOME':'/tmp/curis-agent-home','PREVIOUS_AUTH_CACHE':cache,'json':json,
        'os':SimpleNamespace(umask=lambda mode:calls.append(('umask',mode)),mkdir=lambda path,mode:calls.append(('mkdir',path,mode)),
            open=opened,write=lambda fd,data:len(data),fsync=lambda fd:None,close=lambda fd:calls.append('close'),
            O_WRONLY=os.O_WRONLY,O_CREAT=os.O_CREAT,O_EXCL=os.O_EXCL,O_NOFOLLOW=os.O_NOFOLLOW)}
    node=next(n for n in ast.parse(host._AGENT_CODEX_SOURCE).body if isinstance(n,ast.If) and any(isinstance(v,ast.Call) and isinstance(v.func,ast.Attribute) and v.func.attr=='umask' for v in ast.walk(n)))
    exec(compile(ast.Module(body=[node],type_ignores=[]),'guest-owned-cache-restore','exec'),namespace)
    assert calls==[('umask',0o077),('mkdir','/tmp/curis-agent-home/.codex',0o700),'open','close']
