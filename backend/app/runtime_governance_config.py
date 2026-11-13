"""B 层运行时治理 · 配置 schema 与 tenant-scoped 加载。

本模块定义 ``RuntimeGovernanceConfig`` 及其嵌套 dataclass（全部用标准库
dataclass，零新依赖），并提供 ``load_config(tenant_id)``（tenant-scoped，单租户
``selfuse``）与 ``validate_config_dict()``（加载期校验，拒绝 additionalProperties
与类型/枚举错误）。

铁律值（总控 2026-07-20 拍板，不可改）：
- ``budget.token_hard_limit = 200000``
- ``gates.data_deletion.protected_collections = ("customers","orders","employees")``
- ``default_decision_policy = "ask"``

任何加载/校验失败都 **fail-closed 回退默认值**，绝不抛裸异常透路径。
"""

from __future__ import annotations

import functools
import json
import os
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# 总控拍板默认值（铁律值，不得改）
# ---------------------------------------------------------------------------
DEFAULT_SCHEMA_VERSION = "1.0"
DEFAULT_TOKEN_HARD_LIMIT = 200000
DEFAULT_PROTECTED_COLLECTIONS: tuple[str, ...] = ("customers", "orders", "employees")
DEFAULT_DECISION_POLICY = "ask"
DEFAULT_WARN_RATIO = 0.8

# 单租户 selfuse 默认配置落点（与本文件同目录）。
_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "runtime_governance_config.json",
)


# ---------------------------------------------------------------------------
# 配置数据结构（嵌套 dataclass）
# ---------------------------------------------------------------------------
@dataclass
class GateSwitch:
    """通用单开关闸（G1/G5/G6/G7/G8 共用）。"""

    enabled: bool = True


@dataclass
class ExternalSendGate:
    """G2 对外发消息 / 调外部接口闸（含白名单目的地）。"""

    enabled: bool = True
    allow_list: tuple[str, ...] = ()


@dataclass
class DataDeletionGate:
    """G3 删 / 覆盖业务数据闸（含受保护集合）。"""

    enabled: bool = True
    protected_collections: tuple[str, ...] = DEFAULT_PROTECTED_COLLECTIONS


@dataclass
class BudgetConfig:
    """G4 token / 算力预算（临时桥：以硬限对比调用方累加 token）。"""

    token_hard_limit: int = DEFAULT_TOKEN_HARD_LIMIT
    warn_ratio: float = DEFAULT_WARN_RATIO
    auto_simulate_before_send: bool = True
    fail_closed: bool = True


@dataclass
class WhitelistConfig:
    """免确认动作清单（用户显式关闸）。"""

    actions: tuple[str, ...] = ()


@dataclass
class GateConfig:
    """各高影响类别闸开关（G1–G8）。"""

    production_deploy: GateSwitch = field(default_factory=GateSwitch)
    external_send: ExternalSendGate = field(default_factory=ExternalSendGate)
    data_deletion: DataDeletionGate = field(default_factory=DataDeletionGate)
    billing_config: GateSwitch = field(default_factory=GateSwitch)
    marketplace: GateSwitch = field(default_factory=GateSwitch)
    permission_boundary: GateSwitch = field(default_factory=GateSwitch)
    core_asset: GateSwitch = field(default_factory=GateSwitch)


@dataclass
class RuntimeGovernanceConfig:
    """B 层运行时治理配置（tenant-scoped 单租户 selfuse）。"""

    schema_version: str = DEFAULT_SCHEMA_VERSION
    gates: GateConfig = field(default_factory=GateConfig)
    budget: BudgetConfig = field(default_factory=BudgetConfig)
    default_decision_policy: str = DEFAULT_DECISION_POLICY
    whitelist: WhitelistConfig = field(default_factory=WhitelistConfig)


