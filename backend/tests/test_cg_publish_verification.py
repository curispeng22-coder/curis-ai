"""Platform chain S2: no-send publish verification records + D4 minimal local export.

Contract: docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md (Frozen §3/§4.2, D4).
Storage: runtime_entities PACKAGE_DOMAIN_OBJECT + objectType='PublishVerification' (same
reuse ruling as S1 Architecture Review). Zero new tables, zero outbound, no send/queue/schedule.
"""
import json
import hashlib
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.content_growth_service import (
    ContentGrowthService,
    ContentGrowthConflict,
    VERIFY_PLATFORM_CHECKS,
    VERIFY_COMMON_CHECKS,
)
from backend.tests.test_cg_content_entry import setup, COMPANY, data as content_data, create as create_content
from backend.tests.test_writing_chapter_vertical import scope
from backend.tests.test_cg_channel_accounts import account_data, create as create_account, add_second_workspace

ALL_PLATFORMS = ("xhs", "douyin", "wechat_oa", "tiktok", "youtube", "bilibili")


def checks_for(platform, *, checked=True, note_for=()):
    items = VERIFY_PLATFORM_CHECKS.get(platform, VERIFY_COMMON_CHECKS)
    return [{"key": key, "checked": checked, "note": ("已人工核对备注" if key in note_for else "")} for key, _ in items]


def verify(service, w, content_ref, account_ref, *, platform="xhs", request_id="v-1", checked=True, extra_checks=None):
    checks = checks_for(platform, checked=checked)
    if extra_checks is not None: checks = extra_checks
    return service.verification_create(COMPANY, w, request_id=request_id,
        data={"content_ref": content_ref, "account_ref": account_ref, "checks": checks})


