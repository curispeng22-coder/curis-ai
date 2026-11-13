"""Issue A · P0-3 运行配置指纹（SHA-256）。

把影响运行结果的配置（模型网关 + 模型名、工具作用域、任务 prompt 规格、
策略参数、组件版本、以及开放 ``extra`` 旋钮）归一化为一个**稳定**的指纹摘要，
用于：缓存失效（指纹未变可跳重跑）、恢复校验（``recover`` 比对 parent 指纹）、
运行复现（会话落指纹 + ``a.kernel.*`` 事件）。

归一化规则（直译 Paperclip 算法并落地）：
1. 递归排序键（``json.dumps(sort_keys=True)`` 承担）。
2. 剔除 ``None`` / 空字符串 / 空容器。
3. 剔除噪声字段：时间戳（``timestamp`` / ``created_at`` / ``updated_at``）、
   绝对路径（``path`` / ``file_path`` / ``abs_path``）、``request_id``、
   ``run_id``、随机 ``nonce``、关联 id（``correlation_id`` / ``idempotency_key``）。
4. 脱敏 Secret：键名命中 ``api_key | secret | token | password`` 等 → 值替换为
   常量 ``"<redacted>"``，**且不随真实 Secret 值变化**（真实值不计入哈希）。

铁律（与架构设计一致）：
- 零新依赖：仅标准库（``hashlib`` / ``json`` / ``dataclasses`` / ``typing`` / ``re``）。
- 脱敏贯穿：``compute_fingerprint`` 返回的字符串是哈希摘要，本身不含任何原始
  Secret / 路径 / 参数；归一化 JSON 也仅含 ``"<redacted>"`` 占位。
- 不触 L2 / 不解除 ``LOCKED_ACTIONS``：纯函数模块，无任何治理 / 锁相关依赖。
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
FINGERPRINT_PREFIX = "sha256:"  # 与 credential_vault digest 前缀一致

# 噪声键（命中即剔除，不参与指纹）。小写匹配。
_NOISE_KEYS: frozenset[str] = frozenset(
    {
        "timestamp",
        "created_at",
        "updated_at",
        "path",
        "file_path",
        "abs_path",
        "request_id",
        "run_id",
        "nonce",
        "correlation_id",
        "idempotency_key",
        "session_id",
        "claim_id",
        "event_id",
    }
)

# Secret 键（命中即脱敏为常量占位，真实值不计入哈希）。
_SECRET_KEY_RE = re.compile(
    r"(api[_]?key|secret|token|password|passwd|pwd)", re.IGNORECASE
)

# 归一化哨兵：表示「该节点应被剔除」（与合法 ``None`` / ``0`` / ``False`` 区分）。
_DROP = object()

REDACTED = "<redacted>"


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass
class RunConfig:
    """影响运行结果的配置（确定性旋钮）。

    指纹字段集（P0-3）：模型网关 + 模型名、工具作用域（sandbox 模式 +
    允许路径）、任务 prompt 规格、策略参数（轮次 / 测试命令 / 温度）、组件版本
    （skill / tool / adapter）。明确排除：时间戳、绝对路径、request_id、run_id、
    原始 Secret、随机 nonce。``extra`` 承载其它确定性旋钮。
    """

    model_gateway_id: str  # 如 "anthropic" / "openai" / "workbuddy"
    model_name: str  # 如 "claude-sonnet-4-20250514" / "gpt-4o"
    tool_scope: dict  # {"sandbox_mode": "git", "allow_paths": [...]}
    prompt_spec: dict  # 归一化任务规格（去 run_id / 时间戳 / 绝对路径）
    strategy: dict  # {"max_rounds": 3, "test_command_id": "...", "test_command_argv": [...], "temperature": 0.0}
    component_versions: dict[str, str]  # skill/tool/adapter 版本标签（影响结果）
    extra: dict = field(default_factory=dict)  # 其它确定性旋钮


# ---------------------------------------------------------------------------
# 归一化（递归）
# ---------------------------------------------------------------------------
def _is_noise_key(key: str) -> bool:
    return key.lower() in _NOISE_KEYS


def _is_secret_key(key: str) -> bool:
    return bool(_SECRET_KEY_RE.search(key))


def _normalize(value: Any) -> Any:
    """递归归一化单个值。

    返回 ``_DROP`` 哨兵表示「该节点应被剔除」。
    """
    if value is None:
        return _DROP
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                key = str(key)
            # 噪声键：直接剔除。
            if _is_noise_key(key):
                continue
            # Secret 键：脱敏为常量占位，真实值不计入哈希。
            if _is_secret_key(key):
                out[key] = REDACTED
                continue
            normalized = _normalize(item)
            if normalized is _DROP:
                continue
            out[key] = normalized
        if not out:
            return _DROP
        return out
    if isinstance(value, (list, tuple, set, frozenset)):
        out: list[Any] = []
        for item in value:
            normalized = _normalize(item)
            if normalized is _DROP:
                continue
            out.append(normalized)
        if not out:
            return _DROP
        return out
    if isinstance(value, (str, int, float, bool)):
        if isinstance(value, str) and value == "":
            return _DROP
        return value
    # 其它类型（如 Enum / 对象）：以稳定字符串落库，避免 repr 抖动。
    return str(value)


def normalize_run_config(raw: "RunConfig | dict") -> dict:
    """归一化运行配置为确定性 dict。

    - ``RunConfig`` 经 ``dataclasses.asdict`` 展开为 dict 再归一。
    - 递归排序键、剔除 None / 空 / 噪声 / 脱敏 Secret（见 ``_normalize``）。
    - 返回**新** dict；不修改入参。
    """
    if isinstance(raw, RunConfig):
        source: Any = {
            "model_gateway_id": raw.model_gateway_id,
            "model_name": raw.model_name,
            "tool_scope": raw.tool_scope,
            "prompt_spec": raw.prompt_spec,
            "strategy": raw.strategy,
            "component_versions": raw.component_versions,
            "extra": raw.extra,
        }
    elif isinstance(raw, dict):
        source = raw
    else:
        # 非常规输入：尽力以 dict 形态归一。
        source = {"value": raw}

    normalized = _normalize(source)
    if normalized is _DROP:
        return {}
    assert isinstance(normalized, dict)
    return normalized


# ---------------------------------------------------------------------------
# 指纹
# ---------------------------------------------------------------------------
def compute_fingerprint(config: "RunConfig | dict") -> str:
    """去噪 + 脱敏 → canonical JSON（sort_keys, separators）→ sha256 → 前缀。

    返回 ``"sha256:<hexdigest>"``。同输入恒定返回同一摘要；Secret 真实值不进入哈希。
    """
    normalized = normalize_run_config(config)
    canonical = json.dumps(
        normalized,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"{FINGERPRINT_PREFIX}{digest}"


def config_changed(prev_fp: str, next_fp: str) -> bool:
    """仅比较两指纹的相等性（配置指纹是否变化）。"""
    return prev_fp != next_fp


# ---------------------------------------------------------------------------
# 幂等键构造
# ---------------------------------------------------------------------------
def build_idempotency_key(*parts: Any) -> str:
    """统一拼接幂等键：各 part 转小写、以冒号 ``:`` 分隔。

    空 ``None`` / 空字符串 part 被跳过，保证稳定。
    """
    cleaned = [str(p).strip().lower() for p in parts if p not in (None, "")]
    return ":".join(cleaned)


__all__ = [
    "RunConfig",
    "FINGERPRINT_PREFIX",
    "REDACTED",
    "normalize_run_config",
    "compute_fingerprint",
    "config_changed",
    "build_idempotency_key",
]