# ---------------------------------------------------------------------------
# 校验（拒绝 additionalProperties / 类型 / 枚举错误）
# ---------------------------------------------------------------------------
def validate_config_dict(raw: dict[str, Any]) -> None:
    """校验配置 dict 是否符合 RuntimeGovernanceConfig JSON Schema。

    拒绝额外属性、类型错误、枚举错误。任何违规抛 ``ValueError``（脱敏，
    不携带路径 / 键 / 参数）。
    """
    if not isinstance(raw, dict):
        raise ValueError("runtime governance config must be an object")

    _allowed(raw, {"schema_version", "gates", "budget", "default_decision_policy", "whitelist"})

    if "schema_version" in raw and not isinstance(raw["schema_version"], str):
        raise ValueError("schema_version must be a string")

    # gates
    gates = raw.get("gates", {})
    if not isinstance(gates, dict):
        raise ValueError("gates must be an object")
    _allowed(
        gates,
        {
            "production_deploy",
            "external_send",
            "data_deletion",
            "billing_config",
            "marketplace",
            "permission_boundary",
            "core_asset",
        },
    )
    for name in ("production_deploy", "billing_config", "marketplace", "permission_boundary", "core_asset"):
        if name in gates:
            _validate_gate_switch(gates[name], name)
    if "external_send" in gates:
        _validate_external_send(gates["external_send"])
    if "data_deletion" in gates:
        _validate_data_deletion(gates["data_deletion"])

    # budget
    budget = raw.get("budget", {})
    if not isinstance(budget, dict):
        raise ValueError("budget must be an object")
    _allowed(budget, {"token_hard_limit", "warn_ratio", "auto_simulate_before_send", "fail_closed"})
    if "token_hard_limit" in budget:
        _require(budget["token_hard_limit"], int, "budget.token_hard_limit")
        if isinstance(budget["token_hard_limit"], bool) or budget["token_hard_limit"] < 1:
            raise ValueError("budget.token_hard_limit must be an integer >= 1")
    if "warn_ratio" in budget:
        _require(budget["warn_ratio"], (int, float), "budget.warn_ratio")
        if isinstance(budget["warn_ratio"], bool) or not (0 <= float(budget["warn_ratio"]) <= 1):
            raise ValueError("budget.warn_ratio must be a number in [0, 1]")
    if "auto_simulate_before_send" in budget:
        _require(budget["auto_simulate_before_send"], bool, "budget.auto_simulate_before_send")
    if "fail_closed" in budget:
        _require(budget["fail_closed"], bool, "budget.fail_closed")

    # default_decision_policy
    if "default_decision_policy" in raw:
        if raw["default_decision_policy"] not in ("ask", "simulate_first", "auto_allow_whitelisted"):
            raise ValueError("default_decision_policy must be one of ask/simulate_first/auto_allow_whitelisted")

    # whitelist
    whitelist = raw.get("whitelist", {})
    if not isinstance(whitelist, dict):
        raise ValueError("whitelist must be an object")
    _allowed(whitelist, {"actions"})
    if "actions" in whitelist:
        if not isinstance(whitelist["actions"], (list, tuple)) or not all(
            isinstance(a, str) for a in whitelist["actions"]
        ):
            raise ValueError("whitelist.actions must be a list of strings")


def _allowed(obj: dict[str, Any], keys: set[str]) -> None:
    extra = set(obj) - keys
    if extra:
        raise ValueError(f"unexpected config keys: {sorted(extra)}")


def _require(value: Any, types: Any, name: str) -> None:
    if not isinstance(value, types):
        raise ValueError(f"{name} has wrong type")


def _validate_gate_switch(node: Any, name: str) -> None:
    if not isinstance(node, dict):
        raise ValueError(f"gates.{name} must be an object")
    _allowed(node, {"enabled"})
    if "enabled" in node:
        _require(node["enabled"], bool, f"gates.{name}.enabled")


def _validate_external_send(node: Any) -> None:
    if not isinstance(node, dict):
        raise ValueError("gates.external_send must be an object")
    _allowed(node, {"enabled", "allow_list"})
    if "enabled" in node:
        _require(node["enabled"], bool, "gates.external_send.enabled")
    if "allow_list" in node:
        if not isinstance(node["allow_list"], (list, tuple)) or not all(
            isinstance(a, str) for a in node["allow_list"]
        ):
            raise ValueError("gates.external_send.allow_list must be a list of strings")


def _validate_data_deletion(node: Any) -> None:
    if not isinstance(node, dict):
        raise ValueError("gates.data_deletion must be an object")
    _allowed(node, {"enabled", "protected_collections"})
    if "enabled" in node:
        _require(node["enabled"], bool, "gates.data_deletion.enabled")
    if "protected_collections" in node:
        if not isinstance(node["protected_collections"], (list, tuple)) or not all(
            isinstance(a, str) for a in node["protected_collections"]
        ):
            raise ValueError("gates.data_deletion.protected_collections must be a list of strings")


