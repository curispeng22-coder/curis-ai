# BACKEND-TEST-DB-SAFETY-001 Review

**Status:** IMPLEMENTED / ACCEPTED
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-16
**Issue:** `issues/BACKEND-TEST-DB-SAFETY-001.md`

## Decision

Backend test database safety is unified and accepted.

One test-only helper now enforces:

```text
CURIS_DB + CURIS_DB_PATH + CURIS_WORKSPACE_DB
must all exist
must resolve to one path
must resolve outside the repository
```

The check runs before standard pytest test-module import and before `backend.tests` package
imports can reach `app.main` / module-level `create_app()`.

## Changed files

- `backend/tests/db_safety.py`: single guard implementation;
- `backend/tests/__init__.py`: direct test-package import bootstrap;
- `backend/tests/conftest.py`: pytest bootstrap now calls the generic helper;
- `backend/tests/workspace_package_p0_db_guard.py`: removed specialized duplicate;
- `backend/tests/test_workspace_package_runtime_p0.py`: removed per-Issue guard ownership;
- `backend/tests/test_backend_test_db_safety.py`: focused missing/mismatch/active/repository/
  isolated/import-order regression;
- bounded Issue and this Review.

No production file, production DB resolution, schema, seed, Runtime or business behavior
was modified.

## Acceptance evidence

### Contract matrix

| Case | Result |
| --- | --- |
| any required variable missing | fail-fast before test import |
| three paths differ | fail-fast |
| active `data/curis.sqlite` | fail-fast before `app.main` import |
| another repository-local SQLite | fail-fast |
| one repository-external temporary SQLite | accepted |
| direct `backend.tests` import without variables | fail-fast before `backend.app.main` |

### Focused and shared regression

Isolated database:

`/tmp/curis-backend-test-db-safety-final.EUzWld/runtime.sqlite`

```text
11 passed
  backend/tests/test_backend_test_db_safety.py
  backend/tests/test_rd_artifact_review.py
  backend/tests/test_runtime_foundation_state_contracts.py

Workspace Package P0 collect-only: 1 test collected
python py_compile: pass
git diff --check: pass
```

The focused tests spawn real child Python/pytest processes with the three variables removed
or pointed at the active database, then prove collection/import fails and the active DB
fingerprint stays unchanged.

## Active database truth

Before and after all accepted checks:

```text
size: 1232896
mtime: 1786873339
SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
```

The active database was not opened for initialization, restored, cleaned or modified.

## Recorded external regression

The current mixed-source Workspace P0.5 Runtime has independently made Core reference
fields such as `evidenceRef` read-only. The historical Workspace Package P0 business test
still writes `evidenceRef`, so its full execution currently fails with:

`PackageValidationError: Core reference field is read-only: evidenceRef`

This failure occurs after the unified DB guard has passed and is unrelated to guard
selection, import order or database isolation. The hygiene Issue does not alter Package
business semantics or rewrite that historical test to hide the drift. P0 test collection
under the unified guard succeeds; the business drift remains owned by the active P0.5
Issue.

## Scope confirmation

- no production DB resolution change;
- no active DB mutation;
- no RD 2B-2, Handoff or P7;
- no XHS/TTK or Workspace behavior change;
- no specialized guard logic remains in current Backend tests;
- no push.

## Final result

**BACKEND TEST DB SAFETY IMPLEMENTED / ACCEPTED**
