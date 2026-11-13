"""Server-owned, bounded content-addressed local audio bytes.

Filesystem publication precedes domain registration. Orphans are retained and
have no public identifier. Each scoped read revalidates bytes and WAV metadata.
"""
from __future__ import annotations
import hashlib
import os
import re
import stat
import wave
import io
from pathlib import Path
from uuid import uuid4
from .runtime.music import MusicRuntime
from .runtime import RuntimeScopeError

APPROVED_ROOT = Path("/private/tmp/curis-music-entry-20261005-01")
OPERATING_ROOT = Path("/private/tmp/curis-music-operating-chain-20261005-01/store")
USER_RIGHTS = "LOCAL_USER_PROVIDED_UNVERIFIED"
USER_PURPOSE = "LOCAL_USE_ONLY"
MAX_AUDIO_FILES = 64
MAX_AUDIO_TOTAL = 256 * 1024 * 1024

SAMPLES = {"demo-a.wav": "74d131f06bfcc3aacf37a5c75aeb63341308e5ffd7e78c7c94a661f873ec89f1", "demo-b.wav": "6c314b5f4c3b63c958d606410a6eec951bda2d83b3eb1b610d42e44fd0a58c99"}


def directory(path):
    """Open every component without following symlinks, including ancestors."""
    path = Path(path)
    if not path.is_absolute(): raise ValueError("媒体目录必须由服务器准确配置。")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = new
        return fd
    except BaseException:
        os.close(fd); raise


def read_file(folder, name):
    parent = directory(folder)
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
        with os.fdopen(fd, "rb") as handle:
            metadata = os.fstat(handle.fileno())
            if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= 16_000_000:
                raise ValueError("音频文件类型或大小不合法。")
            return handle.read(16_000_001)
    finally:
        os.close(parent)


def _inspect_audio(raw):
    if not isinstance(raw, bytes) or not 0 < len(raw) <= 16_000_000:
        raise ValueError("音频为空或超过16MB。")
    with wave.open(io.BytesIO(raw), "rb") as audio:
        if audio.getcomptype() != "NONE" or not 1 <= audio.getnchannels() <= 2 or audio.getsampwidth() not in {1, 2, 3, 4} or not 8000 <= audio.getframerate() <= 192000:
            raise ValueError("音频格式不受支持。")
        frames = audio.getnframes(); expected = frames * audio.getnchannels() * audio.getsampwidth()
        if len(audio.readframes(frames)) != expected: raise ValueError("音频数据不完整。")
        duration = frames / audio.getframerate()
        if not 0 < duration <= 600: raise ValueError("音频长度不合法。")
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw), "duration": duration, "mime": "audio/wav", "rights": "LOCAL_DESIGN_ONLY", "purpose": "NONCOMMERCIAL_ISOLATED_TEST", "source_sha256": hashlib.sha256(raw).hexdigest()}


def inspect_audio(raw):
    try:
        return _inspect_audio(raw)
    except (wave.Error, EOFError, OverflowError) as error:
        raise ValueError("WAV 文件格式或数据不完整。") from error


def ensure_directory(path):
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in Path(path).parts[1:]:
            try: os.mkdir(part, 0o700, dir_fd=fd)
            except FileExistsError: pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = child
        return fd
    except BaseException:
        os.close(fd); raise


