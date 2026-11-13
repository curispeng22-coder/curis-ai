"""Task-local Writing domain over declared Package objects and append-only events.

No schema, sample import, default database, model fallback or publication command.
"""
from __future__ import annotations

import hashlib
import json
import uuid

from .conversation_service import ConversationService, digest
from .employee_execution_identity import EmployeeExecutionIdentity
from .knowledge_service import KnowledgeService
from .resource_scope_policy import ResourceScopePolicy
from .runtime import RuntimeScopeError
from .tenant_context import TenantContext

PACKAGE_ID = "com.curis.local.writing-authoring"
PACKAGE_VERSION = "0.1.0"
PACKAGE_DIGEST = "2f4c37d6b579d8db31f88f7626acec44b9f630164ba8c9909e217a5f41e2d66e"
PREFIX = "writing.chapter."
ACTIONS = frozenset(("draft.saved", "discussion.bound", "candidate.recorded", "candidate.adopted",
                     "inspection.recorded", "formal.confirmed", "package.prepared", "work.linked", "context.bound", "candidate.manual-recorded", "candidate.agent-recorded", "candidate.dialogue-recorded"))
CHECKS = ("continuity", "language", "rights")


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class WritingConflict(ValueError):
    pass


def utf16_slice(text, start, end):
    if type(start) is not int or type(end) is not int or start < 0 or end <= start:
        raise ValueError("请选择有效正文范围。")
    raw = text.encode("utf-16-le")
    if end * 2 > len(raw):
        raise ValueError("正文选择范围超出当前版本。")
    try:
        # Decode the prefix too: neither boundary may bisect a surrogate pair.
        raw[:start * 2].decode("utf-16-le")
        return raw[start * 2:end * 2].decode("utf-16-le")
    except UnicodeDecodeError as error:
        raise ValueError("正文选择边界不能拆分字符。") from error


