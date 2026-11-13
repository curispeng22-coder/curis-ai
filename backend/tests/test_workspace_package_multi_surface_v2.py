from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.database import Database
from backend.app.runtime import ResponsibilityRoutingRuntime, RuntimeFoundation
from backend.app.runtime.workspace import WorkspaceRuntime
from backend.app.tenant_context import TenantContext
from backend.app.workspace_package_runtime import PackageScopeError, PackageValidationError, WorkspacePackageRuntime, validate_package
from backend.tests.db_safety import require_isolated_test_database
from backend.tests.test_workspace_package_runtime_p0 import _install_package, _seed_package_department, _write_package


TENANT = "selfuse"
COMPANY = "company-multi-surface"
CEO = "ceo-multi-surface"
CAPABILITY_ID = "core.customer-feedback-triage"
RESPONSIBILITY = "CUSTOMER_FEEDBACK_TRIAGE"


def _write_v2(root: Path, *, version: str = "0.1.0", variant: str = "A") -> None:
    (root / "schemas").mkdir(parents=True)
    capability = {
        "key": "feedback-triage", "source": "tenant_private", "capabilityType": "tool",
        "capabilityId": CAPABILITY_ID,
    }
    manifest = {
        "schemaVersion": "curis.workspace-package/v2",
        "packageId": "com.curis.test.multi-surface-office",
        "publisher": "com.curis.test",
        "version": version,
        "coreCompatibility": ">=0.1.0 <0.2.0",
        "workspace": {
            "name": "Generic Operations Office",
            "navigation": {"label": "Generic Office", "icon": "i-widgets"},
            "domainNavigation": "domain-navigation.json",
            "surfaceRegistry": "professional-surfaces.json",
            "defaultSurfaceRef": "overview",
        },
        "domainSchemas": {"FeedbackRecord": "schemas/feedback.json"},
        "objectViews": "object-views.json",
        "responsibilityRequirements": "responsibility-requirements.json",
        "projectionProfiles": "projection-profiles.json",
        "capabilityRequirements": [capability],
        "actions": ["core.domain-object.create"],
        "retention": "retain-business-data-read-only",
    }
    navigation = [
        {"key": "overview-nav", "label": "Overview", "surfaceRef": "overview", "order": 10, "group": None, "availabilityRef": None},
        {"key": "research-nav", "label": "Research" if variant == "A" else "Research Desk", "surfaceRef": "research", "order": 20, "group": None, "availabilityRef": None},
        {"key": "operations-nav", "label": "Operations", "surfaceRef": "operations", "order": 30, "group": None, "availabilityRef": None},
        {"key": "insights-nav", "label": "Insights", "surfaceRef": "insights", "order": 40, "group": None, "availabilityRef": "insights"},
    ]
    surfaces = [
        {
            "key": "overview", "purpose": "Review the complete Workspace truth", "navigationRefs": ["overview-nav"],
            "defaultEligible": True, "objectTypes": ["FeedbackRecord"],
            "viewRefs": ["feedback-list", "work-list", "result-list"], "primaryViewRef": "feedback-list",
            "responsibilityRequirementRefs": [], "capabilityRequirementRefs": [],
            "projectionRefs": ["shared-work", "shared-results"], "detailViewRef": "feedback-detail",
            "utilityViewRef": "feedback-create", "availability": {"mode": "REQUIRED", "condition": None},
        },
        {
            "key": "research", "purpose": "Research and triage feedback", "navigationRefs": ["research-nav"],
            "defaultEligible": False, "objectTypes": ["FeedbackRecord"],
            "viewRefs": ["feedback-list", "evidence-list"], "primaryViewRef": "feedback-list",
            "responsibilityRequirementRefs": ["feedback-owner"], "capabilityRequirementRefs": [],
            "projectionRefs": ["shared-evidence"], "detailViewRef": "feedback-detail",
            "utilityViewRef": "feedback-create", "availability": {"mode": "REQUIRED", "condition": None},
        },
        {
            "key": "operations", "purpose": "Operate current work", "navigationRefs": ["operations-nav"],
            "defaultEligible": False, "objectTypes": ["FeedbackRecord"],
            "viewRefs": ["work-list", "result-list"], "primaryViewRef": "work-list",
            "responsibilityRequirementRefs": ["feedback-owner"], "capabilityRequirementRefs": [],
            "projectionRefs": ["shared-work", "shared-results"], "detailViewRef": "feedback-detail",
            "utilityViewRef": None, "availability": {"mode": "REQUIRED", "condition": None},
        },
        {
            "key": "insights", "purpose": "Inspect object-dependent insights", "navigationRefs": ["insights-nav"],
            "defaultEligible": False, "objectTypes": ["FeedbackRecord"],
            "viewRefs": ["evidence-list"], "primaryViewRef": "evidence-list",
            "responsibilityRequirementRefs": [], "capabilityRequirementRefs": [],
            "projectionRefs": ["shared-evidence"], "detailViewRef": None,
            "utilityViewRef": None, "availability": {"mode": "CONDITIONAL", "condition": "WORKSPACE_HAS_OBJECTS"},
        },
    ]
    if variant == "B":
        navigation.append({
            "key": "archive-nav", "label": "Archive", "surfaceRef": "archive", "order": 50,
            "group": None, "availabilityRef": None,
        })
        surfaces.append({
            "key": "archive", "purpose": "Optional historical view", "navigationRefs": ["archive-nav"],
            "defaultEligible": False, "objectTypes": ["FeedbackRecord"],
            "viewRefs": ["feedback-list"], "primaryViewRef": "feedback-list",
            "responsibilityRequirementRefs": [], "capabilityRequirementRefs": [], "projectionRefs": [],
            "detailViewRef": "feedback-detail", "utilityViewRef": None,
            "availability": {"mode": "OPTIONAL", "condition": None},
        })
    if variant == "REMOVED":
        navigation = [item for item in navigation if item["surfaceRef"] != "research"]
        surfaces = [item for item in surfaces if item["key"] != "research"]
    views = [
        {"key": "feedback-list", "component": "object-list", "title": "Feedback", "objectType": "FeedbackRecord", "action": None},
        {"key": "feedback-detail", "component": "object-detail", "title": "Feedback detail", "objectType": "FeedbackRecord", "action": None},
        {"key": "feedback-create", "component": "object-create-form", "title": "Create feedback", "objectType": "FeedbackRecord", "action": "core.domain-object.create"},
        {"key": "work-list", "component": "workspace-work-list", "title": "Current Work", "objectType": None, "action": None},
        {"key": "result-list", "component": "workspace-result-list", "title": "Results", "objectType": None, "action": None},
        {"key": "evidence-list", "component": "workspace-evidence-list", "title": "Evidence", "objectType": None, "action": None},
    ]
    requirements = [{
        "key": "feedback-owner", "purpose": "Own feedback triage", "responsibilityKey": RESPONSIBILITY,
        "capabilityRequirementRefs": ["feedback-triage"],
        "surfaceRefs": ["operations"] if variant == "REMOVED" else ["research", "operations"],
    }]
    projections = [
        {"key": "shared-work", "type": "CORE_WORK", "selectors": {"workspaceScope": "CURRENT", "objectTypes": ["FeedbackRecord"], "requirementRefs": ["feedback-owner"], "lifecycleCategories": []}},
        {"key": "shared-results", "type": "CORE_RESULT", "selectors": {"workspaceScope": "CURRENT", "objectTypes": ["FeedbackRecord"], "requirementRefs": ["feedback-owner"], "lifecycleCategories": []}},
        {"key": "shared-evidence", "type": "CORE_EVIDENCE", "selectors": {"workspaceScope": "CURRENT", "objectTypes": ["FeedbackRecord"], "requirementRefs": ["feedback-owner"], "lifecycleCategories": []}},
    ]
    schema = {
        "schemaVersion": "0.1.0", "title": "Feedback", "type": "object", "initialState": "NEW",
        "required": ["title", "channel", "summary", "status", "responsibilityRef"],
        "properties": {
            "title": {"type": "string", "title": "Title", "maxLength": 120},
            "channel": {"type": "string", "title": "Channel", "enum": ["INTERVIEW", "SUPPORT"]},
            "summary": {"type": "string", "title": "Summary", "maxLength": 2000, "multiline": True},
            "status": {"type": "string", "title": "Status", "enum": ["NEW", "TRIAGED", "ARCHIVED"], "default": "NEW"},
            "responsibilityRef": {"type": "string", "title": "Responsibility", "maxLength": 128},
            "evidenceRef": {"type": "string", "title": "Evidence", "maxLength": 256},
        },
    }
    files = {
        "manifest.json": manifest,
        "domain-navigation.json": {"items": navigation},
        "professional-surfaces.json": {"surfaces": surfaces},
        "object-views.json": {"views": views},
        "responsibility-requirements.json": {"requirements": requirements},
        "projection-profiles.json": {"profiles": projections},
        "schemas/feedback.json": schema,
    }
    for name, value in files.items():
        (root / name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _database(path: Path) -> tuple[Database, WorkspacePackageRuntime]:
    require_isolated_test_database()
    database = Database(str(path))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status, is_default) "
            "values (?, ?, ?, 'Multi Surface Company', 'active', 1)",
            (COMPANY, TENANT, CEO),
        )
    _seed_package_department(database, COMPANY)
    database.save_tenant_private_capability(
        tenant_id=TENANT, capability_type="tool", capability_id=CAPABILITY_ID,
        display_name="Core Customer Feedback Triage",
        metadata={"handler": CAPABILITY_ID, "live_status": "available", "permissions": ["feedback.read"], "cost_per_unit": 0},
    )
    return database, WorkspacePackageRuntime(database, path.parent / "package-store")


