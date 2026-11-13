import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.tenant_context import TenantContext


class WorkspaceDepartmentActivationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_activation_write_read_reset_are_tenant_scoped(self):
        tenant_a = {"X-Tenant-Id": "tenant-A"}
        tenant_b = {"X-Tenant-Id": "tenant-B"}

        put_response = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": ["business.general", "function.hr"]},
            headers=tenant_a,
        )
        read_a = self.client.get("/api/workspace/departments/activation", headers=tenant_a)
        read_b = self.client.get("/api/workspace/departments/activation", headers=tenant_b)
        reset_a = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": []},
            headers=tenant_a,
        )

        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(
            put_response.json()["active_department_type_keys"],
            ["business.general", "function.hr"],
        )
        self.assertEqual(
            [item["type_key"] for item in read_a.json()["department_types"] if item["enabled"]],
            ["business.general", "function.hr"],
        )
        self.assertEqual(read_b.json()["active_department_type_keys"], [])
        self.assertEqual(reset_a.json()["active_department_type_keys"], [])

    def test_activation_rejects_unknown_inactive_or_non_official_department_types(self):
        self.database.set_department_type_enabled("function.hr", False)
        with TenantContext.scope("default"):
            self.database.save_department_type(
                "tenant.private",
                "business",
                "Private",
                "tenant private",
                "{}",
                "0.0",
                is_system=False,
            )

        unknown = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": ["missing.type"]},
            headers={"X-Tenant-Id": "tenant-A"},
        )
        inactive = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": ["function.hr"]},
            headers={"X-Tenant-Id": "tenant-A"},
        )
        private = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": ["tenant.private"]},
            headers={"X-Tenant-Id": "tenant-A"},
        )

        self.assertEqual(unknown.status_code, 422)
        self.assertEqual(inactive.status_code, 422)
        self.assertEqual(private.status_code, 422)

    def test_activation_persistence_and_api_are_metadata_only(self):
        response = self.client.put(
            "/api/workspace/departments/activation",
            json={"department_type_keys": ["business.general"]},
            headers={"X-Tenant-Id": "tenant-A"},
        )

        self.assertEqual(response.status_code, 200)
        with closing(sqlite3.connect(self.db_path)) as connection:
            columns = {
                row[1]
                for row in connection.execute("pragma table_info(tenant_department_activations)")
            }
        self.assertEqual(
            columns,
            {
                "tenant_id",
                "department_type_key",
                "source",
                "enabled",
                "display_order",
                "updated_at",
            },
        )
        payload_text = str(
            self.client.get(
                "/api/workspace/departments/activation",
                headers={"X-Tenant-Id": "tenant-A"},
            ).json()
        )
        for forbidden in (
            "api_key",
            "token",
            "password",
            "secret",
            "credential",
            "Authorization",
            "prompt",
            "output",
            "billing",
            "ROI",
            "staffing",
            "permission",
            "routing",
            "model_policy",
            "external_platform",
        ):
            self.assertNotIn(forbidden, payload_text)


if __name__ == "__main__":
    unittest.main()
