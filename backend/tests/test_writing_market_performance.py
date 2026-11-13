"""WR-MARKET + WR-PERFORMANCE operating surfaces (P1-b).

Point-in-time immutable manual records, forced UNVERIFIED, idempotent,
workspace-scoped. Fixtures reuse the accepted writing vertical chain.
"""
import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.writing_router import build_writing_router
from app.database import Database
from app.runtime import RuntimeScopeError
from app.writing_chapter_service import WritingChapterService, WritingConflict
from app.writing_operating_service import WritingOperatingService
from backend.tests.test_writing_chapter_vertical import setup, scope, COMPANY, CEO
from backend.tests.test_writing_operating import service, setup_b, TenantScopeB, COMPANY_B


def snapshot_data(**overrides):
    base = {"title": "10 月悬疑题材市场快照", "body": "公开榜单显示短篇悬疑热度上升，编辑沟通反馈读者偏好强钩子开篇。",
        "period": "2026-10", "source_note": "人工观察公开榜单 + 编辑沟通记录（本地人工录入）"}
    base.update(overrides)
    return base


def observation_data(scope_ref, **overrides):
    base = {"title": "第一章首周人工观察", "body": "作者在读者群人工收集反馈：开场信件设定被频繁提及，节奏偏慢。",
        "scope_ref": scope_ref, "period": "2026-W40"}
    base.update(overrides)
    return base


# ── market snapshot ────────────────────────────────────────────────────────

def test_save_snapshot_forced_unverified_and_exact_fields(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        saved = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m1", data=snapshot_data())
        ref = saved["result_ref"]
        assert ref.startswith("wr-snapshot-")
        data = saved["record"]["data"]
        assert data["verification"] == "UNVERIFIED"
        assert data["revision"] == 1 and data["identity_ref"] == ref and data["previous_ref"] == ""
        assert saved["record"]["verification_status"] == "UNVERIFIED"
        assert data["source_note"].startswith("人工观察")
        # Client cannot declare verification; fields are exact.
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m2", data=snapshot_data(verification="VERIFIED"))
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m3", data=snapshot_data(extra=1))
        # source_note is mandatory.
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m4", data=snapshot_data(source_note="   "))
        # period is bounded but may be empty.
        ok = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m5", data=snapshot_data(period=""))
        assert ok["record"]["data"]["period"] == ""
        # title/body cannot be empty.
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m6", data=snapshot_data(title=""))
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="m7", data=snapshot_data(body=""))


def test_snapshot_is_immutable_append_only(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        first = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="i1", data=snapshot_data())
        # A snapshot is a point-in-time record; no revision path exists.
        with pytest.raises(ValueError):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="i2",
                expected_ref=first["result_ref"], data=snapshot_data())
        # A second save is a separate identity, not a revision.
        second = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="i3",
            data=snapshot_data(title="11 月市场快照"))
        assert second["result_ref"] != first["result_ref"]
        assert second["record"]["data"]["revision"] == 1
        records = op.snapshots_collection(COMPANY, w)["records"]
        assert {r["entity_id"] for r in records} == {first["result_ref"], second["result_ref"]}
        assert op.snapshot_content(COMPANY, w, first["result_ref"])["current_ref"] == first["result_ref"]


def test_snapshot_replay_same_fingerprint_diff_conflict(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        payload = snapshot_data()
        first = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="same", data=payload)
        replay = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="same", data=payload)
        assert replay == first
        with pytest.raises(WritingConflict):
            op.snapshot_command(COMPANY, w, "save-snapshot", request_id="same",
                data=snapshot_data(title="改了内容"))


