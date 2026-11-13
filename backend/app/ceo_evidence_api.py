"""Issue B · CEO Office 真实运行证据（只读聚合层 + 只读 GET 端点）。

本模块是 Issue B 的「真实运行证据」展示层后端：对既有 A 层执行锁 / 会话 /
唤醒请求、B 层治理 pending 决策、C 层预算状态、以及全量 evolution_events
运行时间线做 **只读聚合**，并通过 ``ceo_evidence_router``（FastAPI ``APIRouter``）
注册一组 **只读 GET 端点** 供前端拉取。

路由前缀统一 ``/api/ceo/evidence/*``，与既有 ``/api/ceo/overview`` 并存不冲突。

铁律（与实现级设计一致，不可妥协）：
1. **零新依赖**：仅标准库（sqlite3 / json / dataclasses / typing / datetime）
   + 项目既有模块（Database / PendingDecisionStore / A·C 层 store）。不引入任何新包。
2. **只读展示**：本模块 **只 SELECT**；对 ``decision_sink`` 仅调用
   ``list_pending()``，**绝不** 调用 ``resolve()`` / ``cancel()``；不解除
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
import os
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query

from .database import Database
from .decision_sink import PendingDecisionStore
from .tenant_context import TenantContext


# ---------------------------------------------------------------------------
# 投影 DTO（标准库 dataclass，不引 pydantic）
# ---------------------------------------------------------------------------

@dataclass
class CeoOverviewDTO:
    """CEO 运行态势概览：聚合计数 + 最近活动 + 分层状态摘要。"""
    tenant_id: str
    generated_at: str                       # ISO UTC
    counts: dict                            # {departments, employees, workflows,
                                            #  active_execution_claims, active_sessions,
                                            #  pending_wake_requests, pending_decisions,
                                            #  budget_accumulators}
    recent_activity: list[dict]             # 最近 N 条脱敏 TimelineEventDTO 字典
    layer_status: dict                      # A 层锁/会话、C 层预算、B 层待拍板 汇总


@dataclass
class TimelineEventDTO:
    """运行时间线事件条目（脱敏：仅范围键 + 状态维度）。"""
    event_id: int
    created_at: str                         # ISO UTC，排序键
    event_type: str                         # 如 a.kernel.claim.acquired
    layer: str                              # a.kernel | a.budget | b.governance | usage | other
    scope: str                              # 脱敏范围键（correlation_id / run_id 前缀）
    status_dimension: str                   # ok | waiting | blocked | failed | recovered
    digest: dict                            # 脱敏聚合（仅状态/计数/范围键）


@dataclass
class OrgNodeDTO:
    """组织树节点（company → department → employee → skill/tool）。"""
    node_id: str
    kind: str                               # company | department | employee | skill | tool
    label: str
    status: str = ""
    meta: dict = field(default_factory=dict)
    children: list[dict] = field(default_factory=list)


@dataclass
class PendingDecisionDTO:
    """待拍板决策条目（只读投影，无审批操作）。"""
    pending_id: str
    gate_id: str
    category: str                           # money|data|reputation|irreversible|external
    gate_label: str                         # 如 G1-deploy / G4-token
    status: str                             # pending | resolved | cancelled
    decision: str                           # "" | A | B | C | D
    created_at: str
    expires_at: str
    resolved_at: str | None
    title: str                              # 来自脱敏 gate_snapshot
    business_risk: str                      # 来自脱敏 gate_snapshot
    recommended_option: str                 # A | B | C | D（来自脱敏 gate_snapshot）
    awaiting_letter: str                    # pending 时恒为待 A/B/C/D 拍板


@dataclass
class ExecutionStatusDTO:
    """A 层执行可视化：持有锁 / 活跃会话 / 待处理唤醒请求。"""
    held_claims: int
    active_sessions: int
    pending_wake_requests: int
    claims_sample: list[dict]              # 脱敏（scope/owner/reason/status，无 token）
    sessions_sample: list[dict]            # 脱敏（scope/agent_id/task_id/status）


@dataclass
class BudgetStatusDTO:
    """C 层预算可视化：累加器 + 最近预算事件 + guard 开关。"""
    accumulators: list[dict]               # {scope, accumulated_tokens, updated_at}
    recent_events: list[dict]              # 最近 a.budget.* 事件（TimelineEventDTO 风格）
    guard_enabled: bool                    # 来自 budget_guard_config（只读读取）


# ---------------------------------------------------------------------------
# APIRouter
# ---------------------------------------------------------------------------

ceo_evidence_router = APIRouter(prefix="/api/ceo/evidence", tags=["ceo-evidence"])


# ---------------------------------------------------------------------------
# 纯函数：时间线辅助
# ---------------------------------------------------------------------------

_STATUS_DIMENSION_BY_SUFFIX: dict[str, str] = {
    "completed": "ok",
    "resolved": "ok",
    "created": "waiting",
    "pending": "waiting",
    "claimed": "waiting",
    "blocked": "blocked",
    "failed": "failed",
    "exceeded": "failed",
    "recovered": "recovered",
    "recover": "recovered",
    "ok": "ok",
    "warn": "waiting",
}

_CATEGORY_PREFIXES = ("a.kernel", "a.budget", "b.governance", "usage")


def _map_status_dimension(event_type: str) -> str:
    """由 ``event_type`` 末段映射到 ``status_dimension``（纯函数）。

    §7.2 映射表：``*.*.completed`` / ``*.resolved`` → ``ok``；
    ``*.created`` / ``*.pending`` / ``*.claimed`` → ``waiting``；
    ``b.governance.gate`` / ``*.blocked`` → ``blocked``；
    ``*.failed`` / ``budget_exceeded`` / ``a.budget.exceeded`` → ``failed``；
    ``*.recovered`` / ``*.recover`` → ``recovered``。
    未知模式默认 ``waiting``（fail-open 读取侧，仅影响着色）。
    """
    if not event_type:
        return "waiting"
    suffix = event_type.rsplit(".", 1)[-1]
    return _STATUS_DIMENSION_BY_SUFFIX.get(suffix, "waiting")


def _categorize_layer(event_type: str) -> str:
    """根据前缀判断事件所属 layer。"""
    for prefix in _CATEGORY_PREFIXES:
        if event_type == prefix or event_type.startswith(prefix + "."):
            return prefix
    return "other"


def _desensitize_digest(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    """从 payload 提取脱敏聚合值（仅状态/计数/范围键，无路径/Key/参数）。"""
    digest: dict[str, Any] = {}
    scope = payload.get("scope") or payload.get("run_id") or payload.get("scope_key")
    if scope:
        digest["scope"] = str(scope)[:64]
    ratio = payload.get("ratio")
    if ratio is not None:
        try:
            digest["ratio"] = float(ratio)
        except (ValueError, TypeError):
            pass
    limit = payload.get("limit")
    if limit is not None:
        try:
            digest["limit"] = int(limit)
        except (ValueError, TypeError):
            pass
    status = payload.get("status")
    if status:
        digest["status"] = str(status)
    return digest


# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ceo_evidence_api_config.json")
_DEFAULT_CONFIG: dict[str, Any] = {
    "enabled": True,
    "timeline_default_limit": 200,
    "timeline_max_limit": 1000,
    "org_tree_include_skills": True,
    "org_tree_include_tools": True,
    "pending_include_resolved_recent_days": 7,
}


def _load_config() -> dict[str, Any]:
    """读取 ``ceo_evidence_api_config.json``；缺省走 ``_DEFAULT_CONFIG``。

    加载失败 → 回退默认（只读配置，fail-open 不影响运行）。
    """
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            merged = dict(_DEFAULT_CONFIG)
            merged.update({k: v for k, v in data.items() if k in _DEFAULT_CONFIG})
            return merged
    except Exception:  # noqa: BLE001 - 缺省文件/非法 JSON → 默认
        pass
    return dict(_DEFAULT_CONFIG)


# ---------------------------------------------------------------------------
# pending 决策库路径（与 decision_sink._default_db_path() 同约定）
# ---------------------------------------------------------------------------

def _pending_db_path() -> str:
    """仓库根 ``data/b_layer_pending_decisions.sqlite``。"""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(repo_root, "data", "b_layer_pending_decisions.sqlite")


# ---------------------------------------------------------------------------
# B2 · 概览聚合
# ---------------------------------------------------------------------------

def _build_overview_counts(database: Database) -> dict[str, Any]:
    """只读 SELECT 聚合全量计数（复用既有 ``/api/ceo/overview`` 同表）。"""
    tenant_id = TenantContext.current_tenant_id()
    counts: dict[str, Any] = {
        "companies": 0,
        "departments": 0,
        "employees": 0,
        "projects": 0,
        "workflows": 0,
        "active_execution_claims": 0,
        "active_sessions": 0,
        "pending_wake_requests": 0,
        "pending_decisions": 0,
        "budget_accumulators": 0,
    }
    try:
        with database.connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM companies WHERE tenant_id = ?",
                (tenant_id,),
            ).fetchone()
            if row:
                counts["companies"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM department_instances WHERE tenant_id = ?",
                (tenant_id,),
            ).fetchone()
            if row:
                counts["departments"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM employee_instances WHERE tenant_id = ?",
                (tenant_id,),
            ).fetchone()
            if row:
                counts["employees"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM projects WHERE tenant_id = ?",
                (tenant_id,),
            ).fetchone()
            if row:
                counts["projects"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM workflow_instances WHERE tenant_id = ?",
                (tenant_id,),
            ).fetchone()
            if row:
                counts["workflows"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM agent_execution_claims "
                "WHERE status = 'held' AND expires_at > ?",
                (datetime.now(timezone.utc).isoformat(),),
            ).fetchone()
            if row:
                counts["active_execution_claims"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM agent_task_sessions "
                "WHERE status IN ('pending', 'running', 'recovered')",
            ).fetchone()
            if row:
                counts["active_sessions"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM agent_wakeup_requests WHERE status = 'pending'",
            ).fetchone()
            if row:
                counts["pending_wake_requests"] = row[0]

            row = conn.execute(
                "SELECT COUNT(*) FROM budget_guard_accumulators",
            ).fetchone()
            if row:
                counts["budget_accumulators"] = row[0]
    except sqlite3.OperationalError:
        pass  # 表尚未初始化 → 返回零值（fail-open 读侧）

    # pending_decisions 计数：读取独立 pending 库
    try:
        store = PendingDecisionStore(_pending_db_path())
        pending = store.list_pending()
        counts["pending_decisions"] = len(pending)
    except Exception:  # noqa: BLE001
        counts["pending_decisions"] = 0

    return counts


def _build_recent_activity(database: Database, limit: int = 20) -> list[dict]:
    """取最近 N 条脱敏时间线事件。"""
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT event_id, event_type, payload, correlation_id, created_at "
                "FROM evolution_events ORDER BY created_at DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
    except sqlite3.OperationalError:
        return []

    result: list[dict] = []
    for row in rows:
        try:
            payload = json.loads(row["payload"]) if row["payload"] else {}
        except (json.JSONDecodeError, TypeError):
            payload = {}
        layer = _categorize_layer(row["event_type"])
        event = {
            "event_id": row["event_id"],
            "created_at": row["created_at"],
            "event_type": row["event_type"],
            "layer": layer,
            "scope": str(row["correlation_id"] or "")[-12:] or "unknown",
            "status_dimension": _map_status_dimension(row["event_type"]),
            "digest": _desensitize_digest(payload, row["event_type"]),
        }
        result.append(event)
    return result


# ---------------------------------------------------------------------------
# B3 · 时间线
# ---------------------------------------------------------------------------

def _build_timeline(
    database: Database,
    *,
    layer: str = "all",
    since: str | None = None,
    until: str | None = None,
    limit: int = 200,
    status_dimension: str | None = None,
) -> list[dict]:
    """只读 ``evolution_events``，按 ``created_at`` 倒序，脱敏投影。

    支持 ``layer`` / ``since`` / ``until`` / ``limit`` / ``status_dimension`` 过滤。
    """
    clauses: list[str] = []
    params: list[Any] = []

    if layer and layer != "all":
        if layer == "a.kernel":
            clauses.append("event_type LIKE 'a.kernel.%'")
        elif layer == "a.budget":
            clauses.append("event_type LIKE 'a.budget.%'")
        elif layer == "b.governance":
            clauses.append("event_type LIKE 'b.governance.%'")
        elif layer == "usage":
            clauses.append("event_type LIKE 'usage.%'")
        else:
            clauses.append(
                "(event_type NOT LIKE 'a.kernel.%' AND event_type NOT LIKE 'a.budget.%' "
                "AND event_type NOT LIKE 'b.governance.%' AND event_type NOT LIKE 'usage.%')"
            )

    if since:
        clauses.append("created_at >= ?")
        params.append(since)
    if until:
        clauses.append("created_at <= ?")
        params.append(until)

    where_sql = " AND ".join(clauses) if clauses else "1=1"

    try:
        with database.connect() as conn:
            rows = conn.execute(
                f"SELECT event_id, event_type, payload, correlation_id, created_at "
                f"FROM evolution_events WHERE {where_sql} "
                f"ORDER BY created_at DESC LIMIT ?",
                params + [int(limit)],
            ).fetchall()
    except sqlite3.OperationalError:
        return []

    result: list[dict] = []
    for row in rows:
        try:
            payload = json.loads(row["payload"]) if row["payload"] else {}
        except (json.JSONDecodeError, TypeError):
            payload = {}
        sd = _map_status_dimension(row["event_type"])
        # status_dimension 过滤（在映射后过滤，因为数据库没有此列）
        if status_dimension and sd != status_dimension:
            continue
        layer_val = _categorize_layer(row["event_type"])
        event = {
            "event_id": row["event_id"],
            "created_at": row["created_at"],
            "event_type": row["event_type"],
            "layer": layer_val,
            "scope": str(row["correlation_id"] or "")[-12:] or "unknown",
            "status_dimension": sd,
            "digest": _desensitize_digest(payload, row["event_type"]),
        }
        result.append(event)
    return result


# ---------------------------------------------------------------------------
# B4 · 组织树
# ---------------------------------------------------------------------------

def _build_org_tree(
    database: Database,
    *,
    include_skills: bool = True,
    include_tools: bool = True,
) -> dict:
    """只读 Company→Department→Employee→Skill/Tool 层级。

    源：``department_instances`` / ``employee_instances`` /
    ``employee_skill_bindings`` JOIN ``skills`` /
    ``employee_capability_bindings`` JOIN ``tools``。
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
            departments = [
                dict(r)
                for r in conn.execute(
                    "SELECT id, tenant_id, name, department_type, status "
                    "FROM department_instances WHERE tenant_id = ? ORDER BY name",
                    (tenant_id,),
                ).fetchall()
            ]
            employees = [
                dict(r)
                for r in conn.execute(
                    "SELECT id, tenant_id, department_id, name, role, status, enabled "
                    "FROM employee_instances WHERE tenant_id = ? ORDER BY role, name",
                    (tenant_id,),
                ).fetchall()
            ]
            skill_bindings: list[dict] = []
            if include_skills:
                skill_bindings = [
                    dict(r)
                    for r in conn.execute(
                        "SELECT esb.employee_id, s.name, esb.status "
                        "FROM employee_skill_bindings esb "
                        "JOIN skills s ON esb.skill_id = s.skill_id "
                        "WHERE esb.tenant_id = ?",
                        (tenant_id,),
                    ).fetchall()
                ]
            tool_bindings: list[dict] = []
            if include_tools:
                tool_bindings = [
                    dict(r)
                    for r in conn.execute(
                        "SELECT ecb.employee_id, t.name, ecb.status, t.type "
                        "FROM employee_capability_bindings ecb "
                        "JOIN tools t ON ecb.capability_id = t.name "
                        "WHERE ecb.tenant_id = ?",
                        (tenant_id,),
                    ).fetchall()
                ]
    except sqlite3.OperationalError:
        return {
            "tenant_id": tenant_id,
            "node_id": "root",
            "kind": "company",
            "label": "组织",
            "children": [],
        }

    # 构建树
    from collections import defaultdict

    emp_by_dept: dict[str, list[dict]] = defaultdict(list)
    for e in employees:
        emp_by_dept[e.get("department_id", "")].append(e)

    skills_by_emp: dict[str, list[dict]] = defaultdict(list)
    for sb in skill_bindings:
        skills_by_emp[sb["employee_id"]].append(sb)

    tools_by_emp: dict[str, list[dict]] = defaultdict(list)
    for tb in tool_bindings:
        tools_by_emp[tb["employee_id"]].append(tb)

    company_nodes: list[dict] = []
    for c in companies:
        dept_nodes: list[dict] = []
        for d in departments:
            emp_nodes: list[dict] = []
            for e in emp_by_dept.get(d["id"], []):
                children: list[dict] = []
                for sb in skills_by_emp.get(e["id"], []):
                    children.append({
                        "node_id": f"skill_{sb['name']}",
                        "kind": "skill",
                        "label": sb.get("name", ""),
                        "status": sb.get("status", "active"),
                        "meta": {},
                        "children": [],
                    })
                for tb in tools_by_emp.get(e["id"], []):
                    children.append({
                        "node_id": f"tool_{tb['name']}",
                        "kind": "tool",
                        "label": tb.get("name", ""),
                        "status": tb.get("status", "active"),
                        "meta": {"type": tb.get("type", "")},
                        "children": [],
                    })
                emp_nodes.append({
                    "node_id": e["id"],
                    "kind": "employee",
                    "label": e.get("name", ""),
                    "status": e.get("status", ""),
                    "meta": {"role": e.get("role", "")},
                    "children": children,
                })
            dept_nodes.append({
                "node_id": d["id"],
                "kind": "department",
                "label": d.get("name", ""),
                "status": d.get("status", ""),
                "meta": {"department_type": d.get("department_type", "")},
                "children": emp_nodes,
            })
        company_nodes.append({
            "node_id": c["company_id"],
            "kind": "company",
            "label": c.get("name", ""),
            "status": c.get("status", ""),
            "meta": {},
            "children": dept_nodes,
        })

    return {
        "tenant_id": tenant_id,
        "node_id": "root",
        "kind": "company",
        "label": "组织",
        "children": company_nodes,
    }


