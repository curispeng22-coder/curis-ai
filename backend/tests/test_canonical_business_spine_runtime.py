from __future__ import annotations

import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime.business_spine import CanonicalBusinessSpine
from app.tenant_context import TenantContext
from backend.tests.test_workspace_package_runtime_p0 import _write_package


TENANT = "tenant-canonical-spine-runtime"
CEO = "ceo-canonical-spine-runtime"
COMPANY = "company-canonical-spine-runtime"
DEPARTMENT = "department-canonical-spine-runtime"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO, "X-Role": "ceo"}


def blueprint(kind: str = "RD") -> dict:
    stages = (
        ["INTAKE", "DESIGN", "IMPLEMENT", "VERIFY", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE"]
        if kind == "RD"
        else ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"]
    )
    return {
        "stages": stages,
        "agentRefs": [f"agent-{kind.lower()}"],
        "capabilityRefs": [f"capability-{kind.lower()}"],
        "connectorRefs": [],
        "platformConstraints": {},
        "replyPolicy": "CEO_REVIEW",
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
        **({"platform": kind} if kind != "RD" else {}),
    }


def seed_company_department(path) -> Database:
    database = Database(str(path))
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, ?, 'Spine Company', 'active')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type) "
            "values (?, ?, ?, 'template-rd', '研发部', 'RD')",
            (DEPARTMENT, TENANT, COMPANY),
        )
    return database


def business_payload(*, business_id="business-canonical-rd") -> dict:
    return {
        "ceo_id": CEO,
        "department_id": DEPARTMENT,
        "business_id": business_id,
        "name": "Curis 产品研发",
        "goal": "持续交付可验收的 Curis 产品结果",
        "positioning": "Curis 自有产品研发业务",
        "workspace_name": "Curis 研发",
        "business_type": "RD",
        "blueprint_version": "v1",
        "blueprint": blueprint(),
    }


def test_atomic_business_first_workspace_parent_directory_and_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "canonical.sqlite"
    with TestClient(create_app(str(path))) as client:
        seed_company_department(path)
        created = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/businesses",
            headers=HEADERS,
            json=business_payload(),
        )
        assert created.status_code == 201, created.text
        business = created.json()
        assert business["department_id"] == DEPARTMENT
        assert len(business["workspaces"]) == 1
        first_workspace = business["workspaces"][0]

        parent = client.get(
            f"/api/workspace/runtime/foundation/workspaces/{first_workspace['workspace_id']}/parent-path",
            headers=HEADERS,
        )
        assert parent.status_code == 200
        assert parent.json()["parentPath"]["department"]["id"] == DEPARTMENT
        assert parent.json()["parentPath"]["business"]["business_id"] == business["business_id"]

        second = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "business_ref": business["business_id"],
                "business_type": "RD",
                "name": "Curis 研发二组",
                "blueprint_version": "v1",
                "blueprint": blueprint(),
            },
        )
        assert second.status_code == 201, second.text
        directory = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/businesses/{business['business_id']}",
            headers=HEADERS,
        ).json()
        assert [item["name"] for item in directory["workspaces"]] == ["Curis 研发", "Curis 研发二组"]
        assert directory["operatingSummary"]["workspaceCount"] == 2
        assert directory["operatingSummary"]["source"] == "DERIVED_FROM_WORKSPACE_RUNTIME"

    with TestClient(create_app(str(path))) as reopened:
        saved = reopened.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/businesses/business-canonical-rd",
            headers=HEADERS,
        )
        assert saved.status_code == 200, saved.text
        assert len(saved.json()["workspaces"]) == 2


def test_unknown_business_write_is_rejected_and_atomic_failure_rolls_back(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "failures.sqlite"
    with TestClient(create_app(str(path))) as client:
        database = seed_company_department(path)
        rejected = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-missing", "business_type": "RD",
                "name": "Orphan", "blueprint_version": "v1", "blueprint": blueprint(),
            },
        )
        assert rejected.status_code == 422

        with database.connect() as connection:
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, status) "
                "values ('workspace-fixed', ?, ?, 'legacy-ref', 'Collision', 'DRAFT')",
                (TENANT, COMPANY),
            )
        monkeypatch.setattr("app.runtime.business_spine.uuid4", lambda: "fixed")
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            with pytest.raises(sqlite3.IntegrityError):
                CanonicalBusinessSpine(database).create_draft_with_first_workspace(
                    company_id=COMPANY, department_id=DEPARTMENT, business_id="business-rollback",
                    name="Rollback", goal="", positioning="", workspace_name="Collision",
                    business_type="RD", blueprint_version="v1", blueprint=blueprint(),
                )
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from canonical_businesses where business_id='business-rollback'"
            ).fetchone()[0] == 0


