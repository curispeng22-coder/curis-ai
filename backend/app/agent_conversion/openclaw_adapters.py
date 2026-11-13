"""OpenClaw SKILL.md 与 ClawHub 注册表的最小只读适配器。

适配器只发现、解析和计算摘要；不会执行 supporting files、下载远程包或写入
Company Resource。安装必须由后续 Skill Runtime 在来源/许可证/安全门禁通过后完成。
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Iterable

from .adapter_base import SourceAdapter, SourceEntry, SourceMetadata
from .canonical import CanonicalAgentSpec, Identity, LicenseInfo, SecurityScan, SourceMeta
from .security_scan import scan_all
from .skill_adapter import SkillRepoAdapter, _parse_frontmatter

_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"}
_TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class OpenClawSkillAdapter(SourceAdapter):
    """发现本地 OpenClaw skill 目录并输出 CanonicalAgentSpec。"""

    def __init__(self, repo_url: str = "") -> None:
        self._repo_url = repo_url

    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        root = Path(str(source_root))
        if not root.is_dir():
            return []
        result: list[SourceEntry] = []
        for skill_md in sorted(root.rglob("SKILL.md")):
            if any(part.startswith(".") for part in skill_md.relative_to(root).parts):
                continue
            skill_root = skill_md.parent
            result.append(
                SourceEntry(
                    entry_id=f"openclaw:{skill_root.relative_to(root)}",
                    entry_path=str(skill_md),
                    title=skill_root.name,
                    raw_ref={"root": str(skill_root), "relative_root": str(skill_root.relative_to(root))},
                )
            )
        return result

    def fetch(self, entry: SourceEntry) -> dict[str, Any]:
        root = Path((entry.raw_ref or {}).get("root", Path(entry.entry_path).parent))
        files: list[dict[str, str]] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name == "SKILL.md":
                continue
            files.append({"path": str(path.relative_to(root)), "sha256": _digest(path)})
        return {
            "skill_md": Path(entry.entry_path).read_text(encoding="utf-8"),
            "supporting_files": files,
        }

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        payload = raw if isinstance(raw, dict) else {"skill_md": str(raw or ""), "supporting_files": []}
        skill_md = payload.get("skill_md", "")
        spec = SkillRepoAdapter(repo_url=self._repo_url).parse(skill_md, entry)
        frontmatter = {}
        if skill_md.startswith("---"):
            parts = skill_md.split("---", 2)
            if len(parts) == 3:
                frontmatter = _parse_frontmatter(parts[1])
        license_spdx = str(frontmatter.get("license", "") or "NOASSERTION")
        spec.source = SourceMeta(
            adapter="OpenClawSkillAdapter",
            repo_url=self._repo_url,
            entry_path=(entry.raw_ref or {}).get("relative_root", entry.entry_path),
        )
        spec.license = LicenseInfo(
            spdx=license_spdx,
            commercial_use=license_spdx in _LICENSES,
            copyleft=False,
            attribution_required=True,
            raw_license_text="frontmatter license" if license_spdx != "NOASSERTION" else "license not declared",
        )
        scan = scan_all(skill_md)
        spec.security_scan = SecurityScan(
            credential_patterns=scan["credential_patterns"],
            prompt_injection_flags=scan["prompt_injection_flags"],
            overclaim_flags=scan["overclaim_flags"],
        )
        return spec

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="OpenClawSkillAdapter",
            repo_url=self._repo_url,
            license_spdx="NOASSERTION",
            commercial_use=False,
            copyleft=False,
            attribution_required=True,
        )


class ClawHubAdapter(SourceAdapter):
    """解析 ClawHub 公开注册表元数据；不负责远程下载或安装。"""

    REQUIRED_FIELDS = ("owner", "slug", "version", "digest", "origin")

    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        rows = source_root if isinstance(source_root, list) else []
        return [
            SourceEntry(
                entry_id=f"clawhub:{row['owner']}/{row['slug']}@{row['version']}",
                entry_path="",
                title=row["slug"],
                raw_ref=dict(row),
            )
            for row in rows
            if isinstance(row, dict) and all(row.get(field) for field in self.REQUIRED_FIELDS)
        ]

    def fetch(self, entry: SourceEntry) -> dict[str, Any]:
        return dict(entry.raw_ref or {})

    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        row = raw if isinstance(raw, dict) else {}
        skill_md = str(row.get("skill_md", "") or "")
        identity = str(row.get("name") or row.get("slug") or entry.title)
        license_spdx = str(row.get("license") or "NOASSERTION")
        scan = scan_all(skill_md)
        return CanonicalAgentSpec(
            source=SourceMeta(
                adapter="ClawHubAdapter",
                repo_url=str(row.get("origin") or ""),
                entry_path=f"{row.get('owner', '')}/{row.get('slug', '')}@{row.get('version', '')}",
            ),
            license=LicenseInfo(
                spdx=license_spdx,
                commercial_use=license_spdx in _LICENSES,
                copyleft=False,
                attribution_required=True,
                raw_license_text="registry metadata",
            ),
            security_scan=SecurityScan(
                credential_patterns=scan["credential_patterns"],
                prompt_injection_flags=scan["prompt_injection_flags"],
                overclaim_flags=scan["overclaim_flags"],
            ),
            identity=Identity(name=identity, role=identity, slug=identity.lower().replace("-", "_")),
        )

    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        return spec

    def get_metadata(self) -> SourceMetadata:
        return SourceMetadata(
            adapter="ClawHubAdapter",
            repo_url="https://clawhub.ai",
            license_spdx="registry-declared",
            commercial_use=False,
            copyleft=False,
            attribution_required=True,
        )


def license_gate(spec: CanonicalAgentSpec) -> str:
    """返回 UI/评审使用的许可证状态，不把 NOASSERTION 误判为可安装。"""
    return "pass" if spec.license.spdx in _LICENSES and spec.license.commercial_use else "pending"