def test_snapshot_tamper_detected_and_event_logged(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        saved = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="t1", data=snapshot_data())
        with db.connect() as con:
            row = con.execute("select data_json from runtime_entities where entity_id=?", (saved["result_ref"],)).fetchone()
            tampered = json.loads(row["data_json"]); tampered["body"] = "被篡改的正文"
            con.execute("update runtime_entities set data_json=? where entity_id=?",
                (json.dumps(tampered, ensure_ascii=False), saved["result_ref"]))
            events = con.execute("select event_type from evolution_events where idempotency_key like 'writing:snapshot:%'").fetchall()
        assert [r[0] for r in events] == ["writing.operating.save-snapshot"]
        with pytest.raises(ValueError):
            op.snapshot_content(COMPANY, w, saved["result_ref"])


# ── performance observation ────────────────────────────────────────────────

def test_observation_binds_book_or_chapter_in_workspace(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        on_book = op.observation_command(COMPANY, w, "save-observation", request_id="p1",
            data=observation_data(b))
        assert on_book["result_ref"].startswith("wr-observation-")
        assert on_book["record"]["data"]["scope_ref"] == b
        on_chapter = op.observation_command(COMPANY, w, "save-observation", request_id="p2",
            data=observation_data(c))
        assert on_chapter["record"]["data"]["scope_ref"] == c
        # Scope link written for each observation.
        with db.connect() as con:
            links = con.execute("select source_id, target_id from runtime_links where relation='WRITING_OBSERVATION_SCOPE'").fetchall()
        pairs = {(r[0], r[1]) for r in links}
        assert (on_book["result_ref"], b) in pairs and (on_chapter["result_ref"], c) in pairs
        # Empty / foreign scope fails closed.
        with pytest.raises(RuntimeScopeError):
            op.observation_command(COMPANY, w, "save-observation", request_id="p3",
                data=observation_data(""))
        with pytest.raises(RuntimeScopeError):
            op.observation_command(COMPANY, w, "save-observation", request_id="p4",
                data=observation_data("package-object-foreign"))


def test_observation_forced_unverified_exact_and_immutable(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        saved = op.observation_command(COMPANY, w, "save-observation", request_id="q1",
            data=observation_data(c))
        assert saved["record"]["data"]["verification"] == "UNVERIFIED"
        assert saved["record"]["verification_status"] == "UNVERIFIED"
        with pytest.raises(ValueError):
            op.observation_command(COMPANY, w, "save-observation", request_id="q2",
                data=observation_data(c, verification="VERIFIED"))
        with pytest.raises(ValueError):
            op.observation_command(COMPANY, w, "save-observation", request_id="q3",
                data=observation_data(c, source_note="不允许的字段"))
        with pytest.raises(ValueError):
            op.observation_command(COMPANY, w, "save-observation", request_id="q4",
                expected_ref=saved["result_ref"], data=observation_data(c))
        with pytest.raises(ValueError):
            op.observation_command(COMPANY, w, "save-observation", request_id="q5",
                data=observation_data(c, title=" ", body="正文"))
        replay = op.observation_command(COMPANY, w, "save-observation", request_id="q6",
            data=observation_data(c))
        assert replay["result_ref"] != saved["result_ref"]


def test_observation_collection_detail_and_idempotency(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        payload = observation_data(b)
        first = op.observation_command(COMPANY, w, "save-observation", request_id="same", data=payload)
        replay = op.observation_command(COMPANY, w, "save-observation", request_id="same", data=payload)
        assert replay == first
        with pytest.raises(WritingConflict):
            op.observation_command(COMPANY, w, "save-observation", request_id="same",
                data=observation_data(b, title="不同指纹"))
        records = op.observations_collection(COMPANY, w)["records"]
        assert len(records) == 1 and records[0]["entity_id"] == first["result_ref"]
        detail = op.observation_content(COMPANY, w, first["result_ref"])["record"]
        assert detail["data"]["period"] == "2026-W40"


# ── isolation / persistence ────────────────────────────────────────────────

def test_market_performance_cross_company_invisible(tmp_path):
    db_a, _, w_a, b_a, c_a = setup(tmp_path / "a")
    db_b, w_b, b_b = setup_b(tmp_path / "b")
    with scope():
        op_a, _ = service(db_a)
        s = op_a.snapshot_command(COMPANY, w_a, "save-snapshot", request_id="x1", data=snapshot_data())
        o = op_a.observation_command(COMPANY, w_a, "save-observation", request_id="x2",
            data=observation_data(b_a))
    with TenantScopeB():
        op_b, _ = service(db_b)
        with pytest.raises(RuntimeScopeError):
            op_b.snapshot_content(COMPANY, w_a, s["result_ref"])
        with pytest.raises(RuntimeScopeError):
            op_b.observations_collection(COMPANY, w_a)
        with pytest.raises(RuntimeScopeError):
            op_b.observation_command(COMPANY_B, w_b, "save-observation", request_id="x3",
                data=observation_data(o["result_ref"]))
        assert len(op_b.snapshots_collection(COMPANY_B, w_b)["records"]) == 0
    # Employee role cannot write.
    with scope(role="employee"):
        op, _ = service(db_a)
        with pytest.raises(RuntimeScopeError):
            op.snapshot_command(COMPANY, w_a, "save-snapshot", request_id="x4", data=snapshot_data())


def test_market_performance_cold_restart_retains_unverified(tmp_path):
    db, _, w, b, c = setup(tmp_path)
    with scope():
        op, _ = service(db)
        s = op.snapshot_command(COMPANY, w, "save-snapshot", request_id="k1", data=snapshot_data())
        o = op.observation_command(COMPANY, w, "save-observation", request_id="k2",
            data=observation_data(c))
    cold_op, _ = service(Database(db.path))
    with scope():
        snap = cold_op.snapshot_content(COMPANY, w, s["result_ref"])["record"]
        obs = cold_op.observation_content(COMPANY, w, o["result_ref"])["record"]
        assert snap["data"]["verification"] == "UNVERIFIED"
        assert obs["data"]["verification"] == "UNVERIFIED" and obs["data"]["scope_ref"] == c
        assert len(cold_op.snapshots_collection(COMPANY, w)["records"]) == 1
        assert len(cold_op.observations_collection(COMPANY, w)["records"]) == 1


# ── HTTP API smoke ─────────────────────────────────────────────────────────

def test_api_market_performance_endpoints_mounted(tmp_path):
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
        assert client.get(root + "/operating/snapshots").status_code == 200
        sp = {"request_id": "api1", "expected_ref": "", "data": snapshot_data()}
        saved = client.post(root + "/operating/snapshots/commands/save-snapshot", json=sp)
        assert saved.status_code == 200
        sref = saved.json()["result_ref"]
        assert client.get(root + "/operating/snapshots/" + sref).status_code == 200
        op_ = {"request_id": "api2", "expected_ref": "", "data": observation_data(b)}
        obsaved = client.post(root + "/operating/observations/commands/save-observation", json=op_)
        assert obsaved.status_code == 200
        oref = obsaved.json()["result_ref"]
        assert client.get(root + "/operating/observations/" + oref).status_code == 200
        # Action whitelist per command group.
        assert client.post(root + "/operating/snapshots/commands/save-observation", json=op_).status_code == 422
        assert client.post(root + "/operating/observations/commands/save-snapshot", json=sp).status_code == 422
        # Bad payload (missing source_note) maps to 422; foreign scope maps to 404.
        bad = {"request_id": "api3", "data": {"title": "t", "body": "b", "period": "", "source_note": ""}}
        assert client.post(root + "/operating/snapshots/commands/save-snapshot", json=bad).status_code == 422
        foreign = {"request_id": "api4", "data": observation_data("package-object-x")}
        assert client.post(root + "/operating/observations/commands/save-observation", json=foreign).status_code == 404
        # Cross identity 404.
        assert client.get(root + "/operating/snapshots", headers={"X-Test-CEO": "other"}).status_code == 404
