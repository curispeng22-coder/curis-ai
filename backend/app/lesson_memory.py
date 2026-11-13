"""经验沉淀（P0-6 后半：lessons-learned 持久记忆）。

``LessonMemory`` 把**成功路径 / 失败原因 / 有效降级链**持久化到 ``capability_lessons``
表（T01 新增），供后续任务检索复用（架构 §3 / §8③）。与 ``orchestrator._learn_from_*``
（仅内存）不同，这里是**持久化**版本，二者不冲突、可逐步合并。

设计要点：
- ``record()`` 按 ``signature + outcome + cap_path`` 去重累加 ``reused_count``，避免
  重复经验行膨胀；``query(signature)`` 按 ``reused_count`` DESC 返回，可直接取最优路径。
- 零新依赖（标准库 json + 复用 ``database`` / ``tenant_context``）。
- 写入带 ``tenant_id`` 过滤（共享约定 §7.2）。
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .database import Database
from .tenant_context import TenantContext


@dataclass
class Lesson:
    """一条经验记录。"""

    signature: str
    cap_path: list[str] = field(default_factory=list)
    outcome: str = "unknown"
    reason: str = ""
    reused_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "signature": self.signature,
            "cap_path": list(self.cap_path),
            "outcome": self.outcome,
            "reason": self.reason,
            "reused_count": self.reused_count,
        }


class LessonMemory:
    """经验沉淀存储（capability_lessons 表）。"""

    def __init__(self, database: Database, event_log: Any | None = None) -> None:
        self.database = database
        self.event_log = event_log

    def record(
        self,
        signature: str,
        cap_path: list[str] | None = None,
        outcome: str = "unknown",
        reason: str = "",
        reused_count: int = 0,
    ) -> dict[str, Any]:
        """记录一条经验；相同 (signature, outcome, cap_path) 则累加 reused_count。

        Returns:
            写入/更新后的经验行（dict）。
        """
        cap_path = cap_path or []
        cap_path_json = json.dumps(cap_path, ensure_ascii=False)
        # 去重：同指纹 + 同结果 + 同路径 → 累加复用次数（而非新增行）。
        existing = self.database.list_capability_lessons(
            signature=signature, outcome=outcome
        )
        for les in existing:
            if json.dumps(les.get("cap_path") or [], ensure_ascii=False) == cap_path_json:
                new_count = int(les.get("reused_count") or 0) + 1
                self.database.update_capability_lesson_reuse(les["lesson_id"], new_count)
                updated = dict(les)
                updated["reused_count"] = new_count
                return updated
        tenant = TenantContext.current_tenant_id()
        # 首次记录即算一次复用（reused_count=1）；后续同指纹累加见上分支。
        initial = max(1, int(reused_count or 0))
        return self.database.save_capability_lesson(
            tenant_id=tenant,
            signature=signature,
            cap_path=cap_path,
            outcome=outcome,
            reason=reason,
            reused_count=initial,
        )

    def query(
        self, signature: str, outcome: str | None = None
    ) -> list[dict[str, Any]]:
        """按 signature 查询经验（默认按 reused_count DESC）；可再按 outcome 过滤。"""
        return self.database.list_capability_lessons(
            signature=signature, outcome=outcome
        )

    def list_all(self, outcome: str | None = None) -> list[dict[str, Any]]:
        """列出全部经验（可按 outcome 过滤）。"""
        return self.database.list_capability_lessons(outcome=outcome)

    def best_path(self, signature: str) -> list[str] | None:
        """返回该 signature 下复用最多且成功的有效降级链（供后续任务复用）。"""
        lessons = self.query(signature, outcome="success")
        if not lessons:
            return None
        return list(lessons[0].get("cap_path") or [])

    def bump_reuse(self, signature: str, outcome: str, cap_path: list[str]) -> None:
        """显式标记某路径被复用（累加 reused_count）。"""
        self.record(
            signature=signature, cap_path=cap_path, outcome=outcome, reason="复用成功路径"
        )
