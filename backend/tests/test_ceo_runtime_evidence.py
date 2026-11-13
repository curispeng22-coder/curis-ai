"""Issue B · CEO Office 真实运行证据 后端测试（只读不写断言 + 契约形状断言）。

验收要点：
1. 各 ``build_*`` / 端点返回结构符合 §3 契约。
2. **只读断言**：调用前后 ``evolution_events`` / ``b_layer_pending_decisions``
   行数不变；``decision_sink`` 仅读、无 ``resolve`` / ``cancel`` 调用痕迹。
3. **共存断言**：``ceo_runtime_evidence.py`` 源码不含 ``auto_modify_code`` /
   ``lift_human_approval_gate`` import；不含字面量「锁定动作集合」。
"""

from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.database import Database
from backend.app import ceo_runtime_evidence as module
from backend.app.decision_sink import PendingDecisionStore
from backend.app.gate_prompt import GatePrompt, GateOption


def _make_module_record(
    store: PendingDecisionStore,
    title: str,
    category: str,
    gate_label: str,
):
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


class FakePendingStore:
    """仅实现 list_pending 的假 store，用于断言 build 函数只读、不调用写方法。"""

    def __init__(self, records):
        self._records = records
        self.calls: list[str] = []

    def list_pending(self, correlation_id=None):
        self.calls.append("list_pending")
        return self._records


class FakePendingRecord:
    def __init__(self, gate_snapshot: str):
        self.pending_id = "fake-pending-id"
        self.gate_label = "G4-token"
        self.category = "money"
        self.gate_snapshot = gate_snapshot
        self.status = "pending"
        self.created_at = "2026-07-21T01:02:03+00:00"
        self.expires_at = "2026-07-21T02:02:03+00:00"


class TestCeoRuntimeEvidenceBuild(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.curis = os.path.join(self.tmp, "curis.sqlite")
        self.bdb = os.path.join(self.tmp, "b_layer_pending_decisions.sqlite")
        self.db = Database(self.curis)
        # 受控 evolution_events 表 + 样本行（含 a.kernel / a.budget / usage 类）。
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
        # 受控 b_layer pending 库 + 1 条 pending。
        self.store = PendingDecisionStore(self.bdb)
        _make_module_record(
            self.store,
            "这次可能要花掉远超预期的算力钱",
            "money",
            "G4-token",
        )

    # ── B2 时间线 ──
    def test_build_runtime_timeline_shape_and_readonly(self):
        before = self._count(self.curis, "evolution_events")
        timeline = module.build_runtime_timeline(self.db, limit=50)
        after = self._count(self.curis, "evolution_events")
        self.assertEqual(before, after, "evolution_events 行数应不变（只读）")
        self.assertEqual(len(timeline), 3)
        for item in timeline:
            for key in ("event_id", "event_type", "category", "status_dimension",
                        "scope_key", "summary", "created_at"):
                self.assertIn(key, item)
        # 倒序：最近 created_at 在前。
        self.assertEqual(timeline[0]["event_type"], "usage.model_call")
        # status_dimension 映射正确。
        by_type = {t["event_type"]: t["status_dimension"] for t in timeline}
        self.assertEqual(by_type["a.kernel.session.completed"], "completed")
        self.assertEqual(by_type["a.budget.exceeded"], "hard_stop")
        self.assertEqual(by_type["usage.model_call"], "completed")

    def test_build_runtime_timeline_category_filter(self):
        timeline = module.build_runtime_timeline(
            self.db, categories=("a.budget",)
        )
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]["event_type"], "a.budget.exceeded")

    # ── B4 pending 决策 ──
    def test_build_pending_decisions_shape_and_readonly(self):
        before = self._count(self.bdb, "b_layer_pending_decisions")
        decisions = module.build_pending_decisions(self.store)
        after = self._count(self.bdb, "b_layer_pending_decisions")
        self.assertEqual(before, after, "b_layer_pending_decisions 行数应不变（只读）")
        self.assertEqual(len(decisions), 1)
        d = decisions[0]
        for key in ("pending_id", "gate_label", "category", "title",
                    "business_risk", "options", "recommended", "status",
                    "awaiting_letter", "created_at", "expires_at"):
            self.assertIn(key, d)
        self.assertEqual(d["status"], "pending")
        self.assertEqual(d["awaiting_letter"], "A/B/C")
        self.assertEqual(len(d["options"]), 3)

    def test_build_pending_decisions_only_reads(self):
        fake = FakePendingStore([
            FakePendingRecord(json.dumps({
                "gate_id": "g", "category": "money", "title": "t",
                "business_risk": "r",
                "options": [{"id": "A", "label": "继续", "effect": "e"}],
                "recommended": "A", "one_line_consequence": "c",
            }))
        ])
        out = module.build_pending_decisions(fake)
        self.assertEqual(fake.calls, ["list_pending"])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["title"], "t")

    # ── B5 执行状态（空库也应返回契约形状，不报错）──
    def test_build_execution_status_shape(self):
        status = module.build_execution_status(self.db)
        for key in ("claims", "sessions", "wake_requests"):
            self.assertIn(key, status)
            self.assertIsInstance(status[key], list)

    # ── B6 预算状态 ──
    def test_build_budget_status_shape_and_readonly(self):
        before = self._count(self.curis, "evolution_events")
        budget = module.build_budget_status(self.db)
        after = self._count(self.curis, "evolution_events")
        self.assertEqual(before, after, "evolution_events 行数应不变（只读）")
        self.assertIn("totals", budget)
        self.assertIn("recent_exceeded", budget)
        self.assertIn("accumulators", budget)
        self.assertEqual(budget["totals"]["exceeded"], 1)
        self.assertEqual(len(budget["recent_exceeded"]), 1)
        self.assertEqual(budget["recent_exceeded"][0]["ratio"], 1.02)

    # ── B3 组织树（表不存在时应 fail-open 返回空树，不报错）──
    def test_build_org_tree_missing_tables_is_empty(self):
        tree = module.build_org_tree(self.db)
        self.assertIn("companies", tree)
        self.assertIsInstance(tree["companies"], list)

    @staticmethod
    def _count(db_path: str, table: str) -> int:
        with sqlite3.connect(db_path) as conn:
            try:
                return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except sqlite3.OperationalError:
                return 0


