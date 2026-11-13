from __future__ import annotations

import uuid
from typing import Any

from .database import Database
from .tenant_context import TenantContext


class EmployeeAffiliationService:
    """Tenant-scoped secondary department/project memberships for employees."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def set_affiliations(
        self,
        *,
        employee_id: str,
        affiliations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        employee = self._employee(tenant_id, employee_id)
        normalized: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for item in affiliations:
            department_id = str(item.get("department_id") or "").strip()
            project_id = str(item.get("project_id") or "").strip()
            if not department_id and not project_id:
                raise ValueError(
                    "each affiliation must reference a department or a project"
                )
            if department_id:
                self._department(tenant_id, department_id, employee["company_id"])
            if project_id:
                self._project(tenant_id, project_id, employee["company_id"])
            key = (department_id, project_id)
            if key not in seen:
                seen.add(key)
                normalized.append(key)

        with self.database.connect() as connection:
            connection.execute(
                "delete from employee_affiliations "
                "where tenant_id = ? and employee_id = ?",
                (tenant_id, employee_id),
            )
            connection.executemany(
                """
                insert into employee_affiliations (
                  id, tenant_id, employee_id, department_id, project_id
                ) values (?, ?, ?, ?, ?)
                """,
                [
                    (
                        f"aff-{uuid.uuid4()}",
                        tenant_id,
                        employee_id,
                        department_id,
                        project_id,
                    )
                    for department_id, project_id in normalized
                ],
            )
        return self.list_for_employee(employee_id)

    def list_for_employee(self, employee_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self._employee(tenant_id, employee_id)
        return {
            "employee_id": employee_id,
            "affiliations": self._list(
                "employee_id",
                employee_id,
            ),
        }

    def list_for_department(self, department_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self._department(tenant_id, department_id)
        affiliations = self._list("department_id", department_id)
        return {
            "department_id": department_id,
            "employee_ids": [item["employee_id"] for item in affiliations],
            "affiliations": affiliations,
        }

    def list_for_project(self, project_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self._project(tenant_id, project_id)
        affiliations = self._list("project_id", project_id)
        return {
            "project_id": project_id,
            "employee_ids": [item["employee_id"] for item in affiliations],
            "affiliations": affiliations,
        }

    def delete(self, affiliation_id: str) -> None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            cursor = connection.execute(
                "delete from employee_affiliations where tenant_id = ? and id = ?",
                (tenant_id, affiliation_id),
            )
            if cursor.rowcount != 1:
                raise KeyError("affiliation not found")

    def _list(self, field: str, value: str) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                f"select * from employee_affiliations "
                f"where tenant_id = ? and {field} = ? "
                "order by created_at, id",
                (tenant_id, value),
            ).fetchall()
        return [dict(row) for row in rows]

    def _employee(self, tenant_id: str, employee_id: str) -> dict[str, Any]:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from employee_instances "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (tenant_id, employee_id),
            ).fetchone()
        if row is None:
            raise KeyError("employee not found")
        return dict(row)

    def _department(
        self,
        tenant_id: str,
        department_id: str,
        company_id: str | None = None,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from department_instances "
                "where tenant_id = ? and id = ? and deleted_at is null",
                (tenant_id, department_id),
            ).fetchone()
        if row is None:
            raise KeyError("department not found")
        if company_id is not None and row["company_id"] != company_id:
            raise ValueError("department does not belong to employee company")
        return dict(row)

    def _project(
        self,
        tenant_id: str,
        project_id: str,
        company_id: str | None = None,
    ) -> dict[str, Any]:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from projects "
                "where tenant_id = ? and project_id = ?",
                (tenant_id, project_id),
            ).fetchone()
        if row is None:
            raise KeyError("project not found")
        if company_id is not None and row["company_id"] != company_id:
            raise ValueError("project does not belong to employee company")
        return dict(row)
