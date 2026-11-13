"""Tenant scope for the ADR-0017 multi-tenant subsystem.

This is the S1 D1.impl (issue 057 / ADR-0027) realization of the D1 design-only
reservation. The system is now **tenant-aware**:

  - ``is_multi_tenant()`` returns ``True``.
  - ``scope(tenant_id)`` remains the per-request injection point: it sets the
    tenant contextvar for the duration of the ``with`` block and restores the
    previous value afterwards.
  - ``parse_tenant_from_request(request)`` resolves the tenant id from the
    ``X-Tenant-Id`` header (falling back to the ``DEFAULT_TENANT`` sentinel).
  - The data layer (``ResultStore``) stamps every write with the active tenant
    and filters every read by it, so one tenant cannot observe another's tasks
    or executions.

Evolution-event reads remain unfiltered for S1 (the ``tenant_id`` column on
``evolution_events`` is reserved for future use); **task isolation is the
acceptance criterion** for this slice.

Security boundary (安全边界席 review embedded):
  - The ``tenants`` table carries NO credential/secret columns.
  - The four LOCKED_ACTIONS (``manage_department_types``,
    ``lift_human_approval_gate``, ``auto_modify_code``, ``cross_company_policy``)
    are not implemented or unlocked by this slice.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator

# Self-use v1 (主理人裁定 §六.4)：全局固定单创始人账号 tenant。
# 单账号下不再做多租户选择 / 隔离机械，只保留 tenant_id 列（字段不删，
# 逻辑不写）。所有 seed / 实例化 / Vault 引用统一用此值。
DEFAULT_TENANT = "selfuse"

# Active tenant for the current request/context. Defaults to the single fixed
# self-use tenant so every code path resolves to one concrete account and all
# reads/writes are scoped to it (single-account, no tenant selection UI).
_current_tenant: ContextVar[str] = ContextVar("curis_tenant", default=DEFAULT_TENANT)
_current_identity: ContextVar[dict[str, str]] = ContextVar(
    "curis_identity",
    default={"subject_id": "", "tenant_id": DEFAULT_TENANT, "company_id": "", "ceo_id": "", "role": "", "membership_status": "", "request_id": ""},
)


class TenantContext:
    @staticmethod
    def current_tenant_id() -> str:
        """Return the active tenant id for the current context."""
        return _current_tenant.get()

    @staticmethod
    @contextmanager
    def scope(
        tenant_id: str,
        *,
        subject_id: str = "",
        company_id: str = "",
        ceo_id: str = "",
        role: str = "",
        membership_status: str = "",
        request_id: str = "",
    ) -> Iterator[None]:
        """Per-request tenant injection point.

        Sets the tenant contextvar for the duration of the ``with`` block and
        restores the previous value afterwards. All data-layer reads/writes
        inside the block are scoped to ``tenant_id`` via ``current_tenant_id()``.
        """
        token = _current_tenant.set(tenant_id)
        identity_token = _current_identity.set(
            {"subject_id": subject_id, "tenant_id": tenant_id, "company_id": company_id, "ceo_id": ceo_id, "role": role, "membership_status": membership_status, "request_id": request_id}
        )
        try:
            yield
        finally:
            _current_identity.reset(identity_token)
            _current_tenant.reset(token)

    @staticmethod
    def current_identity() -> dict[str, str]:
        return dict(_current_identity.get())

    @staticmethod
    def is_multi_tenant() -> bool:
        """Feature flag the system branches on. Real isolation is active now."""
        return True

    @staticmethod
    def parse_tenant_from_request(request) -> str:
        """Resolve the tenant id for an incoming HTTP request.

        Reads the ``X-Tenant-Id`` header; falls back to ``DEFAULT_TENANT`` when
        the header is absent or empty. ``fastapi.Request`` is imported locally to
        keep this module import-cycle free (it has no other heavy dependencies).
        """
        from fastapi import Request  # local import to avoid import cycles

        # Defensive: accept any mapping-like headers object; the canonical path
        # is a FastAPI/Starlette ``Request`` exposing ``.headers``.
        headers = getattr(request, "headers", None)
        if headers is None:
            return DEFAULT_TENANT
        tenant_id = headers.get("X-Tenant-Id")
        if not tenant_id:
            return DEFAULT_TENANT
        return tenant_id
