import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[2] / "desktop/runtime/reader_guest_supervisor.py"
spec = importlib.util.spec_from_file_location("reader_guest_supervisor", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

IDENTITY = {"tenant_id": "t", "company_id": "c", "work_ref": "w", "task_id": "t1",
            "employee_id": "e", "binding_ref": "b"}
NONCE = "a" * 48
RUNTIME = {"complete": True, "executionAuthorized": True, "boot_id": "boot",
           "container_id": "container", "image_digest": "sha256:fixture"}


class Owner:
    def __init__(self):
        self.events = []
    def serve_if_active(self, identity, nonce, runtime, bridge, service):
        self.events.append(("serve", identity, nonce, runtime, bridge, service))
        return "fixture"
    def revoke_and_stop(self, identity, nonce):
        self.events.append(("stop", identity, nonce))


def test_real_guest_factory_is_closed():
    with pytest.raises(PermissionError):
        module.open_guest_supervisor(IDENTITY, NONCE, RUNTIME)


def test_wrong_work_or_runtime_fails_before_factory(monkeypatch):
    monkeypatch.setattr(module, "_open_verified_guest_owner", lambda *_: pytest.fail("factory called"))
    with pytest.raises(ValueError):
        module.open_guest_supervisor(IDENTITY, "bad", RUNTIME)
    with pytest.raises(PermissionError):
        module.open_guest_supervisor(IDENTITY, NONCE, {**RUNTIME, "extra": []})


def test_verified_factory_loads_fixed_entrypoints(monkeypatch):
    owner, bridge, service = Owner(), lambda: None, lambda: None
    monkeypatch.setattr(module, "_open_verified_guest_owner", lambda *_: owner)
    monkeypatch.setattr(module, "_PipeGuestOwner", lambda platform: platform)
    monkeypatch.setattr(module, "_canonical_entrypoints", lambda: (bridge, service))
    guest = module.open_guest_supervisor(IDENTITY, NONCE, RUNTIME)
    guest.serve()
    assert owner.events[0][-2:] == (bridge, service)


def test_owner_receives_original_snapshot_and_stop():
    identity, runtime, owner = dict(IDENTITY), dict(RUNTIME), Owner()
    bridge, service = lambda: None, lambda: None
    guest = module.GuestSupervisor(identity, NONCE, runtime, owner, bridge, service)
    identity["work_ref"], runtime["boot_id"] = "other", "other"
    assert guest.serve() == "fixture"
    assert owner.events[0] == ("serve", IDENTITY, NONCE, RUNTIME, bridge, service)
    guest.close()
    assert guest.stop_state == "UNKNOWN"
    with pytest.raises(PermissionError):
        guest.serve()


def test_failure_retains_unknown_and_does_not_blind_retry():
    owner = Owner()
    def fail(*_):
        raise OSError("stop failed")
    owner.revoke_and_stop = fail
    guest = module.GuestSupervisor(IDENTITY, NONCE, RUNTIME, owner, lambda: None, lambda: None)
    with pytest.raises(OSError):
        guest.close()
    assert guest.stop_state == "UNKNOWN"
    with pytest.raises(RuntimeError, match="UNKNOWN"):
        guest.close()


def test_blocked_admission_can_be_revoked():
    import threading
    entered, release = threading.Event(), threading.Event()
    class OwnerWithRevocation(Owner):
        revoked = False
        def serve_if_active(self, *args):
            entered.set()
            if not release.wait(2):
                raise TimeoutError("fixture timeout")
            if self.revoked:
                raise PermissionError("revoked")
        def revoke_and_stop(self, identity, nonce):
            self.revoked = True
            super().revoke_and_stop(identity, nonce)
    owner = OwnerWithRevocation()
    guest = module.GuestSupervisor(IDENTITY, NONCE, RUNTIME, owner, lambda: None, lambda: None)
    errors = []
    def serve():
        try:
            guest.serve()
        except Exception as error:
            errors.append(error)
    thread = threading.Thread(target=serve)
    thread.start()
    try:
        assert entered.wait(2)
        guest.close()
    finally:
        release.set()
        thread.join(2)
    assert not thread.is_alive() and len(errors) == 1 and isinstance(errors[0], PermissionError)
    assert guest.stop_state == "UNKNOWN"


def test_concurrent_close_reports_pending():
    import threading
    entered, release = threading.Event(), threading.Event()
    class BlockingOwner(Owner):
        def revoke_and_stop(self, *_):
            entered.set()
            if not release.wait(2):
                raise TimeoutError("fixture timeout")
    guest = module.GuestSupervisor(IDENTITY, NONCE, RUNTIME, BlockingOwner(), lambda: None, lambda: None)
    thread = threading.Thread(target=guest.close)
    thread.start()
    try:
        assert entered.wait(2)
        with pytest.raises(RuntimeError, match="UNKNOWN"):
            guest.close()
    finally:
        release.set()
        thread.join(2)
    assert not thread.is_alive() and guest.stop_state == "UNKNOWN"


def test_serve_and_stop_failure_report_unknown():
    class FailingOwner(Owner):
        def serve_if_active(self, *_):
            raise ValueError("serve failed")
        def revoke_and_stop(self, *_):
            raise OSError("stop failed")
    guest = module.GuestSupervisor(IDENTITY, NONCE, RUNTIME, FailingOwner(), lambda: None, lambda: None)
    with pytest.raises(ValueError, match="serve failed") as error:
        guest.serve()
    assert any("UNKNOWN" in note for note in error.value.__notes__)


def test_ambiguous_thread_start_does_not_close_reader_fds(monkeypatch):
    class Platform:
        def dispatch_if_active(self, identity, nonce, callback): return callback()
        def take_verified_peer(self, *args): return 99
        def policy_for_work(self, identity): return object()
        def is_active(self): return True
        def revoke_and_stop(self, *args): pass
    class MaybeStarted:
        def __init__(self, **kwargs): pass
        def start(self): raise KeyboardInterrupt()
    pairs = iter(((11, 12), (13, 14)))
    closed = []
    monkeypatch.setattr(module.os, "pipe", lambda: next(pairs))
    monkeypatch.setattr(module.os, "close", lambda fd: closed.append(fd))
    monkeypatch.setattr(module.threading, "Thread", MaybeStarted)
    owner = module._PipeGuestOwner(Platform())
    with pytest.raises(KeyboardInterrupt):
        owner.serve_if_active(IDENTITY, NONCE, RUNTIME, lambda *a, **k: None, lambda *a, **k: None)
    assert closed == [12, 13]
    assert ("peer", 99) in owner._unresolved
    assert ("reader", 11, 14) in owner._unresolved


def test_untransferred_peer_retention_does_not_call_platform_cleanup(monkeypatch):
    class Platform:
        def dispatch_if_active(self, identity, nonce, callback): return callback()
        def take_verified_peer(self, *args): return 99
        def policy_for_work(self, identity): return object()
        def is_active(self): return True
        def revoke_and_stop(self, *args): pass
        def retain_untransferred_peer(self, peer): pytest.fail("must not wait on cleanup")
    def fail_pipe(): raise OSError("pipe failed")
    monkeypatch.setattr(module.os, "pipe", fail_pipe)
    owner = module._PipeGuestOwner(Platform())
    with pytest.raises(OSError):
        owner.serve_if_active(IDENTITY, NONCE, RUNTIME, lambda *a, **k: None, lambda *a, **k: None)
    assert owner._unresolved == [("peer", 99)]
