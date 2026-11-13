# Integration Candidate Review

Review date: 2026-07-30

Branch: `integration/curis-v1`

Baseline: `1f295c06 fix: complete assistant live model chain`

Conclusion: **ACCEPT — CURRENT INTEGRATION SCOPE**

## Findings

- Employee Affiliation backend closure is present: model/schema, tenant-scoped
  service, POST/GET/DELETE routes, employee cleanup, CRUD and isolation tests.
- Schema governance is present: `PRAGMA user_version = 1`,
  `schema_migrations`, fresh/existing database convergence, and fail-closed
  protection for non-empty retired tables.
- No frontend files changed.
- Project Delete is intentionally not implemented or changed in this candidate.
- No `main` merge is included.

## Changed Files

- `.gitignore`
- `backend/app/database.py`
- `backend/app/employee_affiliations.py`
- `backend/app/employee_templates.py`
- `backend/app/main.py`
- `backend/tests/test_integration_baseline_fixes.py`
- `reviews/20260730_integration_candidate_review.md`

## Verification Evidence

Focused integration checks:

```text
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python -m pytest -q \
  backend/tests/test_integration_baseline_fixes.py

4 passed
```

Backend regression:

```text
PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python -m pytest -q backend/tests

1184 passed, 2 skipped
```

Database:

```text
PRAGMA user_version = 1
schema_migrations = 1|integration-v1-schema-baseline
PRAGMA integrity_check = ok
```

Repository:

```text
git diff --check = PASS
```

Warnings are existing FastAPI/Python deprecation warnings; no test failed.

## Remaining Risks

- The frontend's existing Project Delete call still has no backend route.
  Project Delete remains a separately deferred Restrict/Soft Delete contract
  and is outside this candidate.
- This review accepts the current Employee Affiliation and Schema Governance
  scope. Promotion to `main` remains a separate owner decision.
- No live external model invocation was performed; existing Assistant Runtime
  behavior was covered by backend regression only.

## Decision

**Accepted as the `integration/curis-v1` candidate for the current integration
scope.** Project Delete remains explicitly deferred. No merge to `main` was
performed.
