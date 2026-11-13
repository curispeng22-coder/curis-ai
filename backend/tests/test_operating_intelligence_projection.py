from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.result_store import ResultStore
from app.runtime import RuntimeFoundation
from app.runtime.business_spine import CanonicalBusinessSpine
from app.tenant_context import TenantContext


TENANT = "tenant-operating-intelligence"
COMPANY = "company-operating-intelligence"
CEO = "ceo-operating-intelligence"
DEPARTMENT = "department-operating-intelligence"
BUSINESS_A = "business-content"
BUSINESS_B = "business-brand"
EMPLOYEE = "employee-analyst"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO, "X-Role": "ceo"}


def _seed(path) -> tuple[Database, dict[str, str]]:
    database = Database(str(path))
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, ?, 'Curis Test', 'active')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, mission) "
            "values (?, ?, ?, 'template-analysis', '经营部', 'OPERATING', '理解经营事实')",
            (DEPARTMENT, TENANT, COMPANY),
        )
        connection.execute(
            "insert into employee_templates(id, name, role, source, tenant_id) values ('template-analyst', '经营分析师', '经营分析师', 'tenant_private', ?)",
            (TENANT,),
        )
        connection.execute(
            "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
            "values (?, ?, ?, ?, 'template-analyst', '衡川', '经营分析师', 'idle')",
            (EMPLOYEE, TENANT, COMPANY, DEPARTMENT),
        )
    workspaces = {}
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        spine = CanonicalBusinessSpine(database)
        for business_id, name in ((BUSINESS_A, "内容增长"), (BUSINESS_B, "品牌经营")):
            business = spine.create_draft_with_first_workspace(
                company_id=COMPANY, department_id=DEPARTMENT, business_id=business_id,
                name=name, goal=f"持续经营{name}", positioning="测试定位",
                workspace_name=f"{name}工作空间", business_type="GENERIC",
                blueprint_version="v1", blueprint={"surfaces": []},
            )
            workspace_id = business["workspaces"][0]["workspace_id"]
            workspaces[business_id] = workspace_id
            at = datetime.now(timezone.utc).isoformat()
            with database.connect() as connection:
                connection.execute(
                    "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                    "values (?, ?, 'WORK', ?, ?, ?, 'COMPLETED', 'VERIFIED', 'SATISFIED', ?, ?, ?)",
                    (f"work-{business_id}", TENANT, COMPANY, workspace_id, EMPLOYEE, json.dumps({"problem": f"分析{name}", "expectedResult": "真实结果"}, ensure_ascii=False), at, at),
                )
    return database, workspaces


def _usage(database: Database, business_id: str, workspace_id: str, *, offset_days: int, suffix: str, cost: str, latency: int, status: str = "completed", currency: str = "CNY") -> None:
    at = (datetime.now(timezone.utc) - timedelta(days=offset_days)).isoformat()
    task_id = f"task-{business_id}-{suffix}"
    with database.connect() as connection:
        connection.execute(
            "insert into tasks(task_id, tenant_id, company_id, workspace_id, work_ref, execution_ref, content, status, state_flow, employee_id) "
            "values (?, ?, ?, ?, ?, ?, '分析经营事实', 'COMPLETED', '[\"INIT\",\"COMPLETED\"]', ?)",
            (task_id, TENANT, COMPANY, workspace_id, f"work-{business_id}", f"execution-{suffix}", EMPLOYEE),
        )
        connection.execute(
            "insert into ai_usage_records(usage_record_id, tenant_id, company_id, model_gateway_id, provider_id, model_name, "
            "input_tokens, output_tokens, total_tokens, cost_amount, currency, cost_source, employee_id, capability_id, capability_type, "
            "task_id, department_id, business_id, workspace_id, work_ref, execution_ref, request_id, execution_status, metering_status, occurred_at, idempotency_key, latency_ms) "
            "values (?, ?, ?, 'gateway', 'provider', 'model', 10, 5, 15, ?, ?, 'provider_reported', ?, 'model.test', 'model', ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?, ?, ?)",
            (f"usage-{business_id}-{suffix}", TENANT, COMPANY, cost, currency, EMPLOYEE, task_id, DEPARTMENT, business_id, workspace_id, f"work-{business_id}", f"execution-{suffix}", f"request-{suffix}", status, at, f"usage-key-{business_id}-{suffix}", latency),
        )


