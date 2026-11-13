"""Wave-1（Curis 自用 v1 · 第一波）独立验收测试共享助手。

提供：
- ``seed_wave1_full(db_path)``：复刻 ``backend/seed_wave1.py`` 的 5 步序列
  （initialize → seed_wave1 → 两部门实例化 → RD 闭环 → 发布包），落到指定 DB。
- ``query`` / ``scalar``：针对测试 DB 的轻量只读查询助手。
- 关键路径常量：``SEED_SCRIPT`` / ``FRONTEND_PAGE`` 等。

本文件仅含助手，不含任何 ``test_*`` 函数，pytest 不会将其收集为测试。
"""
from __future__ import annotations

from pathlib import Path

# backend/ 目录（app 包所在）
BACKEND_DIR = Path(__file__).resolve().parent.parent
# 仓库根（含 frontend/）
REPO_ROOT = BACKEND_DIR.parent
# 一键种子脚本
SEED_SCRIPT = BACKEND_DIR / "seed_wave1.py"
# 待验收前端页面
FRONTEND_PAGE = REPO_ROOT / "frontend" / "app" / "ceo-office" / "page.js"

# 活跃租户（既定事实，单账号 selfuse）
TENANT = "selfuse"

# 两出厂包
COMPANY_PACKAGES = ["ccp_ai_software_company", "ccp_ai_content_company"]
# 两部门类型键（既定事实）
DEPARTMENT_TYPES = ["tech.rd", "content.growth"]


def seed_wave1_full(db_path: str) -> str:
    """复刻 ``backend/seed_wave1.py`` 的 5 步序列，落到 ``db_path``。

    返回 ``db_path``。调用方负责在临时目录创建该文件。
    """
    import sqlite3

    from app.company_instantiation import CompanyInstantiationService
    from app.database import Database
    from app.evolution_event_log import EvolutionEventLog
    from app.rd_workflow_runtime import RdWorkflowRuntime
    from app.tenant_context import DEFAULT_TENANT
    from app.wave1_seed import seed_wave1

    db = Database(db_path)
    db.initialize()

    event_log = EvolutionEventLog(db)
    seed_wave1(db)

    svc = CompanyInstantiationService(db, event_log)
    svc.instantiate("ccp_ai_software_company", DEFAULT_TENANT)
    svc.instantiate("ccp_ai_content_company", DEFAULT_TENANT)

    conn = sqlite3.connect(db_path)
    try:
        did = conn.execute(
            "select id from department_instances where department_type='tech.rd' limit 1"
        ).fetchone()[0]
    finally:
        conn.close()

    # T10：研发部基础闭环（scaffold 模式，无外部 LLM key）
    RdWorkflowRuntime(db, event_log).run(
        did,
        "wl_ai_rd_software_dev_sop",
        "Wave-1 验收：实现内容发布包 Markdown 导出能力",
    )
    return db_path


def query(db_path: str, sql: str, *params) -> list[dict]:
    """对测试 DB 执行只读查询，返回 dict 列表。"""
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def scalar(db_path: str, sql: str, *params):
    """返回查询的第一个单元格。"""
    import sqlite3

    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(sql, params).fetchone()[0]
    finally:
        conn.close()
