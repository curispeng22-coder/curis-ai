from __future__ import annotations

import re
import sqlite3
import urllib.error
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.ai_usage import AIUsageService
from app.business_metrics import BusinessMetricService
from app.evolution_event_log import EvolutionEventLog
from app.main import create_app
from app.model_gateway import ModelGatewayAdapter
from app.result_store import ResultStore
from app.runtime.general_workspace_delivery import GeneralWorkspaceDelivery
from app.tenant_context import TenantContext
from backend.tests.test_v1_general_operating_contract import (
    BUSINESS,
    COMPANY,
    EMPLOYEE,
    TENANT,
    WORKSPACE,
    add_team,
    seed,
)


PREFIX = "/api/workspace/runtime/foundation/team-operating"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": "ceo"}


class _CanonicalProvider:
    def __init__(self):
        self.calls = []

    def __call__(self, url, payload, headers, timeout):
        self.calls.append(payload)
        match = re.search(r"输出结果类型：([^\n]+)", payload["messages"][-1]["content"])
        result_type = match.group(1).strip() if match else "general-business-result"
        return {
            "choices": [{"message": {"content": (
                '{"status":"ACCEPTED","resultType":"' + result_type
                + '","summary":"完成","problem":""}'
            )}}],
            "usage": {"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7},
        }


class _FailingProvider(_CanonicalProvider):
    def __call__(self, url, payload, headers, timeout):
        self.calls.append(payload)
        raise urllib.error.HTTPError(url, 503, "unavailable", {}, None)


def _execute_one(path, provider=None):
    provider = provider or _CanonicalProvider()
    adapter = ModelGatewayAdapter(
        base_url="https://provider.invalid", api_key="test-only",
        gateway_id="canonical-gateway", model_name="canonical-model", http_post=provider,
    )
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        database = seed(path)
        add_team(database)
        with database.connect() as connection:
            connection.execute("delete from employee_capability_bindings")
            connection.execute(
                "insert or replace into official_models(model_key, provider_id, display_name, "
                "supported_models, gateway_ref, status, default_model, type, name) "
                "values ('model.canonical', 'canonical-provider', 'Canonical', "
                "'[\"canonical-model\"]', 'canonical-gateway', 'active', "
                "'canonical-model', 'model', 'Canonical')"
            )
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, "
                "capability_source, capability_type, capability_id) "
                "values ('binding-model-general', ?, ?, 'official', 'model', 'model.canonical')",
                (TENANT, EMPLOYEE),
            )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            work = GeneralWorkspaceDelivery(database).create_work(
                company_id=COMPANY, workspace_id=WORKSPACE,
                problem="整理本周客户反馈", expected_result="形成一项有证据的改进建议",
                constraints=["只使用已提供资料"], references=["brief:customer-feedback"],
                idempotency_key="canonical-usage-work",
            )["work"]
        response = client.post(
            f"{PREFIX}/works/{work['entity_id']}/execute?max_executions=1", headers=HEADERS
        )
        assert response.status_code == 200, response.text
        if response.json()["work"]["data"]["responsibilityRouting"]["status"] == "COMPLETED":
            replay = client.post(
                f"{PREFIX}/works/{work['entity_id']}/execute?max_executions=1", headers=HEADERS
            )
            assert replay.status_code == 200, replay.text
    return database, provider, work["entity_id"]


def test_general_workspace_records_canonical_usage_without_project_and_survives_restart(tmp_path):
    path = tmp_path / "canonical.sqlite"
    database, provider, work_ref = _execute_one(path)
    assert len(provider.calls) == 1

    with TenantContext.scope(TENANT):
        first = AIUsageService(database).list_records(work_ref=work_ref)
    assert len(first) == 1
    record = first[0]
    assert record["company_id"] == COMPANY
    assert record["business_id"] == BUSINESS
    assert record["workspace_id"] == WORKSPACE
    assert record["work_ref"] == work_ref
    assert record["execution_ref"]
    assert record["project_id"] is None

    restarted = type(database)(str(path))
    restarted.initialize()
    with TenantContext.scope(TENANT):
        after_restart = AIUsageService(restarted).get_record(record["usage_record_id"])
    with restarted.connect() as connection:
        task = connection.execute(
            "select workspace_id, work_ref, execution_ref from tasks where task_id=?",
            (record["task_id"],),
        ).fetchone()
    assert after_restart == record
    assert tuple(task) == (WORKSPACE, work_ref, record["execution_ref"])

    with restarted.connect() as connection:
        payloads = [
            item["payload"] for item in connection.execute(
                "select payload from evolution_events where correlation_id=? "
                "and event_type in ('execution_started','usage.model_call')",
                (record["task_id"],),
            )
        ]
    assert payloads and all(WORKSPACE in payload and work_ref in payload for payload in payloads)


