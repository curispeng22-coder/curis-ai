from __future__ import annotations

import fcntl
import errno
import hashlib
import json
import os
import select
import shutil
import signal
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
import pytest
import zipfile
from unittest.mock import patch
from pathlib import Path


def _damaged_package_fixture(base, kind="full"):
    """Self-authored three-package/eleven-file scene; never a copied user DB."""
    import io
    import wave
    root = base / "profile"
    root.mkdir()
    db, old_store = make_full_root(root, "saved")
    store = root / "data/workspace-packages"
    old_store.rename(store)
    old_store.parent.rmdir()
    first = store / "com.curis.test/0.1.0/published"
    (first / "schemas").mkdir()
    (first / "schemas/item.json").write_text('{"type":"object"}')
    (first / "README.md").write_text("Self-authored recovery fixture")
    package_dirs = [first]
    for index, count in ((1, 4), (2, 3)):
        folder = store / f"com.curis.synthetic{index}/0.1.0/published"
        (folder / "schemas").mkdir(parents=True)
        (folder / "manifest.json").write_text(json.dumps({"packageId": f"com.curis.synthetic{index}"}))
        (folder / "surface.json").write_text('{"title":"synthetic"}')
        (folder / "schemas/item.json").write_text('{"type":"object"}')
        if count == 4: (folder / "README.md").write_text("Self-authored recovery fixture")
        package_dirs.append(folder)
    with sqlite3.connect(db) as conn:
        conn.execute("delete from installed_workspace_packages")
        conn.executemany("insert into installed_workspace_packages values (?,?,?)",
                         [(str(p), _package_digest(p), "ACTIVE") for p in package_dirs])
    (root / "export/cg.json").write_text(json.dumps(cg_export_fixture(), ensure_ascii=False))
    for index in range(5):
        audio = io.BytesIO()
        with wave.open(audio, "wb") as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(8000)
            wav.writeframes(bytes((index, 0)) * 800)
        raw = audio.getvalue()
        target = root / recovery.MUSIC_TREE / (hashlib.sha256(raw).hexdigest() + ".wav")
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
    archive = base / "synthetic.zip"
    saved = backup_v2(root, archive)
    assert saved["status"] == "BACKUP_VERIFIED" and saved["files"] == 20
    with zipfile.ZipFile(archive) as bundle:
        rows = json.loads(bundle.read("manifest.json"))["files"]
    files = sorted(p for folder in package_dirs for p in folder.rglob("*") if p.is_file())
    assert len(files) == 11
    deleted = files if kind == "full" else [first / "schemas/item.json"]
    for path in deleted: path.unlink()
    return root, db, store, archive, rows, deleted


def _fixture_scene(root):
    """Managed-file bytes/links, excluding intentional recovery bookkeeping."""
    result = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("recovery/"): continue
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode): result[rel] = ("link", os.readlink(path))
        elif stat.S_ISREG(info.st_mode): result[rel] = ("file", hashlib.sha256(path.read_bytes()).hexdigest())
    return result


@pytest.mark.parametrize("kind", ["full", "partial"])
@pytest.mark.parametrize("failure", [None, "first", "package"])
def test_damaged_packages_restore_and_exact_missing_rollback(tmp_path, kind, failure):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, kind)
    before = _fixture_scene(root)
    dirs = sorted(str(p) for p in store.rglob("*") if p.is_dir())
    preview = preflight_v2(root, archive)
    assert preview["currentMode"] == "DAMAGED_PACKAGE_FILES"
    assert preview["targetIdentity"] == preview["identity"]
    assert _cold_status(root)["nextAction"] == "CHOOSE_VERIFIED_BACKUP"
    if failure:
        index = 1 if failure == "first" else next(i + 1 for i, row in enumerate(rows) if row["path"].startswith("data/workspace-packages/"))
        with pytest.raises(RuntimeError, match="injected restore interruption"):
            restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], fail_after_files=index)
        assert _fixture_scene(root) == before
        assert all(not p.exists() for p in deleted)
        assert sorted(str(p) for p in store.rglob("*") if p.is_dir()) == dirs
        assert not (root / "recovery/active.json").exists()
        assert _cold_status(root)["currentMode"] == "DAMAGED_PACKAGE_FILES"
        assert recovery._observed_state(root, "data/workspace-packages")["generation"] == preview["currentGeneration"]
        return
    assert restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"])["status"] == "RESTORED"
    assert recovery._observed_state(root, "data/workspace-packages")["mode"] == "HEALTHY"
    assert recovery._raw_rows(root, "data/workspace-packages") == rows
    assert all(p.is_file() for p in deleted)


@pytest.mark.parametrize("kind", ["full", "partial"])
def test_damaged_packages_process_interruption_and_cold_reconcile(tmp_path, kind):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, kind)
    before = _fixture_scene(root)
    preview = preflight_v2(root, archive)
    code = '''import os, signal, sys
from pathlib import Path
from desktop.runtime import recovery as r
original = r._replace_from
def terminate_after_package(root, relative, source, temporary):
    original(root, relative, source, temporary)
    if relative.startswith("data/workspace-packages/"):
        os.kill(os.getpid(), signal.SIGTERM)
r._replace_from = terminate_after_package
r.restore_v2(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4])
'''
    proc = subprocess.run([sys.executable, "-B", "-c", code, str(root), str(archive), preview["archiveSha256"], preview["currentGeneration"]], capture_output=True, timeout=20)
    assert proc.returncode == -signal.SIGTERM, proc.stderr.decode()
    assert (root / "recovery/active.json").exists()
    cold = subprocess.run([sys.executable, "-B", "-c", 'import json,sys;from pathlib import Path;from desktop.runtime import recovery as r;print(json.dumps(r.reconcile_v2(Path(sys.argv[1]))))', str(root)], capture_output=True, timeout=20)
    assert cold.returncode == 0, cold.stderr.decode()
    result = json.loads(cold.stdout)
    assert result["status"] == "RECOVERY_REQUIRED" and result["currentMode"] == "DAMAGED_PACKAGE_FILES"
    assert _fixture_scene(root) == before and all(not p.exists() for p in deleted)
    assert not (root / "recovery/active.json").exists()
    assert recovery._observed_state(root, "data/workspace-packages")["generation"] == preview["currentGeneration"]


@pytest.mark.parametrize("fault", ["owner", "company", "schema", "secret", "foreign_key", "outside", "traversal", "symlink", "hardlink", "unknown", "unreferenced", "extra_package_file", "avatar", "writing", "cg", "music", "store", "root", "version", "tamper"])
def test_damaged_packages_do_not_mask_other_failures(tmp_path, fault):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, "partial")
    if fault in {"owner", "company", "schema", "secret", "foreign_key", "outside", "traversal"}:
        with sqlite3.connect(db) as conn:
            if fault == "owner": conn.execute("update companies set ceo_id='foreign-owner'")
            if fault == "company":
                conn.execute("update companies set company_id='other'")
                conn.execute("update workspaces set company_id='other'")
                conn.execute("update employee_instances set company_id='other'")
            if fault == "schema": conn.execute("create table extra_schema(value text)")
            if fault == "secret":
                conn.execute("create table unsafe(api_key text)"); conn.execute("insert into unsafe values ('self-authored dummy')")
            if fault == "foreign_key":
                conn.execute("create table parents(id integer primary key)")
                conn.execute("create table children(parent_id integer references parents(id))")
                conn.execute("insert into children values (404)")
            if fault == "outside": conn.execute("update installed_workspace_packages set stored_path=?", (str(tmp_path / 'outside'),))
            if fault == "traversal": conn.execute("update installed_workspace_packages set stored_path=?", (str(store / '../outside'),))
    elif fault in {"symlink", "hardlink"}:
        if fault == "symlink": deleted[0].symlink_to(db)
        else: os.link(db, deleted[0])
    elif fault == "unknown": (root / "unreviewed.txt").write_text("synthetic")
    elif fault == "unreferenced": (store / "unreferenced.txt").write_text("synthetic")
    elif fault == "extra_package_file": (deleted[0].parent / "unreviewed.txt").write_text("synthetic")
    elif fault == "avatar": next((root / "data/assets/employee-avatars").rglob("*.png")).unlink()
    elif fault == "writing": (root / "export/writing.json").write_text('{}')
    elif fault == "cg": (root / "export/cg.json").write_text('{"package_type":"unknown"}')
    elif fault == "music": next((root / recovery.MUSIC_TREE).iterdir()).write_bytes(b'invalid audio')
    elif fault == "version":
        # Only the chosen archive metadata is mutated, preserving its digest envelope.
        _rewrite_synthetic_archive(archive, lambda manifest: manifest.update(appVersion="wrong"))
    elif fault in {"root", "store"}:
        _rewrite_synthetic_archive(archive, lambda manifest: manifest.update({"rootBindingSha256" if fault == "root" else "packageStoreRelative": "wrong"}))
    elif fault == "tamper":
        with zipfile.ZipFile(archive, 'a') as bundle: bundle.writestr('unexpected', b'synthetic')
    before, zip_before = _fixture_scene(root), hashlib.sha256(archive.read_bytes()).hexdigest()
    with pytest.raises((ValueError, OSError, sqlite3.DatabaseError)) as caught:
        preflight_v2(root, archive)
    assert not isinstance(caught.value, recovery.PackageFilesDamaged)
    assert _fixture_scene(root) == before and hashlib.sha256(archive.read_bytes()).hexdigest() == zip_before
    assert not (root / "recovery/active.json").exists() and not (root / "recovery/generations").exists()


