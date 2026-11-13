import json
import re
from pathlib import Path

import pytest

from backend.app.database import Database
from backend.app.workspace_package_runtime import (
    PACKAGE_DDL,
    PackageConflictError,
    PackageScopeError,
    PackageValidationError,
    WorkspacePackageRuntime,
)


PACKAGE_DEPARTMENT = "department-package-runtime"
PACKAGE_BUSINESS = "business-package-runtime"


def _seed_package_department(database: Database, company_id: str) -> None:
    with database.connect() as connection:
        connection.execute(
            "insert into department_instances(id, tenant_id, company_id, template_id, name, department_type, status) "
            "values (?, 'selfuse', ?, 'package-test-template', 'Package Test Department', 'TEST', 'active')",
            (PACKAGE_DEPARTMENT, company_id),
        )


def _install_package(runtime: WorkspacePackageRuntime, source: Path, company_id: str):
    return runtime.install(
        source,
        company_id,
        department_id=PACKAGE_DEPARTMENT,
        business_id=PACKAGE_BUSINESS,
        business_name="Customer Feedback Business",
    )


def _write_package(
    root: Path,
    *,
    action: str = "core.domain-object.create",
    surface_title: str = "Records",
    version: str = "0.1.0",
) -> None:
    (root / "schemas").mkdir(parents=True)
    manifest = {
        "schemaVersion": "curis.workspace-package/v1",
        "packageId": "com.example.test.feedback-lab",
        "version": version,
        "coreCompatibility": ">=0.1.0 <0.2.0",
        "workspace": {"name": "Feedback Lab", "navigation": {"label": "Feedback Lab", "icon": "i-chat"}},
        "surfaces": "surfaces.json",
        "domainSchemas": {"FeedbackRecord": "schemas/customer-feedback.json"},
        "actions": [action],
        "capabilityRequirements": [],
        "retention": "retain-business-data-read-only",
    }
    surfaces = {
        "main": {"component": "object-list", "title": surface_title, "objectType": "FeedbackRecord"},
        "context": {"component": "object-detail", "title": "Record detail", "objectType": "FeedbackRecord"},
        "utility": {"component": "object-create-form", "title": "Create record", "objectType": "FeedbackRecord", "action": action},
    }
    schema = {
        "schemaVersion": "0.1.0",
        "title": "Feedback record",
        "type": "object",
        "initialState": "NEW",
        "required": ["title", "channel", "summary", "status", "responsibilityRef"],
        "properties": {
            "title": {"type": "string", "title": "Title", "maxLength": 120},
            "customerRef": {"type": "string", "title": "Customer ref", "maxLength": 128},
            "channel": {"type": "string", "title": "Channel", "enum": ["INTERVIEW", "SUPPORT", "MANUAL"]},
            "summary": {"type": "string", "title": "Summary", "maxLength": 2000, "multiline": True},
            "status": {"type": "string", "title": "Status", "enum": ["NEW", "TRIAGED", "ARCHIVED"], "default": "NEW"},
            "responsibilityRef": {"type": "string", "title": "Responsibility ref", "maxLength": 128},
            "evidenceRef": {"type": "string", "title": "Evidence ref", "maxLength": 256},
        },
    }
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    (root / "surfaces.json").write_text(json.dumps(surfaces, ensure_ascii=False), encoding="utf-8")
    (root / "schemas/customer-feedback.json").write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")


