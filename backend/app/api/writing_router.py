"""Bounded local Writing API; execution opt-in is server owned."""
from typing import Literal
from fastapi import APIRouter, BackgroundTasks, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field

from ..runtime import RuntimeScopeError
from ..writing_chapter_service import WritingChapterService, WritingConflict


class CommandIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=1, max_length=128)
    expected_draft_ref: str = Field(min_length=1, max_length=256)
    data: dict


class MessageIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    binding_ref: str = Field(min_length=1, max_length=256)
    body: str = Field(min_length=1, max_length=8000)
    request_id: str = Field(min_length=1, max_length=128)
    model_key: str = Field(default="", max_length=256)
    retry_no: int = Field(default=0, ge=0, le=1)
    work_ref: str = Field(default="", max_length=256)


class HolderIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    employee_id: str = Field(min_length=1, max_length=256)
    expected_revision: int = Field(ge=0)


class ModelIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_key: str = Field(min_length=1, max_length=256)


class OperatingIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=1, max_length=128)
    expected_ref: str = Field(default="", max_length=256)
    data: dict


def build_writing_router(database, executor, *, conversation_service=None, allow_execution=False, service=None, entry_service=None, operating=None):
    router = APIRouter(prefix="/api/workspace/v1/companies/{company_id}/writing/{workspace_id}")
    service = service or WritingChapterService(database, conversation_service=conversation_service, allow_execution=allow_execution, entry_service=entry_service)

    def invoke(callback):
        try:
            return callback()
        except (RuntimeScopeError, KeyError) as error:
            raise HTTPException(404, str(error)) from error
        except WritingConflict as error:
            raise HTTPException(409, str(error)) from error
        except (ValueError, TypeError, AttributeError) as error:
            raise HTTPException(422, str(error)) from error

    if entry_service is not None:
        @router.get("/entry")
        def entry(company_id: str, workspace_id: str):
            return invoke(lambda: entry_service.metadata(company_id, workspace_id))

        @router.post("/responsibility")
        def responsibility(company_id: str, workspace_id: str, payload: HolderIn):
            return invoke(lambda: entry_service.assign(company_id, workspace_id, **payload.model_dump()))

        @router.post("/model")
        def model(company_id: str, workspace_id: str, payload: ModelIn):
            return invoke(lambda: entry_service.select_model(company_id, workspace_id, payload.model_key))

    from ..writing_book_service import WritingBookService
    books = WritingBookService(database, chapters=service)

    @router.get("/books/{book_ref}/context")
    def book_context(company_id: str, workspace_id: str, book_ref: str, ref: str = ""):
        return invoke(lambda: books.read(company_id, workspace_id, book_ref, ref))

    @router.post("/books/{book_ref}/context")
    def save_book_context(company_id: str, workspace_id: str, book_ref: str, payload: OperatingIn):
        if set(payload.data) != {"context"}:
            raise HTTPException(422, "作品结构保存字段不匹配。")
        return invoke(lambda: books.save(company_id, workspace_id, book_ref, payload.request_id, payload.expected_ref, payload.data["context"]))

    @router.get("")
    def collection(company_id: str, workspace_id: str):
        return invoke(lambda: service.collection(company_id, workspace_id))

    @router.get("/books/{book_ref}/chapters/{chapter_ref}")
    def chapter(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str):
        return invoke(lambda: service.chapter(company_id, workspace_id, book_ref, chapter_ref))

    @router.get("/books/{book_ref}/chapters/{chapter_ref}/manuscript")
    def manuscript(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, version_ref: str = ""):
        return invoke(lambda: service.manuscript(company_id, workspace_id, book_ref, chapter_ref, version_ref))

    @router.get("/books/{book_ref}/chapters/{chapter_ref}/manuscript/copy")
    def copy_manuscript(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, version_ref: str = ""):
        text = invoke(lambda: service.manuscript_text(company_id, workspace_id, book_ref, chapter_ref, version_ref))
        return Response(text, media_type="text/plain", headers={"Cache-Control": "no-store"})

    @router.get("/books/{book_ref}/chapters/{chapter_ref}/manuscript/export")
    def export_manuscript(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, version_ref: str = ""):
        text = invoke(lambda: service.manuscript_text(company_id, workspace_id, book_ref, chapter_ref, version_ref))
        return Response(text, media_type="text/plain", headers={
            "Content-Disposition": 'attachment; filename="manuscript.txt"', "Cache-Control": "no-store"})

    @router.post("/books/{book_ref}/chapters/{chapter_ref}/commands/{action}")
    def command(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, action: str, payload: CommandIn):
        return invoke(lambda: service.command(company_id, workspace_id, book_ref, chapter_ref, action, **payload.model_dump()))

    @router.get("/books/{book_ref}/chapters/{chapter_ref}/packages/{package_ref}/download")
    def download(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, package_ref: str):
        content, digest = invoke(lambda: service.download(company_id, workspace_id, book_ref, chapter_ref, package_ref))
        return Response(content, media_type="application/json", headers={
            "Content-Disposition": 'attachment; filename="writing-local-package.json"',
            "X-Content-SHA256": digest, "Cache-Control": "no-store"})

    @router.get("/books/{book_ref}/chapters/{chapter_ref}/discussion/{binding_ref}")
    def discussion(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, binding_ref: str):
        return invoke(lambda: service.discussion(company_id, workspace_id, book_ref, chapter_ref, binding_ref))

    @router.post("/books/{book_ref}/chapters/{chapter_ref}/discussion")
    def bind_discussion(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, payload: CommandIn):
        return invoke(lambda: service.bind_discussion(company_id, workspace_id, book_ref, chapter_ref, **payload.model_dump()))

    @router.post("/books/{book_ref}/chapters/{chapter_ref}/messages", status_code=202)
    def message(company_id: str, workspace_id: str, book_ref: str, chapter_ref: str, payload: MessageIn, background: BackgroundTasks):
        claim, created = invoke(lambda: service.prepare_message(company_id, workspace_id, book_ref, chapter_ref, **payload.model_dump()))
        if created:
            background.add_task(service.conversations.execute, claim, executor)
        return {"attempt": claim, "created": created, "source_class": claim.get("execution_selection", {}).get("source_class", "CONTROLLED_EXECUTOR")}

    if operating is not None:
        @router.get("/operating/overview")
        def operating_overview(company_id: str, workspace_id: str):
            return invoke(lambda: operating.operating_overview(company_id, workspace_id))

        @router.get("/operating/directions")
        def directions(company_id: str, workspace_id: str):
            return invoke(lambda: operating.directions_collection(company_id, workspace_id))

        @router.get("/operating/directions/{ref}")
        def direction(company_id: str, workspace_id: str, ref: str):
            return invoke(lambda: operating.direction_content(company_id, workspace_id, ref))

        @router.post("/operating/directions/commands/{action}")
        def direction_command(company_id: str, workspace_id: str, action: Literal["save-direction", "apply-direction"], payload: OperatingIn):
            return invoke(lambda: operating.direction_command(company_id, workspace_id, action, **payload.model_dump()))

        @router.get("/operating/learnings")
        def learnings(company_id: str, workspace_id: str):
            return invoke(lambda: operating.learnings_collection(company_id, workspace_id))

        @router.get("/operating/learnings/{ref}")
        def learning(company_id: str, workspace_id: str, ref: str):
            return invoke(lambda: operating.learning_content(company_id, workspace_id, ref))

        @router.post("/operating/learnings/commands/{action}")
        def learning_command(company_id: str, workspace_id: str, action: Literal["save-learning", "use-learning"], payload: OperatingIn):
            return invoke(lambda: operating.learning_command(company_id, workspace_id, action, **payload.model_dump()))

        @router.get("/operating/snapshots")
        def snapshots(company_id: str, workspace_id: str):
            return invoke(lambda: operating.snapshots_collection(company_id, workspace_id))

        @router.get("/operating/snapshots/{ref}")
        def snapshot(company_id: str, workspace_id: str, ref: str):
            return invoke(lambda: operating.snapshot_content(company_id, workspace_id, ref))

        @router.post("/operating/snapshots/commands/{action}")
        def snapshot_command(company_id: str, workspace_id: str, action: Literal["save-snapshot"], payload: OperatingIn):
            return invoke(lambda: operating.snapshot_command(company_id, workspace_id, action, **payload.model_dump()))

        @router.get("/operating/observations")
        def observations(company_id: str, workspace_id: str):
            return invoke(lambda: operating.observations_collection(company_id, workspace_id))

        @router.get("/operating/observations/{ref}")
        def observation(company_id: str, workspace_id: str, ref: str):
            return invoke(lambda: operating.observation_content(company_id, workspace_id, ref))

        @router.post("/operating/observations/commands/{action}")
        def observation_command(company_id: str, workspace_id: str, action: Literal["save-observation"], payload: OperatingIn):
            return invoke(lambda: operating.observation_command(company_id, workspace_id, action, **payload.model_dump()))

    return router
