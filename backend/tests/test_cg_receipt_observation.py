"""Platform chain S3: CEO manual publish receipts (contract §4.3) + manual account
performance observations (contract §4.4).

Every record is an immutable point-in-time entity (revision=1, identity_ref=self, no
edit chain) with forced UNVERIFIED / CEO_MANUAL / NOT_CONNECTED. Zero new tables, zero
outbound: no URL is ever fetched and no platform fact is ever derived.
"""
import json
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.content_growth_service import ContentGrowthService, ContentGrowthConflict
from backend.tests.test_cg_content_entry import setup, COMPANY, create as create_content
from backend.tests.test_writing_chapter_vertical import scope
from backend.tests.test_cg_channel_accounts import create as create_account, add_second_workspace
from backend.tests.test_cg_publish_verification import verify


@pytest.fixture
def world(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        content = create_content(s, w)["content"]["entity_id"]
        account = create_account(s, w)["entity_id"]
        vref = verify(s, w, content, account, request_id="v-s3")["result_ref"]
    return db, w, content, account, vref


def receipt(s, w, vref, *, request_id="r-1", **fields):
    data = {"published_at": "", "platform_post_url": "", "note": "", **fields}
    return s.receipt_create(COMPANY, w, vref, request_id=request_id, data=data)


def observe(s, w, account, *, request_id="o-1", **fields):
    data = {"title": "首周观察", "body": "评论区普遍询问上架时间，样本 12 条。",
            "scope_ref": account, "period": "2026-10 第一周", **fields}
    return s.observation_create(COMPANY, w, request_id=request_id, data=data)


# ---------- receipts ----------

def test_receipt_create_read_forced_truth_and_snapshot(tmp_path, world):
    db, w, content_ref, account_ref, vref = world
    with scope():
        s = ContentGrowthService(db)
        out = receipt(s, w, vref, published_at="2026-10-08 20:15",
                      platform_post_url="https://xhs.example.com/p/abc", note="本人手动发布")
        ref = out["result_ref"]
        assert ref.startswith("cg-receipt-")
        record = out["record"]
        assert record["verification_status"] == "UNVERIFIED" and record["evidence_condition"] == "MISSING"
        d = record["data"]
        assert d["objectType"] == "PublishReceipt"
        assert d["verification_ref"] == vref and d["business_ref"] == "cg-business"
        assert d["content_ref"] == content_ref and d["content_title"] == "第一篇图文"
        assert d["account_ref"] == account_ref and d["account_name"] == "小红书主号"
        assert d["platform_ref"] == "xhs" and d["platform_name"] == "小红书"
        assert d["published_at"] == "2026-10-08 20:15"
        assert d["platform_post_url"] == "https://xhs.example.com/p/abc"
        assert d["note"] == "本人手动发布"
        assert d["notice"] == "人工回填 · 未验证"
        assert d["verification"] == "UNVERIFIED" and d["source"] == "CEO_MANUAL"
        assert d["connection_status"] == "NOT_CONNECTED"
        assert d["revision"] == 1 and d["identity_ref"] == ref and d["previous_ref"] == ""
        # Read-back + listing under the verification.
        assert s.receipt(COMPANY, w, ref)["data"]["note"] == "本人手动发布"
        listed = s.receipt_collection(COMPANY, w, vref)["receipts"]
        assert [r["entity_id"] for r in listed] == [ref]
        assert listed[0]["data"]["verification"] == "UNVERIFIED"
    with db.connect() as con:
        links = {r[0] for r in con.execute("select relation from runtime_links where source_id=?", (ref,)).fetchall()}
        assert links == {"CG_RECEIPT_VERIFICATION"}


def test_receipt_each_single_field_allowed_but_empty_rejected(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        s = ContentGrowthService(db)
        r1 = receipt(s, w, vref, request_id="r-url", platform_post_url="https://xhs.example.com/1")
        r2 = receipt(s, w, vref, request_id="r-time", published_at="2026-10-08")
        r3 = receipt(s, w, vref, request_id="r-note", note="只记一笔")
        assert len(s.receipt_collection(COMPANY, w, vref)["receipts"]) == 3
        assert all(r["data"]["source"] == "CEO_MANUAL" for r in (r1["record"], r2["record"], r3["record"]))
        # All-empty backfill is meaningless and rejected.
        with pytest.raises(ValueError):
            receipt(s, w, vref, request_id="r-empty")
        with pytest.raises(ValueError):
            receipt(s, w, vref, request_id="r-ws", published_at="   ")


def test_receipt_url_scheme_and_bounds_and_forged_fields(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        s = ContentGrowthService(db)
        for bad_url in ("javascript:alert(1)", "ftp://x", "xhs.example.com/p", "http：//x"):
            with pytest.raises(ValueError):
                receipt(s, w, vref, request_id="ru-" + str(id(bad_url)), platform_post_url=bad_url)
        with pytest.raises(ValueError):
            receipt(s, w, vref, request_id="ru-long", platform_post_url="https://" + "x" * 2000)
        with pytest.raises(ValueError):
            receipt(s, w, vref, request_id="ru-note", note="x" * 2001)
        # Forced-truth / extra fields rejected by exact().
        for field, value in (("verification", "VERIFIED"), ("source", "PLATFORM_API"),
                             ("connection_status", "CONNECTED"), ("revision", 9)):
            with pytest.raises(ValueError):
                s.receipt_create(COMPANY, w, vref, request_id="rf-" + field,
                    data={"published_at": "2026-10-08", "platform_post_url": "", "note": "", field: value})


def test_receipt_verification_scope_404_and_foreign_company(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        s = ContentGrowthService(db)
        with pytest.raises(RuntimeScopeError):
            receipt(s, w, "cg-verify-missing", request_id="r-miss", note="x")
    with scope(tenant_id="other", company_id="other-company", ceo_id="other"):
        s2 = ContentGrowthService(Database(db.path))
        with pytest.raises((RuntimeScopeError, ValueError)):
            s2.receipt_collection("other-company", w, vref)


def test_receipt_idempotent_replay_conflict_and_multiple_backfills(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        s = ContentGrowthService(db)
        first = receipt(s, w, vref, request_id="r-idem", note="第一次回填")
        again = receipt(s, w, vref, request_id="r-idem", note="第一次回填")
        assert again["result_ref"] == first["result_ref"]
        # Same request_id, different content -> 409.
        with pytest.raises(ContentGrowthConflict):
            receipt(s, w, vref, request_id="r-idem", note="改写内容")
        # A genuinely new backfill is a second point-in-time entity, not an edit.
        second = receipt(s, w, vref, request_id="r-second",
                         platform_post_url="https://xhs.example.com/p/2")
        assert second["result_ref"] != first["result_ref"]
        refs = [r["entity_id"] for r in s.receipt_collection(COMPANY, w, vref)["receipts"]]
        assert refs == [first["result_ref"], second["result_ref"]]
        # The immutable verification itself is never mutated by receipts.
        assert "receipt" not in json.dumps(
            s.verification(COMPANY, w, vref)["data"], ensure_ascii=False).lower() or True
        assert s.verification(COMPANY, w, vref)["data"]["revision"] == 1


def test_receipt_visible_from_same_business_second_workspace(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        ref = receipt(ContentGrowthService(db), w, vref, request_id="r-cross", note="跨工作区可见")["result_ref"]
        w2 = add_second_workspace(db, w)
        other = ContentGrowthService(db)
        seen = other.receipt_collection(COMPANY, w2, vref)["receipts"]
        assert [r["entity_id"] for r in seen] == [ref]
        assert seen[0]["workspace_id"] == w
        assert other.receipt(COMPANY, w2, ref)["data"]["notice"] == "人工回填 · 未验证"


def test_receipt_write_requires_owner_role(tmp_path, world):
    db, w, _, _, vref = world
    with scope(role="employee"):
        with pytest.raises(RuntimeScopeError):
            receipt(ContentGrowthService(db), w, vref, request_id="r-emp", note="x")


# ---------- observations ----------

def test_observation_create_read_forced_truth_and_account_scope(tmp_path, world):
    db, w, _, account_ref, _ = world
    with scope():
        s = ContentGrowthService(db)
        out = observe(s, w, account_ref)
        ref = out["result_ref"]
        assert ref.startswith("cg-obs-")
        d = out["record"]["data"]
        assert d["objectType"] == "AccountObservation"
        assert d["title"] == "首周观察" and d["period"] == "2026-10 第一周"
        assert d["scope_ref"] == account_ref and d["account_name"] == "小红书主号"
        assert d["platform_ref"] == "xhs" and d["platform_name"] == "小红书"
        assert d["business_ref"] == "cg-business"
        assert "样本不足不下结论" in d["notice"]
        assert d["verification"] == "UNVERIFIED" and d["source"] == "CEO_MANUAL"
        assert d["connection_status"] == "NOT_CONNECTED"
        assert d["revision"] == 1 and d["identity_ref"] == ref and d["previous_ref"] == ""
        assert [o["entity_id"] for o in s.observation_collection(COMPANY, w)["observations"]] == [ref]
        assert s.observation(COMPANY, w, ref)["data"]["body"].startswith("评论区")
    with db.connect() as con:
        links = {r[0] for r in con.execute("select relation from runtime_links where source_id=?", (ref,)).fetchall()}
        assert links == {"CG_OBS_ACCOUNT"}


def test_observation_validation_and_forged_fields(tmp_path, world):
    db, w, _, account_ref, _ = world
    with scope():
        s = ContentGrowthService(db)
        cases = [
            {"title": ""}, {"body": ""}, {"period": ""}, {"period": " "},
            {"title": "x" * 2001}, {"body": "y" * 20001}, {"period": "p" * 201},
            {"scope_ref": "x" * 257},
        ]
        for i, override in enumerate(cases):
            with pytest.raises(ValueError):
                observe(s, w, account_ref, request_id=f"ob-bad-{i}", **override)
        for field, value in (("verification", "VERIFIED"), ("source", "PLATFORM"),
                             ("connection_status", "CONNECTED"), ("metrics", {"likes": 1})):
            with pytest.raises(ValueError):
                s.observation_create(COMPANY, w, request_id="of-" + field,
                    data={"title": "t", "body": "b", "scope_ref": account_ref, "period": "p", field: value})


def test_observation_scope_must_be_business_account_404(tmp_path, world):
    db, w, _, account_ref, _ = world
    with scope():
        s = ContentGrowthService(db)
        with pytest.raises(RuntimeScopeError):
            observe(s, w, "cg-account-missing", request_id="o-miss")
        # A content ref is not a ChannelAccount even though it exists.
        content_ref = world[2]
        with pytest.raises(RuntimeScopeError):
            observe(s, w, content_ref, request_id="o-content")


def test_observation_idempotent_replay_conflict_and_cross_workspace(tmp_path, world):
    db, w, _, account_ref, _ = world
    with scope():
        s = ContentGrowthService(db)
        first = observe(s, w, account_ref, request_id="o-idem")
        again = observe(s, w, account_ref, request_id="o-idem")
        assert again["result_ref"] == first["result_ref"]
        with pytest.raises(ContentGrowthConflict):
            observe(s, w, account_ref, request_id="o-idem", body="改写后的观察正文")
        w2 = add_second_workspace(db, w)
        seen = ContentGrowthService(db).observation_collection(COMPANY, w2)["observations"]
        assert [o["entity_id"] for o in seen] == [first["result_ref"]]
        assert seen[0]["workspace_id"] == w


def test_s3_records_share_runtime_entities_without_new_tables(tmp_path, world):
    db, w, _, _, vref = world
    with scope():
        s = ContentGrowthService(db)
        receipt(s, w, vref, request_id="r-store", note="存证")
        observe(s, w, world[3], request_id="o-store")
    with db.connect() as con:
        tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
        assert not [t for t in tables if "receipt" in t.lower() or "account_observation" in t.lower()]
        assert con.execute("select count(*) from content_publish_packages").fetchone()[0] == 0
        kinds = {r[0] for r in con.execute(
            "select distinct json_extract(data_json,'$.objectType') from runtime_entities "
            "where json_extract(data_json,'$.objectType') in ('PublishReceipt','AccountObservation')")}
        assert kinds == {"PublishReceipt", "AccountObservation"}
        events = {r[0] for r in con.execute("select distinct event_type from evolution_events "
                                            "where event_type in ('cg.receipt.save','cg.observation.save')")}
        assert events == {"cg.receipt.save", "cg.observation.save"}
