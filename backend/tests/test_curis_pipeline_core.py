"""Curis 后端核心（P0）单元测试。

覆盖 T01–T06 核心逻辑 + T07 部分 API：
- T01：official_models.runtime_meta_json 迁移 + capability_lessons 表 + CapabilityCatalog runtime_meta 读写。
- T02：CapabilityResolver 降级链（首选可用 / 首选不可用降级 / 耗尽抛升级）。
- T03：TaskGraph ready_nodes / topo_order / is_complete / 成环防护。
- T04：Scheduler 派发（mock runtime）。
- T05：pipeline_runtime 重试→换能力→重规划→升级 分支。
- T06：lesson_memory 持久化与 query（含去重累加）；project_state 聚合与写回。
- T07：pipeline API 的 /graph / /auto-run / /lessons（含注入 fake runtime 的端到端最小链路）。

运行：``cd backend && python -m pytest tests/test_curis_pipeline_core.py -v``
"""
from __future__ import annotations

import os
import tempfile
import threading
import time
import unittest
from typing import Any

from app.capability_catalog import CapabilityCatalog
from app.capability_resolver import (
    AUTO_DEGRADE_SILENT,
    CapabilityExhausted,
    CapabilityHandle,
    CapabilityRequirement,
    CapabilityResolver,
)
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.issue_pipeline import ResultReviewer
from app.issue_pipeline_api import pipeline_router
from app.lesson_memory import LessonMemory
from app.pipeline_runtime import NodeResult, PipelineRuntime
from app.project_state import ProjectState
from app.scheduler import Scheduler, scheduler_manager
from app.task_graph import TaskGraph, TaskNode, TriggerSpec

from fastapi import FastAPI
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# 测试辅助
# ---------------------------------------------------------------------------

def _tmp_db() -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    return tmp.name


def _fresh_catalog(db_path: str):
    db = Database(db_path)
    db.initialize()
    catalog = CapabilityCatalog(db, EvolutionEventLog(db))
    return db, catalog


class _FakeAdapter:
    """可控 DevAgent：按调用顺序返回预设 outputs。"""

    def __init__(self, outputs: list[dict[str, Any]]):
        self.outputs = list(outputs)
        self.calls = 0

    def execute(self, prompt: str) -> dict[str, Any]:
        idx = min(self.calls, len(self.outputs) - 1)
        out = self.outputs[idx]
        self.calls += 1
        return out


class _ConstAdapter:
    """固定返回单个 output 的 DevAgent（resolver 测试用）。"""

    def __init__(self, key: str, output: dict[str, Any] | None = None):
        self.key = key
        self.output = output or {"output": f"out:{key}", "status": "success"}

    def execute(self, prompt: str) -> dict[str, Any]:
        return self.output


PASS_OUTPUT = {
    "output": "--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-old\n+new\n",
    "status": "success",
}
FAIL_OUTPUT = {"output": "no diff here", "status": "error:boom"}


class _FakeResolver:
    """测试用解析器：按 plan 顺序返回能力句柄，尊重 exclude_keys；耗尽则抛升级。

    每个 key 复用同一个适配器实例（贴近真实 resolver：同一能力返回稳定句柄），
    使降级链在多次 resolve 间保持调用计数连续（重规划后重试仍朝 PASS 推进）。
    """

    def __init__(self, plan: list[tuple[str, list[dict[str, Any]]]], cap_type: str = "model"):
        # plan: [(key, [output, output, ...]), ...]
        self.plan = plan
        self.cap_type = cap_type
        self.resolve_calls: list[tuple[str, list[str]]] = []
        self._adapters: dict[str, _FakeAdapter] = {}

    def resolve(
        self,
        req: CapabilityRequirement,
        exclude_keys: list[str] | None = None,
        employee_id: str | None = None,
    ):
        exclude = set(exclude_keys or [])
        for key, outputs in self.plan:
            if key not in exclude:
                self.resolve_calls.append((key, sorted(exclude)))
                adapter = self._adapters.get(key)
                if adapter is None:
                    adapter = _FakeAdapter(outputs)
                    self._adapters[key] = adapter
                return CapabilityHandle(
                    key=key,
                    type=self.cap_type,
                    adapter=adapter,
                    backup_keys=[],
                    cost=0.0,
                )
        raise CapabilityExhausted(reason="降级链耗尽（测试）", cap_type=self.cap_type)


# ===========================================================================
# T01：能力注册表扩展
# ===========================================================================

