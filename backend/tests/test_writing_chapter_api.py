from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from app.api.writing_router import build_writing_router
from app.api.conversation_router import build_conversation_router
from app.conversation_service import ConversationService
from app.writing_chapter_service import WritingChapterService
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO, local_chain, team, command


def app(db):
    value = FastAPI()
    @value.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-Test-CEO", CEO)):
            return await call_next(request)
    async def forbidden(task): raise AssertionError("Real Provider is not authorized")
    shared = ConversationService(db)
    value.include_router(build_conversation_router(db, forbidden, service=shared))
    value.include_router(build_writing_router(db, forbidden, conversation_service=shared))
    return value, shared


def test_api_chain_strict_body_scope_replay_and_download(tmp_path):
    db, _, w, b, c = setup(tmp_path); application, _ = app(db)
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}"
    chapter = root + f"/books/{b}/chapters/{c}"
    payload = {"request_id": "save", "expected_draft_ref": "ABSENT", "data": {"text": "原创 API 章节", "knowledge": []}}
    with TestClient(application) as client:
        assert client.get(root).status_code == 200
        assert client.get(chapter, headers={"X-Test-CEO": "other"}).status_code == 404
        assert client.post(chapter + "/commands/draft.saved", json={**payload, "source_class": "VERIFIED"}).status_code == 422
        first = client.post(chapter + "/commands/draft.saved", json=payload)
        assert first.status_code == 200
        assert client.post(chapter + "/commands/draft.saved", json=payload).json() == first.json()
        assert client.post(chapter + "/commands/draft.saved", json={**payload, "data": {"text": "不同", "knowledge": []}}).status_code == 409
        assert client.post(chapter + "/commands/package.prepared", json={**payload, "expected_draft_ref": first.json()["draft"]["ref"], "data": {"formal_ref": "fake", "introduction": "", "credits": "", "rights_declared": True, "target": "LOCAL_DOWNLOAD"}}).status_code == 404
        assert client.post(chapter + "/messages", json={"binding_ref": "fake", "request_id": "message", "body": "输入保留"}).status_code == 409
    with scope():
        # New IDs for this second author chain; no synthetic formal/package shortcuts.
        service = WritingChapterService(db)
        check = command(service, w, b, c, "inspection.recorded", {"mode": "AUTHOR_MANUAL", "checks": ["continuity", "language", "rights"], "note": ""})
        formal = command(service, w, b, c, "formal.confirmed", {"inspection_ref": check["ref"], "confirmed": True})
        package = command(service, w, b, c, "package.prepared", {"formal_ref": formal["ref"], "introduction": "合法介绍", "credits": "作者", "rights_declared": True, "target": "LOCAL_DOWNLOAD"})
    with TestClient(application) as client:
        response = client.get(chapter + f'/packages/{package["ref"]}/download')
        assert response.status_code == 200 and response.headers["x-content-sha256"] == package["content_sha256"]
        assert "attachment" in response.headers["content-disposition"]
        assert response.json()["snapshot"]["text"] == "原创 API 章节"


def test_shared_router_does_not_mark_inflight_unverified(tmp_path):
    db, _, w, b, c = setup(tmp_path); application, shared = app(db)
    with scope():
        employee, assignment = team(db, w)
        topic = shared.create(COMPANY, request_id="shared-router", employee_ref=employee)
        claim, _ = shared.prepare(COMPANY, employee, body="只验证在途读取", request_id="inflight", assignment_ref=assignment, conversation_id=topic["conversation_id"])
    with TestClient(application) as client:
        result = client.get(f'/api/workspace/v1/companies/{COMPANY}/conversations/{topic["conversation_id"]}')
        assert result.status_code == 200
        assert result.json()["attempts"][0]["status"] == "RUNNING"
    assert claim["attempt_id"] in shared.running


def test_chapter_api_source_projection_missing_link_target_no_writes(tmp_path):
    from backend.tests.test_writing_entry_readiness import database_values
    db, _, w, b, c = setup(tmp_path)
    application, _ = app(db)
    with db.connect() as con:
        con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values ('selfuse',?,'WRITING_CHAPTER_FROM_LEARNING','absent-learning',current_timestamp)",(c,))
    before = database_values(db)
    with TestClient(application) as client:
        response = client.get(f'/api/workspace/v1/companies/{COMPANY}/writing/{w}/books/{b}/chapters/{c}')
    assert response.status_code == 200,response.text
    assert response.json()['creation_source'] == {'status':'MISSING'}
    assert database_values(db) == before
