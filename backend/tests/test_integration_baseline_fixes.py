from __future__ import annotations

import os
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import Database, SCHEMA_VERSION
from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class EmployeeAffiliationTests(unittest.TestCase):
    def setUp(self):
        identity_env = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        identity_env.start()
        self.addCleanup(identity_env.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)

    def test_crud_and_employee_save_closure(self):
        company, department, employee, project = self._workspace()
        response = self.client.post(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            json={
                "employee_id": employee["id"],
                "affiliations": [
                    {"department_id": department["id"]},
                    {"project_id": project["project_id"]},
                    {"project_id": project["project_id"]},
                ],
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        affiliations = response.json()["affiliations"]
        self.assertEqual(len(affiliations), 2)

        saved = self.client.get(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            params={"employee_id": employee["id"]},
        )
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(len(saved.json()["affiliations"]), 2)

        by_department = self.client.get(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            params={"department_id": department["id"]},
        ).json()
        self.assertEqual(by_department["employee_ids"], [employee["id"]])
        by_project = self.client.get(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            params={"project_id": project["project_id"]},
        ).json()
        self.assertEqual(by_project["employee_ids"], [employee["id"]])

        replaced = self.client.post(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            json={
                "employee_id": employee["id"],
                "affiliations": [{"department_id": department["id"]}],
            },
        ).json()["affiliations"]
        self.assertEqual(len(replaced), 1)
        deleted = self.client.delete(
            f"/api/workspace/employee-affiliations/{replaced[0]['id']}",
            headers=TENANT_A,
        )
        self.assertEqual(deleted.status_code, 204, deleted.text)
        self.assertEqual(
            self.client.get(
                "/api/workspace/employee-affiliations",
                headers=TENANT_A,
                params={"employee_id": employee["id"]},
            ).json()["affiliations"],
            [],
        )
        self.assertEqual(company["company_id"], employee["company_id"])

    def test_tenant_isolation_and_reference_validation(self):
        _, department, employee, project = self._workspace()
        created = self.client.post(
            "/api/workspace/employee-affiliations",
            headers=TENANT_A,
            json={
                "employee_id": employee["id"],
                "affiliations": [{"project_id": project["project_id"]}],
            },
        ).json()["affiliations"][0]

        self.assertEqual(
            self.client.get(
                "/api/workspace/employee-affiliations",
                headers=TENANT_B,
                params={"employee_id": employee["id"]},
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                "/api/workspace/employee-affiliations",
                headers=TENANT_B,
                json={
                    "employee_id": employee["id"],
                    "affiliations": [{"department_id": department["id"]}],
                },
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.delete(
                f"/api/workspace/employee-affiliations/{created['id']}",
                headers=TENANT_B,
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(
                "/api/workspace/employee-affiliations",
                headers=TENANT_A,
                json={
                    "employee_id": employee["id"],
                    "affiliations": [{"project_id": "missing-project"}],
                },
            ).status_code,
            404,
        )

    def _workspace(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        ).json()
        employee_response = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "技术负责人",
                "instructions_override": "负责技术交付。",
            },
        )
        self.assertEqual(employee_response.status_code, 201, employee_response.text)
        employee = employee_response.json()
        project_response = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "集成项目",
                "goal": "验证员工保存闭环。",
                "status": "planned",
            },
        )
        self.assertEqual(project_response.status_code, 201, project_response.text)
        return company, department, employee, project_response.json()


class SchemaGovernanceTests(unittest.TestCase):
    def test_fresh_and_upgraded_schema_match_and_record_version(self):
        with tempfile.TemporaryDirectory() as directory:
            fresh = Path(directory) / "fresh.sqlite"
            upgraded = Path(directory) / "upgraded.sqlite"
            Database(str(fresh)).initialize()
            shutil.copy2(fresh, upgraded)
            with sqlite3.connect(upgraded) as connection:
                connection.execute("pragma user_version = 0")
                connection.execute("delete from schema_migrations")
                connection.execute("drop table employee_affiliations")
                connection.execute(
                    "create table action_proposals (id text primary key)"
                )

            Database(str(upgraded)).initialize()
            self.assertEqual(
                self._schema_signature(upgraded),
                self._schema_signature(fresh),
            )
            with sqlite3.connect(upgraded) as connection:
                self.assertEqual(
                    connection.execute("pragma user_version").fetchone()[0],
                    SCHEMA_VERSION,
                )
                self.assertEqual(
                    connection.execute(
                        "select version, name from schema_migrations"
                    ).fetchall(),
                    [(1, "integration-v1-schema-baseline")],
                )

    def test_non_empty_retired_table_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blocked.sqlite"
            Database(str(path)).initialize()
            with sqlite3.connect(path) as connection:
                connection.execute("pragma user_version = 0")
                connection.execute("delete from schema_migrations")
                connection.execute(
                    "create table action_proposals (id text primary key)"
                )
                connection.execute(
                    "insert into action_proposals(id) values ('keep-me')"
                )
            with self.assertRaisesRegex(
                RuntimeError,
                "refusing to drop non-empty retired table: action_proposals",
            ):
                Database(str(path)).initialize()

    @staticmethod
    def _schema_signature(path: Path):
        with sqlite3.connect(path) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "select name from sqlite_master "
                    "where type = 'table' and name not like 'sqlite_%'"
                )
            }
            return {
                table: {
                    (row[1], row[2].lower(), row[3], row[5])
                    for row in connection.execute(f'pragma table_info("{table}")')
                }
                for table in tables
            }


if __name__ == "__main__":
    unittest.main()
