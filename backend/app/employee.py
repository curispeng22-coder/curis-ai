from __future__ import annotations

from .role_context import RoleContextReference
from .tool_executor import ToolExecutor
from .tool_router import ToolRouter


class AIEmployee:
    def __init__(self, router: ToolRouter, executor: ToolExecutor):
        self.router = router
        self.executor = executor

    async def execute(
        self,
        task_content: str,
        prompt: str,
        role_profile_id: str | None = None,
        role_context: RoleContextReference | None = None,
    ) -> dict:
        effective_prompt = self._with_role_context(prompt, role_profile_id, role_context)
        tool_chain = self.router.plan(task_content)
        return await self.executor.execute_chain(tool_chain, effective_prompt, self.router.fallback_chain)

    async def execute_step(
        self,
        step: dict,
        step_input: str,
        role_profile_id: str | None = None,
        role_context: RoleContextReference | None = None,
    ) -> dict:
        effective_input = self._with_role_context(step_input, role_profile_id, role_context)
        tool_chain = self.router.tools_for_step(step)
        return await self.executor.execute_chain(tool_chain, effective_input, self.router.fallback_chain)

    @staticmethod
    def _with_role_context(text: str, role_profile_id, role_context) -> str:
        if not role_profile_id or role_context is None:
            return text
        try:
            context = role_context.build(role_profile_id)
        except Exception:
            return text
        if not context:
            return text
        excerpt = context.get("context_excerpt")
        if not excerpt:
            return text
        return f"{text}\n\nRole Context (guidance only):\n{excerpt}"
