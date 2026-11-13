from __future__ import annotations

import os
from typing import Any

import pytest

from app.ai_capability_registry import AICapabilityRegistry, ProviderConnectIn
from app.credential_vault import (
    CredentialError,
    CredentialStageFailure,
    CredentialWriteNotStarted,
    CredentialVaultService,
    MacOSKeychainCredentialBackend,
)
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.tenant_context import TenantContext


class FakeDurableBackend:
    def __init__(self, values: dict[tuple[str, str], str] | None = None) -> None:
        self.values = values if values is not None else {}

    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        self.values[(tenant_id, credential_id)] = secret

    def resolve(self, tenant_id: str, credential_id: str) -> str:
        try:
            return self.values[(tenant_id, credential_id)]
        except KeyError as error:
            raise CredentialError("test credential not found") from error

    def disable(self, tenant_id: str, credential_id: str) -> None:
        self.delete(tenant_id, credential_id)

    def delete(self, tenant_id: str, credential_id: str) -> None:
        self.values.pop((tenant_id, credential_id), None)

    def test(self, tenant_id: str, credential_id: str) -> bool:
        return bool(self.resolve(tenant_id, credential_id))

    def redact(self, value: Any) -> str:
        text = str(value)
        for secret in self.values.values():
            text = text.replace(secret, "[REDACTED]")
        return text


class UnavailableBackend(FakeDurableBackend):
    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        raise CredentialError("test keychain unavailable")


def make_vault(tmp_path, backend, *, tenant_id: str = "tenant-a"):
    database = Database(str(tmp_path / f"{tenant_id}.sqlite"))
    database.initialize()
    event_log = EvolutionEventLog(database)
    vault = CredentialVaultService(
        database,
        event_log,
        environment="local",
        vault_backend=backend,
        backend_mode="macos-keychain",
    )
    return database, vault


def test_keychain_vault_survives_service_recreation_and_keeps_provider_scope(tmp_path):
    durable: dict[tuple[str, str], str] = {}
    backend = FakeDurableBackend(durable)
    database, first = make_vault(tmp_path, backend)

    with TenantContext.scope("tenant-a"):
        created = first.create(
            name="DeepSeek key",
            provider="deepseek",
            credential_type="api_key",
            secret="test-v1-p0-003-first",
        )
        assert created["credential_ref"].startswith("vault://tenant/tenant-a/credential/")
        assert created["storage"] == "macos_keychain"
        assert "secret" not in created

        restarted = CredentialVaultService(
            database,
            EvolutionEventLog(database),
            environment="local",
            vault_backend=FakeDurableBackend(durable),
            backend_mode="macos-keychain",
        )
        assert restarted.resolve(created["credential_ref"], provider="deepseek")["secret"] == "test-v1-p0-003-first"
        with pytest.raises(CredentialError, match="provider does not match"):
            restarted.resolve(created["credential_ref"], provider="openai")

        restarted.update(created["credential_id"], secret="test-v1-p0-003-second")
        assert restarted.resolve(created["credential_ref"], provider="deepseek")["secret"] == "test-v1-p0-003-second"
        restarted.delete(created["credential_id"])
        with pytest.raises(CredentialError):
            restarted.resolve(created["credential_ref"], provider="deepseek")


def test_packaged_mode_rejects_memory_fallback(tmp_path, monkeypatch):
    database = Database(str(tmp_path / "packaged.sqlite"))
    database.initialize()
    monkeypatch.setenv("CURIS_PACKAGED_RUNTIME", "1")
    with pytest.raises(CredentialError, match="requires macOS Keychain"):
        CredentialVaultService(
            database,
            EvolutionEventLog(database),
            environment="local",
            backend_mode="local-dev",
        )


def test_keychain_unavailable_leaves_no_credential_metadata(tmp_path):
    database, vault = make_vault(tmp_path, UnavailableBackend())
    with TenantContext.scope("tenant-a"):
        with pytest.raises(CredentialStageFailure) as raised:
            vault.create(
                name="Unavailable",
                provider="deepseek",
                credential_type="api_key",
                secret="test-v1-p0-003-unavailable",
            )
        assert (raised.value.code, raised.value.stage, raised.value.certainty) == ("CREDENTIAL_NATIVE_WRITE_UNCONFIRMED", "native_store", "unknown")
        assert database.list_credential_metadata("tenant-a") == []


