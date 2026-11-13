"""B 层运行时治理 · 闸呈现（小白可读的 GatePrompt 生成 + 禁词红线 enforcement）。

本模块是**唯一**把「高影响动作」翻译成给小白看的「拍板闸」文本的出口：

- ``render_gate_prompt`` 取 ``gate_prompt_templates`` 模板填参 → 组装 ``GatePrompt``
  → **禁词扫描**（唯一 enforcement 点）；命中 ``FORBIDDEN_TERMS`` 则丢弃并回退
  「先模拟(B) + 取消(C)」二元安全闸（回退闸本身也合规）。
- ``standard_options`` 标准选项工厂：A 继续 ⭐ / B 先模拟看看 / C 取消 /（可选）D 换个做法。
- ``scan_forbidden_terms`` / ``validate_gate_prompt`` 提供禁词与 JSON Schema 校验。

全部使用标准库；零新依赖。``FORBIDDEN_TERMS`` 为禁词红线单一真源。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Literal

# ---------------------------------------------------------------------------
# 禁词红线单一真源（总控 2026-07-20 拍板，不得改）
# ---------------------------------------------------------------------------
FORBIDDEN_TERMS: tuple[str, ...] = (
    "sandbox",
    "schema",
    "API",
    "token",
    "diff",
    "回滚",
    "部署",
    "端点",
    "进程",
    "权限位",
)

# GatePrompt.category 业务风险类别（JSON Schema enum）。
_BUSINESS_CATEGORIES: frozenset[str] = frozenset(
    {"money", "data", "reputation", "irreversible", "external"}
)
# GateOption.id 取值。
_OPTION_IDS: frozenset[str] = frozenset({"A", "B", "C", "D"})

# 标准选项短标签（大白话）。
_LABELS: dict[str, str] = {
    "A": "继续",
    "B": "先模拟看看",
    "C": "取消",
    "D": "换个做法",
}


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass
class GateOption:
    """单个拍板选项（大白话）。"""

    id: Literal["A", "B", "C", "D"]
    label: str
    effect: str


@dataclass
class GatePrompt:
    """呈现给小白用户的拍板闸（全部字段大白话，零技术术语）。"""

    gate_id: str
    category: str
    title: str
    business_risk: str
    options: list[GateOption]
    recommended: Literal["A", "B", "C", "D"]
    one_line_consequence: str
    expires_at: str | None = None


class GatePromptValidationError(ValueError):
    """脱敏校验错误：不携带任何路径 / 键 / 参数。"""


# 延迟导入（避免与 gate_prompt_templates 的循环）：本模块常量与数据结构定义之后。
from .gate_prompt_templates import (  # noqa: E402
    GATE_TEMPLATES,
    GATE_BUSINESS_CATEGORY,
    G_CATEGORIES,
    TemplateSpec,
)


# ---------------------------------------------------------------------------
# 标准选项工厂
# ---------------------------------------------------------------------------
def standard_options(category: str, *, allow_d: bool = False) -> list[GateOption]:
    """§3.2 标准选项工厂：A 继续 ⭐ / B 先模拟看看 / C 取消 /（可选）D 换个做法。

    按 category 注入各选项的大白话 effect（文案来自 ``GATE_TEMPLATES``）。
    """
    spec = GATE_TEMPLATES.get(category)
    if spec is None:
        effects = {
            "A": "按系统建议继续",
            "B": "先看看效果再决定",
            "C": "这次先不做",
        }
    else:
        effects = spec.options_effects
    options: list[GateOption] = []
    for key in ("A", "B", "C"):
        if key in effects:
            options.append(GateOption(id=key, label=_LABELS[key], effect=effects[key]))
    if allow_d and "D" in effects:
        options.append(GateOption(id="D", label=_LABELS["D"], effect=effects["D"]))
    return options


# ---------------------------------------------------------------------------
# 禁词扫描
# ---------------------------------------------------------------------------
def scan_forbidden_terms(text: str) -> list[str]:
    """返回 text 中命中的禁词列表（空列表 = 合规）。"""
    if not text:
        return []
    lower = text.lower()
    found: list[str] = []
    for term in FORBIDDEN_TERMS:
        if term.lower() in lower:
            found.append(term)
    return found


# ---------------------------------------------------------------------------
# 参数填充（把 ¥X / 集合名 注入模板）
# ---------------------------------------------------------------------------
def _fill(text: str, action_context: Any) -> str:
    if not text:
        return text
    # G2：约 ¥X → 实际费用（无费用时降级为「一些钱」）。
    if "约 ¥X" in text:
        cost = getattr(action_context, "estimated_cost", 0) or 0
        text = text.replace(
            "约 ¥X", f"约 ¥{cost:.0f}" if cost > 0 else "一些钱"
        )
    # G3：{collections} → 受保护集合名（无时降级为「重要资料」）。
    if "{collections}" in text:
        cols = getattr(action_context, "protected_collections", ()) or ()
        text = text.replace(
            "{collections}", ", ".join(cols) if cols else "重要资料"
        )
    return text


def _prompt_text(prompt: GatePrompt) -> str:
    """拼接 GatePrompt 所有呈现文本，供禁词扫描。"""
    parts = [prompt.title, prompt.business_risk, prompt.one_line_consequence]
    parts.extend(opt.label for opt in prompt.options)
    parts.extend(opt.effect for opt in prompt.options)
    return "\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# JSON Schema 校验
# ---------------------------------------------------------------------------
def validate_gate_prompt(prompt: GatePrompt) -> None:
    """GatePrompt JSON Schema 校验（maxLength / 2–4 选项 / required）。

    违规抛脱敏 ``GatePromptValidationError``（不携带路径 / 键 / 参数）。
    """
    try:
        if not getattr(prompt, "gate_id", None):
            raise GatePromptValidationError("gate_id 必填")
        if prompt.category not in _BUSINESS_CATEGORIES:
            raise GatePromptValidationError("category 非法")
        if not getattr(prompt, "title", None) or len(prompt.title) > 40:
            raise GatePromptValidationError("title 必填且 ≤40 字")
        if prompt.business_risk is None or len(prompt.business_risk) > 120:
            raise GatePromptValidationError("business_risk ≤120 字")
        options = getattr(prompt, "options", None)
        if not isinstance(options, (list, tuple)) or not (2 <= len(options) <= 4):
            raise GatePromptValidationError("options 须 2–4 项")
        ids: set[str] = set()
        for opt in options:
            if getattr(opt, "id", None) not in _OPTION_IDS:
                raise GatePromptValidationError("option.id 非法")
            if not getattr(opt, "label", None) or len(opt.label) > 24:
                raise GatePromptValidationError("option.label 必填且 ≤24 字")
            if not getattr(opt, "effect", None) or len(opt.effect) > 80:
                raise GatePromptValidationError("option.effect 必填且 ≤80 字")
            ids.add(opt.id)
        if prompt.recommended not in ids:
            raise GatePromptValidationError("recommended 须为选项之一")
        if (
            not getattr(prompt, "one_line_consequence", None)
            or len(prompt.one_line_consequence) > 80
        ):
            raise GatePromptValidationError("one_line_consequence 必填且 ≤80 字")
    except GatePromptValidationError:
        raise
    except Exception as exc:  # noqa: BLE001 - 兜底脱敏
        raise GatePromptValidationError("gate prompt 不合规") from exc


# ---------------------------------------------------------------------------
# 回退安全闸（B 模拟 + C 取消，自身禁词合规）
# ---------------------------------------------------------------------------
def _build_fallback_gate(category: str, business_cat: str) -> GatePrompt:
    return GatePrompt(
        gate_id=f"fallback-{category.lower()}-{uuid.uuid4().hex[:8]}",
        category=business_cat,
        title="这个动作影响较大，建议先看看效果再决定",
        business_risk="发出去或改了之后可能很难收回",
        options=[
            GateOption(id="B", label="先模拟看看", effect="先在内部试一遍，不对外，也不改真东西"),
            GateOption(id="C", label="取消", effect="这次先不做"),
        ],
        recommended="B",
        one_line_consequence="先看看效果，不满意还能取消",
        expires_at=None,
    )


# ---------------------------------------------------------------------------
# 唯一呈现出口（禁词红线唯一 enforcement 点）
# ---------------------------------------------------------------------------
def render_gate_prompt(
    category: str,
    action_context: Any,
    config: Any = None,
) -> GatePrompt:
    """生成给小白看的拍板闸。

    ① 取 ``GATE_TEMPLATES`` 对应模板填参；② 组装 ``GatePrompt``；
    ③ **禁词扫描**：任一文本命中 ``FORBIDDEN_TERMS`` → 回退「先模拟(B)+取消(C)」
       二元安全闸；④ 返回 ``GatePrompt``。
    """
    business_cat = GATE_BUSINESS_CATEGORY.get(category, "irreversible")
    spec = GATE_TEMPLATES.get(category)
    if spec is None:
        return _build_fallback_gate(category, business_cat)

    title = _fill(spec.title, action_context)
    business_risk = _fill(spec.business_risk, action_context)
    consequence = _fill(spec.consequence, action_context)

    try:
        options = standard_options(category)
        recommended = spec.recommended if spec.recommended in _OPTION_IDS else "B"
        prompt = GatePrompt(
            gate_id=f"{category.lower()}-{uuid.uuid4().hex[:8]}",
            category=business_cat,
            title=title,
            business_risk=business_risk,
            options=options,
            recommended=recommended,  # type: ignore[arg-type]
            one_line_consequence=consequence,
            expires_at=None,
        )
    except Exception:
        return _build_fallback_gate(category, business_cat)

    # 唯一禁词 enforcement 点：命中即回退安全闸。
    if scan_forbidden_terms(_prompt_text(prompt)):
        return _build_fallback_gate(category, business_cat)

    try:
        validate_gate_prompt(prompt)
    except GatePromptValidationError:
        return _build_fallback_gate(category, business_cat)

    return prompt


__all__ = [
    "FORBIDDEN_TERMS",
    "GateOption",
    "GatePrompt",
    "GatePromptValidationError",
    "standard_options",
    "scan_forbidden_terms",
    "validate_gate_prompt",
    "render_gate_prompt",
    "G_CATEGORIES",
    "GATE_TEMPLATES",
    "GATE_BUSINESS_CATEGORY",
]
