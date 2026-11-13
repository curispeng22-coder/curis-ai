from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys

import pytest

from backend.tests.db_safety import (
    ACTIVE_DATABASE,
    DB_ENVIRONMENT,
    REPOSITORY_ROOT,
    require_isolated_test_database,
)


def _set_database(monkeypatch: pytest.MonkeyPatch, path: Path) -> None:
    for name in DB_ENVIRONMENT:
        monkeypatch.setenv(name, str(path))


def _active_fingerprint() -> tuple[int, int, str] | None:
    # 干净机器没有真实数据库；同样断言子进程不得创建它。
    if not ACTIVE_DATABASE.exists():
        return None
    stat = ACTIVE_DATABASE.stat()
    return stat.st_size, stat.st_mtime_ns, hashlib.sha256(ACTIVE_DATABASE.read_bytes()).hexdigest()


def _run_without_test_database(*command: str, database: Path | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    for name in DB_ENVIRONMENT:
        if database is None:
            environment.pop(name, None)
        else:
            environment[name] = str(database)
    return subprocess.run(
        [sys.executable, *command],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_guard_requires_one_repository_external_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    isolated = tmp_path / "runtime.sqlite"
    _set_database(monkeypatch, isolated)
    assert require_isolated_test_database() == isolated.resolve()

    monkeypatch.delenv("CURIS_DB_PATH")
    with pytest.raises(RuntimeError, match="missing isolated DB variables: CURIS_DB_PATH"):
        require_isolated_test_database()

    _set_database(monkeypatch, isolated)
    monkeypatch.setenv("CURIS_WORKSPACE_DB", str(tmp_path / "other.sqlite"))
    with pytest.raises(RuntimeError, match="must resolve to one database"):
        require_isolated_test_database()

    for rejected in (ACTIVE_DATABASE, REPOSITORY_ROOT / "backend/test.sqlite"):
        _set_database(monkeypatch, rejected)
        with pytest.raises(RuntimeError, match="refusing active or repository database"):
            require_isolated_test_database()


def test_pytest_collection_fails_before_create_app_can_touch_active_database() -> None:
    before = _active_fingerprint()
    target = "backend/tests/test_rd_artifact_review.py"

    missing = _run_without_test_database("-m", "pytest", "--collect-only", "-q", target)
    assert missing.returncode != 0
    assert "Backend test DB safety: missing isolated DB variables" in missing.stderr + missing.stdout

    active = _run_without_test_database("-m", "pytest", "--collect-only", "-q", target, database=ACTIVE_DATABASE)
    assert active.returncode != 0
    assert "Backend test DB safety: refusing active or repository database" in active.stderr + active.stdout
    assert _active_fingerprint() == before


def test_backend_tests_package_import_fails_before_app_import() -> None:
    before = _active_fingerprint()
    process = _run_without_test_database("-c", "import backend.tests; import backend.app.main")
    assert process.returncode != 0
    assert "Backend test DB safety: missing isolated DB variables" in process.stderr + process.stdout
    assert _active_fingerprint() == before
