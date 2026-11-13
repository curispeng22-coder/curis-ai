"""Minimal shared responsibility assignment and deterministic routing runtime.

This is additive beside the legacy sequential WorkflowRuntime.  It stores
assignments and immutable workflow snapshots in the existing Runtime Foundation,
routes an existing Work object, and reuses HANDOFF / DECISION_PACKET lifecycles.
"""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..database import Database
from ..model_gateway import redact_model_gateway_text
from ..resource_scope_policy import ResourceScopePolicy
from ..tenant_context import TenantContext
from .foundation import RuntimeFoundation, RuntimeScopeError
from .registry import get_registered_machine


SCOPES = frozenset(ResourceScopePolicy.EXECUTION_SCOPES)
SIGNALS = frozenset({
    "CONTINUE", "COMPLETED", "RETURN", "NEED_RESPONSIBILITY",
    "NEED_LEADER", "DECISION_GATE", "TERMINAL", "CONSULT", "REVIEW",
    "HANDOFF", "WAIT",
})
ACTION_ALIASES = {
    "STAY_AND_CONTINUE": "CONTINUE",
    "RETURN_OR_REVISION": "RETURN",
    "ESCALATE": "NEED_LEADER",
    "WAIT_DECISION": "DECISION_GATE",
    "COMPLETE_CYCLE": "TERMINAL",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _unique(values: list[str] | None, *, limit: int = 32) -> list[str]:
    return list(dict.fromkeys(str(value) for value in values or [] if str(value).strip()))[:limit]


class ResponsibilityRoutingError(ValueError):
    pass


class HumanInputInvalid(ResponsibilityRoutingError):
    """Malformed or unsafe user supplied Human Input."""


class ResponsibilityRoutingRuntime:
    """Canonical scoped Assignment plus opt-in routing for an existing Work."""

    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def _entity(self, entity_id: str, *, entity_type: str | None = None) -> dict[str, Any]:
        item = self.foundation.get(entity_id)
        if entity_type and item["entity_type"] != entity_type:
            raise ResponsibilityRoutingError(f"{entity_id} is not {entity_type}")
        return item

    def _validate_scope(
        self, *, company_id: str, scope_type: str, scope_ref: str, workspace_id: str | None
    ) -> tuple[str, str]:
        kind = scope_type.upper()
        if kind not in SCOPES or not scope_ref:
            raise ResponsibilityRoutingError("explicit canonical execution scope is required")
        with self.db.connect() as conn:
            try:
                scope = ResourceScopePolicy.resolve_execution_scope(
                    conn, tenant_id=self.tenant_id, company_id=company_id,
                    scope_type=kind, scope_ref=scope_ref,
                )
                if workspace_id != scope["workspace_id"]:
                    raise ValueError("Assignment scope conflicts with Workspace provenance")
            except ValueError as error:
                raise RuntimeScopeError(str(error)) from error
        return kind, scope_ref

    def _validate_employee(self, employee_ref: str, company_id: str, workspace_id: str | None) -> dict:
        employee = self._entity(employee_ref, entity_type="AI_EMPLOYEE")
        if employee["company_id"] != company_id:
            raise RuntimeScopeError("Assignment Employee is outside the Company")
        if employee["workspace_id"] not in (None, workspace_id):
            raise RuntimeScopeError("Assignment Employee is outside the Workspace")
        if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
            raise ResponsibilityRoutingError("Assignment Employee is not available")
        return employee

    def create_assignment(
        self,
        *,
        company_id: str,
        scope_type: str,
        scope_ref: str,
        role_ref: str,
        employee_ref: str,
        responsibility_key: str,
        responsibility: str,
        workspace_id: str | None = None,
        capability_binding_refs: list[str] | None = None,
        input_contract: dict[str, Any] | None = None,
        output_contract: dict[str, Any] | None = None,
        is_leader: bool = False,
        assignment_id: str | None = None,
    ) -> dict:
        kind, scope = self._validate_scope(
            company_id=company_id, scope_type=scope_type, scope_ref=scope_ref, workspace_id=workspace_id
        )
        employee = self._validate_employee(employee_ref, company_id, workspace_id)
        role = self._entity(role_ref, entity_type="ROLE_SLOT")
        if role["company_id"] != company_id or role["workspace_id"] not in (None, workspace_id):
            raise RuntimeScopeError("Assignment Role is outside the requested scope")
        capability_refs = _unique(capability_binding_refs)
        for ref in capability_refs:
            binding = self._entity(ref, entity_type="CAPABILITY_BINDING")
            if binding["company_id"] != company_id or binding["workspace_id"] not in (None, workspace_id):
                raise RuntimeScopeError("Capability Binding is outside the requested scope")
        key, definition = responsibility_key.strip(), responsibility.strip()
        if not key or not definition:
            raise ResponsibilityRoutingError("responsibility key and definition are required")
        assignment = self.foundation.create(
            "RESPONSIBILITY_ASSIGNMENT",
            entity_id=assignment_id,
            company_id=company_id,
            workspace_id=workspace_id,
            owner_ref=employee["entity_id"],
            data={
                "scopeType": kind,
                "scopeRef": scope,
                "roleRef": role_ref,
                "employeeRef": employee_ref,
                "responsibilityKey": key,
                "responsibility": definition,
                "isLeader": bool(is_leader),
                "capabilityBindingRefs": capability_refs,
                "inputContract": dict(input_contract or {}),
                "outputContract": dict(output_contract or {}),
                "revision": 1,
            },
        )
        self.foundation.link(assignment["entity_id"], "ASSIGNED_EMPLOYEE", employee_ref)
        self.foundation.link(assignment["entity_id"], "USES_ROLE", role_ref)
        for ref in capability_refs:
            self.foundation.link(assignment["entity_id"], "REQUIRES_CAPABILITY_BINDING", ref)
        return assignment

    def create_assignment_in_connection(self, connection, *, company_id, scope_type, scope_ref,
            role_ref, employee_ref, responsibility_key, responsibility, workspace_id=None,
            capability_binding_refs=None, input_contract=None, output_contract=None, is_leader=False):
        """Initial-team writes only; transaction ownership stays with the caller."""
        if not connection.in_transaction:
            raise ResponsibilityRoutingError("Assignment requires its caller-owned transaction")
        kind = scope_type.upper()
        try:
            scope = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=self.tenant_id,
                company_id=company_id, scope_type=kind, scope_ref=scope_ref)
            if workspace_id != scope["workspace_id"]:
                raise ValueError("Assignment scope conflicts with Workspace provenance")
        except ValueError as error:
            raise RuntimeScopeError(str(error)) from error
        def scoped(entity_id, entity_type):
            row = connection.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type=?",
                (self.tenant_id, company_id, entity_id, entity_type)).fetchone()
            if row is None or row["workspace_id"] not in (None, workspace_id):
                raise RuntimeScopeError("Assignment reference is outside the requested scope")
            return row
        employee = scoped(employee_ref, "AI_EMPLOYEE")
        if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
            raise ResponsibilityRoutingError("Assignment Employee is not available")
        company_ref = json.loads(employee["data_json"] or "{}").get("companyEmployeeRef")
        if not company_ref or connection.execute("select 1 from employee_instances where tenant_id=? and company_id=? and id=? "
                "and enabled=1 and deleted_at is null and status in ('idle','assigned')",
                (self.tenant_id, company_id, company_ref)).fetchone() is None:
            raise RuntimeScopeError("Initial Assignment requires a real Company Employee")
        role = scoped(role_ref, "ROLE_SLOT")
        if role["lifecycle_status"] not in {"ASSIGNED", "OPERATING"}:
            raise ResponsibilityRoutingError("Assignment Role is not available")
        refs = _unique(capability_binding_refs)
        for ref in refs:
            scoped(ref, "CAPABILITY_BINDING")
        key, definition = responsibility_key.strip(), responsibility.strip()
        if not key or not definition:
            raise ResponsibilityRoutingError("responsibility key and definition are required")
        entity_id, at = str(uuid4()), _now()
        data = {"scopeType": kind, "scopeRef": scope_ref, "roleRef": role_ref, "employeeRef": employee_ref,
            "responsibilityKey": key, "responsibility": definition, "isLeader": bool(is_leader),
            "capabilityBindingRefs": refs, "inputContract": dict(input_contract or {}),
            "outputContract": dict(output_contract or {}), "revision": 1}
        connection.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,owner_ref,lifecycle_status,"
            "verification_status,evidence_condition,data_json,created_at,updated_at) values (?,?,'RESPONSIBILITY_ASSIGNMENT',?,?,?,'ACTIVE','UNVERIFIED','MISSING',?,?,?)",
            (entity_id, self.tenant_id, company_id, workspace_id, employee_ref, json.dumps(data, ensure_ascii=False), at, at))
        for relation, target in [("ASSIGNED_EMPLOYEE", employee_ref), ("USES_ROLE", role_ref)] + [("REQUIRES_CAPABILITY_BINDING", ref) for ref in refs]:
            connection.execute("insert into runtime_links(link_id,tenant_id,company_id,source_id,relation,target_id,created_at) values (?,?,?,?,?,?,?)",
                (str(uuid4()), self.tenant_id, company_id, entity_id, relation, target, at))
        return {"entity_id": entity_id, "data": data}

    def update_assignment(
        self,
        assignment_id: str,
        *,
        employee_ref: str | None = None,
        responsibility: str | None = None,
        input_contract: dict[str, Any] | None = None,
        output_contract: dict[str, Any] | None = None,
    ) -> dict:
        assignment = self._entity(assignment_id, entity_type="RESPONSIBILITY_ASSIGNMENT")
        data = dict(assignment["data"])
        if employee_ref is not None:
            self._validate_employee(employee_ref, assignment["company_id"], assignment["workspace_id"])
            data["employeeRef"] = employee_ref
        if responsibility is not None:
            if not responsibility.strip():
                raise ResponsibilityRoutingError("responsibility definition cannot be empty")
            data["responsibility"] = responsibility.strip()
        if input_contract is not None:
            data["inputContract"] = dict(input_contract)
        if output_contract is not None:
            data["outputContract"] = dict(output_contract)
        data["revision"] = int(data.get("revision") or 1) + 1
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            conn.execute(
                "update runtime_entities set owner_ref=?, data_json=?, updated_at=? "
                "where tenant_id=? and entity_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT'",
                (data["employeeRef"], json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, assignment_id),
            )
            if employee_ref is not None:
                conn.execute(
                    "delete from runtime_links where tenant_id=? and source_id=? and relation='ASSIGNED_EMPLOYEE'",
                    (self.tenant_id, assignment_id),
                )
                conn.execute(
                    "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
                    "values (lower(hex(randomblob(16))), ?, ?, ?, ?, 'ASSIGNED_EMPLOYEE', ?, ?)",
                    (self.tenant_id, assignment["company_id"], assignment["workspace_id"], assignment_id, employee_ref, _now()),
                )
        return self.foundation.get(assignment_id)

    @staticmethod
    def _assignment_snapshot(assignment: dict) -> dict[str, Any]:
        data = assignment["data"]
        return {
            "assignmentRef": assignment["entity_id"],
            "assignmentRevision": data["revision"],
            "responsibilityKey": data["responsibilityKey"],
            "responsibility": data["responsibility"],
            "roleRef": data["roleRef"],
            "employeeRef": data["employeeRef"],
            "isLeader": bool(data.get("isLeader")),
            "capabilityBindingRefs": list(data.get("capabilityBindingRefs") or []),
            "inputContract": dict(data.get("inputContract") or {}),
            "outputContract": dict(data.get("outputContract") or {}),
        }

    def publish_workflow(
        self,
        *,
        company_id: str,
        scope_type: str,
        scope_ref: str,
        workflow_key: str,
        assignment_refs: list[str],
        default_flow: list[str],
        workspace_id: str | None = None,
    ) -> dict:
        kind, scope = self._validate_scope(
            company_id=company_id, scope_type=scope_type, scope_ref=scope_ref, workspace_id=workspace_id
        )
        key = workflow_key.strip()
        if not key or not assignment_refs:
            raise ResponsibilityRoutingError("workflow key and assignments are required")
        snapshots = []
        for ref in assignment_refs:
            assignment = self._entity(ref, entity_type="RESPONSIBILITY_ASSIGNMENT")
            data = assignment["data"]
            if assignment["company_id"] != company_id or data["scopeType"] != kind or data["scopeRef"] != scope:
                raise RuntimeScopeError("Workflow Assignment is outside its scope")
            snapshots.append(self._assignment_snapshot(assignment))
        by_key = {item["responsibilityKey"]: item for item in snapshots}
        if (
            len(by_key) != len(snapshots)
            or not default_flow
            or len(default_flow) != len(set(default_flow))
            or not set(default_flow).issubset(by_key)
        ):
            raise ResponsibilityRoutingError("default flow must contain unique known responsibilities")
        existing = [
            item for item in self.foundation.list("RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id)
            if item["data"].get("workflowKey") == key
            and item["data"].get("scopeType") == kind
            and item["data"].get("scopeRef") == scope
        ]
        version = max((int(item["data"].get("version") or 0) for item in existing), default=0) + 1
        default_next = {current: following for current, following in zip(default_flow, default_flow[1:])}
        return self.foundation.create(
            "RESPONSIBILITY_WORKFLOW",
            company_id=company_id,
            workspace_id=workspace_id,
            owner_ref="SYSTEM",
            data={
                "workflowKey": key,
                "version": version,
                "scopeType": kind,
                "scopeRef": scope,
                "assignments": snapshots,
                "defaultFlow": list(default_flow),
                "defaultNext": default_next,
                "publishedAt": _now(),
            },
        )

    def _latest_workflow(
        self, *, company_id: str, workspace_id: str | None, scope_type: str, scope_ref: str, workflow_key: str
    ) -> dict:
        candidates = [
            item for item in self.foundation.list("RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id)
            if item["data"].get("workflowKey") == workflow_key
            and item["data"].get("scopeType") == scope_type
            and item["data"].get("scopeRef") == scope_ref
        ]
        if not candidates:
            raise ResponsibilityRoutingError("no published responsibility workflow")
        return max(candidates, key=lambda item: int(item["data"].get("version") or 0))

    @staticmethod
    def _workflow_assignment(workflow: dict, responsibility_key: str) -> dict:
        assignment = next(
            (item for item in workflow["data"]["assignments"] if item["responsibilityKey"] == responsibility_key),
            None,
        )
        if assignment is None:
            raise ResponsibilityRoutingError(f"responsibility is not in pinned workflow: {responsibility_key}")
        return assignment

    def start_work(
        self,
        work_ref: str,
        *,
        scope_type: str,
        scope_ref: str,
        workflow_key: str,
        initial_responsibility: str | None = None,
    ) -> dict:
        work = self._entity(work_ref)
        kind, scope = self._validate_scope(
            company_id=work["company_id"], scope_type=scope_type, scope_ref=scope_ref,
            workspace_id=work["workspace_id"],
        )
        existing = work["data"].get("responsibilityRouting")
        if existing:
            return work
        workflow = self._latest_workflow(
            company_id=work["company_id"], workspace_id=work["workspace_id"],
            scope_type=kind, scope_ref=scope, workflow_key=workflow_key,
        )
        first = initial_responsibility or workflow["data"]["defaultFlow"][0]
        assignment = self._workflow_assignment(workflow, first)
        at = _now()
        routing = {
            "workflowRef": workflow["entity_id"],
            "workflowVersion": workflow["data"]["version"],
            "scopeType": kind,
            "scopeRef": scope,
            "currentAssignmentRef": assignment["assignmentRef"],
            "responsibilityHolderRef": assignment["employeeRef"],
            "currentExecutorRef": None,
            "returnStack": [],
            "status": "ACTIVE",
            "handoffRefs": [],
            "resultRefs": [],
            "artifactRefs": [],
            "evidenceRefs": [],
            "updatedAt": at,
        }
        self._write_work(work, routing, assignment, activity="责任已分配，尚未开始执行。")
        return self.foundation.get(work_ref)

    @staticmethod
    def _work_data(work: dict, routing: dict, assignment: dict, *, activity: str) -> dict:
        data = dict(work["data"])
        context = dict(data.get("workContext") or {})
        context.update({
            "responsibilityAssignmentRef": assignment["assignmentRef"],
            "responsibilityEmployeeRef": routing["responsibilityHolderRef"],
            "responsibilityRoleSlotRef": assignment["roleRef"],
            "currentExecutorRef": routing.get("currentExecutorRef"),
            "status": "idle" if routing["status"] == "ACTIVE" else routing["status"].lower(),
            "activity": activity,
            "updatedAt": routing["updatedAt"],
        })
        data["responsibilityRouting"] = routing
        data["workContext"] = context
        return data

    def _write_work(self, work: dict, routing: dict, assignment: dict, *, activity: str,
                    allow_human_close: bool = False) -> None:
        data = self._work_data(work, routing, assignment, activity=activity)
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            row = conn.execute(
                "select data_json, lifecycle_status from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id is ? and entity_id=? and entity_type=?",
                (self.tenant_id, work["company_id"], work["workspace_id"], work["entity_id"], work["entity_type"]),
            ).fetchone()
            if not row or json.loads(row["data_json"]) != work["data"] or row["lifecycle_status"] != work["lifecycle_status"]:
                raise ResponsibilityRoutingError("Work changed concurrently; reread current truth")
            old_request = (work["data"].get("responsibilityRouting") or {}).get("humanInput")
            if old_request and old_request.get("state") not in {"CLOSED", "INVALIDATED"}:
                new_request = routing.get("humanInput")
                close = (allow_human_close and old_request.get("state") == "CLAIMED"
                         and new_request and new_request.get("state") == "CLOSED"
                         and new_request.get("requestId") == old_request.get("requestId")
                         and new_request.get("continuationKey") == old_request.get("continuationKey"))
                invalidate = (allow_human_close and routing.get("status") == "CANCELLED"
                              and new_request and new_request.get("state") == "INVALIDATED"
                              and new_request.get("requestId") == old_request.get("requestId"))
                if new_request != old_request and not (close or invalidate):
                    raise ResponsibilityRoutingError("Human Input requires its scoped Work command")
            cursor = conn.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and company_id=? "
                "and workspace_id is ? and entity_id=? and entity_type=? and lifecycle_status=? and data_json=?",
                (json.dumps(data, ensure_ascii=False), routing["updatedAt"], self.tenant_id,
                 work["company_id"], work["workspace_id"], work["entity_id"], work["entity_type"], work["lifecycle_status"], row["data_json"]),
            )
            if cursor.rowcount != 1:
                raise ResponsibilityRoutingError("Work changed concurrently; reread current truth")

    @staticmethod
    def _human_digest(value: Any) -> str:
        return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def _human_input_fingerprint(self, conn, row, data: dict, routing: dict) -> str:
        cycle = conn.execute(
            "select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id is ? "
            "and entity_id=? and entity_type='CYCLE'",
            (self.tenant_id, row["company_id"], row["workspace_id"], row["parent_id"]),
        ).fetchone()
        workflow = conn.execute(
            "select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id is ? "
            "and entity_id=? and entity_type='RESPONSIBILITY_WORKFLOW'",
            (self.tenant_id, row["company_id"], row["workspace_id"], routing.get("workflowRef")),
        ).fetchone()
        if not cycle or not workflow:
            raise ResponsibilityRoutingError("Human Input source contract is missing")
        assignments = (json.loads(workflow["data_json"]).get("assignments") or [])
        assignment = next((item for item in assignments if item.get("assignmentRef") == routing.get("currentAssignmentRef")), None)
        if not assignment or assignment.get("employeeRef") != routing.get("responsibilityHolderRef"):
            raise ResponsibilityRoutingError("Human Input assignment changed")
        try:
            scope = ResourceScopePolicy.execution_scope_from_record(conn, tenant_id=self.tenant_id, record=dict(row))
            ResourceScopePolicy.authorize_assignment(
                conn, tenant_id=self.tenant_id, company_id=row["company_id"],
                assignment_ref=assignment["assignmentRef"], employee_ref=assignment["employeeRef"],
                revision=assignment.get("assignmentRevision"), scope=scope,
            )
        except ValueError as error:
            raise ResponsibilityRoutingError("Human Input current assignment or scope changed") from error
        return self._human_digest([
            json.loads(cycle["data_json"]).get("contract"), data.get("inputRefs"),
            routing.get("workflowRef"), routing.get("workflowVersion"),
            routing.get("currentAssignmentRef"), assignment.get("assignmentRevision"),
            routing.get("responsibilityHolderRef"),
        ])

    def _human_row(self, conn, company_id: str, workspace_id: str, work_ref: str):
        row = conn.execute(
            "select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_id=? and entity_type='WORK'",
            (self.tenant_id, company_id, workspace_id, work_ref),
        ).fetchone()
        if not row:
            raise RuntimeScopeError("Original Work is not in this General Workspace")
        data = json.loads(row["data_json"])
        routing = dict(data.get("responsibilityRouting") or {})
        if not routing:
            raise ResponsibilityRoutingError("Original Work has no responsibility route")
        return row, data, routing

    def _human_save(self, conn, row, data: dict, routing: dict, *, activity: str) -> None:
        data["responsibilityRouting"] = routing
        context = dict(data.get("workContext") or {})
        context.update({"status": routing["status"].lower(), "activity": activity, "updatedAt": routing["updatedAt"]})
        data["workContext"] = context
        cursor = conn.execute(
            "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and company_id=? "
            "and workspace_id=? and entity_id=? and entity_type='WORK' and lifecycle_status=? and data_json=?",
            (json.dumps(data, ensure_ascii=False), routing["updatedAt"], self.tenant_id,
             row["company_id"], row["workspace_id"], row["entity_id"], row["lifecycle_status"], row["data_json"]),
        )
        if cursor.rowcount != 1:
            raise ResponsibilityRoutingError("Original Work changed; reread before continuing")

    def finish_user_required_execution(
        self, work_ref: str, *, execution_key: str, task_ref: str, session_ref: str,
        request_fields: dict[str, Any], callback: dict[str, Any], source_output: str,
    ) -> dict[str, Any]:
        """Bind a completed Task request and PARTIAL execution in one original-Work write."""
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            source = conn.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=? and entity_type='WORK'",
                (self.tenant_id, work_ref),
            ).fetchone()
            if not source:
                raise ResponsibilityRoutingError("Original Work does not exist")
            row, data, routing = self._human_row(conn, source["company_id"], source["workspace_id"], work_ref)
            executions = dict(routing.get("executions") or {})
            record = dict(executions.get(execution_key) or {})
            task = conn.execute(
                "select * from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
                (self.tenant_id, row["company_id"], row["workspace_id"], task_ref),
            ).fetchone()
            if (not task or task["status"] != "COMPLETED" or task["work_ref"] != work_ref
                or task["execution_ref"] != execution_key or record.get("taskRef") != task_ref
                or record.get("assignmentRef") != routing.get("currentAssignmentRef")
                or task["employee_id"] != record.get("employeeRef")
                or callback.get("verification_status") != "VERIFIED"
                or callback.get("task_ref") != task_ref or callback.get("task_status") != "COMPLETED"
                or callback.get("callback_actor_ref") != record.get("employeeRef")
                or (callback.get("session_ref") is not None and callback.get("session_ref") != session_ref)
                or task["output"] != source_output
                or row["lifecycle_status"] != "ACTIVE"):
                raise ResponsibilityRoutingError("Human Input Task source is not verified for this Work")
            try:
                stored = json.loads(source_output)
            except (TypeError, ValueError) as error:
                raise ResponsibilityRoutingError("Human Input stored Task output is not a valid contract") from error
            required_top = {"status", "resultType", "humanInput"}
            allowed_top = required_top | {"summary", "problem"}
            if (type(stored) is not dict or not required_top.issubset(stored)
                or set(stored) - allowed_top or stored["status"] != "USER_REQUIRED"
                or type(stored["resultType"]) is not str or not stored["resultType"]
                or any(type(stored[key]) is not str for key in ("summary", "problem") if key in stored)
                or type(stored["humanInput"]) is not dict or type(request_fields) is not dict
                or stored["humanInput"] != request_fields):
                raise ResponsibilityRoutingError("Human Input stored Task output is not a valid contract")
            workflow = conn.execute(
                "select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id is ? "
                "and entity_id=? and entity_type='RESPONSIBILITY_WORKFLOW'",
                (self.tenant_id, row["company_id"], row["workspace_id"], routing.get("workflowRef")),
            ).fetchone()
            assignments = (json.loads(workflow["data_json"]).get("assignments") or []) if workflow else []
            assignment = next((item for item in assignments if item.get("assignmentRef") == record.get("assignmentRef")), None)
            expected_type = ((assignment or {}).get("outputContract") or {}).get("resultType")
            if (type(expected_type) is not str or not expected_type
                or stored["resultType"] != expected_type
                or (assignment or {}).get("employeeRef") != record.get("employeeRef")):
                raise ResponsibilityRoutingError("Human Input result type or Assignment changed")
            fields = ("aiCompleted", "whyUser", "userAction", "destination", "doneCriterion", "resumePlan")
            required_request = {"kind", "targetRef", *fields}
            if not required_request.issubset(request_fields) or set(request_fields) - (required_request | {"evidenceRefs"}):
                raise ResponsibilityRoutingError("Human Input request fields are not exact")
            old = routing.get("humanInput") or {}
            if record.get("status") == "PARTIAL" and record.get("humanInputSource") is True:
                if old.get("sourceTaskRef") == task_ref and old.get("sourceExecutionKey") == execution_key:
                    self._human_current(conn, row["company_id"], row["workspace_id"], work_ref,
                                        old["requestId"], old["revision"])
                    return {"work": self.foundation.get(work_ref), "request": old, "duplicate": True}
                raise ResponsibilityRoutingError("Human Input source already finalized differently")
            if record.get("status") != "RUNNING" or old:
                raise ResponsibilityRoutingError("Human Input cannot replace an existing Work request")
            kind = request_fields.get("kind")
            if type(kind) is not str or kind not in {"LOCAL_INFORMATION", "EXTERNAL_ACTION_REPORT"}:
                raise ResponsibilityRoutingError("Human Input kind is invalid")
            if request_fields.get("targetRef") != work_ref:
                raise ResponsibilityRoutingError("Human Input target is outside the original Work")
            for key in fields:
                value = request_fields.get(key)
                if (type(value) is not str or not value.strip() or len(value.encode("utf-8")) > 1000
                    or redact_model_gateway_text(value) != value):
                    raise ResponsibilityRoutingError("Human Input request is incomplete or unsafe")
            refs = request_fields.get("evidenceRefs", [])
            if not isinstance(refs, list) or len(refs) > 16 or any(type(ref) is not str or ref not in (routing.get("evidenceRefs") or []) for ref in refs):
                raise ResponsibilityRoutingError("Human Input evidence reference is outside this Work")
            source_hash = hashlib.sha256(str(task["output"] or "").encode()).hexdigest()
            request_id = "human-" + self._human_digest([self.tenant_id, work_ref, task_ref, execution_key])[:32]
            at = _now()
            request = {
                "requestId": request_id, "revision": 1, "state": "WAITING_INPUT", "kind": kind,
                **{key: request_fields[key].strip() for key in fields},
                "companyId": row["company_id"], "workspaceId": row["workspace_id"], "workRef": work_ref,
                "cycleRef": row["parent_id"], "workflowRef": routing.get("workflowRef"),
                "workflowVersion": routing.get("workflowVersion"),
                "assignmentRef": routing.get("currentAssignmentRef"),
                "holderRef": routing.get("responsibilityHolderRef"),
                "sourceTaskRef": task_ref, "sourceExecutionKey": execution_key,
                "sourceOutputSha256": source_hash, "sourceCallbackStatus": "VERIFIED_BOUND_TASK_ONLY",
                "targetRef": work_ref, "inputFingerprint": self._human_input_fingerprint(conn, row, data, routing),
                "actionVersion": self._human_digest([source_hash, kind, *[request_fields[key] for key in fields]]),
                "waitCondition": "USER_REPORT_AND_RECHECK", "expiresAt": None,
                "evidenceRefs": refs, "report": None, "verification": "UNKNOWN", "continuationKey": None,
                "createdAt": at,
            }
            record.update({"status": "PARTIAL", "resultStatus": "PARTIAL", "resultRef": None,
                           "humanInputSource": True, "humanInputRequestId": request_id,
                           "sessionRef": session_ref or None, "resultSummary": "等待用户提供必要信息或报告",
                           "provenance": callback, "updatedAt": at})
            executions[execution_key] = record
            routing.update({"executions": executions, "humanInput": request, "currentExecutorRef": None,
                            "status": "WAITING", "lastAction": "EMPLOYEE_RESULT_PARTIAL", "updatedAt": at})
            self._human_save(conn, row, data, routing, activity="原工作等待用户必要动作；外部事实尚未核实。")
        return {"work": self.foundation.get(work_ref), "request": request, "duplicate": False}

    def _human_current(self, conn, company_id: str, workspace_id: str, work_ref: str,
                       request_id: str, revision: int):
        row, data, routing = self._human_row(conn, company_id, workspace_id, work_ref)
        request = dict(routing.get("humanInput") or {})
        if request.get("requestId") != request_id or request.get("revision") != revision:
            raise ResponsibilityRoutingError("Human Input request changed; reread original Work")
        if row["lifecycle_status"] in {"PAUSED", "CANCELLED", "COMPLETED", "ARCHIVED"}:
            raise ResponsibilityRoutingError("Original Work lifecycle no longer allows Human Input")
        if routing.get("status") in {"CANCELLED", "COMPLETED"} or request.get("state") in {"CLOSED", "INVALIDATED"}:
            raise ResponsibilityRoutingError("Human Input is no longer active on the original Work")
        if request.get("expiresAt"):
            try:
                expires = datetime.fromisoformat(request["expiresAt"])
            except (TypeError, ValueError) as error:
                raise ResponsibilityRoutingError("Human Input expiry is invalid") from error
            if expires.tzinfo is None or expires <= datetime.now(timezone.utc):
                raise ResponsibilityRoutingError("Human Input request has expired")
        if (request.get("inputFingerprint") != self._human_input_fingerprint(conn, row, data, routing)
            or request.get("targetRef") != work_ref or request.get("assignmentRef") != routing.get("currentAssignmentRef")
            or request.get("holderRef") != routing.get("responsibilityHolderRef")):
            raise ResponsibilityRoutingError("Human Input scope or version changed")
        return row, data, routing, request

    def report_human_input(self, company_id: str, workspace_id: str, work_ref: str, *,
                           request_id: str, revision: int, submission_id: str, kind: str,
                           local_text: str = "", reference_refs: list[str] | None = None,
                           manual_source: str = "", actor: str) -> dict[str, Any]:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            _, previous_data, previous_routing = self._human_row(conn, company_id, workspace_id, work_ref)
            previous = previous_routing.get("humanInput") or {}
            prior_report = previous.get("report") or {}
            submitted_text = local_text.strip() if kind == "LOCAL_INFORMATION" else manual_source.strip()
            if (previous.get("requestId") == request_id and previous.get("revision") == revision + 1
                and prior_report.get("submissionId") == submission_id
                and previous.get("kind") == kind
                and prior_report.get("text") == submitted_text
                and prior_report.get("referenceRefs") == (reference_refs or [])):
                self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision + 1)
                from .general_execution_limits import work_limits as read_general_limits
                if read_general_limits(self.db, work_ref):
                    raise ResponsibilityRoutingError("Original limited Work cannot offer another actionable response")
                return {"work": self.foundation.get(work_ref), "request": previous, "duplicate": True}
            row, data, routing, request = self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision)
            if request.get("state") != "WAITING_INPUT" or request.get("kind") != kind:
                raise ResponsibilityRoutingError("Human Input report does not match the active request")
            refs = reference_refs or []
            if len(refs) > 16 or any(type(ref) is not str or ref not in (data.get("inputRefs") or []) for ref in refs):
                raise HumanInputInvalid("Human Input reference is outside this Work")
            if kind == "LOCAL_INFORMATION":
                if not local_text.strip() and not refs or manual_source:
                    raise HumanInputInvalid("Local information is missing or mismatched")
                note = local_text.strip()
            elif kind == "EXTERNAL_ACTION_REPORT":
                if not manual_source.strip() or local_text or refs:
                    raise HumanInputInvalid("External action report requires only a manual source")
                note = manual_source.strip()
            else:
                raise HumanInputInvalid("Human Input kind is invalid")
            if (len(note.encode("utf-8")) > 2000 or redact_model_gateway_text(note) != note
                or type(submission_id) is not str or not submission_id.strip()
                or len(submission_id) > 128 or not submission_id.isascii()):
                raise HumanInputInvalid("Human Input report is invalid or contains a known secret pattern")
            request["report"] = {"submissionId": submission_id, "actor": actor, "at": _now(),
                                 "source": "USER_LOCAL_INPUT" if kind == "LOCAL_INFORMATION" else "USER_MANUAL_REPORT",
                                 "text": note, "referenceRefs": refs}
            request.update({"revision": revision + 1,
                            "state": "LOCAL_REPORTED" if kind == "LOCAL_INFORMATION" else "EXTERNAL_REPORTED_UNKNOWN"})
            routing.update({"humanInput": request, "updatedAt": _now()})
            self._human_save(conn, row, data, routing, activity="用户已补充；等待原工作核对。" if kind == "LOCAL_INFORMATION" else "用户已报告外部动作；事实未知，原工作继续等待。")
        return {"work": self.foundation.get(work_ref), "request": request}

    def review_human_input(self, company_id: str, workspace_id: str, work_ref: str, *,
                           request_id: str, revision: int) -> dict[str, Any]:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            _, _, current_routing = self._human_row(conn, company_id, workspace_id, work_ref)
            current = current_routing.get("humanInput") or {}
            if (current.get("requestId") == request_id and current.get("revision") == revision + 1
                and current.get("state") == "READY"):
                self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision + 1)
                from .general_execution_limits import work_limits as read_general_limits
                if read_general_limits(self.db, work_ref):
                    raise ResponsibilityRoutingError("Original limited Work cannot offer another actionable response")
                return {"work": self.foundation.get(work_ref), "request": current, "ready": True, "duplicate": True}
            row, data, routing, request = self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision)
            if request.get("state") == "EXTERNAL_REPORTED_UNKNOWN":
                return {"work": self.foundation.get(work_ref), "request": request, "ready": False}
            if request.get("state") != "LOCAL_REPORTED" or not request.get("report"):
                raise ResponsibilityRoutingError("Human Input has no local report to review")
            request.update({"state": "READY", "revision": revision + 1, "reviewedAt": _now()})
            routing.update({"humanInput": request, "updatedAt": _now()})
            self._human_save(conn, row, data, routing, activity="本地补充已核对；等待一次原工作续接。")
        return {"work": self.foundation.get(work_ref), "request": request, "ready": True}

    def claim_human_input(self, company_id: str, workspace_id: str, work_ref: str, *,
                          request_id: str, revision: int, submission_id: str) -> dict[str, Any]:
        from .general_execution_limits import work_limits as read_general_limits
        if read_general_limits(self.db, work_ref):
            raise ResponsibilityRoutingError("Original limited Work has consumed its single execution")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            _, _, current_routing = self._human_row(conn, company_id, workspace_id, work_ref)
            current = current_routing.get("humanInput") or {}
            if (current.get("requestId") == request_id and current.get("revision") == revision + 1
                and current.get("state") == "CLAIMED" and current.get("continuationKey")
                and (current.get("report") or {}).get("submissionId") == submission_id):
                self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision + 1)
                return {"work": self.foundation.get(work_ref), "request": current,
                        "executionKey": current["continuationKey"], "duplicate": True}
            row, data, routing, request = self._human_current(conn, company_id, workspace_id, work_ref, request_id, revision)
            if request.get("state") != "READY" or request.get("kind") != "LOCAL_INFORMATION":
                raise ResponsibilityRoutingError("Human Input cannot continue from this state")
            if request.get("report", {}).get("submissionId") != submission_id:
                raise ResponsibilityRoutingError("Human Input submission changed")
            if routing.get("status") != "WAITING" or routing.get("currentExecutorRef"):
                raise ResponsibilityRoutingError("Original Work is no longer waiting for this input")
            number = 1 + sum(1 for item in (routing.get("executions") or {}).values()
                             if item.get("assignmentRef") == request["assignmentRef"]
                             and str(item.get("executionKey") or "").startswith("responsibility:"))
            key = f"responsibility:{work_ref}:{request['assignmentRef']}:{number}"
            if key in (routing.get("executions") or {}):
                raise ResponsibilityRoutingError("Human Input continuation key is already claimed")
            request.update({"state": "CLAIMED", "revision": revision + 1,
                            "continuationKey": key, "claimedAt": _now()})
            routing.update({"humanInput": request, "status": "ACTIVE", "lastAction": "HUMAN_INPUT_CONTINUATION",
                            "updatedAt": _now()})
            self._human_save(conn, row, data, routing, activity="同一工作已获准一次续接；等待原执行领取。")
        return {"work": self.foundation.get(work_ref), "request": request, "executionKey": key}

    def build_execution_context(
        self,
        work_ref: str,
        *,
        current_truth_refs: list[str] | None = None,
        compact_context: str = "",
    ) -> dict[str, Any]:
        work = self._entity(work_ref)
        routing = work["data"].get("responsibilityRouting") or {}
        workflow = self._entity(str(routing.get("workflowRef") or ""), entity_type="RESPONSIBILITY_WORKFLOW")
        assignment = next(
            item for item in workflow["data"]["assignments"]
            if item["assignmentRef"] == routing["currentAssignmentRef"]
        )
        refs = _unique([
            work_ref,
            *(current_truth_refs or []),
            *routing.get("resultRefs", []),
            *routing.get("artifactRefs", []),
            *routing.get("evidenceRefs", []),
        ])
        return {
            "workRef": work_ref,
            "workflowRef": workflow["entity_id"],
            "workflowVersion": routing["workflowVersion"],
            "assignment": assignment,
            "truthRefs": refs,
            "compactResponsibilityContext": compact_context.strip()[:1000],
            "contextBudget": {"maxRefs": 32, "maxCompactChars": 1000},
        }

    def begin_employee_execution(
        self,
        work_ref: str,
        *,
        execution_key: str,
        assignment_ref: str | None = None,
    ) -> dict[str, Any]:
        """Persist one provider-execution claim on the pinned Work.

        The claim is the duplicate guard.  Responsibility remains owned by the
        pinned holder; ``currentExecutorRef`` is only the Employee whose provider
        Task is currently running (including a consultant).
        """
        work, routing, workflow, current = self._pinned(work_ref)
        human_input = routing.get("humanInput") or {}
        if human_input and human_input.get("state") not in {"CLOSED", "INVALIDATED"}:
            if human_input.get("state") != "CLAIMED" or human_input.get("continuationKey") != execution_key:
                raise ResponsibilityRoutingError("Human Input blocks a new execution")
        assignment = current if not assignment_ref else next(
            (item for item in workflow["data"]["assignments"] if item["assignmentRef"] == assignment_ref),
            None,
        )
        if assignment is None:
            raise ResponsibilityRoutingError("Execution Assignment is not in the pinned workflow")
        executions = dict(routing.get("executions") or {})
        existing = executions.get(execution_key)
        if existing:
            return {"work": work, "execution": existing, "duplicate": True}
        if routing.get("status") in {"CANCELLED", "COMPLETED"} or any(
            item.get("status") == "UNKNOWN" for item in executions.values()
        ):
            raise ResponsibilityRoutingError("Settled or uncertain Work cannot start another execution")
        if routing.get("currentExecutorRef"):
            raise ResponsibilityRoutingError("Work already has an active Employee execution")
        if int(routing.get("executionCount") or 0) >= int(routing.get("maxExecutions") or 24):
            routing.update({"status": "WAITING", "lastAction": "EXECUTION_LIMIT", "updatedAt": _now()})
            self._write_work(work, routing, current, activity="自动执行已达到安全上限，等待处理。")
            raise ResponsibilityRoutingError("Work reached its provider execution limit")
        at = _now()
        record = {
            "executionKey": execution_key,
            "assignmentRef": assignment["assignmentRef"],
            "employeeRef": assignment["employeeRef"],
            "responsibilityKey": assignment["responsibilityKey"],
            "status": "SUBMITTING",
            "taskRef": None,
            "sessionRef": None,
            "resultStatus": None,
            "createdAt": at,
            "updatedAt": at,
        }
        executions[execution_key] = record
        routing.update({
            "executions": executions,
            "executionCount": int(routing.get("executionCount") or 0) + 1,
            "currentExecutorRef": assignment["employeeRef"],
            "status": "EXECUTING",
            "lastAction": "EMPLOYEE_EXECUTION",
            "updatedAt": at,
        })
        self._write_work(work, routing, current, activity=f"{assignment['responsibility']}负责人正在处理。")
        return {"work": self.foundation.get(work_ref), "execution": record, "duplicate": False}

    def attach_provider_task(self, work_ref: str, *, execution_key: str, task_ref: str) -> dict[str, Any]:
        work, routing, _, current = self._pinned(work_ref)
        executions = dict(routing.get("executions") or {})
        record = dict(executions.get(execution_key) or {})
        if not record:
            raise ResponsibilityRoutingError("Employee execution claim does not exist")
        if record.get("taskRef") and record["taskRef"] != task_ref:
            raise ResponsibilityRoutingError("Employee execution already owns another Provider Task")
        if routing.get("status") == "CANCELLED" or record.get("status") not in {"SUBMITTING", "RUNNING"}:
            raise ResponsibilityRoutingError("Cannot attach a Task to a settled execution")
        record.update({"taskRef": task_ref, "status": "RUNNING", "updatedAt": _now()})
        executions[execution_key] = record
        routing.update({"executions": executions, "updatedAt": record["updatedAt"]})
        self._write_work(work, routing, current, activity="员工已开始执行。")
        return self.foundation.get(work_ref)

    def finish_employee_execution(
        self,
        work_ref: str,
        *,
        execution_key: str,
        status: str,
        task_ref: str,
        session_ref: str,
        result_ref: str | None = None,
        artifact_refs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        result_summary: str = "",
        result_type: str = "",
        provenance: dict[str, Any] | None = None,
        context_metrics: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        work, routing, _, current = self._pinned(work_ref)
        executions = dict(routing.get("executions") or {})
        record = dict(executions.get(execution_key) or {})
        if not record or (record.get("taskRef") and record.get("taskRef") != task_ref):
            raise ResponsibilityRoutingError("Provider result does not match the active execution")
        normalized = status.upper()
        if normalized not in {"ACCEPTED", "REJECTED", "PARTIAL", "FAILED", "CANCELLED", "UNKNOWN"}:
            raise ResponsibilityRoutingError("Unsupported Employee Result status")
        if record.get("status") in {"ACCEPTED", "REJECTED", "PARTIAL", "FAILED", "CANCELLED", "UNKNOWN"}:
            if record.get("status") != normalized or record.get("sessionRef") != (session_ref or None):
                raise ResponsibilityRoutingError("Duplicate Provider callback has different truth")
            return {"work": work, "execution": record, "duplicate": True}
        at = _now()
        result_values = _unique([result_ref] if result_ref else [])
        artifact_values = _unique(artifact_refs)
        evidence_values = _unique(evidence_refs)
        record.update({
            "status": normalized,
            "sessionRef": session_ref or None,
            "resultStatus": normalized,
            "resultRef": result_values[0] if result_values else None,
            "artifactRefs": artifact_values,
            "evidenceRefs": evidence_values,
            "resultSummary": result_summary.strip()[:2000],
            "resultType": result_type.strip()[:128],
            "provenance": dict(provenance or {}),
            "contextMetrics": dict(context_metrics or {}),
            "updatedAt": at,
        })
        executions[execution_key] = record
        routing.update({
            "executions": executions,
            "currentExecutorRef": None,
            "status": ("CANCELLED" if routing.get("status") == "CANCELLED" else
                       "ACTIVE" if normalized == "ACCEPTED" else "WAITING"),
            "resultRefs": _unique([*routing.get("resultRefs", []), *result_values]),
            "artifactRefs": _unique([*routing.get("artifactRefs", []), *artifact_values]),
            "evidenceRefs": _unique([*routing.get("evidenceRefs", []), *evidence_values]),
            "lastAction": f"EMPLOYEE_RESULT_{normalized}",
            "updatedAt": at,
        })
        human_input = dict(routing.get("humanInput") or {})
        close_human = (human_input.get("state") == "CLAIMED"
                       and human_input.get("continuationKey") == execution_key
                       and normalized == "ACCEPTED")
        if close_human:
            human_input.update({"state": "CLOSED", "revision": int(human_input["revision"]) + 1,
                                "closedAt": at})
            routing["humanInput"] = human_input
        self._write_work(
            work, routing, current,
            activity="员工结果已验收。" if normalized == "ACCEPTED" else "员工结果未通过，等待处理。",
            allow_human_close=close_human,
        )
        return {"work": self.foundation.get(work_ref), "execution": record, "duplicate": False}

    def cancel_work(self, work_ref: str, *, reason: str) -> dict[str, Any]:
        work, routing, _, current = self._pinned(work_ref)
        at = _now()
        human_input = dict(routing.get("humanInput") or {})
        invalidated = bool(human_input and human_input.get("state") not in {"CLOSED", "INVALIDATED"})
        if invalidated:
            human_input.update({"state": "INVALIDATED", "revision": int(human_input["revision"]) + 1,
                                "invalidatedAt": at, "invalidatedReason": "ORIGINAL_WORK_CANCELLED"})
            routing["humanInput"] = human_input
        executions = {key: dict(value) for key, value in (routing.get("executions") or {}).items()}
        for record in executions.values():
            if record.get("status") in {"SUBMITTING", "RUNNING"}:
                record.update(status="CANCELLED", resultStatus="CANCELLED", updatedAt=at)
        routing["executions"] = executions
        routing.update({
            "status": "CANCELLED",
            "currentExecutorRef": None,
            "lastAction": "CANCELLED",
            "cancelReason": reason.strip()[:2000],
            "updatedAt": at,
        })
        self._write_work(work, routing, current, activity="工作已停止；已有结果与证据保留。",
                         allow_human_close=invalidated)
        return self.foundation.get(work_ref)

    def _pinned(self, work_ref: str) -> tuple[dict, dict, dict, dict]:
        work = self._entity(work_ref)
        routing = dict(work["data"].get("responsibilityRouting") or {})
        if work["lifecycle_status"] in {"COMPLETED", "CANCELLED", "ARCHIVED"} or not routing or routing.get("status") in {"COMPLETED", "CANCELLED"}:
            raise ResponsibilityRoutingError("Work has no active responsibility route")
        workflow = self._entity(routing["workflowRef"], entity_type="RESPONSIBILITY_WORKFLOW")
        if int(workflow["data"]["version"]) != int(routing["workflowVersion"]):
            raise ResponsibilityRoutingError("pinned workflow version is inconsistent")
        current = next(
            item for item in workflow["data"]["assignments"]
            if item["assignmentRef"] == routing["currentAssignmentRef"]
        )
        if routing.get("responsibilityHolderRef") != current["employeeRef"]:
            raise ResponsibilityRoutingError("Holder does not match the pinned Assignment")
        return work, routing, workflow, current

    @staticmethod
    def _collaboration_context(
        *,
        work_ref: str,
        holder_assignment_ref: str,
        target_assignment_ref: str,
        question: str,
        refs: list[str] | None,
        summary: str,
    ) -> dict[str, Any]:
        bounded_question = question.strip()[:1000]
        bounded_summary = summary.strip()[:600]
        context_refs = _unique([work_ref, *(refs or [])], limit=16)
        text = bounded_question + bounded_summary
        return {
            "workRef": work_ref,
            "holderAssignmentRef": holder_assignment_ref,
            "targetAssignmentRef": target_assignment_ref,
            "question": bounded_question,
            "summary": bounded_summary,
            "contextRefs": context_refs,
            "cost": {
                "chars": len(text),
                "bytes": len(text.encode("utf-8")),
                "refsCount": len(context_refs),
                "hydratedBodiesCount": 0,
                "providerTaskCreatedByRouter": False,
                "providerSessionCreatedByRouter": False,
            },
        }

    def _create_collaboration(self, work: dict, routing: dict, current: dict, record: dict) -> dict:
        key = record["interactionKey"]
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            row = conn.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, work["entity_id"]),
            ).fetchone()
            if row is None:
                raise KeyError(work["entity_id"])
            latest = dict(row)
            latest["data"] = json.loads(latest.pop("data_json"))
            live = dict(latest["data"].get("responsibilityRouting") or {})
            if (live.get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
                raise ResponsibilityRoutingError("Human Input blocks collaboration changes")
            if (
                live.get("workflowRef") != routing["workflowRef"]
                or live.get("workflowVersion") != routing["workflowVersion"]
                or live.get("currentAssignmentRef") != current["assignmentRef"]
                or live.get("responsibilityHolderRef") != current["employeeRef"]
            ):
                raise ResponsibilityRoutingError("Collaboration context changed; retry from current truth")
            collaborations = dict(live.get("collaborations") or {})
            existing = collaborations.get(key)
            if existing:
                identity = ("kind", "targetAssignmentRef", "question")
                if any(existing.get(field) != record.get(field) for field in identity):
                    raise ResponsibilityRoutingError("duplicate collaboration key has different content")
                return existing
            collaborations[key] = record
            live["collaborations"] = collaborations
            live["lastAction"] = record["kind"]
            live["updatedAt"] = record["updatedAt"]
            data = self._work_data(
                latest, live, current,
                activity=("正在等待咨询结果。" if record["kind"] == "CONSULT" else "正在等待审核结果。"),
            )
            changed = conn.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? and data_json=?",
                (json.dumps(data, ensure_ascii=False), record["updatedAt"], self.tenant_id, work["entity_id"], row["data_json"]),
            )
            if changed.rowcount != 1:
                raise ResponsibilityRoutingError("Work changed before collaboration write")
        return record

    def _complete_collaboration(
        self,
        work_ref: str,
        *,
        interaction_key: str,
        kind: str,
        status: str,
        response: str,
        result_refs: list[str] | None,
        artifact_refs: list[str] | None,
        evidence_refs: list[str] | None,
    ) -> tuple[dict, dict]:
        work, routing, workflow, current = self._pinned(work_ref)
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            row = conn.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, work_ref),
            ).fetchone()
            latest = dict(row)
            latest["data"] = json.loads(latest.pop("data_json"))
            live = dict(latest["data"].get("responsibilityRouting") or {})
            if (live.get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
                raise ResponsibilityRoutingError("Human Input blocks collaboration changes")
            if (
                live.get("workflowRef") != workflow["entity_id"]
                or live.get("workflowVersion") != routing["workflowVersion"]
                or live.get("currentAssignmentRef") != current["assignmentRef"]
                or live.get("responsibilityHolderRef") != current["employeeRef"]
            ):
                raise ResponsibilityRoutingError("Holder changed before collaboration completed")
            collaborations = dict(live.get("collaborations") or {})
            record = dict(collaborations.get(interaction_key) or {})
            if record.get("kind") != kind:
                raise ResponsibilityRoutingError(f"{kind} interaction does not exist")
            if record.get("status") != "WAITING":
                if record.get("status") == status:
                    return latest, record
                raise ResponsibilityRoutingError("collaboration already completed with another outcome")
            result_values = _unique(result_refs, limit=16)
            artifact_values = _unique(artifact_refs, limit=16)
            evidence_values = _unique(evidence_refs, limit=16)
            if not response.strip() and not (result_values or artifact_values or evidence_values):
                raise ResponsibilityRoutingError("collaboration completion requires a response or reference")
            at = _now()
            record.update({
                "status": status,
                "response": response.strip()[:2000],
                "resultRefs": result_values,
                "artifactRefs": artifact_values,
                "evidenceRefs": evidence_values,
                "updatedAt": at,
            })
            collaborations[interaction_key] = record
            live["collaborations"] = collaborations
            live["resultRefs"] = _unique([*live.get("resultRefs", []), *result_values])
            live["artifactRefs"] = _unique([*live.get("artifactRefs", []), *artifact_values])
            live["evidenceRefs"] = _unique([*live.get("evidenceRefs", []), *evidence_values])
            live["lastAction"] = f"{kind}_{status}"
            live["updatedAt"] = at
            data = self._work_data(
                latest, live, current,
                activity=("咨询结果已返回原负责人。" if kind == "CONSULT" else "审核结果已返回原负责人。"),
            )
            changed = conn.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? and data_json=?",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, work_ref, row["data_json"]),
            )
            if changed.rowcount != 1:
                raise ResponsibilityRoutingError("Work changed before collaboration completion")
        return self.foundation.get(work_ref), record

    def consult(
        self,
        work_ref: str,
        *,
        consultant_responsibility: str,
        question: str,
        interaction_key: str | None = None,
        context_refs: list[str] | None = None,
        bounded_summary: str = "",
        response: str = "",
        result_refs: list[str] | None = None,
        artifact_refs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        work, routing, workflow, current = self._pinned(work_ref)
        consultant = self._workflow_assignment(workflow, consultant_responsibility)
        if consultant["assignmentRef"] == current["assignmentRef"]:
            raise ResponsibilityRoutingError("Consult requires a distinct responsibility Assignment")
        key = interaction_key or f"consult-{uuid4()}"
        at = _now()
        context = self._collaboration_context(
            work_ref=work_ref, holder_assignment_ref=current["assignmentRef"],
            target_assignment_ref=consultant["assignmentRef"], question=question,
            refs=context_refs, summary=bounded_summary,
        )
        record = {
            "interactionKey": key,
            "interactionRef": f"consult:{key}",
            "kind": "CONSULT",
            "status": "WAITING",
            "workflowRef": workflow["entity_id"],
            "workflowVersion": routing["workflowVersion"],
            "holderAssignmentRef": current["assignmentRef"],
            "holderEmployeeRef": current["employeeRef"],
            "targetAssignmentRef": consultant["assignmentRef"],
            "targetEmployeeRef": consultant["employeeRef"],
            "question": context["question"],
            "context": context,
            "createdAt": at,
            "updatedAt": at,
        }
        stored = self._create_collaboration(work, routing, current, record)
        if response.strip() or result_refs or artifact_refs or evidence_refs:
            completed_work, stored = self._complete_collaboration(
                work_ref, interaction_key=key, kind="CONSULT", status="COMPLETED",
                response=response, result_refs=result_refs, artifact_refs=artifact_refs, evidence_refs=evidence_refs,
            )
        else:
            completed_work = self.foundation.get(work_ref)
        return {"action": "CONSULT", "work": completed_work, "consult": stored, "handoff": None}

    def complete_consult(
        self,
        work_ref: str,
        *,
        interaction_key: str,
        response: str,
        result_refs: list[str] | None = None,
        artifact_refs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        work, record = self._complete_collaboration(
            work_ref, interaction_key=interaction_key, kind="CONSULT", status="COMPLETED",
            response=response, result_refs=result_refs, artifact_refs=artifact_refs, evidence_refs=evidence_refs,
        )
        return {"action": "CONSULT_COMPLETED", "work": work, "consult": record, "handoff": None}

    def request_review(
        self,
        work_ref: str,
        *,
        reviewer_responsibility: str,
        question: str,
        interaction_key: str | None = None,
        context_refs: list[str] | None = None,
        bounded_summary: str = "",
    ) -> dict[str, Any]:
        work, routing, workflow, current = self._pinned(work_ref)
        reviewer = self._workflow_assignment(workflow, reviewer_responsibility)
        if reviewer["assignmentRef"] == current["assignmentRef"]:
            raise ResponsibilityRoutingError("Review requires a distinct Reviewer Assignment")
        key = interaction_key or f"review-{uuid4()}"
        at = _now()
        context = self._collaboration_context(
            work_ref=work_ref, holder_assignment_ref=current["assignmentRef"],
            target_assignment_ref=reviewer["assignmentRef"], question=question,
            refs=context_refs, summary=bounded_summary,
        )
        record = {
            "interactionKey": key,
            "interactionRef": f"review:{key}",
            "kind": "REVIEW",
            "status": "WAITING",
            "workflowRef": workflow["entity_id"],
            "workflowVersion": routing["workflowVersion"],
            "holderAssignmentRef": current["assignmentRef"],
            "holderEmployeeRef": current["employeeRef"],
            "targetAssignmentRef": reviewer["assignmentRef"],
            "targetEmployeeRef": reviewer["employeeRef"],
            "question": context["question"],
            "context": context,
            "createdAt": at,
            "updatedAt": at,
        }
        stored = self._create_collaboration(work, routing, current, record)
        return {"action": "REVIEW", "work": self.foundation.get(work_ref), "review": stored, "handoff": None}

    def resolve_review(
        self,
        work_ref: str,
        *,
        interaction_key: str,
        outcome: str,
        response: str,
        result_refs: list[str] | None = None,
        artifact_refs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        revision_responsibility: str | None = None,
        continue_default: bool = False,
    ) -> dict[str, Any]:
        decision = outcome.upper()
        if decision not in {"APPROVE", "REQUEST_REVISION"}:
            raise ResponsibilityRoutingError("Review outcome must be APPROVE or REQUEST_REVISION")
        work, record = self._complete_collaboration(
            work_ref, interaction_key=interaction_key, kind="REVIEW", status=decision,
            response=response, result_refs=result_refs, artifact_refs=artifact_refs, evidence_refs=evidence_refs,
        )
        routed = None
        if record["status"] == decision and record.get("routeApplied"):
            return {"action": f"REVIEW_{decision}", "work": work, "review": record, "routing": None}
        if decision == "APPROVE" and continue_default:
            routed = self.route(work_ref, signal="COMPLETED", result_refs=result_refs)
        elif decision == "REQUEST_REVISION" and revision_responsibility:
            routing = work["data"]["responsibilityRouting"]
            workflow = self._entity(routing["workflowRef"], entity_type="RESPONSIBILITY_WORKFLOW")
            target = self._workflow_assignment(workflow, revision_responsibility)
            if target["assignmentRef"] != routing["currentAssignmentRef"]:
                routed = self.route(
                    work_ref, signal="RETURN_OR_REVISION", responsibility_key=revision_responsibility,
                    result_refs=result_refs, artifact_refs=artifact_refs, evidence_refs=evidence_refs,
                    problem=response,
                )
        if routed:
            latest = routed["work"]
            latest_routing = dict(latest["data"]["responsibilityRouting"])
            collaborations = dict(latest_routing.get("collaborations") or {})
            record = dict(collaborations[interaction_key])
            record["routeApplied"] = routed["action"]
            collaborations[interaction_key] = record
            latest_routing["collaborations"] = collaborations
            current_workflow = self._entity(latest_routing["workflowRef"], entity_type="RESPONSIBILITY_WORKFLOW")
            current = next(
                item for item in current_workflow["data"]["assignments"]
                if item["assignmentRef"] == latest_routing["currentAssignmentRef"]
            )
            latest_routing["updatedAt"] = _now()
            self._write_work(latest, latest_routing, current, activity="审核结果已应用。")
            work = self.foundation.get(work_ref)
        return {"action": f"REVIEW_{decision}", "work": work, "review": record, "routing": routed}

    def _handoff(
        self,
        work: dict,
        routing: dict,
        workflow: dict,
        target: dict,
        *,
        reason: str,
        context_refs: list[str],
        push_return: bool,
    ) -> dict:
        current = next(
            item for item in workflow["data"]["assignments"]
            if item["assignmentRef"] == routing["currentAssignmentRef"]
        )
        if target["assignmentRef"] == current["assignmentRef"]:
            return {"action": "CONTINUE_CURRENT", "work": work, "handoff": None}
        at = _now()
        handoff_id = f"handoff-{uuid4()}"
        context_package = _unique(context_refs)
        if not context_package or work["entity_id"] not in context_package:
            raise ResponsibilityRoutingError("Handoff requires a valid reference-first Context Package")
        handoff_data = {
            "kind": "RESPONSIBILITY_ROUTING",
            "workRef": work["entity_id"],
            "workflowRef": workflow["entity_id"],
            "fromAssignmentRef": current["assignmentRef"],
            "fromEmployeeRef": current["employeeRef"],
            "toAssignmentRef": target["assignmentRef"],
            "toEmployeeRef": target["employeeRef"],
            "toRoleSlotRef": target["roleRef"],
            "responsibilitySummary": target["responsibility"],
            "reason": reason[:2000],
            "contextRefs": context_package,
            "acknowledgement": {
                "mode": "RUNTIME_ATOMIC_ACCEPTANCE",
                "manualConfirmationRequired": False,
                "validated": ["target_assignment", "target_employee", "scope", "work", "workflow_version", "context_package"],
            },
            "createdAt": at,
            "acknowledgedAt": at,
        }
        stack = list(routing.get("returnStack") or [])
        if push_return:
            stack.append(current["assignmentRef"])
        routing.update({
            "currentAssignmentRef": target["assignmentRef"],
            "responsibilityHolderRef": target["employeeRef"],
            "currentExecutorRef": None,
            "returnStack": stack,
            "status": "ACTIVE",
            "handoffRefs": _unique([*routing.get("handoffRefs", []), handoff_id]),
            "lastAction": "HANDOFF",
            "updatedAt": at,
        })
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            row = conn.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, work["entity_id"]),
            ).fetchone()
            if row is None:
                raise KeyError(work["entity_id"])
            latest = dict(row)
            latest["data"] = json.loads(latest.pop("data_json"))
            live_routing = latest["data"].get("responsibilityRouting") or {}
            if (live_routing.get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
                raise ResponsibilityRoutingError("Human Input blocks responsibility handoff")
            if (
                live_routing.get("workflowRef") != workflow["entity_id"]
                or live_routing.get("workflowVersion") != routing["workflowVersion"]
                or live_routing.get("scopeType") != routing["scopeType"]
                or live_routing.get("scopeRef") != routing["scopeRef"]
                or live_routing.get("currentAssignmentRef") != current["assignmentRef"]
                or live_routing.get("responsibilityHolderRef") != current["employeeRef"]
            ):
                raise ResponsibilityRoutingError("Responsibility changed concurrently; retry from current truth")
            assignment_row = conn.execute(
                "select company_id, workspace_id, lifecycle_status, data_json from runtime_entities "
                "where tenant_id=? and entity_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT'",
                (self.tenant_id, target["assignmentRef"]),
            ).fetchone()
            employee_row = conn.execute(
                "select company_id, workspace_id, lifecycle_status from runtime_entities "
                "where tenant_id=? and entity_id=? and entity_type='AI_EMPLOYEE'",
                (self.tenant_id, target["employeeRef"]),
            ).fetchone()
            assignment_data = json.loads(assignment_row["data_json"]) if assignment_row else {}
            if (
                assignment_row is None
                or assignment_row["company_id"] != work["company_id"]
                or assignment_data.get("scopeType") != routing["scopeType"]
                or assignment_data.get("scopeRef") != routing["scopeRef"]
                or employee_row is None
                or employee_row["company_id"] != work["company_id"]
                or employee_row["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
                or (work["workspace_id"] and employee_row["workspace_id"] not in (None, work["workspace_id"]))
            ):
                raise ResponsibilityRoutingError("Handoff target failed atomic acceptance validation")
            conn.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, parent_id, "
                "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, 'HANDOFF', ?, ?, ?, ?, 'CREATED', 'UNVERIFIED', 'MISSING', ?, ?, ?)",
                (handoff_id, self.tenant_id, work["company_id"], work["workspace_id"], work["entity_id"],
                 target["employeeRef"], json.dumps(handoff_data, ensure_ascii=False), at, at),
            )
            conn.execute(
                "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
                "values (?, ?, ?, ?, ?, 'HAS_HANDOFF', ?, ?)",
                (f"link-{uuid4()}", self.tenant_id, work["company_id"], work["workspace_id"], work["entity_id"], handoff_id, at),
            )
            machine = get_registered_machine("handoff")
            source = "CREATED"
            for target_state, actor, trigger in (
                ("SENT", "SYSTEM", "send"),
                ("ACKNOWLEDGED", "AI_EMPLOYEE", "acknowledge"),
                ("COMPLETED", "AI_EMPLOYEE", "complete"),
            ):
                record = machine.transition(
                    handoff_id, source, target_state, actor=actor, trigger=trigger,
                    reason=reason, context={"workRef": work["entity_id"]}, record=False,
                )
                conn.execute(
                    "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, trigger, actor, "
                    "at, reason, company_id, workspace_id, context_json) values (?, 'handoff', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (self.tenant_id, handoff_id, record.source, record.target, record.trigger, record.actor,
                     record.at, reason, work["company_id"], work["workspace_id"], json.dumps(record.context)),
                )
                source = target_state
            conn.execute(
                "update runtime_entities set lifecycle_status='COMPLETED', data_json=?, updated_at=? "
                "where tenant_id=? and entity_id=? and lifecycle_status='CREATED'",
                (json.dumps(handoff_data, ensure_ascii=False), at, self.tenant_id, handoff_id),
            )
            data = self._work_data(latest, routing, target, activity=f"已交给{target['responsibility']}负责人。")
            changed = conn.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? and data_json=?",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, work["entity_id"], row["data_json"]),
            )
            if changed.rowcount != 1:
                raise ResponsibilityRoutingError("Work changed before handoff completion")
        return {
            "action": "HANDOFF",
            "work": self.foundation.get(work["entity_id"]),
            "handoff": self.foundation.get(handoff_id),
        }

    def route(
        self,
        work_ref: str,
        *,
        signal: str,
        responsibility_key: str | None = None,
        result_refs: list[str] | None = None,
        artifact_refs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        problem: str = "",
        interaction_key: str | None = None,
        bounded_summary: str = "",
    ) -> dict[str, Any]:
        action = ACTION_ALIASES.get(signal.upper(), signal.upper())
        if action not in SIGNALS:
            raise ResponsibilityRoutingError("unsupported deterministic routing signal")
        work, routing, workflow, current = self._pinned(work_ref)
        human_input = routing.get("humanInput") or {}
        if human_input and human_input.get("state") not in {"CLOSED", "INVALIDATED"}:
            raise ResponsibilityRoutingError("Human Input must be reviewed on its original Work")
        if routing.get("status") == "WAITING_DECISION" and action != "DECISION_GATE":
            raise ResponsibilityRoutingError("Work is waiting for the existing CEO Decision")
        if action == "CONSULT":
            if not responsibility_key:
                raise ResponsibilityRoutingError("Consult requires a consultant responsibility")
            return self.consult(
                work_ref, consultant_responsibility=responsibility_key, question=problem,
                interaction_key=interaction_key, context_refs=[work_ref, *(artifact_refs or []), *(evidence_refs or [])],
                bounded_summary=bounded_summary, result_refs=result_refs,
            )
        if action == "REVIEW":
            if not responsibility_key:
                raise ResponsibilityRoutingError("Review requires a reviewer responsibility")
            return self.request_review(
                work_ref, reviewer_responsibility=responsibility_key, question=problem,
                interaction_key=interaction_key, context_refs=[work_ref, *(artifact_refs or []), *(evidence_refs or [])],
                bounded_summary=bounded_summary,
            )
        routing["resultRefs"] = _unique([*routing.get("resultRefs", []), *(result_refs or [])])
        routing["artifactRefs"] = _unique([*routing.get("artifactRefs", []), *(artifact_refs or [])])
        routing["evidenceRefs"] = _unique([*routing.get("evidenceRefs", []), *(evidence_refs or [])])
        refs = [*routing["resultRefs"], *routing["artifactRefs"], *routing["evidenceRefs"]]
        if action == "CONTINUE":
            routing.update({"status": "ACTIVE", "lastAction": "STAY_AND_CONTINUE", "updatedAt": _now()})
            self._write_work(work, routing, current, activity="当前负责人继续处理。")
            return {"action": "STAY_AND_CONTINUE", "work": self.foundation.get(work_ref), "handoff": None}
        if action == "WAIT":
            routing.update({"status": "WAITING", "lastAction": "WAIT", "updatedAt": _now()})
            self._write_work(work, routing, current, activity="当前责任等待输入或恢复条件。")
            return {"action": "WAIT", "work": self.foundation.get(work_ref), "handoff": None}
        if action == "DECISION_GATE":
            existing_ref = routing.get("decisionPacketRef")
            if existing_ref:
                decision = self._entity(existing_ref, entity_type="DECISION_PACKET")
                if decision["lifecycle_status"] == "WAITING_CEO":
                    return {"action": "DECISION_GATE", "work": work, "decision": decision}
            decision = self.foundation.create(
                "DECISION_PACKET", company_id=work["company_id"], workspace_id=work["workspace_id"],
                parent_id=work_ref, owner_ref="CEO",
                data={"workRef": work_ref, "assignmentRef": current["assignmentRef"], "problem": problem[:2000], "contextRefs": _unique(refs)},
            )
            decision = self.foundation.transition(decision["entity_id"], "READY", actor="SYSTEM", trigger="prepare")
            decision = self.foundation.transition(decision["entity_id"], "WAITING_CEO", actor="SYSTEM", trigger="request_decision")
            self.foundation.link(work_ref, "HAS_DECISION", decision["entity_id"])
            routing.update({"decisionPacketRef": decision["entity_id"], "status": "WAITING_DECISION", "lastAction": "DECISION_GATE", "updatedAt": _now()})
            self._write_work(work, routing, current, activity="等待 CEO 决定；当前责任未转移。")
            return {"action": "DECISION_GATE", "work": self.foundation.get(work_ref), "decision": decision}
        if action == "TERMINAL":
            if current["outputContract"].get("requiresResult") and not _unique(result_refs):
                raise ResponsibilityRoutingError("current responsibility requires a Result reference")
            routing.update({"status": "COMPLETED", "currentExecutorRef": None, "lastAction": "COMPLETE", "updatedAt": _now()})
            self._write_work(work, routing, current, activity="工作已完成，结果已回收到同一工作对象。")
            return {"action": "COMPLETE", "work": self.foundation.get(work_ref), "handoff": None}

        target: dict | None = None
        push_return = action in {"NEED_RESPONSIBILITY", "NEED_LEADER"}
        if action == "COMPLETED":
            if current["outputContract"].get("requiresResult") and not _unique(result_refs):
                raise ResponsibilityRoutingError("current responsibility requires a Result reference")
            next_key = workflow["data"]["defaultNext"].get(current["responsibilityKey"])
            if next_key is None:
                routing.update({"status": "COMPLETED", "currentExecutorRef": None, "lastAction": "COMPLETE", "updatedAt": _now()})
                self._write_work(work, routing, current, activity="默认流程已结束，结果已回收。")
                return {"action": "COMPLETE", "work": self.foundation.get(work_ref), "handoff": None}
            target = self._workflow_assignment(workflow, next_key)
            push_return = False
        elif action == "RETURN":
            if responsibility_key:
                target = self._workflow_assignment(workflow, responsibility_key)
            else:
                stack = list(routing.get("returnStack") or [])
                if not stack:
                    raise ResponsibilityRoutingError("return target is missing")
                target_ref = stack.pop()
                routing["returnStack"] = stack
                target = next(item for item in workflow["data"]["assignments"] if item["assignmentRef"] == target_ref)
            push_return = False
        elif action == "NEED_RESPONSIBILITY":
            if not responsibility_key:
                raise ResponsibilityRoutingError("explicit responsibility need requires a target")
            target = self._workflow_assignment(workflow, responsibility_key)
        elif action == "HANDOFF":
            if not responsibility_key:
                raise ResponsibilityRoutingError("Handoff requires a target responsibility")
            target = self._workflow_assignment(workflow, responsibility_key)
            push_return = False
        elif action == "NEED_LEADER":
            leaders = [item for item in workflow["data"]["assignments"] if item["isLeader"]]
            if len(leaders) != 1:
                raise ResponsibilityRoutingError("current scope has no Operating Leader Assignment")
            target = leaders[0]
        return self._handoff(
            work, routing, workflow, target, reason=problem or action,
            context_refs=[work_ref, *refs], push_return=push_return,
        )

    def apply_decision(self, work_ref: str, *, choice: str, reason: str) -> dict[str, Any]:
        work = self._entity(work_ref)
        routing = dict(work["data"].get("responsibilityRouting") or {})
        if (routing.get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
            raise ResponsibilityRoutingError("Human Input blocks Decision application")
        if routing.get("status") != "WAITING_DECISION" or not routing.get("decisionPacketRef"):
            raise ResponsibilityRoutingError("Work is not waiting for a Decision")
        decision = self._entity(routing["decisionPacketRef"], entity_type="DECISION_PACKET")
        decision = self.foundation.transition(
            decision["entity_id"], "DECIDED", actor="CEO", trigger="decide", reason=reason,
            context={"choice": choice},
        )
        decision = self.foundation.transition(
            decision["entity_id"], "APPLIED", actor="SYSTEM", trigger="apply", reason=reason,
            context={"choice": choice},
        )
        decision_data = decision["data"] | {
            "choice": choice,
            "choiceReason": reason[:2000],
            "decidedAt": _now(),
            "appliedAt": _now(),
        }
        with self.db.connect() as conn:
            conn.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? "
                "and entity_type='DECISION_PACKET' and lifecycle_status='APPLIED'",
                (json.dumps(decision_data, ensure_ascii=False), _now(), self.tenant_id, decision["entity_id"]),
            )
        decision = self.foundation.get(decision["entity_id"])
        workflow = self._entity(routing["workflowRef"], entity_type="RESPONSIBILITY_WORKFLOW")
        current = next(item for item in workflow["data"]["assignments"] if item["assignmentRef"] == routing["currentAssignmentRef"])
        routing.update({"status": "ACTIVE", "lastAction": "DECISION_APPLIED", "decisionChoice": choice, "updatedAt": _now()})
        self._write_work(work, routing, current, activity="CEO 决定已应用，原责任自动恢复。")
        return {"action": "DECISION_APPLIED", "work": self.foundation.get(work_ref), "decision": decision}
