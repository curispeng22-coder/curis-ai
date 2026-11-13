"""Curis Business Runtime —— 5 个核心对象的状态机注册表。

依据：``docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`` 各对象流转表。

注册表在导入时即装配好，调用方按 ``entity_type`` 取用，避免各模块重复声明、
也避免同一对象在不同模块被声明成两套不同的流转规则。

entity_type 取值（全系统统一）：
    business_direction / commitment / workspace / cadence / scheduled_run

守卫（guard）约定：守卫只读取 ``context`` 中由编排层显式传入的业务条件
（如 ``authorized`` / ``verificationStatus`` / 三级门禁三件套），引擎本身不
感知业务字段——这样状态机保持纯逻辑、可单测。
"""

from __future__ import annotations

from .state_machine import StateMachine, StateMachineRegistry, Transition
from .states import (
    AcceptanceStatus,
    Actor,
    AIEmployeeStatus,
    BusinessLifecycle,
    CadenceStatus,
    CapabilityBindingStatus,
    CEOAssistantStatus,
    CommitmentStatus,
    ContentStatus,
    CycleStatus,
    DecisionPacketStatus,
    FoundingRunStatus,
    HandoffStatus,
    InteractionStatus,
    RunStatus,
    RoleSlotStatus,
    SimulationStatus,
    WorkspaceStatus,
)


foundation_registry = StateMachineRegistry()


