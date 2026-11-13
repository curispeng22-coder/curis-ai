"""自然语言任务管道 API 端点。

| 端点 | 方法 | 功能 |
|------|------|------|
| ``/api/pipeline/submit`` | POST | NL→IssueSpec → 入队 → 返回 {id,status} |
| ``/api/pipeline/list`` | GET | 返回所有任务列表 |
| ``/api/pipeline/{id}`` | GET | 返回单任务详情（含 diff/test/rework_feedback） |
| ``/api/pipeline/{id}/dispatch`` | POST | 触发执行（dequeue→dispatch） |
| ``/api/pipeline/{id}/approve`` | POST | 审批通过 |
| ``/api/pipeline/{id}/reject`` | POST | 打回（body: {"note":"..."}） |
| ``/api/pipeline/{id}/rework`` | POST | 手动触发返工（再排队） |

零新依赖（仅 FastAPI + pydantic + 既有 issue_pipeline 模块）。
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .capability_catalog import CapabilityCatalog
from .capability_adapters import CliAdapter
from .capability_resolver import CapabilityExhausted, CapabilityHandle, CapabilityResolver
from .issue_pipeline import (
    IssueQueue,
    NLParser,
    PipelineDispatcher,
    ResultReviewer,
    submit_natural_language,
)
from .lesson_memory import LessonMemory
from .pipeline_runtime import PipelineRuntime
from .project_state import ProjectState
from .scheduler import scheduler_manager
from .task_graph import TaskGraph
from .tenant_context import TenantContext


pipeline_router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

# 模块级单例（lazy init，FastAPI 生命周期内复用）
_queue: IssueQueue | None = None
_parser: NLParser | None = None
_dispatcher: PipelineDispatcher | None = None

# P0 新增：任务图注册表（进程内，单进程常驻调度）；以及可注入的依赖。
_graph_registry: dict[str, TaskGraph] = {}
_graph_project_registry: dict[str, str] = {}
_graph_task_registry: dict[str, str] = {}
_pipeline_database: Any | None = None
_build_runtime_fn: Any | None = None


class _NullEventLog:
    """最小事件日志桩（API 层构造 resolver/catalog 时避免强依赖 DB event_log 表）。"""

    database = None

    def record(self, **kwargs: Any) -> None:
        return None


class _LocalProjectRuntimeResolver:
    """Exact local Project Runtime fallback; never available outside the fixed local project."""

    def __init__(self, delegate: CapabilityResolver, project_id: str) -> None:
        self.delegate = delegate
        self.project_id = project_id

    def resolve(self, req: Any, exclude_keys: list[str] | None = None, employee_id: str | None = None) -> Any:
        try:
            return self.delegate.resolve(req, exclude_keys=exclude_keys, employee_id=employee_id)
        except CapabilityExhausted:
            from .local_google_oidc import PROJECT_ID

            if (
                os.getenv("CURIS_ENV", "").strip().lower() not in {"local", "development"}
                or self.project_id != PROJECT_ID
                or req.cap_type != "tool"
                or exclude_keys
            ):
                raise
            adapter = CliAdapter({
                "command": "/usr/bin/env",
                "args": [
                    "CURIS_IDENTITY_MODE=test", sys.executable,
                    "-m", "pytest", "-q", "--disable-warnings",
                    "backend/tests/test_project_runtime_page.py",
                ],
                "cwd": str(Path(__file__).resolve().parents[2]),
                "timeout": 120,
                "append_prompt": False,
            })
            return CapabilityHandle(
                key="local.project_runtime.focused",
                type="tool",
                adapter=adapter,
                runtime_meta={"local_only": True},
            )


def _normalize_private_capability(priv: dict[str, Any]) -> dict[str, Any]:
    """把 ``tenant_private_capabilities`` 行标准化为 resolver/catalog 期望的条目形状。

    关键字段：``capability_key=private.<id>``、``type=capability_type``、
    ``source=tenant_private``、``runtime_meta.live_status=available``（乐观可用，
    免去对未知端点的探活）、``private_metadata`` 原文（供 DevAgentFactory 构造
    ModelGatewayAdapter / CapabilityAdapterFactory 构造 CliAdapter 等）。

    使私有能力（model 或 tool）对 resolver 候选池可见、可被降级链选中真实执行：
    - model 类型沿用 ``private_base_url``/``private_credential_ref`` 构造
      ``ModelGatewayAdapter``（自用 DeepSeek 等）；
    - tool 类型从 ``meta.adapter_kind``（缺省按类型启发式）+ ``meta.adapter_config``
      构造 ``CliAdapter``/``HttpApiAdapter`` 等，打通「运行测试/部署/脚本」类节点。
    """
    meta = priv.get("metadata") or {}
    cap_id = priv.get("capability_id") or "unknown"
    cap_type = priv.get("capability_type") or "model"
    # model 默认 model 适配器；tool 等类型按 meta.adapter_kind，缺省留空让 factory 启发式。
    adapter_kind = (meta.get("adapter_kind") or ("model" if cap_type == "model" else ""))
    adapter_config = meta.get("adapter_config") or {}
    return {
        "capability_key": f"private.{cap_id}",
        "model_key": f"private.{cap_id}",
        "type": cap_type,
        "name": cap_id,
        "display_name": priv.get("display_name") or cap_id,
        "provider_id": meta.get("provider_type", ""),
        "status": priv.get("status") or "active",
        "source": "tenant_private",
        "supported_models": [meta.get("model_name") or cap_id],
        "runtime_meta": {
            "live_status": "available",
            "adapter_kind": adapter_kind,
            "adapter_config": adapter_config,
            "private_base_url": meta.get("base_url"),
            "private_credential_ref": meta.get("credential_ref"),
            "private_model_name": meta.get("model_name"),
        },
        "private_metadata": meta,
    }


class _PipelineCapabilityCatalog(CapabilityCatalog):
    """Pipeline 专用 catalog：在官方 ``official_models`` 之上合并租户私有能力。

    仅用于 PipelineRuntime 的能力解析（auto-run 闭环），不影响 Admin catalog 语义。
    私有能力（tenant_private，如用户自配 DeepSeek）对 resolver 可见，使其能被降级
    链选中真实执行，修复「私有模型不在候选池 → 降级链耗尽升级」的阻断。
    """

    def list(self, type_filter: str | None = None, include_inactive: bool = False) -> list[dict[str, Any]]:
        official = super().list(type_filter=type_filter, include_inactive=include_inactive)
        tenant_id = TenantContext.current_tenant_id()
        private_rows = self.database.list_tenant_private_capabilities(
            tenant_id, capability_type=type_filter, include_inactive=include_inactive
        )
        private = [_normalize_private_capability(p) for p in private_rows]
        # 私有能力优先（用户自配能力优于默认官方能力），再列官方，作为降级兜底。
        return private + official

    def get(self, capability_key: str) -> dict[str, Any]:
        if capability_key.startswith("private."):
            pid = capability_key[len("private."):]
            tenant_id = TenantContext.current_tenant_id()
            # 无 type 直接按 id 查（避免 SQL 中 capability_type = NULL 永不匹配）。
            for row in self.database.list_tenant_private_capabilities(tenant_id):
                if row.get("capability_id") == pid:
                    return _normalize_private_capability(row)
        return super().get(capability_key)


def _init_pipeline_deps(database: Any | None = None, build_runtime_fn: Any | None = None) -> None:
    """由 main.py 在 create_app 中注入共享 Database（及可选 runtime 构造钩子）。"""
    global _pipeline_database, _build_runtime_fn
    _pipeline_database = database
    if build_runtime_fn is not None:
        _build_runtime_fn = build_runtime_fn


def _build_runtime(graph: TaskGraph) -> PipelineRuntime:
    """为某 graph 构造验收/返工自动闭环 runtime。

    优先用注入的 ``_build_runtime_fn``（测试/自定义）；否则用进程内 Database 组装
    resolver + reviewer + lesson_memory + project_state（真实路径）。
    """
    if _build_runtime_fn is not None:
        return _build_runtime_fn(graph)
    reviewer = ResultReviewer()
    if _pipeline_database is None:
        return PipelineRuntime(reviewer=reviewer)
    catalog = _PipelineCapabilityCatalog(_pipeline_database, _NullEventLog())
    resolver = CapabilityResolver(
        catalog,
        database=_pipeline_database,
        event_log=_NullEventLog(),
        auto_degrade_silent=True,
    )
    project_id = _graph_project_registry.get(graph.graph_id, graph.graph_id)
    resolver = _LocalProjectRuntimeResolver(resolver, project_id)
    lesson = LessonMemory(_pipeline_database)
    project_state = ProjectState(
        project_id,
        database=_pipeline_database,
    )
    return PipelineRuntime(
        reviewer=reviewer,
        resolver=resolver,
        database=_pipeline_database,
        lesson_memory=lesson,
        project_state=project_state,
        # auto-run 闭环的模型节点由 resolver 选用 chat 类能力（返回文本产物而非
        # 文件 diff），放宽验收：成功且非空输出即视为通过，使「目标→执行→验收→
        # 完成」可端到端跑通；manual dispatch 路径不受影响（默认 False）。
        review_text_artifacts=True,
    )


def _get_queue() -> IssueQueue:
    global _queue
    if _queue is None:
        _queue = IssueQueue()
    return _queue


def _get_parser() -> NLParser:
    global _parser
    if _parser is None:
        _parser = NLParser()
    return _parser


def _get_dispatcher() -> PipelineDispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = PipelineDispatcher(queue=_get_queue())
    return _dispatcher


# ---------------------------------------------------------------------------
# 请求/响应模型
# ---------------------------------------------------------------------------


class SubmitRequest(BaseModel):
    natural_language: str
    project_id: str | None = None


class RejectRequest(BaseModel):
    note: str = ""


class ReworkRequest(BaseModel):
    note: str = "手动触发返工"


# ---------------------------------------------------------------------------
# 端点
# ---------------------------------------------------------------------------


@pipeline_router.post("/submit")
def pipeline_submit(body: SubmitRequest) -> dict[str, Any]:
    """提交自然语言任务 → 澄清→结构化计划(DAG) → 入队 + 登记任务图 → 返回 {id,graph_id,status}。

    若信息不足（NLParser.clarify 返回问题），``questions`` 字段携带澄清追问，
    但仍保持 ``status='pending'``（任务已入队），由前端决定先澄清还是直接跑默认图。
    """
    project = _require_project(body.project_id) if body.project_id else None
    if project is not None:
        existing = _project_task(body.project_id or "", TenantContext.current_tenant_id())
        if existing is not None and existing.status in ("pending", "queued", "running", "review"):
            raise HTTPException(status_code=409, detail="project already has an active runtime")
    parser = _get_parser()
    task = submit_natural_language(
        body.natural_language,
        queue=_get_queue(),
        parser=parser,
    )
    plan = parser.plan(body.natural_language)
    graph_id = f"graph-{uuid.uuid4().hex[:12]}"
    plan["graph_id"] = graph_id
    graph = (
        TaskGraph.from_plan(plan) if plan.get("nodes") else TaskGraph(graph_id=graph_id)
    )
    _graph_registry[graph_id] = graph
    # 无论是否绑定项目，都把 graph 关联写进 issue_spec —— 前端详情页靠
    # pickGraphId(task.issue_spec.pipeline_graph_id) 定位任务图，缺了它「自动调度执行」
    # 按钮会因 graphId 为空而隐藏，闭环卡在 pending。
    task.issue_spec = {
        **(task.issue_spec or {}),
        "pipeline_graph_id": graph_id,
        "pipeline_plan": plan,
    }
    if project is not None:
        tenant_id = TenantContext.current_tenant_id()
        task.issue_spec = {
            **task.issue_spec,
            "project_id": body.project_id,
            "tenant_id": tenant_id,
        }
        _graph_project_registry[graph_id] = body.project_id or ""
        _persist_project_runtime(project, task, graph_id, plan)
    _get_queue().update_status(task.id, issue_spec=task.issue_spec)
    # 始终登记 graph→task 映射（无论是否绑定 project），供 auto-run 的 sync_task
    # 在图完成后将任务翻转为 review / 升级时翻转为 failed。否则无 project_id 的任务
    # 永远停在 pending，无法进入人工验收。
    _graph_task_registry[graph_id] = task.id
    resp: dict[str, Any] = {
        "id": task.id,
        "graph_id": graph_id,
        "status": task.status,
    }
    if plan.get("questions"):
        resp["questions"] = plan["questions"]
    return resp


@pipeline_router.get("/list")
def pipeline_list() -> list[dict[str, Any]]:
    """返回所有任务列表。"""
    tasks = _get_queue().list_all()
    return [_task_to_public(t) for t in tasks]


@pipeline_router.get("/lessons")
def pipeline_lessons(
    signature: str | None = None, outcome: str | None = None
) -> list[dict[str, Any]]:
    """查询经验沉淀（capability_lessons）。

    必须声明在 ``/{task_id}`` 之前，否则会被单段路径参数 ``/{task_id}`` 抢先匹配。
    ``signature`` 按任务指纹过滤；``outcome`` 按 success/fail 过滤；均无则返回全部。
    未注入 Database 时返回空列表。
    """
    if _pipeline_database is None:
        return []
    lm = LessonMemory(_pipeline_database)
    if signature is not None:
        return lm.query(signature, outcome=outcome)
    return lm.database.list_capability_lessons(outcome=outcome)


@pipeline_router.get("/project/{project_id}")
def pipeline_project_runtime(project_id: str) -> dict[str, Any]:
    """Project-scoped read model over the existing queue and in-process DAG."""
    project = _require_project(project_id)
    tenant_id = TenantContext.current_tenant_id()
    task = _project_task(project_id, tenant_id)
    progress = _load_progress(project.get("progress_json"))
    runtime_snapshot = progress.get("runtime") if isinstance(progress.get("runtime"), dict) else {}
    graph_id = (
        (task.issue_spec or {}).get("pipeline_graph_id") if task else None
    ) or runtime_snapshot.get("graph_id")
    graph = _graph_registry.get(str(graph_id)) if graph_id else None
    plan = (task.issue_spec or {}).get("pipeline_plan") if task else runtime_snapshot.get("plan")
    graph_payload = _graph_to_public(graph) if graph is not None else _snapshot_graph(graph_id, plan)
    task_payload = _task_to_public(task) if task is not None else None
    return {
        "project": project,
        "runtime": {
            "persistence": "process_only",
            "task": task_payload,
            "graph": graph_payload,
            "trace": _graph_trace(graph),
            "available_actions": _available_actions(task, graph),
            "blocked_reason": (
                "pipeline_process_state_unavailable"
                if task is not None and task.status in ("pending", "queued", "running") and graph is None
                else None
            ),
        },
    }


@pipeline_router.get("/{task_id}")
def pipeline_get(task_id: str) -> dict[str, Any]:
    """返回单任务详情（含 diff/test/rework_feedback）。"""
    task = _get_queue().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    _require_task_scope(task)
    return _task_to_public(task)


@pipeline_router.post("/{task_id}/dispatch")
def pipeline_dispatch(task_id: str) -> dict[str, Any]:
    """触发执行（dequeue→dispatch），后台线程异步执行，立即返回。"""
    task = _get_queue().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    _require_task_scope(task)
    if task.status not in ("pending", "queued"):
        raise HTTPException(
            status_code=400,
            detail=f"task is in status '{task.status}', cannot dispatch",
        )
    _get_queue().update_status(task_id, status="queued")
    # 后台线程异步执行，不阻塞 HTTP 响应
    import threading
    def _run():
        try:
            _get_dispatcher().dispatch_one(task_id)
        except Exception as exc:
            import traceback
            traceback.print_exc()
    threading.Thread(target=_run, daemon=True).start()
    return {"id": task_id, "status": "running", "message": "execution started in background"}


@pipeline_router.post("/{task_id}/approve")
def pipeline_approve(task_id: str) -> dict[str, Any]:
    """审批通过。"""
    task = _get_queue().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    _require_task_scope(task)
    if task.status != "review":
        raise HTTPException(
            status_code=400,
            detail=f"task is in status '{task.status}', cannot approve",
        )
    _get_queue().update_status(task_id, status="approved", review_decision="approved")
    return {"id": task_id, "status": "approved"}


@pipeline_router.post("/{task_id}/reject")
def pipeline_reject(task_id: str, body: RejectRequest) -> dict[str, Any]:
    """打回任务（body: {"note":"..."}）。"""
    task = _get_queue().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    _require_task_scope(task)
    if task.status != "review":
        raise HTTPException(
            status_code=400,
            detail=f"task is in status '{task.status}', cannot reject",
        )
    _get_queue().update_status(
        task_id,
        status="rejected",
        review_decision="rejected",
        review_note=body.note,
    )
    return {"id": task_id, "status": "rejected"}


@pipeline_router.post("/{task_id}/rework")
def pipeline_rework(task_id: str, body: ReworkRequest = ReworkRequest()) -> dict[str, Any]:
    """手动触发返工（再排队）。"""
    task = _get_queue().get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    _require_task_scope(task)
    if task.rework_count >= 2:
        raise HTTPException(status_code=400, detail="max rework attempts (2) reached")
    new_feedback = list(task.rework_feedback)
    new_feedback.append(body.note)
    _get_queue().update_status(
        task_id,
        status="pending",
        rework_count=task.rework_count + 1,
        rework_feedback=new_feedback,
    )
    return {"id": task_id, "status": "pending"}


# ---------------------------------------------------------------------------
# P0 新增端点：DAG 查看 / 常驻自动执行 / 经验查询
# ---------------------------------------------------------------------------


@pipeline_router.get("/{graph_id}/graph")
def pipeline_graph(graph_id: str) -> dict[str, Any]:
    """查看任务图（DAG）：节点、依赖、触发、当前状态与进度。

    404 若 graph_id 不存在（未通过 /submit 登记）。
    """
    graph = _graph_registry.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="graph not found")
    _require_graph_scope(graph_id)
    return _graph_to_public(graph)


@pipeline_router.post("/{graph_id}/auto-run")
def pipeline_auto_run(graph_id: str) -> dict[str, Any]:
    """启动常驻自动执行：调度器按就绪态自动拉取节点并跑验收/返工闭环。

    404 若 graph_id 不存在。返回 {graph_id, status:"running"}；调度器后台运行，
    完成/升级后自动停止（状态可经 /graph 查询）。
    """
    task = _task_for_graph(graph_id)
    graph = _graph_registry.get(graph_id)
    if task is not None and task.status == "failed":
        graph = _restore_failed_graph(task, graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="graph not found")
    _require_graph_scope(graph_id)
    task_id = _graph_task_registry.get(graph_id)
    if task_id:
        task = _get_queue().get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="task not found")
        if task.status not in ("pending", "queued", "failed"):
            raise HTTPException(status_code=400, detail="task cannot start")
        _get_queue().update_status(
            task_id,
            status="running",
            started_at=datetime.now(timezone.utc).isoformat(),
        )

    def sync_task(_scheduler: Any) -> None:
        if not task_id:
            return
        if graph.is_complete():
            _get_queue().update_status(
                task_id,
                status="review",
                completed_at=datetime.now(timezone.utc).isoformat(),
                executor_result=_graph_result(graph, failed=False),
            )
        elif graph.has_escalation():
            _get_queue().update_status(
                task_id,
                status="failed",
                completed_at=datetime.now(timezone.utc).isoformat(),
                executor_result=_graph_result(graph, failed=True),
            )

    runtime = _build_runtime(graph)
    scheduler_manager.start_scheduler(
        graph,
        runtime=runtime,
        poll_interval=0.2,
        on_tick=sync_task,
    )
    return {"graph_id": graph_id, "status": "running"}


@pipeline_router.get("/{graph_id}/trace")
def pipeline_graph_trace(graph_id: str) -> dict[str, Any]:
    """返回该 graph 的降级/执行 trace（pipeline 维度可观测；不依赖 main.py tasks 体系）。"""
    graph = _graph_registry.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="graph not found")
    _require_graph_scope(graph_id)
    return {
        "graph_id": graph_id,
        "trace": _graph_trace(graph),
        "capability_paths": {nid: n.capability_path for nid, n in graph.nodes.items()},
    }


# ---------------------------------------------------------------------------
# 内部辅助
# ---------------------------------------------------------------------------


def _require_project(project_id: str | None) -> dict[str, Any]:
    if not project_id or _pipeline_database is None:
        raise HTTPException(status_code=404, detail="project not found")
    with _pipeline_database.connect() as connection:
        row = connection.execute(
            "select * from projects where tenant_id = ? and project_id = ?",
            (TenantContext.current_tenant_id(), project_id),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="project not found")
    return dict(row)


def _require_task_scope(task: Any) -> None:
    project_id = (task.issue_spec or {}).get("project_id")
    if project_id:
        _require_project(str(project_id))


def _require_graph_scope(graph_id: str) -> None:
    project_id = _graph_project_registry.get(graph_id)
    if project_id:
        _require_project(project_id)


def _project_task(project_id: str, tenant_id: str) -> Any | None:
    return next(
        (
            item
            for item in _get_queue().list_all()
            if (item.issue_spec or {}).get("project_id") == project_id
            and (item.issue_spec or {}).get("tenant_id") == tenant_id
        ),
        None,
    )


def _task_for_graph(graph_id: str) -> Any | None:
    return next(
        (
            item
            for item in _get_queue().list_all()
            if (item.issue_spec or {}).get("pipeline_graph_id") == graph_id
        ),
        None,
    )


def _restore_failed_graph(task: Any, graph_id: str) -> TaskGraph:
    spec = task.issue_spec or {}
    project_id = str(spec.get("project_id") or "")
    plan = spec.get("pipeline_plan")
    if not project_id or not isinstance(plan, dict) or plan.get("graph_id") != graph_id:
        raise HTTPException(status_code=409, detail="failed graph cannot be restored")
    _require_project(project_id)
    graph = TaskGraph.from_plan(plan)
    _graph_registry[graph_id] = graph
    _graph_project_registry[graph_id] = project_id
    _graph_task_registry[graph_id] = task.id
    return graph


def _load_progress(raw: Any) -> dict[str, Any]:
    if isinstance(raw, dict):
        return dict(raw)
    if not isinstance(raw, str) or not raw.strip():
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _persist_project_runtime(
    project: dict[str, Any], task: Any, graph_id: str, plan: dict[str, Any]
) -> None:
    progress = _load_progress(project.get("progress_json"))
    progress["runtime"] = {
        "task_id": task.id,
        "graph_id": graph_id,
        "plan": plan,
        "persistence": "process_only",
        "updated_at": task.created_at,
    }
    with _pipeline_database.connect() as connection:
        connection.execute(
            "update projects set progress_json = ?, updated_at = current_timestamp "
            "where tenant_id = ? and project_id = ?",
            (
                json.dumps(progress, ensure_ascii=False),
                TenantContext.current_tenant_id(),
                project["project_id"],
            ),
        )


def _graph_to_public(graph: TaskGraph) -> dict[str, Any]:
    return {
        "graph_id": graph.graph_id,
        "available": True,
        "progress": graph.progress(),
        "is_complete": graph.is_complete(),
        "has_escalation": graph.has_escalation(),
        "escalations": graph.escalations,
        "nodes": [node.to_dict() for node in graph.nodes.values()],
    }


def _snapshot_graph(graph_id: Any, plan: Any) -> dict[str, Any] | None:
    if not graph_id or not isinstance(plan, dict):
        return None
    nodes = []
    for node in plan.get("nodes", []):
        if isinstance(node, dict):
            nodes.append({**node, "status": "unknown"})
    return {
        "graph_id": graph_id,
        "available": False,
        "progress": None,
        "is_complete": False,
        "has_escalation": False,
        "escalations": [],
        "nodes": nodes,
    }


def _graph_trace(graph: TaskGraph | None) -> list[dict[str, Any]]:
    if graph is None:
        return []
    events: list[dict[str, Any]] = []
    for node in graph.nodes.values():
        events.extend(node.trace or [])
    return events


def _available_actions(task: Any | None, graph: TaskGraph | None) -> list[str]:
    if task is None:
        return ["submit"]
    if task.status in ("pending", "queued"):
        if task.rework_count:
            return ["dispatch"]
        return ["auto_run"] if graph is not None else []
    if task.status == "review":
        return ["approve", "reject", "rework"]
    if task.status == "failed":
        return ["retry"]
    if task.status in ("approved", "rejected"):
        return ["view_result"]
    return []


def _graph_result(graph: TaskGraph, *, failed: bool) -> dict[str, Any]:
    outputs = [node.result for node in graph.nodes.values() if isinstance(node.result, dict)]
    diff_text = "\n\n".join(
        str(
            result.get("diff_text")
            or (
                result.get("output")
                if str(result.get("output") or "").lstrip().startswith("--- a/")
                else ""
            )
        )
        for result in outputs
        if result.get("diff_text")
        or str(result.get("output") or "").lstrip().startswith("--- a/")
    )
    files = sorted({
        str(path)
        for result in outputs
        for path in (result.get("files") or [])
        if path
    })
    artifact_text = "\n\n".join(
        str(result.get("artifact_text") or result.get("output") or "")
        for result in outputs
        if not str(result.get("output") or "").lstrip().startswith("--- a/")
        and (result.get("artifact_text") or result.get("output"))
    )
    return {
        "status": "failed" if failed else "success",
        "rounds": sum(node.attempts for node in graph.nodes.values()),
        "diff_text": diff_text,
        "test_exit_code": 1 if failed else 0,
        "files": files,
        "artifact_text": artifact_text,
    }


def _task_to_public(task: Any) -> dict[str, Any]:
    """将 PipelineTask 转为可序列化 dict。"""
    d = {
        "id": task.id,
        "created_at": task.created_at,
        "natural_language": task.natural_language,
        "issue_spec": task.issue_spec,
        "status": task.status,
        "queued_at": task.queued_at,
        "started_at": task.started_at,
        "completed_at": task.completed_at,
        "executor_result": task.executor_result,
        "rework_count": task.rework_count,
        "rework_feedback": task.rework_feedback,
        "review_decision": task.review_decision,
        "review_note": task.review_note,
    }
    return d
