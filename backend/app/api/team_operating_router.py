"""Product-language adapter for the accepted responsibility routing runtime."""

from __future__ import annotations

import json
import hashlib
import copy
import re
from types import SimpleNamespace
from typing import Any, Awaitable, Callable, Literal

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictBool
from ..runtime.general_execution_limits import arm as arm_general_limits, work_limits as read_general_limits, command_owner as general_command_owner
from contextlib import nullcontext

from ..database import Database
from ..resource_scope_policy import ResourceScopePolicy
from ..knowledge_service import KnowledgeService
from ..runtime import ResponsibilityRoutingError, ResponsibilityRoutingRuntime, RuntimeFoundation, RuntimeScopeError
from ..runtime.general_workspace_delivery import GeneralWorkspaceDelivery, GeneralWorkspaceGap, GeneralHumanAuthorityGap
from ..runtime.child_work import leader_preferred_binding
from ..tenant_context import TenantContext
from ..agent_adapter import _AGENT_STOP_SPAWN_LOCK


def _verified_origin_projection(work, contract, tenant_id):
    """Return only stable origin identifiers when stored source evidence agrees."""
    unknown = {"status": "UNKNOWN"}
    try:
        assignment = work["data"]["responsibilityAssignmentRef"]
        if "modelSource" in contract:
            snapshot = contract["modelSource"]
            scope = snapshot["scope"]
            source = {"kind": snapshot["kind"], **{key: snapshot.get(key) or scope.get(key) for key in ("book_ref", "chapter_ref", "content_ref", "song_ref")}}
        else:
            source = contract["agentSource"]["input"]
            snapshot = contract["agentSource"]["snapshot"]
        context = snapshot["context"]
        scope = snapshot.get("scope", {})
        kind = source["kind"]
        fields = {"content-growth": ("content_ref",), "music": ("song_ref",),
                  "writing": ("book_ref", "chapter_ref"), "references": ()}.get(kind)
        if fields is None or snapshot["kind"] != kind or not isinstance(assignment, str) or not assignment:
            return unknown
        if any(context.get(key) != value for key, value in {
            "tenant_id": tenant_id, "company_id": work["company_id"],
            "workspace_id": work["workspace_id"], "assignment_ref": assignment}.items()):
            return unknown
        if kind != "references" and any(scope.get(key) != value for key, value in {
            "tenant_id": tenant_id, "company_id": work["company_id"], "workspace_id": work["workspace_id"]}.items()):
            return unknown
        result = {"kind": kind}
        if kind == "references":
            conversation = snapshot.get("conversation_id")
            if not isinstance(conversation, str) or not conversation:
                return unknown
            result["conversation_id"] = conversation
        for field in fields:
            value = source.get(field)
            expected = scope.get(field) if kind == "writing" else snapshot.get(field)
            if not isinstance(value, str) or not value or value != expected:
                return unknown
            result[field] = value
        return {"status": "VERIFIED", "assignment_ref": assignment, "source": result}
    except (KeyError, TypeError, AttributeError):
        return unknown


class LimitedGeneralExecutionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_prompt_bytes: StrictInt = Field(ge=1, le=4096)
    max_output_tokens: StrictInt = Field(ge=1, le=2048)


class ContinueHumanInputIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: StrictInt = Field(ge=1)
    submission_id: str = Field(min_length=1, max_length=128)


class OperatingRoleIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    responsibility_key: str = Field(min_length=1, max_length=96)
    role_name: str = Field(min_length=1, max_length=120)
    employee_ref: str = Field(min_length=1, max_length=128)
    responsibility: str = Field(min_length=1, max_length=1000)
    input_contract: dict[str, Any] = Field(default_factory=dict)
    output_contract: dict[str, Any] = Field(default_factory=dict)
    is_leader: bool = False
    assignment_ref: str | None = Field(default=None, max_length=128)
    role_ref: str | None = Field(default=None, max_length=128)


class PublishOperatingDefinitionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_id: str = Field(min_length=1, max_length=128)
    scope_type: Literal["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"]
    scope_ref: str = Field(min_length=1, max_length=128)
    workspace_id: str | None = Field(default=None, max_length=128)
    workflow_key: str = Field(min_length=1, max_length=128)
    roles: list[OperatingRoleIn] = Field(min_length=1, max_length=32)
    default_flow: list[str] | None = Field(default=None, min_length=1, max_length=32)


class StartOperatingWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_type: Literal["COMPANY", "DEPARTMENT", "BUSINESS", "WORKSPACE"]
    scope_ref: str = Field(min_length=1, max_length=128)
    workflow_key: str = Field(min_length=1, max_length=128)
    initial_responsibility: str | None = Field(default=None, max_length=96)


class RouteOperatingWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal: str = Field(min_length=1, max_length=64)
    responsibility_key: str | None = Field(default=None, max_length=96)
    result_refs: list[str] = Field(default_factory=list, max_length=32)
    artifact_refs: list[str] = Field(default_factory=list, max_length=32)
    evidence_refs: list[str] = Field(default_factory=list, max_length=32)
    problem: str = Field(default="", max_length=2000)
    interaction_key: str | None = Field(default=None, max_length=128)
    bounded_summary: str = Field(default="", max_length=600)


class CompleteConsultIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    response: str = Field(min_length=1, max_length=2000)
    result_refs: list[str] = Field(default_factory=list, max_length=32)
    artifact_refs: list[str] = Field(default_factory=list, max_length=32)
    evidence_refs: list[str] = Field(default_factory=list, max_length=32)


class CancelOperatingWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=1, max_length=2000)


EmployeeExecution = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class AgentCandidateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_ref: str = Field(min_length=1, max_length=128)
    start: StrictInt = Field(ge=0)
    end: StrictInt = Field(gt=0)
    excerpt: str = Field(min_length=1, max_length=200000)
    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    artifact_ref: str | None = Field(default=None, min_length=1, max_length=128)
    artifact_content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    file_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    task_output_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class _WorkCreationConnection:
    """Join canonical nested commands to one request-owned write transaction."""
    def __init__(self, connection):
        self.connection = connection

    def execute(self, statement, *args):
        command = statement.strip().rstrip(";").lower()
        if command in {"begin", "begin immediate"}:
            if not self.connection.in_transaction:
                raise RuntimeScopeError("Work creation transaction is no longer active")
            return self.connection.execute("select 1")
        if command in {"commit", "rollback", "end"}:
            raise RuntimeScopeError("Only the Work request may finish its transaction")
        return self.connection.execute(statement, *args)

    def _finish_forbidden(self, *args, **kwargs):
        raise RuntimeScopeError("Only the Work request may finish its transaction")

    commit = rollback = close = executescript = _finish_forbidden

    def __getattr__(self, name):
        return getattr(self.connection, name)


class PublishAssignedWorkflowIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_id: str = Field(min_length=1, max_length=128)
    workspace_id: str = Field(min_length=1, max_length=128)
    expected_revision: StrictInt = Field(ge=1)
    review_token: str = Field(pattern=r"^[0-9a-f]{64}$")
    confirm: StrictBool


class AssignedWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    problem: str = Field(min_length=1, max_length=1600)
    expected_result: str = Field(min_length=1, max_length=1600)
    request_id: str = Field(min_length=1, max_length=128)
    agent_binding_ref: str | None = Field(default=None, min_length=1, max_length=128)
    model_key: str | None = Field(default=None, min_length=1, max_length=256)
    source: dict[str, Any] | None = None
    browser_hosts: list[str] = Field(default_factory=list, max_length=8)

class PriorResultBasisIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["file", "result"]
    start: StrictInt = Field(ge=0)
    end: StrictInt = Field(gt=0)
    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    task_output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    artifact_ref: str | None = Field(default=None, min_length=1, max_length=128)
    artifact_content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    file_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

class AgentFollowupIn(AssignedWorkIn):
    accepted_task_ref: str = Field(min_length=1, max_length=128)
    accept_result: StrictBool
    prior_result: PriorResultBasisIn


def verify_prior_result(database, company, parent_ref, task_ref, raw_basis):
    """Re-read the explicitly selected prior result without persisting its text."""
    from ..conversation_service import ConversationService
    from ..writing_chapter_service import utf16_slice
    basis = PriorResultBasisIn.model_validate(raw_basis)
    file_values = (basis.artifact_ref, basis.artifact_content_sha256, basis.file_sha256)
    if (basis.mode == "file" and not all(file_values)) or (basis.mode == "result" and any(file_values)):
        raise ValueError("请明确选择原成果文件或无文件结果正文。")
    proof = ConversationService(database).agent_result_proof(
        company, parent_ref, task_ref, require_current_source=False,
        artifact_ref=basis.artifact_ref, for_candidate=True)
    if (proof["text_sha256"] != basis.text_sha256 or proof["task_output_sha256"] != basis.task_output_sha256
            or (basis.mode == "file" and any(proof.get(key) != getattr(basis, key)
                for key in ("artifact_ref", "artifact_content_sha256", "file_sha256")))):
        raise ValueError("原成果文件或结果已变化，请重新核对。")
    selected = utf16_slice(proof["text"], basis.start, basis.end)
    if not selected.strip() or len(selected.encode("utf-8")) > 32768:
        raise ValueError("请选择不超过 32768 字节的非空成果片段。")
    return proof, selected


def verified_prior_for_work(database, work):
    """Return bounded original content only for an exact linked Agent follow-up."""
    data = work.get("data") or {}
    if data.get("leaderRootWorkRef"):
        from ..runtime import RuntimeFoundation
        root = RuntimeFoundation(database).get(data["leaderRootWorkRef"])
        state = root["data"].get("leaderDelegation") or {}
        if (work["entity_id"] not in [*state.get("childWorkRefs", []), state.get("summaryWorkRef")]
                or root["parent_id"] != work["parent_id"] or root["company_id"] != work["company_id"]
                or root["workspace_id"] != work["workspace_id"]):
            raise RuntimeScopeError("Leader child lineage changed")
        return None
    parent_ref = data.get("predecessorWorkRef")
    contract = data.get("followupContract") or {}
    if not contract and not data.get("acceptedPredecessorResultRef"):
        return None
    if not parent_ref or not isinstance(contract, dict) or not contract.get("agentBinding"):
        raise ValueError("续作来源或员工绑定已缺失。")
    from ..runtime import RuntimeFoundation
    parent = RuntimeFoundation(database).get(parent_ref)
    if (parent.get("entity_type") != "WORK" or parent.get("company_id") != work.get("company_id")
            or parent.get("workspace_id") != work.get("workspace_id")):
        raise RuntimeScopeError("续作原工作范围无法核验。")
    accepted = data.get("acceptedPredecessorResultRef")
    if not isinstance(accepted, str) or not accepted.startswith("task:") or not contract.get("priorResult"):
        raise ValueError("续作缺少明确的上次成果依据，请重新核对。")
    task_ref = accepted[5:]
    _, selected = verify_prior_result(database, work["company_id"], parent_ref, task_ref, contract["priorResult"])
    return {"work_ref": parent_ref, "task_ref": task_ref, "content_verification": "UNVERIFIED", "text": selected}


