from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from .database import Database
from .evolution_event_log import EvolutionEventLog
from .model_gateway import redact_model_gateway_text
from .tenant_context import TenantContext
from .agent_adapter import agent_stop_serialized


PAUSED_TASK_STATUSES = {"AWAITING_INPUT", "HUMAN_HANDOFF", "CANCELLED"}
RUNNING_TASK_STATUSES = {"PENDING", "PARSED", "RUNNING", "RESUMED"}
TIMELINE_EVENT_TYPES = {
    "execution_started",
    "capability_selected",
    "knowledge_retrieved",
    "tool_called",
    "awaiting_input",
    "input_supplied",
    "human_handoff_requested",
    "human_handoff_accepted",
    "human_handoff_reassigned",
    "execution_resumed",
    "execution_completed",
    "execution_failed",
    "execution_cancelled",
}


class ExecutionPaused(RuntimeError):
    pass


class AwaitingInputIn(BaseModel):
    current_step: str
    question: str
    context_summary: str
    responsible_id: str = ""
    resume_parameters: dict[str, Any] = Field(default_factory=dict)


class HandoffIn(BaseModel):
    current_step: str
    question: str
    context_summary: str
    assignee_id: str = ""
    resume_parameters: dict[str, Any] = Field(default_factory=dict)


class InputSupplyIn(BaseModel):
    input_summary: str
    resume_parameters: dict[str, Any] = Field(default_factory=dict)


class AssigneeIn(BaseModel):
    assignee_id: str


class ResumeIn(BaseModel):
    resume_parameters: dict[str, Any] = Field(default_factory=dict)


class CancelIn(BaseModel):
    reason: str = ""


