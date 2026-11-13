from __future__ import annotations

from contextlib import contextmanager

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext


PREFIX = "/api/workspace/runtime/foundation"
TENANT_A = "tenant-first-arrival-a"
TENANT_B = "tenant-first-arrival-b"
CEO_A = "ceo-first-arrival-a"
CEO_B = "ceo-first-arrival-b"
HEADERS_A = {"X-Tenant-Id": TENANT_A, "X-Ceo-Id": CEO_A}
HEADERS_B = {"X-Tenant-Id": TENANT_B, "X-Ceo-Id": CEO_B}


@contextmanager
def client_for(path):
    with TestClient(create_app(str(path))) as client:
        yield client


def materialize_company(client: TestClient, headers: dict[str, str], suffix: str) -> dict:
    ceo_id = headers["X-Ceo-Id"]
    created = client.post(
        f"{PREFIX}/founding-runs",
        headers=headers,
        json={"owner_ref": ceo_id, "intent_ref": f"intent-{suffix}"},
    )
    assert created.status_code == 201, created.text
    run_id = created.json()["entity_id"]
    for target, trigger in (
        ("INTENT_CAPTURED", "capture_intent"),
        ("CLARIFYING", "request_clarification"),
        ("PROPOSED", "propose_company"),
        ("CEO_CONFIRMED", "confirm_company"),
    ):
        moved = client.post(
            f"{PREFIX}/entities/{run_id}/transition",
            headers=headers,
            json={"target": target, "actor": "CEO", "trigger": trigger},
        )
        assert moved.status_code == 200, moved.text
    company_id = f"company-first-arrival-{suffix}"
    response = client.post(
        f"{PREFIX}/founding-runs/{run_id}/materialize-company",
        headers=headers,
        json={"company_id": company_id, "ceo_id": ceo_id, "name": f"Runtime Company {suffix}"},
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_fresh_collection_is_empty_read_only_and_excludes_legacy_company(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "first-arrival-fresh.sqlite"

    with client_for(path) as client:
        with Database(str(path)).connect() as connection:
            before = {
                table: connection.execute(f"select count(*) from {table}").fetchone()[0]
                for table in ("companies", "runtime_entities", "runtime_transition_log")
            }
        fresh = client.get(f"{PREFIX}/companies", headers=HEADERS_A)
        assert fresh.status_code == 200, fresh.text
        assert fresh.json() == {"tenant_id": TENANT_A, "companies": []}
        with Database(str(path)).connect() as connection:
            after = {
                table: connection.execute(f"select count(*) from {table}").fetchone()[0]
                for table in ("companies", "runtime_entities", "runtime_transition_log")
            }
            connection.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name, description, status) "
                "values ('company-legacy', ?, ?, 'Legacy Company', 'must stay unchanged', 'active')",
                (TENANT_A, CEO_A),
            )
            legacy_before = dict(connection.execute(
                "select * from companies where company_id = 'company-legacy'",
            ).fetchone())
        with TenantContext.scope(TENANT_A):
            RuntimeFoundation(Database(str(path))).create(
                "CEO_ASSISTANT", company_id="company-legacy", owner_ref=CEO_A,
            )

        excluded = client.get(f"{PREFIX}/companies", headers=HEADERS_A)
        assert excluded.status_code == 200, excluded.text
        assert excluded.json()["companies"] == []
        with Database(str(path)).connect() as connection:
            legacy_after = dict(connection.execute(
                "select * from companies where company_id = 'company-legacy'",
            ).fetchone())
            integrity = connection.execute("pragma integrity_check").fetchone()[0]

    assert before == after == {"companies": 0, "runtime_entities": 0, "runtime_transition_log": 0}
    assert legacy_after == legacy_before
    assert integrity == "ok"


def test_materialized_collection_survives_restart_and_is_tenant_scoped(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "first-arrival-runtime.sqlite"

    with client_for(path) as client:
        runtime_a = materialize_company(client, HEADERS_A, "a")
        runtime_b = materialize_company(client, HEADERS_B, "b")
        collection_a = client.get(f"{PREFIX}/companies", headers=HEADERS_A)
        collection_b = client.get(f"{PREFIX}/companies", headers=HEADERS_B)
        assert collection_a.status_code == collection_b.status_code == 200
        assert [item["company_id"] for item in collection_a.json()["companies"]] == [
            runtime_a["company"]["company_id"]
        ]
        assert [item["company_id"] for item in collection_b.json()["companies"]] == [
            runtime_b["company"]["company_id"]
        ]
        combined = collection_a.text + collection_b.text
        assert "prompt" not in combined.lower()
        assert "apikey" not in combined.lower()
        assert "runtime_entities" not in combined

    with client_for(path) as restarted:
        recovered_a = restarted.get(f"{PREFIX}/companies", headers=HEADERS_A)
        cross_tenant = restarted.get(
            f"{PREFIX}/companies/{runtime_b['company']['company_id']}", headers=HEADERS_A,
        )
        assert recovered_a.status_code == 200
        assert recovered_a.json()["companies"] == collection_a.json()["companies"]
        assert cross_tenant.status_code == 404
        assert cross_tenant.json() == {"detail": "运行对象不存在或无权访问"}
        assert TENANT_B not in cross_tenant.text

    with Database(str(path)).connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
