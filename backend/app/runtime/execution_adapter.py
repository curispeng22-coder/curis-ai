"""Bridge a Runtime Simulation to an existing, scoped execution substrate.

The bridge deliberately keeps the legacy executor behind ``executionRef``. Runtime
owns the business evidence and review state; the legacy run only supplies execution
output and telemetry.
"""

from __future__ import annotations

import inspect
import json
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

from .foundation import RuntimeFoundation, RuntimeScopeError
from .simulation import SimulationRuntime


class RuntimeExecutionError(RuntimeError):
    """A safe, user-facing execution bridge failure."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


ExecutionFn = Callable[[dict[str, Any]], dict[str, Any] | Awaitable[dict[str, Any]]]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _summary(value: Any, limit: int = 4000) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return text[:limit]


class RuntimeExecutionAdapter:
    """Execute one current Simulation without importing legacy lifecycle states."""

    def __init__(self, foundation: RuntimeFoundation, simulations: SimulationRuntime,
                 executor: ExecutionFn | None = None):
        self.foundation = foundation
        self.simulations = simulations
        self.executor = executor

    async def run_bound(self, request: dict[str, Any]) -> dict[str, Any]:
        """Run one explicit child execution without changing Runtime business state."""
        if self.executor is None:
            raise RuntimeExecutionError("execution_unavailable")
        execution_ref = str(request.get("execution_ref") or "").strip()
        if not execution_ref:
            raise RuntimeExecutionError("execution_binding_required")
        if not (
            execution_ref.startswith("workflow_run:")
            or execution_ref.startswith("content_workflow:")
            or execution_ref == "rd_task:auto"
        ):
            raise RuntimeExecutionError("execution_ref_unsupported")
        try:
            result = self.executor(request)
            if inspect.isawaitable(result):
                result = await result
        except RuntimeExecutionError:
            raise
        except Exception as error:  # pragma: no cover - adapter boundary safety
            raise RuntimeExecutionError("execution_failed") from error
        if not isinstance(result, dict):
            raise RuntimeExecutionError("execution_result_invalid")
        return result

    async def execute(self, run: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any]:
        if self.executor is None:
            raise RuntimeExecutionError("execution_unavailable")
        if run.get("lifecycle_status") != "RUNNING":
            raise RuntimeExecutionError("simulation_not_running")
        if run.get("invalidated_at"):
            raise RuntimeExecutionError("simulation_invalidated")
        if run.get("final_state") in {"EXECUTED_UNVERIFIED", "EXECUTION_FAILED"}:
            return run
        if subject.get("company_id") != run.get("company_id") or subject.get("workspace_id") != run.get("workspace_id"):
            raise RuntimeScopeError("execution subject is outside the simulation scope")
        with self.foundation.db.connect() as connection:
            workspace = connection.execute(
                "select blueprint_version from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.foundation.tenant_id, run["company_id"], run["workspace_id"]),
            ).fetchone()
        if workspace is None or workspace["blueprint_version"] != run.get("blueprint_version"):
            raise RuntimeExecutionError("blueprint_not_current")
        execution_ref = str(subject.get("execution_ref") or "").strip()

        request = {
            "simulation_run_id": run["simulation_run_id"],
            "scenario_id": run["scenario_id"],
            "company_id": run["company_id"],
            "workspace_id": run["workspace_id"],
            "blueprint_version": run["blueprint_version"],
            "subject_id": subject["entity_id"],
            "execution_ref": execution_ref,
            "subject": {
                "entity_type": subject.get("entity_type"),
                "owner_ref": subject.get("owner_ref"),
                "data": subject.get("data") or {},
            },
        }
        result = await self.run_bound(request)

        status = str(result.get("status") or "").lower()
        output = result.get("output")
        if status not in {"success", "succeeded", "completed"}:
            failure_id = f"failure-{run['simulation_run_id']}-{int(datetime.now().timestamp())}"
            self.simulations.append(run["simulation_run_id"], "failure_events", {
                "failureId": failure_id,
                "kind": "AI_EXECUTION",
                "status": status or "failed",
                "executionRef": execution_ref,
                "summary": _summary(result.get("error") or output, 1000),
                "occurredAt": _now(),
            })
            self.simulations.set_final_state(run["simulation_run_id"], "EXECUTION_FAILED")
            self.simulations.transition(
                run["simulation_run_id"], "WAITING_CEO", actor="SYSTEM",
                trigger="execution_failed", reason="AI 执行失败，等待 CEO 处理",
            )
            return self.simulations.get(run["simulation_run_id"])

        evidence = self.foundation.create(
            "EVIDENCE",
            company_id=run["company_id"],
            workspace_id=run["workspace_id"],
            parent_id=run["simulation_run_id"],
            owner_ref=subject.get("owner_ref") or "AI Employee",
            verification_status="UNVERIFIED",
            evidence_condition="CURRENT",
            data={
                "fixture": False,
                "source": "AI_EXECUTION",
                "executionRef": execution_ref,
                "status": "UNVERIFIED",
                "summary": _summary(output),
                "receivedAt": _now(),
                "metadata": {key: result[key] for key in ("workflow_run_id", "run_id", "model_name", "total_tokens", "estimated_cost") if key in result},
            },
        )
        self.simulations.append(run["simulation_run_id"], "evidence_refs", evidence["entity_id"])
        self.simulations.append(run["simulation_run_id"], "handoffs", {
            "from": subject.get("owner_ref") or "AI Employee",
            "to": "CEO",
            "executionRef": execution_ref,
            "evidenceRefs": [evidence["entity_id"]],
            "status": "WAITING_CEO",
            "at": _now(),
        })
        self.simulations.set_final_state(run["simulation_run_id"], "EXECUTED_UNVERIFIED")
        self.foundation.attach_execution_ref(
            subject["entity_id"], execution_ref,
            {"executionStatus": "COMPLETED", "executionReceivedAt": _now()},
        )
        return self.simulations.get(run["simulation_run_id"])