def test_provider_health_recovery_uses_same_vault_reference_after_restart(tmp_path):
    durable: dict[tuple[str, str], str] = {}
    database, vault = make_vault(tmp_path, FakeDurableBackend(durable))
    calls: list[tuple[str, dict[str, str]]] = []

    def provider_get(url: str, headers: dict[str, str], timeout: int):
        calls.append((url, headers))
        assert timeout == 15
        return {"data": [{"id": "deepseek-chat"}]}

    with TenantContext.scope("tenant-a"):
        credential = vault.create(
            name="DeepSeek key",
            provider="deepseek",
            credential_type="api_key",
            secret="test-v1-p0-003-provider",
        )
        service = AICapabilityRegistry(database, vault, http_get=provider_get)
        connected = service.connect(
            "deepseek",
            ProviderConnectIn(credential_ref=credential["credential_ref"], save=True),
        )
        assert connected["health"] == "healthy"

        restarted_vault = CredentialVaultService(
            database,
            EvolutionEventLog(database),
            environment="local",
            vault_backend=FakeDurableBackend(durable),
            backend_mode="macos-keychain",
        )
        recovered = AICapabilityRegistry(
            database, restarted_vault, http_get=provider_get
        ).recover("deepseek")
        assert recovered["health"] == "healthy"
        assert len(calls) == 2
        assert all(call[1]["Authorization"] == "Bearer test-v1-p0-003-provider" for call in calls)

        with pytest.raises(CredentialError, match="provider does not match"):
            AICapabilityRegistry(database, restarted_vault, http_get=provider_get).connect(
                "openai",
                ProviderConnectIn(credential_ref=credential["credential_ref"], save=False),
            )
        assert len(calls) == 2


@pytest.mark.skipif(
    os.getenv("CURIS_RUN_NATIVE_KEYCHAIN_TEST") != "1",
    reason="explicit opt-in required for an isolated real macOS Keychain item",
)
def test_real_macos_keychain_round_trip():
    backend = MacOSKeychainCredentialBackend(
        service="com.curis.desktop.credentials.v1.pytest"
    )
    tenant_id = "v1-p0-003-pytest"
    credential_id = "cred-native-roundtrip"
    backend.delete(tenant_id, credential_id)
    try:
        backend.store(tenant_id, credential_id, "test-v1-p0-003-native-first")
        assert backend.resolve(tenant_id, credential_id) == "test-v1-p0-003-native-first"
        backend.store(tenant_id, credential_id, "test-v1-p0-003-native-second")
        assert backend.resolve(tenant_id, credential_id) == "test-v1-p0-003-native-second"
    finally:
        backend.delete(tenant_id, credential_id)
    with pytest.raises(CredentialError, match="not found"):
        backend.resolve(tenant_id, credential_id)


def recovery_native(copy_status=0, default_ref=101, get_status=0, flags=6, add_status=0):
    """Fake native functions only: never initialize or load Security.framework."""
    from ctypes import POINTER, c_void_p, c_uint32, cast
    from types import SimpleNamespace
    calls = []
    releases = []
    def copy_default(out):
        calls.append("default")
        cast(out, POINTER(c_void_p))[0] = default_ref
        return copy_status
    def status(ref, out):
        calls.append("status")
        assert ref.value == default_ref
        cast(out, POINTER(c_uint32))[0] = flags
        return get_status
    def add(ref, service_length, service, account_length, account, length, data, item):
        calls.append("add")
        assert ref is None and service_length == len(service) and account_length == len(account)
        assert service == b"com.curis.desktop.credentials.v1"
        assert account.startswith(b"tenant-") and b":credential-" in account
        assert length > 0
        if add_status == 0:
            cast(item, POINTER(c_void_p))[0] = 202
        return add_status
    backend = MacOSKeychainCredentialBackend.__new__(MacOSKeychainCredentialBackend)
    backend.service = MacOSKeychainCredentialBackend.SERVICE.encode()
    backend._known_secrets = set()
    backend._security = SimpleNamespace(SecKeychainCopyDefault=copy_default, SecKeychainGetStatus=status, SecKeychainAddGenericPassword=add)
    backend._core_foundation = SimpleNamespace(CFRelease=lambda item: releases.append(item.value))
    return backend, calls, releases


@pytest.mark.parametrize("options, expected_calls, released", [
    ({"copy_status": -25307}, ["default"], [101]),
    ({"default_ref": None}, ["default"], []),
    ({"get_status": -25291}, ["default", "status"], [101]),
    ({"flags": 2}, ["default", "status"], [101]),
    ({"flags": 0}, ["default", "status"], [101]),
])
def test_recovery_preflight_failure_never_adds(options, expected_calls, released):
    backend, calls, releases = recovery_native(**options)
    with pytest.raises(CredentialWriteNotStarted) as raised:
        backend.store("tenant-recovery", "cred-fixture", "synthetic-recovery-secret")
    assert (raised.value.code, raised.value.stage, raised.value.certainty) == ("CREDENTIAL_WRITE_NOT_STARTED", "preflight", "not_started")
    assert calls == expected_calls and releases == released
    assert backend._known_secrets == set()


