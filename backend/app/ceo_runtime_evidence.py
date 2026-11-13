"""Issue B · CEO Office 真实运行证据（只读聚合层 + 只读 GET 端点）。

本模块是 Issue B 的「真实运行证据」展示层后端：对既有 A 层执行锁 / 会话 /
唤醒请求、B 层治理 pending 决策、C 层预算状态、以及全量 evolution_events
运行时间线做**只读聚合**，并通过 ``register_ceo_evidence_routes`` 注册一组
**只读 GET 端点**供前端（frontend-ceo-office）拉取。

铁律（与实现级设计一致，不可妥协）：
1. **零新依赖**：仅标准库（sqlite3 / json / dataclasses / typing / datetime）
   + 项目既有模块（Database / EvolutionEventLog / PendingDecisionStore /
   A·C 层 store）。不引入任何新包。
2. **只读展示**：本模块**只 SELECT**；对 ``decision_sink`` 仅调用
   ``list_pending()``，**绝不**调用 ``resolve()`` / ``cancel()``；不解除
   人工批准闸，不触发任何解除执行锁的路径。
3. **脱敏贯穿**：所有响应仅含聚合值 / 状态 / 范围键，**无路径 / Key /
   参数 / 原始 Secret**；A 层执行锁返回刻意排除 ``token``；
   ``evolution_events.payload`` 原样透传（既已脱敏）。错误响应仅含固定
   ``failure_code`` + 中文短述，不携路径。
4. **与 A/C 内核 + B 层治理共存**：本模块不修改任何受保护核心；仅新增只读
   端点，不重评 gate、不解除人工批准闸。
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any

from .database import Database
from .decision_sink import PendingDecisionStore, _default_db_path
from .agent_execution_kernel import ExecutionClaimStore, _SELECT_COLUMNS
from .agent_wakeup_session import WakeRequestStore
from .tenant_context import TenantContext


# ---------------------------------------------------------------------------
# 纯函数：运行时间线 status_dimension 映射（由 event_type 末段映射，无副作用）
# ---------------------------------------------------------------------------
_STATUS_DIMENSION_BY_SUFFIX: dict[str, str] = {
    "completed": "completed",
    "failed": "failed",
    "blocked": "blocked",
    "recovered": "recovered",
    "exceeded": "hard_stop",
    "warn": "warn",
    "ok": "completed",
    "allowed": "allowed",
    "cancelled": "cancelled",
    "cancel": "cancelled",
    "pending": "pending",
    "waiting": "waiting",
}

# 事件类别中文短述（前端可读，非技术术语）。
_CATEGORY_LABEL: dict[str, str] = {
    "a.kernel": "Agent 执行",
    "a.budget": "预算护栏",
    "b.governance": "治理拍板",
    "usage": "模型调用",
}


def _map_status_dimension(event_type: str) -> str:
    """由 ``event_type`` 末段纯函数映射到 ``status_dimension``。

    仅用于前端着色，无副作用、无 IO。例如：
    ``a.kernel.session.completed`` → ``completed``；
    ``a.budget.exceeded`` → ``hard_stop``；
    ``b.governance.gate=allowed`` → ``allowed``。
    """
    if not event_type:
        return "completed"
    suffix = event_type.rsplit(".", 1)[-1]
    # 兼容 ``b.governance.gate=allowed`` 这类等号写法。
    suffix = suffix.split("=", 1)[-1]
    return _STATUS_DIMENSION_BY_SUFFIX.get(suffix, "completed")


def _category_of(event_type: str, categories: tuple[str, ...]) -> str:
    """根据前缀判断事件所属类别（a.kernel / a.budget / b.governance / usage）。"""
    for cat in categories:
        if event_type == cat or event_type.startswith(cat + "."):
            return cat
    # 退化：取第一段作为类别。
    return event_type.split(".", 1)[0]


def _timeline_summary(event_type: str, category: str) -> str:
    """事件中文短述（前端可读，非技术术语）。"""
    label = _CATEGORY_LABEL.get(category, "运行")
    suffix = event_type.rsplit(".", 1)[-1].split("=", 1)[-1]
    detail = {
        "completed": "完成",
        "failed": "失败",
        "blocked": "被拦截",
        "recovered": "已恢复",
        "exceeded": "超阈值硬停",
        "warn": "软提醒",
        "ok": "正常",
        "allowed": "已放行",
        "cancelled": "已取消",
        "pending": "待处理",
        "model_call": "模型调用",
    }.get(suffix, "事件")
    return f"{label}·{detail}"


def _desensitized_scope_key(payload: dict[str, Any], correlation_id: str) -> str:
    """从脱敏 payload 推导范围键（无业务原始 id / 路径 / Key）。"""
    scope = (
        payload.get("scope")
        or payload.get("run_id")
        or payload.get("scope_key")
        or payload.get("agent_session_id")
    )
    if scope:
        return f"scope:{scope}"
    if correlation_id:
        return f"scope:{correlation_id[-8:]}"
    return "scope:unknown"


# ---------------------------------------------------------------------------
# B2 · 运行证据 / 时间线
# ---------------------------------------------------------------------------
def build_runtime_timeline(
    database: Database,
    *,
    limit: int = 200,
    since: str | None = None,
    until: str | None = None,
    categories: tuple[str, ...] = ("a.kernel", "a.budget", "b.governance", "usage"),
) -> list[dict[str, Any]]:
    """只读 ``evolution_events``，按 ``event_type`` 前缀过滤，按 ``created_at``
    倒序，投影为时间线条目（脱敏：仅 event_type / 状态维度 / 范围键）。

    纯只读：仅 ``SELECT``，不写任何数据。
    """
    if not categories:
        categories = ("a.kernel", "a.budget", "b.governance", "usage")
    try:
        where_clauses = " OR ".join("event_type LIKE ?" for _ in categories)
        params: list[Any] = [c + ".%" for c in categories]
        if since:
            where_clauses += " AND created_at >= ?"
            params.append(since)
        if until:
            where_clauses += " AND created_at <= ?"
            params.append(until)
        params.append(int(limit))
        sql = (
            "SELECT event_id, event_type, payload, correlation_id, created_at "
            f"FROM evolution_events WHERE ({where_clauses}) "
            "ORDER BY created_at DESC LIMIT ?"
        )
        with database.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        # 表不存在（尚未积累运行事件）→ 返回空时间线（fail-open 读侧）。
        return []

    timeline: list[dict[str, Any]] = []
    for row in rows:
        event_type = row["event_type"]
        try:
            payload = json.loads(row["payload"]) if row["payload"] else {}
        except (json.JSONDecodeError, TypeError):
            payload = {}
        category = _category_of(event_type, categories)
        timeline.append(
            {
                "event_id": row["event_id"],
                "event_type": event_type,
                "category": category,
                "status_dimension": _map_status_dimension(event_type),
                "scope_key": _desensitized_scope_key(payload, row["correlation_id"]),
                "summary": _timeline_summary(event_type, category),
                "created_at": row["created_at"],
            }
        )
    return timeline


# ---------------------------------------------------------------------------
# B3 · 组织树（Company→Department→Employee→Skill/Tool）
# ---------------------------------------------------------------------------
def build_org_tree(database: Database) -> dict[str, Any]:
    """只读 Company→Department→Employee→Skill/Tool 层级。

    Skill/Tool 叶子：优先取 ``employee_capability_bindings``
    （capability_source + capability_type + capability_id），无绑定则回退
    ``employee_templates.default_capability_types_json``。

    纯只读：仅 ``SELECT``。
    """
    tenant_id = TenantContext.current_tenant_id()
    try:
        with database.connect() as conn:
            companies = [
                dict(r)
                for r in conn.execute(
                    "SELECT company_id, tenant_id, name, description, status, "
                    "company_type FROM companies WHERE tenant_id = ? ORDER BY created_at",
                    (tenant_id,),
                ).fetchall()
            ]
            projects = [
                dict(r)
                for r in conn.execute(
                    "SELECT project_id, tenant_id, company_id, name, status, "
                    "owner_employee_id FROM projects WHERE tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
            ]
            departments = [
                dict(r)
                for r in conn.execute(
                    "SELECT id, tenant_id, company_id, name, department_type, "
                    "status FROM department_instances WHERE tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
            ]
            employees = [
                dict(r)
                for r in conn.execute(
                    "SELECT id, tenant_id, company_id, department_id, template_id, "
                    "name, role, status, enabled FROM employee_instances "
                    "WHERE tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
            ]
            bindings = [
                dict(r)
                for r in conn.execute(
                    "SELECT employee_id, capability_source, capability_type, "
                    "capability_id FROM employee_capability_bindings "
                    "WHERE tenant_id = ?",
                    (tenant_id,),
                ).fetchall()
            ]
            templates = {
                row["id"]: row
                for row in conn.execute(
                    "SELECT id, default_capability_types_json FROM employee_templates"
                ).fetchall()
            }
    except sqlite3.OperationalError:
        # 组织相关表尚未初始化 → 返回空树（fail-open 读侧）。
        return {"tenant_id": tenant_id, "companies": []}

    from collections import defaultdict

    projects_by_company = defaultdict(list)
    for p in projects:
        projects_by_company[p["company_id"]].append(p)
    depts_by_company = defaultdict(list)
    for d in departments:
        depts_by_company[d["company_id"]].append(d)
    emp_by_dept = defaultdict(list)
    for e in employees:
        emp_by_dept[e["department_id"]].append(e)
    bindings_by_emp = defaultdict(list)
    for b in bindings:
        bindings_by_emp[b["employee_id"]].append(b)

    company_nodes: list[dict[str, Any]] = []
    for c in companies:
        company_node: dict[str, Any] = {
            "company_id": c["company_id"],
            "name": c["name"],
            "status": c["status"],
            "projects": [
                {
                    "project_id": p["project_id"],
                    "name": p["name"],
                    "status": p["status"],
                    "owner_employee_id": p.get("owner_employee_id", "") or "",
                }
                for p in projects_by_company.get(c["company_id"], [])
            ],
            "departments": [],
        }
        for d in depts_by_company.get(c["company_id"], []):
            dept_node: dict[str, Any] = {
                "id": d["id"],
                "name": d["name"],
                "department_type": d["department_type"],
                "status": d["status"],
                "employees": [],
            }
            for e in emp_by_dept.get(d["id"], []):
                emp_bindings = bindings_by_emp.get(e["id"], [])
                if emp_bindings:
                    skills_tools = [
                        {
                            "kind": b["capability_type"],
                            "ref": b["capability_id"],
                            "source": b["capability_source"],
                        }
                        for b in emp_bindings
                    ]
                else:
                    tpl = templates.get(e["template_id"], {})
                    try:
                        cap_types = json.loads(
                            tpl.get("default_capability_types_json", "[]") or "[]"
                        )
                    except (json.JSONDecodeError, TypeError):
                        cap_types = []
                    skills_tools = [
                        {"kind": "capability", "ref": ct}
                        for ct in cap_types
                        if ct
                    ]
                dept_node["employees"].append(
                    {
                        "id": e["id"],
                        "name": e["name"],
                        "role": e["role"],
                        "status": e["status"],
                        "skills_tools": skills_tools,
                    }
                )
            company_node["departments"].append(dept_node)
        company_nodes.append(company_node)

    return {"tenant_id": tenant_id, "companies": company_nodes}


# ---------------------------------------------------------------------------
# B4 · B 层治理 pending 决策（只读展示，不审批、不修改）
# ---------------------------------------------------------------------------
def _deserialize_gate_snapshot(gate_snapshot: str) -> dict[str, Any]:
    """反序列化脱敏后的 GatePrompt JSON 快照为前端可读结构。

    ``gate_snapshot`` 已是 ``render_gate_prompt`` 脱敏后的 GatePrompt JSON
    （禁词红线已在 B 层 enforcement），无路径 / Key / 参数。
    """
    try:
        snap = json.loads(gate_snapshot) if gate_snapshot else {}
    except (json.JSONDecodeError, TypeError):
        snap = {}
    options = snap.get("options", []) or []
    option_list = [
        {"id": o.get("id", ""), "label": o.get("label", ""), "effect": o.get("effect", "")}
        for o in options
        if isinstance(o, dict)
    ]
    awaiting = "/".join(
        o["id"] for o in option_list if o.get("id")
    ) or "—"
    return {
        "title": snap.get("title", ""),
        "business_risk": snap.get("business_risk", ""),
        "options": option_list,
        "recommended": snap.get("recommended", ""),
        "one_line_consequence": snap.get("one_line_consequence", ""),
        "awaiting_letter": awaiting,
    }


def build_pending_decisions(store: PendingDecisionStore) -> list[dict[str, Any]]:
    """只读 ``PendingDecisionStore.list_pending()`` 读出待拍板决策。

    仅调用读方法 ``list_pending()``，**绝不**调用 ``resolve()`` / ``cancel()``
    （审批属未来 Workspace resolver，越 B 边界）。反序列化脱敏 ``gate_snapshot``
    为前端可读结构。
    """
    records = store.list_pending()
    decisions: list[dict[str, Any]] = []
    for rec in records:
        gate = _deserialize_gate_snapshot(getattr(rec, "gate_snapshot", "") or "")
        decisions.append(
            {
                "pending_id": rec.pending_id,
                "gate_label": rec.gate_label,
                "category": rec.category,
                "title": gate["title"],
                "business_risk": gate["business_risk"],
                "options": gate["options"],
                "recommended": gate["recommended"],
                "one_line_consequence": gate["one_line_consequence"],
                "status": rec.status,
                "awaiting_letter": gate["awaiting_letter"],
                "created_at": rec.created_at,
                "expires_at": rec.expires_at,
            }
        )
    return decisions


# ---------------------------------------------------------------------------
# B5 · 执行状态（A 层可视化：执行锁 / 会话 / 唤醒请求，脱敏无 token）
# ---------------------------------------------------------------------------
def build_execution_status(database: Database) -> dict[str, Any]:
    """只读 A 层 store：执行锁（claims）/ 会话（sessions）/ 唤醒合并
    （wake_requests）。沿用 ``_SELECT_COLUMNS``（排除 ``token``）。

    纯只读：仅 ``SELECT``；不解除人工批准闸。
    """
    # 执行锁：复用 A 层 ExecutionClaimStore.list_active（返回记录不含 token）。
    try:
        claim_records = ExecutionClaimStore(database).list_active()
        claims = [asdict(c) for c in claim_records]
    except Exception:  # noqa: BLE001 - 读侧异常不阻断其它聚合
        claims = []

    # 会话：A 层 AgentTaskSessionStore 未暴露 list_all，这里按脱敏列只读 SELECT
    # （刻意排除 checkpoint / config_fingerprint 等大体积内部字段，无 token）。
    _SESSION_COLUMNS = (
        "session_id, scope, agent_id, task_id, status, started_at, "
        "last_active_at, expires_at, tenant_id, correlation_id"
    )
    try:
        with database.connect() as conn:
            session_rows = conn.execute(
                f"SELECT {_SESSION_COLUMNS} FROM agent_task_sessions "
                "ORDER BY created_at DESC"
            ).fetchall()
        sessions = [dict(r) for r in session_rows]
    except Exception:  # noqa: BLE001
        sessions = []

    # 唤醒请求：复用 A 层 WakeRequestStore.list_pending。
    try:
        wake_records = WakeRequestStore(database).list_pending()
        wake_requests = [
            {
                "request_id": w.request_id,
                "scope": w.scope,
                "agent_id": w.agent_id,
                "task_id": w.task_id,
                "status": w.status,
                "coalesced_count": int(getattr(w, "coalesced_count", 1) or 1),
                "created_at": getattr(w, "created_at", ""),
                "expires_at": getattr(w, "expires_at", ""),
            }
            for w in wake_records
        ]
    except Exception:  # noqa: BLE001
        wake_requests = []

    return {
        "claims": claims,
        "sessions": sessions,
        "wake_requests": wake_requests,
    }


# ---------------------------------------------------------------------------
# B6 · 预算状态（C 层可视化：a.budget.* 事件 + 可选累加器，脱敏）
# ---------------------------------------------------------------------------
def build_budget_status(database: Database) -> dict[str, Any]:
    """聚合 ``a.budget.ok/warn/exceeded`` 事件计数与最近硬停；可选地只读
    ``budget_guard_accumulators`` 累加表。

    纯只读：仅 ``SELECT``；无价格 / 成本数值（仅 token 维度）。
    """
    tenant_id = TenantContext.current_tenant_id()
    totals = {"ok": 0, "warn": 0, "exceeded": 0}
    recent_exceeded: list[dict[str, Any]] = []
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT event_id, event_type, payload, created_at FROM evolution_events "
                "WHERE tenant_id = ? AND event_type IN "
                "('a.budget.ok', 'a.budget.warn', 'a.budget.exceeded') "
                "ORDER BY created_at DESC",
                (tenant_id,),
            ).fetchall()
        for row in rows:
            try:
                payload = json.loads(row["payload"]) if row["payload"] else {}
            except (json.JSONDecodeError, TypeError):
                payload = {}
            et = row["event_type"]
            if et == "a.budget.ok":
                totals["ok"] += 1
            elif et == "a.budget.warn":
                totals["warn"] += 1
            elif et == "a.budget.exceeded":
                totals["exceeded"] += 1
                recent_exceeded.append(
                    {
                        "event_id": row["event_id"],
                        "scope": payload.get("scope", "") or "",
                        "ratio": float(payload.get("ratio", 0) or 0),
                        "limit": int(payload.get("limit", 0) or 0),
                        "created_at": row["created_at"],
                    }
                )
    except sqlite3.OperationalError:
        # 尚无预算事件 → 返回空聚合（fail-open 读侧）。
        pass

    # 可选累加器（per_agent_session 跨进程耐久表，若不存在则跳过）。
    accumulators: list[dict[str, Any]] = []
    try:
        with database.connect() as conn:
            acc_rows = conn.execute(
                "SELECT acc_key, scope, accumulated_tokens, updated_at "
                "FROM budget_guard_accumulators"
            ).fetchall()
        for row in acc_rows:
            accumulators.append(
                {
                    "scope": row["scope"] or "",
                    "acc_key": row["acc_key"],
                    "accumulated_tokens": int(row["accumulated_tokens"] or 0),
                    "updated_at": row["updated_at"] or "",
                }
            )
    except sqlite3.OperationalError:
        # 累加表未启用 → 跳过（可选）。
        accumulators = []

    return {
        "totals": totals,
        "recent_exceeded": recent_exceeded[:20],
        "accumulators": accumulators,
    }


# ---------------------------------------------------------------------------
# 路由注册（B 端点归 Issue B）
# ---------------------------------------------------------------------------
def _error_response(failure_code: str, message: str):
    """结构化的脱敏错误响应：仅固定 failure_code + 中文短述，不携路径。"""
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=500,
        content={"error": {"failure_code": failure_code, "message": message}},
    )


def register_ceo_evidence_routes(app, database: Database) -> None:
    """在 ``main.py`` 的 ``create_app`` 内调用一次，注册 B1–B6 的全部只读 GET 端点。

    每个端点内部仅调用对应 ``build_*`` 只读聚合函数；异常隔离（返回结构化脱敏
    错误，不抛裸路径）。全部为 GET、只读、不解除人工批准闸。
    """
    from fastapi import Query

    @app.get("/api/ceo/runtime-timeline")
    def ceo_runtime_timeline(
        limit: int = 200,
        since: str | None = None,
        until: str | None = None,
        categories: list[str] | None = Query(default=None),
    ):
        try:
            cats = (
                tuple(categories)
                if categories
                else ("a.kernel", "a.budget", "b.governance", "usage")
            )
            timeline = build_runtime_timeline(
                database, limit=limit, since=since, until=until, categories=cats
            )
            return {
                "tenant_id": TenantContext.current_tenant_id(),
                "timeline": timeline,
            }
        except Exception:  # noqa: BLE001 - 异常隔离，返回脱敏错误
            return _error_response(
                "runtime_timeline_unavailable", "运行时间线暂时无法读取"
            )

    @app.get("/api/ceo/org-tree")
    def ceo_org_tree():
        try:
            return build_org_tree(database)
        except Exception:  # noqa: BLE001
            return _error_response("org_tree_unavailable", "组织树暂时无法读取")

    @app.get("/api/ceo/pending-decisions")
    def ceo_pending_decisions():
        try:
            # 仅读：构造 store 后只调用 list_pending()，不调用 resolve/cancel。
            store = PendingDecisionStore(_default_db_path())
            decisions = build_pending_decisions(store)
            return {"pending_count": len(decisions), "decisions": decisions}
        except Exception:  # noqa: BLE001
            return _error_response(
                "pending_decisions_unavailable", "治理待办暂时无法读取"
            )

    @app.get("/api/ceo/execution-status")
    def ceo_execution_status():
        try:
            return build_execution_status(database)
        except Exception:  # noqa: BLE001
            return _error_response(
                "execution_status_unavailable", "执行状态暂时无法读取"
            )

    @app.get("/api/ceo/budget-status")
    def ceo_budget_status():
        try:
            return build_budget_status(database)
        except Exception:  # noqa: BLE001
            return _error_response(
                "budget_status_unavailable", "预算状态暂时无法读取"
            )


__all__ = [
    "build_runtime_timeline",
    "build_org_tree",
    "build_pending_decisions",
    "build_execution_status",
    "build_budget_status",
    "register_ceo_evidence_routes",
]
