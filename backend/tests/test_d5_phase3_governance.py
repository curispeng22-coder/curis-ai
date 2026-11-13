"""Phase-3 Governance 专项验证测试。

覆盖：
  2a. capability_source 三态展示（official / tenant_private / marketplace）
  2b. tenant_private 隔离（catalog 端点不暴露 tenant_private）
  2c. usage_event 可见但不暴露敏感配置
  2d. AuditEvent 白名单（tenant_private.* 命名空间事件不可见）
  2e. Admin 不提供 tenant_private 编辑入口（静态检查）
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


# ── test helpers ──

_SOURCE_TYPES = ["official", "tenant_private", "marketplace"]


def _seed_source_usage_events(db: Database, tenant_id: str = "t") -> None:
    """Seed 3 usage events, one per capability_source."""
    for source in _SOURCE_TYPES:
        with db.connect() as conn:
            conn.execute(
                "insert into evolution_events "
                "(correlation_id, event_type, payload, tenant_id) "
                "values (?, ?, ?, ?)",
                (
                    f"src-{source}",
                    "usage.model_call",
                    json.dumps(
                        {
                            "capability_type": "model",
                            "capability_source": source,
                            "model_name": "gpt-4",
                            "status": "success",
                        }
                    ),
                    tenant_id,
                ),
            )
            conn.commit()


def _seed_sensitive_usage_event(db: Database, tenant_id: str = "t") -> None:
    """Seed a usage event whose payload contains api_key / access_token / secret / password."""
    with db.connect() as conn:
        conn.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            (
                "sensitive-event",
                "usage.model_call",
                json.dumps(
                    {
                        "capability_type": "model",
                        "capability_source": "official",
                        "model_name": "gpt-4",
                        "status": "success",
                        "prompt_tokens": 100,
                        "completion_tokens": 50,
                        "api_key": "sk-deadbeef",
                        "access_token": "at-12345",
                        "secret": "s3cr3t!",
                        "password": "hunter2",
                    }
                ),
                tenant_id,
            ),
        )
        conn.commit()


def _seed_tenant_private_audit_event(db: Database, tenant_id: str = "t") -> None:
    """Seed a tenant_private.* audit event (should NOT appear in /api/platform/audit)."""
    with db.connect() as conn:
        conn.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            (
                "tp-audit-1",
                "tenant_private.capability.used",
                json.dumps({"message": "private capability usage"}),
                tenant_id,
            ),
        )
        conn.commit()


def _seed_governance_audit_event(db: Database, tenant_id: str = "t") -> None:
    """Seed a governance.* audit event (SHOULD appear in /api/platform/audit)."""
    with db.connect() as conn:
        conn.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            (
                "gov-audit-1",
                "governance.policy_set",
                json.dumps({"policy": "test_policy"}),
                tenant_id,
            ),
        )
        conn.commit()


_SENSITIVE_FIELDS = {"api_key", "access_token", "secret", "password"}
_PROJECTED_FIELDS = {
    "id", "task_id", "capability_type", "capability_id",
    "capability_source", "model_gateway_id", "model_name",
    "prompt_tokens", "completion_tokens", "total_tokens",
    "estimated_cost", "status",
}


class Phase3GovernanceTest(unittest.TestCase):
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

    # ── 2a. capability_source 三态展示 ──

    def test_usage_filter_capability_source_official(self):
        """GET ?tenant_id=t&capability_source=official → 仅返回 official。"""
        _seed_source_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t&capability_source=official",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e.get("capability_source"), "official")

    def test_usage_filter_capability_source_tenant_private(self):
        """GET ?tenant_id=t&capability_source=tenant_private → 仅返回 tenant_private。"""
        _seed_source_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t&capability_source=tenant_private",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e.get("capability_source"), "tenant_private")

    def test_usage_filter_capability_source_marketplace(self):
        """GET ?tenant_id=t&capability_source=marketplace → 仅返回 marketplace。"""
        _seed_source_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t&capability_source=marketplace",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertEqual(e.get("capability_source"), "marketplace")

    def test_usage_no_capability_source_filter_returns_all(self):
        """GET ?tenant_id=t（无 capability_source）→ 全部三条。"""
        _seed_source_usage_events(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertEqual(len(events), 3)

    # ── 2b. tenant_private 隔离 ──

    def test_catalog_capabilities_no_tenant_private_source(self):
        """catalog /api/catalog/capabilities 不含 source='tenant_private'。"""
        client = self._client()
        resp = client.get("/api/catalog/capabilities")
        self.assertEqual(resp.status_code, 200)
        capabilities = resp.json()["capabilities"]
        for cap in capabilities:
            self.assertNotEqual(
                cap.get("source"), "tenant_private",
                "catalog 能力不应包含 source='tenant_private'"
            )

    def test_catalog_models_no_tenant_private_source(self):
        """catalog /api/catalog/models 不含 source='tenant_private'。"""
        client = self._client()
        resp = client.get("/api/catalog/models")
        self.assertEqual(resp.status_code, 200)
        models = resp.json()["models"]
        for model in models:
            self.assertNotEqual(
                model.get("source"), "tenant_private",
                "catalog 模型不应包含 source='tenant_private'"
            )

    def test_catalog_connectors_no_tenant_private_source(self):
        """catalog /api/catalog/connectors 不含 source='tenant_private'。"""
        client = self._client()
        resp = client.get("/api/catalog/connectors")
        self.assertEqual(resp.status_code, 200)
        connectors = resp.json()["connectors"]
        for conn in connectors:
            self.assertNotEqual(
                conn.get("source"), "tenant_private",
                "catalog 连接器不应包含 source='tenant_private'"
            )

    # ── 2c. usage_event 可见但不暴露敏感配置 ──

    def test_usage_event_top_level_no_sensitive_fields(self):
        """usage_event 顶层字段不含 api_key / token / secret / password。

        _usage_event_from_row 只投影固定字段（id / task_id / capability_type /
        capability_id / capability_source / model_gateway_id / model_name /
        prompt_tokens / completion_tokens / total_tokens / estimated_cost /
        status）。sensitives 保留在 payload JSON 内，不提升到顶层。
        """
        _seed_sensitive_usage_event(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        for event in events:
            top_level_keys = set(event.keys())
            intersection = top_level_keys & _SENSITIVE_FIELDS
            self.assertEqual(
                intersection,
                set(),
                f"usage_event 顶层不应包含敏感字段，发现: {intersection}"
            )

    def test_usage_event_payload_retains_data(self):
        """usage_event payload 保留原始数据（含敏感字段在 payload 内）。

        仅确认系统没有抹除 payload，数据完整性保持。
        """
        _seed_sensitive_usage_event(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/usage?tenant_id=t",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["usage_events"]
        self.assertGreaterEqual(len(events), 1)
        payload = events[0].get("payload", {})
        self.assertEqual(payload.get("api_key"), "sk-deadbeef")
        self.assertEqual(payload.get("access_token"), "at-12345")

    # ── 2d. AuditEvent 白名单 ──

    def test_audit_rejects_tenant_private_namespace_events(self):
        """GET /api/platform/audit → 不返回 tenant_private.* 命名空间事件。

        白名单仅 capability.* / governance.*。
        """
        _seed_tenant_private_audit_event(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/audit?tenant_id=t",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["audit_events"]
        for e in events:
            self.assertFalse(
                e.get("event_type", "").startswith("tenant_private"),
                f"审计端点不应返回 tenant_private.* 事件: {e.get('event_type')}"
            )

    def test_audit_includes_governance_namespace_events(self):
        """GET /api/platform/audit → 返回 governance.* 事件。"""
        _seed_tenant_private_audit_event(self.db)
        _seed_governance_audit_event(self.db)
        client = self._client()
        resp = client.get(
            "/api/platform/audit?tenant_id=t",
            headers=ADMIN,
        )
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["audit_events"]
        governance_events = [
            e for e in events
            if (e.get("event_type") or "").startswith("governance.")
        ]
        self.assertGreaterEqual(len(governance_events), 1)

    def test_audit_only_returns_approved_namespaces(self):
        """审计端点返回的所有事件的 event_type 必须以 capability. 或 governance. 开头。"""
        _seed_tenant_private_audit_event(self.db)
        _seed_governance_audit_event(self.db)
        client = self._client()
        resp = client.get("/api/platform/audit?tenant_id=t", headers=ADMIN)
        self.assertEqual(resp.status_code, 200)
        events = resp.json()["audit_events"]
        for e in events:
            et = e.get("event_type", "")
            self.assertTrue(
                et.startswith("capability.") or et.startswith("governance."),
                f"审计事件 event_type 不在白名单: {et!r}"
            )

    # ── 2e. Admin 不提供 tenant_private 编辑入口 ──

    def test_main_tenant_private_count_unchanged(self):
        """main.py 中 Admin 端点（_require_platform_admin 保护）不含 tenant_private 引用。

        tenant_private 仅存在于 Workspace/catalog 上下文，Admin /api/platform/* 端点不提供
        tenant_private 编辑/保存入口。
        """
        main_path = Path(__file__).resolve().parents[1] / "app" / "main.py"
        text = main_path.read_text(encoding="utf-8")
        count = text.count("tenant_private")
        # 引用必须在 3≤count≤24 范围内（Workspace 扩展允许增加但不会爆炸）。
        # 2026-08-03 agent 运行时桥在 execute_model_gateway 增加 tenant_private agent
        # 分支（注释 + 错误消息各 1 处），count 20 → 22，故上限放宽至 24。
        self.assertGreaterEqual(count, 3,
            f"main.py 至少应有 3 处 tenant_private（Workspace 上下文），实际 {count}")
        self.assertLessEqual(count, 24,
            f"main.py tenant_private 引用不应显著增长，实际 {count}")
        # 以 _require_platform_admin 开头的行不应含 tenant_private
        admin_private_lines = [
            line for line in text.splitlines()
            if "tenant_private" in line and "def " in line
        ]
        # 收集含 tenant_private 且位于 Admin 段落的行
        lines_with_tenant_private = []
        in_admin_func = False
        for i, line in enumerate(text.splitlines(), 1):
            if "_require_platform_admin" in line:
                in_admin_func = True
            if "tenant_private" in line and in_admin_func:
                lines_with_tenant_private.append(f"L{i}: {line.strip()}")
            if in_admin_func and line.strip().startswith("return"):
                in_admin_func = False
        self.assertEqual(
            lines_with_tenant_private,
            [],
            f"Admin 端点不应含 tenant_private 引用: {lines_with_tenant_private}"
        )

    def test_capability_catalog_panel_no_tenant_private_reference(self):
        """CapabilityCatalogPanel.js 不含 tenant_private 引用（目录面板仅管理 official）。"""
        panel_path = (
            Path(__file__).resolve().parents[1]
            / ".." / "frontend" / "app" / "platform" / "CapabilityCatalogPanel.js"
        )
        text = panel_path.read_text(encoding="utf-8")
        self.assertNotIn(
            "tenant_private", text,
            "CapabilityCatalogPanel.js 不应引用 tenant_private"
        )

    def test_frontend_no_tenant_private_admin_endpoint(self):
        """前端 platform .js 文件中，除 UsageProjectionPanel.js 下拉选项外无 tenant_private 引用。"""
        platform_dir = (
            Path(__file__).resolve().parents[1]
            / ".." / "frontend" / "app" / "platform"
        )
        # 收集所有 .js 文件
        js_files = sorted(platform_dir.glob("*.js"))
        violations = []
        for jsf in js_files:
            text = jsf.read_text(encoding="utf-8")
            if "tenant_private" in text:
                # UsageProjectionPanel.js 中仅允许下拉选项引用
                if jsf.name == "UsageProjectionPanel.js":
                    lines = text.splitlines()
                    private_lines = [
                        i + 1
                        for i, line in enumerate(lines)
                        if "tenant_private" in line
                    ]
                    # 每行必须为 <option value="tenant_private"> 下拉选项（显示文本可中/英）
                    for ln in private_lines:
                        line = lines[ln - 1].strip()
                        if '<option value="tenant_private">' not in line:
                            violations.append(f"{jsf.name}:{ln}: {line}")
                else:
                    violations.append(jsf.name)
        self.assertEqual(
            violations, [],
            f"前端 platform 文件（除 UsageProjectionPanel 下拉选项外）不应包含 tenant_private: {violations}"
        )

    # ── 禁止区守卫 ──
    def test_forbidden_scope_clean(self):
        violations = assert_forbidden_clean()
        self.assertEqual(
            violations,
            [],
            f"禁止区扫描发现违规: {violations}",
        )
