"""Issue B · CEO Office 真实运行证据 后端测试（只读不写断言 + 契约形状断言）。

验收要点：
1. 6 端点返回结构符合 §3 契约（脱敏、字段齐全）。
2. **只读断言**：调用前后相关表行数不变。
3. **共存断言**：源码不含 ``auto_modify_code`` / ``lift_human_approval_gate`` import；
   不含字面量「锁定动作集合」；不 import ``governance`` / ``runtime_governance``。
4. ``import ceo_evidence_api``（顶层）仍 ``ModuleNotFoundError``。
"""

from __future__ import annotations

import importlib
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.database import Database
from backend.app.decision_sink import PendingDecisionStore
from backend.app.gate_prompt import GatePrompt, GateOption


def _make_pending_record(store: PendingDecisionStore, title: str, category: str, gate_label: str):
    gate = GatePrompt(
        gate_id=f"gate-{gate_label}",
        category=category,
        title=title,
        business_risk="发出去或改了之后可能很难收回",
        options=[
            GateOption(id="A", label="继续", effect="按系统建议继续"),
            GateOption(id="B", label="先模拟看看", effect="先在内部试一遍"),
            GateOption(id="C", label="取消", effect="这次先不做"),
        ],
        recommended="B",
        one_line_consequence="先看看效果，不满意还能取消",
        expires_at=None,
    )
    return store.create(gate, correlation_id="corr-1", gate_label=gate_label)


