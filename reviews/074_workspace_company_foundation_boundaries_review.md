# Review 074: Workspace Company Foundation Boundaries

Date: 2026-07-08

Issue: `issues/077_post_first_version_workspace_company_foundation_gate.md`

Owner: 系统交付席

Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace can now define the first minimal CEO-facing company/workspace frame around the accepted local/demo AI Task Executor MVP without unlocking future company, economy, production, or runtime behavior scope.

## Delivery Result

PASS for architecture/product boundary definition.

No implementation or behavior change was made for this issue.

## Boundary Artifacts

- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
- `issues/077_post_first_version_workspace_company_foundation_gate.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `knowledge/PROJECT_MEMORY.md`
- `reviews/074_workspace_company_foundation_boundaries_review.md`

## Boundary Summary

Workspace Company Foundation is defined as a bounded local/demo company shell over accepted Workspace state:

- tenant/workspace context;
- minimal company identity concept;
- existing department catalog/types and department instances;
- accepted model preference read model;
- accepted task console state and task APIs;
- Project Memory source references;
- local/demo release status.

It is not a full L5 company organization system and does not approve implementation.

## First Implementation Slice Boundary

Recommended first implementation slice after quality acceptance:

- minimal local/demo Workspace company frame in the existing operation console or a separately approved read-model layer;
- company/workspace identity label;
- current local/demo release status;
- current tenant/default workspace context;
- active model preference summary;
- existing task console entry point/status summary;
- Project Memory/source-of-truth pointers;
- bounded department catalog/instance summary only if existing read access exists or a read-model gap is separately approved.

Read-model gap rule:

- If implementation needs a new backend read API for company identity or department summaries, 系统交付席 must document the exact read-model gap and route back for approval before implementation.
- No new persistence table is approved by this boundary.

## Forbidden Scope Confirmed

- Hosted production deployment.
- Admin Platform implementation or platform management UI.
- Billing, ROI, packages, marketplace, or L6 economy behavior.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Business modules or external business-platform connectors.
- Secret input, secret display, credential persistence, provider account editing, provider SDK, direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes, persistence/schema changes, execution-loop changes, tool routing changes, workflow mutation, runtime behavior changes, or automatic evolution behavior changes.

## Verification Performed

Documentation/package whitespace check:

```bash
git diff --check
```

Result: passed.

Staged behavior-file scope guard:

```bash
git diff --cached --name-only -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
```

Result: no backend/frontend behavior files changed.

Boundary scope scan:

```bash
rg -n "implementation|behavior change|hosted production|Admin Platform|billing|ROI|packages|marketplace|Employee CRUD|employee expansion|complex company organization|business modules|secret|provider SDK|direct provider|New API internal|Task API payload|execution-loop|runtime behavior|read-model gap|new persistence table" docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md issues/077_post_first_version_workspace_company_foundation_gate.md reviews/074_workspace_company_foundation_boundaries_review.md
```

Expected result: boundary explicitly preserves or blocks these scopes.

Result: boundary terms are present in ADR-0031, the issue, and this review.

## Verification Checklist For 质量运行席

Confirm:

- ADR-0031 is boundary-only and does not approve implementation;
- boundary connects existing tenant id, company identity concept, department catalog/instances, model preference, task console, and Project Memory as one bounded Workspace frame;
- first implementation slice remains minimal and local/demo;
- any missing company/department read model is routed back as a documented gap before implementation;
- no backend/frontend behavior files were changed;
- source-of-truth status files route next work to quality verification.

## Quality Verification

Quality Result: PASS.

Commands: commit diff check, behavior-file scope guard, secret scan, ADR section/scope scan, source-of-truth routing check, and artifact existence check.

Evidence: boundary commit `651bdb99` contains ADR-0031, issue/review, architecture note, and source-of-truth status files only; behavior-file guard returned no backend app/tests, frontend app, Admin Platform, Workspace, shared, deploy, tools, or data files; ADR-0031 includes product boundary, architecture boundary, source ownership, first-slice boundary, read-model gap rule, and verification plan.

Risks: hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secret persistence/display, provider SDK/direct provider calls, New API source/internal DB dependency, Task API payload changes, execution-loop/runtime behavior changes, and automatic evolution behavior remain blocked.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

Detailed evidence:

```bash
git show --name-only --oneline 651bdb99
git diff --check 651bdb99^ 651bdb99
git diff --name-only 651bdb99^ 651bdb99
git diff --name-only 651bdb99^ 651bdb99 -- backend/app backend/tests frontend/app admin-platform workspace shared deploy tools data
rg -n --pcre2 '(^|[^A-Za-z])sk-(?!placeholder|your|test|example)[A-Za-z0-9_-]{32,}|sk-or-v1-[A-Za-z0-9_-]{32,}|(api[_-]?key|authorization|bearer)\s*[:=]\s*[A-Za-z0-9._-]{16,}' docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md issues/077_post_first_version_workspace_company_foundation_gate.md reviews/074_workspace_company_foundation_boundaries_review.md PROJECT_STATUS.md TASKS.md knowledge/003_Architecture.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
rg -n "Product Boundary|Architecture Boundary|Source Ownership|First Implementation Slice Boundary|Read-model gap rule|Verification Plan|not a full L5|does not approve implementation|No new persistence table|Hosted production|Admin Platform|Billing|ROI|Employee CRUD|complex company organization|Business modules|Secret|provider SDK|direct provider|Task API payload|execution-loop|runtime behavior|automatic evolution|ModelGatewayAdapter" docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md
```

## Handoff

Issue: `issues/077_post_first_version_workspace_company_foundation_gate.md`
Objective: Close out Workspace Company Foundation architecture/product boundary after product acceptance.
Special Constraints: Boundary accepted only; implementation remains separately gated. No implementation or behavior change is approved by this acceptance.
Next Seat: main thread closeout

## Product Acceptance

Product Decision: ACCEPTED.

Priority: move from accepted boundary to first-slice gate.

Scope: accept ADR-0031 as the current Workspace Company Foundation boundary.

Acceptance Criteria:

- ADR-0031 remains boundary-only and does not approve implementation;
- first slice remains minimal local/demo company frame or approved read-model layer;
- read-model gaps must route back before implementation;
- hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, direct provider calls, Task API changes, execution-loop/runtime changes, and automatic evolution behavior remain blocked;
- quality verification passed with no blockers.

Source Of Truth Updates: `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark T-190 accepted and open the next first-slice gate.

Next Seat: 总控决策席 for first-slice gate review.

Open Questions: none for boundary acceptance.

Handoff: final closeout
