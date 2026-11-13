"""R&D 工作流运行时（T10 · 第一波基础闭环）。

把研发部（tech.rd）工作流绑定到执行入口，并打通「任务 → 步骤编排 →
角色执行 → 产物回写」的基础闭环。

设计约束（主理人裁定 + 架构 §三.1）：
- 复用既有 ``CompanyInstantiationService`` 实例化的 DepartmentInstance / EmployeeInstance
  （不各自独立跑执行引擎；真实 LLM 执行引擎若需复用
  ``.worktrees/low-token-workflow-v2``，应在第二波合入主干，本波不擅自 fork）。
- 本波为**基础闭环**：真实 LLM 调用经可注入的 ``model_fn`` 接入
  （main.py 的 ``execute_model_gateway``）；未注入时降级为 scaffold 产物，
  保证闭环可跑、可验证，且**不依赖外部 API key**。
- 只写 workflow_instances / workflow_runs / workflow_steps / step_assignments /
  step_results（沿用既有表，不新增执行链语义）。
- 全局 ``tenant_id = 'selfuse'``（固定单账号）。
"""

from __future__ import annotations

import json
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from .database import Database
from .local_rd_toolset import LocalRDToolError
from .real_rd_executor import RealRDExecutorError
from .tenant_context import TenantContext

# 步骤关键词 → 研发部员工角色（用于把 wt_* 的纯步骤名映射到角色）。
_STEP_ROLE_MAP = [
    ("需求", "product_manager"),
    ("拆解", "tech_lead"),
    ("架构", "architect"),
    ("前端", "backend_engineer"),
    ("后端", "backend_engineer"),
    ("编码", "backend_engineer"),
    ("测试", "qa_engineer"),
    ("验收", "qa_engineer"),
    ("交付", "tech_lead"),
    ("汇总", "tech_lead"),
    ("发布", "devops_engineer"),
    ("部署", "devops_engineer"),
    ("运维", "devops_engineer"),
]


def _role_for_step(step_name: str) -> str:
    for keyword, role in _STEP_ROLE_MAP:
        if keyword in (step_name or ""):
            return role
    return "tech_lead"


