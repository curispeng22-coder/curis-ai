from __future__ import annotations

import os
import tempfile
import threading
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.model_gateway import ModelGatewayAdapter
from app.task_execution_control import TaskExecutionControlService
from app.tenant_context import TenantContext


TENANT_A = {"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"}
TENANT_B = {"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"}


class SignalExecutor:
    def __init__(self, status: str) -> None:
        self.status = status
        self.calls = 0

    def execute(self, _prompt: str) -> dict:
        self.calls += 1
        if self.status == "awaiting_input":
            return {
                "status": "awaiting_input",
                "question": "请补充目标受众",
                "context_summary": "执行到受众确认步骤",
                "resume_parameters": {"required": ["audience"]},
            }
        if self.status == "human_handoff":
            return {
                "status": "human_handoff",
                "question": "请人工确认发布范围",
                "context_summary": "自动执行已停止",
            }
        return {"output": "恢复后完成", "cost": 0}


class UsageHttpPost:
    def __call__(self, url, payload, _headers, _timeout):
        if payload["model"] == "preferred-model":
            raise urllib.error.HTTPError(url, 503, "unavailable", {}, None)
        return {
            "choices": [{"message": {"content": "模型完成"}}],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 3,
                "total_tokens": 8,
                "estimated_cost": 0.001,
            },
        }


