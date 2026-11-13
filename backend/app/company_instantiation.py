"""Gate F — Workspace 实例化编排服务（Phase-1 Asset Factory Consolidation）。

把 ccp_* 聚合包（出厂配置）引用的 ct_/dt_/et_/wt_* 资产实例化到目标租户的
companies / department_instances / employee_instances / workflow_instances，
并为每个实例写一条 ``template_version_snapshots``（``follow_latest=0``，快照隔离）。

设计约束（docs/plan/phase1-impl-design-gate-cdef.md §5）：
- 复用既有 ``EmployeeTemplateContract.create_department_instance`` /
  ``create_employee_instance`` 原语（不新建 Employee CRUD）。
- 新租户直接创建带不可变来源快照的默认 Company；不回填既有 Company。
- persona / skill / tool 仅为目录引用：做存在性校验、不实例化
  （Persona/Skill/Tool 非实例资产）。
- 不触碰 payment / billing；``pricing_reference`` / ``quota_reference`` 仅引用，不持数值。
"""

from __future__ import annotations

import json
import uuid
from typing import Any

from .ceo_context import CeoContext
from .database import Database
from .tenant_context import TenantContext
from .employee_templates import EmployeeTemplateContract


_VERSIONED_WORKFLOW_PACKAGES = {("ccp_ai_software_company", "1.0.0")}


