"""Strict scoped Music commands; reads never trigger execution."""
from typing import Literal
from urllib.parse import unquote
from fastapi import APIRouter, BackgroundTasks, HTTPException, Header, Response, Request
from pydantic import BaseModel, ConfigDict, Field
from .conversation_router import ReferenceIn
from ..runtime import RuntimeScopeError
from ..runtime.music import MusicConflict


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Basis(Strict):
    lyrics_ref: str = Field(min_length=1, max_length=256)
    production_ref: str = Field(min_length=1, max_length=256)
    master_ref: str = Field(default="", max_length=256)


class LyricsSelection(Strict):
    kind: Literal["lyrics"]
    version_ref: str = Field(min_length=1, max_length=256)
    draft_revision: str = Field(min_length=1, max_length=128)
    start: int = Field(ge=0, strict=True)
    end: int = Field(gt=0, strict=True)
    excerpt: str = Field(max_length=20000)
    locator: Literal["lyrics"]


class AudioSelection(Strict):
    kind: Literal["audio"]
    song_ref: str = Field(min_length=1, max_length=256)
    candidate_ref: str = Field(min_length=1, max_length=256)
    candidate_version_ref: str = Field(min_length=1, max_length=256)
    asset_ref: str = Field(min_length=1, max_length=256)
    sha256: str = Field(pattern="^[0-9a-f]{64}$")
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    duration: float = Field(gt=0, le=600)
    anchor: Literal["candidate-audio"]


class CommandIn(Strict):
    request_id: str = Field(min_length=1, max_length=128)
    expected: dict = Field(default_factory=dict)
    data: dict


class DiscussionIn(Strict):
    request_id: str = Field(min_length=1, max_length=128)
    expected: Basis
    assignment_ref: str = Field(min_length=1, max_length=256)


class MessageIn(Strict):
    work_ref: str = Field(default="", max_length=256)
    binding_ref: str = Field(min_length=1, max_length=256)
    request_id: str = Field(min_length=1, max_length=128)
    body: str = Field(min_length=1, max_length=2000)
    model_key: str = Field(min_length=1, max_length=256)
    expected: Basis
    selection: LyricsSelection | AudioSelection = Field(discriminator="kind")
    references: list[ReferenceIn] = Field(default_factory=list, max_length=8)


class CandidateIn(Strict):
    binding_ref: str = Field(min_length=1, max_length=256)
    attempt_id: str = Field(min_length=1, max_length=256)
    request_id: str = Field(min_length=1, max_length=128)


class OperatingIn(Strict):
    request_id: str = Field(min_length=1, max_length=128)
    expected_ref: str = Field(default="", max_length=256)
    data: dict


def build_music_router(database, executor, *, service):
    router = APIRouter(prefix="/api/workspace/v1/companies/{company}/music/{workspace}")
    def invoke(callback):
        try: return callback()
        except (RuntimeScopeError, KeyError, FileNotFoundError) as error: raise HTTPException(404, str(error)) from error
        except MusicConflict as error: raise HTTPException(409, str(error)) from error
        except (ValueError, TypeError, OSError) as error: raise HTTPException(422, str(error)) from error
    @router.get("")
    def collection(company: str, workspace: str): return invoke(lambda: service.collection(company, workspace))
    @router.get("/operating")
    def operating(company: str, workspace: str): return invoke(lambda: service.operating_collection(company, workspace))
    @router.get("/operating/{ref}")
    def operating_content(company: str, workspace: str, ref: str): return invoke(lambda: service.operating_content(company, workspace, ref))
    @router.post("/operating/commands/{action}")
    def operating_command(company: str, workspace: str, action: Literal["save-scope", "save-snapshot", "save-reference", "save-direction", "save-observation", "create-report", "confirm-report", "save-learning", "use-learning", "create-song", "apply-direction"], payload: OperatingIn):
        return invoke(lambda: service.operating_command(company, workspace, action, **payload.model_dump()))
    @router.post("/songs")
    def create(company: str, workspace: str, payload: CommandIn): return invoke(lambda: service.command(company, workspace, "", "create", **payload.model_dump()))
    @router.get("/songs/{song}")
    def content(company: str, workspace: str, song: str): return invoke(lambda: service.content(company, workspace, song))
    @router.post("/songs/{song}/commands/{action}")
    def command(company: str, workspace: str, song: str, action: str, payload: CommandIn): return invoke(lambda: service.command(company, workspace, song, action, **payload.model_dump()))
    @router.get("/songs/{song}/imports/{request_id}")
    def import_status(company: str, workspace: str, song: str, request_id: str):
        return invoke(lambda: service.import_status(company, workspace, song, request_id))
    @router.post("/songs/{song}/audio-import")
    async def import_audio(company: str, workspace: str, song: str, request: Request, metadata: str = Header(alias="X-Music-Import")):
        if request.headers.get("content-type") != "audio/wav" or len(metadata) > 4096:
            raise HTTPException(422, "需要受限WAV文件与准确导入依据。")
        # Scope is checked before reading an authenticated but potentially large body.
        invoke(lambda: service.entry.authoring_scope(company, workspace, write=True))
        try: payload = CommandIn.model_validate_json(unquote(metadata, errors="strict"))
        except ValueError as error: raise HTTPException(422, "导入依据不完整。") from error
        try:
            with service.receiving_import(company, workspace, song, payload.request_id):
                raw = bytearray()
                async for chunk in request.stream():
                    if len(raw) + len(chunk) > 16_000_000: raise HTTPException(413, "音频超过16MB。")
                    raw.extend(chunk)
                return invoke(lambda: service.command(company, workspace, song, "import-audio", **payload.model_dump(), raw_audio=bytes(raw)))
        except MusicConflict as error: raise HTTPException(409, str(error)) from error
    @router.get("/songs/{song}/assets/{asset}")
    def media(company: str, workspace: str, song: str, asset: str, range_value: str | None = Header(default=None, alias="Range")):
        def read():
            with database.connect() as con:
                service.entry.authoring_scope(company, workspace, connection=con)
                try: raw, status, headers = service.media.read(con, company, workspace, song, asset, range_value)
                except ValueError as error:
                    if range_value and "范围" in str(error): raise HTTPException(416, str(error)) from error
                    raise
            return Response(raw, status_code=status, media_type="audio/wav", headers=headers)
        return invoke(read)
    @router.post("/songs/{song}/discussion")
    def bind(company: str, workspace: str, song: str, payload: DiscussionIn): return invoke(lambda: service.bind_discussion(company, workspace, song, **payload.model_dump()))
    @router.get("/songs/{song}/discussion/{binding}")
    def query(company: str, workspace: str, song: str, binding: str, request_id: str | None = None, attempt_id: str | None = None): return invoke(lambda: service.query_request(company, workspace, song, binding, request_id=request_id, attempt_id=attempt_id))
    @router.post("/songs/{song}/messages", status_code=202)
    def message(company: str, workspace: str, song: str, payload: MessageIn, background: BackgroundTasks):
        claim, created = invoke(lambda: service.prepare_message(company, workspace, song, **payload.model_dump()))
        if created: background.add_task(service.conversations.execute, claim, executor)
        return {"attempt": claim, "created": created}
    @router.post("/songs/{song}/reply-candidate")
    def candidate(company: str, workspace: str, song: str, payload: CandidateIn): return invoke(lambda: service.materialize_candidate(company, workspace, song, **payload.model_dump()))
    return router
