from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
import sqlite3
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation, SimulationRuntime
from app.runtime.workspace import CONTENT_STAGES, RD_STAGES, XHS_CONTENT_LIFECYCLE, WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "tenant-workspace-foundation"
OTHER_TENANT = "tenant-workspace-foundation-other"
COMPANY = "company-workspace-foundation"
OTHER_COMPANY = "company-workspace-foundation-other"
SAME_TENANT_COMPANY = "company-workspace-foundation-same-tenant"
CEO = "ceo-workspace-foundation"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}
OTHER_HEADERS = {"X-Tenant-Id": OTHER_TENANT, "X-Ceo-Id": CEO}
NOW = datetime.now(timezone.utc).isoformat()


@contextmanager
def client_for(path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    with TestClient(create_app(str(path))) as client:
        yield client


def seed_companies(path):
    database = Database(str(path))
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Runtime Company')",
            (COMPANY, TENANT, CEO),
        )
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Other Company')",
            (OTHER_COMPANY, OTHER_TENANT, CEO),
        )
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Same Tenant Company')",
            (SAME_TENANT_COMPANY, TENANT, CEO),
        )
    database = Database(str(path))
    for ref in (
        "business-rd", "business-xhs", "business-ttk", "business-rd-studio",
        "business-studio-rd", "business-studio-modify", "business-studio-reject",
    ):
        seed_canonical_business(database, TENANT, COMPANY, ref)


def blueprint(kind, *, reply_policy="CEO_REVIEW"):
    stages = RD_STAGES if kind == "RD" else XHS_CONTENT_LIFECYCLE if kind == "XHS" else CONTENT_STAGES
    value = {
        "stages": list(stages),
        "agentRefs": [f"agent-{kind.lower()}"],
        "capabilityRefs": [f"capability-{kind.lower()}"],
        "connectorRefs": [] if kind == "RD" else [f"connector-{kind.lower()}"],
        "platformConstraints": {} if kind == "RD" else {"format": kind.lower()},
        "replyPolicy": reply_policy,
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
    }
    if kind != "RD":
        value["platform"] = kind
    return value


def studio_blueprint(kind="RD"):
    value = blueprint(kind)
    value.update({
        "lifecycleMode": "STUDIO_DRAFT",
        "roleSlots": [
            {
                "role": "Engineering AI",
                "responsibility": "实现已批准的软件变更",
                "capabilityRefs": ["requirement:code-repository", "requirement:test-runner"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
            {
                "role": "QA AI",
                "responsibility": "验证结果与失败恢复路径",
                "capabilityRefs": ["requirement:test-runner"],
                "staffingStatus": "PLANNED_NOT_MATERIALIZED",
            },
        ],
        "capabilityBindings": [
            {
                "capabilityRef": "requirement:code-repository",
                "capability": "代码仓库",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
            {
                "capabilityRef": "requirement:test-runner",
                "capability": "测试运行器",
                "bindingStatus": "REQUIRED_NOT_AUTHORIZED",
            },
        ],
        "failurePolicy": {
            "manualFallback": "CEO Assistant 升级给 CEO 并转人工处理",
            "owner": "CEO Assistant",
        },
    })
    return value


def prepare_staffing_approval(client, path, *, name="Studio RD"):
    database = Database(str(path))
    with database.connect() as connection:
        assistant = connection.execute(
            "select 1 from runtime_entities where tenant_id = ? and company_id = ? and entity_type = 'CEO_ASSISTANT'",
            (TENANT, COMPANY),
        ).fetchone()
    if assistant is None:
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
    workspace = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=HEADERS,
        json={
            "ceo_id": CEO, "business_ref": f"business-{name.lower().replace(' ', '-')}",
            "business_type": "RD", "name": name, "blueprint_version": "v1",
            "blueprint": studio_blueprint(),
        },
    )
    assert workspace.status_code == 201, workspace.text
    workspace_id = workspace.json()["workspace"]["workspace_id"]
    simulation = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
        headers=HEADERS,
        json={"ceo_id": CEO, "scenario_id": "ORG-001", "blueprint_version": "v1"},
    ).json()
    simulation_id = simulation["simulation_run_id"]
    client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/transition",
        headers=HEADERS,
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start_staffing_simulation"},
    )
    executed = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
        headers=HEADERS,
        json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate_staffing_proposal"},
    ).json()
    reviewed = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
        headers=HEADERS,
        json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": executed["evidence_refs"]},
    )
    assert reviewed.status_code == 200, reviewed.text
    for capability_id, display_name, permissions in (
        ("tenant.repo-reader", "repo-reader", ["repository.read"]),
        ("tenant.test-runner", "test-runner", ["sandbox.execute"]),
    ):
        database.save_tenant_private_capability(
            tenant_id=TENANT,
            capability_type="tool",
            capability_id=capability_id,
            display_name=display_name,
            metadata={"live_status": "available", "cost_per_unit": 0, "permissions": permissions},
        )
    supply = client.post(
        f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/capability-supply-review",
        headers=HEADERS,
        json={
            "ceo_id": CEO,
            "selections": [
                {
                    "requirement_ref": "requirement:code-repository", "source": "tenant_private",
                    "capability_type": "tool", "capability_id": "tenant.repo-reader",
                },
                {
                    "requirement_ref": "requirement:test-runner", "source": "tenant_private",
                    "capability_type": "tool", "capability_id": "tenant.test-runner",
                },
            ],
        },
    )
    assert supply.status_code == 200, supply.text
    assert supply.json()["resourceCheckPassed"] is True
    return workspace_id, simulation_id


