"""Read-only Operating Intelligence projection over canonical Curis truth."""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from hashlib import sha256
from typing import Any

from .database import Database
from .organization_projection import department_assignments
from .runtime import RuntimeFoundation, RuntimeScopeError
from .tenant_context import TenantContext


SUCCESS = {"success", "succeeded", "completed"}
PROVENANCE = {"FACT", "POLICY", "EVIDENCE", "EST", "UNK"}
MIN_COMPARABLE_SAMPLE = 2


def _utc(value: str | None) -> datetime | None:
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).astimezone(timezone.utc)


def _json(value: str | None) -> dict[str, Any]:
    try:
        parsed = json.loads(value or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _metric(
    key: str,
    label: str,
    value: int | float | str | None,
    *,
    unit: str,
    source: str,
    refs: list[str],
    updated_at: str | None,
    verification: str,
    sample_size: int,
    unknown_reason: str | None = None,
    currency: str | None = None,
    excluded_estimated_count: int = 0,
) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "value": value,
        "unit": unit,
        "source": source,
        "source_refs": refs,
        "freshness": "UPDATED" if updated_at else "MISSING",
        "updated_at": updated_at,
        "verification": verification,
        "sample_size": sample_size,
        "unknown_reason": unknown_reason,
        "definition": key,
        "currency": currency,
        "excluded_estimated_count": excluded_estimated_count,
    }


