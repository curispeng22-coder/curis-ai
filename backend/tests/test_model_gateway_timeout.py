"""Local failure regression; never substitutes for real cloud latency evidence."""
import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.model_gateway import ModelGatewayAdapter, ModelGatewayExecutionError, R3_PROFILE
from backend.tests.test_v1_meeting_autonomous_discussion import HEADERS, PREFIX, MeetingProvider, seed
from backend.tests.test_v1_meeting_employee_self_judgment import _create_meeting


def test_model_timeout_bound_and_clone_propagation(monkeypatch):
    monkeypatch.delenv("CURIS_MODEL_GATEWAY_PROFILE", raising=False)
    adapter = ModelGatewayAdapter(base_url="https://example.invalid", api_key="local-test-only", gateway_id="test", model_name="test")
    assert adapter.timeout == 90
    clone = adapter.with_model_metadata(gateway_id="test", model_name="other")
    assert clone.timeout == 90
    with patch("httpx.AsyncClient.post", side_effect=TimeoutError("test timeout")) as post:
        with pytest.raises(ModelGatewayExecutionError, match="test timeout") as error:
            clone.execute("bounded")
        assert error.value.status == "network_error" and error.value.outbound_attempted
        assert post.call_count == 1
    assert ModelGatewayAdapter(timeout=30).timeout == 30
    for bad in (0, -1, 91, True, float("inf"), float("nan"), "90"):
        with pytest.raises(ValueError):
            ModelGatewayAdapter(timeout=bad)
    monkeypatch.setenv("CURIS_MODEL_GATEWAY_PROFILE", R3_PROFILE)
    assert ModelGatewayAdapter().timeout == 60


def test_real_http_drip_is_cancelled_by_total_deadline():
    """Continuous bytes defeat an inactivity timeout, not a total deadline."""
    import threading
    import time
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    disconnected = threading.Event()

    class Drip(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            try:
                for _ in range(100):
                    self.wfile.write(b" ")
                    self.wfile.flush()
                    time.sleep(0.02)
            except (BrokenPipeError, ConnectionResetError):
                disconnected.set()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Drip)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        adapter = ModelGatewayAdapter(
            base_url=f"http://127.0.0.1:{server.server_port}", api_key="local-test-only",
            model_name="test", timeout=1,
        )
        started = time.monotonic()
        with pytest.raises(ModelGatewayExecutionError) as caught:
            adapter.execute("local bounded test")
        assert time.monotonic() - started < 1.8
        assert caught.value.outbound_attempted and caught.value.status == "network_error"
        assert disconnected.wait(1)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(1)


def test_meeting_timeout_finalization_usage_and_restart(tmp_path):
    path = tmp_path / "timeout.sqlite"
    database, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    adapter = provider.adapter()
    attempts = []

    def timed_out(_url, _payload, _headers, timeout):
        attempts.append(timeout)
        raise TimeoutError("The read operation timed out")

    adapter.http_post = timed_out
    meeting_id = _create_meeting(database, employees)
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        client.post(f"{PREFIX}/{meeting_id}/advance", headers=HEADERS)
        before = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    assert attempts == [90]
    assert before["orchestration"]["status"] == "BLOCKED"
    assert before["orchestration"]["usage"]["unknownMetering"] is True
    assert not before["decision_ref"] and before["result_refs"] == []
    with database.connect() as connection:
        assert connection.execute("select status from tasks").fetchone()[0] == "FAILED"
        usage = connection.execute("select execution_status,metering_status,total_tokens from ai_usage_records").fetchone()
        assert tuple(usage) == ("network_error", "unknown", None)
        for row in connection.execute("select data_json from runtime_entities where entity_type='WORK'"):
            assert not json.loads(row[0]).get("responsibilityRouting", {}).get("currentExecutorRef")
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        after = client.get(f"{PREFIX}/{meeting_id}", headers=HEADERS).json()
    assert after["orchestration"] == before["orchestration"]
    assert attempts == [90]
    with database.connect() as connection:
        assert connection.execute("select count(*) from ai_usage_records").fetchone()[0] == 1


def test_interrupted_task_requires_explicit_resume(tmp_path, monkeypatch):
    import asyncio
    import inspect
    from app.orchestrator import Orchestrator
    from app.tenant_context import TenantContext
    from backend.tests.test_v1_meeting_autonomous_discussion import COMPANY, TENANT, WORKSPACE

    path = tmp_path / "interrupted.sqlite"
    db, employees, knowledge = seed(path)
    provider = MeetingProvider(knowledge)
    mid = _create_meeting(db, employees)
    captured = []
    original = Orchestrator.run

    async def interrupted(self, task_id):
        self.store.transition(task_id, "PARSED")
        self.store.transition(task_id, "RUNNING")
        captured.append(task_id)
        raise RuntimeError("test process lost before final outcome")

    monkeypatch.setattr(Orchestrator, "run", interrupted)
    with TestClient(create_app(str(path), model_gateway_adapter=provider.adapter())) as client:
        client.post(f"{PREFIX}/{mid}/advance", headers=HEADERS)
    monkeypatch.setattr(Orchestrator, "run", original)
    app = create_app(str(path), model_gateway_adapter=provider.adapter())
    route = next(r for r in app.routes if r.path.endswith("/meetings/{meeting_id}/advance"))
    schedule = inspect.getclosurevars(route.endpoint).nonlocals["schedule"]
    bridge = inspect.getclosurevars(schedule).nonlocals["employee_execution"]
    with db.connect() as connection:
        row = dict(connection.execute("select * from tasks where task_id=?", (captured[0],)).fetchone())
    request = dict(execution_ref="team_employee:auto", mode="run", task_ref=row["task_id"],
                   company_id=COMPANY, workspace_id=WORKSPACE, runtime_employee_ref=row["employee_id"],
                   execution_key=row["execution_ref"])
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
        first = asyncio.run(bridge(request))
        second = asyncio.run(bridge(request))
    assert first["task_status"] == second["task_status"] == "AWAITING_INPUT"
    assert provider.calls == []
    with TestClient(app) as client:
        resumed = client.post(f"/api/workspace/task-runs/{row['task_id']}/resume", headers=HEADERS,
                              json={"resume_parameters": {"confirmation": "隔离测试确认重试"}})
        assert resumed.status_code == 202, resumed.text
    assert len(provider.calls) == 1


def test_explicit_target_resolution_failure_never_calls_http(monkeypatch):
    monkeypatch.delenv("CURIS_MODEL_GATEWAY_PROFILE", raising=False)
    def forbidden(*args, **kwargs):
        raise AssertionError("HTTP must not run")
    def broken(_):
        raise OSError("synthetic resolver unavailable")
    adapter = ModelGatewayAdapter(base_url="https://default.invalid", api_key="test-only",
                                  gateway_id="default", model_name="default-model",
                                  gateway_resolver=broken, http_post=forbidden)
    with pytest.raises(ModelGatewayExecutionError) as error:
        adapter.with_model_metadata(gateway_id="selected", model_name="selected-model")
    assert error.value.status == "configuration_rejected"
    assert error.value.outbound_attempted is False
