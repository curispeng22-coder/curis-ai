"""CG-REFERENCE-01 material library and CG-LEARNING-01 experience learning chain."""
import sqlite3
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from backend.tests.test_cg_content_entry import setup, data, create, COMPANY
from backend.tests.test_writing_chapter_vertical import scope


def test_materials_read_only_listing(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        result = s.materials(COMPANY, w)
        refs = {m["reference_id"] for m in result["materials"]}
        assert row["content"]["entity_id"] in refs
        assert row["version"]["entity_id"] in refs
        assert all(m["kind"] in {"WORK", "DECISION_PACKET", "CONTENT_ITEM", "CONTENT_VERSION"} for m in result["materials"])
        assert result["entry"]["scope"]["workspace_id"] == w
    with db.connect() as con:
        assert con.execute("select count(*) from runtime_entities where entity_type='PACKAGE_DOMAIN_OBJECT'").fetchone()[0] == 0


def learning_data(**overrides):
    value = {"title": "标题要具体", "body": "正文先给结论再给依据。", "basis_refs": [],
             "applicability": "图文开头", "counterexample": "数据不足时不套用", "accepted": True}
    value.update(overrides)
    return value


def save(service, w, request_id="save-1", expected_ref="", **overrides):
    return service.learning_command(COMPANY, w, "save-learning", request_id=request_id, expected_ref=expected_ref, data=learning_data(**overrides))


def test_learning_save_forces_unverified_and_basis_snapshot(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        basis_ref = row["version"]["entity_id"]
        result = save(s, w, basis_refs=[basis_ref])
        record = result["record"]
        assert record["verification_status"] == "UNVERIFIED"
        assert record["data"]["validation"] == "UNVERIFIED"
        assert record["data"]["revision"] == 1 and record["data"]["identity_ref"] == record["entity_id"]
        assert record["data"]["basis"] and all(len(h) == 64 for h in record["data"]["basis"].values())
        # Tamper with the basis content: read must fail closed.
        with db.connect() as con:
            con.execute("update runtime_entities set data_json=json_set(data_json,'$.body','被改动的正文') where entity_id=?", (basis_ref,))
        with pytest.raises(ValueError, match="原依据内容已改变"):
            s.learning_collection(COMPANY, w)


def test_learning_version_chain_and_historical_use(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        content_ref = row["content"]["entity_id"]
        latest_before = row["content"]["current_version_id"]
        first = save(s, w)["record"]
        second = save(s, w, request_id="save-2", expected_ref=first["entity_id"], body="修订后的经验正文。")["record"]
        assert second["data"]["revision"] == 2 and second["data"]["previous_ref"] == first["entity_id"]
        assert second["data"]["identity_ref"] == first["data"]["identity_ref"]
        # Non-latest application requires explicit historical confirmation.
        with pytest.raises(ContentGrowthConflict, match="原版本"):
            s.learning_command(COMPANY, w, "use-learning", request_id="use-1",
                               data={"learning_ref": first["entity_id"], "content_ref": content_ref, "confirmed": True, "historical": False})
        applied = s.learning_command(COMPANY, w, "use-learning", request_id="use-2",
                                     data={"learning_ref": first["entity_id"], "content_ref": content_ref, "confirmed": True, "historical": True})
        # Application must not replace the latest version pointer.
        after = s.content(COMPANY, w, content_ref)
        assert after["content"]["current_version_id"] == latest_before
        draft = next(v for v in after["versions"] if v["entity_id"] == applied["result_ref"])
        assert draft["data"]["learning_ref"] == first["entity_id"] and draft["data"]["kind"] == "draft"
        with db.connect() as con:
            link = con.execute("select relation from runtime_links where source_id=? and target_id=?",
                               (content_ref, first["entity_id"])).fetchone()
        assert link[0] == "CG_APPLIES_LEARNING"


def test_learning_command_idempotent_replay(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        content_ref = row["content"]["entity_id"]
        saved = save(s, w)
        again = save(s, w)  # same request_id + same payload replays
        assert again["result_ref"] == saved["result_ref"]
        with pytest.raises(ContentGrowthConflict, match="原请求不能改写"):
            save(s, w, title="不同的标题")
        use = {"learning_ref": saved["record"]["entity_id"], "content_ref": content_ref, "confirmed": True, "historical": False}
        applied = s.learning_command(COMPANY, w, "use-learning", request_id="use-1", data=use)
        replay = s.learning_command(COMPANY, w, "use-learning", request_id="use-1", data=use)
        assert replay["result_ref"] == applied["result_ref"]
        with db.connect() as con:
            versions = con.execute("select count(*) from runtime_entities where entity_type='CONTENT_VERSION'").fetchone()[0]
        assert versions == 2  # original head + one applied draft; replay created nothing


def test_learning_requires_acceptance_and_scope(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        unaccepted = save(s, w, request_id="save-u", accepted=False)["record"]
        assert unaccepted["data"]["accepted_by"] == ""
        with pytest.raises(ValueError, match="尚未明确接受"):
            s.learning_command(COMPANY, w, "use-learning", request_id="use-u",
                               data={"learning_ref": unaccepted["entity_id"], "content_ref": row["content"]["entity_id"], "confirmed": True, "historical": False})
        with pytest.raises((RuntimeScopeError, ValueError)):
            s.learning_command(COMPANY, w, "save-learning", request_id="save-x",
                               data=learning_data(basis_refs=["cg-learning-nonexistent"]))
        with pytest.raises((RuntimeScopeError, ValueError)):
            s.learning_collection("other-company", w)


def learning_state(db):
    with db.connect() as con:
        return {table: [tuple(row) for row in con.execute(f"select * from {table} order by rowid")]
                for table in ("runtime_entities", "runtime_links", "evolution_events")}


def test_repeat_learning_creates_distinct_drafts_preserving_heads_and_replays(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        content = row["content"]["entity_id"]
        learning = save(s, w)["record"]
        use = {"learning_ref": learning["entity_id"], "content_ref": content, "confirmed": True, "historical": False}
        first = s.learning_command(COMPANY, w, "use-learning", request_id="first-use", data=use)
        # A later manual head must supply the next draft, while the old draft stays immutable.
        current = s.command(COMPANY, w, content, "save", request_id="later-head",
                            expected_version_ref=row["version"]["entity_id"], data=data("后来人工保存的正文😀。"))
        before = learning_state(db)
        second = s.learning_command(COMPANY, w, "use-learning", request_id="second-use", data=use)
        assert first["result_ref"] != second["result_ref"]
        after = s.content(COMPANY, w, content)
        assert after["content"] == current["content"]
        assert after["version"] == current["version"]
        drafts = {v["entity_id"]: v for v in after["versions"]}
        assert drafts[first["result_ref"]]["data"]["body"] == row["version"]["data"]["body"]
        assert drafts[second["result_ref"]]["data"] == {
            **current["version"]["data"], "kind": "draft", "learning_ref": learning["entity_id"],
            "learning_body": learning["data"]["body"], "learning_applicability": learning["data"]["applicability"],
            "learning_counterexample": learning["data"]["counterexample"]}
        committed = learning_state(db)
        for table in before:
            assert committed[table][:len(before[table])] == before[table]
        for request, result in (("first-use", first), ("second-use", second)):
            assert s.learning_command(COMPANY, w, "use-learning", request_id=request, data=use) == result
        with pytest.raises(ContentGrowthConflict, match="原请求不能改写"):
            s.learning_command(COMPANY, w, "use-learning", request_id="second-use", data={**use, "historical": True})
        assert learning_state(db) == committed
        with db.connect() as con:
            assert con.execute("select count(*) from runtime_links where relation='CG_APPLIES_LEARNING'").fetchone()[0] == 1
            assert con.execute("select count(*) from evolution_events where event_type='cg.learning.use-learning'").fetchone()[0] == 2
            assert con.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert ContentGrowthService(Database(db.path)).content(COMPANY, w, content) == after


def test_repeat_learning_keeps_other_content_and_learning_pairs_distinct(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        c1 = create(s, w)["content"]["entity_id"]
        c2 = s.command(COMPANY, w, "", "create", request_id="other-content", data=data("另一篇正文"))["content"]["entity_id"]
        l1 = save(s, w)["result_ref"]
        l2 = save(s, w, request_id="other-learning", body="另一条经验")["result_ref"]
        pairs = [(c1, l1), (c1, l1), (c2, l1), (c1, l2)]
        results = []
        for i, (content, learning) in enumerate(pairs):
            result = s.learning_command(COMPANY, w, "use-learning", request_id=f"pair-{i}",
                data={"learning_ref": learning, "content_ref": content, "confirmed": True, "historical": False})
            results.append(result["result_ref"])
        assert len(set(results)) == 4
        with db.connect() as con:
            links = con.execute("select source_id,target_id from runtime_links where relation='CG_APPLIES_LEARNING'").fetchall()
            assert {tuple(link) for link in links} == set(pairs) and len(links) == 3


@pytest.mark.parametrize("identity", [{"tenant_id": "foreign"}, {"company_id": "foreign"}])
def test_repeat_learning_rejects_foreign_identity_without_writes(tmp_path, identity):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        content = create(s, w)["content"]["entity_id"]
        use = {"learning_ref": save(s, w)["result_ref"], "content_ref": content, "confirmed": True, "historical": False}
        s.learning_command(COMPANY, w, "use-learning", request_id="first-use", data=use)
    before = learning_state(db)
    with scope(**identity), pytest.raises(RuntimeScopeError):
        s.learning_command(COMPANY, w, "use-learning", request_id="foreign-repeat", data=use)
    assert learning_state(db) == before


def test_repeat_learning_rejects_cross_workspace_refs_without_writes(tmp_path):
    from app.content_growth_entry_service import ASSETS
    db, runtime, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        other = "other-workspace"
        package, target = runtime.prepare_confirmed_assets(ASSETS / "content_growth")
        with db.connect() as con:
            runtime.install_confirmed_in_connection(con, package, target, COMPANY, department_id="cg-dept",
                business_id="other-business", business_name="另一受控业务", business_goal="边界测试",
                business_positioning="合成夹具", workspace_id=other, workspace_name="另一工作区")
        c1 = create(s, w)["content"]["entity_id"]
        c2 = create(s, other)["content"]["entity_id"]
        l1 = save(s, w)["result_ref"]
        l2 = save(s, other)["result_ref"]
        s.learning_command(COMPANY, w, "use-learning", request_id="first-use",
            data={"learning_ref": l1, "content_ref": c1, "confirmed": True, "historical": False})
        before = learning_state(db)
        for i, (workspace, learning, content) in enumerate(((other, l1, c2), (w, l2, c1), (w, l1, c2))):
            with pytest.raises(RuntimeScopeError):
                s.learning_command(COMPANY, workspace, "use-learning", request_id=f"foreign-{i}",
                    data={"learning_ref": learning, "content_ref": content, "confirmed": True, "historical": False})
            assert learning_state(db) == before


@pytest.mark.parametrize("gate", ["confirmed", "historical", "accepted"])
def test_repeat_learning_preserves_confirmation_acceptance_and_history_gates(tmp_path, gate):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        content = create(s, w)["content"]["entity_id"]
        learning = save(s, w)["result_ref"]
        use = {"learning_ref": learning, "content_ref": content, "confirmed": True, "historical": False}
        s.learning_command(COMPANY, w, "use-learning", request_id="first-use", data=use)
        if gate == "confirmed":
            use["confirmed"] = False
        else:
            revised = save(s, w, request_id="revision", expected_ref=learning, accepted=gate != "accepted")
            if gate == "accepted":
                use["learning_ref"] = revised["result_ref"]
        before = learning_state(db)
        with pytest.raises(ValueError, match={"confirmed": "明确确认", "historical": "原版本", "accepted": "尚未明确接受"}[gate]):
            s.learning_command(COMPANY, w, "use-learning", request_id="blocked-repeat", data=use)
        assert learning_state(db) == before


@pytest.mark.parametrize("stage", ["link", "receipt"])
def test_repeat_learning_does_not_hide_other_errors_and_rolls_back(tmp_path, stage):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        content = create(s, w)["content"]["entity_id"]
        use = {"learning_ref": save(s, w)["result_ref"], "content_ref": content, "confirmed": True, "historical": False}
        s.learning_command(COMPANY, w, "use-learning", request_id="first-use", data=use)
        table, condition = ("runtime_links", "new.relation='CG_APPLIES_LEARNING'") if stage == "link" else (
            "evolution_events", "new.event_type='cg.learning.use-learning'")
        with db.connect() as con:
            con.execute(f"create trigger injected_failure before insert on {table} when {condition} "
                        "begin select raise(ABORT,'injected nonduplicate failure'); end")
        before = learning_state(db)
        with pytest.raises(sqlite3.IntegrityError, match="injected nonduplicate failure"):
            s.learning_command(COMPANY, w, "use-learning", request_id="failed-repeat", data=use)
        assert learning_state(db) == before
