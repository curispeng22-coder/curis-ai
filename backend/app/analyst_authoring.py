"""CEO-triggered Operating Intelligence analyst report authoring.

The service resolves the canonical Company Analyst Holder, executes the report
through the Analyst's enabled capability binding via the injected task runner
(production = Orchestrator.run), strictly validates the output contract, and
persists an ``analysis_report`` artifact consumed by the existing read-only
projection and the P7 report-decision chain. It never produces operating data
itself: the grounding prompt only assembles the existing projection truth.
"""

from __future__ import annotations

import json
from typing import Any, Callable
from uuid import uuid4

from .database import Database
from .employee_execution_identity import EmployeeExecutionIdentity
from .evolution_event_log import EvolutionEventLog
from .operating_intelligence import PROVENANCE, OperatingIntelligence
from .organization_projection import department_assignments
from .result_store import ResultStore
from .runtime import RuntimeFoundation, RuntimeScopeError
from .tenant_context import TenantContext

ANALYST_RESPONSIBILITY_KEY = "data.analytics.company_analysis"
AUTHORING_SOURCE_REF = "operating-analysis:authoring"
REPORT_REQUIRED_KEYS = {
    "scope", "period", "facts", "analysis", "unknown",
    "recommendation", "evidenceRefs", "author", "createdAt",
}
DECISION_REQUIRED_KEYS = (
    "event", "cannotDecideReason", "options", "recommendation",
    "recommendationReason", "ceoChoicePrompt", "continuationPlan",
)


