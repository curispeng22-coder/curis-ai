from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.database import Database
from backend.app.runtime import RuntimeFoundation
from backend.app.runtime.workspace import WorkspaceRuntime
from backend.app.workspace_package_runtime import PackageValidationError, WorkspacePackageRuntime
from backend.tests.test_workspace_package_runtime_p0 import _install_package, _seed_package_department, _write_package


TENANT = "selfuse"
COMPANY = "company-p05"
CEO = "ceo-p05"
RESPONSIBILITY = "CUSTOMER_FEEDBACK_TRIAGE"
CAPABILITY_ID = "core.customer-feedback-triage"


def _company(path: Path) -> tuple[Database, WorkspacePackageRuntime, str]:
    database = Database(str(path / "curis.sqlite"))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status, is_default) "
            "values (?, ?, ?, 'P0.5 Company', 'active', 1)",
            (COMPANY, TENANT, CEO),
        )
    _seed_package_department(database, COMPANY)
    database.save_tenant_private_capability(
        tenant_id=TENANT,
        capability_type="tool",
        capability_id=CAPABILITY_ID,
        display_name="Core Customer Feedback Triage",
        metadata={
            "handler": CAPABILITY_ID,
            "live_status": "available",
            "permissions": ["customer-feedback.read", "customer-feedback.write"],
            "cost_per_unit": 0,
        },
    )
    source = path / "customer-feedback-office"
    _write_package(source)
    runtime = WorkspacePackageRuntime(database, path / "package-store")
    workspace_id = _install_package(runtime, source, COMPANY)["instance"]["workspace_id"]
    return database, runtime, workspace_id


def _staff_company_os(database: Database, workspace_id: str) -> dict[str, str]:
    foundation = RuntimeFoundation(database)
    company_runtime = WorkspaceRuntime(database)
    role_id = "role-slot-feedback-triage"
    employee_id = "ai-employee-feedback-triage"
    binding_id = "capability-binding-feedback-triage"
    with database.connect() as connection:
        supply = company_runtime._resolve_supply(
            connection, "tenant_private", "tool", CAPABILITY_ID,
        )
        review = company_runtime._assess_supply(connection, supply)
    assert review["blockers"] == []
    foundation.create(
        "ROLE_SLOT",
        entity_id=role_id,
        company_id=COMPANY,
        workspace_id=workspace_id,
        lifecycle_status="ASSIGNED",
        data={
            "name": "Customer Feedback Owner",
            "responsibilityType": RESPONSIBILITY,
            "responsibility": "Triage customer feedback",
            "assignedEmployeeRef": employee_id,
            "capabilityRefs": ["requirement:customer-feedback-triage"],
            "staffingStatus": "ASSIGNED",
        },
    )
    foundation.create(
        "AI_EMPLOYEE",
        entity_id=employee_id,
        company_id=COMPANY,
        workspace_id=workspace_id,
        lifecycle_status="AVAILABLE",
        presence_state="AVAILABLE",
        data={
            "name": "Feedback Operations AI",
            "roleSlotRef": role_id,
            "responsibility": "Triage customer feedback",
            "staffingStatus": "HIRED_AVAILABLE",
        },
    )
    foundation.create(
        "CAPABILITY_BINDING",
        entity_id=binding_id,
        company_id=COMPANY,
        workspace_id=workspace_id,
        lifecycle_status="ACTIVE",
        capability_ref="requirement:customer-feedback-triage",
        data={
            "name": "Core Customer Feedback Triage",
            "requirementRef": "requirement:customer-feedback-triage",
            "authorizationStatus": "AUTHORIZED_ACTIVE",
            "supplyReview": review,
        },
    )
    foundation.link(employee_id, "PROPOSED_FOR", role_id)
    foundation.link(role_id, "REQUIRES_CAPABILITY", binding_id)
    return {"role": role_id, "employee": employee_id, "binding": binding_id}


def _feedback(runtime: WorkspacePackageRuntime, workspace_id: str, *, summary: str) -> dict:
    return runtime.create_object(
        workspace_id,
        "core.domain-object.create",
        "FeedbackRecord",
        {
            "title": "导出结果难以定位",
            "customerRef": "customer:acme",
            "channel": "INTERVIEW",
            "summary": summary,
        },
    )


