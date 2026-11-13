"""ADR-0028 Phase-2 (issue 065): QA 独立边界 / 异常路径验证（严过关补充）。

工程师既有 test_d5_* 覆盖了 happy path，但遗漏了若干硬指标边界：
  * (指标6) GET /api/platform/usage 在 tenant_id 缺失时必须 fail-closed（400/422），
    不得返回跨租户聚合；
  * (指标6) 提供 tenant_id 时仅返回该租户用量事件（不跨租户泄漏）；
  * (指标6) 用量投影不含 amount/currency/ROI；
  * (指标2/7) usage 与 models 端点无 admin token 时被拒（401）；
  * (指标边界) credential_ref 非法明文格式被拒（422）；
  * (指标边界) 网关非法 status 被拒（422）；
  * (指标边界) 重复 model_key 冲突被拒（422）。

本文件不修改任何既有测试（含 test_d4_platform.py）。
"""
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))  # tests/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # backend/

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from app.model_catalog import GatewayCatalog, ModelCatalog  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class QAUsageAndBoundaryTest(unittest.TestCase):
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

    # ── 指标6: usage 缺失 tenant_id → fail-closed（400/422 拒绝）──
    def test_usage_missing_tenant_id_is_rejected(self):
        client = self._client()
        resp = client.get("/api/platform/usage", headers=ADMIN)
        self.assertIn(
            resp.status_code,
            (400, 422),
            f"usage 查询 tenant_id 缺失必须 fail-closed(400/422)，实际 "
            f"{resp.status_code}: {resp.text}",
        )

    # ── 指标6: 提供 tenant_id 时仅返回该租户（不跨租户聚合）──
    def test_usage_with_tenant_id_scoped_to_that_tenant(self):
        self.event_log.record(
            correlation_id="c1", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 1, "unit": "call"},
            tenant_id="tenant-A",
        )
        self.event_log.record(
            correlation_id="c2", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 2, "unit": "call"},
            tenant_id="tenant-B",
        )
        client = self._client()
        resp = client.get("/api/platform/usage?tenant_id=tenant-A", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        tenant_ids = {e["tenant_id"] for e in events}
        self.assertEqual(
            tenant_ids, {"tenant-A"},
            f"usage 跨租户泄漏：{tenant_ids}",
        )

    # ── 指标6: 用量投影不含 amount/currency/ROI ──
    def test_usage_projection_no_amount_currency_roi(self):
        self.event_log.record(
            correlation_id="c3", event_type="usage.call",
            payload={"scope_type": "tenant", "quantity": 1, "unit": "call",
                     "capability_ref": "x", "raw_meter_value": 1},
            tenant_id="default",
        )
        client = self._client()
        resp = client.get("/api/platform/usage?tenant_id=default", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        for event in resp.json()["usage_events"]:
            self.assertNotIn("amount", event)
            self.assertNotIn("currency", event)
            self.assertNotIn("ROI", event)
            self.assertNotIn("roi", event)

    # ── 指标2/7: usage 端点无 admin token → 401 ──
    def test_usage_requires_admin(self):
        client = self._client()
        self.assertEqual(
            client.get("/api/platform/usage?tenant_id=default").status_code, 401
        )

    # ── 指标7: models 端点无 admin token → 401（GET 与 POST）──
    def test_models_requires_admin(self):
        client = self._client()
        self.assertEqual(client.get("/api/platform/models").status_code, 401)
        self.assertEqual(
            client.post(
                "/api/platform/models",
                json={"model_key": "x", "provider_id": "p", "display_name": "X"},
            ).status_code,
            401,
        )

    # ── 指标边界: credential_ref 明文非法格式 → 422 ──
    def test_gateway_create_invalid_credential_ref_returns_422(self):
        client = self._client()
        resp = client.post(
            "/api/platform/gateways",
            json={
                "gateway_id": "gw_bad", "name": "Bad", "type": "newapi",
                "base_url": "https://x", "credential_ref": "plaintext-secret-key",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── ADR-0029: metadata 不接受疑似密钥值 ──
    def test_gateway_metadata_rejects_secret_like_default_model(self):
        client = self._client()
        resp = client.post(
            "/api/platform/gateways",
            json={
                "gateway_id": "gw_secret_model",
                "name": "Secret Model",
                "type": "newapi",
                "base_url": "https://x",
                "default_model": "sk-or-v1-secret-value-1234567890",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)
        listed = client.get("/api/platform/gateways", headers=ADMIN).json()["gateways"]
        self.assertNotIn("sk-or-v1-secret-value-1234567890", str(listed))

    def test_official_model_metadata_rejects_secret_like_supported_model(self):
        client = self._client()
        resp = client.post(
            "/api/platform/models",
            json={
                "model_key": "secret_model",
                "provider_id": "newapi",
                "display_name": "Secret Model",
                "gateway_ref": "newapi",
                "supported_models": ["deepseek-v4-flash", "sk-or-v1-secret-value-1234567890"],
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)
        platform_models = client.get("/api/platform/models", headers=ADMIN).json()["models"]
        catalog_models = client.get("/api/catalog/models").json()["models"]
        self.assertNotIn("sk-or-v1-secret-value-1234567890", str(platform_models))
        self.assertNotIn("sk-or-v1-secret-value-1234567890", str(catalog_models))

    # ── 指标边界: 网关非法 status → 422 ──
    def test_gateway_create_invalid_status_returns_422(self):
        client = self._client()
        resp = client.post(
            "/api/platform/gateways",
            json={
                "gateway_id": "gw_st", "name": "St", "type": "newapi",
                "base_url": "https://x", "status": "pending",
            },
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── 指标边界: 重复 model_key 冲突 → 422（无 IntegrityError 透传）──
    def test_model_create_duplicate_key_returns_422(self):
        client = self._client()
        payload = {
            "model_key": "dup_m", "provider_id": "p",
            "display_name": "Dup", "gateway_ref": "newapi",
        }
        self.assertEqual(
            client.post("/api/platform/models", json=payload, headers=ADMIN).status_code,
            201,
        )
        resp = client.post("/api/platform/models", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
