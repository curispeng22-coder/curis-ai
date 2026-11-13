# WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001

Status: IMPLEMENTED / ACCEPTED (SCHEMA-STABLE SUBSTRATE ONLY)

Date: 2026-08-17

Owner: Workspace Engineering Core

Review Owner: Curis Runtime / Quality

## Single goal

Prove that an already Operating dynamic Workspace can move between schema-identical Package
versions and roll back without changing its Company/Business/Workspace/instance identity, business
data or real Company OS references.

This Issue implements only the safe boundary defined by
`docs/02_Architecture/WORKSPACE_ENGINEERING_EVOLVABLE_GAP_AUDIT.md`.

## Authorization baseline

- HEAD: `fe55ff5d585d92505e0188d506e2f2ea7c57625e`
- active DB: `data/curis.sqlite`, size `1232896`, mtime `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
  `integrity_check=ok`
- preserved dirty source/doc state is protected input; no reset, clean, broad stage or overwrite

## Allowed files

```text
backend/app/workspace_package_runtime.py
backend/app/workspace_package_api.py
backend/tests/test_workspace_package_runtime_p0.py
backend/tests/test_workspace_package_lifecycle_p1.py
docs/02_Architecture/WORKSPACE_ENGINEERING_EVOLVABLE_GAP_AUDIT.md
issues/WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001.md
reviews/WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001_review.md
docs/reviews/workspace-engineering-p1-lifecycle-2026-08-17/**
docs/00_Context/PRODUCT_DOCUMENT_POINTER.md       # final accepted fact only
docs/00_Context/CURRENT_STATE.md                  # final accepted fact only
docs/08_Change_Log/CHANGE_LOG.md                  # final accepted fact only
```

## Required implementation

1. Add pure update compatibility preview.
2. Same package ID, strictly newer version and exact normalized schema compatibility are mandatory.
3. Schema change fails closed as `MIGRATION_REQUIRED_NOT_SUPPORTED`.
4. Store the new version by immutable digest and preserve install/source provenance.
5. Switch the existing instance pin; never create a replacement Workspace or instance.
6. Preserve Business/Workspace identity, Package objects and all real Company OS entities/links.
7. Record append-only upgrade/rollback provenance and pre/post logical fingerprints.
8. Roll back only to the immediately previous applied, schema-identical version.
9. Preserve the same facts across full Runtime/Desktop restart.
10. Keep build-before-Package dynamic installation guarantees green.

## Acceptance

- success: `0.1.0 → 0.2.0`, same identities/data/Core refs, changed Package projection, durable
  provenance;
- restart: current `0.2.0` pin and Operating chain recover;
- rollback: `0.2.0 → 0.1.0`, same identities/data/Core refs, append-only provenance;
- second restart: rollback pin and Operating chain recover;
- incompatibility: schema-changing `0.3.0` is rejected without files, pin, data or link mutation;
- focused Package/P0.5/Runtime and bounded XHS/RD no-regression pass on isolated DB;
- packaged Desktop build-before-v2 proof passes without source edit/rebuild/reinstall after v2 exists;
- active DB size/mtime/hash/integrity remain exactly unchanged.

## Explicit exclusions

- real Schema/data migration;
- general or irreversible rollback;
- Team identity creation or Frozen Authority change;
- final UI;
- XHS/RD/Content Growth/TTK migration;
- Marketplace/update service/PKI;
- arbitrary Package code or external-side-effect compensation.

## Stop conditions

Stop if this proof requires changing Frozen Company OS/Shell Authority, inventing a Team primitive,
touching active SQLite, irreversible data operations, Shared Runtime refactor or business Workspace
migration.

**WORKSPACE ENGINEERING P1 SCHEMA-STABLE PACKAGE LIFECYCLE IMPLEMENTATION AUTHORIZED**

## Closure

- Implementation commits: `6d8712deb37fc3834f9ef31d15749e009c26ddf7`
- Definition / audit commit: `c4f52380abad3a97da72bbea546ae4cc79eafeb2`
- Focused + bounded no-regression: passed on repository-external isolated SQLite
- Real packaged Desktop: build-before-Package upgrade, incompatible-update failure, two restarts and
  rollback passed
- Active DB: baseline size/mtime/SHA-256 unchanged; `integrity_check=ok`
- Formal Review: `reviews/WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001_review.md`

This closes only the Issue's schema-identical lifecycle boundary. It does not accept general
migration, general rollback, Operating Team continuity or Workspace Engineering `Evolvable`.

**WORKSPACE ENGINEERING P1 SCHEMA-STABLE PACKAGE LIFECYCLE SUBSTRATE IMPLEMENTED / ACCEPTED**
