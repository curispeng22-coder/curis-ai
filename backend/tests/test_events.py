"""Curis Business Runtime —— A3 事件总线验收。

验证：状态流转会发布 ``run_state_changed``；运行进入 WAITING_CEO 时额外发布
``escalation_raised``（驱动 CEO 桌面通知）。订阅方与状态机解耦。
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.database import Database
from app.runtime.events import BusinessEvent, EventBus
from app.runtime.scheduler import RuntimeScheduler, SimulatedExecutor, _iso
from app.runtime.states import RunStatus


def _temp_db() -> Database:
    d = tempfile.mkdtemp()
    return Database(Path(d) / "curis_evt.sqlite")


def _past() -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=1)


def _needs_ceo(cad: dict) -> bool:
    return "ON_MISSING_AUTH" in (cad.get("escalation") or {}).get("triggers", [])


def test_escalation_publishes_events():
    bus = EventBus()
    received: list[BusinessEvent] = []
    bus.subscribe("escalation_raised", received.append)
    bus.subscribe("run_state_changed", received.append)

    db = _temp_db()
    sched = RuntimeScheduler(
        db, SimulatedExecutor(escalate_when=_needs_ceo), event_bus=bus
    )
    cid = sched.create_cadence(
        "biz-y", "抖音·数据回流", "daily 18:00",
        escalation={"triggers": ["ON_MISSING_AUTH"], "reason": "无授权，请补录", "timeoutHours": 4},
    )
    sched.enable_cadence(cid, next_fire_at=_iso(_past()))

    sched.run_once(datetime.now(timezone.utc))

    types = [e.type for e in received]
    assert "escalation_raised" in types
    esc = [e for e in received if e.type == "escalation_raised"][0]
    assert esc.payload["reason"] == "无授权，请补录"
    assert esc.entity_type == "scheduled_run"
    # run_state_changed 至少包含本次 RUNNING → WAITING_CEO
    assert any(
        e.type == "run_state_changed"
        and e.payload.get("source") == RunStatus.RUNNING.value
        and e.payload.get("target") == RunStatus.WAITING_CEO.value
        for e in received
    )
