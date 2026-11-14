"""Conversation messages, reads and explicit Work confirmation."""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ..conversation_service import ConversationService
from ..runtime import RuntimeScopeError


class ReferenceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference_id: str = Field(min_length=1, max_length=256)
    workspace_id: str = Field(min_length=1, max_length=256)
    kind: str = Field(pattern="^(WORK|DECISION_PACKET|RESULT|ARTIFACT|EVIDENCE|KNOWLEDGE|CONTENT_ITEM|CONTENT_VERSION|PACKAGE_DOMAIN_OBJECT)$")

    version_ref: str | None = Field(default=None, min_length=1, max_length=256)
    purpose: str | None = Field(default=None, pattern="^(BACKGROUND|FACT|STYLE|CONSTRAINT)$")
    locator: str | None = Field(default=None, max_length=256)


class ConversationScopeIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_id: str = Field(min_length=1, max_length=256)
    workspace_id: str = Field(min_length=1, max_length=256)


class ConversationSelectedModelIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str = Field(pattern="^(official|tenant_private|marketplace)$")
    model_key: str = Field(min_length=1, max_length=256)


class ConversationExecutionSelectionIn(BaseModel):
    """Direct Employee dialogue model pick (purpose fixed server-side)."""
    model_config = ConfigDict(extra="forbid")
    purpose: str = Field(pattern="^CONVERSATION_REPLY$")
    binding_id: str | None = Field(default=None, min_length=1, max_length=256)
    scope: ConversationScopeIn
    model: ConversationSelectedModelIn


class MessageIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    body: str = Field(min_length=1, max_length=8000)
    request_id: str = Field(min_length=1, max_length=128)
    assignment_ref: str = Field(min_length=1, max_length=256)
    retry_no: int = Field(default=0, ge=0, le=1)
    references: list[ReferenceIn] = Field(default_factory=list, max_length=8)
    execution_selection: ConversationExecutionSelectionIn | None = None


class DiscussionScopeIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str = Field(min_length=1, max_length=256)
    assignment_ref: str = Field(min_length=1, max_length=256)
    object_ref: str | None = Field(default=None, min_length=1, max_length=256)


class TopicIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=1, max_length=128)
    title: str = Field(default="", max_length=120)
    discussion_scope: DiscussionScopeIn | None = None
    employee_ref: str | None = Field(default=None, max_length=256)


class TopicMessageIn(MessageIn):
    assignment_ref: str = Field(default="", max_length=256)


class ReceiveDialogueIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str = Field(min_length=1, max_length=256)
    message_ref: str = Field(min_length=1, max_length=256)
    source: dict


class JoinIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    employee_ref: str = Field(min_length=1, max_length=256)


class ConfirmResearchWorkIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message_ref: str = Field(min_length=1, max_length=256)
    proposal_version: str = Field(pattern="^[0-9a-f]{64}$")


