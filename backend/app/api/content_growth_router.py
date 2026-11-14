"""Canonical graphic authoring; reads never execute or adopt."""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, Request, Header
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from uuid import UUID
import re
from urllib.parse import unquote
from pydantic import field_validator
from ..content_growth_service import ContentGrowthService, ContentGrowthConflict
from ..runtime import RuntimeScopeError

class CommandIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    request_id: str=Field(min_length=1,max_length=128)
    expected_version_ref: str=Field(default="",max_length=256)
    data: dict

class ModelIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assignment_ref: str = Field(min_length=1, max_length=256)
    model_key: str = Field(min_length=1, max_length=256)


class DiscussionIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    request_id: str=Field(min_length=1,max_length=128)
    expected_version_ref: str=Field(min_length=1,max_length=256)
    assignment_ref: str=Field(min_length=1,max_length=256)

class MessageIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    work_ref: str = Field(default="", max_length=256)
    binding_ref: str=Field(min_length=1,max_length=256)
    body: str=Field(min_length=1,max_length=2000)
    request_id: str=Field(min_length=1,max_length=128)
    model_key: str=Field(min_length=1,max_length=256)
    expected_version_ref: str=Field(min_length=1,max_length=256)
    selection: dict
    references: list[dict]=Field(default_factory=list,max_length=8)

class CandidateIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    binding_ref: str=Field(min_length=1,max_length=256)
    attempt_id: str=Field(min_length=1,max_length=256)
    request_id: str=Field(min_length=1,max_length=128)

class CandidateFeedbackIn(BaseModel):
    model_config=ConfigDict(extra="forbid", strict=True)
    candidate_ref: str=Field(min_length=1,max_length=256)
    candidate_version: str
    basis_version_ref: str=Field(min_length=1,max_length=256)
    action: Literal["ACCEPT", "REVISE", "REJECT"]
    reason: str
    request_id: str

    @field_validator("candidate_version")
    @classmethod
    def valid_version(cls, value):
        if not re.fullmatch(r"[0-9a-f]{64}", value): raise ValueError("候选版本无效。")
        return value

    @field_validator("request_id")
    @classmethod
    def valid_request(cls, value):
        if str(UUID(value)) != value: raise ValueError("请求标识必须是规范 UUID。")
        return value

    @field_validator("reason")
    @classmethod
    def valid_reason(cls, value):
        if not value.strip() or len(value.strip().encode("utf-8")) > 2000:
            raise ValueError("请填写不超过 2000 UTF-8 字节的理由。")
        return value.strip()

class LearningIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    request_id: str=Field(min_length=1,max_length=128)
    expected_ref: str=Field(default="",max_length=256)
    data: dict

class AccountIn(BaseModel):
    model_config=ConfigDict(extra="forbid")
    data: dict

