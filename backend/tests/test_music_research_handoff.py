from concurrent.futures import ThreadPoolExecutor

import pytest

from app.api import music_research_handoff as handoff
from app.conversation_service import ConversationService
from app.database import Database
from app.music_service import MusicService
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.runtime.music import MusicConflict
from backend.tests.test_music_canonical_entry import setup
from backend.tests.test_music_operating_chain import chain, op
from backend.tests.test_writing_chapter_vertical import COMPANY, scope


def test_confirm_planning_creates_one_version_bound_work_after_admitted_delivery(tmp_path, monkeypatch):
    db, _, workspace, music = setup(tmp_path)
    with scope():
        _, _, _, direction = chain(music, workspace)
        assignment, = music.entry.authoring_scope(COMPANY, workspace)["assignments"]
        delivery = {"work_ref": "admitted-research-work", "conversation_ref": "original-conversation",
                    "evidence_ref": "admitted-evidence", "evidence_version": "1" * 64,
                    "summary_result_ref": "summary-result", "summary_result_version": "3" * 64}

        # Evidence admission is exercised separately from planning writes.
        def admitted(service, con, company, workspace, **refs):
            return (ConversationService(service.db)._work_database(con),
                    service._operating_entry(company, workspace, connection=con), delivery)

        monkeypatch.setattr(handoff, "_delivery", admitted)
        fields = {"evidence_version": delivery["evidence_version"], "summary_result_ref": "summary-result", "summary_result_version": "3" * 64, "direction_ref": direction["entity_id"],
                  "assignment_ref": assignment["assignment_ref"]}
        with pytest.raises(MusicConflict, match="证据版本"):
            handoff.confirm_research_planning(music, COMPANY, workspace, **{**fields, "evidence_version": "2" * 64})
        with pytest.raises(MusicConflict, match="汇总版本"):
            handoff.confirm_research_planning(music, COMPANY, workspace, **{**fields, "summary_result_version": "4" * 64})
        with scope(role="employee"), pytest.raises(RuntimeScopeError, match="所有者"):
            handoff.confirm_research_planning(music, COMPANY, workspace, **fields)

        def confirm(_):
            with scope():
                return handoff.confirm_research_planning(music, COMPANY, workspace, **fields)

        with ThreadPoolExecutor(max_workers=3) as pool:
            owner, *duplicates = pool.map(confirm, range(3))
        assert duplicates == [owner, owner]
        reopened = MusicService(Database(db.path))
        delivery.update(metrics=[{"label": "公开指标"}], limitations="适用范围待核对", recommendation={"evidence": []})
        replay = handoff.confirm_research_planning(reopened, COMPANY, workspace, **fields)
        work = owner["work"]
        assert replay["work"] == work
        assert work["workspace_id"] == workspace and work["lifecycle_status"] == "PLANNED"
        assert work["data"]["responsibilityAssignmentRef"] == assignment["assignment_ref"]
        source = replay["cycle"]["data"]["contract"]["musicResearchSource"]
        assert source["direction_ref"] == direction["entity_id"] and source["evidence_ref"] == delivery["evidence_ref"]
        assert source["direction_version"] == direction["data"]["payload_sha256"]

        revised = {key: direction["data"][key] for key in ("title", "body", "scope_ref", "reference_refs", "learning_ref")}
        op(music, workspace, "save-direction", {**revised, "confirmed": True}, "revision", direction["entity_id"])
        with pytest.raises(MusicConflict, match="当前歌曲方向"):
            handoff.confirm_research_planning(reopened, COMPANY, workspace, **fields)
        count = len(RuntimeFoundation(db).list("WORK", company_id=COMPANY))
        assert count == 1