class TaskExecutionControlService:
    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    def get_state(self, task_id: str) -> dict[str, Any]:
        task = self._task_context(task_id)
        return {
            "task_run_id": task_id,
            "task_id": task_id,
            "status": self._public_status(task["status"]),
            "task_status": task["status"],
            "current_step": task["current_execution_step"] or "",
            "pending_question": task["pending_question"] or "",
            "context_summary": task["execution_context_summary"] or "",
            "handoff_assignee_id": task["handoff_assignee_id"] or "",
            "resume_parameters_present": bool(
                json.loads(task["resume_parameters_json"] or "{}")
            ),
            "state_changed_at": task["execution_state_changed_at"],
        }

    def get_resume_parameters(self, task_id: str) -> dict[str, Any]:
        task = self._task_context(task_id)
        return json.loads(task["resume_parameters_json"] or "{}")

    def list_timeline(self, task_id: str) -> list[dict[str, Any]]:
        base = self._event_context(self._task_context(task_id))
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select * from evolution_events
                where tenant_id = ?
                  and (
                    correlation_id = ?
                    or json_extract(payload, '$.task_id') = ?
                  )
                order by event_id
                """,
                (tenant_id, task_id, task_id),
            ).fetchall()
            usage_records = {
                row["usage_record_id"]: dict(row)
                for row in connection.execute(
                    """
                    select * from ai_usage_records
                    where tenant_id = ? and task_id = ?
                    """,
                    (tenant_id, task_id),
                ).fetchall()
            }
        timeline: list[dict[str, Any]] = []
        seen_usage_records: set[str] = set()
        for row in rows:
            event_type = str(row["event_type"])
            payload = json.loads(row["payload"])
            if event_type == "usage.model_call":
                usage_record_id = str(payload.get("usage_record_id") or "")
                if (
                    not usage_record_id
                    or usage_record_id in seen_usage_records
                    or usage_record_id not in usage_records
                ):
                    continue
                seen_usage_records.add(usage_record_id)
                usage = usage_records[usage_record_id]
                timeline.append(
                    {
                        "event_id": row["event_id"],
                        "event_type": "model_called",
                        **base,
                        **self._associations(usage, base),
                        "usage_record_id": usage_record_id,
                        "model_gateway_id": str(usage.get("model_gateway_id") or ""),
                        "provider_id": str(usage.get("provider_id") or ""),
                        "model_name": str(usage.get("model_name") or ""),
                        "execution_status": str(usage.get("execution_status") or ""),
                        "timestamp": row["created_at"],
                    }
                )
                continue
            if event_type not in TIMELINE_EVENT_TYPES:
                continue
            timeline.append(
                {
                    "event_id": row["event_id"],
                    "event_type": event_type,
                    **base,
                    **self._associations(payload, base),
                    "usage_record_id": None,
                    "current_step": str(payload.get("current_step") or ""),
                    "question": str(payload.get("question") or ""),
                    "context_summary": str(payload.get("context_summary") or ""),
                    "assignee_id": str(payload.get("assignee_id") or ""),
                    "tool_name": str(payload.get("tool_name") or ""),
                    "execution_status": str(payload.get("execution_status") or ""),
                    "timestamp": row["created_at"],
                }
            )
        return timeline

    def mark_started(self, task_id: str) -> None:
        self._record(
            task_id,
            "execution_started",
            execution_status="running",
        )

    def mark_capability_selected(self, task_id: str) -> None:
        self._record(
            task_id,
            "capability_selected",
            execution_status="running",
        )

    def mark_knowledge_retrieved(self, task_id: str, context_package_id: str) -> None:
        self._record(
            task_id,
            "knowledge_retrieved",
            context_summary="相关上下文已检索" if context_package_id else "未检索到可用上下文",
            execution_status="running",
        )

    def mark_tool_called(self, task_id: str, current_step: str, tool_name: str) -> None:
        self._record(
            task_id,
            "tool_called",
            current_step=self._safe_text(current_step, "current_step", 200),
            tool_name=self._safe_text(tool_name, "tool_name", 256),
            execution_status="running",
        )

    @agent_stop_serialized
    def await_input(
        self,
        task_id: str,
        *,
        current_step: str,
        question: str,
        context_summary: str,
        responsible_id: str = "",
        resume_parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        responsible = self._owner_assignee(responsible_id)
        state = self._persist_control_state(
            task_id,
            allowed_statuses=RUNNING_TASK_STATUSES,
            status="AWAITING_INPUT",
            current_step=current_step,
            question=question,
            context_summary=context_summary,
            assignee_id=responsible,
            resume_parameters=resume_parameters or {},
        )
        self._record(
            task_id,
            "awaiting_input",
            current_step=state["current_step"],
            question=state["pending_question"],
            context_summary=state["context_summary"],
            assignee_id=state["handoff_assignee_id"],
            execution_status="awaiting_input",
        )
        return state

    @agent_stop_serialized
    def request_handoff(
        self,
        task_id: str,
        *,
        current_step: str,
        question: str,
        context_summary: str,
        assignee_id: str = "",
        resume_parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        assignee = self._owner_assignee(assignee_id)
        state = self._persist_control_state(
            task_id,
            allowed_statuses=RUNNING_TASK_STATUSES
            | {"AWAITING_INPUT", "FAILED"},
            status="HUMAN_HANDOFF",
            current_step=current_step,
            question=question,
            context_summary=context_summary,
            assignee_id=assignee,
            resume_parameters=resume_parameters or {},
        )
        self._record(
            task_id,
            "human_handoff_requested",
            current_step=state["current_step"],
            question=state["pending_question"],
            context_summary=state["context_summary"],
            assignee_id=state["handoff_assignee_id"],
            execution_status="human_handoff",
        )
        return state

    def accept_handoff(self, task_id: str) -> dict[str, Any]:
        actor = self._current_actor()
        state = self._persist_control_state(
            task_id,
            allowed_statuses={"HUMAN_HANDOFF"},
            assignee_id=actor,
        )
        self._record(
            task_id,
            "human_handoff_accepted",
            assignee_id=actor,
            execution_status="human_handoff",
            idempotency_key=f"task-run:{TenantContext.current_tenant_id()}:{task_id}:accepted:{actor}",
        )
        return state

    def reassign_handoff(self, task_id: str, assignee_id: str) -> dict[str, Any]:
        assignee = self._owner_assignee(assignee_id)
        if not assignee:
            raise ValueError("assignee_id is required")
        state = self._persist_control_state(
            task_id,
            allowed_statuses={"HUMAN_HANDOFF"},
            assignee_id=assignee,
        )
        self._record(
            task_id,
            "human_handoff_reassigned",
            assignee_id=assignee,
            execution_status="human_handoff",
        )
        return state

    def supply_input(
        self,
        task_id: str,
        *,
        input_summary: str,
        resume_parameters: dict[str, Any],
    ) -> dict[str, Any]:
        summary = self._safe_text(input_summary, "input_summary", 4000)
        if not summary:
            raise ValueError("input_summary is required")
        task = self._task_context(task_id)
        parameters = json.loads(task["resume_parameters_json"] or "{}")
        parameters.update(self._safe_parameters(resume_parameters))
        parameters["additional_context"] = summary
        state = self._persist_control_state(
            task_id,
            task=task,
            allowed_statuses={"AWAITING_INPUT"},
            context_summary="用户已补充恢复所需信息",
            resume_parameters=parameters,
        )
        self._record(
            task_id,
            "input_supplied",
            context_summary="用户已补充恢复所需信息",
            execution_status="awaiting_input",
        )
        return state

    def resume(self, task_id: str, resume_parameters: dict[str, Any]) -> dict[str, Any]:
        task = self._task_context(task_id)
        parameters = json.loads(task["resume_parameters_json"] or "{}")
        parameters.update(self._safe_parameters(resume_parameters))
        state = self._persist_control_state(
            task_id,
            task=task,
            allowed_statuses={"AWAITING_INPUT", "HUMAN_HANDOFF"},
            status="RESUMED",
            question="",
            context_summary="已恢复原任务执行",
            resume_parameters=parameters,
        )
        self._record(
            task_id,
            "execution_resumed",
            current_step=state["current_step"],
            context_summary=state["context_summary"],
            assignee_id=state["handoff_assignee_id"],
            execution_status="resumed",
        )
        return state

    @agent_stop_serialized
    def cancel(self, task_id: str, reason: str = "") -> dict[str, Any]:
        state = self._persist_control_state(
            task_id,
            allowed_statuses=RUNNING_TASK_STATUSES
            | {"INIT", "AWAITING_INPUT", "HUMAN_HANDOFF", "FAILED"},
            status="CANCELLED",
            question="",
            context_summary=self._safe_text(reason, "reason", 1000) or "用户已取消执行",
        )
        self._record(
            task_id,
            "execution_cancelled",
            current_step=state["current_step"],
            context_summary=state["context_summary"],
            assignee_id=state["handoff_assignee_id"],
            execution_status="cancelled",
            idempotency_key=f"task-run:{TenantContext.current_tenant_id()}:{task_id}:cancelled",
        )
        return state

    def mark_completed(self, task_id: str) -> None:
        self._record(
            task_id,
            "execution_completed",
            execution_status="completed",
            idempotency_key=f"task-run:{TenantContext.current_tenant_id()}:{task_id}:completed",
        )

    def mark_failed(self, task_id: str, error: Exception) -> None:
        self._record(
            task_id,
            "execution_failed",
            context_summary=f"执行失败：{type(error).__name__}",
            execution_status="failed",
        )

    def raise_if_stopped(self, task_id: str) -> None:
        status = self._task_context(task_id)["status"]
        if status in PAUSED_TASK_STATUSES:
            raise ExecutionPaused(status)

    def _persist_control_state(
        self,
        task_id: str,
        *,
        allowed_statuses: set[str],
        task: dict[str, Any] | None = None,
        status: str | None = None,
        current_step: str | None = None,
        question: str | None = None,
        context_summary: str | None = None,
        assignee_id: str | None = None,
        resume_parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        task = task or self._task_context(task_id)
        if task["status"] not in allowed_statuses:
            raise ValueError(
                f"task run status {task['status']} does not allow this action"
            )
        tenant_id = TenantContext.current_tenant_id()
        next_status = status or task["status"]
        flow = json.loads(task["state_flow"])
        if flow[-1] != next_status:
            flow.append(next_status)
        values = {
            "status": next_status,
            "state_flow": json.dumps(flow),
            "current_step": task["current_execution_step"]
            if current_step is None
            else self._safe_text(current_step, "current_step", 200),
            "question": task["pending_question"]
            if question is None
            else self._safe_text(question, "question", 2000),
            "context_summary": task["execution_context_summary"]
            if context_summary is None
            else self._safe_text(context_summary, "context_summary", 4000),
            "assignee_id": task["handoff_assignee_id"]
            if assignee_id is None
            else self._safe_text(assignee_id, "assignee_id", 200),
            "resume_parameters": task["resume_parameters_json"]
            if resume_parameters is None
            else json.dumps(self._safe_parameters(resume_parameters), ensure_ascii=False),
        }
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                update tasks
                set status = ?, state_flow = ?, current_execution_step = ?,
                    pending_question = ?, execution_context_summary = ?,
                    handoff_assignee_id = ?, resume_parameters_json = ?,
                    execution_state_changed_at = current_timestamp,
                    updated_at = current_timestamp
                where tenant_id = ? and task_id = ? and status = ?
                  and state_flow = ?
                  and current_execution_step = ?
                  and pending_question = ?
                  and execution_context_summary = ?
                  and handoff_assignee_id = ?
                  and resume_parameters_json = ?
                """,
                (
                    values["status"],
                    values["state_flow"],
                    values["current_step"],
                    values["question"],
                    values["context_summary"],
                    values["assignee_id"],
                    values["resume_parameters"],
                    tenant_id,
                    task_id,
                    task["status"],
                    task["state_flow"],
                    task["current_execution_step"],
                    task["pending_question"],
                    task["execution_context_summary"],
                    task["handoff_assignee_id"],
                    task["resume_parameters_json"],
                ),
            )
        if cursor.rowcount == 0:
            raise ValueError("task run state changed; reload and retry")
        return self.get_state(task_id)

    def _record(
        self,
        task_id: str,
        event_type: str,
        *,
        current_step: str = "",
        question: str = "",
        context_summary: str = "",
        assignee_id: str = "",
        tool_name: str = "",
        execution_status: str = "",
        idempotency_key: str | None = None,
    ) -> None:
        task = self._task_context(task_id)
        self.event_log.record(
            correlation_id=task_id,
            event_type=event_type,
            tenant_id=TenantContext.current_tenant_id(),
            idempotency_key=idempotency_key,
            payload={
                **self._event_context(task),
                "current_step": current_step,
                "question": question,
                "context_summary": context_summary,
                "assignee_id": assignee_id,
                "tool_name": tool_name,
                "execution_status": execution_status,
            },
        )

    def _task_context(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select t.*,
                       coalesce(p.department_id, b.department_id, '') as attribution_department_id,
                       coalesce(w.business_id, '') as attribution_business_id
                from tasks t
                left join projects p
                  on p.tenant_id = t.tenant_id and p.project_id = t.project_id
                left join workspaces w
                  on w.tenant_id = t.tenant_id and w.company_id = t.company_id
                 and w.workspace_id = t.workspace_id
                left join canonical_businesses b
                  on b.tenant_id = w.tenant_id and b.company_id = w.company_id
                 and b.business_id = w.business_id
                where t.tenant_id = ? and t.task_id = ?
                """,
                (tenant_id, task_id),
            ).fetchone()
        if row is None:
            raise KeyError("task run not found")
        return dict(row)

    @staticmethod
    def _event_context(task: dict[str, Any]) -> dict[str, Any]:
        return {
            "tenant_id": task["tenant_id"],
            "company_id": task.get("company_id") or "",
            "department_id": task.get("attribution_department_id") or "",
            "business_id": task.get("attribution_business_id") or "",
            "workspace_id": task.get("workspace_id") or "",
            "work_ref": task.get("work_ref") or "",
            "execution_ref": task.get("execution_ref") or "",
            "project_id": task.get("project_id") or "",
            "task_id": task["task_id"],
            "task_run_id": task["task_id"],
            "employee_id": task.get("employee_id") or "",
            "capability_source": task.get("requested_capability_source") or "",
            "capability_type": task.get("requested_capability_type") or "",
            "capability_id": task.get("requested_capability_id") or "",
        }

    @staticmethod
    def _associations(payload: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
        return {
            key: str(payload.get(key) or fallback.get(key) or "")
            for key in (
                "tenant_id",
                "company_id",
                "department_id",
                "business_id",
                "workspace_id",
                "work_ref",
                "execution_ref",
                "project_id",
                "task_id",
                "task_run_id",
                "employee_id",
                "capability_source",
                "capability_type",
                "capability_id",
            )
        }

    @staticmethod
    def _current_actor() -> str:
        identity = TenantContext.current_identity()
        return str(identity.get("subject_id") or identity.get("ceo_id") or "local-owner")

    @classmethod
    def _owner_assignee(cls, assignee_id: str) -> str:
        assignee = cls._safe_text(assignee_id, "assignee_id", 200)
        actor = cls._current_actor()
        if assignee and assignee != actor:
            raise ValueError("assignee_id must be the current Local Owner")
        return assignee or actor

    @staticmethod
    def _public_status(task_status: str) -> str:
        return {
            "INIT": "queued",
            "PENDING": "running",
            "PARSED": "running",
            "RUNNING": "running",
            "AWAITING_INPUT": "awaiting_input",
            "HUMAN_HANDOFF": "human_handoff",
            "RESUMED": "resumed",
            "COMPLETED": "completed",
            "FAILED": "failed",
            "CANCELLED": "cancelled",
        }.get(task_status, task_status.lower())

    @staticmethod
    def _safe_text(value: Any, field: str, limit: int) -> str:
        text = str(value or "").strip()
        if len(text) > limit:
            raise ValueError(f"{field} exceeds {limit} characters")
        if redact_model_gateway_text(text) != text:
            raise ValueError(f"{field} contains secret-like content")
        return text

    @classmethod
    def _safe_parameters(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("resume_parameters must be an object")
        try:
            encoded = json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError) as error:
            raise ValueError("resume_parameters must be JSON serializable") from error
        if len(encoded.encode("utf-8")) > 8192:
            raise ValueError("resume_parameters exceeds 8192 bytes")

        def validate(item: Any, key: str = "") -> None:
            normalized_key = key.lower().replace("-", "_")
            compact_key = "".join(
                character for character in normalized_key if character.isalnum()
            )
            if (
                compact_key == "cot"
                or any(
                    word in compact_key
                    for word in (
                        "prompt",
                        "answer",
                        "response",
                        "output",
                        "reasoning",
                        "chainofthought",
                        "raw",
                        "token",
                        "cost",
                        "secret",
                        "credential",
                        "password",
                        "apikey",
                    )
                )
            ):
                raise ValueError("resume_parameters contains a forbidden secret field")
            if isinstance(item, str) and redact_model_gateway_text(item) != item:
                raise ValueError("resume_parameters contains secret-like content")
            if isinstance(item, dict):
                for child_key, child in item.items():
                    validate(child, str(child_key))
            elif isinstance(item, list):
                for child in item:
                    validate(child)

        validate(value)
        return value


def build_task_execution_control_router(
    service: TaskExecutionControlService,
    orchestrator: Any,
) -> APIRouter:
    router = APIRouter()

    def original_general_work(task_run_id: str) -> dict[str, str] | None:
        tenant_id = TenantContext.current_tenant_id()
        with service.database.connect() as connection:
            task = connection.execute(
                "select company_id, workspace_id, work_ref from tasks where tenant_id=? and task_id=?",
                (tenant_id, task_run_id),
            ).fetchone()
            if not task or not task["work_ref"] or not task["workspace_id"]:
                return None
            work = connection.execute(
                "select data_json, parent_id from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_id=? and entity_type='WORK'",
                (tenant_id, task["company_id"], task["workspace_id"], task["work_ref"]),
            ).fetchone()
            if not work:
                return None
            data = json.loads(work["data_json"] or "{}")
            if data.get("kind") != "CANONICAL_CHILD_WORK":
                return None
            cycle = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_id=? and entity_type='CYCLE'",
                (tenant_id, task["company_id"], task["workspace_id"], work["parent_id"]),
            ).fetchone()
            if not cycle or json.loads(cycle["data_json"] or "{}").get("kind") != "GENERAL_WORK_CYCLE":
                return None
            identity_company = TenantContext.current_identity().get("company_id")
            if identity_company and identity_company != task["company_id"]:
                raise HTTPException(status_code=404, detail="Original Work is outside the current Company")
            return {"company_id": task["company_id"], "workspace_id": task["workspace_id"],
                    "work_ref": task["work_ref"]}

    def reject_general_task_mutation(task_run_id: str) -> None:
        if original_general_work(task_run_id):
            raise HTTPException(status_code=409, detail="Continue from the original General Work")

    def invoke(action):
        try:
            return action()
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/api/workspace/task-runs/{task_run_id}")
    def get_task_run(task_run_id: str):
        state = invoke(lambda: service.get_state(task_run_id))
        state["original_general_work"] = original_general_work(task_run_id)
        return state

    @router.get("/api/workspace/task-runs/{task_run_id}/timeline")
    def get_task_run_timeline(task_run_id: str):
        return invoke(
            lambda: {
                "task_run_id": task_run_id,
                "events": service.list_timeline(task_run_id),
            }
        )

    @router.post("/api/workspace/task-runs/{task_run_id}/awaiting-input")
    def await_task_input(task_run_id: str, payload: AwaitingInputIn):
        reject_general_task_mutation(task_run_id)
        return invoke(
            lambda: service.await_input(
                task_run_id,
                current_step=payload.current_step,
                question=payload.question,
                context_summary=payload.context_summary,
                responsible_id=payload.responsible_id,
                resume_parameters=payload.resume_parameters,
            )
        )

    @router.post("/api/workspace/task-runs/{task_run_id}/input")
    def supply_task_input(task_run_id: str, payload: InputSupplyIn):
        reject_general_task_mutation(task_run_id)
        return invoke(
            lambda: service.supply_input(
                task_run_id,
                input_summary=payload.input_summary,
                resume_parameters=payload.resume_parameters,
            )
        )

    @router.post("/api/workspace/task-runs/{task_run_id}/handoff")
    def request_task_handoff(task_run_id: str, payload: HandoffIn):
        reject_general_task_mutation(task_run_id)
        return invoke(
            lambda: service.request_handoff(
                task_run_id,
                current_step=payload.current_step,
                question=payload.question,
                context_summary=payload.context_summary,
                assignee_id=payload.assignee_id,
                resume_parameters=payload.resume_parameters,
            )
        )

    @router.post("/api/workspace/task-runs/{task_run_id}/handoff/accept")
    def accept_task_handoff(task_run_id: str):
        reject_general_task_mutation(task_run_id)
        return invoke(lambda: service.accept_handoff(task_run_id))

    @router.patch("/api/workspace/task-runs/{task_run_id}/handoff/assignee")
    def reassign_task_handoff(task_run_id: str, payload: AssigneeIn):
        reject_general_task_mutation(task_run_id)
        return invoke(
            lambda: service.reassign_handoff(task_run_id, payload.assignee_id)
        )

    @router.post("/api/workspace/task-runs/{task_run_id}/resume", status_code=202)
    def resume_task(
        task_run_id: str,
        payload: ResumeIn,
        background_tasks: BackgroundTasks,
    ):
        reject_general_task_mutation(task_run_id)
        state = invoke(lambda: service.resume(task_run_id, payload.resume_parameters))
        tenant_id = TenantContext.current_tenant_id()
        identity = TenantContext.current_identity()

        async def resume_original_run() -> None:
            with TenantContext.scope(
                tenant_id,
                subject_id=identity.get("subject_id", ""),
                company_id=identity.get("company_id", ""),
                ceo_id=identity.get("ceo_id", ""),
                role=identity.get("role", ""),
                membership_status=identity.get("membership_status", ""),
                request_id=identity.get("request_id", ""),
            ):
                await orchestrator.run(task_run_id)

        background_tasks.add_task(resume_original_run)
        return state

    @router.post("/api/workspace/task-runs/{task_run_id}/cancel")
    def cancel_task(task_run_id: str, payload: CancelIn):
        reject_general_task_mutation(task_run_id)
        return invoke(lambda: service.cancel(task_run_id, payload.reason))

    return router