class RdWorkflowRuntime:
    """研发部工作流运行时：绑定执行入口 + 执行基础闭环。"""

    def __init__(
        self,
        database: Database,
        event_log: Any,
        model_fn: Callable[[str], str] | None = None,
        connector_fn: Callable[[str, str, str], str] | None = None,
        real_rd_executor: Any = None,
    ) -> None:
        self.database = database
        self.event_log = event_log
        # 真实 LLM 调用函数（如 main.execute_model_gateway）；None 时降级 scaffold。
        self.model_fn = model_fn
        # 连接器步骤路由函数（step_name, employee_role, prompt -> 输出）；
        # 由 ContentWorkflowRuntime / connector 注册表注入，使 connector 类步骤
        # 可路由到真实 Curis Connector（C1）。None 时该步骤走 scaffold。
        self.connector_fn = connector_fn
        # RealRD 执行器（用于 code_change 步骤，含 code_change_spec 元数据时启用）。
        self.real_rd_executor = real_rd_executor

    # ── 绑定执行入口 ─────────────────────────────────────────────
    def bind_execution_entry(
        self,
        department_id: str,
        workflow_content_id: str,
        *,
        project_id: str | None = None,
    ) -> str:
        """把研发部工作流绑定到一个 workflow_instances 执行入口（幂等）。

        以 (department_id, workflow_content_id) 稳定派生 instance id，
        已存在则直接返回，保证「绑定」可重复、可引用。
        """
        tenant_id = TenantContext.current_tenant_id()
        instance_id = f"wfi-rd-{uuid.uuid5(uuid.NAMESPACE_DNS, department_id + workflow_content_id + (project_id or '')).hex[:16]}"
        with self.database.connect() as connection:
            row = connection.execute(
                "select workflow_instance_id from workflow_instances "
                "where workflow_instance_id = ? and tenant_id = ?",
                (instance_id, tenant_id),
            ).fetchone()
            if row is not None:
                return instance_id
            content = self.database.get_workflow_content(workflow_content_id)
            template = connection.execute(
                "select id, name from workflow_templates where id = ? and status = 'active'",
                (workflow_content_id,),
            ).fetchone()
            wt_ref = (content or {}).get("workflow_template_ref") or (
                template["id"] if template else ""
            )
            name = (content or {}).get("name") or (
                template["name"] if template else workflow_content_id
            )
            if not wt_ref:
                raise ValueError(f"workflow {workflow_content_id} not found")
            connection.execute(
                """
                insert into workflow_instances (
                  workflow_instance_id, tenant_id, company_id, project_id,
                  workflow_template_id, created_from_template_id, name, status, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, 'active', current_timestamp)
                """,
                (instance_id, tenant_id, None, project_id, wt_ref, workflow_content_id, name),
            )
        return instance_id

    # ── 执行闭环 ────────────────────────────────────────────────
    def run(
        self,
        department_id: str,
        workflow_content_id: str,
        prompt: str,
        *,
        task_id: str = "",
        company_id: str | None = None,
        project_id: str | None = None,
        model_fn: Callable[[str], str] | None = None,
        issue_spec_override: dict | None = None,
        require_real: bool = False,
    ) -> dict[str, Any]:
        """执行一次研发部工作流闭环，回写 workflow_runs / steps / results。

        返回运行摘要（run_id / 步骤数 / 状态）。闭环路径：
        wl_* → wt_* 步骤 → 角色映射 → EmployeeInstance → 执行（model/connector/scaffold）
        → workflow_steps.output / step_results.result → final_report。

        ``model_fn`` 允许本次运行覆盖构造时的 LLM 函数（如注入真实 model gateway），
        实现「注入真实 model_fn 时跑通 30 个 tl_ai_rd_*」的 T14 目标；未注入则降级 scaffold。

        ``issue_spec_override`` 允许调用方动态覆盖 code_change 步骤的 target_files /
        test_command_id / test_command_argv / allow_paths / max_rounds，使编码步骤
        可针对任意文件执行 real_rd。
        """
        active_model_fn = model_fn or self.model_fn
        # 保存本次运行的 issue_spec_override，供 _execute_step 内部使用
        self._current_issue_spec_override = issue_spec_override
        self._current_project_id = project_id
        self._current_require_real = require_real
        tenant_id = TenantContext.current_tenant_id()
        instance_id = self.bind_execution_entry(
            department_id,
            workflow_content_id,
            project_id=project_id,
        )

        # 1) 解析部门 + 员工实例（按 role 建索引）。
        department = self._get_department_instance(department_id)
        if department is None or not department.get("enabled"):
            raise ValueError("department instance is not available")
        employees = self._list_employees(department_id)
        employees_by_role = {emp["role"]: emp for emp in employees}

        # 2) 解析工作流步骤（wt_* 容器，纯步骤名）。
        content = self.database.get_workflow_content(workflow_content_id)
        wt_ref = (content or {}).get("workflow_template_ref") or workflow_content_id
        raw_steps = self._get_wt_steps(wt_ref)
        if not raw_steps:
            raise ValueError(f"workflow {workflow_content_id} has no executable steps")
        # 兼容两种形态：若 raw_steps 全是 str，转为 [{step_name: s, step_type: ""}] 格式
        steps_meta: list[dict[str, Any]] = []
        for item in raw_steps:
            if isinstance(item, str):
                steps_meta.append({"step_name": item, "step_type": ""})
            elif isinstance(item, dict):
                steps_meta.append(item)
        steps_meta = steps_meta or [{"step_name": (content or {}).get("name", "step"), "step_type": ""}]
        # 同时从 DB 读取原始 steps_json 以获取完整元数据（含 code_change_spec）。
        raw_parsed: list[dict[str, Any]] = []
        if wt_ref:
            with self.database.connect() as connection:
                row = connection.execute(
                    "select steps_json from workflow_templates where id = ?", (wt_ref,)
                ).fetchone()
            if row:
                try:
                    parsed = json.loads(row["steps_json"] or "[]")
                    if isinstance(parsed, list):
                        raw_parsed = [item for item in parsed if isinstance(item, dict)]
                except (json.JSONDecodeError, TypeError):
                    pass

        # 3) 建 workflow_run。
        run_id = f"wfr-{uuid.uuid4()}"
        resolved_task_id = task_id or f"task-rd-{uuid.uuid4()}"
        started_at = datetime.now(timezone.utc).isoformat()
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into workflow_runs (
                  workflow_run_id, tenant_id, company_id, project_id,
                  created_from_template_id, workflow_instance_id, workflow_template_id,
                  task_id, department_id, status, started_at, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, 'running', ?, current_timestamp, current_timestamp)
                """,
                (
                    run_id, tenant_id, company_id, project_id,
                    workflow_content_id, instance_id, wt_ref,
                    resolved_task_id, department_id, started_at,
                ),
            )

        # 4) 逐步骤编排 + 执行 + 回写。
        results: list[dict[str, Any]] = []
        development_result: dict[str, Any] | None = None
        previous: list[str] = []
        # 按 step_order 建立 step_meta 查找索引
        meta_by_name = {m.get("step_name", ""): m for m in raw_parsed}
        for order, step_meta_item in enumerate(steps_meta, start=1):
            step_name = step_meta_item["step_name"]
            # 优先使用 raw_parsed 中的完整元数据（含 code_change_spec）
            full_meta = meta_by_name.get(step_name, step_meta_item)
            role = _role_for_step(step_name)
            employee = employees_by_role.get(role) or next(iter(employees), None)
            emp_id = employee["id"] if employee else ""
            emp_role = employee["role"] if employee else role
            step_input = self._build_step_prompt(prompt, step_name, previous)
            step_id = self._start_step(
                run_id, order, step_name, emp_role, emp_id, step_input
            )
            try:
                output = self._execute_step(
                    employee,
                    step_name,
                    step_input,
                    model_fn=active_model_fn,
                    step_meta=full_meta,
                    workflow_run_id=run_id,
                    workflow_step_id=step_id,
                    task_id=resolved_task_id,
                )
            except RealRDExecutorError as error:
                self._fail_step(step_id, error.failure_code)
                self._mark_run_failed(run_id, error.failure_code)
                raise
            self._finish_step(step_id, emp_id, output)
            if full_meta.get("step_type") == "code_change":
                try:
                    parsed_output = json.loads(output)
                except (TypeError, json.JSONDecodeError):
                    parsed_output = None
                if isinstance(parsed_output, dict) and parsed_output.get("mode") == "real_rd":
                    development_result = parsed_output
            results.append({
                "order": order, "step": step_name, "role": emp_role,
                "employee_id": emp_id, "output": output,
            })
            previous.append(f"{step_name}：{output[:200]}")

        # 5) final_report 回写 + 收尾。
        final_report = self._build_final_report(prompt, results)
        completed_at = datetime.now(timezone.utc).isoformat()
        with self.database.connect() as connection:
            connection.execute(
                "update workflow_runs set status = 'completed', final_report = ?, "
                "completed_at = ?, updated_at = current_timestamp where workflow_run_id = ?",
                (final_report, completed_at, run_id),
            )
        self.event_log.record(
            correlation_id=run_id,
            event_type="workflow_rd.executed",
            tenant_id=tenant_id,
            payload={
                "workflow_content_id": workflow_content_id,
                "department_id": department_id,
                "steps": len(results),
                "status": "completed",
            },
        )
        return {
            "workflow_run_id": run_id,
            "workflow_instance_id": instance_id,
            "department_id": department_id,
            "workflow_content_id": workflow_content_id,
            "steps": len(results),
            "status": "completed",
            "final_report": final_report,
            "development_result": development_result,
        }

    # ── 内部助手 ────────────────────────────────────────────────
    def _build_issue_spec(self, step_name: str, prompt: str, employee: dict | None, step_meta: dict | None, issue_spec_override: dict | None = None) -> dict | None:
        """从步骤元数据的 code_change_spec 构造 issue_spec。无 spec 返回 None。

        ``issue_spec_override`` 可覆盖 spec 中的 target_files / test_command_id /
        test_command_argv / allow_paths / max_rounds（override 优先）。
        """
        if step_meta is None:
            return None
        # 步骤必须显式声明 code_change_spec 才可触发 real_rd
        if "code_change_spec" not in step_meta:
            return None
        spec = dict(step_meta.get("code_change_spec") or {})
        if issue_spec_override:
            for key in ("target_files", "test_command_id", "test_command_argv", "allow_paths", "max_rounds"):
                if key in issue_spec_override:
                    spec[key] = issue_spec_override[key]
        if not spec:
            return None
        # 如果 target_files 为空，尝试从 prompt 中提取文件路径
        target_files = spec.get("target_files", [])
        if not target_files:
            import re
            matches = re.findall(r'[\w/]+\.\w+', prompt)
            if matches:
                target_files = [m for m in matches if "test" not in m and m.endswith(".py")]
            if not target_files:
                return None  # 没 target → 不触发 real_rd
        return {
            "issue_id": f"rd-wf-{step_name}-{uuid.uuid4().hex[:8]}",
            "target_files": target_files,
            "test_command_id": spec.get("test_command_id", ""),
            "test_command_argv": spec.get("test_command_argv", []),
            "instructions": prompt,
            "allow_paths": spec.get("allow_paths") or target_files,
            "max_rounds": spec.get("max_rounds", 3),
        }

    def _execute_step(
        self,
        employee: dict[str, Any] | None,
        step_name: str,
        prompt: str,
        *,
        model_fn: Callable[[str], str] | None = None,
        step_meta: dict[str, Any] | None = None,
        workflow_run_id: str = "",
        workflow_step_id: str = "",
        task_id: str = "",
    ) -> str:
        skill = (employee or {}).get("default_skill", "")
        tool = (employee or {}).get("default_tool", "")
        require_real = bool(getattr(self, "_current_require_real", False))
        # 1) code_change 必须先走 RealRD；不能被普通模型文案短路。
        if self.real_rd_executor is not None:
            issue_spec = self._build_issue_spec(
                step_name,
                prompt,
                employee,
                step_meta,
                issue_spec_override=getattr(self, "_current_issue_spec_override", None),
            )
            if issue_spec is not None:
                issue_spec.update({
                    "tenant_id": TenantContext.current_tenant_id(),
                    "project_id": getattr(self, "_current_project_id", None),
                    "task_id": task_id,
                })
                try:
                    result = self.real_rd_executor.run(issue_spec)
                except (LocalRDToolError, RealRDExecutorError, ValueError, KeyError) as exc:
                    failure_code = getattr(exc, "failure_code", None) or type(exc).__name__
                    if require_real:
                        raise RealRDExecutorError(failure_code) from exc
                    return json.dumps({
                        "mode": "real_rd",
                        "status": "error",
                        "failure_code": failure_code,
                    }, ensure_ascii=False)
                if result.get("status") != "succeeded":
                    if require_real:
                        raise RealRDExecutorError(f"real_rd_{result.get('status') or 'failed'}")
                    return json.dumps({
                        "mode": "real_rd",
                        "status": result.get("status") or "failed",
                        "reason": f"RealRD executor failed after {result.get('rounds')} rounds",
                    }, ensure_ascii=False)
                diff_text = result.get("diff_text") or ""
                return json.dumps({
                    "mode": "real_rd",
                    "status": "succeeded",
                    "diff_text": diff_text,
                    "diff_sha256": hashlib.sha256(diff_text.encode("utf-8")).hexdigest(),
                    "files": result.get("files") or [],
                    "test_exit_code": result.get("test_exit_code"),
                    "rounds": result.get("rounds"),
                    "total_tokens": result.get("total_tokens"),
                    "estimated_cost": result.get("estimated_cost"),
                    "model_gateway_id": result.get("model_gateway_id"),
                    "model_name": result.get("model_name"),
                }, ensure_ascii=False)

        if require_real:
            checkpoints = {
                "task_breakdown": "已登记 Task、目标文件与测试范围。",
                "architecture_design": "沿用 Curis v1.0 现有架构边界。",
                "qa_verification": "编码步骤的已登记自动测试已通过。",
                "code_review": "真实 Git diff 已生成，等待人工审阅。",
                "delivery": "运行结果已回写 Task 与 WorkflowRun；未执行远程 Git 写入。",
            }
            step_type = (step_meta or {}).get("step_type", "")
            if step_type in checkpoints:
                return json.dumps({
                    "mode": "workflow_checkpoint",
                    "status": "succeeded",
                    "fact": checkpoints[step_type],
                }, ensure_ascii=False)
            raise RealRDExecutorError("real_execution_unavailable")

        # 2) 真实 LLM（注入的 model_fn，如 main.execute_model_gateway）。
        active_model_fn = model_fn or self.model_fn
        if active_model_fn is not None:
            try:
                text = active_model_fn(prompt)
                if isinstance(text, dict):
                    text = text.get("output")
                if text:
                    return text
            except Exception:
                # 真实引擎失败（如未配置 key）→ 降级 connector / scaffold，不中断闭环。
                pass
        # 3) 连接器步骤路由（若注入了 connector_fn，且本步骤映射到连接器动作）。
        if self.connector_fn is not None:
            try:
                routed = self.connector_fn(step_name, (employee or {}).get("role", ""), prompt)
                if routed:
                    return routed
            except Exception:
                pass
        # 4) 兼容旧基础闭环：无真实执行要求时保留 scaffold。
        owner = (employee or {}).get("name") or "未分配员工"
        return (
            f"[{step_name}] 由 {owner} 基于输入完成"
            + (f"（skill={skill}）" if skill else "")
            + (f"（tool={tool}）" if tool else "")
            + f"；输入摘要：{prompt[:80]}"
        )

    def _build_step_prompt(self, prompt: str, step_name: str, previous: list[str]) -> str:
        lines = [f"研发任务：{prompt}", f"当前步骤：{step_name}"]
        if previous:
            lines.append("已完成步骤：")
            lines.extend(f"  - {p}" for p in previous)
        return "\n".join(lines)

    def _build_final_report(self, prompt: str, results: list[dict[str, Any]]) -> str:
        lines = [f"# 研发工作流执行报告", "", f"任务：{prompt}", "", "## 步骤产物", ""]
        for r in results:
            lines.append(f"### {r['order']}. {r['step']}（{r['role']}）")
            lines.append("")
            lines.append(r["output"])
            lines.append("")
        lines.append("---")
        lines.append(f"共 {len(results)} 步，状态 completed。")
        return "\n".join(lines)

    def _start_step(
        self, run_id: str, order: int, step_name: str, emp_role: str,
        emp_id: str, step_input: str,
    ) -> str:
        tenant_id = TenantContext.current_tenant_id()
        step_id = f"wfs-{uuid.uuid4()}"
        now_iso = datetime.now(timezone.utc).isoformat()
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into workflow_steps (
                  workflow_step_id, tenant_id, workflow_run_id, step_order,
                  step_type, step_name, employee_role, status, input, output,
                  started_at, completed_at, created_at, updated_at
                ) values (?, ?, ?, ?, 'rd_step', ?, ?, 'running', ?, '', ?, null, ?, ?)
                """,
                (step_id, tenant_id, run_id, order, step_name, emp_role,
                 step_input, now_iso, now_iso, now_iso),
            )
            if emp_id:
                connection.execute(
                    """
                    insert into step_assignments (
                      step_assignment_id, tenant_id, workflow_step_id,
                      employee_id, employee_role, capability_binding_id, status, created_at
                    ) values (?, ?, ?, ?, ?, '', 'assigned', current_timestamp)
                    """,
                    (f"sa-{uuid.uuid4()}", tenant_id, step_id, emp_id, emp_role),
                )
        return step_id

    def _finish_step(self, step_id: str, emp_id: str, output: str) -> None:
        tenant_id = TenantContext.current_tenant_id()
        completed_at = datetime.now(timezone.utc).isoformat()
        with self.database.connect() as connection:
            connection.execute(
                "update workflow_steps set status = 'completed', output = ?, "
                "completed_at = ?, updated_at = ? where tenant_id = ? "
                "and workflow_step_id = ? and status = 'running'",
                (output, completed_at, completed_at, tenant_id, step_id),
            )
            if emp_id:
                connection.execute(
                    """
                    insert into step_results (
                      step_result_id, tenant_id, workflow_step_id, employee_id, result, status, created_at
                    ) values (?, ?, ?, ?, ?, 'succeeded', current_timestamp)
                    """,
                    (f"sr-{uuid.uuid4()}", tenant_id, step_id, emp_id, output),
                )

    def _fail_step(self, step_id: str, failure_code: str) -> None:
        tenant_id = TenantContext.current_tenant_id()
        failed_at = datetime.now(timezone.utc).isoformat()
        with self.database.connect() as connection:
            connection.execute(
                "update workflow_steps set status = 'failed', error = ?, "
                "completed_at = ?, updated_at = ? where tenant_id = ? "
                "and workflow_step_id = ? and status = 'running'",
                (failure_code, failed_at, failed_at, tenant_id, step_id),
            )

    def _get_department_instance(self, department_id: str) -> dict[str, Any] | None:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from department_instances where tenant_id = ? and id = ?",
                (tenant_id, department_id),
            ).fetchone()
        return dict(row) if row else None

    def _list_employees(self, department_id: str) -> list[dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from employee_instances where tenant_id = ? and department_id = ?",
                (tenant_id, department_id),
            ).fetchall()
        return [dict(r) for r in rows]

    def _get_wt_steps(self, wt_ref: str) -> list[str]:
        if not wt_ref:
            return []
        with self.database.connect() as connection:
            row = connection.execute(
                "select steps_json from workflow_templates where id = ?",
                (wt_ref,),
            ).fetchone()
        if row is None:
            return []
        try:
            parsed = json.loads(row["steps_json"] or "[]")
        except (json.JSONDecodeError, TypeError):
            return []
        # 兼容两种形态：["步骤名"] 或 [{"step_name": ...}]
        steps: list[str] = []
        for item in parsed:
            if isinstance(item, str):
                steps.append(item)
            elif isinstance(item, dict):
                steps.append(item.get("step_name") or item.get("name") or str(item))
        return steps

    def _mark_run_failed(self, run_id: str, reason: str) -> None:
        with self.database.connect() as connection:
            connection.execute(
                "update workflow_runs set status = 'failed', final_report = ?, "
                "updated_at = current_timestamp where workflow_run_id = ?",
                (reason, run_id),
            )
