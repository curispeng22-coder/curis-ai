"""HTTP boundary for the declarative Workspace Package P0."""

from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from .database import Database
from .tenant_context import TenantContext
from .workspace_package_runtime import (
    PackageConflictError,
    PackageScopeError,
    PackageValidationError,
    WorkspacePackageRuntime,
)


class InstallPackageIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    company_id: str = Field(min_length=1, max_length=128)
    department_id: str = Field(min_length=1, max_length=128)
    business_id: str = Field(min_length=1, max_length=128)
    business_name: str = Field(min_length=1, max_length=160)
    business_goal: str = Field(default="", max_length=2000)
    business_positioning: str = Field(default="", max_length=2000)
    source_path: str = Field(min_length=1, max_length=4096)


class TeamAssignmentBasis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ref: str = Field(min_length=1, max_length=256)
    revision: int = Field(ge=1, strict=True)
    employee_ref: str = Field(min_length=1, max_length=256)

class TeamExpected(BaseModel):
    model_config = ConfigDict(extra="forbid")
    business_id: str = Field(min_length=1, max_length=256)
    package_id: str = Field(min_length=1, max_length=256)
    version: str = Field(min_length=1, max_length=128)
    digest: str = Field(pattern="^[0-9a-f]{64}$")
    assignments: list[TeamAssignmentBasis] = Field(max_length=32)

class CompleteTeamIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company_id: str = Field(min_length=1, max_length=256)
    ceo_id: str = Field(min_length=1, max_length=128)
    request_id: str = Field(min_length=1, max_length=128)
    expected: TeamExpected

class PackageObjectIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    object_type: str = Field(min_length=1, max_length=64)
    owner_ref: str = Field(default="", max_length=128)
    data: dict[str, Any]


class PackageCommandIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)


class PackageUpdateIn(PackageCommandIn):
    source_path: str = Field(min_length=1, max_length=4096)


class CompanyOperateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ceo_id: str = Field(min_length=1, max_length=128)
    responsibility_type: str = Field(
        min_length=3, max_length=64, pattern=r"^[A-Z][A-Z0-9_]{2,63}$",
    )


def build_workspace_package_router(database: Database) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/packages", tags=["workspace-packages"])
    runtime = WorkspacePackageRuntime(database)

    def safe(call: Callable[[], Any]) -> Any:
        try:
            return call()
        except PackageScopeError as error:
            raise HTTPException(status_code=404, detail="Package Workspace 不存在或无权访问") from error
        except PackageConflictError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except PackageValidationError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except OSError as error:
            raise HTTPException(status_code=500, detail="Package Store 操作失败") from error

    def require_ceo(ceo_id: str, company_id: str = "") -> None:
        identity = TenantContext.current_identity()
        if identity.get("role") not in {"owner", "ceo", "test"} or identity.get("ceo_id") != ceo_id:
            raise HTTPException(status_code=403, detail="只有当前 CEO 可以修改 Workspace Package")
        if company_id and identity.get("company_id") and identity["company_id"] != company_id:
            raise HTTPException(status_code=404, detail="Company 不存在或无权访问")

    @router.get("/navigation")
    def navigation(company_id: str | None = Query(default=None, max_length=128)) -> dict[str, Any]:
        return {"items": safe(lambda: runtime.navigation(company_id))}

    @router.get("/registry")
    def registry(include_archived: bool = False) -> dict[str, Any]:
        return {"packages": safe(lambda: runtime.registry(include_archived=include_archived))}

    @router.post("/workspaces/{workspace_id}/initial-team")
    def complete_initial_team(workspace_id: str, payload: CompleteTeamIn):
        require_ceo(payload.ceo_id, payload.company_id)
        return safe(lambda: runtime.complete_professional_team(workspace_id, **payload.model_dump()))

    @router.post("/install", status_code=201)
    def install(payload: InstallPackageIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id, payload.company_id)
        return safe(lambda: runtime.install(
            payload.source_path,
            payload.company_id,
            department_id=payload.department_id,
            business_id=payload.business_id,
            business_name=payload.business_name,
            business_goal=payload.business_goal,
            business_positioning=payload.business_positioning,
        ))

    @router.get("/workspaces/{workspace_id}")
    def get_workspace(workspace_id: str) -> dict[str, Any]:
        return safe(lambda: runtime.get_workspace(workspace_id))

    @router.get("/workspaces/{workspace_id}/lifecycle")
    def lifecycle(workspace_id: str) -> dict[str, Any]:
        return safe(lambda: runtime.lifecycle(workspace_id))

    @router.post("/workspaces/{workspace_id}/update-preview")
    def preview_update(workspace_id: str, payload: PackageUpdateIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.preview_update(workspace_id, payload.source_path))

    @router.post("/workspaces/{workspace_id}/update")
    def update(workspace_id: str, payload: PackageUpdateIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.update(workspace_id, payload.source_path))

    @router.post("/workspaces/{workspace_id}/rollback")
    def rollback(workspace_id: str, payload: PackageCommandIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.rollback(workspace_id))

    @router.post("/workspaces/{workspace_id}/actions/{action_id}", status_code=201)
    def create_object(workspace_id: str, action_id: str, payload: PackageObjectIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.create_object(
            workspace_id, action_id, payload.object_type, payload.data, payload.owner_ref,
        ))

    @router.post("/workspaces/{workspace_id}/objects/{object_id}/company-operate")
    def operate_object(workspace_id: str, object_id: str, payload: CompanyOperateIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.operate_object(
            workspace_id, object_id, payload.responsibility_type,
        ))

    @router.get("/workspaces/{workspace_id}/objects/{object_id}/company-integration")
    def resolve_company_integration(workspace_id: str, object_id: str) -> dict[str, Any]:
        return safe(lambda: runtime.resolve_company_integration(workspace_id, object_id))

    @router.post("/workspaces/{workspace_id}/disable")
    def disable(workspace_id: str, payload: PackageCommandIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.disable(workspace_id))

    @router.post("/workspaces/{workspace_id}/uninstall")
    def uninstall(workspace_id: str, payload: PackageCommandIn) -> dict[str, Any]:
        require_ceo(payload.ceo_id)
        return safe(lambda: runtime.uninstall(workspace_id))

    return router
