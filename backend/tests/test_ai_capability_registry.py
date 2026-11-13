import pytest

from app.ai_capability_registry import (
    AGENT_ADAPTER_REGISTRY,
    AICapabilityRegistry,
    PROVIDERS,
    ProviderConnectIn,
    _model_rows,
    scan_local_agents,
)
from app.tenant_context import TenantContext


class FakeDatabase:
    def __init__(self):
        self.saved = []

    def list_tenant_private_capabilities(self, *args, **kwargs):
        return []

    def save_tenant_private_capability(self, **kwargs):
        self.saved.append(kwargs)
        return kwargs


class FakeVault:
    def resolve(self, credential_ref):
        return {"secret": "test-secret"}


def test_provider_registry_has_no_static_model_ids_and_keeps_newapi_advanced():
    assert all("models" not in item for item in PROVIDERS.values())
    assert PROVIDERS["newapi"]["channel"] == "advanced_gateway"
    assert PROVIDERS["openai"]["channel"] == "official_byok"
    assert {"mistral", "xai", "groq", "siliconflow", "openrouter"} <= PROVIDERS.keys()


def _synthetic_app(application):
    import plistlib
    (application / "Contents/MacOS").mkdir(parents=True)
    (application / "Contents/Info.plist").write_bytes(plistlib.dumps({
        "CFBundlePackageType": "APPL", "CFBundleIdentifier": "test.synthetic.agent",
        "CFBundleExecutable": "synthetic-agent"}))
    executable = application / "Contents/MacOS/synthetic-agent"
    executable.write_bytes(b"synthetic; never run")
    executable.chmod(0o700)