def build_conversation_router(database, executor, *, service=None):
    router = APIRouter(prefix="/api/workspace/v1/companies/{company_id}/employees/{employee_ref}/conversation")
    service = service if service is not None else ConversationService(database)

    def read(company_id, employee_ref):
        return {**service.read(company_id, employee_ref),
                "assignments": service.available_assignments(company_id, employee_ref),
                "execution_models": service.execution_models(company_id, employee_ref),
                **service.conversation_metadata(company_id, employee_ref),
                "computer_access": service.computer_access(company_id, employee_ref)}

    @router.get("")
    def get_conversation(company_id: str, employee_ref: str):
        try:
            return read(company_id, employee_ref)
        except (KeyError, RuntimeScopeError):
            raise HTTPException(404, "当前员工对话不可访问，请从员工所在公司重新进入。")

    @router.post("/open")
    def open_conversation(company_id: str, employee_ref: str):
        try:
            service.open(company_id, employee_ref)
            return read(company_id, employee_ref)
        except (KeyError, RuntimeScopeError):
            raise HTTPException(404, "当前员工对话不可访问，请从员工所在公司重新进入。")

    @router.get("/references")
    def reference_options(company_id: str, employee_ref: str, assignment_ref: str):
        try:
            return {"references": service.reference_options(company_id, employee_ref, assignment_ref)}
        except (KeyError, RuntimeScopeError):
            raise HTTPException(404, "当前责任的来源不可访问，请重新选择工作范围。")

    @router.post("/messages", status_code=202)
    def send_message(company_id: str, employee_ref: str, payload: MessageIn, background: BackgroundTasks):
        try:
            claim, created = service.prepare(company_id, employee_ref, **payload.model_dump())
            if created:
                background.add_task(service.execute, claim, executor)
            return read(company_id, employee_ref)
        except (KeyError, RuntimeScopeError):
            raise HTTPException(404, "当前责任或员工绑定不可用。输入已保留，请检查员工的工作范围。")
        except ValueError:
            raise HTTPException(409, "消息尚未接手，请查看已有消息状态；不要重复提交。")

    topics = APIRouter(prefix="/api/workspace/v1/companies/{company_id}/conversations")

    def topic_read(company_id, conversation_id):
        value = service.read(company_id, conversation_id=conversation_id)
        employee_ref = value["owner_ref"]
        if employee_ref:
            employee = service.foundation.get(employee_ref)
            data = employee["data"]
            value["employee"] = {"employee_ref": employee_ref, "id": data.get("companyEmployeeRef") or employee_ref,
                                 "name": data.get("name") or "员工"}
            value["execution_models"] = service.execution_models(company_id, employee_ref)
            value.update(service.conversation_metadata(company_id, employee_ref))
        else:
            value["employee"] = None
            value["execution_models"] = []
        value["computer_access"] = service.computer_access(company_id, employee_ref)
        value["assignments"] = service.available_assignments(company_id, employee_ref) if employee_ref else []
        if value.get("discussion_scope"):
            scoped = value["discussion_scope"]
            value["assignments"] = [a for a in value["assignments"] if a["workspace_id"] == scoped["workspace_id"]
                and (not scoped.get("assignment_ref") or a["assignment_ref"] == scoped["assignment_ref"])]
        return value

    def safe(action):
        try:
            return action()
        except (KeyError, RuntimeScopeError):
            raise HTTPException(404, "这段对话或当前工作范围不可访问，请从所在公司重新进入。")
        except ValueError:
            raise HTTPException(409, "当前操作未确认完成，请重新读取已有记录后重试。")

    @router.post("/research-work/confirm")
    def confirm_employee_research_work(company_id: str, employee_ref: str, payload: ConfirmResearchWorkIn):
        return safe(lambda: service.confirm_research_work(
            company_id, employee_ref=employee_ref, **payload.model_dump()))

    @topics.post("/{conversation_id}/research-work/confirm")
    def confirm_topic_research_work(company_id: str, conversation_id: str, payload: ConfirmResearchWorkIn):
        return safe(lambda: service.confirm_research_work(
            company_id, conversation_id=conversation_id, **payload.model_dump()))

    @topics.get("")
    def recent_conversations(company_id: str, search: str = ""):
        return safe(lambda: {"conversations": service.recent(company_id, search=search[:120])})

    @topics.post("", status_code=201)
    def create_conversation(company_id: str, payload: TopicIn):
        return safe(lambda: topic_read(company_id, service.create(company_id, **payload.model_dump())["conversation_id"]))

    @topics.get("/employees")
    def employees(company_id: str):
        from ..result_attention import ResultAttention
        def read_employees():
            ResultAttention(database).actor(company_id)
            return {"employees": [{"employee_ref": row["entity_id"], "name": row["data"].get("name") or "员工"}
                                  for row in service.foundation.list("AI_EMPLOYEE", company_id=company_id)]}
        return safe(read_employees)

    @topics.get("/{conversation_id}")
    def get_topic(company_id: str, conversation_id: str):
        return safe(lambda: topic_read(company_id, conversation_id))

    @topics.post("/{conversation_id}/receive-result")
    def receive_result(company_id: str, conversation_id: str, payload: ReceiveDialogueIn):
        return safe(lambda: service.receive_dialogue(company_id, conversation_id, **payload.model_dump()))

    @topics.post("/{conversation_id}/employee")
    def join_employee(company_id: str, conversation_id: str, payload: JoinIn):
        def join():
            service.join(company_id, conversation_id, payload.employee_ref)
            return topic_read(company_id, conversation_id)
        return safe(join)

    @topics.post("/{conversation_id}/dismiss")
    def dismiss_conversation(company_id: str, conversation_id: str):
        return safe(lambda: service.dismiss(company_id, conversation_id))

    @topics.post("/{conversation_id}/messages", status_code=202)
    def send_topic(company_id: str, conversation_id: str, payload: TopicMessageIn, background: BackgroundTasks):
        def send():
            owner = service.owner(company_id, conversation_id=conversation_id)
            if owner["owner_ref"]:
                claim, created = service.prepare(company_id, owner["owner_ref"], conversation_id=conversation_id, **payload.model_dump())
                if created:
                    background.add_task(service.execute, claim, executor)
            else:
                if payload.retry_no:
                    raise ValueError("No provider attempt exists")
                if payload.execution_selection is not None:
                    raise ValueError("员工尚未加入对话，不能选择执行模型。")
                service.append_ceo(company_id, conversation_id=conversation_id,
                    **payload.model_dump(exclude={"retry_no", "execution_selection"}))
            return topic_read(company_id, conversation_id)
        return safe(send)

    combined = APIRouter()
    combined.include_router(router)
    combined.include_router(topics)
    return combined
