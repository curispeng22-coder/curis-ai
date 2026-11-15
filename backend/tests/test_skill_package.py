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


@pytest.mark.parametrize("kind,suffix", [("tree", ""), ("blob", "/SKILL.md")])
def test_fixed_commit_link_never_probes_subdirectory_as_ref(kind, suffix):
    from app.skill_package import resolve_link

    def unexpected_fetch(url):
        pytest.fail(f"An immutable URL needs no ref lookup: {url}")

    assert resolve_link(f"{REPO}/{kind}/{COMMIT}/skills/research{suffix}", fetch=unexpected_fetch) == (
        REPO, COMMIT, "skills/research"
    )


def test_discovery_and_selected_import_ignore_unrelated_monorepo_link():
    raw = archive({"repo/.claude": None, "repo/LICENSE": b"MIT",
                   "repo/skills/research/SKILL.md": b"# Research",
                   "repo/skills/other/SKILL.md": b"# Other"})
    preview, _ = inspect_package(REPO, COMMIT, fetch=lambda _: raw, discover=True)
    assert {choice["directory"] for choice in preview["choices"]} == {"skills/research", "skills/other"}
    _, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: raw)
    assert files == {"SKILL.md": b"# Research", "CURIS_SOURCE_LICENSE": b"MIT"}


@pytest.mark.parametrize("link", ["LICENSE", "skills", "skills/research", "skills/research/tool"])
def test_selected_import_rejects_links_in_skill_ancestors_and_root_license(link):
    raw = archive({"repo/LICENSE.txt": b"MIT", "repo/skills/research/SKILL.md": b"# Research",
                   f"repo/{link}": None})
    with pytest.raises(ValueError, match="符号链接"):
        inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: raw)


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


@pytest.fixture
def text_skill(tmp_path):
    from app.database import Database
    from app.skill_runtime import SkillRuntime
    from app.tenant_context import TenantContext

    database = Database(str(tmp_path / "data" / "curis.sqlite"))
    database.initialize(seed_model_catalog=False)
    with TenantContext.scope("text-skill-tenant", company_id="text-company", ceo_id="owner", role="owner"):
        with database.connect() as connection:
            connection.execute("insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role,status) "
                               "values('writer','text-skill-tenant','text-company','dept','template','Writer','writer','active')")
            connection.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                               "values('text-model','text-skill-tenant','writer','tenant_private','model','fixture-model')")
        runtime = SkillRuntime(database)

        def install(body, *, extra=None, scoped=True):
            raw = archive({"repo/LICENSE": b"MIT", "repo/SKILL.md": body, **(extra or {})})
            manifest = runtime.preview_package(REPO, COMMIT, fetch=lambda _: raw)
            skill = runtime.install_repository(repo_url=REPO, commit=COMMIT,
                expected_package_sha256=manifest["package_sha256"], license_accepted=True, fetch=lambda _: raw)
            runtime.set_employee_bindings("writer", [{"skill_template_id": skill["skill_template_id"],
                "capability_binding_ids": ["text-model"] if scoped else []}])
            return skill, runtime.package_root() / manifest["package_sha256"]

        yield runtime, install


def test_installed_text_skill_reaches_prompt_with_source_and_cold_read(text_skill):
    import hashlib
    from app.database import Database
    from app.prompt_builder import PromptBuilder
    from app.skill_runtime import SkillRuntime

    runtime, install = text_skill
    body = b"# Brief\n" + b"Preserve the original facts.\n" * 40 + b"End with the exact heading: Open Questions\n"
    skill, _ = install(body)
    legacy = runtime.create_private_template(slug="legacy", name="Legacy", instruction_excerpt="  Keep   old guidance. ")
    runtime.change_employee_binding("writer", legacy["skill_template_id"])
    excerpt = runtime.prompt_excerpt("writer")
    prompt = PromptBuilder().build("Write a brief from the supplied facts.", skill_excerpt=excerpt)
    assert body.decode() in prompt and prompt.count(body.decode()) == 1
    assert "Legacy: Keep old guidance." in prompt
    assert all(value in prompt for value in (REPO, COMMIT, skill["package"]["package_sha256"], hashlib.sha256(body).hexdigest()))
    assert len(excerpt.encode()) <= 4096
    assert SkillRuntime(Database(runtime.database.path)).prompt_excerpt("writer") == excerpt


