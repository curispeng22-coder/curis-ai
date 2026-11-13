from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from .database import Database
from .resource_scope_policy import ResourceScopePolicy
from .tenant_context import TenantContext


_GROUP_FIELDS = {
    "day": "day",
    "model": "model_name",
    "employee": "employee_id",
    "capability": "capability_id",
    "task": "task_id",
    "project": "project_id",
    "business_department": "department_id",
    "company": "company_id",
    "business": "business_id",
    "workspace": "workspace_id",
    "work": "work_ref",
    "execution": "execution_ref",
    "conversation": "conversation_ref",
    "canonical_employee": "canonical_employee_ref",
}
_SUCCESS_STATUSES = {"success", "succeeded", "completed"}


class AIUsageService:
    """Trusted append-only ledger for actual model-provider call attempts."""

    def __init__(self, database: Database):
        self.database = database

    def record_call(
        self,
        *,
        tenant_id: str,
        model_gateway_id: str,
        provider_id: str,
        model_name: str,
        input_tokens: int | None,
        output_tokens: int | None,
        total_tokens: int | None,
        cost_amount: Decimal | str | int | None,
        currency: str,
        cost_source: str,
        price_version: str | None,
        employee_id: str,
        capability_id: str,
        capability_type: str,
        task_id: str,
        project_id: str | None,
        department_id: str | None,
        request_id: str,
        execution_status: str,
        metering_status: str,
        idempotency_key: str,
        occurred_at: datetime | str | None = None,
        cache_read_tokens: int | None = None,
        cache_write_tokens: int | None = None,
        reasoning_tokens: int | None = None,
        latency_ms: int | None = None,
        workflow_run_id: str | None = None,
        workflow_step_id: str | None = None,
        capability_binding_id: str | None = None,
        logical_call_id: str | None = None,
        attempt_no: int | None = None,
        fallback_from_model: str | None = None,
        fallback_reason: str | None = None,
        http_status: int | None = None,
    ) -> str:
        active_tenant = TenantContext.current_tenant_id().strip()
        if not active_tenant or not tenant_id or tenant_id != active_tenant:
            raise PermissionError("tenant scope mismatch")
        if not idempotency_key.strip():
            raise ValueError("idempotency_key is required")

        with self.database.connect() as connection:
            existing = connection.execute(
                "select usage_record_id, tenant_id from ai_usage_records where idempotency_key = ?",
                (idempotency_key,),
            ).fetchone()
            if existing is not None:
                if existing["tenant_id"] != tenant_id:
                    raise PermissionError("tenant scope mismatch")
                return str(existing["usage_record_id"])

        required = {
            "model_gateway_id": model_gateway_id,
            "provider_id": provider_id,
            "model_name": model_name,
            "currency": currency,
            "employee_id": employee_id,
            "capability_id": capability_id,
            "task_id": task_id,
            "request_id": request_id,
            "execution_status": execution_status,
        }
        missing = [name for name, value in required.items() if not str(value or "").strip()]
        if missing:
            raise ValueError(f"{', '.join(missing)} required")
        if capability_type not in {"model", "agent", "tool", "connector"}:
            raise ValueError("invalid capability_type")
        if metering_status not in {"confirmed", "unknown"}:
            raise ValueError("invalid metering_status")
        if cost_source not in {"unknown", "estimated", "provider_reported"}:
            raise ValueError("invalid cost_source")

        token_values = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cache_read_tokens": cache_read_tokens,
            "cache_write_tokens": cache_write_tokens,
            "reasoning_tokens": reasoning_tokens,
        }
        for name, value in token_values.items():
            if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
                raise ValueError(f"{name} must be a non-negative integer or null")
        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens
        if metering_status == "unknown":
            if any(value is not None for value in (input_tokens, output_tokens, total_tokens)):
                raise ValueError("unknown metering must not contain confirmed token totals")
        elif total_tokens is None:
            raise ValueError("confirmed metering requires total_tokens")

        cost = self._decimal(cost_amount)
        if cost is not None and (not cost.is_finite() or cost < 0):
            raise ValueError("cost_amount must be a finite non-negative decimal")
        if cost is None and cost_source != "unknown":
            raise ValueError("unknown cost must use cost_source=unknown")
        if cost is not None and cost_source == "unknown":
            raise ValueError("known cost requires a known cost_source")
        if cost_source == "estimated" and not str(price_version or "").strip():
            raise ValueError("estimated cost requires price_version")
        if latency_ms is not None and latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        if attempt_no is not None and attempt_no < 1:
            raise ValueError("attempt_no must be positive")
        if http_status is not None and http_status < 0:
            raise ValueError("http_status must be non-negative")

        occurred = self._utc_timestamp(occurred_at)
        usage_record_id = f"usage-{uuid.uuid4()}"
        with self.database.connect() as connection:
            attribution = self._validate_lineage(
                connection,
                tenant_id=tenant_id,
                employee_id=employee_id,
                capability_id=capability_id,
                capability_type=capability_type,
                task_id=task_id,
                project_id=project_id,
                department_id=department_id,
                capability_binding_id=capability_binding_id,
            )
            try:
                connection.execute(
                    """
                    insert into ai_usage_records (
                      usage_record_id, tenant_id, company_id, model_gateway_id, provider_id, model_name,
                      input_tokens, output_tokens, total_tokens, cost_amount, currency,
                      cost_source, price_version, employee_id, capability_id, capability_type,
                      task_id, project_id, department_id, business_id, workspace_id,
                      work_ref, execution_ref, request_id, execution_status,
                      metering_status, occurred_at, idempotency_key, cache_read_tokens,
                      cache_write_tokens, reasoning_tokens, latency_ms, workflow_run_id,
                      workflow_step_id, capability_binding_id, logical_call_id, attempt_no,
                      fallback_from_model, fallback_reason, http_status,
                      conversation_ref, canonical_employee_ref, scope_type, scope_ref
                    ) values (
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        usage_record_id,
                        tenant_id,
                        attribution["company_id"],
                        model_gateway_id,
                        provider_id,
                        model_name,
                        input_tokens,
                        output_tokens,
                        total_tokens,
                        None if cost is None else format(cost, "f"),
                        currency.upper(),
                        cost_source,
                        price_version or None,
                        employee_id,
                        capability_id,
                        capability_type,
                        task_id,
                        attribution["project_id"],
                        attribution["department_id"],
                        attribution["business_id"],
                        attribution["workspace_id"],
                        attribution["work_ref"],
                        attribution["execution_ref"],
                        request_id,
                        execution_status,
                        metering_status,
                        occurred,
                        idempotency_key,
                        cache_read_tokens,
                        cache_write_tokens,
                        reasoning_tokens,
                        latency_ms,
                        workflow_run_id or None,
                        workflow_step_id or None,
                        capability_binding_id or None,
                        logical_call_id or None,
                        attempt_no,
                        fallback_from_model or None,
                        fallback_reason or None,
                        http_status,
                        attribution.get("conversation_ref"),
                        attribution.get("canonical_employee_ref"),
                        attribution.get("scope_type"),
                        attribution.get("scope_ref"),
                    ),
                )
            except sqlite3.IntegrityError:
                existing = connection.execute(
                    "select usage_record_id, tenant_id from ai_usage_records where idempotency_key = ?",
                    (idempotency_key,),
                ).fetchone()
                if existing is None or existing["tenant_id"] != tenant_id:
                    raise
                return str(existing["usage_record_id"])
        return usage_record_id

    def validate_business_context(
        self,
        *,
        tenant_id: str,
        employee_id: str,
        capability_id: str,
        capability_type: str,
        task_id: str,
        project_id: str | None = None,
        department_id: str | None = None,
        capability_binding_id: str | None = None,
    ) -> dict[str, str | None]:
        if not tenant_id or tenant_id != self._tenant():
            raise PermissionError("tenant scope mismatch")
        with self.database.connect() as connection:
            return self._validate_lineage(
                connection,
                tenant_id=tenant_id,
                employee_id=employee_id,
                capability_id=capability_id,
                capability_type=capability_type,
                task_id=task_id,
                project_id=project_id,
                department_id=department_id,
                capability_binding_id=capability_binding_id,
            )

    def get_record(self, usage_record_id: str) -> dict[str, Any]:
        tenant_id = self._tenant()
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from ai_usage_records where tenant_id = ? and usage_record_id = ?",
                (tenant_id, usage_record_id),
            ).fetchone()
        if row is None:
            raise KeyError("usage record not found")
        return self._record(row)

    def list_records(
        self,
        *,
        since: str | None = None,
        until: str | None = None,
        model: str | None = None,
        employee_id: str | None = None,
        capability_id: str | None = None,
        task_id: str | None = None,
        project_id: str | None = None,
        department_id: str | None = None,
        company_id: str | None = None,
        business_id: str | None = None,
        workspace_id: str | None = None,
        work_ref: str | None = None,
        execution_ref: str | None = None,
        conversation_ref: str | None = None,
        canonical_employee_ref: str | None = None,
        execution_status: str | None = None,
        metering_status: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        return self._query(
            since=since,
            until=until,
            model=model,
            employee_id=employee_id,
            capability_id=capability_id,
            task_id=task_id,
            project_id=project_id,
            department_id=department_id,
            company_id=company_id,
            business_id=business_id,
            workspace_id=workspace_id,
            work_ref=work_ref,
            execution_ref=execution_ref,
            conversation_ref=conversation_ref,
            canonical_employee_ref=canonical_employee_ref,
            execution_status=execution_status,
            metering_status=metering_status,
            limit=max(1, min(limit, 1000)),
        )

    def aggregate(self, *, group_by: str | None = None, **filters: Any) -> dict[str, Any]:
        if group_by is not None and group_by not in _GROUP_FIELDS:
            raise ValueError("invalid group_by")
        records = self._query(**filters, limit=None)
        result = {"tenant_id": self._tenant(), "totals": self._totals(records)}
        if group_by:
            buckets: dict[str, list[dict[str, Any]]] = {}
            field = _GROUP_FIELDS[group_by]
            for record in records:
                key = str(record["occurred_at"])[:10] if field == "day" else str(record[field])
                buckets.setdefault(key, []).append(record)
            result["group_by"] = group_by
            result["groups"] = [
                {"key": key, **self._totals(items)}
                for key, items in sorted(buckets.items())
            ]
        return result

    def _query(self, *, limit: int | None = None, **filters: Any) -> list[dict[str, Any]]:
        tenant_id = self._tenant()
        sql = "select * from ai_usage_records where tenant_id = ?"
        params: list[Any] = [tenant_id]
        fields = {
            "model": "model_name",
            "employee_id": "employee_id",
            "capability_id": "capability_id",
            "task_id": "task_id",
            "project_id": "project_id",
            "department_id": "department_id",
            "company_id": "company_id",
            "business_id": "business_id",
            "workspace_id": "workspace_id",
            "work_ref": "work_ref",
            "execution_ref": "execution_ref",
            "conversation_ref": "conversation_ref",
            "canonical_employee_ref": "canonical_employee_ref",
            "execution_status": "execution_status",
            "metering_status": "metering_status",
        }
        for key, column in fields.items():
            value = filters.get(key)
            if value is not None:
                sql += f" and {column} = ?"
                params.append(value)
        for key, operator in (("since", ">="), ("until", "<=")):
            value = filters.get(key)
            if value is not None:
                sql += f" and occurred_at {operator} ?"
                params.append(self._utc_timestamp(value))
        sql += " order by occurred_at desc, created_at desc, usage_record_id desc"
        if limit is not None:
            sql += " limit ?"
            params.append(limit)
        with self.database.connect() as connection:
            rows = connection.execute(sql, params).fetchall()
        return [self._record(row) for row in rows]

    @staticmethod
    def _totals(records: list[dict[str, Any]]) -> dict[str, Any]:
        def token_sum(name: str) -> int | None:
            values = [record[name] for record in records if record[name] is not None]
            return sum(values) if values else None

        def cost_sum(source: str) -> str | None:
            values = [
                Decimal(record["cost_amount"])
                for record in records
                if record["cost_source"] == source and record["cost_amount"] is not None
            ]
            return format(sum(values, Decimal("0")), "f") if values else None

        return {
            "call_count": len(records),
            "input_tokens": token_sum("input_tokens"),
            "output_tokens": token_sum("output_tokens"),
            "total_tokens": token_sum("total_tokens"),
            "confirmed_cost": cost_sum("provider_reported"),
            "estimated_cost": cost_sum("estimated"),
            "unmetered_count": sum(record["metering_status"] == "unknown" for record in records),
            "success_count": sum(record["execution_status"] in _SUCCESS_STATUSES for record in records),
            "failed_count": sum(record["execution_status"] not in _SUCCESS_STATUSES for record in records),
        }

    @staticmethod
    def _validate_lineage(
        connection: sqlite3.Connection,
        *,
        tenant_id: str,
        employee_id: str,
        capability_id: str,
        capability_type: str,
        task_id: str,
        project_id: str | None,
        department_id: str | None,
        capability_binding_id: str | None,
    ) -> dict[str, str | None]:
        task = connection.execute(
            "select tenant_id, company_id, project_id, workspace_id, work_ref, execution_ref, scope_type, scope_ref, "
            "employee_id, requested_capability_source, requested_capability_type, "
            "requested_capability_id from tasks "
            "where tenant_id = ? and task_id = ?",
            (tenant_id, task_id),
        ).fetchone()
        if task is None:
            raise KeyError("usage lineage resource not found")
        if task["scope_type"] or task["scope_ref"]:
            scope = ResourceScopePolicy.execution_scope_from_record(
                connection, tenant_id=tenant_id, record=dict(task),
            )
        employee = connection.execute(
            "select tenant_id, company_id, department_id from employee_instances "
            "where tenant_id = ? and id = ? and deleted_at is null",
            (tenant_id, employee_id),
        ).fetchone()
        if employee is None:
            raise KeyError("usage lineage resource not found")
        if task["employee_id"] and task["employee_id"] != employee_id:
            raise ValueError("usage lineage mismatch")

        conversation_bound = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='conversation.execution_bound'",
            (tenant_id, task_id),
        ).fetchall()
        if conversation_bound:
            attribution = AIUsageService._validate_conversation_lineage(
                connection, tenant_id, dict(task), task_id, employee_id,
                capability_id, capability_binding_id, conversation_bound,
            )
            if project_id or (department_id and department_id != attribution["department_id"]):
                raise ValueError("Conversation attribution conflicts with requested domain scope")
        elif task["workspace_id"] or task["scope_type"]:
            attribution = AIUsageService._validate_canonical_lineage(
                connection,
                tenant_id=tenant_id,
                task=dict(task),
                employee_id=employee_id,
                task_id=task_id,
                project_id=project_id,
                department_id=department_id,
                capability_id=capability_id,
                capability_type=capability_type,
                capability_binding_id=capability_binding_id,
            )
        else:
            attribution = AIUsageService._validate_legacy_lineage(
                connection,
                tenant_id=tenant_id,
                task=dict(task),
                employee=dict(employee),
                project_id=project_id,
                department_id=department_id,
            )
        if employee["company_id"] != attribution["company_id"]:
            raise ValueError("usage lineage mismatch")

        source = str(task["requested_capability_source"] or "")
        if task["requested_capability_type"] and task["requested_capability_type"] != capability_type:
            raise ValueError("capability binding mismatch")
        if task["requested_capability_id"] and task["requested_capability_id"] != capability_id:
            raise ValueError("capability binding mismatch")
        if source == "official" or not source:
            capability = connection.execute(
                "select 1 from official_models where model_key = ? and type = ? and status = 'active'",
                (capability_id, capability_type),
            ).fetchone()
        else:
            capability = None
        if source == "tenant_private" or (not source and capability is None):
            capability = connection.execute(
                "select 1 from tenant_private_capabilities "
                "where tenant_id = ? and capability_id = ? and capability_type = ? and status = 'active'",
                (tenant_id, capability_id, capability_type),
            ).fetchone()
        binding_sql = (
            "select 1 from employee_capability_bindings "
            "where tenant_id = ? and employee_id = ? "
            "and capability_id = ? and capability_type = ? and enabled = 1"
        )
        binding_params: list[Any] = [
            tenant_id,
            employee_id,
            capability_id,
            capability_type,
        ]
        if source:
            binding_sql += " and capability_source = ?"
            binding_params.append(source)
        if capability_binding_id:
            binding_sql += " and id = ?"
            binding_params.append(capability_binding_id)
        binding = connection.execute(binding_sql, binding_params).fetchone()
        if capability_binding_id and binding is None:
            raise ValueError("capability binding mismatch")
        if capability is None and binding is None:
            raise KeyError("capability not found")
        if (task["workspace_id"] or task["scope_type"]) and binding is None:
            raise ValueError("canonical execution requires an active capability binding")
        return attribution

    @staticmethod
    def _validate_conversation_lineage(connection, tenant_id, task, task_id, employee_id,
                                      capability_id, binding_id, records):
        """A conversation is a valid execution origin, not a synthetic Work."""
        columns = {row["name"] for row in connection.execute("pragma table_info(ai_usage_records)")}
        if not {"conversation_ref", "canonical_employee_ref"}.issubset(columns):
            raise ValueError("Conversation-origin usage ledger schema is not supported")
        if len(records) != 1 or task.get("project_id"):
            raise ValueError("Conversation execution origin is ambiguous")
        event = json.loads(records[0]["payload"])
        context = event.get("context") or {}
        work_ref = task.get("work_ref")
        if work_ref:
            selected = event.get("execution_selection") or {}
            kind = {"WRITING_CHAPTER_REPLY": "writing", "CG_GRAPHIC_REPLY": "content-growth",
                    "CG_CONTENT_REPLY": "content-growth", "MUSIC_SONG_REPLY": "music"}.get(selected.get("purpose"))
            if (not kind or selected.get("work_ref") != work_ref
                    or task.get("requested_capability_type") != "model"):
                raise ValueError("Only explicit saved business Work may have dual execution origins")
            # Both independent ownership chains must pass; neither replaces the other.
            AIUsageService._validate_canonical_lineage(connection, tenant_id=tenant_id, task=task,
                employee_id=employee_id, task_id=task_id, project_id=None, department_id=None,
                capability_id=capability_id, capability_type="model", capability_binding_id=binding_id)
            work = connection.execute("select data_json,parent_id from runtime_entities where tenant_id=? "
                "and entity_id=? and entity_type='WORK'", (tenant_id, work_ref)).fetchone()
            data = json.loads(work["data_json"])
            cycle = connection.execute("select data_json from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_id=? and entity_type='CYCLE'",
                (tenant_id, task["company_id"], task["workspace_id"], data.get("cycleRef"))).fetchone()
            contract = json.loads(cycle[0]).get("contract", {}) if cycle else {}
            source, model_binding = contract.get("modelSource", {}), contract.get("modelBinding", {})
            selected_scope = selected.get("scope") or {}
            model = selected.get("model") or {}
            if (not cycle or data.get("cycleRef") != work["parent_id"] or source.get("kind") != kind
                    or source.get("scope") != selected_scope or source.get("selection") != selected.get("selection")
                    or source.get("context") != context or selected.get("context") != context
                    or any(selected_scope.get(key) != value for key, value in {
                        "tenant_id": tenant_id, "company_id": task["company_id"], "workspace_id": task["workspace_id"]}.items())
                    or model_binding != {"bindingRef": binding_id, "model": model}
                    or model.get("model_key") != capability_id or model.get("source") != task.get("requested_capability_source")
                    or (kind == "writing" and (not selected_scope.get("book_ref") or not selected_scope.get("chapter_ref")))
                    or (kind == "content-growth" and (not selected.get("content_ref") or not selected.get("basis_version_ref")
                        or source.get("content_ref") != selected["content_ref"] or source.get("version_ref") != selected["basis_version_ref"]
                        or source.get("references") != selected.get("references")))
                    or (kind == "music" and (not selected.get("song_ref") or not selected.get("expected", {}).get("lyrics_ref")
                        or not selected.get("expected", {}).get("production_ref") or source.get("song_ref") != selected["song_ref"]
                        or source.get("expected") != selected["expected"] or source.get("references") != selected.get("references")))):
                raise ValueError("Work and Conversation source snapshots do not match")
        owner_rows = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? and event_type='conversation.opened'",
            (tenant_id, event.get("conversation_id")),
        ).fetchall()
        if len(owner_rows) != 1:
            raise ValueError("Conversation owner is unavailable")
        owner = json.loads(owner_rows[0]["payload"])
        joined = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='conversation.employee_joined' order by event_id desc limit 1",
            (tenant_id, event.get("conversation_id")),
        ).fetchone()
        if joined:
            participant = json.loads(joined["payload"])
            if participant.get("company_id") != task["company_id"] or participant.get("ceo_id") != owner["participants"][0]["ref"]:
                raise ValueError("Conversation participation scope mismatch")
            owner["participants"] = [owner["participants"][0], {"kind": "EMPLOYEE", "ref": participant.get("employee_ref")}]
        company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?",
                                     (tenant_id, task["company_id"])).fetchone()
        parent = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=tenant_id, record=task)
        authorized = ResourceScopePolicy.authorize_assignment(
            connection, tenant_id=tenant_id, company_id=task["company_id"],
            assignment_ref=context.get("assignment_ref"), employee_ref=event.get("employee_ref"),
            revision=context.get("assignment_revision"), scope=parent,
        )
        if context.get("scope_type"):
            ResourceScopePolicy.require_same_execution_scope(parent, context)
        assignment = connection.execute(
            "select data_json,lifecycle_status,workspace_id,company_id from runtime_entities where tenant_id=? "
            "and entity_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT'",
            (tenant_id, context.get("assignment_ref")),
        ).fetchone()
        data = json.loads(assignment["data_json"]) if assignment else {}
        identity_rows = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? and event_type='execution.identity_bound'",
            (tenant_id, task_id),
        ).fetchall()
        identity = json.loads(identity_rows[0]["payload"]) if len(identity_rows) == 1 else {}
        if task.get("scope_type"):
            ResourceScopePolicy.require_same_execution_scope(parent, {**identity, "tenant_id": tenant_id})
            if identity.get("assignment_ref") != authorized["assignment_ref"] or identity.get("assignment_revision") != authorized["assignment_revision"]:
                raise ValueError("Conversation identity Assignment provenance changed")
        if (not parent or not company or not assignment or assignment["lifecycle_status"] != "ACTIVE"
                or parent["company_id"] != task["company_id"] or assignment["company_id"] != task["company_id"]
                or assignment["workspace_id"] != task["workspace_id"] or context.get("workspace_id") != task["workspace_id"]
                or owner.get("company_id") != task["company_id"] or event.get("company_id") != task["company_id"]
                or owner.get("participants") != [{"kind": "CEO", "ref": company["ceo_id"]}, {"kind": "EMPLOYEE", "ref": event.get("employee_ref")}]
                or data.get("employeeRef") != event.get("employee_ref") or data.get("revision") != context.get("assignment_revision")
                or event.get("task_id") != task_id or event.get("attempt_id") != task.get("execution_ref")
                or event.get("company_employee_ref") != employee_id or identity.get("company_employee_ref") != employee_id
                or identity.get("runtime_employee_ref") != event.get("employee_ref")
                or identity.get("employee_capability_binding_ref") != event.get("binding_id")
                or (binding_id and event.get("binding_id") != binding_id)
                or event.get("capability_id") != capability_id or identity.get("capability_id") != capability_id):
            raise ValueError("Conversation execution ownership does not match current facts")
        return {"company_id": parent["company_id"], "department_id": parent["department_id"],
                "business_id": parent["business_id"], "workspace_id": task["workspace_id"],
                "work_ref": work_ref or None, "execution_ref": task["execution_ref"], "project_id": None,
                # The existing ledger has one primary origin; both verified proofs remain in task binding events.
                "conversation_ref": None if work_ref else event["conversation_id"],
                "canonical_employee_ref": None if work_ref else event["employee_ref"],
                "scope_type": parent["scope_type"], "scope_ref": parent["scope_ref"]}

    @staticmethod
    def _validate_legacy_lineage(
        connection: sqlite3.Connection,
        *,
        tenant_id: str,
        task: dict[str, Any],
        employee: dict[str, Any],
        project_id: str | None,
        department_id: str | None,
    ) -> dict[str, str | None]:
        task_project_id = str(task.get("project_id") or "")
        claimed_project_id = str(project_id or task_project_id)
        if not task_project_id or claimed_project_id != task_project_id:
            raise ValueError("usage lineage mismatch")
        project = connection.execute(
            "select company_id, department_id from projects where tenant_id=? and project_id=?",
            (tenant_id, task_project_id),
        ).fetchone()
        if project is None:
            raise KeyError("usage lineage resource not found")
        resolved_department = str(project["department_id"] or "")
        if department_id and department_id != resolved_department:
            raise ValueError("usage lineage mismatch")
        department = connection.execute(
            "select company_id from department_instances "
            "where tenant_id=? and id=? and deleted_at is null",
            (tenant_id, resolved_department),
        ).fetchone()
        if (
            department is None
            or task.get("company_id") != project["company_id"]
            or department["company_id"] != project["company_id"]
            or employee.get("company_id") != project["company_id"]
            or employee.get("department_id") != resolved_department
        ):
            raise ValueError("usage lineage mismatch")
        return {
            "company_id": str(project["company_id"]),
            "department_id": resolved_department,
            "business_id": None,
            "workspace_id": None,
            "work_ref": None,
            "execution_ref": None,
            "project_id": task_project_id,
        }

    @staticmethod
    def _validate_canonical_lineage(
        connection: sqlite3.Connection,
        *,
        tenant_id: str,
        task: dict[str, Any],
        employee_id: str,
        task_id: str,
        project_id: str | None,
        department_id: str | None,
        capability_id: str,
        capability_type: str,
        capability_binding_id: str | None,
    ) -> dict[str, str | None]:
        scope = ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=tenant_id, record=task)
        workspace_id = scope["workspace_id"]
        work_ref = str(task.get("work_ref") or "")
        execution_ref = str(task.get("execution_ref") or "")
        if not all((task.get("company_id"), work_ref, execution_ref)):
            raise ValueError("canonical usage lineage is incomplete")
        resolved_company = scope["company_id"]
        resolved_department = scope["department_id"]
        if department_id and department_id != resolved_department:
            raise ValueError("canonical usage lineage mismatch")
        work = connection.execute(
            "select company_id, workspace_id, data_json from runtime_entities "
            "where tenant_id=? and entity_id=? and entity_type='WORK'",
            (tenant_id, work_ref),
        ).fetchone()
        if work is None or work["company_id"] != resolved_company or work["workspace_id"] != workspace_id:
            raise ValueError("canonical work attribution mismatch")
        ResourceScopePolicy.require_same_execution_scope(
            scope, ResourceScopePolicy.execution_scope_from_record(connection, tenant_id=tenant_id, record=dict(work)),
        )
        try:
            routing = json.loads(work["data_json"] or "{}").get("responsibilityRouting") or {}
        except (TypeError, json.JSONDecodeError):
            routing = {}

        assignments = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='execution.identity_bound' order by event_id",
            (tenant_id, task_id),
        ).fetchall()
        execution_events = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='team.execution_task_bound' order by event_id",
            (tenant_id, work_ref),
        ).fetchall()
        matching_executions = []
        for event in execution_events:
            try:
                payload = json.loads(event["payload"] or "{}")
            except (TypeError, json.JSONDecodeError):
                continue
            if payload.get("task_ref") == task_id and payload.get("execution_key") == execution_ref:
                matching_executions.append(payload)
        if len(assignments) != 1 or len(matching_executions) != 1:
            raise ValueError("canonical execution provenance is not unique")
        try:
            assignment = json.loads(assignments[0]["payload"] or "{}")
            execution = matching_executions[0]
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("canonical execution provenance is invalid") from error
        if task.get("scope_type"):
            ResourceScopePolicy.require_same_execution_scope(scope, {**assignment, "tenant_id": tenant_id})
            ResourceScopePolicy.authorize_assignment(
                connection, tenant_id=tenant_id, company_id=resolved_company,
                assignment_ref=assignment.get("assignment_ref"), employee_ref=assignment.get("runtime_employee_ref"),
                revision=assignment.get("assignment_revision"), scope=scope,
            )
            claim = (routing.get("executions") or {}).get(execution_ref) or {}
            if (claim.get("assignmentRef") != assignment.get("assignment_ref")
                    or claim.get("employeeRef") != assignment.get("runtime_employee_ref")
                    or claim.get("taskRef") != task_id):
                raise ValueError("canonical Work Assignment changed")
        if (
            assignment.get("task_id") != task_id
            or assignment.get("company_id") != resolved_company
            or assignment.get("workspace_id") != workspace_id
            or assignment.get("company_employee_ref") != employee_id
            or assignment.get("capability_source") != task.get("requested_capability_source")
            or assignment.get("capability_id") != capability_id
            or assignment.get("capability_type") != capability_type
            or (
                capability_binding_id
                and assignment.get("employee_capability_binding_ref") != capability_binding_id
            )
            or (not task.get("scope_type") and routing.get("responsibilityHolderRef") != assignment.get("runtime_employee_ref"))
            or not routing.get("currentAssignmentRef")
            or execution.get("task_ref") != task_id
            or execution.get("work_ref") != work_ref
            or execution.get("execution_key") != execution_ref
        ):
            raise ValueError("canonical execution provenance mismatch")
        task_project_id = str(task.get("project_id") or "")
        if project_id and project_id != task_project_id:
            raise ValueError("canonical Project attribution conflicts with Task")
        if task_project_id:
            project = connection.execute(
                "select company_id, department_id from projects where tenant_id=? and project_id=?",
                (tenant_id, task_project_id),
            ).fetchone()
            if (
                project is None
                or project["company_id"] != resolved_company
                or project["department_id"] != resolved_department
            ):
                raise ValueError("canonical Project attribution conflicts with Workspace")
        return {
            "company_id": resolved_company,
            "department_id": resolved_department,
            "business_id": scope["business_id"],
            "workspace_id": workspace_id,
            "work_ref": work_ref,
            "execution_ref": execution_ref,
            "project_id": task_project_id or None,
            "scope_type": scope["scope_type"],
            "scope_ref": scope["scope_ref"],
        }

    @staticmethod
    def _record(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        record["source_type"] = "CONVERSATION" if record.get("conversation_ref") else "WORK" if record["work_ref"] else "LEGACY_PROJECT"
        record["source_ref"] = record.get("conversation_ref") or record["work_ref"] or record["project_id"]
        if record["cost_amount"] is not None:
            record["cost_amount"] = format(Decimal(str(record["cost_amount"])), "f")
        return record

    @staticmethod
    def _decimal(value: Decimal | str | int | None) -> Decimal | None:
        if value is None:
            return None
        if isinstance(value, bool) or isinstance(value, float):
            raise ValueError("cost_amount must use Decimal, string, integer, or null")
        try:
            return Decimal(str(value))
        except InvalidOperation as error:
            raise ValueError("invalid cost_amount") from error

    @staticmethod
    def _utc_timestamp(value: datetime | str | None) -> str:
        if value is None:
            parsed = datetime.now(timezone.utc)
        elif isinstance(value, datetime):
            parsed = value
        else:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as error:
                raise ValueError("invalid UTC timestamp") from error
        if parsed.tzinfo is None:
            raise ValueError("timestamp must include UTC offset")
        return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _tenant() -> str:
        tenant_id = TenantContext.current_tenant_id().strip()
        if not tenant_id:
            raise PermissionError("tenant_id is required")
        return tenant_id


def build_ai_usage_router(service: AIUsageService):
    from fastapi import APIRouter, HTTPException

    router = APIRouter()

    @router.get("/api/ai-usage/records")
    def list_ai_usage_records(
        since: str | None = None,
        until: str | None = None,
        model: str | None = None,
        employee_id: str | None = None,
        capability_id: str | None = None,
        task_id: str | None = None,
        project_id: str | None = None,
        department_id: str | None = None,
        company_id: str | None = None,
        business_id: str | None = None,
        workspace_id: str | None = None,
        work_ref: str | None = None,
        execution_ref: str | None = None,
        execution_status: str | None = None,
        metering_status: str | None = None,
        limit: int = 200,
    ):
        try:
            return {
                "tenant_id": service._tenant(),
                "records": service.list_records(
                    since=since,
                    until=until,
                    model=model,
                    employee_id=employee_id,
                    capability_id=capability_id,
                    task_id=task_id,
                    project_id=project_id,
                    department_id=department_id,
                    company_id=company_id,
                    business_id=business_id,
                    workspace_id=workspace_id,
                    work_ref=work_ref,
                    execution_ref=execution_ref,
                    execution_status=execution_status,
                    metering_status=metering_status,
                    limit=limit,
                ),
            }
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @router.get("/api/ai-usage/summary")
    def get_ai_usage_summary(
        since: str | None = None,
        until: str | None = None,
        model: str | None = None,
        employee_id: str | None = None,
        capability_id: str | None = None,
        task_id: str | None = None,
        project_id: str | None = None,
        department_id: str | None = None,
        company_id: str | None = None,
        business_id: str | None = None,
        workspace_id: str | None = None,
        work_ref: str | None = None,
        execution_ref: str | None = None,
        execution_status: str | None = None,
        metering_status: str | None = None,
        group_by: str | None = None,
    ):
        try:
            return service.aggregate(
                since=since,
                until=until,
                model=model,
                employee_id=employee_id,
                capability_id=capability_id,
                task_id=task_id,
                project_id=project_id,
                department_id=department_id,
                company_id=company_id,
                business_id=business_id,
                workspace_id=workspace_id,
                work_ref=work_ref,
                execution_ref=execution_ref,
                execution_status=execution_status,
                metering_status=metering_status,
                group_by=group_by,
            )
        except PermissionError as error:
            raise HTTPException(status_code=403, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router
