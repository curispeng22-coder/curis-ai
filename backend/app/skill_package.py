"""Pinned, inert GitHub skill packages. Installation never executes package code."""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
import urllib.request
from uuid import uuid4
from urllib.parse import urlsplit, unquote, quote

MAX_ARCHIVE = 16 * 1024 * 1024
MAX_FILE = 2 * 1024 * 1024
MAX_FILES = 512
LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "MIT_LICENSE")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative_path(value: str, *, empty: bool = False) -> str:
    if empty and value == "":
        return ""
    if (not isinstance(value, str) or not value or "\\" in value
            or any(ord(c) < 32 for c in value) or value.startswith("/")
            or any(p in {"", ".", ".."} for p in value.split("/"))):
        raise ValueError("包内路径不合法。")
    return str(PurePosixPath(value))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError("技能来源发生重定向，请核对原仓库。")


def fetch_public(url: str) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in {"api.github.com", "codeload.github.com"} or parsed.port:
        raise ValueError("只允许受控的公开 GitHub 来源。")
    # No ambient proxy, authorization header or user's Git configuration.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
    request = urllib.request.Request(url, headers={"User-Agent": "Curis-Skill-Import", "Accept": "application/json"})
    with opener.open(request, timeout=20) as response:
        data = response.read(MAX_ARCHIVE + 1)
    if len(data) > MAX_ARCHIVE:
        raise ValueError("技能包超过允许大小。")
    return data


def source_identity(repo_url: str, commit: str, subdirectory: str = "") -> tuple[str, str, str]:
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?", repo_url)
    if not match or any(x in {".", ".."} for x in match.groups()):
        raise ValueError("请输入公开 GitHub 仓库地址，不含凭据或查询参数。")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("请选择固定的完整提交版本。")
    return "/".join(match.groups()), commit, relative_path(subdirectory, empty=True)


def resolve_link(link: str, *, fetch=None) -> tuple[str, str, str]:
    """Resolve a public link to immutable source; no user Git/configuration is read."""
    url = urlsplit(link)
    if (url.scheme != "https" or url.hostname not in {"github.com", "raw.githubusercontent.com"}
            or url.port or url.username or url.password or url.query or url.fragment):
        raise ValueError("请提供不含凭据的公开 GitHub 技能链接。")
    parts = unquote(url.path).strip("/").split("/")
    if len(parts) < 2 or len(parts) > 16:
        raise ValueError("技能链接无法识别。")
    repo = "https://github.com/" + "/".join(parts[:2]).removesuffix(".git")
    source_identity(repo, "0" * 40)
    tail = parts[2:]
    if url.hostname == "raw.githubusercontent.com":
        tail = ["blob", *tail]
    if tail:
        relative_path("/".join(tail))
    getter = fetch or fetch_public
    if not tail:
        result = json.loads(getter(f"https://api.github.com/repos/{repo.rsplit('github.com/', 1)[1]}/commits/HEAD"))
        if not isinstance(result, dict):
            raise ValueError("技能版本响应无法核对。")
        commit = result.get("sha", "")
        source_identity(repo, commit)
        return repo, commit, ""
    if len(tail) < 2 or tail[0] not in {"tree", "blob"}:
        raise ValueError("请提供仓库、技能目录或 SKILL.md 链接。")
    from urllib.error import HTTPError
    # A full commit is unambiguous. Do not probe its subdirectory as part of a ref.
    ref_ends = (2,) if re.fullmatch(r"[0-9a-f]{40}", tail[1]) else range(len(tail), 1, -1)
    for end in ref_ends:
        ref = "/".join(tail[1:end])
        if re.fullmatch(r"[0-9a-f]{40}", ref):
            commit = ref
        else:
            try:
                result = json.loads(getter(f"https://api.github.com/repos/{repo.rsplit('github.com/', 1)[1]}/commits/{quote(ref, safe='')}"))
                if not isinstance(result, dict):
                    raise ValueError("技能版本响应无法核对。")
                commit = result.get("sha", "")
            except HTTPError as error:
                if error.code == 404:
                    continue
                raise
        source_identity(repo, commit)
        directory = "/".join(tail[end:])
        if tail[0] == "blob":
            if directory != "SKILL.md" and not directory.endswith("/SKILL.md"):
                continue
            directory = directory.removesuffix("SKILL.md").rstrip("/")
        return repo, commit, relative_path(directory, empty=True)
    raise ValueError("技能链接中的版本或目录无法识别。")


