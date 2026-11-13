from __future__ import annotations

import hashlib
import json
import plistlib
import shutil
import stat
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable
from xml.parsers.expat import ExpatError
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .tenant_context import TenantContext


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


# Provider definitions describe supply and protocol only. Model IDs always come
# from provider discovery or an explicit user selection.
PROVIDERS: dict[str, dict[str, Any]] = {
    "openai": {
        "name": "OpenAI", "channel": "official_byok", "base_url": "https://api.openai.com",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://platform.openai.com/docs/api-reference/models/list",
    },
    "anthropic": {
        "name": "Anthropic", "channel": "official_byok", "base_url": "https://api.anthropic.com",
        "auth": "anthropic_key", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "anthropic_messages", "chat_path": "/v1/messages",
        "documentation": "https://platform.claude.com/docs/en/api/models/list",
    },
    "gemini": {
        "name": "Google Gemini", "channel": "official_byok",
        "base_url": "https://generativelanguage.googleapis.com", "auth": "google_key",
        "discovery_path": "/v1beta/models", "discovery_mode": "dynamic",
        "protocol": "gemini_generate_content", "chat_path": "",
        "documentation": "https://ai.google.dev/api/models",
    },
    "deepseek": {
        "name": "DeepSeek", "channel": "official_byok", "base_url": "https://api.deepseek.com",
        "auth": "bearer", "discovery_path": "/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://api-docs.deepseek.com/api/list-models",
    },
    "alibaba_qwen": {
        "name": "Alibaba Cloud Model Studio / Qwen", "channel": "official_byok",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode", "auth": "bearer",
        "discovery_path": "", "discovery_mode": "curated",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://help.aliyun.com/en/model-studio/what-is-model-studio",
    },
    "volcengine_doubao": {
        "name": "Volcengine Ark / Doubao", "channel": "official_byok",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3", "auth": "bearer",
        "discovery_path": "", "discovery_mode": "curated",
        "protocol": "openai_chat", "chat_path": "/chat/completions",
        "documentation": "https://www.volcengine.com/docs/82379/1874970",
    },
    "zhipu": {
        "name": "Zhipu", "channel": "official_byok",
        "base_url": "https://open.bigmodel.cn/api/paas/v4", "auth": "bearer",
        "discovery_path": "", "discovery_mode": "curated",
        "protocol": "openai_chat", "chat_path": "/chat/completions",
        "documentation": "https://docs.bigmodel.cn/api-reference/模型-api/对话补全",
    },
    "minimax": {
        "name": "MiniMax", "channel": "official_byok", "base_url": "https://api.minimaxi.com",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://platform.minimaxi.com/docs/api-reference/models/openai/list-models",
    },
    "moonshot_kimi": {
        "name": "Moonshot AI / Kimi", "channel": "official_byok",
        "base_url": "https://api.moonshot.cn", "auth": "bearer",
        "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://platform.moonshot.cn/docs/api-reference",
    },
    "mistral": {
        "name": "Mistral AI", "channel": "official_byok", "base_url": "https://api.mistral.ai",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://docs.mistral.ai/api/endpoint/models",
    },
    "xai": {
        "name": "xAI", "channel": "official_byok", "base_url": "https://api.x.ai",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://docs.x.ai/developers/rest-api-reference/inference/models",
    },
    "groq": {
        "name": "GroqCloud", "channel": "official_byok", "base_url": "https://api.groq.com/openai",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://console.groq.com/docs/models",
    },
    "siliconflow": {
        "name": "SiliconFlow / 硅基流动", "channel": "official_byok",
        "base_url": "https://api.siliconflow.cn", "auth": "bearer",
        "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://docs.siliconflow.cn/en/api-reference/models/get-model-list",
    },
    "openrouter": {
        "name": "OpenRouter", "channel": "advanced_gateway", "base_url": "https://openrouter.ai/api",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions",
        "documentation": "https://openrouter.ai/docs/guides/overview/models",
    },
    "newapi": {
        "name": "New API / Aggregated Gateway", "channel": "advanced_gateway", "base_url": "",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions", "custom_base_url": True,
        "documentation": "https://github.com/QuantumNous/new-api",
    },
    "openai_compatible": {
        "name": "OpenAI Compatible", "channel": "advanced_gateway", "base_url": "",
        "auth": "bearer", "discovery_path": "/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions", "custom_base_url": True,
        "documentation": "",
    },
    "ollama": {
        "name": "Ollama", "channel": "local_model", "base_url": "http://127.0.0.1:11434",
        "auth": "none", "discovery_path": "/api/tags", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions", "custom_base_url": True,
        "documentation": "https://docs.ollama.com/api/tags",
    },
    "lm_studio": {
        "name": "LM Studio", "channel": "local_model", "base_url": "http://127.0.0.1:1234",
        "auth": "optional_bearer", "discovery_path": "/api/v1/models", "discovery_mode": "dynamic",
        "protocol": "openai_chat", "chat_path": "/v1/chat/completions", "custom_base_url": True,
        "documentation": "https://lmstudio.ai/docs/developer/rest",
    },
}


