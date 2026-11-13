"""运行时能力解析器（P0 后端核心：系统级降级链）。

``CapabilityResolver`` 是 P0-4 的核心：给定任务对能力的需求（类型 / IO / 权限），
从统一能力注册表 ``CapabilityCatalog``（落 ``official_models``）中查候选能力，按
``backup_chain`` + 实时可用性（读 ``runtime_meta.live_status``，必要时调
``DevAgent.execute("")`` 探活）选出「首选 → 降级」链路中的首个可用能力，返回可执行的
``CapabilityHandle``。

设计要点（遵循架构蓝图 §1.1 / §8②）：
- **不写死具体产品**：Codex / WorkBuddy / Claude 等均作为 catalog 中某一 type 下的
  条目，解析器只按元数据（类型 + 可用性 + 降级链）选路。
- **静默自动降级**（默认 ``AUTO_DEGRADE_SILENT = True``）：首选不可用时自动切到
  backup_chain 中的下一个可用能力，不中断流程；仅当降级链耗尽 / 触及硬卡点才抛
  出 ``CapabilityExhausted``（供 pipeline_runtime 升级 CEO）。代码同时预留
  ``auto_degrade_silent=False`` 分支（任何降级都先上报，由调用方决定）。
- **与既有 ``ToolRouter`` 协同**：resolver 在其关键词初筛之上，叠加「可用性 +
  备用链」决策；``ToolRouter`` 仅作可选初筛输入，不强制依赖。
- **零新依赖**：仅 Python 标准库 + 复用 ``dev_agent`` / ``capability_catalog``。

错误结构（供 API 层映射为 409/503 + detail.reason）：
- ``CapabilityUnavailable``：非静默模式下首选不可用，需人工确认。
- ``CapabilityExhausted``：降级链耗尽 / 硬卡点，必须升级 CEO。
"""
from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from .capability_adapters import CapabilityAdapterFactory
from .capability_catalog import CapabilityCatalog
from .catalog_constants import CAPABILITY_TYPE
from .database import Database
from .evolution_event_log import EvolutionEventLog
from .tenant_context import TenantContext


# 默认静默降级开关（架构 §8② 推荐默认 True）。可被实例化参数或环境变量覆盖。
AUTO_DEGRADE_SILENT = os.environ.get("CURIS_CAPABILITY_AUTO_DEGRADE", "true").lower() != "false"

# 默认探活开关（False：保持确定性，unknown 乐观视为可用）。可被实例化参数或
# 环境变量覆盖（CURIS_CAPABILITY_PROBE=true 开启真实探活，避免外部能力挂了还
# 静默假装成功）。
PROBE_ENABLED = os.environ.get("CURIS_CAPABILITY_PROBE", "false").lower() == "true"


class CapabilityError(Exception):
    """能力解析基类异常。"""