def _staff(database: Database, workspace_id: str, *, employee_id: str = "employee-feedback") -> dict:
    foundation = RuntimeFoundation(database)
    role_id, binding_id = "role-feedback", "binding-feedback"
    with database.connect() as connection:
        supply = WorkspaceRuntime(database)._resolve_supply(connection, "tenant_private", "tool", CAPABILITY_ID)
        review = WorkspaceRuntime(database)._assess_supply(connection, supply)
    if employee_id == "employee-feedback":
        foundation.create(
            "ROLE_SLOT", entity_id=role_id, company_id=COMPANY, workspace_id=workspace_id,
            lifecycle_status="ASSIGNED", data={
                "name": "Feedback Owner", "responsibilityType": RESPONSIBILITY,
                "responsibility": "Own feedback triage", "assignedEmployeeRef": employee_id,
                "capabilityRefs": ["requirement:feedback-triage"], "staffingStatus": "ASSIGNED",
            },
        )
        foundation.create(
            "CAPABILITY_BINDING", entity_id=binding_id, company_id=COMPANY, workspace_id=workspace_id,
            lifecycle_status="ACTIVE", capability_ref="requirement:feedback-triage",
            data={"name": "Feedback Triage", "requirementRef": "requirement:feedback-triage", "authorizationStatus": "AUTHORIZED_ACTIVE", "supplyReview": review},
        )
        foundation.link(role_id, "REQUIRES_CAPABILITY", binding_id)
    foundation.create(
        "AI_EMPLOYEE", entity_id=employee_id, company_id=COMPANY, workspace_id=workspace_id,
        lifecycle_status="AVAILABLE", presence_state="AVAILABLE",
        data={"name": employee_id, "roleSlotRef": role_id, "responsibility": "Own feedback triage", "staffingStatus": "HIRED_AVAILABLE"},
    )
    foundation.link(employee_id, "PROPOSED_FOR", role_id)
    routing = ResponsibilityRoutingRuntime(database)
    if employee_id == "employee-feedback":
        assignment = routing.create_assignment(
            company_id=COMPANY, scope_type="WORKSPACE", scope_ref=workspace_id, workspace_id=workspace_id,
            role_ref=role_id, employee_ref=employee_id, responsibility_key=RESPONSIBILITY,
            responsibility="Own feedback triage", capability_binding_refs=[binding_id], assignment_id="assignment-feedback",
        )
    else:
        assignment = routing.update_assignment("assignment-feedback", employee_ref=employee_id)
    return {"role": role_id, "binding": binding_id, "employee": employee_id, "assignment": assignment["entity_id"]}


