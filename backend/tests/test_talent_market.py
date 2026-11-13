import tempfile
import unittest
import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.agent_conversion.external_candidates import list_external_candidates


class TalentMarketTest(unittest.TestCase):
    def setUp(self):
        os.environ["CURIS_IDENTITY_MODE"] = "test"
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.tmp.name) / "curis.sqlite")
        self.database = Database(self.db_path)
        self.database.initialize()
        self.client = TestClient(create_app(self.db_path))
        self.headers = {"X-Tenant-Id": "talent-test", "X-Ceo-Id": "talent-ceo"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_skill_install_is_idempotent_and_tenant_scoped(self):
        skill_id = "official.skill.requirement_analysis"
        first = self.client.post(
            f"/api/workspace/skills/templates/{skill_id}/install", headers=self.headers
        )
        second = self.client.post(
            f"/api/workspace/skills/templates/{skill_id}/install", headers=self.headers
        )
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 201)
        self.assertEqual(first.json()["skill_template_id"], second.json()["skill_template_id"])
        self.assertEqual(first.json()["created_from_template_id"], skill_id)
        other = self.client.post(
            f"/api/workspace/skills/templates/{skill_id}/install",
            headers={"X-Tenant-Id": "other-tenant", "X-Ceo-Id": "other-ceo"},
        )
        self.assertEqual(other.status_code, 201)
        self.assertNotEqual(first.json()["skill_template_id"], other.json()["skill_template_id"])

    def test_recruit_fails_closed_without_company(self):
        response = self.client.post(
            "/api/workspace/talent-market/recruit",
            headers=self.headers,
            json={
                "company_id": "missing-company",
                "template_id": "et_product_manager",
                "name": "产品经理",
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("company", response.json()["detail"])

    def test_recruit_creates_company_employee_without_department(self):
        company = self.client.post(
            "/api/workspace/companies", headers=self.headers, json={"name": "无部门测试公司"}
        )
        self.assertEqual(company.status_code, 201)
        recruit = self.client.post(
            "/api/workspace/talent-market/recruit",
            headers=self.headers,
            json={
                "company_id": company.json()["company_id"],
                "template_id": "et_product_manager",
                "name": "公司级产品经理",
            },
        )
        self.assertEqual(recruit.status_code, 201)
        self.assertEqual(recruit.json()["employee"]["department_id"], "")
        self.assertTrue(recruit.json()["skills"]["bindings"])

    def test_first_batch_curis_roles_can_all_be_recruited_without_department(self):
        company = self.client.post(
            "/api/workspace/companies", headers=self.headers, json={"name": "五岗位测试公司"}
        )
        self.assertEqual(company.status_code, 201)
        company_id = company.json()["company_id"]
        template_ids = [
            "et_product_manager",
            "et_architect",
            "et_frontend_engineer",
            "et_backend_engineer",
            "et_qa_engineer",
        ]
        for template_id in template_ids:
            response = self.client.post(
                "/api/workspace/talent-market/recruit",
                headers=self.headers,
                json={"company_id": company_id, "template_id": template_id, "name": template_id},
            )
            self.assertEqual(response.status_code, 201, template_id)
            self.assertEqual(response.json()["employee"]["department_id"], "")
            self.assertTrue(response.json()["skills"]["bindings"])

    def test_recruit_creates_employee_with_template_defaults(self):
        company = self.client.post(
            "/api/workspace/companies", headers=self.headers, json={"name": "人才市场测试公司"}
        )
        self.assertEqual(company.status_code, 201)
        company_id = company.json()["company_id"]
        templates = self.client.get("/api/workspace/department-templates", headers=self.headers).json()
        department_template = next(
            item for item in templates["department_templates"]
            if item["department_type"] == "software_rnd"
        )
        department = self.client.post(
            "/api/workspace/departments",
            headers=self.headers,
            json={"template_id": department_template["id"], "company_id": company_id, "name": "研发部"},
        )
        self.assertEqual(department.status_code, 201)
        recruit = self.client.post(
            "/api/workspace/talent-market/recruit",
            headers=self.headers,
            json={
                "company_id": company_id,
                "department_id": department.json()["id"],
                "template_id": "et_product_manager",
                "name": "产品经理",
            },
        )
        self.assertEqual(recruit.status_code, 201)
        self.assertEqual(recruit.json()["employee"]["name"], "产品经理")
        self.assertTrue(recruit.json()["skills"]["bindings"])
        self.assertEqual(recruit.json()["tool_status"], "blocked_required_capability")

    def test_public_agency_candidates_are_read_only_and_gated(self):
        candidates = list_external_candidates()
        self.assertGreaterEqual(len(candidates), 17)
        self.assertTrue(all(item["market_kind"] == "external_candidate" for item in candidates))
        self.assertTrue(all(item["source_status"] == "pending_snapshot_verification" for item in candidates))
        self.assertTrue(all(not item["recruitable"] for item in candidates))

    def test_public_agency_candidates_endpoint_is_available(self):
        response = self.client.get(
            "/api/workspace/talent-market/external-candidates", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()["candidates"]), 17)

    def test_production_line_returns_deduped_resource_pool_and_maturity(self):
        response = self.client.get(
            "/api/workspace/talent-market/production-line", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload["counts"]["discovered"], payload["counts"]["deduped"])
        self.assertTrue(payload["resources"])
        self.assertTrue(
            all(item["maturity"] in {"DISCOVERED", "CANDIDATE", "COMPOSED", "VALIDATED", "CURIS_READY", "BLOCKED"}
                for item in payload["resources"])
        )

    def test_connector_catalog_keeps_discovery_authorization_and_health_separate(self):
        response = self.client.get("/api/connectors", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        connectors = response.json()["connectors"]
        self.assertTrue(connectors)
        self.assertTrue(all(item["discovery_status"] == "discoverable" for item in connectors))
        self.assertTrue(all(item["authorization_status"] == "not_authorized" for item in connectors))
        self.assertTrue(all(item["health_status"] == "unknown" for item in connectors))
        self.assertTrue(all(item["mock_only"] for item in connectors))


if __name__ == "__main__":
    unittest.main()