@pytest.mark.parametrize("add_status", [0, -128, -25291, -25308])
def test_recovery_store_keeps_native_error_phase_and_parameter_shape(add_status):
    backend, calls, releases = recovery_native(add_status=add_status)
    if add_status:
        with pytest.raises(CredentialStageFailure) as raised:
            backend.store("tenant-recovery", "cred-fixture", "synthetic-recovery-secret")
        assert (raised.value.code, raised.value.stage, raised.value.certainty, raised.value.os_status) == ("CREDENTIAL_NATIVE_WRITE_UNCONFIRMED", "native_store", "unknown", add_status)
        assert "synthetic-recovery-secret" not in str(raised.value)
        assert "OSStatus" not in str(raised.value)
    else:
        backend.store("tenant-recovery", "cred-fixture", "synthetic-recovery-secret")
    assert calls == ["default", "status", "add"]
    assert releases == ([101, 202] if add_status == 0 else [101])


@pytest.mark.parametrize("method, native_status, expected_http", [("POST", -128, 422), ("PUT", -128, 404), ("POST", -25307, 422), ("PUT", -25307, 404)])
def test_recovery_real_credential_endpoint_preserves_safe_detail(tmp_path, monkeypatch, method, native_status, expected_http):
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from fastapi.testclient import TestClient
    path = tmp_path / "endpoint.sqlite"
    for name in ["CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"]:
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    from app.main import create_app
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, "technical-company", "ceo", "ceo", "active", request_id))
    native, calls, _ = recovery_native(copy_status=native_status if native_status == -25307 else 0, add_status=native_status if native_status == -128 else 0)
    monkeypatch.setattr(MacOSKeychainCredentialBackend, "__init__", lambda self, **kwargs: self.__dict__.update(native.__dict__))
    monkeypatch.setenv("CURIS_CREDENTIAL_BACKEND", "macos-keychain")
    database = Database(str(path))
    database.initialize()
    credential_id = "cred-00000000-0000-0000-0000-000000000001"
    if method == "PUT":
        database.save_credential_metadata(credential_id=credential_id, tenant_id="tenant-recovery", name="Technical credential", provider="deepseek", credential_type="api_key", credential_ref=f"vault://tenant/tenant-recovery/credential/{credential_id}", status="active", encrypted_metadata={})
    with TestClient(create_app(str(path))) as client:
        url = "/api/workspace/credentials" + ("/" + credential_id if method == "PUT" else "")
        result = client.request(method, url, headers={"X-Tenant-Id": "tenant-recovery", "X-Ceo-Id": "ceo"}, json={"name": "Technical credential", "provider": "deepseek", "credential_type": "api_key", "secret": "synthetic-recovery-secret"})
        assert result.status_code == expected_http, result.text
        assert result.json()["os_status"] == native_status
        assert result.json()["code"] == ("CREDENTIAL_WRITE_NOT_STARTED" if native_status == -25307 else "CREDENTIAL_NATIVE_WRITE_UNCONFIRMED")
        assert result.json()["stage"] == ("preflight" if native_status == -25307 else "native_store")
        assert result.json()["certainty"] == ("not_started" if native_status == -25307 else "unknown")
        assert "synthetic-recovery-secret" not in result.text
    assert calls == (["default"] if native_status == -25307 else ["default", "status", "add"])
    assert len(database.list_credential_metadata("tenant-recovery")) == (1 if method == "PUT" else 0)


def test_recovery_validation_rejection_has_code_without_native_add(tmp_path, monkeypatch):
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from fastapi.testclient import TestClient
    path = tmp_path / "validation.sqlite"
    for name in ["CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"]:
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    from app.main import create_app
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, "technical-company", "ceo", "ceo", "active", request_id))
    native, calls, _ = recovery_native()
    monkeypatch.setattr(MacOSKeychainCredentialBackend, "__init__", lambda self, **kwargs: self.__dict__.update(native.__dict__))
    monkeypatch.setenv("CURIS_CREDENTIAL_BACKEND", "macos-keychain")
    with TestClient(create_app(str(path))) as client:
        result = client.post("/api/workspace/credentials", headers={"X-Tenant-Id": "tenant-recovery", "X-Ceo-Id": "ceo"}, json={"name": "Technical credential", "provider": "deepseek", "credential_type": "api_key", "secret": "api_key:synthetic-secret"})
        assert result.status_code == 422
        assert result.json()["code"] == "CREDENTIAL_WRITE_NOT_STARTED"
        assert (result.json()["stage"], result.json()["certainty"]) == ("validation", "not_started")
        assert "synthetic-secret" not in result.text
    assert calls == []