def create_workspace(client, kind, *, version="v1", headers=HEADERS):
    response = client.post(
        f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
        headers=headers,
        json={
            "ceo_id": CEO,
            "business_ref": f"business-{kind.lower()}",
            "business_type": kind,
            "name": f"{kind} Workspace",
            "blueprint_version": version,
            "blueprint": blueprint(kind),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_fresh_three_workspaces_restart_and_tenant_isolation(tmp_path, monkeypatch):
    path = tmp_path / "workspace-fresh.sqlite"
    with client_for(path, monkeypatch) as client:
        with Database(str(path)).connect() as connection:
            assert connection.execute("select count(*) from workspaces").fetchone()[0] == 0
        seed_companies(path)
        created = [create_workspace(client, kind) for kind in ("RD", "XHS", "TTK")]
        assert {item["workspace"]["business_type"] for item in created} == {"RD", "XHS", "TTK"}
        assert len({item["workspace"]["workspace_id"] for item in created}) == 3
        workspace_id = created[0]["workspace"]["workspace_id"]
        cross_tenant = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=OTHER_HEADERS,
        )
        forged_ceo = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": "another-ceo", "business_ref": "forged", "business_type": "RD",
                "name": "Forged", "blueprint_version": "v1", "blueprint": blueprint("RD"),
            },
        )
        assert cross_tenant.status_code == 404
        assert forged_ceo.status_code == 404
        assert COMPANY not in cross_tenant.text
        wrong_company = client.get(
            f"/api/workspace/runtime/foundation/companies/{SAME_TENANT_COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        )
        assert wrong_company.status_code == 404

    with client_for(path, monkeypatch) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        )
        assert recovered.status_code == 200
        assert recovered.json()["workspace"]["business_type"] == "RD"
    with Database(str(path)).connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_studio_workspace_atomically_materializes_scoped_staffing_proposals(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            assistant = RuntimeFoundation(database).create(
                "CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO,
                data={"prompt": "private", "credential": "secret"},
            )
        response = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "business_ref": "business-rd-studio",
                "business_type": "RD",
                "name": "Studio RD",
                "blueprint_version": "v1",
                "blueprint": studio_blueprint(),
            },
        )
        assert response.status_code == 201, response.text
        snapshot = response.json()
        workspace_id = snapshot["workspace"]["workspace_id"]
        assert [item["lifecycle_status"] for item in snapshot["role_slots"]] == ["DRAFT", "DRAFT"]
        assert [item["lifecycle_status"] for item in snapshot["employees"]] == ["PROPOSED", "PROPOSED"]
        assert [item["lifecycle_status"] for item in snapshot["capability_bindings"]] == ["PROPOSED", "PROPOSED"]
        assert {item["data"]["name"] for item in snapshot["employees"]} == {"Engineering AI", "QA AI"}
        assert "private" not in response.text
        assert "secret" not in response.text
        org_versions = {
            item["org_version"]
            for key in ("role_slots", "employees", "capability_bindings")
            for item in snapshot[key]
        }
        assert len(org_versions) == 1

        company = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}", headers=HEADERS,
        )
        assert company.status_code == 200, company.text
        assert len(company.json()["organization"]["employees"]) == 2
        assert company.json()["organization"]["employees"][0]["data"]["staffingStatus"] == "PROPOSED_NOT_HIRED"

    with client_for(path, monkeypatch) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        )
        assert recovered.status_code == 200
        assert len(recovered.json()["employees"]) == 2
    with Database(str(path)).connect() as connection:
        assert connection.execute(
            "select count(*) from runtime_links where workspace_id = ?", (workspace_id,),
        ).fetchone()[0] == 9
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"


def test_studio_staffing_failure_rolls_back_workspace_and_proposals(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-rollback.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        response = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "business_ref": "business-rd-studio",
                "business_type": "RD",
                "name": "Studio RD",
                "blueprint_version": "v1",
                "blueprint": studio_blueprint(),
            },
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "请求不符合 Runtime 契约"}
    with Database(str(path)).connect() as connection:
        assert connection.execute("select count(*) from workspaces").fetchone()[0] == 0
        assert connection.execute("select count(*) from runtime_entities").fetchone()[0] == 0


