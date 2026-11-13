"""常驻自动调度器（P0-2：自动调度器）。

``Scheduler`` 是「全自动任务流」的发动机：后台线程循环扫描 ``TaskGraph`` 的就绪节点
（依赖已完成 + 触发条件满足），自动派发给 ``PipelineRuntime`` 执行，**无需人工
dispatch**。支持触发条件最小集（定时 / 事件 / 条件，见 ``TriggerSpec``）。

设计要点：
- 后台线程循环（仿 ``issue_pipeline_api`` 的 ``threading.Thread(daemon=True)`` 范式），
  单进程、串行写安全（_db_lock 在 database 层保证）。
- ``run_once()`` 提供单轮扫描+派发（供单测 mock 验证派发行为，不依赖线程）。
- 完成（``is_complete``）或硬卡点升级（``has_escalation``）时自动停循环。
- ``SchedulerManager`` 管理多 graph 的调度器生命周期，由 ``main.py`` 在
  startup / shutdown 注册（start/stop）。

零新依赖：仅标准库 threading / time / datetime。
"""
from __future__ import annotations

import threading
import time
from datetime import datetime, timezone
from typing import Any, Callable

from .task_graph import TaskGraph


class Scheduler:
    """常驻自动调度器：按就绪态自动拉取待执行任务并派发。"""

    def __init__(
        self,
        graph: TaskGraph,
        runtime: Any | None = None,
        poll_interval: float = 2.0,
        max_loops: int | None = None,
        on_tick: Callable[["Scheduler"], None] | None = None,
    ) -> None:
        """初始化调度器。

        Args:
            graph: 要调度的任务图（共享对象，run_node 会就地更新节点状态）。
            runtime: PipelineRuntime 实例（提供 run_node(node, graph)）。
            poll_interval: 轮询间隔秒。
            max_loops: 最大循环次数（None=无限；测试可设小值）。
            on_tick: 每轮结束后的回调（可选，便于测试/观测）。
        """
        self.graph = graph
        self.runtime = runtime
        self.poll_interval = poll_interval
        self.max_loops = max_loops
        self.on_tick = on_tick
        self._running = False
        self._thread: threading.Thread | None = None
        self.loops = 0
        self.stop_reason: str | None = None
        self.lock = threading.Lock()

    # ── 生命周期 ──────────────────────────────────────────────────────────
    def start(self) -> None:
        """启动后台调度循环（幂等，已运行则忽略）。"""
        with self.lock:
            if self._running:
                return
            self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self, reason: str = "manual") -> None:
        """停止调度循环（幂等）。"""
        with self.lock:
            if not self._running:
                return
            self._running = False
            self.stop_reason = reason

    @property
    def is_running(self) -> bool:
        return self._running

    # ── 主循环 ────────────────────────────────────────────────────────────
    def _loop(self) -> None:
        while self._running:
            self.run_once()
            self.loops += 1
            if self.on_tick is not None:
                try:
                    self.on_tick(self)
                except Exception:
                    pass
            if self.graph.is_complete():
                self.stop(reason="completed")
                break
            if self.graph.has_escalation():
                self.stop(reason="escalated")
                break
            if self.max_loops is not None and self.loops >= self.max_loops:
                self.stop(reason="max_loops")
                break
            # 轮询间隔（运行中可被打断）。
            for _ in range(max(1, int(self.poll_interval * 10))):
                if not self._running:
                    break
                time.sleep(0.1)

    # ── 单轮派发（可单测） ─────────────────────────────────────────────────
    def run_once(self) -> list[Any]:
        """执行一轮：扫描就绪节点并派发。返回本轮派发的节点列表。

        就绪 = 依赖已完成 + 未处于终态/运行态 + 触发条件满足。
        """
        done = {
            nid for nid, n in self.graph.nodes.items() if n.status == "done"
        }
        ready = [
            n for n in self.graph.ready_nodes(done) if self._trigger_satisfied(n)
        ]
        for node in ready:
            node.status = "running"
            self._dispatch(node)
        return ready

    def _dispatch(self, node: Any) -> None:
        """派发单个节点给 runtime 执行（异常兜底为升级）。"""
        if self.runtime is None:
            node.status = "failed"
            node.note = "无 runtime 可派发"
            self.graph.escalations.append({
                "node_id": node.id,
                "reason": "无 runtime 可派发",
            })
            return
        try:
            self.runtime.run_node(node, self.graph)
        except Exception as error:  # noqa: BLE001 — 调度层兜底，避免单节点拖垮整图
            node.status = "failed"
            node.note = f"调度派发异常：{error}"
            self.graph.escalations.append({
                "node_id": node.id,
                "reason": f"调度派发异常：{error}",
            })

    @staticmethod
    def _trigger_satisfied(node: Any) -> bool:
        """触发条件最小集判定（委托 TaskGraph，单一事实来源，避免重复实现）。"""
        return TaskGraph._trigger_satisfied(node)


class SchedulerManager:
    """调度器生命周期管理器（单例风格，供 API / main.py 使用）。

    按 graph_id 维护活动调度器；提供 start / stop / stop_all / get。
    """

    def __init__(self) -> None:
        self._schedulers: dict[str, Scheduler] = {}
        self._lock = threading.Lock()

    def start_scheduler(
        self,
        graph: TaskGraph,
        runtime: Any | None = None,
        poll_interval: float = 2.0,
        max_loops: int | None = None,
        on_tick: Callable[[Scheduler], None] | None = None,
    ) -> Scheduler:
        """为某 graph 启动（或复用）常驻调度器。"""
        graph_id = graph.graph_id
        with self._lock:
            existing = self._schedulers.get(graph_id)
            if existing is not None and existing.is_running:
                return existing
            scheduler = Scheduler(
                graph=graph,
                runtime=runtime,
                poll_interval=poll_interval,
                max_loops=max_loops,
                on_tick=on_tick,
            )
            self._schedulers[graph_id] = scheduler
        scheduler.start()
        return scheduler

    def get(self, graph_id: str) -> Scheduler | None:
        with self._lock:
            return self._schedulers.get(graph_id)

    def is_running(self, graph_id: str) -> bool:
        with self._lock:
            sch = self._schedulers.get(graph_id)
            return sch is not None and sch.is_running

    def stop(self, graph_id: str, reason: str = "manual") -> bool:
        """停止指定 graph 的调度器。返回是否确有活动调度器。"""
        with self._lock:
            sch = self._schedulers.get(graph_id)
            if sch is None:
                return False
            sch.stop(reason=reason)
            self._schedulers.pop(graph_id, None)
            return True

    def stop_all(self, reason: str = "shutdown") -> None:
        """停止全部活动调度器（main.py shutdown 调用）。"""
        with self._lock:
            schedulers = list(self._schedulers.items())
            self._schedulers.clear()
        for graph_id, sch in schedulers:
            sch.stop(reason=reason)


# 进程级单例（模块加载即创建；main.py 的 startup/shutdown 操作它）。
scheduler_manager = SchedulerManager()
