"""运行时 trace 事件服务（EvoFlow 复用 A2，append-only 可观测）。

把 TaskNode.trace（内存字段）升格为独立 ``runtime_trace_event`` append-only 表：
执行管道事件（能力调用 / token / 缓存命中 / 延迟）落库，供 CEO 侧只读查看
执行过程。设计见 docs/plan/evoflow-verified-reuse-plan.md A2。

纪律：
- append-only：只写不更新、不删除（审计语义）。
- 只读查询端点；不改变任何任务/执行语义。
- 不存密钥：payload 写前由调用方保证脱敏（本服务不做二次清洗）。
"""

from __future__ import annotations

import json
import uuid
from typing import Any

from .database import Database
from .tenant_context import TenantContext

_TRACE_FIELDS = (
    "run_id",
    "task_id",
    "task_ref",
    "event_type",
    "capability",
    "tokens_in",
    "tokens_out",
    "cache_hit",
    "latency_ms",
    "payload",
)


class RuntimeTraceService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def write_event(
        self,
        *,
        run_id: str,
        event_type: str,
        capability: str = "",
        task_id: str | None = None,
        task_ref: str | None = None,
        tokens_in: int | None = None,
        tokens_out: int | None = None,
        cache_hit: bool | None = None,
        latency_ms: int | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """写入一条 append-only trace 事件，返回事件行。"""
        tenant_id = TenantContext.current_tenant_id()
        event_id = f"tr-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into runtime_trace_event (
                  id, tenant_id, run_id, task_id, task_ref, event_type,
                  capability, tokens_in, tokens_out, cache_hit, latency_ms,
                  payload_json, created_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, current_timestamp)
                """,
                (
                    event_id,
                    tenant_id,
                    run_id,
                    task_id,
                    task_ref,
                    event_type,
                    capability,
                    tokens_in,
                    tokens_out,
                    1 if cache_hit else (0 if cache_hit is False else None),
                    latency_ms,
                    json.dumps(payload or {}, ensure_ascii=False),
                ),
            )
        return self._get(event_id)

    def list_recent(
        self, *, limit: int = 50, run_id: str | None = None
    ) -> list[dict[str, Any]]:
        """最近 trace 事件（可按 run_id 过滤），按时间倒序。"""
        tenant_id = TenantContext.current_tenant_id()
        limit = max(1, min(int(limit), 200))
        with self.database.connect() as connection:
            if run_id:
                rows = connection.execute(
                    "select * from runtime_trace_event "
                    "where tenant_id = ? and run_id = ? "
                    "order by created_at desc, rowid desc limit ?",
                    (tenant_id, run_id, limit),
                ).fetchall()
            else:
                rows = connection.execute(
                    "select * from runtime_trace_event "
                    "where tenant_id = ? "
                    "order by created_at desc, rowid desc limit ?",
                    (tenant_id, limit),
                ).fetchall()
        return [self._from_row(row) for row in rows]

    def _get(self, event_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from runtime_trace_event "
                "where tenant_id = ? and id = ?",
                (tenant_id, event_id),
            ).fetchone()
        if row is None:
            raise KeyError("trace event not found")
        return self._from_row(row)

    @staticmethod
    def _from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["payload"] = json.loads(item.pop("payload_json", "{}") or "{}")
        item["cache_hit"] = bool(item.get("cache_hit")) if item.get("cache_hit") is not None else None
        return item
