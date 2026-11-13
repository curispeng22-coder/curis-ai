"""Read-only HTTP routes for the Shared Workspace projection."""

from fastapi import APIRouter, HTTPException
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt

from ..database import Database
from ..runtime import RuntimeScopeError
from ..runtime.general_workspace_delivery import GeneralWorkspaceDelivery, GeneralWorkspaceGap, GeneralHumanAuthorityGap
from ..runtime.responsibility_routing import HumanInputInvalid, ResponsibilityRoutingError
from ..shared_workspace_projection import SharedWorkspaceProjection
from ..tenant_context import TenantContext


class GeneralWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    problem: str = Field(min_length=1, max_length=2000)
    expected_result: str = Field(min_length=1, max_length=2000)
    constraints: list[str] = Field(default_factory=list, max_length=32)
    references: list[str] = Field(default_factory=list, max_length=32)
    idempotency_key: str = Field(min_length=1, max_length=128)


class GeneralRouteIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal: str = Field(min_length=1, max_length=64)
    responsibility_key: str | None = Field(default=None, max_length=96)
    result_refs: list[str] = Field(default_factory=list, max_length=32)
    artifact_refs: list[str] = Field(default_factory=list, max_length=32)
    evidence_refs: list[str] = Field(default_factory=list, max_length=32)
    reason: str = Field(default="", max_length=2000)


class GeneralDecisionChoiceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    choice: str = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1, max_length=2000)
    next_check_at: str | None = Field(default=None, max_length=64)


class GeneralEmployeeAssignmentIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id: str = Field(min_length=1, max_length=128)
    responsibility: str = Field(min_length=1, max_length=1000)


class GeneralLifecycleIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(default="", max_length=2000)


class GeneralHumanReportIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: StrictInt = Field(ge=1)
    submission_id: str = Field(min_length=1, max_length=128)
    kind: Literal["LOCAL_INFORMATION", "EXTERNAL_ACTION_REPORT"]
    local_text: str = Field(default="", max_length=2000)
    reference_refs: list[str] = Field(default_factory=list, max_length=16)
    manual_source: str = Field(default="", max_length=2000)


class GeneralHumanReviewIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: StrictInt = Field(ge=1)


