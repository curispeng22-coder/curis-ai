"""Fail fast before Backend tests can initialize a repository database."""

from __future__ import annotations

import os
from pathlib import Path


DB_ENVIRONMENT = ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB")
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ACTIVE_DATABASE = (REPOSITORY_ROOT / "data/curis.sqlite").resolve()


def require_isolated_test_database() -> Path:
    raw = {name: os.environ.get(name, "").strip() for name in DB_ENVIRONMENT}
    missing = [name for name, value in raw.items() if not value]
    if missing:
        raise RuntimeError(f"Backend test DB safety: missing isolated DB variables: {', '.join(missing)}")

    resolved = {name: Path(value).expanduser().resolve() for name, value in raw.items()}
    if len(set(resolved.values())) != 1:
        raise RuntimeError("Backend test DB safety: CURIS_DB, CURIS_DB_PATH and CURIS_WORKSPACE_DB must resolve to one database")

    database = next(iter(resolved.values()))
    if database == ACTIVE_DATABASE or REPOSITORY_ROOT in database.parents:
        raise RuntimeError(f"Backend test DB safety: refusing active or repository database: {database}")
    return database
