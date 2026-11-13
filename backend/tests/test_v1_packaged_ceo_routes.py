"""Desktop self-use identity must own the legally materialized Company."""
from fastapi.testclient import TestClient

from app.main import create_app
from app.database import Database


def test_packaged_ceo_routes_and_restart(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "local")
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "selfuse")
    path = str(tmp_path / "packaged-ceo.sqlite")
    prefix = "/api/workspace/runtime/foundation"
    company = "packaged-owned-company"
    with TestClient(create_app(path)) as client:
        run = client.post(prefix + "/founding-runs", json={
            "owner_ref": "selfuse-ceo", "intent_ref": "routing-proof", "org_version": "v1",
        })
        assert run.status_code == 201, run.text
        ref = run.json()["entity_id"]
        for target, trigger in (("INTENT_CAPTURED", "capture_intent"),
                                ("CLARIFYING", "request_clarification"),
                                ("PROPOSED", "propose_company"),
                                ("CEO_CONFIRMED", "confirm_company")):
            response = client.post(prefix + f"/entities/{ref}/transition", json={
                "target": target, "trigger": trigger, "actor": "CEO", "reason": "isolated acceptance",
            })
            assert response.status_code == 200, response.text
        response = client.post(prefix + f"/founding-runs/{ref}/materialize-company", json={
            "company_id": company, "ceo_id": "selfuse-ceo", "name": "隔离路由验收公司",
        })
        assert response.status_code == 200, response.text
        for endpoint in ("attention", "conversations"):
            response = client.get(f"/api/workspace/v1/companies/{company}/{endpoint}")
            assert response.status_code == 200, response.text
            missing = client.get(f"/api/workspace/v1/companies/not-owned/{endpoint}")
            assert missing.status_code == 404
            assert missing.json()["detail"] != "Not Found"  # business denial, not missing route
    with TestClient(create_app(path)) as client:
        for endpoint in ("attention", "conversations"):
            response = client.get(f"/api/workspace/v1/companies/{company}/{endpoint}")
            assert response.status_code == 200, response.text
        assert client.get(f"/api/workspace/v1/companies/{company}/conversations").json() == {"conversations": []}

    # Deliberately invalid external fixture reproduces the previous Desktop seed.
    # Do not repair ownership or weaken the production access check.
    with Database(path).connect() as connection:
        connection.execute("update companies set ceo_id='ceo' where company_id=?", (company,))
    with TestClient(create_app(path)) as client:
        for endpoint in ("attention", "conversations"):
            response = client.get(f"/api/workspace/v1/companies/{company}/{endpoint}")
            assert response.status_code == 404
            assert response.json()["detail"] != "Not Found"