class TestT01RegistryExtension(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)

    def tearDown(self) -> None:
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except Exception:
            pass

    def test_migration_columns_and_table(self) -> None:
        """runtime_meta_json 列 + capability_lessons 表均存在。"""
        with self.db.connect() as conn:
            cols = [r["name"] for r in conn.execute("pragma table_info(official_models)")]
            self.assertIn("runtime_meta_json", cols)
            tbl = conn.execute(
                "select name from sqlite_master where type='table' and name='capability_lessons'"
            ).fetchone()
            self.assertIsNotNone(tbl)

    def test_catalog_runtime_meta_roundtrip(self) -> None:
        """create 写 runtime_meta，get 反序列化读回。"""
        self.catalog.create(
            "tool-x",
            "tool",
            name="X",
            runtime_meta={
                "cost_per_unit": 0.01,
                "permissions": ["repo.write"],
                "backup_chain": ["tool-y", "tool-z"],
                "live_status": "available",
                "credentials_ref": "env:FOO_KEY",
            },
        )
        row = self.catalog.get("tool-x")
        self.assertEqual(row["runtime_meta"]["live_status"], "available")
        self.assertEqual(row["runtime_meta"]["cost_per_unit"], 0.01)
        self.assertEqual(row["runtime_meta"]["backup_chain"], ["tool-y", "tool-z"])
        self.assertEqual(row["runtime_meta"]["credentials_ref"], "env:FOO_KEY")

    def test_catalog_runtime_meta_default_live_status(self) -> None:
        """未给 live_status 时默认 unknown。"""
        self.catalog.create("tool-w", "tool", name="W", runtime_meta={"cost_per_unit": 0.0})
        row = self.catalog.get("tool-w")
        self.assertEqual(row["runtime_meta"]["live_status"], "unknown")

    def test_catalog_rejects_bad_credential_ref(self) -> None:
        with self.assertRaises(ValueError):
            self.catalog.create(
                "tool-bad", "tool", name="B", runtime_meta={"credentials_ref": "plaintext-key"}
            )

    def test_capability_lessons_persist(self) -> None:
        """capability_lessons 可写入并查回。"""
        self.db.save_capability_lesson(
            tenant_id="selfuse",
            signature="sig1",
            cap_path=["a", "b"],
            outcome="success",
            reason="ok",
        )
        rows = self.db.list_capability_lessons(signature="sig1")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["cap_path"], ["a", "b"])
        self.assertEqual(rows[0]["outcome"], "success")


# ===========================================================================
# T02：能力解析器降级链
# ===========================================================================

