from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import ipaddress
import json
import logging
import os
import uuid

from .tenant_context import DEFAULT_TENANT


_LOG = logging.getLogger("curis.security.identity")


class IdentityAuthorizationError(Exception):
    def __init__(self, status_code: int, reason: str):
        super().__init__(reason)
        self.status_code = status_code
        self.reason = reason


@dataclass(frozen=True)
class AuthorizedMembership:
    subject_id: str
    tenant_id: str
    company_id: str
    ceo_id: str
    role: str
    membership_status: str
    request_id: str


class IdentityMembership:
    def __init__(self, database):
        self.database = database
        self.environment = os.getenv("CURIS_ENV", "local").strip().lower()
        self.product = os.getenv("CURIS_PRODUCT", "").strip().lower()
        self.mode = os.getenv("CURIS_IDENTITY_MODE", "").strip().lower()
        self.gateway_issuer = os.getenv("CURIS_TRUSTED_GATEWAY_ISSUER", "").strip()
        self.gateway_networks = self._networks(os.getenv("CURIS_TRUSTED_GATEWAY_CIDRS", ""))
        self.audit_key = os.getenv("CURIS_IDENTITY_AUDIT_KEY", "").strip() or "curis-local-audit"

    def validate_configuration(self) -> None:
        if self.product != "workspace" or self.environment != "production":
            return
        if self.mode == "selfuse":
            raise RuntimeError("production Workspace rejects self-use identity mode")
        if (
            self.mode != "gateway"
            or not self.gateway_issuer
            or not self.gateway_networks
            or self.audit_key == "curis-local-audit"
        ):
            raise RuntimeError("production Workspace requires trusted gateway issuer and network")

    def authorize(self, request) -> AuthorizedMembership:
        tenant_id = (request.headers.get("X-Tenant-Id") or "").strip()
        request_id = self._request_id(request.headers.get("X-Curis-Gateway-Request-Id"))
        if self.mode == "test" and not (
            self.product == "workspace" and self.environment == "production"
        ):
            return self._authorize_test(tenant_id, request_id)
        if self.mode == "selfuse":
            return self._authorize_selfuse(tenant_id, request_id)
        if self.mode != "gateway":
            self._deny(401, "trusted_identity_missing", request_id, tenant_id)

        client_host = request.client.host if request.client else ""
        if not self._trusted_source(client_host):
            self._deny(401, "untrusted_gateway_source", request_id, tenant_id)
        subject_id = (request.headers.get("X-Curis-Gateway-Subject") or "").strip()
        issuer = (request.headers.get("X-Curis-Gateway-Issuer") or "").strip()
        auth_time = (request.headers.get("X-Curis-Gateway-Auth-Time") or "").strip()
        if not subject_id or issuer != self.gateway_issuer or not auth_time:
            self._deny(401, "trusted_identity_missing", request_id, tenant_id, subject_id, issuer)
        if not tenant_id:
            self._deny(403, "target_tenant_missing", request_id, tenant_id, subject_id, issuer)

        with self.database.connect() as connection:
            row = connection.execute(
                "select * from tenant_memberships where issuer = ? and subject_id = ? "
                "and tenant_id = ? order by created_at desc limit 1",
                (issuer, subject_id, tenant_id),
            ).fetchone()
            if row is None:
                self._deny(403, "active_membership_missing", request_id, tenant_id, subject_id, issuer)
            membership = dict(row)
            if membership["status"] != "active" or membership.get("revoked_at"):
                self._deny(403, "membership_revoked", request_id, tenant_id, subject_id, issuer)
            expires_at = membership.get("expires_at")
            if expires_at and datetime.fromisoformat(expires_at.replace("Z", "+00:00")) <= datetime.now(timezone.utc):
                self._deny(403, "membership_expired", request_id, tenant_id, subject_id, issuer)
            tenant_exists = connection.execute(
                "select 1 from tenants where tenant_id = ?", (tenant_id,)
            ).fetchone()
            company_exists = connection.execute(
                "select 1 from companies where tenant_id = ? and company_id = ?",
                (tenant_id, membership["company_id"]),
            ).fetchone()
        if tenant_exists is None or company_exists is None:
            self._deny(403, "membership_dual_read_mismatch", request_id, tenant_id, subject_id, issuer)

        result = AuthorizedMembership(
            subject_id,
            tenant_id,
            membership["company_id"],
            membership.get("ceo_id") or "",
            membership["role"],
            "active",
            request_id,
        )
        self._audit("allow", "membership_active", result, issuer)
        return result

    def _authorize_selfuse(self, tenant_id: str, request_id: str) -> AuthorizedMembership:
        if self.environment not in {"local", "development", "test"}:
            self._deny(401, "production_selfuse_rejected", request_id, tenant_id)
        if tenant_id and tenant_id != DEFAULT_TENANT:
            self._deny(403, "selfuse_tenant_mismatch", request_id, tenant_id)
        return AuthorizedMembership(
            "selfuse", DEFAULT_TENANT, "", "selfuse-ceo", "owner", "active", request_id
        )

    def _authorize_test(self, tenant_id: str, request_id: str) -> AuthorizedMembership:
        tenant_id = tenant_id or DEFAULT_TENANT
        return AuthorizedMembership("test-suite", tenant_id, "", "", "test", "active", request_id)

    def _deny(
        self,
        status_code: int,
        reason: str,
        request_id: str,
        tenant_id: str,
        subject_id: str = "",
        issuer: str = "",
    ) -> None:
        self._audit(
            "deny", reason, AuthorizedMembership(subject_id, tenant_id, "", "", "", "", request_id), issuer
        )
        raise IdentityAuthorizationError(status_code, reason)

    def _audit(self, outcome: str, reason: str, membership: AuthorizedMembership, issuer: str) -> None:
        digest = hmac.new(
            self.audit_key.encode(), f"{issuer}\0{membership.subject_id}".encode(), hashlib.sha256
        ).hexdigest()
        _LOG.log(
            logging.WARNING if outcome == "deny" else logging.INFO,
            json.dumps(
                {
                    "outcome": outcome,
                    "reason": reason,
                    "request_id": membership.request_id,
                    "subject_digest": digest,
                    "tenant_id": membership.tenant_id,
                },
                separators=(",", ":"),
                sort_keys=True,
            ),
        )

    def _trusted_source(self, host: str) -> bool:
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            return False
        return any(address in network for network in self.gateway_networks)

    @staticmethod
    def _networks(value: str) -> tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]:
        return tuple(
            ipaddress.ip_network(item.strip(), strict=False)
            for item in value.split(",")
            if item.strip()
        )

    @staticmethod
    def _request_id(value: str | None) -> str:
        if value and len(value) <= 128 and all(ch.isalnum() or ch in "-_." for ch in value):
            return value
        return str(uuid.uuid4())
