from __future__ import annotations

import json
import uuid
from typing import Any

from .ceo_context import CeoContext
from .database import Database
from .tenant_context import TenantContext


_COMPANY_STATUSES = frozenset({"draft", "active", "disabled", "archived"})
_PROJECT_STATUSES = frozenset({"planned", "active", "blocked", "completed", "archived"})


class CompanyProjectRuntime:
    """Tenant-scoped Company and Project runtime foundation for Workspace."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def list_companies(self) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self._ensure_default_company()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from companies where tenant_id = ? order by is_default desc, created_at asc",
                (tenant_id,),
            ).fetchall()
        return {"tenant_id": tenant_id, "companies": [self._company_from_row(row) for row in rows]}

    def create_company(
        self,
        *,
        name: str,
        description: str = "",
        status: str = "active",
        created_from_template_id: str | None = None,
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self._ensure_default_company()
        if not name.strip():
            raise ValueError("company name is required")
        self._validate_company_status(status)
        company_id = f"company-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into companies (
                  company_id, tenant_id, ceo_id, name, description, company_type,
                  status, is_default, default_department_ids_json, created_from_template_id, updated_at
                ) values (?, ?, ?, ?, ?, 'software_rnd_company', ?, 0, '[]', ?, current_timestamp)
                """,
                (
                    company_id,
                    tenant_id,
                    CeoContext.current_ceo_id() or "",
                    name.strip(),
                    description.strip(),
                    status,
                    created_from_template_id or None,
                ),
            )
        return self.get_company(company_id)

    def get_company(self, company_id: str) -> dict[str, Any]:
        row = self._find_company(company_id)
        if row is None:
            raise KeyError("company not found")
        return self._company_from_row(row)

    def update_company(self, company_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        company = self.get_company(company_id)
        updates: dict[str, Any] = {}
        if "name" in changes and changes["name"] is not None:
            name = str(changes["name"]).strip()
            if not name:
                raise ValueError("company name is required")
            updates["name"] = name
        if "description" in changes and changes["description"] is not None:
            updates["description"] = str(changes["description"]).strip()
        if "status" in changes and changes["status"] is not None:
            self._validate_company_status(str(changes["status"]))
            updates["status"] = str(changes["status"])
        if not updates:
            return company
        assignments = ", ".join(f"{field} = ?" for field in updates)
        with self.database.connect() as connection:
            connection.execute(
                f"update companies set {assignments}, updated_at = current_timestamp "
                "where tenant_id = ? and company_id = ?",
                (*updates.values(), TenantContext.current_tenant_id(), company_id),
            )
        return self.get_company(company_id)

    def list_projects(self, company_id: str | None = None) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        if company_id:
            self.get_company(company_id)
        query = "select * from projects where tenant_id = ?"
        params: list[str] = [tenant_id]
        if company_id:
            query += " and company_id = ?"
            params.append(company_id)
        query += " order by created_at desc"
        with self.database.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return {"tenant_id": tenant_id, "projects": [self._project_from_row(row) for row in rows]}

    def create_project(
        self,
        *,
        company_id: str,
        name: str,
        goal: str,
        description: str = "",
        department_id: str,
        owner_employee_id: str | None = None,
        status: str = "planned",
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self.get_company(company_id)
        if not name.strip():
            raise ValueError("project name is required")
        if not goal.strip():
            raise ValueError("project goal is required")
        self._validate_project_status(status)
        self._validate_department(company_id, department_id)
        self._validate_owner(company_id, department_id, owner_employee_id)
        project_id = f"project-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into projects (
                  project_id, tenant_id, company_id, department_id, name, goal, description,
                  project_type, status, owner_employee_id, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, 'software_development', ?, ?, current_timestamp)
                """,
                (
                    project_id,
                    tenant_id,
                    company_id,
                    department_id,
                    name.strip(),
                    goal.strip(),
                    description.strip(),
                    status,
                    owner_employee_id,
                ),
            )
        return self.get_project(project_id)

    def get_project(self, project_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from projects where tenant_id = ? and project_id = ?",
                (tenant_id, project_id),
            ).fetchone()
        if row is None:
            raise KeyError("project not found")
        return self._project_from_row(row)

    def update_project(self, project_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        project = self.get_project(project_id)
        updates: dict[str, Any] = {}
        for field in ("name", "goal", "description"):
            if field in changes and changes[field] is not None:
                value = str(changes[field]).strip()
                if field in {"name", "goal"} and not value:
                    raise ValueError(f"project {field} is required")
                updates[field] = value
        if "status" in changes and changes["status"] is not None:
            self._validate_project_status(str(changes["status"]))
            updates["status"] = str(changes["status"])

        department_id = changes.get("department_id", project["department_id"])
        owner_employee_id = changes.get("owner_employee_id", project["owner_employee_id"])
        if "department_id" in changes:
            self._validate_department(project["company_id"], department_id)
            updates["department_id"] = department_id
        if "owner_employee_id" in changes:
            self._validate_owner(project["company_id"], department_id, owner_employee_id)
            updates["owner_employee_id"] = owner_employee_id

        if not updates:
            return project
        assignments = ", ".join(f"{field} = ?" for field in updates)
        with self.database.connect() as connection:
            connection.execute(
                f"update projects set {assignments}, updated_at = current_timestamp "
                "where tenant_id = ? and project_id = ?",
                (*updates.values(), TenantContext.current_tenant_id(), project_id),
            )
        return self.get_project(project_id)

    def resolve_task_context(
        self,
        *,
        company_id: str | None,
        project_id: str | None,
        employee_id: str | None,
    ) -> dict[str, str | None]:
        """Validate optional Task lineage without changing task execution behavior."""
        resolved_company_id = company_id or None
        resolved_project_id = project_id or None
        if resolved_project_id:
            project = self.get_project(resolved_project_id)
            if resolved_company_id and resolved_company_id != project["company_id"]:
                raise ValueError("task company_id must match the project company")
            resolved_company_id = project["company_id"]
        if resolved_company_id:
            self.get_company(resolved_company_id)
        if employee_id and resolved_company_id:
            self._validate_owner(resolved_company_id or "", None, employee_id)
        return {"company_id": resolved_company_id, "project_id": resolved_project_id}

    def _ensure_default_company(self) -> None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            exists = connection.execute(
                "select company_id from companies where tenant_id = ? limit 1", (tenant_id,)
            ).fetchone()
            if exists is not None:
                return
            connection.execute(
                """
                insert into companies (
                  company_id, tenant_id, ceo_id, name, description, company_type,
                  status, is_default, default_department_ids_json, updated_at
                ) values (?, ?, ?, 'Curis AI Company', '', 'software_rnd_company', 'active', 1, '[]', current_timestamp)
                """,
                (f"company-{uuid.uuid4()}", tenant_id, CeoContext.current_ceo_id() or ""),
            )

    def _find_company(self, company_id: str):
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            return connection.execute(
                "select * from companies where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()

    def _validate_department(self, company_id: str, department_id: str | None) -> None:
        if not department_id:
            raise ValueError("project business department is required")
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from department_instances where tenant_id = ? and id = ? and enabled = 1",
                (tenant_id, department_id),
            ).fetchone()
        if row is None or row["company_id"] != company_id:
            raise ValueError("department must be an enabled department of the project company")

    def _validate_owner(
        self,
        company_id: str,
        department_id: str | None,
        owner_employee_id: str | None,
    ) -> None:
        if owner_employee_id is None:
            return
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                """
                select company_id, department_id from employee_instances
                where tenant_id = ? and id = ? and enabled = 1
                """,
                (tenant_id, owner_employee_id),
            ).fetchone()
        if row is None or row["company_id"] != company_id:
            raise ValueError("project owner must be an enabled employee of the project company")
        if department_id is not None and row["department_id"] != department_id:
            raise ValueError("project owner must belong to the project department")

    @staticmethod
    def _validate_company_status(status: str) -> None:
        if status not in _COMPANY_STATUSES:
            raise ValueError("company status must be draft, active, disabled, or archived")

    @staticmethod
    def _validate_project_status(status: str) -> None:
        if status not in _PROJECT_STATUSES:
            raise ValueError("project status must be planned, active, blocked, completed, or archived")

    @staticmethod
    def _company_from_row(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["is_default"] = bool(item.pop("is_default"))
        item["default_department_ids"] = json.loads(item.pop("default_department_ids_json") or "[]")
        return item

    @staticmethod
    def _project_from_row(row: Any) -> dict[str, Any]:
        return dict(row)
