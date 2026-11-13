#!/usr/bin/env python3
"""Curis V1 release backup/restore utility (SQLite only; Keychain is excluded)."""

from __future__ import annotations

import argparse
import fcntl
import contextlib
import hashlib
import io
import wave
import json
import os
import re
import secrets
import struct
import shutil
import sqlite3
import stat
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from pathlib import PurePosixPath


FORMAT = "curis.release-backup/v1"
DB_ENTRY = "data/curis.sqlite"
MANIFEST_ENTRY = "manifest.json"
FULL_FORMAT = "curis.full-backup/v2"
APP_VERSION = os.environ.get("CURIS_DESKTOP_VERSION", "standalone-isolated")
MAX_ARCHIVE = 512 * 1024 * 1024
MAX_TOTAL = 2 * 1024 * 1024 * 1024
MAX_MEMBER = 256 * 1024 * 1024
MAX_ENTRIES = 20_000
MAX_MANIFEST = 4 * 1024 * 1024
MAX_RATIO = 200
SAFETY_LIMIT = 8
EXCLUDED_ROOTS = {"cache", "tmp", "logs", "runtime", "recovery"}
EXCLUDED_DATA = {"curis.sqlite-wal", "curis.sqlite-shm", "curis.sqlite-journal"}


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _strict_json(raw: bytes):
    if len(raw) > MAX_MANIFEST:
        raise ValueError("structured JSON exceeds bound")
    def unique_pairs(pairs):
        value = {}
        for key, child in pairs:
            if key in value:
                raise ValueError("duplicate JSON key")
            value[key] = child
        return value
    value = json.loads(raw, object_pairs_hook=unique_pairs)
    def depth(item, level=0):
        if level > 24:
            raise ValueError("JSON nesting exceeds bound")
        if isinstance(item, dict):
            for child in item.values(): depth(child, level + 1)
        elif isinstance(item, list):
            for child in item: depth(child, level + 1)
    depth(value)
    return value


def _bounded_json(raw: bytes) -> dict:
    value = _strict_json(raw)
    if not isinstance(value, dict):
        raise ValueError("manifest must be an object")
    return value


def _relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("unsafe member name")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(part in {".", "..", ""} for part in path.parts):
        raise ValueError("unsafe member name")
    return value


def _regular(path: Path) -> os.stat_result:
    with _held_file(path) as descriptor:
        info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError("nonregular or linked managed file")
    return info


@contextlib.contextmanager
def _held_dir(path: Path, create: bool = False):
    """Traverse each component from / with an owned, non-following directory fd."""
    absolute = path.absolute()
    if not absolute.is_absolute() or ".." in absolute.parts:
        raise ValueError("unsafe directory path")
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in absolute.parts[1:]:
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=descriptor)
                    os.fsync(descriptor)
                except FileExistsError:
                    pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        yield descriptor
    finally:
        os.close(descriptor)


@contextlib.contextmanager
def _held_file(path: Path, flags: int = os.O_RDONLY, mode: int = 0o600):
    with _held_dir(path.parent) as parent:
        descriptor = os.open(path.name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, mode, dir_fd=parent)
        try:
            info = os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise ValueError("nonregular or linked managed file")
            yield descriptor
        finally:
            os.close(descriptor)


def _copy_held(source: Path, destination: Path) -> None:
    with _held_file(source) as input_fd, _held_dir(destination.parent, create=True) as parent:
        output_fd = os.open(destination.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        try:
            with os.fdopen(os.dup(input_fd), "rb") as inp, os.fdopen(os.dup(output_fd), "wb") as out:
                shutil.copyfileobj(inp, out, 1024 * 1024)
                out.flush()
            os.fsync(output_fd)
        finally:
            os.close(output_fd)
        os.fsync(parent)


def _read_held(path: Path, limit: int) -> bytes:
    with _held_file(path) as descriptor:
        with os.fdopen(os.dup(descriptor), "rb") as stream:
            data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("file exceeds read bound")
    return data


def _unlink_held(path: Path) -> None:
    with _held_dir(path.parent) as parent:
        info = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("unsafe managed target")
        os.unlink(path.name, dir_fd=parent)
        os.fsync(parent)


def _safe_tree(root: Path, base: Path) -> list[Path]:
    if base.is_symlink():
        raise ValueError("managed tree link is forbidden")
    if not base.exists():
        return []
    if base.is_symlink() or not base.is_dir():
        raise ValueError("managed tree is not a real directory")
    files = []
    for parent, dirs, names in os.walk(base, followlinks=False):
        for name in dirs:
            child = Path(parent) / name
            if child.is_symlink() or not child.is_dir():
                raise ValueError("managed directory is unsafe")
        for name in names:
            child = Path(parent) / name
            _regular(child)
            child.relative_to(root)
            files.append(child)
            if len(files) > MAX_ENTRIES:
                raise ValueError("managed file count exceeds bound")
    return sorted(files)


def _store_relative(root: Path, store_root: Path | None) -> str:
    expected = store_root or root / "data/workspace-packages"
    if expected.is_symlink():
        raise ValueError("package store link is forbidden")
    try:
        relative = expected.absolute().relative_to(root.absolute()).as_posix()
    except ValueError as error:
        raise ValueError("package store is outside data root") from error
    if relative in {".", "data", "export", "recovery"} or relative.startswith(("export/", "recovery/", "runtime/", "logs/", "cache/", "tmp/")):
        raise ValueError("package store overlaps reserved data")
    if relative == MUSIC_TREE or relative.startswith(MUSIC_TREE + "/") or MUSIC_TREE.startswith(relative + "/"):
        raise ValueError("package store overlaps managed audio")
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise ValueError("package store ancestor is a link")
    return _relative(relative)


def _root_binding(root: Path) -> str:
    return hashlib.sha256(str(root.absolute()).encode()).hexdigest()


MUSIC_TREE = "data/assets/music-audio"
MUSIC_RIGHTS = "LOCAL_USER_PROVIDED_UNVERIFIED"
MUSIC_PURPOSE = "LOCAL_USE_ONLY"


def _music_wav(path: Path) -> dict:
    raw = _read_held(path, 16_000_000)
    if not raw: raise ValueError("empty managed WAV")
    try:
        with wave.open(io.BytesIO(raw), "rb") as audio:
            if (audio.getcomptype() != "NONE" or not 1 <= audio.getnchannels() <= 2
                    or audio.getsampwidth() not in {1, 2, 3, 4} or not 8000 <= audio.getframerate() <= 192000):
                raise ValueError("unsupported managed PCM WAV")
            frames = audio.getnframes()
            if len(audio.readframes(frames)) != frames * audio.getnchannels() * audio.getsampwidth():
                raise ValueError("truncated managed WAV")
            duration = frames / audio.getframerate()
            if not 0 < duration <= 600: raise ValueError("managed WAV duration exceeds bound")
    except (wave.Error, EOFError, OverflowError) as error:
        raise ValueError("invalid managed WAV") from error
    digest = hashlib.sha256(raw).hexdigest()
    if path.name != digest + ".wav": raise ValueError("managed WAV name/hash mismatch")
    return {"sha256": digest, "source_sha256": digest, "size": len(raw), "duration": duration, "mime": "audio/wav"}


def _music_refs(conn, root: Path, tables: set, workspaces: list) -> list[dict]:
    if "runtime_entities" not in tables: return []
    rows = [dict(row) for row in conn.execute("select entity_id,tenant_id,company_id,workspace_id,parent_id,data_json from runtime_entities where entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.packageId')='com.curis.local.music'")]
    records = {(row["tenant_id"], row["entity_id"]): row for row in rows}
    payloads = {key: _bounded_json(row["data_json"].encode()) for key, row in records.items()}
    for data in payloads.values():
        if data.get("kind") == "AudioAssetVersion" and (data.get("rights"), data.get("purpose")) not in {("LOCAL_DESIGN_ONLY", "NONCOMMERCIAL_ISOLATED_TEST"), (MUSIC_RIGHTS, MUSIC_PURPOSE)}:
            raise ValueError("music audio provenance pair invalid")
    assets = [(key, data) for key, data in payloads.items() if data.get("kind") == "AudioAssetVersion" and data.get("rights") == MUSIC_RIGHTS]
    if not assets: return []  # preserve old no-music and legacy-sample archive semantics
    if len(assets) > 4096: raise ValueError("too many managed music references")
    workspace_keys = set(workspaces)
    def record(key, kind, scope, song=None):
        row = records.get(key); data = payloads.get(key, {})
        if (not row or data.get("kind") != kind or (row["tenant_id"], row["company_id"], row["workspace_id"]) != scope
                or data.get("packageVersion") not in {"0.1.0", "0.2.0"} or data.get("schemaVersion") != data.get("packageVersion") or data.get("objectType") != "MusicSong"):
            raise ValueError("music reference scope/type/version mismatch")
        body = {k: v for k, v in data.items() if k not in {"packageId", "packageVersion", "schemaVersion", "objectType", "kind", "payload_sha256", "song_ref"}}
        if data.get("payload_sha256") != hashlib.sha256(_canonical(body)).hexdigest(): raise ValueError("music reference payload changed")
        if kind == "Song":
            if row["parent_id"] != scope[2]: raise ValueError("music Song parent mismatch")
        elif row["parent_id"] != song or data.get("song_ref") != song:
            raise ValueError("music version parent mismatch")
        return data
    result = []
    for key, data in sorted(assets):
        row = records[key]; scope = (row["tenant_id"], row["company_id"], row["workspace_id"]); song = row["parent_id"]
        if scope not in workspace_keys: raise ValueError("music Workspace absent")
        record((key[0], song), "Song", scope)
        asset = record(key, "AudioAssetVersion", scope, song)
        if asset.get("purpose") != MUSIC_PURPOSE: raise ValueError("managed audio purpose mismatch")
        if "workspace_package_instances" not in tables: raise ValueError("music package identity absent")
        package = conn.execute("select package_id,package_version,package_digest from workspace_package_instances where tenant_id=? and company_id=? and workspace_id=?", scope).fetchall()
        if len(package) != 1 or tuple(package[0]) != ("com.curis.local.music", data["packageVersion"], "cb05fd21e4237d046e20f0b96a81f6894e71caee95c2b0c6559b91ecf56ec802" if data["packageVersion"] == "0.2.0" else "5d9f36c36c2461f4540ad59277b56447a1a67cb2953759f43c52afbe5ed2cf76"):
            raise ValueError("managed music package identity mismatch")
        digest = asset.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest): raise ValueError("managed audio hash invalid")
        relative = MUSIC_TREE + "/" + digest + ".wav"
        actual = _music_wav(root / relative)
        if any(asset.get(k) != value for k, value in actual.items()): raise ValueError("music Asset/WAV metadata mismatch")
        result.append({"tenant_id": key[0], "company_id": row["company_id"], "workspace_id": row["workspace_id"], "song_ref": song, "asset_ref": key[1], "path": relative, **actual, "rights": MUSIC_RIGHTS, "purpose": MUSIC_PURPOSE})
    # Every local-use Candidate/Choice/Master/Release must resolve within the same
    # Song and retain the exact verified asset basis, never a foreign identifier.
    references = {"lyrics_ref": "LyricsVersion", "production_ref": "ProductionVersion", "candidate_ref": "Candidate", "asset_ref": "AudioAssetVersion", "choice_ref": "Choice", "master_ref": "MasterRevision"}
    for key, data in payloads.items():
        if data.get("kind") not in {"Candidate", "Choice", "MasterRevision", "ReleasePackage"}: continue
        row = records[key]; scope = (key[0], row["company_id"], row["workspace_id"]); song = row["parent_id"]
        body = record(key, data["kind"], scope, song)
        for field, kind in references.items():
            if body.get(field): record((key[0], body[field]), kind, scope, song)
        if data["kind"] in {"Choice", "MasterRevision"}:
            candidate = record((key[0], body["candidate_ref"]), "Candidate", scope, song)
            if any(body.get(field) != candidate.get(field) for field in ("asset_ref", "lyrics_ref", "production_ref")): raise ValueError("music candidate basis mismatch")
        if data["kind"] == "MasterRevision":
            asset = record((key[0], body["asset_ref"]), "AudioAssetVersion", scope, song)
            if body.get("rights") != asset.get("rights"): raise ValueError("music Master rights mismatch")
        if data["kind"] == "ReleasePackage":
            master = record((key[0], body["master_ref"]), "MasterRevision", scope, song)
            if body.get("rights") != master.get("rights") or body.get("status") != "LOCAL_PREPARATION_NOT_PUBLISHED": raise ValueError("music preparation rights/status mismatch")
    return result