class TestT02Resolver(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db, self.catalog = _fresh_catalog(self.db_path)
        # 注册三个 tool 能力，构成降级链 a→b→c。
        self.catalog.create(
            "cap-a", "tool", name="A",
            runtime_meta={"backup_chain": ["cap-b", "cap-c"], "live_status": "available"},
        )
        self.catalog.create(
            "cap-b", "tool", name="B",
            runtime_meta={"backup_chain": ["cap-c"], "live_status": "available"},
        )
        self.catalog.create(
            "cap-c", "tool", name="C",
            runtime_meta={"backup_chain": [], "live_status": "available"},
        )
        self.resolver = CapabilityResolver(
            self.catalog,
            database=self.db,
            adapter_factory=lambda cap: _ConstAdapter(cap["capability_key"]),
            auto_degrade_silent=True,
        )

    def tearDown(self) -> None:
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except Exception:
            pass

    def _set_status(self, key: str, live: str) -> None:
        self.catalog.update_runtime_meta(key, {"live_status": live})

    def test_primary_available(self) -> None:
        self._set_status("cap-a", "available")
        handle = self.resolver.resolve(CapabilityRequirement(cap_type="tool"))
        self.assertEqual(handle.key, "cap-a")

    def test_primary_unavailable_silent_degrade(self) -> None:
        self._set_status("cap-a", "unavailable")
        self._set_status("cap-b", "available")
        handle = self.resolver.resolve(CapabilityRequirement(cap_type="tool"))
        self.assertEqual(handle.key, "cap-b")
        self.assertIn("cap-a", handle.backup_keys)

    def test_chain_exhausted_raises(self) -> None:
        self._set_status("cap-a", "unavailable")
        self._set_status("cap-b", "unavailable")
        self._set_status("cap-c", "unavailable")
        with self.assertRaises(CapabilityExhausted):
            self.resolver.resolve(CapabilityRequirement(cap_type="tool"))

    def test_no_candidate_raises(self) -> None:
        with self.assertRaises(CapabilityExhausted):
            self.resolver.resolve(CapabilityRequirement(cap_type="skill"))

    def test_non_silent_mode_raises_unavailable(self) -> None:
        self._set_status("cap-a", "unavailable")
        resolver = CapabilityResolver(
            self.catalog, database=self.db, auto_degrade_silent=False,
            adapter_factory=lambda cap: _ConstAdapter(cap["capability_key"]),
        )
        # 首选不可用且非静默 → 直接抛 CapabilityUnavailable（不降级）。
        from app.capability_resolver import CapabilityUnavailable
        self._set_status("cap-b", "available")
        with self.assertRaises(CapabilityUnavailable):
            resolver.resolve(CapabilityRequirement(cap_type="tool"))


# ===========================================================================
# T03：动态任务图
# ===========================================================================

class TestT03TaskGraph(unittest.TestCase):
    def test_ready_nodes_and_topo(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="n1", goal="g1", deps=[]))
        g.add_node(TaskNode(id="n2", goal="g2", deps=["n1"]))
        g.add_node(TaskNode(id="n3", goal="g3", deps=["n2"]))
        # 初始：仅 n1 就绪。
        ready = g.ready_nodes()
        self.assertEqual([n.id for n in ready], ["n1"])
        # n1 完成后：n2 就绪。
        g.nodes["n1"].status = "done"
        ready = g.ready_nodes()
        self.assertEqual([n.id for n in ready], ["n2"])
        # 拓扑序 n1→n2→n3。
        self.assertEqual(g.topo_order(), ["n1", "n2", "n3"])

    def test_is_complete(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="n1", goal="g1"))
        g.add_node(TaskNode(id="n2", goal="g2"))
        self.assertFalse(g.is_complete())
        g.nodes["n1"].status = "done"
        g.nodes["n2"].status = "done"
        self.assertTrue(g.is_complete())

    def test_cycle_rejected(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="a", goal="ga"))
        g.add_node(TaskNode(id="b", goal="gb"))
        # b 依赖 a
        g.add_edge("a", "b")
        # 让 a 依赖 b 会成环 → 拒绝。
        with self.assertRaises(ValueError):
            g.add_edge("b", "a")

    def test_serialization_roundtrip(self) -> None:
        g = TaskGraph(graph_id="g1")
        g.add_node(TaskNode(id="n1", goal="g1", deps=[], cap_requirement={"cap_type": "model"}))
        g.add_node(TaskNode(id="n2", goal="g2", deps=["n1"]))
        data = g.to_dict()
        g2 = TaskGraph.from_dict(data)
        self.assertEqual(g2.graph_id, "g1")
        self.assertEqual(set(g2.nodes.keys()), {"n1", "n2"})
        self.assertEqual(g2.nodes["n2"].deps, ["n1"])

    def test_from_plan(self) -> None:
        plan = {
            "goal": "做一个功能",
            "nodes": [
                {"id": "n1", "goal": "分析", "cap_type": "model", "deps": []},
                {"id": "n2", "goal": "实现", "cap_type": "model", "deps": ["n1"]},
            ],
        }
        g = TaskGraph.from_plan(plan)
        self.assertEqual(g.nodes["n2"].deps, ["n1"])
        self.assertEqual(g.nodes["n1"].cap_requirement["cap_type"], "model")

    def test_trigger_scheduled(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="n1", goal="g", trigger=TriggerSpec(mode="scheduled", at="2099-01-01T00:00:00+00:00")))
        # 未来时间未到 → 不满足触发 → 不就绪。
        self.assertEqual(g.ready_nodes(), [])
        g.nodes["n1"].trigger = TriggerSpec(mode="condition")
        self.assertEqual([n.id for n in g.ready_nodes()], ["n1"])


# ===========================================================================
# T04：调度器派发
# ===========================================================================

class TestT04Scheduler(unittest.TestCase):
    def test_run_once_dispatches_ready(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="n1", goal="g1"))
        g.add_node(TaskNode(id="n2", goal="g2", deps=["n1"]))
        calls: list[str] = []

        class _RT:
            def run_node(self, node, graph):
                calls.append(node.id)
                node.status = "done"
                return NodeResult(node_id=node.id, status="done")

        sched = Scheduler(g, runtime=_RT(), poll_interval=0.01)
        sched.run_once()
        # n1 执行并标记完成；n2 因 n1 刚完成、本轮 deps 判定基于传入 done 集合（不含刚完成的 n1）。
        self.assertIn("n1", calls)
        self.assertEqual(g.nodes["n1"].status, "done")
        # 第二轮：n2 就绪。
        sched.run_once()
        self.assertIn("n2", calls)
        self.assertTrue(g.is_complete())

    def test_scheduler_stops_on_complete(self) -> None:
        g = TaskGraph()
        g.add_node(TaskNode(id="n1", goal="g"))

        class _RT:
            def run_node(self, node, graph):
                node.status = "done"
                return NodeResult(node_id=node.id, status="done")

        sched = Scheduler(g, runtime=_RT(), poll_interval=0.01, max_loops=10)
        sched.start()
        # 等待完成。
        for _ in range(50):
            if sched.is_running is False:
                break
            time.sleep(0.02)
        self.assertFalse(sched.is_running)
        self.assertTrue(g.is_complete())


