"""Phase-1 Gate C/D/E/F — Catalog Fold Service（只读目录投影）.

把各官方资产表行投影为统一的 ``TemplateCatalogEntry``（9 字段：``template_id`` /
``version`` / ``name`` / ``description`` / ``source`` / ``status`` / ``metadata``），
实现 Gate B §2.3「Admin 只读目录输出」协议。``source`` 收窄为 ``official`` /
``marketplace``（``tenant_private`` 不进入 Admin 发布目录，见
``template-catalog-runtime-contract.md`` §1）。``ccp_*`` 聚合包出目录，不进本投影。

仅读 ``database.py``，不写、不触发任何实例化。Widget Catalog 也经本服务只读暴露
（``list_widget_catalog``），与 ``CatalogAuthoringService`` 共用同一张
``dashboard_widget_catalog`` 表（Gate C 单一真相源）。
"""
from __future__ import annotations

from typing import Any

from .catalog_constants import CATALOG_ENTRY_SOURCE
from .database import Database

# 进入 TemplateCatalogEntry 只读目录的 9 类（ccp_* 聚合包出目录，不在此列）。
SUPPORTED_ENTRY_TYPES = (
    "company_template",
    "department_template",
    "employee_template",
    "workflow_content",
    "persona_template",
    "dashboard_template",
)


class CatalogFoldService:
    """把各资产表行折叠为统一 ``TemplateCatalogEntry`` 的只读服务。"""

    def __init__(self, database: Database) -> None:
        self.database = database

    # ── Widget Catalog 只读暴露（Gate C 单一真相源消费侧）─────────────────
    def list_widget_catalog(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        """读取官方 Widget Catalog（platform 全局，无租户隔离；tenant_id 保留接口兼容）。"""
        return self.database.list_widget_catalog()

    # ── TemplateCatalogEntry 投影 ─────────────────────────────────────────
    @staticmethod
    def _narrow_source(source: str | None) -> str:
        """输出协议收窄：仅 official / marketplace；其余（含 tenant_private）归 official。"""
        return source if source in CATALOG_ENTRY_SOURCE else "official"

    def fold(self, entry_type: str, row: dict[str, Any]) -> dict[str, Any]:
        """把单条资产表行折叠为 ``TemplateCatalogEntry``。

        ``entry_type`` ∈ ``SUPPORTED_ENTRY_TYPES``；未知类型 → ``ValueError``。
        """
        if entry_type == "company_template":
            return self._fold_company_template(row)
        if entry_type == "department_template":
            return self._fold_department_template(row)
        if entry_type == "employee_template":
            return self._fold_employee_template(row)
        if entry_type == "workflow_content":
            return self._fold_workflow_content(row)
        if entry_type == "persona_template":
            return self._fold_persona_template(row)
        if entry_type == "dashboard_template":
            return self._fold_dashboard_template(row)
        raise ValueError(f"不支持的目录类型 {entry_type!r}（仅 {SUPPORTED_ENTRY_TYPES}）")

    def _base(self, row: dict[str, Any], template_id: str, name: str) -> dict[str, Any]:
        return {
            "template_id": template_id,
            "version": row.get("version", "1.0.0"),
            "name": name,
            "description": row.get("description", "") or "",
            "source": self._narrow_source(row.get("source", "official")),
            "status": row.get("status", "draft"),
            "metadata": {},
        }

    def _fold_company_template(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["company_template_id"], row["name"])
        entry["metadata"] = {
            "company_type": row.get("company_type", "ai_rd"),
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    def _fold_department_template(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["id"], row["name"])
        workflow_ref = row.get("default_workflow_template_id")
        entry["metadata"] = {
            "slug": row.get("slug", ""),
            "department_type": row.get("department_type", "software_rnd"),
            "employee_template_refs": row.get("default_employee_templates", []) or [],
            "workflow_template_refs": [workflow_ref] if workflow_ref else [],
            "default_capability_types": row.get("default_capability_types", ["model", "tool", "connector"]),
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    def _fold_employee_template(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["id"], row["name"])
        entry["metadata"] = {
            "slug": row.get("slug", ""),
            "role": row.get("role", ""),
            "department_type": row.get("department_type", "software_rnd"),
            "responsibility": row.get("responsibility", "") or "",
            "persona_ref": row.get("persona_ref", "") or "",
            "default_skill": row.get("default_skill") or None,
            "default_tool": row.get("default_tool") or None,
            "default_capability_types": row.get("default_capability_types", ["model", "tool"]),
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    def _fold_workflow_content(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["workflow_content_id"], row["name"])
        entry["metadata"] = {
            "workflow_template_ref": row.get("workflow_template_ref", "") or "",
            "pack": row.get("pack", "ai_rd"),
            "owner_roles": row.get("owner_roles", []) or [],
            "step_templates": row.get("step_templates", []) or [],
            "source_attribution": row.get("source_attribution", "Curis internal"),
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    def _fold_persona_template(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["persona_id"], row["name"])
        entry["metadata"] = {
            "slug": row.get("slug", ""),
            "archetype": row.get("archetype", ""),
            "traits": row.get("traits", []) or [],
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    def _fold_dashboard_template(self, row: dict[str, Any]) -> dict[str, Any]:
        entry = self._base(row, row["dashboard_template_id"], row["name"])
        entry["metadata"] = {
            "company_type": row.get("company_type", "ai_rd"),
            "role_visibility": row.get("role_visibility", ["ceo"]) or ["ceo"],
            "widget_ids": row.get("widget_ids", []) or [],
            "layout_summary": row.get("layout_summary", "") or "",
            "data_source_refs": row.get("data_source_refs", []) or [],
            "commercial_slot_ref": row.get("commercial_slot_ref"),
            "tenant_id": row.get("tenant_id", "platform"),
        }
        return entry

    # ── 批量投影 ──────────────────────────────────────────────────────────
    def _fetch_rows(self, entry_type: str, tenant_id: str | None) -> list[dict[str, Any]]:
        """按类型从 database 读取原始行（official 内容对所有租户可见）。"""
        resolve = tenant_id or "platform"
        if entry_type == "company_template":
            return self.database.list_company_templates(tenant_id)
        if entry_type == "department_template":
            return self.database.list_department_templates(resolve, include_inactive=True)
        if entry_type == "employee_template":
            return self.database.list_employee_templates(resolve, include_inactive=True)
        if entry_type == "workflow_content":
            return self.database.list_workflow_contents(tenant_id)
        if entry_type == "persona_template":
            return self.database.list_persona_templates(tenant_id)
        if entry_type == "dashboard_template":
            return self.database.list_dashboard_templates(tenant_id)
        raise ValueError(f"不支持的目录类型 {entry_type!r}（仅 {SUPPORTED_ENTRY_TYPES}）")

    def list_catalog(
        self, entry_type: str | None = None, tenant_id: str | None = None
    ) -> dict[str, Any]:
        """折叠全部（或指定类型）官方资产为 ``TemplateCatalogEntry`` 列表。

        返回 ``{"templates": [...]}``。``entry_type`` 非空时仅折叠该类型；
        非法类型 → ``ValueError``。
        """
        if entry_type:
            if entry_type not in SUPPORTED_ENTRY_TYPES:
                raise ValueError(f"不支持的目录类型 {entry_type!r}（仅 {SUPPORTED_ENTRY_TYPES}）")
            types = [entry_type]
        else:
            types = list(SUPPORTED_ENTRY_TYPES)
        templates: list[dict[str, Any]] = []
        for t in types:
            for row in self._fetch_rows(t, tenant_id):
                templates.append(self.fold(t, row))
        return {"templates": templates}
