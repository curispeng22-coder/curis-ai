# WORKSPACE-ENGINEERING-P0-001：Declarative Workspace Package Runtime P0

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-16
**Owner:** Workspace Engineering Core
**Review Owner:** Curis Quality / Runtime Acceptance
**Authority:** Workspace Engineering Methodology / Technical Direction `APPROVED CANDIDATE`; `WORKSPACE_ENGINEERING_P0_DEFINITION.md`

## Goal

Prove that an already-built Curis Desktop can receive and run a previously unknown declarative package without source changes, rebuild or App reinstall:

```text
com.curis.sample.customer-feedback-office@0.1.0
→ install
→ dynamic Workspace navigation
→ declarative Main / Context / Utility
→ real CustomerFeedback in SQLite
→ full Desktop restart recovery
→ uninstall removes navigation
→ business data retained as read-only archive
```

Code existing before this proof is not acceptance. The sample package must be introduced only after the acceptance build is complete.

## Input baseline

- Branch / HEAD at Issue start: `main @ 6f03b5772e3f457e3b423b8b2445138e6715ce3b`.
- Preserved dirty snapshot digest: `sha256:7696b580d90b72af7a8fa4d14af0403175de664ee0416bc30690f0d42c3d8d68` from `git status --porcelain=v1 -uall`.
- The dirty G2 / G3 / Shared Runtime / Product wave is protected input, not this Issue's output. No reset, clean, overwrite, bulk stage or mixed commit is allowed.
- Active database guard at Issue start: `data/curis.sqlite`, size `1175552`, sha256 `d99348dfae4fe9d4468edb1a6f5f9ef1fd0d3dacf86d6fc506303196321bf434`. It is read-only for this Issue.
- All tests and Desktop evidence use a unique isolated App Data root, isolated SQLite and isolated Package Store.

## Technical boundary

- Reuse the existing `Database`, `TenantContext`, `companies`, `workspaces`, Runtime Foundation schema, Trusted Gateway, SQLite and `WorkspacePaneShell`.
- Add one independent package substrate beside the compiled RD / XHS / TTK Runtime. Do not widen their business-type registry or migrate their data.
- A package is data only: strict JSON manifest, surface declarations and local domain schema. No package code, HTML, SQL, credentials or executable hooks.
- Package action declaration is only a request to use a finite Core action. It is not an OS, Connector, Capability or Computer Access grant.
- P0 provenance is local source path + immutable digest + install timestamps and version pin. It is not a signature PKI or publisher trust service.

## Allowed files

```text
backend/app/workspace_package_runtime.py
backend/app/workspace_package_api.py
backend/app/main.py                                  # router registration hunk only
backend/tests/test_workspace_package_runtime_p0.py
backend/tests/workspace_package_p0_db_guard.py
frontend/lib/workspacePackageApi.js
frontend/components/terra/TerraSidebar.js           # Registry projection hunk only
frontend/components/workspace/InstalledWorkspaceRuntime.js
frontend/app/ceo-office/workspace/installed/[workspaceId]/page.js
frontend/tests/workspacePackageRuntime.test.mjs
issues/WORKSPACE-ENGINEERING-P0-001.md
reviews/WORKSPACE-ENGINEERING-P0-001_review.md
docs/reviews/workspace-engineering-p0-2026-08-16/**
docs/00_Context/CURRENT_STATE.md                     # final accepted fact only
docs/00_Context/PRODUCT_DOCUMENT_POINTER.md          # final Issue/Review registration only
docs/04_Development/WORKSPACE_ENGINEERING_P0_IMPLEMENTATION_PLAN.md
docs/08_Change_Log/CHANGE_LOG.md                     # final accepted change only
```

Acceptance-only artifacts may be created under an isolated `/tmp/curis-workspace-engineering-p0-*` root after the Desktop build. They are not source inputs and are not committed.

## Explicit exclusions

- XHS, RD, TTK or Content Growth business logic, routes, data migration or package conversion.
- Existing mixed Shared Runtime restructuring, `WorkspaceRuntime` business-type widening, Product wave cleanup or Preserved Development Baseline repair.
- Arbitrary JavaScript / Python / Shell / SQL / Rust extension, dynamic Tauri plugin, Workflow Engine, DAG Builder, Marketplace or low-code platform.
- Package update, schema migration, rollback engine, signing PKI, publisher service, key rotation or third-party trust.
- New Employee, Responsibility, Capability, Decision P7, Task, Evidence, Artifact, Result or Computer Access system.
- Full Computer Access, permission auto-grant, credential persistence or Connector activation.
- Workspace Engineering product/UX.

## Required implementation

1. Strict Package validator: known fields/files/components/actions only; safe relative paths; file count/size limits; Core compatibility; schema validation; no symlinks or executables.
2. Local atomic Package Store and tenant-scoped Installed Package Registry with digest/provenance, version pin and restart recovery.
3. Template materialization into the existing `workspaces` identity plus a package instance record.
4. Tenant / Company / Workspace-scoped generic package domain object and activity record; P0 action allowlist contains only `core.domain-object.create`.
5. Registry-driven second-level Workspace navigation and one generic installed-package route that reuses `WorkspacePaneShell` for Main / Context / Utility.
6. Disable/uninstall truth: navigation hidden; active files removed on uninstall; workspace/instance archived; manifest, schema, provenance, objects and activities retained read-only.

