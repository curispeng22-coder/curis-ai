"""R1 基线验证 + R2 item1/2 实例化证据测试（Admin 资产复盘）。

证明：从软件公司包 ccp_ai_software_company 实例化 -> 得到 workflow_instances > 0
且无悬空引用（unresolved_refs 三项全空）。与复盘勘误闭环：当前种子 workflow_contents
已含 6 个 wl_* 正确指向 wt_*（见 docs/review/...admin-asset-real-status-review.md 勘误段），
故默认种子即可通过。

复用 093 测试骨架：TemporaryDirectory + create_app + TestClient + CURIS_PLATFORM_ADMIN_TOKEN。
不依赖 092 孤儿实例清理；不修改任何源码或未授权文件。
"""

import os
import json
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.company_instantiation import CompanyInstantiationService
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app
from fastapi.testclient import TestClient

_PLATFORM_ADMIN_TOKEN = "platform-admin-dev"
_TENANT = "t-evidence"


class R2InstantiationEvidenceTest(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", _PLATFORM_ADMIN_TOKEN)
        self.tmp = TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.client = TestClient(create_app(self.db_path))
        self.auth = {"Authorization": f"Bearer {_PLATFORM_ADMIN_TOKEN}"}
        self.tenant = {"X-Tenant-Id": _TENANT}

    def tearDown(self):
        self.tmp.cleanup()

    # ── R2 item1（引用一致）+ R2 item2（实例化 workflow>0）──
    def test_instantiate_yields_workflow_instances_and_no_unresolved(self):
        resp = self.client.post(
            "/api/platform/company-packages/ccp_ai_software_company/instantiate",
            headers={**self.auth, **self.tenant},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()

        self.assertEqual(len(body.get("departments", [])), 1)
        self.assertEqual(len(body.get("employees", [])), 6)
        self.assertEqual(len(body.get("workflows", [])), 6)
        self.assertEqual(len(body.get("snapshots", [])), 13)

        # R2 item1 / 无悬空引用：unresolved_refs 三项全空
        unresolved = body.get("unresolved_refs", {})
        self.assertEqual(unresolved.get("workflow_refs", ["x"]), [])
        self.assertEqual(unresolved.get("skill_refs", ["x"]), [])
        self.assertEqual(unresolved.get("tool_refs", ["x"]), [])

        # 直接查库交叉验证实例数量、wl_* → wt_* 与子包边界。
        conn = sqlite3.connect(self.db_path)
        try:
            self.assertEqual(
                conn.execute(
                    "select count(*) from companies where tenant_id = ?", (_TENANT,)
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                conn.execute(
                    "select count(*) from department_instances where tenant_id = ?", (_TENANT,)
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                conn.execute(
                    "select count(*) from employee_instances where tenant_id = ?", (_TENANT,)
                ).fetchone()[0],
                6,
            )
            self.assertEqual(
                conn.execute(
                    "select count(*) from workflow_instances where tenant_id = ?", (_TENANT,)
                ).fetchone()[0],
                6,
            )
            package = conn.execute(
                "select workflow_refs_json, sub_package_refs_json from company_packages "
                "where company_package_id = 'ccp_ai_software_company'"
            ).fetchone()
            self.assertEqual(json.loads(package[1]), ["cp_content_ops"])
            mappings = conn.execute(
                "select wc.workflow_content_id, wc.workflow_template_ref "
                "from workflow_contents wc join json_each(?) refs "
                "on refs.value = wc.workflow_content_id "
                "join workflow_templates wt on wt.id = wc.workflow_template_ref",
                (package[0],),
            ).fetchall()
            self.assertEqual(len(mappings), 6)
            expected = {row[0]: row[1] for row in mappings}
            expected["wl_ai_rd_software_dev_sop"] = "official.workflow.software_rnd_sop"
            self.assertEqual(
                expected,
                {
                    item["workflow_content_ref"]: item["workflow_template_id"]
                    for item in body["workflows"]
                },
            )
            capability = conn.execute(
                "select connector_ids, workflow_template_ids, employee_template_ids "
                "from capability_packages where package_id = 'cp_content_ops'"
            ).fetchone()
            self.assertEqual(tuple(json.loads(value) for value in capability), ([], [], []))
        finally:
            conn.close()

    # ── 6 条只读 Catalog 路由回归（200 + 行数 > 0）──
    def test_six_catalog_routes_regression(self):
        for route, key in (
            ("/api/platform/company-templates", "company_templates"),
            ("/api/platform/company-packages", "company_packages"),
            ("/api/platform/personas", "persona_templates"),
            ("/api/platform/dashboards", "dashboard_templates"),
            ("/api/platform/tools", "tool_templates"),
            ("/api/platform/workflows", "workflow_templates"),
        ):
            r = self.client.get(route, headers=self.auth)
            self.assertEqual(r.status_code, 200)
            self.assertGreater(len(r.json()[key]), 0)

    def test_tool_and_workflow_capability_states_are_not_overstated(self):
        tools = self.client.get("/api/platform/tools", headers=self.auth).json()[
            "tool_templates"
        ]
        self.assertEqual(len(tools), 115)
        self.assertTrue(all(item["catalog_visible"] for item in tools))
        self.assertTrue(all(not item["configured"] for item in tools))
        self.assertTrue(all(not item["executable"] for item in tools))
        self.assertTrue(all(item["mock_or_stub"] for item in tools))

        workflows = self.client.get("/api/platform/workflows", headers=self.auth).json()[
            "workflow_templates"
        ]
        states = [item["workflow_capability_status"] for item in workflows]
        self.assertGreater(states.count("structured_executable"), 0)
        self.assertEqual(states.count("design_only"), 16)
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                "select steps_json,workflow_capability_status from workflow_templates"
            ).fetchall()
        for steps_json, state in rows:
            steps = json.loads(steps_json)
            structured = bool(steps) and all(
                isinstance(step, dict) and step.get("step_type") for step in steps
            )
            self.assertEqual(
                state,
                "structured_executable" if structured else "design_only",
            )

    def test_workspace_catalog_uses_identity_tenant_not_query_parameter(self):
        with patch.dict(
            os.environ,
            {"CURIS_PRODUCT": "workspace", "CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        ):
            client = TestClient(create_app(self.db_path))
            with sqlite3.connect(self.db_path) as connection:
                connection.executemany(
                    "insert into employee_templates "
                    "(id, slug, name, role, department_type, source, tenant_id, status) "
                    "values (?, ?, ?, 'tenant_probe', 'software_rnd', 'tenant_private', ?, 'active')",
                    (
                        ("tenant-a-probe", "tenant-a-probe", "Tenant A Probe", "tenant-a"),
                        ("tenant-b-probe", "tenant-b-probe", "Tenant B Probe", "tenant-b"),
                    ),
                )
            response = client.get(
                "/api/catalog/templates",
                params={"type": "employee_template", "tenant_id": "tenant-b"},
                headers={"X-Tenant-Id": "tenant-a"},
            )
            self.assertEqual(response.status_code, 200)
            ids = {item["template_id"] for item in response.json()["templates"]}
            self.assertIn("tenant-a-probe", ids)
            self.assertNotIn("tenant-b-probe", ids)
            for route in (
                "/api/platform/company-templates",
                "/api/platform/company-packages",
                "/api/platform/personas",
                "/api/platform/dashboards",
                "/api/platform/tools",
                "/api/platform/workflows",
            ):
                self.assertEqual(client.get(route, headers={"X-Tenant-Id": "tenant-a"}).status_code, 404)

    def test_workspace_db_restores_and_keeps_official_company_package(self):
        workspace_db = str(Path(self.tmp.name) / "workspace.sqlite")
        environment = {
            "CURIS_PRODUCT": "workspace",
            "CURIS_ENV": "test",
            "CURIS_IDENTITY_MODE": "test",
        }
        with patch.dict(os.environ, environment):
            create_app(workspace_db)
            database = Database(workspace_db)
            with database.connect() as connection:
                self.assertEqual(
                    connection.execute("select count(*) from company_packages").fetchone()[0], 1
                )
                self.assertEqual(
                    connection.execute("select count(*) from company_templates").fetchone()[0], 1
                )
                self.assertEqual(
                    connection.execute("select count(*) from capability_packages").fetchone()[0], 1
                )
                connection.execute(
                    "delete from company_packages where company_package_id='ccp_ai_software_company'"
                )
                connection.execute(
                    "delete from company_templates where company_template_id='ct_ai_software_company'"
                )
                connection.execute(
                    "delete from capability_packages where package_id='cp_content_ops'"
                )

            app = create_app(workspace_db)
            app = create_app(workspace_db)
            client = TestClient(app)
            overview = client.get(
                "/api/ceo/overview", headers={"X-Tenant-Id": "tenant-workspace"}
            )
            self.assertEqual(overview.status_code, 200)
            self.assertEqual(
                [item["company_package_id"] for item in overview.json()["company_packages"]],
                ["ccp_ai_software_company"],
            )
            catalog = client.get(
                "/api/catalog/templates",
                params={"type": "company_template"},
                headers={"X-Tenant-Id": "tenant-workspace"},
            )
            self.assertEqual(catalog.status_code, 200)
            self.assertIn(
                "ct_ai_software_company",
                {item["template_id"] for item in catalog.json()["templates"]},
            )

            summary = CompanyInstantiationService(
                database, EvolutionEventLog(database)
            ).instantiate("ccp_ai_software_company", "tenant-workspace")
            self.assertEqual(len(summary["departments"]), 1)
            self.assertEqual(len(summary["employees"]), 6)
            self.assertEqual(len(summary["workflows"]), 6)
            self.assertEqual(summary["unresolved_refs"], {
                "skill_refs": [], "tool_refs": [], "workflow_refs": []
            })

    def test_reconciles_18_employees_and_2_departments_without_deleting(self):
        roles = [
            "architect",
            "backend_engineer",
            "product_manager",
            "qa_engineer",
            "tech_lead",
            *[f"legacy_role_{index}" for index in range(13)],
        ]
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "insert into companies (company_id, tenant_id, name) values ('legacy-company','legacy','Legacy')"
            )
            connection.executemany(
                "insert into department_instances "
                "(id,tenant_id,company_id,template_id,name,department_type) values (?,?,?,?,?,?)",
                (
                    ("legacy-rd", "legacy", "legacy-company", "dt_ai_rd", "研发部", "tech.rd"),
                    ("legacy-content", "legacy", "legacy-company", "dt_ai_content", "内容部", "content.growth"),
                ),
            )
            connection.executemany(
                "insert into employee_instances "
                "(id,tenant_id,company_id,department_id,template_id,name,role,status) "
                "values (?,?,?,?,?,?,?,'idle')",
                [
                    (
                        f"legacy-employee-{index}",
                        "legacy",
                        "legacy-company",
                        "legacy-rd" if index < 6 else "legacy-content",
                        f"legacy-template-{index}",
                        role,
                        role,
                    )
                    for index, role in enumerate(roles)
                ],
            )

        Database(self.db_path).initialize()
        with sqlite3.connect(self.db_path) as connection:
            self.assertEqual(
                connection.execute(
                    "select count(*) from employee_instances where tenant_id='legacy'"
                ).fetchone()[0],
                18,
            )
            self.assertEqual(
                connection.execute(
                    "select count(*) from employee_instances where tenant_id='legacy' "
                    "and template_id in (select id from employee_templates)"
                ).fetchone()[0],
                5,
            )
            self.assertEqual(
                connection.execute(
                    "select count(*) from employee_instances where tenant_id='legacy' "
                    "and status='deprecated' and enabled=0"
                ).fetchone()[0],
                13,
            )
            self.assertEqual(
                connection.execute(
                    "select count(*) from department_instances where tenant_id='legacy' "
                    "and template_id in (select id from department_templates)"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "select count(*) from department_instances where tenant_id='legacy' "
                    "and status='archived' and enabled=0"
                ).fetchone()[0],
                1,
            )

    def test_runtime_referenced_orphan_is_deprecated_not_remapped(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "insert into companies (company_id,tenant_id,name) values ('ref-company','ref','Ref')"
            )
            connection.execute(
                "insert into department_instances "
                "(id,tenant_id,company_id,template_id,name,department_type) "
                "values ('ref-dept','ref','ref-company','dt_engineering','Ref','software_rnd')"
            )
            connection.execute(
                "insert into employee_instances "
                "(id,tenant_id,company_id,department_id,template_id,name,role,status) "
                "values ('ref-employee','ref','ref-company','ref-dept','legacy-architect','Ref','architect','idle')"
            )
            connection.execute(
                "insert into tasks (task_id,content,status,employee_id,tenant_id) "
                "values ('ref-task','referenced','pending','ref-employee','ref')"
            )

        Database(self.db_path).initialize()
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "select template_id,status,enabled from employee_instances where id='ref-employee'"
            ).fetchone()
        self.assertEqual(row, ("legacy-architect", "deprecated", 0))


if __name__ == "__main__":
    unittest.main()
