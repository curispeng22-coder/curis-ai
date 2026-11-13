import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.tenant_context import TenantContext


class D1TenantReservationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()

    def tearDown(self):
        self.tmp.cleanup()

    def _columns(self, table: str) -> set[str]:
        with self.db.connect() as conn:
            return {c["name"] for c in conn.execute(f"pragma table_info({table})")}

    def test_tasks_has_tenant_id_column(self):
        self.assertIn("tenant_id", self._columns("tasks"))

    def test_evolution_events_has_tenant_id_column(self):
        self.assertIn("tenant_id", self._columns("evolution_events"))

    def test_new_row_gets_default_tenant(self):
        with self.db.connect() as conn:
            conn.execute(
                "insert into tasks (task_id, content, status) values ('t2','c2','open')"
            )
        with self.db.connect() as conn:
            row = conn.execute(
                "select tenant_id from tasks where task_id='t2'"
            ).fetchone()
        self.assertEqual(row["tenant_id"], "selfuse")

    def test_preexisting_row_backfills_to_default(self):
        # Simulate a DB created before the tenant_id migration.
        with self.db.connect() as conn:
            conn.execute(
                "create table if not exists tasks "
                "(task_id text primary key, content text not null, status text not null)"
            )
            conn.execute(
                "insert into tasks (task_id, content, status) values ('t1','c','done')"
            )
        # Re-initialize: _ensure_column backfills tenant_id on existing rows.
        self.db.initialize()
        with self.db.connect() as conn:
            row = conn.execute(
                "select tenant_id from tasks where task_id='t1'"
            ).fetchone()
        self.assertEqual(row["tenant_id"], "selfuse")

    def test_context_defaults_to_single_tenant(self):
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
        self.assertTrue(TenantContext.is_multi_tenant())

    def test_scope_sets_and_restores(self):
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
        with TenantContext.scope("ceo-2"):
            self.assertEqual(TenantContext.current_tenant_id(), "ceo-2")
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