def test_ambiguous_legacy_workspace_quarantines_and_cannot_operate(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "legacy.sqlite"
    with TestClient(create_app(str(path))) as client:
        database = seed_company_department(path)
        with database.connect() as connection:
            connection.execute(
                "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
                "blueprint_version, status) values ('workspace-legacy', ?, ?, 'ambiguous-ref', 'Legacy', ?, 'v1', 'DRAFT')",
                (TENANT, COMPANY, __import__("json").dumps({**blueprint(), "businessType": "RD"})),
            )
        unresolved = client.get(
            "/api/workspace/runtime/foundation/workspaces/workspace-legacy/parent-path", headers=HEADERS,
        )
        assert unresolved.status_code == 200
        assert unresolved.json()["status"] == "UNRESOLVED"
        assert unresolved.json()["parentPath"] is None

        quarantined = client.post(
            "/api/workspace/runtime/foundation/workspaces/workspace-legacy/business-relation/quarantine",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "多个 legacy source 无法唯一映射", "owner": "Business Spine Migration"},
        )
        assert quarantined.status_code == 200
        assert quarantined.json()["status"] == "QUARANTINED"

        blocked = client.post(
            "/api/workspace/runtime/foundation/workspaces/workspace-legacy/cycles",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "owner_ref": CEO, "outcome_ref": "none", "intent_ref": "none",
                "blueprint_version": "v1",
            },
        )
        assert blocked.status_code == 404


def test_generic_package_creates_canonical_business_and_first_workspace_atomically(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "generic.sqlite"
    source = tmp_path / "feedback-office"
    _write_package(source)
    with TestClient(create_app(str(path))) as client:
        database = seed_company_department(path)
        installed = client.post(
            "/api/workspace/packages/install",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "company_id": COMPANY,
                "department_id": DEPARTMENT,
                "business_id": "business-generic-feedback",
                "business_name": "客户反馈业务",
                "business_goal": "持续收集并闭环客户反馈",
                "business_positioning": "客户反馈经营空间",
                "source_path": str(source),
            },
        )
        assert installed.status_code == 201, installed.text
        workspace_id = installed.json()["instance"]["workspace_id"]
        business = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/businesses/business-generic-feedback",
            headers=HEADERS,
        )
        assert business.status_code == 200, business.text
        assert [item["workspace_id"] for item in business.json()["workspaces"]] == [workspace_id]
        parent = client.get(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/parent-path", headers=HEADERS,
        )
        assert parent.json()["parentPath"]["business"]["business_id"] == "business-generic-feedback"
        with database.connect() as connection:
            workspace = connection.execute(
                "select status, operating_version, business_relation_status from workspaces where workspace_id=?",
                (workspace_id,),
            ).fetchone()
            assert tuple(workspace) == ("DRAFT", 0, "RESOLVED")

        failed_source = tmp_path / "feedback-office-failure"
        _write_package(failed_source)
        manifest_path = failed_source / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["packageId"] = "com.example.test.feedback-lab-failure"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        failed = client.post(
            "/api/workspace/packages/install",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "company_id": COMPANY,
                "department_id": "department-missing",
                "business_id": "business-generic-rollback",
                "business_name": "应回滚业务",
                "source_path": str(failed_source),
            },
        )
        assert failed.status_code == 404
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from canonical_businesses where business_id='business-generic-rollback'"
            ).fetchone()[0] == 0


def test_directory_projects_exact_package_identity_without_bad_json_or_cross_tenant_leaks(tmp_path):
    path = tmp_path / 'directory.sqlite'
    with TestClient(create_app(str(path))) as client:
        db = seed_company_department(path)
        created = client.post(f'/api/workspace/runtime/foundation/companies/{COMPANY}/businesses', headers=HEADERS,
                              json=business_payload())
        assert created.status_code == 201, created.text
        original = created.json()['workspaces'][0]['workspace_id']
        with db.connect() as con:
            for workspace, tenant, raw in [('real', TENANT, json.dumps({'businessType': 'PACKAGE', 'packageId': 'com.curis.local.music', 'packageVersion': 'v1-exact'})),
                                           ('broken', TENANT, '{invalid'), ('foreign', 'other', '{}')]:
                con.execute("insert into workspaces(workspace_id,tenant_id,company_id,business_id,name,blueprint_json,blueprint_version,status,business_relation_status) "
                    "values (?,?,?,?,?,?,'v1','DRAFT',?)", (workspace, tenant, COMPANY, 'business-canonical-rd', workspace, raw, 'RESOLVED' if tenant == TENANT else 'UNRESOLVED'))
            con.execute('update workspaces set blueprint_json=? where workspace_id=?',
                        (json.dumps({'businessType': [], 'packageId': 42, 'packageVersion': True}), original))
        response = client.get(f'/api/workspace/runtime/foundation/companies/{COMPANY}/businesses/business-canonical-rd', headers=HEADERS)
        assert response.status_code == 200, response.text
        rows = {row['workspace_id']: row for row in response.json()['workspaces']}
        assert set(rows) == {original, 'real', 'broken'}
        assert rows['real']['package_id'] == 'com.curis.local.music' and rows['real']['package_version'] == 'v1-exact'
        assert rows['real']['business_type'] == 'PACKAGE'
        for row in (rows[original], rows['broken']):
            assert row['business_type'] is None and row['package_id'] is None and row['package_version'] is None
        assert all('blueprint_json' not in row for row in rows.values())
