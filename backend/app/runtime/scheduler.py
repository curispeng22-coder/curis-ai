"""Curis Business Runtime —— 持久化队列 + 调度 / 执行（A2）。

依据：``docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`` §6
（Cadence + ScheduledRun，7 态状态机，系统的心跳）。

本模块解决原型的两大缺口（§6.5）：
1. **没有真实定时器**：这里用「持久化的节奏表 + 到点扫描」取代手工点击。
   扫描是纯函数（给定 now 计算该触发谁），因此——
2. **重启不丢**：节奏与运行实例全部落库；进程重启后重新扫描即可，
   已排期的 QUEUED 实例不会因内存丢失而消失。这正是验收核心，
   直接否决「内存调度线程」方案。

设计要点
--------
- 状态流转一律走 :func:`app.runtime.get_machine("scheduled_run")`，不直写 status。
- 创建运行（QUEUED / RUNNING 入口）是 INSERT，不是流转，故不留痕；
  第一次流转（QUEUED→RUNNING 或 RUNNING→终态）起才开始留痕。
- 容量按业务隔离（capacityContract.maxConcurrent），v0.1 不实现跨业务抢占。
- 执行由可注入的 ``Executor`` 完成；A2 只给一个模拟执行器，真实执行引擎
  是后续阶段的职责。
"""

from __future__ import annotations

import json
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence
from contextlib import contextmanager

from ..database import Database
from .registry import runtime_registry
from .states import Actor, CadenceStatus, RunStatus, normalize
from .store import init_transition_log, SQLiteTransitionRecorder
from .events import BusinessEvent


# ---------------------------------------------------------------------------
# 持久化 schema（A2 专属；与 runtime_transition_log 同库）
# ---------------------------------------------------------------------------

RUNTIME_QUEUE_SCHEMA = """
create table if not exists cadences (
  cadence_id      text primary key,
  business_id     text not null,
  name            text not null,
  schedule_kind   text not null,
  schedule_text   text not null,
  owner_id        text not null default '',
  task            text not null default '',
  escalation_json text not null default '{}',
  max_concurrent  integer not null default 1,
  enabled         integer not null default 0,
  status          text not null,
  next_fire_at    text,
  created_at      text not null default current_timestamp,
  updated_at      text not null default current_timestamp
);

create table if not exists scheduled_runs (
  run_id          text primary key,
  cadence_id      text not null,
  business_id     text not null,
  title           text not null default '',
  owner_id        text not null default '',
  status          text not null,
  trigger         text not null default '',
  actor           text not null default '',
  escalation_reason text not null default '',
  cost            real not null default 0,
  attempt_count   integer not null default 0,
  last_error      text not null default '',
  scheduled_at    text,
  requested_at    text,
  queued_at       text,
  started_at      text,
  finished_at     text,
  created_at      text not null default current_timestamp,
  updated_at      text not null default current_timestamp
);
create index if not exists idx_runs_cadence on scheduled_runs(cadence_id, status);
create index if not exists idx_runs_biz_status on scheduled_runs(business_id, status);
"""


# ---------------------------------------------------------------------------
# 时间工具
# ---------------------------------------------------------------------------


def _utcnow_dt() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# 调度表达式（最小 cron：daily HH:MM / weekly <dow> HH:MM）
# ---------------------------------------------------------------------------


def parse_schedule(text: str) -> tuple[str, int, int, int | None]:
    """解析自由文本调度为 ``(kind, hour, minute, dow_or_None)``。"""
    parts = text.strip().split()
    if not parts:
        raise ValueError(f"空调度表达式：{text!r}")
    kind = parts[0].lower()
    if kind == "daily":
        hh, mm = _split_hhmm(parts[1])
        return ("DAILY", hh, mm, None)
    if kind == "weekly":
        dow = int(parts[1])
        hh, mm = _split_hhmm(parts[2])
        return ("WEEKLY", hh, mm, dow)
    raise ValueError(f"不支持的调度类型：{text!r}（A2 仅支持 daily / weekly）")


def _split_hhmm(token: str) -> tuple[int, int]:
    hh, mm = token.split(":")
    return int(hh), int(mm)


def next_fire(spec: tuple[str, int, int, int | None], now: datetime) -> datetime:
    """返回严格晚于 now 的下一个触发时刻（UTC 感知）。"""
    kind, hh, mm, dow = spec
    cand = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if kind == "DAILY":
        while cand <= now:
            cand += timedelta(days=1)
        return cand
    # WEEKLY
    while cand <= now or cand.weekday() != dow:
        cand += timedelta(days=1)
    return cand


# ---------------------------------------------------------------------------
# 执行契约
# ---------------------------------------------------------------------------


