"""ADR-0017 S2 D3.impl (issue 058) — 自可观测真实实现契约测试 + 禁止区守卫。

覆盖 issue 058 acceptance criteria 1-8（真实关联 + 真实聚合 + 自反馈闭环 + 禁止区）：
  - 真实聚合数值断言（call_count / success_rate / quality_line_hits 为真实数）；
  - get_department_event_stream 真实按部门关联（type_key 关联 + 租户作用域）；
  - department_observations 快照 round-trip（tenant-scoped：tenant-A 写、tenant-B 读为空）；
  - 未知 type_key 抛 KeyError；
  - 禁止区自扫描：department_observability.py 无 EvolutionEventLog.record /
    roi_schema / app.get("/api/observ" / app.post("/api/observ"。

使用临时 SQLite 库，不修改任何 app/ 业务代码（除被测模块自身行为）。
"""

import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.department_observability import DepartmentMetrics, DepartmentObservability
from app.tenant_context import DEFAULT_TENANT, TenantContext


_REPO_ROOT = Path(__file__).resolve().parents[2]
_APP_DIR = _REPO_ROOT / "backend" / "app"
_TARGET = _APP_DIR / "department_observability.py"


def _seed_department_event(
    db: Database,
    *,
    tenant_id: str,
    type_key: str,
    event_type: str = "dept.call",
    correlation_id: str | None = None,
    payload: dict | None = None,
) -> None:
    """在 evolution_events 中写入一条「部门关联」事件（测试数据，非生产写路径）。

    通过 payload.type_key 建立部门→事件真实关联；tenant_id 显式写入（因为
    EvolutionEventLog.record 不 stamp tenant_id，这里直接落库以模拟 S1 后真实数据）。
    """
    if payload is None:
        payload = {"type_key": type_key}
    corr = correlation_id if correlation_id is not None else f"{type_key}@call"
    with db.connect() as connection:
        connection.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            (corr, event_type, json.dumps(payload, ensure_ascii=False), tenant_id),
        )


