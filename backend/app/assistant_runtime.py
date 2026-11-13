from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from .tenant_context import TenantContext


logger = logging.getLogger(__name__)

_PENDING_STATUSES = {"AWAITING_INPUT", "HUMAN_HANDOFF"}
_RUNNING_STATUSES = {"INIT", "PENDING", "PARSED", "RUNNING", "RESUMED"}
_QUERY_WORDS = ("怎么样", "如何", "状态", "进展", "风险", "多少", "哪些", "查询", "查看", "?")
_PAGE_CONTEXTS = {"workspace", "ceo-office", "project", "task"}
_CONTEXT_KEYS = {
    "page",
    "company_id",
    "department_id",
    "project_id",
    "task_id",
    "employee_id",
}
_NOTIFICATION_TYPES = {
    "assistant.command_submitted": ("指令已进入 Task", "info"),
    "assistant.identity_updated": ("Assistant Identity 已更新", "info"),
    "awaiting_input": ("Task 等待补充信息", "warning"),
    "input_supplied": ("Task 已补充信息", "info"),
    "human_handoff_requested": ("Task 请求人工接管", "warning"),
    "human_handoff_accepted": ("人工接管已接受", "info"),
    "human_handoff_reassigned": ("人工接管已转派", "info"),
    "execution_resumed": ("Task 已恢复执行", "info"),
    "execution_completed": ("Task 已完成", "success"),
    "execution_failed": ("Task 执行失败", "danger"),
    "execution_cancelled": ("Task 已取消", "warning"),
}
_ASSISTANT_MODEL_CAPABILITY_ID = "official.openai.gpt-5.4-mini-2026-03-17"


class AssistantIdentityIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(default="", max_length=80)
    avatar: str = Field(default="", max_length=32)
    role: str = Field(default="", max_length=160)
    tone: str = Field(default="", max_length=80)
    personality: str = Field(default="", max_length=500)


class AssistantPageContextIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: Literal["workspace", "ceo-office", "project", "task"] = "workspace"
    company_id: str = Field(default="", max_length=160)
    department_id: str = Field(default="", max_length=160)
    project_id: str = Field(default="", max_length=160)
    task_id: str = Field(default="", max_length=160)
    employee_id: str = Field(default="", max_length=160)


class AssistantCommandIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: str = Field(min_length=1, max_length=4000)
    intent: Literal["auto", "query", "execute"] = "auto"
    context: AssistantPageContextIn = Field(default_factory=AssistantPageContextIn)


