"""Minimal General Workspace command adapter over accepted Runtime primitives."""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from typing import Any

from ..database import Database
from ..agent_adapter import agent_stop_serialized
from ..employee_execution_identity import EmployeeExecutionIdentity
from ..employee_templates import EmployeeTemplateContract
from ..model_preferences import TenantModelPreferenceResolver
from ..tenant_context import TenantContext
from ..resource_scope_policy import ResourceScopePolicy
from .child_work import CanonicalChildWorkRuntime, WORK_TRANSITIONS
from .foundation import RuntimeFoundation, RuntimeScopeError
from .responsibility_routing import ResponsibilityRoutingRuntime


class GeneralWorkspaceGap(ValueError):
    def __init__(self, code: str, reason: str, next_action: str):
        super().__init__(reason)
        self.payload = {
            "status": "NEEDS_DECISION",
            "code": code,
            "reason": reason,
            "owner": "CEO",
            "next_action": next_action,
        }


class GeneralHumanAuthorityGap(RuntimeScopeError):
    pass


class GeneralWorkspaceDelivery:
    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.routing = ResponsibilityRoutingRuntime(database)
        self.child_work = CanonicalChildWorkRuntime(database)
        self.identities = EmployeeExecutionIdentity(database)
        self.employees = EmployeeTemplateContract(database)
        self.models = TenantModelPreferenceResolver(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _available_execution_binding(self, company_id: str, workspace_id: str, employee_ref: str) -> bool:
        try:
            identity = self.identities.resolve(
                company_id=company_id,
                workspace_id=workspace_id,
                runtime_employee_ref=employee_ref,
            )
        except (KeyError, RuntimeScopeError):
            return False
        with self.db.connect() as connection:
            bridge_ref = str((identity.get("bridge") or {}).get("verifiedByEmployeeCapabilityBindingRef") or "")
            if bridge_ref:
                bindings = connection.execute(
                    "select capability_source, capability_type, capability_id from employee_capability_bindings "
                    "where tenant_id=? and employee_id=? and id=? and enabled=1",
                    (self.tenant_id, identity["company_employee_ref"], bridge_ref),
                ).fetchall()
            else:
                bindings = connection.execute(
                    "select capability_source, capability_type, capability_id from employee_capability_bindings "
                    "where tenant_id=? and employee_id=? and enabled=1",
                    (self.tenant_id, identity["company_employee_ref"]),
                ).fetchall()
            if len(bindings) != 1:
                return False
            binding = bindings[0]
            if binding["capability_source"] == "tenant_private":
                capability = connection.execute(
                    "select status from tenant_private_capabilities where tenant_id=? and capability_type=? and capability_id=?",
                    (self.tenant_id, binding["capability_type"], binding["capability_id"]),
                ).fetchone()
            elif binding["capability_source"] == "official":
                capability = connection.execute(
                    "select status from official_models where model_key=?",
                    (binding["capability_id"],),
                ).fetchone()
            else:
                capability = None
        return capability is not None and capability["status"] == "active"

    def assignment_candidates(self, *, company_id: str, workspace_id: str) -> dict[str, Any]:
        """List real Company Employees and the current default-model eligibility."""
        self.foundation._require_workspace(workspace_id, company_id)
        preference = self.models.read_current().get("preference")
        assigned = {
            str(item["data"].get("employeeRef") or "")
            for item in self.foundation.list(
                "RESPONSIBILITY_ASSIGNMENT", company_id=company_id, workspace_id=workspace_id,
            )
        }
        with self.db.connect() as connection:
            rows = connection.execute(
                "select id, name, role, status from employee_instances where tenant_id=? and company_id=? "
                "and enabled=1 and deleted_at is null order by created_at, id",
                (self.tenant_id, company_id),
            ).fetchall()
        return {
            "employees": [
                {
                    "employee_id": row["id"],
                    "name": row["name"],
                    "role": row["role"],
                    "status": row["status"],
                    "assigned": row["id"] in assigned,
                    "capability_status": "AVAILABLE" if preference else "NO_VERIFIED_DEFAULT_MODEL",
                    "default_model": None if preference is None else {
                        "model_key": preference["model_key"],
                        "model_name": preference["model_name"],
                        "source": preference["source"],
                    },
                }
                for row in rows
            ],
        }

    def assign_employee(
        self, *, company_id: str, workspace_id: str, employee_id: str, responsibility: str,
    ) -> dict[str, Any]:
        """Attach one recruited Employee to the existing General operating primitives."""
        self.foundation._require_workspace(workspace_id, company_id)
        responsibility = responsibility.strip()
        if not responsibility:
            raise ValueError("Responsibility is required")
        existing_workflows = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id,
            )
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == workspace_id
            and not str(item["data"].get("workflowKey") or "").startswith("meeting:")
        ]
        if existing_workflows:
            if len(existing_workflows) == 1 and any(
                item.get("employeeRef") == employee_id
                for item in existing_workflows[0]["data"].get("assignments") or []
            ):
                return {"created": False, "workflow": existing_workflows[0]}
            raise GeneralWorkspaceGap(
                "RESPONSIBILITY_AMBIGUOUS", "当前工作空间已有另一项团队责任安排", "先确认现有团队责任",
            )
        employee = self.employees.get_employee_instance(employee_id)
        if employee is None or employee["company_id"] != company_id or not employee["enabled"]:
            raise RuntimeScopeError("Employee is outside the current Company")
        preference = self.models.read_current().get("preference")
        if preference is None:
            raise GeneralWorkspaceGap(
                "CAPABILITY_UNAVAILABLE", "当前没有已验证的默认模型", "连接并验证一个模型后返回当前工作空间",
            )
        bindings = self.employees.list_employee_capability_bindings(employee_id)["bindings"]
        binding = next((
            item for item in bindings
            if item["enabled"]
            and item["capability_source"] == preference["source"]
            and item["capability_type"] == "model"
            and item["capability_id"] == preference["model_key"]
        ), None)
        if binding is None:
            updated = self.employees.set_employee_capability_bindings(employee_id, [
                *bindings,
                {
                    "capability_source": preference["source"],
                    "capability_type": "model",
                    "capability_id": preference["model_key"],
                    "priority": 1,
                    "enabled": True,
                },
            ])
            binding = next(
                item for item in updated["bindings"]
                if item["capability_source"] == preference["source"]
                and item["capability_type"] == "model"
                and item["capability_id"] == preference["model_key"]
            )
        suffix = hashlib.sha256(f"{workspace_id}:{employee_id}".encode()).hexdigest()[:16]
        try:
            runtime_employee = self.foundation.get(employee_id)
            if (runtime_employee["entity_type"] != "AI_EMPLOYEE"
                or runtime_employee["company_id"] != company_id
                or runtime_employee["workspace_id"] not in (None, workspace_id)):
                raise GeneralWorkspaceGap(
                    "EMPLOYEE_SCOPE_CONFLICT", "该员工已在另一运行范围承担责任", "先回到原工作空间确认责任",
                )
        except KeyError:
            runtime_employee = self.foundation.create(
                "AI_EMPLOYEE", entity_id=employee_id, company_id=company_id,
                lifecycle_status="AVAILABLE",
                data={"name": employee["name"], "role": employee["role"], "companyEmployeeRef": employee_id},
            )
        role_id = f"general-role-{suffix}"
        try:
            role = self.foundation.get(role_id)
        except KeyError:
            role = self.foundation.create(
                "ROLE_SLOT", entity_id=role_id, company_id=company_id, workspace_id=workspace_id,
                lifecycle_status="ASSIGNED",
                data={"name": employee["role"], "role": employee["role"], "responsibility": responsibility},
            )
        self.identities.bind(
            company_id=company_id,
            workspace_id=workspace_id,
            runtime_employee_ref=runtime_employee["entity_id"],
            company_employee_ref=employee_id,
            employee_capability_binding_ref=binding["id"],
        )
        assignment_id = f"general-assignment-{suffix}"
        try:
            assignment = self.foundation.get(assignment_id)
        except KeyError:
            assignment = self.routing.create_assignment(
                assignment_id=assignment_id,
                company_id=company_id,
                workspace_id=workspace_id,
                scope_type="WORKSPACE",
                scope_ref=workspace_id,
                role_ref=role["entity_id"],
                employee_ref=runtime_employee["entity_id"],
                responsibility_key="general-primary",
                responsibility=responsibility,
                output_contract={"requiresResult": True, "resultType": "general-business-result"},
                is_leader=True,
            )
        workflow = self.routing.publish_workflow(
            company_id=company_id,
            workspace_id=workspace_id,
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workflow_key="general-operating",
            assignment_refs=[assignment["entity_id"]],
            default_flow=["general-primary"],
        )
        self.employees.update_employee_instance(employee_id, {"status": "assigned"})
        return {"created": True, "workflow": workflow, "assignment": assignment}

    def materialize_team(self, *, company_id: str, workspace_id: str) -> dict[str, Any]:
        """Publish already-authorized team truth; never infer or create a role or employee."""
        self.foundation._require_workspace(workspace_id, company_id)
        workflows = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id,
            )
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == workspace_id
            and not str(item["data"].get("workflowKey") or "").startswith("meeting:")
        ]
        if len(workflows) == 1:
            return {"status": "READY", "workflow": workflows[0], "created": False}
        if len(workflows) > 1:
            raise GeneralWorkspaceGap(
                "RESPONSIBILITY_AMBIGUOUS", "存在多个团队责任安排，无法自动选择", "由 CEO 确认唯一团队责任安排",
            )
        assignments = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_ASSIGNMENT", company_id=company_id, workspace_id=workspace_id,
            )
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == workspace_id
        ]
        leaders = [item for item in assignments if item["data"].get("isLeader")]
        operators = [item for item in assignments if not item["data"].get("isLeader")]
        if len(leaders) != 1 or not operators:
            raise GeneralWorkspaceGap(
                "TEAM_TRUTH_INCOMPLETE",
                "当前业务还没有可证明的负责人和执行责任",
                "确认一位业务负责人、至少一项执行责任及对应员工",
            )
        if not all(
            self._available_execution_binding(company_id, workspace_id, item["data"]["employeeRef"])
            for item in assignments
        ):
            raise GeneralWorkspaceGap(
                "CAPABILITY_UNAVAILABLE",
                "当前团队中仍有员工缺少唯一且可用的执行能力",
                "为对应员工配置可用能力后返回当前工作空间",
            )
        workflow = self.routing.publish_workflow(
            company_id=company_id,
            workspace_id=workspace_id,
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workflow_key="general-operating",
            assignment_refs=[item["entity_id"] for item in assignments],
            default_flow=[item["data"]["responsibilityKey"] for item in operators],
        )
        return {"status": "READY", "workflow": workflow, "created": True}

    @staticmethod
    def _decision_fact(value: Any) -> dict[str, str]:
        if not isinstance(value, dict):
            raise ValueError("Decision fact requires value and provenance")
        text = str(value.get("value") or "").strip()
        provenance = str(value.get("provenance") or "").upper()
        if not text or provenance not in {"FACT", "POLICY", "EVIDENCE", "EST", "UNK"}:
            raise ValueError("Decision fact requires truthful provenance")
        return {"value": text[:2000], "provenance": provenance}

    def request_decision(
        self, *, company_id: str, workspace_id: str, work_ref: str, packet: dict[str, Any],
    ) -> dict[str, Any]:
        self._require_general_work(company_id, workspace_id, work_ref)
        complexity = str(packet.get("complexity") or "").upper()
        decision_key = str(packet.get("decisionKey") or "").strip()
        event = str(packet.get("event") or "").strip()
        cannot_decide = str(packet.get("cannotDecideReason") or "").strip()
        choice_prompt = str(packet.get("ceoChoicePrompt") or "").strip()
        continuation = str(packet.get("continuationPlan") or "").strip()
        options = packet.get("options")
        if complexity not in {"LOW_RISK", "HIGH_RISK"} or not all(
            (decision_key, event, cannot_decide, choice_prompt, continuation)
        ):
            raise ValueError("Decision Packet is incomplete")
        if not isinstance(options, list) or not 2 <= len(options) <= 4:
            raise ValueError("Decision Packet requires two to four options")
        normalized, option_ids = [], set()
        for option in options:
            option_id = str(option.get("optionId") or "").strip() if isinstance(option, dict) else ""
            label = str(option.get("label") or "").strip() if isinstance(option, dict) else ""
            if not option_id or option_id in option_ids or not label:
                raise ValueError("Decision option is incomplete")
            option_ids.add(option_id)
            normalized.append({
                "optionId": option_id,
                "label": label[:240],
                "impact": self._decision_fact(option.get("impact")),
                "risk": self._decision_fact(option.get("risk")),
                "cost": self._decision_fact(option.get("cost")),
            })
        recommendation = packet.get("recommendation")
        recommended_id = str(recommendation.get("optionId") or "").strip() if isinstance(recommendation, dict) else ""
        recommendation_provenance = str(recommendation.get("provenance") or "").upper() if isinstance(recommendation, dict) else ""
        if recommended_id not in option_ids or recommendation_provenance not in {"FACT", "POLICY", "EVIDENCE", "EST", "UNK"}:
            raise ValueError("Decision recommendation is invalid")
        recommendation_reason = self._decision_fact(packet.get("recommendationReason"))

        routed = self.routing.route(
            work_ref,
            signal="DECISION_GATE",
            result_refs=list(packet.get("resultRefs") or []),
            artifact_refs=list(packet.get("artifactRefs") or []),
            evidence_refs=list(packet.get("evidenceRefs") or []),
            problem=event,
        )
        decision = routed["decision"]
        existing_key = str(decision["data"].get("decisionKey") or "")
        if existing_key and existing_key != decision_key:
            raise ValueError("Work already has another Decision Packet")
        if not existing_key:
            data = decision["data"] | {
                "kind": "GENERAL_WORK_DECISION",
                "decisionKey": decision_key,
                "complexity": complexity,
                "layer0Actions": (
                    ["VIEW_OPTIONS", "DEFER"] if complexity == "HIGH_RISK"
                    else ["FOLLOW_RECOMMENDATION", "VIEW_OPTIONS", "DEFER"]
                ),
                "event": event[:2000],
                "cannotDecideReason": cannot_decide[:2000],
                "options": normalized,
                "recommendation": {"optionId": recommended_id, "provenance": recommendation_provenance},
                "recommendationReason": recommendation_reason,
                "ceoChoicePrompt": choice_prompt[:1000],
                "continuationPlan": continuation[:2000],
                "createdAt": self._now(),
            }
            with self.db.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? "
                    "and entity_type='DECISION_PACKET' and lifecycle_status='WAITING_CEO'",
                    (json.dumps(data, ensure_ascii=False), self._now(), self.tenant_id, decision["entity_id"]),
                )
            decision = self.foundation.get(decision["entity_id"])
        return {"work": self.foundation.get(work_ref), "decision": decision}

    def review_decision(self, *, company_id: str, workspace_id: str, work_ref: str) -> dict[str, Any]:
        work = self._require_general_work(company_id, workspace_id, work_ref)
        decision = self.foundation.get(work["data"]["responsibilityRouting"]["decisionPacketRef"])
        if decision["lifecycle_status"] != "WAITING_CEO":
            if decision["data"].get("layer1ReviewedAt"):
                return {"work": work, "decision": decision}
            raise ValueError("Decision Package is not available for review")
        if not decision["data"].get("layer1ReviewedAt"):
            data = decision["data"] | {"layer1ReviewedAt": self._now()}
            with self.db.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=? "
                    "and lifecycle_status='WAITING_CEO'",
                    (json.dumps(data, ensure_ascii=False), self._now(), self.tenant_id, decision["entity_id"]),
                )
            decision = self.foundation.get(decision["entity_id"])
        return {"work": work, "decision": decision}

    def choose_decision(
        self, *, company_id: str, workspace_id: str, work_ref: str,
        choice: str, reason: str, next_check_at: str | None = None,
    ) -> dict[str, Any]:
        work = self._require_general_work(company_id, workspace_id, work_ref)
        decision = self.foundation.get(work["data"]["responsibilityRouting"]["decisionPacketRef"])
        choice, reason = choice.strip(), reason.strip()
        if not choice or not reason:
            raise ValueError("Decision choice and reason are required")
        if decision["lifecycle_status"] == "APPLIED":
            if decision["data"].get("choice") == choice:
                return {"work": work, "decision": decision}
            raise ValueError("Decision was already applied with another choice")
        if choice == "DEFER":
            data = decision["data"] | {"deferredAt": self._now(), "deferReason": reason[:2000], "nextCheckAt": next_check_at}
            with self.db.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, next_check_at=?, updated_at=? where tenant_id=? "
                    "and entity_id=? and lifecycle_status='WAITING_CEO'",
                    (json.dumps(data, ensure_ascii=False), next_check_at, self._now(), self.tenant_id, decision["entity_id"]),
                )
            return {"work": work, "decision": self.foundation.get(decision["entity_id"])}
        if choice not in {item.get("optionId") for item in decision["data"].get("options") or []}:
            raise ValueError("Decision choice is not available")
        if decision["data"].get("complexity") == "HIGH_RISK" and not decision["data"].get("layer1ReviewedAt"):
            raise ValueError("High-risk Decision requires review before choosing")
        return self.routing.apply_decision(work_ref, choice=choice, reason=reason)

    def _resolve_assignment(self, company_id: str, workspace_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as connection:
            workspace = connection.execute(
                "select blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
        blueprint = json.loads(workspace["blueprint_json"] or "{}")
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
        keys = {str(item["data"].get("workflowKey") or "") for item in workflows}
        if len(keys) != 1:
            raise GeneralWorkspaceGap(
                "RESPONSIBILITY_UNRESOLVED",
                "当前业务尚未形成唯一的团队责任安排",
                "确认负责岗位与员工",
            )
        workflow = max(workflows, key=lambda item: int(item["data"].get("version") or 0))
        first_key = (workflow["data"].get("defaultFlow") or [None])[0]
        assignment = next(
            (item for item in workflow["data"].get("assignments") or [] if item.get("responsibilityKey") == first_key),
            None,
        )
        if assignment is None:
            raise GeneralWorkspaceGap("RESPONSIBILITY_UNRESOLVED", "团队责任安排不完整", "重新确认团队责任")
        try:
            identity = self.identities.resolve(
                company_id=company_id,
                workspace_id=workspace_id,
                runtime_employee_ref=assignment["employeeRef"],
            )
        except (KeyError, RuntimeScopeError) as error:
            raise GeneralWorkspaceGap("NO_ELIGIBLE_EMPLOYEE", str(error), "选择可执行的员工") from error
        with self.db.connect() as connection:
            bridge_ref = str((identity.get("bridge") or {}).get("verifiedByEmployeeCapabilityBindingRef") or "")
            bindings = connection.execute(
                "select capability_source, capability_type, capability_id from employee_capability_bindings "
                "where tenant_id=? and employee_id=? and id=? and enabled=1",
                (self.tenant_id, identity["company_employee_ref"], bridge_ref),
            ).fetchall() if bridge_ref else connection.execute(
                "select capability_source, capability_type, capability_id from employee_capability_bindings "
                "where tenant_id=? and employee_id=? and enabled=1",
                (self.tenant_id, identity["company_employee_ref"]),
            ).fetchall()
            available = False
            if len(bindings) == 1:
                binding = bindings[0]
                if binding["capability_source"] == "tenant_private":
                    capability = connection.execute(
                        "select status from tenant_private_capabilities where tenant_id=? and capability_type=? and capability_id=?",
                        (self.tenant_id, binding["capability_type"], binding["capability_id"]),
                    ).fetchone()
                    available = capability is not None and capability["status"] == "active"
                elif binding["capability_source"] == "official":
                    capability = connection.execute(
                        "select status from official_models where model_key=?",
                        (binding["capability_id"],),
                    ).fetchone()
                    available = capability is not None and capability["status"] == "active"
        if not available:
            raise GeneralWorkspaceGap(
                "CAPABILITY_UNAVAILABLE",
                "当前负责员工没有唯一且可用的执行能力",
                "配置或选择可用能力后返回当前工作空间",
            )
        return workflow, assignment

    def _require_general_work(self, company_id: str, workspace_id: str, work_ref: str) -> dict[str, Any]:
        self.foundation._require_workspace(workspace_id, company_id)
        work = self.foundation.get(work_ref)
        if work["entity_type"] != "WORK" or work["company_id"] != company_id or work["workspace_id"] != workspace_id:
            raise RuntimeScopeError("Work is outside the current General Workspace")
        with self.db.connect() as connection:
            row = connection.execute(
                "select blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
        if str(json.loads(row["blueprint_json"] or "{}").get("productForm") or "").upper() != "GENERIC":
            raise RuntimeScopeError("Workspace is not a General Workspace")
        return work

    def _human_work(self, company_id: str, workspace_id: str, work_ref: str) -> dict[str, Any]:
        identity = TenantContext.current_identity()
        if identity.get("company_id") != company_id or str(identity.get("role") or "").lower() not in {"ceo", "owner"}:
            raise GeneralHumanAuthorityGap("Current Company owner is required for Human Input")
        work = self._require_general_work(company_id, workspace_id, work_ref)
        if work["data"].get("kind") != "CANONICAL_CHILD_WORK":
            raise RuntimeScopeError("Human Input requires the canonical original Work")
        return work

    def report_human_input(self, *, company_id: str, workspace_id: str, work_ref: str,
                           request_id: str, revision: int, submission_id: str, kind: str,
                           local_text: str = "", reference_refs: list[str] | None = None,
                           manual_source: str = "") -> dict[str, Any]:
        self._human_work(company_id, workspace_id, work_ref)
        return self.routing.report_human_input(
            company_id, workspace_id, work_ref, request_id=request_id, revision=revision,
            submission_id=submission_id, kind=kind, local_text=local_text,
            reference_refs=reference_refs, manual_source=manual_source,
            actor=TenantContext.current_identity().get("subject_id") or "CEO",
        )

    def review_human_input(self, *, company_id: str, workspace_id: str, work_ref: str,
                           request_id: str, revision: int) -> dict[str, Any]:
        self._human_work(company_id, workspace_id, work_ref)
        return self.routing.review_human_input(company_id, workspace_id, work_ref,
                                               request_id=request_id, revision=revision)

    def precheck_human_continuation(self, *, company_id: str, workspace_id: str, work_ref: str,
                                    request_id: str, revision: int, submission_id: str) -> dict[str, Any]:
        from .general_execution_limits import work_limits as read_general_limits
        work = self._human_work(company_id, workspace_id, work_ref)
        if read_general_limits(self.db, work_ref):
            raise RuntimeScopeError("Original limited Work has consumed its single execution; continuation needs a new decision")
        routing = work["data"].get("responsibilityRouting") or {}
        request = routing.get("humanInput") or {}
        if (request.get("requestId") != request_id or request.get("revision") != revision
            or request.get("state") != "READY" or request.get("kind") != "LOCAL_INFORMATION"
            or (request.get("report") or {}).get("submissionId") != submission_id):
            raise RuntimeScopeError("Human Input request is not ready at this revision")
        workflow = self.foundation.get(str(routing.get("workflowRef") or ""))
        assignment = next((item for item in workflow["data"].get("assignments") or []
                           if item.get("assignmentRef") == routing.get("currentAssignmentRef")), None)
        if not assignment or assignment.get("employeeRef") != routing.get("responsibilityHolderRef"):
            raise RuntimeScopeError("Current responsibility assignment changed")
        if not self._available_execution_binding(company_id, workspace_id, assignment["employeeRef"]):
            raise GeneralWorkspaceGap("CAPABILITY_UNAVAILABLE", "当前负责员工没有可用执行能力", "配置能力后返回原工作")
        with self.db.connect() as connection:
            scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=self.tenant_id, record=work)
            ResourceScopePolicy.authorize_assignment(connection, tenant_id=self.tenant_id,
                company_id=company_id, assignment_ref=assignment["assignmentRef"],
                employee_ref=assignment["employeeRef"], revision=assignment["assignmentRevision"], scope=scope)
        return work

    def create_work(
        self,
        *,
        company_id: str,
        workspace_id: str,
        problem: str,
        expected_result: str,
        constraints: list[str],
        references: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        workflow, assignment = self._resolve_assignment(company_id, workspace_id)
        contract = {
            "problem": problem.strip(),
            "expectedResult": expected_result.strip(),
            "constraints": list(dict.fromkeys(item.strip() for item in constraints if item.strip())),
            "references": list(dict.fromkeys(item.strip() for item in references if item.strip())),
        }
        created = self.child_work.create_cycle_work(
            company_id=company_id,
            workspace_id=workspace_id,
            assignment_ref=assignment["assignmentRef"],
            release_key=idempotency_key,
            contract=contract,
            input_refs=contract["references"],
        )
        work = self.routing.start_work(
            created["work"]["entity_id"],
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workflow_key=workflow["data"]["workflowKey"],
            initial_responsibility=assignment["responsibilityKey"],
        )
        if created["work"]["lifecycle_status"] == "PLANNED":
            self.child_work.transition_work(work["entity_id"], "READY", actor="SYSTEM", reason="责任与执行能力已确认")
            work = self.child_work.transition_work(work["entity_id"], "ACTIVE", actor="SYSTEM", reason="员工已接手")
        return {"cycle": created["cycle"], "work": self.foundation.get(work["entity_id"])}

    def route_work(
        self, *, company_id: str, workspace_id: str, work_ref: str, signal: str,
        responsibility_key: str | None = None, result_refs: list[str] | None = None,
        artifact_refs: list[str] | None = None, evidence_refs: list[str] | None = None,
        reason: str = "",
    ) -> dict[str, Any]:
        self._require_general_work(company_id, workspace_id, work_ref)
        return self.routing.route(
            work_ref, signal=signal, responsibility_key=responsibility_key,
            result_refs=result_refs, artifact_refs=artifact_refs,
            evidence_refs=evidence_refs, problem=reason,
        )

    @agent_stop_serialized
    def control_work(
        self, *, company_id: str, workspace_id: str, work_ref: str, action: str, reason: str = "",
    ) -> dict[str, Any]:
        """Control one General Work without introducing a second lifecycle authority."""
        work = self._require_general_work(company_id, workspace_id, work_ref)
        action = action.upper()
        status = work["lifecycle_status"]
        target = {"PAUSE": "PAUSED", "CANCEL": "CANCELLED", "ARCHIVE": "ARCHIVED"}.get(action)
        if target and status != target and target not in WORK_TRANSITIONS.get(status, ()):
            raise ValueError("当前工作状态不允许该操作，请重新读取原工作")
        if action not in {"PAUSE", "RESUME", "CANCEL", "ARCHIVE", "RESTORE"}:
            raise ValueError("unsupported Work lifecycle action")
        route = dict(work["data"].get("responsibilityRouting") or {})
        if action == "CANCEL" and route.get("status") not in {"CANCELLED", "COMPLETED"}:
            active = next(
                (item for item in (route.get("executions") or {}).values() if item.get("status") == "RUNNING"),
                None,
            )
            if active and active.get("taskRef"):
                from ..evolution_event_log import EvolutionEventLog
                from ..task_execution_control import TaskExecutionControlService
                TaskExecutionControlService(self.db, EvolutionEventLog(self.db)).cancel(
                    active["taskRef"], reason.strip() or "CEO 停止当前工作",
                )
            self.routing.cancel_work(work_ref, reason=reason.strip() or "CEO 停止当前工作")
        if action == "ARCHIVE" and route.get("status") not in {"COMPLETED", "CANCELLED"}:
            raise ValueError("只有已完成或已停止的工作可以归档")
        controlled = self.child_work.control_work(
            work_ref, action, actor="CEO" if action in {"PAUSE", "CANCEL", "ARCHIVE", "RESTORE"} else "SYSTEM",
            reason=reason.strip() or {"PAUSE": "CEO 暂停当前工作", "RESUME": "CEO 恢复当前工作", "RESTORE": "恢复已归档工作"}.get(action, ""),
        )
        return {"work": self._require_general_work(company_id, workspace_id, work_ref), "duplicate": controlled["duplicate"]}

    def work_usage(self, *, company_id: str, workspace_id: str, work_ref: str) -> dict[str, Any]:
        from ..ai_usage import AIUsageService

        self._require_general_work(company_id, workspace_id, work_ref)
        return {"company_id": company_id, "workspace_id": workspace_id, "work_ref": work_ref,
                "records": AIUsageService(self.db).list_records(
                    company_id=company_id, workspace_id=workspace_id, work_ref=work_ref,
                )}
