from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


PACKAGE_ID = "ccp_ai_software_company"
PACKAGE_VERSION = "1.0.0"
BRIDGE_ID = "bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0"
WORKFLOW_ID = "official.workflow.software_rnd_sop"
TENANT = {"X-Tenant-Id": "tenant-bridge", "X-Ceo-Id": "ceo-bridge"}
ADMIN = {"Authorization": "Bearer platform-admin-dev"}


@pytest.fixture
def bridge_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    monkeypatch.setenv("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
    db_path = str(tmp_path / "bridge.sqlite")
    with TestClient(create_app(db_path)) as client:
        yield client, db_path


def _instantiate(client: TestClient):
    return client.post(
        f"/api/platform/company-packages/{PACKAGE_ID}/instantiate",
        headers={**ADMIN, **TENANT},
    )


def test_exact_bridge_instance_and_run_provenance(bridge_client):
    client, db_path = bridge_client

    catalog = client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?version={PACKAGE_VERSION}",
        headers=TENANT,
    )
    assert catalog.status_code == 200, catalog.text
    assert catalog.json()["workflows"] == [
        {
            "bridge_id": BRIDGE_ID,
            "company_package_id": PACKAGE_ID,
            "package_version": PACKAGE_VERSION,
            "source_workflow_content_id": "wl_ai_rd_software_dev_sop",
            "source_workflow_content_version": PACKAGE_VERSION,
            "workflow_template_id": WORKFLOW_ID,
            "workflow_template_version": PACKAGE_VERSION,
            "workflow_capability_status": "structured_executable",
            "source": "Curis internal",
            "tenant_id": "platform",
            "status": "active",
            "created_at": catalog.json()["workflows"][0]["created_at"],
            "revoked_at": None,
        }
    ]

    instantiated = _instantiate(client)
    assert instantiated.status_code == 200, instantiated.text
    body = instantiated.json()
    assert body["package_version"] == PACKAGE_VERSION
    assert body["bridge_id"] == BRIDGE_ID
    bridged = [item for item in body["workflows"] if item["bridge_id"]]
    assert len(bridged) == 1
    assert bridged[0]["workflow_template_id"] == WORKFLOW_ID
    assert bridged[0]["workflow_template_version"] == PACKAGE_VERSION

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        company = dict(
            connection.execute(
                "select * from companies where company_id = ?", (body["company_id"],)
            ).fetchone()
        )
        instance = dict(
            connection.execute(
                "select * from workflow_instances where workflow_instance_id = ?",
                (bridged[0]["workflow_instance_id"],),
            ).fetchone()
        )
    for row in (company, instance):
        assert row["source_company_package_id"] == PACKAGE_ID
        assert row["source_package_version"] == PACKAGE_VERSION
        assert row["source_bridge_id"] == BRIDGE_ID
        assert row["source_workflow_template_id"] == WORKFLOW_ID
        assert row["source_workflow_template_version"] == PACKAGE_VERSION

    project = client.post(
        "/api/workspace/projects",
        headers=TENANT,
        json={
            "company_id": body["company_id"],
            "department_id": body["departments"][0]["id"],
            "name": "Versioned provenance project",
            "goal": "Verify immutable package workflow provenance",
        },
    )
    assert project.status_code == 201, project.text
    created = client.post(
        "/api/workspace/workflows",
        headers=TENANT,
        json={
            "workflow_instance_id": bridged[0]["workflow_instance_id"],
            "workflow_template_id": WORKFLOW_ID,
            "department_id": body["departments"][0]["id"],
            "company_id": body["company_id"],
            "project_id": project.json()["project_id"],
            "content": "Provenance-only focused run; do not execute.",
        },
    )
    assert created.status_code == 201, created.text
    run = created.json()
    assert run["status"] == "pending"
    assert [step["status"] for step in run["steps"]] == ["pending"] * 7
    assert run["source_company_package_id"] == PACKAGE_ID
    assert run["source_package_version"] == PACKAGE_VERSION
    assert run["source_bridge_id"] == BRIDGE_ID
    assert run["source_workflow_template_id"] == WORKFLOW_ID
    assert run["source_workflow_template_version"] == PACKAGE_VERSION
    with sqlite3.connect(db_path) as connection:
        assert connection.execute(
            "select count(*) from evolution_events where event_type like 'usage.%'"
        ).fetchone()[0] == 0
        assert connection.execute("select count(*) from step_results").fetchone()[0] == 0


def test_selfuse_migrated_official_workflow_resolves_exact_bridge(bridge_client):
    client, db_path = bridge_client
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "update workflow_contents set tenant_id='selfuse' where source='official'"
        )
        connection.execute(
            "update workflow_templates set tenant_id='selfuse' where source='official'"
        )

    headers = {"X-Tenant-Id": "selfuse", "X-Ceo-Id": "ceo-selfuse"}
    catalog = client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?version={PACKAGE_VERSION}",
        headers=headers,
    )
    assert catalog.status_code == 200, catalog.text
    assert catalog.json()["workflows"][0]["bridge_id"] == BRIDGE_ID

    instantiated = client.post(
        f"/api/platform/company-packages/{PACKAGE_ID}/instantiate",
        headers={**ADMIN, **headers},
    )
    assert instantiated.status_code == 200, instantiated.text
    bridged = [item for item in instantiated.json()["workflows"] if item["bridge_id"]]
    assert len(bridged) == 1
    assert bridged[0]["workflow_template_id"] == WORKFLOW_ID
    assert bridged[0]["workflow_template_version"] == PACKAGE_VERSION


