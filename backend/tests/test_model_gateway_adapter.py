import hashlib
import json
import os
import sqlite3
import tempfile
import unittest
import urllib.error
import uuid
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.workflow_runtime import WorkflowRuntime
from app.model_gateway import (
    ModelGatewayAdapter,
    ModelGatewayExecutionError,
    R3_BASE_URL,
    R3_CAPABILITY_ID,
    R3_GATEWAY_ID,
    R3_WORKFLOW_CONTEXT_MAX_BYTES,
    R3_MODEL_ID,
    R3_PROFILE,
    R3_PROVIDER_ID,
)


class RecordingHttpPost:
    def __init__(self, response: dict):
        self.response = response
        self.calls = []

    def __call__(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        self.calls.append(
            {
                "url": url,
                "payload": payload,
                "headers": headers,
                "timeout": timeout,
            }
        )
        return self.response


class SequencedRecordingHttpPost(RecordingHttpPost):
    def __call__(self, url: str, payload: dict, headers: dict, timeout: int) -> dict:
        order = len(self.calls) + 1
        self.response = {
            "choices": [
                {"message": {"content": f"ORIGINAL-STEP-{order}-" + ("研发结果" * 2_000)}}
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 7, "total_tokens": 12},
        }
        return super().__call__(url, payload, headers, timeout)


class RecordingGateway:
    def __init__(self):
        self.prompts = []

    def execute(self, prompt: str) -> dict:
        self.prompts.append(prompt)
        return {
            "output": "gateway result",
            "cost": 0.0021,
            "model_gateway_id": "newapi-main",
            "model_name": "newapi-model-a",
            "prompt_tokens": 12,
            "completion_tokens": 30,
            "total_tokens": 42,
            "token": 42,
            "estimated_cost": 0.0021,
            "status": "success",
        }


class SecretLeakingGateway:
    def execute(self, prompt: str) -> dict:
        return {
            "output": "safe gateway result",
            "cost": 0.0021,
            "model_gateway_id": "newapi-main",
            "model_name": "deepseek-v4-flash",
            "prompt_tokens": 3,
            "completion_tokens": 4,
            "total_tokens": 7,
            "token": 7,
            "estimated_cost": 0.0021,
            "status": "failed Authorization: Bearer sk-or-v1-secret-value-1234567890",
            "api_key": "sk-or-v1-secret-value-1234567890",
            "prompt": prompt,
            "raw_response": {"output": "raw model output should not persist"},
        }


class ModelGatewayAdapterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(
            os.environ,
            {"CURIS_PLATFORM_ADMIN_TOKEN": "platform-admin-dev"},
        )
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_unusable_provider_response_is_marked_as_an_outbound_attempt(self):
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="test-secret",
            gateway_id="newapi",
            model_name="test-model",
            http_post=RecordingHttpPost({}),
        )

        with self.assertRaises(ModelGatewayExecutionError) as caught:
            adapter.execute("prompt")

        self.assertEqual(caught.exception.status, "response_invalid")
        self.assertTrue(caught.exception.outbound_attempted)

    def _r3_workflow(self, http_post):
        adapter = ModelGatewayAdapter(
            base_url=R3_BASE_URL,
            api_key="test-secret",
            gateway_id=R3_GATEWAY_ID,
            model_name=R3_MODEL_ID,
            http_post=http_post,
        )
        db_path = str(Path(self.tmp.name) / f"r3-{id(http_post)}.sqlite")
        app = create_app(db_path, model_gateway_adapter=adapter)
        if os.getenv("CURIS_IDENTITY_MODE") == "gateway":
            @app.middleware("http")
            async def trusted_gateway_source(request, call_next):
                request.scope["client"] = ("10.0.0.2", 12345)
                return await call_next(request)

            with Database(db_path).connect() as connection:
                connection.execute(
                    "insert into tenants (tenant_id, name) values ('tenant-r3', 'tenant-r3')"
                )
                connection.execute(
                    "insert into companies (company_id, tenant_id, ceo_id, name, is_default) "
                    "values ('company-r3', 'tenant-r3', 'ceo-r3', 'R3 Company', 1)"
                )
                connection.execute(
                    "insert into tenant_memberships "
                    "(membership_id, issuer, subject_id, tenant_id, company_id, ceo_id, role, status) "
                    "values (?, 'https://issuer.example', 'subject-r3', 'tenant-r3', "
                    "'company-r3', 'ceo-r3', 'owner', 'active')",
                    (str(uuid.uuid4()),),
                )
            headers = {
                "X-Tenant-Id": "tenant-r3",
                "X-Curis-Gateway-Subject": "subject-r3",
                "X-Curis-Gateway-Issuer": "https://issuer.example",
                "X-Curis-Gateway-Auth-Time": "1720000000",
                "X-Curis-Gateway-Request-Id": "request-r3",
            }
        else:
            headers = {"X-Tenant-Id": "tenant-r3", "X-Ceo-Id": "ceo-r3"}
        client = TestClient(app)
        company = client.get("/api/workspace/companies", headers=headers).json()["companies"][0]
        department = client.post(
            "/api/workspace/departments",
            headers=headers,
            json={"template_id": "official.department.software_rnd", "name": "R3 研发部"},
        ).json()
        templates = client.get(
            "/api/workspace/employee-templates", headers=headers
        ).json()["employee_templates"]
        employees = {}
        for role in (
            "tech_lead",
            "product_manager",
            "architect",
            "frontend_engineer",
            "backend_engineer",
            "qa_engineer",
        ):
            template = next(item for item in templates if item["role"] == role)
            employees[role] = client.post(
                "/api/workspace/employees",
                headers=headers,
                json={
                    "department_id": department["id"],
                    "template_id": template["id"],
                    "name": f"R3 {role}",
                    "enabled": True,
                },
            ).json()
        employee = employees["tech_lead"]
        project = client.post(
            "/api/workspace/projects",
            headers=headers,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "owner_employee_id": employee["id"],
                "name": "R3 Project",
                "goal": "Produce one traceable model result",
                "status": "active",
            },
        ).json()
        bindings = {}
        for role, role_employee in employees.items():
            bindings[role] = client.put(
                f"/api/workspace/employees/{role_employee['id']}/capabilities",
                headers=headers,
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
            ).json()["bindings"][0]
        binding = bindings["tech_lead"]
        workflow = client.post(
            "/api/workspace/workflows",
            headers=headers,
            json={
                "workflow_template_id": "official.workflow.software_rnd_sop",
                "department_id": department["id"],
                "company_id": company["company_id"],
                "project_id": project["project_id"],
                "content": "Implement the approved R3 slice",
            },
        ).json()
        os.environ.update(
            {
                "CURIS_R3_APPROVED_TENANT_ID": "tenant-r3",
                "CURIS_R3_APPROVED_PROJECT_ID": project["project_id"],
                "CURIS_R3_APPROVED_WORKFLOW_RUN_ID": workflow["workflow_run_id"],
                "CURIS_R3_APPROVED_CAPABILITY_BINDINGS": json.dumps(
                    {role: item["id"] for role, item in bindings.items()}
                ),
            }
        )
        return client, headers, workflow, project, binding, db_path

    @staticmethod
    def _record_r3_outbound(
        db_path: str,
        workflow_run_id: str,
        workflow_step_id: str,
        *,
        estimated_cost: float | None = 0.001,
    ) -> None:
        with Database(db_path).connect() as connection:
            run = connection.execute(
                "select wr.company_id, wr.project_id, wr.department_id, wr.task_id, "
                "ws.employee_role, ws.status "
                "from workflow_runs wr join workflow_steps ws on ws.workflow_run_id=wr.workflow_run_id "
                "where wr.workflow_run_id=? and ws.workflow_step_id=?",
                (workflow_run_id, workflow_step_id),
            ).fetchone()
            if run["status"] == "succeeded":
                existing_result = connection.execute(
                    "select 1 from step_results where tenant_id='tenant-r3' and workflow_step_id=?",
                    (workflow_step_id,),
                ).fetchone()
                if existing_result is None:
                    employee_id = connection.execute(
                        "select id from employee_instances where tenant_id='tenant-r3' "
                        "and department_id=? and role=? and enabled=1 order by created_at, id limit 1",
                        (run["department_id"], run["employee_role"]),
                    ).fetchone()[0]
                    connection.execute(
                        "insert into step_results "
                        "(step_result_id, tenant_id, workflow_step_id, employee_id, result, status) "
                        "values (?, 'tenant-r3', ?, ?, 'recorded prior result', 'succeeded')",
                        (f"wfrs-{uuid.uuid4()}", workflow_step_id, employee_id),
                    )
        approved_bindings = json.loads(os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"])
        with Database(db_path).connect() as connection:
            employee_id = connection.execute(
                "select id from employee_instances where tenant_id='tenant-r3' "
                "and department_id=? and role=? and enabled=1 order by created_at, id limit 1",
                (run["department_id"], run["employee_role"]),
            ).fetchone()[0]
            usage_record_id = f"usage-{uuid.uuid4()}"
            connection.execute(
                "insert into ai_usage_records ("
                "usage_record_id, tenant_id, model_gateway_id, provider_id, model_name, "
                "input_tokens, output_tokens, total_tokens, cost_amount, currency, cost_source, "
                "price_version, employee_id, capability_id, capability_type, task_id, project_id, "
                "department_id, request_id, execution_status, metering_status, occurred_at, "
                "idempotency_key, workflow_run_id, workflow_step_id, capability_binding_id, "
                "logical_call_id, attempt_no, http_status"
                ") values (?, 'tenant-r3', ?, ?, ?, 60, 40, 100, ?, 'USD', ?, ?, ?, ?, "
                "'model', ?, ?, ?, 'fixture-request', 'success', 'confirmed', "
                "'2026-07-29T00:00:00Z', ?, ?, ?, ?, 'fixture-logical', 1, 200)",
                (
                    usage_record_id,
                    R3_GATEWAY_ID,
                    R3_PROVIDER_ID,
                    R3_MODEL_ID,
                    estimated_cost,
                    "estimated" if estimated_cost is not None else "unknown",
                    "2026-07-17" if estimated_cost is not None else None,
                    employee_id,
                    R3_CAPABILITY_ID,
                    run["task_id"],
                    run["project_id"],
                    run["department_id"],
                    f"fixture-{usage_record_id}",
                    workflow_run_id,
                    workflow_step_id,
                    approved_bindings[run["employee_role"]],
                ),
            )
        payload = {
            "usage_record_id": usage_record_id,
            "workflow_run_id": workflow_run_id,
            "workflow_step_id": workflow_step_id,
            "outbound_attempted": True,
            "ceo_id": "ceo-r3",
            "company_id": run["company_id"],
            "project_id": run["project_id"],
            "capability_binding_id": approved_bindings[run["employee_role"]],
            "model_gateway_id": R3_GATEWAY_ID,
            "model_name": R3_MODEL_ID,
        }
        EvolutionEventLog(Database(db_path)).record(
            correlation_id=workflow_run_id,
            event_type="usage.model_call",
            tenant_id="tenant-r3",
            payload=payload,
        )

    def test_adapter_posts_openai_compatible_payload_to_new_api(self):
        http_post = RecordingHttpPost(
            {
                "choices": [{"message": {"content": "adapter output"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                    "estimated_cost": 0.0042,
                },
            }
        )
        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key="test-key",
            gateway_id="newapi-main",
            model_name="newapi-model-a",
            http_post=http_post,
        )

        result = adapter.execute("Run through gateway")

        self.assertEqual(http_post.calls[0]["url"], "https://newapi.example.com/v1/chat/completions")
        self.assertEqual(http_post.calls[0]["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(http_post.calls[0]["payload"]["model"], "newapi-model-a")
        self.assertEqual(http_post.calls[0]["payload"]["messages"], [{"role": "user", "content": "Run through gateway"}])
        self.assertEqual(result["output"], "adapter output")
        self.assertEqual(result["model_gateway_id"], "newapi-main")
        self.assertEqual(result["model_name"], "newapi-model-a")
        self.assertEqual(result["token"], 15)
        self.assertEqual(result["estimated_cost"], 0.0042)
        self.assertEqual(result["status"], "success")

    def test_r3_contract_uses_fixed_path_limits_and_approved_price(self):
        http_post = RecordingHttpPost(
            {
                "choices": [{"message": {"content": "approved output"}}],
                "usage": {
                    "prompt_tokens": 1000,
                    "completion_tokens": 500,
                    "total_tokens": 1500,
                },
            }
        )
        with patch.dict(os.environ, {"CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE}):
            adapter = ModelGatewayAdapter(
                base_url=R3_BASE_URL,
                api_key="test-secret",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=http_post,
            )
            result = adapter.execute("approved prompt")

        call = http_post.calls[0]
        self.assertEqual(call["url"], f"{R3_BASE_URL}/v1/chat/completions")
        self.assertEqual(call["payload"]["model"], R3_MODEL_ID)
        self.assertEqual(call["payload"]["max_completion_tokens"], 2048)
        self.assertEqual(call["timeout"], 60)
        self.assertEqual(result["estimated_cost"], 0.003)
        self.assertEqual(result["price_version"], "2026-07-17")
        self.assertEqual(result["http_status"], 200)

    def test_r3_contract_rejects_unapproved_config_and_oversized_input_before_network(self):
        http_post = RecordingHttpPost({})
        with patch.dict(os.environ, {"CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE}):
            bad = ModelGatewayAdapter(
                base_url="https://other.example",
                api_key="test-secret",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=http_post,
            )
            with self.assertRaisesRegex(RuntimeError, "approved contract"):
                bad.execute("prompt")

            missing_secret = ModelGatewayAdapter(
                base_url=R3_BASE_URL,
                api_key="",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=http_post,
            )
            with self.assertRaises(ModelGatewayExecutionError) as missing_context:
                missing_secret.execute("prompt")
            self.assertEqual(missing_context.exception.http_status, 401)

            approved = ModelGatewayAdapter(
                base_url=R3_BASE_URL,
                api_key="test-secret",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=http_post,
            )
            with self.assertRaises(ModelGatewayExecutionError) as context:
                approved.execute("x" * 8193)

        self.assertEqual(context.exception.http_status, 422)
        self.assertFalse(context.exception.outbound_attempted)
        self.assertEqual(http_post.calls, [])

    def test_r3_contract_classifies_429_without_retry_or_secret_leak(self):
        calls = []

        def rate_limited(url, payload, headers, timeout):
            calls.append(url)
            raise urllib.error.HTTPError(url, 429, "secret upstream text", {}, None)

        with patch.dict(os.environ, {"CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE}):
            adapter = ModelGatewayAdapter(
                base_url=R3_BASE_URL,
                api_key="test-secret",
                gateway_id=R3_GATEWAY_ID,
                model_name=R3_MODEL_ID,
                http_post=rate_limited,
            )
            with self.assertRaises(ModelGatewayExecutionError) as context:
                adapter.execute("approved prompt")

        self.assertEqual(len(calls), 1)
        self.assertEqual(context.exception.http_status, 429)
        self.assertEqual(context.exception.status, "rate_limited")
        self.assertNotIn("secret", str(context.exception))

    def test_workspace_seeds_only_approved_r3_model_metadata_without_secret(self):
        db_path = str(Path(self.tmp.name) / "r3-catalog.sqlite")
        with patch.dict(os.environ, {"CURIS_PRODUCT": "workspace"}):
            create_app(db_path)

        with sqlite3.connect(db_path) as connection:
            model = connection.execute(
                "select model_key, provider_id, gateway_ref, default_model from official_models"
            ).fetchone()
            gateway = connection.execute(
                "select gateway_id, base_url, credential_ref, default_model from model_gateways"
            ).fetchone()
        self.assertEqual(model, (R3_CAPABILITY_ID, "openai", R3_GATEWAY_ID, R3_MODEL_ID))
        self.assertEqual(gateway, (R3_GATEWAY_ID, R3_BASE_URL, None, R3_MODEL_ID))

    def test_r3_workflow_records_scoped_model_usage_and_approved_cost(self):
        calls = RecordingHttpPost(
            {
                "choices": [{"message": {"content": "traceable R3 result"}}],
                "usage": {"prompt_tokens": 5, "completion_tokens": 7, "total_tokens": 12},
            }
        )
        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, project, binding, db_path = self._r3_workflow(calls)
            response = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )
            with sqlite3.connect(db_path) as connection:
                event = json.loads(
                    connection.execute(
                        "select payload from evolution_events where event_type='usage.model_call' "
                        "order by event_id desc limit 1"
                    ).fetchone()[0]
                )
                usage_record = connection.execute(
                    "select usage_record_id, total_tokens, cost_amount, http_status "
                    "from ai_usage_records order by created_at desc limit 1"
                ).fetchone()
                stored_input = connection.execute(
                    "select ws.input, e.prompt from workflow_steps ws "
                    "join workflow_runs wr on wr.workflow_run_id=ws.workflow_run_id "
                    "join executions e on e.task_id=wr.task_id "
                    "where wr.workflow_run_id=? and ws.status='succeeded' "
                    "order by ws.step_order, e.execution_id desc limit 1",
                    (workflow["workflow_run_id"],),
                ).fetchone()

        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["steps"][0]["status"], "succeeded")
        self.assertEqual(len(calls.calls), 1)
        self.assertIn("project_id", event, event)
        self.assertEqual(event["project_id"], project["project_id"])
        self.assertEqual(event["workflow_run_id"], workflow["workflow_run_id"])
        self.assertEqual(event["capability_binding_id"], binding["id"])
        self.assertEqual(event["model_name"], R3_MODEL_ID)
        self.assertEqual(event["usage_record_id"], usage_record[0])
        self.assertNotIn("total_tokens", event)
        self.assertNotIn("estimated_cost", event)
        self.assertEqual(usage_record[1], 12)
        self.assertAlmostEqual(float(usage_record[2]), 0.00003525)
        self.assertEqual(usage_record[3], 200)
        self.assertNotIn("test-secret", str(event))
        self.assertEqual(stored_input, ("[REDACTED:R3_MODEL_INPUT]", "[REDACTED:R3_MODEL_INPUT]"))

    def test_r3_workflow_allows_seven_ordered_steps_once(self):
        calls = SequencedRecordingHttpPost({})
        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, _, _, db_path = self._r3_workflow(calls)
            observed_types = []
            for expected_calls in range(1, 8):
                response = client.post(
                    f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                    headers=headers,
                )
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(len(calls.calls), expected_calls)
                observed_types.append(response.json()["steps"][expected_calls - 1]["step_type"])
            completed = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )
            with sqlite3.connect(db_path) as connection:
                stored_results = connection.execute(
                    "select sr.result from step_results sr "
                    "join workflow_steps ws on ws.workflow_step_id=sr.workflow_step_id "
                    "order by ws.step_order"
                ).fetchall()
                stored_executions = connection.execute(
                    "select output from executions order by created_at, execution_id"
                ).fetchall()

        self.assertEqual(
            observed_types,
            [
                "tech_lead_breakdown",
                "requirement_clarification",
                "architecture_design",
                "frontend_execution",
                "backend_execution",
                "qa_verification",
                "final_report",
            ],
        )
        self.assertEqual(completed.json()["status"], "succeeded")
        self.assertEqual(len(calls.calls), 7)
        self.assertTrue(
            all(
                len(call["payload"]["messages"][0]["content"].encode("utf-8"))
                <= R3_WORKFLOW_CONTEXT_MAX_BYTES
                for call in calls.calls
            )
        )
        expected_outputs = [
            f"ORIGINAL-STEP-{order}-" + ("研发结果" * 2_000) for order in range(1, 8)
        ]
        self.assertEqual([row[0] for row in stored_results], expected_outputs)
        self.assertCountEqual([row[0] for row in stored_executions], expected_outputs)
        final_prompt = calls.calls[-1]["payload"]["messages"][0]["content"]
        self.assertIn("ORIGINAL-STEP-6-", final_prompt)
        self.assertIn("ORIGINAL-STEP-5-", final_prompt)
        self.assertIn("[TRUNCATED:step_result:", final_prompt)
        detail = client.get(
            f"/api/workspace/workflows/{workflow['workflow_run_id']}", headers=headers
        ).json()
        repeated = client.get(
            f"/api/workspace/workflows/{workflow['workflow_run_id']}", headers=headers
        ).json()
        artifact = detail["artifact"]
        report_bytes = detail["final_report"].encode("utf-8")
        self.assertEqual(artifact["artifact_type"], "document_report")
        self.assertEqual(artifact["content"], detail["final_report"])
        self.assertEqual(artifact["content_length"], len(report_bytes))
        self.assertEqual(artifact["content_sha256"], hashlib.sha256(report_bytes).hexdigest())
        self.assertEqual(artifact["tenant_id"], "tenant-r3")
        self.assertEqual(artifact["company_id"], workflow["company_id"])
        self.assertEqual(artifact["project_id"], workflow["project_id"])
        self.assertEqual(artifact["workflow_run_id"], workflow["workflow_run_id"])
        self.assertEqual(artifact["task_id"], workflow["task_id"])
        self.assertEqual(len(artifact["step_references"]), 7)
        self.assertEqual(len(artifact["usage_record_references"]), 7)
        self.assertEqual(artifact["model_gateway_id"], R3_GATEWAY_ID)
        self.assertEqual(artifact["model_name"], R3_MODEL_ID)
        self.assertEqual(artifact["total_tokens"], 84)
        self.assertAlmostEqual(artifact["estimated_cost"], 0.00024675)
        self.assertEqual(detail["project_status"]["execution_status"], "completed")
        self.assertIsNone(detail["project_status"]["next_step_suggestion"])
        self.assertEqual(repeated["artifact"], artifact)
        self.assertEqual(len(calls.calls), 7)

    def test_r3_workflow_rejects_duplicate_result_history_before_network(self):
        calls = RecordingHttpPost({})
        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, _, _, db_path = self._r3_workflow(calls)
            with sqlite3.connect(db_path) as connection:
                first_step = connection.execute(
                    "select workflow_step_id from workflow_steps where workflow_run_id=? "
                    "order by step_order limit 1",
                    (workflow["workflow_run_id"],),
                ).fetchone()[0]
                connection.execute(
                    "update workflow_steps set status='succeeded' where workflow_step_id=?",
                    (first_step,),
                )
            self._record_r3_outbound(db_path, workflow["workflow_run_id"], first_step)
            with sqlite3.connect(db_path) as connection:
                existing = connection.execute(
                    "select employee_id, result from step_results where workflow_step_id=?",
                    (first_step,),
                ).fetchone()
                connection.execute(
                    "insert into step_results "
                    "(step_result_id, tenant_id, workflow_step_id, employee_id, result, status) "
                    "values (?, 'tenant-r3', ?, ?, 'conflicting result', 'succeeded')",
                    (f"wfrs-{uuid.uuid4()}", first_step, existing[0]),
                )
                before = connection.execute(
                    "select step_result_id, result from step_results where workflow_step_id=? order by step_result_id",
                    (first_step,),
                ).fetchall()
                outbound_before = connection.execute(
                    "select count(*) from evolution_events where event_type='usage.model_call'"
                ).fetchone()[0]
            response = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )
            with sqlite3.connect(db_path) as connection:
                after = connection.execute(
                    "select step_result_id, result from step_results where workflow_step_id=? order by step_result_id",
                    (first_step,),
                ).fetchall()
                outbound_after = connection.execute(
                    "select count(*) from evolution_events where event_type='usage.model_call'"
                ).fetchone()[0]

        self.assertEqual(response.status_code, 422, response.text)
        self.assertIn("result history is invalid", response.text)
        self.assertEqual(calls.calls, [])
        self.assertEqual(before, after)
        self.assertEqual(outbound_before, outbound_after)

    def test_r4_projection_rejects_untrusted_cost_and_price_metadata(self):
        steps = [
            {
                "workflow_step_id": f"step-{order}",
                "step_order": order,
                "step_type": f"type-{order}",
                "status": "succeeded",
            }
            for order in range(1, 8)
        ]
        results = [
            {
                "workflow_step_id": f"step-{order}",
                "step_result_id": f"result-{order}",
                "result": f"output-{order}",
                "status": "succeeded",
            }
            for order in range(1, 8)
        ]
        executions = [
            {
                "execution_id": order,
                "tenant_id": "tenant-a",
                "task_id": "task-a",
                "output": f"output-{order}",
            }
            for order in range(1, 8)
        ]

        def usage_payloads():
            return [
                {
                    "usage_record_id": f"usage-{order}",
                    "tenant_id": "tenant-a",
                    "project_id": "project-a",
                    "workflow_run_id": "run-a",
                    "workflow_step_id": f"step-{order}",
                    "task_id": "task-a",
                    "execution_status": "success",
                    "model_gateway_id": "newapi",
                    "model_name": "approved-model",
                    "input_tokens": 6,
                    "output_tokens": 4,
                    "total_tokens": 10,
                    "cost_amount": 0.01,
                    "cost_source": "estimated",
                    "price_version": "2026-07-17",
                }
                for order in range(1, 8)
            ]

        def project(payloads):
            run = {
                "tenant_id": "tenant-a",
                "company_id": "company-a",
                "project_id": "project-a",
                "workflow_run_id": "run-a",
                "task_id": "task-a",
                "status": "succeeded",
                "final_report": "completed report",
                "steps": steps,
                "step_results": results,
            }
            usage_rows = payloads
            WorkflowRuntime._add_read_projection(
                run,
                executions,
                usage_rows,
                {
                    "tenant_id": "tenant-a",
                    "company_id": "company-a",
                    "status": "active",
                },
            )
            return run

        trusted = project(usage_payloads())
        self.assertEqual(trusted["project_status"]["execution_status"], "completed")
        self.assertAlmostEqual(trusted["artifact"]["estimated_cost"], 0.07)

        def zero_without_price(items):
            for item in items:
                item["cost_amount"] = 0
                item.pop("price_version")

        scenarios = {
            "zero_without_price": zero_without_price,
            "missing_cost": lambda items: items[0].update(cost_amount=None),
            "non_numeric_cost": lambda items: items[0].update(cost_amount="bad"),
            "negative_cost": lambda items: items[0].update(cost_amount=-0.01),
            "missing_price": lambda items: items[0].pop("price_version"),
            "non_string_price": lambda items: items[0].update(price_version={}),
            "mixed_price": lambda items: items[0].update(price_version="other"),
        }
        for name, mutate in scenarios.items():
            with self.subTest(name=name):
                payloads = usage_payloads()
                mutate(payloads)
                rejected = project(payloads)
                self.assertIsNone(rejected["artifact"])
                self.assertEqual(
                    rejected["project_status"]["execution_status"], "incomplete"
                )

    def test_r3_workflow_rejects_repeat_jump_and_unavailable_budget_before_network(self):
        scenarios = {
            "repeat": (422, "call limit"),
            "jump": (422, "non-succeeded prior step"),
            "budget": (422, "budget"),
            "missing_audit": (422, "budget"),
        }
        for scenario, (expected_status, expected_detail) in scenarios.items():
            with self.subTest(scenario=scenario):
                calls = RecordingHttpPost({})
                with patch.dict(
                    os.environ,
                    {
                        "CURIS_PRODUCT": "workspace",
                        "CURIS_ENV": "test",
                        "CURIS_IDENTITY_MODE": "test",
                        "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                        "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
                    },
                ):
                    client, headers, workflow, _, _, db_path = self._r3_workflow(calls)
                    with sqlite3.connect(db_path) as connection:
                        steps = connection.execute(
                            "select workflow_step_id from workflow_steps where workflow_run_id=? "
                            "order by step_order",
                            (workflow["workflow_run_id"],),
                        ).fetchall()
                        if scenario == "jump":
                            connection.execute(
                                "update workflow_steps set status='running' where workflow_step_id=?",
                                (steps[0][0],),
                            )
                        elif scenario in {"budget", "missing_audit"}:
                            connection.execute(
                                "update workflow_steps set status='succeeded' where workflow_step_id=?",
                                (steps[0][0],),
                            )
                    if scenario == "repeat":
                        self._record_r3_outbound(
                            db_path, workflow["workflow_run_id"], steps[0][0]
                        )
                    elif scenario == "budget":
                        self._record_r3_outbound(
                            db_path, workflow["workflow_run_id"], steps[0][0], estimated_cost=0.09
                        )
                    elif scenario == "missing_audit":
                        self._record_r3_outbound(
                            db_path, workflow["workflow_run_id"], steps[0][0], estimated_cost=None
                        )
                    response = client.post(
                        f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                        headers=headers,
                    )

                self.assertEqual(response.status_code, expected_status, response.text)
                self.assertIn(expected_detail, response.text)
                self.assertEqual(calls.calls, [])

    def test_r3_binding_set_rejects_invalid_config_without_single_value_fallback(self):
        for scenario in (
            "missing",
            "empty",
            "missing_role",
            "unknown_role",
            "duplicate_role",
            "duplicate_binding",
            "invalid_binding",
        ):
            with self.subTest(scenario=scenario):
                calls = RecordingHttpPost({})
                with patch.dict(
                    os.environ,
                    {
                        "CURIS_PRODUCT": "workspace",
                        "CURIS_ENV": "test",
                        "CURIS_IDENTITY_MODE": "test",
                        "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                        "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
                    },
                ):
                    client, headers, workflow, _, binding, _ = self._r3_workflow(calls)
                    approved = json.loads(os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"])
                    os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDING_ID"] = binding["id"]
                    if scenario == "missing":
                        os.environ.pop("CURIS_R3_APPROVED_CAPABILITY_BINDINGS")
                    elif scenario == "empty":
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = "{}"
                    elif scenario == "missing_role":
                        approved.pop("qa_engineer")
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = json.dumps(approved)
                    elif scenario == "unknown_role":
                        approved["unknown"] = approved.pop("qa_engineer")
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = json.dumps(approved)
                    elif scenario == "duplicate_role":
                        pairs = [*approved.items(), ("tech_lead", approved["product_manager"])]
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = "{" + ",".join(
                            f"{json.dumps(role)}:{json.dumps(binding_id)}"
                            for role, binding_id in pairs
                        ) + "}"
                    elif scenario == "duplicate_binding":
                        approved["qa_engineer"] = approved["product_manager"]
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = json.dumps(approved)
                    else:
                        approved["qa_engineer"] = "not-a-binding"
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = json.dumps(approved)
                    response = client.post(
                        f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                        headers=headers,
                    )

                self.assertEqual(response.status_code, 403, response.text)
                self.assertEqual(calls.calls, [])

    def test_r3_binding_set_rejects_role_ambiguity_and_cross_scope_before_network(self):
        for scenario in ("role_mismatch", "duplicate_employee", "duplicate_binding", "cross_project"):
            with self.subTest(scenario=scenario):
                calls = RecordingHttpPost({})
                with patch.dict(
                    os.environ,
                    {
                        "CURIS_PRODUCT": "workspace",
                        "CURIS_ENV": "test",
                        "CURIS_IDENTITY_MODE": "test",
                        "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                        "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
                    },
                ):
                    client, headers, workflow, _, _, db_path = self._r3_workflow(calls)
                    with Database(db_path).connect() as connection:
                        steps = connection.execute(
                            "select workflow_step_id from workflow_steps where workflow_run_id=? "
                            "order by step_order",
                            (workflow["workflow_run_id"],),
                        ).fetchall()
                        connection.execute(
                            "update workflow_steps set status='succeeded' where workflow_step_id=?",
                            (steps[0][0],),
                        )
                        if scenario == "duplicate_binding":
                            employee_id = connection.execute(
                                "select id from employee_instances where role='product_manager'"
                            ).fetchone()[0]
                            connection.execute(
                                "insert into employee_capability_bindings "
                                "(id, tenant_id, employee_id, employee_template_id, capability_source, "
                                "capability_type, capability_id, priority, enabled) "
                                "select 'bind-00000000-0000-0000-0000-000000000001', tenant_id, "
                                "employee_id, employee_template_id, capability_source, 'tool', "
                                "'model_gateway_tool', priority, enabled from employee_capability_bindings "
                                "where employee_id=?",
                                (employee_id,),
                            )
                        elif scenario == "cross_project":
                            connection.execute(
                                "update projects set department_id='other-department'"
                            )
                    self._record_r3_outbound(db_path, workflow["workflow_run_id"], steps[0][0])
                    if scenario == "role_mismatch":
                        approved = json.loads(os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"])
                        approved["product_manager"], approved["architect"] = (
                            approved["architect"],
                            approved["product_manager"],
                        )
                        os.environ["CURIS_R3_APPROVED_CAPABILITY_BINDINGS"] = json.dumps(approved)
                    elif scenario == "duplicate_employee":
                        templates = client.get(
                            "/api/workspace/employee-templates", headers=headers
                        ).json()["employee_templates"]
                        template = next(item for item in templates if item["role"] == "product_manager")
                        duplicate = client.post(
                            "/api/workspace/employees",
                            headers=headers,
                            json={
                                "department_id": workflow["department_id"],
                                "template_id": template["id"],
                                "name": "Duplicate Product Manager",
                                "enabled": True,
                            },
                        ).json()
                        client.put(
                            f"/api/workspace/employees/{duplicate['id']}/capabilities",
                            headers=headers,
                            json={
                                "bindings": [{
                                    "capability_source": "official",
                                    "capability_type": "model",
                                    "capability_id": R3_CAPABILITY_ID,
                                    "priority": 1,
                                    "enabled": True,
                                }]
                            },
                        )
                    response = client.post(
                        f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                        headers=headers,
                    )

                self.assertEqual(response.status_code, 403, response.text)
                self.assertEqual(calls.calls, [])

    def test_r3_workflow_failure_stops_without_retry(self):
        attempts = []

        def rate_limited(url, payload, headers, timeout):
            attempts.append(url)
            raise urllib.error.HTTPError(url, 429, "rate limited", {}, None)

        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, _, _, _ = self._r3_workflow(rate_limited)
            first = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )
            second = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )

        self.assertEqual(first.status_code, 429, first.text)
        self.assertEqual(second.status_code, 200, second.text)
        self.assertEqual(second.json()["status"], "failed")
        self.assertEqual(len(attempts), 1)

    def test_r3_workflow_rejects_unapproved_project_before_network(self):
        calls = RecordingHttpPost({})
        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, _, _, _ = self._r3_workflow(calls)
            os.environ["CURIS_R3_APPROVED_PROJECT_ID"] = "project-not-approved"
            response = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )

        self.assertEqual(response.status_code, 403, response.text)
        self.assertEqual(calls.calls, [])

    def test_r3_workflow_rejects_unapproved_run_before_network(self):
        calls = RecordingHttpPost({})
        with patch.dict(
            os.environ,
            {
                "CURIS_PRODUCT": "workspace",
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
            },
        ):
            client, headers, workflow, _, _, _ = self._r3_workflow(calls)
            os.environ["CURIS_R3_APPROVED_WORKFLOW_RUN_ID"] = "run-not-approved"
            response = client.post(
                f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                headers=headers,
            )

        self.assertEqual(response.status_code, 403, response.text)
        self.assertEqual(calls.calls, [])

    def test_r3_trusted_ceo_scope_failures_are_rejected_before_network(self):
        mutations = {
            "missing membership CEO": "update tenant_memberships set ceo_id=null",
            "disallowed membership role": "update tenant_memberships set role='viewer'",
            "company CEO mismatch": "update companies set ceo_id='other-ceo' where company_id='company-r3'",
            "inactive department": "update department_instances set status='disabled'",
            "archived project": "update projects set status='archived'",
            "cross-company project": "update projects set company_id='other-company'",
            "disabled employee": "update employee_instances set status='disabled'",
        }
        for label, statement in mutations.items():
            with self.subTest(label=label):
                calls = RecordingHttpPost({})
                with patch.dict(
                    os.environ,
                    {
                        "CURIS_PRODUCT": "workspace",
                        "CURIS_ENV": "production",
                        "CURIS_IDENTITY_MODE": "gateway",
                        "CURIS_TRUSTED_GATEWAY_ISSUER": "https://issuer.example",
                        "CURIS_TRUSTED_GATEWAY_CIDRS": "10.0.0.2/32",
                        "CURIS_IDENTITY_AUDIT_KEY": "r3-audit-test-key",
                        "CURIS_MODEL_GATEWAY_PROFILE": R3_PROFILE,
                    },
                ):
                    client, headers, workflow, _, _, db_path = self._r3_workflow(calls)
                    with sqlite3.connect(db_path) as connection:
                        connection.execute(statement)
                    response = client.post(
                        f"/api/workspace/workflows/{workflow['workflow_run_id']}/run-next-step",
                        headers={**headers, "X-Ceo-Id": "forged-ceo"},
                    )

                self.assertEqual(response.status_code, 403, response.text)
                self.assertEqual(calls.calls, [])

    def test_partial_startup_env_config_fails_closed_without_secret_values(self):
        original_values = {
            key: os.environ.get(key)
            for key in (
                "CURIS_MODEL_GATEWAY_BASE_URL",
                "CURIS_MODEL_GATEWAY_API_KEY",
                "CURIS_MODEL_GATEWAY_MODEL",
            )
        }
        os.environ["CURIS_MODEL_GATEWAY_BASE_URL"] = "https://newapi.example.com"
        os.environ["CURIS_MODEL_GATEWAY_API_KEY"] = "sk-or-v1-secret-value-1234567890"
        os.environ.pop("CURIS_MODEL_GATEWAY_MODEL", None)

        try:
            with self.assertRaises(RuntimeError) as context:
                create_app(str(Path(self.tmp.name) / "startup.sqlite"))
        finally:
            for key, value in original_values.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

        message = str(context.exception)
        self.assertIn("Model Gateway Adapter requires", message)
        self.assertNotIn("sk-or-v1-secret-value-1234567890", message)
        self.assertNotIn("https://newapi.example.com", message)

    def test_adapter_redacts_secret_prompt_and_raw_response_from_errors(self):
        prompt = "Prompt text with user input that must not leak"
        secret = "sk-or-v1-secret-value-1234567890"

        def leaking_http_post(url: str, payload: dict, headers: dict, timeout: int) -> dict:
            raise RuntimeError(
                "Authorization: Bearer sk-or-v1-secret-value-1234567890; "
                "prompt=Prompt text with user input that must not leak; "
                "response={'output':'raw model output should not leak'}"
            )

        adapter = ModelGatewayAdapter(
            base_url="https://newapi.example.com",
            api_key=secret,
            gateway_id="newapi-main",
            model_name="newapi-model-a",
            http_post=leaking_http_post,
        )

        with self.assertRaises(RuntimeError) as context:
            adapter.execute(prompt)

        message = str(context.exception)
        self.assertIn("[REDACTED]", message)
        self.assertNotIn(secret, message)
        self.assertNotIn(prompt, message)
        self.assertNotIn("raw model output should not leak", message)
        self.assertNotIn("Authorization", message)

    def test_unattributed_task_is_rejected_before_model_gateway(self):
        gateway = RecordingGateway()
        app = create_app(
            str(Path(self.tmp.name) / "api.sqlite"),
            model_gateway_adapter=gateway,
        )
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-acme", "X-Ceo-Id": "ceo-001"}
        task_id = client.post(
            "/api/task",
            json={"content": "Plain model task"},
            headers=headers,
        ).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        usage_response = client.get(
            "/api/platform/usage",
            params={"tenant_id": "tenant-acme"},
            headers={"X-Platform-Admin-Token": "platform-admin-dev"},
        )

        self.assertEqual(run_response.status_code, 400)
        self.assertIn("attribution is incomplete", run_response.text)
        self.assertEqual(gateway.prompts, [])
        self.assertEqual(usage_response.json()["usage_events"], [])

    def test_usage_event_payload_is_allowlisted_and_redacts_secret_like_values(self):
        gateway = SecretLeakingGateway()
        app = create_app(
            str(Path(self.tmp.name) / "usage-redaction.sqlite"),
            model_gateway_adapter=gateway,
        )
        client = TestClient(app)
        headers = {"X-Tenant-Id": "tenant-acme", "X-Ceo-Id": "ceo-001"}
        task_id = client.post(
            "/api/task",
            json={"content": "Secret-bearing model task"},
            headers=headers,
        ).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        usage_response = client.get(
            "/api/platform/usage",
            params={"tenant_id": "tenant-acme"},
            headers={"X-Platform-Admin-Token": "platform-admin-dev"},
        )

        self.assertEqual(run_response.status_code, 400)
        self.assertEqual(usage_response.json()["usage_events"], [])
        payload_text = usage_response.text
        self.assertNotIn("sk-or-v1-secret-value-1234567890", payload_text)
        self.assertNotIn("Authorization", payload_text)
        self.assertNotIn("Secret-bearing model task", payload_text)
        self.assertNotIn("raw model output should not persist", payload_text)

    def test_workspace_reads_official_model_catalog_without_credentials(self):
        app = create_app(str(Path(self.tmp.name) / "catalog.sqlite"))
        client = TestClient(app)

        response = client.get(
            "/api/catalog/models",
            headers={"X-Tenant-Id": "tenant-acme"},
        )

        self.assertEqual(response.status_code, 200)
        models = response.json()["models"]
        self.assertTrue(models)
        self.assertTrue(all(item["source"] == "official" for item in models))
        self.assertTrue(all(item["status"] == "active" for item in models))
        self.assertTrue(all("gateway_ref" in item for item in models))
        self.assertTrue(all("supported_models" in item for item in models))
        self.assertFalse(any("api_key" in item or "secret" in item or "password" in item for item in models))


if __name__ == "__main__":
    unittest.main()
