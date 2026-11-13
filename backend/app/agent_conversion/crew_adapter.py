"""CrewYamlAdapter —— CrewAI crew YAML 归一适配器（结构化源）。

实现 ``SourceAdapter`` 契约：把 ``sources/crewai/*.yaml``（agents/tools/tasks）
归一为 ``CanonicalAgentSpec``。CrewAI 为**结构化高保真**源，``tools`` 已是显式
具名字段，故 ``extract_capabilities`` 为**近空操作**（不跑 NLP 抽取）。

本适配器**不读写数据库**（设计稿 4.2）：命中既有 115 工具 / 55 技能的匹配在
映射/seed 阶段完成；此处仅产出候选（``matched_tool_id`` 留空）。其存在意义是
证明 CrewAI 离线副本可重新解析为等价 spec（见 T9 解析测试）；实际落库行来自
``seed_multisource.CREWAI_MANIFEST``（同 pilot_b 模式）。

许可闸门（设计 §7.5）：CrewAI 公共示例多为 MIT，本适配器在 ``get_metadata`` 与
``parse`` 中统一声明 ``license_spdx='MIT'``、``commercial_use=True``、
``copyleft=False``、``attribution_required=True``。
"""

from __future__ import annotations

import os
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
    Persona,
    SecurityScan,
    SourceMeta,
    WorkflowSpec,
    WorkflowStep,
)
from .sanitize import clean_text
from .security_scan import scan_all

DEFAULT_REPO_URL = "https://github.com/crewAIInc/crewAI/tree/main/examples"
CREW_ARCHETYPE = "balanced_facilitator"


def _slugify_role(role: str) -> str:
    """角色名 → 下划线 slug（用于 spec.identity.slug）。"""
    return clean_text(role).lower().replace(" ", "_").replace("-", "_") or "crew_agent"


class CrewYamlAdapter(SourceAdapter):
    """CrewAI crew YAML 归一适配器（结构化源）。"""

    def __init__(self, repo_url: str = DEFAULT_REPO_URL) -> None:
        self._repo_url = repo_url
        self._fetched_at = ""

    # ── SourceAdapter 实现 ──────────────────────────────────────────
    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        root = source_root if isinstance(source_root, str) else str(source_root)
        if not os.path.isdir(root):
            return []
        entries: list[SourceEntry] = []
        for fname in sorted(os.listdir(root)):
            if not fname.endswith((".yaml", ".yml")):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            crew_name = str(data.get("crew_name") or data.get("name") or fname)
            for idx, agent in enumerate(data.get("agents") or []):
                if not isinstance(agent, dict):
                    continue
                role = clean_text(str(agent.get("role") or f"agent_{idx}"))
                entries.append(
                    SourceEntry(
                        entry_id=f"crew:{fname}:{idx}",
                        entry_path=fpath,
                        title=f"{crew_name}/{role}",
                        raw_ref={
                            "file": fname,
                            "crew_name": crew_name,
                            "agent_index": idx,
                            "role": role,
                        },
                    )
                )
        return entries

    def fetch(self, entry: SourceEntry) -> Any:
        with open(entry.entry_path, "r", encoding="utf-8") as fh:
            return fh.read()

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        data = yaml.safe_load(raw) if isinstance(raw, str) else raw
        if not isinstance(data, dict):
            data = {}
        idx = 0
        if isinstance(entry.raw_ref, dict):
            idx = int(entry.raw_ref.get("agent_index", 0) or 0)
        agents = data.get("agents") or []
        agent = agents[idx] if idx < len(agents) else (agents[0] if agents else {})
        if not isinstance(agent, dict):
            agent = {}

        role = clean_text(str(agent.get("role") or (entry.title if isinstance(entry.title, str) else "crew_agent")))
        goal = clean_text(str(agent.get("goal") or ""))
        backstory = clean_text(str(agent.get("backstory") or ""))

        # tools：CrewAI 多为具名字符串列表，也可能为 {name: ...} 字典。
        raw_tools = agent.get("tools") or []
        tool_names: list[str] = []
        for t in raw_tools:
            if isinstance(t, str):
                tool_names.append(t)
            elif isinstance(t, dict):
                tool_names.append(str(t.get("name") or t.get("tool") or ""))
        tool_names = [n for n in tool_names if n]

        # tasks：仅取指派给本 agent 的 task（按 role 匹配）。
        tasks = [
            t
            for t in (data.get("tasks") or [])
            if isinstance(t, dict) and clean_text(str(t.get("agent") or "")) == role
        ]

        # 安全三段初扫（goal + backstory）。
        scan = scan_all(f"{goal}\n{backstory}")
        security_scan = SecurityScan(
            credential_patterns=scan["credential_patterns"],
            prompt_injection_flags=scan["prompt_injection_flags"],
            overclaim_flags=scan["overclaim_flags"],
        )

        tool_candidates = [
            CapabilityCandidate(
                name_hint=n,
                evidence=f"CrewAI agent tool: {n}",
                suggested_tool_type="api_integration",
                matched_tool_id="",
            )
            for n in tool_names
        ]

        steps: list[WorkflowStep] = []
        for i, t in enumerate(tasks):
            desc = clean_text(str(t.get("description") or f"Step {i + 1}"))
            steps.append(
                WorkflowStep(
                    step_order=i + 1,
                    name=desc[:40] or f"Step {i + 1}",
                    instruction_excerpt=desc,
                    expected_output=clean_text(str(t.get("expected_output") or "")),
                    owner_role=role,
                )
            )

        spec = CanonicalAgentSpec(
            source=SourceMeta(
                adapter="CrewYamlAdapter",
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
                    "MIT License — public CrewAI crew example. Permission is hereby "
                    "granted, free of charge, to any person obtaining a copy of this "
                    "software and associated documentation files to deal in the software "
                    "without restriction."
                ),
            ),
            identity=Identity(
                name=role,
                role=role,
                slug=_slugify_role(role),
                description=goal,
                emoji="",  # CrewAI 无 emoji → 清洗后为空
                color="",  # CrewAI 无 color
                vibe="",
            ),
            mission=Mission(
                summary=goal,
                responsibilities=[backstory] if backstory else [],
                critical_rules=[],
            ),
            persona=Persona(
                archetype=CREW_ARCHETYPE,
                traits=[],
                communication_style={"tone": "neutral"},
                reporting_style={"frequency": "per-milestone"},
                decision_style="consultative",
                collaboration_style={"style": "cross-functional"},
            ),
            workflow=WorkflowSpec(process_type="sequential", steps=steps),
            capability_candidates=CapabilityCandidates(
                tool_candidates=tool_candidates, skill_candidates=[]
            ),
            security_scan=security_scan,
        )
        return spec

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        """结构化源近空操作：tools 已具名，无需 NLP 抽取。

        仅确保 ``capability_candidates.tool_candidates`` 已填充（parse 已完成）；
        这里补齐以防调用方直接构造 spec 时缺失。
        """
        if not spec.capability_candidates.tool_candidates:
            # 理论上不会触发（parse 已填）；保留为防御性空实现。
            spec.capability_candidates = CapabilityCandidates(
                tool_candidates=[], skill_candidates=[]
            )
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="CrewYamlAdapter",
            repo_url=self._repo_url,
            license_spdx="MIT",
            commercial_use=True,
            copyleft=False,
            attribution_required=True,
            fetched_at=self._fetched_at,
        )
