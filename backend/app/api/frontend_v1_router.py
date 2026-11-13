"""Small V1 frontend adapters over existing Company OS truth."""

from __future__ import annotations

import json
import uuid
from urllib.parse import urlencode
from typing import Any, Callable, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..database import Database
from ..runtime import RuntimeFoundation, RuntimeScopeError
from ..runtime.first_run_delivery import FirstGeneralWorkspaceDraft, FirstRunDelivery
from ..tenant_context import TenantContext
from ..result_attention import ResultAttention
from ..writing_entry_service import WritingEntryService
from ..shared_workspace_projection import canonical_work_status


class CompanyTextPolicyIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=1, max_length=128)
    expected_revision: str = Field(default="", max_length=128)
    enabled: bool
    consent: bool = False
    history_acknowledged: bool = False
    authorization_mode: Literal["standard", "synthetic_trial", "synthetic_continuous"] = "standard"
    workspace_ids: list[str] = Field(default_factory=list, max_length=100)
    model_keys: list[str] = Field(default_factory=list, max_length=100)
    budget_cny: str = Field(default="", max_length=32)
    valid_hours: int = Field(default=24, ge=1, le=168)
    preview_token: str = Field(default="", max_length=128)


class WritingTaskDraftIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    draft_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    text: str = Field(max_length=200000)
    expected_revision: int = Field(ge=0)


class PresentationIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    welcome_dismissed: bool = False
    display_name: str = Field(default="", max_length=80)
    avatar_ref: str = Field(default="", max_length=260_000)

    @field_validator("display_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise ValueError("display name contains unsafe characters")
        return value

    @field_validator("avatar_ref")
    @classmethod
    def safe_avatar(cls, value: str) -> str:
        if not value or value.startswith("preset:"):
            return value
        if value.startswith(("data:image/png;base64,", "data:image/jpeg;base64,", "data:image/webp;base64,")):
            return value
        raise ValueError("avatar must be a Curis preset or a local image")


class ExistingCompanyBusinessIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    business_name: str = Field(min_length=1, max_length=120)
    goal: str = Field(min_length=1, max_length=2000)
    positioning: str = Field(default="", max_length=2000)
    workspace_name: str = Field(min_length=1, max_length=120)
    intent_summary: str = Field(default="", max_length=2000)
    package_id: str = Field(default="", max_length=128)
    department_id: str = Field(default="", max_length=128)
    proposal_sha256: str = Field(default="", max_length=64)
    retry_no: int = Field(default=0, ge=0, le=1)


class BusinessDraftIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: str = Field(min_length=1, max_length=2000)
    business_name: str = Field(min_length=1, max_length=120)
    goal: str = Field(min_length=1, max_length=2000)
    positioning: str = Field(default="", max_length=2000)
    workspace_name: str = Field(min_length=1, max_length=120)
    company_id: str = Field(default="", max_length=128)
    package_id: str = Field(default="", max_length=128)
    department_id: str = Field(default="", max_length=128)



class ConversationReferenceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference_id: str = Field(min_length=1, max_length=256)
    workspace_id: str = Field(min_length=1, max_length=256)


class AssistantMessageIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1, max_length=4000)
    model_key: str = Field(default="", max_length=256)
    references: list[ConversationReferenceIn] = Field(default_factory=list, max_length=8)


class ResultViewedIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str = Field(min_length=1, max_length=256)
    result_ref: str = Field(min_length=1, max_length=256)
    result_version: str = Field(pattern=r"^[0-9a-f]{64}$")