@pytest.mark.parametrize(
    "mutation",
    [
        "delete from company_package_workflow_bridges",
        "update company_package_workflow_bridges set status='revoked', revoked_at=current_timestamp",
        "update company_package_workflow_bridges set workflow_template_version='9.9.9'",
        "update company_package_workflow_bridges set workflow_template_id='wt_software_dev_sop'",
        """
        insert into company_package_workflow_bridges (
          bridge_id, company_package_id, package_version,
          source_workflow_content_id, source_workflow_content_version,
          workflow_template_id, workflow_template_version,
          workflow_capability_status, source, tenant_id, status
        ) values (
          'bridge-duplicate', 'ccp_ai_software_company', '1.0.0',
          'wl_ai_rd_software_dev_sop', '1.0.0',
          'official.workflow.content_growth_sop', '1.0.0',
          'structured_executable', 'Curis internal', 'platform', 'active'
        )
        """,
    ],
    ids=["missing", "revoked", "version-mismatch", "design-only", "duplicate"],
)
def test_invalid_bridge_fails_before_instance_writes(bridge_client, mutation):
    client, db_path = bridge_client
    with sqlite3.connect(db_path) as connection:
        connection.execute(mutation)

    response = _instantiate(client)
    assert response.status_code == 422, response.text
    with sqlite3.connect(db_path) as connection:
        assert connection.execute(
            "select count(*) from companies where tenant_id = 'tenant-bridge'"
        ).fetchone()[0] == 0
        assert connection.execute(
            "select count(*) from workflow_instances where tenant_id = 'tenant-bridge'"
        ).fetchone()[0] == 0


def test_cross_tenant_and_inference_paths_fail_closed(bridge_client):
    client, db_path = bridge_client
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "update company_package_workflow_bridges set source='tenant_private', tenant_id='tenant-a'"
        )

    assert client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?version={PACKAGE_VERSION}",
        headers={"X-Tenant-Id": "tenant-b", "X-Ceo-Id": "ceo-b"},
    ).status_code == 404
    assert client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?version={PACKAGE_VERSION}",
        headers={"X-Tenant-Id": "tenant-a", "X-Ceo-Id": "ceo-a"},
    ).status_code == 200
    assert client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows",
        headers=TENANT,
    ).status_code == 422
    assert client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?default=true",
        headers=TENANT,
    ).status_code == 422
    assert client.get(
        f"/api/catalog/company-packages/{PACKAGE_ID}/workflows?version=1.0.0&latest=true",
        headers=TENANT,
    ).status_code == 422
    assert client.get(
        "/api/catalog/company-packages/AI%20%E8%BD%AF%E4%BB%B6%E5%85%AC%E5%8F%B8%E5%87%BA%E5%8E%82%E5%8C%85/workflows?version=1.0.0",
        headers=TENANT,
    ).status_code == 404


def test_client_cannot_override_instance_provenance(bridge_client):
    client, db_path = bridge_client
    instantiated = _instantiate(client)
    assert instantiated.status_code == 200, instantiated.text
    body = instantiated.json()
    bridged = next(item for item in body["workflows"] if item["bridge_id"])

    response = client.post(
        "/api/workspace/workflows",
        headers=TENANT,
        json={
            "workflow_instance_id": bridged["workflow_instance_id"],
            "workflow_template_id": WORKFLOW_ID,
            "department_id": body["departments"][0]["id"],
            "company_id": body["company_id"],
            "content": "must not create",
            "source_package_version": "latest",
            "source_bridge_id": "client-override",
        },
    )
    assert response.status_code == 422
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("select count(*) from workflow_runs").fetchone()[0] == 0
        assert connection.execute(
            "select count(*) from evolution_events where event_type like 'usage.%'"
        ).fetchone()[0] == 0


def test_revoked_bridge_rejects_run_before_any_runtime_write(bridge_client):
    client, db_path = bridge_client
    instantiated = _instantiate(client)
    assert instantiated.status_code == 200, instantiated.text
    body = instantiated.json()
    bridged = next(item for item in body["workflows"] if item["bridge_id"])

    counts_sql = """
        select
          (select count(*) from tasks),
          (select count(*) from workflow_runs),
          (select count(*) from workflow_steps),
          (select count(*) from evolution_events where event_type like 'usage.%')
    """
    with sqlite3.connect(db_path) as connection:
        before = connection.execute(counts_sql).fetchone()
        connection.execute(
            "update company_package_workflow_bridges "
            "set status='revoked', revoked_at=current_timestamp where bridge_id = ?",
            (BRIDGE_ID,),
        )

    response = client.post(
        "/api/workspace/workflows",
        headers=TENANT,
        json={
            "workflow_instance_id": bridged["workflow_instance_id"],
            "workflow_template_id": WORKFLOW_ID,
            "department_id": body["departments"][0]["id"],
            "company_id": body["company_id"],
            "content": "must fail before creating a task",
        },
    )
    assert response.status_code == 422, response.text

    with sqlite3.connect(db_path) as connection:
        after = connection.execute(counts_sql).fetchone()
    assert after == before
