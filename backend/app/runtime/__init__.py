"""Curis Business Runtime —— 包入口。

对外暴露：
- runtime_registry：5 个核心对象的状态机注册表（导入即装配）
- get_machine(entity_type)：按 entity_type 取状态机
- SQLiteTransitionRecorder / init_transition_log：流转留痕持久化
- 常用枚举与工具（normalize / check_constraint / labels_of）

设计铁律（A1 契约）：
- 状态值只来自本包 states 模块；
- 流转只走 StateMachine.transition，禁止直接 UPDATE status；
- 非法流转被拒并报错，不静默写入；
- 每次成功流转经 recorder 留痕。
"""

from __future__ import annotations

from .registry import get_registered_machine, runtime_registry
from .state_machine import (
    StateMachine,
    StateMachineRegistry,
    Transition,
    TransitionRecord,
    TransitionRecorder,
)
from .states import (
    Actor,
    AllocationStatus,
    BusinessLifecycle,
    CadenceStatus,
    CommitmentStatus,
    CurisState,
    EvidenceAdoption,
    EvidenceGrade,
    ExceptionStatus,
    EscalationTrigger,
    HumanGate,
    NON_SILENT_TRIGGERS,
    RunStatus,
    StageSlot,
    WorkItemStatus,
    WorkspaceStatus,
    check_constraint,
    labels_of,
    normalize,
)
from .store import SQLiteTransitionRecorder, init_transition_log
from .foundation import RuntimeFoundation, RuntimeScopeError
from .legacy_execution_adapter import LegacyExecutionAdapter
from .simulation import SimulationRuntime
from .responsibility_routing import ResponsibilityRoutingError, ResponsibilityRoutingRuntime
from .autonomous_operating import AutonomousControlError, AutonomousOperatingControl


def get_machine(entity_type: str) -> StateMachine:
    """按 entity_type 取状态机（全局唯一实例）。"""
    return get_registered_machine(entity_type)


__all__ = [
    "runtime_registry",
    "get_machine",
    "StateMachine",
    "StateMachineRegistry",
    "Transition",
    "TransitionRecord",
    "TransitionRecorder",
    "SQLiteTransitionRecorder",
    "init_transition_log",
    "Actor",
    "AllocationStatus",
    "BusinessLifecycle",
    "CadenceStatus",
    "CommitmentStatus",
    "CurisState",
    "EvidenceAdoption",
    "EvidenceGrade",
    "ExceptionStatus",
    "EscalationTrigger",
    "HumanGate",
    "NON_SILENT_TRIGGERS",
    "RunStatus",
    "StageSlot",
    "WorkItemStatus",
    "WorkspaceStatus",
    "check_constraint",
    "labels_of",
    "normalize",
    "RuntimeFoundation",
    "RuntimeScopeError",
    "LegacyExecutionAdapter",
    "SimulationRuntime",
    "ResponsibilityRoutingError",
    "ResponsibilityRoutingRuntime",
    "AutonomousControlError",
    "AutonomousOperatingControl",
]
