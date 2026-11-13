from __future__ import annotations

from enum import Enum

import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from .evolution_event_log import EvolutionEventLog
# B 层运行时治理边界（T06 接线点）：本地工具入口的防御性前置闸（G2 chokepoint）。
from .runtime_governance import ActionContext, evaluate


# 容器内/宿主自适应推导：backend/app/*.py → 仓库根。
# 宿主上 parents[2] 恰等于原硬编码的宿主机用户目录仓库根；
# 容器内则指向挂载的仓库根，不再依赖宿主机绝对路径。
_DERIVED_ROOT = Path(__file__).resolve().parents[2]
# 兼容既有测试（test_local_rd_toolset.py）的别名；本模块运行时统一走 _resolve_workspace_root。
WORKSPACE_ROOT = _DERIVED_ROOT
# 由 build 期 d1_config 注入的可选覆盖位（默认 None → 走 _DERIVED_ROOT）。
_WORKSPACE_ROOT_OVERRIDE: str | None = None
LOCAL_RD_TOOL_IDS = frozenset(
    {
        "tl_ai_rd_file_reader",
        "tl_ai_rd_code_docs_search",
        "tl_ai_rd_file_writer",
        "tl_ai_rd_test_runner",
        "tl_ai_rd_git_client",
    }
)


# ---------------------------------------------------------------------------
# sandbox 网络隔离模式（步骤③ hardening：解除对 sandbox-exec 的硬依赖）
# ---------------------------------------------------------------------------
class SandboxMode(str, Enum):
    """run_test 的网络隔离策略。

    - AUTO    ：默认。sandbox-exec 存在则走隔离；缺失则降级为直跑（仅限本地 /
        受信 CI），并在审计中标记 ``sandbox_degraded``。
    - OFF     ：关闭隔离，直接执行注册命令（仅限本地开发 / 受信 CI）。
    - ENFORCE ：强制隔离。sandbox-exec 缺失时直接拒绝（fail-closed，生产多租户用）。
    """

    AUTO = "auto"
    OFF = "off"
    ENFORCE = "enforce"


def _resolve_sandbox_mode(value: SandboxMode | str | None) -> SandboxMode:
    """解析 sandbox 模式：枚举直通；``None`` 取环境变量 ``CURIS_RD_SANDBOX``（默认 auto）。

    非法字符串回退 auto，避免配置错误导致整体不可用。
    """
    if isinstance(value, SandboxMode):
        return value
    if value is None:
        value = os.getenv("CURIS_RD_SANDBOX", "auto")
    try:
        return SandboxMode(str(value).strip().lower())
    except ValueError:
        return SandboxMode.AUTO

_MAX_READ_BYTES = 1024 * 1024
_MAX_SEARCH_BYTES = 512 * 1024
_MAX_SEARCH_RESULTS = 200
_MAX_PATTERN_BYTES = 256
_MAX_DIFF_BYTES = 128 * 1024
_MAX_DIFF_FILES = 10
_MAX_PROCESS_OUTPUT = 64 * 1024
_PROCESS_TIMEOUT_SECONDS = 120
_FORBIDDEN_DIRS = {".git", "data", "deploy", ".ssh", ".aws", ".kube", "node_modules"}
_FORBIDDEN_SUFFIXES = {".pem", ".crt", ".p12", ".pfx", ".jwk", ".sqlite", ".sqlite3", ".db"}
_FORBIDDEN_NAME = re.compile(
    r"(?:^|[._-])(secret|credential|token|cookie|password|key)(?:[._-]|$)", re.IGNORECASE
)
_SENSITIVE_VALUE = re.compile(
    r"(?:authorization\s*[:=]|cookie\s*[:=]|bearer\s+[A-Za-z0-9._~-]{16,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}|"
    r"(?:api[_-]?key|secret|password|token)\s*[:=]\s*[^\s,;]{8,})",
    re.IGNORECASE,
)
_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?\n?$")


class LocalRDToolError(RuntimeError):
    def __init__(self, failure_code: str, message: str, *, exit_code: int | None = None):
        super().__init__(message)
        self.failure_code = failure_code
        self.exit_code = exit_code