def inspect_package(repo_url: str, commit: str, subdirectory: str = "", *, fetch=None,
                    discover: bool = False) -> tuple[dict, dict[str, bytes]]:
    repo, commit, subdirectory = source_identity(repo_url, commit, subdirectory)
    archive = (fetch or fetch_public)(f"https://codeload.github.com/{repo}/tar.gz/{commit}")
    if not isinstance(archive, bytes) or len(archive) > MAX_ARCHIVE:
        raise ValueError("技能包超过允许大小。")
    files = {}
    symlinks = set()
    seen = set()
    total = 0
    root = None
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            for member in tar:
                name = relative_path(member.name.rstrip("/"))
                parts = name.split("/")
                if root is None:
                    root = parts[0]
                if parts[0] != root or name in seen:
                    raise ValueError("技能包目录重复或来源根目录不一致。")
                seen.add(name)
                if len(seen) > MAX_FILES * 4:
                    raise ValueError("仓库包含过多文件，请选择较小的独立技能仓库。")
                # Discovery may inspect a monorepo. Never read or follow its links.
                if member.issym() and len(parts) > 1 and member.size == 0:
                    symlinks.add("/".join(parts[1:]))
                    continue
                if not member.isdir() and not member.isfile():
                    raise ValueError("技能包不能含链接、设备或其他特殊文件。")
                if member.isdir():
                    continue
                if member.size > MAX_FILE or member.size < 0:
                    raise ValueError("技能文件超过允许大小。")
                total += member.size
                if total > MAX_ARCHIVE:
                    raise ValueError("技能包解压后超过允许大小。")
                relative = "/".join(parts[1:])
                if not relative:
                    raise ValueError("技能文件缺少包内路径。")
                data = tar.extractfile(member).read(MAX_FILE + 1)
                if len(data) != member.size:
                    raise ValueError("技能文件不完整。")
                files[relative] = data
    except (tarfile.TarError, EOFError, OSError) as error:
        raise ValueError("技能归档无法完整读取。") from error
    if symlinks.intersection(LICENSE_NAMES):
        raise ValueError("仓库许可不能含符号链接。")
    prefix = subdirectory + "/" if subdirectory else ""
    if discover and prefix + "SKILL.md" not in files:
        choices = [p.removesuffix("/SKILL.md") for p in files
                   if p.startswith(prefix) and p.endswith("/SKILL.md")]
        if len(choices) == 1:
            subdirectory = choices[0]
            prefix = subdirectory + "/"
        elif choices:
            return {"selection_required": True, "repo_url": f"https://github.com/{repo}",
                    "commit": commit, "choices": [{"directory": p, "name": skill_name(files[p + "/SKILL.md"], p)}
                                                   for p in sorted(choices)]}, {}
    if any(p.startswith(prefix) or subdirectory.startswith(p + "/") or p == subdirectory for p in symlinks):
        raise ValueError("所选技能和上级路径不能含符号链接。")
    selected = {p[len(prefix):]: data for p, data in files.items() if p.startswith(prefix)}
    if "SKILL.md" not in selected or not selected["SKILL.md"].strip():
        raise ValueError("所选目录必须包含完整 SKILL.md。")
    license_path = next((p for p in (*(prefix + name for name in LICENSE_NAMES), *LICENSE_NAMES)
                         if p in files), None)
    if license_path is None:
        raise ValueError("未找到许可文件，不能安装。")
    license_text = files[license_path].decode("utf-8", errors="strict")
    # Show the actual text for human review; never infer legal permission from a filename.
    if not license_text.strip() or len(license_text) > 65536:
        raise ValueError("许可内容无效或超出可核对范围。")
    if not license_path.startswith(prefix) or prefix:
        if "CURIS_SOURCE_LICENSE" in selected:
            raise ValueError("技能包使用了保留文件名。")
        selected["CURIS_SOURCE_LICENSE"] = files[license_path]
    if len(selected) > MAX_FILES or ".curis-package.json" in selected:
        raise ValueError("技能包文件过多或使用了保留文件名。")
    inventory = [{"path": p, "bytes": len(data), "sha256": digest(data)} for p, data in sorted(selected.items())]
    manifest = {"repo_url": f"https://github.com/{repo}", "commit": commit, "subdirectory": subdirectory,
                "archive_sha256": digest(archive), "files": inventory,
                "license_path": license_path, "license_sha256": digest(files[license_path]), "license_text": license_text}
    manifest["name"] = skill_name(selected["SKILL.md"], subdirectory or repo.rsplit("/", 1)[-1])
    manifest["dependencies"] = dependency_requirements(selected, repo)
    manifest["package_sha256"] = digest(json.dumps(manifest, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())
    return manifest, selected


def skill_name(data: bytes, fallback: str) -> str:
    text = data.decode("utf-8", errors="replace")
    name = re.search(r"(?m)^name:\s*([^\n]{1,160})$", text) or re.search(r"(?m)^#\s+([^\n]{1,160})$", text)
    return (name.group(1).strip().strip("\"'") if name else fallback.rsplit("/", 1)[-1])[:160]


def dependency_requirements(files: dict[str, bytes], repo: str) -> list[dict]:
    """Describe requirements, never interpret prose as installation commands."""
    requirements = []
    if repo.lower() == "tencent/browserskill":
        requirements.append({"kind": "browser_skill", "name": "BrowserSkill 官方 CLI、浏览器扩展与连接授权",
                             "preparation": "existing_browser_connection"})
    for name in files:
        if name.rsplit("/", 1)[-1] in {"requirements.txt", "pyproject.toml", "package.json", "Cargo.toml"}:
            requirements.append({"kind": "declared_runtime", "name": name, "preparation": "not_supported"})
    text = files.get("SKILL.md", b"").decode("utf-8", errors="replace")
    if not requirements and (re.search(r"(?im)^\s*(?:requires|dependencies|bins|env|install)\s*:", text)
            or re.search(r"(?im)^#+\s*(?:dependencies|requirements|prerequisites|依赖|安装)", text)
            or re.search(r"\b(?:pip\s+install|npm\s+install|brew\s+install|uvx|npx)\b", text)):
        requirements.append({"kind": "declared_runtime", "name": "SKILL.md 中的运行要求", "preparation": "not_supported"})
    # Executable files are retained, but are not automatically granted an execution environment.
    if not requirements and any(p.endswith((".py", ".js", ".sh", ".rs")) for p in files):
        requirements.append({"kind": "script_runtime", "name": "技能脚本的运行条件", "preparation": "not_supported"})
    return requirements


def safe_directory(path: Path) -> Path:
    path = path.absolute()
    for parent in [*reversed(path.parents), path]:
        if parent.is_symlink():
            raise ValueError("受控目录不能经过符号链接。")
        if parent.exists() and not parent.is_dir():
            raise ValueError("受控目录路径被文件占用。")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def install_package(root: Path, manifest: dict, files: dict[str, bytes]) -> Path:
    key = manifest["package_sha256"]
    if not re.fullmatch(r"[0-9a-f]{64}", key):
        raise ValueError("技能包摘要无效。")
    root = safe_directory(root)
    destination = root / key
    if destination.exists():
        verify_package(destination, manifest)
        return destination
    final_path = destination
    destination = root / (".pending-" + uuid4().hex)
    destination.mkdir(mode=0o700)
    # A failed partial install stays inspectable and is never treated as installed.
    for item in manifest["files"]:
        relative = relative_path(item["path"])
        data = files[relative]
        if len(data) != item["bytes"] or digest(data) != item["sha256"]:
            raise ValueError("技能文件与已确认清单不一致。")
        target = destination / relative
        safe_directory(target.parent)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o400)
    with (destination / ".curis-package.json").open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, ensure_ascii=False, sort_keys=True)
    (destination / ".curis-package.json").chmod(0o400)
    verify_package(destination, manifest)
    if final_path.exists():
        verify_package(final_path, manifest)
        return final_path
    destination.rename(final_path)
    return final_path


def verify_package(path: Path, manifest: dict) -> None:
    if path.is_symlink() or not path.is_dir():
        raise ValueError("技能包目录不存在或不安全。")
    expected = {item["path"]: item for item in manifest["files"]}
    found = set()
    for directory, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            target = Path(directory) / name
            mode = target.lstat().st_mode
            if not stat.S_ISREG(mode) and not stat.S_ISDIR(mode):
                raise ValueError("技能包出现链接或特殊文件。")
            if not stat.S_ISREG(mode):
                continue
            relative = target.relative_to(path).as_posix()
            if relative == ".curis-package.json":
                if json.loads(target.read_text()) != manifest:
                    raise ValueError("技能包安装凭据已变化。")
                continue
            item = expected.get(relative)
            if item is None or target.stat().st_size != item["bytes"] or digest(target.read_bytes()) != item["sha256"]:
                raise ValueError("技能包文件已变化，请重新核对来源。")
            found.add(relative)
    if found != set(expected) or not (path / ".curis-package.json").is_file():
        raise ValueError("技能包文件不完整。")
