"""Issue A · P0-2 唤醒请求与会话续接（Wake / Session）。

持久化「唤醒一个 Agent 去执行某个 Task」的请求，以及「一次运行会话」的状态机，
支持：

- **唤醒合并 / 幂等**：同 ``idempotency_key`` 仍 ``pending`` → ``coalesced_count+1``
  返回既有（不双执行）；否则插入 ``pending``。
- **状态机**：``pending → claimed → completed|failed``（wake）；
  ``pending → running → completed|failed|recovered|expired``（session）。
- **断点恢复**：``recover(parent, owner)`` 基于 parent 最近 checkpoint 建新会话
  （``status=recovered``，携带 ``parent_session_id``）；若运行配置指纹变化 →
  抛 ``AgentTaskSessionError("session_config_mismatch")``（禁止续旧）。
- **可重放**：``replay(session)`` 返回 ``{checkpoint, config_fingerprint}``。

铁律（与架构设计一致）：
1. **零新依赖**：仅标准库（``sqlite3`` / ``threading`` / ``uuid`` / ``json`` /
   ``datetime`` / ``typing`` / ``dataclasses``）+ 复用 ``Database``。
2. **原子性**：所有写用 ``BEGIN IMMEDIATE`` + 条件更新。
3. **脱敏贯穿**：错误仅携带固定 ``failure_code``；落库 payload 仅含
   scope / status / 指纹 / 范围键，无路径 / Key / 参数 / 原始 Secret。
4. **不触 L2 / 不解除 ``LOCKED_ACTIONS``**：本模块不 import / 不调用任何
   解除 A 层锁定的路径；不引入计费 / 多租户 / 商业。
"""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from .database import Database
from .agent_execution_kernel import (  # noqa: E402
    DEFAULT_REAP_INTERVAL_SECONDS,
    DEFAULT_SESSION_TTL_SECONDS,
    DEFAULT_WAKE_TTL_SECONDS,
    load_kernel_config,
)


# ---------------------------------------------------------------------------
# 时间助手（复用 B 层 _now_iso() 风格）
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except Exception:  # noqa: BLE001 - 非法时间视为缺失
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _expired_at(expires_at: str | None) -> bool:
    dt = _parse_iso(expires_at)
    if dt is None:
        return False
    return dt < datetime.now(timezone.utc)


def _now_plus_seconds(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


# ---------------------------------------------------------------------------
# 记录 dataclass
# ---------------------------------------------------------------------------
@dataclass
class WakeRequestRecord:
    """``agent_wakeup_requests`` 表行的映射（脱敏）。"""

    request_id: str
    idempotency_key: str
    scope: str
    agent_id: str
    task_id: str
    status: str  # pending|claimed|completed|failed|cancelled|coalesced
    coalesced_count: int = 1
    config_fingerprint: str = ""
    claimed_by: str = ""
    claimed_at: str = ""
    finished_at: str = ""
    error_code: str = ""
    tenant_id: str = ""
    correlation_id: str = ""
    expires_at: str = ""
    created_at: str = ""


@dataclass
class AgentTaskSessionRecord:
    """``agent_task_sessions`` 表行的映射（脱敏）。"""

    session_id: str
    scope: str
    agent_id: str
    task_id: str
    status: str  # pending|running|completed|failed|recovered|expired
    config_fingerprint: str = ""
    execution_claim_id: str = ""
    wake_request_id: str = ""
    checkpoint: str = "{}"  # JSON
    parent_session_id: str = ""
    owner: str = ""
    started_at: str = ""
    last_active_at: str = ""
    finished_at: str = ""
    expires_at: str = ""
    error_code: str = ""
    tenant_id: str = ""
    correlation_id: str = ""
    created_at: str = ""


class WakeRequestError(Exception):
    """脱敏错误：仅携带固定 ``failure_code``。"""

    def __init__(self, failure_code: str, *, message: str | None = None) -> None:
        self.failure_code = failure_code
        super().__init__(message or "wake request operation failed")


class AgentTaskSessionError(Exception):
    """脱敏错误：仅携带固定 ``failure_code``。"""

    def __init__(self, failure_code: str, *, message: str | None = None) -> None:
        self.failure_code = failure_code
        super().__init__(message or "agent task session operation failed")


# ---------------------------------------------------------------------------
# DDL
# ---------------------------------------------------------------------------
_WAKE_DDL = """
CREATE TABLE IF NOT EXISTS agent_wakeup_requests (
    request_id       TEXT PRIMARY KEY,
    idempotency_key TEXT,
    scope            TEXT,
    agent_id         TEXT,
    task_id          TEXT,
    tenant_id        TEXT,
    priority         INTEGER DEFAULT 5,
    status           TEXT,
    coalesced_count  INTEGER DEFAULT 1,
    payload          TEXT,
    config_fingerprint TEXT,
    claimed_by       TEXT,
    claimed_at       TEXT,
    finished_at      TEXT,
    expires_at       TEXT,
    error_code       TEXT,
    correlation_id   TEXT,
    created_at       TEXT
)
"""

_SESSION_DDL = """
CREATE TABLE IF NOT EXISTS agent_task_sessions (
    session_id          TEXT PRIMARY KEY,
    scope               TEXT,
    agent_id            TEXT,
    task_id             TEXT,
    tenant_id           TEXT,
    status              TEXT,
    config_fingerprint  TEXT,
    execution_claim_id TEXT,
    wake_request_id     TEXT,
    checkpoint          TEXT,
    parent_session_id   TEXT,
    owner               TEXT,
    started_at          TEXT,
    last_active_at      TEXT,
    finished_at         TEXT,
    expires_at          TEXT,
    error_code          TEXT,
    correlation_id      TEXT,
    created_at          TEXT
)
"""

_CREATE_WAKE_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_agent_wake_key "
    "ON agent_wakeup_requests(idempotency_key, status)"
)
_CREATE_SESSION_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_agent_session_scope "
    "ON agent_task_sessions(scope, status)"
)

