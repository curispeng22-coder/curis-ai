from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.database import Database
from backend.app.workspace_package_runtime import (
    PackageValidationError,
    WorkspacePackageRuntime,
    validate_package,
)
from backend.tests.test_workspace_package_company_integration_p05 import (
    CAPABILITY_ID,
    COMPANY,
    RESPONSIBILITY,
    _feedback,
    _staff_company_os,
)
from backend.tests.test_workspace_package_runtime_p0 import _install_package, _seed_package_department, _write_package


def _migration_package(root: Path, *, version: str = "0.2.0", reversible: bool = True) -> None:
    _write_package(root, version=version, surface_title=f"Records {version}")
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["migrationManifest"] = "migrations/manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    schema_path = root / "schemas/customer-feedback.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["schemaVersion"] = "0.2.0"
    schema["properties"]["accountRef"] = schema["properties"].pop("customerRef")
    schema_path.write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")

    (root / "migrations").mkdir()
    migration = {
        "schemaVersion": "curis.workspace-migration/v1",
        "fromVersion": "0.1.0",
        "toVersion": version,
        "reversible": reversible,
        "objects": {
            "FeedbackRecord": {
                "fromSchemaVersion": "0.1.0",
                "toSchemaVersion": "0.2.0",
                "up": [{"op": "renameField", "from": "customerRef", "to": "accountRef"}],
                "down": (
                    [{"op": "renameField", "from": "accountRef", "to": "customerRef"}]
                    if reversible else []
                ),
            },
        },
    }
    (root / "migrations/manifest.json").write_text(
        json.dumps(migration, ensure_ascii=False), encoding="utf-8",
    )


def _company(path: Path) -> tuple[Database, WorkspacePackageRuntime, str, Path]:
    database = Database(str(path / "curis.sqlite"))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status, is_default) "
            "values (?, 'selfuse', 'ceo-p15', 'P1.5 Company', 'active', 1)",
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
    store = path / "package-store"
    v1 = path / "package-v1"
    _write_package(v1, version="0.1.0", surface_title="Records v1")
    runtime = WorkspacePackageRuntime(database, store)
    workspace_id = _install_package(runtime, v1, COMPANY)["instance"]["workspace_id"]
    return database, runtime, workspace_id, store


def _identity(database: Database, workspace_id: str) -> dict:
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
        entities = [dict(row) for row in connection.execute(
            "select entity_id, entity_type, company_id, workspace_id, parent_id, owner_ref, lifecycle_status, "
            "capability_ref, execution_ref from runtime_entities where workspace_id = ? order by entity_id",
            (workspace_id,),
        ).fetchall()]
        links = [dict(row) for row in connection.execute(
            "select * from runtime_links where workspace_id = ? order by link_id", (workspace_id,),
        ).fetchall()]
    return {"workspace": workspace, "instance": instance, "entities": entities, "links": links}


def _object_rows(database: Database, workspace_id: str) -> list[dict]:
    with database.connect() as connection:
        return [
            dict(row) | {"data": json.loads(row["data_json"])}
            for row in connection.execute(
                "select object_id, schema_version, lifecycle_status, owner_ref, data_json "
                "from workspace_package_objects where workspace_id = ? order by object_id",
                (workspace_id,),
            ).fetchall()
        ]


