"""安全红线三段正则扫描（设计稿 §3.4 / §0 勘误）。

对外部 Agent 文本做三类风险初扫，供映射阶段与评审消费：
1. credential_patterns —— api_key / secret / token / password 模式，须剥离、绝不持久化；
2. prompt_injection_flags —— 覆盖系统指令 / 外泄 / 越权注入指令；
3. overclaim_flags —— 越权表述（如"执行任意代码"）须降级为受控 skl_* 或剔除。

所有函数纯函数、无副作用、不读写文件。
"""

from __future__ import annotations

import re

CREDENTIAL_PAT = re.compile(
    r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|client[_-]?secret|private[_-]?key)"
    r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{8,}",
    re.MULTILINE,
)
PROMPT_INJECTION_PAT = re.compile(
    r"(?i)(ignore (previous|above|all) instructions|disregard (your|the) (system|prior) "
    r"prompt|reveal (your|the) (system|hidden) prompt|you are now|new (instructions|rules):)",
    re.MULTILINE,
)
OVERCLAIM_PAT = re.compile(
    r"(?i)(execute (any|arbitrary) code|full (root|admin|sudo) access|"
    r"bypass (all|any) (security|safety|guardrail)|disable (all|any) (protection|restriction))",
    re.MULTILINE,
)


def scan_credential(text: str) -> list[str]:
    """命中 api_key/secret/token/password 等凭证赋值模式即返回匹配片段。"""
    return CREDENTIAL_PAT.findall(text or "")


def scan_prompt_injection(text: str) -> list[str]:
    """命中覆盖系统指令 / 外泄 / 越权注入指令即返回匹配片段。"""
    return PROMPT_INJECTION_PAT.findall(text or "")


def scan_overclaim(text: str) -> list[str]:
    """命中越权表述（执行任意代码 / 全权限 / 绕过安全）即返回匹配片段。"""
    return OVERCLAIM_PAT.findall(text or "")


def scan_all(text: str) -> dict[str, list[str]]:
    """对单段文本跑三段扫描，返回统一字典。"""
    return {
        "credential_patterns": scan_credential(text),
        "prompt_injection_flags": scan_prompt_injection(text),
        "overclaim_flags": scan_overclaim(text),
    }


def is_clean(text: str) -> bool:
    """单段文本是否三段零命中（零漏报）。"""
    if not text:
        return True
    return not (
        scan_credential(text) or scan_prompt_injection(text) or scan_overclaim(text)
    )