class OperatingIntelligence:
    """Bounded analytical view; persisted truth remains in existing stores."""

    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def read(
        self,
        company_id: str,
        *,
        days: int = 30,
        business_id: str | None = None,
    ) -> dict[str, Any]:
        if days not in {7, 30}:
            raise ValueError("time range must be 7 or 30 days")
        self.foundation._require_company(company_id)
        now = datetime.now(timezone.utc)
        current_start = now - timedelta(days=days)
        previous_start = current_start - timedelta(days=days)

        with self.db.connect() as connection:
            company = connection.execute(
                "select company_id, name, status, updated_at from companies "
                "where tenant_id=? and company_id=?",
                (self.tenant_id, company_id),
            ).fetchone()
            businesses = connection.execute(
                "select business_id, department_id, name, lifecycle_status, goal, positioning, updated_at "
                "from canonical_businesses where tenant_id=? and company_id=? "
                "and lifecycle_status!='ARCHIVED' order by created_at, business_id",
                (self.tenant_id, company_id),
            ).fetchall()
            if business_id and business_id not in {row["business_id"] for row in businesses}:
                raise RuntimeScopeError("Business is not in the current Company")
            workspaces = connection.execute(
                "select workspace_id, business_id, name, status, updated_at from workspaces "
                "where tenant_id=? and company_id=? and business_relation_status='RESOLVED'",
                (self.tenant_id, company_id),
            ).fetchall()
            usage = connection.execute(
                "select * from ai_usage_records where tenant_id=? and company_id=? "
                "order by occurred_at, usage_record_id",
                (self.tenant_id, company_id),
            ).fetchall()
            runtime = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type in ('ACCEPTANCE','EVIDENCE','OUTCOME') order by created_at, entity_id",
                (self.tenant_id, company_id),
            ).fetchall()
            reports = connection.execute(
                "select a.*, t.company_id, t.workspace_id, t.work_ref, t.employee_id, t.employee_name "
                "from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                "where a.tenant_id=? and t.company_id=? and a.artifact_type='analysis_report' "
                "order by a.created_at desc, a.artifact_id",
                (self.tenant_id, company_id),
            ).fetchall()
            decisions = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='DECISION_PACKET' order by created_at, entity_id",
                (self.tenant_id, company_id),
            ).fetchall()
            analyst_refs = {
                assignment["data"]["companyEmployeeRef"]
                for assignment in department_assignments(self.db, company_id)
                if assignment["data"].get("responsibilityKey") == "data.analytics.company_analysis"
            }
            analyst = None
            if len(analyst_refs) == 1:
                analyst = connection.execute(
                    "select id, name, role, status from employee_instances where tenant_id=? and company_id=? and id=?",
                    (self.tenant_id, company_id, next(iter(analyst_refs))),
                ).fetchone()

        workspace_business = {row["workspace_id"]: row["business_id"] for row in workspaces}
        scope_usage = [dict(row) for row in usage if not business_id or row["business_id"] == business_id]
        scope_runtime = [
            dict(row) for row in runtime
            if not business_id or workspace_business.get(row["workspace_id"]) == business_id
        ]
        current = self._window(scope_usage, scope_runtime, current_start, now)
        previous = self._window(scope_usage, scope_runtime, previous_start, current_start)
        metrics = self._with_baseline(current, previous)
        report_items = self._reports(reports, decisions, workspace_business, business_id)
        scopes = [
            {
                "business_id": row["business_id"],
                "department_id": row["department_id"],
                "name": row["name"],
                "status": row["lifecycle_status"],
                "goal": row["goal"],
                "workspace_count": sum(item["business_id"] == row["business_id"] for item in workspaces),
            }
            for row in businesses
        ]
        scope_name = next((item["name"] for item in scopes if item["business_id"] == business_id), company["name"])
        return {
            "company": dict(company),
            "scope": {"type": "BUSINESS" if business_id else "COMPANY", "ref": business_id or company_id, "name": scope_name},
            "scopes": scopes,
            "time_range": {"days": days, "start": current_start.isoformat(), "end": now.isoformat()},
            "analyst": dict(analyst) if analyst else {"name": "经营分析", "role": "基于公司事实提供分析", "status": "NEUTRAL"},
            "metrics": metrics,
            "summary": self._summary(metrics),
            "benchmark": self._benchmark(dict(company), scopes, usage, runtime, workspace_business, current_start, now),
            "reports": report_items,
            "trust": {
                "canonical_sources": ["Company OS", "Result / Acceptance", "AI Usage Ledger"],
                "manual_count": sum(_json(row["data_json"]).get("source") == "CEO_MANUAL" for row in scope_runtime),
                "external_outcome": {"status": "MISSING", "label": "外部业务结果待连接", "value": None},
            },
        }

    def _window(
        self,
        usage: list[dict[str, Any]],
        runtime: list[dict[str, Any]],
        start: datetime,
        end: datetime,
    ) -> list[dict[str, Any]]:
        calls = [row for row in usage if (stamp := _utc(row.get("occurred_at"))) and start <= stamp < end]
        acceptances = [
            row for row in runtime
            if row["entity_type"] == "ACCEPTANCE"
            and (stamp := _utc(row.get("updated_at") or row.get("created_at")))
            and start <= stamp < end
            and row["lifecycle_status"] in {"ACCEPTED", "REJECTED"}
        ]
        latest_usage = max((row["occurred_at"] for row in calls), default=None)
        latest_acceptance = max((row["updated_at"] for row in acceptances), default=None)
        provider_cost_rows = [row for row in calls if row["cost_source"] == "provider_reported" and row["cost_amount"] is not None]
        estimated_cost_rows = [row for row in calls if row["cost_source"] == "estimated" and row["cost_amount"] is not None]
        cost_rows = provider_cost_rows or estimated_cost_rows
        latest_cost = max((row["occurred_at"] for row in cost_rows), default=None)
        currencies = {str(row["currency"] or "").upper() for row in cost_rows if row["currency"]}
        latencies = [int(row["latency_ms"]) for row in calls if row["latency_ms"] is not None]
        failed = sum(str(row["execution_status"]).lower() not in SUCCESS for row in calls)
        accepted = sum(row["lifecycle_status"] == "ACCEPTED" for row in acceptances)
        known_cost = sum((Decimal(str(row["cost_amount"])) for row in cost_rows), Decimal("0")) if cost_rows and len(currencies) == 1 else None
        cost_verification = "VERIFIED" if provider_cost_rows and known_cost is not None else "ESTIMATED" if estimated_cost_rows and known_cost is not None else "UNKNOWN"
        cost_unknown = "存在多币种记录，不能直接合计" if len(currencies) > 1 else None if known_cost is not None else "当前时间范围没有可确认的成本记录"
        return [
            _metric("provider_cost", "执行成本", f"{known_cost:.2f}" if known_cost is not None else None, unit="CURRENCY", source="AI Usage Ledger", refs=[row["usage_record_id"] for row in cost_rows], updated_at=latest_cost, verification=cost_verification, sample_size=len(cost_rows), unknown_reason=cost_unknown, currency=next(iter(currencies), None) if len(currencies) == 1 else None, excluded_estimated_count=len(estimated_cost_rows) if provider_cost_rows else 0),
            _metric("latency_p50", "响应时间 P50", int(statistics.median(latencies)) if latencies else None, unit="ms", source="AI Usage Ledger", refs=[row["usage_record_id"] for row in calls if row["latency_ms"] is not None], updated_at=latest_usage, verification="VERIFIED" if latencies else "UNKNOWN", sample_size=len(latencies), unknown_reason=None if latencies else "当前时间范围没有延迟记录"),
            _metric("acceptance_rate", "结果验收率", round(accepted * 100 / len(acceptances), 1) if acceptances else None, unit="%", source="Acceptance Runtime", refs=[row["entity_id"] for row in acceptances], updated_at=latest_acceptance, verification="VERIFIED" if acceptances else "UNKNOWN", sample_size=len(acceptances), unknown_reason=None if acceptances else "当前时间范围没有已裁决的验收记录"),
            _metric("failure_rate", "失败率", round(failed * 100 / len(calls), 1) if calls else None, unit="%", source="AI Usage Ledger", refs=[row["usage_record_id"] for row in calls], updated_at=latest_usage, verification="VERIFIED" if calls else "UNKNOWN", sample_size=len(calls), unknown_reason=None if calls else "当前时间范围没有 Provider 执行记录"),
        ]

    @staticmethod
    def _with_baseline(current: list[dict[str, Any]], previous: list[dict[str, Any]]) -> list[dict[str, Any]]:
        prior = {item["key"]: item for item in previous}
        for metric in current:
            baseline = prior[metric["key"]]
            metric["baseline"] = baseline["value"]
            metric["comparison"] = None
            same_definition = metric["unit"] != "CURRENCY" or metric.get("currency") == baseline.get("currency")
            if metric["value"] is not None and baseline["value"] is not None and same_definition:
                metric["comparison"] = round(float(metric["value"]) - float(baseline["value"]), 2)
            metric["baseline_sample_size"] = baseline["sample_size"]
        return current

    @staticmethod
    def _summary(metrics: list[dict[str, Any]]) -> dict[str, Any]:
        def display(metric: dict[str, Any], value: Any) -> str:
            if metric["unit"] == "CURRENCY":
                symbol = {"CNY": "¥", "USD": "$", "EUR": "€"}.get(metric.get("currency"), f"{metric.get('currency') or ''} ")
                return f"{symbol}{float(value):.2f}"
            return f"{value}{metric['unit']}"

        known = [item for item in metrics if item["value"] is not None]
        compared = [item for item in known if item["comparison"] is not None]
        if compared:
            lead = compared[0]
            delta = display(lead, abs(lead["comparison"]))
            return {
                "headline": f"{lead['label']}较上一周期{'增加' if lead['comparison'] >= 0 else '减少'} {delta}",
                "fact": f"当前值 {display(lead, lead['value'])}，样本 {lead['sample_size']} 条。",
                "analysis": "这是同口径周期比较；原因仍需结合来源记录继续核实。",
                "recommendation": "先查看来源记录，再决定是否形成经营动作。",
                "certainty": "PARTIAL",
            }
        if known:
            return {
                "headline": "已有经营事实，但历史不足以形成趋势",
                "fact": f"当前可读取 {len(known)} 项指标。",
                "analysis": "缺少同口径上一周期数据，不能判断改善或恶化。",
                "recommendation": "继续积累同口径记录。",
                "certainty": "UNKNOWN",
            }
        return {
            "headline": "当前没有足够数据形成经营结论",
            "fact": "尚未读取到当前时间范围内的可验证执行、成本或验收记录。",
            "analysis": "未知不等于零。",
            "recommendation": "连接真实执行或结果来源后再分析。",
            "certainty": "UNKNOWN",
        }

    def _benchmark(self, company: dict[str, Any], scopes: list[dict[str, Any]], usage_rows: list[Any], runtime_rows: list[Any], workspace_business: dict[str, str], start: datetime, end: datetime) -> dict[str, Any]:
        rows = []
        for scope in scopes:
            usage = [dict(row) for row in usage_rows if row["business_id"] == scope["business_id"]]
            runtime = [dict(row) for row in runtime_rows if workspace_business.get(row["workspace_id"]) == scope["business_id"]]
            metrics = self._window(usage, runtime, start, end)
            rows.append({"business_id": scope["business_id"], "name": scope["name"], "metrics": metrics})
        comparable = []
        for key in ("provider_cost", "latency_p50", "acceptance_rate", "failure_rate"):
            values = [next(item for item in row["metrics"] if item["key"] == key) for row in rows]
            same_currency = key != "provider_cost" or len({item.get("currency") for item in values}) == 1
            ready = len(values) >= 2 and same_currency and all(item["value"] is not None and item["sample_size"] >= MIN_COMPARABLE_SAMPLE for item in values)
            comparable.append({
                "metric": key,
                "status": "COMPARABLE" if ready else "NOT_COMPARABLE",
                "reason": None if ready else "至少两个业务需要同一时间范围、同一口径、同一币种且每个业务不少于 2 条样本",
                "rows": [{"business_id": row["business_id"], "name": row["name"], **value} for row, value in zip(rows, values)],
            })
        return {"company_id": company["company_id"], "period": {"start": start.isoformat(), "end": end.isoformat()}, "metrics": comparable}

    @staticmethod
    def _reports(report_rows: list[Any], decision_rows: list[Any], workspace_business: dict[str, str], business_id: str | None) -> list[dict[str, Any]]:
        decisions = [dict(row) | {"data": _json(row["data_json"])} for row in decision_rows]
        result = []
        for row in report_rows:
            if business_id and workspace_business.get(row["workspace_id"]) != business_id:
                continue
            content = _json(row["content"])
            required = {"scope", "period", "facts", "analysis", "unknown", "recommendation", "evidenceRefs", "author", "createdAt"}
            if not required.issubset(content):
                continue
            decision = next((item for item in decisions if item["data"].get("reportRef") == row["artifact_id"]), None)
            result.append({
                "artifact_id": row["artifact_id"], "title": row["title"], "status": row["status"],
                "content_sha256": row["content_sha256"], "created_at": row["created_at"],
                "workspace_id": row["workspace_id"], "business_id": workspace_business.get(row["workspace_id"]),
                "task_id": row["task_id"], "content": content,
                "decision": {"decision_id": decision["entity_id"], "status": decision["lifecycle_status"]} if decision else None,
            })
        return result

    def submit_report_decision(self, company_id: str, artifact_id: str) -> dict[str, Any]:
        """Promote a real analysis Artifact into the existing P7 Decision Packet."""
        self.foundation._require_company(company_id)
        with self.db.connect() as connection:
            row = connection.execute(
                "select a.*, t.company_id, t.workspace_id, t.work_ref from artifacts a "
                "join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                "where a.tenant_id=? and a.artifact_id=? and a.artifact_type='analysis_report'",
                (self.tenant_id, artifact_id),
            ).fetchone()
        if row is None or row["company_id"] != company_id or not row["workspace_id"]:
            raise RuntimeScopeError("Report is not in the current Company")
        content = _json(row["content"])
        candidate = content.get("decisionCandidate")
        if not isinstance(candidate, dict):
            raise ValueError("Report has no decision candidate")
        required = ("event", "cannotDecideReason", "options", "recommendation", "recommendationReason", "ceoChoicePrompt", "continuationPlan")
        if not all(candidate.get(key) for key in required):
            raise ValueError("Report decision candidate is incomplete")
        options = candidate["options"]
        if not isinstance(options, list) or not 2 <= len(options) <= 4:
            raise ValueError("Report decision requires two to four options")
        for option in options:
            if not isinstance(option, dict) or not all(option.get(key) for key in ("optionId", "label", "impact", "risk", "cost")):
                raise ValueError("Report decision option is incomplete")
            for key in ("impact", "risk", "cost"):
                if option[key].get("provenance") not in PROVENANCE or not str(option[key].get("value") or "").strip():
                    raise ValueError("Report decision provenance is invalid")
        recommendation = candidate["recommendation"]
        reason = candidate["recommendationReason"]
        option_ids = {str(option["optionId"]) for option in options}
        if (
            not isinstance(recommendation, dict)
            or recommendation.get("provenance") not in PROVENANCE
            or str(recommendation.get("optionId") or "") not in option_ids
            or not isinstance(reason, dict)
            or reason.get("provenance") not in PROVENANCE
            or not str(reason.get("value") or "").strip()
        ):
            raise ValueError("Report recommendation provenance is invalid")
        report_refs = [str(item) for item in content.get("evidenceRefs") or [] if str(item)]
        if not report_refs:
            raise ValueError("Report decision requires evidence")
        with self.db.connect() as connection:
            known_refs = {
                item["ref"]
                for item in connection.execute(
                    "select usage_record_id as ref from ai_usage_records where tenant_id=? and company_id=? "
                    "union select entity_id as ref from runtime_entities where tenant_id=? and company_id=? and entity_type='EVIDENCE' "
                    "union select a.artifact_id as ref from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                    "where a.tenant_id=? and t.company_id=?",
                    (self.tenant_id, company_id, self.tenant_id, company_id, self.tenant_id, company_id),
                ).fetchall()
            }
        if any(ref not in known_refs for ref in report_refs):
            raise RuntimeScopeError("Report evidence is not in the current Company")
        decision_id = "decision-operating-" + sha256(f"{self.tenant_id}:{artifact_id}".encode()).hexdigest()[:24]
        try:
            existing = self.foundation.get(decision_id)
        except KeyError:
            existing = None
        if existing:
            if existing["data"].get("reportRef") != artifact_id:
                raise ValueError("Decision identity conflict")
            return existing
        packet = self.foundation.create(
            "DECISION_PACKET", entity_id=decision_id, company_id=company_id,
            workspace_id=row["workspace_id"], parent_id=row["work_ref"] or row["task_id"], owner_ref="CEO",
            data={
                "kind": "OPERATING_ANALYSIS_DECISION", "complexity": "HIGH_RISK",
                "layer0Actions": ["VIEW_OPTIONS", "DEFER"], "reportRef": artifact_id,
                "reportSha256": row["content_sha256"], "event": candidate["event"],
                "cannotDecideReason": candidate["cannotDecideReason"], "options": options,
                "recommendation": candidate["recommendation"], "recommendationReason": candidate["recommendationReason"],
                "ceoChoicePrompt": candidate["ceoChoicePrompt"], "continuationPlan": candidate["continuationPlan"],
                "evidenceRefs": report_refs,
                "plainPackage": {
                    "whatHappened": candidate["event"],
                    "whyAiCannotDecide": candidate["cannotDecideReason"],
                    "options": options, "recommendation": candidate["recommendation"],
                    "recommendationReason": candidate["recommendationReason"],
                    "afterChoice": candidate["continuationPlan"], "reportRef": artifact_id,
                    "evidenceRefs": report_refs,
                },
            },
        )
        packet = self.foundation.transition(packet["entity_id"], "READY", actor="SYSTEM", trigger="prepare", evidence_refs=report_refs)
        return self.foundation.transition(packet["entity_id"], "WAITING_CEO", actor="SYSTEM", trigger="request_decision", evidence_refs=report_refs)
