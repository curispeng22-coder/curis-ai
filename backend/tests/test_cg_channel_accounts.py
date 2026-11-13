"""Platform chain S1: ChannelAccount local CRUD, fixed catalog, honest NOT_CONNECTED.

Contract: docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md (Frozen, D1/D2).
Storage: runtime_entities PACKAGE_DOMAIN_OBJECT + objectType='ChannelAccount' (Architecture
Review CURIS_CHANNEL_ACCOUNT_STORAGE_ARCHITECTURE_REVIEW). Zero new tables, zero outbound.
"""
import pytest
from app.database import Database
from app.runtime import RuntimeScopeError
from app.content_growth_service import (
    ContentGrowthService,
    PLATFORM_CATALOG,
    ACCOUNT_GROWTH_STAGES,
    ACCOUNT_STATUS,
    ACCOUNT_CONNECTION_STATUS,
)
from backend.tests.test_cg_content_entry import setup, COMPANY
from backend.tests.test_writing_chapter_vertical import scope

ACCOUNT_REF_FIELDS = ("name", "positioning", "audience", "content_mix", "cadence", "voice", "growth_stage", "responsibility", "status")


def account_data(**overrides):
    value = {"platform_ref": "xhs", "name": "小红书主号", "positioning": "文学读者面对面的原创故事",
             "audience": "20-35 岁都市读者", "content_mix": "故事 7 : 幕后 3", "cadence": "每周三更",
             "voice": "克制、具体", "growth_stage": "cold_start", "responsibility": "CEO 直担", "status": "active"}
    value.update(overrides)
    return value


def edit_data(**overrides):
    return {key: value for key, value in account_data(**overrides).items() if key != "platform_ref"}


def create(service, w, request_id="acc-1", **overrides):
    return service.account_create(COMPANY, w, data=account_data(**overrides))


def add_second_workspace(db, w):
    """Same business, second CG workspace (install is idempotent per business)."""
    w2 = "workspace-package-second"
    with db.connect() as con:
        con.execute("insert into workspaces(workspace_id,tenant_id,company_id,business_id,name,blueprint_json,blueprint_version,operating_version,status,"
            "business_relation_status,business_relation_reason,business_relation_owner,business_relation_source,business_relation_checked_at,"
            "simulation_passed,issues_resolved,external_agent_reviewed,created_at,updated_at) "
            "select ?,tenant_id,company_id,business_id,name||' 二',blueprint_json,blueprint_version,operating_version,status,"
            "business_relation_status,business_relation_reason,business_relation_owner,business_relation_source,business_relation_checked_at,"
            "simulation_passed,issues_resolved,external_agent_reviewed,created_at,updated_at from workspaces where workspace_id=?", (w2, w))
        con.execute("insert into workspace_package_instances(instance_id,tenant_id,company_id,workspace_id,package_id,package_version,package_digest,status,created_at,updated_at) "
            "select 'instance-second',tenant_id,company_id,?,package_id,package_version,package_digest,status,created_at,updated_at "
            "from workspace_package_instances where workspace_id=?", (w2, w))
    return w2


def test_catalog_fixed_six_platforms_and_enums(tmp_path):
    assert [item["platform"] for item in PLATFORM_CATALOG] == ["xhs", "douyin", "wechat_oa", "tiktok", "youtube", "bilibili"]
    assert ACCOUNT_GROWTH_STAGES == ("cold_start", "growing", "mature", "declining_transforming")
    assert ACCOUNT_STATUS == ("active", "dormant", "banned")
    db, _, w = setup(tmp_path)
    with scope():
        result = ContentGrowthService(db).account_collection(COMPANY, w)
        assert result["catalog"] == [dict(item) for item in PLATFORM_CATALOG]
        assert result["accounts"] == []
        assert result["entry"]["scope"]["workspace_id"] == w