def test_transactional_migration_failure_restart_continue_and_down_rollback(tmp_path: Path) -> None:
    database, runtime, workspace_id, store = _company(tmp_path)
    core = _staff_company_os(database, workspace_id)
    first = _feedback(runtime, workspace_id, summary="客户要求迁移后身份、责任、执行与证据仍连续。")
    integrated = runtime.operate_object(workspace_id, first["object_id"], RESPONSIBILITY)
    second = _feedback(runtime, workspace_id, summary="第二条数据用于验证中途失败不会留下半迁移。")
    identity_v1 = _identity(database, workspace_id)
    objects_v1 = _object_rows(database, workspace_id)

    v2 = tmp_path / "package-v2"
    _migration_package(v2)
    preview = runtime.preview_update(workspace_id, v2)
    assert preview["compatible"] is True
    assert preview["migrationMode"] == "DECLARATIVE_RENAME_FIELDS_V1"
    assert preview["migration"]["reversible"] is True
    assert preview["migration"]["affectedObjects"] == 2

    fail_object = sorted([first["object_id"], second["object_id"]])[1]
    with database.connect() as connection:
        connection.execute(
            "create trigger fail_p15_mid_migration before update of schema_version on workspace_package_objects "
            f"when new.object_id = '{fail_object}' begin select raise(abort, 'p15 injected failure'); end"
        )
    with pytest.raises(Exception, match="p15 injected failure"):
        runtime.update(workspace_id, v2)
    with database.connect() as connection:
        connection.execute("drop trigger fail_p15_mid_migration")
        assert connection.execute(
            "select package_version from workspace_package_instances where workspace_id = ?", (workspace_id,),
        ).fetchone()[0] == "0.1.0"
        assert connection.execute(
            "select count(*) from workspace_package_lifecycle_events where workspace_id = ?", (workspace_id,),
        ).fetchone()[0] == 0
        failed = connection.execute(
            "select status, direction from workspace_package_migration_journal where workspace_id = ?",
            (workspace_id,),
        ).fetchall()
        assert [tuple(row) for row in failed] == [("FAILED", "UP")]
    assert _object_rows(database, workspace_id) == objects_v1
    assert _identity(database, workspace_id) == identity_v1
    assert not (store / "com.example.test.feedback-lab" / "0.2.0").exists()

    still_v1 = _feedback(runtime, workspace_id, summary="迁移失败后原办公室继续创建并处理真实反馈。")
    assert runtime.operate_object(workspace_id, still_v1["object_id"], RESPONSIBILITY)["status"] == "COMPLETED"
    identity_before_success = _identity(database, workspace_id)

    upgraded = runtime.update(workspace_id, v2)
    assert upgraded["instance"]["package_version"] == "0.2.0"
    migrated_rows = _object_rows(database, workspace_id)
    assert all(row["schema_version"] == "0.2.0" for row in migrated_rows)
    assert all("accountRef" in row["data"] and "customerRef" not in row["data"] for row in migrated_rows)
    assert _identity(database, workspace_id) == identity_before_success
    recovered = runtime.resolve_company_integration(workspace_id, first["object_id"])
    assert recovered["responsibility"]["roleSlotRef"] == core["role"]
    assert recovered["employee"]["employeeRef"] == core["employee"]
    assert recovered["task"]["task_id"] == integrated["task"]["task_id"]
    assert recovered["evidenceRefs"] == integrated["evidenceRefs"]
    assert recovered["reverseResolved"] is True

    restarted = WorkspacePackageRuntime(database, store)
    assert restarted.lifecycle(workspace_id)["currentVersion"] == "0.2.0"
    post_restart = restarted.create_object(
        workspace_id,
        "core.domain-object.create",
        "FeedbackRecord",
        {
            "title": "迁移后继续经营",
            "accountRef": "account:post-migration",
            "channel": "SUPPORT",
            "summary": "Desktop 重启后用 v2 schema 创建并完成新的真实反馈。",
        },
    )
    post_operating = restarted.operate_object(workspace_id, post_restart["object_id"], RESPONSIBILITY)
    assert post_operating["status"] == "COMPLETED"
    identity_v2 = _identity(database, workspace_id)

    fail_down_object = sorted(row["object_id"] for row in _object_rows(database, workspace_id))[1]
    with database.connect() as connection:
        connection.execute(
            "create trigger fail_p15_mid_down before update of schema_version on workspace_package_objects "
            f"when new.object_id = '{fail_down_object}' begin select raise(abort, 'p15 injected down failure'); end"
        )
    with pytest.raises(Exception, match="p15 injected down failure"):
        restarted.rollback(workspace_id)
    with database.connect() as connection:
        connection.execute("drop trigger fail_p15_mid_down")
    assert restarted.lifecycle(workspace_id)["currentVersion"] == "0.2.0"
    assert all(row["schema_version"] == "0.2.0" for row in _object_rows(database, workspace_id))
    assert _identity(database, workspace_id) == identity_v2

    rolled_back = restarted.rollback(workspace_id)
    assert rolled_back["instance"]["package_version"] == "0.1.0"
    down_rows = _object_rows(database, workspace_id)
    assert all(row["schema_version"] == "0.1.0" for row in down_rows)
    assert all("customerRef" in row["data"] and "accountRef" not in row["data"] for row in down_rows)
    assert _identity(database, workspace_id) == identity_v2
    lifecycle = restarted.lifecycle(workspace_id)
    assert [event["action"] for event in lifecycle["events"]] == ["UPGRADE", "ROLLBACK"]
    assert [event["migration_mode"] for event in lifecycle["events"]] == [
        "DECLARATIVE_RENAME_FIELDS_V1", "DECLARATIVE_RENAME_FIELDS_V1",
    ]
    assert [item["status"] for item in lifecycle["migrations"]] == [
        "FAILED", "APPLIED", "FAILED", "APPLIED",
    ]

    restarted_again = WorkspacePackageRuntime(database, store)
    final = restarted_again.resolve_company_integration(workspace_id, post_restart["object_id"])
    assert restarted_again.lifecycle(workspace_id)["currentVersion"] == "0.1.0"
    assert final["task"]["task_id"] == post_operating["task"]["task_id"]
    assert final["reverseResolved"] is True
    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []
        assert connection.execute(
            "select count(*) from runtime_entities where entity_type in ('TEAM','OPERATING_TEAM')",
        ).fetchone()[0] == 0


