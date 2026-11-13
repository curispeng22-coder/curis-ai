"""岗位级能力授权（Phase-10，Position Capability Authorization）。

岗位模板（employee_templates）声明允许的 effect_class 白名单，员工实例
（employee_instances）可实例级覆盖。授权检查：员工岗位允许集 ∩ 能力标签非空才放行；
未声明授权 = 空集 = deny-by-default；员工无岗位模板 = 放行（用户直接调用）。
默认空授权的官方专业作者仅可按当前公司文字许可核验指定模型，不取得通用 read 权限。

设计见 docs/plan/position-authorization-design.md：
- 兼容策略：内置 et_* 模板迁移回填全开；引导生成的新岗位必须显式声明。
- 授权是硬约束（先于降级求值），拒绝记录由调用方写 trace。
- 标签自动派生 + 例外覆盖：effect_class 由 catalog_constants.effect_class_for_capability
  派生；用户自定义能力 metadata 可声明，但只能收窄不能放宽（见注册层校验）。
"""

from __future__ import annotations

import json
from contextlib import nullcontext
from typing import Any

from .catalog_constants import effect_class_for_capability
from .database import Database
from .tenant_context import TenantContext

_ALL = ("read", "retrieve", "write", "exec")


class CapabilityAuthorizer:
    def __init__(self, database: Database) -> None:
        self.database = database

    def authorize(
        self,
        employee_id: str,
        capability_type: str,
        capability_name: str = "",
        *, connection=None,
    ) -> tuple[bool, str]:
        """检查员工岗位是否允许调用该能力。

        返回 (allowed, reason)。员工无岗位模板 → 放行（用户直接调用/未绑岗位）。
        """
        allowed_classes = self._allowed_classes_for_employee(employee_id, connection=connection)
        if allowed_classes is None:
            return True, "employee has no position template (unrestricted)"
        if not allowed_classes:
            if capability_type == "model" and self._professional_model_allowed(
                employee_id, capability_name, connection=connection
            ):
                return True, "Professional model is covered by current scoped Company consent"
            return False, "position declares no allowed effect classes (deny-by-default)"
        effect_class = effect_class_for_capability(capability_type, capability_name)
        if effect_class not in allowed_classes:
            return False, (
                f"position does not allow effect class '{effect_class}' "
                f"(allowed: {sorted(allowed_classes)})"
            )
        return True, "authorized"

    def _professional_model_allowed(self, employee_id, model_key, *, connection=None) -> bool:
        """A model-specific consent check; never grant a position-wide effect class."""
        from .company_execution_policy import CompanyExecutionPolicy
        from .employee_templates import EmployeeTemplateContract, PROFESSIONAL_TEAM_DEFINITIONS, WRITING_EMPLOYEE_PRESETS
        from .runtime import RuntimeScopeError

        if not model_key:
            return False
        tenant = TenantContext.current_tenant_id()
        with (nullcontext(connection) if connection is not None else self.database.connect()) as con:
            row = con.execute(
                "select e.*,t.allowed_effect_classes_json as template_effects "
                "from employee_instances e join employee_templates t on t.id=e.template_id "
                "where e.tenant_id=? and e.id=? and e.enabled=1 and e.deleted_at is null "
                "and e.status in ('idle','assigned') and e.template_id in (?,?,?,?)",
                (tenant, employee_id, *(row[0] for row in PROFESSIONAL_TEAM_DEFINITIONS.values()),
                 WRITING_EMPLOYEE_PRESETS[1]["templateId"]),
            ).fetchone()
            if row is None:
                return False
            try:
                # Malformed or explicitly configured permissions keep their existing semantics.
                if any(json.loads(row[key] or "[]") != [] for key in
                       ("allowed_effect_classes_json", "template_effects")):
                    return False
                proofs = EmployeeTemplateContract(self.database)._professional_execution_context(con, dict(row))
                if len(proofs) != 1:
                    return False
                grant = CompanyExecutionPolicy(self.database).current_grant(
                    row["company_id"], proofs[0]["workspace_id"], model_key, connection=con
                )
                return (grant["tenant_id"] == tenant and grant["company_id"] == row["company_id"]
                        and grant["workspace_id"] == proofs[0]["workspace_id"]
                        and grant["model_key"] == model_key
                        and grant["effective_system_authorization"] is True)
            except (ValueError, KeyError, TypeError, RuntimeScopeError):
                return False

    def allowed_classes_for_employee(self, employee_id: str, *, connection=None) -> set[str] | None:
        """Read in the caller's transaction when authorizing an atomic binding update."""
        return self._allowed_classes_for_employee(employee_id, connection=connection)

    def _allowed_classes_for_employee(self, employee_id: str, *, connection=None) -> set[str] | None:
        tenant_id = TenantContext.current_tenant_id()
        with (nullcontext(connection) if connection is not None else self.database.connect()) as con:
            row = con.execute(
                "select template_id, allowed_effect_classes_json from employee_instances "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (tenant_id, employee_id),
            ).fetchone()
            if row is None or not row["template_id"]:
                return None
            instance_classes = self._parse(row["allowed_effect_classes_json"])
            if instance_classes:
                return instance_classes
            template = con.execute(
                "select allowed_effect_classes_json from employee_templates where id = ?",
                (row["template_id"],),
            ).fetchone()
            if template is None:
                return None
            return self._parse(template["allowed_effect_classes_json"])

    @staticmethod
    def _parse(raw: str | None) -> set[str]:
        try:
            values = json.loads(raw or "[]")
        except (json.JSONDecodeError, TypeError):
            return set()
        if not isinstance(values, list):
            return set()
        return {str(value) for value in values if str(value) in _ALL}
