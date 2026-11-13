"""Read-only Organization Center projection over canonical Company OS truth."""

from __future__ import annotations

import json
from typing import Any

from .database import Database
from .employee_execution_identity import EmployeeExecutionIdentity
from .runtime import RuntimeScopeError
from .runtime.business_spine import CanonicalBusinessSpine
from .tenant_context import TenantContext


def department_assignments(database: Database, company_id: str) -> list[dict[str, Any]]:
    """Read current departmental holders; identity linkage is not Provider grant."""
    with database.connect() as connection:
        rows = connection.execute(
            "select a.*, e.id company_employee_id, r.data_json role_data from runtime_entities a "
            "join department_instances d on d.id=json_extract(a.data_json,'$.scopeRef') "
            "and d.tenant_id=a.tenant_id and d.company_id=a.company_id and d.deleted_at is null "
            "join runtime_entities p on p.entity_id=json_extract(a.data_json,'$.employeeRef') "
            "and p.entity_type='AI_EMPLOYEE' and p.tenant_id=a.tenant_id and p.company_id=a.company_id "
            "join employee_instances e on e.id=json_extract(p.data_json,'$.companyEmployeeRef') "
            "and e.tenant_id=a.tenant_id and e.company_id=a.company_id and e.enabled=1 and e.deleted_at is null "
            "join runtime_entities r on r.entity_id=json_extract(a.data_json,'$.roleRef') "
            "and r.entity_type='ROLE_SLOT' and r.tenant_id=a.tenant_id and r.company_id=a.company_id "
            "where a.tenant_id=? and a.company_id=? and a.entity_type='RESPONSIBILITY_ASSIGNMENT' "
            "and a.lifecycle_status='ACTIVE' and json_extract(a.data_json,'$.scopeType')='DEPARTMENT' "
            "order by a.entity_id",
            (TenantContext.current_tenant_id(), company_id),
        ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        data = json.loads(item.pop("data_json"))
        data["companyEmployeeRef"] = item.pop("company_employee_id")
        data["roleName"] = json.loads(item.pop("role_data")).get("name", "")
        item["data"] = data
        result.append(item)
    return result


def read_organization_projection(
    database: Database, businesses: CanonicalBusinessSpine, company_id: str,
) -> dict[str, Any]:
    """Compose existing records without becoming a write authority."""
    from .result_attention import ResultAttention
    ceo_id = ResultAttention(database).actor(company_id)
    tenant_id = TenantContext.current_tenant_id()
    with database.connect() as connection:
        company = connection.execute(
            "select company_id, name, description, status from companies "
            "where tenant_id=? and company_id=?",
            (tenant_id, company_id),
        ).fetchone()
        if company is None:
            raise RuntimeScopeError("Company is outside the active scope")
        departments = connection.execute(
            "select id, company_id, name, mission, status, manager_employee_id from department_instances "
            "where tenant_id=? and company_id=? and deleted_at is null order by created_at, id",
            (tenant_id, company_id),
        ).fetchall()
        employees = connection.execute(
            "select id, company_id, department_id, name, role, avatar_ref, status, enabled from employee_instances "
            "where tenant_id=? and company_id=? and deleted_at is null order by created_at, id",
            (tenant_id, company_id),
        ).fetchall()
        pending_proposals = connection.execute(
            "select ? company_id, r.entity_id founding_run_id, "
            "json_extract(r.data_json,'$.v1Proposal.business_name') business_name, r.lifecycle_status "
            "from runtime_entities r join department_instances d "
            "on d.id=json_extract(r.data_json,'$.v1Proposal.department_id') "
            "and d.tenant_id=r.tenant_id and d.company_id=? "
            "and d.deleted_at is null and d.enabled=1 and d.status!='archived' "
            "where r.tenant_id=? and r.entity_type='FOUNDING_RUN' and r.owner_ref=? "
            "and (r.company_id is null or r.company_id='' or r.company_id=?) "
            "and r.lifecycle_status='PROPOSED' and json_valid(r.data_json) "
            "and json_type(r.data_json,'$.firstBusiness') is null "
            "and json_type(r.data_json,'$.v1Activation') is null "
            "and json_extract(r.data_json,'$.v1Proposal.snapshot.company_id')=? "
            "and (json_extract(r.data_json,'$.v1Proposal.company_id') is null "
            "or json_extract(r.data_json,'$.v1Proposal.company_id')=?) "
            "and json_extract(r.data_json,'$.v1Proposal.snapshot.department_id')=d.id "
            "and json_type(r.data_json,'$.v1Proposal.business_name')='text' "
            "and length(trim(json_extract(r.data_json,'$.v1Proposal.business_name')))>0 "
            "and length(json_extract(r.data_json,'$.v1Proposal.proposal_sha256'))>0 "
            "and length(json_extract(r.data_json,'$.v1Proposal.package_id'))>0 "
            "and json_extract(r.data_json,'$.v1Proposal.package_id')="
            "json_extract(r.data_json,'$.v1Proposal.snapshot.definition.package_id') "
            "order by r.updated_at desc, r.entity_id limit 20",
            (company_id, company_id, tenant_id, ceo_id, company_id, company_id, company_id),
        ).fetchall()
        runtime_rows = {row["entity_id"]: dict(row) for row in connection.execute(
            "select * from runtime_entities where tenant_id=? and company_id=?",
            (tenant_id, company_id)).fetchall()}

    from .resource_scope_policy import ResourceScopePolicy
    employee_by_id = {row["id"]: dict(row) for row in employees}
    business_items = businesses.list_businesses(company_id)
    with database.connect() as connection:
        for business in business_items:
            team = []
            for row in runtime_rows.values():
                if row["entity_type"] != "RESPONSIBILITY_ASSIGNMENT" or row["lifecycle_status"] != "ACTIVE":
                    continue
                data = json.loads(row["data_json"] or "{}")
                kind, ref = data.get("scopeType"), data.get("scopeRef")
                if kind not in {"BUSINESS", "WORKSPACE"}:
                    continue
                try:
                    scope = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant_id,
                        company_id=company_id, scope_type=kind, scope_ref=ref)
                except ValueError:
                    continue
                if scope["business_id"] != business["business_id"] or row["workspace_id"] != scope["workspace_id"]:
                    continue
                member = {key: value for key, value in row.items() if key != "data_json"}
                data = dict(data)
                data.pop("companyEmployeeRef", None)
                data.pop("roleName", None)
                data["roleStatus"] = "MISSING"
                data["employeeIdentityStatus"] = "UNRESOLVED"
                runtime = runtime_rows.get(data.get("employeeRef"))
                role = runtime_rows.get(data.get("roleRef"))
                if role and role["entity_type"] == "ROLE_SLOT" and role["workspace_id"] in (None, scope["workspace_id"]):
                    data["roleName"] = json.loads(role["data_json"] or "{}").get("name", "")
                    data["roleStatus"] = role["lifecycle_status"]
                if runtime and runtime["entity_type"] == "AI_EMPLOYEE" and runtime["workspace_id"] in (None, scope["workspace_id"]):
                    identity = json.loads(runtime["data_json"] or "{}").get("companyEmployeeRef")
                    employee = employee_by_id.get(identity or runtime["entity_id"])
                    if employee:
                        data["companyEmployeeRef"] = employee["id"]
                        data["employeeIdentityStatus"] = "VERIFIED_EXPLICIT_BRIDGE" if identity else "EXACT_ID_FALLBACK"
                        data["employeeEnabled"] = bool(employee["enabled"] and runtime["lifecycle_status"] in {"AVAILABLE", "OPERATING"})
                        data["employeeStatus"] = employee["status"]
                member["data"] = data
                team.append(member)
            business["team"] = team
            records, conflicts = [], False
            for row in runtime_rows.values():
                if row["entity_type"] != "FOUNDING_RUN":
                    continue
                data = json.loads(row["data_json"] or "{}")
                first = data.get("firstBusiness") or {}
                if first.get("business_id") != business["business_id"]:
                    continue
                snapshot = (data.get("v1Proposal") or {}).get("snapshot") or {}
                proposal = data.get("v1Proposal") or {}
                activation = data.get("v1Activation") or {}
                initial_team = data.get("initialTeam") or {}
                try:
                    scope = ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant_id,
                        company_id=company_id, scope_type="WORKSPACE", scope_ref=first.get("workspace_id"))
                except ValueError:
                    conflicts = True
                    continue
                if (row["owner_ref"] != ceo_id or scope["business_id"] != business["business_id"]
                        or first.get("company_id", company_id) != company_id
                        or first.get("department_id", scope["department_id"]) != scope["department_id"]
                        or snapshot.get("company_id", company_id) != company_id
                        or proposal.get("company_id", company_id) != company_id
                        or snapshot.get("department_id", scope["department_id"]) != scope["department_id"]
                        or proposal.get("department_id", scope["department_id"]) != scope["department_id"]
                        or activation.get("company_id", company_id) != company_id
                        or (activation.get("snapshot") or {}).get("company_id", company_id) != company_id
                        or (activation.get("snapshot") or {}).get("department_id", scope["department_id"]) != scope["department_id"]
                        or initial_team.get("company_id", company_id) != company_id
                        or initial_team.get("businessRef", business["business_id"]) != business["business_id"]
                        or initial_team.get("workspaceRef", first.get("workspace_id")) != first.get("workspace_id")
                        or any(ref.get("scopeType") not in {"BUSINESS", "WORKSPACE"}
                            or ref.get("scopeRef") != (business["business_id"] if ref.get("scopeType") == "BUSINESS" else first.get("workspace_id"))
                            for ref in initial_team.get("assignments", []))):
                    conflicts = True
                    continue
                records.append({"company_id": company_id, "business_id": business["business_id"],
                    "workspace_id": first["workspace_id"], "founding_run_id": row["entity_id"]})
            business["creation_record"] = records[0] if len(records) == 1 and not conflicts else None
            business["creation_record_availability"] = "AVAILABLE" if business["creation_record"] else "AMBIGUOUS" if conflicts or len(records) > 1 else "NO_RECORD"

    return {
        "company": dict(company),
        "departments": [dict(row) for row in departments],
        "businesses": business_items,
        "pending_business_proposals": [dict(row) for row in pending_proposals],
        "employees": [dict(row) for row in employees],
        "departmentAssignments": department_assignments(database, company_id),
    }