def _resolve_workspace_root(override: str | None = None) -> Path:
    """受控解析 workspace 根：解析失败/为符号链接一律抛脱敏 LocalRDToolError。

    绝不抛裸 FileNotFoundError 穿透 create_app；统一使用 D1_UNAVAILABLE_MESSAGE，
    禁止泄露任何路径/堆栈/Key。默认（override 为 None）走模块级推导的 _DERIVED_ROOT。
    """
    from .d1_config import D1_UNAVAILABLE_MESSAGE

    candidate = Path(override) if override else _DERIVED_ROOT
    try:
        root = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError):
        raise LocalRDToolError("workspace_root_unavailable", D1_UNAVAILABLE_MESSAGE) from None
    if root.is_symlink():
        raise LocalRDToolError("workspace_root_unavailable", D1_UNAVAILABLE_MESSAGE)
    return root


@dataclass(frozen=True)
class LocalRDToolScope:
    tenant_id: str
    project_id: str
    task_id: str
    run_id: str
    allowed_paths: tuple[str, ...]
    workflow_step_id: str = ""

    def __post_init__(self) -> None:
        if not all((self.tenant_id, self.project_id, self.task_id, self.run_id, self.allowed_paths)):
            raise ValueError("complete local tool scope is required")


class LocalRDToolset:
    """Five fixed local tools. Scope and allowlists are supplied by the server."""

    def __init__(
        self,
        scope: LocalRDToolScope,
        event_log: EvolutionEventLog,
        command_registry: dict[str, tuple[str, ...]] | None = None,
        *,
        sandbox_mode: SandboxMode | str | None = None,
    ) -> None:
        root = _resolve_workspace_root(_WORKSPACE_ROOT_OVERRIDE)
        root_stat = root.stat()
        self.root = root
        self._root_identity = (root_stat.st_dev, root_stat.st_ino)
        self.scope = scope
        self.event_log = event_log
        self.allowed_paths = frozenset(self._normalize_allowlist(scope.allowed_paths))
        self.command_registry = self._validate_command_registry(command_registry or {})
        # sandbox 网络隔离模式：仅关键字、默认 None（解析为 auto）。向后兼容：
        # command_registry 保持位置参数。
        self.sandbox_mode = _resolve_sandbox_mode(sandbox_mode)

    def functions(self) -> dict[str, Callable[[str], dict[str, Any]]]:
        return {
            "tl_ai_rd_file_reader": self.read_file,
            "tl_ai_rd_code_docs_search": self.search,
            "tl_ai_rd_file_writer": self.apply_diff,
            "tl_ai_rd_test_runner": self.run_test,
            "tl_ai_rd_git_client": self.git_read,
        }

    def read_file(self, raw: str) -> dict[str, Any]:
        def action() -> tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]:
            payload = self._payload(raw, {"path"})
            relative, path = self._approved_file(payload["path"])
            data = self._read_text(path, _MAX_READ_BYTES)
            self._reject_sensitive(data)
            lines = [
                {"line": number, "text": line[:512], "truncated": len(line) > 512}
                for number, line in enumerate(data.splitlines(), start=1)
            ]
            return {
                "path": relative,
                "lines": lines,
                "ends_with_newline": data.endswith("\n"),
                "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
            }, {"path": relative}, None

        return self._execute("tl_ai_rd_file_reader", action)

    def search(self, raw: str) -> dict[str, Any]:
        def action() -> tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]:
            payload = self._payload(raw, {"query"})
            query = payload["query"]
            if not isinstance(query, str) or not query or len(query.encode("utf-8")) > _MAX_PATTERN_BYTES:
                raise LocalRDToolError("search_pattern_invalid", "search pattern is invalid")
            scanned = 0
            matches: list[dict[str, Any]] = []
            for relative in sorted(self.allowed_paths):
                _, path = self._approved_file(relative)
                size = path.stat().st_size
                scanned += size
                if scanned > _MAX_SEARCH_BYTES:
                    raise LocalRDToolError("search_limit_exceeded", "search scan limit exceeded")
                text = self._read_text(path, _MAX_SEARCH_BYTES)
                for number, line in enumerate(text.splitlines(), start=1):
                    if query not in line:
                        continue
                    snippet = line[:512]
                    self._reject_sensitive(snippet)
                    matches.append({"path": relative, "line": number, "text": snippet})
                    if len(matches) >= _MAX_SEARCH_RESULTS:
                        return {"matches": matches, "truncated": True}, {"path_hash": self._path_hash()}, None
            return {"matches": matches, "truncated": False}, {"path_hash": self._path_hash()}, None

        return self._execute("tl_ai_rd_code_docs_search", action)

    def apply_diff(self, raw: str) -> dict[str, Any]:
        result, _ = self._apply_diff_transactional(raw)
        return result

    def _apply_diff_transactional(
        self, raw: str
    ) -> tuple[dict[str, Any], Callable[[], None]]:
        def action() -> tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]:
            payload = self._payload(raw, {"diff", "preimage_hashes"})
            diff = payload["diff"]
            hashes = payload["preimage_hashes"]
            if not isinstance(diff, str) or not isinstance(hashes, dict):
                raise LocalRDToolError("diff_invalid", "unified diff is invalid")
            changes = self._build_changes(diff, hashes)
            rollback = self._atomic_write(changes)
            summary = [
                {
                    "path": item[0],
                    "preimage_hash": hashlib.sha256(item[2]).hexdigest(),
                    "postimage_hash": hashlib.sha256(item[3]).hexdigest(),
                }
                for item in changes
            ]
            fields = {
                "path_hash": self._hash_text("\n".join(item[0] for item in changes)),
                "preimage_hash": self._hash_text("\n".join(item["preimage_hash"] for item in summary)),
                "postimage_hash": self._hash_text("\n".join(item["postimage_hash"] for item in summary)),
            }
            return {"files": summary}, fields, rollback

        result, rollback = self._execute(
            "tl_ai_rd_file_writer", action, retain_rollback=True
        )
        if rollback is None:
            raise LocalRDToolError("rollback_unavailable", "writer rollback is unavailable")
        return result, rollback

    def run_test(self, raw: str) -> dict[str, Any]:
        def action() -> tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]:
            payload = self._payload(raw, {"command_id"})
            command_id = payload["command_id"]
            # fail-closed：未注册命令先于 sandbox 检查拒绝（与既有行为一致）。
            if not isinstance(command_id, str) or command_id not in self.command_registry:
                raise LocalRDToolError("command_not_registered", "command_id is not registered")
            # 网络隔离降级逻辑（解除对 sandbox-exec 的硬依赖）：
            # - ENFORCE 且 sandbox 缺失 → 拒绝（强制隔离，fail-closed）。
            # - 其余模式按 sandbox 实际存在性决定走/不走隔离。
            # - AUTO 缺失视为降级（degraded），审计额外标记 sandbox_degraded。
            sandbox_bin = Path("/usr/bin/sandbox-exec")
            present = sandbox_bin.is_file()
            if self.sandbox_mode == SandboxMode.ENFORCE and not present:
                raise LocalRDToolError(
                    "sandbox_unavailable", "network isolation is required but unavailable"
                )
            use_sandbox = (self.sandbox_mode != SandboxMode.OFF) and present
            degraded = (self.sandbox_mode == SandboxMode.AUTO) and (not present)
            with tempfile.TemporaryDirectory(prefix="curis-rd-tool-") as temp_dir:
                if use_sandbox:
                    profile = "(version 1)\n(allow default)\n(deny network*)\n"
                    argv = (str(sandbox_bin), "-p", profile, *self.command_registry[command_id])
                else:
                    argv = tuple(self.command_registry[command_id])
                # argv 已含（或不含）sandbox 前缀，故交给 _run_process 时不再包装。
                completed = self._run_process(argv, temp_dir, use_sandbox=False)
            output = self._safe_process_output(completed)
            if completed[0] != 0:
                raise LocalRDToolError("command_failed", "registered command failed", exit_code=completed[0])
            return (
                {"command_id": command_id, "exit_code": 0, "output": output},
                {"command_id": command_id, "exit_code": 0, "sandbox_degraded": degraded},
                None,
            )

        return self._execute("tl_ai_rd_test_runner", action)

    def git_read(self, raw: str) -> dict[str, Any]:
        def action() -> tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]:
            payload = self._payload(raw, {"operation"})
            operation = payload["operation"]
            commands = {
                "status": ("/usr/bin/git", "-C", str(self.root), "status", "--short", "--", *sorted(self.allowed_paths)),
                "diff": (
                    "/usr/bin/git", "-C", str(self.root), "diff", "--no-ext-diff", "--no-textconv",
                    "--", *sorted(self.allowed_paths),
                ),
                "diff_check": (
                    "/usr/bin/git", "-C", str(self.root), "diff", "--check", "--", *sorted(self.allowed_paths),
                ),
            }
            if operation not in commands:
                raise LocalRDToolError("git_operation_forbidden", "git operation is not allowed")
            with tempfile.TemporaryDirectory(prefix="curis-rd-git-") as temp_dir:
                completed = self._run_process(commands[operation], temp_dir)
            output = self._safe_process_output(completed)
            if completed[0] != 0:
                raise LocalRDToolError("git_read_failed", "read-only git operation failed", exit_code=completed[0])
            return (
                {"operation": operation, "exit_code": 0, "output": output, "output_hash": self._hash_text(output)},
                {"path_hash": self._path_hash(), "exit_code": 0},
                None,
            )

        return self._execute("tl_ai_rd_git_client", action)

    def _execute(
        self,
        tool_id: str,
        action: Callable[[], tuple[dict[str, Any], dict[str, Any], Callable[[], None] | None]],
        *,
        retain_rollback: bool = False,
    ) -> Any:
        self._assert_root()
        # B 层运行时治理 · 通用前置闸（G2 防御性 chokepoint）。
        # 本地 5 工具均为 external=False → 自治边界满足 → 恒放行（安全直通，绝不阻断）。
        self._governance_precheck()
        request_id = str(uuid.uuid4())
        started = time.monotonic()
        self._audit(tool_id, request_id, "started", "", None, 0, {})
        rollback: Callable[[], None] | None = None
        try:
            output, fields, rollback = action()
        except LocalRDToolError as error:
            duration_ms = int((time.monotonic() - started) * 1000)
            try:
                self._audit(
                    tool_id, request_id, "rejected", error.failure_code, error.exit_code, duration_ms, {}
                )
            except Exception as audit_error:
                raise LocalRDToolError("audit_failed", "tool audit is unavailable") from audit_error
            raise
        except Exception as error:
            duration_ms = int((time.monotonic() - started) * 1000)
            try:
                self._audit(tool_id, request_id, "failed", "tool_failed", None, duration_ms, {})
            except Exception as audit_error:
                raise LocalRDToolError("audit_failed", "tool audit is unavailable") from audit_error
            raise LocalRDToolError("tool_failed", "local tool failed") from error
        duration_ms = int((time.monotonic() - started) * 1000)
        try:
            self._audit(tool_id, request_id, "succeeded", "", fields.get("exit_code"), duration_ms, fields)
        except Exception as audit_error:
            if rollback is not None:
                try:
                    rollback()
                except Exception as rollback_error:
                    raise LocalRDToolError(
                        "audit_rollback_failed", "tool audit failed and rollback was not completed"
                    ) from rollback_error
            raise LocalRDToolError("audit_failed", "tool audit is unavailable") from audit_error
        response = {
            "output": output,
            "cost": 0,
            "capability_type": "tool",
            "capability_id": tool_id,
            "capability_source": "official",
            "total_tokens": 0,
            "estimated_cost": 0,
            "cost_source": "local_tool_no_model",
            "outbound_attempted": False,
            "request_id": request_id,
            "tenant_id": self.scope.tenant_id,
            "project_id": self.scope.project_id,
            "task_id": self.scope.task_id,
            "workflow_run_id": self.scope.run_id,
            "workflow_step_id": self.scope.workflow_step_id,
            "status": "succeeded",
        }
        return (response, rollback) if retain_rollback else response

    def _audit(
        self,
        tool_id: str,
        request_id: str,
        outcome: str,
        failure_code: str,
        exit_code: int | None,
        duration_ms: int,
        fields: dict[str, Any],
    ) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "tool_id": tool_id,
            "request_id": request_id,
            "run_id": self.scope.run_id,
            "workflow_run_id": self.scope.run_id,
            "workflow_step_id": self.scope.workflow_step_id,
            "tenant_id": self.scope.tenant_id,
            "project_id": self.scope.project_id,
            "task_id": self.scope.task_id,
            "outcome": outcome,
            "failure_code": failure_code,
            "exit_code": exit_code,
            "duration_ms": duration_ms,
            "timestamp": timestamp,
            "capability_type": "tool",
            "capability_id": tool_id,
            "capability_source": "official",
            "outbound_attempted": False,
            **fields,
        }
        event_type = "usage.tool_call" if outcome != "started" else "tool.audit"
        self.event_log.record(
            correlation_id=self.scope.run_id,
            event_type=event_type,
            tenant_id=self.scope.tenant_id,
            idempotency_key=f"{request_id}:{outcome}",
            payload=payload,
        )

    def _normalize_allowlist(self, paths: tuple[str, ...]) -> list[str]:
        normalized = []
        for raw in paths:
            relative = self._normalize_relative(raw)
            self._reject_forbidden_path(relative)
            normalized.append(relative)
        if len(set(normalized)) != len(normalized):
            raise ValueError("duplicate allowed path")
        return normalized

    def _approved_file(self, raw: Any, *, must_exist: bool = True) -> tuple[str, Path]:
        if not isinstance(raw, str):
            raise LocalRDToolError("path_invalid", "relative path is invalid")
        relative = self._normalize_relative(raw)
        self._reject_forbidden_path(relative)
        if relative not in self.allowed_paths:
            raise LocalRDToolError("path_not_allowed", "path is outside the approved allowlist")
        path = self.root / relative
        parent = path.parent.resolve(strict=True)
        if parent != self.root and self.root not in parent.parents:
            raise LocalRDToolError("path_outside_workspace", "path is outside the workspace")
        current = self.root
        for part in PurePosixPath(relative).parts[:-1]:
            current /= part
            if current.is_symlink():
                raise LocalRDToolError("symlink_forbidden", "symbolic links are not allowed")
        if path.exists() or path.is_symlink():
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise LocalRDToolError("symlink_forbidden", "symbolic links are not allowed")
            if not stat.S_ISREG(info.st_mode):
                raise LocalRDToolError("file_type_forbidden", "only regular files are allowed")
            if info.st_nlink != 1:
                raise LocalRDToolError("hardlink_forbidden", "hard links are not allowed")
        elif must_exist:
            raise LocalRDToolError("file_missing", "approved file does not exist")
        return relative, path

    @staticmethod
    def _normalize_relative(raw: str) -> str:
        if not isinstance(raw, str) or not raw or "\x00" in raw or "\\" in raw:
            raise LocalRDToolError("path_invalid", "relative path is invalid")
        path = PurePosixPath(raw)
        if path.is_absolute() or any(part in {"", ".", ".."} for part in raw.split("/")):
            raise LocalRDToolError("path_invalid", "relative path is invalid")
        return path.as_posix()

    @staticmethod
    def _reject_forbidden_path(relative: str) -> None:
        path = PurePosixPath(relative)
        lower_parts = [part.lower() for part in path.parts]
        name = lower_parts[-1]
        if (
            any(part in _FORBIDDEN_DIRS for part in lower_parts)
            or name == ".env"
            or name.startswith(".env.")
            or Path(name).suffix in _FORBIDDEN_SUFFIXES
            or _FORBIDDEN_NAME.search(name)
        ):
            raise LocalRDToolError("sensitive_path_forbidden", "sensitive path is not allowed")

    def _assert_root(self) -> None:
        root = _resolve_workspace_root(_WORKSPACE_ROOT_OVERRIDE)
        info = root.stat()
        if root != self.root or (info.st_dev, info.st_ino) != self._root_identity:
            raise LocalRDToolError("workspace_root_changed", "approved workspace root changed")

    def _governance_precheck(self) -> None:
        """B 层运行时治理前置评估（防御性）。

        本地工具恒为安全直通：``external=False`` 满足自治边界 → ``needs_gate=False``，
        绝不阻断既有 ``_audit`` / ``_reject_sensitive`` / ``_reject_forbidden_path`` /
        sandbox 网络隔离逻辑。评估异常也保持直通（fail-safe）。
        """
        try:
            decision = evaluate(
                ActionContext(
                    action_type="tool_call",
                    external=False,
                    in_sandbox=True,
                    in_path_whitelist=True,
                )
            )
        except Exception:  # noqa: BLE001 - 防御性覆盖，绝不阻断本地工具
            return
        # 即便异常命中（理论不会），本地工具仍保持直通。
        if decision.needs_gate:
            return

    @staticmethod
    def _payload(raw: str, expected_keys: set[str]) -> dict[str, Any]:
        def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            if len({key for key, _ in pairs}) != len(pairs):
                raise ValueError("duplicate key")
            return dict(pairs)

        try:
            payload = json.loads(raw, object_pairs_hook=reject_duplicates)
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            raise LocalRDToolError("input_invalid", "tool input is invalid") from error
        if not isinstance(payload, dict) or set(payload) != expected_keys:
            raise LocalRDToolError("input_invalid", "tool input is invalid")
        return payload

    @staticmethod
    def _read_text(path: Path, maximum: int) -> str:
        data = path.read_bytes()
        if len(data) > maximum or b"\x00" in data:
            raise LocalRDToolError("text_limit_exceeded", "text file limit exceeded")
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise LocalRDToolError("non_text_file", "only UTF-8 text files are allowed") from error

    @staticmethod
    def _reject_sensitive(text: str) -> None:
        if _SENSITIVE_VALUE.search(text):
            raise LocalRDToolError("sensitive_value_detected", "sensitive value detected")

    def _build_changes(
        self, diff: str, hashes: dict[str, Any]
    ) -> list[tuple[str, Path, bytes, bytes, int]]:
        encoded = diff.encode("utf-8")
        if not diff or len(encoded) > _MAX_DIFF_BYTES or "\x00" in diff:
            raise LocalRDToolError("diff_invalid", "unified diff is invalid")
        lines = diff.splitlines(keepends=True)
        index = 0
        changes: list[tuple[str, Path, bytes, bytes, int]] = []
        seen: set[str] = set()
        while index < len(lines):
            if not lines[index].startswith("--- ") or index + 1 >= len(lines) or not lines[index + 1].startswith("+++ "):
                raise LocalRDToolError("diff_invalid", "unified diff is invalid")
            old_name = lines[index][4:].rstrip("\n")
            new_name = lines[index + 1][4:].rstrip("\n")
            if "\t" in old_name or "\t" in new_name or new_name == "/dev/null":
                raise LocalRDToolError("diff_operation_forbidden", "delete or metadata diff is not allowed")
            old_relative = None if old_name == "/dev/null" else self._strip_diff_prefix(old_name, "a/")
            new_relative = self._strip_diff_prefix(new_name, "b/")
            if old_relative is not None and old_relative != new_relative:
                raise LocalRDToolError("diff_operation_forbidden", "rename is not allowed")
            if new_relative in seen:
                raise LocalRDToolError("diff_invalid", "duplicate diff path")
            seen.add(new_relative)
            if len(seen) > _MAX_DIFF_FILES:
                raise LocalRDToolError("diff_limit_exceeded", "diff file limit exceeded")
            relative, path = self._approved_file(new_relative, must_exist=old_relative is not None)
            before = path.read_bytes() if path.exists() else b""
            try:
                before_text = before.decode("utf-8")
            except UnicodeDecodeError as error:
                raise LocalRDToolError("non_text_file", "only UTF-8 text files are allowed") from error
            expected_hash = hashes.get(relative)
            if set(hashes) - self.allowed_paths or not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                raise LocalRDToolError("preimage_hash_invalid", "preimage hash is invalid")
            if hashlib.sha256(before).hexdigest() != expected_hash:
                raise LocalRDToolError("preimage_hash_mismatch", "preimage hash does not match")
            index += 2
            hunks: list[tuple[re.Match[str], list[str]]] = []
            while index < len(lines) and not lines[index].startswith("--- "):
                match = _HUNK.match(lines[index])
                if match is None:
                    raise LocalRDToolError("diff_invalid", "unified diff is invalid")
                index += 1
                body: list[str] = []
                while index < len(lines) and not lines[index].startswith(("@@ ", "--- ")):
                    if lines[index].startswith("\\ No newline at end of file") or not lines[index].startswith((" ", "+", "-")):
                        raise LocalRDToolError("diff_invalid", "unified diff is invalid")
                    body.append(lines[index])
                    index += 1
                hunks.append((match, body))
            after_text = self._apply_hunks(before_text, hunks)
            self._reject_sensitive(after_text)
            mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
            changes.append((relative, path, before, after_text.encode("utf-8"), mode))
        if set(hashes) != {item[0] for item in changes}:
            raise LocalRDToolError("preimage_hash_invalid", "preimage hashes do not match diff paths")
        return changes

    @staticmethod
    def _strip_diff_prefix(value: str, prefix: str) -> str:
        if not value.startswith(prefix):
            raise LocalRDToolError("diff_invalid", "unified diff path is invalid")
        return value[len(prefix):]

    @staticmethod
    def _apply_hunks(before: str, hunks: list[tuple[re.Match[str], list[str]]]) -> str:
        source = before.splitlines(keepends=True)
        output: list[str] = []
        cursor = 0
        for match, body in hunks:
            old_start = int(match.group(1))
            old_count = int(match.group(2) or 1)
            new_count = int(match.group(4) or 1)
            start = 0 if old_start == 0 else old_start - 1
            if start < cursor or start > len(source):
                raise LocalRDToolError("diff_context_mismatch", "diff context does not match")
            output.extend(source[cursor:start])
            cursor = start
            consumed = produced = 0
            for line in body:
                marker, text = line[0], line[1:]
                if marker in {" ", "-"}:
                    if cursor >= len(source) or source[cursor] != text:
                        raise LocalRDToolError("diff_context_mismatch", "diff context does not match")
                    cursor += 1
                    consumed += 1
                if marker in {" ", "+"}:
                    output.append(text)
                    produced += 1
            if consumed != old_count or produced != new_count:
                raise LocalRDToolError("diff_invalid", "diff hunk count is invalid")
        output.extend(source[cursor:])
        return "".join(output)

    @staticmethod
    def _atomic_write(
        changes: list[tuple[str, Path, bytes, bytes, int]]
    ) -> Callable[[], None]:
        applied: list[tuple[Path, bytes, int, bool]] = []

        def replace(path: Path, data: bytes, mode: int) -> None:
            fd, temp_name = tempfile.mkstemp(prefix=".curis-rd-", dir=path.parent)
            try:
                os.fchmod(fd, mode)
                with os.fdopen(fd, "wb", closefd=True) as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp_name, path)
            except Exception:
                try:
                    os.close(fd)
                except OSError:
                    pass
                Path(temp_name).unlink(missing_ok=True)
                raise

        def rollback() -> None:
            for path, before, mode, existed in reversed(applied):
                if existed:
                    replace(path, before, mode)
                else:
                    path.unlink(missing_ok=True)

        try:
            for _, path, before, after, mode in changes:
                existed = path.exists()
                replace(path, after, mode)
                applied.append((path, before, mode, existed))
        except Exception:
            rollback()
            raise
        return rollback

    def _validate_command_registry(
        self, registry: dict[str, tuple[str, ...]]
    ) -> dict[str, tuple[str, ...]]:
        approved: dict[str, tuple[str, ...]] = {}
        compile_command = ("backend/.venv/bin/python", "-m", "compileall", "-q", "backend/app")
        for command_id, command in registry.items():
            if not isinstance(command_id, str) or not command_id or not isinstance(command, tuple):
                raise ValueError("registered command is invalid")
            if command == compile_command:
                approved[command_id] = command
                continue
            if len(command) == 5 and command[:4] == (
                "backend/.venv/bin/python", "-m", "pytest", "-q"
            ):
                test_path = command[4]
                if (
                    test_path in self.allowed_paths
                    and PurePosixPath(test_path).parent == PurePosixPath("backend/tests")
                    and PurePosixPath(test_path).name.startswith("test_")
                    and PurePosixPath(test_path).suffix == ".py"
                ):
                    approved[command_id] = command
                    continue
            raise ValueError("registered command is outside the approved command families")
        return approved

    def _run_process(
        self, command: tuple[str, ...], temp_dir: str, use_sandbox: bool = True
    ) -> tuple[int, bytes, bytes]:
        # 注：真实 sandbox-exec 包装的拼接责任在调用方（run_test）完成；
        # 此处 _run_process 始终按给定 argv 直接执行。``use_sandbox`` 仅作为
        # 接口对称位保留（默认 True，保持既有行为），当前实现不自行改写 argv。
        # 其它调用方（read_file / apply_diff / search / git_read）保持默认
        # use_sandbox=True，行为完全不变。
        environment = {
            "PATH": "/usr/bin:/bin",
            "HOME": temp_dir,
            "TMPDIR": temp_dir,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "NO_PROXY": "*",
            "no_proxy": "*",
        }
        process = subprocess.Popen(
            command,
            cwd=self.root,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=_PROCESS_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as error:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            raise LocalRDToolError("command_timeout", "local command timed out") from error
        return process.returncode, stdout, stderr

    def _safe_process_output(self, completed: tuple[int, bytes, bytes]) -> str:
        data = completed[1] + completed[2]
        if len(data) > _MAX_PROCESS_OUTPUT or b"\x00" in data:
            raise LocalRDToolError("process_output_rejected", "process output limit exceeded")
        try:
            output = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise LocalRDToolError("process_output_rejected", "process output is not UTF-8") from error
        self._reject_sensitive(output)
        return output

    def _path_hash(self) -> str:
        return self._hash_text("\n".join(sorted(self.allowed_paths)))

    @staticmethod
    def _hash_text(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
