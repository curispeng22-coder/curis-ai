"""Canonical child Work identity and sequential release on existing Runtime rows."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from ..database import Database
from ..resource_scope_policy import ResourceScopePolicy
from ..tenant_context import TenantContext
from .registry import get_registered_machine


WORK_STATES = frozenset({
    "PLANNED", "READY", "ACTIVE", "WAITING", "BLOCKED", "PAUSED", "COMPLETED", "FAILED", "CANCELLED", "ARCHIVED",
})
WORK_TRANSITIONS = {
    "PLANNED": frozenset({"READY", "PAUSED", "CANCELLED", "ARCHIVED"}),
    "READY": frozenset({"ACTIVE", "PAUSED", "CANCELLED", "ARCHIVED"}),
    "ACTIVE": frozenset({"WAITING", "BLOCKED", "PAUSED", "COMPLETED", "FAILED", "CANCELLED", "ARCHIVED"}),
    "WAITING": frozenset({"ACTIVE", "PAUSED", "FAILED", "CANCELLED", "ARCHIVED"}),
    "BLOCKED": frozenset({"ACTIVE", "PAUSED", "FAILED", "CANCELLED", "ARCHIVED"}),
    "PAUSED": frozenset({"PLANNED", "READY", "ACTIVE", "WAITING", "BLOCKED", "FAILED", "CANCELLED", "ARCHIVED"}),
    "COMPLETED": frozenset({"ARCHIVED"}),
    "FAILED": frozenset({"ARCHIVED"}),
    "CANCELLED": frozenset({"ARCHIVED"}),
    "ARCHIVED": frozenset({"PLANNED", "READY", "ACTIVE", "WAITING", "BLOCKED", "PAUSED", "COMPLETED", "FAILED", "CANCELLED"}),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _stable_id(prefix: str, *parts: object) -> str:
    digest = hashlib.sha256(_json([str(part) for part in parts]).encode()).hexdigest()[:32]
    return f"{prefix}-{digest}"


def _unique(values: list[str] | None) -> list[str]:
    return list(dict.fromkeys(str(value) for value in values or [] if str(value).strip()))


class ChildWorkError(ValueError):
    pass


def leader_preferred_binding(database, work, assignment, employee_ref):
    from ..employee_templates import EmployeeTemplateContract
    from .foundation import RuntimeFoundation, RuntimeScopeError
    service = EmployeeTemplateContract(database)
    preferred = service.preferred_capability_for_employee(employee_ref)
    contract = work["data"].get("followupContract") or {}
    same_assignment = assignment["assignmentRef"] == work["data"].get("responsibilityAssignmentRef")
    if same_assignment:
        if not contract and work["data"].get("cycleRef"):
            contract = RuntimeFoundation(database).get(work["data"]["cycleRef"])["data"].get("contract") or {}
        selected_agent = contract.get("agentBinding") or {}
        if selected_agent:
            matches = [b for b in service.list_employee_capability_bindings(employee_ref)["bindings"]
                if b["id"] == selected_agent.get("bindingRef") and b["enabled"]
                and b["capability_source"] == "tenant_private" and b["capability_type"] == "agent"
                and b["capability_id"] == selected_agent.get("capabilityRef") and employee_ref == selected_agent.get("employeeRef")]
            if len(matches) != 1:
                raise RuntimeScopeError("Original selected Agent binding changed")
            preferred = matches[0]
    if not preferred or preferred["capability_type"] not in {"agent", "model"}:
        raise RuntimeScopeError("Leader target has no eligible explicit employee preference")
    allowed = assignment.get("capabilityBindingRefs") or []
    if allowed:
        capabilities = []
        for ref in allowed:
            binding = RuntimeFoundation(database).get(ref)
            if (binding["entity_type"] != "CAPABILITY_BINDING" or binding["company_id"] != work["company_id"]
                    or binding["workspace_id"] not in (None, work["workspace_id"])
                    or binding["lifecycle_status"] != "ACTIVE"):
                raise RuntimeScopeError("Assignment capability binding is unavailable")
            capabilities.append(binding["capability_ref"])
        if preferred["capability_id"] not in capabilities:
            raise RuntimeScopeError("Employee preference is outside Assignment capability references")
    pin = contract.get("capabilityBindingRef") if same_assignment else None
    if pin and preferred["id"] != pin:
        raise RuntimeScopeError("Delegated employee preference changed")
    return preferred


class CanonicalChildWorkRuntime:
    """Small shared Work seam; no scheduler, Surface or domain semantics."""

    def __init__(self, database: Database):
        self.db = database

    def release_leader_plan(self, work_ref: str, task_ref: str, items: list[dict]) -> list[str]:
        """Atomically release a bounded plan against the original pinned workflow."""
        from .responsibility_routing import ResponsibilityRoutingRuntime
        routing = ResponsibilityRoutingRuntime(self.db)
        with self.db.connect() as con:
            con.execute("BEGIN IMMEDIATE")
            root = self._entity(self._row(con, work_ref, "WORK"))
            cycle = self._cycle(con, root["parent_id"])
            route = root["data"].get("responsibilityRouting") or {}
            workflow = self._entity(self._row(con, route.get("workflowRef"), "RESPONSIBILITY_WORKFLOW"))
            if (root["data"].get("kind") != "CANONICAL_CHILD_WORK" or cycle["data"].get("kind") != "GENERAL_WORK_CYCLE"
                    or cycle["lifecycle_status"] not in {"PLANNED", "READY", "RUNNING"}):
                raise ChildWorkError("Leader delegation requires its active canonical business Cycle")
            ResourceScopePolicy.require_same_execution_scope(self._scope(con, root), self._scope(con, cycle))
            ResourceScopePolicy.require_same_execution_scope(self._scope(con, root), self._scope(con, workflow))
            assignments = {a["assignmentRef"]: a for a in workflow["data"]["assignments"]}
            leader = assignments.get(route.get("currentAssignmentRef")) or {}
            if (not leader.get("isLeader") or root["lifecycle_status"] != "ACTIVE"
                    or route.get("status") != "ACTIVE" or route.get("currentExecutorRef")
                    or workflow["data"]["version"] != route.get("workflowVersion")):
                raise ChildWorkError("Leader route is no longer active")
            current_leader = self._entity(self._row(con, leader["assignmentRef"], "RESPONSIBILITY_ASSIGNMENT"))
            if routing._assignment_snapshot(current_leader) != leader:
                raise ChildWorkError("Original Leader Assignment changed")
            accepted = [r for r in (route.get("executions") or {}).values()
                        if str(r.get("executionKey", "")).startswith("leader:plan:")
                        and r.get("taskRef") == task_ref and r.get("status") == "ACCEPTED"
                        and r.get("provenance", {}).get("verification_status") == "VERIFIED"]
            task = con.execute("select output from tasks where tenant_id=? and company_id=? and workspace_id is ? "
                "and work_ref=? and task_id=? and status='COMPLETED'",
                (self.tenant_id, root["company_id"], root["workspace_id"], work_ref, task_ref)).fetchone()
            plan = [{k: i[k] for k in ("assignmentRef", "problem", "expectedResult")} for i in items]
            if len(accepted) != 1 or task is None or json.loads(task["output"]).get("delegations") != plan:
                raise ChildWorkError("Leader plan lacks its original verified Result")
            if not 1 <= len(items) <= 6 or len({i["assignmentRef"] for i in items}) != len(items):
                raise ChildWorkError("Leader plan must contain one to six unique responsibilities")
            existing = root["data"].get("leaderDelegation")
            identity = {"planTaskRef": task_ref, "plan": plan, "maxCalls": 8}
            if existing:
                if any(existing.get(k) != v for k, v in identity.items()):
                    raise ChildWorkError("Original Leader plan cannot be replaced")
                return list(existing["childWorkRefs"])
            children = []
            for item in items:
                snapshot = assignments.get(item["assignmentRef"])
                if not snapshot or snapshot.get("isLeader"):
                    raise ChildWorkError("Leader may delegate only to existing non-Leader responsibilities")
                current = self._entity(self._row(con, snapshot["assignmentRef"], "RESPONSIBILITY_ASSIGNMENT"))
                if routing._assignment_snapshot(current) != snapshot:
                    raise ChildWorkError("Pinned Assignment changed")
                child = self._create_work_locked(con, cycle=cycle, assignment_ref=snapshot["assignmentRef"],
                    release_key=f"leader:{work_ref}:{task_ref}:{snapshot['assignmentRef']}", required=True,
                    input_refs=[work_ref, f"task:{task_ref}"], predecessor_work_ref=None, at=_now())
                self._activate_leader_child_locked(con, child, root, snapshot, item["contract"])
                children.append(child["entity_id"])
            root["data"]["leaderDelegation"] = dict(identity, childWorkRefs=children)
            con.execute("update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(root["data"]), _now(), self.tenant_id, work_ref))
            return children

    def _activate_leader_child_locked(self, con, child, root, assignment, contract):
        from .responsibility_routing import ResponsibilityRoutingRuntime
        child_route = dict(root["data"]["responsibilityRouting"], currentAssignmentRef=assignment["assignmentRef"],
            responsibilityHolderRef=assignment["employeeRef"], currentExecutorRef=None,
            returnStack=[], handoffRefs=[], resultRefs=[], artifactRefs=[], evidenceRefs=[], executions={},
            executionCount=0, status="ACTIVE", lastAction="LEADER_DELEGATED")
        data = ResponsibilityRoutingRuntime._work_data(child, child_route, assignment, activity="Leader 已派发当前业务任务。")
        data.update(leaderRootWorkRef=root["entity_id"], followupContract=contract)
        con.execute("update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
            (_json(data), _now(), self.tenant_id, child["entity_id"]))
        current = self._entity(self._row(con, child["entity_id"], "WORK"))
        current = self._transition_locked(con, current, "READY", actor="SYSTEM", reason="原责任与 Leader 计划已核验")
        self._transition_locked(con, current, "ACTIVE", actor="SYSTEM", reason="Leader 已派发")

    def release_leader_summary(self, work_ref: str) -> str:
        with self.db.connect() as con:
            con.execute("BEGIN IMMEDIATE")
            root = self._entity(self._row(con, work_ref, "WORK"))
            route = root["data"]["responsibilityRouting"]
            state = root["data"].get("leaderDelegation") or {}
            if root["lifecycle_status"] != "ACTIVE" or route.get("status") != "ACTIVE" or not state.get("childWorkRefs"):
                raise ChildWorkError("Original Leader Work cannot release summary")
            workflow = self._entity(self._row(con, route["workflowRef"], "RESPONSIBILITY_WORKFLOW"))
            leader = next(a for a in workflow["data"]["assignments"] if a["assignmentRef"] == route["currentAssignmentRef"])
            if not leader.get("isLeader") or workflow["data"]["version"] != route["workflowVersion"]:
                raise ChildWorkError("Original Leader workflow changed")
            inputs = [work_ref]
            for ref in state["childWorkRefs"]:
                child = self._entity(self._row(con, ref, "WORK"))
                ResourceScopePolicy.require_same_execution_scope(self._scope(con, root), self._scope(con, child))
                if (child["data"].get("leaderRootWorkRef") != work_ref or child["parent_id"] != root["parent_id"]
                        or child["lifecycle_status"] not in {"ACTIVE", "COMPLETED"}):
                    raise ChildWorkError("Leader child lineage or lifecycle changed")
                records = [r for r in child["data"]["responsibilityRouting"].get("executions", {}).values()
                    if str(r.get("executionKey", "")).startswith("leader:worker:")]
                if len(records) != 1 or records[0].get("status") != "ACCEPTED" or records[0].get("provenance", {}).get("verification_status") != "VERIFIED":
                    raise ChildWorkError("Leader child Result is not verified")
                inputs.append(f"task:{records[0]['taskRef']}")
            if state.get("summaryWorkRef"):
                return state["summaryWorkRef"]
            cycle = self._cycle(con, root["parent_id"])
            contract = dict(root["data"].get("followupContract") or cycle["data"].get("contract") or {})
            plan_record = next(r for r in route["executions"].values() if r.get("taskRef") == state["planTaskRef"])
            contract["capabilityBindingRef"] = plan_record["provenance"]["provider_capability"]["binding_ref"]
            contract["problem"] = "汇总原业务工作及已验证子 Work 结果；成果仍待既有验收。"
            child = self._create_work_locked(con, cycle=cycle, assignment_ref=leader["assignmentRef"],
                release_key=f"leader-summary:{work_ref}", required=True, input_refs=inputs,
                predecessor_work_ref=None, at=_now())
            self._activate_leader_child_locked(con, child, root, leader, contract)
            state["summaryWorkRef"] = child["entity_id"]
            con.execute("update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(root["data"]), _now(), self.tenant_id, work_ref))
            return child["entity_id"]

    def attach_leader_summary(self, work_ref: str) -> None:
        with self.db.connect() as con:
            con.execute("BEGIN IMMEDIATE")
            root = self._entity(self._row(con, work_ref, "WORK"))
            route = root["data"]["responsibilityRouting"]
            state = root["data"]["leaderDelegation"]
            summary = self._entity(self._row(con, state["summaryWorkRef"], "WORK"))
            ResourceScopePolicy.require_same_execution_scope(self._scope(con, root), self._scope(con, summary))
            if summary["data"].get("leaderRootWorkRef") != work_ref or summary["parent_id"] != root["parent_id"]:
                raise ChildWorkError("Leader summary lineage changed")
            records = [r for r in summary["data"]["responsibilityRouting"].get("executions", {}).values()
                if str(r.get("executionKey", "")).startswith("leader:summary:")]
            if (root["lifecycle_status"] != "ACTIVE" or route.get("status") != "ACTIVE"
                    or len(records) != 1 or records[0].get("status") != "ACCEPTED"
                    or records[0].get("provenance", {}).get("verification_status") != "VERIFIED"):
                raise ChildWorkError("Leader summary is unverified or original Work stopped")
            record = records[0]
            for key, values in (("resultRefs", [record["resultRef"]]), ("artifactRefs", record.get("artifactRefs", [])),
                                ("evidenceRefs", record.get("evidenceRefs", []))):
                route[key] = _unique([*route.get(key, []), *values])
            con.execute("update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(root["data"]), _now(), self.tenant_id, work_ref))

    def reserve_leader_call(self, task_ref: str) -> bool:
        """Share a hard call ceiling on existing execution records; never refund uncertainty."""
        with self.db.connect() as con:
            con.execute("BEGIN IMMEDIATE")
            task = con.execute("select * from tasks where tenant_id=? and task_id=?", (self.tenant_id, task_ref)).fetchone()
            if task is None or not task["work_ref"]:
                return False
            work = self._entity(self._row(con, task["work_ref"]))
            route = work["data"].get("responsibilityRouting") or {}
            leader_key = str(task["execution_ref"] or "").startswith("leader:")
            if not leader_key and not work["data"].get("leaderRootWorkRef"):
                return False
            root = self._entity(self._row(con, work["data"].get("leaderRootWorkRef") or work["entity_id"], "WORK"))
            self._scope(con, root)
            ResourceScopePolicy.require_same_execution_scope(self._scope(con, root), self._scope(con, work))
            state = root["data"].get("leaderDelegation") or {}
            refs = [root["entity_id"], *state.get("childWorkRefs", []), *([state["summaryWorkRef"]] if state.get("summaryWorkRef") else [])]
            if work["entity_id"] not in refs:
                raise ChildWorkError("Leader child is not in the original plan")
            root_route = root["data"].get("responsibilityRouting") or {}
            workflow = self._entity(self._row(con, root_route.get("workflowRef"), "RESPONSIBILITY_WORKFLOW"))
            leader = next((a for a in workflow["data"]["assignments"] if a["assignmentRef"] == root_route.get("currentAssignmentRef")), {})
            if not leader.get("isLeader"):
                raise ChildWorkError("Original Leader responsibility changed")
            for entity in (root, work):
                r = entity["data"].get("responsibilityRouting") or {}
                if entity["lifecycle_status"] != "ACTIVE" or r.get("status") not in {"ACTIVE", "EXECUTING"}:
                    raise ChildWorkError("Leader work is paused, cancelled or blocked")
            record = (route.get("executions") or {}).get(task["execution_ref"]) or {}
            if task["status"] != "RUNNING" or record.get("taskRef") != task_ref or record.get("status") != "RUNNING" or record.get("providerCallReserved"):
                raise ChildWorkError("Leader call already reserved or execution claim changed")
            from .responsibility_routing import ResponsibilityRoutingRuntime
            pinned = next((a for a in workflow["data"]["assignments"] if a["assignmentRef"] == record["assignmentRef"]), None)
            current_assignment = self._entity(self._row(con, record["assignmentRef"], "RESPONSIBILITY_ASSIGNMENT"))
            if not pinned or ResponsibilityRoutingRuntime._assignment_snapshot(current_assignment) != pinned:
                raise ChildWorkError("Leader Assignment snapshot changed")
            ResourceScopePolicy.authorize_assignment(con, tenant_id=self.tenant_id, company_id=work["company_id"],
                assignment_ref=record["assignmentRef"], employee_ref=record["employeeRef"],
                revision=pinned["assignmentRevision"], scope=self._scope(con, work))
            preferred = leader_preferred_binding(self.db, work, pinned, task["employee_id"])
            if (preferred["capability_source"], preferred["capability_type"], preferred["capability_id"]) != (
                    task["requested_capability_source"], task["requested_capability_type"], task["requested_capability_id"]):
                raise ChildWorkError("Original Leader execution preference changed")
            used = sum(bool(r.get("providerCallReserved")) for ref in refs
                for r in (self._entity(self._row(con, ref, "WORK"))["data"].get("responsibilityRouting", {}).get("executions") or {}).values())
            if used >= 8:
                raise ChildWorkError("Leader shared call budget exhausted")
            record["providerCallReserved"] = True
            con.execute("update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(work["data"]), _now(), self.tenant_id, work["entity_id"]))
            return True

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    @staticmethod
    def _entity(row) -> dict[str, Any]:
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        return item

    def _row(self, connection, entity_id: str, entity_type: str | None = None):
        row = connection.execute(
            "select * from runtime_entities where tenant_id=? and entity_id=?",
            (self.tenant_id, entity_id),
        ).fetchone()
        if row is None:
            raise KeyError(entity_id)
        if entity_type and row["entity_type"] != entity_type:
            raise ChildWorkError(f"{entity_id} is not {entity_type}")
        return row

    def _cycle(self, connection, cycle_id: str) -> dict[str, Any]:
        cycle = self._entity(self._row(connection, cycle_id, "CYCLE"))
        self._scope(connection, cycle)
        return cycle

    def _scope(self, connection, record: dict) -> dict:
        try:
            return ResourceScopePolicy.execution_scope_from_record(
                connection, tenant_id=self.tenant_id, record=record,
            )
        except ValueError as error:
            raise ChildWorkError(str(error)) from error

    def _assignment(self, connection, assignment_ref: str, cycle: dict[str, Any]) -> dict[str, Any]:
        assignment = self._entity(self._row(connection, assignment_ref, "RESPONSIBILITY_ASSIGNMENT"))
        data = assignment["data"]
        try:
            ResourceScopePolicy.require_same_execution_scope(
                self._scope(connection, assignment), self._scope(connection, cycle),
            )
        except ValueError as error:
            raise ChildWorkError("Work Assignment is outside the parent Cycle scope") from error
        if assignment["lifecycle_status"] != "ACTIVE":
            raise ChildWorkError("Work Assignment is not active")
        employee_ref = str(data.get("employeeRef") or "")
        employee = self._entity(self._row(connection, employee_ref, "AI_EMPLOYEE"))
        if (
            employee["company_id"] != cycle["company_id"]
            or employee["workspace_id"] not in (None, cycle["workspace_id"])
            or employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
        ):
            raise ChildWorkError("Work holder Employee is unavailable or outside the Cycle scope")
        return {
            "assignmentRef": assignment_ref,
            "assignmentRevision": int(data.get("revision") or 1),
            "responsibilityKey": str(data.get("responsibilityKey") or ""),
            "responsibility": str(data.get("responsibility") or ""),
            "holderEmployeeRef": employee_ref,
            "roleRef": str(data.get("roleRef") or ""),
        }

    @staticmethod
    def _identity(data: dict[str, Any]) -> dict[str, Any]:
        return {
            key: data.get(key)
            for key in (
                "kind", "version", "cycleRef", "seriesRef", "releaseKey", "required",
                "responsibilityAssignmentRef", "assignmentRevision", "responsibilityKey",
                "holderEmployeeRef", "roleRef", "predecessorWorkRef", "inputRefs",
            )
        }

    def _insert_link(self, connection, source: dict[str, Any], relation: str, target_id: str, at: str) -> None:
        connection.execute(
            "insert or ignore into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
            "values (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                _stable_id("link", self.tenant_id, source["entity_id"], relation, target_id),
                self.tenant_id,
                source["company_id"],
                source["workspace_id"],
                source["entity_id"],
                relation,
                target_id,
                at,
            ),
        )

    def _new_work_data(
        self,
        *,
        cycle: dict[str, Any],
        assignment: dict[str, Any],
        release_key: str,
        required: bool,
        input_refs: list[str],
        predecessor_work_ref: str | None,
    ) -> dict[str, Any]:
        return {
            "kind": "CANONICAL_CHILD_WORK",
            "version": 1,
            **{key: cycle["data"][key] for key in ("scopeType", "scopeRef") if key in cycle["data"]},
            "cycleRef": cycle["entity_id"],
            "seriesRef": (cycle["data"].get("autonomousControl") or {}).get("seriesRef"),
            "releaseKey": release_key,
            "required": bool(required),
            "responsibilityAssignmentRef": assignment["assignmentRef"],
            "assignmentRevision": assignment["assignmentRevision"],
            "responsibilityKey": assignment["responsibilityKey"],
            "responsibility": assignment["responsibility"],
            "holderEmployeeRef": assignment["holderEmployeeRef"],
            "roleRef": assignment["roleRef"],
            "predecessorWorkRef": predecessor_work_ref,
            "inputRefs": _unique(input_refs),
            "resultRefs": [],
            "artifactRefs": [],
            "evidenceRefs": [],
            "acceptanceRefs": [],
        }

    def _create_work_locked(
        self,
        connection,
        *,
        cycle: dict[str, Any],
        assignment_ref: str,
        release_key: str,
        required: bool,
        input_refs: list[str],
        predecessor_work_ref: str | None,
        at: str,
    ) -> dict[str, Any]:
        assignment = self._assignment(connection, assignment_ref, cycle)
        work_id = _stable_id("work", self.tenant_id, cycle["entity_id"], release_key)
        data = self._new_work_data(
            cycle=cycle,
            assignment=assignment,
            release_key=release_key,
            required=required,
            input_refs=input_refs,
            predecessor_work_ref=predecessor_work_ref,
        )
        existing = connection.execute(
            "select * from runtime_entities where tenant_id=? and entity_id=?",
            (self.tenant_id, work_id),
        ).fetchone()
        if existing is not None:
            item = self._entity(existing)
            ResourceScopePolicy.require_same_execution_scope(
                self._scope(connection, item), self._scope(connection, cycle),
            )
            if item["entity_type"] != "WORK" or self._identity(item["data"]) != self._identity(data):
                raise ChildWorkError("deterministic Work identity conflicts with existing truth")
            return item
        connection.execute(
            "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, parent_id, "
            "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
            "values (?, ?, 'WORK', ?, ?, ?, ?, 'PLANNED', 'UNVERIFIED', 'MISSING', ?, ?, ?)",
            (
                work_id,
                self.tenant_id,
                cycle["company_id"],
                cycle["workspace_id"],
                cycle["entity_id"],
                assignment["holderEmployeeRef"],
                _json(data),
                at,
                at,
            ),
        )
        work = self._entity(self._row(connection, work_id, "WORK"))
        self._insert_link(connection, cycle, "HAS_WORK", work_id, at)
        return work

    def create_work(
        self,
        *,
        cycle_id: str,
        assignment_ref: str,
        release_key: str,
        input_refs: list[str] | None = None,
        required: bool = True,
    ) -> dict[str, Any]:
        key = release_key.strip()
        if not key:
            raise ChildWorkError("Work requires a deterministic release key")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            cycle = self._cycle(connection, cycle_id)
            if cycle["lifecycle_status"] not in {"PLANNED", "READY", "RUNNING"}:
                raise ChildWorkError("Parent Cycle cannot accept new Work")
            return self._create_work_locked(
                connection,
                cycle=cycle,
                assignment_ref=assignment_ref,
                release_key=key,
                required=required,
                input_refs=_unique(input_refs),
                predecessor_work_ref=None,
                at=_now(),
            )

    def create_cycle_work(
        self,
        *,
        company_id: str,
        workspace_id: str | None = None,
        scope_type: str | None = None,
        scope_ref: str | None = None,
        assignment_ref: str,
        release_key: str,
        contract: dict[str, Any],
        input_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        """Atomically create one existing Cycle and its first canonical Work."""

        key = release_key.strip()
        if not key:
            raise ChildWorkError("Work requires a deterministic release key")
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            scope = self._scope(connection, {
                "company_id": company_id, "workspace_id": workspace_id,
                "scope_type": scope_type, "scope_ref": scope_ref,
            })
            workspace_id = scope["workspace_id"]
            # Keep all historical Workspace release IDs byte-for-byte compatible.
            identity = (workspace_id,) if workspace_id else (company_id, scope["scope_type"], scope["scope_ref"])
            cycle_id = _stable_id("cycle", self.tenant_id, *identity, key)
            cycle = {
                "entity_id": cycle_id,
                "company_id": company_id,
                "workspace_id": workspace_id,
                "data": {"kind": "GENERAL_WORK_CYCLE", "contract": contract, "releaseKey": key,
                         "scopeType": scope["scope_type"], "scopeRef": scope["scope_ref"]},
            }
            assignment = self._assignment(connection, assignment_ref, cycle)
            existing = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, cycle_id),
            ).fetchone()
            if existing is None:
                connection.execute(
                    "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, "
                    "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                    "values (?, ?, 'CYCLE', ?, ?, ?, 'PLANNED', 'UNVERIFIED', 'MISSING', ?, ?, ?)",
                    (
                        cycle_id, self.tenant_id, company_id, workspace_id,
                        assignment["holderEmployeeRef"], _json(cycle["data"]), at, at,
                    ),
                )
                cycle = self._entity(self._row(connection, cycle_id, "CYCLE"))
            else:
                cycle = self._entity(existing)
                ResourceScopePolicy.require_same_execution_scope(self._scope(connection, cycle), scope)
                if (
                    cycle["entity_type"] != "CYCLE"
                    or cycle["company_id"] != company_id
                    or cycle["workspace_id"] != workspace_id
                    or cycle["data"].get("kind") != "GENERAL_WORK_CYCLE"
                    or cycle["data"].get("contract") != contract
                    or cycle["data"].get("releaseKey") != key
                ):
                    raise ChildWorkError("deterministic Cycle identity conflicts with existing truth")
            work = self._create_work_locked(
                connection,
                cycle=cycle,
                assignment_ref=assignment_ref,
                release_key="initial",
                required=True,
                input_refs=_unique(input_refs),
                predecessor_work_ref=None,
                at=at,
            )
            return {"cycle": cycle, "work": work}

    def get_work(self, work_id: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            return self._entity(self._row(connection, work_id, "WORK"))

    def list_cycle_work(self, cycle_id: str) -> list[dict[str, Any]]:
        with self.db.connect() as connection:
            self._cycle(connection, cycle_id)
            rows = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_type='WORK' and parent_id=? "
                "order by created_at, entity_id",
                (self.tenant_id, cycle_id),
            ).fetchall()
            return [self._entity(row) for row in rows]

    def _transition_locked(self, connection, work: dict[str, Any], target: str, *, actor: str, reason: str) -> dict[str, Any]:
        target = target.upper()
        source = work["lifecycle_status"]
        if target not in WORK_STATES:
            raise ChildWorkError("unsupported Work state")
        if source == target:
            return work
        if target not in WORK_TRANSITIONS[source]:
            raise ChildWorkError(f"illegal Work transition: {source} -> {target}")
        at = _now()
        cursor = connection.execute(
            "update runtime_entities set lifecycle_status=?, updated_at=? where tenant_id=? and entity_id=? "
            "and entity_type='WORK' and lifecycle_status=?",
            (target, at, self.tenant_id, work["entity_id"], source),
        )
        if cursor.rowcount != 1:
            raise ChildWorkError("Work changed concurrently; retry from current truth")
        data = dict(work["data"])
        if target == "PAUSED":
            data["pausedFrom"] = source
            data["pausedAt"] = at
        elif source == "PAUSED":
            data.pop("pausedFrom", None)
        if target == "ARCHIVED":
            data["archivedFrom"] = source
            data["archivedAt"] = at
        if data != work["data"]:
            connection.execute(
                "update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (_json(data), self.tenant_id, work["entity_id"]),
            )
        connection.execute(
            "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, trigger, actor, at, "
            "reason, company_id, workspace_id, context_json) values (?, 'work', ?, ?, ?, 'transition', ?, ?, ?, ?, ?, ?)",
            (
                self.tenant_id,
                work["entity_id"],
                source,
                target,
                actor,
                at,
                reason,
                work["company_id"],
                work["workspace_id"],
                _json({"cycleRef": work["parent_id"]}),
            ),
        )
        return self._entity(self._row(connection, work["entity_id"], "WORK"))

    def transition_work(self, work_id: str, target: str, *, actor: str, reason: str = "") -> dict[str, Any]:
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            work = self._entity(self._row(connection, work_id, "WORK"))
            return self._transition_locked(connection, work, target, actor=actor, reason=reason)

    def control_work(self, work_id: str, action: str, *, actor: str, reason: str = "") -> dict[str, Any]:
        """Apply a bounded lifecycle control to the existing canonical Work row."""
        action = action.upper()
        work = self.get_work(work_id)
        status = work["lifecycle_status"]
        if action == "PAUSE":
            if status == "PAUSED":
                return {"work": work, "duplicate": True}
            if status in {"COMPLETED", "CANCELLED", "ARCHIVED"}:
                raise ChildWorkError("terminal Work cannot be paused")
            return {"work": self.transition_work(work_id, "PAUSED", actor=actor, reason=reason), "duplicate": False}
        if action == "RESUME":
            if status != "PAUSED":
                return {"work": work, "duplicate": True}
            target = str(work["data"].get("pausedFrom") or "ACTIVE").upper()
            if target == "PAUSED" or target not in WORK_STATES:
                target = "ACTIVE"
            return {"work": self.transition_work(work_id, target, actor=actor, reason=reason), "duplicate": False}
        if action == "CANCEL":
            if status == "CANCELLED":
                return {"work": work, "duplicate": True}
            if status in {"COMPLETED", "ARCHIVED"}:
                raise ChildWorkError("completed or archived Work cannot be cancelled")
            return {"work": self.transition_work(work_id, "CANCELLED", actor=actor, reason=reason), "duplicate": False}
        if action == "ARCHIVE":
            if status == "ARCHIVED":
                return {"work": work, "duplicate": True}
            return {"work": self.transition_work(work_id, "ARCHIVED", actor=actor, reason=reason), "duplicate": False}
        if action == "RESTORE":
            if status != "ARCHIVED":
                return {"work": work, "duplicate": True}
            target = str(work["data"].get("archivedFrom") or "COMPLETED").upper()
            if target == "ARCHIVED" or target not in WORK_STATES:
                target = "COMPLETED"
            return {"work": self.transition_work(work_id, target, actor=actor, reason=reason), "duplicate": False}
        raise ChildWorkError("unsupported Work lifecycle action")

    def _validate_outcome(
        self,
        connection,
        work: dict[str, Any],
        *,
        result_refs: list[str],
        artifact_refs: list[str],
        evidence_refs: list[str],
        acceptance_refs: list[str],
    ) -> None:
        if not result_refs or not evidence_refs or not acceptance_refs:
            raise ChildWorkError("Work completion requires Result, Evidence and Acceptance")
        delegation = work["data"].get("leaderDelegation")
        summary_ref = None
        if delegation:
            summary_ref = delegation.get("summaryWorkRef")
            if not summary_ref:
                raise ChildWorkError("Leader summary is still missing")
            for ref in [*delegation["childWorkRefs"], summary_ref]:
                child = self._entity(self._row(connection, ref, "WORK"))
                ResourceScopePolicy.require_same_execution_scope(self._scope(connection, work), self._scope(connection, child))
                if (child["data"].get("leaderRootWorkRef") != work["entity_id"] or child["parent_id"] != work["parent_id"]
                        or child["lifecycle_status"] != "COMPLETED"):
                    raise ChildWorkError("Leader children require existing explicit outcome acceptance")
            summary = self._entity(self._row(connection, summary_ref, "WORK"))
            if set(result_refs) != set(summary["data"].get("resultRefs") or []):
                raise ChildWorkError("Original Work must accept its exact Leader summary Result")
        task_ids = []
        for ref in result_refs:
            if not ref.startswith("task:"):
                raise ChildWorkError("Work Result must reference a ResultStore Task")
            task_id = ref.split(":", 1)[1]
            task = connection.execute(
                "select * from tasks where tenant_id=? and task_id=?",
                (self.tenant_id, task_id),
            ).fetchone()
            if task is None or task["status"] != "COMPLETED" or task["company_id"] != work["company_id"]:
                raise ChildWorkError("Work Result Task is missing, incomplete or outside the Company")
            # Broader scopes must never accept same-Company-only legacy results.
            # Keep the original Workspace compatibility path until its callers migrate.
            if not work["workspace_id"] or delegation or work["data"].get("leaderRootWorkRef"):
                ResourceScopePolicy.require_same_execution_scope(
                    self._scope(connection, dict(task)), self._scope(connection, work),
                )
                if task["work_ref"] != (summary_ref or work["entity_id"]):
                    raise ChildWorkError("Result Task does not belong to this Work")
            task_ids.append(task_id)
        for ref in artifact_refs:
            artifact = connection.execute(
                "select task_id from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, ref),
            ).fetchone()
            if artifact is None or artifact["task_id"] not in task_ids:
                raise ChildWorkError("Work Artifact is not owned by a Work Result")
        for ref in evidence_refs:
            evidence = self._row(connection, ref, "EVIDENCE")
            ResourceScopePolicy.require_same_execution_scope(self._scope(connection, dict(evidence)), self._scope(connection, work))
            if (
                evidence["parent_id"] != work["entity_id"]
                or evidence["company_id"] != work["company_id"]
                or evidence["workspace_id"] != work["workspace_id"]
                or evidence["verification_status"] != "VERIFIED"
                or evidence["evidence_condition"] != "CURRENT"
            ):
                raise ChildWorkError("Work Evidence is stale, unverified or outside the Work")
        for ref in acceptance_refs:
            acceptance = self._entity(self._row(connection, ref, "ACCEPTANCE"))
            ResourceScopePolicy.require_same_execution_scope(self._scope(connection, acceptance), self._scope(connection, work))
            data = acceptance["data"]
            if (
                acceptance["parent_id"] != work["entity_id"]
                or acceptance["company_id"] != work["company_id"]
                or acceptance["workspace_id"] != work["workspace_id"]
                or acceptance["lifecycle_status"] != "CLOSED"
                or set(data.get("resultRefs") or []) != set(result_refs)
                or set(data.get("evidenceRefs") or []) != set(evidence_refs)
            ):
                raise ChildWorkError("Work Acceptance does not cover current Result/Evidence truth")

    def complete_work(
        self,
        work_id: str,
        *,
        result_refs: list[str],
        artifact_refs: list[str] | None,
        evidence_refs: list[str],
        acceptance_refs: list[str],
    ) -> dict[str, Any]:
        values = {
            "resultRefs": _unique(result_refs),
            "artifactRefs": _unique(artifact_refs),
            "evidenceRefs": _unique(evidence_refs),
            "acceptanceRefs": _unique(acceptance_refs),
        }
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            work = self._entity(self._row(connection, work_id, "WORK"))
            return self._complete_work_locked(connection, work, values)

    def _complete_work_locked(self, connection, work, values):
        if work["lifecycle_status"] == "COMPLETED":
            if any(work["data"].get(key) != value for key, value in values.items()):
                raise ChildWorkError("completed Work replay has conflicting outcome truth")
            return work
        if work["lifecycle_status"] != "ACTIVE":
            raise ChildWorkError("only ACTIVE Work can complete")
        self._validate_outcome(
            connection,
            work,
            result_refs=values["resultRefs"],
            artifact_refs=values["artifactRefs"],
            evidence_refs=values["evidenceRefs"],
            acceptance_refs=values["acceptanceRefs"],
        )
        data = {**work["data"], **values, "completedAt": _now()}
        if data.get("responsibilityRouting"):
            route = dict(data["responsibilityRouting"])
            human = route.get("humanInput") or {}
            if human and human.get("state") not in {"CLOSED", "INVALIDATED"}:
                raise ChildWorkError("open Human Input must close before Work completion")
            route.update(status="COMPLETED", currentExecutorRef=None, lastAction="COMPLETE", updatedAt=data["completedAt"])
            for key in ("resultRefs", "artifactRefs", "evidenceRefs"):
                route[key] = _unique([*route.get(key, []), *values[key]])
            data["responsibilityRouting"] = route
        connection.execute(
            "update runtime_entities set data_json=? where tenant_id=? and entity_id=? and lifecycle_status='ACTIVE'",
            (_json(data), self.tenant_id, work["entity_id"]),
        )
        live = self._entity(self._row(connection, work["entity_id"], "WORK"))
        return self._transition_locked(connection, live, "COMPLETED", actor="SYSTEM", reason="Work outcome accepted")

    def _accept_agent_result_locked(self, connection, work, result_ref, proof, release_key):
        identity = TenantContext.current_identity()
        actor = str(identity.get("ceo_id") or "")
        if identity.get("role", "").lower() not in {"ceo", "owner"} or not actor:
            raise ChildWorkError("explicit result acceptance requires the current Company owner")
        if result_ref != "task:" + str(proof.get("task_ref") or ""):
            raise ChildWorkError("acceptance must cover the exact original Task Result")
        task = connection.execute("select * from tasks where tenant_id=? and task_id=? and company_id=? "
            "and workspace_id is ? and work_ref=? and status='COMPLETED' and requested_capability_type='agent'",
            (self.tenant_id, proof["task_ref"], work["company_id"], work["workspace_id"], work["entity_id"])).fetchone()
        usage = connection.execute("select * from ai_usage_records where tenant_id=? and task_id=? and company_id=? "
            "and work_ref=? and execution_status='success'",
            (self.tenant_id, proof["task_ref"], work["company_id"], work["entity_id"])).fetchall()
        cycle = self._cycle(connection, work["data"]["cycleRef"])
        contract = work["data"].get("followupContract") or cycle["data"].get("contract") or {}
        source = (contract.get("agentSource") or {}).get("snapshot")
        source_hash = hashlib.sha256(json.dumps(source, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if (not task or hashlib.sha256(task["output"].encode()).hexdigest() != proof.get("task_output_sha256")
                or len(usage) != 1 or usage[0]["usage_record_id"] != proof.get("usage_record_id")
                or source_hash != proof.get("source_snapshot_sha256") or proof.get("content_verification") != "UNVERIFIED"):
            raise ChildWorkError("original execution, metering or source changed before acceptance")
        artifacts = connection.execute("select artifact_id,content_sha256,content from artifacts where tenant_id=? and task_id=? "
            "order by artifact_id", (self.tenant_id, proof["task_ref"])).fetchall()
        if ([(r["artifact_id"], r["content_sha256"]) for r in artifacts] !=
                [(r["artifact_ref"], r["content_sha256"]) for r in proof.get("artifacts", [])]
                or any(hashlib.sha256(r["content"].encode()).hexdigest() != r["content_sha256"] for r in artifacts)):
            raise ChildWorkError("original result receipts changed before acceptance")
        if work["lifecycle_status"] == "COMPLETED":
            if result_ref not in work["data"].get("resultRefs", []):
                raise ChildWorkError("completed parent does not cover this Result")
            return work
        if work["lifecycle_status"] != "ACTIVE":
            raise ChildWorkError("only ACTIVE original Work may receive explicit result acceptance")
        if cycle["lifecycle_status"] in {"CLOSED", "COMPLETED", "CANCELLED", "ARCHIVED"}:
            raise ChildWorkError("closed Cycle cannot receive a new parent Work acceptance")
        evidence_id = _stable_id("evidence", self.tenant_id, work["entity_id"], result_ref)
        acceptance_id = _stable_id("acceptance", self.tenant_id, work["entity_id"], result_ref)
        at = _now()
        evidence = {"kind": "AGENT_EXECUTION_PROVENANCE", **proof,
            "summary": "Original Task, unique Usage, source snapshot and recorded file hashes verified; content remains UNVERIFIED"}
        acceptance = {"resultRefs": [result_ref], "evidenceRefs": [evidence_id], "requestedBy": actor,
            "requestId": release_key, "decision": "ACCEPT_FOR_LINKED_FOLLOWUP", "contentVerification": "UNVERIFIED"}
        for entity_id, kind, state, verification, condition, data in (
                (evidence_id, "EVIDENCE", "CURRENT", "VERIFIED", "CURRENT", evidence),
                (acceptance_id, "ACCEPTANCE", "PENDING", "UNVERIFIED", "MISSING", acceptance)):
            connection.execute(
                "insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,"
                "lifecycle_status,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (entity_id, self.tenant_id, kind, work["company_id"], work["workspace_id"], work["entity_id"],
                 actor, state, verification, condition, _json(data), at, at))
        source_state = "PENDING"
        for target, machine_actor, trigger in (("ACCEPTED", "CEO", "accept"), ("CLOSED", "SYSTEM", "close")):
            record = get_registered_machine("acceptance").transition(acceptance_id, source_state, target,
                actor=machine_actor, trigger=trigger, reason="User explicitly accepted this Result for linked follow-up",
                context={"companyId": work["company_id"], "workspaceId": work["workspace_id"],
                         "evidenceRefs": [evidence_id], "ceoId": actor}, record=False)
            connection.execute("insert into runtime_transition_log(tenant_id,entity_type,entity_id,source,target,trigger,actor,"
                "at,reason,company_id,workspace_id,evidence_refs_json,context_json) values (?,'acceptance',?,?,?,?,?,?,?,?,?,?,?)",
                (self.tenant_id, acceptance_id, record.source, record.target, trigger, machine_actor, record.at,
                 record.reason, work["company_id"], work["workspace_id"], _json([evidence_id]), _json(record.context)))
            source_state = target
        connection.execute("update runtime_entities set lifecycle_status='CLOSED' where tenant_id=? and entity_id=?",
            (self.tenant_id, acceptance_id))
        return self._complete_work_locked(connection, work, {"resultRefs": [result_ref],
            "artifactRefs": [r["artifact_id"] for r in artifacts], "evidenceRefs": [evidence_id],
            "acceptanceRefs": [acceptance_id]})

    def release_next_work(
        self,
        parent_work_id: str,
        *,
        release_key: str,
        target_assignment_ref: str,
        accepted_result_ref: str,
        input_refs: list[str] | None = None,
        reason: str,
        required: bool = True,
        followup_contract: dict[str, Any] | None = None,
        parent_acceptance: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        key = release_key.strip()
        if not key or not reason.strip():
            raise ChildWorkError("next Work release requires key and reason")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            parent = self._entity(self._row(connection, parent_work_id, "WORK"))
            if parent_acceptance is not None:
                if followup_contract is None:
                    raise ChildWorkError("explicit Agent acceptance requires a linked follow-up contract")
                parent = self._accept_agent_result_locked(connection, parent, accepted_result_ref, parent_acceptance, key)
            if parent["lifecycle_status"] != "COMPLETED" or accepted_result_ref not in parent["data"].get("resultRefs", []):
                raise ChildWorkError("next Work requires an accepted parent Work Result")
            cycle = self._cycle(connection, parent["parent_id"])
            target = self._assignment(connection, target_assignment_ref, cycle)
            previous_cycle = cycle
            root_ref = parent["data"].get("rootWorkRef") or parent_work_id
            closed = cycle["lifecycle_status"].upper() in {"CLOSED", "COMPLETED", "CANCELLED", "ARCHIVED"}
            if not closed and cycle["lifecycle_status"] not in {"PLANNED", "READY", "RUNNING"}:
                raise ChildWorkError("current Cycle is paused or waiting for a required review")
            if closed and followup_contract is None:
                raise ChildWorkError("closed Cycle requires an explicit new bounded continuation contract")
            if followup_contract is not None:
                if (not isinstance(followup_contract, dict) or len(_json(followup_contract).encode()) > 65536
                        or not str(followup_contract.get("problem") or "").strip()
                        or not str(followup_contract.get("expectedResult") or "").strip()):
                    raise ChildWorkError("explicit follow-up requires bounded new input and expected result")
                root = self._entity(self._row(connection, root_ref, "WORK"))
                ResourceScopePolicy.require_same_execution_scope(self._scope(connection, root), self._scope(connection, parent))
                original_cycle = self._cycle(connection, root["parent_id"])
                original = original_cycle["data"].get("contract") or {}
                if (target_assignment_ref != parent["data"]["responsibilityAssignmentRef"]
                        or target_assignment_ref != root["data"]["responsibilityAssignmentRef"]
                        or any(target[field] != prior["data"][field] for prior in (parent, root)
                               for field in ("assignmentRevision", "holderEmployeeRef"))
                        or followup_contract.get("agentBinding") != original.get("agentBinding")
                        or not original.get("agentBinding")):
                    raise ChildWorkError("explicit follow-up must preserve the original Employee, Assignment and Agent binding")
                old_source = (original.get("agentSource") or {}).get("input") or {}
                new_source = (followup_contract.get("agentSource") or {}).get("input") or {}
                if any(old_source.get(key) != new_source.get(key) for key in
                       ("kind", "book_ref", "chapter_ref", "content_ref", "song_ref")):
                    raise ChildWorkError("follow-up cannot replace the original professional object")
                original_thread = ((original.get("agentSource") or {}).get("snapshot") or {}).get("conversation_id")
                new_thread = ((followup_contract.get("agentSource") or {}).get("snapshot") or {}).get("conversation_id")
                if not original_thread or new_thread != original_thread:
                    raise ChildWorkError("follow-up must preserve the original Conversation")
                if closed:
                    new_cycle_id = _stable_id("cycle", self.tenant_id, parent_work_id, "followup:" + key)
                    cycle_successors = connection.execute(
                        "select target_id from runtime_links where tenant_id=? and source_id=? and relation='HAS_SUCCESSOR_CYCLE'",
                        (self.tenant_id, cycle["entity_id"])).fetchall()
                    if len(cycle_successors) > 1 or any(row["target_id"] != new_cycle_id for row in cycle_successors):
                        raise ChildWorkError("closed Cycle already has another successor Cycle")
                    data = {"kind": "GENERAL_WORK_CYCLE", "contract": followup_contract,
                        "releaseKey": "followup:" + key, "scopeType": cycle["data"]["scopeType"],
                        "scopeRef": cycle["data"]["scopeRef"], "predecessorCycleRef": cycle["entity_id"],
                        "predecessorWorkRef": parent_work_id, "rootWorkRef": root_ref,
                        "acceptedResultRef": accepted_result_ref}
                    found = connection.execute("select * from runtime_entities where tenant_id=? and entity_id=?",
                        (self.tenant_id, new_cycle_id)).fetchone()
                    if found is None:
                        at = _now()
                        connection.execute(
                            "insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,owner_ref,"
                            "lifecycle_status,verification_status,evidence_condition,data_json,created_at,updated_at) "
                            "values (?,?,'CYCLE',?,?,?,'PLANNED','UNVERIFIED','MISSING',?,?,?)",
                            (new_cycle_id, self.tenant_id, parent["company_id"], parent["workspace_id"],
                             target["holderEmployeeRef"], _json(data), at, at))
                    elif self._entity(found)["data"] != data:
                        raise ChildWorkError("new bounded Cycle conflicts with the original follow-up request")
                    cycle = self._cycle(connection, new_cycle_id)
            child_id = _stable_id("work", self.tenant_id, cycle["entity_id"], f"{parent_work_id}:{key}")
            handoff_id = _stable_id("handoff", self.tenant_id, parent_work_id, key)
            successor = connection.execute(
                "select target_id from runtime_links where tenant_id=? and source_id=? and relation='HAS_SUCCESSOR_WORK'",
                (self.tenant_id, parent_work_id),
            ).fetchone()
            existing_child = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, child_id),
            ).fetchone()
            existing_handoff = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, handoff_id),
            ).fetchone()
            if successor or existing_child or existing_handoff:
                if not successor or successor["target_id"] != child_id or not existing_child or not existing_handoff:
                    raise ChildWorkError("next Work release truth is partial or conflicts with existing lineage")
                child = self._entity(existing_child)
                handoff = self._entity(existing_handoff)
                if (
                    child["data"].get("predecessorWorkRef") != parent_work_id
                    or child["data"].get("responsibilityAssignmentRef") != target_assignment_ref
                    or handoff["data"].get("acceptedResultRef") != accepted_result_ref
                    or handoff["data"].get("releaseKey") != key
                    or (followup_contract is not None and child["data"].get("followupContract") != followup_contract)
                ):
                    raise ChildWorkError("duplicate release key has different target or provenance")
                return {"work": child, "handoff": handoff, "duplicate": True}
            at = _now()
            handoff_data = {
                "kind": "CHILD_WORK_RELEASE",
                "releaseKey": key,
                "cycleRef": cycle["entity_id"],
                "fromWorkRef": parent_work_id,
                "fromAssignmentRef": parent["data"]["responsibilityAssignmentRef"],
                "fromEmployeeRef": parent["data"]["holderEmployeeRef"],
                "toWorkRef": child_id,
                "toAssignmentRef": target_assignment_ref,
                "toEmployeeRef": target["holderEmployeeRef"],
                "acceptedResultRef": accepted_result_ref,
                "evidenceRefs": list(parent["data"].get("evidenceRefs") or []),
                "reason": reason.strip()[:2000],
                "acknowledgement": {"mode": "RUNTIME_ATOMIC_ACCEPTANCE", "manualConfirmationRequired": False},
                "createdAt": at,
                "acknowledgedAt": at,
            }
            if followup_contract is not None:
                handoff_data.update({"rootWorkRef": root_ref, "fromCycleRef": previous_cycle["entity_id"],
                    "toCycleRef": cycle["entity_id"]})
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, parent_id, "
                "owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, 'HANDOFF', ?, ?, ?, ?, 'CREATED', 'UNVERIFIED', 'MISSING', ?, ?, ?)",
                (
                    handoff_id,
                    self.tenant_id,
                    parent["company_id"],
                    parent["workspace_id"],
                    parent_work_id,
                    target["holderEmployeeRef"],
                    _json(handoff_data),
                    at,
                    at,
                ),
            )
            child = self._create_work_locked(
                connection,
                cycle=cycle,
                assignment_ref=target_assignment_ref,
                release_key=f"{parent_work_id}:{key}",
                required=required,
                input_refs=_unique([parent_work_id, handoff_id, accepted_result_ref, *(input_refs or [])]),
                predecessor_work_ref=parent_work_id,
                at=at,
            )
            if child["entity_id"] != child_id:
                raise ChildWorkError("next Work deterministic identity mismatch")
            if followup_contract is not None:
                data = {**child["data"], "rootWorkRef": root_ref, "followupContract": followup_contract,
                        "acceptedPredecessorResultRef": accepted_result_ref, "releaseHandoffRef": handoff_id}
                connection.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                    (_json(data), self.tenant_id, child_id))
                child = self._entity(self._row(connection, child_id, "WORK"))
                if cycle["entity_id"] != previous_cycle["entity_id"]:
                    self._insert_link(connection, previous_cycle, "HAS_SUCCESSOR_CYCLE", cycle["entity_id"], at)
                    self._insert_link(connection, cycle, "HAS_PREDECESSOR_CYCLE", previous_cycle["entity_id"], at)
            machine = get_registered_machine("handoff")
            source = "CREATED"
            for target_state, actor, trigger in (
                ("SENT", "SYSTEM", "send"),
                ("ACKNOWLEDGED", "AI_EMPLOYEE", "acknowledge"),
                ("COMPLETED", "AI_EMPLOYEE", "complete"),
            ):
                record = machine.transition(
                    handoff_id,
                    source,
                    target_state,
                    actor=actor,
                    trigger=trigger,
                    reason=reason,
                    context={"fromWorkRef": parent_work_id, "toWorkRef": child_id},
                    record=False,
                )
                connection.execute(
                    "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, trigger, actor, "
                    "at, reason, company_id, workspace_id, context_json) values (?, 'handoff', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        self.tenant_id,
                        handoff_id,
                        record.source,
                        record.target,
                        record.trigger,
                        record.actor,
                        record.at,
                        reason,
                        parent["company_id"],
                        parent["workspace_id"],
                        _json(record.context),
                    ),
                )
                source = target_state
            connection.execute(
                "update runtime_entities set lifecycle_status='COMPLETED', updated_at=? where tenant_id=? and entity_id=? "
                "and lifecycle_status='CREATED'",
                (at, self.tenant_id, handoff_id),
            )
            self._insert_link(connection, parent, "HAS_SUCCESSOR_WORK", child_id, at)
            self._insert_link(connection, child, "HAS_PREDECESSOR_WORK", parent_work_id, at)
            self._insert_link(connection, parent, "HAS_RELEASE_HANDOFF", handoff_id, at)
            return {
                "work": self._entity(self._row(connection, child_id, "WORK")),
                "handoff": self._entity(self._row(connection, handoff_id, "HANDOFF")),
                "duplicate": False,
            }

    def aggregate_cycle(self, cycle_id: str, *, require_complete: bool = True) -> dict[str, Any]:
        with self.db.connect() as connection:
            cycle = self._cycle(connection, cycle_id)
            rows = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_type='WORK' and parent_id=? "
                "order by created_at, entity_id",
                (self.tenant_id, cycle_id),
            ).fetchall()
            works = [self._entity(row) for row in rows]
            if not works:
                return {"mode": "LEGACY", "cycleRef": cycle_id, "workRefs": []}
            summaries = []
            result_refs: list[str] = []
            artifact_refs: list[str] = []
            evidence_refs: list[str] = []
            acceptance_refs: list[str] = []
            for work in works:
                data = work["data"]
                ResourceScopePolicy.require_same_execution_scope(
                    self._scope(connection, work), self._scope(connection, cycle),
                )
                if require_complete and data.get("required", True) and work["lifecycle_status"] != "COMPLETED":
                    raise ChildWorkError("required child Work is not complete")
                if work["lifecycle_status"] == "COMPLETED":
                    values = {
                        "result_refs": list(data.get("resultRefs") or []),
                        "artifact_refs": list(data.get("artifactRefs") or []),
                        "evidence_refs": list(data.get("evidenceRefs") or []),
                        "acceptance_refs": list(data.get("acceptanceRefs") or []),
                    }
                    self._validate_outcome(connection, work, **values)
                    result_refs.extend(values["result_refs"])
                    artifact_refs.extend(values["artifact_refs"])
                    evidence_refs.extend(values["evidence_refs"])
                    acceptance_refs.extend(values["acceptance_refs"])
                summaries.append({
                    "workRef": work["entity_id"],
                    "required": bool(data.get("required", True)),
                    "status": work["lifecycle_status"],
                    "responsibilityAssignmentRef": data["responsibilityAssignmentRef"],
                    "holderEmployeeRef": data["holderEmployeeRef"],
                    "predecessorWorkRef": data.get("predecessorWorkRef"),
                    "resultRefs": list(data.get("resultRefs") or []),
                    "artifactRefs": list(data.get("artifactRefs") or []),
                    "evidenceRefs": list(data.get("evidenceRefs") or []),
                    "acceptanceRefs": list(data.get("acceptanceRefs") or []),
                })
            payload = {
                "mode": "CHILD_WORK",
                "cycleRef": cycle_id,
                "workRefs": [item["workRef"] for item in summaries],
                "requiredWorkRefs": [item["workRef"] for item in summaries if item["required"]],
                "completedWorkRefs": [item["workRef"] for item in summaries if item["status"] == "COMPLETED"],
                "failedWorkRefs": [item["workRef"] for item in summaries if item["status"] == "FAILED"],
                "resultRefs": _unique(result_refs),
                "artifactRefs": _unique(artifact_refs),
                "evidenceRefs": _unique(evidence_refs),
                "acceptanceRefs": _unique(acceptance_refs),
                "workSummaries": summaries,
            }
            payload["aggregationHash"] = hashlib.sha256(_json(payload).encode()).hexdigest()
            return payload