# Internal compatibility knowledge. The ordinary-user API only returns entries
# actually detected on the current machine; it never renders this registry as an
# Agent brand catalog.
AGENT_ADAPTER_REGISTRY: dict[str, dict[str, Any]] = {
    "chatgpt_app": {
        "name": "ChatGPT App", "vendor": "OpenAI", "region": "global", "type": "general_agent",
        "commands": [], "applications": ["/Applications/ChatGPT.app"], "authorization_probe": [],
        "config_paths": [], "service_urls": [], "interface": "gui_only_unverified",
        "adapter_readiness": "UNVERIFIED", "authorization_required": True, "programmatic_import_supported": False,
    },
    "workbuddy": {
        "name": "WorkBuddy", "vendor": "Tencent", "region": "unknown", "type": "general_agent",
        "commands": [], "applications": ["/Applications/WorkBuddy.app"], "authorization_probe": [],
        "config_paths": [], "service_urls": [], "interface": "machine_interface_unverified",
        "adapter_readiness": "UNVERIFIED", "authorization_required": True, "programmatic_import_supported": False,
    },
    "deepseek_harness": {
        "name": "DeepSeek Harness", "vendor": "DeepSeek", "region": "unknown", "type": "general_agent",
        "commands": [], "applications": ["/Applications/DeepSeek Harness.app"], "authorization_probe": [],
        "config_paths": [], "service_urls": [], "interface": "machine_interface_unverified",
        "adapter_readiness": "UNVERIFIED", "authorization_required": True, "programmatic_import_supported": False,
    },
    "zcode": {
        "name": "ZCode", "vendor": "Z.ai", "region": "unknown", "type": "coding_agent",
        "commands": [], "applications": ["/Applications/ZCode.app"], "authorization_probe": [],
        "config_paths": [], "service_urls": [], "interface": "machine_interface_unverified",
        "adapter_readiness": "UNVERIFIED", "authorization_required": True, "programmatic_import_supported": False,
    },
    "codex": {
        "name": "Codex", "vendor": "OpenAI", "region": "global", "type": "coding_agent",
        "commands": ["codex"], "applications": [], "authorization_probe": ["login", "status"],
        "config_paths": ["~/.codex"], "service_urls": [],
        "interface": "cli_jsonl", "adapter_readiness": "LIVE", "authorization_required": True,
        "programmatic_import_supported": True,
    },
    "claude_code": {
        "name": "Claude Code", "vendor": "Anthropic", "region": "global", "type": "coding_agent",
        "commands": ["claude"], "applications": [], "authorization_probe": [],
        "config_paths": ["~/.claude"], "service_urls": [],
        "interface": "cli_json_stream", "adapter_readiness": "RESEARCHED", "authorization_required": True,
        "programmatic_import_supported": True,
    },
    "trae": {
        "name": "TRAE", "vendor": "ByteDance", "region": "china_global", "type": "coding_agent",
        "commands": ["traecli", "trae-cli"], "applications": ["/Applications/TRAE.app", "/Applications/Trae.app"],
        "config_paths": ["~/.trae"], "service_urls": [],
        "authorization_probe": [], "interface": "cli_or_gui", "adapter_readiness": "RESEARCHED",
        "authorization_required": True, "programmatic_import_supported": True,
    },
    "cursor": {
        "name": "Cursor", "vendor": "Anysphere", "region": "global", "type": "coding_agent",
        "commands": ["cursor-agent"], "applications": ["/Applications/Cursor.app"],
        "config_paths": ["~/.cursor"], "service_urls": [],
        "authorization_probe": [], "interface": "cli_stream_json", "adapter_readiness": "RESEARCHED",
        "authorization_required": True, "programmatic_import_supported": True,
    },
    "openclaw": {
        "name": "OpenClaw", "vendor": "OpenClaw", "region": "global", "type": "general_agent",
        "commands": ["openclaw"], "applications": [], "authorization_probe": [],
        "config_paths": ["~/.openclaw"], "service_urls": [],
        "interface": "cli_json_or_acp", "adapter_readiness": "RESEARCHED", "authorization_required": True,
        "programmatic_import_supported": True,
    },
    "gemini_cli": {
        "name": "Gemini CLI", "vendor": "Google", "region": "global", "type": "coding_agent",
        "commands": ["gemini"], "applications": [], "authorization_probe": [],
        "config_paths": ["~/.gemini"], "service_urls": [],
        "interface": "cli_json_stream", "adapter_readiness": "RESEARCHED", "authorization_required": True,
        "programmatic_import_supported": True,
    },
    "github_copilot_cli": {
        "name": "GitHub Copilot CLI", "vendor": "GitHub", "region": "global", "type": "coding_agent",
        "commands": ["copilot"], "applications": [], "authorization_probe": [],
        "config_paths": [], "service_urls": [],
        "interface": "cli", "adapter_readiness": "RESEARCHED", "authorization_required": True,
        "programmatic_import_supported": True,
    },
}


class ProviderConnectIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    credential_ref: str = ""
    base_url: str = ""
    model_ids: list[str] = Field(default_factory=list)
    save: bool = True


def _safe_base_url(value: str) -> str:
    parsed = urlparse(value.rstrip("/"))
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("base_url must be an http(s) URL without embedded credentials")
    if parsed.scheme == "http" and parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("plain HTTP is allowed only for a loopback local provider")
    return value.rstrip("/")


def _profile(raw: dict[str, Any], provider_id: str) -> dict[str, Any]:
    supported = set(raw.get("supportedGenerationMethods") or [])
    lm_capabilities = raw.get("capabilities") or {}
    if isinstance(lm_capabilities, list):
        lm_capabilities = {str(item): True for item in lm_capabilities}
    elif not isinstance(lm_capabilities, dict):
        lm_capabilities = {}
    features = {
        "chat": "supported",
        "reasoning": "unknown",
        "coding": "unknown",
        "vision": "supported" if lm_capabilities.get("vision") else "unknown",
        "image": "unknown",
        "audio": "unknown",
        "embedding": "supported" if "embedContent" in supported else "unknown",
        "tool_calling": "supported" if (
            lm_capabilities.get("trained_for_tool_use") or lm_capabilities.get("tools")
        ) else "unknown",
        "structured_output": "unknown",
        "context": raw.get("inputTokenLimit") or raw.get("max_context_length"),
        "location": "local" if provider_id in {"ollama", "lm_studio"} else "cloud",
    }
    return {
        "features": features,
        "evidence": "provider_api" if supported or lm_capabilities else "conservative_curis_default",
        "cost": {"status": "unknown", "source": PROVIDERS[provider_id]["documentation"]},
        "availability": "available",
    }


def _model_rows(payload: dict[str, Any], provider_id: str) -> list[dict[str, Any]]:
    if provider_id == "ollama":
        rows = payload.get("models") or []
        return [{"id": row.get("model") or row.get("name"), "raw": row} for row in rows]
    if provider_id == "lm_studio":
        rows = payload.get("models") or payload.get("data") or []
        return [{"id": row.get("key") or row.get("id"), "raw": row} for row in rows]
    if provider_id == "gemini":
        rows = payload.get("models") or []
        return [{"id": row.get("name"), "raw": row} for row in rows]
    rows = payload.get("data") or []
    return [{"id": row.get("id"), "raw": row} for row in rows]


