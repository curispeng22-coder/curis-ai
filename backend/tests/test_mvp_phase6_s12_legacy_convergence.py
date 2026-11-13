import importlib.util
import sqlite3
from pathlib import Path


SCRIPT = Path(__file__).parents[2] / "tools/migrations/converge_legacy_sqlite.py"
SPEC = importlib.util.spec_from_file_location("converge_legacy_sqlite", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def _database(path: Path, current: bool) -> None:
    db = sqlite3.connect(path)
    db.executescript(
        """
        CREATE TABLE companies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            current_note TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE evolution_events (
            event_id INTEGER PRIMARY KEY,
            correlation_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL,
            tenant_id TEXT NOT NULL,
            idempotency_key TEXT
        );
        """
    )
    if current:
        db.executescript(
            """
            CREATE TABLE memory_entries (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                memory_level TEXT NOT NULL,
                user_id TEXT NOT NULL DEFAULT '',
                project_id TEXT,
                employee_id TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                tags_json TEXT NOT NULL DEFAULT '[]',
                source_type TEXT NOT NULL DEFAULT 'manual',
                source_task_id TEXT,
                confidence REAL NOT NULL DEFAULT 1.0,
                status TEXT NOT NULL DEFAULT 'active',
                use_count INTEGER NOT NULL DEFAULT 0,
                last_used_at TEXT,
                created_by TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            INSERT INTO companies VALUES ('company-current', '当前公司', '主库优先');
            """
        )
    else:
        db.executescript(
            """
            INSERT INTO companies (id, name) VALUES
                ('company-current', '旧名称'),
                ('company-legacy', '旧库公司');
            INSERT INTO evolution_events VALUES
                (1, 'run-1', 'workflow.completed', '{"result":"ok"}',
                 '2026-07-01T00:00:00Z', 'tenant-a', NULL);
            """
        )
    db.commit()
    db.close()


def test_legacy_convergence_is_backed_up_transactional_and_idempotent(tmp_path):
    main = tmp_path / "curis.sqlite"
    legacy = tmp_path / "workspace.sqlite"
    backups = tmp_path / "backups"
    _database(main, current=True)
    _database(legacy, current=False)

    first = MODULE.converge(main, [legacy], backups)
    second = MODULE.converge(main, [legacy], backups)

    db = sqlite3.connect(main)
    assert db.execute(
        "SELECT name, current_note FROM companies WHERE id = 'company-current'"
    ).fetchone() == ("当前公司", "主库优先")
    assert db.execute(
        "SELECT name FROM companies WHERE id = 'company-legacy'"
    ).fetchone() == ("旧库公司",)
    assert db.execute(
        "SELECT count(*) FROM memory_entries WHERE created_by = 's12-legacy-migration'"
    ).fetchone() == (1,)
    assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    assert list(db.execute("PRAGMA foreign_key_check")) == []
    db.close()

    assert first["inserted"] == 2
    assert second["inserted"] == 0
    assert len(list(backups.glob("*.bak"))) >= 1
