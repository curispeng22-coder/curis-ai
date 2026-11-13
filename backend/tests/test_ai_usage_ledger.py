from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
import urllib.error
from decimal import Decimal
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.ai_usage import AIUsageService
from app.database import Database
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter
from app.tenant_context import TenantContext


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class AIUsageServiceTests(unittest.TestCase):
    def setUp(self):
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.database = Database(self.db_path)
        self.database.initialize()
        self.service = AIUsageService(self.database)
        self._seed_lineage("tenant-a")

    def _seed_lineage(self, tenant_id: str):
        with self.database.connect() as connection:
            connection.execute(
                "insert or ignore into tenants (tenant_id, name) values (?, ?)",
                (tenant_id, tenant_id),
            )
            connection.execute(
                "insert into companies (company_id, tenant_id, name) values (?, ?, ?)",
                (f"company-{tenant_id}", tenant_id, "Company"),
            )
            connection.execute(
                "insert into department_instances "
                "(id, tenant_id, company_id, template_id, name, department_type) "
                "values (?, ?, ?, 'official.department.software_rnd', '业务部', 'business.general')",
                (f"department-{tenant_id}", tenant_id, f"company-{tenant_id}"),
            )
            connection.execute(
                "insert into employee_instances "
                "(id, tenant_id, company_id, department_id, template_id, name, role) "
                "values (?, ?, ?, ?, 'official.employee.tech_lead', '员工', 'tech_lead')",
                (
                    f"employee-{tenant_id}",
                    tenant_id,
                    f"company-{tenant_id}",
                    f"department-{tenant_id}",
                ),
            )
            connection.execute(
                "insert into projects "
                "(project_id, tenant_id, company_id, department_id, name, goal) "
                "values (?, ?, ?, ?, '项目', '目标')",
                (
                    f"project-{tenant_id}",
                    tenant_id,
                    f"company-{tenant_id}",
                    f"department-{tenant_id}",
                ),
            )
            connection.execute(
                "insert into tasks "
                "(task_id, tenant_id, company_id, project_id, employee_id, content, status, state_flow) "
                "values (?, ?, ?, ?, ?, '任务', 'RUNNING', '[\"RUNNING\"]')",
                (
                    f"task-{tenant_id}",
                    tenant_id,
                    f"company-{tenant_id}",
                    f"project-{tenant_id}",
                    f"employee-{tenant_id}",
                ),
            )
            connection.execute(
                "insert or ignore into official_models "
                "(model_key, provider_id, display_name, supported_models, gateway_ref, "
                "status, default_model, type, name) "
                "values ('model.test', 'provider', 'Model', '[\"model-a\"]', "
                "'gateway', 'active', 'model-a', 'model', 'Model')"
            )

    def _record(self, *, key: str, **overrides):
        values = {
            "tenant_id": "tenant-a",
            "model_gateway_id": "gateway",
            "provider_id": "provider",
            "model_name": "model-a",
            "input_tokens": 8,
            "output_tokens": 4,
            "total_tokens": 12,
            "cost_amount": Decimal("0.001200"),
            "currency": "USD",
            "cost_source": "provider_reported",
            "price_version": None,
            "employee_id": "employee-tenant-a",
            "capability_id": "model.test",
            "capability_type": "model",
            "task_id": "task-tenant-a",
            "project_id": "project-tenant-a",
            "department_id": "department-tenant-a",
            "request_id": "request-a",
            "execution_status": "success",
            "metering_status": "confirmed",
            "idempotency_key": key,
            "logical_call_id": "logical-a",
            "attempt_no": 1,
        }
        values.update(overrides)
        return self.service.record_call(**values)

    def test_record_is_linked_idempotent_immutable_and_sensitive_free(self):
        with TenantContext.scope("tenant-a"):
            first = self._record(key="same-key")
            second = self._record(key="same-key")
            record = self.service.get_record(first)
        self.assertEqual(first, second)
        self.assertEqual(record["department_id"], "department-tenant-a")
        self.assertEqual(record["cost_amount"], "0.0012")
        self.assertEqual(record["total_tokens"], 12)
        for forbidden in ("prompt", "response", "answer", "api_key", "credential", "raw_response"):
            self.assertNotIn(forbidden, record)
        with self.assertRaises(sqlite3.DatabaseError), self.database.connect() as connection:
            connection.execute(
                "update ai_usage_records set model_name = 'changed' where usage_record_id = ?",
                (first,),
            )
        with self.assertRaises(sqlite3.DatabaseError), self.database.connect() as connection:
            connection.execute(
                "delete from ai_usage_records where usage_record_id = ?",
                (first,),
            )

    def test_retry_fallback_aggregation_and_unknown_metering(self):
        with TenantContext.scope("tenant-a"):
            self._record(
                key="attempt-1",
                input_tokens=None,
                output_tokens=None,
                total_tokens=None,
                cost_amount=None,
                cost_source="unknown",
                price_version=None,
                execution_status="gateway_error",
                metering_status="unknown",
                attempt_no=1,
            )
            self._record(
                key="attempt-2",
                cost_amount=Decimal("0.002500"),
                cost_source="estimated",
                price_version="price-v1",
                model_name="model-b",
                attempt_no=2,
                fallback_from_model="model-a",
                fallback_reason="gateway_error",
            )
            summary = self.service.aggregate(group_by="model")
            records = self.service.list_records()
        self.assertEqual(summary["totals"]["call_count"], 2)
        self.assertEqual(summary["totals"]["total_tokens"], 12)
        self.assertEqual(summary["totals"]["estimated_cost"], "0.0025")
        self.assertIsNone(summary["totals"]["confirmed_cost"])
        self.assertEqual(summary["totals"]["unmetered_count"], 1)
        self.assertEqual(summary["totals"]["success_count"], 1)
        self.assertEqual(summary["totals"]["failed_count"], 1)
        self.assertEqual(sum(item["total_tokens"] or 0 for item in records), 12)
        self.assertEqual({item["logical_call_id"] for item in records}, {"logical-a"})
        self.assertEqual({item["attempt_no"] for item in records}, {1, 2})

    def test_cross_tenant_reads_and_writes_fail_closed(self):
        with TenantContext.scope("tenant-a"):
            usage_record_id = self._record(key="tenant-key")
        with TenantContext.scope("tenant-b"):
            self.assertEqual(self.service.list_records(), [])
            with self.assertRaises(KeyError):
                self.service.get_record(usage_record_id)
            with self.assertRaises(PermissionError):
                self._record(key="cross-key")