# ---------------------------------------------------------------------------
# B5 · 待拍板决策
# ---------------------------------------------------------------------------

def _build_pending_decisions(
    store: PendingDecisionStore,
    status_filter: str = "all",
    limit: int = 100,
) -> list[dict]:
    """只读 pending 决策，投影 ``PendingDecisionDTO``。

    pending 经 ``store.list_pending()``；
    ``gate_snapshot`` 已脱敏，仅投影 title/business_risk/recommended。
    """
    try:
        records = store.list_pending()
    except Exception:  # noqa: BLE001
        records = []

    # 如果要求 resolved/cancelled，从独立库 SELECT 历史记录
    extra_records: list[Any] = []
    if status_filter in ("all", "resolved", "cancelled"):
        try:
            db_path = _pending_db_path()
            with sqlite3.connect(db_path) as conn:
                clauses = []
                params: list[Any] = []
                if status_filter != "all":
                    clauses.append("status = ?")
                    params.append(status_filter)
                where = " AND ".join(clauses) if clauses else "1=1"
                rows = conn.execute(
                    f"SELECT pending_id, gate_id, category, gate_snapshot, status, "
                    f"decision, correlation_id, gate_label, created_at, expires_at, "
                    f"resolved_at FROM b_layer_pending_decisions "
                    f"WHERE {where} ORDER BY created_at DESC LIMIT ?",
                    params + [int(limit)],
                ).fetchall()
                for row in rows:
                    extra_records.append(row)
        except Exception:  # noqa: BLE001
            pass

    # 合并 pending + 历史
    all_decisions: list[dict] = []
    seen_ids: set[str] = set()

    for rec in records:
        pending_id = getattr(rec, "pending_id", "")
        seen_ids.add(pending_id)
        gate_snapshot_str = getattr(rec, "gate_snapshot", "") or "{}"
        try:
            snap = json.loads(gate_snapshot_str)
        except (json.JSONDecodeError, TypeError):
            snap = {}
        options = snap.get("options", []) or []
        option_ids = "/".join(
            o.get("id", "") for o in options if isinstance(o, dict) and o.get("id")
        )
        all_decisions.append({
            "pending_id": pending_id,
            "gate_id": getattr(rec, "gate_id", ""),
            "category": getattr(rec, "category", ""),
            "gate_label": getattr(rec, "gate_label", ""),
            "status": getattr(rec, "status", "pending"),
            "decision": getattr(rec, "decision", ""),
            "created_at": getattr(rec, "created_at", ""),
            "expires_at": getattr(rec, "expires_at", ""),
            "resolved_at": getattr(rec, "resolved_at", None),
            "title": snap.get("title", ""),
            "business_risk": snap.get("business_risk", ""),
            "recommended_option": snap.get("recommended", ""),
            "awaiting_letter": option_ids or "待 A/B/C/D 拍板",
        })

    for row in extra_records:
        pid = row[0] if isinstance(row, (list, tuple)) else row["pending_id"]
        if pid in seen_ids:
            continue
        seen_ids.add(pid)
        gate_snapshot_str = row[3] if isinstance(row, (list, tuple)) else row["gate_snapshot"]
        try:
            snap = json.loads(gate_snapshot_str) if gate_snapshot_str else {}
        except (json.JSONDecodeError, TypeError):
            snap = {}
        options = snap.get("options", []) or []
        option_ids = "/".join(
            o.get("id", "") for o in options if isinstance(o, dict) and o.get("id")
        )
        all_decisions.append({
            "pending_id": pid,
            "gate_id": row[1] if isinstance(row, (list, tuple)) else row["gate_id"],
            "category": row[2] if isinstance(row, (list, tuple)) else row["category"],
            "gate_label": row[7] if isinstance(row, (list, tuple)) else row.get("gate_label", ""),
            "status": row[4] if isinstance(row, (list, tuple)) else row["status"],
            "decision": row[5] if isinstance(row, (list, tuple)) else row["decision"],
            "created_at": row[8] if isinstance(row, (list, tuple)) else row["created_at"],
            "expires_at": row[9] if isinstance(row, (list, tuple)) else row["expires_at"],
            "resolved_at": row[10] if isinstance(row, (list, tuple)) else row.get("resolved_at"),
            "title": snap.get("title", ""),
            "business_risk": snap.get("business_risk", ""),
            "recommended_option": snap.get("recommended", ""),
            "awaiting_letter": option_ids or "—",
        })

    # 按 status 过滤
    if status_filter != "all":
        all_decisions = [d for d in all_decisions if d["status"] == status_filter]

    return all_decisions[:int(limit)]


