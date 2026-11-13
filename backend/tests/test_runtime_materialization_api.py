from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json

from fastapi.testclient import TestClient

from app.database import Database
from app.identity_membership import AuthorizedMembership, IdentityMembership
from app.main import create_app


TENANT = "tenant-materialization"
CEO = "ceo-materialization"
OTHER_TENANT = "tenant-materialization-other"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}
OTHER_HEADERS = {"X-Tenant-Id": OTHER_TENANT, "X-Ceo-Id": CEO}
PREFIX = "/api/workspace/runtime/foundation"


@contextmanager
def client_for(path):
    with TestClient(create_app(str(path))) as client:
        yield client


def create_confirmed_run(client: TestClient, *, headers=HEADERS) -> str:
    created = client.post(
        f"{PREFIX}/founding-runs",
        headers=headers,
        json={"owner_ref": headers["X-Ceo-Id"], "intent_ref": "intent-safe-ref"},
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
    return run_id


def materialize(client: TestClient, run_id: str, *, headers=HEADERS, name="Curis Materialized"):
    return client.post(
        f"{PREFIX}/founding-runs/{run_id}/materialize-company",
        headers=headers,
        json={"company_id": "company-materialized", "ceo_id": CEO, "name": name},
    )


def test_fresh_restart_idempotency_transaction_and_audit(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "materialization.sqlite"

    with client_for(path) as client:
        run_id = create_confirmed_run(client)
        first = materialize(client, run_id)
        assert first.status_code == 200, first.text
        payload = first.json()
        assert payload["founding_run"]["lifecycle_status"] == "COMPANY_CREATED"
        assert payload["founding_run"]["company_id"] == "company-materialized"
        assert payload["company"]["company_id"] == "company-materialized"
        assert payload["company"]["name"] == "Curis Materialized"
        assert payload["assistant"]["entity_type"] == "CEO_ASSISTANT"
        assert payload["assistant"]["company_id"] == "company-materialized"
        assert payload["workspaces"] == []
        assistant_id = payload["assistant"]["entity_id"]

        retried = materialize(client, run_id)
        assert retried.status_code == 200, retried.text
        assert retried.json()["assistant"]["entity_id"] == assistant_id

    with client_for(path) as restarted:
        recovered = restarted.get(f"{PREFIX}/founding-runs/{run_id}", headers=HEADERS)
        snapshot = restarted.get(f"{PREFIX}/companies/company-materialized", headers=HEADERS)
        retried_after_restart = materialize(restarted, run_id)
        assert recovered.status_code == snapshot.status_code == retried_after_restart.status_code == 200
        assert recovered.json()["lifecycle_status"] == "COMPANY_CREATED"
        assert snapshot.json()["assistant"]["entity_id"] == assistant_id
        assert retried_after_restart.json()["assistant"]["entity_id"] == assistant_id

    with Database(str(path)).connect() as connection:
        counts = {
            "companies": connection.execute(
                "select count(*) from companies where tenant_id = ?", (TENANT,),
            ).fetchone()[0],
            "assistants": connection.execute(
                "select count(*) from runtime_entities where tenant_id = ? and entity_type = 'CEO_ASSISTANT'",
                (TENANT,),
            ).fetchone()[0],
            "workspaces": connection.execute(
                "select count(*) from workspaces where tenant_id = ?", (TENANT,),
            ).fetchone()[0],
            "projects": connection.execute(
                "select count(*) from projects where tenant_id = ?", (TENANT,),
            ).fetchone()[0],
            "tasks": connection.execute(
                "select count(*) from tasks where tenant_id = ?", (TENANT,),
            ).fetchone()[0],
        }
        audits = connection.execute(
            "select actor, trigger, target, at, company_id, context_json from runtime_transition_log "
            "where tenant_id = ? and entity_id = ? and target = 'COMPANY_CREATED'",
            (TENANT, run_id),
        ).fetchall()
        integrity = connection.execute("pragma integrity_check").fetchone()[0]
    assert counts == {"companies": 1, "assistants": 1, "workspaces": 0, "projects": 0, "tasks": 0}
    assert len(audits) == 1
    audit = dict(audits[0])
    assert audit["actor"] == "SYSTEM"
    assert audit["trigger"] == "persist_company"
    assert audit["target"] == "COMPANY_CREATED"
    assert audit["company_id"] == "company-materialized"
    assert audit["at"]
    assert json.loads(audit["context_json"])["companyId"] == "company-materialized"
    assert integrity == "ok"


def test_concurrent_retries_return_one_company_and_assistant(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "materialization-concurrent.sqlite"
    with client_for(path) as client:
        run_id = create_confirmed_run(client)

    clients = [TestClient(create_app(str(path))), TestClient(create_app(str(path)))]
    with clients[0] as first, clients[1] as second:
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(lambda client: materialize(client, run_id), (first, second)))
    assert [response.status_code for response in responses] == [200, 200]
    assert len({response.json()["assistant"]["entity_id"] for response in responses}) == 1
    with Database(str(path)).connect() as connection:
        assert connection.execute(
            "select count(*) from companies where tenant_id = ?", (TENANT,),
        ).fetchone()[0] == 1
        assert connection.execute(
            "select count(*) from runtime_entities where tenant_id = ? and entity_type = 'CEO_ASSISTANT'",
            (TENANT,),
        ).fetchone()[0] == 1
        assert connection.execute(
            "select count(*) from runtime_transition_log where tenant_id = ? and entity_id = ? "
            "and target = 'COMPANY_CREATED'",
            (TENANT, run_id),
        ).fetchone()[0] == 1


def test_scope_actor_state_and_input_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "materialization-boundaries.sqlite"
    with client_for(path) as client:
        run_id = create_confirmed_run(client)
        unconfirmed = client.post(
            f"{PREFIX}/founding-runs",
            headers=HEADERS,
            json={"owner_ref": CEO},
        ).json()["entity_id"]
        wrong_tenant = materialize(client, run_id, headers=OTHER_HEADERS)
        wrong_ceo = client.post(
            f"{PREFIX}/founding-runs/{run_id}/materialize-company",
            headers={"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo-other"},
            json={"company_id": "company-materialized", "ceo_id": CEO, "name": "Curis Materialized"},
        )
        missing_ceo_identity = client.post(
            f"{PREFIX}/founding-runs/{run_id}/materialize-company",
            headers={"X-Tenant-Id": TENANT},
            json={"company_id": "company-materialized", "ceo_id": CEO, "name": "Curis Materialized"},
        )
        wrong_state = materialize(client, unconfirmed)
        extra_actor = client.post(
            f"{PREFIX}/founding-runs/{run_id}/materialize-company",
            headers=HEADERS,
            json={
                "company_id": "company-materialized", "ceo_id": CEO,
                "name": "Curis Materialized", "actor": "SYSTEM",
            },
        )
        unsafe_id = client.post(
            f"{PREFIX}/founding-runs/{run_id}/materialize-company",
            headers=HEADERS,
            json={"company_id": "../company", "ceo_id": CEO, "name": "Curis"},
        )
        unsafe_name = client.post(
            f"{PREFIX}/founding-runs/{run_id}/materialize-company",
            headers=HEADERS,
            json={"company_id": "company-materialized", "ceo_id": CEO, "name": "Curis\u0000"},
        )
    assert wrong_tenant.status_code == wrong_ceo.status_code == missing_ceo_identity.status_code == 404
    assert wrong_state.status_code == 409
    assert extra_actor.status_code == unsafe_id.status_code == unsafe_name.status_code == 422
    for response in (wrong_tenant, wrong_ceo, missing_ceo_identity, wrong_state, extra_actor, unsafe_id, unsafe_name):
        assert "Traceback" not in response.text
        assert "sqlite" not in response.text.lower()
        assert str(path) not in response.text

    def member_identity(_service, request):
        return AuthorizedMembership(
            "member", request.headers.get("X-Tenant-Id") or TENANT, "", CEO,
            "member", "active", "request-member",
        )

    monkeypatch.setattr(IdentityMembership, "authorize", member_identity)
    with client_for(path) as member_client:
        denied = materialize(member_client, run_id)
    assert denied.status_code == 403
    assert denied.json() == {"detail": "当前操作者无权执行该状态转换"}
