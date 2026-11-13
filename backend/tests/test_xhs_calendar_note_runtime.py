from __future__ import annotations

from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.runtime import RuntimeFoundation
from app.runtime.workspace import WorkspaceRuntime
from app.tenant_context import TenantContext
from backend.tests.conftest import seed_canonical_business


TENANT = "xhs-calendar-test"
CEO = "xhs-calendar-ceo"
COMPANY = "xhs-calendar-company"
HEADERS = {"X-Tenant-Id": TENANT, "X-Ceo-Id": CEO}


def xhs_blueprint() -> dict:
    return {
        "stages": ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"],
        "agentRefs": ["xhs-content-agent"],
        "capabilityRefs": ["xhs-writing"],
        "connectorRefs": ["xhs-publishing"],
        "platformConstraints": {"format": "xhs"},
        "replyPolicy": "CEO_REVIEW",
        "evidenceRules": ["NON_FIXTURE_REQUIRED"],
        "platform": "XHS",
    }


def test_xhs_note_calendar_fields_and_immutable_draft_version_survive_reopen(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    database_path = tmp_path / "xhs-calendar.sqlite"
    with TestClient(create_app(str(database_path))) as client:
        database = Database(str(database_path))
        with database.connect() as connection:
            connection.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, ?)",
                (COMPANY, TENANT, CEO, "XHS Calendar Company"),
            )
        seed_canonical_business(database, TENANT, COMPANY, "xhs-calendar-business")
        workspace_response = client.post(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "business_ref": "xhs-calendar-business",
                "business_type": "XHS",
                "name": "XHS Calendar Office",
                "blueprint_version": "v1",
                "blueprint": xhs_blueprint(),
            },
        )
        assert workspace_response.status_code == 201, workspace_response.text
        workspace_id = workspace_response.json()["workspace"]["workspace_id"]

        created = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "owner_ref": workspace_id,
                "outcome_ref": "验证一条真实内容意图",
                "intent_ref": "验证一条真实内容意图",
                "blueprint_version": "v1",
                "platform": "XHS",
                "platform_variant": "图文",
                "payload_ref": "CEO 手动创建的 Note 草稿",
                "author": "CEO",
                "constraints_check": "尚未审核",
                "title": "真实排期 Note",
                "body": "这是 CEO 保存的草稿说明。",
                "tags": ["内容", "验证"],
                "scheduled_for": "2026-08-15",
            },
        )
        assert created.status_code == 201, created.text
        note = created.json()["content_item"]
        first_version = created.json()["content_version"]
        assert note["lifecycle_status"] == "IDEA"
        assert note["data"]["stages"] == ["IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED"]
        assert first_version["data"]["scheduledFor"] == "2026-08-15"

        accepted = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note['entity_id']}/accept-idea",
            headers=HEADERS,
            json={"ceo_id": CEO},
        )
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["lifecycle_status"] == "DRAFT"

        next_version = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note['entity_id']}/versions",
            headers=HEADERS,
            json={
                "ceo_id": CEO,
                "platform_variant": "图文",
                "payload_ref": "CEO 手动编辑的 Note 草稿",
                "author": "CEO",
                "constraints_check": "尚未审核",
                "title": "修订后的真实排期 Note",
                "body": "这是新的不可变草稿版本。",
                "tags": ["内容", "修订"],
                "scheduled_for": "2026-08-16",
            },
        )
        assert next_version.status_code == 201, next_version.text
        assert next_version.json()["entity_id"] != first_version["entity_id"]

    with TestClient(create_app(str(database_path))) as reopened:
        snapshot = reopened.get(
            f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS
        )
        assert snapshot.status_code == 200, snapshot.text
        notes = snapshot.json()["content_items"]
        versions = snapshot.json()["content_versions"]
        saved = next(item for item in notes if item["entity_id"] == note["entity_id"])
        assert saved["lifecycle_status"] == "DRAFT"
        assert saved["current_version_id"] == next_version.json()["entity_id"]
        assert {item["entity_id"] for item in versions} >= {first_version["entity_id"], next_version.json()["entity_id"]}


