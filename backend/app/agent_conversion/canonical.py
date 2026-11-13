"""CanonicalAgentSpec —— 外部 Agent 转 Curis 资产的统一中间表示（Python 绑定）。

对应设计稿 4.1 JSON Schema 的实例化契约。本模块仅定义类型与构造，
不包含任何 DB 逻辑、IO 或清洗/扫描行为（那些在 ``sanitize`` /
``security_scan`` / 各 ``SourceAdapter`` 中实现）。

字段分组（设计稿 4.1）：
- 内容字段：identity / mission / persona / workflow / deliverables
- 治理字段：source / license / security_scan / conversion_disposition
  （映射阶段被消费，但除 ``source`` 三态与 ``license``→``source_attribution``
  文本外不进入 Curis 业务表）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceMeta:
    """来源治理元数据。"""

    adapter: str = "AgencyMarkdownAdapter"
    repo_url: str = ""
    entry_path: str = ""
    fetched_at: str = ""  # ISO-8601


@dataclass
class LicenseInfo:
    """许可合规闸门输入。"""

    spdx: str = "MIT"
    commercial_use: bool = True
    copyleft: bool = False
    attribution_required: bool = True
    raw_license_text: str = ""


@dataclass
class DivisionInfo:
    """源分区 → Curis 部门映射。"""

    source_key: str = ""  # marketing / sales / support / finance / product
    label: str = ""
    target_dt_type: str = ""  # → department_types.type_key（business.*）


@dataclass
class Identity:
    """角色身份（frontmatter 层）。"""

    name: str = ""
    role: str = ""
    slug: str = ""
    description: str = ""
    emoji: str = ""  # 经 sanitize 清洗后的单 grapheme emoji
    color: str = ""  # 经 sanitize 清洗后的 #RRGGBB
    vibe: str = ""


@dataclass
class Mission:
    """目标 / 职责 / 约束（→ et_*.responsibility + default_instructions + guardrails_json）。"""

    summary: str = ""
    responsibilities: list[str] = field(default_factory=list)
    critical_rules: list[str] = field(default_factory=list)


@dataclass
class Persona:
    """人格层（→ pt_* 或 et_*.persona_overrides_json）。"""

    archetype: str = "balanced_facilitator"  # 6 值 CHECK 之一
    traits: list[str] = field(default_factory=list)
    communication_style: dict = field(default_factory=dict)
    reporting_style: dict = field(default_factory=dict)
    decision_style: str = "consultative"  # 自由文本（无 CHECK）
    collaboration_style: dict = field(default_factory=dict)


@dataclass
class WorkflowStep:
    """单步工作流。"""

    step_order: int = 0
    name: str = ""
    instruction_excerpt: str = ""
    expected_output: str = ""
    owner_role: str = ""


@dataclass
class WorkflowSpec:
    """工作流步骤集合。"""

    process_type: str = "sequential"
    steps: list[WorkflowStep] = field(default_factory=list)


@dataclass
class CapabilityCandidate:
    """单个隐含工具 / 技能候选。"""

    name_hint: str = ""
    evidence: str = ""
    matched_tool_id: str = ""  # 命中 115 则填，否则空
    matched_skill_id: str = ""  # 命中 52 则填，否则空
    suggested_tool_type: str = ""
    suggested_skill_type: str = ""


@dataclass
class CapabilityCandidates:
    """NLP 抽取后的隐含工具 / 技能候选集合。"""

    tool_candidates: list[CapabilityCandidate] = field(default_factory=list)
    skill_candidates: list[CapabilityCandidate] = field(default_factory=list)


@dataclass
class SecurityScan:
    """安全红线扫描结果（关卡⑦输入）。"""

    credential_patterns: list[str] = field(default_factory=list)
    prompt_injection_flags: list[str] = field(default_factory=list)
    overclaim_flags: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        """三段扫描是否零命中（零漏报）。"""
        return not (
            self.credential_patterns
            or self.prompt_injection_flags
            or self.overclaim_flags
        )


@dataclass
class ConversionDisposition:
    """转换处置建议（评审稿元数据，非 DB 列）。"""

    employee_action: str = "create"  # create | enhance_existing | skip
    existing_official_id: str = ""  # enhance_existing 时填 official.employee.tech_lead
    star_rating: int = 1
    notes: str = ""


@dataclass
class CanonicalAgentSpec:
    """外部 Agent 转 Curis 资产的统一中间表示（单一归一契约）。"""

    spec_version: str = "1.0.0"
    source: SourceMeta = field(default_factory=SourceMeta)
    license: LicenseInfo = field(default_factory=LicenseInfo)
    division: DivisionInfo = field(default_factory=DivisionInfo)
    identity: Identity = field(default_factory=Identity)
    mission: Mission = field(default_factory=Mission)
    persona: Persona = field(default_factory=Persona)
    deliverables: dict = field(default_factory=dict)
    workflow: WorkflowSpec = field(default_factory=WorkflowSpec)
    capability_candidates: CapabilityCandidates = field(default_factory=CapabilityCandidates)
    memory_notes: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    security_scan: SecurityScan = field(default_factory=SecurityScan)
    conversion_disposition: ConversionDisposition = field(default_factory=ConversionDisposition)

    def asset_slug(self) -> str:
        """由 identity.slug 推导统一资产 slug（去 et_/pt_ 前缀，下划线形式）。

        §7.1 权威约定：asset_slug = et_ 后缀（如 ``product_feedback_synth``）；
        ``employee id = official.employee.{asset_slug}``；``slug = kebab(asset_slug)``。
        """
        base = self.identity.slug or self.identity.role or self.identity.name
        base = base.strip().lower()
        return base.replace("-", "_").replace(" ", "_")
