"""统一的公开资源扫描与人才成熟度投影。

这是只读生产线：它消费已登记的本地公开快照和现有 Adapter，不写 Employee、Skill
或 Capability 表。真正发布/招募仍由现有 Curis 资源门和 EmployeeTemplate 链负责。
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Iterable

from .agency_adapter import AgencyMarkdownAdapter
from .adapter_base import SourceEntry
from .canonical import CanonicalAgentSpec
from .crew_adapter import CrewYamlAdapter
from .mcp_adapter import MCPManifestAdapter
from .openclaw_adapters import OpenClawSkillAdapter

SOURCE_ROOT = Path(__file__).resolve().parent / "sources"
AGENCY_ZH_URL = "https://github.com/jnMetaCode/agency-agents-zh"
CREWAI_URL = "https://github.com/crewAIInc/crewAI/tree/main/examples"
OPENCLAW_URL = "https://docs.openclaw.ai/tools/skills"
MCP_URL = "https://github.com/modelcontextprotocol/servers"

MATURITY = ("DISCOVERED", "CANDIDATE", "COMPOSED", "VALIDATED", "CURIS_READY", "BLOCKED")
_CATEGORY = {
    "product": "产品",
    "marketing": "增长",
    "sales": "商业",
    "support": "商业",
    "finance": "数据",
    "engineering": "研发",
    "design": "设计",
    "research": "研究",
    "data": "数据",
}

PUBLIC_SOURCE_CATALOG = [
    {"source_id": "agency-agents-zh", "url": AGENCY_ZH_URL, "resource_types": ["agent"], "license_status": "MIT", "scan_status": "scanned_local_snapshot"},
    {"source_id": "crewai-examples", "url": CREWAI_URL, "resource_types": ["agent"], "license_status": "review_required", "scan_status": "scanned_local_snapshot"},
    {"source_id": "openclaw-skills", "url": OPENCLAW_URL, "resource_types": ["skill"], "license_status": "per_item", "scan_status": "scanned_local_snapshot"},
    {"source_id": "mcp-servers", "url": MCP_URL, "resource_types": ["mcp"], "license_status": "transition_review", "scan_status": "scanned_local_snapshot"},
    {"source_id": "anthropic-skills", "url": "https://github.com/anthropics/skills", "resource_types": ["skill"], "license_status": "mixed_review", "scan_status": "source_catalogued_not_imported"},
    {"source_id": "openai-skills", "url": "https://github.com/openai/skills", "resource_types": ["skill"], "license_status": "review_required", "scan_status": "source_catalogued_not_imported"},
    {"source_id": "superpowers", "url": "https://github.com/obra/superpowers", "resource_types": ["skill", "agent"], "license_status": "review_required", "scan_status": "source_catalogued_not_imported"},
]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")


def _digest(raw: Any) -> str:
    if isinstance(raw, str):
        payload = raw.encode("utf-8")
    else:
        payload = repr(raw).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _source_path(entry: SourceEntry) -> str:
    try:
        return str(Path(entry.entry_path).resolve().relative_to(SOURCE_ROOT.resolve()))
    except ValueError:
        return entry.entry_path


def _category(spec: CanonicalAgentSpec) -> str:
    source_key = spec.division.source_key or ""
    if source_key in _CATEGORY:
        return _CATEGORY[source_key]
    haystack = f"{spec.identity.name} {spec.identity.description} {spec.mission.summary}".lower()
    for needle, label in (
        ("design", "设计"),
        ("research", "研究"),
        ("data", "数据"),
        ("code", "研发"),
        ("engineer", "研发"),
        ("content", "内容"),
        ("growth", "增长"),
    ):
        if needle in haystack:
            return label
    return "其他"


def _status(spec: CanonicalAgentSpec, resource_type: str) -> str:
    if not spec.license.commercial_use or spec.license.spdx in {"NOASSERTION", ""}:
        return "BLOCKED"
    if not spec.security_scan.is_clean:
        return "BLOCKED"
    if resource_type == "agent":
        return "CANDIDATE"
    return "DISCOVERED"


def _record(
    spec: CanonicalAgentSpec,
    entry: SourceEntry,
    raw: Any,
    *,
    source_url: str,
    resource_type: str,
    source_status: str = "pending_snapshot_verification",
) -> dict[str, Any]:
    status = _status(spec, resource_type)
    source_path = _source_path(entry)
    digest = _digest(raw)
    skills = [item.name_hint for item in spec.capability_candidates.skill_candidates if item.name_hint]
    tools = [item.name_hint for item in spec.capability_candidates.tool_candidates if item.name_hint]
    identity = {
        "source": source_url,
        "repository": source_url,
        "path": source_path,
        "version": spec.source.fetched_at or "snapshot",
        "digest": digest,
        "license": spec.license.spdx,
    }
    return {
        "id": f"resource:{resource_type}:{_slug(spec.identity.name)}:{digest[:12]}",
        "resource_type": resource_type,
        "name": spec.identity.name or spec.identity.role,
        "role": spec.identity.role,
        "description": spec.identity.description or spec.mission.summary,
        "responsibility": spec.mission.summary,
        "category": _category(spec),
        "maturity": status,
        "status": status.lower(),
        "market_kind": "external_candidate" if resource_type == "agent" else "resource_candidate",
        "source": "external",
        "source_label": source_url.rsplit("/", 1)[-1],
        "source_url": source_url,
        "source_path": source_path,
        "source_status": source_status,
        "source_verified": False,
        "license": spec.license.spdx,
        "license_status": "pass" if spec.license.commercial_use else "blocked",
        "security_status": "pass" if spec.security_scan.is_clean else "blocked",
        "canonical_identity": identity,
        "duplicate_key": f"{resource_type}:{_slug(spec.identity.name)}:{digest}",
        "composition": {
            "status": "proposed" if resource_type == "agent" else "resource_only",
            "skills": skills,
            "tools": tools,
            "mcp": [],
            "knowledge_requirements": [],
            "connector_requirements": [],
            "model_requirements": list(spec.default_model_policy.keys()) if hasattr(spec, "default_model_policy") else [],
            "workflow_steps": len(spec.workflow.steps),
        },
        "candidate_gate": {
            "source": source_status,
            "license": "pass" if spec.license.commercial_use else "blocked",
            "security": "pass" if spec.security_scan.is_clean else "blocked",
            "dedup": "pass",
            "composition": "proposed" if resource_type == "agent" else "not_applicable",
            "validation": "pending",
            "recruit": "blocked_candidate" if resource_type == "agent" else "not_applicable",
        },
        "recruitable": False,
        "security_scan": {
            "credential_patterns": spec.security_scan.credential_patterns,
            "prompt_injection_flags": spec.security_scan.prompt_injection_flags,
            "overclaim_flags": spec.security_scan.overclaim_flags,
        },
    }


def _scan_adapter(
    adapter: Any,
    root: Path,
    *,
    source_url: str,
    resource_type: str,
    category_hint: str | None = None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for entry in adapter.discover(str(root)):
        raw = adapter.fetch(entry)
        spec = adapter.parse(raw, entry)
        spec = adapter.extract_capabilities(spec)
        record = _record(spec, entry, raw, source_url=source_url, resource_type=resource_type)
        if category_hint:
            record["category"] = category_hint
        records.append(record)
    return records


def scan_local_resource_pool() -> dict[str, Any]:
    """扫描当前已登记公开快照，输出去重后的候选池与统计。"""
    raw_records = [
        *_scan_adapter(AgencyMarkdownAdapter(repo_url=AGENCY_ZH_URL), SOURCE_ROOT, source_url=AGENCY_ZH_URL, resource_type="agent"),
        *_scan_adapter(CrewYamlAdapter(repo_url=CREWAI_URL), SOURCE_ROOT / "crewai", source_url=CREWAI_URL, resource_type="agent"),
        *_scan_adapter(OpenClawSkillAdapter(repo_url=OPENCLAW_URL), SOURCE_ROOT / "skill", source_url=OPENCLAW_URL, resource_type="skill"),
        *_scan_adapter(MCPManifestAdapter(repo_url=MCP_URL), SOURCE_ROOT / "mcp", source_url=MCP_URL, resource_type="mcp"),
    ]
    crew_categories = {
        "content_crew.yaml": "内容",
        "engineering_crew.yaml": "研发",
        "growth_crew.yaml": "增长",
        "market_research_crew.yaml": "研究",
        "support_crew.yaml": "商业",
    }
    for record in raw_records:
        if record["source_url"] == CREWAI_URL:
            record["category"] = next(
                (label for filename, label in crew_categories.items() if filename in record["source_path"]),
                record["category"],
            )
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    duplicate_count = 0
    for record in raw_records:
        if record["duplicate_key"] in seen:
            duplicate_count += 1
            continue
        seen.add(record["duplicate_key"])
        records.append(record)
    counts = {
        "discovered": len(raw_records),
        "deduped": len(records),
        "duplicates": duplicate_count,
        "agents": sum(item["resource_type"] == "agent" for item in records),
        "skills": sum(item["resource_type"] == "skill" for item in records),
        "mcp": sum(item["resource_type"] == "mcp" for item in records),
        "candidate": sum(item["maturity"] == "CANDIDATE" for item in records),
        "blocked": sum(item["maturity"] == "BLOCKED" for item in records),
        "composed": sum(item["maturity"] == "COMPOSED" for item in records),
        "validated": sum(item["maturity"] == "VALIDATED" for item in records),
        "curis_ready": sum(item["maturity"] == "CURIS_READY" for item in records),
    }
    return {
        "resources": records,
        "counts": counts,
        "categories": sorted({item["category"] for item in records}),
        "sources": PUBLIC_SOURCE_CATALOG,
    }
