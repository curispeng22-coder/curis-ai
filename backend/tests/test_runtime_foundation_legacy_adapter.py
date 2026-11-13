from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import LegacyExecutionAdapter, RuntimeFoundation
from app.tenant_context import TenantContext


class RuntimeFoundationLegacyAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()
        with self.db.connect() as conn:
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-legacy', 'tenant-legacy', 'ceo', 'Legacy')")

    def test_legacy_execution_is_reference_only(self):
        with TenantContext.scope("tenant-legacy"):
            foundation = RuntimeFoundation(self.db)
            content = foundation.create("CONTENT_ITEM", company_id="company-legacy")
            attached = LegacyExecutionAdapter(foundation).attach(
                content["entity_id"], execution_type="content_workflow_run",
                execution_id="legacy-run-1", legacy_status="completed",
            )
            self.assertEqual(attached["execution_ref"], "content_workflow_run:legacy-run-1")
            self.assertEqual(attached["lifecycle_status"], "IDEA")
            self.assertEqual(attached["data"]["legacyExecutionStatus"], "completed")
            with self.assertRaises(ValueError):
                LegacyExecutionAdapter(foundation).attach(
                    content["entity_id"], execution_type="project", execution_id="legacy-project"
                )


if __name__ == "__main__":
    unittest.main()
