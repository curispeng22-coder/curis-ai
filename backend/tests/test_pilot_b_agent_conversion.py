"""受控试点 B（Agent 拆解转换引擎 V1）独立校验。

显式调用 ``Database.seed_agent_conversion_pilot_b()`` 后，验证：
① 12 个 et_* 字段符合 design §7.1 映射；
② 与 6 官方员工 / 115 工具 / 52 技能零命名冲突；
③ candidate/draft 可回滚（rollback 后计数归零、基线不变）；
④ 所有 et 有合法 business.* department_type（已注册）；
⑤ emoji/color 经清洗、无控制字符、安全三段零漏报。

本测试只读种子结果、不修改业务代码；独立临时 SQLite 库，运行期零外网。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.database import Database  # noqa: E402
from app.agent_conversion.seed import (  # noqa: E402
    PILOT_B_MANIFEST,
    SeedMapper,
    build_pilot_b_rows,
)
from app.agent_conversion.agency_adapter import AgencyMarkdownAdapter  # noqa: E402
from app.agent_conversion.sanitize import clean_color, clean_emoji, has_control_chars  # noqa: E402
from app.agent_conversion.security_scan import (  # noqa: E402
    scan_credential,
    scan_overclaim,
    scan_prompt_injection,
)

SOURCES_ROOT = _BACKEND_ROOT / "app" / "agent_conversion" / "sources"

# ── §7.1 权威映射（来自设计稿，硬编码以真实验证 manifest/database）──
EXPECTED_ET = [
    ("product_feedback_synth", "product", "business.product", "official.employee.product_feedback_synth", "product-feedback-synth", "pt_product_feedback_synth"),
    ("product_trend_researcher", "product", "business.product", "official.employee.product_trend_researcher", "product-trend-researcher", "pt_product_trend_researcher"),
    ("product_nudge_engine", "product", "business.product", "official.employee.product_nudge_engine", "product-behavioral-nudge-engine", "pt_product_nudge_engine"),
    ("marketing_growth_hacker", "marketing", "business.marketing", "official.employee.marketing_growth_hacker", "marketing-growth-hacker", "pt_marketing_growth_hacker"),
    ("marketing_content_creator", "marketing", "business.marketing", "official.employee.marketing_content_creator", "marketing-content-creator", "pt_marketing_content_creator"),
    ("marketing_social_strategist", "marketing", "business.marketing", "official.employee.marketing_social_strategist", "marketing-social-media-strategist", "pt_marketing_social_strategist"),
    ("sales_pipeline_analyst", "sales", "business.sales", "official.employee.sales_pipeline_analyst", "sales-pipeline-analyst", "pt_sales_pipeline_analyst"),
    ("sales_discovery_coach", "sales", "business.sales", "official.employee.sales_discovery_coach", "sales-discovery-coach", "pt_sales_discovery_coach"),
    ("support_responder", "support", "business.support", "official.employee.support_responder", "support-support-responder", "pt_support_responder"),
    ("support_legal_compliance", "support", "business.support", "official.employee.support_legal_compliance", "support-legal-compliance-checker", "pt_support_legal_compliance"),
    ("finance_analyst", "finance", "business.finance", "official.employee.finance_analyst", "finance-financial-analyst", "pt_finance_analyst"),
    ("finance_tax_strategist", "finance", "business.finance", "official.employee.finance_tax_strategist", "finance-tax-strategist", "pt_finance_tax_strategist"),
]
EXPECTED_ASSET_SLUGS = {e[0] for e in EXPECTED_ET}
EXPECTED_ET_IDS = {e[3] for e in EXPECTED_ET}
BUSINESS_TYPES = {"business.product", "business.marketing", "business.sales", "business.support", "business.finance"}


@pytest.fixture(scope="module")
def seeded_db(tmp_path_factory):
    """构建临时库并显式调用 Pilot B opt-in seed（内部先幂等 initialize）。"""
    db_path = str(tmp_path_factory.mktemp("pilot_b") / "curis_pilot_b.sqlite")
    db = Database(path=db_path)
    db.seed_agent_conversion_pilot_b()  # opt-in，内部 initialize() + 叠加
    return db


def _q(db: Database, sql: str, params=()):
    with db.connect() as conn:
        return conn.execute(sql, params).fetchall()


# ───────────────────────── ① 12 et_* 字段符合 §7.1 ─────────────────────────
# 真实基线已含 6 个 official.employee.*（tech_lead 等职岗），与 Pilot B 的 12 个
# 并存；故此处只校验 §7.1 规定的 12 个 Pilot B id 是否齐备，而非全集相等。
_PILOT_ET_IDS = [e[3] for e in EXPECTED_ET]
_PLACEHOLDER = ",".join("?" * len(_PILOT_ET_IDS))


def test_twelve_et_present(seeded_db):
    rows = _q(seeded_db, f"select id from employee_templates where id in ({_PLACEHOLDER})", _PILOT_ET_IDS)
    ids = {r["id"] for r in rows}
    assert ids == EXPECTED_ET_IDS, f"et_* id 集合与 §7.1 不符：缺 {EXPECTED_ET_IDS - ids}，多 {ids - EXPECTED_ET_IDS}"


def test_et_fields_match_section71(seeded_db):
    rows = _q(
        seeded_db,
        "select id, slug, role, responsibility, department_type, default_instructions, "
        "persona_ref, status, source, tenant_id from employee_templates "
        "where id like 'official.employee.%'",
    )
    by_id = {r["id"]: r for r in rows}
    for asset_slug, division, dept, eid, slug, pid in EXPECTED_ET:
        r = by_id[eid]
        assert r["slug"] == slug, f"{eid} slug 应为 {slug}"
        assert r["department_type"] == dept, f"{eid} department_type 应为 {dept}"
        assert r["persona_ref"] == pid, f"{eid} persona_ref 应为 {pid}"
        assert r["status"] == "draft", f"{eid} status 应为 draft"
        assert r["source"] == "official" and r["tenant_id"] == "platform"
        assert r["role"] == asset_slug, f"{eid} role 应为 {asset_slug}"
        assert r["responsibility"] and r["responsibility"].strip(), f"{eid} responsibility 为空"
        assert r["default_instructions"] and r["default_instructions"].strip(), f"{eid} default_instructions 为空"


def test_et_persona_ref_resolves(seeded_db):
    # 仅校验 12 个 Pilot B 员工（基线 6 个 official.employee.* 的 persona_ref 为空，不在此范围）
    rows = _q(seeded_db, f"select persona_ref from employee_templates where id in ({_PLACEHOLDER})", _PILOT_ET_IDS)
    pids = {r["persona_ref"] for r in rows}
    existing = {r["persona_id"] for r in _q(seeded_db, "select persona_id from persona_templates")}
    assert pids <= existing, f"存在指向不存在 persona 的引用：{pids - existing}"


# ───────────────────────── ② 与既有资产零冲突 ─────────────────────────
def test_official_six_et_unaffected(seeded_db):
    """既有 6 官方 et_*（id LIKE 'et_%'）不被破坏。"""
    rows = _q(seeded_db, "select count(*) as c from employee_templates where id like 'et_%'")
    assert rows[0]["c"] == 7, f"et_% 官方员工应恰为 7 行，实测 {rows[0]['c']}"


def test_tool_count_base_preserved(seeded_db):
    base = _q(seeded_db, "select count(*) as c from tool_templates where tool_template_id not like 'tl_pilot_b_%'")[0]["c"]
    pilot = _q(seeded_db, "select count(*) as c from tool_templates where tool_template_id like 'tl_pilot_b_%'")[0]["c"]
    assert base == 115, f"既有 115 工具应保持不变，实测 {base}"
    assert pilot == 10, f"Pilot B 候选工具应为 10，实测 {pilot}"


def test_skill_count_base_preserved(seeded_db):
    # 真实基线技能数 = 55（设计稿 §0 记为 52，已随 baseline 演进而变化；此处对齐真实 DDL）。
    base = _q(seeded_db, "select count(*) as c from skill_templates where skill_template_id not like 'skl_pilot_b_%'")[0]["c"]
    pilot = _q(seeded_db, "select count(*) as c from skill_templates where skill_template_id like 'skl_pilot_b_%'")[0]["c"]
    assert base == 55, f"既有 55 技能应保持不变，实测 {base}"
    assert pilot == 12, f"Pilot B 候选技能应为 12，实测 {pilot}"


def test_no_slug_or_id_collision(seeded_db):
    """Pilot B 资产 id/slug 与既有 6 官方 / 115 工具 / 52 技能无重叠。"""
    # 仅取 12 个 Pilot B 员工（排除基线 6 个 official.employee.*）
    et_ids = {r["id"] for r in _q(seeded_db, f"select id from employee_templates where id in ({_PLACEHOLDER})", _PILOT_ET_IDS)}
    tool_ids = {r["tool_template_id"] for r in _q(seeded_db, "select tool_template_id from tool_templates where tool_template_id like 'tl_pilot_b_%'")}
    skill_ids = {r["skill_template_id"] for r in _q(seeded_db, "select skill_template_id from skill_templates where skill_template_id like 'skl_pilot_b_%'")}
    # 与既有 115 工具 / 52 技能 id 无交
    base_tool_ids = {r["tool_template_id"] for r in _q(seeded_db, "select tool_template_id from tool_templates where tool_template_id not like 'tl_pilot_b_%'")}
    base_skill_ids = {r["skill_template_id"] for r in _q(seeded_db, "select skill_template_id from skill_templates where skill_template_id not like 'skl_pilot_b_%'")}
    assert tool_ids.isdisjoint(base_tool_ids), f"工具 id 冲突：{tool_ids & base_tool_ids}"
    assert skill_ids.isdisjoint(base_skill_ids), f"技能 id 冲突：{skill_ids & base_skill_ids}"
    # slug 全局唯一
    all_tool_slugs = {r["slug"] for r in _q(seeded_db, "select slug from tool_templates")}
    all_skill_slugs = {r["slug"] for r in _q(seeded_db, "select slug from skill_templates")}
    assert len(all_tool_slugs) == _q(seeded_db, "select count(*) as c from tool_templates")[0]["c"], "tool slug 非唯一"
    assert len(all_skill_slugs) == _q(seeded_db, "select count(*) as c from skill_templates")[0]["c"], "skill slug 非唯一"
    # et id 彼此唯一
    assert len(et_ids) == 12


# ───────────────────────── ④ 合法 business.* department_type ─────────────────────────
def test_business_department_types_registered(seeded_db):
    # 真实基线已含 business.general；Pilot B 另注册 5 个 business.*（§7.1）。
    # 此处校验这 5 个 Pilot B 类型均已注册（子集关系，允许基线 business.general 共存）。
    rows = _q(seeded_db, "select type_key from department_types where type_key like 'business.%'")
    registered = {r["type_key"] for r in rows}
    assert BUSINESS_TYPES <= registered, f"business.* type_key 注册不全：{BUSINESS_TYPES - registered}"


def test_et_department_type_valid(seeded_db):
    # 仅校验 12 个 Pilot B 员工（基线 6 个 official.employee.* 用 software_rnd，不在 business.* 范围内）
    rows = _q(seeded_db, f"select id, department_type from employee_templates where id in ({_PLACEHOLDER})", _PILOT_ET_IDS)
    registered = {r["type_key"] for r in _q(seeded_db, "select type_key from department_types")}
    for r in rows:
        assert r["department_type"] in BUSINESS_TYPES, f"{r['id']} department_type 非法：{r['department_type']}"
        assert r["department_type"] in registered, f"{r['id']} 的 department_type 未注册"


# ───────────────────────── ⑤ emoji/color 清洗 + 安全零漏报 ─────────────────────────
def test_pt_image_ref_json_valid(seeded_db):
    rows = _q(
        seeded_db,
        "select persona_id, image_ref_json from persona_templates "
        "where persona_id like 'pt_%' and persona_id not in ("
        "'pt_supportive_coach','pt_direct_executor','pt_analytical_advisor',"
        "'pt_creative_explorer','pt_balanced_facilitator','pt_risk_aware_guardian')",
    )
    assert len(rows) == 12, f"Pilot B persona 应为 12，实测 {len(rows)}"
    for r in rows:
        obj = json.loads(r["image_ref_json"])
        assert set(["avatar", "nickname", "identity", "theme_color"]) <= set(obj.keys()), f"{r['persona_id']} image_ref_json 缺真实三键"
        assert clean_emoji(obj["avatar"]) == obj["avatar"], f"{r['persona_id']} avatar 未清洗：{obj['avatar']!r}"
        assert clean_color(obj["theme_color"]) == obj["theme_color"], f"{r['persona_id']} theme_color 非法：{obj['theme_color']!r}"
        assert not has_control_chars(obj["avatar"] + obj["identity"] + obj["theme_color"]), f"{r['persona_id']} 含控制字符"


def test_candidates_status_and_source(seeded_db):
    # 真实 skill/tool_templates.status 有 CHECK (status in ('draft','active','disabled','archived'))，
    # 不含 'candidate'（设计 §7.1 原拟 candidate，受真实约束限制改用 'draft'）。见评审 doc 的 DDL 勘误。
    skl = _q(seeded_db, "select skill_template_id, status, source from skill_templates where skill_template_id like 'skl_pilot_b_%'")
    tl = _q(seeded_db, "select tool_template_id, status, source from tool_templates where tool_template_id like 'tl_pilot_b_%'")
    for r in skl + tl:
        assert r["status"] == "draft", f"{r[0]} status 应为 draft（真实 CHECK 不允许 candidate）"
        assert r["source"] == "official"


def test_security_zero_leak(seeded_db):
    """所有 Pilot B 文本字段三段安全扫描零命中；无控制字符。"""
    texts: list[str] = []
    texts += [r["responsibility"] + (r["default_instructions"] or "") + (r["guardrails_json"] or "")
              for r in _q(seeded_db, "select responsibility, default_instructions, guardrails_json from employee_templates where id like 'official.employee.%'")]
    texts += [r["name"] + (r["traits_json"] or "") + (r["communication_style_json"] or "") +
              (r["reporting_style_json"] or "") + (r["collaboration_style_json"] or "") + (r["image_ref_json"] or "")
              for r in _q(seeded_db, "select name, traits_json, communication_style_json, reporting_style_json, collaboration_style_json, image_ref_json from persona_templates where persona_id like 'pt_%' and persona_id not in ('pt_supportive_coach','pt_direct_executor','pt_analytical_advisor','pt_creative_explorer','pt_balanced_facilitator','pt_risk_aware_guardian')")]
    texts += [r["name"] + (r["description"] or "") + (r["instruction_excerpt"] or "")
              for r in _q(seeded_db, "select name, description, instruction_excerpt from skill_templates where skill_template_id like 'skl_pilot_b_%'")]
    texts += [r["name"] + (r["description"] or "") + (r["instruction_excerpt"] or "")
              for r in _q(seeded_db, "select name, description, instruction_excerpt from tool_templates where tool_template_id like 'tl_pilot_b_%'")]
    texts += [r["name"] + (r["description"] or "") + (r["steps_json"] or "")
              for r in _q(seeded_db, "select name, description, steps_json from workflow_templates where id like 'wt_pilot_b_%'")]
    texts += [r["display_name"] + (r["description"] or "")
              for r in _q(seeded_db, "select display_name, description from department_types where type_key like 'business.%'")]
    texts += [r["name"] + (r["description"] or "") + (r["default_employee_templates_json"] or "")
              for r in _q(seeded_db, "select name, description, default_employee_templates_json from department_templates where id like 'dt_pilot_b_%'")]

    for t in texts:
        assert not scan_credential(t), f"发现凭证模式：{scan_credential(t)}"
        assert not scan_prompt_injection(t), f"发现 prompt-injection：{scan_prompt_injection(t)}"
        assert not scan_overclaim(t), f"发现 overclaim：{scan_overclaim(t)}"
        assert not has_control_chars(t), f"发现控制字符：{t!r}"


# ───────────────────────── ③ candidate/draft 可回滚 ─────────────────────────
def test_rollback_reversible(tmp_path_factory):
    db_path = str(tmp_path_factory.mktemp("pilot_b_rb") / "rb.sqlite")
    db = Database(path=db_path)
    db.seed_agent_conversion_pilot_b()

    def snapshot():
        return {
            # 仅计 12 个 Pilot B 员工（排除基线 6 个 official.employee.*）
            "et_pilot": _q(db, f"select count(*) as c from employee_templates where id in ({_PLACEHOLDER})", _PILOT_ET_IDS)[0]["c"],
            "et_official": _q(db, "select count(*) as c from employee_templates where id like 'et_%'")[0]["c"],
            # 基线 6 个 official.employee.*（software_rnd，非 Pilot B 资产），回滚须保留
            "et_baseline_official": _q(db, "select count(*) as c from employee_templates where id like 'official.employee.%' and department_type='software_rnd'")[0]["c"],
            "pt_pilot": _q(db, "select count(*) as c from persona_templates where persona_id like 'pt_%' and persona_id not in ('pt_supportive_coach','pt_direct_executor','pt_analytical_advisor','pt_creative_explorer','pt_balanced_facilitator','pt_risk_aware_guardian')")[0]["c"],
            "skl_pilot": _q(db, "select count(*) as c from skill_templates where skill_template_id like 'skl_pilot_b_%'")[0]["c"],
            "tl_pilot": _q(db, "select count(*) as c from tool_templates where tool_template_id like 'tl_pilot_b_%'")[0]["c"],
            "wt_pilot": _q(db, "select count(*) as c from workflow_templates where id like 'wt_pilot_b_%'")[0]["c"],
            "dt_pilot": _q(db, "select count(*) as c from department_templates where id like 'dt_pilot_b_%'")[0]["c"],
            # 仅计 Pilot B 注册的 5 个 business.*（排除基线 business.general，回滚不删它）
            "dt_type": _q(db, "select count(*) as c from department_types where type_key like 'business.%' and type_key != 'business.general'")[0]["c"],
            "tools_total": _q(db, "select count(*) as c from tool_templates")[0]["c"],
            # 真实基线技能数 = 55（非设计稿 §0 的 52）；+12 Pilot B = 67
            "skills_total": _q(db, "select count(*) as c from skill_templates")[0]["c"],
        }

    before = snapshot()
    assert before == {"et_pilot": 12, "et_official": 7, "et_baseline_official": 6, "pt_pilot": 12, "skl_pilot": 12,
                      "tl_pilot": 10, "wt_pilot": 12, "dt_pilot": 5, "dt_type": 5,
                      "tools_total": 125, "skills_total": 67}, before

    db.rollback_agent_conversion_pilot_b()
    after = snapshot()
    assert after == {"et_pilot": 0, "et_official": 7, "et_baseline_official": 6, "pt_pilot": 0, "skl_pilot": 0,
                     "tl_pilot": 0, "wt_pilot": 0, "dt_pilot": 0, "dt_type": 0,
                     "tools_total": 115, "skills_total": 55}, after


# ───────────────────────── 解析层（adapter + mapper）管线一致性 ─────────────────────────
def test_adapter_discovers_twelve():
    adapter = AgencyMarkdownAdapter()
    entries = list(adapter.discover(SOURCES_ROOT))
    assert len(entries) == 12, f"discover 应返回 12 条目，实测 {len(entries)}"
    slugs = {e.raw_ref["slug"] for e in entries}
    assert all("_" not in s for s in slugs)
    assert {e.raw_ref["division"] for e in entries} == {"product", "marketing", "sales", "support", "finance"}


def test_adapter_parse_required_fields():
    adapter = AgencyMarkdownAdapter()
    entries = list(adapter.discover(SOURCES_ROOT))
    for e in entries:
        raw = adapter.fetch(e)
        spec = adapter.extract_capabilities(adapter.parse(raw, e))
        # required 字段齐全
        assert spec.spec_version == "1.0.0"
        assert spec.source.adapter == "AgencyMarkdownAdapter"
        assert spec.license.spdx == "MIT" and spec.license.attribution_required
        assert spec.division.source_key in {"product", "marketing", "sales", "support", "finance"}
        assert spec.identity.name and spec.identity.role
        # 安全三段初扫零漏报
        assert spec.security_scan.is_clean, f"{e.title} 安全扫描未清零：{spec.security_scan}"
        # emoji 已清洗
        assert clean_emoji(spec.identity.emoji) == spec.identity.emoji, f"{e.title} emoji 未清洗"
        # asset_slug ∈ §7.1
        assert spec.asset_slug() in EXPECTED_ASSET_SLUGS, f"{e.title} asset_slug 不在 §7.1：{spec.asset_slug()}"


def test_adapter_extracts_capabilities():
    adapter = AgencyMarkdownAdapter()
    entries = list(adapter.discover(SOURCES_ROOT))
    total = 0
    for e in entries:
        spec = adapter.extract_capabilities(adapter.parse(adapter.fetch(e), e))
        total += len(spec.capability_candidates.tool_candidates) + len(spec.capability_candidates.skill_candidates)
    assert total > 0, "adapter 应至少抽取到若干隐含工具/技能候选"


def test_seedmapper_matches_section71():
    """SeedMapper 产出的 et_*/pt_* 结构键与 §7.1 完全一致。"""
    entries = {e["asset_slug"]: e for e in PILOT_B_MANIFEST}
    for asset_slug, division, dept, eid, slug, pid in EXPECTED_ET:
        e = entries[asset_slug]
        et = SeedMapper.map_employee(e)
        # 顺序：(id, slug, name, role, responsibility, department_type, ...)
        assert et[0] == eid, f"map_employee id 不符：{et[0]} != {eid}"
        assert et[1] == slug, f"map_employee slug 不符：{et[1]} != {slug}"
        assert et[5] == dept, f"map_employee department_type 不符：{et[5]} != {dept}"
        assert et[11] == pid, f"map_employee persona_ref 不符：{et[11]} != {pid}"
        pt = SeedMapper.map_persona(e)
        assert pt[0] == pid, f"map_persona persona_id 不符：{pt[0]} != {pid}"
        # persona slug = kebab(asset_slug)（与既有 6 官方 persona 一致），不等同于 et slug
        assert pt[1] == asset_slug.replace("_", "-"), f"map_persona slug 不符：{pt[1]} != {asset_slug.replace('_','-')}"
        # archetype ∈ 6 值 CHECK
        assert pt[3] in ("supportive_coach", "direct_executor", "analytical_advisor",
                          "creative_explorer", "balanced_facilitator", "risk_aware_guardian")
        # image_ref_json 真实三键 + theme_color
        img = json.loads(pt[14])
        assert set(["avatar", "nickname", "identity", "theme_color"]) <= set(img.keys())


def test_build_pilot_b_rows_shape():
    rows = build_pilot_b_rows()
    assert len(rows["employees"]) == 12
    assert len(rows["personas"]) == 12
    assert len(rows["skills"]) == 12
    assert len(rows["tools"]) == 10
    assert len(rows["workflows"]) == 12
    assert len(rows["departments"]) == 5
    assert len(rows["department_types"]) == 5
