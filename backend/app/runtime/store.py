"""Curis Business Runtime —— 流转留痕持久化（A1 契约第 4 条）。

把每一次成功流转写入 ``runtime_transition_log`` 表。沿用 ``Database.connect()``
上下文管理器与 ``TenantContext`` 租户隔离，因此：

- 流转日志与业务表同库、同租户策略；
- 进程重启不丢（落库而非内存）。

这是 A2（持久化队列 + 后台 worker）之前，状态机唯一允许的落库通道。
"""

from __future__ import annotations

import json
from typing import Any

from ..database import Database
from ..tenant_context import TenantContext
from .registry import runtime_registry
from .state_machine import TransitionRecord, TransitionRecorder


_SCHEMA = """
create table if not exists runtime_transition_log (
  log_id        integer primary key autoincrement,
  tenant_id     text not null default 'selfuse',
  entity_type   text not null,
  entity_id     text not null,
  source        text not null,
  target        text not null,
  trigger       text not null default '',
  actor         text not null,
  at            text not null,
  reason        text not null default '',
  company_id    text,
  workspace_id  text,
  evidence_refs_json text not null default '[]',
  next_check_at text,
  context_json  text not null default '{}'
);
create index if not exists idx_rtl_entity on runtime_transition_log(tenant_id, entity_type, entity_id);
create index if not exists idx_rtl_at on runtime_transition_log(tenant_id, at);
"""


class SQLiteTransitionRecorder(TransitionRecorder):
    """基于 SQLite 的流转留痕接收方。"""

    def __init__(self, database: Database) -> None:
        self._db = database

    def ensure_schema(self) -> None:
        with self._db.connect() as conn:
            conn.executescript(_SCHEMA)
            columns = {row["name"] for row in conn.execute("pragma table_info(runtime_transition_log)")}
            for name, definition in (
                ("company_id", "text"),
                ("workspace_id", "text"),
                ("evidence_refs_json", "text not null default '[]'"),
                ("next_check_at", "text"),
            ):
                if name not in columns:
                    conn.execute(f"alter table runtime_transition_log add column {name} {definition}")

    def record(self, record: TransitionRecord) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into runtime_transition_log
                  (tenant_id, entity_type, entity_id, source, target,
                  trigger, actor, at, reason, company_id, workspace_id,
                  evidence_refs_json, next_check_at, context_json)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    TenantContext.current_tenant_id(),
                    record.entity_type,
                    record.entity_id,
                    record.source,
                    record.target,
                    record.trigger,
                    record.actor,
                    record.at,
                    record.reason,
                    record.context.get("companyId"),
                    record.context.get("workspaceId"),
                    json.dumps(record.context.get("evidenceRefs", []), ensure_ascii=False),
                    record.context.get("nextCheckAt"),
                    json.dumps(record.context, ensure_ascii=False),
                ),
            )

    def history(self, entity_type: str, entity_id: str) -> list[dict[str, Any]]:
        """按时间顺序返回某实体的全部流转留痕（审计 / 前端时间线）。"""
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                select source, target, trigger, actor, at, reason, company_id,
                       workspace_id, evidence_refs_json, next_check_at, context_json
                from runtime_transition_log
                where tenant_id = ? and entity_type = ? and entity_id = ?
                order by at asc, log_id asc
                """,
                (TenantContext.current_tenant_id(), entity_type, entity_id),
            ).fetchall()
        return [dict(row) for row in rows]


def init_transition_log(database: Database) -> SQLiteTransitionRecorder:
    """创建流转日志表并把 recorder 挂到全局注册表（A1 装配入口）。"""
    recorder = SQLiteTransitionRecorder(database)
    recorder.ensure_schema()
    runtime_registry.attach_recorder(recorder)
    return recorder
