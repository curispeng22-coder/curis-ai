"""业务工作台引导（Workbench Guide）后端服务。

创建入口引导：引导 AI 与用户对话摸清业务需求 → 结构化摘要成工作台蓝图 →
用户确认 → 复用现有原语落地生成项目/部门/员工。设计文档：
docs/plan/workbench-guide-backend-design.md。

关键设计（与设计文档一致）：
- 引导流程数据驱动（GuideTemplate），v1 内置 ``guide.business_workbench``，
  注册表预留公司 onboarding 扩展点（未来 admin 化 = 配置表，前端零改动）。
- 引导阶段无 task/employee/project 归属，不走 ``execute_model_gateway``
  （其要求任务归属）；由 ``GuideModelResolver`` 独立解析引导模型
  （自定义 tenant_private model/agent 优先，官方偏好兜底），
  直接构造 ``ModelGatewayAdapter`` 调用。模型调用失败不静默降级，
  重试耗尽转 ``manual_fallback``（前端普通表单）。
- 落地复用 ``EmployeeTemplateContract`` / ``CompanyProjectRuntime`` 原语，
  不新建任何 CRUD 端点。
- 不落密钥：collected_json / blueprint_json 写前经 secret 扫描；
  model_used 仅存脱敏摘要。
"""

from __future__ import annotations

import json
import uuid
from typing import Any

from .credential_vault import is_resolver_managed_ref
from .database import Database
from .evolution_event_log import EvolutionEventLog
from .model_catalog import _reject_secret_like_metadata
from .model_gateway import (
    ModelGatewayAdapter,
    ModelGatewayExecutionError,
    resolve_gateway_api_key,
)
from .model_preferences import TenantModelPreferenceResolver
from .tenant_context import TenantContext

GUIDE_SESSION_STATUSES = ("INIT", "COLLECTING", "READY", "CONFIRMED", "DONE", "ABANDONED")
GUIDE_PRIVATE_CAPABILITY_TYPES = ("model", "agent")
MAX_MODEL_RETRIES = 2

