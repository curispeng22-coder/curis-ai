"""Workspace 联调验证测试。

覆盖：
  ① catalog 端点 Workspace 可读（无需 admin token）；
  ② platform 端点 Admin-only（无 token → 401）；
  ③ usage_event 多维查询（capability_type / model_gateway_id / model_name / capability_source / status / since / until）；
  ④ usage_event tenant_id fail-closed（缺 tenant_id → 422）；
  ⑤ Admin 不读取 tenant_private（catalog 返回无 source='tenant_private'）；
  ⑥ Admin 不 import/修改 Workspace 私有能力（grep capability_catalog.py / main.py 无 tenant_private）；
  ⑦ /api/catalog/connectors 只返回 connector 类型，不泄漏 model/tool。
"""
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conftest import (  # noqa: E402
    _APPROVED_EVENT_TYPES,
    assert_forbidden_clean,
)

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


def _seed_usage_events(db: Database) -> None:
    """Seed 若干 usage.* 事件（含多维 payload 字段）用于多维查询测试。"""
    with db.connect() as conn:
        conn.executemany(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            [
                # tenant-a: model + official + success
                ("cu-1", "usage.model_call",
                 json.dumps({
                     "capability_type": "model",
                     "capability_source": "official",
                     "model_gateway_id": "newapi",
                     "model_name": "gpt-4",
                     "status": "success",
                 }), "tenant-a"),
                # tenant-a: model + official + failure
                ("cu-2", "usage.model_call",
                 json.dumps({
                     "capability_type": "model",
                     "capability_source": "official",
                     "model_gateway_id": "newapi",
                     "model_name": "claude",
                     "status": "failure",
                 }), "tenant-a"),
                # tenant-a: tool type
                ("cu-3", "usage.tool_call",
                 json.dumps({
                     "capability_type": "tool",
                     "capability_source": "official",
                     "status": "success",
                 }), "tenant-a"),
                # tenant-b: model + official + success
                ("cu-4", "usage.model_call",
                 json.dumps({
                     "capability_type": "model",
                     "capability_source": "official",
                     "model_gateway_id": "other-gw",
                     "model_name": "gpt-4",
                     "status": "success",
                 }), "tenant-b"),
            ],
        )
        conn.commit()


class WorkspaceIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def _client(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        return TestClient(create_app(self.db.path))

    # ── ① catalog 端点 Workspace 可读（无需 admin token）──
    def test_catalog_models_readable_without_token(self):
        client = self._client()
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("models", resp.json())

    def test_catalog_tools_readable_without_token(self):
        client = self._client()
        resp = client.get("/api/catalog/tools")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("tools", resp.json())

    def test_catalog_connectors_readable_without_token(self):
        client = self._client()
        resp = client.get("/api/catalog/connectors")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("connectors", resp.json())

    def test_catalog_capabilities_readable_without_token(self):
        client = self._client()
        resp = client.get("/api/catalog/capabilities")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("capabilities", resp.json())

    # ── ② platform 端点 Admin-only（无 token → 401）──
    def test_platform_tenants_requires_admin(self):
        client = self._client()
        resp = client.get("/api/platform/tenants")  # no auth
        self.assertEqual(resp.status_code, 401)

    def test_platform_gateways_post_requires_admin(self):
        client = self._client()
        resp = client.post(
            "/api/platform/gateways",
            json={
                "gateway_id": "gw-test",
                "name": "Test GW",
                "type": "newapi",
                "base_url": "http://localhost",
            },
        )  # no auth
        self.assertEqual(resp.status_code, 401)

    def test_platform_capabilities_post_requires_admin(self):
        client = self._client()
        resp = client.post(
            "/api/platform/capabilities",
            json={
                "capability_key": "cap-test",
                "type": "tool",
                "name": "Test Tool",
            },
        )  # no auth
        self.assertEqual(resp.status_code, 401)

    # ── ③ usage_event 多维查询 ──
    def test_usage_filter_by_capability_type(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&capability_type=tool",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e["payload"].get("capability_type"), "tool")

    def test_usage_filter_by_capability_source(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&capability_source=official",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e["payload"].get("capability_source"), "official")

    def test_usage_filter_by_model_gateway_id(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&model_gateway_id=newapi",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e["payload"].get("model_gateway_id"), "newapi")

    def test_usage_filter_by_model_name(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&model_name=gpt-4",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e["payload"].get("model_name"), "gpt-4")

    def test_usage_filter_by_status(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&status=failure",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e["payload"].get("status"), "failure")

    def test_usage_filter_by_since(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&since=2099-01-01T00:00:00",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        # Far-future since should return 0 events
        self.assertEqual(len(events), 0)

    def test_usage_filter_by_until(self):
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a&until=2000-01-01T00:00:00",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        # Far-past until should return 0 events
        self.assertEqual(len(events), 0)

    def test_usage_tenant_isolation(self):
        """tenant-a 的查询不应返回 tenant-b 的事件。"""
        _seed_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=tenant-a",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        for e in events:
            self.assertEqual(e["tenant_id"], "tenant-a")

    # ── ④ usage_event tenant_id fail-closed ──
    def test_usage_missing_tenant_id_returns_422(self):
        client = self._client()
        resp = client.get("/api/platform/usage", headers=ADMIN)  # no tenant_id
        self.assertEqual(resp.status_code, 422)

    # ── ⑤ Admin 不读取 tenant_private ──
    def test_catalog_capabilities_no_tenant_private_source(self):
        client = self._client()
        resp = client.get("/api/catalog/capabilities")
        self.assertEqual(resp.status_code, 200)
        capabilities = resp.json()["capabilities"]
        for cap in capabilities:
            self.assertNotEqual(
                cap.get("source"), "tenant_private",
                "catalog 能力不应包含 source='tenant_private'"
            )

    # ── ⑥ Admin 不 import/修改 Workspace 私有能力 ──
    def test_capability_catalog_no_tenant_private_reference(self):
        """capability_catalog.py 不含 tenant_private 引用（零）。"""
        cap_path = Path(__file__).resolve().parents[1] / "app" / "capability_catalog.py"
        text = cap_path.read_text(encoding="utf-8")
        self.assertNotIn(
            "tenant_private", text,
            "capability_catalog.py 不应引用 tenant_private"
        )

    def test_main_only_workspace_context_refers_to_tenant_private(self):
        """main.py 中 tenant_private 仅出现于 Workspace 私有能力端点，不出现于 Admin /api/platform/* 上下文。

        Phase-3 允许 Workspace 下新增 private model/tool/connector 与 selector
        路由，因此不能再用全文件固定计数；边界守卫应锁住 Admin platform
        路由段不得引用或修改 tenant_private。
        """
        main_path = Path(__file__).resolve().parents[1] / "app" / "main.py"
        text = main_path.read_text(encoding="utf-8")
        platform_section = text.split('@app.get("/api/platform/tenants")', 1)[1].split(
            '@app.get("/api/catalog/gateways")', 1
        )[0]
        self.assertNotIn(
            "tenant_private", platform_section,
            "Admin /api/platform/* 路由段不应引用 tenant_private"
        )

    # ── ⑦ /api/catalog/connectors 只返回 connector 类型 ──
    def test_connectors_endpoint_only_returns_connector_type(self):
        """验证 /api/catalog/connectors 只返回 type='connector' 的记录，不泄漏 model/tool。"""
        import json as _json
        # Seed a connector capability so there is at least one
        with self.db.connect() as conn:
            conn.execute(
                "insert into official_models "
                "(model_key, provider_id, display_name, supported_models, "
                "auth_type, source, gateway_ref, status, type, name) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("conn.test", "", "Test Connector", _json.dumps([]),
                 "none", "official", "", "active", "connector", "Test Connector"),
            )
            conn.commit()

        client = self._client()
        resp = client.get("/api/catalog/connectors")
        self.assertEqual(resp.status_code, 200)
        connectors = resp.json()["connectors"]
        for conn in connectors:
            self.assertEqual(
                conn.get("type"), "connector",
                f"/api/catalog/connectors 返回了非 connector 类型: {conn.get('type')}"
            )

    def test_connectors_endpoint_excludes_models_and_tools(self):
        """确保 /api/catalog/connectors 的结果中不含 model 或 tool 类型。"""
        client = self._client()
        resp = client.get("/api/catalog/connectors")
        self.assertEqual(resp.status_code, 200)
        connectors = resp.json()["connectors"]
        types_in_response = {c.get("type") for c in connectors}
        self.assertNotIn("model", types_in_response,
                         "/api/catalog/connectors 不应包含 model 类型")
        self.assertNotIn("tool", types_in_response,
                         "/api/catalog/connectors 不应包含 tool 类型")

    # ── 禁止区守卫 ──
    def test_forbidden_scope_clean(self):
        violations = assert_forbidden_clean()
        self.assertEqual(
            violations,
            [],
            f"禁止区扫描发现违规: {violations}",
        )