class CompanyInstantiationService:
    """Gate F 编排服务：把 ccp_* 出厂包实例化为租户内的公司运行态。"""

    def __init__(self, database: Database, event_log: Any) -> None:
        self.database = database
        self.event_log = event_log
        self.employees = EmployeeTemplateContract(database)

    # ── 公开编排入口 ──────────────────────────────────────────────
    def instantiate(self, ccp_id: str, tenant_id: str) -> dict[str, Any]:
        """实例化 ccp_* 出厂包到 tenant_id 租户。

        返回实例化摘要：
        ``{company_package_id, company_template_ref, company_id, tenant_id,
           departments[], employees[], workflows[], snapshots[], unresolved_refs}``。

        Raises:
            KeyError: ccp 不存在（→ 404）。
            ValueError: ccp 不可实例化 / 引用缺失的 persona 模板 / 租户无可用公司（→ 422）。
        """
        # 1. 读 ccp（平台级目录资产，tenant_id=None 不受租户过滤）
        package = self.database.get_company_package(ccp_id)
        if package is None:
            raise KeyError(f"company package {ccp_id} not found")
        status = package.get("status")
        if status != "active" or not package.get("enabled"):
            raise ValueError(f"company package {ccp_id} is not instantiable (status={status})")
        package_version = package.get("version") or ""
        if not package_version:
            raise ValueError("company package version is required")
        company_template_ref = package.get("company_template_ref") or ""

        # 2. 在目标租户作用域内确保 companies 行，并实例化各部门/员工/工作流
        with TenantContext.scope(tenant_id):
            bridge = (
                self.database.resolve_company_package_workflow_bridge(
                    ccp_id, package_version, tenant_id
                )
                if (ccp_id, package_version) in _VERSIONED_WORKFLOW_PACKAGES
                else None
            )
            self._validate_workflow_references(package, bridge)
            company_id = self._ensure_company(tenant_id, package, bridge)

            departments: list[dict[str, Any]] = []
            employees: list[dict[str, Any]] = []
            workflows: list[dict[str, Any]] = []
            snapshot_ids: list[str] = []
            # skill/tool/workflow 当前 seed 未覆盖 skl_*/tl_*/wt_*，做容错记录而非中断
            unresolved_refs: dict[str, list[str]] = {
                "skill_refs": [],
                "tool_refs": [],
                "workflow_refs": [],
            }

            # 6. persona/skill/tool 引用存在性校验（persona 严格；skill/tool 容错）
            self._validate_references(package, unresolved_refs)

            # 3. 部门实例化（dt_* → department_instances + 快照）
            for dept_ref in self._json_list(package.get("department_template_refs")):
                dept = self.employees.create_department_instance(
                    template_id=dept_ref, name="", company_id=company_id
                )
                departments.append(self._summarize_department(dept))
                snapshot = self._write_snapshot(
                    instance_id=dept["id"],
                    template_type="department",
                    template_id=dept_ref,
                    template_row=self.database.get_department_template_row(dept_ref),
                    metadata={"company_id": company_id, "name": dept.get("name", "")},
                )
                snapshot_ids.append(snapshot["id"])

            if not departments:
                raise ValueError("company package has no department template to host employees")

            # 4. 员工实例化（et_* → employee_instances + 快照）
            #    所有 et_* 挂到首个（也是唯一的）出厂部门 dt_engineering。
            host_department_id = departments[0]["id"]
            for emp_ref in self._json_list(package.get("employee_template_refs")):
                emp = self.employees.create_employee_instance(
                    department_id=host_department_id,
                    template_id=emp_ref,
                    name="",
                    company_id=company_id,
                )
                employees.append(self._summarize_employee(emp))
                snapshot = self._write_snapshot(
                    instance_id=emp["id"],
                    template_type="employee",
                    template_id=emp_ref,
                    template_row=self.database.get_employee_template_row(emp_ref),
                    metadata={
                        "company_id": company_id,
                        "department_id": emp.get("department_id", ""),
                        "persona_ref": emp.get("persona_ref", ""),
                        "default_skill": emp.get("default_skill", ""),
                        "default_tool": emp.get("default_tool", ""),
                    },
                )
                snapshot_ids.append(snapshot["id"])

            # 5. 工作流实例化（wl_* → wt_*，写 workflow_instances + 快照）
            for wl_ref in self._json_list(package.get("workflow_refs")):
                self._instantiate_workflow(
                    wl_ref,
                    company_id,
                    package,
                    bridge,
                    workflows,
                    snapshot_ids,
                )

        # 7. 记录实例化事件并返回摘要
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="company.instantiated",
            payload={
                "company_package_id": ccp_id,
                "package_version": package_version,
                "bridge_id": bridge["bridge_id"] if bridge else None,
                "workflow_template_id": bridge["workflow_template_id"] if bridge else None,
                "workflow_template_version": bridge["workflow_template_version"] if bridge else None,
                "company_template_ref": company_template_ref,
                "company_id": company_id,
                "tenant_id": tenant_id,
                "departments": len(departments),
                "employees": len(employees),
                "workflows": len(workflows),
                "snapshots": len(snapshot_ids),
            },
        )
        return {
            "company_package_id": ccp_id,
            "package_version": package_version,
            "bridge_id": bridge["bridge_id"] if bridge else None,
            "workflow_template_id": bridge["workflow_template_id"] if bridge else None,
            "workflow_template_version": bridge["workflow_template_version"] if bridge else None,
            "company_template_ref": company_template_ref,
            "company_id": company_id,
            "tenant_id": tenant_id,
            "departments": departments,
            "employees": employees,
            "workflows": workflows,
            "snapshots": snapshot_ids,
            "unresolved_refs": unresolved_refs,
        }

    # ── 内部助手 ──────────────────────────────────────────────────
    def _ensure_company(
        self,
        tenant_id: str,
        package: dict[str, Any],
        bridge: dict[str, Any] | None,
    ) -> str:
        """Create/reuse only an exactly provenanced package company."""
        expected = (
            package["company_package_id"],
            package["version"],
            bridge["bridge_id"] if bridge else None,
            bridge["workflow_template_id"] if bridge else None,
            bridge["workflow_template_version"] if bridge else None,
        )
        with self.database.connect() as connection:
            matches = connection.execute(
                """
                select company_id from companies
                where tenant_id = ?
                  and source_company_package_id = ? and source_package_version = ?
                  and source_bridge_id is ? and source_workflow_template_id is ?
                  and source_workflow_template_version is ?
                """,
                (tenant_id, *expected),
            ).fetchall()
            if len(matches) > 1:
                raise ValueError("company package provenance is ambiguous")
            if matches:
                return matches[0]["company_id"]

            is_default = not connection.execute(
                "select 1 from companies where tenant_id = ? limit 1", (tenant_id,)
            ).fetchone()
            company_id = f"company-{uuid.uuid4()}"
            connection.execute(
                """
                insert into companies (
                  company_id, tenant_id, ceo_id, name, description, company_type,
                  status, is_default, default_department_ids_json,
                  created_from_template_id, source_company_package_id,
                  source_package_version, source_bridge_id,
                  source_workflow_template_id, source_workflow_template_version,
                  updated_at
                ) values (?, ?, ?, ?, ?, 'software_rnd_company', 'active', ?, '[]',
                          ?, ?, ?, ?, ?, ?, current_timestamp)
                """,
                (
                    company_id,
                    tenant_id,
                    CeoContext.current_ceo_id() or "",
                    package.get("name") or package["company_package_id"],
                    package.get("description") or "",
                    1 if is_default else 0,
                    package.get("company_template_ref") or None,
                    *expected,
                ),
            )
        return company_id

    def _validate_workflow_references(
        self, package: dict[str, Any], bridge: dict[str, Any] | None
    ) -> None:
        """Validate every exact workflow reference before any instance write."""
        workflow_refs = self._json_list(package.get("workflow_refs"))
        if bridge and workflow_refs.count(bridge["source_workflow_content_id"]) != 1:
            raise ValueError("workflow bridge source must occur exactly once in the package")
        for workflow_content_id in workflow_refs:
            content = self.database.get_workflow_content(
                workflow_content_id, TenantContext.current_tenant_id()
            )
            if (
                content is None
                or not content.get("enabled")
                or content.get("status") != "active"
                or not content.get("version")
            ):
                raise ValueError("company package workflow content is not available")
            target_id = content.get("workflow_template_ref") or ""
            target_version = content["version"]
            if bridge and workflow_content_id == bridge["source_workflow_content_id"]:
                if content["version"] != bridge["source_workflow_content_version"]:
                    raise ValueError("workflow bridge source version does not match")
                target_id = bridge["workflow_template_id"]
                target_version = bridge["workflow_template_version"]
            target = self.database.get_official_workflow_template_version(
                target_id, target_version
            )
            if target is None:
                raise ValueError("company package workflow target version is not available")

    def _validate_references(
        self, package: dict[str, Any], unresolved_refs: dict[str, list[str]]
    ) -> None:
        """persona 严格校验；skill/tool 容错记录（当前 seed 未覆盖 skl_*/tl_*）。"""
        persona_refs = self._json_list(package.get("persona_refs"))
        missing_personas = [
            ref for ref in persona_refs if self.database.get_persona_template(ref) is None
        ]
        if missing_personas:
            raise ValueError(
                f"company package references missing persona templates: {missing_personas}"
            )
        for ref in self._json_list(package.get("skill_refs")):
            if not self._skill_exists(ref):
                unresolved_refs["skill_refs"].append(ref)
        for ref in self._json_list(package.get("tool_refs")):
            if not self._tool_exists(ref):
                unresolved_refs["tool_refs"].append(ref)

    def _instantiate_workflow(
        self,
        wl_ref: str,
        company_id: str,
        package: dict[str, Any],
        bridge: dict[str, Any] | None,
        workflows: list[dict[str, Any]],
        snapshot_ids: list[str],
    ) -> None:
        """wl_* 工作流内容 → wt_* 工作流实例（workflow_instances + 快照）。"""
        content = self.database.get_workflow_content(
            wl_ref, TenantContext.current_tenant_id()
        )
        if content is None:
            raise ValueError("company package workflow content is not available")
        bridged = bool(bridge and wl_ref == bridge["source_workflow_content_id"])
        if bridged and bridge:
            wt_ref = bridge["workflow_template_id"]
            wt_version = bridge["workflow_template_version"]
        else:
            wt_ref = content.get("workflow_template_ref") or ""
            wt_version = content["version"]
        instance_id = self._create_workflow_instance(
            company_id=company_id,
            workflow_template_id=wt_ref,
            workflow_template_version=wt_version,
            name=content.get("name") or wl_ref,
            created_from_template_id=wl_ref,
            company_package_id=package["company_package_id"],
            package_version=package["version"],
            bridge_id=bridge["bridge_id"] if bridged and bridge else None,
        )
        workflows.append(
            {
                "workflow_instance_id": instance_id,
                "workflow_template_id": wt_ref,
                "workflow_content_ref": wl_ref,
                "workflow_template_version": wt_version,
                "bridge_id": bridge["bridge_id"] if bridged and bridge else None,
                "name": content.get("name") or wl_ref,
            }
        )
        snapshot = self._write_snapshot(
            instance_id=instance_id,
            template_type="workflow",
            template_id=wt_ref or wl_ref,
            template_row=None,
            version=wt_version,
            metadata={
                "workflow_content_ref": wl_ref,
                "company_package_id": package["company_package_id"],
                "package_version": package["version"],
                "bridge_id": bridge["bridge_id"] if bridged and bridge else None,
                "workflow_template_version": wt_version,
                "name": content.get("name") or wl_ref,
            },
        )
        snapshot_ids.append(snapshot["id"])

    def _create_workflow_instance(
        self,
        *,
        company_id: str,
        workflow_template_id: str,
        workflow_template_version: str,
        name: str,
        created_from_template_id: str,
        company_package_id: str,
        package_version: str,
        bridge_id: str | None,
    ) -> str:
        """写一条 workflow_instances（对齐 workflow_runtime.run_workflow 的插入列）。"""
        instance_id = f"wfi-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into workflow_instances (
                  workflow_instance_id, tenant_id, company_id, project_id, workflow_template_id,
                  created_from_template_id, name, status,
                  source_company_package_id, source_package_version, source_bridge_id,
                  source_workflow_template_id, source_workflow_template_version, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, current_timestamp)
                """,
                (
                    instance_id,
                    TenantContext.current_tenant_id(),
                    company_id,
                    None,
                    workflow_template_id,
                    created_from_template_id,
                    name,
                    company_package_id,
                    package_version,
                    bridge_id,
                    workflow_template_id,
                    workflow_template_version,
                ),
            )
        return instance_id

    def _write_snapshot(
        self,
        *,
        instance_id: str,
        template_type: str,
        template_id: str,
        template_row: dict[str, Any] | None,
        metadata: dict[str, Any],
        version: str | None = None,
    ) -> dict[str, Any]:
        """写一条 template_version_snapshots（follow_latest=0，快照隔离）。"""
        snapshot_version = version or (template_row or {}).get("version") or "1.0.0"
        return self.database.create_template_version_snapshot(
            instance_id=instance_id,
            template_type=template_type,
            template_id=template_id,
            snapshot_version=snapshot_version,
            snapshot_metadata=metadata,
            follow_latest=False,
        )

    def _skill_exists(self, skill_id: str) -> bool:
        with _connect(self.database) as connection:
            row = connection.execute(
                "select skill_template_id from skill_templates where skill_template_id = ?",
                (skill_id,),
            ).fetchone()
        return row is not None

    def _tool_exists(self, tool_id: str) -> bool:
        """工具存在性校验：同时查运行时 ``tools`` 与目录 ``tool_templates``。

        Wave 2 修复：connector 工具（如 ``tl_ai_content_social_upload``）定义在
        ``tool_templates`` 而非运行时 ``tools`` 表；旧实现只查 ``tools`` 导致
        ``tl_*`` 被标 unresolved。现两表任一命中即视为已解析。
        """
        with _connect(self.database) as connection:
            row = connection.execute(
                "select tool_template_id from tool_templates where tool_template_id = ?",
                (tool_id,),
            ).fetchone()
            if row is not None:
                return True
            row = connection.execute("select name from tools where name = ?", (tool_id,)).fetchone()
        return row is not None

    @staticmethod
    def _json_list(value: Any) -> list[Any]:
        if not value:
            return []
        if isinstance(value, list):
            return value
        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
        return parsed if isinstance(parsed, list) else []

    @staticmethod
    def _summarize_department(dept: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": dept.get("id"),
            "name": dept.get("name"),
            "department_type": dept.get("department_type"),
            "company_id": dept.get("company_id"),
            "template_id": dept.get("template_id"),
            "status": dept.get("status"),
            "enabled": dept.get("enabled"),
        }

    @staticmethod
    def _summarize_employee(emp: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": emp.get("id"),
            "name": emp.get("name"),
            "role": emp.get("role"),
            "department_id": emp.get("department_id"),
            "template_id": emp.get("template_id"),
            "company_id": emp.get("company_id"),
            "persona_ref": emp.get("persona_ref", ""),
            "default_skill": emp.get("default_skill", ""),
            "default_tool": emp.get("default_tool", ""),
            "status": emp.get("status"),
            "enabled": emp.get("enabled"),
        }


def _connect(database: Database):
    """复用 Database.connect() 上下文管理器（避免重复导入路径噪音）。"""
    return database.connect()
