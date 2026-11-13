"""MCPManifestAdapter —— MCP server manifest JSON 归一适配器（纯工具源）。

实现 ``SourceAdapter`` 契约：把 ``sources/mcp/*.json``（每个文件一个 server +
tools 数组）归一为 ``CanonicalAgentSpec``。MCP 为**结构化高保真**源，工具已是
显式具名字段，故 ``extract_capabilities`` 为**近空操作**（不跑 NLP 抽取）。

本适配器**不读写数据库**（设计稿 4.2）：实际落库行来自
``seed_multisource.MCP_MANIFEST``（仅 ``tl_mcp_*`` 工具，纯工具源，不写
et_*/pt_*/skl_*/wt_*/dt_*）。其存在意义是证明 MCP 离线副本可重新解析为等价 spec
（见 T9 解析测试）。

许可闸门（设计 §7.5）：知名 MCP server（filesystem / fetch / sqlite / git /
sequentialthinking 等）多为 MIT；本适配器在 ``get_metadata`` / ``parse`` 中按
server 声明的 ``license`` 字段填充，缺失时默认 ``MIT``。
"""

from __future__ import annotations

import json
import os
from typing import Any, Iterable

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
from .sanitize import clean_text
from .security_scan import scan_all
from .seed_multisource import classify_license

DEFAULT_REPO_URL = "https://github.com/modelcontextprotocol/servers"


def _slugify_server(name: str) -> str:
    return clean_text(name).lower().replace(" ", "_").replace("-", "_") or "mcp_server"


class MCPManifestAdapter(SourceAdapter):
    """MCP server manifest JSON 归一适配器（纯工具源）。"""

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
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            server_name = str(data.get("server") or data.get("name") or fname)
            entries.append(
                SourceEntry(
                    entry_id=f"mcp:{fname}:{server_name}",
                    entry_path=fpath,
                    title=server_name,
                    raw_ref={"file": fname, "server_name": server_name},
                )
            )
        return entries

    def fetch(self, entry: SourceEntry) -> Any:
        with open(entry.entry_path, "r", encoding="utf-8") as fh:
            return fh.read()

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        data = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(data, dict):
            data = {}
        server_name = ""
        if isinstance(entry.raw_ref, dict):
            server_name = str(entry.raw_ref.get("server_name") or "")
        if not server_name:
            server_name = str(data.get("server") or data.get("name") or "mcp_server")

        server_desc = clean_text(str(data.get("description") or ""))
        tools = data.get("tools") or []
        spdx = str(data.get("license") or "MIT")

        # 安全三段初扫（server 描述 + 各工具描述）。
        blob = "\n".join(
            [server_desc]
            + [str(t.get("description", "")) for t in tools if isinstance(t, dict)]
        )
        scan = scan_all(blob)
        security_scan = SecurityScan(
            credential_patterns=scan["credential_patterns"],
            prompt_injection_flags=scan["prompt_injection_flags"],
            overclaim_flags=scan["overclaim_flags"],
        )

        tool_candidates = [
            CapabilityCandidate(
                name_hint=str(t.get("name", "")),
                evidence=clean_text(str(t.get("description") or "")),
                suggested_tool_type="api_integration",
                matched_tool_id="",
            )
            for t in tools
            if isinstance(t, dict) and str(t.get("name", ""))
        ]

        # 许可闸门：copyleft / 无 LICENSE → 仍归一到 spec，但 disposition 由
        # classify_license 决定（落库时由 manifest disposition 控制；此处仅记录）。
        allowed, _disposition, _reason = classify_license(spdx)
        spec = CanonicalAgentSpec(
            source=SourceMeta(
                adapter="MCPManifestAdapter",
                repo_url=self._repo_url,
                entry_path=entry.entry_path,
                fetched_at=self._fetched_at,
            ),
            license=LicenseInfo(
                spdx=spdx,
                commercial_use=allowed,
                copyleft=(spdx in ("GPL-3.0", "AGPL-3.0", "CC-BY-SA-4.0")),
                attribution_required=True,
                raw_license_text=f"{spdx} License — public MCP server.",
            ),
            identity=Identity(
                name=server_name,
                role=server_name,
                slug=_slugify_server(server_name),
                description=server_desc,
                emoji="",
                color="",
                vibe="",
            ),
            mission=Mission(summary=server_desc),
            capability_candidates=CapabilityCandidates(
                tool_candidates=tool_candidates, skill_candidates=[]
            ),
            security_scan=security_scan,
        )
        return spec

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        """结构化源近空操作：tools 已具名，无需 NLP 抽取。"""
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="MCPManifestAdapter",
            repo_url=self._repo_url,
            license_spdx="MIT",
            commercial_use=True,
            copyleft=False,
            attribution_required=True,
            fetched_at=self._fetched_at,
        )
