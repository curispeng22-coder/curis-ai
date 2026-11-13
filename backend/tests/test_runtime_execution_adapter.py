from __future__ import annotations

import asyncio

from app.database import Database
from app.runtime import RuntimeFoundation, SimulationRuntime
from app.runtime.execution_adapter import RuntimeExecutionAdapter, RuntimeExecutionError
from app.runtime.workspace import WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-runtime-execution"
COMPANY = "company-runtime-execution"


def _workspace(database: Database) -> tuple[dict, dict, dict]:
    database.initialize()
    with TenantContext.scope(TENANT, ceo_id="ceo", role="test"):
        with database.connect() as connection:
            connection.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo', 'Execution Company')",
                (COMPANY, TENANT),
            )
        seed_canonical_business(database, TENANT, COMPANY, "business-rd")
        workspace = WorkspaceRuntime(database).create_workspace(
            company_id=COMPANY,
            business_ref="business-rd",
            business_type="RD",
            name="研发办公室",
            blueprint_version="v1",
            blueprint={
                "stages": ["INTAKE", "DESIGN", "IMPLEMENT", "VERIFY", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE"],
                "agentRefs": ["engineering-ai"],
                "capabilityRefs": ["model"],
                "connectorRefs": [],
                "evidenceRules": ["NON_FIXTURE_REQUIRED"],
            },
        )
        cycle = WorkspaceRuntime(database).create_cycle(
            company_id=COMPANY,
            workspace_id=workspace["workspace"]["workspace_id"],
            blueprint_version="v1",
            owner_ref="Engineering AI",
            outcome_ref="可用增量",
            intent_ref="完善 Curis",
            execution_ref="workflow_run:wfr-real",
        )
        run = SimulationRuntime(database).create(
            company_id=COMPANY,
            ceo_id="ceo",
            scenario_id="RD-001",
            blueprint_version="v1",
            workspace_id=workspace["workspace"]["workspace_id"],
            subject_id=cycle["entity_id"],
        )
        run = SimulationRuntime(database).transition(run["simulation_run_id"], "RUNNING", actor="CEO", trigger="start")
        return workspace["workspace"], cycle, run


def test_execution_creates_unverified_evidence_and_handoff(tmp_path):
    database = Database(str(tmp_path / "runtime-execution.sqlite"))
    with TenantContext.scope(TENANT, ceo_id="ceo", role="test"):
        workspace, cycle, run = _workspace(database)

        async def execute(request):
            assert request["company_id"] == COMPANY
            assert request["workspace_id"] == workspace["workspace_id"]
            return {"status": "succeeded", "execution_ref": request["execution_ref"], "output": "真实执行摘要"}

        result = asyncio.run(RuntimeExecutionAdapter(
            RuntimeFoundation(database), SimulationRuntime(database), execute,
        ).execute(run, RuntimeFoundation(database).get(cycle["entity_id"])))

        assert result["lifecycle_status"] == "RUNNING"
        assert result["final_state"] == "EXECUTED_UNVERIFIED"
        assert len(result["evidence_refs"]) == 1
        assert result["handoffs"][0]["status"] == "WAITING_CEO"
        evidence = RuntimeFoundation(database).get(result["evidence_refs"][0])
        assert evidence["verification_status"] == "UNVERIFIED"
        assert evidence["data"]["fixture"] is False
        assert evidence["data"]["source"] == "AI_EXECUTION"
        repeated = asyncio.run(RuntimeExecutionAdapter(
            RuntimeFoundation(database), SimulationRuntime(database),
            lambda _: (_ for _ in ()).throw(AssertionError("duplicate execution")),
        ).execute(result, RuntimeFoundation(database).get(cycle["entity_id"])))
        assert repeated["evidence_refs"] == result["evidence_refs"]


def test_execution_without_binding_fails_closed(tmp_path):
    database = Database(str(tmp_path / "runtime-execution-missing.sqlite"))
    with TenantContext.scope(TENANT, ceo_id="ceo", role="test"):
        _workspace_data, cycle, run = _workspace(database)
        foundation = RuntimeFoundation(database)
        foundation.attach_execution_ref(cycle["entity_id"], "")
        try:
            asyncio.run(RuntimeExecutionAdapter(
                foundation, SimulationRuntime(database), lambda _: {"status": "succeeded"},
            ).execute(run, foundation.get(cycle["entity_id"])))
        except RuntimeExecutionError as error:
            assert error.code == "execution_binding_required"
        else:  # pragma: no cover - assertion guard
            raise AssertionError("missing execution binding must fail closed")


def test_execution_failure_is_not_success_evidence(tmp_path):
    database = Database(str(tmp_path / "runtime-execution-failure.sqlite"))
    with TenantContext.scope(TENANT, ceo_id="ceo", role="test"):
        _workspace_data, cycle, run = _workspace(database)
        foundation = RuntimeFoundation(database)
        result = asyncio.run(RuntimeExecutionAdapter(
            foundation, SimulationRuntime(database), lambda _: {"status": "failed", "error": "worker unavailable"},
        ).execute(run, foundation.get(cycle["entity_id"])))
        assert result["lifecycle_status"] == "WAITING_CEO"
        assert result["final_state"] == "EXECUTION_FAILED"
        assert result["evidence_refs"] == []
        assert result["failure_events"][0]["kind"] == "AI_EXECUTION"
