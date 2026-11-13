"""B 层运行时治理边界 · 闸评估引擎（fail-closed 默认）。

本模块是 B 层「拍板闸」的主入口，负责：

- ``ActionContext`` / ``GateDecision`` 数据结构（全工程统一返回类型）。
- ``DecisionSink`` Protocol（接线点构造时可选注入；未注入 → fail-closed 默认 C 取消）。
- ``check_autonomy_boundary``：自治白名单六条件（全满足 → 全自治、不弹闸）。
- ``evaluate`` / ``should_gate``：fail-closed 主入口（自治边界满足 → 放行；
  否则按 action_type 归类 G1–G8 → 闸 enabled 且未命中白名单 → 渲染 GatePrompt）。
- ``load_config``：tenant-scoped 配置加载别名入口。

铁律：
1. 任何评估异常 / 归类失败 → 一律当作高影响 → 弹闸（fail-closed）。
2. B 层**无权解除 A 层锁定**：本模块不 import / 调用任何解除 ``LOCKED_ACTIONS``
   的路径（``auto_modify_code`` / ``lift_human_approval_gate``）。
3. 零新第三方依赖：仅标准库 + 本项目其它标准库模块。

事件落点：闸结果经 ``EvolutionEventLog.record(event_type="b.governance.gate", ...)``
追加写；脱敏（无路径 / Key / 参数）。本模块只生成 ``GateDecision``，落库由接线点负责。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# 输入 / 输出契约
# ---------------------------------------------------------------------------
@dataclass
class ActionContext:
    """一次高影响动作的上下文（接线点构造后传入 ``evaluate``）。"""

    action_type: str  # deploy|external_send|data_delete|token_spend|
    # billing_config|marketplace|permission|core_asset|tool_call
    irreversible: bool = False
    external: bool = False
    estimated_cost: float = 0.0
    estimated_tokens: int = 0
    destination: str = ""  # G2 allow_list 匹配用
    protected_collections: tuple[str, ...] = ()  # G3 命中集合
    in_sandbox: bool = True
    in_path_whitelist: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class GateDecision:
    """``evaluate`` 的统一返回类型。"""

    needs_gate: bool
    category: str | None = None  # "G1".."G8" 或 None
    gate: Any = None  # GatePrompt | None（needs_gate=True 时填充）
    reason: str = ""  # 内部脱敏说明，绝不透给用户


# ---------------------------------------------------------------------------
# 决策吸收器协议（接线点注入；未注入 → fail-closed 默认 C 取消）
# ---------------------------------------------------------------------------
@runtime_checkable
class DecisionSink(Protocol):
    """向用户呈现 GatePrompt 并收集决策。

    返回 ``"A"``（继续）/ ``"B"``（先模拟）/ ``"C"``（取消）/ ``"D"``（换个做法）。
    """

    def ask(self, gate: Any) -> Literal["A", "B", "C", "D"]:
        ...


class AutoApproveSink:
    """非交互 / 自动化上下文用的决策吸收器：一律视为用户选 A（继续）。

    仅用于测试、verify 脚本与无人工审批的自动化流水线；真实产品路径须注入
    会真正向用户呈现 ``GatePrompt`` 并收集选择的 sink。
    """

    def ask(self, gate: Any) -> Literal["A", "B", "C", "D"]:
        return "A"


class CancellingSink:
    """非交互上下文用的决策吸收器：一律视为用户选 C（取消）。用于负向测试。"""

    def ask(self, gate: Any) -> Literal["A", "B", "C", "D"]:
        return "C"


# ---------------------------------------------------------------------------
# 配置 / 模板依赖
# ---------------------------------------------------------------------------
from .gate_prompt import GatePrompt, render_gate_prompt  # noqa: E402
from .gate_prompt_templates import GATE_BUSINESS_CATEGORY, G_CATEGORIES  # noqa: E402
from .runtime_governance_config import RuntimeGovernanceConfig, load_config  # noqa: E402


# action_type → 闸类别（G1–G8）
_ACTION_TO_GATE: dict[str, str] = {
    "deploy": "G1",
    "external_send": "G2",
    "data_delete": "G3",
    "token_spend": "G4",
    "billing_config": "G5",
    "marketplace": "G6",
    "permission": "G7",
    "core_asset": "G8",
}

# L2 冻结能力（G5–G8）对应的 action_type。
_L2_ACTION_TYPES: frozenset[str] = frozenset(
    {"billing_config", "marketplace", "permission", "core_asset"}
)

# 决策字母 → 事件 outcome。
_OUTCOME_BY_LETTER: dict[str, str] = {
    "A": "allowed",
    "B": "simulated",
    "C": "cancelled",
    "D": "alternative",
}


# ---------------------------------------------------------------------------
# 自治白名单六条件
# ---------------------------------------------------------------------------
def check_autonomy_boundary(
    action_context: ActionContext,
    config: RuntimeGovernanceConfig | None = None,
) -> bool:
    """§5.2 自治边界六条件：全满足 → True（全自治、不弹闸）；任一不满足 → False。

    1) in_sandbox / in_path_whitelist
    2) not external
    3) action_type != data_delete
    4) estimated_tokens <= budget.token_hard_limit
    5) action_type 不碰 L2（G5–G8）
    6) not irreversible
    """
    config = config or load_config()
    if not (action_context.in_sandbox and action_context.in_path_whitelist):
        return False
    if action_context.external:
        return False
    if action_context.action_type == "data_delete":
        return False
    if action_context.estimated_tokens > config.budget.token_hard_limit:
        return False
    if action_context.action_type in _L2_ACTION_TYPES:
        return False
    if action_context.irreversible:
        return False
    return True


# ---------------------------------------------------------------------------
# 归类 / 开关 / 白名单
# ---------------------------------------------------------------------------
def _classify(action_context: ActionContext) -> str | None:
    return _ACTION_TO_GATE.get(action_context.action_type)


def _is_enabled(config: RuntimeGovernanceConfig, category: str) -> bool:
    gates = config.gates
    mapping: dict[str, bool] = {
        "G1": gates.production_deploy.enabled,
        "G2": gates.external_send.enabled,
        "G3": gates.data_deletion.enabled,
        # G4 由 token 硬限自身驱动；budget.fail_closed=False 时关闭 G4 闸。
        "G4": config.budget.fail_closed,
        "G5": gates.billing_config.enabled,
        "G6": gates.marketplace.enabled,
        "G7": gates.permission_boundary.enabled,
        "G8": gates.core_asset.enabled,
    }
    return mapping.get(category, False)


def _is_whitelisted(
    config: RuntimeGovernanceConfig,
    category: str,
    action_context: ActionContext,
) -> bool:
    if action_context.action_type in config.whitelist.actions:
        return True
    if category == "G2" and action_context.destination:
        if action_context.destination in config.gates.external_send.allow_list:
            return True
    return False


# ---------------------------------------------------------------------------
# fail-closed 主入口
# ---------------------------------------------------------------------------
def evaluate(
    action_context: ActionContext,
    config: RuntimeGovernanceConfig | None = None,
) -> GateDecision:
    """fail-closed 主入口：

    ① check_autonomy_boundary==True → needs_gate=False；
    ② 否则按 action_type 归类 G1–G8；
    ③ 该闸 enabled? 命中 whitelist.actions / external_send.allow_list? → 否就不弹；
    ④ 需弹 → render_gate_prompt() 生成 GatePrompt（含禁词扫描回退）；
    ⑤ 返回 GateDecision。

    任何异常 / 归类失败 → 一律当作高影响 → 弹闸（fail-closed）。
    """
    try:
        return _evaluate_inner(action_context, config)
    except Exception:
        return GateDecision(needs_gate=True, category=None, reason="evaluation_failed")


def _evaluate_inner(
    action_context: ActionContext,
    config: RuntimeGovernanceConfig | None,
) -> GateDecision:
    config = config or load_config()

    # ① 自治白名单六条件全满足 → 全自治、不弹闸。
    if check_autonomy_boundary(action_context, config):
        return GateDecision(needs_gate=False, category=None, reason="autonomy_boundary")

    # ② 归类 G1–G8。
    category = _classify(action_context)
    if category is None:
        # 归类失败（未知 action_type）→ fail-closed 弹闸。
        return GateDecision(needs_gate=True, category=None, reason="unclassified_high_impact")

    # ③ 该闸 enabled?
    if not _is_enabled(config, category):
        return GateDecision(needs_gate=False, category=category, reason="gate_disabled")

    # ③ 命中白名单 / allow_list?
    if _is_whitelisted(config, category, action_context):
        return GateDecision(needs_gate=False, category=category, reason="whitelisted")

    # G3 仅「命中受保护集合」才弹；不命中则视为普通（可逆）写 → 放行。
    if category == "G3":
        hit = set(action_context.protected_collections) & set(
            config.gates.data_deletion.protected_collections
        )
        if not hit:
            return GateDecision(
                needs_gate=False, category=category, reason="no_protected_collection"
            )

    # G4 token 硬限：未超 → 放行；超 → 弹（warn_ratio 仅提示不阻断，此处不单独处理）。
    if category == "G4":
        if action_context.estimated_tokens <= config.budget.token_hard_limit:
            return GateDecision(needs_gate=False, category=category, reason="within_budget")
        # 超硬限 → 继续渲染 G4 闸。

    # ④ 渲染 GatePrompt（含禁词扫描回退）。
    gate: GatePrompt = render_gate_prompt(category, action_context, config)
    return GateDecision(
        needs_gate=True, category=category, gate=gate, reason="high_impact"
    )


def should_gate(
    action_context: ActionContext,
    config: RuntimeGovernanceConfig | None = None,
) -> GateDecision:
    """``GateEvaluator.should_gate`` 命名兼容别名（设计文档 §6.1）。"""
    return evaluate(action_context, config)


# 决策字母 → outcome 的工具，供接线点复用（避免重复映射）。
def outcome_for_letter(letter: str) -> str:
    return _OUTCOME_BY_LETTER.get(letter, "cancelled")


__all__ = [
    "ActionContext",
    "GateDecision",
    "DecisionSink",
    "AutoApproveSink",
    "CancellingSink",
    "check_autonomy_boundary",
    "evaluate",
    "should_gate",
    "load_config",
    "outcome_for_letter",
    "RuntimeGovernanceConfig",
    "G_CATEGORIES",
    "GATE_BUSINESS_CATEGORY",
]