def _rewrite_synthetic_archive(archive, mutate):
    with zipfile.ZipFile(archive) as bundle:
        members = {name: bundle.read(name) for name in bundle.namelist()}
    manifest = json.loads(members['manifest.json'])
    manifest.pop('contentDigest'); mutate(manifest)
    manifest['contentDigest'] = hashlib.sha256(recovery._canonical(manifest)).hexdigest()
    members['manifest.json'] = recovery._canonical(manifest)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as bundle:
        for name, raw in members.items(): bundle.writestr(name, raw)


@pytest.mark.parametrize("change", ["database", "file", "archive"])
def test_damaged_packages_stale_confirmation_refuses(tmp_path, change):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, "partial")
    preview = preflight_v2(root, archive)
    if change == "database":
        with sqlite3.connect(db) as conn: conn.execute("update truth set value='later'")
    elif change == "file":
        p = root / "export/writing.json"; value = json.loads(p.read_text()); value['title'] = 'later'; p.write_text(json.dumps(value))
    else: _rewrite_synthetic_archive(archive, lambda manifest: manifest.update(createdAt="2026-10-24T00:00:00+00:00"))
    before = _fixture_scene(root)
    with pytest.raises(ValueError, match="stale"):
        restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'])
    assert _fixture_scene(root) == before and not (root / 'recovery/active.json').exists()


@pytest.mark.parametrize("kind", ["full", "partial"])
def test_damaged_packages_backup_and_archive_remain_strict(tmp_path, kind):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, kind)
    with pytest.raises(recovery.PackageFilesDamaged) as caught:
        backup_v2(root, tmp_path / 'must-not-publish.zip')
    assert {x['reason'] for x in caught.value.damage} == ({'PACKAGE_MISSING'} if kind == 'full' else {'PACKAGE_DIGEST_MISMATCH'})
    assert not (tmp_path / 'must-not-publish.zip').exists()
    # Remove an archive member and update every outer integrity field. The inner
    # package digest still has to reject this internally inconsistent archive.
    with zipfile.ZipFile(archive) as bundle: members = {name: bundle.read(name) for name in bundle.namelist()}
    name = deleted[0].relative_to(root).as_posix()
    members.pop(name)
    manifest = json.loads(members['manifest.json']); manifest.pop('contentDigest')
    manifest['files'] = [row for row in manifest['files'] if row['path'] != name]
    manifest['contentDigest'] = hashlib.sha256(recovery._canonical(manifest)).hexdigest()
    members['manifest.json'] = recovery._canonical(manifest)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_STORED) as bundle:
        for name, raw in members.items(): bundle.writestr(name, raw)
    before = _fixture_scene(root)
    with pytest.raises(recovery.PackageFilesDamaged): preflight_v2(root, archive)
    assert _fixture_scene(root) == before


def test_damaged_packages_wal_scene_rollback_and_known_file_damage(tmp_path):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, "partial")
    # Genuine committed WAL/SHM left by a terminated writer, with no live DB user.
    writer = subprocess.run([sys.executable, "-B", "-c", 'import os,sqlite3,sys;c=sqlite3.connect(sys.argv[1]);c.execute("pragma journal_mode=WAL");c.execute("pragma wal_autocheckpoint=0");c.execute("update truth set value=\'after backup in WAL\'");c.commit();os._exit(0)', str(db)], timeout=20)
    assert writer.returncode == 0
    assert db.with_name(db.name + '-wal').is_file() and db.with_name(db.name + '-shm').is_file()
    before = _fixture_scene(root)
    preview = preflight_v2(root, archive)
    assert preview['currentMode'] == 'DAMAGED_PACKAGE_FILES'
    with pytest.raises(RuntimeError):
        restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'], fail_after_files=1)
    assert _fixture_scene(root) == before
    assert all(not p.exists() for p in deleted)


def test_damaged_packages_tampered_safety_refuses_rollback(tmp_path):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, "full")
    preview = preflight_v2(root, archive)
    original = recovery._replace_from
    def stop_after_first(root_path, relative, source, temporary):
        original(root_path, relative, source, temporary)
        raise KeyboardInterrupt('synthetic abrupt stop')
    with patch.object(recovery, '_replace_from', stop_after_first), pytest.raises(KeyboardInterrupt):
        restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'])
    journal = json.loads((root / 'recovery/active.json').read_text())
    safety = root / 'recovery/generations' / journal['safetyId']
    (safety / 'files/data/curis.sqlite').write_bytes(b'synthetic corrupted safety')
    before = _fixture_scene(root)
    assert reconcile_v2(root)['status'] == 'UNKNOWN'
    assert _fixture_scene(root) == before and (root / 'recovery/active.json').exists()


def test_damaged_packages_changed_known_bytes_are_not_claimed_missing(tmp_path):
    root, db, store, archive, rows, deleted = _damaged_package_fixture(tmp_path, "partial")
    deleted[0].write_text('{"type":"modified synthetic schema"}')
    refs = recovery._observed_state(root, 'data/workspace-packages')['refs']
    assert {item['reason'] for item in refs['packageDamage']} == {'PACKAGE_DIGEST_MISMATCH'}
    before = _fixture_scene(root)
    preview = preflight_v2(root, archive)
    with pytest.raises(RuntimeError):
        restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'], fail_after_files=1)
    assert _fixture_scene(root) == before

from desktop.runtime import recovery
from desktop.runtime.recovery import backup, restore, backup_v2, preflight_v2, restore_v2, reconcile_v2, _cold_status, _bounded_json, _pending_work


def isolated_temp():
    return tempfile.TemporaryDirectory(dir=Path(os.environ["CURIS_C03_TEST_ROOT"]))


def make_db(root: Path, value: str) -> Path:
    path = root / "data" / "curis.sqlite"
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("create table truth(value text not null)")
    connection.execute("insert into truth values (?)", (value,))
    connection.execute("pragma user_version = 7")
    connection.commit()
    connection.close()
    return path


def read_value(path: Path) -> str:
    connection = sqlite3.connect(path)
    try:
        return connection.execute("select value from truth").fetchone()[0]
    finally:
        connection.close()


class ReleaseRecoveryTest(unittest.TestCase):
    def test_backup_restore_and_pre_restore_copy(self):
        with isolated_temp() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            archive = root / "curis-backup.zip"
            make_db(source, "accepted")
            manifest = backup(source, archive)
            self.assertEqual(manifest["credentials"], "EXCLUDED_MACOS_KEYCHAIN")
            target_db = make_db(target, "before")
            result = restore(target, archive)
            self.assertEqual(read_value(target_db), "accepted")
            safety = Path(result["safetyCopy"])
            self.assertTrue(safety.is_file())
            self.assertEqual(read_value(safety), "before")

    def test_corrupt_archive_does_not_replace_target(self):
        with isolated_temp() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            archive = root / "curis-backup.zip"
            make_db(source, "accepted")
            target_db = make_db(target, "before")
            backup(source, archive)
            with zipfile.ZipFile(archive, "a") as bundle:
                bundle.writestr("unexpected", "no")
            with self.assertRaises(ValueError):
                restore(target, archive)
            self.assertEqual(read_value(target_db), "before")

    def test_restore_refuses_running_app_lock(self):
        with isolated_temp() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            archive = root / "curis-backup.zip"
            make_db(source, "accepted")
            make_db(target, "before")
            backup(source, archive)
            lock_path = target / "curis-desktop.lock"
            with lock_path.open("a+b") as lock:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaises(RuntimeError):
                    restore(target, archive)


