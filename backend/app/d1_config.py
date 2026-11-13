"""D1 toolchain configuration layer (A+B scope).

Reads environment-driven configuration for the D1 local R&D toolchain:
  - CURIS_D1_FROZEN          (bool, default "false")  kill-switch -> degrade to 503
  - CURIS_D1_WORKSPACE_ROOT  (str,  default None)      optional workspace root override
  - CURIS_ENV                (str,  default "prod")     multi-environment profile selector

Only the standard library is used; no new third-party dependencies are introduced.

Desensitization red line: every warning / log / exception message in this module is a
fixed, path-free, stack-free, key-free constant (see ``D1_UNAVAILABLE_MESSAGE``). This
module intentionally does NOT import ``local_rd_toolset`` so there is no import cycle
and no path resolution happens here.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# 统一脱敏常量：warning / 日志 / 异常文案一律使用，禁止含路径/堆栈/Key/参数值。
D1_UNAVAILABLE_MESSAGE = "D1 toolchain unavailable; service continues without it"

# 多环境 profile 表：每个 profile 仅记录「覆盖来源策略」与「解析严格度」。
# profile 不改变默认 workspace_root（默认根恒由 local_rd_toolset._DERIVED_ROOT 推导），
# 只影响覆盖位是否允许与解析严格度。缺失/非法 profile 安全回退到 "prod" + 脱敏 warning。
_D1_ENV_PROFILES: dict[str, dict[str, Any]] = {
    "dev": {"allow_override": True, "strict_root": False},
    "test": {"allow_override": True, "strict_root": True},
    "prod": {"allow_override": True, "strict_root": True},
}


# 受控执行任务类型常量：唯一被编排层允许真实执行的任务类型。
# 与 d1_single_model_toolchain.D1_TASK_ID 同值（"d1-tenant-reservation"），
# 此处独立声明以避免 d1_config 反向 import d1_single_model_toolchain（防循环依赖）。
D1_EXECUTE_TASK_TYPE = "d1-tenant-reservation"

# 叠加总开关：未拍板/未裁定前必须为 false，绝不真实调用模型网关。
# 读取自 CURIS_D1_EXECUTE_ENABLED（默认 false）。
D1_EXECUTE_ENABLED_ENV = "CURIS_D1_EXECUTE_ENABLED"


@dataclass(frozen=True)
class D1ToolchainConfig:
    """Immutable D1 toolchain configuration, resolved once at application startup."""

    frozen: bool = False
    workspace_root_override: str | None = None
    env_profile: str = "prod"
    # 受控执行总开关（范围 A）。默认 false；与 frozen 叠加，二者任一为真即整体降级。
    execute_enabled: bool = False
    # 唯一允许真实执行的任务类型；其他 task_type 一律受控拒绝（TASK_INVALID）。
    execute_task_type: str = D1_EXECUTE_TASK_TYPE


def _parse_bool(value: str | None, default: bool = False) -> bool:
    """Parse an env-var boolean with permissive truthy/falsy token handling."""
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", ""}:
        return False
    return default


def _resolve_env_profile(raw: str | None) -> str:
    """Return a valid profile name or fall back to 'prod' with a desensitized warning."""
    profile = (raw or "prod").strip().lower()
    if profile not in _D1_ENV_PROFILES:
        logger.warning(D1_UNAVAILABLE_MESSAGE)
        return "prod"
    return profile


def load_d1_config() -> D1ToolchainConfig:
    """Resolve the D1 toolchain configuration from the environment.

    The default workspace root is NOT derived here; ``local_rd_toolset`` derives it
    from its own module location (``_DERIVED_ROOT``). This function only reads the
    optional override and the frozen kill-switch, applying the selected profile's
    override-admissibility policy.

    The ``execute_enabled`` controlled-execution gate (scope A) is also read here;
    it defaults to ``False`` so that, until the security boundary seat ratifies the
    R3 credential injection, no real model-gateway call is ever attempted.
    """
    raw_frozen = os.getenv("CURIS_D1_FROZEN")
    raw_override = os.getenv("CURIS_D1_WORKSPACE_ROOT") or None
    raw_profile = os.getenv("CURIS_ENV")
    raw_execute_enabled = os.getenv(D1_EXECUTE_ENABLED_ENV)

    frozen = _parse_bool(raw_frozen, default=False)
    execute_enabled = _parse_bool(raw_execute_enabled, default=False)
    env_profile = _resolve_env_profile(raw_profile)

    profile = _D1_ENV_PROFILES[env_profile]
    # 覆盖位是否允许由 profile 策略决定；默认全部允许（真实安全兜底在 local_rd_toolset）。
    workspace_root_override: str | None = raw_override if profile["allow_override"] else None

    return D1ToolchainConfig(
        frozen=frozen,
        workspace_root_override=workspace_root_override,
        env_profile=env_profile,
        execute_enabled=execute_enabled,
        execute_task_type=D1_EXECUTE_TASK_TYPE,
    )
