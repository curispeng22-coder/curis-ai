from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from backend.app import local_project_runtime_target as subject


SCHEMA = """
create table tenants (tenant_id text primary key, name text not null, status text, description text);
create table companies (
  company_id text primary key, tenant_id text not null, ceo_id text not null, name text not null,
  description text not null default '', status text not null, is_default integer not null,
  default_project_id text
);
create table projects (
  project_id text primary key, tenant_id text not null, company_id text not null, name text not null,
  goal text not null, description text not null default '', status text not null
);
create table tenant_memberships (
  membership_id text primary key, tenant_id text not null, company_id text not null,
  ceo_id text, role text not null, status text not null
);
"""


class LocalProjectRuntimeTargetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "quality.sqlite"
        with sqlite3.connect(self.db) as connection:
            connection.executescript(SCHEMA)
        self.patches = (
            patch.object(subject, "TARGET_DB", self.db),
            patch.object(subject, "_assert_ports_closed"),
            patch.dict(os.environ, {"CURIS_ENV": "local"}, clear=False),
        )
        for item in self.patches:
            item.start()

    def tearDown(self) -> None:
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def test_creates_one_idempotent_chain_without_membership(self) -> None:
        first = subject.provision()
        second = subject.provision()
        self.assertEqual(first, second)
        with sqlite3.connect(self.db) as connection:
            self.assertEqual(connection.execute("select count(*) from tenants").fetchone()[0], 1)
            self.assertEqual(connection.execute("select count(*) from companies").fetchone()[0], 1)
            self.assertEqual(connection.execute("select count(*) from projects").fetchone()[0], 1)
            self.assertEqual(connection.execute("select count(*) from tenant_memberships").fetchone()[0], 0)
            self.assertEqual(
                connection.execute("select material_digest, status from local_owner_preauthorizations").fetchone(),
                (None, "pending"),
            )

    def test_rejects_non_local_environment_before_write(self) -> None:
        with patch.dict(os.environ, {"CURIS_ENV": "production"}, clear=False):
            with self.assertRaisesRegex(subject.ProvisioningRejected, "local_environment_required"):
                subject.provision()
        with sqlite3.connect(self.db) as connection:
            self.assertIsNone(
                connection.execute(
                    "select 1 from sqlite_master where type='table' and name='local_owner_preauthorizations'"
                ).fetchone()
            )

    def test_rolls_back_every_insert(self) -> None:
        with sqlite3.connect(self.db) as connection:
            connection.execute(
                "create trigger reject_project before insert on projects begin select raise(abort, 'reject'); end"
            )
        with self.assertRaises(sqlite3.IntegrityError):
            subject.provision()
        with sqlite3.connect(self.db) as connection:
            self.assertEqual(connection.execute("select count(*) from tenants").fetchone()[0], 0)
            self.assertEqual(connection.execute("select count(*) from companies").fetchone()[0], 0)
            self.assertEqual(connection.execute("select count(*) from projects").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
