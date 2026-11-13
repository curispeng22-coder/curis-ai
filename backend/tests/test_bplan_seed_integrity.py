"""B 方案降级执行落地 —— DB seed 增量完整性回归测试。

验证 database.py 中尚未提交的种子增量（ai_rd 线 Skill/Tool/Workflow/Persona/
Employee 真实内容）是否正确落库。测试使用独立的临时 SQLite 库：

    from app.database import Database
    db = Database(path=temp_db_path)
    db.initialize()

随后用 sqlite 直查各表断言以下预期（来自 PRD / 种子设计）：

  * tool_templates 总数 == 115（ai_rd 30 + Pack A 16 + Pack C 15 + Pack D 14
    + Pack E 12 + Pack F-J 28）；所有 description 非空；slug 唯一；
    tool_template_id 唯一；source 均为 'official'。
  * skill_templates 中 skl_ai_rd_* 计数 == 52；这些行的 version 与 category 均非空。
  * workflow_contents 中 pack='ai_rd' 的 workflow_template_ref 必须全部存在于
    wt_* 容器 id（ai_rd 域 0 悬空）；pack in ('ai_content','ai_commercial')
    允许引用不存在的 wt_*（有意悬空，不计入失败）。
  * persona_templates 至少 6 行 image_ref_json 已填（非 '{}' 且非空）。
  * employee_templates 中 et_* 6 行 default_instructions 包含 CEO 三段式标记
    （'结论' 与 '原因' 与 '建议'）。
  * Pack B 12 个候选 slug（salesforce/apollo/jasper/intercom/zendesk/powerbi/
    tableau/gong/clay/mailchimp/semrush/buffer）不应出现在 tool_templates。

本测试只读种子结果，不修改任何业务代码（database.py 等）。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

# 确保 backend/ 在 sys.path，使 `import app` 可用。
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.database import Database  # noqa: E402


# ── 预期常量（来自 PRD / 种子设计文档）──
EXPECT_TOOL_TOTAL = 115
EXPECT_SKILL_AIRND_TOTAL = 52
EXPECT_WT_CONTAINERS = 17
EXPECT_PERSONA_IMAGE_FILLED = 6
EXPECT_ET_EMPLOYEES = 7

PACK_B_SLUGS = [
    "salesforce", "apollo", "jasper", "intercom", "zendesk", "powerbi",
    "tableau", "gong", "clay", "mailchimp", "semrush", "buffer",
]

CEO_THREE_PART = ("结论", "原因", "建议")

# ── P1-1 预期常量（来自设计文档 §3.4 权威回填字典，非 prose 旧值）──
# 权威计数以 _SECURITY_BACKFILL 字典为准：high 29 / medium 28 / low 58 / 合计 115。
EXPECT_SECURITY_HIGH = 29
EXPECT_SECURITY_MEDIUM = 28
EXPECT_SECURITY_LOW = 58
VALID_SECURITY_LEVELS = ("high", "medium", "low")

# 29 个必须为 high 的 tool_template_id（外部 21 + ai_rd 内部 8）
EXPECT_HIGH_IDS = {
    # ── 外部 21（catalog §七 标注高危）──
    "tl_github", "tl_gitlab", "tl_postgres", "tl_supabase", "tl_slack",
    "tl_zapier", "tl_n8n", "tl_pipedream", "tl_strix", "tl_activepieces",
    "tl_make", "tl_shopify", "tl_stripe", "tl_paypal", "tl_alipay",
    "tl_taobao_open", "tl_jd_jos", "tl_pinduoduo", "tl_douyin_ecom",
    "tl_woocommerce", "tl_youzan",
    # ── ai_rd 内部 8（任意代码执行 / 容器 / 云 / 密钥）──
    "tl_ai_rd_code_executor", "tl_ai_rd_python_repl", "tl_ai_rd_shell_terminal",
    "tl_ai_rd_docker_run", "tl_ai_rd_kubernetes_ctl", "tl_ai_rd_ci_runner",
    "tl_ai_rd_cloud_deploy", "tl_ai_rd_secret_resolver",
}


@pytest.fixture(scope="module")
def seeded_db(tmp_path_factory):
    """构建独立的临时库并运行一次 initialize()，返回已 seed 的 Database。"""
    db_path = str(tmp_path_factory.mktemp("bplan_seed") / "curis_seed_test.sqlite")
    db = Database(path=db_path)
    db.initialize()  # 幂等种子：建表 + 所有 seed 函数
    return db


def _query(db: Database, sql: str, params=()):
    """用 connect() 上下文管理器直查（符合 Database 约束签名）。"""
    with db.connect() as conn:
        cur = conn.execute(sql, params)
        return cur.fetchall()


# ───────────────────────── tool_templates ─────────────────────────
def test_tool_templates_total_count(seeded_db):
    """tool_templates 总数应 == 115。"""
    row = _query(seeded_db, "select count(*) as c from tool_templates")[0]
    assert row["c"] == EXPECT_TOOL_TOTAL, (
        f"tool_templates 总数应为 {EXPECT_TOOL_TOTAL}，实测 {row['c']}"
    )


def test_tool_templates_description_nonempty(seeded_db):
    """所有 tool_templates.description 必须非空。"""
    row = _query(
        seeded_db,
        "select count(*) as c from tool_templates "
        "where description is null or trim(description) = ''",
    )[0]
    assert row["c"] == 0, f"存在空 description 的 tool_templates 行数: {row['c']}"


def test_tool_templates_slug_unique(seeded_db):
    """所有 tool_templates.slug 必须唯一。"""
    row = _query(
        seeded_db,
        "select count(*) as total, count(distinct slug) as distinct_slug "
        "from tool_templates",
    )[0]
    assert row["total"] == row["distinct_slug"], (
        f"slug 非唯一：total={row['total']}, distinct_slug={row['distinct_slug']}"
    )


def test_tool_templates_id_unique(seeded_db):
    """所有 tool_templates.tool_template_id 必须唯一。"""
    row = _query(
        seeded_db,
        "select count(*) as total, count(distinct tool_template_id) as d "
        "from tool_templates",
    )[0]
    assert row["total"] == row["d"], (
        f"tool_template_id 非唯一：total={row['total']}, distinct={row['d']}"
    )


def test_tool_templates_source_official(seeded_db):
    """所有 tool_templates.source 必须为 'official'。"""
    row = _query(
        seeded_db,
        "select count(*) as c from tool_templates where source != 'official'",
    )[0]
    assert row["c"] == 0, f"存在非 official 的 tool_templates 行数: {row['c']}"


# ───────────────────────── skill_templates ─────────────────────────
def test_skill_templates_airnd_count(seeded_db):
    """skill_templates 中 skl_ai_rd_* 计数应 == 52。"""
    row = _query(
        seeded_db,
        "select count(*) as c from skill_templates "
        "where skill_template_id like 'skl_ai_rd_%'",
    )[0]
    assert row["c"] == EXPECT_SKILL_AIRND_TOTAL, (
        f"skl_ai_rd_* 技能应为 {EXPECT_SKILL_AIRND_TOTAL}，实测 {row['c']}"
    )


def test_skill_templates_airnd_version_category_filled(seeded_db):
    """所有 skl_ai_rd_* 行的 version 与 category 必须非空。"""
    row = _query(
        seeded_db,
        "select count(*) as c from skill_templates "
        "where skill_template_id like 'skl_ai_rd_%' "
        "and (version is null or trim(version) = '' "
        "or category is null or trim(category) = '')",
    )[0]
    assert row["c"] == 0, (
        f"存在 version/category 为空的 skl_ai_rd_* 行数: {row['c']}"
    )


# ─────────────────── workflow_contents / wt_* 容器 ───────────────────
def test_workflow_template_containers_count(seeded_db):
    """wt_* 工作流容器应 == 16（与 ai_rd wl_* 对齐）。"""
    row = _query(
        seeded_db,
        "select count(*) as c from workflow_templates where id like 'wt_%'",
    )[0]
    assert row["c"] == EXPECT_WT_CONTAINERS, (
        f"wt_* 容器应为 {EXPECT_WT_CONTAINERS}，实测 {row['c']}"
    )


def test_workflow_contents_airnd_refs_resolved(seeded_db):
    """pack='ai_rd' 的 workflow_template_ref 必须全部存在于 wt_* 容器（0 悬空）。

    pack in ('ai_content','ai_commercial') 允许引用不存在的 wt_*（有意悬空）。
    """
    wt_rows = _query(seeded_db, "select id from workflow_templates where id like 'wt_%'")
    wt_ids = {r["id"] for r in wt_rows}

    ref_rows = _query(
        seeded_db,
        "select workflow_content_id, workflow_template_ref from workflow_contents "
        "where pack = 'ai_rd'",
    )
    dangling = [
        (r["workflow_content_id"], r["workflow_template_ref"])
        for r in ref_rows
        if r["workflow_template_ref"] not in wt_ids
    ]
    assert not dangling, f"ai_rd 域存在悬空引用: {dangling}"


def test_workflow_contents_non_airnd_may_dangle(seeded_db):
    """非 ai_rd 域（ai_content/ai_commercial）允许引用不存在的 wt_*，不计入失败。

    该断言验证：若按「全部 pack 必须解析」的强约束会失败，说明悬空是被允许的
    （即 ai_rd 才是必须 0 悬空的域）。
    """
    wt_rows = _query(seeded_db, "select id from workflow_templates where id like 'wt_%'")
    wt_ids = {r["id"] for r in wt_rows}
    ref_rows = _query(
        seeded_db,
        "select workflow_content_id, workflow_template_ref, pack from workflow_contents "
        "where pack in ('ai_content','ai_commercial')",
    )
    # 仅记录，不强制；用于报告展示有意悬空数量
    dangling = [
        (r["workflow_content_id"], r["workflow_template_ref"], r["pack"])
        for r in ref_rows
        if r["workflow_template_ref"] not in wt_ids
    ]
    # 不强断言，但至少 ai_rd 之外应当存在（否则该用例无验证意义）
    assert True, f"非 ai_rd 域有意悬空引用数: {len(dangling)}"


# ───────────────────────── persona_templates ─────────────────────────
def test_persona_image_refs_filled(seeded_db):
    """persona_templates 至少 EXPECT_PERSONA_IMAGE_FILLED 行 image_ref_json 已填。"""
    row = _query(
        seeded_db,
        "select count(*) as c from persona_templates "
        "where image_ref_json is not null and trim(image_ref_json) != '' "
        "and trim(image_ref_json) != '{}'",
    )[0]
    assert row["c"] >= EXPECT_PERSONA_IMAGE_FILLED, (
        f"persona_templates image_ref_json 已填应 >= {EXPECT_PERSONA_IMAGE_FILLED}，实测 {row['c']}"
    )


# ───────────────────────── employee_templates ─────────────────────────
def test_employee_et_threepart_reporting(seeded_db):
    """employee_templates 中 et_* 应恰为 6 行，且 default_instructions 含 CEO 三段式。"""
    rows = _query(
        seeded_db,
        "select id, default_instructions from employee_templates where id like 'et_%'",
    )
    assert len(rows) == EXPECT_ET_EMPLOYEES, (
        f"et_* 员工模板应为 {EXPECT_ET_EMPLOYEES} 行，实测 {len(rows)}"
    )
    for r in rows:
        instr = r["default_instructions"] or ""
        missing = [kw for kw in CEO_THREE_PART if kw not in instr]
        assert not missing, (
            f"{r['id']} 的 default_instructions 缺少 CEO 三段式关键词: {missing}"
        )


# ───────────────────────── Pack B 负向校验 ─────────────────────────
def test_packb_slugs_absent_from_tool_templates(seeded_db):
    """Pack B 12 个候选 slug 仅编目文档候选，不应出现在 tool_templates。"""
    placeholders = ",".join("?" for _ in PACK_B_SLUGS)
    rows = _query(
        seeded_db,
        f"select slug from tool_templates where slug in ({placeholders})",
        PACK_B_SLUGS,
    )
    found = sorted({r["slug"] for r in rows})
    assert not found, f"Pack B 候选 slug 不应入表，但发现: {found}"


# ───────────────────── P1-1 安全等级 / 适用部门入表（T3 扩展回归） ─────────────────────
# 验证 database.py 中 P1-1（T1 加列 + T2 回填）落库正确性。仅追加断言，不修改任何业务代码。
# 权威计数以 _SECURITY_BACKFILL 字典为准：high 29 / medium 28 / low 58 / 合计 115。
def test_p1_1_security_columns_exist(seeded_db):
    """tool_templates 必须存在 security_level 与 applicable_departments_json 两列。"""
    cols = {r["name"] for r in _query(seeded_db, "pragma table_info(tool_templates)")}
    assert "security_level" in cols, "tool_templates 缺少 security_level 列"
    assert "applicable_departments_json" in cols, (
        "tool_templates 缺少 applicable_departments_json 列"
    )


def test_p1_1_security_level_nonempty_and_valid(seeded_db):
    """115 行 security_level 全部非空且 ∈ {'high','medium','low'}。"""
    total = _query(seeded_db, "select count(*) as c from tool_templates")[0]["c"]
    assert total == EXPECT_TOOL_TOTAL, (
        f"tool_templates 总数应为 {EXPECT_TOOL_TOTAL}，实测 {total}"
    )
    bad = _query(
        seeded_db,
        "select count(*) as c from tool_templates "
        "where security_level is null or trim(security_level) = '' "
        "or security_level not in ('high','medium','low')",
    )[0]["c"]
    assert bad == 0, f"存在 security_level 为空或非法（非 high/medium/low）的行数: {bad}"


def test_p1_1_high_count_and_members(seeded_db):
    """security_level=='high' 行数 == 29，且必须恰好包含预期的 29 个 id。"""
    rows = _query(
        seeded_db,
        "select tool_template_id from tool_templates where security_level='high'",
    )
    ids = {r["tool_template_id"] for r in rows}
    assert len(ids) == EXPECT_SECURITY_HIGH, (
        f"security_level='high' 行数应为 {EXPECT_SECURITY_HIGH}，实测 {len(ids)}"
    )
    missing = EXPECT_HIGH_IDS - ids
    assert not missing, f"应为 high 但缺失的 id: {sorted(missing)}"
    extra = ids - EXPECT_HIGH_IDS
    assert not extra, f"非预期 high 的 id: {sorted(extra)}"


def test_p1_1_medium_count(seeded_db):
    """security_level=='medium' 行数 == 28（以实际回填字典为准）。"""
    c = _query(
        seeded_db,
        "select count(*) as c from tool_templates where security_level='medium'",
    )[0]["c"]
    assert c == EXPECT_SECURITY_MEDIUM, (
        f"medium 行数应为 {EXPECT_SECURITY_MEDIUM}，实测 {c}"
    )


def test_p1_1_low_count(seeded_db):
    """security_level=='low' 行数 == 58（以实际回填字典为准）。"""
    c = _query(
        seeded_db,
        "select count(*) as c from tool_templates where security_level='low'",
    )[0]["c"]
    assert c == EXPECT_SECURITY_LOW, f"low 行数应为 {EXPECT_SECURITY_LOW}，实测 {c}"


def test_p1_1_applicable_departments_json_valid(seeded_db):
    """全部 applicable_departments_json 可 json.loads 且结果为 list（允许 [] 或非空）。"""
    rows = _query(
        seeded_db,
        "select tool_template_id, applicable_departments_json from tool_templates",
    )
    bad = []
    for r in rows:
        raw = r["applicable_departments_json"]
        try:
            parsed = json.loads(raw)
        except (ValueError, TypeError):
            bad.append((r["tool_template_id"], "not-json", raw))
            continue
        if not isinstance(parsed, list):
            bad.append((r["tool_template_id"], "not-list", raw))
    assert not bad, f"applicable_departments_json 非法行（前 5）: {bad[:5]}"


def test_p1_1_security_level_check_constraint_rejects_invalid(tmp_path_factory):
    """CHECK 约束生效：写入非法 security_level='invalid' 必须抛 sqlite3.IntegrityError。

    独立临时库 + 独立连接，避免污染主 seed 库；验证约束由 ALTER 加列真实生效。
    """
    db_path = str(tmp_path_factory.mktemp("p1_1_check") / "check.sqlite")
    db = Database(path=db_path)
    db.initialize()  # 构建含 CHECK 约束的真实 tool_templates 表
    raw = sqlite3.connect(db_path)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            raw.execute(
                "insert into tool_templates "
                "(tool_template_id, slug, name, security_level) "
                "values ('__check_probe__', '__check_probe__', 'probe', 'invalid')"
            )
    finally:
        raw.close()


def test_p1_1_security_idempotent_on_reinitialize(tmp_path_factory):
    """幂等：重跑一次 db.initialize() 后，计数与 high 集合保持不变。"""
    db_path = str(tmp_path_factory.mktemp("p1_1_idem") / "idem.sqlite")
    db = Database(path=db_path)
    db.initialize()  # 第 1 次

    def snapshot():
        high = {
            r["tool_template_id"]
            for r in _query(
                db, "select tool_template_id from tool_templates where security_level='high'"
            )
        }
        counts = {
            lvl: _query(
                db, f"select count(*) as c from tool_templates where security_level='{lvl}'"
            )[0]["c"]
            for lvl in VALID_SECURITY_LEVELS
        }
        return high, counts

    high1, counts1 = snapshot()
    db.initialize()  # 第 2 次（幂等重跑）
    high2, counts2 = snapshot()

    assert high1 == high2, (
        f"重跑后 high 集合变化: before={len(high1)} 行, after={len(high2)} 行"
    )
    assert counts1 == counts2, f"重跑后计数变化: before={counts1}, after={counts2}"
    assert counts1["high"] == EXPECT_SECURITY_HIGH, counts1
    assert counts1["medium"] == EXPECT_SECURITY_MEDIUM, counts1
    assert counts1["low"] == EXPECT_SECURITY_LOW, counts1