def build_content_growth_router(database,executor,*,service=None):
    service=service or ContentGrowthService(database)
    router=APIRouter(prefix="/api/workspace/v1/companies/{company}/content-growth/{workspace}")
    def invoke(callback):
        try: return callback()
        except (RuntimeScopeError,KeyError) as error: raise HTTPException(404,str(error)) from error
        except ContentGrowthConflict as error: raise HTTPException(409,str(error)) from error
        except (ValueError,TypeError,AttributeError) as error: raise HTTPException(422,str(error)) from error
    from ..content_growth_operating_service import ContentGrowthOperatingService
    operating = ContentGrowthOperatingService(database, service=service)

    @router.get("/operating-context")
    def operating_context(company: str, workspace: str):
        return invoke(lambda: operating.read(company, workspace))

    @router.post("/operating-context/{kind}")
    def operating_save(company: str, workspace: str, kind: Literal["Scope", "Snapshot", "Reference", "Direction", "Report", "Context"], payload: LearningIn):
        return invoke(lambda: operating.command(company, workspace, kind, **payload.model_dump()))

    @router.get("/contents/{content}/media")
    def media_collection(company: str, workspace: str, content: str):
        if service.media is None:
            invoke(lambda: service.content(company, workspace, content))
            return {"entry": invoke(lambda: service.entry.authoring_scope(company, workspace)), "configured": False, "records": []}
        return invoke(lambda: service.media.collection(service, company, workspace, content))

    @router.post("/contents/{content}/media")
    async def media_import(company: str, workspace: str, content: str, request: Request, metadata: str = Header(alias="X-CG-Import")):
        invoke(lambda: service.entry.authoring_scope(company, workspace, write=True))
        if service.media is None: raise HTTPException(422, "本地媒体尚未配置。")
        if len(metadata) > 8192: raise HTTPException(422, "导入依据超过边界。")
        try: payload = CommandIn.model_validate_json(unquote(metadata, errors="strict"))
        except ValueError as error: raise HTTPException(422, "导入依据不完整。") from error
        from ..content_growth_media_service import MIME
        mime = payload.data.get("mime")
        if not isinstance(mime, str) or mime not in MIME: raise HTTPException(422, "媒体格式不支持。")
        raw = bytearray()
        async for chunk in request.stream():
            if len(raw) + len(chunk) > MIME[mime][1]: raise HTTPException(413, "媒体实际字节超过允许大小。")
            raw.extend(chunk)
        return invoke(lambda: service.media.import_asset(service, company, workspace, content, payload.request_id, payload.expected_version_ref, payload.data, bytes(raw)))

    @router.post("/contents/{content}/media/adopt")
    def media_adopt(company: str, workspace: str, content: str, payload: LearningIn):
        if service.media is None or set(payload.data) != {"candidate_ref", "confirmed", "rights_confirmed"}: raise HTTPException(422, "采用依据不完整。")
        return invoke(lambda: service.media.adopt(service, company, workspace, content, payload.request_id, **payload.data))

    @router.get("/contents/{content}/media/{asset}")
    def media_bytes(company: str, workspace: str, content: str, asset: str, range_value: str | None = Header(default=None, alias="Range")):
        if service.media is None: raise HTTPException(404, "资产不可用。")
        raw, mime, status, headers = invoke(lambda: service.media.read(service, company, workspace, content, asset, range_value))
        return Response(raw, media_type=mime, status_code=status, headers=headers)

    @router.get("")
    def collection(company:str,workspace:str): return invoke(lambda:service.collection(company,workspace))
    @router.get("/materials")
    def materials(company:str,workspace:str): return invoke(lambda:service.materials(company,workspace))
    @router.get("/learnings")
    def learnings(company:str,workspace:str): return invoke(lambda:service.learning_collection(company,workspace))
    @router.post("/learnings/commands/{action}")
    def learning_command(company:str,workspace:str,action:str,payload:LearningIn):
        return invoke(lambda:service.learning_command(company,workspace,action,**payload.model_dump()))
    @router.get("/accounts")
    def accounts(company:str,workspace:str): return invoke(lambda:service.account_collection(company,workspace))
    @router.post("/accounts")
    def account_create(company:str,workspace:str,payload:AccountIn):
        return invoke(lambda:service.account_create(company,workspace,data=payload.data))
    @router.get("/accounts/{account}")
    def account(company:str,workspace:str,account:str): return invoke(lambda:service.account(company,workspace,account))
    @router.put("/accounts/{account}")
    def account_edit(company:str,workspace:str,account:str,payload:AccountIn):
        return invoke(lambda:service.account_edit(company,workspace,account,data=payload.data))
    @router.get("/verification-template/{platform_ref}")
    def verification_template(company:str,workspace:str,platform_ref:str):
        return invoke(lambda:service.verification_template(company,workspace,platform_ref))
    @router.get("/verifications")
    def verifications(company:str,workspace:str): return invoke(lambda:service.verification_collection(company,workspace))
    @router.post("/verifications")
    def verification_create(company:str,workspace:str,payload:LearningIn):
        return invoke(lambda:service.verification_create(company,workspace,request_id=payload.request_id,data=payload.data))
    @router.get("/verifications/{verification}")
    def verification(company:str,workspace:str,verification:str):
        return invoke(lambda:service.verification(company,workspace,verification))
    @router.get("/verifications/{verification}/export")
    def verification_export(company:str,workspace:str,verification:str):
        content,digest,filename=invoke(lambda:service.verification_export(company,workspace,verification))
        return Response(content,media_type="application/json",headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-SHA256": digest,"Cache-Control":"no-store"})
    @router.get("/verifications/{verification}/receipts")
    def receipts(company:str,workspace:str,verification:str):
        return invoke(lambda:service.receipt_collection(company,workspace,verification))
    @router.post("/verifications/{verification}/receipts")
    def receipt_create(company:str,workspace:str,verification:str,payload:LearningIn):
        return invoke(lambda:service.receipt_create(company,workspace,verification,request_id=payload.request_id,data=payload.data))
    @router.get("/receipts/{receipt}")
    def receipt(company:str,workspace:str,receipt:str):
        return invoke(lambda:service.receipt(company,workspace,receipt))
    @router.get("/observations")
    def observations(company:str,workspace:str):
        return invoke(lambda:service.observation_collection(company,workspace))
    @router.post("/observations")
    def observation_create(company:str,workspace:str,payload:LearningIn):
        return invoke(lambda:service.observation_create(company,workspace,request_id=payload.request_id,data=payload.data))
    @router.get("/observations/{observation}")
    def observation(company:str,workspace:str,observation:str):
        return invoke(lambda:service.observation(company,workspace,observation))
    @router.post("/model")
    def prepare_model(company: str, workspace: str, payload: ModelIn):
        invoke(lambda: service.entry.prepare_model(company, workspace, **payload.model_dump()))
        return {"prepared": True}

    @router.post("/contents")
    def create(company:str,workspace:str,payload:CommandIn):
        return invoke(lambda:service.command(company,workspace,"","create",**payload.model_dump()))
    @router.get("/contents/{content}")
    def content(company:str,workspace:str,content:str): return invoke(lambda:service.content(company,workspace,content))
    @router.post("/contents/{content}/commands/{action}")
    def command(company:str,workspace:str,content:str,action:str,payload:CommandIn):
        return invoke(lambda:service.command(company,workspace,content,action,**payload.model_dump()))
    @router.post("/contents/{content}/discussion")
    def bind(company:str,workspace:str,content:str,payload:DiscussionIn):
        return invoke(lambda:service.bind_discussion(company,workspace,content,**payload.model_dump()))
    @router.get("/contents/{content}/discussion/{binding}")
    def query(company:str,workspace:str,content:str,binding:str,request_id:str|None=None,attempt_id:str|None=None):
        return invoke(lambda:service.query_request(company,workspace,content,binding,request_id=request_id,attempt_id=attempt_id))
    @router.post("/contents/{content}/messages",status_code=202)
    def message(company:str,workspace:str,content:str,payload:MessageIn,background:BackgroundTasks):
        claim,created=invoke(lambda:service.prepare_message(company,workspace,content,**payload.model_dump()))
        if created: background.add_task(service.conversations.execute,claim,executor)
        return {"attempt":claim,"created":created}
    @router.post("/contents/{content}/reply-candidate")
    def candidate(company:str,workspace:str,content:str,payload:CandidateIn):
        return invoke(lambda:service.materialize_candidate(company,workspace,content,**payload.model_dump()))
    @router.post("/contents/{content}/candidate-feedback")
    def feedback(company:str,workspace:str,content:str,payload:CandidateFeedbackIn):
        return invoke(lambda:service.candidate_feedback(company,workspace,content,**payload.model_dump()))
    return router
