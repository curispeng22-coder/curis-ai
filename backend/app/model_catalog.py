"""ADR-0028 Phase-2 (issue 064/065): New API gateway + official model catalog.

Admin-only metadata management. This module deliberately:
  * stores ONLY gateway / model metadata (no secrets, no api_key / token columns);
  * validates ``credential_ref`` as an opaque ``scheme:reference`` string and
    NEVER parses or resolves it;
  * NEVER imports ``model_gateway`` and NEVER performs any outbound HTTP call;
  * writes append-only ``capability.*`` audit events via ``EvolutionEventLog``.

Usage projection (R-04) is NOT handled here -- it is reused from
``evolution_event_log`` and exposed read-only through ``/api/platform/usage``
(see ``main.py``).
"""
from __future__ import annotations

import ipaddress
import uuid
import re
from typing import Any
from urllib.parse import urlsplit

from .catalog_constants import (
    GATEWAY_TYPE,
    is_valid_auth_type,
    is_valid_credential_ref,
    is_valid_gateway_status,
    is_valid_gateway_type,
    is_valid_model_status,
)
from .database import Database
from .evolution_event_log import EvolutionEventLog


SECRET_LIKE_PATTERN = re.compile(
    r"sk-(?:or-v1-)?[A-Za-z0-9_-]{10,}|"
    r"Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/\-=:-]+|"
    r"Bearer\s+[A-Za-z0-9._~+/\-=:-]+|"
    r"(api[_-]?key|token|password|secret)\s*[:=]\s*[^,\s;}]+",
    re.IGNORECASE,
)
FREELLMAPI_GATEWAY_ID = "freellmapi.experimental"
FREELLMAPI_ALLOWED_HOSTS = {"localhost", "freellmapi", "host.docker.internal"}


def _validate_experimental_gateway(
    gateway_id: str,
    base_url: str,
    status: str,
    credential_ref: str,
) -> None:
    if gateway_id != FREELLMAPI_GATEWAY_ID:
        return
    parsed = urlsplit(base_url)
    host = parsed.hostname or ""
    try:
        address = ipaddress.ip_address(host)
        private_host = (
            (address.is_loopback or address.is_private)
            and not address.is_unspecified
            and not address.is_link_local
            and not address.is_multicast
            and not address.is_reserved
        )
    except ValueError:
        private_host = host in FREELLMAPI_ALLOWED_HOSTS
    try:
        allowed_port = parsed.port in {3001, 3101}
    except ValueError:
        allowed_port = False
    if (
        parsed.scheme != "http"
        or not private_host
        or not allowed_port
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
    ):
        raise ValueError("FreeLLMAPI base_url 仅允许本机或容器内网 HTTP 地址")
    if status != "inactive":
        raise ValueError("FreeLLMAPI 首次登记必须为 inactive，验证成功后才能启用")
    if credential_ref != "env:FREELLMAPI_API_KEY":
        raise ValueError("FreeLLMAPI 仅允许 env:FREELLMAPI_API_KEY 凭证引用")


def _metadata_has_secret_like_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, tuple, set)):
        return any(_metadata_has_secret_like_value(item) for item in value)
    if isinstance(value, dict):
        return any(
            _metadata_has_secret_like_value(key) or _metadata_has_secret_like_value(item)
            for key, item in value.items()
        )
    return bool(SECRET_LIKE_PATTERN.search(str(value)))


def _reject_secret_like_metadata(**fields: Any) -> None:
    for name, value in fields.items():
        if _metadata_has_secret_like_value(value):
            raise ValueError(f"{name} 不允许包含密钥、令牌或 Authorization 信息")


