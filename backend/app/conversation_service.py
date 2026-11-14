"""Shared conversation ownership on the existing append-only event seam.

This is not a Work projection. Existing CEO Assistant and Meeting holders stay
untouched; they can consume this vocabulary without a historical migration.
"""
from __future__ import annotations

import copy
from contextlib import contextmanager, nullcontext
import hashlib
import json
import uuid
from datetime import datetime, timezone
from time import monotonic

from .evolution_event_log import EvolutionEventLog
from .result_attention import ResultAttention
from .runtime import RuntimeFoundation, RuntimeScopeError
from .tenant_context import TenantContext
from .employee_execution_identity import EmployeeExecutionIdentity
from .result_store import ResultStore
from .knowledge_service import KnowledgeService
from .ai_usage import AIUsageService
from .resource_scope_policy import ResourceScopePolicy


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# Read-only ADR-0046 truth projected into the Shared Composer access slot.
# Conversation execution accepts explicitly bridged model bindings only; an
# External Local Agent never participates, so no request/configure choice is
# offered and no effective permission is claimed.
_COMPUTER_ACCESS_MODEL_NOT_APPLICABLE = {
    "slot": "COMPUTER_ACCESS",
    "state": "MODEL_EXECUTOR_NOT_APPLICABLE",
    "selectable": False,
    "requested_intent": None,
    "configured_state": "NOT_APPLICABLE",
    "effective_state": "NOT_APPLICABLE",
    "verification_state": "NOT_APPLICABLE",
}
_COMPUTER_ACCESS_NO_BRIDGE = {
    "slot": "COMPUTER_ACCESS",
    "state": "NO_EXECUTION_BRIDGE",
    "selectable": False,
    "requested_intent": None,
    "configured_state": "UNKNOWN",
    "effective_state": "UNKNOWN",
    "verification_state": "UNVERIFIED",
}


