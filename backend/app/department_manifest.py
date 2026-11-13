"""部门 Manifest 缝的字段契约（ADR-0017 D2 reservation）。

本模块固定 7 个字段命名与位置，使未来 D2.impl / D3 等 slice 有稳定的接缝。
Reservation slice 本身**不主动驱动**任何行为（不解析 / 不校验 / 不消费）；
但 Step2 起，声明字段可通过显式方法被运行时**消费**（opt-in 接缝，不静默改写
reservation 语义）——仅当调用方显式把 ``capability_set`` 传入能力解析链路时才生效。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Manifest 缝的 7 个字段契约：键 -> 期望的 Python 类型。
# 任何未来 slice 只可扩展、不得改名（见 ADR-0023 共享知识）。
MANIFEST_FIELDS: dict[str, type] = {
    "capability_set": list,       # 能力集
    "tool_classes": list,         # 可用工具类
    "quality_lines": list,        # 质量线
    "output_channels": list,      # 输出通道
    "roi_schema": dict,           # ROI schema（仅结构占位，L6 禁止回填）
    "guardrail_refs": list,       # 护栏引用
    "employee_role_spec": dict,   # 员工角色 spec（仅结构占位，Employee CRUD 禁止）
}


@dataclass
class DepartmentManifest:
    """部门 Manifest 配置单元（声明-only，不消费）。

    字段均为占位空结构；本 slice 不会用其驱动工具路由、质量线或员工管理。
    """

    type_key: str
    category: str
    capability_set: list[str] = field(default_factory=list)
    tool_classes: list[str] = field(default_factory=list)
    quality_lines: list[str] = field(default_factory=list)
    output_channels: list[str] = field(default_factory=list)
    roi_schema: dict = field(default_factory=dict)           # 占位，不回填 L6
    guardrail_refs: list[str] = field(default_factory=list)
    employee_role_spec: dict = field(default_factory=dict)   # 占位，不 CRUD
    manifest_schema_version: str = "0.0"

    def filter_capabilities(self, candidate_keys: list[str]) -> list[str]:
        """Step2：把声明的 ``capability_set`` 作为白名单消费。

        返回 ``candidate_keys`` 中属于本部门能力集的子集（保序、去重）。
        调用方（如能力解析链路）显式传入候选 key 列表时才生效；本方法本身
        不读取任何外部状态，保持 reservation 的纯声明契约不被破坏。
        """
        allowed = set(self.capability_set)
        seen: set[str] = set()
        result: list[str] = []
        for key in candidate_keys:
            if key in allowed and key not in seen:
                seen.add(key)
                result.append(key)
        return result

    def to_dict(self) -> dict[str, Any]:
        """序列化为纯 dict（供未来落库 / 传输使用）。

        本 slice 不调用此方法去驱动任何行为；仅作为稳定契约位置预留。
        """
        return {
            "type_key": self.type_key,
            "category": self.category,
            "capability_set": list(self.capability_set),
            "tool_classes": list(self.tool_classes),
            "quality_lines": list(self.quality_lines),
            "output_channels": list(self.output_channels),
            "roi_schema": dict(self.roi_schema),
            "guardrail_refs": list(self.guardrail_refs),
            "employee_role_spec": dict(self.employee_role_spec),
            "manifest_schema_version": self.manifest_schema_version,
        }
