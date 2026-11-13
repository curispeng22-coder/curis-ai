import asyncio
import unittest
from pathlib import Path

from app.employee import AIEmployee
from app.prompt_builder import PromptBuilder
from app.role_context import RoleContextReference
from app.tool_router import ToolRouter


class RecordingChainExecutor:
    def __init__(self):
        self.prompts = []

    async def execute_chain(self, tool_chain, prompt, fallback_chain):
        self.prompts.append(prompt)
        tool = tool_chain[0] if tool_chain else "default_tool"
        return {
            "tool_name": tool,
            "output": "Execution result",
            "cost": 0.01,
            "trace": [
                {
                    "tool": tool,
                    "input": prompt,
                    "output": "Execution result",
                    "error": None,
                    "step": 1,
                    "timestamp": "t",
                }
            ],
        }


class D1RoleWiringTest(unittest.TestCase):
    def setUp(self):
        self.profiles_path = Path(__file__).resolve().parents[2] / "knowledge" / "ROLE_PROFILES.md"
        self.reference = RoleContextReference(self.profiles_path)
        self.valid_id = "curis.role.system-delivery.v1"
        self.invalid_id = "curis.role.unknown.v1"

    def test_prompt_builder_appends_excerpt_for_valid_profile(self):
        prompt = PromptBuilder().build(
            "Write a short plan", role_profile_id=self.valid_id, role_context=self.reference
        )
        self.assertIn("Role Profile:", prompt)
        self.assertIn("系统交付席", prompt)
        self.assertIn("Write a short plan", prompt)

    def test_prompt_builder_unchanged_without_profile_id(self):
        base = PromptBuilder().build("Write a short plan")
        self.assertNotIn("Role Profile:", base)
        self.assertIn("Write a short plan", base)

    def test_prompt_builder_unchanged_with_invalid_profile(self):
        prompt = PromptBuilder().build(
            "Write a short plan", role_profile_id=self.invalid_id, role_context=self.reference
        )
        self.assertNotIn("Role Profile:", prompt)
        self.assertIn("Write a short plan", prompt)

    def test_employee_execute_appends_excerpt_for_valid_profile(self):
        executor = RecordingChainExecutor()
        employee = AIEmployee(ToolRouter(), executor)
        asyncio.run(
            employee.execute(
                "architecture review", "BasePrompt", role_profile_id=self.valid_id, role_context=self.reference
            )
        )
        self.assertEqual(len(executor.prompts), 1)
        self.assertIn("Role Profile:", executor.prompts[0])
        self.assertIn("BasePrompt", executor.prompts[0])

    def test_employee_execute_unchanged_without_profile(self):
        executor = RecordingChainExecutor()
        employee = AIEmployee(ToolRouter(), executor)
        asyncio.run(employee.execute("architecture review", "BasePrompt"))
        self.assertEqual(executor.prompts[0], "BasePrompt")

    def test_employee_execute_step_appends_excerpt_for_valid_profile(self):
        executor = RecordingChainExecutor()
        employee = AIEmployee(ToolRouter(), executor)
        step = {"step": 1, "step_name": "前端实现", "purpose": "coding"}
        asyncio.run(
            employee.execute_step(
                step, "StepInput", role_profile_id=self.valid_id, role_context=self.reference
            )
        )
        self.assertIn("Role Profile:", executor.prompts[0])
        self.assertIn("StepInput", executor.prompts[0])

    def test_employee_execute_step_unchanged_without_profile(self):
        executor = RecordingChainExecutor()
        employee = AIEmployee(ToolRouter(), executor)
        step = {"step": 1, "step_name": "前端实现", "purpose": "coding"}
        asyncio.run(employee.execute_step(step, "StepInput"))
        self.assertEqual(executor.prompts[0], "StepInput")


if __name__ == "__main__":
    unittest.main()