class ConversationService:
    def _work_database(self, connection):
        from .api.team_operating_router import _WorkCreationConnection
        scoped = copy.copy(self.db)
        joined = _WorkCreationConnection(connection)
        scoped.connect = lambda: nullcontext(joined)
        return scoped

    def __init__(self, database):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.events = EvolutionEventLog(database)
        self.process_id = str(uuid.uuid4())
        self.running = set()
        self.credential_wait_started = {}
        self.selection_validator = None
        self.professional_policy = None

    def owner(self, company_id, employee_ref=None, conversation_id=None):
        ceo = ResultAttention(self.db).actor(company_id)
        if conversation_id:
            with self.db.connect() as con:
                row = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='conversation.opened'", (TenantContext.current_tenant_id(), conversation_id)).fetchone()
                joined = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='conversation.employee_joined' order by event_id desc limit 1",
                    (TenantContext.current_tenant_id(), conversation_id)).fetchone()
            if not row:
                raise RuntimeScopeError("Conversation is unavailable")
            owner = json.loads(row["payload"])
            if owner["company_id"] != company_id or owner["participants"][0] != {"kind": "CEO", "ref": ceo}:
                raise RuntimeScopeError("Conversation is outside this CEO scope")
            if joined:
                owner["owner_ref"] = json.loads(joined["payload"])["employee_ref"]
                owner["participants"] = [owner["participants"][0], {"kind": "EMPLOYEE", "ref": owner["owner_ref"]}]
            if owner["owner_ref"]:
                canonical = self.owner(company_id, owner["owner_ref"])
                if employee_ref and self.owner(company_id, employee_ref)["owner_ref"] != canonical["owner_ref"]:
                    raise RuntimeScopeError("Conversation Employee mismatch")
            elif employee_ref:
                raise RuntimeScopeError("Employee has not joined this conversation")
            return owner
        with self.db.connect() as con:
            row = con.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='AI_EMPLOYEE' and entity_id=?",
                (TenantContext.current_tenant_id(), company_id, employee_ref),
            ).fetchone()
            if row is None:
                matches = con.execute(
                    "select * from runtime_entities where tenant_id=? and company_id=? and entity_type='AI_EMPLOYEE' "
                    "and json_extract(data_json,'$.companyEmployeeRef')=?",
                    (TenantContext.current_tenant_id(), company_id, employee_ref),
                ).fetchall()
                if len(matches) == 1:
                    row = matches[0]
        if row is None:
            raise RuntimeScopeError("Canonical Employee is outside this Company")
        employee_ref = row["entity_id"]
        owner = {
            "owner_type": "EMPLOYEE", "owner_ref": employee_ref,
            "tenant_id": TenantContext.current_tenant_id(), "company_id": company_id,
            "participants": [{"kind": "CEO", "ref": ceo}, {"kind": "EMPLOYEE", "ref": employee_ref}],
        }
        owner["conversation_id"] = "conversation-" + digest(owner)
        return owner

    def create(self, company_id, *, request_id, title="", employee_ref=None, discussion_scope=None):
        ceo = ResultAttention(self.db).actor(company_id)
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("Only the CEO can open a conversation")
        if not request_id or len(request_id) > 128 or len(title) > 120:
            raise ValueError("Invalid conversation identity or title")
        employee = self.owner(company_id, employee_ref)["owner_ref"] if employee_ref else ""
        owner = {"owner_type": "TOPIC", "owner_ref": employee, "title": title.strip(),
                 "tenant_id": TenantContext.current_tenant_id(), "company_id": company_id,
                 "participants": [{"kind": "CEO", "ref": ceo}] + ([{"kind": "EMPLOYEE", "ref": employee}] if employee else [])}
        if discussion_scope is not None:
            context = self.context(company_id, employee, discussion_scope.get("assignment_ref"))
            if context["workspace_id"] != discussion_scope.get("workspace_id"):
                raise RuntimeScopeError("讨论不属于当前工作空间。")
            object_ref = discussion_scope.get("object_ref")
            if object_ref:
                obj = self.foundation.get(object_ref)
                if (obj["company_id"] != company_id or obj["workspace_id"] != context["workspace_id"]
                        or obj["entity_type"] not in {"CONTENT_ITEM", "PACKAGE_DOMAIN_OBJECT"}):
                    raise RuntimeScopeError("讨论对象不属于当前工作范围。")
            owner["discussion_scope"] = {"workspace_id": context["workspace_id"], "object_ref": object_ref or None,
                                         "assignment_ref": context["assignment_ref"]}
            # One canonical discussion for this exact current object/Employee responsibility.
            # Selected adapters retain their own immutable bindings but join this same ledger.
            request_id = "scoped:" + digest([owner["discussion_scope"], employee])
            owner["title"] = "当前工作讨论"
        owner["conversation_id"] = "conversation-" + digest([owner["tenant_id"], company_id, ceo, request_id])
        event = self.events.record(correlation_id=owner["conversation_id"], event_type="conversation.opened",
                                   payload=owner, idempotency_key=owner["conversation_id"])
        if event["payload"] != owner:
            raise ValueError("Conversation request identity conflicts")
        return self.owner(company_id, conversation_id=owner["conversation_id"])

    def join(self, company_id, conversation_id, employee_ref):
        owner = self.owner(company_id, conversation_id=conversation_id)
        employee = self.owner(company_id, employee_ref)["owner_ref"]
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("Only the CEO can select the Employee")
        if owner["owner_ref"] and owner["owner_ref"] != employee:
            raise ValueError("This conversation already has an Employee")
        event = self.events.record(correlation_id=conversation_id, event_type="conversation.employee_joined",
            payload={"company_id": company_id, "ceo_id": owner["participants"][0]["ref"], "employee_ref": employee},
            idempotency_key="conversation-employee:" + conversation_id)
        if event["payload"]["employee_ref"] != employee:
            raise ValueError("A different Employee already joined")
        return self.owner(company_id, conversation_id=conversation_id)

    def recent(self, company_id, *, search="", limit=30):
        ceo = ResultAttention(self.db).actor(company_id)
        # Only bounded owner/activity summaries leave SQLite, never full message histories.
        with self.db.connect() as con:
            rows = con.execute("""select o.correlation_id, o.payload,
                max(m.event_id) activity_id, max(m.created_at) activity_at,
                (select substr(json_extract(first.payload,'$.body'),1,60) from evolution_events first
                    where first.tenant_id=o.tenant_id and first.correlation_id=o.correlation_id
                    and first.event_type='conversation.message' order by first.event_id limit 1) fallback_title,
                coalesce((select json_extract(j.payload,'$.employee_ref') from evolution_events j
                    where j.tenant_id=o.tenant_id and j.correlation_id=o.correlation_id
                    and j.event_type='conversation.employee_joined' order by j.event_id desc limit 1),
                    json_extract(o.payload,'$.owner_ref')) employee_ref
                from evolution_events o join evolution_events m on m.tenant_id=o.tenant_id
                    and m.correlation_id=o.correlation_id and m.event_type='conversation.message'
                where o.tenant_id=? and o.event_type='conversation.opened'
                    and json_extract(o.payload,'$.company_id')=?
                    and json_extract(o.payload,'$.participants[0].ref')=?
                group by o.event_id
                having activity_id > coalesce((select max(json_extract(h.payload,'$.through_event'))
                    from evolution_events h where h.tenant_id=o.tenant_id and h.correlation_id=o.correlation_id
                    and h.event_type='conversation.sidebar_dismissed'),0)
                order by activity_id desc limit ?""", (TenantContext.current_tenant_id(), company_id, ceo, max(1, min(limit, 30)))).fetchall()
            result = []
            for row in rows:
                owner = json.loads(row["payload"])
                employee = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? "
                    "and entity_type='AI_EMPLOYEE' and entity_id=?", (TenantContext.current_tenant_id(), company_id, row["employee_ref"])).fetchone()
                data = json.loads(employee["data_json"]) if employee else {}
                item = {"conversation_id": row["correlation_id"], "employee_ref": row["employee_ref"],
                    "employee_name": data.get("name") or ("员工" if row["employee_ref"] else "待选择员工"),
                    "title": owner.get("title") or row["fallback_title"] or "讨论中的事情",
                    "activity_at": row["activity_at"], "activity_id": row["activity_id"]}
                if not search or search.casefold() in (item["title"] + " " + item["employee_name"]).casefold():
                    result.append(item)
        return result

    def dismiss(self, company_id, conversation_id):
        owner = self.owner(company_id, conversation_id=conversation_id)
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("Only the CEO can dismiss a shortcut")
        with self.db.connect() as con:
            through = con.execute("select coalesce(max(event_id),0) from evolution_events where tenant_id=? "
                "and correlation_id=? and event_type='conversation.message'", (owner["tenant_id"], conversation_id)).fetchone()[0]
        self.events.record(correlation_id=conversation_id, event_type="conversation.sidebar_dismissed",
            payload={"through_event": through, "ceo_id": owner["participants"][0]["ref"]},
            idempotency_key=f"conversation-dismiss:{conversation_id}:{through}")

    def context(self, company_id, employee_ref, assignment_ref):
        """Resolve current context afresh, independently of permanent identity."""
        employee_ref = self.owner(company_id, employee_ref)["owner_ref"]
        with self.db.connect() as con:
            try:
                return ResourceScopePolicy.authorize_assignment(
                    con, tenant_id=TenantContext.current_tenant_id(), company_id=company_id,
                    assignment_ref=assignment_ref, employee_ref=employee_ref,
                )
            except ValueError as error:
                raise RuntimeScopeError(str(error)) from error

    def agent_work_source(self, company, workspace, assignment_ref, source):
        if not isinstance(source, dict) or len(json.dumps(source, ensure_ascii=False).encode()) > 32768:
            raise ValueError("请提供有界的原工作来源。")
        assignment = self.foundation.get(assignment_ref)
        context = self.context(company, assignment["data"]["employeeRef"], assignment_ref)
        if context["workspace_id"] != workspace:
            raise RuntimeScopeError("原工作来源与员工责任不在同一范围。")
        kind = source.get("kind")
        if kind == "references":
            if set(source) != {"kind", "references"} or self.professional_workspace(context):
                raise ValueError("专业工作请从原对象的保存版本与选段发起。")
            snapshot = {"kind": kind, "references": self.references(company, context, source["references"])}
        elif kind == "writing":
            from .writing_chapter_service import WritingChapterService
            snapshot = WritingChapterService(self.db, conversation_service=self).agent_work_source(
                company, workspace, assignment_ref, source)
        elif kind == "content-growth":
            from .content_growth_service import ContentGrowthService
            snapshot = ContentGrowthService(self.db, conversations=self).agent_work_source(
                company, workspace, assignment_ref, source)
        elif kind == "music":
            from .music_service import MusicService
            snapshot = MusicService(self.db, conversations=self).agent_work_source(
                company, workspace, assignment_ref, source)
        else:
            raise ValueError("未知的原工作来源。")
        snapshot["context"] = context
        snapshot["conversation_id"] = self.owner(company, context["employee_ref"])["conversation_id"]
        if len(json.dumps(snapshot, ensure_ascii=False).encode()) > 32768:
            raise ValueError("原依据超过本次范围，请缩小选择；不会静默截断。")
        return snapshot

    def validate_model_work(self, con, selection, *, attempt_id=None):
        work_ref = selection.get("work_ref")
        if not work_ref:
            return
        scope = selection["scope"]
        scoped = ConversationService(self._work_database(con))
        work = scoped.foundation.get(work_ref)
        if (work["entity_type"] != "WORK" or work["lifecycle_status"] != "ACTIVE"
                or work["company_id"] != scope["company_id"] or work["workspace_id"] != scope["workspace_id"]):
            raise RuntimeScopeError("原文字 Work 不可用或已终止。")
        contract = scoped.agent_work_contract(work)
        source = contract.get("modelSource") or {}
        kind = {"CG_GRAPHIC_REPLY": "content-growth", "CG_CONTENT_REPLY": "content-growth", "MUSIC_SONG_REPLY": "music"}.get(selection["purpose"])
        origin = (source.get("content_ref"), source.get("version_ref")) if kind == "content-growth" else (source.get("song_ref"), source.get("expected"))
        selected = (selection.get("content_ref"), selection.get("basis_version_ref")) if kind == "content-growth" else (selection.get("song_ref"), selection.get("expected"))
        route = work["data"].get("responsibilityRouting") or {}
        if (not kind or source.get("kind") != kind or origin != selected
                or source.get("scope") != scope or source.get("context") != selection["context"]
                or source.get("selection") != selection["selection"] or source.get("references") != selection["references"]
                or source.get("publication_continuation") != selection.get("publication_continuation")
                or contract.get("problem") != selection.get("work_instruction")
                or contract.get("modelBinding") != {"bindingRef": selection["binding_id"], "model": selection["model"]}
                or route.get("status") in {"CANCELLED", "COMPLETED"}
                or route.get("currentAssignmentRef") != selection["context"]["assignment_ref"]
                or route.get("responsibilityHolderRef") != selection["context"]["employee_ref"]
                or any(key != attempt_id for key in route.get("executions", {}))):
            raise RuntimeScopeError("原文字 Work 的对象、版本、责任、模型或执行依据已变化。")

    def accept_model_work(self, con, *, provenance, task_ref, candidate_ref, text, decision_ref, actor):
        selection = provenance.get("execution_selection") or {}
        scope, work_ref = selection["scope"], selection.get("work_ref")
        if not work_ref or actor != ResultAttention(self.db).actor(scope["company_id"]):
            raise RuntimeScopeError("只有当前所有者可以接受原文字 Work 结果。")
        task = con.execute("select * from tasks where tenant_id=? and company_id=? and workspace_id=? and work_ref=? and task_id=?",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], work_ref, task_ref)).fetchone()
        usage = con.execute("select * from ai_usage_records where tenant_id=? and company_id=? and workspace_id=? and work_ref=? and task_id=? and execution_status='success'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], work_ref, task_ref)).fetchall()
        if (not task or task["status"] != "COMPLETED" or task["output"] != text or len(usage) != 1
                or usage[0]["usage_record_id"] != provenance.get("usage", {}).get("usage_record_id")
                or usage[0]["fallback_from_model"] or usage[0]["execution_ref"] != task["execution_ref"]
                or usage[0]["employee_id"] != task["employee_id"] or usage[0]["capability_binding_id"] != selection["binding_id"]):
            raise RuntimeScopeError("原文字 Work、Result 与唯一实际用量不一致。")
        self.validate_model_work(con, selection, attempt_id=task["execution_ref"])
        claims = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? and event_type='conversation.execution_bound'",
                             (scope["tenant_id"], task_ref)).fetchall()
        if len(claims) != 1 or json.loads(claims[0][0])["execution_selection"] != selection:
            raise RuntimeScopeError("原文字 Work 没有唯一执行依据。")
        from .runtime.child_work import CanonicalChildWorkRuntime
        scoped = self._work_database(con)
        foundation = RuntimeFoundation(scoped)
        result = "task:" + task_ref
        evidence = foundation.create("EVIDENCE", company_id=scope["company_id"], workspace_id=scope["workspace_id"],
            parent_id=work_ref, owner_ref=actor, verification_status="VERIFIED", evidence_condition="CURRENT",
            data={"resultRef": result, "usageRef": usage[0]["usage_record_id"], "candidateRef": candidate_ref,
                  "decisionRef": decision_ref, "textSha256": hashlib.sha256(text.encode()).hexdigest(), "contentVerification": "OWNER_ACCEPTED_TEXT_ONLY"})
        acceptance = foundation.create("ACCEPTANCE", company_id=scope["company_id"], workspace_id=scope["workspace_id"],
            parent_id=work_ref, owner_ref=actor, data={"resultRefs": [result], "evidenceRefs": [evidence["entity_id"]],
                "requestedBy": actor, "decisionRef": decision_ref, "decision": "ACCEPT_TEXT_WORK_RESULT"})
        for target, role, trigger in (("ACCEPTED", "CEO", "accept"), ("CLOSED", "SYSTEM", "close")):
            foundation.transition(acceptance["entity_id"], target, actor=role, trigger=trigger,
                evidence_refs=[evidence["entity_id"]], context={"ceoId": actor})
        artifacts = con.execute("select artifact_id from artifacts where tenant_id=? and task_id=?", (scope["tenant_id"], task_ref)).fetchall()
        CanonicalChildWorkRuntime(scoped).complete_work(work_ref, result_refs=[result], artifact_refs=[r[0] for r in artifacts],
            evidence_refs=[evidence["entity_id"]], acceptance_refs=[acceptance["entity_id"]])
        return acceptance["entity_id"]

    def agent_work_contract(self, work):
        cycle = self.foundation.get(work["data"].get("cycleRef") or "")
        if (cycle["entity_type"] != "CYCLE" or cycle["company_id"] != work["company_id"]
                or cycle["workspace_id"] != work["workspace_id"]):
            raise RuntimeScopeError("原工作来源范围无法核验。")
        return work["data"].get("followupContract") or cycle["data"].get("contract") or {}

    def validate_agent_work_source(self, work):
        source = self.agent_work_contract(work).get("agentSource") or {}
        original = source.get("snapshot") or {}
        context = original.get("context") or {}
        current = self.agent_work_source(work["company_id"], work["workspace_id"],
            context.get("assignment_ref") or "", source.get("input"))
        if current != original:
            raise RuntimeScopeError("原版本、引用或员工责任已变化，保留原工作，不自动换用新依据。")
        return current

    def agent_result_proof(self, company, work_ref, task_ref, *, require_current_source=True, artifact_ref=None, for_candidate=False):
        ResultAttention(self.db).actor(company)
        work = self.foundation.get(work_ref)
        if work["entity_type"] != "WORK" or work["company_id"] != company:
            raise RuntimeScopeError("结果不属于原公司工作。")
        contract = self.agent_work_contract(work)
        source = self.validate_agent_work_source(work) if require_current_source else contract["agentSource"]["snapshot"]
        if source["kind"] not in {"writing", "content-growth", "music"}:
            raise ValueError("此工作没有可回填的原专业对象。")
        binding = contract["agentBinding"]
        with self.db.connect() as con:
            task = con.execute("select * from tasks where tenant_id=? and company_id=? and workspace_id is ? "
                "and work_ref=? and task_id=?", (TenantContext.current_tenant_id(), company, work["workspace_id"], work_ref, task_ref)).fetchone()
            usage = con.execute("select * from ai_usage_records where tenant_id=? and company_id=? and workspace_id is ? "
                "and work_ref=? and task_id=? and capability_binding_id=? and capability_id=?",
                (TenantContext.current_tenant_id(), company, work["workspace_id"], work_ref, task_ref,
                 binding["bindingRef"], binding["capabilityRef"])).fetchall()
            sessions = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='usage.task_execution'", (TenantContext.current_tenant_id(), task_ref)).fetchall()
        if (not task or task["status"] != "COMPLETED" or task["requested_capability_type"] != "agent"
                or len(usage) != 1 or usage[0]["execution_status"] != "success" or usage[0]["fallback_from_model"]
                or task["employee_id"] != usage[0]["employee_id"] or task["employee_id"] != binding["employeeRef"]
                or len(sessions) != 1):
            raise RuntimeScopeError("原 Agent 任务与唯一成功用量尚未核验。")
        session = json.loads(sessions[0]["payload"]).get("session_id")
        callback = EmployeeExecutionIdentity(self.db).verify_task_callback(company_id=company,
            workspace_id=work["workspace_id"], runtime_employee_ref=source["context"]["employee_ref"],
            task_ref=task_ref, session_ref=session or "")
        output = json.loads(task["output"])
        if not isinstance(output, dict) or output.get("status") != "ACCEPTED" or not isinstance(output.get("summary"), str):
            raise ValueError("原结果没有明确可回填的成果正文。")
        text = output["summary"]
        if not text.strip() or len(text) > 200000:
            raise ValueError("原成果正文为空或超出候选范围。")
        proof = {"source": source, "work_ref": work_ref, "task_ref": task_ref, "text": text,
                 "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                 "task_output_sha256": hashlib.sha256(task["output"].encode()).hexdigest(),
                 "provenance": {**callback, "source_class": "AGENT_EXECUTOR", "content_verification": "UNVERIFIED",
                     "work_ref": work_ref, "usage_record_id": usage[0]["usage_record_id"]}}
        # Whole-result acceptance may inspect its completion summary. A candidate
        # with files must instead bind the user's explicit original file choice.
        if for_candidate or artifact_ref is not None:
            from pathlib import Path
            from .agent_work_resources import AgentWorkResources
            evidence = self.agent_acceptance_evidence(company, work_ref, proof)
            files = [item for item in evidence["artifacts"] if "file_sha256" in item]
            if files and artifact_ref is None:
                raise ValueError("请明确选择原执行的成果文件；执行摘要不能作为文件正文。")
            if artifact_ref is not None:
                if type(artifact_ref) is not str or not 1 <= len(artifact_ref) <= 128:
                    raise ValueError("需要明确且有界的原成果文件引用。")
                matches = [item for item in files if item["artifact_ref"] == artifact_ref]
                if len(matches) != 1:
                    raise RuntimeScopeError("成果文件不属于原工作与本次完成任务。")
                with self.db.connect() as con:
                    row = con.execute("select content,content_sha256 from artifacts "
                        "where tenant_id=? and task_id=? and artifact_id=? and artifact_type='agent_file_receipt'",
                        (TenantContext.current_tenant_id(), task_ref, artifact_ref)).fetchone()
                if (not row or row["content_sha256"] != matches[0]["content_sha256"]
                        or hashlib.sha256(row["content"].encode()).hexdigest() != row["content_sha256"]):
                    raise RuntimeScopeError("原成果文件回执已经改变。")
                receipt = json.loads(row["content"])
                resources = AgentWorkResources(Path(self.db.path).absolute().parent / "agent-work",
                    tenant_id=TenantContext.current_tenant_id(), company_id=company, work_ref=work_ref, task_id=task_ref)
                content = resources.read_output(receipt)
                text = content.decode("utf-8", errors="strict")
                if not text.strip() or "\x00" in text or len(text) > 200000:
                    raise ValueError("所选文件不是有界的非空UTF8正文；没有截断或替换内容。")
                proof.update(text=text, text_sha256=hashlib.sha256(content).hexdigest(),
                    artifact_ref=artifact_ref, artifact_content_sha256=row["content_sha256"],
                    file_sha256=receipt["sha256"], file_bytes=len(content),
                    filename=Path(receipt["relative_path"]).name)
                proof["provenance"].update(artifact_ref=artifact_ref,
                    artifact_content_sha256=row["content_sha256"], file_sha256=receipt["sha256"],
                    task_output_sha256=proof["task_output_sha256"],
                    file_verification="FILE_HASH_VERIFIED", filename=proof["filename"])
        return proof

    def agent_acceptance_evidence(self, company, work_ref, proof):
        from pathlib import Path
        from .agent_work_resources import AgentWorkResources
        ResultAttention(self.db).actor(company)
        with self.db.connect() as con:
            rows = con.execute("select artifact_id,artifact_type,content,content_sha256 from artifacts "
                "where tenant_id=? and task_id=? order by artifact_id",
                (TenantContext.current_tenant_id(), proof["task_ref"])).fetchall()
            events = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='usage.task_execution'", (TenantContext.current_tenant_id(), proof["task_ref"])).fetchall()
        if len(events) != 1:
            raise RuntimeScopeError("原执行用量与附件清单无法核验。")
        expected = json.loads(events[0]["payload"]).get("artifact_receipts") or []
        recorded = [json.loads(row["content"]) for row in rows if row["artifact_type"] == "agent_file_receipt"]
        canonical = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False)
        if sorted(map(canonical, expected)) != sorted(map(canonical, recorded)):
            raise RuntimeScopeError("原执行附件回执缺失、重复或不属于本次执行。")
        artifacts = []
        for row in rows:
            if hashlib.sha256(row["content"].encode()).hexdigest() != row["content_sha256"]:
                raise RuntimeScopeError("原结果附件回执已改变。")
            item = {"artifact_ref": row["artifact_id"], "content_sha256": row["content_sha256"]}
            if row["artifact_type"] == "agent_file_receipt":
                receipt = json.loads(row["content"])
                resources = AgentWorkResources(Path(self.db.path).absolute().parent / "agent-work",
                    tenant_id=TenantContext.current_tenant_id(), company_id=company,
                    work_ref=work_ref, task_id=proof["task_ref"])
                resources.read_output(receipt)
                item.update(file_sha256=receipt["sha256"], file_verification="FILE_HASH_VERIFIED")
            artifacts.append(item)
        return {"task_ref": proof["task_ref"], "usage_record_id": proof["provenance"]["usage_record_id"],
            "task_output_sha256": proof["task_output_sha256"],
            "source_snapshot_sha256": hashlib.sha256(json.dumps(proof["source"], sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
            "artifacts": artifacts, "file_receipt_count": len(expected), "content_verification": "UNVERIFIED"}

    def agent_candidate_reply_proof(self, company, work_ref, task_ref, reply):
        from .writing_chapter_service import utf16_slice
        if not isinstance(reply, dict):
            raise ValueError("候选来源参数无效。")
        file_keys = {"artifact_ref", "artifact_content_sha256", "file_sha256", "task_output_sha256"}
        expected = {"start", "end", "excerpt", "text_sha256"}
        if "artifact_ref" in reply:
            expected |= file_keys
        if set(reply) != expected:
            raise ValueError("候选必须保留同一原文件和完整版本摘要。")
        proof = self.agent_result_proof(company, work_ref, task_ref,
            artifact_ref=reply.get("artifact_ref"), for_candidate=True)
        if (any(reply[key] != proof.get(key) for key in file_keys if key in reply)
                or reply["text_sha256"] != proof["text_sha256"]
                or utf16_slice(proof["text"], reply["start"], reply["end"]) != reply["excerpt"]
                or not reply["excerpt"].strip()):
            raise ValueError("所选成果文字与原完整结果不一致。")
        return proof

    def materialize_agent_candidate(self, company, work_ref, task_ref, reply):
        from .writing_chapter_service import WritingChapterService
        proof = self.agent_candidate_reply_proof(company, work_ref, task_ref, reply)
        if proof["source"]["kind"] == "writing":
            service = WritingChapterService(self.db, conversation_service=self)
        elif proof["source"]["kind"] == "content-growth":
            from .content_growth_service import ContentGrowthService
            service = ContentGrowthService(self.db, conversations=self)
        else:
            from .music_service import MusicService
            service = MusicService(self.db, conversations=self)
        return service.materialize_agent_candidate(proof, reply)

    def _rows(self, con, conversation_id):
        rows = con.execute(
            "select event_id,event_type,payload,created_at from evolution_events "
            "where tenant_id=? and correlation_id=? and event_type like 'conversation.%' order by event_id",
            (TenantContext.current_tenant_id(), conversation_id),
        ).fetchall()
        return [{**dict(row), "payload": json.loads(row["payload"])} for row in rows]

    def references(self, company_id, context, references):
        if not isinstance(references, list) or len(references) > 8:
            raise ValueError("Select at most eight references")
        resolved = []
        for reference in references:
            ref = reference.get("reference_id")
            kind = reference.get("kind")
            if (not isinstance(ref, str) or not 1 <= len(ref) <= 256
                    or reference.get("workspace_id") != context["workspace_id"]):
                raise RuntimeScopeError("Reference is outside the current assignment")
            if kind != "KNOWLEDGE":
                with self.db.connect() as con:
                    try:
                        ResourceScopePolicy.require_same_execution_scope(context, ResourceScopePolicy.reference_scope(
                            con, tenant_id=TenantContext.current_tenant_id(), company_id=company_id, reference_id=ref))
                    except ValueError as error:
                        raise RuntimeScopeError(str(error)) from error
            if kind in {"WORK", "DECISION_PACKET", "CONTENT_ITEM", "CONTENT_VERSION"}:
                item = self.foundation.get(ref)
                if (item["company_id"] != company_id or item.get("workspace_id") != context["workspace_id"]
                        or item["entity_type"] != kind):
                    raise RuntimeScopeError("Reference scope mismatch")
                title = item["data"].get("title") or item["data"].get("name") or "查看来源"
            elif kind == "PACKAGE_DOMAIN_OBJECT":
                from .music_entry_service import MusicEntryService
                from .runtime.music import MusicRuntime
                MusicEntryService(self.db).authoring_scope(company_id, context["workspace_id"])
                with self.db.connect() as con:
                    item = MusicRuntime(self.db).get(con, company_id, context["workspace_id"], ref)
                if item["data"]["kind"] not in {"Song", "LyricsVersion", "ProductionVersion", "Candidate", "MasterRevision"}:
                    raise RuntimeScopeError("歌曲引用类型不受支持。")
                if not reference.get("purpose"):
                    raise ValueError("歌曲引用需要明确用途和版本。")
                title = item["data"].get("title") or "歌曲原版本"
            elif kind == "KNOWLEDGE":
                item = KnowledgeService(self.db).get_entry(ref)
                if not KnowledgeService._compatible(item, context):
                    raise RuntimeScopeError("Knowledge is outside the current assignment")
                title = item.get("title") or "查看资料"
            elif kind in {"RESULT", "ARTIFACT", "EVIDENCE"}:
                item = ResultAttention(self.db).detail(company_id, context["workspace_id"], ref, scope=context)
                if item["kind"] != kind:
                    raise RuntimeScopeError("Reference type mismatch")
                title = item.get("title") or "查看来源"
            else:
                raise ValueError("Unsupported reference type")
            value = {"reference_id": ref, "workspace_id": context["workspace_id"], "kind": kind, "title": str(title)[:120]}
            bound = any(reference.get(key) is not None for key in ("version_ref", "purpose", "locator"))
            if bound:
                purpose = reference.get("purpose")
                if purpose not in {"BACKGROUND", "FACT", "STYLE", "CONSTRAINT"}:
                    raise ValueError("引用用途不合法。")
                if kind == "CONTENT_ITEM":
                    version = item.get("current_version_id")
                elif kind == "CONTENT_VERSION" or (kind == "PACKAGE_DOMAIN_OBJECT" and item["data"]["kind"] != "Song"):
                    version = item["entity_id"]
                else:
                    # Snapshot actual persisted content, never a client supplied version label.
                    version = digest(item)
                if reference.get("version_ref") is not None and reference["version_ref"] != version:
                    raise ValueError("引用版本已改变，请核对原依据和当前版本。")
                locator = reference.get("locator") or ""
                if not isinstance(locator, str) or len(locator) > 256:
                    raise ValueError("引用定位不合法。")
                value.update(version_ref=version, purpose=purpose, locator=locator)
            if value not in resolved:
                resolved.append(value)
        return resolved

    def receive_dialogue(self, company, conversation_id, *, workspace_id, message_ref, source):
        kind = source.get("kind")
        if any(not isinstance(v, str) or not v or len(v) > 256 for k, v in source.items() if k != "expected"):
            raise ValueError("接收依据必须使用原对象标识。")
        if kind == "writing" and set(source) == {"kind", "book_ref", "chapter_ref", "expected_draft_ref"}:
            from .writing_chapter_service import WritingChapterService
            result = WritingChapterService(self.db, conversation_service=self).command(company, workspace_id,
                source["book_ref"], source["chapter_ref"], "candidate.dialogue-recorded",
                request_id="dialogue-" + digest([conversation_id, message_ref, source["chapter_ref"]]),
                expected_draft_ref=source["expected_draft_ref"],
                data={"conversation_ref": conversation_id, "message_ref": message_ref})
            return {"candidate_ref": result["ref"]}
        if kind == "content-growth" and set(source) == {"kind", "content_ref", "expected_version_ref"}:
            from .content_growth_service import ContentGrowthService
            return ContentGrowthService(self.db, conversations=self).receive_dialogue(company, workspace_id,
                source["content_ref"], source["expected_version_ref"], conversation_id, message_ref)
        if kind == "music" and set(source) == {"kind", "song_ref", "expected"}:
            from .music_service import MusicService
            return MusicService(self.db, conversations=self).receive_dialogue(company, workspace_id,
                source["song_ref"], source["expected"], conversation_id, message_ref)
        raise ValueError("接收对象与当前版本依据不完整。")

    def dialogue_result(self, con, company, workspace, object_ref, conversation_id, message_ref):
        """Validate original ordinary dialogue without inventing a generation version or Work."""
        owner = self.owner(company, conversation_id=conversation_id)
        discussion = owner.get("discussion_scope") or {}
        if discussion.get("workspace_id") != workspace or discussion.get("object_ref") != object_ref:
            raise RuntimeScopeError("回复不属于当前业务对象的讨论。")
        context = self.context(company, owner["owner_ref"], discussion.get("assignment_ref"))
        if context["workspace_id"] != workspace:
            raise RuntimeScopeError("当前员工责任已变化。")
        messages = [r["payload"] for r in self._rows(con, conversation_id) if r["event_type"] == "conversation.message"]
        replies = [m for m in messages if m["message_id"] == message_ref]
        if len(replies) != 1:
            raise RuntimeScopeError("原回复不存在。")
        reply = replies[0]
        if (reply.get("sender") != {"kind": "EMPLOYEE", "ref": owner["owner_ref"]}
                or reply.get("context") != context or not reply.get("body", "").strip()):
            raise RuntimeScopeError("原回复与当前员工责任不一致。")
        task_ref = reply.get("task_ref")
        rows = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? and event_type='conversation.execution_bound'",
            (TenantContext.current_tenant_id(), task_ref)).fetchall()
        if len(rows) != 1:
            raise RuntimeScopeError("回复没有唯一执行来源。")
        claim = json.loads(rows[0][0]); execution = claim.get("execution_selection") or {}
        if (claim.get("conversation_id") != conversation_id or execution.get("purpose") != "CONVERSATION_REPLY"
                or execution.get("scope") != {"company_id": company, "workspace_id": workspace}
                or reply.get("provenance", {}).get("execution_selection") != execution):
            raise RuntimeScopeError("回复不是当前对象的普通员工交流结果。")
        finishes = [r["payload"] for r in self._rows(con, conversation_id)
                    if r["event_type"] == "conversation.attempt.finished" and r["payload"].get("attempt_id") == claim.get("attempt_id")]
        task = con.execute("select * from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
            (TenantContext.current_tenant_id(), company, workspace, task_ref)).fetchone()
        usage = con.execute("select * from ai_usage_records where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
            (TenantContext.current_tenant_id(), company, workspace, task_ref)).fetchall()
        provenance = reply.get("provenance") or {}
        if (len(finishes) != 1 or finishes[0].get("status") != "COMPLETED" or finishes[0].get("effect_status") == "UNKNOWN"
                or not task or task["status"] != "COMPLETED" or task["output"] != reply["body"]
                or task["execution_ref"] != claim.get("attempt_id") or task["work_ref"]
                or len(usage) != 1 or usage[0]["execution_status"] != "success" or usage[0]["fallback_from_model"]
                or usage[0]["usage_record_id"] != provenance.get("usage", {}).get("usage_record_id")
                or usage[0]["execution_ref"] != claim.get("attempt_id")
                or usage[0]["employee_id"] != task["employee_id"]
                or usage[0]["capability_binding_id"] != execution.get("binding_id")
                or usage[0]["capability_id"] != execution.get("model", {}).get("model_key")):
            raise RuntimeScopeError("回复、已完成任务与唯一实际用量不一致。")
        verified = EmployeeExecutionIdentity(self.db).verify_task_callback(company_id=company,
            workspace_id=workspace, runtime_employee_ref=owner["owner_ref"], task_ref=task_ref, session_ref="")
        if verified.get("verification_status") != "VERIFIED" or reply.get("idempotency_key") != claim.get("attempt_id"):
            raise RuntimeScopeError("原员工执行身份或回复关联不能核验。")
        return {"conversation_ref": conversation_id, "message_ref": message_ref, "task_ref": task_ref,
                "text": reply["body"], "provenance": provenance}

    @contextmanager
    def model_credential_wait(self, attempt_id):
        """Expose a live wait without storing or returning credential information."""
        key = (TenantContext.current_tenant_id(), attempt_id)
        self.credential_wait_started[key] = monotonic()
        try:
            yield
        finally:
            self.credential_wait_started.pop(key, None)

    def _project_credential_wait(self, attempt):
        if attempt["status"] != "RUNNING":
            return
        key = (TenantContext.current_tenant_id(), attempt["attempt_id"])
        started = self.credential_wait_started.get(key)
        if started is not None:
            attempt["credential_wait"] = "LONG_WAIT" if monotonic() - started >= 30 else "WAITING"

    def _project_pre_outbound_failure(self, con, company, conversation_id, attempt):
        """Reconcile only finished ordinary replies with the original zero-outbound receipt."""
        attempt_id, task_ref = attempt.get("attempt_id"), attempt.get("task_ref")
        selection = attempt.get("execution_selection")
        if (attempt.get("status") not in {"FAILED", "UNVERIFIED"} or attempt.get("effect_status") != "UNKNOWN"
                or not all(isinstance(ref, str) and ref for ref in
                           (attempt_id, task_ref, attempt.get("message_id"), attempt.get("employee_ref")))
                or attempt_id in self.running
                or attempt.get("company_id") != company or attempt.get("conversation_id") != conversation_id
                or not isinstance(selection, dict)
                or selection.get("purpose") != "CONVERSATION_REPLY" or selection.get("work_ref")
                or selection.get("source_class") != "EMPLOYEE_BINDING"):
            return
        tenant = TenantContext.current_tenant_id()
        context, grant, model = attempt.get("context"), selection.get("grant"), selection.get("model")
        if not all(isinstance(value, dict) for value in (context, grant, model)):
            return
        workspace = context.get("workspace_id")
        if (not isinstance(workspace, str) or not workspace
                or context.get("company_id") != company
                or selection.get("scope") != {"company_id": company, "workspace_id": workspace}
                or grant.get("grant_ref") != "company-text-attempt:" + attempt_id
                or not grant.get("policy_revision") or not grant.get("price_version")
                or not model.get("model_key") or not model.get("source") or not selection.get("binding_id")
                or (grant.get("tenant_id"), grant.get("company_id"), grant.get("workspace_id"), grant.get("model_key"))
                    != (tenant, company, workspace, model["model_key"])):
            return
        original_message = con.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='conversation.message' and idempotency_key=? and json_valid(payload)",
            (tenant, conversation_id, attempt["message_id"]),
        ).fetchone()
        if not original_message:
            return
        message = json.loads(original_message["payload"])
        if (message.get("message_id") != attempt["message_id"] or message.get("conversation_id") != conversation_id
                or message.get("context") != context or message.get("sender", {}).get("kind") != "CEO"):
            return
        task = con.execute(
            "select status, work_ref, employee_id, requested_capability_type, requested_capability_id, "
            "requested_capability_source, scope_type, scope_ref from tasks where tenant_id=? and company_id=? "
            "and workspace_id=? and task_id=? and execution_ref=?",
            (tenant, company, workspace, task_ref, attempt_id),
        ).fetchone()
        if (not task or task["status"] != "FAILED" or task["work_ref"] or not task["employee_id"]
                or (task["requested_capability_type"], task["requested_capability_id"], task["requested_capability_source"])
                    != ("model", model["model_key"], model["source"])
                or (task["scope_type"], task["scope_ref"]) != (context.get("scope_type"), context.get("scope_ref"))):
            return
        original_fields = ("attempt_id", "message_id", "company_id", "conversation_id",
                           "employee_ref", "context", "execution_selection")
        for event, ref in (("conversation.attempt.started", conversation_id), ("conversation.execution_bound", task_ref),
                           ("conversation.attempt.finished", conversation_id)):
            records = con.execute(
                "select payload from evolution_events where tenant_id=? and correlation_id=? and event_type=? "
                "and case when json_valid(payload) then json_extract(payload,'$.attempt_id') end=?",
                (tenant, ref, event, attempt_id),
            ).fetchall()
            if len(records) != 1:
                return
            source = json.loads(records[0]["payload"])
            if any(source.get(k) != attempt.get(k) for k in original_fields):
                return
            if event == "conversation.attempt.finished" and source != attempt:
                return
            if event == "conversation.execution_bound" and (
                    (source.get("task_id"), source.get("company_employee_ref"), source.get("binding_id"), source.get("capability_id"))
                    != (task_ref, task["employee_id"], selection["binding_id"], model["model_key"])):
                return
        from .company_execution_policy import CompanyExecutionPolicy
        policy = CompanyExecutionPolicy(self.db)
        try:
            reservations = policy.rows(con, company, "reserved")
            settlements = policy.rows(con, company, "settled")
        except (TypeError, ValueError):
            return
        if not all(isinstance(receipt, dict) for receipt in reservations + settlements):
            return
        reservations = [r for r in reservations if r.get("attempt_id") == attempt_id]
        settlements = [r for r in settlements if r.get("attempt_id") == attempt_id]
        if (len(reservations) != 1 or len(settlements) != 1
                or reservations[0].get("grant") != grant or reservations[0].get("context") != context
                or reservations[0].get("message_id") != attempt.get("message_id")):
            return
        settled = settlements[0]
        estimate = settled.get("estimated_micro_cny")
        if (settled.get("basis") != "NO_EXECUTOR_LAUNCH" or type(estimate) is not int or estimate != 0
                or settled.get("currency") != "CNY" or settled.get("actual_paid") is not None
                or settled.get("price_version") != grant["price_version"]):
            return
        outbound = con.execute(
            "select 1 from evolution_events where tenant_id=? "
            "and event_type in ('conversation.outbound.claimed','writing.outbound.claimed','cg.outbound.claimed','music.outbound.claimed') "
            "and (correlation_id=? or case when json_valid(payload) then json_extract(payload,'$.attempt_id') end=?) limit 1",
            (tenant, task_ref, attempt_id),
        ).fetchone()
        usage = con.execute(
            "select 1 from ai_usage_records where tenant_id=? and (task_id=? or execution_ref=?) limit 1",
            (tenant, task_ref, attempt_id),
        ).fetchone()
        if not outbound and not usage:
            attempt.update(status="FAILED", effect_status="SETTLED", recovery_basis="NO_EXECUTOR_LAUNCH")
            return True

    def read_request(self, company_id, conversation_id, request_id=None):
        """Strict original-query projection: no open, task transition or outbound call."""
        owner = self.owner(company_id, conversation_id=conversation_id)
        with self.db.connect() as con:
            rows = self._rows(con, conversation_id)
        messages = [r["payload"] for r in rows if r["event_type"] == "conversation.message"]
        attempts = {}
        for row in rows:
            if row["event_type"] in {"conversation.attempt.started", "conversation.attempt.finished"}:
                attempt = dict(row["payload"])
                if row["event_type"] == "conversation.attempt.finished" and attempt.get("effect_status") == "UNKNOWN":
                    with self.db.connect() as con:
                        self._project_pre_outbound_failure(con, company_id, conversation_id, attempt)
                if attempt["status"] == "RUNNING" and attempt["attempt_id"] not in self.running:
                    attempt.update(status="UNKNOWN", effect_status="UNKNOWN")
                if attempt.get("effect_status") == "UNKNOWN":
                    attempt["status"] = "UNKNOWN"
                self._project_credential_wait(attempt)
                attempts[attempt["attempt_id"]] = attempt
        if request_id is not None:
            originals = [m for m in messages if m.get("idempotency_key") == request_id and m["sender"]["kind"] == "CEO"]
            if len(originals) != 1:
                raise KeyError("原请求不存在。")
            selected = [a for a in attempts.values() if a["message_id"] == originals[0]["message_id"]]
            messages = originals + [m for m in messages if any(m.get("idempotency_key") == a["attempt_id"] for a in selected)]
        else:
            selected = list(attempts.values())
        return {**owner, "messages": messages, "attempts": selected}

    def read_attempt(self, company_id, conversation_id, attempt_id):
        result = self.read_request(company_id, conversation_id)
        matches = [a for a in result["attempts"] if a["attempt_id"] == attempt_id]
        if len(matches) != 1:
            raise KeyError("原执行请求不存在。")
        attempt = matches[0]
        return {"attempt": attempt, "messages": [m for m in result["messages"] if m["message_id"] == attempt["message_id"]
                or m.get("idempotency_key") == attempt_id]}

    def read(self, company_id, employee_ref=None, conversation_id=None):
        owner = self.owner(company_id, employee_ref, conversation_id)
        with self.db.connect() as con:
            rows = self._rows(con, owner["conversation_id"])
        attempts = {}
        finished = set()
        for row in rows:
            if row["event_type"].startswith("conversation.attempt."):
                value = row["payload"]
                attempts[value["attempt_id"]] = value
                if row["event_type"] == "conversation.attempt.finished":
                    finished.add(value["attempt_id"])
        for attempt in attempts.values():
            if attempt["status"] == "RUNNING" and attempt["attempt_id"] not in self.running:
                attempt["status"] = "UNVERIFIED"
                if (attempt.get("execution_selection") or {}).get("purpose") == "CONVERSATION_REPLY":
                    attempt["effect_status"] = "UNKNOWN"
            with self.db.connect() as con:
                if attempt["attempt_id"] in finished:
                    self._project_pre_outbound_failure(con, company_id, owner["conversation_id"], attempt)
                self._terminal_failure(con, attempt)
            if attempt.get("effect_status") == "UNKNOWN":
                attempt["status"] = "UNKNOWN"
            self._project_credential_wait(attempt)
        return {**owner, "messages": [row["payload"] for row in rows if row["event_type"] == "conversation.message"],
                "attempts": list(attempts.values())}

    def _terminal_failure(self, con, attempt):
        """A failed Task closes execution, not its unknown outbound metering."""
        if attempt["status"] != "UNVERIFIED" or not attempt.get("task_ref") or attempt["attempt_id"] in self.running:
            return
        task = con.execute("select status from tasks where tenant_id=? and company_id=? and task_id=? and execution_ref=?",
            (TenantContext.current_tenant_id(), attempt["company_id"], attempt["task_ref"], attempt["attempt_id"])).fetchone()
        if task and task["status"] == "FAILED":
            attempt["status"] = "FAILED"
            attempt["recovery_basis"] = "PERSISTED_TASK_FAILED; OUTBOUND_METERING_NOT_RECONCILED"

    def available_assignments(self, company_id, employee_ref):
        employee_ref = self.owner(company_id, employee_ref)["owner_ref"]
        return [{"assignment_ref": row["entity_id"], "workspace_id": row.get("workspace_id"),
                 "responsibility": row["data"].get("responsibility") or ""}
                for row in self.foundation.list("RESPONSIBILITY_ASSIGNMENT", company_id=company_id)
                if row["lifecycle_status"] == "ACTIVE" and row["data"].get("employeeRef") == employee_ref]

    def execution_models(self, company_id, employee_ref):
        """Global model qualification is visible independently of an internal binding."""
        from .model_preferences import TenantModelPreferenceResolver
        employee_ref = self.owner(company_id, employee_ref)["owner_ref"]
        employee = self.foundation.get(employee_ref)
        company_employee = employee["data"].get("companyEmployeeRef")
        with self.db.connect() as con:
            bindings = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? "
                "and capability_type='model' and enabled=1", (TenantContext.current_tenant_id(), company_employee)).fetchall() if company_employee else []
        models = TenantModelPreferenceResolver(self.db).available_models()
        result = []
        for model in models:
            matches = [row for row in bindings if row["capability_source"] == model["source"] and row["capability_id"] == model["model_key"]]
            result.append({"binding_id": matches[0]["id"] if len(matches) == 1 else None,
                           "source": model["source"], "model_key": model["model_key"],
                           "display_name": model.get("display_name") or model["model_key"]})
        return result

    def conversation_metadata(self, company_id, employee_ref):
        from .model_preferences import TenantModelPreferenceResolver
        preference = TenantModelPreferenceResolver(self.db).read_current()["preference"]
        readiness = []
        for assignment in self.available_assignments(company_id, employee_ref):
            company_text = False
            try:
                context = self.context(company_id, employee_ref, assignment["assignment_ref"])
                company_text = self.professional_workspace(context)
                if company_text:
                    choices = TenantModelPreferenceResolver(self.db).available_models()
                    reasons = []
                    for model in choices:
                        try:
                            if self.professional_policy is None:
                                raise ValueError("当前专业对话尚未接入执行许可。")
                            self.professional_policy(context, model["model_key"], readiness=True)
                            break
                        except (KeyError, ValueError, RuntimeScopeError) as error:
                            reasons.append(str(error))
                    else:
                        raise ValueError(reasons[0] if reasons else "请先配置一个当前可用的全局模型。")
                readiness.append({"assignment_ref": assignment["assignment_ref"], "status": "AVAILABLE",
                                  "company_text": company_text})
            except (KeyError, ValueError, RuntimeScopeError) as error:
                readiness.append({"assignment_ref": assignment["assignment_ref"], "status": "UNAVAILABLE",
                                  "reason": str(error), "company_text": company_text})
        with self.db.connect() as con:
            rows = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.opened' "
                "and json_extract(payload,'$.company_id')=? and json_extract(payload,'$.owner_ref')=?",
                (TenantContext.current_tenant_id(), company_id, employee_ref)).fetchall()
        ceo = ResultAttention(self.db).actor(company_id)
        topics = [{"conversation_id": value["conversation_id"], **value["discussion_scope"]}
                  for row in rows for value in [json.loads(row["payload"])] if value.get("discussion_scope")
                  and value["participants"][0] == {"kind": "CEO", "ref": ceo}]
        from .company_execution_policy import CompanyExecutionPolicy
        agent_policy = CompanyExecutionPolicy(self.db).agent_readiness(company_id)
        agents = [{"capability_id": item["capability_id"], "source": "tenant_private",
                   "display_name": item["display_name"], "kind": item.get("metadata", {}).get("kind", ""),
                   "state": agent_policy["state"], "reason": agent_policy["reason"]}
                  for item in self.db.list_tenant_private_capabilities(TenantContext.current_tenant_id(), "agent")]
        try:
            runtime_employee = self.foundation.get(self.owner(company_id, employee_ref)["owner_ref"])
            identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company_id,
                workspace_id=runtime_employee["workspace_id"], runtime_employee_ref=runtime_employee["entity_id"])
            with self.db.connect() as con:
                bindings = con.execute("select id,capability_id from employee_capability_bindings where tenant_id=? "
                    "and employee_id=? and enabled=1 and capability_type='agent' and capability_source='tenant_private'",
                    (TenantContext.current_tenant_id(), identity["company_employee_ref"])).fetchall()
            for agent in agents:
                matches = [row["id"] for row in bindings if row["capability_id"] == agent["capability_id"]]
                agent["binding_id"] = matches[0] if len(matches) == 1 else None
        except (KeyError, ValueError, RuntimeScopeError):
            pass
        return {"model_preference": preference, "execution_readiness": readiness, "discussion_topics": topics,
                "execution_agents": agents, "agent_execution_readiness": agent_policy}

    def professional_workspace(self, context):
        with self.db.connect() as con:
            row = con.execute("select json_extract(blueprint_json, '$.businessType') as business_type from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (TenantContext.current_tenant_id(), context["company_id"], context["workspace_id"])).fetchone()
        return bool(row and row["business_type"] == "PACKAGE")

    def professional_execution(self, context, model_key, *, prepare=False, attempt_id=None, connection=None):
        if self.professional_policy is None:
            raise RuntimeScopeError("当前专业员工回复尚无已接入的执行授权。")
        return self.professional_policy(context, model_key, prepare=prepare, attempt_id=attempt_id, connection=connection)

    def computer_access(self, company_id, employee_ref=None):
        """Read-only ADR-0046 projection for the conversation Composer slot.

        CEO-only conversations and Employees with enabled model bridges run on
        model executors, so computer access is honestly not applicable. An
        Employee without a verified execution bridge has no access evidence.
        """
        if not employee_ref:
            return dict(_COMPUTER_ACCESS_MODEL_NOT_APPLICABLE)
        return dict(_COMPUTER_ACCESS_MODEL_NOT_APPLICABLE
                    if self.execution_models(company_id, employee_ref)
                    else _COMPUTER_ACCESS_NO_BRIDGE)

    def validate_conversation_selection(self, selection, *, company_id, runtime_employee_ref, context, connection=None, attempt_id=None):
        """Server validator for purpose=CONVERSATION_REPLY direct Employee dialogue."""
        if selection.get("purpose") != "CONVERSATION_REPLY":
            raise ValueError("Unknown selected execution purpose")
        if (selection.get("scope") or {}).get("company_id") != company_id:
            raise RuntimeScopeError("模型选择不属于当前公司。")
        if (selection.get("scope") or {}).get("workspace_id") != context.get("workspace_id"):
            raise RuntimeScopeError("模型选择不属于当前工作空间。")
        model = selection.get("model") or {}
        if self.professional_workspace(context):
            policy = self.professional_execution(context, model.get("model_key"), attempt_id=attempt_id, connection=connection)
            if selection.get("grant") != policy.get("grant"):
                raise RuntimeScopeError("专业会话授权快照已变化。")
        identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company_id,
            workspace_id=context.get("workspace_id"), runtime_employee_ref=runtime_employee_ref)
        if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
            raise RuntimeScopeError("Employee execution identity must be explicitly bound")
        sql = ("select id from employee_capability_bindings where tenant_id=? and employee_id=? and enabled=1 "
               "and capability_type='model' and id=? and capability_source=? and capability_id=?")
        args = (TenantContext.current_tenant_id(), identity["company_employee_ref"],
                selection.get("binding_id"), model.get("source"), model.get("model_key"))
        if connection is not None:
            rows = connection.execute(sql, args).fetchall()
        else:
            with self.db.connect() as con:
                rows = con.execute(sql, args).fetchall()
        if len(rows) != 1:
            raise ValueError("所选员工模型绑定不可用；输入已保留，请重新选择模型。")

    def reference_options(self, company_id, employee_ref, assignment_ref):
        context = self.context(company_id, employee_ref, assignment_ref)
        workspace = context["workspace_id"]
        with self.db.connect() as con:
            rows = con.execute("select * from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id is ? and entity_type in ('WORK','DECISION_PACKET','EVIDENCE') order by updated_at desc limit 20",
                (TenantContext.current_tenant_id(), company_id, workspace)).fetchall()
            tasks = con.execute("select task_id,content from tasks where tenant_id=? and company_id=? and workspace_id is ? "
                "and status in ('COMPLETED','FAILED') order by updated_at desc limit 20",
                (TenantContext.current_tenant_id(), company_id, workspace)).fetchall()
        options = []
        with self.db.connect() as con:
            for row in rows:
                try:
                    ResourceScopePolicy.require_same_execution_scope(context,
                        ResourceScopePolicy.execution_scope_from_record(con,
                            tenant_id=TenantContext.current_tenant_id(), record=dict(row)))
                except ValueError:
                    continue
                data = json.loads(row["data_json"])
                options.append({"reference_id": row["entity_id"], "kind": row["entity_type"],
                    "workspace_id": workspace, "title": str(data.get("title") or data.get("name") or data.get("summary") or "查看来源")[:120]})
        for row in tasks:
            try:
                result = ResultAttention(self.db).detail(company_id, workspace, "task:" + row["task_id"], scope=context)
            except (KeyError, ValueError, RuntimeScopeError):
                continue
            options.append({"reference_id": result["reference_id"], "kind": "RESULT", "workspace_id": workspace,
                            "title": result["title"]})
        # Bounded summaries only; each selected entry is scope-checked again on send.
        for entry in KnowledgeService(self.db).list_entries(company_id=company_id, limit=20)["entries"]:
            try:
                options.extend(self.references(company_id, context, [{"reference_id": entry["id"],
                    "kind": "KNOWLEDGE", "workspace_id": workspace}]))
            except RuntimeScopeError:
                continue
        return options

    def prepare(self, company_id, employee_ref, *, body, request_id, assignment_ref, retry_no=0, references=None, conversation_id=None, execution_selection=None, display_body=None):
        if retry_no not in (0, 1):
            raise ValueError("Only one explicit retry is allowed")
        # Scope and authorization are server facts, including requests omitting selection.
        context = self.context(company_id, employee_ref, assignment_ref)
        company_retry = False
        if (not execution_selection or execution_selection.get("purpose") == "CONVERSATION_REPLY") and self.professional_workspace(context):
            from .model_preferences import TenantModelPreferenceResolver
            resolver = TenantModelPreferenceResolver(self.db)
            preference = resolver.read_current()["preference"]
            if execution_selection and execution_selection.get("scope") != {"company_id": company_id, "workspace_id": context["workspace_id"]}:
                raise RuntimeScopeError("所选模型不属于当前工作范围。")
            selected_model = (execution_selection or {}).get("model") or preference or {}
            model = resolver._require_eligible_model(TenantContext.current_tenant_id(), selected_model.get("model_key"))
            if selected_model.get("source") not in {None, model["source"]}:
                raise RuntimeScopeError("所选模型来源不匹配。")
            # An idempotent read never recreates a binding or consumes a new grant.
            prior_view = self.read(company_id, employee_ref, conversation_id=conversation_id)
            prior_message = next((m for m in prior_view["messages"] if m.get("idempotency_key") == request_id), None)
            own_attempts = [a for a in prior_view["attempts"] if prior_message and a["message_id"] == prior_message["message_id"]]
            previous = own_attempts[0] if own_attempts else None
            if retry_no and previous is None:
                raise RuntimeScopeError("原请求不存在，不能重试。")
            if previous is None and any(a.get("status") in {"RUNNING", "UNVERIFIED", "UNKNOWN"} or a.get("effect_status") == "UNKNOWN" for a in prior_view["attempts"]):
                raise RuntimeScopeError("原讨论请求尚未核验，不能更换模型或发起新的执行。")
            original_selection = (previous or {}).get("execution_selection") or {}
            company_retry = bool(retry_no and original_selection.get("grant", {}).get("policy_revision"))
            if company_retry and (
                    previous.get("recovery_basis") != "NO_EXECUTOR_LAUNCH"
                    or previous["context"] != context
                    or original_selection.get("model") != {"source": model["source"], "model_key": model["model_key"]}
                    or (execution_selection or {}).get("binding_id") not in {None, "", original_selection["binding_id"]}):
                raise RuntimeScopeError("只能使用原员工、模型和来源，重试已核验未外发的请求。")
            if company_retry and len(own_attempts) > retry_no:
                recorded = own_attempts[retry_no]["execution_selection"]
                policy = {"binding": {"id": recorded["binding_id"]}, "grant": recorded["grant"]}
            else:
                policy = self.professional_execution(context, model["model_key"], prepare=previous is None,
                                                     attempt_id=previous["attempt_id"] if previous and not company_retry else None)
            binding = policy.get("binding") or policy.get("model_binding")
            if not binding:
                raise RuntimeScopeError("当前专业模型没有可验证的内部绑定。")
            if company_retry and binding["id"] != original_selection["binding_id"]:
                raise RuntimeScopeError("原员工模型绑定已变化，不能重试原请求。")
            if (execution_selection or {}).get("binding_id") not in {None, "", binding["id"]}:
                raise RuntimeScopeError("所选模型内部绑定已变化。")
            execution_selection = {"purpose": "CONVERSATION_REPLY", "binding_id": binding["id"],
                "scope": {"company_id": company_id, "workspace_id": context["workspace_id"]},
                "model": {"source": model["source"], "model_key": model["model_key"]},
                "grant": policy["grant"]}
        cg = execution_selection is not None and execution_selection.get("purpose") in {"CG_GRAPHIC_REPLY", "CG_CONTENT_REPLY", "MUSIC_SONG_REPLY"}
        if cg and retry_no:
            raise ValueError("内容请求只能核验原请求，不能重放。")
        owner = self.owner(company_id, employee_ref, conversation_id) if cg else self.open(company_id, employee_ref, conversation_id)
        employee_ref = owner["owner_ref"]
        message = self.append_ceo(company_id, employee_ref, body=body, request_id=request_id, assignment_ref=assignment_ref, references=references, conversation_id=owner["conversation_id"], display_body=display_body)
        conversation_id = owner["conversation_id"]
        # ponytail: one in-flight turn per conversation; add a queue only if ordered concurrent turns are needed.
        with self.db.connect() as con:
            con.execute("begin immediate")
            rows = self._rows(con, conversation_id)
            claims = [row["payload"] for row in rows if row["event_type"] == "conversation.attempt.started"]
            finished = {row["payload"]["attempt_id"]: row["payload"] for row in rows if row["event_type"] == "conversation.attempt.finished"}
            verified_pre_outbound = set()
            if not cg:
                for attempt in finished.values():
                    if self._project_pre_outbound_failure(con, company_id, conversation_id, attempt):
                        verified_pre_outbound.add(attempt["attempt_id"])
                    self._terminal_failure(con, attempt)
                    if attempt.get("effect_status") == "UNKNOWN":
                        attempt["status"] = "UNKNOWN"
            own = [claim for claim in claims if claim["message_id"] == message["message_id"]]
            writing_work_retry = bool(retry_no == 1 and own and execution_selection
                and execution_selection.get("purpose") == "WRITING_CHAPTER_REPLY"
                and execution_selection.get("work_ref")
                and execution_selection.get("work_ref") == (own[0].get("execution_selection") or {}).get("work_ref")
                and execution_selection.get("retry_of_attempt") == own[0]["attempt_id"])
            if (retry_no and own and (own[0].get("execution_selection") or {}).get("grant", {}).get("policy_revision")
                    and not company_retry and not writing_work_retry):
                raise RuntimeScopeError("原专业回复只能在原工作范围内使用当前公司许可重试。")
            if company_retry and (not own or own[0]["attempt_id"] not in verified_pre_outbound):
                raise RuntimeScopeError("原请求未证实在外发前终止，不能重试。")
            if len(own) > retry_no:
                if execution_selection is not None:
                    prior = {key: value for key, value in (own[retry_no].get("execution_selection") or {}).items()
                             if key != "source_class"}
                    if company_retry:
                        # A replay returns the existing retry slot, including its original reservation.
                        prior["grant"] = execution_selection["grant"]
                    elif prior.get("grant", {}).get("policy_revision") and prior["grant"]["policy_revision"] == execution_selection.get("grant", {}).get("policy_revision"):
                        prior["grant"] = {**prior["grant"], "grant_ref": execution_selection["grant"]["grant_ref"]}
                    if prior != execution_selection:
                        raise ValueError("同一请求不能更换模型、员工或依据。")
                return own[retry_no], False
            if retry_no and (len(own) != 1 or finished.get(own[0]["attempt_id"], {}).get("status") != "FAILED"):
                raise ValueError("Only a confirmed failed attempt can be retried")
            if any(finished.get(claim["attempt_id"], {}).get("status") not in {"FAILED", "COMPLETED", "CANCELLED"} or (cg and finished.get(claim["attempt_id"], {}).get("effect_status") == "UNKNOWN") for claim in claims):
                raise ValueError("上一条消息仍在处理或等待恢复确认")
            context = self.context(company_id, employee_ref, assignment_ref)
            if execution_selection is not None:
                if execution_selection.get("purpose") == "CONVERSATION_REPLY":
                    self.validate_conversation_selection(execution_selection, company_id=company_id,
                        runtime_employee_ref=employee_ref, context=context, connection=con)
                else:
                    if self.selection_validator is None:
                        raise RuntimeScopeError("Execution selection has no registered server validator")
                    self.selection_validator(execution_selection, connection=con)
            claim = {"attempt_id": "conversation-execution-" + str(uuid.uuid4()),
                     "message_id": message["message_id"], "conversation_id": conversation_id,
                     "company_id": company_id, "employee_ref": employee_ref,
                     "context": context, "status": "RUNNING", "process_id": self.process_id,
                     "retry_no": retry_no}
            if execution_selection is not None:
                stored_selection = json.loads(json.dumps(execution_selection))
                if stored_selection.get("grant", {}).get("policy_revision"):
                    from .company_execution_policy import CompanyExecutionPolicy
                    stored_selection["grant"] = CompanyExecutionPolicy(self.db).reserve(con, claim, stored_selection)
                if stored_selection.get("purpose") == "CONVERSATION_REPLY":
                    # Server-fixed provenance class; clients can never set this via the API.
                    stored_selection["source_class"] = "EMPLOYEE_BINDING"
                claim["execution_selection"] = stored_selection
                if stored_selection.get("work_ref"):
                    if stored_selection.get("purpose") not in {"WRITING_CHAPTER_REPLY", "CG_GRAPHIC_REPLY", "CG_CONTENT_REPLY", "MUSIC_SONG_REPLY"}:
                        raise RuntimeScopeError("Only an explicit saved business request may join this Work")
                    from .runtime import ResponsibilityRoutingRuntime
                    ResponsibilityRoutingRuntime(self._work_database(con)).begin_employee_execution(
                        stored_selection["work_ref"], execution_key=claim["attempt_id"], assignment_ref=assignment_ref)
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
                        "values (?,?,'conversation.attempt.started',?,?)",
                        (owner["tenant_id"], conversation_id, json.dumps(claim), claim["attempt_id"]))
        self.running.add(claim["attempt_id"])
        return claim, True

    async def execute(self, claim, executor):
        """Only the server-owned registered executor may produce an Employee reply."""
        attempt_id = claim["attempt_id"]
        conversation_id = claim["conversation_id"]
        status, task_id = "UNVERIFIED", None
        work_ref = (claim.get("execution_selection") or {}).get("work_ref")
        duplicate_work_task, completed_atomically = False, False
        if work_ref:
            with self.db.connect() as con:
                existing = con.execute("select task_id from tasks where tenant_id=? and work_ref=? and execution_ref=?",
                                       (TenantContext.current_tenant_id(), work_ref, attempt_id)).fetchall()
                finished = con.execute("select 1 from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='conversation.attempt.finished' and idempotency_key=?",
                    (TenantContext.current_tenant_id(), conversation_id, attempt_id + ":finished")).fetchone()
            if existing or finished:
                return  # A retained Task or settled preflight must never replay.
        launched = False
        try:
            company, employee = claim["company_id"], claim["employee_ref"]
            context = self.context(company, employee, claim["context"]["assignment_ref"])
            if context != claim["context"]:
                raise RuntimeScopeError("Assignment changed before execution")
            selection = claim.get("execution_selection")
            if selection is not None:
                if selection.get("purpose") == "CONVERSATION_REPLY":
                    self.validate_conversation_selection(selection, company_id=company,
                        runtime_employee_ref=employee, context=context, attempt_id=attempt_id)
                else:
                    if self.selection_validator is None:
                        raise RuntimeScopeError("Server execution policy is unavailable")
                    self.selection_validator(selection, attempt_id=attempt_id)
            identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=context["workspace_id"], runtime_employee_ref=employee)
            if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
                raise RuntimeScopeError("Employee execution identity must be explicitly bound")
            with self.db.connect() as con:
                bindings = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? "
                                       "and enabled=1 and capability_type='model'",
                                       (TenantContext.current_tenant_id(), identity["company_employee_ref"])).fetchall()
            if selection is not None:
                bindings = [row for row in bindings if row["id"] == selection["binding_id"]
                    and row["capability_source"] == selection["model"]["source"]
                    and row["capability_id"] == selection["model"]["model_key"]]
            if len(bindings) != 1:
                raise ValueError("Employee requires one verified effective model binding")
            binding = dict(bindings[0])
            history = (self.read_request(company, conversation_id) if selection is not None and selection.get("purpose") in {"CG_GRAPHIC_REPLY", "CG_CONTENT_REPLY", "MUSIC_SONG_REPLY"} else self.read(company, employee, conversation_id))["messages"]
            message_index = next(index for index, item in enumerate(history) if item["message_id"] == claim["message_id"])
            message = history[message_index]
            if claim.get("retry_no") and selection and selection.get("purpose") == "CONVERSATION_REPLY" and selection.get("grant", {}).get("policy_revision"):
                history = history[:message_index + 1]
            references = self.references(company, context, message["references"])
            recent = [{"sender": item["sender"], "body": (item.get("display_body") or item["body"])[:1500]}
                      for item in history if item["context"] == context or (
                          item["context"] == {"company_id": company} and not item["references"]
                          and item["sender"] == self.owner(company, conversation_id=conversation_id)["participants"][0])][-6:]
            if selection is not None and selection.get("purpose") == "CG_CONTENT_REPLY":
                from .content_growth_service import ContentGrowthService
                selected_context=ContentGrowthService(self.db).reply_context(selection)
                prompt=(f"你是{identity['employee']['name']}，岗位：{identity['employee']['role']}。不是公司助理。\n"
                    f"当前责任：{context['responsibility']}\n已授权当前对象对话：{json.dumps(recent, ensure_ascii=False)}\n本次CEO消息：{message['body']}\n"
                    f"本次已核验选段与来源：{json.dumps(selected_context,ensure_ascii=False,separators=(',',':'))}\n"
                    "只讨论这次选段或镜头；完整原脚本保留在原版本，不从旧聊天补正文。不执行媒体制作或发布，不猜测事实。")
                if selection.get("publication_package"):
                    prompt = (
                        f"你是{identity['employee']['name']}，负责内容编辑。\n"
                        f"本次要求：{message['body']}\n"
                        f"已核验内容依据：{json.dumps(selected_context, ensure_ascii=False, separators=(',', ':'))}\n"
                        '只返回一个 JSON 对象，字段严格为 title、body、tags、cover_copy、publishing_advice。'
                        'tags 是字符串数组，其余字段是非空字符串。生成完整的图文内容包。'
                        '若包含 previous_formal_package，基于该正式版本和本次要求生成下一期。'
                        '发布建议仅供人工审核，不执行发布，不编造未提供的事实。'
                    )
                if len(prompt.encode("utf-8"))>32000:
                    raise ValueError("当前责任与选段信息超出本次建议范围，输入保留，请显式缩小选择。")
            else:
                # Only current assignment or this CEO's pre-assignment, reference-free topic input.
                # Messages from other assignment contexts remain history, not execution context.
                prompt = (f"你是{identity['employee']['name']}，岗位：{identity['employee']['role']}。不是公司助理。\n"
                          f"当前责任：{context['responsibility']}\n已授权当前对话：{json.dumps(recent, ensure_ascii=False)}\n"
                          f"本次CEO消息：{message['body']}\n"
                          f"CEO所选来源（仅引用，未加载正文）：{json.dumps(references, ensure_ascii=False)}\n"
                          "只回复CEO这条消息；不执行外部写入，不猜测未提供事实。")
            def submit(database):
                task = ResultStore(database).create_task(prompt, company_id=company, workspace_id=context["workspace_id"],
                    scope_type=context["scope_type"], scope_ref=context["scope_ref"],
                    work_ref=work_ref, execution_ref=attempt_id, employee_id=identity["company_employee_ref"],
                    employee_role=identity["employee"]["role"], employee_name=identity["employee"]["name"],
                    capability_source=binding["capability_source"], capability_type="model", capability_id=binding["capability_id"])
                task_id = task["task_id"]
                EmployeeExecutionIdentity(database).record_task_assignment(company_id=company, workspace_id=context["workspace_id"],
                    assignment_ref=context["assignment_ref"], assignment_revision=context["assignment_revision"],
                    runtime_employee_ref=employee, task_ref=task_id, employee_capability_binding_ref=binding["id"])
                events = self.events if database is self.db else EvolutionEventLog(database)
                events.record(correlation_id=task_id, event_type="conversation.execution_bound", idempotency_key="conversation-task:" + task_id,
                    payload={**claim, "task_id": task_id, "company_employee_ref": identity["company_employee_ref"],
                             "binding_id": binding["id"], "capability_id": binding["capability_id"]})
                return task
            if work_ref:
                from .runtime import ResponsibilityRoutingRuntime
                with self.db.connect() as con:
                    con.execute("begin immediate")
                    prior = con.execute("select task_id from tasks where tenant_id=? and work_ref=? and execution_ref=?",
                                        (TenantContext.current_tenant_id(), work_ref, attempt_id)).fetchall()
                    if prior:
                        duplicate_work_task = True
                        return
                    self.selection_validator(selection, attempt_id=attempt_id, connection=con)
                    scoped = self._work_database(con)
                    task = submit(scoped)
                    ResponsibilityRoutingRuntime(scoped).attach_provider_task(work_ref, execution_key=attempt_id, task_ref=task["task_id"])
                    EvolutionEventLog(scoped).record(correlation_id=work_ref, event_type="team.execution_task_bound",
                        payload={"work_ref": work_ref, "execution_key": attempt_id, "task_ref": task["task_id"]},
                        idempotency_key=f"team-execution-task:{TenantContext.current_tenant_id()}:{attempt_id}")
            else:
                task = submit(self.db)
            task_id = task["task_id"]
            AIUsageService(self.db).validate_business_context(tenant_id=TenantContext.current_tenant_id(),
                employee_id=identity["company_employee_ref"], capability_type="model", capability_id=binding["capability_id"],
                task_id=task_id, capability_binding_id=binding["id"])
            launched = True
            task = await executor(task_id)
            if task.get("status") != "COMPLETED" or not str(task.get("output") or "").strip():
                status = "FAILED" if task.get("status") == "FAILED" else "UNVERIFIED"
                raise RuntimeError("Employee execution did not return a completed response")
            verified = EmployeeExecutionIdentity(self.db).verify_task_callback(company_id=company, workspace_id=context["workspace_id"],
                runtime_employee_ref=employee, task_ref=task_id, session_ref="")
            if verified["verification_status"] != "VERIFIED":
                raise RuntimeScopeError("Employee reply provenance is unverified")
            if selection is not None:
                if len(task["output"]) > 8000:
                    raise ValueError("Reply exceeds the declared limit; no clipped selected reply is published")
                with self.db.connect() as con:
                    usage = con.execute("select * from ai_usage_records where tenant_id=? and task_id=? and company_id=? "
                        "and workspace_id=? and employee_id=? and capability_binding_id=? and execution_ref=?",
                        (TenantContext.current_tenant_id(), task_id, company, context["workspace_id"], identity["company_employee_ref"],
                         binding["id"], attempt_id)).fetchall()
                if len(usage) != 1 or usage[0]["execution_status"] != "success" or usage[0]["fallback_from_model"]:
                    raise RuntimeScopeError("Selected reply requires its unique actual canonical Usage attempt")
                verified = {**verified, "source_class": selection["source_class"],
                    "usage": {key: usage[0][key] for key in ("usage_record_id", "logical_call_id", "attempt_no", "metering_status", "cost_amount", "cost_source", "price_version")},
                    "execution_selection": selection}
            reply = {"message_id": attempt_id + ":reply", "conversation_id": conversation_id,
                     "sender": {"kind": "EMPLOYEE", "ref": employee}, "timestamp": datetime.now(timezone.utc).isoformat(),
                     "body": task["output"][:8000], "references": message["references"], "context": context,
                     "idempotency_key": attempt_id, "task_ref": task_id, "provenance": verified}
            if work_ref:
                from .runtime import ResponsibilityRoutingRuntime
                with self.db.connect() as con:
                    con.execute("begin immediate")
                    self.selection_validator(selection, attempt_id=attempt_id, connection=con)
                    scoped = self._work_database(con)
                    EvolutionEventLog(scoped).record(correlation_id=conversation_id, event_type="conversation.message",
                        payload=reply, idempotency_key=reply["message_id"])
                    ResponsibilityRoutingRuntime(scoped).finish_employee_execution(work_ref,
                        execution_key=attempt_id, status="ACCEPTED", task_ref=task_id, session_ref="",
                        result_ref="task:" + task_id, result_summary="章节候选来源已验证，尚待作者明确采用。",
                        result_type="WRITING_CHAPTER_CANDIDATE", provenance=verified)
                    EvolutionEventLog(scoped).record(correlation_id=conversation_id, event_type="conversation.attempt.finished",
                        payload={**claim, "status": "COMPLETED", "task_ref": task_id, "effect_status": "SETTLED"},
                        idempotency_key=attempt_id + ":finished")
                completed_atomically = True
            else:
                self.events.record(correlation_id=conversation_id, event_type="conversation.message", payload=reply, idempotency_key=reply["message_id"])
            status = "COMPLETED"
        except Exception:
            # Failed / uncertain provider attempts never become Employee messages.
            if not launched:
                status = "FAILED"
                if task_id:
                    ResultStore(self.db).transition(task_id, "FAILED", {"error": "Employee conversation execution preflight unavailable"})
        finally:
            if not duplicate_work_task:
                effect = "UNKNOWN" if claim.get("execution_selection") and launched and status != "COMPLETED" else "SETTLED"
                if not completed_atomically:
                    if work_ref:
                        from .runtime import ResponsibilityRoutingRuntime
                        with self.db.connect() as con:
                            con.execute("begin immediate")
                            scoped = self._work_database(con)
                            work = RuntimeFoundation(scoped).get(work_ref)
                            cancelled = work["data"].get("responsibilityRouting", {}).get("status") == "CANCELLED"
                            if cancelled:
                                status = "CANCELLED"
                            else:
                                retained = None
                                if launched and task_id:
                                    retained = con.execute(
                                        "select status from tasks where tenant_id=? and company_id=? and workspace_id=? "
                                        "and work_ref=? and task_id=? and execution_ref=?",
                                        (TenantContext.current_tenant_id(), claim["company_id"], claim["context"]["workspace_id"],
                                         work_ref, task_id, attempt_id),
                                    ).fetchone()
                                if retained and retained["status"] in {"FAILED", "CANCELLED"}:
                                    status = retained["status"]
                                outcome = "UNKNOWN" if launched and status not in {"FAILED", "CANCELLED"} else status
                                ResponsibilityRoutingRuntime(scoped).finish_employee_execution(
                                    work_ref, execution_key=attempt_id, status=outcome,
                                    task_ref=task_id or "", session_ref="",
                                    result_summary=("员工执行未返回可采用结果；外发效果与费用仍待核验。" if launched
                                                    else "发送前失败，原交办保留；没有发起模型调用。"),
                                    provenance={"effect_status": effect},
                                )
                            EvolutionEventLog(scoped).record(correlation_id=conversation_id, event_type="conversation.attempt.finished",
                                payload={**claim, "status": status, "task_ref": task_id, "effect_status": effect},
                                idempotency_key=attempt_id + ":finished")
                    else:
                        self.events.record(correlation_id=conversation_id, event_type="conversation.attempt.finished",
                            payload={**claim, "status": status, "task_ref": task_id, **({"effect_status": effect} if claim.get("execution_selection") else {})},
                            idempotency_key=attempt_id + ":finished")
                if claim.get("execution_selection", {}).get("grant", {}).get("policy_revision"):
                    from .company_execution_policy import CompanyExecutionPolicy
                    CompanyExecutionPolicy(self.db).settle(claim["company_id"], attempt_id, task_id, launched=launched, status=status)
            if not duplicate_work_task:
                self.running.discard(attempt_id)

    def open(self, company_id, employee_ref=None, conversation_id=None):
        owner = self.owner(company_id, employee_ref, conversation_id)
        if conversation_id:
            return self.read(company_id, employee_ref, conversation_id)
        employee_ref = owner["owner_ref"]
        self.events.record(correlation_id=owner["conversation_id"], event_type="conversation.opened",
                           payload=owner, idempotency_key=owner["conversation_id"])
        return self.read(company_id, employee_ref)

    def append_ceo(self, company_id, employee_ref=None, *, body, request_id, assignment_ref="", references=None, conversation_id=None, display_body=None):
        """Atomic idempotent append, with immutable contemporaneous provenance.

        No provider launch occurs here. An executor must separately claim a
        persisted attempt and validate its accounting provenance before launch.
        """
        if not isinstance(body, str) or not body.strip() or len(body) > 8000:
            raise ValueError("Message must contain 1–8000 characters")
        if not isinstance(request_id, str) or not 1 <= len(request_id) <= 128:
            raise ValueError("A bounded idempotency identity is required")
        owner = self.owner(company_id, employee_ref, conversation_id)
        employee_ref = owner["owner_ref"]
        if TenantContext.current_identity().get("role", "").lower() not in {"owner", "ceo"}:
            raise RuntimeScopeError("Only the Company CEO may send this message")
        context = self.context(company_id, employee_ref, assignment_ref) if employee_ref else {"company_id": company_id}
        discussion_scope = owner.get("discussion_scope")
        if discussion_scope and (discussion_scope["workspace_id"] != context["workspace_id"]
                or discussion_scope.get("assignment_ref", context["assignment_ref"]) != context["assignment_ref"]):
            raise RuntimeScopeError("当前话题不能切换到其他工作空间。")
        if discussion_scope and discussion_scope.get("object_ref"):
            obj = self.foundation.get(discussion_scope["object_ref"])
            if obj["company_id"] != company_id or obj["workspace_id"] != context["workspace_id"]:
                raise RuntimeScopeError("原讨论对象已不属于当前范围。")
        if not employee_ref and (references or assignment_ref):
            raise RuntimeScopeError("Select an Employee/current scope before adding work references")
        selected = self.references(company_id, context, references or []) if employee_ref else []
        key = "conversation-message:" + digest([owner["conversation_id"], request_id])
        request_hash = digest([body.strip(), assignment_ref,
            [{key: item[key] for key in ("reference_id", "workspace_id", "kind")} for item in selected]])
        with self.db.connect() as con:
            con.execute("begin immediate")
            existing = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                                   (owner["tenant_id"], key)).fetchone()
            if existing:
                message = json.loads(existing["payload"])
                if message["request_hash"] != request_hash:
                    raise ValueError("Idempotency identity conflicts with the original message")
                return message
            if not employee_ref and con.execute("select 1 from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='conversation.employee_joined'", (owner["tenant_id"], owner["conversation_id"])).fetchone():
                raise RuntimeScopeError("An Employee joined; reload current context before appending")
            current = con.execute("select data_json,lifecycle_status from runtime_entities where tenant_id=? and entity_id=?",
                                  (owner["tenant_id"], assignment_ref)).fetchone()
            current_data = json.loads(current["data_json"]) if current else {}
            if employee_ref and (not current or current["lifecycle_status"] != "ACTIVE"
                    or current_data.get("employeeRef") != employee_ref
                    or current_data.get("revision") != context["assignment_revision"]):
                raise RuntimeScopeError("Assignment changed before append")
            message = {"message_id": key, "conversation_id": owner["conversation_id"],
                       "sender": owner["participants"][0], "timestamp": datetime.now(timezone.utc).isoformat(),
                       "body": body.strip(), "references": selected, "context": context,
                       "idempotency_key": request_id, "request_hash": request_hash}
            if display_body is not None:
                if not isinstance(display_body, str) or not display_body.strip() or len(display_body) > 8000:
                    raise ValueError("Selected message display text is invalid")
                message["display_body"] = display_body.strip()
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
                        "values (?,?,'conversation.message',?,?)",
                        (owner["tenant_id"], owner["conversation_id"], json.dumps(message, ensure_ascii=False), key))
        return message
