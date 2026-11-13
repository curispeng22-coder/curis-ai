"""ADR-0028 Phase-2 (issue 065): New API 网关管理验收测试 + 禁止区守卫。

覆盖：
  * model_gateways 表 additive 存在（且零密钥值列）；
  * 网关 create / enable / disable 全链路（服务层 + API）；
  * capability.gateway_created / capability.gateway_status_changed 审计写入；
  * 受控 evolution_events 写仅批准集合（capability.* + S4 governance.*）；
  * 禁止区关键词零命中（不 import model_gateway、无出站库、无 /api/govern 等）；
  * /api/catalog/gateways 只读且不含 credential_ref。
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
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class NewApiGatewayTest(unittest.TestCase):
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

    # ── AC1: model_gateways 表 additive 存在 + 零密钥值列 ──
    def test_model_gateways_table_exists_and_no_secret_columns(self):
        with self.db.connect() as connection:
            columns = {
                row["name"]
                for row in connection.execute("pragma table_info(model_gateways)")
            }
        for expected in ("gateway_id", "name", "type", "base_url", "status"):
            self.assertIn(expected, columns)
        # 铁律：绝不出现任何密钥值列。
        for forbidden in ("api_key", "token", "secret", "password", "credential"):
            self.assertNotIn(forbidden, columns)

    def test_default_gateway_seeded(self):
        gateways = self.gateway_catalog.list()
        self.assertTrue(any(g["gateway_id"] == "newapi" for g in gateways))

    # ── AC2: 服务层 create / enable / disable 全链路 ──
    def test_gateway_create_full_cycle(self):
        row = self.gateway_catalog.create(
            "gw_prod", "Prod Gateway", "newapi", "https://gw.example.com"
        )
        self.assertEqual(row["gateway_id"], "gw_prod")
        self.assertEqual(row["status"], "active")
        self.assertIsNone(row["credential_ref"])

        row = self.gateway_catalog.set_status("gw_prod", "inactive")
        self.assertEqual(row["status"], "inactive")
        row = self.gateway_catalog.set_status("gw_prod", "active")
        self.assertEqual(row["status"], "active")

    # ── AC2(续): API 层 create / enable / disable ──
    def test_gateway_create_via_api(self):
        client = self._client()
        payload = {
            "gateway_id": "gw_api",
            "name": "API Gateway",
            "type": "newapi",
            "base_url": "https://api.example.com",
        }
        resp = client.post("/api/platform/gateways", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["gateway_id"], "gw_api")

        listed = client.get("/api/platform/gateways", headers=ADMIN).json()["gateways"]
        self.assertTrue(any(g["gateway_id"] == "gw_api" for g in listed))

        resp = client.put(
            "/api/platform/gateways/gw_api",
            json={"action": "disable"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "inactive")

        resp = client.put(
            "/api/platform/gateways/gw_api",
            json={"action": "enable"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "active")

    # ── AC3: capability.* 审计写入 ──
    def test_capability_audit_written(self):
        self.gateway_catalog.create("gw_audit", "Audit GW", "newapi", "https://x")
        self.gateway_catalog.set_status("gw_audit", "inactive")
        self.gateway_catalog.set_status("gw_audit", "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertIn("capability.gateway_created", types)
        self.assertIn("capability.gateway_status_changed", types)

    # ── AC4: 受控写仅批准集合 ──
    def test_controlled_write_only_approved(self):
        self.gateway_catalog.create("gw_ctrl", "Ctrl GW", "newapi", "https://x")
        self.gateway_catalog.set_status("gw_ctrl", "inactive")
        self.gateway_catalog.set_status("gw_ctrl", "active")
        types = {e["event_type"] for e in self.event_log.get_all()}
        self.assertTrue(
            types.issubset(_APPROVED_EVENT_TYPES),
            f"受控写越权：{types - _APPROVED_EVENT_TYPES}",
        )
        self.assertIn("capability.gateway_created", types)
        self.assertIn("capability.gateway_status_changed", types)

    # ── AC5: 鉴权 fail-closed ──
    def test_unauthorized_returns_401(self):
        client = self._client()
        self.assertEqual(
            client.post(
                "/api/platform/gateways",
                json={"gateway_id": "x", "name": "n", "base_url": "https://x"},
            ).status_code,
            401,
        )
        self.assertEqual(client.get("/api/platform/gateways").status_code, 401)

    # ── AC6: 非法枚举 -> 422 ──
    def test_invalid_type_returns_422(self):
        client = self._client()
        # Step 5：openai 已是合法类型；此处用真正不在 GATEWAY_TYPE 内的枚举验证 AC6。
        resp = client.post(
            "/api/platform/gateways",
            json={"gateway_id": "x", "name": "n", "type": "anthropic", "base_url": "https://x"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    def test_invalid_action_returns_422(self):
        client = self._client()
        resp = client.put(
            "/api/platform/gateways/newapi",
            json={"action": "explode"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    def test_duplicate_gateway_returns_422(self):
        client = self._client()
        payload = {
            "gateway_id": "dup",
            "name": "Dup",
            "type": "newapi",
            "base_url": "https://x",
        }
        self.assertEqual(
            client.post("/api/platform/gateways", json=payload, headers=ADMIN).status_code,
            201,
        )
        self.assertEqual(
            client.post("/api/platform/gateways", json=payload, headers=ADMIN).status_code,
            422,
        )

    # ── AC7: /api/catalog/gateways 只读 + 不含 credential_ref ──
    def test_catalog_gateway_read_only_excludes_credential(self):
        client = self._client()
        resp = client.get("/api/catalog/gateways")
        self.assertEqual(resp.status_code, 200)
        gateways = resp.json()["gateways"]
        self.assertTrue(len(gateways) >= 1)
        allowed = {"gateway_id", "name", "type", "base_url", "status"}
        for gateway in gateways:
            self.assertEqual(set(gateway.keys()), allowed)
            self.assertNotIn("credential_ref", gateway)
            self.assertNotIn("default_model", gateway)

    # ── AC8: 禁止区守卫（Admin 绝不 import model_gateway 等）──
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

    # ── AC9: 既有 catalog 读（官方模型）不被破坏 ──
    def test_existing_catalog_models_still_readable(self):
        client = self._client()
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("models", resp.json())

    # ── AC10: usage 查询 tenant_id 缺失 fail-closed（指标6，防跨租户聚合）──
    def test_usage_missing_tenant_id_fail_closed(self):
        client = self._client()
        resp = client.get("/api/platform/usage", headers=ADMIN)
        self.assertIn(resp.status_code, (400, 422))
        # 即便库中存在某租户用量事件，缺失 tenant_id 仍须被拒（绝不跨租户聚合）。
        self.event_log.record(
            correlation_id="u1", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 1, "unit": "call"},
            tenant_id="some-tenant",
        )
        resp = client.get("/api/platform/usage", headers=ADMIN)
        self.assertIn(resp.status_code, (400, 422))

    # ── AC10(续): 提供 tenant_id 时仅返回该租户（不跨租户泄漏）──
    def test_usage_with_tenant_id_scoped(self):
        self.event_log.record(
            correlation_id="u2", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 1, "unit": "call"},
            tenant_id="tenant-A",
        )
        self.event_log.record(
            correlation_id="u3", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 2, "unit": "call"},
            tenant_id="tenant-B",
        )
        client = self._client()
        resp = client.get("/api/platform/usage?tenant_id=tenant-A", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        tenant_ids = {e["tenant_id"] for e in resp.json()["usage_events"]}
        self.assertEqual(tenant_ids, {"tenant-A"})


if __name__ == "__main__":
    unittest.main()