def _build_registry() -> StateMachineRegistry:
    registry = StateMachineRegistry()

    # 1) BusinessDirection —— lifecycleStatus（维度一；维度二 verificationStatus
    #    复用 EvidenceGrade，由守卫在「扩大」时校验，不在此状态机内）。
    registry.register(
        StateMachine(
            entity_type="business_direction",
            states=BusinessLifecycle,
            initial=[BusinessLifecycle.DRAFT],
            terminal=[BusinessLifecycle.ARCHIVED],
            transitions=[
                Transition("DRAFT", "PENDING_APPROVAL", "brief_complete",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PENDING_APPROVAL", "ACTIVE", "approve_team",
                           actors=frozenset({Actor.CEO.value}),
                           guard=lambda c: None if c.get("authorized")
                           else "未勾选授权，启动被拒绝（硬门禁）"),
                Transition("ACTIVE", "ACTIVE", "continue_cycle",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACTIVE", "SCALING", "scale_up",
                           actors=frozenset({Actor.CEO.value}),
                           guard=lambda c: None if c.get("verificationStatus") == "VERIFIED"
                           else "验证结论非 VERIFIED，冻结扩大通道"),
                Transition("ACTIVE", "PAUSED", "pause_review",
                           actors=frozenset({Actor.CEO.value})),
                Transition("SCALING", "PAUSED", "pause_review",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "ACTIVE", "resume",
                           actors=frozenset({Actor.CEO.value})),
                Transition("DRAFT", "ARCHIVED", "close",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PENDING_APPROVAL", "ARCHIVED", "close",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACTIVE", "ARCHIVED", "close",
                           actors=frozenset({Actor.CEO.value})),
                Transition("SCALING", "ARCHIVED", "close",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "ARCHIVED", "close",
                           actors=frozenset({Actor.CEO.value})),
            ],
        )
    )

    # 2) Commitment
    registry.register(
        StateMachine(
            entity_type="commitment",
            states=CommitmentStatus,
            initial=[CommitmentStatus.PENDING],
            terminal=[CommitmentStatus.FULFILLED, CommitmentStatus.RELEASED],
            transitions=[
                Transition("PENDING", "ACTIVE", "first_result_reported",
                           actors=frozenset({Actor.AI_EMPLOYEE.value})),
                Transition("ACTIVE", "ACTIVE", "continue_cycle",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACTIVE", "PENDING_REVISION", "revise_responsibility",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PENDING_REVISION", "ACTIVE", "blueprint_approved",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACTIVE", "PAUSED", "pause",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "ACTIVE", "resume",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACTIVE", "FULFILLED", "fulfill",
                           actors=frozenset({Actor.CEO.value}),
                           guard=lambda c: None if c.get("verificationStatus") == "VERIFIED"
                           else "目标结果未 VERIFIED，不得标记完成"),
                Transition("PENDING", "RELEASED", "release_on_archive",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("ACTIVE", "RELEASED", "release_on_archive",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("PENDING_REVISION", "RELEASED", "release_on_archive",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("PAUSED", "RELEASED", "release_on_archive",
                           actors=frozenset({Actor.SYSTEM.value})),
            ],
        )
    )

    # 3) Workspace（装修流水线：DRAFT→BLUEPRINTING→SIMULATED→PENDING_APPROVAL
    #    →OPERATING，外加 PAUSED / ARCHIVED）
    registry.register(
        StateMachine(
            entity_type="workspace",
            states=WorkspaceStatus,
            initial=[WorkspaceStatus.DRAFT],
            terminal=[WorkspaceStatus.ARCHIVED],
            transitions=[
                Transition("DRAFT", "BLUEPRINTING", "start_blueprint",
                           actors=frozenset({Actor.CEO.value})),
                Transition("BLUEPRINTING", "SIMULATED", "simulation_passed",
                           actors=frozenset({Actor.CEO.value, Actor.SYSTEM.value}),
                           guard=lambda c: None if c.get("simulationPassed")
                           else "模拟未通过，请先运行模拟"),
                Transition("SIMULATED", "PENDING_APPROVAL", "submit_for_approval",
                           actors=frozenset({Actor.CEO.value}),
                           guard=lambda c: None if (
                               c.get("issuesResolved")
                               and c.get("simulationPassed")
                               and c.get("externalAgentReviewed")
                           ) else "三级门禁未通过：请先修复配置问题 / 运行模拟 / 审阅外部 Agent"),
                Transition("PENDING_APPROVAL", "OPERATING", "approve_and_launch",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PENDING_APPROVAL", "BLUEPRINTING", "request_changes",
                           actors=frozenset({Actor.CEO.value})),
                Transition("OPERATING", "PAUSED", "pause",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "OPERATING", "resume",
                           actors=frozenset({Actor.CEO.value})),
                Transition("DRAFT", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
                Transition("BLUEPRINTING", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
                Transition("SIMULATED", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PENDING_APPROVAL", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
                Transition("OPERATING", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "ARCHIVED", "archive",
                           actors=frozenset({Actor.CEO.value})),
            ],
        )
    )

    # 4) Cadence（原型只有 enabled 布尔；扩为完整生命周期）
    registry.register(
        StateMachine(
            entity_type="cadence",
            states=CadenceStatus,
            initial=[CadenceStatus.DRAFT],
            terminal=[CadenceStatus.RETIRED],
            transitions=[
                Transition("DRAFT", "ENABLED", "enable",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ENABLED", "PAUSED", "pause",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "ENABLED", "resume",
                           actors=frozenset({Actor.CEO.value})),
                Transition("DRAFT", "RETIRED", "retire",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ENABLED", "RETIRED", "retire",
                           actors=frozenset({Actor.CEO.value})),
                Transition("PAUSED", "RETIRED", "retire",
                           actors=frozenset({Actor.CEO.value})),
            ],
        )
    )

    # 5) ScheduledRun（7 态，系统的心跳）
    #    注意：RUNNING → RESOLVED 是文档明确禁止的非法流转，此处**不声明**。
    registry.register(
        StateMachine(
            entity_type="scheduled_run",
            states=RunStatus,
            initial=[RunStatus.QUEUED, RunStatus.RUNNING],
            terminal=[RunStatus.COMPLETED, RunStatus.RESOLVED],
            transitions=[
                Transition("QUEUED", "RUNNING", "capacity_released",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("RUNNING", "COMPLETED", "execution_finished",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("RUNNING", "WAITING_CEO", "escalation_hit",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("RUNNING", "FAILED", "execution_error",
                           actors=frozenset({Actor.SYSTEM.value})),
                Transition("WAITING_CEO", "ACKNOWLEDGED", "ceo_opened",
                           actors=frozenset({Actor.CEO.value})),
                Transition("ACKNOWLEDGED", "RESOLVED", "ceo_resolved",
                           actors=frozenset({Actor.CEO.value})),
                Transition("FAILED", "ACKNOWLEDGED", "ceo_intervened",
                           actors=frozenset({Actor.CEO.value})),
                Transition("FAILED", "RESOLVED", "ceo_intervened",
                           actors=frozenset({Actor.CEO.value})),
                Transition("QUEUED", "FAILED", "queue_timeout",
                           actors=frozenset({Actor.SYSTEM.value})),
            ],
        )
    )

    def add(entity_type, states, transitions, *, terminal=()):
        foundation_registry.register(
            StateMachine(
                entity_type=entity_type,
                states=states,
                initial=[next(iter(states))],
                terminal=list(terminal),
                transitions=[
                    Transition(source, target, trigger, actors=frozenset(actors), guard=guard)
                    for source, target, trigger, actors, guard in transitions
                ],
            )
        )

    CEO_ONLY = {Actor.CEO.value}
    SYSTEM_ONLY = {Actor.SYSTEM.value}
    AI_OR_SYSTEM = {Actor.AI_EMPLOYEE.value, Actor.SYSTEM.value}
    CEO_OR_SYSTEM = {Actor.CEO.value, Actor.SYSTEM.value}

    add("founding_run", FoundingRunStatus, [
        ("ARRIVED", "INTENT_CAPTURED", "capture_intent", CEO_OR_SYSTEM, None),
        ("INTENT_CAPTURED", "CLARIFYING", "request_clarification", CEO_OR_SYSTEM, None),
        ("CLARIFYING", "PROPOSED", "propose_company", CEO_OR_SYSTEM, None),
        ("PROPOSED", "CEO_CONFIRMED", "confirm_company", CEO_ONLY, None),
        ("PROPOSED", "WAITING_CEO", "wait_for_ceo", AI_OR_SYSTEM, None),
        ("WAITING_CEO", "PROPOSED", "resume_proposal", CEO_ONLY, None),
        ("CEO_CONFIRMED", "PROPOSED", "reject_confirmation", CEO_ONLY, None),
        ("CEO_CONFIRMED", "COMPANY_CREATED", "persist_company", SYSTEM_ONLY, None),
        ("COMPANY_CREATED", "FIRST_BUSINESS_CONFIGURING", "configure_business", CEO_OR_SYSTEM, None),
        ("FIRST_BUSINESS_CONFIGURING", "WAITING_CEO", "wait_for_business_input", AI_OR_SYSTEM, None),
        ("WAITING_CEO", "FIRST_BUSINESS_CONFIGURING", "resume_business_configuration", CEO_ONLY, None),
        ("FIRST_BUSINESS_CONFIGURING", "FIRST_BUSINESS_READY", "business_ready", CEO_ONLY, None),
        ("FIRST_BUSINESS_READY", "COMPLETED", "complete_founding", CEO_ONLY, None),
        ("PROPOSED", "REJECTED", "reject_proposal", CEO_ONLY, None),
        ("REJECTED", "CLARIFYING", "revise_proposal", CEO_ONLY, None),
        ("CLARIFYING", "RETURNED", "return_scope", CEO_OR_SYSTEM, None),
        ("RETURNED", "CLARIFYING", "resume_returned", CEO_ONLY, None),
        ("ARRIVED", "ABANDONED", "abandon", CEO_ONLY, None),
        ("PROPOSED", "ABANDONED", "abandon", CEO_ONLY, None),
    ], terminal=(FoundingRunStatus.COMPLETED, FoundingRunStatus.ABANDONED))

    add("ceo_assistant", CEOAssistantStatus, [
        ("CREATED", "CONFIGURED", "configure", CEO_ONLY, None),
        ("CONFIGURED", "LEARNING_CONTEXT", "learn_context", CEO_OR_SYSTEM, None),
        ("LEARNING_CONTEXT", "OPERATING", "accept_context", CEO_ONLY, None),
        ("OPERATING", "EVALUATING", "evaluate", CEO_OR_SYSTEM, None),
        ("EVALUATING", "OPERATING", "resume", CEO_ONLY, None),
        ("OPERATING", "SUSPENDED", "suspend", CEO_ONLY, None),
        ("EVALUATING", "UPGRADED", "upgrade", CEO_ONLY, None),
        ("EVALUATING", "REASSIGNED", "reassign", CEO_ONLY, None),
        ("UPGRADED", "OPERATING", "complete_upgrade", CEO_ONLY, None),
        ("REASSIGNED", "OPERATING", "complete_reassignment", CEO_ONLY, None),
        ("SUSPENDED", "CONFIGURED", "reconfigure", CEO_ONLY, None),
    ])

    add("ai_employee", AIEmployeeStatus, [
        ("PROPOSED", "CREATED", "accept_proposal", CEO_ONLY, None),
        ("CREATED", "CONFIGURED", "configure", CEO_ONLY, None),
        ("CONFIGURED", "AVAILABLE", "approve_simulation", CEO_ONLY, None),
        ("AVAILABLE", "OPERATING", "accept_handoff", {Actor.AI_EMPLOYEE.value}, None),
        ("OPERATING", "AVAILABLE", "complete_responsibility", AI_OR_SYSTEM, None),
        ("AVAILABLE", "DEGRADED", "capacity_or_capability_gap", AI_OR_SYSTEM, None),
        ("OPERATING", "DEGRADED", "execution_degraded", AI_OR_SYSTEM, None),
        ("DEGRADED", "AVAILABLE", "gap_resolved", CEO_OR_SYSTEM, None),
        ("DEGRADED", "SUSPENDED", "suspend", CEO_ONLY, None),
        ("AVAILABLE", "SUSPENDED", "suspend", CEO_ONLY, None),
        ("OPERATING", "REASSIGNED", "reassign", CEO_ONLY, None),
        ("REASSIGNED", "CONFIGURED", "complete_reassignment", CEO_ONLY, None),
        ("OPERATING", "RETIRED", "retire", CEO_ONLY, None),
        ("SUSPENDED", "RETIRED", "retire", CEO_ONLY, None),
    ], terminal=(AIEmployeeStatus.RETIRED,))

    add("role_slot", RoleSlotStatus, [
        ("DRAFT", "READY", "validate_role", CEO_OR_SYSTEM, None),
        ("READY", "ASSIGNED", "assign", CEO_ONLY, None),
        ("ASSIGNED", "OPERATING", "accept_assignment", {Actor.AI_EMPLOYEE.value}, None),
        ("READY", "BLOCKED", "block", AI_OR_SYSTEM, None),
        ("ASSIGNED", "BLOCKED", "block", AI_OR_SYSTEM, None),
        ("BLOCKED", "READY", "resolve_block", CEO_OR_SYSTEM, None),
        ("ASSIGNED", "REASSIGNING", "reassign", CEO_ONLY, None),
        ("OPERATING", "REASSIGNING", "reassign", CEO_ONLY, None),
        ("REASSIGNING", "READY", "return_to_ready", CEO_OR_SYSTEM, None),
        ("READY", "RETIRED", "retire", CEO_ONLY, None),
    ], terminal=(RoleSlotStatus.RETIRED,))

    add("capability_binding", CapabilityBindingStatus, [
        ("PROPOSED", "AUTHORIZED", "authorize", CEO_ONLY, None),
        ("AUTHORIZED", "ACTIVE", "activate", CEO_OR_SYSTEM, None),
        ("ACTIVE", "DEGRADED", "degrade", AI_OR_SYSTEM, None),
        ("DEGRADED", "ACTIVE", "restore", CEO_OR_SYSTEM, None),
        ("AUTHORIZED", "REVOKED", "revoke", CEO_ONLY, None),
        ("ACTIVE", "REVOKED", "revoke", CEO_ONLY, None),
        ("DEGRADED", "REVOKED", "revoke", CEO_ONLY, None),
    ], terminal=(CapabilityBindingStatus.REVOKED,))

    add("cycle", CycleStatus, [
        ("PLANNED", "READY", "ready", CEO_ONLY, None),
        ("READY", "RUNNING", "start", CEO_ONLY, None),
        ("RUNNING", "WAITING_CEO", "request_acceptance", AI_OR_SYSTEM, None),
        ("WAITING_CEO", "ACCEPTED", "accept", CEO_ONLY, lambda c: None if c.get("acceptanceId") else "缺少 Acceptance"),
        ("WAITING_CEO", "REJECTED", "reject", CEO_ONLY, None),
        ("REJECTED", "PLANNED", "revise", CEO_ONLY, None),
        ("ACCEPTED", "REVIEWING", "review", CEO_OR_SYSTEM, None),
        ("REVIEWING", "CLOSED", "close", CEO_ONLY, None),
        ("RUNNING", "PAUSED", "pause", CEO_OR_SYSTEM, None),
        ("PAUSED", "RUNNING", "resume", CEO_ONLY, None),
        ("RUNNING", "FAILED", "fail", AI_OR_SYSTEM, None),
    ], terminal=(CycleStatus.CLOSED, CycleStatus.FAILED))

    add("handoff", HandoffStatus, [
        ("CREATED", "SENT", "send", AI_OR_SYSTEM, None),
        ("SENT", "ACKNOWLEDGED", "acknowledge", {Actor.AI_EMPLOYEE.value, Actor.CEO.value}, None),
        ("ACKNOWLEDGED", "COMPLETED", "complete", {Actor.AI_EMPLOYEE.value, Actor.CEO.value}, None),
        ("SENT", "RETURNED", "return", {Actor.AI_EMPLOYEE.value}, None),
        ("SENT", "REJECTED", "reject", {Actor.AI_EMPLOYEE.value, Actor.CEO.value}, None),
    ], terminal=(HandoffStatus.COMPLETED, HandoffStatus.RETURNED, HandoffStatus.REJECTED))

    add("decision_packet", DecisionPacketStatus, [
        ("DRAFT", "READY", "prepare", AI_OR_SYSTEM, None),
        ("READY", "DECIDED", "leader_decide", {Actor.AI_EMPLOYEE.value},
         lambda c: None if (
             c.get("decisionDomain") == "AUTONOMOUS_NEXT_CYCLE"
             and c.get("leaderAuthorized") is True
             and c.get("decision") in {"CONTINUE", "ADJUST", "WAIT"}
         ) else "仅允许已验证 Leader 在 Approved Strategy Envelope 内形成下一周期决定"),
        ("READY", "WAITING_CEO", "request_decision", AI_OR_SYSTEM, None),
        ("WAITING_CEO", "DECIDED", "decide", CEO_ONLY, None),
        ("DECIDED", "APPLIED", "apply", SYSTEM_ONLY, None),
        ("APPLIED", "ROLLED_BACK", "rollback", CEO_ONLY, None),
    ], terminal=(DecisionPacketStatus.ROLLED_BACK,))

    add("acceptance", AcceptanceStatus, [
        ("PENDING", "ACCEPTED", "accept", CEO_ONLY, None),
        ("PENDING", "REJECTED", "reject", CEO_ONLY, None),
        ("PENDING", "EVIDENCE_REQUIRED", "request_evidence", CEO_ONLY, None),
        ("EVIDENCE_REQUIRED", "PENDING", "supply_evidence", AI_OR_SYSTEM, None),
        ("ACCEPTED", "CLOSED", "close", CEO_OR_SYSTEM, None),
        ("REJECTED", "CLOSED", "close", CEO_OR_SYSTEM, None),
    ], terminal=(AcceptanceStatus.CLOSED,))

    add("simulation_run", SimulationStatus, [
        ("DRAFT", "RUNNING", "start", CEO_OR_SYSTEM, None),
        ("RUNNING", "WAITING_CEO", "wait_for_ceo", AI_OR_SYSTEM, None),
        ("WAITING_CEO", "RUNNING", "resume", CEO_ONLY, None),
        ("RUNNING", "REVIEWED", "review", CEO_OR_SYSTEM, None),
        ("REVIEWED", "PASSED", "pass", CEO_ONLY, lambda c: None if c.get("passStatus") == "PASS" else "passStatus 必须为 PASS"),
        ("REVIEWED", "FAILED", "fail", CEO_ONLY, None),
        ("RUNNING", "CANCELLED", "cancel", CEO_ONLY, None),
        ("PASSED", "ARCHIVED", "archive", CEO_ONLY, None),
        ("FAILED", "ARCHIVED", "archive", CEO_ONLY, None),
        ("CANCELLED", "ARCHIVED", "archive", CEO_ONLY, None),
    ], terminal=(SimulationStatus.ARCHIVED,))

    add("content_item", ContentStatus, [
        ("IDEA", "DRAFT", "accept_idea", CEO_OR_SYSTEM, None),
        ("DRAFT", "IN_REVIEW", "submit_review", {Actor.AI_EMPLOYEE.value, Actor.CEO.value}, None),
        ("IN_REVIEW", "APPROVED", "approve", CEO_ONLY, lambda c: None if c.get("approvedVersionId") else "缺少 approvedVersionId"),
        ("IN_REVIEW", "DRAFT", "request_changes", CEO_ONLY, None),
        ("APPROVED", "SCHEDULED", "schedule", CEO_OR_SYSTEM, None),
        ("APPROVED", "PUBLISHED", "manual_publish", CEO_ONLY, lambda c: None if c.get("publishedVersionId") and (c.get("externalReceipt") or c.get("manualFeedbackRef")) else "缺少发布版本或外部回执"),
        ("SCHEDULED", "PUBLISHED", "publish", {Actor.EXTERNAL.value, Actor.SYSTEM.value}, lambda c: None if c.get("publishedVersionId") and c.get("externalReceipt") else "缺少发布版本或外部回执"),
        ("PUBLISHED", "AWAITING_FEEDBACK", "await_feedback", SYSTEM_ONLY, None),
        ("AWAITING_FEEDBACK", "REVIEWED", "review_outcome", CEO_ONLY, None),
        ("REVIEWED", "CARRIED_FORWARD", "carry_forward", CEO_ONLY, None),
        ("REVIEWED", "ARCHIVED", "archive", CEO_ONLY, None),
    ], terminal=(ContentStatus.ARCHIVED, ContentStatus.CARRIED_FORWARD))

    add("interaction_item", InteractionStatus, [
        ("RECEIVED", "CLASSIFIED", "classify", AI_OR_SYSTEM, None),
        ("CLASSIFIED", "WAITING_CEO", "request_decision", AI_OR_SYSTEM, None),
        ("CLASSIFIED", "RESPONDED", "respond", AI_OR_SYSTEM, lambda c: None if c.get("replyPolicy") == "AUTO_APPROVED" and c.get("responseVersion") and c.get("externalReceipt") else "回复策略、回复版本或外部回执不完整"),
        ("WAITING_CEO", "RESPONDED", "approve_response", CEO_ONLY, lambda c: None if c.get("responseVersion") and c.get("externalReceipt") else "缺少回复版本或外部回执"),
        ("RESPONDED", "CLOSED", "close", CEO_OR_SYSTEM, None),
    ], terminal=(InteractionStatus.CLOSED,))

    return registry


#: 默认全局注册表（导入即装配）。
runtime_registry = _build_registry()


def get_registered_machine(entity_type: str) -> StateMachine:
    try:
        return runtime_registry.get(entity_type)
    except KeyError:
        return foundation_registry.get(entity_type)