def test_declarative_package_install_restart_failure_and_uninstall_retention(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "curis.sqlite"))
    database.initialize()
    with database.connect() as connection:
        connection.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status, is_default) values ('company-p0', 'selfuse', 'selfuse-ceo', 'P0 Company', 'active', 1)"
        )
    _seed_package_department(database, "company-p0")

    store = tmp_path / "package-store"
    runtime = WorkspacePackageRuntime(database, store)
    invalid = tmp_path / "invalid"
    _write_package(invalid, action="unsafe.shell")
    with pytest.raises(PackageValidationError):
        _install_package(runtime, invalid, "company-p0")
    assert runtime.registry(include_archived=True) == []
    assert not store.exists()

    source = tmp_path / "package"
    _write_package(source)
    installed = _install_package(runtime, source, "company-p0")
    workspace_id = installed["instance"]["workspace_id"]
    with database.connect() as connection:
        workspace_relation = connection.execute(
            "select business_id, business_relation_status from workspaces where workspace_id=?", (workspace_id,),
        ).fetchone()
        assert tuple(workspace_relation) == (PACKAGE_BUSINESS, "RESOLVED")
        assert connection.execute(
            "select count(*) from canonical_businesses where business_id=?", (PACKAGE_BUSINESS,),
        ).fetchone()[0] == 1
    stored_path = Path(installed["package"]["stored_path"])
    assert stored_path.is_dir()
    assert runtime.navigation("company-p0")[0]["label"] == "Feedback Lab"
    assert set(installed["surfaces"]) == {"main", "context", "utility"}
    assert installed["package"]["capability_requirements"] == installed["package"]["granted_capabilities"] == []

    conflict = tmp_path / "conflict"
    _write_package(conflict, surface_title="Another title")
    with pytest.raises(PackageConflictError):
        _install_package(runtime, conflict, "company-p0")
    assert len(runtime.registry()) == 1

    with pytest.raises(PackageValidationError):
        runtime.create_object(
            workspace_id,
            "core.domain-object.create",
            "FeedbackRecord",
            {
                "title": "伪造关系",
                "channel": "INTERVIEW",
                "summary": "Package 字符串不得冒充 Core 关系。",
                "responsibilityRef": "employee:fake",
            },
        )
    created = runtime.create_object(
        workspace_id,
        "core.domain-object.create",
        "FeedbackRecord",
        {
            "title": "导出结果不易定位",
            "customerRef": "customer:acme",
            "channel": "INTERVIEW",
            "summary": "客户需要从结果直接回到责任与证据。",
        },
    )
    assert created["object_type"] == "FeedbackRecord"
    assert created["lifecycle_status"] == "NEW"
    assert created["owner_ref"] == ""
    assert created["data"]["responsibilityRef"] == ""
    assert created["data"]["evidenceRef"] == ""
    assert created["company_integration"]["status"] == "NOT_STARTED"
    with database.connect() as connection:
        identity = connection.execute(
            "select entity_type, company_id, workspace_id from runtime_entities where entity_id = ?",
            (created["object_id"],),
        ).fetchone()
    assert dict(identity) == {
        "entity_type": "PACKAGE_DOMAIN_OBJECT",
        "company_id": "company-p0",
        "workspace_id": workspace_id,
    }

    restarted = WorkspacePackageRuntime(database, store)
    recovered = restarted.get_workspace(workspace_id)
    assert recovered["objects"][0]["object_id"] == created["object_id"]
    assert recovered["activities"][0]["action_id"] == "core.domain-object.create"

    disabled = restarted.disable(workspace_id)
    assert disabled["read_only"] is True
    assert restarted.navigation("company-p0") == []
    archived = restarted.uninstall(workspace_id)
    assert archived["package"]["status"] == "UNINSTALLED"
    assert archived["objects"][0]["object_id"] == created["object_id"]
    assert not stored_path.exists()
    with pytest.raises(PackageScopeError):
        restarted.get_workspace(workspace_id)
    with database.connect() as connection:
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert connection.execute("pragma foreign_key_check").fetchall() == []
        assert connection.execute("select status from workspaces where workspace_id = ?", (workspace_id,)).fetchone()[0] == "ARCHIVED"


def _package_table_sql(table: str) -> str:
    for statement in PACKAGE_DDL.split(";"):
        match = re.search(r"create table if not exists (\w+)", statement)
        if match and match.group(1) == table:
            return statement.strip()
    raise AssertionError(f"{table} not declared in PACKAGE_DDL")


def _legacy_parent_sql() -> str:
    new_sql = _package_table_sql("workspace_package_instances")
    legacy = new_sql.replace("  foreign key(tenant_id, package_id, package_version)",
                             "  unique(tenant_id, company_id, package_id, package_version),\n"
                             "  foreign key(tenant_id, package_id, package_version)")
    assert legacy != new_sql
    return legacy


def _force_legacy_parent_shape(database: Database) -> None:
    with database.connect() as connection:
        connection.execute("drop table workspace_package_instances")
        connection.execute(_legacy_parent_sql())


def _seed_unrelated_orphan(database: Database) -> None:
    with database.connect() as connection:
        connection.execute("create table if not exists unrelated_parent (id text primary key)")
        connection.execute(
            "create table if not exists unrelated_child ("
            "id text primary key, parent_id text references unrelated_parent(id))"
        )
        connection.execute("insert into unrelated_child values ('orphan-1', 'missing-parent')")


def _seed_installed_package(database: Database, *, status: str = "DISABLED") -> None:
    with database.connect() as connection:
        connection.execute(
            "insert into installed_workspace_packages(tenant_id, package_id, version, digest, status,"
            " manifest_json, surfaces_json, schemas_json, source_path, stored_path, installed_at)"
            " values ('selfuse', 'com.example.test.orphan-guard', '0.1.0', 'digest-1', ?,"
            " '{}', '{}', '{}', '/nonexistent', '/nonexistent', '2026-10-06T00:00:00Z')",
            (status,),
        )


