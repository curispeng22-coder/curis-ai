"""Bounded user-provided CG originals, with scoped immutable candidates and no external media."""
from __future__ import annotations
import fcntl
import hashlib
import json
import os
import re
import stat
import struct
import zlib
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone
from .music_media_service import directory, ensure_directory, inspect_audio
from .content_growth_service import ContentGrowthConflict
from .content_growth_operating_service import ContentGrowthOperatingService, encode, digest
from .runtime import RuntimeScopeError

TREE = "data/assets/content-growth-media"
SCHEMA = "cg.local-media/v1"
MAX_TOTAL = 128 * 1024 * 1024
MAX_FILES = 128
MAX_BACKUP = 512 * 1024 * 1024
MIME = {"image/png": ("png", 20 * 1024 * 1024), "image/jpeg": ("jpg", 20 * 1024 * 1024), "audio/wav": ("wav", 16_000_000), "video/mp4": ("mp4", MAX_TOTAL)}


def inspect_media(raw, mime):
    if not isinstance(mime, str) or mime not in MIME or not isinstance(raw, bytes) or not 0 < len(raw) <= MIME[mime][1]:
        raise ValueError("本地媒体格式不支持或超过允许大小。")
    details = {}
    if mime == "audio/wav":
        details["duration"] = inspect_audio(raw)["duration"]
    elif mime == "image/png":
        if raw[:8] != b"\x89PNG\r\n\x1a\n": raise ValueError("PNG签名不匹配。")
        offset, ended = 8, False
        while offset + 12 <= len(raw):
            size = int.from_bytes(raw[offset:offset+4], "big"); tag = raw[offset+4:offset+8]
            end = offset + 12 + size
            if end > len(raw) or zlib.crc32(raw[offset+4:end-4]) & 0xffffffff != int.from_bytes(raw[end-4:end], "big"):
                raise ValueError("PNG块长度或摘要不合法。")
            if offset == 8:
                if tag != b"IHDR" or size != 13: raise ValueError("PNG缺少明确尺寸。")
                width, height = struct.unpack(">II", raw[offset+8:offset+16])
                if not 0 < width <= 16384 or not 0 < height <= 16384 or width * height > 64_000_000: raise ValueError("图片尺寸超过本地预览范围。")
                details.update(width=width, height=height)
            offset = end
            if tag == b"IEND":
                ended = size == 0 and offset == len(raw)
                break
        if not ended: raise ValueError("PNG数据不完整。")
    elif mime == "image/jpeg":
        if raw[:2] != b"\xff\xd8" or raw[-2:] != b"\xff\xd9": raise ValueError("JPEG签名或结尾不完整。")
        offset = 2
        while offset + 4 <= len(raw):
            if raw[offset] != 255: raise ValueError("JPEG块无效。")
            marker = raw[offset+1]; offset += 2
            if marker == 255: offset -= 1; continue
            if marker in {0xd8, 0xd9}: continue
            length = int.from_bytes(raw[offset:offset+2], "big")
            if length < 2 or offset + length > len(raw): raise ValueError("JPEG块越界。")
            if marker in {0xc0, 0xc1, 0xc2}:
                if length < 8: raise ValueError("JPEG尺寸缺失。")
                height, width = struct.unpack(">HH", raw[offset+3:offset+7])
                if not 0 < width <= 16384 or not 0 < height <= 16384 or width * height > 64_000_000: raise ValueError("图片尺寸超出范围。")
                details.update(width=width, height=height)
            if marker == 0xda: break
            offset += length
        if not details: raise ValueError("JPEG缺少可核对尺寸。")
    else:
        offset, boxes = 0, set()
        while offset + 8 <= len(raw):
            length = int.from_bytes(raw[offset:offset+4], "big"); tag = raw[offset+4:offset+8]; header = 8
            if length == 1:
                if offset + 16 > len(raw): raise ValueError("MP4扩展块不完整。")
                length = int.from_bytes(raw[offset+8:offset+16], "big"); header = 16
            if length == 0: length = len(raw) - offset
            if length < header or offset + length > len(raw): raise ValueError("MP4块长度无效。")
            if offset == 0 and (tag != b"ftyp" or length < 16 or raw[offset+8:offset+12] not in {b"isom", b"iso2", b"mp41", b"mp42", b"avc1", b"M4V "}):
                raise ValueError("MP4签名或容器类型不支持。")
            boxes.add(tag); offset += length
        if offset != len(raw) or not {b"ftyp", b"moov", b"mdat"} <= boxes: raise ValueError("MP4容器不完整。")
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw), "mime": mime, "extension": MIME[mime][0], **details}


