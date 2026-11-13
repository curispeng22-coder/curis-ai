"""Curis Business Runtime —— 状态机引擎 + 注册表 + 流转留痕 单测（A1）。

覆盖 A1 的核心契约：
- 状态值集中、别名归一、未知值抛错；
- 非法流转被拒（含 RUNNING→RESOLVED 硬要求）；
- 守卫门禁生效（授权门禁、验证结论门禁、三级门禁）；
- 声明式自环（ACTIVE→ACTIVE cycle+1）合法；
- 终态不可再流转；
- 流转留痕写入 SQLite 且可按实体回溯。
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from app.database import Database
from app.runtime import Actor, get_machine, init_transition_log, runtime_registry
from app.runtime.state_machine import (
    ActorNotAllowedError,
    GuardRejectedError,
    IllegalTransitionError,
    TerminalStateError,
)
from app.runtime.states import (
    BusinessLifecycle,
    CommitmentStatus,
    RunStatus,
    UnknownStateError,
    WorkspaceStatus,
    normalize,
)


def _temp_db() -> Database:
    d = tempfile.mkdtemp()
    return Database(Path(d) / "curis_test.sqlite")


# ---- 1. 枚举与归一 ----------------------------------------------------------


def test_normalize_accepts_enum_member():
    assert normalize(RunStatus, RunStatus.RUNNING) is RunStatus.RUNNING


def test_normalize_alias_succeeded_maps_to_completed():
    # 修复历史缺陷：代码写 succeeded、约束写 completed，归一为 COMPLETED
    assert normalize(RunStatus, "succeeded").value == "COMPLETED"
    assert normalize(RunStatus, "completed").value == "COMPLETED"
    assert normalize(RunStatus, "done").value == "COMPLETED"


def test_normalize_unknown_raises():
    try:
        normalize(RunStatus, "watermelon")
        assert False, "未知状态应抛 UnknownStateError"
    except UnknownStateError:
        pass


# ---- 2. 非法流转被拒 --------------------------------------------------------


def test_run_running_to_resolved_is_illegal():
    m = get_machine("scheduled_run")
    try:
        m.transition("run-1", RunStatus.RUNNING, RunStatus.RESOLVED,
                     actor=Actor.CEO, trigger="x")
        assert False, "RUNNING→RESOLVED 必须被拒绝"
    except IllegalTransitionError:
        pass


def test_run_queued_to_running_ok():
    m = get_machine("scheduled_run")
    rec = m.transition("run-1", RunStatus.QUEUED, RunStatus.RUNNING,
                       actor=Actor.SYSTEM, trigger="capacity_released")
    assert rec.target == "RUNNING"


def test_actor_not_allowed():
    m = get_machine("scheduled_run")
    try:
        m.transition("run-2", RunStatus.WAITING_CEO, RunStatus.ACKNOWLEDGED,
                     actor=Actor.SYSTEM, trigger="ceo_opened")
        assert False, "SYSTEM 无权执行 ceo_opened"
    except ActorNotAllowedError:
        pass


# ---- 3. 守卫门禁 ------------------------------------------------------------


def test_business_direction_requires_authorization():
    m = get_machine("business_direction")
    try:
        m.transition("biz-1", BusinessLifecycle.PENDING_APPROVAL,
                     BusinessLifecycle.ACTIVE, actor=Actor.CEO,
                     trigger="approve_team", context={"authorized": False})
        assert False, "未授权必须被守卫拒绝"
    except GuardRejectedError:
        pass
    rec = m.transition("biz-1", BusinessLifecycle.PENDING_APPROVAL,
                       BusinessLifecycle.ACTIVE, actor=Actor.CEO,
                       trigger="approve_team", context={"authorized": True})
    assert rec.target == "ACTIVE"


def test_scaling_requires_verified():
    m = get_machine("business_direction")
    m.transition("biz-2", BusinessLifecycle.DRAFT,
                 BusinessLifecycle.PENDING_APPROVAL, actor=Actor.CEO,
                 trigger="brief_complete")
    m.transition("biz-2", BusinessLifecycle.PENDING_APPROVAL,
                 BusinessLifecycle.ACTIVE, actor=Actor.CEO,
                 trigger="approve_team", context={"authorized": True})
    try:
        m.transition("biz-2", BusinessLifecycle.ACTIVE,
                     BusinessLifecycle.SCALING, actor=Actor.CEO,
                     trigger="scale_up", context={"verificationStatus": "UNVERIFIED"})
        assert False, "非 VERIFIED 不得扩大"
    except GuardRejectedError:
        pass


def test_workspace_three_gate():
    m = get_machine("workspace")
    m.transition("ws-1", WorkspaceStatus.DRAFT, WorkspaceStatus.BLUEPRINTING,
                 actor=Actor.CEO, trigger="start_blueprint")
    m.transition("ws-1", WorkspaceStatus.BLUEPRINTING, WorkspaceStatus.SIMULATED,
                 actor=Actor.CEO, trigger="simulation_passed",
                 context={"simulationPassed": True})
    try:
        m.transition("ws-1", WorkspaceStatus.SIMULATED, WorkspaceStatus.PENDING_APPROVAL,
                     actor=Actor.CEO, trigger="submit_for_approval",
                     context={"issuesResolved": False, "simulationPassed": True,
                               "externalAgentReviewed": True})
        assert False, "三级门禁未过必须拒绝"
    except GuardRejectedError:
        pass
    rec = m.transition("ws-1", WorkspaceStatus.SIMULATED, WorkspaceStatus.PENDING_APPROVAL,
                       actor=Actor.CEO, trigger="submit_for_approval",
                       context={"issuesResolved": True, "simulationPassed": True,
                                 "externalAgentReviewed": True})
    assert rec.target == "PENDING_APPROVAL"


# ---- 4. 声明式自环（cycle+1）----------------------------------------------


def test_business_direction_self_loop_allowed():
    m = get_machine("business_direction")
    m.transition("biz-3", BusinessLifecycle.DRAFT,
                 BusinessLifecycle.PENDING_APPROVAL, actor=Actor.CEO,
                 trigger="brief_complete")
    m.transition("biz-3", BusinessLifecycle.PENDING_APPROVAL,
                 BusinessLifecycle.ACTIVE, actor=Actor.CEO,
                 trigger="approve_team", context={"authorized": True})
    rec = m.transition("biz-3", BusinessLifecycle.ACTIVE,
                       BusinessLifecycle.ACTIVE, actor=Actor.CEO,
                       trigger="continue_cycle", reason="进入下一责任周期")
    assert rec.source == "ACTIVE" and rec.target == "ACTIVE"
    assert rec.reason == "进入下一责任周期"


# ---- 5. 终态不可再流转 ------------------------------------------------------


def test_terminal_state_blocks_further_transition():
    m = get_machine("business_direction")
    m.transition("biz-4", BusinessLifecycle.DRAFT, BusinessLifecycle.ARCHIVED,
                 actor=Actor.CEO, trigger="close")
    try:
        m.transition("biz-4", BusinessLifecycle.ARCHIVED,
                     BusinessLifecycle.DRAFT, actor=Actor.CEO, trigger="close")
        assert False, "终态 ARCHIVED 不可再流转"
    except TerminalStateError:
        pass


# ---- 6. 流转留痕持久化 ------------------------------------------------------


def test_recorder_writes_and_history_reads_back():
    db = _temp_db()
    from app.runtime.store import SQLiteTransitionRecorder

    recorder = SQLiteTransitionRecorder(db)
    recorder.ensure_schema()
    m = get_machine("scheduled_run")
    m.recorder = recorder  # 仅本机局部挂接，避免污染其它测试

    m.transition("run-rec-1", RunStatus.QUEUED, RunStatus.RUNNING,
                 actor=Actor.SYSTEM, trigger="capacity_released", reason="容量释放")
    rows = recorder.history("scheduled_run", "run-rec-1")
    assert len(rows) == 1
    assert rows[0]["source"] == "QUEUED"
    assert rows[0]["target"] == "RUNNING"
    assert rows[0]["actor"] == "SYSTEM"

    m.transition("run-rec-1", RunStatus.RUNNING, RunStatus.WAITING_CEO,
                 actor=Actor.SYSTEM, trigger="escalation_hit",
                 context={"escalation": "ON_MISSING_AUTH"})
    rows = recorder.history("scheduled_run", "run-rec-1")
    assert len(rows) == 2
    assert json.loads(rows[1]["context_json"])["escalation"] == "ON_MISSING_AUTH"


def test_init_transition_log_attaches_to_all():
    db = _temp_db()
    recorder = init_transition_log(db)
    for m in runtime_registry.all():
        assert m.recorder is recorder
    # 还原为无 recorder，避免污染其它测试模块
    runtime_registry.attach_recorder(None)


# ---- 7. 注册表装配完整 ------------------------------------------------------


def test_registry_has_five_machines():
    types = {m.entity_type for m in runtime_registry.all()}
    assert types == {
        "business_direction", "commitment", "workspace",
        "cadence", "scheduled_run",
    }


def test_unregistered_entity_raises():
    import pytest

    with pytest.raises(KeyError):
        get_machine("not_a_real_entity")
