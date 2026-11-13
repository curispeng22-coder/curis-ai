from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import uuid
from ctypes import POINTER, byref, c_char_p, c_int32, c_uint32, c_void_p, cdll, string_at
from ctypes.util import find_library
from datetime import datetime, timezone
from typing import Any, Protocol

from .ceo_context import CeoContext
from .database import Database
from .evolution_event_log import EvolutionEventLog
from .model_gateway import redact_model_gateway_text
from .tenant_context import TenantContext


LOCAL_REF_RE = re.compile(r"^local-dev://tenant/([^/]+)/credential/([^/]+)$")
VAULT_REF_RE = re.compile(r"^(vault|kms)://tenant/([^/]+)/credential/([^/]+)$")
SECRET_FIELD_RE = re.compile(
    r"(api[_-]?key|token|password|secret|credential_value)\s*[:=]",
    re.IGNORECASE,
)
_CODEX_AUTH_TYPE = "codex-managed-auth-v1"


class CredentialError(ValueError):
    pass


class CredentialStageFailure(CredentialError):
    """Fixed, non-secret phase and certainty for a failed save request."""

    def __init__(self, code: str, stage: str, certainty: str, *, os_status: int | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.stage = stage
        self.certainty = certainty
        self.os_status = os_status if type(os_status) is int and -(2**31) <= os_status < 2**31 else None


class CredentialWriteNotStarted(CredentialStageFailure):
    """The current request was rejected before a native credential write."""

    def __init__(self, _reason: str = "", *, stage: str = "validation", os_status: int | None = None) -> None:
        super().__init__("CREDENTIAL_WRITE_NOT_STARTED", stage, "not_started", os_status=os_status)


class CredentialBackend(Protocol):
    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        ...

    def resolve(self, tenant_id: str, credential_id: str) -> str:
        ...

    def disable(self, tenant_id: str, credential_id: str) -> None:
        ...

    def delete(self, tenant_id: str, credential_id: str) -> None:
        ...

    def test(self, tenant_id: str, credential_id: str) -> bool:
        ...

    def redact(self, value: Any) -> str:
        ...


class LocalDevCredentialBackend:
    """Local/demo secret holder.

    Secrets live only inside this app process. The database stores only
    credential metadata plus a digest, never the plaintext secret.
    """

    def __init__(self) -> None:
        self._secrets: dict[tuple[str, str], str] = {}

    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        self._secrets[(tenant_id, credential_id)] = secret

    def resolve(self, tenant_id: str, credential_id: str) -> str:
        try:
            return self._secrets[(tenant_id, credential_id)]
        except KeyError as error:
            raise CredentialError("credential secret is not available in local-dev memory") from error

    def disable(self, tenant_id: str, credential_id: str) -> None:
        self._secrets.pop((tenant_id, credential_id), None)

    def delete(self, tenant_id: str, credential_id: str) -> None:
        self._secrets.pop((tenant_id, credential_id), None)

    def test(self, tenant_id: str, credential_id: str) -> bool:
        return bool(self.resolve(tenant_id, credential_id))

    def redact(self, value: Any) -> str:
        text = str(value)
        for secret in self._secrets.values():
            if secret:
                text = text.replace(secret, "[REDACTED]")
        return redact_model_gateway_text(text)


class UnconfiguredVaultBackend:
    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        raise CredentialError("external credential backend is not configured")

    def resolve(self, tenant_id: str, credential_id: str) -> str:
        raise CredentialError("external credential backend is not configured")

    def disable(self, tenant_id: str, credential_id: str) -> None:
        raise CredentialError("external credential backend is not configured")

    def delete(self, tenant_id: str, credential_id: str) -> None:
        raise CredentialError("external credential backend is not configured")

    def test(self, tenant_id: str, credential_id: str) -> bool:
        raise CredentialError("external credential backend is not configured")

    def redact(self, value: Any) -> str:
        return redact_model_gateway_text(value)


class MacOSKeychainCredentialBackend:
    """Native generic-password storage backed by macOS Security.framework."""

    SERVICE = "com.curis.desktop.credentials.v1"
    _DUPLICATE_ITEM = -25299
    _ITEM_NOT_FOUND = -25300

    def __init__(self, service: str = SERVICE) -> None:
        if sys.platform != "darwin":
            raise CredentialError("macOS Keychain is unavailable on this platform")
        security_path = find_library("Security")
        core_foundation_path = find_library("CoreFoundation")
        if not security_path or not core_foundation_path:
            raise CredentialError("macOS Keychain framework is unavailable")
        self.service = service.encode("utf-8")
        self._security = cdll.LoadLibrary(security_path)
        self._core_foundation = cdll.LoadLibrary(core_foundation_path)
        self._known_secrets: set[str] = set()
        self._configure_native_api()

    def _configure_native_api(self) -> None:
        self._security.SecKeychainCopyDefault.argtypes = [POINTER(c_void_p)]
        self._security.SecKeychainCopyDefault.restype = c_int32
        self._security.SecKeychainGetStatus.argtypes = [c_void_p, POINTER(c_uint32)]
        self._security.SecKeychainGetStatus.restype = c_int32
        self._security.SecKeychainAddGenericPassword.argtypes = [
            c_void_p, c_uint32, c_char_p, c_uint32, c_char_p,
            c_uint32, c_void_p, POINTER(c_void_p),
        ]
        self._security.SecKeychainAddGenericPassword.restype = c_int32
        self._security.SecKeychainFindGenericPassword.argtypes = [
            c_void_p, c_uint32, c_char_p, c_uint32, c_char_p,
            POINTER(c_uint32), POINTER(c_void_p), POINTER(c_void_p),
        ]
        self._security.SecKeychainFindGenericPassword.restype = c_int32
        self._security.SecKeychainItemModifyAttributesAndData.argtypes = [
            c_void_p, c_void_p, c_uint32, c_void_p,
        ]
        self._security.SecKeychainItemModifyAttributesAndData.restype = c_int32
        self._security.SecKeychainItemDelete.argtypes = [c_void_p]
        self._security.SecKeychainItemDelete.restype = c_int32
        self._security.SecKeychainItemFreeContent.argtypes = [c_void_p, c_void_p]
        self._security.SecKeychainItemFreeContent.restype = c_int32
        self._core_foundation.CFRelease.argtypes = [c_void_p]
        self._core_foundation.CFRelease.restype = None

    @staticmethod
    def _account(tenant_id: str, credential_id: str) -> bytes:
        tenant_digest = hashlib.sha256(tenant_id.encode("utf-8")).hexdigest()
        return f"tenant-{tenant_digest}:credential-{credential_id}".encode("utf-8")

    def store(self, tenant_id: str, credential_id: str, secret: str) -> None:
        self._preflight()
        account = self._account(tenant_id, credential_id)
        secret_bytes = secret.encode("utf-8")
        item = c_void_p()
        status = self._security.SecKeychainAddGenericPassword(
            None,
            len(self.service), self.service,
            len(account), account,
            len(secret_bytes), c_char_p(secret_bytes),
            byref(item),
        )
        if status == self._DUPLICATE_ITEM:
            item = self._find_item(account)
            try:
                status = self._security.SecKeychainItemModifyAttributesAndData(
                    item, None, len(secret_bytes), c_char_p(secret_bytes)
                )
            finally:
                self._release(item)
        elif item.value:
            self._release(item)
        self._raise_status(status, "store")
        self._known_secrets.add(secret)

    def _preflight(self) -> None:
        keychain = c_void_p()
        try:
            self._raise_status(self._security.SecKeychainCopyDefault(byref(keychain)), "preflight")
            if not keychain.value:
                raise CredentialWriteNotStarted(stage="preflight")
            flags = c_uint32()
            self._raise_status(self._security.SecKeychainGetStatus(keychain, byref(flags)), "preflight")
            if flags.value & 6 != 6:
                raise CredentialWriteNotStarted(stage="preflight")
        finally:
            self._release(keychain)

    def resolve(self, tenant_id: str, credential_id: str) -> str:
        account = self._account(tenant_id, credential_id)
        length = c_uint32()
        data = c_void_p()
        item = c_void_p()
        status = self._security.SecKeychainFindGenericPassword(
            None,
            len(self.service), self.service,
            len(account), account,
            byref(length), byref(data), byref(item),
        )
        self._raise_status(status, "resolve")
        try:
            secret = string_at(data, length.value).decode("utf-8")
        except UnicodeDecodeError as error:
            raise CredentialError("macOS Keychain credential is not valid UTF-8") from error
        finally:
            if data.value:
                self._security.SecKeychainItemFreeContent(None, data)
            self._release(item)
        self._known_secrets.add(secret)
        return secret

    def disable(self, tenant_id: str, credential_id: str) -> None:
        self.delete(tenant_id, credential_id)

    def delete(self, tenant_id: str, credential_id: str) -> None:
        account = self._account(tenant_id, credential_id)
        try:
            item = self._find_item(account)
        except CredentialError as error:
            if "not found" in str(error):
                return
            raise
        try:
            status = self._security.SecKeychainItemDelete(item)
        finally:
            self._release(item)
        self._raise_status(status, "delete")

    def test(self, tenant_id: str, credential_id: str) -> bool:
        account = self._account(tenant_id, credential_id)
        item = self._find_item(account)
        self._release(item)
        return True

    def redact(self, value: Any) -> str:
        text = str(value)
        for secret in self._known_secrets:
            if secret:
                text = text.replace(secret, "[REDACTED]")
        return redact_model_gateway_text(text)

    def _find_item(self, account: bytes) -> c_void_p:
        item = c_void_p()
        status = self._security.SecKeychainFindGenericPassword(
            None,
            len(self.service), self.service,
            len(account), account,
            None, None, byref(item),
        )
        self._raise_status(status, "find")
        return item

    def _raise_status(self, status: int, action: str) -> None:
        if status == 0:
            return
        if action == "preflight":
            raise CredentialWriteNotStarted(stage="preflight", os_status=status)
        if action == "store":
            raise CredentialStageFailure("CREDENTIAL_NATIVE_WRITE_UNCONFIRMED", "native_store", "unknown", os_status=status)
        if status == self._ITEM_NOT_FOUND and action != "preflight":
            raise CredentialError("macOS Keychain credential was not found")
        if status == -128:
            raise CredentialError(f"macOS Keychain {action} cancelled (OSStatus {status})")
        raise CredentialError(f"macOS Keychain {action} failed (OSStatus {status})")

    def _release(self, item: c_void_p) -> None:
        if item.value:
            self._core_foundation.CFRelease(item)


def credential_ref_digest(credential_ref: str) -> str:
    return "sha256:" + hashlib.sha256(credential_ref.encode("utf-8")).hexdigest()


def is_resolver_managed_ref(value: str | None) -> bool:
    if not value:
        return False
    return bool(LOCAL_REF_RE.match(value) or VAULT_REF_RE.match(value))


def safe_credential_metadata(row: dict[str, Any]) -> dict[str, Any]:
    scheme = str(row["credential_ref"]).split(":", 1)[0]
    return {
        "credential_id": row["credential_id"],
        "tenant_id": row["tenant_id"],
        "name": row["name"],
        "provider": row["provider"],
        "credential_type": row["credential_type"],
        "credential_ref": row["credential_ref"],
        "credential_ref_digest": credential_ref_digest(row["credential_ref"]),
        "storage": "macos_keychain" if scheme == "vault" else "process_memory",
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "disabled_at": row.get("disabled_at") or "",
    }


class CredentialVaultService:
    def __init__(
        self,
        database: Database,
        event_log: EvolutionEventLog,
        *,
        environment: str | None = None,
        local_backend: LocalDevCredentialBackend | None = None,
        vault_backend: CredentialBackend | None = None,
        kms_backend: CredentialBackend | None = None,
        backend_mode: str | None = None,
    ) -> None:
        self.database = database
        self.event_log = event_log
        self.environment = (environment or os.getenv("CURIS_ENV", "local")).lower()
        self.local_backend = local_backend or LocalDevCredentialBackend()
        packaged = os.getenv("CURIS_PACKAGED_RUNTIME", "").strip().lower() in {"1", "true", "yes"}
        self.backend_mode = (
            backend_mode
            or os.getenv("CURIS_CREDENTIAL_BACKEND")
            or ("macos-keychain" if packaged or self.environment in {"production", "prod"} else "local-dev")
        ).strip().lower()
        if packaged and self.backend_mode != "macos-keychain":
            raise CredentialError("packaged Runtime requires macOS Keychain credential storage")
        if self.backend_mode == "macos-keychain":
            self.vault_backend = vault_backend or MacOSKeychainCredentialBackend()
        elif self.backend_mode == "local-dev":
            self.vault_backend = vault_backend or UnconfiguredVaultBackend()
        else:
            raise CredentialError("credential backend mode is not supported")
        self.kms_backend = kms_backend or UnconfiguredVaultBackend()

    def create(
        self,
        *,
        name: str,
        provider: str,
        credential_type: str,
        secret: str,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        if credential_type == _CODEX_AUTH_TYPE:
            raise CredentialWriteNotStarted("Codex authentication requires its original owned lease")
        if self.environment in {"production", "prod"} and self.backend_mode != "macos-keychain":
            raise CredentialError("local-dev credential creation is not allowed in production")
        self._validate_secret(secret)
        credential_id = f"cred-{uuid.uuid4()}"
        scheme = "vault" if self.backend_mode == "macos-keychain" else "local-dev"
        credential_ref = f"{scheme}://tenant/{tenant_id}/credential/{credential_id}"
        try:
            backend = self._backend_for_ref(credential_ref)
        except CredentialError as error:
            raise CredentialWriteNotStarted(stage="validation") from error
        self._store_with_stage(backend, tenant_id, credential_id, secret)
        try:
            row = self.database.save_credential_metadata(
                credential_id=credential_id,
                tenant_id=tenant_id,
                name=name,
                provider=provider,
                credential_type=credential_type,
                credential_ref=credential_ref,
                status="active",
                encrypted_metadata={
                    "backend": self.backend_mode,
                    "secret_digest": self._secret_digest(secret),
                },
            )
        except Exception as error:
            try:
                backend.delete(tenant_id, credential_id)
            except Exception:
                pass  # A failed cleanup cannot establish whether the native item exists.
            raise CredentialStageFailure("CREDENTIAL_METADATA_UNCONFIRMED", "metadata", "native_returned_success") from error
        try:
            self._audit("credential.created", row, "success")
        except Exception as error:
            raise CredentialStageFailure("CREDENTIAL_AUDIT_FAILED", "audit", "metadata_returned_success") from error
        return safe_credential_metadata(row)

    @staticmethod
    def _store_with_stage(backend: CredentialBackend, tenant_id: str, credential_id: str, secret: str) -> None:
        try:
            backend.store(tenant_id, credential_id, secret)
        except CredentialStageFailure:
            raise
        except Exception as error:
            raise CredentialStageFailure("CREDENTIAL_NATIVE_WRITE_UNCONFIRMED", "native_store", "unknown") from error

    def list(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        return {
            "tenant_id": tenant_id,
            "credentials": [
                safe_credential_metadata(row)
                for row in self.database.list_credential_metadata(tenant_id)
            ],
        }

    def update(
        self,
        credential_id: str,
        *,
        name: str | None = None,
        provider: str | None = None,
        credential_type: str | None = None,
        secret: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        try:
            row = self._get_owned(tenant_id, credential_id)
        except CredentialError as error:
            raise CredentialWriteNotStarted(stage="validation") from error
        encrypted_metadata = dict(row.get("encrypted_metadata", {}))
        if row["credential_type"] == _CODEX_AUTH_TYPE or credential_type == _CODEX_AUTH_TYPE:
            raise CredentialWriteNotStarted("Use the owned Codex connection controls")
        if secret:
            self._validate_secret(secret)
            try:
                backend = self._backend_for_ref(row["credential_ref"])
            except CredentialError as error:
                raise CredentialWriteNotStarted(stage="validation") from error
            self._store_with_stage(backend, tenant_id, credential_id, secret)
            encrypted_metadata["secret_digest"] = self._secret_digest(secret)
        try:
            updated = self.database.save_credential_metadata(
                credential_id=credential_id,
                tenant_id=tenant_id,
                name=name if name is not None else row["name"],
                provider=provider if provider is not None else row["provider"],
                credential_type=credential_type if credential_type is not None else row["credential_type"],
                credential_ref=row["credential_ref"],
                status=row["status"],
                encrypted_metadata=encrypted_metadata,
            )
        except Exception as error:
            raise CredentialStageFailure("CREDENTIAL_METADATA_UNCONFIRMED", "metadata", "native_returned_success" if secret else "not_started") from error
        try:
            self._audit("credential.updated", updated, "success")
        except Exception as error:
            raise CredentialStageFailure("CREDENTIAL_AUDIT_FAILED", "audit", "metadata_returned_success") from error
        return safe_credential_metadata(updated)

    def disable(self, credential_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        row = self._get_owned(tenant_id, credential_id)
        if row["credential_type"] == _CODEX_AUTH_TYPE:
            raise CredentialError("Use the owned Codex disconnect control")
        self._backend_for_ref(row["credential_ref"]).disable(tenant_id, credential_id)
        disabled = self.database.disable_credential_metadata(tenant_id, credential_id)
        self._audit("credential.disabled", disabled, "success")
        return safe_credential_metadata(disabled)

    def delete(self, credential_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        row = self._get_owned(tenant_id, credential_id)
        if row["credential_type"] == _CODEX_AUTH_TYPE:
            raise CredentialError("Use the owned Codex disconnect control")
        self._backend_for_ref(row["credential_ref"]).delete(tenant_id, credential_id)
        deleted = self.database.delete_credential_metadata(tenant_id, credential_id)
        self._audit("credential.deleted", deleted, "success")
        return safe_credential_metadata(deleted)

    def test(self, credential_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        row = self._get_owned(tenant_id, credential_id)
        try:
            resolved = self.resolve(row["credential_ref"])
            ok = bool(resolved["secret"])
        except CredentialError as error:
            self._audit("credential.tested", row, "failure", str(error))
            raise
        self._audit("credential.tested", row, "success")
        return {
            "credential_id": credential_id,
            "credential_ref": row["credential_ref"],
            "credential_ref_digest": credential_ref_digest(row["credential_ref"]),
            "status": "ok" if ok else "failed",
        }

    def resolve(self, credential_ref: str, *, provider: str | None = None) -> dict[str, str]:
        tenant_id = TenantContext.current_tenant_id()
        try:
            scheme, ref_tenant, credential_id = self._parse_ref(credential_ref)
            if ref_tenant != tenant_id:
                raise CredentialError("credential_ref tenant does not match current tenant")
            if scheme == "local-dev" and self.environment in {"production", "prod"}:
                raise CredentialError("local-dev credential_ref is not allowed in production")
            row = self._get_owned(tenant_id, credential_id)
            if row["credential_type"] == _CODEX_AUTH_TYPE:
                raise CredentialError("Codex credentials require the original execution lease")
            if row["status"] != "active":
                raise CredentialError("credential is not active")
            if provider is not None and row["provider"] != provider:
                raise CredentialError("credential provider does not match requested provider")
            secret = self._backend_for_ref(credential_ref).resolve(tenant_id, credential_id)
            self._audit("credential.resolved", row, "success")
            return {
                "credential_id": credential_id,
                "credential_ref": credential_ref,
                "credential_ref_digest": credential_ref_digest(credential_ref),
                "secret": secret,
            }
        except CredentialError as error:
            self._audit_resolve_failed(credential_ref, str(error))
            raise CredentialError(redact_model_gateway_text(error)) from error

    def resolve_for_provider(self, credential_ref: str, provider: str) -> dict[str, str]:
        return self.resolve(credential_ref, provider=provider)

    def codex_connection(self, company_id: str, capability_id: str) -> dict[str, Any]:
        tenant = TenantContext.current_tenant_id()
        rows = [row for row in self.database.list_credential_metadata(tenant)
            if row["credential_type"] == _CODEX_AUTH_TYPE and row["provider"] == "codex-cli"
            and row["status"] == "active" and row["encrypted_metadata"].get("company_id") == company_id
            and row["encrypted_metadata"].get("capability_id") == capability_id]
        if len(rows) > 1: raise CredentialError("Codex connection ownership is ambiguous; HELD")
        metadata = rows[0]["encrypted_metadata"] if rows else {}
        return {"company_id": company_id, "capability_id": capability_id,
            "state": metadata.get("auth_state", "DISCONNECTED"), "generation": metadata.get("generation")}

    def begin_codex_lease(self, company_id, capability_id, identity, *, intent="use", expected_generation=None, parent=None):
        import secrets
        tenant = TenantContext.current_tenant_id()
        keys = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
        if (self.backend_mode != "macos-keychain" or type(identity) is not dict or set(identity) != keys
                or any(type(v) is not str or not v for v in identity.values())
                or identity["tenant_id"] != tenant or identity["company_id"] != company_id
                or type(capability_id) is not str or not capability_id or len(capability_id) > 128
                or intent not in {"login", "use", "status", "disconnect"}):
            raise CredentialError("Owned Codex authentication scope is invalid")
        lease_nonce = secrets.token_hex(24)
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            rows = connection.execute("select * from credential_metadata where tenant_id=? and provider=? and credential_type=? and status='active'",
                (tenant, "codex-cli", _CODEX_AUTH_TYPE)).fetchall()
            owned = []
            for candidate in rows:
                metadata = json.loads(candidate["encrypted_metadata"])
                if metadata.get("company_id") == company_id and metadata.get("capability_id") == capability_id:
                    owned.append((candidate, metadata))
            if len(owned) > 1: raise CredentialError("Codex connection ownership is ambiguous; HELD")
            row, metadata = owned[0] if owned else (None, {})
            if row is not None and not re.fullmatch(r"[0-9a-f]{48}", str(metadata.get("generation"))):
                raise CredentialError("Codex connection generation is invalid; HELD")
            if metadata.get("auth_state") in {"LEASED", "WRITEBACK_PENDING", "CACHE_SAVED"}:
                from .reader_vm_host import _OriginalWorkOwners
                if (intent!="login" or expected_generation!=metadata.get("generation")
                        or type(parent) is not _OriginalWorkOwners or parent.identity!=identity or not parent.can_reseed()):
                    raise CredentialError("Codex authentication is already leased or unresolved")
            if expected_generation is not None and metadata.get("generation") != expected_generation:
                raise CredentialError("Codex connection changed; read its current state")
            if intent == "login":
                if row is not None and metadata.get("auth_state") == "CONNECTED":
                    raise CredentialError("Codex is already connected")
                if row is not None:
                    if expected_generation != metadata.get("generation"):
                        raise CredentialError("Reconnect requires the held original generation")
                    connection.execute("update credential_metadata set status='disabled', updated_at=current_timestamp where tenant_id=? and credential_id=?",
                        (tenant, row["credential_id"]))
                credential_id = "cred-" + str(uuid.uuid4())
                credential_ref = f"vault://tenant/{tenant}/credential/{credential_id}"
                metadata = {"backend": "macos-keychain", "company_id": company_id,
                    "capability_id": capability_id, "generation": secrets.token_hex(24)}
            else:
                if row is None or metadata.get("auth_state") != "CONNECTED":
                    raise CredentialError("Codex authentication requires explicit connection; HELD")
                credential_id, credential_ref = row["credential_id"], row["credential_ref"]
                if (metadata.get("backend") != "macos-keychain"
                        or credential_ref != f"vault://tenant/{tenant}/credential/{credential_id}"):
                    raise CredentialError("Codex Keychain reference changed; HELD")
            metadata.update(auth_state="LEASED", lease_nonce=lease_nonce, intent=intent,
                original_identity_sha256=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(",", ":")).encode()).hexdigest())
            connection.execute("""insert into credential_metadata
                (credential_id,tenant_id,name,provider,credential_type,credential_ref,status,encrypted_metadata,updated_at)
                values (?,?,?,?,?,?,'active',?,current_timestamp)
                on conflict(credential_id) do update set encrypted_metadata=excluded.encrypted_metadata,updated_at=current_timestamp""",
                (credential_id,tenant,"Curis Codex connection","codex-cli",_CODEX_AUTH_TYPE,credential_ref,json.dumps(metadata)))
        return _CodexAuthLease(self, tenant, credential_id, metadata, identity)

    def _codex_lease_state(self, lease, *, expected, target):
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute("select encrypted_metadata,status,credential_type,provider,credential_ref from credential_metadata where tenant_id=? and credential_id=?",
                (lease.tenant,lease.credential_id)).fetchone()
            if (row is None or row["status"] != "active" or row["credential_type"] != _CODEX_AUTH_TYPE or row["provider"] != "codex-cli"
                    or row["credential_ref"] != f"vault://tenant/{lease.tenant}/credential/{lease.credential_id}"):
                raise CredentialError("Original Codex lease is unavailable")
            metadata = json.loads(row["encrypted_metadata"])
            if (metadata.get("backend") != "macos-keychain" or any(metadata.get(key) != lease.metadata[key] for key in
                    ("company_id","capability_id","generation","lease_nonce","original_identity_sha256"))
                    or metadata.get("auth_state") not in expected):
                raise CredentialError("Original Codex lease changed; HELD")
            if target is not None:
                metadata["auth_state"] = target
                if target == "DISCONNECTED": metadata["lease_nonce"] = None
                connection.execute("update credential_metadata set encrypted_metadata=?,status=?,updated_at=current_timestamp where tenant_id=? and credential_id=?",
                    (json.dumps(metadata), "disabled" if target == "DISCONNECTED" else "active", lease.tenant,lease.credential_id))
            return metadata

    def bind_capability(
        self,
        *,
        capability_type: str,
        capability_id: str,
        credential_ref: str,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        resolved = self._resolve_metadata_only(credential_ref)
        capability = self.database.get_tenant_private_capability(tenant_id, capability_type, capability_id)
        if capability is None:
            raise CredentialError("tenant_private capability is not available")
        metadata = dict(capability.get("metadata", {}))
        field = "credential_ref" if capability_type == "model" else "config_ref"
        metadata[field] = credential_ref
        updated = self.database.save_tenant_private_capability(
            tenant_id=tenant_id,
            capability_type=capability_type,
            capability_id=capability_id,
            display_name=capability.get("display_name", capability_id),
            metadata=metadata,
            status=capability.get("status", "active"),
        )
        self._audit("credential.bound", resolved, "success", capability_id)
        return updated

    def unbind_capability(self, *, capability_type: str, capability_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        capability = self.database.get_tenant_private_capability(tenant_id, capability_type, capability_id)
        if capability is None:
            raise CredentialError("tenant_private capability is not available")
        metadata = dict(capability.get("metadata", {}))
        credential_ref = metadata.pop("credential_ref", "") or metadata.pop("config_ref", "")
        updated = self.database.save_tenant_private_capability(
            tenant_id=tenant_id,
            capability_type=capability_type,
            capability_id=capability_id,
            display_name=capability.get("display_name", capability_id),
            metadata=metadata,
            status=capability.get("status", "active"),
        )
        if credential_ref and is_resolver_managed_ref(credential_ref):
            self._audit("credential.unbound", self._resolve_metadata_only(credential_ref), "success", capability_id)
        return updated

    def redact(self, value: Any) -> str:
        text = self.local_backend.redact(value)
        text = self.vault_backend.redact(text)
        return self.kms_backend.redact(text)

    def _resolve_metadata_only(self, credential_ref: str) -> dict[str, Any]:
        scheme, ref_tenant, credential_id = self._parse_ref(credential_ref)
        tenant_id = TenantContext.current_tenant_id()
        if ref_tenant != tenant_id:
            raise CredentialError("credential_ref tenant does not match current tenant")
        if scheme == "local-dev" and self.environment in {"production", "prod"}:
            raise CredentialError("local-dev credential_ref is not allowed in production")
        row = self._get_owned(tenant_id, credential_id)
        if row["status"] != "active":
            raise CredentialError("credential is not active")
        return row

    def _get_owned(self, tenant_id: str, credential_id: str) -> dict[str, Any]:
        row = self.database.get_credential_metadata(tenant_id, credential_id)
        if row is None:
            raise CredentialError("credential is not available for this tenant")
        return row

    def _backend_for_ref(self, credential_ref: str) -> CredentialBackend:
        scheme, _, _ = self._parse_ref(credential_ref)
        if scheme == "local-dev":
            return self.local_backend
        if scheme == "vault":
            return self.vault_backend
        if scheme == "kms":
            return self.kms_backend
        raise CredentialError("credential_ref scheme is not allowed")

    @staticmethod
    def _parse_ref(credential_ref: str) -> tuple[str, str, str]:
        local = LOCAL_REF_RE.match(credential_ref or "")
        if local:
            return "local-dev", local.group(1), local.group(2)
        external = VAULT_REF_RE.match(credential_ref or "")
        if external:
            return external.group(1), external.group(2), external.group(3)
        raise CredentialError("credential_ref format is not allowed")

    @staticmethod
    def _validate_secret(secret: str) -> None:
        if not secret or not str(secret).strip():
            raise CredentialWriteNotStarted("credential secret is required")
        if SECRET_FIELD_RE.search(str(secret)):
            # The value itself may contain these words; this blocks attempts to
            # submit serialized key/value config where the DB could persist a
            # recoverable plaintext secret bundle.
            raise CredentialWriteNotStarted("credential secret must be submitted as a single opaque value")
        if "\x00" in str(secret):
            raise CredentialWriteNotStarted("credential secret contains an invalid null byte")

    @staticmethod
    def _secret_digest(secret: str) -> str:
        return "sha256:" + hashlib.sha256(secret.encode("utf-8")).hexdigest()

    def _audit(
        self,
        action: str,
        row: dict[str, Any],
        status: str,
        reason: str = "",
    ) -> None:
        tenant_id = row["tenant_id"]
        credential_ref = row["credential_ref"]
        self.event_log.record(
            correlation_id=row["credential_id"],
            event_type=action,
            tenant_id=tenant_id,
            payload={
                "tenant_id": tenant_id,
                "credential_id": row["credential_id"],
                "credential_ref_digest": credential_ref_digest(credential_ref),
                "actor_id": CeoContext.current_ceo_id() or "workspace-runtime",
                "action": action,
                "status": status,
                "reason": redact_model_gateway_text(reason),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    def _audit_resolve_failed(self, credential_ref: str, reason: str) -> None:
        credential_id = ""
        try:
            _, _, credential_id = self._parse_ref(credential_ref)
        except CredentialError:
            pass
        self.event_log.record(
            correlation_id=credential_id or str(uuid.uuid4()),
            event_type="credential.resolve_failed",
            tenant_id=TenantContext.current_tenant_id(),
            payload={
                "tenant_id": TenantContext.current_tenant_id(),
                "credential_id": credential_id,
                "credential_ref_digest": credential_ref_digest(credential_ref or ""),
                "actor_id": CeoContext.current_ceo_id() or "workspace-runtime",
                "action": "credential.resolve_failed",
                "status": "failure",
                "reason": redact_model_gateway_text(reason),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )


class _CodexAuthLease:
    """Keychain cache round-trip for one original server-owned execution only."""
    def __init__(self, service, tenant, credential_id, metadata, identity):
        import threading
        self.service, self.tenant, self.credential_id = service, tenant, credential_id
        self.metadata, self.identity = dict(metadata), dict(identity)
        self.intent = metadata["intent"]
        self.binding, self.restored, self.finished = None, False, False
        self.cache_saved = False
        self.parent, self._redactions = None, set()
        self.cancelled = threading.Event()

    def __enter__(self): return self

    def __exit__(self, kind, error, traceback):
        failure = None
        if not self.finished and kind is None and self.cache_saved and self.parent is not None and not self.cancelled.is_set():
            try: self.finish(self.parent.receipt)
            except BaseException as failed: failure = failed
        if not self.finished:
            try: self.abort()
            except BaseException:
                if error is None: raise
                error.add_note("Codex authentication remains HELD/UNKNOWN")
            if error is None and failure is None:
                failure = CredentialError("Codex authentication was not finalized")
        if failure is not None:
            raise CredentialError("Codex authentication closure remains HELD/UNKNOWN") from None

    def bind_parent(self, parent):
        from .reader_vm_host import _OriginalWorkOwners
        if (type(parent) is not _OriginalWorkOwners or parent.identity != self.identity or parent.closed
                or self.parent is not None and self.parent is not parent):
            raise CredentialError("Original Codex parent lease changed")
        self.parent = parent

    def _remember_redactions(self, cache):
        self._redactions.update(value for value in json.loads(cache)["tokens"].values() if type(value) is str and value)

    def redact_output(self, value):
        if type(value) is not str: raise CredentialError("Invalid Codex output")
        for token in self._redactions:
            value = value.replace(token, "[REDACTED]").replace(json.dumps(token)[1:-1], "[REDACTED]")
        return value

    @staticmethod
    def _cache(value):
        if type(value) is not str or not 0 < len(value.encode("utf-8")) <= 32768 or "\0" in value:
            raise CredentialError("Managed Codex auth cache shape is invalid")
        def unique(pairs):
            result = {}
            for key, item in pairs:
                if key in result: raise CredentialError("Managed Codex auth cache has duplicate fields")
                result[key] = item
            return result
        def invalid(_value): raise ValueError("Nonfinite auth cache field")
        try:
            data = json.loads(value, object_pairs_hook=unique, parse_constant=invalid)
            if (type(data) is not dict or set(data) - {"auth_mode", "OPENAI_API_KEY", "tokens", "last_refresh"}
                    or data.get("auth_mode") != "chatgpt" or data.get("OPENAI_API_KEY") not in (None, "")):
                raise ValueError()
            tokens = data.get("tokens")
            if (type(tokens) is not dict or set(tokens) - {"access_token", "refresh_token", "id_token", "account_id"}
                    or any(type(tokens.get(k)) is not str or not tokens[k] for k in ("access_token", "refresh_token", "id_token"))):
                raise ValueError()
            if tokens.get("account_id") is not None and type(tokens["account_id"]) is not str: raise ValueError()
            if data.get("last_refresh") is not None:
                if type(data["last_refresh"]) is not str: raise ValueError()
                datetime.fromisoformat(data["last_refresh"].replace("Z", "+00:00"))
        except (ValueError, TypeError, CredentialError):
            raise CredentialError("Managed Codex auth cache shape is invalid") from None
        return value

    def restore(self, binding):
        keys = {"identity", "nonce", "boot_id", "container_id", "image_digest", "parent_attempt"}
        if (self.restored or self.finished or self.cancelled.is_set() or type(binding) is not dict or set(binding) != keys
                or binding["identity"] != self.identity
                or not re.fullmatch(r"[0-9a-f]{48}", str(binding["nonce"]))
                or not re.fullmatch(r"[0-9a-f]{48}", str(binding["parent_attempt"]))
                or not re.fullmatch(r"[0-9a-f]{64}", str(binding["container_id"]))
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(binding["image_digest"]))
                or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", str(binding["boot_id"]))):
            raise CredentialError("Original Codex authentication runtime changed")
        self.service._codex_lease_state(self, expected={"LEASED"}, target=None)
        self.binding = {**binding, "identity": self.identity.copy()}
        if self.parent is not None and (self.parent.attempt != binding["parent_attempt"] or self.parent.boot_id != binding["boot_id"]):
            raise CredentialError("Original Codex parent generation changed")
        self.restored = True
        if self.intent == "login": return None
        try:
            cache = self._cache(self.service.vault_backend.resolve(self.tenant, self.credential_id))
            self._remember_redactions(cache)
            if self.cancelled.is_set(): raise CredentialError("Original Codex authentication cancelled")
            return cache
        except Exception:
            self.abort()
            raise CredentialError("Owned Codex Keychain cache is unavailable; HELD") from None

    def persist(self, binding, cache, *, authenticated):
        if self.binding is None or binding != self.binding or self.cancelled.is_set() or type(authenticated) is not bool:
            raise CredentialError("Original Codex authentication writeback changed")
        disconnect = self.intent == "disconnect"
        if disconnect:
            if authenticated is not False or cache is not None:
                raise CredentialError("Official Codex local logout is unconfirmed")
        elif authenticated is not True:
            raise CredentialError("Official Codex authentication is unconfirmed")
        else:
            cache = self._cache(cache)
            self._remember_redactions(cache)
        self.service._codex_lease_state(self, expected={"LEASED"}, target="WRITEBACK_PENDING")
        try:
            if disconnect: self.service.vault_backend.delete(self.tenant, self.credential_id)
            else: self.service._store_with_stage(self.service.vault_backend, self.tenant, self.credential_id, cache)
            if self.cancelled.is_set(): raise CredentialError("Original Codex authentication cancelled")
            self.service._codex_lease_state(self, expected={"WRITEBACK_PENDING"}, target="CACHE_SAVED")
            self.cache_saved = True
        except BaseException:
            self.abort()
            raise CredentialError("Codex Keychain writeback is unconfirmed; HELD") from None

    def finish(self, receipt):
        if self.cancelled.is_set() or self.finished or self.binding is None or type(receipt) is not dict:
            raise CredentialError("Codex authentication closure is unconfirmed")
        children = receipt.get("children")
        if (receipt.get("identity") != self.identity or receipt.get("parent_attempt") != self.binding["parent_attempt"]
                or receipt.get("boot_id") != self.binding["boot_id"] or receipt.get("ledger_state") != "CLOSED_VERIFIED"
                or type(children) is not list or not children
                or any(type(child) is not dict or child.get("identity") != self.identity
                    or child.get("ledger_state") != "CLOSED_VERIFIED" or child.get("boot_id") != self.binding["boot_id"] for child in children)
                or not any(all(child.get(key) == self.binding[key] for key in ("nonce", "container_id", "image_digest")) for child in children)):
            raise CredentialError("Original Codex parent closure changed")
        seen = set()
        for child in children:
            cid, proxy = child.get("container_id"), child.get("proxy_id")
            if type(cid) is not str or (proxy is not None and (type(proxy) is not str or proxy == cid)):
                raise CredentialError("Original Codex child exit evidence changed")
            ids = {cid, proxy} if proxy is not None else {cid}
            if (any(not re.fullmatch(r"[0-9a-f]{64}", str(value)) for value in ids) or seen.intersection(ids)
                    or not re.fullmatch(r"[0-9a-f]{48}", str(child.get("nonce")))
                    or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(child.get("image_digest")))
                    or type(child.get("exit_codes")) is not dict or set(child["exit_codes"]) != ids
                    or any(type(value) is not int for value in child["exit_codes"].values())):
                raise CredentialError("Original Codex child exit evidence changed")
            seen.update(ids)
        self.service._codex_lease_state(self, expected={"CACHE_SAVED"},
            target="DISCONNECTED" if self.intent == "disconnect" else "CONNECTED")
        if self.cancelled.is_set() and self.intent != "disconnect":
            self.service._codex_lease_state(self, expected={"CONNECTED"}, target="HELD")
            raise CredentialError("Codex authentication cancelled during lease release; HELD")
        self.finished = True

    def cancel(self):
        self.cancelled.set()  # Stop execution first; metadata I/O runs after owned cleanup.

    def abort(self):
        self.cancelled.set()
        if not self.finished:
            self.service._codex_lease_state(self, expected={"LEASED", "WRITEBACK_PENDING", "CACHE_SAVED", "HELD"}, target="HELD")
