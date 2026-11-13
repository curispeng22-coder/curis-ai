# SHARED-EMPLOYEE-ORGANIZATION-PROJECTION-001

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-17
**Owner:** Curis Shared Runtime

## Goal

Enrich Runtime `AI_EMPLOYEE` reads with existing Company Employee/Department/Project affiliation
facts only when the persisted employee identifier matches exactly in the same tenant and Company.

## Allowed Files

```text
backend/app/shared_workspace_projection.py
backend/tests/test_shared_workspace_projection.py
frontend/components/workspace/SharedEmployeeWorkArea.js
issues/SHARED-EMPLOYEE-ORGANIZATION-PROJECTION-001.md
reviews/SHARED-EMPLOYEE-ORGANIZATION-PROJECTION-001_review.md
```

## Explicit exclusions

- name/role fuzzy matching;
- new identity map, schema, migration or backfill;
- writes to Employee, Department, Team, affiliation or Workspace;
- domain page migration, Frozen changes, active DB or provider behavior.

## Acceptance

1. Exact same-ID, same-tenant, same-Company Employee resolves organization facts.
2. Primary Department and persisted secondary affiliations are readable.
3. Non-matching Runtime Employee remains unresolved; it is not treated as an error or guessed.
4. Cross-Company same-ID data cannot resolve.
5. Existing responsibility/executor/result truth and restart behavior remain unchanged.

## Implementation result

- Runtime `AI_EMPLOYEE` identity remains authoritative for responsibility and execution.
- Existing Company Employee facts are attached only after exact ID, tenant and Company matching.
- Primary Department and persisted Department/Project affiliations are read-only projections.
- An unresolved or cross-Company employee returns `organization_record = null`; no identity is guessed.
- No schema, migration, backfill, write path or Domain lifecycle changed.