# ── 内置引导模板（数据驱动，v1 代码 seed；未来 admin 化 = 配置表） ──────
BUILTIN_GUIDE_TEMPLATES: dict[str, dict[str, Any]] = {
    "guide.business_workbench": {
        "guide_id": "guide.business_workbench",
        "version": "1.0.0",
        "name": "业务工作台引导",
        "audience": "tenant_side",
        "steps": [
            {
                "step": 1,
                "type": "free_form",
                "title": "描述你的业务",
                "prompt": "你想做的业务是什么？请用几句话描述：业务目标、面向谁、预期产出。",
                "ai_turns": 3,
                "min_chars": 20,
                "extract_schema": {
                    "goal": {"type": "string", "required": True},
                    "domain": {"type": "string", "required": False},
                    "audience": {"type": "string", "required": False},
                },
            },
            {
                "step": 2,
                "type": "confirm",
                "title": "确认工作台方案",
                "prompt": "基于你的描述，我建议这样搭建工作台。请确认或修改：",
                "blueprint_schema": {
                    "project_name": {"type": "string", "required": True},
                    "goal": {"type": "string", "required": True},
                    "description": {"type": "string", "required": False},
                    "departments": {
                        "type": "array",
                        "required": True,
                        "items": {
                            "template_id": {"type": "string", "required": True},
                            "name": {"type": "string", "required": False},
                            "employees": {
                                "type": "array",
                                "required": False,
                                "items": {
                                    "template_id": {"type": "string", "required": True},
                                    "name": {"type": "string", "required": False},
                                    "allowed_effect_classes": {
                                        # Phase-10 岗位授权（员工实例级覆盖，空 = 继承模板）
                                        "type": "array",
                                        "required": False,
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                    "owner_employee_ref": {"type": "string", "required": False},
                },
            },
        ],
        "model": {"prefer": "custom", "fallback": "official_default"},
        "blueprint": "workbench",
    },
}


class GuideTemplateError(ValueError):
    """引导模板不可用（404 语义）。"""

    def __init__(self, message: str, *, status: str = "not_found", http_status: int = 404):
        super().__init__(message)
        self.status = status
        self.http_status = http_status


class GuideSessionError(ValueError):
    """引导会话状态冲突 / 非法输入（409 / 422 语义）。"""

    def __init__(self, message: str, *, status: str = "conflict", http_status: int = 409):
        super().__init__(message)
        self.status = status
        self.http_status = http_status


class GuideTemplateRegistry:
    """引导模板注册表：v1 内置；预留 onboarding 扩展点。"""

    def __init__(self, templates: dict[str, dict[str, Any]] | None = None) -> None:
        self._templates = (
            dict(templates) if templates is not None else dict(BUILTIN_GUIDE_TEMPLATES)
        )

    def list(self) -> list[dict[str, Any]]:
        return [
            {
                "guide_id": template["guide_id"],
                "version": template["version"],
                "name": template["name"],
                "steps": [
                    {key: step[key] for key in ("step", "type", "title") if key in step}
                    for step in template["steps"]
                ],
            }
            for template in self._templates.values()
        ]

    def get(self, guide_id: str) -> dict[str, Any]:
        template = self._templates.get(guide_id)
        if template is None:
            raise GuideTemplateError(f"guide template {guide_id} not found")
        return template


class GuideModelResolver:
    """引导模型解析：自定义 tenant_private model/agent 优先，官方偏好/默认兜底。

    resolve 阶段允许 custom → official 兜底（无自定义能力时）；但模型**调用**
    失败绝不静默换模型（见 GuideService._call_with_retry）。
    """

    def __init__(
        self,
        *,
        database: Database,
        model_preferences: TenantModelPreferenceResolver,
        default_executor: ModelGatewayAdapter,
        credential_vault: Any | None = None,
        http_post: Any | None = None,
    ) -> None:
        self.database = database
        self.model_preferences = model_preferences
        self.default_executor = default_executor
        self.credential_vault = credential_vault
        self.http_post = http_post or getattr(default_executor, "http_post", None)

    def resolve(
        self, tenant_id: str, prefer: str = "custom"
    ) -> tuple[ModelGatewayAdapter, dict[str, str]]:
        """返回 (executor, model_used)。model_used 仅脱敏摘要，绝不含密钥。"""
        if prefer == "custom":
            for candidate in self._custom_candidates(tenant_id):
                executor, summary = self._build_custom_executor(candidate)
                if executor is not None:
                    return executor, summary
        return self._official_executor()

    def _custom_candidates(self, tenant_id: str) -> list[dict[str, Any]]:
        capabilities = self.database.list_tenant_private_capabilities(tenant_id)
        candidates = [
            capability
            for capability in capabilities
            if capability.get("capability_type") in GUIDE_PRIVATE_CAPABILITY_TYPES
            and capability.get("status") == "active"
        ]
        preference = self.model_preferences.read_current().get("preference")
        if preference and preference.get("source") == "tenant_private":
            preferred = str(preference.get("model_key") or "")
            candidates.sort(key=lambda item: item.get("capability_id") != preferred)
        return candidates

    def _build_custom_executor(
        self, capability: dict[str, Any]
    ) -> tuple[ModelGatewayAdapter | None, dict[str, str] | None]:
        metadata = capability.get("metadata") or {}
        endpoint = str(metadata.get("endpoint") or metadata.get("base_url") or "").rstrip("/")
        if not endpoint:
            return None, None
        credential_ref = str(
            metadata.get("credential_ref") or metadata.get("config_ref") or ""
        )
        api_key = self._resolve_key(credential_ref)
        if not api_key:
            return None, None
        adapter = ModelGatewayAdapter(
            base_url=endpoint,
            api_key=api_key,
            gateway_id=str(
                metadata.get("provider_type")
                or capability.get("capability_type")
                or "openai-compatible"
            ),
            model_name=str(
                metadata.get("model_name") or capability.get("capability_id") or "agent"
            ),
            timeout=self.default_executor.timeout,
            http_post=self.http_post,
        )
        summary = {
            "source": "tenant_private",
            "capability_type": str(capability.get("capability_type") or ""),
            "capability_id": str(capability.get("capability_id") or ""),
            "provider": adapter.gateway_id,
            "model": adapter.model_name,
        }
        return adapter, summary

    def _resolve_key(self, credential_ref: str) -> str | None:
        if not credential_ref:
            return None
        if is_resolver_managed_ref(credential_ref):
            if self.credential_vault is None:
                return None
            info = self.credential_vault.resolve(credential_ref)
            secret = str(info.get("secret") or "") if info else ""
            return secret or None
        if credential_ref.startswith("env:"):
            return resolve_gateway_api_key(credential_ref) or None
        return None

    def _official_executor(
        self,
    ) -> tuple[ModelGatewayAdapter, dict[str, str]]:
        preference = self.model_preferences.resolve_runtime_model()
        if preference and preference.get("source") == "official":
            executor = ModelGatewayAdapter(
                base_url=self.default_executor.base_url,
                api_key=self.default_executor.api_key,
                gateway_id=preference["gateway_id"],
                model_name=preference["model_name"],
                timeout=self.default_executor.timeout,
                http_post=self.http_post,
            )
            return executor, {
                "source": "official",
                "provider": executor.gateway_id,
                "model": executor.model_name,
            }
        return self.default_executor, {
            "source": "official_default",
            "provider": self.default_executor.gateway_id,
            "model": self.default_executor.model_name,
        }


class WorkbenchInstantiator:
    """工作台蓝图落地：复用 EmployeeTemplateContract / CompanyProjectRuntime 原语。"""

    def __init__(
        self,
        *,
        database: Database,
        event_log: EvolutionEventLog,
        employees: Any,
        company_runtime: Any,
    ) -> None:
        self.database = database
        self.event_log = event_log
        self.employees = employees
        self.company_runtime = company_runtime

    def instantiate(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        """落地蓝图 → 部门/员工/项目。返回工作台摘要。"""
        tenant_id = TenantContext.current_tenant_id()
        self._validate_blueprint(blueprint)
        company_id = self._default_company_id(tenant_id)

        department_ids: list[str] = []
        employee_ids: list[str] = []
        employee_name_to_id: dict[str, str] = {}
        for dept in blueprint["departments"]:
            dept_inst = self.employees.create_department_instance(
                template_id=dept["template_id"],
                name=dept.get("name", ""),
                company_id=company_id,
            )
            department_id = dept_inst["id"]
            department_ids.append(department_id)
            for employee in dept.get("employees") or []:
                employee_inst = self.employees.create_employee_instance(
                    department_id=department_id,
                    template_id=employee["template_id"],
                    name=employee.get("name", ""),
                    company_id=company_id,
                )
                employee_ids.append(employee_inst["id"])
                if employee.get("name"):
                    employee_name_to_id[employee["name"]] = employee_inst["id"]
                # Phase-10 岗位授权：蓝图允许的 effect_class 作为员工实例级覆盖
                # （空 = 继承岗位模板默认；非空 = 按业务收敛授权）。
                allowed_classes = employee.get("allowed_effect_classes")
                if allowed_classes:
                    with self.database.connect() as connection:
                        connection.execute(
                            "update employee_instances set allowed_effect_classes_json = ? "
                            "where tenant_id = ? and id = ?",
                            (
                                json.dumps(
                                    [str(item) for item in allowed_classes],
                                    ensure_ascii=False,
                                ),
                                TenantContext.current_tenant_id(),
                                employee_inst["id"],
                            ),
                        )

        owner_employee_id = self._resolve_owner(blueprint, employee_ids, employee_name_to_id)
        project = self.company_runtime.create_project(
            company_id=company_id,
            name=blueprint["project_name"],
            goal=blueprint["goal"],
            description=blueprint.get("description", ""),
            department_id=department_ids[0],
            owner_employee_id=owner_employee_id,
            status="active",
        )
        result = {
            "project_id": project["project_id"],
            "project_name": project["name"],
            "company_id": company_id,
            "department_ids": department_ids,
            "employee_ids": employee_ids,
            "owner_employee_id": owner_employee_id,
        }
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="guide.workbench_created",
            tenant_id=tenant_id,
            payload={
                "project_id": result["project_id"],
                "company_id": company_id,
                "departments": len(department_ids),
                "employees": len(employee_ids),
                "owner_employee_id": owner_employee_id,
            },
        )
        return result

    def _default_company_id(self, tenant_id: str) -> str:
        # list_companies 内部惰性确保默认公司存在（is_default=1, status=active），
        # 并按下默认优先排序，companies[0] 即租户默认公司。
        companies = self.company_runtime.list_companies()["companies"]
        default = next(
            (company for company in companies if company.get("is_default")),
            companies[0] if companies else None,
        )
        if default is None:
            raise GuideSessionError(
                "尚未创建公司，请先创建公司后再发起业务引导",
                status="no_company",
                http_status=422,
            )
        return default["company_id"]

    def _resolve_owner(
        self,
        blueprint: dict[str, Any],
        employee_ids: list[str],
        employee_name_to_id: dict[str, str],
    ) -> str | None:
        reference = str(blueprint.get("owner_employee_ref") or "").strip()
        if not reference:
            return None
        if reference.startswith("emp-"):
            return reference if reference in employee_ids else None
        # "部门名/员工名" 或 "员工名"
        name = reference.split("/")[-1].strip()
        return employee_name_to_id.get(name)

    @staticmethod
    def _validate_blueprint(blueprint: dict[str, Any]) -> None:
        if not isinstance(blueprint, dict):
            raise GuideSessionError("blueprint must be an object", http_status=422)
        if not str(blueprint.get("project_name") or "").strip():
            raise GuideSessionError("blueprint.project_name is required", http_status=422)
        if not str(blueprint.get("goal") or "").strip():
            raise GuideSessionError("blueprint.goal is required", http_status=422)
        departments = blueprint.get("departments")
        if not isinstance(departments, list) or not departments:
            raise GuideSessionError("blueprint.departments must be a non-empty array", http_status=422)
        for dept in departments:
            if not isinstance(dept, dict) or not str(dept.get("template_id") or "").strip():
                raise GuideSessionError("each department requires template_id", http_status=422)
            for employee in dept.get("employees") or []:
                if not isinstance(employee, dict) or not str(employee.get("template_id") or "").strip():
                    raise GuideSessionError("each employee requires template_id", http_status=422)


class GuideService:
    """引导会话编排：start / answer / confirm / abandon + 事件记录。"""

    def __init__(
        self,
        *,
        database: Database,
        event_log: EvolutionEventLog,
        registry: GuideTemplateRegistry,
        resolver: GuideModelResolver,
        instantiator: WorkbenchInstantiator,
    ) -> None:
        self.database = database
        self.event_log = event_log
        self.registry = registry
        self.resolver = resolver
        self.instantiator = instantiator

    # ── 公开入口 ──────────────────────────────────────────────────
    def list_guides(self) -> list[dict[str, Any]]:
        return self.registry.list()

    def start_session(self, guide_id: str) -> dict[str, Any]:
        template = self.registry.get(guide_id)
        tenant_id = TenantContext.current_tenant_id()
        session_id = f"gs-{uuid.uuid4()}"
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into guide_sessions (
                  session_id, tenant_id, guide_id, guide_version, status,
                  current_step, collected_json, blueprint_json, model_used, updated_at
                ) values (?, ?, ?, ?, 'COLLECTING', 1, '{}', NULL, NULL, current_timestamp)
                """,
                (session_id, tenant_id, guide_id, template["version"]),
            )
        return {
            "session_id": session_id,
            "guide_id": guide_id,
            "status": "COLLECTING",
            "current_step": 1,
            "step": template["steps"][0],
        }

    def answer(self, session_id: str, step: int, answer: str) -> dict[str, Any]:
        session = self._get_session(session_id)
        template = self.registry.get(session["guide_id"])
        self._require_status(session, "COLLECTING")
        if int(step) != int(session["current_step"]):
            raise GuideSessionError("step does not match current step", http_status=422)
        if not str(answer or "").strip():
            raise GuideSessionError("answer is required", http_status=422)
        try:
            _reject_secret_like_metadata(answer=answer)
        except ValueError as error:
            raise GuideSessionError(str(error), http_status=422) from error

        collected = json.loads(session["collected_json"] or "{}")
        collected[str(step)] = {"answer": str(answer)}

        tenant_id = TenantContext.current_tenant_id()
        executor, model_used = self.resolver.resolve(
            tenant_id, prefer=self._model_prefer(template)
        )
        prompt = self._build_prompt(template, int(step), collected)
        output = self._call_with_retry(executor, prompt, model_used, session_id, tenant_id)
        if output is None:
            return self._manual_fallback(template, int(step), model_used)

        parsed = self._parse_ai_output(output)
        if parsed is None:
            return self._manual_fallback(template, int(step), model_used)

        mode = parsed.get("mode")
        if mode == "follow_up":
            self._save_state(session_id, tenant_id, collected=collected)
            return {
                "session_id": session_id,
                "status": "COLLECTING",
                "current_step": int(step),
                "mode": "follow_up",
                "question": str(parsed.get("question") or "请补充说明："),
            }

        if mode == "blueprint":
            blueprint = parsed.get("blueprint")
            if not isinstance(blueprint, dict) or not blueprint:
                return self._manual_fallback(template, int(step), model_used)
            self._save_state(
                session_id,
                tenant_id,
                collected=collected,
                blueprint=blueprint,
                status="READY",
                current_step=int(step) + 1,
                model_used=model_used,
            )
            return {
                "session_id": session_id,
                "status": "READY",
                "current_step": int(step) + 1,
                "mode": "blueprint",
                "blueprint": blueprint,
                "model_used": model_used,
            }

        return self._manual_fallback(template, int(step), model_used)

    def confirm(self, session_id: str, blueprint: dict[str, Any]) -> dict[str, Any]:
        session = self._get_session(session_id)
        self._require_status(session, "READY")
        try:
            _reject_secret_like_metadata(blueprint=blueprint)
        except ValueError as error:
            raise GuideSessionError(str(error), http_status=422) from error
        result = self.instantiator.instantiate(blueprint)
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute(
                """
                update guide_sessions
                set status = 'DONE', blueprint_json = ?, updated_at = current_timestamp
                where session_id = ? and tenant_id = ?
                """,
                (json.dumps(blueprint, ensure_ascii=False), session_id, tenant_id),
            )
        return {"session_id": session_id, "status": "DONE", "workbench": result}

    def abandon(self, session_id: str) -> dict[str, Any]:
        session = self._get_session(session_id)
        if session["status"] in {"DONE", "ABANDONED"}:
            raise GuideSessionError(
                f"session is already {session['status']}", http_status=409
            )
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            connection.execute(
                """
                update guide_sessions
                set status = 'ABANDONED', updated_at = current_timestamp
                where session_id = ? and tenant_id = ?
                """,
                (session_id, tenant_id),
            )
        return {"session_id": session_id, "status": "ABANDONED"}

    # ── 内部 ──────────────────────────────────────────────────────
    def _get_session(self, session_id: str) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from guide_sessions where session_id = ? and tenant_id = ?",
                (session_id, tenant_id),
            ).fetchone()
        if row is None:
            raise GuideSessionError("guide session not found", http_status=404)
        return dict(row)

    @staticmethod
    def _require_status(session: dict[str, Any], expected: str) -> None:
        if session["status"] != expected:
            raise GuideSessionError(
                f"session status {session['status']} does not allow this action"
            )

    @staticmethod
    def _model_prefer(template: dict[str, Any]) -> str:
        return str((template.get("model") or {}).get("prefer") or "custom")

    def _build_prompt(
        self, template: dict[str, Any], step: int, collected: dict[str, Any]
    ) -> str:
        step_def = next(s for s in template["steps"] if s["step"] == step)
        parts = [step_def["prompt"]]
        for index, item in collected.items():
            answer = item.get("answer") or ""
            if answer:
                parts.append(f"[已收集·步骤{index}] {answer}")
        parts.append(
            "请严格只输出一个 JSON 对象（不要 markdown 代码块）："
            '{"mode": "follow_up", "question": "追问用户的一句话"} '
            "或 {\"mode\": \"blueprint\", \"blueprint\": {工作台蓝图}}。"
            "若信息不足以生成蓝图，必须用 follow_up 追问；"
            "蓝图至少包含 project_name、goal、departments[].template_id。"
        )
        return "\n".join(parts)

    def _call_with_retry(
        self,
        executor: ModelGatewayAdapter,
        prompt: str,
        model_used: dict[str, str],
        session_id: str,
        tenant_id: str,
    ) -> str | None:
        """调用引导模型；失败重试（同一 executor，绝不换模型），耗尽返回 None。

        捕获 ModelGatewayExecutionError（网关错误）与 RuntimeError
        （validate_runtime_config 配置不完整）两类失败；其余异常不应被吞，
        让调用方显式处理（属编程错误，应立即暴露）。
        """
        for attempt in range(1, MAX_MODEL_RETRIES + 1):
            try:
                response = executor.execute(prompt)
            except (ModelGatewayExecutionError, RuntimeError) as error:
                self._record_model_call(
                    session_id,
                    tenant_id,
                    model_used,
                    ok=False,
                    status=str(getattr(error, "status", "failed")),
                    http_status=int(getattr(error, "http_status", 0) or 0),
                    latency_ms=int(getattr(error, "latency_ms", 0) or 0),
                    outbound_attempted=bool(
                        getattr(error, "outbound_attempted", False)
                    ),
                )
                continue
            content = ""
            try:
                # ModelGatewayAdapter.execute 返回精简结果（output 为模型文本）。
                content = str(response.get("output") or "")
            except (KeyError, IndexError, TypeError):
                pass
            self._record_model_call(
                session_id, tenant_id, model_used, ok=True, status="ok"
            )
            if content.strip():
                return content
        return None

    def _record_model_call(
        self,
        session_id: str,
        tenant_id: str,
        model_used: dict[str, str],
        *,
        ok: bool,
        status: str,
        http_status: int = 0,
        latency_ms: int = 0,
        outbound_attempted: bool = False,
    ) -> None:
        try:
            self.event_log.record(
                correlation_id=session_id,
                event_type="guide.model_call",
                tenant_id=tenant_id,
                payload={
                    **model_used,
                    "ok": ok,
                    "status": status,
                    "http_status": http_status,
                    "latency_ms": latency_ms,
                    "outbound_attempted": outbound_attempted,
                    "runtime_stage": "provider_execution",
                },
            )
        except Exception:  # 事件记录失败不阻断引导主流程
            pass

    @staticmethod
    def _parse_ai_output(content: str) -> dict[str, Any] | None:
        text = content.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        try:
            parsed = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return None
        if not isinstance(parsed, dict):
            return None
        mode = parsed.get("mode")
        if mode not in {"follow_up", "blueprint"}:
            return None
        return parsed

    def _save_state(
        self,
        session_id: str,
        tenant_id: str,
        *,
        collected: dict[str, Any],
        blueprint: dict[str, Any] | None = None,
        status: str = "COLLECTING",
        current_step: int | None = None,
        model_used: dict[str, str] | None = None,
    ) -> None:
        sets = ["collected_json = ?", "status = ?", "updated_at = current_timestamp"]
        params: list[Any] = [json.dumps(collected, ensure_ascii=False), status]
        if blueprint is not None:
            sets.append("blueprint_json = ?")
            params.append(json.dumps(blueprint, ensure_ascii=False))
        if current_step is not None:
            sets.append("current_step = ?")
            params.append(current_step)
        if model_used is not None:
            sets.append("model_used = ?")
            params.append(json.dumps(model_used, ensure_ascii=False))
        params.extend([session_id, tenant_id])
        with self.database.connect() as connection:
            connection.execute(
                f"update guide_sessions set {', '.join(sets)} "
                "where session_id = ? and tenant_id = ?",
                params,
            )

    def _manual_fallback(
        self, template: dict[str, Any], step: int, model_used: dict[str, str]
    ) -> dict[str, Any]:
        step_def = next(s for s in template["steps"] if s["step"] == step)
        fields = list((step_def.get("extract_schema") or {}).keys())
        return {
            "mode": "manual_fallback",
            "message": "引导 AI 暂不可用，请直接填写以下字段：",
            "fields": fields,
            "model_used": model_used,
        }
