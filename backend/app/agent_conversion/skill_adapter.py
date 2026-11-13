"""SkillRepoAdapter —— skill 仓库（curispeng22-coder/skill）SKILL.md 归一适配器。

实现 ``SourceAdapter`` 契约：遍历 ``sources/skill/*/SKILL.md``（每目录 1 条目），
把 skill 元数据 + 工具引用归一为 ``CanonicalAgentSpec``。skill 仓库为**结构化
高保真**源，工具引用已是显式字段，故 ``extract_capabilities`` 为**近空操作**。

许可（§7.5，总控特批）：curispeng22 为无 LICENSE 个人仓库，已获总控授权 harvest
为 draft 候选（不发布、不 instantiation）。本适配器在 ``get_metadata`` / ``parse``
中按授权元数据落库：``license_spdx='NOASSERTION'``、``commercial_use=False``、
``attribution_required=True``，并在 attribution 中注明来源与授权范围。代码层通用
许可闸门逻辑不变（仍拒绝 copyleft、仍对无 LICENSE 源打 skip 标记）——本仓库因总控
特批不触发 skip，直接按上述元数据落库。

本适配器**不读写数据库**；实际落库行来自 ``seed_multisource.SKILL_MANIFEST``
（同 pilot_b / crew / mcp 模式）。其存在意义是证明 skill 离线副本可重新解析为
等价 spec（见 T9 解析测试）。
"""

from __future__ import annotations

import os
import re
from typing import Any, Iterable

import yaml

from .adapter_base import SourceAdapter, SourceEntry, SourceMetadata
from .canonical import (
    CanonicalAgentSpec,
    CapabilityCandidate,
    CapabilityCandidates,
    Identity,
    LicenseInfo,
    Mission,
    SecurityScan,
    SourceMeta,
)
from .sanitize import clean_text, strip_invisible
from .security_scan import scan_all

DEFAULT_REPO_URL = "https://github.com/curispeng22-coder/skill"
ATTRIBUTION = (
    "来源 curispeng22-coder/skill；总控授权 draft 候选、不发布、不 instantiation。"
)


def _parse_frontmatter(fm_text: str) -> dict:
    """解析 YAML frontmatter；优先 pyyaml，缺失时回退极简扁平标量解析器。"""
    fm_text = fm_text.strip()
    try:
        data = yaml.safe_load(fm_text)
        if isinstance(data, dict):
            return {str(k): v for k, v in data.items()}
    except Exception:
        pass
    data: dict = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[key] = val
    return data


def _split_sections(body: str) -> dict:
    """按 `## ` 切分章节，返回 {标题: 文本}。"""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _extract_tool_refs(body: str) -> list[str]:
    """从 SKILL.md 的 Tools/工具 章节提取具名工具引用。"""
    sections = _split_sections(body)
    tool_text = ""
    for heading, text in sections.items():
        if re.search(r"tool|工具", heading, re.IGNORECASE):
            tool_text = text
            break
    refs: list[str] = []
    for line in tool_text.splitlines():
        line = line.strip()
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            chunk = m.group(1).strip()
        elif line:
            chunk = line
        else:
            continue
        # 支持逗号/顿号分隔与行内反引号
        chunk = chunk.strip("`").strip()
        for part in re.split(r"[,，、]", chunk):
            name = clean_text(part)
            if name:
                refs.append(name)
    return refs


class SkillRepoAdapter(SourceAdapter):
    """skill 仓库 SKILL.md 归一适配器（结构化源）。"""

    def __init__(self, repo_url: str = DEFAULT_REPO_URL) -> None:
        self._repo_url = repo_url
        self._fetched_at = ""

    # ── SourceAdapter 实现 ──────────────────────────────────────────
    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        root = source_root if isinstance(source_root, str) else str(source_root)
        if not os.path.isdir(root):
            return []
        entries: list[SourceEntry] = []
        for dname in sorted(os.listdir(root)):
            dpath = os.path.join(root, dname)
            if not os.path.isdir(dpath):
                continue
            skill_md = os.path.join(dpath, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            entries.append(
                SourceEntry(
                    entry_id=f"skill:{dname}",
                    entry_path=skill_md,
                    title=dname,
                    raw_ref={"dir": dname, "path": skill_md},
                )
            )
        return entries

    def fetch(self, entry: SourceEntry) -> Any:
        with open(entry.entry_path, "r", encoding="utf-8") as fh:
            return fh.read()

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        raw = raw or ""
        fm: dict = {}
        body = raw
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.DOTALL)
        if m:
            fm = _parse_frontmatter(m.group(1))
            body = m.group(2)
        body = strip_invisible(body)

        name = clean_text(str(fm.get("name", "") or (entry.title if isinstance(entry.title, str) else "")))
        description = clean_text(str(fm.get("description", "") or ""))
        tool_refs = _extract_tool_refs(body)

        # 安全三段初扫（frontmatter + 正文）。
        scan = scan_all(f"{description}\n{body}")
        security_scan = SecurityScan(
            credential_patterns=scan["credential_patterns"],
            prompt_injection_flags=scan["prompt_injection_flags"],
            overclaim_flags=scan["overclaim_flags"],
        )

        tool_candidates = [
            CapabilityCandidate(
                name_hint=t,
                evidence=f"SKILL.md 工具引用: {t}",
                suggested_tool_type="api_integration",
                matched_tool_id="",
            )
            for t in tool_refs
        ]

        spec = CanonicalAgentSpec(
            source=SourceMeta(
                adapter="SkillRepoAdapter",
                repo_url=self._repo_url,
                entry_path=entry.entry_path,
                fetched_at=self._fetched_at,
            ),
            license=LicenseInfo(
                spdx="NOASSERTION",
                commercial_use=False,
                copyleft=False,
                attribution_required=True,
                raw_license_text=ATTRIBUTION,
            ),
            identity=Identity(
                name=name,
                role=name,
                slug=clean_text(name).lower().replace(" ", "_"),
                description=description,
                emoji="",
                color="",
                vibe="",
            ),
            mission=Mission(summary=description),
            capability_candidates=CapabilityCandidates(
                tool_candidates=tool_candidates, skill_candidates=[]
            ),
            security_scan=security_scan,
        )
        return spec

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        """结构化源近空操作：工具引用已具名，无需 NLP 抽取。"""
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="SkillRepoAdapter",
            repo_url=self._repo_url,
            license_spdx="NOASSERTION",
            commercial_use=False,
            copyleft=False,
            attribution_required=True,
            fetched_at=self._fetched_at,
        )
