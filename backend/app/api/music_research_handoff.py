"""Read a Music research delivery in its original conversation and confirm planning."""
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field

from ..conversation_service import ConversationService, digest
from ..resource_scope_policy import ResourceScopePolicy
from ..result_attention import ResultAttention
from ..runtime import RuntimeScopeError
from ..runtime.child_work import CanonicalChildWorkRuntime
from ..runtime.music import MusicConflict
from ..tenant_context import TenantContext


class ConfirmResearchPlanningIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conversation_ref: str = Field(min_length=1, max_length=256)
    research_work_ref: str = Field(min_length=1, max_length=256)
    child_work_ref: str = Field(min_length=1, max_length=256)
    evidence_ref: str = Field(min_length=1, max_length=256)
    evidence_version: str = Field(pattern=r"^[0-9a-f]{64}$")
    summary_result_ref: str = Field(min_length=1, max_length=256)
    summary_result_version: str = Field(pattern=r"^[0-9a-f]{64}$")
    direction_ref: str = Field(min_length=1, max_length=256)
    assignment_ref: str = Field(min_length=1, max_length=256)


def _public_source(payload):
    source_url = payload.get("sourceUrl")
    captured_at = payload.get("capturedAt")
    snapshot_sha256 = payload.get("snapshotSha256")
    if not all(isinstance(value, str) and value for value in (source_url, captured_at, snapshot_sha256)):
        raise RuntimeScopeError("研究证据缺少公开来源、采集时间或快照摘要。")
    url = urlsplit(source_url)
    if (url.scheme != "https" or not url.hostname or url.username is not None
            or datetime.fromisoformat(captured_at).utcoffset() != timedelta(0)
            or not re.fullmatch(r"[0-9a-f]{64}", snapshot_sha256)):
        raise RuntimeScopeError("研究证据的公开来源格式不一致。")
    return {"url": source_url, "captured_at": captured_at, "snapshot_sha256": snapshot_sha256}


