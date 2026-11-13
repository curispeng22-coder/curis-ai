# SHARED-EMPLOYEE-ORGANIZATION-PROJECTION-001 Review

**Status:** IMPLEMENTED / ACCEPTED
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-17
**Issue:** `issues/SHARED-EMPLOYEE-ORGANIZATION-PROJECTION-001.md`

## Decision

The bounded organization projection is accepted. A Runtime `AI_EMPLOYEE` may expose an existing
Company Employee, primary Department and persisted Department/Project affiliations only when its
identifier resolves exactly inside the same tenant and Company. Missing identity links remain
unknown rather than inferred.

## Runtime evidence

- exact current-Company Employee ID: `identity_status = EXACT_ID_MATCH`;
- primary Department and Project affiliation are returned from persisted records;
- same Runtime Employee ID present only in another Company returns no organization record;
- responsibility holder, current executor, system activity and result references are unchanged;
- restart reads the same projection from repository-external isolated SQLite.

## Verification

Repository-external database:

`/tmp/curis-shared-org-projection.LFnQ6i/runtime.sqlite`

```text
Backend focused/no-regression: 7 passed
Frontend Shared Employee Work Area: 4 passed
Focused ESLint: pass
git diff --check: pass
```

Backend coverage includes Shared projection, RD real execution, XHS Calendar/Note Runtime and
Workspace Package Company integration.

## Active database truth

Before and after verification:

```text
size: 1232896
mtime: 1786873339
SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
integrity_check: ok
foreign_key_check: 0
```

The active database was not initialized, migrated, cleaned or modified.

## Scope confirmation

- no fuzzy name or role matching;
- no identity map, schema, migration or backfill;
- no Company/Employee/Department/Project/Workspace write;
- no RD/XHS/TTK or Workspace Package lifecycle change;
- no Frozen Authority or provider behavior change.

## Remaining boundary

The current repository still has no canonical persisted bridge between legacy Company Employees
and Runtime `AI_EMPLOYEE` records when identifiers differ. Solving that requires a separately
approved identity contract; this Issue intentionally does not guess or create one.