def test_staffing_simulation_is_derived_reviewable_and_never_activates_proposals(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-simulation.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
        workspace = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-rd-studio", "business_type": "RD",
                "name": "Studio RD", "blueprint_version": "v1", "blueprint": studio_blueprint(),
            },
        ).json()
        workspace_id = workspace["workspace"]["workspace_id"]
        payload = {
            "ceo_id": CEO,
            "scenario_id": "ORG-001",
            "blueprint_version": "v1",
        }
        created = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json=payload,
        )
        assert created.status_code == 201, created.text
        simulation_id = created.json()["simulation_run_id"]
        assert created.json()["subject_id"] is None
        repeated = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json=payload,
        )
        assert repeated.status_code == 201
        assert repeated.json()["simulation_run_id"] == simulation_id
        forged = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={**payload, "participants": ["forged-employee"]},
        )
        assert forged.status_code == 422

        started = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/transition",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start_staffing_simulation"},
        )
        assert started.status_code == 200, started.text
        executed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate_staffing_proposal"},
        )
        assert executed.status_code == 200, executed.text
        result = executed.json()
        assert result["lifecycle_status"] == "WAITING_CEO"
        assert result["final_state"] == "STAFFING_PROPOSAL_VALIDATED"
        assert result["evidence_count"] == result["handoff_count"] == 1
        assert result["failure_summary"]["count"] == 0
        repeated_execution = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "retry"},
        )
        assert repeated_execution.status_code == 200
        assert repeated_execution.json()["evidence_count"] == repeated_execution.json()["handoff_count"] == 1
        evidence_id = result["evidence_refs"][0]
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            evidence = RuntimeFoundation(database).get(evidence_id)
        assert evidence["verification_status"] == "VERIFIED"
        assert evidence["data"]["fixture"] is False
        assert evidence["data"]["kind"] == "STAFFING_PROPOSAL_VALIDATION"

        reviewed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "decision": "PASS", "evidence_refs": [evidence_id],
                "notes": "候选组织结构验证通过，不授权激活",
            },
        )
        assert reviewed.status_code == 200, reviewed.text
        assert reviewed.json()["lifecycle_status"] == "PASSED"
        assert reviewed.json()["pass_status"] == "PASS"
        recovered = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS,
        ).json()
        assert recovered["workspace"]["status"] == "DRAFT"
        assert recovered["workspace"]["simulation_passed"] == 0
        assert {item["lifecycle_status"] for item in recovered["role_slots"]} == {"DRAFT"}
        assert {item["lifecycle_status"] for item in recovered["employees"]} == {"PROPOSED"}
        assert {item["lifecycle_status"] for item in recovered["capability_bindings"]} == {"PROPOSED"}

    with client_for(path, monkeypatch) as restarted:
        simulations = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
        )
        assert simulations.status_code == 200
        assert simulations.json()["simulations"][0]["lifecycle_status"] == "PASSED"


def test_staffing_simulation_persists_blocked_contract_without_partial_activation(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-simulation-blocked.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
        workspace = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-rd-studio", "business_type": "RD",
                "name": "Studio RD", "blueprint_version": "v1", "blueprint": studio_blueprint(),
            },
        ).json()
        workspace_id = workspace["workspace"]["workspace_id"]
        with database.connect() as connection:
            connection.execute(
                "delete from runtime_links where tenant_id = ? and workspace_id = ? and relation = 'REQUIRES_CAPABILITY' "
                "and link_id = (select link_id from runtime_links where tenant_id = ? and workspace_id = ? "
                "and relation = 'REQUIRES_CAPABILITY' order by created_at, link_id limit 1)",
                (TENANT, workspace_id, TENANT, workspace_id),
            )
        created = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={"ceo_id": CEO, "scenario_id": "ORG-001", "blueprint_version": "v1"},
        ).json()
        simulation_id = created["simulation_run_id"]
        client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/transition",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start_staffing_simulation"},
        )
        executed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate_staffing_proposal"},
        )
        assert executed.status_code == 200, executed.text
        assert executed.json()["lifecycle_status"] == "WAITING_CEO"
        assert executed.json()["final_state"] == "BLOCKED"
        assert executed.json()["evidence_count"] == 0
        assert executed.json()["failure_summary"]["unresolved_count"] == 1
        rejected_pass = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
            headers=HEADERS,
            json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": [], "notes": "should fail"},
        )
        assert rejected_pass.status_code == 422
        failed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
            headers=HEADERS,
            json={"ceo_id": CEO, "decision": "FAIL", "evidence_refs": [], "notes": "返回 Studio 修复"},
        )
        assert failed.status_code == 200, failed.text
        assert failed.json()["lifecycle_status"] == "FAILED"
        recovered = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS,
        ).json()
        assert recovered["workspace"]["simulation_passed"] == 0
        assert {item["lifecycle_status"] for item in recovered["role_slots"]} == {"DRAFT"}
        assert {item["lifecycle_status"] for item in recovered["employees"]} == {"PROPOSED"}
        assert {item["lifecycle_status"] for item in recovered["capability_bindings"]} == {"PROPOSED"}