# ---------------------------------------------------------------------------
# B6 · 执行状态（A 层可视化）
# ---------------------------------------------------------------------------

def _build_execution_status(database: Database) -> dict:
    """只读 A 层：执行锁 / 会话 / 唤醒请求（脱敏无 token）。"""
    result: dict[str, Any] = {
        "held_claims": 0,
        "active_sessions": 0,
        "pending_wake_requests": 0,
        "claims_sample": [],
        "sessions_sample": [],
    }

    # 执行锁计数 + 样本
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT claim_id, scope, owner, reason, status, "
                "acquired_at, expires_at, last_heartbeat_at, "
                "heartbeat_interval_seconds, tenant_id, correlation_id "
                "FROM agent_execution_claims "
                "WHERE status = 'held' AND expires_at > ? "
                "ORDER BY acquired_at DESC",
                (datetime.now(timezone.utc).isoformat(),),
            ).fetchall()
        result["held_claims"] = len(rows)
        result["claims_sample"] = [
            {
                "claim_id": r["claim_id"],
                "scope": r["scope"],
                "owner": r["owner"],
                "reason": r["reason"],
                "status": r["status"],
                "acquired_at": r["acquired_at"],
                "expires_at": r["expires_at"],
            }
            for r in rows[:20]
        ]
    except sqlite3.OperationalError:
        pass

    # 活跃会话计数 + 样本
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT session_id, scope, agent_id, task_id, status, "
                "started_at, last_active_at, expires_at "
                "FROM agent_task_sessions "
                "WHERE status IN ('pending', 'running', 'recovered') "
                "ORDER BY created_at DESC"
            ).fetchall()
        result["active_sessions"] = len(rows)
        result["sessions_sample"] = [
            {
                "session_id": r["session_id"],
                "scope": r["scope"],
                "agent_id": r["agent_id"],
                "task_id": r["task_id"],
                "status": r["status"],
                "started_at": r["started_at"],
            }
            for r in rows[:20]
        ]
    except sqlite3.OperationalError:
        pass

    # 待处理唤醒请求
    try:
        with database.connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM agent_wakeup_requests WHERE status = 'pending'",
            ).fetchone()
            if row:
                result["pending_wake_requests"] = row[0]
    except sqlite3.OperationalError:
        pass

    return result


