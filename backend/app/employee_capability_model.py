"""P1（T09）：员工 = 能力组合模型。

把「员工」定义为一组可调用 official_models 能力的组合（而非固定 Agent 实例）。
数据落在 ``employee_capabilities`` 表（tenant_id 隔离），与既有
``employee_capability_bindings``（skill/tool 绑定）语义区分：本表绑定的是
official_models.capability_key（能力层 key）。

设计要点：
- 写/读均带 tenant_id 过滤（沿用 TenantContext.current_tenant_id()）。
- 不写死具体能力产品；员工只是「职责 + 目标 + 权限 + 项目上下文 + 记忆 + 可用能力」。
- 零新依赖（仅标准库 + TenantContext）。
"""
from __future__ import annotations

from typing import Any

from .tenant_context import TenantContext


class EmployeeCapabilityModel:
    """员工 ↔ official_models 能力组合的读写模型。"""

    def __init__(self, database: Any) -> None:
        self.database = database

    def set_employee_capabilities(
        self,
        employee_id: str,
        cap_keys: list[str],
        preferred: str | None = None,
    ) -> None:
        """设置某员工的全部可调用能力（有序）；preferred 为首选能力 key。"""
        tenant_id = TenantContext.current_tenant_id()
        self.database.replace_employee_capabilities(tenant_id, employee_id, list(cap_keys), preferred)

    def get_employee_capabilities(self, employee_id: str) -> list[str]:
        """返回某员工的可调用能力 key 列表（按 sort_order）。"""
        tenant_id = TenantContext.current_tenant_id()
        rows = self.database.list_employee_capabilities(tenant_id, employee_id)
        return [r["capability_key"] for r in rows]

    def get_employee_preferred(self, employee_id: str) -> str | None:
        """返回某员工的首选能力 key（无则返回 None）。"""
        tenant_id = TenantContext.current_tenant_id()
        row = self.database.get_employee_preferred_capability(tenant_id, employee_id)
        return row["capability_key"] if row else None


__all__ = ["EmployeeCapabilityModel"]
