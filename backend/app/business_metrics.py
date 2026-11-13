"""CEO 经营日聚合与经营指标事实源（Phase-9）。

从现有实体（projects / tasks / artifacts / ai_usage_records / workflow_runs /
employee_instances）聚合租户内公司级经营指标，持久化到 ``business_metrics``
（周期桶 + 唯一键 upsert），并提供 CEO 经营日聚合五段结构
（brief / matters / timeline / pulse / handoffs）。

设计文档：docs/plan/ceo-operating-day-design.md

纪律：
- 全部租户作用域（TenantContext），company 归属校验。
- ``estimated_cost`` 仅估算聚合，不做计费、不触碰 payment。
- v1 不调 AI（brief 模板拼装），matters 为确定性规则推导。
- 不新建实体 CRUD、不改既有表结构。
"""

from __future__ import annotations

import datetime
import json
import uuid
from typing import Any

from .database import Database
from .evolution_event_log import EvolutionEventLog
from .tenant_context import TenantContext

# 周期桶格式：'day:YYYY-MM-DD'（week/month 预留）
METRIC_KEYS = (
    "active_projects",
    "tasks_total",
    "tasks_completed",
    "blocked_tasks",
    "task_completion_rate",
    "artifacts_count",
    "employees_active",
    "workflow_runs",
    "estimated_cost",
)

_METRIC_UNITS = {
    "active_projects": "个",
    "tasks_total": "个",
    "tasks_completed": "个",
    "blocked_tasks": "个",
    "task_completion_rate": "%",
    "artifacts_count": "项",
    "employees_active": "人",
    "workflow_runs": "次",
    "estimated_cost": "USD",
}


def _today_period() -> str:
    return "day:" + datetime.date.today().isoformat()


def _previous_day_period(period: str) -> str:
    """day 周期取前一天；非 day 周期无对比 → 返回原周期（趋势判 flat）。"""
    if period.startswith("day:"):
        day = datetime.date.fromisoformat(period.split(":", 1)[1])
        return "day:" + (day - datetime.timedelta(days=1)).isoformat()
    return period


