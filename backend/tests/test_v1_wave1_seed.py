"""Wave-1 验收：验证项 1（种子幂等）与验证项 2（两部门实例化）。

运行方式（在 backend/ 目录下，使用项目 .venv）：
    ../.venv/bin/python -m pytest tests/test_v1_wave1_seed.py -v

覆盖：
- 验证项 1：连跑两次 ``python backend/seed_wave1.py``，第二次无 UNIQUE/重复
  报错；目录层统计稳定（tenants=1 / rd 员工=6 / content 技能=33 /
  content 工具=11 / content 员工=12 / content wt 容器=12 / department_types
  含 tech.rd+content.growth / company_packages=2）。
- 验证项 2：departments 表 tech.rd + content.growth 各 1 行；
  employee_instances≈18；workflow 实例≈29（rd 17 / content 12）。
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # 使 v1_wave1_helpers 可导入

import pytest

from v1_wave1_helpers import (
    BACKEND_DIR,
    COMPANY_PACKAGES,
    DEPARTMENT_TYPES,
    SEED_SCRIPT,
    TENANT,
    query,
    scalar,
    seed_wave1_full,
)


def _run_seed_script(db_path: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONPATH": str(BACKEND_DIR)}
    return subprocess.run(
        [sys.executable, str(SEED_SCRIPT), db_path],
        capture_output=True,
        text=True,
        cwd=str(BACKEND_DIR),
        env=env,
    )


def test_seed_script_idempotent_catalog_stable(tmp_path):
    """验证项 1：连跑两次种子脚本，目录层统计稳定且无 UNIQUE/崩溃。"""
    db = str(tmp_path / "curis.sqlite")
    r1 = _run_seed_script(db)
    assert r1.returncode == 0, r1.stderr
    r2 = _run_seed_script(db)
    assert r2.returncode == 0, r2.stderr

    # 无 UNIQUE / 重复 / 异常堆栈
    assert "UNIQUE" not in r2.stderr
    assert "Traceback" not in r2.stderr

    # 目录层（insert or ignore）统计稳定
    assert scalar(db, "select count(*) from tenants where tenant_id=?", TENANT) == 1
    assert scalar(
        db, "select count(*) from employee_templates where department_type='tech.rd'"
    ) == 6
    assert scalar(
        db,
        "select count(*) from skill_templates where skill_template_id like 'skl_ai_content_%'",
    ) == 33
    assert scalar(
        db,
        "select count(*) from tool_templates where tool_template_id like 'tl_ai_content_%'",
    ) == 11
    assert scalar(
        db,
        "select count(*) from employee_templates where department_type='content.growth'",
    ) == 12
    # content 工作流容器（department_type='content.growth'），命名含 wt_ 与
    # wt_content_ 两种前缀（既定事实），数量恒为 12。
    assert scalar(
        db, "select count(*) from workflow_templates where department_type='content.growth'"
    ) == 12

    types = {r["type_key"] for r in query(db, "select type_key from department_types")}
    for dt in DEPARTMENT_TYPES:
        assert dt in types, f"department_types 缺少 {dt}"

    assert scalar(
        db, "select count(*) from company_packages where tenant_id=?", TENANT
    ) == len(COMPANY_PACKAGES)


def test_two_departments_instantiated(tmp_path):
    """验证项 2：两部门实例化——departments 各 1 行，员工≈18，工作流实例≈29。"""
    db = str(tmp_path / "curis.sqlite")
    seed_wave1_full(db)

    depts = query(db, "select department_type, name from department_instances")
    types = {d["department_type"] for d in depts}
    assert types == {"tech.rd", "content.growth"}
    assert sum(1 for d in depts if d["department_type"] == "tech.rd") == 1
    assert sum(1 for d in depts if d["department_type"] == "content.growth") == 1

    # 员工实例：rd 6 + content 12 = 18
    assert scalar(db, "select count(*) from employee_instances") == 18
    assert scalar(
        db,
        "select count(*) from employee_instances where department_id in "
        "(select id from department_instances where department_type='tech.rd')",
    ) == 6
    assert scalar(
        db,
        "select count(*) from employee_instances where department_id in "
        "(select id from department_instances where department_type='content.growth')",
    ) == 12

    # 工作流实例：rd 17 + content 12 = 29
    assert scalar(db, "select count(*) from workflow_instances") == 29
    assert scalar(
        db,
        "select count(*) from workflow_instances "
        "where created_from_template_id like 'wl_ai_rd_%'",
    ) == 17
    assert scalar(
        db,
        "select count(*) from workflow_instances "
        "where created_from_template_id like 'wl_ai_content_%'",
    ) == 12