@dataclass
class ExecutionResult:
    escalated: bool = False
    reason: str = ""
    output: str = ""
    cost: float = 0.0
    error: str = ""


class Executor(Protocol):
    def execute(self, cadence: Mapping[str, Any], run: Mapping[str, Any]) -> ExecutionResult:
        """执行一次运行。返回结果：升级 / 完成 / 异常。"""
        ...


class SimulatedExecutor:
    """A2 默认模拟执行器。

    ``escalate_when(cadence)`` 命中则返回升级；否则视为执行成功。
    真实执行引擎是后续阶段职责，这里只把「是否升级」的决策点暴露出来。
    """

    def __init__(self, escalate_when: Callable[[Mapping[str, Any]], bool] | None = None) -> None:
        self.escalate_when = escalate_when

    def execute(self, cadence: Mapping[str, Any], run: Mapping[str, Any]) -> ExecutionResult:
        if self.escalate_when and self.escalate_when(cadence):
            esc = cadence.get("escalation") or {}
            return ExecutionResult(escalated=True, reason=esc.get("reason", "需要 CEO 拍板"))
        return ExecutionResult(escalated=False, output="simulated-ok", cost=0.0)


# ---------------------------------------------------------------------------
# 调度器 / 执行器（持久化队列）
# ---------------------------------------------------------------------------