class D3ImplObservabilityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.observability = DepartmentObservability(self.db, event_log=None)

    def tearDown(self):
        self.tmp.cleanup()

    # ── AC1/AC2：真实关联 + 真实聚合数值 ──
    def test_metrics_real_aggregation_numbers(self):
        # 在 default 租户下为 function.bi 写入 4 条关联事件（已知成功/质量标记）
        _seed_department_event(
            self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi",
            payload={"type_key": "function.bi", "success": True, "quality_line_hit": True},
        )
        _seed_department_event(
            self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi",
            payload={"type_key": "function.bi", "success": True, "quality_check": "pass"},
        )
        _seed_department_event(
            self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi",
            payload={"type_key": "function.bi", "success": False, "quality_line_hit": False},
        )
        _seed_department_event(
            self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi",
            payload={"type_key": "function.bi", "status": "success", "quality_score": 0.9},
        )

        metrics = self.observability.get_department_metrics("function.bi")
        self.assertIsInstance(metrics, DepartmentMetrics)
        self.assertEqual(metrics.type_key, "function.bi")
        # call_count = 4
        self.assertEqual(metrics.call_count, 4)
        # success: e1(True) + e2(True) + e4(status=success) = 3 → 0.75
        self.assertAlmostEqual(metrics.success_rate, 0.75, places=6)
        # quality: e1(True) + e2(pass) + e4(0.9>=0.8) = 3
        self.assertEqual(metrics.quality_line_hits, 3)
        # available_fields 仍声明可计算字段
        self.assertEqual(
            metrics.available_fields, ["call_count", "success_rate", "quality_line_hits"]
        )
        # event_stream 仅含与本部门关联的事件（真实关联，非全量投影）
        self.assertEqual(len(metrics.event_stream), 4)
        for event in metrics.event_stream:
            self.assertEqual(event["payload"]["type_key"], "function.bi")

    def test_metrics_empty_department_is_zero(self):
        # 未播种任何事件 → 零值，不抛错
        metrics = self.observability.get_department_metrics("function.hr")
        self.assertEqual(metrics.call_count, 0)
        self.assertAlmostEqual(metrics.success_rate, 0.0, places=6)
        self.assertEqual(metrics.quality_line_hits, 0)

    # ── AC2：真实关联（type_key 过滤，排除他部门事件）──
    def test_event_stream_correlated_by_type_key(self):
        _seed_department_event(self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi")
        _seed_department_event(self.db, tenant_id=DEFAULT_TENANT, type_key="function.bi")
        _seed_department_event(self.db, tenant_id=DEFAULT_TENANT, type_key="function.hr")
        _seed_department_event(self.db, tenant_id=DEFAULT_TENANT, type_key="function.hr")
        _seed_department_event(self.db, tenant_id=DEFAULT_TENANT, type_key="function.hr")

        bi_stream = self.observability.get_department_event_stream("function.bi")
        self.assertEqual(len(bi_stream), 2)
        for event in bi_stream:
            self.assertEqual(event["payload"]["type_key"], "function.bi")

        hr_stream = self.observability.get_department_event_stream("function.hr")
        self.assertEqual(len(hr_stream), 3)
        for event in hr_stream:
            self.assertEqual(event["payload"]["type_key"], "function.hr")

    def test_event_stream_correlation_via_correlation_id_prefix(self):
        # 无 payload.type_key，仅以 correlation_id 前缀 "<type_key>@" 关联
        with self.db.connect() as connection:
            connection.execute(
                "insert into evolution_events "
                "(correlation_id, event_type, payload, tenant_id) "
                "values (?, ?, ?, ?)",
                ("function.bi@external", "dept.call", json.dumps({}), DEFAULT_TENANT),
            )
        stream = self.observability.get_department_event_stream("function.bi")
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0]["correlation_id"], "function.bi@external")

    # ── AC1（续）：租户作用域（tenant-A 事件对 tenant-B 不可见）──
    def test_event_stream_tenant_isolated(self):
        with TenantContext.scope("tenant-a"):
            _seed_department_event(
                self.db, tenant_id="tenant-a", type_key="function.bi",
                payload={"type_key": "function.bi", "success": True},
            )
        with TenantContext.scope("tenant-b"):
            stream = self.observability.get_department_event_stream("function.bi")
            self.assertEqual(stream, [])  # tenant-b 看不到 tenant-a 的事件

    # ── AC1：未知 type_key 抛 KeyError ──
    def test_event_stream_unknown_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.observability.get_department_event_stream("function.unknown", 10)

    def test_metrics_unknown_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.observability.get_department_metrics("function.unknown")

    # ── AC3：自反馈闭环（建议 dict + 快照持久化，tenant-scoped）──
    def test_suggest_self_improvement_returns_dict_and_persists_snapshot(self):
        with TenantContext.scope("tenant-a"):
            _seed_department_event(
                self.db, tenant_id="tenant-a", type_key="function.bi",
                payload={"type_key": "function.bi", "success": True, "quality_line_hit": True},
            )
            suggestion = self.observability.suggest_self_improvement("function.bi", None)

            # 返回 dict，含建议条目且明确「不改码 / 不触发 Governor」
            self.assertIsInstance(suggestion, dict)
            self.assertIn("items", suggestion)
            self.assertFalse(suggestion["modifies_code"])
            self.assertFalse(suggestion["triggers_governor"])
            self.assertEqual(suggestion["type_key"], "function.bi")
            self.assertEqual(suggestion["tenant_id"], "tenant-a")

            # 快照已落 department_observations（tenant-scoped round-trip）
            rows_a = self.db.list_department_observations(tenant_id="tenant-a")
            self.assertEqual(len(rows_a), 1)
            row = rows_a[0]
            self.assertEqual(row["tenant_id"], "tenant-a")
            self.assertEqual(row["type_key"], "function.bi")
            metrics_back = json.loads(row["metrics_json"])
            self.assertEqual(metrics_back["call_count"], 1)
            self.assertAlmostEqual(metrics_back["success_rate"], 1.0, places=6)
            self.assertEqual(metrics_back["quality_line_hits"], 1)
            suggestion_back = json.loads(row["suggestion_json"])
            self.assertEqual(suggestion_back["type_key"], "function.bi")

        # tenant-b 看不到 tenant-a 的快照（跨租户隔离）
        with TenantContext.scope("tenant-b"):
            rows_b = self.db.list_department_observations(tenant_id="tenant-b")
            self.assertEqual(rows_b, [])

    def test_suggest_self_improvement_accepts_metrics_object(self):
        metrics = DepartmentMetrics(
            type_key="function.hr",
            observed_at="2026-07-08T00:00:00+00:00",
            call_count=2,
            success_rate=1.0,
            quality_line_hits=2,
        )
        suggestion = self.observability.suggest_self_improvement("function.hr", metrics)
        self.assertIsInstance(suggestion, dict)
        rows = self.db.list_department_observations(type_key="function.hr")
        self.assertEqual(len(rows), 1)

    def test_suggest_self_improvement_unknown_key_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.observability.suggest_self_improvement("function.unknown", None)

    # ── AC3（续）：默认不写 evolution_events ──
    def test_suggest_self_improvement_does_not_write_evolution_events(self):
        with TenantContext.scope("tenant-a"):
            before = len(self.db.list_department_observations(tenant_id="tenant-a"))
            # 直接数 evolution_events（tenant-a）
            with self.db.connect() as conn:
                before_events = conn.execute(
                    "select count(*) as c from evolution_events where tenant_id = ?",
                    ("tenant-a",),
                ).fetchone()["c"]
            self.observability.suggest_self_improvement(
                "function.bi",
                DepartmentMetrics(
                    type_key="function.bi", observed_at="t",
                    call_count=0, success_rate=0.0, quality_line_hits=0,
                ),
            )
            after = len(self.db.list_department_observations(tenant_id="tenant-a"))
            with self.db.connect() as conn:
                after_events = conn.execute(
                    "select count(*) as c from evolution_events where tenant_id = ?",
                    ("tenant-a",),
                ).fetchone()["c"]
            # 快照 +1，但 evolution_events 计数不变（默认不写 evolution_events）
            self.assertEqual(after, before + 1)
            self.assertEqual(after_events, before_events)

    # ── AC4 / 禁止区自扫描 ──
    def _grep_file(self, path: Path, pattern: str) -> list[str]:
        compiled = re.compile(pattern)
        hits: list[str] = []
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return hits
        for i, line in enumerate(text.splitlines(), start=1):
            if compiled.search(line):
                hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        return hits

    def _grep_app(self, pattern: str) -> list[str]:
        compiled = re.compile(pattern)
        hits: list[str] = []
        for path in _APP_DIR.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if compiled.search(line):
                    hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        return hits

    def test_forbidden_scope_no_evolution_event_log_record(self):
        hits = self._grep_file(_TARGET, r"EvolutionEventLog\.record")
        self.assertEqual(hits, [], f"禁止区命中 EvolutionEventLog.record: {hits}")

    def test_forbidden_scope_no_roi_schema(self):
        hits = self._grep_file(_TARGET, r"roi_schema")
        self.assertEqual(hits, [], f"禁止区命中 roi_schema: {hits}")

    def test_forbidden_scope_no_observ_endpoints(self):
        hits = self._grep_app(r'app\.(get|post|put|delete)\(\s*["\']/api/observ')
        self.assertEqual(hits, [], f"禁止区命中新 observ endpoint: {hits}")

    def test_forbidden_scope_no_department_id_leak_filter(self):
        # 仅允许以 tenant_id 作用域过滤；不应出现跨租户泄漏的 WHERE department_id 读路径
        hits = self._grep_file(_TARGET, r"WHERE\s+department_id")
        self.assertEqual(hits, [], f"禁止区命中 WHERE department_id 读路径过滤: {hits}")

    def test_constructor_signature_injects_database(self):
        self.assertIs(self.observability.database, self.db)


if __name__ == "__main__":
    unittest.main()
