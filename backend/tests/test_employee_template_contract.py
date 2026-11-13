import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app


class WorkspaceEmployeeTemplateContractTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))

    def tearDown(self):
        self.tmp.cleanup()

    def test_employee_template_contract_tables_are_reserved_only(self):
        expected = {
            "employee_templates": {
                "id",
                "slug",
                "name",
                "role",
                "responsibility",
                "description",
                "department_type",
                "default_instructions",
                "default_capability_types_json",
                "default_model_policy_json",
                "default_workflow_step_types_json",
                "guardrails_json",
                "source",
                "tenant_id",
                "enabled",
                "created_at",
                # ── Gate E 官方 catalog 内容补全（design §4.2 / §延后 backlog 7）──
                "persona_ref",
                "default_skill",
                "default_tool",
                "persona_overrides_json",
                "version",
                "status",
                "updated_at",
                # ── Phase-10 岗位级授权：岗位允许的 effect_class 白名单 ──
                "allowed_effect_classes_json",
            },
            "employee_instances": {
                "id",
                "tenant_id",
                "company_id",
                "department_id",
                "template_id",
                "name",
                "role",
                "instructions_override",
                "status",
                "enabled",
                "created_from_template_id",
                "created_at",
                # ── Gate E 运行时快照冻结（design §4.2）──
                "persona_ref",
                "default_skill",
                "default_tool",
                # ── Workspace 员工目录 v1：软删除列 ──
                "deleted_at",
                # ── Phase-10 岗位级授权：员工实例级授权覆盖（空 = 继承模板）──
                "allowed_effect_classes_json",
            },
            "department_templates": {
                "id",
                "slug",
                "name",
                "department_type",
                "description",
                "default_employee_templates_json",
                "default_workflow_template_id",
                "default_capability_types_json",
                "source",
                "tenant_id",
                "enabled",
                "created_at",
                # ── Phase-1 加列（design §4.2）──
                "version",
                "status",
            },
            "employee_capability_bindings": {
                "id",
                "tenant_id",
                "employee_id",
                "employee_template_id",
                "capability_source",
                "capability_type",
                "capability_id",
                "priority",
                "enabled",
                "created_at",
            },
        }

        with closing(sqlite3.connect(self.db_path)) as connection:
            for table, columns in expected.items():
                actual = {
                    row[1] for row in connection.execute(f"pragma table_info({table})")
                }
                self.assertEqual(actual, columns)

    def test_employee_templates_endpoint_is_read_only_metadata(self):
        response = self.client.get(
            "/api/workspace/employee-templates",
            headers={"X-Tenant-Id": "tenant-a"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["tenant_id"], "tenant-a")
        self.assertIn("employee_templates", payload)
        self.assertTrue(payload["employee_templates"])
        template = payload["employee_templates"][0]
        self.assertEqual(
            set(template),
            {
                "id",
                "slug",
                "name",
                "role",
                "responsibility",
                "description",
                "department_type",
                "default_instructions",
                "default_capability_types",
                "default_model_policy",
                "default_workflow_step_types",
                "guardrails",
                "source",
                "tenant_id",
                "enabled",
                "created_at",
            },
        )
        self.assertEqual(template["source"], "official")
        self.assertIsInstance(template["default_capability_types"], list)
        self.assertIsInstance(template["default_model_policy"], dict)
        self.assertTrue(template["enabled"])

        payload_text = str(payload)
        for forbidden in (
            "api_key",
            "token",
            "password",
            "secret",
            "credential",
            "billing",
            "ROI",
            "execution_route",
            "task_state",
        ):
            self.assertNotIn(forbidden, payload_text)

    def test_department_templates_endpoint_is_read_only_metadata(self):
        response = self.client.get(
            "/api/workspace/department-templates",
            headers={"X-Tenant-Id": "tenant-a"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["tenant_id"], "tenant-a")
        self.assertIn("department_templates", payload)
        self.assertTrue(payload["department_templates"])
        template = payload["department_templates"][0]
        self.assertEqual(
            set(template),
            {
                "id",
                "slug",
                "name",
                "department_type",
                "description",
                "default_employee_templates",
                "default_workflow_template_id",
                "default_capability_types",
                "source",
                "tenant_id",
                "enabled",
                "created_at",
            },
        )
        self.assertEqual(template["source"], "official")
        self.assertIsInstance(template["default_employee_templates"], list)
        self.assertTrue(template["enabled"])

    def test_tenant_private_templates_are_visible_only_to_current_tenant(self):
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into employee_templates (
                  id, name, role, description, department_type,
                  default_instructions, default_capability_types_json,
                  default_model_policy_json, source, tenant_id, enabled
                ) values (?, ?, ?, ?, ?, ?, ?, ?, 'tenant_private', ?, 1)
                """,
                (
                    "tenant-a.employee.writer",
                    "Tenant A Writer",
                    "writer",
                    "Tenant A private writer",
                    "software_rnd",
                    "Write for tenant A only.",
                    '["model"]',
                    '{"mode":"tenant_default"}',
                    "tenant-a",
                ),
            )
            connection.execute(
                """
                insert into employee_templates (
                  id, name, role, description, department_type,
                  default_instructions, default_capability_types_json,
                  default_model_policy_json, source, tenant_id, enabled
                ) values (?, ?, ?, ?, ?, ?, ?, ?, 'tenant_private', ?, 1)
                """,
                (
                    "tenant-b.employee.writer",
                    "Tenant B Writer",
                    "writer",
                    "Tenant B private writer",
                    "software_rnd",
                    "Write for tenant B only.",
                    '["model"]',
                    '{"mode":"tenant_default"}',
                    "tenant-b",
                ),
            )

        tenant_a = self.client.get(
            "/api/workspace/employee-templates",
            headers={"X-Tenant-Id": "tenant-a"},
        ).json()["employee_templates"]
        tenant_b = self.client.get(
            "/api/workspace/employee-templates",
            headers={"X-Tenant-Id": "tenant-b"},
        ).json()["employee_templates"]

        self.assertIn("tenant-a.employee.writer", [item["id"] for item in tenant_a])
        self.assertNotIn("tenant-b.employee.writer", [item["id"] for item in tenant_a])
        self.assertIn("tenant-b.employee.writer", [item["id"] for item in tenant_b])
        self.assertNotIn("tenant-a.employee.writer", [item["id"] for item in tenant_b])

    def test_template_reads_do_not_touch_task_execution_tables(self):
        self.client.get(
            "/api/workspace/employee-templates",
            headers={"X-Tenant-Id": "tenant-a"},
        )
        self.client.get(
            "/api/workspace/department-templates",
            headers={"X-Tenant-Id": "tenant-a"},
        )

        with closing(sqlite3.connect(self.db_path)) as connection:
            task_count = connection.execute("select count(*) from tasks").fetchone()[0]
            execution_count = connection.execute(
                "select count(*) from executions"
            ).fetchone()[0]

        self.assertEqual(task_count, 0)
        self.assertEqual(execution_count, 0)


class ContentGrowthDepartmentCatalogTest(unittest.TestCase):
    """Exact catalog repair evidence; fixtures stay in the approved external root."""

    def setUp(self):
        import os
        import uuid

        root = Path("/private/tmp/curis-cg-department-catalog-tests-20261010-01")
        self.db_path = str(root / "data" / f"catalog-{uuid.uuid4()}.sqlite")
        for key in ("CURIS_DB", "CURIS_DB_PATH", "CURIS_WORKSPACE_DB"):
            os.environ[key] = self.db_path
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))

    def test_public_definition_and_normal_instance_have_genuine_type_and_no_defaults(self):
        payload = self.client.get("/api/workspace/department-templates").json()
        template = next(item for item in payload["department_templates"] if item["id"] == "dt_content_growth")
        self.assertEqual((template["name"], template["department_type"], template["source"], template["tenant_id"]),
                         ("内容增长部", "content_growth", "official", "platform"))
        self.assertTrue(template["enabled"])
        self.assertEqual(template["default_employee_templates"], [])
        self.assertEqual(template["default_capability_types"], [])
        self.assertIsNone(template["default_workflow_template_id"])
        self.assertIn("不保证真实媒体", template["description"])
        company = self.client.post("/api/workspace/companies", json={"name": "CG catalog isolated test"})
        self.assertEqual(company.status_code, 201, company.text)
        company_id = company.json()["company_id"]
        with self.database.connect() as con:
            employees_before = con.execute("select count(*) from employee_instances").fetchone()[0]
            self.assertEqual(con.execute("select count(*) from department_instances where department_type='content_growth'").fetchone()[0], 0)
        result = self.client.post("/api/workspace/departments", json={
            "template_id": "dt_content_growth", "company_id": company_id,
            "name": "内容增长内部审阅部", "mission": "本地脚本与人工核验观察，不授平台或模型执行",
            "enabled_employee_template_ids": [], "enabled": True, "manager_employee_id": None,
        })
        self.assertEqual(result.status_code, 201, result.text)
        department = result.json()
        self.assertEqual(department["company_id"], company_id)
        self.assertEqual(department["department_type"], "content_growth")
        self.assertEqual(department["created_from_template_id"], "dt_content_growth")
        self.assertEqual(department["enabled_employee_template_ids"], [])
        self.assertIsNone(department["manager_employee_id"])
        with self.database.connect() as con:
            self.assertEqual(con.execute("select count(*) from employee_instances").fetchone()[0], employees_before)
            self.assertEqual(con.execute("select count(*) from canonical_businesses").fetchone()[0], 0)

    def test_repeat_initialization_is_idempotent_without_company_or_employee_materialization(self):
        with self.database.connect() as con:
            before = {table: [tuple(row) for row in con.execute(f"select * from {table} order by 1")]
                      for table in ("companies", "department_instances", "employee_instances", "canonical_businesses", "workspaces", "runtime_entities")}
        self.database.initialize()
        with self.database.connect() as con:
            for table, rows in before.items():
                self.assertEqual([tuple(row) for row in con.execute(f"select * from {table} order by 1")], rows, table)
            self.assertEqual(con.execute("select count(*) from department_types where type_key='content_growth'").fetchone()[0], 1)
            self.assertEqual(con.execute("select count(*) from department_templates where id='dt_content_growth'").fetchone()[0], 1)
            self.assertEqual(con.execute("select count(*) from department_templates where id='official.department.content_growth'").fetchone()[0], 0)

    def test_type_conflict_and_disabled_type_are_not_overwritten_or_enabled(self):
        for disabled in (False, True):
            with self.database.connect() as con:
                if disabled:
                    con.execute("insert into department_type_status(type_key,enabled,updated_at) values ('content_growth',0,current_timestamp)")
                else:
                    con.execute("update department_types set display_name='Existing custom type' where type_key='content_growth'")
                before = tuple(con.execute("select * from department_types where type_key='content_growth'").fetchone())
                with self.assertRaisesRegex(ValueError, "department type conflicts"):
                    self.database._seed_department_catalog(con)
                self.assertEqual(tuple(con.execute("select * from department_types where type_key='content_growth'").fetchone()), before)
                if disabled:
                    self.assertEqual(con.execute("select enabled from department_type_status where type_key='content_growth'").fetchone()[0], 0)
                else:
                    con.execute("update department_types set display_name='内容增长部' where type_key='content_growth'")

    def test_catalog_upgrade_preserves_existing_company_support_and_legacy_lineage(self):
        company = self.client.post("/api/workspace/companies", json={"name": "Existing company preservation"}).json()["company_id"]
        result = self.client.post("/api/workspace/departments", json={"template_id": "dt_engineering", "company_id": company, "name": "Original R&D department"})
        self.assertEqual(result.status_code, 201, result.text)
        with self.database.connect() as con:
            con.execute("insert into department_instances(id,tenant_id,company_id,template_id,name,department_type,status,enabled,created_from_template_id) "
                        "values ('legacy-archived-cg','selfuse',?,'dt_ai_content','Legacy archived record','content.growth','archived',0,'dt_ai_content')", (company,))
            before = {table: [tuple(row) for row in con.execute(f"select * from {table} order by 1")]
                      for table in ("companies", "department_instances", "employee_instances", "canonical_businesses", "workspaces", "runtime_entities")}
            con.execute("delete from department_templates where id='dt_content_growth'")
            con.execute("delete from department_types where type_key='content_growth'")
        self.database.initialize()
        with self.database.connect() as con:
            for table, rows in before.items():
                self.assertEqual([tuple(row) for row in con.execute(f"select * from {table} order by 1")], rows, table)
            self.assertEqual(con.execute("select template_id from department_instances where id='legacy-archived-cg'").fetchone()[0], "dt_ai_content")
            self.assertEqual(con.execute("select count(*) from department_templates where id='dt_content_growth'").fetchone()[0], 1)

    def test_template_conflict_or_disabled_definition_is_not_replaced_or_enabled(self):
        for change in ("name='Existing definition'", "enabled=0"):
            with self.database.connect() as con:
                con.execute(f"update department_templates set {change} where id='dt_content_growth'")
                before = tuple(con.execute("select * from department_templates where id='dt_content_growth'").fetchone())
                with self.assertRaisesRegex(ValueError, "department template conflicts"):
                    self.database._seed_employee_template_contract(con)
                self.assertEqual(tuple(con.execute("select * from department_templates where id='dt_content_growth'").fetchone()), before)
                con.execute("update department_templates set name='内容增长部',enabled=1 where id='dt_content_growth'")

    def test_disabled_foreign_or_unregistered_template_and_foreign_company_fail_closed(self):
        from app.employee_templates import EmployeeTemplateContract
        contract = EmployeeTemplateContract(self.database)
        company = self.client.post("/api/workspace/companies", json={"name": "CG scope test"}).json()["company_id"]
        with self.database.connect() as con:
            con.execute("update department_templates set enabled=0 where id='dt_content_growth'")
        with self.assertRaisesRegex(ValueError, "template is not available"):
            contract.create_department_instance(template_id="dt_content_growth", name="CG", company_id=company)
        with self.database.connect() as con:
            con.execute("update department_templates set enabled=1,department_type='unregistered.cg' where id='dt_content_growth'")
        with self.assertRaisesRegex(ValueError, "template is not available|type is not registered"):
            contract.create_department_instance(template_id="dt_content_growth", name="CG", company_id=company)
        with self.database.connect() as con:
            con.execute("update department_templates set department_type='content_growth',source='tenant_private',tenant_id='foreign-tenant' where id='dt_content_growth'")
        with self.assertRaisesRegex(ValueError, "template is not available"):
            contract.create_department_instance(template_id="dt_content_growth", name="CG", company_id=company)
        with self.database.connect() as con:
            con.execute("update department_templates set source='official',tenant_id='platform' where id='dt_content_growth'")
        with self.assertRaises((ValueError, KeyError)):
            contract.create_department_instance(template_id="dt_content_growth", name="CG", company_id="foreign-company")


if __name__ == "__main__":
    unittest.main()


def test_existing_writing_author_normal_binding_api_preserves_empty_permissions(tmp_path, monkeypatch):
    import pytest
    from dataclasses import replace
    from app.company_execution_policy import CompanyExecutionPolicy
    from app.model_preferences import TenantModelPreferenceResolver
    from app.identity_membership import IdentityMembership
    from test_position_authorization import writing_model_position
    from test_writing_chapter_vertical import scope, COMPANY, CEO
    db, service, employee, key, workspace = writing_model_position(tmp_path)
    original = IdentityMembership._authorize_test
    monkeypatch.setattr(IdentityMembership, "_authorize_test", lambda self, tenant, request:
        replace(original(self, tenant, request), role="ceo"))
    app = create_app(str(db.path))
    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": CEO}
    url = f"/api/workspace/employees/{employee}/capabilities"
    body = {"bindings": [{"capability_source": "tenant_private", "capability_type": "model",
                           "capability_id": key, "priority": 10, "enabled": True}]}
    with TestClient(app) as client:
        response = client.put(url, headers=headers, json=body)
        assert response.status_code == 200, response.text
        saved = response.json()
        assert len(saved["bindings"]) == 1
        assert saved["execution_permission"]["effective_classes"] == []
        assert not saved["execution_permission"]["enabled"]
        binding_id = saved["bindings"][0]["id"]
        response = client.put(url, headers=headers, json={"bindings": [{**body["bindings"][0], "enabled": False}]})
        assert response.status_code == 200, response.text
        assert response.json()["bindings"][0]["id"] == binding_id
        assert not response.json()["bindings"][0]["enabled"]
    with scope():
        assert not service.list_employee_capability_bindings(employee)["bindings"][0]["enabled"]
        grant = CompanyExecutionPolicy(db).current_grant(COMPANY, workspace, key)
        with pytest.raises(ValueError):
            TenantModelPreferenceResolver(db).prepare_employee_model(COMPANY, workspace, employee, key, grant)
        assert not service.list_employee_capability_bindings(employee)["bindings"][0]["enabled"]
        with db.connect() as con:
            assert con.execute("select count(*) from tasks").fetchone()[0] == 0
            assert con.execute("select count(*) from ai_usage_records").fetchone()[0] == 0
