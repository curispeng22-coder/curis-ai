# WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001

Status: IMPLEMENTED / ACCEPTED

Date: 2026-08-16

Owner: Workspace Engineering Core

Review Owner: Curis Runtime / Quality

## Goal

Prove that a dynamically installed `customer-feedback-office` is not a Package island and runs one
real Company OS loop:

```text
CustomerFeedback
→ real Responsibility
→ real Employee
→ existing Capability
→ real Task / Execution
→ Evidence / Result Reference
→ CustomerFeedback state/result update
→ full Desktop restart with every reference still resolvable
```

Acceptance requires both `Company Integrated` and `Operating` under
`WORKSPACE_ENGINEERING_END_TO_END_ACCEPTANCE_CONTRACT.md`.

## Frozen implementation contract

`docs/02_Architecture/WORKSPACE_PACKAGE_COMPANY_OS_IDENTITY_REFERENCE_CONTRACT.md`

Development cannot start until that contract is Frozen. The contract is subordinate to and does
not modify existing Frozen Authority.

## Input baseline

- HEAD at authorization: `df9ebbe07882074cf0cb60c76b424def07302d19`.
- Preserved dirty snapshot digest: `sha256:c179854371e37734bd007406fd65e812226d17a214abff3cc29da45e011486d6`.
- Repository active DB at authorization: `data/curis.sqlite`, size `1232896`, mtime
  `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
  `integrity_check=ok`.
- Dirty G2/G3/Shared Runtime/Product wave remains protected input. No reset, clean, overwrite,
  broad stage or mixed commit is allowed.

## Allowed files

```text
backend/app/workspace_package_runtime.py
backend/app/workspace_package_api.py
backend/tests/test_workspace_package_runtime_p0.py
backend/tests/test_workspace_package_company_integration_p05.py
frontend/components/workspace/InstalledWorkspaceRuntime.js
frontend/lib/workspacePackageApi.js
frontend/tests/workspacePackageRuntime.test.mjs
docs/02_Architecture/WORKSPACE_ENGINEERING_END_TO_END_ACCEPTANCE_CONTRACT.md
docs/02_Architecture/WORKSPACE_ENGINEERING_P05_COMPANY_INTEGRATION_AUDIT.md
docs/02_Architecture/WORKSPACE_PACKAGE_COMPANY_OS_IDENTITY_REFERENCE_CONTRACT.md
issues/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001.md
reviews/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001_review.md
docs/reviews/workspace-engineering-p05-2026-08-16/**
docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
docs/00_Context/CURRENT_STATE.md                  # accepted fact only
docs/08_Change_Log/CHANGE_LOG.md                  # contract freeze / accepted fact only
```

## Required implementation

1. Newly created Package objects receive a same-ID Core Runtime identity in the existing
   `runtime_entities` table. The P0 table remains a renderer projection, not a second identity.
2. `owner_ref`, `responsibilityRef` and `evidenceRef` reject Package-authored non-empty values and
   become read-only projections of validated Core facts.
3. One Core command resolves an existing Role Slot/Responsibility, Employee and active Capability
   Binding without accepting direct relationship IDs from Package data.
4. The command creates a real existing Task/Execution and Artifact through ResultStore.
5. Successful execution creates existing Runtime Evidence/Outcome and Core-owned links, then
   transitions `CustomerFeedback NEW → TRIAGED`.
6. Failed execution creates real Task/Execution failure truth, keeps `NEW` and creates no successful
   Evidence/Outcome relationship.
7. One resolver proves forward and reverse relationships, including native Task/Execution/Artifact
   resolution, before and after full Desktop restart.
8. Generic Desktop projection shows Core-resolved integration truth. No Package-specific compiled
   route/component is added.

## Acceptance gates

1. Identity contract is Frozen before the first code edit.
2. Fake Package-authored relationship strings fail closed.
3. Wrong-type/cross-scope/stale Core facts fail closed without Task/state residue.
4. Success path contains real IDs for Role Slot, Employee, Capability Binding/catalog supply,
   Task, Execution, Artifact, Evidence and Outcome.
5. Failure path contains a real failed Task/Execution and no false `TRIAGED`/Evidence/Outcome.
6. Full Desktop restart resolves the same chain and reverse links from isolated SQLite.
7. Focused Package/Runtime and bounded XHS/RD no-regression checks pass.
8. Repository active DB hash, mtime, integrity and Package-table absence remain unchanged.
9. Real packaged Desktop evidence is recorded; backend-only success is insufficient.

## Explicit exclusions

- Handoff and P7.
- Shared Runtime refactor or Frozen Authority changes.
- XHS/RD/TTK migration.
- Package update, migration, rollback, Marketplace, signing or Evolution.
- arbitrary extensions or a second Company OS primitive/store.

## Stop conditions

Stop if a legal same-ID Package Object ↔ Core identity cannot be established, if implementation
requires modifying existing Frozen Authority or refactoring Shared Runtime, if active SQLite is
touched, or if scope expands into excluded systems.

## Closure

- Formal Review: `reviews/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001_review.md`
- Desktop evidence: `docs/reviews/workspace-engineering-p05-2026-08-16/README.md`
- Highest accepted layer: `Operating`
- Handoff: `NOT REQUIRED` — the same responsibility holder completes the bounded triage loop.
- Decision P7: `NOT REQUIRED` — no CEO judgment, external commitment or governed side effect occurs.
- Later layer: `Evolvable NOT ACCEPTED / NOT IMPLEMENTED`.

**WORKSPACE ENGINEERING P0.5 IMPLEMENTED / ACCEPTED**