class AnalystAuthoring:
    """Bounded authoring service; persisted truth stays in existing stores."""

    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.identities = EmployeeExecutionIdentity(database)
        self.event_log = EvolutionEventLog(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def author_report(
        self,
        company_id: str,
        *,
        business_id: str | None = None,
        days: int = 30,
        idempotency_key: str | None = None,
        task_runner: Callable[[str], Any],
    ) -> dict[str, Any]:
        self.foundation._require_company(company_id)
        key = (idempotency_key or "").strip()
        if idempotency_key is not None and not key:
            raise ValueError("Idempotency-Key 不能为空")
        if len(key) > 128:
            raise ValueError("Idempotency-Key 过长")
        source_ref = f"{AUTHORING_SOURCE_REF}:{key}" if key else AUTHORING_SOURCE_REF
        if key:
            replay = self._find_artifact(company_id, source_ref)
            if replay is not None:
                return replay
        projection = OperatingIntelligence(self.db).read(
            company_id, days=days, business_id=business_id,
        )
        analyst = self._resolve_analyst(company_id)
        binding = self._resolve_binding(analyst["id"])
        workspace_id = self._resolve_workspace(company_id, business_id)
        known_refs = self._known_refs(company_id)
        prompt = self._grounding_prompt(projection, analyst, known_refs)
        work_ref, execution_ref = self._create_work(company_id, workspace_id, analyst, projection)
        store = ResultStore(self.db)
        task = store.create_task(
            prompt,
            company_id=company_id,
            workspace_id=workspace_id,
            work_ref=work_ref,
            execution_ref=execution_ref,
            capability_source=binding["capability_source"],
            capability_type=binding["capability_type"],
            capability_id=binding["capability_id"],
            employee_id=analyst["id"],
            employee_role=str(analyst.get("role") or ""),
            employee_name=str(analyst.get("name") or ""),
        )
        self._bind_task(company_id, workspace_id, work_ref, execution_ref, analyst, binding, task)
        try:
            task_runner(task["task_id"])
        except Exception as error:
            raise ValueError(f"公司经营分析师执行失败：{error}") from error
        task = store.get_task(task["task_id"])
        if task["status"] != "COMPLETED":
            detail = str(task.get("error") or "").strip()
            raise ValueError(
                f"公司经营分析师执行未完成（{task['status']}）" + (f"：{detail}" if detail else "")
            )
        report = self._parse_and_validate(
            task["output"],
            company_id=company_id,
            business_id=business_id,
            days=days,
            analyst=analyst,
            known_refs=known_refs,
        )
        artifact = store.save_artifact(
            task["task_id"],
            title=f"经营分析报告 · {projection['scope']['name']} · 近{days}天",
            content=json.dumps(report, ensure_ascii=False),
            source_ref=source_ref,
            artifact_type="analysis_report",
        )
        return {"artifact": artifact, "task": task, "report": report, "replay": False}

    def _find_artifact(self, company_id: str, source_ref: str) -> dict[str, Any] | None:
        with self.db.connect() as connection:
            row = connection.execute(
                "select a.* from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                "where a.tenant_id=? and t.company_id=? and a.artifact_type='analysis_report' and a.source_ref=?",
                (self.tenant_id, company_id, source_ref),
            ).fetchone()
        if row is None:
            return None
        artifact = dict(row)
        store = ResultStore(self.db)
        return {
            "artifact": artifact,
            "task": store.get_task(artifact["task_id"]),
            "report": _loads(artifact["content"]),
            "replay": True,
        }

    def _resolve_analyst(self, company_id: str) -> dict[str, Any]:
        matches = [
            assignment
            for assignment in department_assignments(self.db, company_id)
            if assignment["data"].get("responsibilityKey") == ANALYST_RESPONSIBILITY_KEY
        ]
        analyst_refs = {assignment["data"]["companyEmployeeRef"] for assignment in matches}
        if len(analyst_refs) != 1:
            raise ValueError(
                "公司经营分析责任缺少唯一 Holder（当前 "
                f"{len(analyst_refs)} 个），请先在组织中指派唯一公司经营分析师"
            )
        employee_id = next(iter(analyst_refs))
        assignment = next(item for item in matches if item["data"]["companyEmployeeRef"] == employee_id)
        with self.db.connect() as connection:
            row = connection.execute(
                "select id, name, role, status from employee_instances "
                "where tenant_id=? and company_id=? and id=? and enabled=1 and deleted_at is null",
                (self.tenant_id, company_id, employee_id),
            ).fetchone()
        if row is None:
            raise ValueError("公司经营分析师员工不存在或已停用")
        return {
            **dict(row),
            "runtime_employee_ref": assignment["data"]["employeeRef"],
            "assignment_ref": assignment["entity_id"],
        }

    def _resolve_binding(self, employee_id: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "select id, capability_source, capability_type, capability_id, priority "
                "from employee_capability_bindings "
                "where tenant_id=? and employee_id=? and enabled=1 "
                "and capability_type in ('model','agent') "
                "and capability_source in ('official','tenant_private') "
                "order by priority, id",
                (self.tenant_id, employee_id),
            ).fetchall()
        if not rows:
            raise ValueError("公司经营分析师没有已启用的 model/agent 能力绑定")
        binding = dict(rows[0])
        capability_id = binding["capability_id"]
        if binding["capability_source"] == "official":
            if binding["capability_type"] != "model":
                raise ValueError("公司经营分析师绑定的 official 非 model 能力不支持报告撰写")
            if self.db.get_active_official_model(capability_id) is None:
                raise ValueError(f"公司经营分析师绑定的官方模型能力不可用（{capability_id}）")
            return binding
        capability = self.db.get_tenant_private_capability(
            self.tenant_id, binding["capability_type"], capability_id,
        )
        if capability is None or capability.get("status") != "active":
            raise ValueError(f"公司经营分析师绑定的私有能力不可用（{capability_id}）")
        return binding

    def _resolve_workspace(self, company_id: str, business_id: str | None) -> str:
        with self.db.connect() as connection:
            if business_id:
                row = connection.execute(
                    "select workspace_id from workspaces "
                    "where tenant_id=? and company_id=? and business_id=? "
                    "and business_relation_status='RESOLVED' order by created_at, workspace_id",
                    (self.tenant_id, company_id, business_id),
                ).fetchone()
            else:
                # A report always has a concrete execution home (the accepted P7
                # chain requires workspace provenance); Company-scope reports use
                # the Company's first resolved workspace, deterministically.
                row = connection.execute(
                    "select workspace_id from workspaces "
                    "where tenant_id=? and company_id=? "
                    "and business_relation_status='RESOLVED' order by created_at, workspace_id",
                    (self.tenant_id, company_id),
                ).fetchone()
        if row is None:
            if business_id:
                raise ValueError("目标业务没有已归属的工作空间，报告无法落位")
            raise ValueError("公司还没有已归属的工作空间，经营分析师无处执行")
        return row["workspace_id"]

    def _create_work(
        self,
        company_id: str,
        workspace_id: str,
        analyst: dict[str, Any],
        projection: dict[str, Any],
    ) -> tuple[str, str]:
        # RuntimeFoundation.create has no WORK state machine; canonical child_work
        # inserts WORK rows directly. This Work is the execution-attribution home
        # required by the canonical usage lineage (no Cycle is involved here).
        self.foundation._require_workspace(workspace_id, company_id)
        work_ref = f"work-{uuid4().hex[:16]}"
        data = {
            "kind": "OPERATING_ANALYSIS_AUTHORING",
            "version": 1,
            "problem": f"撰写{projection['scope']['name']}经营分析报告",
            "expectedResult": "通过报告契约校验并落库为 analysis_report artifact",
            "responsibilityRouting": {
                "responsibilityHolderRef": analyst["runtime_employee_ref"],
                "currentAssignmentRef": analyst["assignment_ref"],
            },
        }
        with self.db.connect() as connection:
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, "
                "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, "
                "created_at, updated_at) "
                "values (?, ?, 'WORK', ?, ?, ?, 'PLANNED', 'UNVERIFIED', 'MISSING', ?, "
                "current_timestamp, current_timestamp)",
                (work_ref, self.tenant_id, company_id, workspace_id, analyst["id"], json.dumps(data, ensure_ascii=False)),
            )
        return work_ref, f"operating-analysis:{uuid4().hex[:16]}"

    def _bind_task(
        self,
        company_id: str,
        workspace_id: str,
        work_ref: str,
        execution_ref: str,
        analyst: dict[str, Any],
        binding: dict[str, Any],
        task: dict[str, Any],
    ) -> None:
        identity = self.identities.resolve(
            company_id=company_id, workspace_id=workspace_id,
            runtime_employee_ref=analyst["runtime_employee_ref"],
        )
        if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
            self.identities.bind(
                company_id=company_id, workspace_id=workspace_id,
                runtime_employee_ref=analyst["runtime_employee_ref"],
                company_employee_ref=analyst["id"],
                employee_capability_binding_ref=binding["id"],
            )
        self.identities.record_task_assignment(
            company_id=company_id, workspace_id=workspace_id,
            runtime_employee_ref=analyst["runtime_employee_ref"],
            task_ref=task["task_id"],
            employee_capability_binding_ref=binding["id"],
        )
        self.event_log.record(
            correlation_id=work_ref,
            event_type="team.execution_task_bound",
            payload={"work_ref": work_ref, "execution_key": execution_ref, "task_ref": task["task_id"]},
            idempotency_key=f"team-execution-task:{self.tenant_id}:{execution_ref}",
        )

    def _known_refs(self, company_id: str) -> set[str]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "select usage_record_id as ref from ai_usage_records where tenant_id=? and company_id=? "
                "union select entity_id as ref from runtime_entities where tenant_id=? and company_id=? and entity_type='EVIDENCE' "
                "union select a.artifact_id as ref from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                "where a.tenant_id=? and t.company_id=?",
                (self.tenant_id, company_id, self.tenant_id, company_id, self.tenant_id, company_id),
            ).fetchall()
        return {row["ref"] for row in rows}

    @staticmethod
    def _grounding_prompt(
        projection: dict[str, Any], analyst: dict[str, Any], known_refs: set[str],
    ) -> str:
        metrics = [
            {
                "key": item["key"], "label": item["label"], "value": item["value"],
                "unit": item["unit"], "verification": item["verification"],
                "unknown_reason": item["unknown_reason"], "source_refs": item["source_refs"],
                "sample_size": item["sample_size"], "baseline": item.get("baseline"),
                "comparison": item.get("comparison"),
            }
            for item in projection["metrics"]
        ]
        grounding = {
            "company": projection["company"],
            "scope": projection["scope"],
            "scopes": projection["scopes"],
            "time_range": projection["time_range"],
            "metrics": metrics,
            "benchmark": projection["benchmark"],
            "trust": projection["trust"],
        }
        contract = {
            "scope": {"type": projection["scope"]["type"], "ref": projection["scope"]["ref"]},
            "period": {"days": projection["time_range"]["days"]},
            "facts": [{"value": "事实条目", "provenance": "FACT|POLICY|EVIDENCE|EST|UNK"}],
            "analysis": [{"value": "解读条目", "provenance": "同上枚举"}],
            "unknown": [{"value": "未知条目（无未知项时给空列表）", "provenance": "同上枚举"}],
            "recommendation": {"value": "建议", "provenance": "同上枚举"},
            "evidenceRefs": ["必须非空且全部来自下方允许引用清单"],
            "author": {"employeeRef": analyst["id"], "name": analyst["name"]},
            "createdAt": "ISO8601 时间",
            "decisionCandidate": {
                "说明": "可选；仅当事实足以形成需要 CEO 拍板的经营取舍时给出",
                "event": "...", "cannotDecideReason": "...",
                "options": [
                    {"optionId": "...", "label": "...",
                     "impact": {"value": "...", "provenance": "同上枚举"},
                     "risk": {"value": "...", "provenance": "同上枚举"},
                     "cost": {"value": "...", "provenance": "同上枚举"}}
                ],
                "recommendation": {"optionId": "必须属于 options", "provenance": "同上枚举"},
                "recommendationReason": {"value": "...", "provenance": "同上枚举"},
                "ceoChoicePrompt": "...", "continuationPlan": "...",
                "约束": "options 必须 2-4 个",
            },
        }
        return (
            "你是本公司的公司经营分析师，请仅基于下方已核实的经营投影事实撰写经营分析报告。\n"
            "禁止编造任何投影之外的事实；未知就是未知。\n\n"
            f"经营投影事实（JSON）：\n{json.dumps(grounding, ensure_ascii=False)}\n\n"
            f"允许引用的证据 ref 清单（evidenceRefs 只能取这里的值）：\n{json.dumps(sorted(known_refs), ensure_ascii=False)}\n\n"
            f"输出契约（只输出一个 JSON 对象，不要输出任何其他文字）：\n{json.dumps(contract, ensure_ascii=False)}\n\n"
            "scope 与 period 必须原样回显给定值；author.employeeRef 必须原样回显。"
        )

    def _parse_and_validate(
        self,
        output: str,
        *,
        company_id: str,
        business_id: str | None,
        days: int,
        analyst: dict[str, Any],
        known_refs: set[str],
    ) -> dict[str, Any]:
        report = _parse_json_object(output)
        missing = REPORT_REQUIRED_KEYS - set(report)
        if missing:
            raise ValueError(f"报告缺少必填键：{', '.join(sorted(missing))}")
        expected_scope = {
            "type": "BUSINESS" if business_id else "COMPANY",
            "ref": business_id or company_id,
        }
        scope = report["scope"]
        if (
            not isinstance(scope, dict)
            or scope.get("type") != expected_scope["type"]
            or str(scope.get("ref") or "") != expected_scope["ref"]
        ):
            raise ValueError("报告 scope 与触发范围不一致")
        period = report["period"]
        try:
            period_days = int(period.get("days")) if isinstance(period, dict) else None
        except (TypeError, ValueError):
            period_days = None
        if period_days != days:
            raise ValueError("报告 period 与触发周期不一致")
        _validate_entries(report["facts"], "facts", allow_empty=False)
        _validate_entries(report["analysis"], "analysis", allow_empty=False)
        _validate_entries(report["unknown"], "unknown", allow_empty=True)
        recommendation = report["recommendation"]
        if (
            not isinstance(recommendation, dict)
            or not str(recommendation.get("value") or "").strip()
            or recommendation.get("provenance") not in PROVENANCE
        ):
            raise ValueError("报告 recommendation 必须包含 value 与合法 provenance")
        refs = report["evidenceRefs"]
        if not isinstance(refs, list) or not refs or any(not str(ref).strip() for ref in refs):
            raise ValueError("报告 evidenceRefs 必须是非空引用列表")
        refs = [str(ref) for ref in refs]
        if any(ref not in known_refs for ref in refs):
            raise RuntimeScopeError("Report evidence is not in the current Company")
        author = report["author"]
        if not isinstance(author, dict) or str(author.get("employeeRef") or "") != analyst["id"]:
            raise ValueError("报告 author 必须是当前公司经营分析师")
        if not str(report.get("createdAt") or "").strip():
            raise ValueError("报告缺少 createdAt")
        _check_provenance(report)
        candidate = report.get("decisionCandidate")
        if candidate is not None:
            _validate_decision_candidate(candidate)
        return report