def test_irreversible_migration_fails_before_store_or_journal(tmp_path: Path) -> None:
    database, runtime, workspace_id, store = _company(tmp_path)
    _feedback(runtime, workspace_id, summary="不可逆迁移必须在任何候选写入前失败。")
    excessive = tmp_path / "package-v2-extra-change"
    _migration_package(excessive)
    schema_path = excessive / "schemas/customer-feedback.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["properties"]["summary"]["maxLength"] = 1999
    schema_path.write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")
    hidden_change = runtime.preview_update(workspace_id, excessive)
    assert hidden_change["compatible"] is False
    assert "MIGRATION_SCHEMA_CHANGE_EXCEEDS_DECLARATION" in hidden_change["reasons"]

    irreversible = tmp_path / "package-v2-irreversible"
    _migration_package(irreversible, reversible=False)

    preview = runtime.preview_update(workspace_id, irreversible)
    assert preview["compatible"] is False
    assert "IRREVERSIBLE_MIGRATION_NOT_SUPPORTED" in preview["reasons"]
    with pytest.raises(PackageValidationError, match="IRREVERSIBLE_MIGRATION_NOT_SUPPORTED"):
        runtime.update(workspace_id, irreversible)
    assert runtime.lifecycle(workspace_id)["currentVersion"] == "0.1.0"
    assert runtime.lifecycle(workspace_id)["migrations"] == []
    assert not (store / "com.example.test.feedback-lab" / "0.2.0").exists()


def test_restart_recovers_prepared_attempt_without_inferring_activation(tmp_path: Path) -> None:
    database, runtime, workspace_id, store = _company(tmp_path)
    _feedback(runtime, workspace_id, summary="PREPARED journal 不能让重启从文件推断激活。")
    source = tmp_path / "package-v2"
    _migration_package(source)
    package = validate_package(source)
    target, created = runtime._store_package(package)
    assert created is True
    with database.connect() as connection:
        current = runtime._instance(connection, workspace_id)
        report = runtime._compatibility_report(current, package, require_newer=True)
        preflight = runtime._migration_preflight(connection, current, package, direction="up")
    runtime._prepare_migration(current, package, report, preflight, target, direction="UP")

    restarted = WorkspacePackageRuntime(database, store)
    lifecycle = restarted.lifecycle(workspace_id)
    assert lifecycle["currentVersion"] == "0.1.0"
    assert lifecycle["events"] == []
    assert lifecycle["migrations"][0]["status"] == "FAILED"
    assert lifecycle["migrations"][0]["error_code"] == "INTERRUPTED_BEFORE_ATOMIC_COMMIT"
    assert not (store / "com.example.test.feedback-lab" / "0.2.0").exists()
