"""Bounded Music metadata and real global bootstrap; external fixtures only."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path("/private/tmp/curis-music-review-bootstrap-20261011-01")
DB_KEYS = ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB")
assert {os.environ.get(key) for key in DB_KEYS} == {str(ROOT / "data/curis.sqlite")}
assert not ROOT.is_symlink()
from app.database import Database
from app.music_media_service import MusicMediaService

ALLOWED = "/private/tmp/curis-music-operating-chain-20261005-01/store"

@pytest.mark.parametrize("configured", [None, "", ALLOWED, "/private/tmp/unapproved-music-root"])
def test_real_global_music_bootstrap(configured, tmp_path):
    assert ROOT in tmp_path.parents
    env = dict(os.environ)
    env["CURIS_LOCAL_OWNER_ENABLED"] = "0"
    database = tmp_path / "bootstrap.sqlite"
    env.update({key: str(database) for key in DB_KEYS})
    if configured is None:
        env.pop("CURIS_MUSIC_REVIEW_MEDIA_ROOT", None)
    else:
        env["CURIS_MUSIC_REVIEW_MEDIA_ROOT"] = configured
    child = subprocess.run([sys.executable, "-c", "import json; from app.main import app; print('MUSIC_BOOTSTRAP='+json.dumps({'root':str(app.state.music_service.media.root) if app.state.music_service.media.root is not None else None}))"], env=env, capture_output=True, text=True, timeout=60)
    if configured == "/private/tmp/unapproved-music-root":
        assert child.returncode != 0
        assert '"exception_type":"ValueError"' in child.stderr
        with pytest.raises(ValueError, match="当前媒体目录未获准确授权"):
            MusicMediaService(Database(str(database)), root=configured)
        assert "MUSIC_BOOTSTRAP=" not in child.stdout
    else:
        assert child.returncode == 0, child.stdout + child.stderr
        value = next(line.removeprefix("MUSIC_BOOTSTRAP=") for line in child.stdout.splitlines() if line.startswith("MUSIC_BOOTSTRAP="))
        assert json.loads(value)["root"] == (configured or None)


def snapshot(db):
    with db.connect() as con:
        return {table: [tuple(row) for row in con.execute(f"select * from {table} order by 1")] for table in ["department_types", "department_type_status", "department_templates", "department_instances", "employee_instances"]}


def test_music_catalog_idempotent_empty_defaults_no_instances(tmp_path):
    assert ROOT in tmp_path.parents
    db = Database(str(tmp_path / "catalog.sqlite")); db.initialize()
    original = snapshot(db)
    with db.connect() as con:
        kind = con.execute("select * from department_types where type_key='music'").fetchone()
        template = con.execute("select * from department_templates where id='dt_music'").fetchone()
    assert kind["display_name"] == template["name"] == "音乐部"
    assert kind["category"] == "business" and kind["is_system"] == 1
    assert template["department_type"] == "music"
    assert template["source"] == "official" and template["tenant_id"] == "platform"
    assert template["status"] == "active" and template["enabled"] == 1
    assert json.loads(template["default_employee_templates_json"]) == []
    assert json.loads(template["default_capability_types_json"]) == []
    assert template["default_workflow_template_id"] is None
    db.initialize()
    assert snapshot(db) == original


@pytest.mark.parametrize("mutation", ["type-name", "type-disabled", "template-name", "template-disabled", "template-defaults"])
def test_music_catalog_conflict_fails_without_overwrite(mutation, tmp_path):
    assert ROOT in tmp_path.parents
    db = Database(str(tmp_path / "conflict.sqlite")); db.initialize()
    with db.connect() as con:
        if mutation == "type-name": con.execute("update department_types set display_name='已有私有音乐' where type_key='music'")
        elif mutation == "type-disabled": con.execute("insert into department_type_status(type_key,enabled) values ('music',0)")
        elif mutation == "template-name": con.execute("update department_templates set name='已有模板' where id='dt_music'")
        elif mutation == "template-disabled": con.execute("update department_templates set enabled=0 where id='dt_music'")
        else: con.execute("update department_templates set default_employee_templates_json='[\"existing-employee\"]' where id='dt_music'")
    original = snapshot(db)
    with pytest.raises(ValueError, match="Music department"):
        db.initialize()
    assert snapshot(db) == original