def test_canonical_usage_matches_current_task_when_work_has_multiple_execution_attempts(tmp_path):
    database, _, work_ref = _execute_one(tmp_path / "retry-attribution.sqlite")
    with TenantContext.scope(TENANT):
        record = AIUsageService(database).list_records(work_ref=work_ref)[0]
    with database.connect() as connection:
        event = connection.execute(
            "select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='team.execution_task_bound'",
            (TENANT, work_ref),
        ).fetchone()
        payload = event["payload"].replace(record["task_id"], "later-task", 1)
        connection.execute(
            "insert into evolution_events(tenant_id, event_type, payload, correlation_id, idempotency_key) "
            "values (?, 'team.execution_task_bound', ?, ?, 'later-execution-bound')",
            (TENANT, payload, work_ref),
        )

    with TenantContext.scope(TENANT):
        attribution = AIUsageService(database).validate_business_context(
            tenant_id=TENANT,
            employee_id=record["employee_id"],
            capability_id=record["capability_id"],
            capability_type=record["capability_type"],
            task_id=record["task_id"],
            capability_binding_id=record["capability_binding_id"],
        )
    assert attribution["work_ref"] == work_ref
    assert attribution["execution_ref"] == record["execution_ref"]


@pytest.mark.parametrize(
    ("mutation", "kwargs"),
    [
        ("update tasks set company_id='wrong-company' where task_id=?", {}),
        ("update tasks set work_ref='wrong-work' where task_id=?", {}),
        (None, {"employee_id": "wrong-employee"}),
        (None, {"capability_id": "wrong-capability"}),
        (None, {"project_id": "synthetic-project"}),
    ],
)
def test_conflicting_canonical_claims_fail_closed(mutation, kwargs, tmp_path):
    path = tmp_path / "conflict.sqlite"
    database, provider, work_ref = _execute_one(path)
    with TenantContext.scope(TENANT):
        record = AIUsageService(database).list_records(work_ref=work_ref)[0]
    if mutation:
        target = WORKSPACE if "workspaces" in mutation else record["task_id"]
        with database.connect() as connection:
            connection.execute(mutation, (target,))

    claims = {
        "tenant_id": TENANT,
        "employee_id": record["employee_id"],
        "capability_id": record["capability_id"],
        "capability_type": record["capability_type"],
        "task_id": record["task_id"],
        "capability_binding_id": record["capability_binding_id"],
        **kwargs,
    }
    with TenantContext.scope(TENANT), pytest.raises((KeyError, ValueError)):
        AIUsageService(database).validate_business_context(**claims)
    assert len(provider.calls) == 1


def test_wrong_business_relation_is_rejected_by_canonical_database_contract(tmp_path):
    database, provider, _ = _execute_one(tmp_path / "wrong-business.sqlite")
    with database.connect() as connection, pytest.raises(sqlite3.IntegrityError, match="business missing"):
        connection.execute(
            "update workspaces set business_id='wrong-business' where workspace_id=?",
            (WORKSPACE,),
        )
    assert len(provider.calls) == 1


def test_cross_tenant_canonical_claim_is_rejected(tmp_path):
    database, provider, work_ref = _execute_one(tmp_path / "cross-tenant.sqlite")
    with TenantContext.scope(TENANT):
        record = AIUsageService(database).list_records(work_ref=work_ref)[0]
    with TenantContext.scope("other-tenant"), pytest.raises(PermissionError):
        AIUsageService(database).validate_business_context(
            tenant_id=TENANT,
            employee_id=record["employee_id"],
            capability_id=record["capability_id"],
            capability_type=record["capability_type"],
            task_id=record["task_id"],
            capability_binding_id=record["capability_binding_id"],
        )
    assert len(provider.calls) == 1


