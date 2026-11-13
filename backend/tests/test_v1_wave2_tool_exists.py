"""Wave 2 验证项 5（_tool_exists 修复复验）。

覆盖：
- 实例化两部门（研发 + 内容）后，tl_* unresolved 列表应为空
  （C1 修复 _tool_exists 解析 tool_templates）。
- 特别地，tl_ai_content_social_upload 已解析（不再是 unresolved）。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")

from app.company_instantiation import CompanyInstantiationService  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.tenant_context import DEFAULT_TENANT  # noqa: E402

import pytest  # noqa: E402


def test_instantiate_both_departments_no_unresolved_tool_refs(seeded_db):
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    svc = CompanyInstantiationService(db, event_log)

    rd = svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    content = svc.instantiate("ccp_ai_content_company", DEFAULT_TENANT)

    rd_unresolved = rd.get("unresolved_refs", {}).get("tool_refs", [])
    ct_unresolved = content.get("unresolved_refs", {}).get("tool_refs", [])

    assert rd_unresolved == [], f"研发部 unresolved tool_refs: {rd_unresolved}"
    assert ct_unresolved == [], f"内容部 unresolved tool_refs: {ct_unresolved}"

    # 关键工具已解析（C1 修复点）
    assert "tl_ai_content_social_upload" not in ct_unresolved


def test_tl_ai_content_social_upload_template_exists(seeded_db):
    """底层事实：tl_ai_content_social_upload 工具模板已 seed（解析可成功）。"""
    with Database(seeded_db).connect() as conn:
        n = conn.execute(
            "select count(*) as c from tool_templates where tool_template_id='tl_ai_content_social_upload'"
        ).fetchone()["c"]
    assert n == 1


def test_tl_ai_rd_tool_templates_count(seeded_db):
    """研发部 30 个 tl_ai_rd_* 工具模板已就位（T14 基础）。"""
    with Database(seeded_db).connect() as conn:
        n = conn.execute(
            "select count(*) as c from tool_templates where tool_template_id like 'tl_ai_rd_%'"
        ).fetchone()["c"]
    assert n == 30, f"tl_ai_rd_* 工具模板数应为 30，实际 {n}"
