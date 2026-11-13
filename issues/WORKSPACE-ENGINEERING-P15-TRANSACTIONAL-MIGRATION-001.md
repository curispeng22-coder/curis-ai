# WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001

Status: IMPLEMENTED / ACCEPTED (BOUNDED RENAME MIGRATION ONLY)

Date: 2026-08-17

Owner: Workspace Engineering Core

Review Owner: Curis Runtime / Quality

## Single goal

Prove that an already Operating dynamic Workspace can transactionally migrate Package-owned
business JSON data across one declared reversible schema rename while preserving every authoritative
Core identity/reference, recovering atomically from failure, restarting and continuing operation.

The implementation is bounded by
`docs/02_Architecture/WORKSPACE_ENGINEERING_P15_TRANSACTIONAL_MIGRATION_AUDIT.md`.

## Authorization baseline

- HEAD: `a9a9105a5e68a840be78115a3aedff2416924f79`
- P1 schema-stable lifecycle remains accepted and is not reworked
- active DB: `data/curis.sqlite`, size `1232896`, mtime `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
  `integrity_check=ok`
- preserved dirty work is protected input; no reset, clean, broad stage or overwrite

## Allowed files

```text
backend/app/workspace_package_runtime.py
backend/tests/test_workspace_package_transactional_migration_p15.py
docs/02_Architecture/WORKSPACE_ENGINEERING_P15_TRANSACTIONAL_MIGRATION_AUDIT.md
issues/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001.md
reviews/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001_review.md
docs/reviews/workspace-engineering-p15-migration-2026-08-17/**
docs/00_Context/PRODUCT_DOCUMENT_POINTER.md       # final accepted fact only
docs/00_Context/CURRENT_STATE.md                  # final accepted fact only
docs/08_Change_Log/CHANGE_LOG.md                  # final accepted fact only
```

## Required implementation

1. Validate the optional bounded migration manifest and include it in Package digest/provenance.
2. Add pure preflight with exact affected object count and transformed-data validation.
3. Record durable PREPARED/APPLIED/FAILED migration journal and exact Package-owned checkpoint.
4. Transform object row and same-ID Runtime projection in one SQLite transaction.
5. Activate package/schema/projection pin only inside the same transaction.
6. Inject a real SQLite mid-migration failure in tests and prove zero partial data/pin/schema/event.
7. Reject irreversible migration before Package Store or database mutation.
8. Roll back with declared down migration and exact checkpoint verification.
9. Recover migration/rollback and real Company OS references across full Desktop restart.
10. Continue operating after migration using the migrated schema.

## Acceptance

- v1 real business data and Company OS operating chain exist before migration;
- v2 renames persisted `customerRef → accountRef` and bumps the object schema version;
- IDs and all Core relationships remain exact;
- failure after at least one row update rolls back all rows and retains the v1 office;
- reversible down migration restores exact checkpoint data and v1 pin;
- irreversible declaration fails closed without candidate/store/journal residue;
- restart recovers v2 and continued operation; later rollback/restart recovers v1;
- focused Package/P0.5/P1/P1.5 and bounded RD/XHS/Shared Runtime regressions pass on isolated DB;
- active DB size/mtime/hash/integrity remain exactly unchanged.

## Explicit gaps / exclusions

- authoritative Operating Team identity (Core proposal required);
- physical/arbitrary SQLite migration, general migration language or arbitrary code;
- irreversible data migration/checkpoint restore;
- multi-instance install/cardinality changes;
- history GC/uninstall redesign;
- XHS/RD/TTK migration;
- Marketplace/PKI/update distribution/UI;
- Frozen Authority or Shared Runtime Primitive changes.

## Stop conditions

Stop the affected sub-item if it requires a Team primitive, Frozen Authority change, Shared Runtime
refactor, active DB access, irreversible operation or Domain migration. Continue independent safe
P1.5 work.

**WORKSPACE ENGINEERING P1.5 BOUNDED TRANSACTIONAL MIGRATION IMPLEMENTATION AUTHORIZED**

## Closure

- Definition / audit commit: `948ead875dba6d2bc933b87ac3096547a1bedacb`
- Implementation commit: `3276538c6aefc742158f441488e7858549db864c`
- Focused + bounded no-regression passed on repository-external isolated SQLite
- Real packaged Desktop build-before-Package migration/failure/restart/continue/rollback/restart
  proof passed
- Active DB exact baseline size/mtime/SHA-256 preserved; `integrity_check=ok`
- Formal Review: `reviews/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001_review.md`

This closes only reversible Package-owned JSON field rename migration. It does not accept
authoritative Team continuity, physical/general/irreversible migration, multi-instance lifecycle or
Full Evolvable.

**WORKSPACE ENGINEERING P1.5 TRANSACTIONAL PACKAGE DOMAIN DATA MIGRATION SUBSTRATE IMPLEMENTED / ACCEPTED**