def test_invalid_parent_is_rejected_before_provider_launch(tmp_path):
    path = tmp_path / "preflight.sqlite"
    provider = _CanonicalProvider()
    adapter = ModelGatewayAdapter(
        base_url="https://provider.invalid", api_key="test-only",
        gateway_id="canonical-gateway", model_name="canonical-model", http_post=provider,
    )
    with TestClient(create_app(str(path), model_gateway_adapter=adapter)) as client:
        database = seed(path)
        add_team(database)
        with database.connect() as connection:
            connection.execute("delete from employee_capability_bindings")
            connection.execute(
                "insert or replace into official_models(model_key, provider_id, display_name, "
                "supported_models, gateway_ref, status, default_model, type, name) "
                "values ('model.canonical', 'canonical-provider', 'Canonical', "
                "'[\"canonical-model\"]', 'canonical-gateway', 'active', "
                "'canonical-model', 'model', 'Canonical')"
            )
            connection.execute(
                "insert into employee_capability_bindings(id, tenant_id, employee_id, "
                "capability_source, capability_type, capability_id) "
                "values ('binding-model-general', ?, ?, 'official', 'model', 'model.canonical')",
                (TENANT, EMPLOYEE),
            )
        with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id="ceo", role="test"):
            work = GeneralWorkspaceDelivery(database).create_work(
                company_id=COMPANY, workspace_id=WORKSPACE,
                problem="整理本周客户反馈", expected_result="形成改进建议",
                constraints=[], references=[], idempotency_key="invalid-parent-work",
            )["work"]
        with database.connect() as connection:
            connection.execute(
                "update workspaces set business_relation_status='QUARANTINED' where workspace_id=?",
                (WORKSPACE,),
            )
        response = client.post(
            f"{PREFIX}/works/{work['entity_id']}/execute?max_executions=1", headers=HEADERS
        )
        assert response.status_code == 422, response.text
        assert "canonical Company lineage" in response.json()["detail"]
    assert provider.calls == []


def test_failed_provider_attempt_keeps_canonical_attribution_without_fake_completion(tmp_path):
    database, provider, work_ref = _execute_one(
        tmp_path / "failed-provider.sqlite", _FailingProvider()
    )
    with TenantContext.scope(TENANT):
        records = AIUsageService(database).list_records(work_ref=work_ref)
    assert provider.calls
    assert records
    assert all(record["project_id"] is None for record in records)
    assert all(record["workspace_id"] == WORKSPACE for record in records)
    assert all(record["execution_status"] != "success" for record in records)
    with database.connect() as connection:
        task = connection.execute(
            "select status from tasks where task_id=?", (records[0]["task_id"],)
        ).fetchone()
        assert task["status"] == "FAILED"
        assert connection.execute(
            "select count(*) from artifacts where task_id=?", (records[0]["task_id"],)
        ).fetchone()[0] == 0


def test_company_metrics_count_canonical_and_legacy_usage_once(tmp_path):
    database, _provider, work_ref = _execute_one(tmp_path / "metrics.sqlite")
    with TenantContext.scope(TENANT):
        service = AIUsageService(database)
        canonical = service.list_records(work_ref=work_ref)[0]
        service.record_call(
            tenant_id=TENANT, model_gateway_id="gateway", provider_id="provider",
            model_name="model", input_tokens=1, output_tokens=1, total_tokens=2,
            cost_amount=Decimal("0.25"), currency="USD", cost_source="estimated",
            price_version="v1", employee_id=canonical["employee_id"],
            capability_id=canonical["capability_id"], capability_type=canonical["capability_type"],
            task_id=canonical["task_id"], project_id=None,
            department_id=canonical["department_id"], request_id="canonical-cost",
            execution_status="success", metering_status="confirmed",
            idempotency_key="canonical-cost", capability_binding_id=canonical["capability_binding_id"],
        )
        with database.connect() as connection:
            connection.execute(
                "insert into projects(project_id, tenant_id, company_id, department_id, name, goal) "
                "values ('legacy-project', ?, ?, 'department', 'Legacy', 'Compatibility')",
                (TENANT, COMPANY),
            )
        legacy_task = ResultStore(database).create_task(
            "legacy", company_id=COMPANY, project_id="legacy-project",
            capability_source="official", capability_type="model",
            capability_id="model.canonical", employee_id=EMPLOYEE,
        )
        service.record_call(
            tenant_id=TENANT, model_gateway_id="gateway", provider_id="provider",
            model_name="model", input_tokens=1, output_tokens=1, total_tokens=2,
            cost_amount=Decimal("0.50"), currency="USD", cost_source="estimated",
            price_version="v1", employee_id=EMPLOYEE, capability_id="model.canonical",
            capability_type="model", task_id=legacy_task["task_id"],
            project_id="legacy-project", department_id="department", request_id="legacy-cost",
            execution_status="success", metering_status="confirmed", idempotency_key="legacy-cost",
            capability_binding_id="binding-model-general",
        )
        metrics = BusinessMetricService(database, EvolutionEventLog(database)).compute(
            COMPANY, "day:2026-08-27"
        )
    assert metrics["estimated_cost"]["value"] is None  # one actual outbound call is unpriced
    with TenantContext.scope(TENANT):
        assert service.aggregate(company_id=COMPANY)["totals"]["estimated_cost"] == "0.75"