def test_capability_supply_review_is_atomic_recoverable_and_never_authorizes(tmp_path, monkeypatch):
    path = tmp_path / "workspace-capability-supply.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            RuntimeFoundation(database).create("CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO)
        workspace = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-rd-studio", "business_type": "RD",
                "name": "Studio RD", "blueprint_version": "v1", "blueprint": studio_blueprint(),
            },
        ).json()
        workspace_id = workspace["workspace"]["workspace_id"]
        simulation = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={"ceo_id": CEO, "scenario_id": "ORG-001", "blueprint_version": "v1"},
        ).json()
        simulation_id = simulation["simulation_run_id"]
        client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/transition",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "start_staffing_simulation"},
        )
        executed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/execute",
            headers=HEADERS,
            json={"ceo_id": CEO, "target": "RUNNING", "trigger": "validate_staffing_proposal"},
        ).json()
        reviewed = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations/{simulation_id}/review",
            headers=HEADERS,
            json={"ceo_id": CEO, "decision": "PASS", "evidence_refs": executed["evidence_refs"]},
        )
        assert reviewed.status_code == 200, reviewed.text

        database.save_official_model(
            model_key="official.repo-reader",
            provider_id="curis",
            display_name="repo-reader",
            supported_models=[],
            auth_type="none",
            gateway_ref="",
            type="tool",
            name="repo-reader",
            runtime_meta_json=json.dumps({
                "live_status": "available",
                "cost_per_unit": 0,
                "credentials_ref": "env:DO_NOT_EXPOSE",
            }),
        )
        database.save_tenant_private_capability(
            tenant_id=TENANT,
            capability_type="tool",
            capability_id="tenant.test-runner",
            display_name="test-runner",
            metadata={
                "live_status": "available",
                "cost_per_unit": 0,
                "permissions": ["sandbox.execute"],
                "credentials_ref": "env:PRIVATE_DO_NOT_EXPOSE",
            },
        )

        review_url = f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/capability-supply-review"
        selections = [
            {
                "requirement_ref": "requirement:code-repository",
                "source": "official",
                "capability_type": "tool",
                "capability_id": "official.repo-reader",
            },
            {
                "requirement_ref": "requirement:test-runner",
                "source": "tenant_private",
                "capability_type": "tool",
                "capability_id": "tenant.test-runner",
            },
        ]
        incomplete = client.post(review_url, headers=HEADERS, json={"ceo_id": CEO, "selections": selections[:1]})
        assert incomplete.status_code == 422
        with database.connect() as connection:
            assert connection.execute(
                "select count(*) from runtime_entities where workspace_id = ? and entity_type = 'CAPABILITY_BINDING' "
                "and data_json like '%supplyReview%'", (workspace_id,),
            ).fetchone()[0] == 0

        response = client.post(review_url, headers=HEADERS, json={"ceo_id": CEO, "selections": selections})
        assert response.status_code == 200, response.text
        supply = response.json()
        assert supply["reviewComplete"] is True
        assert supply["resourceCheckPassed"] is True
        assert supply["readyForApproval"] is True
        assert supply["activationReady"] is False
        assert supply["blockers"] == []
        assert "DO_NOT_EXPOSE" not in response.text
        assert "PRIVATE_DO_NOT_EXPOSE" not in response.text
        repeated = client.post(review_url, headers=HEADERS, json={"ceo_id": CEO, "selections": selections})
        assert repeated.status_code == 200
        assert [item["selection"]["reviewedAt"] for item in repeated.json()["requirements"]] == [
            item["selection"]["reviewedAt"] for item in supply["requirements"]
        ]

        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS,
        ).json()
        assert snapshot["workspace"]["status"] == "DRAFT"
        assert snapshot["workspace"]["simulation_passed"] == 0
        assert {item["lifecycle_status"] for item in snapshot["role_slots"]} == {"DRAFT"}
        assert {item["lifecycle_status"] for item in snapshot["employees"]} == {"PROPOSED"}
        assert {item["lifecycle_status"] for item in snapshot["capability_bindings"]} == {"PROPOSED"}
        assert {item["data"]["authorizationStatus"] for item in snapshot["capability_bindings"]} == {
            "PROPOSED_NOT_AUTHORIZED"
        }

        cross_tenant = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/capability-supply-review",
            headers=OTHER_HEADERS,
        )
        assert cross_tenant.status_code == 404

    with client_for(path, monkeypatch) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/capability-supply-review",
            headers=HEADERS,
        )
        assert recovered.status_code == 200
        assert recovered.json()["resourceCheckPassed"] is True

        Database(str(path)).set_official_model_status("official.repo-reader", "inactive")
        stale = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/capability-supply-review",
            headers=HEADERS,
        )
        assert stale.status_code == 200
        assert stale.json()["resourceCheckPassed"] is False
        assert "SUPPLY_UNAVAILABLE_OR_CHANGED" in stale.json()["blockers"]

        with Database(str(path)).connect() as connection:
            connection.execute(
                "delete from runtime_entities where workspace_id = ? and entity_type = 'CAPABILITY_BINDING' "
                "and entity_id = (select entity_id from runtime_entities where workspace_id = ? "
                "and entity_type = 'CAPABILITY_BINDING' order by entity_id limit 1)",
                (workspace_id, workspace_id),
            )
        incomplete_runtime = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/capability-supply-review",
            headers=HEADERS,
        )
        assert incomplete_runtime.status_code == 422


