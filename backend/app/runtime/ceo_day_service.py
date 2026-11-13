"""Curis Business Runtime —— 「CEO 的一天」闭环编排（第 2 步）。

把 BusinessDirection / Commitment / Workspace / Cadence / ScheduledRun /
Outcome / Attribution 串成一条可端到端验收的真实经营闭环。

铁律（A1 契约 §1.1）：
- 所有 5 个注册对象（business_direction / commitment / workspace / cadence /
  scheduled_run）的状态列更新**只允许**走 ``runtime_registry`` 状态机，
  由 :meth:`_transition` 统一执行；禁止业务代码直写 status。
- Cadence / ScheduledRun 的执行与升级闭环委托 :class:`RuntimeScheduler`（A2）。
- Outcome / Attribution 的 attribution_status 不在注册表内（v0.1），以带
  校验的列更新管理（权重合计必须 = 100% 才能 REVIEWED）。
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from ..database import Database
from .models import ensure_ceo_day_schema
from .registry import runtime_registry
from .scheduler import RuntimeScheduler, SimulatedExecutor
from .states import Actor, EvidenceGrade
from .store import init_transition_log


class CeoDayService:
    """闭环编排服务。"""

    def __init__(
        self,
        database: Database,
        scheduler: RuntimeScheduler | None = None,
    ) -> None:
        self._db = database
        ensure_ceo_day_schema(database)
        init_transition_log(database)  # 挂全局 recorder（状态机留痕）
        self._scheduler = scheduler or RuntimeScheduler(
            database, SimulatedExecutor()
        )

    # -- 通用流转（5 个注册对象共用）---------------------------------------

    def _get_status(
        self, table: str, id_col: str, entity_id: str, status_col: str
    ) -> str:
        with self._db.connect() as conn:
            row = conn.execute(
                f"select {status_col} as s from {table} where {id_col} = ?",
                (entity_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"{table} 记录不存在：{entity_id}")
        return str(row["s"])

    def _transition(
        self,
        entity_type: str,
        table: str,
        id_col: str,
        entity_id: str,
        dst: str,
        *,
        actor: Actor,
        trigger: str,
        guard_ctx: Mapping[str, Any] | None = None,
        status_col: str = "status",
    ) -> str:
        src = self._get_status(table, id_col, entity_id, status_col)
        rec = runtime_registry.get(entity_type).transition(
            entity_id, src, dst,
            actor=actor, trigger=trigger, context=dict(guard_ctx or {}),
        )
        with self._db.connect() as conn:
            conn.execute(
                f"update {table} set {status_col} = ?, updated_at = current_timestamp "
                f"where {id_col} = ?",
                (rec.target, entity_id),
            )
        return rec.target

    # -- BusinessDirection ---------------------------------------------------

    def create_business_direction(
        self, *, name: str, template_type: str, opportunity: str,
        target_outcome: str, timebox_days: int = 30, evidence_route: str = "",
    ) -> str:
        import uuid
        did = uuid.uuid4().hex
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into business_directions
                  (direction_id, name, template_type, opportunity, target_outcome,
                   timebox_days, evidence_route, lifecycle_status, verification_status)
                values (?, ?, ?, ?, ?, ?, ?, 'DRAFT', 'UNVERIFIED')
                """,
                (did, name, template_type, opportunity, target_outcome,
                 timebox_days, evidence_route),
            )
        return did

    def submit_direction_brief(self, direction_id: str) -> str:
        return self._transition(
            "business_direction", "business_directions", "direction_id",
            direction_id, "PENDING_APPROVAL", actor=Actor.CEO,
            trigger="brief_complete", status_col="lifecycle_status",
        )

    def approve_direction(self, direction_id: str, *, authorized: bool) -> str:
        """勾选授权才能启动；未授权被守卫拒绝（硬门禁）。"""
        return self._transition(
            "business_direction", "business_directions", "direction_id",
            direction_id, "ACTIVE", actor=Actor.CEO, trigger="approve_team",
            guard_ctx={"authorized": authorized}, status_col="lifecycle_status",
        )

    def continue_direction_cycle(self, direction_id: str) -> str:
        return self._transition(
            "business_direction", "business_directions", "direction_id",
            direction_id, "ACTIVE", actor=Actor.CEO, trigger="continue_cycle",
            status_col="lifecycle_status",
        )

    def scale_direction(self, direction_id: str) -> str:
        """仅当 verificationStatus == VERIFIED 才允许（守卫）。"""
        return self._transition(
            "business_direction", "business_directions", "direction_id",
            direction_id, "SCALING", actor=Actor.CEO, trigger="scale_up",
            guard_ctx={"verificationStatus": self._get_status(
                "business_directions", "direction_id", direction_id,
                "verification_status")},
            status_col="lifecycle_status",
        )

    def set_direction_verification(self, direction_id: str, grade: str) -> None:
        """维度二：验证结论字段（不进状态机，单独维护）。"""
        value = EvidenceGrade(grade).value
        with self._db.connect() as conn:
            conn.execute(
                "update business_directions set verification_status = ?, "
                "updated_at = current_timestamp where direction_id = ?",
                (value, direction_id),
            )

    def get_direction(self, direction_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from business_directions where direction_id = ?",
                (direction_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"业务方向不存在：{direction_id}")
        return dict(row)

    # -- Commitment ----------------------------------------------------------

    def create_commitment(
        self, business_id: str, *, department_name: str, name: str,
        target_outcome: str, capacity_contract: Mapping[str, Any] | None = None,
    ) -> str:
        import uuid
        cid = uuid.uuid4().hex
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into commitments
                  (commitment_id, business_id, department_name, name,
                   target_outcome, status, cycle, capacity_contract_json)
                values (?, ?, ?, ?, ?, 'PENDING', 1, ?)
                """,
                (cid, business_id, department_name, name, target_outcome,
                 _json(capacity_contract or {})),
            )
        return cid

    def report_commitment_first_result(self, commitment_id: str) -> str:
        """AI 员工回报首条真实结果，PENDING → ACTIVE。"""
        return self._transition(
            "commitment", "commitments", "commitment_id", commitment_id,
            "ACTIVE", actor=Actor.AI_EMPLOYEE, trigger="first_result_reported",
        )

    def continue_commitment(self, commitment_id: str) -> str:
        return self._transition(
            "commitment", "commitments", "commitment_id", commitment_id,
            "ACTIVE", actor=Actor.CEO, trigger="continue_cycle",
        )

    def fulfill_commitment(self, commitment_id: str, *, verification_status: str) -> str:
        """目标达成且 verificationStatus == VERIFIED 才能收尾（守卫）。"""
        return self._transition(
            "commitment", "commitments", "commitment_id", commitment_id,
            "FULFILLED", actor=Actor.CEO, trigger="fulfill",
            guard_ctx={"verificationStatus": verification_status},
        )

    def release_commitment(self, commitment_id: str) -> str:
        return self._transition(
            "commitment", "commitments", "commitment_id", commitment_id,
            "RELEASED", actor=Actor.SYSTEM, trigger="release_on_archive",
        )

    def get_commitment(self, commitment_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from commitments where commitment_id = ?",
                (commitment_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"承诺不存在：{commitment_id}")
        return dict(row)

    # -- Workspace（装修流水线 + 三级门禁）-----------------------------------

    def create_workspace(self, business_id: str, *, name: str) -> str:
        import uuid
        wid = uuid.uuid4().hex
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into workspaces
                  (workspace_id, business_id, name, status)
                values (?, ?, ?, 'DRAFT')
                """,
                (wid, business_id, name),
            )
        return wid

    def _set_workspace_flags(
        self, workspace_id: str, *, simulation_passed: int,
        issues_resolved: int, external_agent_reviewed: int,
    ) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """
                update workspaces
                  set simulation_passed = ?, issues_resolved = ?,
                      external_agent_reviewed = ?, updated_at = current_timestamp
                where workspace_id = ?
                """,
                (simulation_passed, issues_resolved, external_agent_reviewed,
                 workspace_id),
            )

    def start_blueprint(self, workspace_id: str) -> str:
        return self._transition(
            "workspace", "workspaces", "workspace_id", workspace_id,
            "BLUEPRINTING", actor=Actor.CEO, trigger="start_blueprint",
        )

    def pass_simulation(self, workspace_id: str) -> str:
        self._set_workspace_flags(workspace_id, simulation_passed=1,
                                  issues_resolved=0, external_agent_reviewed=0)
        return self._transition(
            "workspace", "workspaces", "workspace_id", workspace_id,
            "SIMULATED", actor=Actor.CEO, trigger="simulation_passed",
            guard_ctx={"simulationPassed": True},
        )

    def submit_workspace_for_approval(
        self, workspace_id: str, *, issues_resolved: bool,
        external_agent_reviewed: bool,
    ) -> str:
        self._set_workspace_flags(
            workspace_id, simulation_passed=1,
            issues_resolved=1 if issues_resolved else 0,
            external_agent_reviewed=1 if external_agent_reviewed else 0,
        )
        return self._transition(
            "workspace", "workspaces", "workspace_id", workspace_id,
            "PENDING_APPROVAL", actor=Actor.CEO, trigger="submit_for_approval",
            guard_ctx={
                "issuesResolved": issues_resolved,
                "simulationPassed": True,
                "externalAgentReviewed": external_agent_reviewed,
            },
        )

    def approve_and_launch_workspace(self, workspace_id: str) -> str:
        return self._transition(
            "workspace", "workspaces", "workspace_id", workspace_id,
            "OPERATING", actor=Actor.CEO, trigger="approve_and_launch",
        )

    def get_workspace(self, workspace_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from workspaces where workspace_id = ?",
                (workspace_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"工作空间不存在：{workspace_id}")
        return dict(row)

    # -- Cadence / ScheduledRun（委托 scheduler）-----------------------------

    def create_cadence(self, business_id: str, name: str, schedule_text: str,
                       **kw: Any) -> str:
        return self._scheduler.create_cadence(
            business_id, name, schedule_text, **kw)

    def enable_cadence(self, cadence_id: str, **kw: Any) -> None:
        self._scheduler.enable_cadence(cadence_id, **kw)

    def fire_due_runs(self, now=None) -> list[str]:
        return self._scheduler.run_once(now)

    def ceo_open_run(self, run_id: str) -> None:
        self._scheduler.ceo_open(run_id)

    def ceo_resolve_run(self, run_id: str, *, reason: str = "") -> None:
        self._scheduler.ceo_resolve(run_id, reason=reason)

    def get_run(self, run_id: str) -> dict[str, Any]:
        return self._scheduler._get_run(run_id)

    def run_history(self, run_id: str) -> list[dict[str, Any]]:
        return self._scheduler.history(run_id)

    # -- Outcome + Attribution（闭环收口）-----------------------------------

    def record_outcome(
        self, business_id: str, *, run_id: str | None = None,
        commitment_id: str | None = None, route: str = "", value: float = 0.0,
        evidence_grade: str = "UNVERIFIED", source: str = "",
        evidence_ref: str = "", evidence_type: str = "",
        contributors: Sequence[Mapping[str, Any]] | None = None,
    ) -> str:
        import uuid
        oid = uuid.uuid4().hex
        grade = EvidenceGrade(evidence_grade).value
        with self._db.connect() as conn:
            conn.execute(
                """
                insert into outcomes
                  (outcome_id, business_id, commitment_id, run_id, route, value,
                   evidence_grade, source, evidence_ref, evidence_type,
                   attribution_status)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_REVIEW')
                """,
                (oid, business_id, commitment_id, run_id, route, value,
                 grade, source, evidence_ref, evidence_type),
            )
            for c in (contributors or []):
                conn.execute(
                    """
                    insert into attributions
                      (attribution_id, outcome_id, agent, model, skills_json,
                       tools_json, weight)
                    values (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (uuid.uuid4().hex, oid, c.get("agent", ""),
                     c.get("model", ""), _json(c.get("skills", []) or []),
                     _json(c.get("tools", []) or []), float(c.get("weight", 0))),
                )
        return oid

    def confirm_attribution(self, outcome_id: str) -> None:
        """CEO 确认贡献权重；合计必须 = 100%，否则拒绝（硬规则）。"""
        rows: list[dict[str, Any]] = []
        with self._db.connect() as conn:
            rows = list(conn.execute(
                "select weight from attributions where outcome_id = ?",
                (outcome_id,),
            ).fetchall())
        total = sum(float(r["weight"]) for r in rows)
        if abs(total - 100.0) > 1e-6:
            raise ValueError(
                f"贡献权重合计 {total}%，必须等于 100% 才能确认（当前 {len(rows)} 条）"
            )
        with self._db.connect() as conn:
            conn.execute(
                "update outcomes set attribution_status = 'REVIEWED', "
                "updated_at = current_timestamp where outcome_id = ?",
                (outcome_id,),
            )

    def get_outcome(self, outcome_id: str) -> dict[str, Any]:
        with self._db.connect() as conn:
            row = conn.execute(
                "select * from outcomes where outcome_id = ?", (outcome_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"成果不存在：{outcome_id}")
        return dict(row)


def _json(obj: Any) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False)
