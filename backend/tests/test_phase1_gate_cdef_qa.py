"""Phase-1 Gate C/D/E/F — 独立验证测试（QA：严过关）。

本文件为 QA 独立补充测试，**不修改任何既有测试**，覆盖工程师 T01–T05 实现的核心 /
风险路径：

- T05 端到端：``POST /api/platform/company-packages/ccp_ai_software_company/instantiate``
  （admin 令牌 + X-Tenant-Id）→ 200；产出 ≥1 部门 / 6 员工 / 6 工作流 / ≥13 快照
  且 follow_latest=0。
- Gate D 鉴权：无令牌→401；未知 ccp id→404；正常 admin→200；正常写 persona→201。
- Gate E 注入：et_backend_engineer 实例快照列含
  persona_ref=pt_direct_executor / default_skill=skl_ai_rd_python_development /
  default_tool=tl_ai_rd_code_executor。
- Gate C：dashboard_widget_catalog 单一真相源；token_cost→ai_cost / tech_risk→project_risk
  去重；目录仅存规范 id、DashboardTemplate.widget_ids 全部指向已有 catalog 行。
- T01：docs/contracts 6 处 patch 落实 + 6 张新表存在 + 前缀/去重常量单一真相源。

全部基于 fresh temp DB + TestClient，互不污染。
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

from app.catalog_constants import (
    TEMPLATE_ID_PREFIXES,
    is_valid_company_package_id,
    is_valid_template_id,
    normalize_widget_id,
)
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app

# backend/tests/ -> repo root（docs/contracts 位于 repo 根）
REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = REPO_ROOT / "docs" / "contracts"

PLATFORM_ADMIN_TOKEN = os.getenv("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
ADMIN_HEADERS = {"Authorization": f"Bearer {PLATFORM_ADMIN_TOKEN}"}


class Phase1GateCDEFRoutingTest(unittest.TestCase):
    """Gate D/F 路由层 + 端到端串联（HTTP 层，带 admin 令牌 / X-Tenant-Id）。"""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    # ── T05 端到端 ────────────────────────────────────────────────────────
    def test_t05_instantiate_ccp_e2e_200_and_counts(self) -> None:
        """ccp_ai_software_company 实例化 → 200，产出 ≥1 部门 / 6 员工 / 6 工作流 / ≥13 快照。"""
        response = self.client.post(
            "/api/platform/company-packages/ccp_ai_software_company/instantiate",
            headers={**ADMIN_HEADERS, "X-Tenant-Id": "tenant-qa"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertGreaterEqual(len(payload["departments"]), 1)
        self.assertEqual(len(payload["employees"]), 6)
        self.assertEqual(len(payload["workflows"]), 6)
        self.assertGreaterEqual(len(payload["snapshots"]), 13)
        # 每个部门 / 员工 / 工作流都对应一条快照 id
        snapshotted = (
            len(payload["departments"])
            + len(payload["employees"])
            + len(payload["workflows"])
        )
        self.assertEqual(len(payload["snapshots"]), snapshotted)

    def test_t05_snapshots_follow_latest_isolated(self) -> None:
        """每条 template_version_snapshots 的 follow_latest 必须为 0（快照隔离）。"""
        self.client.post(
            "/api/platform/company-packages/ccp_ai_software_company/instantiate",
            headers={**ADMIN_HEADERS, "X-Tenant-Id": "tenant-qa"},
        )
        with closing(sqlite3.connect(self.db_path)) as connection:
            rows = connection.execute(
                "select follow_latest from template_version_snapshots"
            ).fetchall()
        self.assertGreaterEqual(len(rows), 13)
        self.assertTrue(all(row[0] == 0 for row in rows), rows)

    # ── Gate E 注入 ───────────────────────────────────────────────────────
    def test_gate_e_employee_injection_snapshot_columns(self) -> None:
        """et_backend_engineer 实例快照列冻结 persona_ref / default_skill / default_tool。"""
        response = self.client.post(
            "/api/platform/company-packages/ccp_ai_software_company/instantiate",
            headers={**ADMIN_HEADERS, "X-Tenant-Id": "tenant-qa"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        employees = response.json()["employees"]
        backend = next(
            e for e in employees if e["template_id"] == "et_backend_engineer"
        )
        self.assertEqual(backend["persona_ref"], "pt_direct_executor")
        self.assertEqual(backend["default_skill"], "skl_ai_rd_python_development")
        self.assertEqual(backend["default_tool"], "tl_ai_rd_code_executor")

        # DB 层 employee_instances 列同样冻结
        with closing(sqlite3.connect(self.db_path)) as connection:
            row = connection.execute(
                "select persona_ref, default_skill, default_tool "
                "from employee_instances where template_id = 'et_backend_engineer' limit 1"
            ).fetchone()
        self.assertEqual(row[0], "pt_direct_executor")
        self.assertEqual(row[1], "skl_ai_rd_python_development")
        self.assertEqual(row[2], "tl_ai_rd_code_executor")

    # ── Gate D 鉴权 ───────────────────────────────────────────────────────
    def test_gate_d_no_token_returns_401(self) -> None:
        """缺 admin 令牌 → 401。"""
        payload = {
            "persona_id": "pt_auth_probe",
            "slug": "auth-probe",
            "name": "Auth Probe",
            "archetype": "direct_executor",
        }
        response = self.client.post("/api/platform/personas", json=payload)
        self.assertEqual(response.status_code, 401)

    def test_gate_d_unknown_ccp_returns_404(self) -> None:
        """未知 ccp id → 404（KeyError 映射）。"""
        response = self.client.post(
            "/api/platform/company-packages/ccp_does_not_exist/instantiate",
            headers={**ADMIN_HEADERS, "X-Tenant-Id": "tenant-qa"},
        )
        self.assertEqual(response.status_code, 404)

    def test_gate_d_valid_admin_instantiate_200(self) -> None:
        """正常 admin 令牌 + 已知 ccp → 200。"""
        response = self.client.post(
            "/api/platform/company-packages/ccp_ai_software_company/instantiate",
            headers={**ADMIN_HEADERS, "X-Tenant-Id": "tenant-qa"},
        )
        self.assertEqual(response.status_code, 200)

    def test_gate_d_create_persona_201(self) -> None:
        """正常 admin 写 persona → 201，落 pt_* 行。"""
        payload = {
            "persona_id": "pt_qa_probe",
            "slug": "qa-probe",
            "name": "QA Probe Persona",
            "archetype": "risk_aware_guardian",
        }
        response = self.client.post(
            "/api/platform/personas", json=payload, headers=ADMIN_HEADERS
        )
        self.assertEqual(response.status_code, 201, response.text)
        body = response.json()
        self.assertEqual(body["persona_id"], "pt_qa_probe")
        self.assertEqual(body["archetype"], "risk_aware_guardian")

    # ── Gate C 单一真相源 ─────────────────────────────────────────────────
    def test_gate_c_widget_catalog_dedup(self) -> None:
        """GET /api/catalog/widgets 仅含规范 id；弃用别名 token_cost/tech_risk 不进目录。"""
        response = self.client.get("/api/catalog/widgets")
        self.assertEqual(response.status_code, 200)
        ids = {w["widget_id"] for w in response.json()["widgets"]}
        self.assertIn("ai_cost", ids)
        self.assertIn("project_risk", ids)
        self.assertNotIn("token_cost", ids)
        self.assertNotIn("tech_risk", ids)

    def test_gate_c_dashboard_widget_refs_resolve(self) -> None:
        """DashboardTemplate.widget_ids 全部指向已存在的 catalog 行（引用完整性）。"""
        widgets = self.client.get("/api/catalog/widgets").json()["widgets"]
        catalog_ids = {w["widget_id"] for w in widgets}
        dashboards = self.client.get(
            "/api/catalog/templates", params={"type": "dashboard_template"}
        ).json()["templates"]
        self.assertTrue(dashboards)
        for dash in dashboards:
            for wid in dash["metadata"]["widget_ids"]:
                self.assertIn(wid, catalog_ids, f"{dash['template_id']} -> {wid}")

    def test_gate_c_deprecated_alias_normalized_at_service(self) -> None:
        """服务层 create_widget 把 token_cost/tech_risk 归一为规范 id（单一真相源）。"""
        from app.catalog_authoring import CatalogAuthoringService

        service = CatalogAuthoringService(self.database, EvolutionEventLog(self.database))
        row = service.create_widget("token_cost", domain="cost")
        self.assertEqual(row["widget_id"], "ai_cost")
        row2 = service.create_widget("tech_risk", domain="project", data_class="tech")
        self.assertEqual(row2["widget_id"], "project_risk")


class Phase1T01ContractsAndSchemaTest(unittest.TestCase):
    """T01：契约 patch 落实 + 6 张新表存在 + 前缀/去重常量单一真相源。"""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_six_new_tables_exist(self) -> None:
        """T01 新建 6 张表均存在。"""
        expected = {
            "company_packages",
            "persona_templates",
            "dashboard_templates",
            "workflow_contents",
            "dashboard_widget_catalog",
            "template_version_snapshots",
        }
        with closing(sqlite3.connect(self.db_path)) as connection:
            actual = {
                r[0]
                for r in connection.execute(
                    "select name from sqlite_master where type='table'"
                ).fetchall()
            }
        self.assertTrue(expected.issubset(actual), actual - expected)

    def _read_contract(self, name: str) -> str:
        path = CONTRACTS_DIR / name
        self.assertTrue(path.exists(), f"missing contract file: {name}")
        return path.read_text(encoding="utf-8")

    def test_contract_template_catalog_regex_patched(self) -> None:
        text = self._read_contract("template-catalog-runtime-contract.md")
        self.assertIn("pt_|wl_|dtpl_", text)
        self.assertIn("ccp_", text)

    def test_contract_ai_company_template_system_patched(self) -> None:
        text = self._read_contract("ai-company-template-system.md")
        self.assertIn("dtpl_", text)
        self.assertIn("pt_", text)

    def test_contract_template_versioning_policy_patched(self) -> None:
        text = self._read_contract("template-versioning-policy.md")
        self.assertIn("dtpl_", text)
        self.assertIn("pt_", text)

    def test_contract_company_package_patched(self) -> None:
        text = self._read_contract("company-package-contract.md")
        self.assertIn("persona_refs", text)
        self.assertIn("ccp_", text)

    def test_contract_dashboard_template_admin_patched(self) -> None:
        text = self._read_contract("dashboard-template-admin-contract.md")
        self.assertIn("ai_commercial", text)
        self.assertIn("role_visibility", text)

    def test_contract_workflow_template_patched(self) -> None:
        text = self._read_contract("workflow-template-contract.md")
        self.assertIn("wl_", text)


class Phase1CatalogConstantsTest(unittest.TestCase):
    """T01/T02：前缀 / 去重常量单一真相源（catalog_constants.py）。"""

    def test_template_id_prefixes_include_new_classes(self) -> None:
        for prefix in (
            "ct_", "dt_", "et_", "wt_", "st_", "tt_", "pt_", "wl_", "dtpl_"
        ):
            self.assertIn(prefix, TEMPLATE_ID_PREFIXES, prefix)

    def test_prefix_and_dedup_validation(self) -> None:
        self.assertTrue(is_valid_template_id("pt_direct_executor"))
        self.assertTrue(is_valid_template_id("dtpl_ai_rd_ceo_cockpit"))
        self.assertTrue(is_valid_company_package_id("ccp_ai_software_company"))
        # ccp_* 不属于目录 template_id 正则
        self.assertFalse(is_valid_template_id("ccp_ai_software_company"))
        # Gate C 去重归一
        self.assertEqual(normalize_widget_id("token_cost"), "ai_cost")
        self.assertEqual(normalize_widget_id("tech_risk"), "project_risk")
        self.assertEqual(normalize_widget_id("ai_cost"), "ai_cost")


if __name__ == "__main__":
    unittest.main()
