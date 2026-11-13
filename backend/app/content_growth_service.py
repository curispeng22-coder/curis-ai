"""Graphic authoring over canonical Content/Version and Shared Conversation."""
from __future__ import annotations
import json
import hashlib
import re
from uuid import UUID
from datetime import datetime, timezone
from .runtime import RuntimeFoundation, RuntimeScopeError
from .runtime.workspace import WorkspaceRuntime
from .tenant_context import TenantContext
from .conversation_service import ConversationService, digest
from .resource_scope_policy import ResourceScopePolicy
from .content_growth_entry_service import ContentGrowthEntryService, PURPOSE, CONTENT_PURPOSE, FORMATS, VERSION, VERSION_2

class ContentGrowthConflict(ValueError):
    pass

# Platform chain S1 (contract CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT §2, D1/D2):
# fixed read-only 6-platform catalog; ChannelAccount is a business-level long-lived
# operating unit stored like CG Learning (PACKAGE_DOMAIN_OBJECT, UNVERIFIED/MISSING).
PLATFORM_CATALOG = (
    {"platform": "xhs", "name": "小红书"},
    {"platform": "douyin", "name": "抖音"},
    {"platform": "wechat_oa", "name": "公众号"},
    {"platform": "tiktok", "name": "TikTok"},
    {"platform": "youtube", "name": "YouTube"},
    {"platform": "bilibili", "name": "bilibili"},
)
ACCOUNT_GROWTH_STAGES = ("cold_start", "growing", "mature", "declining_transforming")
ACCOUNT_STATUS = ("active", "dormant", "banned")
ACCOUNT_CONNECTION_STATUS = "NOT_CONNECTED"
ACCOUNT_TEXT_FIELDS = ("positioning", "audience", "content_mix", "cadence", "voice", "responsibility")
ACCOUNT_CREATE_FIELDS = frozenset({"platform_ref", "name", "growth_stage", "status", *ACCOUNT_TEXT_FIELDS})
ACCOUNT_EDIT_FIELDS = frozenset({"name", "growth_stage", "status", *ACCOUNT_TEXT_FIELDS})

# Platform chain S2 (contract §4.2, D1/D4): per-account no-send verification checklists.
# The three primary platforms carry production-chain templates; the other three carry
# common compliance items only. Server-owned labels; clients submit keys + results only.
VERIFY_PLATFORM_CHECKS = {
    "xhs": (
        ("cover", "封面"),
        ("title_keywords", "标题关键词"),
        ("tags_topics", "标签话题"),
        ("graphic_format", "图文格式"),
    ),
    "douyin": (
        ("cover_title", "封面标题"),
        ("duration_subtitles", "时长字幕"),
    ),
    "wechat_oa": (
        ("layout", "排版"),
        ("title_summary_cover", "标题·摘要·封面"),
    ),
}
# Minimal engineering reading of the contract's "common compliance items" for the
# non-primary platforms; Owner Review may amend. Not merged into primary templates.
VERIFY_COMMON_CHECKS = (
    ("copyright", "版权与素材授权"),
    ("compliance", "内容合规（无违法违规与敏感信息）"),
    ("honesty", "表述真实（数据与效果不夸大、不伪造）"),
)
VERIFY_CREATE_FIELDS = frozenset({"content_ref", "account_ref", "checks"})
VERIFY_NOTICE = "本地核验导出，不构成发布；平台连接不存在。"

# Platform chain S3 (contract §4.3/§4.4): CEO manual point-in-time records only.
# Receipt backfill fields are all optional per the contract, but at least one must be
# non-empty (an empty receipt is no evidence); observations mirror Music/Writing
# observation fields (title/body/scope_ref/period), but every save is a NEW revision=1
# immutable entity per contract §1.2 — no version chain.
RECEIPT_CREATE_FIELDS = frozenset({"published_at", "platform_post_url", "note"})
RECEIPT_NOTICE = "人工回填 · 未验证"
OBSERVATION_CREATE_FIELDS = frozenset({"title", "body", "scope_ref", "period"})
OBSERVATION_NOTICE = "人工观察 · 未验证；分析仅基于人工观察，样本不足不下结论。"

def exact(data, fields):
    if not isinstance(data, dict) or set(data) != set(fields):
        raise ValueError("命令字段不完整或包含未知字段。")

def learning_text(value, limit, *, empty=True):
    if not isinstance(value, str) or len(value) > limit or (not empty and not value.strip()):
        raise ValueError("文字为空或超过允许长度。")
    return value

