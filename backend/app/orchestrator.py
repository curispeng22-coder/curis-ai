from __future__ import annotations

import json
import secrets

from .agent_adapter import AgentExecutionError, CodexExecutionHeld, CODEX_EXECUTION_HOLD_CODE
from .employee import AIEmployee
from .evolution_governor import EvolutionGovernor
from .prompt_builder import PromptBuilder
from .result_store import ResultStore
from .runtime_capability_context import RuntimeCapabilityContext
from .task_execution_control import ExecutionPaused
from .tool_executor import ToolExecutionError
from .tenant_context import TenantContext


class Orchestrator:
    def __init__(
        self,
        store: ResultStore,
        prompt_builder: PromptBuilder,
        employee: AIEmployee,
        skill_runtime=None,
        context_service=None,
        execution_control=None,
    ):
        self.store = store
        self.prompt_builder = prompt_builder
        self.employee = employee
        self.skill_runtime = skill_runtime
        self.context_service = context_service
        self.execution_control = execution_control
        self.evolution_governor = EvolutionGovernor(store, store.event_log)

    async def run(self, task_id: str) -> dict:
        task = self.store.get_task(task_id)
        if task["status"] in {"COMPLETED", "CANCELLED"}:
            return task
        from .runtime.general_execution_limits import task_limits
        general_limits = task_limits(self.store.database, task_id)
        writing_selection = self._writing_reply_selection(task)
        resuming = task["status"] == "RESUMED"
        if general_limits and resuming:
            raise ValueError("A limited attempt cannot be resumed or replayed")
        if writing_selection and resuming:
            raise ValueError("Unknown selected outbound attempts require reconciliation, not workflow replay")
        if self.execution_control and not resuming:
            self.execution_control.mark_started(task_id)
            self.execution_control.mark_capability_selected(task_id)
        skill_excerpt = self.skill_runtime.prompt_excerpt(task.get("employee_id")) if self.skill_runtime and not writing_selection else ""
        context_excerpt = ""
        context_package = None
        if self.context_service is not None and not writing_selection:
            context_package = self.context_service.build(task_id)
            context_excerpt = (
                self.context_service.prompt_excerpt(context_package, include_task_goal=False)
                if general_limits and not task.get("prompt")
                else self.context_service.prompt_excerpt(context_package)
            )
        if self.execution_control and not resuming:
            self.execution_control.mark_knowledge_retrieved(
                task_id, str((context_package or {}).get("id") or "")
            )
        if self.execution_control:
            try:
                self.execution_control.raise_if_stopped(task_id)
            except ExecutionPaused:
                return self.store.get_task(task_id)
        prompt = task.get("prompt") or self.prompt_builder.build(
            task["content"], skill_excerpt=skill_excerpt, context_excerpt=context_excerpt
        )
        if resuming:
            parameters = (
                self.execution_control.get_resume_parameters(task_id)
                if self.execution_control
                else {}
            )
            if parameters:
                prompt = (
                    f"{prompt}\n\nUser-supplied recovery context:\n"
                    f"{json.dumps(parameters, ensure_ascii=False)}"
                )
        try:
            workflow_plan = self.store.get_workflow(task_id)["workflow_plan"] if resuming else None
        except KeyError:
            workflow_plan = None
        if general_limits and workflow_plan is not None:
            if len(workflow_plan) != 1 or workflow_plan[0].get("tool_required") != "model_gateway_tool":
                raise ValueError("Original limited workflow does not match its constraint")
        if workflow_plan is None:
            self.store.transition(task_id, "PARSED", {"prompt": prompt})
            workflow_plan = ([{**self._step(1, "reply", {"CG_GRAPHIC_REPLY": "图文讨论回复", "CG_CONTENT_REPLY": "内容脚本讨论回复", "WRITING_CHAPTER_REPLY": "章节讨论回复", "MUSIC_SONG_REPLY": "歌曲讨论回复", "CONVERSATION_REPLY": "员工对话回复"}[writing_selection["purpose"]], {"CG_GRAPHIC_REPLY": "Reply only to the authorized selected graphic context.", "CG_CONTENT_REPLY": "Reply only to the authorized saved content/script context and exact selected text or shot. Text suggestions only; never claim media generation, rights, publication or account verification.", "WRITING_CHAPTER_REPLY": "Reply only to the authorized selected chapter context.", "MUSIC_SONG_REPLY": "Reply only to the authorized saved Song context. Text suggestions only; do not claim audio generation.", "CONVERSATION_REPLY": "Reply only to the CEO message under the current authorized assignment; do not perform external writes or invent facts."}[writing_selection["purpose"]], "Employee reply"),
                               "tool_required": "model_gateway_tool"}] if writing_selection else [{**self._step(1, "execute", "内部交付核对", "Execute the authorized internal review once.", "Task result"), "tool_required": "model_gateway_tool"}] if general_limits else self.generate_auto_workflow(task["content"]))
            if (
                task.get("requested_capability_source") == "tenant_private"
                or task.get("requested_capability_type") == "model"
            ):
                workflow_plan = [
                    {**step, "tool_required": "model_gateway_tool"}
                    for step in workflow_plan
                ]
            if task.get("requested_capability_type") == "agent":
                workflow_plan = [{**self._step(1, "execute", "员工执行原工作", "Complete only the authorized original Work.", "Original Work result"),
                                  "tool_required": "model_gateway_tool"}]
            self.store.save_workflow(task_id, workflow_plan)
            self.store.save_auto_workflow(task_id, workflow_plan)
        if self.execution_control:
            try:
                self.execution_control.raise_if_stopped(task_id)
            except ExecutionPaused:
                return self.store.get_task(task_id)
        self.store.transition(task_id, "RUNNING")
        self.store.update_workflow(task_id, status="RUNNING")
        self.store.update_auto_workflow(task_id, status="EXECUTING")
        workflow_completed = False
        try:
            capability_context = {
                "source": task.get("requested_capability_source"),
                "type": task.get("requested_capability_type"),
                "id": task.get("requested_capability_id"),
                "employee_id": task.get("employee_id"),
                "company_id": task.get("company_id"),
                "project_id": task.get("project_id"),
                "workspace_id": task.get("workspace_id"),
                "work_ref": task.get("work_ref"),
                "execution_ref": task.get("execution_ref"),
                "task_id": task["task_id"],
                **({"binding_id": writing_selection["binding_id"]} if writing_selection else {}),
            }
            with RuntimeCapabilityContext.scope(capability_context):
                result = await self._run_workflow(task_id, task["content"], workflow_plan, prompt)
            if self.execution_control and task.get("requested_capability_type") != "agent":
                self.execution_control.raise_if_stopped(task_id)
            result = self._apply_requested_capability(task, result)
            if task.get("requested_capability_type") == "agent":
                completed = self.store.finalize_agent_execution(task_id, prompt, result)
                if completed["status"] != "COMPLETED":
                    return completed
                # The Agent result is committed; later failures must not turn
                # that committed Task into a failed Task or replay the call.
                workflow_completed = True
                self._learn_from_execution(task, workflow_plan, result, "success")
                if self.execution_control:
                    self.execution_control.mark_completed(task_id)
                tenant = TenantContext.current_tenant_id()
                self.store.event_log.record(correlation_id=task_id,
                    event_type="agent.completion.followup_recorded", payload={"task_id": task_id},
                    idempotency_key=f"agent-completion-followup-done:{tenant}:{task_id}")
                return completed
            self.store.update_workflow(task_id, status="COMPLETED")
            self.store.update_auto_workflow(
                task_id,
                status="COMPLETED",
                adaptation_event={"event": "workflow_completed"},
            )
            workflow_completed = True
            self._learn_from_execution(task, workflow_plan, result, "success")
            self.store.save_execution(
                task_id,
                result["tool_name"],
                prompt,
                result["output"],
                result["cost"],
                usage=result,
            )
            completed = self.store.transition(
                task_id,
                "COMPLETED",
                {
                    "selected_tool": result["tool_name"],
                    "output": result["output"],
                    "cost": result["cost"],
                    "error": None,
                },
            )
            if completed["status"] != "COMPLETED":
                self.store.update_workflow(task_id, status=completed["status"])
                self.store.update_auto_workflow(task_id, status=completed["status"])
                return completed
            for artifact in result.get("artifact_receipts", []):
                self.store.save_artifact(task_id, title=artifact["relative_path"],
                    content=json.dumps(artifact, ensure_ascii=False, sort_keys=True),
                    source_ref="agent.output:" + artifact["relative_path"], artifact_type="agent_file_receipt")
            if self.execution_control:
                self.execution_control.mark_completed(task_id)
            return completed
        except ExecutionPaused:
            if task.get("requested_capability_type") == "agent" and self.store.has_scoped_agent_reservation(task_id):
                self.store.record_agent_outcome_unknown(task_id)
            task = self.store.get_task(task_id)
            self.store.update_workflow(task_id, status=task["status"])
            self.store.update_auto_workflow(task_id, status=task["status"])
            return task
        except ToolExecutionError as error:
            if workflow_completed and task.get("requested_capability_type") == "agent":
                raise AgentExecutionError("原执行已提交，但后续记录未确认。",
                    status="completion_followup_unknown", outbound_attempted=True) from error
            if isinstance(error.cause, AgentExecutionError) and error.cause.status == "outcome_unknown":
                self.store.record_agent_outcome_unknown(task_id)
            if self.execution_control:
                try:
                    self.execution_control.raise_if_stopped(task_id)
                except ExecutionPaused:
                    return self.store.get_task(task_id)
            self.store.update_workflow(task_id, status="FAILED")
            self.store.update_auto_workflow(
                task_id,
                status="FAILED",
                adaptation_event={"event": "workflow_failed", "reason": str(error)},
            )
            held = type(error.cause) is CodexExecutionHeld
            nonce = secrets.token_hex(16) if held else ""
            failure = CODEX_EXECUTION_HOLD_CODE + ":" + nonce if held else str(error)
            if not held and failure.startswith(CODEX_EXECUTION_HOLD_CODE + ":"):
                failure = "agent_execution_failed"
            failed_task = self.store.transition(task_id, "FAILED", {"error": failure})
            if (held and failed_task["status"] == "FAILED" and failed_task["error"] == failure
                    and self.store.event_log is not None):
                try:
                    self.store.event_log.record(correlation_id=task_id, event_type="agent.execution.codex_held",
                        payload={"task_id": task_id, "work_ref": task.get("work_ref") or "",
                                 "company_id": task.get("company_id") or "", "workspace_id": task.get("workspace_id"),
                                 "nonce": nonce, "state_flow": failed_task["state_flow"]})
                except Exception:
                    pass
            if self.execution_control:
                self.execution_control.mark_failed(task_id, error)
            raise
        except Exception as error:
            if workflow_completed and task.get("requested_capability_type") == "agent":
                raise AgentExecutionError("原执行已提交，但后续记录未确认。",
                    status="completion_followup_unknown", outbound_attempted=True) from error
            if isinstance(error, AgentExecutionError) and error.status == "outcome_unknown":
                self.store.record_agent_outcome_unknown(task_id)
            if self.execution_control:
                try:
                    self.execution_control.raise_if_stopped(task_id)
                except ExecutionPaused:
                    return self.store.get_task(task_id)
            if not workflow_completed:
                self.store.update_workflow(task_id, status="FAILED")
                self.store.update_auto_workflow(
                    task_id,
                    status="FAILED",
                    adaptation_event={"event": "workflow_failed", "reason": str(error)},
                )
            held = type(error) is CodexExecutionHeld
            nonce = secrets.token_hex(16) if held else ""
            failure = CODEX_EXECUTION_HOLD_CODE + ":" + nonce if held else str(error)
            if not held and failure.startswith(CODEX_EXECUTION_HOLD_CODE + ":"):
                failure = "agent_execution_failed"
            failed_task = self.store.transition(task_id, "FAILED", {"error": failure})
            if (held and failed_task["status"] == "FAILED" and failed_task["error"] == failure
                    and self.store.event_log is not None):
                try:
                    self.store.event_log.record(correlation_id=task_id, event_type="agent.execution.codex_held",
                        payload={"task_id": task_id, "work_ref": task.get("work_ref") or "",
                                 "company_id": task.get("company_id") or "", "workspace_id": task.get("workspace_id"),
                                 "nonce": nonce, "state_flow": failed_task["state_flow"]})
                except Exception:
                    pass
            if self.execution_control:
                self.execution_control.mark_failed(task_id, error)
            raise

    @staticmethod
    def _apply_requested_capability(task: dict, result: dict) -> dict:
        if not task.get("requested_capability_id"):
            result = dict(result)
            result["employee_id"] = task.get("employee_id") or ""
            result["employee_role"] = task.get("employee_role") or "tech_lead"
            result["employee_name"] = task.get("employee_name") or "Tech Lead"
            return result
        result = dict(result)
        result["tool_name"] = task["requested_capability_id"]
        result["capability_source"] = task["requested_capability_source"]
        result["capability_type"] = task["requested_capability_type"]
        result["capability_id"] = task["requested_capability_id"]
        result["employee_id"] = task.get("employee_id") or ""
        result["employee_role"] = task.get("employee_role") or "tech_lead"
        result["employee_name"] = task.get("employee_name") or "Tech Lead"
        for trace_step in result.get("trace", []):
            if not trace_step.get("error"):
                trace_step["tool"] = task["requested_capability_id"]
        return result

    def plan_workflow(self, task_content: str) -> list[dict]:
        return self.generate_auto_workflow(task_content)

    def _writing_reply_selection(self, task):
        with self.store.database.connect() as con:
            rows = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='conversation.execution_bound'", (TenantContext.current_tenant_id(), task["task_id"])).fetchall()
        selections = [json.loads(row["payload"]) for row in rows if json.loads(row["payload"]).get("execution_selection")]
        if not selections:
            return None
        if len(rows) != 1:
            raise ValueError("Conversation Task requires a unique server execution binding")
        bound = selections[0]; selected = bound["execution_selection"]
        if (selected.get("purpose") not in {"WRITING_CHAPTER_REPLY", "CG_GRAPHIC_REPLY", "CG_CONTENT_REPLY", "MUSIC_SONG_REPLY", "CONVERSATION_REPLY"} or bound["attempt_id"] != task["execution_ref"]
                or bound["company_id"] != task["company_id"] or bound["company_employee_ref"] != task["employee_id"]
                or selected["binding_id"] != bound["binding_id"] or selected["scope"]["workspace_id"] != task["workspace_id"]
                or selected["model"]["model_key"] != task["requested_capability_id"]
                or selected["model"]["source"] != task["requested_capability_source"]):
            raise ValueError("Selected Task selection does not match persisted execution facts")
        return selected

    def generate_auto_workflow(self, task_content: str) -> list[dict]:
        content = task_content.lower()
        learned_pattern = self.store.best_execution_pattern(self._task_signature(task_content))
        if learned_pattern is not None:
            return self._apply_adaptive_optimization(
                [
                    self._step_for_action(index, action, learned_pattern["tool_chain"][index - 1] if index <= len(learned_pattern["tool_chain"]) else None)
                    for index, action in enumerate(learned_pattern["step_sequence"], start=1)
                ]
            )
        steps = [self._step(1, "analyze", "需求分析", "Understand task intent and decompose execution needs.", "Task requirements summary")]
        wants_architecture = any(keyword in content for keyword in ("architecture", "system design", "technical design", "架构"))
        wants_ui = any(keyword in content for keyword in ("ui", "frontend", "page", "页面", "登录"))
        wants_backend = any(keyword in content for keyword in ("api", "backend", "后端", "接口"))
        wants_code = any(keyword in content for keyword in ("code", "implement", "function", "代码", "开发", "实现", "parser"))
        if wants_architecture and wants_code and not wants_ui and not wants_backend:
            return self._apply_adaptive_optimization([
                self._step(1, "design_architecture", "架构设计", "Design the technical structure before implementation.", "Architecture outline"),
                self._step(2, "generate_code", "代码实现", "Generate the implementation output.", "Code output"),
            ])
        if wants_code and not wants_ui and not wants_backend:
            return self._apply_adaptive_optimization([self._step(1, "generate_code", "代码实现", "Generate the implementation output.", "Code output")])
        if wants_ui:
            steps.append(self._step(len(steps) + 1, "design_ui", "UI设计", "Design the user interface structure.", "UI structure"))
            steps.append(self._step(len(steps) + 1, "generate_frontend", "前端实现", "Generate frontend implementation.", "Frontend code"))
        if wants_backend:
            steps.append(self._step(len(steps) + 1, "generate_backend", "后端API实现", "Generate backend API implementation.", "Backend API code"))
        steps.append(self._step(len(steps) + 1, "validate", "联调测试", "Validate the accumulated execution output.", "Validation result"))
        if len(steps) == 2 and not any((wants_ui, wants_backend, wants_code)):
            return self._apply_adaptive_optimization([self._step(1, "execute", "任务执行", "Execute the task directly.", "Task result")])
        return self._apply_adaptive_optimization(steps)

    def _step(self, index: int, action: str, step_name: str, purpose: str, expected_output: str) -> dict:
        step = {
            "step": index,
            "action": action,
            "description": purpose,
            "step_name": step_name,
            "purpose": purpose,
            "expected_output": expected_output,
        }
        step["tool_required"] = self.employee.router.tool_for_generated_step(step)
        return step

    def _apply_adaptive_optimization(self, steps: list[dict]) -> list[dict]:
        evolution_decisions = {
            item["optimization_decision"]
            for item in self.store.list_system_evolution_log()
        }
        if "remove_design_ui_for_ui_api" in evolution_decisions:
            steps = [step for step in steps if step["action"] != "design_ui"]
            for index, step in enumerate(steps, start=1):
                step["step"] = index
        tool_overrides = {
            event["from"]: event["to"]
            for event in self.store.list_adaptation_events()
            if event.get("event") == "tool_fallback" and event.get("from") and event.get("to")
        }
        performance = self.store.list_tool_performance()
        for step in steps:
            if step["tool_required"] in tool_overrides:
                step["tool_required"] = tool_overrides[step["tool_required"]]
                step["purpose"] = f"{step['purpose']} Adapted from prior tool fallback."
                step["description"] = step["purpose"]
            learned_tool = self.employee.router.select_best_tool(step, performance)
            if learned_tool != step["tool_required"]:
                step["tool_required"] = learned_tool
                step["purpose"] = f"{step['purpose']} Learned from historical tool performance."
                step["description"] = step["purpose"]
        return steps

    def _step_for_action(self, index: int, action: str, learned_tool: str | None = None) -> dict:
        templates = {
            "analyze": ("需求分析", "Understand task intent and decompose execution needs.", "Task requirements summary"),
            "design_ui": ("UI设计", "Design the user interface structure.", "UI structure"),
            "generate_frontend": ("前端实现", "Generate frontend implementation.", "Frontend code"),
            "generate_backend": ("后端API实现", "Generate backend API implementation.", "Backend API code"),
            "validate": ("联调测试", "Validate the accumulated execution output.", "Validation result"),
            "design_architecture": ("架构设计", "Design the technical structure before implementation.", "Architecture outline"),
            "generate_code": ("代码实现", "Generate the implementation output.", "Code output"),
            "execute": ("任务执行", "Execute the task directly.", "Task result"),
        }
        step_name, purpose, expected_output = templates.get(action, ("任务执行", "Execute the task directly.", "Task result"))
        step = self._step(index, action, step_name, purpose, expected_output)
        if learned_tool is not None:
            step["tool_required"] = learned_tool
            step["purpose"] = f"{step['purpose']} Reused from successful execution pattern."
            step["description"] = step["purpose"]
        return step

    def _task_signature(self, task_content: str) -> str:
        content = task_content.lower()
        wants_ui = any(keyword in content for keyword in ("ui", "frontend", "page", "页面", "登录"))
        wants_backend = any(keyword in content for keyword in ("api", "backend", "后端", "接口"))
        wants_architecture = any(keyword in content for keyword in ("architecture", "system design", "technical design", "架构"))
        wants_code = any(keyword in content for keyword in ("code", "implement", "function", "代码", "开发", "实现", "parser"))
        if wants_ui and wants_backend:
            return "ui_api"
        if wants_architecture and wants_code:
            return "architecture_code"
        if wants_code:
            return "code"
        return "general"

    async def _run_workflow(self, task_id: str, task_content: str, workflow_plan: list[dict], initial_prompt: str) -> dict:
        capability = RuntimeCapabilityContext.current() or {}
        agent_turn = capability.get("type") == "agent"
        deferred_agent_steps = []
        agent_outbound_states = []
        workflow = self.store.get_workflow(task_id)
        completed_steps = set(workflow["completed_steps"])
        prior_rows = {
            item["step_index"]: item
            for item in self.store.list_workflow_trace(task_id)
            if item["step_index"] in completed_steps
        }
        prior_trace = {
            step_index: item["output"] for step_index, item in prior_rows.items()
        }
        if agent_turn and completed_steps.difference(prior_rows):
            raise AgentExecutionError("原Agent步骤证据不完整，需先核对原执行。",
                status="outcome_unknown", outbound_attempted=False)
        previous_outputs = [
            f"Step {step['step']} {step['step_name']} output:\n{prior_trace[step['step']]}"
            for step in workflow_plan
            if step["step"] in prior_trace
        ]
        accumulated_context = "\n".join(previous_outputs)
        previous_output = prior_trace.get(max(completed_steps), "") if completed_steps else ""
        prior_tool = (
            prior_rows[max(completed_steps)]["tool_used"] if completed_steps else ""
        )
        final_result = {
            "tool_name": prior_tool,
            "output": accumulated_context if len(workflow_plan) > 1 else previous_output,
            "cost": 0.0,
            "trace": [],
                "model_gateway_id": "",
                "model_name": "",
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "token": 0,
                "estimated_cost": 0.0,
                "status": "not_run",
        }
        for step in workflow_plan:
            if step["step"] in completed_steps:
                continue
            if self.execution_control:
                self.execution_control.raise_if_stopped(task_id)
            self.store.update_workflow(task_id, current_step=step["step"])
            step_input = initial_prompt if len(workflow_plan) == 1 else self._build_step_input(task_content, step, previous_output, accumulated_context)
            try:
                result = await self.employee.execute_step(step, step_input)
            except ToolExecutionError as error:
                if agent_turn:
                    # The outer handler preserves typed UNKNOWN before checking
                    # cancellation; do not publish an uncommitted trace here.
                    raise
                if self.execution_control:
                    self.execution_control.raise_if_stopped(task_id)
                self.store.save_trace(task_id, error.trace)
                self.store.update_workflow(task_id, current_step=step["step"], failed_step=step["step"], status="FAILED")
                self._learn_from_failure(task_id, step, error.trace)
                self.store.update_auto_workflow(
                    task_id,
                    status="FAILED",
                    adaptation_event={"event": "step_failed", "step": step["step"], "reason": str(error)},
                )
                raise
            if self.execution_control:
                for trace_item in result["trace"]:
                    self.execution_control.mark_tool_called(
                        task_id,
                        str(step["step"]),
                        str(trace_item.get("tool") or result["tool_name"]),
                    )
                signal_status = str(result.get("status") or "").lower()
                if signal_status == "awaiting_input":
                    self.execution_control.await_input(
                        task_id,
                        current_step=str(step["step"]),
                        question=str(result.get("question") or "需要补充执行信息"),
                        context_summary=str(result.get("context_summary") or "执行已安全暂停"),
                        responsible_id=str(result.get("responsible_id") or ""),
                        resume_parameters=result.get("resume_parameters") or {},
                    )
                    raise ExecutionPaused("AWAITING_INPUT")
                if signal_status == "human_handoff":
                    self.execution_control.request_handoff(
                        task_id,
                        current_step=str(step["step"]),
                        question=str(result.get("question") or "需要人工接管"),
                        context_summary=str(result.get("context_summary") or "执行已停止自动推进"),
                        assignee_id=str(result.get("assignee_id") or ""),
                        resume_parameters=result.get("resume_parameters") or {},
                    )
                    raise ExecutionPaused("HUMAN_HANDOFF")
            if agent_turn:
                if not result.get("trace"):
                    raise AgentExecutionError("Agent执行证据不完整，效果仍需核验。",
                        status="outcome_unknown", outbound_attempted=result.get("outbound_attempted") is not False)
                agent_outbound_states.append(result.get("outbound_attempted"))
                deferred_agent_steps.append({"step": step, "input": step_input,
                    "tool_traces": self._tool_traces_for_step(step, result, step_input, previous_output),
                    "tool_name": result["tool_name"], "output": result["output"],
                    "timestamp": result["trace"][-1]["timestamp"]})
            else:
                self._record_adaptations(task_id, step, result)
                self.store.save_trace(task_id, self._tool_traces_for_step(step, result, step_input, previous_output))
                self.store.save_workflow_trace(task_id, step, result, step_input)
                self.store.update_workflow(task_id, completed_step=step["step"])
            if self.execution_control and not agent_turn:
                self.execution_control.raise_if_stopped(task_id)
            previous_output = result["output"]
            accumulated_context = f"{accumulated_context}\nStep {step['step']} {step['step_name']} output:\n{previous_output}".strip()
            output = previous_output if len(workflow_plan) == 1 else accumulated_context
            final_result = {
                "tool_name": result["tool_name"],
                "output": output,
                "cost": round(float(final_result["cost"]) + float(result.get("cost", 0)), 6),
                "trace": [*final_result["trace"], *result["trace"]],
                "model_gateway_id": result.get("model_gateway_id") or final_result["model_gateway_id"],
                "model_name": result.get("model_name") or final_result["model_name"],
                "prompt_tokens": int(final_result["prompt_tokens"]) + int(result.get("prompt_tokens", 0) or 0),
                "completion_tokens": int(final_result["completion_tokens"]) + int(result.get("completion_tokens", 0) or 0),
                "total_tokens": int(final_result["total_tokens"]) + int(result.get("total_tokens", result.get("token", 0)) or 0),
                "token": int(final_result["token"]) + int(result.get("total_tokens", result.get("token", 0)) or 0),
                "estimated_cost": round(
                    float(final_result["estimated_cost"]) + float(result.get("estimated_cost", result.get("cost", 0)) or 0),
                    6,
                ),
                "status": result.get("status") or "success",
                "credential_id": result.get("credential_id") or final_result.get("credential_id", ""),
                "credential_ref_digest": result.get("credential_ref_digest") or final_result.get("credential_ref_digest", ""),
                "fallback_used": bool(result.get("fallback_used") or final_result.get("fallback_used")),
                "fallback_from_model": result.get("fallback_from_model") or final_result.get("fallback_from_model", ""),
                "fallback_reason": result.get("fallback_reason") or final_result.get("fallback_reason", ""),
                "session_id": result.get("session_id") or final_result.get("session_id", ""),
                "agent_artifacts": result.get("artifacts") or final_result.get("agent_artifacts", []),
                "agent_permissions": result.get("permissions") or final_result.get("agent_permissions", {}),
                "computer_access": result.get("computer_access") or final_result.get("computer_access", {}),
                "resume_supported": bool(result.get("resume_supported") or final_result.get("resume_supported")),
                "cancel_supported": bool(result.get("cancel_supported") or final_result.get("cancel_supported")),
                "artifact_receipts": [*final_result.get("artifact_receipts", []), *result.get("artifact_receipts", [])],
                "skill_packages": result.get("skill_packages") or final_result.get("skill_packages", []),
                "skill_file_reads": [*final_result.get("skill_file_reads", []), *result.get("skill_file_reads", [])],
                "browser_tool_calls": [*final_result.get("browser_tool_calls", []), *result.get("browser_tool_calls", [])],
                "agent_authorization_ref": result.get("agent_authorization_ref") or final_result.get("agent_authorization_ref"),
                "native_model_profile": result.get("native_model_profile") or final_result.get("native_model_profile"),
            }
        if agent_turn:
            if not deferred_agent_steps:
                raise AgentExecutionError("原Agent步骤已完成，需先核对原执行。",
                    status="outcome_unknown", outbound_attempted=False)
            final_result["_agent_step_traces"] = deferred_agent_steps
            final_result["outbound_attempted"] = (True if any(value is True for value in agent_outbound_states)
                else False if all(value is False for value in agent_outbound_states) else None)
        return final_result

    def _record_adaptations(self, task_id: str, step: dict, result: dict) -> None:
        failed_attempts = [item for item in result["trace"] if item.get("error")]
        if not failed_attempts:
            return
        self.store.update_auto_workflow(
            task_id,
            status="ADAPTING",
            adaptation_event={
                "event": "tool_fallback",
                "step": step["step"],
                "from": failed_attempts[-1]["tool"],
                "to": result["tool_name"],
            },
        )
        self.store.update_auto_workflow(task_id, status="EXECUTING")

    def _learn_from_execution(self, task: dict, workflow_plan: list[dict], result: dict, status: str) -> None:
        task_signature = self._task_signature(task["content"])
        tool_chain = [step["tool"] for step in result["trace"] if not step.get("error")]
        self.store.save_workflow_metric(
            task_id=task["task_id"],
            task_signature=task_signature,
            step_count=len(workflow_plan),
            status=status,
            total_cost=float(result.get("cost", 0)),
            tool_chain=tool_chain,
        )
        self.store.save_execution_pattern(
            task_signature=task_signature,
            pattern_type="successful_workflow" if status == "success" else "failed_workflow",
            step_sequence=[step["action"] for step in workflow_plan],
            tool_chain=[step["tool_required"] for step in workflow_plan],
            success_rate=1.0 if status == "success" else 0.0,
            avg_step_count=len(workflow_plan),
        )
        for trace_step in result["trace"]:
            if trace_step.get("error"):
                self.store.record_tool_performance(trace_step["tool"], success=False, latency_ms=1000, cost=0)
                self.store.save_failure_log(
                    task_id=task["task_id"],
                    step_index=trace_step["step"],
                    tool_name=trace_step["tool"],
                    failure_type="tool_failure",
                    root_cause=trace_step["error"],
                    correction_strategy="Use fallback tool and lower future routing priority for this tool.",
                )
            else:
                self.store.record_tool_performance(trace_step["tool"], success=True, latency_ms=1, cost=float(result.get("cost", 0)))
        self._run_development_loop(task, workflow_plan, result)

    def _learn_from_failure(self, task_id: str, step: dict, trace: list[dict]) -> None:
        for trace_step in trace:
            self.store.record_tool_performance(trace_step["tool"], success=False, latency_ms=1000, cost=0)
            self.store.save_failure_log(
                task_id=task_id,
                step_index=step["step"],
                tool_name=trace_step["tool"],
                failure_type="tool_failure",
                root_cause=trace_step.get("error", "step failed"),
                correction_strategy="Avoid the failed tool for matching future workflow steps.",
            )

    def _run_development_loop(self, task: dict, workflow_plan: list[dict], result: dict) -> None:
        trace = result["trace"]
        failed_steps = [step for step in trace if step.get("error")]
        codex_calls = [step for step in trace if step["tool"] == "codex_tool" and not step.get("error")]
        repeated_tools = len(trace) - len({step["tool"] for step in trace})
        has_output = bool(str(result.get("output", "")).strip())
        step_count = len(workflow_plan)
        speed_score = max(0, 100 - (step_count * 10) - (len(failed_steps) * 20))
        correctness_score = 100 if has_output and not failed_steps else 60 if has_output else 0
        efficiency_score = max(0, 100 - (max(0, step_count - 3) * 15) - (max(0, len(codex_calls) - 1) * 10))
        tool_usage_score = max(0, 100 - (repeated_tools * 10) - (len(failed_steps) * 25))
        self.store.save_execution_score(
            task_id=task["task_id"],
            speed_score=speed_score,
            correctness_score=correctness_score,
            efficiency_score=efficiency_score,
            tool_usage_score=tool_usage_score,
        )
        inefficiencies = []
        strategy_parts = []
        if step_count > 4:
            inefficiencies.append("workflow_length")
            strategy_parts.append("Simplify future workflows by removing redundant planning-only steps.")
            self.store.save_system_evolution_log(
                task_id=task["task_id"],
                target_module="workflow_generator",
                optimization_decision="remove_design_ui_for_ui_api",
                applied_change="Future matching UI/API workflows skip standalone design_ui and pass context directly into implementation steps.",
            )
        if len(codex_calls) > 1:
            inefficiencies.append("codex_overuse")
            strategy_parts.append("Optimize code generation by reusing previous code-generation context and avoiding redundant Codex calls.")
            self.store.save_system_evolution_log(
                task_id=task["task_id"],
                target_module="tool_router",
                optimization_decision="reduce_redundant_codex_calls",
                applied_change="Codex remains primary for coding steps, but repeated coding steps are treated as a token-usage bottleneck.",
            )
        if not has_output:
            inefficiencies.append("inconsistent_output")
            strategy_parts.append("Self-debug empty outputs by rerouting future matching steps through a validating reasoning tool.")
            self.store.save_failure_log(
                task_id=task["task_id"],
                step_index=workflow_plan[-1]["step"] if workflow_plan else 0,
                tool_name=result.get("tool_name", ""),
                failure_type="inconsistent_output",
                root_cause="empty output from execution",
                correction_strategy="Validate output before completion and reroute empty responses through a reasoning fallback.",
            )
        if failed_steps:
            inefficiencies.append("tool_failure")
            strategy_parts.append("Reduce future failure risk by lowering priority for failed tools.")
        if not strategy_parts:
            strategy_parts.append("Keep current workflow shape and preserve successful tool routing.")
        self.store.save_development_strategy(
            task_id=task["task_id"],
            development_strategy=" ".join(strategy_parts),
            detected_inefficiencies=inefficiencies,
        )
        self._run_meta_development_system(task, workflow_plan, result, inefficiencies)
        self.evolution_governor.evaluate(
            task=task,
            workflow_plan=workflow_plan,
            result=result,
            inefficiencies=inefficiencies,
        )

    def _run_meta_development_system(
        self,
        task: dict,
        workflow_plan: list[dict],
        result: dict,
        inefficiencies: list[str],
    ) -> None:
        actions = [step["action"] for step in workflow_plan]
        has_output = bool(str(result.get("output", "")).strip())
        gap_analysis = {
            "task_signature": self._task_signature(task["content"]),
            "observed_steps": actions,
            "detected_gaps": inefficiencies,
            "current_gate": "Tool System v1.6",
            "status": "ready_for_review" if has_output else "needs_debugging",
        }
        planned_issues = [
            {
                "title": "Review generated execution output",
                "owner_seat": "产品规划席",
                "scope": "Confirm whether the execution result satisfies the task intent before advancing the next issue.",
            }
        ]
        if inefficiencies:
            planned_issues.append(
                {
                    "title": "Reduce detected development inefficiencies",
                    "owner_seat": "系统交付席",
                    "scope": "Adjust workflow generation or tool routing for: " + ", ".join(inefficiencies),
                }
            )
        verification_plan = [
            "Backend tests: .venv/bin/python -m unittest discover -s tests",
            "API evidence: create task, run task, retrieve status, retrieve meta development report",
            "Scope drift scan: rg forbidden terms across backend/app backend/tests frontend/app",
        ]
        source_of_truth_suggestions = [
            "knowledge/CURRENT_CONTEXT.md",
            "TASKS.md",
            "PROJECT_STATUS.md",
            "reviews/",
        ]
        self.store.save_meta_development_report(
            task_id=task["task_id"],
            gap_analysis=gap_analysis,
            planned_issues=planned_issues,
            verification_plan=verification_plan,
            source_of_truth_suggestions=source_of_truth_suggestions,
        )

    def _tool_traces_for_step(self, step: dict, result: dict, step_input: str, previous_output: str) -> list[dict]:
        traces = []
        for trace_step in result["trace"]:
            traces.append(
                {
                    "step": step["step"],
                    "tool": trace_step["tool"],
                    "input": previous_output or trace_step.get("input", step_input),
                    "output": trace_step.get("output", ""),
                    "error": trace_step.get("error"),
                    "timestamp": trace_step["timestamp"],
                }
            )
        return traces

    def _build_step_input(self, task_content: str, step: dict, previous_output: str, accumulated_context: str) -> str:
        return (
            f"Original task:\n{task_content}\n\n"
            f"Current step {step['step']} - {step['step_name']} ({step['action']}):\n"
            f"Purpose: {step['purpose']}\n"
            f"Expected output: {step['expected_output']}\n"
            f"Tool required: {step['tool_required']}\n\n"
            f"Previous step output:\n{previous_output or 'None'}\n\n"
            f"Accumulated context:\n{accumulated_context or 'None'}"
        )
