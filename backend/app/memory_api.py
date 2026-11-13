from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field


class MemoryCreateIn(BaseModel):
    memory_type: str
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    project_id: str | None = None
    employee_id: str | None = None
    source_task_id: str | None = None
    confidence: float = 1.0


class MemoryUpdateIn(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    confidence: float | None = None
    status: str | None = None


class MemoryRetrieveIn(BaseModel):
    query: str
    project_id: str | None = None
    employee_id: str | None = None
    limit: int = 5


class ContextBuildIn(BaseModel):
    task_id: str


def build_memory_router(memory_service, context_service) -> APIRouter:
    router = APIRouter()

    @router.get("/api/workspace/memory")
    def list_memory(
        q: str = Query(default="", max_length=200),
        scope: str = Query(default="all"),
        project_id: str = Query(default=""),
        employee_id: str = Query(default=""),
        include_archived: bool = Query(default=False),
    ):
        return _call(
            memory_service.list_entries,
            query=q,
            scope=scope,
            project_id=project_id,
            employee_id=employee_id,
            include_archived=include_archived,
        )

    @router.post("/api/workspace/memory", status_code=201)
    def create_memory(payload: MemoryCreateIn):
        return _call(memory_service.create_entry, **payload.model_dump())

    @router.post("/api/workspace/memory/retrieve")
    def retrieve_memory(payload: MemoryRetrieveIn):
        entries = _call(memory_service.retrieve, **payload.model_dump())
        return {"entries": entries}

    @router.get("/api/workspace/memory/{memory_id}")
    def get_memory(memory_id: str):
        return _call(memory_service.get_entry, memory_id)

    @router.patch("/api/workspace/memory/{memory_id}")
    def update_memory(memory_id: str, payload: MemoryUpdateIn):
        return _call(
            memory_service.update_entry,
            memory_id,
            **payload.model_dump(exclude_unset=True),
        )

    @router.post("/api/workspace/context/build", status_code=201)
    def build_context(payload: ContextBuildIn):
        return _call(context_service.build, payload.task_id)

    @router.get("/api/workspace/context/task/{task_id}")
    def latest_task_context(task_id: str):
        context = _call(context_service.latest_for_task, task_id)
        return {"context_package": context}

    @router.get("/api/workspace/context/{package_id}")
    def get_context(package_id: str):
        return _call(context_service.get, package_id)

    return router


def _call(function, *args, **kwargs) -> Any:
    try:
        return function(*args, **kwargs)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