def test_recovery_metadata_failure_after_native_success_does_not_claim_no_store(tmp_path, monkeypatch):
    native, calls, _ = recovery_native()
    database, vault = make_vault(tmp_path, native, tenant_id="tenant-recovery")
    def fail_metadata(**kwargs):
        raise RuntimeError("Technical metadata commit failure")
    monkeypatch.setattr(database, "save_credential_metadata", fail_metadata)
    deleted = []
    monkeypatch.setattr(native, "delete", lambda tenant, credential: deleted.append(credential))
    with TenantContext.scope("tenant-recovery"), pytest.raises(CredentialStageFailure) as raised:
        vault.create(name="Technical credential", provider="deepseek", credential_type="api_key", secret="synthetic-recovery-secret")
    assert (raised.value.code, raised.value.stage, raised.value.certainty) == ("CREDENTIAL_METADATA_UNCONFIRMED", "metadata", "native_returned_success")
    assert calls == ["default", "status", "add"] and len(deleted) == 1
    assert database.list_credential_metadata("tenant-recovery") == []


def test_stage_audit_failure_reports_committed_metadata_without_secret(tmp_path, monkeypatch):
    backend = FakeDurableBackend()
    database, vault = make_vault(tmp_path, backend, tenant_id="tenant-recovery")
    def fail_audit(*args, **kwargs):
        raise RuntimeError("synthetic-audit-secret")
    monkeypatch.setattr(vault, "_audit", fail_audit)
    with TenantContext.scope("tenant-recovery"), pytest.raises(CredentialStageFailure) as raised:
        vault.create(name="Technical credential", provider="deepseek", credential_type="api_key", secret="synthetic-recovery-secret")
    assert (raised.value.code, raised.value.stage, raised.value.certainty) == ("CREDENTIAL_AUDIT_FAILED", "audit", "metadata_returned_success")
    assert "secret" not in str(raised.value)
    assert len(database.list_credential_metadata("tenant-recovery")) == 1


@pytest.mark.parametrize("failed_stage, expected_code, expected_certainty", [
    ("metadata", "CREDENTIAL_METADATA_UNCONFIRMED", "native_returned_success"),
    ("audit", "CREDENTIAL_AUDIT_FAILED", "metadata_returned_success"),
])
def test_stage_route_returns_only_fixed_failure_fields(tmp_path, monkeypatch, failed_stage, expected_code, expected_certainty):
    from app.identity_membership import IdentityMembership, AuthorizedMembership
    from fastapi.testclient import TestClient
    path = tmp_path / "stage-route.sqlite"
    for name in ["CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"]:
        monkeypatch.setenv(name, str(path))
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "0")
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    from app.main import create_app
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request_id: AuthorizedMembership("technical-owner", tenant, "technical-company", "ceo", "ceo", "active", request_id))
    native, calls, _ = recovery_native()
    monkeypatch.setattr(MacOSKeychainCredentialBackend, "__init__", lambda self, **kwargs: self.__dict__.update(native.__dict__))
    monkeypatch.setenv("CURIS_CREDENTIAL_BACKEND", "macos-keychain")
    with TestClient(create_app(str(path))) as client:
        if failed_stage == "metadata":
            def fail_metadata(self, **kwargs):
                raise RuntimeError("SENTINEL_PRIVATE_DETAIL")
            monkeypatch.setattr(Database, "save_credential_metadata", fail_metadata)
            monkeypatch.setattr(MacOSKeychainCredentialBackend, "delete", lambda self, tenant, credential: None)
        else:
            original = EvolutionEventLog.record
            def fail_audit(self, **kwargs):
                if kwargs.get("event_type") == "credential.created":
                    raise RuntimeError("SENTINEL_PRIVATE_DETAIL")
                return original(self, **kwargs)
            monkeypatch.setattr(EvolutionEventLog, "record", fail_audit)
        result = client.post("/api/workspace/credentials", headers={"X-Tenant-Id": "tenant-recovery", "X-Ceo-Id": "ceo"}, json={"name": "Technical credential", "provider": "deepseek", "credential_type": "api_key", "secret": "synthetic-recovery-secret"})
        assert result.status_code == 500
        assert result.json() == {"detail": "Credential save did not complete.", "code": expected_code, "stage": failed_stage, "certainty": expected_certainty}
        assert "SENTINEL_PRIVATE_DETAIL" not in result.text and "synthetic-recovery-secret" not in result.text
    assert calls == ["default", "status", "add"]
