from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..company_project_runtime import CompanyProjectRuntime
from ..database import Database
from ..employee_templates import EmployeeTemplateContract
from ..result_store import ResultStore
from ..tenant_context import TenantContext


def _ai_readiness(database: Database, tenant_id: str) -> dict[str, bool]:
    """首屏 first-run 判断：是否已有私有模型 / 是否已绑员工能力。

    作为 CEO 工作台「接入 AI 能力」引导门禁的唯一真源，避免前端各自探测。
    """
    try:
        with database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT count(*) FROM tenant_private_capabilities "
                "WHERE tenant_id=? AND capability_type='model'",
                (tenant_id,),
            )
            has_private_model = (cursor.fetchone() or (0,))[0] > 0
            cursor.execute(
                "SELECT count(*) FROM employee_capability_bindings WHERE tenant_id=?",
                (tenant_id,),
            )
            has_bound_employee = (cursor.fetchone() or (0,))[0] > 0
            return {
                "has_private_model": has_private_model,
                "has_bound_employee": has_bound_employee,
            }
    except Exception:
        return {"has_private_model": False, "has_bound_employee": False}


def build_home_router(database: Database) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/home", tags=["workspace-home"])
    companies = CompanyProjectRuntime(database)
    organization = EmployeeTemplateContract(database)

    @router.get("/summary")
    def get_home_summary() -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        company_items = companies.list_companies()["companies"]
        company = next((item for item in company_items if item["is_default"]), company_items[0] if company_items else None)
        if company is None:
            return _empty_summary(tenant_id)

        company_id = company["company_id"]
        departments = organization.list_department_instances(company_id)["departments"]
        projects = companies.list_projects(company_id)["projects"]
        employees = [
            item
            for item in organization.list_employee_instances()["employees"]
            if item.get("company_id") == company_id
        ]
        employee_counts = _count_by(employees, "department_id")
        project_counts = _count_by(projects, "department_id")
        department_items = [
            {
                **department,
                "employee_count": employee_counts.get(department["id"], 0),
                "project_count": project_counts.get(department["id"], 0),
            }
            for department in departments
        ]
        return {
            "tenant_id": tenant_id,
            "company": company,
            "departments": department_items,
            "projects": projects,
            "employees": employees,
            "recent_artifacts": _recent_artifacts(database, tenant_id),
            "ai_readiness": _ai_readiness(database, tenant_id),
            "counts": {
                "departments": len(departments),
                "projects": len(projects),
                "employees": len(employees),
            },
        }

    return router


def _count_by(items: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = item.get(field)
        if value:
            counts[value] = counts.get(value, 0) + 1
    return counts


def _recent_artifacts(database: Database, tenant_id: str, limit: int = 5) -> list[dict[str, Any]]:
    return [
        {**artifact, "type": artifact["artifact_type"]}
        for artifact in ResultStore(database).list_artifacts(limit=limit)
    ]


def _empty_summary(tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "company": None,
        "departments": [],
        "projects": [],
        "employees": [],
        "recent_artifacts": [],
        "ai_readiness": {"has_private_model": False, "has_bound_employee": False},
        "counts": {"departments": 0, "projects": 0, "employees": 0},
    }
