"""D134: a full same-root restore must survive two Workspace starts."""

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.model_gateway import R3_CAPABILITY_ID, R3_GATEWAY_ID
from desktop.runtime.recovery import backup_v2, preflight_v2, restore_v2
from desktop.tests.test_release_recovery import make_canonical_initialized_root


class C03CatalogPreservationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ["CURIS_C03_TEST_ROOT"])
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "company"
        self.environment = patch.dict(os.environ, {
            "CURIS_PRODUCT": "workspace",
            "CURIS_ENV": "test",
            "CURIS_IDENTITY_MODE": "test",
            "CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev",
            "CURIS_D1_EXECUTE_ENABLED": "false",
            "CURIS_RD_SANDBOX": "off",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)

    @staticmethod
    def _rows(db: Path, table: str):
        with sqlite3.connect(db) as connection:
            return {row[0]: tuple(row[1:]) for row in connection.execute(f"select rowid, * from {table}")}

    def test_full_restore_preserves_existing_catalog_and_authorization_after_two_starts(self):
        db, store = make_canonical_initialized_root(self.root)
        with sqlite3.connect(db) as connection:
            connection.execute("update model_gateways set credential_ref='keychain:test-only-ref', name='Existing factory gateway' where gateway_id='newapi'")
            connection.execute("insert or ignore into model_gateways(gateway_id,name,type,base_url,status,credential_ref,default_model) values (?,?, 'newapi','https://example.invalid','active','keychain:test-only-r3','existing-model')", (R3_GATEWAY_ID, "Existing R3 gateway"))
            connection.execute("insert or ignore into official_models(model_key,provider_id,display_name,supported_models,auth_type,source,gateway_ref,status) values (?,?,?,'[]','apikey','official',?,'active')", (R3_CAPABILITY_ID, "test-provider", "Existing R3 model", R3_GATEWAY_ID))
            connection.execute("update employee_templates set allowed_effect_classes_json='[]' where rowid=(select rowid from employee_templates where source='official' limit 1)")
            connection.execute("update plans set price=37, price_currency='EUR', billing_cycle='year', updated_at='2020-01-01' where plan_id='plan_pro'")
            connection.execute("update workflow_templates set name='Existing approved workflow', workflow_capability_status='instantiation_forbidden', updated_at='2020-01-01' where id='official.workflow.software_rnd_sop'")
            connection.execute("insert into tools(name,type,description,entry) values ('default_tool','test','Existing tool','existing-entry')")
            connection.execute("update dashboard_templates set name='Existing dashboard' where rowid=(select rowid from dashboard_templates limit 1)")
            connection.execute("insert into dashboard_templates(dashboard_template_id,name,company_type,source,tenant_id) values('dtpl_test_custom','Custom dashboard','generic','tenant_private','selfuse')")
            connection.execute("insert into dashboard_widget_catalog(widget_id,domain,title,source,tenant_id) values('test_custom_widget','company','Custom widget','tenant_private','selfuse')")
            connection.execute("update pricing_rules set amount=37, updated_at='2020-01-01' where pricing_rule_id='pr_default_pro'")
        watched = ("dashboard_templates", "dashboard_widget_catalog", "model_gateways", "official_models", "platform_policies", "pricing_rules", "quota_rules", "capability_packages", "company_packages", "company_templates", "employee_templates", "plans", "workflow_templates", "tools")
        before = {table: self._rows(db, table) for table in watched}
        archive = Path(self.temp.name) / "full.zip"
        self.assertEqual(backup_v2(self.root, archive, store)["status"], "BACKUP_VERIFIED")
        with sqlite3.connect(db) as connection:
            connection.execute("update plans set name='after-backup' where plan_id='plan_pro'")
        preview = preflight_v2(self.root, archive, store)
        self.assertEqual(restore_v2(self.root, archive, preview["archiveSha256"], preview["currentGeneration"], store)["status"], "RESTORED")
        for table in watched:
            self.assertEqual(self._rows(db, table), before[table], f"restore {table}")

        for boot in (1, 2):
            with TestClient(create_app(str(db))) as client:
                self.assertEqual(client.get("/api/platform/dashboards").status_code, 404)
                self.assertEqual(client.get("/api/platform/dashboards", headers={"Authorization": "Bearer platform-admin-dev"}).status_code, 404)
                for route in ("/api/catalog/models", "/api/catalog/capabilities"):
                    response = client.get(route)
                    self.assertEqual(response.status_code, 200)
                    self.assertNotIn("keychain:test-only", response.text)
            for table in watched:
                after = self._rows(db, table)
                for rowid, row in before[table].items():
                    self.assertEqual(after.get(rowid), row, f"boot {boot} changed {table} rowid {rowid}")
            with sqlite3.connect(db) as connection:
                for table in ("tasks", "ai_usage_records", "evolution_events"):
                    self.assertEqual(connection.execute(f"select count(*) from {table}").fetchone()[0], 0)
                self.assertEqual(connection.execute("pragma integrity_check").fetchone()[0], "ok")
                self.assertEqual(connection.execute("pragma foreign_key_check").fetchall(), [])

    def test_fresh_workspace_keeps_exact_r3_catalog(self):
        db = self.root / "data/curis.sqlite"
        db.parent.mkdir(parents=True)
        with TestClient(create_app(str(db))):
            pass
        with sqlite3.connect(db) as connection:
            self.assertEqual([row[0] for row in connection.execute("select gateway_id from model_gateways")], [R3_GATEWAY_ID])
            self.assertEqual([row[0] for row in connection.execute("select model_key from official_models")], [R3_CAPABILITY_ID])

    def test_truly_legacy_authorization_column_backfills_once(self):
        db = self.root / "legacy.sqlite"
        db.parent.mkdir(parents=True)
        with sqlite3.connect(db) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("create table employee_templates(id text, source text)")
            connection.execute("create table employee_instances(id text)")
            connection.execute("insert into employee_templates values('official-one','official')")
            database = Database(str(db))
            database._migrate_position_authorization(connection)
            first = connection.execute("select allowed_effect_classes_json from employee_templates").fetchone()[0]
            self.assertEqual(first, '["read","retrieve","write","exec"]')
            database._migrate_position_authorization(connection)
            self.assertEqual(connection.execute("select allowed_effect_classes_json from employee_templates").fetchone()[0], first)


if __name__ == "__main__":
    unittest.main()
