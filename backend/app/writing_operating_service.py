"""Writing operating surfaces — WR-DIRECTION + WR-LEARNING (P1-a).

Local manual fact chain only. Forced UNVERIFIED. No execution grant,
no schema change: records reuse runtime_entities PACKAGE_DOMAIN_OBJECT
(Music / CG accepted pattern). Contract: docs/03_Design/Curis_Writing_Domain_Authority.md
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from .runtime import RuntimeScopeError
from .tenant_context import TenantContext
from .writing_chapter_service import WritingConflict, PACKAGE_ID, PACKAGE_VERSION, PREFIX

DIRECTION_KIND = "WritingDirection"
LEARNING_KIND = "WritingLearning"
SNAPSHOT_KIND = "WritingMarketSnapshot"
OBSERVATION_KIND = "WritingObservation"
SCHEMA_VERSION = "writing.operating/v1"


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(encode(value).encode("utf-8")).hexdigest()


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def bounded_text(value, limit, *, label, empty=True):
    if not isinstance(value, str) or len(value.encode("utf-8")) > limit * 4:
        raise ValueError(f"{label}超过允许长度。")
    if not empty and not value.strip():
        raise ValueError(f"{label}不能为空。")
    return value


def exact(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError("动作参数与声明不匹配。")


class WritingOperatingService:
    def __init__(self, database, *, chapter_service):
        self.db = database
        self.chapters = chapter_service

    # ── scope / storage primitives ──────────────────────────────────────

    def _scope(self, con, company, workspace, *, write=False):
        scope, actor, _, instance = self.chapters._scope(con, company, workspace, write=write)
        read_only = instance["status"] != "ACTIVE" or instance["package_status"] != "ACTIVE"
        return scope, actor, instance, read_only

    def _entity_exists(self, con, scope, ref):
        return con.execute("select 1 from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], ref)).fetchone() is not None

    def _require_book(self, con, scope, book_ref):
        if not book_ref:
            raise RuntimeScopeError("请明确选择当前作品。")
        row = con.execute("select 1 from workspace_package_objects where tenant_id=? and company_id=? "
            "and workspace_id=? and instance_id=? and object_id=? and object_type='WritingBook'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], scope["instance_id"], book_ref)).fetchone()
        if not row:
            raise RuntimeScopeError("作品不在当前工作空间。")

    def _require_scope_target(self, con, scope, target_ref):
        if not target_ref:
            raise RuntimeScopeError("请明确选择观察对象（作品或章节）。")
        row = con.execute("select 1 from workspace_package_objects where tenant_id=? and company_id=? "
            "and workspace_id=? and instance_id=? and object_id=? "
            "and object_type in ('WritingBook','WritingChapter')",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], scope["instance_id"], target_ref)).fetchone()
        if not row:
            raise RuntimeScopeError("观察对象不在当前工作空间。")

    def _record_rows(self, con, scope, object_type):
        return con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
            "and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
            "order by created_at,entity_id",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], object_type)).fetchall()

    def _insert_record(self, con, scope, object_type, kind, payload, actor, entity_id):
        data = {"packageId": PACKAGE_ID, "packageVersion": PACKAGE_VERSION, "schemaVersion": SCHEMA_VERSION,
            "objectType": object_type, "kind": kind, **payload}
        data["payload_sha256"] = digest({k: v for k, v in data.items() if k not in
            {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256",
             "identity_ref", "previous_ref", "revision", "basis"}})
        at = datetime.now(timezone.utc).isoformat()
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,"
            "parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,"
            "data_json,created_at,updated_at) values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?,?,?,?,?)",
            (entity_id, scope["tenant_id"], scope["company_id"], scope["workspace_id"], scope["workspace_id"],
             actor, "ACTIVE", PACKAGE_VERSION, "UNVERIFIED", "MISSING",
             json.dumps(data, ensure_ascii=False), at, at))
        return entity_id

    def _get(self, con, scope, ref, object_type, *, seen=None):
        visited = set(seen or ())
        if ref in visited:
            raise ValueError("引用关系形成循环。")
        visited.add(ref)
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], ref)).fetchone()
        if not row:
            raise RuntimeScopeError("经营记录不在当前工作空间。")
        result = dict(row)
        data = json.loads(result.pop("data_json"))
        result["data"] = data
        if data.get("objectType") != object_type:
            raise RuntimeScopeError("记录类型不匹配。")
        payload = {k: v for k, v in data.items() if k not in
            {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256",
             "identity_ref", "previous_ref", "revision", "basis"}}
        if data.get("payload_sha256") != digest(payload):
            raise ValueError("经营记录内容已改变。")
        if data["previous_ref"]:
            previous = self._get(con, scope, data["previous_ref"], object_type, seen=visited)
            if previous["data"]["identity_ref"] != data["identity_ref"] or previous["data"]["revision"] + 1 != data["revision"]:
                raise ValueError("原版本关系不一致。")
        elif data["identity_ref"] != ref or data["revision"] != 1:
            raise ValueError("对象首次版本身份不一致。")
        return result

    def _latest_ref(self, con, scope, record, object_type):
        identity = record["data"]["identity_ref"]
        rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? "
            "and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')=? "
            "and json_extract(data_json,'$.identity_ref')=? order by json_extract(data_json,'$.revision') desc",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], object_type, identity)).fetchall()
        return rows[0][0]

    def _require_learning(self, con, scope, ref, *, historical):
        learning = self._get(con, scope, ref, LEARNING_KIND)
        if not learning["data"].get("accepted_by"):
            raise ValueError("经验的用途尚未明确接受。")
        if self._latest_ref(con, scope, learning, LEARNING_KIND) != ref and not historical:
            raise WritingConflict("所选经验属于原版本；保留原引用只读，明确核对历史用途后才可采用。")
        return learning

    def _refs(self, con, scope, values, *, label):
        if not isinstance(values, list) or len(values) > 8:
            raise ValueError(f"{label}最多选择八项。")
        if len({v for v in values}) != len(values):
            raise ValueError(f"{label}不能重复。")
        for ref in values:
            bounded_text(ref, 256, label=label)
            if not self._entity_exists(con, scope, ref):
                raise RuntimeScopeError(f"{label}不在当前工作空间。")
        return list(values)

    # ── reads ───────────────────────────────────────────────────────────

    def directions_collection(self, company, workspace):
        with self.db.connect() as con:
            scope, actor, instance, read_only = self._scope(con, company, workspace)
            records = [self._get(con, scope, r[0], DIRECTION_KIND) for r in self._record_rows(con, scope, DIRECTION_KIND)]
        return {"entry": {"scope": scope, "actor": actor, "read_only": read_only}, "records": records}

    def direction_content(self, company, workspace, ref):
        with self.db.connect() as con:
            scope, _, _, _ = self._scope(con, company, workspace)
            record = self._get(con, scope, ref, DIRECTION_KIND)
        return {"record": record, "current_ref": self._latest_ref_with_scope(company, workspace, record, DIRECTION_KIND)}

    def learnings_collection(self, company, workspace):
        with self.db.connect() as con:
            scope, actor, instance, read_only = self._scope(con, company, workspace)
            records = [self._get(con, scope, r[0], LEARNING_KIND) for r in self._record_rows(con, scope, LEARNING_KIND)]
        return {"entry": {"scope": scope, "actor": actor, "read_only": read_only}, "records": records}

    def learning_content(self, company, workspace, ref):
        with self.db.connect() as con:
            scope, _, _, _ = self._scope(con, company, workspace)
            record = self._get(con, scope, ref, LEARNING_KIND)
        return {"record": record, "current_ref": self._latest_ref_with_scope(company, workspace, record, LEARNING_KIND)}

    def snapshots_collection(self, company, workspace):
        with self.db.connect() as con:
            scope, actor, instance, read_only = self._scope(con, company, workspace)
            records = [self._get(con, scope, r[0], SNAPSHOT_KIND) for r in self._record_rows(con, scope, SNAPSHOT_KIND)]
        return {"entry": {"scope": scope, "actor": actor, "read_only": read_only}, "records": records}

    def snapshot_content(self, company, workspace, ref):
        with self.db.connect() as con:
            scope, _, _, _ = self._scope(con, company, workspace)
            record = self._get(con, scope, ref, SNAPSHOT_KIND)
        return {"record": record, "current_ref": self._latest_ref_with_scope(company, workspace, record, SNAPSHOT_KIND)}

    def observations_collection(self, company, workspace):
        with self.db.connect() as con:
            scope, actor, instance, read_only = self._scope(con, company, workspace)
            records = [self._get(con, scope, r[0], OBSERVATION_KIND) for r in self._record_rows(con, scope, OBSERVATION_KIND)]
        return {"entry": {"scope": scope, "actor": actor, "read_only": read_only}, "records": records}

    def observation_content(self, company, workspace, ref):
        with self.db.connect() as con:
            scope, _, _, _ = self._scope(con, company, workspace)
            record = self._get(con, scope, ref, OBSERVATION_KIND)
        return {"record": record, "current_ref": self._latest_ref_with_scope(company, workspace, record, OBSERVATION_KIND)}

    # ── read-only operating projection (WR-OP-01, P1-c) ──────────────────

    OVERVIEW_LATEST_LIMIT = 3

    def operating_overview(self, company, workspace):
        """Aggregate a read-only projection of existing workspace objects.

        Not a data source: creates no rows/tables, performs no writes.
        Per-block honest empty states are the frontend's job; every block is
        always present and simply empty when the workspace has no such data.
        """
        with self.db.connect() as con:
            scope, actor, instance, read_only = self._scope(con, company, workspace)
            rows = con.execute(
                "select object_id,object_type,data_json from workspace_package_objects "
                "where tenant_id=? and company_id=? and workspace_id=? and instance_id=? "
                "order by created_at,object_id",
                (scope["tenant_id"], scope["company_id"], scope["workspace_id"],
                 scope["instance_id"])).fetchall()
            objects = [{"ref": r["object_id"], "type": r["object_type"], **json.loads(r["data_json"])} for r in rows]
            books = [o for o in objects if o["type"] == "WritingBook"]
            book_refs = {o["ref"] for o in books}
            chapters = [o for o in objects if o["type"] == "WritingChapter" and o.get("bookRef") in book_refs]
            chapter_refs = [c["ref"] for c in chapters]
            drafted = set()
            if chapter_refs:
                placeholders = ",".join("?" for _ in chapter_refs)
                drows = con.execute(
                    f"select distinct correlation_id from evolution_events where tenant_id=? "
                    f"and event_type='writing.chapter.draft.saved' and correlation_id in ({placeholders})",
                    (scope["tenant_id"], *chapter_refs)).fetchall()
                drafted = {r[0] for r in drows}
            counts = {}
            for ch in chapters:
                counts[ch["bookRef"]] = counts.get(ch["bookRef"], 0) + 1
            book_titles = {b["ref"]: b.get("title", "") for b in books}
            books_view = [{"ref": b["ref"], "title": b.get("title", ""),
                           "chapter_count": counts.get(b["ref"], 0)} for b in books]
            chapters_view = [{"ref": c["ref"], "title": c.get("title", ""),
                              "book_ref": c.get("bookRef", ""), "book_title": book_titles.get(c.get("bookRef"), ""),
                              "has_draft": c["ref"] in drafted} for c in chapters]

            def all_records(kind):
                return [self._get(con, scope, r[0], kind) for r in self._record_rows(con, scope, kind)]

            def current_per_identity(records):
                latest = {}
                for rec in records:
                    identity = rec["data"]["identity_ref"]
                    old = latest.get(identity)
                    if old is None or rec["data"]["revision"] > old["data"]["revision"]:
                        latest[identity] = rec
                return list(latest.values())

            direction_records = all_records(DIRECTION_KIND)
            directions_current = [{
                "ref": rec["entity_id"], "title": rec["data"]["title"],
                "scope_ref": rec["data"]["scope_ref"], "confirmed": bool(rec["data"].get("confirmed_by")),
                "revision": rec["data"]["revision"], "created_at": rec["created_at"],
            } for rec in current_per_identity(direction_records)]

            learning_records = all_records(LEARNING_KIND)
            learnings_current = [{
                "ref": rec["entity_id"], "title": rec["data"]["title"],
                "applicability": rec["data"].get("applicability", ""),
                "accepted": bool(rec["data"].get("accepted_by")),
                "revision": rec["data"]["revision"], "created_at": rec["created_at"],
            } for rec in current_per_identity(learning_records)]

            snapshot_records = all_records(SNAPSHOT_KIND)
            observation_records = all_records(OBSERVATION_KIND)

            def latest_records(kind, records):
                rows = con.execute(
                    "select entity_id from runtime_entities where tenant_id=? and company_id=? "
                    "and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' "
                    "and json_extract(data_json,'$.objectType')=? "
                    "order by created_at desc, entity_id desc limit ?",
                    (scope["tenant_id"], scope["company_id"], scope["workspace_id"], kind,
                     self.OVERVIEW_LATEST_LIMIT)).fetchall()
                by_id = {rec["entity_id"]: rec for rec in records}
                return [by_id[r[0]] for r in rows]

            snapshots_latest = [{
                "ref": rec["entity_id"], "title": rec["data"]["title"],
                "period": rec["data"].get("period", ""), "created_at": rec["created_at"],
            } for rec in latest_records(SNAPSHOT_KIND, snapshot_records)]
            observations_latest = [{
                "ref": rec["entity_id"], "title": rec["data"]["title"],
                "scope_ref": rec["data"]["scope_ref"], "period": rec["data"].get("period", ""),
                "created_at": rec["created_at"],
            } for rec in latest_records(OBSERVATION_KIND, observation_records)]

        return {
            "entry": {"scope": scope, "actor": actor, "read_only": read_only},
            "books": books_view,
            "chapters": chapters_view,
            "directions": {"total_versions": len(direction_records), "current": directions_current},
            "learnings": {"total_versions": len(learning_records), "current": learnings_current},
            "snapshots": {"total": len(snapshot_records), "latest": snapshots_latest},
            "observations": {"total": len(observation_records), "latest": observations_latest},
        }

    def _latest_ref_with_scope(self, company, workspace, record, object_type):
        with self.db.connect() as con:
            scope, _, _, _ = self._scope(con, company, workspace)
            return self._latest_ref(con, scope, record, object_type)

    # ── writes ──────────────────────────────────────────────────────────

    def direction_command(self, company, workspace, action, *, request_id, expected_ref="", data):
        return self._command(company, workspace, action, "writing:direction:", request_id, expected_ref, data)

    def learning_command(self, company, workspace, action, *, request_id, expected_ref="", data):
        return self._command(company, workspace, action, "writing:learning:", request_id, expected_ref, data)

    def snapshot_command(self, company, workspace, action, *, request_id, expected_ref="", data):
        return self._command(company, workspace, action, "writing:snapshot:", request_id, expected_ref, data)

    def observation_command(self, company, workspace, action, *, request_id, expected_ref="", data):
        return self._command(company, workspace, action, "writing:observation:", request_id, expected_ref, data)

    def _command(self, company, workspace, action, prefix, request_id, expected_ref, data):
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("请求标识为空或超过允许长度。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            scope, actor, instance, read_only = self._scope(con, company, workspace, write=True)
            if read_only:
                raise WritingConflict("工作空间包已停用，经营记录仅可读取。")
            key = prefix + digest([scope["tenant_id"], scope["workspace_id"], action, actor, request_id])
            fingerprint = digest({"action": action, "data": data, "expected_ref": expected_ref})
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                (scope["tenant_id"], key)).fetchone()
            if old:
                replay = json.loads(old[0])
                if replay["fingerprint"] != fingerprint:
                    raise WritingConflict("原请求不能改写内容或依据。")
                return replay["result"]
            if action == "save-direction":
                result = self._save_direction(con, scope, actor, data, expected_ref)
            elif action == "apply-direction":
                result = self._apply_direction(con, scope, actor, data)
            elif action == "save-learning":
                result = self._save_learning(con, scope, actor, data, expected_ref)
            elif action == "use-learning":
                result = self._use_learning(con, scope, actor, instance, data)
            elif action == "save-snapshot":
                result = self._save_snapshot(con, scope, actor, data, expected_ref)
            elif action == "save-observation":
                result = self._save_observation(con, scope, actor, data, expected_ref)
            else:
                raise ValueError("未授权的写作经营动作。")
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
                "values (?,?,?,?,?)",
                (scope["tenant_id"], workspace, "writing.operating." + action,
                 json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False), key))
            return result

    def _version_payload(self, con, scope, expected_ref, object_type):
        if expected_ref:
            previous = self._get(con, scope, expected_ref, object_type)
            if self._latest_ref(con, scope, previous, object_type) != expected_ref:
                raise WritingConflict("原版本已有后续修改，请保留输入并核对。")
            return previous["data"]["identity_ref"], expected_ref, previous["data"]["revision"] + 1
        new_identity = None
        return new_identity, "", 1

    def _save_direction(self, con, scope, actor, data, expected_ref):
        exact(data, {"title", "body", "scope_ref", "reference_refs", "learning_ref", "confirmed"})
        bounded_text(data["title"], 2000, label="方向标题", empty=False)
        bounded_text(data["body"], 20000, label="方向正文", empty=False)
        bounded_text(data["scope_ref"], 256, label="适用范围")
        bounded_text(data["learning_ref"], 256, label="来源经验")
        if data["scope_ref"]:
            self._require_book(con, scope, data["scope_ref"])
        refs = self._refs(con, scope, data["reference_refs"], label="方向参考")
        if data["learning_ref"]:
            self._require_learning(con, scope, data["learning_ref"], historical=False)
        if type(data["confirmed"]) is not bool:
            raise ValueError("方向确认必须明确。")
        identity_ref, previous_ref, revision = self._version_payload(con, scope, expected_ref, DIRECTION_KIND)
        ref = "wr-direction-" + str(uuid4())
        value = {"title": data["title"], "body": data["body"], "scope_ref": data["scope_ref"],
            "reference_refs": refs, "learning_ref": data["learning_ref"],
            "confirmed_by": actor if data["confirmed"] else "",
            "confirmed_at": datetime.now(timezone.utc).isoformat() if data["confirmed"] else "",
            "identity_ref": identity_ref or ref, "previous_ref": previous_ref, "revision": revision}
        self._insert_record(con, scope, DIRECTION_KIND, "Direction", value, actor, ref)
        return {"record": self._get(con, scope, ref, DIRECTION_KIND), "result_ref": ref}

    def _apply_direction(self, con, scope, actor, data):
        exact(data, {"direction_ref", "book_ref", "chapter_ref", "confirmed", "historical"})
        if data["confirmed"] is not True or type(data["historical"]) is not bool:
            raise ValueError("请明确确认引用方向与原版本。")
        direction = self._get(con, scope, data["direction_ref"], DIRECTION_KIND)
        if not direction["data"].get("confirmed_by"):
            raise ValueError("方向尚未明确确认。")
        if self._latest_ref(con, scope, direction, DIRECTION_KIND) != data["direction_ref"] and not data["historical"]:
            raise WritingConflict("所选方向属于原版本；明确核对历史用途后才可采用。")
        # Validates book + chapter belong to this workspace and chapter.bookRef == book.
        self.chapters._scope(con, scope["company_id"], scope["workspace_id"], data["book_ref"], data["chapter_ref"])
        existing = con.execute("select 1 from runtime_links where tenant_id=? and source_id=? and relation=? and target_id=?",
            (scope["tenant_id"], data["chapter_ref"], "WRITING_DIRECTION_REFERENCE", data["direction_ref"])).fetchone()
        if not existing:
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                (scope["tenant_id"], data["chapter_ref"], "WRITING_DIRECTION_REFERENCE", data["direction_ref"]))
        return {"book_ref": data["book_ref"], "chapter_ref": data["chapter_ref"], "direction_ref": data["direction_ref"]}

    def _save_learning(self, con, scope, actor, data, expected_ref):
        exact(data, {"title", "body", "basis_refs", "applicability", "counterexample", "accepted"})
        bounded_text(data["title"], 2000, label="经验标题", empty=False)
        bounded_text(data["body"], 20000, label="经验正文", empty=False)
        bounded_text(data["applicability"], 2000, label="适用范围")
        bounded_text(data["counterexample"], 20000, label="反例与限制")
        if type(data["accepted"]) is not bool:
            raise ValueError("接受用途必须明确。")
        basis_refs = self._refs(con, scope, data["basis_refs"], label="原依据")
        basis = {}
        for source in basis_refs:
            row = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_id=?",
                (scope["tenant_id"], scope["company_id"], scope["workspace_id"], source)).fetchone()
            basis[source] = digest(json.loads(row["data_json"]))
        identity_ref, previous_ref, revision = self._version_payload(con, scope, expected_ref, LEARNING_KIND)
        ref = "wr-learning-" + str(uuid4())
        value = {"title": data["title"], "body": data["body"], "basis_refs": basis_refs, "basis": basis,
            "applicability": data["applicability"], "counterexample": data["counterexample"],
            "accepted_by": actor if data["accepted"] else "", "validation": "UNVERIFIED",
            "identity_ref": identity_ref or ref, "previous_ref": previous_ref, "revision": revision}
        self._insert_record(con, scope, LEARNING_KIND, "Learning", value, actor, ref)
        for source in basis_refs:
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
                (scope["tenant_id"], ref, "WRITING_LEARNING_BASIS", source))
        return {"record": self._get(con, scope, ref, LEARNING_KIND), "result_ref": ref}

    def _use_learning(self, con, scope, actor, instance, data):
        exact(data, {"learning_ref", "book_ref", "title", "confirmed", "historical"})
        if data["confirmed"] is not True or type(data["historical"]) is not bool:
            raise ValueError("请明确确认引用经验的用途与原版本。")
        bounded_text(data["title"], 160, label="新章节标题", empty=False)
        learning = self._require_learning(con, scope, data["learning_ref"], historical=data["historical"])
        self._require_book(con, scope, data["book_ref"])
        schemas = json.loads(instance["schemas_json"])
        schema = schemas.get("WritingChapter")
        if not schema or schema.get("schemaVersion") != "writing.chapter/v1":
            raise WritingConflict("写作对象声明与授权不一致。")
        at = datetime.now(timezone.utc).isoformat()
        chapter_ref = "package-object-" + str(uuid4())
        activity_ref = "package-activity-" + str(uuid4())
        chapter_data = {"title": data["title"], "status": "DRAFT", "bookRef": data["book_ref"]}
        # New WritingChapter package object + core entity (mirrors WorkspacePackageRuntime.create_object).
        con.execute("insert into workspace_package_objects values (?,?,?,?,?,?,?,?,?,?,?,?)",
            (chapter_ref, scope["instance_id"], scope["tenant_id"], scope["company_id"], scope["workspace_id"],
             "WritingChapter", schema["schemaVersion"], schema["initialState"], "",
             json.dumps(chapter_data, ensure_ascii=False), at, at))
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,"
            "owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
            "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,'UNVERIFIED','MISSING',?,?,?)",
            (chapter_ref, scope["tenant_id"], scope["company_id"], scope["workspace_id"], "",
             schema["initialState"], PACKAGE_VERSION,
             json.dumps({"packageId": PACKAGE_ID, "packageVersion": PACKAGE_VERSION,
                 "objectType": "WritingChapter", "schemaVersion": schema["schemaVersion"],
                 "businessData": chapter_data, "companyIntegration": {"status": "NOT_STARTED"}}, ensure_ascii=False),
             at, at))
        con.execute("insert into workspace_package_activities values (?,?,?,?,?,?,?,?,?)",
            (activity_ref, scope["instance_id"], scope["tenant_id"], scope["company_id"], scope["workspace_id"],
             "core.domain-object.create", chapter_ref, json.dumps({"objectType": "WritingChapter"}), at))
        # First draft of the NEW chapter carries the learning; no existing chapter/head is touched.
        d = learning["data"]
        text = (data["title"] + "\n\n原经验：" + d["body"] + "\n适用范围：" + d["applicability"]
            + "\n反例与限制：" + d["counterexample"] + "\n效果仍待验证；已固定原经验版本。")
        chapter_scope = {**scope, "book_ref": data["book_ref"], "chapter_ref": chapter_ref}
        draft_ref = "writing-draft-saved-" + str(uuid4())
        draft = {"ref": draft_ref, "text": text, "sha256": sha(text), "knowledge": []}
        payload = {"scope": chapter_scope,
            "request": {"expected_draft_ref": "ABSENT", "data": {"text": text, "knowledge": []}, "author": actor},
            "output": {"ref": draft_ref, "draft": draft, "author": actor}}
        con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) "
            "values (?,?,?,?,?)",
            (scope["tenant_id"], chapter_ref, PREFIX + "draft.saved", json.dumps(payload, ensure_ascii=False),
             "writing:chapter:from-learning:" + str(uuid4())))
        con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
            (scope["tenant_id"], chapter_ref, "WRITING_CHAPTER_FROM_LEARNING", learning["entity_id"]))
        return {"book_ref": data["book_ref"], "chapter_ref": chapter_ref, "draft": draft,
            "learning_ref": learning["entity_id"]}

    # ── P1-b: market snapshots & performance observations (point-in-time, immutable) ──

    def _save_snapshot(self, con, scope, actor, data, expected_ref):
        if expected_ref:
            raise ValueError("市场快照是时点记录，不能修订原快照；请录入新快照。")
        exact(data, {"title", "body", "period", "source_note"})
        bounded_text(data["title"], 2000, label="快照标题", empty=False)
        bounded_text(data["body"], 20000, label="快照正文", empty=False)
        bounded_text(data["period"], 200, label="观察周期")
        bounded_text(data["source_note"], 2000, label="人工来源说明", empty=False)
        ref = "wr-snapshot-" + str(uuid4())
        value = {"title": data["title"], "body": data["body"], "period": data["period"],
            "source_note": data["source_note"], "verification": "UNVERIFIED",
            "identity_ref": ref, "previous_ref": "", "revision": 1}
        self._insert_record(con, scope, SNAPSHOT_KIND, "MarketSnapshot", value, actor, ref)
        return {"record": self._get(con, scope, ref, SNAPSHOT_KIND), "result_ref": ref}

    def _save_observation(self, con, scope, actor, data, expected_ref):
        if expected_ref:
            raise ValueError("表现观察是时点记录，不能修订原观察；请录入新观察。")
        exact(data, {"title", "body", "scope_ref", "period"})
        bounded_text(data["title"], 2000, label="观察标题", empty=False)
        bounded_text(data["body"], 20000, label="观察正文", empty=False)
        bounded_text(data["period"], 200, label="观察周期")
        bounded_text(data["scope_ref"], 256, label="观察对象")
        self._require_scope_target(con, scope, data["scope_ref"])
        ref = "wr-observation-" + str(uuid4())
        value = {"title": data["title"], "body": data["body"], "scope_ref": data["scope_ref"],
            "period": data["period"], "verification": "UNVERIFIED",
            "identity_ref": ref, "previous_ref": "", "revision": 1}
        self._insert_record(con, scope, OBSERVATION_KIND, "Observation", value, actor, ref)
        con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)",
            (scope["tenant_id"], ref, "WRITING_OBSERVATION_SCOPE", data["scope_ref"]))
        return {"record": self._get(con, scope, ref, OBSERVATION_KIND), "result_ref": ref}