# ---------------------------------------------------------------------------
# B7 · 预算状态（C 层可视化）
# ---------------------------------------------------------------------------

def _build_budget_status(database: Database) -> dict:
    """只读 C 层：累加器 + 最近事件 + guard 开关。"""
    result: dict[str, Any] = {
        "accumulators": [],
        "recent_events": [],
        "guard_enabled": False,
    }

    # 累加器
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT scope, accumulated_tokens, updated_at "
                "FROM budget_guard_accumulators"
            ).fetchall()
        result["accumulators"] = [
            {
                "scope": r["scope"],
                "accumulated_tokens": int(r["accumulated_tokens"] or 0),
                "updated_at": r["updated_at"] or "",
            }
            for r in rows
        ]
    except sqlite3.OperationalError:
        pass

    # 最近 a.budget.* 事件
    try:
        with database.connect() as conn:
            rows = conn.execute(
                "SELECT event_id, event_type, payload, correlation_id, created_at "
                "FROM evolution_events "
                "WHERE event_type IN ('a.budget.ok', 'a.budget.warn', 'a.budget.exceeded', "
                "'a.budget.config_error') "
                "ORDER BY created_at DESC LIMIT 50"
            ).fetchall()
        for r in rows:
            try:
                payload = json.loads(r["payload"]) if r["payload"] else {}
            except (json.JSONDecodeError, TypeError):
                payload = {}
            result["recent_events"].append({
                "event_id": r["event_id"],
                "created_at": r["created_at"],
                "event_type": r["event_type"],
                "layer": "a.budget",
                "scope": str(r["correlation_id"] or "")[-12:] or "unknown",
                "status_dimension": _map_status_dimension(r["event_type"]),
                "digest": _desensitize_digest(payload, r["event_type"]),
            })
    except sqlite3.OperationalError:
        pass

    # 只读读取 budget_guard_config.json 的 enabled
    try:
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "budget_guard_config.json"
        )
        with open(config_path, "r", encoding="utf-8") as fh:
            bg_config = json.load(fh)
        result["guard_enabled"] = bool(bg_config.get("enabled", False))
    except Exception:  # noqa: BLE001
        result["guard_enabled"] = False

    return result


