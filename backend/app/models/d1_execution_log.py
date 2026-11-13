"""D1 execution log store (scope B).

Structured, desensitized record of every D1 controlled-gate execution attempt.
Nothing path / stack / key / request-parameter related is ever written here;
only the controlled outcome (status + error category), tenant id, task type,
duration, and token count.

Standard library only; raw SQL consistent with the rest of ``app.database``.
No new third-party dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..database import Database


@dataclass(frozen=True)
class D1ExecutionLogRow:
    """Immutable view of one ``d1_execution_log`` row."""

    id: int
    tenant_id: str
    task_type: str
    status: str
    error_category: str | None
    duration_ms: int
    token_count: int
    created_at: str


class D1ExecutionLogRepository:
    """Append-only accessor for the ``d1_execution_log`` table.

    All writes are INSERTs; there is no update / delete path, keeping the log
    tamper-evident by construction. Reads are limited to the desensitized
    columns defined on the table.
    """

    def __init__(self, database: Database) -> None:
        self._db = database

    def insert(
        self,
        *,
        tenant_id: str,
        task_type: str,
        status: str,
        error_category: str | None,
        duration_ms: int,
        token_count: int,
    ) -> int:
        """Insert one execution outcome row; returns the new row id."""
        with self._db.connect() as connection:
            cursor = connection.execute(
                """
                insert into d1_execution_log
                  (tenant_id, task_type, status, error_category, duration_ms, token_count)
                values (?, ?, ?, ?, ?, ?)
                """,
                (
                    tenant_id,
                    task_type,
                    status,
                    error_category,
                    duration_ms,
                    token_count,
                ),
            )
            return cursor.lastrowid

    def recent(self, limit: int = 50) -> list[D1ExecutionLogRow]:
        """Return the most recent rows (newest first)."""
        with self._db.connect() as connection:
            rows = connection.execute(
                "select id, tenant_id, task_type, status, error_category, "
                "duration_ms, token_count, created_at "
                "from d1_execution_log order by id desc limit ?",
                (limit,),
            ).fetchall()
        return [self._row_from(row) for row in rows]

    def count_by_status(self) -> dict[str, int]:
        """Aggregate row counts keyed by outcome ``status``."""
        with self._db.connect() as connection:
            rows = connection.execute(
                "select status, count(*) as c from d1_execution_log group by status"
            ).fetchall()
        return {row["status"]: row["c"] for row in rows}

    @staticmethod
    def _row_from(row: Any) -> D1ExecutionLogRow:
        return D1ExecutionLogRow(
            id=row["id"],
            tenant_id=row["tenant_id"],
            task_type=row["task_type"],
            status=row["status"],
            error_category=row["error_category"],
            duration_ms=row["duration_ms"],
            token_count=row["token_count"],
            created_at=row["created_at"],
        )
