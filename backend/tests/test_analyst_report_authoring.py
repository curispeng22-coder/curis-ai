"""End-to-end tests for CEO-triggered analyst report authoring (GAP1 follow-up).

The real Orchestrator.run production path executes the task through the
GAP1 dispatcher against a stubbed allowlisted ``claude`` CLI on PATH; no real
provider or external binary is ever called.
"""
from __future__ import annotations

import json
import os
import shlex
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.analyst_authoring import AnalystAuthoring
from app.database import Database
from app.main import create_app
from app.organization_projection import department_assignments
from app.runtime import RuntimeFoundation
from app.runtime.business_spine import CanonicalBusinessSpine
from app.tenant_context import TenantContext


TENANT = "tenant-analyst-authoring"
COMPANY = "company-analyst-authoring"
CEO = "ceo-analyst-authoring"
BUSINESS = "business-authoring-content"
AGENT_CAPABILITY = "qa-analyst-agent"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO, "X-Role": "ceo"}
ENDPOINT = f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence/reports"
PROJECTION = f"/api/workspace/runtime/foundation/companies/{COMPANY}/operating-intelligence"
USAGE_REF = f"usage-{BUSINESS}-current-1"


def _bootstrap(path) -> tuple[Database, str, str, str, str]:
    database = Database(str(path))
    database.initialize()
    with TenantContext.scope(TENANT):
        foundation = RuntimeFoundation(database)
        run = foundation.create("FOUNDING_RUN", owner_ref=CEO)
        for state, actor in (("INTENT_CAPTURED", "CEO"), ("CLARIFYING", "SYSTEM"),
                             ("PROPOSED", "SYSTEM"), ("CEO_CONFIRMED", "CEO")):
            run = foundation.transition(run["entity_id"], state, actor=actor, trigger="test")
        foundation.materialize_company(
            run["entity_id"], company_id=COMPANY, ceo_id=CEO, name="Authoring Co")
    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        assignment = next(
            item for item in department_assignments(database, COMPANY)
            if item["data"].get("responsibilityKey") == "data.analytics.company_analysis"
        )
        analyst_id = assignment["data"]["companyEmployeeRef"]
        department_id = assignment["data"]["scopeRef"]
        business = CanonicalBusinessSpine(database).create_draft_with_first_workspace(
            company_id=COMPANY, department_id=department_id,
            business_id=BUSINESS, name="内容增长", goal="持续经营内容增长", positioning="测试定位",
            workspace_name="内容增长工作空间", business_type="GENERIC",
            blueprint_version="v1", blueprint={"surfaces": []},
        )
    return database, analyst_id, assignment["entity_id"], department_id, business["workspaces"][0]["workspace_id"]


def _bind_agent(database: Database, analyst_id: str, *, capability_status: str = "active") -> None:
    with database.connect() as connection:
        connection.execute(
            "insert into employee_capability_bindings(id, tenant_id, employee_id, capability_source, "
            "capability_type, capability_id, priority, enabled) "
            "values ('binding-analyst-agent', ?, ?, 'tenant_private', 'agent', ?, 100, 1)",
            (TENANT, analyst_id, AGENT_CAPABILITY),
        )
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="agent", capability_id=AGENT_CAPABILITY,
        display_name="QA Analyst Agent",
        metadata={"kind": "local-cli", "command": "claude", "timeout": 60},
        status=capability_status,
    )


def _usage(database: Database, workspace_id: str, analyst_id: str, department_id: str) -> None:
    at = datetime.now(timezone.utc).isoformat()
    with database.connect() as connection:
        connection.execute(
            "insert into tasks(task_id, tenant_id, company_id, workspace_id, work_ref, execution_ref, content, status, state_flow, employee_id) "
            "values (?, ?, ?, ?, ?, ?, '经营执行', 'COMPLETED', '[\"INIT\",\"COMPLETED\"]', ?)",
            (f"task-{BUSINESS}-current-1", TENANT, COMPANY, workspace_id,
             f"work-{BUSINESS}", f"execution-{BUSINESS}-current-1", analyst_id),
        )
        connection.execute(
            "insert into ai_usage_records(usage_record_id, tenant_id, company_id, model_gateway_id, provider_id, model_name, "
            "input_tokens, output_tokens, total_tokens, cost_amount, currency, cost_source, employee_id, capability_id, capability_type, "
            "task_id, department_id, business_id, workspace_id, work_ref, execution_ref, request_id, execution_status, metering_status, occurred_at, idempotency_key, latency_ms) "
            "values (?, ?, ?, 'gateway', 'provider', 'model', 10, 5, 15, '1.00', 'CNY', 'provider_reported', ?, 'model.test', 'model', "
            "?, ?, ?, ?, ?, ?, ?, 'completed', 'confirmed', ?, ?, ?)",
            (USAGE_REF, TENANT, COMPANY, analyst_id, f"task-{BUSINESS}-current-1", department_id, BUSINESS, workspace_id,
             f"work-{BUSINESS}", f"execution-{BUSINESS}-current-1", "request-current-1",
             at, f"usage-key-{BUSINESS}-current-1", 100),
        )


