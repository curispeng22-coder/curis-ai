from __future__ import annotations

import json

import pytest

from app.database import Database
from app.employee_execution_identity import EmployeeExecutionIdentity
from app.evolution_event_log import EvolutionEventLog
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.models import ensure_ceo_day_schema
from app.shared_workspace_projection import SharedWorkspaceProjection
from app.tenant_context import TenantContext


TENANT = "tenant-employee-trust"
COMPANY = "company-employee-trust"
WORKSPACE = "workspace-employee-trust"
RUNTIME_EMPLOYEE = "runtime-employee-reviewer"
COMPANY_EMPLOYEE = "company-employee-reviewer"
BINDING = "employee-binding-codex"


def _seed(path) -> tuple[Database, str, str]:
    database = Database(str(path))
    database.initialize()
    ensure_ceo_day_schema(database)
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, 'ceo-trust', 'Trust Company')",
            (COMPANY, TENANT),
        )
        connection.execute(
            "insert into business_directions(direction_id, tenant_id, name, template_type, target_outcome, lifecycle_status) "
            "values ('business-trust', ?, 'Trust Business', 'CUSTOM', 'Trusted result', 'OPERATING')",
            (TENANT,),
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, blueprint_version) "
            "values (?, ?, ?, 'business-trust', 'Trust Workspace', 'OPERATING', 'v1')",
            (WORKSPACE, TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_templates(id, name, role, source, tenant_id) "
            "values ('reviewer-template', '代码审核员', '代码审核员', 'tenant_private', ?)",
            (TENANT,),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values (?, ?, ?, '', 'reviewer-template', '林审', '代码审核员', 'idle')",
            (COMPANY_EMPLOYEE, TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, capability_type, capability_id) "
            "values (?, ?, ?, 'tenant_private', 'agent', 'agent.codex')",
            (BINDING, TENANT, COMPANY_EMPLOYEE),
        )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        foundation = RuntimeFoundation(database)
        foundation.create(
            "AI_EMPLOYEE", entity_id=RUNTIME_EMPLOYEE, company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="AVAILABLE",
            data={"name": "林审", "responsibility": "检查代码结果"},
        )
        identity = EmployeeExecutionIdentity(database)
        identity.bind(
            company_id=COMPANY,
            workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE,
            company_employee_ref=COMPANY_EMPLOYEE,
            employee_capability_binding_ref=BINDING,
        )
        store = ResultStore(database)
        task = store.create_task(
            "检查代码结果", company_id=COMPANY, project_id="project-trust",
            capability_source="tenant_private", capability_type="agent",
            capability_id="agent.codex", employee_id=COMPANY_EMPLOYEE,
            employee_role="代码审核员", employee_name="林审",
        )
        task = store.transition(task["task_id"], "COMPLETED", {"output": "审核完成"})
        identity.record_task_assignment(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task["task_id"],
            employee_capability_binding_ref=BINDING,
        )
        event = EvolutionEventLog(database).record(
            correlation_id=task["task_id"], event_type="usage.task_execution",
            tenant_id=TENANT, idempotency_key=f"trust:{task['task_id']}",
            payload={
                "task_id": task["task_id"], "company_id": COMPANY,
                "employee_id": COMPANY_EMPLOYEE, "capability_source": "tenant_private",
                "capability_type": "task", "capability_id": "task_execution",
                "session_id": "session-codex-1", "status": "success",
            },
        )
        handoff = foundation.create(
            "HANDOFF", entity_id="handoff-trust", company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="SENT",
            data={"toEmployeeRef": RUNTIME_EMPLOYEE},
        )
        foundation.create(
            "CYCLE", entity_id="cycle-trust", company_id=COMPANY,
            workspace_id=WORKSPACE, lifecycle_status="RUNNING",
            data={
                "responsibilityHandoff": {
                    "handoffRef": handoff["entity_id"], "toEmployeeRef": RUNTIME_EMPLOYEE,
                },
            },
        )
    return database, task["task_id"], str(event["event_id"])


