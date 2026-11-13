#!/usr/bin/env python3
"""ADR-0017 D1 tenant_id 预留的本地端到端断言验证脚本。

本脚本对齐工具链中既有的 `tools/local_demo_api_smoke.py` 工程风格，作为
独立的本地 / demo 验证自动化，对 D1 多租户预留不变式做**只读断言**验证：

  - `tasks` 与 `evolution_events` 表均包含 `tenant_id` 列；
  - 新插入行（不显式指定 tenant_id）落库为哨兵值 'default'；
  - 迁移前已存在的旧行在重新 `initialize()` 后回填为 'default'；
  - `TenantContext.current_tenant_id()` 在 scope 外恒为 'default'（向后兼容哨兵），
    `is_multi_tenant()` 现已为 True（S1 D1.impl 真实多租户隔离已开启）；
  - `TenantContext.scope('ceo-2')` 在 `with` 块内注入 'ceo-2'，块外恢复 'default'；
  - D2（department 目录多租户）尚未落地：department 表不存在或为空，
    reservation 边界清晰（本项仅为读取式确认，绝不创建或修改任何表）。

红线约束：脚本只做读取 / 断言，不写库、不改 backend 业务代码、不引入未批准 slice。
退出码：0 = PASS，1 = FAIL。不依赖 pytest / unittest，可独立运行。
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# --- 路径注入 -------------------------------------------------------------
# 脚本位于仓库的 `tools/` 目录，目标模块 `app` 位于其兄弟目录 `backend/`。
# 依据脚本自身位置推导 backend 目录并加入 sys.path，确保从仓库任意位置运行。
_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = (_SCRIPT_DIR / ".." / "backend").resolve()
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

try:
    from app.database import Database
    from app.tenant_context import DEFAULT_TENANT, TenantContext
except ImportError as error:
    print(
        f"FAIL: 无法导入 backend 模块（请确认在 Curis 仓库内运行，"
        f"且 backend 处于 {_BACKEND_DIR}）：{error}",
        file=sys.stderr,
    )
    raise SystemExit(1)


@dataclass(frozen=True)
class VerifyConfig:
    """验证脚本的配置。

    Attributes:
        db_path: 用于验证的 SQLite 数据库文件路径。
        temp_dir: 使用默认临时库时为 TemporaryDirectory，否则为 None（由 main 负责清理）。
    """

    db_path: Path
    temp_dir: tempfile.TemporaryDirectory | None


class VerificationFailure(RuntimeError):
    """验证断言失败时抛出，由 main() 转换为退出码 1。"""


def main() -> int:
    """执行全部 D1 不变式断言。

    Returns:
        0 表示全部断言通过（PASS），1 表示存在失败断言（FAIL）。
    """
    config = _parse_args()
    try:
        checks = _run_all_checks(config)
    except VerificationFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    finally:
        if config.temp_dir is not None:
            config.temp_dir.cleanup()
    print("PASS: ADR-0017 D1 tenant_id 预留验证通过")
    print(
        json.dumps(
            {
                "db_path": str(config.db_path),
                "checks": checks,
            },
            ensure_ascii=False,
        )
    )
    return 0


def _parse_args() -> VerifyConfig:
    """解析命令行参数，返回 VerifyConfig。"""
    parser = argparse.ArgumentParser(
        description="对 ADR-0017 D1 tenant_id 预留不变式做本地端到端断言验证。"
    )
    parser.add_argument(
        "--db-path",
        default=None,
        help="指定数据库文件路径；未指定则使用临时库（自动清理）。",
    )
    args = parser.parse_args()

    temp_dir: tempfile.TemporaryDirectory | None = None
    if args.db_path is None:
        # 未指定路径时使用临时库，避免污染仓库或本地环境。
        temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(temp_dir.name) / "curis.sqlite"
    else:
        db_path = Path(args.db_path)

    return VerifyConfig(db_path=db_path, temp_dir=temp_dir)


def _run_all_checks(config: VerifyConfig) -> list[str]:
    """按顺序执行全部 D1 不变式断言，返回通过的 check 名称列表。

    执行次序说明：
      - 回填校验必须先于首次 `initialize()`，以模拟迁移前的无 tenant_id 状态；
        其 `initialize()` 后两表均已具备 tenant_id 列。
      - department 边界校验在 `initialize()` 之后进行，确认 D2 尚未落地。
    全程只读，不写库、不改 backend、不实现 D2 逻辑。
    """
    db = Database(str(config.db_path))

    checks: list[str] = []

    # 1) 旧行回填：模拟迁移前建表（无 tenant_id）并插入，再 initialize() 触发增量迁移回填。
    checks.append(_verify_preexisting_row_backfills(db))

    # 2) D2 reservation 边界：department 表不存在或为空（确认 D2 尚未实现）。
    checks.append(_verify_department_not_implemented(db))

    # 3) 列存在性：initialize() 后两表均含 tenant_id。
    checks.extend(_verify_table_columns(db))

    # 4) 新行默认租户：不显式指定 tenant_id 时落库为 'default'。
    checks.append(_verify_new_row_default_tenant(db))

    # 5) 上下文多租户感知（S1 D1.impl：is_multi_tenant() 现已为 True）。
    checks.append(_verify_context_tenant_aware())

    # 6) scope 注入与恢复。
    checks.append(_verify_scope_set_and_restore())

    return checks


def _columns(db: Database, table: str) -> set[str]:
    """返回指定表的列名集合。"""
    with db.connect() as conn:
        return {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}


def _verify_table_columns(db: Database) -> list[str]:
    """断言 tasks 与 evolution_events 表均包含 tenant_id 列（D1 预留字段）。"""
    checks: list[str] = []
    for table in ("tasks", "evolution_events"):
        columns = _columns(db, table)
        _require(
            "tenant_id" in columns,
            f"表 {table} 必须包含 tenant_id 预留列（实际列：{sorted(columns)}）",
        )
        checks.append(f"{table}_has_tenant_id_column")
    return checks


def _verify_new_row_default_tenant(db: Database) -> str:
    """断言新插入行（不指定 tenant_id）落库为哨兵值 'default'。"""
    with db.connect() as conn:
        conn.execute(
            "INSERT INTO tasks (task_id, content, status) VALUES ('t2', 'c2', 'open')"
        )
    with db.connect() as conn:
        tenant = conn.execute(
            "SELECT tenant_id FROM tasks WHERE task_id = 't2'"
        ).fetchone()["tenant_id"]
    _require(
        tenant == DEFAULT_TENANT,
        f"新插入行 tenant_id 应为 '{DEFAULT_TENANT}'，实际为 '{tenant}'",
    )
    return "new_row_default_tenant"


def _verify_preexisting_row_backfills(db: Database) -> str:
    """断言迁移前已存在、无 tenant_id 的旧行在重新 initialize() 后回填为 'default'。"""
    # 模拟迁移前状态：tasks 表不含 tenant_id 列，并已存在一行旧数据。
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(task_id TEXT PRIMARY KEY, content TEXT NOT NULL, status TEXT NOT NULL)"
        )
        conn.execute(
            "INSERT INTO tasks (task_id, content, status) VALUES ('t1', 'c', 'done')"
        )
    # 触发 ADR-0017 D1 增量迁移（_ensure_column 追加 tenant_id 并回填旧行）。
    db.initialize()
    with db.connect() as conn:
        tenant = conn.execute(
            "SELECT tenant_id FROM tasks WHERE task_id = 't1'"
        ).fetchone()["tenant_id"]
    _require(
        tenant == DEFAULT_TENANT,
        f"预存在旧行 tenant_id 应回填为 '{DEFAULT_TENANT}'，实际为 '{tenant}'",
    )
    return "preexisting_row_backfilled"


def _verify_department_not_implemented(db: Database) -> str:
    """确认 D2（department 目录多租户）尚未落地，D1 reservation 边界清晰。

    仅为读取式断言：department 表不应存在；若因其他脚手架残留而存在，
    则必须为空（无数据），以确认 D2 逻辑尚未实现。绝不创建或修改任何表。
    """
    with db.connect() as conn:
        exists = (
            conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='department'"
            ).fetchone()
            is not None
        )
    if exists:
        with db.connect() as conn:
            count = conn.execute("SELECT COUNT(*) AS n FROM department").fetchone()["n"]
        _require(
            count == 0,
            f"D2 尚未批准：department 表应无数据（reservation 边界），实际有 {count} 行",
        )
    return "department_not_implemented"


def _verify_context_tenant_aware() -> str:
    """断言 TenantContext 在 S1 D1.impl 后已进入真实多租户隔离态。

    scope 之外 current_tenant_id() 仍为哨兵 'default'（向后兼容），
    但 is_multi_tenant() 现已为 True（真实隔离已开启，读取按租户过滤）。
    """
    _require(
        TenantContext.current_tenant_id() == DEFAULT_TENANT,
        f"current_tenant_id() 在 scope 外应为哨兵 '{DEFAULT_TENANT}'，"
        f"实际为 '{TenantContext.current_tenant_id()}'",
    )
    _require(
        TenantContext.is_multi_tenant() is True,
        "S1 D1.impl 后 is_multi_tenant() 必须为 True（真实多租户隔离已开启）",
    )
    return "context_tenant_aware"


def _verify_scope_set_and_restore() -> str:
    """断言 scope() 在 with 块内注入租户、块外恢复哨兵值。"""
    _require(
        TenantContext.current_tenant_id() == DEFAULT_TENANT,
        "进入 scope 前 current_tenant_id() 应为哨兵值 'default'",
    )
    with TenantContext.scope("ceo-2"):
        inner = TenantContext.current_tenant_id()
        _require(
            inner == "ceo-2",
            f"scope 块内 current_tenant_id() 应为 'ceo-2'，实际为 '{inner}'",
        )
    outer = TenantContext.current_tenant_id()
    _require(
        outer == DEFAULT_TENANT,
        f"scope 块外 current_tenant_id() 应恢复为 '{DEFAULT_TENANT}'，实际为 '{outer}'",
    )
    return "scope_set_and_restore"


def _require(condition: bool, message: str) -> None:
    """断言条件为真，否则抛出 VerificationFailure。"""
    if not condition:
        raise VerificationFailure(message)


if __name__ == "__main__":
    raise SystemExit(main())