class DigitalEmployeeExecutionControlLoopTests(unittest.TestCase):
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
        self.clients: list[TestClient] = []

    def _client(self, *, executor=None, model_gateway_adapter=None) -> TestClient:
        client = TestClient(
            create_app(
                self.db_path,
                tool_functions=None if model_gateway_adapter else {"default_tool": executor.execute},
                model_gateway_adapter=model_gateway_adapter,
            )
        )
        self.clients.append(client)
        self.addCleanup(client.close)
        return client

    @staticmethod
    def _lineage(client: TestClient, *, model: bool = False):
        company = client.get("/api/workspace/companies", headers=TENANT_A).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=TENANT_A,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "业务部",
            },
        ).json()
        employee = client.post(
            "/api/workspace/employees",
            headers=TENANT_A,
            json={
                "department_id": department["id"],
                "template_id": "official.employee.tech_lead",
                "name": "数字员工",
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
                "name": "执行闭环",
                "goal": "验证暂停恢复",
                "owner_employee_id": employee["id"],
            },
        ).json()
        capability = {
            "capability_source": "official",
            "capability_type": "model" if model else "tool",
            "capability_id": "model.execution" if model else "tool.execution",
        }
        created = client.post(
            "/api/workspace/capabilities/registry",
            headers=TENANT_A,
            json={
                "capability_key": capability["capability_id"],
                "type": capability["capability_type"],
                "name": "执行能力",
                "provider_id": "newapi" if model else "local",
                "model_name": "preferred-model" if model else "",
                "description": "执行闭环聚焦测试",
            },
        )
        if created.status_code not in {201, 409} and "已存在" not in created.text:
            raise AssertionError(created.text)
        client.put(
            f"/api/workspace/employees/{employee['id']}/capabilities",
            headers=TENANT_A,
            json={"bindings": [{**capability, "priority": 1, "enabled": True}]},
        )
        task = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks",
            headers=TENANT_A,
            json={
                "content": "执行一次闭环任务",
                "employee_id": employee["id"],
                **capability,
            },
        ).json()
        return project, employee, task

    def _start(self, client, project, task):
        response = client.post(
            f"/api/workspace/projects/{project['project_id']}/tasks/{task['task_id']}/jobs",
            headers=TENANT_A,
        )
        self.assertEqual(response.status_code, 202, response.text)

    def test_model_call_timeline_references_each_usage_record_once(self):
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="test-only-key",
            gateway_id="newapi",
            model_name="fallback-model",
            http_post=UsageHttpPost(),
        )
        client = self._client(model_gateway_adapter=adapter)
        project, _employee, task = self._lineage(client, model=True)
        self._start(client, project, task)

        timeline = client.get(
            f"/api/workspace/task-runs/{task['task_id']}/timeline",
            headers=TENANT_A,
        ).json()["events"]
        records = client.get("/api/ai-usage/records", headers=TENANT_A).json()["records"]
        model_events = [event for event in timeline if event["event_type"] == "model_called"]

        self.assertEqual(
            [event["event_type"] for event in timeline],
            [
                "execution_started",
                "capability_selected",
                "knowledge_retrieved",
                "model_called",
                "model_called",
                "tool_called",
                "execution_completed",
            ],
        )
        self.assertEqual(len(records), 2)
        self.assertEqual(
            {event["usage_record_id"] for event in model_events},
            {record["usage_record_id"] for record in records},
        )
        for key in (
            "tenant_id",
            "department_id",
            "project_id",
            "task_id",
            "task_run_id",
            "employee_id",
            "capability_id",
        ):
            self.assertTrue(model_events[0][key], key)
        response_text = str(timeline).lower()
        for forbidden in ("prompt", "answer", "api_key", "credential", "raw_response"):
            self.assertNotIn(forbidden, response_text)

    def test_awaiting_input_survives_restart_and_resumes_the_same_task_run(self):
        executor = SignalExecutor("awaiting_input")
        client = self._client(executor=executor)
        project, _employee, task = self._lineage(client)
        self._start(client, project, task)
        task_id = task["task_id"]

        state = client.get(
            f"/api/workspace/task-runs/{task_id}", headers=TENANT_A
        ).json()
        self.assertEqual(state["status"], "awaiting_input")
        self.assertEqual(state["current_step"], "1")
        self.assertEqual(executor.calls, 1)

        client.close()
        resumed_executor = SignalExecutor("success")
        restarted = self._client(executor=resumed_executor)
        persisted = restarted.get(
            f"/api/workspace/task-runs/{task_id}", headers=TENANT_A
        ).json()
        self.assertEqual(persisted["pending_question"], "请补充目标受众")
        supplied = restarted.post(
            f"/api/workspace/task-runs/{task_id}/input",
            headers=TENANT_A,
            json={
                "input_summary": "目标受众为现有付费客户",
                "resume_parameters": {"audience": "existing_customers"},
            },
        )
        self.assertEqual(supplied.status_code, 200, supplied.text)
        resumed = restarted.post(
            f"/api/workspace/task-runs/{task_id}/resume",
            headers=TENANT_A,
            json={},
        )
        self.assertEqual(resumed.status_code, 202, resumed.text)
        job = restarted.get(f"/api/workspace/jobs/{task_id}", headers=TENANT_A).json()
        self.assertEqual(job["status"], "completed")
        self.assertEqual(job["task_id"], task_id)
        self.assertEqual(resumed_executor.calls, 1)
        timeline = restarted.get(
            f"/api/workspace/task-runs/{task_id}/timeline",
            headers=TENANT_A,
        ).json()["events"]
        types = [event["event_type"] for event in timeline]
        self.assertIn("awaiting_input", types)
        self.assertIn("input_supplied", types)
        self.assertIn("execution_resumed", types)
        self.assertEqual(types[-1], "execution_completed")

    def test_handoff_stops_automation_until_accept_or_resume_and_cancel_is_terminal(self):
        executor = SignalExecutor("human_handoff")
        client = self._client(executor=executor)
        project, _employee, task = self._lineage(client)
        self._start(client, project, task)
        task_id = task["task_id"]
        self.assertEqual(executor.calls, 1)

        accepted = client.post(
            f"/api/workspace/task-runs/{task_id}/handoff/accept",
            headers=TENANT_A,
        )
        self.assertEqual(accepted.status_code, 200, accepted.text)
        reassigned = client.patch(
            f"/api/workspace/task-runs/{task_id}/handoff/assignee",
            headers=TENANT_A,
            json={"assignee_id": "owner-2"},
        )
        self.assertEqual(reassigned.status_code, 422, reassigned.text)
        reassigned = client.patch(
            f"/api/workspace/task-runs/{task_id}/handoff/assignee",
            headers=TENANT_A,
            json={"assignee_id": accepted.json()["handoff_assignee_id"]},
        )
        self.assertEqual(reassigned.status_code, 200, reassigned.text)
        self.assertEqual(executor.calls, 1)

        cancelled = client.post(
            f"/api/workspace/task-runs/{task_id}/cancel",
            headers=TENANT_A,
            json={"reason": "人工决定终止"},
        )
        self.assertEqual(cancelled.status_code, 200, cancelled.text)
        self.assertEqual(cancelled.json()["status"], "cancelled")
        blocked_resume = client.post(
            f"/api/workspace/task-runs/{task_id}/resume",
            headers=TENANT_A,
            json={},
        )
        self.assertEqual(blocked_resume.status_code, 422)
        self.assertEqual(executor.calls, 1)

    def test_control_reads_are_tenant_isolated_and_secret_like_input_is_rejected(self):
        executor = SignalExecutor("awaiting_input")
        client = self._client(executor=executor)
        project, _employee, task = self._lineage(client)
        self._start(client, project, task)
        task_id = task["task_id"]

        self.assertEqual(
            client.get(
                f"/api/workspace/task-runs/{task_id}", headers=TENANT_B
            ).status_code,
            404,
        )
        rejected = client.post(
            f"/api/workspace/task-runs/{task_id}/input",
            headers=TENANT_A,
            json={
                "input_summary": "Authorization: Bearer secret-value",
                "resume_parameters": {},
            },
        )
        self.assertEqual(rejected.status_code, 422)
        for forbidden in (
            "prompt",
            "answer",
            "chain_of_thought",
            "raw_response",
            "apiKey",
            "chainOfThought",
            "rawResponse",
            "accessToken",
            "estimatedCost",
            "modelAnswer",
            "systemPrompt",
        ):
            response = client.post(
                f"/api/workspace/task-runs/{task_id}/input",
                headers=TENANT_A,
                json={
                    "input_summary": "安全补充信息",
                    "resume_parameters": {forbidden: "should-not-persist"},
                },
            )
            self.assertEqual(response.status_code, 422, forbidden)
        nested = client.post(
            f"/api/workspace/task-runs/{task_id}/input",
            headers=TENANT_A,
            json={
                "input_summary": "安全补充信息",
                "resume_parameters": {"safe": {"modelAnswer": "should-not-persist"}},
            },
        )
        self.assertEqual(nested.status_code, 422)
        supplied = client.post(
            f"/api/workspace/task-runs/{task_id}/input",
            headers=TENANT_A,
            json={
                "input_summary": "安全补充信息",
                "resume_parameters": {"audience": "owner"},
            },
        )
        self.assertEqual(supplied.status_code, 200, supplied.text)
        self.assertNotIn("resume_parameters", supplied.json())
        task_payload = client.get(f"/api/task/{task_id}", headers=TENANT_A).json()
        self.assertNotIn("resume_parameters_json", task_payload)

    def test_concurrent_resume_and_cancel_handoff_use_atomic_state_transitions(self):
        executor = SignalExecutor("awaiting_input")
        client = self._client(executor=executor)
        project, _employee, task = self._lineage(client)
        self._start(client, project, task)
        task_id = task["task_id"]
        database = Database(self.db_path)
        service = TaskExecutionControlService(database, EvolutionEventLog(database))

        def race(actions):
            barrier = threading.Barrier(2)
            lock = threading.Lock()
            reads = 0
            original = service._task_context

            def synchronized_read(target):
                nonlocal reads
                value = original(target)
                with lock:
                    reads += 1
                    should_wait = reads <= 2
                if should_wait:
                    barrier.wait(timeout=5)
                return value

            service._task_context = synchronized_read

            def invoke(action):
                with TenantContext.scope("tenant-a", ceo_id="ceo-a"):
                    try:
                        action()
                        return "ok"
                    except ValueError:
                        return "rejected"

            try:
                with ThreadPoolExecutor(max_workers=2) as pool:
                    return list(pool.map(invoke, actions))
            finally:
                service._task_context = original

        results = race([
            lambda: service.resume(task_id, {}),
            lambda: service.resume(task_id, {}),
        ])
        self.assertEqual(sorted(results), ["ok", "rejected"])
        with TenantContext.scope("tenant-a", ceo_id="ceo-a"):
            resumed_events = [
                event
                for event in service.list_timeline(task_id)
                if event["event_type"] == "execution_resumed"
            ]
        self.assertEqual(len(resumed_events), 1)

        second_project, _second_employee, second = self._lineage(client)
        self._start(client, second_project, second)
        second_id = second["task_id"]
        results = race([
            lambda: service.cancel(second_id, "并发取消"),
            lambda: service.request_handoff(
                second_id,
                current_step="1",
                question="并发接管",
                context_summary="安全摘要",
            ),
        ])
        self.assertEqual(sorted(results), ["ok", "rejected"])
        with TenantContext.scope("tenant-a", ceo_id="ceo-a"):
            state = service.get_state(second_id)
            if state["status"] == "human_handoff":
                service.cancel(second_id, "终态确认")
            with self.assertRaises(ValueError):
                service.request_handoff(
                    second_id,
                    current_step="1",
                    question="不得复活",
                    context_summary="安全摘要",
                )


if __name__ == "__main__":
    unittest.main()
