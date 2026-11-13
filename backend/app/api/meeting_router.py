from __future__ import annotations

from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ..database import Database
from ..meeting_service import EmployeeExecution, MeetingService
from ..runtime.foundation import RuntimeScopeError
from ..tenant_context import TenantContext


class MeetingContextRefIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str = Field(min_length=1, max_length=32)
    ref: str = Field(min_length=1, max_length=256)


class MeetingCreateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=240)
    background: str = Field(default="", max_length=4000)
    business_id: str = Field(default="", max_length=128)
    workspace_id: str = Field(default="", max_length=128)
    participant_refs: list[str] = Field(min_length=1, max_length=32)
    leader_ref: str = Field(min_length=1, max_length=128)
    ceo_participation_mode: str = Field(default="DECISION_ONLY", max_length=32)
    context_refs: list[MeetingContextRefIn] = Field(default_factory=list, max_length=32)


class MeetingMessageIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    actor_type: str = Field(default="CEO", max_length=16)
    actor_ref: str = Field(default="", max_length=128)
    text: str = Field(min_length=1, max_length=4000)
    context_refs: list[MeetingContextRefIn] = Field(default_factory=list, max_length=32)


class MeetingDecisionChoiceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    choice: str = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1, max_length=2000)


def build_meeting_router(database: Database, employee_execution: EmployeeExecution | None = None) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/runtime/foundation", tags=["meeting-room"])
    service = MeetingService(database, employee_execution)

    def schedule(background_tasks: BackgroundTasks, company_id: str, meeting_id: str) -> None:
        if employee_execution is None:
            return
        tenant_id = TenantContext.current_tenant_id()
        identity = TenantContext.current_identity()

        async def run() -> None:
            with TenantContext.scope(
                tenant_id,
                subject_id=identity.get("subject_id", ""), company_id=identity.get("company_id", ""),
                ceo_id=identity.get("ceo_id", ""), role=identity.get("role", ""),
                membership_status=identity.get("membership_status", ""), request_id=identity.get("request_id", ""),
            ):
                await MeetingService(database, employee_execution).advance(company_id, meeting_id)

        background_tasks.add_task(run)

    def require_company(company_id: str) -> None:
        current = TenantContext.current_identity().get("company_id")
        if current and current != company_id:
            raise RuntimeScopeError("Company identity does not match the current Meeting")

    def command(action):
        try:
            return action()
        except KeyError as error:
            raise HTTPException(status_code=404, detail="会议不存在或无权访问") from error
        except RuntimeScopeError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/companies/{company_id}/meetings")
    def list_meetings(company_id: str) -> dict[str, Any]:
        return command(lambda: (require_company(company_id), service.list(company_id))[1])

    @router.post("/companies/{company_id}/meetings", status_code=201)
    def create_meeting(company_id: str, payload: MeetingCreateIn, background_tasks: BackgroundTasks) -> dict[str, Any]:
        meeting = command(lambda: (
            require_company(company_id),
            service.create(
                company_id=company_id, title=payload.title, background=payload.background,
                business_id=payload.business_id, workspace_id=payload.workspace_id,
                participant_refs=payload.participant_refs, leader_ref=payload.leader_ref,
                ceo_participation_mode=payload.ceo_participation_mode,
                context_refs=[item.model_dump() for item in payload.context_refs],
            ),
        )[1])
        schedule(background_tasks, company_id, meeting["meeting_id"])
        return meeting

    @router.get("/companies/{company_id}/meetings/{meeting_id}")
    def get_meeting(company_id: str, meeting_id: str) -> dict[str, Any]:
        return command(lambda: (require_company(company_id), service.get(company_id, meeting_id))[1])

    @router.post("/companies/{company_id}/meetings/{meeting_id}/messages")
    def add_message(
        company_id: str, meeting_id: str, payload: MeetingMessageIn, background_tasks: BackgroundTasks,
    ) -> dict[str, Any]:
        meeting = command(lambda: (
            require_company(company_id),
            service.add_message(
                company_id, meeting_id, actor_type=payload.actor_type,
                actor_ref=payload.actor_ref, text=payload.text,
                context_refs=[item.model_dump() for item in payload.context_refs],
            ),
        )[1])
        schedule(background_tasks, company_id, meeting_id)
        return meeting

    @router.post("/companies/{company_id}/meetings/{meeting_id}/decision")
    def request_decision(company_id: str, meeting_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return command(lambda: (
            require_company(company_id), service.request_decision(company_id, meeting_id, payload),
        )[1])

    @router.post("/companies/{company_id}/meetings/{meeting_id}/decision/review")
    def review_decision(company_id: str, meeting_id: str) -> dict[str, Any]:
        return command(lambda: (
            require_company(company_id), service.review_decision(company_id, meeting_id),
        )[1])

    @router.post("/companies/{company_id}/meetings/{meeting_id}/decision/choose")
    def choose_decision(
        company_id: str, meeting_id: str, payload: MeetingDecisionChoiceIn,
        background_tasks: BackgroundTasks,
    ) -> dict[str, Any]:
        meeting = command(lambda: (
            require_company(company_id),
            service.choose_decision(
                company_id, meeting_id, choice=payload.choice, reason=payload.reason,
            ),
        )[1])
        schedule(background_tasks, company_id, meeting_id)
        return meeting

    @router.post("/companies/{company_id}/meetings/{meeting_id}/sync")
    def sync_meeting(company_id: str, meeting_id: str, background_tasks: BackgroundTasks) -> dict[str, Any]:
        meeting = command(lambda: (
            require_company(company_id), service.sync(company_id, meeting_id),
        )[1])
        schedule(background_tasks, company_id, meeting_id)
        return meeting

    @router.post("/companies/{company_id}/meetings/{meeting_id}/advance", status_code=202)
    def advance_meeting(company_id: str, meeting_id: str, background_tasks: BackgroundTasks) -> dict[str, Any]:
        meeting = command(lambda: (
            require_company(company_id), service.get(company_id, meeting_id),
        )[1])
        schedule(background_tasks, company_id, meeting_id)
        return meeting

    @router.post("/companies/{company_id}/meetings/{meeting_id}/close")
    def close_meeting(company_id: str, meeting_id: str) -> dict[str, Any]:
        return command(lambda: (
            require_company(company_id), service.close(company_id, meeting_id),
        )[1])

    return router