def test_xhs_work_context_requires_real_employee_references_and_survives_reopen(tmp_path, monkeypatch):
    monkeypatch.setenv("CURIS_ENV", "test")
    monkeypatch.setenv("CURIS_IDENTITY_MODE", "test")
    database_path = tmp_path / "xhs-work-context.sqlite"
    with TestClient(create_app(str(database_path))) as client:
        database = Database(str(database_path))
        with database.connect() as connection:
            connection.execute("insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, ?)", (COMPANY, TENANT, CEO, "XHS Work Context Company"))
        seed_canonical_business(database, TENANT, COMPANY, "xhs-work-context")
        workspace_response = client.post(f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces", headers=HEADERS, json={"ceo_id": CEO, "business_ref": "xhs-work-context", "business_type": "XHS", "name": "XHS Work Context Office", "blueprint_version": "v1", "blueprint": xhs_blueprint()})
        assert workspace_response.status_code == 201, workspace_response.text
        workspace_id = workspace_response.json()["workspace"]["workspace_id"]
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            foundation = RuntimeFoundation(database)
            creator = foundation.create("AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace_id, lifecycle_status="AVAILABLE", owner_ref=CEO, data={"name": "内容创作 AI", "responsibility": "内容创作"})
            reviewer = foundation.create("AI_EMPLOYEE", company_id=COMPANY, workspace_id=workspace_id, lifecycle_status="AVAILABLE", owner_ref=CEO, data={"name": "内容审核 AI", "responsibility": "内容审核"})
        created = client.post(f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items", headers=HEADERS, json={"ceo_id": CEO, "owner_ref": workspace_id, "outcome_ref": "验证真实员工引用", "intent_ref": "验证真实员工引用", "blueprint_version": "v1", "platform": "XHS", "platform_variant": "图文", "payload_ref": "保存的 Note", "author": "CEO", "constraints_check": "尚未审核", "execution_ref": "workflow_run:xhs-phase4-bound", "title": "员工引用 Note", "scheduled_for": "2026-08-16"})
        assert created.status_code == 201, created.text
        note_id = created.json()["content_item"]["entity_id"]
        forged = client.post(f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note_id}/work-context", headers=HEADERS, json={"ceo_id": CEO, "responsibility_employee_ref": "missing-employee", "current_executor_ref": "missing-employee", "status": "working"})
        assert forged.status_code == 404
        context = client.post(f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note_id}/work-context", headers=HEADERS, json={"ceo_id": CEO, "responsibility_employee_ref": creator["entity_id"], "current_executor_ref": creator["entity_id"], "next_responsibility_employee_ref": reviewer["entity_id"], "activity": "准备内容草稿", "status": "working"})
        assert context.status_code == 200, context.text
        accepted = client.post(f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note_id}/accept-idea", headers=HEADERS, json={"ceo_id": CEO})
        assert accepted.status_code == 200, accepted.text
        with TenantContext.scope(TENANT, ceo_id=CEO, role="test"):
            runtime = WorkspaceRuntime(database)
            failed = runtime.record_content_execution_failure(company_id=COMPANY, workspace_id=workspace_id, content_id=note_id, code="execution_unavailable")
            assert failed["data"]["workContext"]["status"] == "failed"
            handed_off = runtime.record_content_execution_completion(company_id=COMPANY, workspace_id=workspace_id, content_id=note_id, result={"output": "创作执行结果"})
            assert handed_off["lifecycle_status"] == "IN_REVIEW"
            needs_ceo = runtime.record_content_execution_completion(company_id=COMPANY, workspace_id=workspace_id, content_id=note_id, result={"output": "审核执行结果"})
            assert needs_ceo["lifecycle_status"] == "IN_REVIEW"
            decision_id = needs_ceo["data"]["decisionPacketId"]
            decision_packet = foundation.get(decision_id)
            assert decision_packet["lifecycle_status"] == "WAITING_CEO"
            assert decision_packet["data"]["conversation"]["message"]
            package = decision_packet["data"]["plainPackage"]
            assert package["recommendation"]["source"] == "POLICY"
            assert {option["key"] for option in package["options"]} == {"APPROVE", "RETURN", "DEFER"}
            assert all(option[field]["source"] for option in package["options"] for field in ("impact", "risk", "cost"))
            assert len([item for item in foundation.list("DECISION_PACKET", company_id=COMPANY, workspace_id=workspace_id) if item["parent_id"] == note_id]) == 1
            assert len([item for item in foundation.list("HANDOFF", company_id=COMPANY, workspace_id=workspace_id) if item["parent_id"] == note_id]) == 1
        decided = client.post(f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note_id}/decision", headers=HEADERS, json={"ceo_id": CEO, "choice": "APPROVE", "reason": "审核结论符合当前内容目标"})
        assert decided.status_code == 200, decided.text
        assert decided.json()["lifecycle_status"] == "SCHEDULED"
        version_id = created.json()["content_version"]["entity_id"]
        manual = client.post(
            f"/api/workspace/runtime/foundation/workspaces/{workspace_id}/content-items/{note_id}/receipts",
            headers=HEADERS,
            json={"ceo_id": CEO, "source": "CEO_MANUAL", "status": "RECEIVED", "approved_version_id": version_id, "published_version_id": version_id, "recorded_by": CEO},
        )
        assert manual.status_code == 201, manual.text
        assert manual.json()["verification_status"] == "UNVERIFIED"
        direct_publish = client.post(
            f"/api/workspace/runtime/foundation/entities/{note_id}/transition",
            headers=HEADERS,
            json={"target": "PUBLISHED", "actor": "CEO", "trigger": "manual_publish"},
        )
        assert direct_publish.status_code == 403

    with TestClient(create_app(str(database_path))) as reopened:
        snapshot = reopened.get(f"/api/workspace/runtime/foundation/companies/{COMPANY}/workspaces/{workspace_id}", headers=HEADERS)
        assert snapshot.status_code == 200, snapshot.text
        note = next(item for item in snapshot.json()["content_items"] if item["entity_id"] == note_id)
        assert note["work_context"]["object_owner"]["ref"] == workspace_id
        assert note["work_context"]["current_responsibility"]["employee"]["entity_id"] == reviewer["entity_id"]
        assert note["work_context"]["current_executor"] is None
        assert note["work_context"]["system_activity"]["status"] == "waiting"
        assert note["publication"]["status"] == "MANUAL_RECEIPT_UNVERIFIED"
        assert note["analytics"]["status"] == "UNAVAILABLE"
        assert note["lifecycle_status"] == "SCHEDULED"
        handoff = next(item for item in snapshot.json()["handoffs"] if item["parent_id"] == note_id)
        decision = next(item for item in snapshot.json()["decisions"] if item["parent_id"] == note_id)
        assert handoff["lifecycle_status"] == "ACKNOWLEDGED"
        assert decision["lifecycle_status"] == "APPLIED"
        assert decision["data"]["plainPackage"]["happened"]["source"] == "FACT"
