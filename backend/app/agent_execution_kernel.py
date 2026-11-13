"""Issue A · P0-1 通用执行锁（ExecutionClaim）。

跨 Task 类型的单执行者保证：同一 ``scope`` 在任意时刻至多一个
``held`` 锁，且锁由 ``owner`` 持有、须凭不透明 ``token`` 才能释放 / 续约。
用于防止重复执行与孤儿锁：

- **幂等获取**：同 ``(scope, owner, token)`` 已 ``held`` → 返回既有
  （不双执行）；他 ``owner`` 正 ``held`` → 抛 ``ExecutionClaimError(
  "claim_already_held")``。
- **TTL / heartbeat**：``held`` 且 ``expires_at > now`` 才视为 active；
  owner 须周期性 ``heartbeat`` / ``renew`` 顺延 ``expires_at``；进程死亡
  → 心跳停 → TTL 过 → ``reap_expired`` 标 ``expired`` → 可重领。
- **强释放**：``force_release`` 可无视 token 将 ``held → force_released``，
  用于运维清孤儿锁（正常路径不调用）。

铁律（与架构设计一致）：
1. **零新依赖**：仅标准库（``sqlite3`` / ``threading`` / ``uuid`` /
   ``json`` / ``datetime`` / ``typing`` / ``dataclasses``）+ 复用 ``Database``。
2. **原子性**：所有写用 ``BEGIN IMMEDIATE`` + 条件更新（沿用
   ``real_rd_executor._claim_once`` 单主占锁范式）。
3. **脱敏贯穿**：错误仅携带固定 ``failure_code``（``claim_already_held`` /
   ``claim_token_mismatch`` / ``claim_not_found`` / ``claim_expired``），无路径 /
   Key / 参数；落库 payload 仅含 scope / status / 指纹 / 范围键。
4. **不触 L2 / 不解除 ``LOCKED_ACTIONS``**：本模块不 import / 不调用任何
   解除 A 层锁定的路径；不引入计费 / 多租户 / 商业。
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


# ---------------------------------------------------------------------------
# 复用既有 Database（接受 Database | str）
# ---------------------------------------------------------------------------
from .database import Database  # noqa: E402

# 默认阈值（与 agent_execution_kernel_config.json 对齐；加载失败回退此处）。
DEFAULT_CLAIM_TTL_SECONDS = 300
DEFAULT_CLAIM_HEARTBEAT_INTERVAL_SECONDS = 60
DEFAULT_WAKE_TTL_SECONDS = 3600
DEFAULT_SESSION_TTL_SECONDS = 3600
DEFAULT_REAP_INTERVAL_SECONDS = 60
EXPIRED_GRACE_SECONDS = 30

# 内核默认开关（接线点 default-off 的单一真源兜底）。
DEFAULT_KERNEL_ENABLED = False

# 配置落点（与 agent_execution_kernel_config.json 对齐）。
_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "agent_execution_kernel_config.json"
)

_DEFAULT_CONFIG: dict[str, Any] = {
    "enabled": False,
    "claim_ttl_seconds": DEFAULT_CLAIM_TTL_SECONDS,
    "claim_heartbeat_interval_seconds": DEFAULT_CLAIM_HEARTBEAT_INTERVAL_SECONDS,
    "wake_ttl_seconds": DEFAULT_WAKE_TTL_SECONDS,
    "session_ttl_seconds": DEFAULT_SESSION_TTL_SECONDS,
    "reap_interval_seconds": DEFAULT_REAP_INTERVAL_SECONDS,
}


def load_kernel_config() -> dict[str, Any]:
    """读取 agent_execution_kernel_config.json（缺省走 _DEFAULT_CONFIG）。

    加载失败 → fail-closed 回退默认配置（绝不抛路径异常）。
    """
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            merged = dict(_DEFAULT_CONFIG)
            merged.update({k: v for k, v in data.items() if k in _DEFAULT_CONFIG})
            return merged
    except Exception:  # noqa: BLE001 - 缺省文件/非法 JSON → 默认
        pass
    return dict(_DEFAULT_CONFIG)


def is_kernel_enabled() -> bool:
    """内核自身默认开关（接线点 master 开关仍以 executor 构造参数为准）。"""
    return bool(load_kernel_config().get("enabled", DEFAULT_KERNEL_ENABLED))


# ---------------------------------------------------------------------------
# 时间助手（复用 B 层 _now_iso() 风格）
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(value: str | None) -> datetime | None:
    """解析 ISO 时间；缺失 / 非法 → ``None``。"""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except Exception:  # noqa: BLE001 - 非法时间视为缺失（读取侧 fail-open）
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _expired_at(expires_at: str | None) -> bool:
    """``expires_at < now`` → True；缺失 / 非法 → False（fail-open 偏保守）。"""
    dt = _parse_iso(expires_at)
    if dt is None:
        return False
    return dt < datetime.now(timezone.utc)


def _now_plus_seconds(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()


# ---------------------------------------------------------------------------
# 记录 / 结果 dataclass
# ---------------------------------------------------------------------------
@dataclass
class ExecutionClaimRecord:
    """``agent_execution_claims`` 表行的映射（脱敏：不含 token）。"""

    claim_id: str
    scope: str
    owner: str
    reason: str
    status: str  # held|released|expired|force_released
    acquired_at: str
    expires_at: str
    last_heartbeat_at: str
    heartbeat_interval_seconds: int
    tenant_id: str = ""
    correlation_id: str = ""


@dataclass
class ClaimResult:
    """``acquire`` 的统一返回（脱敏：仅 ``failure_code``）。"""

    ok: bool
    claim: "ExecutionClaimRecord | None" = None
    failure_code: "str | None" = None  # claim_already_held|claim_token_mismatch|claim_not_found|claim_expired


class ExecutionClaimError(Exception):
    """脱敏错误：仅携带固定 ``failure_code``，无路径 / Key / 参数。"""

    def __init__(self, failure_code: str, *, message: str | None = None) -> None:
        self.failure_code = failure_code
        super().__init__(message or "execution claim operation failed")


# ---------------------------------------------------------------------------
# DDL
# ---------------------------------------------------------------------------
_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS agent_execution_claims (
    claim_id                  TEXT PRIMARY KEY,
    scope                     TEXT,
    owner                     TEXT,
    reason                    TEXT,
    token                     TEXT,
    status                    TEXT,
    acquired_at               TEXT,
    expires_at                TEXT,
    last_heartbeat_at        TEXT,
    heartbeat_interval_seconds INTEGER,
    tenant_id                 TEXT,
    correlation_id            TEXT
)
"""

_CREATE_SCOPE_INDEX = (
    "CREATE INDEX IF NOT EXISTS idx_agent_claims_scope "
    "ON agent_execution_claims(scope, status)"
)

# SELECT 列（刻意不取 token，脱敏返回）。
_SELECT_COLUMNS = (
    "claim_id, scope, owner, reason, status, acquired_at, expires_at, "
    "last_heartbeat_at, heartbeat_interval_seconds, tenant_id, correlation_id"
)


# ---------------------------------------------------------------------------
# ExecutionClaimStore
# ---------------------------------------------------------------------------
class ExecutionClaimStore:
    """通用执行锁存储（sqlite3 + threading.Lock，单执行者保证）。

    ``database`` 接受 ``Database`` 实例或 ``str`` 路径；接线点（如
    ``RealRDExecutor``）传入既有的 ``self.event_log.database``，保证与共享后端
    同库同文件；独立恢复脚本可传 ``str`` 路径。
    """

    def __init__(
        self,
        database: "Database | str",
        *,
        default_ttl_seconds: int | None = None,
        default_heartbeat_interval_seconds: int | None = None,
    ) -> None:
        self._database = database if isinstance(database, Database) else Database(database)
        self.default_ttl_seconds = (
            default_ttl_seconds
            if default_ttl_seconds is not None
            else int(load_kernel_config().get("claim_ttl_seconds", DEFAULT_CLAIM_TTL_SECONDS))
        )
        self.default_heartbeat_interval_seconds = (
            default_heartbeat_interval_seconds
            if default_heartbeat_interval_seconds is not None
            else int(
                load_kernel_config().get(
                    "claim_heartbeat_interval_seconds",
                    DEFAULT_CLAIM_HEARTBEAT_INTERVAL_SECONDS,
                )
            )
        )
        self._lock = threading.Lock()
        self._init_schema()

    # ── 私有助手 ──────────────────────────────────────────────────────
    def _init_schema(self) -> None:
        with self._lock:
            with self._database.connect() as conn:
                conn.execute(_TABLE_DDL)
                conn.execute(_CREATE_SCOPE_INDEX)

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> ExecutionClaimRecord:
        return ExecutionClaimRecord(
            claim_id=row["claim_id"],
            scope=row["scope"],
            owner=row["owner"],
            reason=row["reason"],
            status=row["status"],
            acquired_at=row["acquired_at"],
            expires_at=row["expires_at"],
            last_heartbeat_at=row["last_heartbeat_at"],
            heartbeat_interval_seconds=int(row["heartbeat_interval_seconds"] or 0),
            tenant_id=row["tenant_id"] or "",
            correlation_id=row["correlation_id"] or "",
        )

    # ── 幂等获取 ────────────────────────────────────────────────────
    def acquire(
        self,
        scope: str,
        owner: str,
        reason: str,
        *,
        ttl_seconds: int | None = None,
        heartbeat_interval_seconds: int | None = None,
        token: str,
        tenant_id: str = "",
        correlation_id: str = "",
    ) -> ExecutionClaimRecord:
        """幂等获取执行锁。

        - 同 ``(scope, owner, token)`` 已 ``held`` → 返回既有（不双执行）。
        - 他 ``owner`` 正 ``held`` → 抛 ``ExecutionClaimError("claim_already_held")``。
        - 同 ``scope`` 同 ``owner`` 但 ``token`` 不符 → 抛
          ``ExecutionClaimError("claim_token_mismatch")``（fail-closed）。
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        hb = (
            heartbeat_interval_seconds
            if heartbeat_interval_seconds is not None
            else self.default_heartbeat_interval_seconds
        )
        with self._lock:
            with self._database.connect() as conn:
                # 单主占锁：BEGIN IMMEDIATE + 条件读取。
                conn.execute("begin immediate")
                existing = conn.execute(
                    f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
                    "WHERE scope = ? AND status = 'held' AND expires_at > ? "
                    "ORDER BY acquired_at DESC LIMIT 1",
                    (scope, _now_iso()),
                ).fetchone()
                if existing is not None:
                    rec = self._row_to_record(existing)
                    if rec.owner != owner:
                        # 他 owner 正 held → 禁止双执行。
                        raise ExecutionClaimError("claim_already_held")
                    # 同 owner：须 token 匹配才视为幂等重领。
                    stored = conn.execute(
                        "SELECT token FROM agent_execution_claims "
                        "WHERE claim_id = ?",
                        (rec.claim_id,),
                    ).fetchone()
                    if stored is None or stored["token"] != token:
                        raise ExecutionClaimError("claim_token_mismatch")
                    return rec

                # 无冲突 held → 插入新锁。
                claim_id = uuid.uuid4().hex
                now = _now_iso()
                expires_at = _now_plus_seconds(ttl)
                conn.execute(
                    "INSERT INTO agent_execution_claims "
                    "(claim_id, scope, owner, reason, token, status, acquired_at, "
                    "expires_at, last_heartbeat_at, heartbeat_interval_seconds, "
                    "tenant_id, correlation_id) "
                    "VALUES (?, ?, ?, ?, ?, 'held', ?, ?, ?, ?, ?, ?)",
                    (
                        claim_id,
                        scope,
                        owner,
                        reason,
                        token,
                        now,
                        expires_at,
                        now,
                        int(hb),
                        tenant_id or "",
                        correlation_id or "",
                    ),
                )
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
        return self._row_to_record(row)

    # ── 释放 / 续约 / 心跳 ───────────────────────────────────────
    def release(self, claim_id: str, token: str) -> ExecutionClaimRecord:
        """仅 owner + token 可释放；非持有 / 令牌错 → 抛错。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS}, token FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
                if row is None:
                    raise ExecutionClaimError("claim_not_found")
                if row["status"] != "held":
                    raise ExecutionClaimError("claim_not_found")
                if row["token"] != token:
                    raise ExecutionClaimError("claim_token_mismatch")
                conn.execute(
                    "UPDATE agent_execution_claims SET status = 'released' "
                    "WHERE claim_id = ?",
                    (claim_id,),
                )
                out = self._row_to_record(row)
                out.status = "released"
        return out

    def renew(
        self,
        claim_id: str,
        token: str,
        *,
        ttl_seconds: int | None = None,
    ) -> ExecutionClaimRecord:
        """owner 续约：顺延 ``expires_at`` + 刷新 ``last_heartbeat_at``；幂等。"""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS}, token FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
                if row is None:
                    raise ExecutionClaimError("claim_not_found")
                if row["status"] != "held":
                    raise ExecutionClaimError("claim_expired")
                if row["token"] != token:
                    raise ExecutionClaimError("claim_token_mismatch")
                expires_at = _now_plus_seconds(ttl)
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_execution_claims "
                    "SET expires_at = ?, last_heartbeat_at = ? "
                    "WHERE claim_id = ?",
                    (expires_at, now, claim_id),
                )
                out = self._row_to_record(row)
                out.expires_at = expires_at
                out.last_heartbeat_at = now
        return out

    def heartbeat(self, claim_id: str, token: str) -> ExecutionClaimRecord:
        """存活心跳：仅刷新 ``last_heartbeat_at``（不延 TTL，由 renew 延）。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS}, token FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
                if row is None:
                    raise ExecutionClaimError("claim_not_found")
                if row["status"] != "held":
                    raise ExecutionClaimError("claim_expired")
                if row["token"] != token:
                    raise ExecutionClaimError("claim_token_mismatch")
                now = _now_iso()
                conn.execute(
                    "UPDATE agent_execution_claims SET last_heartbeat_at = ? "
                    "WHERE claim_id = ?",
                    (now, claim_id),
                )
                out = self._row_to_record(row)
                out.last_heartbeat_at = now
        return out

    # ── 强释放（清孤儿备用，无视 token） ───────────────────────
    def force_release(
        self, claim_id: str, *, reason: str = "force_release"
    ) -> ExecutionClaimRecord:
        """管理员 / 恢复清孤儿用：无视 token 将 ``held → force_released``。"""
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
                if row is None:
                    raise ExecutionClaimError("claim_not_found")
                conn.execute(
                    "UPDATE agent_execution_claims SET status = 'force_released' "
                    "WHERE claim_id = ?",
                    (claim_id,),
                )
                out = self._row_to_record(row)
                out.status = "force_released"
        return out

    # ── 查询 ─────────────────────────────────────────────────────
    def is_held(self, scope: str) -> bool:
        """``status == held`` 且 ``expires_at > now`` → True。"""
        with self._lock:
            with self._database.connect() as conn:
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
                    "WHERE scope = ? AND status = 'held' AND expires_at > ? "
                    "LIMIT 1",
                    (scope, _now_iso()),
                ).fetchone()
        return row is not None

    def get(self, claim_id: str) -> "ExecutionClaimRecord | None":
        with self._lock:
            with self._database.connect() as conn:
                row = conn.execute(
                    f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
                    "WHERE claim_id = ?",
                    (claim_id,),
                ).fetchone()
        if row is None:
            return None
        return self._row_to_record(row)

    def list_active(
        self, scope: str | None = None, owner: str | None = None
    ) -> list[ExecutionClaimRecord]:
        """返回所有 ``held`` 且未过期的锁，可按 scope / owner 过滤。"""
        clauses = ["status = 'held'", "expires_at > ?"]
        params: list[Any] = [_now_iso()]
        if scope is not None:
            clauses.append("scope = ?")
            params.append(scope)
        if owner is not None:
            clauses.append("owner = ?")
            params.append(owner)
        sql = (
            f"SELECT {_SELECT_COLUMNS} FROM agent_execution_claims "
            f"WHERE {' AND '.join(clauses)} ORDER BY acquired_at DESC"
        )
        with self._lock:
            with self._database.connect() as conn:
                rows = conn.execute(sql, params).fetchall()
        return [self._row_to_record(r) for r in rows]

    # ── 孤儿锁清理 ───────────────────────────────────────────────
    def reap_expired(self) -> int:
        """``held`` 且 ``expires_at < now`` → ``expired``（TTL 自然过期）。

        返回清理数量。正常续约的锁不会命中；进程死亡导致的孤儿锁
        经此回收后可被新 owner 重领（无双执行）。
        """
        with self._lock:
            with self._database.connect() as conn:
                conn.execute("begin immediate")
                cur = conn.execute(
                    "UPDATE agent_execution_claims SET status = 'expired' "
                    "WHERE status = 'held' AND expires_at < ?",
                    (_now_iso(),),
                )
                count = cur.rowcount
        return count


__all__ = [
    "ExecutionClaimRecord",
    "ClaimResult",
    "ExecutionClaimError",
    "ExecutionClaimStore",
    "DEFAULT_CLAIM_TTL_SECONDS",
    "DEFAULT_CLAIM_HEARTBEAT_INTERVAL_SECONDS",
    "DEFAULT_KERNEL_ENABLED",
]