def test_staffing_approval_is_atomic_idempotent_recoverable_and_rollbackable(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-approval.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        workspace_id, simulation_id = prepare_staffing_approval(client, path)
        approval_url = f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision"
        approval_read = (
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}/staffing-approval"
        )
        ready = client.get(approval_read, headers=HEADERS)
        assert ready.status_code == 200, ready.text
        assert ready.json()["activationReady"] is True
        assert ready.json()["decision"] is None

        database = Database(str(path))
        with database.connect() as connection:
            before_logs = connection.execute("select count(*) from runtime_transition_log").fetchone()[0]
            connection.execute(
                "create trigger force_atomic_activation_failure before update on runtime_entities "
                "when new.entity_type = 'AI_EMPLOYEE' and new.lifecycle_status = 'AVAILABLE' "
                "begin select raise(abort, 'forced activation failure'); end"
            )
        failed = client.post(
            approval_url, headers=HEADERS,
            json={"ceo_id": CEO, "choice": "APPROVE", "reason": "批准当前最小运行团队"},
        )
        assert failed.status_code == 500
        with database.connect() as connection:
            connection.execute("drop trigger force_atomic_activation_failure")
            assert connection.execute("select status from workspaces where workspace_id = ?", (workspace_id,)).fetchone()[0] == "DRAFT"
            assert connection.execute("select count(*) from runtime_transition_log").fetchone()[0] == before_logs
            assert connection.execute(
                "select count(*) from runtime_entities where workspace_id = ? and entity_type = 'AI_EMPLOYEE' "
                "and lifecycle_status = 'PROPOSED'", (workspace_id,),
            ).fetchone()[0] == 2

        approved = client.post(
            approval_url, headers=HEADERS,
            json={"ceo_id": CEO, "choice": "APPROVE", "reason": "批准当前最小运行团队"},
        )
        assert approved.status_code == 200, approved.text
        result = approved.json()
        assert result["workspaceStatus"] == "OPERATING"
        assert result["operatingVersion"] == 1
        assert result["decision"]["choice"] == "APPROVE"
        assert result["decision"]["state"] == "APPLIED"
        assert result["activationReady"] is False
        assert result["rollbackReady"] is True
        assert result["roleSlotStatuses"] == ["ASSIGNED", "ASSIGNED"]
        assert result["employeeStatuses"] == ["AVAILABLE", "AVAILABLE"]
        assert result["bindingStatuses"] == ["ACTIVE", "ACTIVE"]
        assert "credential" not in approved.text.lower()
        assert "secret" not in approved.text.lower()

        repeated = client.post(
            approval_url, headers=HEADERS,
            json={"ceo_id": CEO, "choice": "APPROVE", "reason": "重复提交"},
        )
        assert repeated.status_code == 200
        assert repeated.json()["decision"]["decisionId"] == result["decision"]["decisionId"]
        conflicting = client.post(
            approval_url, headers=HEADERS,
            json={"ceo_id": CEO, "choice": "REJECT", "reason": "不能覆盖已生效决定"},
        )
        assert conflicting.status_code == 409
        cross_tenant = client.get(approval_read, headers=OTHER_HEADERS)
        assert cross_tenant.status_code == 404

        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS,
        ).json()
        assert snapshot["workspace"]["status"] == "OPERATING"
        assert snapshot["workspace"]["simulation_passed"] == 1
        assert snapshot["workspace"]["operating_version"] == 1
        assert {item["data"]["staffingStatus"] for item in snapshot["employees"]} == {"HIRED_AVAILABLE"}
        assert {item["data"]["authorizationStatus"] for item in snapshot["capability_bindings"]} == {
            "AUTHORIZED_ACTIVE"
        }

    with client_for(path, monkeypatch) as restarted:
        recovered = restarted.get(approval_read, headers=HEADERS)
        assert recovered.status_code == 200
        assert recovered.json()["decision"]["state"] == "APPLIED"
        rolled_back = restarted.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-rollback",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "真实运行前发现责任边界需重做"},
        )
        assert rolled_back.status_code == 200, rolled_back.text
        result = rolled_back.json()
        assert result["workspaceStatus"] == "PAUSED"
        assert result["operatingVersion"] == 0
        assert result["decision"]["state"] == "ROLLED_BACK"
        assert result["rollbackReady"] is False
        assert result["roleSlotStatuses"] == ["READY", "READY"]
        assert result["employeeStatuses"] == ["SUSPENDED", "SUSPENDED"]
        assert result["bindingStatuses"] == ["REVOKED", "REVOKED"]
        repeated_rollback = restarted.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-rollback",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "重复回滚"},
        )
        assert repeated_rollback.status_code == 200
        assert repeated_rollback.json()["decision"]["decisionId"] == result["decision"]["decisionId"]

    with Database(str(path)).connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        simulation = connection.execute(
            "select invalidated_at, invalidation_reason from runtime_simulation_runs where simulation_run_id = ?",
            (simulation_id,),
        ).fetchone()
        assert simulation["invalidated_at"]
        assert simulation["invalidation_reason"] == "STAFFING_ACTIVATION_ROLLED_BACK"


def test_staffing_modify_and_reject_preserve_draft_without_activation(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-decisions.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        for choice in ("MODIFY", "REJECT"):
            workspace_id, simulation_id = prepare_staffing_approval(client, path, name=f"Studio {choice}")
            response = client.post(
                f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
                headers=HEADERS,
                json={"ceo_id": CEO, "choice": choice, "reason": f"CEO {choice} 保留草案"},
            )
            assert response.status_code == 200, response.text
            result = response.json()
            assert result["workspaceStatus"] == "BLUEPRINTING"
            assert result["operatingVersion"] == 0
            assert result["decision"]["choice"] == choice
            assert result["decision"]["state"] == "RECORDED"
            assert result["roleSlotStatuses"] == ["DRAFT", "DRAFT"]
            assert result["employeeStatuses"] == ["PROPOSED", "PROPOSED"]
            assert result["bindingStatuses"] == ["PROPOSED", "PROPOSED"]
            repeated = client.post(
                f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
                headers=HEADERS,
                json={"ceo_id": CEO, "choice": choice, "reason": "重复决定"},
            )
            assert repeated.status_code == 200
            conflicting = client.post(
                f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
                headers=HEADERS,
                json={"ceo_id": CEO, "choice": "APPROVE", "reason": "不得覆盖"},
            )
            assert conflicting.status_code == 409
            with Database(str(path)).connect() as connection:
                simulation = connection.execute(
                    "select invalidated_at, invalidation_reason from runtime_simulation_runs where simulation_run_id = ?",
                    (simulation_id,),
                ).fetchone()
                assert simulation["invalidated_at"]
                assert simulation["invalidation_reason"] == f"CEO_{choice}"


def test_staffing_rollback_refuses_expired_window_without_partial_change(tmp_path, monkeypatch):
    path = tmp_path / "workspace-staffing-expired-rollback.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        workspace_id, _ = prepare_staffing_approval(client, path)
        approved = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-decision",
            headers=HEADERS,
            json={"ceo_id": CEO, "choice": "APPROVE", "reason": "批准"},
        )
        assert approved.status_code == 200, approved.text
        database = Database(str(path))
        with database.connect() as connection:
            row = connection.execute(
                "select data_json from runtime_workspace_versions where workspace_id = ? and blueprint_version = 'v1'",
                (workspace_id,),
            ).fetchone()
            data = json.loads(row["data_json"])
            data["staffingDecision"]["rollbackUntil"] = "2000-01-01T00:00:00+00:00"
            connection.execute(
                "update runtime_workspace_versions set data_json = ? where workspace_id = ? and blueprint_version = 'v1'",
                (json.dumps(data), workspace_id),
            )
        expired = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/staffing-rollback",
            headers=HEADERS,
            json={"ceo_id": CEO, "reason": "超窗回滚"},
        )
        assert expired.status_code == 409
        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS,
        ).json()
        assert snapshot["workspace"]["status"] == "OPERATING"
        assert {item["lifecycle_status"] for item in snapshot["employees"]} == {"AVAILABLE"}
        assert {item["lifecycle_status"] for item in snapshot["capability_bindings"]} == {"ACTIVE"}


