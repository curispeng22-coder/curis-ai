# CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001 REVIEW

Status: Review

Authority Class: REVIEW / EVIDENCE

Disposition: M2.5A IMPLEMENTED / CLOSED; M2.5B UI-HOLD; CEO REVIEW REQUIRED

Date: 2026-08-27

## Verdict

The existing Team Operating adapter now resolves a canonical General Work's bounded execution context from its existing Cycle, Business, Workspace, Assignment and Employee truth. It does not create or copy a second Context, Memory, Knowledge, Prompt, Project, Workflow or Runtime system.

## M2.5A implemented truth

- A canonical child Work resolves its `GENERAL_WORK_CYCLE` and verifies Cycle/Work Company and Workspace identity.
- The Provider Task receives canonical Business identity/name/goal/positioning, Workspace identity/name/purpose, Work problem/expected result/constraints/input refs/why, and current Employee role/responsibility.
- Existing selected Result/Artifact/Evidence refs remain reference-first through Responsibility Routing; whole Workspace, history, conversation, Memory and Knowledge are not hydrated.
- Curis-owned Runtime/Task/Artifact references that resolve outside the current tenant, Company or Workspace fail closed before `begin_employee_execution()` and before Provider launch. Opaque external source refs remain references rather than invented bodies.
- A Provider `REJECTED` result persists the exact `problem` plus `恢复方式：补充所需输入后继续同一工作。` in the existing execution record. Work remains `WAITING`, Holder remains and Current Executor clears.
- Existing `CONTINUE` plus selected truth refs resumes the same Work. The existing execution key/claim prevents duplicate active execution; completed replay does not create another Provider call or Result.
- Non-General child Work and legacy Team Operating prompt/context behavior remain unchanged.

## Runtime evidence

Repository-external isolated SQLite tests proved:

1. Provider submit payload contains the real Business, Workspace, Cycle contract, Employee role and selected input ref.
2. Prompt is bounded for the accepted scenario and reports `copiedConversationHistory = false`, `hydratedBodiesCount = 0`.
3. First Provider result `REJECTED: 缺少客户反馈数据` produces Work `WAITING`, durable exact reason/recovery, retained Holder and no Current Executor.
4. Runtime is reopened on the same isolated SQLite and rereads the same execution truth.
5. Adding `source:customer-feedback`, continuing and executing the same Work creates one second bounded attempt, reaches `COMPLETED`, and replay creates no third call.
6. Cross-tenant and same-tenant/cross-Company Evidence refs both return HTTP 422 before any Employee/Provider callback.
7. An invalid/quarantined canonical parent returns HTTP 422 before Provider launch.

The accepted earlier M2 live `codex-cli 0.144.6` proof was not rerun. This closure verifies the corrected Provider input at the real Team Operating submit boundary with a deterministic adapter; it does not claim a new external-model-quality result.

## Tests

- General Work context + canonical usage attribution: `14 passed`.
- General/Team/Responsibility/RD real execution combined regression: `31 passed` (includes the preceding 14).
- First Run, Context, Backend DB Safety, RD Phase 2B and XHS regression: `12 passed`.
- Distinct accepted total: `43 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.

All pytest runs set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one repository-external temporary SQLite.

## M2.5B decision

`UI-HOLD`.

The backend `FirstRunDelivery` and `materialize-first-general-workspace` contract already persist normalized goal, positioning and intent summary. The current onboarding working copy is preserved mixed-source and intentionally sends only an opaque intent reference. Deciding how natural language becomes editable normalized fields changes final First Run interaction semantics; adding an unused runtimeApi wrapper would not close capture truth. No frontend file was modified.

## Changed files

- `backend/app/api/team_operating_router.py`
- `backend/tests/test_v1_general_operating_contract.py`
- `backend/tests/test_canonical_usage_attribution.py`
- `issues/CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001.md`
- `docs/reviews/CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001_review.md`
- bounded status-only updates in the existing Epic and `CURRENT_STATE.md`

`backend/app/runtime/responsibility_routing.py`, frontend, schema, active databases, RD and Content Growth implementation were not modified by this Issue.

## Remaining gates

- M2.5A: CLOSED.
- M2.5B: UI-HOLD pending accepted First Run interaction semantics.
- M3 durable native Keychain: independently SECURITY BLOCKED.
- M4 RD canonical integration and M5 Content Growth headless: not started by this Issue.

No commit or push was created.

STOP FOR CEO M2.5 IMPLEMENTATION REVIEW.