def backup_budget(root, additional):
    """Conservative ZIP_STORED budget, including WAL, manifest/header/transaction reserve."""
    total, count = 0, 0
    for base, dirs, files in os.walk(root, followlinks=False):
        relative = Path(base).relative_to(root)
        if relative == Path("."): dirs[:] = [n for n in dirs if n not in {"cache", "tmp", "logs", "runtime", "recovery"}]
        for name in dirs + files:
            path = Path(base) / name; value = path.lstat()
            if stat.S_ISLNK(value.st_mode) or (stat.S_ISREG(value.st_mode) and value.st_nlink != 1): raise ValueError("数据根包含不安全链接。")
        for name in files:
            path = Path(base) / name; value = path.lstat()
            if not stat.S_ISREG(value.st_mode): raise ValueError("数据根含非常规文件。")
            total += value.st_size; count += 1
    # Recovery's unchanged MAX_MANIFEST=4MiB plus room for the registration transaction.
    if count + 8 > 20_000 or total + additional + 8 * 1024 * 1024 + (count + 8) * 1024 > MAX_BACKUP:
        raise ValueError("当前数据根接近备份容量上限；没有保存新媒体，请先处理已有本地数据。")


class ContentGrowthMediaService:
    def __init__(self, database, *, data_root=None):
        self.db, self.data_root, self.root = database, None, None
        if data_root is not None:
            base = Path(os.path.abspath(data_root))
            if not Path(data_root).is_absolute(): raise ValueError("媒体数据根必须是服务器指定绝对路径。")
            expected = base / "data/curis.sqlite"
            if any(not value or Path(os.path.abspath(value)) != expected for value in [database.path, *(os.environ.get(k) for k in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"))]):
                raise ValueError("CG媒体数据根与数据库别名不一致。")
            fd = directory(base); os.close(fd)
            self.data_root, self.root = base, base / TREE

    def _rows(self, con, info, content):
        scope = info["scope"]
        rows = con.execute("select entity_id,data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and parent_id=? "
            "and entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.schemaVersion')=? order by created_at,entity_id",
            (scope["tenant_id"], scope["company_id"], scope["workspace_id"], content, SCHEMA)).fetchall()
        result = []
        for row in rows:
            data = json.loads(row["data_json"])
            if data.get("scope") != scope or data.get("content_ref") != content or digest(data.get("payload")) != data.get("payload_sha256"):
                raise ContentGrowthConflict("媒体来源与摘要不一致。")
            result.append({"ref": row["entity_id"], **data})
        return result

    def _insert(self, con, info, content, kind, payload):
        ref, at, scope = "cg-media-" + str(uuid4()), datetime.now(timezone.utc).isoformat(), info["scope"]
        record = {"ref": ref, "schemaVersion": SCHEMA, "objectType": "CGMedia" + kind, "kind": kind, "scope": scope, "content_ref": content,
            "payload": payload, "payload_sha256": digest(payload), "actor": info["actor"], "created_at": at,
            "rights": "LOCAL_USER_PROVIDED_UNVERIFIED", "purpose": "LOCAL_USE_ONLY"}
        con.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
            "values (?,?,'PACKAGE_DOMAIN_OBJECT',?,?,?,?,'ACTIVE',?,'UNVERIFIED','MISSING',?,?,?)", (ref, scope["tenant_id"], scope["company_id"], scope["workspace_id"], content, info["actor"], SCHEMA, encode(record), at, at))
        return record

    def _raw(self, asset):
        if self.root is None: raise RuntimeScopeError("本地媒体尚未配置。")
        meta = asset["payload"]["media"]
        if meta.get("mime") not in MIME or not re.fullmatch(r"[0-9a-f]{64}", str(meta.get("sha256", ""))) or meta.get("extension") != MIME[meta["mime"]][0]: raise ValueError("媒体元数据无效。")
        parent = directory(self.root)
        try:
            fd = os.open(meta["sha256"] + "." + meta["extension"], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
            with os.fdopen(fd, "rb") as handle:
                st = os.fstat(handle.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size != meta["size"] or not 0 < st.st_size <= MIME[meta["mime"]][1]: raise ValueError("媒体文件不完整或不安全。")
                raw = handle.read(st.st_size + 1)
            if inspect_media(raw, meta["mime"]) != meta: raise ValueError("媒体字节与原资产不一致。")
            return raw
        finally: os.close(parent)

    def collection(self, service, company, workspace, content):
        with self.db.connect() as con:
            info = service.entry.authoring_scope(company, workspace, connection=con)
            item = con.execute("select current_version_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? and entity_id=? and entity_type='CONTENT_ITEM'", (info["scope"]["tenant_id"], company, workspace, content)).fetchone()
            if not item: raise RuntimeScopeError("媒体所属内容不可访问。")
            rows = self._rows(con, info, content)
            current = ContentGrowthOperatingService(self.db, service=service).context(con, info, content, item[0])
            context_ref = current["ref"] if current else ""
            for row in rows:
                if row["kind"] == "Candidate": row["eligible"] = row["payload"]["version_ref"] == item[0] and row["payload"]["context_ref"] == context_ref
            return {"entry": info, "configured": self.root is not None, "records": rows}

    def import_asset(self, service, company, workspace, content, request_id, expected_version_ref, data, raw):
        if self.root is None: raise RuntimeScopeError("当前服务器未配置本机媒体根。")
        if not isinstance(data, dict) or set(data) != {"title", "sha256", "size", "mime", "use"} or not isinstance(data["title"], str) or not data["title"].strip() or len(data["title"]) > 240 or data["use"] not in {"REFERENCE", "OUTPUT"}:
            raise ValueError("请明确本地媒体名称、格式和用途。")
        meta = inspect_media(raw, data["mime"])
        if type(data["size"]) is not int or data["size"] != len(raw) or data["sha256"] != meta["sha256"]: raise ValueError("媒体实际字节与原请求大小/摘要不一致。")
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128: raise ValueError("请保留原导入请求。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = service.entry.authoring_scope(company, workspace, connection=con, write=True)
            companion = ContentGrowthOperatingService(self.db, service=service)
            item, version = companion._content(con, info, content, expected_version_ref)
            fingerprint = digest([content, expected_version_ref, data])
            key = "cg.media.import:" + digest([info["scope"], info["actor"], request_id])
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (info["scope"]["tenant_id"], key)).fetchone()
            if old:
                receipt = json.loads(old[0])
                if receipt["fingerprint"] != fingerprint: raise ContentGrowthConflict("原导入请求不能换文件或版本。")
                self._raw(receipt["asset"])
                return receipt
            if item["current_version_id"] != expected_version_ref: raise ContentGrowthConflict("正文已更新，请保存原文件并核对新依据。")
            format = json.loads(item["data_json"])["format"]
            category = meta["mime"].split("/")[0]
            if data["use"] == "OUTPUT" and category != {"graphic": "image", "speech": "audio", "short_video": "video", "long_video": "video"}[format]:
                raise ValueError("候选文件类型与当前制作形态不一致；可另选为参考素材。")
            context = companion.context(con, info, content, expected_version_ref)
            parent = ensure_directory(self.root); lockdir = ensure_directory(self.data_root / "cache/tmp")
            lockfd = os.open("cg-media.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=lockdir)
            try:
                if not stat.S_ISREG(os.fstat(lockfd).st_mode) or os.fstat(lockfd).st_nlink != 1: raise ValueError("媒体配额锁不安全。")
                fcntl.flock(lockfd, fcntl.LOCK_EX)
                names = os.listdir(parent)
                if any(not re.fullmatch(r"[0-9a-f]{64}\.(png|jpg|wav|mp4)", n) for n in names): raise ValueError("媒体根包含未知文件。")
                sizes = [os.stat(n, dir_fd=parent, follow_symlinks=False) for n in names]
                if any(not stat.S_ISREG(v.st_mode) or v.st_nlink != 1 for v in sizes): raise ValueError("媒体根包含不安全文件。")
                name = meta["sha256"] + "." + meta["extension"]
                additional = 0 if name in names else len(raw)
                if len(names) + (name not in names) > MAX_FILES or sum(v.st_size for v in sizes) + additional > MAX_TOTAL: raise ValueError("本地CG媒体最多128个文件且总额128MiB；原数据保留。")
                backup_budget(self.data_root, additional)
                if name not in names:
                    # Publish only complete bytes with O_EXCL; quota/orphans remain accounted after a registration failure.
                    temporary = "cg-import-" + str(uuid4())
                    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=lockdir)
                    try:
                        with os.fdopen(fd, "wb") as target: target.write(raw); target.flush(); os.fsync(target.fileno())
                        # Same-device publication uses an exclusive target; no overwriting an existing original.
                        os.link(temporary, name, src_dir_fd=lockdir, dst_dir_fd=parent, follow_symlinks=False)
                        os.fsync(parent)
                    finally: os.unlink(temporary, dir_fd=lockdir)
                asset = self._insert(con, info, content, "Asset", {"title": data["title"], "version_ref": expected_version_ref, "media": meta, "use": data["use"]})
                self._raw(asset)
                candidate = self._insert(con, info, content, "Candidate", {"title": data["title"], "asset_ref": asset["ref"], "version_ref": expected_version_ref, "context_ref": context["ref"] if context else ""}) if data["use"] == "OUTPUT" else None
                receipt = {"fingerprint": fingerprint, "asset": asset, "candidate": candidate}
                con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)", (info["scope"]["tenant_id"], content, "cg.media.imported", encode(receipt), key))
                return receipt
            finally: os.close(lockfd); os.close(lockdir); os.close(parent)

    def adopt(self, service, company, workspace, content, request_id, candidate_ref, confirmed, rights_confirmed):
        if confirmed is not True or rights_confirmed is not True or not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128: raise ValueError("请明确核对内容、原依据与仅本地用途。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            info = service.entry.authoring_scope(company, workspace, connection=con, write=True)
            rows = self._rows(con, info, content); candidate = next((r for r in rows if r["ref"] == candidate_ref and r["kind"] == "Candidate"), None)
            if not candidate: raise RuntimeScopeError("媒体候选不属于当前内容。")
            key = "cg.media.adopt:" + digest([info["scope"], info["actor"], request_id])
            old = con.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?", (info["scope"]["tenant_id"], key)).fetchone()
            if old:
                value = json.loads(old[0])
                if value["candidate_ref"] != candidate_ref: raise ContentGrowthConflict("原采用请求不能替换候选。")
                return value
            companion = ContentGrowthOperatingService(self.db, service=service)
            item, _ = companion._content(con, info, content, candidate["payload"]["version_ref"])
            current = companion.context(con, info, content, item["current_version_id"])
            if item["current_version_id"] != candidate["payload"]["version_ref"] or candidate["payload"]["context_ref"] != (current["ref"] if current else ""):
                raise ContentGrowthConflict("媒体候选的正文或引用已变化，请保留原候选并重新核对。")
            asset = next((r for r in rows if r["ref"] == candidate["payload"]["asset_ref"] and r["kind"] == "Asset"), None)
            if not asset: raise RuntimeScopeError("媒体资产缺失。")
            self._raw(asset)
            result = self._insert(con, info, content, "Adoption", {"candidate_ref": candidate_ref, "asset_ref": asset["ref"], "version_ref": candidate["payload"]["version_ref"], "context_ref": candidate["payload"]["context_ref"]})
            receipt = {"candidate_ref": candidate_ref, "adoption": result}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)", (info["scope"]["tenant_id"], content, "cg.media.adopted", encode(receipt), key))
            return receipt

    def read(self, service, company, workspace, content, asset_ref, range_header=None):
        result = self.collection(service, company, workspace, content)
        asset = next((r for r in result["records"] if r["ref"] == asset_ref and r["kind"] == "Asset"), None)
        if asset is None: raise RuntimeScopeError("资产不属于这个内容。")
        raw = self._raw(asset); start, end, status = 0, len(raw) - 1, 200
        headers = {"Accept-Ranges": "bytes", "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff", "ETag": '"' + asset["payload"]["media"]["sha256"] + '"'}
        if range_header:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header)
            if not match or not any(match.groups()): raise ValueError("媒体范围不合法。")
            left, right = match.groups()
            if left: start = int(left); end = min(int(right), end) if right else end
            elif int(right) > 0: start = max(0, len(raw) - int(right))
            else: raise ValueError("媒体范围无效。")
            if not 0 <= start <= end < len(raw): raise ValueError("媒体范围超出文件。")
            status = 206; headers["Content-Range"] = f"bytes {start}-{end}/{len(raw)}"
        return raw[start:end+1], asset["payload"]["media"]["mime"], status, headers
