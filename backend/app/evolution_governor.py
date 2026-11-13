from __future__ import annotations

import uuid
from typing import Any

from .governor_sandbox import GovernorSandbox
from .result_store import ResultStore


class EvolutionGovernor:
    policy = ["STABILITY", "OPTIMIZATION", "EVOLUTION"]

    def __init__(self, store: ResultStore, event_log=None):
        self.store = store
        self.event_log = event_log

    def evaluate(
        self,
        *,
        task: dict[str, Any],
        workflow_plan: list[dict[str, Any]],
        result: dict[str, Any],
        inefficiencies: list[str],
    ) -> dict[str, Any]:
        correlation_id = str(uuid.uuid4())
        trace = result.get("trace", [])
        failed_steps = [step for step in trace if step.get("error")]
        failure_rate = len(failed_steps) / len(trace) if trace else 0.0
        step_count = len(workflow_plan)
        total_cost = float(result.get("cost", 0))
        latency_increase = max(0.0, (step_count - 3) * 0.10)
        workflow_inefficiency = max(0.0, (step_count - 3) / 3)
        thresholds_met = []
        if failure_rate >= 0.30:
            thresholds_met.append("failure_rate")
        if latency_increase >= 0.20:
            thresholds_met.append("latency_increase")
        if workflow_inefficiency >= 0.50 or inefficiencies:
            thresholds_met.append("workflow_inefficiency")

        target_module = self._target_module(inefficiencies)
        locked_modules = {item["module_name"] for item in self.store.list_architecture_locks()}
        locked_module_blocked = target_module in locked_modules
        proposal = None
        if thresholds_met:
            proposal = {
                "proposal_type": "controlled_self_rewrite",
                "target_module": target_module,
                "change_summary": self._proposal_summary(inefficiencies),
                "requires_approval": True,
                "automatic_application": False,
            }

        if proposal is not None and self.event_log is not None:
            self.event_log.record(correlation_id=correlation_id, event_type="proposal", payload=proposal)

        risk_analysis = {
            "stability_risk": {
                "level": "high" if failure_rate >= 0.30 else "low",
                "failure_rate": failure_rate,
            },
            "regression_risk": {
                "level": "medium" if thresholds_met else "low",
                "affected_steps": [step.get("action") for step in workflow_plan],
            },
            "locked_module_risk": {
                "blocked": locked_module_blocked,
                "target_module": target_module,
                "locked_modules": sorted(locked_modules),
            },
            "rollback_risk": {
                "level": "controlled" if thresholds_met else "minimal",
                "rollback_record_required": bool(thresholds_met),
            },
        }

        if not thresholds_met:
            decision = "do_not_evolve"
        elif locked_module_blocked or failure_rate >= 0.30:
            decision = "postpone_evolution"
        else:
            decision = "evolve"

        self.store.save_evolution_simulation(
            task_id=task["task_id"],
            task_flow=[step.get("action") for step in workflow_plan],
            tool_routing=[step.get("tool_required") for step in workflow_plan],
            workflow_graph=[
                {
                    "from": workflow_plan[index - 1].get("action") if index > 0 else "task",
                    "to": step.get("action"),
                }
                for index, step in enumerate(workflow_plan)
            ],
            performance_impact={
                "current_step_count": step_count,
                "estimated_step_reduction": max(0, step_count - 3) if proposal else 0,
                "current_cost": total_cost,
                "latency_increase": latency_increase,
            },
            correlation_id=correlation_id,
        )
        self.store.save_rollback_record(
            task_id=task["task_id"],
            previous_architecture="Tool System v1.6 meta-development loop",
            stable_version="Tool System v1.8 pre-evolution baseline",
            performance_comparison={
                "current_step_count": step_count,
                "current_cost": total_cost,
                "thresholds_met": thresholds_met,
            },
            correlation_id=correlation_id,
        )
        decision_record = self.store.save_evolution_decision(
            task_id=task["task_id"],
            policy=self.policy,
            decision=decision,
            threshold_evaluation={
                "failure_rate": failure_rate,
                "latency_increase": latency_increase,
                "workflow_inefficiency": workflow_inefficiency,
                "thresholds_met": thresholds_met,
            },
            proposal=proposal,
            risk_analysis=risk_analysis,
            automatic_code_modification_allowed=False,
            correlation_id=correlation_id,
        )
        decision_record["correlation_id"] = correlation_id
        return decision_record

    def demonstrate(self, proposal: dict[str, Any], *, dry_run: bool = True) -> dict[str, Any]:
        # Additive demonstration substrate. Does NOT change evaluate()'s decision
        # logic. Any real production mutation still requires the explicit
        # human-approval path outside this sandbox (gate not lifted).
        snapshot = {"architecture_locks": self.store.list_architecture_locks()}
        sandbox = GovernorSandbox(snapshot)
        return sandbox.run(proposal, dry_run=dry_run)

    def _target_module(self, inefficiencies: list[str]) -> str:
        if "workflow_length" in inefficiencies:
            return "workflow_optimizer"
        if "codex_overuse" in inefficiencies or "tool_failure" in inefficiencies:
            return "tool_router"
        return "execution_quality"

    def _proposal_summary(self, inefficiencies: list[str]) -> str:
        if not inefficiencies:
            return "No rewrite proposal; current system remains stable."
        return "Prepare an approval-gated optimization for: " + ", ".join(inefficiencies)
