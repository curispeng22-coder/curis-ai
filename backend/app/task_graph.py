"""动态任务图（DAG）（P0-1：动态任务图）。

``TaskGraph`` 表达任务的**依赖 / 输入输出 / 触发条件**，并提供：
- ``ready_nodes(done)``：就绪判定（依赖已全部完成且未处于终态/运行态）。
- ``topo_order()``：拓扑展开（Kahn 算法，环则回退插入序）。
- ``is_complete()``：全部节点完成判定。

与既有 ``IssueQueue``（扁平队列）不同，本结构是**带依赖的 DAG**，是「自动调度 +
验收/返工闭环」的数据基座。节点携带 ``cap_requirement``（能力需求），供
``CapabilityResolver`` 在调度时按需选能力（P0-4）。

设计要点：
- 零新依赖（仅标准库 dataclasses / typing）。
- 节点状态机：``pending → ready → running → review → approved → done``，失败为
  ``failed``（由 pipeline_runtime 触发重试/换能力/重规划/升级）。
- 可序列化（``to_dict`` / ``from_dict``）+ 从结构化计划构造（``from_plan``），
  供 API 展示 DAG 与持久化。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .capability_resolver import CapabilityRequirement

# 不参与「就绪」计算的节点状态（已完成 / 正在运行 / 已硬失败需升级）。
_NON_READY_STATES = frozenset({"done", "running", "failed"})

# 终态集合。
_TERMINAL_STATES = frozenset({"done", "failed"})


@dataclass
class TriggerSpec:
    """节点触发条件（最小集：定时 / 事件 / 条件）。

    Attributes:
        mode: ``scheduled`` | ``event`` | ``condition``（缺省 condition）。
        at: 定时触发时间（ISO 字符串，scheduled 模式用）。
        on_event: 关注的事件名（event 模式用）。
        condition: 条件表达式（condition 模式用，最小集仅作占位/可扩展）。
    """

    mode: str = "condition"
    at: str | None = None
    on_event: str | None = None
    condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "at": self.at,
            "on_event": self.on_event,
            "condition": self.condition,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "TriggerSpec":
        if not data:
            return cls()
        return cls(
            mode=data.get("mode", "condition"),
            at=data.get("at"),
            on_event=data.get("on_event"),
            condition=data.get("condition"),
        )


@dataclass
class TaskNode:
    """DAG 节点。

    Attributes:
        id: 节点唯一 ID。
        goal: 节点目标（自然语言）。
        deps: 依赖的节点 ID 列表（须全部完成才可就绪）。
        input_refs: 输入引用（如 ["n1.output"]），最小集占位。
        output_ref: 输出引用（如 "n3.output"）。
        trigger: 触发条件（TriggerSpec）。
        cap_requirement: 能力需求（dict 形态，运行时转 CapabilityRequirement）。
        employee_id: 可选员工 ID（T09-2）；运行时透传给 resolver 以员工能力组合选路。
        status: 节点状态机。
        timeout: 执行超时秒（默认 900，见架构 §8③）。
        rework_count: 已重试次数。
        cap_switch_count: 已换能力次数。
        attempts: 总尝试次数。
        result: 最近一次执行结果（dict）。
        note: 备注（如升级原因）。
    """

    id: str
    goal: str = ""
    deps: list[str] = field(default_factory=list)
    input_refs: list[str] = field(default_factory=list)
    output_ref: str | None = None
    trigger: TriggerSpec = field(default_factory=TriggerSpec)
    cap_requirement: dict[str, Any] = field(default_factory=dict)
    employee_id: str | None = None
    status: str = "pending"
    timeout: int = 900
    rework_count: int = 0
    cap_switch_count: int = 0
    attempts: int = 0
    result: dict[str, Any] | None = None
    note: str | None = None
    capability_path: list[str] = field(default_factory=list)  # 实际尝试的能力链（含降级）
    trace: list[dict[str, Any]] = field(default_factory=list)  # 降级/执行事件（pipeline 维度可观测）

    def cap_requirement_obj(self) -> CapabilityRequirement:
        """转换为 CapabilityRequirement（供 CapabilityResolver 使用）。"""
        req = self.cap_requirement or {}
        return CapabilityRequirement(
            cap_type=req.get("cap_type", "model"),
            io_schema=req.get("io_schema", {}) or {},
            permissions=req.get("permissions", []) or [],
            prefer_employee_bindings=req.get("prefer_employee_bindings", []) or [],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "goal": self.goal,
            "deps": list(self.deps),
            "input_refs": list(self.input_refs),
            "output_ref": self.output_ref,
            "trigger": self.trigger.to_dict(),
            "cap_requirement": dict(self.cap_requirement),
            "employee_id": self.employee_id,
            "status": self.status,
            "timeout": self.timeout,
            "rework_count": self.rework_count,
            "cap_switch_count": self.cap_switch_count,
            "attempts": self.attempts,
            "result": self.result,
            "note": self.note,
            "capability_path": list(self.capability_path),
            "trace": list(self.trace),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskNode":
        return cls(
            id=data["id"],
            goal=data.get("goal", ""),
            deps=list(data.get("deps", []) or []),
            input_refs=list(data.get("input_refs", []) or []),
            output_ref=data.get("output_ref"),
            trigger=TriggerSpec.from_dict(data.get("trigger")),
            cap_requirement=dict(data.get("cap_requirement", {}) or {}),
            employee_id=data.get("employee_id"),
            status=data.get("status", "pending"),
            timeout=int(data.get("timeout", 900) or 900),
            rework_count=int(data.get("rework_count", 0) or 0),
            cap_switch_count=int(data.get("cap_switch_count", 0) or 0),
            attempts=int(data.get("attempts", 0) or 0),
            result=data.get("result"),
            note=data.get("note"),
            capability_path=list(data.get("capability_path", []) or []),
            trace=list(data.get("trace", []) or []),
        )


class TaskGraph:
    """动态任务图（DAG）。

    节点以 ``id`` 索引；边通过 ``add_edge(from, to)``（to 依赖 from）或节点
    ``deps`` 字段表达。提供就绪判定 / 拓扑展开 / 完成判定。不支持循环依赖
    （``add_edge`` 会检测并拒绝成环）。
    """

    def __init__(self, graph_id: str | None = None) -> None:
        self.graph_id = graph_id or f"graph-{id(self)}"
        self.nodes: dict[str, TaskNode] = {}
        self.escalations: list[dict[str, Any]] = []

    # ── 构建 ──────────────────────────────────────────────────────────────
    def add_node(self, node: TaskNode) -> None:
        """加入一个节点（若 id 已存在则覆盖）。"""
        self.nodes[node.id] = node

    def add_edge(self, from_id: str, to_id: str) -> None:
        """声明依赖：``to_id`` 依赖 ``from_id``（即 to 在 from 完成后才就绪）。

        等价地：把 ``from_id`` 加入 ``to_id.deps``。若会构成环则拒绝。

        Raises:
            KeyError: 节点不存在。
            ValueError: 成环（拒绝）。
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            raise KeyError("add_edge 引用的节点不存在")
        if from_id == to_id:
            raise ValueError("依赖会构成环（自依赖），已拒绝")
        if from_id in self.nodes[to_id].deps:
            return  # 已存在，幂等
        # 预检：若 from_id 已经（传递）依赖 to_id，则再加 to_id→from_id 成环。
        if self._reaches_via_deps(from_id, to_id):
            raise ValueError("依赖会构成环，已拒绝")
        self.nodes[to_id].deps.append(from_id)

    def _reaches_via_deps(self, start: str, target: str) -> bool:
        """从 start 沿 deps（依赖）边是否能到达 target（即 start 是否依赖 target）。"""
        stack = [start]
        visited: set[str] = set()
        while stack:
            cur = stack.pop()
            if cur == target:
                return True
            if cur in visited:
                continue
            visited.add(cur)
            for nxt in self.nodes.get(cur, TaskNode(id=cur)).deps:
                stack.append(nxt)
        return False

    # ── 就绪 / 拓扑 / 完成 ─────────────────────────────────────────────────
    def ready_nodes(self, done: set[str] | None = None) -> list[TaskNode]:
        """返回当前可调度节点（依赖全部完成 + 触发条件满足 + 未处于非就绪态）。

        Args:
            done: 已完成节点 ID 集合（用于依赖判定；缺省用节点 status=='done'）。
        """
        done = done if done is not None else {
            nid for nid, n in self.nodes.items() if n.status == "done"
        }
        ready: list[TaskNode] = []
        for node in self.nodes.values():
            if node.id in done:
                continue
            if node.status in _NON_READY_STATES:
                continue
            if not all(dep in done for dep in node.deps):
                continue
            if not self._trigger_satisfied(node):
                continue
            ready.append(node)
        return ready

    def topo_order(self) -> list[str]:
        """拓扑展开（Kahn）。存在环时回退为插入顺序（保证不崩溃）。"""
        indeg = {nid: 0 for nid in self.nodes}
        adj: dict[str, list[str]] = {nid: [] for nid in self.nodes}
        # 边语义：dep → node（node 依赖 dep），即 indeg[node] += 1。
        for nid, node in self.nodes.items():
            for dep in node.deps:
                if dep in self.nodes:
                    adj[dep].append(nid)
                    indeg[nid] += 1
        queue = [nid for nid, d in indeg.items() if d == 0]
        order: list[str] = []
        while queue:
            cur = queue.pop(0)
            order.append(cur)
            for nxt in adj[cur]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        if len(order) == len(self.nodes):
            return order
        # 环：回退插入顺序。
        return list(self.nodes.keys())

    def is_complete(self) -> bool:
        """是否全部节点完成（终态为 done）。"""
        if not self.nodes:
            return False
        return all(n.status == "done" for n in self.nodes.values())

    def has_escalation(self) -> bool:
        """是否仍有升级中（未收敛）的节点。"""
        return any(n.status == "failed" for n in self.nodes.values()) or bool(
            self.escalations
        )

    def progress(self) -> dict[str, Any]:
        """聚合进度概览（供 API / project_state 复用）。"""
        total = len(self.nodes)
        done = sum(1 for n in self.nodes.values() if n.status == "done")
        failed = sum(1 for n in self.nodes.values() if n.status == "failed")
        running = sum(1 for n in self.nodes.values() if n.status == "running")
        return {
            "graph_id": self.graph_id,
            "total": total,
            "done": done,
            "running": running,
            "failed": failed,
            "pending": total - done - running - failed,
            "percent": round(done / total * 100, 1) if total else 0.0,
        }

    # ── 序列化 / 反序列化 ─────────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "escalations": list(self.escalations),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskGraph":
        graph = cls(graph_id=data.get("graph_id"))
        for nd in data.get("nodes", []) or []:
            graph.add_node(TaskNode.from_dict(nd))
        graph.escalations = list(data.get("escalations", []) or [])
        return graph

    # ── 触发条件（与 Scheduler 共用同一最小集判定） ─────────────────────────
    @staticmethod
    def _trigger_satisfied(node: "TaskNode") -> bool:
        """触发条件最小集判定（scheduled / event / condition）。

        - ``scheduled``：``at`` 为未来 ISO 时间则未到 → 不满足。
        - ``event`` / ``condition`` / 未知：默认满足（自动调度）。
        """
        trigger = node.trigger
        if trigger is None:
            return True
        if trigger.mode == "scheduled":
            at = trigger.at
            if not at:
                return True
            try:
                at_dt = datetime.fromisoformat(at)
                return datetime.now(timezone.utc) >= at_dt
            except Exception:
                return True
        # event / condition / 未知：默认满足（自动调度）。
        return True

    @classmethod
    def from_plan(cls, plan: dict[str, Any]) -> "TaskGraph":
        """从结构化计划（NLParser.plan 输出）构造 DAG。

        plan 结构：
            {"goal": str, "nodes": [{"id","goal","cap_type","deps":[...]}, ...]}
        """
        graph = cls(graph_id=plan.get("graph_id"))
        for nd in plan.get("nodes", []) or []:
            node = TaskNode(
                id=nd["id"],
                goal=nd.get("goal", ""),
                deps=list(nd.get("deps", []) or []),
                cap_requirement={
                    "cap_type": nd.get("cap_type", "model"),
                    "io_schema": nd.get("io_schema", {}) or {},
                    "permissions": nd.get("permissions", []) or [],
                    "prefer_employee_bindings": nd.get("prefer_employee_bindings", []) or [],
                },
                employee_id=nd.get("employee_id"),
                trigger=TriggerSpec.from_dict(nd.get("trigger")),
                timeout=int(nd.get("timeout", 900) or 900),
            )
            graph.add_node(node)
        return graph
