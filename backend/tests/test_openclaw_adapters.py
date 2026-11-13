import tempfile
import unittest
from pathlib import Path

from app.agent_conversion.openclaw_adapters import (
    ClawHubAdapter,
    OpenClawSkillAdapter,
    license_gate,
)


class OpenClawAdapterTest(unittest.TestCase):
    def test_skill_md_supporting_files_are_discovered_and_gated(self):
        with tempfile.TemporaryDirectory() as root:
            skill = Path(root) / "research"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: Research\nlicense: MIT\n---\n## Tools\n- browser\n",
                encoding="utf-8",
            )
            (skill / "README.md").write_text("supporting file", encoding="utf-8")
            adapter = OpenClawSkillAdapter(repo_url="https://example.test/skill")
            entries = list(adapter.discover(root))
            self.assertEqual(len(entries), 1)
            raw = adapter.fetch(entries[0])
            self.assertEqual(raw["supporting_files"][0]["path"], "README.md")
            spec = adapter.parse(raw, entries[0])
            self.assertEqual(spec.source.adapter, "OpenClawSkillAdapter")
            self.assertEqual(spec.license.spdx, "MIT")
            self.assertEqual(license_gate(spec), "pass")

    def test_clawhub_requires_origin_version_digest_and_owner(self):
        entries = list(
            ClawHubAdapter().discover(
                [
                    {"owner": "community", "slug": "research", "version": "1.0.0", "digest": "sha256:x", "origin": "https://clawhub.ai/community/research"},
                    {"owner": "community", "slug": "incomplete", "version": "1.0.0"},
                ]
            )
        )
        self.assertEqual(len(entries), 1)
        spec = ClawHubAdapter().parse(ClawHubAdapter().fetch(entries[0]), entries[0])
        self.assertEqual(spec.source.entry_path, "community/research@1.0.0")
        self.assertEqual(license_gate(spec), "pending")


if __name__ == "__main__":
    unittest.main()
