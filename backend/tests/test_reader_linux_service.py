import pytest

from app import reader_linux_service as service


def test_missing_platform_verifier_fails_closed():
    with pytest.raises(PermissionError):
        service._open_verified_environment({}, {}, "", {})


def test_service_rejects_unapproved_image_before_opening_environment(monkeypatch):
    monkeypatch.setattr(service, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:approved"})
    monkeypatch.setattr(service, "_open_verified_environment", lambda *_: pytest.fail("must not open"))
    runtime = {"complete": True, "executionAuthorized": True, "image_digest": "sha256:other"}
    with pytest.raises(PermissionError):
        service.serve_linux_reader({}, "", runtime, None, 1, 2)


def test_service_checks_environment_before_guest(monkeypatch):
    monkeypatch.setattr(service, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:approved"})
    monkeypatch.setattr(service, "_open_verified_environment", lambda *_: type("Env", (), {"verify": lambda self: False})())
    runtime = {"complete": True, "executionAuthorized": True, "image_digest": "sha256:approved"}
    with pytest.raises(PermissionError):
        service.serve_linux_reader({}, "", runtime, None, 1, 2)


def test_service_forwards_handoff_only_to_reader(monkeypatch):
    identity = {"tenant_id": "t", "company_id": "c", "work_ref": "w", "task_id": "t1",
                "employee_id": "e", "binding_ref": "b"}
    runtime = {"complete": True, "executionAuthorized": True, "boot_id": "boot",
               "container_id": "container", "image_digest": "sha256:approved"}
    monkeypatch.setattr(service, "load_trusted_reader_lock", lambda: {"browserImageDigest": "sha256:approved"})
    monkeypatch.setattr(service, "_open_verified_environment", lambda *_: type("Env", (), {"verify": lambda self: True})())
    seen = []
    monkeypatch.setattr(service, "serve_reader", lambda *args, **kwargs: seen.append(kwargs["handoff"]))
    receipt = bytearray(1)
    service.serve_linux_reader(identity, "a" * 48, runtime, object(), 9001, 9002, handoff=receipt)
    assert seen == [receipt] and receipt == b"\x00"
