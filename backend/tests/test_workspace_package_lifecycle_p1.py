from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.database import Database
from backend.app.workspace_package_runtime import (
    PackageConflictError,
    PackageValidationError,
    WorkspacePackageRuntime,
)
from backend.tests.test_workspace_package_company_integration_p05 import (
    CAPABILITY_ID,
    COMPANY,
    RESPONSIBILITY,
    _feedback,
    _staff_company_os,
)
from backend.tests.test_workspace_package_runtime_p0 import _install_package, _seed_package_department, _write_package


def _truth(database: Database, workspace_id: str) -> dict:
    with database.connect() as connection:
        workspace = dict(connection.execute(
            "select tenant_id, company_id, business_id, workspace_id from workspaces where workspace_id = ?",
            (workspace_id,),
        ).fetchone())
        instance = dict(connection.execute(
            "select instance_id, tenant_id, company_id, workspace_id from workspace_package_instances "
            "where workspace_id = ?",
            (workspace_id,),
        ).fetchone())
        objects = [dict(row) for row in connection.execute(
            "select * from workspace_package_objects where workspace_id = ? order by object_id",
            (workspace_id,),
        ).fetchall()]
        entities = [dict(row) for row in connection.execute(
            "select * from runtime_entities where workspace_id = ? order by entity_id",
            (workspace_id,),
        ).fetchall()]
        links = [dict(row) for row in connection.execute(
            "select * from runtime_links where workspace_id = ? order by link_id",
            (workspace_id,),
        ).fetchall()]
        tasks = [dict(row) for row in connection.execute(
            "select * from tasks where company_id = ? order by task_id",
            (COMPANY,),
        ).fetchall()]
    return {
        "workspace": workspace,
        "instance": instance,
        "objects": objects,
        "entities": entities,
        "links": links,
        "tasks": tasks,
    }


