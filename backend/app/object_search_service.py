"""Read-only company-wide object search.

Aggregates nine existing object stores into a single grouped result. No schema,
writes, events, or external calls. Company isolation is enforced by filtering
every table by the current tenant and the requested company; cross-tenant
leakage is impossible because tenant_id is stamped on every row except
``tasks`` (which is isolated via company_id, a company table primary key).
"""
from __future__ import annotations

import json
from typing import Any

from .database import Database
from .tenant_context import TenantContext


MAX_QUERY = 64
GROUP_LIMIT = 8


def _escape_like(value: str) -> str:
    """Escape LIKE wildcards so user input never becomes a pattern."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _json_data(raw: Any) -> dict[str, Any]:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (TypeError, ValueError):
        return {}


class ObjectSearchService:
    """Read-only aggregator for the company-wide object search surface."""

    def __init__(self, database: Database) -> None:
        self.database = database

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def _require_company(self, company_id: str) -> None:
        with self.database.connect() as conn:
            row = conn.execute(
                "select 1 from companies where tenant_id = ? and company_id = ?",
                (self.tenant_id, company_id),
            ).fetchone()
        if row is None:
            raise KeyError("company does not belong to current tenant")

    def search(self, company_id: str, query: str) -> dict[str, Any]:
        self._require_company(company_id)
        q = (query or "").strip()
        if not q:
            return {"query": "", "groups": []}
        if len(q) > MAX_QUERY:
            raise ValueError("query too long")
        needle = "%" + _escape_like(q) + "%"
        with self.database.connect() as conn:
            groups = [
                self._businesses(conn, company_id, needle),
                self._workspaces(conn, company_id, needle),
                self._employees(conn, company_id, q, needle),
                self._business_objects(conn, company_id, q, needle),
                self._knowledge(conn, company_id, needle),
                self._meetings(conn, company_id, needle),
                self._decisions(conn, company_id, q, needle),
                self._tasks(conn, company_id, needle),
                self._results(conn, company_id, needle),
            ]
        return {"query": q, "groups": [g for g in groups if g["items"]]}

    def _businesses(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select b.business_id as id, b.name as title, d.name as department "
            "from canonical_businesses b left join department_instances d "
            "on d.tenant_id = b.tenant_id and d.company_id = b.company_id and d.id = b.department_id "
            "where b.tenant_id = ? and b.company_id = ? and b.name like ? escape '\\' "
            "order by b.updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {"id": r["id"], "title": r["title"], "context": r["department"] or "未分配部门"}
            for r in rows
        ]
        return {"type": "business", "label": "业务", "items": items}

    def _workspaces(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select w.workspace_id as id, w.name as title, b.name as business "
            "from workspaces w left join canonical_businesses b on b.business_id = w.business_id "
            "where w.tenant_id = ? and w.company_id = ? and w.name like ? escape '\\' "
            "order by w.updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {"id": r["id"], "title": r["title"], "context": r["business"] or "未归属业务"}
            for r in rows
        ]
        return {"type": "workspace", "label": "工作台", "items": items}

    def _employees(self, conn, company_id: str, q: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select entity_id as id, data_json from runtime_entities "
            "where tenant_id = ? and company_id = ? and entity_type = 'AI_EMPLOYEE' "
            "and data_json like ? escape '\\' "
            "order by updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT * 4),
        ).fetchall()
        items = []
        for r in rows:
            data = _json_data(r["data_json"])
            name = data.get("name") or ""
            role = data.get("role") or data.get("responsibility") or "未设置岗位"
            if isinstance(name, str) and (q in name or q in role):
                items.append({"id": r["id"], "title": name, "context": role})
            if len(items) >= GROUP_LIMIT:
                break
        return {"type": "employee", "label": "员工", "items": items}

    def _business_objects(self, conn, company_id: str, q: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select entity_id as id, data_json from runtime_entities "
            "where tenant_id = ? and company_id = ? and entity_type = 'PACKAGE_DOMAIN_OBJECT' "
            "and data_json like ? escape '\\' order by updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT * 4),
        ).fetchall()
        items = []
        for r in rows:
            data = _json_data(r["data_json"])
            title = (
                data.get("title")
                or data.get("name")
                or data.get("kind")
                or data.get("objectType")
                or "业务对象"
            )
            context = data.get("objectType") or "业务对象"
            if isinstance(title, str) and q in title:
                items.append({"id": r["id"], "title": title[:80], "context": context})
            if len(items) >= GROUP_LIMIT:
                break
        return {"type": "business_object", "label": "业务对象", "items": items}

    def _knowledge(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select id, title, source_label from knowledge_entries "
            "where tenant_id = ? and company_id = ? and lifecycle_status = 'ACTIVE' "
            "and title like ? escape '\\' order by updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {"id": r["id"], "title": r["title"], "context": r["source_label"] or "资料库"}
            for r in rows
        ]
        return {"type": "knowledge", "label": "资料", "items": items}

    def _meetings(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select meeting_id as id, title, status from strategy_meetings "
            "where tenant_id = ? and company_id = ? and title like ? escape '\\' "
            "order by updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {"id": r["id"], "title": r["title"], "context": r["status"] or "会议"}
            for r in rows
        ]
        return {"type": "meeting", "label": "会议", "items": items}

    def _decisions(self, conn, company_id: str, q: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select entity_id as id, data_json, lifecycle_status from runtime_entities "
            "where tenant_id = ? and company_id = ? and entity_type = 'DECISION_PACKET' "
            "and data_json like ? escape '\\' order by updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT * 4),
        ).fetchall()
        items = []
        for r in rows:
            data = _json_data(r["data_json"])
            problem = data.get("problem") or data.get("question") or ""
            if isinstance(problem, str) and q in problem:
                items.append({
                    "id": r["id"],
                    "title": problem[:80],
                    "context": r["lifecycle_status"] or "决策",
                })
            if len(items) >= GROUP_LIMIT:
                break
        return {"type": "decision", "label": "决策", "items": items}

    def _tasks(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select task_id as id, content, status from tasks "
            "where company_id = ? and content like ? escape '\\' "
            "order by updated_at desc limit ?",
            (company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {"id": r["id"], "title": r["content"][:80], "context": r["status"] or "任务"}
            for r in rows
        ]
        return {"type": "task", "label": "任务", "items": items}

    def _results(self, conn, company_id: str, needle: str) -> dict[str, Any]:
        rows = conn.execute(
            "select a.artifact_id as id, a.title, a.artifact_type, t.workspace_id "
            "from artifacts a join tasks t on t.task_id = a.task_id "
            "where a.tenant_id = ? and t.company_id = ? and a.title like ? escape '\\' "
            "order by a.updated_at desc limit ?",
            (self.tenant_id, company_id, needle, GROUP_LIMIT),
        ).fetchall()
        items = [
            {
                "id": r["id"],
                "title": r["title"],
                "context": r["artifact_type"] or "结果",
                "workspace_id": r["workspace_id"] or "",
            }
            for r in rows
        ]
        return {"type": "result", "label": "结果", "items": items}