class RuntimeScheduler:
    """基于 SQLite 的节奏调度与运行执行。

    典型用法::

        sched = RuntimeScheduler(db, SimulatedExecutor(escalate_when=...))
        cid = sched.create_cadence(biz, "小红书·每日研究", "daily 08:00", ...)
        sched.enable_cadence(cid, next_fire_at="2026-07-29T08:00:00")  # 或在 enable 时自动算
        sched.run_once()          # 单轮：扫描到点节奏 + 推进队列
        # 或常驻：sched.start(interval_sec=30) ... sched.stop()
    """

    def __init__(
        self,
        database: Database,
        executor: Executor | None = None,
        event_bus: Any | None = None,
    ) -> None:
        self._db = database
        self._executor: Executor = executor or SimulatedExecutor()
        self._event_bus = event_bus
        self._machine = runtime_registry.get("scheduled_run")
        self._cadence_machine = runtime_registry.get("cadence")
        self._recorder: SQLiteTransitionRecorder = init_transition_log(database)
        self._ensure_queue_schema()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    # -- schema --------------------------------------------------------------

    def _ensure_queue_schema(self) -> None:
        with self._db.connect() as conn:
            conn.executescript(RUNTIME_QUEUE_SCHEMA)

    # -- 节奏 CRUD -----------------------------------------------------------

    def create_cadence(
        self,
        business_id: str,
        name: str,
        schedule_text: str,
        *,
        owner_id: str = "",
        task: str = "",
        escalation: Mapping[str, Any] | None = None,
        max_concurrent: int = 1,
    ) -> str:
        cid = uuid.uuid4().hex
        spec = parse_schedule(schedule_text)
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into cadences
                  (cadence_id, business_id, name, schedule_kind, schedule_text,
                   owner_id, task, escalation_json, max_concurrent, enabled, status)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """,
                (
                    cid, business_id, name, spec[0], schedule_text,
                    owner_id, task, _json(escalation or {}),
                    max_concurrent, CadenceStatus.DRAFT.value,
                ),
            )
        return cid

    def enable_cadence(self, cadence_id: str, next_fire_at: str | None = None,
                       now: datetime | None = None) -> None:
        now = now or _utcnow_dt()
        cad = self._get_cadence(cadence_id)
        self._cadence_machine.transition(
            cadence_id, cad["status"], CadenceStatus.ENABLED.value,
            actor=Actor.CEO, trigger="enable",
        )
        if next_fire_at is None:
            spec = parse_schedule(cad["schedule_text"])
            next_fire_at = _iso(next_fire(spec, now))
        with self._db.connect() as conn:
            conn.execute(
                "update cadences set enabled = 1, status = ?, next_fire_at = ?, "
                "updated_at = current_timestamp where cadence_id = ?",
                (CadenceStatus.ENABLED.value, next_fire_at, cadence_id),
            )

    def retire_cadence(self, cadence_id: str) -> None:
        cad = self._get_cadence(cadence_id)
        self._cadence_machine.transition(
            cadence_id, cad["status"], CadenceStatus.RETIRED.value,
            actor=Actor.CEO, trigger="retire",
        )
        with self._db.connect() as conn:
            conn.execute(
                "update cadences set enabled = 0, status = ? "
                "where cadence_id = ?",
                (CadenceStatus.RETIRED.value, cadence_id),
            )

    # -- 调度主循环 ----------------------------------------------------------

    def run_once(self, now: datetime | None = None) -> list[str]:
        """一轮工作：扫描到点节奏并推进队列。返回本轮生成的运行实例 id。"""
        now = now or _utcnow_dt()
        spawned = self.tick(now)
        self.process_queue(now)
        return spawned

    def tick(self, now: datetime | None = None) -> list[str]:
        """扫描到点的 ENABLED 节奏，生成运行实例并推进 next_fire_at。"""
        now = now or _utcnow_dt()
        now_iso = _iso(now)
        spawned: list[str] = []
        for cad in self._due_cadences(now_iso):
            run_id = self._spawn_run(cad, now)
            spawned.append(run_id)
            spec = parse_schedule(cad["schedule_text"])
            with self._db.connect() as conn:
                conn.execute(
                    "update cadences set next_fire_at = ? where cadence_id = ?",
                    (_iso(next_fire(spec, now)), cad["cadence_id"]),
                )
        return spawned

    def process_queue(self, now: datetime | None = None) -> None:
        """按容量把 QUEUED 提升为 RUNNING 并执行所有 RUNNING。

        单轮内反复「提升 + 执行」，直到一轮毫无进展——这样前序运行释放容量后，
        被挡在 QUEUED 的实例会在同一轮被自动提升并接着执行。
        """
        now = now or _utcnow_dt()
        while True:
            progressed = False
            for run in self._queued_runs():
                if self._running_count(run["business_id"]) < self._max_concurrent(run["cadence_id"]):
                    self._promote(run, now)
                    progressed = True
                    break
            for run in self._running_runs():
                self._execute_run(run["run_id"], now)
                progressed = True
            if not progressed:
                break

    # -- 人工介入（升级闭环）-------------------------------------------------

    def ceo_open(self, run_id: str) -> None:
        run = self._get_run(run_id)
        self._transition_run(run, RunStatus.WAITING_CEO, RunStatus.ACKNOWLEDGED,
                             actor=Actor.CEO, trigger="ceo_opened")

    def ceo_resolve(self, run_id: str, *, reason: str = "") -> None:
        run = self._get_run(run_id)
        src = RunStatus(run["status"])
        # ACKNOWLEDGED（已打开）或 FAILED 都可经 CEO 处置收结。
        # WAITING_CEO 必须先 ceo_open 才能收结（不可跨态直结）。
        if src not in (RunStatus.ACKNOWLEDGED, RunStatus.FAILED):
            raise ValueError(f"run {run_id} 当前 {src.value}，不可由 CEO 直接收结")
        self._transition_run(run, src, RunStatus.RESOLVED,
                             actor=Actor.CEO, trigger="ceo_resolved", reason=reason)

    # -- 后台常驻 ------------------------------------------------------------

    def start(self, interval_sec: float = 30.0) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()

        def _loop() -> None:
            while not self._stop.wait(interval_sec):
                try:
                    self.run_once()
                except Exception:  # 单轮异常不应杀死常驻线程
                    continue

        self._thread = threading.Thread(target=_loop, name="curis-scheduler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self._thread = None

    # -- 内部：生成与执行 ----------------------------------------------------

    def _spawn_run(self, cad: Mapping[str, Any], now: datetime) -> str:
        now_iso = _iso(now)
        running = self._running_count(cad["business_id"])
        if running < cad["max_concurrent"]:
            status = RunStatus.RUNNING
            started_at = now_iso
            queued_at = None
        else:
            status = RunStatus.QUEUED
            started_at = None
            queued_at = now_iso
        run_id = uuid.uuid4().hex
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into scheduled_runs
                  (run_id, cadence_id, business_id, title, owner_id, status,
                   actor, scheduled_at, requested_at, queued_at, started_at)
                values (?, ?, ?, ?, ?, ?, 'SYSTEM', ?, ?, ?, ?)
                """,
                (
                    run_id, cad["cadence_id"], cad["business_id"], cad["name"],
                    cad["owner_id"], status.value, now_iso, now_iso, queued_at, started_at,
                ),
            )
        return run_id

    def _promote(self, run: Mapping[str, Any], now: datetime) -> None:
        self._transition_run(run, RunStatus.QUEUED, RunStatus.RUNNING,
                             actor=Actor.SYSTEM, trigger="capacity_released")
        with self._db.connect() as conn:
            conn.execute(
                "update scheduled_runs set started_at = ?, queued_at = null "
                "where run_id = ?",
                (_iso(now), run["run_id"]),
            )

    def _execute_run(self, run_id: str, now: datetime) -> None:
        run = self._get_run(run_id)
        cad = self._get_cadence(run["cadence_id"])
        try:
            result = self._executor.execute(cad, run)
        except Exception as exc:  # 执行器抛错视为运行异常
            result = ExecutionResult(error=str(exc))
        target: RunStatus
        reason = ""
        if result.error:
            target = RunStatus.FAILED
            reason = result.error
        elif result.escalated:
            target = RunStatus.WAITING_CEO
            reason = result.reason
        else:
            target = RunStatus.COMPLETED
        self._transition_run(run, RunStatus.RUNNING, target,
                             actor=Actor.SYSTEM,
                             trigger="execution_finished" if target is RunStatus.COMPLETED
                             else "escalation_hit" if target is RunStatus.WAITING_CEO
                             else "execution_error",
                             reason=reason)
        with self._db.connect() as conn:
            conn.execute(
                """
                update scheduled_runs
                  set finished_at = ?, cost = ?, escalation_reason = ?,
                      last_error = ?, attempt_count = attempt_count + 1,
                      updated_at = current_timestamp
                where run_id = ?
                """,
                (_iso(now), result.cost, reason if target is RunStatus.WAITING_CEO else "",
                 result.error, run_id),
            )

    def _transition_run(self, run: Mapping[str, Any], src: RunStatus, dst: RunStatus,
                        *, actor: Actor, trigger: str, reason: str = "") -> None:
        rec = self._machine.transition(
            run["run_id"], src.value, dst.value,
            actor=actor, trigger=trigger, reason=reason,
        )
        with self._db.connect() as conn:
            conn.execute(
                "update scheduled_runs set status = ?, updated_at = current_timestamp "
                "where run_id = ?",
                (rec.target, run["run_id"]),
            )
        # A3：发布领域事件，解耦通知 / 经营账 / 归因等订阅方
        if self._event_bus is not None:
            self._event_bus.publish(BusinessEvent(
                type="run_state_changed", entity_type="scheduled_run",
                entity_id=run["run_id"],
                payload={"source": src.value, "target": rec.target,
                         "trigger": trigger, "actor": actor.value},
                at=rec.at,
            ))
            if dst is RunStatus.WAITING_CEO:
                self._event_bus.publish(BusinessEvent(
                    type="escalation_raised", entity_type="scheduled_run",
                    entity_id=run["run_id"],
                    payload={"reason": reason, "business_id": run["business_id"]},
                    at=rec.at,
                ))

    # -- 内部：查询 ----------------------------------------------------------

    def _due_cadences(self, now_iso: str) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                select * from cadences
                where enabled = 1 and status = ?
                  and next_fire_at is not null and next_fire_at <= ?
                order by next_fire_at asc
                """,
                (CadenceStatus.ENABLED.value, now_iso),
            ).fetchall()
        return [dict(r) for r in rows]

    def _queued_runs(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute(
                "select * from scheduled_runs where status = ? "
                "order by scheduled_at asc, run_id asc",
                (RunStatus.QUEUED.value,),
            ).fetchall()
        return [dict(r) for r in rows]

    def _running_runs(self) -> list[dict[str, Any]]:
        with self._db.connect() as conn:
            rows = conn.execute(
                "select * from scheduled_runs where status = ?",
                (RunStatus.RUNNING.value,),
            ).fetchall()
        return [dict(r) for r in rows]

    def _running_count(self, business_id: str) -> int:
        with self._db.connect() as conn:
            row = conn.execute(
                "select count(*) as c from scheduled_runs "
                "where business_id = ? and status = ?",
                (business_id, RunStatus.RUNNING.value),
            ).fetchone()
        return int(row["c"])

    def _max_concurrent(self, cadence_id: str) -> int:
        cad = self._get_cadence(cadence_id)
        return int(cad["max_concurrent"]) or 1

    def _get_run(self, run_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from scheduled_runs where run_id = ?", (run_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"运行不存在：{run_id}")
        return dict(row)

    def _get_cadence(self, cadence_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from cadences where cadence_id = ?", (cadence_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"节奏不存在：{cadence_id}")
        d = dict(row)
        d["escalation"] = _parse_json(d.get("escalation_json") or "{}")
        return d

    # -- 查询 / 审计 ---------------------------------------------------------

    def list_runs(self, cadence_id: str | None = None,
                  status: str | None = None) -> list[dict[str, Any]]:
        sql = "select * from scheduled_runs"
        clauses: list[str] = []
        params: list[str] = []
        if cadence_id is not None:
            clauses.append("cadence_id = ?")
            params.append(cadence_id)
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        if clauses:
            sql += " where " + " and ".join(clauses)
        sql += " order by scheduled_at asc, run_id asc"
        with self._db.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def history(self, run_id: str) -> list[dict[str, Any]]:
        """该运行的全流转留痕（审计 / 前端时间线）。"""
        return self._recorder.history("scheduled_run", run_id)


# ---------------------------------------------------------------------------
# JSON 辅助
# ---------------------------------------------------------------------------


def _json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return {}
