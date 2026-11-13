from __future__ import annotations

from typing import Any

from .database import Database
from .model_gateway import redact_model_gateway_text
from .tenant_context import TenantContext


class TenantDepartmentActivation:
    """Tenant-local activation of active official department type metadata."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def read_current(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        active_keys = self._active_keys(tenant_id)
        active_set = set(active_keys)
        return {
            "tenant_id": tenant_id,
            "active_department_type_keys": active_keys,
            "department_types": [
                {
                    "type_key": row["type_key"],
                    "category": row["category"],
                    "display_name": row["display_name"],
                    "source": "official",
                    "enabled": row["type_key"] in active_set,
                }
                for row in self._active_official_department_types()
            ],
        }

    def set_current(self, department_type_keys: list[str]) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        unique_keys = list(dict.fromkeys(department_type_keys))
        allowed = {row["type_key"] for row in self._active_official_department_types()}
        invalid = [key for key in unique_keys if key not in allowed]
        if invalid:
            raise ValueError(
                "department_type_keys must reference active official department types"
            )
        activation = {
            "tenant_id": tenant_id,
            "department_type_keys": unique_keys,
            "source": "official",
        }
        self._require_metadata_only(activation)
        self.database.save_tenant_department_activations(tenant_id, unique_keys)
        return self.read_current()

    def _active_keys(self, tenant_id: str) -> list[str]:
        allowed = {row["type_key"] for row in self._active_official_department_types()}
        return [
            row["department_type_key"]
            for row in self.database.list_tenant_department_activations(tenant_id)
            if row["source"] == "official" and row["department_type_key"] in allowed
        ]

    def _active_official_department_types(self) -> list[dict[str, Any]]:
        rows = []
        for row in self.database.list_department_types():
            is_official = row.get("source") == "official" or int(row.get("is_system", 0)) == 1
            is_enabled = int(row.get("enabled", 1)) == 1
            if is_official and is_enabled:
                rows.append(row)
        return rows

    def _require_metadata_only(self, activation: dict[str, Any]) -> None:
        for key, value in activation.items():
            if redact_model_gateway_text(value) != str(value):
                raise ValueError(f"{key} must not contain secret-like material")
