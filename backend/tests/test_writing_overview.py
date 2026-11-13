"""WR-OP-01 read-only operating projection (P1-c).

Aggregates existing workspace objects only: no writes, no new tables,
honest per-block emptiness. Fixtures reuse the accepted writing chain.
"""
import time

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.writing_router import build_writing_router
from app.database import Database
from app.runtime import RuntimeScopeError
from app.writing_chapter_service import WritingChapterService
from app.writing_operating_service import WritingOperatingService
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO
from backend.tests.test_writing_operating import (
    service, setup_b, TenantScopeB, COMPANY_B, direction_data, learning_data)
from backend.tests.test_writing_market_performance import snapshot_data, observation_data


def table_counts(db):
    with db.connect() as con:
        return {
            "entities": con.execute("select count(*) from runtime_entities").fetchone()[0],
            "links": con.execute("select count(*) from runtime_links").fetchone()[0],
            "events": con.execute("select count(*) from evolution_events").fetchone()[0],
        }


def test_overview_empty_workspace_all_blocks_empty(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        view = op.operating_overview(COMPANY, w)
    assert set(view) == {"entry", "books", "chapters", "directions", "learnings", "snapshots", "observations"}
    assert view["books"] and view["chapters"]  # vertical seed installs one book + one chapter
    assert view["directions"] == {"total_versions": 0, "current": []}
    assert view["learnings"] == {"total_versions": 0, "current": []}
    assert view["snapshots"] == {"total": 0, "latest": []}
    assert view["observations"] == {"total": 0, "latest": []}
    assert view["entry"]["read_only"] is False


def test_overview_books_chapters_and_draft_truth(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, chapters = service(db)
        before = op.operating_overview(COMPANY, w)
        seeded_chapter = next(ch for ch in before["chapters"] if ch["ref"] == c)
        assert seeded_chapter["has_draft"] is False
        assert seeded_chapter["book_ref"] == b
        book = next(x for x in before["books"] if x["ref"] == b)
        assert book["chapter_count"] == 1
        # Saving a draft flips the projection truth; projection itself writes nothing.
        chapters.command(COMPANY, w, b, c, "draft.saved", "ov-draft-1", "ABSENT",
                         {"text": "投影面应读到这版草稿存在。", "knowledge": []})
        after = op.operating_overview(COMPANY, w)
        flipped = next(ch for ch in after["chapters"] if ch["ref"] == c)
        assert flipped["has_draft"] is True
        assert next(x for x in after["books"] if x["ref"] == b)["chapter_count"] == 1


def test_overview_directions_keep_only_current_revision_with_truth(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        first = op.direction_command(COMPANY, w, "save-direction", request_id="ovd1",
            data=direction_data(confirmed=False))
        second = op.direction_command(COMPANY, w, "save-direction", request_id="ovd2",
            expected_ref=first["result_ref"], data=direction_data())
        # A second identity at workspace scope.
        other = op.direction_command(COMPANY, w, "save-direction", request_id="ovd3",
            data=direction_data(title="工作区级方向", scope_ref="", confirmed=False))
        view = op.operating_overview(COMPANY, w)
        assert view["directions"]["total_versions"] == 3
        current = view["directions"]["current"]
        assert len(current) == 2
        revised = next(x for x in current if x["ref"] == second["result_ref"])
        assert revised["revision"] == 2 and revised["confirmed"] is True
        assert first["result_ref"] not in {x["ref"] for x in current}
        pending = next(x for x in current if x["ref"] == other["result_ref"])
        assert pending["confirmed"] is False and pending["scope_ref"] == ""


def test_overview_learnings_current_with_acceptance_truth(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        pending = op.learning_command(COMPANY, w, "save-learning", request_id="ovl1",
            data=learning_data(accepted=False))
        accepted = op.learning_command(COMPANY, w, "save-learning", request_id="ovl2",
            expected_ref=pending["result_ref"], data=learning_data())
        view = op.operating_overview(COMPANY, w)
        assert view["learnings"]["total_versions"] == 2
        current = view["learnings"]["current"]
        assert len(current) == 1 and current[0]["ref"] == accepted["result_ref"]
        assert current[0]["accepted"] is True and current[0]["revision"] == 2
        assert current[0]["applicability"] == "悬疑类长篇开篇"


def test_overview_snapshots_and_observations_latest_three(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        titles = []
        for i in range(4):
            titles.append(f"QA快照{i+1}")
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id=f"ovs{i+1}",
                data=snapshot_data(title=titles[-1], period=f"2026-10-0{i+1}"))
            time.sleep(0.01)
        op.observation_command(COMPANY, w, "save-observation", request_id="ovo1",
            data=observation_data(b, title="QA作品观察"))
        op.observation_command(COMPANY, w, "save-observation", request_id="ovo2",
            data=observation_data(c, title="QA章节观察"))
        view = op.operating_overview(COMPANY, w)
        assert view["snapshots"]["total"] == 4
        latest_titles = [x["title"] for x in view["snapshots"]["latest"]]
        assert latest_titles == ["QA快照4", "QA快照3", "QA快照2"]
        assert all(x["ref"].startswith("wr-snapshot-") for x in view["snapshots"]["latest"])
        assert view["observations"]["total"] == 2
        scopes = {x["title"]: x["scope_ref"] for x in view["observations"]["latest"]}
        assert scopes == {"QA作品观察": b, "QA章节观察": c}


def test_overview_is_strictly_read_only(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        op.direction_command(COMPANY, w, "save-direction", request_id="seed1", data=direction_data())
        op.snapshot_command(COMPANY, w, "save-snapshot", request_id="seed2", data=snapshot_data())
        op.observation_command(COMPANY, w, "save-observation", request_id="seed3",
            data=observation_data(b))
        before = table_counts(db)
        for _ in range(3):
            op.operating_overview(COMPANY, w)
        assert table_counts(db) == before


def test_overview_cross_company_invisible_but_employee_can_read(tmp_path):
    db_a, _, w_a, b_a, c_a = setup(tmp_path / "a")
    db_b, w_b, b_b = setup_b(tmp_path / "b")
    with scope():
        op_a, _ = service(db_a)
        op_a.snapshot_command(COMPANY, w_a, "save-snapshot", request_id="o1", data=snapshot_data())
    with TenantScopeB():
        op_b, _ = service(db_b)
        with pytest.raises(RuntimeScopeError):
            op_b.operating_overview(COMPANY, w_a)
        empty_b = op_b.operating_overview(COMPANY_B, w_b)
        assert empty_b["snapshots"]["total"] == 0 and len(empty_b["books"]) == 1
    # Projection is read-only: employee role may read (write gates stay on command paths).
    with scope(role="employee"):
        op, _ = service(db_a)
        view = op.operating_overview(COMPANY, w_a)
        assert view["snapshots"]["total"] == 1
        with pytest.raises(RuntimeScopeError):
            op.snapshot_command(COMPANY, w_a, "save-snapshot", request_id="o2", data=snapshot_data())


def test_overview_cold_restart(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        op.direction_command(COMPANY, w, "save-direction", request_id="k1", data=direction_data())
        op.snapshot_command(COMPANY, w, "save-snapshot", request_id="k2", data=snapshot_data())
        op.observation_command(COMPANY, w, "save-observation", request_id="k3",
            data=observation_data(c))
    cold_op, _ = service(Database(db.path))
    with scope():
        view = cold_op.operating_overview(COMPANY, w)
        assert view["directions"]["total_versions"] == 1
        assert view["snapshots"]["total"] == 1 and view["observations"]["total"] == 1
        assert view["chapters"] and view["books"]


def test_api_overview_endpoint_read_only_mounted(tmp_path):
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
        ok = client.get(root + "/operating/overview")
        assert ok.status_code == 200
        assert set(ok.json()) == {"entry", "books", "chapters", "directions", "learnings",
                                 "snapshots", "observations"}
        # Projection is GET-only; no command route exists under /overview.
        assert client.post(root + "/operating/overview", json={}).status_code == 405
        # Cross identity 404.
        assert client.get(root + "/operating/overview", headers={"X-Test-CEO": "other"}).status_code == 404