def _report(analyst_id: str, *, business_ref: str | None = BUSINESS, evidence_ref: str = USAGE_REF) -> dict:
    content = {
        "scope": {"type": "BUSINESS" if business_ref else "COMPANY", "ref": business_ref or COMPANY},
        "period": {"days": 30},
        "facts": [{"value": "当前周期存在真实执行记录", "provenance": "FACT"}],
        "analysis": [{"value": "样本仍有限，不能直接外推", "provenance": "EVIDENCE"}],
        "unknown": [{"value": "外部业务结果未连接", "provenance": "UNK"}],
        "recommendation": {"value": "继续观察同口径记录", "provenance": "EVIDENCE"},
        "evidenceRefs": [evidence_ref],
        "author": {"employeeRef": analyst_id, "name": "司衡"},
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "decisionCandidate": {
            "event": "内容增长投入是否需要调整",
            "cannotDecideReason": "涉及经营投入取舍，需要 CEO 判断",
            "options": [
                {"optionId": "hold", "label": "维持投入",
                 "impact": {"value": "维持当前节奏", "provenance": "FACT"},
                 "risk": {"value": "外部结果仍未知", "provenance": "UNK"},
                 "cost": {"value": "按现有成本继续", "provenance": "EVIDENCE"}},
                {"optionId": "pause", "label": "暂缓新增投入",
                 "impact": {"value": "等待更多事实", "provenance": "FACT"},
                 "risk": {"value": "可能延后验证", "provenance": "EST"},
                 "cost": {"value": "新增成本未知", "provenance": "UNK"}},
            ],
            "recommendation": {"optionId": "hold", "provenance": "EVIDENCE"},
            "recommendationReason": {"value": "当前只有内部执行事实", "provenance": "EVIDENCE"},
            "ceoChoicePrompt": "是否维持当前投入？",
            "continuationPlan": "记录选择并回到原业务继续观察",
        },
    }
    return content


def _install_stub_cli(tmp_path, monkeypatch, report: dict | None = None, *, exit_code: int = 0, raw: str | None = None) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    payload = tmp_path / "stub_report.json"
    payload.write_text(raw if raw is not None else json.dumps(report, ensure_ascii=False), encoding="utf-8")
    script = bin_dir / "claude"
    script.write_text(f"#!/bin/sh\ncat {shlex.quote(str(payload))}\nexit {exit_code}\n", encoding="utf-8")
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")


def _counts(database: Database) -> dict[str, int]:
    with database.connect() as connection:
        return {
            "tasks": connection.execute("select count(*) from tasks where tenant_id=?", (TENANT,)).fetchone()[0],
            "reports": connection.execute(
                "select count(*) from artifacts where tenant_id=? and artifact_type='analysis_report'", (TENANT,)).fetchone()[0],
            "usage": connection.execute("select count(*) from ai_usage_records where tenant_id=?", (TENANT,)).fetchone()[0],
        }


