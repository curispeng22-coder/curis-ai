from __future__ import annotations

from fastapi import APIRouter

from .tenant_context import TenantContext


def build_model_gateway_workspace_router(
    database,
    model_preferences,
    usage_meter,
    default_executor,
) -> APIRouter:
    router = APIRouter()

    @router.get("/api/workspace/model-gateway")
    def get_model_gateway_summary():
        tenant_id = TenantContext.current_tenant_id()
        preference = model_preferences.read_current()
        configured = getattr(default_executor, "runtime_config_is_declared", None)
        return {
            "providers": database.list_catalog_gateways(),
            "models": preference["available_models"],
            "preference": preference["preference"],
            "runtime": {
                "configured": bool(configured()) if callable(configured) else True,
                "gateway_id": getattr(default_executor, "gateway_id", ""),
                "model_name": getattr(default_executor, "model_name", ""),
                "fallback_policy": "selected_then_default_once",
            },
            "usage": usage_meter.query(tenant_id=tenant_id, capability_type="model"),
        }

    return router
