#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SEED_PATH = ROOT / "docs" / "demo" / "phase7-demo-seed.json"
SECRET_VALUE = "demo-local-credential-value"


def main() -> int:
    sys.path.insert(0, str(BACKEND))

    from fastapi.testclient import TestClient

    from app.main import create_app
    from app.model_gateway import ModelGatewayAdapter

    seed = json.loads(SEED_PATH.read_text())
    gateway_calls: list[dict[str, Any]] = []

    def fake_http_post(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> dict[str, Any]:
        gateway_calls.append({"url": url, "payload": payload, "headers": headers, "timeout": timeout})
        return {
            "choices": [
                {
                    "message": {
                        "content": f"Phase-7 stable demo step result {len(gateway_calls)}",
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 11,
                "completion_tokens": 13,
                "total_tokens": 24,
                "estimated_cost": 0.000024,
            },
            "model": seed["private_model"]["model_name"],
        }

    db_handle = tempfile.NamedTemporaryFile(prefix="curis_phase7_demo_", suffix=".sqlite", delete=False)
    db_path = db_handle.name
    db_handle.close()
    previous_env = os.environ.get("CURIS_ENV")
    os.environ["CURIS_ENV"] = "local"

    try:
        client = TestClient(
            create_app(
                db_path,
                model_gateway_adapter=ModelGatewayAdapter(
                    base_url=seed["private_model"]["base_url"],
                    api_key="fallback-demo-key",
                    model_name=seed["private_model"]["model_name"],
                    http_post=fake_http_post,
                ),
            )
        )
        result = run_demo(client, seed, gateway_calls)
    finally:
        if previous_env is None:
            os.environ.pop("CURIS_ENV", None)
        else:
            os.environ["CURIS_ENV"] = previous_env
        try:
            os.unlink(db_path)
        except FileNotFoundError:
            pass

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def run_demo(client: Any, seed: dict[str, Any], gateway_calls: list[dict[str, Any]]) -> dict[str, Any]:
    tenant_headers = {"X-Tenant-Id": seed["tenant_id"], "X-Ceo-Id": seed["ceo_id"]}
    other_tenant_headers = {"X-Tenant-Id": "other-tenant", "X-Ceo-Id": "other-ceo"}
    admin_headers = {"Authorization": "Bearer platform-admin-dev"}

    _expect(client.get("/health").json()["status"] == "ok", "health must be ok")

    credential = _post(
        client,
        "/api/workspace/credentials",
        tenant_headers,
        {
            "name": seed["credential"]["name"],
            "provider": seed["credential"]["provider"],
            "credential_type": seed["credential"]["credential_type"],
            "secret": SECRET_VALUE,
        },
        201,
    )
    _expect(SECRET_VALUE not in json.dumps(credential), "credential response leaked secret")
    credential_ref = credential["credential_ref"]

    private_model_payload = {
        "name": seed["private_model"]["name"],
        "provider_type": seed["private_model"]["provider_type"],
        "base_url": seed["private_model"]["base_url"],
        "model_name": seed["private_model"]["model_name"],
        "credential_ref": credential_ref,
        "enabled": True,
    }
    private_model = _post(client, "/api/workspace/private-models", tenant_headers, private_model_payload, 201)
    _expect(SECRET_VALUE not in json.dumps(private_model), "private model response leaked secret")

    private_tool = _post(
        client,
        "/api/workspace/private-tools",
        tenant_headers,
        {
            "name": "phase7-private-tool",
            "type": "demo_tool",
            "description": "Phase-7 local demo private tool metadata.",
            "config_ref": credential_ref,
            "enabled": True,
        },
        201,
    )
    private_connector = _post(
        client,
        "/api/workspace/private-connectors",
        tenant_headers,
        {
            "name": "phase7-private-connector",
            "connector_type": "demo_connector",
            "config_ref": credential_ref,
            "enabled": True,
        },
        201,
    )

    department = _post(
        client,
        "/api/workspace/departments",
        tenant_headers,
        {
            "template_id": seed["department"]["template_id"],
            "name": seed["department"]["name"],
            "company_id": seed["company_id"],
            "enabled": True,
        },
        201,
    )

    templates = _get(client, "/api/workspace/employee-templates", tenant_headers)["employee_templates"]
    template_by_role = {template["role"]: template["id"] for template in templates}
    employees: dict[str, dict[str, Any]] = {}
    for role in seed["employees"]:
        employee = _post(
            client,
            "/api/workspace/employees",
            tenant_headers,
            {
                "department_id": department["id"],
                "template_id": template_by_role[role],
                "name": f"Phase-7 {role}",
                "company_id": seed["company_id"],
                "instructions_override": f"Use bound capability as {role}.",
                "status": "idle",
                "enabled": True,
            },
            201,
        )
        employees[role] = employee
        _put(
            client,
            f"/api/workspace/employees/{employee['id']}/capabilities",
            tenant_headers,
            {
                "bindings": [
                    {
                        "capability_source": "tenant_private",
                        "capability_type": "model",
                        "capability_id": seed["private_model"]["name"],
                        "priority": 1,
                        "enabled": True,
                    }
                ]
            },
            200,
        )

    selector = _get(client, "/api/workspace/capabilities/selector", tenant_headers)
    selector_json = json.dumps(selector)
    _expect('"source": "official"' in selector_json or '"source":"official"' in selector_json, "selector must include official capabilities")
    _expect(seed["private_model"]["name"] in selector_json, "selector must include tenant_private model")

    workflow = _post(
        client,
        "/api/workspace/workflows",
        tenant_headers,
        {
            "workflow_template_id": seed["workflow"]["workflow_template_id"],
            "department_id": department["id"],
            "name": seed["workflow"]["name"],
            "content": seed["workflow"]["content"],
        },
        201,
    )
    workflow_run_id = workflow["workflow_run_id"]
    statuses = []
    for _ in range(7):
        run = _post(client, f"/api/workspace/workflows/{workflow_run_id}/run-next-step", tenant_headers, None, 200)
        statuses.append(run["status"])

    detail = _get(client, f"/api/workspace/workflows/{workflow_run_id}", tenant_headers)
    _expect(detail["status"] == "succeeded", "workflow must succeed")
    _expect(len(detail["steps"]) == 7, "workflow must have seven steps")
    _expect(len(detail["step_results"]) == 7, "workflow must have seven step results")
    _expect("Phase-7 stable demo step result" in detail["final_report"], "final report must include gateway result")

    usage = _get(client, f"/api/platform/usage?tenant_id={seed['tenant_id']}&capability_source=tenant_private", admin_headers)
    usage_events = usage["usage_events"]
    model_calls = [event for event in usage_events if event["event_type"] == "usage.model_call"]
    _expect(len(model_calls) == 7, "usage_event must include seven model calls")
    for event in model_calls:
        _expect(event["workflow_run_id"] == workflow_run_id, "usage_event missing workflow_run_id")
        _expect(event["workflow_step_id"], "usage_event missing workflow_step_id")
        _expect(event["employee_id"], "usage_event missing employee_id")
        _expect(event["capability_source"] == "tenant_private", "usage_event must mark tenant_private source")
        _expect(event["capability_id"] == seed["private_model"]["name"], "usage_event capability_id mismatch")
        _expect(event["credential_id"] == credential["credential_id"], "usage_event credential attribution mismatch")
    _expect(SECRET_VALUE not in json.dumps(usage_events), "usage_event leaked secret")

    audit = _get(client, f"/api/platform/audit?tenant_id={seed['tenant_id']}&event_type=workflow.run.completed", admin_headers)
    _expect(len(audit["audit_events"]) == 1, "audit_event must include workflow.run.completed")
    _expect(SECRET_VALUE not in json.dumps(audit), "audit_event leaked secret")

    isolated = client.get(f"/api/workspace/workflows/{workflow_run_id}", headers=other_tenant_headers)
    _expect(isolated.status_code == 404, "cross-tenant workflow read must be rejected")

    _expect(gateway_calls, "model gateway must be called")
    _expect(gateway_calls[-1]["headers"].get("Authorization") == f"Bearer {SECRET_VALUE}", "resolver must supply credential only to server-side gateway call")

    public_payload = json.dumps(
        {
            "credential": credential,
            "private_model": private_model,
            "private_tool": private_tool,
            "private_connector": private_connector,
            "workflow_detail": detail,
            "usage": usage,
            "audit": audit,
        },
        ensure_ascii=False,
    )
    _expect(SECRET_VALUE not in public_payload, "public demo payload leaked secret")

    return {
        "status": "PASS",
        "tenant_id": seed["tenant_id"],
        "workflow_run_id": workflow_run_id,
        "workflow_statuses": statuses,
        "step_count": len(detail["steps"]),
        "step_result_count": len(detail["step_results"]),
        "usage_model_call_count": len(model_calls),
        "audit_completed_count": len(audit["audit_events"]),
        "tenant_isolation": "PASS",
        "secret_leakage": "PASS",
        "admin_plaintext_visibility": "BLOCKED",
        "workspace_runtime_platform_calls": "not exercised by runtime path",
    }


def _get(client: Any, path: str, headers: dict[str, str]) -> dict[str, Any]:
    response = client.get(path, headers=headers)
    _expect(response.status_code == 200, f"GET {path} returned {response.status_code}: {response.text}")
    return response.json()


def _post(client: Any, path: str, headers: dict[str, str], payload: dict[str, Any] | None, status_code: int) -> dict[str, Any]:
    response = client.post(path, headers=headers, json=payload) if payload is not None else client.post(path, headers=headers)
    _expect(response.status_code == status_code, f"POST {path} returned {response.status_code}: {response.text}")
    return response.json()


def _put(client: Any, path: str, headers: dict[str, str], payload: dict[str, Any], status_code: int) -> dict[str, Any]:
    response = client.put(path, headers=headers, json=payload)
    _expect(response.status_code == status_code, f"PUT {path} returned {response.status_code}: {response.text}")
    return response.json()


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    raise SystemExit(main())