def test_rd_cycle_eight_stages_failure_ceo_rejection_and_reverse_keys(tmp_path, monkeypatch):
    path = tmp_path / "workspace-rd.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        workspace_id = create_workspace(client, "RD")["workspace"]["workspace_id"]
        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            evidence = RuntimeFoundation(database).create(
                "EVIDENCE", company_id=COMPANY, workspace_id=workspace_id,
                verification_status="VERIFIED", evidence_condition="CURRENT",
                data={"source": "test-run", "fixture": False},
            )
        cycle_response = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/cycles",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "owner_ref": "engineering-ai", "outcome_ref": "usable-increment",
                "intent_ref": "curis-self-development", "blueprint_version": "v1",
                "execution_ref": "task-ref-only", "evidence_refs": [evidence["entity_id"]],
                "next_check_at": NOW,
            },
        )
        assert cycle_response.status_code == 201, cycle_response.text
        cycle = cycle_response.json()
        assert cycle["data"]["workItemName"] == "完善 Curis"
        assert cycle["data"]["stages"] == list(RD_STAGES)
        assert cycle["execution_ref"] == "task-ref-only"

        simulation = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "subject_id": cycle["entity_id"], "scenario_id": "RD-001",
                "blueprint_version": "v1", "participants": ["engineering-ai"],
                "input_refs": ["intent:curis-self-development"],
            },
        )
        assert simulation.status_code == 201, simulation.text
        assert simulation.json()["subject_id"] == cycle["entity_id"]

        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            foundation = RuntimeFoundation(database)
            failed = foundation.transition(cycle["entity_id"], "READY", actor="CEO", trigger="ready")
            failed = foundation.transition(failed["entity_id"], "RUNNING", actor="CEO", trigger="start")
            failed = foundation.transition(failed["entity_id"], "FAILED", actor="SYSTEM", trigger="fail")
            rejected = WorkspaceRuntime(database).create_cycle(
                company_id=COMPANY, workspace_id=workspace_id, blueprint_version="v1",
                owner_ref="engineering-ai", outcome_ref="revision", intent_ref="ceo-review",
            )
            rejected = foundation.transition(rejected["entity_id"], "READY", actor="CEO", trigger="ready")
            rejected = foundation.transition(rejected["entity_id"], "RUNNING", actor="CEO", trigger="start")
            rejected = foundation.transition(
                rejected["entity_id"], "WAITING_CEO", actor="SYSTEM", trigger="request_acceptance",
            )
            rejected = foundation.transition(rejected["entity_id"], "REJECTED", actor="CEO", trigger="reject")
        assert failed["lifecycle_status"] == "FAILED"
        assert rejected["lifecycle_status"] == "REJECTED"

        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        first = next(item for item in snapshot["cycles"] if item["entity_id"] == cycle["entity_id"])
        assert first["data"]["currentStage"] == "INTAKE"
        assert first["data"]["evidenceRefs"] == [evidence["entity_id"]]
        assert snapshot["simulations"][0]["subject_id"] == cycle["entity_id"]


