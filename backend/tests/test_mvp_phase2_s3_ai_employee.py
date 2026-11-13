from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}
ROOT = Path(__file__).resolve().parents[2]


class MVPPhase2S3AIEmployeeTests(unittest.TestCase):
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

    def test_create_employee_bind_profile_update_status_and_isolate_tenant(self):
        company = self.client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department_response = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "研发部",
            },
        )
        self.assertEqual(department_response.status_code, 201, department_response.text)
        department = department_response.json()

        templates = self.client.get(
            "/api/workspace/employee-templates", headers=TENANT_A
        ).json()["employee_templates"]
        template = next(
            item
            for item in templates
            if item["department_type"] == department["department_type"]
            and item["role"] == "tech_lead"
        )
        employee_response = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": template["id"],
                "name": "研发负责人",
                "instructions_override": "负责技术方案、任务拆解与代码质量。",
                "status": "idle",
                "enabled": True,
            },
        )
        self.assertEqual(employee_response.status_code, 201, employee_response.text)
        employee = employee_response.json()
        self.assertEqual(employee["role"], "tech_lead")
        self.assertEqual(
            employee["instructions_override"],
            "负责技术方案、任务拆解与代码质量。",
        )

        selector = self.client.get(
            "/api/workspace/capabilities/selector", headers=TENANT_A
        ).json()["capabilities"]
        capability = next(
            item
            for item in selector
            if item["enabled"]
            and item["source"] == "official"
            and item["capability_type"] in {"model", "tool", "connector"}
        )
        profile_response = self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT_A,
            json={
                "bindings": [
                    {
                        "capability_source": capability["source"],
                        "capability_type": capability["capability_type"],
                        "capability_id": capability["capability_id"],
                        "priority": 10,
                        "enabled": True,
                    }
                ]
            },
        )
        self.assertEqual(profile_response.status_code, 200, profile_response.text)
        bindings = profile_response.json()["bindings"]
        self.assertEqual(len(bindings), 1)
        self.assertEqual(bindings[0]["capability_id"], capability["capability_id"])

        updated = self.client.patch(
            f"/api/workspace/employees/{employee['id']}",
            headers=TENANT_A,
            json={
                "name": "技术负责人",
                "instructions_override": "负责技术交付与质量。",
                "status": "assigned",
            },
        )
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["status"], "assigned")
        self.assertEqual(updated.json()["name"], "技术负责人")

        tenant_a_employees = self.client.get(
            "/api/workspace/employees", headers=TENANT_A
        ).json()["employees"]
        tenant_b_employees = self.client.get(
            "/api/workspace/employees", headers=TENANT_B
        ).json()["employees"]
        self.assertEqual([item["id"] for item in tenant_a_employees], [employee["id"]])
        self.assertEqual(tenant_b_employees, [])

    def test_employee_pages_use_real_api_and_no_sample_or_local_draft(self):
        paths = [
            ROOT / "frontend/app/ceo-office/organization/employees/page.js",
            ROOT / "frontend/app/ceo-office/organization/employees/EmployeeFormDrawer.js",
            ROOT / "frontend/app/ceo-office/organization/employees/[id]/page.js",
            ROOT / "frontend/app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("SAMPLE_EMP", source)
        self.assertNotIn("本地草稿", source)
        self.assertIn("createEmployee", source)
        self.assertIn("setEmployeeCapabilities", source)
        self.assertIn("updateEmployee", source)
        self.assertIn("deleteEmployee", source)
        for label in ("空闲", "工作中", "已完成", "异常", "已暂停"):
            self.assertIn(label, source)


if __name__ == "__main__":
    unittest.main()
