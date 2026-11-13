"""Minimal declarative Workspace Package substrate for P0."""

from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from uuid import uuid4

from .database import Database
from .result_store import ResultStore
from .runtime.workspace import WorkspaceRuntime
from .shared_workspace_projection import SharedWorkspaceProjection
from .tenant_context import TenantContext


PACKAGE_SCHEMA = "curis.workspace-package/v1"
PACKAGE_SCHEMA_V2 = "curis.workspace-package/v2"
MIGRATION_SCHEMA = "curis.workspace-migration/v1"
CORE_COMPATIBILITY = ">=0.1.0 <0.2.0"
SAFE_ACTIONS = frozenset({"core.domain-object.create"})
SAFE_COMPONENTS = {
    "main": "object-list",
    "context": "object-detail",
    "utility": "object-create-form",
}
MAX_FILES = 16
MAX_FILE_SIZE = 256 * 1024
V2_VIEW_COMPONENTS = frozenset({
    "object-list", "workspace-work-list", "workspace-result-list", "workspace-evidence-list",
    "object-detail", "object-create-form",
})
V2_PROJECTION_TYPES = frozenset({"CORE_WORK", "CORE_RESULT", "CORE_EVIDENCE"})
V2_AVAILABILITY_MODES = frozenset({"REQUIRED", "OPTIONAL", "CONDITIONAL"})
V2_CONDITIONS = frozenset({"WORKSPACE_HAS_OBJECTS"})
CORE_REFERENCE_FIELDS = frozenset({"responsibilityRef", "evidenceRef"})
PROTECTED_MIGRATION_FIELDS = CORE_REFERENCE_FIELDS | {"status"}
COMPANY_OPERATE_ACTION = "core.company-object.operate"
MIN_OPERATING_SUMMARY_LENGTH = 8
CORE_COMPANY_CAPABILITY = "core.customer-feedback-triage"

PACKAGE_DDL = """
create table if not exists installed_workspace_packages (
  tenant_id       text not null,
  package_id      text not null,
  version         text not null,
  digest          text not null,
  status          text not null check(status in ('ACTIVE','DISABLED','UNINSTALLED','BROKEN')),
  manifest_json   text not null,
  surfaces_json   text not null,
  schemas_json    text not null,
  source_path     text not null,
  stored_path     text not null,
  installed_at    text not null,
  disabled_at     text,
  uninstalled_at  text,
  primary key (tenant_id, package_id, version)
);

create table if not exists workspace_package_instances (
  instance_id     text primary key,
  tenant_id       text not null,
  company_id      text not null,
  workspace_id    text not null unique,
  package_id      text not null,
  package_version text not null,
  package_digest  text not null,
  status          text not null check(status in ('ACTIVE','DISABLED','ARCHIVED')),
  created_at      text not null,
  updated_at      text not null,
  foreign key(tenant_id, package_id, package_version)
    references installed_workspace_packages(tenant_id, package_id, version)
);

create table if not exists workspace_package_objects (
  object_id       text primary key,
  instance_id     text not null references workspace_package_instances(instance_id),
  tenant_id       text not null,
  company_id      text not null,
  workspace_id    text not null,
  object_type     text not null,
  schema_version  text not null,
  lifecycle_status text not null,
  owner_ref       text not null default '',
  data_json       text not null,
  created_at      text not null,
  updated_at      text not null
);

create table if not exists workspace_package_activities (
  activity_id     text primary key,
  instance_id     text not null references workspace_package_instances(instance_id),
  tenant_id       text not null,
  company_id      text not null,
  workspace_id    text not null,
  action_id       text not null,
  object_id       text not null references workspace_package_objects(object_id),
  detail_json     text not null default '{}',
  created_at      text not null
);

create table if not exists workspace_package_lifecycle_events (
  event_id                     text primary key,
  instance_id                  text not null references workspace_package_instances(instance_id),
  tenant_id                    text not null,
  company_id                   text not null,
  workspace_id                 text not null,
  package_id                   text not null,
  action                       text not null check(action in ('UPGRADE','ROLLBACK')),
  from_version                 text not null,
  from_digest                  text not null,
  to_version                   text not null,
  to_digest                    text not null,
  compatibility_mode           text not null,
  migration_mode               text not null,
  data_fingerprint_before      text not null,
  data_fingerprint_after       text not null,
  company_os_fingerprint_before text not null,
  company_os_fingerprint_after text not null,
  detail_json                  text not null default '{}',
  created_at                   text not null
);

create table if not exists workspace_package_migration_journal (
  migration_id        text primary key,
  instance_id         text not null references workspace_package_instances(instance_id),
  tenant_id           text not null,
  company_id          text not null,
  workspace_id        text not null,
  package_id          text not null,
  direction           text not null check(direction in ('UP','DOWN')),
  status              text not null check(status in ('PREPARED','APPLIED','FAILED')),
  from_version        text not null,
  from_digest         text not null,
  to_version          text not null,
  to_digest           text not null,
  reversible          integer not null check(reversible in (0,1)),
  affected_count      integer not null,
  target_path         text not null,
  migration_json      text not null,
  checkpoint_json     text not null,
  data_fingerprint_before text not null,
  data_fingerprint_after  text,
  protected_fingerprint_before text not null,
  protected_fingerprint_after  text,
  error_code          text,
  created_at          text not null,
  updated_at          text not null
);

create index if not exists idx_workspace_package_objects_scope
  on workspace_package_objects(tenant_id, company_id, workspace_id, object_type, created_at);
create index if not exists idx_workspace_package_activities_scope
  on workspace_package_activities(tenant_id, company_id, workspace_id, created_at);
create index if not exists idx_workspace_package_lifecycle_scope
  on workspace_package_lifecycle_events(tenant_id, company_id, workspace_id, created_at);
create index if not exists idx_workspace_package_migration_scope
  on workspace_package_migration_journal(tenant_id, company_id, workspace_id, created_at);
"""


class PackageValidationError(ValueError):
    pass


class PackageConflictError(RuntimeError):
    pass


