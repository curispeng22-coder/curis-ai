"""Curis Business Runtime —— A2 调度 / 持久化队列 验收。

对应定义文档 §6.6 的四条硬验收：
- 到点自动产生 RUNNING 实例，无需手工操作；
- 命中升级声明 → WAITING_CEO，CEO 处理后收结；
- 重启进程后 QUEUED 实例不丢失，仍被推进；
- 并发打满 → 新实例进 QUEUED，前序完成后自动提升。
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.database import Database
from app.runtime.scheduler import (
    ExecutionResult,
    RuntimeScheduler,
    SimulatedExecutor,
    _iso,
)
from app.runtime.states import CadenceStatus, RunStatus


def _temp_db() -> Database:
    d = tempfile.mkdtemp()
    return Database(Path(d) / "curis_sched.sqlite")


def _past() -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=1)


def _needs_ceo(cad: dict) -> bool:
    return "ON_MISSING_AUTH" in (cad.get("escalation") or {}).get("triggers", [])


# ---- 1. 到点自动产生 RUNNING → COMPLETED，无手工操作 -----------------------


def test_auto_fire_daily_no_manual_op():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    cid = sched.create_cadence("biz-x", "小红书·每日研究", "daily 08:00",
                               escalation={"triggers": [], "reason": ""})
    sched.enable_cadence(cid, next_fire_at=_iso(_past()))

    now = datetime.now(timezone.utc)
    spawned = sched.run_once(now)

    assert len(spawned) == 1
    runs = sched.list_runs()
    assert len(runs) == 1
    assert runs[0]["status"] == RunStatus.COMPLETED.value
    # 证明其经历过 RUNNING：留痕里有 RUNNING → COMPLETED
    hist = sched.history(runs[0]["run_id"])
    transitions = [(h["source"], h["target"]) for h in hist]
    assert (RunStatus.RUNNING.value, RunStatus.COMPLETED.value) in transitions


def test_future_cadence_not_fired():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    cid = sched.create_cadence("biz-x", "future", "daily 08:00")
    future = _iso(datetime.now(timezone.utc) + timedelta(hours=3))
    sched.enable_cadence(cid, next_fire_at=future)

    assert sched.run_once(datetime.now(timezone.utc)) == []
    assert sched.list_runs() == []


# ---- 2. 升级 → CEO 闭环 ----------------------------------------------------


def test_escalation_then_ceo_loop():
    db = _temp_db()
    sched = RuntimeScheduler(
        db, SimulatedExecutor(escalate_when=_needs_ceo)
    )
    cid = sched.create_cadence(
        "biz-y", "抖音·数据回流", "daily 18:00",
        escalation={"triggers": ["ON_MISSING_AUTH"], "reason": "无授权，请补录", "timeoutHours": 4},
    )
    sched.enable_cadence(cid, next_fire_at=_iso(_past()))

    sched.run_once(datetime.now(timezone.utc))
    runs = sched.list_runs()
    assert len(runs) == 1
    assert runs[0]["status"] == RunStatus.WAITING_CEO.value
    assert "无授权" in runs[0]["escalation_reason"]

    # CEO 打开 → 处置 → 收结
    sched.ceo_open(runs[0]["run_id"])
    assert sched.list_runs(status=RunStatus.ACKNOWLEDGED.value)[0]["run_id"] == runs[0]["run_id"]
    sched.ceo_resolve(runs[0]["run_id"], reason="已手动补录")
    assert sched.list_runs(status=RunStatus.RESOLVED.value)[0]["run_id"] == runs[0]["run_id"]

    hist = sched.history(runs[0]["run_id"])
    transitions = [(h["source"], h["target"], h["actor"]) for h in hist]
    assert (RunStatus.RUNNING.value, RunStatus.WAITING_CEO.value, "SYSTEM") in transitions
    assert (RunStatus.WAITING_CEO.value, RunStatus.ACKNOWLEDGED.value, "CEO") in transitions
    assert (RunStatus.ACKNOWLEDGED.value, RunStatus.RESOLVED.value, "CEO") in transitions


def test_ceo_resolve_rejects_non_waiting():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    cid = sched.create_cadence("biz-z", "will-run", "daily 08:00")
    sched.enable_cadence(cid, next_fire_at=_iso(_past()))
    sched.tick(datetime.now(timezone.utc))  # 只生成，不执行 → 留下 RUNNING
    run = sched.list_runs(status=RunStatus.RUNNING.value)[0]
    try:
        sched.ceo_resolve(run["run_id"])
        assert False, "RUNNING 不可由 CEO 直接收结"
    except ValueError:
        pass


# ---- 3. 重启后 QUEUED 不丢失 -----------------------------------------------


def test_restart_preserves_queued_run():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    cid = sched.create_cadence("biz-q", "persisted", "daily 09:00", max_concurrent=1)
    sched.enable_cadence(cid)

    # 模拟「重启前」已落库、仍 QUEUED 的运行实例
    rid = "queued-before-restart"
    now_iso = _iso(datetime.now(timezone.utc))
    with db.connect() as conn:
        conn.execute(
            """
            insert into scheduled_runs
              (run_id, cadence_id, business_id, title, status, actor,
               scheduled_at, requested_at, queued_at)
            values (?, ?, ?, ?, ?, 'SYSTEM', ?, ?, ?)
            """,
            (rid, cid, "biz-q", "persisted", RunStatus.QUEUED.value,
             now_iso, now_iso, now_iso),
        )

    # 进程重启：全新的调度器实例，同一库
    sched2 = RuntimeScheduler(db)
    sched2.run_once(datetime.now(timezone.utc))

    completed = sched2.list_runs(status=RunStatus.COMPLETED.value)
    assert len(completed) == 1
    assert completed[0]["run_id"] == rid


# ---- 4. 并发打满 → QUEUED → 自动提升 ----------------------------


def test_capacity_gating_then_promote():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    c1 = sched.create_cadence("biz-c", "a", "daily 08:00", max_concurrent=1)
    c2 = sched.create_cadence("biz-c", "b", "daily 08:00", max_concurrent=1)
    sched.enable_cadence(c1, next_fire_at=_iso(_past()))
    sched.enable_cadence(c2, next_fire_at=_iso(_past()))

    sched.run_once(datetime.now(timezone.utc))

    runs = sched.list_runs()
    assert len(runs) == 2
    # 全部最终完成（第二个在第一个释放容量后被提升）
    assert all(r["status"] == RunStatus.COMPLETED.value for r in runs)


# ---- 5. 节奏状态机装配 ------------------------------------------------------


def test_cadence_lifecycle():
    db = _temp_db()
    sched = RuntimeScheduler(db)
    cid = sched.create_cadence("biz-l", "life", "daily 08:00")
    assert sched._get_cadence(cid)["status"] == CadenceStatus.DRAFT.value
    sched.enable_cadence(cid, next_fire_at=_iso(_past()))
    assert sched._get_cadence(cid)["status"] == CadenceStatus.ENABLED.value
    sched.retire_cadence(cid)
    assert sched._get_cadence(cid)["status"] == CadenceStatus.RETIRED.value