class AICapabilityRegistry:
    def __init__(
        self,
        database,
        credential_vault,
        *,
        http_get: Callable[[str, dict[str, str], int], dict[str, Any]] | None = None,
    ) -> None:
        self.database = database
        self.credential_vault = credential_vault
        self.http_get = http_get or self._http_get

    def providers(self) -> list[dict[str, Any]]:
        configured = {
            (item.get("metadata") or {}).get("provider_type")
            for item in self.database.list_tenant_private_capabilities(
                TenantContext.current_tenant_id(), capability_type="model", include_inactive=True
            )
        }
        return [
            {
                "provider_id": provider_id,
                **definition,
                "credential_sources": ["USER", "PLATFORM"],
                "current_credential_source": "USER",
                "configured": provider_id in configured,
            }
            for provider_id, definition in PROVIDERS.items()
        ]

    def connect(self, provider_id: str, payload: ProviderConnectIn) -> dict[str, Any]:
        try:
            definition = PROVIDERS[provider_id]
        except KeyError as error:
            raise ValueError("provider is not registered") from error
        base_url = _safe_base_url(payload.base_url or definition["base_url"])
        if (
            payload.base_url
            and not definition.get("custom_base_url")
            and base_url != str(definition["base_url"]).rstrip("/")
        ):
            raise ValueError("custom base_url is not allowed for this official provider")
        secret = ""
        resolve_for_provider = getattr(self.credential_vault, "resolve_for_provider", None)
        resolve_credential = (
            (lambda credential_ref: resolve_for_provider(credential_ref, provider_id))
            if callable(resolve_for_provider)
            else self.credential_vault.resolve
        )
        if definition["auth"] not in {"none", "optional_bearer"}:
            if not payload.credential_ref:
                raise ValueError("credential_ref is required")
            secret = resolve_credential(payload.credential_ref)["secret"]
        elif payload.credential_ref:
            secret = resolve_credential(payload.credential_ref)["secret"]

        headers = {"Accept": "application/json"}
        if definition["auth"] == "anthropic_key":
            headers.update({"x-api-key": secret, "anthropic-version": "2023-06-01"})
        elif definition["auth"] == "google_key":
            headers["x-goog-api-key"] = secret
        elif secret:
            headers["Authorization"] = f"Bearer {secret}"

        mode = definition["discovery_mode"]
        if mode == "dynamic":
            response = self.http_get(base_url + definition["discovery_path"], headers, 15)
            discovered = _model_rows(response, provider_id)
        else:
            discovered = [{"id": model_id, "raw": {}} for model_id in payload.model_ids]

        tenant_id = TenantContext.current_tenant_id()
        previous = [
            item
            for item in self.database.list_tenant_private_capabilities(
                tenant_id, capability_type="model", include_inactive=True
            )
            if (item.get("metadata") or {}).get("provider_type") == provider_id
        ]
        models = []
        discovered_ids: set[str] = set()
        for discovered_model in discovered:
            model_id = str(discovered_model.get("id") or "").strip()
            if not model_id or len(model_id) > 256 or any(ord(character) < 32 for character in model_id):
                continue
            profile = _profile(discovered_model.get("raw") or {}, provider_id)
            if mode != "dynamic":
                profile["availability"] = "configured"
            capability_id = "user.%s.%s" % (
                provider_id,
                hashlib.sha256(model_id.encode("utf-8")).hexdigest()[:16],
            )
            discovered_ids.add(capability_id)
            item = {
                "capability_id": capability_id,
                "model_id": model_id,
                "display_name": model_id.removeprefix("models/"),
                "capability_profile": profile,
            }
            if payload.save:
                self.database.save_tenant_private_capability(
                    tenant_id=TenantContext.current_tenant_id(),
                    capability_type="model",
                    capability_id=capability_id,
                    display_name=item["display_name"],
                    metadata={
                        "name": item["display_name"],
                        "provider_type": provider_id,
                        "base_url": base_url,
                        "model_name": model_id.removeprefix("models/"),
                        "credential_ref": payload.credential_ref,
                        "credential_source": "USER",
                        "provider_protocol": definition["protocol"],
                        "chat_path": definition["chat_path"],
                        "capability_profile": profile,
                        "discovery_verification": {
                            "status": "verified" if mode == "dynamic" else "not_tested",
                            "provider_id": provider_id,
                            "discovery_id": model_id,
                            "model_id": model_id.removeprefix("models/"),
                            "mode": mode,
                            "requires_credential": definition["auth"]
                            not in {"none", "optional_bearer"},
                        },
                    },
                    status="active" if mode == "dynamic" else "inactive",
                )
            models.append(item)
        if payload.save and mode == "dynamic":
            for stale in previous:
                if stale["capability_id"] in discovered_ids:
                    continue
                metadata = dict(stale.get("metadata") or {})
                verification = dict(metadata.get("discovery_verification") or {})
                verification.update({"status": "unavailable", "provider_id": provider_id})
                metadata["discovery_verification"] = verification
                self.database.save_tenant_private_capability(
                    tenant_id=tenant_id,
                    capability_type="model",
                    capability_id=stale["capability_id"],
                    display_name=stale.get("display_name") or stale["capability_id"],
                    metadata=metadata,
                    status="inactive",
                )
        return {
            "provider_id": provider_id,
            "channel": definition["channel"],
            "credential_source": "USER",
            "discovery_mode": mode,
            "health": "healthy" if mode == "dynamic" else "not_tested",
            "available": bool(models) and mode == "dynamic",
            "models": models,
            "saved": payload.save,
        }

    def recover(self, provider_id: str) -> dict[str, Any]:
        """Revalidate one configured provider from persisted non-secret metadata."""
        try:
            definition = PROVIDERS[provider_id]
        except KeyError as error:
            raise ValueError("provider is not registered") from error
        capabilities = [
            item
            for item in self.database.list_tenant_private_capabilities(
                TenantContext.current_tenant_id(), capability_type="model", include_inactive=True
            )
            if (item.get("metadata") or {}).get("provider_type") == provider_id
        ]
        if not capabilities:
            raise ValueError("provider has no saved model configuration")
        metadata_rows = [item.get("metadata") or {} for item in capabilities]
        credential_refs = {
            str(metadata.get("credential_ref") or "")
            for metadata in metadata_rows
            if metadata.get("credential_ref")
        }
        if definition["auth"] not in {"none", "optional_bearer"} and len(credential_refs) != 1:
            raise ValueError("provider credential configuration is missing or ambiguous")
        if len(credential_refs) > 1:
            raise ValueError("provider credential configuration is ambiguous")
        base_urls = {
            str(metadata.get("base_url") or definition["base_url"])
            for metadata in metadata_rows
        }
        if len(base_urls) != 1:
            raise ValueError("provider endpoint configuration is ambiguous")
        model_ids = sorted(
            {
                str(metadata.get("model_name") or "")
                for metadata in metadata_rows
                if metadata.get("model_name")
            }
        )
        return self.connect(
            provider_id,
            ProviderConnectIn(
                credential_ref=next(iter(credential_refs), ""),
                base_url=next(iter(base_urls)),
                model_ids=model_ids,
                save=True,
            ),
        )

    @staticmethod
    def _http_get(url: str, headers: dict[str, str], timeout: int) -> dict[str, Any]:
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.build_opener(_NoRedirect).open(request, timeout=timeout) as response:
                raw = response.read(2_000_001)
        except urllib.error.HTTPError as error:
            raise ValueError(f"provider connection failed with HTTP {error.code}") from error
        except (OSError, urllib.error.URLError) as error:
            raise ValueError("provider connection failed") from error
        if len(raw) > 2_000_000:
            raise ValueError("provider model response is too large")
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("provider model response is not valid JSON") from error
        if not isinstance(payload, dict):
            raise ValueError("provider model response is not an object")
        return payload