class MusicMediaService:
    def __init__(self, database, *, root=None, data_root=None):
        self.db = database; self.runtime = MusicRuntime(database)
        # No default-root creation or client-controlled directory configuration.
        self.root = Path(root) if root is not None else None
        if self.root is not None and self.root not in {APPROVED_ROOT, OPERATING_ROOT}:
            raise ValueError("当前媒体目录未获准确授权。")
        self.data_root = None
        if data_root is not None and root is None:
            base = Path(os.path.abspath(data_root))
            if not Path(data_root).is_absolute(): raise ValueError("本机数据根必须为绝对路径。")
            expected = base / "data/curis.sqlite"
            paths = [database.path, *(os.environ.get(key) for key in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"))]
            if any(not value or Path(os.path.abspath(value)) != expected for value in paths):
                raise ValueError("音乐存储与本机数据根、数据库别名不一致。")
            # Constructor checks only; storage is created after explicit import.
            fd = directory(base); os.close(fd)
            self.data_root = base
            self.root = base / "data/assets/music-audio"

    def stage_user(self, raw):
        if self.data_root is None: raise RuntimeScopeError("普通本地音频导入未配置。")
        meta = {**inspect_audio(raw), "rights": USER_RIGHTS, "purpose": USER_PURPOSE}
        target = meta["sha256"] + ".wav"
        media = ensure_directory(self.root)
        staging = None
        temporary = str(uuid4()) + ".wav"
        created = False
        try:
            staging = ensure_directory(self.data_root / "cache/tmp/music-import")
            names = os.listdir(media)
            if any(not re.fullmatch(r"[0-9a-f]{64}\.wav", name) for name in names): raise ValueError("音频存储存在未知文件，请保留现场。")
            sizes = [os.stat(name, dir_fd=media, follow_symlinks=False) for name in names]
            if any(not stat.S_ISREG(item.st_mode) for item in sizes): raise ValueError("音频存储存在不安全文件。")
            # Finalized orphans are retained and backed up as validated WAV, never
            # publicly addressable without a scoped Asset. Bound prevents growth.
            if target not in names and (len(names) >= MAX_AUDIO_FILES or sum(item.st_size for item in sizes) + len(raw) > MAX_AUDIO_TOTAL):
                raise ValueError("本地音频存储已到上限，请先保留完整备份。")
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=staging); created = True
            with os.fdopen(fd, "wb") as handle: handle.write(raw); handle.flush(); os.fsync(handle.fileno())
            try: os.link(temporary, target, src_dir_fd=staging, dst_dir_fd=media, follow_symlinks=False)
            except FileExistsError: pass
            os.fsync(media)
            checked = inspect_audio(read_file(self.root, target))
            if any(checked[key] != meta[key] for key in ("sha256", "size", "duration", "mime", "source_sha256")): raise ValueError("持久音频字节核对失败。")
        finally:
            if created: os.unlink(temporary, dir_fd=staging)  # only this operation's private staging file
            if staging is not None: os.close(staging)
            os.close(media)
        return meta

    def stage_sample(self, name):
        if self.root is None or name not in SAMPLES: raise RuntimeScopeError("本地媒体样本尚未由服务器授权。")
        raw = read_file(self.root / "inputs", name); meta = inspect_audio(raw)
        if meta["sha256"] != SAMPLES[name]: raise ValueError("样本哈希与授权来源不一致。")
        target = meta["sha256"] + ".wav"
        staging = directory(self.root / "staging"); media = directory(self.root / "media")
        temporary = str(uuid4()) + ".wav"
        try:
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=staging)
            with os.fdopen(fd, "wb") as handle: handle.write(raw); handle.flush(); os.fsync(handle.fileno())
            # Hard-link gives create-if-absent semantics; an existing symlink is
            # rejected by the verification read below, never overwritten.
            try: os.link(temporary, target, src_dir_fd=staging, dst_dir_fd=media, follow_symlinks=False)
            except FileExistsError: pass
            os.fsync(media)
        finally:
            os.close(staging); os.close(media)
        if inspect_audio(read_file(self.root / "media", target)) != meta: raise ValueError("持久音频与样本不一致。")
        # Staging leftovers and unregistered bytes intentionally retained.
        return meta

    def verify(self, con, company, workspace, song, asset_ref):
        if self.root is None: raise RuntimeScopeError("音频库未配置。")
        asset = self.runtime.get(con, company, workspace, asset_ref, kind="AudioAssetVersion", song=song)
        data = asset["data"]
        if not re.fullmatch(r"[0-9a-f]{64}", data.get("sha256", "")): raise ValueError("音频标识不合法。")
        meta = inspect_audio(read_file(self.root if self.data_root is not None else self.root / "media", data["sha256"] + ".wav"))
        if self.data_root is not None: meta.update(rights=USER_RIGHTS, purpose=USER_PURPOSE)
        if any(data.get(k) != value for k, value in meta.items()): raise ValueError("音频字节、长度或用途已改变。")
        if self.data_root is None and meta["sha256"] not in SAMPLES.values(): raise ValueError("音频来源不在授权样本内。")
        return asset

    def read(self, con, company, workspace, song, asset_ref, range_header=None):
        asset = self.verify(con, company, workspace, song, asset_ref); data = asset["data"]
        raw = read_file(self.root if self.data_root is not None else self.root / "media", data["sha256"] + ".wav")
        if inspect_audio(raw)["sha256"] != data["sha256"]: raise ValueError("音频读取期间已改变。")
        size = len(raw); start = 0; end = size - 1; status = 200
        headers = {"Accept-Ranges": "bytes", "ETag": '"' + data["sha256"] + '"', "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"}
        if range_header:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header)
            if not match or not any(match.groups()): raise ValueError("不支持的音频范围。")
            left, right = match.groups()
            if left: start = int(left); end = min(int(right), end) if right else end
            else:
                suffix = int(right)
                if suffix <= 0: raise ValueError("音频范围无效。")
                start = max(0, size - suffix)
            if not 0 <= start <= end < size: raise ValueError("音频范围超出文件。")
            status = 206; headers["Content-Range"] = f"bytes {start}-{end}/{size}"
        return raw[start:end+1], status, headers
