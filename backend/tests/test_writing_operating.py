"""WR-DIRECTION + WR-LEARNING operating surfaces (P1-a).

Local manual facts, forced UNVERIFIED, idempotent, workspace-scoped.
Fixtures reuse the accepted writing vertical chain; no Provider calls.
"""
import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.writing_router import build_writing_router
from app.database import Database
from app.runtime import RuntimeScopeError
from app.workspace_package_runtime import WorkspacePackageRuntime
from app.writing_chapter_service import WritingChapterService, WritingConflict
from app.writing_operating_service import WritingOperatingService
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO, SOURCE, command
from app.writing_chapter_service import PACKAGE_DIGEST
from app.workspace_package_runtime import validate_package

COMPANY_B = "writing-test-company-b"
CEO_B = "writing-test-author-b"


def service(db):
    chapters = WritingChapterService(db)
    return WritingOperatingService(db, chapter_service=chapters), chapters


def direction_data(**overrides):
    base = {"title": "都市悬疑方向", "body": "雨夜、匿名信、克制的第三人称。",
        "scope_ref": "", "reference_refs": [], "learning_ref": "", "confirmed": True}
    base.update(overrides)
    return base


def learning_data(**overrides):
    base = {"title": "开篇经验", "body": "第一章必须在三百字内给出异常物。",
        "basis_refs": [], "applicability": "悬疑类长篇开篇", "counterexample": "温情回忆叙事不适用", "accepted": True}
    base.update(overrides)
    return base


def setup_b(path):
    db = Database(str(path / "writing-b.sqlite")); db.initialize()
    with db.connect() as con:
        con.execute("insert into companies(company_id,tenant_id,ceo_id,name,status) values (?,'selfuse',?,'B 公司','active')", (COMPANY_B, CEO_B))
        con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status) "
            "values ('writing-test-department-b','selfuse',?,'writing-test-template','B 部门','TEST','active')", (COMPANY_B,))
    with TenantScopeB():
        runtime = WorkspacePackageRuntime(db, path / "package-store-b")
        installed = runtime.install(SOURCE, COMPANY_B, department_id="writing-test-department-b", business_id="b-business", business_name="B 写作")
        wb = installed["instance"]["workspace_id"]
        book = runtime.create_object(wb, "core.domain-object.create", "WritingBook", {"title": "B 作品", "status": "DRAFT"})["object_id"]
    return db, wb, book


class TenantScopeB:
    def __enter__(self):
        from app.tenant_context import TenantContext
        self._cm = TenantContext.scope(tenant_id="selfuse", company_id=COMPANY_B, ceo_id=CEO_B, role="ceo")
        return self._cm.__enter__()

    def __exit__(self, *args):
        return self._cm.__exit__(*args)


# ── direction ────────────────────────────────────────────────────────────