# ---------------------------------------------------------------------------
# 错误响应
# ---------------------------------------------------------------------------

def _error_response(failure_code: str, message: str):
    """结构化的脱敏错误响应：仅固定 failure_code + 中文短述，不携路径。"""
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=500,
        content={"error": {"failure_code": failure_code, "message": message}},
    )


# ---------------------------------------------------------------------------
# 端点定义（全部 GET，只读）
# ---------------------------------------------------------------------------

@ceo_evidence_router.get("/overview")
def ceo_evidence_overview():
    """CEO 运行态势概览：部门/员工/工作流/A 层/C 层/B 层聚合计数 + 最近活动。

    纯只读 SELECT，不写库、不审批、不触发锁定动作集合。
    """
    try:
        config = _load_config()
        database = _get_database()
        tenant_id = TenantContext.current_tenant_id()
        counts = _build_overview_counts(database)
        recent = _build_recent_activity(database, limit=20)
        # 层状态摘要
        layer_status = {
            "a_layer": {
                "held_claims": counts.get("active_execution_claims", 0),
                "active_sessions": counts.get("active_sessions", 0),
            },
            "c_layer": {
                "accumulators": counts.get("budget_accumulators", 0),
            },
            "b_layer": {
                "pending_decisions": counts.get("pending_decisions", 0),
            },
        }
        return {
            "tenant_id": tenant_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "counts": counts,
            "recent_activity": recent,
            "layer_status": layer_status,
        }
    except Exception:  # noqa: BLE001 - 异常隔离，返回脱敏错误
        return _error_response("evidence_overview_unavailable", "运行概览暂时无法读取")