@pytest.fixture
def world(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        content = create_content(s, w)["content"]["entity_id"]
        account = create_account(s, w)["entity_id"]
    return db, w, content, account


def test_templates_fixed_per_platform_and_invalid(tmp_path, world):
    db, w, _, _ = world
    with scope():
        s = ContentGrowthService(db)
        assert [c["key"] for c in s.verification_template(COMPANY, w, "xhs")["checks"]] == ["cover", "title_keywords", "tags_topics", "graphic_format"]
        assert [c["key"] for c in s.verification_template(COMPANY, w, "douyin")["checks"]] == ["cover_title", "duration_subtitles"]
        assert [c["key"] for c in s.verification_template(COMPANY, w, "wechat_oa")["checks"]] == ["layout", "title_summary_cover"]
        for platform in ("tiktok", "youtube", "bilibili"):
            result = s.verification_template(COMPANY, w, platform)
            assert [c["key"] for c in result["checks"]] == [k for k, _ in VERIFY_COMMON_CHECKS]
            assert result["name"]
        # Labels are present and non-empty on every spec.
        for platform in ALL_PLATFORMS:
            assert all(c["label"] for c in s.verification_template(COMPANY, w, platform)["checks"])
        for bad in ("weibo", "", "XHS", None, 123):
            with pytest.raises(ValueError):
                s.verification_template(COMPANY, w, bad)


def test_create_read_forced_truth_and_immutable_shape(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        out = verify(s, w, content_ref, account_ref)
        ref = out["result_ref"]
        assert ref.startswith("cg-verify-")
        record = out["record"]
        assert record["verification_status"] == "UNVERIFIED" and record["evidence_condition"] == "MISSING"
        d = record["data"]
        assert d["objectType"] == "PublishVerification"
        assert d["verification"] == "UNVERIFIED" and d["source"] == "CEO_MANUAL"
        assert d["connection_status"] == "NOT_CONNECTED"
        assert d["revision"] == 1 and d["identity_ref"] == ref and d["previous_ref"] == ""
        assert d["business_ref"] == "cg-business"
        assert d["content_ref"] == content_ref and d["content_workspace_id"] == w
        assert d["account_ref"] == account_ref and d["account_name"] == "小红书主号"
        assert d["platform_ref"] == "xhs" and d["platform_name"] == "小红书"
        assert d["content_title"] == "第一篇图文"
        assert [c["key"] for c in d["checks"]] == ["cover", "title_keywords", "tags_topics", "graphic_format"]
        assert all(c["checked"] is True and c["label"] for c in d["checks"])
        # Read-back and list.
        assert s.verification(COMPANY, w, ref)["data"]["content_title"] == "第一篇图文"
        assert [v["entity_id"] for v in s.verification_collection(COMPANY, w)["verifications"]] == [ref]
    with db.connect() as con:
        stored = json.loads(con.execute("select data_json from runtime_entities where entity_id=?", (ref,)).fetchone()[0])
        assert stored["verification"] == "UNVERIFIED" and stored["source"] == "CEO_MANUAL"
        links = {r[0] for r in con.execute("select relation from runtime_links where source_id=?", (ref,)).fetchall()}
        assert links == {"CG_VERIFY_ACCOUNT", "CG_VERIFY_CONTENT"}


def test_unchecked_items_allowed_but_every_item_required(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        checks = checks_for("xhs")
        checks[1]["checked"] = False  # a failed check is still an honest verification result
        out = s.verification_create(COMPANY, w, request_id="v-fail",
            data={"content_ref": content_ref, "account_ref": account_ref, "checks": checks})
        stored = out["record"]["data"]["checks"]
        assert stored[1]["checked"] is False and sum(c["checked"] for c in stored) == 3
        # Missing / extra / unknown keys.
        for bad in (checks[1:], checks + [{"key": "copyright", "checked": True}],
                    [{**c, "key": "nope"} if c["key"] == "cover" else c for c in checks]):
            with pytest.raises(ValueError):
                s.verification_create(COMPANY, w, request_id="v-bad-" + str(id(bad)),
                    data={"content_ref": content_ref, "account_ref": account_ref, "checks": bad})
        # checked must be bool; note bounded; no duplicate keys.
        for bad in ([{**c, "checked": "true"} for c in checks],
                    [{**c, "note": "x" * 2001} for c in checks],
                    checks[:3] + [{"key": "cover", "checked": True}]):
            with pytest.raises(ValueError):
                s.verification_create(COMPANY, w, request_id="v-bad2-" + str(id(bad)),
                    data={"content_ref": content_ref, "account_ref": account_ref, "checks": bad})


def test_client_label_and_truth_fields_cannot_be_forged(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        forged = [{**c, "label": "伪造检查项"} for c in checks_for("xhs")]
        out = verify(s, w, content_ref, account_ref, request_id="v-label", extra_checks=forged)
        # Server-owned labels win over client text.
        assert out["record"]["data"]["checks"][0]["label"] == "封面"
        # Top-level truth fields are rejected by exact() (unknown field).
        for field, value in (("verification", "VERIFIED"), ("source", "PLATFORM_API"),
                             ("connection_status", "CONNECTED")):
            with pytest.raises(ValueError):
                s.verification_create(COMPANY, w, request_id="v-truth-" + field,
                    data={"content_ref": content_ref, "account_ref": account_ref,
                          "checks": checks_for("xhs"), field: value})


def test_content_and_account_scope_404(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        # Missing content raises KeyError at entity lookup; router maps both to 404.
        with pytest.raises((RuntimeScopeError, KeyError)):
            verify(s, w, "content-item-missing", account_ref, request_id="v-m1")
        with pytest.raises(RuntimeScopeError):
            verify(s, w, content_ref, "cg-account-missing", request_id="v-m2")
    # Foreign tenant/company isolation.
    with scope(tenant_id="other", company_id="other-company", ceo_id="other"):
        s2 = ContentGrowthService(Database(db.path))
        with pytest.raises((RuntimeScopeError, ValueError)):
            s2.verification_collection("other-company", w)


def test_idempotent_replay_same_ref_conflict_on_fingerprint_change(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        first = verify(s, w, content_ref, account_ref, request_id="v-idem")
        again = verify(s, w, content_ref, account_ref, request_id="v-idem")
        assert again["result_ref"] == first["result_ref"]
        changed = checks_for("xhs"); changed[0]["checked"] = False
        with pytest.raises(ContentGrowthConflict):
            s.verification_create(COMPANY, w, request_id="v-idem",
                data={"content_ref": content_ref, "account_ref": account_ref, "checks": changed})


def test_snapshot_survives_later_content_change(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        ref = verify(s, w, content_ref, account_ref, request_id="v-snap")["result_ref"]
        # Content gets a new saved head after verification.
        s.command(COMPANY, w, content_ref, "save", request_id="save-after",
            expected_version_ref=s.content(COMPANY, w, content_ref)["version"]["entity_id"],
            data=content_data("改后的全新正文标题不变正文变"))
        record = s.verification(COMPANY, w, ref)["data"]
        assert record["content_title"] == "第一篇图文"
        assert "改后的全新正文" not in record["content_body"]
        assert record["content_body"] == "雨后😀，书桌上的信仍未打开。"


def test_export_shape_digest_and_filename(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        ref = verify(s, w, content_ref, account_ref, request_id="v-export")["result_ref"]
        raw, digest, filename = s.verification_export(COMPANY, w, ref)
        package = json.loads(raw)
        assert filename == f"cg-local-verification-{ref.replace('cg-verify-', '')[:8]}.json"
        assert digest == hashlib.sha256(raw).hexdigest()
        assert package["package_type"] == "curis.cg.local-verification-export/1"
        assert package["verification_ref"] == ref
        assert package["title"] == "第一篇图文" and package["body"]
        assert package["format"] == "graphic"
        assert package["platform"] == {"ref": "xhs", "name": "小红书"}
        assert package["account"]["ref"] == account_ref and package["account"]["name"] == "小红书主号"
        assert len(package["checks"]) == 4
        assert package["connection_status"] == "NOT_CONNECTED"
        assert package["verification"] == "UNVERIFIED" and package["source"] == "CEO_MANUAL"
        assert "不构成发布" in package["notice"]
        # Export is a read-only projection: no new entity/event.
        with db.connect() as con:
            assert con.execute("select count(*) from evolution_events where event_type='cg.verification.save'").fetchone()[0] == 1


def test_business_level_visibility_and_export_from_second_workspace(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope():
        s = ContentGrowthService(db)
        ref = verify(s, w, content_ref, account_ref, request_id="v-cross")["result_ref"]
        w2 = add_second_workspace(db, w)
        other = ContentGrowthService(db)
        seen = other.verification_collection(COMPANY, w2)["verifications"]
        assert [v["entity_id"] for v in seen] == [ref]
        assert seen[0]["workspace_id"] == w  # creating workspace retained as provenance
        raw, digest, filename = other.verification_export(COMPANY, w2, ref)
        assert json.loads(raw)["verification_ref"] == ref and digest and filename


def test_write_requires_owner_role(tmp_path, world):
    db, w, content_ref, account_ref = world
    with scope(role="employee"):
        with pytest.raises(RuntimeScopeError):
            verify(ContentGrowthService(db), w, content_ref, account_ref, request_id="v-emp")
    # Reads stay available.
    with scope():
        assert ContentGrowthService(db).verification_collection(COMPANY, w)["entry"]["scope"]["workspace_id"] == w


def test_nonprimary_platform_uses_common_compliance(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        account = create_account(s, w, platform_ref="youtube", name="YouTube 频道")["entity_id"]
        content = create_content(s, w)["content"]["entity_id"]
        out = verify(s, w, content, account, platform="youtube", request_id="v-yt")
        keys = [c["key"] for c in out["record"]["data"]["checks"]]
        assert keys == ["copyright", "compliance", "honesty"]