def test_save_direction_workspace_and_book_scope_versioning(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        first = op.direction_command(COMPANY, w, "save-direction", request_id="d1", data=direction_data(confirmed=False))
        assert first["record"]["data"]["confirmed_by"] == ""
        assert first["record"]["verification_status"] == "UNVERIFIED"
        # Unconfirmed direction cannot be applied.
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "apply-direction", request_id="d2",
                data={"direction_ref": first["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": True, "historical": False})
        # Revision 2 confirms; unknown expected_ref fails closed (404, same as CG chain).
        with pytest.raises(RuntimeScopeError):
            op.direction_command(COMPANY, w, "save-direction", request_id="d3", expected_ref="wr-direction-missing",
                data=direction_data())
        second = op.direction_command(COMPANY, w, "save-direction", request_id="d3", expected_ref=first["result_ref"],
            data=direction_data())
        assert second["record"]["data"]["revision"] == 2
        assert second["record"]["data"]["previous_ref"] == first["result_ref"]
        assert second["record"]["data"]["identity_ref"] == first["result_ref"]
        assert second["record"]["data"]["confirmed_by"] == CEO
        # apply links chapter to the confirmed direction.
        applied = op.direction_command(COMPANY, w, "apply-direction", request_id="d4",
            data={"direction_ref": second["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": True, "historical": False})
        assert applied["chapter_ref"] == c
        with db.connect() as con:
            links = con.execute("select count(*) from runtime_links where source_id=? and relation='WRITING_DIRECTION_REFERENCE' and target_id=?",
                (c, second["result_ref"])).fetchone()[0]
        assert links == 1
        # Repeated apply stays idempotent (no duplicate link).
        op.direction_command(COMPANY, w, "apply-direction", request_id="d5",
            data={"direction_ref": second["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": True, "historical": False})
        with db.connect() as con:
            assert con.execute("select count(*) from runtime_links where source_id=? and relation='WRITING_DIRECTION_REFERENCE'", (c,)).fetchone()[0] == 1
        # Book-scoped direction accepted; invalid book rejected.
        ok = op.direction_command(COMPANY, w, "save-direction", request_id="d6", data=direction_data(scope_ref=b))
        assert ok["record"]["data"]["scope_ref"] == b
        with pytest.raises(RuntimeScopeError):
            op.direction_command(COMPANY, w, "save-direction", request_id="d7", data=direction_data(scope_ref="not-a-book"))


def test_direction_reference_refs_bounded_and_in_scope(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        ok = op.direction_command(COMPANY, w, "save-direction", request_id="r1",
            data=direction_data(reference_refs=[b, c]))
        assert ok["record"]["data"]["reference_refs"] == [b, c]
        with pytest.raises(RuntimeScopeError):
            op.direction_command(COMPANY, w, "save-direction", request_id="r2",
                data=direction_data(reference_refs=["package-object-foreign"]))
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "save-direction", request_id="r3",
                data=direction_data(reference_refs=[b, b]))
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "save-direction", request_id="r4",
                data=direction_data(reference_refs=[str(i) for i in range(9)]))
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "save-direction", request_id="r5",
                data=direction_data(confirmed="yes"))


def test_direction_replay_same_fingerprint_diff_conflict(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        payload = direction_data()
        first = op.direction_command(COMPANY, w, "save-direction", request_id="same", data=payload)
        replay = op.direction_command(COMPANY, w, "save-direction", request_id="same", data=payload)
        assert replay == first
        with pytest.raises(WritingConflict):
            op.direction_command(COMPANY, w, "save-direction", request_id="same", data=direction_data(title="改了"))


def test_direction_apply_chapter_scope_fail_closed(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        d = op.direction_command(COMPANY, w, "save-direction", request_id="x1", data=direction_data())
        # chapter from another book, swapped book/chapter pair, historical missing.
        with pytest.raises(RuntimeScopeError):
            op.direction_command(COMPANY, w, "apply-direction", request_id="x2",
                data={"direction_ref": d["result_ref"], "book_ref": b, "chapter_ref": b, "confirmed": True, "historical": False})
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "apply-direction", request_id="x3",
                data={"direction_ref": d["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": False, "historical": False})
        # Old revision without historical flag rejected.
        old = op.direction_command(COMPANY, w, "save-direction", request_id="x4", expected_ref=d["result_ref"],
            data=direction_data(body="修订后的方向正文。"))
        with pytest.raises(WritingConflict):
            op.direction_command(COMPANY, w, "apply-direction", request_id="x5",
                data={"direction_ref": d["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": True, "historical": False})
        applied = op.direction_command(COMPANY, w, "apply-direction", request_id="x6",
            data={"direction_ref": d["result_ref"], "book_ref": b, "chapter_ref": c, "confirmed": True, "historical": True})
        assert applied["direction_ref"] == d["result_ref"]


# ── learning ─────────────────────────────────────────────────────────────

def test_save_learning_forced_unverified_basis_snapshot(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        saved = op.learning_command(COMPANY, w, "save-learning", request_id="l1",
            data=learning_data(basis_refs=[c]))
        data = saved["record"]["data"]
        assert data["validation"] == "UNVERIFIED"
        assert data["accepted_by"] == CEO
        assert c in data["basis"] and len(data["basis"][c]) == 64
        assert saved["record"]["verification_status"] == "UNVERIFIED"
        # Client cannot force a validation state.
        with pytest.raises(ValueError):
            op.learning_command(COMPANY, w, "save-learning", request_id="l2",
                data=learning_data(validation="VERIFIED"))
        # Tampered basis record is detected on read.
        with db.connect() as con:
            row = con.execute("select data_json from runtime_entities where entity_id=?", (saved["result_ref"],)).fetchone()
            tampered = json.loads(row["data_json"]); tampered["title"] = "被篡改"
            con.execute("update runtime_entities set data_json=? where entity_id=?",
                (json.dumps(tampered, ensure_ascii=False), saved["result_ref"]))
        with pytest.raises(ValueError):
            op.learning_content(COMPANY, w, saved["result_ref"])


def test_use_learning_creates_new_chapter_without_touching_latest(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, chapters = service(db)
        before = chapters.chapter(COMPANY, w, b, c)
        learning = op.learning_command(COMPANY, w, "save-learning", request_id="u1",
            data=learning_data(basis_refs=[c]))
        result = op.learning_command(COMPANY, w, "use-learning", request_id="u2",
            data={"learning_ref": learning["result_ref"], "book_ref": b, "title": "经验驱动新章",
                  "confirmed": True, "historical": False})
        new_chapter = result["chapter_ref"]
        assert new_chapter != c
        assert result["draft"]["text"].startswith("经验驱动新章")
        assert "第一章必须在三百字内给出异常物。" in result["draft"]["text"]
        assert "效果仍待验证" in result["draft"]["text"]
        # The new chapter exists in the package and its first draft matches.
        state = chapters.chapter(COMPANY, w, b, new_chapter)
        assert state["draft"]["ref"] == result["draft"]["ref"]
        assert state["draft"]["text"] == result["draft"]["text"]
        # Existing chapter head is untouched.
        after = chapters.chapter(COMPANY, w, b, c)
        assert after["draft"]["ref"] == before["draft"]["ref"]
        assert after["draft"]["text"] == before["draft"]["text"]
        # Link recorded.
        with db.connect() as con:
            link = con.execute("select count(*) from runtime_links where source_id=? and relation='WRITING_CHAPTER_FROM_LEARNING' and target_id=?",
                (new_chapter, learning["result_ref"])).fetchone()[0]
        assert link == 1
        # Idempotent replay returns the same chapter.
        replay = op.learning_command(COMPANY, w, "use-learning", request_id="u2",
            data={"learning_ref": learning["result_ref"], "book_ref": b, "title": "经验驱动新章",
                  "confirmed": True, "historical": False})
        assert replay["chapter_ref"] == new_chapter
        # Collection contains the new chapter under the book.
        collection = chapters.collection(COMPANY, w)
        assert any(ch["ref"] == new_chapter and ch["bookRef"] == b for ch in collection["chapters"])


def test_use_learning_requires_acceptance_current_version_and_book(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        pending = op.learning_command(COMPANY, w, "save-learning", request_id="p1", data=learning_data(accepted=False))
        with pytest.raises(ValueError):
            op.learning_command(COMPANY, w, "use-learning", request_id="p2",
                data={"learning_ref": pending["result_ref"], "book_ref": b, "title": "新章", "confirmed": True, "historical": False})
        first = op.learning_command(COMPANY, w, "save-learning", request_id="p3", expected_ref=pending["result_ref"],
            data=learning_data())
        second = op.learning_command(COMPANY, w, "save-learning", request_id="p4", expected_ref=first["result_ref"],
            data=learning_data(body="更新后的经验正文内容。"))
        with pytest.raises(WritingConflict):
            op.learning_command(COMPANY, w, "use-learning", request_id="p5",
                data={"learning_ref": first["result_ref"], "book_ref": b, "title": "新章", "confirmed": True, "historical": False})
        historical = op.learning_command(COMPANY, w, "use-learning", request_id="p6",
            data={"learning_ref": first["result_ref"], "book_ref": b, "title": "历史经验新章", "confirmed": True, "historical": True})
        assert "更新后的经验正文内容。" not in historical["draft"]["text"]
        with pytest.raises(RuntimeScopeError):
            op.learning_command(COMPANY, w, "use-learning", request_id="p7",
                data={"learning_ref": second["result_ref"], "book_ref": "missing-book", "title": "新章", "confirmed": True, "historical": False})
        with pytest.raises(ValueError):
            op.learning_command(COMPANY, w, "use-learning", request_id="p8",
                data={"learning_ref": second["result_ref"], "book_ref": b, "title": "  ", "confirmed": True, "historical": False})


def test_unknown_action_and_bad_fields_rejected(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        with pytest.raises(ValueError):
            op.direction_command(COMPANY, w, "save-snapshot", request_id="z1", data={})
        with pytest.raises(ValueError):
            op.learning_command(COMPANY, w, "save-learning", request_id="z2", data=learning_data(extra_field=1))


# ── isolation / persistence ──────────────────────────────────────────────

def test_cross_company_invisible_and_employee_cannot_write(tmp_path):
    db_a, _, w_a, b_a, c_a = setup(tmp_path / "a")
    db_b, w_b, b_b = setup_b(tmp_path / "b")
    with scope():
        op_a, _ = service(db_a)
        d = op_a.direction_command(COMPANY, w_a, "save-direction", request_id="o1", data=direction_data(reference_refs=[b_a]))
        l = op_a.learning_command(COMPANY, w_a, "save-learning", request_id="o2", data=learning_data())
    # Company B database cannot see A records (physical DB isolation);
    # same-DB cross-company attempt must fail scope resolution.
    with TenantScopeB():
        op_b, _ = service(db_b)
        with pytest.raises(RuntimeScopeError):
            op_b.direction_content(COMPANY, w_a, d["result_ref"])
        with pytest.raises(RuntimeScopeError):
            op_b.learning_command(COMPANY_B, w_b, "use-learning", request_id="o3",
                data={"learning_ref": l["result_ref"], "book_ref": b_b, "title": "越权", "confirmed": True, "historical": False})
    # Non-owner role cannot write.
    with scope(role="employee"):
        op, _ = service(db_a)
        with pytest.raises(RuntimeScopeError):
            op.direction_command(COMPANY, w_a, "save-direction", request_id="o4", data=direction_data())


def test_cold_restart_records_retain_unverified(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        d = op.direction_command(COMPANY, w, "save-direction", request_id="k1", data=direction_data())
        l = op.learning_command(COMPANY, w, "save-learning", request_id="k2", data=learning_data())
    cold_db = Database(db.path)
    with scope():
        cold_op, _ = service(cold_db)
        record = cold_op.direction_content(COMPANY, w, d["result_ref"])["record"]
        assert record["verification_status"] == "UNVERIFIED" and record["data"]["confirmed_by"] == CEO
        learning = cold_op.learning_content(COMPANY, w, l["result_ref"])["record"]
        assert learning["data"]["validation"] == "UNVERIFIED"
        assert len(cold_op.learnings_collection(COMPANY, w)["records"]) == 1
        assert len(cold_op.directions_collection(COMPANY, w)["records"]) == 1


# ── HTTP API smoke ───────────────────────────────────────────────────────

def test_api_operating_endpoints_mounted(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    chapters = WritingChapterService(db)
    operating = WritingOperatingService(db, chapter_service=chapters)
    application = FastAPI()

    @application.middleware("http")
    async def identity(request: Request, call_next):
        with scope(ceo_id=request.headers.get("X-Test-CEO", CEO)):
            return await call_next(request)

    async def forbidden(task):
        raise AssertionError("Real Provider is not authorized")

    application.include_router(build_writing_router(db, forbidden, service=chapters, operating=operating))
    root = f"/api/workspace/v1/companies/{COMPANY}/writing/{w}"
    with TestClient(application) as client:
        assert client.get(root + "/operating/directions").status_code == 200
        payload = {"request_id": "api1", "expected_ref": "", "data": direction_data()}
        saved = client.post(root + "/operating/directions/commands/save-direction", json=payload)
        assert saved.status_code == 200
        ref = saved.json()["result_ref"]
        assert client.get(root + "/operating/directions/" + ref).status_code == 200
        # Unknown action is rejected by the Literal whitelist.
        bad = client.post(root + "/operating/directions/commands/save-snapshot", json=payload)
        assert bad.status_code == 422
        # Cross identity 404.
        assert client.get(root + "/operating/directions", headers={"X-Test-CEO": "other"}).status_code == 404


def test_creation_source_projection_original_version_read_only_and_fail_closed(tmp_path):
    from backend.tests.test_writing_entry_readiness import database_values
    db, _, w, b, c = setup(tmp_path)
    with scope():
        operating, chapters = service(db)
        assert chapters.chapter(COMPANY, w, b, c)['creation_source'] == {'status': 'NONE'}
        saved = operating.learning_command(COMPANY, w, 'save-learning', request_id='source-original', data=learning_data())['record']
        created = operating.learning_command(COMPANY, w, 'use-learning', request_id='source-use', data={'learning_ref':saved['entity_id'],'book_ref':b,'title':'来源验收新章','confirmed':True,'historical':False})
        operating.learning_command(COMPANY, w, 'save-learning', request_id='source-revision', expected_ref=saved['entity_id'], data=learning_data(body='后来的经验版本'))
        before = database_values(db)
        read = chapters.chapter(COMPANY,w,b,created['chapter_ref'])
        assert read['creation_source']['status'] == 'AVAILABLE'
        assert read['creation_source']['learning_ref'] == saved['entity_id']
        assert read['creation_source']['revision'] == 1
        assert read['creation_source']['payload_sha256'] == saved['data']['payload_sha256']
        assert read['draft']['knowledge'] == []
        import os
        from pathlib import Path
        output = os.environ.get('CURIS_TEST_CREATION_SOURCE_OUTPUT')
        if output:
            Path(output).write_text(json.dumps({'chapter': read, 'source_record': saved},ensure_ascii=False,indent=2))
        assert database_values(db) == before
        with db.connect() as con:
            con.execute("insert into runtime_links(tenant_id,source_id,relation,target_id,created_at) values ('selfuse',?,'WRITING_CHAPTER_FROM_LEARNING','missing-target',current_timestamp)",(created['chapter_ref'],))
        before = database_values(db)
        assert chapters.chapter(COMPANY,w,b,created['chapter_ref'])['creation_source']['status'] == 'AMBIGUOUS'
        assert database_values(db) == before
        with db.connect() as con:
            con.execute("delete from runtime_links where source_id=? and target_id='missing-target'",(created['chapter_ref'],))
            con.execute("update runtime_entities set company_id='foreign' where entity_id=?",(saved['entity_id'],))
        before = database_values(db)
        assert chapters.chapter(COMPANY,w,b,created['chapter_ref'])['creation_source'] == {'status':'MISSING'}
        assert database_values(db) == before