def _client(path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    return TestClient(create_app(str(path)))


def test_authoring_full_chain_business_scope_projection_and_p7(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "authoring.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "authoring.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        response = client.post(
            ENDPOINT, headers={**HEADERS, "Idempotency-Key": "authoring-1"},
            json={"business_id": BUSINESS, "days": 30},
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["replay"] is False
        artifact, task, report = payload["artifact"], payload["task"], payload["report"]
        assert artifact["artifact_type"] == "analysis_report"
        assert artifact["source_ref"] == "operating-analysis:authoring:authoring-1"
        assert task["status"] == "COMPLETED"
        assert report["scope"] == {"type": "BUSINESS", "ref": BUSINESS}
        with database.connect() as connection:
            task_row = connection.execute(
                "select * from tasks where task_id=?", (task["task_id"],)).fetchone()
            assert task_row["requested_capability_source"] == "tenant_private"
            assert task_row["requested_capability_type"] == "agent"
            assert task_row["requested_capability_id"] == AGENT_CAPABILITY
            assert task_row["employee_id"] == analyst_id
            usage_rows = connection.execute(
                "select * from ai_usage_records where tenant_id=? and task_id=?",
                (TENANT, task["task_id"])).fetchall()
            assert len(usage_rows) == 1
            assert usage_rows[0]["capability_id"] == AGENT_CAPABILITY
            assert usage_rows[0]["capability_type"] == "agent"
            assert str(usage_rows[0]["execution_status"]).lower() in {"success", "succeeded", "completed"}
        projection = client.get(f"{PROJECTION}?days=30&business_id={BUSINESS}", headers=HEADERS).json()
        projected = next(item for item in projection["reports"] if item["artifact_id"] == artifact["artifact_id"])
        assert projected["business_id"] == BUSINESS
        assert projected["decision"] is None
        decision = client.post(f"{PROJECTION}/reports/{artifact['artifact_id']}/decision", headers=HEADERS)
        assert decision.status_code == 200, decision.text
        assert decision.json()["lifecycle_status"] == "WAITING_CEO"
        replayed = client.post(f"{PROJECTION}/reports/{artifact['artifact_id']}/decision", headers=HEADERS)
        assert replayed.json()["entity_id"] == decision.json()["entity_id"]
        projected = client.get(f"{PROJECTION}?days=30&business_id={BUSINESS}", headers=HEADERS).json()["reports"]
        assert next(item for item in projected if item["artifact_id"] == artifact["artifact_id"])["decision"] == {
            "decision_id": decision.json()["entity_id"], "status": "WAITING_CEO"}


def test_authoring_idempotent_replay_returns_same_artifact(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "idempotent.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "idempotent.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        before = _counts(database)
        first = client.post(ENDPOINT, headers={**HEADERS, "Idempotency-Key": "same-key"}, json={"business_id": BUSINESS})
        replay = client.post(ENDPOINT, headers={**HEADERS, "Idempotency-Key": "same-key"}, json={"business_id": BUSINESS})
        assert first.status_code == replay.status_code == 200
        assert first.json()["artifact"]["artifact_id"] == replay.json()["artifact"]["artifact_id"]
        assert replay.json()["replay"] is True
        after = _counts(database)
        assert after["tasks"] == before["tasks"] + 1
        assert after["reports"] == before["reports"] + 1
        assert after["usage"] == before["usage"] + 1


def test_authoring_company_scope_report_visible_in_projection(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "company.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "company.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id, business_ref=None))
        response = client.post(ENDPOINT, headers=HEADERS, json={"days": 30})
        assert response.status_code == 200, response.text
        artifact = response.json()["artifact"]
        assert artifact["source_ref"] == "operating-analysis:authoring"
        projection = client.get(f"{PROJECTION}?days=30", headers=HEADERS).json()
        projected = next(item for item in projection["reports"] if item["artifact_id"] == artifact["artifact_id"])
        # Projection business_id is derived from the execution-home workspace
        # (existing contract); the report's analysis scope stays COMPANY.
        assert projected["business_id"] == BUSINESS
        assert projected["content"]["scope"] == {"type": "COMPANY", "ref": COMPANY}


def test_authoring_fails_without_unique_analyst_holder(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "no-holder.sqlite", monkeypatch) as client:
        database, analyst_id, assignment_id, department_id, workspace_id = _bootstrap(tmp_path / "no-holder.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        with database.connect() as connection:
            connection.execute(
                "update runtime_entities set lifecycle_status='ARCHIVED' where tenant_id=? and entity_id=?",
                (TENANT, assignment_id))
        before = _counts(database)
        missing = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert missing.status_code == 422
        assert "唯一" in missing.json()["detail"]
        with database.connect() as connection:
            row = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?", (TENANT, assignment_id)).fetchone()
            data = json.loads(row["data_json"])
            second_employee = f"{analyst_id}-second"
            connection.execute(
                "insert into employee_instances(id, tenant_id, company_id, department_id, template_id, name, role, status) "
                "values (?, ?, ?, ?, ?, '司衡二号', ?, 'idle')",
                (second_employee, TENANT, COMPANY,
                 connection.execute("select department_id from employee_instances where tenant_id=? and id=?",
                                    (TENANT, analyst_id)).fetchone()[0],
                 connection.execute("select template_id from employee_instances where tenant_id=? and id=?",
                                    (TENANT, analyst_id)).fetchone()[0],
                 connection.execute("select role from employee_instances where tenant_id=? and id=?",
                                    (TENANT, analyst_id)).fetchone()[0]))
            ai = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (TENANT, data["employeeRef"])).fetchone()
            ai_data = json.loads(ai["data_json"])
            ai_data["companyEmployeeRef"] = second_employee
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, "
                "lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{ai['entity_id']}-second", TENANT, ai["entity_type"], COMPANY, ai["workspace_id"],
                 ai["owner_ref"], ai["lifecycle_status"], ai["verification_status"], ai["evidence_condition"],
                 json.dumps(ai_data, ensure_ascii=False), ai["created_at"], ai["updated_at"]))
            data["employeeRef"] = f"{ai['entity_id']}-second"
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, owner_ref, "
                "lifecycle_status, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"{assignment_id}-second", TENANT, row["entity_type"], COMPANY, row["workspace_id"],
                 row["owner_ref"], "ACTIVE", row["verification_status"], row["evidence_condition"],
                 json.dumps(data, ensure_ascii=False), row["created_at"], row["updated_at"]))
            connection.execute(
                "update runtime_entities set lifecycle_status='ACTIVE' where tenant_id=? and entity_id=?",
                (TENANT, assignment_id))
        duplicate = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert duplicate.status_code == 422
        assert "唯一" in duplicate.json()["detail"]
        assert _counts(database) == before


