"""「CEO 的一天」闭环 HTTP 接口（A5 信封 + 第 2 步领域模型）。

所有响应统一包 ``ApiResponse[T]``（A5）。服务实例挂在 ``app.state.ceo_day_service``，
由 ``create_app`` 装配。本路由是 Step 3 前端接入的真实后端入口。
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from .envelope import ok


class _Body(BaseModel):
    pass


class AuthorizeBody(BaseModel):
    authorized: bool = False


class VerificationBody(BaseModel):
    grade: str = "UNVERIFIED"


class FulfillBody(BaseModel):
    verification_status: str = "VERIFIED"


class WorkspaceApprovalBody(BaseModel):
    issues_resolved: bool = True
    external_agent_reviewed: bool = True


class EnableBody(BaseModel):
    next_fire_at: str | None = None


class ResolveBody(BaseModel):
    reason: str = ""


class Contributor(BaseModel):
    agent: str = ""
    model: str = ""
    skills: list[str] = []
    tools: list[str] = []
    weight: float = 0.0


class OutcomeBody(BaseModel):
    business_id: str
    run_id: str | None = None
    commitment_id: str | None = None
    route: str = ""
    value: float = 0.0
    evidence_grade: str = "UNVERIFIED"
    source: str = ""
    evidence_ref: str = ""
    evidence_type: str = ""
    contributors: list[Contributor] = []


class DirectionBody(BaseModel):
    name: str
    template_type: str
    opportunity: str = ""
    target_outcome: str = ""
    timebox_days: int = 30
    evidence_route: str = ""


class CommitmentBody(BaseModel):
    business_id: str
    department_name: str = ""
    name: str
    target_outcome: str = ""
    capacity_contract: dict[str, Any] = {}


class WorkspaceBody(BaseModel):
    business_id: str
    name: str


class CadenceBody(BaseModel):
    business_id: str
    name: str
    schedule_text: str
    owner_id: str = ""
    task: str = ""
    escalation: dict[str, Any] = {}
    max_concurrent: int = 1


def _svc(request: Request):
    svc = getattr(request.app.state, "ceo_day_service", None)
    if svc is None:
        raise HTTPException(status_code=503, detail="ceo_day_service 未装配")
    return svc


def build_ceo_day_router() -> APIRouter:
    router = APIRouter(prefix="/api/ceo-day", tags=["ceo-day"])

    # BusinessDirection
    @router.post("/business-directions")
    def create_direction(body: DirectionBody, request: Request):
        did = _svc(request).create_business_direction(
            name=body.name, template_type=body.template_type,
            opportunity=body.opportunity, target_outcome=body.target_outcome,
            timebox_days=body.timebox_days, evidence_route=body.evidence_route,
        )
        return ok(_svc(request).get_direction(did))

    @router.post("/business-directions/{did}/submit-brief")
    def submit_brief(did: str, request: Request):
        _svc(request).submit_direction_brief(did)
        return ok(_svc(request).get_direction(did))

    @router.post("/business-directions/{did}/approve")
    def approve(did: str, body: AuthorizeBody, request: Request):
        _svc(request).approve_direction(did, authorized=body.authorized)
        return ok(_svc(request).get_direction(did))

    @router.post("/business-directions/{did}/scale")
    def scale(did: str, request: Request):
        _svc(request).scale_direction(did)
        return ok(_svc(request).get_direction(did))

    @router.post("/business-directions/{did}/verification")
    def verification(did: str, body: VerificationBody, request: Request):
        _svc(request).set_direction_verification(did, body.grade)
        return ok(_svc(request).get_direction(did))

    # Commitment
    @router.post("/commitments")
    def create_commitment(body: CommitmentBody, request: Request):
        cid = _svc(request).create_commitment(
            body.business_id, department_name=body.department_name,
            name=body.name, target_outcome=body.target_outcome,
            capacity_contract=body.capacity_contract,
        )
        return ok(_svc(request).get_commitment(cid))

    @router.post("/commitments/{cid}/first-result")
    def first_result(cid: str, request: Request):
        _svc(request).report_commitment_first_result(cid)
        return ok(_svc(request).get_commitment(cid))

    @router.post("/commitments/{cid}/fulfill")
    def fulfill(cid: str, body: FulfillBody, request: Request):
        _svc(request).fulfill_commitment(cid, verification_status=body.verification_status)
        return ok(_svc(request).get_commitment(cid))

    # Workspace
    @router.post("/workspaces")
    def create_workspace(body: WorkspaceBody, request: Request):
        wid = _svc(request).create_workspace(body.business_id, name=body.name)
        return ok(_svc(request).get_workspace(wid))

    @router.post("/workspaces/{wid}/start-blueprint")
    def start_blueprint(wid: str, request: Request):
        _svc(request).start_blueprint(wid)
        return ok(_svc(request).get_workspace(wid))

    @router.post("/workspaces/{wid}/pass-simulation")
    def pass_sim(wid: str, request: Request):
        _svc(request).pass_simulation(wid)
        return ok(_svc(request).get_workspace(wid))

    @router.post("/workspaces/{wid}/submit-approval")
    def submit_appr(wid: str, body: WorkspaceApprovalBody, request: Request):
        _svc(request).submit_workspace_for_approval(
            wid, issues_resolved=body.issues_resolved,
            external_agent_reviewed=body.external_agent_reviewed,
        )
        return ok(_svc(request).get_workspace(wid))

    @router.post("/workspaces/{wid}/approve-launch")
    def launch(wid: str, request: Request):
        _svc(request).approve_and_launch_workspace(wid)
        return ok(_svc(request).get_workspace(wid))

    # Cadence / Run
    @router.post("/cadences")
    def create_cadence(body: CadenceBody, request: Request):
        cid = _svc(request).create_cadence(
            body.business_id, body.name, body.schedule_text,
            owner_id=body.owner_id, task=body.task,
            escalation=body.escalation, max_concurrent=body.max_concurrent,
        )
        return ok({"cadence_id": cid})

    @router.post("/cadences/{cid}/enable")
    def enable(cid: str, body: EnableBody, request: Request):
        _svc(request).enable_cadence(cid, next_fire_at=body.next_fire_at)
        return ok({"cadence_id": cid, "enabled": True})

    @router.post("/fire")
    def fire(request: Request):
        spawned = _svc(request).fire_due_runs()
        return ok({"spawned": spawned})

    @router.post("/runs/{run_id}/open")
    def open_run(run_id: str, request: Request):
        _svc(request).ceo_open_run(run_id)
        return ok(_svc(request).get_run(run_id))

    @router.post("/runs/{run_id}/resolve")
    def resolve_run(run_id: str, body: ResolveBody, request: Request):
        _svc(request).ceo_resolve_run(run_id, reason=body.reason)
        return ok(_svc(request).get_run(run_id))

    # Outcome
    @router.post("/outcomes")
    def create_outcome(body: OutcomeBody, request: Request):
        oid = _svc(request).record_outcome(
            body.business_id, run_id=body.run_id,
            commitment_id=body.commitment_id, route=body.route, value=body.value,
            evidence_grade=body.evidence_grade, source=body.source,
            evidence_ref=body.evidence_ref, evidence_type=body.evidence_type,
            contributors=[c.model_dump() for c in body.contributors],
        )
        return ok(_svc(request).get_outcome(oid))

    @router.post("/outcomes/{oid}/confirm-attribution")
    def confirm_attr(oid: str, request: Request):
        _svc(request).confirm_attribution(oid)
        return ok(_svc(request).get_outcome(oid))

    return router
