"""Agent 拆解转换引擎 V1 — 解析层（agency-agents 范式 1）。

本包把异构外部 Agent 源归一为统一中间表示 ``CanonicalAgentSpec``，
再经 ``SeedMapper`` 映射到 Curis 真实表（employee_templates / persona_templates /
skill_templates / tool_templates / workflow_templates / department_templates）。

设计约束（受控试点 B）：
- 所有资产为 candidate / draft 态、可回滚；不接入凭证、不建 marketplace、
  不 instantiation（ADR-0017 仍锁 Instance/Runtime）。
- 解析层为纯函数 + dataclass，**不读写数据库**（DB 写通道在 ``app.database``）。
- 真实数据源离线落 ``sources/``，运行期零外网依赖。
"""

from .canonical import (
    CanonicalAgentSpec,
    CapabilityCandidate,
    CapabilityCandidates,
    ConversionDisposition,
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
from .adapter_base import SourceAdapter, SourceEntry, SourceMetadata
from .sanitize import clean_color, clean_emoji, strip_invisible
from .security_scan import (
    scan_credential,
    scan_overclaim,
    scan_prompt_injection,
)

__all__ = [
    "CanonicalAgentSpec",
    "CapabilityCandidate",
    "CapabilityCandidates",
    "ConversionDisposition",
    "DivisionInfo",
    "Identity",
    "LicenseInfo",
    "Mission",
    "Persona",
    "SecurityScan",
    "SourceMeta",
    "WorkflowSpec",
    "WorkflowStep",
    "SourceAdapter",
    "SourceEntry",
    "SourceMetadata",
    "clean_color",
    "clean_emoji",
    "strip_invisible",
    "scan_credential",
    "scan_overclaim",
    "scan_prompt_injection",
]