# ===========================================================================
# T05：验收/返工自动闭环
# ===========================================================================

class TestT05PipelineRuntime(unittest.TestCase):
    def _rt(self, resolver_plan, max_cap_switch=2):
        reviewer = ResultReviewer()
        resolver = _FakeResolver(resolver_plan)
        return PipelineRuntime(reviewer=reviewer, resolver=resolver, max_cap_switch=max_cap_switch)

    def test_retry_then_success(self) -> None:
        """同能力重试一次后通过（rework 分支）。"""
        rt = self._rt([("c1", [FAIL_OUTPUT, PASS_OUTPUT])])
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "model"})
        g = TaskGraph(); g.add_node(node)
        result = rt.run_node(node, g)
        self.assertEqual(result.status, "done")
        self.assertFalse(result.escalated)

    def test_switch_capability_then_success(self) -> None:
        """首选失败→换能力→通过（switch 分支）。"""
        rt = self._rt([
            ("c1", [FAIL_OUTPUT, FAIL_OUTPUT]),
            ("c2", [PASS_OUTPUT]),
        ])
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "model"})
        g = TaskGraph(); g.add_node(node)
        result = rt.run_node(node, g)
        self.assertEqual(result.status, "done")
        # 应经历 c1（含一次重试）后切到 c2。
        self.assertIn(("c2", ["c1"]), rt.resolver.resolve_calls)

    def test_replan_then_success(self) -> None:
        """三次能力均失败→重规划→重置后以新策略通过。"""
        rt = self._rt([
            ("c1", [FAIL_OUTPUT, FAIL_OUTPUT, FAIL_OUTPUT, PASS_OUTPUT]),
            ("c2", [FAIL_OUTPUT, FAIL_OUTPUT]),
            ("c3", [FAIL_OUTPUT, FAIL_OUTPUT]),
        ], max_cap_switch=2)
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "model"})
        g = TaskGraph(); g.add_node(node)
        result = rt.run_node(node, g)
        self.assertEqual(result.status, "done")
        self.assertFalse(result.escalated)

    def test_escalate_on_exhaust(self) -> None:
        """降级链立即耗尽→升级 CEO（escalated）。"""
        rt = self._rt([])  # 空 plan → resolve 直接抛 CapabilityExhausted
        node = TaskNode(id="n1", goal="g", cap_requirement={"cap_type": "model"})
        g = TaskGraph(); g.add_node(node)
        result = rt.run_node(node, g)
        self.assertTrue(result.escalated)
        self.assertEqual(node.status, "failed")
        self.assertTrue(g.has_escalation())
        self.assertIsNotNone(result.reason)


# ===========================================================================
# T06：经验沉淀 + 项目状态
# ===========================================================================

class TestT06MemoryAndState(unittest.TestCase):
    def setUp(self) -> None:
        self.db_path = _tmp_db()
        self.db = Database(self.db_path)
        self.db.initialize()

    def tearDown(self) -> None:
        try:
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except Exception:
            pass

    def test_lesson_record_and_query(self) -> None:
        lm = LessonMemory(self.db)
        lm.record(signature="sigA", cap_path=["c1", "c2"], outcome="success", reason="ok")
        rows = lm.query("sigA")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["outcome"], "success")
        self.assertEqual(rows[0]["cap_path"], ["c1", "c2"])

    def test_lesson_dedup_increments_reuse(self) -> None:
        lm = LessonMemory(self.db)
        lm.record(signature="sigB", cap_path=["c1"], outcome="fail", reason="r1")
        lm.record(signature="sigB", cap_path=["c1"], outcome="fail", reason="r1")
        rows = lm.query("sigB")
        self.assertEqual(len(rows), 1)  # 去重为同一行
        self.assertEqual(rows[0]["reused_count"], 2)  # 累加

    def test_best_path(self) -> None:
        lm = LessonMemory(self.db)
        lm.record(signature="sigC", cap_path=["c1", "c3"], outcome="success", reason="ok")
        self.assertEqual(lm.best_path("sigC"), ["c1", "c3"])
        self.assertIsNone(lm.best_path("nope"))

    def test_project_state_aggregate_and_persist(self) -> None:
        g = TaskGraph(graph_id="proj-1")
        g.add_node(TaskNode(id="n1", goal="g1", status="done", result=PASS_OUTPUT))
        g.add_node(TaskNode(id="n2", goal="g2", status="running"))
        g.add_node(TaskNode(id="n3", goal="g3"))
        ps = ProjectState("proj-1", database=self.db)
        ps.aggregate(g)
        self.assertEqual(ps.total, 3)
        self.assertEqual(ps.done, 1)
        self.assertAlmostEqual(ps.progress, 33.3, places=1)
        self.assertEqual(ps.health, "in_progress")
        ps.persist()
        with self.db.connect() as conn:
            row = conn.execute(
                "select progress_json, status from projects where project_id=?", ("proj-1",)
            ).fetchone()
            self.assertIsNotNone(row)
            self.assertIn("progress", row["progress_json"])