@ceo_evidence_router.get("/timeline")
def ceo_evidence_timeline(
    layer: str = Query("all", description="事件层级过滤: a.kernel|a.budget|b.governance|usage|all"),
    since: str | None = Query(None, description="起始时间 ISO UTC"),
    until: str | None = Query(None, description="截止时间 ISO UTC"),
    limit: int = Query(200, description="返回条数上限", ge=1, le=1000),
    status_dimension: str | None = Query(None, description="状态维度过滤: ok|waiting|blocked|failed|recovered"),
):
    """运行时间线：基于 ``evolution_events`` 的脱敏时序事件列表。

    纯只读 SELECT；layer 和 status_dimension 均为前端着色/过滤辅助。
    """
    try:
        database = _get_database()
        timeline = _build_timeline(
            database,
            layer=layer,
            since=since,
            until=until,
            limit=limit,
            status_dimension=status_dimension,
        )
        return {"timeline": timeline}
    except Exception:  # noqa: BLE001
        return _error_response("evidence_timeline_unavailable", "运行时间线暂时无法读取")


@ceo_evidence_router.get("/org-tree")
def ceo_evidence_org_tree(
    include_skills: bool = Query(True, description="是否包含技能节点"),
    include_tools: bool = Query(True, description="是否包含工具节点"),
):
    """组织树：Company→Department→Employee→Skill/Tool 层级（只读）。"""
    try:
        database = _get_database()
        return _build_org_tree(
            database,
            include_skills=include_skills,
            include_tools=include_tools,
        )
    except Exception:  # noqa: BLE001
        return _error_response("evidence_org_tree_unavailable", "组织树暂时无法读取")