def _command_status(command: str) -> tuple[bool, str]:
    from .agent_adapter import local_codex_executable
    path = local_codex_executable() if command == "codex" else shutil.which(command)
    if not path:
        return False, ""
    try:
        result = subprocess.run(
            [path, "--version"], capture_output=True, text=True, timeout=4, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return True, ""
    version = (result.stdout or result.stderr).strip().splitlines()
    return True, version[0][:160] if version else ""


def _run_probe(command: str, arguments: list[str]) -> bool:
    from .agent_adapter import local_codex_executable
    executable = local_codex_executable() if command == "codex" else shutil.which(command)
    if not executable:
        return False
    try:
        return subprocess.run(
            [executable, *arguments],
            capture_output=True, text=True, timeout=5, check=False,
        ).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _service_status(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        return False
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status < 500
    except (OSError, urllib.error.URLError, ValueError):
        return False


def scan_local_agents(
    *,
    command_status: Callable[[str], tuple[bool, str]] | None = None,
    path_exists: Callable[[str], bool] | None = None,
    authorization_probe: Callable[[str, list[str]], bool] | None = None,
    service_status: Callable[[str], bool] | None = None,
    registry: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    command_status = command_status or _command_status
    path_exists = path_exists or (lambda value: Path(value).expanduser().exists())
    authorization_probe = authorization_probe or _run_probe
    service_status = service_status or _service_status
    detected_agents = []
    for agent_id, definition in (registry or AGENT_ADAPTER_REGISTRY).items():
        selected_command = ""
        version = ""
        for command in definition["commands"]:
            detected, candidate_version = command_status(command)
            if detected:
                selected_command = command
                version = candidate_version
                break
        application_detected = any(path_exists(path) for path in definition["applications"])
        config_detected = any(path_exists(path) for path in definition.get("config_paths", []))
        service_detected = any(service_status(url) for url in definition.get("service_urls", []))
        detected = bool(selected_command or application_detected or service_detected)
        if not detected:
            continue
        configured = bool(selected_command or config_detected or service_detected)
        probe = definition["authorization_probe"]
        authorized: bool | None = None
        if configured and probe:
            authorized = authorization_probe(selected_command, probe)
        healthy: bool | None = bool(version) if selected_command else (True if service_detected else None)
        auth_satisfied = authorized is True if definition["authorization_required"] else True
        available = bool(
            definition["adapter_readiness"] == "LIVE" and configured and healthy and auth_satisfied
        )
        if available:
            state = "Available"
        elif configured and authorized is False:
            state = "AuthRequired"
        else:
            state = "Detected"
        detected_agents.append({
            "agent_id": agent_id,
            "name": definition["name"],
            "detected": True,
            "configured": configured,
            "authorized": authorized,
            "healthy": healthy,
            "available": available,
            "state": state,
            "version": version,
            "execution_ready": False,
            "execution_limitation": "计费、当前工作授权和有效访问仍需核验。" if selected_command else "未验证可用于工作的机器接口。",
            "programmatic_import_supported": bool(
                (selected_command or service_detected) and definition["programmatic_import_supported"]
            ),
            "current_limitation": "" if (selected_command or service_detected) else "DETECTED_BUT_PROGRAMMATIC_IMPORT_UNSUPPORTED",
        })
    return detected_agents


LOCAL_APPLICATION_ROOT = Path("/Applications")


def _application_identity(application: Path) -> list[Any]:
    """Read bounded public bundle identity only; never run the declared executable."""
    root = application.resolve(strict=True)
    metadata_path = root / "Contents/Info.plist"
    if metadata_path.is_symlink() or metadata_path.resolve(strict=True) != metadata_path:
        raise ValueError("应用元数据路径无效。")
    metadata_info = metadata_path.stat()
    if not stat.S_ISREG(metadata_info.st_mode) or metadata_info.st_size > 262144:
        raise ValueError("应用元数据文件无效。")
    with metadata_path.open("rb") as stream:
        raw = stream.read(262145)
    if len(raw) > 262144:
        raise ValueError("应用元数据过大。")
    try:
        metadata = plistlib.loads(raw)
    except (ValueError, plistlib.InvalidFileException, TypeError, ExpatError, OverflowError) as error:
        raise ValueError("应用元数据无效。") from error
    if not isinstance(metadata, dict):
        raise ValueError("应用元数据无效。")
    bundle_id = metadata.get("CFBundleIdentifier")
    executable = metadata.get("CFBundleExecutable")
    if (metadata.get("CFBundlePackageType") != "APPL"
            or not isinstance(bundle_id, str) or not bundle_id.strip() or len(bundle_id) > 255
            or not isinstance(executable, str) or not executable or executable in {".", ".."}
            or "/" in executable or "\\" in executable):
        raise ValueError("缺少有效应用身份。")
    binary = root / "Contents/MacOS" / executable
    if binary.is_symlink() or binary.resolve(strict=True) != binary:
        raise ValueError("应用可执行文件路径无效。")
    info = binary.stat()
    if not stat.S_ISREG(info.st_mode) or not info.st_mode & 0o111:
        raise ValueError("应用可执行文件无效。")
    return [bundle_id, executable, hashlib.sha256(raw).hexdigest(),
            info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns]


def discover_local_agents(installation_path: str = "") -> list[dict[str, Any]]:
    """Inspect public installation identity; never launch or inspect auth."""
    agents = []
    definitions = dict(AGENT_ADAPTER_REGISTRY)
    if not isinstance(installation_path, str):
        raise ValueError("应用路径必须为字符串。")
    if installation_path:
        candidate = Path(installation_path)
        root = LOCAL_APPLICATION_ROOT.resolve()
        if candidate.parent != LOCAL_APPLICATION_ROOT or candidate.suffix != ".app":
            raise ValueError("请选择 /Applications 下的应用包路径。")
        try:
            resolved = candidate.resolve(strict=True)
            if resolved.parent != root or not resolved.is_dir():
                raise ValueError("应用路径不可用或超出公共安装目录。")
        except OSError as error:
            raise ValueError("应用路径不可用。") from error
        definitions = {"selected_app": {"name": candidate.stem, "commands": [],
                       "applications": [str(candidate)], "adapter_readiness": "UNVERIFIED"}}
    for agent_id, definition in definitions.items():
        executable = next((value for name in definition["commands"] if (value := shutil.which(name))), None)
        if not executable and agent_id == "codex":
            candidate = Path.home() / ".codex/packages/standalone/releases/0.144.6-aarch64-apple-darwin/bin/codex"
            if candidate.is_file():
                executable = str(candidate)
        application = next((path for path in definition["applications"] if Path(path).is_dir()), None)
        selected = executable or application
        if not selected:
            continue
        try:
            path = Path(selected).resolve(strict=True)
            info = path.stat()
            if executable and (not stat.S_ISREG(info.st_mode) or not info.st_mode & 0o111):
                continue
            application_identity = _application_identity(path) if not executable else None
            identity = [str(path), info.st_dev, info.st_ino, info.st_uid, info.st_mode,
                        info.st_size, info.st_mtime_ns, info.st_ctime_ns, application_identity]
        except (OSError, ValueError):
            if installation_path:
                raise ValueError("所选路径不是有效应用包，请核对安装。")
            continue
        acp = None
        if agent_id in ACP_INSTALLATIONS and str(path) == ACP_INSTALLATIONS[agent_id]["application"]:
            try:
                acp = acp_installation(agent_id)
                identity.append(acp["installation_ref"])
            except (OSError, ValueError):
                pass
        reference = hashlib.sha256(json.dumps([agent_id, identity], separators=(",", ":")).encode()).hexdigest()
        bindable = bool(acp or (executable and agent_id == "codex" and definition["adapter_readiness"] == "LIVE"))
        agents.append({"agent_id": agent_id, "name": definition["name"],
                       "discovery_ref": reference, "capability_id": f"agent.local.{agent_id}.{reference[:16]}",
                       **({"agent_kind": "acp-stdio", "installation_ref": acp["installation_ref"]} if acp else {}),
                       "installation_path": str(path), "manual_selection": bool(installation_path), "bindable": bindable,
                       "state": "Detected", "authorized": None, "healthy": None,
                       "available": False, "execution_ready": False,
                       "limitation": "仅发现安装；绑定后仍需独立核验连接、授权、费用和当前工作权限。" if bindable
                       else "已发现安装，当前机器接口尚未验证；可登记，暂不能绑定执行。"})
    return agents


# First inspected install-backed ACP provider. Other providers share the protocol
# bridge only after their own official entry/identity contract is approved.
ACP_INSTALLATIONS = {
    "deepseek_harness": {
        "application": "/Applications/DeepSeek Harness.app",
        "bundle_id": "com.deepseek.dsh", "version": "0.2.1-rc.5",
        "launcher": "Contents/Resources/runtime/cli/bin/dsh",
        "files": {
            "Contents/Resources/runtime/cli/bin/dsh": "61647349bd61a5cfff40c338c7d5af767a22f409ddce36feabfb2f693d1e66af",
            "Contents/Resources/app.asar": "8dad52f295bdbe9fa71948fdf38ac2ce3c910213d3b89c37174b2af77db9fb31",
            "Contents/MacOS/DeepSeek Harness": "b7ca6fc3356ebdb4daa79827e6433c4c1a9cdd2196014a693ee873bae54d9949",
        },
        "args": ["--profile", "acp"],
        "profile_directory": ".dsh/profiles/acp", "profile_environment": {"DSH_HOME": ".dsh"},
    }
}


def acp_installation(agent_id: str) -> dict[str, Any]:
    definition = ACP_INSTALLATIONS.get(agent_id)
    if definition is None:
        raise ValueError("该 ACP 安装入口尚未核验。")
    root = Path(definition["application"])
    if root.is_symlink() or root.resolve(strict=True) != root:
        raise ValueError("ACP 安装路径无效。")
    identity = _application_identity(root)
    if identity[0] != definition["bundle_id"]:
        raise ValueError("ACP 应用身份不匹配。")
    with (root / "Contents/Info.plist").open("rb") as stream:
        raw = stream.read(262145)
    if len(raw) > 262144:
        raise ValueError("ACP 应用元数据超出限制。")
    metadata = plistlib.loads(raw)
    if metadata.get("CFBundleShortVersionString") != definition["version"]:
        raise ValueError("ACP 应用版本未核验。")
    files = []
    for relative, expected in definition["files"].items():
        path = root / relative
        if path.resolve(strict=True) != path or not path.is_file():
            raise ValueError("ACP 安装文件无效。")
        info = path.stat()
        if relative == definition["launcher"] and not info.st_mode & 0o111:
            raise ValueError("ACP 启动入口不可执行。")
        if info.st_size > 512 * 1024 * 1024:
            raise ValueError("ACP 安装文件超出限制。")
        digest = hashlib.sha256()
        consumed = 0
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                consumed += len(chunk)
                if consumed > 512 * 1024 * 1024:
                    raise ValueError("ACP 安装文件超出限制。")
                digest.update(chunk)
        if path.stat() != info or digest.hexdigest() != expected:
            raise ValueError("ACP 安装文件已变化。")
        files.append([relative, expected, info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns])
    reference = hashlib.sha256(json.dumps([agent_id, identity, files], separators=(",", ":")).encode()).hexdigest()
    return {"agent_id": agent_id, "installation_ref": reference, "version": definition["version"],
            "command": [str(root / definition["launcher"]), *definition["args"]],
            "profile_directory": definition["profile_directory"], "profile_environment": definition["profile_environment"]}


def local_agent_registration(metadata: dict[str, Any], capability_id: str) -> tuple[dict[str, Any], str]:
    shared_account = metadata.get("dsh_shared_account", False)
    if type(shared_account) is not bool:
        raise ValueError("共享 DSH 账号与配置必须明确选择。")
    reference = metadata.get("local_agent_ref")
    if not isinstance(reference, str) or len(reference) != 64:
        raise ValueError("本机 Agent 来源无效，请重新发现。")
    selected = next((item for item in discover_local_agents(metadata.get("local_installation_path", "")) if item["discovery_ref"] == reference), None)
    if not selected or selected["capability_id"] != capability_id:
        raise ValueError("本机 Agent 安装已变化或不可用，请重新发现。")
    if shared_account and (selected["agent_id"] != "deepseek_harness" or selected.get("agent_kind") != "acp-stdio"):
        raise ValueError("共享 DSH 账号仅适用于已核验的 DeepSeek Harness 安装。")
    return {"kind": selected.get("agent_kind", "codex-cli") if selected["bindable"] else "local-unverified",
            **({"installation_ref": selected["installation_ref"]} if selected.get("agent_kind") == "acp-stdio" else {}),
            "local_agent_ref": reference, "agent_id": selected["agent_id"],
            **({"dsh_shared_account": shared_account} if selected["agent_id"] == "deepseek_harness" else {}),
            "installation_path": selected["installation_path"], "discovery_state": "Detected",
            "execution_ready": False, "limitation": selected["limitation"],
            **({"computer_access_intent": "ASK_WHEN_NEEDED"} if selected["bindable"] and selected.get("agent_kind") != "acp-stdio" else {})}, (
                "active" if selected["bindable"] else "inactive")


def scan_local_capabilities() -> dict[str, Any]:
    agents = scan_local_agents()

    local_models = []
    for provider_id, command, app_path in (
        ("ollama", "ollama", "/Applications/Ollama.app"),
        ("lm_studio", "lms", "/Applications/LM Studio.app"),
    ):
        detected, version = _command_status(command)
        detected = detected or Path(app_path).exists()
        healthy = False
        model_count = 0
        if detected:
            definition = PROVIDERS[provider_id]
            try:
                payload = AICapabilityRegistry._http_get(
                    definition["base_url"] + definition["discovery_path"], {}, 3
                )
                model_count = len(_model_rows(payload, provider_id))
                healthy = True
            except ValueError:
                pass
        local_models.append({
            "provider_id": provider_id,
            "detected": detected,
            "configured": detected,
            "authorized": True if detected else False,
            "healthy": healthy,
            "available": bool(healthy and model_count),
            "state": "Available" if healthy and model_count else ("Detected" if detected else "Unavailable"),
            "version": version,
            "model_count": model_count,
        })
    return {"agents": agents, "local_model_providers": local_models}


def build_ai_capability_router(database, credential_vault) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/ai-capabilities")
    service = AICapabilityRegistry(database, credential_vault)

    @router.get("/providers")
    def list_providers():
        return {"providers": service.providers()}

    @router.post("/providers/{provider_id}/connect")
    def connect_provider(provider_id: str, payload: ProviderConnectIn):
        try:
            return service.connect(provider_id, payload)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/providers/{provider_id}/recover")
    def recover_provider(provider_id: str):
        try:
            return service.recover(provider_id)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/local")
    def local_capabilities(metadata_only: bool = False, installation_path: str = ""):
        if metadata_only:
            try:
                return {"agents": discover_local_agents(installation_path), "local_model_providers": []}
            except ValueError as error:
                raise HTTPException(status_code=422, detail=str(error)) from error
        return scan_local_capabilities()

    @router.get("/bootstrap")
    def bootstrap_capabilities():
        local = scan_local_capabilities()
        available = any(item["available"] for item in (*local["agents"], *local["local_model_providers"]))
        return {
            **local,
            "has_available_ai": available,
            "recommended_providers": [] if available else ["openai", "anthropic", "gemini", "deepseek"],
        }

    return router