def test_metadata_only_local_discovery_never_launches_or_reads_auth(tmp_path, monkeypatch):
    import app.ai_capability_registry as module
    executable = tmp_path / "codex"
    executable.write_bytes(b"synthetic installation; never run")
    executable.chmod(0o700)
    monkeypatch.setattr(module.shutil, "which", lambda name: str(executable) if name == "codex" else None)
    monkeypatch.setattr(module.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(module, "AGENT_ADAPTER_REGISTRY", {"codex": AGENT_ADAPTER_REGISTRY["codex"]})
    monkeypatch.setattr(module.subprocess, "run", lambda *_a, **_k: pytest.fail("discovery launched a process"))
    monkeypatch.setattr(module, "_run_probe", lambda *_: pytest.fail("discovery inspected auth"))
    rows = module.discover_local_agents()
    codex = next(row for row in rows if row["agent_id"] == "codex")
    assert codex["bindable"] is True
    assert codex["state"] == "Detected" and codex["authorized"] is None
    assert codex["available"] is False and codex["execution_ready"] is False
    metadata, status = module.local_agent_registration(
        {"local_agent_ref": codex["discovery_ref"], "execution_ready": True, "kind": "http"}, codex["capability_id"])
    assert status == "active" and metadata["kind"] == "codex-cli" and metadata["execution_ready"] is False
    executable.write_bytes(b"changed installation metadata")
    with pytest.raises(ValueError, match="安装已变化"):
        module.local_agent_registration({"local_agent_ref": codex["discovery_ref"]}, codex["capability_id"])


def test_metadata_discovery_keeps_unverified_cli_and_app_inactive(tmp_path, monkeypatch):
    import app.ai_capability_registry as module
    executable = tmp_path / "claude"
    executable.write_bytes(b"synthetic")
    executable.chmod(0o700)
    application = tmp_path / "WorkBuddy.app"
    _synthetic_app(application)
    monkeypatch.setattr(module.shutil, "which", lambda name: str(executable) if name == "claude" else None)
    monkeypatch.setattr(module.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(module, "AGENT_ADAPTER_REGISTRY", {
        "claude_code": {**AGENT_ADAPTER_REGISTRY["claude_code"], "applications": []},
        "workbuddy": {**AGENT_ADAPTER_REGISTRY["workbuddy"], "applications": [str(application)]},
    })
    rows = module.discover_local_agents()
    assert len(rows) == 2
    for row in rows:
        metadata, status = module.local_agent_registration({"local_agent_ref": row["discovery_ref"]}, row["capability_id"])
        assert row["bindable"] is False and status == "inactive"
        assert metadata["kind"] == "local-unverified" and metadata["execution_ready"] is False
        with pytest.raises(ValueError):
            module.local_agent_registration({"local_agent_ref": row["discovery_ref"]}, "forged-id")


def test_metadata_only_route_does_not_enter_legacy_probe(monkeypatch):
    import app.ai_capability_registry as module
    monkeypatch.setattr(module, "discover_local_agents", lambda *_: [{"state": "Detected"}])
    monkeypatch.setattr(module, "scan_local_capabilities", lambda: pytest.fail("legacy probing invoked"))
    router = module.build_ai_capability_router(FakeDatabase(), FakeVault())
    endpoint = next(route.endpoint for route in router.routes if route.path.endswith("/local"))
    assert endpoint(metadata_only=True) == {"agents": [{"state": "Detected"}], "local_model_providers": []}


def test_ollama_discovery_saves_existing_private_model_contract():
    database = FakeDatabase()
    service = AICapabilityRegistry(
        database,
        FakeVault(),
        http_get=lambda *_: {"models": [{"model": "qwen-local", "details": {"family": "qwen"}}]},
    )
    with TenantContext.scope("tenant-a"):
        result = service.connect("ollama", ProviderConnectIn())
    assert result["health"] == "healthy"
    assert result["models"][0]["model_id"] == "qwen-local"
    assert database.saved[0]["capability_type"] == "model"
    assert database.saved[0]["metadata"]["provider_protocol"] == "openai_chat"
    assert database.saved[0]["metadata"]["credential_ref"] == ""
    assert database.saved[0]["metadata"]["discovery_verification"] == {
        "status": "verified",
        "provider_id": "ollama",
        "discovery_id": "qwen-local",
        "model_id": "qwen-local",
        "mode": "dynamic",
        "requires_credential": False,
    }


def test_gemini_capability_uses_provider_metadata_not_brand_guessing():
    rows = _model_rows(
        {"models": [{"name": "models/example", "supportedGenerationMethods": ["generateContent", "embedContent"]}]},
        "gemini",
    )
    assert rows[0]["id"] == "models/example"


def test_ollama_capability_list_shape_is_supported():
    database = FakeDatabase()
    service = AICapabilityRegistry(
        database,
        FakeVault(),
        http_get=lambda *_: {"models": [{"model": "local", "capabilities": ["completion", "tools"]}]},
    )
    with TenantContext.scope("tenant-a"):
        result = service.connect("ollama", ProviderConnectIn(save=False))
    assert result["models"][0]["capability_profile"]["features"]["tool_calling"] == "supported"


def test_curated_provider_is_not_advertised_available_without_real_health():
    database = FakeDatabase()
    service = AICapabilityRegistry(database, FakeVault())
    with TenantContext.scope("tenant-a"):
        result = service.connect(
            "alibaba_qwen",
            ProviderConnectIn(credential_ref="local-dev://tenant/tenant-a/credential/c", model_ids=["manual-model"]),
        )
    assert result["health"] == "not_tested"
    assert result["available"] is False
    assert database.saved[0]["status"] == "inactive"


def test_local_agent_registry_hides_undetected_products_and_keeps_detection_generic():
    def command_status(command):
        return (True, "codex-cli test") if command == "codex" else (False, "")

    agents = scan_local_agents(
        command_status=command_status,
        path_exists=lambda _path: False,
        authorization_probe=lambda _command, _arguments: True,
    )

    assert [item["agent_id"] for item in agents] == ["codex"]
    assert agents[0]["available"] is True
    assert {"codex", "claude_code", "trae", "cursor", "openclaw"} <= AGENT_ADAPTER_REGISTRY.keys()


def test_detected_gui_without_cli_is_not_advertised_as_importable():
    agents = scan_local_agents(
        command_status=lambda _command: (False, ""),
        path_exists=lambda path: path == "/Applications/Cursor.app",
    )

    assert [item["agent_id"] for item in agents] == ["cursor"]
    assert agents[0]["state"] == "Detected"
    assert agents[0]["programmatic_import_supported"] is False
    assert agents[0]["current_limitation"] == "DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED"

    service_agents = scan_local_agents(
        command_status=lambda _command: (False, ""),
        path_exists=lambda _path: False,
        service_status=lambda url: url == "http://127.0.0.1:9999/health",
        registry={"service_agent": {
            "name": "Service Agent", "commands": [], "applications": [], "config_paths": [],
            "service_urls": ["http://127.0.0.1:9999/health"], "authorization_probe": [],
            "adapter_readiness": "LIVE", "authorization_required": False,
            "programmatic_import_supported": True,
        }},
    )
    assert service_agents[0]["configured"] is True
    assert service_agents[0]["programmatic_import_supported"] is True


def test_manual_public_app_is_unverified_and_revalidated(tmp_path, monkeypatch):
    import app.ai_capability_registry as module
    root = tmp_path / "Applications"
    root.mkdir()
    application = root / "Unknown Agent.app"
    _synthetic_app(application)
    monkeypatch.setattr(module, "LOCAL_APPLICATION_ROOT", root)
    monkeypatch.setattr(module.subprocess, "run", lambda *_a, **_k: pytest.fail("launched app"))
    row, = module.discover_local_agents(str(application))
    assert row["manual_selection"] and not row["bindable"] and not row["execution_ready"]
    metadata = {"local_agent_ref": row["discovery_ref"], "local_installation_path": str(application), "kind": "codex-cli"}
    normalized, status = module.local_agent_registration(metadata, row["capability_id"])
    assert status == "inactive" and normalized["kind"] == "local-unverified"
    with pytest.raises(ValueError):
        module.discover_local_agents(str(tmp_path / "Private.app"))
    (application / "changed").mkdir()
    with pytest.raises(ValueError):
        module.local_agent_registration(metadata, row["capability_id"])


def test_additional_brands_have_metadata_entries_without_execution_claim():
    for agent in ("deepseek_harness", "zcode", "workbuddy"):
        assert AGENT_ADAPTER_REGISTRY[agent]["applications"]
        assert AGENT_ADAPTER_REGISTRY[agent]["adapter_readiness"] == "UNVERIFIED"
    assert "traecli" in AGENT_ADAPTER_REGISTRY["trae"]["commands"]


@pytest.mark.parametrize("invalid", ["empty", "malformed", "missing_id", "wrong_type", "traversal", "missing_executable", "metadata_symlink", "executable_symlink"])
def test_public_app_identity_rejects_invalid_bundles(tmp_path, monkeypatch, invalid):
    import plistlib
    import app.ai_capability_registry as module
    root = tmp_path / "Applications"
    root.mkdir()
    app = root / "Invalid.app"
    monkeypatch.setattr(module, "LOCAL_APPLICATION_ROOT", root)
    if invalid == "empty":
        app.mkdir()
    else:
        _synthetic_app(app)
        metadata = app / "Contents/Info.plist"
        data = plistlib.loads(metadata.read_bytes())
        if invalid == "malformed": metadata.write_bytes(b"<plist>broken")
        elif invalid == "missing_id":
            data.pop("CFBundleIdentifier"); metadata.write_bytes(plistlib.dumps(data))
        elif invalid == "wrong_type":
            data["CFBundlePackageType"] = "BNDL"; metadata.write_bytes(plistlib.dumps(data))
        elif invalid == "traversal":
            data["CFBundleExecutable"] = "../../outside"; metadata.write_bytes(plistlib.dumps(data))
        elif invalid == "missing_executable": (app / "Contents/MacOS/synthetic-agent").unlink()
        elif invalid == "metadata_symlink":
            outside = root / "outside.plist"; outside.write_bytes(metadata.read_bytes()); metadata.unlink(); metadata.symlink_to(outside)
        else:
            binary = app / "Contents/MacOS/synthetic-agent"
            outside = root / "outside"; outside.write_bytes(b"synthetic"); outside.chmod(0o700)
            binary.unlink(); binary.symlink_to(outside)
    with pytest.raises(ValueError): module.discover_local_agents(str(app))


def test_registration_rechecks_changed_bundle_metadata_and_executable(tmp_path, monkeypatch):
    import plistlib
    import app.ai_capability_registry as module
    root = tmp_path / "Applications"; root.mkdir()
    application = root / "Valid.app"; _synthetic_app(application)
    monkeypatch.setattr(module, "LOCAL_APPLICATION_ROOT", root)
    row, = module.discover_local_agents(str(application))
    metadata = {"local_agent_ref": row["discovery_ref"], "local_installation_path": str(application)}
    path = application / "Contents/Info.plist"
    data = plistlib.loads(path.read_bytes()); data["CFBundleIdentifier"] = "test.changed"
    path.write_bytes(plistlib.dumps(data))
    with pytest.raises(ValueError): module.local_agent_registration(metadata, row["capability_id"])
    row, = module.discover_local_agents(str(application))
    metadata["local_agent_ref"] = row["discovery_ref"]
    (application / "Contents/MacOS/synthetic-agent").chmod(0o600)
    with pytest.raises(ValueError): module.local_agent_registration(metadata, row["capability_id"])


def _synthetic_acp_installation(tmp_path, monkeypatch):
    import hashlib
    import plistlib
    import app.ai_capability_registry as module
    application = tmp_path / "Synthetic DSH.app"
    _synthetic_app(application)
    path = application / "Contents/Info.plist"
    metadata = plistlib.loads(path.read_bytes()); metadata["CFBundleShortVersionString"] = "synthetic"
    path.write_bytes(plistlib.dumps(metadata))
    launcher = application / "Contents/MacOS/synthetic-agent"
    definition = {"application": str(application), "bundle_id": "test.synthetic.agent", "version": "synthetic",
        "launcher": "Contents/MacOS/synthetic-agent", "files": {"Contents/MacOS/synthetic-agent": hashlib.sha256(launcher.read_bytes()).hexdigest()},
        "args": ["--profile", "acp"], "profile_directory": ".dsh/profiles/acp", "profile_environment": {"DSH_HOME": ".dsh"}}
    monkeypatch.setattr(module, "ACP_INSTALLATIONS", {"deepseek_harness": definition})
    monkeypatch.setattr(module, "AGENT_ADAPTER_REGISTRY", {"deepseek_harness": {
        "name": "Synthetic DSH", "commands": [], "applications": [str(application)], "adapter_readiness": "UNVERIFIED"}})
    return module.acp_installation("deepseek_harness"), launcher


def test_verified_dsh_discovery_registers_bindable_configuration_without_execution(tmp_path, monkeypatch):
    import app.ai_capability_registry as module
    installation, launcher = _synthetic_acp_installation(tmp_path, monkeypatch)
    monkeypatch.setattr(module.subprocess, "run", lambda *_a, **_k: pytest.fail("Agent started"))
    row, = module.discover_local_agents()
    assert row["bindable"] and not row["execution_ready"] and not row["available"]
    metadata, status = module.local_agent_registration({"local_agent_ref": row["discovery_ref"], "kind": "forged"}, row["capability_id"])
    assert status == "active" and metadata["kind"] == "acp-stdio"
    assert metadata["installation_ref"] == installation["installation_ref"]
    assert not metadata["execution_ready"] and "computer_access_intent" not in metadata
    assert metadata["dsh_shared_account"] is False
    shared, _ = module.local_agent_registration({"local_agent_ref": row["discovery_ref"],
        "dsh_shared_account": True, "profile_home": "/forged", "credential_ref": "forged"}, row["capability_id"])
    assert shared["dsh_shared_account"] is True
    assert "profile_home" not in shared and "credential_ref" not in shared
    for consent in ("true", 1, None, {}):
        with pytest.raises(ValueError):
            module.local_agent_registration({"local_agent_ref": row["discovery_ref"], "dsh_shared_account": consent}, row["capability_id"])
    launcher.write_bytes(b"drift")
    with pytest.raises(ValueError): module.local_agent_registration({"local_agent_ref": row["discovery_ref"]}, row["capability_id"])
