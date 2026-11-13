"""Versioned local book knowledge; canonical Book/Chapter and package bytes stay put."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from uuid import uuid4

from .runtime import RuntimeScopeError
from .writing_chapter_service import WritingConflict, encode, sha

SCHEMA = "writing.book-context/v1"
KINDS = {"outline", "volume", "chapter", "node", "world", "character", "relationship"}
ITEM_FIELDS = {"id", "kind", "title", "body", "goal", "status", "order", "parent", "chapter_ref", "category", "role", "knowledge", "from_character", "to_character", "handoff", "character_refs", "world_refs", "direction_refs"}
COMMON_FIELDS = {"id", "kind", "title", "body", "goal", "status", "order"}
KIND_FIELDS = {
    "outline": COMMON_FIELDS | {"character_refs", "world_refs", "direction_refs"},
    "volume": COMMON_FIELDS | {"parent", "character_refs", "world_refs", "direction_refs"},
    "chapter": COMMON_FIELDS | {"parent", "chapter_ref", "handoff", "character_refs", "world_refs", "direction_refs"},
    "node": COMMON_FIELDS | {"parent", "character_refs", "world_refs", "direction_refs"},
    "world": COMMON_FIELDS | {"category"}, "character": COMMON_FIELDS | {"role", "knowledge"},
    "relationship": COMMON_FIELDS | {"from_character", "to_character"},
}
SETUP_FIELDS = {"reader", "genre", "premise", "style", "conflict"}


def empty_context():
    return {"setup": {key: "" for key in sorted(SETUP_FIELDS)}, "items": []}


class WritingBookService:
    def __init__(self, database, *, chapters):
        self.db, self.chapters = database, chapters

    def _rows(self, con, scope):
        rows = con.execute("select entity_id,data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and parent_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')='WritingBookContext' "
            "order by json_extract(data_json,'$.revision'),entity_id", (scope["tenant_id"], scope["company_id"], scope["workspace_id"], scope["book_ref"])).fetchall()
        result = []
        for row in rows:
            data = json.loads(row["data_json"])
            if data.get("scope") != scope or data.get("schemaVersion") != SCHEMA or data.get("payload_sha256") != sha(encode(data.get("context"))):
                raise WritingConflict("作品结构的来源或摘要无法核对，请保留原记录。")
            result.append({"ref": row["entity_id"], **data})
        for index, record in enumerate(result):
            if record["revision"] != index + 1 or record["previous_ref"] != (result[index - 1]["ref"] if index else ""):
                raise WritingConflict("作品结构版本链不唯一，请核对原记录。")
        return result

    def read(self, company, workspace, book, ref=""):
        with self.db.connect() as con:
            scope, _, _, instance = self.chapters._scope(con, company, workspace, book)
            rows = self._rows(con, scope)
            record = next((r for r in rows if r["ref"] == ref), None) if ref else (rows[-1] if rows else None)
            if ref and record is None:
                raise RuntimeScopeError("原作品结构版本不在本书中。")
            chapters = con.execute("select object_id,data_json from workspace_package_objects where tenant_id=? and company_id=? "
                "and workspace_id=? and instance_id=? and object_type='WritingChapter' order by created_at,object_id",
                (scope["tenant_id"], company, workspace, scope["instance_id"])).fetchall()
            chapters = [{"ref": r["object_id"], **json.loads(r["data_json"])} for r in chapters if json.loads(r["data_json"]).get("bookRef") == book]
            return {"scope": scope, "schema_version": SCHEMA, "record": record,
                "context": record["context"] if record else empty_context(), "head_ref": rows[-1]["ref"] if rows else "",
                "history": [{"ref": r["ref"], "revision": r["revision"], "sha256": r["payload_sha256"]} for r in rows],
                "chapters": chapters, "read_only": instance["status"] != "ACTIVE" or instance["package_status"] != "ACTIVE"}

    def _validate(self, con, scope, context):
        if not isinstance(context, dict) or set(context) != {"setup", "items"}:
            raise ValueError("作品结构需要明确的初始化信息和条目。")
        if not isinstance(context["setup"], dict) or set(context["setup"]) != SETUP_FIELDS:
            raise ValueError("初始化字段与作品合同不匹配。")
        if any(not isinstance(v, str) or len(v) > 2000 for v in context["setup"].values()):
            raise ValueError("初始化每项最多2000字。")
        items = context["items"]
        if not isinstance(items, list) or len(items) > 4096 or len(encode(context).encode()) > 1024 * 1024:
            raise ValueError("作品结构最多4096项且总大小不超过1MiB；请缩小本次条目。")
        by_id, chapters, refs = {}, set(), 0
        for item in items:
            if not isinstance(item, dict) or set(item) - ITEM_FIELDS or not {"id", "kind", "title", "order"} <= set(item):
                raise ValueError("作品条目的字段不匹配。")
            if not isinstance(item["kind"], str) or item["kind"] not in KINDS or not isinstance(item["id"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", item["id"]) or item["id"] in by_id:
                raise ValueError("条目需要不重复的稳定标识与合法类型。")
            if set(item) - KIND_FIELDS[item["kind"]]:
                raise ValueError("条目字段不属于这个结构类型。")
            if type(item["order"]) is not int or not 0 <= item["order"] <= 100000:
                raise ValueError("条目顺序不合法。")
            for key, value in item.items():
                if key in {"order", "character_refs", "world_refs", "direction_refs"}: continue
                if not isinstance(value, str) or len(value) > (20000 if key in {"body", "knowledge"} else 2000):
                    raise ValueError("作品条目的文字或标识超过边界。")
            if not item["title"].strip() or len(item["title"]) > 160:
                raise ValueError("请填写不超过160字的条目标题。")
            if item.get("status", "未开始") not in {"未开始", "进行中", "已完成", "已归档"}:
                raise ValueError("条目状态不合法。")
            for field in ("character_refs", "world_refs", "direction_refs"):
                values = item.get(field, [])
                if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
                    raise ValueError("条目引用需为不重复的明确标识。")
                refs += len(values)
            by_id[item["id"]] = item
        if refs > 16384:
            raise ValueError("作品结构最多16384项显式引用。")
        order_keys = set()
        for item in items:
            kind, parent = item["kind"], item.get("parent", "")
            allowed = {"outline": set(), "volume": {"outline"}, "chapter": {"outline", "volume"}, "node": {"chapter"}, "world": set(), "character": set(), "relationship": set()}[kind]
            if parent and (parent not in by_id or by_id[parent]["kind"] not in allowed):
                raise ValueError("条目的所属层级不合法。")
            if kind == "node" and not parent:
                raise ValueError("故事节点必须属于一个真实章节计划。")
            order_key = (kind, parent, item["order"])
            if order_key in order_keys: raise ValueError("同层同类型条目的顺序不能重复。")
            order_keys.add(order_key)
            visited = {item["id"]}; cursor = parent
            while cursor:
                if cursor in visited: raise ValueError("作品结构不能形成循环。")
                visited.add(cursor); cursor = by_id[cursor].get("parent", "")
            if kind == "chapter":
                chapter = item.get("chapter_ref", "")
                self.chapters._scope(con, scope["company_id"], scope["workspace_id"], scope["book_ref"], chapter, write=True)
                if not chapter or chapter in chapters: raise ValueError("章节计划必须引用本书不重复的真实章节。")
                chapters.add(chapter)
                row = con.execute("select data_json from workspace_package_objects where tenant_id=? and object_id=?", (scope["tenant_id"], chapter)).fetchone()
                legacy = json.loads(row[0])
                if legacy.get("volumeRef") and legacy["volumeRef"] != parent:
                    raise WritingConflict("原章节已有卷关联，请核对后再明确归卷。")
            for field, target_kind in (("character_refs", "character"), ("world_refs", "world")):
                if any(v not in by_id or by_id[v]["kind"] != target_kind for v in item.get(field, [])):
                    raise ValueError("人物或世界设定引用不属于本书的正确条目。")
            if kind == "relationship":
                left, right = item.get("from_character"), item.get("to_character")
                if left == right or any(v not in by_id or by_id[v]["kind"] != "character" for v in (left, right)):
                    raise ValueError("人物关系需要本书两个不同人物。")
            for ref in item.get("direction_refs", []): self._direction(con, scope, ref)
        return context

    def _direction(self, con, scope, ref):
        from .writing_operating_service import WritingOperatingService, DIRECTION_KIND
        operating = WritingOperatingService(self.db, chapter_service=self.chapters)
        record = operating._get(con, scope, ref, DIRECTION_KIND)
        data = record["data"]
        if data.get("objectType") != "WritingDirection" or not data.get("confirmed_by") or data.get("scope_ref", "") not in {"", scope["book_ref"]}:
            raise RuntimeScopeError("方向必须是本书或工作区明确确认的原版本。")
        return {"ref": ref, "sha256": sha(encode(data)), "title": data["title"], "body": data["body"], "revision": data["revision"]}

    def save(self, company, workspace, book, request_id, expected_ref, context):
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128: raise ValueError("请保留明确的保存请求。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            scope, actor, _, _ = self.chapters._scope(con, company, workspace, book, write=True)
            fingerprint = sha(encode({"expected_ref": expected_ref, "context": context}))
            key = "writing.book-context:" + sha(encode([scope, actor, request_id]))
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (scope["tenant_id"], key)).fetchone()
            if old:
                receipt = json.loads(old[0])
                if receipt["fingerprint"] != fingerprint: raise WritingConflict("原请求不能换内容。")
                return receipt["record"]
            rows = self._rows(con, scope)
            if expected_ref != (rows[-1]["ref"] if rows else ""): raise WritingConflict("作品结构已有新版本，输入保留，请核对后再保存。")
            self._validate(con, scope, context)
            ref, at = "writing-book-context-" + str(uuid4()), datetime.now(timezone.utc).isoformat()
            data = {"schemaVersion": SCHEMA, "objectType": "WritingBookContext", "scope": scope, "context": context,
                "revision": len(rows) + 1, "identity_ref": rows[0]["ref"] if rows else ref, "previous_ref": expected_ref,
                "payload_sha256": sha(encode(context)), "actor": actor, "created_at": at}
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,'ACTIVE',?,'UNVERIFIED','MISSING',?,?,?)", (ref, scope["tenant_id"], company, workspace, book, actor, SCHEMA, encode(data), at, at))
            record = {"ref": ref, **data}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (scope["tenant_id"], book, "writing.book-context.saved", encode({"fingerprint": fingerprint, "record": record}), key))
            return record

    def basis(self, con, scope, draft, context_ref, item_ids):
        book_scope = {**scope, "chapter_ref": ""}
        records = self._rows(con, book_scope)
        record = next((r for r in records if r["ref"] == context_ref), None)
        if not record or records[-1]["ref"] != context_ref: raise WritingConflict("请核对并选择当前作品结构版本。")
        if not isinstance(item_ids, list) or not item_ids or len(item_ids) > 64 or any(not isinstance(v, str) for v in item_ids) or len(set(item_ids)) != len(item_ids):
            raise ValueError("请明确选择1–64个本章依据条目。")
        by_id = {i["id"]: i for i in record["context"]["items"]}
        chosen = []
        for item_id in item_ids:
            item = by_id.get(item_id)
            if not item or item.get("status") == "已归档": raise WritingConflict("所选依据已移除或归档，请重新选择。")
            chapter_item = item if item["kind"] == "chapter" else by_id.get(item.get("parent")) if item["kind"] == "node" else None
            if chapter_item and chapter_item.get("chapter_ref") != scope["chapter_ref"]: raise RuntimeScopeError("节点或章节计划属于本书另一章。")
            chosen.append(item)
        # Resolve transitive professional context from this exact immutable revision, never latest.
        queue = list(chosen); seen = {item["id"] for item in chosen}
        while queue:
            item = queue.pop(0)
            refs = ([item["parent"]] if item.get("parent") else []) + item.get("character_refs", []) + item.get("world_refs", [])
            if item["kind"] == "relationship": refs += [item["from_character"], item["to_character"]]
            for ref in refs:
                if ref not in seen:
                    linked = by_id[ref]
                    if linked.get("status") == "已归档": raise WritingConflict("本章关联条目已归档，请调整关联后重新选择。")
                    seen.add(ref); chosen.append(linked); queue.append(linked)
        characters = {item["id"] for item in chosen if item["kind"] == "character"}
        chosen += [item for item in by_id.values() if item["kind"] == "relationship" and item.get("from_character") in characters and item.get("to_character") in characters and item["id"] not in seen and item.get("status") != "已归档"]
        directions = set(r[0] for r in con.execute("select target_id from runtime_links where tenant_id=? and source_id=? and relation='WRITING_DIRECTION_REFERENCE'", (scope["tenant_id"], scope["chapter_ref"])).fetchall())
        directions.update(ref for item in chosen for ref in item.get("direction_refs", []))
        return {"schema_version": SCHEMA, "context_ref": context_ref, "context_sha256": record["payload_sha256"],
            "book_ref": scope["book_ref"], "chapter_ref": scope["chapter_ref"], "draft_ref": draft["ref"], "draft_sha256": draft["sha256"],
            "items": chosen, "setup": record["context"]["setup"], "directions": [self._direction(con, scope, ref) for ref in sorted(directions)]}

    def basis_status(self, con, scope, basis):
        if not basis: return {"status": "ABSENT", "reason": "尚未选择作品结构依据。"}
        rows = self._rows(con, {**scope, "chapter_ref": ""})
        current = rows[-1] if rows else None
        if (basis.get("schema_version") != SCHEMA or basis.get("book_ref") != scope["book_ref"] or basis.get("chapter_ref") != scope["chapter_ref"]
                or not current or current["ref"] != basis.get("context_ref") or current["payload_sha256"] != basis.get("context_sha256")):
            return {"status": "STALE", "reason": "作品结构已有变化；原依据快照保留，请核对后明确重选。"}
        for direction in basis.get("directions", []):
            try:
                actual = self._direction(con, scope, direction["ref"])
            except (ValueError, RuntimeScopeError): return {"status": "STALE", "reason": "原方向无法核对；原快照保留。"}
            from .writing_operating_service import WritingOperatingService, DIRECTION_KIND
            operating=WritingOperatingService(self.db,chapter_service=self.chapters)
            record=operating._get(con,scope,direction["ref"],DIRECTION_KIND)
            if actual != direction or operating._latest_ref(con,scope,record,DIRECTION_KIND) != direction["ref"]:
                return {"status": "STALE", "reason": "原方向已有变化；请明确核对并重选。"}
        return {"status": "CURRENT", "reason": "本章保留明确选择的原版本依据。"}
