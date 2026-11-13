import pytest

from app import reader_vsock_egress as egress

IDENTITY = {"tenant_id": "tenant", "company_id": "company", "work_ref": "work",
            "task_id": "task", "employee_id": "employee", "binding_ref": "binding"}
NONCE = "a" * 48
RUNTIME = {"complete": True, "executionAuthorized": True, "boot_id": "boot",
           "container_id": "container", "image_digest": "sha256:fixture"}


def proxy_fixture(policy):
    import threading
    # No proxy constructor, listener, socket, TLS, or DNS is started.
    proxy = object.__new__(egress.PublicReadProxy)
    proxy.policy = policy
    proxy.permits = threading.BoundedSemaphore(8)
    proxy.serve = lambda stream: ("handled", stream)
    return proxy


class Owner:
    def __init__(self):
        self.events = []
    def dispatch_authenticated(self, identity, nonce, stream, handler):
        self.events.append(("dispatch", identity, nonce, stream))
        return handler(stream)
    def revoke_and_stop(self, identity, nonce):
        self.events.append(("stop_requested", identity, nonce))


def test_platform_factory_is_closed():
    with pytest.raises(PermissionError):
        egress._open_verified_egress(IDENTITY, NONCE, RUNTIME, object(), {})


def test_invalid_identity_and_runtime_fail_before_platform(monkeypatch):
    monkeypatch.setattr(egress, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:fixture"})
    monkeypatch.setattr(egress, "_open_verified_egress", lambda *_: pytest.fail("must remain closed"))
    with pytest.raises(ValueError):
        egress.open_work_egress(IDENTITY, "invalid", RUNTIME, object())
    with pytest.raises(PermissionError):
        egress.open_work_egress(IDENTITY, NONCE, {**RUNTIME, "image_digest": "other"}, object())
    with pytest.raises(PermissionError):
        egress.open_work_egress(IDENTITY, NONCE, {**RUNTIME, "extra": []}, object())


def test_rejected_proxy_reports_unknown_without_closing_unproven_object(monkeypatch):
    monkeypatch.setattr(egress, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:fixture"})
    owner = Owner()
    monkeypatch.setattr(egress, "_open_verified_egress", lambda *_: (owner, object()))
    with pytest.raises(ValueError) as error:
        egress.open_work_egress(IDENTITY, NONCE, RUNTIME, object())
    assert any("UNKNOWN" in note for note in error.value.__notes__)
    assert owner.events == []


def test_work_identity_and_runtime_are_snapshotted_before_factory(monkeypatch):
    import threading
    monkeypatch.setattr(egress, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:fixture"})
    identity, runtime, policy, owner = dict(IDENTITY), dict(RUNTIME), object(), Owner()
    entered, release, results = threading.Event(), threading.Event(), []
    def factory(given_identity, nonce, given_runtime, given_policy, lock):
        entered.set()
        if not release.wait(2):
            raise TimeoutError("test did not release factory")
        assert given_identity == IDENTITY and given_runtime == RUNTIME
        return owner, proxy_fixture(policy)
    monkeypatch.setattr(egress, "_open_verified_egress", factory)
    def open_work():
        try:
            results.append(egress.open_work_egress(identity, NONCE, runtime, policy))
        except Exception as error:
            results.append(error)
    thread = threading.Thread(target=open_work)
    thread.start()
    try:
        assert entered.wait(2)
        identity["work_ref"] = "other"
        runtime["boot_id"] = "changed"
    finally:
        release.set()
        thread.join(2)
    assert not thread.is_alive() and len(results) == 1
    work = results[0]
    assert isinstance(work, egress._WorkEgress)
    work.serve(object())
    assert owner.events[0][1] == IDENTITY


def test_only_owner_admits_stream_to_existing_handler():
    policy, owner, stream = object(), Owner(), object()
    work = egress._WorkEgress(IDENTITY, NONCE, owner, proxy_fixture(policy), policy)
    assert work.serve(stream) == ("handled", stream)
    assert owner.events[0] == ("dispatch", IDENTITY, NONCE, stream)
    work.close()
    assert owner.events[-1] == ("stop_requested", IDENTITY, NONCE)
    assert work.stop_state == "UNKNOWN"
    with pytest.raises(PermissionError):
        work.serve(stream)


def test_stop_failure_remains_unknown_and_is_not_blindly_retried():
    policy, owner = object(), Owner()
    def fail(*_):
        raise OSError("stop failed")
    owner.revoke_and_stop = fail
    work = egress._WorkEgress(IDENTITY, NONCE, owner, proxy_fixture(policy), policy)
    with pytest.raises(OSError):
        work.close()
    assert work.stop_state == "UNKNOWN"
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        work.close()


def test_existing_proxy_permit_is_enforced_and_released():
    policy, owner = object(), Owner()
    proxy = proxy_fixture(policy)
    work = egress._WorkEgress(IDENTITY, NONCE, owner, proxy, policy)
    for _ in range(8):
        assert proxy.permits.acquire(blocking=False)
    with pytest.raises(PermissionError, match="limit"):
        work.serve(object())
    for _ in range(8):
        proxy.permits.release()
    def fail(_):
        raise ValueError("handler failure")
    proxy.serve = fail
    with pytest.raises(ValueError, match="handler"):
        work.serve(object())
    for _ in range(8):
        assert proxy.permits.acquire(blocking=False)
    for _ in range(8):
        proxy.permits.release()
