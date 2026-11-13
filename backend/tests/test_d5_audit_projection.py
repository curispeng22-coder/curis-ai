"""AuditEvent 只读投影验收测试。

覆盖：
  * admin 鉴权（无 token → 401）；
  * 过滤（tenant_id / event_type / since）；
  * 白名单命名空间不泄漏（usage.* 不出现、非受控类型不出现）；
  * 只读投影不写任何数据；
  * 既有 D5 测试全绿（回归验证）。
"""
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conftest import _APPROVED_EVENT_TYPES, _APP_DIR, assert_forbidden_clean  # noqa: E402

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}


def _seed_events(db: Database, event_log: EvolutionEventLog) -> None:
    """Seed 若干 capability.* / governance.* / usage.* 事件用于审计过滤测试。"""
    import json
    with db.connect() as conn:
        conn.executemany(
            "insert into evolution_events (correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            [
                ("corr-1", "capability.gateway_created",
                 json.dumps({"gateway": "gw_x"}), "tenant-a"),
                ("corr-2", "capability.model_created",
                 json.dumps({"model": "m1"}), "tenant-b"),
                ("corr-3", "governance.type_created",
                 json.dumps({"type": "dt"}), "tenant-a"),
                ("corr-4", "governance.policy_set",
                 json.dumps({"policy": "p1"}), "default"),
                ("corr-5", "usage.gateway_call",
                 json.dumps({"model": "newapi"}), "tenant-a"),
                ("corr-6", "usage.model_call",
                 json.dumps({"model": "gpt"}), "tenant-b"),
            ],
        )
        conn.commit()


class AuditProjectionTest(unittest.TestCase):
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

    # ── AC1: admin 鉴权 ──
    def test_audit_endpoint_rejects_anonymous(self):
        client = self._client()
        resp = client.get("/api/platform/audit")  # no Authorization
        self.assertEqual(resp.status_code, 401)

    def test_audit_endpoint_rejects_wrong_token(self):
        client = self._client()
        resp = client.get(
            "/api/platform/audit",
            headers={"Authorization": "Bearer wrong-token"},
        )
        self.assertEqual(resp.status_code, 401)

    def test_audit_endpoint_accepts_admin(self):
        client = self._client()
        resp = client.get("/api/platform/audit", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("audit_events", resp.json())
        self.assertIn("total", resp.json())

    # ── AC2: 白名单命名空间不泄漏 ──
    def test_audit_only_returns_whitelist_namespaces(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        resp = client.get("/api/platform/audit", headers=ADMIN)
        events = resp.json()["audit_events"]
        event_types = {e["event_type"] for e in events}
        # usage.* 绝不应出现
        for t in event_types:
            self.assertFalse(
                t.startswith("usage."),
                f"usage.* 事件不应该出现在审计投影中: {t}",
            )
        # 仅 capability.* / governance.*
        for t in event_types:
            self.assertTrue(
                t.startswith("capability.") or t.startswith("governance."),
                f"未授权事件类型 {t} 不应出现在审计投影中",
            )
        # 应包含 4 条（2 capability + 2 governance），不包含 2 usage
        self.assertEqual(len(events), 4)

    # ── AC3: tenant_id 过滤 ──
    def test_audit_filter_by_tenant_id(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        resp = client.get(
            "/api/platform/audit?tenant_id=tenant-a", headers=ADMIN
        )
        events = resp.json()["audit_events"]
        self.assertEqual(len(events), 2)
        for e in events:
            self.assertEqual(e["tenant_id"], "tenant-a")

    # ── AC4: event_type 过滤 ──
    def test_audit_filter_by_event_type(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        resp = client.get(
            "/api/platform/audit?event_type=capability.gateway_created",
            headers=ADMIN,
        )
        events = resp.json()["audit_events"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "capability.gateway_created")

    # ── AC5: since 过滤 ──
    def test_audit_filter_by_since(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        # Use a far-future date to filter everything out
        resp = client.get(
            "/api/platform/audit?since=2099-01-01T00:00:00", headers=ADMIN
        )
        events = resp.json()["audit_events"]
        self.assertEqual(len(events), 0)

    # ── AC6: limit 参数 ──
    def test_audit_limit(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        resp = client.get("/api/platform/audit?limit=1", headers=ADMIN)
        events = resp.json()["audit_events"]
        self.assertLessEqual(len(events), 1)

    # ── AC7: tenant_id 缺失不 fail-closed（审计轨迹不同于 usage）──
    def test_audit_missing_tenant_id_not_fail_closed(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        resp = client.get("/api/platform/audit", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        # 应返回全局审计事件（至少 4 条受控命名空间事件）
        events = resp.json()["audit_events"]
        self.assertGreaterEqual(len(events), 4)

    # ── AC8: 只读投影不写 evolution_events ──
    def test_audit_endpoint_does_not_write(self):
        _seed_events(self.db, self.event_log)
        client = self._client()
        before = len(self.event_log.get_all())
        client.get("/api/platform/audit", headers=ADMIN)
        after = len(self.event_log.get_all())
        self.assertEqual(before, after, "审计投影端点不应写入任何 evolution_events 行")

    # ── AC9: 禁止区守卫 ──
    def test_forbidden_scope_clean(self):
        violations = assert_forbidden_clean()
        self.assertEqual(
            violations,
            [],
            f"禁止区扫描发现违规: {violations}",
        )
