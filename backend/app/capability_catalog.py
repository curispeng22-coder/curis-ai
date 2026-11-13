"""ADR-0028 Phase-2 (issue 070/071): unified official capability catalog.

Admin-only metadata management for model / tool / connector / skill / mcp / api
/ cli / webhook / workflow capabilities, all stored in the additive-extended
``official_models`` table (issue 071 adds the ``type`` / ``name`` columns; P0
后端核心新增 ``runtime_meta_json`` 承载运行态元数据).

This module deliberately:
  * stores ONLY capability metadata (no secrets, no api_key / token columns);
  * validates ``gateway_ref`` existence for model capabilities only (fail-closed
    via ``KeyError`` -> caller maps to 422). tool / connector carry no gateway
    association, so they are stored with ``gateway_ref = ''`` and are never
    validated against a gateway;
  * NEVER imports ``model_gateway`` and NEVER performs any outbound HTTP call;
  * writes append-only ``capability.*`` audit events via ``EvolutionEventLog``;
  * reuses ``model_catalog._reject_secret_like_metadata`` to reject any
    credential-shaped payloads (same helper used by ``ModelCatalog`` / ``GatewayCatalog``);
  * P0 扩展：``create()`` 接受 ``runtime_meta``（cost/permissions/io_schema/
    backup_chain/credentials_ref/live_status），写 ``runtime_meta_json`` 列；
    ``get()`` / ``list()`` 已自动反序列化该列（见 database 读路径）。

This is additive on top of ``ModelCatalog`` (which remains for backward
compatibility with issue 065's model-specific endpoints). The two services share
the ``official_models`` table but use distinct ``capability.*`` event types
(``capability.created`` / ``capability.status_changed`` here vs.
``capability.model_created`` / ``capability.model_status_changed`` in ``ModelCatalog``).
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from .catalog_constants import (
    CAPABILITY_TYPE,
    is_valid_auth_type,
    is_valid_capability_owner_type,
    is_valid_capability_source,
    is_valid_capability_type,
    is_valid_capability_visibility,
    is_valid_credential_ref,
    is_valid_model_status,
)
from .database import Database
from .evolution_event_log import EvolutionEventLog
# Reuse the credential-shape rejection helper from ModelCatalog so all official
# catalog services reject secret-like metadata with one shared implementation.
from .model_catalog import _reject_secret_like_metadata


class CapabilityCatalog:
    """Admin unified capability (model / tool / connector) management.

    Enforces ``gateway_ref`` existence for model capabilities only (fail-closed
    via ``KeyError`` -> caller maps to 422), the ``active`` <-> ``inactive``
    state machine (no physical delete), and a globally unique ``capability_key``
    (the physical ``model_key`` PK, shared across the three types). Audit events
    ``capability.created`` / ``capability.status_changed`` are written
    append-only on every create / status change.
    """

    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    @staticmethod
    def _to_view(row: dict[str, Any]) -> dict[str, Any]:
        """Attach the ``capability_key`` alias (the physical ``model_key`` PK) so
        API responses expose a uniform field regardless of capability type."""
        row["capability_key"] = row["model_key"]
        return row

    def create(
        self,
        capability_key: str,
        type: str,
        name: str = "",
        provider_id: str = "",
        display_name: str = "",
        auth_type: str = "none",
        gateway_ref: str = "",
        supported_models: list[str] | None = None,
        status: str = "active",
        runtime_meta: dict[str, Any] | None = None,
        owner_type: str = "official",
        owner_id: str = "",
        visibility: str = "public",
        source: str = "official",
    ) -> dict[str, Any]:
        """Create a unified capability entry.

        ``capability_key`` is the physical PK (shared across model / tool /
        connector / skill / mcp / api / cli / webhook / workflow, global
        uniqueness enforced). For ``type = 'model'`` a ``gateway_ref`` MUST
        resolve to an existing ``model_gateways`` row (else ``KeyError`` -> 422,
        fail-closed, no dangling reference). tool / connector do NOT validate
        ``gateway_ref`` and are stored with ``gateway_ref = ''``. Duplicate
        ``capability_key`` -> ``ValueError`` -> 422.

        ``runtime_meta``（P0 后端核心）承载能力运行态元数据：
        ``cost_per_unit`` / ``io_schema`` / ``permissions`` / ``credentials_ref``
        （仅 ``scheme:reference`` 形态，绝不存明文）/ ``backup_chain``（降级链
        有序 key 列表）/ ``live_status``（available|unavailable|unknown）。该字段
        经 ``runtime_meta_json`` 列落库，写路径校验 credentials_ref 形态与
        backup_chain 类型，不触发任何出站调用。
        """
        if not capability_key:
            raise ValueError("capability_key 不能为空")
        if not is_valid_capability_type(type):
            raise ValueError(
                f"不支持的 capability type {type!r}（仅 {CAPABILITY_TYPE}）"
            )
        if not is_valid_auth_type(auth_type):
            raise ValueError(
                f"不支持的 auth_type {auth_type!r}（仅形状 none|oauth|apikey）"
            )
        if not is_valid_model_status(status):
            raise ValueError(f"不支持的能力状态 {status!r}（仅 active|inactive）")
        if not is_valid_capability_owner_type(owner_type):
            raise ValueError(
                f"不支持的 owner_type {owner_type!r}（仅 official|tenant|system）"
            )
        if not is_valid_capability_visibility(visibility):
            raise ValueError(
                f"不支持的 visibility {visibility!r}（仅 private|tenant|public）"
            )
        if not is_valid_capability_source(source):
            raise ValueError(
                f"不支持的 source {source!r}（仅 official_curated|user_registered|marketplace|official）"
            )

        # runtime_meta 校验：仅校验结构合法性，绝不解析/解析凭证值。
        runtime_meta = dict(runtime_meta or {})
        credentials_ref = runtime_meta.get("credentials_ref")
        if credentials_ref is not None and not is_valid_credential_ref(credentials_ref):
            raise ValueError(
                f"credentials_ref 形态非法（需 scheme:reference，如 env:OPENAI_API_KEY）：{credentials_ref!r}"
            )
        backup_chain = runtime_meta.get("backup_chain")
        if backup_chain is not None and not isinstance(backup_chain, list):
            raise ValueError("runtime_meta.backup_chain 必须为 key 列表")
        io_schema = runtime_meta.get("io_schema")
        if io_schema is not None and not isinstance(io_schema, dict):
            raise ValueError("runtime_meta.io_schema 必须为 {input, output} 结构")
        if "live_status" not in runtime_meta:
            # 缺省为 unknown，交由 resolver 首次探活刷新。
            runtime_meta["live_status"] = "unknown"

        # gateway_ref 关联校验：仅 model 类型需要，且 fail-closed（无悬空引用）。
        # 模型缺省 gateway_ref 为 'newapi'（与 ModelCatalog / 种子对齐）；若显式
        # 提供则必须存在，否则 KeyError -> 422。tool / connector 不关联网关。
        effective_gateway_ref = ""
        if type == "model":
            effective_gateway_ref = gateway_ref or "newapi"
            if self.database.get_model_gateway(effective_gateway_ref) is None:
                raise KeyError(f"gateway_ref 不存在：{effective_gateway_ref}")

        if self.database.get_official_model(capability_key) is not None:
            raise ValueError(f"能力 {capability_key} 已存在")

        resolved_name = name or capability_key
        _reject_secret_like_metadata(
            capability_key=capability_key,
            type=type,
            name=resolved_name,
            provider_id=provider_id,
            display_name=display_name,
            auth_type=auth_type,
            gateway_ref=effective_gateway_ref,
            supported_models=supported_models or [],
            runtime_meta=runtime_meta,
        )

        self.database.save_official_model(
            model_key=capability_key,
            provider_id=provider_id,
            display_name=display_name,
            supported_models=supported_models or [],
            auth_type=auth_type,
            source=source,
            gateway_ref=effective_gateway_ref,
            status=status,
            default_model=None,
            type=type,
            name=resolved_name,
            runtime_meta_json=json.dumps(runtime_meta, ensure_ascii=False),
            owner_type=owner_type,
            owner_id=owner_id,
            visibility=visibility,
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.created",
            payload={
                "capability_key": capability_key,
                "type": type,
                "name": resolved_name,
                "provider_id": provider_id,
                "display_name": display_name,
                "auth_type": auth_type,
                "gateway_ref": effective_gateway_ref,
                "status": status,
                "runtime_meta": runtime_meta,
            },
        )
        return self._to_view(self.database.get_official_model(capability_key))

    def update_runtime_meta(
        self, capability_key: str, runtime_meta: dict[str, Any]
    ) -> dict[str, Any]:
        """更新能力的运行态元数据（如 resolver 探活后回写的 live_status / backup_chain）。

        Raises:
            KeyError: 能力不存在。
        """
        if self.database.get_official_model(capability_key) is None:
            raise KeyError(f"能力不存在：{capability_key}")
        existing = self.database.get_official_model(capability_key) or {}
        merged = dict(existing.get("runtime_meta") or {})
        merged.update(runtime_meta or {})
        self.database.update_capability_runtime_meta(capability_key, merged)
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.runtime_meta_updated",
            payload={"capability_key": capability_key, "runtime_meta": merged},
        )
        return self._to_view(self.database.get_official_model(capability_key))

    def set_status(self, capability_key: str, status: str) -> dict[str, Any]:
        """Enable / disable a capability. Raises ``KeyError`` if absent."""
        if not is_valid_model_status(status):
            raise ValueError(f"不支持的能力状态 {status!r}（仅 active|inactive）")
        if self.database.get_official_model(capability_key) is None:
            raise KeyError(f"能力不存在：{capability_key}")
        self.database.set_official_model_status(capability_key, status)
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="capability.status_changed",
            payload={"capability_key": capability_key, "status": status},
        )
        return self._to_view(self.database.get_official_model(capability_key))

    def get(self, capability_key: str) -> dict[str, Any]:
        """Return a single capability row; raises ``KeyError`` if absent."""
        row = self.database.get_official_model(capability_key)
        if row is None:
            raise KeyError(f"能力不存在：{capability_key}")
        return self._to_view(row)

    def register_external_agent(
        self,
        name: str,
        kind: str,
        config: dict[str, Any] | None = None,
        backup_chain: list[str] | None = None,
        credentials_ref: str | None = None,
        provider_id: str = "external",
        display_name: str | None = None,
        status: str = "active",
    ) -> dict[str, Any]:
        """T10：把外部 Agent 作为可调用能力登记（纯配置操作，零代码改动）。

        组装 runtime_meta = {adapter_kind: kind, adapter_config: config, backup_chain,
        credentials_ref, live_status: "unknown"}，落 official_models 一条记录。
        能力 key 形如 ``ext.{name}``，type = kind（model/agent 类型被拒，仅非 model
        外部能力走此登记）。

        红线（L2）：本方法**仅**把外部 Agent 登记为能力层条目，**绝不**导入为
        Package/Department/Employee/Skill/Workflow 资产。属能力层配置化机制，已获
        愿景预授权（外部 Agent 经适配器统一接入）。

        Raises:
            ValueError: kind 非法 / 为 model|agent（应走既有模型网关登记）。
        """
        if not is_valid_capability_type(kind):
            raise ValueError(
                f"不支持的外部能力类型 {kind!r}（仅 {CAPABILITY_TYPE}）"
            )
        if kind in ("model", "agent"):
            raise ValueError(
                "register_external_agent 仅用于非 model/agent 的外部能力"
                "（cli/http/webhook/mcp/...）；model/agent 请走既有模型网关登记"
            )
        capability_key = f"ext.{name}"
        runtime_meta = {
            "adapter_kind": kind,
            "adapter_config": config or {},
            "backup_chain": backup_chain or [],
            "credentials_ref": credentials_ref,
            "live_status": "unknown",
        }
        return self.create(
            capability_key=capability_key,
            type=kind,
            name=display_name or name,
            provider_id=provider_id,
            auth_type="none",
            gateway_ref="",  # 非 model 类型不关联网关
            status=status,
            runtime_meta=runtime_meta,
        )

    def list(
        self, type_filter: str | None = None, include_inactive: bool = False
    ) -> list[dict[str, Any]]:
        """List capabilities (active only unless ``include_inactive``)."""
        return self.database.list_capabilities(
            type_filter=type_filter, include_inactive=include_inactive
        )

    def register_official(
        self,
        capability_key: str,
        type: str,
        name: str = "",
        provider_id: str = "curis",
        display_name: str = "",
        auth_type: str = "none",
        gateway_ref: str = "",
        supported_models: list[str] | None = None,
        runtime_meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """官方供给写通道（双轨之一）：Curis 团队策划的能力，owner=official、
        visibility=public、source=official_curated。

        v1 仅开放数据结构与后端写通道，无 Admin UI；未来由官方目录 / Admin 调用。
        校验与 ``create`` 一致（gateway_ref 仅 model 类型校验存在性）。
        """
        return self.create(
            capability_key=capability_key,
            type=type,
            name=name,
            provider_id=provider_id,
            display_name=display_name,
            auth_type=auth_type,
            gateway_ref=gateway_ref,
            supported_models=supported_models,
            status="active",
            runtime_meta=runtime_meta,
            owner_type="official",
            owner_id="",
            visibility="public",
            source="official_curated",
        )

    def list_by_owner(
        self,
        owner_type: str | None = None,
        visibility: str | None = None,
        type_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """按归属 / 可见性列出能力（官方目录浏览、租户私有筛选）。

        供未来「官方能力」页与「我的能力」页分别拉取；当前 v1 前端未区分，但数据
        层已可精确筛出双轨。
        """
        return self.database.list_capabilities_by_owner(
            owner_type=owner_type,
            visibility=visibility,
            type_filter=type_filter,
        )
