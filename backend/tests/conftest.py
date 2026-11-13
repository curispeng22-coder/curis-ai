"""ADR-0028 Phase-2 (issue 065) shared test guards + fixtures.

Reuses the S4 D4.platform forbidden-scope list (``test_d4_platform._FORBIDDEN``)
verbatim, and extends the approved controlled-write event types with the new
``capability.*`` namespace introduced by this feature. Scans the three app files
touched by this feature: ``model_catalog.py``, ``main.py``, ``database.py``.

Imported by the D5 unittest modules via ``from conftest import ...`` (the test
files insert their own directory onto sys.path so the import is robust under
pytest's package-import mode).
"""
from __future__ import annotations

import re
from pathlib import Path
from runpy import run_path

ISOLATED_TEST_DATABASE = run_path(
    str(Path(__file__).with_name("db_safety.py"))
)["require_isolated_test_database"]()

_REPO_ROOT = Path(__file__).resolve().parents[1]  # backend/
_APP_DIR = _REPO_ROOT / "app"

# 真实研发闭环 fixture 用例（test_real_rd_fixture_a.py / _b.py）初始即失败——其源码
# 处于"待 executor 修复"的 buggy 状态（设计意图：fail-before-pass 的 TDD 题目）。
# 为避免污染常规 `pytest backend/tests/` 绿闸收集，将其排除；它们由 executor 通过
# 显式路径运行（见 backend/tests/real_run/run_real_issues.py）。
# 使用绝对路径以确保在不同 rootdir 推断下都能稳定命中。
_TESTS_DIR = Path(__file__).resolve().parent
collect_ignore = [
    _TESTS_DIR / "test_real_rd_fixture_a.py",
    _TESTS_DIR / "test_real_rd_fixture_b.py",
]

# App files modified/added by this feature (forbidden-scope scan scope).
_CHANGED_APP_FILES = [
    _APP_DIR / "model_catalog.py",
    _APP_DIR / "capability_catalog.py",
    _APP_DIR / "main.py",
    _APP_DIR / "database.py",
]

# S4 D4.platform forbidden-scope list (verbatim from test_d4_platform._FORBIDDEN).
# (pattern, kind): "zero" -> zero hits; "def-only" -> def placeholder only;
# "decl-str" -> only inside a LOCKED_ACTIONS string literal.
_FORBIDDEN = [
    (r"lift_human_approval_gate\(", "zero"),
    (r"auto_modify_code", "decl-str"),
    (r"manage_employees\(", "zero"),
    (r"connect_platform\(", "zero"),
    (r"roi_schema", "zero"),
    (r'app\.get\(\s*["\']/api/govern', "zero"),
    (r'app\.post\(\s*["\']/api/govern', "zero"),
    (r"\bvector\b", "zero"),
    (r"\bembedding\b", "zero"),
    (r"import openai", "zero"),
    (r"import boto3", "zero"),
    (r"import anthropic", "zero"),
    (r"from requests", "zero"),
    (r"import requests", "zero"),
]

# Approved controlled evolution_events write types:
#  - S4 governance.* (gate-approved)
#  - Phase-2 capability.* (this feature)
_APPROVED_EVENT_TYPES = {
    "governance.propose",
    "governance.apply",
    "governance.type_created",
    "governance.type_removed",
    "governance.policy_set",
    "capability.gateway_created",
    "capability.gateway_status_changed",
    "capability.model_created",
    "capability.model_status_changed",
    "capability.created",
    "capability.status_changed",
}


def grep_files(files, pattern):
    """Return list of ``relpath:line: code`` hits for ``pattern`` across ``files``."""
    compiled = re.compile(pattern)
    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if compiled.search(line):
                try:
                    rel = path.relative_to(_REPO_ROOT.parent)
                except ValueError:
                    rel = path
                hits.append(f"{rel}:{i}: {line.strip()}")
    return hits