def test_explicit_bridge_callback_handoff_and_restart(tmp_path):
    database, task_ref, event_ref = _seed(tmp_path / "identity.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        identity = EmployeeExecutionIdentity(database)
        resolved = identity.resolve(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE,
        )
        assert resolved["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE"
        assert resolved["company_employee_ref"] == COMPANY_EMPLOYEE

        provenance = identity.verify_task_callback(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
            session_ref="session-codex-1",
        )
        assert provenance == {
            **provenance,
            "verification_status": "VERIFIED",
            "callback_actor_ref": RUNTIME_EMPLOYEE,
            "company_employee_ref": COMPANY_EMPLOYEE,
            "evidence_event_ref": event_ref,
        }
        ack = identity.verify_handoff_ack(
            company_id=COMPANY, workspace_id=WORKSPACE, cycle_ref="cycle-trust",
            target_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
            session_ref="session-codex-1",
        )
        assert ack["verification_status"] == "VERIFIED"
        assert ack["ack_actor_ref"] == RUNTIME_EMPLOYEE
        assert RuntimeFoundation(database).get("handoff-trust")["lifecycle_status"] == "SENT"
        with database.connect() as connection:
            cycle = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and entity_id='cycle-trust'",
                (TENANT,),
            ).fetchone()
            data = json.loads(cycle["data_json"])
            data["executionBinding"] = {"callbackProvenance": provenance}
            connection.execute(
                "update runtime_entities set data_json=? where tenant_id=? and entity_id='cycle-trust'",
                (json.dumps(data), TENANT),
            )
        foundation = RuntimeFoundation(database)
        foundation.create(
            "EVIDENCE", entity_id="evidence-trust", company_id=COMPANY,
            workspace_id=WORKSPACE, parent_id="cycle-trust", owner_ref=RUNTIME_EMPLOYEE,
            lifecycle_status="CURRENT", verification_status="VERIFIED",
            evidence_condition="CURRENT", data={"summary": "真实审核证据"},
        )
        foundation.create(
            "OUTCOME", entity_id="outcome-trust", company_id=COMPANY,
            workspace_id=WORKSPACE, parent_id="cycle-trust", owner_ref=RUNTIME_EMPLOYEE,
            lifecycle_status="CURRENT", verification_status="VERIFIED",
            evidence_condition="CURRENT", data={"summary": "真实审核结果"},
        )
        projection = SharedWorkspaceProjection(database)
        for reference in ("evidence-trust", "outcome-trust"):
            result = projection.result(COMPANY, WORKSPACE, reference)
            assert result["owner_ref"] == RUNTIME_EMPLOYEE
            assert result["execution_provenance"]["callback_actor_ref"] == RUNTIME_EMPLOYEE

    reopened = Database(str(tmp_path / "identity.sqlite"))
    reopened.initialize()
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        assert EmployeeExecutionIdentity(reopened).verify_task_callback(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
            session_ref="session-codex-1",
        )["verification_status"] == "VERIFIED"
        employee = SharedWorkspaceProjection(reopened).employee(
            COMPANY, WORKSPACE, RUNTIME_EMPLOYEE,
        )
        assert employee["company_employee_ref"] == COMPANY_EMPLOYEE
        assert employee["organization_record"]["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE"


def test_bridge_and_callback_fail_closed(tmp_path):
    database, task_ref, _ = _seed(tmp_path / "fail-closed.sqlite")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        identity = EmployeeExecutionIdentity(database)
        with pytest.raises(ValueError, match="another execution identity"):
            identity.bind(
                company_id=COMPANY, workspace_id=WORKSPACE,
                runtime_employee_ref=RUNTIME_EMPLOYEE,
                company_employee_ref="forged-employee",
                employee_capability_binding_ref="forged-binding",
            )
        with pytest.raises(ValueError, match="no matching execution evidence"):
            identity.verify_task_callback(
                company_id=COMPANY, workspace_id=WORKSPACE,
                runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
                session_ref="forged-session",
            )
        with pytest.raises(RuntimeScopeError, match="Task callback"):
            with database.connect() as connection:
                connection.execute(
                    "update tasks set employee_id='forged-employee' where tenant_id=? and task_id=?",
                    (TENANT, task_ref),
                )
            identity.verify_task_callback(
                company_id=COMPANY, workspace_id=WORKSPACE,
                runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
                session_ref="session-codex-1",
            )


def test_unverified_failure_is_formal_not_trusted(tmp_path):
    database, task_ref, _ = _seed(tmp_path / "unverified.sqlite")
    with database.connect() as connection:
        connection.execute(
            "delete from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='usage.task_execution'",
            (TENANT, task_ref),
        )
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        result = EmployeeExecutionIdentity(database).verify_task_callback(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref,
            session_ref="", allow_unverified=True,
        )
        assert result["verification_status"] == "UNVERIFIED"
        assert result["reason"] == "NO_MATCHING_EXECUTION_EVIDENCE"


def test_model_callback_uses_scoped_model_usage_evidence_without_agent_session(tmp_path):
    database, task_ref, _ = _seed(tmp_path / "model-callback.sqlite")
    with database.connect() as connection:
        connection.execute(
            "update employee_capability_bindings set capability_type='model', capability_id='model.deepseek' "
            "where tenant_id=? and id=?",
            (TENANT, BINDING),
        )
        connection.execute(
            "update tasks set requested_capability_type='model', requested_capability_id='model.deepseek' "
            "where tenant_id=? and task_id=?",
            (TENANT, task_ref),
        )
        assignment = connection.execute(
            "select event_id, payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='execution.identity_bound'",
            (TENANT, task_ref),
        ).fetchone()
        payload = json.loads(assignment["payload"])
        payload.update({"capability_type": "model", "capability_id": "model.deepseek"})
        connection.execute(
            "update evolution_events set payload=? where event_id=?",
            (json.dumps(payload), assignment["event_id"]),
        )
        connection.execute(
            "delete from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='usage.task_execution'",
            (TENANT, task_ref),
        )
    event = EvolutionEventLog(database).record(
        correlation_id=task_ref, event_type="usage.model_call", tenant_id=TENANT,
        idempotency_key=f"model-callback:{task_ref}",
        payload={
            "task_id": task_ref, "company_id": COMPANY, "workspace_id": WORKSPACE,
            "employee_id": COMPANY_EMPLOYEE, "capability_source": "tenant_private",
            "capability_type": "model", "capability_id": "model.deepseek",
            "request_id": "request-deepseek-1", "status": "success",
        },
    )

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo-trust", role="test"):
        result = EmployeeExecutionIdentity(database).verify_task_callback(
            company_id=COMPANY, workspace_id=WORKSPACE,
            runtime_employee_ref=RUNTIME_EMPLOYEE, task_ref=task_ref, session_ref="",
        )
        assert result["verification_status"] == "VERIFIED"
        assert result["session_ref"] is None
        assert result["provider_request_ref"] == "request-deepseek-1"
        assert result["evidence_event_ref"] == str(event["event_id"])