def test_real_company_chain_failure_truth_and_restart_resolution(tmp_path: Path) -> None:
    database, runtime, workspace_id = _company(tmp_path)
    core = _staff_company_os(database, workspace_id)

    with pytest.raises(PackageValidationError):
        runtime.create_object(
            workspace_id,
            "core.domain-object.create",
            "FeedbackRecord",
            {
                "title": "伪造引用",
                "channel": "INTERVIEW",
                "summary": "这条记录试图用 Package 字符串冒充真实关系。",
                "responsibilityRef": core["employee"],
                "evidenceRef": "evidence:fake",
            },
        )

    success = _feedback(runtime, workspace_id, summary="客户需要从导出结果直接回到责任人与证据记录。")
    integrated = runtime.operate_object(workspace_id, success["object_id"], RESPONSIBILITY)
    assert integrated["status"] == "COMPLETED"
    assert integrated["resolvable"] is True
    assert integrated["reverseResolved"] is True
    assert integrated["responsibility"]["roleSlotRef"] == core["role"]
    assert integrated["employee"]["employeeRef"] == core["employee"]
    assert integrated["capability"]["bindingRef"] == core["binding"]
    assert integrated["capability"]["capabilityId"] == CAPABILITY_ID
    assert integrated["task"]["status"] == "COMPLETED"
    assert integrated["execution"]["task_id"] == integrated["task"]["task_id"]
    assert len(integrated["evidenceRefs"]) == 1
    assert len(integrated["resultRefs"]) == 1
    assert len(integrated["artifactRefs"]) == 1

    completed = runtime.get_object(workspace_id, success["object_id"])
    assert completed["lifecycle_status"] == completed["data"]["status"] == "TRIAGED"
    assert completed["owner_ref"] == core["employee"]
    assert completed["data"]["responsibilityRef"] == core["role"]
    assert completed["data"]["evidenceRef"] == integrated["evidenceRefs"][0]

    failed = _feedback(runtime, workspace_id, summary="信息不足")
    failure = runtime.operate_object(workspace_id, failed["object_id"], RESPONSIBILITY)
    assert failure["status"] == "FAILED"
    assert failure["task"]["status"] == "FAILED"
    assert failure["execution"] is not None
    assert failure["evidenceRefs"] == failure["resultRefs"] == failure["artifactRefs"] == []
    assert runtime.get_object(workspace_id, failed["object_id"])["lifecycle_status"] == "NEW"

    with database.connect() as connection:
        before_tasks = connection.execute("select count(*) from tasks").fetchone()[0]
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) "
            "values ('company-other', ?, ?, 'Other Company', 'active')",
            (TENANT, CEO),
        )
    RuntimeFoundation(database).create(
        "AI_EMPLOYEE",
        entity_id="employee-cross-scope",
        company_id="company-other",
        lifecycle_status="AVAILABLE",
        presence_state="AVAILABLE",
        data={"name": "Wrong Scope", "roleSlotRef": "role-cross-scope"},
    )
    RuntimeFoundation(database).create(
        "ROLE_SLOT",
        entity_id="role-cross-scope",
        company_id=COMPANY,
        workspace_id=workspace_id,
        lifecycle_status="ASSIGNED",
        data={
            "name": "Forged Role",
            "responsibilityType": "FORGED_CROSS_SCOPE",
            "assignedEmployeeRef": "employee-cross-scope",
        },
    )
    forged = _feedback(runtime, workspace_id, summary="这条记录必须拒绝跨 Company Employee。")
    with pytest.raises(PackageValidationError):
        runtime.operate_object(workspace_id, forged["object_id"], "FORGED_CROSS_SCOPE")
    with database.connect() as connection:
        assert connection.execute("select count(*) from tasks").fetchone()[0] == before_tasks
        assert connection.execute(
            "select lifecycle_status from workspace_package_objects where object_id = ?",
            (forged["object_id"],),
        ).fetchone()[0] == "NEW"

    restarted = WorkspacePackageRuntime(database, tmp_path / "package-store")
    recovered = restarted.resolve_company_integration(workspace_id, success["object_id"])
    assert recovered["status"] == "COMPLETED"
    assert recovered["task"]["task_id"] == integrated["task"]["task_id"]
    assert recovered["execution"]["execution_id"] == integrated["execution"]["execution_id"]
    assert recovered["evidenceRefs"] == integrated["evidenceRefs"]
    assert recovered["resultRefs"] == integrated["resultRefs"]
    assert recovered["artifactRefs"] == integrated["artifactRefs"]
    assert recovered["reverseResolved"] is True

    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []
        assert connection.execute(
            "select count(*) from runtime_entities where entity_id = ? and entity_type = 'PACKAGE_DOMAIN_OBJECT'",
            (success["object_id"],),
        ).fetchone()[0] == 1
        assert connection.execute(
            "select count(*) from runtime_entities where parent_id = ? and entity_type in ('EVIDENCE','OUTCOME')",
            (success["object_id"],),
        ).fetchone()[0] == 2
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type in ('HANDOFF','DECISION_PACKET') and parent_id = ?",
            (success["object_id"],),
        ).fetchone()[0] == 0
