from __future__ import annotations

import json
import hashlib
import re
import uuid
from contextlib import nullcontext
from typing import Any

from .database import Database
from .resource_scope_policy import ResourceScopePolicy
from .model_gateway import redact_model_gateway_text
from .tenant_context import TenantContext


class ResultStore:
    def __init__(self, database: Database, event_log=None):
        self.database = database
        self.event_log = event_log

    def record_agent_local_child_exit(self, task_id: str, evidence: dict) -> None:
        """Record only an attempt-bound direct child reap; external effects remain unknown."""
        if (self.event_log is None or not isinstance(evidence, dict)
                or set(evidence) != {"child_pid", "returncode", "attempt_sha256"}
                or type(evidence["child_pid"]) is not int or evidence["child_pid"] <= 1
                or type(evidence["returncode"]) is not int or not -255 <= evidence["returncode"] <= 255
                or not isinstance(evidence["attempt_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", evidence["attempt_sha256"])):
            raise ValueError("invalid local child evidence")
        tenant = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select t.task_id,t.company_id,t.workspace_id,t.work_ref from tasks t join runtime_entities w "
                "on w.tenant_id=t.tenant_id and w.company_id=t.company_id and w.workspace_id is t.workspace_id "
                "and w.entity_id=t.work_ref and w.entity_type='WORK' "
                "where t.tenant_id=? and t.task_id=? and t.requested_capability_type='agent'",
                (tenant, task_id),
            ).fetchone()
            if row is None or not row["company_id"] or not row["work_ref"]:
                raise ValueError("local child evidence scope is unavailable")
            payload = {"task_id": row["task_id"], "company_id": row["company_id"],
                       "workspace_id": row["workspace_id"], "work_ref": row["work_ref"],
                       "attempt_sha256": evidence["attempt_sha256"], "state": "DIRECT_CHILD_REAPED",
                       "returncode": evidence["returncode"], "external_effect": "UNKNOWN"}
            self.event_log.record_in_connection(
                connection, correlation_id=task_id, event_type="agent.execution.local_child_exit",
                payload=payload, idempotency_key=f"agent-local-child-exit:{tenant}:{task_id}:{evidence['attempt_sha256']}",
            )

    def record_agent_outcome_unknown(self, task_id: str) -> None:
        """Persist a scoped hold before projecting an uncertain Agent result."""
        if self.event_log is None:
            raise RuntimeError("Agent outcome cannot be recorded")
        tenant = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select task_id,company_id,workspace_id,work_ref from tasks where tenant_id=? and task_id=?",
                (tenant, task_id),
            ).fetchone()
            if not row or not row["company_id"] or not row["work_ref"]:
                raise RuntimeError("Agent outcome scope cannot be verified")
            payload = {"task_id": row["task_id"], "company_id": row["company_id"],
                       "workspace_id": row["workspace_id"], "work_ref": row["work_ref"]}
            self.event_log.record_in_connection(
                connection, correlation_id=task_id, event_type="agent.execution.outcome_unknown",
                payload=payload, idempotency_key=f"agent-outcome-unknown:{tenant}:{task_id}",
            )

    def has_scoped_agent_reservation(self, task_id: str) -> bool:
        tenant = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            task = connection.execute("select company_id,work_ref from tasks where tenant_id=? and task_id=?",
                                      (tenant, task_id)).fetchone()
            if task is None or not task["company_id"] or not task["work_ref"]:
                raise ValueError("original Agent work scope is unavailable")
            rows = connection.execute("select payload from evolution_events where tenant_id=? "
                "and correlation_id='curis-existing-codex-allowance-v1' "
                "and event_type='company.agent_allowance.reserved'", (tenant,)).fetchall()
        for row in rows:
            payload = json.loads(row["payload"])
            if not isinstance(payload, dict):
                raise ValueError("Agent reservation evidence is invalid")
            if payload.get("task_id") == task_id:
                if payload.get("company_id") != task["company_id"] or payload.get("work_ref") != task["work_ref"]:
                    raise ValueError("Agent reservation scope is inconsistent")
                return True
        return False

    def create_task(
        self,
        content: str,
        *,
        company_id: str | None = None,
        project_id: str | None = None,
        workspace_id: str | None = None,
        scope_type: str | None = None,
        scope_ref: str | None = None,
        work_ref: str | None = None,
        execution_ref: str | None = None,
        capability_source: str | None = None,
        capability_type: str | None = None,
        capability_id: str | None = None,
        employee_id: str | None = None,
        employee_role: str | None = None,
        employee_name: str | None = None,
    ) -> dict[str, Any]:
        if not content:
            raise ValueError("content is required")
        if any((capability_source, capability_type, capability_id)) and not all(
            (capability_source, capability_type, capability_id)
        ):
            raise ValueError("capability_source, capability_type, and capability_id must be provided together")
        if capability_source and capability_source not in {"official", "tenant_private"}:
            raise ValueError("capability_source must be official or tenant_private")
        if capability_type and capability_type not in {"model", "agent", "tool", "connector"}:
            raise ValueError("capability_type must be model, agent, tool, or connector")
        task_id = str(uuid.uuid4())
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            if scope_type is not None or scope_ref is not None:
                scope = ResourceScopePolicy.execution_scope_from_record(
                    connection, tenant_id=tenant_id,
                    record={"company_id": company_id, "workspace_id": workspace_id,
                            "scope_type": scope_type, "scope_ref": scope_ref},
                )
                scope_type, scope_ref, workspace_id = scope["scope_type"], scope["scope_ref"], scope["workspace_id"]
                if work_ref:
                    work = connection.execute(
                        "select * from runtime_entities where tenant_id=? and entity_id=? and entity_type='WORK'",
                        (tenant_id, work_ref),
                    ).fetchone()
                    if work is None:
                        raise ValueError("Task Work does not exist in this execution scope")
                    ResourceScopePolicy.require_same_execution_scope(
                        scope, ResourceScopePolicy.execution_scope_from_record(
                            connection, tenant_id=tenant_id, record=dict(work),
                        ),
                    )
            connection.execute(
                """
                insert into tasks (
                  task_id, tenant_id, company_id, project_id, workspace_id, work_ref,
                  execution_ref, scope_type, scope_ref, content, status, state_flow,
                  requested_capability_source, requested_capability_type,
                  requested_capability_id, employee_id, employee_role, employee_name
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    tenant_id,
                    company_id,
                    project_id,
                    workspace_id,
                    work_ref,
                    execution_ref,
                    scope_type,
                    scope_ref,
                    content,
                    "INIT",
                    json.dumps(["INIT"]),
                    capability_source,
                    capability_type,
                    capability_id,
                    employee_id,
                    employee_role,
                    employee_name,
                ),
            )
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from tasks where task_id = ? and tenant_id = ?",
                (task_id, tenant_id),
            ).fetchone()
            if row is None:
                raise KeyError("task not found")
            return self._task_from_row(row)

    def list_tasks(self) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from tasks where tenant_id = ? order by created_at desc",
                (tenant_id,),
            ).fetchall()
            return [self._task_from_row(row) for row in rows]

    def transition(self, task_id: str, status: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        task = self.get_task(task_id)
        state_flow = list(task["state_flow"])
        if state_flow[-1] != status:
            state_flow.append(status)
        payload = {
            "status": status,
            "state_flow": state_flow,
            "prompt": task["prompt"],
            "output": task["output"],
            "selected_tool": task["selected_tool"],
            "cost": task["cost"],
            "error": task["error"],
            **(data or {}),
        }
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                update tasks
                set status = ?, state_flow = ?, prompt = ?, output = ?, selected_tool = ?, cost = ?,
                    error = ?, updated_at = current_timestamp
                where task_id = ? and tenant_id = ?
                  and status not in ('AWAITING_INPUT', 'HUMAN_HANDOFF', 'CANCELLED')
                """,
                (
                    payload["status"],
                    json.dumps(payload["state_flow"]),
                    payload["prompt"],
                    payload["output"],
                    payload["selected_tool"],
                    payload["cost"],
                    payload["error"],
                    task_id,
                    TenantContext.current_tenant_id(),
                ),
            )
        if cursor.rowcount == 0:
            return self.get_task(task_id)
        if status == "COMPLETED" and str(payload["output"] or "").strip():
            self.save_artifact(
                task_id,
                title=task["content"][:120],
                content=str(payload["output"]),
                source_ref="task.output",
            )
        return self.get_task(task_id)

    def save_artifact(
        self,
        task_id: str,
        *,
        title: str,
        content: str,
        source_ref: str,
        artifact_type: str = "execution_result",
    ) -> dict[str, Any]:
        task = self.get_task(task_id)
        if task["status"] != "COMPLETED":
            raise ValueError("artifact requires a completed task")
        tenant_id = TenantContext.current_tenant_id()
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        artifact_id = f"artifact-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into artifacts (
                  artifact_id, tenant_id, task_id, title, artifact_type,
                  status, content, source_ref, content_sha256, updated_at
                ) values (?, ?, ?, ?, ?, 'generated', ?, ?, ?, current_timestamp)
                on conflict (tenant_id, task_id, source_ref) do update set
                  title = excluded.title,
                  artifact_type = excluded.artifact_type,
                  content = excluded.content,
                  content_sha256 = excluded.content_sha256,
                  updated_at = current_timestamp
                """,
                (
                    artifact_id,
                    tenant_id,
                    task_id,
                    title.strip() or "未命名成果",
                    artifact_type,
                    content,
                    source_ref,
                    digest,
                ),
            )
            row = connection.execute(
                """
                select * from artifacts
                where tenant_id = ? and task_id = ? and source_ref = ?
                """,
                (tenant_id, task_id, source_ref),
            ).fetchone()
        return dict(row)

    def list_artifacts(
        self,
        *,
        task_id: str | None = None,
        project_id: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        if task_id:
            self.get_task(task_id)
        query = """
            select a.* from artifacts a
            join tasks t on t.task_id = a.task_id and t.tenant_id = a.tenant_id
            where a.tenant_id = ?
        """
        params: list[Any] = [tenant_id]
        if task_id:
            query += " and a.task_id = ?"
            params.append(task_id)
        if project_id:
            query += " and t.project_id = ?"
            params.append(project_id)
        query += " order by a.created_at desc limit ?"
        params.append(max(1, min(limit, 200)))
        with self.database.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def save_execution(
        self,
        task_id: str,
        tool_name: str,
        prompt: str,
        output: str,
        cost: float,
        usage: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into executions (task_id, tenant_id, tool_name, prompt, output, cost)
                values (?, ?, ?, ?, ?, ?)
                """,
                (task_id, tenant_id, tool_name, prompt, output, cost),
            )
            execution_id = cursor.lastrowid
            row = connection.execute(
                "select * from executions where execution_id = ?",
                (execution_id,),
            ).fetchone()
            execution = dict(row)
        self._record_usage_events(task_id, tool_name, cost, usage or {})
        return execution

    def finalize_agent_execution(self, task_id: str, prompt: str, result: dict[str, Any]) -> dict[str, Any]:
        """Commit one Agent result only if its original Task still owns execution."""
        if self.event_log is None:
            raise RuntimeError("Agent result audit is unavailable")
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            task = connection.execute("select * from tasks where tenant_id=? and task_id=?",
                                      (tenant_id, task_id)).fetchone()
            if task is None or task["requested_capability_type"] != "agent":
                raise ValueError("original Agent task is unavailable")
            if task["status"] == "COMPLETED":
                raise ValueError("Agent task is already completed")
            if task["status"] not in {"RUNNING", "CANCELLED", "AWAITING_INPUT", "HUMAN_HANDOFF"}:
                raise ValueError("Agent task state cannot be finalized")
            if connection.execute("select 1 from executions where tenant_id=? and task_id=? limit 1",
                                  (tenant_id, task_id)).fetchone():
                raise ValueError("Agent execution already has a result record")
            won = task["status"] == "RUNNING"
            output = result["output"] if won else ""
            usage = result if won else {**result, "agent_artifacts": [], "artifact_receipts": []}
            connection.execute("insert into executions (task_id,tenant_id,tool_name,prompt,output,cost) "
                               "values (?,?,?,?,?,?)",
                               (task_id, tenant_id, result["tool_name"], prompt, output, result["cost"]))
            self._record_usage_events(task_id, result["tool_name"], result["cost"], usage, connection=connection)
            if not won:
                if (connection.execute("update workflows set status=? where tenant_id=? and task_id=?",
                                       (task["status"], tenant_id, task_id)).rowcount != 1 or
                    connection.execute("update auto_workflows set status=? where tenant_id=? and task_id=?",
                                       (task["status"], tenant_id, task_id)).rowcount != 1):
                    raise ValueError("original Agent workflow is unavailable")
                if result.get("outbound_attempted") is not False:
                    if not task["company_id"] or not task["work_ref"]:
                        raise ValueError("original Agent work scope is unavailable")
                    payload = {"task_id": task_id, "company_id": task["company_id"],
                               "workspace_id": task["workspace_id"], "work_ref": task["work_ref"]}
                    self.event_log.record_in_connection(connection, correlation_id=task_id,
                        event_type="agent.execution.outcome_unknown", payload=payload,
                        idempotency_key=f"agent-outcome-unknown:{tenant_id}:{task_id}")
            else:
                step_traces = result.get("_agent_step_traces")
                if (not isinstance(step_traces, list) or not step_traces or
                    any(not isinstance(item, dict) or not isinstance(item.get("step"), dict) for item in step_traces)):
                    raise ValueError("original Agent step evidence is unavailable")
                workflow_row = connection.execute("select completed_steps from workflows where tenant_id=? and task_id=?",
                                                  (tenant_id, task_id)).fetchone()
                if workflow_row is None:
                    raise ValueError("original Agent workflow is unavailable")
                completed_steps = json.loads(workflow_row["completed_steps"])
                if not isinstance(completed_steps, list):
                    raise ValueError("Agent step is already committed or invalid")
                for item in step_traces:
                    if item["step"]["step"] in completed_steps:
                        raise ValueError("Agent step is already committed or invalid")
                    completed_steps.append(item["step"]["step"])
                flow = json.loads(task["state_flow"])
                if not isinstance(flow, list):
                    raise ValueError("task state history is invalid")
                if not flow or flow[-1] != "COMPLETED":
                    flow.append("COMPLETED")
                changed = connection.execute("update tasks set status='COMPLETED',state_flow=?,selected_tool=?,"
                    "output=?,cost=?,error=NULL,updated_at=current_timestamp where tenant_id=? and task_id=? and status='RUNNING'",
                    (json.dumps(flow), result["tool_name"], output, result["cost"], tenant_id, task_id))
                if changed.rowcount != 1:
                    raise ValueError("Agent task state changed during finalization")
                workflow = connection.execute("update workflows set status='COMPLETED',completed_steps=? "
                                              "where tenant_id=? and task_id=?",
                                              (json.dumps(completed_steps), tenant_id, task_id))
                auto = connection.execute("select adaptation_log from auto_workflows where tenant_id=? and task_id=?",
                                          (tenant_id, task_id)).fetchone()
                if workflow.rowcount != 1 or auto is None:
                    raise ValueError("original Agent workflow is unavailable")
                log = json.loads(auto["adaptation_log"])
                if not isinstance(log, list):
                    raise ValueError("Agent workflow history is invalid")
                for item in step_traces:
                    failed = [trace for trace in item["tool_traces"] if trace.get("error")]
                    if failed:
                        log.append({"event": "tool_fallback", "step": item["step"]["step"],
                                    "from": failed[-1]["tool"], "to": item["tool_name"]})
                log.append({"event": "workflow_completed"})
                connection.execute("update auto_workflows set status='COMPLETED',adaptation_log=? where tenant_id=? and task_id=?",
                                   (json.dumps(log), tenant_id, task_id))
                for item in step_traces:
                    step = item["step"]
                    for trace in item["tool_traces"]:
                        connection.execute("insert into tool_traces (task_id,tenant_id,step_index,tool_name,input,output,error,timestamp) "
                            "values (?,?,?,?,?,?,?,?)", (task_id, tenant_id, trace["step"], trace["tool"],
                            trace["input"], trace.get("output", ""), trace.get("error"), trace["timestamp"]))
                    connection.execute("insert into workflow_traces (task_id,tenant_id,step_index,action,tool_used,input,output,timestamp) "
                        "values (?,?,?,?,?,?,?,?)", (task_id, tenant_id, step["step"],
                        step.get("action", step.get("step_name", "execute")), item["tool_name"],
                        item["input"], item["output"], item["timestamp"]))
                artifacts = []
                if str(output or "").strip():
                    artifacts.append((task["content"][:120], output, "task.output", "execution_result"))
                for item in result.get("artifact_receipts", []):
                    artifacts.append((item["relative_path"], json.dumps(item, ensure_ascii=False, sort_keys=True),
                                      "agent.output:" + item["relative_path"], "agent_file_receipt"))
                for title, content, source_ref, artifact_type in artifacts:
                    connection.execute("insert into artifacts (artifact_id,tenant_id,task_id,title,artifact_type,status,content,"
                        "source_ref,content_sha256,updated_at) values (?,?,?,?,?,'generated',?,?,?,current_timestamp) "
                        "on conflict (tenant_id,task_id,source_ref) do update set title=excluded.title,"
                        "artifact_type=excluded.artifact_type,content=excluded.content,content_sha256=excluded.content_sha256,"
                        "updated_at=current_timestamp", (f"artifact-{uuid.uuid4()}", tenant_id, task_id,
                        title.strip() or "未命名成果", artifact_type, content, source_ref, hashlib.sha256(content.encode()).hexdigest()))
                self.event_log.record_in_connection(connection, correlation_id=task_id,
                    event_type="agent.completion.followup_pending", payload={"task_id": task_id},
                    idempotency_key=f"agent-completion-followup:{tenant_id}:{task_id}")
        return self.get_task(task_id)

    def list_executions(self, task_id: str) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from executions where task_id = ? and tenant_id = ? order by execution_id",
                (task_id, tenant_id),
            ).fetchall()
            return [dict(row) for row in rows]

    def save_trace(self, task_id: str, trace: list[dict[str, Any]]) -> None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            for step in trace:
                connection.execute(
                    """
                    insert into tool_traces (
                      task_id, tenant_id, step_index, tool_name, input, output, error, timestamp
                    ) values (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        task_id,
                        tenant_id,
                        step["step"],
                        step["tool"],
                        step["input"],
                        step.get("output", ""),
                        step.get("error"),
                        step["timestamp"],
                    ),
                )

    def list_trace(self, task_id: str) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select step_index, tool_name, input, output, error, timestamp
                from tool_traces
                where task_id = ? and tenant_id = ?
                order by step_index, trace_id
                """,
                (task_id, tenant_id),
            ).fetchall()
            return [dict(row) for row in rows]

    def save_workflow(self, task_id: str, workflow_plan: list[dict[str, Any]], status: str = "PLANNED") -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into workflows (
                  task_id, tenant_id, workflow_plan, current_step, completed_steps, failed_steps, status
                ) values (?, ?, ?, ?, ?, ?, ?)
                on conflict(task_id) do update set
                  workflow_plan = excluded.workflow_plan,
                  current_step = excluded.current_step,
                  completed_steps = excluded.completed_steps,
                  failed_steps = excluded.failed_steps,
                  status = excluded.status
                """,
                (task_id, tenant_id, json.dumps(workflow_plan), 0, "[]", "[]", status),
            )
        return self.get_workflow(task_id)

    def update_workflow(
        self,
        task_id: str,
        *,
        current_step: int | None = None,
        completed_step: int | None = None,
        failed_step: int | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        workflow = self.get_workflow(task_id)
        completed_steps = list(workflow["completed_steps"])
        failed_steps = list(workflow["failed_steps"])
        if completed_step is not None and completed_step not in completed_steps:
            completed_steps.append(completed_step)
        if failed_step is not None and failed_step not in failed_steps:
            failed_steps.append(failed_step)
        with self.database.connect() as connection:
            connection.execute(
                """
                update workflows
                set current_step = ?, completed_steps = ?, failed_steps = ?, status = ?
                where task_id = ?
                """,
                (
                    workflow["current_step"] if current_step is None else current_step,
                    json.dumps(completed_steps),
                    json.dumps(failed_steps),
                    workflow["status"] if status is None else status,
                    task_id,
                ),
            )
        return self.get_workflow(task_id)

    def get_workflow(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from workflows where task_id = ? and tenant_id = ?",
                (task_id, tenant_id),
            ).fetchone()
            if row is None:
                raise KeyError("workflow not found")
            workflow = dict(row)
            workflow["workflow_plan"] = json.loads(workflow["workflow_plan"])
            workflow["completed_steps"] = json.loads(workflow["completed_steps"])
            workflow["failed_steps"] = json.loads(workflow["failed_steps"])
            return workflow

    def save_auto_workflow(
        self,
        task_id: str,
        generated_steps: list[dict[str, Any]],
        status: str = "PLANNED",
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into auto_workflows (
                  task_id, tenant_id, generated_steps, status, adaptation_log
                ) values (?, ?, ?, ?, ?)
                on conflict(task_id) do update set
                  generated_steps = excluded.generated_steps,
                  status = excluded.status,
                  adaptation_log = excluded.adaptation_log
                """,
                (task_id, tenant_id, json.dumps(generated_steps), status, "[]"),
            )
        return self.get_auto_workflow(task_id)

    def update_auto_workflow(
        self,
        task_id: str,
        *,
        status: str | None = None,
        adaptation_event: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        workflow = self.get_auto_workflow(task_id)
        adaptation_log = list(workflow["adaptation_log"])
        if adaptation_event is not None:
            adaptation_log.append(adaptation_event)
        with self.database.connect() as connection:
            connection.execute(
                """
                update auto_workflows
                set status = ?, adaptation_log = ?
                where task_id = ?
                """,
                (
                    workflow["status"] if status is None else status,
                    json.dumps(adaptation_log),
                    task_id,
                ),
            )
        return self.get_auto_workflow(task_id)

    def get_auto_workflow(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from auto_workflows where task_id = ? and tenant_id = ?",
                (task_id, tenant_id),
            ).fetchone()
            if row is None:
                raise KeyError("auto workflow not found")
            workflow = dict(row)
            workflow["generated_steps"] = json.loads(workflow["generated_steps"])
            workflow["adaptation_log"] = json.loads(workflow["adaptation_log"])
            return workflow

    def list_adaptation_events(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select adaptation_log from auto_workflows").fetchall()
        events: list[dict[str, Any]] = []
        for row in rows:
            events.extend(json.loads(row["adaptation_log"]))
        return events

    def save_workflow_trace(self, task_id: str, step: dict[str, Any], tool_result: dict[str, Any], input_text: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        trace_step = tool_result["trace"][-1]
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into workflow_traces (
                  task_id, tenant_id, step_index, action, tool_used, input, output, timestamp
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    tenant_id,
                    step["step"],
                    step.get("action", step.get("step_name", "execute")),
                    tool_result["tool_name"],
                    input_text,
                    tool_result["output"],
                    trace_step["timestamp"],
                ),
            )
            row = connection.execute(
                "select * from workflow_traces where trace_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            return dict(row)

    def list_workflow_trace(self, task_id: str) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select step_index, action, tool_used, input, output, timestamp
                from workflow_traces
                where task_id = ? and tenant_id = ?
                order by step_index, trace_id
                """,
                (task_id, tenant_id),
            ).fetchall()
            return [dict(row) for row in rows]

    def save_execution_pattern(
        self,
        *,
        task_signature: str,
        pattern_type: str,
        step_sequence: list[str],
        tool_chain: list[str],
        success_rate: float,
        avg_step_count: float,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into execution_patterns (
                  task_signature, pattern_type, step_sequence, tool_chain, success_rate, avg_step_count
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (
                    task_signature,
                    pattern_type,
                    json.dumps(step_sequence),
                    json.dumps(tool_chain),
                    success_rate,
                    avg_step_count,
                ),
            )
            row = connection.execute(
                "select * from execution_patterns where pattern_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._pattern_from_row(row)

    def list_execution_patterns(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                select * from execution_patterns
                order by success_rate desc, avg_step_count asc, pattern_id desc
                """
            ).fetchall()
        return [self._pattern_from_row(row) for row in rows]

    def best_execution_pattern(self, task_signature: str) -> dict[str, Any] | None:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from execution_patterns
                where task_signature = ? and pattern_type = 'successful_workflow'
                order by success_rate desc, avg_step_count asc, pattern_id desc
                limit 1
                """,
                (task_signature,),
            ).fetchone()
        return None if row is None else self._pattern_from_row(row)

    def save_failure_log(
        self,
        *,
        task_id: str,
        step_index: int,
        tool_name: str,
        failure_type: str,
        root_cause: str,
        correction_strategy: str,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into failure_logs (
                  task_id, step_index, tool_name, failure_type, root_cause, correction_strategy
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (task_id, step_index, tool_name, failure_type, root_cause, correction_strategy),
            )
            row = connection.execute(
                "select * from failure_logs where failure_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row)

    def list_failure_logs(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from failure_logs order by failure_id").fetchall()
            return [dict(row) for row in rows]

    def record_tool_performance(
        self,
        tool_name: str,
        *,
        success: bool,
        latency_ms: float,
        cost: float,
    ) -> dict[str, Any]:
        current = self.get_tool_performance(tool_name)
        success_count = current["success_count"] + (1 if success else 0)
        failure_count = current["failure_count"] + (0 if success else 1)
        total_latency_ms = current["total_latency_ms"] + latency_ms
        total_count = success_count + failure_count
        avg_latency_ms = total_latency_ms / total_count if total_count else 0
        total_cost = current["total_cost"] + cost
        priority_weight = round((success_count * 2) - (failure_count * 3) - (avg_latency_ms / 1000) - total_cost, 6)
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into tool_performance (
                  tool_name, success_count, failure_count, total_latency_ms, avg_latency_ms, total_cost, priority_weight
                ) values (?, ?, ?, ?, ?, ?, ?)
                on conflict(tool_name) do update set
                  success_count = excluded.success_count,
                  failure_count = excluded.failure_count,
                  total_latency_ms = excluded.total_latency_ms,
                  avg_latency_ms = excluded.avg_latency_ms,
                  total_cost = excluded.total_cost,
                  priority_weight = excluded.priority_weight,
                  updated_at = current_timestamp
                """,
                (tool_name, success_count, failure_count, total_latency_ms, avg_latency_ms, total_cost, priority_weight),
            )
        return self.get_tool_performance(tool_name)

    def get_tool_performance(self, tool_name: str) -> dict[str, Any]:
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from tool_performance where tool_name = ?",
                (tool_name,),
            ).fetchone()
        if row is None:
            return {
                "tool_name": tool_name,
                "success_count": 0,
                "failure_count": 0,
                "total_latency_ms": 0.0,
                "avg_latency_ms": 0.0,
                "total_cost": 0.0,
                "priority_weight": 0.0,
            }
        return dict(row)

    def list_tool_performance(self) -> dict[str, dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from tool_performance order by tool_name").fetchall()
        return {row["tool_name"]: dict(row) for row in rows}

    def save_workflow_metric(
        self,
        *,
        task_id: str,
        task_signature: str,
        step_count: int,
        status: str,
        total_cost: float,
        tool_chain: list[str],
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into workflow_metrics (
                  task_id, task_signature, step_count, status, total_cost, tool_chain
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (task_id, task_signature, step_count, status, total_cost, json.dumps(tool_chain)),
            )
            row = connection.execute(
                "select * from workflow_metrics where metric_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        metric = dict(row)
        metric["tool_chain"] = json.loads(metric["tool_chain"])
        return metric

    def list_workflow_metrics(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from workflow_metrics order by metric_id").fetchall()
        metrics = []
        for row in rows:
            metric = dict(row)
            metric["tool_chain"] = json.loads(metric["tool_chain"])
            metrics.append(metric)
        return metrics

    def get_execution_summary_memory(self) -> dict[str, Any]:
        patterns = self.list_execution_patterns()
        failures = self.list_failure_logs()
        performance = self.list_tool_performance()
        return {
            "successful_patterns": [pattern for pattern in patterns if pattern["pattern_type"] == "successful_workflow"],
            "failed_patterns": failures,
            "optimal_tool_chains": [
                {"tool_name": tool, "priority_weight": data["priority_weight"]}
                for tool, data in sorted(performance.items(), key=lambda item: item[1]["priority_weight"], reverse=True)
            ],
        }

    def _record_usage_events(self, task_id: str, tool_name: str, cost: float, usage: dict[str, Any], *, connection=None) -> None:
        if self.event_log is None:
            return
        tenant_id = TenantContext.current_tenant_id()
        identity = TenantContext.current_identity()
        ceo_id = identity.get("ceo_id", "")
        if not ceo_id:
            raise RuntimeError("trusted CEO UsageContext is required to write UsageEvent")
        status = redact_model_gateway_text(usage.get("status") or "success")
        capability_source = redact_model_gateway_text(usage.get("capability_source") or "official")
        requested_capability_type = redact_model_gateway_text(usage.get("capability_type") or "")
        requested_capability_id = redact_model_gateway_text(usage.get("capability_id") or "")
        usage_record_id = redact_model_gateway_text(usage.get("usage_record_id") or "")
        employee_id = redact_model_gateway_text(usage.get("employee_id") or "")
        employee_role = redact_model_gateway_text(usage.get("employee_role") or "tech_lead")
        employee_name = redact_model_gateway_text(usage.get("employee_name") or "Tech Lead")
        workflow_run_id = redact_model_gateway_text(usage.get("workflow_run_id") or "")
        workflow_step_id = redact_model_gateway_text(usage.get("workflow_step_id") or "")
        with (nullcontext(connection) if connection is not None else self.database.connect()) as current:
            task = current.execute(
                "select company_id, project_id, workspace_id, work_ref, execution_ref "
                "from tasks where tenant_id=? and task_id=?",
                (tenant_id, task_id),
            ).fetchone()
            ledger = None
            if usage_record_id:
                ledger = current.execute(
                    "select company_id, department_id, business_id, workspace_id, work_ref, "
                    "execution_ref, project_id from ai_usage_records "
                    "where tenant_id=? and usage_record_id=?",
                    (tenant_id, usage_record_id),
                ).fetchone()
        attribution = dict(ledger or task or {})
        event_specs = [
            ("usage.tool_call", "tool", tool_name),
            ("usage.task_execution", "task", "task_execution"),
        ]
        for event_type, capability_type, capability_id in event_specs:
            if requested_capability_id and capability_type == requested_capability_type:
                capability_id = requested_capability_id
            idempotency_key = hashlib.sha256(
                f"{event_type}:{tenant_id}:{ceo_id}:{task_id}:{workflow_run_id}:{workflow_step_id}:{tool_name}".encode("utf-8")
            ).hexdigest()
            payload = {
                "id": idempotency_key,
                "tenant_id": tenant_id,
                "task_id": task_id,
                "ceo_id": ceo_id,
                "actor_type": "ceo",
                "employee_id": employee_id,
                "employee_role": employee_role,
                "employee_name": employee_name,
                "capability_type": capability_type,
                "capability_id": capability_id,
                "capability_source": capability_source,
                "usage_record_id": usage_record_id or None,
                "status": status,
                "scope_type": capability_type,
                "scope_ref": capability_id,
                "quantity": 1,
                "unit": "call",
                "capability_ref": {
                    "key": f"{capability_type}:{capability_id}",
                    "source": capability_source,
                    "owner_tenant_id": None if capability_source == "official" else tenant_id,
                    "visibility": "global" if capability_source == "official" else "tenant",
                },
                "idempotency_key": idempotency_key,
            }
            optional_audit_fields = {
                "request_id": usage.get("request_id"),
                "subject_id": usage.get("subject_id"),
                "subject_digest": usage.get("subject_digest"),
                "company_id": usage.get("company_id"),
                "project_id": usage.get("project_id"),
                "department_id": usage.get("department_id"),
                "business_id": usage.get("business_id"),
                "workspace_id": usage.get("workspace_id"),
                "work_ref": usage.get("work_ref"),
                "execution_ref": usage.get("execution_ref"),
                "workflow_id": usage.get("workflow_id"),
                "capability_binding_id": usage.get("capability_binding_id"),
                "http_status": usage.get("http_status"),
                "latency_ms": usage.get("latency_ms"),
                "outbound_attempted": usage.get("outbound_attempted"),
                "logical_call_id": usage.get("logical_call_id"),
                "attempt_no": usage.get("attempt_no"),
                "fallback_used": usage.get("fallback_used") or None,
                "fallback_from_model": usage.get("fallback_from_model"),
                "fallback_reason": usage.get("fallback_reason"),
                "session_id": usage.get("session_id"),
                "agent_artifacts": usage.get("agent_artifacts"),
                "artifact_receipts": usage.get("artifact_receipts") or [],
                "skill_packages": usage.get("skill_packages") or [],
                "skill_file_reads": usage.get("skill_file_reads") or [],
                "browser_tool_calls": usage.get("browser_tool_calls") or [],
                "agent_authorization_ref": usage.get("agent_authorization_ref"),
                "native_model_profile": usage.get("native_model_profile"),
                "agent_permissions": usage.get("agent_permissions"),
                "computer_access": usage.get("computer_access"),
                "resume_supported": usage.get("resume_supported"),
                "cancel_supported": usage.get("cancel_supported"),
            }
            for key in (
                "company_id", "department_id", "business_id", "workspace_id",
                "work_ref", "execution_ref", "project_id",
            ):
                if not optional_audit_fields.get(key):
                    optional_audit_fields[key] = attribution.get(key)
            for key, value in optional_audit_fields.items():
                if value is not None and value != "":
                    payload[key] = (
                        redact_model_gateway_text(value)
                        if isinstance(value, str)
                        else value
                    )
            if workflow_run_id:
                payload["workflow_run_id"] = workflow_run_id
            if workflow_step_id:
                payload["workflow_step_id"] = workflow_step_id
            if connection is None:
                self.event_log.record(correlation_id=task_id, event_type=event_type, payload=payload,
                                      tenant_id=tenant_id, idempotency_key=idempotency_key)
            else:
                self.event_log.record_in_connection(connection, correlation_id=task_id, event_type=event_type,
                                                    payload=payload, idempotency_key=idempotency_key)

    def save_execution_score(
        self,
        *,
        task_id: str,
        speed_score: float,
        correctness_score: float,
        efficiency_score: float,
        tool_usage_score: float,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into execution_scores (
                  task_id, speed_score, correctness_score, efficiency_score, tool_usage_score
                ) values (?, ?, ?, ?, ?)
                """,
                (task_id, speed_score, correctness_score, efficiency_score, tool_usage_score),
            )
            row = connection.execute(
                "select * from execution_scores where score_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row)

    def list_execution_scores(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from execution_scores order by score_id").fetchall()
            return [dict(row) for row in rows]

    def save_development_strategy(
        self,
        *,
        task_id: str,
        development_strategy: str,
        detected_inefficiencies: list[str],
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into development_strategies (
                  task_id, development_strategy, detected_inefficiencies
                ) values (?, ?, ?)
                """,
                (task_id, development_strategy, json.dumps(detected_inefficiencies)),
            )
            row = connection.execute(
                "select * from development_strategies where strategy_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        strategy = dict(row)
        strategy["detected_inefficiencies"] = json.loads(strategy["detected_inefficiencies"])
        return strategy

    def list_development_strategies(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from development_strategies order by strategy_id").fetchall()
        strategies = []
        for row in rows:
            strategy = dict(row)
            strategy["detected_inefficiencies"] = json.loads(strategy["detected_inefficiencies"])
            strategies.append(strategy)
        return strategies

    def save_system_evolution_log(
        self,
        *,
        task_id: str,
        target_module: str,
        optimization_decision: str,
        applied_change: str,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into system_evolution_log (
                  task_id, target_module, optimization_decision, applied_change
                ) values (?, ?, ?, ?)
                """,
                (task_id, target_module, optimization_decision, applied_change),
            )
            row = connection.execute(
                "select * from system_evolution_log where log_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return dict(row)

    def list_system_evolution_log(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from system_evolution_log order by log_id").fetchall()
            return [dict(row) for row in rows]

    def save_meta_development_report(
        self,
        *,
        task_id: str,
        gap_analysis: dict[str, Any],
        planned_issues: list[dict[str, Any]],
        verification_plan: list[str],
        source_of_truth_suggestions: list[str],
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into meta_development_reports (
                  task_id, tenant_id, gap_analysis, planned_issues, verification_plan, source_of_truth_suggestions
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    tenant_id,
                    json.dumps(gap_analysis),
                    json.dumps(planned_issues),
                    json.dumps(verification_plan),
                    json.dumps(source_of_truth_suggestions),
                ),
            )
            row = connection.execute(
                "select * from meta_development_reports where report_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._meta_development_report_from_row(row)

    def get_meta_development_report(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from meta_development_reports
                where task_id = ? and tenant_id = ?
                order by report_id desc
                limit 1
                """,
                (task_id, tenant_id),
            ).fetchone()
        if row is None:
            raise KeyError("meta development report not found")
        return self._meta_development_report_from_row(row)

    def save_architecture_lock(self, *, module_name: str, reason: str, locked_by: str, correlation_id: str | None = None) -> dict[str, Any]:
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into architecture_locks (module_name, reason, locked_by, active)
                values (?, ?, ?, 1)
                on conflict(module_name) do update set
                  reason = excluded.reason,
                  locked_by = excluded.locked_by,
                  active = 1
                """,
                (module_name, reason, locked_by),
            )
            row = connection.execute(
                "select * from architecture_locks where module_name = ?",
                (module_name,),
            ).fetchone()
        lock = dict(row)
        self._emit(correlation_id, "lock", lock)
        return lock

    def list_architecture_locks(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from architecture_locks where active = 1 order by module_name"
            ).fetchall()
        return [dict(row) for row in rows]

    def save_evolution_simulation(
        self,
        *,
        task_id: str,
        task_flow: list[str],
        tool_routing: list[str],
        workflow_graph: list[dict[str, Any]],
        performance_impact: dict[str, Any],
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into evolution_simulations (
                  task_id, tenant_id, task_flow, tool_routing, workflow_graph, performance_impact
                ) values (?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    tenant_id,
                    json.dumps(task_flow),
                    json.dumps(tool_routing),
                    json.dumps(workflow_graph),
                    json.dumps(performance_impact),
                ),
            )
            row = connection.execute(
                "select * from evolution_simulations where simulation_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        simulation = self._evolution_simulation_from_row(row)
        self._emit(correlation_id, "simulation", simulation)
        return simulation

    def get_evolution_simulation(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from evolution_simulations
                where task_id = ? and tenant_id = ?
                order by simulation_id desc
                limit 1
                """,
                (task_id, tenant_id),
            ).fetchone()
        if row is None:
            raise KeyError("evolution simulation not found")
        return self._evolution_simulation_from_row(row)

    def save_rollback_record(
        self,
        *,
        task_id: str,
        previous_architecture: str,
        stable_version: str,
        performance_comparison: dict[str, Any],
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into rollback_records (
                  task_id, tenant_id, previous_architecture, stable_version, performance_comparison
                ) values (?, ?, ?, ?, ?)
                """,
                (task_id, tenant_id, previous_architecture, stable_version, json.dumps(performance_comparison)),
            )
            row = connection.execute(
                "select * from rollback_records where rollback_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        rollback = self._rollback_record_from_row(row)
        self._emit(correlation_id, "rollback", rollback)
        return rollback

    def get_rollback_record(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from rollback_records
                where task_id = ? and tenant_id = ?
                order by rollback_id desc
                limit 1
                """,
                (task_id, tenant_id),
            ).fetchone()
        if row is None:
            raise KeyError("rollback record not found")
        return self._rollback_record_from_row(row)

    def save_evolution_decision(
        self,
        *,
        task_id: str,
        policy: list[str],
        decision: str,
        threshold_evaluation: dict[str, Any],
        proposal: dict[str, Any] | None,
        risk_analysis: dict[str, Any],
        automatic_code_modification_allowed: bool,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                insert into evolution_decisions (
                  task_id, tenant_id, policy, decision, threshold_evaluation, proposal, risk_analysis,
                  automatic_code_modification_allowed
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    tenant_id,
                    json.dumps(policy),
                    decision,
                    json.dumps(threshold_evaluation),
                    json.dumps(proposal) if proposal is not None else None,
                    json.dumps(risk_analysis),
                    1 if automatic_code_modification_allowed else 0,
                ),
            )
            row = connection.execute(
                "select * from evolution_decisions where decision_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        decision = self._evolution_decision_from_row(row)
        self._emit(correlation_id, "decision", decision)
        return decision

    def get_evolution_decision(self, task_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select * from evolution_decisions
                where task_id = ? and tenant_id = ?
                order by decision_id desc
                limit 1
                """,
                (task_id, tenant_id),
            ).fetchone()
        if row is None:
            raise KeyError("evolution decision not found")
        return self._evolution_decision_from_row(row)

    def _task_from_row(self, row: Any) -> dict[str, Any]:
        task = dict(row)
        task["state_flow"] = json.loads(task["state_flow"])
        task.pop("resume_parameters_json", None)
        return task

    def _pattern_from_row(self, row: Any) -> dict[str, Any]:
        pattern = dict(row)
        pattern["step_sequence"] = json.loads(pattern["step_sequence"])
        pattern["tool_chain"] = json.loads(pattern["tool_chain"])
        return pattern

    def _meta_development_report_from_row(self, row: Any) -> dict[str, Any]:
        report = dict(row)
        report["gap_analysis"] = json.loads(report["gap_analysis"])
        report["planned_issues"] = json.loads(report["planned_issues"])
        report["verification_plan"] = json.loads(report["verification_plan"])
        report["source_of_truth_suggestions"] = json.loads(report["source_of_truth_suggestions"])
        return report

    def _evolution_simulation_from_row(self, row: Any) -> dict[str, Any]:
        simulation = dict(row)
        simulation["task_flow"] = json.loads(simulation["task_flow"])
        simulation["tool_routing"] = json.loads(simulation["tool_routing"])
        simulation["workflow_graph"] = json.loads(simulation["workflow_graph"])
        simulation["performance_impact"] = json.loads(simulation["performance_impact"])
        return simulation

    def _rollback_record_from_row(self, row: Any) -> dict[str, Any]:
        rollback = dict(row)
        rollback["performance_comparison"] = json.loads(rollback["performance_comparison"])
        return rollback

    def _evolution_decision_from_row(self, row: Any) -> dict[str, Any]:
        decision = dict(row)
        decision["policy"] = json.loads(decision["policy"])
        decision["threshold_evaluation"] = json.loads(decision["threshold_evaluation"])
        decision["proposal"] = json.loads(decision["proposal"]) if decision["proposal"] else None
        decision["risk_analysis"] = json.loads(decision["risk_analysis"])
        decision["automatic_code_modification_allowed"] = bool(decision["automatic_code_modification_allowed"])
        return decision

    def _emit(self, correlation_id: str | None, event_type: str, payload: dict[str, Any]) -> None:
        if self.event_log is not None and correlation_id is not None:
            self.event_log.record(correlation_id=correlation_id, event_type=event_type, payload=payload)