# ---------------------------------------------------------------------------
# 从 dict 构造（带默认值）
# ---------------------------------------------------------------------------
def _config_from_dict(raw: dict[str, Any]) -> RuntimeGovernanceConfig:
    gates_raw = raw.get("gates", {}) or {}
    budget_raw = raw.get("budget", {}) or {}
    whitelist_raw = raw.get("whitelist", {}) or {}

    gates = GateConfig(
        production_deploy=GateSwitch(
            enabled=bool(gates_raw.get("production_deploy", {}).get("enabled", True))
        ),
        external_send=ExternalSendGate(
            enabled=bool(gates_raw.get("external_send", {}).get("enabled", True)),
            allow_list=tuple(gates_raw.get("external_send", {}).get("allow_list", ()) or ()),
        ),
        data_deletion=DataDeletionGate(
            enabled=bool(gates_raw.get("data_deletion", {}).get("enabled", True)),
            protected_collections=tuple(
                gates_raw.get("data_deletion", {}).get(
                    "protected_collections", DEFAULT_PROTECTED_COLLECTIONS
                )
                or DEFAULT_PROTECTED_COLLECTIONS
            ),
        ),
        billing_config=GateSwitch(
            enabled=bool(gates_raw.get("billing_config", {}).get("enabled", True))
        ),
        marketplace=GateSwitch(
            enabled=bool(gates_raw.get("marketplace", {}).get("enabled", True))
        ),
        permission_boundary=GateSwitch(
            enabled=bool(gates_raw.get("permission_boundary", {}).get("enabled", True))
        ),
        core_asset=GateSwitch(
            enabled=bool(gates_raw.get("core_asset", {}).get("enabled", True))
        ),
    )

    budget = BudgetConfig(
        token_hard_limit=int(budget_raw.get("token_hard_limit", DEFAULT_TOKEN_HARD_LIMIT)),
        warn_ratio=float(budget_raw.get("warn_ratio", DEFAULT_WARN_RATIO)),
        auto_simulate_before_send=bool(budget_raw.get("auto_simulate_before_send", True)),
        fail_closed=bool(budget_raw.get("fail_closed", True)),
    )

    return RuntimeGovernanceConfig(
        schema_version=str(raw.get("schema_version", DEFAULT_SCHEMA_VERSION)),
        gates=gates,
        budget=budget,
        default_decision_policy=str(
            raw.get("default_decision_policy", DEFAULT_DECISION_POLICY)
        ),
        whitelist=WhitelistConfig(
            actions=tuple(whitelist_raw.get("actions", ()) or ())
        ),
    )


# ---------------------------------------------------------------------------
# tenant-scoped 加载（fail-closed 回退默认）
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=8)
def load_config(tenant_id: str | None = None) -> RuntimeGovernanceConfig:
    """tenant-scoped 加载治理配置。

    - ``tenant_id`` 缺省取 ``TenantContext.current_tenant_id()``（单租户 ``selfuse``）。
    - 读 ``runtime_governance_config.json``；读取 / 解析 / 校验任一失败 →
      **fail-closed 回退默认值**，绝不抛裸异常透路径。
    """
    if tenant_id is None:
        try:
            from .tenant_context import TenantContext

            tenant_id = TenantContext.current_tenant_id()
        except Exception:
            tenant_id = "selfuse"
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        validate_config_dict(raw)
        return _config_from_dict(raw)
    except Exception:
        # fail-closed：任何异常都回退默认配置（租户隔离在当前单租户下无差异）。
        return RuntimeGovernanceConfig()


# 供测试在改完配置后清缓存使用。
def clear_config_cache() -> None:
    load_config.cache_clear()


__all__ = [
    "GateSwitch",
    "ExternalSendGate",
    "DataDeletionGate",
    "BudgetConfig",
    "WhitelistConfig",
    "GateConfig",
    "RuntimeGovernanceConfig",
    "validate_config_dict",
    "load_config",
    "clear_config_cache",
    "DEFAULT_TOKEN_HARD_LIMIT",
    "DEFAULT_PROTECTED_COLLECTIONS",
    "DEFAULT_DECISION_POLICY",
]