class CapabilityUnavailable(CapabilityError):
    """非静默模式下首选能力不可用，需人工确认（应映射为 409）。"""

    def __init__(self, reason: str, cap_type: str | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.cap_type = cap_type


class CapabilityExhausted(CapabilityError):
    """降级链耗尽 / 硬卡点：必须升级 CEO（应映射为 503）。"""

    def __init__(self, reason: str, cap_type: str | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.cap_type = cap_type


@dataclass
class CapabilityRequirement:
    """任务对能力的需求描述（解析器输入）。

    Attributes:
        cap_type: 能力类型（model / tool / skill / mcp / api / cli / webhook / workflow）。
        io_schema: 期望的 IO 形态（可选，{"input": [...], "output": [...]}）。
        permissions: 所需权限（可选，如 ["repo.write"]）。
        prefer_employee_bindings: 员工首选能力 key 列表（T09 边界，仅作路由偏好）。
    """

    cap_type: str = "model"
    io_schema: dict[str, Any] = field(default_factory=dict)
    permissions: list[str] = field(default_factory=list)
    prefer_employee_bindings: list[str] = field(default_factory=list)

    def signature(self) -> str:
        """生成需求指纹（供经验沉淀 / 复用检索）。"""
        return f"{self.cap_type}"


@dataclass
class CapabilityHandle:
    """解析出的可执行能力句柄（解析器输出）。

    包装一个 ``DevAgent`` 适配器实例，暴露统一 ``execute(prompt)``。
    """

    key: str
    type: str
    adapter: Any
    backup_keys: list[str] = field(default_factory=list)
    cost: float = 0.0
    runtime_meta: dict[str, Any] = field(default_factory=dict)

    def execute(self, prompt: str) -> dict[str, Any]:
        """执行该能力（委托给底层 DevAgent 适配器）。"""
        return self.adapter.execute(prompt)


class CapabilityResolver:
    """运行时能力解析器：查 catalog → 按 backup_chain + 实时可用性选首选→降级。"""

    def __init__(
        self,
        catalog: CapabilityCatalog,
        database: Database | None = None,
        event_log: EvolutionEventLog | None = None,
        tool_router: Any | None = None,
        adapter_factory: Callable[[dict[str, Any]], Any] | None = None,
        auto_degrade_silent: bool = AUTO_DEGRADE_SILENT,
        probe_enabled: bool = PROBE_ENABLED,
    ) -> None:
        """初始化解析器。

        Args:
            catalog: 统一能力注册表（必填）。
            database: 可选，用于回写探活结果（live_status）与员工能力组合查询。
            event_log: 可选，降级事件审计（capability.degraded）。
            tool_router: 可选，关键词初筛协同输入（仅作提示，不强制）。
            adapter_factory: 可选，cap→适配器工厂；缺省 ``CapabilityAdapterFactory.build``
                （P1 重构：按 adapter_kind 分派 CLI/HTTP/MCP/Webhook/模型适配器）。
            auto_degrade_silent: 首选不可用时是否静默降级（默认 True）。
            probe_enabled: 是否对 live_status=unknown 的能力真实探活（默认 False，保持确定性）。
        """
        self.catalog = catalog
        self.database = database
        self.event_log = event_log
        self.tool_router = tool_router
        self.adapter_factory = adapter_factory or CapabilityAdapterFactory.build
        self.auto_degrade_silent = auto_degrade_silent
        self.probe_enabled = probe_enabled
        # 当前解析请求的「员工能力组合」过滤集（T09-2）；None 表示不限（全局能力池）。
        self._employee_keys: set[str] | None = None
        # Phase-10 岗位授权：员工岗位允许的 effect_class 集合；None = 无岗位模板（不限）。
        self._allowed_effect_classes: set[str] | None = None

    # ── 公共 API ──────────────────────────────────────────────────────────
    def resolve(
        self,
        req: CapabilityRequirement,
        exclude_keys: list[str] | None = None,
        employee_id: str | None = None,
        allowed_keys: set[str] | None = None,
    ) -> CapabilityHandle:
        """解析出满足需求的可执行能力句柄。

        Args:
            req: 能力需求。
            exclude_keys: 已尝试过、需跳过的能力 key（供 pipeline_runtime 自动换能力）。
            employee_id: 可选员工 ID（T09-2）。提供时，候选能力被该员工的
                ``employee_capabilities`` 组合过滤；其首选置于首位。员工组合为空
                时回退全局能力池。
            allowed_keys: 可选能力 key 白名单（Step2：部门 Manifest 的
                ``capability_set`` 落地的消费入口）。提供时，候选进一步被限制在白名单
                内。为 None 时不影响既有行为——部门层为 opt-in 接缝，不静默改写
                ADR-0017 的 reservation（仅当调用方显式传入部门能力集才生效）。

        Returns:
            CapabilityHandle（首选或降级链路中首个可用能力）。

        Raises:
            CapabilityExhausted: 降级链耗尽 / 硬卡点（静默模式）。
            CapabilityUnavailable: 首选不可用且非静默模式（需人工确认）。
        """
        # T09-2：解析员工能力组合，作为候选过滤 / 首选偏好。
        self._employee_keys = None
        # 注意：用 `is not None` 区分「未提供」（None，不改行为）与「空白名单」
        # （set()，显式禁止一切）。空 set 是 falsy，不能用 `if allowed_keys`。
        self._allowed_keys = set(allowed_keys) if allowed_keys is not None else None
        preferred_key: str | None = None
        # Phase-10 岗位授权：员工岗位允许的 effect_class 集合（None = 无岗位模板，不限）。
        self._allowed_effect_classes = None
        if employee_id and self.database is not None:
            try:
                from .employee_capability_model import EmployeeCapabilityModel

                emp_model = EmployeeCapabilityModel(self.database)
                keys = emp_model.get_employee_capabilities(employee_id)
                if keys:
                    self._employee_keys = set(keys)
                    preferred_key = emp_model.get_employee_preferred(employee_id)
            except Exception:
                self._employee_keys = None
            try:
                from .capability_authorizer import CapabilityAuthorizer

                self._allowed_effect_classes = CapabilityAuthorizer(
                    self.database
                ).allowed_classes_for_employee(employee_id)
            except Exception:
                self._allowed_effect_classes = None

        if req.cap_type not in CAPABILITY_TYPE:
            raise CapabilityUnavailable(
                reason=f"不支持的 capability type {req.cap_type!r}",
                cap_type=req.cap_type,
            )

        # 把员工首选注入需求（供 _select_primary 优先命中）。
        effective_req = req
        if preferred_key is not None:
            effective_req = CapabilityRequirement(
                cap_type=req.cap_type,
                io_schema=req.io_schema,
                permissions=req.permissions,
                prefer_employee_bindings=[preferred_key],
            )

        primary = self._select_primary(effective_req)
        if primary is None:
            if self.auto_degrade_silent:
                raise CapabilityExhausted(
                    reason=f"无可用能力（type={req.cap_type}）",
                    cap_type=req.cap_type,
                )
            raise CapabilityUnavailable(
                reason=f"无可用能力（type={req.cap_type}），需人工登记/确认",
                cap_type=req.cap_type,
            )

        chain = self._build_chain(primary, effective_req)
        tried = set(exclude_keys or [])

        chosen: dict[str, Any] | None = None
        if self.auto_degrade_silent:
            # 静默模式：沿降级链选首个可用（首选不可用则自动切备用）。
            for cap in chain:
                key = cap["capability_key"]
                if key in tried:
                    continue
                # Phase-10 岗位授权过滤（授权是硬约束，先于可用性判定）。
                if not self._authorized(cap):
                    continue
                if self._is_available(cap):
                    chosen = cap
                    break
        else:
            # 非静默模式：仅看首选（primary），不可用即上报，绝不自动降级。
            primary_key = primary["capability_key"]
            if primary_key not in tried and self._is_available(primary) and self._authorized(primary):
                chosen = primary

        if chosen is None:
            # 首选 + 降级链均不可用 / 已尝试过。
            if self.auto_degrade_silent:
                raise CapabilityExhausted(
                    reason=(
                        f"能力降级链耗尽（type={req.cap_type}，"
                        f"已尝试 {sorted(tried) or [primary['capability_key']]}）"
                    ),
                    cap_type=req.cap_type,
                )
            raise CapabilityUnavailable(
                reason=f"首选能力不可用，需人工确认（type={req.cap_type}）",
                cap_type=req.cap_type,
            )

        degraded = chosen["capability_key"] != primary["capability_key"]
        if degraded and self.auto_degrade_silent:
            self._audit_degrade(primary, chosen, req)
        adapter = self.adapter_factory(chosen)
        backup_keys = [
            c["capability_key"]
            for c in chain
            if c["capability_key"] != chosen["capability_key"]
            and c["capability_key"] not in tried
        ]
        runtime_meta = chosen.get("runtime_meta") or {}
        return CapabilityHandle(
            key=chosen["capability_key"],
            type=chosen["type"],
            adapter=adapter,
            backup_keys=backup_keys,
            cost=float(runtime_meta.get("cost_per_unit", 0.0) or 0.0),
            runtime_meta=runtime_meta,
        )

    # ── 内部：候选选择 / 链路构建 / 可用性 ─────────────────────────────────
    def _candidates(self, cap_type: str) -> list[dict[str, Any]]:
        """列出该类型下所有 active 能力（含 runtime_meta）。"""
        candidates = self.catalog.list(type_filter=cap_type, include_inactive=False)
        # T09-2：若提供了员工能力组合，仅保留该员工可调用能力（其余不可见）。
        if self._employee_keys is not None:
            candidates = [c for c in candidates if c["capability_key"] in self._employee_keys]
        # Step2：部门能力集白名单（opt-in）。仅当选调用方显式传入部门 capability_set
        # 时才生效，不静默改写 ADR-0017 reservation 的「声明不消费」语义。
        if self._allowed_keys is not None:
            candidates = [c for c in candidates if c["capability_key"] in self._allowed_keys]
        return candidates

    def _select_primary(self, req: CapabilityRequirement) -> dict[str, Any] | None:
        """选首选候选：优先员工首选绑定，其次 catalog 默认顺序首个。"""
        candidates = self._candidates(req.cap_type)
        if not candidates:
            return None
        # 员工首选能力（T09 边界：仅作偏好，不强制）。
        for pref in req.prefer_employee_bindings or []:
            for cap in candidates:
                if cap["capability_key"] == pref:
                    return cap
        # ToolRouter 关键词初筛提示（不强制，仅当存在且能缩小范围时使用首个匹配）。
        if self.tool_router is not None and getattr(req, "io_schema", None):
            pass  # 关键词初筛在 P0 仅作占位协同；主决策仍按 backup_chain + 可用性。
        return candidates[0]

    def _build_chain(
        self, primary: dict[str, Any], req: CapabilityRequirement
    ) -> list[dict[str, Any]]:
        """构造有序降级链：[primary] + backup_chain 中存在的候选（去重、保序）。"""
        chain: list[dict[str, Any]] = [primary]
        backup_chain = (primary.get("runtime_meta") or {}).get("backup_chain") or []
        seen = {primary["capability_key"]}
        for backup_key in backup_chain:
            cap = self.catalog.get(backup_key)
            if cap is None:
                continue
            if cap["capability_key"] in seen:
                continue
            if cap.get("status") == "inactive":
                continue
            seen.add(cap["capability_key"])
            chain.append(cap)
        # 若降级链未覆盖全部候选（如员工偏好之外的其他同类型能力），追加为末位备用。
        for cap in self._candidates(req.cap_type):
            if cap["capability_key"] not in seen and cap.get("status") != "inactive":
                seen.add(cap["capability_key"])
                chain.append(cap)
        return chain

    def _is_available(self, cap: dict[str, Any]) -> bool:
        """判断能力当前是否可用（读 runtime_meta.live_status）。"""
        live = (cap.get("runtime_meta") or {}).get("live_status")
        if live == "available":
            return True
        if live == "unavailable":
            return False
        # unknown / None：按需探活，否则乐观视为可用（交由执行器真实尝试）。
        if self.probe_enabled:
            return self._probe(cap)
        return True

    def _authorized(self, cap: dict[str, Any]) -> bool:
        """Phase-10 岗位授权：员工岗位允许集 ∩ 能力 effect_class 非空才放行。

        无岗位模板（None）或未启用授权（全开）时不拦截；空集（deny-by-default）
        拦截一切。能力标签自动派生（A1），不依赖 cap 是否携带 effect_class。
        """
        if self._allowed_effect_classes is None:
            return True
        from .catalog_constants import effect_class_for_capability

        effect_class = effect_class_for_capability(
            str(cap.get("type") or ""), str(cap.get("name") or "")
        )
        return effect_class in self._allowed_effect_classes

    def _probe(self, cap: dict[str, Any]) -> bool:
        """真实探活：调 DevAgent.execute("") 判 status，并回写 live_status。"""
        try:
            adapter = self.adapter_factory(cap)
            result = adapter.execute("")
        except Exception:
            available = False
        else:
            status = result.get("status", "")
            available = status in ("success",) or not (
                status in ("no_api_key", "cli_not_found", "timeout")
                or status.startswith("error")
            )
        meta = dict(cap.get("runtime_meta") or {})
        meta["live_status"] = "available" if available else "unavailable"
        if self.database is not None:
            self.database.update_capability_runtime_meta(cap["capability_key"], meta)
        return available

    def _audit_degrade(
        self,
        primary: dict[str, Any],
        chosen: dict[str, Any],
        req: CapabilityRequirement,
    ) -> None:
        """静默降级审计（写 capability.degraded 事件，复用 EvolutionEventLog）。"""
        if self.event_log is None:
            return
        try:
            self.event_log.record(
                correlation_id=str(uuid.uuid4()),
                event_type="capability.degraded",
                payload={
                    "tenant_id": TenantContext.current_tenant_id(),
                    "cap_type": req.cap_type,
                    "primary": primary["capability_key"],
                    "degraded_to": chosen["capability_key"],
                    "reason": "首选不可用，按 backup_chain 静默降级",
                },
            )
        except Exception:
            # 审计失败不阻断主流程。
            pass