CG_TREE = "data/assets/content-growth-media"


def _cg_file(path):
    name = path.name
    if not re.fullmatch(r"[0-9a-f]{64}\.(png|jpg|wav|mp4)", name): raise ValueError("unknown CG media filename")
    limit = {"png":20*1024*1024,"jpg":20*1024*1024,"wav":16_000_000,"mp4":128*1024*1024}[path.suffix[1:]]
    value = _regular(path)
    if value.st_nlink != 1 or not 0 < value.st_size <= limit: raise ValueError("invalid CG media regular file")
    raw = _read_held(path, limit)
    if hashlib.sha256(raw).hexdigest() != name.split(".")[0]: raise ValueError("CG media hash mismatch")
    mime = {"png":"image/png","jpg":"image/jpeg","wav":"audio/wav","mp4":"video/mp4"}[path.suffix[1:]]
    if mime == "image/png" and not raw.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError("CG PNG signature mismatch")
    if mime == "image/jpeg" and not (raw.startswith(b"\xff\xd8") and raw.endswith(b"\xff\xd9")): raise ValueError("CG JPEG signature mismatch")
    if mime == "audio/wav": _music_wav(path)
    if mime == "video/mp4" and raw[4:8] != b"ftyp": raise ValueError("CG MP4 signature mismatch")
    return {"sha256":name.split(".")[0],"size":len(raw),"mime":mime,"extension":path.suffix[1:]}


def _companion_refs(conn, root, tables, workspaces):
    if "runtime_entities" not in tables: return []
    rows = [dict(r) for r in conn.execute("select entity_id,tenant_id,company_id,workspace_id,parent_id,data_json from runtime_entities where entity_type='PACKAGE_DOMAIN_OBJECT' and json_extract(data_json,'$.schemaVersion') in ('writing.book-context/v1','cg.operating-context/v1','cg.local-media/v1')")]
    records = {r['entity_id']:(r,_bounded_json(r['data_json'].encode())) for r in rows}
    workspace_keys = set(workspaces)
    result = []
    def canonical_object(ref,kind,scope,parent=None):
        r=conn.execute("select tenant_id,company_id,workspace_id,parent_id,entity_type from runtime_entities where entity_id=?",(ref,)).fetchone()
        if not r or tuple(r[:3]) != (scope['tenant_id'],scope['company_id'],scope['workspace_id']) or r['entity_type']!=kind or parent is not None and r['parent_id']!=parent: raise ValueError("companion original object scope mismatch")
    def chapter(ref,book,scope):
        r=conn.execute("select data_json from workspace_package_objects where tenant_id=? and company_id=? and workspace_id=? and object_id=? and object_type='WritingChapter'",(scope['tenant_id'],scope['company_id'],scope['workspace_id'],ref)).fetchone()
        if not r or _bounded_json(r[0].encode()).get('bookRef')!=book: raise ValueError("book context chapter mismatch")
    def cg_version(ref,scope,content):
        if not isinstance(ref,str) or not ref or len(ref)>256: raise ValueError("CG original version identity invalid")
        canonical_object(ref,'CONTENT_VERSION',scope,content)
        row=conn.execute("select data_json from runtime_entities where entity_id=?",(ref,)).fetchone()
        value=_bounded_json(row[0].encode())
        if not isinstance(value,dict): raise ValueError("CG original version payload invalid")
        return value
    def cg_receipt(event_type,ref,scope,content):
        rows=conn.execute("select payload from evolution_events where tenant_id=? and correlation_id=? and event_type=? "
            "and (not json_valid(payload) or case when json_valid(payload) then json_extract(payload,'$.version_ref')=? else 0 end)",
            (scope['tenant_id'],content,event_type,ref)).fetchall()
        if len(rows)!=1: raise ValueError("CG inherited version receipt missing or ambiguous")
        value=_bounded_json(rows[0][0].encode())
        if not isinstance(value,dict) or value.get('version_ref')!=ref or not isinstance(value.get('request'),dict): raise ValueError("CG inherited version receipt invalid")
        return value
    def cg_context_origin(version_ref,context_ref,context,scope,content):
        origin=context.get('version_ref');original=cg_version(origin,scope,content)
        if original.get('kind') not in {'draft','adopted'}: raise ValueError("CG context origin version type invalid")
        seen=set();current=version_ref
        while current!=origin:
            if current in seen: raise ValueError("CG inherited context version cycle")
            seen.add(current);version=cg_version(current,scope,content)
            if version.get('kind')=='adopted':
                candidate_ref=version.get('source_candidate_ref');candidate=cg_version(candidate_ref,scope,content)
                receipt=cg_receipt('cg.content.adopted',current,scope,content)
                if (version.get('context_basis_ref')!=context_ref or candidate.get('kind')!='candidate'
                        or candidate.get('context_basis_ref')!=context_ref
                        or version.get('basis_version_ref')!=candidate.get('basis_version_ref')
                        or receipt['request'].get('candidate_ref')!=candidate_ref
                        or receipt['request'].get('expected_version_ref')!=version.get('basis_version_ref')):
                    raise ValueError("CG adopted context original candidate or receipt mismatch")
                current=version.get('basis_version_ref')
            elif version.get('kind')=='draft':
                receipt=cg_receipt('cg.content.saved',current,scope,content)
                if receipt.get('context_ref')!=context_ref: raise ValueError("CG inherited version context mismatch")
                current=receipt['request'].get('expected_version_ref')
            else: raise ValueError("CG inherited context version type invalid")
        # Even an explicit same-version binding must point to a scoped canonical original.
        cg_version(current,scope,content)
    for ref,(row,data) in records.items():
        scope=data.get('scope',{}); identity=(row['tenant_id'],row['company_id'],row['workspace_id'])
        if identity not in workspace_keys or identity != (scope.get('tenant_id'),scope.get('company_id'),scope.get('workspace_id')): raise ValueError("companion scope mismatch")
        schema=data['schemaVersion']
        if schema=='writing.book-context/v1':
            book=scope.get('book_ref');r=conn.execute("select 1 from workspace_package_objects where tenant_id=? and company_id=? and workspace_id=? and object_id=? and object_type='WritingBook'",(*identity,book)).fetchone()
            context=data.get('context')
            if not r or row['parent_id']!=book or not isinstance(context,dict) or data.get('payload_sha256')!=hashlib.sha256(_canonical(context)).hexdigest(): raise ValueError("book context source/hash invalid")
            items=context.get('items',[])
            if not isinstance(items,list) or len(items)>4096 or len(_canonical(context))>1024*1024: raise ValueError("book context limits exceeded")
            ids={i.get('id') for i in items if isinstance(i,dict) and isinstance(i.get('id'),str)}
            if len(ids)!=len(items): raise ValueError("book context item identity invalid")
            for item in items:
                if item.get('kind')=='chapter': chapter(item.get('chapter_ref'),book,scope)
                if item.get('parent') and item['parent'] not in ids: raise ValueError("book context parent absent")
                if any(v not in ids for k in ('character_refs','world_refs') for v in item.get(k,[])): raise ValueError("book context source absent")
            by_id={item['id']:item for item in items};ref_count=0
            parents={'outline':set(),'volume':{'outline'},'chapter':{'outline','volume'},'node':{'chapter'},'world':set(),'character':set(),'relationship':set()}
            for item in items:
                kind=item.get('kind');parent=item.get('parent','')
                if kind not in parents or parent and by_id[parent].get('kind') not in parents[kind]: raise ValueError("book context parent type invalid")
                visited={item['id']};cursor=parent
                while cursor:
                    if cursor in visited: raise ValueError("book context parent cycle")
                    visited.add(cursor);cursor=by_id[cursor].get('parent','')
                for key,wanted in [('character_refs','character'),('world_refs','world')]:
                    refs=item.get(key,[])
                    if not isinstance(refs,list) or len(set(refs))!=len(refs) or any(by_id[r].get('kind')!=wanted for r in refs): raise ValueError("book context typed source invalid")
                    ref_count+=len(refs)
                ref_count+=len(item.get('direction_refs',[]))+bool(parent)
                if kind=='relationship':
                    a,b=item.get('from_character'),item.get('to_character')
                    if a==b or any(by_id.get(r,{}).get('kind')!='character' for r in (a,b)): raise ValueError("book relationship endpoint invalid")
                    ref_count+=2
            if ref_count>16384: raise ValueError("book context reference limit exceeded")
        else:
            payload=data.get('payload')
            if not isinstance(payload,dict) or data.get('payload_sha256')!=hashlib.sha256(_canonical(payload)).hexdigest(): raise ValueError("CG companion payload mismatch")
            if schema=='cg.local-media/v1':
                content=data.get('content_ref');canonical_object(content,'CONTENT_ITEM',scope)
                canonical_object(payload.get('version_ref'),'CONTENT_VERSION',scope,content)
                if data.get('rights')!='LOCAL_USER_PROVIDED_UNVERIFIED' or data.get('purpose')!='LOCAL_USE_ONLY': raise ValueError("CG media provenance invalid")
                if data.get('kind')=='Asset':
                    media=payload.get('media',{});rel=CG_TREE+'/'+str(media.get('sha256'))+'.'+str(media.get('extension'))
                    checked=_cg_file(root/rel)
                    if any(checked[k]!=media.get(k) for k in checked): raise ValueError("CG asset metadata mismatch")
                    result.append({'ref':ref,'path':rel,'sha256':checked['sha256']})
                elif data.get('kind') in {'Candidate','Adoption'}:
                    target=records.get(payload.get('asset_ref'))
                    if not target or target[0]['parent_id']!=content or target[1].get('kind')!='Asset' or target[1].get('scope')!=scope: raise ValueError("CG candidate asset mismatch")
                    if payload.get('context_ref'):
                        target=records.get(payload['context_ref'])
                        if not target or target[1].get('schemaVersion')!='cg.operating-context/v1' or target[1].get('objectType')!='CGManualContext' or target[1].get('kind')!='Context' or target[1].get('scope')!=scope or target[1]['payload']['content_ref']!=content: raise ValueError("CG candidate context mismatch")
                        cg_context_origin(payload['version_ref'],payload['context_ref'],target[1]['payload'],scope,content)
                    if data['kind']=='Adoption':
                        target=records.get(payload.get('candidate_ref'))
                        if not target or target[1].get('kind')!='Candidate' or target[1].get('scope')!=scope or target[1]['payload']['asset_ref']!=payload['asset_ref']: raise ValueError("CG adoption candidate mismatch")
                else: raise ValueError("unknown CG media kind")
            else:
                for original in data.get('basis',[]):
                    if original.get('kind')=='AccountObservation':
                        r=conn.execute("select tenant_id,company_id,data_json from runtime_entities where entity_id=?",(original['ref'],)).fetchone()
                        if not r or r['tenant_id']!=scope['tenant_id'] or r['company_id']!=scope['company_id'] or hashlib.sha256(_canonical(_bounded_json(r['data_json'].encode()))).hexdigest()!=original['sha256']: raise ValueError("CG report observation mismatch")
                    else:
                        target=records.get(original.get('ref'))
                        if not target or target[1].get('scope')!=scope or target[1].get('payload_sha256')!=original.get('sha256'): raise ValueError("CG original context mismatch")
    if 'evolution_events' in tables:
        for row in conn.execute("select payload from evolution_events where event_type like 'writing.chapter.%'"):
            event=_bounded_json(row[0].encode());out=event.get('output',{})
            basis=out.get('book_context_basis') or out.get('draft',{}).get('book_context_basis') or out.get('snapshot',{}).get('book_context_basis')
            if basis:
                target=records.get(basis.get('context_ref'));scope=event.get('scope',{})
                if not target or target[1].get('scope')!={**scope,'chapter_ref':''} or target[1]['payload_sha256']!=basis.get('context_sha256') or basis.get('book_ref')!=scope.get('book_ref') or basis.get('chapter_ref')!=scope.get('chapter_ref'): raise ValueError("chapter context basis source mismatch")
                original={v['id']:v for v in target[1]['context']['items']}
                if any(v!=original.get(v.get('id')) for v in basis.get('items',[])): raise ValueError("chapter basis snapshot mismatch")
    return sorted(result,key=lambda r:r['ref'])