class BusinessMetricService:
    """经营指标事实源：聚合 → upsert → 读取。"""

    def __init__(self, database: Database, event_log: EvolutionEventLog) -> None:
        self.database = database
        self.event_log = event_log

    def compute(self, company_id: str, period: str | None = None) -> dict[str, dict[str, Any]]:
        """聚合公司指标并 upsert 到 business_metrics，返回 {metric_key: {value, unit}}。"""
        tenant_id = TenantContext.current_tenant_id()
        self._require_company(tenant_id, company_id)
        period = period or _today_period()
        metrics = self._aggregate(tenant_id, company_id)
        with self.database.connect() as connection:
            for metric_key, item in metrics.items():
                if item["value"] is None:
                    # Unknown is not zero. This is a replaceable aggregate cache,
                    # never the immutable usage ledger or business history.
                    connection.execute("delete from business_metrics where tenant_id=? and company_id=? and period=? and metric_key=?",
                        (tenant_id, company_id, period, metric_key))
                    continue
                connection.execute(
                    """
                    insert into business_metrics (
                      metric_id, tenant_id, company_id, period, metric_key,
                      value, unit, source, updated_at
                    ) values (?, ?, ?, ?, ?, ?, ?, 'aggregated', current_timestamp)
                    on conflict(tenant_id, company_id, period, metric_key) do update set
                      value = excluded.value,
                      unit = excluded.unit,
                      source = 'aggregated',
                      updated_at = current_timestamp
                    """,
                    (
                        f"bm-{uuid.uuid4()}",
                        tenant_id,
                        company_id,
                        period,
                        metric_key,
                        item["value"],
                        item["unit"],
                    ),
                )
        self.event_log.record(
            correlation_id=str(uuid.uuid4()),
            event_type="business.metrics_computed",
            tenant_id=tenant_id,
            payload={
                "company_id": company_id,
                "period": period,
                "metric_count": len(metrics),
            },
        )
        return {key: {"value": item["value"], "unit": item["unit"]} for key, item in metrics.items()}

    def read_period(
        self, company_id: str, period: str
    ) -> dict[str, dict[str, Any]]:
        tenant_id = TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select metric_key, value, unit from business_metrics "
                "where tenant_id = ? and company_id = ? and period = ?",
                (tenant_id, company_id, period),
            ).fetchall()
        result = {row["metric_key"]: {"value": row["value"], "unit": row["unit"]} for row in rows}
        if rows and "estimated_cost" not in result:
            result["estimated_cost"] = {"value": None, "unit": _METRIC_UNITS["estimated_cost"]}
        return result

    # ── 内部 ──────────────────────────────────────────────────────
    def _require_company(self, tenant_id: str, company_id: str) -> None:
        with self.database.connect() as connection:
            row = connection.execute(
                "select company_id from companies where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()
        if row is None:
            raise KeyError("company not found")

    def _aggregate(
        self, tenant_id: str, company_id: str
    ) -> dict[str, dict[str, Any]]:
        with self.database.connect() as connection:
            active_projects = connection.execute(
                "select count(*) as n from projects "
                "where tenant_id = ? and company_id = ? and status = 'active'",
                (tenant_id, company_id),
            ).fetchone()["n"]
            tasks_total = connection.execute(
                "select count(*) as n from tasks "
                "where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()["n"]
            tasks_completed = connection.execute(
                "select count(*) as n from tasks "
                "where tenant_id = ? and company_id = ? and status = 'COMPLETED'",
                (tenant_id, company_id),
            ).fetchone()["n"]
            blocked_tasks = connection.execute(
                "select count(*) as n from tasks "
                "where tenant_id = ? and company_id = ? and status in ('FAILED','BLOCKED')",
                (tenant_id, company_id),
            ).fetchone()["n"]
            artifacts_count = connection.execute(
                "select count(*) as n from artifacts a join tasks t "
                "on t.tenant_id = a.tenant_id and t.task_id = a.task_id "
                "where a.tenant_id = ? and t.company_id = ?",
                (tenant_id, company_id),
            ).fetchone()["n"]
            employees_active = connection.execute(
                "select count(*) as n from employee_instances "
                "where tenant_id = ? and company_id = ? and enabled = 1 "
                "and deleted_at is null",
                (tenant_id, company_id),
            ).fetchone()["n"]
            workflow_runs = connection.execute(
                "select count(*) as n from workflow_runs "
                "where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()["n"]
            estimated_cost = connection.execute(
                "select case when count(*)=0 then 0 when count(cost_amount)<count(*) then null else sum(cost_amount) end as n from ai_usage_records "
                "where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()["n"]

        completion_rate = (
            round(tasks_completed / tasks_total * 100, 1) if tasks_total else 0.0
        )
        return {
            "active_projects": {"value": float(active_projects), "unit": _METRIC_UNITS["active_projects"]},
            "tasks_total": {"value": float(tasks_total), "unit": _METRIC_UNITS["tasks_total"]},
            "tasks_completed": {"value": float(tasks_completed), "unit": _METRIC_UNITS["tasks_completed"]},
            "blocked_tasks": {"value": float(blocked_tasks), "unit": _METRIC_UNITS["blocked_tasks"]},
            "task_completion_rate": {"value": completion_rate, "unit": _METRIC_UNITS["task_completion_rate"]},
            "artifacts_count": {"value": float(artifacts_count), "unit": _METRIC_UNITS["artifacts_count"]},
            "employees_active": {"value": float(employees_active), "unit": _METRIC_UNITS["employees_active"]},
            "workflow_runs": {"value": float(workflow_runs), "unit": _METRIC_UNITS["workflow_runs"]},
            "estimated_cost": {"value": None if estimated_cost is None else round(float(estimated_cost), 6), "unit": _METRIC_UNITS["estimated_cost"]},
        }


class CeoOperatingDayService:
    """CEO 经营日聚合：brief / matters / timeline / pulse / handoffs。"""

    def __init__(
        self,
        database: Database,
        metric_service: BusinessMetricService,
    ) -> None:
        self.database = database
        self.metric_service = metric_service

    def build(self, company_id: str, period: str | None = None) -> dict[str, Any]:
        tenant_id = TenantContext.current_tenant_id()
        self.metric_service._require_company(tenant_id, company_id)
        period = period or _today_period()
        metrics = self.metric_service.compute(company_id, period)

        pulse = self._build_pulse(company_id, period, metrics)
        matters = self._build_matters(metrics)
        timeline = self._build_timeline(tenant_id, company_id)
        brief = self._build_brief(metrics)
        return {
            "company_id": company_id,
            "date": period.split(":", 1)[1] if ":" in period else period,
            "period": period,
            "brief": brief,
            "matters": matters,
            "timeline": timeline,
            "pulse": pulse,
            "handoffs": [],
        }

    def _build_pulse(
        self,
        company_id: str,
        period: str,
        metrics: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        previous = self.metric_service.read_period(company_id, _previous_day_period(period))
        pulse = []
        for metric_key in METRIC_KEYS:
            item = metrics[metric_key]
            trend = "flat"
            if previous and metric_key in previous:
                current = item["value"]
                old = previous[metric_key]["value"]
                if current is not None and old is not None and abs(current - old) > 1e-9:
                    trend = "up" if current > old else "down"
            pulse.append(
                {
                    "metric_key": metric_key,
                    "value": item["value"],
                    "unit": item["unit"],
                    "trend": trend,
                }
            )
        return pulse

    def _build_matters(self, metrics: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
        matters: list[dict[str, Any]] = []
        blocked = int(metrics["blocked_tasks"]["value"])
        if blocked > 0:
            matters.append(
                {
                    "level": "risk",
                    "severity": "high",
                    "metric_key": "blocked_tasks",
                    "message": f"{blocked} 个任务受阻，需要处理",
                }
            )
        total = int(metrics["tasks_total"]["value"])
        rate = metrics["task_completion_rate"]["value"]
        if total > 0 and rate < 30:
            matters.append(
                {
                    "level": "attention",
                    "severity": "medium",
                    "metric_key": "task_completion_rate",
                    "message": f"任务完成率偏低（{rate}%）",
                }
            )
        cost = metrics["estimated_cost"]["value"]
        if cost is not None and cost > 0:
            matters.append(
                {
                    "level": "attention",
                    "severity": "low",
                    "metric_key": "estimated_cost",
                    "message": f"本周期模型成本估算 ${cost:.2f}",
                }
            )
        if not matters:
            active = int(metrics["active_projects"]["value"])
            matters.append(
                {
                    "level": "info",
                    "severity": "low",
                    "metric_key": "active_projects",
                    "message": f"经营正常：{active} 个项目活跃",
                }
            )
        return matters

    def _build_timeline(
        self, tenant_id: str, company_id: str
    ) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            tasks = connection.execute(
                "select task_id, content, created_at from tasks "
                "where tenant_id = ? and company_id = ? "
                "order by created_at desc limit 5",
                (tenant_id, company_id),
            ).fetchall()
            runs = connection.execute(
                "select workflow_run_id, workflow_template_id, created_at "
                "from workflow_runs where tenant_id = ? and company_id = ? "
                "order by created_at desc limit 3",
                (tenant_id, company_id),
            ).fetchall()
            artifacts = connection.execute(
                "select a.artifact_id, a.title, a.created_at from artifacts a "
                "join tasks t on t.tenant_id = a.tenant_id and t.task_id = a.task_id "
                "where a.tenant_id = ? and t.company_id = ? "
                "order by a.created_at desc limit 3",
                (tenant_id, company_id),
            ).fetchall()
        events: list[dict[str, Any]] = []
        for row in tasks:
            events.append(
                {
                    "at": row["created_at"],
                    "type": "task",
                    "title": str(row["content"] or "")[:60],
                    "ref": row["task_id"],
                }
            )
        for row in runs:
            events.append(
                {
                    "at": row["created_at"],
                    "type": "workflow",
                    "title": str(row["workflow_template_id"] or ""),
                    "ref": row["workflow_run_id"],
                }
            )
        for row in artifacts:
            events.append(
                {
                    "at": row["created_at"],
                    "type": "artifact",
                    "title": str(row["title"] or "")[:60],
                    "ref": row["artifact_id"],
                }
            )
        events.sort(key=lambda item: str(item["at"] or ""), reverse=True)
        return events[:10]

    @staticmethod
    def _build_brief(metrics: dict[str, dict[str, Any]]) -> dict[str, Any]:
        active = int(metrics["active_projects"]["value"])
        total = int(metrics["tasks_total"]["value"])
        rate = metrics["task_completion_rate"]["value"]
        artifacts = int(metrics["artifacts_count"]["value"])
        employees = int(metrics["employees_active"]["value"])
        blocked = int(metrics["blocked_tasks"]["value"])
        if total == 0 and artifacts == 0 and employees == 0:
            summary = "暂无经营数据，先创建你的第一个业务。"
        else:
            parts = [f"{active} 个项目活跃", f"任务完成率 {rate}%", f"累计成果 {artifacts} 项", f"员工 {employees} 人"]
            if blocked:
                parts.append(f"{blocked} 个任务受阻")
            summary = "；".join(parts) + "。"
        return {
            "summary": summary,
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