def test_content_objects_versions_receipts_interactions_and_manual_boundary(tmp_path, monkeypatch):
    path = tmp_path / "workspace-content.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        xhs_id = create_workspace(client, "XHS")["workspace"]["workspace_id"]
        ttk_id = create_workspace(client, "TTK")["workspace"]["workspace_id"]

        def create_content(workspace_id, platform):
            response = client.post(
                f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items",
                headers=HEADERS,
                json={
                    "ceo_id": CEO, "owner_ref": "content-ai", "outcome_ref": f"outcome-{platform}",
                    "intent_ref": f"intent-{platform}", "blueprint_version": "v1", "platform": platform,
                    "platform_variant": f"{platform}_V1", "payload_ref": f"artifact-{platform}-v1",
                    "author": "content-ai", "constraints_check": "PASSED", "next_check_at": NOW,
                },
            )
            assert response.status_code == 201, response.text
            return response.json()

        xhs = create_content(xhs_id, "XHS")
        ttk = create_content(ttk_id, "TTK")
        assert xhs["content_item"]["entity_id"] != ttk["content_item"]["entity_id"]
        assert xhs["content_item"]["data"]["platform"] == "XHS"
        assert ttk["content_item"]["data"]["platform"] == "TTK"
        wrong_scenario = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{ttk_id}/simulations",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "subject_id": ttk["content_item"]["entity_id"],
                "scenario_id": "XHS-001", "blueprint_version": "v1",
            },
        )
        assert wrong_scenario.status_code == 422

        database = Database(str(path))
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            foundation = RuntimeFoundation(database)
            runtime = WorkspaceRuntime(database)
            content_id = xhs["content_item"]["entity_id"]
            content = foundation.transition(content_id, "DRAFT", actor="SYSTEM", trigger="accept_idea")
            content = foundation.transition(content_id, "IN_REVIEW", actor="AI_EMPLOYEE", trigger="submit_review")
            content = foundation.transition(
                content_id, "DRAFT", actor="CEO", trigger="request_changes", reason="CEO rejects title",
            )
            version = runtime.add_content_version(
                content_id, platform_variant="XHS_V2", payload_ref="artifact-xhs-v2",
                author="content-ai", constraints_check="PASSED",
            )
            content = foundation.transition(content_id, "IN_REVIEW", actor="AI_EMPLOYEE", trigger="submit_review")
            foundation.set_version_refs(content_id, approved_version_id=version["entity_id"])
            content = foundation.transition(content_id, "APPROVED", actor="CEO", trigger="approve")
            manual = runtime.record_publication_receipt(
                content_id, source="CEO_MANUAL", status="RECEIVED",
                approved_version_id=version["entity_id"], published_version_id=version["entity_id"],
                recorded_by=CEO,
            )
            platform = runtime.record_publication_receipt(
                content_id, source="PLATFORM_API", status="SUCCESS",
                approved_version_id=version["entity_id"], published_version_id=version["entity_id"],
                external_id="xhs-post-1",
            )
            interaction = runtime.record_interaction(
                content_id, source="PLATFORM_API", external_id="comment-1", intent="QUESTION",
                sensitivity="LOW", reply_policy="CEO_REVIEW", next_check_at=NOW,
            )
            with pytest.raises(ValueError):
                runtime.record_publication_receipt(
                    content_id, source="PLATFORM_API", status="SUCCESS",
                    approved_version_id=version["entity_id"],
                    published_version_id=xhs["content_version"]["entity_id"], external_id="mismatch",
                )
            simulation = SimulationRuntime(database).create(
                company_id=COMPANY, ceo_id=CEO, scenario_id="XHS-001", blueprint_version="v1",
                workspace_id=xhs_id, subject_id=content_id,
            )
            simulation = SimulationRuntime(database).transition(
                simulation["simulation_run_id"], "RUNNING", actor="SYSTEM", trigger="start",
            )
            simulations = SimulationRuntime(database)
            simulations.append(simulation["simulation_run_id"], "handoffs", {"handoffId": "handoff-xhs"})
            simulations.append(simulation["simulation_run_id"], "evidence_refs", platform["entity_id"])
            simulations.append(simulation["simulation_run_id"], "ceo_decisions", {"choice": "ACCEPT"})
            simulations.append(simulation["simulation_run_id"], "receipts", {
                "receiptId": manual["entity_id"], "source": "CEO_MANUAL", "status": "RECEIVED",
                "receivedAt": NOW, "recordedBy": CEO, "verificationStatus": "UNVERIFIED",
            })
            simulations.set_final_state(simulation["simulation_run_id"], "CONTENT_REVIEWED")
            with pytest.raises(ValueError):
                simulations.review(simulation["simulation_run_id"], reviewer="CEO", pass_status="PASS")
            simulations.append(simulation["simulation_run_id"], "receipts", {
                "receiptId": platform["entity_id"], "source": "PLATFORM_API", "status": "SUCCESS",
                "receivedAt": NOW, "externalId": "xhs-post-1", "verificationStatus": "VERIFIED",
            })
            passed = simulations.review(simulation["simulation_run_id"], reviewer="CEO", pass_status="PASS")

        assert content["lifecycle_status"] == "APPROVED"
        assert manual["verification_status"] == "UNVERIFIED"
        assert platform["verification_status"] == "VERIFIED"
        assert interaction["parent_id"] == content_id
        assert passed["pass_status"] == "PASS"
        api_manual = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{xhs_id}/content-items/{content_id}/receipts",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "source": "CEO_MANUAL", "status": "RECEIVED",
                "approved_version_id": version["entity_id"],
                "published_version_id": version["entity_id"], "recorded_by": CEO,
            },
        )
        rejected_platform_receipt = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{xhs_id}/content-items/{content_id}/receipts",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "source": "PLATFORM_API", "status": "SUCCESS",
                "approved_version_id": version["entity_id"],
                "published_version_id": version["entity_id"], "recorded_by": CEO,
            },
        )
        wrong_workspace_receipt = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{ttk_id}/content-items/{content_id}/receipts",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "source": "CEO_MANUAL", "status": "RECEIVED",
                "approved_version_id": version["entity_id"],
                "published_version_id": version["entity_id"], "recorded_by": CEO,
            },
        )
        api_interaction = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{xhs_id}/content-items/{content_id}/interactions",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "source": "CEO_MANUAL", "external_id": "manual-comment-1",
                "intent": "QUESTION", "sensitivity": "LOW", "reply_policy": "CEO_REVIEW",
            },
        )
        rejected_platform_interaction = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{xhs_id}/content-items/{content_id}/interactions",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "source": "PLATFORM_API", "external_id": "platform-comment-2",
                "intent": "QUESTION", "sensitivity": "LOW", "reply_policy": "CEO_REVIEW",
            },
        )
        assert api_manual.status_code == 201
        assert api_manual.json()["verification_status"] == "UNVERIFIED"
        assert rejected_platform_receipt.status_code == 403
        assert wrong_workspace_receipt.status_code == 404
        assert api_interaction.status_code == 201
        assert rejected_platform_interaction.status_code == 403
        snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{xhs_id}", headers=HEADERS,
        ).json()
        assert len(snapshot["content_versions"]) == 2
        assert {item["data"]["source"] for item in snapshot["publication_receipts"]} == {
            "CEO_MANUAL", "PLATFORM_API",
        }
        assert {item["entity_id"] for item in snapshot["interactions"]} == {
            interaction["entity_id"], api_interaction.json()["entity_id"],
        }
        ttk_snapshot = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{ttk_id}", headers=HEADERS,
        ).json()
        assert [item["data"]["platform"] for item in ttk_snapshot["content_items"]] == ["TTK"]

        collision = "content_version-00000000-0000-0000-0000-000000000002"
        rolled_back_content = "content_item-00000000-0000-0000-0000-000000000001"
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            RuntimeFoundation(database).create(
                "CONTENT_VERSION", entity_id=collision, company_id=COMPANY, workspace_id=xhs_id,
            )
            ids = iter((UUID(int=1), UUID(int=2)))
            monkeypatch.setattr("app.runtime.workspace.uuid4", lambda: next(ids))
            with pytest.raises(sqlite3.IntegrityError):
                WorkspaceRuntime(database).create_content_item(
                    company_id=COMPANY, workspace_id=xhs_id, blueprint_version="v1", platform="XHS",
                    owner_ref="content-ai", outcome_ref="rollback", intent_ref="rollback",
                    platform_variant="XHS_ROLLBACK", payload_ref="artifact-rollback",
                    author="content-ai", constraints_check="PASSED",
                )
            with pytest.raises(KeyError):
                RuntimeFoundation(database).get(rolled_back_content)