@ceo_evidence_router.get("/pending-decisions")
def ceo_evidence_pending_decisions(
    status: str = Query("all", description="过滤状态: pending|resolved|cancelled|all"),
    limit: int = Query(100, description="返回条数上限", ge=1, le=500),
):
    """待拍板决策列表（只读展示，不审批、不修改）。

    pending 经 ``PendingDecisionStore.list_pending()`` 只读；
    resolved/cancelled 经独立只读 SELECT。
    """
    try:
        config = _load_config()
        store = PendingDecisionStore(_pending_db_path())
        decisions = _build_pending_decisions(
            store,
            status_filter=status,
            limit=limit,
        )
        return {
            "pending_count": len([d for d in decisions if d["status"] == "pending"]),
            "decisions": decisions,
        }
    except Exception:  # noqa: BLE001
        return _error_response("evidence_pending_decisions_unavailable", "治理待办暂时无法读取")


@ceo_evidence_router.get("/execution")
def ceo_evidence_execution():
    """A 层执行状态：活跃锁 / 会话 / 唤醒请求（脱敏，无 token）。"""
    try:
        database = _get_database()
        return _build_execution_status(database)
    except Exception:  # noqa: BLE001
        return _error_response("evidence_execution_unavailable", "执行状态暂时无法读取")


