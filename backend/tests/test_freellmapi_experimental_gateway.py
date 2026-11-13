from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading

from fastapi.testclient import TestClient
import pytest

from backend.app.database import Database
from backend.app.evolution_event_log import EvolutionEventLog
from backend.app.main import create_app
from backend.app.model_catalog import GatewayCatalog
from backend.app.model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError


def _configure(monkeypatch, *, trusted_cidr: str = "127.0.0.1/32") -> None:
    monkeypatch.setenv("CURIS_PRODUCT", "workspace")
    monkeypatch.setenv("CURIS_ENV", "development")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "gateway")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_ISSUER", "https://quality.issuer.local")
    monkeypatch.setenv("CURIS_TRUSTED_GATEWAY_CIDRS", trusted_cidr)
    monkeypatch.setenv("CURIS_IDENTITY_AUDIT_KEY", "freellmapi-focused-audit-key")
    monkeypatch.setenv("CURIS_LOCAL_OWNER_ENABLED", "1")
    monkeypatch.setenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "0")
    monkeypatch.setenv("FREELLMAPI_API_KEY", "freellmapi-focused-secret")


def _gateway(db_path, *, base_url: str = "http://127.0.0.1:3101") -> GatewayCatalog:
    database = Database(str(db_path))
    catalog = GatewayCatalog(database, EvolutionEventLog(database))
    catalog.create(
        gateway_id="freellmapi.experimental",
        name="FreeLLMAPI Experimental",
        gateway_type="newapi",
        base_url=base_url,
        status="inactive",
        credential_ref="env:FREELLMAPI_API_KEY",
        default_model="auto",
    )
    return catalog


def _client(app, host: str):
    @app.middleware("http")
    async def fixed_client(request, call_next):
        request.scope["client"] = (host, 12345)
        return await call_next(request)

    return TestClient(app)


def test_registration_is_private_inactive_and_workspace_hidden(tmp_path):
    database = Database(str(tmp_path / "catalog.sqlite"))
    database.initialize()
    catalog = GatewayCatalog(database, EvolutionEventLog(database))
    with pytest.raises(ValueError, match="本机或容器内网"):
        catalog.create(
            "freellmapi.experimental",
            "FreeLLMAPI Experimental",
            "newapi",
            "https://public.example.com",
            "inactive",
            "env:FREELLMAPI_API_KEY",
            "auto",
        )
    with pytest.raises(ValueError, match="本机或容器内网"):
        catalog.create(
            "freellmapi.experimental",
            "FreeLLMAPI Experimental",
            "newapi",
            "http://169.254.169.254:3001",
            "inactive",
            "env:FREELLMAPI_API_KEY",
            "auto",
        )
    with pytest.raises(ValueError, match="首次登记必须为 inactive"):
        catalog.create(
            "freellmapi.experimental",
            "FreeLLMAPI Experimental",
            "newapi",
            "http://127.0.0.1:3101",
            "active",
            "env:FREELLMAPI_API_KEY",
            "auto",
        )
    _gateway(tmp_path / "catalog.sqlite")
    assert all(
        row["gateway_id"] != "freellmapi.experimental"
        for row in database.list_catalog_gateways()
    )
    with pytest.raises(ValueError, match="Owner-local"):
        catalog.set_status("freellmapi.experimental", "active")
    with pytest.raises(ValueError, match="Workspace 官方模型"):
        database.save_official_model(
            "official.freellmapi.auto",
            "freellmapi",
            "FreeLLMAPI Auto",
            ["auto"],
            gateway_ref="freellmapi.experimental",
            default_model="auto",
        )
    with pytest.raises(ValueError, match="Workspace 私有模型"):
        database.save_tenant_private_capability(
            tenant_id="selfuse",
            capability_type="model",
            capability_id="private.freellmapi",
            metadata={
                "provider_type": "freellmapi.experimental",
                "base_url": "http://127.0.0.1:3101",
                "model_name": "auto",
            },
        )


def test_local_owner_verifies_and_activates_without_exposing_content(tmp_path, monkeypatch):
    _configure(monkeypatch)
    calls = []

    def fake_post(url, payload, headers, timeout):
        calls.append((url, payload, headers, timeout))
        return {
            "model": "provider-default",
            "choices": [{"message": {"content": "CURIS_FREELLMAPI_OWNER_LOCAL_OK"}}],
            "usage": {"prompt_tokens": 7, "completion_tokens": 3, "total_tokens": 10},
            "__curis_routed_via": "groq/llama-3.3-70b-versatile",
        }

    db_path = tmp_path / "owner.sqlite"
    app = create_app(
        str(db_path),
        model_gateway_adapter=ModelGatewayAdapter(http_post=fake_post),
    )
    catalog = _gateway(db_path)
    with catalog.database.connect() as connection:
        connection.execute(
            "insert into official_models "
            "(model_key, provider_id, display_name, supported_models, auth_type, "
            "source, gateway_ref, status, default_model, type, name) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "legacy.freellmapi.auto",
                "freellmapi",
                "Legacy FreeLLMAPI Auto",
                '["auto"]',
                "apikey",
                "official",
                "freellmapi.experimental",
                "active",
                "auto",
                "model",
                "Legacy FreeLLMAPI Auto",
            ),
        )
    with _client(app, "127.0.0.1") as client:
        assert client.post(
            "/api/auth/local/initialize",
            headers={"Origin": "http://127.0.0.1:3001"},
        ).status_code == 201
        available = client.get("/api/workspace/model-preference").json()["available_models"]
        assert all(
            model["gateway_ref"] != "freellmapi.experimental"
            for model in available
        )
        response = client.post("/api/owner/experimental-gateways/freellmapi/verify")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "gateway_id": "freellmapi.experimental",
        "provider_id": "groq",
        "model_name": "llama-3.3-70b-versatile",
        "status": "success",
        "http_status": 200,
        "latency_ms": response.json()["latency_ms"],
        "input_tokens": 7,
        "output_tokens": 3,
        "total_tokens": 10,
        "metering_status": "confirmed",
    }
    assert "output" not in response.json()
    assert calls[0][0] == "http://127.0.0.1:3101/v1/chat/completions"
    assert calls[0][1]["model"] == "auto"
    assert calls[0][1]["messages"][0]["content"].startswith("Return exactly")
    assert calls[0][2]["Authorization"] == "Bearer freellmapi-focused-secret"
    assert catalog.get("freellmapi.experimental")["status"] == "active"
    assert all(
        row["gateway_id"] != "freellmapi.experimental"
        for row in catalog.database.list_catalog_gateways()
    )
    event_text = json.dumps(
        EvolutionEventLog(catalog.database).get_all(),
        ensure_ascii=False,
    )
    assert "freellmapi-focused-secret" not in event_text
    assert "Return exactly" not in event_text
    assert "CURIS_FREELLMAPI_OWNER_LOCAL_OK" not in event_text


