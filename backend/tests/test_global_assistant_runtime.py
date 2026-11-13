from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch
import json

from fastapi.testclient import TestClient

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app
from app.model_gateway import (
    ModelGatewayAdapter,
    R3_BASE_URL,
    R3_CAPABILITY_ID,
    R3_GATEWAY_ID,
    R3_MODEL_ID,
    R3_PROFILE,
)
from app.tenant_context import TenantContext


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class GlobalAssistantRuntimeTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(
            os.environ,
            {"CURIS_ENV": "test", "CURIS_IDENTITY_MODE": "test"},
        )
        environment.start()
        self.addCleanup(environment.stop)
        handle = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = handle.name
        handle.close()
        self.addCleanup(
            lambda: os.path.exists(self.db_path) and os.unlink(self.db_path)
        )
        self.clients: list[TestClient] = []

    def _client(self, model_gateway_adapter=None) -> TestClient:
        client = TestClient(
            create_app(
                self.db_path,
                tool_functions=(
                    None
                    if model_gateway_adapter
                    else {
                        "default_tool": lambda _prompt: {
                            "output": "Assistant Task 已完成",
                            "cost": 0,
                        }
                    }
                ),
                model_gateway_adapter=model_gateway_adapter,
            )
        )
        self.clients.append(client)
        self.addCleanup(client.close)
        return client

    @staticmethod
    def _lineage(client: TestClient, *, status: str = "active"):
        company = client.get(
            "/api/workspace/companies", headers=TENANT_A
        ).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "小红书业务部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "内容负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        project = client.post(
            "/api/workspace/projects",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "小红书内容增长",
                "goal": "持续生产高质量选题",
                "owner_employee_id": employee["id"],
                "status": status,
            },
        ).json()
        return company, department, employee, project

    def test_identity_is_user_owned_persistent_and_tenant_isolated(self):
        client = self._client()
        empty = client.get(
            "/api/workspace/assistant/identity", headers=TENANT_A
        ).json()
        self.assertEqual(
            {key: empty[key] for key in ("name", "avatar", "role", "tone", "personality")},
            {"name": "", "avatar": "", "role": "", "tone": "", "personality": ""},
        )

        saved = client.put(
            "/api/workspace/assistant/identity",
            headers=TENANT_A,
            json={
                "name": "小助手",
                "avatar": "🌿",
                "role": "CEO 秘书",
                "tone": "简洁",
                "personality": "主动、克制",
            },
        )
        self.assertEqual(saved.status_code, 200, saved.text)
        self.assertEqual(saved.json()["name"], "小助手")

        client.close()
        restarted = self._client()
        self.assertEqual(
            restarted.get(
                "/api/workspace/assistant/identity", headers=TENANT_A
            ).json()["personality"],
            "主动、克制",
        )
        tenant_b = restarted.get(
            "/api/workspace/assistant/identity", headers=TENANT_B
        ).json()
        self.assertEqual(tenant_b["name"], "")

    def test_snapshot_aggregates_real_pending_risk_usage_and_artifacts(self):
        client = self._client()
        _company, _department, employee, project = self._lineage(
            client, status="blocked"
        )
        pending = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "等待 CEO 补充范围", "employee_id": employee["id"]},
        ).json()
        failed = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={"content": "历史失败 Task", "employee_id": employee["id"]},
        ).json()
        database = Database(self.db_path)
        with database.connect() as connection:
            connection.execute(
                "update tasks set status='AWAITING_INPUT' where tenant_id=? and task_id=?",
                ("tenant-a", pending["task_id"]),
            )
            connection.execute(
                "update tasks set status='FAILED' where tenant_id=? and task_id=?",
                ("tenant-a", failed["task_id"]),
            )
            connection.execute(
                """
                insert into ai_usage_records (
                  usage_record_id, tenant_id, model_gateway_id, provider_id,
                  model_name, input_tokens, output_tokens, total_tokens,
                  cost_amount, currency, cost_source, employee_id, capability_id,
                  capability_type, task_id, project_id, department_id, request_id,
                  execution_status, metering_status, occurred_at, idempotency_key
                ) values (
                  'usage-unmetered', 'tenant-a', 'gateway', 'provider', 'model',
                  null, null, null, null, 'USD', 'unknown', ?, 'model.test',
                  'model', ?, ?, ?, 'request-1', 'failed', 'unknown',
                  '2026-07-30T00:00:00Z', 'assistant-unmetered'
                )
                """,
                (
                    employee["id"],
                    failed["task_id"],
                    project["project_id"],
                    project["department_id"],
                ),
            )

        snapshot = client.get(
            "/api/workspace/assistant/snapshot", headers=TENANT_A
        )
        self.assertEqual(snapshot.status_code, 200, snapshot.text)
        payload = snapshot.json()
        self.assertEqual(payload["brief"]["counts"]["business_departments"], 1)
        self.assertEqual(payload["brief"]["counts"]["projects"], 1)
        self.assertEqual(payload["brief"]["ai_usage"]["unmetered_count"], 1)
        self.assertEqual(payload["pending"][0]["task_id"], pending["task_id"])
        risk_types = {item["type"] for item in payload["risks"]}
        self.assertTrue(
            {"project_blocked", "task_failed", "ai_usage_unmetered", "ai_usage_failed"}
            <= risk_types
        )

    def test_query_reads_project_and_business_department_facts(self):
        client = self._client()
        _company, department, _employee, project = self._lineage(client)

        project_query = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_A,
            json={
                "command": "当前项目进展怎么样？",
                "intent": "query",
                "context": {
                    "page": "project",
                    "project_id": project["project_id"],
                },
            },
        )
        self.assertEqual(project_query.status_code, 202, project_query.text)
        self.assertEqual(project_query.json()["facts"]["scope"], "project")
        self.assertEqual(
            project_query.json()["facts"]["project_id"], project["project_id"]
        )

        business_query = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_A,
            json={
                "command": "当前小红书业务部怎么样？",
                "intent": "auto",
                "context": {"page": "ceo-office"},
            },
        )
        self.assertEqual(
            business_query.json()["facts"]["scope"], "business_department"
        )
        self.assertEqual(
            business_query.json()["facts"]["department_id"], department["id"]
        )

    def test_execute_command_creates_and_runs_existing_task(self):
        with patch.dict(
            os.environ,
            {
                "CURIS_ENV": "development",
                "CURIS_PRODUCT": "workspace",
                "CURIS_LOCAL_OWNER_ENABLED": "1",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            adapter = ModelGatewayAdapter(
                base_url=R3_BASE_URL,
                api_key="test-key-not-a-real-secret",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=lambda _url, _payload, _headers, _timeout: {
                    "choices": [
                        {"message": {"content": "Assistant 真实链模拟结果"}}
                    ],
                    "usage": {
                        "prompt_tokens": 12,
                        "completion_tokens": 8,
                        "total_tokens": 20,
                    },
                },
            )
            client = self._client(adapter)
            company, _department, employee, project = self._lineage(client)
            no_binding = client.post(
                "/api/workspace/assistant/commands",
                headers=TENANT_A,
                json={
                    "command": "让内容负责人生成10个选题",
                    "intent": "execute",
                    "context": {
                        "page": "project",
                        "project_id": project["project_id"],
                    },
                },
            )
            self.assertEqual(no_binding.status_code, 202, no_binding.text)
            self.assertEqual(no_binding.json()["status"], "awaiting_capability")

            binding_response = client.put(
                f"/api/workspace/employees/{employee['id']}/capabilities",
                headers=TENANT_A,
                json={
                    "bindings": [
                        {
                            "capability_source": "official",
                            "capability_type": "model",
                            "capability_id": R3_CAPABILITY_ID,
                            "priority": 1,
                            "enabled": True,
                        }
                    ]
                },
            )
            self.assertEqual(
                binding_response.status_code, 200, binding_response.text
            )
            binding_id = binding_response.json()["bindings"][0]["id"]

            response = client.post(
                "/api/workspace/assistant/commands",
                headers=TENANT_A,
                json={
                    "command": "让内容负责人生成10个选题",
                    "intent": "execute",
                    "context": {
                        "page": "project",
                        "project_id": project["project_id"],
                    },
                },
            )
            self.assertEqual(response.status_code, 202, response.text)
            result = response.json()
            self.assertEqual(result["status"], "queued")
            self.assertEqual(result["capability_id"], R3_CAPABILITY_ID)
            task = client.get(
                f"/api/task/{result['task_id']}", headers=TENANT_A
            ).json()
            self.assertEqual(task["project_id"], project["project_id"])
            self.assertEqual(task["employee_id"], employee["id"])
            self.assertEqual(task["content"], "让内容负责人生成10个选题")
            self.assertEqual(task["status"], "COMPLETED")
            self.assertEqual(
                task["requested_capability_id"], R3_CAPABILITY_ID
            )

            database = Database(self.db_path)
            with database.connect() as connection:
                usage = connection.execute(
                    "select * from ai_usage_records where tenant_id=? and task_id=?",
                    ("tenant-a", result["task_id"]),
                ).fetchall()
                model_event = connection.execute(
                    "select payload from evolution_events "
                    "where tenant_id=? and correlation_id=? "
                    "and event_type='usage.model_call'",
                    ("tenant-a", result["task_id"]),
                ).fetchone()
                artifact = connection.execute(
                    "select artifact_id from artifacts where tenant_id=? and task_id=?",
                    ("tenant-a", result["task_id"]),
                ).fetchone()
            self.assertEqual(len(usage), 1)
            self.assertEqual(usage[0]["capability_binding_id"], binding_id)
            self.assertEqual(usage[0]["total_tokens"], 20)
            self.assertGreater(float(usage[0]["cost_amount"]), 0)
            self.assertIsNotNone(model_event)
            self.assertEqual(
                json.loads(model_event["payload"])["usage_record_id"],
                usage[0]["usage_record_id"],
            )
            timeline = client.get(
                f"/api/workspace/task-runs/{result['task_id']}/timeline",
                headers=TENANT_A,
            ).json()["events"]
            model_calls = [
                event for event in timeline if event["event_type"] == "model_called"
            ]
            self.assertEqual(len(model_calls), 1)
            self.assertEqual(
                model_calls[0]["usage_record_id"], usage[0]["usage_record_id"]
            )
            timeline_text = json.dumps(timeline).lower()
            for forbidden in ("prompt", "answer", "api_key", "credential"):
                self.assertNotIn(forbidden, timeline_text)
            self.assertIsNotNone(artifact)

        missing_context = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_A,
            json={
                "command": "生成10个选题",
                "intent": "execute",
                "context": {"page": "ceo-office"},
            },
        ).json()
        self.assertEqual(missing_context["status"], "awaiting_context")

        other_department = client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "电商业务部",
            },
        ).json()
        other_employee = client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": other_department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "电商负责人",
                "status": "idle",
                "enabled": True,
            },
        ).json()
        wrong_department = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_A,
            json={
                "command": f"让电商负责人执行{project['name']}",
                "intent": "execute",
                "context": {
                    "page": "ceo-office",
                    "employee_id": other_employee["id"],
                },
            },
        )
        self.assertEqual(wrong_department.status_code, 422, wrong_department.text)

    def test_notifications_are_whitelisted_and_cross_tenant_context_fails_closed(self):
        client = self._client()
        _company, _department, _employee, project = self._lineage(client)
        database = Database(self.db_path)
        event_log = EvolutionEventLog(database)
        with TenantContext.scope("tenant-a"):
            event_log.record(
                correlation_id="task-sensitive",
                event_type="execution_failed",
                payload={
                    "task_id": "task-sensitive",
                    "project_id": project["project_id"],
                    "prompt": "do not return",
                    "api_key": "secret",
                    "raw_response": "private",
                },
            )
        notifications = client.get(
            "/api/workspace/assistant/notifications", headers=TENANT_A
        )
        self.assertEqual(notifications.status_code, 200, notifications.text)
        text = notifications.text.lower()
        for forbidden in ("prompt", "api_key", "raw_response", "secret", "private"):
            self.assertNotIn(forbidden, text)
        self.assertEqual(
            notifications.json()["notifications"][-1]["entity_refs"]["task_id"],
            "task-sensitive",
        )
        self.assertEqual(
            client.get(
                "/api/workspace/assistant/notifications", headers=TENANT_B
            ).json()["notifications"],
            [],
        )
        cross_tenant = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_B,
            json={
                "command": "项目状态怎么样？",
                "intent": "query",
                "context": {
                    "page": "project",
                    "project_id": project["project_id"],
                },
            },
        )
        self.assertEqual(cross_tenant.status_code, 404)

        unsafe_page = client.post(
            "/api/workspace/assistant/commands",
            headers=TENANT_A,
            json={
                "command": "项目状态怎么样？",
                "intent": "query",
                "context": {"page": "api_key=must-not-enter-events"},
            },
        )
        self.assertEqual(unsafe_page.status_code, 422, unsafe_page.text)
        self.assertNotIn(
            "must-not-enter-events",
            client.get(
                "/api/workspace/assistant/notifications", headers=TENANT_A
            ).text,
        )


if __name__ == "__main__":
    unittest.main()
