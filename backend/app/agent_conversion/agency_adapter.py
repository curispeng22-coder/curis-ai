"""AgencyMarkdownAdapter —— agency-agents（范式 1）Markdown 归一适配器。

实现 ``SourceAdapter`` 契约：把 ``sources/<division>/<slug>.md`` 归一为
``CanonicalAgentSpec``。frontmatter 解析优先用 ``pyyaml``，缺失时回退极简解析器
（agency frontmatter 均为扁平标量，足以覆盖）。章节切分 + emoji/color 清洗 +
三段安全扫描均在此完成。

本适配器**不读写数据库**（设计稿 4.2）：命中既有 115 工具 / 52 技能的匹配在
映射/seed 阶段完成，此处仅产出候选（matched_*_id 留空）。
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Iterable

from .adapter_base import SourceAdapter, SourceEntry, SourceMetadata
from .canonical import (
    CanonicalAgentSpec,
    CapabilityCandidate,
    CapabilityCandidates,
    DivisionInfo,
    Identity,
    LicenseInfo,
    Mission,
    Persona,
    SecurityScan,
    SourceMeta,
    WorkflowSpec,
    WorkflowStep,
)
from .sanitize import clean_color, clean_emoji, clean_text, strip_invisible
from .security_scan import scan_all
from .seed import PILOT_B_MANIFEST  # §7.1 权威资产定义：source (division,slug) → asset_slug

# 源文件命名（agency 仓库惯例）与 §7.1 规范 asset_slug 并非总是 kebab 互逆
# （如 finance-financial-analyst → finance_analyst）。归一时以 §7.1 为准。
_SOURCE_TO_ASSET_SLUG: dict[tuple[str, str], str] = {
    (e["division"], e["slug"]): e["asset_slug"] for e in PILOT_B_MANIFEST
}

DEFAULT_REPO_URL = "https://github.com/msitarzewski/agency-agents"
ALLOWED_DIVISIONS = ("product", "marketing", "sales", "support", "finance")
DIVISION_LABELS = {
    "product": "产品部",
    "marketing": "市场部",
    "sales": "销售部",
    "support": "客服部",
    "finance": "财务部",
}
DIVISION_ARCHETYPE = {
    "product": "balanced_facilitator",
    "marketing": "creative_explorer",
    "sales": "direct_executor",
    "support": "supportive_coach",
    "finance": "analytical_advisor",
}

# 关键词 → 隐含能力候选（name_hint / 类型 / 是否工具）。适配器不连 DB，
# matched_*_id 留空，由映射/seed 阶段决定是否生成 candidate。
_CAPABILITY_KEYWORDS: list[tuple[str, str, str, bool]] = [
    ("surveys", "survey_tool", "data_processing", True),
    ("product analytics", "product_analytics", "api_integration", True),
    ("github", "github", "api_integration", True),
    ("trend scanning", "trend_scanning", "research", False),
    ("web research", "web_research", "research", False),
    ("competitor research", "competitor_research", "research", False),
    ("a/b testing", "ab_testing", "analysis", False),
    ("hubspot", "hubspot", "api_integration", True),
    ("funnel analytics", "funnel_analytics", "data_processing", True),
    ("content drafting", "content_drafting", "creation", False),
    ("cms", "cms", "data_processing", True),
    ("social calendar", "social_calendar", "creation", False),
    ("social publishing", "social_publishing", "api_integration", True),
    ("salesforce", "salesforce", "api_integration", True),
    ("pipeline forecasting", "pipeline_forecast", "analysis", False),
    ("discovery calls", "discovery_call", "creation", False),
    ("intercom", "intercom", "api_integration", True),
    ("zendesk", "zendesk", "api_integration", True),
    ("ticket triage", "ticket_triage", "creation", False),
    ("compliance scanning", "compliance_scan", "analysis", False),
    ("contract review", "contract_review", "analysis", False),
    ("financial modeling", "financial_modeling", "analysis", False),
    ("stripe", "stripe", "api_integration", True),
    ("tax planning", "tax_planning", "analysis", False),
    ("regulatory", "regulatory_research", "research", False),
]


def _parse_frontmatter(fm_text: str) -> dict:
    """解析 YAML frontmatter；优先 pyyaml，缺失时回退极简扁平标量解析器。"""
    fm_text = fm_text.strip()
    try:
        import yaml  # 延迟导入：环境无 pyyaml 时回退，不影响解析

        data = yaml.safe_load(fm_text)
        if isinstance(data, dict):
            return {str(k): v for k, v in data.items()}
    except Exception:
        pass
    # 极简回退：仅支持 `key: value`（值可带引号），适配 agency 扁平 frontmatter。
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
    current = None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _bullets(text: str) -> list[str]:
    """提取 `- ` / `* ` 开头的列表项（清洗后非空）。"""
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            cleaned = clean_text(m.group(1))
            if cleaned:
                out.append(cleaned)
    return out


def _first_paragraph(text: str) -> str:
    """取首个非空段落（清洗后）。"""
    for blk in re.split(r"\n\s*\n", text.strip()):
        blk = clean_text(blk)
        if blk:
            return blk
    return ""


class AgencyMarkdownAdapter(SourceAdapter):
    """agency-agents Markdown 归一适配器（范式 1）。"""

    def __init__(self, repo_url: str = DEFAULT_REPO_URL) -> None:
        self._repo_url = repo_url
        self._fetched_at = ""

    # ── SourceAdapter 实现 ──────────────────────────────────────────
    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        root = source_root if isinstance(source_root, str) else str(source_root)
        if not os.path.isdir(root):
            return []
        entries: list[SourceEntry] = []
        for division in sorted(ALLOWED_DIVISIONS):
            dpath = os.path.join(root, division)
            if not os.path.isdir(dpath):
                continue
            for fname in sorted(os.listdir(dpath)):
                if not fname.endswith(".md"):
                    continue
                slug = fname[: -len(".md")]
                entry_id = f"agency:{division}:{slug}"
                entries.append(
                    SourceEntry(
                        entry_id=entry_id,
                        entry_path=os.path.join(dpath, fname),
                        title=f"{division}/{slug}",
                        raw_ref={"division": division, "slug": slug},
                    )
                )
        return entries

    def fetch(self, entry: SourceEntry) -> Any:
        with open(entry.entry_path, "r", encoding="utf-8") as fh:
            return fh.read()

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        raw = raw or ""
        division = ""
        slug = ""
        if isinstance(entry.raw_ref, dict):
            division = entry.raw_ref.get("division", "")
            slug = entry.raw_ref.get("slug", "")
        # §7.1 规范 asset_slug（源文件名与规范 slug 非总是互逆，以 manifest 为准）
        asset_slug = _SOURCE_TO_ASSET_SLUG.get((division, slug), (slug or "").replace("-", "_"))
        # frontmatter 解析
        fm: dict = {}
        body = raw
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.DOTALL)
        if m:
            fm = _parse_frontmatter(m.group(1))
            body = m.group(2)
        sections = _split_sections(body)

        raw_emoji = str(fm.get("emoji", "") or "")
        raw_color = str(fm.get("color", "") or "")
        name = clean_text(str(fm.get("name", "") or ""))
        description = clean_text(str(fm.get("description", "") or ""))
        vibe = clean_text(str(fm.get("vibe", "") or ""))

        identity = Identity(
            name=name or slug,
            role=asset_slug,
            slug=asset_slug,
            description=description,
            emoji=clean_emoji(raw_emoji),
            color=clean_color(raw_color),
            vibe=vibe,
        )

        mission_text = sections.get("Core Mission", "")
        mission = Mission(
            summary=_first_paragraph(mission_text) or description,
            responsibilities=_bullets(mission_text),
            critical_rules=_bullets(sections.get("Critical Rules", "")),
        )

        archetype = DIVISION_ARCHETYPE.get(division, "balanced_facilitator")
        persona = Persona(
            archetype=archetype,
            traits=[vibe] if vibe else [],
            communication_style={"tone": _first_paragraph(sections.get("Communication Style", "")) or "neutral"},
            reporting_style={"frequency": "per-milestone"},
            decision_style="consultative" if division != "finance" else "evidence_based",
            collaboration_style={"style": "cross-functional"},
        )

        # workflow steps
        steps: list[WorkflowStep] = []
        wf_text = sections.get("Workflow Process", "")
        for line in wf_text.splitlines():
            sm = re.match(r"^Step\s+(\d+)\s*[:：]\s*(.*)$", line.strip())
            if sm:
                steps.append(
                    WorkflowStep(
                        step_order=int(sm.group(1)),
                        name=f"Step {sm.group(1)}",
                        instruction_excerpt=clean_text(sm.group(2)),
                        expected_output="",
                        owner_role=identity.role,
                    )
                )
        workflow = WorkflowSpec(process_type="sequential", steps=steps)

        # deliverables 文本块
        deliverables = {
            "text_blocks": [
                clean_text(b)
                for b in _bullets(sections.get("Technical Deliverables", ""))
            ]
        }

        success_metrics = _bullets(sections.get("Success Metrics", ""))

        # 安全初扫（对全文，剥离 frontmatter 外的正文）
        scan = scan_all(body)
        security_scan = SecurityScan(
            credential_patterns=scan["credential_patterns"],
            prompt_injection_flags=scan["prompt_injection_flags"],
            overclaim_flags=scan["overclaim_flags"],
        )

        spec = CanonicalAgentSpec(
            source=SourceMeta(
                adapter="AgencyMarkdownAdapter",
                repo_url=self._repo_url,
                entry_path=entry.entry_path,
                fetched_at=self._fetched_at,
            ),
            license=LicenseInfo(
                spdx="MIT",
                commercial_use=True,
                copyleft=False,
                attribution_required=True,
                raw_license_text=(
                    f"MIT License — source {self._repo_url}. "
                    "Permission is hereby granted, free of charge, to any person "
                    "obtaining a copy of this software and associated documentation "
                    "files to deal in the software without restriction."
                ),
            ),
            division=DivisionInfo(
                source_key=division,
                label=DIVISION_LABELS.get(division, division),
                target_dt_type=f"business.{division}" if division else "",
            ),
            identity=identity,
            mission=mission,
            persona=persona,
            deliverables=deliverables,
            workflow=workflow,
            memory_notes=[],
            success_metrics=success_metrics,
            security_scan=security_scan,
        )
        return spec

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        haystack = " ".join(
            [
                spec.mission.summary,
                " ".join(spec.mission.responsibilities),
            " ".join(spec.deliverables.get("text_blocks", [])),
            " ".join(spec.workflow.steps and [s.instruction_excerpt for s in spec.workflow.steps] or []),
                " ".join(spec.success_metrics),
            ]
        ).lower()
        tool_candidates: list[CapabilityCandidate] = []
        skill_candidates: list[CapabilityCandidate] = []
        seen: set[str] = set()
        for kw, hint, suggested_type, is_tool in _CAPABILITY_KEYWORDS:
            if kw in haystack and hint not in seen:
                seen.add(hint)
                cand = CapabilityCandidate(
                    name_hint=hint,
                    evidence=f"源文本命中关键词 '{kw}'",
                    matched_tool_id="",
                    matched_skill_id="",
                    suggested_tool_type=suggested_type if is_tool else "",
                    suggested_skill_type="" if is_tool else suggested_type,
                )
                (tool_candidates if is_tool else skill_candidates).append(cand)
        spec.capability_candidates = CapabilityCandidates(
            tool_candidates=tool_candidates,
            skill_candidates=skill_candidates,
        )
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="AgencyMarkdownAdapter",
            repo_url=self._repo_url,
            license_spdx="MIT",
            commercial_use=True,
            copyleft=False,
            attribution_required=True,
            fetched_at=self._fetched_at,
        )
