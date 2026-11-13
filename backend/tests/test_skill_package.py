import io
import tarfile
from pathlib import Path

import pytest

from app.skill_package import inspect_package, install_package, verify_package, source_identity

REPO = "https://github.com/example/research-skill"
COMMIT = "a" * 40


def archive(entries=None):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as tar:
        for name, data in (entries or {
            "repo/LICENSE": b"MIT License\nCopyright fixture. Permission is hereby granted.",
            "repo/skills/research/SKILL.md": b"# Research\nRead references/method.md and cite sources.",
            "repo/skills/research/references/method.md": b"Preserve original URL and observation time.",
            "repo/skills/research/scripts/format.py": b"raise RuntimeError('installation must not execute me')",
        }).items():
            member = tarfile.TarInfo(name)
            if data is None:
                member.type = tarfile.SYMTYPE
                member.linkname = "/etc/passwd"
                tar.addfile(member)
            else:
                member.size = len(data)
                tar.addfile(member, io.BytesIO(data))
    return stream.getvalue()


def test_complete_package_has_license_and_every_subdirectory_file(tmp_path):
    manifest, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: archive())
    assert set(files) == {"SKILL.md", "references/method.md", "scripts/format.py", "CURIS_SOURCE_LICENSE"}
    path = install_package(tmp_path / "packages", manifest, files)
    assert install_package(tmp_path / "packages", manifest, files) == path
    verify_package(path, manifest)
    (path / "references/method.md").chmod(0o600)
    (path / "references/method.md").write_text("changed")
    with pytest.raises(ValueError, match="变化"):
        verify_package(path, manifest)


@pytest.mark.parametrize("name,data", [("repo/../escape", b"bad"), ("repo/skills/research/link", None),
                                      ("/absolute", b"bad"), ("repo/skills/research/a\\b", b"bad")])
def test_hostile_archive_rejected_before_filesystem_write(name, data, tmp_path):
    with pytest.raises(ValueError):
        inspect_package(REPO, COMMIT, fetch=lambda _: archive({name: data}))
    assert not list(tmp_path.iterdir())


def test_missing_license_and_mutable_or_private_source_are_rejected():
    with pytest.raises(ValueError, match="许可"):
        inspect_package(REPO, COMMIT, fetch=lambda _: archive({"repo/SKILL.md": b"skill"}))
    for url, version in [(REPO, "main"), ("https://user:secret@github.com/a/b", COMMIT),
                         ("https://localhost/a/b", COMMIT), (REPO + "?token=x", COMMIT)]:
        with pytest.raises(ValueError):
            source_identity(url, version)


def test_unexpected_file_or_link_invalidates_installed_package(tmp_path):
    manifest, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: archive())
    path = install_package(tmp_path, manifest, files)
    (path / "extra").symlink_to("SKILL.md")
    with pytest.raises(ValueError, match="链接"):
        verify_package(path, manifest)


def test_install_does_not_overwrite_unrelated_or_partial_package(tmp_path):
    manifest, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: archive())
    target = tmp_path / manifest["package_sha256"]
    target.mkdir()
    (target / "unrelated").write_text("retain")
    with pytest.raises(ValueError):
        install_package(tmp_path, manifest, files)
    assert (target / "unrelated").read_text() == "retain"


def test_public_links_resolve_versions_internally_and_discover_skills():
    import json
    from urllib.error import HTTPError
    from app.skill_package import resolve_link
    def fetch(url):
        if url.endswith("/HEAD") or url.endswith("/main") or url.endswith("/release%2Fv1"):
            return json.dumps({"sha": COMMIT}).encode()
        raise HTTPError(url, 404, "not found", {}, None)
    assert resolve_link(REPO, fetch=fetch) == (REPO, COMMIT, "")
    for link in [REPO + "/blob/main/skills/research/SKILL.md",
                 "https://raw.githubusercontent.com/example/research-skill/main/skills/research/SKILL.md",
                 REPO + "/tree/release/v1/skills/research"]:
        assert resolve_link(link, fetch=fetch) == (REPO, COMMIT, "skills/research")
    manifest, files = inspect_package(REPO, COMMIT, fetch=lambda _: archive(), discover=True)
    assert manifest["name"] == "Research" and manifest["subdirectory"] == "skills/research"
    assert "scripts/format.py" in files
    raw = archive({"repo/LICENSE": b"MIT", "repo/a/SKILL.md": b"# First", "repo/b/SKILL.md": b"# Second"})
    choices, files = inspect_package(REPO, COMMIT, fetch=lambda _: raw, discover=True)
    assert choices["selection_required"] and [x["name"] for x in choices["choices"]] == ["First", "Second"]
    assert files == {} and "package_sha256" not in choices


def test_skill_links_never_read_ambient_credentials_or_follow_private_sources():
    from app.skill_package import resolve_link
    calls = []
    for link in ["https://github.com@localhost/a/b", REPO + "?token=private", REPO + "#x",
                 "https://user:pass@github.com/a/b", "file:///tmp/SKILL.md", REPO + "/tree/main/../secret"]:
        with pytest.raises(ValueError):
            resolve_link(link, fetch=lambda url: calls.append(url))
    assert calls == []


def test_dependency_metadata_does_not_execute_or_claim_installation():
    from app.skill_package import dependency_requirements
    from app.skill_runtime import SkillRuntime
    plain = {"SKILL.md": b"# Summarize", "references/method.md": b"Use original sources"}
    assert SkillRuntime.dependency_status({"dependencies": dependency_requirements(plain, "example/summary")})["ready"]
    browser = SkillRuntime.dependency_status({"dependencies": dependency_requirements(plain, "Tencent/BrowserSkill")})
    assert not browser["ready"] and browser["preparation"] == "existing_browser_connection"
    scripts = {**plain, "scripts/setup.sh": b"do not execute"}
    assert SkillRuntime.dependency_status({"dependencies": dependency_requirements(scripts, "example/scripts")})["state"] == "UNSUPPORTED_REQUIREMENTS"
    assert SkillRuntime.dependency_status({})["state"] == "UNKNOWN"
    declared = {"SKILL.md": b"---\nname: Render\nrequires: ffmpeg\n---\n# Render"}
    assert not SkillRuntime.dependency_status({"dependencies": dependency_requirements(declared, "example/render")})["ready"]


def test_plain_skill_uses_existing_work_scoped_package_and_output_receipts(tmp_path):
    from app.agent_work_resources import AgentWorkResources
    raw = archive({"repo/LICENSE": b"MIT", "repo/SKILL.md": b"# Research", "repo/references/method.md": b"Use original work"})
    manifest, files = inspect_package(REPO, COMMIT, fetch=lambda _: raw)
    installed = install_package(tmp_path / "packages", manifest, files)
    resources = AgentWorkResources(tmp_path / "agent-work", tenant_id="tenant", company_id="company", work_ref="original-work", task_id="task")
    prepared = resources.prepare([{"skill_template_id": "skill", "manifest": manifest, "path": str(installed)}])
    assert prepared["receipt"]["work_ref"] == "original-work"
    assert prepared["receipt"]["skills"][0]["package_sha256"] == manifest["package_sha256"]
    (Path(prepared["cwd"]) / "output" / "result.md").write_text("synthetic source-backed result")
    receipts = resources.collect()
    assert receipts[0]["work_ref"] == "original-work" and receipts[0]["company_id"] == "company"
    assert receipts[0]["relative_path"] == "result.md"