class PackageFilesDamaged(ValueError):
    """Registered, safely scoped package bytes disagree with the readable DB."""

    def __init__(self, damage: list[dict]):
        self.damage = damage
        super().__init__("managed package files are damaged")


def _schema_and_refs(db: Path, root: Path, store_rel: str, reference_root: Path | None = None,
                     *, allow_package_damage: bool = False) -> dict:
    reference_root = reference_root or root
    conn = sqlite3.connect(f"file:{db.absolute()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        if conn.execute("pragma integrity_check").fetchone()[0] != "ok":
            raise ValueError("database integrity failed")
        if conn.execute("pragma foreign_key_check").fetchone():
            raise ValueError("database foreign keys failed")
        tables = {row[0] for row in conn.execute("select name from sqlite_master where type='table'")}
        required = {"companies", "workspaces", "employee_instances", "installed_workspace_packages"}
        if not required <= tables:
            raise ValueError("required identity/reference tables absent")
        identity = [dict(row) for row in conn.execute("select tenant_id, company_id from companies order by tenant_id, company_id")]
        if not identity:
            raise ValueError("company identity absent")
        owners = [tuple(row) for row in conn.execute("select tenant_id,company_id,ceo_id from companies order by tenant_id,company_id")]
        if any(tenant != "selfuse" or owner != "selfuse-ceo" for tenant, _, owner in owners):
            raise ValueError("local owner identity is incompatible")
        workspaces = [tuple(row) for row in conn.execute("select tenant_id,company_id,workspace_id from workspaces order by tenant_id,company_id,workspace_id")]
        employees = [tuple(row) for row in conn.execute("select tenant_id,company_id,id from employee_instances order by tenant_id,company_id,id")]
        company_keys = {(tenant, company) for tenant, company, _ in owners}
        if any((tenant, company) not in company_keys for tenant, company, _ in workspaces + employees):
            raise ValueError("workspace or employee company identity mismatch")
        owner_digest = hashlib.sha256(_canonical(owners)).hexdigest()
        lineage_digest = hashlib.sha256(_canonical({"owners": owners, "workspaces": workspaces, "employees": employees})).hexdigest()
        avatars = []
        for row in conn.execute("select tenant_id,id,avatar_ref from employee_instances where avatar_ref like 'asset:%'"):
            ref = str(row["avatar_ref"])
            match = re.fullmatch(r"asset:([0-9a-f]{64})\.(png|jpg|webp)", ref)
            if not match:
                raise ValueError("invalid avatar reference")
            tenant = hashlib.sha256(str(row["tenant_id"]).encode()).hexdigest()[:20]
            employee = hashlib.sha256(str(row["id"]).encode()).hexdigest()[:24]
            rel = f"data/assets/employee-avatars/{tenant}/{employee}/{match[1]}.{match[2]}"
            path = root / rel
            if not path.is_file() or _sha256(path) != match[1]:
                raise ValueError("avatar reference is missing or invalid")
            avatars.append(rel)
        packages = []
        package_damage = []
        for row in conn.execute("select stored_path,digest,status from installed_workspace_packages where status != 'UNINSTALLED'"):
            stored = Path(str(row["stored_path"]))
            try:
                rel = stored.relative_to(reference_root / store_rel)
            except ValueError as error:
                raise ValueError("installed package path outside active store") from error
            _relative(rel.as_posix())
            if not re.fullmatch(r"[0-9a-f]{64}", str(row["digest"])):
                raise ValueError("invalid installed package digest")
            package_dir = root / store_rel / rel
            ref = package_dir.relative_to(root).as_posix()
            packages.append(ref)
            try:
                with _held_dir(package_dir):
                    pass
            except FileNotFoundError:
                package_damage.append({"path": ref, "reason": "PACKAGE_MISSING"})
                continue
            entries = _safe_tree(root, package_dir)
            digest = hashlib.sha256()
            for file in entries:
                name = file.relative_to(package_dir).as_posix()
                digest.update(name.encode()); digest.update(b"\0")
                with _held_file(file) as descriptor:
                    with os.fdopen(os.dup(descriptor), "rb") as stream:
                        for chunk in iter(lambda: stream.read(1024 * 1024), b""): digest.update(chunk)
                digest.update(b"\0")
            if digest.hexdigest() != row["digest"]:
                package_damage.append({"path": ref, "reason": "PACKAGE_DIGEST_MISMATCH"})
        # Inspect only structured field names, never print values or arbitrary body/prompt text.
        forbidden = re.compile(r"(?:api[_-]?key|password|access[_-]?token|refresh[_-]?token|secret|private[_-]?key|cookie)", re.I)
        def inspect_keys(value, level=0):
            if level > 24:
                raise ValueError("structured metadata nesting exceeds bound")
            if isinstance(value, dict):
                for key, child in value.items():
                    if forbidden.search(str(key)) and key not in {"secret_digest", "credential_ref_digest"}:
                        raise ValueError("forbidden structured secret key present")
                    inspect_keys(child, level + 1)
            elif isinstance(value, list):
                for child in value:
                    inspect_keys(child, level + 1)
        for table in tables:
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
                raise ValueError("unsafe table name")
            for column in conn.execute(f'pragma table_info("{table}")'):
                name = str(column[1])
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
                    raise ValueError("unsafe column name")
                if forbidden.search(name) and name not in {"secret_digest", "credential_ref_digest"}:
                    count = conn.execute(f'select count(*) from "{table}" where "{name}" is not null and length("{name}") > 0').fetchone()[0]
                    if count:
                        raise ValueError("forbidden secret-shaped database field present")
                # These two producers persist JSON in a plain `payload` column.
                # Do not interpret arbitrary user prose columns as structured JSON.
                structured_payload = (table, name) in {
                    ("evolution_events", "payload"),
                    ("agent_wakeup_requests", "payload"),
                }
                if name.endswith("_json") or name in {"encrypted_metadata", "metadata"} or structured_payload:
                    for (raw,) in conn.execute(f'select "{name}" from "{table}" where "{name}" is not null'):
                        if len(str(raw).encode()) > MAX_MANIFEST:
                            raise ValueError("structured metadata exceeds bound")
                        try:
                            inspect_keys(_strict_json(str(raw).encode()))
                        except (TypeError, json.JSONDecodeError) as error:
                            raise ValueError("structured metadata is invalid") from error
        if "credential_metadata" in tables:
            expected = {"credential_id", "tenant_id", "name", "provider", "credential_type",
                        "credential_ref", "status", "encrypted_metadata", "created_at", "updated_at", "disabled_at",
                        "account_id"}
            actual = {str(row[1]) for row in conn.execute('pragma table_info("credential_metadata")')}
            if actual - expected:
                raise ValueError("unreviewed credential metadata schema")
            for (raw,) in conn.execute("select encrypted_metadata from credential_metadata"):
                value = _bounded_json(str(raw).encode())
                if set(value) - {"backend", "secret_digest"}:
                    raise ValueError("unreviewed credential metadata field")
        schema = sorted((str(row[0]), str(row[1]), str(row[2] or "")) for row in
                        conn.execute("select type,name,sql from sqlite_master where name not like 'sqlite_%'"))
        music_refs = _music_refs(conn, root, tables, workspaces)
        companion_refs = _companion_refs(conn, root, tables, workspaces)
        # Damage never skips later identity, metadata or business-reference checks.
        if package_damage and not allow_package_damage:
            raise PackageFilesDamaged(package_damage)
        return {**({"packageDamage": package_damage} if package_damage else {}), **({"cgMediaRefs": companion_refs} if companion_refs else {}), **({"musicRefs": music_refs} if music_refs else {}), "schemaVersion": int(conn.execute("pragma user_version").fetchone()[0]),
                "schemaFingerprint": hashlib.sha256(_canonical(schema)).hexdigest(),
                "ownerDigest": owner_digest, "lineageDigest": lineage_digest,
                "identity": identity, "avatarRefs": sorted(set(avatars)), "packageRefs": sorted(set(packages))}
    finally:
        conn.close()


def _managed_files(root: Path, store_rel: str, *, require_db: bool = True) -> list[Path]:
    db = root / DB_ENTRY
    if db.exists() or db.is_symlink():
        _regular(db)
        files = [db]
    elif require_db:
        raise FileNotFoundError("active database is missing")
    else:
        files = []
    for entry in root.iterdir():
        name = entry.name
        if name in EXCLUDED_ROOTS:
            if entry.is_symlink() or not entry.is_dir():
                raise ValueError("excluded runtime namespace is unsafe")
            continue
        if name == "curis-desktop.lock":
            _regular(entry)
            continue
        if name in {"data", "export"}:
            continue
        if store_rel.split("/")[0] == name:
            continue
        raise ValueError("unknown data-root entry")
    data = root / "data"
    if data.is_symlink() or not data.is_dir():
        raise ValueError("data directory is unsafe")
    allowed_data = {"curis.sqlite", "assets"}
    if store_rel.startswith("data/"):
        allowed_data.add(store_rel.split("/")[1])
    for entry in data.iterdir():
        if entry.name in EXCLUDED_DATA or re.fullmatch(r"curis\.sqlite\.pre-restore-[0-9TZ]+", entry.name):
            _regular(entry)
            continue
        if entry.name in allowed_data:
            continue
        raise ValueError("unknown data directory entry")
    avatar_root = root / "data/assets/employee-avatars"
    assets = root / "data/assets"
    if assets.is_symlink():
        raise ValueError("asset tree link is forbidden")
    if assets.exists():
        allowed_assets = {avatar_root, root / MUSIC_TREE, root / CG_TREE}
        if store_rel.startswith("data/assets/"):
            allowed_assets.add(root / "data/assets" / store_rel.split("/")[2])
        for entry in assets.iterdir():
            if entry not in allowed_assets:
                raise ValueError("unknown asset tree")
    store_parts = PurePosixPath(store_rel).parts
    ancestor = root
    for index, part in enumerate(store_parts[:-1]):
        ancestor = ancestor / part
        if ancestor.exists() and (ancestor.is_symlink() or not ancestor.is_dir()):
            raise ValueError("package store ancestor is unsafe")
        if ancestor.exists():
            allowed = {store_parts[index + 1]}
            if index == 0 and part == "data":
                # These exact SQLite sidecars were already regular-file checked
                # above; raw safety must retain them beside the package store.
                allowed |= allowed_data | EXCLUDED_DATA
            if index == 1 and store_parts[:2] == ("data", "assets"):
                allowed |= {"employee-avatars", "music-audio", "content-growth-media"}
            if {x.name for x in ancestor.iterdir()} - allowed:
                raise ValueError("unknown sibling of package store")
    for base in (avatar_root, root / MUSIC_TREE, root / CG_TREE, root / store_rel, root / "export"):
        files.extend(_safe_tree(root, base))
    if len(files) > MAX_ENTRIES or any(file.stat().st_size > MAX_MEMBER for file in files) or sum(file.stat().st_size for file in files) > MAX_TOTAL:
        raise ValueError("managed data exceeds bound")
    return sorted(set(files))


def _raw_rows(root: Path, store_rel: str) -> list[dict]:
    files = _managed_files(root, store_rel, require_db=False)
    for suffix in ("-wal", "-shm", "-journal"):
        sidecar = root / "data" / ("curis.sqlite" + suffix)
        if sidecar.exists() or sidecar.is_symlink():
            _regular(sidecar)
            files.append(sidecar)
    rows = [{"path": path.relative_to(root).as_posix(), "bytes": _regular(path).st_size,
             "sha256": _sha256(path)} for path in sorted(set(files))]
    if len(rows) > MAX_ENTRIES or any(row["bytes"] > MAX_MEMBER for row in rows) or sum(row["bytes"] for row in rows) > MAX_TOTAL:
        raise ValueError("raw current state exceeds preservation bound")
    return rows


def _raw_generation(mode: str, rows: list[dict]) -> str:
    return hashlib.sha256(_canonical({"mode": mode, "rows": rows})).hexdigest()


def _observed_state(root: Path, store_rel: str) -> dict:
    db = root / DB_ENTRY
    if not db.exists() and not db.is_symlink():
        rows = _raw_rows(root, store_rel)
        return {"mode": "MISSING_DB", "rows": rows, "generation": _raw_generation("MISSING_DB", rows), "refs": None}
    _regular(db)
    try:
        with tempfile.TemporaryDirectory(prefix="db-probe-", dir=_recovery_dir(root)) as raw:
            probe = Path(raw) / DB_ENTRY
            _copy_held(db, probe)
            for suffix in ("-wal", "-shm", "-journal"):
                sidecar = db.with_name(db.name + suffix)
                if sidecar.exists() or sidecar.is_symlink():
                    _copy_held(sidecar, probe.with_name(probe.name + suffix))
            _verify_db(probe)
    except (sqlite3.DatabaseError, ValueError):
        rows = _raw_rows(root, store_rel)
        return {"mode": "DAMAGED_DB", "rows": rows, "generation": _raw_generation("DAMAGED_DB", rows), "refs": None}
    refs, _, _ = _generation(root, store_rel, allow_package_damage=True)
    rows = _raw_rows(root, store_rel)
    mode = "DAMAGED_PACKAGE_FILES" if refs.get("packageDamage") else "HEALTHY"
    return {"mode": mode, "rows": rows, "generation": _raw_generation(mode, rows), "refs": refs}


def _validate_cg_export(payload: dict) -> None:
    # Match Native validate_cg_export's saved projection; recovery has no live UI selection.
    fields = {"package_type", "verification_ref", "exported_at", "title", "body", "format",
              "platform", "account", "checks", "connection_status", "verification", "source", "notice"}
    if (set(payload) != fields or payload["package_type"] != "curis.cg.local-verification-export/1"
            or payload["notice"] != "本地核验导出，不构成发布；平台连接不存在。"
            or payload["verification"] != "UNVERIFIED" or payload["source"] != "CEO_MANUAL"
            or payload["connection_status"] != "NOT_CONNECTED"):
        raise ValueError("CG export contract is invalid")

    def text(value, limit, nonempty=True):
        return isinstance(value, str) and len(value) <= limit and (not nonempty or bool(value))

    if (not text(payload["verification_ref"], 256) or not payload["verification_ref"].startswith("cg-verify-")
            or not text(payload["exported_at"], 128)
            or any(not isinstance(payload[key], str) for key in ("title", "body", "format"))):
        raise ValueError("CG export fields are invalid")
    for key in ("account", "platform"):
        item = payload[key]
        if (not isinstance(item, dict) or set(item) != {"ref", "name"}
                or not text(item["ref"], 256) or not text(item["name"], 2000)):
            raise ValueError("CG export fields are invalid")
    if (not payload["account"]["ref"].startswith("cg-account-")
            or payload["platform"]["ref"] not in {"xhs", "douyin", "wechat_oa", "tiktok", "youtube", "bilibili"}):
        raise ValueError("CG export fields are invalid")
    checks = payload["checks"]
    if not isinstance(checks, list) or not 1 <= len(checks) <= 64:
        raise ValueError("CG export checks are invalid")
    keys = set()
    for item in checks:
        if (not isinstance(item, dict) or set(item) != {"key", "label", "checked", "note"}
                or not text(item["key"], 256) or not text(item["label"], 2000)
                or not isinstance(item["checked"], bool) or not text(item["note"], 2000, False)
                or item["key"] in keys):
            raise ValueError("CG export checks are invalid")
        keys.add(item["key"])


def _inventory(root: Path, db: Path, store_rel: str, files: list[Path], reference_root: Path | None = None,
               *, allow_package_damage: bool = False) -> tuple[dict, list[dict]]:
    refs = _schema_and_refs(db, root, store_rel, reference_root, allow_package_damage=True)
    rows = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel.startswith("export/"):
            if path.suffix != ".json" or _regular(path).st_size > 2 * 1024 * 1024:
                raise ValueError("export is not a validated local JSON")
            payload = _bounded_json(_read_held(path, 2 * 1024 * 1024))
            if "package_type" in payload:
                _validate_cg_export(payload)
            elif payload.get("schema_version") != "writing.local-package/v1" or payload.get("metadata", {}).get("target") != "LOCAL_DOWNLOAD":
                raise ValueError("export contract is invalid")
        rows.append({"path": rel, "bytes": _regular(path).st_size, "sha256": _sha256(path)})
    music_files = [row for row in rows if row["path"].startswith(MUSIC_TREE + "/")]
    if len(music_files) > 64 or sum(row["bytes"] for row in music_files) > 256 * 1024 * 1024:
        raise ValueError("managed audio exceeds retention bound")
    for row in music_files:
        # Retain and validate bounded finalized orphans after failed registration;
        # no Asset identifier means they are never served by the business API.
        if len(PurePosixPath(row["path"]).parts) != 4: raise ValueError("unknown music asset subtree")
        _music_wav(root / row["path"])
    cg_files = [row for row in rows if row["path"].startswith(CG_TREE + "/")]
    if len(cg_files) > 128 or sum(row["bytes"] for row in cg_files) > 128 * 1024 * 1024:
        raise ValueError("managed CG media exceeds retained quota")
    for row in cg_files:
        if len(PurePosixPath(row["path"]).parts) != 4: raise ValueError("unknown CG media subtree")
        _cg_file(root / row["path"])
    avatar_files = {row["path"] for row in rows if row["path"].startswith("data/assets/employee-avatars/")}
    if avatar_files != set(refs["avatarRefs"]):
        raise ValueError("avatar file/reference mismatch")
    package_files = {row["path"] for row in rows if row["path"].startswith(store_rel + "/")}
    damaged_refs = {item["path"] for item in refs.get("packageDamage", [])}
    for ref in refs["packageRefs"]:
        if ref not in damaged_refs and not any(name.startswith(ref + "/") for name in package_files):
            raise ValueError("package file/reference mismatch")
    if package_files and any(not any(name.startswith(ref + "/") for ref in refs["packageRefs"]) for name in package_files):
        raise ValueError("unreferenced package file")
    if damaged_refs and not allow_package_damage:
        raise PackageFilesDamaged(refs["packageDamage"])
    return refs, rows


def _generation(root: Path, store_rel: str, *, allow_package_damage: bool = False) -> tuple[dict, list[dict], str]:
    with tempfile.TemporaryDirectory(prefix="generation-", dir=_recovery_dir(root)) as raw:
        refs, rows = _snapshot_files(root, Path(raw) / "payload", store_rel, allow_package_damage=allow_package_damage)
        return refs, rows, hashlib.sha256(_canonical(rows)).hexdigest()


def _recovery_dir(root: Path) -> Path:
    path = root / "recovery"
    if path.exists() and (path.is_symlink() or not path.is_dir()):
        raise ValueError("recovery namespace is unsafe")
    path.mkdir(mode=0o700, exist_ok=True)
    return path


def _fsync_dir(path: Path) -> None:
    with _held_dir(path) as descriptor:
        os.fsync(descriptor)


def _write_json(path: Path, value: dict) -> None:
    with _held_file(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL) as descriptor:
        with os.fdopen(os.dup(descriptor), "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            stream.flush()
        os.fsync(descriptor)
    _fsync_dir(path.parent)


def _replace_json(path: Path, value: dict) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{secrets.token_hex(16)}")
    try:
        _write_json(temporary, value)
        with _held_dir(path.parent) as parent:
            os.replace(temporary.name, path.name, src_dir_fd=parent, dst_dir_fd=parent)
            os.fsync(parent)
    finally:
        try: _unlink_held(temporary)
        except FileNotFoundError: pass


def _lineage_record(root: Path, store_rel: str, refs: dict) -> dict:
    return {"format": "curis.recovery-lineage/v1", "rootBindingSha256": _root_binding(root),
            "packageStoreRelative": store_rel, "appVersion": APP_VERSION,
            "ownerDigest": refs["ownerDigest"]}


def _read_lineage(root: Path, store_rel: str) -> dict:
    value = _bounded_json(_read_held(root / "recovery/lineage.json", MAX_MANIFEST))
    if (set(value) != {"format", "rootBindingSha256", "packageStoreRelative", "appVersion", "ownerDigest"}
            or value["format"] != "curis.recovery-lineage/v1"
            or value["rootBindingSha256"] != _root_binding(root)
            or value["packageStoreRelative"] != store_rel or value["appVersion"] != APP_VERSION
            or not re.fullmatch(r"[0-9a-f]{64}", str(value["ownerDigest"]))):
        raise ValueError("local recovery lineage is incompatible")
    return value


def _ensure_lineage(root: Path, store_rel: str, refs: dict) -> dict:
    expected = _lineage_record(root, store_rel, refs)
    path = _recovery_dir(root) / "lineage.json"
    try:
        current = _read_lineage(root, store_rel)
    except FileNotFoundError:
        _write_json(path, expected)
        current = _read_lineage(root, store_rel)
    if current != expected:
        raise ValueError("current Company lineage differs from prior backup")
    return current


def _snapshot_files(root: Path, destination: Path, store_rel: str, *, allow_package_damage: bool = False) -> tuple[dict, list[dict]]:
    files = _managed_files(root, store_rel)
    for file in files:
        relative = file.relative_to(root)
        target = destination / relative
        if relative.as_posix() == DB_ENTRY:
            raw_db = destination / "recovery-db/curis.sqlite"
            _copy_held(file, raw_db)
            wal = file.with_name(file.name + "-wal")
            if wal.exists() or wal.is_symlink():
                _copy_held(wal, raw_db.with_name(raw_db.name + "-wal"))
            source = sqlite3.connect(f"file:{raw_db.absolute()}?mode=ro", uri=True)
            target.parent.mkdir(parents=True, exist_ok=True)
            copy = sqlite3.connect(target)
            try: source.backup(copy)
            finally: copy.close(); source.close()
            _fsync_dir(target.parent)
            shutil.rmtree(destination / "recovery-db")
        else:
            before = _sha256(file)
            _copy_held(file, target)
            if _sha256(file) != before or _sha256(target) != before:
                raise ValueError("managed file changed during snapshot")
    staged = _managed_files(destination, store_rel)
    return _inventory(destination, destination / DB_ENTRY, store_rel, staged, root, allow_package_damage=allow_package_damage)


def backup_v2(data_root: Path, output: Path, store_root: Path | None = None) -> dict:
    root = data_root.absolute()
    if root.is_symlink() or not root.is_dir():
        raise ValueError("data root is unsafe")
    store_rel = _store_relative(root, store_root)
    if (root / "recovery/active.json").exists():
        raise ValueError("unfinished recovery blocks backup")
    if output.exists() or output.is_symlink() or output.absolute().is_relative_to(root):
        raise ValueError("backup destination is occupied or inside active root")
    parent = output.parent
    with _held_dir(parent):
        pass
    with tempfile.TemporaryDirectory(prefix="stage-", dir=_recovery_dir(root)) as raw:
        staged = Path(raw) / "payload"
        staged.mkdir()
        refs, rows = _snapshot_files(root, staged, store_rel)
        _ensure_lineage(root, store_rel, refs)
        manifest = {"format": FULL_FORMAT, "createdAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "schemaVersion": refs["schemaVersion"], "schemaFingerprint": refs["schemaFingerprint"],
                    "backupProtocol": 2, "appVersion": APP_VERSION, "identity": refs["identity"],
                    "ownerDigest": refs["ownerDigest"], "lineageDigest": refs["lineageDigest"],
                    "rootBindingSha256": _root_binding(root), "packageStoreRelative": store_rel,
                    "files": rows, "avatarRefs": refs["avatarRefs"], "packageRefs": refs["packageRefs"],
                    "excluded": ["KEYCHAIN", "CREDENTIAL", "COOKIE", "BROWSER_PROFILE", "EXTERNAL_KNOWLEDGE", "EXTERNAL_MEDIA", "CACHE", "LOGS", "RUNTIME", "SAFETY_POINTS"]}
        if refs.get("musicRefs"): manifest["musicRefs"] = refs["musicRefs"]
        if refs.get("cgMediaRefs"): manifest["cgMediaRefs"] = refs["cgMediaRefs"]
        manifest["contentDigest"] = hashlib.sha256(_canonical(manifest)).hexdigest()
        raw_manifest = _canonical(manifest)
        if len(raw_manifest) > MAX_MANIFEST:
            raise ValueError("manifest exceeds bound")
        with _held_dir(parent) as parent_fd:
            temporary = ".curis-v2-" + secrets.token_hex(16)
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent_fd)
            temporary_exists = True
            try:
                with os.fdopen(fd, "wb") as stream:
                    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
                        archive.writestr(MANIFEST_ENTRY, raw_manifest)
                        for row in rows:
                            with _held_file(staged / row["path"]) as source_fd:
                                with os.fdopen(os.dup(source_fd), "rb") as source, archive.open(row["path"], "w") as sink:
                                    shutil.copyfileobj(source, sink, 1024 * 1024)
                    stream.flush(); os.fsync(stream.fileno())
                staged_stat = os.stat(temporary, dir_fd=parent_fd, follow_symlinks=False)
                if staged_stat.st_size > MAX_ARCHIVE:
                    raise ValueError("archive exceeds bound")
                os.link(temporary, output.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd, follow_symlinks=False)
                os.unlink(temporary, dir_fd=parent_fd)
                temporary_exists = False
                os.fsync(parent_fd)
                # The published name, rather than only the staged inode, is the
                # user-facing backup. Read its manifest and every member back.
                before = os.stat(output.name, dir_fd=parent_fd, follow_symlinks=False)
                if (before.st_dev, before.st_ino, before.st_size) != (staged_stat.st_dev, staged_stat.st_ino, staged_stat.st_size):
                    raise ValueError("published backup identity changed")
                published_sha = _sha256(output)
                with tempfile.TemporaryDirectory(prefix="readback-", dir=_recovery_dir(root)) as readback:
                    verified_manifest, verified_rows = _extract_v2(output, Path(readback))
                after = os.stat(output.name, dir_fd=parent_fd, follow_symlinks=False)
                final_sha = _sha256(output)
                final_stat = os.stat(output.name, dir_fd=parent_fd, follow_symlinks=False)
                if (verified_manifest != manifest or verified_rows != rows
                        or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
                        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
                        or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
                        != (final_stat.st_dev, final_stat.st_ino, final_stat.st_size, final_stat.st_mtime_ns)
                        or final_sha != published_sha):
                    raise ValueError("published backup read-back changed")
            finally:
                if temporary_exists:
                    os.unlink(temporary, dir_fd=parent_fd)
    return {"status": "BACKUP_VERIFIED", "archiveSha256": published_sha, "files": len(rows),
            "contentDigest": manifest["contentDigest"], "identity": refs["identity"],
            "createdAt": manifest["createdAt"], "appVersion": APP_VERSION,
            "schemaVersion": manifest["schemaVersion"],
            "archiveFile": {"device": final_stat.st_dev, "inode": final_stat.st_ino,
                            "bytes": final_stat.st_size, "mtimeNs": final_stat.st_mtime_ns}}


def _extract_v2(archive_path: Path, destination: Path, current_bytes: int = 0) -> tuple[dict, list[dict]]:
    _regular(archive_path)
    names = set(); folded = set(); total = 0
    with _held_file(archive_path) as archive_fd:
      archive_size = os.fstat(archive_fd).st_size
      if archive_size > MAX_ARCHIVE or archive_size < 22:
          raise ValueError("archive size is invalid")
      # Bound central-directory allocation before ZipFile constructs its entry list.
      os.lseek(archive_fd, max(0, archive_size - 65557), os.SEEK_SET)
      tail = os.read(archive_fd, min(65557, archive_size))
      marker = tail.rfind(b"PK\x05\x06")
      if marker < 0 or marker + 22 > len(tail):
          raise ValueError("ZIP end record missing")
      disk, central_disk, disk_entries, entries, central_bytes, central_offset, comment = struct.unpack_from("<HHHHIIH", tail, marker + 4)
      if (disk, central_disk) != (0, 0) or disk_entries != entries or entries > MAX_ENTRIES + 1 or entries == 0:
          raise ValueError("ZIP central entry count invalid")
      if entries == 0xffff or central_bytes == 0xffffffff or central_offset == 0xffffffff or central_bytes > 32 * 1024 * 1024:
          raise ValueError("ZIP central directory exceeds bound")
      if marker + 22 + comment != len(tail) or central_offset + central_bytes > archive_size:
          raise ValueError("ZIP central directory is inconsistent")
      os.lseek(archive_fd, 0, os.SEEK_SET)
      with os.fdopen(os.dup(archive_fd), "rb") as archive_stream, zipfile.ZipFile(archive_stream, "r") as archive:
        infos = archive.infolist()
        if not infos or len(infos) > MAX_ENTRIES + 1:
            raise ValueError("archive entry count invalid")
        for info in infos:
            name = _relative(info.filename)
            if name in names or name.casefold() in folded or info.is_dir():
                raise ValueError("duplicate, colliding or directory ZIP entry")
            names.add(name); folded.add(name.casefold())
            mode = (info.external_attr >> 16) & 0xffff
            kind = stat.S_IFMT(mode)
            if kind not in {0, stat.S_IFREG} or info.flag_bits & 0x1 or info.extra:
                raise ValueError("unsafe ZIP entry type")
            if info.file_size > MAX_MEMBER or (info.compress_size == 0 and info.file_size > 0):
                raise ValueError("ZIP member exceeds bound")
            if info.compress_size and info.file_size > info.compress_size * MAX_RATIO:
                raise ValueError("ZIP compression ratio exceeds bound")
            total += info.file_size
            if total > MAX_TOTAL:
                raise ValueError("ZIP expanded size exceeds bound")
        if MANIFEST_ENTRY not in names or archive.getinfo(MANIFEST_ENTRY).file_size > MAX_MANIFEST:
            raise ValueError("manifest missing or oversized")
        manifest = _bounded_json(archive.read(MANIFEST_ENTRY))
        digest = manifest.pop("contentDigest", None)
        if not isinstance(digest, str) or hashlib.sha256(_canonical(manifest)).hexdigest() != digest:
            raise ValueError("manifest content digest mismatch")
        manifest["contentDigest"] = digest
        if manifest.get("format") != FULL_FORMAT:
            raise ValueError("not a full v2 backup")
        rows = manifest.get("files")
        if not isinstance(rows, list) or not rows or len(rows) > MAX_ENTRIES:
            raise ValueError("manifest files invalid")
        declared = set()
        for row in rows:
            if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
                raise ValueError("manifest file row invalid")
            name = _relative(row["path"])
            if name in declared or not isinstance(row["bytes"], int) or row["bytes"] < 0 or row["bytes"] > MAX_MEMBER or not re.fullmatch(r"[0-9a-f]{64}", str(row["sha256"])):
                raise ValueError("manifest file value invalid")
            declared.add(name)
        if declared | {MANIFEST_ENTRY} != names or DB_ENTRY not in declared:
            raise ValueError("ZIP and manifest entries disagree")
        rough_required = 2 * current_bytes + 2 * total + 128 * 1024 * 1024
        if shutil.disk_usage(destination).free < rough_required:
            raise ValueError("insufficient space before archive extraction")
        for row in rows:
            target = destination / row["path"]
            with _held_dir(target.parent, create=True):
                pass
            digest_file = hashlib.sha256(); size = 0
            with archive.open(row["path"]) as source, _held_file(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL) as target_fd:
                with os.fdopen(os.dup(target_fd), "wb") as sink:
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        size += len(chunk)
                        if size > row["bytes"] or size > MAX_MEMBER:
                            raise ValueError("decompressed member exceeds bound")
                        digest_file.update(chunk); sink.write(chunk)
                    sink.flush()
                os.fsync(target_fd)
            if size != row["bytes"] or digest_file.hexdigest() != row["sha256"]:
                raise ValueError("archive member hash mismatch")
    return manifest, rows


def preflight_v2(data_root: Path, archive_path: Path, store_root: Path | None = None) -> dict:
    root = data_root.absolute()
    store_rel = _store_relative(root, store_root)
    if (root / "recovery/active.json").exists():
        raise ValueError("unfinished recovery blocks preflight")
    try:
        lineage = _read_lineage(root, store_rel)
    except FileNotFoundError as error:
        raise ValueError("local recovery lineage is missing") from error
    observed = _observed_state(root, store_rel)
    current_bytes = sum(row["bytes"] for row in observed["rows"])
    with tempfile.TemporaryDirectory(prefix="preflight-", dir=_recovery_dir(root)) as raw:
        stage = Path(raw)
        manifest, rows = _extract_v2(archive_path, stage, current_bytes)
        if manifest.get("rootBindingSha256") != _root_binding(root) or manifest.get("packageStoreRelative") != store_rel:
            raise ValueError("backup belongs to a different exact data root or package store")
        restored_refs, checked = _inventory(stage, stage / DB_ENTRY, store_rel, _managed_files(stage, store_rel), root)
        if manifest.get("cgMediaRefs", []) != restored_refs.get("cgMediaRefs", []):
            raise ValueError("CG media reference inventory mismatch")
        if (rows != checked or manifest.get("identity") != restored_refs["identity"]
                or manifest.get("ownerDigest") != lineage["ownerDigest"]
                or restored_refs["ownerDigest"] != lineage["ownerDigest"]
                or manifest.get("lineageDigest") != restored_refs["lineageDigest"]):
            raise ValueError("Company identity or file inventory mismatch")
        if (manifest.get("backupProtocol") != 2 or manifest.get("appVersion") != APP_VERSION
                or manifest.get("schemaVersion") != restored_refs["schemaVersion"]
                or manifest.get("schemaFingerprint") != restored_refs["schemaFingerprint"]):
            raise ValueError("app version or SQLite schema version is incompatible")
        if observed["refs"] is not None:
            current_refs = observed["refs"]
            if (current_refs["identity"] != restored_refs["identity"]
                    or current_refs["ownerDigest"] != lineage["ownerDigest"]
                    or current_refs["schemaVersion"] != restored_refs["schemaVersion"]
                    or current_refs["schemaFingerprint"] != restored_refs["schemaFingerprint"]):
                raise ValueError("current Company or schema differs from the selected backup")
        if observed["mode"] == "DAMAGED_PACKAGE_FILES":
            # A digest mismatch cannot prove an extra file is owned. Only known
            # archive member names may be replaced during this recovery mode.
            archive_names = {row["path"] for row in rows}
            if any(row["path"].startswith(store_rel + "/") and row["path"] not in archive_names
                   for row in observed["rows"]):
                raise ValueError("damaged package contains an unknown backup member")
        if manifest.get("avatarRefs") != restored_refs["avatarRefs"] or manifest.get("packageRefs") != restored_refs["packageRefs"] or manifest.get("musicRefs", []) != restored_refs.get("musicRefs", []):
            raise ValueError("managed references disagree")
        expanded_bytes = sum(row["bytes"] for row in rows)
        required = 2 * current_bytes + 2 * expanded_bytes + 128 * 1024 * 1024
        if shutil.disk_usage(root).free < required:
            raise ValueError("insufficient space for preserve and restore")
    created_at = manifest.get("createdAt")
    if (not isinstance(created_at, str) or len(created_at) > 40
            or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00", created_at)):
        raise ValueError("backup creation time is invalid")
    return {"status": "PREFLIGHT_OK", "archiveSha256": _sha256(archive_path), "contentDigest": manifest["contentDigest"],
            "rootBindingSha256": _root_binding(root), "packageStoreRelative": store_rel,
            "currentGeneration": observed["generation"], "currentMode": observed["mode"],
            "impact": "原资料受损/缺失；将保全原始现场后恢复" if observed["mode"] != "HEALTHY" else "当前同公司资料将由备份替换",
            "identity": restored_refs["identity"], "targetIdentity": observed["refs"]["identity"] if observed["refs"] is not None else None,
            "createdAt": created_at, "appVersion": manifest["appVersion"],
            "schemaVersion": manifest["schemaVersion"], "backupProtocol": manifest["backupProtocol"],
            "compatibility": {"sameRoot": "MATCHED", "company": "MATCHED", "appVersion": "MATCHED", "schema": "MATCHED"},
            "files": len(rows), "requiredFreeBytes": required, "reconnect": ["CREDENTIALS", "PERMISSIONS", "CAPABILITIES", "EXTERNAL_FILES", "EXTERNAL_EFFECTS"]}


def _safe_parent(root: Path, relative: str) -> Path:
    parent = root / PurePosixPath(_relative(relative)).parent
    with _held_dir(parent, create=True):
        pass
    return parent


def _atomic_temp_name(journal: dict, phase: str, relative: str) -> str:
    if phase not in {"commit", "rollback"}:
        raise ValueError("invalid atomic replacement phase")
    _relative(relative)
    scheme = journal.get("atomicTempScheme")
    nonce = journal.get("atomicTempNonce")
    if "atomicTempScheme" not in journal and "atomicTempNonce" not in journal:
        # Older journals had random commit names; this binds any new rollback write.
        nonce = hashlib.sha256(_canonical(journal)).hexdigest()[:32]
    elif scheme != "journal-v1" or not isinstance(nonce, str) or not re.fullmatch(r"[0-9a-f]{32}", nonce):
        raise ValueError("unknown atomic temporary scheme")
    digest = hashlib.sha256(f"curis-restore-v2\0{nonce}\0{phase}\0{relative}".encode()).hexdigest()[:32]
    return ".curis-restore-" + digest


def _replace_from(root: Path, relative: str, source: Path, temporary: str) -> None:
    parent = _safe_parent(root, relative)
    if not re.fullmatch(r"\.curis-restore-[0-9a-f]{32}", temporary):
        raise ValueError("invalid atomic temporary name")
    with _held_dir(parent) as parent_fd, _held_file(source) as source_fd:
        target = PurePosixPath(relative).name
        try:
            info = os.stat(target, dir_fd=parent_fd, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise ValueError("unsafe restore target")
        except FileNotFoundError:
            pass
        temporary_fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent_fd)
        try:
            with os.fdopen(os.dup(source_fd), "rb") as inp, os.fdopen(os.dup(temporary_fd), "wb") as out:
                shutil.copyfileobj(inp, out, 1024 * 1024)
                out.flush()
            os.fsync(temporary_fd)
            os.replace(temporary, target, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
            os.fsync(parent_fd)
        finally:
            os.close(temporary_fd)
            try: os.unlink(temporary, dir_fd=parent_fd)
            except FileNotFoundError: pass


def _fsync_tree(path: Path) -> None:
    for parent, dirs, names in os.walk(path, topdown=False, followlinks=False):
        for name in names:
            with _held_file(Path(parent) / name) as descriptor:
                os.fsync(descriptor)
        _fsync_dir(Path(parent))


def _verified_safety(root: Path, journal: dict) -> tuple[Path, list[dict]]:
    store_rel = _relative(journal.get("packageStoreRelative"))
    if _store_relative(root, root / store_rel) != store_rel:
        raise ValueError("recovery package-store scope is invalid")
    identifier = str(journal.get("safetyId", ""))
    if not re.fullmatch(r"[0-9]{8}T[0-9]{12}Z", identifier):
        raise ValueError("safety identifier invalid")
    safety = root / "recovery/generations" / identifier
    with _held_dir(safety):
        pass
    metadata = _bounded_json(_read_held(safety / "metadata.json", MAX_MANIFEST))
    old = metadata.get("files")
    new = metadata.get("newFiles")
    mode = metadata.get("oldMode")
    if (mode not in {"HEALTHY", "DAMAGED_DB", "MISSING_DB", "DAMAGED_PACKAGE_FILES"} or mode != journal.get("oldMode")
            or not isinstance(old, list) or not isinstance(new, list)
            or old != journal.get("oldRows") or new != journal.get("newRows")):
        raise ValueError("safety manifest disagrees with journal")
    old_root = safety / "files"
    checked = _raw_rows(old_root, store_rel)
    if checked != old or _raw_generation(mode, checked) != journal["oldGeneration"]:
        raise ValueError("safety generation is incomplete")
    new_root = safety / "new"
    new_refs, checked_new = _inventory(new_root, new_root / DB_ENTRY, journal["packageStoreRelative"],
                                      _managed_files(new_root, journal["packageStoreRelative"]), root)
    if (checked_new != new or new_refs["identity"] != metadata.get("identity")
            or new_refs["lineageDigest"] != metadata.get("lineageDigest")):
        raise ValueError("staged generation is incomplete")
    return safety, old


def _prefix_matches(candidate_fd: int, source: Path, size: int) -> bool:
    with _held_file(source) as source_fd:
        if os.fstat(source_fd).st_size < size:
            return False
        os.lseek(candidate_fd, 0, os.SEEK_SET)
        while size:
            chunk = os.read(candidate_fd, min(size, 1024 * 1024))
            if not chunk or chunk != os.read(source_fd, len(chunk)):
                return False
            size -= len(chunk)
    return True


def _preserve_atomic_residuals(root: Path, safety: Path, journal: dict, paths: set[str]) -> None:
    """Move only proven atomic-write residues out of managed parents, losslessly."""
    parents = {str(PurePosixPath(path).parent) for path in paths}
    sources = {"commit": safety / "new", "rollback": safety / "files"}
    candidates = []
    for parent_rel in sorted(parents):
        parent = root / parent_rel
        try:
            with _held_dir(parent) as parent_fd:
                for name in os.listdir(parent_fd):
                    if not name.startswith(".curis-restore-"):
                        continue
                    if not re.fullmatch(r"\.curis-restore-[0-9a-f]{32}", name):
                        raise ValueError("unknown restore temporary entry")
                    candidates.append((parent_rel, name))
                    if len(candidates) > min(MAX_ENTRIES, 128):
                        raise ValueError("too many restore temporary entries")
        except FileNotFoundError:
            continue
    if not candidates:
        return
    residuals = safety / "residuals"
    for parent_rel, name in candidates:
        parent = root / parent_rel
        with _held_dir(parent) as parent_fd:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
            try:
                info = os.fstat(fd)
                if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                        or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > MAX_MEMBER
                        or info.st_nlink not in {1, 2}):
                    raise ValueError("unsafe restore temporary entry")
                relative = parent_rel + "/" + name
                exact = []
                for target in paths:
                    if str(PurePosixPath(target).parent) != parent_rel:
                        continue
                    for phase in sources:
                        if (sources[phase] / target).exists() and name == _atomic_temp_name(journal, phase, target):
                            exact.append((phase, target))
                if len(exact) > 1:
                    raise ValueError("ambiguous atomic temporary binding")
                if exact:
                    phase, target = exact[0]
                    if not _prefix_matches(fd, sources[phase] / target, info.st_size):
                        raise ValueError("atomic temporary content differs from safety source")
                    proof = "journal-exact"
                else:
                    if "atomicTempScheme" in journal or "atomicTempNonce" in journal:
                        raise ValueError("unbound journal atomic temporary")
                    if info.st_size == 0:
                        raise ValueError("zero-length legacy temporary is unproved")
                    matches = {target for target in paths if str(PurePosixPath(target).parent) == parent_rel
                               for source in sources.values() if (source / target).exists()
                               and _prefix_matches(fd, source / target, info.st_size)}
                    if len(matches) != 1:
                        raise ValueError("legacy temporary source is ambiguous or absent")
                    target = matches.pop()
                    phase = "legacy"
                    proof = "unique-source-prefix"
                os.lseek(fd, 0, os.SEEK_SET)
                digest = hashlib.sha256()
                for chunk in iter(lambda: os.read(fd, 1024 * 1024), b""):
                    digest.update(chunk)
                after = os.fstat(fd)
                if (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) != (
                        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
                    raise ValueError("restore temporary changed during proof")
                marker_sha = digest.hexdigest()
                evidence_id = hashlib.sha256(f"{relative}\0{info.st_dev}\0{info.st_ino}\0{marker_sha}".encode()).hexdigest()
                with _held_dir(residuals, create=True) as evidence_fd:
                    evidence_info = os.fstat(evidence_fd)
                    if evidence_info.st_uid != os.getuid() or stat.S_IMODE(evidence_info.st_mode) != 0o700:
                        raise ValueError("restore temporary evidence directory is unsafe")
                    evidence_name = evidence_id + ".bin"
                    receipt = {"originalPath": relative, "targetPath": target, "phase": phase,
                               "proof": proof, "sha256": marker_sha, "bytes": info.st_size,
                               "device": info.st_dev, "inode": info.st_ino, "uid": info.st_uid,
                               "mode": stat.S_IMODE(info.st_mode), "mtimeNs": info.st_mtime_ns}
                    receipt_path = residuals / (evidence_id + ".json")
                    if receipt_path.exists():
                        if _bounded_json(_read_held(receipt_path, MAX_MANIFEST)) != receipt:
                            raise ValueError("restore temporary audit conflicts")
                    elif info.st_nlink == 2:
                        raise ValueError("restore temporary hard link has no audit")
                    else:
                        _write_json(receipt_path, receipt)
                    if info.st_nlink == 2:
                        try:
                            prior = os.stat(evidence_name, dir_fd=evidence_fd, follow_symlinks=False)
                        except FileNotFoundError as error:
                            raise ValueError("unmatched restore temporary hard link") from error
                        if (prior.st_dev, prior.st_ino) != (info.st_dev, info.st_ino):
                            raise ValueError("foreign restore temporary hard link")
                    try:
                        if info.st_nlink == 1:
                            os.link(name, evidence_name, src_dir_fd=parent_fd, dst_dir_fd=evidence_fd, follow_symlinks=False)
                            os.fsync(evidence_fd)
                    except FileExistsError:
                        pass
                    saved = os.stat(evidence_name, dir_fd=evidence_fd, follow_symlinks=False)
                    current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                    if ((saved.st_dev, saved.st_ino) != (info.st_dev, info.st_ino)
                            or (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino)
                            or current.st_nlink != 2 or saved.st_nlink != 2):
                        raise ValueError("restore temporary evidence link is unproved")
                    os.lseek(fd, 0, os.SEEK_SET)
                    confirmed = hashlib.sha256()
                    for chunk in iter(lambda: os.read(fd, 1024 * 1024), b""):
                        confirmed.update(chunk)
                    if confirmed.hexdigest() != marker_sha:
                        raise ValueError("restore temporary evidence changed")
                    current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
                    if (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns) != (
                            info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns):
                        raise ValueError("restore temporary changed before preservation")
                    os.unlink(name, dir_fd=parent_fd)
                    os.fsync(parent_fd)
            finally:
                os.close(fd)


def _rollback_v2(root: Path, journal: dict) -> dict:
    safety, old_rows = _verified_safety(root, journal)
    old = journal.get("oldFiles")
    new = journal.get("newFiles")
    if not isinstance(old, list) or not isinstance(new, list):
        raise ValueError("recovery journal is invalid")
    if old != [row["path"] for row in old_rows] or new != [row["path"] for row in journal["newRows"]]:
        raise ValueError("recovery journal path list disagrees")
    _store_relative(root, root / journal["packageStoreRelative"])
    for relative in set(old + new):
        _relative(relative)
        if not (relative == DB_ENTRY or relative in {DB_ENTRY + "-wal", DB_ENTRY + "-shm", DB_ENTRY + "-journal"}
                or relative.startswith(("data/assets/employee-avatars/", MUSIC_TREE + "/", CG_TREE + "/", "export/", journal["packageStoreRelative"] + "/"))):
            raise ValueError("recovery journal path is outside managed scope")
        target = root / relative
        try: _regular(target)
        except FileNotFoundError: pass
    _atomic_temp_name(journal, "rollback", DB_ENTRY)
    _preserve_atomic_residuals(root, safety, journal, set(old + new))
    for relative in set(old + new):
        try: _unlink_held(root / relative)
        except FileNotFoundError: pass
    for row in old_rows:
        _replace_from(root, row["path"], safety / "files" / row["path"],
                      _atomic_temp_name(journal, "rollback", row["path"]))
    observed = _observed_state(root, journal["packageStoreRelative"])
    rows, generation = observed["rows"], observed["generation"]
    if generation != journal["oldGeneration"] or rows != old_rows or observed["mode"] != journal["oldMode"]:
        raise ValueError("rollback verification failed")
    status = "ROLLED_BACK" if observed["mode"] == "HEALTHY" else "RECOVERY_REQUIRED"
    result = {"status": status, "currentMode": observed["mode"], "currentGeneration": generation, "files": len(rows)}
    _replace_json(root / "recovery/last.json", result)
    _unlink_held(root / "recovery/active.json")
    _fsync_dir(root / "recovery")
    return result


def _cold_status(root: Path, store_root: Path | None = None) -> dict:
    recovery = root / "recovery"
    if (recovery / "active.json").exists():
        return {"status": "UNKNOWN", "nextAction": "RECONCILE_OFFLINE"}
    last = recovery / "last.json"
    try:
        previous = _bounded_json(_read_held(last, MAX_MANIFEST)) if last.exists() or last.is_symlink() else None
    except (OSError, ValueError, json.JSONDecodeError):
        return {"status": "RECOVERY_REQUIRED", "currentMode": "UNPROVED",
                "nextAction": "CHECK_LOCAL_LINEAGE"}
    lineage_file = recovery / "lineage.json"
    if lineage_file.exists() or lineage_file.is_symlink():
        try:
            raw = _bounded_json(_read_held(lineage_file, MAX_MANIFEST))
            store_rel = _store_relative(root, store_root or root / _relative(raw["packageStoreRelative"]))
            lineage = _read_lineage(root, store_rel)
            observed = _observed_state(root, store_rel)
            if observed["mode"] != "HEALTHY" or observed["refs"]["ownerDigest"] != lineage["ownerDigest"]:
                return {"status": "RECOVERY_REQUIRED", "currentMode": observed["mode"],
                        "nextAction": "CHOOSE_VERIFIED_BACKUP"}
            if previous and previous.get("status") == "RECOVERY_HOLD":
                return previous
        except (OSError, ValueError, sqlite3.DatabaseError, KeyError, TypeError):
            return {"status": "RECOVERY_REQUIRED", "currentMode": "UNPROVED",
                    "nextAction": "CHECK_LOCAL_LINEAGE"}
    elif (last.exists() or last.is_symlink() or
          ((recovery / "generations").is_dir() and any((recovery / "generations").iterdir()))):
        return {"status": "RECOVERY_REQUIRED", "currentMode": "UNBOUND_PRIOR_RECOVERY",
                "nextAction": "CHECK_LOCAL_LINEAGE"}
    elif (root / DB_ENTRY).exists() or (root / DB_ENTRY).is_symlink():
        try:
            _regular(root / DB_ENTRY)
            _verify_db(root / DB_ENTRY)
        except (OSError, ValueError, sqlite3.DatabaseError):
            return {"status": "RECOVERY_REQUIRED", "currentMode": "UNBOUND_DAMAGED_DB",
                    "nextAction": "CHECK_LOCAL_LINEAGE"}
    return previous or {"status": "NO_PENDING_RECOVERY"}


def reconcile_v2(data_root: Path, store_root: Path | None = None) -> dict:
    root = data_root.absolute()
    journal_path = root / "recovery/active.json"
    if not journal_path.exists():
        return _cold_status(root, store_root)
    try:
        journal = _bounded_json(_read_held(journal_path, MAX_MANIFEST))
        result = _rollback_v2(root, journal)
        return result
    except Exception as error:
        # Never start business sidecars after an unproved partial restore.
        return {"status": "UNKNOWN", "reason": type(error).__name__}


def _pending_work(db: Path) -> bool:
    """Conservatively hold restored work that could repeat a former external effect."""
    conn = sqlite3.connect(f"file:{db.absolute()}?mode=ro", uri=True)
    try:
        tables = {row[0] for row in conn.execute("select name from sqlite_master where type='table'")}
        if "tasks" in tables and conn.execute(
            "select 1 from tasks where upper(status) in ('PENDING','PARSED','RUNNING','RESUMED','AWAITING_INPUT','HUMAN_HANDOFF') limit 1"
        ).fetchone():
            return True
        if "evolution_events" in tables:
            attempts = {}
            for event_type, raw in conn.execute(
                "select event_type,payload from evolution_events "
                "where event_type in ('conversation.attempt.started','conversation.attempt.finished') "
                "order by event_id"
            ):
                value = _bounded_json(str(raw).encode())
                attempt_id = value.get("attempt_id")
                if not isinstance(attempt_id, str) or not attempt_id:
                    return True
                attempts[attempt_id] = (event_type, value)
            for event_type, value in attempts.values():
                if event_type == "conversation.attempt.started":
                    return True
                if (value.get("status") not in {"FAILED", "COMPLETED"}
                        or value.get("effect_status") == "UNKNOWN"
                        or (value.get("execution_selection") and value.get("effect_status") != "SETTLED")):
                    return True
        if "runtime_entities" in tables:
            for kind, status, raw in conn.execute("select entity_type,lifecycle_status,data_json from runtime_entities"):
                kind, status = str(kind).upper(), str(status).upper()
                if kind in {"WORK", "HANDOFF", "EXECUTION", "TRIGGER_CLAIM"} \
                        and status in {"CREATED", "READY", "RUNNING", "SENT", "ACKNOWLEDGED", "PENDING"}:
                    return True
                if raw:
                    value = _bounded_json(str(raw).encode())
                    if value.get("effect_status") == "UNKNOWN" or value.get("effectStatus") == "UNKNOWN":
                        return True
                    if kind == "CYCLE" and value.get("executionStatus") in {"PENDING", "RUNNING", "UNKNOWN"}:
                        return True
        if "pending_effect" in tables and conn.execute(
            "select 1 from pending_effect where upper(status) not in ('SETTLED','CANCELLED') limit 1"
        ).fetchone():
            return True
        return False
    finally:
        conn.close()


def restore_v2(data_root: Path, archive_path: Path, expected_archive_sha256: str,
               expected_generation: str, store_root: Path | None = None,
               *, fail_after_files: int | None = None) -> dict:
    root = data_root.absolute()
    store_rel = _store_relative(root, store_root)
    if (root / "recovery/active.json").exists():
        raise ValueError("unfinished recovery blocks restore")
    preview = preflight_v2(root, archive_path, store_root)
    if preview["archiveSha256"] != expected_archive_sha256 or preview["currentGeneration"] != expected_generation:
        raise ValueError("restore confirmation is stale")
    recovery = _recovery_dir(root)
    generations = recovery / "generations"
    generations.mkdir(mode=0o700, exist_ok=True)
    if len(list(generations.iterdir())) >= SAFETY_LIMIT:
        raise ValueError("safety generation retention is full")
    observed = _observed_state(root, store_rel)
    old_rows, old_generation = observed["rows"], observed["generation"]
    if old_generation != expected_generation or observed["mode"] != preview["currentMode"]:
        raise ValueError("current data changed before commit")
    safety_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    safety = generations / safety_id
    with _held_dir(safety, create=True):
        pass
    journal_published = False
    try:
        stage = safety / "new"
        with _held_dir(stage, create=True):
            pass
        manifest, new_rows = _extract_v2(archive_path, stage, sum(row["bytes"] for row in old_rows))
        lineage = _read_lineage(root, store_rel)
        if (manifest["packageStoreRelative"] != store_rel or _sha256(archive_path) != expected_archive_sha256
                or manifest.get("ownerDigest") != lineage["ownerDigest"]
                or (observed["refs"] is not None and observed["refs"]["identity"] != manifest["identity"])):
            raise ValueError("selected package or identity changed")
        old_root = safety / "files"
        with _held_dir(old_root / "data", create=True):
            pass
        for row in old_rows:
            _copy_held(root / row["path"], old_root / row["path"])
        saved_rows = _raw_rows(old_root, store_rel)
        if saved_rows != old_rows:
            raise ValueError("safety generation differs from current data")
        metadata = {"oldGeneration": old_generation, "files": old_rows, "newFiles": new_rows,
                    "oldMode": observed["mode"], "identity": manifest["identity"],
                    "lineageDigest": manifest["lineageDigest"]}
        _write_json(safety / "metadata.json", metadata)
        _fsync_tree(safety)
        journal = {"safetyId": safety_id, "oldGeneration": old_generation, "oldMode": observed["mode"],
                   "oldFiles": [row["path"] for row in old_rows], "newFiles": [row["path"] for row in new_rows],
                   "oldRows": old_rows, "newRows": new_rows,
                   "packageStoreRelative": store_rel, "archiveSha256": expected_archive_sha256,
                   "atomicTempScheme": "journal-v1", "atomicTempNonce": secrets.token_hex(16)}
        _verified_safety(root, journal)
        _write_json(recovery / "active.json", journal)
        journal_published = True
        try:
            new_set = set(journal["newFiles"])
            for relative in journal["oldFiles"]:
                if relative not in new_set:
                    _unlink_held(root / relative)
            for index, row in enumerate(new_rows):
                _replace_from(root, row["path"], stage / row["path"],
                              _atomic_temp_name(journal, "commit", row["path"]))
                if fail_after_files is not None and index + 1 >= fail_after_files:
                    raise RuntimeError("injected restore interruption")
            restored_refs, restored_rows, _ = _generation(root, store_rel)
            if (restored_rows != new_rows or restored_refs["identity"] != manifest["identity"]
                    or restored_refs["ownerDigest"] != lineage["ownerDigest"]
                    or restored_refs["lineageDigest"] != manifest["lineageDigest"]):
                raise ValueError("restored generation failed readback")
        except Exception:
            rollback = reconcile_v2(root)
            if rollback["status"] not in {"ROLLED_BACK", "RECOVERY_REQUIRED"}:
                return {"status": "UNKNOWN", "safetyGeneration": safety_id}
            raise
        hold = _pending_work(stage / DB_ENTRY)
        _replace_json(recovery / "last.json", {"status": "RECOVERY_HOLD" if hold else "RESTORED", "safetyGeneration": safety_id,
                                                 "currentGeneration": hashlib.sha256(_canonical(new_rows)).hexdigest(),
                                                 "nextAction": "VERIFY_PENDING_EFFECTS" if hold else "RECONNECT_AND_REVIEW"})
        _unlink_held(recovery / "active.json")
        _fsync_dir(recovery)
    except Exception:
        if not journal_published:
            shutil.rmtree(safety)
        raise
    return {"status": "RECOVERY_HOLD" if hold else "RESTORED", "safetyGeneration": safety_id, "files": len(new_rows),
            "identity": manifest["identity"], "reconnect": preview["reconnect"], "resumeCheck": "PENDING_NO_REPLAY"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with _held_file(path) as descriptor:
        with os.fdopen(os.dup(descriptor), "rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def _verify_db(path: Path) -> int:
    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    try:
        integrity = connection.execute("pragma integrity_check").fetchone()[0]
        if integrity != "ok":
            raise ValueError(f"SQLite integrity check failed: {integrity}")
        return int(connection.execute("pragma user_version").fetchone()[0])
    finally:
        connection.close()


def backup(data_root: Path, output: Path) -> dict:
    source = data_root / DB_ENTRY
    if not source.is_file():
        raise FileNotFoundError(f"Curis database not found: {source}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="curis-backup-") as raw_tmp:
        snapshot = Path(raw_tmp) / "curis.sqlite"
        src = sqlite3.connect(f"file:{source.resolve()}?mode=ro", uri=True)
        dst = sqlite3.connect(snapshot)
        try:
            src.backup(dst)
        finally:
            dst.close()
            src.close()
        schema_version = _verify_db(snapshot)
        manifest = {
            "format": FORMAT,
            "createdAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "databaseEntry": DB_ENTRY,
            "databaseSha256": _sha256(snapshot),
            "schemaVersion": schema_version,
            "credentials": "EXCLUDED_MACOS_KEYCHAIN",
        }
        temp_output = output.with_name(f".{output.name}.tmp-{os.getpid()}")
        try:
            with zipfile.ZipFile(temp_output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr(MANIFEST_ENTRY, json.dumps(manifest, sort_keys=True, indent=2))
                archive.write(snapshot, DB_ENTRY)
            os.replace(temp_output, output)
        finally:
            temp_output.unlink(missing_ok=True)
    return manifest


def _read_archive(archive_path: Path, target_dir: Path) -> tuple[dict, Path]:
    with zipfile.ZipFile(archive_path, "r") as archive:
        if set(archive.namelist()) != {MANIFEST_ENTRY, DB_ENTRY}:
            raise ValueError("backup archive has unexpected entries")
        manifest = json.loads(archive.read(MANIFEST_ENTRY))
        if manifest.get("format") != FORMAT or manifest.get("databaseEntry") != DB_ENTRY:
            raise ValueError("backup manifest is unsupported")
        restored = target_dir / "restored.sqlite"
        with archive.open(DB_ENTRY) as source, restored.open("wb") as target:
            shutil.copyfileobj(source, target)
    if _sha256(restored) != manifest.get("databaseSha256"):
        raise ValueError("backup database hash mismatch")
    schema_version = _verify_db(restored)
    if schema_version != int(manifest.get("schemaVersion", -1)):
        raise ValueError("backup schema version mismatch")
    return manifest, restored


def restore(data_root: Path, archive_path: Path) -> dict:
    data_dir = data_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    lock_path = data_root / "curis-desktop.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("Curis is running; close it before restore") from error
        with tempfile.TemporaryDirectory(prefix="curis-restore-", dir=data_dir) as raw_tmp:
            manifest, restored = _read_archive(archive_path, Path(raw_tmp))
            target = data_dir / "curis.sqlite"
            safety_copy = None
            if target.exists():
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                safety_copy = data_dir / f"curis.sqlite.pre-restore-{stamp}"
                shutil.copy2(target, safety_copy)
            os.replace(restored, target)
            _verify_db(target)
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return {**manifest, "safetyCopy": str(safety_copy) if safety_copy else None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("backup", "restore"):
        command = subparsers.add_parser(name)
        command.add_argument("--data-root", required=True, type=Path)
        command.add_argument("--archive", required=True, type=Path)
    for name in ("full-backup", "full-preflight", "full-commit", "full-reconcile", "full-status"):
        command = subparsers.add_parser(name)
        command.add_argument("--data-root", required=True, type=Path)
        command.add_argument("--app-lock-fd", required=True, type=int)
        if name in {"full-backup", "full-preflight", "full-commit"}:
            command.add_argument("--archive", required=True, type=Path)
        if name == "full-commit":
            command.add_argument("--archive-sha256", required=True)
            command.add_argument("--current-generation", required=True)
    args = parser.parse_args()
    try:
        if args.command in {"backup", "restore"}:
            result = backup(args.data_root, args.archive) if args.command == "backup" else restore(args.data_root, args.archive)
        else:
            lock = Path(args.data_root) / "curis-desktop.lock"
            if args.app_lock_fd < 3 or os.fstat(args.app_lock_fd).st_ino != lock.stat().st_ino or os.fstat(args.app_lock_fd).st_dev != lock.stat().st_dev:
                raise ValueError("native App lock was not inherited")
            fcntl.flock(args.app_lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            store = Path(os.environ["CURIS_WORKSPACE_PACKAGE_STORE"]) if os.environ.get("CURIS_WORKSPACE_PACKAGE_STORE") else None
            if args.command == "full-backup":
                result = backup_v2(args.data_root, args.archive, store)
            elif args.command == "full-preflight":
                result = preflight_v2(args.data_root, args.archive, store)
            elif args.command == "full-commit":
                result = restore_v2(args.data_root, args.archive, args.archive_sha256, args.current_generation, store)
            elif args.command == "full-reconcile":
                result = reconcile_v2(args.data_root, store)
            else:
                recovery = Path(args.data_root) / "recovery"
                status = _cold_status(Path(args.data_root), store)
                result = {**status, "safetyGenerations": len(list((recovery / "generations").iterdir())) if (recovery / "generations").is_dir() else 0}
    except (FileNotFoundError, RuntimeError, ValueError, sqlite3.DatabaseError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as error:
        print(f"{args.command} failed: {type(error).__name__}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
