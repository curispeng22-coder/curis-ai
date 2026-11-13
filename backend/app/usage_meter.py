from __future__ import annotations

from collections import defaultdict
from typing import Any

from decimal import Decimal

from .ai_usage import AIUsageService


class UsageMeterService:
    """Read-only Workspace usage aggregation for future Admin Billing.

    Compatibility projection backed by the authoritative AI usage ledger.
    """

    def __init__(self, ai_usage: AIUsageService):
        self.ai_usage = ai_usage

    def query(
        self,
        *,
        tenant_id: str,
        capability_type: str | None = None,
        capability_source: str | None = None,
        model_gateway_id: str | None = None,
        model_name: str | None = None,
        status: str | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> dict[str, Any]:
        if tenant_id != self.ai_usage._tenant():
            raise PermissionError("tenant scope mismatch")
        events = self.ai_usage.list_records(
            model=model_name,
            execution_status=status,
            since=since,
            until=until,
            limit=1000,
        )
        if capability_type is not None:
            events = [item for item in events if item["capability_type"] == capability_type]
        if model_gateway_id is not None:
            events = [item for item in events if item["model_gateway_id"] == model_gateway_id]
        return {
            "tenant_id": tenant_id,
            "filters": {
                "capability_type": capability_type,
                "capability_source": capability_source,
                "model_gateway_id": model_gateway_id,
                "model_name": model_name,
                "status": status,
                "since": since,
                "until": until,
            },
            "totals": self._totals(events),
            "by_capability_source": self._group(events, "capability_source"),
            "by_capability_type": self._group(events, "capability_type"),
            "by_model": self._group_model(events),
            "by_employee": self._group(events, "employee_id", fallback_key="employee_role"),
            "by_workflow": self._group(events, "workflow_run_id"),
        }

    @staticmethod
    def _totals(events: list[dict[str, Any]]) -> dict[str, Any]:
        def token_sum(name: str) -> int | None:
            values = [event[name] for event in events if event[name] is not None]
            return sum(values) if values else None

        return {
            "usage_event_count": len(events),
            "prompt_tokens": token_sum("input_tokens"),
            "completion_tokens": token_sum("output_tokens"),
            "total_tokens": token_sum("total_tokens"),
            **UsageMeterService._cost_totals(events),
            "unmetered_count": sum(event["metering_status"] == "unknown" for event in events),
        }

    @staticmethod
    def _cost_totals(events: list[dict[str, Any]]) -> dict[str, Any]:
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            buckets[str(event.get("currency") or "UNKNOWN")].append(event)
        amounts = []
        for currency, rows in sorted(buckets.items()):
            known = [Decimal(str(row["cost_amount"])) for row in rows
                     if row.get("cost_amount") is not None and row.get("cost_source") != "unknown"]
            amounts.append({"currency": currency,
                            "known_cost": float(sum(known, Decimal("0"))) if known else None,
                            "unknown_cost_count": len(rows) - len(known)})
        unknown = sum(row["unknown_cost_count"] for row in amounts)
        single = amounts[0] if len(amounts) == 1 else None
        return {
            "estimated_cost": single["known_cost"] if single and not unknown and single["currency"] != "UNKNOWN" else None,
            "currency": single["currency"] if single else None,
            "unknown_cost_count": unknown,
            "cost_by_currency": amounts,
        }

    def _group(
        self,
        events: list[dict[str, Any]],
        key: str,
        *,
        fallback_key: str | None = None,
    ) -> list[dict[str, Any]]:
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            raw_key = event.get(key) or (event.get(fallback_key) if fallback_key else "")
            bucket_key = str(raw_key or "unassigned")
            buckets[bucket_key].append(event)
        return [
            {"key": bucket_key, **self._totals(bucket_events)}
            for bucket_key, bucket_events in sorted(buckets.items())
        ]

    def _group_model(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            gateway_id = str(event.get("model_gateway_id") or "unassigned")
            model_name = str(event.get("model_name") or "unassigned")
            buckets[(gateway_id, model_name)].append(event)
        return [
            {
                "key": f"{gateway_id}:{model_name}",
                "model_gateway_id": gateway_id,
                "model_name": model_name,
                **self._totals(bucket_events),
            }
            for (gateway_id, model_name), bucket_events in sorted(buckets.items())
        ]
