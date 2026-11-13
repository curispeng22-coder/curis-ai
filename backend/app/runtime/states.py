"""Curis Business Runtime —— 状态枚举集中定义。

依据：``docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`` §1.1

为什么需要这个模块
------------------
接管审计（2026-08-03）发现：后端全域只有 2 个 Enum，却有 12 套裸字符串状态，
并且已经出过事——业务代码写 ``succeeded``，数据库 check 约束写 ``completed``，
两边对不上。

因此本模块是**唯一**的状态值来源：

  - 业务代码禁止再出现裸字符串状态字面量；
  - 历史裸字符串通过 :func:`normalize` 收敛到规范值；
  - 每个状态都带中文界面文案（``label``），界面层不再自行硬编码翻译。

界面用语纪律（ADR 中文用语统一）：界面禁用「下注/赌注/ROI/KPI/投资组合」，
本模块给出的 ``label`` 即为界面可直接使用的措辞。
"""

from __future__ import annotations

from enum import Enum
from typing import Iterable


class CurisState(str, Enum):
    """所有业务状态枚举的基类。

    继承 ``str`` 以便直接与数据库中的文本列互操作，同时保留枚举的类型约束。
    """

    @property
    def label(self) -> str:
        """返回该状态的中文界面文案。"""
        return _LABELS.get((type(self).__name__, self.value), self.value)

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls)

    @classmethod
    def has(cls, value: str) -> bool:
        return value in cls.values()

    def __str__(self) -> str:  # pragma: no cover - 便于日志输出
        return self.value


# ---------------------------------------------------------------------------
# 通用维度
# ---------------------------------------------------------------------------


class Actor(str, Enum):
    """状态流转的触发者分类。

    归因与审计的基础：任何一次流转都必须能回答「是谁让它变的」。
    """

    CEO = "CEO"
    AI_EMPLOYEE = "AI_EMPLOYEE"
    SYSTEM = "SYSTEM"
    EXTERNAL = "EXTERNAL"


class EvidenceGrade(CurisState):
    """证据等级。被结果、经营账、公司脉搏共用。

    硬规则：只有 ``VERIFIED`` 的结果才能支持「扩大业务」；
    ``ABNORMAL`` 冻结扩大权限。
    """

    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    ABNORMAL = "ABNORMAL"


class EscalationTrigger(str, Enum):
    """结构化升级声明。

    取代原型里「用正则匹配任务描述文案」的隐式契约——那种做法下，
    改一句措辞就会静默改变系统行为。
    """

    ON_FAILURE = "ON_FAILURE"
    ON_MISSING_AUTH = "ON_MISSING_AUTH"
    ON_EXTERNAL_DATA_RETURN = "ON_EXTERNAL_DATA_RETURN"
    ON_ABNORMAL_RESULT = "ON_ABNORMAL_RESULT"
    ALWAYS_BEFORE_PUBLISH = "ALWAYS_BEFORE_PUBLISH"
    ALWAYS_BEFORE_SPEND = "ALWAYS_BEFORE_SPEND"
    ALWAYS_BEFORE_EXTERNAL_COMMITMENT = "ALWAYS_BEFORE_EXTERNAL_COMMITMENT"
    ALWAYS_BEFORE_PERMISSION_CHANGE = "ALWAYS_BEFORE_PERMISSION_CHANGE"
    ALWAYS_BEFORE_IRREVERSIBLE = "ALWAYS_BEFORE_IRREVERSIBLE"
    ALWAYS_BEFORE_SCOPE_EXPANSION = "ALWAYS_BEFORE_SCOPE_EXPANSION"
    NEVER = "NEVER"


#: 六件 AI 不得静默执行的事——命中即必须升级 CEO，不接受配置为 NEVER。
NON_SILENT_TRIGGERS: frozenset[EscalationTrigger] = frozenset(
    {
        EscalationTrigger.ALWAYS_BEFORE_PUBLISH,
        EscalationTrigger.ALWAYS_BEFORE_SPEND,
        EscalationTrigger.ALWAYS_BEFORE_EXTERNAL_COMMITMENT,
        EscalationTrigger.ALWAYS_BEFORE_PERMISSION_CHANGE,
        EscalationTrigger.ALWAYS_BEFORE_IRREVERSIBLE,
        EscalationTrigger.ALWAYS_BEFORE_SCOPE_EXPANSION,
    }
)


