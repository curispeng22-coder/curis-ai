"""Phase-1 Gate C/D/E/F — Catalog Authoring Service（Admin 供给侧写服务）.

职责：
  * **Gate C（§2.2）Widget Catalog 单一真相源**：widget 读写 + 引用完整性校验。
    Admin ``DashboardTemplate.widgets[].widget_id`` 与 Workspace 运行时 Widget
    Catalog 引用同一张 ``dashboard_widget_catalog`` 表，禁止两处各定义。
  * **Gate D（§3.3）官方模板作者端点落点**：``create_persona`` / ``create_dashboard`` /
    ``create_company_package`` / ``create_workflow_content`` / ``upsert_employee_template`` /
    ``create_company_template``（见 T03 追加实现）。

所有写经本服务进入 ``database.py``（Admin/Workspace 唯一数据交换面）；引用完整性校验
（R3）fail-closed：引用缺失 → ``KeyError``（路由层映射 404/422）。不触碰 Workspace 执行链
/ ``credential_vault``；不实现任何 billing/invoice 代码（``cmcf_*`` 收费路径严格隔离）。
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from .catalog_constants import (
    PACK_ENUM,
    TEMPLATE_STATUS,
    WIDGET_DOMAINS,
    is_valid_archetype,
    is_valid_catalog_entry_source,
    is_valid_company_package_id,
    is_valid_company_package_status,
    is_valid_company_type,
    is_valid_pack,
    is_valid_template_id,
    is_valid_template_status,
    is_valid_widget_domain,
    normalize_widget_id,
)
from .database import Database
from .evolution_event_log import EvolutionEventLog


class CatalogAuthoringService:
    """Admin 官方资产目录写服务（Gate C/D 落点）。"""

    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    # ── Gate C：Widget Catalog 单一真相源（读写 + 引用校验）─────────────────
    def list_widgets(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        """读取官方 Widget Catalog（platform 全局，无租户隔离；tenant_id 保留接口兼容）。"""
        return self.database.list_widget_catalog()

    def get_widget(self, widget_id: str, tenant_id: str | None = None) -> dict[str, Any]:
        """读取单个 widget；缺失 → ``KeyError``。"""
        row = self.database.get_widget(widget_id)
        if row is None:
            raise KeyError(f"widget 不存在：{widget_id}")
        return row

    def create_widget(
        self,
        widget_id: str,
        domain: str,
        data_class: str = "",
        title: str = "",
        description: str = "",
        source: str = "official",
        tenant_id: str = "platform",
    ) -> dict[str, Any]:
        """幂等写入（insert or ignore 语义：重复 widget_id 返回既有行）一个规范 widget。

        规则：
          * ``widget_id`` 先做别名归一（``token_cost→ai_cost`` / ``tech_risk→project_risk``）；
          * 校验 ``domain`` 属于 ``WIDGET_DOMAINS``；
          * 校验 ``source`` 属于官方目录源枚举；
          * 重复 ``widget_id`` 不报错，返回既有行。
        """
        normalized = normalize_widget_id(widget_id)
        if not normalized:
            raise ValueError("widget_id 不能为空")
        if not is_valid_widget_domain(domain):
            raise ValueError(f"不支持的 widget domain {domain!r}（仅 {WIDGET_DOMAINS}）")
        if not is_valid_catalog_entry_source(source):
            raise ValueError(f"不支持的 widget source {source!r}（仅 official/marketplace）")
        existing = self.database.get_widget(normalized)
        if existing is not None:
            return existing
        self.database.save_widget_catalog_entry(
            widget_id=normalized,
            domain=domain,
            data_class=data_class,
            title=title or normalized,
            description=description,
            source=source,
            tenant_id=tenant_id,
            enabled=True,
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.widget.created",
            payload={"widget_id": normalized, "domain": domain, "source": source},
        )
        return self.database.get_widget(normalized, tenant_id)

    def ensure_widget_exists(self, widget_id: str, tenant_id: str | None = None) -> str:
        """引用完整性校验（R3）：``widget_id`` 必须存在于 catalog，否则 ``KeyError``。

        返回归一化后的 ``widget_id``（供调用方落库），便于去重别名自动收敛。
        """
        normalized = normalize_widget_id(widget_id)
        if self.database.get_widget(normalized) is None:
            raise KeyError(f"widget_id 不存在于 Widget Catalog：{widget_id}")
        return normalized

    def validate_widget_references(
        self, widget_ids: list[str], tenant_id: str | None = None
    ) -> list[str]:
        """批量校验 widget 引用；返回归一化后的 widget_id 列表（保序）。"""
        return [self.ensure_widget_exists(wid, tenant_id) for wid in widget_ids]

    # ── Gate D：官方模板作者端点落点（§3.3）────────────────────────────────
    @staticmethod
    def _validate_prefix(template_id: str, prefix: str) -> None:
        """校验 template_id 前缀（统一走 catalog_constants 单一真相源）。"""
        if not template_id or not template_id.startswith(prefix):
            raise ValueError(f"template_id 必须以 {prefix} 开头（收到 {template_id!r}）")

    @staticmethod
    def _ensure_refs_exist(
        refs: list[str], getter, label: str
    ) -> None:
        """批量校验引用存在性（R3 fail-closed）：任一缺失 → KeyError。"""
        for ref in refs or []:
            if getter(ref) is None:
                raise KeyError(f"{label} 引用不存在：{ref}")

    def create_persona(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``pt_*`` PersonaTemplate。

        校验：``persona_id`` 前缀（pt_）、``archetype`` 枚举、``status`` 枚举。
        重复 ``persona_id`` → ``ValueError``（422）。
        """
        persona_id = payload.get("persona_id", "")
        self._validate_prefix(persona_id, "pt_")
        if self.database.get_persona_template(persona_id) is not None:
            raise ValueError(f"Persona 已存在：{persona_id}")
        archetype = payload.get("archetype", "")
        if not is_valid_archetype(archetype):
            raise ValueError(f"不支持的 archetype {archetype!r}")
        status = payload.get("status", "draft")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        self.database.save_persona_template(
            persona_id=persona_id,
            slug=payload.get("slug", ""),
            name=payload.get("name", ""),
            archetype=archetype,
            traits=payload.get("traits"),
            communication_style=payload.get("communication_style"),
            reporting_style=payload.get("reporting_style"),
            decision_style=payload.get("decision_style", "consultative"),
            collaboration_style=payload.get("collaboration_style"),
            description=payload.get("description", ""),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.persona.created",
            payload={"persona_id": persona_id, "archetype": archetype},
        )
        return self.database.get_persona_template(persona_id)

    def create_dashboard(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``dtpl_*`` DashboardTemplate。

        校验：``dashboard_template_id`` 前缀（dtpl_）、``company_type`` 枚举、
        ``status`` 枚举、``widget_ids`` 全部存在于 Widget Catalog（Gate C §2.2 R3）。
        重复 id → ``ValueError``（422）。
        """
        dashboard_template_id = payload.get("dashboard_template_id", "")
        self._validate_prefix(dashboard_template_id, "dtpl_")
        if self.database.get_dashboard_template(dashboard_template_id) is not None:
            raise ValueError(f"Dashboard 已存在：{dashboard_template_id}")
        company_type = payload.get("company_type", "ai_rd")
        if not is_valid_company_type(company_type):
            raise ValueError(f"不支持的 company_type {company_type!r}")
        status = payload.get("status", "draft")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        widget_ids = self.validate_widget_references(payload.get("widget_ids", []))
        self.database.save_dashboard_template(
            dashboard_template_id=dashboard_template_id,
            name=payload.get("name", ""),
            company_type=company_type,
            role_visibility=payload.get("role_visibility", ["ceo"]),
            widget_ids=widget_ids,
            layout_summary=payload.get("layout_summary", ""),
            data_source_refs=payload.get("data_source_refs"),
            commercial_slot_ref=payload.get("commercial_slot_ref"),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.dashboard.created",
            payload={"dashboard_template_id": dashboard_template_id, "company_type": company_type},
        )
        return self.database.get_dashboard_template(dashboard_template_id)

    def create_workflow_content(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``wl_*`` WorkflowContent（折叠进 catalog，Variant B）。

        校验：``workflow_content_id`` 前缀（wl_）、``pack`` 枚举、``status`` 枚举。
        """
        workflow_content_id = payload.get("workflow_content_id", "")
        self._validate_prefix(workflow_content_id, "wl_")
        if self.database.get_workflow_content(workflow_content_id) is not None:
            raise ValueError(f"WorkflowContent 已存在：{workflow_content_id}")
        pack = payload.get("pack", "ai_rd")
        if not is_valid_pack(pack):
            raise ValueError(f"不支持的 pack {pack!r}（仅 {PACK_ENUM}）")
        status = payload.get("status", "active")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        self.database.save_workflow_content(
            workflow_content_id=workflow_content_id,
            name=payload.get("name", ""),
            workflow_template_ref=payload.get("workflow_template_ref", ""),
            pack=pack,
            owner_roles=payload.get("owner_roles"),
            step_templates=payload.get("step_templates"),
            source_attribution=payload.get("source_attribution", "Curis internal"),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.workflow_content.created",
            payload={"workflow_content_id": workflow_content_id, "pack": pack},
        )
        return self.database.get_workflow_content(workflow_content_id)

    def create_company_template(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``ct_*`` CompanyTemplate（类型容器，最小 schema）。"""
        company_template_id = payload.get("company_template_id", "")
        self._validate_prefix(company_template_id, "ct_")
        if self.database.get_company_template(company_template_id) is not None:
            raise ValueError(f"CompanyTemplate 已存在：{company_template_id}")
        company_type = payload.get("company_type", "ai_rd")
        if not is_valid_company_type(company_type):
            raise ValueError(f"不支持的 company_type {company_type!r}")
        status = payload.get("status", "draft")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        self.database.save_company_template(
            company_template_id=company_template_id,
            name=payload.get("name", ""),
            company_type=company_type,
            description=payload.get("description", ""),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.company_template.created",
            payload={"company_template_id": company_template_id},
        )
        return self.database.get_company_template(company_template_id)

    def create_department_template(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``dt_*`` DepartmentTemplate。"""
        department_id = payload.get("id", "")
        self._validate_prefix(department_id, "dt_")
        if self.database.get_department_template_row(department_id) is not None:
            raise ValueError(f"DepartmentTemplate 已存在：{department_id}")
        status = payload.get("status", "active")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        self.database.save_department_template(
            id=department_id,
            slug=payload.get("slug", ""),
            name=payload.get("name", ""),
            department_type=payload.get("department_type", "software_rnd"),
            description=payload.get("description", ""),
            default_employee_templates=payload.get("default_employee_templates"),
            default_workflow_template_id=payload.get("default_workflow_template_id"),
            default_capability_types_json=json.dumps(payload.get("default_capability_types", ["model", "tool", "connector"]), ensure_ascii=False),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.department_template.created",
            payload={"department_id": department_id},
        )
        return self.database.get_department_template_row(department_id)

    def create_company_package(self, payload: dict[str, Any]) -> dict[str, Any]:
        """写入 ``ccp_*`` CompanyPackage（变体 C 聚合包，出目录）。

        校验：``company_package_id`` 前缀（ccp_）、``status``（Company Package 枚举）、
        ``pack`` 枚举；引用完整性（R3）：``company_template_ref`` / ``persona_refs`` /
        ``workflow_refs`` 做存在性校验（fail-closed），``employee/department/skill/tool`` refs
        做前缀格式校验（R3 允许「先发布包、后补模板」）。
        """
        company_package_id = payload.get("company_package_id", "")
        if not is_valid_company_package_id(company_package_id):
            raise ValueError(f"company_package_id 必须以 ccp_ 开头（收到 {company_package_id!r}）")
        if self.database.get_company_package(company_package_id) is not None:
            raise ValueError(f"CompanyPackage 已存在：{company_package_id}")
        status = payload.get("status", "draft")
        if not is_valid_company_package_status(status):
            raise ValueError(f"不支持的包状态 {status!r}（仅 {COMPANY_PACKAGE_STATUS}）")
        pack = payload.get("pack", "ai_rd")
        if not is_valid_pack(pack):
            raise ValueError(f"不支持的 pack {pack!r}（仅 {PACK_ENUM}）")

        company_template_ref = payload.get("company_template_ref")
        if company_template_ref:
            if self.database.get_company_template(company_template_ref) is None:
                raise KeyError(f"company_template_ref 不存在：{company_template_ref}")
        persona_refs = payload.get("persona_refs", []) or []
        self._ensure_refs_exist(persona_refs, self.database.get_persona_template, "persona_refs")
        workflow_refs = payload.get("workflow_refs", []) or []
        self._ensure_refs_exist(workflow_refs, self.database.get_workflow_content, "workflow_refs")
        for ref in (payload.get("employee_template_refs", []) or []):
            if not ref.startswith("et_"):
                raise ValueError(f"employee_template_refs 必须是 et_*：{ref}")
        for ref in (payload.get("department_template_refs", []) or []):
            if not ref.startswith("dt_"):
                raise ValueError(f"department_template_refs 必须是 dt_*：{ref}")
        for ref in (payload.get("skill_refs", []) or []):
            if not ref.startswith("skl_"):
                raise ValueError(f"skill_refs 必须是 skl_*：{ref}")
        for ref in (payload.get("tool_refs", []) or []):
            if not ref.startswith("tl_"):
                raise ValueError(f"tool_refs 必须是 tl_*：{ref}")

        self.database.save_company_package(
            company_package_id=company_package_id,
            name=payload.get("name", ""),
            description=payload.get("description", ""),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "Curis internal"),
            pack=pack,
            company_template_ref=company_template_ref,
            department_template_refs=payload.get("department_template_refs"),
            employee_template_refs=payload.get("employee_template_refs"),
            persona_refs=persona_refs,
            skill_refs=payload.get("skill_refs"),
            tool_refs=payload.get("tool_refs"),
            workflow_refs=workflow_refs,
            sub_package_refs=payload.get("sub_package_refs"),
            pricing_reference=payload.get("pricing_reference"),
            quota_reference=payload.get("quota_reference"),
            availability=payload.get("availability", "public"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.company_package.created",
            payload={"company_package_id": company_package_id, "pack": pack},
        )
        return self.database.get_company_package(company_package_id)

    def upsert_employee_template(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Upsert ``et_*`` EmployeeTemplate（官方 catalog 内容补全，含 persona_ref 等）。

        校验：``id`` 前缀（et_）、``status`` 枚举。复用 database.upsert_employee_template
        （既有行保留 created_at / 未托管列）。
        """
        employee_id = payload.get("id", "")
        self._validate_prefix(employee_id, "et_")
        status = payload.get("status", "draft")
        if not is_valid_template_status(status):
            raise ValueError(f"不支持的模板状态 {status!r}（仅 {TEMPLATE_STATUS}）")
        self.database.upsert_employee_template(
            id=employee_id,
            slug=payload.get("slug", ""),
            name=payload.get("name", ""),
            role=payload.get("role", ""),
            responsibility=payload.get("responsibility", ""),
            description=payload.get("description", ""),
            department_type=payload.get("department_type", "software_rnd"),
            default_instructions=payload.get("default_instructions", ""),
            default_capability_types_json=json.dumps(payload.get("default_capability_types", ["model", "tool"]), ensure_ascii=False),
            default_model_policy_json=json.dumps(payload.get("default_model_policy", {}), ensure_ascii=False),
            default_workflow_step_types_json=json.dumps(payload.get("default_workflow_step_types", []), ensure_ascii=False),
            guardrails_json=json.dumps(payload.get("guardrails", []), ensure_ascii=False),
            persona_ref=payload.get("persona_ref", ""),
            default_skill=payload.get("default_skill", ""),
            default_tool=payload.get("default_tool", ""),
            version=payload.get("version", "1.0.0"),
            status=status,
            source=payload.get("source", "official"),
            tenant_id=payload.get("tenant_id", "platform"),
        )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="catalog.employee_template.upserted",
            payload={"employee_id": employee_id},
        )
        return self.database.get_employee_template_row(employee_id)
