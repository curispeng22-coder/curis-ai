"""Song commands and immutable media/selection basis; Shared owns execution."""
from __future__ import annotations
import json
import hashlib
import threading
from contextlib import contextmanager
import math
from .runtime import RuntimeScopeError
from .runtime.music import MusicRuntime, MusicConflict, digest, exact, text
from .music_entry_service import MusicEntryService, PURPOSE
from .music_media_service import MusicMediaService
from .conversation_service import ConversationService
from .tenant_context import TenantContext


class MusicService:
    def __init__(self, database, *, entry=None, conversations=None, media=None):
        self.db = database; self.entry = entry or MusicEntryService(database)
        self.runtime = MusicRuntime(database); self.conversations = conversations or ConversationService(database)
        self.media = media or MusicMediaService(database)
        self._import_lock = threading.Lock()
        self._active_imports = set()

    def content(self, company, workspace, song_ref, *, connection=None):
        self.entry.authoring_scope(company, workspace, connection=connection)
        def read(con):
            song = self.runtime.get(con, company, workspace, song_ref, kind="Song")
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and parent_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' order by created_at,entity_id", (TenantContext.current_tenant_id(), company, workspace, song_ref)).fetchall()
            children = [self.runtime.get(con, company, workspace, row[0], song=song_ref) for row in rows]
            def head(key, kind):
                ref = song["data"][key]
                return self.runtime.get(con, company, workspace, ref, kind=kind, song=song_ref) if ref else None
            text_results = {}
            for candidate in children:
                selection = candidate["data"].get("provenance", {}).get("execution_selection", {})
                if candidate["data"]["kind"] != "Candidate" or not selection.get("work_ref"):
                    continue
                work = con.execute("select lifecycle_status,data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and entity_type='WORK'",
                    (TenantContext.current_tenant_id(), company, workspace, selection["work_ref"])).fetchone()
                if work:
                    text_results[candidate["entity_id"]] = {"work_ref": selection["work_ref"], "status": work["lifecycle_status"],
                        "acceptance_refs": json.loads(work["data_json"]).get("acceptanceRefs", [])}
            return {"text_work_results": text_results, "song": song, "lyrics": head("lyrics_ref", "LyricsVersion"), "production": head("production_ref", "ProductionVersion"), "choice": head("choice_ref", "Choice"), "master": head("master_ref", "MasterRevision"), "versions": children,
                "candidates": [v for v in children if v["data"]["kind"] == "Candidate"], "assets": [v for v in children if v["data"]["kind"] == "AudioAssetVersion"], "releases": [v for v in children if v["data"]["kind"] == "ReleasePackage"]}
        if connection is not None: return read(connection)
        with self.db.connect() as con: return read(con)

    def pending(self, scope, *, connection=None, except_attempt=None):
        def read(con):
            starts = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.attempt.started' and json_extract(payload,'$.execution_selection.purpose')=? and json_extract(payload,'$.execution_selection.scope.company_id')=? and json_extract(payload,'$.execution_selection.scope.workspace_id')=?", (scope["tenant_id"], PURPOSE, scope["company_id"], scope["workspace_id"])).fetchall()
            pending = []
            for row in starts:
                claim = json.loads(row[0])
                if claim["attempt_id"] == except_attempt: continue
                finish = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.attempt.finished' and json_extract(payload,'$.attempt_id')=?", (scope["tenant_id"], claim["attempt_id"])).fetchone()
                result = json.loads(finish[0]) if finish else {}
                if result.get("status") not in {"FAILED", "COMPLETED"} or result.get("effect_status") == "UNKNOWN":
                    binding = con.execute("select payload from evolution_events where tenant_id=? and event_type='music.discussion.bound' and json_extract(payload,'$.conversation_id')=?", (scope["tenant_id"], claim["conversation_id"])).fetchone()
                    pending.append({**claim, "status": "UNKNOWN" if result.get("effect_status") == "UNKNOWN" else result.get("status", "RUNNING"), "binding_ref": json.loads(binding[0])["binding_ref"] if binding else ""})
            return pending
        if connection is not None: return read(connection)
        with self.db.connect() as con: return read(con)

    def collection(self, company, workspace):
        info = self.entry.authoring_scope(company, workspace)
        with self.db.connect() as con:
            rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.packageId')='com.curis.local.music' and json_extract(data_json,'$.kind')='Song' order by created_at,entity_id", (TenantContext.current_tenant_id(), company, workspace)).fetchall()
        info["model_preference"] = self.entry.models.read_current()["preference"]
        for assignment in info["assignments"]:
            assignment["models"] = self.entry.models.available_models()
        return {"songs": [self.content(company, workspace, row[0]) for row in rows], "entry": info, "pending_requests": self.pending(info["scope"]), "notice": "本地编辑与样本试听不等于音频生成、商用权利或发行。", "media_configured": self.media.root is not None, "user_media_configured": self.media.data_root is not None, "legacy_media_configured": self.media.root is not None and self.media.data_root is None}

    def basis(self, con, company, workspace, song, expected):
        exact(expected, {"lyrics_ref", "production_ref", "master_ref"})
        if any(song["data"][key] != value for key, value in expected.items()): raise MusicConflict("歌曲依据已改变，请保留原版本并重新核对。")

    def command(self, company, workspace, song_ref, action, *, request_id, expected=None, data, raw_audio=None):
        expected = expected or {}
        if action == "import-audio":
            exact(data, {"title", "sha256", "size"})
            if type(data["size"]) is not int or not isinstance(raw_audio, bytes) or len(raw_audio) != data["size"] or hashlib.sha256(raw_audio).hexdigest() != data["sha256"]:
                raise ValueError("导入字节与原文件摘要不一致。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            actor = info["actor"]
            def insert(kind, value, song=song_ref): return self.runtime.insert(con, company, workspace, kind, value, actor, song=song or None, version=info["definition"]["version"])
            def operation():
                if action == "create":
                    if song_ref or expected: raise ValueError("新歌曲不能携带旧歌曲依据。")
                    exact(data, {"title", "intention", "lyrics", "production", "draft_revision"})
                    payload = {"title": text(data["title"], 240, empty=False), "intention": text(data["intention"], 2000), "lyrics_ref": "", "production_ref": "", "choice_ref": "", "master_ref": ""}
                    if info["definition"]["version"] == "0.2.0": payload.update(direction_ref="", learning_ref="")
                    ref = insert("Song", payload)
                    lyrics = insert("LyricsVersion", {"text": data["lyrics"], "previous_ref": "", "draft_revision": data["draft_revision"]}, ref)
                    production = insert("ProductionVersion", {"brief": data["production"], "previous_ref": "", "draft_revision": data["draft_revision"]}, ref)
                    self.runtime.head(con, self.runtime.get(con, company, workspace, ref), {"lyrics_ref": lyrics, "production_ref": production}); return ref
                song = self.runtime.get(con, company, workspace, song_ref, kind="Song"); head = song["data"]
                if action in {"save-lyrics", "save-production"}:
                    field = "lyrics_ref" if action == "save-lyrics" else "production_ref"; body = "text" if field == "lyrics_ref" else "brief"
                    exact(expected, {field}); exact(data, {body, "draft_revision"})
                    if expected[field] != head[field]: raise MusicConflict("原版本已改变，未保存新的副本。")
                    version = insert("LyricsVersion" if field == "lyrics_ref" else "ProductionVersion", {body: data[body], "previous_ref": head[field], "draft_revision": data["draft_revision"]})
                    self.runtime.head(con, song, {field: version}); return version
                if action == "save-details":
                    exact(expected, {"title", "intention"}); exact(data, {"title", "intention"})
                    if any(head[k] != v for k, v in expected.items()): raise MusicConflict("歌名或意图已改变。")
                    self.runtime.head(con, song, {"title": text(data["title"], 240, empty=False), "intention": text(data["intention"], 2000)}); return song_ref
                self.basis(con, company, workspace, song, expected)
                if action == "adopt-dialogue-lyrics":
                    exact(data, {"candidate_ref", "confirmed"})
                    if data["confirmed"] is not True:
                        raise ValueError("请明确确认用此回复替换当前歌词。")
                    candidate = self.runtime.get(con, company, workspace, data["candidate_ref"], kind="Candidate", song=song_ref)
                    value = candidate["data"]; provenance = value["provenance"]
                    source = provenance.get("dialogue_source") or {}
                    if value["asset_ref"] or provenance.get("receiving_basis") != expected:
                        raise MusicConflict("文字候选的接收版本已变化。")
                    proof = self.conversations.dialogue_result(con, company, workspace, song_ref,
                        source.get("conversation_ref"), source.get("message_ref"))
                    if proof["text"] != value["suggestion"] or any(provenance.get(k) != v for k, v in proof["provenance"].items()):
                        raise MusicConflict("原对话文字与来源不一致。")
                    version = insert("LyricsVersion", {"text": value["suggestion"], "previous_ref": head["lyrics_ref"],
                        "draft_revision": "dialogue-" + digest(data["candidate_ref"])})
                    self.runtime.head(con, song, {"lyrics_ref": version})
                    return version
                if action == "accept-text-result":
                    exact(data, {"candidate_ref", "confirmed"})
                    if data["confirmed"] is not True:
                        raise ValueError("请明确接受这次文字工作结果。")
                    candidate = self.runtime.get(con, company, workspace, data["candidate_ref"], kind="Candidate", song=song_ref)
                    value = candidate["data"]
                    if value.get("asset_ref") or not value.get("provenance", {}).get("execution_selection", {}).get("work_ref"):
                        raise RuntimeScopeError("此候选不是已关联正式 Work 的文字结果。")
                    if (value["lyrics_ref"], value["production_ref"]) != (head["lyrics_ref"], head["production_ref"]):
                        raise MusicConflict("原文字结果的歌曲版本已改变。")
                    usage = con.execute("select task_id from ai_usage_records where tenant_id=? and company_id=? and workspace_id=? and usage_record_id=?",
                        (TenantContext.current_tenant_id(), company, workspace, value["provenance"].get("usage", {}).get("usage_record_id"))).fetchone()
                    if not usage:
                        raise RuntimeScopeError("文字候选缺少原实际用量。")
                    return self.conversations.accept_model_work(con, provenance=value["provenance"], task_ref=usage[0],
                        candidate_ref=candidate["entity_id"], text=value["suggestion"], decision_ref=request_id, actor=actor)
                if action == "import-audio":
                    exact(data, {"title", "sha256", "size"})
                    text(data["title"], 240, empty=False)
                    if not isinstance(raw_audio, bytes) or len(raw_audio) != data["size"] or hashlib.sha256(raw_audio).hexdigest() != data["sha256"]:
                        raise ValueError("导入字节与原文件摘要不一致。")
                    meta = self.media.stage_user(raw_audio)
                    asset = insert("AudioAssetVersion", meta)
                    return insert("Candidate", {"title": data["title"], "suggestion": "", "lyrics_ref": head["lyrics_ref"], "production_ref": head["production_ref"], "asset_ref": asset, "source": "MANUAL_LOCAL", "provenance": {"rights": meta["rights"], "purpose": meta["purpose"], "source": "USER_SELECTED_LOCAL_FILE", "lyrics_vocal_match": "NOT_VERIFIED"}})
                if action == "local-sample":
                    exact(data, {"sample", "title"})
                    asset = insert("AudioAssetVersion", self.media.stage_sample(data["sample"]))
                    return insert("Candidate", {"title": data["title"], "suggestion": "", "lyrics_ref": head["lyrics_ref"], "production_ref": head["production_ref"], "asset_ref": asset, "source": "MANUAL_LOCAL", "provenance": {"rights": "LOCAL_DESIGN_ONLY", "lyrics_vocal_match": "NOT_VERIFIED"}})
                if action == "candidate":
                    exact(data, {"title", "suggestion"})
                    return insert("Candidate", {**data, "lyrics_ref": head["lyrics_ref"], "production_ref": head["production_ref"], "asset_ref": "", "source": "MANUAL_LOCAL", "provenance": {}})
                if action == "choose":
                    exact(data, {"candidate_ref", "audition"})
                    candidate = self.runtime.get(con, company, workspace, data["candidate_ref"], kind="Candidate", song=song_ref)["data"]
                    if any(candidate[k] != head[k] for k in {"lyrics_ref", "production_ref"}): raise MusicConflict("候选依据已过期，不能替换为当前版本。")
                    asset = self.media.verify(con, company, workspace, song_ref, candidate["asset_ref"])["data"]
                    audition = data["audition"]; exact(audition, {"asset_ref", "sha256", "position", "duration", "source"})
                    if (audition["asset_ref"] != candidate["asset_ref"] or audition["sha256"] != asset["sha256"] or audition["duration"] != asset["duration"] or audition["source"] != "USER_REPORTED_PLAYBACK" or type(audition["position"]) not in {int, float} or not math.isfinite(audition["position"]) or not 0 < audition["position"] <= asset["duration"]): raise ValueError("请选择实际试听的准确音频版本。")
                    choice = insert("Choice", {"candidate_ref": data["candidate_ref"], "asset_ref": candidate["asset_ref"], "lyrics_ref": candidate["lyrics_ref"], "production_ref": candidate["production_ref"], "audition": audition, "confirmed_by": actor})
                    self.runtime.head(con, song, {"choice_ref": choice}); return choice
                if action == "confirm-master":
                    exact(data, {"choice_ref", "credits", "confirmation"})
                    if head["choice_ref"] != data["choice_ref"]: raise MusicConflict("选择已改变，请核对原选择。")
                    choice = self.runtime.get(con, company, workspace, data["choice_ref"], kind="Choice", song=song_ref)["data"]
                    if any(choice[k] != head[k] for k in {"lyrics_ref", "production_ref"}): raise MusicConflict("选择原依据已过期，请查看原版本。")
                    checked_asset = self.media.verify(con, company, workspace, song_ref, choice["asset_ref"])
                    master = insert("MasterRevision", {"previous_ref": head["master_ref"], "choice_ref": data["choice_ref"], **{k: choice[k] for k in ("candidate_ref", "asset_ref", "lyrics_ref", "production_ref")}, "rights": checked_asset["data"]["rights"], "credits": data["credits"], "confirmed_by": actor, "confirmation": data["confirmation"]})
                    self.runtime.head(con, song, {"master_ref": master}); return master
                if action == "prepare-release":
                    exact(data, {"master_ref"})
                    master = self.runtime.get(con, company, workspace, data["master_ref"], kind="MasterRevision", song=song_ref)["data"]
                    checked_asset = self.media.verify(con, company, workspace, song_ref, master["asset_ref"])
                    if master["rights"] != checked_asset["data"]["rights"]: raise ValueError("成品与音频用途不一致。")
                    return insert("ReleasePackage", {"master_ref": data["master_ref"], "title": head["title"], "status": "LOCAL_PREPARATION_NOT_PUBLISHED", "rights": master["rights"], "credits": master["credits"]})
                raise ValueError("不支持的歌曲命令。")
            result = self.runtime.receipt(con, scope=info["scope"], song=song_ref, action=action, request_id=request_id, inputs={"expected": expected, "data": data}, operation=operation)
            root = result if action == "create" else song_ref
        return {**self.content(company, workspace, root), "result_ref": result}

    @contextmanager
    def receiving_import(self, company, workspace, song_ref, request_id):
        text(request_id, 128, empty=False)
        info = self.entry.authoring_scope(company, workspace, write=True)
        key = digest([info["scope"], song_ref, "import-audio", request_id])
        with self._import_lock:
            if key in self._active_imports: raise MusicConflict("同一文件仍在接收，请查询原请求。")
            if len(self._active_imports) >= 64: raise MusicConflict("本机正在接收音频，请稍后再试。")
            self._active_imports.add(key)
        try: yield
        finally:
            with self._import_lock: self._active_imports.discard(key)

    def import_status(self, company, workspace, song_ref, request_id):
        text(request_id, 128, empty=False)
        info = self.entry.authoring_scope(company, workspace)
        key = "music-command:" + digest([info["scope"], song_ref, "import-audio", request_id])
        with self.db.connect() as con:
            original = self.runtime.get(con, company, workspace, song_ref, kind="Song")
            saved = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (TenantContext.current_tenant_id(), key)).fetchone()
            if not saved:
                with self._import_lock: receiving = key.removeprefix("music-command:") in self._active_imports
                return {"status": "UNKNOWN" if receiving else "NOT_APPLIED", "request_id": request_id, "basis": {key: original["data"][key] for key in ("lyrics_ref", "production_ref", "master_ref")}}
            receipt = json.loads(saved[0])
            self.runtime.get(con, company, workspace, receipt["result_ref"], kind="Candidate", song=song_ref)
        return {"status": "APPLIED", "request_id": request_id, "result_ref": receipt["result_ref"], **self.content(company, workspace, song_ref)}

    def selection(self, company, workspace, song_ref, selection, *, connection=None):
        def validate(con):
            song = self.runtime.get(con, company, workspace, song_ref, kind="Song")
            if not isinstance(selection, dict): raise ValueError("选段不合法。")
            if selection.get("kind") == "lyrics":
                exact(selection, {"kind", "version_ref", "draft_revision", "start", "end", "excerpt", "locator"})
                version = self.runtime.get(con, company, workspace, selection["version_ref"], kind="LyricsVersion", song=song_ref)
                body = version["data"]["text"].encode("utf-16-le")
                if (selection["version_ref"] != song["data"]["lyrics_ref"] or selection["draft_revision"] != version["data"]["draft_revision"] or selection["locator"] != "lyrics" or type(selection["start"]) is not int or type(selection["end"]) is not int or not 0 <= selection["start"] < selection["end"] <= len(body)//2): raise MusicConflict("歌词选段已过期或超出原版本。")
                try: excerpt = body[selection["start"]*2:selection["end"]*2].decode("utf-16-le")
                except UnicodeError as error: raise ValueError("不能切开完整字符。") from error
                if excerpt != selection["excerpt"]: raise MusicConflict("歌词选段与原保存版本不一致。")
            elif selection.get("kind") == "audio":
                exact(selection, {"kind", "song_ref", "candidate_ref", "candidate_version_ref", "asset_ref", "sha256", "start", "end", "duration", "anchor"})
                candidate = self.runtime.get(con, company, workspace, selection["candidate_ref"], kind="Candidate", song=song_ref)
                asset = self.media.verify(con, company, workspace, song_ref, selection["asset_ref"])["data"]
                if (selection["song_ref"] != song_ref or selection["candidate_version_ref"] != candidate["entity_id"] or candidate["data"]["asset_ref"] != selection["asset_ref"] or selection["sha256"] != asset["sha256"] or selection["duration"] != asset["duration"] or selection["anchor"] != "candidate-audio" or any(candidate["data"][k] != song["data"][k] for k in {"lyrics_ref", "production_ref"}) or any(type(selection[k]) not in {int, float} or not math.isfinite(selection[k]) for k in {"start", "end"}) or not 0 <= selection["start"] < selection["end"] <= asset["duration"]): raise MusicConflict("音频范围或原候选版本已过期。")
            else: raise ValueError("不支持的选段类型。")
            return dict(selection)
        if connection is not None: return validate(connection)
        with self.db.connect() as con: return validate(con)

    def resolve_references(self, scope, references):
        if not isinstance(references, list) or len(references) > 8: raise ValueError("引用超过允许数量。")
        if any(not isinstance(r, dict) or set(r)-{"reference_id", "workspace_id", "kind", "title", "version_ref", "purpose", "locator"} or not r.get("purpose") for r in references): raise ValueError("引用需要明确来源和用途。")
        return self.conversations.references(scope["company_id"], scope, references)

    def bind_discussion(self, company, workspace, song_ref, *, request_id, expected, assignment_ref):
        row = self.content(company, workspace, song_ref)
        info = self.entry.authoring_scope(company, workspace, write=True)
        with self.db.connect() as con: self.basis(con, company, workspace, row["song"], expected)
        if self.pending(info["scope"]): raise MusicConflict("请先核验工作空间的原请求。")
        assignment = next((a for a in info["assignments"] if a["assignment_ref"] == assignment_ref), None)
        if not assignment: raise RuntimeScopeError("歌曲缺少当前责任员工。")
        text(request_id, 128, empty=False)
        binding_ref = "music-binding:" + digest([info["scope"], song_ref, request_id])
        conversation = self.conversations.create(company, request_id=binding_ref, title=row["song"]["data"]["title"][:120], employee_ref=assignment["employee_ref"], discussion_scope={"workspace_id": workspace, "object_ref": song_ref, "assignment_ref": assignment_ref})
        binding = {"binding_ref": binding_ref, "scope": info["scope"], "song_ref": song_ref, "expected": expected, "context": self.conversations.context(company, assignment["employee_ref"], assignment_ref), "conversation_id": conversation["conversation_id"], "discussion_scope": conversation.get("discussion_scope")}
        event = self.conversations.events.record(correlation_id=song_ref, event_type="music.discussion.bound", payload=binding, idempotency_key=binding_ref)
        if event["payload"] != binding: raise MusicConflict("原讨论不能更换员工或依据。")
        return binding

    def query_request(self, company, workspace, song_ref, binding_ref, *, request_id=None, attempt_id=None):
        self.content(company, workspace, song_ref)
        with self.db.connect() as con:
            row = con.execute("select payload from evolution_events where tenant_id=? and event_type='music.discussion.bound' and idempotency_key=?", (TenantContext.current_tenant_id(), binding_ref)).fetchone()
        if not row: raise KeyError("原讨论不存在。")
        binding = json.loads(row[0])
        if (binding["song_ref"], binding["scope"]["company_id"], binding["scope"]["workspace_id"]) != (song_ref, company, workspace): raise RuntimeScopeError("原讨论不在当前歌曲。")
        result = self.conversations.read_attempt(company, binding["conversation_id"], attempt_id) if attempt_id else self.conversations.read_request(company, binding["conversation_id"], request_id)
        return {"binding": binding, **result}

    def agent_work_source(self, company, workspace, assignment_ref, source):
        exact(source, {"kind", "song_ref", "expected", "selection", "references"})
        info = self.entry.authoring_scope(company, workspace, write=True)
        row = self.content(company, workspace, source["song_ref"])
        with self.db.connect() as con:
            self.basis(con, company, workspace, row["song"], source["expected"])
        selected = self.selection(company, workspace, source["song_ref"], source["selection"])
        if selected["kind"] != "lyrics":
            raise RuntimeScopeError("当前 Agent 工作尚未核验音频读取，请先选择歌词；不能把音频元数据当作已听过音频。")
        refs = self.resolve_references(info["scope"], source["references"])
        return {"kind": "music", "scope": info["scope"], "song_ref": source["song_ref"],
                "expected": source["expected"], "selection": selected, "references": refs,
                "lyrics": row["lyrics"]["data"]["text"], "production": row["production"]["data"]["brief"]}

    def prepare_message(self, company, workspace, song_ref, *, binding_ref, body, request_id, model_key, expected, selection, references, work_ref=""):
        text(body, 2000, empty=False)
        row = self.content(company, workspace, song_ref); query = self.query_request(company, workspace, song_ref, binding_ref)
        binding = query["binding"]
        inputs = {"body": body, "model_key": model_key, "expected": expected, "selection": selection, "references": references}
        if work_ref:
            inputs["work_ref"] = work_ref
        originals = [m for m in query["messages"] if m.get("idempotency_key") == request_id]
        if originals:
            original = next((a for a in query["attempts"] if a["message_id"] == originals[0]["message_id"]), None)
            if original and original["execution_selection"]["input"] == inputs: return original, False
            raise MusicConflict("原请求不能换歌、模型或选段后重发。")
        if self.pending(binding["scope"]): raise MusicConflict("请先核验工作空间的原请求。")
        with self.db.connect() as con: self.basis(con, company, workspace, row["song"], expected)
        selected = self.selection(company, workspace, song_ref, selection)
        refs = self.resolve_references(binding["scope"], references)
        self.entry.prepare_model(company, workspace, binding["context"]["assignment_ref"], model_key)
        policy = self.entry.execution_policy(company, workspace, binding["context"]["assignment_ref"], model_key)
        context = self.conversations.context(company, policy["context"]["employee_ref"], binding["context"]["assignment_ref"])
        if context != binding["context"]: raise RuntimeScopeError("原责任已改变。")
        execution = {"purpose": PURPOSE, "scope": binding["scope"], "song_ref": song_ref, "content_ref": song_ref, "expected": expected, "basis_version_ref": expected["lyrics_ref"], "selection": selected, "references": refs, "context": context, "model": policy["model"], "binding_id": policy["binding"]["id"], "grant": policy["grant"], "source_class": policy["grant"].get("source_class", "REAL_PROVIDER_TEXT"), "input": inputs}
        if work_ref:
            execution.update(work_ref=work_ref, work_instruction=body.strip())
        compiled = body + "\n歌曲的原保存依据（仅文字建议，不生成音频）：" + json.dumps({"lyrics": row["lyrics"]["data"]["text"], "production": row["production"]["data"]["brief"], "execution": execution}, sort_keys=True, ensure_ascii=False)
        return self.conversations.prepare(company, context["employee_ref"], body=compiled, display_body=body, request_id=request_id, assignment_ref=context["assignment_ref"], references=refs, conversation_id=binding["conversation_id"], execution_selection=execution)

    def materialize_agent_candidate(self, proof, reply):
        source = proof["source"]
        company, workspace, song = source["scope"]["company_id"], source["scope"]["workspace_id"], source["song_ref"]
        info = self.entry.authoring_scope(company, workspace, write=True)
        with self.db.connect() as con:
            con.execute("begin immediate")
            row = self.content(company, workspace, song, connection=con)
            self.basis(con, company, workspace, row["song"], source["expected"])
            def operation():
                return self.runtime.insert(con, company, workspace, "Candidate", {"title": "Agent 文字建议",
                    "suggestion": reply["excerpt"], "lyrics_ref": source["expected"]["lyrics_ref"],
                    "production_ref": source["expected"]["production_ref"], "asset_ref": "",
                    "source": "AGENT_EXECUTOR", "provenance": proof["provenance"]}, info["actor"], song=song)
            ref = self.runtime.receipt(con, scope=info["scope"], song=song, action="agent-candidate",
                request_id=proof["task_ref"], inputs={"task_ref": proof["task_ref"], "reply": reply}, operation=operation)
        return {"candidate_ref": ref}

    def receive_dialogue(self, company, workspace, song_ref, expected, conversation, message):
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            song = self.runtime.get(con, company, workspace, song_ref, kind="Song")
            proof = self.conversations.dialogue_result(con, company, workspace, song_ref, conversation, message)
            def operation():
                self.basis(con, company, workspace, song, expected)
                return self.runtime.insert(con, company, workspace, "Candidate", {"title": "员工讨论文字回复",
                    "suggestion": proof["text"], "lyrics_ref": expected["lyrics_ref"], "production_ref": expected["production_ref"],
                    "asset_ref": "", "source": "CONTROLLED_EXECUTOR" if proof["provenance"].get("source_class") == "CONTROLLED_EXECUTOR" else "REAL_PROVIDER_TEXT",
                    "provenance": {**proof["provenance"], "dialogue_source": {"conversation_ref": conversation,
                        "message_ref": message}, "receiving_basis": expected}}, info["actor"], song=song_ref)
            ref = self.runtime.receipt(con, scope=info["scope"], song=song_ref, action="dialogue-candidate",
                request_id=digest([conversation, message]), inputs={"conversation_ref": conversation,
                    "message_ref": message, "expected": expected}, operation=operation)
            return {"candidate_ref": ref}

    def materialize_candidate(self, company, workspace, song_ref, *, binding_ref, attempt_id, request_id):
        query = self.query_request(company, workspace, song_ref, binding_ref, attempt_id=attempt_id)
        attempt = query["attempt"]
        replies = [m for m in query["messages"] if m["sender"]["kind"] == "EMPLOYEE" and m.get("idempotency_key") == attempt_id]
        if attempt["status"] != "COMPLETED" or len(replies) != 1: raise MusicConflict("原请求没有已核验的完整建议。")
        reply = replies[0]; provenance = reply.get("provenance", {}); execution = attempt.get("execution_selection", {})
        original = query["binding"]
        if (execution.get("purpose") != PURPOSE or execution.get("song_ref") != song_ref
                or execution.get("scope") != original["scope"] or execution.get("context") != original["context"]
                or execution.get("expected") != original["expected"]):
            raise RuntimeScopeError("只有这次歌曲选段的原请求可生成候选；普通讨论回复不会自动转为候选。")
        if provenance.get("execution_selection") != execution or not provenance.get("usage", {}).get("usage_record_id"): raise RuntimeScopeError("建议缺少实际用量依据。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = self.entry.authoring_scope(company, workspace, connection=con, write=True)
            usage = con.execute("select * from ai_usage_records where tenant_id=? and task_id=? and company_id=? and workspace_id=? and execution_ref=? and capability_binding_id=? and capability_id=?", (TenantContext.current_tenant_id(), reply["task_ref"], company, workspace, attempt_id, execution["binding_id"], execution["model"]["model_key"])).fetchall()
            task = con.execute("select status,output,employee_id from tasks where tenant_id=? and task_id=? and company_id=? and workspace_id=?", (TenantContext.current_tenant_id(), reply["task_ref"], company, workspace)).fetchone()
            if (len(usage) != 1 or usage[0]["usage_record_id"] != provenance["usage"]["usage_record_id"] or usage[0]["execution_status"] != "success" or usage[0]["fallback_from_model"] or not task or task["status"] != "COMPLETED" or task["output"] != reply["body"] or task["employee_id"] != usage[0]["employee_id"]): raise RuntimeScopeError("原建议、任务与实际用量不一致。")
            for field, kind in [("lyrics_ref", "LyricsVersion"), ("production_ref", "ProductionVersion")]: self.runtime.get(con, company, workspace, execution["expected"][field], kind=kind, song=song_ref)
            def operation():
                return self.runtime.insert(con, company, workspace, "Candidate", {"title": "员工文字建议", "suggestion": reply["body"], "lyrics_ref": execution["expected"]["lyrics_ref"], "production_ref": execution["expected"]["production_ref"], "asset_ref": "", "source": "CONTROLLED_EXECUTOR" if execution["source_class"] == "CONTROLLED_EXECUTOR" else "REAL_PROVIDER_TEXT", "provenance": provenance}, info["actor"], song=song_ref)
            # One candidate per actual attempt, regardless of changed client key.
            ref = self.runtime.receipt(con, scope=info["scope"], song=song_ref, action="reply-candidate", request_id=attempt_id, inputs={"attempt_id": attempt_id}, operation=operation)
        return {**self.content(company, workspace, song_ref), "result_ref": ref}

    def _operating_entry(self, company, workspace, *, connection=None, write=False):
        info = self.entry.authoring_scope(company, workspace, connection=connection, write=write)
        if info['definition']['version'] != '0.2.0':
            raise RuntimeScopeError('原版歌曲仍可继续；经营依据需要准确的新版本工作空间。')
        return info

    def _operating_records(self, con, company, workspace):
        from .runtime.music import OPERATING_KINDS
        rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.packageId')=? and json_extract(data_json,'$.objectType')='MusicOperatingScope' order by created_at,entity_id", (TenantContext.current_tenant_id(), company, workspace, 'com.curis.local.music')).fetchall()
        return [self._operating_get(con, company, workspace, x[0]) for x in rows if self.runtime.get(con, company, workspace, x[0])['data']['kind'] in OPERATING_KINDS]

    def _operating_get(self, con, company, workspace, ref, *, kind=None, seen=None):
        from .runtime.music import OPERATING_KINDS
        visited = set(seen or ())
        if ref in visited: raise ValueError('原依据关系形成循环。')
        visited.add(ref)
        row = self.runtime.get(con, company, workspace, ref, kind=kind)
        d = row['data']
        if d['kind'] not in OPERATING_KINDS: raise RuntimeScopeError('不是合法经营依据。')
        if d['previous_ref']:
            previous = self._operating_get(con, company, workspace, d['previous_ref'], kind=d['kind'], seen=visited)
            if previous['data']['identity_ref'] != d['identity_ref'] or previous['data']['revision'] + 1 != d['revision']: raise ValueError('原版本关系不一致。')
        elif d['identity_ref'] != ref or d['revision'] != 1: raise ValueError('对象首次版本身份不一致。')
        for source, hashed in d['basis'].items():
            original = self.runtime.get(con, company, workspace, source)
            if original['data']['payload_sha256'] != hashed: raise ValueError('原依据内容不可确认。')
            if original['data']['kind'] in OPERATING_KINDS: self._operating_get(con, company, workspace, source, seen=visited)
        sources = self._operating_sources(con, company, workspace, d['kind'], d)
        if d["basis"] != {x["entity_id"]: x["data"]["payload_sha256"] for x in sources}: raise ValueError("原依据关系校验不一致。")
        return row

    def _latest_operating(self, con, company, workspace, record):
        identity = record['data']['identity_ref']
        rows = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.objectType')='MusicOperatingScope' and json_extract(data_json,'$.identity_ref')=? order by json_extract(data_json,'$.revision') desc", (TenantContext.current_tenant_id(), company, workspace, identity)).fetchall()
        return self.runtime.get(con, company, workspace, rows[0][0], kind=record['data']['kind'])

    def _operating_sources(self, con, company, workspace, kind, d):
        sources = []
        def use(ref, expected):
            row = self.runtime.get(con, company, workspace, ref, kind=expected)
            sources.append(row); return row
        if kind != 'OperatingScope': use(d['scope_ref'], 'OperatingScope')
        if kind == 'ReferenceAnalysis':
            snapshot = use(d['snapshot_ref'], 'MarketSnapshot')
            if snapshot['data']['scope_ref'] != d['scope_ref']: raise RuntimeScopeError('参考属于另一个原观察范围。')
        if kind == 'Direction':
            for ref in d['reference_refs']:
                item = use(ref, 'ReferenceAnalysis')
                if item['data']['scope_ref'] != d['scope_ref']: raise RuntimeScopeError('方向参考不属于原观察范围。')
            if d['learning_ref']:
                item = use(d['learning_ref'], 'Learning')
                if item['data']['scope_ref'] != d['scope_ref'] or not item['data']['accepted_by']: raise RuntimeScopeError('所选经验没有明确接受或属于其他范围。')
        if kind == 'Observation':
            song = self.runtime.get(con, company, workspace, d['song_ref'], kind='Song')
            master = use(d['master_ref'], 'MasterRevision'); package = use(d['release_ref'], 'ReleasePackage')
            if any(x['parent_id'] != song['entity_id'] for x in (master, package)) or package['data']['master_ref'] != master['entity_id']: raise RuntimeScopeError('观察没有指向同一首歌的准确Master与发行准备包。')
            direction_ref = song['data'].get('direction_ref')
            if direction_ref and self.runtime.get(con, company, workspace, direction_ref, kind='Direction')['data']['scope_ref'] != d['scope_ref']: raise RuntimeScopeError('歌曲创作范围与观察不一致。')
        if kind == 'Report':
            for ref in d['observation_refs']:
                row = use(ref, 'Observation')
                if row['data']['scope_ref'] != d['scope_ref']: raise RuntimeScopeError('报告观察不属于原范围。')
            for saved, source in zip(d['rows'], sources[1:]):
                if saved != source: raise ValueError('报告原始观察快照不一致。')
            permitted = {u['usage_record_id']: u for u in self._report_usage(con, company, workspace, d['rows'])}
            if len({u.get('usage_record_id') for u in d['usage']}) != len(d['usage']) or any(permitted.get(u.get('usage_record_id')) != u for u in d['usage']): raise RuntimeScopeError('原报告用量不属于所选歌曲的唯一实际账本来源。')
        if kind == 'Learning':
            report = use(d['report_ref'], 'Report')
            if report['data']['scope_ref'] != d['scope_ref'] or not report['data']['confirmed_by']: raise RuntimeScopeError('经验缺少已确认的原报告。')
        return sources

    def _append_operating(self, con, company, workspace, kind, payload, actor, expected_ref=''):
        from uuid import uuid4
        if set(payload) & {"identity_ref", "previous_ref", "revision", "basis"}: raise ValueError("不能提供服务器版本身份。")
        previous = self._operating_get(con, company, workspace, expected_ref, kind=kind) if expected_ref else None
        if previous and self._latest_operating(con, company, workspace, previous)['entity_id'] != expected_ref: raise MusicConflict('原版本已有后续修改，请保留输入并核对。')
        ref = 'music-' + str(uuid4())
        sources = self._operating_sources(con, company, workspace, kind, payload)
        basis = {x['entity_id']: x['data']['payload_sha256'] for x in sources}
        value = {**payload, 'identity_ref': previous['data']['identity_ref'] if previous else ref, 'previous_ref': expected_ref,
            'revision': previous['data']['revision'] + 1 if previous else 1, 'basis': basis}
        result = self.runtime.insert(con, company, workspace, kind, value, actor, entity_id=ref)
        for original in sources:
            con.execute('insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)', (TenantContext.current_tenant_id(), result, 'MUSIC_USES_' + original['data']['kind'].upper(), original['entity_id']))
        return result

    def _observation_rows(self, con, company, workspace, selection):
        exact(selection, {'scope_ref', 'song_ref', 'period'})
        self._operating_get(con, company, workspace, selection['scope_ref'], kind='OperatingScope')
        if selection['song_ref']: self.runtime.get(con, company, workspace, selection['song_ref'], kind='Song')
        text(selection['period'], 200, empty=False)
        records = self._operating_records(con, company, workspace)
        rows = [x for x in records if x['data']['kind'] == 'Observation' and x['data']['scope_ref'] == selection['scope_ref'] and
            (not selection['song_ref'] or x['data']['song_ref'] == selection['song_ref']) and
            (selection['period'] == 'all' or '|'.join(x['data']['period'][k] for k in ('start', 'end', 'timezone')) == selection['period'])]
        rows = [x for x in rows if self._latest_operating(con, company, workspace, x)['entity_id'] == x['entity_id']]
        return sorted(rows, key=lambda x: (x['data']['identity_ref'], x['data']['revision']))

    def _report_usage(self, con, company, workspace, observations):
        ids = set()
        for ref in {x['data']['song_ref'] for x in observations}:
            song = self.content(company, workspace, ref, connection=con)
            for candidate in song['candidates']:
                usage = candidate['data']['provenance'].get('usage', {})
                if usage.get('usage_record_id'): ids.add(usage['usage_record_id'])
        rows = []
        for ref in sorted(ids):
            row = con.execute('select usage_record_id,task_id,execution_ref,employee_id,model_name,input_tokens,output_tokens,total_tokens,cost_amount,currency,cost_source from ai_usage_records where tenant_id=? and company_id=? and workspace_id=? and usage_record_id=?', (TenantContext.current_tenant_id(), company, workspace, ref)).fetchone()
            if not row: raise RuntimeScopeError('原任务用量来源不可确认。')
            rows.append(dict(row))
        return rows

    def _report_current(self, con, company, workspace, report):
        d = report['data']; rows = self._observation_rows(con, company, workspace, d['selection']); usage = self._report_usage(con, company, workspace, rows)
        return d['basis_hash'] == digest({'rows': rows, 'usage': usage, 'selection': d['selection']})

    def operating_collection(self, company, workspace):
        info = self._operating_entry(company, workspace)
        with self.db.connect() as con:
            records = self._operating_records(con, company, workspace)
            return {'entry': info, 'records': records, 'pending_requests': self.pending(info['scope'], connection=con),
                'report_current': {r['entity_id']: self._report_current(con, company, workspace, r) for r in records if r['data']['kind'] == 'Report'}}

    def operating_content(self, company, workspace, ref):
        self._operating_entry(company, workspace)
        with self.db.connect() as con:
            row = self._operating_get(con, company, workspace, ref)
            return {'record': row, 'current_version_ref': self._latest_operating(con, company, workspace, row)['entity_id'],
                'report_current': self._report_current(con, company, workspace, row) if row['data']['kind'] == 'Report' else None}

    def operating_command(self, company, workspace, action, *, request_id, expected_ref='', data):
        from datetime import datetime, timezone
        with self.db.connect() as con:
            con.execute('begin immediate')
            info = self._operating_entry(company, workspace, connection=con, write=True)
            if self.pending(info['scope'], connection=con): raise MusicConflict('请先核验本工作空间的原建议请求。')
            actor = info['actor']
            def operation():
                kinds = {'save-scope': 'OperatingScope', 'save-snapshot': 'MarketSnapshot', 'save-reference': 'ReferenceAnalysis', 'save-direction': 'Direction', 'save-observation': 'Observation', 'save-learning': 'Learning'}
                if action in kinds:
                    kind = kinds[action]; value = dict(data)
                    if kind == 'Direction':
                        exact(value, {'title', 'body', 'scope_ref', 'reference_refs', 'learning_ref', 'confirmed'})
                        if type(value['confirmed']) is not bool: raise ValueError('方向确认必须明确。')
                        value['confirmed_by'] = actor if value.pop('confirmed') else ''; value['confirmed_at'] = datetime.now(timezone.utc).isoformat() if value['confirmed_by'] else ''
                        if value['learning_ref']: self._require_learning(con, company, workspace, value['learning_ref'], historical=False)
                    if kind == 'Observation':
                        if 'verification' in value: raise ValueError('不能指定外部效果核验状态。')
                        value['verification'] = 'UNVERIFIED'
                    if kind == 'Learning':
                        exact(value, {'title', 'body', 'scope_ref', 'report_ref', 'counterexample', 'applicability', 'accepted'})
                        report = self._operating_get(con, company, workspace, value['report_ref'], kind='Report')
                        if not self._report_current(con, company, workspace, report): raise MusicConflict('当前观察依据已改变，原报告保持可读，请明确核对新报告。')
                        if type(value['accepted']) is not bool: raise ValueError('接受用途必须明确。')
                        value['accepted_by'] = actor if value.pop('accepted') else ''; value['validation'] = 'UNVERIFIED'
                    return self._append_operating(con, company, workspace, kind, value, actor, expected_ref)
                if action in {'create-report', 'confirm-report'}:
                    if action == 'create-report':
                        exact(data, {'title', 'body', 'selection'})
                        rows = self._observation_rows(con, company, workspace, data['selection'])
                        if not rows: raise ValueError('当前范围与周期没有原观察，不生成空事实报告。')
                        usage = self._report_usage(con, company, workspace, rows)
                        value = {**data, 'scope_ref': data['selection']['scope_ref'], 'observation_refs': [x['entity_id'] for x in rows], 'rows': rows, 'usage': usage, 'basis_hash': digest({'rows': rows, 'usage': usage, 'selection': data['selection']}), 'confirmed_by': '', 'usage_basis': 'SONG_CUMULATIVE_CREATIVE_CALLS'}
                    else:
                        exact(data, {'report_ref', 'confirmed'})
                        report = self._operating_get(con, company, workspace, data['report_ref'], kind='Report')
                        if expected_ref != report['entity_id'] or data['confirmed'] is not True or not self._report_current(con, company, workspace, report): raise MusicConflict('原报告依据已改变或未明确确认。')
                        value = {k: v for k, v in report['data'].items() if k not in {'packageId', 'packageVersion', 'schemaVersion', 'objectType', 'kind', 'payload_sha256', 'identity_ref', 'previous_ref', 'revision', 'basis'}}
                        value['confirmed_by'] = actor
                    return self._append_operating(con, company, workspace, 'Report', value, actor, expected_ref)
                if action == 'use-learning':
                    exact(data, {'learning_ref', 'title', 'body', 'confirmed', 'historical'})
                    if data['confirmed'] is not True or type(data['historical']) is not bool: raise ValueError('请明确确认引用经验的用途与原版本。')
                    learning = self._require_learning(con, company, workspace, data['learning_ref'], historical=data['historical'])
                    report = self._operating_get(con, company, workspace, learning['data']['report_ref'], kind='Report')
                    original_refs = []
                    for saved in report['data']['rows']:
                        song = self.runtime.get(con, company, workspace, saved['data']['song_ref'], kind='Song')
                        if song['data'].get('direction_ref'):
                            direction = self._operating_get(con, company, workspace, song['data']['direction_ref'], kind='Direction')
                            original_refs.extend(direction['data']['reference_refs'])
                    if not original_refs: raise ValueError('原作品没有可确认的方向参考，经验保留只读，不能补造方向。')
                    d = learning['data']
                    value = {'title': data['title'], 'body': data['body'] + '\n原经验：' + d['body'] + '\n适用范围：' + d['applicability'] + '\n反例与限制：' + d['counterexample'] + '\n效果仍待验证；固定原报告与原观察版本。', 'scope_ref': d['scope_ref'], 'reference_refs': list(dict.fromkeys(original_refs)), 'learning_ref': learning['entity_id'], 'confirmed_by': actor, 'confirmed_at': datetime.now(timezone.utc).isoformat()}
                    return self._append_operating(con, company, workspace, 'Direction', value, actor, expected_ref)
                if action in {'create-song', 'apply-direction'}:
                    fields = {'direction_ref', 'confirmed', 'historical', 'title', 'intention', 'lyrics', 'production', 'draft_revision'} if action == 'create-song' else {'direction_ref', 'song_ref', 'confirmed', 'historical'}
                    exact(data, fields)
                    if data['confirmed'] is not True or type(data['historical']) is not bool: raise ValueError('请明确确认原方向及本次创作意图。')
                    direction = self._operating_get(con, company, workspace, data['direction_ref'], kind='Direction'); d = direction['data']
                    if not d['confirmed_by']: raise ValueError('方向尚未明确确认。')
                    if self._latest_operating(con, company, workspace, direction)['entity_id'] != direction['entity_id'] and not data['historical']: raise MusicConflict('方向已有后续版本；请明确选择原版及适用范围。')
                    if d['learning_ref']: self._require_learning(con, company, workspace, d['learning_ref'], historical=data['historical'])
                    if action == 'apply-direction':
                        song = self.runtime.get(con, company, workspace, data['song_ref'], kind='Song')
                        con.execute('insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)', (TenantContext.current_tenant_id(), song['entity_id'], 'MUSIC_EXPLICIT_DIRECTION_REFERENCE', direction['entity_id']))
                        return song['entity_id']
                    value = {"title": text(data["title"], 240, empty=False), "intention": text(data["intention"], 2000)}
                    value.update(lyrics_ref='', production_ref='', choice_ref='', master_ref='', direction_ref=direction['entity_id'], learning_ref=d['learning_ref'])
                    song = self.runtime.insert(con, company, workspace, 'Song', value, actor)
                    lyrics = self.runtime.insert(con, company, workspace, 'LyricsVersion', {'text': data['lyrics'], 'previous_ref': '', 'draft_revision': data['draft_revision']}, actor, song=song)
                    production = self.runtime.insert(con, company, workspace, 'ProductionVersion', {'brief': data['production'], 'previous_ref': '', 'draft_revision': data['draft_revision']}, actor, song=song)
                    self.runtime.head(con, self.runtime.get(con, company, workspace, song, kind='Song'), {'lyrics_ref': lyrics, 'production_ref': production})
                    con.execute('insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values (?,?,?,?,current_timestamp)', (TenantContext.current_tenant_id(), song, 'MUSIC_CREATED_FROM_DIRECTION', direction['entity_id']))
                    return song
                raise ValueError('未授权的音乐经营动作。')
            result = self.runtime.receipt(con, scope=info['scope'], song=expected_ref, action='operating:' + action, request_id=request_id, inputs={'expected_ref': expected_ref, 'data': data}, operation=operation)
        if action in {'create-song', 'apply-direction'}: return {**self.content(company, workspace, result), 'result_ref': result}
        return {**self.operating_content(company, workspace, result), 'result_ref': result}

    def _require_learning(self, con, company, workspace, ref, *, historical):
        learning = self._operating_get(con, company, workspace, ref, kind='Learning')
        if not learning['data']['accepted_by']: raise ValueError('经验的用途尚未明确接受。')
        report = self._operating_get(con, company, workspace, learning['data']['report_ref'], kind='Report')
        current = self._latest_operating(con, company, workspace, learning)['entity_id'] == ref and self._report_current(con, company, workspace, report)
        if not current and not historical: raise MusicConflict('所选经验属于原版本；保留原引用只读，明确核对历史用途后才可采用。')
        return learning