# ---------------------------------------------------------------------------
# 业务方向
# ---------------------------------------------------------------------------


class BusinessLifecycle(CurisState):
    """业务方向的生命周期。

    与 :class:`EvidenceGrade`（验证结论）是**两个正交维度**。
    原型把二者混在一个 pill 里显示，造成语义重叠，此处拆开。
    """

    DRAFT = "DRAFT"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    ACTIVE = "ACTIVE"
    SCALING = "SCALING"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


# ---------------------------------------------------------------------------
# 承诺
# ---------------------------------------------------------------------------


class CommitmentStatus(CurisState):
    """承诺状态。

    ``FULFILLED`` / ``RELEASED`` 是本次补齐——原型里承诺只能被暂停，
    没有正常收尾的终态。
    """

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PENDING_REVISION = "PENDING_REVISION"
    PAUSED = "PAUSED"
    FULFILLED = "FULFILLED"
    RELEASED = "RELEASED"


# ---------------------------------------------------------------------------
# 工作空间
# ---------------------------------------------------------------------------


class WorkspaceStatus(CurisState):
    """工作空间生命周期。

    对应装修流水线：Discover → Blueprint → Compose → Bind → Staff →
    Simulate → Approve → Operate。
    """

    DRAFT = "DRAFT"
    BLUEPRINTING = "BLUEPRINTING"
    SIMULATED = "SIMULATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    OPERATING = "OPERATING"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


class StageSlot(str, Enum):
    """通用 9 槽位交付骨架。

    四个业务运行时（短视频/小红书/软件研发/部门型）经比对是**同一引擎的
    四份配置**，槽位对齐。业务差异只允许存在于配置里，严禁为每个业务
    写一套页面或一套后端逻辑。
    """

    INTAKE = "INTAKE"
    PRODUCE = "PRODUCE"
    DELIVER = "DELIVER"
    COLLECT = "COLLECT"
    ACCEPT = "ACCEPT"
    REVIEW = "REVIEW"
    IMPROVE = "IMPROVE"
    ARCHIVE = "ARCHIVE"


class HumanGate(str, Enum):
    """环节的人工介入档位。"""

    AUTO = "AUTO"
    CEO_CHECKPOINT = "CEO_CHECKPOINT"
    CEO_REQUIRED = "CEO_REQUIRED"


class WorkItemStatus(CurisState):
    """在环节之间流动的工件状态（如一条待发布的视频）。"""

    ON_TRACK = "ON_TRACK"
    ATTENTION = "ATTENTION"
    AWAITING_DECISION = "AWAITING_DECISION"
    AT_RISK = "AT_RISK"
    ARCHIVED = "ARCHIVED"


# ---------------------------------------------------------------------------
# 节奏与运行
# ---------------------------------------------------------------------------


class CadenceStatus(CurisState):
    """节奏定义状态。原型只有 enabled 布尔，此处扩为完整生命周期。"""

    DRAFT = "DRAFT"
    ENABLED = "ENABLED"
    PAUSED = "PAUSED"
    RETIRED = "RETIRED"


class RunStatus(CurisState):
    """单次运行实例状态——系统的心跳，原型中最完整的一个状态机。

    注意：``RUNNING → RESOLVED`` 是**非法**流转。运行中不得被直接判结，
    必须先经过 ``WAITING_CEO`` / ``ACKNOWLEDGED`` 或 ``FAILED``。
    """

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING_CEO = "WAITING_CEO"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


# ---------------------------------------------------------------------------
# 结果与归因
# ---------------------------------------------------------------------------


class EvidenceAdoption(CurisState):
    """证据采用状态。"""

    PENDING_ADOPTION = "PENDING_ADOPTION"
    ADOPTED = "ADOPTED"
    UNREGISTERED = "UNREGISTERED"


class AllocationStatus(CurisState):
    """贡献分配状态。确认时权重合计必须等于 100%。"""

    PENDING_REVIEW = "PENDING_REVIEW"
    REVIEWED = "REVIEWED"


# ---------------------------------------------------------------------------
# Runtime Foundation v1.6
# ---------------------------------------------------------------------------


