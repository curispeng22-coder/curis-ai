"""Materialize and verify resources for one existing Work execution."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

from .skill_package import safe_directory, verify_package, relative_path, digest


SCOPED_CODEX_INSTRUCTIONS = (
    "You are a bounded Curis employee executor. Use only the supplied tools for this Work. "
    "Do not delegate or access other tasks. Return textual evidence for human review."
)


def scoped_codex_model_catalog(public_catalog, model):
    """Reduce the proved SDK model profile; never retain bundled model prompts."""
    if model != "gpt-5.6-sol":
        raise ValueError("该 Native 模型的执行边界尚未核验。")
    models = public_catalog.get("models") if isinstance(public_catalog, dict) else public_catalog
    if not isinstance(models, list) or len(models) > 128:
        raise ValueError("Native 内置模型目录无法核验。")
    matches = [item for item in models if isinstance(item, dict) and item.get("slug") == model]
    if len(matches) != 1:
        raise ValueError("Native 内置目录未提供唯一已核验模型。")
    entry = dict(matches[0])
    requested = {key: entry.get(key) for key in ("slug", "tool_mode", "multi_agent_version", "use_responses_lite")}
    reductions = dict(base_instructions=SCOPED_CODEX_INSTRUCTIONS, model_messages=None, comp_hash=None,
        multi_agent_version="disabled", tool_mode="direct", input_modalities=["text"],
        supports_image_detail_original=False, supports_search_tool=False, experimental_supported_tools=[],
        apply_patch_tool_type=None, include_skills_usage_instructions=False, supports_parallel_tool_calls=False)
    native = requested == {"slug": model, "tool_mode": "code_mode_only", "multi_agent_version": "v2", "use_responses_lite": True}
    # The released Linux catalog has already undergone this exact reduction.
    scoped = all(key in entry and type(entry[key]) is type(value) and entry[key] == value
        for key, value in reductions.items())
    if entry.get("use_responses_lite") is not True or not (native or scoped):
        raise ValueError("Native 模型能力已改变，请重新核验后执行。")
    entry.update(reductions)
    effective = {key: entry.get(key) for key in ("slug", "tool_mode", "multi_agent_version", "use_responses_lite",
        "input_modalities", "apply_patch_tool_type", "supports_search_tool", "supports_parallel_tool_calls")}
    return {"models": [entry]}, {"requested_native_metadata": requested, "effective_configuration": effective,
        "tool_surface_basis": "PINNED_SDK_OFFLINE_PROOF_NOT_PER_TURN_TOOL_OBSERVATION",
        "native_builtins": ["list_mcp_resources", "list_mcp_resource_templates", "read_mcp_resource", "update_plan", "view_image"],
        "view_image_boundary": "TEXT_ONLY_MODEL_REJECTS_IMAGE_TOOL_BEFORE_FILE_READ",
        "vendor_prompt_stored": False, "global_configuration_changed": False}


def validate_reader_png(data: bytes) -> tuple[int, int]:
    """Validate bounded, non-interlaced RGB/RGBA8 PNG structure and decompressed rows."""
    import struct
    import zlib
    if not isinstance(data, bytes) or not data.startswith(bytes.fromhex("89504e470d0a1a0a")) or len(data) > 8 * 1024 * 1024:
        raise ValueError("Invalid PNG signature or size")
    position, width, height, bpp, compressed, ended = 8, 0, 0, 0, bytearray(), False
    while position < len(data):
        if position + 12 > len(data):
            raise ValueError("Truncated PNG chunk")
        size = struct.unpack(">I", data[position:position+4])[0]
        kind = data[position+4:position+8]
        end = position + 12 + size
        if end > len(data) or size > 8 * 1024 * 1024:
            raise ValueError("Truncated or oversized PNG chunk")
        payload = data[position+8:position+8+size]
        crc = struct.unpack(">I", data[position+8+size:end])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError("PNG chunk CRC mismatch")
        if kind == b"IHDR":
            if position != 8 or size != 13 or width:
                raise ValueError("Invalid PNG header")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            if not (0 < width <= 4096 and 0 < height <= 4096 and width * height <= 16000000
                    and depth == 8 and color in (2, 6) and compression == filtering == interlace == 0):
                raise ValueError("Unsupported PNG dimensions or format")
            bpp = 3 if color == 2 else 4
        elif kind == b"IDAT":
            if not width or ended:
                raise ValueError("Invalid PNG image data")
            compressed.extend(payload)
        elif kind == b"IEND":
            if size or not compressed or end != len(data):
                raise ValueError("Invalid PNG ending")
            ended = True
            position = end
            break
        elif kind[0] & 32 == 0:
            raise ValueError("Unsupported PNG critical chunk")
        position = end
    if not ended:
        raise ValueError("PNG is incomplete")
    row = width * bpp + 1
    expected = row * height
    inflater = zlib.decompressobj()
    try:
        decoded = inflater.decompress(bytes(compressed), expected + 1)
    except zlib.error as error:
        raise ValueError("PNG image data invalid") from error
    if len(decoded) != expected or not inflater.eof or inflater.unused_data or inflater.unconsumed_tail:
        raise ValueError("PNG image data invalid or oversized")
    if any(decoded[i * row] > 4 for i in range(height)):
        raise ValueError("PNG filter invalid")
    return width, height


def scope_key(tenant_id: str, company_id: str, work_ref: str, task_id: str) -> str:
    if not all(isinstance(value, str) and value for value in (tenant_id, company_id, work_ref, task_id)):
        raise ValueError("Agent execution requires its original Company, Work and Task")
    return digest(json.dumps([tenant_id, company_id, work_ref, task_id], separators=(",", ":")).encode())


def open_directory(path: Path, root: Path) -> int:
    """Anchor in application-owned storage, then pin each execution-owned component."""
    path, root = path.absolute(), root.absolute()
    parts = path.relative_to(root).parts
    for parent in (root, *root.parents):
        if not stat.S_ISDIR(parent.lstat().st_mode):
            raise ValueError("应用成果根目录不能包含链接。")
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in parts:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


class AgentWorkResources:
    def __init__(self, root: Path, *, tenant_id: str, company_id: str, work_ref: str, task_id: str):
        self.key = scope_key(tenant_id, company_id, work_ref, task_id)
        self.path = Path(root).absolute() / self.key
        self.identity = {"tenant_id": tenant_id, "company_id": company_id, "work_ref": work_ref, "task_id": task_id}
        self._browser_captures = {}
        self._pending_browser_capture = None

    def prepare(self, packages: list[dict], *, temporary_root: Path | None = None) -> dict:
        if self.path.exists():
            # No reusing a possibly running, cancelled or incomplete execution directory.
            raise ValueError("原执行目录已存在，请核验原工作，不能自动重复执行。")
        safe_directory(self.path)
        output = safe_directory(self.path / "output")
        skills = []
        for package in packages:
            manifest = package["manifest"]
            source = Path(package["path"])
            verify_package(source, manifest)
            key = manifest["package_sha256"]
            if not re.fullmatch(r"[0-9a-f]{64}", key):
                raise ValueError("技能包摘要不合法。")
            target = safe_directory(self.path / ".agents" / "skills" / key)
            for item in manifest["files"]:
                name = relative_path(item["path"])
                dest = target / name
                safe_directory(dest.parent)
                data = (source / name).read_bytes()
                if digest(data) != item["sha256"] or len(data) != item["bytes"]:
                    raise ValueError("技能包在加载前发生变化。")
                with dest.open("xb") as file:
                    file.write(data)
                dest.chmod(0o400)
            skills.append({"skill_template_id": package["skill_template_id"], "package_sha256": key,
                           "path": str(target), "file_count": len(manifest["files"]),
                           "loaded": True, "used": "UNVERIFIED"})
        receipt = {**self.identity, "skills": skills, "output_directory": str(output)}
        with (self.path / "resources.json").open("x") as file:
            json.dump(receipt, file, sort_keys=True)
        # Do not copy credentials or override HOME/CODEX_HOME. Native profile use is a separate gate.
        temporary = safe_directory(self.path / "tmp") if temporary_root is None else self.prepare_temporary(temporary_root)
        environment = {"PATH": "/usr/bin:/bin", "TMPDIR": str(temporary), "LANG": "en_US.UTF-8",
                       "NO_PROXY": "localhost,127.0.0.1,::1", "no_proxy": "localhost,127.0.0.1,::1"}
        return {"cwd": str(self.path), "environment": environment, "receipt": receipt}

    def owner_channel_descriptor(self, manifests):
        """Describe verified tool-only resources without exporting host paths or files."""
        from .agent_tool_server import read_manifest_file
        if type(manifests) is not dict or len(manifests) > 32:
            raise ValueError("工作技能清单超出边界。")
        skills = []
        total = 0
        for key, manifest in sorted(manifests.items()):
            if (type(key) is not str or not re.fullmatch(r"[0-9a-f]{64}",key)
                    or type(manifest) is not dict or manifest.get("package_sha256") != key
                    or type(manifest.get("files")) is not list):
                raise ValueError("工作技能摘要无法核验。")
            files = []
            seen = set()
            for item in manifest["files"]:
                total += 1
                if total > 256:raise ValueError("工作技能文件数超出边界。")
                name = relative_path(item["path"])
                if name in seen:raise ValueError("工作技能文件路径重复。")
                seen.add(name)
                read_manifest_file(self.path / ".agents" / "skills" / key,name,item)
                files.append({"path":name,"sha256":item["sha256"],"bytes":item["bytes"]})
            skills.append({"package_sha256":key,"files":files})
        descriptor = {"identity":self.identity.copy(),"skills":skills,
            "resource_access":"ORIGINAL_WORK_TOOLS_ONLY","output_directory":"output"}
        raw = json.dumps(descriptor,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
        if len(raw) > 32768:raise ValueError("工作资源描述超出通道边界。")
        return {"resources":descriptor,"sha256":digest(raw)}

    def prepare_temporary(self, root):
        root = Path(root)
        if not root.is_absolute():
            raise ValueError("原执行临时根必须是明确的绝对路径。")
        root = safe_directory(root)
        info = root.lstat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
            raise ValueError("原执行临时根必须由当前用户独占，权限为0700。")
        temporary = root / self.key[:16]
        if len(str(temporary).encode()) > 64:
            raise ValueError("原执行临时路径过长，不能可靠承接本机IPC。")
        if temporary.exists():
            marker = temporary / "owner.json"
            if marker.is_symlink() or not marker.is_file() or json.loads(marker.read_text()) != self.identity:
                raise ValueError("短临时路径与原执行身份不一致。")
            raise ValueError("原执行临时目录已存在，不自动复用或重放。")
        temporary.mkdir(mode=0o700)
        fd = os.open(temporary / "owner.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as handle:
            json.dump(self.identity, handle, sort_keys=True)
        return temporary

    def begin_browser_capture(self):
        # Cross-instance capture commitment and revocation are not yet proved.
        # Refuse before creating an output file, including after a cold restart.
        raise ValueError("截图成果暂不可用：跨实例来源与撤权边界尚未验证。")

    def collect(self, *, _capture_token=None) -> list[dict]:
        if self._pending_browser_capture is not None and _capture_token is not self._pending_browser_capture:
            raise ValueError("截图来源尚未完成登记，不能收集成果。")
        output = self.path / "output"
        output_fd = open_directory(output, self.path.parent)
        try:
            receipts = self._collect(output_fd)
            for receipt in receipts:
                capture = self._browser_captures.get(receipt["relative_path"])
                if capture is not None:
                    if (receipt["sha256"], receipt["bytes"]) != (capture["sha256"], capture["bytes"]):
                        raise ValueError("原浏览截图与已登记来源不一致。")
                    receipt["browser_capture"] = dict(capture)
            if set(self._browser_captures) - {r["relative_path"] for r in receipts}:
                raise ValueError("已登记的浏览截图不再存在。")
            return receipts
        finally:
            os.close(output_fd)

    def register_browser_capture(self, receipt: dict, *, url: str, session_id: str, tab_id: str, _capture_token=None) -> dict:
        # Generic outputs cannot claim browser provenance while capture is held.
        raise ValueError("截图成果暂不可用：跨实例来源与撤权边界尚未验证。")

    def read_output(self, receipt: dict) -> bytes:
        if any(receipt.get(key) != value for key, value in self.identity.items()):
            raise ValueError("文件回执不属于原公司、工作和执行。")
        name = Path(relative_path(receipt["relative_path"]))
        if (type(receipt.get("bytes")) is not int or not 0 <= receipt["bytes"] <= 8 * 1024 * 1024
                or not re.fullmatch(r"[0-9a-f]{64}", str(receipt.get("sha256", "")))):
            raise ValueError("原文件回执不完整。")
        directory = open_directory(self.path / "output", self.path.parent)
        try:
            for part in name.parts[:-1]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                os.close(directory)
                directory = child
            fd = os.open(name.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            try:
                before = os.fstat(fd)
                if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size != receipt["bytes"]:
                    raise ValueError("原成果文件类型或大小已改变。")
                with os.fdopen(fd, "rb", closefd=False) as file:
                    data = file.read(8 * 1024 * 1024 + 1)
                after = os.fstat(fd)
                if (before.st_size, before.st_mtime_ns, before.st_ctime_ns, before.st_ino) != (
                        after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_ino):
                    raise ValueError("成果文件仍在变化。")
                if len(data) != receipt["bytes"] or digest(data) != receipt["sha256"]:
                    raise ValueError("成果文件与原回执不一致，拒绝下载。")
                return data
            finally:
                os.close(fd)
        finally:
            os.close(directory)

    def _collect(self, output_fd: int) -> list[dict]:
        result = []
        total = 0
        for directory, dirs, names, directory_fd in os.fwalk(".", dir_fd=output_fd, follow_symlinks=False):
            for name in dirs:
                if not stat.S_ISDIR(os.stat(name, dir_fd=directory_fd, follow_symlinks=False).st_mode):
                    raise ValueError("输出目录不能包含链接。")
            for name in names:
                path = Path(directory) / name
                fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
                try:
                    before = os.fstat(fd)
                    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > 8 * 1024 * 1024:
                        raise ValueError("输出文件类型或大小不符合当前范围。")
                    with os.fdopen(fd, "rb", closefd=False) as file:
                        data = file.read(8 * 1024 * 1024 + 1)
                    after = os.fstat(fd)
                    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino) or len(data) != before.st_size:
                        raise ValueError("输出文件仍在变化，不能登记为已回收。")
                finally:
                    os.close(fd)
                total += len(data)
                if total > 16 * 1024 * 1024 or len(result) >= 32:
                    raise ValueError("本次输出超出允许范围。")
                result.append({**self.identity, "relative_path": path.as_posix(),
                               "sha256": digest(data), "bytes": len(data), "verification_status": "FILE_HASH_VERIFIED",
                               "content_verification": "UNVERIFIED"})
        return result


def require_browser_boundary(receipt: dict, *, company_id: str, work_ref: str, profile_id: str, url: str, action: str) -> None:
    """Validate facts supplied by an enforcing browser adapter, never by page text."""
    parsed = urlsplit(url)
    if (receipt.get("company_id"), receipt.get("work_ref"), receipt.get("profile_id")) != (company_id, work_ref, profile_id):
        raise ValueError("浏览器会话不属于原公司、工作和独立账号环境。")
    if action not in {"observe", "extract", "navigate"} or action not in receipt.get("allowed_actions", []):
        raise ValueError("当前浏览授权不包含这个动作。")
    if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.port not in {None, 443}
            or parsed.hostname not in receipt.get("allowed_hosts", []) or parsed.hostname in {"localhost", "127.0.0.1", "::1"}):
        raise ValueError("目标不在本次已授权的公开网页范围内。")
    # BrowserSkill's separate window and broad extension permissions are not enforcement evidence.
    # No current enforcing bridge is released: reject even a caller-claimed verified receipt.
    raise ValueError("浏览器站点、重定向和账号隔离尚未在实际工具边界核验，暂不能自动浏览。")
