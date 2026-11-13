"""Finite Music schemas on the existing PACKAGE_DOMAIN_OBJECT primary.

All domain writes and their receipts share one SQLite transaction. Leaf versions
are insert-only; Song alone has mutable head pointers, changed by explicit CAS.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4
from ..tenant_context import TenantContext
from .foundation import RuntimeScopeError

PACKAGE_ID = "com.curis.local.music"
VERSION = "0.2.0"
LEGACY_VERSION = "0.1.0"
LEGACY_DIGEST = "5d9f36c36c2461f4540ad59277b56447a1a67cb2953759f43c52afbe5ed2cf76"
OPERATING_KINDS = {"OperatingScope", "MarketSnapshot", "ReferenceAnalysis", "Direction", "Observation", "Report", "Learning"}
KINDS = {"Song", "LyricsVersion", "ProductionVersion", "Candidate", "AudioAssetVersion", "Choice", "MasterRevision", "ReleasePackage"}


class MusicConflict(ValueError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def text(value, limit, *, empty=True):
    if not isinstance(value, str) or len(value) > limit or (not empty and not value.strip()):
        raise ValueError("文字为空或超过允许长度。")
    return value


def exact(data, fields):
    if not isinstance(data, dict) or set(data) != set(fields):
        raise ValueError("歌曲命令字段不完整或包含未知字段。")


class MusicRuntime:
    def __init__(self, database):
        self.db = database

    def get(self, con, company, workspace, ref, *, kind=None, song=None):
        row = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and entity_type='PACKAGE_DOMAIN_OBJECT'",
            (TenantContext.current_tenant_id(), company, workspace, ref)).fetchone()
        if not row:
            raise RuntimeScopeError("歌曲对象不在当前工作空间。")
        result = dict(row); data = json.loads(result.pop("data_json")); result["data"] = data
        if (data.get("packageId"), data.get("packageVersion"), data.get("schemaVersion")) not in {(PACKAGE_ID, v, v) for v in (VERSION, LEGACY_VERSION)} or data.get("kind") not in KINDS | OPERATING_KINDS:
            raise RuntimeScopeError("歌曲对象缺少有限类型依据。")
        if (kind and data["kind"] != kind) or (song and result["parent_id"] != song):
            raise RuntimeScopeError("歌曲对象类型或父级不一致。")
        payload = {k: v for k, v in data.items() if k not in ({"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256"} | ({"song_ref"} if data["kind"] not in OPERATING_KINDS else set()))}
        version = data["schemaVersion"]
        operating = data["kind"] in OPERATING_KINDS
        if data.get("objectType") != ("MusicOperatingScope" if operating else "MusicSong") or (operating and version != VERSION):
            raise RuntimeScopeError("音乐对象与明确版本不一致。")
        self.validate(data["kind"], payload, version=version)
        if data.get("payload_sha256") != digest(payload):
            raise ValueError("歌曲版本内容已改变。")
        if data["kind"] == "Song" or operating:
            if result["parent_id"] != workspace:
                raise RuntimeScopeError("歌曲父级不一致。")
        else:
            self.get(con, company, workspace, result["parent_id"], kind="Song")
            if data.get("song_ref") != result["parent_id"]:
                raise RuntimeScopeError("歌曲版本父级不一致。")
        return result

    def insert(self, con, company, workspace, kind, payload, actor, *, song=None, version=None, entity_id=None):
        operating = kind in OPERATING_KINDS
        if kind not in KINDS | OPERATING_KINDS or (kind == "Song" or operating) != (song is None):
            raise ValueError("不支持的歌曲类型。")
        if song:
            parent = self.get(con, company, workspace, song, kind="Song")
            version = parent["data"]["schemaVersion"]
        version = version or VERSION
        if version not in {VERSION, LEGACY_VERSION} or (operating and version != VERSION):
            raise ValueError("不支持写入此音乐版本。")
        self.validate(kind, payload, version=version)
        if kind == "Candidate" and payload["source"] == "AGENT_EXECUTOR":
            from ..conversation_service import ConversationService
            service = ConversationService(self.db)
            provenance = payload["provenance"]
            proof = service.agent_result_proof(company, provenance["work_ref"], provenance["task_ref"],
                artifact_ref=provenance.get("artifact_ref"), for_candidate=True)
            source = proof["source"]
            service.agent_acceptance_evidence(company, provenance["work_ref"], proof)
            if (proof["provenance"] != provenance or source["kind"] != "music"
                    or source["song_ref"] != song or source["scope"]["workspace_id"] != workspace
                    or payload["lyrics_ref"] != source["expected"]["lyrics_ref"]
                    or payload["production_ref"] != source["expected"]["production_ref"]
                    or payload["asset_ref"] or not payload["suggestion"].strip()
                    or payload["suggestion"] not in proof["text"]):
                raise RuntimeScopeError("Agent 候选必须保留原歌曲、执行与成果文字，不能自报来源。")
        if song:
            reference_kinds = {"lyrics_ref": "LyricsVersion", "production_ref": "ProductionVersion", "candidate_ref": "Candidate", "asset_ref": "AudioAssetVersion", "choice_ref": "Choice", "master_ref": "MasterRevision"}
            for field, expected_kind in reference_kinds.items():
                if payload.get(field): self.get(con, company, workspace, payload[field], kind=expected_kind, song=song)
            if payload.get("previous_ref"): self.get(con, company, workspace, payload["previous_ref"], kind=kind, song=song)
        ref = entity_id or "music-" + str(uuid4()); now = datetime.now(timezone.utc).isoformat()
        data = {**payload, "packageId": PACKAGE_ID, "packageVersion": version, "schemaVersion": version, "objectType": "MusicOperatingScope" if operating else "MusicSong", "kind": kind}
        data["payload_sha256"] = digest(payload)
        if song: data["song_ref"] = song
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,data_json,created_at,updated_at) values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,?,?,?, ?,?)",
            (ref, TenantContext.current_tenant_id(), company, workspace, song or workspace, actor, "DRAFT" if kind == "Song" else "CREATED", version, json.dumps(data, ensure_ascii=False, allow_nan=False), now, now))
        if song:
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,?)", (TenantContext.current_tenant_id(), song, "MUSIC_HAS_" + kind.upper(), ref, now))
        return ref

    def validate(self, kind, p, *, version=VERSION):
        if kind in OPERATING_KINDS:
            return self.validate_operating(kind, p)
        fields = {
            "Song": {"title", "intention", "lyrics_ref", "production_ref", "choice_ref", "master_ref"},
            "LyricsVersion": {"text", "previous_ref", "draft_revision"},
            "ProductionVersion": {"brief", "previous_ref", "draft_revision"},
            "Candidate": {"title", "suggestion", "lyrics_ref", "production_ref", "asset_ref", "source", "provenance"},
            "AudioAssetVersion": {"sha256", "size", "duration", "mime", "rights", "purpose", "source_sha256"},
            "Choice": {"candidate_ref", "asset_ref", "lyrics_ref", "production_ref", "audition", "confirmed_by"},
            "MasterRevision": {"previous_ref", "choice_ref", "candidate_ref", "asset_ref", "lyrics_ref", "production_ref", "rights", "credits", "confirmed_by", "confirmation"},
            "ReleasePackage": {"master_ref", "title", "status", "rights", "credits"},
        }
        if kind == "Song" and version == VERSION: fields[kind] |= {"direction_ref", "learning_ref"}
        exact(p, fields[kind])
        for key in ("title", "intention", "text", "brief", "suggestion", "credits"):
            if key in p: text(p[key], 20000 if key in {"text", "suggestion"} else 2000, empty=key != "title")
        for key, value in p.items():
            if key.endswith("_ref"): text(value, 256)
        if kind in {"LyricsVersion", "ProductionVersion"}: text(p["draft_revision"], 128, empty=False)
        if kind == "Candidate" and (p["source"] not in {"MANUAL_LOCAL", "CONTROLLED_EXECUTOR", "REAL_PROVIDER_TEXT", "AGENT_EXECUTOR"} or not isinstance(p["provenance"], dict)):
            raise ValueError("候选来源不合法。")
        if kind == "Candidate" and p["source"] == "AGENT_EXECUTOR":
            proof = p["provenance"]
            if (proof.get("source_class") != "AGENT_EXECUTOR" or proof.get("content_verification") != "UNVERIFIED"
                    or proof.get("verification_status") != "VERIFIED"
                    or any(not isinstance(proof.get(key), str) or not proof[key] for key in ("work_ref", "task_ref", "usage_record_id"))
                    or p["asset_ref"]):
                raise ValueError("Agent 文字候选缺少原执行依据；不能冒充音频或已核验内容。")
        if kind == "AudioAssetVersion":
            if (len(p["sha256"]) != 64 or p["source_sha256"] != p["sha256"] or type(p["size"]) is not int or not 0 < p["size"] <= 16_000_000 or type(p["duration"]) not in {int, float} or not 0 < p["duration"] <= 600 or p["mime"] != "audio/wav" or (p["rights"], p["purpose"]) not in {("LOCAL_DESIGN_ONLY", "NONCOMMERCIAL_ISOLATED_TEST"), ("LOCAL_USER_PROVIDED_UNVERIFIED", "LOCAL_USE_ONLY")}):
                raise ValueError("音频来源或本地用途不合法。")
        if kind == "Choice" and (not isinstance(p["audition"], dict) or not p["confirmed_by"]): raise ValueError("选择缺少实际试听依据。")
        if kind == "MasterRevision" and (p["confirmation"] != {"basis": True, "local_only": True} or p["rights"] not in {"LOCAL_DESIGN_ONLY", "LOCAL_USER_PROVIDED_UNVERIFIED"} or not p["confirmed_by"]): raise ValueError("Master 必须明确确认原依据与本地用途。")
        if kind == "ReleasePackage" and (p["status"] != "LOCAL_PREPARATION_NOT_PUBLISHED" or p["rights"] not in {"LOCAL_DESIGN_ONLY", "LOCAL_USER_PROVIDED_UNVERIFIED"}): raise ValueError("本地样本不能发行。")

    def head(self, con, song, changes):
        data = {**song["data"], **changes}
        payload = {k: v for k, v in data.items() if k not in {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256"}}
        self.validate("Song", payload, version=data["schemaVersion"])
        data["payload_sha256"] = digest(payload)
        con.execute("update runtime_entities set data_json=?,updated_at=? where tenant_id=? and entity_id=?", (json.dumps(data, ensure_ascii=False), datetime.now(timezone.utc).isoformat(), TenantContext.current_tenant_id(), song["entity_id"]))

    def receipt(self, con, *, scope, song, action, request_id, inputs, operation):
        text(request_id, 128, empty=False)
        key = "music-command:" + digest([scope, song, action, request_id]); fingerprint = digest(inputs)
        old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (TenantContext.current_tenant_id(), key)).fetchone()
        if old:
            payload = json.loads(old[0])
            if payload["fingerprint"] != fingerprint: raise MusicConflict("原请求不能改写内容或依据。")
            return payload["result_ref"]
        result = operation()
        con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'music.command.completed',?,?)",
            (TenantContext.current_tenant_id(), song or result, json.dumps({"action": action, "fingerprint": fingerprint, "result_ref": result, "scope": scope}, ensure_ascii=False), key))
        return result

    def validate_operating(self, kind, p):
        common = {"identity_ref", "previous_ref", "revision", "title", "body", "basis"}
        fields = {
            "OperatingScope": {"platform", "keywords", "period"},
            "MarketSnapshot": {"scope_ref", "source", "metrics"},
            "ReferenceAnalysis": {"scope_ref", "snapshot_ref", "purpose", "locator", "material_available"},
            "Direction": {"scope_ref", "reference_refs", "learning_ref", "confirmed_by", "confirmed_at"},
            "Observation": {"scope_ref", "song_ref", "master_ref", "release_ref", "platform", "account", "metric", "definition", "unit", "value", "currency", "coverage", "method", "period", "source", "verification"},
            "Report": {"scope_ref", "observation_refs", "rows", "usage", "basis_hash", "confirmed_by", "selection", "usage_basis"},
            "Learning": {"scope_ref", "report_ref", "counterexample", "applicability", "accepted_by", "validation"},
        }
        exact(p, common | fields[kind])
        text(p["identity_ref"], 256, empty=False); text(p["previous_ref"], 256)
        if type(p["revision"]) is not int or p["revision"] < 1: raise ValueError("版本不合法。")
        text(p["title"], 240, empty=False); text(p["body"], 20000)
        if not isinstance(p["basis"], dict) or len(p["basis"]) > 100: raise ValueError("原依据不合法。")
        for ref, hashed in p["basis"].items():
            text(ref, 256, empty=False)
            if not isinstance(hashed, str) or len(hashed) != 64: raise ValueError("原依据缺少内容校验。")
        for key, value in p.items():
            if key.endswith("_ref"): text(value, 256, empty=key in {"previous_ref", "learning_ref"})
        if kind == "OperatingScope":
            text(p["platform"], 120, empty=False); text(p["keywords"], 2000, empty=False); self.period(p["period"])
        if kind in {"MarketSnapshot", "Observation"}: self.source(p["source"])
        if kind == "MarketSnapshot":
            if not isinstance(p["metrics"], list) or not 1 <= len(p["metrics"]) <= 30: raise ValueError("需要有来源的观察值。")
            for metric in p["metrics"]:
                exact(metric, {"metric", "definition", "unit", "value", "account", "coverage", "method", "period", "currency"}); self.metric(metric)
        if kind == "Observation":
            self.metric(p); text(p["platform"], 120, empty=False)
            if p["verification"] != "UNVERIFIED": raise ValueError("人工观察没有联网核验。")
        if kind == "ReferenceAnalysis":
            if p["purpose"] not in {"REFERENCE", "PATTERN", "STRUCTURE", "EVIDENCE", "CONTEXT"} or type(p["material_available"]) is not bool: raise ValueError("引用用途不合法。")
            text(p["locator"], 2000, empty=False)
            if not p["material_available"] and p["purpose"] in {"REFERENCE", "STRUCTURE"}: raise ValueError("原素材缺失，不能作为音频或结构依据。")
        if kind in {"Direction", "ReferenceAnalysis", "Learning"}: text(p["body"], 20000, empty=False)
        if kind == "Direction":
            if not isinstance(p["reference_refs"], list) or not 1 <= len(p["reference_refs"]) <= 20 or len(set(p["reference_refs"])) != len(p["reference_refs"]): raise ValueError("方向需要明确的原参考。")
            for ref in p["reference_refs"]: text(ref, 256, empty=False)
            text(p["confirmed_by"], 256); text(p["confirmed_at"], 80)
        if kind == "Report":
            if p["usage_basis"] != "SONG_CUMULATIVE_CREATIVE_CALLS": raise ValueError("报告用量口径不一致。")
            if not isinstance(p["rows"], list) or not 1 <= len(p["rows"]) <= 50 or not isinstance(p["usage"], list) or not isinstance(p["selection"], dict): raise ValueError("报告需要固定原观察。")
            if p["observation_refs"] != [r["entity_id"] for r in p["rows"]] or p["basis_hash"] != digest({"rows": p["rows"], "usage": p["usage"], "selection": p["selection"]}): raise ValueError("报告原事实已改变。")
        if kind == "Learning":
            text(p["counterexample"], 2000, empty=False); text(p["applicability"], 2000, empty=False); text(p["accepted_by"], 256)
            if p["validation"] != "UNVERIFIED": raise ValueError("接受经验不等于效果已验证。")

    @staticmethod
    def period(value):
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
        exact(value, {"start", "end", "timezone"})
        try:
            start = datetime.fromisoformat(value["start"]); end = datetime.fromisoformat(value["end"])
            ZoneInfo(value["timezone"])
        except (ValueError, TypeError, KeyError, ZoneInfoNotFoundError): raise ValueError("周期或时区不合法。") from None
        if bool(start.tzinfo) != bool(end.tzinfo): raise ValueError("周期起止必须使用一致的时区格式。")
        if start >= end: raise ValueError("周期结束必须晚于开始。")
        return start, end

    @staticmethod
    def source(value):
        exact(value, {"label", "locator", "note", "captured_at"})
        for key in {"label", "locator", "note"}: text(value[key], 2000, empty=False)
        try: datetime.fromisoformat(value["captured_at"])
        except (ValueError, TypeError): raise ValueError("来源记录时间不合法。") from None

    @classmethod
    def metric(cls, value):
        import math
        for key in {"metric", "definition", "unit", "coverage", "method"}: text(value[key], 500, empty=False)
        for key in {"currency", "account"}:
            if value[key] is not None: text(value[key], 120, empty=False)
        if value["value"] is not None and (type(value["value"]) not in {int, float} or not math.isfinite(value["value"]) or value["value"] < 0): raise ValueError("未知值应留空，已知值必须是非负有限数。")
        cls.period(value["period"])
