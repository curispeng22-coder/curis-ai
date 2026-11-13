"""emoji / color 清洗 + 通用 Unicode 注入剥离。

清洗在 ``SourceAdapter.parse()`` 的归一阶段强制实施，保证进入 Curis 的
字符串字段不携带隐藏字符、非法 emoji / color。所有函数纯函数、无副作用。

emoji 白名单区段（设计稿 4.4 Q5）：
    Emoticons   U+1F300–1FAFF
    MiscSymbols U+2600–26FF
    Dingbats    U+2700–27BF
    Arrows      U+2190–21FF
    Geometric   U+25A0–25FF
规则：按 code point 计 ≤1；剥离变体选择符(VS16)、零宽连接符(ZWJ)、
RTL 覆盖符、控制字符、不可见字符；归一后 >1 code point 即拒收置空。
"""

from __future__ import annotations

import re
import unicodedata

EMOJI_RANGES: list[tuple[int, int]] = [
    (0x1F300, 0x1FAFF),
    (0x2600, 0x26FF),
    (0x2700, 0x27BF),
    (0x2190, 0x21FF),
    (0x25A0, 0x25FF),
]

# 零宽 / BOM / RTL 覆盖 / 变体选择符（VS16）等不可见字符
INVISIBLE = re.compile(
    "[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\u00ad\ufe0f]"
)


def clean_emoji(raw: str) -> str:
    """白名单 Unicode 区段 + 按 code point ≤1；剥离 VS16/ZWJ/控制符；超 1 code point 拒收置空。

    Args:
        raw: 原始 emoji 字符串（可能含 ZWJ / VS16 / 控制符）。
    Returns:
        清洗后的单 emoji 字符串；不合规返回空串。
    """
    if not raw:
        return ""
    s = INVISIBLE.sub("", raw)
    cps = [c for c in s if any(lo <= ord(c) <= hi for lo, hi in EMOJI_RANGES)]
    if len(cps) == 0 or len(cps) > 1:
        return ""
    return cps[0]


def clean_color(raw: str) -> str:
    """严格 #RRGGBB；拒绝具名色 / CSS 表达式。

    Args:
        raw: 原始颜色字符串（可能含前后空格）。
    Returns:
        规范化 #RRGGBB；不合规返回空串。
    """
    if not raw:
        return ""
    m = re.fullmatch(r"#[0-9a-fA-F]{6}", raw.strip())
    return m.group(0) if m else ""


def strip_invisible(text: str) -> str:
    """通用防注入：剥离零宽 / BOM / RTL 覆盖 / 控制字符（保留换行与制表）。

    Args:
        text: 任意字符串字段。
    Returns:
        去不可见字符后的字符串。
    """
    if not text:
        return ""
    text = INVISIBLE.sub("", text)
    return "".join(
        ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in "\n\t"
    )


def clean_text(text: str) -> str:
    """对自由文本字段的统一清洗：剥离不可见字符 + 控制字符，折叠多余空白。

    Args:
        text: 角色名 / 描述 / 指令等任意文本。
    Returns:
        清洗后的文本（首尾去空白；内部连续空白折叠为单空格）。
    """
    if not text:
        return ""
    text = strip_invisible(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def has_control_chars(text: str) -> bool:
    """检测字符串是否仍含控制字符 / 不可见字符（供校验脚本使用）。"""
    if not text:
        return False
    if INVISIBLE.search(text):
        return True
    return any(unicodedata.category(ch)[0] == "C" and ch not in "\n\t" for ch in text)