def assert_forbidden_clean(files=None):
    """Return a list of (pattern, hits) violations; empty list == pass."""
    files = files or _CHANGED_APP_FILES
    violations = []
    for pattern, kind in _FORBIDDEN:
        hits = grep_files(files, pattern)
        if kind == "zero":
            if hits:
                violations.append((pattern, hits))
        elif kind == "def-only":
            for hit in hits:
                code = hit.split(": ", 1)[-1]
                if not code.strip().startswith("def "):
                    violations.append((pattern, [hit]))
        elif kind == "decl-str":
            for hit in hits:
                code = hit.split(": ", 1)[-1]
                if not re.match(r'^\s*"[^"]*",?\s*$', code.strip()):
                    violations.append((pattern, [hit]))
    return violations


def changed_app_files():
    """Return the list of app files scanned by the forbidden-scope guard."""
    return list(_CHANGED_APP_FILES)


def seed_canonical_business(database, tenant_id, company_id, business_id, *, department_id=None):
    """Seed only the parent relation required by legacy focused Runtime tests."""
    department_id = department_id or f"department-{company_id}"
    with database.connect() as connection:
        connection.execute(
            "insert or ignore into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values (?, ?, ?, 'test-department-template', '测试部门', 'TEST')",
            (department_id, tenant_id, company_id),
        )
        connection.execute(
            "insert or ignore into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
            "lifecycle_status, created_at, updated_at) values (?, ?, ?, ?, ?, 'DRAFT', current_timestamp, current_timestamp)",
            (business_id, tenant_id, company_id, department_id, business_id),
        )
    return business_id


# ── Wave 2（v1-selfuse）共享夹具 ──────────────────────────────────────────
# 强制 mock 模式（验证项 1：Connector mock 端到端），其余测试不受影响。
import os as _os
import sys as _sys

_os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")
_os.environ.setdefault("CURIS_ENV", "test")
_os.environ.setdefault("CURIS_IDENTITY_MODE", "test")

_BACKEND_DIR = str(_REPO_ROOT)
if _BACKEND_DIR not in _sys.path:
    _sys.path.insert(0, _BACKEND_DIR)

# 子进程不会继承 sys.path；显式传递仓库与 backend 的模块搜索路径。
_IMPORT_ROOTS = (str(_REPO_ROOT.parent), _BACKEND_DIR)
for _import_root in _IMPORT_ROOTS:
    if _import_root not in _sys.path:
        _sys.path.insert(0, _import_root)
_existing_pythonpath = _os.environ.get("PYTHONPATH", "").split(_os.pathsep)
_os.environ["PYTHONPATH"] = _os.pathsep.join(dict.fromkeys(
    [*_IMPORT_ROOTS, *(entry for entry in _existing_pythonpath if entry)]
))

# 决策队列的默认库独立于 CURIS_DB；在应用导入前将两种模块名都隔离。
# 显式传入路径的 PendingDecisionStore 仍按原测试要求工作。
import importlib as _importlib
for _module_name in ("app.decision_sink", "backend.app.decision_sink"):
    _decision_sink = _importlib.import_module(_module_name)
    _decision_sink._default_db_path = lambda: str(
        ISOLATED_TEST_DATABASE.parent / "b_layer_pending_decisions.sqlite"
    )

from app.database import Database as _Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog as _EvolutionEventLog  # noqa: E402
from app.wave1_seed import seed_wave1 as _seed_wave1  # noqa: E402
from app.tenant_context import DEFAULT_TENANT as _DEFAULT_TENANT  # noqa: E402

import pytest as _pytest


@_pytest.fixture
def seeded_db(tmp_path):
    """返回已 initialize + seed_wave1 的临时 DB 路径（未实例化部门）。"""
    db_path = str(tmp_path / "curis.sqlite")
    db = _Database(db_path)
    db.initialize()
    _seed_wave1(db)
    yield db_path


@_pytest.fixture
def tenant():
    return _DEFAULT_TENANT