def _loads(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _parse_json_object(output: str) -> dict[str, Any]:
    text = (output or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError("公司经营分析师输出不是合法 JSON") from error
    if not isinstance(parsed, dict):
        raise ValueError("公司经营分析师输出必须是 JSON 对象")
    return parsed


def _validate_entries(value: Any, name: str, *, allow_empty: bool) -> None:
    if not isinstance(value, list) or (not value and not allow_empty):
        requirement = "条目列表" if allow_empty else "非空条目列表"
        raise ValueError(f"报告 {name} 必须是{requirement}")
    for item in value:
        if (
            not isinstance(item, dict)
            or not str(item.get("value") or "").strip()
            or item.get("provenance") not in PROVENANCE
        ):
            raise ValueError(f"报告 {name} 条目必须包含 value 与合法 provenance")


def _check_provenance(node: Any) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "provenance" and value not in PROVENANCE:
                raise ValueError(f"报告 provenance 非法：{value!r}")
            _check_provenance(value)
    elif isinstance(node, list):
        for item in node:
            _check_provenance(item)


def _validate_decision_candidate(candidate: Any) -> None:
    """Same-level validation as the accepted P7 report-decision chain."""
    if not isinstance(candidate, dict):
        raise ValueError("Report has no decision candidate")
    if not all(candidate.get(key) for key in DECISION_REQUIRED_KEYS):
        raise ValueError("Report decision candidate is incomplete")
    options = candidate["options"]
    if not isinstance(options, list) or not 2 <= len(options) <= 4:
        raise ValueError("Report decision requires two to four options")
    for option in options:
        if not isinstance(option, dict) or not all(
            option.get(key) for key in ("optionId", "label", "impact", "risk", "cost")
        ):
            raise ValueError("Report decision option is incomplete")
        for key in ("impact", "risk", "cost"):
            if (
                not isinstance(option[key], dict)
                or option[key].get("provenance") not in PROVENANCE
                or not str(option[key].get("value") or "").strip()
            ):
                raise ValueError("Report decision provenance is invalid")
    recommendation = candidate["recommendation"]
    reason = candidate["recommendationReason"]
    option_ids = {str(option["optionId"]) for option in options}
    if (
        not isinstance(recommendation, dict)
        or recommendation.get("provenance") not in PROVENANCE
        or str(recommendation.get("optionId") or "") not in option_ids
        or not isinstance(reason, dict)
        or reason.get("provenance") not in PROVENANCE
        or not str(reason.get("value") or "").strip()
    ):
        raise ValueError("Report recommendation provenance is invalid")