def test_create_read_edit_all_fields_and_honest_connection(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        row = create(s, w)
        ref = row["entity_id"]
        assert row["data"]["connection_status"] == "NOT_CONNECTED"
        assert row["verification_status"] == "UNVERIFIED" and row["evidence_condition"] == "MISSING"
        assert row["data"]["platform_ref"] == "xhs"
        assert s.account(COMPANY, w, ref)["data"]["name"] == "小红书主号"
        edited = s.account_edit(COMPANY, w, ref, data=edit_data(
            name="改名后的账号", growth_stage="growing", status="dormant", connection_status="CONNECTED"))
        # platform_ref is not editable (absent from edit fields); connection_status stays server-owned.
        assert edited["data"]["platform_ref"] == "xhs"
        assert edited["data"]["connection_status"] == "NOT_CONNECTED"
        for field in ACCOUNT_REF_FIELDS:
            assert field in edited["data"]
        assert edited["data"]["name"] == "改名后的账号"
        assert edited["data"]["growth_stage"] == "growing" and edited["data"]["status"] == "dormant"
        assert s.account_collection(COMPANY, w)["accounts"][0]["entity_id"] == ref
    with db.connect() as con:
        stored = con.execute("select data_json from runtime_entities where entity_id=?", (ref,)).fetchone()[0]
    assert '"connection_status": "NOT_CONNECTED"' in stored or '"connection_status":"NOT_CONNECTED"' in stored.replace(" ", "")


def test_create_ignores_client_connection_status(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        row = create(ContentGrowthService(db), w, connection_status="CONNECTED")
        assert row["data"]["connection_status"] == ACCOUNT_CONNECTION_STATUS == "NOT_CONNECTED"


def test_invalid_platform_ref_and_enum_422(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        for bad in ("", "weibo", "XHS", 123, None):
            with pytest.raises(ValueError):
                s.account_create(COMPANY, w, data=account_data(platform_ref=bad))
        for field, values in (("growth_stage", ("launch", "cold-start", "")), ("status", ("paused", "ACTIVE", ""))):
            for value in values:
                with pytest.raises(ValueError):
                    s.account_create(COMPANY, w, data=account_data(**{field: value}))
        ref = create(s, w)["entity_id"]
        with pytest.raises(ValueError):
            s.account_edit(COMPANY, w, ref, data=edit_data(status="closed"))
        with pytest.raises(ValueError):  # edit payload must not carry platform_ref
            s.account_edit(COMPANY, w, ref, data=account_data(platform_ref="douyin"))


def test_cross_company_404(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        ref = create(s, w)["entity_id"]
        for company in ("other-company", ""):
            with pytest.raises((RuntimeScopeError, ValueError)):
                s.account(company, w, ref)
            with pytest.raises((RuntimeScopeError, ValueError)):
                s.account_collection(company, w)
        with pytest.raises(RuntimeScopeError):
            s.account(COMPANY, w, "cg-account-missing")
    with scope(tenant_id="other", company_id="other-company", ceo_id="other"):
        with pytest.raises(RuntimeScopeError):
            ContentGrowthService(Database(db.path)).account("other-company", w, ref)


def test_business_level_visibility_across_workspaces(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        ref = create(s, w)["entity_id"]
        w2 = add_second_workspace(db, w)
        other = ContentGrowthService(db)
        seen = other.account_collection(COMPANY, w2)["accounts"]
        assert [a["entity_id"] for a in seen] == [ref]
        assert other.account(COMPANY, w2, ref)["data"]["name"] == "小红书主号"
        edited = other.account_edit(COMPANY, w2, ref, data=edit_data(name="跨工作区编辑"))
        assert edited["data"]["name"] == "跨工作区编辑"
        assert s.account(COMPANY, w, ref)["data"]["name"] == "跨工作区编辑"
        assert {a["workspace_id"] for a in s.account_collection(COMPANY, w2)["accounts"]} == {w}


def test_write_requires_owner_role(tmp_path):
    db, _, w = setup(tmp_path)
    with scope():
        s = ContentGrowthService(db)
        ref = create(s, w)["entity_id"]
    with scope(role="employee"):
        with pytest.raises(RuntimeScopeError):
            create(ContentGrowthService(db), w)
        with pytest.raises(RuntimeScopeError):
            ContentGrowthService(db).account_edit(COMPANY, w, ref, data=edit_data(name="越权编辑"))
        # Read remains available to scoped company members.
        assert ContentGrowthService(db).account_collection(COMPANY, w)["entry"]["scope"]["workspace_id"] == w