@ceo_evidence_router.get("/budget")
def ceo_evidence_budget():
    """C 层预算状态：累加器 + 最近事件 + guard 开关（只读）。"""
    try:
        database = _get_database()
        return _build_budget_status(database)
    except Exception:  # noqa: BLE001
        return _error_response("evidence_budget_unavailable", "预算状态暂时无法读取")


# ---------------------------------------------------------------------------
# 数据库获取（内置单例，便于端点引用）
# ---------------------------------------------------------------------------

_shared_database: Database | None = None


def _get_database() -> Database:
    """获取共享 ``Database`` 实例（lazy init，避免 import 时触盘）。

    统一从环境变量或相对路径解析，**不**使用 ``__file__`` 硬编码父目录，
    否则 uvicorn 启动 cwd 变化时，Issue B 端点会读到与写库路径不同的 db 文件。
    """
    global _shared_database
    if _shared_database is None:
        db_path = os.getenv("CURIS_DB", "data/curis.sqlite")
        _shared_database = Database(db_path)
    return _shared_database


__all__ = [
    "ceo_evidence_router",
    "CeoOverviewDTO",
    "TimelineEventDTO",
    "OrgNodeDTO",
    "PendingDecisionDTO",
    "ExecutionStatusDTO",
    "BudgetStatusDTO",
]
