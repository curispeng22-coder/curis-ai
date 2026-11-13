from __future__ import annotations

import logging
from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient
import pytest

from backend.app.local_google_oidc import (
    CEO_ID,
    COMPANY_ID,
    ISSUER,
    LocalOidcRejected,
    PREAUTHORIZATION_ID,
    PROJECT_ID,
    TENANT_ID,
)
from backend.app.main import create_app


def _seed_target(db_path: str) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "create table local_owner_preauthorizations ("
            "authorization_id text primary key, operation_key text not null unique, "
            "tenant_id text not null, company_id text not null, ceo_id text not null, "
            "project_id text not null, material_digest text, status text not null, "
            "created_at text default current_timestamp, consumed_at text)"
        )
        connection.execute("insert into tenants (tenant_id, name) values (?, 'Local')", (TENANT_ID,))
        connection.execute(
            "insert into companies (company_id, tenant_id, ceo_id, name, default_project_id) "
            "values (?, ?, ?, 'Local', ?)",
            (COMPANY_ID, TENANT_ID, CEO_ID, PROJECT_ID),
        )
        connection.execute(
            "insert into projects (project_id, tenant_id, company_id, name, goal) "
            "values (?, ?, ?, 'Runtime', 'Goal')",
            (PROJECT_ID, TENANT_ID, COMPANY_ID),
        )
        connection.execute(
            "insert into local_owner_preauthorizations "
            "(authorization_id, operation_key, tenant_id, company_id, ceo_id, project_id, status) "
            "values (?, 'test', ?, ?, ?, ?, 'pending')",
            (PREAUTHORIZATION_ID, TENANT_ID, COMPANY_ID, CEO_ID, PROJECT_ID),
        )


@pytest.fixture
def local_client(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "development")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "https://quality.issuer.local")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "focused-audit-key")
    monkeypatch.setenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "1")
    db_path = str(tmp_path / "quality.sqlite")
    app = create_app(db_path, tool_functions={"default_tool": lambda prompt: prompt})
    _seed_target(db_path)

    @app.middleware("http")
    async def trusted_gateway(request, call_next):
        request.scope["client"] = ("10.0.0.2", 12345)
        response = await call_next(request)
        app.state.last_query_string = request.scope["query_string"]
        return response

    app.state.local_google_oidc.inject(
        {
            "google_client_id": "focused-client-id",
            "google_client_secret": "focused-client-secret",
            "bootstrap_material": "b" * 32,
        }
    )
    with TestClient(app) as client:
        yield client, app.state.local_google_oidc, db_path


def _login(client: TestClient, manager, subject: str, next_path: str = ""):
    start = client.get(
        "/api/auth/google/login",
        params={"next": next_path} if next_path else None,
        follow_redirects=False,
    )
    assert start.status_code == 303
    state = client.cookies["curis_oidc_state"]
    manager._google_claims = lambda code, nonce: {"sub": subject}
    return client.get(
        "/api/auth/google/callback",
        params={"code": "one-code", "state": state},
        follow_redirects=False,
    )


def test_callback_atomically_consumes_preauthorization(local_client):
    client, manager, db_path = local_client
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("select count(*) from tenant_memberships").fetchone()[0] == 0
        digest, status = connection.execute(
            "select material_digest, status from local_owner_preauthorizations"
        ).fetchone()
        assert digest and status == "pending"

    callback = _login(
        client,
        manager,
        "verified-google-subject",
        "/ceo-office/organization",
    )
    assert callback.status_code == 303
    assert callback.headers["location"].endswith(
        "/onboarding?next=%2Fceo-office%2Forganization"
    )
    runtime = client.get(f"/api/pipeline/project/{PROJECT_ID}")
    assert runtime.status_code == 200
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "select issuer, subject_id, tenant_id, company_id, ceo_id, role, status "
            "from tenant_memberships"
        ).fetchone()
        assert row == (ISSUER, "verified-google-subject", TENANT_ID, COMPANY_ID, CEO_ID, "owner", "active")
        assert connection.execute(
            "select status from local_owner_preauthorizations"
        ).fetchone()[0] == "consumed"


