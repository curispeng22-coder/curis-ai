from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from backend.app.main import create_app


@pytest.fixture
def local_owner_client(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "development")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "https://quality.issuer.local")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "focused-audit-key")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "1")
    monkeypatch.setenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "0")
    app = create_app(str(tmp_path / "local-owner.sqlite"))

    @app.middleware("http")
    async def trusted_gateway(request, call_next):
        request.scope["client"] = ("10.0.0.2", 12345)
        return await call_next(request)

    with TestClient(app) as client:
        yield client


def test_first_start_creates_owner_session_and_mvp_entities(local_owner_client):
    client = local_owner_client
    origin = {"Origin": "http://127.0.0.1:3001"}

    assert client.get("/api/auth/local/status").json() == {
        "mode": "local_desktop",
        "initialized": False,
        "authenticated": False,
    }
    assert client.get("/api/workspace/companies").status_code == 401

    initialized = client.post(
        "/api/auth/local/initialize",
        params={"next": "/ceo-office/projects"},
        headers=origin,
    )
    assert initialized.status_code == 201
    assert initialized.json()["next"] == "/onboarding?next=%2Fceo-office%2Fprojects"
    assert "httponly" in initialized.headers["set-cookie"].lower()
    assert client.get("/api/auth/local/status").json()["authenticated"] is True

    company = client.post(
        "/api/workspace/companies",
        json={"name": "Local Owner Company", "description": "Desktop MVP"},
    )
    assert company.status_code == 201, company.text
    company_id = company.json()["company_id"]

    department = client.post(
        "/api/workspace/departments",
        json={
            "company_id": company_id,
            "template_id": "official.department.software_rnd",
            "name": "Local Owner Department",
        },
    )
    assert department.status_code == 201, department.text
    department_id = department.json()["id"]

    employee = client.post(
        "/api/workspace/employees",
        json={
            "department_id": department_id,
            "template_id": "official.employee.tech_lead",
            "name": "Local Owner Employee",
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
            "name": "Local Owner Project",
            "goal": "Verify the Local Desktop MVP flow",
            "department_id": department_id,
            "owner_employee_id": employee_id,
        },
    )
    assert project.status_code == 201, project.text


def test_existing_owner_can_start_a_new_session(local_owner_client):
    client = local_owner_client
    origin = {"Origin": "http://127.0.0.1:3001"}
    assert client.post("/api/auth/local/initialize", headers=origin).status_code == 201

    client.cookies.clear()
    status = client.get("/api/auth/local/status").json()
    assert status["initialized"] is True
    assert status["authenticated"] is False

    session = client.post(
        "/api/auth/local/session",
        params={"next": "/ceo-office"},
        headers=origin,
    )
    assert session.status_code == 200
    assert session.json() == {"authenticated": True, "next": "/ceo-office"}
    assert client.get("/api/workspace/companies").status_code == 200


def test_foreign_origin_cannot_force_local_owner_logout(local_owner_client):
    client = local_owner_client
    origin = {"Origin": "http://127.0.0.1:3001"}
    assert client.post("/api/auth/local/initialize", headers=origin).status_code == 201

    rejected = client.post(
        "/api/auth/local/logout",
        headers={"Origin": "https://evil.example"},
    )
    assert rejected.status_code == 403
    assert "set-cookie" not in rejected.headers
    assert client.get("/api/auth/local/status").json()["authenticated"] is True

    signed_out = client.post("/api/auth/local/logout", headers=origin)
    assert signed_out.status_code == 200
    assert signed_out.json() == {"status": "signed_out"}
    assert "curis_local_session=" in signed_out.headers["set-cookie"]
    assert client.get("/api/auth/local/status").json()["authenticated"] is False


def test_local_owner_rejects_foreign_origin_and_unsafe_return(local_owner_client):
    client = local_owner_client

    rejected = client.post(
        "/api/auth/local/initialize",
        headers={"Origin": "https://evil.example"},
    )
    assert rejected.status_code == 403

    initialized = client.post(
        "/api/auth/local/initialize",
        params={"next": "https://evil.example"},
        headers={"Origin": "http://127.0.0.1:3001"},
    )
    assert initialized.status_code == 201
    assert initialized.json()["next"] == "/onboarding?next=%2Fceo-office"


def test_local_owner_cannot_enable_in_production(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "production")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "issuer")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "audit")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "1")
    monkeypatch.setenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "0")

    with pytest.raises(RuntimeError, match="local Owner requires"):
        create_app(str(tmp_path / "production.sqlite"))
