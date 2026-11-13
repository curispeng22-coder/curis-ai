"""Read-only Company OS projection shared by compiled and packaged Workspaces."""

from __future__ import annotations

import json
from contextlib import nullcontext
from typing import Any

from .database import Database
from .resource_scope_policy import ResourceScopePolicy
from .runtime import RuntimeFoundation, RuntimeScopeError
from .runtime.child_work import WORK_STATES
from .tenant_context import TenantContext


_REFERENCE_KEYS = frozenset({"artifactRefs", "evidenceRefs", "resultRefs", "outputRefs"})


def canonical_work_status(work: dict[str, Any]) -> str:
    lifecycle = str(work.get("lifecycle_status") or "UNKNOWN").upper()
    if lifecycle not in WORK_STATES:
        return "UNKNOWN"
    if lifecycle != "ACTIVE":
        return lifecycle
    data = work.get("data") or _json(work.get("data_json"))
    return str((data.get("responsibilityRouting") or {}).get("status") or "UNKNOWN").upper()


def _json(value: str | None) -> dict[str, Any]:
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _refs(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in _REFERENCE_KEYS and isinstance(item, list):
                found.extend(str(ref) for ref in item if ref)
            elif isinstance(item, (dict, list)):
                found.extend(_refs(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_refs(item))
    return list(dict.fromkeys(found))


class SharedWorkspaceProjection:
    """Unifies existing facts without owning any business transition."""

    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def workspace(self, company_id: str, workspace_id: str) -> dict[str, Any]:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as connection:
            company = connection.execute(
                "select company_id, name, description, company_type, status from companies "
                "where tenant_id = ? and company_id = ?",
                (self.tenant_id, company_id),
            ).fetchone()
            workspace = connection.execute(
                "select workspace_id, company_id, business_id, name, status, blueprint_version, "
                "operating_version, business_relation_status, business_relation_reason, updated_at from workspaces "
                "where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
            rows = connection.execute(
                "select * from runtime_entities where tenant_id = ? and company_id = ? "
                "and workspace_id = ? order by updated_at, entity_id",
                (self.tenant_id, company_id, workspace_id),
            ).fetchall()
            links = connection.execute(
                "select source_id, relation, target_id from runtime_links where tenant_id = ? "
                "and company_id = ? and workspace_id = ? order by created_at, link_id",
                (self.tenant_id, company_id, workspace_id),
            ).fetchall()
            business = connection.execute(
                "select business_id, business_id as direction_id, department_id, name, "
                "goal as target_outcome, positioning, lifecycle_status "
                "from canonical_businesses where tenant_id=? and company_id=? and business_id=?",
                (self.tenant_id, company_id, workspace["business_id"] if workspace else ""),
            ).fetchone()
        if company is None or workspace is None:
            raise RuntimeScopeError("workspace does not belong to current Company")

        entities = [self._entity(row) for row in rows]
        team_entities = self._general_assignment_entities(company_id, workspace_id, entities)
        by_type: dict[str, list[dict[str, Any]]] = {}
        by_id = {item["entity_id"]: item for item in team_entities}
        for item in team_entities:
            by_type.setdefault(item["entity_type"], []).append(item)
        link_rows = [dict(row) for row in links]
        roles = by_type.get("ROLE_SLOT", [])
        bindings = by_type.get("CAPABILITY_BINDING", [])
        work_items = self._work_items(entities, roles, link_rows)
        employees = [
            self._employee(item, roles, bindings, work_items, link_rows)
            for item in by_type.get("AI_EMPLOYEE", [])
        ]
        organization = self._employee_organization(
            company_id, [item["company_employee_ref"] for item in employees],
        )
        for employee in employees:
            record = organization.get(employee["company_employee_ref"])
            if record and employee["identity_status"] == "VERIFIED_EXPLICIT_BRIDGE":
                record["identity_status"] = employee["identity_status"]
            employee["organization_record"] = record
        result_refs = _refs([item["data"] for item in entities])
        result_index = [
            summary for ref in result_refs
            if (summary := self._result(company_id, workspace_id, ref, include_content=False))
        ]
        project_refs = list(dict.fromkeys(
            str(item["data"].get("projectRef"))
            for item in entities if item["data"].get("projectRef")
        ))
        projects, departments = self._projects(company_id, project_refs)
        if business and business["department_id"] not in {item["department_id"] for item in departments}:
            with self.db.connect() as connection:
                department = connection.execute(
                    "select id as department_id, name, department_type, status from department_instances "
                    "where tenant_id=? and company_id=? and id=? and deleted_at is null",
                    (self.tenant_id, company_id, business["department_id"]),
                ).fetchone()
            if department:
                departments = [dict(department), *departments]
        return {
            "company": dict(company),
            "business": dict(business) | {"resolved": True} if business else {
                "direction_id": workspace["business_id"], "resolved": False,
                "status": workspace["business_relation_status"],
                "reason": workspace["business_relation_reason"],
            },
            "workspace": dict(workspace),
            "departments": departments,
            "projects": projects,
            "team": {
                "role_slots": [self._role(role, by_id) for role in roles],
                "employees": employees,
                "capability_bindings": [self._binding(item) for item in bindings],
            },
            "work_items": work_items,
            "system_activity": [
                {"object_ref": item["object_ref"], **item["system_activity"]}
                for item in work_items if item["system_activity"]
            ],
            "results": result_index,
            "updated_at": workspace["updated_at"],
        }

    def _general_assignment_entities(self, company_id, workspace_id, entities):
        """Read current General responsibility links without moving Company Employees."""
        workflows = [item for item in entities
            if item["entity_type"] == "RESPONSIBILITY_WORKFLOW"
            and item["data"].get("workflowKey") == "general-operating"]
        if not workflows:
            return entities
        local_employees = {item["entity_id"] for item in entities if item["entity_type"] == "AI_EMPLOYEE"}
        referenced = {assignment.get("employeeRef") for workflow in workflows
            for assignment in workflow["data"].get("assignments") or []}
        # Workspace-owned legacy teams keep their accepted projection contract.
        if referenced and referenced.issubset(local_employees):
            return entities
        def reject():
            raise RuntimeScopeError("General team assignment or execution identity requires review")
        versions = [item["data"].get("version") for item in workflows]
        if any(type(version) is not int or version < 1 for version in versions):
            reject()
        latest = [item for item in workflows if item["data"]["version"] == max(versions)]
        if len(latest) != 1 or latest[0]["lifecycle_status"] != "PUBLISHED":
            reject()
        workflow = latest[0]["data"]
        if workflow.get("scopeType") != "WORKSPACE" or workflow.get("scopeRef") != workspace_id:
            reject()
        assignments = workflow.get("assignments") or []
        if not assignments:
            reject()
        by_id = {item["entity_id"]: item for item in entities}
        projected = {}
        role_holders = {}
        employee_roles = {}
        keys = set()
        with self.db.connect() as connection:
            for snapshot in assignments:
                assignment = by_id.get(snapshot.get("assignmentRef"))
                if not assignment or assignment["entity_type"] != "RESPONSIBILITY_ASSIGNMENT" or assignment["lifecycle_status"] != "ACTIVE":
                    reject()
                data = assignment["data"]
                if data.get("scopeType") != "WORKSPACE" or data.get("scopeRef") != workspace_id:
                    reject()
                if any(snapshot.get(key) != data.get(key) for key in ("roleRef", "employeeRef", "responsibilityKey", "responsibility")) or snapshot.get("assignmentRevision") != data.get("revision"):
                    reject()
                role_ref, employee_ref, key = data.get("roleRef"), data.get("employeeRef"), data.get("responsibilityKey")
                if not role_ref or not employee_ref or not key or key in keys or role_ref in role_holders or employee_ref in employee_roles:
                    reject()
                role = by_id.get(role_ref)
                if not role or role["entity_type"] != "ROLE_SLOT" or role["lifecycle_status"] not in {"ASSIGNED", "OPERATING"}:
                    reject()
                if role["data"].get("assignedEmployeeRef") not in (None, "", employee_ref):
                    reject()
                row = connection.execute(
                    "select * from runtime_entities where tenant_id=? and company_id=? "
                    "and entity_id=? and entity_type='AI_EMPLOYEE' and (workspace_id is null or workspace_id=?)",
                    (self.tenant_id, company_id, employee_ref, workspace_id),
                ).fetchone()
                if row is None:
                    reject()
                employee = self._entity(row)
                bridge = employee["data"].get("identityBridge") or {}
                company_ref = employee["data"].get("companyEmployeeRef")
                if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"} or not company_ref or bridge.get("status") != "VERIFIED" or bridge.get("companyEmployeeRef") != company_ref:
                    reject()
                identity = connection.execute(
                    "select i.id from employee_instances i join employee_capability_bindings b "
                    "on b.tenant_id=i.tenant_id and b.employee_id=i.id "
                    "where i.tenant_id=? and i.company_id=? and i.id=? and i.enabled=1 "
                    "and i.deleted_at is null and i.status in ('idle','assigned') and b.id=? and b.enabled=1",
                    (self.tenant_id, company_id, company_ref, bridge.get("verifiedByEmployeeCapabilityBindingRef")),
                ).fetchone()
                if identity is None:
                    reject()
                keys.add(key)
                role_holders[role_ref] = employee_ref
                employee_roles[employee_ref] = role_ref
                projected[role_ref] = {**role, "data": {**role["data"], "assignedEmployeeRef": employee_ref}}
                projected[employee_ref] = {**employee, "data": {**employee["data"], "roleSlotRef": role_ref}}
        flow = workflow.get("defaultFlow") or []
        if not flow or len(set(flow)) != len(flow) or not set(flow).issubset(keys):
            reject()
        # These are projection-local copies; canonical identity and Role data stay unchanged.
        return [projected.pop(item["entity_id"], item) for item in entities] + list(projected.values())

    def employees(self, company_id: str, workspace_id: str) -> list[dict[str, Any]]:
        return self.workspace(company_id, workspace_id)["team"]["employees"]

    def general_workspace(self, company_id: str, workspace_id: str) -> dict[str, Any]:
        """Product read model for a Generic Workspace; never guesses a Team."""

        snapshot = self.workspace(company_id, workspace_id)
        with self.db.connect() as connection:
            row = connection.execute(
                "select blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
        blueprint = _json(row["blueprint_json"] if row else None)
        if str(blueprint.get("productForm") or "").upper() != "GENERIC":
            raise RuntimeScopeError("Workspace is not a General Workspace")

        workflows = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id,
            )
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == workspace_id
            and not str(item["data"].get("workflowKey") or "").startswith("meeting:")
        ]
        workflow_keys = sorted({str(item["data"].get("workflowKey") or "") for item in workflows})
        assignments = {
            item["assignmentRef"]: item
            for workflow in workflows for item in workflow["data"].get("assignments") or []
        }
        employees = snapshot["team"]["employees"]
        employee_names = {item["employee_ref"]: item["name"] for item in employees}
        current_work = []
        for work in self.foundation.list("WORK", company_id=company_id, workspace_id=workspace_id):
            routing = work["data"].get("responsibilityRouting") or {}
            if not routing:
                continue
            try:
                cycle = self.foundation.get(work.get("parent_id") or "")
                if cycle["entity_type"] != "CYCLE" or cycle["company_id"] != company_id or cycle["workspace_id"] != workspace_id:
                    cycle = {"data": {}}
            except KeyError:
                cycle = {"data": {}}
            contract = cycle["data"].get("contract") or {}
            executions = list((routing.get("executions") or {}).values())
            latest = executions[-1] if executions else {}
            lifecycle_status = str(work["lifecycle_status"] or "UNKNOWN").upper()
            responsibility_status = str(routing.get("status") or "UNKNOWN").upper()
            status = canonical_work_status(work)
            holder_ref = str(routing.get("responsibilityHolderRef") or "")
            holder_name = employee_names.get(holder_ref)
            if holder_ref and not holder_name:
                with self.db.connect() as connection:
                    holder = connection.execute(
                        "select coalesce(i.name, json_extract(e.data_json,'$.name')) name from runtime_entities e "
                        "left join employee_instances i on i.tenant_id=e.tenant_id and i.company_id=e.company_id "
                        "and i.id=coalesce(json_extract(e.data_json,'$.companyEmployeeRef'),e.entity_id) "
                        "and i.enabled=1 and i.deleted_at is null "
                        "where e.tenant_id=? and e.company_id=? and (e.workspace_id is null or e.workspace_id=?) "
                        "and e.entity_id=? and e.entity_type='AI_EMPLOYEE'",
                        (self.tenant_id, company_id, workspace_id, holder_ref),
                    ).fetchone()
                holder_name = holder["name"] if holder else None
            current_assignment = assignments.get(routing.get("currentAssignmentRef")) or {}
            result_refs = list(dict.fromkeys([
                *list(routing.get("resultRefs") or []),
                *[str(item.get("resultRef")) for item in executions if item.get("resultRef")],
            ]))
            evidence_refs = list(dict.fromkeys(
                str(ref) for item in executions for ref in item.get("evidenceRefs") or [] if ref
            ))
            artifact_refs = list(dict.fromkeys(
                str(ref) for item in executions for ref in item.get("artifactRefs") or [] if ref
            ))
            reason = str(latest.get("resultSummary") or routing.get("problem") or "")
            if lifecycle_status == status:
                with self.db.connect() as connection:
                    transition = connection.execute(
                        "select reason from runtime_transition_log where tenant_id=? and company_id=? "
                        "and workspace_id is ? and entity_type='work' and entity_id=? "
                        "and target=? order by rowid desc limit 1",
                        (self.tenant_id, company_id, workspace_id, work["entity_id"], lifecycle_status),
                    ).fetchone()
                reason = str((transition["reason"] if transition else "") or routing.get("cancelReason") or reason)
            recovery = (
                "恢复这项工作后继续" if status == "PAUSED"
                else "这项工作已归档，可按需恢复查看" if status == "ARCHIVED"
                else "这项工作已停止，历史结果与证据仍保留" if status == "CANCELLED"
                else "核对原执行与证据，确认恢复条件后再决定" if status in {"WAITING", "FAILED", "BLOCKED"}
                else "等待 CEO 完成当前决定" if status == "WAITING_DECISION"
                else "等待当前员工返回结果" if status in {"EXECUTING", "RUNNING"}
                else "责任已接续；尚未确认有员工执行" if status == "ACTIVE"
                else "当前工作已收口" if status == "COMPLETED"
                else "查看当前责任并继续"
            )
            decision = None
            decision_ref = routing.get("decisionPacketRef")
            if decision_ref:
                try:
                    packet = self.foundation.get(decision_ref)
                    if packet["company_id"] == company_id and packet["workspace_id"] == workspace_id:
                        decision = {
                            "decision_ref": packet["entity_id"],
                            "status": packet["lifecycle_status"],
                            **packet["data"],
                        }
                except KeyError:
                    decision = None
            handoffs = []
            for handoff_ref in routing.get("handoffRefs") or []:
                try:
                    handoff = self.foundation.get(handoff_ref)
                except KeyError:
                    continue
                if handoff["company_id"] == company_id and handoff["workspace_id"] == workspace_id:
                    handoff_data = handoff["data"]
                    from_assignment = assignments.get(handoff_data.get("fromAssignmentRef")) or {}
                    to_assignment = assignments.get(handoff_data.get("toAssignmentRef")) or {}
                    handoffs.append({
                        "handoff_ref": handoff["entity_id"],
                        "status": handoff["lifecycle_status"],
                        **handoff_data,
                        "from_responsibility": str(from_assignment.get("responsibilityKey") or "原责任"),
                        "to_responsibility": str(to_assignment.get("responsibilityKey") or "下一责任"),
                        "from_employee_name": employee_names.get(handoff_data.get("fromEmployeeRef")) or "原负责人",
                        "to_employee_name": employee_names.get(handoff_data.get("toEmployeeRef")) or "下一负责人",
                    })
            all_refs = list(dict.fromkeys([*result_refs, *evidence_refs, *artifact_refs]))
            current_work.append({
                "work_ref": work["entity_id"],
                "cycle_ref": work.get("parent_id"),
                "problem": str(contract.get("problem") or ""),
                "expected_result": str(contract.get("expectedResult") or ""),
                "status": status,
                "lifecycle_status": lifecycle_status,
                "responsibility_status": responsibility_status,
                "execution_status": str(latest.get("status") or "NONE").upper(),
                "responsibility_key": str(current_assignment.get("responsibilityKey") or ""),
                "responsibility_holder_ref": holder_ref or None,
                "responsibility_holder_name": holder_name or None,
                "current_executor_ref": None if lifecycle_status in {"COMPLETED", "CANCELLED", "ARCHIVED"} else routing.get("currentExecutorRef"),
                "reason": reason,
                "recovery_action": recovery,
                "result_refs": result_refs,
                "artifact_refs": artifact_refs,
                "evidence_refs": evidence_refs,
                "execution_count": len(executions),
                "resume_to": work["data"].get("pausedFrom"),
                "restore_to": work["data"].get("archivedFrom"),
                "human_input": (dict(routing["humanInput"]) if isinstance(routing.get("humanInput"), dict) else None),
                "decision": decision,
                "handoffs": handoffs,
                "result_summaries": [
                    summary for ref in all_refs
                    if (summary := self._result(company_id, workspace_id, ref, include_content=False))
                ],
                "updated_at": routing.get("updatedAt") or work.get("updated_at"),
            })
        if len(workflow_keys) != 1:
            readiness = "NEEDS_DECISION"
            reason = "尚未形成唯一的团队责任安排" if not workflow_keys else "存在多个团队责任安排，需要选择"
        elif not employees:
            readiness = "NEEDS_DECISION"
            reason = "责任安排尚未绑定可用员工"
        else:
            readiness = "READY_FOR_WORK"
            reason = "团队责任与员工已明确"
        return {
            "company": snapshot["company"],
            "business": snapshot["business"],
            "workspace": snapshot["workspace"],
            "goal": snapshot["business"].get("target_outcome") or blueprint.get("goal") or "",
            "proposal": blueprint.get("proposal") or None,
            "team": snapshot["team"],
            "current_work": current_work,
            "results": snapshot["results"],
            "system_activity": snapshot["system_activity"],
            "operating_readiness": {
                "status": readiness,
                "reason": reason,
                "workflow_key": workflow_keys[0] if len(workflow_keys) == 1 else None,
                "owner": "CEO" if readiness == "NEEDS_DECISION" else None,
                "next_action": "确认团队责任与员工" if readiness == "NEEDS_DECISION" else "创建工作",
            },
            "updated_at": snapshot["updated_at"],
        }

    def employee(self, company_id: str, workspace_id: str, employee_id: str) -> dict[str, Any]:
        snapshot = self.workspace(company_id, workspace_id)
        employee = next(
            (item for item in snapshot["team"]["employees"] if item["employee_ref"] == employee_id),
            None,
        )
        if employee is None:
            raise RuntimeScopeError("Employee is outside the current Workspace")
        return employee | {
            "organization": {
                "company": snapshot["company"],
                "workspace": snapshot["workspace"],
                "departments": snapshot["departments"],
                "reporting_to_ref": employee["reporting_to_ref"],
                "exact_company_employee": employee["organization_record"],
            },
        }

    def result(self, company_id: str, workspace_id: str | None, reference_id: str, *, scope=None) -> dict[str, Any]:
        if scope is None:
            self.foundation._require_workspace(workspace_id, company_id)
        else:
            with self.db.connect() as connection:
                requested = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=self.tenant_id,
                    company_id=company_id, scope_type=scope.get("scope_type"), scope_ref=scope.get("scope_ref"))
                ResourceScopePolicy.require_same_execution_scope(requested, ResourceScopePolicy.reference_scope(
                    connection, tenant_id=self.tenant_id, company_id=company_id, reference_id=reference_id))
                if workspace_id != requested["workspace_id"]:
                    raise RuntimeScopeError("Result scope does not match execution context")
        result = self._result(company_id, workspace_id, reference_id, include_content=True, scope=scope)
        if result is None:
            raise RuntimeScopeError("Result reference is outside the current Workspace")
        return result

    @staticmethod
    def _entity(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["data"] = _json(item.pop("data_json", None))
        return item

    @staticmethod
    def _role(role: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
        data = role["data"]
        employee_ref = data.get("assignedEmployeeRef")
        return {
            "role_slot_ref": role["entity_id"],
            "name": data.get("name") or "未命名岗位",
            "responsibility": data.get("responsibility") or "",
            "assigned_employee_ref": employee_ref,
            "assigned_employee_exists": employee_ref in by_id if employee_ref else False,
            "status": role["lifecycle_status"],
            "capability_requirement_refs": list(data.get("capabilityRefs") or []),
        }

    @staticmethod
    def _binding(binding: dict[str, Any]) -> dict[str, Any]:
        data = binding["data"]
        review = data.get("supplyReview") if isinstance(data.get("supplyReview"), dict) else {}
        blockers = list(review.get("blockers") or [])
        authorized = str(data.get("authorizationStatus") or "").startswith("AUTHORIZED")
        available = binding["lifecycle_status"] == "ACTIVE" and authorized and not blockers
        return {
            "binding_ref": binding["entity_id"],
            "requirement_ref": data.get("requirementRef") or binding.get("capability_ref"),
            "name": data.get("name") or "未命名能力",
            "status": "AVAILABLE" if available else ("NEEDS_AUTH" if not authorized else "UNAVAILABLE"),
            "authorization_status": data.get("authorizationStatus") or "UNKNOWN",
            "verification_status": binding.get("verification_status") or "UNKNOWN",
            "supply": {
                key: review.get(key) for key in ("source", "capabilityType", "capabilityId")
            } if review else None,
            "blockers": blockers,
        }

    def _employee(
        self,
        employee: dict[str, Any],
        roles: list[dict[str, Any]],
        bindings: list[dict[str, Any]],
        work_items: list[dict[str, Any]],
        links: list[dict[str, Any]],
    ) -> dict[str, Any]:
        data = employee["data"]
        role_ref = data.get("roleSlotRef") or next((
            link["target_id"] for link in links
            if link["source_id"] == employee["entity_id"] and link["relation"] == "PROPOSED_FOR"
        ), None)
        role = next((item for item in roles if item["entity_id"] == role_ref), None)
        held = [item for item in work_items if item["responsibility_holder_ref"] == employee["entity_id"]]
        executing = [item for item in work_items if item["current_executor_ref"] == employee["entity_id"]]
        blocked = [item for item in held if item["work_status"] in {"waiting", "needs_ceo", "failed"}]
        if executing:
            ui_status = {"code": "working", "label": f"工作中 · {executing[-1]['activity'] or '正在处理'}"}
        elif blocked:
            ui_status = {"code": "blocked", "label": f"阻塞 · {blocked[-1]['activity'] or '等待处理'}"}
        else:
            ui_status = {"code": "idle", "label": "空闲"}
        requirements = set((role or {}).get("data", {}).get("capabilityRefs") or [])
        capability_items = [
            self._binding(item) for item in bindings
            if item["data"].get("requirementRef") in requirements
        ]
        access = next((
            item["computer_access"] for item in reversed(executing or held) if item["computer_access"]
        ), None) or {
            "requested_intent": "UNKNOWN", "configured_state": "UNKNOWN",
            "effective_state": "UNKNOWN", "verification_state": "UNVERIFIED",
        }
        return {
            "employee_ref": employee["entity_id"],
            "company_employee_ref": data.get("companyEmployeeRef") or employee["entity_id"],
            "identity_status": (
                "VERIFIED_EXPLICIT_BRIDGE" if data.get("companyEmployeeRef") else "EXACT_ID_FALLBACK"
            ),
            "identity_bridge": data.get("identityBridge") if data.get("companyEmployeeRef") else None,
            "name": data.get("name") or "未命名员工",
            "role_slot_ref": role_ref,
            "role": (role or {}).get("data", {}).get("name") or data.get("responsibility") or "未设置岗位",
            "responsibility": (role or {}).get("data", {}).get("responsibility") or data.get("responsibility") or "",
            "reporting_to_ref": data.get("reportingTo") or employee.get("parent_id"),
            "runtime_status": employee["lifecycle_status"],
            "presence_state": employee.get("presence_state"),
            "ui_status": ui_status,
            "current_responsibilities": held,
            "current_execution": executing[-1] if executing else None,
            "recent_result_refs": list(dict.fromkeys(
                ref for item in held for ref in item["result_refs"]
            )),
            "composer": {
                "capabilities": capability_items,
                "model_backed": any(
                    item.get("supply", {}).get("capabilityType") == "model"
                    for item in capability_items if item.get("supply")
                ),
                "agent_backed": any(
                    item.get("supply", {}).get("capabilityType") == "agent"
                    for item in capability_items if item.get("supply")
                ),
                "computer_access": access,
            },
        }

    @staticmethod
    def _work_items(
        entities: list[dict[str, Any]], roles: list[dict[str, Any]], links: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        role_to_employee = {
            role["entity_id"]: role["data"].get("assignedEmployeeRef") for role in roles
        }
        role_to_employee.update({
            link["target_id"]: link["source_id"] for link in links if link["relation"] == "PROPOSED_FOR"
        })
        items = []
        excluded = {"AI_EMPLOYEE", "ROLE_SLOT", "CAPABILITY_BINDING", "EVIDENCE", "OUTCOME"}
        for entity in entities:
            if entity["entity_type"] in excluded:
                continue
            data = entity["data"]
            context = data.get("workContext") if isinstance(data.get("workContext"), dict) else {}
            role_ref = context.get("responsibilityRoleSlotRef") or data.get("responsibilityRef")
            holder_ref = context.get("responsibilityEmployeeRef") or role_to_employee.get(role_ref)
            executor_ref = None if entity["lifecycle_status"] in {"COMPLETED", "CANCELLED", "ARCHIVED"} else context.get("currentExecutorRef")
            system_activity = context.get("systemActivity") if isinstance(context.get("systemActivity"), dict) else None
            if not (holder_ref or executor_ref or system_activity or context):
                continue
            items.append({
                "object_ref": entity["entity_id"],
                "object_type": entity["entity_type"],
                "object_owner_ref": context.get("objectOwnerRef") or entity.get("owner_ref") or None,
                "responsibility_holder_ref": holder_ref,
                "responsibility_role_slot_ref": role_ref,
                "current_executor_ref": executor_ref,
                "activity": context.get("activity") or "",
                "work_status": canonical_work_status(entity).lower() if entity["entity_type"] == "WORK" else context.get("status") or "idle",
                "system_activity": system_activity,
                "result_refs": _refs(data),
                "computer_access": data.get("computerAccess") if isinstance(data.get("computerAccess"), dict) else None,
                "updated_at": entity.get("updated_at"),
            })
        return items

    def _projects(self, company_id: str, refs: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        if not refs:
            return [], []
        placeholders = ",".join("?" for _ in refs)
        with self.db.connect() as connection:
            rows = connection.execute(
                f"select project_id, department_id, name, goal, status from projects "
                f"where tenant_id = ? and company_id = ? and project_id in ({placeholders})",
                [self.tenant_id, company_id, *refs],
            ).fetchall()
            department_refs = list(dict.fromkeys(row["department_id"] for row in rows if row["department_id"]))
            departments = []
            if department_refs:
                department_placeholders = ",".join("?" for _ in department_refs)
                departments = connection.execute(
                    f"select id as department_id, name, department_type, status from department_instances "
                    f"where tenant_id = ? and company_id = ? and id in ({department_placeholders})",
                    [self.tenant_id, company_id, *department_refs],
                ).fetchall()
        return [dict(row) for row in rows], [dict(row) for row in departments]

    def _employee_organization(self, company_id: str, employee_refs: list[str]) -> dict[str, dict[str, Any]]:
        if not employee_refs:
            return {}
        placeholders = ",".join("?" for _ in employee_refs)
        with self.db.connect() as connection:
            employees = connection.execute(
                f"select id, name, role, department_id, status from employee_instances "
                f"where tenant_id = ? and company_id = ? and deleted_at is null "
                f"and id in ({placeholders})",
                [self.tenant_id, company_id, *employee_refs],
            ).fetchall()
            affiliations = connection.execute(
                f"select employee_id, department_id, project_id from employee_affiliations "
                f"where tenant_id = ? and employee_id in ({placeholders}) order by created_at, id",
                [self.tenant_id, *employee_refs],
            ).fetchall()
            department_refs = list(dict.fromkeys(
                ref for row in [*employees, *affiliations]
                if (ref := row["department_id"])
            ))
            project_refs = list(dict.fromkeys(row["project_id"] for row in affiliations if row["project_id"]))
            departments = {}
            if department_refs:
                marks = ",".join("?" for _ in department_refs)
                departments = {
                    row["id"]: dict(row) for row in connection.execute(
                        f"select id, name, department_type, status from department_instances "
                        f"where tenant_id = ? and company_id = ? and deleted_at is null and id in ({marks})",
                        [self.tenant_id, company_id, *department_refs],
                    ).fetchall()
                }
            projects = {}
            if project_refs:
                marks = ",".join("?" for _ in project_refs)
                projects = {
                    row["project_id"]: dict(row) for row in connection.execute(
                        f"select project_id, name, goal, status from projects where tenant_id = ? "
                        f"and company_id = ? and project_id in ({marks})",
                        [self.tenant_id, company_id, *project_refs],
                    ).fetchall()
                }
        affiliations_by_employee: dict[str, list[dict[str, Any]]] = {}
        for row in affiliations:
            affiliations_by_employee.setdefault(row["employee_id"], []).append({
                "department": departments.get(row["department_id"]),
                "project": projects.get(row["project_id"]),
            })
        return {
            row["id"]: {
                "identity_status": "EXACT_ID_MATCH",
                "name": row["name"],
                "role": row["role"],
                "status": row["status"],
                "primary_department": departments.get(row["department_id"]),
                "affiliations": affiliations_by_employee.get(row["id"], []),
            }
            for row in employees
        }

    def _result(
        self, company_id: str, workspace_id: str | None, reference_id: str, *, include_content: bool, scope=None, connection=None,
    ) -> dict[str, Any] | None:
        with (nullcontext(connection) if connection is not None else self.db.connect()) as connection:
            if reference_id.startswith("task:"):
                task_id = reference_id.removeprefix("task:")
                task = connection.execute(
                    "select * from tasks where tenant_id=? and company_id=? and workspace_id is ? and task_id=?",
                    (self.tenant_id, company_id, workspace_id, task_id),
                ).fetchone()
                if task is None:
                    return None
                task_item = dict(task)
                artifacts = connection.execute(
                    "select artifact_id, title, artifact_type, status, source_ref, content_sha256, "
                    "created_at, updated_at from artifacts where tenant_id=? and task_id=? order by created_at",
                    (self.tenant_id, task_id),
                ).fetchall()
                execution = None
                title = "工作结果"
                if task_item.get("work_ref"):
                    work = connection.execute(
                        "select data_json, parent_id from runtime_entities where tenant_id=? and company_id=? "
                        "and workspace_id is ? and entity_id=? and entity_type='WORK'",
                        (self.tenant_id, company_id, workspace_id, task_item["work_ref"]),
                    ).fetchone()
                    routing = (_json(work["data_json"]).get("responsibilityRouting") or {}) if work else {}
                    if work:
                        cycle = connection.execute(
                            "select data_json from runtime_entities where tenant_id=? and company_id=? "
                            "and workspace_id is ? and entity_id=? and entity_type='CYCLE'",
                            (self.tenant_id, company_id, workspace_id, work["parent_id"]),
                        ).fetchone()
                        contract = (_json(cycle["data_json"]).get("contract") or {}) if cycle else {}
                        title = str(contract.get("problem") or _json(work["data_json"]).get("goal") or title)[:120]
                    execution = next((
                        item for item in (routing.get("executions") or {}).values()
                        if item.get("resultRef") == reference_id or item.get("taskRef") == task_id
                    ), None)
                    if execution and execution.get("humanInputSource") is True and execution.get("taskRef") == task_id:
                        return None
                provenance = (execution or {}).get("provenance") or {}
                return {
                    "reference_id": reference_id,
                    "kind": "RESULT",
                    "status": task_item["status"],
                    "verification_status": provenance.get("verification_status") or "UNVERIFIED",
                    "title": title,
                    "summary": (execution or {}).get("resultSummary") or str(task_item.get("output") or "")[:500],
                    "content": task_item.get("output") if include_content else None,
                    "owner_ref": task_item.get("employee_id") or None,
                    "source_work_ref": task_item.get("work_ref") or None,
                    "execution_ref": task_item.get("execution_ref") or None,
                    "execution_provenance": provenance or None,
                    "artifact_refs": [row["artifact_id"] for row in artifacts],
                    "artifacts": [dict(row) for row in artifacts],
                    "created_at": task_item["created_at"],
                    "updated_at": task_item["updated_at"],
                }
            entity = connection.execute(
                "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id is ? "
                "and entity_id = ? and entity_type in ('EVIDENCE','OUTCOME')",
                (self.tenant_id, company_id, workspace_id, reference_id),
            ).fetchone()
            if entity:
                item = self._entity(entity)
                parent = connection.execute(
                    "select data_json from runtime_entities where tenant_id=? and company_id=? "
                    "and workspace_id is ? and entity_id=?",
                    (self.tenant_id, company_id, workspace_id, item.get("parent_id") or ""),
                ).fetchone()
                parent_data = _json(parent["data_json"]) if parent else {}
                review = parent_data.get("artifactReview") if isinstance(parent_data.get("artifactReview"), dict) else {}
                execution_binding = (
                    review.get("executionBinding")
                    if isinstance(review.get("executionBinding"), dict)
                    else parent_data.get("executionBinding")
                ) or {}
                return {
                    "reference_id": reference_id,
                    "kind": item["entity_type"],
                    "status": item["lifecycle_status"],
                    "verification_status": item["verification_status"],
                    "evidence_condition": item["evidence_condition"],
                    "owner_ref": item.get("owner_ref") or None,
                    "execution_provenance": execution_binding.get("callbackProvenance"),
                    "summary": item["data"].get("summary") or "",
                    "data": item["data"] if include_content else None,
                    "created_at": item["created_at"],
                    "updated_at": item["updated_at"],
                }
            referenced = connection.execute(
                "select data_json from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? and ?=0",
                (self.tenant_id, company_id, workspace_id, int(scope is not None)),
            ).fetchall()
            referenced_data = [_json(row["data_json"]) for row in referenced]
            if scope is None and reference_id not in _refs(referenced_data):
                return None
            execution_provenance = None
            for data in referenced_data:
                review = data.get("artifactReview") if isinstance(data.get("artifactReview"), dict) else {}
                for binding in (data.get("executionBinding"), review.get("executionBinding")):
                    if isinstance(binding, dict) and binding.get("callbackProvenance"):
                        execution_provenance = binding["callbackProvenance"]
                        break
                if execution_provenance:
                    break
            artifact = connection.execute(
                "select a.*, t.company_id, t.employee_id from artifacts a join tasks t on t.tenant_id = a.tenant_id "
                "and t.task_id = a.task_id where a.tenant_id = ? and a.artifact_id = ? and t.company_id = ?",
                (self.tenant_id, reference_id, company_id),
            ).fetchone()
        if artifact is None:
            return None
        item = dict(artifact)
        return {
            "reference_id": reference_id,
            "kind": "ARTIFACT",
            "status": item["status"],
            "verification_status": "UNKNOWN",
            "title": item["title"],
            "artifact_type": item["artifact_type"],
            "source_ref": item["source_ref"],
            "content_sha256": item["content_sha256"],
            "company_employee_ref": item.get("employee_id") or None,
            "task_ref": item.get("task_id"),
            "execution_provenance": execution_provenance,
            "content": item["content"] if include_content else None,
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
        }
