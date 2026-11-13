from __future__ import annotations

import json
from typing import Any

from .database import Database
from .tenant_context import TenantContext


class EvolutionEventLog:
    """Append-only event log for evolution audit.

    This class is intentionally write-restricted: the ONLY mutation method is
    ``record`` (INSERT). There is deliberately no update / delete / mutate path,
    so the log is tamper-evident by construction. Read access is provided via
    ``get_by_correlation_id`` and ``get_all``.
    """

    def __init__(self, database: Database):
        self.database = database

    def record_in_connection(self, connection, *, correlation_id: str, event_type: str,
                             payload: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        """Append inside the caller's already-started write transaction."""
        tenant = TenantContext.current_tenant_id()
        existing = connection.execute(
            "select * from evolution_events where idempotency_key=?", (idempotency_key,),
        ).fetchone()
        if existing is not None:
            if (existing["tenant_id"], existing["event_type"], existing["correlation_id"]) != (tenant, event_type, correlation_id):
                raise ValueError("Event idempotency key belongs to a different scope")
            event = self._event_from_row(existing)
            if event["payload"] != payload:
                raise ValueError("Event idempotency key has a different payload")
            return event
        cursor = connection.execute(
            "insert into evolution_events(correlation_id,event_type,payload,tenant_id,idempotency_key) values (?,?,?,?,?)",
            (correlation_id, event_type, json.dumps(payload, ensure_ascii=False), tenant, idempotency_key),
        )
        return self._event_from_row(connection.execute(
            "select * from evolution_events where event_id=?", (cursor.lastrowid,),
        ).fetchone())

    def record(
        self,
        *,
        correlation_id: str,
        event_type: str,
        payload: dict[str, Any],
        tenant_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        resolved_tenant = tenant_id or TenantContext.current_tenant_id()
        with self.database.connect() as connection:
            if idempotency_key:
                # Serialize check + append across processes; no schema/index migration.
                connection.execute("begin immediate")
                existing = connection.execute(
                    "select * from evolution_events where idempotency_key = ?",
                    (idempotency_key,),
                ).fetchone()
                if existing is not None:
                    if existing["tenant_id"] != resolved_tenant or existing["event_type"] != event_type or existing["correlation_id"] != correlation_id:
                        raise ValueError("Event idempotency key belongs to a different scope")
                    return self._event_from_row(existing)
            cursor = connection.execute(
                """
                insert into evolution_events (
                  correlation_id, event_type, payload, tenant_id, idempotency_key
                ) values (?, ?, ?, ?, ?)
                """,
                (
                    correlation_id,
                    event_type,
                    json.dumps(payload, ensure_ascii=False),
                    resolved_tenant,
                    idempotency_key,
                ),
            )
            row = connection.execute(
                "select * from evolution_events where event_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
        return self._event_from_row(row)

    @staticmethod
    def _read_tenant() -> str:
        identity = TenantContext.current_identity()
        tenant = TenantContext.current_tenant_id()
        if not tenant or identity.get("tenant_id") != tenant or not identity.get("subject_id"):
            raise PermissionError("Trusted tenant identity is required for event reads")
        return tenant

    def get_by_correlation_id(self, correlation_id: str) -> list[dict[str, Any]]:
        tenant = self._read_tenant()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from evolution_events where tenant_id = ? and correlation_id = ? order by event_id",
                (tenant, correlation_id),
            ).fetchall()
        return [self._event_from_row(row) for row in rows]

    def get_all(self) -> list[dict[str, Any]]:
        tenant = self._read_tenant()
        with self.database.connect() as connection:
            rows = connection.execute(
                "select * from evolution_events where tenant_id = ? order by event_id", (tenant,)
            ).fetchall()
        return [self._event_from_row(row) for row in rows]

    def list_for_tenant(
        self,
        tenant_id: str,
        *,
        after_event_id: int = 0,
        event_types: set[str] | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        if not tenant_id:
            raise ValueError("tenant_id is required")
        params: list[Any] = [tenant_id, max(0, int(after_event_id))]
        sql = (
            "select * from evolution_events "
            "where tenant_id = ? and event_id > ?"
        )
        if event_types:
            values = sorted(event_types)
            sql += f" and event_type in ({','.join('?' for _ in values)})"
            params.extend(values)
        sql += " order by event_id desc limit ?"
        params.append(max(1, min(int(limit), 200)))
        with self.database.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._event_from_row(row) for row in reversed(rows)]

    def list_usage_events(
        self,
        tenant_id: str | None = None,
        capability_type: str | None = None,
        capability_source: str | None = None,
        model_gateway_id: str | None = None,
        model_name: str | None = None,
        status: str | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> list[dict[str, Any]]:
        params: list[Any] = []
        sql = "select * from evolution_events where event_type like 'usage.%'"
        if tenant_id:
            sql += " and tenant_id = ?"
            params.append(tenant_id)
        if capability_type is not None:
            sql += " and json_extract(payload, '$.capability_type') = ?"
            params.append(capability_type)
        if capability_source is not None:
            sql += " and json_extract(payload, '$.capability_source') = ?"
            params.append(capability_source)
        if model_gateway_id is not None:
            sql += " and json_extract(payload, '$.model_gateway_id') = ?"
            params.append(model_gateway_id)
        if model_name is not None:
            sql += " and json_extract(payload, '$.model_name') = ?"
            params.append(model_name)
        if status is not None:
            sql += " and json_extract(payload, '$.status') = ?"
            params.append(status)
        if since is not None:
            sql += " and created_at >= ?"
            params.append(since)
        if until is not None:
            sql += " and created_at <= ?"
            params.append(until)
        sql += " order by created_at desc"
        with self.database.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._usage_event_from_row(row) for row in rows]

    @staticmethod
    def _event_from_row(row: Any) -> dict[str, Any]:
        event = dict(row)
        event["payload"] = json.loads(event["payload"])
        return event

    @classmethod
    def _usage_event_from_row(cls, row: Any) -> dict[str, Any]:
        event = cls._event_from_row(row)
        payload = event["payload"]
        has_tokens = any(
            key in payload for key in ("prompt_tokens", "completion_tokens", "total_tokens", "token")
        )
        has_cost = "estimated_cost" in payload
        capability_ref = payload.get("capability_ref", {})
        capability_ref_source = (
            capability_ref.get("source", "official")
            if isinstance(capability_ref, dict)
            else "official"
        )
        return {
            **event,
            "id": payload.get("id") or str(event["event_id"]),
            "task_id": payload.get("task_id") or event["correlation_id"],
            "workflow_run_id": payload.get("workflow_run_id", ""),
            "workflow_step_id": payload.get("workflow_step_id", ""),
            "employee_id": payload.get("employee_id", ""),
            "employee_role": payload.get("employee_role", ""),
            "employee_name": payload.get("employee_name", ""),
            "credential_id": payload.get("credential_id", ""),
            "credential_ref_digest": payload.get("credential_ref_digest", ""),
            "request_id": payload.get("request_id", ""),
            "subject_id": payload.get("subject_id", ""),
            "company_id": payload.get("company_id", ""),
            "project_id": payload.get("project_id", ""),
            "workflow_id": payload.get("workflow_id", ""),
            "capability_binding_id": payload.get("capability_binding_id", ""),
            "capability_type": payload.get("capability_type") or payload.get("scope_type", ""),
            "capability_id": payload.get("capability_id") or payload.get("scope_ref", ""),
            "capability_source": payload.get("capability_source") or capability_ref_source,
            "model_gateway_id": payload.get("model_gateway_id", ""),
            "model_name": payload.get("model_name", ""),
            "provider_id": payload.get("provider_id", ""),
            "prompt_tokens": int(payload.get("prompt_tokens", 0) or 0) if has_tokens else None,
            "completion_tokens": int(payload.get("completion_tokens", 0) or 0) if has_tokens else None,
            "total_tokens": int(payload.get("total_tokens", payload.get("token", 0)) or 0)
            if has_tokens else None,
            "token_usage": payload.get("token_usage") or ({
                "prompt_tokens": int(payload.get("prompt_tokens", 0) or 0),
                "completion_tokens": int(payload.get("completion_tokens", 0) or 0),
                "total_tokens": int(payload.get("total_tokens", payload.get("token", 0)) or 0),
            } if has_tokens else None),
            "estimated_cost": float(payload.get("estimated_cost", 0) or 0) if has_cost else None,
            "cost_metadata": payload.get("cost_metadata") or ({
                "estimated_cost": float(payload.get("estimated_cost", 0) or 0),
                "currency": payload.get("currency", "USD"),
                "cost_source": payload.get("cost_source", "legacy_usage_event"),
            } if has_cost else None),
            "status": payload.get("status", ""),
            "http_status": int(payload.get("http_status", 0) or 0),
            "latency_ms": int(payload.get("latency_ms", 0) or 0),
            "outbound_attempted": bool(payload.get("outbound_attempted", False)),
        }
