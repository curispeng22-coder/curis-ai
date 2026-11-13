"""Canonical Company -> Department -> Business -> Workspace relation service."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..database import Database
from ..tenant_context import TenantContext
from .workspace import WorkspaceRuntime


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class BusinessSpineError(ValueError):
    pass


class CanonicalBusinessSpine:
    def __init__(self, database: Database):
        self.db = database

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    @staticmethod
    def _name(value: str, label: str) -> str:
        value = value.strip()
        if not value or any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise BusinessSpineError(f"{label} is required")
        return value

    def _require_company_department(self, connection, company_id: str, department_id: str) -> tuple[dict, dict]:
        company = connection.execute(
            "select company_id, tenant_id, name, status from companies where tenant_id=? and company_id=?",
            (self.tenant_id, company_id),
        ).fetchone()
        if company is None:
            raise BusinessSpineError("Company is not in the current tenant")
        department = connection.execute(
            "select id, company_id, name, status from department_instances "
            "where tenant_id=? and company_id=? and id=? and deleted_at is null",
            (self.tenant_id, company_id, department_id),
        ).fetchone()
        if department is None:
            raise BusinessSpineError("Department is not in the current Company")
        return dict(company), dict(department)

    def create_draft_with_first_workspace(
        self,
        *,
        company_id: str,
        department_id: str,
        name: str,
        goal: str,
        positioning: str,
        workspace_name: str,
        business_type: str,
        blueprint_version: str,
        blueprint: dict[str, Any],
        business_id: str | None = None,
        workspace_id: str | None = None,
        version_id: str | None = None,
    ) -> dict[str, Any]:
        """Create DRAFT Business and first Workspace in one transaction."""

        business_id = business_id or f"business-{uuid4()}"
        workspace_id = workspace_id or f"workspace-{uuid4()}"
        version_id = version_id or f"workspace-version-{uuid4()}"
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            self._create_draft_with_first_workspace(
                connection,
                company_id=company_id,
                department_id=department_id,
                name=name,
                goal=goal,
                positioning=positioning,
                workspace_name=workspace_name,
                business_type=business_type,
                blueprint_version=blueprint_version,
                blueprint=blueprint,
                business_id=business_id,
                workspace_id=workspace_id,
                version_id=version_id,
            )
        return self.get_business(company_id, business_id)

    @staticmethod
    def _generic_blueprint(blueprint: dict[str, Any]) -> dict[str, Any]:
        forbidden = {"prompt", "apikey", "api_key", "credential", "secret", "rawpayload", "raw_payload"}

        def check(value: Any) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    if str(key).lower() in forbidden:
                        raise BusinessSpineError("Generic Workspace Blueprint cannot contain secrets or raw prompts")
                    check(item)
            elif isinstance(value, list):
                for item in value:
                    check(item)

        check(blueprint)
        return {**blueprint, "businessType": "GENERIC", "productForm": "GENERIC"}

    def _create_draft_with_first_workspace(
        self,
        connection,
        *,
        company_id: str,
        department_id: str,
        name: str,
        goal: str,
        positioning: str,
        workspace_name: str,
        business_type: str,
        blueprint_version: str,
        blueprint: dict[str, Any],
        business_id: str,
        workspace_id: str,
        version_id: str,
    ) -> None:
        business_name = self._name(name, "Business name")
        first_workspace_name = self._name(workspace_name, "Workspace name")
        if not all(value.strip() for value in (business_id, workspace_id, version_id, blueprint_version)):
            raise BusinessSpineError("Business, Workspace and version identity are required")
        kind = business_type.upper()
        snapshot = self._generic_blueprint(blueprint) if kind == "GENERIC" else WorkspaceRuntime._blueprint(
            WorkspaceRuntime._business_type(kind), blueprint,
        )
        if snapshot.get("lifecycleMode") == "STUDIO_DRAFT":
            raise BusinessSpineError("Atomic first Workspace cannot materialize proposed staffing")

        at = _now()
        self._require_company_department(connection, company_id, department_id)
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
            "lifecycle_status, goal, positioning, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, 'DRAFT', ?, ?, ?, ?)",
            (business_id, self.tenant_id, company_id, department_id, business_name,
             goal.strip(), positioning.strip(), at, at),
        )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
            "blueprint_version, operating_version, status, simulation_passed, business_relation_status, "
            "business_relation_reason, business_relation_owner, business_relation_source, "
            "business_relation_checked_at, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, ?, ?, 0, 'DRAFT', 0, 'RESOLVED', '', 'Business Spine', "
            "'CANONICAL_ATOMIC_CREATE', ?, ?, ?)",
            (workspace_id, self.tenant_id, company_id, business_id, first_workspace_name,
             json.dumps(snapshot, ensure_ascii=False), blueprint_version, at, at, at),
        )
        connection.execute(
            "insert into runtime_workspace_versions(version_id, tenant_id, company_id, workspace_id, "
            "blueprint_version, status, simulation_passed, operating_version, change_kind, data_json, "
            "created_at, updated_at) values (?, ?, ?, ?, ?, 'DRAFT', 0, 0, 'BUSINESS_ATOMIC_CREATE', ?, ?, ?)",
            (version_id, self.tenant_id, company_id, workspace_id, blueprint_version,
             json.dumps({"blueprint": snapshot, "changeReason": "canonical business first workspace"}, ensure_ascii=False), at, at),
        )

    def get_business(self, company_id: str, business_id: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            business = connection.execute(
                "select * from canonical_businesses where tenant_id=? and company_id=? and business_id=?",
                (self.tenant_id, company_id, business_id),
            ).fetchone()
            if business is None:
                raise BusinessSpineError("Business is not in the current Company")
            department = connection.execute(
                "select id, name, status from department_instances where tenant_id=? and company_id=? "
                "and id=? and deleted_at is null",
                (self.tenant_id, company_id, business["department_id"]),
            ).fetchone()
            company = connection.execute(
                "select company_id, name, status from companies where tenant_id=? and company_id=?",
                (self.tenant_id, company_id),
            ).fetchone()
            workspaces = connection.execute(
                "select workspace_id, name, status, case when json_valid(blueprint_json) then case when json_type(blueprint_json, '$.businessType')='text' then json_extract(blueprint_json, '$.businessType') end end as business_type, "
                "case when json_valid(blueprint_json) then case when json_type(blueprint_json, '$.packageId')='text' then json_extract(blueprint_json, '$.packageId') end end as package_id, "
                "case when json_valid(blueprint_json) then case when json_type(blueprint_json, '$.packageVersion')='text' then json_extract(blueprint_json, '$.packageVersion') end end as package_version, blueprint_version, operating_version, updated_at "
                "from workspaces where tenant_id=? and company_id=? and business_id=? "
                "and business_relation_status='RESOLVED' order by created_at, rowid",
                (self.tenant_id, company_id, business_id),
            ).fetchall()
            assignments = connection.execute(
                "select entity_id, owner_ref, lifecycle_status, data_json, updated_at from runtime_entities "
                "where tenant_id=? and company_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT' "
                "and json_extract(data_json, '$.scopeType')='BUSINESS' "
                "and json_extract(data_json, '$.scopeRef')=? order by created_at, entity_id",
                (self.tenant_id, company_id, business_id),
            ).fetchall()
            workspace_ids = [row["workspace_id"] for row in workspaces]
            waiting_count = 0
            if workspace_ids:
                marks = ",".join("?" for _ in workspace_ids)
                waiting_count = connection.execute(
                    f"select count(*) from runtime_entities where tenant_id=? and company_id=? "
                    f"and workspace_id in ({marks}) and lifecycle_status in ('WAITING_CEO','FAILED','BLOCKED')",
                    (self.tenant_id, company_id, *workspace_ids),
                ).fetchone()[0]

        from ..shared_workspace_projection import SharedWorkspaceProjection

        projection = SharedWorkspaceProjection(self.db)
        result_count = sum(len(projection.workspace(company_id, ref)["results"]) for ref in workspace_ids)
        item = dict(business)
        item["definition"] = {
            "businessId": item["business_id"], "name": item["name"], "goal": item["goal"],
            "positioning": item["positioning"], "lifecycleStatus": item["lifecycle_status"],
            "strategyDirectionRef": item["strategy_direction_ref"],
        }
        item["parentPath"] = {
            "company": dict(company) if company else None,
            "department": dict(department) if department else None,
            "business": {"business_id": item["business_id"], "name": item["name"]},
        }
        item["operatingSummary"] = {
            "workspaceCount": len(workspaces), "resultCount": result_count,
            "needsAttentionCount": waiting_count, "source": "DERIVED_FROM_WORKSPACE_RUNTIME",
            "freshness": item["updated_at"],
        }
        item["workspaces"] = [dict(row) for row in workspaces]
        item["team"] = [{**dict(row), "data": json.loads(row["data_json"])} for row in assignments]
        for member in item["team"]:
            member.pop("data_json", None)
        return item

    def list_businesses(self, company_id: str) -> list[dict[str, Any]]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "select business_id from canonical_businesses where tenant_id=? and company_id=? "
                "order by created_at, business_id",
                (self.tenant_id, company_id),
            ).fetchall()
        return [self.get_business(company_id, row["business_id"]) for row in rows]

    def resolve_workspace_parent(self, workspace_id: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            workspace = connection.execute(
                "select * from workspaces where tenant_id=? and workspace_id=?",
                (self.tenant_id, workspace_id),
            ).fetchone()
            if workspace is None:
                raise BusinessSpineError("Workspace is not in the current tenant")
            relation_status = workspace["business_relation_status"]
            if relation_status != "RESOLVED":
                return {
                    "workspaceId": workspace_id, "status": relation_status,
                    "reason": workspace["business_relation_reason"],
                    "owner": workspace["business_relation_owner"],
                    "source": workspace["business_relation_source"], "parentPath": None,
                }
            business = connection.execute(
                "select * from canonical_businesses where tenant_id=? and company_id=? and business_id=?",
                (self.tenant_id, workspace["company_id"], workspace["business_id"]),
            ).fetchone()
            if business is None:
                raise BusinessSpineError("Resolved Workspace has no canonical Business")
            department = connection.execute(
                "select id, name, status from department_instances where tenant_id=? and company_id=? "
                "and id=? and deleted_at is null",
                (self.tenant_id, workspace["company_id"], business["department_id"]),
            ).fetchone()
            company = connection.execute(
                "select company_id, name, status from companies where tenant_id=? and company_id=?",
                (self.tenant_id, workspace["company_id"]),
            ).fetchone()
            if department is None or company is None:
                raise BusinessSpineError("Canonical parent path is stale")
        return {
            "workspaceId": workspace_id, "status": "RESOLVED", "reason": "",
            "parentPath": {
                "company": dict(company), "department": dict(department),
                "business": {"business_id": business["business_id"], "name": business["name"]},
                "workspace": {"workspace_id": workspace["workspace_id"], "name": workspace["name"]},
            },
        }

    def quarantine_legacy_workspace(self, workspace_id: str, *, reason: str, owner: str) -> dict[str, Any]:
        if not reason.strip() or not owner.strip():
            raise BusinessSpineError("Quarantine reason and owner are required")
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select business_relation_status from workspaces where tenant_id=? and workspace_id=?",
                (self.tenant_id, workspace_id),
            ).fetchone()
            if row is None:
                raise BusinessSpineError("Workspace is not in the current tenant")
            if row["business_relation_status"] == "RESOLVED":
                raise BusinessSpineError("Resolved Workspace cannot be quarantined")
            connection.execute(
                "update workspaces set business_relation_status='QUARANTINED', business_relation_reason=?, "
                "business_relation_owner=?, business_relation_source='LEGACY_CLASSIFICATION', "
                "business_relation_checked_at=?, updated_at=? where tenant_id=? and workspace_id=?",
                (reason.strip(), owner.strip(), at, at, self.tenant_id, workspace_id),
            )
        return self.resolve_workspace_parent(workspace_id)
