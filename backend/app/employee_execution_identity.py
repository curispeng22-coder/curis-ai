"""Canonical bridge between Curis business Employees and provider execution facts.

Runtime ``AI_EMPLOYEE`` remains the canonical business identity.  The legacy
Company Employee is only an execution identity and Provider payloads never get
to choose either identity.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .database import Database
from .resource_scope_policy import ResourceScopePolicy
from .runtime import RuntimeScopeError
from .tenant_context import TenantContext


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(value: str | None) -> dict[str, Any]:
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


class EmployeeExecutionIdentity:
    """Resolve and verify existing identities without owning their lifecycle."""

    def __init__(self, database: Database):
        self.db = database

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def bind(
        self,
        *,
        company_id: str,
        workspace_id: str | None = None,
        runtime_employee_ref: str,
        company_employee_ref: str,
        employee_capability_binding_ref: str,
    ) -> dict[str, Any]:
        """Persist one explicit, scope-checked execution identity bridge."""
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            runtime = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and (workspace_id is null or workspace_id=?) and entity_id=? and entity_type='AI_EMPLOYEE'",
                (self.tenant_id, company_id, workspace_id, runtime_employee_ref),
            ).fetchone()
            if runtime is None:
                raise RuntimeScopeError("Employee execution identity is outside the active scope")
            data = _json(runtime["data_json"])
            current = str(data.get("companyEmployeeRef") or "")
            if current and current != company_employee_ref:
                raise ValueError("Runtime Employee already has another execution identity")
            employee = connection.execute(
                "select id, name, role, status from employee_instances where tenant_id=? "
                "and company_id=? and id=? and enabled=1 and deleted_at is null "
                "and status in ('idle','assigned')",
                (self.tenant_id, company_id, company_employee_ref),
            ).fetchone()
            binding = connection.execute(
                "select id, capability_source, capability_type, capability_id from "
                "employee_capability_bindings where tenant_id=? and employee_id=? and id=? and enabled=1",
                (self.tenant_id, company_employee_ref, employee_capability_binding_ref),
            ).fetchone()
            if employee is None or binding is None:
                raise RuntimeScopeError("Employee execution identity is outside the active scope")
            bridge = {
                "status": "VERIFIED",
                "source": "EXECUTION_ASSIGNMENT",
                "companyEmployeeRef": company_employee_ref,
                "verifiedByEmployeeCapabilityBindingRef": employee_capability_binding_ref,
                "verifiedAt": at,
            }
            data = data | {"companyEmployeeRef": company_employee_ref, "identityBridge": bridge}
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and company_id=? "
                "and (workspace_id is null or workspace_id=?) and entity_id=? and entity_type='AI_EMPLOYEE'",
                (
                    json.dumps(data, ensure_ascii=False), at, self.tenant_id, company_id,
                    workspace_id, runtime_employee_ref,
                ),
            )
        return {
            "runtime_employee_ref": runtime_employee_ref,
            "company_employee_ref": company_employee_ref,
            "identity_status": "VERIFIED_EXPLICIT_BRIDGE",
            "bridge": bridge,
            "employee": dict(employee),
        }

    def record_task_assignment(
        self,
        *,
        company_id: str,
        workspace_id: str | None = None,
        assignment_ref: str | None = None,
        assignment_revision: int | None = None,
        runtime_employee_ref: str,
        task_ref: str,
        employee_capability_binding_ref: str,
    ) -> dict[str, Any]:
        """Bind one Task to its canonical Runtime Employee in the append-only log."""
        identity = self.resolve(
            company_id=company_id,
            workspace_id=workspace_id,
            runtime_employee_ref=runtime_employee_ref,
        )
        if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
            raise ValueError("Task assignment requires an explicit Employee execution bridge")
        with self.db.connect() as connection:
            task = connection.execute(
                "select * from tasks "
                "where tenant_id=? and task_id=?",
                (self.tenant_id, task_ref),
            ).fetchone()
            binding = connection.execute(
                "select id, capability_source, capability_type, capability_id from "
                "employee_capability_bindings where tenant_id=? and employee_id=? and id=? and enabled=1",
                (
                    self.tenant_id, identity["company_employee_ref"],
                    employee_capability_binding_ref,
                ),
            ).fetchone()
            if (
                task is None
                or binding is None
                or task["company_id"] != company_id
                or task["employee_id"] != identity["company_employee_ref"]
                or task["requested_capability_source"] != binding["capability_source"]
                or task["requested_capability_type"] != binding["capability_type"]
                or task["requested_capability_id"] != binding["capability_id"]
            ):
                raise RuntimeScopeError("Task assignment does not match the Employee execution bridge")
            existing = connection.execute(
                "select event_id, payload, created_at from evolution_events where tenant_id=? "
                "and correlation_id=? and event_type='execution.identity_bound' order by event_id",
                (self.tenant_id, task_ref),
            ).fetchall()
            expected = {
                "task_id": task_ref,
                "company_id": company_id,
                "workspace_id": workspace_id,
                "runtime_employee_ref": runtime_employee_ref,
                "company_employee_ref": identity["company_employee_ref"],
                "employee_capability_binding_ref": employee_capability_binding_ref,
                "capability_source": binding["capability_source"],
                "capability_type": binding["capability_type"],
                "capability_id": binding["capability_id"],
            }
            if task["scope_type"] or task["scope_ref"]:
                scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=self.tenant_id, record=dict(task))
                if workspace_id != scope["workspace_id"]:
                    raise RuntimeScopeError("Task assignment scope conflicts with execution context")
                authorized = ResourceScopePolicy.authorize_assignment(
                    connection, tenant_id=self.tenant_id, company_id=company_id,
                    assignment_ref=assignment_ref, employee_ref=runtime_employee_ref,
                    revision=assignment_revision, scope=scope,
                )
                expected.update({key: authorized[key] for key in ("scope_type", "scope_ref", "assignment_ref", "assignment_revision")})
            if existing:
                payloads = [_json(row["payload"]) for row in existing]
                if len(existing) == 1 and all(payloads[0].get(key) == value for key, value in expected.items()):
                    return {**expected, "evidence_event_ref": str(existing[0]["event_id"])}
                raise ValueError("Task already has another canonical Employee assignment")
            cursor = connection.execute(
                "insert into evolution_events(correlation_id, event_type, payload, tenant_id, idempotency_key) "
                "values (?, 'execution.identity_bound', ?, ?, ?)",
                (
                    task_ref, json.dumps(expected, ensure_ascii=False), self.tenant_id,
                    f"execution-identity:{self.tenant_id}:{task_ref}",
                ),
            )
        return {**expected, "evidence_event_ref": str(cursor.lastrowid)}

    def resolve(
        self, *, company_id: str, workspace_id: str | None = None, runtime_employee_ref: str,
    ) -> dict[str, Any]:
        """Resolve an explicit bridge; exact-ID fallback exists only for old records."""
        with self.db.connect() as connection:
            runtime = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and (workspace_id is null or workspace_id=?) and entity_id=? and entity_type='AI_EMPLOYEE'",
                (self.tenant_id, company_id, workspace_id, runtime_employee_ref),
            ).fetchone()
            if runtime is None:
                raise RuntimeScopeError("Runtime Employee is outside the current execution context")
            data = _json(runtime["data_json"])
            explicit_ref = str(data.get("companyEmployeeRef") or "")
            company_employee_ref = explicit_ref or runtime_employee_ref
            employee = connection.execute(
                "select id, name, role, status from employee_instances where tenant_id=? "
                "and company_id=? and id=? and enabled=1 and deleted_at is null",
                (self.tenant_id, company_id, company_employee_ref),
            ).fetchone()
        if employee is None:
            raise RuntimeScopeError("Runtime Employee has no active Company execution identity")
        return {
            "runtime_employee_ref": runtime_employee_ref,
            "company_employee_ref": company_employee_ref,
            "identity_status": (
                "VERIFIED_EXPLICIT_BRIDGE" if explicit_ref else "EXACT_ID_FALLBACK"
            ),
            "bridge": data.get("identityBridge") if explicit_ref else None,
            "employee": dict(employee),
        }

    def verify_task_callback(
        self,
        *,
        company_id: str,
        workspace_id: str | None = None,
        runtime_employee_ref: str,
        task_ref: str,
        session_ref: str,
        allow_unverified: bool = False,
    ) -> dict[str, Any]:
        """Verify callback provenance from persisted Task and UsageEvent facts."""
        identity = self.resolve(
            company_id=company_id,
            workspace_id=workspace_id,
            runtime_employee_ref=runtime_employee_ref,
        )
        if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
            raise ValueError("Provider callback requires an explicit Employee execution bridge")
        with self.db.connect() as connection:
            task = connection.execute(
                "select * from tasks "
                "where tenant_id=? and task_id=?",
                (self.tenant_id, task_ref),
            ).fetchone()
            events = connection.execute(
                "select event_id, event_type, payload, created_at from evolution_events where tenant_id=? "
                "and correlation_id=? and event_type in ('usage.task_execution', 'usage.model_call') "
                "order by event_id desc",
                (self.tenant_id, task_ref),
            ).fetchall()
            assignments = connection.execute(
                "select event_id, payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='execution.identity_bound' order by event_id",
                (self.tenant_id, task_ref),
            ).fetchall()
        if (
            task is None
            or task["company_id"] != company_id
            or task["employee_id"] != identity["company_employee_ref"]
        ):
            raise RuntimeScopeError("Task callback does not match the persisted Employee binding")
        assigned = [
            row for row in assignments
            if (payload := _json(row["payload"]))
            and payload.get("task_id") == task_ref
            and payload.get("company_id") == company_id
            and payload.get("workspace_id") == workspace_id
            and payload.get("runtime_employee_ref") == runtime_employee_ref
            and payload.get("company_employee_ref") == identity["company_employee_ref"]
        ]
        if len(assignments) != 1 or len(assigned) != 1:
            raise ValueError("Task has no unique canonical Employee assignment")
        assignment = _json(assigned[0]["payload"])
        with self.db.connect() as connection:
            if task["scope_type"] or task["scope_ref"]:
                scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=self.tenant_id, record=dict(task))
                ResourceScopePolicy.require_same_execution_scope(
                    scope, {**assignment, "tenant_id": self.tenant_id},
                )
                ResourceScopePolicy.authorize_assignment(
                    connection, tenant_id=self.tenant_id, company_id=company_id,
                    assignment_ref=assignment.get("assignment_ref"), employee_ref=runtime_employee_ref,
                    revision=assignment.get("assignment_revision"), scope=scope,
                )
            binding = connection.execute(
                "select id, capability_source, capability_type, capability_id from "
                "employee_capability_bindings where tenant_id=? and employee_id=? and id=? and enabled=1",
                (
                    self.tenant_id, identity["company_employee_ref"],
                    assignment.get("employee_capability_binding_ref"),
                ),
            ).fetchone()
        if (
            binding is None
            or task["requested_capability_source"] != binding["capability_source"]
            or task["requested_capability_type"] != binding["capability_type"]
            or task["requested_capability_id"] != binding["capability_id"]
            or assignment.get("capability_source") != binding["capability_source"]
            or assignment.get("capability_type") != binding["capability_type"]
            or assignment.get("capability_id") != binding["capability_id"]
        ):
            raise RuntimeScopeError("Task callback capability provenance is no longer valid")
        matched = next(
            (
                (row, payload)
                for row in events
                if (payload := _json(row["payload"]))
                and payload.get("task_id") == task_ref
                and payload.get("employee_id") == identity["company_employee_ref"]
                and payload.get("capability_source") == binding["capability_source"]
                and (not payload.get("company_id") or payload.get("company_id") == company_id)
                and (not payload.get("workspace_id") or payload.get("workspace_id") == workspace_id)
                and (
                    (
                        row["event_type"] == "usage.task_execution"
                        and bool(session_ref)
                        and payload.get("session_id") == session_ref
                    )
                    or (
                        row["event_type"] == "usage.model_call"
                        and binding["capability_type"] == "model"
                        and payload.get("capability_type") == "model"
                        and payload.get("capability_id") == binding["capability_id"]
                        and payload.get("status") == "success"
                    )
                )
            ),
            None,
        )
        if matched is None:
            if allow_unverified:
                return {
                    "verification_status": "UNVERIFIED",
                    "callback_actor_ref": runtime_employee_ref,
                    "company_employee_ref": identity["company_employee_ref"],
                    "task_ref": task_ref,
                    "task_status": task["status"],
                    "session_ref": session_ref or None,
                    "reason": "NO_MATCHING_EXECUTION_EVIDENCE",
                }
            raise ValueError("Provider callback has no matching execution evidence")
        event, payload = matched
        return {
            "verification_status": "VERIFIED",
            "callback_actor_ref": runtime_employee_ref,
            "company_employee_ref": identity["company_employee_ref"],
            "task_ref": task_ref,
            "task_status": task["status"],
            "provider_capability": {
                "source": binding["capability_source"],
                "type": binding["capability_type"],
                "id": binding["capability_id"],
                "binding_ref": binding["id"],
            },
            "session_ref": session_ref or None,
            "provider_request_ref": payload.get("request_id"),
            "execution_status": payload.get("status") or "UNKNOWN",
            "evidence_event_ref": str(event["event_id"]),
            "verified_at": event["created_at"],
        }

    def verify_handoff_ack(
        self,
        *,
        company_id: str,
        workspace_id: str | None,
        cycle_ref: str,
        target_employee_ref: str,
        task_ref: str,
        session_ref: str,
    ) -> dict[str, Any]:
        """Verify a Provider-native ACK; the Domain still owns the transition."""
        with self.db.connect() as connection:
            cycle = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id is ? and entity_id=? and entity_type='CYCLE'",
                (self.tenant_id, company_id, workspace_id, cycle_ref),
            ).fetchone()
            if cycle is None:
                raise RuntimeScopeError("Handoff Cycle is outside the current Workspace")
            handoff_projection = _json(cycle["data_json"]).get("responsibilityHandoff") or {}
            handoff_ref = str(handoff_projection.get("handoffRef") or "")
            handoff = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id is ? and entity_id=? and entity_type='HANDOFF'",
                (self.tenant_id, company_id, workspace_id, handoff_ref),
            ).fetchone()
            task = connection.execute("select * from tasks where tenant_id=? and company_id=? and task_id=?",
                (self.tenant_id, company_id, task_ref)).fetchone()
            if task is not None and (task["scope_type"] or task["scope_ref"]):
                actual = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=self.tenant_id, record=dict(task))
                for item in (cycle, handoff):
                    if item is None:
                        raise RuntimeScopeError("Handoff scope is missing")
                    ResourceScopePolicy.require_same_execution_scope(actual,
                        ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=self.tenant_id, record=dict(item)))
        if (
            handoff is None
            or handoff["lifecycle_status"] != "SENT"
            or handoff_projection.get("toEmployeeRef") != target_employee_ref
            or _json(handoff["data_json"]).get("toEmployeeRef") != target_employee_ref
        ):
            raise ValueError("Handoff ACK actor is not the current SENT target")
        provenance = self.verify_task_callback(
            company_id=company_id,
            workspace_id=workspace_id,
            runtime_employee_ref=target_employee_ref,
            task_ref=task_ref,
            session_ref=session_ref,
        )
        return {
            "handoff_ref": handoff_ref,
            "ack_actor_ref": target_employee_ref,
            "verification_status": "VERIFIED",
            "execution_provenance": provenance,
        }
