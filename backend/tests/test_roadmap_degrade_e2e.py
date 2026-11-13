"""Roadmap ④ 降级实测端到端（真实 CLI 适配器 + 员工能力组合 + 升级 + 经验沉淀 + 节点可观测）。

补齐 P1 联调未覆盖的关键路径：
- 降级链耗尽 → 升级 CEO（has_escalation）。
- 降级事件写入节点 trace（pipeline 维度可观测，供 /api/pipeline/{id}/trace）。
- 经验沉淀（capability_lessons 成功/失败路径均写入）。

纯离线 / 不触真实外部网络；零新依赖。
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from typing import Any

from app.capability_adapters import CapabilityAdapterFactory
from app.capability_catalog import CapabilityCatalog
from app.capability_resolver import CapabilityResolver
from app.database import Database
from app.employee_capability_model import EmployeeCapabilityModel
from app.lesson_memory import LessonMemory
from app.pipeline_runtime import PipelineRuntime
from app.task_graph import TaskGraph, TaskNode


class DiffStatusReviewer:
    """仅当执行 status==success 且 output 含合法 diff 头时通过（与 P1 联调同款）。"""

    def review(self, task):  # noqa: A003 - 与 ResultReviewer 同签名
        result = task.executor_result or {}
        status = result.get("status", "")
        output = result.get("output", "") or ""
        passes = status == "success" and "--- a/" in output
        return {
            "passes": passes,
            "needs_rework": not passes,
            "escalated": False,
            "feedback": [] if passes else ["execution failed or no valid diff"],
        }


class _NullEventLog:
    database = None

    def record(self, **kwargs: Any) -> None:
        return None


def _tmp_db() -> str:
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    os.unlink(path)
    return path


def _fresh(db_path: str):
    db = Database(db_path)
    db.initialize()
    return db, CapabilityCatalog(db, _NullEventLog())


_DIFF = [
    sys.executable, "-c",
    "import sys; print('--- a/foo.py\\n+++ b/foo.py\\n@@ -1 +1 @@\\n-x\\n+y')",
]


class DegradeExhaustedTestCase(unittest.TestCase):
    """④ 关键缺口：降级链耗尽 → 升级 CEO（P1 未覆盖）。"""

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh(self.db_path)
        self.catalog.create(
            "ext.bad", "cli", name="Bad",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": "no-such-binary-xyz"}, "live_status": "available"},
        )
        emp = EmployeeCapabilityModel(self.db)
        emp.set_employee_capabilities("emp_only", ["ext.bad"], preferred="ext.bad")

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _runtime(self, lesson=None) -> PipelineRuntime:
        r = CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=True,
            adapter_factory=CapabilityAdapterFactory.build,
        )
        return PipelineRuntime(reviewer=DiffStatusReviewer(), resolver=r, database=self.db, lesson_memory=lesson)

    def test_exhausted_escalates_to_ceo(self) -> None:
        rt = self._runtime()
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "cli"}, employee_id="emp_only")
        g = TaskGraph()
        g.add_node(node)
        res = rt.run_node(node, g)
        self.assertEqual(res.status, "escalated")
        self.assertTrue(res.escalated)
        self.assertEqual(res.capability_path, ["ext.bad"])
        self.assertTrue(g.has_escalation())


class NodeTraceObservabilityTestCase(unittest.TestCase):
    """增强：降级链写入节点 trace（pipeline 维度可观测）。"""

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh(self.db_path)
        self.catalog.create(
            "ext.good", "cli", name="Good",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": _DIFF[0], "args": _DIFF[1:]}, "live_status": "available"},
        )
        self.catalog.create(
            "ext.bad", "cli", name="Bad",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": "no-such-binary-xyz"}, "live_status": "available"},
        )
        emp = EmployeeCapabilityModel(self.db)
        emp.set_employee_capabilities("emp1", ["ext.bad", "ext.good"], preferred="ext.bad")

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _runtime(self, lesson=None) -> PipelineRuntime:
        r = CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=True,
            adapter_factory=CapabilityAdapterFactory.build,
        )
        return PipelineRuntime(reviewer=DiffStatusReviewer(), resolver=r, database=self.db, lesson_memory=lesson)

    def test_node_trace_records_degradation(self) -> None:
        rt = self._runtime()
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "cli"}, employee_id="emp1")
        g = TaskGraph()
        g.add_node(node)
        res = rt.run_node(node, g)
        self.assertEqual(res.status, "done")
        # 节点能力路径应记录 [首选bad, 降级good]。
        self.assertEqual(node.capability_path, ["ext.bad", "ext.good"])
        # trace 应记录：bad 失败（含一次 rework 重试）+ good 成功。
        self.assertGreaterEqual(len(node.trace), 2)
        bad_events = [e for e in node.trace if e["tool"] == "ext.bad"]
        good_events = [e for e in node.trace if e["tool"] == "ext.good"]
        self.assertTrue(any(e["error"] is not None for e in bad_events))
        self.assertTrue(any(e["error"] is None for e in good_events))


class LessonMemoryTestCase(unittest.TestCase):
    """P0 七项能力：经验沉淀（成功/失败路径均写入 capability_lessons）。"""

    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh(self.db_path)
        self.catalog.create(
            "ext.good", "cli", name="Good",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": _DIFF[0], "args": _DIFF[1:]}, "live_status": "available"},
        )
        self.catalog.create(
            "ext.bad", "cli", name="Bad",
            runtime_meta={"adapter_kind": "cli", "adapter_config": {"command": "no-such-binary-xyz"}, "live_status": "available"},
        )
        emp = EmployeeCapabilityModel(self.db)
        emp.set_employee_capabilities("emp1", ["ext.bad", "ext.good"], preferred="ext.bad")
        emp.set_employee_capabilities("emp_only", ["ext.bad"], preferred="ext.bad")

    def tearDown(self) -> None:
        try:
            os.unlink(self.db_path)
        except Exception:
            pass

    def _runtime(self, lm: LessonMemory) -> PipelineRuntime:
        r = CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=True,
            adapter_factory=CapabilityAdapterFactory.build,
        )
        return PipelineRuntime(reviewer=DiffStatusReviewer(), resolver=r, database=self.db, lesson_memory=lm)

    def test_lesson_recorded_success_and_failure(self) -> None:
        lm = LessonMemory(self.db)
        rt = self._runtime(lm)
        # 成功路径：emp1 首选 bad → 降级 good → 完成。
        n1 = TaskNode(id="ok", goal="g", cap_requirement={"cap_type": "cli"}, employee_id="emp1")
        g1 = TaskGraph()
        g1.add_node(n1)
        rt.run_node(n1, g1)
        # 失败路径：emp_only 只有 bad → 耗尽 → 升级。
        n2 = TaskNode(id="fail", goal="g", cap_requirement={"cap_type": "cli"}, employee_id="emp_only")
        g2 = TaskGraph()
        g2.add_node(n2)
        rt.run_node(n2, g2)

        lessons = lm.list_all()
        outcomes = {l.get("outcome") for l in lessons}
        self.assertIn("success", outcomes)
        self.assertIn("fail", outcomes)


if __name__ == "__main__":
    unittest.main()