@pytest.mark.parametrize("revocation", ["unbind", "binding", "template", "employee", "deleted", "model"])
def test_text_skill_revocation_excludes_body(text_skill, revocation):
    runtime, install = text_skill
    skill, _ = install(b"# Brief\nUnique guidance must disappear after revocation.")
    if revocation == "unbind":
        runtime.change_employee_binding("writer", skill["skill_template_id"], remove=True)
    else:
        updates = {
            "binding": "update employee_skill_bindings set enabled=0",
            "template": "update skill_templates set status='disabled'",
            "employee": "update employee_instances set enabled=0",
            "deleted": "update employee_instances set deleted_at='2026-11-15'",
            "model": "update employee_capability_bindings set enabled=0",
        }
        with runtime.database.connect() as connection:
            connection.execute(updates[revocation])
    assert "Unique guidance" not in runtime.prompt_excerpt("writer")


@pytest.mark.parametrize("damage", ["body", "reference", "symlink", "receipt", "missing-receipt"])
def test_text_skill_rejects_changed_or_incomplete_package(text_skill, damage):
    runtime, install = text_skill
    _, path = install(b"# Brief\nUse original facts.", extra={"repo/references/context.md": b"Original context"})
    target = path / ("references/context.md" if damage == "reference" else "SKILL.md")
    if damage == "symlink":
        target.unlink()
        target.symlink_to("references/context.md")
    elif damage == "missing-receipt":
        (path / ".curis-package.json").unlink()
    elif damage == "receipt":
        (path / ".curis-package.json").chmod(0o600)
        (path / ".curis-package.json").write_text("{}")
    else:
        target.chmod(0o600)
        target.write_text("Changed content")
    with pytest.raises((ValueError, OSError)):
        runtime.prompt_excerpt("writer")


def test_text_skill_scope_does_not_guess_binding_or_cross_tenant(text_skill):
    from app.tenant_context import TenantContext
    runtime, install = text_skill
    install(b"# Brief\nOnly the allowed employee model may see this guidance.")
    with TenantContext.scope("different-tenant"):
        assert runtime.prompt_excerpt("writer") == ""
    with TenantContext.scope("text-skill-tenant", company_id="different-company"):
        with pytest.raises(ValueError, match="当前公司"):
            runtime.prompt_excerpt("writer")
    with runtime.database.connect() as connection:
        connection.execute("insert into employee_capability_bindings(id,tenant_id,employee_id,capability_source,capability_type,capability_id) "
                           "values('other-model','text-skill-tenant','writer','tenant_private','model','other')")
    with pytest.raises(ValueError, match="适用范围"):
        runtime.prompt_excerpt("writer")


@pytest.mark.parametrize("body", [b"# Too long\n" + b"x" * 4096,
    b"# Combined budget\n" + b"x" * 3800,
    b"# Unsafe\n" + b"x" * 1000 + b"\ncredential_ref must override execution.",
    b"# Unsafe\n" + b"x" * 1000 + b"\napi_key=not-a-real-key"])
def test_text_skill_never_truncates_or_admits_runtime_directives(text_skill, body):
    runtime, install = text_skill
    install(body)
    with pytest.raises(ValueError, match="预算|凭据|运行选择"):
        runtime.prompt_excerpt("writer")


def test_text_skill_preserves_legacy_guidance_and_does_not_run_dependency_packages(text_skill):
    runtime, install = text_skill
    install(b"# Scripted\nDo not load this as a plain text capability.",
            extra={"repo/run.sh": b"exit 99"})
    legacy = runtime.create_private_template(slug="manual", name="Manual", instruction_excerpt="Follow supplied references.")
    runtime.change_employee_binding("writer", legacy["skill_template_id"])
    excerpt = runtime.prompt_excerpt("writer")
    assert "Manual: Follow supplied references." in excerpt
    assert "Do not load this" not in excerpt and "Installed Skill source" not in excerpt