def test_schema_stable_upgrade_rollback_and_restart_preserve_operating_truth(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "curis.sqlite"))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status, is_default) "
            "values (?, 'selfuse', 'ceo-p1', 'P1 Lifecycle Company', 'active', 1)",
            (COMPANY,),
        )
    _seed_package_department(database, COMPANY)
    database.save_tenant_private_capability(
        tenant_id="selfuse",
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

    store = tmp_path / "package-store"
    v1 = tmp_path / "package-v1"
    _write_package(v1, version="0.1.0", surface_title="Records v1")
    runtime = WorkspacePackageRuntime(database, store)
    installed = _install_package(runtime, v1, COMPANY)
    workspace_id = installed["instance"]["workspace_id"]
    instance_id = installed["instance"]["instance_id"]
    core = _staff_company_os(database, workspace_id)
    feedback = _feedback(runtime, workspace_id, summary="客户需要升级后仍能找到原责任、执行与结果。")
    integrated = runtime.operate_object(workspace_id, feedback["object_id"], RESPONSIBILITY)
    assert integrated["status"] == "COMPLETED"
    before = _truth(database, workspace_id)

    v2 = tmp_path / "package-v2"
    _write_package(v2, version="0.2.0", surface_title="Records v2")
    preview = runtime.preview_update(workspace_id, v2)
    assert preview["compatible"] is True
    assert preview["migrationMode"] == "NONE_SCHEMA_IDENTICAL"
    assert preview["reasons"] == []

    upgraded = runtime.update(workspace_id, v2)
    assert upgraded["instance"]["instance_id"] == instance_id
    assert upgraded["instance"]["workspace_id"] == workspace_id
    assert upgraded["instance"]["package_version"] == "0.2.0"
    assert upgraded["surfaces"]["main"]["title"] == "Records v2"
    assert _truth(database, workspace_id) == before
    after_upgrade = runtime.resolve_company_integration(workspace_id, feedback["object_id"])
    assert after_upgrade["task"]["task_id"] == integrated["task"]["task_id"]
    assert after_upgrade["evidenceRefs"] == integrated["evidenceRefs"]
    assert after_upgrade["resultRefs"] == integrated["resultRefs"]
    assert after_upgrade["responsibility"]["roleSlotRef"] == core["role"]
    assert after_upgrade["employee"]["employeeRef"] == core["employee"]
    lifecycle = runtime.lifecycle(workspace_id)
    assert lifecycle["currentVersion"] == "0.2.0"
    assert [event["action"] for event in lifecycle["events"]] == ["UPGRADE"]
    assert lifecycle["events"][0]["data_fingerprint_before"] == lifecycle["events"][0]["data_fingerprint_after"]
    assert lifecycle["events"][0]["company_os_fingerprint_before"] == lifecycle["events"][0]["company_os_fingerprint_after"]

    restarted = WorkspacePackageRuntime(database, store)
    assert restarted.lifecycle(workspace_id)["currentVersion"] == "0.2.0"
    assert restarted.resolve_company_integration(workspace_id, feedback["object_id"])["reverseResolved"] is True

    with database.connect() as connection:
        v1_stored = Path(connection.execute(
            "select stored_path from installed_workspace_packages where tenant_id = 'selfuse' "
            "and package_id = 'com.example.test.feedback-lab' and version = '0.1.0'",
        ).fetchone()[0])
    quarantine = tmp_path / "rollback-target-quarantine"
    v1_stored.rename(quarantine)
    with pytest.raises(PackageConflictError, match="rollback target package is unavailable"):
        restarted.rollback(workspace_id)
    assert restarted.lifecycle(workspace_id)["currentVersion"] == "0.2.0"
    assert _truth(database, workspace_id) == before
    quarantine.rename(v1_stored)

    rolled_back = restarted.rollback(workspace_id)
    assert rolled_back["instance"]["instance_id"] == instance_id
    assert rolled_back["instance"]["package_version"] == "0.1.0"
    assert rolled_back["surfaces"]["main"]["title"] == "Records v1"
    assert _truth(database, workspace_id) == before
    lifecycle = restarted.lifecycle(workspace_id)
    assert lifecycle["currentVersion"] == "0.1.0"
    assert [event["action"] for event in lifecycle["events"]] == ["UPGRADE", "ROLLBACK"]
    assert all(event["migration_mode"] == "NONE_SCHEMA_IDENTICAL" for event in lifecycle["events"])

    restarted_again = WorkspacePackageRuntime(database, store)
    recovered = restarted_again.resolve_company_integration(workspace_id, feedback["object_id"])
    assert restarted_again.lifecycle(workspace_id)["currentVersion"] == "0.1.0"
    assert recovered["task"]["task_id"] == integrated["task"]["task_id"]
    assert recovered["execution"]["execution_id"] == integrated["execution"]["execution_id"]
    assert recovered["reverseResolved"] is True

    v3 = tmp_path / "package-v3-schema-change"
    _write_package(v3, version="0.3.0", surface_title="Records v3")
    schema_path = v3 / "schemas/customer-feedback.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["properties"]["summary"]["maxLength"] = 1999
    schema_path.write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")
    rejected = restarted_again.preview_update(workspace_id, v3)
    assert rejected["compatible"] is False
    assert rejected["migrationMode"] == "MIGRATION_REQUIRED_NOT_SUPPORTED"
    assert "MIGRATION_REQUIRED_NOT_SUPPORTED" in rejected["reasons"]
    with pytest.raises(PackageValidationError, match="MIGRATION_REQUIRED_NOT_SUPPORTED"):
        restarted_again.update(workspace_id, v3)
    assert restarted_again.lifecycle(workspace_id)["currentVersion"] == "0.1.0"
    assert len(restarted_again.lifecycle(workspace_id)["events"]) == 2
    assert _truth(database, workspace_id) == before
    assert not (store / "com.example.test.feedback-lab" / "0.3.0").exists()
    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []
