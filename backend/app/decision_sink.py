"""B 层运行时治理 · 真实 DecisionSink 后端机制（净新增能力）。

本模块是架构增量 ``docs/architecture/b-layer-runtime-governance-decisionsink.md``
（T-DS1）的核心实现，提供「真实等用户拍板」的后端机制：

- ``PendingDecisionRecord``：持久化行的 dataclass 映射（脱敏 GatePrompt 快照）。
- ``PendingDecisionStore``：sqlite3 + ``threading.Lock`` 持久化；``get_letter`` 为
  fail-closed 单一真源（resolved→回填字母；pending/过期/缺失/cancelled→``"C"``）。
- ``PendingDecisionSink``：非阻塞 sink，``ask(gate, ...)`` 仅写入存储即返回
  ``pending_id``（**不阻塞**，不实现阻塞式 ``DecisionSink`` Protocol）。
- ``PendingDecisionRaised``：接线点向「上层编排」返回的信号（动作尚未执行）。
- ``resolve_decision``：resolver 函数（供未来 Workspace UI/CLI/API 调用）。
- ``PendingDecisionError``：脱敏错误（不携带路径 / Key / 参数）。

铁律（与架构增量一致）：
1. **零新依赖**：仅标准库（``sqlite3`` / ``threading`` / ``time`` / ``uuid`` /
   ``json`` / ``dataclasses`` / ``typing`` / ``datetime``）。
2. **fail-closed 贯穿**：``get_letter`` 单一真源缺失 / 过期 / 取消 → ``"C"``；
   resolver 异常 → 抛 ``PendingDecisionError``，绝不静默放行。
3. **不触 L2**：仅持久化脱敏 GatePrompt 快照 + 决策字母；不引入计费 / 多租户 /
   商业；本模块**不得 import** 任何解除 ``LOCKED_ACTIONS`` 的路径。
4. **脱敏**：落库 ``gate_snapshot`` 为 GatePrompt JSON（禁词红线已在
   ``render_gate_prompt`` enforcement，快照天然不含路径 / Key / 参数）；错误不携
   带任何路径 / Key / 参数。

注意：本模块刻意**不** import ``runtime_governance``（保持 import-light、与既有
``DecisionSink`` 协议解耦）。``PendingDecisionSink`` 经独立 ``pending_sink`` 参数
接线，不污染既有 ``DecisionSink`` 注入路径。
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

# 仅复用既有的 GatePrompt 数据结构（脱敏快照序列化用），不引入任何 L2 / 锁相关路径。
from .gate_prompt import GatePrompt


# ---------------------------------------------------------------------------
# 错误类型（脱敏）
# ---------------------------------------------------------------------------
class PendingDecisionError(Exception):
    """脱敏错误：记录缺失 / 已终态 / 已过期 / letter 非法。

    不携带任何路径 / Key / 参数——仅固定 ``failure_code`` 语义的文案。
    """

    def __init__(self, failure_code: str, *, message: str | None = None) -> None:
        self.failure_code = failure_code
        super().__init__(message or "pending decision operation failed")


# ---------------------------------------------------------------------------
# 持久化行映射
# ---------------------------------------------------------------------------
@dataclass
class PendingDecisionRecord:
    """``b_layer_pending_decisions`` 表行的映射（脱敏）。"""

    pending_id: str  # uuid4 hex（主键）
    gate_id: str  # GatePrompt.gate_id（对外关联）
    category: str  # GatePrompt.category（业务风险类别，供 UI 分组）
    gate_snapshot: str  # JSON(GatePrompt) —— 脱敏快照，无路径/Key/参数
    status: str = "pending"  # "pending" | "resolved" | "cancelled"
    decision: str = ""  # "" | "A" | "B" | "C" | "D"（resolver 回填）
    correlation_id: str = ""  # 接线点 correlation_id（审计关联）
    gate_label: str = ""  # 接线点 gate_label（如 "G1-deploy" / "G4-token"）
    created_at: str = ""  # ISO 8601 UTC
    expires_at: str = ""  # ISO 8601 UTC（status=pending 时有效）
    resolved_at: str | None = None  # ISO 8601 UTC（resolve/cancel 时写）


# ---------------------------------------------------------------------------
# 接线信号
# ---------------------------------------------------------------------------
@dataclass
class PendingDecisionRaised:
    """接线点向『上层编排』返回的信号：动作尚未执行，需等 resolver 回填后 resume。

    本期上层编排（Workspace UI/CLI/API）未建；接线点仅在 ``pending_sink is not None``
    时产生本信号，由未来编排层负责捕获 ``pending_id`` 并 resume。
    """

    pending_id: str
    gate_label: str
    gate_id: str


# ---------------------------------------------------------------------------
# 持久化存储（sqlite3 + threading.Lock）
# ---------------------------------------------------------------------------
_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS b_layer_pending_decisions (
    pending_id    TEXT PRIMARY KEY,
    gate_id       TEXT,
    category      TEXT,
    gate_snapshot TEXT,
    status        TEXT,
    decision      TEXT,
    correlation_id TEXT,
    gate_label    TEXT,
    created_at    TEXT,
    expires_at    TEXT,
    resolved_at   TEXT
)
"""

_VALID_LETTERS = ("A", "B", "C", "D")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _expired_at(expires_at: str | None) -> bool:
    """判断 expires_at 是否早于当前 UTC 时刻（缺失 / 非法 → 视为未过期）。"""
    if not expires_at:
        return False
    try:
        dt = datetime.fromisoformat(expires_at)
    except Exception:  # noqa: BLE001 - 非法时间视为未过期（fail-open 偏保守的读取侧）
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt < datetime.now(timezone.utc)


class PendingDecisionStore:
    """sqlite3 持久化的待决策存储；``get_letter`` 为 fail-closed 单一真源。

    线程安全：``threading.Lock`` 串行化每次操作；每操作独立 sqlite 连接
    （``check_same_thread=False`` 无虞）。默认库位于 ``data/``（已 gitignore）。
    """

    def __init__(self, db_path: str, default_ttl_seconds: int = 3600) -> None:
        """``db_path`` 缺省指向 ``data/b_layer_pending_decisions.sqlite``（可覆盖）。

        ``default_ttl_seconds``：pending 默认存活（覆盖 ``GatePrompt.expires_at``
        缺省 None）。
        """
        self.db_path = db_path
        self.default_ttl_seconds = default_ttl_seconds
        self._lock = threading.Lock()
        parent = os.path.dirname(db_path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        self._init_schema()

    # ── 私有助手 ──────────────────────────────────────────────────────
    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_schema(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.execute(_TABLE_DDL)
                conn.commit()

    @staticmethod
    def _row_to_record(row: tuple[Any, ...]) -> PendingDecisionRecord:
        return PendingDecisionRecord(
            pending_id=row[0],
            gate_id=row[1],
            category=row[2],
            gate_snapshot=row[3],
            status=row[4],
            decision=row[5],
            correlation_id=row[6],
            gate_label=row[7],
            created_at=row[8],
            expires_at=row[9],
            resolved_at=row[10],
        )

    # ── 公共 API ──────────────────────────────────────────────────────
    def create(
        self,
        gate: GatePrompt,
        *,
        correlation_id: str,
        gate_label: str,
        ttl_seconds: int | None = None,
    ) -> str:
        """写入一条 pending 决策，返回 ``pending_id``。

        ``expires_at = gate.expires_at or now + (ttl_seconds or default_ttl)``。
        """
        pending_id = uuid.uuid4().hex
        gate_id = getattr(gate, "gate_id", "") or ""
        category = getattr(gate, "category", "") or ""
        # 脱敏快照：仅 GatePrompt JSON（禁词红线已在 render_gate_prompt enforcement）。
        try:
            gate_snapshot = json.dumps(asdict(gate), ensure_ascii=False)
        except Exception:  # noqa: BLE001 - 兜底脱敏，绝不抛路径/Key
            gate_snapshot = json.dumps(
                {"gate_id": gate_id, "category": category}, ensure_ascii=False
            )
        now = datetime.now(timezone.utc)
        created_at = now.isoformat()
        gate_expires = getattr(gate, "expires_at", None)
        if gate_expires:
            expires_at = gate_expires
        else:
            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
            expires_at = (now + timedelta(seconds=ttl)).isoformat()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO b_layer_pending_decisions "
                    "(pending_id, gate_id, category, gate_snapshot, status, decision, "
                    " correlation_id, gate_label, created_at, expires_at, resolved_at) "
                    "VALUES (?, ?, ?, ?, 'pending', '', ?, ?, ?, ?, NULL)",
                    (
                        pending_id,
                        gate_id,
                        category,
                        gate_snapshot,
                        correlation_id or "",
                        gate_label or "",
                        created_at,
                        expires_at,
                    ),
                )
                conn.commit()
        return pending_id

    def get(self, pending_id: str) -> PendingDecisionRecord | None:
        """按 id 取记录；不存在返 ``None``。"""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT pending_id, gate_id, category, gate_snapshot, status, "
                    "decision, correlation_id, gate_label, created_at, expires_at, "
                    "resolved_at FROM b_layer_pending_decisions WHERE pending_id = ?",
                    (pending_id,),
                ).fetchone()
        if row is None:
            return None
        return self._row_to_record(row)

    def resolve(self, pending_id: str, letter: str) -> PendingDecisionRecord:
        """resolver 回填：``status→resolved``、``decision=letter``、``resolved_at=now``。

        前置：记录须存在且 ``status==pending`` 且未过期；否则抛 ``PendingDecisionError``。
        """
        normalized = (letter or "").strip().upper()
        if normalized not in _VALID_LETTERS:
            raise PendingDecisionError("illegal_decision_letter")
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT status, expires_at FROM b_layer_pending_decisions "
                    "WHERE pending_id = ?",
                    (pending_id,),
                ).fetchone()
                if row is None:
                    raise PendingDecisionError("pending_decision_not_found")
                status, expires_at = row
                if status != "pending":
                    raise PendingDecisionError("pending_decision_already_finalized")
                if _expired_at(expires_at):
                    raise PendingDecisionError("pending_decision_expired")
                resolved_at = _now_iso()
                conn.execute(
                    "UPDATE b_layer_pending_decisions SET status = 'resolved', "
                    "decision = ?, resolved_at = ? WHERE pending_id = ?",
                    (normalized, resolved_at, pending_id),
                )
                conn.commit()
        record = self.get(pending_id)
        if record is None:  # 极不可能，作防御
            raise PendingDecisionError("pending_decision_not_found")
        return record

    def cancel(self, pending_id: str) -> PendingDecisionRecord:
        """fail-closed 显式取消：``status→cancelled``、``decision="C"``、``resolved_at=now``。

        缺失 → 抛 ``PendingDecisionError``（便于发现误调用）；已 ``resolved`` / ``cancelled``
        → 幂等 no-op（返回既有记录）。
        """
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT status FROM b_layer_pending_decisions WHERE pending_id = ?",
                    (pending_id,),
                ).fetchone()
                if row is None:
                    raise PendingDecisionError("pending_decision_not_found")
                status = row[0]
                if status in ("resolved", "cancelled"):
                    # 已终态 → 幂等 no-op。
                    existing = conn.execute(
                        "SELECT pending_id, gate_id, category, gate_snapshot, status, "
                        "decision, correlation_id, gate_label, created_at, expires_at, "
                        "resolved_at FROM b_layer_pending_decisions WHERE pending_id = ?",
                        (pending_id,),
                    ).fetchone()
                    return self._row_to_record(existing)
                resolved_at = _now_iso()
                conn.execute(
                    "UPDATE b_layer_pending_decisions SET status = 'cancelled', "
                    "decision = 'C', resolved_at = ? WHERE pending_id = ?",
                    (resolved_at, pending_id),
                )
                conn.commit()
        record = self.get(pending_id)
        if record is None:
            raise PendingDecisionError("pending_decision_not_found")
        return record

    def get_letter(self, pending_id: str) -> str:
        """引擎读回决策（fail-closed 单一真源）：

        ``status==resolved`` → ``decision``；
        其余（pending 未回填 / 过期 / 缺失 / cancelled）→ ``"C"``。
        """
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT status, decision, expires_at FROM b_layer_pending_decisions "
                    "WHERE pending_id = ?",
                    (pending_id,),
                ).fetchone()
        if row is None:
            return "C"
        status, decision, expires_at = row
        if status == "resolved":
            return decision or "C"
        # pending（含过期） / cancelled / 任何其它 → fail-closed C。
        return "C"

    def is_expired(self, pending_id: str) -> bool:
        """``expires_at < now`` 且 ``status==pending`` → True；其余（含缺失/已终态）→ False。"""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT status, expires_at FROM b_layer_pending_decisions "
                    "WHERE pending_id = ?",
                    (pending_id,),
                ).fetchone()
        if row is None:
            return False
        status, expires_at = row
        if status != "pending":
            return False
        return _expired_at(expires_at)

    def list_pending(
        self, correlation_id: str | None = None
    ) -> list[PendingDecisionRecord]:
        """供未来 UI 轮询未决决策（可选，本期测试桩可用）。"""
        with self._lock:
            with self._connect() as conn:
                if correlation_id:
                    rows = conn.execute(
                        "SELECT pending_id, gate_id, category, gate_snapshot, status, "
                        "decision, correlation_id, gate_label, created_at, expires_at, "
                        "resolved_at FROM b_layer_pending_decisions "
                        "WHERE status = 'pending' AND correlation_id = ?",
                        (correlation_id,),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT pending_id, gate_id, category, gate_snapshot, status, "
                        "decision, correlation_id, gate_label, created_at, expires_at, "
                        "resolved_at FROM b_layer_pending_decisions "
                        "WHERE status = 'pending'",
                    ).fetchall()
        return [self._row_to_record(row) for row in rows]


# ---------------------------------------------------------------------------
# 非阻塞 sink
# ---------------------------------------------------------------------------
class PendingDecisionSink:
    """真实 DecisionSink 后端机制：把闸请求持久化，返回 ``pending_id``（**非阻塞**）。

    注意：本类 **不** 实现阻塞式 ``DecisionSink`` Protocol（``ask`` 返回 ``str`` 而非
    letter），因此必须经独立参数 ``pending_sink`` 接线，或由接线点 ``isinstance`` 识别。
    """

    def __init__(self, store: PendingDecisionStore, ttl_seconds: int | None = None) -> None:
        self.store = store
        self.ttl_seconds = ttl_seconds

    def ask(
        self,
        gate: GatePrompt,
        *,
        correlation_id: str | None = None,
        gate_label: str | None = None,
    ) -> str:
        """写入存储并返回 ``pending_id``（**非阻塞**）。

        接线点据此返回 ``PendingDecisionRaised(pending_id)`` 信号，不在此等待。
        """
        return self.store.create(
            gate,
            correlation_id=correlation_id or "",
            gate_label=gate_label or "",
            ttl_seconds=self.ttl_seconds,
        )


# ---------------------------------------------------------------------------
# resolver 函数（供未来 Workspace UI/CLI/API 调用）
# ---------------------------------------------------------------------------
_default_store_instance: PendingDecisionStore | None = None
_default_store_lock = threading.Lock()


def _default_db_path() -> str:
    """仓库根 ``data/b_layer_pending_decisions.sqlite``（已被 .gitignore 忽略）。"""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(repo_root, "data", "b_layer_pending_decisions.sqlite")


def _default_store() -> PendingDecisionStore:
    """模块级默认 store 单例（lazy init，避免 import 时即触盘）。"""
    global _default_store_instance
    with _default_store_lock:
        if _default_store_instance is None:
            _default_store_instance = PendingDecisionStore(_default_db_path())
    return _default_store_instance


def resolve_decision(
    pending_id: str,
    letter: str,
    store: PendingDecisionStore | None = None,
) -> PendingDecisionRecord:
    """resolver 函数（供未来 Workspace UI/CLI/API 调用）。

    未传 ``store`` 时用模块级默认 store 单例（lazy init）。委托 ``store.resolve()``。
    """
    target = store or _default_store()
    return target.resolve(pending_id, letter)


__all__ = [
    "PendingDecisionError",
    "PendingDecisionRecord",
    "PendingDecisionRaised",
    "PendingDecisionStore",
    "PendingDecisionSink",
    "resolve_decision",
]
