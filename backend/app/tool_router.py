from __future__ import annotations


class ToolRouter:
    def __init__(self, model_tool_name: str | None = None):
        self.model_tool_name = model_tool_name

    def _model_tool(self, legacy_name: str) -> str:
        return self.model_tool_name or legacy_name

    def plan(self, task_content: str) -> list[str]:
        content = task_content.lower()
        tools = []
        if any(keyword in content for keyword in ("architecture", "system design", "technical design")):
            tools.append(self._model_tool("claude_tool"))
        if any(keyword in content for keyword in ("reason", "analyze", "explain", "think")):
            tools.append(self._model_tool("gpt_tool"))
        if any(keyword in content for keyword in ("code", "implement", "function", "debug", "parser")):
            tools.append(self._model_tool("codex_tool"))
        return tools or [self._model_tool("default_tool")]

    def select_tool(self, task_content: str) -> str:
        return self.plan(task_content)[0]

    def tools_for_step(self, step: dict) -> list[str]:
        if step.get("tool_required"):
            return [self._model_tool(step["tool_required"])]
        action = step.get("action", "").lower()
        if "analyze" in action or "validate" in action:
            return [self._model_tool("gpt_tool")]
        if "design" in action or "architecture" in action:
            return [self._model_tool("claude_tool")]
        if "frontend" in action or "backend" in action or "code" in action:
            return [self._model_tool("codex_tool")]
        return [self._model_tool("default_tool")]

    def tool_for_generated_step(self, step: dict) -> str:
        text = " ".join(
            str(step.get(key, ""))
            for key in ("step_name", "purpose", "expected_output", "action", "description")
        ).lower()
        if any(keyword in text for keyword in ("architecture", "system design", "technical design", "架构")):
            return self._model_tool("claude_tool")
        if any(keyword in text for keyword in ("ui design", "ui设计", "design ui", "设计")):
            return self._model_tool("claude_tool")
        if any(keyword in text for keyword in ("code", "coding", "implement", "frontend", "backend", "api", "代码", "实现", "前端", "后端", "接口")):
            return self._model_tool("codex_tool")
        if any(keyword in text for keyword in ("reason", "reasoning", "analyze", "analysis", "validate", "test", "需求", "分析", "联调", "测试", "验证")):
            return self._model_tool("gpt_tool")
        return self._model_tool("gpt_tool")

    def select_best_tool(self, step: dict, performance: dict[str, dict] | None = None) -> str:
        primary = self.tool_for_generated_step(step)
        performance = performance or {}
        candidates = self.fallback_chain(primary)
        known_candidates = [tool for tool in candidates if tool in performance]
        if not known_candidates:
            return primary
        return max(
            candidates,
            key=lambda tool: performance.get(tool, {}).get("priority_weight", -1000 if tool != primary else 0),
        )

    def fallback_chain(self, tool_name: str) -> list[str]:
        fallbacks = {
            "model_gateway_tool": ["model_gateway_tool"],
            "codex_tool": ["codex_tool", "gpt_tool", "default_tool"],
            "gpt_tool": ["gpt_tool", "claude_tool", "default_tool"],
            "claude_tool": ["claude_tool", "gpt_tool", "default_tool"],
            "default_tool": ["default_tool"],
        }
        return fallbacks.get(tool_name, [tool_name, "default_tool"])

    def rd_tools_for_step(self, step: dict, employee_role: str) -> list[str]:
        """研发部步骤 → 工具路由。当 role 为 tech_lead/backend_engineer 且 step 为 code_change 时，走 real_rd_executor_tool。

        否则回落 tools_for_step(step)（模型生成或默认工具）。
        """
        if employee_role in ("tech_lead", "backend_engineer"):
            step_type = (step.get("step_type") or "").lower()
            step_name = (step.get("step_name") or "").lower()
            is_code_change = (
                step_type == "code_change"
                or any(kw in step_name for kw in ("编码", "修改", "code", "modify"))
            )
            if is_code_change:
                return [self._model_tool("real_rd_executor_tool")]
        return self.tools_for_step(step)