class WritingChapterService:
    def __init__(self, database, *, conversation_service=None, allow_execution=False, entry_service=None):
        self.db = database
        self.conversations = conversation_service or ConversationService(database)
        self.allow_execution = allow_execution
        self.entry = entry_service

    def _scope(self, con, company, workspace, book=None, chapter=None, *, write=False):
        identity = TenantContext.current_identity()
        tenant = TenantContext.current_tenant_id()
        ceo = identity.get("ceo_id")
        row = con.execute("select ceo_id from companies where tenant_id=? and company_id=?", (tenant, company)).fetchone()
        if (not ceo or not row or row["ceo_id"] != ceo or
                (identity.get("company_id") and identity["company_id"] != company)):
            raise RuntimeScopeError("当前身份不能访问这家公司的作品。")
        if write and identity.get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有作者所有者可以修改章节。")
        instance = con.execute("select i.*,p.digest,p.status package_status,p.schemas_json,p.manifest_json "
            "from workspace_package_instances i join installed_workspace_packages p on p.tenant_id=i.tenant_id "
            "and p.package_id=i.package_id and p.version=i.package_version "
            "where i.tenant_id=? and i.company_id=? and i.workspace_id=?", (tenant, company, workspace)).fetchone()
        if (not instance or instance["package_id"] != PACKAGE_ID or instance["package_version"] != PACKAGE_VERSION
                or instance["package_digest"] != PACKAGE_DIGEST or instance["digest"] != PACKAGE_DIGEST):
            raise RuntimeScopeError("没有匹配本批授权的写作工作空间包。")
        schemas = json.loads(instance["schemas_json"])
        if (schemas.get("WritingBook", {}).get("schemaVersion") != "writing.book/v1" or
                schemas.get("WritingChapter", {}).get("schemaVersion") != "writing.chapter/v1"):
            raise RuntimeScopeError("写作对象声明与授权不一致。")
        if write and (instance["status"] != "ACTIVE" or instance["package_status"] != "ACTIVE"):
            raise WritingConflict("工作空间包已停用，章节仅可读取。")
        try:
            lineage = ResourceScopePolicy.resolve_execution_scope(con, tenant_id=tenant, company_id=company,
                scope_type="WORKSPACE", scope_ref=workspace)
        except ValueError as error:
            raise RuntimeScopeError(str(error)) from error
        scope = {"tenant_id": tenant, "company_id": company, "workspace_id": workspace,
                 "instance_id": instance["instance_id"], "package_id": PACKAGE_ID,
                 "package_version": PACKAGE_VERSION, "package_digest": PACKAGE_DIGEST,
                 "book_ref": book or "", "chapter_ref": chapter or ""}
        for ref, kind, version in ((book, "WritingBook", "writing.book/v1"), (chapter, "WritingChapter", "writing.chapter/v1")):
            if not ref:
                continue
            obj = con.execute("select * from workspace_package_objects where tenant_id=? and company_id=? "
                "and workspace_id=? and instance_id=? and object_id=? and object_type=? and schema_version=?",
                (tenant, company, workspace, instance["instance_id"], ref, kind, version)).fetchone()
            core = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'", (tenant, company, workspace, ref)).fetchone()
            if not obj or not core:
                raise RuntimeScopeError("作品或章节不属于当前工作空间。")
            if write and obj["lifecycle_status"] == "ARCHIVED":
                raise WritingConflict("已归档的对象不能修改。")
            data = json.loads(obj["data_json"])
            if write and data.get("status") == "ARCHIVED":
                raise WritingConflict("已归档的对象不能修改。")
            if kind == "WritingChapter" and (not book or data.get("bookRef") != book):
                raise RuntimeScopeError("章节没有匹配的真实父作品。")
        return scope, ceo, lineage, instance

    @staticmethod
    def _events(con, scope):
        rows = con.execute("select event_id,event_type,payload,created_at from evolution_events "
            "where tenant_id=? and correlation_id=? and event_type like 'writing.chapter.%' order by event_id",
            (scope["tenant_id"], scope["chapter_ref"])).fetchall()
        result = []
        for row in rows:
            payload = json.loads(row["payload"])
            if payload.get("scope") == scope:
                result.append({"event_id": row["event_id"], "action": row["event_type"][len(PREFIX):],
                               **payload["output"], "created_at": row["created_at"]})
        return result

    @staticmethod
    def _draft(events):
        draft = next((event["draft"] for event in reversed(events) if "draft" in event),
                     {"ref": "ABSENT", "text": "", "sha256": sha(""), "knowledge": []})
        basis = next((event["book_context_basis"] for event in reversed(events) if event["action"] == "context.bound"), None)
        return {**draft, **({"book_context_basis": basis} if basis else {})}

    def _knowledge(self, lineage, values):
        if (not isinstance(values, list) or len(values) > 8 or not all(isinstance(v, dict) for v in values)
                or len({v.get("ref") for v in values}) != len(values)):
            raise ValueError("最多选择八项不重复知识来源。")
        for value in values:
            if set(value) != {"ref", "sha256"}:
                raise ValueError("知识来源需要明确标识和版本摘要。")
            entry = KnowledgeService(self.db).get_entry(value["ref"])
            if not KnowledgeService._compatible(entry, lineage) or entry.get("lifecycle_status") != "ACTIVE":
                raise RuntimeScopeError("知识来源不属于当前写作范围。")
            if entry.get("content_sha256") != value["sha256"]:
                raise WritingConflict("知识来源已更新，请核对新版本。")
        return values

    def _selection(self, draft, selection, lineage):
        if set(selection) != {"draft_ref", "sha256", "start", "end", "excerpt", "anchor", "knowledge"}:
            raise ValueError("选择范围缺少版本、位置或来源。")
        if selection["draft_ref"] != draft["ref"] or selection["sha256"] != draft["sha256"]:
            raise WritingConflict("正文版本已变化，请重新选择。")
        if selection["knowledge"] != draft["knowledge"]:
            raise WritingConflict("选择范围的知识依据与正文不一致。")
        self._knowledge(lineage, selection["knowledge"])
        excerpt = utf16_slice(draft["text"], selection["start"], selection["end"])
        anchor = f'{draft["ref"]}:{selection["start"]}:{selection["end"]}'
        if excerpt != selection["excerpt"] or selection["anchor"] != anchor:
            raise WritingConflict("正文范围、引用或定位不匹配。")
        return selection

    def responsibility(self, company, workspace, *, connection=None):
        if self.entry is not None:
            with self.db.connect() as con:
                self._scope(con, company, workspace)
                assignments = self.entry.assignments(con, company, workspace)
            if len(assignments) != 1:
                return {"status": "UNAVAILABLE", "reason": "请明确唯一的章节作者。"}
            assignment = assignments[0]
            employee = assignment["data"]["employeeRef"]
            try:
                context = self.conversations.context(company, employee, assignment["entity_id"])
                identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=employee)
                policy = self.entry.execution_policy(company, workspace, connection=connection)
                return {"status": "AVAILABLE", "execution": policy, "reason": policy.get("reason", ""), "employee_ref": employee,
                        "employee_name": identity["employee"]["name"], "assignment_ref": assignment["entity_id"], "context": context}
            except (RuntimeScopeError, ValueError, KeyError) as error:
                return {"status": "UNAVAILABLE", "reason": str(error), "assignment_ref": assignment["entity_id"], "employee_ref": employee}
        with self.db.connect() as con:
            self._scope(con, company, workspace)
            rows = con.execute("select entity_id,data_json from runtime_entities where tenant_id=? "
                "and company_id=? and workspace_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT'",
                (TenantContext.current_tenant_id(), company, workspace)).fetchall()
        matches = [(r["entity_id"], json.loads(r["data_json"])) for r in rows
                   if json.loads(r["data_json"]).get("responsibilityKey") == "WRITING_CHAPTER_AUTHOR"]
        if len(matches) != 1:
            return {"status": "UNAVAILABLE", "reason": "没有唯一的章节写作责任分配。"}
        ref, data = matches[0]
        employee = data.get("employeeRef")
        try:
            context = self.conversations.context(company, employee, ref)
            if context.get("scope_type") != "WORKSPACE" or context.get("scope_ref") != workspace:
                raise RuntimeScopeError("责任范围不匹配。")
            identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company,
                workspace_id=workspace, runtime_employee_ref=employee)
            if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE" or (identity.get("bridge") or {}).get("status") != "VERIFIED":
                raise RuntimeScopeError("员工执行身份尚未验证。")
            with self.db.connect() as con:
                models = con.execute("select id from employee_capability_bindings where tenant_id=? and employee_id=? "
                    "and enabled=1 and capability_type='model'", (TenantContext.current_tenant_id(), identity["company_employee_ref"])).fetchall()
            if len(models) != 1:
                raise RuntimeScopeError("员工需要唯一已启用的模型绑定。")
        except (RuntimeScopeError, ValueError, KeyError) as error:
            return {"status": "UNAVAILABLE", "reason": str(error)}
        return {"status": "AVAILABLE" if self.allow_execution else "UNAVAILABLE", "assignment_ref": ref,
                "employee_ref": employee, "employee_name": identity["employee"]["name"], "context": context,
                "reason": "" if self.allow_execution else "本批仅验证本地写作；员工执行未启用。"}

    def collection(self, company, workspace):
        with self.db.connect() as con:
            scope, _, _, instance = self._scope(con, company, workspace)
            rows = con.execute("select object_id,object_type,data_json from workspace_package_objects "
                "where tenant_id=? and company_id=? and workspace_id=? and instance_id=? order by created_at,object_id",
                (scope["tenant_id"], company, workspace, scope["instance_id"])).fetchall()
        objects = [{"ref": r["object_id"], "type": r["object_type"], **json.loads(r["data_json"])} for r in rows]
        books = [o for o in objects if o["type"] == "WritingBook"]
        book_refs = {o["ref"] for o in books}
        return {"scope": scope, "books": books,
                "chapters": [o for o in objects if o["type"] == "WritingChapter" and o.get("bookRef") in book_refs],
                "read_only": instance["status"] != "ACTIVE" or instance["package_status"] != "ACTIVE",
                "responsibility": self.responsibility(company, workspace)}

    def _creation_source(self, con, scope):
        from .writing_operating_service import WritingOperatingService, LEARNING_KIND, SCHEMA_VERSION
        links = con.execute(
            "select target_id,company_id from runtime_links where tenant_id=? and source_id=? "
            "and relation='WRITING_CHAPTER_FROM_LEARNING'",
            (scope["tenant_id"], scope["chapter_ref"]),
        ).fetchall()
        if not links:
            return {"status": "NONE"}
        if len(links) != 1:
            return {"status": "AMBIGUOUS"}
        if links[0]["company_id"] not in (None, "", scope["company_id"]):
            return {"status": "MISSING"}
        try:
            # This existing constructor only binds references; _get uses this same read connection.
            reader = WritingOperatingService(self.db, chapter_service=self)
            record = reader._get(con, scope, links[0]["target_id"], LEARNING_KIND)
            data = record["data"]
            if (data.get("packageId") != PACKAGE_ID or data.get("packageVersion") != PACKAGE_VERSION
                    or data.get("schemaVersion") != SCHEMA_VERSION):
                return {"status": "MISSING"}
            return {"status": "AVAILABLE", "kind": "WRITING_LEARNING", "learning_ref": record["entity_id"],
                    "title": data["title"], "revision": data["revision"], "identity_ref": data["identity_ref"],
                    "payload_sha256": data["payload_sha256"], "created_at": record["created_at"],
                    "verification": "UNVERIFIED"}
        except (KeyError, ValueError, RuntimeScopeError):
            return {"status": "MISSING"}

    def chapter(self, company, workspace, book, chapter):
        if not book or not chapter:
            raise RuntimeScopeError("需要明确作品和章节标识。")
        with self.db.connect() as con:
            scope, _, _, instance = self._scope(con, company, workspace, book, chapter)
            events = self._events(con, scope)
            creation_source = self._creation_source(con, scope)
            from .writing_book_service import WritingBookService
            books = WritingBookService(self.db, chapters=self)
            basis_status = books.basis_status(con, scope, self._draft(events).get("book_context_basis"))
        context = books.read(company, workspace, book)
        return {"scope": scope, "draft": self._draft(events), "events": events, "creation_source": creation_source,
                "book_context": context, "book_context_status": basis_status,
                "read_only": instance["status"] != "ACTIVE" or instance["package_status"] != "ACTIVE",
                "responsibility": self.responsibility(company, workspace),
                "independent_review": {"status": "UNAVAILABLE", "reason": "本批仅提供作者人工检查。"},
                "business_result": {"status": "UNAVAILABLE", "reason": "尚无验证章节依据的业务结果。"}}

    def agent_work_source(self, company, workspace, assignment_ref, source):
        self._fields(source, {"kind", "book_ref", "chapter_ref", "expected_draft_ref", "selection"}
                     | ({"review_ref"} if "review_ref" in source else set()))
        assignment = self.conversations.foundation.get(assignment_ref)
        if assignment["data"].get("responsibilityKey") != "WRITING_CHAPTER_AUTHOR":
            raise RuntimeScopeError("当前责任不是章节作者。")
        with self.db.connect() as con:
            scope, _, lineage, _ = self._scope(con, company, workspace, source["book_ref"], source["chapter_ref"], write=True)
            draft = self._draft(self._events(con, scope))
            if source["expected_draft_ref"] != draft["ref"]:
                raise WritingConflict("原章节版本已变化，请重新保存并选择。")
            self._selection(draft, source["selection"], lineage)
            review = self.review_work_basis(con, scope, draft, source["review_ref"]) if "review_ref" in source else None
        knowledge = []
        for selected in source["selection"]["knowledge"]:
            item = KnowledgeService(self.db).get_entry(selected["ref"])
            if item.get("content_sha256") != selected["sha256"]:
                raise WritingConflict("知识来源已变化。")
            knowledge.append({**selected, "title": item["title"], "body": item["body"]})
        return {**({"review": review} if review else {}), "kind": "writing", "scope": scope, "selection": source["selection"],
                "draft_ref": draft["ref"], "draft_sha256": draft["sha256"], "knowledge": knowledge,
                "book_context_basis_sha256": sha(encode(draft.get("book_context_basis")))}

    def review_work_basis(self, con, scope, draft, review_ref):
        if not isinstance(review_ref, str) or not 1 <= len(review_ref) <= 128:
            raise WritingConflict("请明确选择本章当前版本的作者复盘。")
        events = self._events(con, scope)
        review = next((e for e in events if e["action"] == "inspection.recorded" and e["ref"] == review_ref), None)
        adoption = next((e for e in events if e["action"] == "candidate.adopted"
                         and e.get("draft", {}).get("ref") == draft["ref"] and e.get("work_ref")), None)
        if (not review or not adoption or review["event_id"] <= adoption["event_id"]
                or review.get("draft_ref") != draft["ref"] or review.get("draft_sha256") != draft["sha256"]
                or review.get("book_context_basis") != draft.get("book_context_basis")
                or review.get("mode") != "AUTHOR_MANUAL" or review.get("checks") != list(CHECKS)):
            raise WritingConflict("复盘必须基于本章已明确采用的 Work 当前版本。")
        work = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='WORK' and entity_id=? and lifecycle_status='COMPLETED'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], adoption["work_ref"])).fetchone()
        acceptance = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='ACCEPTANCE' and entity_id=? and parent_id=? and lifecycle_status='CLOSED'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], adoption.get("acceptance_ref"), adoption["work_ref"])).fetchone()
        if not work or not acceptance:
            raise WritingConflict("上一 Work 尚无本章已关闭的明确采用凭据。")
        data, accepted = json.loads(work["data_json"]), json.loads(acceptance["data_json"])
        if (data.get("writingBasis", {}).get("book_ref") != scope["book_ref"]
                or data.get("writingBasis", {}).get("chapter_ref") != scope["chapter_ref"]
                or adoption["acceptance_ref"] not in data.get("acceptanceRefs", [])
                or accepted.get("adoptionRef") != adoption["ref"]
                or accepted.get("resultRefs") != data.get("resultRefs") or not data.get("resultRefs")):
            raise WritingConflict("上一 Work 的采用来源已变化。")
        return {"review_ref": review_ref, "work_ref": adoption["work_ref"],
                "acceptance_ref": adoption["acceptance_ref"], "adoption_ref": adoption["ref"],
                "draft_ref": draft["ref"], "draft_sha256": draft["sha256"],
                "checks": review["checks"], "note": review["note"]}

    def materialize_agent_candidate(self, proof, reply):
        scope = proof["source"]["scope"]
        return self.command(scope["company_id"], scope["workspace_id"], scope["book_ref"], scope["chapter_ref"],
            "candidate.agent-recorded", "agent-result:" + proof["task_ref"], proof["source"]["draft_ref"],
            {"work_ref": proof["work_ref"], "task_ref": proof["task_ref"], "reply": reply})

    def command(self, company, workspace, book, chapter, action, request_id, expected_draft_ref, data):
        if not book or not chapter:
            raise RuntimeScopeError("需要明确作品和章节标识。")
        if action not in ACTIONS or not request_id or len(request_id) > 128:
            raise ValueError("无效章节动作或请求标识。")
        if len(encode(data).encode()) > 1024 * 1024:
            raise ValueError("章节事件超过1MiB限制。")
        # BEGIN IMMEDIATE protects replay, current head and append across clients/processes.
        with self.db.connect() as con:
            con.execute("begin immediate")
            scope, author, lineage, _ = self._scope(con, company, workspace, book, chapter, write=True)
            if action == "candidate.dialogue-recorded":
                self._fields(data, {"conversation_ref", "message_ref"})
                if any(not isinstance(value, str) or not value for value in data.values()):
                    raise ValueError("需要明确原对话和回复标识。")
                conversation_ref = data["conversation_ref"]
                message_ref = data["message_ref"]
                self.conversations.dialogue_result(con, company, workspace, chapter, conversation_ref, message_ref)
                request_id = "dialogue-" + digest([conversation_ref, message_ref, chapter])
            request = {"expected_draft_ref": expected_draft_ref, "data": data, "author": author}
            key = PREFIX + sha(encode([scope, action, request_id]))
            existing = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (scope["tenant_id"], key)).fetchone()
            if existing:
                payload = json.loads(existing["payload"])
                if payload.get("request") != request or payload.get("scope") != scope:
                    raise WritingConflict("同一请求标识不能提交不同内容。")
                return payload["output"]
            events = self._events(con, scope)
            draft = self._draft(events)
            if expected_draft_ref != draft["ref"]:
                raise WritingConflict("章节已被另一处更新；输入保留，请重新读取。")
            ref = "writing-" + action.replace(".", "-") + "-" + str(uuid.uuid4())
            output = self._apply(con, scope, lineage, author, events, draft, action, data, ref)
            output = {"ref": ref, **output}
            payload = {"scope": scope, "request": request, "output": output}
            serialized = encode(payload)
            if len(serialized.encode()) > 1024 * 1024:
                raise ValueError("章节事件超过1MiB限制；没有保存或截断正文。")
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
                "values (?,?,?,?,?)", (scope["tenant_id"], chapter, PREFIX + action, serialized, key))
        return output

    @staticmethod
    def _fields(data, fields):
        if not isinstance(data, dict) or set(data) != set(fields):
            raise ValueError("动作参数与声明不匹配。")

    def _apply(self, con, scope, lineage, author, events, draft, action, data, ref):
        types = {
            "draft.saved": {"text": str, "knowledge": list},
            "context.bound": {"context_ref": str, "item_ids": list, "confirmed": bool},
            "candidate.manual-recorded": {"selection": dict, "replacement": str},
            "candidate.dialogue-recorded": {"conversation_ref": str, "message_ref": str},
            "candidate.agent-recorded": {"work_ref": str, "task_ref": str, "reply": dict},
            "discussion.bound": {"selection": dict, "conversation_ref": str, "assignment_ref": str},
            "candidate.recorded": {"binding_ref": str, "message_ref": str, "reply_start": int, "reply_end": int, "reply_excerpt": str},
            "candidate.adopted": {"candidate_ref": str, "confirmed": bool},
            "inspection.recorded": {"mode": str, "checks": list, "note": str},
            "formal.confirmed": {"inspection_ref": str, "confirmed": bool},
            "package.prepared": {"formal_ref": str, "introduction": str, "credits": str, "rights_declared": bool, "target": str},
            "work.linked": {"work_ref": str, "basis_draft_ref": str, "basis_sha256": str},
        }[action]
        if set(data) != set(types) or any(type(data[k]) is not kind for k, kind in types.items()):
            raise ValueError("章节动作参数的字段或类型不匹配。")
        def find(kind, value):
            item = next((e for e in events if e["action"] == kind and e["ref"] == value), None)
            if not item:
                raise RuntimeScopeError("引用记录不属于当前章节。")
            return item

        from .writing_book_service import WritingBookService
        books = WritingBookService(self.db, chapters=self)
        basis = draft.get("book_context_basis")
        def with_basis(value):
            return {**value, **({"book_context_basis": basis} if basis else {})}
        if action == "context.bound":
            if data["confirmed"] is not True or draft["ref"] == "ABSENT":
                raise ValueError("请先保存正文，再明确选择本章依据。")
            return {"book_context_basis": books.basis(con, scope, draft, data["context_ref"], data["item_ids"]), "author": author}
        if action == "candidate.agent-recorded":
            proof = self.conversations.agent_candidate_reply_proof(
                scope["company_id"], data["work_ref"], data["task_ref"], data["reply"])
            source = proof["source"]
            if source.get("kind") != "writing" or source.get("scope") != scope or source["draft_ref"] != draft["ref"]:
                raise WritingConflict("原成果不属于当前章节版本。")
            reply = data["reply"]
            excerpt = utf16_slice(proof["text"], reply["start"], reply["end"])
            if excerpt != reply["excerpt"] or reply["text_sha256"] != proof["text_sha256"] or not excerpt.strip():
                raise WritingConflict("候选文字与原 Agent 结果不一致。")
            self._selection(draft, source["selection"], lineage)
            return {**data, "selection": source["selection"], "replacement": excerpt, "draft_ref": draft["ref"],
                    "book_context_basis": basis, "source_class": "AGENT_EXECUTOR", "provenance": proof["provenance"]}
        if action == "candidate.dialogue-recorded":
            proof = self.conversations.dialogue_result(con, scope["company_id"], scope["workspace_id"],
                scope["chapter_ref"], data["conversation_ref"], data["message_ref"])
            if len(proof["text"]) > 200000:
                raise ValueError("回复超过章节正文上限；未截断。")
            return {**data, "replacement": proof["text"], "draft_ref": draft["ref"],
                    "book_context_basis": basis, "source_class": "CONVERSATION_REPLY",
                    "task_ref": proof["task_ref"], "provenance": proof["provenance"],
                    "receiving_basis": {"draft_ref": draft["ref"], "sha256": draft["sha256"]}}
        if action == "candidate.manual-recorded":
            self._selection(draft, data["selection"], lineage)
            if not data["replacement"].strip() or len(data["replacement"]) > 200000:
                raise ValueError("请填写不超过200000字的人工候选修改。")
            return {**data, "draft_ref": draft["ref"], "basis": basis, "source_class": "CEO_MANUAL", "kind": "AUTHOR_MANUAL_PROPOSAL", "author": author}
        if action == "draft.saved":
            self._fields(data, ("text", "knowledge"))
            if not isinstance(data["text"], str) or len(data["text"]) > 200000:
                raise ValueError("正文最多200000字符；没有保存或截断。")
            data["text"].encode("utf-8")
            self._knowledge(lineage, data["knowledge"])
            return {"draft": with_basis({"ref": ref, "text": data["text"], "sha256": sha(data["text"]), "knowledge": data["knowledge"]}),
                    "author": author}
        if action == "discussion.bound":
            self._fields(data, ("selection", "conversation_ref", "assignment_ref"))
            self._selection(draft, data["selection"], lineage)
            responsibility = self.responsibility(scope["company_id"], scope["workspace_id"], connection=con)
            if responsibility["status"] != "AVAILABLE" or responsibility["assignment_ref"] != data["assignment_ref"]:
                raise WritingConflict("当前写作责任或执行不可用。")
            owner = self.conversations.owner(scope["company_id"], responsibility["employee_ref"], data["conversation_ref"])
            return {**data, "employee_ref": owner["owner_ref"], "context": responsibility["context"], "discussion_scope": owner.get("discussion_scope"),
                    "source_class": "SERVER_VALIDATED_DISCUSSION" if self.entry else "CONTROLLED_EXECUTOR", "draft_ref": draft["ref"], "book_context_basis": basis}
        if action == "candidate.recorded":
            self._fields(data, ("binding_ref", "message_ref", "reply_start", "reply_end", "reply_excerpt"))
            binding = find("discussion.bound", data["binding_ref"])
            if binding.get("book_context_basis") != basis:
                raise WritingConflict("讨论绑定的作品依据已变化，请重新选择正文并发起讨论。")
            self._selection(draft, binding["selection"], lineage)
            current = self.responsibility(scope["company_id"], scope["workspace_id"], connection=con)
            if current.get("context") != binding["context"]:
                raise WritingConflict("写作责任已变化。")
            messages = self.conversations.read(scope["company_id"], conversation_id=binding["conversation_ref"])["messages"]
            message = next((m for m in messages if m["message_id"] == data["message_ref"]), None)
            if (not message or message.get("sender") != {"kind": "EMPLOYEE", "ref": binding["employee_ref"]}
                    or message.get("context") != binding["context"] or not message.get("task_ref")
                    or message.get("provenance", {}).get("verification_status") != "VERIFIED"):
                raise RuntimeScopeError("候选修改缺少已验证员工回复来源。")
            task = con.execute("select output from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
                (scope["tenant_id"], scope["company_id"], scope["workspace_id"], message["task_ref"])).fetchone()
            if not task or task["output"] != message["body"]:
                raise WritingConflict("回复与完整执行正文不一致或已被截断，不能作为修改来源。")
            bound = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='conversation.execution_bound'", (scope["tenant_id"], message["task_ref"])).fetchall()
            if len(bound) != 1:
                raise RuntimeScopeError("回复缺少唯一执行来源。")
            claim = json.loads(bound[0]["payload"])
            if claim.get("execution_selection", {}).get("purpose") != "WRITING_CHAPTER_REPLY":
                raise RuntimeScopeError("普通讨论回复不能作为章节选段的候选修改。")
            original = next((m for m in messages if m["message_id"] == claim.get("message_id")), None)
            try:
                origin = json.loads(original["body"]) if original else {}
            except (ValueError, TypeError):
                origin = {}
            if (claim.get("conversation_id") != binding["conversation_ref"] or
                    origin.get("chapter_scope") != scope or origin.get("selection") != binding["selection"]
                    or (origin.get("book_context_basis_sha256") or "") != (sha(encode(basis)) if basis else "")):
                raise RuntimeScopeError("员工回复没有当前章节选择范围依据。")
            EmployeeExecutionIdentity(self.db).verify_task_callback(company_id=scope["company_id"],
                workspace_id=scope["workspace_id"], runtime_employee_ref=binding["employee_ref"],
                task_ref=message["task_ref"], session_ref="")
            excerpt = utf16_slice(message["body"], data["reply_start"], data["reply_end"])
            if excerpt != data["reply_excerpt"]:
                raise WritingConflict("候选修改与员工回复不一致。")
            return {**data, "selection": binding["selection"], "replacement": excerpt, "draft_ref": draft["ref"], "book_context_basis": basis,
                    "source_class": message.get("provenance", {}).get("source_class", "CONTROLLED_EXECUTOR"), "kind": "REPLY_DERIVED_PROPOSAL", "task_ref": message["task_ref"],
                    **({"work_ref": claim["execution_selection"]["work_ref"]} if claim["execution_selection"].get("work_ref") else {})}
        if action == "candidate.adopted":
            self._fields(data, ("candidate_ref", "confirmed"))
            if data["confirmed"] is not True:
                raise ValueError("需要明确确认采用修改。")
            candidate = next((e for e in events if e["action"] in {"candidate.recorded", "candidate.manual-recorded", "candidate.agent-recorded", "candidate.dialogue-recorded"} and e["ref"] == data["candidate_ref"]), None)
            if candidate is None: raise RuntimeScopeError("候选不属于当前章节。")
            if candidate["action"] == "candidate.dialogue-recorded":
                if candidate["draft_ref"] != draft["ref"] or candidate.get("book_context_basis") != basis:
                    raise WritingConflict("接收时的正文或作品依据已变化。")
                proof = self.conversations.dialogue_result(con, scope["company_id"], scope["workspace_id"],
                    scope["chapter_ref"], candidate["conversation_ref"], candidate["message_ref"])
                if proof["text"] != candidate["replacement"] or proof["provenance"] != candidate["provenance"]:
                    raise WritingConflict("原对话结果来源已变化。")
                if books.basis_status(con, scope, basis)["status"] == "STALE":
                    raise WritingConflict("作品依据已变化。")
                return {**data, "draft": with_basis({"ref": ref, "text": proof["text"],
                    "sha256": sha(proof["text"]), "knowledge": draft["knowledge"]}), "author": author}
            if candidate["action"] == "candidate.manual-recorded":
                if candidate.get("author") != author or candidate.get("basis") != basis or candidate["draft_ref"] != draft["ref"]:
                    raise WritingConflict("人工候选的正文或作品依据已变化，请重新准备。")
            elif candidate["action"] == "candidate.agent-recorded":
                if candidate.get("book_context_basis") != basis:
                    raise WritingConflict("Agent 候选的作品依据已变化。")
                self._apply(con, scope, lineage, author, events, draft, "candidate.agent-recorded",
                    {k: candidate[k] for k in ("work_ref", "task_ref", "reply")}, ref)
            else:
                if candidate.get("book_context_basis") != basis:
                    raise WritingConflict("员工候选的原作品依据已变化，请重新准备。")
                self._apply(con, scope, lineage, author, events, draft, "candidate.recorded",
                    {k: candidate[k] for k in ("binding_ref", "message_ref", "reply_start", "reply_end", "reply_excerpt")}, ref)
            if books.basis_status(con, scope, basis)["status"] == "STALE":
                raise WritingConflict("作品依据已变化，请先核对并明确重选。")
            selection = self._selection(draft, candidate["selection"], lineage)
            raw = draft["text"].encode("utf-16-le")
            text = (raw[:selection["start"] * 2] + candidate["replacement"].encode("utf-16-le") + raw[selection["end"] * 2:]).decode("utf-16-le")
            if len(text) > 200000:
                raise ValueError("采用后的正文超过200000字符。")
            outcome = {}
            if candidate.get("work_ref") and candidate["action"] == "candidate.recorded":
                outcome = self.accept_model_work(con, scope, candidate, ref, sha(text), author)
            return {**data, **outcome, "draft": with_basis({"ref": ref, "text": text, "sha256": sha(text), "knowledge": draft["knowledge"]}), "author": author}
        if action == "inspection.recorded":
            if books.basis_status(con, scope, basis)["status"] == "STALE":
                raise WritingConflict("作品依据已变化，请先核对并明确重选，再检查正文。")
            self._fields(data, ("mode", "checks", "note"))
            if data["mode"] != "AUTHOR_MANUAL" or data["checks"] != list(CHECKS) or len(data["note"]) > 2000:
                raise ValueError("请由作者完成连贯性、语言和权利三项人工检查。")
            self._knowledge(lineage, draft["knowledge"])
            if not draft["text"].strip():
                raise ValueError("请先保存非空正文。")
            return {**data, "draft_ref": draft["ref"], "draft_sha256": draft["sha256"], "author": author,
                    "knowledge": draft["knowledge"], "book_context_basis": basis, "independent_review": False}
        if action == "formal.confirmed":
            self._fields(data, ("inspection_ref", "confirmed"))
            inspection = find("inspection.recorded", data["inspection_ref"])
            if (data["confirmed"] is not True or inspection["draft_ref"] != draft["ref"]
                    or inspection["draft_sha256"] != draft["sha256"] or inspection["author"] != author
                    or inspection.get("book_context_basis") != basis or books.basis_status(con, scope, basis)["status"] == "STALE"):
                raise WritingConflict("请检查当前版本并明确确认正式稿。")
            self._knowledge(lineage, draft["knowledge"])
            return {**data, "snapshot": draft, "author": author, "status": "FORMAL_NOT_PUBLISHED"}
        if action == "package.prepared":
            self._fields(data, ("formal_ref", "introduction", "credits", "rights_declared", "target"))
            formal = find("formal.confirmed", data["formal_ref"])
            if not data["introduction"].strip() or len(data["introduction"]) > 2000:
                raise ValueError("introduction:请填写不超过2000字符的作品介绍。")
            if not data["credits"].strip() or len(data["credits"]) > 1000:
                raise ValueError("credits:请填写不超过1000字符的署名。")
            if data["rights_declared"] is not True or data["target"] != "LOCAL_DOWNLOAD":
                raise ValueError("需要作者权利声明；本批只支持本地下载。")
            package = {"schema_version": "writing.local-package/v1", "package_ref": ref, "scope": scope, "formal_ref": formal["ref"],
                       "snapshot": formal["snapshot"], "metadata": data, "author": author,
                       "external_publication": "NOT_PUBLISHED", "platform_capability": "UNVERIFIED",
                       "rights_status": "AUTHOR_DECLARED"}
            if len(encode(package).encode("utf-8")) > 2 * 1024 * 1024:
                raise ValueError("本地发布包超过Native现有2MiB边界；原正式稿保持，请减少本次导出依据后重新明确确认。")
            return {"package": package, "content_sha256": sha(encode(package)), "formal_ref": formal["ref"]}
        if action == "work.linked":
            self._fields(data, ("work_ref", "basis_draft_ref", "basis_sha256"))
            work = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? "
                "and entity_type='WORK'", (scope["tenant_id"], scope["company_id"], data["work_ref"])).fetchone()
            if not work:
                raise RuntimeScopeError("工作不可访问。")
            ResourceScopePolicy.require_same_execution_scope(lineage, ResourceScopePolicy.execution_scope_from_record(
                con, tenant_id=scope["tenant_id"], record=dict(work)))
            basis = json.loads(work["data_json"]).get("writingBasis")
            responsibility = self.responsibility(scope["company_id"], scope["workspace_id"], connection=con)
            routing = json.loads(work["data_json"]).get("responsibilityRouting") or {}
            if not responsibility.get("context") or routing.get("assignmentRef") != responsibility.get("assignment_ref"):
                raise WritingConflict("工作缺少当前写作责任依据。")
            expected = {"book_ref": scope["book_ref"], "chapter_ref": scope["chapter_ref"],
                        "draft_ref": draft["ref"], "sha256": draft["sha256"]}
            if basis != expected or data["basis_draft_ref"] != draft["ref"] or data["basis_sha256"] != draft["sha256"]:
                raise WritingConflict("工作没有已验证章节版本依据。")
            return {**data, "relation_only": True}
        raise ValueError("不支持的章节动作。")

    def download(self, company, workspace, book, chapter, package_ref):
        state = self.chapter(company, workspace, book, chapter)
        package = next((e for e in state["events"] if e["action"] == "package.prepared" and e["ref"] == package_ref), None)
        if not package:
            raise RuntimeScopeError("发布包不属于当前章节。")
        return encode(package["package"]).encode("utf-8"), package["content_sha256"]

    def discussion(self, company, workspace, book, chapter, binding_ref):
        state = self.chapter(company, workspace, book, chapter)
        binding = next((e for e in state["events"] if e["action"] == "discussion.bound" and e["ref"] == binding_ref), None)
        if not binding:
            raise RuntimeScopeError("章节讨论来源不可访问。")
        return self.conversations.read(company, conversation_id=binding["conversation_ref"])

    def bind_discussion(self, company, workspace, book, chapter, request_id, expected_draft_ref, data):
        self._fields(data, ("selection",))
        if self.entry is None and not self.allow_execution:
            raise WritingConflict("员工执行未启用；选中文章和输入已保留。")
        state = self.chapter(company, workspace, book, chapter)
        if expected_draft_ref != state["draft"]["ref"] or state["responsibility"]["status"] != "AVAILABLE":
            raise WritingConflict("章节版本或写作责任已变化。")
        with self.db.connect() as con:
            _, _, lineage, _ = self._scope(con, company, workspace, book, chapter, write=True)
        self._selection(state["draft"], data["selection"], lineage)
        topic = self.conversations.create(company, request_id="writing-topic-" + sha(encode([state["scope"], request_id])),
            title="章节选文讨论", employee_ref=state["responsibility"]["employee_ref"],
            discussion_scope={"workspace_id": workspace, "object_ref": chapter, "assignment_ref": state["responsibility"]["assignment_ref"]})
        return self.command(company, workspace, book, chapter, "discussion.bound", request_id, expected_draft_ref,
            {"selection": data["selection"], "conversation_ref": topic["conversation_id"],
             "assignment_ref": state["responsibility"]["assignment_ref"]})

    def prepare_message(self, company, workspace, book, chapter, *, binding_ref, body, request_id, model_key="", retry_no=0, work_ref=""):
        state = self.chapter(company, workspace, book, chapter)
        binding = next((e for e in state["events"] if e["action"] == "discussion.bound" and e["ref"] == binding_ref), None)
        if not binding or (self.entry is None and not self.allow_execution):
            raise WritingConflict("员工执行未启用；输入已保留。")
        with self.db.connect() as con:
            _, _, lineage, _ = self._scope(con, company, workspace, book, chapter, write=True)
        self._selection(state["draft"], binding["selection"], lineage)
        if state["responsibility"].get("context") != binding["context"]:
            raise WritingConflict("写作责任已变化。")
        if binding.get("book_context_basis") != state["draft"].get("book_context_basis"):
            raise WritingConflict("讨论绑定的作品依据已变化，请重新发起讨论。")
        basis_hash = sha(encode(binding["book_context_basis"])) if binding.get("book_context_basis") else ""
        execution_selection = None
        knowledge = []
        if self.entry is not None:
            if model_key:
                self.entry.prepare_model(company, workspace, binding["assignment_ref"], model_key)
            policy = self.entry.execution_policy(company, workspace)
            if policy["status"] != "AVAILABLE":
                raise WritingConflict(policy["reason"])
            if model_key and model_key != policy["selected"]["model"]["model_key"]:
                raise WritingConflict("模型选择已变化，输入和原请求保留。")
            for selected in binding["selection"]["knowledge"]:
                item = KnowledgeService(self.db).get_entry(selected["ref"])
                knowledge.append({**selected, "title": item["title"], "body": item["body"]})
            execution_selection = {"purpose": "WRITING_CHAPTER_REPLY", "scope": state["scope"], "selection": binding["selection"],
                "context": binding["context"], "binding_id": policy["binding"]["id"], "model": policy["selected"]["model"],
                "grant": policy["grant"], "book_context_basis_sha256": basis_hash, "source_class": policy["grant"].get("source_class", "PROVIDER_EXECUTOR")}
        if work_ref:
            if execution_selection is None:
                raise WritingConflict("Explicit Work requires a selected model")
            execution_selection["work_ref"] = work_ref
            execution_selection["work_instruction"] = body.strip()
            if retry_no:
                previous = self.conversations.read_request(company, binding["conversation_ref"], request_id)["attempts"]
                original = previous[0] if previous else {}
                if (retry_no != 1 or original.get("status") != "FAILED"
                        or original.get("effect_status") != "SETTLED" or original.get("task_ref")
                        or (original.get("execution_selection") or {}).get("work_ref") != work_ref):
                    raise WritingConflict("Only a proven pre-Task Writing failure can be retried once")
                execution_selection["retry_of_attempt"] = original["attempt_id"]
            with self.db.connect() as con:
                work = self.validate_model_work(con, execution_selection)
                cycle_ref = json.loads(work["data_json"])["cycleRef"]
                contract = json.loads(con.execute("select data_json from runtime_entities where tenant_id=? and entity_id=?",
                    (TenantContext.current_tenant_id(), cycle_ref)).fetchone()[0])["contract"]
                if contract["modelSource"].get("review"):
                    execution_selection["work_review"] = contract["modelSource"]["review"]
        compiled = encode({"author_message": body, "chapter_scope": state["scope"], "selection": binding["selection"], "book_context_basis_sha256": basis_hash,
                           **({"selected_knowledge": knowledge, "effective_model": execution_selection["model"]} if execution_selection else {}),
                           **({"writing_review": execution_selection["work_review"]} if execution_selection and execution_selection.get("work_review") else {})})
        if not body.strip() or len(compiled) > 8000:
            raise ValueError("消息连同选中文章依据超过8000字符；没有截断。")
        return self.conversations.prepare(company, binding["employee_ref"], body=compiled, display_body=body,
            request_id=request_id, assignment_ref=binding["assignment_ref"], references=[],
            conversation_id=binding["conversation_ref"], retry_no=retry_no, execution_selection=execution_selection)

    def accept_model_work(self, con, scope, candidate, adoption_ref, draft_hash, author):
        from .runtime import RuntimeFoundation
        from .runtime.child_work import CanonicalChildWorkRuntime
        task_ref, work_ref = candidate["task_ref"], candidate["work_ref"]
        task = con.execute("select * from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=? and work_ref=? "
            "and status='COMPLETED'", (scope["tenant_id"], scope["company_id"], scope["workspace_id"], task_ref, work_ref)).fetchone()
        usage = con.execute("select * from ai_usage_records where tenant_id=? and task_id=? and work_ref=? and execution_status='success'",
                            (scope["tenant_id"], task_ref, work_ref)).fetchall()
        if not task or len(usage) != 1 or usage[0]["fallback_from_model"]:
            raise WritingConflict("Original Work result or usage is not uniquely verified")
        claims = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='conversation.execution_bound'", (scope["tenant_id"], task_ref)).fetchall()
        if len(claims) != 1:
            raise WritingConflict("Original Work has no unique chapter execution")
        claim = json.loads(claims[0][0])
        self.validate_model_work(con, claim["execution_selection"], attempt_id=claim["attempt_id"])
        scoped = self.conversations._work_database(con)
        foundation = RuntimeFoundation(scoped)
        result = "task:" + task_ref
        evidence = foundation.create("EVIDENCE", company_id=scope["company_id"], workspace_id=scope["workspace_id"],
            parent_id=work_ref, owner_ref=author, verification_status="VERIFIED", evidence_condition="CURRENT",
            data={"resultRef": result, "usageRef": usage[0]["usage_record_id"], "candidateRef": candidate["ref"],
                  "adoptionRef": adoption_ref, "draftSha256": draft_hash, "contentVerification": "AUTHOR_ADOPTED"})
        acceptance = foundation.create("ACCEPTANCE", company_id=scope["company_id"], workspace_id=scope["workspace_id"],
            parent_id=work_ref, owner_ref=author, data={"resultRefs": [result], "evidenceRefs": [evidence["entity_id"]],
            "requestedBy": author, "adoptionRef": adoption_ref, "decision": "ADOPT_CHAPTER_CANDIDATE"})
        for target, actor, trigger in (("ACCEPTED", "CEO", "accept"), ("CLOSED", "SYSTEM", "close")):
            foundation.transition(acceptance["entity_id"], target, actor=actor, trigger=trigger,
                                  evidence_refs=[evidence["entity_id"]], context={"ceoId": author})
        artifacts = con.execute("select artifact_id from artifacts where tenant_id=? and task_id=?", (scope["tenant_id"], task_ref)).fetchall()
        CanonicalChildWorkRuntime(scoped).complete_work(work_ref, result_refs=[result],
            artifact_refs=[row[0] for row in artifacts], evidence_refs=[evidence["entity_id"]], acceptance_refs=[acceptance["entity_id"]])
        return {"work_ref": work_ref, "acceptance_ref": acceptance["entity_id"], "evidence_ref": evidence["entity_id"]}

    def validate_model_work(self, con, selection, *, attempt_id=None):
        work_ref = selection.get("work_ref")
        if not work_ref:
            return None
        scope = selection["scope"]
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='WORK' and entity_id=?", (scope["tenant_id"], scope["company_id"], scope["workspace_id"], work_ref)).fetchone()
        if not row or row["lifecycle_status"] != "ACTIVE":
            raise WritingConflict("Original Writing Work is unavailable or stopped")
        data = json.loads(row["data_json"])
        cycle = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                            "and entity_id=? and entity_type='CYCLE'", (scope["tenant_id"], scope["company_id"],
                            scope["workspace_id"], data.get("cycleRef"))).fetchone()
        contract = json.loads(cycle[0]).get("contract", {}) if cycle else {}
        source, binding = contract.get("modelSource", {}), contract.get("modelBinding", {})
        expected = {"book_ref": scope["book_ref"], "chapter_ref": scope["chapter_ref"],
                    "draft_ref": selection["selection"]["draft_ref"], "sha256": selection["selection"]["sha256"]}
        if source.get("review"):
            draft = self._draft(self._events(con, scope))
            current_review = self.review_work_basis(con, scope, draft, source["review"].get("review_ref"))
            if current_review != source["review"] or (attempt_id and selection.get("work_review") != current_review):
                raise WritingConflict("本次 Work 的复盘来源已变化。")
        route = data.get("responsibilityRouting", {})
        if (route.get("status") in {"CANCELLED", "COMPLETED"}
                or contract.get("problem") != selection.get("work_instruction")
                or source.get("book_context_basis_sha256") != (selection.get("book_context_basis_sha256") or sha(encode(None)))
                or source.get("scope") != scope or source.get("selection") != selection["selection"]
                or source.get("context") != selection["context"] or data.get("writingBasis") != expected
                or binding != {"bindingRef": selection["binding_id"], "model": selection["model"]}
                or route.get("currentAssignmentRef") != selection["context"]["assignment_ref"]
                or any(key != attempt_id and not self._safe_work_retry(con, selection, key, execution)
                       for key, execution in route.get("executions", {}).items())):
            raise WritingConflict("Original Work chapter, responsibility, model or execution differs")
        return dict(row)

    @staticmethod
    def _safe_work_retry(con, selection, key, execution):
        # A stopped/unknown physical call is never retried. Only an original
        # attempt that failed before Task creation may share this Work.
        if (selection.get("retry_of_attempt") != key or execution.get("status") != "FAILED"
                or execution.get("taskRef")):
            return False
        scope = selection["scope"]
        rows = con.execute("select payload from evolution_events where tenant_id=? "
            "and event_type='conversation.attempt.finished' and json_extract(payload,'$.attempt_id')=?",
            (scope["tenant_id"], key)).fetchall()
        if len(rows) != 1:
            return False
        finished = json.loads(rows[0][0])
        prior = finished.get("execution_selection") or {}
        if (finished.get("status") != "FAILED" or finished.get("effect_status") != "SETTLED"
                or finished.get("task_ref") or prior.get("work_ref") != selection["work_ref"]
                or prior.get("scope") != scope or prior.get("context") != selection["context"]
                or prior.get("binding_id") != selection["binding_id"] or prior.get("model") != selection["model"]):
            return False
        return con.execute("select 1 from tasks where tenant_id=? and execution_ref=? limit 1",
                           (scope["tenant_id"], key)).fetchone() is None

    def validate_execution_selection(self, selection, *, attempt_id=None, connection=None):
        if self.entry is None or selection.get("purpose") != "WRITING_CHAPTER_REPLY":
            raise RuntimeScopeError("No registered Writing execution policy")
        scope = selection["scope"]
        company, workspace = scope["company_id"], scope["workspace_id"]
        def validate(con):
            actual, _, lineage, _ = self._scope(con, company, workspace, scope["book_ref"], scope["chapter_ref"], write=True)
            if actual != scope:
                raise WritingConflict("原请求范围已变化。")
            self.validate_model_work(con, selection, attempt_id=attempt_id)
            current_draft = self._draft(self._events(con, scope))
            current_basis = current_draft.get("book_context_basis")
            if (selection.get("book_context_basis_sha256") or "") != (sha(encode(current_basis)) if current_basis else ""):
                raise WritingConflict("原请求的作品依据已变化。")
            self._selection(current_draft, selection["selection"], lineage)
            if any(value["attempt_id"] != attempt_id for value in self.entry.pending(con, company, workspace)):
                raise WritingConflict("原请求正在处理或结果待核验。")
            policy = self.entry.execution_policy(company, workspace, connection=con, attempt_id=attempt_id)
            if policy["status"] != "AVAILABLE":
                raise WritingConflict(policy["reason"])
            if (policy["binding"]["id"] != selection["binding_id"] or policy["selected"]["model"] != selection["model"]
                    or policy["grant"] != selection["grant"]):
                raise WritingConflict("原请求的模型或授权快照已变化。")
            context = self.conversations.context(company, policy["selected"]["employee_ref"], policy["selected"]["assignment_ref"])
            if context != selection["context"]:
                raise WritingConflict("原请求的责任依据已变化。")
        if connection is not None:
            validate(connection)
        else:
            with self.db.connect() as con:
                validate(con)