def test_returning_owner_returns_to_original_safe_path(local_client):
    client, manager, _ = local_client
    assert _login(client, manager, "owner-subject").headers["location"].endswith(
        "/onboarding?next=%2Fceo-office"
    )
    client.cookies.clear()

    callback = _login(
        client,
        manager,
        "owner-subject",
        "/ceo-office/projects?view=active",
    )

    assert callback.status_code == 303
    assert callback.headers["location"].endswith(
        "/ceo-office/projects?view=active"
    )


def test_authenticated_local_owner_can_complete_mvp_setup(local_client):
    client, manager, _ = local_client
    assert _login(client, manager, "owner-subject").status_code == 303

    company = client.post(
        "/api/workspace/companies",
        json={"name": "Authentication E2E Company", "description": "P0 setup"},
    )
    assert company.status_code == 201, company.text
    company_id = company.json()["company_id"]

    department = client.post(
        "/api/workspace/departments",
        json={
            "company_id": company_id,
            "template_id": "official.department.software_rnd",
            "name": "Authentication E2E Department",
        },
    )
    assert department.status_code == 201, department.text
    department_id = department.json()["id"]

    employee = client.post(
        "/api/workspace/employees",
        json={
            "department_id": department_id,
            "template_id": "official.employee.tech_lead",
            "name": "Authentication E2E Employee",
            "status": "idle",
            "enabled": True,
        },
    )
    assert employee.status_code == 201, employee.text
    employee_id = employee.json()["id"]

    project = client.post(
        "/api/workspace/projects",
        json={
            "company_id": company_id,
            "name": "Authentication E2E Project",
            "goal": "Verify the authenticated setup flow",
            "department_id": department_id,
            "owner_employee_id": employee_id,
        },
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["project_id"]

    task = client.post(
        f"/api/workspace/projects/{project_id}/tasks",
        json={"content": "Verify the authenticated task entry", "employee_id": employee_id},
    )
    assert task.status_code == 201, task.text
    assert task.json()["project_id"] == project_id


@pytest.mark.parametrize(
    "unsafe",
    [
        "https://evil.example/path",
        "//evil.example/path",
        "/\t/evil.example/path",
        r"/\\evil.example/path",
        "/ceo-office\r\nLocation:https://evil.example",
    ],
)
def test_login_rejects_unsafe_return_paths(local_client, unsafe):
    client, manager, _ = local_client

    callback = _login(client, manager, "owner-subject", unsafe)

    assert callback.status_code == 303
    assert callback.headers["location"].endswith(
        "/onboarding?next=%2Fceo-office"
    )


@pytest.mark.parametrize(
    ("params", "expected_reason"),
    [
        ({"error": "provider-secret"}, "provider_error"),
        ({"state": "state-secret"}, "code_missing"),
        ({"code": "code-secret"}, "state_missing"),
        ({"code": "code-secret", "state": "state-secret"}, "state_cookie_mismatch"),
    ],
)
def test_callback_rejection_logs_only_fixed_internal_reason(
    local_client, caplog, params, expected_reason
):
    client, _, _ = local_client
    caplog.set_level(logging.WARNING, logger="curis.security.local_google_oidc")

    response = client.get(
        "/api/auth/google/callback", params=params, follow_redirects=False
    )

    assert response.headers["location"].endswith("?error=login_failed")
    assert caplog.messages == [
        f"local_google_oidc_callback_rejected reason={expected_reason}"
    ]
    assert all(value not in caplog.text for value in params.values())


def test_callback_query_is_removed_from_both_access_log_layers(local_client):
    client, manager, _ = local_client
    state = "non-sensitive-state-probe"
    client.cookies.set("curis_oidc_state", "different-probe", path="/api/auth/google")

    response = client.get(
        "/api/auth/google/callback",
        params={"code": "non-sensitive-code-probe", "state": state},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert manager.ready is True
    assert client.app.state.last_query_string == b""
    template = (
        Path(__file__).parents[2] / "deploy/curis/gateway/envoy.yaml.template"
    ).read_text()
    assert "%REQ_WITHOUT_QUERY(:PATH)%" in template
    assert "%REQ(:PATH)%" not in template
    assert template.index('prefix: "/api/pipeline/"') < template.index('name: cookie')
    assert template.index('prefix: "/api/workspace/projects/"') < template.index('name: cookie')
    assert template.count('exact_match: "http://127.0.0.1:3001"') == 2
    assert template.count('name: ":method", exact_match: "OPTIONS"') == 2
    assert 'regex: "^(GET|POST)$"' in template
    assert 'name: "access-control-request-method", exact_match: "PATCH"' in template
    assert template.count('name: "access-control-request-headers", exact_match: "content-type"') == 2
    assert template.count("direct_response: { status: 204 }") == 2
    assert template.count('key: "access-control-allow-origin", value: "http://127.0.0.1:3001"') == 2
    assert template.count('key: "access-control-allow-headers", value: "content-type"') == 2
    assert template.count('key: "access-control-allow-credentials", value: "true"') == 2


def test_different_subject_cannot_claim_consumed_owner(local_client):
    client, manager, db_path = local_client
    assert _login(client, manager, "owner-subject").status_code == 303
    client.cookies.clear()
    rejected = _login(client, manager, "different-subject")
    assert rejected.status_code == 303
    assert rejected.headers["location"].endswith("?error=owner_activation_not_pre_authorized")
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("select count(*) from tenant_memberships").fetchone()[0] == 1


def test_missing_session_and_cross_tenant_are_rejected(local_client):
    client, manager, _ = local_client
    assert client.get(f"/api/pipeline/project/{PROJECT_ID}").status_code == 401
    assert _login(client, manager, "owner-subject").status_code == 303
    assert client.get("/api/pipeline/project/not-the-fixed-project").status_code == 404


def test_target_drift_rejects_before_membership_write(local_client):
    client, manager, db_path = local_client
    with sqlite3.connect(db_path) as connection:
        connection.execute("update companies set ceo_id='drifted' where company_id=?", (COMPANY_ID,))
    rejected = _login(client, manager, "owner-subject")
    assert rejected.headers["location"].endswith("?error=owner_activation_not_pre_authorized")
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("select count(*) from tenant_memberships").fetchone()[0] == 0


def test_failed_start_can_reset_pending_material(local_client):
    _, manager, db_path = local_client
    manager.reset_pending_bootstrap()
    assert manager.ready is False
    with sqlite3.connect(db_path) as connection:
        assert connection.execute(
            "select material_digest, status from local_owner_preauthorizations"
        ).fetchone() == (None, "pending")


def test_consumed_owner_can_rotate_ephemeral_bootstrap(local_client):
    client, manager, db_path = local_client
    assert _login(client, manager, "owner-subject").status_code == 303

    manager.reset_pending_bootstrap()
    assert manager.ready is False
    manager.inject(
        {
            "google_client_id": "focused-client-id",
            "google_client_secret": "focused-client-secret",
            "bootstrap_material": "c" * 32,
        }
    )

    assert manager.ready is True
    with sqlite3.connect(db_path) as connection:
        digest, status = connection.execute(
            "select material_digest, status from local_owner_preauthorizations"
        ).fetchone()
        assert digest and status == "consumed"
        assert connection.execute(
            "select count(*) from tenant_memberships where issuer=? and role='owner' and status='active'",
            (ISSUER,),
        ).fetchone()[0] == 1


def test_consumed_bootstrap_requires_one_existing_owner(local_client):
    client, manager, db_path = local_client
    assert _login(client, manager, "owner-subject").status_code == 303
    with sqlite3.connect(db_path) as connection:
        connection.execute("delete from tenant_memberships")

    with pytest.raises(LocalOidcRejected, match="preauthorization_not_pending"):
        manager.reset_pending_bootstrap()


def test_local_oidc_cannot_enable_in_production(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "production")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "issuer")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "audit")
    monkeypatch.setenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "1")
    with pytest.raises(RuntimeError, match="local Google OIDC requires"):
        create_app(str(tmp_path / "production.sqlite"), tool_functions={"default_tool": lambda p: p})