def _delivery(service, con, company, workspace, conversation_ref, research_work_ref, child_work_ref, evidence_ref):
    conversations = ConversationService(ConversationService(service.db)._work_database(con))
    owner = conversations.owner(company, conversation_id=conversation_ref)
    entry = service._operating_entry(company, workspace, connection=con)
    business = entry["scope"]["business_id"]
    rows = conversations._rows(con, conversation_ref)
    receipts = [row["payload"] for row in rows if row["event_type"] == "conversation.research_work.confirmed"
                and row["payload"].get("work_ref") == research_work_ref]
    if len(receipts) != 1:
        raise RuntimeScopeError("此研究工作不属于原对话。")
    receipt = receipts[0]
    foundation = conversations.foundation
    root = foundation.get(research_work_ref)
    child = foundation.get(child_work_ref)
    source_scope = ResourceScopePolicy.resolve_execution_scope(con, tenant_id=entry["scope"]["tenant_id"],
        company_id=company, scope_type="BUSINESS", scope_ref=business)
    for work in (root, child):
        if work["entity_type"] != "WORK":
            raise RuntimeScopeError("需要正式研究工作。")
        ResourceScopePolicy.require_same_execution_scope(source_scope, ResourceScopePolicy.execution_scope_from_record(
            con, tenant_id=source_scope["tenant_id"], record=work))
    cycle = foundation.get(receipt["cycle_ref"])
    origin = cycle["data"].get("contract", {}).get("conversationResearchSource")
    if (receipt["conversation_ref"] != conversation_ref or receipt["business_ref"] != business
            or receipt["employee_ref"] != owner["owner_ref"] or root["parent_id"] != cycle["entity_id"]
            or origin != {key: value for key, value in receipt.items() if key not in {"work_ref", "cycle_ref"}}
            or root["data"].get("responsibilityAssignmentRef") != receipt["assignment_ref"]
            or root["lifecycle_status"] in {"CANCELLED", "ARCHIVED", "FAILED"}
            or child_work_ref not in (root["data"].get("leaderDelegation") or {}).get("childWorkRefs", [])
            or child["data"].get("leaderRootWorkRef") != research_work_ref or child["parent_id"] != root["parent_id"]
            or child["owner_ref"] == root["owner_ref"]):
        raise RuntimeScopeError("原对话与研究交接关系不一致。")

    evidence = ResultAttention(conversations.db).detail(company, None, evidence_ref, scope=source_scope)
    entity = foundation.get(evidence_ref)
    payload = dict(entity["data"])
    version = payload.pop("payloadSha256", None)
    if (not version or digest(payload) != version):
        raise RuntimeScopeError("研究证据缺少正式来源版本，或内容已变化。")
    if (evidence["kind"] != "EVIDENCE" or entity["parent_id"] != child_work_ref
            or evidence["verification_status"] != "VERIFIED" or evidence["evidence_condition"] != "CURRENT"
            or evidence["status"] != "CURRENT" or entity["data"].get("fixture")
            or entity["data"].get("kind") != "MUSIC_MARKET_EVIDENCE"
            or entity["data"].get("contentVerification") != "VERIFIED"
            or entity["data"].get("sourceWorkRef") != child_work_ref
            or entity["data"].get("rootWorkRef") != research_work_ref
            or entity["data"].get("businessRef") != business
            or not entity["data"].get("sourceTaskRef")
            or "task:" + entity["data"]["sourceTaskRef"] not in child["data"].get("resultRefs", [])
            or child["lifecycle_status"] != "COMPLETED" or evidence_ref not in child["data"].get("evidenceRefs", [])):
        raise RuntimeScopeError("研究子工作尚无已验收的当前证据。")
    source = _public_source(payload)

    CanonicalChildWorkRuntime(conversations.db)._validate_outcome(con, child,
        result_refs=child["data"].get("resultRefs", []), artifact_refs=child["data"].get("artifactRefs", []),
        evidence_refs=child["data"].get("evidenceRefs", []), acceptance_refs=child["data"].get("acceptanceRefs", []))
    summary_ref = (root["data"].get("leaderDelegation") or {}).get("summaryWorkRef")
    if not summary_ref:
        raise RuntimeScopeError("负责人尚未交回原研究汇总。")
    summary = foundation.get(summary_ref)
    ResourceScopePolicy.require_same_execution_scope(source_scope, ResourceScopePolicy.execution_scope_from_record(
        con, tenant_id=source_scope["tenant_id"], record=summary))
    if (summary["entity_type"] != "WORK" or summary["parent_id"] != root["parent_id"]
            or summary["owner_ref"] != root["owner_ref"]
            or summary["data"].get("leaderRootWorkRef") != research_work_ref):
        raise RuntimeScopeError("负责人汇总不属于原研究工作。")
    statements = [record for record in summary["data"].get("responsibilityRouting", {}).get("executions", {}).values()
                  if str(record.get("executionKey") or "").startswith("leader:summary:")
                  and record.get("status") == "ACCEPTED"
                  and record.get("provenance", {}).get("verification_status") == "VERIFIED"]
    if len(statements) != 1:
        raise RuntimeScopeError("负责人汇总尚未核验。")
    statement = statements[0]
    if {"evidence_ref": evidence_ref, "evidence_version": version} not in statement.get("evidenceInputs", []):
        raise RuntimeScopeError("负责人汇总未引用此证据版本。")
    result_ref = statement.get("resultRef")
    if not result_ref or result_ref not in root["data"].get("responsibilityRouting", {}).get("resultRefs", []):
        raise RuntimeScopeError("负责人汇总尚未回到原研究工作。")
    result = ResultAttention(conversations.db).detail(company, None, result_ref, scope=source_scope)
    if (result.get("source_work_ref") != summary_ref or result.get("status") != "COMPLETED"
            or result.get("kind") != "RESULT" or result.get("verification_status") != "VERIFIED"
            or not result.get("result_version")
            or result_ref != f"task:{statement.get('taskRef')}"):
        raise RuntimeScopeError("负责人汇总结果来源不一致。")
    content = json.loads(result["content"] or "{}")
    opportunity = content.get("summary") if isinstance(content, dict) else None
    if (not isinstance(opportunity, str) or not opportunity.strip()
            or opportunity[:2000].strip() != statement["resultSummary"]):
        raise RuntimeScopeError("负责人建议与原结果正文不一致。")

    data = {**receipt, "child_work_ref": child_work_ref, "evidence_ref": evidence_ref,
            "summary_work_ref": summary_ref, "summary_result_ref": result_ref,
            "summary_result_version": result["result_version"], "opportunity_summary": statement["resultSummary"],
            "evidence_version": version, "research_employee_ref": child["owner_ref"],
            "research_assignment_ref": child["data"]["responsibilityAssignmentRef"],
            "evidence_summary": evidence["summary"], "source": source}
    return conversations.db, entry, data


