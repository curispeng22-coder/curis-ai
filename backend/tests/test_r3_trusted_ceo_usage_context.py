from __future__ import annotations

import json

import pytest

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.result_store import ResultStore
from app.tenant_context import TenantContext


def test_usage_audit_uses_service_context_and_references_ledger_only(tmp_path):
    database = Database(str(tmp_path / "usage-context.sqlite"))
    database.initialize()
    store = ResultStore(database, EvolutionEventLog(database))
    usage = {
        "ceo_id": "forged-payload-ceo",
        "request_id": "request-1",
        "subject_id": "subject-digest",
        "subject_digest": "subject-digest",
        "company_id": "company-a",
        "project_id": "project-a",
        "workflow_id": "official.workflow.software_rnd_sop",
        "workflow_run_id": "run-a",
        "workflow_step_id": "step-a",
        "employee_id": "employee-a",
        "capability_binding_id": "binding-a",
        "usage_record_id": "usage-a",
        "model_gateway_id": "openai-newapi-controlled",
        "model_name": "gpt-5.4-mini-2026-03-17",
        "prompt_tokens": 10,
        "completion_tokens": 5,
        "total_tokens": 15,
        "estimated_cost": 0.01,
        "price_version": "2026-07-17",
        "status": "success",
    }

    with TenantContext.scope(
        "tenant-a",
        subject_id="raw-subject",
        company_id="company-a",
        ceo_id="trusted-ceo",
        role="owner",
        membership_status="active",
        request_id="request-1",
    ):
        store._record_usage_events("task-a", "model_gateway_tool", 0.01, usage)

    with database.connect() as connection:
        payload = json.loads(
            connection.execute(
                "select payload from evolution_events where event_type='usage.tool_call'"
            ).fetchone()[0]
        )
    assert payload["ceo_id"] == "trusted-ceo"
    assert payload["subject_digest"] == "subject-digest"
    assert payload["usage_record_id"] == "usage-a"
    for key in (
        "tenant_id", "company_id", "project_id", "workflow_run_id", "workflow_step_id",
        "employee_id", "capability_binding_id", "status", "request_id",
    ):
        assert key in payload
    for forbidden in (
        "prompt_tokens", "completion_tokens", "total_tokens", "estimated_cost",
        "price_version", "credential_id",
    ):
        assert forbidden not in payload


def test_usage_event_fails_closed_without_service_context_ceo(tmp_path):
    database = Database(str(tmp_path / "missing-usage-context.sqlite"))
    database.initialize()
    store = ResultStore(database, EvolutionEventLog(database))

    with TenantContext.scope("tenant-a", subject_id="subject", company_id="company-a"):
        with pytest.raises(RuntimeError, match="trusted CEO UsageContext"):
            store._record_usage_events(
                "task-a",
                "model_gateway_tool",
                0,
                {"ceo_id": "forged-payload-ceo"},
            )