def _package_digest(package: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(path for path in package.rglob("*") if path.is_file()):
        digest.update(file.relative_to(package).as_posix().encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def make_full_root(root: Path, value: str) -> tuple[Path, Path]:
    db = root / "data/curis.sqlite"
    db.parent.mkdir(parents=True)
    avatar = b"PNG fixture bytes"
    avatar_sha = hashlib.sha256(avatar).hexdigest()
    tenant_key = hashlib.sha256(b"selfuse").hexdigest()[:20]
    employee_key = hashlib.sha256(b"employee-1").hexdigest()[:24]
    avatar_path = root / "data/assets/employee-avatars" / tenant_key / employee_key / f"{avatar_sha}.png"
    avatar_path.parent.mkdir(parents=True)
    avatar_path.write_bytes(avatar)
    store = root / "assets/packages"
    package = store / "com.curis.test" / "0.1.0" / "published"
    package.mkdir(parents=True)
    (package / "manifest.json").write_text('{"packageId":"com.curis.test"}')
    (package / "surface.json").write_text('{"title":"fixture"}')
    export = root / "export"; export.mkdir()
    (export / "writing.json").write_text(json.dumps({"schema_version":"writing.local-package/v1","metadata":{"target":"LOCAL_DOWNLOAD"}}))
    conn = sqlite3.connect(db)
    conn.executescript("create table companies(tenant_id text,company_id text,ceo_id text);"
                       "create table workspaces(workspace_id text,tenant_id text,company_id text);"
                       "create table employee_instances(tenant_id text,company_id text,id text,avatar_ref text);"
                       "create table installed_workspace_packages(stored_path text,digest text,status text);"
                       "create table truth(value text);")
    conn.execute("insert into companies values (?,?,?)", ("selfuse", "company-1", "selfuse-ceo"))
    conn.execute("insert into workspaces values (?,?,?)", ("workspace-1", "selfuse", "company-1"))
    conn.execute("insert into employee_instances values (?,?,?,?)", ("selfuse", "company-1", "employee-1", f"asset:{avatar_sha}.png"))
    conn.execute("insert into installed_workspace_packages values (?,?,?)", (str(package), _package_digest(package), "ACTIVE"))
    conn.execute("insert into truth values (?)", (value,))
    conn.execute("pragma user_version=7"); conn.commit(); conn.close()
    return db, store


def make_canonical_initialized_root(root: Path) -> tuple[Path, Path]:
    from backend.app.database import Database
    from backend.app.runtime.ceo_day_service import CeoDayService
    from backend.app.workspace_package_runtime import WorkspacePackageRuntime

    root.mkdir(parents=True)
    db = root / "data/curis.sqlite"
    store = root / "assets/packages"
    store.mkdir(parents=True)
    database = Database(str(db))
    database.initialize()
    WorkspacePackageRuntime(database, store_root=store)
    CeoDayService(database)  # schema initialization only; no scheduler run
    with sqlite3.connect(db) as conn:
        conn.execute(
            "insert into companies(company_id,tenant_id,ceo_id,name) values (?,?,?,?)",
            ("company-1", "selfuse", "selfuse-ceo", "Test company"),
        )
        conn.execute(
            "insert into workspaces(workspace_id,tenant_id,company_id,business_id,name,status) values (?,?,?,?,?,?)",
            ("workspace-1", "selfuse", "company-1", "business-1", "Test workspace", "draft"),
        )
        conn.execute(
            "insert into employee_instances(id,tenant_id,company_id,department_id,template_id,name,role) values (?,?,?,?,?,?,?)",
            ("employee-1", "selfuse", "company-1", "department-1", "template-1", "Test employee", "assistant"),
        )
    return db, store


class FullRecoveryTest(unittest.TestCase):
    @staticmethod
    def _pending_test_restore(raw: str, *, duplicate_export: bool = False):
        root = Path(raw) / "company"; root.mkdir()
        db, store = make_full_root(root, "saved")
        if duplicate_export:
            shutil.copyfile(root / "export/writing.json", root / "export/second.json")
        archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
        with sqlite3.connect(db) as conn:
            conn.execute("update truth set value='current'")
        preview = preflight_v2(root, archive, store)
        with patch("desktop.runtime.recovery.reconcile_v2", return_value={"status": "UNKNOWN"}):
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=1)
        assert result["status"] == "UNKNOWN"
        journal = json.loads((root / "recovery/active.json").read_text())
        safety = root / "recovery/generations" / journal["safetyId"]
        return root, db, store, journal, safety

    @staticmethod
    def _cold_reconcile_child(root: Path, store: Path):
        code = """
import sys
from pathlib import Path
from desktop.runtime.recovery import reconcile_v2
print('ENTER_RECONCILE', flush=True)
print(reconcile_v2(Path(sys.argv[1]), Path(sys.argv[2]))['status'], flush=True)
"""
        child = subprocess.Popen([sys.executable, "-c", code, str(root), str(store)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            try:
                output, errors = child.communicate(timeout=4)
                return child.returncode, output, errors
            except subprocess.TimeoutExpired:
                child.send_signal(signal.SIGTERM)
                output, errors = child.communicate(timeout=10)
                return "TIMED_OUT", output, errors
        finally:
            if child.poll() is None:
                child.kill(); child.communicate(timeout=10)

    def test_strict_atomic_fifo_without_writer_returns_unknown_promptly(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            marker = root / "data" / recovery._atomic_temp_name(journal, "commit", "data/curis.sqlite")
            os.mkfifo(marker, 0o600)
            original = db.read_bytes()
            active = (root / "recovery/active.json").read_bytes()
            safety_db = (safety / "files/data/curis.sqlite").read_bytes()
            code, output, errors = self._cold_reconcile_child(root, store)
            self.assertTrue(stat.S_ISFIFO(marker.lstat().st_mode))
            self.assertEqual(db.read_bytes(), original)
            self.assertEqual((root / "recovery/active.json").read_bytes(), active)
            self.assertEqual((safety / "files/data/curis.sqlite").read_bytes(), safety_db)
            self.assertFalse((root / "recovery/last.json").exists())
            self.assertFalse((safety / "residuals").exists())
            self.assertEqual((code, output.splitlines()), (0, ["ENTER_RECONCILE", "UNKNOWN"]), errors)

    def test_managed_database_fifo_without_writer_returns_unknown_promptly(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            active = (root / "recovery/active.json").read_bytes()
            safety_db = (safety / "files/data/curis.sqlite").read_bytes()
            db.unlink()
            os.mkfifo(db, 0o600)
            code, output, errors = self._cold_reconcile_child(root, store)
            self.assertTrue(stat.S_ISFIFO(db.lstat().st_mode))
            self.assertEqual((root / "recovery/active.json").read_bytes(), active)
            self.assertEqual((safety / "files/data/curis.sqlite").read_bytes(), safety_db)
            self.assertFalse((root / "recovery/last.json").exists())
            self.assertEqual((code, output.splitlines()), (0, ["ENTER_RECONCILE", "UNKNOWN"]), errors)

    def test_unbound_journal_v1_known_prefix_is_not_legacy(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            name = ".curis-restore-" + "f" * 32
            bound = {recovery._atomic_temp_name(journal, phase, path)
                     for phase in ("commit", "rollback")
                     for path in {row["path"] for row in journal["oldRows"] + journal["newRows"]}}
            self.assertNotIn(name, bound)
            marker = root / "data" / name
            marker.write_bytes((safety / "new/data/curis.sqlite").read_bytes()[:100])
            marker.chmod(0o600)
            original = db.read_bytes()
            active = (root / "recovery/active.json").read_bytes()
            safety_db = (safety / "files/data/curis.sqlite").read_bytes()
            self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertEqual(marker.read_bytes(), (safety / "new/data/curis.sqlite").read_bytes()[:100])
            self.assertEqual(db.read_bytes(), original)
            self.assertEqual((root / "recovery/active.json").read_bytes(), active)
            self.assertEqual((safety / "files/data/curis.sqlite").read_bytes(), safety_db)
            self.assertFalse((root / "recovery/last.json").exists())
            self.assertFalse((safety / "residuals").exists())

    def test_explicit_null_atomic_scheme_is_not_legacy(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            journal["atomicTempScheme"] = None
            journal["atomicTempNonce"] = None
            active_path = root / "recovery/active.json"
            active_path.write_text(json.dumps(journal))
            marker = root / "data" / (".curis-restore-" + "e" * 32)
            marker.write_bytes((safety / "new/data/curis.sqlite").read_bytes()[:100])
            marker.chmod(0o600)
            active = active_path.read_bytes()
            original = db.read_bytes()
            self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertEqual(active_path.read_bytes(), active)
            self.assertEqual(db.read_bytes(), original)
            self.assertTrue(marker.is_file())
            self.assertFalse((root / "recovery/last.json").exists())

    def test_sigterm_partial_atomic_copy_cold_rollback_preserves_residual(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            with sqlite3.connect(db) as conn:
                conn.execute("update truth set value='current'")
            preview = preflight_v2(root, archive, store)
            code = """
import os, signal, sys
from pathlib import Path
from unittest.mock import patch
from desktop.runtime import recovery
root, archive, sha, generation, store = sys.argv[1:]
original = recovery.shutil.copyfileobj
def interrupt_copy(source, target, length=0):
    if (Path(root) / 'recovery/active.json').exists():
        target.write(source.read(100))
        target.flush(); os.fsync(target.fileno())
        print('PARTIAL_WRITTEN', flush=True)
        signal.pause()
    return original(source, target, length)
with patch.object(recovery.shutil, 'copyfileobj', interrupt_copy):
    recovery.restore_v2(Path(root), Path(archive), sha, generation, Path(store))
"""
            child = subprocess.Popen(
                [sys.executable, "-c", code, str(root), str(archive), preview["archiveSha256"],
                 preview["currentGeneration"], str(store)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            try:
                ready, _, _ = select.select([child.stdout], [], [], 15)
                self.assertTrue(ready, "isolated child never reached partial atomic copy")
                self.assertEqual(child.stdout.readline().strip(), "PARTIAL_WRITTEN")
                child.send_signal(signal.SIGTERM)
                self.assertEqual(child.wait(timeout=10), -signal.SIGTERM)
            finally:
                if child.poll() is None:
                    child.kill(); child.wait(timeout=10)
                child.communicate(timeout=10)
            self.assertTrue((root / "recovery/active.json").is_file())
            self.assertFalse((root / "recovery/last.json").exists())
            self.assertEqual(len(list(root.rglob(".curis-restore-*"))), 1)
            self.assertEqual(reconcile_v2(root, store)["status"], "ROLLED_BACK")
            self.assertEqual(read_value(db), "current")
            self.assertFalse((root / "recovery/active.json").exists())
            self.assertTrue((root / "recovery/last.json").is_file())
            self.assertEqual(len(list((root / "recovery/generations").rglob("residuals/*.bin"))), 1)
            self.assertEqual(len(list((root / "recovery/generations").rglob("residuals/*.json"))), 1)

    def test_legacy_partial_copy_and_interrupted_evidence_link_are_idempotent(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            journal.pop("atomicTempScheme"); journal.pop("atomicTempNonce")
            (root / "recovery/active.json").write_text(json.dumps(journal))
            marker = root / "export" / (".curis-restore-" + "a" * 32)
            marker.write_bytes((safety / "new/export/writing.json").read_bytes()[:30])
            marker.chmod(0o600)
            original_unlink = recovery.os.unlink
            def interrupt_unlink(path, *args, **kwargs):
                if path == marker.name:
                    raise RuntimeError("isolated link-before-unlink interruption")
                return original_unlink(path, *args, **kwargs)
            with patch("desktop.runtime.recovery.os.unlink", side_effect=interrupt_unlink):
                self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertEqual(marker.stat().st_nlink, 2)
            self.assertEqual(len(list(safety.glob("residuals/*.json"))), 1)
            self.assertEqual(reconcile_v2(root, store)["status"], "ROLLED_BACK")
            self.assertEqual(read_value(db), "current")
            self.assertFalse(marker.exists())
            self.assertEqual(len(list(safety.glob("residuals/*.bin"))), 1)
            self.assertEqual(_cold_status(root, store)["status"], "ROLLED_BACK")

    def test_rollback_phase_partial_copy_recovers_again(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            temporary = recovery._atomic_temp_name(journal, "rollback", "data/curis.sqlite")
            original_replace = recovery._replace_from
            def interrupt_rollback(root_path, relative, source, temp_name):
                if relative == "data/curis.sqlite":
                    marker = root_path / "data" / temp_name
                    marker.write_bytes(source.read_bytes()[:100])
                    marker.chmod(0o600)
                    raise RuntimeError("isolated second interruption")
                return original_replace(root_path, relative, source, temp_name)
            with patch("desktop.runtime.recovery._replace_from", side_effect=interrupt_rollback):
                self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertTrue((root / "data" / temporary).exists())
            self.assertEqual(reconcile_v2(root, store)["status"], "ROLLED_BACK")
            self.assertEqual(read_value(db), "current")
            self.assertEqual(len(list(safety.glob("residuals/*.bin"))), 1)

    def test_exact_journal_zero_copy_and_legacy_shared_prefix_boundary(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            marker = root / "data" / recovery._atomic_temp_name(journal, "commit", "data/curis.sqlite")
            marker.write_bytes(b""); marker.chmod(0o600)
            self.assertEqual(reconcile_v2(root, store)["status"], "ROLLED_BACK")
            self.assertEqual(len(list(safety.glob("residuals/*.bin"))), 1)
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw, duplicate_export=True)
            journal.pop("atomicTempScheme"); journal.pop("atomicTempNonce")
            (root / "recovery/active.json").write_text(json.dumps(journal))
            marker = root / "export" / (".curis-restore-" + "c" * 32)
            marker.write_bytes((safety / "new/export/writing.json").read_bytes()[:30])
            marker.chmod(0o600)
            original = marker.read_bytes()
            self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertEqual(marker.read_bytes(), original)
            self.assertTrue((root / "recovery/active.json").exists())
            self.assertFalse((root / "recovery/last.json").exists())

    def test_foreign_zero_link_and_cross_volume_residuals_fail_closed(self):
        for kind in ("foreign", "zero", "symlink", "hardlink", "cross-volume"):
            with self.subTest(kind=kind), isolated_temp() as raw:
                root, db, store, journal, safety = self._pending_test_restore(raw)
                if kind == "zero":
                    journal.pop("atomicTempScheme"); journal.pop("atomicTempNonce")
                    (root / "recovery/active.json").write_text(json.dumps(journal))
                    name = ".curis-restore-" + "b" * 32
                else:
                    name = recovery._atomic_temp_name(journal, "commit", "data/curis.sqlite")
                marker = root / "data" / name
                if kind == "symlink":
                    marker.symlink_to(db)
                elif kind == "hardlink":
                    linked_source = Path(raw) / "linked-source"
                    linked_source.write_bytes((safety / "new/data/curis.sqlite").read_bytes()[:100])
                    linked_source.chmod(0o600)
                    os.link(linked_source, marker)
                elif kind in {"foreign", "zero"}:
                    marker.write_bytes(b"not a staged source" if kind == "foreign" else b"")
                else:
                    marker.write_bytes((safety / "new/data/curis.sqlite").read_bytes()[:100])
                if not marker.is_symlink(): marker.chmod(0o600)
                before = marker.read_bytes()
                if kind == "cross-volume":
                    with patch("desktop.runtime.recovery.os.link", side_effect=OSError(errno.EXDEV, "cross-volume")) as link:
                        result = reconcile_v2(root, store)
                    link.assert_called_once()
                else:
                    result = reconcile_v2(root, store)
                self.assertEqual(result["status"], "UNKNOWN")
                self.assertTrue((root / "recovery/active.json").is_file())
                self.assertFalse((root / "recovery/last.json").exists())
                self.assertEqual(marker.read_bytes(), before)

    def test_unknown_atomic_scheme_keeps_active_journal_and_safety(self):
        with isolated_temp() as raw:
            root, db, store, journal, safety = self._pending_test_restore(raw)
            journal["atomicTempScheme"] = "unreviewed"
            (root / "recovery/active.json").write_text(json.dumps(journal))
            before = db.read_bytes()
            self.assertEqual(reconcile_v2(root, store)["status"], "UNKNOWN")
            self.assertEqual(db.read_bytes(), before)
            self.assertTrue((root / "recovery/active.json").is_file())
            self.assertTrue((safety / "files/data/curis.sqlite").is_file())
            self.assertFalse((root / "recovery/last.json").exists())

    def test_missing_active_database_restores_original_company_workspace_employee(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            db.unlink()
            self.assertEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")
            preview = preflight_v2(root, archive, store)
            self.assertEqual(preview["currentMode"], "MISSING_DB")
            self.assertIn("受损/缺失", preview["impact"])
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RESTORED")
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("select tenant_id,company_id,ceo_id from companies").fetchone(), ("selfuse", "company-1", "selfuse-ceo"))
                self.assertEqual(conn.execute("select workspace_id from workspaces").fetchone(), ("workspace-1",))
                self.assertEqual(conn.execute("select id from employee_instances").fetchone(), ("employee-1",))
            self.assertNotEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")

    def test_damaged_active_database_restore_and_failed_restore_preserve_raw_scene(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            damaged = b"not a SQLite database; raw prior bytes"
            db.write_bytes(damaged)
            sidecar = db.with_name(db.name + "-wal"); sidecar.write_bytes(b"prior WAL bytes")
            self.assertEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")
            preview = preflight_v2(root, archive, store)
            self.assertEqual(preview["currentMode"], "DAMAGED_DB")
            with self.assertRaises(RuntimeError):
                restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=1)
            self.assertEqual(db.read_bytes(), damaged)
            self.assertEqual(sidecar.read_bytes(), b"prior WAL bytes")
            self.assertEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")
            preview = preflight_v2(root, archive, store)
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RESTORED")
            self.assertEqual(read_value(db), "saved")
            self.assertFalse(sidecar.exists())

    def test_missing_database_failed_restore_preserves_exact_absence(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            db.unlink()
            preview = preflight_v2(root, archive, store)
            with self.assertRaises(RuntimeError):
                restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=1)
            self.assertFalse(db.exists())
            self.assertEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")

    def test_same_owner_can_restore_prior_workspace_and_employee_roster(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            original = Path(raw) / "original.zip"; backup_v2(root, original, store)
            with sqlite3.connect(db) as conn:
                conn.execute("insert into workspaces values (?,?,?)", ("workspace-2", "selfuse", "company-1"))
                conn.execute("insert into employee_instances values (?,?,?,?)", ("selfuse", "company-1", "employee-2", ""))
            self.assertNotEqual(_cold_status(root, store)["status"], "RECOVERY_REQUIRED")
            backup_v2(root, Path(raw) / "later.zip", store)
            preview = preflight_v2(root, original, store)
            result = restore_v2(root, original, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RESTORED")
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("select workspace_id from workspaces order by workspace_id").fetchall(), [("workspace-1",)])
                self.assertEqual(conn.execute("select id from employee_instances order by id").fetchall(), [("employee-1",)])

    def test_unknown_keeps_both_complete_generations_and_tampered_safety_never_rolls_back(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            with sqlite3.connect(db) as conn: conn.execute("update truth set value='current'")
            preview = preflight_v2(root, archive, store)
            with patch("desktop.runtime.recovery.reconcile_v2", return_value={"status": "UNKNOWN"}):
                result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=1)
            self.assertEqual(result["status"], "UNKNOWN")
            safety = root / "recovery/generations" / result["safetyGeneration"]
            self.assertTrue((safety / "files/data/curis.sqlite").is_file())
            self.assertTrue((safety / "new/data/curis.sqlite").is_file())
            safety_file = safety / "files/export/writing.json"
            safety_file.write_text("tampered")
            before = db.read_bytes()
            self.assertEqual(reconcile_v2(root)["status"], "UNKNOWN")
            self.assertEqual(db.read_bytes(), before)
            self.assertTrue((root / "recovery/active.json").is_file())

    def test_schema_and_structured_secret_and_zip_header_fail_closed(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            with patch("desktop.runtime.recovery.APP_VERSION", "different-build"):
                with self.assertRaisesRegex(ValueError, "lineage"):
                    preflight_v2(root, archive, store)
            with sqlite3.connect(db) as conn: conn.execute("alter table truth add column changed_shape text")
            with self.assertRaisesRegex(ValueError, "current Company or schema"):
                preflight_v2(root, archive, store)
            with sqlite3.connect(db) as conn:
                conn.execute("alter table truth add column detail_json text")
                conn.execute("update truth set detail_json=?", ('{"nested":{"access_token":"fixture-only"}}',))
            with self.assertRaisesRegex(ValueError, "structured secret"):
                backup_v2(root, Path(raw) / "secret.zip", store)
            with sqlite3.connect(db) as conn: conn.execute("update truth set detail_json=?", ('{"safe":1,"safe":2}',))
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                backup_v2(root, Path(raw) / "duplicate.zip", store)
            with sqlite3.connect(db) as conn: conn.execute("update truth set detail_json='{}'")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                _bounded_json(b'{"format":"one","format":"two"}')
            header = Path(raw) / "bad-count.zip"
            data = bytearray(archive.read_bytes()); marker = data.rfind(b"PK\x05\x06")
            self.assertGreater(marker, 0)
            data[marker + 10:marker + 12] = (65000).to_bytes(2, "little")
            header.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "central entry count"):
                preflight_v2(root, header, store)

    def test_canonical_migrated_credential_reference_backup_and_unknowns(self):
        with isolated_temp() as raw:
            root = Path(raw) / "canonical"
            db, store = make_canonical_initialized_root(root)
            with sqlite3.connect(db) as conn:
                columns = {row[1] for row in conn.execute('pragma table_info("credential_metadata")')}
                self.assertEqual(columns, {
                    "credential_id", "tenant_id", "name", "provider", "credential_type",
                    "credential_ref", "status", "encrypted_metadata", "created_at",
                    "updated_at", "disabled_at", "account_id",
                })
                self.assertEqual(conn.execute("select count(*) from credential_metadata").fetchone()[0], 0)
            empty = Path(raw) / "canonical-empty.zip"
            self.assertEqual(backup_v2(root, empty, store)["status"], "BACKUP_VERIFIED")
            self.assertEqual(preflight_v2(root, empty, store)["status"], "PREFLIGHT_OK")

            with sqlite3.connect(db) as conn:
                conn.execute(
                    "insert into credential_metadata "
                    "(credential_id,tenant_id,name,provider,credential_type,credential_ref,account_id,encrypted_metadata) "
                    "values (?,?,?,?,?,?,?,?)",
                    ("credential-1", "selfuse", "Test reference", "test-provider", "reference",
                     "keychain:test-only-ref", "account-1",
                     json.dumps({"backend": "macos-keychain", "secret_digest": hashlib.sha256(b"synthetic").hexdigest()})),
                )
            metadata_only = Path(raw) / "canonical-metadata.zip"
            self.assertEqual(backup_v2(root, metadata_only, store)["status"], "BACKUP_VERIFIED")
            self.assertEqual(preflight_v2(root, metadata_only, store)["status"], "PREFLIGHT_OK")

            with sqlite3.connect(db) as conn:
                conn.execute("alter table credential_metadata add column future_field text")
            unknown = Path(raw) / "unknown-column.zip"
            with self.assertRaisesRegex(ValueError, "unreviewed credential metadata schema"):
                backup_v2(root, unknown, store)
            self.assertFalse(unknown.exists())

            with sqlite3.connect(db) as conn:
                conn.execute("alter table credential_metadata add column api_key text")
                conn.execute("update credential_metadata set api_key='synthetic-only'")
            raw_secret = Path(raw) / "raw-secret.zip"
            with self.assertRaisesRegex(ValueError, "forbidden secret-shaped database field"):
                backup_v2(root, raw_secret, store)
            self.assertFalse(raw_secret.exists())

    def test_legacy_eleven_credential_columns_still_allowed_but_empty_unknown_denied(self):
        with isolated_temp() as raw:
            root = Path(raw) / "legacy"; root.mkdir()
            db, store = make_full_root(root, "saved")
            with sqlite3.connect(db) as conn:
                conn.execute(
                    "create table credential_metadata ("
                    "credential_id text primary key, tenant_id text not null, name text not null, "
                    "provider text not null, credential_type text not null, credential_ref text not null, "
                    "status text not null, encrypted_metadata text not null, created_at text, "
                    "updated_at text, disabled_at text)"
                )
            legacy = Path(raw) / "legacy.zip"
            self.assertEqual(backup_v2(root, legacy, store)["status"], "BACKUP_VERIFIED")
            with sqlite3.connect(db) as conn:
                conn.execute("alter table credential_metadata add column unreviewed_future text")
            unknown = Path(raw) / "empty-unknown.zip"
            with self.assertRaisesRegex(ValueError, "unreviewed credential metadata schema"):
                backup_v2(root, unknown, store)
            self.assertFalse(unknown.exists())

    def test_v2_same_root_db_avatar_package_export_and_rollback(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"
            created = backup_v2(root, archive, store)
            self.assertEqual(created["status"], "BACKUP_VERIFIED")
            self.assertEqual(created["files"], 5)
            with sqlite3.connect(db) as conn: conn.execute("update truth set value='current'")
            preview = preflight_v2(root, archive, store)
            self.assertEqual(preview["status"], "PREFLIGHT_OK")
            with self.assertRaises(RuntimeError):
                restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=2)
            self.assertEqual(read_value(db), "current")
            self.assertEqual(reconcile_v2(root)["status"], "ROLLED_BACK")
            preview = preflight_v2(root, archive, store)
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RESTORED")
            self.assertEqual(read_value(db), "saved")
            self.assertTrue((root / "export/writing.json").is_file())
            self.assertEqual(result["resumeCheck"], "PENDING_NO_REPLAY")

    def test_v1_is_not_full_and_tamper_stale_and_unknown_file_refuse(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            legacy = Path(raw) / "legacy.zip"; backup(root, legacy)
            with self.assertRaises(ValueError): preflight_v2(root, legacy, store)
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            before = preflight_v2(root, archive, store)
            with sqlite3.connect(db) as conn: conn.execute("update truth set value='changed'")
            with self.assertRaises(ValueError): restore_v2(root, archive, before["archiveSha256"], before["currentGeneration"], store)
            self.assertEqual(read_value(db), "changed")
            with zipfile.ZipFile(archive, "a") as bundle: bundle.writestr("../escape", b"not allowed")
            with self.assertRaises(ValueError): preflight_v2(root, archive, store)
            self.assertEqual(read_value(db), "changed")
            (root / "unknown-user-file").write_text("unclassified")
            with self.assertRaises(ValueError): backup_v2(root, Path(raw) / "blocked.zip", store)
            self.assertFalse((Path(raw) / "blocked.zip").exists())

    def test_external_package_store_and_full_safety_retention_refuse(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            _, store = make_full_root(root, "saved")
            with self.assertRaises(ValueError): backup_v2(root, Path(raw) / "outside.zip", Path(raw) / "external")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            preview = preflight_v2(root, archive, store)
            generations = root / "recovery/generations"; generations.mkdir()
            for index in range(8): (generations / f"held-{index}").mkdir()
            with self.assertRaises(ValueError): restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(len(list(generations.iterdir())), 8)

    def test_bad_zip_type_ratio_missing_reference_space_and_secret_field_refuse(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            with patch("desktop.runtime.recovery.shutil.disk_usage", return_value=type("Usage", (), {"free": 1})()):
                with self.assertRaisesRegex(ValueError, "insufficient space"):
                    preflight_v2(root, archive, store)
            symlink = Path(raw) / "link.zip"
            with zipfile.ZipFile(archive) as source, zipfile.ZipFile(symlink, "w") as target:
                for item in source.infolist(): target.writestr(item, source.read(item.filename))
                item = zipfile.ZipInfo("export/link.json"); item.create_system = 3
                item.external_attr = (0o120777 << 16)
                target.writestr(item, "outside")
            with self.assertRaises(ValueError): preflight_v2(root, symlink, store)
            bomb = Path(raw) / "bomb.zip"
            with zipfile.ZipFile(archive) as source, zipfile.ZipFile(bomb, "w", compression=zipfile.ZIP_DEFLATED) as target:
                for item in source.infolist(): target.writestr(item.filename, source.read(item.filename))
                target.writestr("export/bomb.json", b"0" * 1024 * 1024)
            with self.assertRaises(ValueError): preflight_v2(root, bomb, store)
            avatar = next((root / "data/assets/employee-avatars").rglob("*.png"))
            avatar.unlink()
            with self.assertRaises(ValueError): backup_v2(root, Path(raw) / "missing.zip", store)
            avatar.write_bytes(b"PNG fixture bytes")
            with sqlite3.connect(db) as conn:
                conn.execute("alter table truth add column api_key text")
                conn.execute("update truth set api_key='fixture-only'")
            with self.assertRaisesRegex(ValueError, "secret-shaped"):
                backup_v2(root, Path(raw) / "secret.zip", store)
            self.assertFalse((Path(raw) / "secret.zip").exists())

    def test_reconnect_metadata_never_executes_a_pending_effect(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            with sqlite3.connect(db) as conn:
                conn.execute("create table pending_effect(effect_id text,status text)")
                conn.execute("insert into pending_effect values ('effect-1','UNKNOWN')")
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            preview = preflight_v2(root, archive, store)
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RECOVERY_HOLD")
            self.assertEqual(result["resumeCheck"], "PENDING_NO_REPLAY")
            self.assertEqual(reconcile_v2(root)["status"], "RECOVERY_HOLD")
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute("select effect_id,status from pending_effect").fetchall(), [("effect-1", "UNKNOWN")])

    def test_actual_task_and_conversation_attempts_use_latest_terminal_effect(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, "saved")
            with sqlite3.connect(db) as conn:
                conn.execute("create table tasks(task_id text,status text)")
                conn.execute("create table evolution_events(event_id integer primary key,event_type text,payload text)")
                conn.execute("insert into tasks values ('task-1','AWAITING_INPUT')")
            self.assertTrue(_pending_work(db))
            with sqlite3.connect(db) as conn:
                conn.execute("update tasks set status='HUMAN_HANDOFF'")
            self.assertTrue(_pending_work(db))
            with sqlite3.connect(db) as conn:
                conn.execute("update tasks set status='COMPLETED'")
                conn.execute("insert into evolution_events(event_type,payload) values (?,?)",
                             ("conversation.attempt.started", json.dumps({"attempt_id": "a", "status": "RUNNING", "execution_selection": {"purpose": "CONVERSATION_REPLY"}})))
            self.assertTrue(_pending_work(db))
            with sqlite3.connect(db) as conn:
                conn.execute("insert into evolution_events(event_type,payload) values (?,?)",
                             ("conversation.attempt.finished", json.dumps({"attempt_id": "a", "status": "COMPLETED", "effect_status": "SETTLED", "execution_selection": {"purpose": "CONVERSATION_REPLY"}})))
            self.assertFalse(_pending_work(db), "old RUNNING claim was settled by its latest finish")
            with sqlite3.connect(db) as conn:
                conn.execute("insert into evolution_events(event_type,payload) values (?,?)",
                             ("conversation.attempt.finished", json.dumps({"attempt_id": "b", "status": "UNVERIFIED", "effect_status": "UNKNOWN", "execution_selection": {"purpose": "CONVERSATION_REPLY"}})))
            self.assertTrue(_pending_work(db))
            archive = Path(raw) / "full.zip"; backup_v2(root, archive, store)
            preview = preflight_v2(root, archive, store)
            result = restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)
            self.assertEqual(result["status"], "RECOVERY_HOLD")
            self.assertEqual(reconcile_v2(root)["status"], "RECOVERY_HOLD")

    def test_final_published_archive_is_read_back_before_verified_receipt(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            _, store = make_full_root(root, "saved")
            good = Path(raw) / "good.zip"
            created = backup_v2(root, good, store)
            self.assertEqual(created["status"], "BACKUP_VERIFIED")
            self.assertEqual(created["archiveSha256"], hashlib.sha256(good.read_bytes()).hexdigest())
            self.assertEqual(preflight_v2(root, good, store)["createdAt"], created["createdAt"])
            damaged = Path(raw) / "damaged.zip"
            original_link = os.link
            def corrupt_after_publish(*args, **kwargs):
                original_link(*args, **kwargs)
                with damaged.open("r+b") as published:
                    published.truncate(32)
            with patch("desktop.runtime.recovery.os.link", side_effect=corrupt_after_publish):
                with self.assertRaises((ValueError, zipfile.BadZipFile)):
                    backup_v2(root, damaged, store)
            self.assertTrue(damaged.is_file(), "retain the failed published bytes as evidence")
            with self.assertRaises((ValueError, zipfile.BadZipFile)):
                preflight_v2(root, damaged, store)
            replaced = Path(raw) / "replaced.zip"
            def replace_after_publish(source_name, target_name, **kwargs):
                original_link(source_name, target_name, **kwargs)
                replaced.unlink()
                shutil.copyfile(replaced.parent / source_name, replaced)
            with patch("desktop.runtime.recovery.os.link", side_effect=replace_after_publish):
                with self.assertRaisesRegex(ValueError, "identity changed"):
                    backup_v2(root, replaced, store)
            self.assertEqual(preflight_v2(root, replaced, store)["status"], "PREFLIGHT_OK")

    def test_known_json_payload_columns_reject_nested_secret_keys_only(self):
        with isolated_temp() as raw:
            root = Path(raw) / "company"; root.mkdir()
            db, store = make_full_root(root, '{"api_key":"ordinary user prose"}')
            with sqlite3.connect(db) as conn:
                conn.execute("create table evolution_events(event_id integer primary key,event_type text,payload text)")
                conn.execute("create table agent_wakeup_requests(request_id text,payload text)")
                conn.execute("insert into evolution_events(event_type,payload) values (?,?)",
                             ("conversation.message", json.dumps({"message_id": "m", "body": "ordinary user text"})))
                conn.execute("insert into agent_wakeup_requests values (?,?)", ("wake", json.dumps({"context": {"task": "ok"}})))
            self.assertEqual(backup_v2(root, Path(raw) / "ordinary.zip", store)["status"], "BACKUP_VERIFIED")
            with sqlite3.connect(db) as conn:
                conn.execute("update evolution_events set payload=?", (json.dumps({"context": [{"api_key": "synthetic"}]}),))
            with self.assertRaisesRegex(ValueError, "forbidden structured secret key"):
                backup_v2(root, Path(raw) / "secret-event.zip", store)
            with sqlite3.connect(db) as conn:
                conn.execute("update evolution_events set payload=?", (json.dumps({"message_id": "m"}),))
                conn.execute("update agent_wakeup_requests set payload=?", (json.dumps({"nested": {"refresh_token": "synthetic"}}),))
            with self.assertRaisesRegex(ValueError, "forbidden structured secret key"):
                backup_v2(root, Path(raw) / "secret-wake.zip", store)
            with sqlite3.connect(db) as conn:
                conn.execute("update agent_wakeup_requests set payload=?", ('{"task":"one","task":"two"}',))
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                backup_v2(root, Path(raw) / "duplicate-payload.zip", store)
            deep = {"leaf": "ok"}
            for _ in range(26):
                deep = {"layer": deep}
            with sqlite3.connect(db) as conn:
                conn.execute("update agent_wakeup_requests set payload=?", (json.dumps({"nested": {"ok": True}}),))
                conn.execute("update evolution_events set payload=?", (json.dumps(deep),))
            with self.assertRaisesRegex(ValueError, "nesting exceeds bound"):
                backup_v2(root, Path(raw) / "deep-payload.zip", store)


if __name__ == "__main__":
    unittest.main()


def cg_export_fixture():
    return {
        "package_type": "curis.cg.local-verification-export/1", "verification_ref": "cg-verify-synthetic",
        "exported_at": "2026-10-23T00:00:00+00:00", "title": "合成核验标题", "body": "自行编写的隔离测试正文",
        "format": "article", "platform": {"ref": "xhs", "name": "小红书"},
        "account": {"ref": "cg-account-synthetic", "name": "测试账号"},
        "checks": [{"key": "copyright", "label": "素材权利", "checked": False, "note": "人工核对"}],
        "connection_status": "NOT_CONNECTED", "verification": "UNVERIFIED", "source": "CEO_MANUAL",
        "notice": "本地核验导出，不构成发布；平台连接不存在。",
    }


def test_cg_export_writing_wav_full_backup_restore_and_rollback(tmp_path):
    import io
    import wave
    root = tmp_path / "profile"
    db, store = make_full_root(root, "original")
    cg = root / "export/cg.json"
    cg.write_text(json.dumps(cg_export_fixture(), ensure_ascii=False))
    audio = io.BytesIO()
    with wave.open(audio, "wb") as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(8000); wav.writeframes(b"\x00\x00" * 800)
    wav_bytes = audio.getvalue()
    wav_path = root / recovery.MUSIC_TREE / (hashlib.sha256(wav_bytes).hexdigest() + ".wav")
    wav_path.parent.mkdir(parents=True); wav_path.write_bytes(wav_bytes)
    expected = {p.relative_to(root).as_posix(): p.read_bytes() for p in (cg, root / "export/writing.json", wav_path)}
    archive = tmp_path / "complete.zip"
    assert backup_v2(root, archive, store)["status"] == "BACKUP_VERIFIED"
    with zipfile.ZipFile(archive) as bundle:
        rows = {r["path"]: r for r in json.loads(bundle.read("manifest.json"))["files"]}
        for name, raw in expected.items():
            assert bundle.read(name) == raw
            assert rows[name]["sha256"] == hashlib.sha256(raw).hexdigest()
    with sqlite3.connect(db) as con: con.execute("update truth set value='later'")
    changed = cg_export_fixture(); changed["body"] = "后续正文"
    cg.write_text(json.dumps(changed))
    (root / "export/writing.json").write_text(json.dumps({"schema_version": "writing.local-package/v1", "metadata": {"target": "LOCAL_DOWNLOAD"}, "title": "后续 Writing"}))
    before = recovery._generation(root, "assets/packages")[2]
    preview = preflight_v2(root, archive, store)
    with pytest.raises(RuntimeError):
        restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store, fail_after_files=2)
    assert reconcile_v2(root)["status"] == "ROLLED_BACK"
    assert recovery._generation(root, "assets/packages")[2] == before
    preview = preflight_v2(root, archive, store)
    assert restore_v2(root, archive, preview["archiveSha256"], preview["currentGeneration"], store)["status"] == "RESTORED"
    assert read_value(db) == "original"
    for name, raw in expected.items():
        assert (root / name).read_bytes() == raw
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == hashlib.sha256(raw).hexdigest()


@pytest.mark.parametrize("field,value", [
    ("package_type", "curis.cg.local-verification-export/2"), ("package_type", "arbitrary"),
    ("notice", "已发布"), ("verification", "VERIFIED"), ("source", "EMPLOYEE"),
    ("connection_status", "CONNECTED"), ("verification_ref", "foreign"), ("verification_ref", "x" * 257),
    ("exported_at", ""), ("exported_at", "x" * 129), ("title", {}), ("body", []), ("format", 1),
    ("account", {"ref": "cg-account-x", "name": "test", "api_key": "synthetic"}),
    ("account", {"ref": "foreign", "name": "test"}), ("account", {"ref": "cg-account-x", "name": ""}),
    ("platform", {"ref": "unknown", "name": "test"}), ("platform", []),
    ("checks", []), ("checks", {}),
    ("checks", [{"key": "one", "label": "label", "checked": 1, "note": ""}]),
    ("checks", [{"key": "one", "label": "label", "checked": False, "note": {"password": "synthetic"}}]),
    ("checks", [{"key": "one", "label": "label", "checked": True, "note": ""}] * 2),
    ("checks", [{"key": str(n), "label": "label", "checked": True, "note": ""} for n in range(65)]),
    ("api_key", "synthetic"), ("schema_version", "writing.local-package/v1"),
])
def test_cg_export_invalid_contract_refuses_complete_backup(tmp_path, field, value):
    root = tmp_path / "profile"; db, store = make_full_root(root, "original")
    payload = cg_export_fixture(); payload[field] = value
    (root / "export/cg.json").write_text(json.dumps(payload))
    before = db.read_bytes(); archive = tmp_path / "refused.zip"
    with pytest.raises(ValueError, match="CG export"):
        backup_v2(root, archive, store)
    assert db.read_bytes() == before and not archive.exists()


@pytest.mark.parametrize("bad", ["missing", "unknown-version", "secret", "duplicate-key", "corrupt", "oversize"])
def test_cg_export_invalid_archive_refuses_preflight_with_valid_hashes(tmp_path, bad):
    root = tmp_path / "profile"; db, store = make_full_root(root, "original")
    cg = root / "export/cg.json"; cg.write_text(json.dumps(cg_export_fixture()))
    valid = tmp_path / "valid.zip"; backup_v2(root, valid, store)
    with zipfile.ZipFile(valid) as bundle: members = {n: bundle.read(n) for n in bundle.namelist()}
    payload = cg_export_fixture()
    if bad == "missing": del payload["notice"]
    if bad == "unknown-version": payload["package_type"] = "curis.cg.local-verification-export/2"
    if bad == "secret": payload["checks"][0]["access_token"] = "synthetic"
    raw = json.dumps(payload).encode()
    if bad == "duplicate-key": raw = raw[:-1] + b', "notice": "duplicate"}'
    if bad == "corrupt": raw = b'{'
    if bad == "oversize": raw += b' ' * (2 * 1024 * 1024)
    manifest = json.loads(members["manifest.json"])
    for row in manifest["files"]:
        if row["path"] == "export/cg.json": row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    del manifest["contentDigest"]
    manifest["contentDigest"] = hashlib.sha256(recovery._canonical(manifest)).hexdigest()
    members["manifest.json"] = recovery._canonical(manifest); members["export/cg.json"] = raw
    archive = tmp_path / "invalid.zip"
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_STORED) as bundle:
        for name, body in members.items(): bundle.writestr(name, body)
    before = recovery._generation(root, "assets/packages")[2]
    with pytest.raises(ValueError): preflight_v2(root, archive, store)
    assert recovery._generation(root, "assets/packages")[2] == before


def test_music_user_wav_backup_restore_and_failed_restore_preserve(tmp_path, monkeypatch):
    from backend.tests.test_music_local_import import local_setup, scope, create, wav, upload, finish, COMPANY
    root, db, runtime, w, service = local_setup(tmp_path, monkeypatch)
    with scope(): row = finish(service, w, upload(service, w, create(service, w), wav()))
    store = root / 'assets/packages'; archive = tmp_path / 'music.zip'
    backup_v2(root, archive, store)
    with zipfile.ZipFile(archive) as bundle:
        manifest = json.loads(bundle.read('manifest.json'))
        assert len(manifest['musicRefs']) == 1
        assert manifest['musicRefs'][0]['asset_ref'] == row['assets'][0]['entity_id']
    with scope():
        service.command(COMPANY, w, row['song']['entity_id'], 'save-lyrics', request_id='later', expected={'lyrics_ref':row['lyrics']['entity_id']}, data={'text':'更新但不改成品','draft_revision':'v2'})
    before = recovery._generation(root, 'assets/packages')[2]
    preview = preflight_v2(root, archive, store)
    with pytest.raises(RuntimeError): restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'], store, fail_after_files=2)
    assert reconcile_v2(root)['status'] == 'ROLLED_BACK'
    assert recovery._generation(root, 'assets/packages')[2] == before
    preview = preflight_v2(root, archive, store)
    assert restore_v2(root, archive, preview['archiveSha256'], preview['currentGeneration'], store)['status'] == 'RESTORED'
    with scope(), db.connect() as con:
        assert service.content(COMPANY,w,row['song']['entity_id'])['master'] == row['master']
        raw,status,_ = service.media.read(con,COMPANY,w,row['song']['entity_id'],row['assets'][0]['entity_id'])
        assert raw == wav() and status == 200


def test_music_inventory_rejects_missing_tampered_foreign_and_links(tmp_path, monkeypatch):
    from backend.tests.test_music_local_import import local_setup, scope, create, wav, upload
    root, db, runtime, w, service = local_setup(tmp_path, monkeypatch)
    with scope(): row=upload(service,w,create(service,w),wav())
    target=service.media.root/(row['assets'][0]['data']['sha256']+'.wav')
    for content in (b'tampered', None):
        if content is None: target.unlink()
        else: target.write_bytes(content)
        with pytest.raises((ValueError, OSError)): recovery._generation(root,'assets/packages')
        target.write_bytes(wav())
    target.unlink(); outside=root/'cache/other.wav';outside.write_bytes(wav());target.symlink_to(outside)
    with pytest.raises((ValueError,OSError)):recovery._generation(root,'assets/packages')
    target.unlink();target.write_bytes(wav())
    with db.connect() as con:con.execute('update runtime_entities set company_id=? where entity_id=?',('foreign',row['assets'][0]['entity_id']))
    with pytest.raises(ValueError):recovery._generation(root,'assets/packages')


def test_music_no_audio_refs_keep_old_archive_and_export_guard(tmp_path, monkeypatch):
    root=tmp_path/'old';root.mkdir();db,store=make_full_root(root,'old')
    archive=tmp_path/'old.zip';backup_v2(root,archive,store)
    with zipfile.ZipFile(archive) as bundle:assert 'musicRefs' not in json.loads(bundle.read('manifest.json'))
    assert preflight_v2(root,archive,store)['status']=='PREFLIGHT_OK'
    (root/'export/foreign.wav').write_bytes(b'RIFF')
    with pytest.raises(ValueError):backup_v2(root,tmp_path/'rejected.zip',store)


def test_music_orphan_retained_in_verified_backup_without_public_asset(tmp_path,monkeypatch):
    from backend.tests.test_music_local_import import local_setup, wav
    root,db,runtime,w,service=local_setup(tmp_path,monkeypatch)
    meta=service.media.stage_user(wav());archive=tmp_path/'orphan.zip'
    backup_v2(root,archive,root/'assets/packages')
    with zipfile.ZipFile(archive) as bundle:
        manifest=json.loads(bundle.read('manifest.json'))
        assert 'musicRefs' not in manifest
        assert f'data/assets/music-audio/{meta["sha256"]}.wav' in bundle.namelist()
    with pytest.raises(ValueError):recovery._store_relative(root,root/recovery.MUSIC_TREE)


def test_design_companion_and_real_cg_media_backup_restore_rollback(tmp_path,monkeypatch):
    from backend.tests.test_music_local_import import local_setup, scope, create as song, wav, upload, finish, COMPANY
    from backend.tests.test_content_growth_local_media import png,payload
    from app.content_growth_entry_service import ASSETS
    from app.content_growth_service import ContentGrowthService
    from app.content_growth_media_service import ContentGrowthMediaService
    from app.writing_chapter_service import WritingChapterService
    from app.writing_book_service import WritingBookService,empty_context
    root,db,runtime,mw,music=local_setup(tmp_path,monkeypatch)
    with scope():
        musicrow=finish(music,mw,upload(music,mw,song(music,mw),wav()))
        cg=runtime.install(ASSETS/'content_growth_v02',COMPANY,department_id='local-dept',business_id='cg-local',business_name='本地内容')
        w=cg['instance']['workspace_id'];media=ContentGrowthMediaService(db,data_root=root);s=ContentGrowthService(db,media=media)
        from backend.tests.test_cg_four_form_interaction import draft
        row=s.command(COMPANY,w,'','create',request_id='content',data=draft('graphic'))
        from app.content_growth_operating_service import ContentGrowthOperatingService
        ops=ContentGrowthOperatingService(db,service=s)
        cg_context=ops.command(COMPANY,w,'Context','original-context','',{'title':'固定人工创作依据','content_ref':row['content']['entity_id'],'version_ref':row['version']['entity_id'],'reference_refs':[],'direction_ref':'','report_refs':[]})
        row=s.command(COMPANY,w,row['content']['entity_id'],'save',request_id='inherit-context',expected_version_ref=row['version']['entity_id'],data=draft('graphic','自作正文'))
        assert row['operating_context']['ref']==cg_context['ref']
        result=media.import_asset(s,COMPANY,w,row['content']['entity_id'],'image',row['version']['entity_id'],payload(png()),png())
        writing=runtime.install(ASSETS/'writing_authoring',COMPANY,department_id='local-dept',business_id='writing-local',business_name='本地写作')
        ww=writing['instance']['workspace_id'];book=runtime.create_object(ww,'core.domain-object.create','WritingBook',{'title':'我的书','status':'DRAFT'})['object_id']
        chapter=runtime.create_object(ww,'core.domain-object.create','WritingChapter',{'title':'第一章','bookRef':book,'status':'DRAFT'})['object_id']
        chapters=WritingChapterService(db);books=WritingBookService(db,chapters=chapters)
        context=empty_context();context['items']=[{'id':'chapter','kind':'chapter','title':'第一章','chapter_ref':chapter,'order':0}]
        saved=books.save(COMPANY,ww,book,'context','',context)
        draft_out=chapters.command(COMPANY,ww,book,chapter,'draft.saved','draft','ABSENT',{'text':'自作正文','knowledge':[]})
        chapters.command(COMPANY,ww,book,chapter,'context.bound','basis',draft_out['draft']['ref'],{'context_ref':saved['ref'],'item_ids':['chapter'],'confirmed':True})
    archive=tmp_path/'design.zip';store=root/'assets/packages'
    backup_v2(root,archive,store)
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('manifest.json'));assert len(manifest['cgMediaRefs'])==1 and len(manifest['musicRefs'])==1
    with scope():
        books.save(COMPANY,ww,book,'next',saved['ref'],{**context,'setup':{**context['setup'],'genre':'新修订'}})
    before=recovery._generation(root,'assets/packages')[2]
    preview=preflight_v2(root,archive,store)
    with pytest.raises(RuntimeError):restore_v2(root,archive,preview['archiveSha256'],preview['currentGeneration'],store,fail_after_files=2)
    assert reconcile_v2(root)['status']=='ROLLED_BACK'
    assert recovery._generation(root,'assets/packages')[2]==before
    preview=preflight_v2(root,archive,store)
    assert restore_v2(root,archive,preview['archiveSha256'],preview['currentGeneration'],store)['status']=='RESTORED'
    with scope():
        assert books.read(COMPANY,ww,book)['record']['ref']==saved['ref']
        assert s.content(COMPANY,w,row['content']['entity_id'])['operating_context']['ref']==cg_context['ref']
        assert media.read(s,COMPANY,w,row['content']['entity_id'],result['asset']['ref'])[0]==png()
        assert music.content(COMPANY,mw,musicrow['song']['entity_id'])['master']==musicrow['master']
    asset=root/'data/assets/content-growth-media'/f"{payload(png())['sha256']}.png"
    original=asset.read_bytes();asset.write_bytes(original[:-1]+b'x')
    with pytest.raises(ValueError):backup_v2(root,tmp_path/'bad.zip',store)


def _legal_adopted_cg_media(path,monkeypatch):
    from uuid import uuid4
    import struct,zlib
    from backend.tests.test_music_local_import import local_setup,scope,COMPANY
    from backend.tests.test_cg_content_entry import data,selected
    from backend.tests.test_content_growth_operating_context import draft
    from app.content_growth_entry_service import ASSETS
    from app.content_growth_service import ContentGrowthService
    from app.content_growth_operating_service import ContentGrowthOperatingService
    from app.content_growth_media_service import ContentGrowthMediaService
    root,db,runtime,_,_=local_setup(path,monkeypatch)
    with scope():
        installed=runtime.install(ASSETS/'content_growth_v02',COMPANY,department_id='local-dept',business_id='cg-adopted-media',business_name='受控采用媒体')
        w=installed['instance']['workspace_id'];media=ContentGrowthMediaService(db,data_root=root);service=ContentGrowthService(db,media=media);ops=ContentGrowthOperatingService(db,service=service)
        first=service.command(COMPANY,w,'','create',request_id='create',data=draft('graphic',data()['body']));c=first['content']['entity_id'];v=first['version']['entity_id']
        context=ops.command(COMPANY,w,'Context','context','',{'title':'明确的人工依据A','content_ref':c,'version_ref':v,'reference_refs':[],'direction_ref':'','report_refs':[]})
        prepared=service.command(COMPANY,w,c,'candidate',request_id='candidate',expected_version_ref=v,data={**draft('graphic','原创候选正文'),'selection':selected(first)})
        candidate=prepared['candidates'][0];assert candidate['eligible'] and not candidate['reasons']
        feedback=service.candidate_feedback(COMPANY,w,c,candidate_ref=candidate['version']['entity_id'],candidate_version=candidate['feedback_version'],basis_version_ref=v,action='ACCEPT',reason='人工核对三个边界',request_id=str(uuid4()))
        assert feedback['action']=='ACCEPT'
        adopted=service.command(COMPANY,w,c,'adopt',request_id='adopt',expected_version_ref=v,data={'candidate_ref':candidate['version']['entity_id'],'checks':{'content':True,'references':True,'account':True}})
        assert adopted['operating_context']['ref']==context['ref']
        def chunk(tag,raw):return struct.pack('>I',len(raw))+tag+raw+struct.pack('>I',zlib.crc32(tag+raw)&0xffffffff)
        raw=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xff\0\0'))+chunk(b'IEND',b'')
        imported=media.import_asset(service,COMPANY,w,c,'media',adopted['version']['entity_id'],{'title':'自写像素','sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'mime':'image/png','use':'OUTPUT'},raw)
        media.adopt(service,COMPANY,w,c,'adopt-media',imported['candidate']['ref'],True,True)
    return dict(root=root,db=db,runtime=runtime,company=COMPANY,scope=scope,workspace=w,content=c,service=service,ops=ops,media=media,first=first,context=context,candidate=candidate['version'],adopted=adopted,imported=imported,raw=raw)


def test_legal_script_adoption_media_backup_preflight_restore_and_failed_restore_rollback(tmp_path,monkeypatch):
    from backend.tests.test_content_growth_operating_context import draft
    fixture=_legal_adopted_cg_media(tmp_path,monkeypatch);f=fixture;root=f['root'];store=root/'assets/packages';archive=tmp_path/'adopted-media.zip'
    backup_v2(root,archive,store)
    with f['scope']():
        later=f['service'].command(f['company'],f['workspace'],f['content'],'save',request_id='after-backup',expected_version_ref=f['adopted']['version']['entity_id'],data=draft('graphic','采用后的继续保存'))
        assert later['operating_context']['ref']==f['context']['ref']
    before=recovery._generation(root,'assets/packages')[2];preview=preflight_v2(root,archive,store)
    with pytest.raises(RuntimeError):restore_v2(root,archive,preview['archiveSha256'],preview['currentGeneration'],store,fail_after_files=2)
    assert reconcile_v2(root)['status']=='ROLLED_BACK' and recovery._generation(root,'assets/packages')[2]==before
    with f['scope']():assert f['service'].content(f['company'],f['workspace'],f['content'])['version']['entity_id']==later['version']['entity_id']
    preview=preflight_v2(root,archive,store)
    assert restore_v2(root,archive,preview['archiveSha256'],preview['currentGeneration'],store)['status']=='RESTORED'
    from app.content_growth_service import ContentGrowthService
    with f['scope']():
        cold=ContentGrowthService(f['db']).content(f['company'],f['workspace'],f['content']);assert cold['version']['entity_id']==f['adopted']['version']['entity_id'] and cold['operating_context']['ref']==f['context']['ref']
        assert f['media'].read(f['service'],f['company'],f['workspace'],f['content'],f['imported']['asset']['ref'])[0]==f['raw']
        for old in(f['first']['version'],f['candidate'],f['adopted']['version']):assert next(v for v in cold['versions']if v['entity_id']==old['entity_id'])==old
        with f['db'].connect()as con:assert con.execute('select count(*) from ai_usage_records').fetchone()[0]==0


def test_adopted_media_explicit_same_version_context_keeps_both_original_pins_recoverable(tmp_path,monkeypatch):
    f=_legal_adopted_cg_media(tmp_path,monkeypatch)
    with f['scope']():
        rebound=f['ops'].command(f['company'],f['workspace'],'Context','rebind',f['context']['ref'],{**f['context']['payload'],'title':'明确的新绑定B','version_ref':f['adopted']['version']['entity_id']})
        current=f['service'].content(f['company'],f['workspace'],f['content']);assert current['operating_context']['ref']==rebound['ref']
        raw=f['raw'];imported=f['media'].import_asset(f['service'],f['company'],f['workspace'],f['content'],'media-after-explicit',f['adopted']['version']['entity_id'],{'title':'自写像素B','sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'mime':'image/png','use':'OUTPUT'},raw)
        assert imported['candidate']['payload']['context_ref']==rebound['ref']
    archive=tmp_path/'explicit-media.zip';store=f['root']/'assets/packages';backup_v2(f['root'],archive,store);assert preflight_v2(f['root'],archive,store)['archiveSha256']


@pytest.mark.parametrize('corruption',['adopted-pin','candidate-pin','missing-adoption-receipt','receipt-basis','foreign-candidate','saved-receipt-pin'])
def test_adopted_media_corrupt_original_proof_refuses_without_changing_destination(tmp_path,monkeypatch,corruption):
    from backend.tests.test_content_growth_operating_context import draft
    f=_legal_adopted_cg_media(tmp_path,monkeypatch);root=f['root'];store=root/'assets/packages';archive=tmp_path/'valid.zip';backup_v2(root,archive,store)
    with f['scope']():
        if corruption=='foreign-candidate':
            other=f['service'].command(f['company'],f['workspace'],'','create',request_id='other',data=draft('graphic','另一内容'))
        if corruption=='saved-receipt-pin':
            saved=f['service'].command(f['company'],f['workspace'],f['content'],'save',request_id='save-for-negative',expected_version_ref=f['adopted']['version']['entity_id'],data=draft('graphic','后续正文'))
            f['media'].import_asset(f['service'],f['company'],f['workspace'],f['content'],'saved-media',saved['version']['entity_id'],{'title':'后续像素','sha256':hashlib.sha256(f['raw']).hexdigest(),'size':len(f['raw']),'mime':'image/png','use':'OUTPUT'},f['raw'])
        # Corrupt only after actual legal adoption; no candidate/adoption row is manufactured.
        with f['db'].connect()as con:
            if corruption in{'adopted-pin','candidate-pin','foreign-candidate'}:
                ref=f['candidate']['entity_id']if corruption=='candidate-pin'else f['adopted']['version']['entity_id'];row=con.execute('select data_json from runtime_entities where entity_id=?',(ref,)).fetchone();value=json.loads(row[0])
                if corruption=='foreign-candidate':value['source_candidate_ref']=other['version']['entity_id']
                else:value['context_basis_ref']='missing-or-foreign-context'
                con.execute('update runtime_entities set data_json=? where entity_id=?',(json.dumps(value),ref))
            elif corruption=='missing-adoption-receipt':con.execute("delete from evolution_events where correlation_id=? and event_type='cg.content.adopted'",(f['content'],))
            else:
                event='cg.content.saved'if corruption=='saved-receipt-pin'else'cg.content.adopted';row=con.execute('select event_id,payload from evolution_events where correlation_id=? and event_type=?',(f['content'],event)).fetchone();value=json.loads(row['payload'])
                if corruption=='saved-receipt-pin':value['context_ref']='missing-context'
                else:value['request']['expected_version_ref']=f['candidate']['entity_id']
                con.execute('update evolution_events set payload=? where event_id=?',(json.dumps(value),row['event_id']))
    dbhash=hashlib.sha256(Path(f['db'].path).read_bytes()).hexdigest();asset=root/'data/assets/content-growth-media'/(hashlib.sha256(f['raw']).hexdigest()+'.png');asset_hash=hashlib.sha256(asset.read_bytes()).hexdigest()
    with pytest.raises(ValueError):backup_v2(root,tmp_path/'refused.zip',store)
    with pytest.raises(ValueError):preflight_v2(root,archive,store)
    assert hashlib.sha256(Path(f['db'].path).read_bytes()).hexdigest()==dbhash and hashlib.sha256(asset.read_bytes()).hexdigest()==asset_hash
