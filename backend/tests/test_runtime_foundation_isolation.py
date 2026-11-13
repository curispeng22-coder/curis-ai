from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import RuntimeFoundation, RuntimeScopeError
from app.tenant_context import TenantContext


class RuntimeFoundationIsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()
        with self.db.connect() as conn:
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-a', 'tenant-a', 'ceo-a', 'A')")
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-b', 'tenant-b', 'ceo-b', 'B')")
            conn.execute("insert into workspaces(workspace_id, tenant_id, business_id, company_id, name, status) values ('workspace-a', 'tenant-a', 'business-a', 'company-a', 'WA', 'DRAFT')")
            conn.execute("insert into workspaces(workspace_id, tenant_id, business_id, company_id, name, status) values ('workspace-b', 'tenant-b', 'business-b', 'company-b', 'WB', 'DRAFT')")

    def test_tenant_company_and_workspace_fail_closed(self):
        with TenantContext.scope("tenant-a"):
            service = RuntimeFoundation(self.db)
            local = service.create("CYCLE", company_id="company-a", workspace_id="workspace-a")
            with self.assertRaises(RuntimeScopeError):
                service.create("CYCLE", company_id="company-b")
            with self.assertRaises(RuntimeScopeError):
                service.create("CYCLE", company_id="company-a", workspace_id="workspace-b")
        with TenantContext.scope("tenant-b"):
            service = RuntimeFoundation(self.db)
            with self.assertRaises(KeyError):
                service.get(local["entity_id"])

    def test_cross_company_link_is_rejected(self):
        with self.db.connect() as conn:
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-a2', 'tenant-a', 'ceo-a', 'A2')")
        with TenantContext.scope("tenant-a"):
            service = RuntimeFoundation(self.db)
            left = service.create("CYCLE", company_id="company-a")
            right = service.create("EVIDENCE", company_id="company-a2")
            with self.assertRaises(RuntimeScopeError):
                service.link(left["entity_id"], "HAS_EVIDENCE", right["entity_id"])


if __name__ == "__main__":
    unittest.main()