class PackageScopeError(PermissionError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _version_tuple(version: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"0\.[0-9]+\.[0-9]+", version):
        raise PackageValidationError("package version is invalid")
    return tuple(int(part) for part in version.split("."))


def _fingerprint(rows: list[dict]) -> str:
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def _expect_keys(value: dict, required: set[str], *, where: str) -> None:
    if not isinstance(value, dict) or set(value) != required:
        raise PackageValidationError(f"{where} fields are invalid")


def _safe_ref(value: object, *, where: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise PackageValidationError(f"{where} must be a safe relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or any(part in {"", "."} for part in path.parts):
        raise PackageValidationError(f"{where} must be a safe relative path")
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", value):
        raise PackageValidationError(f"{where} contains unsupported characters")
    return value


def _read_json(root: Path, ref: str) -> dict:
    path = root.joinpath(*PurePosixPath(ref).parts)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PackageValidationError(f"invalid JSON file: {ref}") from error
    if not isinstance(value, dict):
        raise PackageValidationError(f"JSON root must be an object: {ref}")
    return value


def _validate_domain_schema(object_type: str, schema: dict) -> None:
    _expect_keys(
        schema,
        {"schemaVersion", "title", "type", "initialState", "required", "properties"},
        where=f"schema {object_type}",
    )
    if schema["type"] != "object" or not isinstance(schema["title"], str) or not schema["title"].strip():
        raise PackageValidationError(f"schema {object_type} is not an object contract")
    if not isinstance(schema["schemaVersion"], str) or not schema["schemaVersion"]:
        raise PackageValidationError(f"schema {object_type} needs schemaVersion")
    required = schema["required"]
    properties = schema["properties"]
    if not isinstance(required, list) or not isinstance(properties, dict) or not properties:
        raise PackageValidationError(f"schema {object_type} properties are invalid")
    if len(required) != len(set(required)) or any(name not in properties for name in required):
        raise PackageValidationError(f"schema {object_type} required fields are invalid")
    for name, field in properties.items():
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", name) or not isinstance(field, dict):
            raise PackageValidationError(f"schema {object_type} property is invalid")
        allowed = {"type", "title", "maxLength", "enum", "default", "multiline"}
        if set(field) - allowed or field.get("type") != "string" or not str(field.get("title") or "").strip():
            raise PackageValidationError(f"schema {object_type}.{name} is unsupported")
        if "maxLength" in field and (not isinstance(field["maxLength"], int) or not 1 <= field["maxLength"] <= 20000):
            raise PackageValidationError(f"schema {object_type}.{name} maxLength is invalid")
        if "enum" in field and (
            not isinstance(field["enum"], list)
            or not field["enum"]
            or len(field["enum"]) != len(set(field["enum"]))
            or any(not isinstance(item, str) or not item for item in field["enum"])
        ):
            raise PackageValidationError(f"schema {object_type}.{name} enum is invalid")
        if "default" in field and not isinstance(field["default"], str):
            raise PackageValidationError(f"schema {object_type}.{name} default is invalid")
        if field.get("default") and field.get("enum") and field["default"] not in field["enum"]:
            raise PackageValidationError(f"schema {object_type}.{name} default is outside enum")
    state = schema["initialState"]
    status = properties.get("status", {})
    if not isinstance(state, str) or state not in status.get("enum", []):
        raise PackageValidationError(f"schema {object_type} initialState must be a declared status")


def _validate_migration_manifest(migration: dict, manifest: dict, schemas: dict[str, dict]) -> None:
    _expect_keys(
        migration,
        {"schemaVersion", "fromVersion", "toVersion", "reversible", "objects"},
        where="migration manifest",
    )
    if migration["schemaVersion"] != MIGRATION_SCHEMA:
        raise PackageValidationError("migration schema is unsupported")
    if (
        not isinstance(migration["fromVersion"], str)
        or not isinstance(migration["toVersion"], str)
        or migration["toVersion"] != manifest["version"]
        or _version_tuple(migration["fromVersion"]) >= _version_tuple(migration["toVersion"])
    ):
        raise PackageValidationError("migration version transition is invalid")
    if not isinstance(migration["reversible"], bool):
        raise PackageValidationError("migration reversible flag is invalid")
    objects = migration["objects"]
    if not isinstance(objects, dict) or not objects:
        raise PackageValidationError("migration objects are invalid")
    for object_type, plan in objects.items():
        if object_type not in schemas or not isinstance(plan, dict):
            raise PackageValidationError("migration object type is invalid")
        _expect_keys(
            plan,
            {"fromSchemaVersion", "toSchemaVersion", "up", "down"},
            where=f"migration {object_type}",
        )
        if (
            not isinstance(plan["fromSchemaVersion"], str)
            or not isinstance(plan["toSchemaVersion"], str)
            or plan["fromSchemaVersion"] == plan["toSchemaVersion"]
            or plan["toSchemaVersion"] != schemas[object_type]["schemaVersion"]
        ):
            raise PackageValidationError(f"migration {object_type} schema versions are invalid")
        for direction in ("up", "down"):
            operations = plan[direction]
            if not isinstance(operations, list):
                raise PackageValidationError(f"migration {object_type} {direction} operations are invalid")
            for operation in operations:
                if not isinstance(operation, dict):
                    raise PackageValidationError("migration operation is invalid")
                _expect_keys(operation, {"op", "from", "to"}, where="migration operation")
                if operation["op"] != "renameField":
                    raise PackageValidationError("migration operation is unsupported")
                source, target = operation["from"], operation["to"]
                if (
                    not isinstance(source, str)
                    or not isinstance(target, str)
                    or source == target
                    or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", source)
                    or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", target)
                    or source in PROTECTED_MIGRATION_FIELDS
                    or target in PROTECTED_MIGRATION_FIELDS
                ):
                    raise PackageValidationError("migration field rename is invalid")
        if not plan["up"]:
            raise PackageValidationError(f"migration {object_type} has no up operation")
        if migration["reversible"]:
            expected_down = [
                {"op": "renameField", "from": item["to"], "to": item["from"]}
                for item in reversed(plan["up"])
            ]
            if plan["down"] != expected_down:
                raise PackageValidationError(f"migration {object_type} down operations are not exact inverse")
        elif plan["down"]:
            raise PackageValidationError("irreversible migration cannot declare down operations")


def _schema_after_renames(schema: dict, plan: dict, *, direction: str) -> dict:
    result = json.loads(json.dumps(schema, ensure_ascii=False))
    operations = plan[direction]
    for operation in operations:
        source, target = operation["from"], operation["to"]
        if source not in result["properties"] or target in result["properties"]:
            raise PackageValidationError("migration schema rename cannot be applied")
        result["properties"][target] = result["properties"].pop(source)
        result["required"] = [target if field == source else field for field in result["required"]]
    result["schemaVersion"] = (
        plan["toSchemaVersion"] if direction == "up" else plan["fromSchemaVersion"]
    )
    return result


def _data_after_renames(data: dict, operations: list[dict]) -> dict:
    result = dict(data)
    for operation in operations:
        source, target = operation["from"], operation["to"]
        if source not in result or target in result:
            raise PackageValidationError("migration data rename cannot be applied without loss")
        result[target] = result.pop(source)
    return result


def _package_digest(root: Path, entries: list[Path]) -> str:
    digest = hashlib.sha256()
    for ref in sorted(path.relative_to(root).as_posix() for path in entries):
        digest.update(ref.encode())
        digest.update(b"\0")
        digest.update(root.joinpath(*PurePosixPath(ref).parts).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_v2_package(root: Path, entries: list[Path], manifest: dict) -> dict:
    fields = {
        "schemaVersion", "packageId", "publisher", "version", "coreCompatibility", "workspace",
        "domainSchemas", "objectViews", "responsibilityRequirements", "projectionProfiles",
        "capabilityRequirements", "actions", "retention",
    }
    if set(manifest) not in (fields, fields | {"migrationManifest"}):
        raise PackageValidationError("v2 manifest fields are invalid")
    if manifest["coreCompatibility"] != CORE_COMPATIBILITY:
        raise PackageValidationError("package is not compatible with this Core")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:\.[a-z0-9-]+){2,7}", str(manifest["packageId"])):
        raise PackageValidationError("packageId is invalid")
    if not re.fullmatch(r"[a-z][a-z0-9.-]{2,127}", str(manifest["publisher"])):
        raise PackageValidationError("publisher is invalid")
    _version_tuple(str(manifest["version"]))
    workspace = manifest["workspace"]
    _expect_keys(
        workspace,
        {"name", "navigation", "domainNavigation", "surfaceRegistry", "defaultSurfaceRef"},
        where="v2 workspace",
    )
    _expect_keys(workspace["navigation"], {"label", "icon"}, where="navigation")
    if not isinstance(workspace["name"], str) or not workspace["name"].strip():
        raise PackageValidationError("workspace name is invalid")
    navigation = workspace["navigation"]
    if (
        not isinstance(navigation["label"], str) or not navigation["label"].strip()
        or not re.fullmatch(r"i-[a-z0-9_]+", str(navigation["icon"]))
    ):
        raise PackageValidationError("navigation contract is invalid")
    if manifest["actions"] != ["core.domain-object.create"] or set(manifest["actions"]) - SAFE_ACTIONS:
        raise PackageValidationError("package action is not allowed")
    if manifest["retention"] != "retain-business-data-read-only":
        raise PackageValidationError("retention contract is invalid")

    refs = {
        "domainNavigation": _safe_ref(workspace["domainNavigation"], where="domainNavigation"),
        "surfaceRegistry": _safe_ref(workspace["surfaceRegistry"], where="surfaceRegistry"),
        "objectViews": _safe_ref(manifest["objectViews"], where="objectViews"),
        "responsibilityRequirements": _safe_ref(
            manifest["responsibilityRequirements"], where="responsibilityRequirements",
        ),
        "projectionProfiles": _safe_ref(manifest["projectionProfiles"], where="projectionProfiles"),
    }
    domain_refs = manifest["domainSchemas"]
    if not isinstance(domain_refs, dict) or not domain_refs:
        raise PackageValidationError("domainSchemas is invalid")
    schemas = {}
    for object_type, ref in domain_refs.items():
        if not re.fullmatch(r"[A-Z][A-Za-z0-9]{1,63}", object_type):
            raise PackageValidationError("domain object type is invalid")
        safe = _safe_ref(ref, where=f"schema {object_type}")
        schemas[object_type] = _read_json(root, safe)
        _validate_domain_schema(object_type, schemas[object_type])

    navigation_model = _read_json(root, refs["domainNavigation"])
    surface_model = _read_json(root, refs["surfaceRegistry"])
    view_model = _read_json(root, refs["objectViews"])
    requirement_model = _read_json(root, refs["responsibilityRequirements"])
    projection_model = _read_json(root, refs["projectionProfiles"])
    for model, key, where in (
        (navigation_model, "items", "domain navigation"),
        (surface_model, "surfaces", "surface registry"),
        (view_model, "views", "object view registry"),
        (requirement_model, "requirements", "responsibility requirements"),
        (projection_model, "profiles", "projection profiles"),
    ):
        _expect_keys(model, {key}, where=where)
        if not isinstance(model[key], list):
            raise PackageValidationError(f"{where} must be a list")

    capabilities = manifest["capabilityRequirements"]
    if not isinstance(capabilities, list):
        raise PackageValidationError("capabilityRequirements must be a list")
    capability_by_key = {}
    for item in capabilities:
        _expect_keys(item, {"key", "source", "capabilityType", "capabilityId"}, where="capability requirement")
        key = item["key"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in capability_by_key
            or item["source"] not in {"tenant_private", "catalog"}
            or item["capabilityType"] not in {"tool", "model", "agent", "skill"}
            or not isinstance(item["capabilityId"], str) or not item["capabilityId"].strip()
        ):
            raise PackageValidationError("capability requirement is invalid")
        capability_by_key[key] = item

    view_by_key = {}
    for item in view_model["views"]:
        _expect_keys(item, {"key", "component", "title", "objectType", "action"}, where="object view")
        key = item["key"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in view_by_key or item["component"] not in V2_VIEW_COMPONENTS
            or not isinstance(item["title"], str) or not item["title"].strip()
            or item["objectType"] not in ({None} | set(schemas))
            or item["action"] not in ({None} | set(SAFE_ACTIONS))
        ):
            raise PackageValidationError("object view is invalid")
        if item["component"] in {"object-list", "object-detail", "object-create-form"} and not item["objectType"]:
            raise PackageValidationError("object view requires an objectType")
        if item["component"] == "object-create-form" and item["action"] not in SAFE_ACTIONS:
            raise PackageValidationError("create view requires a safe action")
        view_by_key[key] = item

    projection_by_key = {}
    for item in projection_model["profiles"]:
        _expect_keys(item, {"key", "type", "selectors"}, where="projection profile")
        _expect_keys(
            item["selectors"], {"workspaceScope", "objectTypes", "requirementRefs", "lifecycleCategories"},
            where="projection selectors",
        )
        key, selectors = item["key"], item["selectors"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in projection_by_key or item["type"] not in V2_PROJECTION_TYPES
            or selectors["workspaceScope"] != "CURRENT"
            or not isinstance(selectors["objectTypes"], list)
            or any(value not in schemas for value in selectors["objectTypes"])
            or not isinstance(selectors["requirementRefs"], list)
            or not isinstance(selectors["lifecycleCategories"], list)
            or any(not isinstance(value, str) for value in selectors["lifecycleCategories"])
        ):
            raise PackageValidationError("projection profile is invalid")
        projection_by_key[key] = item

    requirement_by_key = {}
    for item in requirement_model["requirements"]:
        _expect_keys(
            item,
            {"key", "purpose", "responsibilityKey", "capabilityRequirementRefs", "surfaceRefs"},
            where="responsibility requirement",
        )
        key = item["key"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in requirement_by_key
            or not isinstance(item["purpose"], str) or not item["purpose"].strip()
            or not re.fullmatch(r"[A-Z][A-Z0-9_]{2,63}", str(item["responsibilityKey"]))
            or not isinstance(item["capabilityRequirementRefs"], list)
            or any(ref not in capability_by_key for ref in item["capabilityRequirementRefs"])
            or not isinstance(item["surfaceRefs"], list)
        ):
            raise PackageValidationError("responsibility requirement is invalid")
        requirement_by_key[key] = item

    surface_by_key = {}
    for item in surface_model["surfaces"]:
        _expect_keys(
            item,
            {"key", "purpose", "navigationRefs", "defaultEligible", "objectTypes", "viewRefs",
             "primaryViewRef", "responsibilityRequirementRefs", "capabilityRequirementRefs",
             "projectionRefs", "detailViewRef", "utilityViewRef", "availability"},
            where="professional surface",
        )
        _expect_keys(item["availability"], {"mode", "condition"}, where="surface availability")
        key, availability = item["key"], item["availability"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in surface_by_key
            or not isinstance(item["purpose"], str) or not item["purpose"].strip()
            or not isinstance(item["defaultEligible"], bool)
            or not isinstance(item["navigationRefs"], list)
            or any(value not in schemas for value in item["objectTypes"])
            or not item["viewRefs"] or any(ref not in view_by_key for ref in item["viewRefs"])
            or item["primaryViewRef"] not in item["viewRefs"]
            or any(ref not in requirement_by_key for ref in item["responsibilityRequirementRefs"])
            or any(ref not in capability_by_key for ref in item["capabilityRequirementRefs"])
            or any(ref not in projection_by_key for ref in item["projectionRefs"])
            or item["detailViewRef"] not in ({None} | set(view_by_key))
            or item["utilityViewRef"] not in ({None} | set(view_by_key))
            or availability["mode"] not in V2_AVAILABILITY_MODES
            or (
                availability["mode"] == "CONDITIONAL"
                and availability["condition"] not in V2_CONDITIONS
            )
            or (availability["mode"] != "CONDITIONAL" and availability["condition"] is not None)
        ):
            raise PackageValidationError("professional surface is invalid")
        surface_by_key[key] = item

    navigation_by_key = {}
    for item in navigation_model["items"]:
        _expect_keys(item, {"key", "label", "surfaceRef", "order", "group", "availabilityRef"}, where="domain navigation item")
        key = item["key"]
        if (
            not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", key)
            or key in navigation_by_key or not isinstance(item["label"], str) or not item["label"].strip()
            or item["surfaceRef"] not in surface_by_key or not isinstance(item["order"], int)
            or item["order"] < 0 or item["group"] is not None and not isinstance(item["group"], str)
            or item["availabilityRef"] not in ({None} | set(surface_by_key))
        ):
            raise PackageValidationError("domain navigation item is invalid")
        navigation_by_key[key] = item
    if len({item["order"] for item in navigation_by_key.values()}) != len(navigation_by_key):
        raise PackageValidationError("domain navigation order must be stable and unique")
    for key, surface in surface_by_key.items():
        if any(ref not in navigation_by_key for ref in surface["navigationRefs"]):
            raise PackageValidationError("surface navigation reference is invalid")
        for requirement_ref in surface["responsibilityRequirementRefs"]:
            if key not in requirement_by_key[requirement_ref]["surfaceRefs"]:
                raise PackageValidationError("surface/requirement relation is not reciprocal")
    for requirement in requirement_by_key.values():
        if any(ref not in surface_by_key for ref in requirement["surfaceRefs"]):
            raise PackageValidationError("requirement surface reference is invalid")
    if workspace["defaultSurfaceRef"] not in surface_by_key or not surface_by_key[workspace["defaultSurfaceRef"]]["defaultEligible"]:
        raise PackageValidationError("default Surface is invalid")

    migration = None
    migration_ref = manifest.get("migrationManifest")
    if migration_ref is not None:
        migration_ref = _safe_ref(migration_ref, where="migrationManifest")
        migration = _read_json(root, migration_ref)
        _validate_migration_manifest(migration, manifest, schemas)
    declared = {"manifest.json", *refs.values(), *domain_refs.values()}
    if migration_ref:
        declared.add(migration_ref)
    actual = {path.relative_to(root).as_posix() for path in entries}
    if actual != declared:
        raise PackageValidationError("package contains undeclared or missing files")
    compiled = {
        "contract": PACKAGE_SCHEMA_V2,
        "domainNavigation": sorted(navigation_model["items"], key=lambda item: (item["order"], item["key"])),
        "surfaces": surface_model["surfaces"],
        "objectViews": view_model["views"],
        "responsibilityRequirements": requirement_model["requirements"],
        "capabilityRequirements": capabilities,
        "projectionProfiles": projection_model["profiles"],
        "defaultSurfaceRef": workspace["defaultSurfaceRef"],
    }
    return {
        "root": root.resolve(), "manifest": manifest, "surfaces": compiled,
        "schemas": schemas, "migration": migration, "digest": _package_digest(root, entries),
    }


def validate_package(source: str | Path) -> dict:
    root = Path(source)
    if not root.is_dir() or root.is_symlink():
        raise PackageValidationError("package source must be a real directory")
    entries = [path for path in root.rglob("*") if path.is_file() or path.is_symlink()]
    if not entries or len(entries) > MAX_FILES:
        raise PackageValidationError("package file count is invalid")
    if any(path.is_symlink() or path.stat().st_size > MAX_FILE_SIZE for path in entries):
        raise PackageValidationError("package symlink or file size is invalid")

    manifest = _read_json(root, "manifest.json")
    if manifest.get("schemaVersion") == PACKAGE_SCHEMA_V2:
        return _validate_v2_package(root, entries, manifest)
    manifest_fields = {
        "schemaVersion", "packageId", "version", "coreCompatibility", "workspace",
        "surfaces", "domainSchemas", "actions", "capabilityRequirements", "retention",
    }
    if not manifest_fields.issubset(manifest) or set(manifest) - manifest_fields - {"migrationManifest", "canonicalEntityBindings"}:
        raise PackageValidationError("manifest fields are invalid")
    if manifest["schemaVersion"] != PACKAGE_SCHEMA or manifest["coreCompatibility"] != CORE_COMPATIBILITY:
        raise PackageValidationError("package is not compatible with this Core")
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:\.[a-z0-9-]+){2,7}", str(manifest["packageId"])):
        raise PackageValidationError("packageId is invalid")
    if not re.fullmatch(r"0\.[0-9]+\.[0-9]+", str(manifest["version"])):
        raise PackageValidationError("P0 package version is invalid")
    _expect_keys(manifest["workspace"], {"name", "navigation"}, where="workspace")
    _expect_keys(manifest["workspace"]["navigation"], {"label", "icon"}, where="navigation")
    if any(not isinstance(manifest["workspace"][key], str) or not manifest["workspace"][key].strip() for key in ("name",)):
        raise PackageValidationError("workspace name is invalid")
    navigation = manifest["workspace"]["navigation"]
    if not isinstance(navigation["label"], str) or not navigation["label"].strip() or not re.fullmatch(r"i-[a-z0-9_]+", str(navigation["icon"])):
        raise PackageValidationError("navigation contract is invalid")
    if manifest["actions"] != ["core.domain-object.create"] or set(manifest["actions"]) - SAFE_ACTIONS:
        raise PackageValidationError("package action is not allowed")
    if manifest["capabilityRequirements"] != []:
        raise PackageValidationError("P0 package cannot request capabilities")
    if manifest["retention"] != "retain-business-data-read-only":
        raise PackageValidationError("retention contract is invalid")

    surfaces_ref = _safe_ref(manifest["surfaces"], where="surfaces")
    domain_refs = manifest["domainSchemas"]
    if not isinstance(domain_refs, dict) or not domain_refs:
        raise PackageValidationError("domainSchemas is invalid")
    bindings = manifest.get("canonicalEntityBindings", {})
    if (not isinstance(bindings, dict) or any(key not in domain_refs or not isinstance(value, str) or value not in {"CONTENT_ITEM", "CONTENT_VERSION", "PACKAGE_DOMAIN_OBJECT"}
                                             for key, value in bindings.items())):
        raise PackageValidationError("canonicalEntityBindings must name declared schemas and supported canonical types")
    schemas = {}
    for object_type, ref in domain_refs.items():
        if not re.fullmatch(r"[A-Z][A-Za-z0-9]{1,63}", object_type):
            raise PackageValidationError("domain object type is invalid")
        schemas[object_type] = _read_json(root, _safe_ref(ref, where=f"schema {object_type}"))
        _validate_domain_schema(object_type, schemas[object_type])

    migration = None
    migration_ref = manifest.get("migrationManifest")
    if migration_ref is not None:
        migration_ref = _safe_ref(migration_ref, where="migrationManifest")
        migration = _read_json(root, migration_ref)
        _validate_migration_manifest(migration, manifest, schemas)

    surfaces = _read_json(root, surfaces_ref)
    _expect_keys(surfaces, set(SAFE_COMPONENTS), where="surfaces")
    for pane, expected_component in SAFE_COMPONENTS.items():
        expected = {"component", "title", "objectType"} | ({"action"} if pane == "utility" else set())
        _expect_keys(surfaces[pane], expected, where=f"surface {pane}")
        surface = surfaces[pane]
        if surface["component"] != expected_component or surface["objectType"] not in schemas:
            raise PackageValidationError(f"surface {pane} is unsupported")
        if not isinstance(surface["title"], str) or not surface["title"].strip():
            raise PackageValidationError(f"surface {pane} title is invalid")
        if pane == "utility" and surface["action"] not in SAFE_ACTIONS:
            raise PackageValidationError("surface action is not allowed")

    declared = {"manifest.json", surfaces_ref, *domain_refs.values()}
    if migration_ref:
        declared.add(migration_ref)
    actual = {path.relative_to(root).as_posix() for path in entries}
    if actual != declared:
        raise PackageValidationError("package contains undeclared or missing files")
    return {
        "root": root.resolve(), "manifest": manifest, "surfaces": surfaces,
        "schemas": schemas, "migration": migration, "digest": _package_digest(root, entries),
    }


class WorkspacePackageRuntime:
    def __init__(self, database: Database, store_root: str | Path | None = None):
        self.db = database
        self.results = ResultStore(database)
        self.company_runtime = WorkspaceRuntime(database)
        self.shared_projection = SharedWorkspaceProjection(database)
        configured = store_root or os.getenv("CURIS_WORKSPACE_PACKAGE_STORE")
        self.store_root = Path(configured) if configured else Path(database.path).resolve().parent / "workspace-packages"
        self._migrate_instance_uniqueness()
        with self.db.connect() as connection:
            connection.executescript(PACKAGE_DDL)
        self._reconcile()

    def _migrate_instance_uniqueness(self) -> None:
        """Remove the legacy instance limit without changing IDs or child rows."""
        parent = "workspace_package_instances"
        children = ("workspace_package_objects", "workspace_package_activities",
                    "workspace_package_lifecycle_events", "workspace_package_migration_journal")
        def normalized(sql):
            # Ignore formatting outside string literals; changed CHECK/default values are unknown.
            parts = re.split(r"('(?:''|[^'])*')", sql.replace('"' + parent + '"', parent))
            return "".join(part if index % 2 else re.sub(r"\s+", "",
                re.sub(r"\bif\s+not\s+exists\b", "", part, flags=re.I).lower())
                for index, part in enumerate(parts)).rstrip(";")
        expected = {}
        for statement in PACKAGE_DDL.split(";"):
            match = re.search(r"create table if not exists (\w+)", statement)
            if match:
                expected[match[1]] = statement.strip()
        new_sql = expected[parent]
        old_sql = new_sql.replace("  foreign key(tenant_id, package_id, package_version)",
                                 "  unique(tenant_id, company_id, package_id, package_version),\n"
                                 "  foreign key(tenant_id, package_id, package_version)")
        with self.db.connect() as connection:
            original_fk = connection.execute("pragma foreign_keys").fetchone()[0]
            connection.execute("pragma foreign_keys = off")
            try:
                connection.execute("begin immediate")
                catalog = connection.execute("select type, name, tbl_name, sql from sqlite_master").fetchall()
                tables = {row["name"]: row["sql"] for row in catalog if row["type"] == "table"}
                if parent not in tables:
                    if any(child in tables for child in children):
                        raise PackageConflictError("instance migration: missing parent with existing children")
                    connection.commit()
                    return
                shape = normalized(tables[parent])
                if shape not in (normalized(old_sql), normalized(new_sql)):
                    raise PackageConflictError("instance migration: unknown parent schema")
                for child in children:
                    if child not in tables or normalized(tables[child]) != normalized(expected[child]):
                        raise PackageConflictError("instance migration: unknown child schema")
                if normalized(tables.get("installed_workspace_packages", "")) != normalized(expected["installed_workspace_packages"]):
                    raise PackageConflictError("instance migration: unknown definition schema")
                for row in catalog:
                    sql = row["sql"] or ""
                    if row["type"] in ("trigger", "view") and (
                        row["tbl_name"] in (parent, *children) or any(
                            re.search(r"\b" + dependency + r"\b", sql, re.I) for dependency in (parent, *children))
                    ):
                        raise PackageConflictError("instance migration: unknown trigger or view dependency")
                    if row["type"] == "index" and row["tbl_name"] == parent and sql:
                        raise PackageConflictError("instance migration: unknown parent index")
                for table in tables:
                    quoted = '"' + table.replace('"', '""') + '"'
                    references = connection.execute(f"pragma foreign_key_list({quoted})").fetchall()
                    for reference in references:
                        if reference["table"] == parent and (
                            table not in children or reference["from"] != "instance_id"
                            or reference["to"] != "instance_id" or reference["on_delete"] != "NO ACTION"
                            or reference["on_update"] != "NO ACTION"
                        ):
                            raise PackageConflictError("instance migration: unknown inbound dependency")
                if shape == normalized(new_sql):
                    connection.commit()
                    return
                tracked = (parent, *children)
                if any(connection.execute(f'pragma foreign_key_check("{table}")').fetchall() for table in tracked):
                    raise PackageConflictError("instance migration: pre-existing orphan")
                if [r[0] for r in connection.execute("pragma integrity_check")] != ["ok"]:
                    raise PackageConflictError("instance migration: database integrity failed")
                def snapshot():
                    return {table: tuple(tuple(row) for row in connection.execute(
                        f'select * from "{table}" order by 1')) for table in tracked}
                before = snapshot()
                replacement = "workspace_package_instances_uniqueness_migration"
                if replacement in tables:
                    raise PackageConflictError("instance migration: replacement table already exists")
                connection.execute(new_sql.replace("create table if not exists " + parent,
                                                   "create table " + replacement, 1))
                columns = ",".join(row["name"] for row in connection.execute(f"pragma table_info({parent})"))
                connection.execute(f"insert into {replacement} ({columns}) select {columns} from {parent}")
                copied = tuple(tuple(row) for row in connection.execute(f"select * from {replacement} order by 1"))
                if copied != before[parent]:
                    raise PackageConflictError("instance migration: parent copy differs")
                connection.execute(f"drop table {parent}")
                connection.execute(f"alter table {replacement} rename to {parent}")
                if snapshot() != before or any(connection.execute(f'pragma foreign_key_check("{table}")').fetchall() for table in tracked):
                    raise PackageConflictError("instance migration: values or references changed")
                if [r[0] for r in connection.execute("pragma integrity_check")] != ["ok"]:
                    raise PackageConflictError("instance migration: post-copy integrity failed")
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                connection.execute(f"pragma foreign_keys = {int(original_fk)}")
                if connection.execute("pragma foreign_keys").fetchone()[0] != original_fk:
                    raise PackageConflictError("instance migration: foreign key setting not restored")

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def _reconcile(self) -> None:
        staging = self.store_root / ".staging"
        if staging.exists():
            for path in staging.iterdir():
                shutil.rmtree(path) if path.is_dir() else path.unlink()
        orphaned_targets: list[Path] = []
        with self.db.connect() as connection:
            rows = connection.execute(
                "select package_id, version, stored_path from installed_workspace_packages where tenant_id = ? and status = 'ACTIVE'",
                (self.tenant_id,),
            ).fetchall()
            for row in rows:
                if Path(row["stored_path"]).is_dir():
                    continue
                connection.execute(
                    "update installed_workspace_packages set status = 'BROKEN' where tenant_id = ? and package_id = ? and version = ?",
                    (self.tenant_id, row["package_id"], row["version"]),
                )
                connection.execute(
                    "update workspace_package_instances set status = 'DISABLED', updated_at = ? where tenant_id = ? and package_id = ? and package_version = ?",
                    (_now(), self.tenant_id, row["package_id"], row["version"]),
                )
            prepared = connection.execute(
                "select * from workspace_package_migration_journal where tenant_id = ? and status = 'PREPARED'",
                (self.tenant_id,),
            ).fetchall()
            for attempt in prepared:
                current = connection.execute(
                    "select package_version, package_digest from workspace_package_instances "
                    "where tenant_id = ? and instance_id = ?",
                    (self.tenant_id, attempt["instance_id"]),
                ).fetchone()
                old_pin = bool(
                    current
                    and current["package_version"] == attempt["from_version"]
                    and current["package_digest"] == attempt["from_digest"]
                )
                connection.execute(
                    "update workspace_package_migration_journal set status = 'FAILED', error_code = ?, updated_at = ? "
                    "where migration_id = ? and status = 'PREPARED'",
                    (
                        "INTERRUPTED_BEFORE_ATOMIC_COMMIT" if old_pin else "PIN_CHANGED_OUTSIDE_MIGRATION",
                        _now(), attempt["migration_id"],
                    ),
                )
                referenced = connection.execute(
                    "select 1 from installed_workspace_packages where tenant_id = ? and package_id = ? "
                    "and version = ? and digest = ?",
                    (
                        self.tenant_id, attempt["package_id"], attempt["to_version"],
                        attempt["to_digest"],
                    ),
                ).fetchone()
                if old_pin and not referenced:
                    orphaned_targets.append(Path(attempt["target_path"]))
        for target in orphaned_targets:
            if target.is_dir():
                shutil.rmtree(target)
                for parent in (target.parent, target.parent.parent):
                    if parent != self.store_root and parent.is_dir() and not any(parent.iterdir()):
                        parent.rmdir()

    def _require_company(self, connection, company_id: str) -> None:
        row = connection.execute(
            "select 1 from companies where tenant_id = ? and company_id = ?",
            (self.tenant_id, company_id),
        ).fetchone()
        if row is None:
            raise PackageScopeError("company does not belong to current tenant")

    def _write_install(self, connection, package, target, company_id, *, department_id,
                       business_id, business_name, business_goal, business_positioning,
                       workspace_id, instance_id, at, blueprint, insert_definition=True, workspace_name=""):
        """Same Package install writes; the caller owns the canonical confirmation transaction."""
        manifest = package["manifest"]
        package_id, version, digest = manifest["packageId"], manifest["version"], package["digest"]
        self._require_company(connection, company_id)
        department = connection.execute(
            "select 1 from department_instances where tenant_id=? and company_id=? and id=? "
            "and deleted_at is null and status != 'archived'",
            (self.tenant_id, company_id, department_id),
        ).fetchone()
        if department is None:
            raise PackageScopeError("department does not belong to current company")
        connection.execute(
            "insert into canonical_businesses(business_id, tenant_id, company_id, department_id, name, "
            "lifecycle_status, goal, positioning, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, 'DRAFT', ?, ?, ?, ?)",
            (business_id, self.tenant_id, company_id, department_id, business_name.strip(),
             business_goal.strip(), business_positioning.strip(), at, at),
        )
        if insert_definition:
            connection.execute(
                "insert into installed_workspace_packages values (?, ?, ?, ?, 'ACTIVE', ?, ?, ?, ?, ?, ?, null, null)",
                (
                    self.tenant_id, package_id, version, digest,
                    json.dumps(manifest, ensure_ascii=False),
                    json.dumps(package["surfaces"], ensure_ascii=False),
                    json.dumps(package["schemas"], ensure_ascii=False),
                    str(package["root"]), str(target), at,
                ),
            )
        connection.execute(
            "insert into workspaces(workspace_id, tenant_id, company_id, business_id, name, blueprint_json, "
            "blueprint_version, operating_version, status, simulation_passed, business_relation_status, "
            "business_relation_reason, business_relation_owner, business_relation_source, "
            "business_relation_checked_at, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, ?, ?, 0, 'DRAFT', 0, 'RESOLVED', '', 'Workspace Package Runtime', "
            "'CANONICAL_PACKAGE_INSTALL', ?, ?, ?)",
            (workspace_id, self.tenant_id, company_id, business_id, workspace_name or manifest["workspace"]["name"],
             json.dumps(blueprint), version, at, at, at),
        )
        connection.execute(
            "insert into runtime_workspace_versions(version_id, tenant_id, company_id, workspace_id, blueprint_version, status, simulation_passed, operating_version, change_kind, data_json, created_at, updated_at) values (?, ?, ?, ?, ?, 'DRAFT', 0, 0, 'PACKAGE_INSTALL', ?, ?, ?)",
            (f"workspace-package-version-{uuid4()}", self.tenant_id, company_id, workspace_id, version, json.dumps(blueprint), at, at),
        )
        connection.execute(
            "insert into workspace_package_instances values (?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)",
            (instance_id, self.tenant_id, company_id, workspace_id, package_id, version, digest, at, at),
        )

    def prepare_confirmed_assets(self, source):
        """Publish only fully verified assets; never replace another producer's target."""
        package = validate_package(source)
        manifest = package["manifest"]
        target = self.store_root / manifest["packageId"] / manifest["version"] / package["digest"]
        target.parent.mkdir(parents=True, exist_ok=True)
        def verify_target():
            if target.is_symlink() or validate_package(target)["digest"] != package["digest"]:
                raise PackageConflictError("immutable installed asset does not match the definition")
        if target.exists() or target.is_symlink():
            verify_target()
            return package, target
        staging = target.with_name(f".{target.name}.{uuid4()}.staging")
        staging.mkdir()
        owned = staging.stat(follow_symlinks=False)
        try:
            shutil.copytree(package["root"], staging, dirs_exist_ok=True)
            if validate_package(staging)["digest"] != package["digest"]:
                raise PackageConflictError("prepared immutable asset does not match the definition")
            try:
                if os.name == "nt":
                    os.rename(staging, target)  # Windows rename refuses an existing destination.
                else:
                    libc = ctypes.CDLL(None, use_errno=True)
                    if sys.platform == "darwin":
                        rename = libc.renamex_np
                        rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
                        rename.restype = ctypes.c_int
                        result = rename(os.fsencode(staging), os.fsencode(target), 0x4)  # RENAME_EXCL
                    elif sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
                        rename = libc.renameat2
                        rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
                        rename.restype = ctypes.c_int
                        result = rename(-100, os.fsencode(staging), -100, os.fsencode(target), 1)  # RENAME_NOREPLACE
                    else:
                        raise PackageConflictError("atomic no-replace asset publication is unavailable")
                    if result:
                        error = ctypes.get_errno()
                        raise OSError(error, os.strerror(error), str(target))
            except OSError as error:
                if error.errno not in {errno.EEXIST, errno.ENOTEMPTY}:
                    raise
                verify_target()
            return package, target
        finally:
            try:
                current = staging.stat(follow_symlinks=False)
            except FileNotFoundError:
                current = None
            if current and not staging.is_symlink() and (current.st_dev, current.st_ino) == (owned.st_dev, owned.st_ino):
                shutil.rmtree(staging)

    def install_confirmed_in_connection(self, connection, package, target, company_id, *,
            department_id, business_id, business_name, business_goal, business_positioning,
            workspace_id, workspace_name):
        """One confirmation creates one Business/Workspace; the same package may serve other Businesses."""
        manifest = package["manifest"]
        package_id, version, digest = manifest["packageId"], manifest["version"], package["digest"]
        existing = connection.execute(
            "select digest,status from installed_workspace_packages where tenant_id=? and package_id=? and version=?",
            (self.tenant_id, package_id, version)).fetchone()
        if existing and (existing["digest"] != digest or existing["status"] != "ACTIVE"):
            raise PackageConflictError("the exact definition is no longer available for activation")
        at = _now()
        blueprint = {"businessType": "PACKAGE", "packageId": package_id, "packageVersion": version,
                     "packageDigest": digest, "surfaceContract": manifest["schemaVersion"]}
        self._write_install(connection, package, target, company_id, department_id=department_id,
            business_id=business_id, business_name=business_name, business_goal=business_goal,
            business_positioning=business_positioning, workspace_id=workspace_id, workspace_name=workspace_name,
            instance_id="workspace-package-instance-" + str(uuid4()), at=at, blueprint=blueprint,
            insert_definition=not bool(existing))

    def install(
        self,
        source: str | Path,
        company_id: str,
        *,
        department_id: str,
        business_id: str,
        business_name: str,
        business_goal: str = "",
        business_positioning: str = "",
    ) -> dict:
        if not business_id.strip() or not business_name.strip():
            raise PackageValidationError("canonical business identity and name are required")
        package = validate_package(source)
        manifest = package["manifest"]
        package_id, version, digest = manifest["packageId"], manifest["version"], package["digest"]
        target = self.store_root / package_id / version / digest
        staging = self.store_root / ".staging" / f"install-{uuid4()}"
        with self.db.connect() as connection:
            self._require_company(connection, company_id)
            existing = connection.execute(
                "select * from installed_workspace_packages where tenant_id = ? and package_id = ? and version = ?",
                (self.tenant_id, package_id, version),
            ).fetchone()
            if existing:
                if existing["digest"] != digest:
                    raise PackageConflictError("package version already exists with another digest")
                instances = connection.execute(
                    "select i.workspace_id, w.business_id from workspace_package_instances i join workspaces w on w.workspace_id=i.workspace_id and w.tenant_id=i.tenant_id and w.company_id=i.company_id where i.tenant_id = ? and i.company_id = ? and i.package_id = ? and i.package_version = ? and i.status = 'ACTIVE'",
                    (self.tenant_id, company_id, package_id, version),
                ).fetchall()
                if len(instances) > 1:
                    matches = [row for row in instances if row["business_id"] == business_id]
                    if len(matches) != 1:
                        raise PackageConflictError("multiple package instances require an unambiguous existing business identity")
                    instance = matches[0]
                else:
                    instance = instances[0] if instances else None
                    if instance and instance["business_id"] != business_id:
                        raise PackageConflictError("existing Package instance belongs to a different Business")
                if existing["status"] == "ACTIVE" and instance:
                    return self.get_workspace(instance["workspace_id"])
                raise PackageConflictError("P0 does not reinstall, update or roll back a package")

        staging.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package["root"], staging)
        target.parent.mkdir(parents=True, exist_ok=True)
        workspace_id = f"workspace-package-{uuid4()}"
        instance_id = f"workspace-package-instance-{uuid4()}"
        at = _now()
        blueprint = {
            "businessType": "PACKAGE",
            "packageId": package_id,
            "packageVersion": version,
            "packageDigest": digest,
            "surfaceContract": manifest["schemaVersion"],
        }
        moved = False
        try:
            with self.db.connect() as connection:
                connection.execute("begin immediate")
                self._write_install(connection, package, target, company_id,
                    department_id=department_id, business_id=business_id, business_name=business_name,
                    business_goal=business_goal, business_positioning=business_positioning,
                    workspace_id=workspace_id, instance_id=instance_id, at=at, blueprint=blueprint)
                from .employee_templates import EmployeeTemplateContract, professional_team_contract, PROFESSIONAL_TEAM_PACKAGES
                if (package_id, version) in PROFESSIONAL_TEAM_PACKAGES:
                    identity = TenantContext.current_identity()
                    company = connection.execute("select ceo_id,status from companies where tenant_id=? and company_id=?", (self.tenant_id, company_id)).fetchone()
                    if identity.get("role") not in {"owner", "ceo", "test"} or identity.get("ceo_id") != company[0] or company[1] not in {"draft", "active"} or identity.get("company_id") and identity["company_id"] != company_id:
                        raise PackageScopeError("Professional initial team requires the current Company's CEO")
                    contract = professional_team_contract(package_id, version, digest)
                    try:
                        EmployeeTemplateContract(self.db).materialize_professional_team_in_connection(connection,
                            company_id=company_id, business_id=business_id, workspace_id=workspace_id, contract=contract)
                    except ValueError as error:
                        raise PackageConflictError(str(error)) from error
                os.replace(staging, target)
                moved = True
        except Exception:
            if moved and target.exists():
                shutil.rmtree(target)
            elif staging.exists():
                shutil.rmtree(staging)
            raise
        return self.get_workspace(workspace_id)

    @staticmethod
    def _rows(connection, sql: str, params: tuple[object, ...]) -> list[dict]:
        return [dict(row) for row in connection.execute(sql, params).fetchall()]

    def complete_professional_team(self, workspace_id, *, company_id, ceo_id, request_id, expected):
        from .employee_templates import EmployeeTemplateContract, professional_team_contract
        from .resource_scope_policy import ResourceScopePolicy
        from .tenant_context import TenantContext
        identity = TenantContext.current_identity()
        if identity.get("role") not in {"owner", "ceo", "test"} or identity.get("ceo_id") != ceo_id:
            raise PackageScopeError("Only the current CEO can complete an initial team")
        if identity.get("company_id") and identity["company_id"] != company_id:
            raise PackageScopeError("Team Company differs from current identity")
        if not isinstance(request_id, str) or not 1 <= len(request_id.strip()) <= 128:
            raise PackageValidationError("Explicit original team request is required")
        encoded = json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        fingerprint = hashlib.sha256(encoded.encode()).hexdigest()
        key = "professional-team:" + hashlib.sha256(json.dumps([self.tenant_id, company_id, workspace_id, request_id]).encode()).hexdigest()
        with self.db.connect() as con:
            con.execute("begin immediate")
            owner = con.execute("select ceo_id,status from companies where tenant_id=? and company_id=?", (self.tenant_id, company_id)).fetchone()
            if owner is None or owner[0] != ceo_id or owner[1] not in {"draft", "active"}:
                raise PackageScopeError("Current CEO does not own a configurable Company")
            instance = self._instance(con, workspace_id)
            if instance["company_id"] != company_id:
                raise PackageScopeError("Team Workspace is outside Company")
            try:
                scope = ResourceScopePolicy.resolve_execution_scope(con, tenant_id=self.tenant_id, company_id=company_id, scope_type="WORKSPACE", scope_ref=workspace_id)
            except ValueError as error:
                raise PackageScopeError(str(error)) from error
            definition = con.execute("select digest from installed_workspace_packages where tenant_id=? and package_id=? and version=? and status='ACTIVE'", (self.tenant_id, instance["package_id"], instance["package_version"])).fetchone()
            if definition is None or definition[0] != instance["package_digest"]:
                raise PackageConflictError("Installed definition differs from the instance Package")
            department = con.execute("select 1 from department_instances where tenant_id=? and company_id=? and id=? and enabled=1 and deleted_at is null and status!='archived'",
                (self.tenant_id, company_id, scope["department_id"])).fetchone()
            workspace = con.execute("select status,blueprint_version,blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                (self.tenant_id, company_id, workspace_id)).fetchone()
            if not department or workspace[0] in {"ARCHIVED", "DISABLED"}:
                raise PackageScopeError("Team Workspace or department is unavailable")
            actual = {"business_id": scope["business_id"], "package_id": instance["package_id"], "version": instance["package_version"], "digest": instance["package_digest"]}
            blueprint = json.loads(workspace[2])
            if workspace[1] != actual["version"] or any(blueprint.get(k) != v for k, v in [("packageId",actual["package_id"]),("packageVersion",actual["version"]),("packageDigest",actual["digest"])]):
                raise PackageConflictError("Workspace blueprint differs from the current Package")
            if not isinstance(expected, dict) or set(expected) != set(actual) | {"assignments"} or any(expected[k] != v for k, v in actual.items()):
                raise PackageConflictError("Original team scope or Package changed")
            try:
                contract = professional_team_contract(actual["package_id"], actual["version"], actual["digest"])
                if contract is None: raise ValueError("Package has no approved initial team")
                service = EmployeeTemplateContract(self.db)
                state = service.professional_team_state_in_connection(con, company_id=company_id, business_id=scope["business_id"], workspace_id=workspace_id, contract=contract)
            except ValueError as error:
                raise PackageConflictError(str(error)) from error
            old = con.execute("select event_type,payload from evolution_events where tenant_id=? and idempotency_key=?", (self.tenant_id, key)).fetchall()
            if old:
                if len(old) != 1 or old[0][0] != "professional.initial_team.completed":
                    raise PackageConflictError("Team receipt identity is ambiguous")
                payload = json.loads(old[0][1])
                if payload["fingerprint"] != fingerprint or payload["scope"] != scope or payload["actor"] != ceo_id:
                    raise PackageConflictError("Original team request cannot change its scope or basis")
                return {"receipt": payload["result"], "current_team": state["team"]}
            if expected["assignments"] != state["basis"]:
                raise PackageConflictError("Current team arrangements changed; read them before confirming")
            try:
                result = state["team"] or service.materialize_professional_team_in_connection(con,
                    company_id=company_id, business_id=scope["business_id"], workspace_id=workspace_id, contract=contract)
            except ValueError as error:
                raise PackageConflictError(str(error)) from error
            payload = {"scope": scope, "actor": ceo_id, "request_id": request_id, "contract_sha256": contract["sha256"], "package_identity": actual, "fingerprint": fingerprint, "inputs": expected, "result": result}
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'professional.initial_team.completed',?,?)",
                (self.tenant_id, workspace_id, json.dumps(payload, ensure_ascii=False), key))
            current = service.professional_team_state_in_connection(con, company_id=company_id, business_id=scope["business_id"], workspace_id=workspace_id, contract=contract)
            return {"receipt": result, "current_team": current["team"]}

    def _continuity_snapshot(self, connection, instance) -> dict[str, str]:
        workspace = connection.execute(
            "select tenant_id, company_id, business_id, workspace_id from workspaces "
            "where tenant_id = ? and company_id = ? and workspace_id = ?",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        ).fetchone()
        if workspace is None:
            raise PackageValidationError("Workspace identity does not resolve")
        identity = {
            "tenant_id": self.tenant_id,
            "company_id": instance["company_id"],
            "business_id": workspace["business_id"],
            "workspace_id": instance["workspace_id"],
            "instance_id": instance["instance_id"],
        }
        data_rows = self._rows(
            connection,
            "select * from workspace_package_objects where tenant_id = ? and company_id = ? "
            "and workspace_id = ? order by object_id",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        )
        company_rows: list[dict] = []
        for table, sql, params in (
            (
                "runtime_entities",
                "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? order by entity_id",
                (self.tenant_id, instance["company_id"], instance["workspace_id"]),
            ),
            (
                "runtime_links",
                "select * from runtime_links where tenant_id = ? and company_id = ? and workspace_id = ? order by link_id",
                (self.tenant_id, instance["company_id"], instance["workspace_id"]),
            ),
            (
                "tasks",
                "select * from tasks where tenant_id = ? and company_id = ? order by task_id",
                (self.tenant_id, instance["company_id"]),
            ),
            (
                "executions",
                "select e.* from executions e join tasks t on t.task_id = e.task_id "
                "where e.tenant_id = ? and t.tenant_id = ? and t.company_id = ? order by e.execution_id",
                (self.tenant_id, self.tenant_id, instance["company_id"]),
            ),
            (
                "artifacts",
                "select a.* from artifacts a join tasks t on t.task_id = a.task_id "
                "where a.tenant_id = ? and t.tenant_id = ? and t.company_id = ? order by a.artifact_id",
                (self.tenant_id, self.tenant_id, instance["company_id"]),
            ),
        ):
            company_rows.extend({"table": table, "row": row} for row in self._rows(connection, sql, params))
        return {
            "identity": _fingerprint([identity]),
            "data": _fingerprint(data_rows),
            "company_os": _fingerprint(company_rows),
        }

    def _protected_migration_snapshot(self, connection, instance) -> dict[str, str]:
        workspace = connection.execute(
            "select tenant_id, company_id, business_id, workspace_id from workspaces "
            "where tenant_id = ? and company_id = ? and workspace_id = ?",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        ).fetchone()
        if workspace is None:
            raise PackageValidationError("Workspace identity does not resolve")
        identity = dict(workspace) | {"instance_id": instance["instance_id"]}
        objects = self._rows(
            connection,
            "select object_id, instance_id, tenant_id, company_id, workspace_id, object_type, "
            "lifecycle_status, owner_ref, created_at from workspace_package_objects "
            "where tenant_id = ? and company_id = ? and workspace_id = ? order by object_id",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        )
        company_rows: list[dict] = []
        entities = self._rows(
            connection,
            "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? "
            "order by entity_id",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        )
        for entity in entities:
            if entity["entity_type"] == "PACKAGE_DOMAIN_OBJECT":
                entity = {
                    key: value for key, value in entity.items()
                    if key not in {"data_json", "blueprint_version", "updated_at"}
                }
            company_rows.append({"table": "runtime_entities", "row": entity})
        for table, sql, params in (
            (
                "runtime_links",
                "select * from runtime_links where tenant_id = ? and company_id = ? and workspace_id = ? order by link_id",
                (self.tenant_id, instance["company_id"], instance["workspace_id"]),
            ),
            (
                "tasks",
                "select * from tasks where tenant_id = ? and company_id = ? order by task_id",
                (self.tenant_id, instance["company_id"]),
            ),
            (
                "executions",
                "select e.* from executions e join tasks t on t.task_id = e.task_id "
                "where e.tenant_id = ? and t.tenant_id = ? and t.company_id = ? order by e.execution_id",
                (self.tenant_id, self.tenant_id, instance["company_id"]),
            ),
            (
                "artifacts",
                "select a.* from artifacts a join tasks t on t.task_id = a.task_id "
                "where a.tenant_id = ? and t.tenant_id = ? and t.company_id = ? order by a.artifact_id",
                (self.tenant_id, self.tenant_id, instance["company_id"]),
            ),
        ):
            company_rows.extend({"table": table, "row": row} for row in self._rows(connection, sql, params))
        return {
            "identity": _fingerprint([identity]),
            "objects": _fingerprint(objects),
            "company_os": _fingerprint(company_rows),
        }

    @staticmethod
    def _assert_data_matches_schema(schema: dict, values: dict) -> None:
        if not isinstance(values, dict) or set(values) - set(schema["properties"]):
            raise PackageValidationError("migrated object contains unknown fields")
        for name, field in schema["properties"].items():
            value = values.get(name)
            if (
                name in schema["required"]
                and name not in CORE_REFERENCE_FIELDS
                and (not isinstance(value, str) or not value.strip())
            ):
                raise PackageValidationError(f"migrated object field is required: {name}")
            if value is None:
                continue
            if not isinstance(value, str):
                raise PackageValidationError(f"migrated object field must be a string: {name}")
            if len(value) > field.get("maxLength", 20000):
                raise PackageValidationError(f"migrated object field is too long: {name}")
            if field.get("enum") and value not in field["enum"]:
                raise PackageValidationError(f"migrated object enum is invalid: {name}")

    def _migration_preflight(self, connection, current, package: dict, *, direction: str) -> dict:
        migration = package["migration"]
        if migration is None or not migration["reversible"]:
            raise PackageValidationError("IRREVERSIBLE_MIGRATION_NOT_SUPPORTED")
        target_schemas = package["schemas"]
        rows = self._rows(
            connection,
            "select * from workspace_package_objects where tenant_id = ? and company_id = ? "
            "and workspace_id = ? order by object_id",
            (self.tenant_id, current["company_id"], current["workspace_id"]),
        )
        affected = [row for row in rows if row["object_type"] in migration["objects"]]
        checkpoint = {"objects": [], "projections": []}
        transformed: list[dict] = []
        for row in affected:
            plan = migration["objects"][row["object_type"]]
            expected_from = plan["fromSchemaVersion"] if direction == "up" else plan["toSchemaVersion"]
            target_schema = target_schemas[row["object_type"]]
            if row["schema_version"] != expected_from:
                raise PackageValidationError("persisted object schema version does not match migration")
            data = json.loads(row["data_json"])
            migrated = _data_after_renames(data, plan[direction])
            self._assert_data_matches_schema(target_schema, migrated)
            projection_row = connection.execute(
                "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? "
                "and entity_id = ? and entity_type = 'PACKAGE_DOMAIN_OBJECT'",
                (self.tenant_id, current["company_id"], current["workspace_id"], row["object_id"]),
            ).fetchone()
            if projection_row is None:
                raise PackageValidationError("Package object Core projection does not resolve")
            projection = dict(projection_row)
            projection_data = json.loads(projection["data_json"])
            if projection_data.get("businessData") != data:
                raise PackageValidationError("Package object and Core projection data diverged")
            checkpoint["objects"].append({
                "objectId": row["object_id"], "objectType": row["object_type"],
                "schemaVersion": row["schema_version"], "data": data,
            })
            checkpoint["projections"].append({
                "entityId": row["object_id"], "blueprintVersion": projection["blueprint_version"],
                "data": projection_data,
            })
            transformed.append({
                "objectId": row["object_id"], "objectType": row["object_type"],
                "schemaVersion": target_schema["schemaVersion"], "data": migrated,
                "projection": projection_data,
            })
        return {
            "affected": transformed,
            "checkpoint": checkpoint,
            "checkpointDigest": _fingerprint([checkpoint]),
            "dataFingerprintBefore": _fingerprint(rows),
        }

    @staticmethod
    def _migration_schema_reasons(current, package: dict) -> list[str]:
        current_schemas = json.loads(current["schemas_json"])
        target_schemas = package["schemas"]
        migration = package["migration"]
        changed = {
            object_type for object_type in set(current_schemas) | set(target_schemas)
            if current_schemas.get(object_type) != target_schemas.get(object_type)
        }
        if not changed:
            return ["MIGRATION_NOT_REQUIRED"] if migration else []
        if migration is None:
            return ["MIGRATION_REQUIRED_NOT_SUPPORTED", "MIGRATION_MANIFEST_REQUIRED"]
        reasons: list[str] = []
        if migration["fromVersion"] != current["package_version"]:
            reasons.append("MIGRATION_FROM_VERSION_MISMATCH")
        if migration["toVersion"] != package["manifest"]["version"]:
            reasons.append("MIGRATION_TO_VERSION_MISMATCH")
        if not migration["reversible"]:
            reasons.append("IRREVERSIBLE_MIGRATION_NOT_SUPPORTED")
        if set(migration["objects"]) != changed:
            reasons.append("MIGRATION_OBJECT_SET_MISMATCH")
            return reasons
        for object_type, plan in migration["objects"].items():
            source = current_schemas.get(object_type)
            target = target_schemas.get(object_type)
            if source is None or target is None:
                reasons.append("MIGRATION_OBJECT_TYPE_MISMATCH")
                continue
            if source["schemaVersion"] != plan["fromSchemaVersion"]:
                reasons.append("MIGRATION_FROM_SCHEMA_VERSION_MISMATCH")
            try:
                transformed = _schema_after_renames(source, plan, direction="up")
            except PackageValidationError:
                reasons.append("MIGRATION_SCHEMA_RENAME_INVALID")
            else:
                if transformed != target:
                    reasons.append("MIGRATION_SCHEMA_CHANGE_EXCEEDS_DECLARATION")
        return list(dict.fromkeys(reasons))

    @staticmethod
    def _v2_surface_impact_reasons(current, package: dict) -> list[str]:
        current_manifest = json.loads(current["manifest_json"])
        if current_manifest.get("schemaVersion") != PACKAGE_SCHEMA_V2:
            return []
        current_model = json.loads(current["surfaces_json"])
        target_model = package["surfaces"]
        current_surfaces = {item["key"]: item for item in current_model["surfaces"]}
        target_surfaces = {item["key"]: item for item in target_model["surfaces"]}
        if set(current_surfaces) - set(target_surfaces):
            return ["SURFACE_REMOVAL_REQUIRES_EXPLICIT_MIGRATION"]
        reasons = []
        protected = {
            "navigationRefs", "defaultEligible", "objectTypes", "primaryViewRef",
            "responsibilityRequirementRefs", "capabilityRequirementRefs", "projectionRefs",
            "detailViewRef", "utilityViewRef", "availability",
        }
        for key, current_surface in current_surfaces.items():
            target_surface = target_surfaces[key]
            if any(current_surface[field] != target_surface[field] for field in protected):
                reasons.append("SURFACE_SEMANTIC_CHANGE_REQUIRES_EXPLICIT_MIGRATION")
            if not set(current_surface["viewRefs"]).issubset(target_surface["viewRefs"]):
                reasons.append("SURFACE_VIEW_REMOVAL_REQUIRES_EXPLICIT_MIGRATION")
        for key in set(target_surfaces) - set(current_surfaces):
            if target_surfaces[key]["availability"]["mode"] != "OPTIONAL":
                reasons.append("ADDED_NON_OPTIONAL_SURFACE_NOT_SUPPORTED")
        current_navigation = {item["key"]: item for item in current_model["domainNavigation"]}
        target_navigation = {item["key"]: item for item in target_model["domainNavigation"]}
        if set(current_navigation) - set(target_navigation):
            reasons.append("DOMAIN_NAVIGATION_REMOVAL_REQUIRES_EXPLICIT_MIGRATION")
        for key, current_item in current_navigation.items():
            if key not in target_navigation:
                continue
            target_item = target_navigation[key]
            if current_item["surfaceRef"] != target_item["surfaceRef"]:
                reasons.append("DOMAIN_NAVIGATION_RETARGET_REQUIRES_EXPLICIT_MIGRATION")
        if current_model["defaultSurfaceRef"] != target_model["defaultSurfaceRef"]:
            reasons.append("DEFAULT_SURFACE_CHANGE_REQUIRES_EXPLICIT_MIGRATION")
        return list(dict.fromkeys(reasons))

    @classmethod
    def _compatibility_report(cls, current, package: dict, *, require_newer: bool) -> dict:
        current_manifest = json.loads(current["manifest_json"])
        current_schemas = json.loads(current["schemas_json"])
        target_manifest = package["manifest"]
        reasons: list[str] = []
        if target_manifest["packageId"] != current["package_id"]:
            reasons.append("PACKAGE_ID_MISMATCH")
        if target_manifest["coreCompatibility"] != current_manifest["coreCompatibility"]:
            reasons.append("CORE_COMPATIBILITY_MISMATCH")
        if target_manifest.get("schemaVersion") != current_manifest.get("schemaVersion"):
            reasons.append("PACKAGE_CONTRACT_TRANSITION_NOT_SUPPORTED")
        if require_newer and _version_tuple(target_manifest["version"]) <= _version_tuple(current["package_version"]):
            reasons.append("TARGET_VERSION_MUST_BE_NEWER")
        reasons.extend(cls._migration_schema_reasons(current, package))
        for field in ("actions", "capabilityRequirements", "retention"):
            if target_manifest[field] != current_manifest[field]:
                reasons.append(f"{field.upper()}_CHANGE_NOT_SUPPORTED")
        reasons.extend(cls._v2_surface_impact_reasons(current, package))
        schema_changed = package["schemas"] != current_schemas
        return {
            "compatible": not reasons,
            "compatibilityMode": (
                "DECLARED_PACKAGE_DATA_MIGRATION" if schema_changed else "EXACT_SCHEMA_STABLE"
            ),
            "migrationMode": (
                "DECLARATIVE_RENAME_FIELDS_V1" if schema_changed and package["migration"]
                else "NONE_SCHEMA_IDENTICAL" if not schema_changed
                else "MIGRATION_REQUIRED_NOT_SUPPORTED"
            ),
            "current": {
                "packageId": current["package_id"],
                "version": current["package_version"],
                "digest": current["package_digest"],
            },
            "target": {
                "packageId": target_manifest["packageId"],
                "version": target_manifest["version"],
                "digest": package["digest"],
            },
            "preserves": [
                "company_id", "business_id", "workspace_id", "instance_id",
                "object_id", "company_os_entities", "company_os_links",
            ],
            "reasons": reasons,
        }

    def preview_update(self, workspace_id: str, source: str | Path) -> dict:
        package = validate_package(source)
        with self.db.connect() as connection:
            current = self._instance(connection, workspace_id)
            report = self._compatibility_report(current, package, require_newer=True)
            report["continuity"] = self._continuity_snapshot(connection, current)
            if report["compatible"] and report["migrationMode"] == "DECLARATIVE_RENAME_FIELDS_V1":
                preflight = self._migration_preflight(connection, current, package, direction="up")
                report["migration"] = {
                    "reversible": True,
                    "affectedObjects": len(preflight["affected"]),
                    "checkpointDigest": preflight["checkpointDigest"],
                    "dataFingerprintBefore": preflight["dataFingerprintBefore"],
                }
            return report

    def _store_package(self, package: dict) -> tuple[Path, bool]:
        manifest = package["manifest"]
        target = self.store_root / manifest["packageId"] / manifest["version"] / package["digest"]
        if target.exists():
            if validate_package(target)["digest"] != package["digest"]:
                raise PackageConflictError("Package Store target digest is invalid")
            return target, False
        staging = self.store_root / ".staging" / f"lifecycle-{uuid4()}"
        staging.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package["root"], staging)
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staging, target)
        return target, True

    @staticmethod
    def _package_blueprint(workspace, package: dict) -> dict:
        blueprint = json.loads(workspace["blueprint_json"])
        blueprint.update({
            "packageId": package["manifest"]["packageId"],
            "packageVersion": package["manifest"]["version"],
            "packageDigest": package["digest"],
            "surfaceContract": package["manifest"]["schemaVersion"],
        })
        return blueprint

    def _record_lifecycle_event(
        self,
        connection,
        instance,
        *,
        action: str,
        report: dict,
        before: dict[str, str],
        after: dict[str, str],
        detail: dict,
        at: str,
    ) -> None:
        connection.execute(
            "insert into workspace_package_lifecycle_events values "
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                f"package-lifecycle-{uuid4()}", instance["instance_id"], self.tenant_id,
                instance["company_id"], instance["workspace_id"], instance["package_id"], action,
                report["current"]["version"], report["current"]["digest"],
                report["target"]["version"], report["target"]["digest"],
                report["compatibilityMode"], report["migrationMode"],
                before["data"], after["data"], before["company_os"], after["company_os"],
                json.dumps(detail, ensure_ascii=False), at,
            ),
        )

    def _prepare_migration(
        self,
        current,
        package: dict,
        report: dict,
        preflight: dict,
        target: Path,
        *,
        direction: str,
    ) -> str:
        migration_id = f"package-migration-{uuid4()}"
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            fresh = self._instance(connection, current["workspace_id"])
            if (
                fresh["package_version"] != report["current"]["version"]
                or fresh["package_digest"] != report["current"]["digest"]
            ):
                raise PackageConflictError("Workspace package pin changed before migration prepare")
            protected = self._protected_migration_snapshot(connection, fresh)
            connection.execute(
                "insert into workspace_package_migration_journal "
                "(migration_id, instance_id, tenant_id, company_id, workspace_id, package_id, direction, status, "
                "from_version, from_digest, to_version, to_digest, reversible, affected_count, target_path, "
                "migration_json, checkpoint_json, data_fingerprint_before, protected_fingerprint_before, "
                "created_at, updated_at) values (?, ?, ?, ?, ?, ?, ?, 'PREPARED', ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    migration_id, fresh["instance_id"], self.tenant_id, fresh["company_id"],
                    fresh["workspace_id"], fresh["package_id"], direction,
                    report["current"]["version"], report["current"]["digest"],
                    report["target"]["version"], report["target"]["digest"],
                    len(preflight["affected"]), str(target),
                    json.dumps(package["migration"], ensure_ascii=False),
                    json.dumps(preflight["checkpoint"], ensure_ascii=False),
                    preflight["dataFingerprintBefore"], _fingerprint([protected]), at, at,
                ),
            )
        return migration_id

    def _mark_migration_failed(self, migration_id: str, error: Exception) -> None:
        with self.db.connect() as connection:
            connection.execute(
                "update workspace_package_migration_journal set status = 'FAILED', error_code = ?, updated_at = ? "
                "where tenant_id = ? and migration_id = ? and status = 'PREPARED'",
                (type(error).__name__, _now(), self.tenant_id, migration_id),
            )

    def _remove_unreferenced_target(self, target: Path, package: dict) -> None:
        with self.db.connect() as connection:
            referenced = connection.execute(
                "select 1 from installed_workspace_packages where tenant_id = ? and package_id = ? "
                "and version = ? and digest = ?",
                (
                    self.tenant_id, package["manifest"]["packageId"], package["manifest"]["version"],
                    package["digest"],
                ),
            ).fetchone()
        if not referenced and target.is_dir():
            shutil.rmtree(target)
            for parent in (target.parent, target.parent.parent):
                if parent != self.store_root and parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()

    def _apply_object_migration(
        self,
        connection,
        current,
        package: dict,
        preflight: dict,
        *,
        direction: str,
        at: str,
    ) -> None:
        for item in preflight["affected"]:
            plan = package["migration"]["objects"][item["objectType"]]
            projection = dict(item["projection"])
            projection.update({
                "packageVersion": package["manifest"]["version"],
                "schemaVersion": item["schemaVersion"],
                "businessData": item["data"],
            })
            object_update = connection.execute(
                "update workspace_package_objects set schema_version = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and company_id = ? and workspace_id = ? and object_id = ? "
                "and schema_version = ?",
                (
                    item["schemaVersion"], json.dumps(item["data"], ensure_ascii=False), at,
                    self.tenant_id, current["company_id"], current["workspace_id"], item["objectId"],
                    plan["fromSchemaVersion"] if direction == "up" else plan["toSchemaVersion"],
                ),
            )
            projection_update = connection.execute(
                "update runtime_entities set blueprint_version = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and company_id = ? and workspace_id = ? and entity_id = ? "
                "and entity_type = 'PACKAGE_DOMAIN_OBJECT'",
                (
                    package["manifest"]["version"], json.dumps(projection, ensure_ascii=False), at,
                    self.tenant_id, current["company_id"], current["workspace_id"], item["objectId"],
                ),
            )
            if object_update.rowcount != 1 or projection_update.rowcount != 1:
                raise PackageConflictError("migration object changed during atomic apply")

    def _update_with_migration(self, workspace_id: str, package: dict, report: dict) -> dict:
        target, created_target = self._store_package(package)
        migration_id = ""
        try:
            with self.db.connect() as connection:
                current = self._instance(connection, workspace_id)
                report = self._compatibility_report(current, package, require_newer=True)
                if not report["compatible"] or report["migrationMode"] != "DECLARATIVE_RENAME_FIELDS_V1":
                    raise PackageValidationError(", ".join(report["reasons"]) or "migration is not compatible")
                preflight = self._migration_preflight(connection, current, package, direction="up")
            migration_id = self._prepare_migration(
                current, package, report, preflight, target, direction="UP",
            )
            at = _now()
            with self.db.connect() as connection:
                connection.execute("begin immediate")
                current = self._instance(connection, workspace_id)
                if (
                    current["package_version"] != report["current"]["version"]
                    or current["package_digest"] != report["current"]["digest"]
                ):
                    raise PackageConflictError("Workspace package pin changed during migration")
                report = self._compatibility_report(current, package, require_newer=True)
                if not report["compatible"] or report["migrationMode"] != "DECLARATIVE_RENAME_FIELDS_V1":
                    raise PackageValidationError(", ".join(report["reasons"]) or "migration is not compatible")
                preflight = self._migration_preflight(connection, current, package, direction="up")
                journal = connection.execute(
                    "select * from workspace_package_migration_journal where tenant_id = ? "
                    "and migration_id = ? and status = 'PREPARED'",
                    (self.tenant_id, migration_id),
                ).fetchone()
                if journal is None or _fingerprint([preflight["checkpoint"]]) != _fingerprint([
                    json.loads(journal["checkpoint_json"])
                ]):
                    raise PackageConflictError("migration checkpoint changed before atomic apply")
                protected_before = self._protected_migration_snapshot(connection, current)
                if _fingerprint([protected_before]) != journal["protected_fingerprint_before"]:
                    raise PackageConflictError("protected identity changed before migration")
                existing = connection.execute(
                    "select * from installed_workspace_packages where tenant_id = ? and package_id = ? and version = ?",
                    (self.tenant_id, current["package_id"], report["target"]["version"]),
                ).fetchone()
                if existing is None:
                    connection.execute(
                        "insert into installed_workspace_packages values (?, ?, ?, ?, 'ACTIVE', ?, ?, ?, ?, ?, ?, null, null)",
                        (
                            self.tenant_id, current["package_id"], report["target"]["version"],
                            report["target"]["digest"], json.dumps(package["manifest"], ensure_ascii=False),
                            json.dumps(package["surfaces"], ensure_ascii=False),
                            json.dumps(package["schemas"], ensure_ascii=False), str(package["root"]),
                            str(target), at,
                        ),
                    )
                elif existing["digest"] != report["target"]["digest"] or existing["status"] != "ACTIVE":
                    raise PackageConflictError("target package version conflicts with installed provenance")
                self._apply_object_migration(
                    connection, current, package, preflight, direction="up", at=at,
                )
                workspace = connection.execute(
                    "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (self.tenant_id, current["company_id"], workspace_id),
                ).fetchone()
                if workspace is None:
                    raise PackageValidationError("Workspace identity disappeared during migration")
                operating_version = int(workspace["operating_version"] or 0) + 1
                blueprint = self._package_blueprint(workspace, package)
                updated = connection.execute(
                    "update workspace_package_instances set package_version = ?, package_digest = ?, updated_at = ? "
                    "where tenant_id = ? and instance_id = ? and package_version = ? and package_digest = ?",
                    (
                        report["target"]["version"], report["target"]["digest"], at, self.tenant_id,
                        current["instance_id"], report["current"]["version"], report["current"]["digest"],
                    ),
                )
                if updated.rowcount != 1:
                    raise PackageConflictError("Workspace package migration lost its compare-and-swap")
                connection.execute(
                    "update workspaces set blueprint_json = ?, blueprint_version = ?, operating_version = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (
                        json.dumps(blueprint, ensure_ascii=False), report["target"]["version"], operating_version,
                        at, self.tenant_id, current["company_id"], workspace_id,
                    ),
                )
                connection.execute(
                    "update runtime_workspace_versions set status = 'SUPERSEDED', updated_at = ? "
                    "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                    (at, self.tenant_id, workspace_id, report["current"]["version"]),
                )
                connection.execute(
                    "insert into runtime_workspace_versions(version_id, tenant_id, company_id, workspace_id, "
                    "blueprint_version, status, simulation_passed, operating_version, change_kind, data_json, created_at, updated_at) "
                    "values (?, ?, ?, ?, ?, 'ACTIVE', 0, ?, 'PACKAGE_DATA_MIGRATION', ?, ?, ?) "
                    "on conflict(tenant_id, workspace_id, blueprint_version) do update set status = 'ACTIVE', "
                    "operating_version = excluded.operating_version, change_kind = excluded.change_kind, "
                    "data_json = excluded.data_json, updated_at = excluded.updated_at",
                    (
                        f"workspace-package-version-{uuid4()}", self.tenant_id, current["company_id"],
                        workspace_id, report["target"]["version"], operating_version,
                        json.dumps(blueprint, ensure_ascii=False), at, at,
                    ),
                )
                updated_instance = self._instance(connection, workspace_id)
                protected_after = self._protected_migration_snapshot(connection, updated_instance)
                if protected_before != protected_after:
                    raise PackageValidationError("migration changed protected Core identity or references")
                data_after = _fingerprint(self._rows(
                    connection,
                    "select * from workspace_package_objects where tenant_id = ? and company_id = ? "
                    "and workspace_id = ? order by object_id",
                    (self.tenant_id, current["company_id"], workspace_id),
                ))
                connection.execute(
                    "update workspace_package_migration_journal set status = 'APPLIED', "
                    "data_fingerprint_after = ?, protected_fingerprint_after = ?, updated_at = ? "
                    "where tenant_id = ? and migration_id = ? and status = 'PREPARED'",
                    (data_after, _fingerprint([protected_after]), at, self.tenant_id, migration_id),
                )
                transition_before = {
                    "data": preflight["dataFingerprintBefore"],
                    "company_os": protected_before["company_os"],
                }
                transition_after = {"data": data_after, "company_os": protected_after["company_os"]}
                self._record_lifecycle_event(
                    connection, current, action="UPGRADE", report=report,
                    before=transition_before, after=transition_after,
                    detail={
                        "operatingVersion": operating_version,
                        "rollbackBoundary": "DECLARED_DOWN_MIGRATION_REQUIRED",
                        "migrationId": migration_id,
                        "checkpointDigest": preflight["checkpointDigest"],
                        "affectedObjects": len(preflight["affected"]),
                        "protectedContinuity": protected_before,
                    },
                    at=at,
                )
        except Exception as error:
            if migration_id:
                self._mark_migration_failed(migration_id, error)
            if created_target:
                self._remove_unreferenced_target(target, package)
            raise
        return self.get_workspace(workspace_id)

    def update(self, workspace_id: str, source: str | Path) -> dict:
        package = validate_package(source)
        with self.db.connect() as connection:
            current = self._instance(connection, workspace_id)
            report = self._compatibility_report(current, package, require_newer=True)
            if not report["compatible"]:
                raise PackageValidationError(", ".join(report["reasons"]))
            existing = connection.execute(
                "select * from installed_workspace_packages where tenant_id = ? and package_id = ? and version = ?",
                (self.tenant_id, current["package_id"], report["target"]["version"]),
            ).fetchone()
            if existing and (existing["digest"] != report["target"]["digest"] or existing["status"] != "ACTIVE"):
                raise PackageConflictError("target package version conflicts with installed provenance")

        if report["migrationMode"] == "DECLARATIVE_RENAME_FIELDS_V1":
            return self._update_with_migration(workspace_id, package, report)

        target, created_target = self._store_package(package)
        at = _now()
        try:
            with self.db.connect() as connection:
                connection.execute("begin immediate")
                current = self._instance(connection, workspace_id)
                if (
                    current["package_version"] != report["current"]["version"]
                    or current["package_digest"] != report["current"]["digest"]
                ):
                    raise PackageConflictError("Workspace package pin changed during update")
                report = self._compatibility_report(current, package, require_newer=True)
                if not report["compatible"]:
                    raise PackageValidationError(", ".join(report["reasons"]))
                before = self._continuity_snapshot(connection, current)
                existing = connection.execute(
                    "select * from installed_workspace_packages where tenant_id = ? and package_id = ? and version = ?",
                    (self.tenant_id, current["package_id"], report["target"]["version"]),
                ).fetchone()
                if existing is None:
                    connection.execute(
                        "insert into installed_workspace_packages values (?, ?, ?, ?, 'ACTIVE', ?, ?, ?, ?, ?, ?, null, null)",
                        (
                            self.tenant_id, current["package_id"], report["target"]["version"],
                            report["target"]["digest"], json.dumps(package["manifest"], ensure_ascii=False),
                            json.dumps(package["surfaces"], ensure_ascii=False),
                            json.dumps(package["schemas"], ensure_ascii=False), str(package["root"]),
                            str(target), at,
                        ),
                    )
                elif existing["digest"] != report["target"]["digest"] or existing["status"] != "ACTIVE":
                    raise PackageConflictError("target package version conflicts with installed provenance")
                workspace = connection.execute(
                    "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (self.tenant_id, current["company_id"], workspace_id),
                ).fetchone()
                if workspace is None:
                    raise PackageValidationError("Workspace identity disappeared during update")
                operating_version = int(workspace["operating_version"] or 0) + 1
                blueprint = self._package_blueprint(workspace, package)
                updated = connection.execute(
                    "update workspace_package_instances set package_version = ?, package_digest = ?, updated_at = ? "
                    "where tenant_id = ? and instance_id = ? and package_version = ? and package_digest = ?",
                    (
                        report["target"]["version"], report["target"]["digest"], at, self.tenant_id,
                        current["instance_id"], report["current"]["version"], report["current"]["digest"],
                    ),
                )
                if updated.rowcount != 1:
                    raise PackageConflictError("Workspace package pin update lost its compare-and-swap")
                connection.execute(
                    "update workspaces set blueprint_json = ?, blueprint_version = ?, operating_version = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (
                        json.dumps(blueprint, ensure_ascii=False), report["target"]["version"], operating_version,
                        at, self.tenant_id, current["company_id"], workspace_id,
                    ),
                )
                connection.execute(
                    "update runtime_workspace_versions set status = 'SUPERSEDED', updated_at = ? "
                    "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                    (at, self.tenant_id, workspace_id, report["current"]["version"]),
                )
                connection.execute(
                    "insert into runtime_workspace_versions(version_id, tenant_id, company_id, workspace_id, "
                    "blueprint_version, status, simulation_passed, operating_version, change_kind, data_json, created_at, updated_at) "
                    "values (?, ?, ?, ?, ?, 'ACTIVE', 0, ?, 'PACKAGE_UPGRADE', ?, ?, ?) "
                    "on conflict(tenant_id, workspace_id, blueprint_version) do update set status = 'ACTIVE', "
                    "operating_version = excluded.operating_version, change_kind = excluded.change_kind, "
                    "data_json = excluded.data_json, updated_at = excluded.updated_at",
                    (
                        f"workspace-package-version-{uuid4()}", self.tenant_id, current["company_id"], workspace_id,
                        report["target"]["version"], operating_version,
                        json.dumps(blueprint, ensure_ascii=False), at, at,
                    ),
                )
                updated_instance = self._instance(connection, workspace_id)
                after = self._continuity_snapshot(connection, updated_instance)
                if before != after:
                    raise PackageValidationError("Package update changed protected instance or Company OS data")
                self._record_lifecycle_event(
                    connection, current, action="UPGRADE", report=report, before=before, after=after,
                    detail={
                        "operatingVersion": operating_version,
                        "rollbackBoundary": "LOCAL_PACKAGE_PROJECTION_ONLY",
                        "continuity": before,
                    },
                    at=at,
                )
        except Exception:
            if created_target and target.exists():
                shutil.rmtree(target)
            raise
        return self.get_workspace(workspace_id)

    def _rollback_migration(self, workspace_id: str, current, prior, target_row) -> dict:
        detail = json.loads(prior["detail_json"])
        migration_id_up = detail.get("migrationId")
        with self.db.connect() as connection:
            applied = connection.execute(
                "select * from workspace_package_migration_journal where tenant_id = ? and migration_id = ? "
                "and direction = 'UP' and status = 'APPLIED'",
                (self.tenant_id, migration_id_up),
            ).fetchone()
            if applied is None or not applied["reversible"]:
                raise PackageConflictError("applied migration has no reversible checkpoint")
            old_checkpoint = json.loads(applied["checkpoint_json"])
        package = validate_package(target_row["stored_path"])
        migration = json.loads(applied["migration_json"])
        package["migration"] = migration
        current_schemas = json.loads(current["schemas_json"])
        for object_type, plan in migration["objects"].items():
            if (
                object_type not in current_schemas
                or object_type not in package["schemas"]
                or _schema_after_renames(current_schemas[object_type], plan, direction="down")
                != package["schemas"][object_type]
            ):
                raise PackageValidationError("down migration schema does not restore rollback target")
        report = {
            "compatible": True,
            "compatibilityMode": "DECLARED_PACKAGE_DATA_MIGRATION",
            "migrationMode": "DECLARATIVE_RENAME_FIELDS_V1",
            "current": {
                "packageId": current["package_id"], "version": current["package_version"],
                "digest": current["package_digest"],
            },
            "target": {
                "packageId": current["package_id"], "version": target_row["version"],
                "digest": target_row["digest"],
            },
            "preserves": [
                "company_id", "business_id", "workspace_id", "instance_id", "object_id",
                "company_os_entities", "company_os_links",
            ],
            "reasons": [],
        }
        with self.db.connect() as connection:
            preflight = self._migration_preflight(connection, current, package, direction="down")
        migration_id = self._prepare_migration(
            current, package, report, preflight, Path(target_row["stored_path"]), direction="DOWN",
        )
        try:
            at = _now()
            with self.db.connect() as connection:
                connection.execute("begin immediate")
                current = self._instance(connection, workspace_id)
                if current["package_version"] != prior["to_version"] or current["package_digest"] != prior["to_digest"]:
                    raise PackageConflictError("Workspace package pin changed during migration rollback")
                preflight = self._migration_preflight(connection, current, package, direction="down")
                journal = connection.execute(
                    "select * from workspace_package_migration_journal where tenant_id = ? "
                    "and migration_id = ? and status = 'PREPARED'",
                    (self.tenant_id, migration_id),
                ).fetchone()
                if journal is None or _fingerprint([preflight["checkpoint"]]) != _fingerprint([
                    json.loads(journal["checkpoint_json"])
                ]):
                    raise PackageConflictError("rollback checkpoint changed before atomic apply")
                protected_before = self._protected_migration_snapshot(connection, current)
                if _fingerprint([protected_before]) != journal["protected_fingerprint_before"]:
                    raise PackageConflictError("protected identity changed before rollback")
                self._apply_object_migration(
                    connection, current, package, preflight, direction="down", at=at,
                )
                for expected in old_checkpoint["objects"]:
                    restored = connection.execute(
                        "select schema_version, data_json from workspace_package_objects "
                        "where tenant_id = ? and workspace_id = ? and object_id = ?",
                        (self.tenant_id, workspace_id, expected["objectId"]),
                    ).fetchone()
                    if (
                        restored is None
                        or restored["schema_version"] != expected["schemaVersion"]
                        or json.loads(restored["data_json"]) != expected["data"]
                    ):
                        raise PackageValidationError("down migration does not match the original data checkpoint")
                for expected in old_checkpoint["projections"]:
                    restored = connection.execute(
                        "select blueprint_version, data_json from runtime_entities where tenant_id = ? "
                        "and workspace_id = ? and entity_id = ? and entity_type = 'PACKAGE_DOMAIN_OBJECT'",
                        (self.tenant_id, workspace_id, expected["entityId"]),
                    ).fetchone()
                    if (
                        restored is None
                        or restored["blueprint_version"] != expected["blueprintVersion"]
                        or json.loads(restored["data_json"]) != expected["data"]
                    ):
                        raise PackageValidationError("down migration does not match the original projection checkpoint")
                workspace = connection.execute(
                    "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (self.tenant_id, current["company_id"], workspace_id),
                ).fetchone()
                if workspace is None:
                    raise PackageValidationError("Workspace identity disappeared during migration rollback")
                operating_version = int(workspace["operating_version"] or 0) + 1
                blueprint = self._package_blueprint(workspace, package)
                updated = connection.execute(
                    "update workspace_package_instances set package_version = ?, package_digest = ?, updated_at = ? "
                    "where tenant_id = ? and instance_id = ? and package_version = ? and package_digest = ?",
                    (
                        report["target"]["version"], report["target"]["digest"], at, self.tenant_id,
                        current["instance_id"], report["current"]["version"], report["current"]["digest"],
                    ),
                )
                if updated.rowcount != 1:
                    raise PackageConflictError("migration rollback lost its compare-and-swap")
                connection.execute(
                    "update workspaces set blueprint_json = ?, blueprint_version = ?, operating_version = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (
                        json.dumps(blueprint, ensure_ascii=False), report["target"]["version"], operating_version,
                        at, self.tenant_id, current["company_id"], workspace_id,
                    ),
                )
                connection.execute(
                    "update runtime_workspace_versions set status = 'ROLLED_BACK', updated_at = ? "
                    "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                    (at, self.tenant_id, workspace_id, report["current"]["version"]),
                )
                connection.execute(
                    "update runtime_workspace_versions set status = 'ACTIVE', operating_version = ?, "
                    "change_kind = 'PACKAGE_MIGRATION_ROLLBACK', data_json = ?, updated_at = ? "
                    "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                    (
                        operating_version, json.dumps(blueprint, ensure_ascii=False), at,
                        self.tenant_id, workspace_id, report["target"]["version"],
                    ),
                )
                rolled_back = self._instance(connection, workspace_id)
                protected_after = self._protected_migration_snapshot(connection, rolled_back)
                if protected_before != protected_after:
                    raise PackageValidationError("migration rollback changed protected Core identity or references")
                data_after = _fingerprint(self._rows(
                    connection,
                    "select * from workspace_package_objects where tenant_id = ? and company_id = ? "
                    "and workspace_id = ? order by object_id",
                    (self.tenant_id, current["company_id"], workspace_id),
                ))
                connection.execute(
                    "update workspace_package_migration_journal set status = 'APPLIED', "
                    "data_fingerprint_after = ?, protected_fingerprint_after = ?, updated_at = ? "
                    "where tenant_id = ? and migration_id = ? and status = 'PREPARED'",
                    (data_after, _fingerprint([protected_after]), at, self.tenant_id, migration_id),
                )
                self._record_lifecycle_event(
                    connection, current, action="ROLLBACK", report=report,
                    before={
                        "data": preflight["dataFingerprintBefore"],
                        "company_os": protected_before["company_os"],
                    },
                    after={"data": data_after, "company_os": protected_after["company_os"]},
                    detail={
                        "operatingVersion": operating_version,
                        "rollbackBoundary": "DECLARED_DOWN_MIGRATION_CHECKPOINT_VERIFIED",
                        "migrationId": migration_id,
                        "rollbackOfMigrationId": migration_id_up,
                        "checkpointDigest": _fingerprint([old_checkpoint]),
                        "affectedObjects": len(preflight["affected"]),
                        "protectedContinuity": protected_before,
                    },
                    at=at,
                )
        except Exception as error:
            self._mark_migration_failed(migration_id, error)
            raise
        return self.get_workspace(workspace_id)

    def rollback(self, workspace_id: str) -> dict:
        with self.db.connect() as connection:
            current = self._instance(connection, workspace_id)
            prior = connection.execute(
                "select * from workspace_package_lifecycle_events where tenant_id = ? and workspace_id = ? "
                "and action = 'UPGRADE' and to_version = ? and to_digest = ? order by rowid desc limit 1",
                (self.tenant_id, workspace_id, current["package_version"], current["package_digest"]),
            ).fetchone()
            if prior is None:
                raise PackageConflictError("current package version has no applied upgrade to roll back")
            target_row = connection.execute(
                "select * from installed_workspace_packages where tenant_id = ? and package_id = ? and version = ? and digest = ? and status = 'ACTIVE'",
                (self.tenant_id, current["package_id"], prior["from_version"], prior["from_digest"]),
            ).fetchone()
            if target_row is None or not Path(target_row["stored_path"]).is_dir():
                raise PackageConflictError("rollback target package is unavailable")
            migration_rollback = prior["migration_mode"] == "DECLARATIVE_RENAME_FIELDS_V1"
            if migration_rollback:
                package = None
            else:
                package = validate_package(target_row["stored_path"])
                report = self._compatibility_report(current, package, require_newer=False)
                if not report["compatible"]:
                    raise PackageValidationError(", ".join(report["reasons"]))

        if migration_rollback:
            return self._rollback_migration(workspace_id, current, prior, target_row)

        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            current = self._instance(connection, workspace_id)
            if current["package_version"] != prior["to_version"] or current["package_digest"] != prior["to_digest"]:
                raise PackageConflictError("Workspace package pin changed during rollback")
            before = self._continuity_snapshot(connection, current)
            workspace = connection.execute(
                "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.tenant_id, current["company_id"], workspace_id),
            ).fetchone()
            if workspace is None:
                raise PackageValidationError("Workspace identity disappeared during rollback")
            operating_version = int(workspace["operating_version"] or 0) + 1
            blueprint = self._package_blueprint(workspace, package)
            updated = connection.execute(
                "update workspace_package_instances set package_version = ?, package_digest = ?, updated_at = ? "
                "where tenant_id = ? and instance_id = ? and package_version = ? and package_digest = ?",
                (
                    report["target"]["version"], report["target"]["digest"], at, self.tenant_id,
                    current["instance_id"], report["current"]["version"], report["current"]["digest"],
                ),
            )
            if updated.rowcount != 1:
                raise PackageConflictError("Workspace package rollback lost its compare-and-swap")
            connection.execute(
                "update workspaces set blueprint_json = ?, blueprint_version = ?, operating_version = ?, updated_at = ? "
                "where tenant_id = ? and company_id = ? and workspace_id = ?",
                (
                    json.dumps(blueprint, ensure_ascii=False), report["target"]["version"], operating_version,
                    at, self.tenant_id, current["company_id"], workspace_id,
                ),
            )
            connection.execute(
                "update runtime_workspace_versions set status = 'ROLLED_BACK', updated_at = ? "
                "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                (at, self.tenant_id, workspace_id, report["current"]["version"]),
            )
            connection.execute(
                "update runtime_workspace_versions set status = 'ACTIVE', operating_version = ?, "
                "change_kind = 'PACKAGE_ROLLBACK', data_json = ?, updated_at = ? "
                "where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                (
                    operating_version, json.dumps(blueprint, ensure_ascii=False), at,
                    self.tenant_id, workspace_id, report["target"]["version"],
                ),
            )
            rolled_back_instance = self._instance(connection, workspace_id)
            after = self._continuity_snapshot(connection, rolled_back_instance)
            if before != after:
                raise PackageValidationError("Package rollback changed protected instance or Company OS data")
            self._record_lifecycle_event(
                connection, current, action="ROLLBACK", report=report, before=before, after=after,
                detail={
                    "operatingVersion": operating_version,
                    "rollbackBoundary": "LOCAL_PACKAGE_PROJECTION_ONLY",
                    "continuity": before,
                },
                at=at,
            )
        return self.get_workspace(workspace_id)

    def lifecycle(self, workspace_id: str) -> dict:
        with self.db.connect() as connection:
            current = self._instance(connection, workspace_id)
            events = self._rows(
                connection,
                "select * from workspace_package_lifecycle_events where tenant_id = ? and workspace_id = ? order by rowid",
                (self.tenant_id, workspace_id),
            )
            for event in events:
                event["detail"] = json.loads(event.pop("detail_json"))
            migrations = self._rows(
                connection,
                "select migration_id, direction, status, from_version, from_digest, to_version, to_digest, "
                "reversible, affected_count, data_fingerprint_before, data_fingerprint_after, "
                "protected_fingerprint_before, protected_fingerprint_after, error_code, created_at, updated_at "
                "from workspace_package_migration_journal where tenant_id = ? and workspace_id = ? order by rowid",
                (self.tenant_id, workspace_id),
            )
            return {
                "instanceId": current["instance_id"],
                "companyId": current["company_id"],
                "workspaceId": current["workspace_id"],
                "packageId": current["package_id"],
                "currentVersion": current["package_version"],
                "currentDigest": current["package_digest"],
                "events": events,
                "migrations": migrations,
            }

    def navigation(self, company_id: str | None = None) -> list[dict]:
        params: list[str] = [self.tenant_id]
        company_filter = ""
        if company_id:
            company_filter = " and i.company_id = ?"
            params.append(company_id)
        with self.db.connect() as connection:
            rows = connection.execute(
                "select i.workspace_id, i.company_id, i.package_id, i.package_version, p.manifest_json "
                "from workspace_package_instances i join installed_workspace_packages p "
                "on p.tenant_id = i.tenant_id and p.package_id = i.package_id and p.version = i.package_version "
                "where i.tenant_id = ? and i.status = 'ACTIVE' and p.status = 'ACTIVE'" + company_filter + " order by i.created_at",
                params,
            ).fetchall()
        result = []
        for row in rows:
            manifest = json.loads(row["manifest_json"])
            result.append({
                "workspace_id": row["workspace_id"], "company_id": row["company_id"],
                "package_id": row["package_id"], "package_version": row["package_version"],
                "label": manifest["workspace"]["navigation"]["label"],
                "icon": manifest["workspace"]["navigation"]["icon"],
                "href": f"/ceo-office/workspace/installed/{row['workspace_id']}",
            })
        return result

    def _instance(self, connection, workspace_id: str, *, active: bool = True):
        status = " and i.status = 'ACTIVE' and p.status = 'ACTIVE'" if active else ""
        row = connection.execute(
            "select i.*, p.status as package_status, p.manifest_json, p.surfaces_json, p.schemas_json, p.source_path, p.stored_path, p.installed_at, p.disabled_at, p.uninstalled_at "
            "from workspace_package_instances i join installed_workspace_packages p "
            "on p.tenant_id = i.tenant_id and p.package_id = i.package_id and p.version = i.package_version "
            "where i.tenant_id = ? and i.workspace_id = ?" + status,
            (self.tenant_id, workspace_id),
        ).fetchone()
        if row is None:
            raise PackageScopeError("installed workspace does not exist or is inactive")
        return row

    def _resolve_v2_requirement(self, connection, instance, requirement: dict, capabilities: dict) -> dict:
        rows = connection.execute(
            "select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='RESPONSIBILITY_ASSIGNMENT' and lifecycle_status != 'ARCHIVED'",
            (self.tenant_id, instance["company_id"], instance["workspace_id"]),
        ).fetchall()
        assignments = [self._runtime_item(row) for row in rows]
        assignments = [
            item for item in assignments
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == instance["workspace_id"]
            and item["data"].get("responsibilityKey") == requirement["responsibilityKey"]
        ]
        if len(assignments) != 1:
            return {"status": "RESPONSIBILITY_GAP", "eligible": False, "requirementRef": requirement["key"]}
        assignment = assignments[0]
        data = assignment["data"]
        try:
            role = self._runtime_entity(
                connection, str(data.get("roleRef") or ""), "ROLE_SLOT",
                instance["company_id"], instance["workspace_id"],
            )
            employee = self._runtime_entity(
                connection, str(data.get("employeeRef") or ""), "AI_EMPLOYEE",
                instance["company_id"], instance["workspace_id"],
            )
        except PackageValidationError:
            return {
                "status": "UNSTAFFED", "eligible": False, "requirementRef": requirement["key"],
                "assignmentRef": assignment["entity_id"],
            }
        if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
            return {
                "status": "UNSTAFFED", "eligible": False, "requirementRef": requirement["key"],
                "assignmentRef": assignment["entity_id"], "roleRef": role["entity_id"],
            }
        binding_refs = list(data.get("capabilityBindingRefs") or [])
        resolved_bindings = []
        for capability_ref in requirement["capabilityRequirementRefs"]:
            declared = capabilities[capability_ref]
            matches = []
            for binding_ref in binding_refs:
                try:
                    binding = self._runtime_entity(
                        connection, binding_ref, "CAPABILITY_BINDING",
                        instance["company_id"], instance["workspace_id"],
                    )
                except PackageValidationError:
                    continue
                review = binding["data"].get("supplyReview")
                if isinstance(review, dict) and all(
                    review.get(key) == declared[key] for key in ("source", "capabilityType", "capabilityId")
                ):
                    matches.append((binding, review))
            if len(matches) != 1:
                return {
                    "status": "CAPABILITY_GAP", "eligible": False, "requirementRef": requirement["key"],
                    "assignmentRef": assignment["entity_id"], "employeeRef": employee["entity_id"],
                    "capabilityRequirementRef": capability_ref,
                }
            binding, review = matches[0]
            supply = self.company_runtime._resolve_supply(
                connection, review.get("source"), review.get("capabilityType"), review.get("capabilityId"),
            )
            current = self.company_runtime._assess_supply(connection, supply) if supply else None
            if (
                binding["lifecycle_status"] != "ACTIVE"
                or not str(binding["data"].get("authorizationStatus") or "").startswith("AUTHORIZED")
                or current is None or current["blockers"]
                or any(review.get(key) != current.get(key) for key in ("source", "capabilityType", "capabilityId", "catalogUpdatedAt"))
            ):
                return {
                    "status": "CAPABILITY_GAP", "eligible": False, "requirementRef": requirement["key"],
                    "assignmentRef": assignment["entity_id"], "employeeRef": employee["entity_id"],
                    "capabilityRequirementRef": capability_ref,
                }
            resolved_bindings.append(binding["entity_id"])
        return {
            "status": "RESOLVED", "eligible": True, "requirementRef": requirement["key"],
            "assignmentRef": assignment["entity_id"], "roleRef": role["entity_id"],
            "employeeRef": employee["entity_id"], "capabilityBindingRefs": resolved_bindings,
        }

    def _v2_runtime_model(self, connection, instance, compiled: dict, objects: list) -> dict:
        requirements = {item["key"]: item for item in compiled["responsibilityRequirements"]}
        capabilities = {item["key"]: item for item in compiled["capabilityRequirements"]}
        requirement_status = {
            key: self._resolve_v2_requirement(connection, instance, item, capabilities)
            for key, item in requirements.items()
        }
        surfaces = []
        for surface in compiled["surfaces"]:
            gaps = [
                requirement_status[ref] for ref in surface["responsibilityRequirementRefs"]
                if not requirement_status[ref]["eligible"]
            ]
            availability = surface["availability"]
            if availability["mode"] == "CONDITIONAL" and availability["condition"] == "WORKSPACE_HAS_OBJECTS" and not objects:
                gaps.append({"status": "CONDITION_NOT_MET", "condition": availability["condition"], "eligible": False})
            eligible = not gaps
            surfaces.append(surface | {
                "eligible": eligible,
                "status": "AVAILABLE" if eligible else gaps[0]["status"],
                "gaps": gaps,
            })
        by_key = {item["key"]: item for item in surfaces}
        navigation = [
            item | {
                "eligible": by_key[item["surfaceRef"]]["eligible"],
                "status": by_key[item["surfaceRef"]]["status"],
            }
            for item in compiled["domainNavigation"]
        ]
        required = [item for item in surfaces if item["availability"]["mode"] == "REQUIRED"]
        return {
            **compiled,
            "domainNavigation": navigation,
            "surfaces": surfaces,
            "requirementResolution": list(requirement_status.values()),
            "operationalStatus": "OPERATIONAL" if all(item["eligible"] for item in required) else "DRAFT",
            "workspaceGap": {
                "key": "__workspace_gap__", "source": "CORE", "status": "WORKSPACE_GAP",
                "eligible": True, "purpose": "Resolve required Workspace responsibility or capability gaps",
            },
        }

    @staticmethod
    def _v2_projection_profiles(compiled: dict, shared: dict) -> dict:
        results = shared["results"]
        values = {
            "CORE_WORK": shared["work_items"],
            "CORE_RESULT": [item for item in results if item["kind"] != "EVIDENCE"],
            "CORE_EVIDENCE": [item for item in results if item["kind"] == "EVIDENCE"],
        }
        return {item["key"]: values[item["type"]] for item in compiled["projectionProfiles"]}

    def get_workspace(self, workspace_id: str, *, include_archived: bool = False) -> dict:
        with self.db.connect() as connection:
            row = self._instance(connection, workspace_id, active=not include_archived)
            objects = connection.execute(
                "select * from workspace_package_objects where tenant_id = ? and workspace_id = ? order by created_at, object_id",
                (self.tenant_id, workspace_id),
            ).fetchall()
            activities = connection.execute(
                "select * from workspace_package_activities where tenant_id = ? and workspace_id = ? order by created_at, activity_id",
                (self.tenant_id, workspace_id),
            ).fetchall()
            object_projections = [self._object_with_integration(connection, item) for item in objects]
            manifest = json.loads(row["manifest_json"])
            surfaces = json.loads(row["surfaces_json"])
            runtime_model = (
                self._v2_runtime_model(connection, row, surfaces, object_projections)
                if manifest.get("schemaVersion") == PACKAGE_SCHEMA_V2 else None
            )
        shared = self.shared_projection.workspace(row["company_id"], workspace_id) if runtime_model else None
        result = {
            "instance": {key: row[key] for key in ("instance_id", "company_id", "workspace_id", "package_id", "package_version", "package_digest", "status")},
            "package": {
                "package_id": row["package_id"], "version": row["package_version"], "digest": row["package_digest"],
                "status": row["package_status"], "source_path": row["source_path"], "stored_path": row["stored_path"],
                "installed_at": row["installed_at"], "disabled_at": row["disabled_at"], "uninstalled_at": row["uninstalled_at"],
                "schema_version": manifest["schemaVersion"],
                "capability_requirements": manifest["capabilityRequirements"], "granted_capabilities": [],
            },
            "workspace": manifest["workspace"],
            "surfaces": surfaces,
            "schemas": json.loads(row["schemas_json"]),
            "objects": object_projections,
            "activities": [self._activity_projection(item) for item in activities],
            "read_only": row["status"] != "ACTIVE" or row["package_status"] != "ACTIVE",
        }
        if runtime_model:
            result["surfaceModel"] = runtime_model
            result["shared"] = {
                "team": shared["team"],
                "projections": self._v2_projection_profiles(runtime_model, shared),
            }
        return result

    @staticmethod
    def _object_projection(row) -> dict:
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        return item

    @staticmethod
    def _activity_projection(row) -> dict:
        item = dict(row)
        item["detail"] = json.loads(item.pop("detail_json"))
        return item

    def _object_with_integration(self, connection, row) -> dict:
        item = self._object_projection(row)
        try:
            item["company_integration"] = self._integration_projection(
                connection, item["object_id"], item["company_id"], item["workspace_id"], strict=False,
            )
        except (KeyError, PackageValidationError):
            item["company_integration"] = {"status": "INVALID", "resolvable": False}
        return item

    @staticmethod
    def _runtime_item(row) -> dict:
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        return item

    def _runtime_entity(
        self,
        connection,
        entity_id: str,
        expected_type: str,
        company_id: str,
        workspace_id: str,
    ) -> dict:
        row = connection.execute(
            "select * from runtime_entities where tenant_id = ? and entity_id = ?",
            (self.tenant_id, entity_id),
        ).fetchone()
        if row is None:
            raise PackageValidationError(f"Core reference does not resolve: {entity_id}")
        item = self._runtime_item(row)
        if (
            item["entity_type"] != expected_type
            or item["company_id"] != company_id
            or item["workspace_id"] != workspace_id
        ):
            raise PackageValidationError(f"Core reference type or scope is invalid: {entity_id}")
        return item

    def _links(self, connection, source_id: str, relation: str) -> list[dict]:
        return [dict(row) for row in connection.execute(
            "select * from runtime_links where tenant_id = ? and source_id = ? and relation = ? "
            "order by created_at, link_id",
            (self.tenant_id, source_id, relation),
        ).fetchall()]

    def _insert_link(self, connection, source: dict, relation: str, target: dict, at: str) -> None:
        if source["company_id"] != target["company_id"] or source["workspace_id"] != target["workspace_id"]:
            raise PackageValidationError("cross-scope Core relationship rejected")
        connection.execute(
            "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
            "values (?, ?, ?, ?, ?, ?, ?, ?) on conflict(tenant_id, source_id, relation, target_id) do nothing",
            (
                f"link-{uuid4()}", self.tenant_id, source["company_id"], source["workspace_id"],
                source["entity_id"], relation, target["entity_id"], at,
            ),
        )

    def _resolve_operating_chain(
        self,
        connection,
        company_id: str,
        workspace_id: str,
        responsibility_type: str,
    ) -> dict:
        role_rows = connection.execute(
            "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? "
            "and entity_type = 'ROLE_SLOT' and lifecycle_status in ('ASSIGNED','OPERATING')",
            (self.tenant_id, company_id, workspace_id),
        ).fetchall()
        roles = [self._runtime_item(row) for row in role_rows]
        roles = [item for item in roles if item["data"].get("responsibilityType") == responsibility_type]
        if len(roles) != 1:
            raise PackageValidationError("responsibility routing must resolve exactly one active Role Slot")
        role = roles[0]
        employee_id = str(role["data"].get("assignedEmployeeRef") or "")
        employee = self._runtime_entity(connection, employee_id, "AI_EMPLOYEE", company_id, workspace_id)
        if (
            employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
            or employee["data"].get("roleSlotRef") != role["entity_id"]
            or not connection.execute(
                "select 1 from runtime_links where tenant_id = ? and source_id = ? and relation = 'PROPOSED_FOR' and target_id = ?",
                (self.tenant_id, employee["entity_id"], role["entity_id"]),
            ).fetchone()
        ):
            raise PackageValidationError("responsibility has no valid current Employee")

        capability_links = self._links(connection, role["entity_id"], "REQUIRES_CAPABILITY")
        if len(capability_links) != 1:
            raise PackageValidationError("responsibility must resolve exactly one Capability Binding")
        binding = self._runtime_entity(
            connection, capability_links[0]["target_id"], "CAPABILITY_BINDING", company_id, workspace_id,
        )
        review = binding["data"].get("supplyReview")
        if binding["lifecycle_status"] != "ACTIVE" or binding["data"].get("authorizationStatus") != "AUTHORIZED_ACTIVE" or not isinstance(review, dict):
            raise PackageValidationError("Capability Binding is not active and authorized")
        supply = self.company_runtime._resolve_supply(
            connection, review.get("source"), review.get("capabilityType"), review.get("capabilityId"),
        )
        if supply is None:
            raise PackageValidationError("Capability supply is unavailable")
        current = self.company_runtime._assess_supply(connection, supply) | {"runtimeMeta": supply["runtimeMeta"]}
        if current["blockers"] or any(
            review.get(key) != current.get(key)
            for key in ("source", "capabilityType", "capabilityId", "catalogUpdatedAt")
        ):
            raise PackageValidationError("Capability supply is blocked or stale")
        if (
            current["capabilityId"] != CORE_COMPANY_CAPABILITY
            or current["runtimeMeta"].get("handler") != CORE_COMPANY_CAPABILITY
        ):
            raise PackageValidationError("Capability supply has no supported Core operating handler")
        return {"role": role, "employee": employee, "binding": binding, "capability": current}

    def get_object(self, workspace_id: str, object_id: str) -> dict:
        with self.db.connect() as connection:
            self._instance(connection, workspace_id)
            row = connection.execute(
                "select * from workspace_package_objects where tenant_id = ? and workspace_id = ? and object_id = ?",
                (self.tenant_id, workspace_id, object_id),
            ).fetchone()
            if row is None:
                raise PackageScopeError("Package object does not exist")
            return self._object_with_integration(connection, row)

    @staticmethod
    def _validated_data(schema: dict, values: dict) -> dict:
        if not isinstance(values, dict) or set(values) - set(schema["properties"]):
            raise PackageValidationError("domain object contains unknown fields")
        result = dict(values)
        for name in CORE_REFERENCE_FIELDS:
            if str(result.get(name) or "").strip():
                raise PackageValidationError(f"Core reference field is read-only: {name}")
            if name in schema["properties"]:
                result[name] = ""
        for name, field in schema["properties"].items():
            if name not in result and "default" in field:
                result[name] = field["default"]
            value = result.get(name)
            if name in schema["required"] and name not in CORE_REFERENCE_FIELDS and (
                not isinstance(value, str) or not value.strip()
            ):
                raise PackageValidationError(f"domain object field is required: {name}")
            if value is None:
                continue
            if not isinstance(value, str):
                raise PackageValidationError(f"domain object field must be a string: {name}")
            if len(value) > field.get("maxLength", 20000):
                raise PackageValidationError(f"domain object field is too long: {name}")
            if field.get("enum") and value not in field["enum"]:
                raise PackageValidationError(f"domain object enum is invalid: {name}")
        return result

    def create_object(self, workspace_id: str, action_id: str, object_type: str, values: dict, owner_ref: str = "") -> dict:
        if action_id not in SAFE_ACTIONS:
            raise PackageValidationError("Core action is not allowed")
        if owner_ref.strip():
            raise PackageValidationError("owner_ref is a read-only Core relationship projection")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            object_id = f"package-object-{uuid4()}"
            self.create_object_in_connection(connection, workspace_id, action_id, object_type, values, object_id)
        return self.get_object(workspace_id, object_id)

    def create_object_in_connection(self, connection, workspace_id, action_id, object_type, values, object_id):
        if not connection.in_transaction or action_id not in SAFE_ACTIONS:
            raise PackageValidationError("Package object creation requires an allowed action and transaction")
        at = _now()
        instance = self._instance(connection, workspace_id)
        manifest = json.loads(instance["manifest_json"])
        schemas = json.loads(instance["schemas_json"])
        if action_id not in manifest["actions"] or object_type not in schemas:
            raise PackageValidationError("action or object type is not declared by the package")
        if object_type in manifest.get("canonicalEntityBindings", {}):
            raise PackageValidationError("canonical domain object must use its scoped domain command, not package object storage")
        data = self._validated_data(schemas[object_type], values)
        activity_id = f"package-activity-{uuid4()}"
        connection.execute(
            "insert into workspace_package_objects values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                object_id, instance["instance_id"], self.tenant_id, instance["company_id"], workspace_id,
                object_type, schemas[object_type]["schemaVersion"], schemas[object_type]["initialState"],
                "", json.dumps(data, ensure_ascii=False), at, at,
            ),
        )
        connection.execute(
            "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, "
            "owner_ref, lifecycle_status, blueprint_version, verification_status, evidence_condition, "
            "data_json, created_at, updated_at) values (?, ?, 'PACKAGE_DOMAIN_OBJECT', ?, ?, '', ?, ?, "
            "'UNVERIFIED', 'MISSING', ?, ?, ?)",
            (
                object_id, self.tenant_id, instance["company_id"], workspace_id,
                schemas[object_type]["initialState"], instance["package_version"],
                json.dumps({
                    "packageId": instance["package_id"],
                    "packageVersion": instance["package_version"],
                    "objectType": object_type,
                    "schemaVersion": schemas[object_type]["schemaVersion"],
                    "businessData": data,
                    "companyIntegration": {"status": "NOT_STARTED"},
                }, ensure_ascii=False),
                at, at,
            ),
        )
        connection.execute(
            "insert into workspace_package_activities values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                activity_id, instance["instance_id"], self.tenant_id, instance["company_id"], workspace_id,
                action_id, object_id, json.dumps({"objectType": object_type}), at,
            ),
        )

    def operate_object(self, workspace_id: str, object_id: str, responsibility_type: str) -> dict:
        responsibility_type = responsibility_type.strip().upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{2,63}", responsibility_type):
            raise PackageValidationError("responsibility_type is invalid")
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            instance = self._instance(connection, workspace_id)
            row = connection.execute(
                "select * from workspace_package_objects where tenant_id = ? and workspace_id = ? and object_id = ?",
                (self.tenant_id, workspace_id, object_id),
            ).fetchone()
            if row is None:
                raise PackageScopeError("Package object does not exist")
            package_object = self._object_projection(row)
            schemas = json.loads(instance["schemas_json"])
            schema = schemas.get(package_object["object_type"]) or {}
            status_field = (schema.get("properties") or {}).get("status") or {}
            if "TRIAGED" not in (status_field.get("enum") or []) or "summary" not in (schema.get("properties") or {}):
                raise PackageValidationError("Company operating proof requires summary and TRIAGED domain semantics")
            identity = self._runtime_entity(
                connection, object_id, "PACKAGE_DOMAIN_OBJECT", instance["company_id"], workspace_id,
            )
            if identity["lifecycle_status"] != package_object["lifecycle_status"]:
                raise PackageValidationError("Package projection and Core identity state disagree")
            if identity["lifecycle_status"] != "NEW":
                raise PackageConflictError("Package object is not in an operable NEW state")
            chain = self._resolve_operating_chain(
                connection, instance["company_id"], workspace_id, responsibility_type,
            )
            self._insert_link(connection, identity, "HAS_CURRENT_RESPONSIBILITY", chain["role"], at)
            self._insert_link(connection, identity, "HAS_CURRENT_EXECUTOR", chain["employee"], at)
            self._insert_link(connection, identity, "USES_CAPABILITY", chain["binding"], at)
            data = identity["data"] | {
                "companyIntegration": {
                    "status": "ROUTED",
                    "responsibilityType": responsibility_type,
                    "responsibilityRef": chain["role"]["entity_id"],
                    "employeeRef": chain["employee"]["entity_id"],
                    "capabilityBindingRef": chain["binding"]["entity_id"],
                    "capability": {key: value for key, value in chain["capability"].items() if key != "runtimeMeta"},
                    "routedAt": at,
                },
                "operatingDefinitionOrigin": {
                    "kind": "PACKAGE_DOMAIN_SCHEMA",
                    "packageId": instance["package_id"],
                    "packageVersion": instance["package_version"],
                    "schemaVersion": package_object["schema_version"],
                },
                "workContext": {
                    "objectOwnerRef": chain["employee"]["entity_id"],
                    "responsibilityRoleSlotRef": chain["role"]["entity_id"],
                    "responsibilityEmployeeRef": chain["employee"]["entity_id"],
                    "currentExecutorRef": chain["employee"]["entity_id"],
                    "status": "working", "activity": "Company OS execution started", "updatedAt": at,
                },
            }
            business_data = dict(package_object["data"])
            if "responsibilityRef" in business_data:
                business_data["responsibilityRef"] = chain["role"]["entity_id"]
            if "evidenceRef" in business_data:
                business_data["evidenceRef"] = ""
            data["businessData"] = business_data
            connection.execute(
                "update runtime_entities set owner_ref = ?, capability_ref = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'NEW'",
                (
                    chain["employee"]["entity_id"], chain["binding"]["entity_id"],
                    json.dumps(data, ensure_ascii=False), at, self.tenant_id, object_id,
                ),
            )
            connection.execute(
                "update workspace_package_objects set owner_ref = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and object_id = ? and lifecycle_status = 'NEW'",
                (
                    chain["employee"]["entity_id"], json.dumps(business_data, ensure_ascii=False), at,
                    self.tenant_id, object_id,
                ),
            )

        capability = chain["capability"]
        employee = chain["employee"]
        task = self.results.create_task(
            f"Operate Package object {object_id} for {responsibility_type}",
            company_id=instance["company_id"],
            capability_source=capability["source"],
            capability_type=capability["capabilityType"],
            capability_id=capability["capabilityId"],
            employee_id=employee["entity_id"],
            employee_role=str(chain["role"]["data"].get("name") or responsibility_type),
            employee_name=str(employee["data"].get("name") or employee["entity_id"]),
        )
        self.results.transition(task["task_id"], "RUNNING", {"selected_tool": capability["capabilityId"]})
        self._bind_task(object_id, task["task_id"])

        capability_result = self._execute_company_capability(capability, package_object["data"])
        prompt = f"{responsibility_type}: {str(package_object['data'].get('summary') or '').strip()}"
        if capability_result["status"] == "failed":
            error = capability_result["error"]
            execution = self.results.save_execution(
                task["task_id"], capability["capabilityId"], prompt, error, 0,
            )
            self.results.transition(task["task_id"], "FAILED", {
                "selected_tool": capability["capabilityId"], "error": error,
            })
            self._finalize_failed_operation(
                workspace_id, object_id, task["task_id"], execution["execution_id"], error,
            )
            return self.resolve_company_integration(workspace_id, object_id)

        output = capability_result["output"]
        execution = self.results.save_execution(
            task["task_id"], capability["capabilityId"], prompt, output, 0,
        )
        self.results.transition(task["task_id"], "COMPLETED", {
            "selected_tool": capability["capabilityId"], "output": output, "cost": 0, "error": None,
        })
        artifacts = self.results.list_artifacts(task_id=task["task_id"])
        if len(artifacts) != 1:
            raise PackageValidationError("completed Company execution must produce exactly one Artifact")
        self._finalize_successful_operation(
            workspace_id, object_id, task["task_id"], execution["execution_id"], artifacts[0], output,
        )
        return self.resolve_company_integration(workspace_id, object_id)

    @staticmethod
    def _execute_company_capability(capability: dict, business_data: dict) -> dict:
        if capability.get("capabilityId") != CORE_COMPANY_CAPABILITY:
            raise PackageValidationError("unsupported Core Company capability")
        summary = str(business_data.get("summary") or "").strip()
        if len(summary) < MIN_OPERATING_SUMMARY_LENGTH:
            return {"status": "failed", "error": "customer_feedback_summary_insufficient"}
        title = str(business_data.get("title") or "Untitled feedback").strip()
        channel = str(business_data.get("channel") or "UNKNOWN").strip()
        return {
            "status": "completed",
            "output": f"Feedback triaged: {title}; channel={channel}; summary={summary[:1000]}",
        }

    def _bind_task(self, object_id: str, task_id: str) -> None:
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            identity = connection.execute(
                "select data_json from runtime_entities where tenant_id = ? and entity_id = ? and entity_type = 'PACKAGE_DOMAIN_OBJECT'",
                (self.tenant_id, object_id),
            ).fetchone()
            if identity is None:
                raise PackageValidationError("Package Core identity disappeared before execution")
            data = json.loads(identity["data_json"])
            integration = dict(data.get("companyIntegration") or {}) | {"status": "RUNNING", "taskRef": task_id}
            data["companyIntegration"] = integration
            data["workContext"] = dict(data.get("workContext") or {}) | {
                "status": "working", "activity": "Core Task is running", "updatedAt": _now(),
            }
            connection.execute(
                "update runtime_entities set execution_ref = ?, data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ?",
                (f"task:{task_id}", json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, object_id),
            )

    def _finalize_failed_operation(
        self,
        workspace_id: str,
        object_id: str,
        task_id: str,
        execution_id: int,
        error: str,
    ) -> None:
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            object_row = connection.execute(
                "select company_id from workspace_package_objects where tenant_id = ? and workspace_id = ? and object_id = ?",
                (self.tenant_id, workspace_id, object_id),
            ).fetchone()
            if object_row is None:
                raise PackageScopeError("Package object disappeared before failure recording")
            identity = self._runtime_entity(
                connection, object_id, "PACKAGE_DOMAIN_OBJECT", object_row["company_id"], workspace_id,
            )
            data = identity["data"]
            data["companyIntegration"] = dict(data.get("companyIntegration") or {}) | {
                "status": "FAILED", "taskRef": task_id, "executionRef": str(execution_id),
                "error": error, "failedAt": at,
            }
            data["workContext"] = dict(data.get("workContext") or {}) | {
                "currentExecutorRef": None, "status": "failed", "activity": error, "updatedAt": at,
            }
            connection.execute(
                "update runtime_entities set execution_ref = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'NEW'",
                (
                    f"task:{task_id}:execution:{execution_id}", json.dumps(data, ensure_ascii=False), at,
                    self.tenant_id, object_id,
                ),
            )
            self._insert_activity(
                connection, workspace_id, COMPANY_OPERATE_ACTION + ".failed", object_id,
                {"taskRef": task_id, "executionRef": str(execution_id), "error": error}, at,
            )

    def _finalize_successful_operation(
        self,
        workspace_id: str,
        object_id: str,
        task_id: str,
        execution_id: int,
        artifact: dict,
        output: str,
    ) -> None:
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            object_row = connection.execute(
                "select * from workspace_package_objects where tenant_id = ? and workspace_id = ? and object_id = ?",
                (self.tenant_id, workspace_id, object_id),
            ).fetchone()
            if object_row is None:
                raise PackageScopeError("Package object disappeared before completion")
            package_object = self._object_projection(object_row)
            identity = self._runtime_entity(
                connection, object_id, "PACKAGE_DOMAIN_OBJECT", package_object["company_id"], workspace_id,
            )
            if identity["lifecycle_status"] != "NEW" or package_object["lifecycle_status"] != "NEW":
                raise PackageConflictError("Package object changed before Company result feedback")
            integration = dict(identity["data"].get("companyIntegration") or {})
            employee = self._runtime_entity(
                connection, integration["employeeRef"], "AI_EMPLOYEE", package_object["company_id"], workspace_id,
            )
            evidence_id = f"evidence-{uuid4()}"
            outcome_id = f"outcome-{uuid4()}"
            execution_ref = f"task:{task_id}:execution:{execution_id}"
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, parent_id, "
                "owner_ref, lifecycle_status, execution_ref, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, 'EVIDENCE', ?, ?, ?, ?, 'CURRENT', ?, 'UNVERIFIED', 'CURRENT', ?, ?, ?)",
                (
                    evidence_id, self.tenant_id, package_object["company_id"], workspace_id, object_id,
                    employee["entity_id"], execution_ref,
                    json.dumps({
                        "source": "TASK_EXECUTION", "taskRef": task_id, "executionRef": str(execution_id),
                        "artifactRefs": [artifact["artifact_id"]], "summary": output, "receivedAt": at,
                    }, ensure_ascii=False), at, at,
                ),
            )
            connection.execute(
                "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, parent_id, "
                "owner_ref, lifecycle_status, execution_ref, verification_status, evidence_condition, data_json, created_at, updated_at) "
                "values (?, ?, 'OUTCOME', ?, ?, ?, ?, 'CREATED', ?, 'UNVERIFIED', 'CURRENT', ?, ?, ?)",
                (
                    outcome_id, self.tenant_id, package_object["company_id"], workspace_id, object_id,
                    employee["entity_id"], execution_ref,
                    json.dumps({
                        "taskRef": task_id, "executionRef": str(execution_id),
                        "artifactRefs": [artifact["artifact_id"]], "evidenceRefs": [evidence_id],
                        "summary": output, "createdAt": at,
                    }, ensure_ascii=False), at, at,
                ),
            )
            evidence = self._runtime_entity(connection, evidence_id, "EVIDENCE", package_object["company_id"], workspace_id)
            outcome = self._runtime_entity(connection, outcome_id, "OUTCOME", package_object["company_id"], workspace_id)
            self._insert_link(connection, identity, "HAS_EVIDENCE", evidence, at)
            self._insert_link(connection, identity, "HAS_RESULT", outcome, at)
            self._insert_link(connection, evidence, "PRODUCED_BY", employee, at)
            self._insert_link(connection, outcome, "SUPPORTED_BY", evidence, at)

            business_data = dict(package_object["data"])
            business_data["status"] = "TRIAGED"
            if "responsibilityRef" in business_data:
                business_data["responsibilityRef"] = integration["responsibilityRef"]
            if "evidenceRef" in business_data:
                business_data["evidenceRef"] = evidence_id
            integration |= {
                "status": "COMPLETED", "taskRef": task_id, "executionRef": str(execution_id),
                "evidenceRefs": [evidence_id], "resultRefs": [outcome_id, artifact["artifact_id"]],
                "completedAt": at,
            }
            identity_data = identity["data"] | {
                "businessData": business_data,
                "companyIntegration": integration,
                "workContext": dict(identity["data"].get("workContext") or {}) | {
                    "currentExecutorRef": None,
                    "status": "completed",
                    "activity": "Company OS result and evidence recorded",
                    "resultRefs": [outcome_id, artifact["artifact_id"]],
                    "evidenceRefs": [evidence_id],
                    "updatedAt": at,
                },
            }
            connection.execute(
                "update runtime_entities set lifecycle_status = 'TRIAGED', execution_ref = ?, data_json = ?, "
                "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'NEW'",
                (
                    execution_ref, json.dumps(identity_data, ensure_ascii=False), at, self.tenant_id, object_id,
                ),
            )
            connection.execute(
                "update workspace_package_objects set lifecycle_status = 'TRIAGED', owner_ref = ?, data_json = ?, "
                "updated_at = ? where tenant_id = ? and object_id = ? and lifecycle_status = 'NEW'",
                (
                    employee["entity_id"], json.dumps(business_data, ensure_ascii=False), at,
                    self.tenant_id, object_id,
                ),
            )
            connection.execute(
                "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, trigger, actor, "
                "at, reason, company_id, workspace_id, evidence_refs_json, context_json) "
                "values (?, 'PACKAGE_DOMAIN_OBJECT', ?, 'NEW', 'TRIAGED', 'company_execution_completed', ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.tenant_id, object_id, employee["entity_id"], at,
                    "Task/Execution result fed back to Package object", package_object["company_id"], workspace_id,
                    json.dumps([evidence_id]), json.dumps({"taskRef": task_id, "resultRef": outcome_id}),
                ),
            )
            self._insert_activity(
                connection, workspace_id, COMPANY_OPERATE_ACTION, object_id,
                {
                    "taskRef": task_id, "executionRef": str(execution_id),
                    "evidenceRefs": [evidence_id], "resultRefs": [outcome_id, artifact["artifact_id"]],
                }, at,
            )

    def _insert_activity(self, connection, workspace_id: str, action_id: str, object_id: str, detail: dict, at: str) -> None:
        instance = self._instance(connection, workspace_id)
        connection.execute(
            "insert into workspace_package_activities values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                f"package-activity-{uuid4()}", instance["instance_id"], self.tenant_id,
                instance["company_id"], workspace_id, action_id, object_id,
                json.dumps(detail, ensure_ascii=False), at,
            ),
        )

    def resolve_company_integration(self, workspace_id: str, object_id: str) -> dict:
        with self.db.connect() as connection:
            instance = self._instance(connection, workspace_id)
            row = connection.execute(
                "select 1 from workspace_package_objects where tenant_id = ? and workspace_id = ? and object_id = ?",
                (self.tenant_id, workspace_id, object_id),
            ).fetchone()
            if row is None:
                raise PackageScopeError("Package object does not exist")
            return self._integration_projection(
                connection, object_id, instance["company_id"], workspace_id, strict=True,
            )

    def _integration_projection(
        self,
        connection,
        object_id: str,
        company_id: str,
        workspace_id: str,
        *,
        strict: bool,
    ) -> dict:
        identity = self._runtime_entity(
            connection, object_id, "PACKAGE_DOMAIN_OBJECT", company_id, workspace_id,
        )
        integration = dict(identity["data"].get("companyIntegration") or {})
        status = str(integration.get("status") or "NOT_STARTED")
        base = {
            "status": status,
            "resolvable": status != "NOT_STARTED",
            "objectIdentityRef": object_id,
            "objectLifecycleStatus": identity["lifecycle_status"],
        }
        if status == "NOT_STARTED":
            return base

        def linked(relation: str, expected_type: str) -> dict:
            links = self._links(connection, object_id, relation)
            if len(links) != 1:
                raise PackageValidationError(f"Company integration requires exactly one {relation} link")
            return self._runtime_entity(connection, links[0]["target_id"], expected_type, company_id, workspace_id)

        role = linked("HAS_CURRENT_RESPONSIBILITY", "ROLE_SLOT")
        employee = linked("HAS_CURRENT_EXECUTOR", "AI_EMPLOYEE")
        binding = linked("USES_CAPABILITY", "CAPABILITY_BINDING")
        if role["data"].get("assignedEmployeeRef") != employee["entity_id"] or employee["data"].get("roleSlotRef") != role["entity_id"]:
            raise PackageValidationError("Responsibility and Employee relationship drifted")
        review = binding["data"].get("supplyReview") or {}
        supply = self.company_runtime._resolve_supply(
            connection, review.get("source"), review.get("capabilityType"), review.get("capabilityId"),
        )
        current = (
            self.company_runtime._assess_supply(connection, supply) | {"runtimeMeta": supply["runtimeMeta"]}
            if supply else None
        )
        if (
            current is None
            or current["blockers"]
            or current["capabilityId"] != CORE_COMPANY_CAPABILITY
            or current["runtimeMeta"].get("handler") != CORE_COMPANY_CAPABILITY
            or any(
                review.get(key) != current.get(key)
                for key in ("source", "capabilityType", "capabilityId", "catalogUpdatedAt")
            )
        ):
            raise PackageValidationError("Capability can no longer be resolved as effective")

        task_id = str(integration.get("taskRef") or "")
        task = connection.execute(
            "select * from tasks where tenant_id = ? and company_id = ? and task_id = ?",
            (self.tenant_id, company_id, task_id),
        ).fetchone() if task_id else None
        if task is None and status in {"RUNNING", "FAILED", "COMPLETED"}:
            raise PackageValidationError("Company Task reference does not resolve")
        execution_id = str(integration.get("executionRef") or "")
        execution = connection.execute(
            "select * from executions where tenant_id = ? and task_id = ? and cast(execution_id as text) = ?",
            (self.tenant_id, task_id, execution_id),
        ).fetchone() if execution_id else None
        if execution_id and execution is None:
            raise PackageValidationError("Company Execution reference does not resolve")

        evidence_refs: list[str] = []
        result_refs: list[str] = []
        artifact_refs: list[str] = []
        reverse_resolved = True
        if status == "COMPLETED":
            evidence = linked("HAS_EVIDENCE", "EVIDENCE")
            outcome = linked("HAS_RESULT", "OUTCOME")
            evidence_refs = [evidence["entity_id"]]
            result_refs = [outcome["entity_id"]]
            artifact_refs = list(outcome["data"].get("artifactRefs") or [])
            if not artifact_refs:
                raise PackageValidationError("Company Result has no Artifact reference")
            for artifact_id in artifact_refs:
                artifact = connection.execute(
                    "select 1 from artifacts where tenant_id = ? and task_id = ? and artifact_id = ?",
                    (self.tenant_id, task_id, artifact_id),
                ).fetchone()
                if artifact is None:
                    raise PackageValidationError("Company Artifact reference does not resolve")
            for target_id, relation in (
                (role["entity_id"], "HAS_CURRENT_RESPONSIBILITY"),
                (employee["entity_id"], "HAS_CURRENT_EXECUTOR"),
                (binding["entity_id"], "USES_CAPABILITY"),
                (evidence["entity_id"], "HAS_EVIDENCE"),
                (outcome["entity_id"], "HAS_RESULT"),
            ):
                reverse_resolved = reverse_resolved and bool(connection.execute(
                    "select 1 from runtime_links where tenant_id = ? and target_id = ? and relation = ? and source_id = ?",
                    (self.tenant_id, target_id, relation, object_id),
                ).fetchone())
            if not reverse_resolved:
                raise PackageValidationError("Company relationship reverse resolution failed")
        if strict and status not in {"FAILED", "COMPLETED"}:
            raise PackageValidationError("Company integration is not in a terminal operating state")
        return base | {
            "resolvable": True,
            "responsibility": {"type": integration.get("responsibilityType"), "roleSlotRef": role["entity_id"]},
            "employee": {"employeeRef": employee["entity_id"], "name": employee["data"].get("name")},
            "capability": {
                "bindingRef": binding["entity_id"],
                **{key: value for key, value in current.items() if key != "runtimeMeta"},
            },
            "task": dict(task) if task else None,
            "execution": dict(execution) if execution else None,
            "evidenceRefs": evidence_refs,
            "resultRefs": result_refs,
            "artifactRefs": artifact_refs,
            "reverseResolved": reverse_resolved,
            "error": integration.get("error"),
        }

    def disable(self, workspace_id: str) -> dict:
        at = _now()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = self._instance(connection, workspace_id)
            identity = TenantContext.current_identity()
            if (identity.get("company_id") and identity["company_id"] != row["company_id"]
                or identity.get("role") and identity["role"].lower() not in {"ceo", "owner"}):
                raise PackageScopeError("workspace lifecycle does not belong to the current company owner")
            company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?",
                                         (self.tenant_id, row["company_id"])).fetchone()
            if identity.get("ceo_id") and (not company or identity["ceo_id"] != company["ceo_id"]):
                raise PackageScopeError("workspace lifecycle owner identity does not match")
            connection.execute(
                "update workspace_package_instances set status = 'DISABLED', updated_at = ? where tenant_id = ? and instance_id = ?",
                (at, self.tenant_id, row["instance_id"]),
            )
            active = connection.execute(
                "select 1 from workspace_package_instances where tenant_id=? and package_id=? and package_version=? and status='ACTIVE' limit 1",
                (self.tenant_id, row["package_id"], row["package_version"]),
            ).fetchone()
            if not active:
                connection.execute(
                    "update installed_workspace_packages set status = 'DISABLED', disabled_at = ? where tenant_id = ? and package_id = ? and version = ?",
                    (at, self.tenant_id, row["package_id"], row["package_version"]),
                )
            connection.execute(
                "update workspaces set status = 'PAUSED', updated_at = ? where tenant_id = ? and workspace_id = ?",
                (at, self.tenant_id, workspace_id),
            )
        return self.get_workspace(workspace_id, include_archived=True)

    def uninstall(self, workspace_id: str) -> dict:
        at = _now()
        trash = self.store_root / ".staging" / f"uninstall-{uuid4()}"
        moved_from: Path | None = None
        try:
            with self.db.connect() as connection:
                connection.execute("begin immediate")
                row = self._instance(connection, workspace_id, active=False)
                identity = TenantContext.current_identity()
                if (identity.get("company_id") and identity["company_id"] != row["company_id"]
                    or identity.get("role") and identity["role"].lower() not in {"ceo", "owner"}):
                    raise PackageScopeError("workspace lifecycle does not belong to the current company owner")
                company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?",
                                             (self.tenant_id, row["company_id"])).fetchone()
                if identity.get("ceo_id") and (not company or identity["ceo_id"] != company["ceo_id"]):
                    raise PackageScopeError("workspace lifecycle owner identity does not match")
                if row["status"] == "ARCHIVED":
                    raise PackageConflictError("workspace package instance is already uninstalled")
                connection.execute(
                    "update workspace_package_instances set status = 'ARCHIVED', updated_at = ? where tenant_id = ? and instance_id = ?",
                    (at, self.tenant_id, row["instance_id"]),
                )
                connection.execute(
                    "update workspaces set status = 'ARCHIVED', updated_at = ? where tenant_id = ? and workspace_id = ?",
                    (at, self.tenant_id, workspace_id),
                )
                referenced = connection.execute(
                    "select 1 from workspace_package_instances where tenant_id=? and package_id=? and package_version=? and status!='ARCHIVED' limit 1",
                    (self.tenant_id, row["package_id"], row["package_version"]),
                ).fetchone()
                if not referenced:
                    stored = Path(row["stored_path"])
                    expected = self.store_root / row["package_id"] / row["package_version"] / row["package_digest"]
                    if stored.resolve() != expected.resolve() or not stored.resolve().is_relative_to(self.store_root.resolve()):
                        raise PackageConflictError("uninstall asset path is outside the owned package store")
                    if stored.exists():
                        trash.parent.mkdir(parents=True, exist_ok=True)
                        os.replace(stored, trash)
                        moved_from = stored
                    connection.execute(
                        "update installed_workspace_packages set status = 'UNINSTALLED', uninstalled_at = ? where tenant_id = ? and package_id = ? and version = ?",
                        (at, self.tenant_id, row["package_id"], row["package_version"]),
                    )
        except Exception:
            if moved_from and trash.exists():
                moved_from.parent.mkdir(parents=True, exist_ok=True)
                os.replace(trash, moved_from)
            raise
        if trash.exists():
            shutil.rmtree(trash)
        return self.get_workspace(workspace_id, include_archived=True)

    def registry(self, *, include_archived: bool = False) -> list[dict]:
        clause = "" if include_archived else " and p.status = 'ACTIVE' and i.status = 'ACTIVE'"
        with self.db.connect() as connection:
            rows = connection.execute(
                "select p.package_id, p.version, p.digest, p.status, p.installed_at, p.disabled_at, p.uninstalled_at, i.instance_id, i.company_id, i.workspace_id, i.status as instance_status "
                "from installed_workspace_packages p join workspace_package_instances i "
                "on i.tenant_id = p.tenant_id and i.package_id = p.package_id and i.package_version = p.version "
                "where p.tenant_id = ?" + clause + " order by p.installed_at",
                (self.tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]