class ResultResponseIn(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    workspace_id: str = Field(min_length=1, max_length=256)
    result_ref: str = Field(pattern=r"^task:[^\s]{1,250}$")
    result_version: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_work_ref: str = Field(min_length=1, max_length=256)
    action: Literal["ACCEPT", "REVISE", "REJECT"]
    reason: str
    request_id: str

    @field_validator("reason")
    @classmethod
    def response_reason(cls, value: str) -> str:
        value = value.strip()
        if not value or len(value.encode("utf-8")) > 2000:
            raise ValueError("请填写不超过 2000 UTF-8 字节的理由。")
        return value

    @field_validator("request_id")
    @classmethod
    def response_request_id(cls, value: str) -> str:
        try:
            if str(uuid.UUID(value)) != value:
                raise ValueError
        except ValueError as error:
            raise ValueError("请求标识必须是规范 UUID。") from error
        return value


def _presentation_key() -> str:
    identity = TenantContext.current_identity()
    ceo_id = identity.get("ceo_id") or "local-ceo"
    return f"v1.presentation.{TenantContext.current_tenant_id()}.{ceo_id}"


def _presentation(database: Database) -> dict[str, Any]:
    raw = database.get_setting(_presentation_key(), "") or ""
    try:
        value = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        value = {}
    return {
        "welcome_dismissed": bool(value.get("welcome_dismissed")),
        "display_name": str(value.get("display_name") or ""),
        "avatar_ref": str(value.get("avatar_ref") or ""),
    }


def _attention_item(row: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(row.get("data_json") or "{}")
    kind = row["entity_type"]
    status = row["lifecycle_status"]
    exception = row.get("exception_status") or "NONE"
    waiting_decision = kind == "DECISION_PACKET" and status == "WAITING_CEO"
    failed = exception != "NONE" or status in {"FAILED", "BLOCKED", "INVALIDATED", "REQUIRES_REPAIR"}
    handoff = kind == "HANDOFF" and status not in {"ACKNOWLEDGED", "COMPLETED", "CANCELLED"}
    result_review = kind in {"RESULT", "OUTCOME", "ACCEPTANCE"} and status in {"PENDING", "IN_REVIEW", "WAITING_CEO"}
    follow_up = bool(row.get("next_check_at"))
    rank = 1 if waiting_decision else 2 if failed else 3 if handoff else 4 if result_review else 5 if follow_up else 6
    routing = data.get("responsibilityRouting") or {}
    work_ref = ""
    recovery = ""
    if kind == "WORK":
        work_ref = row["entity_id"]
        status = canonical_work_status(row)
        latest = list((routing.get("executions") or {}).values())[-1:] or [{}]
        human = routing.get("humanInput") or {}
        needs_human = human.get("state") in {"WAITING_INPUT", "LOCAL_REPORTED", "EXTERNAL_REPORTED_UNKNOWN", "READY"}
        failed = exception != "NONE" or status in {"FAILED", "BLOCKED"} or (
            status == "WAITING" and latest[0].get("status") in {"FAILED", "PARTIAL", "REJECTED", "CANCELLED", "UNVERIFIED"})
        rank = 1 if status == "WAITING_DECISION" else 2 if failed else 3 if needs_human else 5 if follow_up else 6
        if status in {"COMPLETED", "CANCELLED", "ARCHIVED", "PAUSED", "UNKNOWN"}:
            rank = 6
        cycle = json.loads(row.get("cycle_data_json") or "{}")
        data = {**data, "title": (cycle.get("contract") or {}).get("problem") or (data.get("workContext") or {}).get("activity"),
                "reason": (row.get("transition_reason") if status == row["lifecycle_status"] else "") or routing.get("cancelReason") or latest[0].get("resultSummary") or routing.get("problem") or human.get("whyUser") or ""}
        recovery = "回到原工作核对执行与证据；确认恢复条件后再决定"
        if status == "WAITING_DECISION":
            recovery = "回到原工作查看当前决定"
        elif needs_human:
            recovery = str(human.get("userAction") or "回到原工作补充必要信息")
    summary = next((str(data.get(key) or "").strip() for key in (
        "event", "summary", "title", "reason", "goal", "responsibility", "expectedResult"
    ) if str(data.get(key) or "").strip()), "有一项经营事实需要查看")
    return {
        "source_ref": row["entity_id"],
        "source_type": kind,
        "workspace_id": row.get("workspace_id") or "",
        "status": status,
        "exception_status": exception,
        "owner_ref": routing.get("responsibilityHolderRef") or row.get("owner_ref") or "",
        "responsibility_ref": str(data.get("responsibilityRef") or data.get("responsibility_ref") or ""),
        "current_executor": str(routing.get("currentExecutorRef") or data.get("currentExecutor") or data.get("current_executor") or ""),
        "evidence_refs": list(data.get("evidenceRefs") or data.get("evidence_refs") or []),
        "summary": summary,
        "next_check_at": row.get("next_check_at"),
        "updated_at": row.get("updated_at"),
        "rank": rank,
        "work_ref": work_ref,
        "reason": str(data.get("reason") or ""),
        "recovery_action": recovery,
    }


AssistantModelCall = Callable[[str, str], dict[str, Any]]


def build_frontend_v1_router(
    database: Database, assistant_model_call: AssistantModelCall | None = None, *, writing_entry_service=None, content_growth_entry_service=None, music_entry_service=None,
) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/v1", tags=["frontend-v1"])
    foundation = RuntimeFoundation(database)
    first_run = FirstRunDelivery(database)
    result_attention = ResultAttention(database)
    writing_entry = writing_entry_service or WritingEntryService(database)
    from ..content_growth_entry_service import ContentGrowthEntryService, PACKAGE_ID as CG_PACKAGE_ID, ASSETS as CG_ASSETS
    cg_entry = content_growth_entry_service or ContentGrowthEntryService(database)
    from ..music_entry_service import MusicEntryService, PACKAGE_ID as MUSIC_PACKAGE_ID, ASSETS as MUSIC_ASSETS
    music_entry = music_entry_service or MusicEntryService(database)

    from ..first_launch_service import FirstLaunchService
    launch = FirstLaunchService(database)

    @router.post("/first-launch")
    def first_launch():
        try:
            return launch.ensure()
        except RuntimeScopeError as error:
            raise HTTPException(403, str(error)) from None
        except ValueError as error:
            raise HTTPException(409, str(error)) from None

    @router.put("/companies/{company_id}/writing/{workspace_id}/task-draft")
    def save_writing_task_draft(company_id: str, workspace_id: str, payload: WritingTaskDraftIn):
        try:
            return launch.save_draft(company_id, workspace_id, payload.draft_id, payload.text, payload.expected_revision)
        except (RuntimeScopeError, KeyError):
            raise HTTPException(404, "任务不属于当前工作空间。") from None
        except ValueError as error:
            raise HTTPException(409, str(error)) from None

    @router.get("/companies/{company_id}/writing/{workspace_id}/task-drafts/{work_id}")
    def read_writing_task_draft(company_id: str, workspace_id: str, work_id: str):
        try:
            return launch.read_draft(company_id, workspace_id, work_id)
        except (RuntimeScopeError, KeyError):
            raise HTTPException(404, "任务不属于当前工作空间。") from None

    @router.get("/companies/{company_id}/text-execution-policy")
    def company_text_policy(company_id: str):
        from ..company_execution_policy import CompanyExecutionPolicy
        try:
            return CompanyExecutionPolicy(database).read(company_id)
        except (RuntimeScopeError, KeyError):
            raise HTTPException(404, "当前公司或文字许可不可访问。") from None

    @router.put("/companies/{company_id}/text-execution-policy")
    def save_company_text_policy(company_id: str, payload: CompanyTextPolicyIn):
        from ..company_execution_policy import CompanyExecutionPolicy
        try:
            values = payload.model_dump(exclude={"authorization_mode"})
            if payload.authorization_mode == "synthetic_trial":
                from ..company_execution_policy import TRIAL_AUTHORIZATION
                values["trial_authorization_ref"] = TRIAL_AUTHORIZATION
            elif payload.authorization_mode == "synthetic_continuous":
                from ..company_execution_policy import CONTINUOUS_TEST_AUTHORIZATION
                values["test_authorization_ref"] = CONTINUOUS_TEST_AUTHORIZATION
            return CompanyExecutionPolicy(database).save(company_id, **values)
        except (RuntimeScopeError, KeyError):
            raise HTTPException(403, "当前身份、工作范围或模型不允许此许可。") from None
        except ValueError as error:
            raise HTTPException(409, str(error)) from None

    def assistant_conversation(company_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        foundation._require_company(company_id)
        identity_company = TenantContext.current_identity().get("company_id")
        if identity_company and identity_company != company_id:
            raise RuntimeScopeError("Company identity does not match")
        assistants = foundation.list("CEO_ASSISTANT", company_id=company_id)
        if len(assistants) != 1:
            raise RuntimeScopeError("Company requires exactly one CEO Assistant")
        messages = assistants[0]["data"].get("v1Conversation") or []
        return assistants[0], [item for item in messages if isinstance(item, dict)][-40:]

    @router.get("/presentation")
    def get_presentation() -> dict[str, Any]:
        return _presentation(database)

    @router.put("/presentation")
    def put_presentation(payload: PresentationIn) -> dict[str, Any]:
        value = payload.model_dump()
        database.set_setting(_presentation_key(), json.dumps(value, ensure_ascii=False))
        return value

    @router.get("/companies/{company_id}/attention")
    def get_attention(company_id: str) -> dict[str, Any]:
        try:
            result_attention.actor(company_id)
            foundation._require_company(company_id)
            identity_company = TenantContext.current_identity().get("company_id")
            if identity_company and identity_company != company_id:
                raise RuntimeScopeError("Company identity does not match")
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="公司不存在或无权访问") from error
        with database.connect() as connection:
            company = connection.execute(
                "select company_id, name, status, updated_at from companies where tenant_id=? and company_id=?",
                (foundation.tenant_id, company_id),
            ).fetchone()
            workspace_count = connection.execute(
                "select count(*) from workspaces where tenant_id=? and company_id=? and business_relation_status='RESOLVED'",
                (foundation.tenant_id, company_id),
            ).fetchone()[0]
            rows = connection.execute(
                "select e.*, (select p.data_json from runtime_entities p where p.tenant_id=e.tenant_id "
                "and p.company_id=e.company_id and p.workspace_id is e.workspace_id "
                "and p.entity_id=e.parent_id and p.entity_type='CYCLE') cycle_data_json, "
                "(select t.reason from runtime_transition_log t where t.tenant_id=e.tenant_id "
                "and t.company_id=e.company_id and t.workspace_id is e.workspace_id and t.entity_type='work' "
                "and t.entity_id=e.entity_id and t.target=e.lifecycle_status order by t.rowid desc limit 1) transition_reason "
                "from runtime_entities e where e.tenant_id=? and e.company_id=? "
                "and e.entity_type in ('WORK','DECISION_PACKET','HANDOFF','EVIDENCE','OUTCOME','ACCEPTANCE','CYCLE','RESPONSIBILITY_ASSIGNMENT')",
                (foundation.tenant_id, company_id),
            ).fetchall()
        items = []
        by_id = {row["entity_id"]: dict(row) for row in rows}
        for row in rows:
            item = _attention_item(dict(row))
            item["owner_name"] = ""
            if item["owner_ref"] == "CEO":
                item["owner_name"] = "CEO"
            elif item["owner_ref"]:
                with database.connect() as connection:
                    holder = connection.execute(
                        "select coalesce(i.name,json_extract(e.data_json,'$.name')) name from runtime_entities e "
                        "left join employee_instances i on i.tenant_id=e.tenant_id and i.company_id=e.company_id "
                        "and i.id=coalesce(json_extract(e.data_json,'$.companyEmployeeRef'),e.entity_id) "
                        "and i.enabled=1 and i.deleted_at is null "
                        "where e.tenant_id=? and e.company_id=? and e.entity_id=? and e.entity_type='AI_EMPLOYEE' "
                        "and (e.workspace_id is null or e.workspace_id is ?)",
                        (foundation.tenant_id, company_id, item["owner_ref"], item["workspace_id"] or None),
                    ).fetchone()
                item["owner_name"] = str(holder["name"] or "") if holder else ""
            if item["source_type"] == "WORK":
                packet = by_id.get((json.loads(row["data_json"] or "{}").get("responsibilityRouting") or {}).get("decisionPacketRef"))
                if packet and packet["entity_type"] == "DECISION_PACKET" and packet["workspace_id"] == row["workspace_id"] and packet["lifecycle_status"] == "WAITING_CEO":
                    continue
            if item["source_type"] == "DECISION_PACKET":
                original = by_id.get(json.loads(row["data_json"] or "{}").get("workRef") or row["parent_id"])
                if original and original["entity_type"] == "WORK" and original["workspace_id"] == row["workspace_id"]:
                    if original["lifecycle_status"] in {"COMPLETED", "CANCELLED", "ARCHIVED"}:
                        continue
                    item["work_ref"] = original["entity_id"]
            # Decisions use their lifecycle, never viewing receipts. Ranking a
            # historical item is not proof that it still needs CEO attention.
            if item["source_type"] == "DECISION_PACKET":
                if item["status"] == "WAITING_CEO":
                    items.append(item)
            elif item["rank"] < 6:
                items.append(item)
        items.extend(result_attention.unseen_results(company_id))
        items = list({item["source_ref"]: item for item in items}.values())
        items.sort(key=lambda item: (
            item["rank"], item.get("next_check_at") or "9999", item.get("updated_at") or "", item["source_ref"]
        ))
        return {
            "company": dict(company) if company else None,
            "workspace_count": workspace_count,
            "state": "QUIET" if not items else "PARTIAL",
            "items": items,
            "unavailable": ["company_importance_scoring", "predicted_return_time"],
        }

    @router.get("/companies/{company_id}/result-detail")
    def get_result_detail(company_id: str, workspace_id: str, result_ref: str) -> dict[str, Any]:
        try:
            return result_attention.detail(company_id, workspace_id, result_ref)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="结果不存在或无权访问，请返回原工作查看。") from error

    @router.post("/companies/{company_id}/result-viewed")
    def view_result(company_id: str, payload: ResultViewedIn) -> dict[str, Any]:
        try:
            return result_attention.mark_viewed(company_id, payload.workspace_id, payload.result_ref, payload.result_version)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="结果不存在或无权访问，请返回原工作查看。") from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.post("/companies/{company_id}/result-response")
    def respond_to_result(company_id: str, payload: ResultResponseIn) -> dict[str, Any]:
        try:
            return result_attention.decide_response(company_id, workspace_id=payload.workspace_id,
                result_ref=payload.result_ref, result_version_value=payload.result_version,
                source_work_ref=payload.source_work_ref, action=payload.action,
                reason=payload.reason, request_id=payload.request_id)
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail="结果或原工作不在当前公司范围。") from error
        except ValueError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.get("/companies/{company_id}/assistant/conversation")
    def get_assistant_conversation(company_id: str) -> dict[str, Any]:
        try:
            assistant, messages = assistant_conversation(company_id)
            return {
                "assistant": {
                    "assistant_id": assistant["entity_id"],
                    "name": assistant["data"].get("name") or "CEO 助理",
                    "role": assistant["data"].get("role") or "公司级协调与经营跟进",
                },
                "messages": messages,
            }
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.post("/companies/{company_id}/assistant/conversation")
    def post_assistant_message(company_id: str, payload: AssistantMessageIn) -> dict[str, Any]:
        try:
            assistant, messages = assistant_conversation(company_id)
            references = []
            for ref in payload.references:
                result = result_attention.detail(company_id, ref.workspace_id, ref.reference_id)
                references.append({
                    "reference_id": ref.reference_id, "workspace_id": ref.workspace_id,
                    "kind": result["kind"], "title": result.get("title") or "查看来源",
                    "href": "/ceo-office/workspace?" + urlencode({
                        "workspace_id": ref.workspace_id, "result_workspace": ref.workspace_id,
                        "result_ref": ref.reference_id,
                    }),
                })
            if assistant_model_call is None:
                raise RuntimeError("CEO Assistant model execution is unavailable")
            with database.connect() as connection:
                company = connection.execute(
                    "select name from companies where tenant_id=? and company_id=?",
                    (foundation.tenant_id, company_id),
                ).fetchone()
            recent = "\n".join(
                f"{item.get('role')}: {str(item.get('text') or '')[:1000]}" for item in messages[-6:]
            )
            prompt = (
                f"你是 {assistant['data'].get('name') or 'CEO 助理'}，负责协调公司经营，不替代专业员工。\n"
                f"公司：{company['name'] if company else company_id}\n"
                f"最近对话：\n{recent or '无'}\n"
                f"CEO：{payload.message.strip()}\n"
                f"CEO明确选择的来源引用（仅标识，未加载全文）：{json.dumps(references, ensure_ascii=False)}\n"
                "请用简洁中文回答；未知事实明确说明未知，不得伪造业务结果。"
            )
            result = assistant_model_call(prompt, payload.model_key)
            output = str(result.get("output") or "").strip()
            if not output:
                raise RuntimeError("CEO Assistant model returned no response")
            next_messages = [
                *messages,
                {"message_id": str(uuid.uuid4()), "role": "user", "text": payload.message.strip(), "references": references},
                {
                    "message_id": str(uuid.uuid4()),
                    "role": "assistant",
                    "text": output[:8000],
                    "provider": str(result.get("provider") or ""),
                    "model": str(result.get("model") or ""),
                    "references": references,
                },
            ][-40:]
            data = {**assistant["data"], "v1Conversation": next_messages}
            with database.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=current_timestamp "
                    "where tenant_id=? and company_id=? and entity_id=? and entity_type='CEO_ASSISTANT'",
                    (json.dumps(data, ensure_ascii=False), foundation.tenant_id, company_id, assistant["entity_id"]),
                )
            return {
                "assistant_id": assistant["entity_id"],
                "messages": next_messages,
                "provider": str(result.get("provider") or ""),
                "model": str(result.get("model") or ""),
            }
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except (RuntimeError, ValueError) as error:
            raise HTTPException(status_code=503, detail="助理暂时无法回复。你的输入仍保留，请检查模型连接后重试。") from error

    @router.get("/companies/{company_id}/business-definitions")
    def business_definitions(company_id: str):
        try:
            writing = writing_entry.definitions(company_id)
            cg = cg_entry.definitions(company_id)
            music = music_entry.definitions(company_id)
            return {**writing, "definitions": [item["definition"] for item in (writing, cg, music) if item["available"]],
                    "notices": [item["notice"] for item in (writing, cg, music) if not item["available"] and item.get("notice")]}
        except (RuntimeScopeError, ValueError) as error:
            raise HTTPException(403, str(error)) from error

    @router.get("/companies/{company_id}/founding-runs/{founding_run_id}/business-result")
    def business_creation_result(company_id: str, founding_run_id: str):
        try:
            ceo = writing_entry.actor(company_id)
            return first_run.package_creation_status(founding_run_id, company_id, ceo)
        except (RuntimeScopeError, ValueError, KeyError) as error:
            raise HTTPException(409, str(error)) from error

    @router.post("/companies/{company_id}/founding-runs/{founding_run_id}/business")
    def create_business(company_id: str, founding_run_id: str, payload: ExistingCompanyBusinessIn) -> dict[str, Any]:
        identity = TenantContext.current_identity()
        if identity.get("ceo_id") != payload.ceo_id:
            raise HTTPException(status_code=403, detail="CEO 身份不匹配")
        try:
            if payload.package_id:
                writing_entry.actor(company_id, write=True)
                service = music_entry if payload.package_id == MUSIC_PACKAGE_ID else cg_entry if payload.package_id == CG_PACKAGE_ID else writing_entry
                definition = service.publication()
                if payload.package_id != definition["package_id"]:
                    raise ValueError("写作组件与确认依据不一致。")
                from ..workspace_package_runtime import WorkspacePackageRuntime
                from ..writing_entry_service import ASSETS
                return first_run.materialize_package_for_existing_company(founding_run_id,
                    FirstGeneralWorkspaceDraft(company_id=company_id, ceo_id=payload.ceo_id, company_name="",
                        department_name="", business_name=payload.business_name, goal=payload.goal,
                        positioning=payload.positioning, workspace_name=payload.workspace_name,
                        intent_summary=payload.intent_summary), package_runtime=WorkspacePackageRuntime(database),
                    source=(MUSIC_ASSETS / "music" if payload.package_id == MUSIC_PACKAGE_ID else CG_ASSETS / ("content_growth_v02" if definition["version"] == "0.2.0" else "content_growth") if payload.package_id == CG_PACKAGE_ID else ASSETS / "writing_authoring"), definition=definition,
                    department_id=payload.department_id, proposal_sha256=payload.proposal_sha256, retry_no=payload.retry_no)
            return first_run.materialize_for_existing_company(
                founding_run_id,
                FirstGeneralWorkspaceDraft(
                    company_id=company_id,
                    ceo_id=payload.ceo_id,
                    company_name="",
                    department_name="业务部",
                    business_name=payload.business_name,
                    goal=payload.goal,
                    positioning=payload.positioning,
                    workspace_name=payload.workspace_name,
                    intent_summary=payload.intent_summary,
                    recommendation_reason="当前没有经过验证的专业工作空间匹配，先从通用工作空间开始。",
                ),
            )
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.put("/founding-runs/{founding_run_id}/business-draft")
    def save_business_draft(founding_run_id: str, payload: BusinessDraftIn) -> dict[str, Any]:
        try:
            run = foundation.get(founding_run_id)
            identity = TenantContext.current_identity()
            if run["entity_type"] != "FOUNDING_RUN" or run["owner_ref"] != identity.get("ceo_id"):
                raise RuntimeScopeError("FoundingRun is outside the current CEO scope")
            if run["lifecycle_status"] in {"COMPANY_CREATED", "ABANDONED"}:
                raise ValueError("FoundingRun no longer accepts draft changes")
            proposal = payload.model_dump()
            professional = bool(payload.package_id or (run["data"].get("v1Proposal") or {}).get("package_id"))
            if professional:
                if run["lifecycle_status"] == "CEO_CONFIRMED" or (run["data"].get("v1Activation") or {}).get("status") in {"RUNNING", "COMPLETED"}:
                    raise ValueError("原确认正在处理或结果待核验；不能改写它的提案。")
                proposal = (music_entry if payload.package_id == MUSIC_PACKAGE_ID else cg_entry if payload.package_id == CG_PACKAGE_ID else writing_entry).proposal(payload.company_id, proposal)
            else:
                proposal = {key: proposal[key] for key in ("intent", "business_name", "goal", "positioning", "workspace_name")}
            with database.connect() as connection:
                connection.execute("begin immediate")
                current = connection.execute("select lifecycle_status,data_json from runtime_entities where tenant_id=? and entity_id=?",
                    (foundation.tenant_id, founding_run_id)).fetchone()
                data = json.loads(current["data_json"])
                if professional and (current["lifecycle_status"] != "PROPOSED"
                    or (data.get("v1Activation") or {}).get("status") in {"RUNNING", "COMPLETED"}):
                    raise ValueError("确认状态已变化，保留原提案并重新读取。")
                data["v1Proposal"] = proposal
                connection.execute("update runtime_entities set data_json=?, updated_at=current_timestamp where tenant_id=? and entity_id=?",
                    (json.dumps(data, ensure_ascii=False), foundation.tenant_id, founding_run_id))
            return foundation.get(founding_run_id)
        except (KeyError, RuntimeScopeError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @router.get("/founding-runs/{founding_run_id}/business-draft")
    def get_business_draft(founding_run_id: str) -> dict[str, Any]:
        try:
            run = foundation.get(founding_run_id)
            identity = TenantContext.current_identity()
            if run["entity_type"] != "FOUNDING_RUN" or run["owner_ref"] != identity.get("ceo_id"):
                raise RuntimeScopeError("FoundingRun is outside the current CEO scope")
            return {
                "founding_run_id": founding_run_id,
                "lifecycle_status": run["lifecycle_status"],
                "proposal": run["data"].get("v1Proposal"),
            }
        except (KeyError, RuntimeScopeError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    return router