_WAKE_SELECT = (
    "request_id, idempotency_key, scope, agent_id, task_id, status, "
    "coalesced_count, config_fingerprint, claimed_by, claimed_at, "
    "finished_at, error_code, tenant_id, correlation_id, expires_at, created_at"
)
_SESSION_SELECT = (
    "session_id, scope, agent_id, task_id, status, config_fingerprint, "
    "execution_claim_id, wake_request_id, checkpoint, parent_session_id, "
    "owner, started_at, last_active_at, finished_at, expires_at, "
    "error_code, tenant_id, correlation_id, created_at"
)


# ---------------------------------------------------------------------------
# WakeRequestStore
# ---------------------------------------------------------------------------
class WakeRequestStore:
    """唤醒请求存储（幂等合并 + 原子领取 + 状态机）。"""

    def __init__(
        self, database: "Database | str", *, default_ttl_seconds: int | None = None
    ) -> None:
        self._database = database if isinstance(database, Database) else Database(database)
        self.default_ttl_seconds = (
            default_ttl_seconds
            if default_ttl_seconds is not None
            else int(
                load_kernel_config().get("wake_ttl_seconds", DEFAULT_WAKE_TTL_SECONDS)
            )
        )
        self._lock = threading.Lock()
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            with self._database.connect() as conn:
                conn.execute(_WAKE_DDL)
                conn.execute(_SESSION_DDL)
                conn.execute(_CREATE_WAKE_INDEX)
                conn.execute(_CREATE_SESSION_INDEX)

    @staticmethod
    def _wake_row_to_record(row: sqlite3.Row) -> WakeRequestRecord:
        return WakeRequestRecord(
            request_id=row["request_id"],
            idempotency_key=row["idempotency_key"] or "",
            scope=row["scope"],
            agent_id=row["agent_id"],
            task_id=row["task_id"],
            status=row["status"],
            coalesced_count=int(row["coalesced_count"] or 1),
            config_fingerprint=row["config_fingerprint"] or "",
            claimed_by=row["claimed_by"] or "",
            claimed_at=row["claimed_at"] or "",
            finished_at=row["finished_at"] or "",
            error_code=row["error_code"] or "",
            tenant_id=row["tenant_id"] or "",
            correlation_id=row["correlation_id"] or "",
            expires_at=row["expires_at"] or "",
            created_at=row["created_at"] or "",
        )

    # ── 幂等合并创建 ──────────────────────────────────────────────
    def create(
        self,
        scope: str,
        agent_id: str,
        task_id: str,
        *,
        idempotency_key: str,
        priority: int = 5,
        payload: dict,
        config_fingerprint: str = "",
        tenant_id: str = "",
        correlation_id: str = "",
        ttl_seconds: int | None = None,
    ) -> WakeRequestRecord:
        """幂等合并创建唤醒请求。

        - 同 ``idempotency_key`` 仍 ``pending`` → ``coalesced_count+1``
          返回既有（不双执行）。
        - 否则插入 ``pending``（带 TTL）。
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                existing = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE idempotency_key = ? AND status = 'pending' "
                    "ORDER BY created_at DESC LIMIT 1",
                    (idempotency_key,),
                ).fetchone()
                if existing is not None:
                    rec = self._wake_row_to_record(existing)
                    conn.execute(
                        "UPDATE agent_wakeup_requests SET coalesced_count = "
                        "coalesced_count + 1 WHERE request_id = ?",
                        (rec.request_id,),
                    )
                    rec.coalesced_count += 1
                    return rec

                request_id = uuid.uuid4().hex
                now = _now_iso()
                expires_at = _now_plus_seconds(ttl)
                conn.execute(
                    "INSERT INTO agent_wakeup_requests "
                    "(request_id, idempotency_key, scope, agent_id, task_id, "
                    "tenant_id, priority, status, coalesced_count, payload, "
                    "config_fingerprint, claimed_by, claimed_at, finished_at, "
                    "expires_at, error_code, correlation_id, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 1, ?, ?, "
                    "'', '', '', ?, '', ?, ?)",
                    (
                        request_id,
                        idempotency_key,
                        scope,
                        agent_id,
                        task_id,
                        tenant_id or "",
                        int(priority),
                        json.dumps(payload, ensure_ascii=False),
                        config_fingerprint or "",
                        expires_at,
                        correlation_id or "",
                        now,
                    ),
                )
                row = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
        return self._wake_row_to_record(row)

    # ── 原子领取 ────────────────────────────────────────────────
    def claim(
        self, request_id: str, session_id: str, *, ttl_seconds: int | None = None
    ) -> WakeRequestRecord:
        """原子领取：``pending → claimed``（BEGIN IMMEDIATE 条件更新）。

        - 已 ``claimed`` 同 ``session_id`` → 返回既有（幂等）。
        - 他 ``session_id`` 已 ``claimed`` → 抛 ``WakeRequestError("wake_already_claimed")``。
        - 仍 ``pending`` 但已过期 → 抛 ``WakeRequestError("wake_expired")``。
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
                if row is None:
                    raise WakeRequestError("wake_not_found")
                rec = self._wake_row_to_record(row)
                if rec.status == "claimed":
                    if rec.claimed_by == session_id:
                        return rec
                    raise WakeRequestError("wake_already_claimed")
                if rec.status != "pending":
                    raise WakeRequestError("wake_already_claimed")
                if _expired_at(rec.expires_at):
                    raise WakeRequestError("wake_expired")
                now = _now_iso()
                expires_at = _now_plus_seconds(ttl)
                conn.execute(
                    "UPDATE agent_wakeup_requests SET status = 'claimed', "
                    "claimed_by = ?, claimed_at = ?, expires_at = ? "
                    "WHERE request_id = ?",
                    (session_id, now, expires_at, request_id),
                )
                updated = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
        return self._wake_row_to_record(updated)

    # ── 完成 / 取消 ───────────────────────────────────────────
    def complete(
        self, request_id: str, *, outcome: str, error_code: str = ""
    ) -> WakeRequestRecord:
        """``claimed → completed|failed``。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
                if row is None:
                    raise WakeRequestError("wake_not_found")
                rec = self._wake_row_to_record(row)
                if rec.status not in ("claimed", "pending"):
                    raise WakeRequestError("wake_already_claimed")
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_wakeup_requests SET status = ?, "
                    "finished_at = ?, error_code = ? WHERE request_id = ?",
                    (outcome, now, error_code or "", request_id),
                )
                updated = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
        out = self._wake_row_to_record(updated)
        out.status = outcome
        out.finished_at = now
        out.error_code = error_code or ""
        return out

    def cancel(self, request_id: str, *, reason: str = "") -> WakeRequestRecord:
        """``pending|claimed → cancelled``（幂等 no-op 终态）。"""
        with self._lock:
            with self._database.connect() as conn:
                row = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
                if row is None:
                    raise WakeRequestError("wake_not_found")
                rec = self._wake_row_to_record(row)
                if rec.status in ("completed", "failed", "cancelled"):
                    return rec
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_wakeup_requests SET status = 'cancelled', "
                    "finished_at = ?, error_code = ? WHERE request_id = ?",
                    (now, reason or "", request_id),
                )
                updated = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
        out = self._wake_row_to_record(updated)
        out.status = "cancelled"
        return out

    # ── 查询 ──────────────────────────────────────────────────
    def get(self, request_id: str) -> "WakeRequestRecord | None":
        with self._lock:
            with self._database.connect() as conn:
                row = conn.execute(
                    f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
                    "WHERE request_id = ?",
                    (request_id,),
                ).fetchone()
        if row is None:
            return None
        return self._wake_row_to_record(row)

    def list_pending(
        self, scope: str | None = None, agent_id: str | None = None
    ) -> list[WakeRequestRecord]:
        clauses = ["status = 'pending'"]
        params: list[Any] = []
        if scope is not None:
            clauses.append("scope = ?")
            params.append(scope)
        if agent_id is not None:
            clauses.append("agent_id = ?")
            params.append(agent_id)
        sql = (
            f"SELECT {_WAKE_SELECT} FROM agent_wakeup_requests "
            f"WHERE {' AND '.join(clauses)} ORDER BY created_at DESC"
        )
        with self._lock:
            with self._database.connect() as conn:
                rows = conn.execute(sql, params).fetchall()
        return [self._wake_row_to_record(r) for r in rows]

    # ── 过期清理 ───────────────────────────────────────────────
    def reap_expired(self) -> int:
        """``pending``/``claimed`` 且 ``expires_at < now`` → 终态。

        ``pending → cancelled``；``claimed → expired``。返回清理数量。
        """
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                pending = conn.execute(
                    "UPDATE agent_wakeup_requests SET status = 'cancelled', "
                    "finished_at = ? WHERE status = 'pending' AND expires_at < ?",
                    (_now_iso(), _now_iso()),
                ).rowcount
                claimed = conn.execute(
                    "UPDATE agent_wakeup_requests SET status = 'expired', "
                    "finished_at = ? WHERE status = 'claimed' AND expires_at < ?",
                    (_now_iso(), _now_iso()),
                ).rowcount
        return int(pending + claimed)


# ---------------------------------------------------------------------------
# AgentTaskSessionStore
# ---------------------------------------------------------------------------
class AgentTaskSessionStore:
    """Agent 任务会话存储（状态机 + 续接 + 重放）。"""

    def __init__(
        self, database: "Database | str", *, default_ttl_seconds: int | None = None
    ) -> None:
        self._database = database if isinstance(database, Database) else Database(database)
        self.default_ttl_seconds = (
            default_ttl_seconds
            if default_ttl_seconds is not None
            else int(
                load_kernel_config().get(
                    "session_ttl_seconds", DEFAULT_SESSION_TTL_SECONDS
                )
            )
        )
        self._lock = threading.Lock()
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            with self._database.connect() as conn:
                conn.execute(_WAKE_DDL)
                conn.execute(_SESSION_DDL)
                conn.execute(_CREATE_WAKE_INDEX)
                conn.execute(_CREATE_SESSION_INDEX)

    @staticmethod
    def _session_row_to_record(row: sqlite3.Row) -> AgentTaskSessionRecord:
        return AgentTaskSessionRecord(
            session_id=row["session_id"],
            scope=row["scope"],
            agent_id=row["agent_id"],
            task_id=row["task_id"],
            status=row["status"],
            config_fingerprint=row["config_fingerprint"] or "",
            execution_claim_id=row["execution_claim_id"] or "",
            wake_request_id=row["wake_request_id"] or "",
            checkpoint=row["checkpoint"] or "{}",
            parent_session_id=row["parent_session_id"] or "",
            owner=row["owner"] or "",
            started_at=row["started_at"] or "",
            last_active_at=row["last_active_at"] or "",
            finished_at=row["finished_at"] or "",
            expires_at=row["expires_at"] or "",
            error_code=row["error_code"] or "",
            tenant_id=row["tenant_id"] or "",
            correlation_id=row["correlation_id"] or "",
            created_at=row["created_at"] or "",
        )

    # ── 创建 / 启动 ───────────────────────────────────────────
    def create(
        self,
        scope: str,
        agent_id: str,
        task_id: str,
        *,
        config_fingerprint: str,
        execution_claim_id: str,
        wake_request_id: str,
        owner: str,
        checkpoint: dict | None = None,
        tenant_id: str = "",
        correlation_id: str = "",
        ttl_seconds: int | None = None,
        session_id: str | None = None,
    ) -> AgentTaskSessionRecord:
        """创建会话（→ ``pending``）。"""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        sid = session_id or uuid.uuid4().hex
        now = _now_iso()
        expires_at = _now_plus_seconds(ttl)
        with self._lock:
            with self._database.connect() as conn:
                conn.execute(
                    "INSERT INTO agent_task_sessions "
                    "(session_id, scope, agent_id, task_id, tenant_id, status, "
                    "config_fingerprint, execution_claim_id, wake_request_id, "
                    "checkpoint, parent_session_id, owner, started_at, "
                    "last_active_at, finished_at, expires_at, error_code, "
                    "correlation_id, created_at) "
                    "VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?, '', ?, '', "
                    "?, '', ?, '', ?, ?)",
                    (
                        sid,
                        scope,
                        agent_id,
                        task_id,
                        tenant_id or "",
                        config_fingerprint or "",
                        execution_claim_id or "",
                        wake_request_id or "",
                        json.dumps(checkpoint or {}, ensure_ascii=False),
                        owner or "",
                        now,  # last_active_at
                        expires_at,
                        correlation_id or "",
                        now,  # created_at
                    ),
                )
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (sid,),
                ).fetchone()
        return self._session_row_to_record(row)

    def start(self, session_id: str, owner: str) -> AgentTaskSessionRecord:
        """``pending|recovered → running``；owner 不符 → ``session_owner_mismatch``。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if row is None:
                    raise AgentTaskSessionError("session_not_found")
                rec = self._session_row_to_record(row)
                if rec.status in ("completed", "failed", "expired", "cancelled"):
                    raise AgentTaskSessionError("session_already_terminal")
                if rec.owner and rec.owner != owner:
                    raise AgentTaskSessionError("session_owner_mismatch")
                now = _now_iso()
                started = rec.started_at or now
                conn.execute(
                    "UPDATE agent_task_sessions SET status = 'running', "
                    "owner = ?, started_at = ?, last_active_at = ? "
                    "WHERE session_id = ?",
                    (owner, started, now, session_id),
                )
                updated = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        out = self._session_row_to_record(updated)
        out.status = "running"
        return out

    # ── 续接 / 完成 ──────────────────────────────────────────
    def checkpoint(
        self, session_id: str, owner: str, checkpoint: dict
    ) -> AgentTaskSessionRecord:
        """续接状态 + 刷新 ``last_active_at``；owner 不符 → ``session_owner_mismatch``。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if row is None:
                    raise AgentTaskSessionError("session_not_found")
                rec = self._session_row_to_record(row)
                if rec.status in ("completed", "failed", "expired", "cancelled"):
                    raise AgentTaskSessionError("session_already_terminal")
                if rec.owner and rec.owner != owner:
                    raise AgentTaskSessionError("session_owner_mismatch")
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_task_sessions SET checkpoint = ?, "
                    "last_active_at = ? WHERE session_id = ?",
                    (json.dumps(checkpoint, ensure_ascii=False), now, session_id),
                )
                updated = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        out = self._session_row_to_record(updated)
        out.checkpoint = json.dumps(checkpoint, ensure_ascii=False)
        out.last_active_at = now
        return out

    def complete(
        self, session_id: str, owner: str, *, outcome: str, error_code: str = ""
    ) -> AgentTaskSessionRecord:
        """``running → completed|failed``；owner 不符 → ``session_owner_mismatch``。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if row is None:
                    raise AgentTaskSessionError("session_not_found")
                rec = self._session_row_to_record(row)
                if rec.status in ("completed", "failed", "expired", "cancelled"):
                    raise AgentTaskSessionError("session_already_terminal")
                if rec.owner and rec.owner != owner:
                    raise AgentTaskSessionError("session_owner_mismatch")
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_task_sessions SET status = ?, finished_at = ?, "
                    "error_code = ?, last_active_at = ? WHERE session_id = ?",
                    (outcome, now, error_code or "", now, session_id),
                )
                updated = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        out = self._session_row_to_record(updated)
        out.status = outcome
        out.finished_at = now
        out.error_code = error_code or ""
        return out

    # ── 断点恢复 ─────────────────────────────────────────────
    def recover(
        self,
        parent_session_id: str,
        owner: str,
        *,
        checkpoint: dict | None = None,
    ) -> AgentTaskSessionRecord:
        """断点恢复：基于 parent 最近 checkpoint 建新会话。

        - parent 缺失 → ``session_not_found``。
        - parent 已终态（``completed|failed|cancelled``）→ ``session_already_terminal``。
        - **运行配置指纹变化** → ``session_config_mismatch``（禁止续旧）。新运行指纹
          经 ``checkpoint["_config_fingerprint"]`` 传入与 parent 比对；未传则跳过比
          对（由调用方决定）。
        - 否则建新会话 ``status=recovered``，携带 ``parent_session_id`` 与 parent
          的 ``config_fingerprint``；``start()`` 可将其翻为 ``running``。
        """
        ttl = self.default_ttl_seconds
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (parent_session_id,),
                ).fetchone()
                if row is None:
                    raise AgentTaskSessionError("session_not_found")
                parent = self._session_row_to_record(row)
                if parent.status in ("completed", "failed", "expired", "cancelled"):
                    raise AgentTaskSessionError("session_already_terminal")

                # 配置指纹变化 → 禁止续旧。
                if checkpoint is not None and isinstance(checkpoint, dict):
                    incoming_fp = checkpoint.get("_config_fingerprint")
                    if incoming_fp is not None and incoming_fp != parent.config_fingerprint:
                        raise AgentTaskSessionError("session_config_mismatch")

                session_id = uuid.uuid4().hex
                now = _now_iso()
                expires_at = _now_plus_seconds(ttl)
                new_checkpoint = (
                    checkpoint
                    if checkpoint is not None
                    else _safe_json_loads(parent.checkpoint)
                )
                conn.execute(
                    "INSERT INTO agent_task_sessions "
                    "(session_id, scope, agent_id, task_id, tenant_id, status, "
                    "config_fingerprint, execution_claim_id, wake_request_id, "
                    "checkpoint, parent_session_id, owner, started_at, "
                    "last_active_at, finished_at, expires_at, error_code, "
                    "correlation_id, created_at) "
                    "VALUES (?, ?, ?, ?, ?, 'recovered', ?, ?, ?, ?, ?, ?, '', "
                    "?, '', ?, '', ?, ?)",
                    (
                        session_id,
                        parent.scope,
                        parent.agent_id,
                        parent.task_id,
                        parent.tenant_id,
                        parent.config_fingerprint,
                        parent.execution_claim_id,
                        parent.wake_request_id,
                        json.dumps(new_checkpoint, ensure_ascii=False),
                        parent_session_id,
                        owner,
                        now,  # last_active_at
                        expires_at,
                        parent.correlation_id,
                        now,  # created_at
                    ),
                )
                new_row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        out = self._session_row_to_record(new_row)
        out.status = "recovered"
        out.parent_session_id = parent_session_id
        out.owner = owner
        return out

    def replay(self, session_id: str) -> dict:
        """返回 ``{checkpoint, config_fingerprint}`` 供重跑。"""
        rec = self.get(session_id)
        if rec is None:
            raise AgentTaskSessionError("session_not_found")
        return {
            "checkpoint": _safe_json_loads(rec.checkpoint),
            "config_fingerprint": rec.config_fingerprint,
        }

    # ── 查询 ──────────────────────────────────────────────────
    def get(self, session_id: str) -> "AgentTaskSessionRecord | None":
        with self._lock:
            with self._database.connect() as conn:
                row = conn.execute(
                    f"SELECT {_SESSION_SELECT} FROM agent_task_sessions "
                    "WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
        if row is None:
            return None
        return self._session_row_to_record(row)

    def list_by_scope(
        self, scope: str, active_only: bool = False
    ) -> list[AgentTaskSessionRecord]:
        sql = (
            f"SELECT {_SESSION_SELECT} FROM agent_task_sessions WHERE scope = ?"
        )
        if active_only:
            sql += " AND status IN ('pending', 'running', 'recovered')"
        sql += " ORDER BY created_at DESC"
        with self._lock:
            with self._database.connect() as conn:
                rows = conn.execute(sql, (scope,)).fetchall()
        return [self._session_row_to_record(r) for r in rows]

    # ── 过期清理 ───────────────────────────────────────────────
    def reap_expired(self) -> int:
        """``running`` 且 ``expires_at < now`` → ``expired``。返回清理数量。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                cur = conn.execute(
                    "UPDATE agent_task_sessions SET status = 'expired', "
                    "finished_at = ? WHERE status = 'running' AND expires_at < ?",
                    (_now_iso(), _now_iso()),
                )
                count = cur.rowcount
        return int(count)


def _safe_json_loads(text: str) -> dict:
    try:
        data = json.loads(text or "{}")
    except Exception:  # noqa: BLE001 - 兜底空 dict
        return {}
    return data if isinstance(data, dict) else {}


__all__ = [
    "WakeRequestRecord",
    "AgentTaskSessionRecord",
    "WakeRequestError",
    "AgentTaskSessionError",
    "WakeRequestStore",
    "AgentTaskSessionStore",
]
