# BACKEND-TEST-DB-SAFETY-001

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-16
**Owner:** Curis main development / Backend test infrastructure

## Goal

Provide one Backend test-only database guard so every standard pytest collection and
`backend.tests` package import fails before `app.main` / `create_app()` can initialize a
database when:

- `CURIS_DB`, `CURIS_DB_PATH` or `CURIS_WORKSPACE_DB` is missing;
- the three variables do not resolve to one path; or
- the resolved path is the repository active SQLite or any repository-local database.

The accepted contract is:

```text
explicit three-variable isolated DB
-> same resolved path
-> outside repository
-> test import may continue
```

## Authority and baseline

- `docs/00_Context/CURRENT_STATE.md`
- `docs/04_Development/Curis_Development_Guide.md`
- `reviews/WORKSPACE-ENGINEERING-P0-001_review.md`
- `reviews/RD-PHASE-2B-ARTIFACT-REVIEW-001_review.md`
- Git baseline: `523ec49e0acd89de27cd803e0172e401d06a4a0d`

Pre-change SHA-256:

| File | SHA-256 |
| --- | --- |
| `backend/tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `backend/tests/conftest.py` | `676e6dac35305c09892f1b2ed508481deefd8526f5450ec0d533052460f33912` |
| `backend/tests/workspace_package_p0_db_guard.py` | `198f18fdd744e9dd721d71d88d8e5623c6746520ac73dfa7e7dc79584d836e21` |
| `backend/tests/test_workspace_package_runtime_p0.py` | `6288906c2b6a3baf65a881f6aa2af15a1d2c39593c99321a88217dc877434716` |

## Allowed Files

```text
backend/tests/db_safety.py
backend/tests/__init__.py
backend/tests/conftest.py
backend/tests/workspace_package_p0_db_guard.py
backend/tests/test_workspace_package_runtime_p0.py
backend/tests/test_backend_test_db_safety.py
issues/BACKEND-TEST-DB-SAFETY-001.md
reviews/BACKEND-TEST-DB-SAFETY-001_review.md
```

The specialized P0 guard may be deleted after all repository references use the unified
helper. No other test file requires migration because pytest collection is protected by
the root Backend `conftest.py`.

## Explicit exclusions

- production `Database` or `create_app()` DB resolution;
- changes to `CURIS_DB` production defaults, launchers or Desktop paths;
- schema, seed, migration or business Runtime changes;
- activity database cleanup, restore or mutation;
- RD 2B-2, Handoff, P7, XHS, TTK or Workspace Package behavior;
- generalized environment/config framework;
- stage/push of unrelated Preserved Development Baseline files.

## Acceptance

1. Missing any required variable fails before test-module import.
2. Three variables resolving to different paths fail.
3. Active `data/curis.sqlite` and any repository-local DB fail.
4. One repository-external temporary SQLite path passes.
5. `backend.tests` package import applies the same guard before importing `app.main`.
6. Standard pytest collection applies the guard before test import / `create_app()`.
7. Workspace Package P0 uses the unified helper; no specialized guard logic remains.
8. Focused guard, RD Artifact Review and shared Runtime regression pass with an isolated
   SQLite; Workspace Package P0 collection proves it consumes the global pytest guard.
   Any pre-existing Package business-test drift must be recorded rather than repaired in
   this hygiene Issue.
9. Active DB SHA/size/mtime are unchanged throughout verification.

## Commit boundary

Only Allowed Files may be staged. One bounded local commit is allowed. No push.

## Implementation result

- `backend/tests/db_safety.py` is the sole three-variable guard implementation.
- Backend pytest collection invokes it from the root `conftest.py` before test import.
- `backend.tests` package import invokes the same helper before an importing script can
  reach `app.main` / module-level `create_app()`.
- Workspace Package P0 no longer owns or duplicates guard code.
- Production database resolution, schema and business Runtime are unchanged.
