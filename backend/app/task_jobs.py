from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException

from .tenant_context import TenantContext


logger = logging.getLogger(__name__)


def build_task_job_router(store, orchestrator) -> APIRouter:
    router = APIRouter()

    def job_payload(task_id: str) -> dict:
        task = store.get_task(task_id)
        model_usage = None
        if store.event_log is not None:
            for event in reversed(store.event_log.get_by_correlation_id(task_id)):
                if event["event_type"] == "usage.model_call":
                    payload = event["payload"]
                    usage_record_id = payload.get("usage_record_id")
                    with store.database.connect() as connection:
                        record = connection.execute(
                            "select * from ai_usage_records "
                            "where tenant_id = ? and usage_record_id = ?",
                            (TenantContext.current_tenant_id(), usage_record_id),
                        ).fetchone()
                    if record is not None:
                        record = dict(record)
                        model_usage = {
                            "model_gateway_id": record["model_gateway_id"],
                            "model_name": record["model_name"],
                            "prompt_tokens": record["input_tokens"],
                            "completion_tokens": record["output_tokens"],
                            "total_tokens": record["total_tokens"],
                            "estimated_cost": (
                                float(record["cost_amount"])
                                if record["cost_source"] == "estimated"
                                and record["cost_amount"] is not None
                                else None
                            ),
                            "currency": record["currency"],
                            "fallback_used": bool(record["fallback_from_model"]),
                            "fallback_from_model": record["fallback_from_model"] or "",
                            "fallback_reason": record["fallback_reason"] or "",
                        }
                    break
        status = {
            "INIT": "queued",
            "PENDING": "queued",
            "PARSED": "running",
            "RUNNING": "running",
            "AWAITING_INPUT": "awaiting_input",
            "HUMAN_HANDOFF": "human_handoff",
            "RESUMED": "resumed",
            "COMPLETED": "completed",
            "FAILED": "failed",
            "CANCELLED": "cancelled",
        }.get(task["status"], task["status"].lower())
        return {
            "job_id": task_id,
            "task_id": task_id,
            "project_id": task["project_id"],
            "status": status,
            "task_status": task["status"],
            "state_flow": task["state_flow"],
            "output": task["output"],
            "error": task["error"],
            "selected_tool": task["selected_tool"],
            "cost": task["cost"],
            "context_package_id": task.get("context_package_id") or "",
            "executions": store.list_executions(task_id),
            "model_usage": model_usage,
        }

    async def run_task(task_id: str, tenant_id: str, identity: dict[str, str]) -> None:
        try:
            with TenantContext.scope(
                tenant_id,
                subject_id=identity.get("subject_id", ""),
                company_id=identity.get("company_id", ""),
                ceo_id=identity.get("ceo_id", ""),
                role=identity.get("role", ""),
                membership_status=identity.get("membership_status", ""),
                request_id=identity.get("request_id", ""),
            ):
                await orchestrator.run(task_id)
        except Exception as error:
            logger.warning("Task job failed: %s (%s)", task_id, type(error).__name__)

    @router.post(
        "/api/workspace/projects/{project_id}/tasks/{task_id}/jobs",
        status_code=202,
    )
    def start_task_job(project_id: str, task_id: str, background_tasks: BackgroundTasks):
        try:
            task = store.get_task(task_id)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        if task["project_id"] != project_id:
            raise HTTPException(status_code=404, detail="task not found in project")
        if task["status"] in {"INIT", "FAILED"}:
            store.transition(task_id, "PENDING")
            background_tasks.add_task(
                run_task,
                task_id,
                TenantContext.current_tenant_id(),
                TenantContext.current_identity(),
            )
        return job_payload(task_id)

    @router.get("/api/workspace/jobs/{job_id}")
    def get_task_job(job_id: str):
        try:
            return job_payload(job_id)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    return router