def test_non_owner_and_non_loopback_are_rejected(tmp_path, monkeypatch):
    _configure(monkeypatch, trusted_cidr="10.0.0.2/32")
    app = create_app(str(tmp_path / "boundary.sqlite"))
    _gateway(tmp_path / "boundary.sqlite")
    with _client(app, "10.0.0.2") as client:
        assert client.post(
            "/api/auth/local/initialize",
            headers={"Origin": "http://127.0.0.1:3001"},
        ).status_code == 201
        response = client.post("/api/owner/experimental-gateways/freellmapi/verify")
    assert response.status_code == 403
    assert response.json() == {"detail": "local_owner_required"}


def test_real_gateway_failure_is_not_reported_as_success(tmp_path, monkeypatch):
    _configure(monkeypatch)

    def failed_post(url, payload, headers, timeout):
        raise OSError(
            f"upstream unavailable {headers['Authorization']} "
            f"{payload['messages'][0]['content']}"
        )

    db_path = tmp_path / "failure.sqlite"
    app = create_app(
        str(db_path),
        model_gateway_adapter=ModelGatewayAdapter(http_post=failed_post),
    )
    catalog = _gateway(db_path)
    with _client(app, "127.0.0.1") as client:
        client.post(
            "/api/auth/local/initialize",
            headers={"Origin": "http://127.0.0.1:3001"},
        )
        response = client.post("/api/owner/experimental-gateways/freellmapi/verify")

    assert response.status_code == 502
    assert response.json()["detail"]["status"] == "network_error"
    assert catalog.get("freellmapi.experimental")["status"] == "inactive"
    persisted = json.dumps(
        EvolutionEventLog(catalog.database).get_all(),
        ensure_ascii=False,
    )
    assert "freellmapi-focused-secret" not in persisted
    assert "Return exactly" not in persisted


def test_sidecar_cannot_echo_secret_through_route_metadata(tmp_path, monkeypatch):
    _configure(monkeypatch)

    def hostile_post(url, payload, headers, timeout):
        return {
            "model": "auto",
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            "__curis_routed_via": "freellmapi-focused-secret/model",
        }

    db_path = tmp_path / "hostile-header.sqlite"
    app = create_app(
        str(db_path),
        model_gateway_adapter=ModelGatewayAdapter(http_post=hostile_post),
    )
    catalog = _gateway(db_path)
    with _client(app, "127.0.0.1") as client:
        client.post(
            "/api/auth/local/initialize",
            headers={"Origin": "http://127.0.0.1:3001"},
        )
        response = client.post("/api/owner/experimental-gateways/freellmapi/verify")

    assert response.status_code == 502
    assert response.json()["detail"]["status"] == "response_invalid"
    assert "freellmapi-focused-secret" not in response.text
    assert catalog.get("freellmapi.experimental")["status"] == "inactive"
    persisted = json.dumps(
        EvolutionEventLog(catalog.database).get_all(),
        ensure_ascii=False,
    )
    assert "freellmapi-focused-secret" not in persisted


def test_sidecar_redirect_is_not_followed_with_authorization():
    source_requests = []
    target_requests = []

    class TargetHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            target_requests.append(dict(self.headers))
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass

    target = ThreadingHTTPServer(("127.0.0.1", 0), TargetHandler)

    class RedirectHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            source_requests.append(dict(self.headers))
            self.send_response(302)
            self.send_header(
                "Location",
                f"http://127.0.0.1:{target.server_port}/capture",
            )
            self.end_headers()

        def log_message(self, format, *args):
            pass

    source = ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
    threads = [
        threading.Thread(target=server.serve_forever, daemon=True)
        for server in (target, source)
    ]
    for thread in threads:
        thread.start()
    try:
        adapter = ModelGatewayAdapter(
            base_url=f"http://127.0.0.1:{source.server_port}",
            api_key="freellmapi-redirect-secret",
            gateway_id="freellmapi.experimental",
            model_name="auto",
        )
        with pytest.raises(ModelGatewayExecutionError) as raised:
            adapter.execute("fixed synthetic prompt")
        assert raised.value.status == "gateway_error"
        assert raised.value.http_status == 302
        assert raised.value.outbound_attempted is True
        assert source_requests[0]["Authorization"] == "Bearer freellmapi-redirect-secret"
        assert target_requests == []
    finally:
        source.shutdown()
        target.shutdown()
        source.server_close()
        target.server_close()
