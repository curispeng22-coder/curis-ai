"""Curis Business Runtime —— 统一状态机引擎。

依据：``docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md`` §1.1

契约（四条，全部强制）
----------------------
1. 状态值必须来自 :mod:`app.runtime.states` 的集中枚举，不允许裸字符串。
2. 流转必须走 :meth:`StateMachine.transition`，禁止直接 ``UPDATE ... SET status``。
3. 非法流转必须被拒绝并报错，不允许静默写入。
4. 每次流转必须留痕：``from / to / trigger / actor / at / reason``。

引擎本身是纯逻辑，不碰数据库，因此可以脱离 FastAPI 与 sqlite 单测。
持久化由 :mod:`app.runtime.store` 提供，通过 ``recorder`` 注入。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

from .states import Actor, CurisState, normalize

#: 守卫函数签名：返回 ``None`` 表示放行，返回字符串表示拒绝原因。
Guard = Callable[[Mapping[str, Any]], "str | None"]


class TransitionError(RuntimeError):
    """状态流转被拒绝的基类。"""


class IllegalTransitionError(TransitionError):
    """目标状态不在合法流转表中。"""


class GuardRejectedError(TransitionError):
    """流转在语义上被守卫条件拒绝（路径合法但业务条件不满足）。"""


class ActorNotAllowedError(TransitionError):
    """该触发者无权执行这次流转。"""


class TerminalStateError(TransitionError):
    """试图从终态继续流转。"""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Transition:
    """一条合法流转的声明。"""

    source: str
    target: str
    trigger: str
    actors: frozenset[str] = frozenset()
    guard: Guard | None = None
    description: str = ""

    def allows(self, actor: str) -> bool:
        return not self.actors or actor in self.actors


@dataclass(frozen=True)
class TransitionRecord:
    """一次成功流转的留痕。"""

    entity_type: str
    entity_id: str
    source: str
    target: str
    trigger: str
    actor: str
    at: str
    reason: str = ""
    context: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "source": self.source,
            "target": self.target,
            "trigger": self.trigger,
            "actor": self.actor,
            "at": self.at,
            "reason": self.reason,
            "context": dict(self.context),
        }


class TransitionRecorder(Protocol):
    """流转留痕接收方。"""

    def record(self, record: TransitionRecord) -> None:  # pragma: no cover - 协议
        ...


class StateMachine:
    """某一类业务对象的状态机。

    用法::

        machine = StateMachine(
            entity_type="run",
            states=RunStatus,
            initial=[RunStatus.QUEUED, RunStatus.RUNNING],
            terminal=[RunStatus.COMPLETED, RunStatus.RESOLVED],
            transitions=[...],
        )
        record = machine.transition("run-1", RunStatus.RUNNING,
                                    RunStatus.COMPLETED,
                                    actor=Actor.SYSTEM, trigger="execution_finished")
    """

    def __init__(
        self,
        *,
        entity_type: str,
        states: type[CurisState],
        transitions: Sequence[Transition],
        initial: Sequence[CurisState] | None = None,
        terminal: Sequence[CurisState] | None = None,
        recorder: TransitionRecorder | None = None,
    ) -> None:
        self.entity_type = entity_type
        self.states = states
        self.initial = tuple(initial or ())
        self.terminal = frozenset(state.value for state in (terminal or ()))
        self.recorder = recorder
        self._transitions: dict[tuple[str, str], Transition] = {}

        for transition in transitions:
            self._register(transition)

    # -- 注册与校验 ---------------------------------------------------------

    def _register(self, transition: Transition) -> None:
        source = normalize(self.states, transition.source).value
        target = normalize(self.states, transition.target).value
        key = (source, target)
        if key in self._transitions:
            raise ValueError(
                f"{self.entity_type}: 重复声明流转 {source} → {target}"
            )
        self._transitions[key] = Transition(
            source=source,
            target=target,
            trigger=transition.trigger,
            actors=transition.actors,
            guard=transition.guard,
            description=transition.description,
        )

    def is_terminal(self, state: str | CurisState) -> bool:
        return normalize(self.states, state).value in self.terminal

    def can(self, source: str | CurisState, target: str | CurisState) -> bool:
        """仅检查路径是否声明过，不执行守卫。"""
        src = normalize(self.states, source).value
        dst = normalize(self.states, target).value
        return (src, dst) in self._transitions

    def allowed_targets(self, source: str | CurisState) -> tuple[str, ...]:
        """列出从当前状态出发的全部合法目标，供界面渲染可用动作。"""
        src = normalize(self.states, source).value
        return tuple(
            target for (candidate, target) in self._transitions if candidate == src
        )

    def describe(self) -> list[dict[str, Any]]:
        """导出流转表，供文档生成与前端可视化。"""
        return [
            {
                "source": transition.source,
                "target": transition.target,
                "trigger": transition.trigger,
                "actors": sorted(transition.actors) or ["*"],
                "description": transition.description,
            }
            for transition in self._transitions.values()
        ]

    # -- 执行 ---------------------------------------------------------------

    def transition(
        self,
        entity_id: str,
        source: str | CurisState,
        target: str | CurisState,
        *,
        actor: Actor | str,
        trigger: str = "",
        reason: str = "",
        context: Mapping[str, Any] | None = None,
        record: bool = True,
    ) -> TransitionRecord:
        """执行一次流转。

        校验顺序：状态收敛 → 终态检查 → 路径合法性 → 触发者权限 → 守卫条件。
        任一不过即抛异常，绝不静默写入。
        """
        src = normalize(self.states, source)
        dst = normalize(self.states, target)
        actor_value = actor.value if isinstance(actor, Actor) else str(actor)
        ctx: dict[str, Any] = dict(context or {})

        # 自环（src == dst）仅在显式声明时允许——例如业务方向的「继续下一周期」。
        # 未声明的自环会落入下方「路径合法性」检查被拒绝，不会静默放行。

        if self.is_terminal(src):
            raise TerminalStateError(
                f"{self.entity_type} {entity_id}: {src.value}（{src.label}）是终态，"
                f"不能再流转到 {dst.value}"
            )

        declared = self._transitions.get((src.value, dst.value))
        if declared is None:
            allowed = self.allowed_targets(src) or ("<无>",)
            raise IllegalTransitionError(
                f"{self.entity_type} {entity_id}: 非法流转 {src.value} → {dst.value}；"
                f"允许的目标：{', '.join(allowed)}"
            )

        if not declared.allows(actor_value):
            raise ActorNotAllowedError(
                f"{self.entity_type} {entity_id}: {actor_value} 无权执行 "
                f"{src.value} → {dst.value}；允许：{', '.join(sorted(declared.actors))}"
            )

        if declared.guard is not None:
            ctx.setdefault("entity_id", entity_id)
            ctx.setdefault("source", src.value)
            ctx.setdefault("target", dst.value)
            ctx.setdefault("actor", actor_value)
            rejection = declared.guard(ctx)
            if rejection:
                raise GuardRejectedError(
                    f"{self.entity_type} {entity_id}: {src.value} → {dst.value} 被拒绝——{rejection}"
                )

        result = TransitionRecord(
            entity_type=self.entity_type,
            entity_id=entity_id,
            source=src.value,
            target=dst.value,
            trigger=trigger or declared.trigger,
            actor=actor_value,
            at=_utcnow(),
            reason=reason,
            context=ctx,
        )

        if record and self.recorder is not None:
            self.recorder.record(result)
        return result


class StateMachineRegistry:
    """全局状态机注册表。

    调用方按 ``entity_type`` 取机器，而不是各自 new 一个——避免同一对象
    在不同模块被声明成两套不同的流转规则。
    """

    def __init__(self) -> None:
        self._machines: dict[str, StateMachine] = {}

    def register(self, machine: StateMachine) -> StateMachine:
        if machine.entity_type in self._machines:
            raise ValueError(f"状态机已注册：{machine.entity_type}")
        self._machines[machine.entity_type] = machine
        return machine

    def get(self, entity_type: str) -> StateMachine:
        try:
            return self._machines[entity_type]
        except KeyError:
            raise KeyError(
                f"未注册的状态机：{entity_type}；"
                f"已注册：{', '.join(sorted(self._machines))}"
            ) from None

    def all(self) -> Iterable[StateMachine]:
        return tuple(self._machines.values())

    def attach_recorder(self, recorder: TransitionRecorder) -> None:
        """为全部已注册状态机统一挂上留痕接收方。"""
        for machine in self._machines.values():
            machine.recorder = recorder
