# SHARED-EMPLOYEE-WORK-AREA-001

**Status:** IMPLEMENTED / ACCEPTED AS SHARED CAPABILITY
**Date:** 2026-08-17
**Owner:** Curis Shared Workspace UI

## Goal

Provide one reusable Shared Work Area that consumes the accepted Shared Workspace read model and
renders real Employee rows, Employee Detail, Result Reference entry points and a truthful Composer
capability summary. It must not create conversation, execution or capability facts.

## Authority

- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` (Frozen, Delta-X9/X10/X12)
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md` (Frozen)
- `SHARED-BUSINESS-WORKSPACE-READ-MODEL-001` accepted read model

## Allowed Files

```text
backend/app/shared_workspace_projection.py
backend/tests/test_shared_workspace_projection.py
frontend/components/workspace/SharedEmployeeWorkArea.js
frontend/lib/sharedWorkspaceApi.js
frontend/tests/sharedEmployeeWorkArea.test.mjs
issues/SHARED-EMPLOYEE-WORK-AREA-001.md
reviews/SHARED-EMPLOYEE-WORK-AREA-001_review.md
```

## Explicit exclusions

- RD/XHS/TTK/Package page integration or visual redesign;
- provider-native conversation, send command, mode or permission implementation;
- fake Employee, conversation, activity, result or effective access state;
- schema, Runtime writes, new state, Workflow/DAG or Frozen authority changes;
- active DB access, broad stage/commit, push or unrelated dirty files.

## Acceptance

1. Employee rows use real Employee identity, role, responsibility and three-state UI projection.
2. Avatar/name opens Utility Employee Detail; there is no duplicate Detail button.
3. Expand/collapse is local UI state and never mutates Runtime.
4. A single real working Employee may default expanded; no status forces later UI changes.
5. Conversation area shows only persisted activity/result references; no generated messages.
6. Result Reference delegates to the scoped Utility read API.
7. Composer exposes real model/agent/capability/access facts and stays disabled without a real send handler.
8. Employee Detail contains organization context, responsibility, capability/work style and recent results.
9. Frontend focused checks and backend read-model regression pass.

## Implementation result

- Shared Employee Work Area, Employee Detail and Result Utility components are available for
  Workspace adoption.
- A read-only frontend API consumes the scoped Shared Runtime endpoints.
- Employee Detail now includes exact Company/Workspace organization context and recent result refs.
- No Workspace page was migrated in this bounded slice; availability is not represented as domain adoption.
