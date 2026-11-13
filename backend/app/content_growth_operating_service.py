"""Manual, scoped CG observations and decisions; no external collection or shared engine."""
from __future__ import annotations
import json
import math
import hashlib
from datetime import datetime, timezone
from uuid import uuid4
from .content_growth_service import ContentGrowthConflict
from .runtime import RuntimeScopeError

def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


SCHEMA = "cg.operating-context/v1"
FIELDS = {
    "Scope": {"title", "platform", "keywords", "period"},
    "Snapshot": {"title", "scope_ref", "source", "period", "value", "unit", "definition", "body"},
    "Reference": {"title", "scope_ref", "snapshot_ref", "body", "purpose", "locator"},
    "Direction": {"title", "reference_ref", "body", "confirmed"},
    "Report": {"title", "account_ref", "period", "observation_refs", "content_ref", "version_ref", "artifact_ref", "fact", "interpretation", "unknown", "next_decision", "confirmed"},
    "Context": {"title", "content_ref", "version_ref", "reference_refs", "direction_ref", "report_refs"},
}


class ContentGrowthOperatingService:
    def __init__(self, database, *, service):
        self.db, self.service = database, service

    def _rows(self, con, info, kind=None):
        scope = info["scope"]
        rows = con.execute("select entity_id,data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.schemaVersion')=? order by created_at,entity_id",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], SCHEMA)).fetchall()
        result = []
        for row in rows:
            data = json.loads(row["data_json"])
            if data.get("scope") != scope or data.get("kind") not in FIELDS or digest(data.get("payload")) != data.get("payload_sha256"):
                raise ContentGrowthConflict("人工依据的范围或摘要不一致。")
            if kind is None or data["kind"] == kind: result.append({"ref": row["entity_id"], **data})
        return result

    def _get(self, con, info, ref, kind=None):
        value = next((r for r in self._rows(con, info, kind) if r["ref"] == ref), None)
        if value is None: raise RuntimeScopeError("原人工依据不属于当前工作区。")
        return value

    def read(self, company, workspace):
        with self.db.connect() as con:
            info = self.service.entry.authoring_scope(company, workspace, connection=con)
            rows = self._rows(con, info)
            return {"entry": info, "schema_version": SCHEMA, "records": rows}

    def _content(self, con, info, content_ref, version_ref):
        scope = info["scope"]
        content = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and entity_type='CONTENT_ITEM'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], content_ref)).fetchone()
        version = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and parent_id=? and entity_type='CONTENT_VERSION'",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], version_ref, content_ref)).fetchone()
        if not content or not version: raise RuntimeScopeError("内容与原版本不属于当前工作区。")
        return dict(content), dict(version)

    def _source(self, con, info, ref, kind=None):
        value = self._get(con, info, ref, kind)
        return {"ref": value["ref"], "kind": value["kind"], "sha256": value["payload_sha256"], "revision": value["revision"], "payload": value["payload"]}

    def _validate(self, con, info, kind, data):
        if kind not in FIELDS or not isinstance(data, dict) or set(data) != FIELDS[kind]:
            raise ValueError("人工依据字段与类型不匹配。")
        if not isinstance(data["title"], str) or not data["title"].strip() or len(data["title"]) > 240:
            raise ValueError("请填写不超过240字的标题。")
        for key, value in data.items():
            if key in {"source", "value", "confirmed", "observation_refs", "reference_refs", "report_refs"}: continue
            if not isinstance(value, str) or len(value) > (20000 if key in {"body", "fact", "interpretation", "unknown", "next_decision"} else 2000):
                raise ValueError("人工依据文字超出边界。")
        for key in ("observation_refs", "reference_refs", "report_refs"):
            if key in data and (not isinstance(data[key], list) or len(data[key]) > 64 or any(not isinstance(v, str) or not v or len(v) > 256 for v in data[key]) or len(set(data[key])) != len(data[key])):
                raise ValueError("请提供最多64个不重复的明确来源。")
        sources = []
        if kind == "Scope":
            from .content_growth_service import PLATFORM_CATALOG
            if data["platform"] not in {p["platform"] for p in PLATFORM_CATALOG} or not data["keywords"].strip() or not data["period"].strip():
                raise ValueError("请选择已有平台并明确关键词和观察期间。")
        if kind == "Snapshot":
            sources.append(self._source(con, info, data["scope_ref"], "Scope"))
            source = data["source"]
            if not isinstance(source, dict) or set(source) != {"label", "locator", "note"} or any(not isinstance(v, str) or len(v) > 2000 for v in source.values()) or not source["label"].strip() or not source["locator"].strip():
                raise ValueError("请记录人工来源、原位置和核对限制。")
            value = data["value"]
            if value is not None and (type(value) not in {int, float} or not math.isfinite(value)):
                raise ValueError("原观察数值必须有限；未知请留空。")
            if not data["period"].strip() or value is not None and (not data["unit"].strip() or not data["definition"].strip()):
                raise ValueError("请保留原期间；数值需要单位和统计口径。")
        if kind == "Reference":
            sources += [self._source(con, info, data["scope_ref"], "Scope"), self._source(con, info, data["snapshot_ref"], "Snapshot")]
            if sources[1]["payload"]["scope_ref"] != data["scope_ref"]: raise ValueError("参考与原观察范围不一致。")
            if data["purpose"] not in {"PATTERN", "EVIDENCE", "CONTEXT", "REFERENCE", "STRUCTURE"} or not data["locator"].strip() or not data["body"].strip():
                raise ValueError("请明确原材料位置、用途与人工判断。")
        if kind == "Direction":
            sources.append(self._source(con, info, data["reference_ref"], "Reference"))
            if type(data["confirmed"]) is not bool or not data["body"].strip(): raise ValueError("方向需要正文与明确确认状态。")
        if kind == "Report":
            if type(data["confirmed"]) is not bool or not data["period"].strip() or not data["fact"].strip() or not data["observation_refs"]:
                raise ValueError("报告需要原观察、期间、事实与明确确认状态。")
            # Existing account/observation accessors enforce business scope, including other workspaces.
            account = self.service.account(info["scope"]["company_id"], info["scope"]["workspace_id"], data["account_ref"])
            for ref in data["observation_refs"]:
                observation = self.service.observation(info["scope"]["company_id"], info["scope"]["workspace_id"], ref)
                row = observation.get("record", observation.get("observation", observation))
                raw = row.get("data", {})
                if raw.get("scope_ref") != data["account_ref"] or raw.get("period") != data["period"]:
                    raise ValueError("报告只能固定同一账号和期间的原观察。")
                sources.append({"ref": ref, "kind": "AccountObservation", "sha256": digest(raw), "payload": raw})
            if data["content_ref"] or data["version_ref"]:
                self._content(con, info, data["content_ref"], data["version_ref"])
            if data["artifact_ref"]:
                row = con.execute("select data_json,parent_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=?",
                    (info["scope"]["tenant_id"], info["scope"]["company_id"], info["scope"]["workspace_id"], data["artifact_ref"])).fetchone()
                if not row or row["parent_id"] != data["content_ref"]: raise RuntimeScopeError("原成果不属于所选内容。")
        if kind == "Context":
            content, _ = self._content(con, info, data["content_ref"], data["version_ref"])
            if content["current_version_id"] != data["version_ref"]: raise ContentGrowthConflict("正文已更新，请核对本次原依据。")
            sources += [self._source(con, info, ref, "Reference") for ref in data["reference_refs"]]
            sources += [self._source(con, info, ref, "Report") for ref in data["report_refs"]]
            if data["direction_ref"]:
                direction = self._source(con, info, data["direction_ref"], "Direction")
                if direction["payload"]["confirmed"] is not True: raise ValueError("方向尚未明确确认。")
                sources.append(direction)
        if len(encode(data).encode()) > 128 * 1024: raise ValueError("人工依据超过128KiB。")
        return sources

    def command(self, company, workspace, kind, request_id, expected_ref, data):
        if not isinstance(kind, str) or kind not in FIELDS or not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ValueError("动作与请求标识无效。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.service.entry.authoring_scope(company, workspace, connection=con, write=True)
            scope, actor = info["scope"], info["actor"]
            fingerprint = digest({"kind": kind, "expected_ref": expected_ref, "data": data})
            key = "cg.operating-context:" + digest([scope, actor, kind, request_id])
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (scope["tenant_id"], key)).fetchone()
            if old:
                receipt = json.loads(old[0])
                if receipt["fingerprint"] != fingerprint: raise ContentGrowthConflict("原请求不能替换内容或来源。")
                return receipt["record"]
            if kind == "Context" and not expected_ref:
                existing_contexts = [r for r in self._rows(con, info, "Context") if r["payload"].get("content_ref") == data.get("content_ref") and r["payload"].get("version_ref") == data.get("version_ref")]
                if existing_contexts: raise ContentGrowthConflict("本版本已有明确依据，请核对原依据后以其版本修订。")
            previous = self._get(con, info, expected_ref, kind) if expected_ref else None
            if previous:
                if kind == "Context" and previous["payload"]["content_ref"] != data.get("content_ref"):
                    raise ContentGrowthConflict("不能将原内容的依据链改挂另一内容。")
                versions = [r for r in self._rows(con, info, kind) if r["identity_ref"] == previous["identity_ref"]]
                if any(r["revision"] > previous["revision"] for r in versions): raise ContentGrowthConflict("原依据已有新版本，请保留输入并核对。")
            sources = self._validate(con, info, kind, data)
            ref, at = "cg-operating-" + str(uuid4()), datetime.now(timezone.utc).isoformat()
            record = {"ref": ref, "schemaVersion": SCHEMA, "objectType": "CGManual" + kind, "kind": kind, "scope": scope, "payload": data,
                "payload_sha256": digest(data), "basis": sources, "revision": previous["revision"] + 1 if previous else 1,
                "identity_ref": previous["identity_ref"] if previous else ref, "previous_ref": expected_ref, "actor": actor, "created_at": at,
                "verification": "UNVERIFIED", "source": "CEO_MANUAL", "connection_status": "NOT_CONNECTED"}
            con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
                "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,'ACTIVE',?,'UNVERIFIED','MISSING',?,?,?)", (ref, scope["tenant_id"], company, workspace, data.get("content_ref") or workspace, actor, SCHEMA, encode(record), at, at))
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                (scope["tenant_id"], workspace, "cg.operating-context.saved", encode({"fingerprint": fingerprint, "record": record}), key))
            return record

    def context(self, con, info, content_ref, version_ref):
        if not version_ref: return None
        if not isinstance(content_ref, str) or not content_ref or len(content_ref)>256:
            raise ContentGrowthConflict("正文来源标识无效。")
        def version_row(ref):
            if not isinstance(ref, str) or not ref or len(ref)>256:
                raise ContentGrowthConflict("原正文版本标识无效。")
            return self._content(con, info, content_ref, ref)
        _, version = version_row(version_ref)
        def version_payload(version):
            try: value=json.loads(version["data_json"])
            except (ValueError,TypeError) as error: raise ContentGrowthConflict("原正文版本记录无效。") from error
            if not isinstance(value,dict): raise ContentGrowthConflict("原正文版本记录类型无效。")
            return value
        data = version_payload(version)
        contexts=self._rows(con,info,"Context")
        if any(r.get("objectType")!="CGManualContext" or not isinstance(r["payload"],dict) or set(r["payload"])!=FIELDS["Context"]
                or not isinstance(r["payload"].get("content_ref"),str) or not isinstance(r["payload"].get("version_ref"),str) for r in contexts):
            raise ContentGrowthConflict("原人工依据记录类型无效。")
        rows = [r for r in contexts if r["payload"]["content_ref"] == content_ref and r["payload"]["version_ref"] == version_ref]
        # An explicit binding on this version wins; inherited bindings always keep their exact ref.
        if rows: return max(rows, key=lambda r: (r["created_at"], r["revision"], r["ref"]))

        def receipt(event_type, ref):
            matches = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? and event_type=? "
                "and (not json_valid(payload) or case when json_valid(payload) then json_extract(payload,'$.version_ref')=? else 0 end)",
                (info["scope"]["tenant_id"], content_ref, event_type, ref)).fetchall()
            if len(matches) > 1: raise ContentGrowthConflict("正文依据回执不唯一。")
            if not matches: return None
            try: value = json.loads(matches[0][0])
            except (ValueError, TypeError) as error: raise ContentGrowthConflict("正文依据回执无效。") from error
            if not isinstance(value, dict) or value.get("version_ref") != ref or not isinstance(value.get("request"), dict):
                raise ContentGrowthConflict("正文依据回执无效。")
            return value

        def pin(value):
            if value is None or value == "": return ""
            if not isinstance(value, str) or len(value) > 256: raise ContentGrowthConflict("原人工依据标识无效。")
            return value

        def original(ref, basis_ref):
            record = self._get(con, info, ref, "Context")
            payload = record["payload"]
            if payload["content_ref"] != content_ref: raise RuntimeScopeError("原内容依据属于另一内容。")
            _, origin = version_row(payload["version_ref"])
            if version_payload(origin).get("kind") not in {"draft", "adopted"}:
                raise ContentGrowthConflict("原人工依据不是正文版本的明确绑定。")
            _, basis = version_row(basis_ref)
            if payload["version_ref"] != basis_ref:
                saved_basis = receipt("cg.content.saved", basis_ref)
                if (version_payload(basis).get("context_basis_ref") != ref
                        and (saved_basis or {}).get("context_ref") != ref):
                    raise ContentGrowthConflict("原人工依据与正文来源根不一致。")
            return record

        saved = receipt("cg.content.saved", version_ref)
        saved_ref = pin(saved.get("context_ref")) if saved else ""
        if saved and "context_ref" in saved and not saved_ref:
            raise ContentGrowthConflict("正文保存回执缺少明确的原人工依据。")
        version_pin = pin(data.get("context_basis_ref"))
        if saved_ref and version_pin and saved_ref != version_pin:
            raise ContentGrowthConflict("正文保存回执与原候选依据不一致。")
        if data.get("kind") == "adopted":
            _, candidate = version_row(data.get("source_candidate_ref"))
            candidate_data = version_payload(candidate)
            adopted = receipt("cg.content.adopted", version_ref)
            if (candidate_data.get("kind") != "candidate" or pin(candidate_data.get("context_basis_ref")) != version_pin
                    or data.get("basis_version_ref") != candidate_data.get("basis_version_ref") or not adopted
                    or adopted["request"].get("candidate_ref") != candidate["entity_id"]
                    or adopted["request"].get("expected_version_ref") != data.get("basis_version_ref")):
                raise ContentGrowthConflict("采用版本与原候选或依据回执不一致。")
        elif version_pin and data.get("kind") != "candidate":
            raise ContentGrowthConflict("原候选依据的版本类型无效。")
        if version_pin: return original(version_pin, data.get("basis_version_ref"))
        if saved_ref: return original(saved_ref, saved["request"].get("expected_version_ref"))
        # Legacy/no-Context saves have no such pin. Never infer one from a later binding.
        return None