def prior_binding_digest(prior):
    if prior is None:
        return "none"
    return hashlib.sha256(json.dumps(prior, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_team_operating_router(
    database: Database, employee_execution: EmployeeExecution | None = None,
) -> APIRouter:
    router = APIRouter(prefix="/team-operating", tags=["team-operating"])
    foundation = RuntimeFoundation(database)
    routing = ResponsibilityRoutingRuntime(database)
    general_delivery = GeneralWorkspaceDelivery(database)
    knowledge = KnowledgeService(database)

    def assigned_workflow_review(assignment_ref, company_id, workspace_id, connection):
        # The outer transaction owns commit/rollback for all canonical runtime calls.
        scoped_database = SimpleNamespace(connect=lambda: nullcontext(connection))
        scoped = ResponsibilityRoutingRuntime(scoped_database)
        assignment = scoped.foundation.get(assignment_ref)
        require_company(company_id)
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有当前公司的 CEO 可以核对和发布责任流程。")
        if assignment["company_id"] != company_id or assignment["workspace_id"] != workspace_id:
            raise RuntimeScopeError("当前责任不属于指定公司和工作空间。")
        from ..result_attention import ResultAttention
        ResultAttention(scoped_database).actor(company_id)
        scope = ResourceScopePolicy.authorize_assignment(connection, tenant_id=scoped.tenant_id,
            company_id=company_id, assignment_ref=assignment_ref,
            employee_ref=assignment["data"].get("employeeRef"))
        if scope["workspace_id"] != workspace_id:
            raise RuntimeScopeError("当前责任范围与工作空间不一致。")
        workspace = connection.execute(
            "select name,blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
            (scoped.tenant_id, company_id, workspace_id)).fetchone()
        blueprint = json.loads(workspace["blueprint_json"])
        professional = (blueprint.get("businessType") == "PACKAGE"
            and blueprint.get("productForm") != "GENERIC"
            and blueprint.get("packageId") in {"com.curis.local.content-growth",
                "com.curis.local.writing-authoring", "com.curis.local.music"})
        data = assignment["data"]
        latest = {}
        for item in scoped.foundation.list("RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id):
            row = item["data"]
            if row.get("scopeType") != data["scopeType"] or row.get("scopeRef") != data["scopeRef"]:
                continue
            key = row["workflowKey"]
            if key not in latest or row["version"] > latest[key]["data"]["version"]:
                latest[key] = item
        matches = [item for item in latest.values()
            if any(value.get("assignmentRef") == assignment_ref for value in item["data"]["assignments"])]
        snapshot = scoped._assignment_snapshot(assignment)
        identity = [scoped.tenant_id, company_id, workspace_id, assignment_ref]
        workflow_key = "agent-assignment-" + hashlib.sha256(
            json.dumps(identity, separators=(",", ":")).encode()).hexdigest()[:32]
        current = len(matches) == 1 and snapshot in matches[0]["data"]["assignments"]
        collision = not matches and workflow_key in latest
        state = ("AMBIGUOUS" if len(matches) > 1 else "READY" if current
            else "STALE" if matches else "CONFLICT" if collision
            else "NEEDS_PUBLICATION" if professional else "UNSUPPORTED")
        reasons = {
            "AMBIGUOUS": "当前责任对应多个已发布流程，请由负责人核对，系统不会自动选择。",
            "READY": "已读取唯一的当前责任流程。继续原创建请求需要您单独确认。",
            "STALE": "已发布流程的责任快照已过期，请由负责人核对后再继续。",
            "CONFLICT": "当前责任的流程标识已被其他流程占用，请由负责人核对。",
            "NEEDS_PUBLICATION": "当前责任尚无已发布流程。请核对范围与责任，再明确确认发布。",
            "UNSUPPORTED": "请从该业务原有的团队流程入口核对和发布。",
        }
        token = hashlib.sha256(json.dumps({"identity": identity, "assignment": snapshot,
            "package_id": blueprint.get("packageId"), "scope": [data["scopeType"], data["scopeRef"]]},
            sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
        employee = scoped.foundation.get(data["employeeRef"])
        role = scoped.foundation.get(data["roleRef"])
        preview = {"tenant_id": scoped.tenant_id, "company_id": company_id, "workspace_id": workspace_id,
            "workspace_name": workspace["name"], "assignment_ref": assignment_ref,
            "assignment_revision": data["revision"], "employee_ref": data["employeeRef"],
            "employee_name": employee["data"].get("name") or data["employeeRef"],
            "role_ref": data["roleRef"], "role_name": role["data"].get("name") or data["responsibilityKey"],
            "responsibility_key": data["responsibilityKey"], "responsibility": data["responsibility"],
            "scope_type": data["scopeType"], "scope_ref": data["scopeRef"],
            "matching_count": len(matches), "state": state, "reason": reasons[state],
            "publication_allowed": professional and state == "NEEDS_PUBLICATION",
            "review_token": token, "workflow_key": workflow_key,
            "workflow": ({"workflow_ref": matches[0]["entity_id"],
                "version": matches[0]["data"]["version"],
                "default_flow": matches[0]["data"]["defaultFlow"]} if len(matches) == 1 else None)}
        return preview, assignment, scoped

    @router.get("/assignments/{assignment_ref}/agent-workflow")
    def read_assigned_agent_workflow(assignment_ref: str, company_id: str, workspace_id: str):
        try:
            with database.connect() as connection:
                connection.execute("begin")
                return assigned_workflow_review(assignment_ref, company_id, workspace_id, connection)[0]
        except KeyError as error:
            raise HTTPException(status_code=404, detail="当前责任不存在或不可访问。") from error
        except RuntimeScopeError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.post("/assignments/{assignment_ref}/agent-workflow")
    def publish_assigned_agent_workflow(assignment_ref: str, payload: PublishAssignedWorkflowIn):
        if not payload.confirm:
            raise HTTPException(status_code=422, detail="需要明确确认发布当前责任流程。")
        try:
            with database.connect() as connection:
                # Lock before checking the reviewed basis, including against other
                # processes and assignment edits. Publication uses the same transaction.
                connection.execute("begin immediate")
                preview, assignment, scoped = assigned_workflow_review(
                    assignment_ref, payload.company_id, payload.workspace_id, connection)
                if (preview["assignment_revision"] != payload.expected_revision
                    or preview["review_token"] != payload.review_token):
                    raise HTTPException(status_code=409, detail="责任或范围已变化，请重新核对后确认。")
                if preview["state"] == "READY":
                    return {**preview, "published": False}
                if not preview["publication_allowed"]:
                    raise HTTPException(status_code=409, detail=preview["reason"])
                data = assignment["data"]
                scoped.publish_workflow(company_id=payload.company_id, workspace_id=payload.workspace_id,
                    scope_type=data["scopeType"], scope_ref=data["scopeRef"],
                    workflow_key=preview["workflow_key"], assignment_refs=[assignment_ref],
                    default_flow=[data["responsibilityKey"]])
                result = assigned_workflow_review(
                    assignment_ref, payload.company_id, payload.workspace_id, connection)[0]
                if result["state"] != "READY":
                    raise HTTPException(status_code=409, detail="发布结果无法唯一核验，事务已撤销。")
                return {**result, "published": True}
        except KeyError as error:
            raise HTTPException(status_code=404, detail="当前责任不存在或不可访问。") from error
        except RuntimeScopeError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.post("/assignments/{assignment_ref}/work")
    def create_assigned_work(assignment_ref: str, payload: AssignedWorkIn, request: Request):
        if not payload.agent_binding_ref and not payload.model_key:
            return create_assigned_work_in_scope(assignment_ref, payload, database)
        with database.connect() as connection:
            connection.execute("begin immediate")
            # Copy only the database handle, never the database or global connect().
            # All bound Database methods now use this request's connection.
            scoped_database = copy.copy(database)
            scoped_connection = _WorkCreationConnection(connection)
            scoped_database.connect = lambda: nullcontext(scoped_connection)
            return create_assigned_work_in_scope(assignment_ref, payload, scoped_database,
                writing_entry=getattr(request.app.state, "writing_entry_service", None))

    def create_assigned_work_in_scope(assignment_ref, payload, database, *, writing_entry=None):
        from ..runtime.child_work import CanonicalChildWorkRuntime
        foundation = RuntimeFoundation(database)
        routing = ResponsibilityRoutingRuntime(database)
        try:
            assignment = foundation.get(assignment_ref)
            require_company(assignment["company_id"])
            if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
                raise RuntimeScopeError("Only the authorized Company actor may request work")
            with database.connect() as connection:
                scope = ResourceScopePolicy.authorize_assignment(connection, tenant_id=foundation.tenant_id,
                    company_id=assignment["company_id"], assignment_ref=assignment_ref,
                    employee_ref=assignment["data"].get("employeeRef"))
            contract = {"problem": payload.problem.strip(), "expectedResult": payload.expected_result.strip(),
                        "constraints": [], "references": []}
            workflow = None
            if payload.source and "review_ref" in payload.source and not payload.model_key:
                raise ValueError("Writing review continuation requires its chapter Model Work")
            if payload.model_key and payload.agent_binding_ref:
                raise ValueError("Choose one Model or Agent for the original Work")
            if payload.model_key:
                from ..employee_execution_identity import EmployeeExecutionIdentity
                from ..model_preferences import TenantModelPreferenceResolver
                from ..conversation_service import ConversationService
                if not payload.source or payload.source.get("kind") not in {"writing", "content-growth", "music"} or payload.browser_hosts:
                    raise ValueError("Model Work requires an explicit saved business object source")
                model = TenantModelPreferenceResolver(database)._require_eligible_model(foundation.tenant_id, payload.model_key)
                identity = EmployeeExecutionIdentity(database).resolve(company_id=scope["company_id"],
                    workspace_id=scope["workspace_id"], runtime_employee_ref=assignment["data"]["employeeRef"])
                with database.connect() as connection:
                    bindings = connection.execute("select * from employee_capability_bindings where tenant_id=? "
                        "and employee_id=? and capability_type='model' and capability_source=? and capability_id=? and enabled=1",
                        (foundation.tenant_id, identity["company_employee_ref"], model["source"], model["model_key"])).fetchall()
                if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE" or len(bindings) != 1:
                    raise RuntimeScopeError("Model Work requires its unique current employee binding")
                contract["modelBinding"] = {"bindingRef": bindings[0]["id"], "model": model}
                contract["modelSource"] = ConversationService(database).agent_work_source(
                    scope["company_id"], scope["workspace_id"], assignment_ref, payload.source)
                if contract["modelSource"].get("review"):
                    if writing_entry is None:
                        raise RuntimeScopeError("Current Writing execution authorization is unavailable")
                    with database.connect() as connection:
                        policy = writing_entry.execution_policy(scope["company_id"], scope["workspace_id"], connection=connection)
                    if (policy["status"] != "AVAILABLE" or policy["selected"]["model"] != model
                            or policy["binding"]["id"] != bindings[0]["id"]):
                        raise RuntimeScopeError("Current Writing authorization differs or is unavailable")
                    contract["references"] = [{"kind": "WRITING_REVIEW", **contract["modelSource"]["review"]}]
            elif payload.agent_binding_ref:
                from ..employee_execution_identity import EmployeeExecutionIdentity
                identity = EmployeeExecutionIdentity(database).resolve(company_id=scope["company_id"],
                    workspace_id=scope["workspace_id"], runtime_employee_ref=assignment["data"]["employeeRef"])
                with database.connect() as connection:
                    binding = connection.execute("select * from employee_capability_bindings where tenant_id=? "
                        "and employee_id=? and id=? and enabled=1 and capability_type='agent' and capability_source='tenant_private'",
                        (foundation.tenant_id, identity["company_employee_ref"], payload.agent_binding_ref)).fetchone()
                if binding is None:
                    raise RuntimeScopeError("所选 Agent 不属于当前员工的有效绑定。")
                capability = database.get_tenant_private_capability(foundation.tenant_id, "agent", binding["capability_id"])
                if not capability or capability.get("status") != "active":
                    raise RuntimeScopeError("所选 Agent 已不可用。")
                contract["agentBinding"] = {"bindingRef": binding["id"], "capabilityRef": binding["capability_id"],
                                            "employeeRef": identity["company_employee_ref"]}
                from ..conversation_service import ConversationService
                source = payload.source or {"kind": "references", "references": []}
                contract["agentSource"] = {"input": source, "snapshot": ConversationService(database).agent_work_source(
                    scope["company_id"], scope["workspace_id"], assignment_ref, source)}
                if payload.browser_hosts:
                    from ..agent_browser import PublicTargets
                    contract["agentBrowser"] = {"hosts": sorted(PublicTargets(payload.browser_hosts).hosts)}
            elif payload.source is not None or payload.browser_hosts:
                raise ValueError("原业务来源只用于明确选择 Agent 的正式工作。")
            if payload.agent_binding_ref or payload.model_key or assignment["data"].get("isLeader"):
                latest = {}
                for candidate in foundation.list("RESPONSIBILITY_WORKFLOW", company_id=scope["company_id"], workspace_id=scope["workspace_id"]):
                    data = candidate["data"]
                    if (data.get("scopeType"), data.get("scopeRef")) != (scope["scope_type"], scope["scope_ref"]):
                        continue
                    key = data["workflowKey"]
                    if key not in latest or data["version"] > latest[key]["data"]["version"]:
                        latest[key] = candidate
                matches = [item for item in latest.values() if any(row["assignmentRef"] == assignment_ref
                    for row in item["data"]["assignments"])]
                if len(matches) != 1:
                    raise RuntimeScopeError("当前员工责任没有唯一已发布流程，不能创建执行工作。")
                workflow = matches[0]
                if routing._assignment_snapshot(assignment) not in workflow["data"]["assignments"]:
                    raise RuntimeScopeError("已发布流程的员工责任快照已过期，不能创建执行工作。")
            child = CanonicalChildWorkRuntime(database)
            result = child.create_cycle_work(
                company_id=scope["company_id"], workspace_id=scope["workspace_id"],
                scope_type=scope["scope_type"], scope_ref=scope["scope_ref"], assignment_ref=assignment_ref,
                release_key=payload.request_id,
                contract=contract)
            if workflow:
                work = routing.start_work(result["work"]["entity_id"], scope_type=scope["scope_type"], scope_ref=scope["scope_ref"],
                    workflow_key=workflow["data"]["workflowKey"], initial_responsibility=assignment["data"]["responsibilityKey"])
                if work["lifecycle_status"] == "PLANNED":
                    child.transition_work(work["entity_id"], "READY", actor="SYSTEM", reason="原责任与执行偏好已核验")
                    child.transition_work(work["entity_id"], "ACTIVE", actor="SYSTEM", reason="等待用户启动原工作")
                result["work"] = foundation.get(work["entity_id"])
            if payload.model_key and contract["modelSource"]["kind"] == "writing":
                work, source = result["work"], contract["modelSource"]
                basis = {"book_ref": source["scope"]["book_ref"], "chapter_ref": source["scope"]["chapter_ref"],
                         "draft_ref": source["draft_ref"], "sha256": source["draft_sha256"]}
                with database.connect() as connection:
                    connection.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                        (json.dumps({**work["data"], "writingBasis": basis}, ensure_ascii=False), foundation.tenant_id, work["entity_id"]))
                result["work"] = foundation.get(work["entity_id"])
            return result
        except (KeyError, ValueError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/follow-up")
    def continue_agent_work(work_ref: str, payload: AgentFollowupIn):
        if payload.model_key:
            raise HTTPException(status_code=422, detail="Writing Model follow-up must originate in its chapter")
        from ..conversation_service import ConversationService
        from ..runtime.child_work import CanonicalChildWorkRuntime
        try:
            parent = foundation.get(work_ref)
            require_company(parent["company_id"])
            if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
                raise RuntimeScopeError("只有当前公司所有者可以明确续作。")
            if not payload.accept_result:
                raise RuntimeScopeError("请先明确认可本次结果作为续作依据。")
            service = ConversationService(database)
            proof, _ = verify_prior_result(database, parent["company_id"], work_ref,
                                           payload.accepted_task_ref, payload.prior_result.model_dump(exclude_none=True))
            original = service.agent_work_contract(parent)
            binding = original["agentBinding"]
            if payload.agent_binding_ref not in (None, binding["bindingRef"]):
                raise RuntimeScopeError("原工作续作不能替换已选员工与 Agent。")
            assignment_ref = parent["data"]["responsibilityAssignmentRef"]
            assignment = foundation.get(assignment_ref)
            source = payload.source or {"kind": "references", "references": []}
            snapshot = service.agent_work_source(parent["company_id"], parent["workspace_id"], assignment_ref, source)
            with database.connect() as con:
                enabled = con.execute("select 1 from employee_capability_bindings where tenant_id=? and id=? "
                    "and employee_id=? and capability_id=? and enabled=1 and capability_type='agent' and capability_source='tenant_private'",
                    (foundation.tenant_id, binding["bindingRef"], binding["employeeRef"], binding["capabilityRef"])).fetchone()
            if not enabled:
                raise RuntimeScopeError("原 Agent 绑定已变化；保留原结果，不能自动替换。")
            contract = {"problem": payload.problem.strip(), "expectedResult": payload.expected_result.strip(),
                "constraints": [], "references": [], "agentBinding": binding,
                "agentSource": {"input": source, "snapshot": snapshot},
                "priorResult": payload.prior_result.model_dump(exclude_none=True)}
            if payload.browser_hosts:
                from ..agent_browser import PublicTargets
                contract["agentBrowser"] = {"hosts": sorted(PublicTargets(payload.browser_hosts).hosts)}
            prior_route = parent["data"].get("responsibilityRouting") or {}
            workflow = foundation.get(prior_route.get("workflowRef") or "")
            latest = routing._latest_workflow(company_id=parent["company_id"], workspace_id=parent["workspace_id"],
                scope_type=prior_route["scopeType"], scope_ref=prior_route["scopeRef"],
                workflow_key=workflow["data"]["workflowKey"])
            if latest["entity_id"] != workflow["entity_id"]:
                raise RuntimeScopeError("原责任流程已变化，需要先核对，不会自动换用其他流程。")
            child = CanonicalChildWorkRuntime(database)
            result = child.release_next_work(work_ref, release_key=payload.request_id,
                target_assignment_ref=assignment_ref, accepted_result_ref="task:" + proof["task_ref"],
                reason=payload.problem, followup_contract=contract,
                parent_acceptance=service.agent_acceptance_evidence(parent["company_id"], work_ref, proof))
            work = routing.start_work(result["work"]["entity_id"], scope_type=prior_route["scopeType"],
                scope_ref=prior_route["scopeRef"], workflow_key=workflow["data"]["workflowKey"],
                initial_responsibility=assignment["data"]["responsibilityKey"])
            if work["lifecycle_status"] == "PLANNED":
                child.transition_work(work["entity_id"], "READY", actor="SYSTEM", reason="用户明确续作，原对象与新依据已核验")
                child.transition_work(work["entity_id"], "ACTIVE", actor="SYSTEM", reason="等待用户启动本次续作")
            result["work"] = foundation.get(work["entity_id"])
            return result
        except (KeyError, ValueError, OSError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/works/{work_ref}/candidate-source/{task_ref}")
    def read_agent_candidate_source(work_ref: str, task_ref: str, artifact_ref: str | None = None):
        from ..conversation_service import ConversationService
        try:
            work = foundation.get(work_ref)
            require_company(work["company_id"])
            proof = ConversationService(database).agent_result_proof(work["company_id"], work_ref, task_ref,
                require_current_source=False, artifact_ref=artifact_ref, for_candidate=True)
            return {"tenant_id": foundation.tenant_id, "company_id": work["company_id"], "workspace_id": work["workspace_id"],
                    "work_ref": work_ref, "task_ref": task_ref, "text": proof["text"], "text_sha256": proof["text_sha256"],
                    "task_output_sha256": proof["task_output_sha256"],
                    "source_kind": proof["source"]["kind"], "content_verification": "UNVERIFIED",
                    **({key: proof[key] for key in ("artifact_ref", "artifact_content_sha256", "file_sha256",
                        "task_output_sha256", "filename", "file_bytes")} if proof.get("artifact_ref") else {})}
        except (KeyError, ValueError, OSError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/candidate")
    def create_agent_candidate(work_ref: str, payload: AgentCandidateIn):
        from ..conversation_service import ConversationService
        try:
            work = foundation.get(work_ref)
            require_company(work["company_id"])
            if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
                raise RuntimeScopeError("只有当前公司所有者可以保存候选。")
            return ConversationService(database).materialize_agent_candidate(work["company_id"], work_ref,
                payload.task_ref, payload.model_dump(exclude={"task_ref"}, exclude_none=True))
        except (KeyError, ValueError, OSError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/works/{work_ref}/files/{artifact_ref}")
    def read_original_agent_file(work_ref: str, artifact_ref: str):
        import base64
        import hashlib
        from pathlib import Path
        from ..agent_work_resources import AgentWorkResources
        from ..result_attention import ResultAttention
        try:
            work = foundation.get(work_ref)
            if work["entity_type"] != "WORK":
                raise RuntimeScopeError("需要原工作引用。")
            require_company(work["company_id"])
            ResultAttention(database).actor(work["company_id"])
            with database.connect() as con:
                artifact = con.execute("select a.*,t.task_id from artifacts a join tasks t "
                    "on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                    "where a.tenant_id=? and a.artifact_id=? and a.artifact_type='agent_file_receipt' "
                    "and t.company_id=? and t.workspace_id is ? and t.work_ref=? and t.status='COMPLETED'",
                    (foundation.tenant_id, artifact_ref, work["company_id"], work["workspace_id"], work_ref)).fetchone()
            if not artifact or hashlib.sha256(artifact["content"].encode()).hexdigest() != artifact["content_sha256"]:
                raise RuntimeScopeError("原成果回执不存在或已改变。")
            receipt = json.loads(artifact["content"])
            resources = AgentWorkResources(Path(database.path).absolute().parent / "agent-work",
                tenant_id=foundation.tenant_id, company_id=work["company_id"], work_ref=work_ref, task_id=artifact["task_id"])
            content = resources.read_output(receipt)
            capture = receipt.get("browser_capture")
            if capture is not None:
                expected = {**resources.identity, "relative_path": receipt["relative_path"],
                            "sha256": receipt["sha256"], "bytes": receipt["bytes"]}
                from ..agent_work_resources import validate_reader_png
                validate_reader_png(content)
                if (not isinstance(capture, dict) or any(capture.get(k) != v for k, v in expected.items())
                        or capture.get("mime_type") != "image/png"
                        or not capture.get("session_id") or not capture.get("tab_id")
                        or not str(capture.get("url", "")).startswith("https://")):
                    raise RuntimeScopeError("浏览截图来源不一致。")
            return {"tenant_id": foundation.tenant_id, "company_id": work["company_id"], "work_ref": work_ref,
                    "workspace_id": work["workspace_id"], "task_id": artifact["task_id"],
                    "artifact_ref": artifact_ref, "artifact_content_sha256": artifact["content_sha256"],
                    "filename": Path(receipt["relative_path"]).name,
                    "sha256": receipt["sha256"], "bytes": len(content), "content_verification": "UNVERIFIED",
                    **({"browser_capture": capture, "mime_type": "image/png"} if capture else {}),
                    "content_base64": base64.b64encode(content).decode("ascii")}
        except (KeyError, ValueError, OSError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    def original_work_snapshot(work):
        with database.connect() as con:
            rows = con.execute("select task_id,status,updated_at,error,state_flow from tasks where tenant_id=? and company_id=? "
                "and workspace_id is ? and work_ref=? order by created_at",
                (foundation.tenant_id, work["company_id"], work["workspace_id"], work["entity_id"])).fetchall()
            tasks = []
            for row in rows:
                reserved = con.execute("select 1 from evolution_events where tenant_id=? and event_type='company.agent_allowance.reserved' "
                    "and json_extract(payload,'$.task_id')=? limit 1", (foundation.tenant_id, row["task_id"])).fetchone()
                progress = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='agent.execution.progress' order by event_id desc limit 1",
                    (foundation.tenant_id, row["task_id"])).fetchone()
                uncertain_events = con.execute(
                    "select payload,idempotency_key from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='agent.execution.outcome_unknown'",
                    (foundation.tenant_id, row["task_id"]),
                ).fetchall()
                uncertain_reason = None
                if uncertain_events:
                    uncertain_reason = "outcome_unverified"
                    try:
                        if (len(uncertain_events) == 1 and
                            uncertain_events[0]["idempotency_key"] == f"agent-outcome-unknown:{foundation.tenant_id}:{row['task_id']}" and
                            json.loads(uncertain_events[0]["payload"]) == {
                                "task_id": row["task_id"], "company_id": work["company_id"],
                                "workspace_id": work["workspace_id"], "work_ref": work["entity_id"]}):
                            uncertain_reason = "outcome_unknown"
                    except (TypeError, ValueError):
                        pass
                local_events = con.execute(
                    "select payload,idempotency_key from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='agent.execution.local_child_exit' limit 2",
                    (foundation.tenant_id, row["task_id"]),
                ).fetchall()
                local_process_state = "UNKNOWN"
                if len(local_events) == 1:
                    try:
                        local = json.loads(local_events[0]["payload"])
                        if not isinstance(local, dict):
                            raise ValueError("invalid local process evidence")
                        attempt = local.get("attempt_sha256")
                        expected = {"task_id": row["task_id"], "company_id": work["company_id"],
                                    "workspace_id": work["workspace_id"], "work_ref": work["entity_id"],
                                    "attempt_sha256": attempt, "state": "DIRECT_CHILD_REAPED",
                                    "returncode": local.get("returncode"), "external_effect": "UNKNOWN"}
                        if (local == expected and isinstance(attempt, str) and re.fullmatch(r"[0-9a-f]{64}", attempt)
                                and type(local["returncode"]) is int and -255 <= local["returncode"] <= 255
                                and local_events[0]["idempotency_key"] ==
                                    f"agent-local-child-exit:{foundation.tenant_id}:{row['task_id']}:{attempt}"):
                            local_process_state = "DIRECT_CHILD_REAPED"
                    except (TypeError, ValueError):
                        pass
                held_events = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='agent.execution.codex_held' limit 2",
                    (foundation.tenant_id, row["task_id"])).fetchall()
                held = False
                prefix = "codex_execution_held:"
                error_value = row["error"] or ""
                nonce = error_value[len(prefix):] if error_value.startswith(prefix) else ""
                if len(held_events) == 1 and len(nonce) == 32 and all(c in "0123456789abcdef" for c in nonce):
                    try:
                        held = json.loads(held_events[0]["payload"]) == {
                            "task_id": row["task_id"], "work_ref": work["entity_id"],
                            "company_id": work["company_id"], "workspace_id": work["workspace_id"],
                            "nonce": nonce, "state_flow": json.loads(row["state_flow"])}
                    except (TypeError, ValueError):
                        pass
                tasks.append({"task_id": row["task_id"], "status": row["status"], "updated_at": row["updated_at"],
                              "work_ref": work["entity_id"], "stage": json.loads(progress[0]).get("stage") if progress else None,
                              "call_reserved": bool(reserved),
                              "local_process_state": local_process_state,
                              "reason_code": uncertain_reason or ("codex_execution_held" if held and row["status"] == "FAILED" else None),
                              "result_ref": "task:" + row["task_id"] if row["status"] == "COMPLETED" and not uncertain_reason else None})
        return {"work": work, "tasks": tasks}

    @router.get("/works/{work_ref}")
    def read_original_work(work_ref: str):
        from ..result_attention import ResultAttention
        try:
            work = foundation.get(work_ref)
            if work["entity_type"] != "WORK":
                raise RuntimeScopeError("需要原工作引用。")
            require_company(work["company_id"])
            ResultAttention(database).actor(work["company_id"])
            root_ref = work["data"].get("rootWorkRef") or work_ref
            current = foundation.get(root_ref)
            history, seen = [], set()
            while True:
                if (current["entity_type"] != "WORK" or current["company_id"] != work["company_id"]
                        or current["workspace_id"] != work["workspace_id"] or current["entity_id"] in seen or len(seen) >= 64):
                    raise RuntimeScopeError("原工作续作关联无法完整核验。")
                seen.add(current["entity_id"])
                history.append(original_work_snapshot(current))
                with database.connect() as con:
                    successors = con.execute("select target_id from runtime_links where tenant_id=? and source_id=? "
                        "and relation='HAS_SUCCESSOR_WORK'", (foundation.tenant_id, current["entity_id"])).fetchall()
                if not successors:
                    break
                if len(successors) != 1:
                    raise RuntimeScopeError("原工作存在冲突的后续关联。")
                successor = foundation.get(successors[0]["target_id"])
                if successor["data"].get("rootWorkRef") != root_ref:
                    break
                if successor["data"].get("predecessorWorkRef") != current["entity_id"]:
                    raise RuntimeScopeError("原工作前后关联不一致。")
                current = successor
            if work_ref not in seen:
                raise RuntimeScopeError("该工作未包含在原工作关联中。")
            from ..conversation_service import ConversationService
            origin = {"status": "UNKNOWN"}
            try:
                service = ConversationService(database)
                origins = [_verified_origin_projection(item["work"], service.agent_work_contract(item["work"]),
                                                       foundation.tenant_id) for item in history]
                if origins and origins[0].get("status") == "VERIFIED" and all(value == origins[0] for value in origins):
                    origin = origins[0]
            except (KeyError, ValueError, RuntimeScopeError, TypeError):
                pass
            return {"tenant_id": foundation.tenant_id, "root_work_ref": root_ref,
                    **history[-1], "history": history, "origin": origin}
        except (KeyError, ValueError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    def require_company(company_id: str) -> None:
        current = TenantContext.current_identity().get("company_id")
        if current and current != company_id:
            raise RuntimeScopeError("Company identity does not match the current request")

    def workflows(company_id: str, workspace_id: str | None, scope_type: str, scope_ref: str, workflow_key: str):
        return [
            item for item in foundation.list("RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id)
            if item["data"].get("scopeType") == scope_type
            and item["data"].get("scopeRef") == scope_ref
            and item["data"].get("workflowKey") == workflow_key
        ]

    def running_work(workflow_refs: list[str]) -> list[dict[str, Any]]:
        if not workflow_refs:
            return []
        with database.connect() as conn:
            rows = conn.execute(
                "select entity_id, entity_type, lifecycle_status, data_json from runtime_entities "
                "where tenant_id=? and json_extract(data_json, '$.responsibilityRouting.workflowRef') in "
                f"({','.join('?' for _ in workflow_refs)}) order by created_at, entity_id",
                (TenantContext.current_tenant_id(), *workflow_refs),
            ).fetchall()
        import json
        result = []
        for row in rows:
            data = json.loads(row["data_json"])
            route = data["responsibilityRouting"]
            result.append({
                "work_ref": row["entity_id"],
                "work_type": row["entity_type"],
                "work_status": row["lifecycle_status"] if row["lifecycle_status"] in {"COMPLETED", "CANCELLED", "ARCHIVED"} else route.get("status"),
                "workflow_ref": route.get("workflowRef"),
                "workflow_version": route.get("workflowVersion"),
                "responsibility_holder_ref": route.get("responsibilityHolderRef"),
                "current_executor_ref": None if row["lifecycle_status"] in {"COMPLETED", "CANCELLED", "ARCHIVED"} else route.get("currentExecutorRef"),
            })
        return result

    def projection(company_id: str, workspace_id: str | None, scope_type: str, scope_ref: str, workflow_key: str):
        require_company(company_id)
        values = workflows(company_id, workspace_id, scope_type, scope_ref, workflow_key)
        latest = max(values, key=lambda item: int(item["data"].get("version") or 0), default=None)
        employees = foundation.list("AI_EMPLOYEE", company_id=company_id, workspace_id=workspace_id)
        roles = []
        for item in (latest["data"]["assignments"] if latest else []):
            role = foundation.get(item["roleRef"])
            roles.append({**item, "roleName": role["data"].get("role") or item["responsibilityKey"]})
        return {
            "scope": {"type": scope_type, "ref": scope_ref, "workspace_id": workspace_id},
            "workflow_key": workflow_key,
            "published": None if latest is None else {
                "workflow_ref": latest["entity_id"],
                "version": latest["data"]["version"],
                "default_flow": latest["data"]["defaultFlow"],
                "roles": roles,
                "published_at": latest["data"]["publishedAt"],
            },
            "available_employees": [
                {"employee_ref": item["entity_id"], "name": item["data"].get("name") or item["entity_id"], "status": item["lifecycle_status"]}
                for item in employees if item["lifecycle_status"] in {"AVAILABLE", "OPERATING"}
            ],
            "running_work": running_work([item["entity_id"] for item in values]),
        }

    def assignment_for(work: dict[str, Any], assignment_ref: str | None = None) -> dict[str, Any]:
        route = work["data"]["responsibilityRouting"]
        workflow = foundation.get(route["workflowRef"])
        wanted = assignment_ref or route["currentAssignmentRef"]
        return next(item for item in workflow["data"]["assignments"] if item["assignmentRef"] == wanted)

    def execution_key(work: dict[str, Any], assignment: dict[str, Any], purpose: str) -> str:
        route = work["data"]["responsibilityRouting"]
        human = route.get("humanInput") or {}
        if purpose == "responsibility" and human.get("state") == "CLAIMED":
            if human.get("assignmentRef") != assignment["assignmentRef"]:
                raise ResponsibilityRoutingError("Human Input assignment changed")
            return human["continuationKey"]
        records = list((route.get("executions") or {}).values())
        matching = [
            item for item in records
            if item.get("assignmentRef") == assignment["assignmentRef"]
            and str(item.get("executionKey") or "").startswith(f"{purpose}:")
        ]
        if matching and purpose.startswith("leader:"):
            return matching[-1]["executionKey"]
        if matching and matching[-1].get("status") == "ACCEPTED":
            if purpose.startswith("consult:") or route.get("lastAction") == "EMPLOYEE_RESULT_ACCEPTED":
                return matching[-1]["executionKey"]
        number = 1 + sum(
            1 for item in records
            if item.get("assignmentRef") == assignment["assignmentRef"]
            and str(item.get("executionKey") or "").startswith(f"{purpose}:")
        )
        return f"{purpose}:{work['entity_id']}:{assignment['assignmentRef']}:{number}"

    def normalized_result(raw: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
        output = str(raw.get("output") or "")
        try:
            value = json.loads(output)
        except (TypeError, json.JSONDecodeError):
            value = {}
        expected = str(assignment.get("outputContract", {}).get("resultType") or "").strip()
        result_type = value.get("resultType", "").strip() if isinstance(value, dict) and type(value.get("resultType")) is str else ""
        provider_status = value.get("status", "").upper() if isinstance(value, dict) and type(value.get("status")) is str else ""
        callback = (raw.get("execution_binding") or {}).get("callbackProvenance") or {}
        task_ok = str(raw.get("task_status") or "").upper() == "COMPLETED"
        provenance_ok = callback.get("verification_status") == "VERIFIED"
        contract_ok = bool(result_type) and (not expected or result_type == expected)
        accepted = provider_status == "ACCEPTED" and task_ok and provenance_ok and contract_ok
        rejected = provider_status == "REJECTED" and task_ok and provenance_ok and contract_ok
        requested = provider_status == "USER_REQUIRED" and task_ok and provenance_ok and contract_ok
        return {
            "status": "ACCEPTED" if accepted else "REJECTED" if rejected else "PARTIAL" if requested else "FAILED",
            "summary": str(value.get("summary") or "")[:2000] if isinstance(value, dict) else "",
            "result_type": result_type,
            "problem": str(value.get("problem") or "")[:2000] if isinstance(value, dict) else "",
            "request_fields": value.get("humanInput") if requested and isinstance(value.get("humanInput"), dict) else {},
        }

    def general_work_context(work: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any] | None:
        data = work["data"]
        if data.get("kind") != "CANONICAL_CHILD_WORK":
            return None
        cycle = foundation.get(str(data.get("cycleRef") or ""))
        if (
            cycle["entity_type"] != "CYCLE"
            or cycle["company_id"] != work["company_id"]
            or cycle["workspace_id"] != work["workspace_id"]
        ):
            raise RuntimeScopeError("General Work requires its canonical Cycle context")
        if cycle["data"].get("kind") != "GENERAL_WORK_CYCLE":
            return None
        contract = data.get("followupContract") or cycle["data"].get("contract") or {}
        agent_source = None
        if contract.get("agentBinding"):
            from ..conversation_service import ConversationService
            agent_source = ConversationService(database).validate_agent_work_source(work)
        prior_result = verified_prior_for_work(database, work) if contract.get("agentBinding") or data.get("followupContract") else None
        if not str(contract.get("problem") or "").strip() or not str(contract.get("expectedResult") or "").strip():
            raise RuntimeScopeError("General Work Cycle context is incomplete")
        with database.connect() as connection:
            scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=TenantContext.current_tenant_id(), record=work)
            ResourceScopePolicy.require_same_execution_scope(scope, ResourceScopePolicy.execution_scope_from_record(
                connection, tenant_id=TenantContext.current_tenant_id(), record=cycle))
            ResourceScopePolicy.authorize_assignment(connection, tenant_id=TenantContext.current_tenant_id(),
                company_id=work["company_id"], assignment_ref=assignment["assignmentRef"],
                employee_ref=assignment["employeeRef"], revision=assignment["assignmentRevision"], scope=scope)
            canonical = ResourceScopePolicy.bounded_lineage_context(connection, scope)
        employee = foundation.get(assignment["employeeRef"])
        role = foundation.get(assignment["roleRef"])
        if employee["company_id"] != work["company_id"] or employee["workspace_id"] not in (None, work["workspace_id"]):
            raise RuntimeScopeError("General Work Employee is outside the Workspace")
        refs = list(dict.fromkeys([
            *list(contract.get("references") or []),
            *list(data.get("inputRefs") or []),
        ]))
        knowledge_work = knowledge._work_scope(work["entity_id"])
        explicit_knowledge = knowledge.list_work_references(work["entity_id"])["references"]
        with database.connect() as connection:
            links = connection.execute(
                "select company_id, workspace_id, target_ref from typed_object_references "
                "where tenant_id=? and source_type='WORK' and source_ref=? "
                "and relation='USES_REFERENCE' and target_type='KNOWLEDGE'",
                (foundation.tenant_id, work["entity_id"]),
            ).fetchall()
        if (len(links) != len(explicit_knowledge)
                or {row["target_ref"] for row in links} != {item["id"] for item in explicit_knowledge}
                or any(row["company_id"] != work["company_id"] or row["workspace_id"] != work["workspace_id"] for row in links)
                or any(item["lifecycle_status"] != "ACTIVE" or not knowledge._compatible(item, knowledge_work) for item in explicit_knowledge)):
            raise RuntimeScopeError("General Work knowledge reference is invalid or outside its scope")
        knowledge_context = knowledge.context_for_work(work["entity_id"], query="")
        knowledge_refs = [item["ref"] for item in knowledge_context["references"]]
        return {
            "cycle_ref": cycle["entity_id"],
            **canonical,
            "work": {
                "agentSource": agent_source,
                **({"priorResultHash": prior_binding_digest(prior_result)} if contract.get("agentBinding") else {}),
                "problem": str(contract["problem"]),
                "expectedResult": str(contract["expectedResult"]),
                "constraints": [str(item)[:300] for item in list(contract.get("constraints") or [])[:16]],
                "inputRefs": refs[:32],
                "why": f"{str(canonical.get('business', {}).get('goal') or '')[:400]} → {str(contract['problem'])[:400]}",
            },
            "employee": {
                "id": assignment["employeeRef"],
                "name": str(employee["data"].get("name") or assignment["employeeRef"])[:120],
                "role": str(role["data"].get("role") or role["data"].get("name") or assignment["responsibilityKey"])[:120],
                "responsibility": str(assignment["responsibility"])[:1000],
            },
            "knowledge": knowledge_context,
            "selected_refs": list(dict.fromkeys([*refs, *knowledge_refs]))[:32],
        }

    def require_scoped_refs(work: dict[str, Any], refs: list[str]) -> None:
        with database.connect() as connection:
            scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=TenantContext.current_tenant_id(), record=work)
            for reference in refs:
                if reference.startswith("knowledge:"):
                    knowledge_ref = reference.split(":", 1)[1]
                    linked = connection.execute(
                        "select 1 from typed_object_references where tenant_id=? and company_id=? "
                        "and workspace_id is ? and source_type='WORK' and source_ref=? "
                        "and relation='USES_REFERENCE' and target_type='KNOWLEDGE' and target_ref=?",
                        (
                            TenantContext.current_tenant_id(), work["company_id"],
                            work["workspace_id"], work["entity_id"], knowledge_ref,
                        ),
                    ).fetchone()
                    if linked is None:
                        raise RuntimeScopeError("Knowledge reference is not selected for this Work")
                    continue
                runtime = connection.execute(
                    "select * from runtime_entities where entity_id=? limit 1",
                    (reference,),
                ).fetchone()
                task_ref = reference.split(":", 1)[1] if reference.startswith("task:") else ""
                task = connection.execute(
                    "select * from tasks where task_id=? limit 1",
                    (task_ref,),
                ).fetchone() if task_ref else None
                artifact = connection.execute(
                    "select t.* from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                    "where a.artifact_id=? limit 1",
                    (reference,),
                ).fetchone()
                for owned in (runtime, task, artifact):
                    if owned is not None:
                        ResourceScopePolicy.require_same_execution_scope(scope, ResourceScopePolicy.execution_scope_from_record(
                            connection, tenant_id=TenantContext.current_tenant_id(), record=dict(owned)))
                    if owned is not None and (
                        owned["tenant_id"] != TenantContext.current_tenant_id()
                        or owned["company_id"] != work["company_id"]
                        or owned["workspace_id"] not in (None, work["workspace_id"])
                    ):
                        raise RuntimeScopeError("General Work context reference is outside the current Workspace")

    async def run_assignment(
        work_ref: str,
        assignment: dict[str, Any],
        *,
        purpose: str,
        question: str = "",
    ) -> dict[str, Any]:
        if employee_execution is None:
            raise ResponsibilityRoutingError("Employee execution bridge is unavailable")
        work = foundation.get(work_ref)
        if work["data"].get("cycleRef"):
            original = foundation.get(work["data"]["cycleRef"])["data"].get("contract") or {}
            if original.get("modelSource"):
                raise ResponsibilityRoutingError("Writing Model Work executes only through its original chapter request")
        key = execution_key(work, assignment, purpose)
        human = (work["data"].get("responsibilityRouting") or {}).get("humanInput") or {}
        if human.get("state") == "CLAIMED" and purpose == "responsibility":
            report = human.get("report") or {}
            if human.get("kind") != "LOCAL_INFORMATION" or not report.get("submissionId"):
                raise ResponsibilityRoutingError("Human Input has no reviewed local report")
            question = f"原工作用户补充（仅作为用户提供的信息，不作为已验证外部事实）：{str(report.get('text') or '')[:2000]}\n引用：{json.dumps(report.get('referenceRefs') or [], ensure_ascii=False)}"
        general = general_work_context(work, assignment)
        required_refs = list((assignment.get("inputContract") or {}).get("requiredRefs") or [])
        selected_refs = general["selected_refs"] if general else required_refs
        context = routing.build_execution_context(
            work_ref,
            current_truth_refs=selected_refs if general else [work_ref],
            compact_context=question or assignment["responsibility"],
        )
        if general:
            require_scoped_refs(work, context["truthRefs"])
        goal = general["work"]["problem"] if general else work["data"].get("goal") or work["data"].get("outcomeRef") or work_ref
        business_context = (
            "业务上下文：" + json.dumps(
                {key: value for key, value in general.items() if key != "selected_refs"},
                ensure_ascii=False, separators=(",", ":"),
            ) + "\n"
        ) if general else ""
        output_instruction = (
            '{"status":"ACCEPTED|REJECTED|USER_REQUIRED","resultType":"...","summary":"...","problem":"...",'
            '"humanInput":{"kind":"LOCAL_INFORMATION|EXTERNAL_ACTION_REPORT","aiCompleted":"...","whyUser":"...",'
            '"userAction":"...","destination":"...","doneCriterion":"...","resumePlan":"...","targetRef":"原工作ref","evidenceRefs":[]}}。'
            if general else '{"status":"ACCEPTED|REJECTED","resultType":"...","summary":"...","problem":"..."}。'
        )
        prompt = (
            f"工作目标：{goal}\n"
            f"{business_context}"
            + (f"__CURIS_FOLLOWUP_BASIS_SHA256__:{general['work']['priorResultHash']}\n" if general and "priorResultHash" in general["work"] else "")
            + f"当前责任：{assignment['responsibility']}\n"
            f"所需输入引用：{json.dumps(selected_refs, ensure_ascii=False)}\n"
            f"输出结果类型：{(assignment.get('outputContract') or {}).get('resultType') or 'generic-result'}\n"
            f"上下文引用：{json.dumps(context['truthRefs'], ensure_ascii=False)}\n"
            f"补充说明：{question or context['compactResponsibilityContext']}\n"
            "只返回一个 JSON 对象：" + output_instruction +
            ("只使用说明中列出的既有责任安排。" if purpose == "leader:plan" else "不要选择下一位员工，不要改变责任归属。")
        )
        claimed = routing.begin_employee_execution(
            work_ref, execution_key=key, assignment_ref=assignment["assignmentRef"],
        )
        record = claimed["execution"]
        if claimed["duplicate"] and record.get("status") in {"ACCEPTED", "REJECTED", "PARTIAL", "FAILED", "CANCELLED"}:
            return {
                "status": record["status"], "task_ref": record.get("taskRef"),
                "artifact_refs": list(record.get("artifactRefs") or []),
                "context_metrics": dict(record.get("contextMetrics") or {}),
                "summary": str(record.get("resultSummary") or ""),
                "result_type": str(record.get("resultType") or ""), "problem": "",
            }
        if claimed["duplicate"] and record.get("status") in {"SUBMITTING", "RUNNING"}:
            return {"status": "IN_PROGRESS", "task_ref": record.get("taskRef"),
                    "artifact_refs": [], "context_metrics": {}, "summary": "原执行仍在进行", "result_type": "", "problem": ""}
        task_ref = str(record.get("taskRef") or "")
        human_continuation = (human.get("state") == "CLAIMED" and human.get("continuationKey") == key)
        try:
            if not task_ref:
                submitted = await employee_execution({
                    "execution_ref": "team_employee:auto", "mode": "submit",
                    "company_id": work["company_id"], "workspace_id": work["workspace_id"],
                    "work_ref": work_ref, "execution_key": key,
                    "runtime_employee_ref": assignment["employeeRef"],
                    "assignment": assignment, "prompt": prompt,
                })
                task_ref = str(submitted.get("task_ref") or "")
                if not task_ref:
                    raise ResponsibilityRoutingError("Employee execution did not create a Provider Task")
                routing.attach_provider_task(work_ref, execution_key=key, task_ref=task_ref)
            raw = await employee_execution({
                "execution_ref": "team_employee:auto", "mode": "run",
                "company_id": work["company_id"], "workspace_id": work["workspace_id"],
                "work_ref": work_ref, "execution_key": key,
                "runtime_employee_ref": assignment["employeeRef"], "task_ref": task_ref,
            })
        except Exception as error:
            if human_continuation:
                if not task_ref:
                    with database.connect() as connection:
                        matching = connection.execute(
                            "select task_id from tasks where tenant_id=? and company_id=? and workspace_id=? "
                            "and work_ref=? and execution_ref=?",
                            (TenantContext.current_tenant_id(), work["company_id"], work["workspace_id"], work_ref, key),
                        ).fetchall()
                    if len(matching) > 1:
                        raise ResponsibilityRoutingError("Human Input continuation has ambiguous Task evidence") from error
                    if matching:
                        task_ref = matching[0]["task_id"]
                        routing.attach_provider_task(work_ref, execution_key=key, task_ref=task_ref)
                return {"status": "IN_PROGRESS", "task_ref": task_ref or None,
                        "artifact_refs": [], "context_metrics": {},
                        "summary": "原工作续接结果尚未确认；保留原领取并等待核对，不自动重试",
                        "result_type": "", "problem": ""}
            failure = str(getattr(error, "code", "employee_execution_failed"))
            routing.finish_employee_execution(
                work_ref, execution_key=key, status="FAILED", task_ref=task_ref,
                session_ref="", result_summary=failure, context_metrics={
                    "chars": len(prompt), "bytes": len(prompt.encode("utf-8")),
                    "refsCount": len(context["truthRefs"]), "hydratedBodiesCount": 0,
                    "copiedConversationHistory": False, "providerTaskCount": 1 if task_ref else 0,
                    "providerSessionCount": 0,
                },
            )
            return {
                "status": "FAILED", "task_ref": task_ref, "artifact_refs": [],
                "context_metrics": {}, "summary": failure, "result_type": "", "problem": failure,
            }
        if human_continuation:
            binding = raw.get("execution_binding") if isinstance(raw, dict) else None
            callback_evidence = binding.get("callbackProvenance") if isinstance(binding, dict) else None
            with database.connect() as connection:
                task_evidence = connection.execute(
                    "select status, output, employee_id from tasks where tenant_id=? and company_id=? "
                    "and workspace_id=? and task_id=? and work_ref=? and execution_ref=?",
                    (TenantContext.current_tenant_id(), work["company_id"], work["workspace_id"],
                     task_ref, work_ref, key),
                ).fetchone()
            terminal_evidence = (
                isinstance(raw, dict) and isinstance(callback_evidence, dict)
                and task_evidence is not None
                and task_evidence["status"] in {"COMPLETED", "FAILED"}
                and raw.get("task_ref") in {None, task_ref}
                and raw.get("task_status") == task_evidence["status"]
                and task_evidence["employee_id"] == assignment["employeeRef"]
                and callback_evidence.get("verification_status") == "VERIFIED"
                and callback_evidence.get("task_ref") == task_ref
                and callback_evidence.get("task_status") == task_evidence["status"]
                and callback_evidence.get("callback_actor_ref") == assignment["employeeRef"]
                and (task_evidence["status"] != "COMPLETED" or raw.get("output") == task_evidence["output"])
            )
            if not terminal_evidence:
                return {"status": "IN_PROGRESS", "task_ref": task_ref or None,
                        "artifact_refs": [], "context_metrics": {},
                        "summary": "原工作续接结果尚未确认；保留原领取并等待核对，不自动重试",
                        "result_type": "", "problem": ""}
        normalized = normalized_result(raw, assignment)
        artifacts = [str(item) for item in raw.get("artifact_refs") or []]
        callback = (raw.get("execution_binding") or {}).get("callbackProvenance") or {}
        context_metrics = {
            "chars": len(prompt), "bytes": len(prompt.encode("utf-8")),
            "refsCount": len(context["truthRefs"]), "hydratedBodiesCount": 0,
            "knowledgeRefsCount": len((general or {}).get("knowledge", {}).get("references", [])),
            "copiedConversationHistory": False, "providerTaskCount": 1,
            "providerSessionCount": 1 if raw.get("session_ref") else 0,
        }
        if normalized["status"] == "PARTIAL" and general:
            try:
                routing.finish_user_required_execution(
                    work_ref, execution_key=key, task_ref=task_ref,
                    session_ref=str(raw.get("session_ref") or ""),
                    request_fields=normalized["request_fields"], callback=callback,
                    source_output=str(raw.get("output") or ""),
                )
            except ResponsibilityRoutingError:
                routing.finish_employee_execution(
                    work_ref, execution_key=key, status="FAILED", task_ref=task_ref,
                    session_ref=str(raw.get("session_ref") or ""), result_ref=f"task:{task_ref}",
                    result_summary="Human Input request contract invalid; original Work awaits review",
                    result_type=normalized["result_type"], provenance=callback,
                    context_metrics=context_metrics,
                )
                return {"status": "FAILED", "task_ref": task_ref, "artifact_refs": [],
                        "context_metrics": context_metrics, "summary": "Human Input request contract invalid",
                        "result_type": normalized["result_type"], "problem": "Human Input request contract invalid"}
            return {**normalized, "task_ref": task_ref, "artifact_refs": [], "context_metrics": context_metrics}
        routing.finish_employee_execution(
            work_ref, execution_key=key, status=normalized["status"], task_ref=task_ref,
            session_ref=str(raw.get("session_ref") or ""), result_ref=f"task:{task_ref}",
            artifact_refs=artifacts,
            evidence_refs=[str(callback["evidence_event_ref"])] if callback.get("evidence_event_ref") else [],
            result_summary=(
                f"{normalized['problem']} 恢复方式：补充所需输入后继续同一工作。"
                if normalized["status"] == "REJECTED" and normalized["problem"]
                else normalized["summary"]
            ), result_type=normalized["result_type"],
            provenance=callback, context_metrics=context_metrics,
        )
        return {**normalized, "task_ref": task_ref, "artifact_refs": artifacts, "context_metrics": context_metrics}

    def leader_child_contract(root, assignment, item):
        from ..employee_execution_identity import EmployeeExecutionIdentity
        identity = EmployeeExecutionIdentity(database).resolve(company_id=root["company_id"],
            workspace_id=root["workspace_id"], runtime_employee_ref=assignment["employeeRef"])
        binding = leader_preferred_binding(database, root, assignment, identity["company_employee_ref"])
        if binding["capability_type"] not in {"agent", "model"}:
            raise RuntimeScopeError("Leader target requires an Agent or API model")
        if binding["capability_source"] == "tenant_private":
            capability = database.get_tenant_private_capability(foundation.tenant_id, binding["capability_type"], binding["capability_id"])
        elif binding["capability_source"] == "official" and binding["capability_type"] == "model":
            capability = database.get_active_official_model(binding["capability_id"])
        else:
            capability = None
        if not capability or capability.get("status") != "active":
            raise RuntimeScopeError("Leader target capability is unavailable")
        original = root["data"].get("followupContract") or foundation.get(root["parent_id"])["data"].get("contract") or {}
        contract = {"problem": item["problem"], "expectedResult": item["expectedResult"],
                    "constraints": list(original.get("constraints") or []), "references": list(original.get("references") or []),
                    "capabilityBindingRef": binding["id"]}
        if binding["capability_type"] == "agent":
            from ..conversation_service import ConversationService
            source = (original.get("agentSource") or {}).get("input") or {"kind": "references", "references": contract["references"]}
            contract["agentBinding"] = {"bindingRef": binding["id"], "capabilityRef": binding["capability_id"],
                                        "employeeRef": identity["company_employee_ref"]}
            contract["agentSource"] = {"input": source, "snapshot": ConversationService(database).agent_work_source(
                root["company_id"], root["workspace_id"], assignment["assignmentRef"], source)}
        return contract

    async def run_leader(work_ref):
        from ..runtime.child_work import CanonicalChildWorkRuntime
        child_runtime = CanonicalChildWorkRuntime(database)
        root = foundation.get(work_ref)
        route = root["data"]["responsibilityRouting"]
        leader = assignment_for(root)
        workflow = foundation.get(route["workflowRef"])
        targets = [a for a in workflow["data"]["assignments"] if not a.get("isLeader")]
        if not targets or root["data"].get("kind") != "CANONICAL_CHILD_WORK":
            raise RuntimeScopeError("Leader delegation requires canonical business Work and existing target responsibilities")
        state = root["data"].get("leaderDelegation")
        if not state:
            description = [{k: a[k] for k in ("assignmentRef", "responsibility", "employeeRef")} for a in targets]
            result = await run_assignment(work_ref, leader, purpose="leader:plan", question=
                "在现有授权内自主派发普通业务任务。仅从以下责任中选择，每个责任最多一项、总计最多6项。"
                "额外返回 delegations 数组，每项严格为 assignmentRef、problem、expectedResult 三个字符串。"
                "不得扩大权限或要求用户逐项确认计划；已有高风险限制仍适用。可选责任：" + json.dumps(description, ensure_ascii=False))
            if result["status"] != "ACCEPTED":
                return {"work": foundation.get(work_ref), "delegation_status": result["status"]}
            with database.connect() as con:
                task = con.execute("select output from tasks where tenant_id=? and work_ref=? and task_id=? and status='COMPLETED'",
                    (foundation.tenant_id, work_ref, result["task_ref"])).fetchone()
            plan = json.loads(task["output"]).get("delegations") if task else None
            if not isinstance(plan, list) or not 1 <= len(plan) <= 6:
                raise RuntimeScopeError("Leader Result requires a bounded delegation plan; original Result retained")
            items = []
            for item in plan:
                if (not isinstance(item, dict) or set(item) != {"assignmentRef", "problem", "expectedResult"}
                        or any(type(v) is not str or not v.strip() or len(v) > 1600 for v in item.values())):
                    raise RuntimeScopeError("Leader delegation item has an invalid contract")
                target = next((a for a in targets if a["assignmentRef"] == item["assignmentRef"]), None)
                if not target:
                    raise RuntimeScopeError("Leader selected an unknown responsibility")
                items.append({**item, "contract": leader_child_contract(root, target, item)})
            child_runtime.release_leader_plan(work_ref, result["task_ref"], items)
            state = foundation.get(work_ref)["data"]["leaderDelegation"]
        results = []
        for ref in state["childWorkRefs"]:
            current_root = foundation.get(work_ref)
            if current_root["lifecycle_status"] != "ACTIVE" or current_root["data"]["responsibilityRouting"]["status"] != "ACTIVE":
                return {"work": current_root, "delegation_status": "BLOCKED"}
            child = foundation.get(ref)
            if child["lifecycle_status"] not in {"ACTIVE", "COMPLETED"}:
                return {"work": current_root, "delegation_status": "CHILD_BLOCKED", "child_work_ref": ref}
            result = await run_assignment(ref, assignment_for(child), purpose="leader:worker")
            if result["status"] != "ACCEPTED":
                return {"work": foundation.get(work_ref), "delegation_status": result["status"], "child_work_ref": ref}
            results.append({"workRef": ref, "taskRef": result["task_ref"], "summary": result["summary"],
                            "acceptance": "PENDING", "artifactRefs": result["artifact_refs"]})
        summary_ref = child_runtime.release_leader_summary(work_ref)
        result = await run_assignment(summary_ref, leader, purpose="leader:summary", question=
            "汇总以下原子 Work 的已验证员工结果，返回原 Work；这些成果仍待既有验收，不得声称用户已接受或产品已完成。"
            + json.dumps(results, ensure_ascii=False))
        if result["status"] == "ACCEPTED":
            child_runtime.attach_leader_summary(work_ref)
        return {"work": foundation.get(work_ref), "delegation_status": result["status"], "summary_work_ref": summary_ref,
                "child_work_refs": state["childWorkRefs"], "acceptance_pending": True}

    async def run_loop(work_ref: str, max_executions: int = 16) -> dict[str, Any]:
        for _ in range(max_executions):
            work = foundation.get(work_ref)
            if work["lifecycle_status"] in {"PAUSED", "CANCELLED", "ARCHIVED", "COMPLETED", "FAILED"}:
                return {"work": work, "execution_blocked": "Work lifecycle does not allow a new execution"}
            route = work["data"].get("responsibilityRouting") or {}
            human = route.get("humanInput") or {}
            if human and human.get("state") not in {"CLOSED", "INVALIDATED", "CLAIMED"}:
                return {"work": work, "execution_blocked": "原工作等待用户必要输入"}
            if route.get("status") in {"COMPLETED", "CANCELLED", "WAITING", "WAITING_DECISION"}:
                return {"work": work}
            assignment = assignment_for(work)
            if (assignment.get("isLeader") and work["data"].get("kind") == "CANONICAL_CHILD_WORK"
                    and not work["data"].get("leaderRootWorkRef")
                    and any(not a.get("isLeader") for a in foundation.get(route["workflowRef"])["data"]["assignments"])):
                return await run_leader(work_ref)
            input_contract = assignment.get("inputContract") or {}
            consult_key = f"auto-consult:{assignment['assignmentRef']}"
            consult_responsibility = str(input_contract.get("consultResponsibility") or "")
            collaboration = (route.get("collaborations") or {}).get(consult_key)
            if consult_responsibility and not collaboration:
                collaboration = routing.consult(
                    work_ref, consultant_responsibility=consult_responsibility,
                    question=str(input_contract.get("consultQuestion") or assignment["responsibility"]),
                    interaction_key=consult_key, context_refs=[work_ref],
                    bounded_summary="只提供当前工作、责任和已验收结果引用。",
                )["consult"]
            if collaboration and collaboration.get("status") == "WAITING":
                consultant = assignment_for(foundation.get(work_ref), collaboration["targetAssignmentRef"])
                result = await run_assignment(
                    work_ref, consultant, purpose=f"consult:{consult_key}", question=collaboration["question"],
                )
                if result["status"] != "ACCEPTED":
                    return {"work": foundation.get(work_ref)}
                routing.complete_consult(
                    work_ref, interaction_key=consult_key, response=result["summary"] or "咨询已完成",
                    result_refs=[f"task:{result['task_ref']}"], artifact_refs=result["artifact_refs"],
                )
                work = foundation.get(work_ref)
                assignment = assignment_for(work)

            result = await run_assignment(work_ref, assignment, purpose="responsibility")
            if result["status"] == "ACCEPTED":
                routed = routing.route(
                    work_ref, signal="COMPLETED", result_refs=[f"task:{result['task_ref']}"],
                    artifact_refs=result["artifact_refs"],
                )
                if routed["action"] == "COMPLETE":
                    return {"work": routed["work"]}
                continue
            return_key = str((assignment.get("outputContract") or {}).get("returnResponsibility") or "")
            rejected = sum(
                1 for item in (foundation.get(work_ref)["data"]["responsibilityRouting"].get("executions") or {}).values()
                if item.get("assignmentRef") == assignment["assignmentRef"] and item.get("resultStatus") == "REJECTED"
            )
            max_returns = int((assignment.get("outputContract") or {}).get("maxReturns") or 2)
            if result["status"] == "REJECTED" and return_key and rejected <= max_returns:
                routing.route(
                    work_ref, signal="RETURN_OR_REVISION", responsibility_key=return_key,
                    result_refs=[f"task:{result['task_ref']}"], artifact_refs=result["artifact_refs"],
                    problem=result["problem"] or result["summary"],
                )
                continue
            return {"work": foundation.get(work_ref)}
        return {"work": foundation.get(work_ref), "continuation_pending": True}

    @router.get("/definition")
    def read_definition(
        company_id: str,
        scope_type: Literal["BUSINESS", "WORKSPACE"],
        scope_ref: str,
        workflow_key: str,
        workspace_id: str | None = Query(default=None),
    ):
        try:
            routing._validate_scope(company_id=company_id, scope_type=scope_type, scope_ref=scope_ref, workspace_id=workspace_id)
            return projection(company_id, workspace_id, scope_type, scope_ref, workflow_key)
        except (KeyError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/definitions/publish")
    def publish_definition(payload: PublishOperatingDefinitionIn):
        try:
            require_company(payload.company_id)
            keys = [item.responsibility_key.strip() for item in payload.roles]
            if len(keys) != len(set(keys)):
                raise ResponsibilityRoutingError("每个责任岗位必须唯一")
            assignment_refs = [item.assignment_ref for item in payload.roles if item.assignment_ref]
            if len(assignment_refs) != len(set(assignment_refs)):
                raise ResponsibilityRoutingError("每个责任岗位必须引用独立的责任安排")
            default_flow = payload.default_flow or [item.responsibility_key for item in payload.roles if not item.is_leader]
            if not default_flow or len(default_flow) != len(set(default_flow)) or not set(default_flow).issubset(keys):
                raise ResponsibilityRoutingError("默认流程必须引用唯一且已定义的责任岗位")
            # Validate the whole payload before mutating any Assignment.
            routing._validate_scope(
                company_id=payload.company_id, scope_type=payload.scope_type,
                scope_ref=payload.scope_ref, workspace_id=payload.workspace_id,
            )
            for item in payload.roles:
                routing._validate_employee(item.employee_ref, payload.company_id, payload.workspace_id)
                if item.assignment_ref:
                    current = foundation.get(item.assignment_ref)
                    if current["entity_type"] != "RESPONSIBILITY_ASSIGNMENT" or current["data"].get("scopeRef") != payload.scope_ref:
                        raise RuntimeScopeError("责任岗位不属于当前经营范围")
                if item.role_ref:
                    role = foundation.get(item.role_ref)
                    if role["entity_type"] != "ROLE_SLOT" or role["company_id"] != payload.company_id:
                        raise RuntimeScopeError("岗位不属于当前公司")

            assignment_refs = []
            for item in payload.roles:
                role_ref = item.role_ref
                if not role_ref:
                    role = foundation.create(
                        "ROLE_SLOT", company_id=payload.company_id, workspace_id=payload.workspace_id,
                        data={"role": item.role_name.strip(), "roleKey": item.responsibility_key.strip()},
                    )
                    role_ref = role["entity_id"]
                if item.assignment_ref:
                    assignment = routing.update_assignment(
                        item.assignment_ref, employee_ref=item.employee_ref,
                        responsibility=item.responsibility,
                        input_contract=item.input_contract, output_contract=item.output_contract,
                    )
                else:
                    assignment = routing.create_assignment(
                        company_id=payload.company_id, workspace_id=payload.workspace_id,
                        scope_type=payload.scope_type, scope_ref=payload.scope_ref,
                        role_ref=role_ref, employee_ref=item.employee_ref,
                        responsibility_key=item.responsibility_key,
                        responsibility=item.responsibility,
                        input_contract=item.input_contract, output_contract=item.output_contract,
                        is_leader=item.is_leader,
                    )
                assignment_refs.append(assignment["entity_id"])
            routing.publish_workflow(
                company_id=payload.company_id, workspace_id=payload.workspace_id,
                scope_type=payload.scope_type, scope_ref=payload.scope_ref,
                workflow_key=payload.workflow_key, assignment_refs=assignment_refs,
                default_flow=default_flow,
            )
            return projection(payload.company_id, payload.workspace_id, payload.scope_type, payload.scope_ref, payload.workflow_key)
        except (KeyError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/start")
    def start_work(work_ref: str, payload: StartOperatingWorkIn):
        try:
            if ((foundation.get(work_ref)["data"].get("responsibilityRouting") or {}).get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
                raise ResponsibilityRoutingError("Human Input blocks direct Work start")
            work = routing.start_work(
                work_ref, scope_type=payload.scope_type, scope_ref=payload.scope_ref,
                workflow_key=payload.workflow_key, initial_responsibility=payload.initial_responsibility,
            )
            return {"work": work}
        except (KeyError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/route")
    def route_work(work_ref: str, payload: RouteOperatingWorkIn):
        try:
            return routing.route(
                work_ref, signal=payload.signal, responsibility_key=payload.responsibility_key,
                result_refs=payload.result_refs, artifact_refs=payload.artifact_refs,
                evidence_refs=payload.evidence_refs, problem=payload.problem,
                interaction_key=payload.interaction_key, bounded_summary=payload.bounded_summary,
            )
        except (KeyError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/execute")
    async def execute_work(work_ref: str, limits: LimitedGeneralExecutionIn | None = None, max_executions: int = Query(default=16, ge=1, le=16)):
        try:
            work = foundation.get(work_ref)
            require_company(work["company_id"])
            if work["data"].get("cycleRef"):
                contract = work["data"].get("followupContract") or foundation.get(work["data"]["cycleRef"])["data"].get("contract") or {}
                if contract.get("modelSource"):
                    raise RuntimeScopeError("Writing Model Work executes only through its original chapter request")
                if contract.get("agentBinding"):
                    if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
                        raise RuntimeScopeError("只有当前公司所有者可以启动 Agent 工作。")
                    from ..company_execution_policy import CompanyExecutionPolicy
                    from ..conversation_service import ConversationService
                    snapshot = ConversationService(database).validate_agent_work_source(work)
                    original_route = work["data"].get("responsibilityRouting") or {}
                    if (original_route.get("currentAssignmentRef") != work["data"].get("responsibilityAssignmentRef")
                            or original_route.get("responsibilityHolderRef") != work["data"].get("holderEmployeeRef")
                            or snapshot["context"]["assignment_ref"] != work["data"].get("responsibilityAssignmentRef")
                            or snapshot["context"]["employee_ref"] != work["data"].get("holderEmployeeRef")):
                        raise RuntimeScopeError("原员工与责任关联已变化；不能自动切换执行者。")
                    has_leader_plan = assignment_for(work).get("isLeader") and any(
                        str(key).startswith("leader:plan:") for key in original_route.get("executions", {}))
                    if not has_leader_plan:
                        CompanyExecutionPolicy(database).require_unreserved_agent_work(work["company_id"], work_ref)
                    max_executions = 1
            route = work["data"].get("responsibilityRouting") or {}
            if (route.get("humanInput") or {}).get("state") not in {None, "CLOSED", "INVALIDATED"}:
                raise ResponsibilityRoutingError("Human Input requires the scoped original Work continuation")
            original_limits = read_general_limits(database, work_ref)
            if original_limits or limits is not None:
                require_company(work["company_id"])
                if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
                    raise RuntimeScopeError("Only the current Company owner may execute limited Work")
                if original_limits and limits is not None and limits.model_dump() != {k: original_limits[k] for k in ("max_prompt_bytes", "max_output_tokens")}:
                    raise RuntimeScopeError("Original execution limits cannot be replaced")
                if original_limits and route.get("status") == "COMPLETED":
                    return {"work": work, "execution_limits": original_limits}
                original_limits = arm_general_limits(database, work_ref, limits.model_dump() if limits is not None else None)
            ownership = general_command_owner(database, work_ref, execution_key(work, assignment_for(work), "responsibility"), employee_execution) if original_limits else nullcontext()
            with ownership:
                if route.get("status") == "WAITING" and route.get("lastAction") in {
                    "EMPLOYEE_RESULT_FAILED", "EMPLOYEE_RESULT_REJECTED", "EMPLOYEE_RESULT_PARTIAL",
                }:
                    routing.route(work_ref, signal="CONTINUE")
                result = await run_loop(work_ref, 1 if original_limits else max_executions)
            if original_limits:
                result["execution_limits"] = original_limits
            return result
        except ResponsibilityRoutingError as error:
            if str(error) == "Work has no active responsibility route":
                try:
                    work = foundation.get(work_ref)
                    require_company(work["company_id"])
                except (KeyError, RuntimeScopeError) as reread_error:
                    raise HTTPException(status_code=422, detail="原工作状态无法核验。") from reread_error
                if (work["data"].get("responsibilityRouting") or {}).get("status") == "CANCELLED":
                    return {"work": work, "execution_blocked": "原工作已请求停止；外部效果仍需核验。"}
            raise HTTPException(status_code=422, detail=str(error)) from error
        except (KeyError, ValueError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/human-input/{request_id}/continue")
    async def continue_human_input(work_ref: str, request_id: str, payload: ContinueHumanInputIn):
        try:
            work = foundation.get(work_ref)
            require_company(work["company_id"])
            general_delivery._human_work(work["company_id"], work["workspace_id"], work_ref)
            human = (work["data"].get("responsibilityRouting") or {}).get("humanInput") or {}
            if (human.get("requestId") == request_id
                and ((human.get("state") == "CLAIMED" and human.get("revision") == payload.revision + 1)
                     or (human.get("state") == "CLOSED" and human.get("revision") == payload.revision + 2))
                and (human.get("report") or {}).get("submissionId") == payload.submission_id):
                if (human.get("companyId") != work["company_id"]
                    or human.get("workspaceId") != work["workspace_id"]
                    or human.get("workRef") != work_ref or human.get("targetRef") != work_ref):
                    raise ResponsibilityRoutingError("Historical Human Input is outside the original Work scope")
                if human["state"] == "CLAIMED":
                    checked = routing.claim_human_input(
                        work["company_id"], work["workspace_id"], work_ref,
                        request_id=request_id, revision=payload.revision,
                        submission_id=payload.submission_id,
                    )
                    return {"work": checked["work"], "human_input_request": checked["request"],
                            "duplicate": True, "actionable": False}
                return {"work": work, "human_input_request": human,
                        "duplicate": True, "historical": True, "actionable": False}
            general_delivery.precheck_human_continuation(
                company_id=work["company_id"], workspace_id=work["workspace_id"],
                work_ref=work_ref, request_id=request_id, revision=payload.revision,
                submission_id=payload.submission_id,
            )
            claimed = routing.claim_human_input(
                work["company_id"], work["workspace_id"], work_ref,
                request_id=request_id, revision=payload.revision, submission_id=payload.submission_id,
            )
            result = await run_loop(work_ref, 1)
            result["human_input_request"] = claimed["request"]
            return result
        except GeneralWorkspaceGap as error:
            raise HTTPException(status_code=409, detail=error.payload) from error
        except GeneralHumanAuthorityGap as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except (ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/cancel")
    def cancel_work(work_ref: str, payload: CancelOperatingWorkIn):
        with _AGENT_STOP_SPAWN_LOCK:
            try:
                work = foundation.get(work_ref)
                route = work["data"].get("responsibilityRouting") or {}
                active = next(
                    (item for item in (route.get("executions") or {}).values() if item.get("status") == "RUNNING"),
                    None,
                )
                if active and active.get("taskRef"):
                    from ..evolution_event_log import EvolutionEventLog
                    from ..task_execution_control import TaskExecutionControlService
                    TaskExecutionControlService(database, EvolutionEventLog(database)).cancel(
                        active["taskRef"], payload.reason,
                    )
                return {"work": routing.cancel_work(work_ref, reason=payload.reason)}
            except (KeyError, ResponsibilityRoutingError, RuntimeScopeError, ValueError) as error:
                raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/works/{work_ref}/consult/{interaction_key}/complete")
    def complete_consult(work_ref: str, interaction_key: str, payload: CompleteConsultIn):
        try:
            return routing.complete_consult(
                work_ref, interaction_key=interaction_key, response=payload.response,
                result_refs=payload.result_refs, artifact_refs=payload.artifact_refs,
                evidence_refs=payload.evidence_refs,
            )
        except (KeyError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router
