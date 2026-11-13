"""T-001: invalid database paths must fail before filesystem access."""
from pathlib import Path

import pytest

from app.database import Database
from app.main import create_app


@pytest.mark.parametrize("factory", [Database, create_app])
@pytest.mark.parametrize("invalid", [None, False, 0, 1, [], {}, b"db.sqlite", object()])
def test_invalid_database_path_types(factory, invalid, tmp_path, monkeypatch):
    if factory is create_app and invalid is None:
        # None is the documented default for create_app, tested separately below.
        monkeypatch.setenv("CURIS_DB", str(tmp_path / "default.sqlite"))
        factory(invalid)
        assert (tmp_path / "default.sqlite").is_file()
        return
    monkeypatch.chdir(tmp_path)
    with pytest.raises(TypeError):
        factory(invalid)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("factory", [Database, create_app])
@pytest.mark.parametrize("stringified", [False, True])
def test_database_instance_cannot_become_filename(factory, stringified, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    database = Database(tmp_path / "valid.sqlite")
    with pytest.raises(TypeError):
        factory(str(database) if stringified else database)
    assert not list(tmp_path.glob("<app.database.Database object*"))
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("factory", [Database, create_app])
@pytest.mark.parametrize("as_string", [False, True])
def test_valid_database_paths(factory, as_string, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "valid.sqlite"
    result = factory(str(path) if as_string else path)
    if factory is Database:
        with result.connect() as connection:
            assert connection.execute("select 1").fetchone()[0] == 1
    assert path.is_file()
    assert not list(Path.cwd().glob("<app.database.Database object*"))