class GatewayCatalog:
    """Admin gateway (GatewayConfig) metadata management.

    Lifecycle state machine: ``active`` <-> ``inactive`` (no physical delete).
    No secret is ever stored or transmitted; ``credential_ref`` is an opaque
    external reference string only.
    """

    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    def create(
        self,
        gateway_id: str,
        name: str,
        gateway_type: str,
        base_url: str,
        status: str = "active",
        credential_ref: str = "",
        default_model: str = "",
    ) -> dict[str, Any]:
        """Create a gateway config. Raises ``ValueError`` on invalid input and
        ``KeyError`` (caller maps to 422) when the gateway_id already exists."""
        if not gateway_id:
            raise ValueError("gateway_id 不能为空")
        if not name:
            raise ValueError("网关 name 不能为空")
        if not is_valid_gateway_type(gateway_type):
            raise ValueError(
                f"不支持的网关类型 {gateway_type!r}（仅允许 {GATEWAY_TYPE}）"
            )
        if not is_valid_gateway_status(status):
            raise ValueError(f"不支持的网关状态 {status!r}（仅 active|inactive）")
        if not is_valid_credential_ref(credential_ref):
            raise ValueError(
                "credential_ref 须为空或 'scheme:reference' 格式（scheme ∈ env/kms/vault）"
            )
        _validate_experimental_gateway(
            gateway_id,
            base_url,
            status,
            credential_ref,
        )
        _reject_secret_like_metadata(
            gateway_id=gateway_id,
            name=name,
            base_url=base_url,
            default_model=default_model,
        )
        if self.database.get_model_gateway(gateway_id) is not None:
            raise ValueError(f"网关 {gateway_id} 已存在")
        self.database.save_model_gateway(
            gateway_id=gateway_id,
            name=name,
            gateway_type=gateway_type,
            base_url=base_url,
            status=status,
            credential_ref=credential_ref or None,
            default_model=default_model or None,
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.gateway_created",
            payload={
                "gateway_id": gateway_id,
                "name": name,
                "type": gateway_type,
                "base_url": base_url,
                "status": status,
                "credential_ref": credential_ref or None,
                "default_model": default_model or None,
            },
        )
        return self.database.get_model_gateway(gateway_id)

    def set_status(
        self,
        gateway_id: str,
        status: str,
        *,
        verified: bool = False,
    ) -> dict[str, Any]:
        """Enable / disable a gateway. Raises ``KeyError`` if it does not exist."""
        if not is_valid_gateway_status(status):
            raise ValueError(f"不支持的网关状态 {status!r}（仅 active|inactive）")
        if gateway_id == FREELLMAPI_GATEWAY_ID and status == "active" and not verified:
            raise ValueError("FreeLLMAPI 必须通过 Owner-local 验证后才能启用")
        if self.database.get_model_gateway(gateway_id) is None:
            raise KeyError(f"网关不存在：{gateway_id}")
        self.database.set_model_gateway_status(gateway_id, status)
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.gateway_status_changed",
            payload={"gateway_id": gateway_id, "status": status},
        )
        return self.database.get_model_gateway(gateway_id)

    def get(self, gateway_id: str) -> dict[str, Any]:
        """Return a single gateway row; raises ``KeyError`` if absent."""
        row = self.database.get_model_gateway(gateway_id)
        if row is None:
            raise KeyError(f"网关不存在：{gateway_id}")
        return row

    def list(self) -> list[dict[str, Any]]:
        """List all gateway configs."""
        return self.database.list_model_gateways()


class ModelCatalog:
    """Admin official model catalog management.

    Enforces ``gateway_ref`` existence (no dangling references) and the
    ``active`` <-> ``inactive`` state machine (no physical delete).
    """

    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    def create(
        self,
        model_key: str,
        provider_id: str,
        display_name: str,
        supported_models: list[str] | None = None,
        auth_type: str = "apikey",
        gateway_ref: str = "newapi",
        status: str = "active",
        default_model: str = "",
    ) -> dict[str, Any]:
        """Create an official model catalog entry.

        Raises ``KeyError`` (caller maps to 422) when ``gateway_ref`` does not
        exist, and ``ValueError`` on invalid enums or duplicate model_key.
        """
        if not model_key:
            raise ValueError("model_key 不能为空")
        if not is_valid_auth_type(auth_type):
            raise ValueError(
                f"不支持的 auth_type {auth_type!r}（仅形状 none|oauth|apikey）"
            )
        if not is_valid_model_status(status):
            raise ValueError(f"不支持的模型状态 {status!r}（仅 active|inactive）")
        if self.database.get_model_gateway(gateway_ref) is None:
            raise KeyError(f"gateway_ref 不存在：{gateway_ref}")
        if self.database.get_official_model(model_key) is not None:
            raise ValueError(f"模型 {model_key} 已存在")
        _reject_secret_like_metadata(
            model_key=model_key,
            provider_id=provider_id,
            display_name=display_name,
            supported_models=supported_models or [],
            gateway_ref=gateway_ref,
            default_model=default_model,
        )
        self.database.save_official_model(
            model_key=model_key,
            provider_id=provider_id,
            display_name=display_name,
            supported_models=supported_models or [],
            auth_type=auth_type,
            source="official",
            gateway_ref=gateway_ref,
            status=status,
            default_model=default_model or None,
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.model_created",
            payload={
                "model_key": model_key,
                "provider_id": provider_id,
                "display_name": display_name,
                "auth_type": auth_type,
                "gateway_ref": gateway_ref,
                "status": status,
                "default_model": default_model or None,
            },
        )
        return self.database.get_official_model(model_key)

    def set_status(self, model_key: str, status: str) -> dict[str, Any]:
        """Enable / disable an official model. Raises ``KeyError`` if absent."""
        if not is_valid_model_status(status):
            raise ValueError(f"不支持的模型状态 {status!r}（仅 active|inactive）")
        if self.database.get_official_model(model_key) is None:
            raise KeyError(f"模型不存在：{model_key}")
        self.database.set_official_model_status(model_key, status)
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.model_status_changed",
            payload={"model_key": model_key, "status": status},
        )
        return self.database.get_official_model(model_key)

    def get(self, model_key: str) -> dict[str, Any]:
        """Return a single model row; raises ``KeyError`` if absent."""
        row = self.database.get_official_model(model_key)
        if row is None:
            raise KeyError(f"模型不存在：{model_key}")
        return row

    def list(self, include_inactive: bool = False) -> list[dict[str, Any]]:
        """List official models (active only unless ``include_inactive``)."""
        return self.database.list_all_official_models(include_inactive=include_inactive)
