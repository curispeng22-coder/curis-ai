from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


ROOT = Path(__file__).resolve().parents[2]
TENANT = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TYPES = (
    "model", "agent", "skill", "tool", "workflow", "connector",
    "cli", "api", "webhook", "mcp",
)


class MVPPhase4S6CapabilityRegistryTests(unittest.TestCase):
    def setUp(self):
        identity_env = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        identity_env.start()
        self.addCleanup(identity_env.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)

    def test_workspace_registry_manages_all_six_types_without_admin(self):
        for capability_type in TYPES:
            response = self.client.post(
                "/api/workspace/capabilities/registry",
                headers=TENANT,
                json={
                    "capability_key": f"mvp.{capability_type}",
                    "type": capability_type,
                    "name": f"MVP {capability_type}",
                    "provider_id": "curis",
                    "model_name": "mvp-model" if capability_type == "model" else "",
                    "description": f"{capability_type} description",
                    "version": "1.2.3",
                },
            )
            self.assertEqual(response.status_code, 201, response.text)
            self.assertEqual(response.json()["type"], capability_type)

        listed = self.client.get(
            "/api/workspace/capabilities/registry", headers=TENANT
        )
        self.assertEqual(listed.status_code, 200, listed.text)
        self.assertEqual(listed.json()["types"], list(TYPES))
        self.assertTrue(
            all(
                not {"runtime_meta", "runtime_meta_json", "credentials_ref", "api_key", "token"}
                & set(item)
                for item in listed.json()["capabilities"]
            )
        )
        keys = {
            item["capability_key"]: item
            for item in listed.json()["capabilities"]
        }
        self.assertTrue({f"mvp.{item}" for item in TYPES}.issubset(keys))
        self.assertEqual(keys["mvp.model"]["gateway_ref"], "newapi")
        self.assertEqual(keys["mvp.agent"]["version"], "1.2.3")

        disabled = self.client.put(
            "/api/workspace/capabilities/registry/mvp.tool",
            headers=TENANT,
            json={"action": "disable"},
        )
        self.assertEqual(disabled.status_code, 200, disabled.text)
        self.assertEqual(disabled.json()["status"], "inactive")
        enabled = self.client.put(
            "/api/workspace/capabilities/registry/mvp.tool",
            headers=TENANT,
            json={"action": "enable"},
        )
        self.assertEqual(enabled.status_code, 200, enabled.text)
        self.assertEqual(enabled.json()["status"], "active")

        detail = self.client.get(
            "/api/workspace/capabilities/registry/mvp.tool", headers=TENANT
        )
        self.assertEqual(detail.status_code, 200, detail.text)
        self.assertEqual(detail.json()["description"], "tool description")

    def test_historical_skill_migration_is_idempotent_and_license_gated(self):
        first = self.client.post(
            "/api/workspace/capabilities/registry/migrate-skills", headers=TENANT
        )
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(first.json()["migrated_count"], 5)
        self.assertEqual(first.json()["skipped_count"], 0)

        second = self.client.post(
            "/api/workspace/capabilities/registry/migrate-skills", headers=TENANT
        )
        self.assertEqual(second.status_code, 200, second.text)
        self.assertEqual(second.json()["migrated_count"], 0)
        self.assertEqual(second.json()["skipped_count"], 5)

        listed = self.client.get(
            "/api/workspace/capabilities/registry?type=skill&include_inactive=true",
            headers=TENANT,
        ).json()["capabilities"]
        migrated = [item for item in listed if item["capability_key"].startswith("skl_skill_")]
        self.assertEqual(len(migrated), 5)
        for item in migrated:
            self.assertEqual(item["status"], "inactive")
            self.assertEqual(item["provider_id"], "legacy_skill")
            self.assertEqual(item["migration_status"], "draft_candidate")
            self.assertEqual(item["license"], "NOASSERTION")
            self.assertFalse(item["commercial_use"])
            self.assertEqual(item["source_template_id"], item["capability_key"])

        blocked = self.client.put(
            f"/api/workspace/capabilities/registry/{migrated[0]['capability_key']}",
            headers=TENANT,
            json={"action": "enable"},
        )
        self.assertEqual(blocked.status_code, 422, blocked.text)
        self.assertIn("license review", blocked.json()["detail"])

    def test_registry_rejects_invalid_types_and_secret_like_metadata(self):
        invalid = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT,
            json={"capability_key": "mvp.binary", "type": "binary", "name": "Binary"},
        )
        self.assertEqual(invalid.status_code, 422, invalid.text)

        secret = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT,
            json={
                "capability_key": "mvp.secret",
                "type": "tool",
                "name": "Secret",
                "description": "api_key=do-not-store",
            },
        )
        self.assertEqual(secret.status_code, 422, secret.text)
        missing = self.client.get(
            "/api/workspace/capabilities/registry/mvp.secret", headers=TENANT
        )
        self.assertEqual(missing.status_code, 404, missing.text)

    def test_frontend_uses_real_registry(self):
        paths = [
            ROOT / "frontend/lib/capabilities.js",
            ROOT / "frontend/app/ceo-office/capabilities/page.js",
            ROOT / "frontend/app/ceo-office/capabilities/CapabilityFormDrawer.js",
            ROOT / "frontend/app/ceo-office/capabilities/[type]/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("SAMPLE_", source)
        self.assertNotIn("TerraSampleBadge", source)
        for api_name in (
            "getCapabilities",
            "getCapability",
            "createCapability",
            "updateCapabilityStatus",
            "migrateHistoricalSkills",
        ):
            self.assertIn(api_name, source)

    def test_step1_endpoint_and_credential_ref_become_callable_adapter(self):
        """Step1 验收：前端填 endpoint + credential_ref 后，注册的能力在 runtime_meta
        中存为可消费的 adapter_config / credentials_ref，且工厂能构建真实适配器。

        注：目录 type 用内核的 api（非 http）；适配器 kind 用 http。
        """
        from app.capability_adapters import (
            CapabilityAdapterFactory,
            HttpApiAdapter,
            McpAdapter,
        )

        # api 能力：endpoint 应归位成 adapter_config.url，工厂构建 HttpApiAdapter。
        resp = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT,
            json={
                "capability_key": "ext.my-api",
                "type": "api",
                "name": "My External API",
                "endpoint": "https://api.example.com/run",
                "credential_ref": "env:MY_API_KEY",
            },
        )
        self.assertEqual(resp.status_code, 201, resp.text)
        body = resp.json()
        self.assertEqual(body["endpoint"], "https://api.example.com/run")
        self.assertEqual(body["credential_ref"], "env:MY_API_KEY")
        self.assertEqual(body["adapter_kind"], "http")
        self.assertEqual(body["adapter_config"], {"url": "https://api.example.com/run"})

        detail = self.client.get(
            "/api/workspace/capabilities/registry/ext.my-api", headers=TENANT
        ).json()
        self.assertIsInstance(CapabilityAdapterFactory.build(detail), HttpApiAdapter)

        # mcp 能力：endpoint 应归位成 adapter_config.server_command。
        mcp = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT,
            json={
                "capability_key": "ext.my-mcp",
                "type": "mcp",
                "name": "My MCP",
                "endpoint": "npx -y @my/mcp-server",
                "credential_ref": "env:MCP_TOKEN",
            },
        )
        self.assertEqual(mcp.status_code, 201, mcp.text)
        self.assertEqual(
            mcp.json()["adapter_config"], {"server_command": "npx -y @my/mcp-server"}
        )
        self.assertEqual(mcp.json()["adapter_kind"], "mcp")
        mcp_detail = self.client.get(
            "/api/workspace/capabilities/registry/ext.my-mcp", headers=TENANT
        ).json()
        self.assertIsInstance(CapabilityAdapterFactory.build(mcp_detail), McpAdapter)


if __name__ == "__main__":
    unittest.main()