class ContentGrowthService:
    def __init__(self, database, *, entry=None, conversations=None, media=None):
        self.db = database
        self.media = media
        self.entry = entry or ContentGrowthEntryService(database)
        self.foundation = RuntimeFoundation(database)
        self.workspace = WorkspaceRuntime(database)
        self.conversations = conversations or ConversationService(database)

    def collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and entity_type='CONTENT_ITEM' and json_extract(data_json,'$.format') in ('graphic','short_video','long_video','speech') order by created_at,entity_id",
                (TenantContext.current_tenant_id(),company,workspace)).fetchall()
            bindings = con.execute("select payload from evolution_events where tenant_id=? and event_type='cg.discussion.bound' "
                "and json_extract(payload,'$.scope.company_id')=? and json_extract(payload,'$.scope.workspace_id')=?",
                (TenantContext.current_tenant_id(),company,workspace)).fetchall()
        items = [self.content(company,workspace,r["entity_id"]) for r in rows]
        pending=[]
        for row in bindings:
            binding=json.loads(row["payload"])
            result=self.conversations.read_request(company,binding["conversation_id"])
            for attempt in result["attempts"]:
                if attempt["status"] in {"RUNNING","UNKNOWN","UNVERIFIED"}:
                    pending.append({"content_ref":binding["content_ref"],"binding_ref":binding["binding_ref"],
                        "conversation_id":binding["conversation_id"],"attempt_id":attempt["attempt_id"],"status":attempt["status"]})
        models=self.entry.models.available_models()
        for model in models:
            try:
                grant = self.entry.models.professional_grant(self.entry.execution_grant, company, workspace, model["model_key"])
                self.entry.models.require_professional_grant(grant, company, workspace, model["model_key"])
                model.update(execution_authorized=True, execution_notice="当前公司许可已核对；发送时仍会重验范围与费用额度。")
            except (KeyError, ValueError, RuntimeScopeError) as error:
                model.update(execution_authorized=False, execution_notice=str(error))
        info["model_preference"] = self.entry.models.read_current()["preference"]
        for assignment in info["assignments"]:
            assignment["models"] = models
        sources=[]
        with self.db.connect() as con:
            rows=con.execute("select entity_id,entity_type from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and entity_type in ('WORK','DECISION_PACKET','CONTENT_ITEM','CONTENT_VERSION')",
                (TenantContext.current_tenant_id(),company,workspace)).fetchall()
        for ref in rows:
            try: sources.extend(self.resolve_references(info["scope"],[{"reference_id":ref["entity_id"],"workspace_id":workspace,
                "kind":ref["entity_type"],"purpose":"BACKGROUND" if info["definition"]["version"] == VERSION else "CONTEXT","locator":""}]))
            except (ValueError,KeyError,RuntimeScopeError): continue
        # These are actual scoped sources. An empty list means genuinely unconnected.
        return {"contents":items,"pending_requests":pending,"entry":info,"reference_options":sources,
                "execution_authorized":any(model["execution_authorized"] for model in models),
                "execution_notice":"本地编辑与人工采用可用；真实员工建议需当前员工、模型、费用与系统授权。",
                "account_notice":"尚未连接目标账号；本地内容不等于发布。"}

    def materials(self, company, workspace):
        """CG-REFERENCE-01: read-only material library listing. Same authorization as collection."""
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            rows = con.execute("select entity_id,entity_type from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and entity_type in ('WORK','DECISION_PACKET','CONTENT_ITEM','CONTENT_VERSION') order by created_at,entity_id",
                (TenantContext.current_tenant_id(),company,workspace)).fetchall()
        items = []
        for row in rows:
            try:
                resolved = self.resolve_references(info["scope"], [{"reference_id": row["entity_id"], "workspace_id": workspace,
                    "kind": row["entity_type"], "purpose": "BACKGROUND" if info["definition"]["version"] == VERSION else "CONTEXT", "locator": ""}])
                if resolved:
                    items.append({**resolved[0], "entity_type": row["entity_type"]})
            except (ValueError, KeyError, RuntimeScopeError):
                continue
        return {"materials": items, "entry": info}

    def content(self, company, workspace, content_ref, *, connection=None):
        scope_info=self.entry.authoring_scope(company,workspace,connection=connection)
        def read(con):
            item=self.workspace._entity_row(con,content_ref)
            if (item["entity_type"] != "CONTENT_ITEM" or item["company_id"] != company or item["workspace_id"] != workspace
                    or item["data"].get("format") not in (("graphic",) if item["blueprint_version"] == VERSION else FORMATS)):
                raise RuntimeScopeError("内容不在当前图文工作空间。")
            rows=con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and parent_id=? and entity_type='CONTENT_VERSION' order by created_at,entity_id",
                (TenantContext.current_tenant_id(),company,workspace,content_ref)).fetchall()
            versions=[self.workspace._entity_row(con,r["entity_id"]) for r in rows]
            head=next((v for v in versions if v["entity_id"] == item["current_version_id"]),None)
            if not head:
                raise RuntimeScopeError("当前版本的内容父级不一致。")
            malformed = con.execute("select 1 from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type in ('cg.candidate.created','cg.candidate.feedback') "
                "and case when json_valid(payload) then json_type(payload) else 'invalid' end!='object' limit 1",
                (TenantContext.current_tenant_id(), content_ref)).fetchone()
            if malformed:
                raise ContentGrowthConflict("候选来源或反馈记录格式无法核验。")
            adopted={v["data"].get("source_candidate_ref") for v in versions}
            candidates=[]
            for version in versions:
                if version["data"].get("kind") != "candidate": continue
                reasons=[]
                if version["data"].get("basis_version_ref") != head["entity_id"]: reasons.append("正文已改变，请查看原版本并重新准备候选。")
                try: self.resolve_references(self.entry.authoring_scope(company,workspace,connection=con)["scope"],version["data"].get("references",[]))
                except (ValueError,RuntimeScopeError,KeyError) as error: reasons.append(str(error))
                if version["data"].get("targetAccountRefs"): reasons.append("目标账号依据未获验证。")
                try: self.check_qualification(self.entry.authoring_scope(company,workspace,connection=con), version["data"])
                except (ValueError, RuntimeScopeError, KeyError) as error: reasons.append(str(error))
                if version["data"].get("source_class") == "MANUAL_CANDIDATE":
                    try: self._feedback_source(con, company, workspace, content_ref, version["entity_id"])
                    except (ValueError, RuntimeScopeError, ContentGrowthConflict, KeyError, TypeError, AttributeError) as error:
                        reasons.append(str(error))
                from .content_growth_operating_service import ContentGrowthOperatingService
                context = ContentGrowthOperatingService(self.db, service=self).context(con, scope_info, content_ref, version["data"].get("basis_version_ref", ""))
                if version["data"].get("context_basis_ref", "") != (context["ref"] if context else ""):
                    reasons.append("人工方向或来源已有变化，请保留原候选并重新核对。")
                feedback_version = digest([version["entity_id"], version["data"]])
                receipt = con.execute("select * from evolution_events where tenant_id=? and event_type='cg.candidate.feedback' "
                    "and correlation_id=? and case when json_valid(payload) then json_extract(payload,'$.candidate_ref') end=? "
                    "and case when json_valid(payload) then json_extract(payload,'$.ceo_id') end=? "
                    "and case when json_valid(payload) then json_extract(payload,'$.candidate_version') end=? order by event_id limit 1",
                    (TenantContext.current_tenant_id(), content_ref, version["entity_id"], scope_info["actor"], feedback_version)).fetchone()
                if receipt:
                    stored = json.loads(receipt["payload"])
                    if (not isinstance(stored, dict) or stored.get("company_id") != company
                            or stored.get("workspace_id") != workspace or stored.get("content_ref") != content_ref
                            or stored.get("candidate_ref") != version["entity_id"]
                            or stored.get("candidate_version") != feedback_version
                            or stored.get("basis_version_ref") != version["data"].get("basis_version_ref")
                            or stored.get("ceo_id") != scope_info["actor"]
                            or stored.get("action") not in {"ACCEPT", "REVISE", "REJECT"}
                            or not isinstance(stored.get("reason"), str) or not stored["reason"].strip()):
                        raise ContentGrowthConflict("候选反馈记录无法核验。")
                    feedback = {**stored, "tenant_id": receipt["tenant_id"],
                        "receipt_ref": receipt["event_id"], "decided_at": receipt["created_at"]}
                else:
                    feedback = None
                if version["entity_id"] in adopted:
                    reasons = ["已采用，请查看采用版本。"]
                candidates.append({"version":version,"reasons":reasons,"eligible":not reasons,
                    "feedback_version":feedback_version,"feedback":feedback})
            from .content_growth_operating_service import ContentGrowthOperatingService
            context = ContentGrowthOperatingService(self.db, service=self).context(con, scope_info, content_ref, head["entity_id"])
            return {"content":item,"version":head,"versions":versions,"candidates":candidates,"operating_context":context}
        if connection is not None: return read(connection)
        with self.db.connect() as con: return read(con)

    def _feedback_source(self, con, company, workspace, content_ref, candidate_ref):
        info = self.entry.authoring_scope(company, workspace, connection=con, write=True, feedback=True)
        tenant = info["scope"]["tenant_id"]
        item = self.workspace._entity_row(con, content_ref)
        candidate = self.workspace._entity_row(con, candidate_ref)
        if (item["entity_type"] != "CONTENT_ITEM" or item["company_id"] != company
                or item["workspace_id"] != workspace or item["tenant_id"] != tenant
                or item["blueprint_version"] != info["definition"]["version"]
                or candidate["entity_type"] != "CONTENT_VERSION" or candidate["parent_id"] != content_ref
                or candidate["company_id"] != company or candidate["workspace_id"] != workspace
                or candidate["tenant_id"] != tenant):
            raise RuntimeScopeError("候选不属于当前内容工作空间。")
        data = candidate["data"]
        if not isinstance(data, dict):
            raise ContentGrowthConflict("候选保存资料无法核验。")
        if (data.get("kind") != "candidate" or data.get("source_class") != "MANUAL_CANDIDATE"
                or data.get("manual_actor") != info["actor"] or candidate["owner_ref"] != info["actor"]
                or data.get("task_ref") or data.get("attempt_id") or data.get("provenance")):
            raise RuntimeScopeError("这不是当前 CEO 创建的人工候选。")
        events = con.execute("select payload from evolution_events where tenant_id=? and event_type='cg.candidate.created' "
            "and correlation_id=? and case when json_valid(payload) then json_extract(payload,'$.version_ref') end=?",
            (tenant, content_ref, candidate_ref)).fetchall()
        malformed = con.execute("select 1 from evolution_events where tenant_id=? and event_type='cg.candidate.created' "
            "and correlation_id=? and case when json_valid(payload) then json_type(payload) else 'invalid' end!='object' limit 1",
            (tenant, content_ref)).fetchone()
        if malformed:
            raise ContentGrowthConflict("候选原创建记录格式无法核验。")
        if len(events) != 1:
            raise RuntimeScopeError("候选缺少唯一原创建记录。")
        try:
            creation = json.loads(events[0]["payload"])
        except (TypeError, json.JSONDecodeError) as error:
            raise ContentGrowthConflict("候选原创建记录无法核验。") from error
        original = creation.get("request") if isinstance(creation, dict) else None
        submitted = original.get("data") if isinstance(original, dict) else None
        if (not isinstance(submitted, dict) or creation.get("version_ref") != candidate_ref
                or original.get("actor") != info["actor"]
                or original.get("expected_version_ref") != data.get("basis_version_ref")
                or any(submitted.get(key) != data.get(key) for key in ("title", "topic", "audience", "body", "selection"))
                or submitted.get("target_account_refs") not in (None, [])
                or submitted.get("format", "graphic") != data.get("format")):
            raise RuntimeScopeError("候选原创建依据不一致。")
        # The creation event stores the submitted references while the candidate
        # stores their resolved snapshots. Every submitted source must survive.
        def source_identity(reference):
            if not isinstance(reference, dict):
                raise ContentGrowthConflict("候选原引用资料无效。")
            return tuple(reference.get(key) for key in ("reference_id", "workspace_id", "kind", "version_ref", "purpose", "locator"))
        originals = submitted.get("references", [])
        saved = data.get("references")
        if (not isinstance(originals, list) or not isinstance(saved, list)
                or [source_identity(ref) for ref in originals] != [source_identity(ref) for ref in saved]
                or len(originals) != len(saved)
                or any("title" in original and original["title"] != persisted.get("title")
                    for original, persisted in zip(originals, saved))):
            raise ContentGrowthConflict("候选原引用与保存来源不一致。")
        submitted_work, saved_work = submitted.get("work"), data.get("work")
        if submitted_work is not None or saved_work is not None:
            if not isinstance(submitted_work, dict) or not isinstance(saved_work, dict):
                raise ContentGrowthConflict("候选原脚本来源无效。")
            if any(submitted_work.get(key) != saved_work.get(key) for key in self.WORK_FIELDS - {"source_refs"}):
                raise ContentGrowthConflict("候选原脚本与保存版本不一致。")
            raw_sources, saved_sources = submitted_work.get("source_refs"), saved_work.get("source_refs")
            if (not isinstance(raw_sources, list) or not isinstance(saved_sources, list)
                    or [source_identity(ref) for ref in raw_sources] != [source_identity(ref) for ref in saved_sources]
                    or len(raw_sources) != len(saved_sources)
                    or any("title" in original and original["title"] != persisted.get("title")
                        for original, persisted in zip(raw_sources, saved_sources))):
                raise ContentGrowthConflict("候选原脚本引用与保存来源不一致。")
        basis = self.workspace._entity_row(con, data.get("basis_version_ref") or "")
        if (basis["entity_type"] != "CONTENT_VERSION" or basis["parent_id"] != content_ref
                or basis["tenant_id"] != tenant or basis["company_id"] != company
                or basis["workspace_id"] != workspace or basis["blueprint_version"] != item["blueprint_version"]):
            raise RuntimeScopeError("候选原版本不属于当前内容。")
        self.selection(basis, data.get("selection"))
        return info, item, candidate, basis

    def _feedback_current(self, con, info, item, candidate, basis):
        from .content_growth_operating_service import ContentGrowthOperatingService
        current = ContentGrowthOperatingService(self.db, service=self).context(con, info, item["entity_id"], basis["entity_id"])
        if candidate["data"].get("context_basis_ref", "") != (current["ref"] if current else ""):
            raise ContentGrowthConflict("候选的人工方向/依据已变化，请重新核对。")
        if item["current_version_id"] != basis["entity_id"]:
            raise ContentGrowthConflict("正文已改变，请先核对原候选依据。")
        data = candidate["data"]
        if data.get("targetAccountRefs"):
            raise ContentGrowthConflict("目标账号依据未获验证。")
        references = list(data.get("references") or []) + list((data.get("work") or {}).get("source_refs") or [])
        for ref in references:
            if not isinstance(ref, dict) or ref.get("kind") not in {"WORK", "DECISION_PACKET", "CONTENT_ITEM", "CONTENT_VERSION"}:
                raise ContentGrowthConflict("候选引用需重新核对。")
            entity = self.workspace._entity_row(con, ref.get("reference_id") or "")
            if entity["entity_type"] != ref["kind"]:
                raise ContentGrowthConflict("候选引用类型已改变。")
            ResourceScopePolicy.require_same_execution_scope(info["scope"],
                ResourceScopePolicy.reference_scope(con, tenant_id=info["scope"]["tenant_id"],
                    company_id=info["scope"]["company_id"], reference_id=entity["entity_id"]))
            version = entity["current_version_id"] if entity["entity_type"] == "CONTENT_ITEM" else (
                entity["entity_id"] if entity["entity_type"] == "CONTENT_VERSION" else digest(entity))
            if ref.get("version_ref") != version:
                raise ContentGrowthConflict("候选引用版本已改变。")
        work = data.get("work") or {}
        qualification = data.get("qualification") or {}
        if not work:
            return
        tenant, company, workspace = info["scope"]["tenant_id"], info["scope"]["company_id"], info["scope"]["workspace_id"]
        current = {"sources": work.get("source_refs"), "assignment": None, "model": None}
        if work.get("assignment_ref"):
            assignment = self.workspace._entity_row(con, work["assignment_ref"])
            if (assignment["entity_type"] != "RESPONSIBILITY_ASSIGNMENT" or assignment["lifecycle_status"] != "ACTIVE"
                    or assignment["data"].get("responsibilityKey") != "CONTENT_AUTHOR"):
                raise ContentGrowthConflict("候选责任来源已改变。")
            employee_ref = assignment["data"].get("employeeRef")
            context = ResourceScopePolicy.authorize_assignment(con, tenant_id=tenant, company_id=company,
                assignment_ref=work["assignment_ref"], employee_ref=employee_ref, scope=info["scope"])
            runtime = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and (workspace_id is null or workspace_id=?) and entity_id=? and entity_type='AI_EMPLOYEE'",
                (tenant, company, workspace, employee_ref)).fetchone()
            bridge = json.loads(runtime["data_json"] or "{}") if runtime else {}
            employee_id = bridge.get("companyEmployeeRef")
            employee = con.execute("select id,name from employee_instances where tenant_id=? and company_id=? "
                "and id=? and enabled=1 and deleted_at is null", (tenant, company, employee_id)).fetchone()
            if not employee or employee_id != work.get("recipient_ref"):
                raise ContentGrowthConflict("候选原员工身份已改变。")
            context.update(name=employee["name"], company_employee_ref=employee_id)
            current["assignment"] = {"assignment": digest(assignment), "context": context}
        elif work.get("recipient_ref") or work.get("model_key"):
            raise ContentGrowthConflict("候选责任与模型依据不完整。")
        if work.get("model_key"):
            model = self._feedback_model_in_connection(con, tenant, work["model_key"])
            if not model:
                raise ContentGrowthConflict("候选原模型资格已改变。")
            bindings = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? "
                "and capability_source=? and capability_id=? and capability_type='model' and enabled=1",
                (tenant, work["recipient_ref"], model["source"], model["model_key"])).fetchall()
            if len(bindings) != 1:
                raise ContentGrowthConflict("候选原员工模型绑定已改变。")
            current["model"] = {"model": model, "binding": digest(dict(bindings[0]))}
        if current != qualification:
            raise ContentGrowthConflict("候选原脚本来源、责任或模型资格已改变。")

    @staticmethod
    def _feedback_model_in_connection(con, tenant, model_key):
        official = con.execute("select * from official_models where model_key=? and source='official' "
            "and status='active' and gateway_ref!='freellmapi.experimental'", (model_key,)).fetchone()
        if official:
            item = dict(official)
            supported = json.loads(item["supported_models"] or "[]")
            name = item.get("default_model") or (supported[0] if supported else "")
            if not name: return None
            return {"model_key": model_key, "provider_id": item["provider_id"], "display_name": item["display_name"],
                "gateway_ref": item["gateway_ref"], "model_name": str(name), "source": "official",
                "status": item["status"], "updated_at": item["updated_at"]}
        private = con.execute("select * from tenant_private_capabilities where tenant_id=? and capability_type='model' "
            "and capability_id=? and source='tenant_private' and status='active'", (tenant, model_key)).fetchone()
        if not private: return None
        metadata = json.loads(private["metadata_json"] or "{}")
        if (metadata.get("provider_type") == "freellmapi.experimental"
                or metadata.get("credential_ref") == "env:FREELLMAPI_API_KEY"
                or str(metadata.get("base_url") or "").rstrip("/") in
                {"http://127.0.0.1:3101", "http://localhost:3101", "http://freellmapi:3001"}):
            return None
        provider, name = str(metadata.get("provider_type") or ""), str(metadata.get("model_name") or "")
        verification = metadata.get("discovery_verification") or {}
        discovery = str(verification.get("discovery_id") or name)
        expected = f"user.{provider}.{hashlib.sha256(discovery.encode('utf-8')).hexdigest()[:16]}"
        if (not provider or not name or model_key != expected or verification.get("status") != "verified"
                or verification.get("provider_id") != provider or verification.get("model_id") != name):
            return None
        if verification.get("requires_credential"):
            credential = con.execute("select 1 from credential_metadata where tenant_id=? and credential_ref=? "
                "and status='active' and provider=?", (tenant, str(metadata.get("credential_ref") or ""), provider)).fetchone()
            if not credential: return None
        return {"model_key": model_key, "provider_id": provider, "display_name": private["display_name"] or name,
            "gateway_ref": provider, "model_name": name, "source": "tenant_private",
            "status": private["status"], "updated_at": private["updated_at"]}

    def candidate_feedback(self, company, workspace, content_ref, *, candidate_ref, candidate_version,
                           basis_version_ref, action, reason, request_id):
        values = (company, workspace, content_ref, candidate_ref, basis_version_ref, action, request_id)
        if (any(type(value) is not str or not value or value != value.strip() for value in values)
                or type(candidate_version) is not str or not re.fullmatch(r"[0-9a-f]{64}", candidate_version)
                or action not in {"ACCEPT", "REVISE", "REJECT"} or type(reason) is not str):
            raise ValueError("人工候选反馈字段无效。")
        try:
            if str(UUID(request_id)) != request_id: raise ValueError
        except ValueError as error:
            raise ValueError("请求标识必须是规范 UUID。") from error
        reason = reason.strip()
        if not reason or len(reason.encode("utf-8")) > 2000:
            raise ValueError("请填写不超过 2000 UTF-8 字节的理由。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info, item, candidate, basis = self._feedback_source(con, company, workspace, content_ref, candidate_ref)
            if basis["entity_id"] != basis_version_ref:
                raise ContentGrowthConflict("候选原版本已改变。")
            version = digest([candidate["entity_id"], candidate["data"]])
            tenant, actor = info["scope"]["tenant_id"], info["actor"]
            payload = {"company_id": company, "workspace_id": workspace, "content_ref": content_ref,
                "candidate_ref": candidate_ref, "candidate_version": candidate_version,
                "basis_version_ref": basis_version_ref, "ceo_id": actor, "action": action,
                "reason": reason, "request_id": request_id}
            key = "cg.candidate.feedback:" + digest([tenant, company, workspace, content_ref, candidate_ref, actor, request_id])
            prior = con.execute("select * from evolution_events where tenant_id=? and idempotency_key=?", (tenant, key)).fetchone()
            if prior:
                event = self.conversations.events._event_from_row(prior)
                if (event["tenant_id"] != tenant or event["event_type"] != "cg.candidate.feedback"
                        or event["correlation_id"] != content_ref or event["payload"] != payload):
                    raise ContentGrowthConflict("相同请求不能更换候选或选择。")
                return {**payload, "receipt_ref": event["event_id"], "decided_at": event["created_at"], "replayed": True}
            if version != candidate_version:
                raise ContentGrowthConflict("候选版本已变化。")
            self._feedback_current(con, info, item, candidate, basis)
            count = con.execute("select count(*) from evolution_events where tenant_id=? and event_type='cg.candidate.feedback' "
                "and correlation_id=? and case when json_valid(payload) then json_extract(payload,'$.candidate_ref') end=? "
                "and case when json_valid(payload) then json_extract(payload,'$.candidate_version') end=?",
                (tenant, content_ref, candidate_ref, candidate_version)).fetchone()[0]
            if count:
                raise ContentGrowthConflict("此候选版本已经保存过人类选择。")
            event = self.conversations.events.record_in_connection(con, correlation_id=content_ref,
                event_type="cg.candidate.feedback", payload=payload, idempotency_key=key)
            return {**payload, "receipt_ref": event["event_id"], "decided_at": event["created_at"], "replayed": False}

    # Business purposes survive unchanged; Shared alone resolves source qualification.
    REFERENCE_ADAPTER = {"ORIGINAL":"BACKGROUND", "PATTERN":"STYLE", "EVIDENCE":"FACT", "DIRECTION":"CONSTRAINT", "CONTEXT":"BACKGROUND"}
    WORK_FIELDS = {"goal","shots","recording_requirements","output_intent","output_spec","source_refs","assignment_ref","recipient_ref","model_key"}

    def technical_references(self, references):
        return [{**r, "purpose": self.REFERENCE_ADAPTER.get(r["purpose"], r["purpose"])} for r in references]

    def work_metadata(self, info, work):
        if not isinstance(work,dict) or set(work) != self.WORK_FIELDS:
            raise ValueError("脚本依据字段不完整或包含未授权媒体/来源字段。")
        limits = {"goal":1000,"recording_requirements":2000,"output_spec":1000,"assignment_ref":256,"recipient_ref":256,"model_key":256}
        for k,limit in limits.items():
            if not isinstance(work[k],str) or len(work[k]) > limit: raise ValueError("脚本依据超出字段边界。")
        if work["output_intent"] not in {"UNCONFIRMED","AUDIO","VIDEO"}: raise ValueError("请明确本次输出意图。")
        shots=work["shots"]
        if not isinstance(shots,list) or len(shots)>40: raise ValueError("镜头数量超出边界。")
        ids=set()
        for shot in shots:
            if not isinstance(shot,dict) or set(shot) != {"id","title","description","camera","caption","sound","duration"}: raise ValueError("镜头字段不完整。")
            for k,limit in {"id":128,"title":240,"description":2000,"camera":1000,"caption":1000,"sound":1000}.items():
                if not isinstance(shot[k],str) or len(shot[k])>limit: raise ValueError("镜头字段超出边界。")
            if not shot["id"] or shot["id"] in ids or type(shot["duration"]) not in {int,float} or not 0 <= shot["duration"] <= 600:
                raise ValueError("镜头需要唯一稳定标识和有效时长。")
            ids.add(shot["id"])
        sources=self.resolve_references(info["scope"],work["source_refs"])
        qualification={"sources":sources, "assignment":None, "model":None}
        assignment=None
        if work["assignment_ref"]:
            assignment=next((a for a in info["assignments"] if a["assignment_ref"]==work["assignment_ref"]),None)
            if not assignment or assignment["company_employee_ref"] != work["recipient_ref"]: raise RuntimeScopeError("原责任或收件员工当前不合法。")
            actual=self.foundation.get(work["assignment_ref"])
            qualification["assignment"]={"assignment":digest(actual),"context":assignment}
        elif work["recipient_ref"] or work["model_key"]: raise ValueError("请先明确真实责任员工。")
        if work["model_key"]:
            model=self.entry.models._require_eligible_model(info["scope"]["tenant_id"],work["model_key"])
            with self.db.connect() as con:
                bindings=con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? and capability_source=? and capability_id=? and capability_type='model' and enabled=1",
                    (info["scope"]["tenant_id"],work["recipient_ref"],model["source"],model["model_key"])).fetchall()
            if len(bindings)!=1: raise RuntimeScopeError("原模型与员工能力授权不再一致。")
            qualification["model"]={"model":model,"binding":digest(dict(bindings[0]))}
        stored=json.loads(json.dumps(work));stored["source_refs"]=sources
        return {"work":stored,"qualification":qualification}

    def check_qualification(self, info, data):
        if info["definition"]["version"] == VERSION: return
        fresh=self.work_metadata(info,data["work"])
        if fresh["qualification"] != data["qualification"]: raise ContentGrowthConflict("原脚本来源、责任或模型资格已改变。")

    def draft_metadata(self, info, data, *, candidate=False):
        legacy=info["definition"]["version"]==VERSION
        allowed={"title","topic","audience","body","target_account_refs","references","selection"} | (set() if legacy else {"format","work"})
        if not isinstance(data,dict) or set(data)-allowed or data.get("target_account_refs"): raise ValueError("未知字段或目标账号绑定未获验证。")
        for key,limit in (("title",240),("topic",1000),("audience",1000),("body",20000)):
            if not isinstance(data.get(key),str) or len(data[key])>limit or (key != "body" or candidate) and not data[key].strip():
                raise ValueError("请填写标题、主题和受众；候选正文不能为空。")
        format=data.get("format","graphic")
        if format not in (("graphic",) if legacy else FORMATS): raise ValueError("内容格式未获授权。")
        metadata={"format":format,"topic":data["topic"],"audience":data["audience"],"targetAccountRefs":[],"references":self.resolve_references(info["scope"],data.get("references",[])),"kind":"draft"}
        if not legacy: metadata.update(self.work_metadata(info,data.get("work")))
        return metadata

    def resolve_references(self, scope, references):
        if not isinstance(references,list) or len(references)>8: raise ValueError("最多选择八项有界来源。")
        if any(not isinstance(r,dict) or set(r)-{"reference_id","workspace_id","kind","title","version_ref","purpose","locator"}
                or not r.get("purpose") for r in references):
            raise ValueError("引用需要明确的来源和用途。")
        info=self.entry.authoring_scope(scope["company_id"],scope["workspace_id"])
        if info["definition"]["version"] == VERSION: return self.conversations.references(scope["company_id"],scope,references)
        if any(r["purpose"] not in self.REFERENCE_ADAPTER for r in references): raise ValueError("请使用明确的内容业务引用用途。")
        result=[]
        for original in references:
            resolved=self.conversations.references(scope["company_id"],scope,self.technical_references([original]))[0]
            value={**resolved,"purpose":original["purpose"]}
            if value not in result: result.append(value)
        return result

    def selection(self, version, selection):
        if isinstance(selection,dict) and selection.get("locator")=="shot":
            if set(selection)!={"version_ref","locator","shot_id","shot_snapshot"} or selection["version_ref"]!=version["entity_id"]:
                raise ContentGrowthConflict("镜头来自原版本，请重新选择。")
            shot=next((s for s in version["data"].get("work",{}).get("shots",[]) if s["id"]==selection["shot_id"]),None)
            if not shot or shot!=selection["shot_snapshot"] or not any(shot[k].strip() for k in ("title","description","caption")):
                raise ContentGrowthConflict("镜头依据不一致或没有有效脚本输入。")
            return json.loads(json.dumps(selection))
        if not isinstance(selection,dict) or set(selection) != {"version_ref","start","end","excerpt","locator"}:
            raise ValueError("请在保存后的正文中重新选择片段。")
        body=version["data"].get("body","")
        if (selection["version_ref"] != version["entity_id"] or type(selection["start"]) is not int or type(selection["end"]) is not int
                or not 0 <= selection["start"] < selection["end"] <= len(body.encode("utf-16-le"))//2
                or selection["locator"] != "body"):
            raise ContentGrowthConflict("选段来自旧版本，只能查看原依据；请重新选择。")
        try: actual=body.encode("utf-16-le")[selection["start"]*2:selection["end"]*2].decode("utf-16-le")
        except UnicodeDecodeError as error: raise ValueError("选段不能切开字符。") from error
        if actual != selection["excerpt"]: raise ContentGrowthConflict("选段与保存正文不一致。")
        return dict(selection)

    def _save_with_context(self, info, content_ref, request_id, expected_version_ref, values, metadata, context_ref):
        """Same canonical content insert; pin companion provenance in the atomic save receipt."""
        from hashlib import sha256
        from .content_growth_operating_service import ContentGrowthOperatingService
        with self.db.connect() as con:
            con.execute("begin immediate")
            content=self.workspace._entity_row(con,content_ref)
            current_info=self.workspace._require_content_authoring_scope(con,content)
            if current_info["scope"]!=info["scope"] or current_info["actor"]!=info["actor"]:
                raise RuntimeScopeError("正文保存范围已变化。")
            if self.draft_metadata(current_info,values)!=metadata or metadata["format"]!=content["data"]["format"]:
                raise ContentGrowthConflict("脚本结构或资格已变化。")
            data={"platform":content["data"]["platform"],"platformVariant":"","payloadRef":"","author":info["actor"],
                "constraintsCheck":"LOCAL_AUTHORING_NO_PUBLICATION","versionStatus":"READY","title":values["title"].strip(),
                "body":values["body"],"tags":[],"coverRef":"","scheduledFor":None,**metadata}
            request={"author":info["actor"],"expected_version_ref":expected_version_ref,"data":data}
            key="cg:save:"+sha256(json.dumps([info["scope"]["tenant_id"],content_ref,info["actor"],request_id]).encode()).hexdigest()
            old=con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",(info["scope"]["tenant_id"],key)).fetchone()
            if old:
                receipt=json.loads(old[0])
                if receipt["request"]!=request: raise ContentGrowthConflict("同一请求不能更换正文或依据。")
                return receipt["version_ref"]
            current=ContentGrowthOperatingService(self.db,service=self).context(con,current_info,content_ref,expected_version_ref)
            if not current or current["ref"]!=context_ref: raise ContentGrowthConflict("本次作品依据已变化，请保留输入并重新核对。")
            version=self.workspace._insert_content_version_in_connection(con,content,data,info["actor"],head=True,expected=expected_version_ref)
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (info["scope"]["tenant_id"],content_ref,"cg.content.saved",json.dumps({"request":request,"version_ref":version,"context_ref":context_ref},ensure_ascii=False),key))
            return version

    def command(self, company, workspace, content_ref, action, *, request_id, expected_version_ref="", data):
        if not isinstance(request_id,str) or not 1 <= len(request_id) <= 128: raise ValueError("缺少有界请求标识。")
        info=self.entry.authoring_scope(company,workspace,write=True)
        if action in {"create","save","candidate"}:
            metadata=self.draft_metadata(info,data,candidate=action=="candidate")
            refs=metadata["references"]
            if action == "create":
                item,_=self.workspace.create_content_item(company_id=company,workspace_id=workspace,blueprint_version=info["blueprint_version"],
                    platform="",owner_ref=info["actor"],outcome_ref="",intent_ref=data["topic"],platform_variant="",payload_ref="",
                    author=info["actor"],constraints_check="LOCAL_AUTHORING_NO_PUBLICATION",title=data["title"],body=data["body"],
                    format=metadata["format"],topic=data["topic"],audience=data["audience"],references=refs,request_id=request_id,start_draft=True,
                    script_metadata={k:metadata[k] for k in ("work","qualification") if k in metadata})
                return self.content(company,workspace,item["entity_id"])
            row=self.content(company,workspace,content_ref)
            if metadata["format"] != row["content"]["data"]["format"]: raise ValueError("既有内容不能换形态，请显式新建。")
            if action == "save":
                from .content_growth_operating_service import ContentGrowthOperatingService
                with self.db.connect() as context_connection:
                    previous_context = ContentGrowthOperatingService(self.db, service=self).context(context_connection, info, content_ref, expected_version_ref)
                if previous_context:
                    self._save_with_context(info,content_ref,request_id,expected_version_ref,data,metadata,previous_context["ref"])
                else:
                    self.workspace.add_content_version(content_ref,platform_variant="",payload_ref="",author=info["actor"],
                        constraints_check="LOCAL_AUTHORING_NO_PUBLICATION",title=data["title"],body=data["body"],
                        expected_version_ref=expected_version_ref,request_id=request_id,metadata=metadata)
            else:
                with self.db.connect() as con:
                    con.execute("begin immediate")
                    row=self.content(company,workspace,content_ref,connection=con)
                    self.workspace._require_content_authoring_scope(con,row["content"])
                    request={"data":data,"expected_version_ref":expected_version_ref,"actor":info["actor"]}
                    key="cg:candidate:"+digest([info["scope"],content_ref,request_id])
                    old=con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",(TenantContext.current_tenant_id(),key)).fetchone()
                    if old:
                        if json.loads(old[0])["request"] != request: raise ContentGrowthConflict("候选请求不能更换依据。")
                    else:
                        if row["version"]["entity_id"] != expected_version_ref: raise ContentGrowthConflict("正文已改变，请重新准备候选。")
                        if info["definition"]["version"] != VERSION:
                            basis=row["version"]["data"]
                            if any(metadata[k]!=basis[k] for k in metadata if k!="kind") or data["title"]!=basis["title"]:
                                raise ContentGrowthConflict("候选必须保留完整原脚本依据。")
                        selected=self.selection(row["version"],data["selection"])
                        if refs != self.resolve_references(info["scope"],refs): raise ContentGrowthConflict("引用版本已改变。")
                        from .content_growth_operating_service import ContentGrowthOperatingService
                        manual_context = ContentGrowthOperatingService(self.db, service=self).context(con, info, content_ref, expected_version_ref)
                        candidate={**row["version"]["data"],**metadata,"kind":"candidate","title":data["title"],"body":data["body"],
                            "basis_version_ref":expected_version_ref,"selection":selected,"source_class":"MANUAL_CANDIDATE",
                            "manual_actor":info["actor"], "context_basis_ref": manual_context["ref"] if manual_context else ""}
                        ref=self.workspace._insert_content_version_in_connection(con,row["content"],candidate,info["actor"])
                        con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'cg.candidate.created',?,?)",
                            (TenantContext.current_tenant_id(),content_ref,json.dumps({"request":request,"version_ref":ref},ensure_ascii=False),key))
            return self.content(company,workspace,content_ref)
        if action == "adopt":
            if set(data) != {"candidate_ref","checks"} or not isinstance(data["checks"],dict) or any(v is not True for v in data["checks"].values()):
                raise ValueError("请明确完成三个采用检查。")
            with self.db.connect() as con:
                con.execute("begin immediate")
                row=self.content(company,workspace,content_ref,connection=con)
                candidate=next((v for v in row["versions"] if v["entity_id"] == data["candidate_ref"]),None)
                if not candidate: raise RuntimeScopeError("候选不存在于当前内容。")
                key="cg:adopt:"+hashlib.sha256(json.dumps([info["scope"],content_ref,info["actor"],request_id],sort_keys=True).encode()).hexdigest()
                replay=con.execute("select 1 from evolution_events where tenant_id=? and idempotency_key=?",(TenantContext.current_tenant_id(),key)).fetchone()
                if not replay:
                    selected=next(c for c in row["candidates"] if c["version"]["entity_id"] == candidate["entity_id"])
                    if selected["reasons"]: raise ContentGrowthConflict("；".join(selected["reasons"]))
                    basis=next(v for v in row["versions"] if v["entity_id"] == candidate["data"]["basis_version_ref"])
                    if candidate["data"].get("source_class") == "CONVERSATION_REPLY":
                        source = candidate["data"]["dialogue_source"]
                        proof = self.conversations.dialogue_result(con, company, workspace, content_ref,
                            source["conversation_ref"], source["message_ref"])
                        if proof["text"] != candidate["data"]["body"] or proof["provenance"] != candidate["data"]["provenance"]:
                            raise ContentGrowthConflict("原对话结果来源已变化。")
                    else:
                        self.selection(basis,candidate["data"]["selection"])
                if not replay and candidate["data"].get("provenance", {}).get("execution_selection", {}).get("work_ref"):
                    self.conversations.accept_model_work(con, provenance=candidate["data"]["provenance"],
                        task_ref=candidate["data"]["task_ref"], candidate_ref=candidate["entity_id"], text=candidate["data"]["body"],
                        decision_ref=key, actor=info["actor"])
                self.workspace.adopt_content_candidate(con,row["content"],candidate,author=info["actor"],request_id=request_id,
                    expected_version_ref=expected_version_ref,checks=data["checks"])
            return self.content(company,workspace,content_ref)
        raise ValueError("未支持的内容动作。")

    def bind_discussion(self, company, workspace, content_ref, *, request_id, expected_version_ref, assignment_ref):
        row=self.content(company,workspace,content_ref)
        info=self.entry.authoring_scope(company,workspace,write=True)
        if row["version"]["entity_id"] != expected_version_ref: raise ContentGrowthConflict("请先保存当前正文。")
        if self.collection(company,workspace)["pending_requests"]: raise ContentGrowthConflict("先核验原请求，不能更换内容或员工重新发送。")
        assignment=next((a for a in info["assignments"] if a["assignment_ref"] == assignment_ref),None)
        if not assignment: raise RuntimeScopeError("缺少当前内容责任员工。")
        binding_ref="cg-binding:"+digest([info["scope"],content_ref,request_id])
        conversation=self.conversations.create(company,request_id=binding_ref,title=row["version"]["data"]["title"][:120],employee_ref=assignment["employee_ref"], discussion_scope={"workspace_id": workspace, "object_ref": content_ref, "assignment_ref": assignment_ref})
        value={"binding_ref":binding_ref,"scope":info["scope"],"content_ref":content_ref,"basis_version_ref":expected_version_ref,
            "context":self.conversations.context(company,assignment["employee_ref"],assignment_ref),
            "conversation_id":conversation["conversation_id"], "discussion_scope": conversation.get("discussion_scope")}
        self.conversations.events.record(correlation_id=content_ref,event_type="cg.discussion.bound",payload=value,idempotency_key=binding_ref)
        return value

    def query_request(self, company, workspace, content_ref, binding_ref, *, request_id=None, attempt_id=None):
        self.content(company,workspace,content_ref)
        with self.db.connect() as con:
            row=con.execute("select payload from evolution_events where tenant_id=? and event_type='cg.discussion.bound' and idempotency_key=?",
                (TenantContext.current_tenant_id(),binding_ref)).fetchone()
        if not row: raise KeyError("原讨论不存在。")
        binding=json.loads(row[0])
        if binding["content_ref"] != content_ref or binding["scope"]["company_id"] != company or binding["scope"]["workspace_id"] != workspace:
            raise RuntimeScopeError("原讨论不在当前内容。")
        result=self.conversations.read_attempt(company,binding["conversation_id"],attempt_id) if attempt_id else self.conversations.read_request(company,binding["conversation_id"],request_id)
        return {"binding":binding,**result}

    def agent_work_source(self, company, workspace, assignment_ref, source):
        if set(source) != {"kind", "content_ref", "expected_version_ref", "selection", "references"}:
            raise ValueError("内容工作需要原对象、版本、选段和明确引用。")
        row = self.content(company, workspace, source["content_ref"])
        info = self.entry.authoring_scope(company, workspace, write=True)
        self.check_qualification(info, row["version"]["data"])
        if row["version"]["entity_id"] != source["expected_version_ref"]:
            raise ContentGrowthConflict("原内容版本已变化，请重新保存并选择。")
        selected = self.selection(row["version"], source["selection"])
        refs = self.resolve_references(info["scope"], source["references"])
        if info["definition"]["version"] != VERSION:
            if row["version"]["data"]["work"]["assignment_ref"] != assignment_ref:
                raise RuntimeScopeError("本次员工与原保存责任不一致。")
            if refs != row["version"]["data"]["references"]:
                raise ContentGrowthConflict("引用与原保存依据不一致。")
        return {"kind": "content-growth", "scope": info["scope"],
                "content_ref": source["content_ref"], "version_ref": source["expected_version_ref"],
                "selection": selected, "references": refs, "saved_content": row["version"]["data"]}

    def prepare_message(self, company, workspace, content_ref, *, binding_ref, body, request_id, model_key, expected_version_ref, selection, references, work_ref=""):
        row=self.content(company,workspace,content_ref)
        query=self.query_request(company,workspace,content_ref,binding_ref)
        binding=query["binding"]
        inputs={"body":body,"model_key":model_key,"expected_version_ref":expected_version_ref,"selection":selection,"references":references}
        if work_ref:
            inputs["work_ref"] = work_ref
        originals=[m for m in query["messages"] if m.get("idempotency_key") == request_id]
        if originals:
            original=next((a for a in query["attempts"] if a["message_id"] == originals[0]["message_id"]),None)
            if original and original["execution_selection"]["input"] == inputs: return original,False
            raise ContentGrowthConflict("原请求不能更换模型、员工或依据。")
        if self.collection(company,workspace)["pending_requests"]: raise ContentGrowthConflict("请先查看原请求，当前仍在处理或等待确认。")
        if row["version"]["entity_id"] != expected_version_ref: raise ContentGrowthConflict("正文已改变，请先保存并重新选择。")
        info=self.entry.authoring_scope(company,workspace,write=True)
        self.check_qualification(info,row["version"]["data"])
        if not isinstance(body,str) or not body.strip() or len(body)>2000: raise ValueError("讨论输入不能为空或超出边界。")
        selected=self.selection(row["version"],selection)
        refs=self.resolve_references(binding["scope"],references)
        self.entry.prepare_model(company, workspace, binding["context"]["assignment_ref"], model_key)
        policy=self.entry.execution_policy(company,workspace,binding["context"]["assignment_ref"],model_key)
        context=self.conversations.context(company,policy["context"]["employee_ref"],binding["context"]["assignment_ref"])
        if context != binding["context"]: raise RuntimeScopeError("责任已改变，请重新核对。")
        if info["definition"]["version"] != VERSION:
            work=row["version"]["data"]["work"]
            if refs != row["version"]["data"]["references"]: raise ContentGrowthConflict("发送引用与原保存依据不一致。")
            if (work["assignment_ref"],work["recipient_ref"],work["model_key"]) != (binding["context"]["assignment_ref"],policy["context"]["company_employee_ref"],model_key):
                raise ContentGrowthConflict("先保存本次责任员工与模型依据，再发送。")
        execution={"purpose":PURPOSE if info["definition"]["version"]==VERSION else CONTENT_PURPOSE,"scope":binding["scope"],"content_ref":content_ref,"basis_version_ref":expected_version_ref,
            "selection":selected,"references":refs,"context":context,"model":policy["model"],"binding_id":policy["binding"]["id"],
            "grant":policy["grant"],"source_class":policy["grant"].get("source_class","REAL_PROVIDER"),"input":inputs}
        if work_ref:
            execution.update(work_ref=work_ref, work_instruction=body.strip())
        if info["definition"]["version"] != VERSION:
            execution["basis_sha256"]=digest(row["version"]["data"])
            self.reply_context(execution)  # Validate selected-input size before append/claim.
            return self.conversations.prepare(company,context["employee_ref"],body=body,request_id=request_id,
                assignment_ref=context["assignment_ref"],references=self.technical_references(refs),conversation_id=binding["conversation_id"],execution_selection=execution)
        saved=row["version"]["data"]
        context_basis={"version_ref":expected_version_ref,"title":saved["title"],"topic":saved["topic"],"audience":saved["audience"],"selection":selected,"references":refs}
        if info["definition"]["version"] == VERSION:
            context_basis["execution"]=execution  # Preserve the exact legacy context contract.
        else:
            context_basis["format"]=saved["format"]
            context_basis["work"]={k:saved["work"][k] for k in ("goal","recording_requirements","output_intent","output_spec","source_refs")}
            context_basis["shot_set"]=[s["id"] for s in saved["work"]["shots"]]
        # Entire immutable work stays server-side. Prompt contains selected input, never
        # duplicate grant/binding/qualification internals or unselected shot contents.
        compiled=body+"\n保存的内容与脚本依据："+json.dumps(context_basis,sort_keys=True,ensure_ascii=False,separators=(",",":"))
        if len(compiled)>8000: raise ValueError("本次选段与引用超出建议消息范围；原输入保留，请明确缩小选择。")
        return self.conversations.prepare(company,context["employee_ref"],body=compiled,display_body=body,request_id=request_id,
            assignment_ref=context["assignment_ref"],references=self.technical_references(refs),conversation_id=binding["conversation_id"],execution_selection=execution)

    def reply_context(self, selection):
        if selection.get("purpose") != CONTENT_PURPOSE: raise RuntimeScopeError("脚本建议用途不合法。")
        scope=selection["scope"]
        info=self.entry.authoring_scope(scope["company_id"],scope["workspace_id"],write=True)
        if info["scope"] != scope or info["definition"]["version"]!=VERSION_2: raise RuntimeScopeError("脚本建议范围已改变。")
        row=self.content(scope["company_id"],scope["workspace_id"],selection["content_ref"])
        saved=row["version"]["data"]
        if row["version"]["entity_id"]!=selection["basis_version_ref"] or digest(saved)!=selection["basis_sha256"]:
            raise ContentGrowthConflict("原脚本版本或完整依据已改变。")
        self.check_qualification(info,saved)
        selected=self.selection(row["version"],selection["selection"])
        references=self.resolve_references(scope,selection["references"])
        if references!=selection["references"] or references!=saved["references"]: raise ContentGrowthConflict("原引用资格已改变。")
        work=saved["work"]
        result={"version_ref":selection["basis_version_ref"],"basis_sha256":selection["basis_sha256"],"format":saved["format"],"title":saved["title"],"topic":saved["topic"],"audience":saved["audience"],"selection":selected,
            "work":{k:work[k] for k in ("goal","recording_requirements","output_intent","output_spec","source_refs")},"references":references}
        # Full body, all other shots and qualification remain referenced server truth.
        # Never truncate a selected excerpt, shot or evidence to make it executable.
        if len(json.dumps(result,ensure_ascii=False,separators=(",",":")).encode("utf-8"))>16000:
            raise ValueError("本次选段或来源超出建议范围；原脚本完整保留，请显式选择更小范围。")
        return result

    def materialize_agent_candidate(self, proof, reply):
        source = proof["source"]
        company, workspace = source["scope"]["company_id"], source["scope"]["workspace_id"]
        info = self.entry.authoring_scope(company, workspace, write=True)
        with self.db.connect() as con:
            con.execute("begin immediate")
            row = self.content(company, workspace, source["content_ref"], connection=con)
            if row["version"]["entity_id"] != source["version_ref"] or row["version"]["data"] != source["saved_content"]:
                raise ContentGrowthConflict("原内容已变化，候选不能改用新依据。")
            key = "cg:agent-candidate:" + digest([source["scope"], proof["task_ref"]])
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                saved = json.loads(old["payload"])
                if saved.get("reply") != reply:
                    raise ContentGrowthConflict("原结果已生成另一份候选，请先核对原候选。")
                return {"candidate_ref": saved["version_ref"]}
            data = {**row["version"]["data"], "kind": "candidate", "body": reply["excerpt"],
                "basis_version_ref": source["version_ref"], "selection": source["selection"],
                "references": source["references"], "task_ref": proof["task_ref"],
                "attempt_id": proof["task_ref"], "provenance": proof["provenance"], "source_class": "AGENT_EXECUTOR"}
            ref = self.workspace._insert_content_version_in_connection(con, row["content"], data, info["actor"])
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
                "values (?,?,'cg.candidate.created',?,?)", (TenantContext.current_tenant_id(), source["content_ref"],
                    json.dumps({"version_ref": ref, "attempt_id": proof["task_ref"], "reply": reply}), key))
        return {"candidate_ref": ref}

    def receive_dialogue(self, company, workspace, content_ref, expected, conversation, message):
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            proof = self.conversations.dialogue_result(con, company, workspace, content_ref, conversation, message)
            row = self.content(company, workspace, content_ref, connection=con)
            key = "cg:dialogue-candidate:" + digest([info["scope"], content_ref, conversation, message])
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                if json.loads(old[0])["receiving_basis"] != expected:
                    raise ContentGrowthConflict("原回复已经送回另一接收版本。")
                return {"candidate_ref": json.loads(old[0])["version_ref"]}
            if row["version"]["entity_id"] != expected:
                raise ContentGrowthConflict("接收时的内容版本已变化。")
            basis = row["version"]; body = basis["data"].get("body", "")
            from .content_growth_operating_service import ContentGrowthOperatingService
            context = ContentGrowthOperatingService(self.db, service=self).context(con, info, content_ref, expected)
            data = {**basis["data"], "kind": "candidate", "body": proof["text"],
                "basis_version_ref": expected, "selection": {"version_ref": expected, "start": 0,
                    "end": len(body.encode("utf-16-le")) // 2, "excerpt": body, "locator": "body"},
                "source_class": "CONVERSATION_REPLY", "task_ref": proof["task_ref"],
                "provenance": proof["provenance"], "dialogue_source": {"conversation_ref": conversation, "message_ref": message},
                "context_basis_ref": context["ref"] if context else ""}
            ref = self.workspace._insert_content_version_in_connection(con, row["content"], data, info["actor"])
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'cg.candidate.created',?,?)",
                (TenantContext.current_tenant_id(), content_ref, json.dumps({"version_ref": ref, "receiving_basis": expected}), key))
            return {"candidate_ref": ref}

    def materialize_candidate(self, company, workspace, content_ref, *, binding_ref, attempt_id, request_id):
        query=self.query_request(company,workspace,content_ref,binding_ref,attempt_id=attempt_id)
        attempt=query["attempt"]
        replies=[m for m in query["messages"] if m["sender"]["kind"] == "EMPLOYEE" and m.get("idempotency_key") == attempt_id]
        if attempt["status"] != "COMPLETED" or len(replies) != 1: raise ContentGrowthConflict("原请求没有已核验的完整建议。")
        reply=replies[0]; provenance=reply.get("provenance",{}); execution=attempt.get("execution_selection",{})
        original = query["binding"]
        if (execution.get("purpose") not in {PURPOSE, CONTENT_PURPOSE} or execution.get("content_ref") != content_ref
                or execution.get("scope") != original["scope"] or execution.get("context") != original["context"]
                or execution.get("basis_version_ref") != original["basis_version_ref"]):
            raise RuntimeScopeError("只有这次内容选段的原请求可生成候选；普通讨论回复不会自动转为候选。")
        if provenance.get("execution_selection") != execution or not provenance.get("usage",{}).get("usage_record_id"):
            raise RuntimeScopeError("建议没有唯一实际用量依据。")
        with self.db.connect() as con:
            usage=con.execute("select * from ai_usage_records where tenant_id=? and task_id=? and company_id=? and workspace_id=? "
                "and execution_ref=? and capability_binding_id=? and capability_id=?",
                (TenantContext.current_tenant_id(),reply["task_ref"],company,workspace,attempt_id,execution["binding_id"],execution["model"]["model_key"])).fetchall()
            task=con.execute("select status,output,employee_id from tasks where tenant_id=? and task_id=? and company_id=? and workspace_id=?",
                (TenantContext.current_tenant_id(),reply["task_ref"],company,workspace)).fetchone()
        if (len(usage) != 1 or usage[0]["usage_record_id"] != provenance["usage"]["usage_record_id"]
                or usage[0]["execution_status"] != "success" or usage[0]["fallback_from_model"]
                or not task or task["status"] != "COMPLETED" or task["output"] != reply["body"]
                or task["employee_id"] != usage[0]["employee_id"]):
            raise RuntimeScopeError("原建议、任务与实际用量不一致。")
        info=self.entry.authoring_scope(company,workspace,write=True)
        with self.db.connect() as con:
            con.execute("begin immediate")
            row=self.content(company,workspace,content_ref,connection=con)
            basis=next((v for v in row["versions"] if v["entity_id"] == execution["basis_version_ref"]),None)
            if not basis: raise RuntimeScopeError("建议依据不存在。")
            key="cg:reply-candidate:"+digest([info["scope"],content_ref,attempt_id])
            old=con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",(TenantContext.current_tenant_id(),key)).fetchone()
            if not old:
                data={**basis["data"],"kind":"candidate","body":reply["body"],"basis_version_ref":basis["entity_id"],
                    "selection":execution["selection"],"references":execution["references"],"task_ref":reply["task_ref"],
                    "attempt_id":attempt_id,"provenance":provenance,"source_class":execution["source_class"]}
                ref=self.workspace._insert_content_version_in_connection(con,row["content"],data,info["actor"])
                con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'cg.candidate.created',?,?)",
                    (TenantContext.current_tenant_id(),content_ref,json.dumps({"version_ref":ref,"attempt_id":attempt_id,"request_id":request_id}),key))
        return self.content(company,workspace,content_ref)

    # CG-LEARNING-01: manual experience learning, forced UNVERIFIED.
    # Reuses runtime_entities PACKAGE_DOMAIN_OBJECT pattern (Music accepted).
    CG_LEARNING_KIND = "ContentGrowthLearning"

    def _learning_get(self, con, company, workspace, ref, *, seen=None):
        visited = set(seen or ())
        if ref in visited: raise ValueError("原依据关系形成循环。")
        visited.add(ref)
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (TenantContext.current_tenant_id(), company, workspace, ref)).fetchone()
        if not row: raise RuntimeScopeError("经验对象不在当前工作空间。")
        result = dict(row); data = json.loads(result.pop("data_json")); result["data"] = data
        if data.get("objectType") != self.CG_LEARNING_KIND: raise RuntimeScopeError("不是合法的经验对象。")
        payload = {k: v for k, v in data.items() if k not in {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256", "identity_ref", "previous_ref", "revision", "basis"}}
        if data.get("payload_sha256") != digest(payload): raise ValueError("经验内容已改变。")
        if data["previous_ref"]:
            previous = self._learning_get(con, company, workspace, data["previous_ref"], seen=visited)
            if previous["data"]["identity_ref"] != data["identity_ref"] or previous["data"]["revision"] + 1 != data["revision"]: raise ValueError("原版本关系不一致。")
        elif data["identity_ref"] != ref or data["revision"] != 1: raise ValueError("对象首次版本身份不一致。")
        for source, hashed in data["basis"].items():
            original = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=?",
                (TenantContext.current_tenant_id(), company, workspace, source)).fetchone()
            if not original: raise ValueError("原依据内容不可确认。")
            original_data = json.loads(original["data_json"])
            if digest(original_data) != hashed: raise ValueError("原依据内容已改变，请重新核对经验。")
            if original_data.get("objectType") == self.CG_LEARNING_KIND: self._learning_get(con, company, workspace, source, seen=visited)
        return result

    def _latest_learning(self, con, company, workspace, record):
        identity = record["data"]["identity_ref"]
        rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? and json_extract(data_json,'$.identity_ref')=? order by json_extract(data_json,'$.revision') desc",
            (TenantContext.current_tenant_id(), company, workspace, self.CG_LEARNING_KIND, identity)).fetchall()
        return self._learning_get(con, company, workspace, rows[0][0])

    def _insert_learning(self, con, company, workspace, payload, actor, *, entity_id):
        data = {"packageId": "com.curis.local.content-growth", "packageVersion": "0.2.0", "schemaVersion": "0.2.0",
            "objectType": self.CG_LEARNING_KIND, "kind": "Learning", **payload}
        data["payload_sha256"] = digest({k: v for k, v in data.items() if k not in {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256", "identity_ref", "previous_ref", "revision", "basis"}})
        at = datetime.now(timezone.utc).isoformat()
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
            "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
            (entity_id, TenantContext.current_tenant_id(), company, workspace, workspace, actor, "ACTIVE", "0.2.0", "UNVERIFIED", "MISSING", json.dumps(data, ensure_ascii=False), at, at))
        return entity_id

    def learning_collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? order by created_at,entity_id",
                (TenantContext.current_tenant_id(), company, workspace, self.CG_LEARNING_KIND)).fetchall()
            records = [self._learning_get(con, company, workspace, row[0]) for row in rows]
            return {"records": records, "entry": info}

    def learning_command(self, company, workspace, action, *, request_id, expected_ref="", data):
        from uuid import uuid4
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("请求标识为空或超过允许长度。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            actor = info["actor"]
            key = "cg:learning:" + digest([info["scope"], action, actor, request_id])
            fingerprint = digest({"action": action, "data": data, "expected_ref": expected_ref})
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                replay = json.loads(old[0])
                if replay["fingerprint"] != fingerprint: raise ContentGrowthConflict("原请求不能改写内容或依据。")
                return replay["result"]
            if action == "save-learning":
                exact(data, {"title", "body", "basis_refs", "applicability", "counterexample", "accepted"})
                learning_text(data["title"], 2000, empty=False)
                learning_text(data["body"], 20000, empty=False)
                learning_text(data["applicability"], 2000)
                learning_text(data["counterexample"], 20000)
                if type(data["accepted"]) is not bool: raise ValueError("接受用途必须明确。")
                if not isinstance(data["basis_refs"], list) or len(data["basis_refs"]) > 8: raise ValueError("原依据引用超出边界。")
                # Validate basis refs are in scope and snapshot their content hashes.
                resolved = []
                basis_hashes = {}
                for ref in data["basis_refs"]:
                    learning_text(ref, 256, empty=False)
                    row = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=?",
                        (TenantContext.current_tenant_id(), company, workspace, ref)).fetchone()
                    if not row: raise RuntimeScopeError("原依据不在当前工作空间。")
                    basis_data = json.loads(row["data_json"])
                    if basis_data.get("schemaVersion") == "cg.operating-context/v1":
                        if basis_data.get("kind") not in {"Reference", "Report"} or basis_data.get("kind") == "Report" and basis_data.get("payload", {}).get("confirmed") is not True:
                            raise ValueError("请选择原参考或明确确认的人工报告。")
                    resolved.append(ref)
                    basis_hashes[ref] = digest(basis_data)
                value = {"title": data["title"], "body": data["body"], "basis_refs": resolved, "applicability": data["applicability"],
                    "counterexample": data["counterexample"], "accepted_by": actor if data["accepted"] else "", "validation": "UNVERIFIED"}
                ref = "cg-learning-" + str(uuid4())
                previous = self._learning_get(con, company, workspace, expected_ref) if expected_ref else None
                if previous and self._latest_learning(con, company, workspace, previous)["entity_id"] != expected_ref: raise ContentGrowthConflict("原版本已有后续修改，请保留输入并核对。")
                value.update(identity_ref=previous["data"]["identity_ref"] if previous else ref,
                    previous_ref=expected_ref, revision=previous["data"]["revision"] + 1 if previous else 1,
                    basis=basis_hashes)
                self._insert_learning(con, company, workspace, value, actor, entity_id=ref)
                for source in resolved:
                    con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                        (TenantContext.current_tenant_id(), ref, "CG_LEARNING_BASIS", source))
                result = {"record": self._learning_get(con, company, workspace, ref), "result_ref": ref}
            elif action == "use-learning":
                exact(data, {"learning_ref", "content_ref", "confirmed", "historical"})
                if data["confirmed"] is not True or type(data["historical"]) is not bool: raise ValueError("请明确确认引用经验的用途与原版本。")
                learning = self._learning_get(con, company, workspace, data["learning_ref"])
                if not learning["data"]["accepted_by"]: raise ValueError("经验的用途尚未明确接受。")
                current = self._latest_learning(con, company, workspace, learning)["entity_id"] == data["learning_ref"]
                if not current and not data["historical"]: raise ContentGrowthConflict("所选经验属于原版本；保留原引用只读，明确核对历史用途后才可采用。")
                # Apply: create new content version with learning basis, without replacing latest.
                content_row = self.content(company, workspace, data["content_ref"], connection=con)
                basis = content_row["version"]["data"]
                new_data = {**basis, "kind": "draft",
                    "learning_ref": learning["entity_id"],
                    "learning_body": learning["data"]["body"],
                    "learning_applicability": learning["data"]["applicability"],
                    "learning_counterexample": learning["data"]["counterexample"]}
                ref = self.workspace._insert_content_version_in_connection(con, content_row["content"], new_data, actor)
                con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp) "
                    "on conflict(tenant_id,source_id,relation,target_id) do nothing",
                    (TenantContext.current_tenant_id(), content_row["content"]["entity_id"], "CG_APPLIES_LEARNING", learning["entity_id"]))
                result = {"record": self._learning_get(con, company, workspace, learning["entity_id"]), "result_ref": ref}
            else:
                raise ValueError("未授权的学习动作。")
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (TenantContext.current_tenant_id(), workspace, "cg.learning." + action,
                 json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), key))
            return result

    # Platform chain S1: ChannelAccount local CRUD with honest NOT_CONNECTED projection.
    # Business-level visibility (D2): rows are scoped by company_id + data_json.business_ref,
    # so the same account is visible from every CG workspace of the same business.
    CG_ACCOUNT_KIND = "ChannelAccount"

    def _account_payload(self, data, *, create):
        # connection_status is server-owned; client values are silently ignored.
        data = {key: value for key, value in data.items() if key != "connection_status"}
        exact(data, ACCOUNT_CREATE_FIELDS if create else ACCOUNT_EDIT_FIELDS)
        if create and (not isinstance(data["platform_ref"], str)
                or data["platform_ref"] not in {item["platform"] for item in PLATFORM_CATALOG}):
            raise ValueError("平台不在当前平台目录中。")
        learning_text(data["name"], 256, empty=False)
        for key in ACCOUNT_TEXT_FIELDS: learning_text(data[key], 2000)
        if data["growth_stage"] not in ACCOUNT_GROWTH_STAGES: raise ValueError("经营阶段不在枚举内。")
        if data["status"] not in ACCOUNT_STATUS: raise ValueError("账号状态不在枚举内。")
        return {**data, "connection_status": ACCOUNT_CONNECTION_STATUS}

    def _account_row(self, con, company, business_ref, ref):
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (TenantContext.current_tenant_id(), company, ref)).fetchone()
        data = json.loads(row["data_json"]) if row else {}
        if not row or data.get("objectType") != self.CG_ACCOUNT_KIND or data.get("business_ref") != business_ref:
            raise RuntimeScopeError("账号不在当前业务范围。")
        result = dict(row); result["data"] = data; return result

    def _account_business_ref(self, info):
        business = info["scope"].get("business_id")
        if not business: raise RuntimeScopeError("当前工作空间没有明确的业务归属。")
        return business

    def account_collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        business = self._account_business_ref(info)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
                "and json_extract(data_json,'$.business_ref')=? order by created_at,entity_id",
                (TenantContext.current_tenant_id(), company, self.CG_ACCOUNT_KIND, business)).fetchall()
            return {"catalog": [dict(item) for item in PLATFORM_CATALOG],
                    "accounts": [self._account_row(con, company, business, row[0]) for row in rows], "entry": info}

    def account(self, company, workspace, account_ref):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            return self._account_row(con, company, self._account_business_ref(info), account_ref)

    def account_create(self, company, workspace, *, data):
        from uuid import uuid4
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            payload = self._account_payload(data, create=True)
            payload = {"objectType": self.CG_ACCOUNT_KIND, **payload, "business_ref": self._account_business_ref(info)}
            ref = "cg-account-" + str(uuid4())
            at = datetime.now(timezone.utc).isoformat()
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
                (ref, TenantContext.current_tenant_id(), company, workspace, workspace, info["actor"], "ACTIVE",
                 info["blueprint_version"], "UNVERIFIED", "MISSING", json.dumps(payload, ensure_ascii=False), at, at))
            return self._account_row(con, company, payload["business_ref"], ref)

    def account_edit(self, company, workspace, account_ref, *, data):
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            business = self._account_business_ref(info)
            row = self._account_row(con, company, business, account_ref)
            merged = {**row["data"], **self._account_payload(data, create=False),
                      "connection_status": ACCOUNT_CONNECTION_STATUS, "business_ref": business}
            con.execute("update runtime_entities set data_json=?,updated_at=? where entity_id=?",
                (json.dumps(merged, ensure_ascii=False), datetime.now(timezone.utc).isoformat(), account_ref))
            return self._account_row(con, company, business, account_ref)

    # Platform chain S2: per-account no-send publish verification records (point-in-time
    # immutable) plus the D4 new minimal local export. Nothing here sends, queues, schedules,
    # or mutates the content state machine / INTERNAL_CANDIDATE_NO_PUBLICATION gate.
    CG_VERIFY_KIND = "PublishVerification"

    def _platform_name(self, platform_ref):
        return next((item["name"] for item in PLATFORM_CATALOG if item["platform"] == platform_ref), "")

    def _verify_template(self, platform_ref):
        if not isinstance(platform_ref, str) or platform_ref not in {item["platform"] for item in PLATFORM_CATALOG}:
            raise ValueError("平台不在当前平台目录中。")
        items = VERIFY_PLATFORM_CHECKS.get(platform_ref, VERIFY_COMMON_CHECKS)
        return [{"key": key, "label": label} for key, label in items]

    def _verify_check_results(self, template, submitted):
        # Clients submit key + checked (+ optional note); labels are always server-owned.
        if not isinstance(submitted, list) or len(submitted) != len(template):
            raise ValueError("请逐项核对检查清单。")
        allowed = {spec["key"] for spec in template}
        by_key = {}
        for item in submitted:
            if not isinstance(item, dict): raise ValueError("检查结果格式不合法。")
            keys = set(item)
            # Client-supplied labels are tolerated but discarded: labels are server-owned.
            if not {"key", "checked"} <= keys <= {"key", "checked", "note", "label"}:
                raise ValueError("检查结果字段不合法。")
            if not isinstance(item["key"], str) or not isinstance(item["checked"], bool):
                raise ValueError("检查结果字段不合法。")
            if item["key"] in by_key: raise ValueError("检查项重复。")
            note = item.get("note", "")
            learning_text(note, 2000)
            by_key[item["key"]] = (item["checked"], note)
        if set(by_key) != allowed: raise ValueError("检查项与当前平台模板不一致。")
        return [{"key": spec["key"], "label": spec["label"], "checked": by_key[spec["key"]][0],
                 "note": by_key[spec["key"]][1]} for spec in template]

    def _verify_row(self, con, company, business_ref, ref):
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (TenantContext.current_tenant_id(), company, ref)).fetchone()
        data = json.loads(row["data_json"]) if row else {}
        if not row or data.get("objectType") != self.CG_VERIFY_KIND or data.get("business_ref") != business_ref:
            raise RuntimeScopeError("核验记录不在当前业务范围。")
        result = dict(row); result["data"] = data; return result

    def verification_template(self, company, workspace, platform_ref):
        info = self.entry.authoring_scope(company, workspace)
        template = self._verify_template(platform_ref)
        return {"platform": platform_ref, "name": self._platform_name(platform_ref), "checks": template, "entry": info}

    def verification_collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        business = self._account_business_ref(info)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
                "and json_extract(data_json,'$.business_ref')=? order by created_at,entity_id",
                (TenantContext.current_tenant_id(), company, self.CG_VERIFY_KIND, business)).fetchall()
            return {"verifications": [self._verify_row(con, company, business, row[0]) for row in rows], "entry": info}

    def verification(self, company, workspace, verification_ref):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            return self._verify_row(con, company, self._account_business_ref(info), verification_ref)

    def verification_create(self, company, workspace, *, request_id, data):
        from uuid import uuid4
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("请求标识为空或超过允许长度。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            exact(data, VERIFY_CREATE_FIELDS)
            learning_text(data["content_ref"], 256, empty=False)
            learning_text(data["account_ref"], 256, empty=False)
            business = self._account_business_ref(info)
            account = self._account_row(con, company, business, data["account_ref"])
            # Content is a workspace-level object: it must live in the CURRENT workspace.
            content_row = self.content(company, workspace, data["content_ref"], connection=con)
            head = content_row["version"]["data"]
            platform_ref = account["data"]["platform_ref"]
            checks = self._verify_check_results(self._verify_template(platform_ref), data["checks"])
            actor = info["actor"]
            key = "cg:verification:" + digest([info["scope"], actor, request_id])
            fingerprint = digest({"data": data})
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                replay = json.loads(old[0])
                if replay["fingerprint"] != fingerprint: raise ContentGrowthConflict("原请求不能改写核验内容。")
                return replay["result"]
            ref = "cg-verify-" + str(uuid4())
            at = datetime.now(timezone.utc).isoformat()
            payload = {
                "objectType": self.CG_VERIFY_KIND, "business_ref": business,
                "account_ref": account["entity_id"], "account_name": account["data"]["name"],
                "platform_ref": platform_ref, "platform_name": self._platform_name(platform_ref),
                "content_ref": content_row["content"]["entity_id"],
                "content_workspace_id": content_row["content"]["workspace_id"],
                "content_title": head.get("title", "") or "",
                "content_body": head.get("body", "") or "",
                "content_format": content_row["content"]["data"].get("format", "") or "",
                "checks": checks,
                "verification": "UNVERIFIED", "source": "CEO_MANUAL",
                "connection_status": ACCOUNT_CONNECTION_STATUS,
                "revision": 1, "identity_ref": ref, "previous_ref": "",
            }
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
                (ref, TenantContext.current_tenant_id(), company, workspace, workspace, actor, "ACTIVE",
                 info["blueprint_version"], "UNVERIFIED", "MISSING", json.dumps(payload, ensure_ascii=False), at, at))
            for relation, target in (("CG_VERIFY_ACCOUNT", account["entity_id"]),
                                     ("CG_VERIFY_CONTENT", content_row["content"]["entity_id"])):
                con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                    (TenantContext.current_tenant_id(), ref, relation, target))
            result = {"record": self._verify_row(con, company, business, ref), "result_ref": ref}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (TenantContext.current_tenant_id(), workspace, "cg.verification.save",
                 json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), key))
            return result

    def verification_export(self, company, workspace, verification_ref):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            record = self._verify_row(con, company, self._account_business_ref(info), verification_ref)
        data = record["data"]
        package = {
            "package_type": "curis.cg.local-verification-export/1",
            "verification_ref": verification_ref,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "title": data["content_title"], "body": data["content_body"], "format": data["content_format"],
            "platform": {"ref": data["platform_ref"], "name": data["platform_name"]},
            "account": {"ref": data["account_ref"], "name": data["account_name"]},
            "checks": data["checks"],
            "connection_status": ACCOUNT_CONNECTION_STATUS,
            "verification": "UNVERIFIED", "source": "CEO_MANUAL",
            "notice": VERIFY_NOTICE,
        }
        raw = json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        filename = "cg-local-verification-" + verification_ref.replace("cg-verify-", "")[:8] + ".json"
        return raw, hashlib.sha256(raw).hexdigest(), filename

    # Platform chain S3: CEO manual publish receipts (§4.3) and manual account
    # performance observations (§4.4). Both are immutable point-in-time records with
    # the three forced truths (UNVERIFIED / CEO_MANUAL / NOT_CONNECTED); nothing here
    # fetches a URL, connects, analyzes, or mutates verifications/contents.
    CG_RECEIPT_KIND = "PublishReceipt"
    CG_OBS_KIND = "AccountObservation"

    def _domain_row(self, con, company, business_ref, ref, kind, error):
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (TenantContext.current_tenant_id(), company, ref)).fetchone()
        data = json.loads(row["data_json"]) if row else {}
        if not row or data.get("objectType") != kind or data.get("business_ref") != business_ref:
            raise RuntimeScopeError(error)
        result = dict(row); result["data"] = data; return result

    def _receipt_row(self, con, company, business_ref, ref):
        return self._domain_row(con, company, business_ref, ref, self.CG_RECEIPT_KIND, "发布回执不在当前业务范围。")

    def _observation_row(self, con, company, business_ref, ref):
        return self._domain_row(con, company, business_ref, ref, self.CG_OBS_KIND, "表现观察不在当前业务范围。")

    def _receipt_payload(self, data):
        exact(data, RECEIPT_CREATE_FIELDS)
        published_at = data["published_at"].strip()
        platform_post_url = data["platform_post_url"].strip()
        note = data["note"].strip()
        if not (published_at or platform_post_url or note):
            raise ValueError("请至少回填一项（发布时间、平台链接或备注）。")
        learning_text(published_at, 200)
        learning_text(note, 2000)
        if platform_post_url:
            learning_text(platform_post_url, 2000)
            lowered = platform_post_url.lower()
            if not (lowered.startswith("http://") or lowered.startswith("https://")):
                raise ValueError("平台链接需以 http:// 或 https:// 开头；链接仅作人工回填，系统不会访问。")
        return {"published_at": published_at, "platform_post_url": platform_post_url,
                "note": note, "notice": RECEIPT_NOTICE}

    def receipt_collection(self, company, workspace, verification_ref):
        info = self.entry.authoring_scope(company, workspace)
        business = self._account_business_ref(info)
        with self.db.connect() as con:
            verification = self._verify_row(con, company, business, verification_ref)
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
                "and json_extract(data_json,'$.business_ref')=? and json_extract(data_json,'$.verification_ref')=? "
                "order by created_at,entity_id",
                (TenantContext.current_tenant_id(), company, self.CG_RECEIPT_KIND, business, verification_ref)).fetchall()
            return {"verification": verification,
                    "receipts": [self._receipt_row(con, company, business, row[0]) for row in rows], "entry": info}

    def receipt(self, company, workspace, receipt_ref):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            return self._receipt_row(con, company, self._account_business_ref(info), receipt_ref)

    def receipt_create(self, company, workspace, verification_ref, *, request_id, data):
        from uuid import uuid4
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("请求标识为空或超过允许长度。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            business = self._account_business_ref(info)
            verification = self._verify_row(con, company, business, verification_ref)
            fields = self._receipt_payload(data)
            actor = info["actor"]
            key = "cg:receipt:" + digest([info["scope"], actor, request_id, verification_ref])
            fingerprint = digest({"data": data, "verification_ref": verification_ref})
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                replay = json.loads(old[0])
                if replay["fingerprint"] != fingerprint: raise ContentGrowthConflict("原请求不能改写回执内容。")
                return replay["result"]
            vdata = verification["data"]
            ref = "cg-receipt-" + str(uuid4())
            at = datetime.now(timezone.utc).isoformat()
            payload = {
                "objectType": self.CG_RECEIPT_KIND, "business_ref": business,
                "verification_ref": verification_ref,
                "content_ref": vdata.get("content_ref", ""), "content_title": vdata.get("content_title", ""),
                "account_ref": vdata.get("account_ref", ""), "account_name": vdata.get("account_name", ""),
                "platform_ref": vdata.get("platform_ref", ""), "platform_name": vdata.get("platform_name", ""),
                **fields,
                "verification": "UNVERIFIED", "source": "CEO_MANUAL",
                "connection_status": ACCOUNT_CONNECTION_STATUS,
                "revision": 1, "identity_ref": ref, "previous_ref": "",
            }
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
                (ref, TenantContext.current_tenant_id(), company, workspace, workspace, actor, "ACTIVE",
                 info["blueprint_version"], "UNVERIFIED", "MISSING", json.dumps(payload, ensure_ascii=False), at, at))
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                (TenantContext.current_tenant_id(), ref, "CG_RECEIPT_VERIFICATION", verification_ref))
            result = {"record": self._receipt_row(con, company, business, ref), "result_ref": ref}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (TenantContext.current_tenant_id(), workspace, "cg.receipt.save",
                 json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), key))
            return result

    def _observation_payload(self, data):
        exact(data, OBSERVATION_CREATE_FIELDS)
        learning_text(data["title"], 2000, empty=False)
        learning_text(data["body"], 20000, empty=False)
        period = data["period"].strip()
        learning_text(period, 200, empty=False)
        learning_text(data["scope_ref"], 256, empty=False)
        return {"title": data["title"].strip(), "body": data["body"].strip(),
                "scope_ref": data["scope_ref"].strip(), "period": period}

    def observation_collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        business = self._account_business_ref(info)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
                "and json_extract(data_json,'$.business_ref')=? order by created_at,entity_id",
                (TenantContext.current_tenant_id(), company, self.CG_OBS_KIND, business)).fetchall()
            return {"observations": [self._observation_row(con, company, business, row[0]) for row in rows], "entry": info}

    def observation(self, company, workspace, observation_ref):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            return self._observation_row(con, company, self._account_business_ref(info), observation_ref)

    def observation_create(self, company, workspace, *, request_id, data):
        from uuid import uuid4
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("请求标识为空或超过允许长度。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            business = self._account_business_ref(info)
            fields = self._observation_payload(data)
            # scope_ref MUST resolve to a ChannelAccount in the current business (contract §4.4).
            account = self._account_row(con, company, business, fields["scope_ref"])
            actor = info["actor"]
            key = "cg:observation:" + digest([info["scope"], actor, request_id])
            fingerprint = digest({"data": data})
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), key)).fetchone()
            if old:
                replay = json.loads(old[0])
                if replay["fingerprint"] != fingerprint: raise ContentGrowthConflict("原请求不能改写观察内容。")
                return replay["result"]
            adata = account["data"]
            ref = "cg-obs-" + str(uuid4())
            at = datetime.now(timezone.utc).isoformat()
            payload = {
                "objectType": self.CG_OBS_KIND, "business_ref": business,
                "title": fields["title"], "body": fields["body"], "period": fields["period"],
                "scope_ref": account["entity_id"], "account_name": adata.get("name", ""),
                "platform_ref": adata.get("platform_ref", ""), "platform_name": self._platform_name(adata.get("platform_ref", "")),
                "notice": OBSERVATION_NOTICE,
                "verification": "UNVERIFIED", "source": "CEO_MANUAL",
                "connection_status": ACCOUNT_CONNECTION_STATUS,
                "revision": 1, "identity_ref": ref, "previous_ref": "",
            }
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
                (ref, TenantContext.current_tenant_id(), company, workspace, workspace, actor, "ACTIVE",
                 info["blueprint_version"], "UNVERIFIED", "MISSING", json.dumps(payload, ensure_ascii=False), at, at))
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                (TenantContext.current_tenant_id(), ref, "CG_OBS_ACCOUNT", account["entity_id"]))
            result = {"record": self._observation_row(con, company, business, ref), "result_ref": ref}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (TenantContext.current_tenant_id(), workspace, "cg.observation.save",
                 json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), key))
            return result