class FoundingRunStatus(CurisState):
    ARRIVED = "ARRIVED"
    INTENT_CAPTURED = "INTENT_CAPTURED"
    CLARIFYING = "CLARIFYING"
    PROPOSED = "PROPOSED"
    CEO_CONFIRMED = "CEO_CONFIRMED"
    COMPANY_CREATED = "COMPANY_CREATED"
    FIRST_BUSINESS_CONFIGURING = "FIRST_BUSINESS_CONFIGURING"
    FIRST_BUSINESS_READY = "FIRST_BUSINESS_READY"
    WAITING_CEO = "WAITING_CEO"
    RETURNED = "RETURNED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class CEOAssistantStatus(CurisState):
    CREATED = "CREATED"
    CONFIGURED = "CONFIGURED"
    LEARNING_CONTEXT = "LEARNING_CONTEXT"
    OPERATING = "OPERATING"
    EVALUATING = "EVALUATING"
    SUSPENDED = "SUSPENDED"
    UPGRADED = "UPGRADED"
    REASSIGNED = "REASSIGNED"


class AIEmployeeStatus(CurisState):
    PROPOSED = "PROPOSED"
    CREATED = "CREATED"
    CONFIGURED = "CONFIGURED"
    AVAILABLE = "AVAILABLE"
    OPERATING = "OPERATING"
    DEGRADED = "DEGRADED"
    SUSPENDED = "SUSPENDED"
    REASSIGNED = "REASSIGNED"
    RETIRED = "RETIRED"


class PresenceState(CurisState):
    AVAILABLE = "AVAILABLE"
    RUNNING = "RUNNING"
    WAITING_CEO = "WAITING_CEO"
    BLOCKED = "BLOCKED"
    PAUSED = "PAUSED"


class RoleSlotStatus(CurisState):
    DRAFT = "DRAFT"
    READY = "READY"
    ASSIGNED = "ASSIGNED"
    OPERATING = "OPERATING"
    BLOCKED = "BLOCKED"
    REASSIGNING = "REASSIGNING"
    RETIRED = "RETIRED"


class CapabilityBindingStatus(CurisState):
    PROPOSED = "PROPOSED"
    AUTHORIZED = "AUTHORIZED"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    REVOKED = "REVOKED"


class CycleStatus(CurisState):
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING_CEO = "WAITING_CEO"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REVIEWING = "REVIEWING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    CLOSED = "CLOSED"


class HandoffStatus(CurisState):
    CREATED = "CREATED"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    COMPLETED = "COMPLETED"
    RETURNED = "RETURNED"
    REJECTED = "REJECTED"


class DecisionPacketStatus(CurisState):
    DRAFT = "DRAFT"
    READY = "READY"
    WAITING_CEO = "WAITING_CEO"
    DECIDED = "DECIDED"
    APPLIED = "APPLIED"
    ROLLED_BACK = "ROLLED_BACK"


class AcceptanceStatus(CurisState):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"
    CLOSED = "CLOSED"


class VerificationStatus(CurisState):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class EvidenceCondition(CurisState):
    CURRENT = "CURRENT"
    MISSING = "MISSING"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    ABNORMAL = "ABNORMAL"


class ExceptionStatus(CurisState):
    NONE = "NONE"
    INVALID = "INVALID"
    WAITING_CEO = "WAITING_CEO"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    STALE = "STALE"
    ABNORMAL = "ABNORMAL"
    ESCALATED = "ESCALATED"


class SimulationStatus(CurisState):
    DRAFT = "DRAFT"
    RUNNING = "RUNNING"
    WAITING_CEO = "WAITING_CEO"
    REVIEWED = "REVIEWED"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class SimulationPassStatus(CurisState):
    NOT_RUN = "NOT_RUN"
    IN_PROGRESS = "IN_PROGRESS"
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ContentStatus(CurisState):
    IDEA = "IDEA"
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    AWAITING_FEEDBACK = "AWAITING_FEEDBACK"
    REVIEWED = "REVIEWED"
    CARRIED_FORWARD = "CARRIED_FORWARD"
    ARCHIVED = "ARCHIVED"


class InteractionStatus(CurisState):
    RECEIVED = "RECEIVED"
    CLASSIFIED = "CLASSIFIED"
    WAITING_CEO = "WAITING_CEO"
    RESPONDED = "RESPONDED"
    CLOSED = "CLOSED"


# ---------------------------------------------------------------------------
# 中文界面文案
# ---------------------------------------------------------------------------