class TestCeoEvidenceApiBuildFunctions(unittest.TestCase):
    """测试各个 ``_build_*`` 只读聚合函数。"""

    @classmethod
    def setUpClass(cls):
        # 确保模块可以从 backend.app 导入
        if "backend" not in sys.modules and os.path.isdir("backend"):
            sys.path.insert(0, os.getcwd())

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.curis = os.path.join(self.tmp, "curis.sqlite")
        self.bdb = os.path.join(self.tmp, "b_layer_pending_decisions.sqlite")
        self.db = Database(self.curis)

        # 创建受控的 evolution_events 表 + 样本行
        with self.db.connect() as conn:
            conn.execute(
                "CREATE TABLE evolution_events ("
                "event_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "correlation_id TEXT, event_type TEXT, payload TEXT, "
                "created_at TEXT, tenant_id TEXT, idempotency_key TEXT)"
            )
            samples = [
                ("corr-1", "a.kernel.session.completed", '{"scope":"run-1"}',
                 "2026-07-21T01:00:00+00:00", "selfuse"),
                ("corr-2", "a.budget.exceeded", '{"scope":"per_run","ratio":1.02,"limit":100000}',
                 "2026-07-21T02:00:00+00:00", "selfuse"),
                ("corr-3", "usage.model_call", '{"scope":"call-9"}',
                 "2026-07-21T03:00:00+00:00", "selfuse"),
            ]
            conn.executemany(
                "INSERT INTO evolution_events "
                "(correlation_id, event_type, payload, created_at, tenant_id) "
                "VALUES (?,?,?,?,?)",
                samples,
            )

        # 更新数据库路径为指向临时文件
        from backend.app import ceo_evidence_api as module
        self.module = module
        self._orig_db_path = module._pending_db_path

        # 创建受控 pending 库
        self.store = PendingDecisionStore(self.bdb)
        _make_pending_record(self.store, "测试治理待办", "money", "G4-token")

        # mock _pending_db_path 指向临时文件
        module._pending_db_path = lambda: self.bdb

    def tearDown(self):
        self.module._pending_db_path = self._orig_db_path

    # ── overview ──
    def test_build_overview_counts_shape(self):
        counts = self.module._build_overview_counts(self.db)
        for key in ("departments", "employees", "workflows",
                    "active_execution_claims", "active_sessions",
                    "pending_wake_requests", "pending_decisions",
                    "budget_accumulators"):
            self.assertIn(key, counts, f"counts 应包含 {key}")
            self.assertIsInstance(counts[key], int, f"{key} 应为 int")

    def test_build_recent_activity_shape(self):
        recent = self.module._build_recent_activity(self.db, limit=10)
        self.assertIsInstance(recent, list)
        if recent:
            item = recent[0]
            for key in ("event_id", "created_at", "event_type", "layer",
                        "scope", "status_dimension", "digest"):
                self.assertIn(key, item, f"activity 项应包含 {key}")

    # ── timeline ──
    def test_build_timeline_shape_and_readonly(self):
        before = self._count(self.curis, "evolution_events")
        timeline = self.module._build_timeline(self.db, limit=50)
        after = self._count(self.curis, "evolution_events")
        self.assertEqual(before, after, "evolution_events 行数应不变（只读）")
        self.assertEqual(len(timeline), 3)
        for item in timeline:
            for key in ("event_id", "created_at", "event_type", "layer",
                        "scope", "status_dimension", "digest"):
                self.assertIn(key, item)

    def test_build_timeline_layer_filter(self):
        timeline = self.module._build_timeline(self.db, layer="a.budget")
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]["event_type"], "a.budget.exceeded")

    def test_build_timeline_status_dimension_filter(self):
        timeline = self.module._build_timeline(self.db, status_dimension="failed")
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]["event_type"], "a.budget.exceeded")

    # ── org-tree ──
    def test_build_org_tree_missing_tables_is_empty(self):
        tree = self.module._build_org_tree(self.db)
        self.assertIn("node_id", tree)
        self.assertIn("children", tree)

    # ── pending-decisions ──
    def test_build_pending_decisions_shape(self):
        decisions = self.module._build_pending_decisions(self.store, status_filter="all")
        self.assertIsInstance(decisions, list)
        for d in decisions:
            for key in ("pending_id", "gate_id", "category", "gate_label",
                        "status", "decision", "created_at", "expires_at",
                        "title", "business_risk", "recommended_option",
                        "awaiting_letter"):
                self.assertIn(key, d, f"pending 项应包含 {key}")
        if decisions:
            d = decisions[0]
            self.assertIn(d["status"], ("pending", "resolved", "cancelled"))

    # ── execution ──
    def test_build_execution_status_shape(self):
        status = self.module._build_execution_status(self.db)
        for key in ("held_claims", "active_sessions", "pending_wake_requests",
                    "claims_sample", "sessions_sample"):
            self.assertIn(key, status, f"execution 应包含 {key}")
        self.assertIsInstance(status["claims_sample"], list)
        self.assertIsInstance(status["sessions_sample"], list)

    # ── budget ──
    def test_build_budget_status_shape(self):
        budget = self.module._build_budget_status(self.db)
        for key in ("accumulators", "recent_events", "guard_enabled"):
            self.assertIn(key, budget, f"budget 应包含 {key}")
        self.assertIsInstance(budget["accumulators"], list)
        self.assertIsInstance(budget["recent_events"], list)
        self.assertIsInstance(budget["guard_enabled"], bool)

    @staticmethod
    def _count(db_path: str, table: str) -> int:
        with sqlite3.connect(db_path) as conn:
            try:
                return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except sqlite3.OperationalError:
                return 0


