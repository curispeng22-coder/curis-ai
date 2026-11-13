"""Router for company-wide object search (read-only)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..object_search_service import ObjectSearchService


def build_object_search_router(database):
    router = APIRouter(prefix="/api/workspace/companies/{company_id}", tags=["object-search"])
    service = ObjectSearchService(database)

    @router.get("/object-search")
    def object_search(company_id: str, q: str = ""):
        try:
            return service.search(company_id, q)
        except KeyError as error:
            raise HTTPException(status_code=404, detail="公司不存在或无权访问") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router
