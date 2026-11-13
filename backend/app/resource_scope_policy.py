from __future__ import annotations


class ResourceScopePolicy:
    # One lineage vocabulary; optional domain objects (e.g. Project) are not parents.
    EXECUTION_SCOPES = {
        "COMPANY": ("companies", "company_id", None, None, "1=1"),
        "DEPARTMENT": ("department_instances", "id", "COMPANY", "company_id", "deleted_at is null"),
        "BUSINESS": ("canonical_businesses", "business_id", "DEPARTMENT", "department_id", "lifecycle_status != 'ARCHIVED'"),
        "WORKSPACE": ("workspaces", "workspace_id", "BUSINESS", "business_id", "business_relation_status='RESOLVED'"),
    }
    RESOURCES = {
        "company": ("companies", "company_id"),
        "department": ("department_instances", "id"),
        "project": ("projects", "project_id"),
        "employee": ("employee_instances", "id"),
        "workflow": ("workflow_runs", "workflow_run_id"),
        "result": ("step_results", "step_result_id"),
        "usage": ("evolution_events", "event_id"),
    }
    PATH_RESOURCES = {
        "companies": "company",
        "departments": "department",
        "projects": "project",
        "employees": "employee",
        "workflows": "workflow",
    }

    def __init__(self, database):
        self.database = database

    @classmethod
    def resolve_execution_scope(cls, connection, *, tenant_id: str, company_id: str,
                                scope_type: str, scope_ref: str) -> dict:
        """Resolve ownership in the caller's transaction; never grants actor access.

        Callers must validate the current actor/Assignment and selected references.
        A parent lineage is not permission to hydrate all descendant resources.
        """
        kind = str(scope_type).upper()
        if kind not in cls.EXECUTION_SCOPES or not all((tenant_id, company_id, scope_ref)):
            raise ValueError("explicit canonical execution scope is required")
        result = dict(tenant_id=tenant_id, company_id=company_id, department_id=None,
                      business_id=None, workspace_id=None, scope_type=kind, scope_ref=scope_ref)
        current_kind, current_ref = kind, scope_ref
        while current_kind:
            table, key, parent_kind, parent_key, predicate = cls.EXECUTION_SCOPES[current_kind]
            row = connection.execute(
                f"select * from {table} where tenant_id=? and {key}=? and {predicate}",
                (tenant_id, current_ref),
            ).fetchone()
            if row is None or row["company_id"] != company_id:
                raise ValueError("execution scope is outside canonical Company lineage")
            result[f"{current_kind.lower()}_id"] = current_ref
            if parent_kind:
                current_ref = row[parent_key]
                if not current_ref:
                    raise ValueError("execution scope parent is unresolved")
            current_kind = parent_kind
        return result

    @classmethod
    def execution_scope_from_record(cls, connection, *, tenant_id: str, record: dict, _parents=()) -> dict:
        """Explicit scope, or proven legacy Workspace only; NULL is not Company."""
        import json

        data = record.get("data")
        if data is None:
            data = json.loads(record.get("data_json") or "{}")
        if not isinstance(data, dict) or (record.get("tenant_id") and record["tenant_id"] != tenant_id):
            raise ValueError("invalid execution scope record")
        for field, key in (("scope_type", "scopeType"), ("scope_ref", "scopeRef")):
            if record.get(field) and data.get(key) and record[field] != data[key]:
                raise ValueError("conflicting execution scope representations")
        kind = record.get("scope_type") or data.get("scopeType")
        ref = record.get("scope_ref") or data.get("scopeRef")
        workspace = record.get("workspace_id")
        if not kind and not ref and workspace:
            kind, ref = "WORKSPACE", workspace
        if not kind and not ref and not workspace and record.get("entity_type") in {
            "EVIDENCE", "OUTCOME", "ACCEPTANCE", "HANDOFF", "DECISION_PACKET",
        }:
            parent_id = record.get("parent_id")
            if not parent_id or parent_id in _parents or len(_parents) >= 8:
                raise ValueError("reference scope provenance is unresolved")
            parent = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? and entity_id=?",
                (tenant_id, record.get("company_id"), parent_id),
            ).fetchone()
            if parent is None:
                raise ValueError("reference parent is outside Company scope")
            return cls.execution_scope_from_record(connection, tenant_id=tenant_id, record=dict(parent),
                                                    _parents=(*_parents, parent_id))
        scope = cls.resolve_execution_scope(
            connection, tenant_id=tenant_id, company_id=record.get("company_id"),
            scope_type=kind, scope_ref=ref,
        )
        if workspace and scope["workspace_id"] != workspace:
            raise ValueError("execution scope conflicts with persisted Workspace provenance")
        return scope

    @classmethod
    def reference_scope(cls, connection, *, tenant_id, company_id, reference_id):
        if reference_id.startswith("task:"):
            row = connection.execute("select * from tasks where tenant_id=? and company_id=? and task_id=?",
                                     (tenant_id, company_id, reference_id[5:])).fetchone()
        else:
            row = connection.execute("select * from runtime_entities where tenant_id=? and company_id=? and entity_id=?",
                                     (tenant_id, company_id, reference_id)).fetchone()
            if row is None:
                row = connection.execute("select t.* from artifacts a join tasks t on t.tenant_id=a.tenant_id and t.task_id=a.task_id "
                    "where a.tenant_id=? and t.company_id=? and a.artifact_id=?", (tenant_id, company_id, reference_id)).fetchone()
        if row is None:
            raise ValueError("selected reference is missing or outside Company scope")
        return cls.execution_scope_from_record(connection, tenant_id=tenant_id, record=dict(row))

    @staticmethod
    def require_same_execution_scope(left: dict, right: dict) -> None:
        """Exact execution boundary, not inherited permission from Company membership."""
        keys = ("tenant_id", "company_id", "scope_type", "scope_ref")
        if any(not left.get(key) or left.get(key) != right.get(key) for key in keys):
            raise ValueError("execution scopes do not match")

    @classmethod
    def authorize_assignment(cls, connection, *, tenant_id, company_id, assignment_ref,
                             employee_ref, revision=None, scope=None):
        """Current Responsibility authorizes the Employee in one exact execution scope."""
        import json

        row = connection.execute(
            "select * from runtime_entities where tenant_id=? and company_id=? and entity_id=? "
            "and entity_type='RESPONSIBILITY_ASSIGNMENT' and lifecycle_status='ACTIVE'",
            (tenant_id, company_id, assignment_ref),
        ).fetchone()
        if row is None:
            raise ValueError("current Assignment is unavailable")
        assignment = dict(row)
        data = json.loads(assignment["data_json"])
        actual = cls.execution_scope_from_record(connection, tenant_id=tenant_id, record=assignment)
        if scope is not None:
            cls.require_same_execution_scope(actual, scope)
        if data.get("employeeRef") != employee_ref or (revision is not None and data.get("revision") != revision):
            raise ValueError("Assignment Employee or revision changed")
        for ref, kind in ((employee_ref, "AI_EMPLOYEE"), (data.get("roleRef"), "ROLE_SLOT")):
            member = connection.execute(
                "select workspace_id,lifecycle_status from runtime_entities where tenant_id=? "
                "and company_id=? and entity_id=? and entity_type=?",
                (tenant_id, company_id, ref, kind),
            ).fetchone()
            if member is None or member["workspace_id"] not in (None, actual["workspace_id"]):
                raise ValueError("Assignment participant is outside execution scope")
            if kind == "AI_EMPLOYEE" and member["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
                raise ValueError("Assignment Employee is unavailable")
        return {**actual, "assignment_ref": assignment_ref, "assignment_revision": data.get("revision"),
                "employee_ref": employee_ref, "role_ref": data.get("roleRef"),
                "responsibility": data.get("responsibility") or ""}

    @classmethod
    def bounded_lineage_context(cls, connection, scope):
        """Names and bounded goals only; no history, secrets or descendant hydration."""
        import json

        result = {}
        for kind, (table, key, _, _, _) in cls.EXECUTION_SCOPES.items():
            ref = scope.get(f"{kind.lower()}_id")
            if not ref:
                continue
            row = connection.execute(f"select * from {table} where tenant_id=? and {key}=?",
                                     (scope["tenant_id"], ref)).fetchone()
            if row is None:
                raise ValueError("scope context disappeared")
            row = dict(row)
            value = {"id": ref, "name": str(row.get("name") or "")[:160]}
            for field in ("goal", "positioning"):
                if row.get(field):
                    value[field] = str(row[field])[:800]
            if row.get("blueprint_json"):
                blueprint = json.loads(row["blueprint_json"])
                value["purpose"] = str(blueprint.get("purpose") or blueprint.get("goal") or blueprint.get("intentSummary") or "")[:800]
            result[kind.lower()] = value
        return result

    def owns(self, resource_type: str, resource_id: str, tenant_id: str) -> bool:
        table, id_column = self.RESOURCES[resource_type]
        with self.database.connect() as connection:
            return connection.execute(
                f"select 1 from {table} where {id_column} = ? and tenant_id = ?",
                (resource_id, tenant_id),
            ).fetchone() is not None

    def path_is_owned(self, path: str, tenant_id: str) -> bool:
        parts = [part for part in path.split("/") if part]
        if len(parts) < 4 or parts[:2] != ["api", "workspace"]:
            return True
        collection, resource_id = parts[2:4]
        if collection == "departments" and resource_id == "activation":
            return True
        resource_type = self.PATH_RESOURCES.get(collection)
        return not resource_type or self.owns(resource_type, resource_id, tenant_id)
