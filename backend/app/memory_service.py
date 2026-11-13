from __future__ import annotations

import json
import re
import uuid
from typing import Any

from .database import Database
from .tenant_context import TenantContext


MEMORY_LEVELS = {"user": "user", "project": "L2", "employee": "L3"}
TERMINAL_TASK_STATUSES = {"COMPLETED", "FAILED"}


def relevance_score(query: str, *values: str) -> int:
    query_terms = _terms(query)
    if not query_terms:
        return 0
    haystack = " ".join(str(value or "") for value in values).lower()
    score = len(query_terms & _terms(haystack)) * 5
    normalized = query.strip().lower()
    if normalized and normalized in haystack:
        score += 25
    return score


def _terms(value: str) -> set[str]:
    lowered = value.lower()
    terms = set(re.findall(r"[a-z0-9_]{2,}", lowered))
    for chunk in re.findall(r"[\u4e00-\u9fff]+", lowered):
        if len(chunk) == 1:
            terms.add(chunk)
        else:
            terms.update(chunk[index : index + 2] for index in range(len(chunk) - 1))
    return terms


class MemoryService:
    """Confirmed, tenant-scoped user/project/employee experience."""

    MAX_CONTENT_BYTES = 20 * 1024

    def __init__(self, database: Database) -> None:
        self.database = database

    def create_entry(
        self,
        *,
        memory_type: str,
        title: str,
        content: str,
        tags: list[str] | None = None,
        project_id: str | None = None,
        employee_id: str | None = None,
        source_task_id: str | None = None,
        confidence: float = 1.0,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        user_id = self._user_id()
        clean_title = self._title(title)
        clean_content = self._content(content)
        clean_tags = self._tags(tags or [])
        confidence = self._confidence(confidence)
        project_id, employee_id = self._validate_scope(
            memory_type, project_id, employee_id
        )
        if source_task_id:
            self._validate_source_task(
                source_task_id,
                memory_type=memory_type,
                project_id=project_id,
                employee_id=employee_id,
            )
        memory_id = f"memory-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into memory_entries (
                  id, tenant_id, memory_type, memory_level, user_id,
                  project_id, employee_id, title, content, summary, tags_json,
                  source_type, source_task_id, confidence, created_by
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    memory_id,
                    tenant_id,
                    memory_type,
                    MEMORY_LEVELS[memory_type],
                    user_id if memory_type == "user" else "",
                    project_id,
                    employee_id,
                    clean_title,
                    clean_content,
                    self._summary(clean_content),
                    json.dumps(clean_tags, ensure_ascii=False),
                    "task" if source_task_id else "manual",
                    source_task_id,
                    confidence,
                    user_id,
                ),
            )
        return self.get_entry(memory_id)

    def list_entries(
        self,
        *,
        query: str = "",
        scope: str = "all",
        project_id: str = "",
        employee_id: str = "",
        include_archived: bool = False,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        user_id = self._user_id()
        needle = query.strip()
        if len(needle) > 200:
            raise ValueError("memory query is too long")
        if scope not in {"all", *MEMORY_LEVELS}:
            raise ValueError("memory scope is invalid")
        clauses = ["me.tenant_id = ?"]
        params: list[Any] = [tenant_id]
        if not include_archived:
            clauses.append("me.status = 'active'")
        if scope == "user":
            clauses.extend(["me.memory_type = 'user'", "me.user_id = ?"])
            params.append(user_id)
        elif scope in {"project", "employee"}:
            clauses.append("me.memory_type = ?")
            params.append(scope)
        else:
            clauses.append("(me.memory_type != 'user' or me.user_id = ?)")
            params.append(user_id)
        if project_id:
            clauses.append("me.project_id = ?")
            params.append(project_id)
        if employee_id:
            clauses.append("me.employee_id = ?")
            params.append(employee_id)
        if needle:
            like = f"%{needle}%"
            clauses.append(
                "(me.title like ? or me.summary like ? or me.content like ? or me.tags_json like ?)"
            )
            params.extend([like, like, like, like])
        with self.database.connect() as connection:
            rows = connection.execute(
                self._select_sql()
                + " where "
                + " and ".join(clauses)
                + " order by me.updated_at desc, me.id limit 100",
                params,
            ).fetchall()
        return {
            "tenant_id": tenant_id,
            "entries": [self._entry(row) for row in rows],
        }

    def get_entry(self, memory_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        user_id = self._user_id()
        with self.database.connect() as connection:
            row = connection.execute(
                self._select_sql()
                + " where me.tenant_id = ? and me.id = ? "
                + "and (me.memory_type != 'user' or me.user_id = ?)",
                (tenant_id, memory_id, user_id),
            ).fetchone()
        if row is None:
            raise KeyError("memory entry not found")
        return self._entry(row)

    def update_entry(
        self,
        memory_id: str,
        *,
        title: str | None = None,
        content: str | None = None,
        tags: list[str] | None = None,
        confidence: float | None = None,
        status: str | None = None,
    ) -> dict[str, Any]:
        current = self.get_entry(memory_id)
        if status is not None and status not in {"active", "archived"}:
            raise ValueError("memory status is invalid")
        clean_title = self._title(title) if title is not None else current["title"]
        clean_content = (
            self._content(content) if content is not None else current["content"]
        )
        clean_tags = self._tags(tags) if tags is not None else current["tags"]
        clean_confidence = (
            self._confidence(confidence)
            if confidence is not None
            else current["confidence"]
        )
        with self.database.connect() as connection:
            connection.execute(
                """
                update memory_entries
                set title=?, content=?, summary=?, tags_json=?, confidence=?,
                    status=?, updated_at=current_timestamp
                where tenant_id=? and id=?
                """,
                (
                    clean_title,
                    clean_content,
                    self._summary(clean_content),
                    json.dumps(clean_tags, ensure_ascii=False),
                    clean_confidence,
                    status or current["status"],
                    TenantContext.current_tenant_id(),
                    memory_id,
                ),
            )
        return self.get_entry(memory_id)

    def retrieve(
        self,
        *,
        query: str,
        project_id: str | None,
        employee_id: str | None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        user_id = self._user_id()
        limit = max(1, min(int(limit), 10))
        clauses = [
            "me.tenant_id = ?",
            "me.status = 'active'",
            "((me.memory_type = 'user' and me.user_id = ?)",
        ]
        params: list[Any] = [tenant_id, user_id]
        if project_id:
            clauses[-1] += " or (me.memory_type = 'project' and me.project_id = ?)"
            params.append(project_id)
        if employee_id:
            clauses[-1] += " or (me.memory_type = 'employee' and me.employee_id = ?)"
            params.append(employee_id)
        clauses[-1] += ")"
        with self.database.connect() as connection:
            rows = connection.execute(
                self._select_sql()
                + " where "
                + " and ".join(clauses)
                + " order by me.updated_at desc limit 100",
                params,
            ).fetchall()
        ranked = []
        priority = {"project": 300, "employee": 200, "user": 100}
        for row in rows:
            entry = self._entry(row)
            lexical = relevance_score(
                query,
                entry["title"],
                entry["summary"],
                entry["content"],
                " ".join(entry["tags"]),
            )
            if lexical <= 0:
                continue
            entry["relevance_score"] = priority[entry["memory_type"]] + lexical
            ranked.append(entry)
        ranked.sort(
            key=lambda item: (item["relevance_score"], item["updated_at"]),
            reverse=True,
        )
        return ranked[:limit]

    def mark_used(self, memory_ids: list[str]) -> None:
        if not memory_ids:
            return
        tenant_id = TenantContext.current_tenant_id()
        placeholders = ",".join("?" for _ in memory_ids)
        with self.database.connect() as connection:
            connection.execute(
                f"update memory_entries set use_count=use_count+1, "
                f"last_used_at=current_timestamp where tenant_id=? and id in ({placeholders})",
                [tenant_id, *memory_ids],
            )

    def _validate_scope(
        self,
        memory_type: str,
        project_id: str | None,
        employee_id: str | None,
    ) -> tuple[str | None, str | None]:
        if memory_type not in MEMORY_LEVELS:
            raise ValueError("memory type is invalid")
        tenant_id = TenantContext.current_tenant_id()
        if memory_type == "user":
            if project_id or employee_id:
                raise ValueError("user memory cannot have project or employee scope")
            return None, None
        with self.database.connect() as connection:
            if memory_type == "project":
                if not project_id or employee_id:
                    raise ValueError("project memory requires one project")
                if not connection.execute(
                    "select 1 from projects where tenant_id=? and project_id=?",
                    (tenant_id, project_id),
                ).fetchone():
                    raise ValueError("project is not available")
                return project_id, None
            if not employee_id or project_id:
                raise ValueError("employee memory requires one employee")
            if not connection.execute(
                "select 1 from employee_instances "
                "where tenant_id=? and id=? and deleted_at is null",
                (tenant_id, employee_id),
            ).fetchone():
                raise ValueError("employee is not available")
        return None, employee_id

    def _validate_source_task(
        self,
        task_id: str,
        *,
        memory_type: str,
        project_id: str | None,
        employee_id: str | None,
    ) -> None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            task = connection.execute(
                "select task_id, project_id, employee_id, status from tasks "
                "where tenant_id=? and task_id=?",
                (tenant_id, task_id),
            ).fetchone()
        if task is None:
            raise ValueError("source task is not available")
        if task["status"] not in TERMINAL_TASK_STATUSES:
            raise ValueError("source task must be completed or failed")
        if memory_type == "project" and task["project_id"] != project_id:
            raise ValueError("source task does not belong to the selected project")
        if memory_type == "employee" and task["employee_id"] != employee_id:
            raise ValueError("source task does not belong to the selected employee")

    @staticmethod
    def _title(value: str | None) -> str:
        clean = str(value or "").strip()
        if not clean or len(clean) > 160:
            raise ValueError("memory title is required and must be at most 160 characters")
        return clean

    def _content(self, value: str | None) -> str:
        clean = str(value or "").strip()
        if not clean:
            raise ValueError("memory content is required")
        if len(clean.encode("utf-8")) > self.MAX_CONTENT_BYTES:
            raise ValueError("memory content is too large")
        return clean

    @staticmethod
    def _tags(values: list[str]) -> list[str]:
        tags: list[str] = []
        for raw in values:
            tag = str(raw).strip()
            if tag and tag not in tags:
                if len(tag) > 50:
                    raise ValueError("memory tag is too long")
                tags.append(tag)
        if len(tags) > 10:
            raise ValueError("memory supports at most 10 tags")
        return tags

    @staticmethod
    def _confidence(value: float | None) -> float:
        confidence = float(value if value is not None else 1.0)
        if confidence < 0 or confidence > 1:
            raise ValueError("memory confidence must be between 0 and 1")
        return confidence

    @staticmethod
    def _summary(content: str) -> str:
        return re.sub(r"\s+", " ", content).strip()[:300]

    @staticmethod
    def _user_id() -> str:
        identity = TenantContext.current_identity()
        user_id = identity.get("ceo_id") or identity.get("subject_id") or ""
        if not user_id:
            raise ValueError("trusted user identity is required")
        return user_id

    @staticmethod
    def _select_sql() -> str:
        return (
            "select me.*, p.name as project_name, e.name as employee_name, "
            "t.content as source_task_title, t.status as source_task_status "
            "from memory_entries me "
            "left join projects p on p.tenant_id=me.tenant_id and p.project_id=me.project_id "
            "left join employee_instances e "
            "on e.tenant_id=me.tenant_id and e.id=me.employee_id "
            "left join tasks t on t.tenant_id=me.tenant_id and t.task_id=me.source_task_id"
        )

    @staticmethod
    def _entry(row: Any) -> dict[str, Any]:
        entry = dict(row)
        entry["tags"] = json.loads(entry.pop("tags_json") or "[]")
        entry["confidence"] = float(entry["confidence"])
        entry["use_count"] = int(entry["use_count"])
        entry["scope_name"] = (
            entry.get("project_name")
            or entry.get("employee_name")
            or "用户 Memory"
        )
        return entry