_LABELS: dict[tuple[str, str], str] = {
    ("EvidenceGrade", "UNVERIFIED"): "数据待验证",
    ("EvidenceGrade", "VERIFIED"): "已验证价值",
    ("EvidenceGrade", "ABNORMAL"): "结果异常",
    ("BusinessLifecycle", "DRAFT"): "草稿",
    ("BusinessLifecycle", "PENDING_APPROVAL"): "待批准团队配置",
    ("BusinessLifecycle", "ACTIVE"): "验证中",
    ("BusinessLifecycle", "SCALING"): "扩大中",
    ("BusinessLifecycle", "PAUSED"): "已暂停",
    ("BusinessLifecycle", "ARCHIVED"): "已归档",
    ("CommitmentStatus", "PENDING"): "待接受",
    ("CommitmentStatus", "ACTIVE"): "运行中",
    ("CommitmentStatus", "PENDING_REVISION"): "待调整",
    ("CommitmentStatus", "PAUSED"): "已暂停",
    ("CommitmentStatus", "FULFILLED"): "已完成",
    ("CommitmentStatus", "RELEASED"): "已解除",
    ("WorkspaceStatus", "DRAFT"): "草稿 · 未命名",
    ("WorkspaceStatus", "BLUEPRINTING"): "装修中",
    ("WorkspaceStatus", "SIMULATED"): "模拟已通过，可提交审批",
    ("WorkspaceStatus", "PENDING_APPROVAL"): "待审批",
    ("WorkspaceStatus", "OPERATING"): "运行中",
    ("WorkspaceStatus", "PAUSED"): "已暂停",
    ("WorkspaceStatus", "ARCHIVED"): "已归档",
    ("WorkItemStatus", "ON_TRACK"): "正常",
    ("WorkItemStatus", "ATTENTION"): "关注",
    ("WorkItemStatus", "AWAITING_DECISION"): "待决策",
    ("WorkItemStatus", "AT_RISK"): "风险",
    ("WorkItemStatus", "ARCHIVED"): "已归档",
    ("CadenceStatus", "DRAFT"): "草稿",
    ("CadenceStatus", "ENABLED"): "已启用",
    ("CadenceStatus", "PAUSED"): "已暂停",
    ("CadenceStatus", "RETIRED"): "已停用",
    ("RunStatus", "QUEUED"): "排队中",
    ("RunStatus", "RUNNING"): "执行中",
    ("RunStatus", "WAITING_CEO"): "待 CEO",
    ("RunStatus", "ACKNOWLEDGED"): "已打开",
    ("RunStatus", "RESOLVED"): "已处理",
    ("RunStatus", "FAILED"): "异常",
    ("RunStatus", "COMPLETED"): "已完成",
    ("EvidenceAdoption", "PENDING_ADOPTION"): "待 CEO 采用",
    ("EvidenceAdoption", "ADOPTED"): "已采用",
    ("EvidenceAdoption", "UNREGISTERED"): "未登记",
    ("AllocationStatus", "PENDING_REVIEW"): "待复核",
    ("AllocationStatus", "REVIEWED"): "已确认",
}


# ---------------------------------------------------------------------------
# 历史裸字符串收敛
# ---------------------------------------------------------------------------