def test_v1_is_still_readable_under_version_dispatch(tmp_path: Path) -> None:
    require_isolated_test_database()
    source = tmp_path / "v1"
    _write_package(source)
    assert validate_package(source)["manifest"]["schemaVersion"] == "curis.workspace-package/v1"


def test_v2_compiles_resolves_projects_updates_and_restarts(tmp_path: Path) -> None:
    database, runtime = _database(tmp_path / "curis.sqlite")
    source = tmp_path / "v2-a"
    _write_v2(source)
    installed = _install_package(runtime, source, COMPANY)
    workspace_id = installed["instance"]["workspace_id"]
    digest = installed["package"]["digest"]
    assert installed["package"]["schema_version"] == "curis.workspace-package/v2"
    assert len(installed["surfaceModel"]["surfaces"]) == 4
    assert installed["surfaceModel"]["operationalStatus"] == "DRAFT"
    assert {item["status"] for item in installed["surfaceModel"]["requirementResolution"]} == {"RESPONSIBILITY_GAP"}
    assert next(item for item in installed["surfaceModel"]["surfaces"] if item["key"] == "insights")["status"] == "CONDITION_NOT_MET"

    core = _staff(database, workspace_id)
    resolved = runtime.get_workspace(workspace_id)
    assert resolved["surfaceModel"]["operationalStatus"] == "OPERATIONAL"
    requirement = resolved["surfaceModel"]["requirementResolution"][0]
    assert requirement["assignmentRef"] == core["assignment"]
    assert requirement["employeeRef"] == core["employee"]
    assert requirement["capabilityBindingRefs"] == [core["binding"]]
    assert {item["key"] for item in resolved["surfaceModel"]["surfaces"] if item["eligible"]} == {"overview", "research", "operations"}
    assert all("employee" not in json.dumps(item).lower() for item in validate_package(source)["manifest"]["capabilityRequirements"])
    assert resolved["surfaceModel"]["surfaces"][0]["viewRefs"] == ["feedback-list", "work-list", "result-list"]
    assert not set(item["key"] for item in resolved["surfaceModel"]["objectViews"]) & set(item["key"] for item in resolved["surfaceModel"]["surfaces"])

    with database.connect() as connection:
        connection.execute("update runtime_entities set lifecycle_status='DISABLED' where entity_id=?", (core["binding"],))
    assert runtime.get_workspace(workspace_id)["surfaceModel"]["requirementResolution"][0]["status"] == "CAPABILITY_GAP"
    with database.connect() as connection:
        connection.execute("update runtime_entities set lifecycle_status='ACTIVE' where entity_id=?", (core["binding"],))
        assignment = connection.execute("select data_json from runtime_entities where entity_id=?", (core["assignment"],)).fetchone()
        assignment_data = json.loads(assignment[0])
        assignment_data["employeeRef"] = "employee-outside-scope"
        connection.execute("update runtime_entities set data_json=? where entity_id=?", (json.dumps(assignment_data), core["assignment"]))
    assert runtime.get_workspace(workspace_id)["surfaceModel"]["requirementResolution"][0]["status"] == "UNSTAFFED"
    ResponsibilityRoutingRuntime(database).update_assignment(core["assignment"], employee_ref=core["employee"])

    created = runtime.create_object(
        workspace_id, "core.domain-object.create", "FeedbackRecord",
        {"title": "Export navigation", "channel": "INTERVIEW", "summary": "Customers need a durable route back to evidence."},
    )
    assert runtime.get_workspace(workspace_id)["surfaceModel"]["surfaces"][3]["eligible"] is True
    operated = runtime.operate_object(workspace_id, created["object_id"], RESPONSIBILITY)
    assert operated["status"] == "COMPLETED"
    projected = runtime.get_workspace(workspace_id)
    assert projected["shared"]["projections"]["shared-work"][0]["object_ref"] == created["object_id"]
    assert projected["shared"]["projections"]["shared-results"]
    assert projected["shared"]["projections"]["shared-evidence"]
    with database.connect() as connection:
        origin_before = connection.execute(
            "select data_json from runtime_entities where entity_id=?", (created["object_id"],),
        ).fetchone()[0]

    second = _staff(database, workspace_id, employee_id="employee-feedback-2")
    swapped = runtime.get_workspace(workspace_id)["surfaceModel"]["requirementResolution"][0]
    assert swapped["employeeRef"] == second["employee"]
    assert runtime.get_workspace(workspace_id)["package"]["digest"] == digest

    target = tmp_path / "v2-b"
    _write_v2(target, version="0.2.0", variant="B")
    preview = runtime.preview_update(workspace_id, target)
    assert preview["compatible"] is True
    upgraded = runtime.update(workspace_id, target)
    assert upgraded["instance"]["workspace_id"] == workspace_id
    assert upgraded["instance"]["package_version"] == "0.2.0"
    assert len(upgraded["surfaceModel"]["surfaces"]) == 5
    with database.connect() as connection:
        assert connection.execute(
            "select data_json from runtime_entities where entity_id=?", (created["object_id"],),
        ).fetchone()[0] == origin_before

    removed = tmp_path / "v2-removed"
    _write_v2(removed, version="0.3.0", variant="REMOVED")
    rejected = runtime.preview_update(workspace_id, removed)
    assert rejected["compatible"] is False
    assert "SURFACE_REMOVAL_REQUIRES_EXPLICIT_MIGRATION" in rejected["reasons"]
    with pytest.raises(PackageValidationError, match="SURFACE_REMOVAL_REQUIRES_EXPLICIT_MIGRATION"):
        runtime.update(workspace_id, removed)

    restarted = WorkspacePackageRuntime(database, tmp_path / "package-store")
    recovered = restarted.get_workspace(workspace_id)
    assert recovered["instance"]["workspace_id"] == workspace_id
    assert recovered["instance"]["package_version"] == "0.2.0"
    assert recovered["surfaceModel"]["operationalStatus"] == "OPERATIONAL"
    assert recovered["shared"]["projections"]["shared-evidence"]
    assert restarted.navigation(COMPANY)[0]["workspace_id"] == workspace_id
    with TenantContext.scope("other-tenant"):
        with pytest.raises(PackageScopeError):
            restarted.get_workspace(workspace_id)
    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []


def test_v2_rejects_unknown_condition_employee_binding_and_cross_scope_assignment(tmp_path: Path) -> None:
    source = tmp_path / "invalid"
    _write_v2(source)
    registry = json.loads((source / "professional-surfaces.json").read_text())
    registry["surfaces"][0]["employee_id"] = "forbidden"
    (source / "professional-surfaces.json").write_text(json.dumps(registry))
    with pytest.raises(PackageValidationError):
        validate_package(source)

    unknown = tmp_path / "unknown"
    _write_v2(unknown)
    registry = json.loads((unknown / "professional-surfaces.json").read_text())
    registry["surfaces"][3]["availability"]["condition"] = "ARBITRARY_EXPRESSION"
    (unknown / "professional-surfaces.json").write_text(json.dumps(registry))
    with pytest.raises(PackageValidationError):
        validate_package(unknown)
