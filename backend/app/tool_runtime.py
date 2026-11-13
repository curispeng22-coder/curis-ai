from __future__ import annotations

from typing import Any

from .database import Database
from .tenant_context import TenantContext


class ToolRuntime:
    """Read-only normalized Tool Runtime projection over existing registries."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def list_tools(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            official_rows = connection.execute("select * from tools order by name").fetchall()
        official = [
            {
                "tool_runtime_id": f"official:{row['name']}",
                "tenant_id": None,
                "company_id": None,
                "name": row["name"],
                "tool_type": row["type"],
                "description": row["description"],
                "entry": row["entry"],
                "capability_source": "official",
                "capability_id": row["name"],
                "credential_ref": None,
                "created_from_template_id": row["created_from_template_id"],
                "status": "active",
                "created_at": row["created_at"],
            }
            for row in official_rows
        ]
        private = []
        for item in self.database.list_tenant_private_capabilities(
            tenant_id, capability_type="tool", include_inactive=True
        ):
            metadata = item.get("metadata") or {}
            private.append(
                {
                    "tool_runtime_id": f"tenant_private:{item['capability_id']}",
                    "tenant_id": tenant_id,
                    "company_id": metadata.get("company_id"),
                    "name": metadata.get("name") or item["display_name"] or item["capability_id"],
                    "tool_type": metadata.get("type") or "tool",
                    "description": metadata.get("description") or "",
                    "entry": "",
                    "capability_source": "tenant_private",
                    "capability_id": item["capability_id"],
                    "credential_ref": None,
                    "credential_ref_present": bool(metadata.get("config_ref")),
                    "created_from_template_id": metadata.get("created_from_template_id") or None,
                    "status": item["status"],
                    "created_at": item["created_at"],
                }
            )
        return {"tenant_id": tenant_id, "tools": [*official, *private]}

    def get_tool(self, tool_runtime_id: str) -> dict[str, Any]:
        tool = next((item for item in self.list_tools()["tools"] if item["tool_runtime_id"] == tool_runtime_id), None)
        if tool is None:
            raise KeyError("tool runtime not found")
        return tool
