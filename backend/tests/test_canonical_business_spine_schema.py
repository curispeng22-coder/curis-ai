from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import pytest

from app.database import Database


TENANT = "tenant-business-spine"
COMPANY = "company-business-spine"
DEPARTMENT = "department-business-spine"
NOW = datetime.now(timezone.utc).isoformat()


def _database(path) -> Database:
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, 'ceo', 'Company', 'active')",
            (COMPANY, TENANT),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values (?, ?, ?, 'department-template', '研发部', 'RD')",
            (DEPARTMENT, TENANT, COMPANY),
        )
    return database


def _insert_business(connection, *, company_id=COMPANY, department_id=DEPARTMENT):
    connection.execute(
        "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, created_at, updated_at) "
        "values ('business-canonical', ?, ?, ?, 'Curis 产品研发', ?, ?)",
        (TENANT, company_id, department_id, NOW, NOW),
    )


def test_canonical_business_rejects_orphan_company_and_department(tmp_path) -> None:
    database = _database(tmp_path / "spine.sqlite")
    with pytest.raises(sqlite3.IntegrityError, match="company missing"):
        with database.connect() as connection:
            _insert_business(connection, company_id="company-missing")
    with pytest.raises(sqlite3.IntegrityError, match="department missing"):
        with database.connect() as connection:
            _insert_business(connection, department_id="department-missing")


def test_resolved_workspace_requires_canonical_business(tmp_path) -> None:
    database = _database(tmp_path / "spine.sqlite")
    with pytest.raises(sqlite3.IntegrityError, match="workspace business missing"):
        with database.connect() as connection:
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, "
                "business_relation_status) values ('workspace-orphan', ?, ?, 'business-missing', 'Workspace', "
                "'DRAFT', 'RESOLVED')",
                (TENANT, COMPANY),
            )

    with database.connect() as connection:
        _insert_business(connection)
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status, "
            "business_relation_status, business_relation_reason, business_relation_source) "
            "values ('workspace-resolved', ?, ?, 'business-canonical', 'Workspace', 'DRAFT', "
            "'RESOLVED', '', 'CANONICAL')",
            (TENANT, COMPANY),
        )
        row = connection.execute(
            "select business_relation_status from workspaces where workspace_id='workspace-resolved'"
        ).fetchone()
    assert row["business_relation_status"] == "RESOLVED"


def test_legacy_workspace_is_additively_unresolved(tmp_path) -> None:
    database = _database(tmp_path / "spine.sqlite")
    with database.connect() as connection:
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status) "
            "values ('workspace-legacy', ?, ?, 'free-form-legacy', 'Legacy', 'DRAFT')",
            (TENANT, COMPANY),
        )
        row = connection.execute(
            "select business_relation_status, business_relation_source from workspaces "
            "where workspace_id='workspace-legacy'"
        ).fetchone()
    assert dict(row) == {"business_relation_status": "UNRESOLVED", "business_relation_source": "LEGACY"}