class AssistantRuntimeService:
    """Tenant-scoped facade over existing Curis business services."""

    def __init__(
        self,
        *,
        database,
        company_runtime,
        organization,
        capability_catalog,
        store,
        memory_service,
        ai_usage,
        event_log,
        task_factory: Callable[..., dict[str, Any]],
    ) -> None:
        self.database = database
        self.company_runtime = company_runtime
        self.organization = organization
        self.capability_catalog = capability_catalog
        self.store = store
        self.memory_service = memory_service
        self.ai_usage = ai_usage
        self.event_log = event_log
        self.task_factory = task_factory

    def get_identity(self) -> dict[str, Any]:
        tenant_id = self._tenant()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from assistant_identities where tenant_id = ?",
                (tenant_id,),
            ).fetchone()
        if row is None:
            return {
                "tenant_id": tenant_id,
                "name": "",
                "avatar": "",
                "role": "",
                "tone": "",
                "personality": "",
                "updated_at": None,
            }
        return dict(row)

    def update_identity(self, values: dict[str, Any]) -> dict[str, Any]:
        tenant_id = self._tenant()
        clean = {
            "name": self._identity_text(values.get("name"), "name", 80),
            "avatar": self._identity_text(values.get("avatar"), "avatar", 32),
            "role": self._identity_text(values.get("role"), "role", 160),
            "tone": self._identity_text(values.get("tone"), "tone", 80),
            "personality": self._identity_text(
                values.get("personality"), "personality", 500
            ),
        }
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into assistant_identities (
                  tenant_id, name, avatar, role, tone, personality
                ) values (?, ?, ?, ?, ?, ?)
                on conflict (tenant_id) do update set
                  name=excluded.name,
                  avatar=excluded.avatar,
                  role=excluded.role,
                  tone=excluded.tone,
                  personality=excluded.personality,
                  updated_at=current_timestamp
                """,
                (
                    tenant_id,
                    clean["name"],
                    clean["avatar"],
                    clean["role"],
                    clean["tone"],
                    clean["personality"],
                ),
            )
        self.event_log.record(
            correlation_id=f"assistant-identity:{tenant_id}",
            event_type="assistant.identity_updated",
            payload={"changed_fields": sorted(clean)},
            tenant_id=tenant_id,
        )
        return self.get_identity()

    def snapshot(self) -> dict[str, Any]:
        facts = self._facts()
        pending = self._pending(facts["tasks"])
        risks = self._risks(facts)
        counts = {
            "companies": len(facts["companies"]),
            "business_departments": len(facts["departments"]),
            "projects": len(facts["projects"]),
            "tasks": len(facts["tasks"]),
            "employees": len(facts["employees"]),
            "capabilities": len(facts["capabilities"]),
            "artifacts": len(facts["artifacts"]),
            "memory_entries": len(facts["memories"]),
        }
        return {
            "tenant_id": self._tenant(),
            "generated_at": self._now(),
            "identity": self.get_identity(),
            "brief": {
                "date": self._now()[:10],
                "summary": (
                    f"当前有 {counts['business_departments']} 个业务部门、"
                    f"{counts['projects']} 个项目、{counts['tasks']} 个 Task，"
                    f"{len(pending)} 项需要处理、{len(risks)} 项风险。"
                ),
                "counts": counts,
                "ai_usage": facts["usage"],
                "recent_artifacts": [
                    self._artifact_view(item) for item in facts["artifacts"][:5]
                ],
            },
            "pending": pending,
            "risks": risks,
        }

    def notifications(
        self, *, after_event_id: int = 0, limit: int = 50
    ) -> dict[str, Any]:
        events = self.event_log.list_for_tenant(
            self._tenant(),
            after_event_id=after_event_id,
            event_types=set(_NOTIFICATION_TYPES),
            limit=limit,
        )
        return {
            "tenant_id": self._tenant(),
            "notifications": [self._notification(event) for event in events],
            "latest_event_id": events[-1]["event_id"] if events else after_event_id,
        }

    def submit_command(
        self,
        *,
        command: str,
        intent: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        clean_command = " ".join(str(command or "").split())
        if not clean_command:
            raise ValueError("command is required")
        if len(clean_command) > 4000:
            raise ValueError("command is too long")
        safe_context = self._validated_context(self._context(context))
        resolved_intent = self._intent(clean_command, intent)
        if resolved_intent == "query":
            return self._answer_query(clean_command, safe_context)

        project = self._resolve_project(clean_command, safe_context)
        if project is None:
            return {
                "tenant_id": self._tenant(),
                "intent": "execute",
                "status": "awaiting_context",
                "required": ["project_id"],
                "message": "执行指令需要明确 Project 上下文。",
            }
        employee_id = safe_context.get("employee_id") or project.get(
            "owner_employee_id"
        )
        if not employee_id:
            return {
                "tenant_id": self._tenant(),
                "intent": "execute",
                "status": "awaiting_context",
                "required": ["employee_id"],
                "message": "执行指令需要明确 Employee。",
            }
        employee = self.organization.get_employee_instance(employee_id)
        if employee is None:
            raise KeyError("employee not found")
        if (
            employee["company_id"] != project["company_id"]
            or employee["department_id"] != project["department_id"]
        ):
            raise ValueError("assistant employee does not belong to project")
        model_bindings = [
            item
            for item in self.organization.list_employee_capability_bindings(
                employee_id
            )["bindings"]
            if item["enabled"]
            and item["capability_source"] == "official"
            and item["capability_type"] == "model"
            and item["capability_id"] == _ASSISTANT_MODEL_CAPABILITY_ID
        ]
        if len(model_bindings) != 1:
            return {
                "tenant_id": self._tenant(),
                "intent": "execute",
                "status": "awaiting_capability",
                "required": ["employee_model_capability"],
                "employee_id": employee_id,
                "message": "执行员工需要绑定唯一可用的官方 Model Capability。",
            }
        task = self.task_factory(
            command=clean_command,
            project_id=project["project_id"],
            employee_id=employee_id or None,
            capability_source="official",
            capability_type="model",
            capability_id=_ASSISTANT_MODEL_CAPABILITY_ID,
        )
        self.event_log.record(
            correlation_id=task["task_id"],
            event_type="assistant.command_submitted",
            payload={
                "task_id": task["task_id"],
                "project_id": task.get("project_id") or "",
                "employee_id": task.get("employee_id") or "",
                "page": safe_context.get("page") or "workspace",
            },
            tenant_id=self._tenant(),
        )
        return {
            "tenant_id": self._tenant(),
            "intent": "execute",
            "status": "created",
            "task_id": task["task_id"],
            "project_id": task.get("project_id") or "",
            "capability_id": task.get("requested_capability_id") or "",
        }

    def _facts(self) -> dict[str, Any]:
        return {
            "companies": self.company_runtime.list_companies()["companies"],
            "departments": self.organization.list_department_instances()[
                "departments"
            ],
            "projects": self.company_runtime.list_projects()["projects"],
            "tasks": self.store.list_tasks(),
            "employees": self.organization.list_employee_instances()["employees"],
            "capabilities": self.capability_catalog.list(),
            "artifacts": self.store.list_artifacts(limit=50),
            "memories": self.memory_service.list_entries()["entries"],
            "usage": self.ai_usage.aggregate()["totals"],
        }

    def _answer_query(
        self, command: str, context: dict[str, str]
    ) -> dict[str, Any]:
        facts = self._facts()
        project = self._resolve_project(command, context, facts=facts)
        if project is not None:
            tasks = [
                item
                for item in facts["tasks"]
                if item.get("project_id") == project["project_id"]
            ]
            artifacts = [
                item
                for item in facts["artifacts"]
                if self._artifact_project(item, facts["tasks"])
                == project["project_id"]
            ]
            failed = sum(item["status"] == "FAILED" for item in tasks)
            pending = sum(item["status"] in _PENDING_STATUSES for item in tasks)
            running = sum(item["status"] in _RUNNING_STATUSES for item in tasks)
            answer = (
                f"{project['name']}当前状态为{project['status']}；"
                f"共有 {len(tasks)} 个 Task，其中 {running} 个执行中、"
                f"{pending} 个待处理、{failed} 个失败；已有 {len(artifacts)} 项成果。"
            )
            return {
                "tenant_id": self._tenant(),
                "intent": "query",
                "status": "answered",
                "answer": answer,
                "identity": self.get_identity(),
                "facts": {
                    "scope": "project",
                    "project_id": project["project_id"],
                    "project_status": project["status"],
                    "task_count": len(tasks),
                    "running_count": running,
                    "pending_count": pending,
                    "failed_count": failed,
                    "artifact_count": len(artifacts),
                },
                "source_refs": [
                    {"type": "project", "id": project["project_id"]},
                ],
            }

        department = self._resolve_department(command, context, facts)
        if department is not None:
            projects = [
                item
                for item in facts["projects"]
                if item.get("department_id") == department["id"]
            ]
            project_ids = {item["project_id"] for item in projects}
            tasks = [
                item
                for item in facts["tasks"]
                if item.get("project_id") in project_ids
            ]
            employees = [
                item
                for item in facts["employees"]
                if item.get("department_id") == department["id"]
            ]
            blocked = sum(item["status"] == "blocked" for item in projects)
            failed = sum(item["status"] == "FAILED" for item in tasks)
            answer = (
                f"{department['name']}当前有 {len(employees)} 名员工、"
                f"{len(projects)} 个项目和 {len(tasks)} 个 Task；"
                f"{blocked} 个项目阻塞、{failed} 个 Task 失败。"
            )
            return {
                "tenant_id": self._tenant(),
                "intent": "query",
                "status": "answered",
                "answer": answer,
                "identity": self.get_identity(),
                "facts": {
                    "scope": "business_department",
                    "department_id": department["id"],
                    "employee_count": len(employees),
                    "project_count": len(projects),
                    "task_count": len(tasks),
                    "blocked_project_count": blocked,
                    "failed_task_count": failed,
                },
                "source_refs": [
                    {"type": "business_department", "id": department["id"]},
                ],
            }

        snapshot = self.snapshot()
        return {
            "tenant_id": self._tenant(),
            "intent": "query",
            "status": "answered",
            "answer": snapshot["brief"]["summary"],
            "identity": snapshot["identity"],
            "facts": {
                "scope": "workspace",
                **snapshot["brief"]["counts"],
            },
            "source_refs": [{"type": "workspace", "id": self._tenant()}],
        }

    def _resolve_project(
        self,
        command: str,
        context: dict[str, str],
        *,
        facts: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        project_id = context.get("project_id")
        if project_id:
            return self.company_runtime.get_project(project_id)
        projects = (
            facts["projects"]
            if facts is not None
            else self.company_runtime.list_projects()["projects"]
        )
        matches = [
            item
            for item in projects
            if item.get("name") and item["name"].lower() in command.lower()
        ]
        return matches[0] if len(matches) == 1 else None

    def _validated_context(self, context: dict[str, str]) -> dict[str, str]:
        result = dict(context)
        task = None
        if result.get("task_id"):
            task = self.store.get_task(result["task_id"])
            if result.get("project_id") and task.get("project_id") != result["project_id"]:
                raise ValueError("assistant task context does not belong to project")
            result["project_id"] = result.get("project_id") or task.get("project_id") or ""
        project = None
        if result.get("project_id"):
            project = self.company_runtime.get_project(result["project_id"])
            if result.get("company_id") and project["company_id"] != result["company_id"]:
                raise ValueError("assistant project context does not belong to company")
            if result.get("department_id") and project["department_id"] != result["department_id"]:
                raise ValueError("assistant project context does not belong to department")
            result["company_id"] = result.get("company_id") or project["company_id"]
            result["department_id"] = result.get("department_id") or project["department_id"]
        if result.get("company_id"):
            self.company_runtime.get_company(result["company_id"])
        if result.get("department_id"):
            department = self.organization.get_department_instance(
                result["department_id"]
            )
            if department is None:
                raise KeyError("department not found")
            if result.get("company_id") and department["company_id"] != result["company_id"]:
                raise ValueError("assistant department context does not belong to company")
        if result.get("employee_id"):
            employee = self.organization.get_employee_instance(result["employee_id"])
            if employee is None:
                raise KeyError("employee not found")
            if result.get("company_id") and employee["company_id"] != result["company_id"]:
                raise ValueError("assistant employee context does not belong to company")
            if result.get("department_id") and employee["department_id"] != result["department_id"]:
                raise ValueError("assistant employee context does not belong to department")
        return result

    @staticmethod
    def _resolve_department(
        command: str,
        context: dict[str, str],
        facts: dict[str, Any],
    ) -> dict[str, Any] | None:
        department_id = context.get("department_id")
        if department_id:
            return next(
                (
                    item
                    for item in facts["departments"]
                    if item["id"] == department_id
                ),
                None,
            )
        matches = [
            item
            for item in facts["departments"]
            if item.get("name") and item["name"].lower() in command.lower()
        ]
        return matches[0] if len(matches) == 1 else None

    @staticmethod
    def _pending(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "id": task["task_id"],
                "type": "task",
                "status": task["status"].lower(),
                "title": str(task.get("content") or "未命名 Task")[:120],
                "task_id": task["task_id"],
                "project_id": task.get("project_id") or "",
                "updated_at": task.get("updated_at") or task.get("created_at"),
            }
            for task in tasks
            if task["status"] in _PENDING_STATUSES
        ][:20]

    @staticmethod
    def _risks(facts: dict[str, Any]) -> list[dict[str, Any]]:
        risks: list[dict[str, Any]] = []
        for project in facts["projects"]:
            if project["status"] == "blocked":
                risks.append(
                    {
                        "id": f"project:{project['project_id']}",
                        "type": "project_blocked",
                        "severity": "high",
                        "title": f"{project['name']}处于阻塞状态",
                        "project_id": project["project_id"],
                    }
                )
        for task in facts["tasks"]:
            if task["status"] == "FAILED":
                risks.append(
                    {
                        "id": f"task:{task['task_id']}",
                        "type": "task_failed",
                        "severity": "high",
                        "title": str(task.get("content") or "Task 执行失败")[:120],
                        "task_id": task["task_id"],
                        "project_id": task.get("project_id") or "",
                    }
                )
        usage = facts["usage"]
        if usage["unmetered_count"]:
            risks.append(
                {
                    "id": "ai-usage:unmetered",
                    "type": "ai_usage_unmetered",
                    "severity": "warning",
                    "title": f"{usage['unmetered_count']} 次 AI 调用未完成计量",
                }
            )
        if usage["failed_count"]:
            risks.append(
                {
                    "id": "ai-usage:failed",
                    "type": "ai_usage_failed",
                    "severity": "warning",
                    "title": f"{usage['failed_count']} 次 AI 调用失败",
                }
            )
        return risks[:30]

    @staticmethod
    def _notification(event: dict[str, Any]) -> dict[str, Any]:
        title, severity = _NOTIFICATION_TYPES[event["event_type"]]
        payload = event["payload"] if isinstance(event["payload"], dict) else {}
        refs = {
            key: payload[key]
            for key in (
                "task_id",
                "project_id",
                "department_id",
                "employee_id",
                "capability_id",
                "usage_record_id",
            )
            if payload.get(key)
        }
        return {
            "notification_id": event["event_id"],
            "event_type": event["event_type"],
            "title": title,
            "severity": severity,
            "entity_refs": refs,
            "occurred_at": event["created_at"],
        }

    @staticmethod
    def _artifact_view(artifact: dict[str, Any]) -> dict[str, Any]:
        return {
            "artifact_id": artifact["artifact_id"],
            "task_id": artifact["task_id"],
            "title": artifact["title"],
            "artifact_type": artifact["artifact_type"],
            "status": artifact["status"],
            "created_at": artifact["created_at"],
        }

    @staticmethod
    def _artifact_project(
        artifact: dict[str, Any], tasks: list[dict[str, Any]]
    ) -> str:
        task = next(
            (item for item in tasks if item["task_id"] == artifact["task_id"]),
            None,
        )
        return "" if task is None else task.get("project_id") or ""

    @staticmethod
    def _intent(command: str, requested: str) -> str:
        if requested in {"query", "execute"}:
            return requested
        # ponytail: local keyword routing; replace with Model Gateway
        # classification only when live Assistant-model routing is approved.
        return "query" if any(word in command for word in _QUERY_WORDS) else "execute"

    @staticmethod
    def _context(context: dict[str, Any]) -> dict[str, str]:
        unknown = set(context) - _CONTEXT_KEYS
        if unknown:
            raise ValueError("unsupported assistant context fields")
        result: dict[str, str] = {}
        for key in _CONTEXT_KEYS:
            value = " ".join(str(context.get(key) or "").split())
            if len(value) > 160:
                raise ValueError(f"{key} is too long")
            result[key] = value
        result["page"] = result["page"] or "workspace"
        if result["page"] not in _PAGE_CONTEXTS:
            raise ValueError("unsupported assistant page context")
        return result

    @staticmethod
    def _identity_text(value: Any, field: str, limit: int) -> str:
        clean = " ".join(str(value or "").split())
        if len(clean) > limit:
            raise ValueError(f"{field} is too long")
        if any(ord(character) < 32 for character in clean):
            raise ValueError(f"{field} contains control characters")
        return clean

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _tenant() -> str:
        tenant_id = TenantContext.current_tenant_id().strip()
        if not tenant_id:
            raise PermissionError("tenant_id is required")
        return tenant_id


async def _run_assistant_task(
    orchestrator,
    task_id: str,
    tenant_id: str,
    identity: dict[str, str],
) -> None:
    try:
        with TenantContext.scope(
            tenant_id,
            subject_id=identity.get("subject_id", ""),
            company_id=identity.get("company_id", ""),
            ceo_id=identity.get("ceo_id", ""),
            role=identity.get("role", ""),
            membership_status=identity.get("membership_status", ""),
            request_id=identity.get("request_id", ""),
        ):
            await orchestrator.run(task_id)
    except Exception as error:
        logger.warning(
            "Assistant Task failed: %s (%s)", task_id, type(error).__name__
        )


def build_assistant_router(
    service: AssistantRuntimeService,
    *,
    store,
    orchestrator,
) -> APIRouter:
    router = APIRouter(prefix="/api/workspace/assistant", tags=["assistant"])

    @router.get("/identity")
    def get_identity():
        return _call(service.get_identity)

    @router.put("/identity")
    def update_identity(payload: AssistantIdentityIn):
        return _call(service.update_identity, payload.model_dump())

    @router.get("/snapshot")
    def get_snapshot():
        return _call(service.snapshot)

    @router.get("/notifications")
    def get_notifications(
        after_event_id: int = Query(default=0, ge=0),
        limit: int = Query(default=50, ge=1, le=200),
    ):
        return _call(
            service.notifications,
            after_event_id=after_event_id,
            limit=limit,
        )

    @router.post("/commands", status_code=202)
    def submit_command(
        payload: AssistantCommandIn,
        background_tasks: BackgroundTasks,
    ):
        result = _call(
            service.submit_command,
            command=payload.command,
            intent=payload.intent,
            context=payload.context.model_dump(),
        )
        if result["status"] != "created":
            return result
        task_id = result["task_id"]
        task = store.get_task(task_id)
        if task["status"] == "INIT":
            store.transition(task_id, "PENDING")
            background_tasks.add_task(
                _run_assistant_task,
                orchestrator,
                task_id,
                TenantContext.current_tenant_id(),
                TenantContext.current_identity(),
            )
        return {**result, "status": "queued", "job_id": task_id}

    return router


def _call(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