# ===========================================================================
# T07：Pipeline API（graph / auto-run / lessons）+ 端到端最小链路
# ===========================================================================

class _FakeRuntime(PipelineRuntime):
    """测试用 runtime：直接标记节点完成（不触网）。"""

    def run_node(self, node, graph):
        node.status = "done"
        node.result = {"output": "ok", "status": "success"}
        return NodeResult(
            node_id=node.id, status="done", output=node.result,
            capability_path=[node.cap_requirement.get("cap_type", "model")],
        )


class TestT07PipelineAPI(unittest.TestCase):
    def setUp(self) -> None:
        app = FastAPI()
        app.include_router(pipeline_router)
        self.client = TestClient(app)
        # 注入 fake runtime，使 auto-run 端到端可完成而不触网。
        import app.issue_pipeline_api as api
        api._build_runtime_fn = lambda graph: _FakeRuntime(reviewer=ResultReviewer())
        # 本类测试不依赖 DB：强制清空模块级 _pipeline_database，避免被其他用例
        # 经 main.py startup 注入的真实 DB 污染（保证 /lessons 走「无 DB→[]」分支）。
        api._pipeline_database = None
        self.api = api

    def tearDown(self) -> None:
        scheduler_manager.stop_all(reason="test_teardown")
        self.api._build_runtime_fn = None

    def test_submit_returns_graph_id(self) -> None:
        resp = self.client.post("/api/pipeline/submit", json={"natural_language": "请实现一个登录功能"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("id", data)
        self.assertIn("graph_id", data)
        self.assertEqual(data["status"], "pending")

    def test_graph_endpoint_404_and_200(self) -> None:
        self.client.post("/api/pipeline/submit", json={"natural_language": "实现一个搜索功能"})
        # 未知 graph_id → 404。
        r404 = self.client.get("/api/pipeline/nope/graph")
        self.assertEqual(r404.status_code, 404)
        # 这里直接往 registry 塞一个已知 graph，验证 200 与结构。
        from app.task_graph import TaskGraph, TaskNode
        g = TaskGraph(graph_id="g-test")
        g.add_node(TaskNode(id="n1", goal="g"))
        self.api._graph_registry["g-test"] = g
        r200 = self.client.get("/api/pipeline/g-test/graph")
        self.assertEqual(r200.status_code, 200)
        self.assertEqual(r200.json()["graph_id"], "g-test")
        self.assertIn("nodes", r200.json())

    def test_lessons_endpoint(self) -> None:
        # 未注入 DB → 返回空列表（不报错）。
        r = self.client.get("/api/pipeline/lessons")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), [])

    def test_auto_run_end_to_end(self) -> None:
        """auto-run 启动常驻调度 → 2 节点 DAG 自动完成（端到端最小链路）。"""
        from app.task_graph import TaskGraph, TaskNode
        g = TaskGraph(graph_id="g-e2e")
        g.add_node(TaskNode(id="n1", goal="g1"))
        g.add_node(TaskNode(id="n2", goal="g2", deps=["n1"]))
        self.api._graph_registry["g-e2e"] = g

        r = self.client.post("/api/pipeline/g-e2e/auto-run")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "running")

        # 轮询等待完成（后台线程调度）。
        for _ in range(100):
            if g.is_complete():
                break
            time.sleep(0.02)
        self.assertTrue(g.is_complete())
        self.assertEqual(g.nodes["n1"].status, "done")
        self.assertEqual(g.nodes["n2"].status, "done")


if __name__ == "__main__":
    unittest.main()
