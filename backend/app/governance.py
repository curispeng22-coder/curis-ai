"""两级治理（Two-Tier Governance）真实治理执行（ADR-0017 D4.impl, issue 059）。

本模块是 D4 reservation 走向实现的治理执行一步：把 ``propose_department_toggle``
从「构造内存对象」升级为持久化 ``GovernanceProposal``（status='proposed'，
tenant/CEO-scoped）；新增最小后端人工批准流 ``approve_proposal``（不解除人工批准
门控——任何落地须先经人工批准）；``apply_proposal`` 真实落地（仅当 status==
'approved'）：持久化公司部门启用态到 additive ``company_department_state``、对
D2.impl 真实 ``departments`` 执行 enabled/disabled、并经 gate 显式批准的受控写路径
向 ``evolution_events`` 写 ``governance.propose`` / ``governance.apply``（保持
ADR-0016 D3 追加写不变式）。

范围与硬约束（来自 ADR-0025 / issue 059 + ADR-0027 S4 D4.platform / issue 060）：
- D4.platform 解锁 ``manage_department_types``（真实部门类型目录 CRUD，首个写入者）
  与 ``cross_company_policy``（真实跨公司策略 / 全局护栏，依赖 S1 租户边界）；
- 解除人工批准门控 / 自动改码 全程锁定（见 ``LOCKED_ACTIONS`` 中对应两项；
  无真实实现、无调用）；
- 平台级类型新增 / 移除仍须 human-approval 门控步骤（gate 未解除）：调用方须显式提供
  ``approved_by`` 以证明人工批准，否则拒绝（PermissionError）；
- 不接外部平台、不碰凭证、不触合规面（管理后台鉴权仅为运行时令牌比对，不持久化凭证）；
- 不做 L6 经济 / ROI 度量（不回填 ROI schema 占位）；
- 不做 Employee CRUD（``employee.py`` 零触碰）；
- 不新增任何非 ``/api/platform/*`` 的 API endpoint（新增端点集中在 main.py 且须鉴权）；
- 受控写 ``evolution_events`` 仅限 ``governance.propose`` / ``governance.apply``
  （D4.impl）/ ``governance.type_created`` / ``governance.type_removed`` /
  ``governance.policy_set``（D4.platform，本切片 gate 显式批准）；其他写路径禁止；
- 不动 D1 的 ``TenantContext`` 不变式（单租户哨兵 'default'）；
- 复用 ``department_manifest.MANIFEST_FIELDS`` 7 键契约做类型定义校验（仅结构校验，
  不消费 Manifest 字段）。
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .database import Database
from .department_catalog import CompanyTopology, DepartmentCatalog, DepartmentType
from .department_manifest import MANIFEST_FIELDS
from .evolution_event_log import EvolutionEventLog
from .tenant_context import TenantContext
# B 层运行时治理边界（T08 接线点）：apply_proposal 入口的 G5–G8 业务风险呈现。
from .runtime_governance import (
    ActionContext,
    evaluate,
    load_config,
    GateDecision,
    outcome_for_letter,
)
# 真实 DecisionSink 后端机制（T-DS1 接线信号；仅类型依赖，零新依赖）。
from .decision_sink import PendingDecisionRaised


@dataclass
class GovernanceScope:
    """CEO 级治理作用域边界（只读投影，封装其 CompanyTopology）。

    不持久化 topology；仅声明「公司内配置变更 = 仅作用于该 CompanyTopology 投影」
    的不变量。``locked_actions`` 声明本切片锁定的动作（平台级 / 解除门控 / 自动改码
    / 跨公司策略），``selectable_type_keys`` 为系统级目录全量 type 的**只读清单**
    （CEO 可选/卸，但不得增删类型）。
    """

    ceo_id: str
    topology: CompanyTopology
    locked_actions: list[str] = field(default_factory=list)
    # DepartmentCatalog.list_types() 实际返回 list[DepartmentType]（非空字符串列表）。
    selectable_type_keys: list[DepartmentType] = field(default_factory=list)
    schema_version: str = "1.0"


@dataclass
class DepartmentGovernanceView:
    """公司内某部门的治理视图（投影 CEO 选定的 type 集合 + 真实启用态）。"""

    type_key: str
    display_name: str
    category: str
    enabled: bool
    quality_lines: list[str] = field(default_factory=list)  # 占位结构，不消费
    is_locked: bool = False
    requires_human_approval: bool = True  # 任何变更需人工批准（门控不解除）


@dataclass
class GovernanceProposal:
    """治理变更提案（持久化、生命周期 proposed → approved → applied）。

    ``proposal_id`` 为全局唯一主键；``tenant_id`` / ``ceo_id`` 提供租户与公司作用域；
    ``approved_by`` / ``approved_at`` / ``applied_at`` 记录人工批准流与落地留痕；
    ``status`` 仅取 'proposed' / 'approved' / 'applied' 三态；``requires_human_approval``
    恒 True（本切片不解除人工批准门控）。
    """

    proposal_id: str
    ceo_id: str
    type_key: str
    action: str
    proposed_enabled: bool
    proposed_at: str
    approved_by: str | None = None
    approved_at: str | None = None
    applied_at: str | None = None
    status: str = "proposed"  # proposed → approved → applied
    requires_human_approval: bool = True  # 恒 True（门控不解除）
    schema_version: str = "1.0"


class CompanyGovernance:
    """CEO 级治理执行（提案持久化 + 人工批准流 + apply 真实落地）。

    复用 D2 的 ``DepartmentCatalog``（目录索引 + 真实部门实例）与 ADR-0016 D3 的
    ``EvolutionEventLog``（受控治理事件写）。提案持久化于 additive
    ``governance_proposals``；落地态持久化于 additive ``company_department_state``。
    平台级动作 ``manage_department_types`` / ``cross_company_policy`` 已在 D4.platform
    解锁（真实实现）；仅「解除人工批准门控 / 自动改码」两项仍锁定
    （见 ``LOCKED_ACTIONS``）。
    """

    # 本切片仍锁定的动作（解除人工批准门控 / 自动改码）。出现于此列表仅声明锁定，
    # 不表示任何实现或调用；受控写扫描会将其作为声明白名单放行。D4.platform 已解锁
    # manage_department_types 与 cross_company_policy（见下方真实实现），故不在本列表。
    LOCKED_ACTIONS: list[str] = [
        "lift_human_approval_gate",
        "auto_modify_code",
    ]

    def __init__(self, database: Database) -> None:
        self.database = database
        # 构造注入 Database；内部复用 D2 目录索引与 ADR-0016 D3 事件日志。
        self._catalog = DepartmentCatalog(self.database)
        self._event_log = EvolutionEventLog(self.database)

    def get_governance_scope(
        self, ceo_id: str, selected_type_keys: list[str]
    ) -> GovernanceScope:
        """返回 CEO 级治理作用域：封装 CompanyTopology + 锁定动作 + 目录只读清单。

        不持久化、不写 tenant。
        """
        topology = self._catalog.assemble_company_topology(ceo_id, selected_type_keys)
        return GovernanceScope(
            ceo_id=ceo_id,
            topology=topology,
            locked_actions=list(self.LOCKED_ACTIONS),
            # selectable_type_keys = 系统级目录全量 type 只读清单（D2 list_types）
            selectable_type_keys=self._catalog.list_types(),
            schema_version="1.0",
        )

    def list_company_departments(
        self, ceo_id: str, selected_type_keys: list[str]
    ) -> list[DepartmentGovernanceView]:
        """返回公司内各部门的治理视图（投影 CEO 选定的 type 集合 + 真实启用态）。

        启用态来自 ``company_department_state``（tenant/CEO-scoped）；未有落地态的
        type 默认按 selected = enabled 处理。每个视图 ``requires_human_approval=True``
        （门控不解除）；``quality_lines`` 仅占位结构（不消费）。
        """
        tenant_id = TenantContext.current_tenant_id()
        type_lookup = {item.type_key: item for item in self._catalog.list_types()}
        # 读取本 CEO 公司内各 type 的落地启用态，投影为 type_key -> enabled 映射。
        state_rows = self.database.list_company_department_state(
            tenant_id=tenant_id, ceo_id=ceo_id
        )
        state_enabled = {row["type_key"]: bool(row["enabled"]) for row in state_rows}
        views: list[DepartmentGovernanceView] = []
        for type_key in selected_type_keys:
            dept = type_lookup.get(type_key)
            # 未有落地态 → 默认启用（selected = enabled）；有落地态 → 取真实态。
            enabled = state_enabled.get(type_key, True)
            views.append(
                DepartmentGovernanceView(
                    type_key=type_key,
                    display_name=dept.display_name if dept else "",
                    category=dept.category if dept else "",
                    enabled=enabled,
                    quality_lines=[],
                    is_locked=False,
                    requires_human_approval=True,
                )
            )
        return views

    def propose_department_toggle(
        self, ceo_id: str, type_key: str, enabled: bool, selected_type_keys: list[str]
    ) -> GovernanceProposal:
        """提案启用/停用某部门类型（持久化 + 受控治理事件写）。

        - 经 DepartmentCatalog.get_manifest(type_key) 校验 type_key 存在于
          系统级目录（索引角色）；未知 type_key 抛 KeyError。
        - 持久化 ``GovernanceProposal``（status='proposed'，tenant/CEO-scoped）。
        - 经 gate 批准写 ``governance.propose`` 事件（ADR-0016 D3 追加写不变式保持）。
        - 治理不变式：提案绑定 (ceo_id, selected_type_keys) 作用域，不得逃逸出自身
          CompanyTopology、不得改其他 CEO 拓扑、不得改系统级 department_types。
        """
        # 索引校验：type_key 必须存在于目录（get_manifest 对未知 key 返回 None）。
        manifest = self._catalog.get_manifest(type_key)
        if manifest is None:
            raise KeyError(
                f"未知部门类型 type_key={type_key!r}："
                f"不在系统级部门目录中（须先经目录校验）"
            )
        tenant_id = TenantContext.current_tenant_id()
        proposal_id = uuid.uuid4().hex
        proposed_at = datetime.now(timezone.utc).isoformat()
        # 持久化提案（status='proposed'）。
        self.database.save_governance_proposal(
            proposal_id=proposal_id,
            tenant_id=tenant_id,
            ceo_id=ceo_id,
            type_key=type_key,
            action="toggle_department",
            proposed_enabled=enabled,
            proposed_at=proposed_at,
            status="proposed",
        )
        # 受控写 governance.propose（gate 批准；保持 ADR-0016 D3 追加写不变式）。
        self._event_log.record(
            correlation_id=f"{type_key}@{ceo_id}",
            event_type="governance.propose",
            payload={
                "proposal_id": proposal_id,
                "ceo_id": ceo_id,
                "type_key": type_key,
                "proposed_enabled": enabled,
                "selected_type_keys": list(selected_type_keys),
                "status": "proposed",
            },
        )
        return GovernanceProposal(
            proposal_id=proposal_id,
            ceo_id=ceo_id,
            type_key=type_key,
            action="toggle_department",
            proposed_enabled=enabled,
            proposed_at=proposed_at,
            approved_by=None,
            approved_at=None,
            applied_at=None,
            status="proposed",
            requires_human_approval=True,
            schema_version="1.0",
        )

    def approve_proposal(self, proposal_id: str, approver: str) -> None:
        """人工批准流（最小后端，无 UI）：将提案置为 'approved'。

        记录 ``approved_by`` / ``approved_at``。仅为 apply 的前置门控步骤，本身不落地
        部门态、不写治理事件。仅 'proposed' 态可批准；未知 proposal_id 抛 KeyError；
        非 'proposed' 态（已批准/已落地）抛 ValueError。
        """
        proposal = self.database.get_governance_proposal(proposal_id)
        if proposal is None:
            raise KeyError(f"未知治理提案 proposal_id={proposal_id!r}")
        if proposal["status"] != "proposed":
            raise ValueError(
                f"提案 status={proposal['status']!r} 不可批准"
                f"（仅 'proposed' 态可进入人工批准流）"
            )
        approved_at = datetime.now(timezone.utc).isoformat()
        self.database.update_governance_proposal_status(
            proposal_id=proposal_id,
            status="approved",
            approved_by=approver,
            approved_at=approved_at,
        )

    def apply_proposal(self, proposal_id: str, decision_sink: Any = None, pending_sink: Any = None) -> None:
        """真实落地提案（仅当 status=='approved'，human-approval gate 不解除）。

        执行三步：① 持久化公司部门启用态到 additive ``company_department_state``
        （tenant/CEO-scoped，含 approved_by/approved_at/applied_at）；② 对 D2.impl
        真实 ``departments`` 执行 enabled/disabled（经 DepartmentCatalog 状态写辅助）；
        ③ 经 gate 批准写 ``governance.apply`` 事件（ADR-0016 D3 追加写不变式）。
        最后将提案置为 'applied'。

        若 status != 'approved'（未通过人工批准），抛 PermissionError——人工批准门控
        为强制步骤，本切片不解除。
        """
        proposal = self.database.get_governance_proposal(proposal_id)
        if proposal is None:
            raise KeyError(f"未知治理提案 proposal_id={proposal_id!r}")
        # B 层运行时治理 · G5–G8 业务风险呈现（不解除 A 层 human-approval 门控）。
        # 用户选 C → 中止，不进入 apply_proposal 写链路；选 A → 照常走 A 层批准流。
        # 顶层无 resume 编排：pending 信号 → fail-closed 中止（不静默误用）。
        gate_result = self._governance_present(proposal, decision_sink, pending_sink)
        if isinstance(gate_result, PendingDecisionRaised):
            return
        if not gate_result:
            return
        # human-approval gate：仅 approved 可落地（门控不解除）。
        if proposal["status"] != "approved":
            raise PermissionError(
                f"提案 status={proposal['status']!r} 未通过人工批准"
                f"（human-approval gate）：仅 'approved' 态可落地"
            )
        tenant_id = proposal["tenant_id"]
        ceo_id = proposal["ceo_id"]
        type_key = proposal["type_key"]
        enabled = bool(proposal["proposed_enabled"])
        applied_at = datetime.now(timezone.utc).isoformat()
        # ① 持久化公司部门启用态（tenant/CEO-scoped）。
        self.database.save_company_department_state(
            tenant_id=tenant_id,
            ceo_id=ceo_id,
            type_key=type_key,
            enabled=enabled,
            approved_by=proposal["approved_by"],
            approved_at=proposal["approved_at"],
            applied_at=applied_at,
        )
        # ② 对真实 departments 执行 enabled/disabled（'active'=启用 / 'disabled'=停用）。
        self._catalog.set_departments_status_by_type(
            type_key, "active" if enabled else "disabled"
        )
        # ③ 受控写 governance.apply（gate 批准；保持 ADR-0016 D3 追加写不变式）。
        self._event_log.record(
            correlation_id=f"{type_key}@{ceo_id}",
            event_type="governance.apply",
            payload={
                "proposal_id": proposal_id,
                "ceo_id": ceo_id,
                "type_key": type_key,
                "enabled": enabled,
                "applied_at": applied_at,
            },
        )
        # 提案置为 'applied'（落地完成）。
        self.database.update_governance_proposal_status(
            proposal_id=proposal_id,
            status="applied",
            approved_by=proposal["approved_by"],
            approved_at=proposal["approved_at"],
            applied_at=applied_at,
        )

    # ── B 层运行时治理 · G5–G8 业务风险呈现（不解除 A 层门控）──
    def _governance_present(
        self, proposal: dict[str, Any], decision_sink: Any, pending_sink: Any = None
    ) -> "bool | PendingDecisionRaised":
        """B 层业务风险呈现：返回 ``True``=继续，``False``=用户取消（中止写链路）；
        ``pending_sink`` 注入且需弹闸时返回 ``PendingDecisionRaised`` 信号。

        不解除 A 层 human-approval 门控；用户选 C → 中止，不进入 apply_proposal 写链路；
        选 A → 照常走 A 层批准流。
        """
        category = self._map_proposal_to_gate_category(proposal)
        config = load_config()
        action_type = {
            "G5": "billing_config",
            "G6": "marketplace",
            "G7": "permission",
            "G8": "core_asset",
        }.get(category, "core_asset")
        try:
            decision = evaluate(ActionContext(action_type=action_type), config)
        except Exception:
            decision = GateDecision(needs_gate=True, category=category, reason="evaluation_failed")
        if not decision.needs_gate:
            return True
        if pending_sink is not None:
            # 真实等用户拍板（非阻塞）：写入存储即返回 pending_id 信号。
            pending_id = pending_sink.ask(
                decision.gate,
                correlation_id=proposal.get("proposal_id", ""),
                gate_label="apply_proposal",
            )
            self._record_governance_gate(
                decision, "pending", proposal["proposal_id"], category, proposal
            )
            return PendingDecisionRaised(
                pending_id=pending_id,
                gate_label="apply_proposal",
                gate_id=getattr(decision.gate, "gate_id", ""),
            )
        if decision_sink is None:
            # 无 sink → fail-closed 默认取消（不进入 apply_proposal 写链路）。
            self._record_governance_gate(
                decision, "cancelled", proposal["proposal_id"], category, proposal
            )
            return False
        letter = decision_sink.ask(decision.gate)
        # 统一经中心映射（③）：B→simulated，A→allowed，C→cancelled，D→alternative。
        outcome = outcome_for_letter(letter)
        self._record_governance_gate(
            decision, outcome, proposal["proposal_id"], category, proposal
        )
        return letter in ("A", "B")

    @staticmethod
    def _map_proposal_to_gate_category(proposal: dict[str, Any]) -> str:
        """按 proposal 的 type_key 粗略映射到 G5–G8（仅用于业务风险呈现类别）。"""
        key = str(proposal.get("type_key", "")).lower()
        if any(token in key for token in ("billing", "price", "pay", "quota", "fee")):
            return "G5"
        if any(token in key for token in ("market", "shop", "mall")):
            return "G6"
        if any(token in key for token in ("permission", "role", "admin", "member", "employee")):
            return "G7"
        return "G8"

    def _record_governance_gate(
        self, decision: Any, outcome: str, proposal_id: str, category: str, proposal: dict[str, Any]
    ) -> None:
        """落 ``b.governance.gate`` 事件（脱敏：无路径 / Key / 参数）。"""
        try:
            self._event_log.record(
                correlation_id=f"{category}@{proposal.get('ceo_id', '')}",
                event_type="b.governance.gate",
                payload={
                    "gate_label": "apply_proposal",
                    "category": category,
                    "outcome": outcome,
                    "needs_gate": bool(getattr(decision, "needs_gate", True)),
                },
                tenant_id=proposal.get("tenant_id"),
                idempotency_key=f"{proposal_id}:b-gov:apply_proposal:{outcome}",
            )
        except Exception:  # noqa: BLE001 - 治理事件为尽力而为
            pass

    def list_governance_audit(
        self, ceo_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """治理审计只读投影（复用 ADR-0016 D3 evolution_events）。

        - 经 EvolutionEventLog.get_all() 取全量事件只读投影，按 event_type 以
          'governance.' 前缀过滤，截断至最近 limit 条。
        - 治理动作留痕为受控写路径（governance.propose / governance.apply），
          D3 追加写不变式保持。
        """
        events = self._event_log.get_all()
        audit = [
            event
            for event in events
            if str(event.get("event_type", "")).startswith("governance.")
        ]
        if limit > 0:
            audit = audit[-limit:]
        return audit

    def list_department_types(self) -> list[dict[str, Any]]:
        """列出系统级部门类型目录（含 enabled 状态）。只读投影，供平台管理后台。"""
        return self.database.list_department_types()

    # ── ADR-0017 S4 D4.platform (issue 060): 平台级部门类型目录 CRUD（解锁 LOCKED）──
    def manage_department_types(
        self,
        action: str,
        type_key: str,
        *,
        category: str = "",
        display_name: str = "",
        description: str = "",
        manifest: dict[str, Any] | None = None,
        approved_by: str | None = None,
    ) -> dict[str, Any]:
        """平台级部门类型目录 CRUD（解锁 LOCKED_ACTION，D4.platform）。

        动作：
        - ``create``：新增部门类型。校验 type_key 非空 + manifest 符合
          ``MANIFEST_FIELDS`` 7 键契约；新增须经 human-approval 门控（``approved_by``
          必须提供，否则 PermissionError —— 门控未解除）；写入 ``department_types`` +
          受控写 ``governance.type_created``。
        - ``remove``：移除部门类型。须存在（否则 KeyError）；移除须经 human-approval
          门控（``approved_by`` 必须提供）；删除行 + 受控写 ``governance.type_removed``。
        - ``edit``：编辑展示字段（display_name/description/category）；无需门控；
          无事件写。
        - ``disable`` / ``enable``：停用/启用；无需门控；无事件写（受控写清单仅
          type_created / type_removed / policy_set）。

        返回操作后的部门类型行（dict）；remove 后返回含 ``removed=True`` 的投影。
        """
        valid_actions = {"create", "remove", "edit", "disable", "enable"}
        if action not in valid_actions:
            raise ValueError(
                f"不支持的 action={action!r}（须为 {sorted(valid_actions)}）"
            )
        type_key = (type_key or "").strip()
        if not type_key:
            raise ValueError("type_key 不能为空")

        if action == "create":
            # 索引校验：type_key 不得重复（get_manifest 对未知 key 返回 None）。
            if self._catalog.get_manifest(type_key) is not None:
                raise ValueError(f"部门类型 type_key={type_key!r} 已存在")
            # 契约校验：manifest 须含 MANIFEST_FIELDS 7 键（仅结构校验，不消费字段）。
            manifest = self._validate_manifest_contract(manifest)
            # human-approval 门控：gate 未解除，新增须提供 approved_by 证明人工批准。
            if not approved_by:
                raise PermissionError(
                    "部门类型新增须经 human-approval 门控（gate 未解除）："
                    "须提供 approved_by 以证明人工批准"
                )
            manifest_json = json.dumps(manifest, ensure_ascii=False)
            self.database.save_department_type(
                type_key=type_key,
                category=category or "custom",
                display_name=display_name or type_key,
                description=description or "",
                manifest_json=manifest_json,
                manifest_schema_version="1.0",
                is_system=False,
            )
            # 受控写 governance.type_created（gate 批准；保持 ADR-0016 D3 追加写不变式）。
            self._event_log.record(
                correlation_id=f"type:{type_key}",
                event_type="governance.type_created",
                payload={
                    "type_key": type_key,
                    "category": category or "custom",
                    "display_name": display_name or type_key,
                    "approved_by": approved_by,
                    "action": "create",
                },
            )
        elif action == "remove":
            # 索引校验：type_key 必须存在（get_manifest 返回 None → KeyError）。
            if self._catalog.get_manifest(type_key) is None:
                raise KeyError(f"未知部门类型 type_key={type_key!r}（不在目录中）")
            # human-approval 门控：gate 未解除，移除须提供 approved_by 证明人工批准。
            if not approved_by:
                raise PermissionError(
                    "部门类型移除须经 human-approval 门控（gate 未解除）："
                    "须提供 approved_by 以证明人工批准"
                )
            self.database.remove_department_type(type_key)
            # 受控写 governance.type_removed（gate 批准）。
            self._event_log.record(
                correlation_id=f"type:{type_key}",
                event_type="governance.type_removed",
                payload={
                    "type_key": type_key,
                    "approved_by": approved_by,
                    "action": "remove",
                },
            )
            return {"type_key": type_key, "removed": True}
        elif action == "edit":
            if self._catalog.get_manifest(type_key) is None:
                raise KeyError(f"未知部门类型 type_key={type_key!r}（不在目录中）")
            self.database.update_department_type_fields(
                type_key=type_key,
                display_name=display_name or None,
                description=description or None,
                category=category or None,
            )
        else:  # disable / enable
            if self._catalog.get_manifest(type_key) is None:
                raise KeyError(f"未知部门类型 type_key={type_key!r}（不在目录中）")
            self.database.set_department_type_enabled(
                type_key, enabled=(action == "enable")
            )
        # 返回操作后行（create/edit/disable/enable）。
        row = self.database.get_department_type(type_key)
        return dict(row) if row is not None else {"type_key": type_key, "removed": True}

    @staticmethod
    def _validate_manifest_contract(manifest: dict[str, Any] | None) -> dict[str, Any]:
        """校验 manifest 含 ``MANIFEST_FIELDS`` 7 键契约（仅结构校验，不消费字段）。"""
        if not isinstance(manifest, dict):
            raise ValueError("manifest 必须为 dict（须含 MANIFEST_FIELDS 7 键契约）")
        missing = [key for key in MANIFEST_FIELDS if key not in manifest]
        if missing:
            raise ValueError(
                f"manifest 缺失契约键 {missing}（须含 MANIFEST_FIELDS 7 键）"
            )
        return manifest

    # ── ADR-0017 S4 D4.platform (issue 060): 跨公司策略 / 全局护栏（解锁 LOCKED）──
    def cross_company_policy(
        self,
        action: str,
        policy_key: str,
        value: Any = None,
        tenant_scope: str = "all",
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """跨公司策略 / 全局护栏配置（解锁 LOCKED_ACTION，D4.platform）。

        依赖 S1 D1.impl 租户边界：``tenant_scope`` 描述适用租户（'all' = 全局护栏，
        或具体 tenant_id）。持久化于 additive ``platform_policies``；'set' 经 gate 批准
        写 ``governance.policy_set``（保持 ADR-0016 D3 追加写不变式）。

        动作：
        - ``set``：upsert 一条策略（policy_key 唯一维度）；写 ``governance.policy_set``；
          返回该策略行。
        - ``get``：按 policy_key 取；返回 dict 或 None（无事件写）。
        - ``list``：列出策略（可按 tenant_scope 过滤为「该租户 + 全局」）；无事件写。
        - ``disable`` / ``enable``：启停某策略；无事件写（受控写清单仅 policy_set）。
        """
        valid_actions = {"set", "get", "list", "disable", "enable"}
        if action not in valid_actions:
            raise ValueError(
                f"不支持的 action={action!r}（须为 {sorted(valid_actions)}）"
            )
        tenant_scope = tenant_scope or "all"
        # list 按 tenant_scope 过滤，无需 policy_key。
        if action == "list":
            return self.database.list_platform_policies(tenant_scope=tenant_scope)
        policy_key = (policy_key or "").strip()
        if not policy_key:
            raise ValueError("policy_key 不能为空")

        if action == "set":
            payload_value = value if value is not None else {}
            policy_value = json.dumps(payload_value, ensure_ascii=False)
            self.database.save_platform_policy(
                policy_id=uuid.uuid4().hex,
                policy_key=policy_key,
                policy_value=policy_value,
                tenant_scope=tenant_scope,
                enabled=True,
            )
            # 受控写 governance.policy_set（gate 批准）。
            self._event_log.record(
                correlation_id=f"policy:{policy_key}",
                event_type="governance.policy_set",
                payload={
                    "policy_key": policy_key,
                    "tenant_scope": tenant_scope,
                    "value": payload_value,
                    "action": "set",
                },
            )
            return self.database.get_platform_policy(policy_key)
        if action == "get":
            return self.database.get_platform_policy(policy_key)
        # disable / enable
        if self.database.get_platform_policy(policy_key) is None:
            raise KeyError(f"未知策略 policy_key={policy_key!r}")
        self.database.set_platform_policy_enabled(
            policy_key, enabled=(action == "enable")
        )
        return self.database.get_platform_policy(policy_key)