def test_authoring_fails_without_enabled_binding(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "no-binding.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "no-binding.sqlite")
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        before = _counts(database)
        response = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert response.status_code == 422
        assert "能力绑定" in response.json()["detail"]
        assert _counts(database) == before


def test_authoring_fails_when_bound_capability_not_active(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "inactive.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "inactive.sqlite")
        _bind_agent(database, analyst_id, capability_status="disabled")
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        before = _counts(database)
        response = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert response.status_code == 422
        assert "不可用" in response.json()["detail"]
        assert _counts(database) == before


def test_authoring_honest_failure_when_capability_execution_fails(tmp_path, monkeypatch) -> None:
    """执行底座抛错 → 如实 422，零 artifact，任务不伪装 COMPLETED。"""
    database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "exec-fail.sqlite")
    _bind_agent(database, analyst_id)
    _usage(database, workspace_id, analyst_id, department_id)
    before = _counts(database)

    def exploding_runner(task_id: str) -> None:
        raise RuntimeError(f"stub capability exploded for {task_id}")

    with TenantContext.scope(TENANT, company_id=COMPANY, ceo_id=CEO, role="ceo"):
        try:
            AnalystAuthoring(database).author_report(
                COMPANY, business_id=BUSINESS, days=30, task_runner=exploding_runner)
        except ValueError as error:
            assert "执行失败" in str(error)
        else:  # pragma: no cover - must never succeed
            raise AssertionError("capability failure must not produce a report")
    after = _counts(database)
    assert after["reports"] == before["reports"]
    assert after["usage"] == before["usage"]
    assert after["tasks"] == before["tasks"] + 1
    with database.connect() as connection:
        task = connection.execute(
            "select status from tasks where tenant_id=? order by rowid desc limit 1", (TENANT,)).fetchone()
    assert task["status"] != "COMPLETED"


def test_authoring_rejects_invalid_output_contract(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "bad-contract.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "bad-contract.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, raw=json.dumps({"foo": 1}))
        before = _counts(database)
        response = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert response.status_code == 422
        assert "必填键" in response.json()["detail"]
        after = _counts(database)
        assert after["reports"] == before["reports"]
        assert after["tasks"] == before["tasks"] + 1


def test_authoring_rejects_foreign_evidence_refs(tmp_path, monkeypatch) -> None:
    with _client(tmp_path / "foreign.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "foreign.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id, evidence_ref="usage-foreign-company"))
        before = _counts(database)
        response = client.post(ENDPOINT, headers=HEADERS, json={"business_id": BUSINESS})
        assert response.status_code == 404
        after = _counts(database)
        assert after["reports"] == before["reports"]
        assert after["tasks"] == before["tasks"] + 1


def test_authoring_rejects_cross_tenant_access(tmp_path, monkeypatch) -> None:
    """跨租户身份看不到本公司：如实 404，原租户零副作用。"""
    with _client(tmp_path / "actor.sqlite", monkeypatch) as client:
        database, analyst_id, _, department_id, workspace_id = _bootstrap(tmp_path / "actor.sqlite")
        _bind_agent(database, analyst_id)
        _usage(database, workspace_id, analyst_id, department_id)
        _install_stub_cli(tmp_path, monkeypatch, _report(analyst_id))
        before = _counts(database)
        response = client.post(
            ENDPOINT, headers={**HEADERS, "X-Tenant-Id": "tenant-analyst-other"}, json={"business_id": BUSINESS})
        assert response.status_code == 404
        assert _counts(database) == before