def _acceptance(database: Database, workspace_id: str, *, accepted: bool, offset_days: int, suffix: str) -> None:
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        item = RuntimeFoundation(database).create(
            "ACCEPTANCE", entity_id=f"acceptance-{suffix}", company_id=COMPANY,
            workspace_id=workspace_id, lifecycle_status="ACCEPTED" if accepted else "REJECTED",
            data={"source": "CEO"},
        )
    at = (datetime.now(timezone.utc) - timedelta(days=offset_days)).isoformat()
    with database.connect() as connection:
        connection.execute(
            "update runtime_entities set created_at=?, updated_at=? where tenant_id=? and entity_id=?",
            (at, at, TENANT, item["entity_id"]),
        )


def _report(database: Database, workspace_id: str) -> str:
    with TenantContext.scope(TENANT):
        store = ResultStore(database)
        task = store.create_task(
            "形成内容增长经营分析", company_id=COMPANY, workspace_id=workspace_id,
            work_ref=f"work-{BUSINESS_A}", execution_ref="execution-report", employee_id=EMPLOYEE,
        )
        store.transition(task["task_id"], "COMPLETED", {"output": "经营分析已经完成"})
        content = {
            "scope": {"type": "BUSINESS", "ref": BUSINESS_A},
            "period": {"days": 30},
            "facts": [{"value": "两次真实模型调用", "provenance": "FACT"}],
            "analysis": [{"value": "样本仍有限", "provenance": "EVIDENCE"}],
            "unknown": [{"value": "外部业务结果未连接", "provenance": "UNK"}],
            "recommendation": {"value": "继续观察", "provenance": "EVIDENCE"},
            "evidenceRefs": ["usage-business-content-current-1"],
            "author": {"employeeRef": EMPLOYEE, "name": "衡川"},
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "decisionCandidate": {
                "event": "内容增长成本投入是否需要调整",
                "cannotDecideReason": "涉及经营投入取舍，需要 CEO 判断",
                "options": [
                    {"optionId": "hold", "label": "维持投入", "impact": {"value": "维持当前节奏", "provenance": "FACT"}, "risk": {"value": "外部结果仍未知", "provenance": "UNK"}, "cost": {"value": "按现有成本继续", "provenance": "EVIDENCE"}},
                    {"optionId": "pause", "label": "暂缓新增投入", "impact": {"value": "等待更多事实", "provenance": "FACT"}, "risk": {"value": "可能延后验证", "provenance": "EST"}, "cost": {"value": "新增成本未知", "provenance": "UNK"}},
                ],
                "recommendation": {"optionId": "hold", "provenance": "EVIDENCE"},
                "recommendationReason": {"value": "当前只有内部执行事实", "provenance": "EVIDENCE"},
                "ceoChoicePrompt": "是否维持当前投入？",
                "continuationPlan": "记录选择并回到原业务继续观察",
            },
        }
        artifact = store.save_artifact(
            task["task_id"], title="内容增长 30 天经营分析",
            content=json.dumps(content, ensure_ascii=False),
            source_ref="operating-analysis:test", artifact_type="analysis_report",
        )
    return artifact["artifact_id"]


def test_projection_uses_real_sources_baseline_and_scope(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "operating.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, workspaces = _seed(path)
        _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=2, suffix="current-1", cost="1.00", latency=100)
        _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=3, suffix="current-2", cost="2.00", latency=200, status="failed")
        _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=35, suffix="previous-1", cost="1.00", latency=300)
        _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=36, suffix="previous-2", cost="1.00", latency=500)
        _usage(database, BUSINESS_B, workspaces[BUSINESS_B], offset_days=2, suffix="brand-1", cost="9.00", latency=900)
        _acceptance(database, workspaces[BUSINESS_A], accepted=True, offset_days=2, suffix="current-yes")
        _acceptance(database, workspaces[BUSINESS_A], accepted=False, offset_days=3, suffix="current-no")
        _acceptance(database, workspaces[BUSINESS_A], accepted=True, offset_days=35, suffix="previous-yes-1")
        _acceptance(database, workspaces[BUSINESS_A], accepted=True, offset_days=36, suffix="previous-yes-2")
        response = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?days=30&business_id={BUSINESS_A}",
            headers=HEADERS,
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        metrics = {item["key"]: item for item in payload["metrics"]}
        assert metrics["provider_cost"]["value"] == "3.00"
        assert metrics["provider_cost"]["currency"] == "CNY"
        assert metrics["provider_cost"]["baseline"] == "2.00"
        assert metrics["provider_cost"]["comparison"] == 1.0
        assert metrics["latency_p50"]["value"] == 150
        assert metrics["acceptance_rate"]["value"] == 50.0
        assert metrics["acceptance_rate"]["baseline"] == 100.0
        assert metrics["failure_rate"]["value"] == 50.0
        assert payload["trust"]["external_outcome"] == {"status": "MISSING", "label": "外部业务结果待连接", "value": None}
        assert all("brand" not in ref for metric in metrics.values() for ref in metric["source_refs"])
        denied = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?business_id=other",
            headers=HEADERS,
        )
        assert denied.status_code == 404
        cross_tenant = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence",
            headers={**HEADERS, "X-Tenant-Id": "other-tenant"},
        )
        assert cross_tenant.status_code == 404