#: 历史遗留写法 → 规范值。
#:
#: 这里修复的是接管审计发现的真实缺陷：业务代码写 ``succeeded``，
#: 数据库 check 约束写 ``completed``。别名表让旧数据在读取时被收敛，
#: 而不是让两套写法长期共存。
_ALIASES: dict[str, dict[str, str]] = {
    "RunStatus": {
        "succeeded": "COMPLETED",
        "success": "COMPLETED",
        "done": "COMPLETED",
        "finished": "COMPLETED",
        "complete": "COMPLETED",
        "completed": "COMPLETED",
        "queued": "QUEUED",
        "pending": "QUEUED",
        "waiting": "QUEUED",
        "running": "RUNNING",
        "in_progress": "RUNNING",
        "executing": "RUNNING",
        "waiting_ceo": "WAITING_CEO",
        "awaiting_ceo": "WAITING_CEO",
        "acknowledged": "ACKNOWLEDGED",
        "resolved": "RESOLVED",
        "failed": "FAILED",
        "error": "FAILED",
        "failure": "FAILED",
    },
    "CommitmentStatus": {
        "pending": "PENDING",
        "active": "ACTIVE",
        "pending_revision": "PENDING_REVISION",
        "paused": "PAUSED",
        "fulfilled": "FULFILLED",
        "released": "RELEASED",
    },
    "BusinessLifecycle": {
        "draft": "DRAFT",
        "pending_approval": "PENDING_APPROVAL",
        "continue": "ACTIVE",
        "active": "ACTIVE",
        "operating": "ACTIVE",
        "scale": "SCALING",
        "scaling": "SCALING",
        "pause": "PAUSED",
        "paused": "PAUSED",
        "close": "ARCHIVED",
        "closed": "ARCHIVED",
        "archived": "ARCHIVED",
    },
    "WorkspaceStatus": {
        "draft": "DRAFT",
        "blueprinting": "BLUEPRINTING",
        "装修中": "BLUEPRINTING",
        "simulated": "SIMULATED",
        "pending_approval": "PENDING_APPROVAL",
        "operating": "OPERATING",
        "运行中": "OPERATING",
        "paused": "PAUSED",
        "archived": "ARCHIVED",
        "已归档": "ARCHIVED",
    },
    "EvidenceGrade": {
        "unverified": "UNVERIFIED",
        "数据待验证": "UNVERIFIED",
        "verified": "VERIFIED",
        "已验证价值": "VERIFIED",
        "abnormal": "ABNORMAL",
        "结果异常": "ABNORMAL",
    },
    "WorkItemStatus": {
        "ontrack": "ON_TRACK",
        "on_track": "ON_TRACK",
        "attention": "ATTENTION",
        "decision": "AWAITING_DECISION",
        "risk": "AT_RISK",
        "archived": "ARCHIVED",
    },
    "CadenceStatus": {
        "draft": "DRAFT",
        "enabled": "ENABLED",
        "paused": "PAUSED",
        "retired": "RETIRED",
    },
}


class UnknownStateError(ValueError):
    """给定的状态值无法被收敛到规范枚举。"""


def normalize(enum_cls: type[CurisState], value: str | CurisState) -> CurisState:
    """把任意历史写法收敛成规范枚举成员。

    收敛顺序：枚举成员 → 精确值 → 大写值 → 别名表（大小写不敏感）。
    无法识别时抛 :class:`UnknownStateError`，而不是静默放行——
    静默放行正是 ``succeeded`` / ``completed`` 不一致能长期存在的原因。
    """
    if isinstance(value, enum_cls):
        return value
    if value is None:  # type: ignore[comparison-overlap]
        raise UnknownStateError(f"{enum_cls.__name__} 不接受空状态值")

    raw = str(value).strip()
    if not raw:
        raise UnknownStateError(f"{enum_cls.__name__} 不接受空状态值")

    if enum_cls.has(raw):
        return enum_cls(raw)

    upper = raw.upper()
    if enum_cls.has(upper):
        return enum_cls(upper)

    alias_map = _ALIASES.get(enum_cls.__name__, {})
    mapped = alias_map.get(raw) or alias_map.get(raw.lower())
    if mapped is not None:
        return enum_cls(mapped)

    raise UnknownStateError(
        f"无法把 {raw!r} 收敛为 {enum_cls.__name__}；"
        f"合法值：{', '.join(enum_cls.values())}"
    )


def labels_of(enum_cls: type[CurisState]) -> dict[str, str]:
    """返回某个枚举的 ``值 → 中文文案`` 映射，供接口一次性下发给前端。"""
    return {member.value: member.label for member in enum_cls}


def check_constraint(column: str, enum_cls: type[CurisState]) -> str:
    """生成 SQLite ``check`` 约束片段，保证库内取值与枚举同源。

    这样就不会再出现「代码一套值、约束另一套值」的漂移。
    """
    allowed = ", ".join(f"'{value}'" for value in enum_cls.values())
    return f"check ({column} in ({allowed}))"


def all_state_enums() -> Iterable[type[CurisState]]:
    """返回全部业务状态枚举，供自检与文档生成使用。"""
    return (
        EvidenceGrade,
        BusinessLifecycle,
        CommitmentStatus,
        WorkspaceStatus,
        WorkItemStatus,
        CadenceStatus,
        RunStatus,
        EvidenceAdoption,
        AllocationStatus,
        FoundingRunStatus,
        CEOAssistantStatus,
        AIEmployeeStatus,
        PresenceState,
        RoleSlotStatus,
        CapabilityBindingStatus,
        CycleStatus,
        HandoffStatus,
        DecisionPacketStatus,
        AcceptanceStatus,
        VerificationStatus,
        EvidenceCondition,
        ExceptionStatus,
        SimulationStatus,
        SimulationPassStatus,
        ContentStatus,
        InteractionStatus,
    )
