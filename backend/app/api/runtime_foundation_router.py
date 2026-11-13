"""Tenant-scoped HTTP adapter for the persisted Runtime Foundation."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..analyst_authoring import AnalystAuthoring
from ..database import Database
from ..employee_execution_identity import EmployeeExecutionIdentity
from ..operating_intelligence import OperatingIntelligence
from ..organization_projection import read_organization_projection
from ..runtime import RuntimeFoundation, RuntimeScopeError, SimulationRuntime
from ..runtime.business_spine import CanonicalBusinessSpine
from ..runtime.execution_adapter import RuntimeExecutionAdapter, RuntimeExecutionError
from ..runtime.first_run_delivery import FirstGeneralWorkspaceDraft, FirstRunDelivery
from ..runtime.state_machine import ActorNotAllowedError, TransitionError
from ..runtime.workspace import WorkspaceRuntime
from ..tenant_context import TenantContext
from .shared_workspace_router import build_shared_workspace_router
from .team_operating_router import build_team_operating_router


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class FoundingRunIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner_ref: str = Field(min_length=1, max_length=128)
    intent_ref: str = Field(default="", max_length=256)
    org_version: str = Field(default="org-v1", max_length=64)
    blueprint_version: str = Field(default="", max_length=64)


class TransitionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target: str = Field(min_length=1, max_length=64)
    actor: str = Field(min_length=1, max_length=64)
    trigger: str = Field(min_length=1, max_length=128)
    reason: str = Field(default="", max_length=2000)
    evidenceRefs: list[str] = Field(default_factory=list)
    nextCheckAt: str | None = Field(default=None, max_length=64)
    context: dict[str, str | bool | int | float | None] = Field(default_factory=dict)


class MaterializeCompanyIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    ceo_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    name: str = Field(min_length=1, max_length=120)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value or any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise ValueError("unsafe company name")
        return value


class MaterializeFirstGeneralWorkspaceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    ceo_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    company_name: str = Field(min_length=1, max_length=120)
    department_name: str = Field(default="业务部", min_length=1, max_length=120)
    business_name: str = Field(min_length=1, max_length=120)
    goal: str = Field(min_length=1, max_length=2000)
    positioning: str = Field(default="", max_length=2000)
    workspace_name: str = Field(min_length=1, max_length=120)
    intent_summary: str = Field(default="", max_length=2000)
    recommendation_reason: str = Field(default="", max_length=2000)
    template_match_status: str = Field(default="NO_VERIFIED_MATCH", pattern=r"^NO_VERIFIED_MATCH$")
    blueprint: dict[str, Any] = Field(default_factory=dict)


class WorkspaceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    business_ref: str = Field(min_length=1, max_length=128)
    business_type: str = Field(min_length=2, max_length=3)
    name: str = Field(min_length=1, max_length=120)
    blueprint_version: str = Field(min_length=1, max_length=64)
    blueprint: dict[str, Any]
    workspace_id: str | None = Field(default=None, max_length=128)
    change_kind: str | None = Field(default=None, max_length=64)
    change_reason: str = Field(default="", max_length=2000)


class BusinessWithFirstWorkspaceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    department_id: str = Field(min_length=1, max_length=128)
    business_id: str | None = Field(default=None, max_length=128)
    name: str = Field(min_length=1, max_length=120)
    goal: str = Field(default="", max_length=2000)
    positioning: str = Field(default="", max_length=2000)
    workspace_name: str = Field(min_length=1, max_length=120)
    business_type: str = Field(min_length=2, max_length=3)
    blueprint_version: str = Field(min_length=1, max_length=64)
    blueprint: dict[str, Any]


class LegacyWorkspaceQuarantineIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2000)
    owner: str = Field(min_length=1, max_length=128)


class CycleIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    owner_ref: str = Field(min_length=1, max_length=128)
    outcome_ref: str = Field(min_length=1, max_length=256)
    intent_ref: str = Field(min_length=1, max_length=256)
    blueprint_version: str = Field(min_length=1, max_length=64)
    execution_ref: str | None = Field(default=None, max_length=256)
    project_ref: str | None = Field(default=None, max_length=128)
    work_item_title: str = Field(default="", max_length=240)
    instruction: str = Field(default="", max_length=4000)
    resource_refs: list[str] = Field(default_factory=list, max_length=32)
    test_command: list[str] = Field(default_factory=list, max_length=32)
    requested_access_intent: str = Field(
        default="AUTO_WITHIN_BOUNDARY",
        pattern=r"^(ASK_WHEN_NEEDED|AUTO_WITHIN_BOUNDARY|REQUEST_WIDEST_NATIVE_ACCESS)$",
    )
    evidence_refs: list[str] = Field(default_factory=list)
    next_check_at: str | None = Field(default=None, max_length=64)


class ContentItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    owner_ref: str = Field(min_length=1, max_length=128)
    outcome_ref: str = Field(min_length=1, max_length=256)
    intent_ref: str = Field(min_length=1, max_length=256)
    blueprint_version: str = Field(min_length=1, max_length=64)
    platform: str = Field(min_length=2, max_length=3)
    platform_variant: str = Field(min_length=1, max_length=128)
    payload_ref: str = Field(min_length=1, max_length=256)
    author: str = Field(min_length=1, max_length=128)
    constraints_check: str = Field(min_length=1, max_length=128)
    execution_ref: str | None = Field(default=None, max_length=256)
    next_check_at: str | None = Field(default=None, max_length=64)
    title: str = Field(default="", max_length=240)
    body: str = Field(default="", max_length=20000)
    tags: list[str] = Field(default_factory=list, max_length=12)
    cover_ref: str = Field(default="", max_length=512)
    scheduled_for: str | None = Field(default=None, max_length=64)

    format: str = Field(default="", pattern="^(|graphic)$")
    topic: str = Field(default="", max_length=1000)
    audience: str = Field(default="", max_length=1000)
    target_account_refs: list[str] = Field(default_factory=list, max_length=8)
    references: list[dict] = Field(default_factory=list, max_length=8)
    request_id: str = Field(default="", max_length=128)
    start_draft: bool = False


class ContentVersionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    platform_variant: str = Field(min_length=1, max_length=128)
    payload_ref: str = Field(min_length=1, max_length=256)
    author: str = Field(min_length=1, max_length=128)
    constraints_check: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=240)
    body: str = Field(default="", max_length=20000)
    tags: list[str] = Field(default_factory=list, max_length=12)
    cover_ref: str = Field(default="", max_length=512)
    scheduled_for: str | None = Field(default=None, max_length=64)

    expected_version_ref: str | None = Field(default=None, max_length=256)
    request_id: str = Field(default="", max_length=128)
    topic: str | None = Field(default=None, max_length=1000)
    audience: str | None = Field(default=None, max_length=1000)
    references: list[dict] | None = Field(default=None, max_length=8)


class ContentIdeaActionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)


class ContentWorkContextIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    responsibility_employee_ref: str | None = Field(default=None, max_length=128)
    current_executor_ref: str | None = Field(default=None, max_length=128)
    next_responsibility_employee_ref: str | None = Field(default=None, max_length=128)
    activity: str = Field(default="", max_length=240)
    status: str = Field(default="idle", pattern=r"^(working|waiting|needs_ceo|completed|failed|idle)$")
    system_activity: dict[str, str] | None = None


class ContentDecisionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    choice: str = Field(min_length=1, pattern=r"^(APPROVE|RETURN|DEFER)$")
    reason: str = Field(min_length=1, max_length=2000)


class ContentExecutionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)


class WorkspaceSimulationIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    subject_id: str | None = Field(default=None, max_length=128)
    scenario_id: str = Field(min_length=1, max_length=64)
    blueprint_version: str = Field(min_length=1, max_length=64)
    participants: list[str] = Field(default_factory=list)
    input_refs: list[str] = Field(default_factory=list)


class SimulationTransitionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    target: str = Field(min_length=1, max_length=32)
    trigger: str = Field(min_length=1, max_length=128)
    reason: str = Field(default="", max_length=2000)


class SimulationReviewIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    decision: str = Field(min_length=1, max_length=32)
    evidence_refs: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=2000)


class CapabilitySupplySelectionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_ref: str = Field(min_length=1, max_length=128, pattern=r"^requirement:[a-z0-9][a-z0-9-]{1,63}$")
    source: str = Field(min_length=1, max_length=32, pattern=r"^(official|tenant_private)$")
    capability_type: str = Field(min_length=1, max_length=32, pattern=r"^[a-z][a-z0-9_-]*$")
    capability_id: str = Field(min_length=1, max_length=256)


class CapabilitySupplyReviewIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    selections: list[CapabilitySupplySelectionIn] = Field(min_length=1, max_length=64)


class StaffingDecisionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    choice: str = Field(min_length=1, max_length=16, pattern=r"^(APPROVE|MODIFY|REJECT)$")
    reason: str = Field(default="", max_length=2000)


class StaffingRollbackIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2000)


class OperatingCycleActionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2000)


class ArtifactReviewRequestIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    reviewer_employee_ref: str = Field(min_length=1, max_length=128)


class ArtifactRevisionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    request_ref: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2000)


class ResponsibilityHandoffIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    target_employee_ref: str = Field(min_length=1, max_length=128)
    responsibility_summary: str = Field(min_length=1, max_length=1000)
    reason: str = Field(min_length=1, max_length=2000)
    next_check_at: str | None = Field(default=None, max_length=64)


class ResponsibilityHandoffResponseIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    decision: str = Field(min_length=1, max_length=16, pattern=r"^(ACKNOWLEDGE|RETURN|REJECT)$")
    reason: str = Field(min_length=1, max_length=2000)


class ProviderHandoffAckIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    task_ref: str = Field(min_length=1, max_length=128)
    session_ref: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2000)


class DecisionFactIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str = Field(min_length=1, max_length=2000)
    provenance: str = Field(min_length=3, max_length=8, pattern=r"^(FACT|POLICY|EVIDENCE|EST|UNK)$")


class RDDecisionOptionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    option_id: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=240)
    impact: DecisionFactIn
    risk: DecisionFactIn
    cost: DecisionFactIn
    continuation_instruction: str = Field(min_length=1, max_length=4000)
    resource_refs: list[str] = Field(min_length=1, max_length=32)
    test_command: list[str] = Field(min_length=1, max_length=32)


class RDDecisionPacketIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    decision_key: str = Field(min_length=1, max_length=128)
    event: str = Field(min_length=1, max_length=2000)
    cannot_decide_reason: str = Field(min_length=1, max_length=2000)
    options: list[RDDecisionOptionIn] = Field(min_length=2, max_length=4)
    recommendation_option_id: str = Field(min_length=1, max_length=64)
    recommendation_provenance: str = Field(min_length=3, max_length=8, pattern=r"^(FACT|POLICY|EVIDENCE|EST|UNK)$")
    recommendation_reason: DecisionFactIn
    ceo_choice_prompt: str = Field(min_length=1, max_length=1000)
    continuation_plan: str = Field(min_length=1, max_length=2000)


class RDDecisionChoiceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    choice: str = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1, max_length=2000)
    next_check_at: str | None = Field(default=None, max_length=64)


class OperatingCycleReviewIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    decision: str = Field(min_length=1, max_length=16, pattern=r"^(ACCEPT|REJECT)$")
    evidence_refs: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1, max_length=2000)


class OperatingCycleCloseIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    choice: str = Field(min_length=1, max_length=16, pattern=r"^(CONTINUE|ADJUST|PAUSE)$")
    reason: str = Field(min_length=1, max_length=2000)


class ManualReceiptIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    source: str = Field(default="CEO_MANUAL", min_length=1, max_length=32)
    status: str = Field(default="RECEIVED", min_length=1, max_length=32)
    approved_version_id: str = Field(min_length=1, max_length=128)
    published_version_id: str = Field(min_length=1, max_length=128)
    recorded_by: str = Field(min_length=1, max_length=128)
    run_ref: str = Field(default="", max_length=256)


class ManualInteractionIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    source: str = Field(default="CEO_MANUAL", min_length=1, max_length=32)
    external_id: str = Field(min_length=1, max_length=256)
    intent: str = Field(min_length=1, max_length=128)
    sensitivity: str = Field(min_length=1, max_length=64)
    reply_policy: str = Field(min_length=1, max_length=128)
    next_check_at: str | None = Field(default=None, max_length=64)


class OperatingReportAuthoringIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    business_id: str | None = Field(default=None, min_length=1, max_length=128)
    days: int = Field(default=30)


_SAFE_CONTEXT_KEYS = frozenset({"acceptanceId", "responseVersion", "externalReceipt", "verificationStatus"})


def build_runtime_foundation_router(database: Database, execution_executor=None, task_runner=None) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/runtime/foundation", tags=["runtime-foundation"])
    router.include_router(build_shared_workspace_router(database))
    router.include_router(build_team_operating_router(database, execution_executor))
    foundation = RuntimeFoundation(database)
    simulations = SimulationRuntime(database)
    workspaces = WorkspaceRuntime(database)
    businesses = CanonicalBusinessSpine(database)
    operating_intelligence = OperatingIntelligence(database)
    analyst_authoring = AnalystAuthoring(database)
    first_run_delivery = FirstRunDelivery(database)
    employee_identity = EmployeeExecutionIdentity(database)
    execution = RuntimeExecutionAdapter(foundation, simulations, execution_executor)

    @router.on_event("startup")
    def reconcile_interrupted_rd_executions() -> None:
        workspaces.reconcile_interrupted_rd_executions()

    async def finish_rd_execution(
        request: dict[str, Any], tenant_id: str, identity: dict[str, str],
    ) -> None:
        with TenantContext.scope(
            tenant_id,
            subject_id=identity.get("subject_id", ""),
            company_id=identity.get("company_id", ""),
            ceo_id=identity.get("ceo_id", ""),
            role=identity.get("role", ""),
            membership_status=identity.get("membership_status", ""),
            request_id=identity.get("request_id", ""),
        ):
            try:
                result = await execution.run_bound(request)
            except RuntimeExecutionError as error:
                workspaces.record_operating_cycle_failure(
                    company_id=request["company_id"], workspace_id=request["workspace_id"],
                    cycle_id=request["cycle_id"], code=error.code,
                )
                return
            status = str(result.get("status") or "").lower()
            if status not in {"success", "succeeded", "completed"}:
                workspaces.record_operating_cycle_failure(
                    company_id=request["company_id"], workspace_id=request["workspace_id"],
                    cycle_id=request["cycle_id"], code=status or "execution_failed",
                    summary=str(result.get("error") or result.get("output") or ""), result=result,
                )
                return
            workspaces.record_operating_cycle_execution(
                company_id=request["company_id"], workspace_id=request["workspace_id"],
                cycle_id=request["cycle_id"], result=result,
            )

    async def finish_rd_artifact_review(
        request: dict[str, Any], tenant_id: str, identity: dict[str, str], request_ref: str,
    ) -> None:
        with TenantContext.scope(
            tenant_id,
            subject_id=identity.get("subject_id", ""),
            company_id=identity.get("company_id", ""),
            ceo_id=identity.get("ceo_id", ""),
            role=identity.get("role", ""),
            membership_status=identity.get("membership_status", ""),
            request_id=identity.get("request_id", ""),
        ):
            try:
                result = await execution.run_bound(request)
            except RuntimeExecutionError as error:
                workspaces.record_artifact_review_failure(
                    company_id=request["company_id"], workspace_id=request["workspace_id"],
                    cycle_id=request["cycle_id"], request_ref=request_ref, code=error.code,
                )
                return
            status = str(result.get("status") or "").lower()
            if status not in {"success", "succeeded", "completed"}:
                workspaces.record_artifact_review_failure(
                    company_id=request["company_id"], workspace_id=request["workspace_id"],
                    cycle_id=request["cycle_id"], request_ref=request_ref,
                    code=status or "review_execution_failed",
                    summary=str(result.get("error") or result.get("output") or ""), result=result,
                )
                return
            workspaces.record_artifact_review_result(
                company_id=request["company_id"], workspace_id=request["workspace_id"],
                cycle_id=request["cycle_id"], request_ref=request_ref, result=result,
            )

    def require_ceo(actor: str = "CEO") -> None:
        if actor != "CEO" or TenantContext.current_identity().get("role") not in {"owner", "ceo", "test"}:
            raise ActorNotAllowedError("runtime API only accepts explicit CEO commands")

    def require_ceo_identity(ceo_id: str) -> None:
        require_ceo()
        if not TenantContext.current_identity().get("ceo_id") or TenantContext.current_identity()["ceo_id"] != ceo_id:
            raise RuntimeScopeError("CEO identity does not match the current command")

    def require_company_identity(company_id: str) -> None:
        identity_company = TenantContext.current_identity().get("company_id")
        if identity_company and identity_company != company_id:
            raise RuntimeScopeError("Company identity does not match the current command")

    def safe(call: Callable[[], Any]) -> Any:
        try:
            return call()
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except ActorNotAllowedError as error:
            raise HTTPException(status_code=403, detail="当前操作者无权执行该状态转换") from error
        except TransitionError as error:
            raise HTTPException(status_code=409, detail="当前状态不允许该操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error
        except Exception as error:
            raise HTTPException(status_code=500, detail="Runtime 操作失败，请稍后重试") from error

    @router.get("/companies")
    def list_runtime_companies() -> dict[str, Any]:
        return safe(lambda: {
            "tenant_id": foundation.tenant_id,
            "companies": _runtime_company_collection(database, foundation),
        })

    @router.get("/companies/{company_id}")
    def get_company_snapshot(company_id: str) -> dict[str, Any]:
        return safe(lambda: _company_snapshot(database, foundation, company_id))

    @router.get("/companies/{company_id}/businesses")
    def list_canonical_businesses(company_id: str) -> dict[str, Any]:
        return safe(lambda: {"company_id": company_id, "businesses": businesses.list_businesses(company_id)})

    @router.get("/companies/{company_id}/organization")
    def get_organization_projection(company_id: str) -> dict[str, Any]:
        return safe(lambda: read_organization_projection(database, businesses, company_id))

    @router.get("/companies/{company_id}/operating-intelligence")
    def get_operating_intelligence(
        company_id: str, days: int = 30, business_id: str | None = None,
    ) -> dict[str, Any]:
        return safe(lambda: operating_intelligence.read(company_id, days=days, business_id=business_id))

    @router.post("/companies/{company_id}/operating-intelligence/reports/{artifact_id}/decision")
    def submit_operating_report_decision(company_id: str, artifact_id: str) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo()
            require_company_identity(company_id)
            return _runtime_object_projection(
                operating_intelligence.submit_report_decision(company_id, artifact_id)
            )

        return safe(command)

    @router.post("/companies/{company_id}/operating-intelligence/reports")
    def author_operating_analysis_report(
        company_id: str,
        payload: OperatingReportAuthoringIn,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    ) -> dict[str, Any]:
        if task_runner is None:
            raise HTTPException(status_code=503, detail="经营分析报告撰写执行底座未接线")

        def command() -> dict[str, Any]:
            require_ceo()
            require_company_identity(company_id)
            return analyst_authoring.author_report(
                company_id,
                business_id=payload.business_id,
                days=payload.days,
                idempotency_key=idempotency_key,
                task_runner=task_runner,
            )

        try:
            return command()
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except ActorNotAllowedError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(status_code=500, detail="Runtime 操作失败，请稍后重试") from error

    @router.get("/companies/{company_id}/businesses/{business_id}")
    def get_canonical_business(company_id: str, business_id: str) -> dict[str, Any]:
        return safe(lambda: businesses.get_business(company_id, business_id))

    @router.post("/companies/{company_id}/businesses", status_code=201)
    def create_canonical_business(company_id: str, payload: BusinessWithFirstWorkspaceIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            require_company_identity(company_id)
            return businesses.create_draft_with_first_workspace(
                company_id=company_id, department_id=payload.department_id,
                business_id=payload.business_id, name=payload.name, goal=payload.goal,
                positioning=payload.positioning, workspace_name=payload.workspace_name,
                business_type=payload.business_type, blueprint_version=payload.blueprint_version,
                blueprint=payload.blueprint,
            )

        return safe(command)

    @router.get("/workspaces/{workspace_id}/parent-path")
    def get_workspace_parent_path(workspace_id: str) -> dict[str, Any]:
        return safe(lambda: businesses.resolve_workspace_parent(workspace_id))

    @router.post("/workspaces/{workspace_id}/business-relation/quarantine")
    def quarantine_workspace_business_relation(
        workspace_id: str, payload: LegacyWorkspaceQuarantineIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            return businesses.quarantine_legacy_workspace(
                workspace_id, reason=payload.reason, owner=payload.owner,
            )

        return safe(command)

    @router.post("/companies/{company_id}/workspaces", status_code=201)
    def create_or_revise_workspace(company_id: str, payload: WorkspaceIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            require_company_identity(company_id)
            if payload.workspace_id:
                if not payload.change_kind or not payload.change_reason.strip():
                    raise ValueError("blueprint revision requires change_kind and change_reason")
                current = workspaces.get_workspace(company_id, payload.workspace_id)["workspace"]
                if (
                    payload.business_ref != current["business_id"]
                    or payload.business_type.upper() != current["business_type"]
                    or payload.name.strip() != current["name"]
                ):
                    raise ValueError("blueprint revision cannot change Workspace identity")
                return _workspace_projection(workspaces.revise_blueprint(
                    company_id=company_id,
                    workspace_id=payload.workspace_id,
                    blueprint_version=payload.blueprint_version,
                    blueprint=payload.blueprint,
                    change_kind=payload.change_kind,
                    change_reason=payload.change_reason.strip(),
                ))
            return _workspace_projection(workspaces.create_workspace(
                company_id=company_id,
                business_ref=payload.business_ref,
                business_type=payload.business_type,
                name=payload.name.strip(),
                blueprint_version=payload.blueprint_version,
                blueprint=payload.blueprint,
            ))

        return safe(command)

    @router.get("/companies/{company_id}/workspaces/{workspace_id}")
    def get_workspace(company_id: str, workspace_id: str) -> dict[str, Any]:
        def query() -> dict[str, Any]:
            require_company_identity(company_id)
            return _workspace_projection(workspaces.get_workspace(company_id, workspace_id))

        return safe(query)

    @router.post("/workspaces/{workspace_id}/cycles", status_code=201)
    def create_cycle(workspace_id: str, payload: CycleIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.create_cycle(
                company_id=workspace["company_id"],
                workspace_id=workspace_id,
                blueprint_version=payload.blueprint_version,
                owner_ref=payload.owner_ref,
                outcome_ref=payload.outcome_ref,
                intent_ref=payload.intent_ref,
                execution_ref=payload.execution_ref,
                project_ref=payload.project_ref,
                work_item_title=payload.work_item_title,
                instruction=payload.instruction,
                resource_refs=payload.resource_refs,
                test_command=payload.test_command,
                requested_access_intent=payload.requested_access_intent,
                evidence_refs=payload.evidence_refs,
                next_check_at=payload.next_check_at,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/start")
    def start_operating_cycle(workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.start_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/resume")
    def resume_operating_cycle(workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.resume_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/execute")
    async def execute_operating_cycle(
        workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn,
        background_tasks: BackgroundTasks,
    ) -> Any:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            cycle = workspaces.get_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, states={"RUNNING"},
            )
            request = {
                "company_id": workspace["company_id"],
                "workspace_id": workspace_id,
                "cycle_id": cycle_id,
                "blueprint_version": cycle["blueprint_version"],
                "execution_ref": cycle["execution_ref"],
                "subject_id": cycle_id,
                "subject": {
                    "entity_type": "CYCLE",
                    "owner_ref": cycle["owner_ref"],
                    "data": cycle["data"],
                },
            }
            if cycle["execution_ref"] == "rd_task:auto":
                if cycle["data"].get("executionStatus") == "RUNNING":
                    return JSONResponse(_runtime_object_projection(cycle), status_code=202)
                try:
                    cycle = workspaces.begin_operating_cycle_execution(
                        company_id=workspace["company_id"], workspace_id=workspace_id,
                        cycle_id=cycle_id,
                    )
                except TransitionError:
                    cycle = workspaces.get_operating_cycle(
                        company_id=workspace["company_id"], workspace_id=workspace_id,
                        cycle_id=cycle_id, states={"RUNNING"},
                    )
                    if cycle["data"].get("executionStatus") != "RUNNING":
                        raise
                    return JSONResponse(_runtime_object_projection(cycle), status_code=202)
                request["subject"]["data"] = cycle["data"]
                background_tasks.add_task(
                    finish_rd_execution, request, TenantContext.current_tenant_id(),
                    TenantContext.current_identity(),
                )
                return JSONResponse(_runtime_object_projection(cycle), status_code=202)
            try:
                result = await execution.run_bound(request)
            except RuntimeExecutionError as error:
                if error.code == "execution_unavailable":
                    raise
                return _runtime_object_projection(workspaces.record_operating_cycle_failure(
                    company_id=workspace["company_id"], workspace_id=workspace_id,
                    cycle_id=cycle_id, code=error.code,
                ))
            status = str(result.get("status") or "").lower()
            if status not in {"success", "succeeded", "completed"}:
                return _runtime_object_projection(workspaces.record_operating_cycle_failure(
                    company_id=workspace["company_id"], workspace_id=workspace_id,
                    cycle_id=cycle_id, code=status or "execution_failed",
                    summary=str(result.get("error") or result.get("output") or ""),
                    result=result,
                ))
            return _runtime_object_projection(workspaces.record_operating_cycle_execution(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, result=result,
            ))
        except RuntimeExecutionError as error:
            status = 503 if error.code == "execution_unavailable" else 409
            raise HTTPException(status_code=status, detail=error.code) from error
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许执行这个操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/artifact-review", status_code=201)
    def create_artifact_review(
        workspace_id: str, cycle_id: str, payload: ArtifactReviewRequestIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.create_artifact_review_request(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, reviewer_employee_ref=payload.reviewer_employee_ref,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/artifact-review/execute")
    async def execute_artifact_review(
        workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn,
        background_tasks: BackgroundTasks,
    ) -> Any:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            cycle = workspaces.get_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, states={"RUNNING"},
            )
            review = cycle["data"].get("artifactReview") or {}
            if review.get("status") == "REVIEWING":
                return JSONResponse(_runtime_object_projection(cycle), status_code=202)
            cycle = workspaces.begin_artifact_review_execution(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
            )
            review = cycle["data"]["artifactReview"]
            request = {
                "company_id": workspace["company_id"],
                "workspace_id": workspace_id,
                "cycle_id": cycle_id,
                "blueprint_version": cycle["blueprint_version"],
                "execution_ref": "rd_task:auto",
                "subject_id": cycle_id,
                "subject": {
                    "entity_type": "CYCLE",
                    "owner_ref": cycle["owner_ref"],
                    "data": cycle["data"] | {"artifactReviewExecution": review},
                },
            }
            background_tasks.add_task(
                finish_rd_artifact_review, request, TenantContext.current_tenant_id(),
                TenantContext.current_identity(), review["requestRef"],
            )
            return JSONResponse(_runtime_object_projection(cycle), status_code=202)
        except RuntimeExecutionError as error:
            status = 503 if error.code == "execution_unavailable" else 409
            raise HTTPException(status_code=status, detail=error.code) from error
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许执行这个操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/artifact-review/revise")
    async def revise_after_artifact_review(
        workspace_id: str, cycle_id: str, payload: ArtifactRevisionIn,
        background_tasks: BackgroundTasks,
    ) -> Any:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            cycle = workspaces.prepare_rd_artifact_revision(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, request_ref=payload.request_ref, reason=payload.reason,
            )
            execution_status = cycle["data"].get("executionStatus")
            if execution_status == "RUNNING":
                return JSONResponse(_runtime_object_projection(cycle), status_code=202)
            if execution_status != "READY":
                return _runtime_object_projection(cycle)
            cycle = workspaces.begin_operating_cycle_execution(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
            )
            request = {
                "company_id": workspace["company_id"],
                "workspace_id": workspace_id,
                "cycle_id": cycle_id,
                "blueprint_version": cycle["blueprint_version"],
                "execution_ref": cycle["execution_ref"],
                "subject_id": cycle_id,
                "subject": {
                    "entity_type": "CYCLE",
                    "owner_ref": cycle["owner_ref"],
                    "data": cycle["data"],
                },
            }
            background_tasks.add_task(
                finish_rd_execution, request, TenantContext.current_tenant_id(),
                TenantContext.current_identity(),
            )
            return JSONResponse(_runtime_object_projection(cycle), status_code=202)
        except RuntimeExecutionError as error:
            status = 503 if error.code == "execution_unavailable" else 409
            raise HTTPException(status_code=status, detail=error.code) from error
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许执行这个操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/responsibility-handoff", status_code=201)
    def create_responsibility_handoff(
        workspace_id: str, cycle_id: str, payload: ResponsibilityHandoffIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.create_rd_responsibility_handoff(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, target_employee_ref=payload.target_employee_ref,
                responsibility_summary=payload.responsibility_summary, reason=payload.reason,
                next_check_at=payload.next_check_at,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/responsibility-handoff/send")
    def send_responsibility_handoff(
        workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.send_rd_responsibility_handoff(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/responsibility-handoff/respond")
    def respond_responsibility_handoff(
        workspace_id: str, cycle_id: str, payload: ResponsibilityHandoffResponseIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.respond_rd_responsibility_handoff(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
                decision=payload.decision, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/responsibility-handoff/provider-ack")
    def acknowledge_responsibility_handoff_from_provider(
        workspace_id: str, cycle_id: str, payload: ProviderHandoffAckIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            cycle = workspaces.get_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, states={"RUNNING"},
            )
            handoff = cycle["data"].get("responsibilityHandoff") or {}
            existing_ack = handoff.get("providerAck") or {}
            existing_provenance = existing_ack.get("execution_provenance") or {}
            if (
                handoff.get("status") == "COMPLETED"
                and existing_ack.get("verification_status") == "VERIFIED"
                and existing_provenance.get("task_ref") == payload.task_ref
                and existing_provenance.get("session_ref") == payload.session_ref
            ):
                return _runtime_object_projection(cycle)
            target_employee_ref = str(handoff.get("toEmployeeRef") or "")
            verified_ack = employee_identity.verify_handoff_ack(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_ref=cycle_id, target_employee_ref=target_employee_ref,
                task_ref=payload.task_ref, session_ref=payload.session_ref,
            )
            return _runtime_object_projection(workspaces.respond_rd_responsibility_handoff(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, decision="ACKNOWLEDGE", reason=payload.reason,
                provider_ack=verified_ack,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/rd-decision", status_code=201)
    def create_rd_decision(
        workspace_id: str, cycle_id: str, payload: RDDecisionPacketIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.create_rd_decision_packet(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
                packet={
                    "decisionKey": payload.decision_key,
                    "event": payload.event,
                    "cannotDecideReason": payload.cannot_decide_reason,
                    "options": [{
                        "optionId": item.option_id,
                        "label": item.label,
                        "impact": item.impact.model_dump(),
                        "risk": item.risk.model_dump(),
                        "cost": item.cost.model_dump(),
                        "continuationInstruction": item.continuation_instruction,
                        "resourceRefs": item.resource_refs,
                        "testCommand": item.test_command,
                    } for item in payload.options],
                    "recommendation": {
                        "optionId": payload.recommendation_option_id,
                        "provenance": payload.recommendation_provenance,
                    },
                    "recommendationReason": payload.recommendation_reason.model_dump(),
                    "ceoChoicePrompt": payload.ceo_choice_prompt,
                    "continuationPlan": payload.continuation_plan,
                },
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/rd-decision/review")
    def review_rd_decision(
        workspace_id: str, cycle_id: str, payload: OperatingCycleActionIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.review_rd_decision_packet(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/rd-decision/choose")
    async def choose_rd_decision(
        workspace_id: str, cycle_id: str, payload: RDDecisionChoiceIn,
        background_tasks: BackgroundTasks,
    ) -> Any:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            cycle = workspaces.apply_rd_decision_choice(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
                choice=payload.choice, reason=payload.reason, next_check_at=payload.next_check_at,
            )
            if payload.choice == "DEFER" or cycle["data"].get("executionStatus") != "READY":
                return _runtime_object_projection(cycle)
            cycle = workspaces.begin_operating_cycle_execution(
                company_id=workspace["company_id"], workspace_id=workspace_id, cycle_id=cycle_id,
            )
            request = {
                "company_id": workspace["company_id"],
                "workspace_id": workspace_id,
                "cycle_id": cycle_id,
                "blueprint_version": cycle["blueprint_version"],
                "execution_ref": cycle["execution_ref"],
                "subject_id": cycle_id,
                "subject": {
                    "entity_type": "CYCLE",
                    "owner_ref": cycle["owner_ref"],
                    "data": cycle["data"],
                },
            }
            background_tasks.add_task(
                finish_rd_execution, request, TenantContext.current_tenant_id(),
                TenantContext.current_identity(),
            )
            return JSONResponse(_runtime_object_projection(cycle), status_code=202)
        except RuntimeExecutionError as error:
            status = 503 if error.code == "execution_unavailable" else 409
            raise HTTPException(status_code=status, detail=error.code) from error
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许执行这个操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/review")
    def review_operating_cycle(workspace_id: str, cycle_id: str, payload: OperatingCycleReviewIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.review_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, decision=payload.decision,
                evidence_refs=payload.evidence_refs, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/cycles/{cycle_id}/close")
    def close_operating_cycle(workspace_id: str, cycle_id: str, payload: OperatingCycleCloseIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.close_operating_cycle(
                company_id=workspace["company_id"], workspace_id=workspace_id,
                cycle_id=cycle_id, choice=payload.choice, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items", status_code=201)
    def create_content_item(workspace_id: str, payload: ContentItemIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            if payload.format == "graphic":
                raise ValueError("Use the scoped graphic command with explicit canonical references")
            content, version = workspaces.create_content_item(
                company_id=workspace["company_id"],
                workspace_id=workspace_id,
                blueprint_version=payload.blueprint_version,
                platform=payload.platform,
                owner_ref=payload.owner_ref,
                outcome_ref=payload.outcome_ref,
                intent_ref=payload.intent_ref,
                platform_variant=payload.platform_variant,
                payload_ref=payload.payload_ref,
                author=payload.author,
                constraints_check=payload.constraints_check,
                execution_ref=payload.execution_ref,
                next_check_at=payload.next_check_at,
                title=payload.title,
                body=payload.body,
                tags=payload.tags,
                cover_ref=payload.cover_ref,
                scheduled_for=payload.scheduled_for,
            )
            return {
                "content_item": _runtime_object_projection(content),
                "content_version": _runtime_object_projection(version),
            }

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/accept-idea")
    def accept_content_idea(workspace_id: str, content_id: str, payload: ContentIdeaActionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.accept_content_idea(
                company_id=workspace["company_id"], workspace_id=workspace_id, content_id=content_id,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/work-context")
    def set_content_work_context(workspace_id: str, content_id: str, payload: ContentWorkContextIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.set_content_work_context(
                company_id=workspace["company_id"], workspace_id=workspace_id, content_id=content_id,
                responsibility_employee_ref=payload.responsibility_employee_ref,
                current_executor_ref=payload.current_executor_ref,
                next_responsibility_employee_ref=payload.next_responsibility_employee_ref,
                activity=payload.activity, status=payload.status, system_activity=payload.system_activity,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/decision")
    def decide_content_review(workspace_id: str, content_id: str, payload: ContentDecisionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            return _runtime_object_projection(workspaces.decide_content_review(
                company_id=workspace["company_id"], workspace_id=workspace_id, content_id=content_id,
                choice=payload.choice, reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/execute")
    async def execute_content_stage(workspace_id: str, content_id: str, payload: ContentExecutionIn) -> dict[str, Any]:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            content = foundation.get(content_id)
            if content["company_id"] != workspace["company_id"] or content["workspace_id"] != workspace_id:
                raise RuntimeScopeError("ContentItem is outside the current workspace")
            if content["data"].get("format") == "graphic":
                raise ValueError("Graphic suggestions require the shared selected execution command")
            request = {
                "company_id": workspace["company_id"], "workspace_id": workspace_id,
                "content_id": content_id, "blueprint_version": content["blueprint_version"],
                "execution_ref": content["execution_ref"], "subject_id": content_id,
                "subject": {"entity_type": "CONTENT_ITEM", "owner_ref": content["owner_ref"], "data": content["data"]},
            }
            try:
                result = await execution.run_bound(request)
            except RuntimeExecutionError as error:
                return _runtime_object_projection(workspaces.record_content_execution_failure(
                    company_id=workspace["company_id"], workspace_id=workspace_id,
                    content_id=content_id, code=error.code,
                ))
            status = str(result.get("status") or "").lower()
            if status not in {"success", "succeeded", "completed"}:
                return _runtime_object_projection(workspaces.record_content_execution_failure(
                    company_id=workspace["company_id"], workspace_id=workspace_id, content_id=content_id,
                    code=status or "execution_failed", summary=str(result.get("error") or result.get("output") or ""),
                ))
            return _runtime_object_projection(workspaces.record_content_execution_completion(
                company_id=workspace["company_id"], workspace_id=workspace_id, content_id=content_id, result=result,
            ))
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许该操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/versions", status_code=201)
    def add_content_version(workspace_id: str, content_id: str, payload: ContentVersionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            content = foundation.get(content_id)
            if content["company_id"] != workspace["company_id"] or content["workspace_id"] != workspace_id:
                raise RuntimeScopeError("ContentItem is outside the current workspace")
            if content["data"].get("format") == "graphic":
                raise ValueError("Use the scoped graphic save command with atomic expected version")
            return _runtime_object_projection(workspaces.add_content_version(
                content_id,
                platform_variant=payload.platform_variant,
                payload_ref=payload.payload_ref,
                author=payload.author,
                constraints_check=payload.constraints_check,
                title=payload.title,
                body=payload.body,
                tags=payload.tags,
                cover_ref=payload.cover_ref,
                scheduled_for=payload.scheduled_for,
            ))

        return safe(command)

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/capability-supply-review")
    def get_capability_supply_review(company_id: str, workspace_id: str) -> dict[str, Any]:
        def query() -> dict[str, Any]:
            require_company_identity(company_id)
            return workspaces.get_capability_supply_review(company_id, workspace_id)

        return safe(query)

    @router.post("/workspaces/{workspace_id}/capability-supply-review")
    def review_capability_supply(workspace_id: str, payload: CapabilitySupplyReviewIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            row = _workspace_row(database, foundation, workspace_id)
            require_company_identity(row["company_id"])
            return workspaces.review_capability_supply(
                company_id=row["company_id"],
                workspace_id=workspace_id,
                selections=[{
                    "requirementRef": item.requirement_ref,
                    "source": item.source,
                    "capabilityType": item.capability_type,
                    "capabilityId": item.capability_id,
                } for item in payload.selections],
            )

        return safe(command)

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/staffing-approval")
    def get_staffing_approval(company_id: str, workspace_id: str) -> dict[str, Any]:
        def query() -> dict[str, Any]:
            require_company_identity(company_id)
            return workspaces.get_staffing_approval(company_id, workspace_id)

        return safe(query)

    @router.post("/workspaces/{workspace_id}/staffing-decision")
    def decide_staffing(workspace_id: str, payload: StaffingDecisionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            row = _workspace_row(database, foundation, workspace_id)
            require_company_identity(row["company_id"])
            return workspaces.decide_staffing(
                company_id=row["company_id"], workspace_id=workspace_id,
                choice=payload.choice, reason=payload.reason,
            )

        return safe(command)

    @router.post("/workspaces/{workspace_id}/staffing-rollback")
    def rollback_staffing(workspace_id: str, payload: StaffingRollbackIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            row = _workspace_row(database, foundation, workspace_id)
            require_company_identity(row["company_id"])
            return workspaces.rollback_staffing(
                company_id=row["company_id"], workspace_id=workspace_id, reason=payload.reason,
            )

        return safe(command)

    @router.post("/workspaces/{workspace_id}/simulations", status_code=201)
    def create_workspace_simulation(workspace_id: str, payload: WorkspaceSimulationIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            if payload.scenario_id == "ORG-001":
                if payload.subject_id or payload.participants or payload.input_refs:
                    raise ValueError("ORG-001 scope is derived by Runtime")
                return _simulation_projection(simulations.create_staffing(
                    company_id=workspace["company_id"],
                    ceo_id=payload.ceo_id,
                    workspace_id=workspace_id,
                    blueprint_version=payload.blueprint_version,
                ))
            if payload.scenario_id not in {"RD-001", "XHS-001", "TTK-001"} or not payload.subject_id:
                raise ValueError("Workspace simulation scenario or subject is invalid")
            with database.connect() as connection:
                current_workspace = connection.execute(
                    "select status from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (foundation.tenant_id, workspace["company_id"], workspace_id),
                ).fetchone()
            if current_workspace is None or current_workspace["status"] == "OPERATING":
                raise ValueError("Operating Workspace uses Cycle Runtime, not a new SimulationRun")
            return _simulation_projection(simulations.create(
                company_id=workspace["company_id"],
                ceo_id=payload.ceo_id,
                scenario_id=payload.scenario_id,
                blueprint_version=payload.blueprint_version,
                workspace_id=workspace_id,
                subject_id=payload.subject_id,
                participants=payload.participants,
                input_refs=payload.input_refs,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/simulations/{simulation_id}/transition")
    def transition_workspace_simulation(
        workspace_id: str, simulation_id: str, payload: SimulationTransitionIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            if payload.target.upper() != "RUNNING":
                raise ValueError("Desktop simulation transition only starts RUNNING")
            current = simulations.get(simulation_id)
            if current["workspace_id"] != workspace_id or current["company_id"] != workspace["company_id"]:
                raise RuntimeScopeError("simulation does not belong to current workspace")
            if current["invalidated_at"]:
                raise ValueError("invalidated simulation cannot start")
            return _simulation_projection(simulations.transition(
                simulation_id,
                "RUNNING",
                actor="CEO",
                trigger=payload.trigger,
                reason=payload.reason,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/simulations/{simulation_id}/execute")
    async def execute_workspace_simulation(workspace_id: str, simulation_id: str, payload: SimulationTransitionIn) -> dict[str, Any]:
        try:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            current = simulations.get(simulation_id)
            if current["workspace_id"] != workspace_id or current["company_id"] != workspace["company_id"]:
                raise RuntimeScopeError("simulation does not belong to current workspace")
            if current["scenario_id"] == "ORG-001":
                return _simulation_projection(simulations.execute_staffing(simulation_id))
            subject_id = current.get("subject_id")
            if not subject_id:
                raise RuntimeExecutionError("execution_subject_required")
            subject = foundation.get(subject_id)
            result = await execution.execute(current, subject)
            return _simulation_projection(result)
        except RuntimeExecutionError as error:
            status = 503 if error.code == "execution_unavailable" else 409
            raise HTTPException(status_code=status, detail=error.code) from error
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="运行对象不存在或无权访问") from error
        except (ActorNotAllowedError, TransitionError) as error:
            raise HTTPException(status_code=409, detail="当前状态不允许执行这个操作") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail="请求不符合 Runtime 契约") from error

    @router.post("/workspaces/{workspace_id}/simulations/{simulation_id}/review")
    def review_workspace_simulation(workspace_id: str, simulation_id: str, payload: SimulationReviewIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            current = simulations.get(simulation_id)
            if current["workspace_id"] != workspace_id or current["company_id"] != workspace["company_id"]:
                raise RuntimeScopeError("simulation does not belong to current workspace")
            decision = payload.decision.upper()
            if decision not in {"PASS", "FAIL", "REVIEW_REQUIRED"}:
                raise ValueError("review decision must be PASS, FAIL or REVIEW_REQUIRED")
            refs = list(dict.fromkeys(payload.evidence_refs))
            for evidence_id in refs:
                evidence = foundation.get(evidence_id)
                if (
                    evidence["entity_type"] != "EVIDENCE"
                    or evidence["company_id"] != current["company_id"]
                    or evidence["workspace_id"] != current["workspace_id"]
                    or evidence["parent_id"] != simulation_id
                ):
                    raise RuntimeScopeError("review evidence is outside the current simulation")
            simulations.append(simulation_id, "ceo_decisions", {
                "decision": decision,
                "evidenceRefs": refs,
                "notes": payload.notes,
                "actor": "CEO",
                "at": _now(),
            })
            if decision == "PASS":
                if not refs:
                    raise ValueError("PASS requires CEO-selected evidence")
                for evidence_id in refs:
                    foundation.set_dimensions(evidence_id, verification_status="VERIFIED")
            return _simulation_projection(simulations.review(
                simulation_id, reviewer="CEO", pass_status=decision, notes=payload.notes,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/receipts", status_code=201)
    def record_manual_receipt(workspace_id: str, content_id: str, payload: ManualReceiptIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            if payload.source.upper() != "CEO_MANUAL":
                raise ActorNotAllowedError("platform receipts require a trusted backend integration")
            if payload.status.upper() != "RECEIVED" or payload.recorded_by != payload.ceo_id:
                raise ValueError("manual receipts must remain RECEIVED and be recorded by the current CEO")
            content = foundation.get(content_id)
            if content["workspace_id"] != workspace_id:
                raise RuntimeScopeError("ContentItem does not belong to current workspace")
            return _runtime_object_projection(workspaces.record_publication_receipt(
                content_id,
                source="CEO_MANUAL",
                status=payload.status.upper(),
                approved_version_id=payload.approved_version_id,
                published_version_id=payload.published_version_id,
                recorded_by=payload.recorded_by,
                run_ref=payload.run_ref,
            ))

        return safe(command)

    @router.post("/workspaces/{workspace_id}/content-items/{content_id}/interactions", status_code=201)
    def record_manual_interaction(workspace_id: str, content_id: str, payload: ManualInteractionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo_identity(payload.ceo_id)
            workspace = _workspace_row(database, foundation, workspace_id)
            require_company_identity(workspace["company_id"])
            if payload.source.upper() != "CEO_MANUAL":
                raise ActorNotAllowedError("platform interactions require a trusted backend integration")
            content = foundation.get(content_id)
            if content["workspace_id"] != workspace_id:
                raise RuntimeScopeError("ContentItem does not belong to current workspace")
            return _runtime_object_projection(workspaces.record_interaction(
                content_id,
                source="CEO_MANUAL",
                external_id=payload.external_id,
                intent=payload.intent,
                sensitivity=payload.sensitivity,
                reply_policy=payload.reply_policy,
                recorded_by=payload.ceo_id,
                next_check_at=payload.next_check_at,
            ))

        return safe(command)

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/simulations")
    def list_workspace_simulations(company_id: str, workspace_id: str) -> dict[str, Any]:
        def query() -> dict[str, Any]:
            _require_workspace(database, foundation, company_id, workspace_id)
            return {
                "company_id": company_id,
                "workspace_id": workspace_id,
                "simulations": [
                    _simulation_projection(item)
                    for item in simulations.list(company_id=company_id, workspace_id=workspace_id)
                ],
            }

        return safe(query)

    @router.post("/founding-runs", status_code=201)
    def create_founding_run(payload: FoundingRunIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo()
            return _entity_projection(foundation.create(
                "FOUNDING_RUN",
                owner_ref=payload.owner_ref,
                org_version=payload.org_version,
                blueprint_version=payload.blueprint_version or None,
                data={"intentRef": payload.intent_ref} if payload.intent_ref else {},
            ))

        return safe(command)

    @router.get("/founding-runs/{founding_run_id}")
    def get_founding_run(founding_run_id: str) -> dict[str, Any]:
        def query() -> dict[str, Any]:
            entity = foundation.get(founding_run_id)
            if entity["entity_type"] != "FOUNDING_RUN":
                raise KeyError(founding_run_id)
            return _entity_projection(entity)

        return safe(query)

    @router.post("/founding-runs/{founding_run_id}/materialize-company")
    def materialize_company(founding_run_id: str, payload: MaterializeCompanyIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo()
            identity_ceo_id = TenantContext.current_identity().get("ceo_id")
            if not identity_ceo_id or payload.ceo_id != identity_ceo_id:
                raise RuntimeScopeError("CEO identity does not match the materialization command")
            run, _assistant = foundation.materialize_company(
                founding_run_id,
                company_id=payload.company_id,
                ceo_id=payload.ceo_id,
                name=payload.name,
            )
            snapshot = _company_snapshot(database, foundation, payload.company_id)
            return {"founding_run": _entity_projection(run), **snapshot}

        return safe(command)

    @router.post("/founding-runs/{founding_run_id}/materialize-first-general-workspace")
    def materialize_first_general_workspace(
        founding_run_id: str, payload: MaterializeFirstGeneralWorkspaceIn,
    ) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo()
            identity_ceo_id = TenantContext.current_identity().get("ceo_id")
            if not identity_ceo_id or payload.ceo_id != identity_ceo_id:
                raise RuntimeScopeError("CEO identity does not match the materialization command")
            result = first_run_delivery.materialize(
                founding_run_id,
                FirstGeneralWorkspaceDraft(**payload.model_dump()),
            )
            return {
                **result,
                "founding_run": _entity_projection(result["founding_run"]),
                "assistant": _entity_projection(result["assistant"]),
            }

        return safe(command)

    @router.post("/entities/{entity_id}/transition")
    def transition_entity(entity_id: str, payload: TransitionIn) -> dict[str, Any]:
        def command() -> dict[str, Any]:
            require_ceo(payload.actor)
            if set(payload.context) - _SAFE_CONTEXT_KEYS:
                raise ValueError("unsupported transition context")
            current = foundation.get(entity_id)
            if current["entity_type"] == "CONTENT_ITEM" and payload.target == "PUBLISHED":
                raise ActorNotAllowedError("ContentItem publication requires a trusted publishing receipt")
            for evidence_id in payload.evidenceRefs:
                evidence = foundation.get(evidence_id)
                if evidence["entity_type"] != "EVIDENCE":
                    raise ValueError("evidenceRefs must reference Evidence")
                for field in ("company_id", "workspace_id"):
                    if current[field] and evidence[field] and current[field] != evidence[field]:
                        raise RuntimeScopeError("cross-scope evidence rejected")
            return _entity_projection(foundation.transition(
                entity_id,
                payload.target,
                actor=payload.actor,
                trigger=payload.trigger,
                reason=payload.reason,
                evidence_refs=payload.evidenceRefs,
                next_check_at=payload.nextCheckAt,
                context=payload.context,
            ))

        return safe(command)

    return router


def _runtime_company_collection(database: Database, foundation: RuntimeFoundation) -> list[dict[str, Any]]:
    with database.connect() as connection:
        rows = connection.execute(
            """
            select c.company_id, c.name, c.description, c.company_type, c.status,
                   c.is_default, c.created_at, c.updated_at
            from companies c
            where c.tenant_id = ?
              and exists (
                select 1
                from runtime_entities founding
                join runtime_entities assistant
                  on assistant.tenant_id = founding.tenant_id
                 and assistant.entity_id = founding.parent_id
                 and assistant.entity_type = 'CEO_ASSISTANT'
                 and assistant.company_id = founding.company_id
                where founding.tenant_id = c.tenant_id
                  and founding.company_id = c.company_id
                  and founding.entity_type = 'FOUNDING_RUN'
              )
            order by c.created_at, c.company_id
            """,
            (foundation.tenant_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def _company_snapshot(database: Database, foundation: RuntimeFoundation, company_id: str) -> dict[str, Any]:
    foundation._require_company(company_id)
    with database.connect() as connection:
        company = connection.execute(
            "select company_id, name, description, company_type, status, is_default, created_at, updated_at "
            "from companies where tenant_id = ? and company_id = ?",
            (foundation.tenant_id, company_id),
        ).fetchone()
        workspaces = connection.execute(
            "select workspace_id, business_id, name, status, blueprint_version, operating_version, "
            "simulation_passed, created_at, updated_at from workspaces "
            "where tenant_id = ? and company_id = ? order by created_at, workspace_id",
            (foundation.tenant_id, company_id),
        ).fetchall()
    if company is None:
        raise KeyError(company_id)
    by_type = {
        entity_type: [_entity_projection(item) for item in foundation.list(entity_type, company_id=company_id)]
        for entity_type in ("CEO_ASSISTANT", "AI_EMPLOYEE", "ROLE_SLOT", "CAPABILITY_BINDING")
    }
    return {
        "company": dict(company),
        "assistant": by_type["CEO_ASSISTANT"][0] if by_type["CEO_ASSISTANT"] else None,
        "organization": {
            "employees": by_type["AI_EMPLOYEE"],
            "role_slots": by_type["ROLE_SLOT"],
            "capability_bindings": by_type["CAPABILITY_BINDING"],
        },
        "workspaces": [dict(item) for item in workspaces],
    }


def _require_workspace(
    database: Database,
    foundation: RuntimeFoundation,
    company_id: str,
    workspace_id: str,
) -> None:
    foundation._require_company(company_id)
    with database.connect() as connection:
        row = connection.execute(
            "select 1 from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
            (foundation.tenant_id, company_id, workspace_id),
        ).fetchone()
    if row is None:
        raise RuntimeScopeError("workspace does not belong to current company")


def _workspace_row(database: Database, foundation: RuntimeFoundation, workspace_id: str) -> dict[str, Any]:
    foundation._require_workspace(workspace_id, None)
    with database.connect() as connection:
        row = connection.execute(
            "select company_id, business_relation_status from workspaces where tenant_id = ? and workspace_id = ?",
            (foundation.tenant_id, workspace_id),
        ).fetchone()
    if row is None:
        raise RuntimeScopeError("workspace does not belong to current tenant")
    if row["business_relation_status"] != "RESOLVED":
        raise RuntimeScopeError("workspace business relation is not resolved")
    return dict(row)


def _entity_projection(entity: dict[str, Any]) -> dict[str, Any]:
    projection = {
        key: entity.get(key)
        for key in (
            "entity_id", "entity_type", "company_id", "workspace_id", "parent_id", "owner_ref",
            "lifecycle_status", "exception_status", "presence_state", "org_version", "blueprint_version",
            "capability_ref", "execution_ref", "verification_status", "evidence_condition", "next_check_at",
            "current_version_id", "approved_version_id", "published_version_id",
            "created_at", "updated_at",
        )
    }
    if entity.get("entity_type") in {"AI_EMPLOYEE", "ROLE_SLOT", "CAPABILITY_BINDING"}:
        projection["data"] = {
            key: value
            for key, value in entity.get("data", {}).items()
            if key in {
                "name", "responsibility", "capabilityRefs", "reportingTo", "staffingStatus",
                "roleSlotRef", "requirementRef", "authorizationStatus",
            }
        }
    if entity.get("entity_type") == "FOUNDING_RUN":
        data = entity.get("data", {})
        projection["intent_ref"] = data.get("intentRef", "")
        first_business = data.get("firstBusiness")
        if isinstance(first_business, dict):
            projection["first_business"] = {
                key: first_business.get(key)
                for key in (
                    "department_id", "business_id", "workspace_id", "version_id",
                    "templateMatchStatus",
                )
            }
    return projection


_SAFE_RUNTIME_DATA = frozenset({
    "workItemName", "outcomeRef", "intentRef", "currentStage", "stages", "evidenceRefs",
    "platform", "platformVariant", "payloadRef", "author", "constraintsCheck", "versionStatus",
    "title", "body", "tags", "coverRef", "scheduledFor",
    "ownerRole", "source", "status", "approvedVersionId", "publishedVersionId", "externalId",
    "recordedBy", "runRef", "receivedAt", "intent", "sensitivity", "replyPolicy",
    "operatingVersion", "orgVersion", "teamRefs", "roleSlotRefs", "inputHandoffRefs",
    "outputHandoffId", "acceptanceId", "executionStatus", "executionReceivedAt",
    "failureEvents", "acceptanceDecision", "decisionPacketId", "nextAction", "reviewReason",
    "completedAt", "startedAt", "kind", "cycleId", "fromRole", "toRole", "roleSlotRef",
    "employeeRef", "inputRefs", "outputRefs", "acknowledgement", "actor", "at", "criteria",
    "decision", "reason", "decidedAt", "currentState", "whyNow", "unknowns", "options",
    "recommendation", "choice", "effectiveAt", "rollbackCondition", "summary", "executionRef",
    "workContext", "conversation", "plainPackage", "artifactReview", "reviewConversation", "requestRef",
    "responsibilityHandoff", "responsibilityHandoffRefs", "handoffRef", "fromEmployeeRef",
    "toEmployeeRef", "toRoleSlotRef", "responsibilitySummary", "nextCheckAt", "contextRefs",
    "createdAt", "sentAt", "respondedAt", "responseReason", "providerAck",
    "rdDecisionPacketRef", "decisionConversation", "decisionKey", "complexity", "layer0Actions",
    "event", "cannotDecideReason", "recommendationReason", "ceoChoicePrompt", "continuationPlan",
    "responsibilityHolderRef", "layer1ReviewedAt", "deferredAt", "deferReason", "choiceReason",
    "appliedAt", "rdDecisionApplied", "taskHistoryRefs", "artifactHistoryRefs", "resultHistoryRefs",
    "artifactReviewHistory",
    "reportRef", "reportSha256", "analysisContext",
    "projectRef", "instruction", "resourceRefs", "testCommand", "requestedAccessIntent",
    "executionBinding", "taskRef", "sessionRef", "artifactRefs", "resultRefs",
    "computerAccess", "testResult", "changedFiles",
})


def _runtime_object_projection(entity: dict[str, Any]) -> dict[str, Any]:
    return _entity_projection(entity) | {
        "data": {key: value for key, value in entity.get("data", {}).items() if key in _SAFE_RUNTIME_DATA}
    }


def _workspace_projection(snapshot: dict[str, Any]) -> dict[str, Any]:
    workspace = snapshot["workspace"]
    versions = [
        {
            key: item.get(key)
            for key in (
                "version_id", "blueprint_version", "status", "simulation_passed",
                "operating_version", "change_kind", "created_at", "updated_at",
            )
        } | {"change_reason": item.get("data", {}).get("changeReason", "")}
          | {"blueprint": item.get("data", {}).get("blueprint", {})}
        for item in snapshot["versions"]
    ]
    employees = [_entity_projection(item) for item in snapshot["entities"]["AI_EMPLOYEE"]]
    employee_by_id = {item["entity_id"]: item for item in employees}
    receipts = snapshot["entities"]["PUBLICATION_RECEIPT"]

    def content_projection(item: dict[str, Any]) -> dict[str, Any]:
        projection = _runtime_object_projection(item)
        context = item.get("data", {}).get("workContext") or {}
        responsibility_ref = context.get("responsibilityEmployeeRef")
        executor_ref = context.get("currentExecutorRef")
        projection["work_context"] = {
            "object_owner": {
                "kind": "WORKSPACE",
                "ref": workspace["workspace_id"],
                "label": workspace["name"],
            },
            "current_responsibility": {
                "employee_ref": responsibility_ref,
                "employee": employee_by_id.get(responsibility_ref),
                "role_slot_ref": context.get("responsibilityRoleSlotRef"),
                "activity": context.get("activity", ""),
                "status": context.get("status", "idle"),
            } if responsibility_ref else None,
            "current_executor": {
                "employee_ref": executor_ref,
                "employee": employee_by_id.get(executor_ref),
            } if executor_ref else None,
            "system_activity": context.get("systemActivity"),
        }
        item_receipts = [receipt for receipt in receipts if receipt["parent_id"] == item["entity_id"]]
        verified_receipt = next(
            (
                receipt for receipt in item_receipts
                if receipt["verification_status"] == "VERIFIED"
                and receipt["data"].get("source") == "PLATFORM_API"
                and receipt["data"].get("status") == "SUCCESS"
                and receipt["data"].get("externalId")
            ),
            None,
        )
        manual_receipt = next(
            (receipt for receipt in item_receipts if receipt["data"].get("source") == "CEO_MANUAL"),
            None,
        )
        if item["lifecycle_status"] == "PUBLISHED" and verified_receipt:
            publication = {"status": "PUBLISHED_VERIFIED", "label": "已发布（已验证）", "receipt_ref": verified_receipt["entity_id"]}
        elif item["lifecycle_status"] == "PUBLISHED":
            publication = {"status": "PUBLISHED_UNVERIFIED", "label": "发布事实未验证", "receipt_ref": None}
        elif manual_receipt:
            publication = {"status": "MANUAL_RECEIPT_UNVERIFIED", "label": "已有手动回执，尚未验证发布", "receipt_ref": manual_receipt["entity_id"]}
        elif item["lifecycle_status"] == "SCHEDULED":
            publication = {"status": "WAITING_FOR_CAPABILITY", "label": "等待发布能力", "receipt_ref": None}
        else:
            publication = {"status": "NOT_READY", "label": "尚未到发布阶段", "receipt_ref": None}
        projection["publication"] = publication
        projection["analytics"] = {
            "status": "WAITING_FOR_CAPABILITY" if verified_receipt else "UNAVAILABLE",
            "label": "等待数据能力" if verified_receipt else "暂无数据",
            "metrics": None,
        }
        return projection

    return {
        "workspace": {
            key: workspace.get(key)
            for key in (
                "workspace_id", "company_id", "business_id", "business_type", "name", "status",
                "blueprint_version", "operating_version", "simulation_passed", "created_at", "updated_at",
            )
        } | {"blueprint": workspace["blueprint"]},
        "versions": versions,
        "employees": employees,
        "role_slots": [_entity_projection(item) for item in snapshot["entities"]["ROLE_SLOT"]],
        "capability_bindings": [
            _entity_projection(item) for item in snapshot["entities"]["CAPABILITY_BINDING"]
        ],
        "cycles": [_runtime_object_projection(item) for item in snapshot["entities"]["CYCLE"]],
        "content_items": [content_projection(item) for item in snapshot["entities"]["CONTENT_ITEM"]],
        "content_versions": [_runtime_object_projection(item) for item in snapshot["entities"]["CONTENT_VERSION"]],
        "publication_receipts": [
            _runtime_object_projection(item) for item in snapshot["entities"]["PUBLICATION_RECEIPT"]
        ],
        "interactions": [_runtime_object_projection(item) for item in snapshot["entities"]["INTERACTION_ITEM"]],
        "handoffs": [_runtime_object_projection(item) for item in snapshot["entities"]["HANDOFF"]],
        "acceptances": [_runtime_object_projection(item) for item in snapshot["entities"]["ACCEPTANCE"]],
        "decisions": [_runtime_object_projection(item) for item in snapshot["entities"]["DECISION_PACKET"]],
        "evidence": [_runtime_object_projection(item) for item in snapshot["entities"]["EVIDENCE"]],
        "simulations": [_simulation_projection(item) for item in snapshot["simulations"]],
    }


def _simulation_projection(run: dict[str, Any]) -> dict[str, Any]:
    failures = [item for item in run["failure_events"] if isinstance(item, dict)]
    return {
        key: run.get(key)
        for key in (
            "simulation_run_id", "company_id", "workspace_id", "scenario_id", "blueprint_version",
            "lifecycle_status", "pass_status", "final_state", "started_at", "finished_at", "reviewed_at",
            "invalidated_at", "invalidation_reason", "created_at", "updated_at",
            "subject_id",
        )
    } | {
        "evidence_refs": list(run.get("evidence_refs") or []),
        "evidence_count": len(run.get("evidence_refs") or []),
        "handoff_count": len(run.get("handoffs") or []),
        "ceo_decision_count": len(run.get("ceo_decisions") or []),
        "failure_summary": {
            "count": len(run["failure_events"]),
            "unresolved_count": sum(
                not isinstance(item, dict) or not item.get("resolvedAt")
                for item in run["failure_events"]
            ),
            "kinds": sorted({str(item.get("kind")) for item in failures if item.get("kind")}),
        }
    }
