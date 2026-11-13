from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .agent_conversion.seed_multisource import SKILL_MANIFEST


# 对外 6 类（原产品面）+ 4 类适配器可消费外部能力（cli/api/webhook/mcp）。
# 内核 CAPABILITY_TYPE 共 10 类（含 api 而非 http），此前前端/registry 只暴露 6 类，
# 导致 mcp/api 等「系统认得、用户摸不到」。Step1 把 4 类外部能力也暴露出来。
REGISTRY_TYPES = (
    "model", "agent", "skill", "tool", "workflow", "connector",
    "cli", "api", "webhook", "mcp",
)
_CAPABILITY_KEY = re.compile(r"^[a-z0-9][a-z0-9._-]{1,127}$")


class RegistryCapabilityIn(BaseModel):
    capability_key: str
    type: str
    name: str
    provider_id: str = ""
    model_name: str = ""
    description: str = ""
    version: str = "1.0.0"
    auth_type: str = "none"
    gateway_ref: str = ""
    io_schema: dict[str, Any] = Field(default_factory=dict)
    status: str = "active"
    # Step1：从「只登记名片」升级为「能接入」。endpoint 按类型归位到适配器的
    # adapter_config（url / server_command / command）；credential_ref 仅存
    # scheme:reference（env:/kms:/vault:），绝不接收明文密钥。
    endpoint: str = ""
    credential_ref: str = ""
    adapter_config: dict[str, Any] = Field(default_factory=dict)


class RegistryStatusIn(BaseModel):
    action: str


