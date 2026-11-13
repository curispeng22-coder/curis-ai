from __future__ import annotations

import logging
import sqlite3
import uuid

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.ceo_context import CeoContext
from app.main import create_app
from app.resource_scope_policy import ResourceScopePolicy
from app.tenant_context import DEFAULT_TENANT, TenantContext


ISSUER = "https://issuer.example"
SUBJECT = "subject-123"


def _company(
    connection: sqlite3.Connection,
    tenant_id: str,
    company_id: str,
    ceo_id: str = "",
) -> None:
    connection.execute("insert into tenants (tenant_id, name) values (?, ?)", (tenant_id, tenant_id))
    connection.execute(
        "insert into companies (company_id, tenant_id, ceo_id, name) values (?, ?, ?, ?)",
        (company_id, tenant_id, ceo_id, company_id),
    )


@pytest.fixture
def identity_client(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "production")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", ISSUER)
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "test-audit-key")
    db_path = str(tmp_path / "identity.sqlite")
    app = create_app(db_path, tool_functions={"default_tool": lambda prompt: prompt})

    @app.get("/api/workspace/_trusted-context")
    def trusted_context():
        return {
            "identity": TenantContext.current_identity(),
            "ceo_id": CeoContext.current_ceo_id(),
        }

    @app.middleware("http")
    async def trusted_gateway_source(request, call_next):
        request.scope["client"] = ("10.0.0.2", 12345)
        return await call_next(request)

    database = Database(db_path)
    with database.connect() as connection:
        _company(connection, "tenant-a", "company-a", "ceo-a")
        _company(connection, "tenant-b", "company-b")
        connection.execute(
            "insert into tenant_memberships "
            "(membership_id, issuer, subject_id, tenant_id, company_id, ceo_id, role, status) "
            "values (?, ?, ?, ?, ?, 'ceo-a', 'owner', 'active')",
            (str(uuid.uuid4()), ISSUER, SUBJECT, "tenant-a", "company-a"),
        )
    headers = {
        "X-Tenant-Id": "tenant-a",
        "X-Curis-Gateway-Subject": SUBJECT,
        "X-Curis-Gateway-Issuer": ISSUER,
        "X-Curis-Gateway-Auth-Time": "1720000000",
        "X-Curis-Gateway-Request-Id": "request-1",
    }
    return TestClient(app), database, headers


def test_http_200_401_403_404(identity_client):
    client, _, headers = identity_client
    assert client.get("/api/workspace/companies", headers=headers).status_code == 200
    assert client.get("/api/workspace/companies", headers={"X-Tenant-Id": "tenant-a"}).status_code == 401
    assert client.get(
        "/api/workspace/companies", headers={**headers, "X-Tenant-Id": "tenant-b"}
    ).status_code == 403
    assert client.get("/api/workspace/companies/company-b", headers=headers).status_code == 404


def test_gateway_membership_ceo_wins_over_spoofed_client_header(identity_client):
    client, _, headers = identity_client
    response = client.get(
        "/api/workspace/_trusted-context",
        headers={**headers, "X-Ceo-Id": "forged-ceo"},
    )
    assert response.status_code == 200
    assert response.json()["identity"]["ceo_id"] == "ceo-a"
    assert response.json()["ceo_id"] == "ceo-a"


def test_untrusted_network_cannot_forge_gateway_headers(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "production")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", ISSUER)
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", "10.0.0.2/32")
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "test-audit-key")
    app = create_app(str(tmp_path / "untrusted.sqlite"), tool_functions={"default_tool": lambda p: p})
    response = TestClient(app).get(
        "/api/workspace/companies",
        headers={
            "X-Tenant-Id": "tenant-a",
            "X-Curis-Gateway-Subject": SUBJECT,
            "X-Curis-Gateway-Issuer": ISSUER,
            "X-Curis-Gateway-Auth-Time": "1720000000",
        },
    )
    assert response.status_code == 401


def test_revoked_expired_and_dual_read_fail_closed(identity_client):
    client, database, headers = identity_client
    with database.connect() as connection:
        connection.execute("update tenant_memberships set status='revoked', revoked_at=current_timestamp")
    assert client.get("/api/workspace/companies", headers=headers).status_code == 403
    with database.connect() as connection:
        connection.execute(
            "update tenant_memberships set status='active', revoked_at=null, expires_at='2000-01-01T00:00:00+00:00'"
        )
    assert client.get("/api/workspace/companies", headers=headers).status_code == 403
    with database.connect() as connection:
        connection.execute("update tenant_memberships set expires_at=null, company_id='missing'")
    assert client.get("/api/workspace/companies", headers=headers).status_code == 403


def test_security_log_is_redacted(identity_client, caplog):
    client, _, headers = identity_client
    caplog.set_level(logging.INFO, logger="curis.security.identity")
    client.get(
        "/api/workspace/companies",
        headers={**headers, "Authorization": "Bearer raw-jwt", "Cookie": "session=sensitive"},
    )
    output = caplog.text
    assert "subject_digest" in output and "request-1" in output
    assert SUBJECT not in output and "raw-jwt" not in output and "session=sensitive" not in output


def test_production_workspace_rejects_selfuse_and_missing_gateway(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "production")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "selfuse")
    with pytest.raises(RuntimeError, match="rejects self-use"):
        create_app(str(tmp_path / "selfuse.sqlite"), tool_functions={"default_tool": lambda p: p})
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.delenv("CURIS_TRUSTED_GATEWAY_ISSUER", raising=False)
    monkeypatch.delenv("CURIS_TRUSTED_GATEWAY_CIDRS", raising=False)
    with pytest.raises(RuntimeError, match="requires trusted gateway"):
        create_app(str(tmp_path / "missing.sqlite"), tool_functions={"default_tool": lambda p: p})


def test_tenant_context_and_resource_policy_contract():
    before = TenantContext.current_identity()
    with TenantContext.scope(
        "tenant-a", subject_id=SUBJECT, company_id="company-a", ceo_id="ceo-a", role="owner",
        membership_status="active", request_id="request-1",
    ):
        assert TenantContext.current_identity()["subject_id"] == SUBJECT
        assert TenantContext.current_identity()["ceo_id"] == "ceo-a"
        assert TenantContext.current_identity()["membership_status"] == "active"
    assert TenantContext.current_identity() == before
    assert TenantContext.current_tenant_id() == DEFAULT_TENANT
    assert set(ResourceScopePolicy.RESOURCES) == {
        "company", "department", "project", "employee", "workflow", "result", "usage"
    }


def test_existing_membership_table_gets_nullable_ceo_id_additively(tmp_path):
    db_path = str(tmp_path / "membership-migration.sqlite")
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "create table tenant_memberships ("
            "membership_id text primary key, issuer text not null, subject_id text not null, "
            "tenant_id text not null, company_id text not null, role text not null, "
            "status text not null, created_at text, expires_at text, revoked_at text)"
        )
        connection.execute(
            "insert into tenant_memberships "
            "(membership_id, issuer, subject_id, tenant_id, company_id, role, status) "
            "values ('membership-old', 'issuer', 'subject', 'tenant', 'company', 'owner', 'active')"
        )

    Database(db_path).initialize()

    with sqlite3.connect(db_path) as connection:
        columns = {row[1] for row in connection.execute("pragma table_info(tenant_memberships)")}
        ceo_id = connection.execute(
            "select ceo_id from tenant_memberships where membership_id='membership-old'"
        ).fetchone()[0]
    assert "ceo_id" in columns
    assert ceo_id is None
