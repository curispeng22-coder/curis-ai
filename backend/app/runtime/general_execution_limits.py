"""Opt-in General limits over existing immutable Work/Task event receipts."""
from __future__ import annotations

import hashlib
import json
import os
import asyncio
from contextlib import contextmanager
from contextvars import ContextVar
from uuid import uuid4

from ..employee_execution_identity import EmployeeExecutionIdentity
from ..evolution_event_log import EvolutionEventLog
from ..model_gateway import ModelGatewayAdapter
from ..resource_scope_policy import ResourceScopePolicy
from ..tenant_context import TenantContext
from .foundation import RuntimeFoundation, RuntimeScopeError
from .general_workspace_delivery import GeneralWorkspaceDelivery

MARK = "general.execution_limits.bound"
RESERVE = "general.execution_task.reserved"
BIND = "general.execution_task.bound"
OUTBOUND = "general.outbound.claimed"
_command_owner = ContextVar("general_command_owner", default=None)


class GeneralLimitsError(RuntimeScopeError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize(value):
    if not isinstance(value, dict) or set(value) != {"max_prompt_bytes", "max_output_tokens"}:
        raise GeneralLimitsError("Invalid General execution limits")
    for key, ceiling in [("max_prompt_bytes", 4096), ("max_output_tokens", 2048)]:
        if type(value[key]) is not int or not 1 <= value[key] <= ceiling:
            raise GeneralLimitsError("General limits must be positive integers within their ceiling")
    return dict(value)


def event(db, kind, ref):
    # Locate the original mark before current lineage, even if ownership was moved.
    prefixes = {MARK: "general-limits:", RESERVE: "general-task-slot:", OUTBOUND: "general-outbound:"}
    with db.connect() as con:
        if kind in prefixes:
            rows = con.execute("select tenant_id, payload, event_type, correlation_id from evolution_events where idempotency_key=? or (event_type=? and correlation_id=?)", (prefixes[kind] + digest(ref), kind, ref)).fetchall()
        else:
            rows = con.execute("select tenant_id, payload, event_type, correlation_id from evolution_events where event_type=? and correlation_id=?", (kind, ref)).fetchall()
    if not rows:
        return None
    if len(rows) != 1:
        raise GeneralLimitsError("General execution receipt is ambiguous")
    if rows[0]["event_type"] != kind or rows[0]["correlation_id"] != ref:
        raise GeneralLimitsError("Original General receipt identity changed")
    try:
        value = json.loads(rows[0]["payload"])
        if not isinstance(value, dict) or value.get("tenant_id") != rows[0]["tenant_id"]:
            raise ValueError()
    except (ValueError, TypeError):
        raise GeneralLimitsError("General execution receipt is corrupt") from None
    return value


def snapshot(db, work_ref, limits):
    foundation = RuntimeFoundation(db)
    work = foundation.get(work_ref)
    if work["entity_type"] != "WORK" or not work.get("workspace_id"):
        raise GeneralLimitsError("Limited execution requires a canonical General Work")
    cycle = foundation.get(work.get("parent_id") or "")
    if (cycle["entity_type"] != "CYCLE" or cycle["data"].get("kind") != "GENERAL_WORK_CYCLE"
        or cycle["company_id"] != work["company_id"] or cycle["workspace_id"] != work["workspace_id"]):
        raise GeneralLimitsError("General Cycle lineage changed")
    workflow, assignment = GeneralWorkspaceDelivery(db)._resolve_assignment(work["company_id"], work["workspace_id"])
    data = workflow["data"]
    route = work["data"].get("responsibilityRouting") or {}
    if (len(data.get("defaultFlow") or []) != 1 or len(data.get("assignments") or []) != 1
        or route.get("workflowRef") != workflow["entity_id"] or route.get("workflowVersion") != data.get("version")
        or route.get("currentAssignmentRef") != assignment["assignmentRef"]
        or assignment.get("inputContract", {}).get("consultResponsibility") or route.get("collaborations")):
        raise GeneralLimitsError("Limited execution requires one primary responsibility without consultation")
    identity = EmployeeExecutionIdentity(db).resolve(company_id=work["company_id"], workspace_id=work["workspace_id"], runtime_employee_ref=assignment["employeeRef"])
    if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE":
        raise GeneralLimitsError("Limited execution requires an explicit Employee bridge")
    with db.connect() as con:
        scope = ResourceScopePolicy.execution_scope_from_record(con, tenant_id=TenantContext.current_tenant_id(), record=work)
        authorized = ResourceScopePolicy.authorize_assignment(con, tenant_id=scope["tenant_id"], company_id=work["company_id"], assignment_ref=assignment["assignmentRef"], employee_ref=assignment["employeeRef"], revision=assignment["assignmentRevision"], scope=scope)
        bindings = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? and enabled=1", (scope["tenant_id"], identity["company_employee_ref"])).fetchall()
        if len(bindings) != 1 or bindings[0]["capability_type"] != "model" or (identity.get("bridge") or {}).get("verifiedByEmployeeCapabilityBindingRef") != bindings[0]["id"]:
            raise GeneralLimitsError("Limited execution requires one current model binding")
        binding = dict(bindings[0])
        if binding["capability_source"] == "tenant_private":
            row = con.execute("select * from tenant_private_capabilities where tenant_id=? and capability_type='model' and capability_id=? and status='active'", (scope["tenant_id"], binding["capability_id"])).fetchone()
            if row is None:
                raise GeneralLimitsError("Model capability is unavailable")
            meta = json.loads(row["metadata_json"] or "{}")
            gateway, model = meta.get("provider_type"), meta.get("model_name")
            config = [str(meta.get("base_url") or "").rstrip("/"), meta.get("provider_protocol") or "openai_chat", meta.get("chat_path") or "/v1/chat/completions"]
        elif binding["capability_source"] == "official":
            row = con.execute("select * from official_models where model_key=? and status='active'", (binding["capability_id"],)).fetchone()
            if row is None:
                raise GeneralLimitsError("Model capability is unavailable")
            gateway, model = row["gateway_ref"], row["default_model"]
            config = None
        else:
            raise GeneralLimitsError("Unsupported model capability source")
    if not gateway or not model:
        raise GeneralLimitsError("Actual provider and model must be pinned")
    value = dict(version=1, tenant_id=scope["tenant_id"], company_id=work["company_id"], workspace_id=work["workspace_id"], work_ref=work_ref,
                 cycle_ref=cycle["entity_id"], workflow_ref=workflow["entity_id"], workflow_version=data["version"], assignment_ref=authorized["assignment_ref"], assignment_revision=assignment["assignmentRevision"],
                 assignment_contract_hash=digest({k: assignment.get(k) for k in ("responsibility", "inputContract", "outputContract")}),
                 employee_ref=assignment["employeeRef"], company_employee_ref=identity["company_employee_ref"], binding_ref=binding["id"], capability_source=binding["capability_source"], capability_id=binding["capability_id"],
                 gateway_id=gateway, model_id=model, adapter_profile=os.getenv("CURIS_MODEL_GATEWAY_PROFILE", "").strip(), config_hash=digest(config) if config else None, max_attempts=1, **normalize(limits))
    return value


def work_limits(db, work_ref):
    value = event(db, MARK, work_ref)
    if value is None:
        if event(db, RESERVE, work_ref) or event(db, OUTBOUND, work_ref):
            raise GeneralLimitsError("Original limited Work marker is missing")
        with db.connect() as con:
            bound = con.execute("select 1 from evolution_events where event_type=? and json_valid(payload) and json_extract(payload,'$.work_ref')=? limit 1", (BIND, work_ref)).fetchone()
        if bound:
            raise GeneralLimitsError("Original limited Work marker is missing")
        return None
    try:
        current = snapshot(db, work_ref, {k: value[k] for k in ["max_prompt_bytes", "max_output_tokens"]})
    except (KeyError, ValueError, TypeError) as error:
        raise GeneralLimitsError("Original limited Work is no longer valid") from error
    if value != current or value["tenant_id"] != TenantContext.current_tenant_id():
        raise GeneralLimitsError("Original limited Work scope, model, or revision changed")
    return value


def arm(db, work_ref, requested=None):
    original = work_limits(db, work_ref)
    if original is None and requested is None:
        return None
    identity = TenantContext.current_identity()
    if identity.get("role", "").lower() not in {"ceo", "owner"}:
        raise GeneralLimitsError("Only the current Company owner can select execution limits")
    value = original or snapshot(db, work_ref, normalize(requested))
    if identity.get("company_id") and identity["company_id"] != value["company_id"]:
        raise GeneralLimitsError("Limited Work belongs to another Company")
    if requested is not None and normalize(requested) != {k: value[k] for k in ["max_prompt_bytes", "max_output_tokens"]}:
        raise GeneralLimitsError("Original limits cannot be replaced")
    if original is None:
        work = RuntimeFoundation(db).get(work_ref)
        if work["lifecycle_status"] not in {"READY", "ACTIVE"} or (work["data"].get("responsibilityRouting") or {}).get("executions"):
            raise GeneralLimitsError("Select limits before any execution starts")
        recorded = EvolutionEventLog(db).record(correlation_id=work_ref, event_type=MARK, tenant_id=value["tenant_id"], idempotency_key="general-limits:" + digest(work_ref), payload=value)["payload"]
        if recorded != value:
            raise GeneralLimitsError("Original Work limit snapshot conflicts")
    if event(db, OUTBOUND, work_ref) or event(db, RESERVE, work_ref):
        raise GeneralLimitsError("Original limited attempt is held; reread its result, do not retry")
    return value


def reserve_task(db, work_ref, execution_key):
    value = work_limits(db, work_ref)
    if value is None:
        return None
    nonce = uuid4().hex
    claim = {"tenant_id": value["tenant_id"], "work_ref": work_ref, "limits_hash": digest(value), "execution_key": execution_key, "nonce": nonce}
    got = EvolutionEventLog(db).record(correlation_id=work_ref, event_type=RESERVE, tenant_id=value["tenant_id"], idempotency_key="general-task-slot:" + digest(work_ref), payload=claim)["payload"]
    if got != claim:
        raise GeneralLimitsError("Original limited Task is held; no replacement Task")
    return value


@contextmanager
def command_owner(db, work_ref, execution_key, executor):
    if _command_owner.get() is not None:
        raise GeneralLimitsError("Limited command cannot reenter its ownership scope")
    value = work_limits(db, work_ref)
    if value is None or not callable(executor):
        raise GeneralLimitsError("Limited command requires its internal execution callback")
    work = RuntimeFoundation(db).get(work_ref)
    route = work["data"].get("responsibilityRouting") or {}
    if (route.get("executions") or work["lifecycle_status"] not in {"READY", "ACTIVE"}
        or execution_key != f"responsibility:{work_ref}:{value['assignment_ref']}:1"):
        raise GeneralLimitsError("Limited command requires its original unstarted execution")
    reserve_task(db, work_ref, execution_key)
    # Durable nonce alone never authorizes submit; only this live callback invocation does.
    owner = dict(database=db, executor=executor, invocation=asyncio.current_task(),
                 limits=value, reservation=event(db, RESERVE, work_ref), consumed=False)
    token = _command_owner.set(owner)
    try:
        yield
    finally:
        _command_owner.reset(token)


def consume_task_owner(db, work_ref, execution_key, executor):
    value = work_limits(db, work_ref)
    if value is None:
        return None
    owner = _command_owner.get()
    if (owner is None or owner["database"] is not db or owner["executor"] is not executor
        or owner["invocation"] is not asyncio.current_task() or owner["consumed"]
        or owner["limits"] != value):
        raise GeneralLimitsError("Limited submit has no unused internal command ownership")
    reserve = event(db, RESERVE, work_ref)
    work = RuntimeFoundation(db).get(work_ref)
    lease = (work["data"].get("responsibilityRouting") or {}).get("executions", {}).get(execution_key) or {}
    if (reserve != owner["reservation"] or reserve.get("limits_hash") != digest(value)
        or reserve.get("execution_key") != execution_key or event(db, OUTBOUND, work_ref)
        or lease.get("status") != "SUBMITTING" or lease.get("taskRef")
        or lease.get("employeeRef") != value["employee_ref"] or lease.get("assignmentRef") != value["assignment_ref"]):
        raise GeneralLimitsError("Limited command reservation or current lease changed")
    owner["consumed"] = True
    return value


def bind_task(db, limits, task_ref, execution_key):
    if limits is None:
        return
    reserve = event(db, RESERVE, limits["work_ref"])
    if not reserve or reserve.get("limits_hash") != digest(limits) or reserve.get("execution_key") != execution_key:
        raise GeneralLimitsError("Task reservation changed")
    claim = {"tenant_id": limits["tenant_id"], "work_ref": limits["work_ref"], "task_ref": task_ref, "execution_key": execution_key, "limits_hash": digest(limits)}
    result = EvolutionEventLog(db).record(correlation_id=task_ref, event_type=BIND, tenant_id=limits["tenant_id"], idempotency_key="general-task-binding:" + digest(limits["work_ref"]), payload=claim)["payload"]
    if result != claim:
        raise GeneralLimitsError("Limited Task binding conflicts")


def task_limits(db, task_ref):
    bound = event(db, BIND, task_ref)
    with db.connect() as con:
        task = con.execute("select * from tasks where tenant_id=? and task_id=?", (TenantContext.current_tenant_id(), task_ref)).fetchone()
    if bound is None:
        if task and task["work_ref"] and event(db, MARK, task["work_ref"]):
            raise GeneralLimitsError("Limited Work has no trusted Task binding")
        return None
    if set(bound) != {"tenant_id", "work_ref", "task_ref", "execution_key", "limits_hash"}:
        raise GeneralLimitsError("Limited Task binding is corrupt")
    if task is None or bound.get("task_ref") != task_ref or bound.get("tenant_id") != TenantContext.current_tenant_id():
        raise GeneralLimitsError("Limited Task ownership changed")
    value = work_limits(db, bound.get("work_ref") or "")
    if value is None or bound.get("limits_hash") != digest(value):
        raise GeneralLimitsError("Limited Task marker is missing or corrupt")
    expected = dict(company_id=value["company_id"], workspace_id=value["workspace_id"], work_ref=value["work_ref"], execution_ref=bound["execution_key"], employee_id=value["company_employee_ref"],
                    requested_capability_source=value["capability_source"], requested_capability_type="model", requested_capability_id=value["capability_id"], scope_type="WORKSPACE", scope_ref=value["workspace_id"])
    if any(task[k] != v for k, v in expected.items()):
        raise GeneralLimitsError("Limited Task scope or model does not match its original binding")
    work = RuntimeFoundation(db).get(value["work_ref"])
    lease = (work["data"].get("responsibilityRouting") or {}).get("executions", {}).get(bound["execution_key"]) or {}
    if lease.get("taskRef") != task_ref or lease.get("employeeRef") != value["employee_ref"] or lease.get("assignmentRef") != value["assignment_ref"]:
        raise GeneralLimitsError("Current Work execution lease does not match")
    return value


def claim_outbound(db, task_ref, prompt, executor):
    limits = task_limits(db, task_ref)
    if limits is None:
        return None
    if not isinstance(executor, ModelGatewayAdapter) or executor.profile != limits["adapter_profile"]:
        raise GeneralLimitsError("Only the pinned model Adapter profile may execute limited Work")
    executor.validate_runtime_config()
    if (executor.gateway_id != limits["gateway_id"] or executor.model_name != limits["model_id"]
        or (limits["config_hash"] is not None and digest([executor.base_url, executor.protocol, executor.chat_path or "/v1/chat/completions"]) != limits["config_hash"])):
        raise GeneralLimitsError("Actual model transport changed")
    size = len(prompt.encode("utf-8"))
    if size > limits["max_prompt_bytes"]:
        raise GeneralLimitsError("Complete prompt exceeds the approved byte limit")
    nonce = uuid4().hex
    claim = {"tenant_id": limits["tenant_id"], "work_ref": limits["work_ref"], "task_ref": task_ref, "limits_hash": digest(limits), "nonce": nonce, "prompt_bytes": size, "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()}
    got = EvolutionEventLog(db).record(correlation_id=limits["work_ref"], event_type=OUTBOUND, tenant_id=limits["tenant_id"], idempotency_key="general-outbound:" + digest(limits["work_ref"]), payload=claim)["payload"]
    if got != claim:
        raise GeneralLimitsError("Original outbound attempt is held; its effect must be reconciled")
    return limits