def _seed_instance(database: Database, instance_id: str = "instance-1") -> None:
    with database.connect() as connection:
        connection.execute(
            "insert into workspace_package_instances(instance_id, tenant_id, company_id, workspace_id,"
            " package_id, package_version, package_digest, status, created_at, updated_at)"
            " values (?, 'selfuse', ?, ?, 'com.example.test.orphan-guard',"
            " '0.1.0', 'digest-1', 'DISABLED', '2026-10-06T00:00:00Z', '2026-10-06T00:00:00Z')",
            (instance_id, f"{instance_id}-company", f"{instance_id}-workspace"),
        )

def test_migration_tolerates_unrelated_orphans_when_parent_already_migrated(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "curis.sqlite"))
    database.initialize()
    WorkspacePackageRuntime(database, tmp_path / "store")
    _seed_unrelated_orphan(database)

    restarted = WorkspacePackageRuntime(database, tmp_path / "store")
    assert restarted.registry() == []
    with database.connect() as connection:
        leftovers = connection.execute("pragma foreign_key_check").fetchall()
        assert [row["table"] for row in leftovers] == ["unrelated_child"]
        for table in ("workspace_package_instances", "workspace_package_objects",
                      "workspace_package_activities", "workspace_package_lifecycle_events",
                      "workspace_package_migration_journal"):
            assert connection.execute(f'pragma foreign_key_check("{table}")').fetchall() == []


@pytest.mark.parametrize("orphan_target", ["parent", "workspace_package_objects"])
def test_migration_rejects_package_domain_orphans(tmp_path: Path, orphan_target: str) -> None:
    database = Database(str(tmp_path / "curis.sqlite"))
    database.initialize()
    WorkspacePackageRuntime(database, tmp_path / "store")
    _force_legacy_parent_shape(database)
    if orphan_target == "parent":
        with database.connect() as connection:
            connection.execute(
                "insert into workspace_package_instances(instance_id, tenant_id, company_id, workspace_id,"
                " package_id, package_version, package_digest, status, created_at, updated_at)"
                " values ('orphan-instance', 'selfuse', 'company-1', 'workspace-1', 'missing-package',"
                " '0.1.0', 'digest-x', 'DISABLED', '2026-10-06T00:00:00Z', '2026-10-06T00:00:00Z')"
            )
    else:
        with database.connect() as connection:
            connection.execute(
                "insert into workspace_package_objects(object_id, instance_id, tenant_id, company_id,"
                " workspace_id, object_type, schema_version, lifecycle_status, data_json, created_at, updated_at)"
                " values ('orphan-object', 'missing-instance', 'selfuse', 'company-1', 'workspace-1',"
                " 'FeedbackRecord', '0.1.0', 'NEW', '{}', '2026-10-06T00:00:00Z', '2026-10-06T00:00:00Z')"
            )

    with pytest.raises(PackageConflictError, match="pre-existing orphan"):
        WorkspacePackageRuntime(database, tmp_path / "store")


def test_migration_rebuilds_legacy_parent_with_unrelated_orphans_preserving_rows(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "curis.sqlite"))
    database.initialize()
    WorkspacePackageRuntime(database, tmp_path / "store")
    _force_legacy_parent_shape(database)
    _seed_installed_package(database)
    _seed_instance(database, "instance-legacy-1")
    _seed_instance(database, "instance-legacy-2")
    _seed_unrelated_orphan(database)
    with database.connect() as connection:
        before = connection.execute("select * from workspace_package_instances order by 1").fetchall()
        legacy_sql = connection.execute(
            "select sql from sqlite_master where name = 'workspace_package_instances'").fetchone()[0]
    assert "unique(tenant_id, company_id, package_id, package_version)" in legacy_sql

    restarted = WorkspacePackageRuntime(database, tmp_path / "store")
    assert restarted.registry() == []
    with database.connect() as connection:
        after = connection.execute("select * from workspace_package_instances order by 1").fetchall()
        assert [tuple(row) for row in after] == [tuple(row) for row in before]
        migrated_sql = connection.execute(
            "select sql from sqlite_master where name = 'workspace_package_instances'").fetchone()[0]
        assert "unique(tenant_id, company_id, package_id, package_version)" not in migrated_sql
        for table in ("workspace_package_instances", "workspace_package_objects",
                      "workspace_package_activities", "workspace_package_lifecycle_events",
                      "workspace_package_migration_journal"):
            assert connection.execute(f'pragma foreign_key_check("{table}")').fetchall() == []
        leftovers = connection.execute("pragma foreign_key_check").fetchall()
        assert [row["table"] for row in leftovers] == ["unrelated_child"]
        assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