class TestCeoEvidenceRoutes(unittest.TestCase):
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
        _make_module_record(self.store, "治理待办样例", "money", "G4-token")
        # 让端点里的 PendingDecisionStore 指向受控库。
        self._orig_path = module._default_db_path
        module._default_db_path = lambda: self.bdb

        app = FastAPI()
        module.register_ceo_evidence_routes(app, self.db)
        self.client = TestClient(app)

    def tearDown(self):
        module._default_db_path = self._orig_path

    def test_routes_registered(self):
        for path in (
            "/api/ceo/runtime-timeline",
            "/api/ceo/org-tree",
            "/api/ceo/pending-decisions",
            "/api/ceo/execution-status",
            "/api/ceo/budget-status",
        ):
            resp = self.client.get(path)
            self.assertIn(resp.status_code, (200, 500), path)

    def test_pending_decisions_endpoint_shape(self):
        resp = self.client.get("/api/ceo/pending-decisions")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("pending_count", data)
        self.assertIn("decisions", data)
        self.assertEqual(data["pending_count"], 1)
        self.assertEqual(len(data["decisions"]), 1)

    def test_runtime_timeline_endpoint_shape(self):
        resp = self.client.get("/api/ceo/runtime-timeline")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("timeline", data)
        self.assertEqual(len(data["timeline"]), 1)


class TestCoexistence(unittest.TestCase):
    """共存断言：源码不含锁定动作集合解除路径、不含禁用字面量。"""

    def test_source_has_no_locked_action_imports(self):
        src = self._read_source()
        self.assertNotIn("auto_modify_code", src)
        self.assertNotIn("lift_human_approval_gate", src)

    def test_source_avoids_forbidden_literal(self):
        src = self._read_source()
        # 必须用「不解除人工批准闸」类措辞，而非字面量「锁定动作集合」。
        self.assertNotIn("锁定动作集合", src)

    @staticmethod
    def _read_source() -> str:
        path = os.path.join(
            os.path.dirname(__file__), "..", "app", "ceo_runtime_evidence.py"
        )
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()


if __name__ == "__main__":
    unittest.main()
