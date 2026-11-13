from __future__ import annotations

import asyncio
import inspect
import logging
from collections.abc import Callable
from datetime import datetime, timezone

from .local_rd_toolset import LOCAL_RD_TOOL_IDS
from .tool_registry import ToolRegistry


ToolFunction = Callable[[str], dict]

# RealRD 执行器超时保护：超过 300 秒视为超时。
_REAL_RD_TIMEOUT_SECONDS = 300
_REAL_RD_TOOL_NAME = "real_rd_executor_tool"

_logger = logging.getLogger(__name__)


class ToolExecutor:
    def __init__(self, registry: ToolRegistry, tool_functions: dict[str, ToolFunction]):
        self.registry = registry
        self.tool_functions = tool_functions

    async def execute(self, tool_name: str, prompt: str) -> dict:
        tool = self.registry.get(tool_name)
        function = self.tool_functions.get(tool["name"])
        if function is None:
            raise RuntimeError(f"tool executor is not configured: {tool_name}")
        from .runtime_capability_context import RuntimeCapabilityContext
        context = RuntimeCapabilityContext.current() or {}
        # Keep the request loop free to accept stop/revocation while an Agent runs.
        result = (await asyncio.to_thread(function, prompt)
                  if context.get("type") == "agent" and not inspect.iscoroutinefunction(function)
                  else function(prompt))
        if inspect.isawaitable(result):
            result = await result
        signal_status = str(result.get("status") or "").lower()
        output = (
            str(result.get("output") or "")
            if signal_status in {"awaiting_input", "human_handoff"}
            else result["output"]
        )
        response = {
            "tool_name": tool["name"],
            "output": output,
            "cost": result.get("cost", 0),
        }
        for key in (
            "model_gateway_id",
            "model_name",
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "token",
            "estimated_cost",
            "status",
            "capability_source",
            "credential_id",
            "credential_ref_digest",
            "provider_id",
            "unit_price_input",
            "unit_price_output",
            "price_version",
            "currency",
            "cost_source",
            "http_status",
            "latency_ms",
            "outbound_attempted",
            "request_id",
            "subject_id",
            "tenant_id",
            "company_id",
            "project_id",
            "workflow_id",
            "workflow_run_id",
            "workflow_step_id",
            "capability_binding_id",
            "capability_id",
            "capability_type",
            "employee_id",
            "fallback_used",
            "fallback_from_model",
            "fallback_reason",
            "usage_record_id",
            "logical_call_id",
            "attempt_no",
            "question",
            "context_summary",
            "responsible_id",
            "assignee_id",
            "resume_parameters",
            "session_id",
            "progress",
            "artifacts",
            "permissions",
            "computer_access",
            "resume_supported",
            "cancel_supported",
            "artifact_receipts",
            "skill_packages",
            "skill_file_reads",
            "browser_tool_calls",
            "agent_authorization_ref",
            "native_model_profile",
        ):
            if key in result:
                response[key] = result[key]
        return response

    async def execute_chain(self, tool_chain: list[str], initial_input: str, fallback_planner=None) -> dict:
        current_input = initial_input
        trace = []
        total_cost = 0.0
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        estimated_cost = 0.0
        model_gateway_id = ""
        model_name = ""
        status = "not_run"
        credential_id = ""
        credential_ref_digest = ""
        audit_metadata = {}
        selected_tool = None

        for planned_tool in tool_chain:
            candidates = fallback_planner(planned_tool) if fallback_planner else self._fallback_chain(planned_tool)
            step_result = None
            last_error = None
            for candidate in candidates:
                step_index = len(trace) + 1
                try:
                    if candidate == _REAL_RD_TOOL_NAME:
                        _logger.info("real_rd_executor_tool selected for step")
                        # 为 RealRD 执行添加超时保护
                        result = await asyncio.wait_for(
                            self.execute(candidate, current_input),
                            timeout=_REAL_RD_TIMEOUT_SECONDS,
                        )
                    else:
                        result = await self.execute(candidate, current_input)
                    step = self._trace_step(step_index, candidate, current_input, result["output"])
                    trace.append(step)
                    total_cost += float(result.get("cost", 0))
                    prompt_tokens += int(result.get("prompt_tokens", 0) or 0)
                    completion_tokens += int(result.get("completion_tokens", 0) or 0)
                    total_tokens += int(result.get("total_tokens", result.get("token", 0)) or 0)
                    estimated_cost += float(result.get("estimated_cost", result.get("cost", 0)) or 0)
                    model_gateway_id = result.get("model_gateway_id", model_gateway_id)
                    model_name = result.get("model_name", model_name)
                    status = result.get("status", "success")
                    credential_id = result.get("credential_id", credential_id)
                    credential_ref_digest = result.get("credential_ref_digest", credential_ref_digest)
                    audit_metadata.update(
                        {
                            key: result[key]
                            for key in (
                                "provider_id", "unit_price_input", "unit_price_output",
                                "price_version", "currency", "cost_source", "http_status",
                                "latency_ms", "outbound_attempted", "request_id", "subject_id",
                                "tenant_id", "company_id", "project_id", "workflow_id",
                                "workflow_run_id", "workflow_step_id", "capability_binding_id",
                                "capability_id", "capability_type", "employee_id",
                                "fallback_used", "fallback_from_model", "fallback_reason",
                                "usage_record_id", "logical_call_id", "attempt_no",
                                "question", "context_summary", "responsible_id",
                                "assignee_id", "resume_parameters", "session_id", "progress",
                                "artifacts", "permissions", "computer_access", "resume_supported", "cancel_supported", "artifact_receipts", "skill_packages", "skill_file_reads", "browser_tool_calls", "agent_authorization_ref", "native_model_profile",
                            )
                            if key in result
                        }
                    )
                    selected_tool = candidate
                    current_input = result["output"]
                    step_result = result
                    break
                except Exception as error:
                    last_error = error
                    trace.append(self._trace_step(step_index, candidate, current_input, "", str(error)))
                    from .agent_adapter import AgentExecutionError, CodexExecutionHeld
                    if (type(error) is CodexExecutionHeld
                            or (isinstance(error, AgentExecutionError) and
                                (error.outbound_attempted or error.status in {"cancelled", "authorization_revoked", "reservation_unknown", "outcome_unknown", "supervisor_unavailable"}))
                            or (getattr(error, "outbound_attempted", False) and getattr(error, "status", "") == "network_error")):
                        # Never replay an uncertain call or bypass a held executor.
                        break
            if step_result is None:
                raise ToolExecutionError(str(last_error), trace, last_error)

        return {
            "tool_name": selected_tool or "",
            "output": current_input,
            "cost": round(total_cost, 8),
            "model_gateway_id": model_gateway_id,
            "model_name": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "token": total_tokens,
            "estimated_cost": round(estimated_cost, 8),
            "status": status,
            "credential_id": credential_id,
            "credential_ref_digest": credential_ref_digest,
            "trace": trace,
            **audit_metadata,
        }

    def _trace_step(self, step: int, tool_name: str, input_text: str, output: str, error: str | None = None) -> dict:
        if tool_name in LOCAL_RD_TOOL_IDS:
            input_text = output = ""
        item = {
            "step": step,
            "tool": tool_name,
            "input": input_text,
            "output": output,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if error:
            item["error"] = error
        return item

    def _fallback_chain(self, tool_name: str) -> list[str]:
        if tool_name in LOCAL_RD_TOOL_IDS:
            return [tool_name]
        fallbacks = {
            "codex_tool": ["codex_tool", "gpt_tool", "default_tool"],
            "gpt_tool": ["gpt_tool", "claude_tool", "default_tool"],
            "claude_tool": ["claude_tool", "gpt_tool", "default_tool"],
            "default_tool": ["default_tool"],
            _REAL_RD_TOOL_NAME: [_REAL_RD_TOOL_NAME],  # 无 fallback
        }
        result = fallbacks.get(tool_name, [tool_name, "default_tool"])
        if tool_name == _REAL_RD_TOOL_NAME:
            _logger.info("real_rd_executor_tool selected for step")
        return result


class ToolExecutionError(RuntimeError):
    def __init__(self, message: str, trace: list[dict], cause: Exception | None = None):
        super().__init__(message)
        self.trace = trace
        self.cause = cause
        self.http_status = int(getattr(cause, "http_status", 0) or 0)
        self.status = str(getattr(cause, "status", "failed"))
        self.outbound_attempted = bool(getattr(cause, "outbound_attempted", False))
