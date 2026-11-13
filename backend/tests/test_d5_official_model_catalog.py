"""ADR-0028 Phase-2 (issue 065): 官方模型目录管理验收测试 + 禁止区守卫。

覆盖：
  * 官方模型 create 时 gateway_ref 不存在 -> 422（fail-closed，无悬空引用）；
  * 模型状态机 active<->inactive（无删除）；
  * catalog 读不含 credential_ref（官方模型表本就零凭证列）；
  * capability.model_created / capability.model_status_changed 审计写入；
  * 受控 evolution_events 写仅批准集合；
  * 禁止区关键词零命中；
  * 既有 S1–S4 测试不受影响（本文件不修改任何既有测试）。
"""
import os
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conftest import (  # noqa: E402
    _APPROVED_EVENT_TYPES,
    _APP_DIR,
    assert_forbidden_clean,
)

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from app.model_catalog import GatewayCatalog, ModelCatalog  # noqa: E402
from app.capability_catalog import CapabilityCatalog  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class OfficialModelCatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)
        self.gateway_catalog = GatewayCatalog(self.db, self.event_log)
        self.model_catalog = ModelCatalog(self.db, self.event_log)

    def tearDown(self):
        self.tmp.cleanup()

    def _client(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        return TestClient(create_app(self.db.path))

    # ── AC1: 状态机 active<->inactive ──
    def test_model_state_machine(self):
        row = self.model_catalog.create(
            "m1", "prov", "Model One", ["gpt-4o"], auth_type="apikey", gateway_ref="newapi"
        )
        self.assertEqual(row["status"], "active")
        row = self.model_catalog.set_status("m1", "inactive")
        self.assertEqual(row["status"], "inactive")
        row = self.model_catalog.set_status("m1", "active")
        self.assertEqual(row["status"], "active")

    # ── AC2: gateway_ref 不存在 -> KeyError -> 422（fail-closed）──
    def test_model_create_missing_gateway_ref_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.model_catalog.create(
                "m2", "prov", "M2", ["x"], gateway_ref="does_not_exist"
            )

    def test_model_create_missing_gateway_ref_via_api_422(self):
        client = self._client()
        resp = client.post(
            "/api/platform/models",
            json={
                "model_key": "m2",
                "provider_id": "p",
                "display_name": "M2",
                "gateway_ref": "nope",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── AC2(续): 非法 auth_type -> ValueError -> 422 ──
    def test_model_create_invalid_auth_type_raises_valueerror(self):
        with self.assertRaises(ValueError):
            self.model_catalog.create(
                "mx", "p", "MX", [], auth_type="basic", gateway_ref="newapi"
            )

    # ── AC3: 服务层 create 全链路 + capability 审计 ──
    def test_model_create_full_cycle_and_audit(self):
        self.model_catalog.create(
            "m3", "prov", "Model Three", ["gpt-4o", "gpt-4o-mini"],
            auth_type="oauth", gateway_ref="newapi", default_model="gpt-4o",
        )
        self.model_catalog.set_status("m3", "inactive")
        self.model_catalog.set_status("m3", "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertIn("capability.model_created", types)
        self.assertIn("capability.model_status_changed", types)

    # ── AC4: 受控写仅批准集合 ──
    def test_controlled_write_only_approved(self):
        self.model_catalog.create("m4", "prov", "Model Four", ["x"], gateway_ref="newapi")
        self.model_catalog.set_status("m4", "inactive")
        self.model_catalog.set_status("m4", "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertTrue(
            types.issubset(_APPROVED_EVENT_TYPES),
            f"受控写越权：{types - _APPROVED_EVENT_TYPES}",
        )
        self.assertIn("capability.model_created", types)
        self.assertIn("capability.model_status_changed", types)

    # ── AC5: catalog 读（官方模型）不含 credential_ref ──
    def test_catalog_models_read_excludes_credential_ref(self):
        client = self._client()
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        for model in resp.json()["models"]:
            self.assertNotIn("credential_ref", model)
            self.assertNotIn("api_key", model)
            self.assertNotIn("token", model)

    # ── AC5(续): API 层官方模型 create / 启用停用 ──
    def test_model_create_via_api(self):
        client = self._client()
        payload = {
            "model_key": "m_api",
            "provider_id": "prov",
            "display_name": "API Model",
            "supported_models": ["gpt-4o"],
            "auth_type": "apikey",
            "gateway_ref": "newapi",
        }
        resp = client.post("/api/platform/models", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["model_key"], "m_api")

        listed = client.get(
            "/api/platform/models?include_inactive=true", headers=ADMIN
        ).json()["models"]
        self.assertTrue(any(m["model_key"] == "m_api" for m in listed))

        resp = client.put(
            "/api/platform/models/m_api", json={"action": "disable"}, headers=ADMIN
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "inactive")
        resp = client.put(
            "/api/platform/models/m_api", json={"action": "enable"}, headers=ADMIN
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "active")

    # ── AC6: 禁止区守卫 ──
    def test_forbidden_scope_zero_hits(self):
        violations = assert_forbidden_clean()
        self.assertEqual(violations, [], f"禁止区命中: {violations}")

    def test_admin_does_not_import_model_gateway(self):
        # 约束 6/7：Admin 绝不 import / 调用 model_gateway 执行层模块。
        # 仅匹配真正的模块 import / 符号引用，避免误伤 get_model_gateway 等自有标识符。
        pattern = re.compile(
            r"from \.model_gateway import|import \.model_gateway|import model_gateway|ModelGatewayAdapter"
        )
        hits = []
        for path in (_APP_DIR / "model_catalog.py", _APP_DIR / "database.py"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if pattern.search(line):
                    hits.append(f"{path.name}:{i}: {line.strip()}")
        self.assertEqual(
            hits, [], f"Admin 不应 import / 调用 model_gateway 模块: {hits}"
        )

    # ── AC7: 既有 S1–S4 测试不受影响（本文件不修改任何既有测试）──
    def test_seed_official_model_present(self):
        # 既有 _seed_official_model_catalog 仍生效（issue 066）。
        self.assertIsNotNone(self.db.get_official_model("official.newapi.default"))

    # ── AC8 (issue 070/071 向后兼容): /api/catalog/models 仍仅返回 type='model' ──
    def test_catalog_models_only_returns_model_type(self):
        # 本期新增 tool/connector 能力不应泄漏进官方模型 catalog。
        capability_catalog = CapabilityCatalog(self.db, self.event_log)
        capability_catalog.create(
            "tool.search", "tool", provider_id="internal", display_name="Search"
        )
        capability_catalog.create(
            "conn.slack", "connector", provider_id="slack", display_name="Slack"
        )
        client = self._client()
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        models = resp.json()["models"]
        # 种子官方模型（type='model'）仍在；tool/connector 不在。
        self.assertTrue(any(m["model_key"] == "official.newapi.default" for m in models))
        self.assertTrue(all(m["type"] == "model" for m in models))
        self.assertFalse(any(m["model_key"] == "tool.search" for m in models))
        self.assertFalse(any(m["model_key"] == "conn.slack" for m in models))


if __name__ == "__main__":
    unittest.main()
