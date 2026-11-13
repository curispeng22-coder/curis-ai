#!/usr/bin/env python3
"""Merge legacy Curis SQLite records into the single active database."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

HISTORY_TABLES = {"evolution_events", "capability_lessons"}


def _quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _tables(db: sqlite3.Connection) -> list[str]:
    return [
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def _columns(db: sqlite3.Connection, table: str) -> list[str]:
    return [row[1] for row in db.execute(f"PRAGMA table_info({_quote(table)})")]


def _history_memory(table: str, row: sqlite3.Row) -> tuple:
    values = dict(row)
    stable = json.dumps(
        [table, values],
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )
    memory_id = "memory-legacy-" + hashlib.sha256(stable.encode()).hexdigest()[:24]
    if table == "evolution_events":
        title = f"历史事件：{values.get('event_type') or '未记录'}"
        content = values.get("payload") or "{}"
    else:
        title = f"历史能力经验：{values.get('signature') or '未记录'}"
        content = json.dumps(
            {
                "capability_path": json.loads(values.get("cap_path_json") or "[]"),
                "outcome": values.get("outcome") or "unknown",
                "reason": values.get("reason") or "",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    created_at = values.get("created_at") or datetime.now(timezone.utc).isoformat()
    return (
        memory_id,
        values.get("tenant_id") or "default",
        "user",
        "L2",
        "legacy-import",
        title,
        content,
        json.dumps(["legacy-migration", table], ensure_ascii=False),
        "manual",
        0.5,
        "s12-legacy-migration",
        created_at,
        created_at,
    )


def _migrate_history(
    main: sqlite3.Connection,
    legacy: sqlite3.Connection,
    table: str,
) -> int:
    if table not in _tables(legacy):
        return 0
    inserted = 0
    for row in legacy.execute(f"SELECT * FROM {_quote(table)}"):
        values = _history_memory(table, row)
        before = main.total_changes
        main.execute(
            """
            INSERT OR IGNORE INTO memory_entries (
                id, tenant_id, memory_type, memory_level, user_id,
                title, content, tags_json, source_type, confidence,
                created_by, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        inserted += main.total_changes - before
    return inserted


def _migrate_table(
    main: sqlite3.Connection,
    legacy: sqlite3.Connection,
    table: str,
) -> int:
    common = [
        column for column in _columns(legacy, table) if column in _columns(main, table)
    ]
    if not common:
        return 0
    names = ", ".join(_quote(column) for column in common)
    placeholders = ", ".join("?" for _ in common)
    inserted = 0
    for row in legacy.execute(f"SELECT {names} FROM {_quote(table)}"):
        before = main.total_changes
        main.execute(
            f"INSERT OR IGNORE INTO {_quote(table)} ({names}) VALUES ({placeholders})",
            tuple(row),
        )
        inserted += main.total_changes - before
    return inserted


def converge(main_path: Path, legacy_paths: list[Path], backup_dir: Path) -> dict:
    main_path = main_path.resolve()
    legacy_paths = [path.resolve() for path in legacy_paths]
    if not main_path.is_file():
        raise FileNotFoundError(f"主库不存在：{main_path}")
    if any(path == main_path for path in legacy_paths):
        raise ValueError("旧库不能与主库相同")
    missing = [str(path) for path in legacy_paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("旧库不存在：" + ", ".join(missing))

    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_path = backup_dir.resolve() / f"{main_path.name}.before-s12-{stamp}.bak"
    shutil.copy2(main_path, backup_path)

    report = {"backup": str(backup_path), "legacy": {}, "inserted": 0}
    main = sqlite3.connect(main_path)
    main.row_factory = sqlite3.Row
    try:
        main.execute("PRAGMA foreign_keys = OFF")
        main.execute("BEGIN IMMEDIATE")
        main_tables = set(_tables(main))
        current_counts = {}
        for table in HISTORY_TABLES:
            count = _migrate_history(main, main, table)
            if count:
                current_counts[table] = count
                report["inserted"] += count
        if current_counts:
            report["legacy"][str(main_path)] = current_counts
        for legacy_path in legacy_paths:
            legacy = sqlite3.connect(f"file:{legacy_path}?mode=ro", uri=True)
            legacy.row_factory = sqlite3.Row
            try:
                counts = {}
                for table in _tables(legacy):
                    if table in HISTORY_TABLES:
                        count = _migrate_history(main, legacy, table)
                    elif table in main_tables:
                        count = _migrate_table(main, legacy, table)
                    else:
                        continue
                    if count:
                        counts[table] = count
                        report["inserted"] += count
                report["legacy"][str(legacy_path)] = counts
            finally:
                legacy.close()
        integrity = main.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = list(main.execute("PRAGMA foreign_key_check"))
        if integrity != "ok" or foreign_keys:
            raise RuntimeError(
                f"迁移后检查失败：integrity={integrity}, foreign_keys={len(foreign_keys)}"
            )
        main.commit()
        report["integrity_check"] = integrity
        report["foreign_key_violations"] = 0
        return report
    except Exception:
        main.rollback()
        shutil.copy2(backup_path, main_path)
        raise
    finally:
        main.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", type=Path, required=True, help="活动 data/curis.sqlite")
    parser.add_argument(
        "--legacy",
        type=Path,
        action="append",
        required=True,
        help="待迁移旧库，可重复",
    )
    parser.add_argument("--backup-dir", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            converge(args.main, args.legacy, args.backup_dir),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