class _FallbackHttpPost:
    def __call__(self, url, payload, headers, timeout):
        if payload["model"] == "preferred-model":
            raise urllib.error.HTTPError(url, 503, "unavailable", {}, None)
        return {
            "choices": [{"message": {"content": "完成"}}],
            "usage": {
                "prompt_tokens": 6,
                "completion_tokens": 4,
                "total_tokens": 10,
                "estimated_cost": 0.0042,
            },
        }


class AIUsageGatewayIntegrationTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_MODEL_GATEWAY_PRICE_VERSION": "test-v1",
            },
        )
        environment.start()
        self.addCleanup(environment.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="secret-not-for-ledger",
            gateway_id="newapi",
            model_name="fallback-model",
            http_post=_FallbackHttpPost(),
        )
        self.client = TestClient(create_app(self.db_path, model_gateway_adapter=adapter))
        self.addCleanup(self.client.close)

    def test_each_outbound_fallback_attempt_is_recorded_once(self):
        model = self.client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT_A,
            json={
                "capability_key": "model.preferred",
                "type": "model",
                "name": "首选模型",
                "provider_id": "newapi",
                "model_name": "preferred-model",
                "description": "聚焦测试",
            },
        )
        self.assertEqual(model.status_code, 201, model.text)
        company = self.client.get("/api/workspace/companies", headers=TENANT_A).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "业务部",
            },
        ).json()
        employee = self.client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "员工",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        project = self.client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "项目",
                "goal": "验证账本",
                "owner_employee_id": employee["id"],
            },
        ).json()
        self.client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT_A,
            json={
                "bindings": [{
                    "capability_source": "official",
                    "capability_type": "model",
                    "capability_id": "model.preferred",
                    "priority": 1,
                    "enabled": True,
                }]
            },
        )
        task = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={
                "content": "执行模型调用",
                "employee_id": employee["id"],
                "capability_source": "official",
                "capability_type": "model",
                "capability_id": "model.preferred",
            },
        ).json()
        started = self.client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks/{task['task_id']}/jobs",
            headers=TENANT_A,
        )
        self.assertEqual(started.status_code, 202, started.text)
        records_response = self.client.get("/api/ai-usage/records", headers=TENANT_A)
        self.assertEqual(records_response.status_code, 200, records_response.text)
        records = records_response.json()["records"]
        self.assertEqual(len(records), 2)
        self.assertEqual({item["attempt_no"] for item in records}, {1, 2})
        self.assertEqual(len({item["logical_call_id"] for item in records}), 1)
        summary = self.client.get("/api/ai-usage/summary", headers=TENANT_A).json()["totals"]
        self.assertEqual(summary["call_count"], 2)
        self.assertEqual(summary["estimated_cost"], "0.0042")
        self.assertEqual(summary["unmetered_count"], 1)
        cross_tenant = self.client.get(
            "/api/ai-usage/summary?tenant_id=tenant-a",
            headers=TENANT_B,
        )
        self.assertEqual(cross_tenant.status_code, 200)
        self.assertEqual(cross_tenant.json()["totals"]["call_count"], 0)
        self.assertNotIn("secret-not-for-ledger", str(records_response.json()))

    def test_admin_product_cannot_read_workspace_usage_routes(self):
        with patch.dict(os.environ, {"CURIS_PRODUCT": "admin"}):
            response = self.client.get(
                "/api/ai-usage/records",
                headers={"X-Tenant-Id": "tenant-a"},
            )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