def test_blueprint_revision_invalidates_simulation_without_overwriting_runtime_version(tmp_path, monkeypatch):
    path = tmp_path / "workspace-version.sqlite"
    with client_for(path, monkeypatch) as client:
        seed_companies(path)
        workspace = create_workspace(client, "XHS")
        workspace_id = workspace["workspace"]["workspace_id"]
        content = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "owner_ref": "content-ai", "outcome_ref": "outcome-xhs",
                "intent_ref": "intent-xhs", "blueprint_version": "v1", "platform": "XHS",
                "platform_variant": "XHS_V1", "payload_ref": "artifact-xhs-v1",
                "author": "content-ai", "constraints_check": "PASSED",
            },
        ).json()["content_item"]
        simulation = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "subject_id": content["entity_id"], "scenario_id": "XHS-001",
                "blueprint_version": "v1",
            },
        ).json()
        revised = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-xhs", "business_type": "XHS",
                "name": "XHS Workspace", "workspace_id": workspace_id, "blueprint_version": "v2",
                "change_kind": "REPLY_POLICY", "change_reason": "CEO requires review",
                "blueprint": blueprint("XHS", reply_policy="CEO_ALWAYS"),
            },
        )
        assert revised.status_code == 201, revised.text
        body = revised.json()
        assert body["workspace"]["blueprint_version"] == "v2"
        assert body["workspace"]["operating_version"] == 0
        assert body["workspace"]["simulation_passed"] == 0
        assert [item["blueprint_version"] for item in body["versions"]] == ["v1", "v2"]
        assert body["versions"][0]["blueprint"]["replyPolicy"] == "CEO_REVIEW"
        assert body["versions"][1]["blueprint"]["replyPolicy"] == "CEO_ALWAYS"
        old_run = next(item for item in body["simulations"] if item["simulation_run_id"] == simulation["simulation_run_id"])
        assert old_run["invalidated_at"]
        assert old_run["invalidation_reason"] == "REPLY_POLICY"
        assert body["content_items"][0]["blueprint_version"] == "v1"
        stale = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/simulations",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "subject_id": content["entity_id"], "scenario_id": "XHS-001",
                "blueprint_version": "v1",
            },
        )
        assert stale.status_code == 422
        assert "sqlite" not in stale.text.lower()
        assert "Traceback" not in stale.text
        invalid_revision = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO, "business_ref": "business-xhs", "business_type": "XHS",
                "name": "XHS Workspace", "workspace_id": workspace_id, "blueprint_version": "v3",
                "change_kind": "NOT_ALLOWED", "change_reason": "must roll back",
                "blueprint": blueprint("XHS", reply_policy="INVALID"),
            },
        )
        assert invalid_revision.status_code == 422
        unchanged = client.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        ).json()
        assert unchanged["workspace"]["blueprint_version"] == "v2"
        assert [item["blueprint_version"] for item in unchanged["versions"]] == ["v1", "v2"]

    with client_for(path, monkeypatch) as restarted:
        recovered = restarted.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}",
            headers=HEADERS,
        )
        assert recovered.status_code == 200
        assert recovered.json()["workspace"]["blueprint_version"] == "v2"
    with Database(str(path)).connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