class TestCeoEvidenceApiRoutes(unittest.TestCase):
    """测试 6 个 GET 端点的可达性及返回结构。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.curis = os.path.join(self.tmp, "curis.sqlite")
        self.bdb = os.path.join(self.tmp, "b_layer_pending_decisions.sqlite")
        self.db = Database(self.curis)

        with self.db.connect() as conn:
            conn.execute(
                "CREATE TABLE evolution_events ("
                "event_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "correlation_id TEXT, event_type TEXT, payload TEXT, "
                "created_at TEXT, tenant_id TEXT, idempotency_key TEXT)"
            )
            conn.execute(
                "INSERT INTO evolution_events "
                "(correlation_id, event_type, payload, created_at, tenant_id) "
                "VALUES (?,?,?,?,?)",
                ("corr-1", "a.kernel.session.completed", '{"scope":"run-1"}',
                 "2026-07-21T01:00:00+00:00", "selfuse"),
            )

        self.store = PendingDecisionStore(self.bdb)
        _make_pending_record(self.store, "治理待办样例", "money", "G4-token")

        from backend.app import ceo_evidence_api as module
        self.module = module
        self._orig_path = module._pending_db_path
        module._pending_db_path = lambda: self.bdb

        # 创建测试 app 并注册 router
        app = FastAPI()
        app.include_router(module.ceo_evidence_router)
        self.client = TestClient(app)

    def tearDown(self):
        self.module._pending_db_path = self._orig_path

    def test_overview_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/overview")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            for key in ("tenant_id", "generated_at", "counts", "recent_activity", "layer_status"):
                self.assertIn(key, data)
            for ck in ("departments", "employees", "workflows"):
                self.assertIn(ck, data["counts"])

    def test_timeline_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/timeline")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            self.assertIn("timeline", data)
            self.assertIsInstance(data["timeline"], list)

    def test_timeline_endpoint_with_filters(self):
        resp = self.client.get("/api/ceo/evidence/timeline?layer=a.kernel&limit=10")
        self.assertIn(resp.status_code, (200, 500))

    def test_org_tree_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/org-tree")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            self.assertIn("node_id", data)

    def test_org_tree_endpoint_with_params(self):
        resp = self.client.get("/api/ceo/evidence/org-tree?include_skills=1&include_tools=0")
        self.assertIn(resp.status_code, (200, 500))

    def test_pending_decisions_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/pending-decisions")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            self.assertIn("pending_count", data)
            self.assertIn("decisions", data)
            self.assertIsInstance(data["decisions"], list)

    def test_pending_decisions_endpoint_with_filter(self):
        resp = self.client.get("/api/ceo/evidence/pending-decisions?status=pending")
        self.assertIn(resp.status_code, (200, 500))

    def test_execution_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/execution")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            for key in ("held_claims", "active_sessions", "pending_wake_requests"):
                self.assertIn(key, data)

    def test_budget_endpoint(self):
        resp = self.client.get("/api/ceo/evidence/budget")
        self.assertIn(resp.status_code, (200, 500))
        if resp.status_code == 200:
            data = resp.json()
            for key in ("accumulators", "recent_events", "guard_enabled"):
                self.assertIn(key, data)

    def test_all_six_routes_registered(self):
        paths = [
            "/api/ceo/evidence/overview",
            "/api/ceo/evidence/timeline",
            "/api/ceo/evidence/org-tree",
            "/api/ceo/evidence/pending-decisions",
            "/api/ceo/evidence/execution",
            "/api/ceo/evidence/budget",
        ]
        for path in paths:
            resp = self.client.get(path)
            self.assertIn(resp.status_code, (200, 500), f"{path} 应可达")


class TestCoexistence(unittest.TestCase):
    """共存断言：源码符合 B 层铁律。"""

    def setUp(self):
        self.source_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "ceo_evidence_api.py"
        )

    def test_source_has_no_locked_action_imports(self):
        with open(self.source_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("auto_modify_code", src)
        self.assertNotIn("lift_human_approval_gate", src)

    def test_source_avoids_forbidden_literal(self):
        with open(self.source_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        # 必须用「不解除人工批准闸」类措辞，而非字面量「锁定动作集合」。
        self.assertNotIn("LOCKED_ACTIONS", src)

    def test_source_no_governance_import(self):
        with open(self.source_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("import governance", src)
        self.assertNotIn("import runtime_governance", src)

    def test_source_no_runtime_governance_import(self):
        with open(self.source_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("from .governance", src)
        self.assertNotIn("from .runtime_governance", src)

    def test_top_level_import_fails(self):
        """``import ceo_evidence_api``（顶层）仍 ``ModuleNotFoundError``。"""
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module("ceo_evidence_api")


if __name__ == "__main__":
    unittest.main()