def test_comparable_gate_and_unknown_are_formal_truth(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "benchmark.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, workspaces = _seed(path)
        for business_id in (BUSINESS_A, BUSINESS_B):
            _usage(database, business_id, workspaces[business_id], offset_days=1, suffix=f"{business_id}-1", cost="1.00", latency=100)
            _usage(database, business_id, workspaces[business_id], offset_days=2, suffix=f"{business_id}-2", cost="2.00", latency=200)
        payload = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?days=30",
            headers=HEADERS,
        ).json()
        benchmark = {item["metric"]: item for item in payload["benchmark"]["metrics"]}
        assert benchmark["provider_cost"]["status"] == "COMPARABLE"
        assert benchmark["acceptance_rate"]["status"] == "NOT_COMPARABLE"
        assert all(row["value"] is None for row in benchmark["acceptance_rate"]["rows"])


def test_empty_projection_keeps_unknown_distinct_from_zero(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "empty.sqlite"
    with TestClient(create_app(str(path))) as client:
        _seed(path)
        payload = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?days=7",
            headers=HEADERS,
        ).json()
        assert all(item["value"] is None for item in payload["metrics"])
        assert all(item["verification"] == "UNKNOWN" for item in payload["metrics"])
        assert payload["summary"]["headline"] == "当前没有足够数据形成经营结论"
        assert payload["reports"] == []


def test_cost_benchmark_requires_same_currency(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "currency.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, workspaces = _seed(path)
        for index in (1, 2):
            _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=index, suffix=f"cny-{index}", cost="1.00", latency=100, currency="CNY")
            _usage(database, BUSINESS_B, workspaces[BUSINESS_B], offset_days=index, suffix=f"usd-{index}", cost="1.00", latency=100, currency="USD")
        payload = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?days=30",
            headers=HEADERS,
        ).json()
        cost = next(item for item in payload["benchmark"]["metrics"] if item["metric"] == "provider_cost")
        assert cost["status"] == "NOT_COMPARABLE"
        assert all(row["value"] == "2.00" for row in cost["rows"])


def test_existing_report_creates_one_canonical_p7_decision_and_survives_restart(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "report.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, workspaces = _seed(path)
        _usage(database, BUSINESS_A, workspaces[BUSINESS_A], offset_days=1, suffix="current-1", cost="1.00", latency=100)
        report_id = _report(database, workspaces[BUSINESS_A])
        endpoint = f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence/reports/{report_id}/decision"
        first = client.post(endpoint, headers=HEADERS)
        replay = client.post(endpoint, headers=HEADERS)
        assert first.status_code == replay.status_code == 200
        assert first.json()["entity_id"] == replay.json()["entity_id"]
        assert first.json()["lifecycle_status"] == "WAITING_CEO"
        assert first.json()["data"]["reportRef"] == report_id
        assert first.json()["data"]["layer0Actions"] == ["VIEW_OPTIONS", "DEFER"]
        attention = client.get(f"/api/workspace/v1/companies/{COMPANY}/attention", headers=HEADERS).json()
        assert [item["source_ref"] for item in attention["items"]].count(first.json()["entity_id"]) == 1

    with TestClient(create_app(str(path))) as reopened:
        payload = reopened.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence?days=30",
            headers=HEADERS,
        ).json()
        report = next(item for item in payload["reports"] if item["artifact_id"] == report_id)
        assert report["decision"] == {"decision_id": first.json()["entity_id"], "status": "WAITING_CEO"}


def test_report_decision_rejects_unowned_evidence(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    path = tmp_path / "unowned-evidence.sqlite"
    with TestClient(create_app(str(path))) as client:
        database, workspaces = _seed(path)
        report_id = _report(database, workspaces[BUSINESS_A])
        response = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence/reports/{report_id}/decision",
            headers=HEADERS,
        )
        assert response.status_code == 404
