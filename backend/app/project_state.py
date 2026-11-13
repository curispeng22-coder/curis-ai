"""项目级状态聚合（P0-6 前半：project_state）。

``ProjectState`` 从任务图 ``TaskGraph`` 聚合**进度 / 健康 / 成本**，并写回既有
``projects`` 表（T01 新增 ``progress_json`` 列，**不新建表**）。供 CEO 极简入口查看
「项目整体进度」。

设计要点：
- 聚合源为 TaskGraph（DAG）：progress = done/total；health 由终态/运行态推导；
  cost 累加各节点执行结果的 estimated_cost（无则按尝试次数近似）。
- ``persist()`` 复用 ``database.upsert_project_progress``（additive 写回 projects）。
- 零新依赖（标准库 json + 复用 ``database`` / ``tenant_context`` / ``task_graph``）。
"""
from __future__ import annotations

import json
from typing import Any

from .database import Database
from .task_graph import TaskGraph
from .tenant_context import TenantContext


class ProjectState:
    """项目级状态聚合器。"""

    def __init__(
        self, project_id: str, database: Database | None = None, tenant_id: str | None = None
    ) -> None:
        self.project_id = project_id
        self.database = database
        self.tenant_id = tenant_id or TenantContext.current_tenant_id()
        self.progress: float = 0.0
        self.health: str = "planned"
        self.cost: float = 0.0
        self.total: int = 0
        self.done: int = 0
        self.running: int = 0
        self.failed: int = 0
        self.pending: int = 0

    def aggregate(self, graph: TaskGraph) -> None:
        """从任务图聚合进度/健康/成本（就地更新属性）。"""
        nodes = list(graph.nodes.values())
        total = len(nodes)
        done = sum(1 for n in nodes if n.status == "done")
        running = sum(1 for n in nodes if n.status == "running")
        failed = sum(1 for n in nodes if n.status == "failed")
        pending = total - done - running - failed

        self.total = total
        self.done = done
        self.running = running
        self.failed = failed
        self.pending = pending
        self.progress = round(done / total * 100, 1) if total else 0.0

        # 健康度推导。
        if total == 0:
            self.health = "planned"
        elif graph.has_escalation() or failed > 0:
            self.health = "blocked"
        elif done == total:
            self.health = "completed"
        elif running > 0:
            self.health = "in_progress"
        else:
            self.health = "planned"

        # 成本：累加各节点执行结果的 estimated_cost（缺省按尝试次数近似）。
        cost = 0.0
        for n in nodes:
            res = n.result or {}
            c = res.get("estimated_cost")
            if isinstance(c, (int, float)):
                cost += float(c)
            else:
                cost += float(n.attempts)
        self.cost = round(cost, 4)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "progress": self.progress,
            "health": self.health,
            "cost": self.cost,
            "total": self.total,
            "done": self.done,
            "running": self.running,
            "failed": self.failed,
            "pending": self.pending,
        }

    def persist(self) -> None:
        """把聚合状态写回 projects 表（progress_json 列）。需已提供 database。"""
        if self.database is None:
            return
        status = "completed" if self.health == "completed" else (
            "blocked" if self.health == "blocked" else "active"
        )
        progress_json = json.dumps(self.to_dict(), ensure_ascii=False)
        self.database.upsert_project_progress(
            project_id=self.project_id,
            tenant_id=self.tenant_id,
            status=status,
            progress_json=progress_json,
        )
