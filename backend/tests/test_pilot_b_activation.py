"""受控试点 B 聚焦激活（★5）独立校验。

验证 ``Database.activate_pilot_b_highvalue()`` / ``deactivate_pilot_b_highvalue()``：
- 激活后：4 个 et_* status='active'、4 个 pt_* status='active'；
  其余 8 个 et / 8 个 pt 仍 'draft'；基线 6 个 official.employee.*(software_rnd)
  不受影响；基线 115 工具 / 55 技能（非 pilot_b_ 前缀）不被改动；
  工具/技能/persona 总数与 seed 后完全一致（激活仅改 status 元数据，不改增删）。
- 回滚后：上述 4 个 et/pt 回到 'draft'，与激活前（纯 seed）等价。

独立临时 SQLite 库，运行期零外网。本文件不修改业务代码。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.database import Database  # noqa: E402

# 4 个 ★5 激活目标（与 database.py 中激活函数保持一致）
HV_ET_IDS = (
    "official.employee.marketing_growth_hacker",
    "official.employee.marketing_content_creator",
    "official.employee.support_responder",
    "official.employee.finance_analyst",
)
HV_PT_IDS = (
    "pt_marketing_growth_hacker",
    "pt_marketing_content_creator",
    "pt_support_responder",
    "pt_finance_analyst",
)
# 其余 8 个 Pilot B et/pt（激活函数不应触碰）
OTHER_ET_IDS = (
    "official.employee.product_feedback_synth",
    "official.employee.product_trend_researcher",
    "official.employee.product_nudge_engine",
    "official.employee.marketing_social_strategist",
    "official.employee.sales_pipeline_analyst",
    "official.employee.sales_discovery_coach",
    "official.employee.support_legal_compliance",
    "official.employee.finance_tax_strategist",
)
OTHER_PT_IDS = (
    "pt_product_feedback_synth",
    "pt_product_trend_researcher",
    "pt_product_nudge_engine",
    "pt_marketing_social_strategist",
    "pt_sales_pipeline_analyst",
    "pt_sales_discovery_coach",
    "pt_support_legal_compliance",
    "pt_finance_tax_strategist",
)

_PLACEHOLDER_ET = ",".join("?" * len(HV_ET_IDS))
_PLACEHOLDER_PT = ",".join("?" * len(HV_PT_IDS))


@pytest.fixture(scope="module")
def activated_db(tmp_path_factory):
    """先 opt-in seed Pilot B（全 draft），再聚焦激活 4 个 ★5。"""
    db_path = str(tmp_path_factory.mktemp("pilot_b_act") / "curis_activate.sqlite")
    db = Database(path=db_path)
    db.seed_agent_conversion_pilot_b()  # 落 12 et(draft) + 12 pt(draft) + skl/tl/wt/dt
    db.activate_pilot_b_highvalue()     # 仅 4 et + 4 pt → 'active'
    return db


def _q(db: Database, sql: str, params=()) -> list:
    with db.connect() as conn:
        return conn.execute(sql, params).fetchall()


def _status_et(db: Database, eids: tuple) -> dict:
    ph = ",".join("?" * len(eids))
    rows = _q(db, f"select id, status from employee_templates where id in ({ph})", eids)
    return {r["id"]: r["status"] for r in rows}


def _status_pt(db: Database, pids: tuple) -> dict:
    ph = ",".join("?" * len(pids))
    rows = _q(db, f"select persona_id, status from persona_templates where persona_id in ({ph})", pids)
    return {r["persona_id"]: r["status"] for r in rows}


# ───────────────────────── 激活：4 个 ★5 变 active ─────────────────────────
def test_four_hv_et_active(activated_db):
    st = _status_et(activated_db, HV_ET_IDS)
    assert set(st.keys()) == set(HV_ET_IDS), f"激活目标 et 缺失：{set(HV_ET_IDS) - set(st.keys())}"
    assert all(v == "active" for v in st.values()), f"4 个 ★5 et 应全 active：{st}"


def test_four_hv_pt_active(activated_db):
    st = _status_pt(activated_db, HV_PT_IDS)
    assert set(st.keys()) == set(HV_PT_IDS), f"激活目标 pt 缺失：{set(HV_PT_IDS) - set(st.keys())}"
    assert all(v == "active" for v in st.values()), f"4 个 ★5 pt 应全 active：{st}"


def test_other_eight_et_still_draft(activated_db):
    st = _status_et(activated_db, OTHER_ET_IDS)
    assert set(st.keys()) == set(OTHER_ET_IDS), f"其余 8 个 et 应齐全：{set(OTHER_ET_IDS) - set(st.keys())}"
    assert all(v == "draft" for v in st.values()), f"其余 8 个 et 应维持 draft：{st}"


def test_other_eight_pt_still_draft(activated_db):
    st = _status_pt(activated_db, OTHER_PT_IDS)
    assert set(st.keys()) == set(OTHER_PT_IDS)
    assert all(v == "draft" for v in st.values()), f"其余 8 个 pt 应维持 draft：{st}"


def test_baseline_official_employees_unaffected(activated_db):
    """基线 6 个 official.employee.*(software_rnd) 不受激活影响。"""
    rows = _q(
        activated_db,
        "select count(*) as c from employee_templates "
        "where id like 'official.employee.%' and department_type='software_rnd'",
    )
    assert rows[0]["c"] == 6, f"基线 6 个 official.employee.* 应保留，实测 {rows[0]['c']}"


def test_baseline_tools_skills_untouched(activated_db):
    """基线 115 工具 / 55 技能（非 pilot_b_ 前缀）不被激活改动。"""
    base_tools = _q(
        activated_db,
        "select count(*) as c from tool_templates where tool_template_id not like 'tl_pilot_b_%'",
    )[0]["c"]
    base_skills = _q(
        activated_db,
        "select count(*) as c from skill_templates where skill_template_id not like 'skl_pilot_b_%'",
    )[0]["c"]
    assert base_tools == 115, f"基线 115 工具应保持不变，实测 {base_tools}"
    assert base_skills == 55, f"基线 55 技能应保持不变，实测 {base_skills}"


def test_totals_preserved_after_activation(activated_db):
    """激活仅改 status 元数据：与 seed 后计数完全一致（125 工具 / 67 技能 / 18 persona）。"""
    tools = _q(activated_db, "select count(*) as c from tool_templates")[0]["c"]
    skills = _q(activated_db, "select count(*) as c from skill_templates")[0]["c"]
    personas = _q(activated_db, "select count(*) as c from persona_templates")[0]["c"]
    assert tools == 125, f"工具总数不应因激活变化（125），实测 {tools}"
    assert skills == 67, f"技能总数不应因激活变化（67），实测 {skills}"
    # 6 基线官方 persona + 12 Pilot B = 18
    assert personas == 18, f"persona 总数不应因激活变化（18），实测 {personas}"


# ───────────────────────── 回滚：回到 draft，与激活前等价 ─────────────────────────
def test_deactivate_returns_to_draft(tmp_path_factory):
    db_path = str(tmp_path_factory.mktemp("pilot_b_deact") / "deact.sqlite")
    db = Database(path=db_path)
    db.seed_agent_conversion_pilot_b()
    db.activate_pilot_b_highvalue()
    # 激活后确为 active
    st_act_et = _status_et(db, HV_ET_IDS)
    st_act_pt = _status_pt(db, HV_PT_IDS)
    assert all(v == "active" for v in st_act_et.values()), f"激活后 4 et 应 active：{st_act_et}"
    assert all(v == "active" for v in st_act_pt.values()), f"激活后 4 pt 应 active：{st_act_pt}"

    # 回滚
    db.deactivate_pilot_b_highvalue()

    st_et = _status_et(db, HV_ET_IDS)
    st_pt = _status_pt(db, HV_PT_IDS)
    assert all(v == "draft" for v in st_et.values()), f"回滚后 4 et 应回 draft：{st_et}"
    assert all(v == "draft" for v in st_pt.values()), f"回滚后 4 pt 应回 draft：{st_pt}"
    # 与「从未激活」等价：其余 8 个保持 draft
    st_other = _status_et(db, OTHER_ET_IDS)
    st_other_pt = _status_pt(db, OTHER_PT_IDS)
    assert all(v == "draft" for v in st_other.values()), f"回滚后其余 8 et 应 draft：{st_other}"
    assert all(v == "draft" for v in st_other_pt.values()), f"回滚后其余 8 pt 应 draft：{st_other_pt}"
    # 计数不变
    tools = _q(db, "select count(*) as c from tool_templates")[0]["c"]
    skills = _q(db, "select count(*) as c from skill_templates")[0]["c"]
    assert tools == 125 and skills == 67, f"回滚后计数应不变（125/67），实测 {tools}/{skills}"


def test_deactivate_idempotent_on_draft(tmp_path_factory):
    """未激活（全 draft）状态下调用 deactivate 也安全（幂等，不影响其他行）。"""
    db_path = str(tmp_path_factory.mktemp("pilot_b_deact_idem") / "idem.sqlite")
    db = Database(path=db_path)
    db.seed_agent_conversion_pilot_b()  # 全 draft
    db.deactivate_pilot_b_highvalue()   # 无激活也安全

    st_et = _status_et(db, HV_ET_IDS)
    st_pt = _status_pt(db, HV_PT_IDS)
    assert all(v == "draft" for v in st_et.values()), f"deactivate(全 draft) 后 4 et 应仍 draft：{st_et}"
    assert all(v == "draft" for v in st_pt.values()), f"deactivate(全 draft) 后 4 pt 应仍 draft：{st_pt}"
    # 其他 8 个同样不受影响
    st_other = _status_et(db, OTHER_ET_IDS)
    assert all(v == "draft" for v in st_other.values())