## Acceptance gates

1. Pre-package source/build scan contains no sample package ID, workspace type or Chinese office label.
2. Build/package digest and build completion time precede creation of the sample package directory.
3. Invalid path/action/schema/Core compatibility and conflicting duplicate installs fail closed with no Registry/files residue.
4. Installed package appears in dynamic navigation and opens all three declarative panes without package-specific compiled route or component.
5. UI/Core action creates one real `CustomerFeedback` with object ID, tenant/company/workspace scope, lifecycle state, owner/ref, timestamps and activity.
6. Full Desktop stop/start restores the same registry, instance, object and activity from isolated SQLite.
7. Uninstall removes navigation and active files; direct active route fails; archived business data and provenance remain in SQLite.
8. `pragma integrity_check` is `ok`, `pragma foreign_key_check` is empty, and the active `data/curis.sqlite` hash/mtime do not change.
9. Focused Package tests, frontend renderer test, frontend production build, Runtime Foundation persistence/scope, XHS accepted slice, RD accepted Phase 0/1 slice and ADR-0046 Computer Access truth checks pass without new regression.
10. A real packaged Desktop screenshot/log/API/SQLite evidence chain proves build-before-package. API success or source existence alone is insufficient.

## Stop conditions

Stop without widening this Issue if completion requires changing Frozen Authority, migrating/refactoring XHS/RD/TTK, destroying the preserved baseline, arbitrary extensions/Marketplace, or an architecture change that cannot remain inside the Allowed Files.

**WORKSPACE ENGINEERING P0 IMPLEMENTATION AUTHORIZED**

**WORKSPACE ENGINEERING P0 ACCEPTANCE REQUIRED**

## Blocker record — 2026-08-16

The focused regression command imported `backend/app/main.py` without setting the required isolated DB environment trio. The module-level `app = create_app()` therefore opened the default `data/curis.sqlite`, and the newly registered Package router created its four empty P0 tables there.

Observed after the command:

- active DB size/hash changed from `1175552 / d99348df...` to `1232896 / a5051402...`;
- `installed_workspace_packages`, `workspace_package_instances`, `workspace_package_objects` and `workspace_package_activities` each contain `0` rows;
- `pragma integrity_check = ok`; `pragma foreign_key_check` returns no rows;
- no process held the file when checked.

No table was dropped, no VACUUM/restore was attempted, and no active business row was intentionally changed. Exact byte restoration is impossible without a verified pre-command database copy. P0 Desktop build-before-package acceptance and commits are stopped until the owner supplies a verified backup or explicitly authorizes a bounded logical repair and accepts that the original hash cannot be recovered.

**WORKSPACE ENGINEERING P0 NOT ACCEPTED**

## Guard repair resolution — 2026-08-16

Owner authorization permitted a bounded logical repair. Before repair, the four P0 tables were reconfirmed at zero rows, their schema was recorded, the active database passed integrity/foreign-key checks, and a SQLite backup was created at:

`data/backups/curis-before-workspace-p0-guard-repair-20260816.sqlite`

The repair transaction verified the exact expected columns and zero rows, then dropped only these tables in dependency order: `workspace_package_activities`, `workspace_package_objects`, `workspace_package_instances`, `installed_workspace_packages`.

Before/after logical fingerprints for every non-target schema object and all 96 non-target tables / 391 rows were identical:

- non-target schema: `91e6b246db77ac3d4ceed03c81d03d9548f54c2989be9e101efeef4a8b0a133c`;
- non-target data: `05a671d8030e0dcbf6b96c4cb2b4a19c740947f18b6157ef32e4c0342e645b39`.

Post-repair integrity is `ok`, foreign-key check is empty, and the four tables are absent. The original byte hash was not and cannot be restored; the post-repair byte hash is `c838f41deaf643b6a0ef55aa63b7467dbaaf9bb6d3a0e5a425e3d459f7ca53f0`.

`workspace_package_p0_db_guard.py` now requires all three DB environment variables to resolve to one database outside the repository before P0 regression imports may continue.

**ACTIVE SQLITE LOGICAL REPAIR VERIFIED / BYTE HASH NOT RESTORED**

## Final acceptance — 2026-08-16

The packaged Desktop was built before `com.curis.sample.customer-feedback-office@0.1.0` existed. The sample Package was introduced only after build completion and was then installed through the packaged Runtime without source modification, rebuild or App reinstall.

The same App binary proved dynamic navigation, declarative Main / Context / Utility, UI creation and SQLite persistence of one real `CustomerFeedback`, complete Desktop stop/start recovery, fail-closed unknown action handling, uninstall navigation/file removal and read-only retention of Package provenance, object and activity.

Focused/shared regression passed with isolated database environment truth: backend `25 passed`, frontend `11 passed`, and the pre-Package production/Desktop build passed. The active database stayed at post-repair SHA-256 `c838f41deaf643b6a0ef55aa63b7467dbaaf9bb6d3a0e5a425e3d459f7ca53f0`, remained integral, and contained none of the four Package tables throughout final acceptance.

Formal record: `reviews/WORKSPACE-ENGINEERING-P0-001_review.md`

Evidence: `docs/reviews/workspace-engineering-p0-2026-08-16/README.md`

**WORKSPACE ENGINEERING P0 ACCEPTED**
