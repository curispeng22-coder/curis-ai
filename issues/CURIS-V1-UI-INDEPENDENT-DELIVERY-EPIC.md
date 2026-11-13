# CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC

Status: REVIEW — M1 CLOSED / M2 CLOSED / M2.5A CLOSED / M2.5B UI-HOLD / M3 SECURITY BLOCKED / M4 CLOSED / M5 CLOSED HEADLESS

Owner: Main Development / Runtime Integration

Date: 2026-08-26

## Goal

Close the V1 backend/runtime/API/projection/recovery work that does not require accepted final UI. M1 is bounded to:

`FoundingRun → Company + CEO Assistant + real Department + canonical Business + first Generic Workspace`

The creation boundary is transactional, duplicate-safe, restart-readable and resolvable through the canonical parent path.

## Authority

- `docs/00_Context/CURRENT_STATE.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/reviews/CURIS_V1_APP_READINESS_AUDIT.md`
- `docs/reviews/CURIS_V1_DEVELOPMENT_MASTER_PLAN.md`
- `docs/reviews/CURIS_V1_UI_DEPENDENCY_MATRIX.md`
- accepted Canonical Business Spine and Workspace Package reviews

## Pre-change baseline

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Preserved worktree: 76 modified, 2 deleted, 432 untracked paths at preflight.
- Active DB fingerprints are recorded in `CURIS_V1_APP_READINESS_AUDIT.md` and must remain unchanged.

### M1 owned clean source hashes

| Path | Pre-change SHA-256 |
|---|---|
| `backend/app/runtime/foundation.py` | `206810ddfd26a1c33ba70644c2da03f74108076f9b7a6d6c57d3729556e358c8` |
| `backend/app/runtime/business_spine.py` | `d3e26c753c2f8b918fe2430e3dd857b6da73382440d869061ffd1c0efd186f89` |
| `backend/app/api/runtime_foundation_router.py` | `7750369eaab7a9bf395d5a6de3af08dc885710d63077f800b760bdd906eb0b37` |

## M1 Allowed Files

- `backend/app/runtime/foundation.py`
- `backend/app/runtime/business_spine.py`
- `backend/app/runtime/first_run_delivery.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_v1_first_run_delivery.py`
- `docs/reviews/CURIS_V1_UI_DEPENDENCY_MATRIX.md`
- `docs/reviews/CURIS_V1_UI_INDEPENDENT_DELIVERY_REPORT.md`
- `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md`
- `issues/CURIS-V1-UI-INDEPENDENT-DELIVERY-EPIC.md`

## Explicit Exclusions

- No final First Run UI.
- No frontend changes in M1.
- No new Company, Business, Workspace, Employee, Work, Result, Decision or Workflow primitive.
- No professional Domain lifecycle for Generic Workspace.
- No Package marketplace or generated professional UI.
- No active DB initialization/migration/write.
- No RD/XHS/TTK changes.
- No commit or push before milestone acceptance.

## M1 Contract

- Existing Company/Assistant may be reused only when identity and request match.
- IDs generated from the FoundingRun are stable across retries.
- A real `business.general` Department is created in the same transaction when absent.
- Generic Workspace is a canonical DRAFT Workspace with no invented professional stages.
- Cancelled FoundingRun creates no Company/Department/Business/Workspace.
- Any failure rolls back every object created by the request.
- Retry returns the original IDs and creates no duplicate.
- Restart returns the same FoundingRun, Business, Workspace and parent resolver result.

## Acceptance

1. Success creates exactly one Company, Assistant, Department, Business and Workspace.
2. Workspace parent resolves to Business → Department → Company.
3. Retry is idempotent.
4. Cancel creates nothing.
5. Injected/validation failure creates nothing partial.
6. Restart reads the same IDs.
7. Legacy company-only materialization remains compatible.
8. Existing Business Spine, FoundingRun and Package tests pass.
9. Active DB fingerprints remain unchanged.

## Stop gates

Stop on Frozen Authority conflict, new Runtime primitive requirement, destructive schema change, active DB risk, or ownership collision in an Allowed File.

## M2 bounded extension — General Workspace read contract

Goal: expose a stable, UI-independent General Workspace overview from existing canonical Business, Shared Workspace and Team Operating facts. It must not infer or fabricate a Team.

Allowed Files:

- `backend/app/shared_workspace_projection.py`
- `backend/app/api/shared_workspace_router.py`
- `backend/tests/test_v1_general_workspace_contract.py`
- `backend/app/runtime/child_work.py`
- `backend/app/runtime/general_workspace_delivery.py`
- `backend/tests/test_v1_general_operating_contract.py`
- this Issue and the Epic matrix/report/backlog

Explicit exclusions: no automatic role inference, no Employee creation, no Work/Workflow primitive, no provider execution change, no final Workspace UI.

Truth rule: zero or ambiguous Workspace responsibility definitions, or no eligible Employee, returns `NEEDS_DECISION` without creating Runtime objects.

The ordinary-language command may reuse an existing unique Workspace responsibility workflow and its eligible Employee. It may atomically create one existing `CYCLE` plus one canonical child `WORK`, then attach the existing Responsibility Routing contract. It must not create or infer a Workflow, Role, Employee or capability binding.

### M2 implemented boundary

- `problem + expected_result + constraints + references` creates one atomic existing `CYCLE` plus canonical child `WORK` after resolving one published Workspace responsibility workflow, one canonical Employee and one active capability binding.
- Missing or ambiguous responsibility, Employee or capability returns a responsibility gap and writes no Cycle/Work.
- Replay returns the same Cycle/Work; a conflicting replay fails; restart preserves the same identities.
- The Work is attached to existing Responsibility Routing with a real holder and `currentExecutorRef = null` before Provider execution.

### M2 architecture stop gate — CLOSED 2026-08-27

The live isolated Provider proof reaches the accepted Team Operating execution path, creates a real ResultStore Task, and then fails closed before launching Codex with `business model call attribution is incomplete`.

Root cause: `execute_model_gateway()` and `AIUsageService` currently require `Task → Project → Department` lineage. Current Product Authority defines `Project` as a legacy compatibility object and explicitly states that new canonical Business Spine creation does not write Project. A General Workspace therefore has canonical `Workspace → Business → Department → Company` attribution but no legitimate Project attribution.

The bounded shared implementation in `CURIS-CANONICAL-USAGE-ATTRIBUTION-001` now accepts verified canonical Business/Workspace/Work/Execution attribution in the existing ledger while preserving verified legacy Project attribution. No synthetic Project or validation bypass was added. A real installed Codex provider launched from a General Workspace with no Project, persisted canonical usage/Result/Artifact/Evidence, and was reread after restart. M2's attribution architecture and execution blocker is closed.

The provider truthfully rejected the requested business outcome because the supplied Work context lacked sufficient facts, so the Work remained `WAITING`. That is a separate General Workspace context-assembly product gap and is not represented as successful business completion.

### M2.5 context closure — IMPLEMENTED / CEO REVIEW REQUIRED

`CURIS-V1-M2.5-GENERAL-WORKSPACE-CONTEXT-001` now supplies bounded canonical Business/Workspace/Cycle/Work/Employee truth and selected references to the existing Provider Task. Missing facts remain `REJECTED → WAITING` with durable exact reason/recovery; same-Work retry and cross-scope fail-closed behavior are verified. M2.5A is closed. M2.5B is `UI-HOLD` because the current preserved onboarding adapter needs accepted interaction semantics to convert natural language into normalized First Run fields; no frontend change was made.

## M4/M5 bounded completion

`CURIS-V1-M4-M5-CONTINUOUS-DELIVERY-001` closes the remaining UI-independent RD
canonical integration and Content Growth headless assembly. RD reuses its accepted
Project/Cycle domain model but now owns canonical Work/Responsibility and one canonical
usage lineage. Content Growth uses a canonical Generic Workspace and shared child Work,
Team Operating, Result/Evidence and Handoff; it does not create XHS/channel Workspace
identity or fake publication/analytics. Evidence is recorded in
`docs/reviews/CURIS_V1_M4_M5_CONTINUOUS_DELIVERY_REVIEW.md`.

## Current gate

The repository has only `LocalDevCredentialBackend`, whose secret disappears with the
process. No reusable OS Keychain backend is registered. M3 cannot be accepted without a
bounded security design and native packaged implementation; command-line plaintext,
environment variables and files are prohibited substitutes. M3 remains independently
blocked. M2.5B is UI-HOLD. M4 and M5 are closed at the UI-independent boundary; final
UI/Browser/Packaged delivery remains outside this Epic.