def build_shared_workspace_router(database: Database) -> APIRouter:
    router = APIRouter()
    shared = SharedWorkspaceProjection(database)
    general = GeneralWorkspaceDelivery(database)

    def require_company(company_id: str) -> None:
        current = TenantContext.current_identity().get("company_id")
        if current and current != company_id:
            raise RuntimeScopeError("Company identity does not match the current query")

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared")
    def workspace(company_id: str, workspace_id: str):
        try:
            require_company(company_id)
            return shared.workspace(company_id, workspace_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="Workspace 不存在或无权访问") from error

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared/general")
    def general_workspace(company_id: str, workspace_id: str):
        try:
            require_company(company_id)
            return shared.general_workspace(company_id, workspace_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works")
    def create_general_work(company_id: str, workspace_id: str, payload: GeneralWorkIn):
        try:
            require_company(company_id)
            return general.create_work(
                company_id=company_id,
                workspace_id=workspace_id,
                problem=payload.problem,
                expected_result=payload.expected_result,
                constraints=payload.constraints,
                references=payload.references,
                idempotency_key=payload.idempotency_key,
            )
        except GeneralWorkspaceGap as error:
            raise HTTPException(status_code=409, detail=error.payload) from error
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/team/materialize")
    def materialize_general_team(company_id: str, workspace_id: str):
        try:
            require_company(company_id)
            return general.materialize_team(company_id=company_id, workspace_id=workspace_id)
        except GeneralWorkspaceGap as error:
            raise HTTPException(status_code=409, detail=error.payload) from error
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared/general/team/candidates")
    def general_team_candidates(company_id: str, workspace_id: str):
        try:
            require_company(company_id)
            return general.assignment_candidates(company_id=company_id, workspace_id=workspace_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/team/assign")
    def assign_general_employee(company_id: str, workspace_id: str, payload: GeneralEmployeeAssignmentIn):
        try:
            require_company(company_id)
            return general.assign_employee(
                company_id=company_id,
                workspace_id=workspace_id,
                employee_id=payload.employee_id,
                responsibility=payload.responsibility,
            )
        except GeneralWorkspaceGap as error:
            raise HTTPException(status_code=409, detail=error.payload) from error
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/route")
    def route_general_work(company_id: str, workspace_id: str, work_ref: str, payload: GeneralRouteIn):
        try:
            require_company(company_id)
            return general.route_work(
                company_id=company_id, workspace_id=workspace_id, work_ref=work_ref,
                signal=payload.signal, responsibility_key=payload.responsibility_key,
                result_refs=payload.result_refs, artifact_refs=payload.artifact_refs,
                evidence_refs=payload.evidence_refs, reason=payload.reason,
            )
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/human-input/{request_id}/report")
    def report_general_human_input(company_id: str, workspace_id: str, work_ref: str,
                                   request_id: str, payload: GeneralHumanReportIn):
        try:
            require_company(company_id)
            return general.report_human_input(company_id=company_id, workspace_id=workspace_id,
                work_ref=work_ref, request_id=request_id, revision=payload.revision,
                submission_id=payload.submission_id, kind=payload.kind,
                local_text=payload.local_text, reference_refs=payload.reference_refs,
                manual_source=payload.manual_source)
        except HumanInputInvalid as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except ResponsibilityRoutingError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except GeneralHumanAuthorityGap as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except RuntimeScopeError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except (KeyError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/human-input/{request_id}/review")
    def review_general_human_input(company_id: str, workspace_id: str, work_ref: str,
                                   request_id: str, payload: GeneralHumanReviewIn):
        try:
            require_company(company_id)
            return general.review_human_input(company_id=company_id, workspace_id=workspace_id,
                work_ref=work_ref, request_id=request_id, revision=payload.revision)
        except ResponsibilityRoutingError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except GeneralHumanAuthorityGap as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except RuntimeScopeError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except (KeyError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/usage")
    def general_work_usage(company_id: str, workspace_id: str, work_ref: str):
        try:
            require_company(company_id)
            return general.work_usage(company_id=company_id, workspace_id=workspace_id, work_ref=work_ref)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="工作不存在或无权访问") from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/lifecycle/{action}")
    def control_general_work(
        company_id: str, workspace_id: str, work_ref: str,
        action: Literal["pause", "resume", "cancel", "archive", "restore"],
        payload: GeneralLifecycleIn,
    ):
        try:
            require_company(company_id)
            return general.control_work(
                company_id=company_id, workspace_id=workspace_id, work_ref=work_ref,
                action=action, reason=payload.reason,
            )
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/decision")
    def request_general_decision(company_id: str, workspace_id: str, work_ref: str, payload: dict):
        try:
            require_company(company_id)
            return general.request_decision(
                company_id=company_id, workspace_id=workspace_id, work_ref=work_ref, packet=payload,
            )
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/decision/review")
    def review_general_decision(company_id: str, workspace_id: str, work_ref: str):
        try:
            require_company(company_id)
            return general.review_decision(company_id=company_id, workspace_id=workspace_id, work_ref=work_ref)
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.post("/companies/{company_id}/workspaces/{workspace_id}/shared/general/works/{work_ref}/decision/choose")
    def choose_general_decision(
        company_id: str, workspace_id: str, work_ref: str, payload: GeneralDecisionChoiceIn,
    ):
        try:
            require_company(company_id)
            return general.choose_decision(
                company_id=company_id, workspace_id=workspace_id, work_ref=work_ref,
                choice=payload.choice, reason=payload.reason, next_check_at=payload.next_check_at,
            )
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared/employees/{employee_id}")
    def employee(company_id: str, workspace_id: str, employee_id: str):
        try:
            require_company(company_id)
            return shared.employee(company_id, workspace_id, employee_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="员工不存在或不属于当前工作空间") from error

    @router.get("/companies/{company_id}/workspaces/{workspace_id}/shared/results/{reference_id}")
    def result(company_id: str, workspace_id: str, reference_id: str):
        try:
            require_company(company_id)
            return shared.result(company_id, workspace_id, reference_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="结果不存在或不属于当前工作空间") from error

    return router
