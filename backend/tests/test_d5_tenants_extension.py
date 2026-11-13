"""ADR-0017 S1 D1.impl (issue 063): 租户扩展 CRUD 验收测试。

覆盖：
  * 租户 CRUD（创建/读取/更新/列表）；
  * 状态机 active ↔ inactive ↔ suspended + 非法 status 拒绝；
  * admin 鉴权（无 token → 401）；
  * tenant_id 重复冲突 → 409；
  * 禁止区守卫（零命中）。
"""
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conftest import assert_forbidden_clean, _APP_DIR  # noqa: E402

from app.database import Database  # noqa: E402
from app.main import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


class TenantsExtensionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()

    def tearDown(self):
        self.tmp.cleanup()

    def _client(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        return TestClient(create_app(self.db.path))

    # ── AC1: GET /api/platform/tenants 返回新字段 ──
    def test_list_tenants_includes_new_columns(self):
        client = self._client()
        resp = client.get("/api/platform/tenants", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        tenants = resp.json()["tenants"]
        self.assertGreaterEqual(len(tenants), 1)
        default = next(t for t in tenants if t["tenant_id"] == "selfuse")
        self.assertIn("plan_tier", default)
        self.assertIn("contact_email", default)
        self.assertIn("status", default)
        self.assertIn("description", default)
        self.assertEqual(default["status"], "active")
        self.assertEqual(default["plan_tier"], "free")

    # ── AC2: POST /api/platform/tenants 创建租户 ──
    def test_create_tenant_via_api(self):
        client = self._client()
        payload = {
            "tenant_id": "tenant-01",
            "name": "Tenant One",
            "plan_tier": "growth",
            "contact_email": "admin@tenant1.com",
            "description": "A test tenant",
        }
        resp = client.post("/api/platform/tenants", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["tenant_id"], "tenant-01")
        self.assertEqual(data["name"], "Tenant One")
        self.assertEqual(data["plan_tier"], "growth")
        self.assertEqual(data["contact_email"], "admin@tenant1.com")
        self.assertEqual(data["status"], "active")
        self.assertEqual(data["description"], "A test tenant")

    # ── AC3: 创建时缺省字段使用默认值 ──
    def test_create_tenant_defaults(self):
        client = self._client()
        resp = client.post(
            "/api/platform/tenants",
            json={"tenant_id": "tenant-min", "name": "Minimal"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["plan_tier"], "free")
        self.assertEqual(data["contact_email"], "")
        self.assertEqual(data["status"], "active")
        self.assertEqual(data["description"], "")

    # ── AC4: tenant_id 重复 → 409 ──
    def test_create_duplicate_tenant_conflict(self):
        client = self._client()
        payload = {"tenant_id": "dup", "name": "First"}
        resp = client.post("/api/platform/tenants", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 201)
        resp = client.post("/api/platform/tenants", json=payload, headers=ADMIN)
        self.assertEqual(resp.status_code, 409)

    # ── AC5: 无管理员令牌 → 401 ──
    def test_admin_only_401(self):
        client = self._client()
        no_auth = {}

        resp = client.get("/api/platform/tenants", headers=no_auth)
        self.assertEqual(resp.status_code, 401)

        resp = client.post(
            "/api/platform/tenants",
            json={"tenant_id": "t", "name": "T"},
            headers=no_auth,
        )
        self.assertEqual(resp.status_code, 401)

        resp = client.put(
            "/api/platform/tenants/t",
            json={"status": "inactive"},
            headers=no_auth,
        )
        self.assertEqual(resp.status_code, 401)

        resp = client.get("/api/platform/tenants/t", headers=no_auth)
        self.assertEqual(resp.status_code, 401)

    # ── AC6: PUT 更新租户字段 ──
    def test_update_tenant_fields(self):
        client = self._client()
        client.post(
            "/api/platform/tenants",
            json={"tenant_id": "t-upd", "name": "Original"},
            headers=ADMIN,
        )
        resp = client.put(
            "/api/platform/tenants/t-upd",
            json={"name": "Updated", "plan_tier": "growth", "description": "desc"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["name"], "Updated")
        self.assertEqual(data["plan_tier"], "growth")
        self.assertEqual(data["description"], "desc")

    # ── AC7: 仅更新部分字段不影响其他字段 ──
    def test_update_partial_fields(self):
        client = self._client()
        client.post(
            "/api/platform/tenants",
            json={
                "tenant_id": "t-partial",
                "name": "Partial",
                "contact_email": "p@t.com",
            },
            headers=ADMIN,
        )
        resp = client.put(
            "/api/platform/tenants/t-partial",
            json={"name": "Renamed"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["name"], "Renamed")
        self.assertEqual(data["contact_email"], "p@t.com")

    # ── AC8: GET /api/platform/tenants/{tenant_id} ──
    def test_get_single_tenant(self):
        client = self._client()
        client.post(
            "/api/platform/tenants",
            json={"tenant_id": "t-get", "name": "Get Me", "plan_tier": "growth"},
            headers=ADMIN,
        )
        resp = client.get("/api/platform/tenants/t-get", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["tenant_id"], "t-get")
        self.assertEqual(resp.json()["plan_tier"], "growth")

    # ── AC9: 不存在的租户 → 404 ──
    def test_get_nonexistent_tenant_404(self):
        client = self._client()
        resp = client.get("/api/platform/tenants/no-such-tenant", headers=ADMIN)
        self.assertEqual(resp.status_code, 404)

    # ── AC10: 状态机 active → inactive → suspended ──
    def test_status_machine_transitions(self):
        client = self._client()
        client.post(
            "/api/platform/tenants",
            json={"tenant_id": "t-status", "name": "Status Test"},
            headers=ADMIN,
        )

        # active → inactive
        resp = client.put(
            "/api/platform/tenants/t-status",
            json={"status": "inactive"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "inactive")

        # inactive → suspended
        resp = client.put(
            "/api/platform/tenants/t-status",
            json={"status": "suspended"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "suspended")

        # suspended → active
        resp = client.put(
            "/api/platform/tenants/t-status",
            json={"status": "active"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "active")

    # ── AC11: 非法 status 拒绝 → 422 ──
    def test_invalid_status_rejected(self):
        client = self._client()
        client.post(
            "/api/platform/tenants",
            json={"tenant_id": "t-bad", "name": "Bad Status"},
            headers=ADMIN,
        )
        resp = client.put(
            "/api/platform/tenants/t-bad",
            json={"status": "deleted"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

        resp = client.put(
            "/api/platform/tenants/t-bad",
            json={"status": "unknown"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 422)

    # ── AC12: 不存在的租户 PUT → 404 ──
    def test_update_nonexistent_tenant_404(self):
        client = self._client()
        resp = client.put(
            "/api/platform/tenants/no-such",
            json={"name": "Ghost"},
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 404)

    # ── AC13: database 层 set_tenant_status 直接测试 ──
    def test_set_tenant_status_direct(self):
        self.db.create_tenant("t-db", "Direct Test")
        row = self.db.set_tenant_status("t-db", "inactive")
        self.assertEqual(row["status"], "inactive")
        row = self.db.set_tenant_status("t-db", "suspended")
        self.assertEqual(row["status"], "suspended")
        row = self.db.set_tenant_status("t-db", "active")
        self.assertEqual(row["status"], "active")

    # ── AC14: database 层非法 status → ValueError ──
    def test_invalid_status_valueerror(self):
        self.db.create_tenant("t-val", "Validate")
        with self.assertRaises(ValueError):
            self.db.set_tenant_status("t-val", "deleted")

    # ── AC15: database 层 create duplicate → IntegrityError ──
    def test_create_duplicate_database(self):
        self.db.create_tenant("t-dup", "First")
        with self.assertRaises(Exception):
            self.db.create_tenant("t-dup", "Second")

    # ── AC16: 禁止区守卫 ──
    def test_forbidden_scope_zero_hits(self):
        violations = assert_forbidden_clean()
        self.assertEqual(violations, [], f"禁止区命中: {violations}")


if __name__ == "__main__":
    unittest.main()