def build_capability_registry_router(catalog) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/capabilities/registry")

    def view(row: dict[str, Any]) -> dict[str, Any]:
        runtime_meta = row.get("runtime_meta") or {}
        return {
            "capability_key": row.get("capability_key") or row.get("model_key"),
            "type": row.get("type"),
            "name": row.get("name") or row.get("display_name"),
            "display_name": row.get("display_name") or row.get("name"),
            "provider_id": row.get("provider_id") or "",
            "source": row.get("source") or "official",
            "owner_type": row.get("owner_type") or "official",
            "owner_id": row.get("owner_id") or "",
            "visibility": row.get("visibility") or "public",
            "status": row.get("status"),
            "auth_type": row.get("auth_type") or "none",
            "gateway_ref": row.get("gateway_ref") or "",
            "model_name": row.get("default_model")
            or ((row.get("supported_models") or [""])[0]),
            "description": runtime_meta.get("description") or "",
            "version": runtime_meta.get("version") or "",
            "io_schema": runtime_meta.get("io_schema") or {},
            "live_status": runtime_meta.get("live_status") or "unknown",
            "migration_status": runtime_meta.get("migration_status") or "",
            "license": runtime_meta.get("license") or "",
            "commercial_use": runtime_meta.get("commercial_use"),
            "source_template_id": runtime_meta.get("source_template_id") or "",
            # Step1：接入信息暴露（credential_ref 仅 scheme:reference，不泄露明文）。
            "endpoint": runtime_meta.get("endpoint") or "",
            "base_url": runtime_meta.get("base_url") or "",
            "credential_ref": runtime_meta.get("credentials_ref") or "",
            "adapter_kind": runtime_meta.get("adapter_kind") or "",
            "adapter_config": runtime_meta.get("adapter_config") or {},
            "created_at": row.get("created_at"),
            "updated_at": row.get("updated_at"),
        }

    @router.get("")
    def list_registry(type: str | None = None, include_inactive: bool = True):
        if type and type not in REGISTRY_TYPES:
            raise HTTPException(status_code=422, detail="capability type is not supported")
        rows = catalog.list(type_filter=type, include_inactive=include_inactive)
        return {
            "types": list(REGISTRY_TYPES),
            "capabilities": [view(row) for row in rows if row.get("type") in REGISTRY_TYPES],
        }

    @router.post("", status_code=201)
    def create_registry_capability(payload: RegistryCapabilityIn):
        if payload.type not in REGISTRY_TYPES:
            raise HTTPException(status_code=422, detail="capability type is not supported")
        if not _CAPABILITY_KEY.fullmatch(payload.capability_key):
            raise HTTPException(status_code=422, detail="capability_key format is invalid")
        if not payload.name.strip():
            raise HTTPException(status_code=422, detail="capability name is required")
        if payload.type == "model" and not payload.model_name.strip():
            raise HTTPException(status_code=422, detail="model_name is required for model capability")
        try:
            # Step1：把前端填的 endpoint / credential_ref 归位成适配器可消费的 runtime_meta。
            endpoint = (payload.endpoint or "").strip()
            credential_ref = (payload.credential_ref or "").strip()
            adapter_config = dict(payload.adapter_config or {})
            # endpoint 按类型映射到适配器期望的 adapter_config 字段。
            if endpoint and not adapter_config:
                if payload.type == "mcp":
                    adapter_config = {"server_command": endpoint}
                elif payload.type in ("cli", "local"):
                    adapter_config = {"command": endpoint}
                elif payload.type in (
                    "api", "webhook", "connector", "tool", "skill", "workflow"
                ):
                    adapter_config = {"url": endpoint}
            # 显式声明 adapter_kind，免去工厂启发式猜测。
            # 注：目录 type 用内核的 api（非 http）；适配器 kind 用 http。
            kind_map = {
                "api": "http", "webhook": "webhook", "connector": "http",
                "mcp": "mcp", "cli": "cli", "local": "cli",
                "tool": "http", "skill": "http", "workflow": "http",
            }
            runtime_meta: dict[str, Any] = {
                "description": payload.description.strip(),
                "version": payload.version.strip(),
                "io_schema": payload.io_schema,
                "live_status": "unknown",
            }
            if endpoint:
                runtime_meta["endpoint"] = endpoint
            if credential_ref:
                runtime_meta["credentials_ref"] = credential_ref
            if adapter_config:
                runtime_meta["adapter_config"] = adapter_config
            if payload.type == "model":
                runtime_meta["adapter_kind"] = "model"
                if endpoint:
                    # 私有模型 base_url 覆盖（网关多供应商在 Step5 生效）。
                    runtime_meta["base_url"] = endpoint
            elif payload.type in kind_map:
                runtime_meta["adapter_kind"] = kind_map[payload.type]
            return view(
                catalog.create(
                    capability_key=payload.capability_key,
                    type=payload.type,
                    name=payload.name.strip(),
                    provider_id=payload.provider_id.strip(),
                    display_name=payload.name.strip(),
                    auth_type=payload.auth_type,
                    gateway_ref=payload.gateway_ref,
                    supported_models=[payload.model_name.strip()] if payload.type == "model" else [],
                    status=payload.status,
                    runtime_meta=runtime_meta,
                    # 双轨：租户自助登记一律归属 tenant / 私有 / user_registered；
                    # 官方供给不走此通道（由 register_official 写），租户无法自标 official。
                    owner_type="tenant",
                    owner_id="",
                    visibility="private",
                    source="user_registered",
                )
            )
        except (KeyError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/migrate-skills")
    def migrate_historical_skills():
        migrated = []
        skipped = []
        for skill in SKILL_MANIFEST:
            capability_key = skill["id"]
            try:
                catalog.get(capability_key)
            except KeyError:
                migrated.append(
                    view(
                        catalog.create(
                            capability_key=capability_key,
                            type="skill",
                            name=skill["name"],
                            provider_id="legacy_skill",
                            display_name=skill["name"],
                            status="inactive",
                            runtime_meta={
                                "description": skill["description"],
                                "version": "1.0.0",
                                "live_status": "unknown",
                                "migration_status": "draft_candidate",
                                "license": "NOASSERTION",
                                "commercial_use": False,
                                "source_template_id": capability_key,
                            },
                        )
                    )
                )
            else:
                skipped.append(capability_key)
        return {
            "migrated": migrated,
            "skipped": skipped,
            "migrated_count": len(migrated),
            "skipped_count": len(skipped),
        }

    @router.get("/{capability_key}")
    def get_registry_capability(capability_key: str):
        try:
            row = catalog.get(capability_key)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        if row.get("type") not in REGISTRY_TYPES:
            raise HTTPException(status_code=404, detail="capability not found")
        return view(row)

    @router.put("/{capability_key}")
    def update_registry_capability(capability_key: str, payload: RegistryStatusIn):
        if payload.action not in {"enable", "disable"}:
            raise HTTPException(status_code=422, detail="action must be enable or disable")
        try:
            current = catalog.get(capability_key)
            if (
                payload.action == "enable"
                and (current.get("runtime_meta") or {}).get("migration_status") == "draft_candidate"
            ):
                raise ValueError("historical skill requires license review before enable")
            return view(
                catalog.set_status(
                    capability_key,
                    "active" if payload.action == "enable" else "inactive",
                )
            )
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router
