"""ADR-0028 Phase-2 (issue 070/071): 统一官方能力目录（model/tool/connector）验收测试 + 禁止区守卫。

覆盖：
  * 统一能力 create：model 走 gateway_ref 校验（缺失 -> 422），tool/connector 不校验；
  * 状态机 active<->inactive（无物理删除）；
  * capability.created / capability.status_changed 审计写入；
  * 受控 evolution_events 写仅批准集合（capability.* + S4 governance.*）；
  * catalog 读（/api/catalog/capabilities）白名单列、不含 credential_ref/api_key/token；
  * 禁止区关键词零命中；
  * CapabilityCatalog 不 import model_gateway（约束 6/7）；
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

from app.capability_catalog import CapabilityCatalog  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class UnifiedCapabilityCatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)
        self.capability_catalog = CapabilityCatalog(self.db, self.event_log)

    def tearDown(self):
        self.tmp.cleanup()

    def _client(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        return TestClient(create_app(self.db.path))

    # ── AC1: model create 走 gateway_ref 校验（存在 -> 201）──
    def test_model_create_via_api_success(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "m_unified",
                "type": "model",
                "name": "Unified Model",
                "provider_id": "openai",
                "display_name": "Unified Model",
                "gateway_ref": "newapi",
                "auth_type": "apikey",
                "status": "active",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["capability_key"], "m_unified")
        self.assertEqual(resp.json()["type"], "model")

    # ── AC1(续): model create gateway_ref 不存在 -> KeyError -> 422（fail-closed）──
    def test_model_create_missing_gateway_ref_returns_422(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "m_nogw",
                "type": "model",
                "display_name": "No Gateway",
                "gateway_ref": "does_not_exist",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    def test_model_create_missing_gateway_ref_service_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.capability_catalog.create(
                "m_nogw_svc", "model", display_name="X", gateway_ref="does_not_exist"
            )

    # ── AC2: tool / connector create 不校验 gateway_ref（即便给不存在的 ref 也成功）──
    def test_tool_create_no_gateway_check(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "tool.web_search",
                "type": "tool",
                "name": "Web Search",
                "provider_id": "internal",
                "display_name": "Web Search",
                "gateway_ref": "does_not_exist",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["type"], "tool")
        # tool 不关联网关，gateway_ref 必须为空。
        self.assertEqual(resp.json()["gateway_ref"], "")

    def test_connector_create_no_gateway_check(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "conn.slack",
                "type": "connector",
                "provider_id": "slack",
                "display_name": "Slack",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["type"], "connector")

    # ── AC3: 状态机 active<->inactive（无物理删除）──
    def test_capability_state_machine(self):
        self.capability_catalog.create(
            "m_sm", "model", display_name="State Machine", gateway_ref="newapi"
        )
        self.assertEqual(
            self.capability_catalog.get("m_sm")["status"], "active"
        )
        self.assertEqual(
            self.capability_catalog.set_status("m_sm", "inactive")["status"], "inactive"
        )
        self.assertEqual(
            self.capability_catalog.set_status("m_sm", "active")["status"], "active"
        )

    def test_capability_disable_enable_via_api(self):
        client = self._client()
        client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "m_api_sm",
                "type": "model",
                "display_name": "API SM",
                "gateway_ref": "newapi",
            },
            headers=ADMIN,
        )
        resp = client.put(
            "/api/platform/capabilities/m_api_sm",
            json={"action": "disable"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "inactive")
        resp = client.put(
            "/api/platform/capabilities/m_api_sm",
            json={"action": "enable"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "active")

    # ── AC3(续): 非法 action -> 422 ──
    def test_capability_invalid_action_returns_422(self):
        client = self._client()
        client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "m_act",
                "type": "model",
                "display_name": "Act",
                "gateway_ref": "newapi",
            },
            headers=ADMIN,
        )
        resp = client.put(
            "/api/platform/capabilities/m_act",
            json={"action": "explode"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── AC4: 重复 capability_key -> ValueError -> 422 ──
    def test_capability_duplicate_key_returns_422(self):
        client = self._client()
        payload = {
            "capability_key": "m_dup",
            "type": "model",
            "display_name": "Dup",
            "gateway_ref": "newapi",
        }
        self.assertEqual(
            client.post("/api/platform/capabilities", json=payload, headers=ADMIN).status_code,
            201,
        )
        self.assertEqual(
            client.post("/api/platform/capabilities", json=payload, headers=ADMIN).status_code,
            422,
        )

    # ── AC5: 非法 type -> 422 ──
    def test_capability_invalid_type_returns_422(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={"capability_key": "x", "type": "binary", "display_name": "X"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── AC6: capability.* 审计写入 ──
    def test_capability_audit_written(self):
        self.capability_catalog.create(
            "m_audit", "model", display_name="Audit", gateway_ref="newapi"
        )
        self.capability_catalog.set_status("m_audit", "inactive")
        self.capability_catalog.set_status("m_audit", "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertIn("capability.created", types)
        self.assertIn("capability.status_changed", types)

    # ── AC7: 受控写仅批准集合 ──
    def test_controlled_write_only_approved(self):
        self.capability_catalog.create(
            "m_ctrl", "model", display_name="Ctrl", gateway_ref="newapi"
        )
        self.capability_catalog.create(
            "tool_ctrl", "tool", display_name="Ctrl Tool"
        )
        self.capability_catalog.create(
            "conn_ctrl", "connector", display_name="Ctrl Conn"
        )
        for key in ("m_ctrl", "tool_ctrl", "conn_ctrl"):
            self.capability_catalog.set_status(key, "inactive")
            self.capability_catalog.set_status(key, "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertTrue(
            types.issubset(_APPROVED_EVENT_TYPES),
            f"受控写越权：{types - _APPROVED_EVENT_TYPES}",
        )
        self.assertIn("capability.created", types)
        self.assertIn("capability.status_changed", types)

    # ── AC8: catalog 读（/api/catalog/capabilities）白名单列 + 不含密钥 ──
    def test_catalog_capabilities_read_excludes_secrets(self):
        client = self._client()
        # 创建三类能力
        client.post(
            "/api/platform/capabilities",
            json={"capability_key": "m_c", "type": "model", "display_name": "C-M", "gateway_ref": "newapi"},
            headers=ADMIN,
        )
        client.post(
            "/api/platform/capabilities",
            json={"capability_key": "tool_c", "type": "tool", "display_name": "C-T"},
            headers=ADMIN,
        )
        client.post(
            "/api/platform/capabilities",
            json={"capability_key": "conn_c", "type": "connector", "display_name": "C-C"},
            headers=ADMIN,
        )
        resp = client.get("/api/catalog/capabilities")
        self.assertEqual(resp.status_code, 200)
        caps = resp.json()["capabilities"]
        # 种子官方模型（type='model'）也会出现在 catalog 投影中，故仅校验三类能力
        # 均已被 Workspace 发现，而不强断言精确行数。
        created_keys = {c["capability_key"] for c in caps}
        self.assertIn("m_c", created_keys)
        self.assertIn("tool_c", created_keys)
        self.assertIn("conn_c", created_keys)
        allowed = {
            "capability_key", "type", "name", "provider_id", "display_name",
            "source", "gateway_ref", "auth_type", "status", "created_at",
            "updated_at",
            "effect_class",  # EvoFlow 复用 A1：副作用面元数据（派生，非密钥）
        }
        for cap in caps:
            self.assertEqual(set(cap.keys()), allowed)
            self.assertNotIn("credential_ref", cap)
            self.assertNotIn("api_key", cap)
            self.assertNotIn("token", cap)
        # 三类都在 catalog 投影中能被 Workspace 发现
        types = {c["type"] for c in caps}
        self.assertEqual(types, {"model", "tool", "connector"})

    # ── AC8(续): tool/connector 不应泄漏进官方模型 catalog（仅 type='model'）──
    def test_tool_not_in_model_catalog(self):
        client = self._client()
        client.post(
            "/api/platform/capabilities",
            json={"capability_key": "tool.only", "type": "tool", "display_name": "Only Tool"},
            headers=ADMIN,
        )
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        models = resp.json()["models"]
        self.assertTrue(all(m["type"] == "model" for m in models))
        self.assertFalse(any(m["model_key"] == "tool.only" for m in models))

    # ── AC9: 禁止区守卫 ──
    def test_forbidden_scope_zero_hits(self):
        violations = assert_forbidden_clean()
        self.assertEqual(violations, [], f"禁止区命中: {violations}")

    def test_capability_catalog_does_not_import_model_gateway(self):
        # 约束 6/7：Admin 绝不 import / 调用 model_gateway 执行层模块。
        pattern = re.compile(
            r"from \.model_gateway import|import \.model_gateway|import model_gateway|ModelGatewayAdapter"
        )
        hits = []
        for path in (
            _APP_DIR / "capability_catalog.py",
            _APP_DIR / "model_catalog.py",
            _APP_DIR / "database.py",
        ):
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

    # ── AC10: 既有 S1–S4 测试不受影响（本文件不修改任何既有测试）──
    def test_seed_official_model_present(self):
        # 既有 _seed_official_model_catalog 仍生效（issue 066），且其 type='model'。
        row = self.db.get_official_model("official.newapi.default")
        self.assertIsNotNone(row)
        self.assertEqual(row["type"], "model")


if __name__ == "__main__":
    unittest.main()