def read_research_delivery(service, company, workspace, *, conversation_ref, research_work_ref):
    with service.db.connect() as con:
        con.execute("begin")
        conversations = ConversationService(ConversationService(service.db)._work_database(con))
        conversations.owner(company, conversation_id=conversation_ref)
        entry = service._operating_entry(company, workspace, connection=con)
        receipts = [row["payload"] for row in conversations._rows(con, conversation_ref)
                    if row["event_type"] == "conversation.research_work.confirmed"
                    and row["payload"].get("work_ref") == research_work_ref
                    and row["payload"].get("business_ref") == entry["scope"]["business_id"]]
        if len(receipts) != 1:
            raise RuntimeScopeError("此研究工作不属于原对话。")
        root = conversations.foundation.get(research_work_ref)
        source_scope = ResourceScopePolicy.resolve_execution_scope(con, tenant_id=entry["scope"]["tenant_id"],
            company_id=company, scope_type="BUSINESS", scope_ref=entry["scope"]["business_id"])
        ResourceScopePolicy.require_same_execution_scope(source_scope,
            ResourceScopePolicy.execution_scope_from_record(con, tenant_id=source_scope["tenant_id"], record=root))
        if root["entity_type"] != "WORK" or root["parent_id"] != receipts[0]["cycle_ref"]:
            raise RuntimeScopeError("此研究工作不属于原对话。")
        route = root["data"].get("responsibilityRouting") or {}
        deliveries = []
        for child_ref in (root["data"].get("leaderDelegation") or {}).get("childWorkRefs", []):
            child = conversations.foundation.get(child_ref)
            if child["lifecycle_status"] != "COMPLETED":
                continue
            for evidence_ref in child["data"].get("evidenceRefs", []):
                try:
                    _, _, delivery = _delivery(service, con, company, workspace, conversation_ref,
                                               research_work_ref, child_ref, evidence_ref)
                except (RuntimeScopeError, KeyError, ValueError):
                    continue
                deliveries.append(delivery)
        saved = con.execute(
            "select w.entity_id, w.lifecycle_status, "
            "json_extract(c.data_json,'$.contract.musicResearchSource.direction_ref') direction_ref, "
            "json_extract(c.data_json,'$.contract.musicResearchSource.direction_identity_ref') direction_identity_ref "
            "from runtime_entities c join runtime_entities w on w.tenant_id=c.tenant_id and w.parent_id=c.entity_id "
            "where c.tenant_id=? and c.company_id=? and c.workspace_id=? and c.entity_type='CYCLE' "
            "and w.company_id=c.company_id and w.workspace_id=c.workspace_id and w.entity_type='WORK' "
            "and json_extract(w.data_json,'$.releaseKey')='initial' "
            "and json_extract(c.data_json,'$.contract.musicResearchSource.conversation_ref')=? "
            "and json_extract(c.data_json,'$.contract.musicResearchSource.work_ref')=?",
            (entry["scope"]["tenant_id"], company, workspace, conversation_ref, research_work_ref),
        ).fetchall()
        return {"conversation_ref": conversation_ref, "research_work_ref": research_work_ref,
                "research_status": root["lifecycle_status"],
                "can_start_research": root["lifecycle_status"] == "ACTIVE" and route.get("status") == "ACTIVE"
                    and not route.get("executions") and not root["data"].get("leaderDelegation"),
                "deliveries": deliveries, "planning_receipts": [
                    {"work_ref": row["entity_id"], "direction_ref": row["direction_ref"],
                     "direction_identity_ref": row["direction_identity_ref"], "status": row["lifecycle_status"]}
                    for row in saved]}


def confirm_research_planning(service, company, workspace, *, evidence_version, summary_result_ref, summary_result_version, direction_ref, assignment_ref, **refs):
    if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
        raise RuntimeScopeError("只有当前公司所有者可以确认歌曲策划。")
    with service.db.connect() as con:
        con.execute("begin immediate")
        database, entry, delivery = _delivery(service, con, company, workspace, **refs)
        if delivery["evidence_version"] != evidence_version:
            raise MusicConflict("原研究证据版本已变化。")
        if (delivery["summary_result_ref"], delivery["summary_result_version"]) != (summary_result_ref, summary_result_version):
            raise MusicConflict("原负责人汇总版本已变化。")
        direction = service._operating_get(con, company, workspace, direction_ref, kind="Direction")
        data = direction["data"]
        if not data["confirmed_by"] or service._latest_operating(con, company, workspace, direction)["entity_id"] != direction_ref:
            raise MusicConflict("请确认当前歌曲方向版本。")
        assignment = next((row for row in entry["assignments"] if row["assignment_ref"] == assignment_ref), None)
        if not assignment:
            raise RuntimeScopeError("当前歌曲创作责任不可用。")
        origin = {**delivery, "direction_ref": direction_ref, "direction_identity_ref": data["identity_ref"],
                  "direction_version": data["payload_sha256"],
                  "planning_assignment_ref": assignment_ref, "planning_assignment_revision": assignment["assignment_revision"],
                  "confirmed_by": entry["actor"]}
        key = digest([company, workspace, delivery["work_ref"], data["identity_ref"]])
        return CanonicalChildWorkRuntime(database).create_cycle_work(company_id=company, workspace_id=workspace,
            scope_type="WORKSPACE", scope_ref=workspace, assignment_ref=assignment_ref,
            release_key="music-research-planning:" + key, contract={
                "problem": "歌曲策划：" + data["title"], "expectedResult": data["body"],
                "constraints": ["只交付歌曲策划，不生成音频或进行发布。"], "references": [],
                "musicResearchSource": origin,
            })
