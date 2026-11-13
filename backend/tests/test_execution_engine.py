import os
import asyncio
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.codex_executor import CodexExecutor
from app.database import Database
from app.employee import AIEmployee
from app.main import create_app
from app.orchestrator import Orchestrator
from app.prompt_builder import PromptBuilder
from app.result_store import ResultStore
from app.tool_executor import ToolExecutor
from app.tool_registry import ToolRegistry
from app.tool_router import ToolRouter


class RecordingExecutor:
    def __init__(self):
        self.prompts = []

    def execute(self, prompt: str) -> dict:
        self.prompts.append(prompt)
        return {"output": "Execution result", "cost": 0.0123}


class FailingExecutor:
    def execute(self, prompt: str) -> dict:
        raise RuntimeError("executor failed")


class AsyncRecordingExecutor:
    def __init__(self, label: str):
        self.label = label
        self.inputs = []

    async def execute(self, prompt: str) -> dict:
        self.inputs.append(prompt)
        await asyncio.sleep(0)
        return {"output": f"{self.label}: {prompt}", "cost": 0.01}


class FailOnceExecutor:
    def execute(self, prompt: str) -> dict:
        raise RuntimeError("primary failed")


class EmptyExecutor:
    def execute(self, prompt: str) -> dict:
        return {"output": "", "cost": 0.01}


class ExecutionEngineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.database = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.database.initialize()
        self.store = ResultStore(self.database)
        self.registry = ToolRegistry(self.database)

    def tearDown(self):
        self.tmp.cleanup()

    def test_task_api_creates_init_task(self):
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"default_tool": RecordingExecutor().execute})
        client = TestClient(app)

        response = client.post("/api/task", json={"content": "Write a short plan"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "created")
        self.assertTrue(payload["task_id"])
        task = client.get(f"/api/task/{payload['task_id']}").json()
        self.assertEqual(task["status"], "INIT")
        self.assertEqual(task["state_flow"], ["INIT"])

    def test_run_task_executes_codex_and_persists_result(self):
        executor = RecordingExecutor()
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"codex_tool": executor.execute})
        client = TestClient(app)
        headers = {"X-Ceo-Id": "ceo-test"}
        task_id = client.post("/api/task", json={"content": "Create code release notes"}, headers=headers).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        status_response = client.get(f"/api/task/{task_id}")
        list_response = client.get("/api/tasks")

        self.assertEqual(run_response.status_code, 200)
        task = status_response.json()
        self.assertEqual(task["status"], "COMPLETED")
        self.assertEqual(task["output"], "Execution result")
        self.assertEqual(task["cost"], 0.0123)
        self.assertEqual(task["selected_tool"], "codex_tool")
        self.assertEqual(task["state_flow"], ["INIT", "PARSED", "RUNNING", "COMPLETED"])
        self.assertIn("Create code release notes", task["prompt"])
        self.assertEqual(executor.prompts, [task["prompt"]])
        self.assertEqual(list_response.json()[0]["task_id"], task_id)

    def test_successful_run_exposes_complete_existing_evidence_chain(self):
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"codex_tool": RecordingExecutor().execute})
        client = TestClient(app)
        headers = {"X-Ceo-Id": "ceo-test"}
        task_id = client.post("/api/task", json={"content": "implement code parser"}, headers=headers).json()["task_id"]

        run_response = client.post(f"/api/task/{task_id}/run", headers=headers)
        task = client.get(f"/api/task/{task_id}").json()
        trace = client.get(f"/api/task/{task_id}/trace").json()
        workflow = client.get(f"/api/task/{task_id}/workflow").json()
        meta_development = client.get(f"/api/task/{task_id}/meta-development").json()
        evolution = client.get(f"/api/task/{task_id}/evolution-decisions").json()

        self.assertEqual(run_response.status_code, 200)
        self.assertEqual(task["status"], "COMPLETED")
        self.assertEqual(task["selected_tool"], "codex_tool")
        self.assertEqual(task["executions"][0]["tool_name"], "codex_tool")
        self.assertEqual(task["executions"][0]["output"], task["output"])
        self.assertEqual([step["tool_name"] for step in trace], ["codex_tool"])
        self.assertEqual(workflow["status"], "COMPLETED")
        self.assertEqual(workflow["completed_steps"], [1])
        self.assertEqual(workflow["trace"][0]["tool_used"], "codex_tool")
        self.assertEqual(meta_development["task_id"], task_id)
        self.assertEqual(meta_development["gap_analysis"]["status"], "ready_for_review")
        self.assertEqual(evolution["task_id"], task_id)
        self.assertEqual(evolution["decision"], "do_not_evolve")
        self.assertFalse(evolution["automatic_code_modification_allowed"])

    def test_failed_execution_updates_task_status(self):
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"codex_tool": FailingExecutor().execute})
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "Run code failure"}).json()["task_id"]

        response = client.post(f"/api/task/{task_id}/run")
        task = client.get(f"/api/task/{task_id}").json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(task["status"], "FAILED")
        self.assertEqual(task["state_flow"], ["INIT", "PARSED", "RUNNING", "FAILED"])

    def test_failed_run_records_single_error_trace_and_workflow_evidence(self):
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"codex_tool": FailingExecutor().execute})
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "Run code failure"}).json()["task_id"]

        response = client.post(f"/api/task/{task_id}/run")
        trace_response = client.get(f"/api/task/{task_id}/trace")
        workflow_response = client.get(f"/api/task/{task_id}/workflow")
        task = client.get(f"/api/task/{task_id}").json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(task["status"], "FAILED")
        self.assertEqual(task["error"], "tool executor is not configured: default_tool")
        self.assertEqual([step["tool_name"] for step in trace_response.json()], ["codex_tool", "gpt_tool", "default_tool"])
        self.assertEqual([step["step_index"] for step in trace_response.json()], [1, 2, 3])
        self.assertTrue(all(step["error"] for step in trace_response.json()))
        workflow = workflow_response.json()
        self.assertEqual(workflow["status"], "FAILED")
        self.assertEqual(workflow["failed_steps"], [1])
        self.assertTrue(any(item["event"] == "step_failed" for item in workflow["adaptation_log"]))
        self.assertTrue(any(item["event"] == "workflow_failed" for item in workflow["adaptation_log"]))

    def test_orchestrator_state_machine_stores_execution_row(self):
        executor = RecordingExecutor()
        self.registry.register(
            {
                "name": "codex_tool",
                "type": "llm",
                "description": "Code generation",
                "entry": "codex",
            }
        )
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"codex_tool": executor.execute}))
        task = self.store.create_task("Summarize code state machine")

        result = asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["selected_tool"], "codex_tool")
        self.assertEqual(result["state_flow"], ["INIT", "PARSED", "RUNNING", "COMPLETED"])
        execution = self.store.list_executions(task["task_id"])[0]
        self.assertEqual(execution["tool_name"], "codex_tool")
        self.assertEqual(execution["output"], "Execution result")

    def test_tool_registry_registers_gets_and_lists_tools(self):
        tool = self.registry.register(
            {
                "name": "gpt_tool",
                "type": "llm",
                "description": "Reasoning",
                "entry": "gpt",
            }
        )

        self.assertEqual(tool["name"], "gpt_tool")
        self.assertEqual(self.registry.get("gpt_tool")["entry"], "gpt")
        self.assertEqual([item["name"] for item in self.registry.list()], ["gpt_tool"])

    def test_tool_router_selects_replaceable_tool_without_employee_logic(self):
        router = ToolRouter()

        self.assertEqual(router.plan("write code for a parser"), ["codex_tool"])
        self.assertEqual(router.plan("reason about this issue"), ["gpt_tool"])
        self.assertEqual(router.plan("architecture for backend"), ["claude_tool"])
        self.assertEqual(router.plan("architecture then code for backend"), ["claude_tool", "codex_tool"])
        self.assertEqual(router.plan("plain task"), ["default_tool"])

    def test_employee_coordinates_tool_router_and_executor(self):
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        executor = RecordingExecutor()
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"claude_tool": executor.execute}))

        result = asyncio.run(employee.execute("architecture review", "Prompt"))

        self.assertEqual(result["tool_name"], "claude_tool")
        self.assertEqual(result["output"], "Execution result")

    def test_tool_executor_runs_chain_and_records_intermediate_trace(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        gpt = AsyncRecordingExecutor("gpt")
        codex = AsyncRecordingExecutor("codex")
        executor = ToolExecutor(self.registry, {"gpt_tool": gpt.execute, "codex_tool": codex.execute})

        result = asyncio.run(executor.execute_chain(["gpt_tool", "codex_tool"], "Initial input"))

        self.assertEqual(result["tool_name"], "codex_tool")
        self.assertEqual(result["output"], "codex: gpt: Initial input")
        self.assertEqual([step["step"] for step in result["trace"]], [1, 2])
        self.assertEqual([step["tool"] for step in result["trace"]], ["gpt_tool", "codex_tool"])
        self.assertEqual(result["trace"][1]["input"], "gpt: Initial input")

    def test_tool_executor_falls_back_when_primary_tool_fails(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"})
        fallback = RecordingExecutor()
        executor = ToolExecutor(
            self.registry,
            {
                "codex_tool": FailOnceExecutor().execute,
                "gpt_tool": fallback.execute,
                "default_tool": RecordingExecutor().execute,
            },
        )

        result = asyncio.run(executor.execute_chain(["codex_tool"], "Prompt"))

        self.assertEqual(result["tool_name"], "gpt_tool")
        self.assertEqual(result["output"], "Execution result")
        self.assertEqual(result["trace"][0]["tool"], "codex_tool")
        self.assertIn("primary failed", result["trace"][0]["error"])
        self.assertEqual(result["trace"][1]["tool"], "gpt_tool")

    def test_orchestrator_stores_full_tool_trace(self):
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        claude = AsyncRecordingExecutor("claude")
        codex = AsyncRecordingExecutor("codex")
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(self.registry, {"claude_tool": claude.execute, "codex_tool": codex.execute}),
        )
        task = self.store.create_task("architecture then code module")

        result = asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        trace = self.store.list_trace(task["task_id"])

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["selected_tool"], "codex_tool")
        self.assertEqual([step["tool_name"] for step in trace], ["claude_tool", "codex_tool"])
        self.assertEqual(trace[1]["input"], trace[0]["output"])

    def test_trace_api_returns_full_execution_chain(self):
        app = create_app(
            str(Path(self.tmp.name) / "api.sqlite"),
            tool_functions={
                "claude_tool": AsyncRecordingExecutor("claude").execute,
                "codex_tool": AsyncRecordingExecutor("codex").execute,
            },
        )
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "architecture then code flow"}).json()["task_id"]

        client.post(f"/api/task/{task_id}/run")
        trace_response = client.get(f"/api/task/{task_id}/trace")

        self.assertEqual(trace_response.status_code, 200)
        self.assertEqual([step["tool_name"] for step in trace_response.json()], ["claude_tool", "codex_tool"])

    def test_workflow_planner_converts_task_into_ordered_steps(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"gpt_tool": RecordingExecutor().execute}))
        orchestrator = Orchestrator(self.store, PromptBuilder(), employee)

        plan = orchestrator.plan_workflow("创建一个登录页面并写API")

        self.assertEqual([step["action"] for step in plan], ["analyze", "design_ui", "generate_frontend", "generate_backend", "validate"])
        self.assertEqual([step["step_name"] for step in plan], ["需求分析", "UI设计", "前端实现", "后端API实现", "联调测试"])
        for step in plan:
            self.assertTrue(step["purpose"])
            self.assertTrue(step["tool_required"])
            self.assertTrue(step["expected_output"])
        self.assertEqual(ToolRouter().tools_for_step(plan[0]), ["gpt_tool"])
        self.assertEqual(ToolRouter().tools_for_step(plan[2]), ["codex_tool"])
        self.assertEqual(ToolRouter().tools_for_step(plan[3]), ["codex_tool"])
        self.assertEqual(ToolRouter().tools_for_step(plan[4]), ["gpt_tool"])

    def test_tool_router_auto_assigns_generated_steps_with_cost_aware_defaults(self):
        router = ToolRouter()

        self.assertEqual(router.tool_for_generated_step({"step_name": "前端实现", "purpose": "coding"}), "codex_tool")
        self.assertEqual(router.tool_for_generated_step({"step_name": "需求分析", "purpose": "reasoning"}), "gpt_tool")
        self.assertEqual(router.tool_for_generated_step({"step_name": "架构设计", "purpose": "architecture"}), "claude_tool")
        self.assertEqual(router.tool_for_generated_step({"step_name": "未知步骤", "purpose": "general work"}), "gpt_tool")

    def test_workflow_execution_persists_state_trace_and_context(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        gpt = AsyncRecordingExecutor("gpt")
        claude = AsyncRecordingExecutor("claude")
        codex = AsyncRecordingExecutor("codex")
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": gpt.execute,
                    "claude_tool": claude.execute,
                    "codex_tool": codex.execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        result = asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        workflow = self.store.get_workflow(task["task_id"])
        auto_workflow = self.store.get_auto_workflow(task["task_id"])
        trace = self.store.list_workflow_trace(task["task_id"])

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(workflow["status"], "COMPLETED")
        self.assertEqual(auto_workflow["status"], "COMPLETED")
        self.assertEqual(len(auto_workflow["generated_steps"]), 5)
        self.assertEqual(auto_workflow["adaptation_log"][-1]["event"], "workflow_completed")
        self.assertEqual(workflow["current_step"], 5)
        self.assertEqual(workflow["completed_steps"], [1, 2, 3, 4, 5])
        self.assertEqual([step["action"] for step in workflow["workflow_plan"]], ["analyze", "design_ui", "generate_frontend", "generate_backend", "validate"])
        self.assertEqual([step["tool_used"] for step in trace], ["gpt_tool", "claude_tool", "codex_tool", "codex_tool", "gpt_tool"])
        self.assertIn(trace[0]["output"], trace[1]["input"])
        self.assertIn(trace[1]["output"], trace[2]["input"])

    def test_auto_workflow_records_adaptation_when_primary_tool_falls_back(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "codex_tool": FailOnceExecutor().execute,
                    "gpt_tool": RecordingExecutor().execute,
                    "default_tool": RecordingExecutor().execute,
                },
            ),
        )
        task = self.store.create_task("implement code parser")

        orchestrator = Orchestrator(self.store, PromptBuilder(), employee)
        asyncio.run(orchestrator.run(task["task_id"]))
        auto_workflow = self.store.get_auto_workflow(task["task_id"])
        trace = self.store.list_trace(task["task_id"])
        future_plan = orchestrator.generate_auto_workflow("implement another parser")

        self.assertEqual(auto_workflow["status"], "COMPLETED")
        self.assertTrue(any(item["event"] == "tool_fallback" for item in auto_workflow["adaptation_log"]))
        self.assertEqual([step["tool_name"] for step in trace], ["codex_tool", "gpt_tool"])
        self.assertIn("primary failed", trace[0]["error"])
        self.assertEqual(future_plan[0]["tool_required"], "gpt_tool")

    def test_successful_fallback_exposes_existing_evidence_map(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "codex_tool": FailOnceExecutor().execute,
                    "gpt_tool": RecordingExecutor().execute,
                    "default_tool": RecordingExecutor().execute,
                },
            ),
        )
        task = self.store.create_task("implement code parser")

        result = asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        trace = self.store.list_trace(task["task_id"])
        workflow = self.store.get_workflow(task["task_id"])
        auto_workflow = self.store.get_auto_workflow(task["task_id"])
        workflow_trace = self.store.list_workflow_trace(task["task_id"])
        failures = self.store.list_failure_logs()
        performance = self.store.list_tool_performance()

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(workflow["status"], "COMPLETED")
        self.assertEqual(workflow["completed_steps"], [1])
        self.assertEqual([step["tool_name"] for step in trace], ["codex_tool", "gpt_tool"])
        self.assertTrue(trace[0]["error"])
        self.assertEqual(trace[1]["error"], None)
        self.assertEqual(workflow_trace[0]["tool_used"], "gpt_tool")
        self.assertTrue(any(item["event"] == "tool_fallback" and item["from"] == "codex_tool" and item["to"] == "gpt_tool" for item in auto_workflow["adaptation_log"]))
        self.assertEqual(failures[0]["step_index"], 1)
        self.assertEqual(failures[0]["tool_name"], "codex_tool")
        self.assertEqual(performance["codex_tool"]["failure_count"], 1)
        self.assertEqual(performance["gpt_tool"]["success_count"], 1)

    def test_full_fallback_failure_maps_failure_logs_to_workflow_step(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "codex_tool": FailingExecutor().execute,
                    "gpt_tool": FailingExecutor().execute,
                    "default_tool": FailingExecutor().execute,
                },
            ),
        )
        task = self.store.create_task("implement code parser")

        with self.assertRaises(RuntimeError):
            asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        trace = self.store.list_trace(task["task_id"])
        workflow = self.store.get_workflow(task["task_id"])
        auto_workflow = self.store.get_auto_workflow(task["task_id"])
        failures = self.store.list_failure_logs()
        performance = self.store.list_tool_performance()

        self.assertEqual(workflow["status"], "FAILED")
        self.assertEqual(workflow["failed_steps"], [1])
        self.assertEqual([step["tool_name"] for step in trace], ["codex_tool", "gpt_tool", "default_tool"])
        self.assertTrue(all(step["error"] for step in trace))
        self.assertTrue(any(item["event"] == "step_failed" and item["step"] == 1 for item in auto_workflow["adaptation_log"]))
        self.assertTrue(any(item["event"] == "workflow_failed" for item in auto_workflow["adaptation_log"]))
        self.assertEqual([failure["step_index"] for failure in failures], [1, 1, 1])
        self.assertEqual([failure["tool_name"] for failure in failures], ["codex_tool", "gpt_tool", "default_tool"])
        self.assertEqual(performance["codex_tool"]["failure_count"], 1)
        self.assertEqual(performance["gpt_tool"]["failure_count"], 1)
        self.assertEqual(performance["default_tool"]["failure_count"], 1)

    def test_workflow_api_returns_plan_status_and_trace(self):
        app = create_app(
            str(Path(self.tmp.name) / "workflow-api.sqlite"),
            tool_functions={
                "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                "claude_tool": AsyncRecordingExecutor("claude").execute,
                "codex_tool": AsyncRecordingExecutor("codex").execute,
            },
        )
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "创建一个登录页面并写API"}).json()["task_id"]

        client.post(f"/api/task/{task_id}/run")
        response = client.get(f"/api/task/{task_id}/workflow")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "COMPLETED")
        self.assertEqual(len(payload["workflow_plan"]), 5)
        self.assertEqual(len(payload["generated_steps"]), 5)
        self.assertEqual(payload["generated_steps"][0]["step_name"], "需求分析")
        self.assertEqual(payload["adaptation_log"][-1]["event"], "workflow_completed")
        self.assertEqual(len(payload["trace"]), 5)

    def test_learning_loop_stores_execution_patterns_metrics_and_tool_performance(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        patterns = self.store.list_execution_patterns()
        metrics = self.store.list_workflow_metrics()
        performance = self.store.list_tool_performance()
        memory = self.store.get_execution_summary_memory()

        self.assertEqual(patterns[0]["pattern_type"], "successful_workflow")
        self.assertEqual(patterns[0]["step_sequence"], ["analyze", "design_ui", "generate_frontend", "generate_backend", "validate"])
        self.assertEqual(metrics[0]["status"], "success")
        self.assertEqual(metrics[0]["step_count"], 5)
        self.assertGreaterEqual(performance["gpt_tool"]["success_count"], 1)
        self.assertGreaterEqual(performance["codex_tool"]["success_count"], 2)
        self.assertIn("successful_patterns", memory)
        self.assertIn("optimal_tool_chains", memory)

    def test_failure_analysis_logs_root_cause_and_penalizes_failed_tool(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "default_tool", "type": "llm", "description": "Default", "entry": "default"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "codex_tool": FailOnceExecutor().execute,
                    "gpt_tool": RecordingExecutor().execute,
                    "default_tool": RecordingExecutor().execute,
                },
            ),
        )
        task = self.store.create_task("implement code parser")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        failures = self.store.list_failure_logs()
        performance = self.store.list_tool_performance()

        self.assertEqual(failures[0]["failure_type"], "tool_failure")
        self.assertIn("primary failed", failures[0]["root_cause"])
        self.assertTrue(failures[0]["correction_strategy"])
        self.assertEqual(performance["codex_tool"]["failure_count"], 1)
        self.assertEqual(performance["gpt_tool"]["success_count"], 1)

    def test_tool_selection_uses_historical_performance_weights(self):
        self.store.record_tool_performance("codex_tool", success=False, latency_ms=4000, cost=0.03)
        self.store.record_tool_performance("gpt_tool", success=True, latency_ms=200, cost=0.01)
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"codex_tool": RecordingExecutor().execute}))
        orchestrator = Orchestrator(self.store, PromptBuilder(), employee)

        plan = orchestrator.generate_auto_workflow("implement parser")

        self.assertEqual(plan[0]["tool_required"], "gpt_tool")
        self.assertIn("learned", plan[0]["purpose"].lower())

    def test_successful_patterns_are_reused_to_reduce_future_workflow_size(self):
        self.store.save_execution_pattern(
            task_signature="ui_api",
            pattern_type="successful_workflow",
            step_sequence=["analyze", "generate_frontend", "generate_backend", "validate"],
            tool_chain=["gpt_tool", "codex_tool", "codex_tool", "gpt_tool"],
            success_rate=1.0,
            avg_step_count=4,
        )
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"gpt_tool": RecordingExecutor().execute}))
        orchestrator = Orchestrator(self.store, PromptBuilder(), employee)

        plan = orchestrator.generate_auto_workflow("创建一个登录页面并写API")

        self.assertEqual([step["action"] for step in plan], ["analyze", "generate_frontend", "generate_backend", "validate"])
        self.assertEqual(len(plan), 4)

    def test_autonomous_development_loop_scores_strategy_and_evolution_log(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        scores = self.store.list_execution_scores()
        strategies = self.store.list_development_strategies()
        evolution_log = self.store.list_system_evolution_log()

        self.assertGreaterEqual(scores[0]["speed_score"], 0)
        self.assertGreaterEqual(scores[0]["correctness_score"], 0)
        self.assertGreaterEqual(scores[0]["efficiency_score"], 0)
        self.assertGreaterEqual(scores[0]["tool_usage_score"], 0)
        self.assertTrue(strategies[0]["development_strategy"])
        self.assertEqual(evolution_log[0]["target_module"], "workflow_generator")
        self.assertTrue(evolution_log[0]["optimization_decision"])

    def test_self_refinement_reduces_redundant_steps_after_execution(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")
        orchestrator = Orchestrator(self.store, PromptBuilder(), employee)

        asyncio.run(orchestrator.run(task["task_id"]))
        future_plan = orchestrator.generate_auto_workflow("创建一个登录页面并写API")

        self.assertEqual([step["action"] for step in future_plan], ["analyze", "generate_frontend", "generate_backend", "validate"])
        self.assertEqual(len(future_plan), 4)

    def test_self_debugging_logs_inconsistent_output_and_strategy(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"gpt_tool": EmptyExecutor().execute}))
        task = self.store.create_task("reason about empty response")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        failures = self.store.list_failure_logs()
        strategies = self.store.list_development_strategies()

        self.assertEqual(failures[0]["failure_type"], "inconsistent_output")
        self.assertIn("empty", failures[0]["root_cause"])
        self.assertIn("self-debug", strategies[0]["development_strategy"].lower())

    def test_meta_development_report_persists_gap_issue_verification_and_source_of_truth_plan(self):
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"codex_tool": RecordingExecutor().execute}))
        task = self.store.create_task("implement code parser")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        report = self.store.get_meta_development_report(task["task_id"])

        self.assertEqual(report["task_id"], task["task_id"])
        self.assertIn("gap_analysis", report)
        self.assertIn("planned_issues", report)
        self.assertIn("verification_plan", report)
        self.assertIn("source_of_truth_suggestions", report)
        self.assertGreaterEqual(len(report["planned_issues"]), 1)
        self.assertIn("backend tests", " ".join(report["verification_plan"]).lower())
        self.assertIn("knowledge/CURRENT_CONTEXT.md", report["source_of_truth_suggestions"])

    def test_meta_development_api_returns_report_for_completed_task(self):
        executor = RecordingExecutor()
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"codex_tool": executor.execute})
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "implement code parser"}).json()["task_id"]

        client.post(f"/api/task/{task_id}/run")
        response = client.get(f"/api/task/{task_id}/meta-development")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["task_id"], task_id)
        self.assertGreaterEqual(len(payload["planned_issues"]), 1)
        self.assertIn("scope drift", " ".join(payload["verification_plan"]).lower())

    def test_evolution_governor_safely_rejects_when_thresholds_are_not_met(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"gpt_tool": RecordingExecutor().execute}))
        task = self.store.create_task("reason about current status")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])

        self.assertEqual(decision["decision"], "do_not_evolve")
        self.assertEqual(decision["policy"], ["STABILITY", "OPTIMIZATION", "EVOLUTION"])
        self.assertIsNone(decision["proposal"])
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertEqual(decision["threshold_evaluation"]["thresholds_met"], [])

    def test_stable_execution_exposes_do_not_evolve_evidence_map(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        employee = AIEmployee(ToolRouter(), ToolExecutor(self.registry, {"gpt_tool": RecordingExecutor().execute}))
        task = self.store.create_task("reason about current status")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])
        simulation = self.store.get_evolution_simulation(task["task_id"])
        rollback = self.store.get_rollback_record(task["task_id"])

        self.assertEqual(decision["decision"], "do_not_evolve")
        self.assertEqual(decision["policy"], ["STABILITY", "OPTIMIZATION", "EVOLUTION"])
        self.assertEqual(decision["threshold_evaluation"]["thresholds_met"], [])
        self.assertIsNone(decision["proposal"])
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertEqual(simulation["performance_impact"]["estimated_step_reduction"], 0)
        self.assertEqual(rollback["performance_comparison"]["thresholds_met"], [])
        self.assertEqual(decision["risk_analysis"]["rollback_risk"]["level"], "minimal")

    def test_evolution_governor_generates_controlled_proposal_when_thresholds_are_met(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])
        simulation = self.store.get_evolution_simulation(task["task_id"])
        rollback = self.store.get_rollback_record(task["task_id"])

        self.assertEqual(decision["decision"], "evolve")
        self.assertIn("workflow_inefficiency", decision["threshold_evaluation"]["thresholds_met"])
        self.assertEqual(decision["proposal"]["target_module"], "workflow_optimizer")
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertIn("task_flow", simulation)
        self.assertIn("tool_routing", simulation)
        self.assertIn("workflow_graph", simulation)
        self.assertIn("performance_impact", simulation)
        self.assertIn("previous_architecture", rollback)
        self.assertIn("stable_version", rollback)
        self.assertIn("performance_comparison", rollback)

    def test_threshold_trigger_exposes_controlled_proposal_evidence_map(self):
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])
        simulation = self.store.get_evolution_simulation(task["task_id"])
        rollback = self.store.get_rollback_record(task["task_id"])

        self.assertEqual(decision["decision"], "evolve")
        self.assertEqual(decision["proposal"]["proposal_type"], "controlled_self_rewrite")
        self.assertTrue(decision["proposal"]["requires_approval"])
        self.assertFalse(decision["proposal"]["automatic_application"])
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertIn("workflow_inefficiency", decision["threshold_evaluation"]["thresholds_met"])
        self.assertGreater(simulation["performance_impact"]["estimated_step_reduction"], 0)
        self.assertEqual(rollback["stable_version"], "Tool System v1.8 pre-evolution baseline")
        self.assertEqual(rollback["performance_comparison"]["thresholds_met"], decision["threshold_evaluation"]["thresholds_met"])

    def test_evolution_governor_postpones_when_locked_module_would_be_modified(self):
        self.store.save_architecture_lock(
            module_name="workflow_optimizer",
            reason="Workflow optimization path is locked for stability.",
            locked_by="系统交付席",
        )
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])

        self.assertEqual(decision["decision"], "postpone_evolution")
        self.assertEqual(decision["proposal"]["target_module"], "workflow_optimizer")
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertTrue(decision["risk_analysis"]["locked_module_risk"]["blocked"])

    def test_locked_module_postpone_exposes_risk_evidence_map(self):
        self.store.save_architecture_lock(
            module_name="workflow_optimizer",
            reason="Workflow optimization path is locked for stability.",
            locked_by="系统交付席",
        )
        self.registry.register({"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"})
        self.registry.register({"name": "claude_tool", "type": "llm", "description": "Architecture", "entry": "claude"})
        self.registry.register({"name": "codex_tool", "type": "llm", "description": "Code", "entry": "codex"})
        employee = AIEmployee(
            ToolRouter(),
            ToolExecutor(
                self.registry,
                {
                    "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                    "claude_tool": AsyncRecordingExecutor("claude").execute,
                    "codex_tool": AsyncRecordingExecutor("codex").execute,
                },
            ),
        )
        task = self.store.create_task("创建一个登录页面并写API")

        asyncio.run(Orchestrator(self.store, PromptBuilder(), employee).run(task["task_id"]))
        decision = self.store.get_evolution_decision(task["task_id"])
        rollback = self.store.get_rollback_record(task["task_id"])

        locked_risk = decision["risk_analysis"]["locked_module_risk"]
        self.assertEqual(decision["decision"], "postpone_evolution")
        self.assertTrue(locked_risk["blocked"])
        self.assertEqual(locked_risk["target_module"], "workflow_optimizer")
        self.assertIn("workflow_optimizer", locked_risk["locked_modules"])
        self.assertFalse(decision["automatic_code_modification_allowed"])
        self.assertEqual(rollback["performance_comparison"]["thresholds_met"], decision["threshold_evaluation"]["thresholds_met"])

    def test_evolution_decision_api_returns_record_for_completed_task(self):
        app = create_app(
            str(Path(self.tmp.name) / "api.sqlite"),
            tool_functions={
                "gpt_tool": AsyncRecordingExecutor("gpt").execute,
                "claude_tool": AsyncRecordingExecutor("claude").execute,
                "codex_tool": AsyncRecordingExecutor("codex").execute,
            },
        )
        client = TestClient(app)
        task_id = client.post("/api/task", json={"content": "创建一个登录页面并写API"}).json()["task_id"]

        client.post(f"/api/task/{task_id}/run")
        response = client.get(f"/api/task/{task_id}/evolution-decisions")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["task_id"], task_id)
        self.assertIn(payload["decision"], ["evolve", "do_not_evolve", "postpone_evolution"])
        self.assertIn("risk_analysis", payload)
        self.assertIn("simulation", payload)
        self.assertIn("rollback", payload)
        self.assertIn("performance_impact", payload["simulation"])
        self.assertIn("performance_comparison", payload["rollback"])
        self.assertFalse(payload["automatic_code_modification_allowed"])

    def test_tool_api_registers_lists_and_executes_tools(self):
        executor = RecordingExecutor()
        app = create_app(str(Path(self.tmp.name) / "api.sqlite"), tool_functions={"gpt_tool": executor.execute})
        client = TestClient(app)

        register_response = client.post(
            "/api/tool/register",
            json={"name": "gpt_tool", "type": "llm", "description": "Reasoning", "entry": "gpt"},
        )
        execute_response = client.post("/api/tool/execute", json={"tool_name": "gpt_tool", "input": "Prompt"})
        tools_response = client.get("/api/tools")

        self.assertEqual(register_response.status_code, 200)
        self.assertEqual(execute_response.json()["output"], "Execution result")
        self.assertIn("gpt_tool", [tool["name"] for tool in tools_response.json()])

    def test_codex_executor_requires_model_gateway_configuration(self):
        original_values = {
            key: os.environ.get(key)
            for key in (
                "CURIS_MODEL_GATEWAY_BASE_URL",
                "CURIS_MODEL_GATEWAY_API_KEY",
                "CURIS_MODEL_GATEWAY_MODEL",
            )
        }
        for key in original_values:
            os.environ.pop(key, None)

        try:
            with self.assertRaisesRegex(RuntimeError, "Model Gateway Adapter requires"):
                CodexExecutor().execute("Run task")
        finally:
            for key, value in original_values.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
